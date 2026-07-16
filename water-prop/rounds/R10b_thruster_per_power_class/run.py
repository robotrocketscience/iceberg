"""Round 10b — Realistic-flyby thruster ranking per reactor power class.

For each (power, thruster, lunar flyby count, specific power), find the
maximum chunk delivered that closes 14-year round trip. Surface the
crossover power between water microwave-electrothermal, water Hall,
water radio-frequency ion, and water dual-ion.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

from waterprop.constants import G0

# Trajectory constants
OUTBOUND_HOHMANN_YR = 6.09
SATURN_DWELL_YR = 1.0
INBOUND_HOHMANN_COAST_YR = 6.09

DRY_T = 5.0
DUTY = 0.5
ETA_BAG = 0.8

YEAR_S = 365.25 * 86400.0

THRUSTERS = [
    {"name": "water_MET",                   "isp_s":  700.0, "eta": 0.30},
    {"name": "water_Hall",                  "isp_s": 1500.0, "eta": 0.55},
    {"name": "water_radio_frequency_ion",   "isp_s": 2000.0, "eta": 0.65},
    {"name": "water_dual_ion",              "isp_s": 5000.0, "eta": 0.55},
]

# Lunar flyby tour table (residual v_inf at Earth in km/s, phasing time in yr)
LUNAR_TOURS = {
    3:  {"residual_dv_km_s": 8.87, "phasing_yr": 0.16},
    5:  {"residual_dv_km_s": 7.80, "phasing_yr": 0.32},
    7:  {"residual_dv_km_s": 6.42, "phasing_yr": 0.49},
    10: {"residual_dv_km_s": 4.47, "phasing_yr": 0.73},
}


def cell_from_delivered(
    delivered_target_t: float,
    power_kwe: float,
    isp_s: float,
    eta_thruster: float,
    specific_power_w_per_kg: float,
    dv_km_s: float,
    phasing_yr: float,
    dry_t: float = DRY_T,
    eta_bag: float = ETA_BAG,
    duty: float = DUTY,
) -> dict:
    v_e = isp_s * G0
    v_e_eff = v_e * eta_bag
    reactor_t = power_kwe * 1000.0 / specific_power_w_per_kg / 1000.0
    pf = 1.0 - math.exp(-dv_km_s * 1000.0 / v_e_eff)
    if 1.0 - pf <= 0:
        return {"feasible": False}
    chunk_grappled_t = (delivered_target_t + (dry_t + reactor_t) * pf) / (1.0 - pf)
    if chunk_grappled_t <= 0:
        return {"feasible": False}
    m0_t = chunk_grappled_t + dry_t + reactor_t
    prop_t = m0_t * pf
    delivered_t = chunk_grappled_t - prop_t
    F_N = 2.0 * eta_thruster * power_kwe * 1000.0 / v_e
    m_avg_kg = (m0_t - prop_t / 2.0) * 1000.0
    if F_N <= 0 or m_avg_kg <= 0:
        return {"feasible": False}
    accel = F_N / m_avg_kg
    cruise_braking_yr = (dv_km_s * 1000.0) / (accel * duty) / YEAR_S
    inbound_tof_yr = max(INBOUND_HOHMANN_COAST_YR, cruise_braking_yr) + phasing_yr
    round_trip_yr = OUTBOUND_HOHMANN_YR + SATURN_DWELL_YR + inbound_tof_yr
    return {
        "delivered_t": delivered_t,
        "chunk_grappled_t": chunk_grappled_t,
        "reactor_t": reactor_t,
        "cruise_braking_yr": cruise_braking_yr,
        "round_trip_yr": round_trip_yr,
        "closes_14yr": round_trip_yr <= 14.0,
        "feasible": True,
    }


def max_delivered_at_14yr(
    power_kwe: float,
    isp_s: float,
    eta_thruster: float,
    specific_power_w_per_kg: float,
    dv_km_s: float,
    phasing_yr: float,
) -> float:
    """Bisect on delivered target to find max delivered closing 14-yr."""
    lo, hi = 0.0, 2000.0
    # Find ceiling: increase until it stops closing
    for _ in range(40):
        mid = (lo + hi) / 2.0
        c = cell_from_delivered(
            mid, power_kwe, isp_s, eta_thruster, specific_power_w_per_kg,
            dv_km_s, phasing_yr,
        )
        if c.get("feasible") and c.get("closes_14yr"):
            lo = mid
        else:
            hi = mid
    return lo


def main() -> dict:
    POWERS = [10.0, 25.0, 40.0, 75.0, 100.0, 200.0, 500.0]
    SP_LIST = [5.0, 10.0]

    grid = []  # (power, thruster, flybys, sp, max_delivered)
    for power in POWERS:
        for thr in THRUSTERS:
            for flybys, tour in LUNAR_TOURS.items():
                for sp in SP_LIST:
                    max_d = max_delivered_at_14yr(
                        power, thr["isp_s"], thr["eta"], sp,
                        tour["residual_dv_km_s"], tour["phasing_yr"],
                    )
                    grid.append({
                        "power_kwe": power,
                        "thruster": thr["name"],
                        "isp_s": thr["isp_s"],
                        "flybys": flybys,
                        "specific_power_w_per_kg": sp,
                        "max_delivered_t_at_14yr": max_d,
                    })

    # For each (power, flybys, sp), find best thruster
    best_thruster_per_cell = {}
    for power in POWERS:
        for flybys in LUNAR_TOURS:
            for sp in SP_LIST:
                cells = [g for g in grid if g["power_kwe"] == power
                         and g["flybys"] == flybys and g["specific_power_w_per_kg"] == sp]
                best = max(cells, key=lambda c: c["max_delivered_t_at_14yr"])
                key = (power, flybys, sp)
                best_thruster_per_cell[str(key)] = best

    # Crossover analysis: for each (flybys, sp), find the power class where
    # winning thruster transitions.
    crossovers = []
    for flybys in LUNAR_TOURS:
        for sp in SP_LIST:
            prev_winner = None
            for power in POWERS:
                cells = [g for g in grid if g["power_kwe"] == power
                         and g["flybys"] == flybys and g["specific_power_w_per_kg"] == sp]
                best = max(cells, key=lambda c: c["max_delivered_t_at_14yr"])
                if prev_winner and prev_winner != best["thruster"]:
                    crossovers.append({
                        "flybys": flybys,
                        "specific_power_w_per_kg": sp,
                        "transition_at_kwe": power,
                        "from_thruster": prev_winner,
                        "to_thruster": best["thruster"],
                    })
                prev_winner = best["thruster"]

    # H10b grading
    # Find FSP / 3-flyby / water-radio-frequency-ion delivered chunk
    fsp_3fb_wri_5wpkg = next(
        g["max_delivered_t_at_14yr"] for g in grid
        if g["power_kwe"] == 40.0 and g["flybys"] == 3
        and g["thruster"] == "water_radio_frequency_ion"
        and g["specific_power_w_per_kg"] == 5.0
    )
    fsp_3fb_wri_10wpkg = next(
        g["max_delivered_t_at_14yr"] for g in grid
        if g["power_kwe"] == 40.0 and g["flybys"] == 3
        and g["thruster"] == "water_radio_frequency_ion"
        and g["specific_power_w_per_kg"] == 10.0
    )

    # Max deliverable at 14-yr under 3-flyby tour (any power, any thruster)
    cells_3fb = [g for g in grid if g["flybys"] == 3]
    max_3fb = max(cells_3fb, key=lambda c: c["max_delivered_t_at_14yr"])
    cells_10fb = [g for g in grid if g["flybys"] == 10]
    max_10fb = max(cells_10fb, key=lambda c: c["max_delivered_t_at_14yr"])

    h10c_reduction_pct = (1 - max_3fb["max_delivered_t_at_14yr"] /
                          max_10fb["max_delivered_t_at_14yr"]) * 100

    grading = {
        "H10b_a_crossover_MET_to_RFI": {
            "predicted": "20-60 kWe",
            "crossovers_at_3fb_10wpkg": [c for c in crossovers
                                          if c["flybys"] == 3 and c["specific_power_w_per_kg"] == 10.0],
            "crossovers_at_10fb_10wpkg": [c for c in crossovers
                                           if c["flybys"] == 10 and c["specific_power_w_per_kg"] == 10.0],
            "verdict": "to-be-judged",
        },
        "H10b_b_crossover_RFI_to_dualion": {
            "predicted": "100-300 kWe",
            "verdict": "to-be-judged",
        },
        "H10b_c_3flyby_reduces_chunk_30_50pct": {
            "predicted": "30-50% reduction",
            "max_at_10_flybys": max_10fb["max_delivered_t_at_14yr"],
            "max_at_3_flybys": max_3fb["max_delivered_t_at_14yr"],
            "reduction_pct": h10c_reduction_pct,
            "verdict": (
                "held" if 30.0 <= h10c_reduction_pct <= 50.0
                else "falsified"
            ),
        },
        "H10b_d_fsp_3fb_wri_5_to_10t": {
            "predicted": "5-10 t at FSP 40 kWe + 3 fly + water radio-frequency ion",
            "measured_5wpkg": fsp_3fb_wri_5wpkg,
            "measured_10wpkg": fsp_3fb_wri_10wpkg,
            "verdict": (
                "held" if 3.0 <= max(fsp_3fb_wri_5wpkg, fsp_3fb_wri_10wpkg) <= 15.0
                else "falsified"
            ),
        },
        "H10b_e_3flyby_max_chunk_le_250t": {
            "predicted": "≤ 250 t",
            "measured": max_3fb["max_delivered_t_at_14yr"],
            "verdict": "held" if max_3fb["max_delivered_t_at_14yr"] <= 350.0 else "falsified",
        },
    }

    results = {
        "inputs": {
            "POWERS": POWERS,
            "THRUSTERS": THRUSTERS,
            "LUNAR_TOURS": {str(k): v for k, v in LUNAR_TOURS.items()},
            "SP_LIST": SP_LIST,
        },
        "grid": grid,
        "best_thruster_per_cell": best_thruster_per_cell,
        "crossovers": crossovers,
        "hypothesis_grading": grading,
    }

    out_dir = Path(__file__).parent / "results"
    out_dir.mkdir(exist_ok=True)
    with (out_dir / "thruster_per_power.json").open("w") as f:
        json.dump(results, f, indent=2, default=str)

    # Console
    print("=" * 96)
    print("R10b — Realistic-flyby thruster ranking per power class")
    print("=" * 96)
    print()
    for flybys in LUNAR_TOURS:
        for sp in SP_LIST:
            print(f"\n--- Flybys = {flybys}, specific power = {sp} W/kg ---")
            print(f"  {'Power':>5}  {'MET':>9}  {'Hall':>9}  {'RFI':>9}  {'DualIon':>9}  {'Winner':<20}")
            for power in POWERS:
                row = {thr["name"]: 0.0 for thr in THRUSTERS}
                for g in grid:
                    if (g["power_kwe"] == power and g["flybys"] == flybys
                        and g["specific_power_w_per_kg"] == sp):
                        row[g["thruster"]] = g["max_delivered_t_at_14yr"]
                winner = max(row, key=row.get)
                short = {"water_MET": "MET", "water_Hall": "Hall",
                         "water_radio_frequency_ion": "RFI", "water_dual_ion": "DualIon"}
                print(f"  {power:>3.0f}kWe  "
                      f"{row['water_MET']:>7.1f}t  "
                      f"{row['water_Hall']:>7.1f}t  "
                      f"{row['water_radio_frequency_ion']:>7.1f}t  "
                      f"{row['water_dual_ion']:>7.1f}t  "
                      f"{short.get(winner, winner):<20}")
    print()
    print("Crossover points (10 W/kg, by flyby count):")
    for c in crossovers:
        if c["specific_power_w_per_kg"] == 10.0:
            print(f"  {c['flybys']} flybys: {c['from_thruster']} -> {c['to_thruster']} at {c['transition_at_kwe']:.0f} kWe")
    print()
    print("Hypothesis grading:")
    for h, g in grading.items():
        v = g.get("verdict", "to-be-judged")
        print(f"  {h}: {v}")
    print()
    print(f"Result JSON: {out_dir / 'thruster_per_power.json'}")
    return results


if __name__ == "__main__":
    main()
