"""Scores.  Every scorer works on a whole batch of extracts at once
(rows = draws, columns = positions; -1 = nothing there).  The real digits go
through exactly the same code as the random draws, as a batch of one.

targets  -- how many DIFFERENT target words appear in the extract (picking
            the same name twice counts once).
            'item' extracts: a target must match one extracted word, or a run
            of consecutive extracted words that together spell it
            (Val + d + Or = Val-d'Or).  'letter' extracts: a target must
            appear as consecutive letters (gaps break it).
            A convention "hits" if it scores at least 1.

letters  -- for letter extracts only: the best way to read the extract as
            dictionary words.  Each word found scores its length squared
            (a 2-letter word = 4, a 4-letter word = 16), words cannot
            overlap, letters may be left over.  1- and 2-letter words count,
            so short messages are not missed.  A convention "hits" if it has
            at least 3 letters and 80% or more of them are covered by words.
"""
from __future__ import annotations

from typing import Dict, List, Sequence, Tuple

import numpy as np

from .text import fold

MAX_WORD = 13  # 27**13 still fits the 64-bit word codes used below


def read_word_file(path: str) -> List[str]:
    """One entry per line; blank lines and lines starting with # ignored."""
    out = []
    with open(path, "r", encoding="utf-8-sig") as fh:
        for line in fh:
            line = line.strip()
            if line and not line.startswith("#"):
                out.append(line)
    return out


def unique_keys(words: Sequence[str]) -> List[str]:
    seen, out = set(), []
    for w in words:
        k = fold(w)
        if k and k not in seen:
            seen.add(k)
            out.append(k)
    return out


class TargetScorer:
    mode = "targets"

    def __init__(self, targets: Sequence[str], vocab: List[str]):
        self.keys = unique_keys(targets)
        if not self.keys:
            raise ValueError("the target list is empty")
        V = len(vocab)
        # one-word matches: vocab id -> target number (-1 = not a target)
        tnum = {k: i for i, k in enumerate(self.keys)}
        self.single = np.array([tnum.get(k, -1) if k else -1 for k in vocab], dtype=np.int64)
        # multi-word matches: for each target, a table ok[offset, word] that
        # says whether `word` continues the target at `offset`.
        vlen = np.array([len(k) for k in vocab], dtype=np.int64)
        self.vlen = vlen
        self.multi = []
        for t in self.keys:
            ok = np.zeros((len(t), V), dtype=bool)
            for vid, k in enumerate(vocab):
                if not k or k not in t:
                    continue
                for off in range(len(t)):
                    if t.startswith(k, off) and (off > 0 or len(k) < len(t)):
                        ok[off, vid] = True
            if ok[0].any():
                self.multi.append((self.keys.index(t), len(t), ok))
        self.letter_targets = [np.array([ord(c) - 97 for c in t], dtype=np.int64) for t in self.keys]

    def score(self, kind: str, codes: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        N, K = codes.shape
        found = np.zeros((N, len(self.keys)), dtype=bool)
        if kind == "item":
            valid = codes >= 0
            c0 = np.where(valid, codes, 0)
            tid = np.where(valid, self.single[c0], -1)
            for ti in np.unique(tid[tid >= 0]):
                found[:, ti] |= (tid == ti).any(axis=1)
            for ti, tlen, ok in self.multi:
                for j in range(K - 1):
                    off = np.zeros(N, dtype=np.int64)
                    alive = np.ones(N, dtype=bool)
                    for k in range(j, K):
                        c = c0[:, k]
                        step = alive & valid[:, k] & ok[np.minimum(off, tlen - 1), c]
                        off = np.where(step, off + self.vlen[c], off)
                        found[:, ti] |= step & (off == tlen) & (k > j)
                        alive = step & (off < tlen)
                        if not alive.any():
                            break
        else:
            for ti, t in enumerate(self.letter_targets):
                m = len(t)
                for j in range(K - m + 1):
                    found[:, ti] |= np.all(codes[:, j:j + m] == t, axis=1)
        s = found.sum(axis=1).astype(np.int32)
        return s, s >= 1


class LetterScorer:
    mode = "letters"

    def __init__(self, words: Sequence[str]):
        keys = [k for k in unique_keys(words) if len(k) <= MAX_WORD]
        if not keys:
            raise ValueError("the wordlist is empty")
        self.n_words = len(keys)
        by_len: Dict[int, List[int]] = {}
        for k in keys:
            code = 0
            for c in k:
                code = code * 27 + (ord(c) - 96)
            by_len.setdefault(len(k), []).append(code)
        self.by_len = {m: np.array(sorted(v), dtype=np.int64) for m, v in by_len.items()}
        self.maxlen = max(self.by_len)

    def best(self, codes: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """(score, letters covered) of the best reading, per row."""
        N, K = codes.shape
        # value = score * 1024 + covered letters: maximising it maximises the
        # score and, among equal scores, the coverage.
        best = np.zeros((N, K + 1), dtype=np.int64)
        for s in range(K):
            np.maximum(best[:, s + 1], best[:, s], out=best[:, s + 1])
            code = np.zeros(N, dtype=np.int64)
            ok = np.ones(N, dtype=bool)
            for m in range(1, min(self.maxlen, K - s) + 1):
                c = codes[:, s + m - 1]
                ok &= c >= 0
                if not ok.any():
                    break
                code = code * 27 + (c + 1)
                arr = self.by_len.get(m)
                if arr is None:
                    continue
                i = np.minimum(np.searchsorted(arr, code), len(arr) - 1)
                isw = ok & (arr[i] == code)
                cand = best[:, s] + m * m * 1024 + m
                best[:, s + m] = np.where(isw, np.maximum(best[:, s + m], cand), best[:, s + m])
        return best[:, K] // 1024, best[:, K] % 1024

    def score(self, kind: str, codes: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        if kind != "letter":
            raise ValueError("letter scoring only applies to letter extracts")
        sc, cov = self.best(codes)
        n = (codes >= 0).sum(axis=1)
        return sc.astype(np.int32), (n >= 3) & (cov * 5 >= n * 4)
