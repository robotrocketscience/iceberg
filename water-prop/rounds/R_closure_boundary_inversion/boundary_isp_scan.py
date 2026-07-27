"""R-closure-boundary-inversion — Isp scan (deviation D-6, declared post-hoc).

Stage-1 bisection treated water-MET Isp as monotone. It is NOT: at fixed power
and delta-v, propellant need falls with Isp but power-limited burn time grows
roughly linearly with exhaust velocity (t = m*ve^2/2P with m ~ m0*dv/ve), so a
finite closure WINDOW in Isp can exist that 3-point monotonicity spot-checks
miss. This scan replaces the (invalid) Isp bisections with explicit scans, and
probes the honest-arm closure frontier.

Writes results/boundary_isp_scan.json.
"""

from __future__ import annotations

import json
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
ISP_SCAN = (800, 1000, 1200, 1500, 2000, 2500, 3000, 4000, 5000, 7000, 10000)

BASES = {
    "record_powerext": {},
    "S3_x5_33wkg": {"launcher_cap_multiplier": 5.0,
                    "reactor_specific_power_w_per_kg": 33.0},
}


def scan(arm_params, base, label):
    rows = {}
    for isp in ISP_SCAN:
        s = summarize(run_grid(dict(arm_params, **base, water_met_isp_s=float(isp)),
                               power=POWER_EXT))
        rows[isp] = {p: s[p] for p in PREDICATES} | {
            "max_delivered_t": s["max_delivered_t"]}
    window = [i for i, v in rows.items() if v["arrived_at_depot"] > 0]
    print(f"  {label}: closing Isp values {window or 'NONE'}; "
          f"best delivered {max(v['max_delivered_t'] for v in rows.values())} t")
    return rows


def strict_vs_waiver(params, power=POWER_EXT):
    cells = run_grid(params, power=power)
    strict = waiver = 0
    for c in cells:
        if c.skipped_reason is not None:
            continue
        for r in c.results:
            if r.is_feasible and r.closure_verdicts.get("arrived_at_depot") == "close":
                v = r.closure_verdicts.get("round_trip_time")
                if v == "close_strict":
                    strict += 1
                elif v == "close_waiver":
                    waiver += 1
    return {"paths_strict_15yr": strict, "paths_waiver_25yr": waiver}


def main():
    out = {}
    for arm_name, arm in (("armA_record", {}), ("armB_honest", dict(ARM_B_PARAMS))):
        print(f"== {arm_name} ==")
        block = {}
        for base_name, base in BASES.items():
            block[f"isp_scan[{base_name}]"] = scan(arm, base, f"{base_name}")
        out[arm_name] = block

    # Honest-arm frontier probes: what reaches 10 t / 30 t under arm B
    print("== armB frontier probes ==")
    probes = {
        "isp2000_x5_40wkg": {"water_met_isp_s": 2000.0, "launcher_cap_multiplier": 5.0,
                             "reactor_specific_power_w_per_kg": 40.0},
        "isp3000_x5_40wkg": {"water_met_isp_s": 3000.0, "launcher_cap_multiplier": 5.0,
                             "reactor_specific_power_w_per_kg": 40.0},
        "isp3000_x8_60wkg": {"water_met_isp_s": 3000.0, "launcher_cap_multiplier": 8.0,
                             "reactor_specific_power_w_per_kg": 60.0},
        "isp3000_x8_60wkg_f0.4": {"water_met_isp_s": 3000.0, "launcher_cap_multiplier": 8.0,
                                  "reactor_specific_power_w_per_kg": 60.0,
                                  "propellant_fraction": 0.40},
        "isp5000_x8_100wkg": {"water_met_isp_s": 5000.0, "launcher_cap_multiplier": 8.0,
                              "reactor_specific_power_w_per_kg": 100.0},
        "isp3000_x5_40wkg_500kwe": {"water_met_isp_s": 3000.0,
                                    "launcher_cap_multiplier": 5.0,
                                    "reactor_specific_power_w_per_kg": 40.0,
                                    "_power": (100.0, 200.0, 300.0, 500.0)},
    }
    fp = {}
    for name, extra in probes.items():
        power = extra.pop("_power", POWER_EXT)
        params = dict(ARM_B_PARAMS, **extra)
        s = summarize(run_grid(params, power=power))
        fp[name] = {p: s[p] for p in PREDICATES} | {
            "max_delivered_t": s["max_delivered_t"],
            "taxonomy_top3": dict(list(s["taxonomy"].items())[:3])}
        fp[name] |= strict_vs_waiver(params, power=power)
        print(f"  {name}: arrived={s['arrived_at_depot']} 10t={s['delivered_floor_10t']} "
              f"30t={s['delivered_floor']} max_t={s['max_delivered_t']} "
              f"strict={fp[name]['paths_strict_15yr']}")
    out["armB_frontier"] = fp

    # Strict-vs-waiver at the arm-A S5 scenario (are any closures 15-yr strict?)
    out["armA_S5_strict_vs_waiver"] = strict_vs_waiver(
        {"launcher_cap_multiplier": 5.0, "reactor_specific_power_w_per_kg": 33.0,
         "water_met_isp_s": 2000.0})
    print(f"armA S5 strict/waiver: {out['armA_S5_strict_vs_waiver']}")

    with open(HERE / "results" / "boundary_isp_scan.json", "w") as f:
        json.dump(out, f, indent=1)
    print("wrote results/boundary_isp_scan.json")


if __name__ == "__main__":
    main()
