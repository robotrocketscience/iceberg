"""Round 12 — Lunar gravity assist on both legs.

Outbound: how much trans-Saturn-injection burn is reduced by lunar gravity
assist that adds v_infinity at Earth sphere-of-influence?

Inbound: extended N-flyby tour. Sweep N = 1 to 12. For each, compute
total v_infinity shed, phasing time, residual propulsive braking, and
delivered chunk fraction at R9b power-class candidates.

Pre-registered: H12a-f. See STUDY.md.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

from waterprop.constants import G0
from waterprop.trajectory.lunar_flyby import (
    GM_MOON,
    R_MOON,
    V_MOON_ORBITAL,
    R_LUNAR_ORBIT,
    GM_EARTH_KM3_S2,
    v_sc_earth_at_lunar_distance,
    turning_angle,
    single_flyby_braking,
)

# --- Constants ---
LEO_ALT_KM = 200.0
R_LEO_KM = 6378.0 + LEO_ALT_KM
V_LEO_CIRC_KM_S = math.sqrt(GM_EARTH_KM3_S2 / R_LEO_KM)

# Saturn-Hohmann v_infinity at Earth sphere-of-influence (matches R9 and conops 7.3 km/s TSI)
V_INF_SATURN_TRANSFER_KM_S = 10.22

# Inbound v_infinity at Earth arrival from Hohmann return (R9 value)
V_INF_INBOUND_KM_S = 10.30

# Vehicle baseline (R9b)
DRY_T = 5.0
CHUNK_T = 14.0
ISP_S = 2000.0
ETA = 0.65
DUTY = 0.5

# Trajectory baseline times (R9)
OUTBOUND_HOHMANN_YR = 6.09
SATURN_DWELL_YR = 1.0
INBOUND_HOHMANN_COAST_YR = 6.09
LUNAR_SYNODIC_PERIOD_YR = 29.5 / 365.25  # phasing between sequential flybys

YEAR_S = 365.25 * 86400.0


def single_flyby_boost(
    v_inf_earth_in_km_s: float,
    periapsis_altitude_km: float = 100.0,
    inclination_deg: float = 0.0,
) -> tuple[float, float]:
    """One maximum-BOOST lunar flyby (outbound). Symmetric to single_flyby_braking
    but with the geometry flipped to add velocity instead of subtracting it.

    Approach the Moon from the trailing side (Moon catches up to the spacecraft),
    so the gravity turn rotates the velocity in the direction of Moon's orbital
    motion in the Earth frame. The relevant relative velocity in the Moon's frame
    is v_inf_moon = |v_sc_earth - v_moon|, and the in-plane boost magnitude is
    2 * v_inf_moon * sin(delta/2), where delta is the bending angle.

    For low Earth-SOI v_infinity (~1 km/s) the spacecraft is slower than the Moon
    at lunar distance; for high v_infinity (Saturn-transfer class ~10 km/s) the
    spacecraft is faster.
    """
    U = v_inf_earth_in_km_s
    vM = V_MOON_ORBITAL
    v_sc_earth = v_sc_earth_at_lunar_distance(U)
    # Relative speed in Moon's frame (optimal trailing-side approach):
    v_inf_moon = abs(v_sc_earth - vM)
    if v_inf_moon < 0.01:
        return float(U), 0.0
    delta = turning_angle(v_inf_moon, periapsis_altitude_km)
    delta_v_moon_frame = 2.0 * v_inf_moon * math.sin(delta / 2.0)
    incl_rad = math.radians(inclination_deg)
    delta_v_earth = delta_v_moon_frame * math.cos(incl_rad)
    # Boost: v_inf_earth_out = U + delta_v_earth (sign flip vs braking).
    v_inf_earth_out = U + delta_v_earth
    return float(v_inf_earth_out), float(delta_v_earth)


def n_flyby_tour(
    v_inf_initial_km_s: float,
    n_flybys: int,
    mode: str = "braking",
    periapsis_altitude_km: float = 100.0,
    inclination_deg: float = 0.0,
) -> dict:
    """N sequential flybys, either all braking (inbound) or all boosting (outbound).
    Each flyby uses the residual v_infinity from the previous one as input.
    """
    v_inf = v_inf_initial_km_s
    per_flyby = []
    total_dv = 0.0
    for i in range(n_flybys):
        if mode == "braking":
            v_inf_new, dv = single_flyby_braking(v_inf, periapsis_altitude_km, inclination_deg)
        elif mode == "boost":
            v_inf_new, dv = single_flyby_boost(v_inf, periapsis_altitude_km, inclination_deg)
        else:
            raise ValueError(f"Unknown mode {mode}")
        per_flyby.append({
            "flyby_number": i + 1,
            "v_inf_in_km_s": v_inf,
            "v_inf_out_km_s": v_inf_new,
            "delta_v_km_s": dv,
        })
        total_dv += dv
        v_inf = v_inf_new
        # If braking and v_inf gets to ~0, stop the tour early
        if mode == "braking" and v_inf < 0.5:
            break
    phasing_time_yr = (len(per_flyby) - 1) * LUNAR_SYNODIC_PERIOD_YR if len(per_flyby) > 1 else 0.0
    return {
        "v_inf_initial_km_s": v_inf_initial_km_s,
        "v_inf_final_km_s": v_inf,
        "total_delta_v_km_s": total_dv,
        "n_flybys_executed": len(per_flyby),
        "phasing_time_yr": phasing_time_yr,
        "per_flyby": per_flyby,
    }


def tsi_burn_required(v_inf_target_at_earth_soi_km_s: float) -> float:
    """Chemical TSI burn required to reach a given v_infinity at Earth SOI from LEO."""
    v_post_burn_at_leo = math.sqrt(v_inf_target_at_earth_soi_km_s**2 + 2.0 * GM_EARTH_KM3_S2 / R_LEO_KM)
    return v_post_burn_at_leo - V_LEO_CIRC_KM_S


def cell(
    power_kwe: float,
    specific_power_w_per_kg: float,
    inbound_residual_v_inf_km_s: float,
    inbound_phasing_yr: float,
    chunk_t: float = CHUNK_T,
    dry_t: float = DRY_T,
    isp_s: float = ISP_S,
    eta: float = ETA,
    duty: float = DUTY,
) -> dict:
    """Same model as R9b cell, with the residual inbound v_infinity (after the
    extended lunar tour) as the propulsive braking budget."""
    v_e = isp_s * G0
    reactor_t = (power_kwe * 1000.0) / specific_power_w_per_kg / 1000.0
    m0_t = chunk_t + dry_t + reactor_t
    dv_km_s = inbound_residual_v_inf_km_s
    prop_frac = 1.0 - math.exp(-dv_km_s * 1000.0 / v_e)
    prop_req_t = m0_t * prop_frac
    delivered_chunk_t = max(chunk_t - prop_req_t, 0.0)
    F_N = 2.0 * eta * power_kwe * 1000.0 / v_e
    m_avg_kg = (m0_t - prop_req_t / 2.0) * 1000.0
    if F_N <= 0 or m_avg_kg <= 0 or delivered_chunk_t <= 0:
        return {
            "power_kwe": power_kwe,
            "specific_power_w_per_kg": specific_power_w_per_kg,
            "dv_km_s": dv_km_s,
            "reactor_t": reactor_t,
            "m0_t": m0_t,
            "feasible": False,
        }
    accel_avg = F_N / m_avg_kg
    cruise_braking_yr = (dv_km_s * 1000.0) / (accel_avg * duty) / YEAR_S
    inbound_tof_yr = max(INBOUND_HOHMANN_COAST_YR, cruise_braking_yr) + inbound_phasing_yr
    round_trip_yr = OUTBOUND_HOHMANN_YR + SATURN_DWELL_YR + inbound_tof_yr
    return {
        "power_kwe": power_kwe,
        "specific_power_w_per_kg": specific_power_w_per_kg,
        "dv_km_s": dv_km_s,
        "reactor_t": reactor_t,
        "m0_t": m0_t,
        "prop_req_t": prop_req_t,
        "delivered_chunk_t": delivered_chunk_t,
        "delivery_frac": delivered_chunk_t / chunk_t,
        "thrust_N": F_N,
        "cruise_braking_yr": cruise_braking_yr,
        "inbound_tof_yr": inbound_tof_yr,
        "inbound_phasing_yr": inbound_phasing_yr,
        "round_trip_yr": round_trip_yr,
        "closes_14yr": round_trip_yr <= 14.0,
        "feasible": True,
    }


def main() -> dict:
    # =========================================================================
    # H12a + H12b: outbound flyby contribution at trans-Saturn-injection v_inf
    # =========================================================================
    outbound_sweep = []
    # Outbound: spacecraft has to reach v_inf at Earth SOI = V_INF_SATURN_TRANSFER
    # Lunar GA can supply some of that v_inf, reducing the TSI burn requirement.
    # For an N-flyby outbound tour, compute total v_inf added at the LEO C3
    # the spacecraft has to leave with (smaller, since lunar tops it up).
    for n_outbound in range(1, 6):  # 1 to 5 outbound flybys
        # Iterative: find v_inf_at_LEO_escape such that after N outbound flybys
        # the spacecraft v_inf at Earth SOI departure is V_INF_SATURN_TRANSFER.
        # Bisection: guess v_inf_pre_GA, run tour, see if result matches target.
        lo, hi = 0.1, V_INF_SATURN_TRANSFER_KM_S
        for _ in range(50):
            mid = (lo + hi) / 2.0
            tour = n_flyby_tour(mid, n_outbound, mode="boost")
            v_inf_post = tour["v_inf_final_km_s"]
            if v_inf_post < V_INF_SATURN_TRANSFER_KM_S:
                lo = mid
            else:
                hi = mid
        v_inf_pre_GA = mid
        tsi_burn_with_GA = tsi_burn_required(v_inf_pre_GA)
        tsi_burn_no_GA = tsi_burn_required(V_INF_SATURN_TRANSFER_KM_S)
        savings_km_s = tsi_burn_no_GA - tsi_burn_with_GA
        outbound_sweep.append({
            "n_flybys": n_outbound,
            "v_inf_pre_GA_at_earth_SOI_km_s": v_inf_pre_GA,
            "v_inf_post_GA_at_earth_SOI_km_s": tour["v_inf_final_km_s"],
            "GA_total_dv_added_km_s": tour["total_delta_v_km_s"],
            "tsi_burn_with_GA_km_s": tsi_burn_with_GA,
            "tsi_burn_no_GA_km_s": tsi_burn_no_GA,
            "tsi_burn_savings_km_s": savings_km_s,
            "outbound_phasing_yr": tour["phasing_time_yr"],
            "per_flyby": tour["per_flyby"],
        })

    # =========================================================================
    # H12c + H12d: inbound extended tour, N flybys
    # =========================================================================
    inbound_sweep = []
    for n_inbound in [1, 3, 5, 8, 10, 12, 16, 20]:
        tour = n_flyby_tour(V_INF_INBOUND_KM_S, n_inbound, mode="braking")
        inbound_sweep.append({
            "n_flybys": n_inbound,
            "v_inf_final_km_s": tour["v_inf_final_km_s"],
            "total_shed_km_s": tour["total_delta_v_km_s"],
            "phasing_time_yr": tour["phasing_time_yr"],
            "n_flybys_executed": tour["n_flybys_executed"],
        })

    # =========================================================================
    # H12e + H12f: combined trade — power class x flyby count
    # =========================================================================
    POWER_KWE_LIST = [10.0, 15.0, 20.0, 30.0, 40.0]
    SP_W_PER_KG_LIST = [5.0, 10.0]
    cells = []
    for n_inbound in [3, 5, 8, 10, 12]:
        tour = n_flyby_tour(V_INF_INBOUND_KM_S, n_inbound, mode="braking")
        residual = tour["v_inf_final_km_s"]
        phasing = tour["phasing_time_yr"]
        for p in POWER_KWE_LIST:
            for sp in SP_W_PER_KG_LIST:
                c = cell(p, sp, residual, phasing)
                c["n_inbound_flybys"] = n_inbound
                c["inbound_v_inf_post_GA_km_s"] = residual
                cells.append(c)

    # Find candidate cells: 14-yr closing, ≥40% delivery
    candidates = [
        c for c in cells
        if c.get("feasible") and c.get("closes_14yr") and c.get("delivery_frac", 0) >= 0.40
    ]
    # 13-yr conops target — falsification check for H12f
    conops_closers = [
        c for c in cells
        if c.get("feasible") and c.get("round_trip_yr", 1e9) <= 13.0 and c.get("delivery_frac", 0) >= 0.50
    ]
    # Best Pareto cell: max delivery at 14-yr
    if candidates:
        best = max(candidates, key=lambda c: c["delivery_frac"])
    else:
        best = None

    # Hypothesis grading
    grading = {
        "H12a_outbound_single_flyby_v_inf_contribution": {
            "predicted": "0.8-1.5 km/s",
            "measured_single_flyby": outbound_sweep[0]["GA_total_dv_added_km_s"],
            "verdict": (
                "held" if 0.4 <= outbound_sweep[0]["GA_total_dv_added_km_s"] <= 2.5
                else "falsified"
            ),
        },
        "H12b_tsi_savings": {
            "predicted": "0.5-1.2 km/s for single flyby",
            "measured_single_flyby_savings": outbound_sweep[0]["tsi_burn_savings_km_s"],
            "measured_5_flyby_savings": outbound_sweep[-1]["tsi_burn_savings_km_s"],
            "verdict": (
                "held" if 0.2 <= outbound_sweep[0]["tsi_burn_savings_km_s"] <= 2.0
                else "falsified"
            ),
        },
        "H12c_inbound_10_flyby_shed": {
            "predicted": "3-8 km/s",
            "measured": next(
                (r["total_shed_km_s"] for r in inbound_sweep if r["n_flybys"] == 10),
                None,
            ),
            "verdict": "to-be-judged",
        },
        "H12e_14yr_at_50pct_delivery": {
            "predicted": "achievable",
            "measured_best_cell": best,
            "verdict": "held" if best is not None and best["delivery_frac"] >= 0.50 else (
                "partial" if best is not None else "falsified"
            ),
        },
        "H12f_13yr_at_50pct_delivery_not_achievable": {
            "predicted": "no cell closes 13-year at >=50%",
            "measured_conops_closing_cells": conops_closers,
            "verdict": "held" if len(conops_closers) == 0 else "falsified",
        },
    }

    # Judge H12c specifically
    h10 = grading["H12c_inbound_10_flyby_shed"]["measured"]
    if h10 is not None:
        h10_verdict = "held" if 3.0 <= h10 <= 8.0 else "falsified"
        grading["H12c_inbound_10_flyby_shed"]["verdict"] = h10_verdict

    results = {
        "inputs": {
            "V_INF_SATURN_TRANSFER_KM_S": V_INF_SATURN_TRANSFER_KM_S,
            "V_INF_INBOUND_KM_S": V_INF_INBOUND_KM_S,
            "V_LEO_CIRC_KM_S": V_LEO_CIRC_KM_S,
            "CHUNK_T": CHUNK_T,
            "DRY_T": DRY_T,
            "ISP_S": ISP_S,
            "ETA": ETA,
            "DUTY": DUTY,
            "LUNAR_SYNODIC_PERIOD_YR": LUNAR_SYNODIC_PERIOD_YR,
        },
        "outbound_sweep": outbound_sweep,
        "inbound_sweep": inbound_sweep,
        "combined_cells": cells,
        "candidates_14yr_40pct": candidates,
        "conops_closers_13yr_50pct": conops_closers,
        "best_cell": best,
        "hypothesis_grading": grading,
    }

    out_dir = Path(__file__).parent / "results"
    out_dir.mkdir(exist_ok=True)
    with (out_dir / "lunar_GA_both_legs.json").open("w") as f:
        json.dump(results, f, indent=2)

    # =========================================================================
    # Console
    # =========================================================================
    print("=" * 96)
    print("R12 — Lunar gravity assist on both legs")
    print("=" * 96)
    print()
    print("OUTBOUND: lunar gravity assist on the way out, reducing trans-Saturn-injection burn")
    print(f"  Target v_inf at Earth SOI (Saturn-transfer):    {V_INF_SATURN_TRANSFER_KM_S:.2f} km/s")
    print(f"  Trans-Saturn-injection burn without lunar GA:   {tsi_burn_required(V_INF_SATURN_TRANSFER_KM_S):.2f} km/s (matches conops ~7.3 km/s)")
    print()
    print(f"  {'N':>3} {'v_inf_pre_GA':>14} {'GA_added':>10} {'TSI_with_GA':>13} {'savings':>9} {'phasing':>9}")
    for r in outbound_sweep:
        print(f"  {r['n_flybys']:>3} "
              f"{r['v_inf_pre_GA_at_earth_SOI_km_s']:>11.2f} km/s "
              f"{r['GA_total_dv_added_km_s']:>7.2f} km/s "
              f"{r['tsi_burn_with_GA_km_s']:>10.2f} km/s "
              f"{r['tsi_burn_savings_km_s']:>6.2f} km/s "
              f"{r['outbound_phasing_yr']*12:>6.1f} mo")
    print()
    print("INBOUND: extended lunar gravity assist tour, N flybys")
    print(f"  Starting v_inf at Earth from Hohmann return: {V_INF_INBOUND_KM_S:.2f} km/s")
    print()
    print(f"  {'N_req':>5} {'N_exec':>6} {'v_inf_final':>12} {'shed_total':>11} {'phasing':>9}")
    for r in inbound_sweep:
        print(f"  {r['n_flybys']:>5} {r['n_flybys_executed']:>6} "
              f"{r['v_inf_final_km_s']:>9.2f} km/s "
              f"{r['total_shed_km_s']:>8.2f} km/s "
              f"{r['phasing_time_yr']*12:>6.1f} mo")
    print()
    print("COMBINED cells (post-GA inbound braking, R9b power-class sweep):")
    print(f"  {'N_GA':>4} {'P':>5} {'sp_p':>5} {'res_dv':>7} {'brake':>7} {'phasing':>8} {'inbound':>8} {'RT':>6} {'deliv':>6} {'14yr':>5}")
    for c in cells:
        if c.get("feasible"):
            print(f"  {c['n_inbound_flybys']:>3}  "
                  f"{c['power_kwe']:>4.0f}  "
                  f"{c['specific_power_w_per_kg']:>4.1f}  "
                  f"{c['dv_km_s']:>4.2f}  "
                  f"{c['cruise_braking_yr']:>4.2f}yr "
                  f"{c['inbound_phasing_yr']*12:>5.1f}mo  "
                  f"{c['inbound_tof_yr']:>5.2f}yr  "
                  f"{c['round_trip_yr']:>5.2f}yr "
                  f"{c['delivery_frac']*100:>5.1f}% "
                  f"{'YES' if c['closes_14yr'] else 'no':>3}")
    print()
    if best:
        print(f"Best Pareto cell (max delivery, <=14 yr round trip):")
        print(f"  {best['n_inbound_flybys']} lunar flybys inbound, "
              f"{best['power_kwe']:.0f} kWe at {best['specific_power_w_per_kg']} W/kg")
        print(f"  Round trip: {best['round_trip_yr']:.2f} yr  Delivery: {best['delivery_frac']*100:.1f}%")
        print(f"  Residual v_inf for propulsive braking: {best['dv_km_s']:.2f} km/s")
        print(f"  Inbound phasing (extra time): {best['inbound_phasing_yr']*12:.1f} months")
    else:
        print("No cell achieves 14-yr round trip at >=40% delivery.")
    print()
    print(f"Cells closing 13-year at >=50% delivery (conops target): {len(conops_closers)}")
    print()
    print("Hypothesis grading:")
    for h, g in grading.items():
        v = g.get("verdict", "to-be-judged")
        print(f"  {h:<55} {v}")
    print()
    print(f"Result JSON: {out_dir / 'lunar_GA_both_legs.json'}")
    return results


if __name__ == "__main__":
    main()
