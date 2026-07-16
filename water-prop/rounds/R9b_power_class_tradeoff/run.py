"""Round 9b — Power-class trade for chunk-fed inbound braking.

Sweeps reactor power and reactor specific power. For each (P, specific_power)
cell, computes inbound braking cruise time + delivered chunk fraction +
total round trip. Searches for cells that close 13-yr round trip with >= 50%
delivery (pre-registered H9b-e prediction: none exist).
"""

from __future__ import annotations

import json
import math
from pathlib import Path

from waterprop.constants import G0

# --- Cruise constants from R9 ---
OUTBOUND_HOHMANN_YR = 6.09
SATURN_DWELL_YR = 1.0
INBOUND_HOHMANN_COAST_YR = 6.09  # Hohmann inbound free-flight time

# --- Vehicle / propulsion constants ---
DRY_T = 5.0
CHUNK_T = 14.0
ISP_S = 2000.0  # water RF ion (Pale Blue class)
ETA = 0.65
DUTY = 0.5

# --- Sweep grid ---
POWER_KWE_LIST = [5.0, 10.0, 20.0, 40.0, 80.0, 160.0]
SPECIFIC_POWER_W_PER_KG_LIST = [2.5, 5.0, 10.0]
DV_BUDGETS_KM_S = {
    "post_3flyby_tour_R9": 8.87,   # R9 result
    "R10_case_B_no_GA": 5.94,      # comparison
}


def cell(
    power_kwe: float,
    specific_power_w_per_kg: float,
    dv_km_s: float,
    chunk_t: float = CHUNK_T,
    dry_t: float = DRY_T,
    isp_s: float = ISP_S,
    eta: float = ETA,
    duty: float = DUTY,
) -> dict:
    v_e = isp_s * G0
    reactor_t = (power_kwe * 1000.0) / specific_power_w_per_kg / 1000.0
    m0_t = chunk_t + dry_t + reactor_t
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
            "note": "non-positive thrust, mass, or delivery",
        }
    accel_avg = F_N / m_avg_kg
    cruise_braking_s = (dv_km_s * 1000.0) / (accel_avg * duty)
    cruise_braking_yr = cruise_braking_s / (365.25 * 86400.0)
    # Realistic interpretation: braking happens DURING cruise, not after.
    # Inbound TOF is the larger of the Hohmann coast or the braking time.
    # (Optimal low-thrust trajectories overlap these phases.)
    inbound_tof_yr = max(INBOUND_HOHMANN_COAST_YR, cruise_braking_yr)
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
        "accel_avg_m_s2": accel_avg,
        "cruise_braking_yr": cruise_braking_yr,
        "inbound_tof_yr": inbound_tof_yr,
        "round_trip_yr": round_trip_yr,
        "closes_13yr": round_trip_yr <= 13.0,
        "feasible": True,
    }


def main() -> dict:
    all_cells = []
    for dv_name, dv in DV_BUDGETS_KM_S.items():
        for p in POWER_KWE_LIST:
            for sp in SPECIFIC_POWER_W_PER_KG_LIST:
                c = cell(power_kwe=p, specific_power_w_per_kg=sp, dv_km_s=dv)
                c["dv_label"] = dv_name
                all_cells.append(c)

    # Find cells that close 13-yr round trip
    closes_13yr = [c for c in all_cells if c.get("closes_13yr")]
    # Among those, find any with >= 50% delivery
    closes_and_delivers = [c for c in closes_13yr if c.get("delivery_frac", 0) >= 0.5]
    # Pareto frontier: lowest round-trip for each delivery fraction
    feasible = [c for c in all_cells if c.get("feasible")]
    feasible_post_GA = [c for c in feasible if c["dv_label"] == "post_3flyby_tour_R9"]

    # Bisection-like search: at 5 W/kg, what power closes 13-yr exactly?
    # cruise_braking_yr = 13 - 13.18 = -0.18 yr ... so 13-yr is unreachable.
    # What's the lowest achievable round trip at 5 W/kg?
    sp_5 = [c for c in feasible_post_GA if c["specific_power_w_per_kg"] == 5.0]
    sp_5_sorted = sorted(sp_5, key=lambda c: c["round_trip_yr"])
    min_round_trip_5wpkg = sp_5_sorted[0] if sp_5_sorted else None

    # Hypothesis grading
    grading = {
        "H9b_a_power_class_to_close_13yr": {
            "predicted": "40-80 kWe at 5 W/kg",
            "cells_closing_13yr_at_5wpkg_post_GA": [
                {"power_kwe": c["power_kwe"], "round_trip_yr": c["round_trip_yr"]}
                for c in feasible_post_GA
                if c["specific_power_w_per_kg"] == 5.0 and c["closes_13yr"]
            ],
            "verdict": "to-be-judged",
        },
        "H9b_b_delivery_at_round_trip_closing_power": {
            "predicted": "25-40%",
            "delivery_at_closing_cells": [
                {"power_kwe": c["power_kwe"], "delivery_frac": c["delivery_frac"]}
                for c in closes_13yr
            ],
            "verdict": "to-be-judged",
        },
        "H9b_e_13yr_with_50pct_delivery_achievable": {
            "predicted": "No — no cell achieves both",
            "measured_cells_with_both": closes_and_delivers,
            "verdict": "held" if len(closes_and_delivers) == 0 else "falsified",
        },
    }

    results = {
        "inputs": {
            "OUTBOUND_HOHMANN_YR": OUTBOUND_HOHMANN_YR,
            "SATURN_DWELL_YR": SATURN_DWELL_YR,
            "INBOUND_HOHMANN_COAST_YR": INBOUND_HOHMANN_COAST_YR,
            "DRY_T": DRY_T,
            "CHUNK_T": CHUNK_T,
            "ISP_S": ISP_S,
            "ETA": ETA,
            "DUTY": DUTY,
            "POWER_KWE_LIST": POWER_KWE_LIST,
            "SPECIFIC_POWER_W_PER_KG_LIST": SPECIFIC_POWER_W_PER_KG_LIST,
            "DV_BUDGETS_KM_S": DV_BUDGETS_KM_S,
        },
        "cells": all_cells,
        "cells_closing_13yr": closes_13yr,
        "cells_closing_13yr_and_50pct_delivery": closes_and_delivers,
        "min_round_trip_5wpkg_post_GA": min_round_trip_5wpkg,
        "hypothesis_grading": grading,
    }

    out_dir = Path(__file__).parent / "results"
    out_dir.mkdir(exist_ok=True)
    with (out_dir / "power_class_sweep.json").open("w") as f:
        json.dump(results, f, indent=2)

    # --- Console summary ---
    print("=" * 96)
    print("R9b — Power-class trade for chunk-fed inbound braking")
    print("=" * 96)
    print()
    for dv_label, dv in DV_BUDGETS_KM_S.items():
        print(f"Inbound braking ∆v = {dv:.2f} km/s ({dv_label})")
        print(f"  {'P (kWe)':>8} {'sp_pwr':>8} {'reactor':>7} {'m0':>5} {'F':>6} {'accel':>10} "
              f"{'brake':>8} {'RT':>7} {'deliv':>7} {'closes':>7}")
        for c in [c for c in all_cells if c["dv_label"] == dv_label]:
            if c.get("feasible"):
                print(f"  {c['power_kwe']:>6.0f}   {c['specific_power_w_per_kg']:>5.1f} W/kg "
                      f"{c['reactor_t']:>4.1f} t {c['m0_t']:>4.1f} t "
                      f"{c['thrust_N']:>4.2f} N {c['accel_avg_m_s2']:>8.2e} m/s² "
                      f"{c['cruise_braking_yr']:>5.2f} yr {c['round_trip_yr']:>5.2f} yr "
                      f"{c['delivery_frac']*100:>5.1f}% {'YES' if c['closes_13yr'] else 'no':>5}")
            else:
                print(f"  {c['power_kwe']:>6.0f}   {c['specific_power_w_per_kg']:>5.1f} W/kg "
                      f"INFEASIBLE ({c.get('note','')})")
        print()

    print(f"Cells closing 13-yr round trip: {len(closes_13yr)}")
    print(f"Cells closing 13-yr AND >= 50% delivery: {len(closes_and_delivers)}")
    print()
    if min_round_trip_5wpkg:
        print(f"Minimum round trip achievable at 5 W/kg post-GA:")
        print(f"  Power: {min_round_trip_5wpkg['power_kwe']:.0f} kWe")
        print(f"  Round trip: {min_round_trip_5wpkg['round_trip_yr']:.2f} yr")
        print(f"  Delivery: {min_round_trip_5wpkg['delivery_frac']*100:.1f}%")
    print()
    print("Hypothesis grading:")
    for h, g in grading.items():
        v = g.get("verdict", "to-be-judged")
        print(f"  {h}: {v}")
    print()
    print(f"Result JSON: {out_dir / 'power_class_sweep.json'}")
    return results


if __name__ == "__main__":
    main()
