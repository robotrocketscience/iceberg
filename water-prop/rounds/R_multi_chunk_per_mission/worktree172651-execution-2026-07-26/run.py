"""R-multi-chunk-per-mission execution 2 — Tier-1 models + corridor re-run.

See STUDY.md. Writes results/multi_chunk_results.json.

Run from repo root:
  PYTHONPATH=water-prop/sims water-prop/.venv/bin/python \
      water-prop/rounds/R_multi_chunk_per_mission/worktree172651-execution-2026-07-26/run.py
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SIMS = HERE.parents[2] / "sims"
if str(SIMS) not in sys.path:
    sys.path.insert(0, str(SIMS))

from mission_graph.framework import VehicleState, walk  # noqa: E402
from mission_graph.missions.saturn_water_v2 import (  # noqa: E402
    saturn_water_v2, make_derived_mass_transform_v2)

GM = 3.7931e7 * 1e9
A0 = 100_000e3
V0 = math.sqrt(GM / A0)
SECONDS_PER_YEAR = 365.25 * 86400.0


# ------------------------------------------------------------------ #
# H-M1: Hill-regime re-rendezvous
# ------------------------------------------------------------------ #

def rendezvous(delta_a_m):
    """Coplanar orbit-raise + phasing to a chunk delta_a away in semi-major axis.

    Two-burn Hohmann-like raise: dv ~ (v/2a)*da each end; phasing time from the
    differential mean motion at separation delta_a (worst-case half-lap phase).
    """
    dv = (V0 / (2 * A0)) * delta_a_m * 2.0  # depart + arrive
    n0 = math.sqrt(GM / A0**3)
    dn = 1.5 * (n0 / A0) * delta_a_m       # differential mean motion
    t_phase_worst = math.pi / dn            # half-lap catch-up
    return dv, t_phase_worst


# ------------------------------------------------------------------ #
# H-M2: reliability ledger
# ------------------------------------------------------------------ #

def reliability_table():
    rows = {}
    for p in (0.961, 0.549):
        for n in (1, 2, 3, 5):
            rows[f"p{p}_N{n}"] = round(p ** n, 3)
    return rows


# ------------------------------------------------------------------ #
# H-M3: containment scaling
# ------------------------------------------------------------------ #

def containment_ratio(n):
    """Round-J ceiling ratio: N chunks of m/N vs one chunk of m: (1/N)^(-1/6)."""
    return round(n ** (1.0 / 6.0), 3)


# ------------------------------------------------------------------ #
# H-M4: despin ledger (Tier-1)
# ------------------------------------------------------------------ #

def despin_dv(chunk_kg=400_000.0, radius_m=4.6, spin_rpm=0.05, arm_m=4.6):
    """RCS impulse to despin a uniform sphere chunk via surface-mounted arm.

    L = (2/5) m r^2 omega; impulse = L / arm. Slow-rotator default 0.05 rpm
    (residence-class); the 0.28-rpm fast corner reported alongside.
    """
    omega = spin_rpm * 2 * math.pi / 60.0
    L = 0.4 * chunk_kg * radius_m**2 * omega
    impulse = L / arm_m           # N*s
    return impulse


# ------------------------------------------------------------------ #
# H-M5: corridor re-run with overheads
# ------------------------------------------------------------------ #

CORRIDOR = {
    "chemical_isp_s": 340.0, "electric_isp_s": 3000.0,
    "electric_thrust_n": 10.0, "water_met_isp_s": 800.0,
    "launch_epoch_jd": 0.0, "multi_falcon_launch_count": 6,
    "capture_arch": "harpoon", "plans_aerocapture": False,
    "reactor_specific_power_w_per_kg": 33.0, "electrolysis_isp_s": 900.0,
    "launcher_cap_multiplier": 16.0,
}


def corridor_cell(power, aggregate_kg, n_chunks, f=0.80):
    bp = dict(CORRIDOR, chunk_mass_kg=aggregate_kg, propellant_fraction=f,
              bus_mass_floor_kg=2000.0 + 350.0 * n_chunks)
    tr = make_derived_mass_transform_v2(bp)
    st = VehicleState(mass_kg=1.0, propellant_kg=0.0, payload_kg=0.0,
                      location="pre_launch", v_inf_km_s=0.0, time_elapsed_s=0.0,
                      epoch_jd=None, power_available_kwe=power)
    st = tr(st, {"power_kwe": power, "chunk_mass_kg": aggregate_kg,
                 "electric_thrust_n": 10.0})
    best = None
    for r in walk(saturn_water_v2, st, bp):
        if not (r.is_feasible and "electrolysis" in r.path_label
                and "aero" not in r.path_label
                and r.closure_verdicts.get("arrived_at_depot") == "close"):
            continue
        if best is None or r.leaf_state.payload_kg > best[0]:
            best = (r.leaf_state.payload_kg, r.leaf_state.time_elapsed_s)
    if best is None:
        return None
    ops_years = 0.25 * (n_chunks - 1)
    total_years = best[1] / SECONDS_PER_YEAR + ops_years
    return {"delivered_t": round(best[0] / 1e3, 1),
            "round_trip_yr_incl_ops": round(total_years, 1),
            "within_25yr_waiver": total_years <= 25.0}


def main():
    out = {}
    out["H-M1_rendezvous"] = {
        f"da_{int(da/1e3)}km": {"dv_m_s": round(rendezvous(da)[0], 2),
                                "t_phase_worst_days": round(rendezvous(da)[1] / 86400, 1)}
        for da in (10e3, 100e3, 1000e3)}
    out["H-M2_reliability"] = reliability_table()
    out["H-M3_containment_ceiling_gain"] = {f"N{n}": containment_ratio(n) for n in (2, 3, 5)}
    out["H-M4_despin"] = {
        "slow_0.05rpm_400t_impulse_Ns": round(despin_dv(), 0),
        "fast_0.28rpm_400t_impulse_Ns": round(despin_dv(spin_rpm=0.28), 0),
        "note": "impulse at 340 s Isp => propellant kg = impulse/(Isp*g0)",
    }
    out["H-M4_despin"]["slow_prop_kg_at_340s"] = round(
        out["H-M4_despin"]["slow_0.05rpm_400t_impulse_Ns"] / (340 * 9.81), 1)
    out["H-M4_despin"]["fast_prop_kg_at_340s"] = round(
        out["H-M4_despin"]["fast_0.28rpm_400t_impulse_Ns"] / (340 * 9.81), 1)

    grid = {}
    for aggregate, power in ((500_000.0, 150.0), (1_000_000.0, 200.0),
                             (2_000_000.0, 500.0)):
        n = math.ceil(aggregate / 400_000.0)
        base = corridor_cell(power, aggregate, 1)      # single-chunk-equivalent
        multi = corridor_cell(power, aggregate, n)     # overhead-charged
        grid[f"{int(aggregate/1e3)}t_{int(power)}kwe"] = {
            "n_chunks": n, "no_overhead": base, "with_overhead": multi}
        print(f"{int(aggregate/1e3)} t @ {int(power)} kWe (N={n}): "
              f"base={base} multi={multi}", flush=True)
    out["H-M5_corridor_with_overheads"] = grid

    (HERE / "results").mkdir(exist_ok=True)
    with open(HERE / "results" / "multi_chunk_results.json", "w") as f:
        json.dump(out, f, indent=1)
    for k in ("H-M1_rendezvous", "H-M2_reliability", "H-M3_containment_ceiling_gain",
              "H-M4_despin"):
        print(k, out[k])
    print("wrote results/multi_chunk_results.json")


if __name__ == "__main__":
    main()
