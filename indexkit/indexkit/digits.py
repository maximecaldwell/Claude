"""Digit strings: parsing, random strings of the same shape, and the digit
groupings (how a digit string is turned into a list of numbers).
"""
from __future__ import annotations

import re
from typing import List

import numpy as np

GROUPINGS = ("given", "single", "pairs", "cumulative", "reversed")

GROUPING_HELP = {
    "given": "numbers exactly as grouped in the string (no separators = one big number)",
    "single": "every digit on its own",
    "pairs": "digits taken two at a time, ignoring the separators (an odd last digit stays single)",
    "cumulative": "the given numbers are steps: each position = previous position + next number",
    "reversed": "the whole string read backwards, then grouped as given",
}

MAX_DIGITS = 60
MAX_GROUP = 15


class DigitString:
    """A digit string such as "810-419-227" or "6 2 76 37 3 25 69 4 20".

    The *shape* is the list of group lengths plus the separators; random
    strings for the null keep the shape and draw every digit uniformly.
    """

    def __init__(self, raw: str):
        self.raw = raw.strip()
        self.groups = re.findall(r"[0-9]+", self.raw)
        self.seps = re.split(r"[0-9]+", self.raw)
        if not self.groups:
            raise ValueError("no digits found in %r" % raw)
        self.lengths = [len(g) for g in self.groups]
        if sum(self.lengths) > MAX_DIGITS:
            raise ValueError("at most %d digits are supported" % MAX_DIGITS)
        if max(self.lengths) > MAX_GROUP:
            raise ValueError("a single group may have at most %d digits" % MAX_GROUP)
        self.n_digits = sum(self.lengths)

    def shape(self) -> str:
        return "-".join(str(n) for n in self.lengths)

    def matrix(self) -> np.ndarray:
        return np.array([[int(c) for c in "".join(self.groups)]], dtype=np.int64)

    def random_matrix(self, rng: np.random.Generator, n: int) -> np.ndarray:
        return rng.integers(0, 10, size=(n, self.n_digits), dtype=np.int64)

    def format_row(self, row) -> str:
        """Rebuild a digit row with this string's separators."""
        digits = "".join(str(int(d)) for d in row)
        out, pos = [self.seps[0]], 0
        for n, sep in zip(self.lengths, self.seps[1:]):
            out.append(digits[pos:pos + n])
            out.append(sep)
            pos += n
        return "".join(out)


def _given(d: np.ndarray, lengths: List[int]) -> np.ndarray:
    cols, pos = [], 0
    for n in lengths:
        w = 10 ** np.arange(n - 1, -1, -1, dtype=np.int64)
        cols.append(d[:, pos:pos + n] @ w)
        pos += n
    return np.stack(cols, axis=1)


def numbers(grouping: str, d: np.ndarray, lengths: List[int]) -> np.ndarray:
    """Turn a digit matrix (rows = digit strings) into a number matrix."""
    if grouping == "given":
        return _given(d, lengths)
    if grouping == "single":
        return d.copy()
    if grouping == "pairs":
        n = d.shape[1]
        return _given(d, [2] * (n // 2) + [1] * (n % 2))
    if grouping == "cumulative":
        return np.cumsum(_given(d, lengths), axis=1)
    if grouping == "reversed":
        return _given(d[:, ::-1], lengths[::-1])
    raise ValueError("unknown grouping %r (choose from %s)" % (grouping, ", ".join(GROUPINGS)))


def distinct_groupings(ds: DigitString, groupings, seed: int = 0) -> List[List[str]]:
    """Group the groupings that are the *same function* for this shape (for
    example 'single' == 'given' when every group has one digit).  Tested on
    the real digits plus 50 random strings of the same shape, so the result
    depends only on the shape, never on luck in the real digits.
    Returns a list of alias lists; the first name in each list is used.
    """
    rng = np.random.default_rng(seed)
    probe = np.vstack([ds.matrix(), ds.random_matrix(rng, 50)])
    kept: List[List[str]] = []
    outs = []
    for g in groupings:
        out = numbers(g, probe, ds.lengths)
        for i, o in enumerate(outs):
            if o.shape == out.shape and np.array_equal(o, out):
                kept[i].append(g)
                break
        else:
            kept.append([g])
            outs.append(out)
    return kept
