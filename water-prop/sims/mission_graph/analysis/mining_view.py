"""Mining-company economics view over walker results.

Reframes raw WalkResults into the metrics a mining-company operator cares
about: time-to-first-revenue, annual throughput (steady-state), tonnage
per ship, and capital lock-up. The intent is to make the time-vs-yield
trade visible so an operator can pick an architecture by economic shape,
not just by delivered tonnage alone.

Definitions:
  - round_trip_years: total elapsed time per ship, pre-launch -> depot
  - delivered_t: payload mass at depot, in tonnes
  - throughput_t_per_yr: delivered_t / round_trip_years (steady-state
    assumption: one ship returns per round-trip duration)
  - time_bucket: round-trip duration rounded into 1-year bins

A 'mining timeline' sweep groups feasible architectures by their
round-trip year and reports the best throughput in each bucket. This
answers the operator question: 'I'm willing to wait X years for first
revenue; what's the best architecture I can run, and what does it
deliver?'
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable, Sequence

from ..framework import WalkResult


SECONDS_PER_YEAR = 365.25 * 86_400


@dataclass(frozen=True)
class MiningMetrics:
    path_label: str
    round_trip_years: float
    delivered_t: float
    throughput_t_per_yr: float
    closure_verdicts: dict


def to_mining_metrics(result: WalkResult) -> MiningMetrics | None:
    """Convert a single WalkResult into mining metrics. Returns None if
    the result was infeasible or has no leaf state."""
    if not result.is_feasible or result.leaf_state is None:
        return None
    years = result.leaf_state.time_elapsed_s / SECONDS_PER_YEAR
    delivered_t = result.leaf_state.payload_kg / 1000.0
    throughput = delivered_t / years if years > 0 else 0.0
    return MiningMetrics(
        path_label=result.path_label,
        round_trip_years=years,
        delivered_t=delivered_t,
        throughput_t_per_yr=throughput,
        closure_verdicts=dict(result.closure_verdicts),
    )


def feasible_metrics(results: Iterable[WalkResult]) -> tuple[MiningMetrics, ...]:
    """Filter to feasible results and convert each to mining metrics."""
    out = []
    for r in results:
        m = to_mining_metrics(r)
        if m is not None:
            out.append(m)
    return tuple(out)


def bucket_by_round_trip_year(
    metrics: Sequence[MiningMetrics],
    min_year: float,
    max_year: float,
) -> dict[int, list[MiningMetrics]]:
    """Group metrics by integer-year round-trip bucket within [min_year, max_year]."""
    buckets: dict[int, list[MiningMetrics]] = defaultdict(list)
    for m in metrics:
        if m.round_trip_years < min_year or m.round_trip_years > max_year:
            continue
        bucket_year = int(m.round_trip_years)
        buckets[bucket_year].append(m)
    return dict(buckets)


def best_per_bucket(
    buckets: dict[int, list[MiningMetrics]],
    key: str = "throughput_t_per_yr",
) -> list[MiningMetrics]:
    """For each time bucket, return the metric with the highest `key`."""
    out = []
    for year in sorted(buckets.keys()):
        best = max(buckets[year], key=lambda m: getattr(m, key))
        out.append(best)
    return out


def short_path_label(metrics: MiningMetrics) -> str:
    """Strip phase prefixes and hashes; keep option_ids in a -> chain."""
    parts = metrics.path_label.split(" -> ")
    return " -> ".join(p.split(".")[1] for p in parts)
