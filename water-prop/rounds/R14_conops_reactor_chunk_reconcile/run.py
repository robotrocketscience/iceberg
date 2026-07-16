"""Round 14 — Reconciling conops chunk-to-reactor scaling against the 13-yr
round-trip headline.

For each (delivered chunk target, reactor power, specific impulse, specific
power), find the achievable round trip via the standard trajectory + lunar
tour model. Flag conops cells (Kilopower 10 kWe -> 50 t, Fission Surface
Power 40 kWe -> 200 t, megawatt 500 kWe -> 750 t) and report the round
trip they actually deliver.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

from waterprop.constants import G0

# Trajectory constants (R12 baseline)
OUTBOUND_HOHMANN_YR = 6.09
SATURN_DWELL_YR = 1.0
INBOUND_HOHMANN_COAST_YR = 6.09
LUNAR_TOUR_PHASING_YR = 0.73
INBOUND_DV_KM_S = 4.47

# Vehicle
DRY_T = 5.0
DUTY = 0.5
ETA_BAG = 0.8  # conops design point η_c

YEAR_S = 365.25 * 86400.0


def cell_from_delivered(
    delivered_target_t: float,
    power_kwe: float,
    isp_s: float,
    eta_thruster: float,
    specific_power_w_per_kg: float,
    dv_km_s: float = INBOUND_DV_KM_S,
    eta_bag: float = ETA_BAG,
    dry_t: float = DRY_T,
    duty: float = DUTY,
) -> dict:
    """Iterate chunk grappled to hit delivered target. Then compute round trip."""
    v_e = isp_s * G0
    v_e_eff = v_e * eta_bag  # bag eff lowers effective exhaust velocity per conops
    reactor_t = power_kwe * 1000.0 / specific_power_w_per_kg / 1000.0
    # Solve for chunk_grappled G:
    #   m0 = G + dry + reactor
    #   prop = m0 * (1 - exp(-dv/v_e_eff))
    #   delivered = G - prop
    #   delivered = G - (G + dry + reactor) * pf
    #   delivered = G(1-pf) - (dry+reactor)*pf
    #   G = (delivered + (dry+reactor)*pf) / (1 - pf)
    pf = 1.0 - math.exp(-dv_km_s * 1000.0 / v_e_eff)
    if 1.0 - pf <= 0:
        return {
            "delivered_target_t": delivered_target_t,
            "feasible": False,
            "note": "specific impulse too low for delta-velocity",
        }
    chunk_grappled_t = (delivered_target_t + (dry_t + reactor_t) * pf) / (1.0 - pf)
    if chunk_grappled_t <= 0:
        return {
            "delivered_target_t": delivered_target_t,
            "feasible": False,
            "note": "negative chunk required",
        }
    m0_t = chunk_grappled_t + dry_t + reactor_t
    prop_t = m0_t * pf
    delivered_t = chunk_grappled_t - prop_t
    # Use thruster nominal v_e for thrust calc (bag eff affects propellant
    # consumption, not thrust directly):
    F_N = 2.0 * eta_thruster * power_kwe * 1000.0 / v_e
    m_avg_kg = (m0_t - prop_t / 2.0) * 1000.0
    if F_N <= 0 or m_avg_kg <= 0:
        return {
            "delivered_target_t": delivered_target_t,
            "chunk_grappled_t": chunk_grappled_t,
            "feasible": False,
        }
    accel = F_N / m_avg_kg
    cruise_braking_yr = (dv_km_s * 1000.0) / (accel * duty) / YEAR_S
    inbound_tof_yr = max(INBOUND_HOHMANN_COAST_YR, cruise_braking_yr) + LUNAR_TOUR_PHASING_YR
    round_trip_yr = OUTBOUND_HOHMANN_YR + SATURN_DWELL_YR + inbound_tof_yr
    return {
        "delivered_target_t": delivered_target_t,
        "chunk_grappled_t": chunk_grappled_t,
        "delivered_t": delivered_t,
        "power_kwe": power_kwe,
        "isp_s": isp_s,
        "eta_thruster": eta_thruster,
        "specific_power_w_per_kg": specific_power_w_per_kg,
        "reactor_t": reactor_t,
        "m0_t": m0_t,
        "prop_t": prop_t,
        "delivery_frac_chunk": delivered_t / chunk_grappled_t,
        "thrust_N": F_N,
        "cruise_braking_yr": cruise_braking_yr,
        "inbound_tof_yr": inbound_tof_yr,
        "round_trip_yr": round_trip_yr,
        "closes_14yr": round_trip_yr <= 14.0,
        "closes_18yr": round_trip_yr <= 18.0,
        "closes_25yr": round_trip_yr <= 25.0,
        "feasible": True,
    }


def main() -> dict:
    DELIVERED_TARGETS = [5.0, 14.0, 50.0, 100.0, 200.0, 500.0]
    POWERS = [10.0, 40.0, 100.0, 200.0, 500.0]
    THRUSTERS = [
        ("water_MET",                 700.0, 0.30),
        ("water_radio_frequency_ion", 2000.0, 0.65),
        ("water_dual_ion",            5000.0, 0.55),
    ]
    SP_LIST = [5.0, 10.0]

    cells = []
    for dt in DELIVERED_TARGETS:
        for p in POWERS:
            for thr_name, isp, eta in THRUSTERS:
                for sp in SP_LIST:
                    c = cell_from_delivered(dt, p, isp, eta, sp)
                    c["thruster"] = thr_name
                    cells.append(c)

    # Conops cells (specific claims)
    conops_claims = [
        {"reactor": "Kilopower", "power_kwe": 10.0, "delivered_t": 50.0},
        {"reactor": "Fission_Surface_Power", "power_kwe": 40.0, "delivered_t": 200.0},
        {"reactor": "megawatt_class", "power_kwe": 500.0, "delivered_t": 750.0},
    ]
    conops_reconciliation = []
    for claim in conops_claims:
        best_round_trip = {"thruster": None, "round_trip_yr": math.inf, "sp": None}
        for thr_name, isp, eta in THRUSTERS:
            for sp in SP_LIST:
                c = cell_from_delivered(
                    claim["delivered_t"], claim["power_kwe"], isp, eta, sp,
                )
                if c.get("feasible") and c["round_trip_yr"] < best_round_trip["round_trip_yr"]:
                    best_round_trip = {
                        "thruster": thr_name,
                        "isp_s": isp,
                        "sp_w_per_kg": sp,
                        "round_trip_yr": c["round_trip_yr"],
                        "chunk_grappled_t": c["chunk_grappled_t"],
                        "delivery_frac_chunk": c["delivery_frac_chunk"],
                        "cruise_braking_yr": c["cruise_braking_yr"],
                        "cell": c,
                    }
        conops_reconciliation.append({
            "conops_claim": claim,
            "actual_best_round_trip": best_round_trip,
        })

    # What chunk delivers AT 14-year ceiling, per power class?
    chunk_at_14yr = {}
    for p in POWERS:
        best_chunk = 0.0
        best_cell = None
        for c in cells:
            if (c.get("feasible") and c.get("closes_14yr")
                and c["power_kwe"] == p and c["specific_power_w_per_kg"] == 10.0):
                if c["delivered_target_t"] > best_chunk:
                    best_chunk = c["delivered_target_t"]
                    best_cell = c
        chunk_at_14yr[p] = best_cell

    # Hypothesis grading
    h14a = cell_from_delivered(50.0, 10.0, 700.0, 0.30, 10.0)
    h14b = cell_from_delivered(50.0, 10.0, 2000.0, 0.65, 10.0)
    h14c = cell_from_delivered(50.0, 40.0, 2000.0, 0.65, 10.0)
    h14d = cell_from_delivered(50.0, 10.0, 700.0, 0.30, 10.0)
    h14e = cell_from_delivered(200.0, 40.0, 2000.0, 0.65, 10.0)

    grading = {
        "H14a_10kwe_water_MET_50t_at_14yr": {
            "predicted": "delivered chunk ≤ 10 t at 14 yr",
            "actual_round_trip_yr": h14a.get("round_trip_yr"),
            "verdict": "to-be-judged",
        },
        "H14b_10kwe_water_RFI_50t_at_14yr": {
            "predicted": "delivered chunk ≤ 10 t at 14 yr",
            "actual_round_trip_yr": h14b.get("round_trip_yr"),
            "verdict": "to-be-judged",
        },
        "H14c_40kwe_water_RFI_200t_at_14yr": {
            "predicted": "round trip > 14 yr",
            "actual_round_trip_yr": h14c.get("round_trip_yr"),
            "verdict": "to-be-judged",
        },
        "H14d_kilopower_50t_round_trip": {
            "predicted": "≥ 35 yr",
            "actual_round_trip_yr": h14d.get("round_trip_yr"),
            "verdict": "to-be-judged",
        },
        "H14e_fsp_200t_round_trip": {
            "predicted": "≥ 30 yr",
            "actual_round_trip_yr": h14e.get("round_trip_yr"),
            "verdict": "to-be-judged",
        },
    }

    # Judge the predictions
    h14a_rt = h14a.get("round_trip_yr")
    grading["H14a_10kwe_water_MET_50t_at_14yr"]["verdict"] = (
        "held" if h14a_rt and h14a_rt > 14.0 else "falsified"
    )
    h14b_rt = h14b.get("round_trip_yr")
    grading["H14b_10kwe_water_RFI_50t_at_14yr"]["verdict"] = (
        "held" if h14b_rt and h14b_rt > 14.0 else "falsified"
    )
    h14c_rt = h14c.get("round_trip_yr")
    grading["H14c_40kwe_water_RFI_200t_at_14yr"]["verdict"] = (
        "held" if h14c_rt and h14c_rt > 14.0 else "falsified"
    )
    h14d_rt = h14d.get("round_trip_yr")
    grading["H14d_kilopower_50t_round_trip"]["verdict"] = (
        "held" if h14d_rt and h14d_rt >= 35.0
        else "partial" if h14d_rt and h14d_rt >= 25.0 else "falsified"
    )
    h14e_rt = h14e.get("round_trip_yr")
    grading["H14e_fsp_200t_round_trip"]["verdict"] = (
        "held" if h14e_rt and h14e_rt >= 30.0
        else "partial" if h14e_rt and h14e_rt >= 25.0 else "falsified"
    )

    results = {
        "inputs": {
            "INBOUND_DV_KM_S": INBOUND_DV_KM_S,
            "DRY_T": DRY_T,
            "ETA_BAG": ETA_BAG,
            "DUTY": DUTY,
            "DELIVERED_TARGETS": DELIVERED_TARGETS,
            "POWERS": POWERS,
            "THRUSTERS": [{"name": n, "isp_s": i, "eta": e} for (n, i, e) in THRUSTERS],
            "SP_LIST": SP_LIST,
        },
        "cells": cells,
        "conops_reconciliation": conops_reconciliation,
        "chunk_at_14yr_by_power": chunk_at_14yr,
        "hypothesis_grading": grading,
    }

    out_dir = Path(__file__).parent / "results"
    out_dir.mkdir(exist_ok=True)
    with (out_dir / "reconciliation.json").open("w") as f:
        json.dump(results, f, indent=2)

    # Console
    print("=" * 96)
    print("R14 — Reconciling conops reactor → chunk-mass scaling")
    print("=" * 96)
    print()
    print(f"CONOPS CLAIMS vs ACTUAL BEST ROUND TRIP:")
    for r in conops_reconciliation:
        claim = r["conops_claim"]
        a = r["actual_best_round_trip"]
        if a["thruster"]:
            print(f"  Conops: {claim['reactor']:<25} {claim['power_kwe']:>5.0f} kWe -> "
                  f"{claim['delivered_t']:>5.0f} t delivered")
            print(f"    Actual best: {a['thruster']} at {a['isp_s']:.0f} s, "
                  f"sp_pwr {a['sp_w_per_kg']:.0f} W/kg -> {a['round_trip_yr']:.2f} yr round trip")
            print(f"    Chunk grappled: {a['chunk_grappled_t']:.0f} t  "
                  f"Delivery frac: {a['delivery_frac_chunk']*100:.1f}%  "
                  f"Braking: {a['cruise_braking_yr']:.2f} yr")
        else:
            print(f"  Conops: {claim['reactor']} {claim['power_kwe']} kWe -> "
                  f"{claim['delivered_t']} t: no feasible thruster found")
        print()

    print(f"CHUNK DELIVERED AT 14-YEAR CEILING (max, per reactor power, 10 W/kg):")
    print(f"  {'Power':>6} {'Reactor_class':<25} {'Max_delivered':>14} {'Thruster':>30}")
    for p, c in chunk_at_14yr.items():
        cls = (
            "Kilopower" if p == 10.0
            else "Fission Surface Power" if p == 40.0
            else "stretch (no program)" if p == 100.0
            else "sub-megawatt (paper)" if p == 200.0
            else "megawatt (paper)"
        )
        if c:
            print(f"  {p:>4.0f} kWe  {cls:<25} {c['delivered_t']:>12.1f} t  {c['thruster']:>30}")
        else:
            print(f"  {p:>4.0f} kWe  {cls:<25} {'NONE':>12}")
    print()
    print(f"Hypothesis grading:")
    for h, g in grading.items():
        v = g.get('verdict')
        rt = g.get('actual_round_trip_yr')
        rt_s = f"{rt:.2f} yr" if rt else "n/a"
        print(f"  {h:<55} {v}  (round_trip = {rt_s})")
    print()
    print(f"Result JSON: {out_dir / 'reconciliation.json'}")
    return results


if __name__ == "__main__":
    main()
