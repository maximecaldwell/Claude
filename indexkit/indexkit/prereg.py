"""Pre-registration files.

A pre-registration is a JSON file listing everything that decides the
outcome: digits, texts (with SHA-256 hashes), score, targets, wordlist,
every convention, the null, the number of draws, the seed and the pass
threshold.  Its own SHA-256 is printed and saved next to it
(FILE.sha256).  `run --prereg FILE` re-checks all of it and refuses to run
if anything differs or if you try to override any of it.
"""
from __future__ import annotations

import hashlib
import json
import os
from typing import Tuple

PREREG_VERSION = 1


def canonical_bytes(spec: dict) -> bytes:
    return (json.dumps(spec, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


def sidecar(path: str) -> str:
    return path + ".sha256"


def write(path: str, spec: dict) -> Tuple[str, bool]:
    """Write the file and its .sha256.  Never overwrites a different
    pre-registration.  Returns (hash, created_new)."""
    data = canonical_bytes(spec)
    digest = hashlib.sha256(data).hexdigest()
    if os.path.exists(path):
        with open(path, "rb") as fh:
            old = fh.read()
        if old == data:
            return digest, False
        raise SystemExit("REFUSED: %s already exists with different content. A pre-registration is never "
                         "overwritten. Pick a new file name (for example add _v2)." % path)
    with open(path, "wb") as fh:
        fh.write(data)
    with open(sidecar(path), "w", encoding="utf-8") as fh:
        fh.write("%s  %s\n" % (digest, os.path.basename(path)))
    return digest, True


def load(path: str) -> Tuple[dict, str]:
    if not os.path.exists(path):
        raise SystemExit("REFUSED: pre-registration file %s not found." % path)
    with open(path, "rb") as fh:
        data = fh.read()
    digest = hashlib.sha256(data).hexdigest()
    sc = sidecar(path)
    if os.path.exists(sc):
        with open(sc, encoding="utf-8") as fh:
            recorded = fh.read().split()[0] if fh else ""
        if recorded != digest:
            raise SystemExit("REFUSED: %s has been edited since it was registered (hash %s, recorded %s)."
                             % (path, digest[:16], recorded[:16]))
    else:
        raise SystemExit("REFUSED: %s has no %s next to it, so edits cannot be detected." % (path, sc))
    try:
        spec = json.loads(data.decode("utf-8"))
    except ValueError:
        raise SystemExit("REFUSED: %s is not a valid pre-registration file." % path)
    if spec.get("indexkit_prereg") != PREREG_VERSION:
        raise SystemExit("REFUSED: %s is not an indexkit pre-registration (version %r)."
                         % (path, spec.get("indexkit_prereg")))
    return spec, digest
