"""The engine: extract with every convention, score, and build the two nulls.

Null A: random digit strings with the same shape, on the real text.
Null B: the real digits, on copies of the text whose paragraphs (all except
        the title) are put in a random order.

For each draw we keep the BEST score over all conventions, exactly as for the
real digits, so the p-value already pays for having tried every convention.
"""
from __future__ import annotations

import math
from typing import Optional, Sequence

import numpy as np

from .conventions import Config, TextViews, View, build_conventions
from .digits import DigitString, numbers
from .scoring import LetterScorer, TargetScorer
from .text import Text

MIN_DRAWS = 10000


def gather(view: View, pos: np.ndarray, order: Optional[np.ndarray] = None) -> np.ndarray:
    """Item codes at 0-based stream positions `pos` (rows x K); -1 = no item.

    order=None means the text as written.  Otherwise each row of `order` is a
    paragraph order (order[:, 0] is always 0, the title) and positions are
    counted through the paragraphs in that order, from the view's start.
    """
    if order is None:
        total = len(view.flat) - view.start_flat
        valid = (pos >= 0) & (pos < total)
        idx = np.where(valid, view.start_flat + pos, 0)
        return np.where(valid, view.flat[idx] if len(view.flat) else -1, -1)

    N, P = order.shape
    if pos.shape[0] == 1 and N > 1:
        pos = np.broadcast_to(pos, (N, pos.shape[1]))
    lens = view.para_len[order]
    offs = np.zeros_like(lens)
    if view.start[0] == "slot":
        lens[:, :view.start[1]] = 0
    else:
        _, m, o = view.start
        slot_m = np.argmax(order == m, axis=1)
        cols = np.arange(P)[None, :]
        lens[cols < slot_m[:, None]] = 0
        rows = np.arange(N)
        lens[rows, slot_m] = view.para_len[m] - o
        offs[rows, slot_m] = o
    cum = np.cumsum(lens, axis=1)
    total = cum[:, -1:]
    valid = (pos >= 0) & (pos < total)
    big = int(total.max()) + 1
    rowoff = (np.arange(N, dtype=np.int64) * big)[:, None]
    q = np.clip(pos, 0, total) + rowoff
    slot = np.searchsorted((cum + rowoff).ravel(), q.ravel(), side="right").reshape(q.shape)
    slot = np.clip(slot - np.arange(N)[:, None] * P, 0, P - 1)
    before = np.take_along_axis(cum - lens, slot, axis=1)
    para = np.take_along_axis(order, slot, axis=1)
    off = np.take_along_axis(offs, slot, axis=1)
    idx = view.para_base[para] + off + (np.clip(pos, 0, total) - before)
    idx = np.where(valid, idx, 0)
    return np.where(valid, view.flat[idx] if len(view.flat) else -1, -1)


def random_orders(rng: np.random.Generator, n: int, P: int) -> np.ndarray:
    body = np.argsort(rng.random((n, P - 1)), axis=1) + 1
    return np.hstack([np.zeros((n, 1), dtype=np.int64), body.astype(np.int64)])


class TailModel:
    """How unusual is a score *for one particular convention*?

    Conventions are not on the same scale: one that extracts 28 letters
    scores higher by chance than one that extracts 4.  So the raw scores are
    first turned into rarities, learned from a separate set of reference
    draws ("what is normal for this convention").

    rarity(x) = share of reference draws scoring >= x for that convention.
    Beyond the last value seen at least 10 times, the tail is continued
    smoothly (an exponential fitted between the values seen >= 100 and >= 10
    times), so extreme scores keep getting rarer instead of all tying.

    The model is fixed before the real digits are compared with the second,
    independent set of null draws, so the p-value is exact whatever this
    model gets wrong; a poor model can only cost power, never create a
    false positive.
    """

    def __init__(self, R: np.ndarray):
        self.NR, self.M = R.shape
        top = int(R.max()) if R.size else 0
        cnt = np.zeros((self.M, top + 2), dtype=np.int64)
        for j in range(self.M):
            cnt[j, :top + 1] = np.bincount(R[:, j], minlength=top + 1)[::-1].cumsum()[::-1]
        self.cnt = cnt
        idx = np.arange(top + 2)[None, :]
        vb = np.where(cnt >= 10, idx, 0).max(axis=1)
        va = np.where(cnt >= 100, idx, 0).max(axis=1)
        lam = np.full(self.M, np.nan)
        ok = vb > va
        rows = np.arange(self.M)
        lam[ok] = (np.log((cnt[rows, va] + 1.0) / (cnt[rows, vb] + 1.0))[ok] / (vb - va)[ok])
        fallback = float(np.median(lam[ok])) if ok.any() else math.log(10.0)
        self.lam = np.where(ok, lam, fallback)
        self.vb = vb
        self.log_norm = math.log(self.NR + 1.0)

    def log_rarity(self, S: np.ndarray) -> np.ndarray:
        x = np.minimum(S, self.vb[None, :])
        c = self.cnt[np.arange(self.M)[None, :], x]
        return np.log(c + 1.0) - self.log_norm - self.lam[None, :] * np.maximum(0, S - self.vb[None, :])

    def statistic(self, S: np.ndarray) -> np.ndarray:
        """Log-rarity of the most unusual convention, per row (lower = rarer)."""
        return self.log_rarity(S).min(axis=1)


class NullTest:
    """Reference draws -> TailModel; independent test draws -> null
    distribution of the statistic.  p = (1 + #null <= observed) / (1 + N)."""

    def __init__(self, ref: np.ndarray, test: np.ndarray):
        self.tail = TailModel(ref)
        self.null_stat = self.tail.statistic(test)
        self.N = len(self.null_stat)

    def p(self, S_obs: np.ndarray, u: Optional[float] = None) -> float:
        f = float(self.tail.statistic(S_obs[None, :])[0])
        if u is None:
            return (1.0 + float(np.sum(self.null_stat <= f))) / (1.0 + self.N)
        less = float(np.sum(self.null_stat < f))
        eq = float(np.sum(self.null_stat == f))
        return (less + u * (eq + 1.0)) / (1.0 + self.N)


class Analysis:
    """Everything needed to test one digit string against one text."""

    def __init__(self, text: Text, ds: DigitString, cfg: Config,
                 targets: Optional[Sequence[str]] = None, wordlist: Optional[Sequence[str]] = None):
        self.text = text
        self.ds = ds
        self.cfg = cfg
        self.tv = TextViews(text, cfg)
        if not self.tv.views:
            raise ValueError("no conventions left for %s (check --units/--starts)" % text.label)
        self.convs, self.groups = build_conventions(self.tv, ds, cfg)
        if cfg.mode == "targets":
            self.scorer = TargetScorer(targets or [], self.tv.vocab_list())
        else:
            self.scorer = LetterScorer(wordlist or [])
        self.col = {}
        for i, c in enumerate(self.convs):
            gi = next(k for k, ga in enumerate(self.groups) if ga[0] == c.grouping)
            self.col[(c.view_index, gi, c.base)] = i
        self.n_paragraphs = len(text.paragraphs)

    @property
    def M(self) -> int:
        return len(self.convs)

    def positions(self, dmat: np.ndarray, gi: int, base: int) -> np.ndarray:
        return numbers(self.groups[gi][0], dmat, self.ds.lengths) - base

    def evaluate(self, dmat: np.ndarray, order: Optional[np.ndarray] = None):
        """Scores (rows x conventions) and hit flags for a batch."""
        N = max(dmat.shape[0], 0 if order is None else order.shape[0])
        scores = np.zeros((N, self.M), dtype=np.int32)
        hits = np.zeros((N, self.M), dtype=bool)
        for gi in range(len(self.groups)):
            for b in self.cfg.bases:
                pos = self.positions(dmat, gi, b)
                for vi, v in enumerate(self.tv.views):
                    codes = gather(v, pos, order)
                    s, h = self.scorer.score(v.kind, codes)
                    j = self.col[(vi, gi, b)]
                    scores[:, j] = s
                    hits[:, j] = h
        return scores, hits

    def observed(self):
        s, h = self.evaluate(self.ds.matrix())
        return s[0], h[0]

    def null(self, which: str, draws: int, seed: int, stream: int = 0, chunk: int = 2000, progress=None):
        """Scores of every convention (draws x M) and hit counts per draw.
        stream 0 = reference draws, stream 1 = test draws (independent)."""
        rng = np.random.default_rng([seed, 1 if which == "A" else 2, stream])
        S = np.zeros((draws, self.M), dtype=np.int32)
        nhit = np.zeros(draws, dtype=np.int32)
        done = 0
        while done < draws:
            n = min(chunk, draws - done)
            if which == "A":
                s, h = self.evaluate(self.ds.random_matrix(rng, n))
            elif self.n_paragraphs < 3:
                s, h = self.evaluate(self.ds.matrix())
                s, h = np.repeat(s, n, axis=0), np.repeat(h, n, axis=0)
            else:
                s, h = self.evaluate(self.ds.matrix(), random_orders(rng, n, self.n_paragraphs))
            S[done:done + n] = s
            nhit[done:done + n] = h.sum(axis=1)
            done += n
            if progress:
                progress(which, stream, done, draws)
        return S, nhit

    def extract(self, ci: int) -> dict:
        """Human-readable extract of convention ci for the real digits."""
        c = self.convs[ci]
        v = self.tv.views[c.view_index]
        gi = next(k for k, ga in enumerate(self.groups) if ga[0] == c.grouping)
        pos = self.positions(self.ds.matrix(), gi, c.base)[0]
        total = len(v.flat) - v.start_flat
        items, letters = [], []
        for p in pos:
            if 0 <= p < total:
                d = v.disp[v.start_flat + int(p)]
                code = int(v.flat[v.start_flat + int(p)])
                items.append(d if d else "∅")
                letters.append(chr(97 + code).upper() if (v.kind == "letter" and code >= 0) else "·")
            else:
                items.append("·")
                letters.append("·")
        return {"numbers": [int(x) for x in self.positions(self.ds.matrix(), gi, 0)[0]],
                "items": items, "letters": "".join(letters) if v.kind == "letter" else None}


def analyse(text: Text, ds: DigitString, cfg: Config, draws: int, seed: int,
            targets=None, wordlist=None, progress=None, chunk: int = 2000, return_raw: bool = False):
    """Full analysis of one text.  Returns a plain dict for the report."""
    if draws < MIN_DRAWS:
        raise ValueError("at least %d null draws are required" % MIN_DRAWS)
    an = Analysis(text, ds, cfg, targets=targets, wordlist=wordlist)
    obs_s, obs_h = an.observed()
    tests = {}
    for which in ("A", "B"):
        ref, _ = an.null(which, draws, seed, 0, chunk=chunk, progress=progress)
        test, hits = an.null(which, draws, seed, 1, chunk=chunk, progress=progress)
        tests[which] = (NullTest(ref, test), test, hits)
    nA, SA, hitsA = tests["A"]
    nB, SB, hitsB = tests["B"]
    pA, pB = nA.p(obs_s), nB.p(obs_s)
    rar = nA.tail.log_rarity(obs_s[None, :])[0]
    order = sorted(range(an.M), key=lambda i: (float(rar[i]), -int(obs_s[i]), i))
    top = []
    for i in order[:5]:
        e = an.extract(i)
        top.append({"name": an.convs[i].name, "aliases": an.convs[i].aliases, "score": int(obs_s[i]),
                    "hit": bool(obs_h[i]), "rarity": float(math.exp(rar[i])), **e})
    best = order[0]
    winners = [i for i in range(an.M) if rar[i] == rar[best] and obs_s[i] > 0]
    rawA, rawB = SA.max(axis=1), SB.max(axis=1)
    result = {
        "label": text.label, "path": text.path, "sha256": text.sha256,
        "paragraphs": len(text.paragraphs), "words": text.word_count(),
        "M": an.M, "merged_views": an.tv.n_merged, "n_views": len(an.tv.views),
        "groupings": an.groups, "warnings": list(an.tv.warnings),
        "by_unit": {u: sum(1 for c in an.convs if c.unit == u) for u in cfg.units},
        "conventions": [c.name for c in an.convs],
        "draws": draws,
        "best_name": an.convs[best].name, "best_score": int(obs_s[best]), "best_rarity": float(math.exp(rar[best])),
        "raw_max": int(obs_s.max()),
        "nullA_raw_max_median": float(np.median(rawA)), "nullB_raw_max_median": float(np.median(rawB)),
        "hits": int(obs_h.sum()),
        "nullA_mean_hits": float(hitsA.mean()), "nullA_hits_95": int(np.percentile(hitsA, 95)),
        "pA": pA, "pB": pB, "p": max(pA, pB),
        "shuffle_possible": an.n_paragraphs >= 3,
        "top": top,
        "winners": [an.convs[i].aliases for i in winners],
        "n_winners": len(winners),
    }
    if return_raw:
        return result, {"analysis": an, "nullA": nA, "nullB": nB, "obs": obs_s}
    return result
