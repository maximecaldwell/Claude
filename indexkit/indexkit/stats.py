"""Kolmogorov-Smirnov test against the uniform distribution (no scipy)."""
from __future__ import annotations

import math
from typing import Sequence, Tuple


def ks_uniform(values: Sequence[float]) -> Tuple[float, float]:
    """Return (D, p-value) for H0: values ~ Uniform(0, 1)."""
    x = sorted(values)
    n = len(x)
    d = 0.0
    for i, v in enumerate(x):
        d = max(d, (i + 1) / n - v, v - i / n)
    en = math.sqrt(n)
    lam = (en + 0.12 + 0.11 / en) * d
    if lam < 1e-3:
        return d, 1.0
    p = 0.0
    for k in range(1, 101):
        term = 2.0 * (-1) ** (k - 1) * math.exp(-2.0 * k * k * lam * lam)
        p += term
        if abs(term) < 1e-12:
            break
    return d, min(1.0, max(0.0, p))
