"""Single-path mass-ledger walks (PROTOCOL lesson 25 compliance, latest+29b).

Lesson 25 (ratified 2026-07-26): any round producing a NEW closure surface must
ship a single-path mass-ledger walk of at least one closing path. This script
walks (a) the Arm-A S5 closing cell of R-closure-boundary-inversion and (b) the
v2 electrolysis-NTP 900-s corridor cell of R-saturn-water-v2-electrolysis-
departure, printing launch wet mass through every phase to delivered payload.

Run from repo root:
  PYTHONPATH=water-prop/sims water-prop/.venv/bin/python \
      water-prop/rounds/R_closure_boundary_inversion/ledger_walk.py

Writes results/ledger_walks.txt (small, committed).
"""

from __future__ import annotations

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


def best_closing_path(mission, transform, coords, params):
    state = VehicleState(
        mass_kg=1.0, propellant_kg=0.0, payload_kg=0.0, location="pre_launch",
        v_inf_km_s=0.0, time_elapsed_s=0.0, epoch_jd=None,
        power_available_kwe=coords["power_kwe"])
    state = transform(state, coords)
    results = walk(mission, state, params)
    closing = [r for r in results if r.is_feasible
               and r.closure_verdicts.get("arrived_at_depot") == "close"]
    if not closing:
        return state, None
    return state, max(closing, key=lambda r: r.leaf_state.payload_kg)


def option_ids_from_label(path_label):
    return [seg.strip().split(".")[1] for seg in path_label.split("->")]


def ledger(mission, start_state, path_label, params, out_lines):
    options_by_phase = {ph.phase_id: {o.option_id: o for o in ph.options}
                        for ph in mission.phase_sequence}
    ids = option_ids_from_label(path_label)
    state = start_state
    out_lines.append(f"  {'phase.option':55s} {'mass_t':>8s} {'prop_t':>8s} "
                     f"{'payload_t':>9s} {'yrs':>6s}")
    out_lines.append(f"  {'LAUNCH (derived wet)':55s} {state.mass_kg/1e3:8.1f} "
                     f"{state.propellant_kg/1e3:8.1f} {state.payload_kg/1e3:9.1f} "
                     f"{state.time_elapsed_s/3.156e7:6.2f}")
    for ph, oid in zip(mission.phase_sequence, ids):
        opt = options_by_phase[ph.phase_id][oid]
        ok, why = opt.precondition(state, params)
        assert ok, f"{ph.phase_id}.{oid}: {why}"
        state = opt.executor(state, params)
        out_lines.append(f"  {ph.phase_id + '.' + oid:55s} {state.mass_kg/1e3:8.1f} "
                         f"{state.propellant_kg/1e3:8.1f} {state.payload_kg/1e3:9.1f} "
                         f"{state.time_elapsed_s/3.156e7:6.2f}")
    return state


def main():
    out_lines = []

    # (a) Arm-A S5 closing cell: 100 kWe / 200 t chunk / 1 N,
    # launcher x5 + 33 W/kg + water-MET 2,000 s.
    params_a = {
        "chemical_isp_s": 340.0, "electric_isp_s": 3000.0,
        "electric_thrust_n": 1.0, "water_met_isp_s": 2000.0,
        "chunk_mass_kg": 200_000.0, "multi_falcon_launch_count": 6,
        "launch_epoch_jd": 0.0, "launcher_cap_multiplier": 5.0,
        "reactor_specific_power_w_per_kg": 33.0,
    }
    coords_a = {"power_kwe": 100.0, "chunk_mass_kg": 200_000.0,
                "electric_thrust_n": 1.0}
    start, best = best_closing_path(
        saturn_water_v1, make_derived_mass_transform(params_a), coords_a, params_a)
    out_lines.append("(a) Arm-A S5 cell — saturn_water_v1, 100 kWe / 200 t / "
                     "1 N; x5 launch, 33 W/kg, 2,000 s "
                     "[NOTE latest+29c: Arm A re-labeled impulsive-regime bound "
                     "per R-departure-anchor-resolution]")
    assert best is not None, "S5 cell no longer closes — ledger invalid"
    out_lines.append(f"  path: {best.path_label}")
    final = ledger(saturn_water_v1, start, best.path_label, params_a, out_lines)
    out_lines.append(f"  DELIVERED: {final.payload_kg/1e3:.2f} t at {final.location}; "
                     f"round trip {final.time_elapsed_s/3.156e7:.1f} yr")
    out_lines.append("")

    # (b) v2 electrolysis-NTP 900-s corridor cell: 200 kWe / 1,000 t harvest /
    # 10 N; x16 launch, 33 W/kg, harpoon, no TPS.
    params_b = {
        "chemical_isp_s": 340.0, "electric_isp_s": 3000.0,
        "electric_thrust_n": 10.0, "water_met_isp_s": 800.0,
        "chunk_mass_kg": 1_000_000.0, "multi_falcon_launch_count": 6,
        "launch_epoch_jd": 0.0, "launcher_cap_multiplier": 16.0,
        "reactor_specific_power_w_per_kg": 33.0, "capture_arch": "harpoon",
        "plans_aerocapture": False, "electrolysis_isp_s": 900.0,
    }
    coords_b = {"power_kwe": 200.0, "chunk_mass_kg": 1_000_000.0,
                "electric_thrust_n": 10.0}
    start, best = best_closing_path(
        saturn_water_v2, make_derived_mass_transform_v2(params_b), coords_b, params_b)
    out_lines.append("(b) v2 electrolysis-NTP corridor cell — saturn_water_v2, "
                     "200 kWe / 1,000 t harvest / 10 N; x16 launch, 33 W/kg, "
                     "harpoon, path-conditional TPS, stage Isp 900 s")
    assert best is not None, "v2 corridor cell no longer closes — ledger invalid"
    out_lines.append(f"  path: {best.path_label}")
    final = ledger(saturn_water_v2, start, best.path_label, params_b, out_lines)
    out_lines.append(f"  DELIVERED: {final.payload_kg/1e3:.2f} t at {final.location}; "
                     f"round trip {final.time_elapsed_s/3.156e7:.1f} yr")

    text = "\n".join(out_lines)
    print(text)
    (HERE / "results").mkdir(exist_ok=True)
    (HERE / "results" / "ledger_walks.txt").write_text(text + "\n")
    print("\nwrote results/ledger_walks.txt")


if __name__ == "__main__":
    main()
