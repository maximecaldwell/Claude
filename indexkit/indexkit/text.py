"""Reading texts: Unicode clean-up, letter folding, tokenizers, and the
paragraph / line / sentence structure that the counting conventions use.

Everything here works on plain Python strings and is deliberately simple,
because the tokenizers are part of the search space and must be easy to
reason about.  Each tokenizer returns (token, start, end) spans so that a
"marker line" can be located inside any kind of unit.
"""
from __future__ import annotations

import hashlib
import re
import unicodedata
from typing import List, Optional, Tuple

Span = Tuple[str, int, int]

# Apostrophe-like characters seen in English and French text.
APOSTROPHES = "'’ʼ‘"

_LIGATURES = {"œ": "oe", "Œ": "oe", "æ": "ae", "Æ": "ae", "ß": "ss"}


def normalize(raw: str) -> str:
    """NFC-normalise, drop a byte-order mark, unify line endings."""
    if raw.startswith("﻿"):
        raw = raw[1:]
    raw = raw.replace("\r\n", "\n").replace("\r", "\n")
    return unicodedata.normalize("NFC", raw)


def fold(s: str) -> str:
    """Reduce a string to plain lowercase a-z letters.

    Accents are removed (é -> e), ligatures expanded (œ -> oe), and anything
    that is not a letter (digits, apostrophes, hyphens, punctuation) is
    dropped.  "Val-d'Or" and "VAL D’OR" both fold to "valdor".
    """
    out = []
    for ch in unicodedata.normalize("NFKD", s):
        ch = _LIGATURES.get(ch, ch)
        for c in ch.casefold():
            if "a" <= c <= "z":
                out.append(c)
    return "".join(out)


def letter_code(s: str) -> int:
    """0..25 for the first folded letter of s, or -1 if s has no letter."""
    f = fold(s)
    return ord(f[0]) - 97 if f else -1


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


# --------------------------------------------------------------------------
# Tokenizers
# --------------------------------------------------------------------------

TOKENIZERS = ("ws", "ws-drop", "strip", "split")

TOKENIZER_HELP = {
    "ws": "split on whitespace only; standalone punctuation such as ':' '–' '«' counts as a word",
    "ws-drop": "split on whitespace, then drop tokens that contain no letter or digit",
    "strip": "split on whitespace, strip punctuation from both ends of each token, drop empty ones",
    "split": "split on whitespace, hyphens and apostrophes too (Val-d'Or -> Val d Or, l'Or -> l Or)",
}

_WS_TOKEN = re.compile(r"\S+")
_ALNUM_RUN = re.compile(r"[^\W_]+")


def _has_alnum(s: str) -> bool:
    return any(c.isalnum() for c in s)


def tokenize(s: str, name: str) -> List[Span]:
    """Tokenize s with the named tokenizer; returns (token, start, end)."""
    if name == "split":
        return [(m.group(), m.start(), m.end()) for m in _ALNUM_RUN.finditer(s)]
    raw = [(m.group(), m.start(), m.end()) for m in _WS_TOKEN.finditer(s)]
    if name == "ws":
        return raw
    if name == "ws-drop":
        return [t for t in raw if _has_alnum(t[0])]
    if name == "strip":
        out = []
        for tok, a, b in raw:
            i, j = 0, len(tok)
            while i < j and not tok[i].isalnum():
                i += 1
            while j > i and not tok[j - 1].isalnum():
                j -= 1
            if i < j:
                out.append((tok[i:j], a + i, a + j))
        return out
    raise ValueError("unknown tokenizer %r (choose from %s)" % (name, ", ".join(TOKENIZERS)))


def tokens(s: str, name: str) -> List[str]:
    """Just the token strings (handy in tests and the REPL)."""
    return [t for t, _, _ in tokenize(normalize(s), name)]


# --------------------------------------------------------------------------
# Lines and sentences inside one paragraph
# --------------------------------------------------------------------------

def line_spans(p: str) -> List[Span]:
    out = []
    pos = 0
    for line in p.split("\n"):
        a = pos + (len(line) - len(line.lstrip()))
        b = pos + len(line.rstrip())
        if b > a:
            out.append((p[a:b], a, b))
        pos += len(line) + 1
    return out


# A sentence ends at . ! ? or … (possibly repeated), optionally followed by
# closing quotes/brackets (French « … » allows a space before the »), and
# then whitespace or the end of the paragraph.
_SENT_END = re.compile(r"[.!?…]+(?:\s*[»”)\]]|[\"'’])*(?=\s|$)")


def sentence_spans(p: str) -> List[Span]:
    out = []
    start = 0
    ends = [m.end() for m in _SENT_END.finditer(p)]
    if not ends or ends[-1] < len(p):
        ends.append(len(p))
    for end in ends:
        seg = p[start:end]
        a = start + (len(seg) - len(seg.lstrip()))
        b = start + len(seg.rstrip())
        if b > a and _has_alnum(p[a:b]):
            out.append((p[a:b], a, b))
        start = end
    return out


# --------------------------------------------------------------------------
# A whole text
# --------------------------------------------------------------------------

class Text:
    """A text split into paragraphs.  Paragraph 0 is always the title (the
    first non-empty line).  Further paragraphs are separated by blank lines.
    """

    def __init__(self, label: str, paragraphs: List[str], path: str = "<built-in>",
                 sha256: Optional[str] = None):
        if len(paragraphs) < 1:
            raise ValueError("text %r is empty" % label)
        self.label = label
        self.paragraphs = paragraphs
        self.path = path
        self.sha256 = sha256 or hashlib.sha256("\n\n".join(paragraphs).encode("utf-8")).hexdigest()

    @classmethod
    def from_string(cls, label: str, raw: str, path: str = "<built-in>",
                    sha256: Optional[str] = None) -> "Text":
        text = normalize(raw)
        lines = text.split("\n")
        i = 0
        while i < len(lines) and not lines[i].strip():
            i += 1
        if i == len(lines):
            raise ValueError("text %r is empty" % label)
        paragraphs = [lines[i].strip()]
        current: List[str] = []
        for line in lines[i + 1:]:
            if line.strip():
                current.append(line.rstrip())
            elif current:
                paragraphs.append("\n".join(current))
                current = []
        if current:
            paragraphs.append("\n".join(current))
        return cls(label, paragraphs, path=path, sha256=sha256)

    @classmethod
    def from_file(cls, label: str, path: str) -> "Text":
        with open(path, "rb") as fh:
            data = fh.read()
        try:
            raw = data.decode("utf-8")
        except UnicodeDecodeError:
            raise ValueError("%s is not UTF-8 text. Re-save it as 'UTF-8' plain text." % path)
        return cls.from_string(label, raw, path=path, sha256=hashlib.sha256(data).hexdigest())

    def word_count(self) -> int:
        return sum(len(tokenize(p, "ws-drop")) for p in self.paragraphs)

    def find_marker(self, marker: str) -> Optional[Tuple[int, int, str]]:
        """Locate a marker line.  `marker` may hold alternatives separated by
        '|' (e.g. "Chapter 2|Chapitre 2"); the first one found wins.  Matching
        ignores case.  Returns (paragraph index, char offset of the line start
        inside that paragraph, the alternative that matched) or None.
        """
        for alt in [a.strip() for a in normalize(marker).split("|") if a.strip()]:
            needle = alt.casefold()
            for pi, p in enumerate(self.paragraphs):
                for line, a, _ in line_spans(p):
                    if needle in line.casefold():
                        return pi, a, alt
        return None
