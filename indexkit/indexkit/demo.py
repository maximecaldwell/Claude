"""`demo`: a made-up bilingual article, one planted index, one coincidence."""
from __future__ import annotations

import argparse
import os

from .demo_article import EN_PARAGRAPHS, FR_PARAGRAPHS, TARGETS, as_file_text

# Planted: word 67, 90 and 143 of the English article, counting words with
# the 'strip' tokenizer, 1-based, from the title -> three place names.
PLANTED = "67-90-143"
# Not planted: a string chosen only because some conventions happen to pick
# out place names.  It looks exciting and means nothing.
COINCIDENCE = "130-315-814"


def _write(path: str, content: str) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)


def run_demo(outdir: str, do_run, Inputs) -> None:
    os.makedirs(outdir, exist_ok=True)
    en = os.path.join(outdir, "demo_article_en.txt")
    fr = os.path.join(outdir, "demo_article_fr.txt")
    places = os.path.join(outdir, "demo_places.txt")
    _write(en, as_file_text(EN_PARAGRAPHS))
    _write(fr, as_file_text(FR_PARAGRAPHS))
    _write(places, "# what counts as a hit in the demo (one per line)\n" + "\n".join(TARGETS) + "\n")
    print("Wrote the made-up article and place list to %s/" % outdir)

    runs = [
        ("REAL HIT", PLANTED, "demo_report_real_hit.md",
         "These digits were planted: in the English text they pick out three place names."),
        ("COINCIDENCE", COINCIDENCE, "demo_report_coincidence.md",
         "These digits were NOT planted. Some conventions still find place names - that always happens."),
    ]
    for title, digits, name, blurb in runs:
        print("")
        print("=" * 72)
        print("DEMO %s: digits %s" % (title, digits))
        print(blurb)
        print("=" * 72)
        ns = argparse.Namespace(digits=digits, text=["en=" + en, "fr=" + fr], targets=places, wordlist=None,
                                score="targets", marker=[], units=None, tokenizers=None, bases=None,
                                starts=None, groupings=None, draws=10000, seed=1856, threshold=0.01)
        do_run(Inputs(ns), os.path.join(outdir, name))
    print("")
    print("What to notice:")
    print(" * Both runs find conventions that 'hit'. Hits alone prove nothing.")
    print(" * The planted string is significant in English only (it was planted there);")
    print("   French uses different words, so the same convention does not win there.")
    print(" * The coincidence hits about as often as random strings do, so its p-value is large.")
    print("Open the two demo_report_*.md files in %s/ to read the full reports." % outdir)
