"""Command line: python3 -m indexkit <command> ...

Commands: selftest, demo, conventions, run, prereg.  Everything except
selftest is locked until selftest has passed for the current code.
"""
from __future__ import annotations

import argparse
import datetime
import os
import sys
from typing import List, Optional

from . import __version__, gate, prereg
from .conventions import BASES, DEFAULT_STARTS, UNITS, Config, TextViews, build_conventions
from .digits import GROUPINGS, DigitString
from .engine import MIN_DRAWS, analyse
from .report import conventions_help, markdown, null_sentence, terminal_summary
from .scoring import read_word_file
from .text import TOKENIZERS, Text, sha256_file
from .wordlists import builtin_name, builtin_wordlist

DEFAULT_SEED = 1856
DEFAULT_THRESHOLD = 0.01


def _csv(s: Optional[str], allowed, cast=str):
    if s is None:
        return list(allowed)
    out = [cast(x.strip()) for x in s.split(",") if x.strip()]
    return out


def _parse_text_arg(arg: str):
    if "=" in arg:
        label, path = arg.split("=", 1)
        if label and "/" not in label and "\\" not in label:
            return label.strip(), path.strip()
    return os.path.splitext(os.path.basename(arg))[0], arg


def add_input_args(p: argparse.ArgumentParser, with_run_options: bool = True) -> None:
    p.add_argument("--digits", help='the digit string, in quotes, e.g. "810-419-227"')
    p.add_argument("--text", action="append", default=[], metavar="LABEL=FILE",
                   help="a plain .txt file, optionally labelled (en=article_en.txt). Repeat for each language.")
    p.add_argument("--targets", metavar="FILE", help="file with one target word/name per line (what counts as a hit)")
    p.add_argument("--wordlist", metavar="FILE", help="file with one word per line for the letters score")
    p.add_argument("--score", choices=("targets", "letters"),
                   help="targets (needs --targets) or letters. Default: targets if --targets is given, else letters")
    p.add_argument("--marker", action="append", default=[], metavar="TEXT",
                   help='extra start point: the line containing TEXT. Use "English|Français" for both languages.')
    p.add_argument("--units", help="restrict units (comma list from: %s)" % ",".join(UNITS))
    p.add_argument("--tokenizers", help="restrict tokenizers (from: %s)" % ",".join(TOKENIZERS))
    p.add_argument("--bases", help="restrict counting base (0,1)")
    p.add_argument("--starts", help="restrict start points (from: title,body)")
    p.add_argument("--groupings", help="restrict digit groupings (from: %s)" % ",".join(GROUPINGS))
    if with_run_options:
        p.add_argument("--draws", type=int, default=MIN_DRAWS,
                       help="draws per null and per stage (minimum and default %d)" % MIN_DRAWS)
        p.add_argument("--seed", type=int, default=DEFAULT_SEED, help="random seed (default %d)" % DEFAULT_SEED)
        p.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD,
                       help="pass threshold before splitting over texts (default %g)" % DEFAULT_THRESHOLD)


class Inputs:
    """Everything a run needs, loaded and checked."""

    def __init__(self, a: argparse.Namespace):
        if not a.digits:
            raise SystemExit("Please give the digit string, e.g.  --digits \"810-419-227\"")
        if not a.text:
            raise SystemExit("Please give at least one text, e.g.  --text en=article_en.txt")
        self.ds = DigitString(a.digits)
        self.texts: List[Text] = []
        seen = set()
        for t in a.text:
            label, path = _parse_text_arg(t)
            if not os.path.exists(path):
                raise SystemExit("Text file not found: %s" % path)
            if label in seen:
                raise SystemExit("Two texts have the same label %r; label them like en=... fr=..." % label)
            seen.add(label)
            self.texts.append(Text.from_file(label, path))
        mode = a.score or ("targets" if a.targets else "letters")
        if mode == "targets" and not a.targets:
            raise SystemExit("--score targets needs a --targets FILE (one target word per line)")
        self.targets = read_word_file(a.targets) if a.targets else None
        self.targets_path = a.targets
        self.targets_sha = sha256_file(a.targets) if a.targets else None
        self.wordlist_path = a.wordlist
        self.wordlist = read_word_file(a.wordlist) if a.wordlist else None
        self.wordlist_sha = sha256_file(a.wordlist) if a.wordlist else None
        self.cfg = Config(mode, units=_csv(a.units, UNITS), tokenizers=_csv(a.tokenizers, TOKENIZERS),
                          bases=_csv(a.bases, BASES, int), starts=_csv(a.starts, DEFAULT_STARTS),
                          markers=a.marker, groupings=_csv(a.groupings, GROUPINGS))
        self.draws = getattr(a, "draws", MIN_DRAWS)
        self.seed = getattr(a, "seed", DEFAULT_SEED)
        self.threshold = getattr(a, "threshold", DEFAULT_THRESHOLD)
        if self.draws < MIN_DRAWS:
            raise SystemExit("--draws must be at least %d" % MIN_DRAWS)
        if not 0 < self.threshold < 1:
            raise SystemExit("--threshold must be between 0 and 1")

    def wordlist_for(self, label: str):
        return self.wordlist if self.wordlist is not None else builtin_wordlist(label)

    def wordlist_desc(self) -> str:
        if self.wordlist_path:
            return "`%s` (%d words, SHA-256 `%s`)" % (self.wordlist_path, len(self.wordlist), self.wordlist_sha)
        return "; ".join("%s: %s" % (t.label, builtin_name(t.label)) for t in self.texts)

    def convention_lists(self):
        out = {}
        for t in self.texts:
            tv = TextViews(t, self.cfg)
            convs, _ = build_conventions(tv, self.ds, self.cfg)
            out[t.label] = [c.name for c in convs]
        return out

    def prereg_spec(self) -> dict:
        lists = self.convention_lists()
        return {
            "indexkit_prereg": prereg.PREREG_VERSION,
            "digits": self.ds.raw,
            "texts": [{"label": t.label, "path": t.path, "sha256": t.sha256} for t in self.texts],
            "score": self.cfg.mode,
            "targets": self.targets,
            "targets_file": ({"path": self.targets_path, "sha256": self.targets_sha} if self.targets_path else None),
            "wordlist_file": ({"path": self.wordlist_path, "sha256": self.wordlist_sha} if self.wordlist_path
                              else "built-in"),
            "config": self.cfg.to_dict(),
            "search_space": {k: len(v) for k, v in lists.items()},
            "conventions": lists,
            "null": {"statement": null_sentence([len(v) for v in lists.values()], self.draws),
                     "draws": self.draws, "seed": self.seed},
            "threshold": self.threshold,
            "pass_rule": "a text passes if max(pA, pB) <= threshold / number of texts",
        }


def _inputs_from_prereg(path: str, a: argparse.Namespace):
    spec, digest = prereg.load(path)
    overrides = [n for n in ("digits", "targets", "wordlist", "score", "units", "tokenizers", "bases",
                             "starts", "groupings") if getattr(a, n)]
    overrides += ["text"] if a.text else []
    overrides += ["marker"] if a.marker else []
    overrides += [n for n, d in (("draws", MIN_DRAWS), ("seed", DEFAULT_SEED), ("threshold", DEFAULT_THRESHOLD))
                  if getattr(a, n) != d]
    if overrides:
        raise SystemExit("REFUSED: --prereg fixes everything; remove these options: --%s" % ", --".join(overrides))
    for t in spec["texts"]:
        if not os.path.exists(t["path"]):
            raise SystemExit("REFUSED: registered text %s not found." % t["path"])
        if sha256_file(t["path"]) != t["sha256"]:
            raise SystemExit("REFUSED: %s changed since pre-registration (SHA-256 differs)." % t["path"])
    for key in ("targets_file", "wordlist_file"):
        f = spec.get(key)
        if isinstance(f, dict):
            if not os.path.exists(f["path"]) or sha256_file(f["path"]) != f["sha256"]:
                raise SystemExit("REFUSED: %s is missing or changed since pre-registration." % f["path"])
    c = spec["config"]
    ns = argparse.Namespace(
        digits=spec["digits"], text=["%s=%s" % (t["label"], t["path"]) for t in spec["texts"]],
        targets=(spec["targets_file"] or {}).get("path"),
        wordlist=spec["wordlist_file"]["path"] if isinstance(spec["wordlist_file"], dict) else None,
        score=spec["score"], marker=c["markers"], units=",".join(c["units"]),
        tokenizers=",".join(c["tokenizers"]), bases=",".join(str(b) for b in c["bases"]),
        starts=",".join(c["starts"]), groupings=",".join(c["groupings"]),
        draws=spec["null"]["draws"], seed=spec["null"]["seed"], threshold=spec["threshold"])
    inp = Inputs(ns)
    if inp.targets is not None and inp.targets != spec["targets"]:
        raise SystemExit("REFUSED: the target list differs from the pre-registration.")
    if inp.convention_lists() != spec["conventions"]:
        raise SystemExit("REFUSED: the conventions this version of indexkit would try differ from the "
                         "pre-registered list. Use the indexkit version you registered with.")
    return inp, "`%s` (SHA-256 `%s`)" % (path, digest)


def _progress(label):
    def f(which, stream, done, total):
        if done == total:
            print("  [%s] null %s, %s draws: %d done" % (label, which, "reference" if stream == 0 else "test", total))
    return f


def do_run(inp: Inputs, out: str, prereg_note: Optional[str] = None, quiet: bool = False) -> List[dict]:
    if inp.cfg.is_restricted() and not prereg_note:
        print("WARNING: you restricted the search space. That is only honest if you decided on the "
              "restriction BEFORE looking at any result. Consider `prereg`.")
    print("Null hypothesis: " + null_sentence([len(v) for v in inp.convention_lists().values()], inp.draws))
    results = []
    for t in inp.texts:
        print("Analysing %s (%s)..." % (t.label, t.path))
        r = analyse(t, inp.ds, inp.cfg, inp.draws, inp.seed, targets=inp.targets,
                    wordlist=inp.wordlist_for(t.label), progress=_progress(t.label))
        results.append(r)
    info = {
        "version": __version__, "code_hash": gate.code_hash(), "when": datetime.date.today().isoformat(),
        "digits": inp.ds.raw, "shape": inp.ds.shape(), "n_digits": inp.ds.n_digits,
        "score": inp.cfg.mode, "targets": inp.targets or [], "targets_path": inp.targets_path,
        "targets_sha256": inp.targets_sha, "wordlist_desc": inp.wordlist_desc(),
        "markers": list(inp.cfg.markers), "draws": inp.draws, "seed": inp.seed, "threshold": inp.threshold,
        "prereg": prereg_note, "units": list(inp.cfg.units), "tokenizers": list(inp.cfg.tokenizers),
        "starts": list(inp.cfg.starts), "bases": list(inp.cfg.bases), "groupings": list(inp.cfg.groupings),
        "restricted": (", ".join("%s=%s" % (k, ",".join(str(x) for x in v)) for k, v in inp.cfg.to_dict().items()
                                 if k in ("units", "tokenizers", "bases", "starts", "groupings"))
                       if inp.cfg.is_restricted() else None),
    }
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(markdown(info, results))
    if not quiet:
        print(terminal_summary(info, results))
    print("Report written to %s" % out)
    return results


def cmd_conventions(a) -> None:
    inp = Inputs(a)
    print(conventions_help())
    print("")
    for t in inp.texts:
        tv = TextViews(t, inp.cfg)
        convs, groups = build_conventions(tv, inp.ds, inp.cfg)
        print("=== %s: %d conventions ===" % (t.label, len(convs)))
        for w in tv.warnings:
            print("warning: " + w)
        for c in convs:
            extra = "   (same as: %s)" % "; ".join(c.aliases[1:]) if len(c.aliases) > 1 else ""
            print("  " + c.name + extra)
        print("=== %s: %d conventions in total (search space) ===" % (t.label, len(convs)))


def cmd_prereg(a) -> None:
    if not a.out:
        raise SystemExit("Please name the pre-registration file, e.g.  --out my_test.prereg.json")
    inp = Inputs(a)
    spec = inp.prereg_spec()
    digest, new = prereg.write(a.out, spec)
    for label, n in spec["search_space"].items():
        print("%s: %d conventions registered" % (label, n))
    if new:
        print("Pre-registration written to %s" % a.out)
    else:
        print("%s already exists with exactly this content; nothing changed." % a.out)
    print("SHA-256: %s" % digest)
    print("Copy this hash somewhere you cannot edit later (send it to a teammate). Then run:")
    print("  python3 -m indexkit run --prereg %s" % a.out)


def cmd_run(a) -> None:
    if a.prereg:
        inp, note = _inputs_from_prereg(a.prereg, a)
        print("Pre-registration verified: %s" % note)
    else:
        inp, note = Inputs(a), None
    do_run(inp, a.out, note)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="python3 -m indexkit",
                                description="Honest test of 'these digits index into this text'.")
    sub = p.add_subparsers(dest="cmd")
    sub.add_parser("selftest", help="check the instrument (must pass before anything else works)")
    d = sub.add_parser("demo", help="made-up article: what a real hit and a coincidence look like")
    d.add_argument("--outdir", default="demo_output", help="folder for demo files (default demo_output)")
    c = sub.add_parser("conventions", help="list every convention that would be tried, and count them")
    add_input_args(c, with_run_options=False)
    r = sub.add_parser("run", help="test a digit string against one or more texts")
    add_input_args(r)
    r.add_argument("--prereg", metavar="FILE", help="run exactly what a pre-registration file says")
    r.add_argument("--out", default="indexkit_report.md", help="report file (default indexkit_report.md)")
    g = sub.add_parser("prereg", help="write a pre-registration file and print its hash")
    add_input_args(g)
    g.add_argument("--out", help="the pre-registration file to create, e.g. my_test.prereg.json")
    return p


def main(argv=None) -> int:
    parser = build_parser()
    a = parser.parse_args(argv)
    if not a.cmd:
        parser.print_help()
        return 0
    if a.cmd == "selftest":
        from .selftest import run_selftest
        return 0 if run_selftest() else 1
    ok, why = gate.check()
    if not ok:
        print("indexkit is locked: %s" % why)
        print("Run this first:  python3 -m indexkit selftest")
        return 2
    try:
        if a.cmd == "demo":
            from .demo import run_demo
            run_demo(a.outdir, do_run, Inputs)
        elif a.cmd == "conventions":
            cmd_conventions(a)
        elif a.cmd == "run":
            cmd_run(a)
        elif a.cmd == "prereg":
            cmd_prereg(a)
    except ValueError as e:
        print("Error: %s" % e)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
