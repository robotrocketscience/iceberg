"""R-closure-boundary-inversion — Stage 3 conditional bisections + cell detail.

Per STUDY stage 3 (2-D / conditional boundaries around found thresholds):
holding the S3 scenario base fixed (launcher x5, 33 W/kg, extended power grid),
bisect the remaining axes for each predicate; dump closing-cell coordinates
with a power-thrust consistency flag (D-4: the framework does not enforce
F <= 2P/ve in P1; closures relying on inconsistent cells are flagged).

Writes results/boundary_conditional.json.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from boundary_sweep import (  # noqa: E402
    ARM_B_PARAMS,
    PREDICATES,
    RECORD_POWER,
    run_grid,
    summarize,
)

POWER_EXT = RECORD_POWER + (100.0, 200.0)

S3_BASE = {"launcher_cap_multiplier": 5.0, "reactor_specific_power_w_per_kg": 33.0}


def closes_at(params, predicate):
    return summarize(run_grid(params, power=POWER_EXT))[predicate] >= 1


def bisect_min(name, lo, hi, base, predicate, rel_tol=0.02):
    """Smallest value in [lo,hi] that closes, holding `base` fixed."""
    if closes_at(dict(base, **{name: lo}), predicate):
        return lo
    if not closes_at(dict(base, **{name: hi}), predicate):
        return None
    while (hi - lo) / hi > rel_tol:
        mid = 0.5 * (lo + hi)
        if closes_at(dict(base, **{name: mid}), predicate):
            hi = mid
        else:
            lo = mid
    return round(hi, 1)


def min_power_class(base, predicate, isp):
    """Smallest single power class that closes with the S3 base + given Isp."""
    for p_kwe in (30.0, 55.0, 75.0, 100.0, 150.0, 200.0, 300.0, 500.0):
        s = summarize(run_grid(dict(base, water_met_isp_s=isp), power=(p_kwe,)))
        if s[predicate] >= 1:
            return p_kwe
    return None


def cell_detail(params, power=POWER_EXT):
    """Closing-cell coordinates + delivered mass + power-thrust consistency."""
    cells = run_grid(params, power=power)
    rows = []
    for c in cells:
        if c.skipped_reason is not None:
            continue
        for r in c.results:
            if not r.is_feasible:
                continue
            if r.closure_verdicts.get("arrived_at_depot") != "close":
                continue
            coords = dict(c.coords)
            p_kwe = coords.get("power_kwe")
            thrust = coords.get("electric_thrust_n")
            isp_e = params.get("electric_isp_s", 3000.0)
            f_max = 2.0 * p_kwe * 1000.0 / (isp_e * 9.81)
            rows.append({
                "power_kwe": p_kwe,
                "chunk_t": coords.get("chunk_mass_kg") / 1000.0,
                "thrust_n": thrust,
                "delivered_t": round(r.leaf_state.payload_kg / 1000.0, 2),
                "years": round(r.leaf_state.time_elapsed_s / (365.25 * 86400), 1),
                "round_trip": r.closure_verdicts.get("round_trip_time"),
                "power_thrust_consistent": thrust <= f_max + 1e-9,
                "options": list(r.option_ids) if hasattr(r, "option_ids") else None,
            })
    rows.sort(key=lambda x: -x["delivered_t"])
    return rows


def main():
    out = {}
    for arm_name, arm in (("armA_record", {}), ("armB_honest", dict(ARM_B_PARAMS))):
        base = dict(arm, **S3_BASE)
        block = {}
        # Conditional Isp thresholds under S3 base
        for pred in PREDICATES:
            block[f"min_water_met_isp_s[{pred}]"] = bisect_min(
                "water_met_isp_s", 800.0, 20000.0, base, pred)
        # Min launcher multiplier at Isp 2000 (S5 propulsion)
        s5 = dict(arm, reactor_specific_power_w_per_kg=33.0, water_met_isp_s=2000.0)
        for pred in PREDICATES:
            block[f"min_launcher_multiplier[{pred}]@isp2000"] = bisect_min(
                "launcher_cap_multiplier", 1.0, 16.0, s5, pred)
        # Min specific power at Isp 2000 + launcher x5
        s5l = dict(arm, launcher_cap_multiplier=5.0, water_met_isp_s=2000.0)
        for pred in PREDICATES:
            block[f"min_specific_power_w_per_kg[{pred}]@isp2000_x5"] = bisect_min(
                "reactor_specific_power_w_per_kg", 2.4, 400.0, s5l, pred)
        # Min single power class
        for isp in (900.0, 2000.0, 3000.0):
            block[f"min_power_class_kwe@isp{int(isp)}"] = min_power_class(
                base, "arrived_at_depot", isp)
        # Cell detail at the S5 scenario
        block["S5_closing_cells"] = cell_detail(
            dict(arm, **S3_BASE, water_met_isp_s=2000.0))[:12]
        # Demonstrator failure taxonomy (why S7b fails)
        s = summarize(run_grid(dict(arm, water_met_isp_s=1500.0,
                                    chunk_fed_min_power_kwe=10.0),
                               chunk=(500.0, 1000.0, 2000.0, 5000.0),
                               power=(10.0, 20.0, 30.0)))
        block["demonstrator_taxonomy"] = s["taxonomy"]
        out[arm_name] = block
        print(f"== {arm_name} ==")
        for k, v in block.items():
            if k != "S5_closing_cells":
                print(f"  {k}: {v}")
        for row in block["S5_closing_cells"][:6]:
            print(f"    cell {row}")

    with open(HERE / "results" / "boundary_conditional.json", "w") as f:
        json.dump(out, f, indent=1)
    print("wrote results/boundary_conditional.json")


if __name__ == "__main__":
    main()
