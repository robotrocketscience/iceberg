"""R-per-phase-propellant-fidelity — minimal-f scan per path family.

See STUDY.md. Writes results/min_multiplier_vs_f.json.

Run from repo root:
  PYTHONPATH=water-prop/sims water-prop/.venv/bin/python \
      water-prop/rounds/R_per_phase_propellant_fidelity/run.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SIMS = HERE.parents[1] / "sims"
if str(SIMS) not in sys.path:
    sys.path.insert(0, str(SIMS))

from mission_graph.framework import VehicleState, walk  # noqa: E402
from mission_graph.missions.saturn_water_v1 import (  # noqa: E402
    saturn_water_v1, make_derived_mass_transform)
from mission_graph.missions.saturn_water_v2 import (  # noqa: E402
    saturn_water_v2, make_derived_mass_transform_v2)

BASE = {
    "chemical_isp_s": 340.0, "electric_isp_s": 3000.0,
    "electric_thrust_n": 10.0, "water_met_isp_s": 800.0,
    "launch_epoch_jd": 0.0, "multi_falcon_launch_count": 6,
}

CORRIDOR = {  # v2 electrolysis-NTP posture (latest+29c self-consistent corridor)
    "capture_arch": "harpoon", "plans_aerocapture": False,
    "reactor_specific_power_w_per_kg": 33.0, "electrolysis_isp_s": 900.0,
}
ELECTRIC = {  # v1 arm-B-resolved electric family
    "visviva_capture": True, "chunk_fed_dv_km_s": 22.5,
    "reactor_lifetime_years": 10.0, "water_met_isp_s": 3000.0,
    "reactor_specific_power_w_per_kg": 60.0,
}

F_GRID = [round(0.30 + 0.05 * i, 2) for i in range(12)]  # 0.30..0.85


def best_delivered(mission, transform_maker, params, power, chunk,
                   floor_kg, non_aero, electro_only):
    bp = dict(BASE, **params, chunk_mass_kg=chunk)
    tr = transform_maker(bp)
    st = VehicleState(mass_kg=1.0, propellant_kg=0.0, payload_kg=0.0,
                      location="pre_launch", v_inf_km_s=0.0, time_elapsed_s=0.0,
                      epoch_jd=None, power_available_kwe=power)
    st = tr(st, {"power_kwe": power, "chunk_mass_kg": chunk,
                 "electric_thrust_n": bp["electric_thrust_n"]})
    best = 0.0
    for r in walk(mission, st, bp):
        if not r.is_feasible:
            continue
        if r.closure_verdicts.get("arrived_at_depot") != "close":
            continue
        if non_aero and "aero" in r.path_label:
            continue
        if electro_only and "electrolysis" not in r.path_label:
            continue
        best = max(best, r.leaf_state.payload_kg)
    return best if best >= floor_kg else 0.0


def min_multiplier(mission, tm, params, power, chunk, floor_kg,
                   non_aero, electro_only, lo=1.0, hi=32.0):
    def ok(m):
        return best_delivered(mission, tm, dict(params, launcher_cap_multiplier=m),
                              power, chunk, floor_kg, non_aero, electro_only) > 0
    if not ok(hi):
        return None, 0.0
    while hi - lo > 0.25:
        mid = 0.5 * (lo + hi)
        if ok(mid):
            hi = mid
        else:
            lo = mid
    d = best_delivered(mission, tm, dict(params, launcher_cap_multiplier=hi),
                       power, chunk, floor_kg, non_aero, electro_only)
    return round(hi, 2), round(d / 1000.0, 1)


def main():
    out = {}
    cases = [
        ("corridor_150kwe_500t", saturn_water_v2, make_derived_mass_transform_v2,
         CORRIDOR, 150.0, 500_000.0, 30_000.0, True, True),
        ("corridor_200kwe_1000t", saturn_water_v2, make_derived_mass_transform_v2,
         CORRIDOR, 200.0, 1_000_000.0, 30_000.0, True, True),
        ("electric_200kwe_500t_10tfloor", saturn_water_v1, make_derived_mass_transform,
         ELECTRIC, 200.0, 500_000.0, 10_000.0, False, False),
    ]
    for name, mission, tm, fam, power, chunk, floor, non_aero, eo in cases:
        rows = {}
        for f in F_GRID:
            m, d = min_multiplier(mission, tm, dict(fam, propellant_fraction=f),
                                  power, chunk, floor, non_aero, eo)
            rows[f] = {"min_multiplier": m, "delivered_t": d}
            print(f"{name} f={f}: min_mult={m} delivered={d} t", flush=True)
        feasible = {f: v for f, v in rows.items() if v["min_multiplier"]}
        if feasible:
            f_opt = min(feasible, key=lambda f: feasible[f]["min_multiplier"])
            out[name] = {"scan": rows, "f_optimal": f_opt,
                         "min_mult_at_opt": feasible[f_opt]["min_multiplier"],
                         "min_mult_at_f080": rows.get(0.80, {}).get("min_multiplier"),
                         "delivered_at_opt_t": feasible[f_opt]["delivered_t"]}
        else:
            out[name] = {"scan": rows, "f_optimal": None}
        print(f"== {name}: f_opt={out[name].get('f_optimal')} "
              f"mult_opt={out[name].get('min_mult_at_opt')} "
              f"mult@0.80={out[name].get('min_mult_at_f080')}")
    (HERE / "results").mkdir(exist_ok=True)
    with open(HERE / "results" / "min_multiplier_vs_f.json", "w") as fjs:
        json.dump(out, fjs, indent=1)
    print("wrote results/min_multiplier_vs_f.json")


if __name__ == "__main__":
    main()
