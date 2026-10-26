"""The search space.

A *convention* is one complete way of reading a digit string against a text:

    unit x tokenizer x read x start x counting base x digit grouping

A *view* is everything except base and grouping: the ordered stream of items
(words, letters, lines...) that the numbers index into, stored paragraph by
paragraph so that the paragraph-shuffle null can rebuild it cheaply.

Views that turn out to be identical for a given text (for example 'line'
and 'paragraph' when the text has no hard line breaks) are merged and listed
as aliases, so the search-space count is never inflated by duplicates.
"""
from __future__ import annotations

from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

from .digits import GROUPINGS, DigitString, distinct_groupings
from .text import (TOKENIZERS, Text, fold, letter_code, line_spans, sentence_spans,
                   tokenize)

UNITS = ("word", "letter", "nonspace", "line", "sentence", "paragraph")
UNIT_HELP = {
    "word": "the n-th word (depends on the tokenizer)",
    "letter": "the n-th letter (a-z and accented letters; spaces, digits, punctuation skipped)",
    "nonspace": "the n-th character that is not a space (punctuation and digits count)",
    "line": "the n-th non-empty line of the file",
    "sentence": "the n-th sentence",
    "paragraph": "the n-th paragraph (the title is paragraph 1 when counting from the title)",
}
READS = {
    "word": ("item", "initial"),
    "letter": ("char",),
    "nonspace": ("char",),
    "line": ("item", "initial"),
    "sentence": ("item", "initial"),
    "paragraph": ("item", "initial"),
}
READ_HELP = {
    "item": "take the whole word (for line/sentence/paragraph: its first word)",
    "initial": "take only the first letter of that word (classic book cipher)",
    "char": "take the character itself",
}
BASES = (0, 1)
DEFAULT_STARTS = ("title", "body")
START_HELP = {
    "title": "count from the very first line (the title counts)",
    "body": "count from the first paragraph after the title",
    "marker": "count from the start of the line containing the marker text",
}


class Config:
    """Which dimensions to search.  Defaults = everything."""

    def __init__(self, mode: str, units: Sequence[str] = UNITS, tokenizers: Sequence[str] = TOKENIZERS,
                 bases: Sequence[int] = BASES, starts: Sequence[str] = DEFAULT_STARTS,
                 markers: Sequence[str] = (), groupings: Sequence[str] = GROUPINGS):
        if mode not in ("targets", "letters"):
            raise ValueError("score must be 'targets' or 'letters'")
        for name, given, allowed in (("unit", units, UNITS), ("tokenizer", tokenizers, TOKENIZERS),
                                     ("base", bases, BASES), ("start", starts, DEFAULT_STARTS),
                                     ("grouping", groupings, GROUPINGS)):
            bad = [g for g in given if g not in allowed]
            if bad or not given and name != "start":
                raise ValueError("bad %s list %r; allowed: %s" % (name, list(given), list(allowed)))
        if not starts and not markers:
            raise ValueError("need at least one start point")
        self.mode = mode
        self.units = tuple(u for u in UNITS if u in units)
        self.tokenizers = tuple(t for t in TOKENIZERS if t in tokenizers)
        self.bases = tuple(b for b in BASES if b in bases)
        self.starts = tuple(s for s in DEFAULT_STARTS if s in starts)
        self.markers = tuple(markers)
        self.groupings = tuple(g for g in GROUPINGS if g in groupings)

    def is_restricted(self) -> bool:
        return (self.units != UNITS or self.tokenizers != TOKENIZERS or self.bases != BASES
                or self.starts != DEFAULT_STARTS or self.groupings != GROUPINGS)

    def to_dict(self) -> dict:
        return {"score": self.mode, "units": list(self.units), "tokenizers": list(self.tokenizers),
                "bases": list(self.bases), "starts": list(self.starts), "markers": list(self.markers),
                "groupings": list(self.groupings)}

    @classmethod
    def from_dict(cls, d: dict) -> "Config":
        return cls(d["score"], d["units"], d["tokenizers"], d["bases"], d["starts"],
                   d["markers"], d["groupings"])


class View:
    def __init__(self, name: str, kind: str, para_codes: List[np.ndarray], para_disp: List[List[str]],
                 start: Tuple):
        self.name = name
        self.aliases = [name]
        self.kind = kind                      # "item" (vocab ids) or "letter" (0..25)
        self.para_len = np.array([len(c) for c in para_codes], dtype=np.int64)
        self.para_base = np.concatenate([[0], np.cumsum(self.para_len)[:-1]]).astype(np.int64)
        self.flat = (np.concatenate(para_codes) if para_codes else np.zeros(0)).astype(np.int64)
        self.disp = [d for ds in para_disp for d in ds]
        self.start = start                    # ("slot", s) or ("anchor", para, offset)
        if start[0] == "slot":
            self.start_flat = int(self.para_base[start[1]])
        else:
            self.start_flat = int(self.para_base[start[1]] + start[2])
        self.signature = (kind, start, tuple(c.tobytes() for c in para_codes))


class Convention:
    def __init__(self, view_index: int, view: View, grouping_aliases: List[str], base: int):
        self.view_index = view_index
        self.grouping = grouping_aliases[0]
        self.base = base
        self.name = "%s | %d-based | digits=%s" % (view.name, base, self.grouping)
        self.aliases = ["%s | %d-based | digits=%s" % (v, base, g)
                        for v in view.aliases for g in grouping_aliases]
        self.unit = view.name.split(" ")[0]


def _unit_items(p: str, unit: str, tok: Optional[str]) -> List[Tuple[str, str, int, int]]:
    """(display, foldable text, start, end) for every item of a paragraph."""
    if unit == "word":
        return [(t, t, a, b) for t, a, b in tokenize(p, tok)]
    if unit == "letter":
        return [(c, c, i, i + 1) for i, c in enumerate(p) if c.isalpha()]
    if unit == "nonspace":
        return [(c, c, i, i + 1) for i, c in enumerate(p) if not c.isspace()]
    spans = {"line": line_spans, "sentence": sentence_spans,
             "paragraph": lambda s: [(s, 0, len(s))]}[unit](p)
    out = []
    for s, a, b in spans:
        first = tokenize(s, "strip")
        w = first[0][0] if first else ""
        out.append((w, w, a, b))
    return out


class TextViews:
    """All distinct views of one text, plus the shared vocabulary of folded
    words used by 'item' views."""

    def __init__(self, text: Text, cfg: Config):
        self.text = text
        self.vocab: Dict[str, int] = {"": 0}
        self.views: List[View] = []
        self.warnings: List[str] = []
        self.n_merged = 0
        by_sig: Dict[tuple, int] = {}

        starts = []
        for s in cfg.starts:
            if s == "body" and len(text.paragraphs) < 2:
                self.warnings.append("start 'body' skipped: %s has no paragraph after the title" % text.label)
                continue
            starts.append((s, None))
        for m in cfg.markers:
            found = text.find_marker(m)
            if found is None:
                self.warnings.append("marker %r not found in %s; that start point is skipped for this text"
                                     % (m, text.label))
            else:
                starts.append(("marker:" + m, found))

        for unit in cfg.units:
            toks = cfg.tokenizers if unit == "word" else (None,)
            for tok in toks:
                items = [_unit_items(p, unit, tok) for p in text.paragraphs]
                for read in READS[unit]:
                    kind = "item" if read == "item" else "letter"
                    if cfg.mode == "letters" and kind == "item":
                        continue
                    codes, disp = [], []
                    for its in items:
                        if kind == "item":
                            codes.append(np.array([self._vid(fold(f)) for _, f, _, _ in its], dtype=np.int64))
                        else:
                            codes.append(np.array([letter_code(f) for _, f, _, _ in its], dtype=np.int64))
                        disp.append([d for d, _, _, _ in its])
                    for sname, found in starts:
                        if found is None:
                            start = ("slot", 0 if sname == "title" else 1)
                        else:
                            pi, line_start, _ = found
                            off = next((k for k, it in enumerate(items[pi]) if it[3] > line_start),
                                       len(items[pi]))
                            start = ("slot", 0) if (pi == 0 and off == 0) else ("anchor", pi, off)
                        parts = [unit] + ([tok] if tok else []) + [read, "from=" + sname]
                        v = View(" ".join([parts[0]] + ["| " + x for x in parts[1:]]), kind, codes, disp, start)
                        if v.signature in by_sig:
                            self.views[by_sig[v.signature]].aliases.append(v.name)
                            self.n_merged += 1
                        else:
                            by_sig[v.signature] = len(self.views)
                            self.views.append(v)

    def _vid(self, key: str) -> int:
        if key not in self.vocab:
            self.vocab[key] = len(self.vocab)
        return self.vocab[key]

    def vocab_list(self) -> List[str]:
        out = [""] * len(self.vocab)
        for k, i in self.vocab.items():
            out[i] = k
        return out


def build_conventions(tv: TextViews, ds: DigitString, cfg: Config):
    """Returns (conventions, grouping alias lists)."""
    groups = distinct_groupings(ds, cfg.groupings)
    convs = []
    for vi, v in enumerate(tv.views):
        for ga in groups:
            for b in cfg.bases:
                convs.append(Convention(vi, v, ga, b))
    return convs, groups
