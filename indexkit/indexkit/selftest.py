"""Instrument validation.

1. Tokenizers behave as documented on tricky French/English snippets.
2. The fast path and the paragraph-shuffle path agree when nothing is shuffled.
3. PLANTED (letters): a message is hidden as word initials in the made-up
   English article.  The tool must find it, under the right convention, with
   a small p-value.
4. PLANTED (targets): place names are hidden in the made-up French article
   with cumulative offsets.  Same requirement.
5. CALIBRATION: hundreds of fresh random digit strings (null A) and fresh
   paragraph shuffles (null B) are scored exactly like real input.  Their
   p-values must look uniform (Kolmogorov-Smirnov test) and the share with
   p <= 0.05 / 0.01 must not exceed 5% / 1% by more than chance allows.
"""
from __future__ import annotations

import math

import numpy as np

from . import gate
from .conventions import Config
from .demo_article import EN_PARAGRAPHS, FR_PARAGRAPHS, TARGETS, as_file_text
from .digits import DigitString
from .engine import MIN_DRAWS, analyse, gather, random_orders
from .stats import ks_uniform
from .text import Text, fold, tokenize, tokens
from .wordlists import builtin_wordlist

N_CALIB = 400
SEED = 20240611


class Check:
    def __init__(self):
        self.rows = []

    def __call__(self, name: str, ok: bool, detail: str = "") -> bool:
        self.rows.append((name, bool(ok), detail))
        print("  [%s] %s%s" % ("PASS" if ok else "FAIL", name, ("  -- " + detail) if detail else ""))
        return ok

    @property
    def all_ok(self) -> bool:
        return all(ok for _, ok, _ in self.rows)


def _tokenizer_checks(check: Check) -> None:
    s = "« Bonjour » : l’Or de Val-d'Or – fin."
    check("tokenizer ws keeps standalone punctuation",
          tokens(s, "ws") == ["«", "Bonjour", "»", ":", "l’Or", "de", "Val-d'Or", "–", "fin."])
    check("tokenizer ws-drop drops it", tokens(s, "ws-drop") == ["Bonjour", "l’Or", "de", "Val-d'Or", "fin."])
    check("tokenizer strip keeps inner apostrophes/hyphens",
          tokens(s, "strip") == ["Bonjour", "l’Or", "de", "Val-d'Or", "fin"])
    check("tokenizer split splits elisions and hyphens",
          tokens(s, "split") == ["Bonjour", "l", "Or", "de", "Val", "d", "Or", "fin"])
    check("folding: accents, both apostrophes, case", fold("VAL-D’OR") == fold("Val-d'Or") == "valdor"
          and fold("Hérons") == "herons" and fold("cœur") == "coeur")
    decomposed = "Hérons"
    check("NFC: decomposed é is one letter", tokens(decomposed, "strip") == ["Hérons"])


def _plant_letters(text: Text, message: str, rng) -> str:
    """Hide `message` as initials of words: tokenizer ws, counted 1-based
    from the first paragraph after the title, numbers as given."""
    words = [w for p in text.paragraphs[1:] for w, _, _ in tokenize(p, "ws")]
    picks = []
    for ch in message:
        cands = [i + 1 for i, w in enumerate(words) if fold(w)[:1] == ch and i + 1 >= 10]
        picks.append(int(rng.choice(cands)))
    return " ".join(str(n) for n in picks)


def _plant_targets(text: Text) -> str:
    """Hide place names: tokenizer split, 0-based from the title, numbers are
    steps between successive positions (cumulative)."""
    words = [fold(w) for p in text.paragraphs for w, _, _ in tokenize(p, "split")]
    want = ["cuivre", "cuivre", "herons", "sureau"]
    pos, last = [], -1
    for w in want:
        last = next(i for i in range(last + 1, len(words)) if words[i] == w)
        pos.append(last)
    steps = [pos[0]] + [b - a for a, b in zip(pos, pos[1:])]
    return "-".join(str(s) for s in steps)


def _calibrate(check: Check, name: str, raw: dict, ds: DigitString, seed: int) -> None:
    an = raw["analysis"]
    rng = np.random.default_rng([seed, 99])
    u = np.random.default_rng([seed, 98]).random(2 * N_CALIB)
    for which, null in (("A", raw["nullA"]), ("B", raw["nullB"])):
        if which == "A":
            s, _ = an.evaluate(ds.random_matrix(rng, N_CALIB))
        else:
            s, _ = an.evaluate(ds.matrix(), random_orders(rng, N_CALIB, an.n_paragraphs))
        k = 0 if which == "A" else N_CALIB
        prand = [null.p(row, float(u[k + i])) for i, row in enumerate(s)]
        pcons = [null.p(row) for row in s]
        d, pks = ks_uniform(prand)
        hist = np.histogram(prand, bins=10, range=(0, 1))[0]
        check("%s null %s: p-values of %d random inputs look uniform" % (name, which, N_CALIB), pks >= 0.01,
              "KS D=%.3f, p=%.3f; deciles %s" % (d, pks, " ".join(str(x) for x in hist)))
        for a in (0.05, 0.01):
            n_sig = sum(1 for p in pcons if p <= a)
            limit = N_CALIB * a + 3 * math.sqrt(N_CALIB * a * (1 - a))
            check("%s null %s: random inputs significant at %.2f" % (name, which, a), n_sig <= limit,
                  "%d of %d (allowed up to %.0f)" % (n_sig, N_CALIB, limit))


def run_selftest() -> bool:
    print("indexkit self-test (takes about a minute)")
    check = Check()
    _tokenizer_checks(check)

    en = Text.from_string("en", as_file_text(EN_PARAGRAPHS))
    fr = Text.from_string("fr", as_file_text(FR_PARAGRAPHS))

    # 2. consistency of the two extraction paths
    from .engine import Analysis
    ds_probe = DigitString("12 345 6 78")
    an = Analysis(fr, ds_probe, Config("targets", markers=["Son magasin"]), targets=TARGETS)
    ident = np.tile(np.arange(an.n_paragraphs), (7, 1))
    d = ds_probe.random_matrix(np.random.default_rng(1), 7)
    same = all(np.array_equal(gather(v, an.positions(d, g, b)), gather(v, an.positions(d, g, b), ident))
               for v in an.tv.views for g in range(len(an.groups)) for b in (0, 1))
    check("shuffle path == plain path when nothing is shuffled", same)

    # 3. planted letters
    rng = np.random.default_rng(SEED)
    message = "goldisnorth"
    digits = _plant_letters(en, message, rng)
    ds = DigitString(digits)
    cfg = Config("letters")
    print("  planting %r as word initials in the English demo text: %s" % (message.upper(), digits))
    res, raw = analyse(en, ds, cfg, MIN_DRAWS, SEED, wordlist=builtin_wordlist("en"), return_raw=True)
    planted = "word | ws | initial | from=body | 1-based | digits=given"
    found = any(planted in a for a in res["winners"])
    top = res["top"][0]
    check("planted letters: found by the planted convention", found,
          "top: %s -> %s" % (top["name"], top["letters"]))
    check("planted letters: p <= 0.01", res["p"] <= 0.01, "pA=%.5f pB=%.5f" % (res["pA"], res["pB"]))
    _calibrate(check, "letters", raw, ds, SEED)

    # 4. planted targets
    digits = _plant_targets(fr)
    ds = DigitString(digits)
    cfg = Config("targets")
    print("  planting place names in the French demo text (cumulative offsets): %s" % digits)
    res, raw = analyse(fr, ds, cfg, MIN_DRAWS, SEED, targets=TARGETS, return_raw=True)
    planted = "word | split | item | from=title | 0-based | digits=cumulative"
    found = any(planted in a for a in res["winners"])
    top = res["top"][0]
    check("planted targets: found by the planted convention", found,
          "top: %s -> %s (score %d)" % (top["name"], " ".join(top["items"]), top["score"]))
    check("planted targets: p <= 0.01", res["p"] <= 0.01, "pA=%.5f pB=%.5f" % (res["pA"], res["pB"]))
    _calibrate(check, "targets", raw, ds, SEED + 1)

    ok = check.all_ok
    gate.write_stamp(ok, {"checks": [{"name": n, "ok": o, "detail": d} for n, o, d in check.rows]})
    n_fail = sum(1 for _, o, _ in check.rows if not o)
    print("")
    if ok:
        print("SELFTEST PASSED (%d checks). The other commands are now unlocked." % len(check.rows))
    else:
        print("SELFTEST FAILED (%d of %d checks failed). The other commands stay locked." % (n_fail, len(check.rows)))
    return ok
