"""R-vehicle-mass-fidelity-refinement — H1/H4/H5 sweep harness.

Sweeps launch propellant fraction f x plans_aerocapture over the standard
150-cell closed-loop grid. See STUDY.md for pre-registered predictions.

Run from project root:
  python3 water-prop/rounds/R_vehicle_mass_fidelity_refinement/run.py

Writes results/fidelity_sweep.json (small aggregate; not committed).
"""

from __future__ import annotations

import json
import sys
import time
from collections import Counter
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

from saturn_water_v1_closure_sweep import run_closed_loop, cell_closes  # noqa: E402


F_GRID = (0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.88, 0.92)
AEROCAPTURE = (True, False)
PREDICATES = (
    "arrived_at_depot",
    "delivered_floor_10t",
    "delivered_floor_20t",
    "delivered_floor",        # 30 t
    "delivered_floor_50t",
    "delivered_floor_100t",
)


def closure_summary(cells):
    """Per-predicate closure counts + per-cell closure sets."""
    counts = {p: 0 for p in PREDICATES}
    closing_cells = {p: set() for p in PREDICATES}
    by_power = {p: Counter() for p in PREDICATES}
    by_chunk = {p: Counter() for p in PREDICATES}
    for cell in cells:
        for p in PREDICATES:
            if cell_closes(cell, p):
                counts[p] += 1
                closing_cells[p].add(cell.cell_id)
                by_power[p][cell.coords.get("power_kwe")] += 1
                by_chunk[p][cell.coords.get("chunk_mass_kg")] += 1
    return counts, closing_cells, by_power, by_chunk


def main():
    runs = []
    union = {ac: {p: set() for p in PREDICATES} for ac in AEROCAPTURE}
    union_power = {ac: {p: Counter() for p in PREDICATES} for ac in AEROCAPTURE}
    union_chunk = {ac: {p: Counter() for p in PREDICATES} for ac in AEROCAPTURE}

    for ac in AEROCAPTURE:
        for f in F_GRID:
            t0 = time.time()
            cells = run_closed_loop(extra_params={
                "propellant_fraction": f,
                "plans_aerocapture": ac,
            })
            counts, closing, by_power, by_chunk = closure_summary(cells)
            dt = time.time() - t0
            runs.append({
                "f": f, "plans_aerocapture": ac,
                "counts": counts,
                "by_power": {p: dict(by_power[p]) for p in PREDICATES},
                "by_chunk": {p: dict(by_chunk[p]) for p in PREDICATES},
                "runtime_s": round(dt, 1),
            })
            for p in PREDICATES:
                union[ac][p] |= closing[p]
                union_power[ac][p].update(by_power[p])
                union_chunk[ac][p].update(by_chunk[p])
            arr = counts["arrived_at_depot"]
            print(f"f={f:.2f} aerocapture={ac!s:5s}  arrived={arr:>3d}  "
                  f"10t={counts['delivered_floor_10t']:>3d}  "
                  f"20t={counts['delivered_floor_20t']:>3d}  "
                  f"30t={counts['delivered_floor']:>3d}  "
                  f"50t={counts['delivered_floor_50t']:>3d}  ({dt:.0f}s)", flush=True)

    print("\n=== best-f-per-cell union (H1 upper bound on any per-phase derivation) ===")
    for ac in AEROCAPTURE:
        line = "  ".join(f"{p.replace('delivered_floor', 'floor')}={len(union[ac][p])}" for p in PREDICATES)
        print(f"aerocapture={ac!s:5s}: {line}")

    out = Path(__file__).parent / "results"
    out.mkdir(exist_ok=True)
    (out / "fidelity_sweep.json").write_text(json.dumps({
        "f_grid": F_GRID,
        "runs": runs,
        "union_best_f": {
            str(ac): {p: sorted(union[ac][p]) for p in PREDICATES} for ac in AEROCAPTURE
        },
        "union_by_power": {
            str(ac): {p: {str(k): v for k, v in union_power[ac][p].items()} for p in PREDICATES}
            for ac in AEROCAPTURE
        },
        "union_by_chunk": {
            str(ac): {p: {str(k): v for k, v in union_chunk[ac][p].items()} for p in PREDICATES}
            for ac in AEROCAPTURE
        },
    }, indent=2))
    print(f"wrote {out / 'fidelity_sweep.json'}")


if __name__ == "__main__":
    main()
