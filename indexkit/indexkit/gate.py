"""The self-test gate.  `selftest` writes a stamp file; every other command
checks that the stamp exists, says PASSED, and matches the current code,
Python and numpy versions.  Change any of those and selftest must run again.
"""
from __future__ import annotations

import hashlib
import json
import os
import platform
from typing import Tuple

import numpy as np

PKG_DIR = os.path.dirname(os.path.abspath(__file__))
STAMP = os.path.join(os.path.dirname(PKG_DIR), ".indexkit_selftest.json")


def code_hash() -> str:
    h = hashlib.sha256()
    for name in sorted(os.listdir(PKG_DIR)):
        if name.endswith(".py"):
            h.update(name.encode())
            with open(os.path.join(PKG_DIR, name), "rb") as fh:
                h.update(hashlib.sha256(fh.read()).digest())
    return h.hexdigest()


def environment() -> dict:
    return {"code_hash": code_hash(), "python": ".".join(platform.python_version_tuple()[:2]),
            "numpy": np.__version__}


def write_stamp(passed: bool, details: dict) -> None:
    data = dict(environment(), passed=passed, details=details)
    with open(STAMP, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)


def check() -> Tuple[bool, str]:
    if not os.path.exists(STAMP):
        return False, "the self-test has not been run yet."
    try:
        with open(STAMP, encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError):
        return False, "the self-test record is unreadable."
    if not data.get("passed"):
        return False, "the last self-test FAILED."
    env = environment()
    names = {"code_hash": "indexkit code", "python": "Python version", "numpy": "numpy version"}
    for key, name in names.items():
        if data.get(key) != env[key]:
            return False, "the %s changed since the last self-test." % name
    return True, "ok"
