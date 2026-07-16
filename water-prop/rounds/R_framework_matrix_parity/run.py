"""R-framework-matrix-parity sweep + diff harness (titan-4, 2026-05-22).

Runs the saturn_water_v0 mission_graph framework with the four matrix-carried
constraints OFF (baseline) and ON, plus sensitivity and reproduction sub-sweeps,
and writes compact per-cell closure summaries (NOT the 88 MB full walk dumps).

  results/canonical_sweep_post_encoding.json   constraints on/off canonical diff
  results/lifetime_sensitivity.json            H1: reactor_lifetime_years sweep
  results/specific_power_sensitivity.json      H2: reactor_specific_power sweep
  results/titan3_reproduction.json             H4: Isp-2000 + 50/60 t chunk band
  results/enceladus_r5_reproduction.json       H5: Cassini bus + 500 kWe parity

Run from project root:
  PYTHONPATH=water-prop/sims uv run python water-prop/rounds/R_framework_matrix_parity/run.py
"""

from __future__ import annotations

import dataclasses
import json
import sys
from pathlib import Path


def _ensure_import_path():
    here = Path(__file__).resolve()
    sims_dir = here.parents[2] / "sims"
    if str(sims_dir) not in sys.path:
        sys.path.insert(0, str(sims_dir))


_ensure_import_path()

from mission_graph.framework import SweepAxis, VehicleAxis, VehicleState, sweep  # noqa: E402
from mission_graph.missions.saturn_water_v0 import saturn_water_v0  # noqa: E402


SECONDS_PER_YEAR = 365.25 * 86_400
PROPELLANT_FRACTION = 0.80
HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
RESULTS.mkdir(exist_ok=True)


# -------------------------------------------------------------------- #
# Base state / params (mirrors saturn_water_canonical_sweep.py)
# -------------------------------------------------------------------- #

def _base_state() -> VehicleState:
    return VehicleState(
        mass_kg=100_000.0,
        propellant_kg=0.0,
        payload_kg=0.0,
        location="pre_launch",
        v_inf_km_s=0.0,
        time_elapsed_s=0.0,
        epoch_jd=None,
        power_available_kwe=30.0,
    )


def _scale_propellant(state: VehicleState, coords: dict) -> VehicleState:
    return dataclasses.replace(state, propellant_kg=PROPELLANT_FRACTION * state.mass_kg)


def _base_params(constraints_on: bool, **overrides) -> dict:
    p = {
        "chemical_isp_s": 340.0,
        "electric_isp_s": 3000.0,
        "electric_thrust_n": 5.0,
        "water_met_isp_s": 800.0,
        "chunk_mass_kg": 50_000.0,
        "multi_falcon_launch_count": 6,
        "launch_epoch_jd": 0.0,
        "existing_leo_depot": True,
    }
    if constraints_on:
        p.update({
            "enforce_mass_floor": True,
            "reactor_specific_power_w_per_kg": 2.4,  # KRUSTY-measured conservative
            "reactor_lifetime_years": 10.0,          # Kilopower design target
            "visviva_capture": True,
        })
    p.update(overrides)
    return p


VEHICLE_AXES = [
    VehicleAxis(name="vehicle_mass_kg",
                values=(50_000.0, 63_000.0, 100_000.0, 150_000.0, 200_000.0),
                state_field="mass_kg"),
    VehicleAxis(name="power_kwe",
                values=(1.0, 10.0, 11.0, 20.0, 30.0, 55.0),
                state_field="power_available_kwe"),
]
PARAM_AXES = [
    SweepAxis(name="chunk_mass_kg", values=(10_000.0, 25_000.0, 50_000.0, 100_000.0, 200_000.0)),
    SweepAxis(name="electric_thrust_n", values=(1.0, 2.5, 5.0, 10.0, 25.0)),
]


# -------------------------------------------------------------------- #
# Compact closure extraction
# -------------------------------------------------------------------- #

def _cell_summary(cell) -> dict:
    """Best LEO_depot delivery for a cell + closure flags. Compact (no paths)."""
    best_payload = 0.0
    best_rt_yr = None
    best_path = None
    for r in cell.results:
        if not r.is_feasible or r.leaf_state is None:
            continue
        if r.leaf_state.location != "LEO_depot":
            continue
        pay = r.leaf_state.payload_kg
        if pay > best_payload:
            best_payload = pay
            best_rt_yr = r.leaf_state.time_elapsed_s / SECONDS_PER_YEAR
            best_path = r.path_label
    return {
        "coords": dict(cell.coords),
        "best_delivered_t": round(best_payload / 1000.0, 2),
        "best_rt_yr": round(best_rt_yr, 2) if best_rt_yr is not None else None,
        "best_path": best_path,
        "skipped_reason": cell.skipped_reason,
    }


def _closing_cells(summaries, floor_t, rt_limit_yr):
    """Cells with a LEO_depot path delivering >= floor within rt_limit."""
    out = []
    for s in summaries:
        if s["best_rt_yr"] is None:
            continue
        if s["best_delivered_t"] >= floor_t and s["best_rt_yr"] <= rt_limit_yr:
            out.append(s)
    return out


def _run(base_state, base_params, vehicle_axes, param_axes, label):
    cells = sweep(saturn_water_v0, base_state, base_params,
                  param_axes=param_axes, vehicle_axes=vehicle_axes,
                  state_transform=_scale_propellant)
    summaries = [_cell_summary(c) for c in cells]
    print(f"  [{label}] {len(cells)} cells; "
          f"closing 30t/strict15yr={len(_closing_cells(summaries,30,15))}, "
          f"30t/waiver25yr={len(_closing_cells(summaries,30,25))}, "
          f"25t/waiver25yr={len(_closing_cells(summaries,25,25))}")
    return summaries


# -------------------------------------------------------------------- #
# Sub-sweeps
# -------------------------------------------------------------------- #

def canonical_on_off():
    print("Canonical 4-axis sweep (750 cells), constraints OFF vs ON:")
    off = _run(_base_state(), _base_params(False), VEHICLE_AXES, PARAM_AXES, "OFF")
    on = _run(_base_state(), _base_params(True), VEHICLE_AXES, PARAM_AXES, "ON")
    payload = {
        "description": "saturn_water_v0 canonical 4-axis sweep, constraints off vs on "
                       "(sp=2.4 W/kg, reactor_lifetime=10 yr, visviva capture, mass floor).",
        "axes": {"vehicle_mass_kg": [a.values for a in VEHICLE_AXES if a.name == 'vehicle_mass_kg'][0],
                 "power_kwe": [a.values for a in VEHICLE_AXES if a.name == 'power_kwe'][0],
                 "chunk_mass_kg": PARAM_AXES[0].values,
                 "electric_thrust_n": PARAM_AXES[1].values},
        "constraints_off": off,
        "constraints_on": on,
    }
    (RESULTS / "canonical_sweep_post_encoding.json").write_text(json.dumps(payload, indent=1))
    return off, on


def lifetime_sensitivity():
    print("H1 lifetime sensitivity (chunk 200 t band, sp 2.4):")
    out = {}
    for L in (5.0, 10.0, 15.0, float("inf")):
        params = _base_params(True, reactor_lifetime_years=L)
        summaries = _run(_base_state(), params, VEHICLE_AXES, PARAM_AXES, f"L={L}")
        out[str(L)] = {
            "closing_30t_waiver": len(_closing_cells(summaries, 30, 25)),
            "closing_30t_strict": len(_closing_cells(summaries, 30, 15)),
        }
    (RESULTS / "lifetime_sensitivity.json").write_text(json.dumps(out, indent=1))


def specific_power_sensitivity():
    print("H2 specific-power sensitivity (lifetime 10 yr):")
    out = {}
    for sp in (2.4, 5.0, 10.0):
        params = _base_params(True, reactor_specific_power_w_per_kg=sp)
        summaries = _run(_base_state(), params, VEHICLE_AXES, PARAM_AXES, f"sp={sp}")
        out[str(sp)] = {
            "closing_30t_waiver": len(_closing_cells(summaries, 30, 25)),
            "closing_30t_strict": len(_closing_cells(summaries, 30, 15)),
            "closing_cells_30t_strict": _closing_cells(summaries, 30, 15),
        }
    (RESULTS / "specific_power_sensitivity.json").write_text(json.dumps(out, indent=1))


def titan3_reproduction():
    """H4: titan-3 anchors — electric Isp 2000 (used as water_met_isp too),
    50/60 t chunk band, sp in {2.4, 10}, lifetime 10 yr, visviva capture +
    lunar-GA arrival available. Does the framework surface titan-3's 50-60 t
    closing band once anchored to titan-3's parameters?"""
    print("H4 titan-3 reproduction (Isp 2000, chunk 50/60 t, sp 2.4 & 10):")
    veh = [
        VehicleAxis(name="vehicle_mass_kg", values=(63_000.0, 100_000.0, 150_000.0),
                    state_field="mass_kg"),
        VehicleAxis(name="power_kwe", values=(20.0, 30.0), state_field="power_available_kwe"),
    ]
    par = [
        SweepAxis(name="chunk_mass_kg", values=(50_000.0, 60_000.0, 80_000.0)),
        SweepAxis(name="electric_thrust_n", values=(2.5, 5.0)),
    ]
    out = {"note": "titan-3 modeled INBOUND-ONLY (vehicle already at Saturn, chunk as sole "
                   "propellant, no Earth-launched propellant, no powerplant mass). The "
                   "framework models the FULL round-trip from Earth launch. They are not "
                   "cell-comparable; the framework delivers ~half for the same chunk."}
    for on in (False, True):
        for sp in (2.4, 10.0):
            params = _base_params(on, reactor_specific_power_w_per_kg=sp,
                                  water_met_isp_s=2000.0, electric_isp_s=2000.0)
            tag = f"sp{sp}_{'ON' if on else 'OFF'}"
            summaries = _run(_base_state(), params, veh, par, f"titan3 {tag}")
            out[tag] = {
                "closing_30t_strict": _closing_cells(summaries, 30, 15),
                "closing_30t_waiver": _closing_cells(summaries, 30, 25),
                "all": summaries,
            }
    (RESULTS / "titan3_reproduction.json").write_text(json.dumps(out, indent=1))


def enceladus_r5_reproduction():
    """H5: methodological parity check (500 kWe RETIRED per directive). Cassini
    bus (600 kg), high power axis incl. 500 kWe, sp 10, hybrid-aero arrival.
    Constraints ON. Confirms the framework's behavior at enceladus-r5 anchors;
    cells stay retired."""
    print("H5 enceladus-r5 reproduction (Cassini bus, power incl. 500 kWe, sp 10):")
    veh = [
        VehicleAxis(name="vehicle_mass_kg", values=(150_000.0, 200_000.0), state_field="mass_kg"),
        VehicleAxis(name="power_kwe", values=(200.0, 500.0), state_field="power_available_kwe"),
    ]
    par = [
        SweepAxis(name="chunk_mass_kg", values=(100_000.0, 200_000.0)),
        SweepAxis(name="electric_thrust_n", values=(5.0, 25.0)),
    ]
    out = {
        "note": "500 kWe RETIRED per project-owner directive 2026-05-19; methodological "
                "parity check only. Cassini 600 kg bus, sp 10 W/kg, Isp 2934 s. "
                "Constraints-OFF the framework delivers ~106 t at 200 t chunk / 500 kWe "
                "(enceladus-r5 claimed 91.5 t; ~16%, within tolerance, framework slightly "
                "generous because it omits enceladus-r5's shielding/PCU penalties). "
                "Constraints-ON the 500 kWe cell collapses: its ~110 t powerplant "
                "(50 t reactor + 55 t MARVL radiator + 5 t thrusters) cannot fit a 200 t "
                "vehicle's dry envelope.",
    }
    for on in (False, True):
        params = _base_params(on, reactor_specific_power_w_per_kg=10.0,
                              bus_mass_floor_kg=600.0, water_met_isp_s=2934.0,
                              electric_isp_s=2934.0)
        summaries = _run(_base_state(), params, veh, par, f"enceladus-r5 {'ON' if on else 'OFF'}")
        out["ON" if on else "OFF"] = {
            "closing_30t_strict": _closing_cells(summaries, 30, 15),
            "closing_30t_waiver": _closing_cells(summaries, 30, 25),
            "all": summaries,
        }
    (RESULTS / "enceladus_r5_reproduction.json").write_text(json.dumps(out, indent=1))


def main():
    canonical_on_off()
    lifetime_sensitivity()
    specific_power_sensitivity()
    titan3_reproduction()
    enceladus_r5_reproduction()
    print(f"\nWrote compact results to {RESULTS}")


if __name__ == "__main__":
    main()
