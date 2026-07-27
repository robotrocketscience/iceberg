"""R-l0-relaxation-envelope proper round — three relaxation sweeps + failure taxonomy.

Pre-registration: STUDY.md (this directory). Deterministic; no randomness.

Run from project root:
  python water-prop/rounds/R_l0_relaxation_envelope/sweep_combined.py
"""

from __future__ import annotations

import json
import re
import sys
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

from saturn_water_v1_closure_sweep import (  # noqa: E402
    run_closed_loop,
    POWER_VALUES,
    CHUNK_VALUES,
    THRUST_VALUES,
)

YEAR_S = 365.25 * 86400.0

# Pre-registered axes (STUDY.md)
SWEEP1_FLOORS_T = (0.5, 1.0, 2.0, 5.0, 10.0, 15.0, 20.0, 25.0)
SWEEP1_CEILING_YR = 25.0
SWEEP2_CEILINGS_YR = (15.0, 18.0, 20.0, 22.0, 25.0, 28.0, 30.0, 35.0)
SWEEP2_FLOOR_T = 10.0
COMBINED_FLOOR_T = 5.0
COMBINED_CEILING_YR = 25.0
NON_NUCLEAR_KWE = (1.0, 10.0, 11.0)  # L0-24 vacated: RTG / solar-hybrid classes


def feasible_leaves(cell):
    if cell.skipped_reason is not None:
        return []
    return [r for r in cell.results if r.is_feasible and r.leaf_state is not None]


def arrivals(cell):
    """Feasible leaves that reached the LEO depot with positive payload."""
    out = []
    for r in feasible_leaves(cell):
        s = r.leaf_state
        if s.location == "LEO_depot" and s.payload_kg > 0.0:
            out.append(r)
    return out


def cell_closes_at(cell, floor_t: float, ceiling_yr: float) -> bool:
    for r in arrivals(cell):
        s = r.leaf_state
        if s.payload_kg >= floor_t * 1000.0 and s.time_elapsed_s / YEAR_S <= ceiling_yr:
            return True
    return False


def closure_rate(cells, floor_t, ceiling_yr, power_filter=None):
    pool = [c for c in cells
            if power_filter is None or c.coords.get("power_kwe") in power_filter]
    n_close = sum(1 for c in pool if cell_closes_at(c, floor_t, ceiling_yr))
    return n_close, len(pool)


_NUM = re.compile(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?")


def reason_class(reason: str) -> str:
    """Collapse numeric details so identical failure modes group together."""
    if reason is None:
        return "(none)"
    return _NUM.sub("#", reason).strip()[:140]


def failure_taxonomy(cells):
    tax = Counter()
    n_paths = 0
    n_feasible = 0
    for cell in cells:
        if cell.skipped_reason is not None:
            tax[("cell_skipped", reason_class(cell.skipped_reason))] += 1
            continue
        for r in cell.results:
            n_paths += 1
            if r.is_feasible:
                n_feasible += 1
            else:
                tax[(r.infeasible_at, reason_class(r.infeasible_reason))] += 1
    return tax, n_paths, n_feasible


def summarize(cells, tag):
    tax, n_paths, n_feasible = failure_taxonomy(cells)
    all_arr = [r for c in cells for r in arrivals(c)]
    best_payload_t = max((r.leaf_state.payload_kg / 1000.0 for r in all_arr), default=0.0)

    sweep1 = []
    for floor in SWEEP1_FLOORS_T:
        n_all, d_all = closure_rate(cells, floor, SWEEP1_CEILING_YR)
        n_nn, d_nn = closure_rate(cells, floor, SWEEP1_CEILING_YR, NON_NUCLEAR_KWE)
        sweep1.append({"floor_t": floor, "close_all": n_all, "of_all": d_all,
                       "close_nonnuclear": n_nn, "of_nonnuclear": d_nn})

    sweep2 = []
    for ceil in SWEEP2_CEILINGS_YR:
        n_all, d_all = closure_rate(cells, SWEEP2_FLOOR_T, ceil)
        n_nn, d_nn = closure_rate(cells, SWEEP2_FLOOR_T, ceil, NON_NUCLEAR_KWE)
        sweep2.append({"ceiling_yr": ceil, "close_all": n_all, "of_all": d_all,
                       "close_nonnuclear": n_nn, "of_nonnuclear": d_nn})

    combined_by_power = {}
    for p in POWER_VALUES:
        n, d = closure_rate(cells, COMBINED_FLOOR_T, COMBINED_CEILING_YR, (p,))
        combined_by_power[p] = {"close": n, "of": d}
    n_comb, d_comb = closure_rate(cells, COMBINED_FLOOR_T, COMBINED_CEILING_YR)

    print(f"\n===== {tag} =====")
    print(f"paths walked: {n_paths}  feasible leaves: {n_feasible}  "
          f"arrivals at LEO depot (payload>0): {len(all_arr)}  "
          f"best payload: {best_payload_t:.2f} t")
    print(f"H1 (any arrival): {'HOLDS' if all_arr else 'FALSIFIED'}")
    print("\nSweep 1 — L0-04 floor sensitivity (ceiling 25 yr):")
    for row in sweep1:
        print(f"  floor {row['floor_t']:5.1f} t: all-power {row['close_all']}/{row['of_all']}"
              f"  non-nuclear {row['close_nonnuclear']}/{row['of_nonnuclear']}")
    print("Sweep 2 — L0-05 ceiling sensitivity (floor 10 t):")
    for row in sweep2:
        print(f"  ceiling {row['ceiling_yr']:4.0f} yr: all-power {row['close_all']}/{row['of_all']}"
              f"  non-nuclear {row['close_nonnuclear']}/{row['of_nonnuclear']}")
    print(f"Sweep 3 — combined (floor {COMBINED_FLOOR_T} t, ceiling {COMBINED_CEILING_YR} yr): "
          f"{n_comb}/{d_comb} ({100.0*n_comb/max(d_comb,1):.1f} %)  by power: "
          + ", ".join(f"{p:.0f}kWe {v['close']}/{v['of']}" for p, v in combined_by_power.items()))
    print("\nFailure taxonomy (top 12, phase :: reason-class :: count):")
    for (phase, reason), count in tax.most_common(12):
        print(f"  {count:6d}  {phase} :: {reason}")

    return {
        "tag": tag,
        "n_paths": n_paths,
        "n_feasible_leaves": n_feasible,
        "n_arrivals": len(all_arr),
        "best_payload_t": best_payload_t,
        "sweep1_floor_sensitivity": sweep1,
        "sweep2_ceiling_sensitivity": sweep2,
        "sweep3_combined": {"close": n_comb, "of": d_comb,
                            "by_power": {str(k): v for k, v in combined_by_power.items()}},
        "failure_taxonomy_top25": [
            {"phase": phase, "reason": reason, "count": count}
            for (phase, reason), count in tax.most_common(25)
        ],
    }


def main():
    print("Running saturn_water_v1 closed-loop sweep (f = 0.80 baseline)...")
    base = run_closed_loop()
    print(f"  {len(base)} cells")
    out_base = summarize(base, "baseline f=0.80")

    print("\nRunning f = 0.20 guard-rail (STUDY deviation D-2)...")
    guard = run_closed_loop({"propellant_fraction": 0.20})
    out_guard = summarize(guard, "guard-rail f=0.20")

    out = Path(__file__).parent / "results"
    out.mkdir(exist_ok=True)
    payload = {
        "round": "R_l0_relaxation_envelope",
        "study": "STUDY.md pre-registration; corrected kick physics (post d379198)",
        "grid": {"power_kwe": list(POWER_VALUES),
                 "chunk_t": [c / 1000.0 for c in CHUNK_VALUES],
                 "thrust_n": list(THRUST_VALUES)},
        "non_nuclear_kwe": list(NON_NUCLEAR_KWE),
        "baseline": out_base,
        "guard_rail_f020": out_guard,
    }
    (out / "closure_rate_envelope.json").write_text(json.dumps(payload, indent=2))
    print(f"\nWrote {out / 'closure_rate_envelope.json'}")


if __name__ == "__main__":
    main()
