"""Aggregation over Sequence[SweepCell].

Pure functions. No formatting, no mutation, no I/O. Mirror the patterns
in mining_view.py (bucket-by-something + best-per-bucket).

Vocabulary:
  - "close verdicts" are the verdict strings that count as a closure for a
    given predicate. Default is ("close", "close_strict", "close_waiver")
    to match the campaign matrix's threshold-laden predicates.
  - "marginal" means: collapse all other axes, sum across them, report per
    value on the named axis. Matches the matrix's standard reading.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Dict, Mapping, Optional, Sequence, Set, Tuple

from ..framework import SweepCell, WalkResult


DEFAULT_CLOSE_VERDICTS: Tuple[str, ...] = ("close", "close_strict", "close_waiver")


def closure_by_cell(
    cells: Sequence[SweepCell],
    predicate_name: str,
) -> Dict[int, Dict[str, int]]:
    """Per-cell: verdict-string -> count, for one predicate, across feasible
    results in the cell."""
    out: Dict[int, Dict[str, int]] = {}
    for cell in cells:
        counts: Dict[str, int] = defaultdict(int)
        for r in cell.results:
            if not r.is_feasible:
                continue
            verdict = r.closure_verdicts.get(predicate_name)
            if verdict is None:
                continue
            counts[verdict] += 1
        out[cell.cell_id] = dict(counts)
    return out


def floor_close_count(
    cells: Sequence[SweepCell],
    predicate_name: str,
    close_verdicts: Sequence[str] = DEFAULT_CLOSE_VERDICTS,
) -> Dict[int, Tuple[int, int]]:
    """Per-cell: (n_close, n_total_feasible) for one predicate. Matches the
    matrix's 'X of N close at conditions Y' headline shape."""
    out: Dict[int, Tuple[int, int]] = {}
    close_set = set(close_verdicts)
    for cell in cells:
        n_close = 0
        n_total = 0
        for r in cell.results:
            if not r.is_feasible:
                continue
            verdict = r.closure_verdicts.get(predicate_name)
            if verdict is None:
                continue
            n_total += 1
            if verdict in close_set:
                n_close += 1
        out[cell.cell_id] = (n_close, n_total)
    return out


def best_delivery_per_cell(
    cells: Sequence[SweepCell],
) -> Dict[int, Optional[WalkResult]]:
    """Per-cell: feasible WalkResult with maximum leaf payload_kg. None if
    no feasible result. Mirrors best_per_bucket in mining_view.py."""
    out: Dict[int, Optional[WalkResult]] = {}
    for cell in cells:
        feasible = [r for r in cell.results if r.is_feasible]
        if not feasible:
            out[cell.cell_id] = None
            continue
        out[cell.cell_id] = max(feasible, key=lambda r: r.leaf_state.payload_kg)
    return out


def marginal_closure(
    cells: Sequence[SweepCell],
    axis_name: str,
    predicate_name: str,
    close_verdicts: Sequence[str] = DEFAULT_CLOSE_VERDICTS,
) -> Dict[float, Tuple[int, int]]:
    """Collapse all axes except `axis_name`. Sum (n_close, n_total) across
    the collapsed axes per value of the named axis.

    This is the 'holding all other axes' forward-propagation readout. The
    denominator is feasible-result count (matrix convention).
    """
    close_set = set(close_verdicts)
    sums: Dict[float, Tuple[int, int]] = defaultdict(lambda: (0, 0))
    for cell in cells:
        if axis_name not in cell.coords:
            continue
        axis_val = cell.coords[axis_name]
        prev_close, prev_total = sums[axis_val]
        n_close = 0
        n_total = 0
        for r in cell.results:
            if not r.is_feasible:
                continue
            verdict = r.closure_verdicts.get(predicate_name)
            if verdict is None:
                continue
            n_total += 1
            if verdict in close_set:
                n_close += 1
        sums[axis_val] = (prev_close + n_close, prev_total + n_total)
    return dict(sums)


def back_propagate(
    cells: Sequence[SweepCell],
    predicate_name: str,
    target_verdicts: Sequence[str] = DEFAULT_CLOSE_VERDICTS,
) -> Dict[str, Set[float]]:
    """For cells with at least one result matching any target verdict,
    collect each axis's value. Returns axis_name -> set of admitting
    values. Direct answer to 'which axis values enable closure?'"""
    target_set = set(target_verdicts)
    admitting: Dict[str, Set[float]] = defaultdict(set)
    for cell in cells:
        if cell.skipped_reason is not None:
            continue
        cell_admits = False
        for r in cell.results:
            if not r.is_feasible:
                continue
            verdict = r.closure_verdicts.get(predicate_name)
            if verdict in target_set:
                cell_admits = True
                break
        if not cell_admits:
            continue
        for axis_name, axis_val in cell.coords.items():
            admitting[axis_name].add(axis_val)
    return dict(admitting)


def architectures_admitted(
    cells: Sequence[SweepCell],
) -> Dict[int, Tuple[str, ...]]:
    """Per-cell: sorted tuple of path_labels that arrived end-to-end."""
    out: Dict[int, Tuple[str, ...]] = {}
    for cell in cells:
        labels = sorted({r.path_label for r in cell.results if r.is_feasible})
        out[cell.cell_id] = tuple(labels)
    return out


def architecture_cell_counts(
    cells: Sequence[SweepCell],
) -> Dict[str, int]:
    """Inverse view: path_label -> number of cells where it appears
    feasible end-to-end. Useful for ranking 'most-robust architectures'."""
    counts: Dict[str, int] = defaultdict(int)
    for cell in cells:
        seen = {r.path_label for r in cell.results if r.is_feasible}
        for label in seen:
            counts[label] += 1
    return dict(counts)
