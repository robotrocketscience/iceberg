"""Round 13 — Dual-ion architecture trade.

Sweeps chunk mass x reactor power x specific impulse x reactor specific
power for water dual-ion (electrolyzed H+ + O+) inbound braking.
Compares against R12 best cell (water radio-frequency ion + 10-flyby
lunar tour: 14 t / 13.91 yr / 70.1% delivery at 15 kWe).
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
LUNAR_TOUR_PHASING_YR = 0.73  # R12's 10-flyby tour
INBOUND_DV_KM_S = 4.47        # R12 residual after 10-flyby lunar tour

# Vehicle
DRY_T_BASE = 5.0
DUTY = 0.5

# Dual-ion thruster assumptions
ETA_DUAL_ION = 0.55              # slightly worse than water RF ion's 0.65
ELECTROLYZER_KG_PER_KWE = 0.5     # mass penalty for the electrolyzer

YEAR_S = 365.25 * 86400.0

# Sweep
CHUNK_T_LIST = [14.0, 50.0, 200.0]
POWER_KWE_LIST = [10.0, 40.0, 100.0, 200.0, 500.0]
ISP_S_LIST = [3000.0, 5000.0, 7500.0, 10000.0, 12000.0]
SPECIFIC_POWER_W_PER_KG_LIST = [5.0, 10.0]


def cell(
    chunk_t: float,
    power_kwe: float,
    isp_s: float,
    specific_power_w_per_kg: float,
    dv_km_s: float = INBOUND_DV_KM_S,
    dry_t_base: float = DRY_T_BASE,
    eta: float = ETA_DUAL_ION,
    duty: float = DUTY,
) -> dict:
    v_e = isp_s * G0  # m/s
    reactor_t = (power_kwe * 1000.0) / specific_power_w_per_kg / 1000.0
    electrolyzer_t = (power_kwe * ELECTROLYZER_KG_PER_KWE) / 1000.0
    dry_t = dry_t_base + electrolyzer_t
    m0_t = chunk_t + dry_t + reactor_t
    prop_frac = 1.0 - math.exp(-dv_km_s * 1000.0 / v_e)
    prop_req_t = m0_t * prop_frac
    delivered_chunk_t = max(chunk_t - prop_req_t, 0.0)
    if delivered_chunk_t <= 0:
        return {
            "chunk_t": chunk_t,
            "power_kwe": power_kwe,
            "isp_s": isp_s,
            "specific_power_w_per_kg": specific_power_w_per_kg,
            "feasible": False,
            "note": "propellant exceeds chunk",
        }
    F_N = 2.0 * eta * power_kwe * 1000.0 / v_e
    m_avg_kg = (m0_t - prop_req_t / 2.0) * 1000.0
    if F_N <= 0 or m_avg_kg <= 0:
        return {
            "chunk_t": chunk_t,
            "power_kwe": power_kwe,
            "isp_s": isp_s,
            "specific_power_w_per_kg": specific_power_w_per_kg,
            "feasible": False,
            "note": "no thrust or zero mass",
        }
    accel = F_N / m_avg_kg
    cruise_braking_yr = (dv_km_s * 1000.0) / (accel * duty) / YEAR_S
    inbound_tof_yr = max(INBOUND_HOHMANN_COAST_YR, cruise_braking_yr) + LUNAR_TOUR_PHASING_YR
    round_trip_yr = OUTBOUND_HOHMANN_YR + SATURN_DWELL_YR + inbound_tof_yr
    return {
        "chunk_t": chunk_t,
        "power_kwe": power_kwe,
        "isp_s": isp_s,
        "specific_power_w_per_kg": specific_power_w_per_kg,
        "reactor_t": reactor_t,
        "electrolyzer_t": electrolyzer_t,
        "dry_t": dry_t,
        "m0_t": m0_t,
        "prop_req_t": prop_req_t,
        "delivered_chunk_t": delivered_chunk_t,
        "delivery_frac": delivered_chunk_t / chunk_t,
        "thrust_N": F_N,
        "accel_m_s2": accel,
        "cruise_braking_yr": cruise_braking_yr,
        "inbound_tof_yr": inbound_tof_yr,
        "round_trip_yr": round_trip_yr,
        "closes_14yr": round_trip_yr <= 14.0,
        "feasible": True,
    }


def water_rf_ion_baseline_cell(
    chunk_t: float,
    power_kwe: float,
    specific_power_w_per_kg: float,
    isp_s: float = 2000.0,
    eta: float = 0.65,
) -> dict:
    """R12-style water radio-frequency ion baseline at the same trajectory
    + lunar tour assumption. For direct comparison."""
    v_e = isp_s * G0
    reactor_t = (power_kwe * 1000.0) / specific_power_w_per_kg / 1000.0
    dry_t = DRY_T_BASE
    m0_t = chunk_t + dry_t + reactor_t
    dv_km_s = INBOUND_DV_KM_S
    prop_frac = 1.0 - math.exp(-dv_km_s * 1000.0 / v_e)
    prop_req_t = m0_t * prop_frac
    delivered_chunk_t = max(chunk_t - prop_req_t, 0.0)
    if delivered_chunk_t <= 0:
        return {"chunk_t": chunk_t, "power_kwe": power_kwe, "feasible": False}
    F_N = 2.0 * eta * power_kwe * 1000.0 / v_e
    m_avg_kg = (m0_t - prop_req_t / 2.0) * 1000.0
    accel = F_N / m_avg_kg
    cruise_braking_yr = (dv_km_s * 1000.0) / (accel * DUTY) / YEAR_S
    inbound_tof_yr = max(INBOUND_HOHMANN_COAST_YR, cruise_braking_yr) + LUNAR_TOUR_PHASING_YR
    round_trip_yr = OUTBOUND_HOHMANN_YR + SATURN_DWELL_YR + inbound_tof_yr
    return {
        "chunk_t": chunk_t,
        "power_kwe": power_kwe,
        "isp_s": isp_s,
        "specific_power_w_per_kg": specific_power_w_per_kg,
        "reactor_t": reactor_t,
        "dry_t": dry_t,
        "m0_t": m0_t,
        "delivered_chunk_t": delivered_chunk_t,
        "delivery_frac": delivered_chunk_t / chunk_t,
        "cruise_braking_yr": cruise_braking_yr,
        "round_trip_yr": round_trip_yr,
        "closes_14yr": round_trip_yr <= 14.0,
        "feasible": True,
    }


def main() -> dict:
    cells = []
    for chunk_t in CHUNK_T_LIST:
        for p in POWER_KWE_LIST:
            for isp in ISP_S_LIST:
                for sp in SPECIFIC_POWER_W_PER_KG_LIST:
                    cells.append(cell(chunk_t, p, isp, sp))

    feasible = [c for c in cells if c.get("feasible")]
    closes_14yr = [c for c in feasible if c.get("closes_14yr")]

    # Baseline comparison: water RF ion at the same power × chunk grid
    baseline = []
    for chunk_t in CHUNK_T_LIST:
        for p in POWER_KWE_LIST:
            for sp in SPECIFIC_POWER_W_PER_KG_LIST:
                baseline.append(water_rf_ion_baseline_cell(chunk_t, p, sp))

    # Best cells per chunk mass that close 14-yr round trip
    best_per_chunk = {}
    for chunk_t in CHUNK_T_LIST:
        chunk_cells = [c for c in closes_14yr if c["chunk_t"] == chunk_t]
        if chunk_cells:
            best_per_chunk[chunk_t] = max(chunk_cells, key=lambda c: c["delivery_frac"])
        else:
            best_per_chunk[chunk_t] = None

    # Side-by-side comparison: dual-ion best vs water-RF-ion best at same chunk
    comparison = []
    for chunk_t in CHUNK_T_LIST:
        dual_best = best_per_chunk[chunk_t]
        wri_cells = [c for c in baseline if c["chunk_t"] == chunk_t and c.get("closes_14yr")]
        wri_best = max(wri_cells, key=lambda c: c["delivery_frac"]) if wri_cells else None
        comparison.append({
            "chunk_t": chunk_t,
            "dual_ion_best": dual_best,
            "water_rf_ion_best": wri_best,
            "delta_delivery_pp": (
                (dual_best["delivery_frac"] - wri_best["delivery_frac"]) * 100
                if (dual_best and wri_best) else None
            ),
        })

    # Hypothesis grading
    def find_cell(chunk_t, power_kwe, isp_s, sp_w_per_kg):
        for c in cells:
            if (c["chunk_t"] == chunk_t and c["power_kwe"] == power_kwe
                and c["isp_s"] == isp_s and c["specific_power_w_per_kg"] == sp_w_per_kg
                and c.get("feasible")):
                return c
        return None
    def find_baseline(chunk_t, power_kwe, sp_w_per_kg):
        for c in baseline:
            if (c["chunk_t"] == chunk_t and c["power_kwe"] == power_kwe
                and c["specific_power_w_per_kg"] == sp_w_per_kg and c.get("feasible")):
                return c
        return None

    h13a_dual = find_cell(14.0, 40.0, 5000.0, 10.0)
    h13a_wri = find_baseline(14.0, 40.0, 10.0)
    h13a_delta = (
        (h13a_dual["delivery_frac"] - h13a_wri["delivery_frac"]) * 100
        if h13a_dual and h13a_wri else None
    )

    h13b = find_cell(14.0, 100.0, 7500.0, 10.0)
    h13c = find_cell(200.0, 500.0, 10000.0, 10.0)

    grading = {
        "H13a_40kwe_dual_vs_water_rf_ion": {
            "predicted": "comparable, ±5 pp",
            "dual_ion_cell": h13a_dual,
            "wri_cell": h13a_wri,
            "delta_pp": h13a_delta,
            "verdict": (
                "held" if h13a_delta is not None and abs(h13a_delta) <= 10
                else "falsified"
            ),
        },
        "H13b_100kwe_85pct_at_14yr": {
            "predicted": "yes",
            "measured": h13b,
            "verdict": (
                "held" if h13b and h13b.get("closes_14yr") and h13b["delivery_frac"] >= 0.85
                else "falsified" if h13b else "no cell"
            ),
        },
        "H13c_500kwe_200t_at_14yr": {
            "predicted": "yes",
            "measured": h13c,
            "verdict": (
                "held" if h13c and h13c.get("closes_14yr") and h13c["delivered_chunk_t"] >= 80
                else "falsified" if h13c else "no cell"
            ),
        },
    }

    results = {
        "inputs": {
            "OUTBOUND_HOHMANN_YR": OUTBOUND_HOHMANN_YR,
            "SATURN_DWELL_YR": SATURN_DWELL_YR,
            "INBOUND_HOHMANN_COAST_YR": INBOUND_HOHMANN_COAST_YR,
            "LUNAR_TOUR_PHASING_YR": LUNAR_TOUR_PHASING_YR,
            "INBOUND_DV_KM_S": INBOUND_DV_KM_S,
            "ETA_DUAL_ION": ETA_DUAL_ION,
            "ELECTROLYZER_KG_PER_KWE": ELECTROLYZER_KG_PER_KWE,
            "DUTY": DUTY,
            "CHUNK_T_LIST": CHUNK_T_LIST,
            "POWER_KWE_LIST": POWER_KWE_LIST,
            "ISP_S_LIST": ISP_S_LIST,
            "SPECIFIC_POWER_W_PER_KG_LIST": SPECIFIC_POWER_W_PER_KG_LIST,
        },
        "cells": cells,
        "baseline_water_rf_ion": baseline,
        "best_per_chunk": best_per_chunk,
        "side_by_side": comparison,
        "hypothesis_grading": grading,
    }

    out_dir = Path(__file__).parent / "results"
    out_dir.mkdir(exist_ok=True)
    with (out_dir / "dual_ion_sweep.json").open("w") as f:
        json.dump(results, f, indent=2)

    # Console summary
    print("=" * 96)
    print("R13 — Dual-ion architecture trade (electrolyzed H+/O+ at 3000-12000 s specific impulse)")
    print("=" * 96)
    print()
    print(f"Inbound braking delta-v: {INBOUND_DV_KM_S} km/s (R12 post 10-flyby lunar tour)")
    print(f"Dual-ion efficiency assumed: {ETA_DUAL_ION}")
    print(f"Electrolyzer mass penalty: {ELECTROLYZER_KG_PER_KWE} kg/kWe")
    print()
    print(f"DUAL-ION CELLS (closing 14-year round trip):")
    print(f"  {'chunk':>5} {'power':>5} {'isp':>5} {'sp_p':>4} {'reactor':>7} {'elec':>5} {'thrust':>7} {'brake':>6} {'RT':>6} {'deliv':>6}")
    for c in closes_14yr:
        print(f"  {c['chunk_t']:>4.0f}t {c['power_kwe']:>3.0f}kWe "
              f"{c['isp_s']:>4.0f}s {c['specific_power_w_per_kg']:>3.1f} "
              f"{c['reactor_t']:>4.1f}t {c['electrolyzer_t']:>4.2f}t "
              f"{c['thrust_N']:>4.2f}N {c['cruise_braking_yr']:>4.2f}yr "
              f"{c['round_trip_yr']:>5.2f}yr {c['delivery_frac']*100:>5.1f}%")
    print()
    print(f"SIDE-BY-SIDE (best cell per chunk mass closing 14-yr):")
    for cmp in comparison:
        print(f"\n  Chunk = {cmp['chunk_t']:.0f} t:")
        d = cmp["dual_ion_best"]
        w = cmp["water_rf_ion_best"]
        if d:
            print(f"    Dual-ion best:      {d['power_kwe']:>4.0f} kWe at {d['isp_s']:>5.0f} s -> "
                  f"{d['round_trip_yr']:.2f} yr / {d['delivery_frac']*100:.1f}% delivery")
        else:
            print("    Dual-ion:           NO 14-yr-closing cell")
        if w:
            print(f"    Water RF ion best:  {w['power_kwe']:>4.0f} kWe at 2000 s -> "
                  f"{w['round_trip_yr']:.2f} yr / {w['delivery_frac']*100:.1f}% delivery")
        else:
            print("    Water RF ion:       NO 14-yr-closing cell")
        if cmp["delta_delivery_pp"] is not None:
            print(f"    Delta (dual − water RF ion): {cmp['delta_delivery_pp']:+.1f} percentage points")
    print()
    print(f"Hypothesis grading:")
    for h, g in grading.items():
        print(f"  {h}: {g.get('verdict')}")
    print()
    print(f"Result JSON: {out_dir / 'dual_ion_sweep.json'}")
    return results


if __name__ == "__main__":
    main()
