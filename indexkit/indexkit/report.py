"""Markdown report and terminal summary."""
from __future__ import annotations

import datetime
from typing import List

from .conventions import READ_HELP, START_HELP, UNIT_HELP
from .digits import GROUPING_HELP
from .text import TOKENIZER_HELP

SIGNAL_ONLY = "SIGNAL ONLY: this says nothing about what it means."


def null_sentence(M_list: List[int], draws: int) -> str:
    ms = " / ".join(str(m) for m in M_list)
    return ("The digits carry no information about the text: across all %s conventions, the most unusual "
            "score they produce is no more unusual than the most unusual score produced by random digit "
            "strings of the same shape (null A) or by the real digits on paragraph-shuffled copies of the "
            "text (null B), judged on %d seeded test draws per null after %d separate reference draws "
            "per null." % (ms, draws, draws))


def rarity_text(r: float) -> str:
    if r >= 0.5:
        return "common (half of random strings or more)"
    if r >= 1e-4:
        return "about 1 in %s random strings" % format(int(round(1.0 / r)), ",")
    return "fewer than 1 in 10,000 random strings"


def fmt_p(p: float, draws: int) -> str:
    if p <= 1.0 / (draws + 1) + 1e-12:
        return "%.5f (the smallest possible with %d draws)" % (p, draws)
    return "%.4f" % p


def verdict(r: dict, per_text_threshold: float) -> str:
    if r["p"] <= per_text_threshold:
        return "SIGNIFICANT (p = %.4f ≤ %.4g)" % (r["p"], per_text_threshold)
    return "NOT significant (p = %.4f > %.4g) — consistent with coincidence" % (r["p"], per_text_threshold)


def same_winner(results: List[dict]):
    """Do the texts share at least one top-scoring convention?"""
    if len(results) < 2:
        return None, []
    sets = []
    for r in results:
        names = set()
        for aliases in r["winners"]:
            names.update(aliases)
        sets.append(names)
    common = set.intersection(*sets) if all(sets) else set()
    return bool(common), sorted(common)


def _extract_line(t: dict) -> str:
    items = " ".join(t["items"])
    if t["letters"] is not None:
        return "`%s`  (from: %s)" % (t["letters"], items)
    return "`%s`" % items


def markdown(info: dict, results: List[dict]) -> str:
    draws, thr = info["draws"], info["threshold"]
    k = len(results)
    per_text = thr / k
    L = []
    L.append("# indexkit report")
    L.append("")
    L.append("_%s · indexkit %s · code %s_" % (info.get("when") or datetime.date.today().isoformat(),
                                                      info["version"], info["code_hash"][:12]))
    L.append("")
    L.append("## Null hypothesis (stated before any result)")
    L.append("")
    L.append(null_sentence([r["M"] for r in results], draws))
    L.append("")
    L.append("Pass rule: a text is called significant only if p ≤ %.4g, where p is the LARGER of the "
             "two null p-values and %.4g is the threshold %.4g split over %d text(s)." % (per_text, per_text, thr, k))
    L.append("")
    L.append("## Inputs")
    L.append("")
    L.append("- Digit string: `%s` (shape %s, %d digits)" % (info["digits"], info["shape"], info["n_digits"]))
    for r in results:
        L.append("- Text **%s**: `%s` — SHA-256 `%s` (%d paragraphs incl. title, ~%d words)"
                 % (r["label"], r["path"], r["sha256"], r["paragraphs"], r["words"]))
    if info["score"] == "targets":
        L.append("- Score: **targets** — %d target words%s: %s" % (
            len(info["targets"]), (" from `%s` (SHA-256 `%s`)" % (info["targets_path"], info["targets_sha256"])
                                   if info.get("targets_path") else ""),
            ", ".join(info["targets"])))
    else:
        L.append("- Score: **letters** — wordlist: %s" % info["wordlist_desc"])
    if info["markers"]:
        L.append("- Marker lines: %s" % ", ".join("`%s`" % m for m in info["markers"]))
    L.append("- Null draws: %d for null A and %d for null B, seed %d" % (draws, draws, info["seed"]))
    L.append("- Pre-registration: %s" % (info.get("prereg") or "none (results are exploratory)"))
    if info.get("restricted"):
        L.append("- **Restricted search space** (%s). This is only honest if the restriction was chosen "
                 "before looking at any result." % info["restricted"])
    L.append("")
    L.append("## Search space")
    L.append("")
    for r in results:
        bu = ", ".join("%s %d" % (u, n) for u, n in r["by_unit"].items())
        L.append("- **%s: %d conventions** tried (%s). %d exact duplicate readings were merged."
                 % (r["label"], r["M"], bu, r["merged_views"]))
        if len(r["groupings"]) < len(info["groupings"]):
            same = ["=".join(g) for g in r["groupings"] if len(g) > 1]
            L.append("  - digit groupings that are identical for this shape were merged: %s" % ", ".join(same))
        for w in r["warnings"]:
            L.append("  - warning: %s" % w)
    L.append("")
    L.append("Dimensions searched: units %s; tokenizers %s (words only); reads %s; starts %s; "
             "counting %s-based; digit groupings %s."
             % (", ".join(info["units"]), ", ".join(info["tokenizers"]), "item/initial/char",
                ", ".join(info["starts"] + ["marker:" + m for m in info["markers"]]),
                "/".join(str(b) for b in info["bases"]), ", ".join(info["groupings"])))
    L.append("")
    for r in results:
        L.append("## Result — %s" % r["label"])
        L.append("")
        L.append("- **%d of %d conventions hit.** Random digit strings of this shape hit on average %.1f of %d "
                 "(95%% of them hit ≤ %d)." % (r["hits"], r["M"], r["nullA_mean_hits"], r["M"], r["nullA_hits_95"]))
        L.append("- Most unusual convention: `%s`, score %d. For that one convention alone, "
                 "this score is reached by %s. **Uncorrected \u2014 do not quote this; the p-values below "
                 "are the honest ones.**" % (r["best_name"], r["best_score"], rarity_text(r["best_rarity"])))
        L.append("- Highest raw score: %d (median highest raw score: random strings %.0f, shuffled text %.0f)"
                 % (r["raw_max"], r["nullA_raw_max_median"], r["nullB_raw_max_median"]))
        L.append("- p, null A (random digits): %s" % fmt_p(r["pA"], draws))
        L.append("- p, null B (shuffled paragraphs): %s%s" % (fmt_p(r["pB"], draws), "" if r["shuffle_possible"]
                 else " — the text has fewer than 2 body paragraphs, so it cannot be shuffled; p is set to 1"))
        L.append("- **p (the larger, already corrected for all %d conventions): %.4f**" % (r["M"], r["p"]))
        L.append("- Verdict: **%s**" % verdict(r, per_text))
        if r["n_winners"] > 1:
            L.append("- %d conventions are tied as most unusual, so the \"winner\" below is not unique." % r["n_winners"])
        L.append("")
        L.append("Top 5 conventions for the real digits, most unusual first (rarity = how often random strings "
                 "do this well with that one convention; it ignores the search, so it always looks impressive):")
        L.append("")
        L.append("| # | convention | score | uncorrected rarity | extract |")
        L.append("|---|---|---|---|---|")
        for i, t in enumerate(r["top"], 1):
            name = t["name"].replace("|", "·")
            if len(t["aliases"]) > 1:
                name += " (+%d identical reading%s)" % (len(t["aliases"]) - 1, "s" if len(t["aliases"]) > 2 else "")
            L.append("| %d | %s | %d | %s | %s |" % (i, name, t["score"], rarity_text(t["rarity"]),
                                                      _extract_line(t).replace("|", "\\|")))
        L.append("")
    L.append("## English / French check")
    L.append("")
    if len(results) < 2:
        L.append("Only one text was given, so there is no cross-language check.")
    else:
        for r in results:
            L.append("- %s: %s" % (r["label"], verdict(r, per_text)))
        same, common = same_winner(results)
        if same:
            L.append("- The same convention reaches the top score in every text: %s" %
                     ", ".join("`%s`" % c for c in common[:3]))
        else:
            L.append("- The top-scoring convention is **not** the same across texts.")
        L.append("- Each text is scored and tested on its own; the scores are never combined.")
    L.append("")
    L.append("**%s**" % SIGNAL_ONLY)
    L.append("")
    return "\n".join(L)


def terminal_summary(info: dict, results: List[dict]) -> str:
    k = len(results)
    per_text = info["threshold"] / k
    out = ["", "NULL: " + null_sentence([r["M"] for r in results], info["draws"]), ""]
    for r in results:
        out.append("[%s] search space: %d conventions" % (r["label"], r["M"]))
        out.append("[%s] %d of %d conventions hit (random strings: %.1f on average)"
                   % (r["label"], r["hits"], r["M"], r["nullA_mean_hits"]))
        out.append("[%s] pA=%.4f  pB=%.4f  p=%.4f  -> %s"
                   % (r["label"], r["pA"], r["pB"], r["p"], verdict(r, per_text)))
        if r["top"]:
            t = r["top"][0]
            out.append("[%s] most unusual: %s  =>  %s  (score %d)" % (r["label"], t["name"], _extract_line(t), t["score"]))
        out.append("")
    if k > 1:
        same, _ = same_winner(results)
        out.append("Same convention wins in all texts: %s" % ("yes" if same else "no"))
    out.append(SIGNAL_ONLY)
    return "\n".join(out)


def conventions_help() -> str:
    L = ["Units:"] + ["  %-10s %s" % kv for kv in UNIT_HELP.items()]
    L += ["Tokenizers (word unit only):"] + ["  %-10s %s" % kv for kv in TOKENIZER_HELP.items()]
    L += ["Reads:"] + ["  %-10s %s" % kv for kv in READ_HELP.items()]
    L += ["Starts:"] + ["  %-10s %s" % kv for kv in START_HELP.items()]
    L += ["Counting: 0-based (first item is 0) or 1-based (first item is 1)"]
    L += ["Digit groupings:"] + ["  %-10s %s" % kv for kv in GROUPING_HELP.items()]
    return "\n".join(L)
