"""R-saturn-water-v2-electrolysis-departure — closure sweep (H-V1..H-V5).

Sweeps saturn_water_v2 (electrolysis H2/O2 impulsive departure) against the
matched saturn_water_v1 baseline at identical parameters, per STUDY.md:
power {30,55,100,150,200} kWe x chunk {50,100,200,300,500} t x thrust
{2.5,10,25} N; arms A/B; launcher multiplier {1,5,8}.

Run from repo root:
  PYTHONPATH=water-prop/sims water-prop/.venv/bin/python \
      water-prop/rounds/R_saturn_water_v2_electrolysis_departure/run.py

Writes results/v2_closure_results.json (small, committed).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SIMS = HERE.parents[1] / "sims"
if str(SIMS) not in sys.path:
    sys.path.insert(0, str(SIMS))

from mission_graph.framework import SweepAxis, VehicleAxis, VehicleState, sweep  # noqa: E402
from mission_graph.missions.saturn_water_v1 import (  # noqa: E402
    saturn_water_v1,
    make_derived_mass_transform,
)
from mission_graph.missions.saturn_water_v2 import (  # noqa: E402
    saturn_water_v2,
    make_derived_mass_transform_v2,
)

POWER = (30.0, 55.0, 100.0, 150.0, 200.0)
CHUNK = (50_000.0, 100_000.0, 200_000.0, 300_000.0, 500_000.0)
THRUST = (2.5, 10.0, 25.0)

BASE_PARAMS = {
    "chemical_isp_s": 340.0,
    "electric_isp_s": 3000.0,
    "electric_thrust_n": 5.0,
    "water_met_isp_s": 800.0,
    "chunk_mass_kg": 50_000.0,
    "multi_falcon_launch_count": 6,
    "launch_epoch_jd": 0.0,
}

ARM_B = {"visviva_capture": True, "chunk_fed_dv_km_s": 18.0,
         "reactor_lifetime_years": 10.0}

PREDICATES = ("arrived_at_depot", "delivered_floor_10t", "delivered_floor")


def run(mission, transform_maker, extra):
    bp = dict(BASE_PARAMS)
    bp.update(extra)
    state = VehicleState(
        mass_kg=50_000.0, propellant_kg=0.0, payload_kg=0.0,
        location="pre_launch", v_inf_km_s=0.0, time_elapsed_s=0.0,
        epoch_jd=None, power_available_kwe=30.0,
    )
    return sweep(
        mission, state, bp,
        param_axes=[SweepAxis("chunk_mass_kg", CHUNK),
                    SweepAxis("electric_thrust_n", THRUST)],
        vehicle_axes=[VehicleAxis("power_kwe", POWER, "power_available_kwe")],
        state_transform=transform_maker(bp),
    )


def summarize(cells, electrolysis_only=False):
    out = {p: 0 for p in PREDICATES}
    max_delivered = 0.0
    best_cell = None
    taxonomy: dict[str, int] = {}
    electro_paths = 0
    strict = waiver = 0
    for c in cells:
        if c.skipped_reason is not None:
            continue
        cell_close = {p: False for p in PREDICATES}
        for r in c.results:
            used_electro = "electrolysis_kick_departure" in r.path_label
            if electrolysis_only and not used_electro:
                continue
            if r.is_feasible:
                if used_electro:
                    electro_paths += 1
                arrived = r.closure_verdicts.get("arrived_at_depot") == "close"
                if arrived:
                    v = r.closure_verdicts.get("round_trip_time")
                    strict += v == "close_strict"
                    waiver += v == "close_waiver"
                for p in PREDICATES:
                    if r.closure_verdicts.get(p) in ("close", "close_strict", "close_waiver"):
                        cell_close[p] = True
                if r.leaf_state.location == "LEO_depot" and r.leaf_state.payload_kg > max_delivered:
                    max_delivered = r.leaf_state.payload_kg
                    best_cell = dict(c.coords) | {"used_electrolysis": used_electro}
            else:
                ph = r.infeasible_at or "unknown"
                taxonomy[ph] = taxonomy.get(ph, 0) + 1
        for p in PREDICATES:
            if cell_close[p]:
                out[p] += 1
    out["max_delivered_t"] = round(max_delivered / 1000.0, 2)
    out["best_cell"] = best_cell
    out["feasible_electrolysis_paths"] = electro_paths
    out["paths_strict_15yr"] = strict
    out["paths_waiver_25yr"] = waiver
    out["taxonomy_top4"] = dict(sorted(taxonomy.items(), key=lambda kv: -kv[1])[:4])
    return out


def main():
    results = {}
    for arm_name, arm in (("armA_record", {}), ("armB_honest", dict(ARM_B))):
        for mult in (1.0, 5.0, 8.0):
            extra = dict(arm, launcher_cap_multiplier=mult)
            v2 = summarize(run(saturn_water_v2, make_derived_mass_transform_v2, extra))
            v2e = summarize(run(saturn_water_v2, make_derived_mass_transform_v2, extra),
                            electrolysis_only=True)
            v1 = summarize(run(saturn_water_v1, make_derived_mass_transform, extra))
            key = f"{arm_name}_x{int(mult)}"
            results[key] = {"v2_all": v2, "v2_electrolysis_paths_only": v2e,
                            "v1_matched": v1}
            print(f"{key}:")
            print(f"  v1 matched : arrived={v1['arrived_at_depot']:3d} 10t={v1['delivered_floor_10t']:3d} "
                  f"30t={v1['delivered_floor']:3d} max={v1['max_delivered_t']} t")
            print(f"  v2 all     : arrived={v2['arrived_at_depot']:3d} 10t={v2['delivered_floor_10t']:3d} "
                  f"30t={v2['delivered_floor']:3d} max={v2['max_delivered_t']} t "
                  f"strict={v2['paths_strict_15yr']} waiver={v2['paths_waiver_25yr']}")
            print(f"  v2 electro : arrived={v2e['arrived_at_depot']:3d} 10t={v2e['delivered_floor_10t']:3d} "
                  f"30t={v2e['delivered_floor']:3d} max={v2e['max_delivered_t']} t "
                  f"paths={v2e['feasible_electrolysis_paths']} tax={v2e['taxonomy_top4']}")
            print(f"  v2 best cell: {v2['best_cell']}")

    out = HERE / "results"
    out.mkdir(exist_ok=True)
    with open(out / "v2_closure_results.json", "w") as f:
        json.dump(results, f, indent=1)
    print("wrote results/v2_closure_results.json")


if __name__ == "__main__":
    main()
