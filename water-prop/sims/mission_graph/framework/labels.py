"""Stable labels for nodes (phase+option+params) and paths through a mission.

A node label looks like `P1.hohmann_chemical.a7f2b1` and identifies one
phase-option-parameter triple. The 6-char suffix is a hex hash over the
canonicalized parameter dictionary — same inputs always produce the same
label, different inputs always (within hash collision probability) produce
different labels.

A path label looks like `P0.falcon.b1c2 -> P1.hohmann.a7f2b1 -> ...` and
identifies a complete mission architecture as a chain of node labels.

Canonicalization handles three sources of accidental hash difference:
  - dictionary key ordering (sort)
  - float precision drift (round to fixed digits)
  - numeric type confusion (340 vs 340.0; coerce to float)

The default precision is 6 significant digits, which is finer than any of
the sizing-round anchors and avoids accidental collisions between cells
that are genuinely distinct.
"""

from __future__ import annotations

import hashlib
import json
from typing import Iterable, Mapping


_PRECISION_DIGITS = 6
_HASH_LENGTH = 6
_PATH_SEPARATOR = " -> "


def canonicalize_params(params: Mapping[str, float], precision: int = _PRECISION_DIGITS) -> str:
    """Convert a parameter dict to a deterministic string form.

    Sorted keys, fixed-precision floats, JSON-serialized.
    """
    canonical = {}
    for key in sorted(params.keys()):
        value = params[key]
        if isinstance(value, bool):
            canonical[key] = value
        elif isinstance(value, (int, float)):
            canonical[key] = round(float(value), precision)
        else:
            canonical[key] = value
    return json.dumps(canonical, sort_keys=True, separators=(",", ":"))


def params_hash(params: Mapping[str, float], length: int = _HASH_LENGTH) -> str:
    """Short hex hash of the canonicalized parameter dict."""
    canonical = canonicalize_params(params)
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return digest[:length]


def node_label(phase_id: str, option_id: str, params: Mapping[str, float]) -> str:
    """Stable label for one phase-option-parameter triple."""
    return f"{phase_id}.{option_id}.{params_hash(params)}"


def path_label(node_labels: Iterable[str]) -> str:
    """Stable label for a sequence of nodes (one complete mission architecture)."""
    return _PATH_SEPARATOR.join(node_labels)
