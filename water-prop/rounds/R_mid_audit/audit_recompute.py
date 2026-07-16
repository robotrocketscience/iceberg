"""R-mid — Recompute headline cells under relaxed constraints.

Sweeps round-trip ceiling (14/15/16/18/20 yr), duty cycle (0.5/0.7/0.85),
and thruster choice. Reports max chunk delivered at each (ceiling, duty,
thruster) cell to surface which constraints are load-bearing.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

from waterprop.constants import G0

OUTBOUND_HOHMANN_YR = 6.09
SATURN_DWELL_YR = 1.0
INBOUND_HOHMANN_COAST_YR = 6.09
LUNAR_TOUR_PHASING_YR_3FB = 0.16
LUNAR_TOUR_PHASING_YR_10FB = 0.73
DV_3FB_KM_S = 8.87  # R9 result, 3-flyby tour
DV_10FB_KM_S = 4.47  # R12 result, 10-flyby tour
ETA_BAG = 0.8
DRY_T = 5.0
YEAR_S = 365.25 * 86400.0

THRUSTERS = [
    {"name": "water_MET",                   "isp_s":  700.0, "eta": 0.30},
    {"name": "water_Hall",                  "isp_s": 1500.0, "eta": 0.55},
    {"name": "water_radio_frequency_ion",   "isp_s": 2000.0, "eta": 0.65},
    {"name": "water_dual_ion_5000s",        "isp_s": 5000.0, "eta": 0.55},
    {"name": "water_dual_ion_10000s",       "isp_s":10000.0, "eta": 0.55},
]


def cell_from_delivered(
    delivered_target_t, power_kwe, isp_s, eta_thruster, sp_w_per_kg,
    dv_km_s, phasing_yr, duty, dry_t=DRY_T, eta_bag=ETA_BAG,
) -> dict:
    v_e = isp_s * G0
    v_e_eff = v_e * eta_bag
    reactor_t = power_kwe * 1000.0 / sp_w_per_kg / 1000.0
    pf = 1.0 - math.exp(-dv_km_s * 1000.0 / v_e_eff)
    if 1.0 - pf <= 0:
        return {"feasible": False}
    G = (delivered_target_t + (dry_t + reactor_t) * pf) / (1.0 - pf)
    if G <= 0:
        return {"feasible": False}
    m0_t = G + dry_t + reactor_t
    prop_t = m0_t * pf
    delivered_t = G - prop_t
    F_N = 2.0 * eta_thruster * power_kwe * 1000.0 / v_e
    m_avg_kg = (m0_t - prop_t / 2.0) * 1000.0
    if F_N <= 0 or m_avg_kg <= 0:
        return {"feasible": False}
    accel = F_N / m_avg_kg
    cruise_braking_yr = (dv_km_s * 1000.0) / (accel * duty) / YEAR_S
    inbound_tof_yr = max(INBOUND_HOHMANN_COAST_YR, cruise_braking_yr) + phasing_yr
    rt_yr = OUTBOUND_HOHMANN_YR + SATURN_DWELL_YR + inbound_tof_yr
    return {
        "delivered_t": delivered_t,
        "chunk_grappled_t": G,
        "reactor_t": reactor_t,
        "cruise_braking_yr": cruise_braking_yr,
        "round_trip_yr": rt_yr,
        "feasible": True,
    }


def max_delivered_at_ceiling(power_kwe, isp_s, eta_thruster, sp,
                              dv_km_s, phasing_yr, duty, rt_ceiling_yr):
    lo, hi = 0.0, 5000.0
    for _ in range(50):
        mid = (lo + hi) / 2.0
        c = cell_from_delivered(mid, power_kwe, isp_s, eta_thruster, sp,
                                 dv_km_s, phasing_yr, duty)
        if c.get("feasible") and c["round_trip_yr"] <= rt_ceiling_yr:
            lo = mid
        else:
            hi = mid
    return lo


def main():
    POWERS = [10.0, 40.0, 100.0, 500.0]
    DUTIES = [0.5, 0.7, 0.85]
    RT_CEILINGS = [14.0, 15.0, 16.0, 18.0, 20.0]
    SP = 10.0  # Fission Surface Power target specific power
    TOURS = {
        "3-flyby": (DV_3FB_KM_S, LUNAR_TOUR_PHASING_YR_3FB),
        "10-flyby": (DV_10FB_KM_S, LUNAR_TOUR_PHASING_YR_10FB),
    }

    grid = []
    for tour_name, (dv, phasing) in TOURS.items():
        for power in POWERS:
            for thr in THRUSTERS:
                for duty in DUTIES:
                    for rt_ceil in RT_CEILINGS:
                        max_d = max_delivered_at_ceiling(
                            power, thr["isp_s"], thr["eta"], SP,
                            dv, phasing, duty, rt_ceil,
                        )
                        grid.append({
                            "tour": tour_name,
                            "power_kwe": power,
                            "thruster": thr["name"],
                            "isp_s": thr["isp_s"],
                            "duty": duty,
                            "rt_ceiling_yr": rt_ceil,
                            "max_delivered_t": max_d,
                        })

    out_dir = Path(__file__).parent / "results"
    out_dir.mkdir(exist_ok=True)
    with (out_dir / "audit_recompute.json").open("w") as f:
        json.dump({"grid": grid}, f, indent=2)

    print("=" * 96)
    print("R-mid — Constraint relaxation sweep: round-trip ceiling × duty × tour × thruster")
    print("=" * 96)
    print()
    print("Specific power held at 10 W/kg. Bag η_c = 0.8.")
    print()
    for tour_name in TOURS:
        for duty in DUTIES:
            print(f"\n--- {tour_name} tour, duty cycle = {duty} ---")
            print(f"  Max delivered chunk (tonnes) at each round-trip ceiling × power × thruster:")
            print(f"  {'Power':>5} {'Thruster':<28} " +
                  "  ".join(f"{rt:.0f}yr" for rt in RT_CEILINGS))
            for power in POWERS:
                for thr in THRUSTERS:
                    row = []
                    for rt_ceil in RT_CEILINGS:
                        c = next(g for g in grid
                                 if g["tour"] == tour_name and g["power_kwe"] == power
                                 and g["thruster"] == thr["name"]
                                 and g["duty"] == duty and g["rt_ceiling_yr"] == rt_ceil)
                        row.append(f"{c['max_delivered_t']:>5.0f}")
                    print(f"  {power:>3.0f}kWe  {thr['name']:<25} " + "    ".join(row))
    print()

    # Headline: max delivered per power class at relaxed ceilings
    print("HEADLINE COMPARISON (3-flyby tour, best thruster per cell):")
    print(f"  {'Power':>5} {'Duty':>4}  " + "  ".join(f"{rt:.0f}yr" for rt in RT_CEILINGS))
    for duty in DUTIES:
        for power in POWERS:
            row = []
            for rt_ceil in RT_CEILINGS:
                best = max(
                    (g for g in grid if g["tour"] == "3-flyby"
                     and g["power_kwe"] == power
                     and g["duty"] == duty
                     and g["rt_ceiling_yr"] == rt_ceil),
                    key=lambda g: g["max_delivered_t"],
                )
                row.append(f"{best['max_delivered_t']:>5.0f}t ({best['thruster'][:8]})")
            print(f"  {power:>3.0f}kWe  {duty:.2f}   " + "  ".join(row))
    print()


if __name__ == "__main__":
    main()
