"""In-session sanity check: do any L0 relaxations bring back commercial closure under saturn_water_v1?

Uses the existing closed-loop closure sweep (150 cells) and counts cells that close at
each (L0-04 floor, L0-05 ceiling) combination across power classes including the
non-nuclear regime (1 kilowatt-electric, RTG-class).

Produces a closure table per (delivered-mass floor, round-trip ceiling, power class).
Headline question: which combinations of relaxations bring closure rate above zero?

Run from project root:
  python water-prop/rounds/R_l0_relaxation_envelope/relaxation_sweep.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def _ensure_import_path():
    here = Path(__file__).resolve()
    sims_dir = here.parents[2] / "sims"
    if str(sims_dir) not in sys.path:
        sys.path.insert(0, str(sims_dir))
    sweeps_dir = sims_dir / "mission_graph" / "missions" / "sweeps"
    if str(sweeps_dir) not in sys.path:
        sys.path.insert(0, str(sweeps_dir))


_ensure_import_path()


from saturn_water_v1_closure_sweep import (  # noqa: E402
    run_closed_loop,
    POWER_VALUES,
    CHUNK_VALUES,
    THRUST_VALUES,
)


L0_04_FLOORS = (
    ("delivered_floor_10t", 10),
    ("delivered_floor_20t", 20),
    ("delivered_floor",     30),
    ("delivered_floor_50t", 50),
    ("delivered_floor_100t", 100),
)


def cell_floor_close(cell, predicate_name: str) -> tuple[bool, float]:
    """(closes, best_round_trip_years) under the named delivered-floor predicate.

    Returns (False, inf) if the cell is skipped or no path closes the predicate.
    """
    if cell.skipped_reason is not None:
        return (False, float("inf"))
    best_rt = float("inf")
    closes = False
    for r in cell.results:
        if not r.is_feasible:
            continue
        if r.closure_verdicts.get(predicate_name) in ("close", "close_strict", "close_waiver"):
            closes = True
            rt = r.final_state.time_elapsed_s / (365.25 * 86400.0)
            if rt < best_rt:
                best_rt = rt
    return (closes, best_rt)


def closure_at_floor_and_ceiling(cells, predicate_name: str, ceiling_years: float):
    """How many cells close at this (floor, ceiling) combination?

    A cell qualifies if some path through it satisfies BOTH the delivered-floor
    predicate AND round-trip <= ceiling_years.
    """
    qualifying = 0
    closers_by_power = {}
    for cell in cells:
        closes, rt = cell_floor_close(cell, predicate_name)
        if closes and rt <= ceiling_years:
            qualifying += 1
            power = cell.coords.get("power_kwe")
            closers_by_power.setdefault(power, 0)
            closers_by_power[power] += 1
    return qualifying, closers_by_power


def main():
    print("Running saturn_water_v1 closed-loop closure sweep...")
    cells = run_closed_loop()
    print(f"  {len(cells)} cells swept")

    # Build closure table: rows = (L0-04 floor in tonnes), cols = (L0-05 ceiling in years)
    ceilings = (15.0, 20.0, 25.0, 30.0, 9999.0)  # last = no ceiling
    rows = []
    for pred_name, floor_t in L0_04_FLOORS:
        cols = []
        for ceiling in ceilings:
            count, by_power = closure_at_floor_and_ceiling(cells, pred_name, ceiling)
            cols.append({"ceiling_yr": ceiling, "count": count, "by_power": by_power})
        rows.append({"floor_t": floor_t, "predicate": pred_name, "ceilings": cols})

    # Console output
    print("\n=== Closure table: L0-04 floor (rows) x L0-05 ceiling (cols) ===")
    print(f"Power axis: {POWER_VALUES} kilowatts-electric")
    print(f"Chunk axis: {[c/1000 for c in CHUNK_VALUES]} tonnes")
    print(f"Thrust axis: {THRUST_VALUES} N")
    print(f"Total cells per sweep: {len(cells)}")
    print()
    header = " floor_t | " + " | ".join(f"<={c:.0f}yr" if c < 1000 else "any RT" for c in ceilings)
    print(header)
    print("-" * len(header))
    for row in rows:
        cells_str = " | ".join(f"{c['count']:>7d}" for c in row["ceilings"])
        print(f" {row['floor_t']:>7d}t | {cells_str}")

    # Per-power breakdown at the most-relaxed (any-ceiling) bucket per floor
    print("\n=== Closures at any round-trip ceiling, by power class ===")
    print(f"{'floor_t':>8s} | " + " | ".join(f"{p:>5.0f}kWe" for p in POWER_VALUES))
    print("-" * 80)
    for row in rows:
        last = row["ceilings"][-1]  # no ceiling
        cells_str = " | ".join(
            f"{last['by_power'].get(p, 0):>7d}" for p in POWER_VALUES
        )
        print(f" {row['floor_t']:>7d}t | {cells_str}")

    # Save JSON
    out = Path(__file__).parent / "results"
    out.mkdir(exist_ok=True)
    (out / "relaxation_sweep.json").write_text(json.dumps({
        "n_cells": len(cells),
        "power_kwe_axis": list(POWER_VALUES),
        "chunk_mass_t_axis": [c/1000 for c in CHUNK_VALUES],
        "thrust_n_axis": list(THRUST_VALUES),
        "ceilings_yr": list(ceilings),
        "rows": rows,
    }, indent=2))
    print(f"\nWrote {out / 'relaxation_sweep.json'}")


if __name__ == "__main__":
    main()
