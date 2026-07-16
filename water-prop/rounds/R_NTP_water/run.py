"""R-NTP-water — Nuclear thermal water propulsion architecture analysis.

Computes per-ship mass budget and round-trip time under NTP-water,
comparing against R15-rerun electric-propulsion baseline.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

# Mission delta-velocity breakdown
DV_TSI_KM_S = 7.3            # Trans-Saturn-injection from low Earth orbit
DV_SATURN_CAPTURE_KM_S = 1.0
DV_SATURN_DEPART_KM_S = 1.5  # Chunk-fed
DV_INBOUND_CRUISE_KM_S = 2.0  # Chunk-fed
DV_EARTH_ARRIVAL_KM_S = 2.5  # After lunar gravity assist, chunk-fed

DRY_T = 5.0          # Operator-side dry vehicle mass
NTP_REACTOR_T = 8.0  # NTP reactor + chamber + nozzle, NERVA-class ~6-10 t
EARTH_WATER_RESERVE_T = 2.0  # Buffer for outbound trim corrections
BAG_ETA_C = 0.8

G0 = 9.81
YEAR_S = 365.25 * 86400.0

# Round-trip composition
OUTBOUND_HOHMANN_YR = 6.09
SATURN_DWELL_YR = 1.0
INBOUND_HOHMANN_YR = 6.09
NTP_BURN_TOTAL_YR = 0.3  # impulsive burns negligible vs cruise time


def ntp_mission_mass_budget(
    isp_s: float,
    chunk_grappled_t: float,
    bag_eta_c: float = BAG_ETA_C,
) -> dict:
    """Compute pre-launch mass and delivered chunk for NTP-water mission.

    Mission profile: TSI + Saturn capture done with Earth-launched water at
    full Isp. Saturn depart + inbound cruise + Earth arrival done with
    chunk-fed water at bag_eta_c × Isp effective.
    """
    v_e_earth = isp_s * G0
    v_e_chunk = isp_s * G0 * bag_eta_c

    # Inbound delta-velocity total (after lunar gravity assist), chunk-fed:
    dv_chunk_total = DV_SATURN_DEPART_KM_S + DV_INBOUND_CRUISE_KM_S + DV_EARTH_ARRIVAL_KM_S
    pf_chunk = 1.0 - math.exp(-dv_chunk_total * 1000.0 / v_e_chunk)
    if pf_chunk >= 1.0:
        return {"feasible": False, "note": "chunk delta-v exceeds effective specific impulse"}

    # Working backward: chunk_grappled → delivered_chunk
    # Initial mass at Saturn departure = chunk_grappled + dry + reactor
    m0_at_saturn_depart = chunk_grappled_t + DRY_T + NTP_REACTOR_T
    chunk_propellant_burned = m0_at_saturn_depart * pf_chunk
    delivered_chunk_t = max(chunk_grappled_t - chunk_propellant_burned, 0.0)

    # Working forward: Earth-launched water required for trans-Saturn-injection + Saturn capture
    dv_earth_total = DV_TSI_KM_S + DV_SATURN_CAPTURE_KM_S
    pf_earth = 1.0 - math.exp(-dv_earth_total * 1000.0 / v_e_earth)
    if pf_earth >= 1.0:
        return {"feasible": False, "note": "Earth-side delta-v exceeds specific impulse"}

    # Mass at Saturn arrival (before grapple) = dry + reactor + small reserve
    # (Earth-launched water mostly burned by then)
    m_at_saturn_arrival = DRY_T + NTP_REACTOR_T + EARTH_WATER_RESERVE_T  # buffer
    # Mass at LEO pre-TSI = m_at_saturn_arrival / (1 - pf_earth)
    # But this assumes ALL Earth water is burned in TSI+capture. Reserve is on top.
    m0_leo_pre_tsi = m_at_saturn_arrival / (1.0 - pf_earth)
    earth_water_propellant = m0_leo_pre_tsi - m_at_saturn_arrival

    return {
        "isp_s": isp_s,
        "v_e_earth_m_s": v_e_earth,
        "v_e_chunk_m_s": v_e_chunk,
        "chunk_grappled_t": chunk_grappled_t,
        "chunk_propellant_burned_t": chunk_propellant_burned,
        "delivered_chunk_t": delivered_chunk_t,
        "delivery_frac": delivered_chunk_t / chunk_grappled_t,
        "m0_leo_pre_tsi_t": m0_leo_pre_tsi,
        "earth_water_propellant_t": earth_water_propellant,
        "m_at_saturn_arrival_t": m_at_saturn_arrival,
        "m_at_saturn_depart_t": m0_at_saturn_depart,
        "pf_earth": pf_earth,
        "pf_chunk": pf_chunk,
        "feasible": delivered_chunk_t > 0.0,
        "round_trip_yr": OUTBOUND_HOHMANN_YR + SATURN_DWELL_YR + INBOUND_HOHMANN_YR + NTP_BURN_TOTAL_YR,
    }


def main() -> dict:
    ISP_LIST = [400.0, 500.0, 600.0]
    CHUNK_LIST = [14.0, 50.0, 100.0, 200.0]

    cells = []
    for isp in ISP_LIST:
        for chunk in CHUNK_LIST:
            c = ntp_mission_mass_budget(isp, chunk)
            cells.append(c)

    out_dir = Path(__file__).parent / "results"
    out_dir.mkdir(exist_ok=True)
    with (out_dir / "ntp_water.json").open("w") as f:
        json.dump({"cells": cells}, f, indent=2)

    print("=" * 96)
    print("R-NTP-water — Nuclear thermal water propulsion architecture")
    print("=" * 96)
    print()
    print(f"Mission profile: NTP for trans-Saturn-injection + Saturn capture (Earth water)")
    print(f"  + NTP for Saturn depart + inbound braking (chunk-fed at bag eta_c = {BAG_ETA_C})")
    print(f"  Round trip: Hohmann + Saturn dwell + Hohmann + impulsive burns = "
          f"{OUTBOUND_HOHMANN_YR + SATURN_DWELL_YR + INBOUND_HOHMANN_YR + NTP_BURN_TOTAL_YR:.2f} yr")
    print()
    print(f"{'Isp':>4}  {'Chunk':>5}  {'PreTSI_m':>9}  {'Earth_H2O':>9}  "
          f"{'M@Sat_arr':>9}  {'M@Sat_dep':>9}  {'Prop_burn':>9}  {'Delivered':>9}  {'Fraction':>8}")
    for c in cells:
        if not c.get("feasible"):
            print(f"  {c['isp_s']:>3.0f}s  {c['chunk_grappled_t']:>3.0f}t  INFEASIBLE  {c.get('note','')}")
            continue
        print(f"  {c['isp_s']:>3.0f}s  {c['chunk_grappled_t']:>3.0f}t  "
              f"{c['m0_leo_pre_tsi_t']:>6.1f}t  "
              f"{c['earth_water_propellant_t']:>6.1f}t  "
              f"{c['m_at_saturn_arrival_t']:>6.1f}t  "
              f"{c['m_at_saturn_depart_t']:>6.1f}t  "
              f"{c['chunk_propellant_burned_t']:>6.1f}t  "
              f"{c['delivered_chunk_t']:>6.1f}t  "
              f"{c['delivery_frac']*100:>5.1f}%")

    print()
    # Comparison vs electric baseline (R15-rerun audited)
    # R15-rerun gave Kilopower 7t, FSP 42t, etc. Those numbers assumed 14-yr round trip via
    # 10-flyby lunar tour. NTP-water gives 13.5 yr.
    print("Comparison: NTP-water 500s Isp vs electric water radio-frequency ion (R15-rerun audited):")
    print(f"  Architecture                         Round trip   Delivered (14 t chunk grappled)   Pre-TSI mass")
    ntp_500_14 = ntp_mission_mass_budget(500.0, 14.0)
    print(f"  NTP-water 500 s + 14 t chunk         13.5 yr      {ntp_500_14['delivered_chunk_t']:.1f} t                          "
          f"{ntp_500_14['m0_leo_pre_tsi_t']:.1f} t")
    # Electric baseline at Kilopower 10 kWe with R15-rerun audited delivery
    print(f"  Electric water radio-frequency ion   14-18 yr     7-42 t (depending on reactor era)    ~45 t")
    print()
    print("Best NTP-water cell (highest delivery):")
    feasible = [c for c in cells if c.get("feasible")]
    best = max(feasible, key=lambda c: c["delivered_chunk_t"])
    print(f"  Isp {best['isp_s']:.0f} s, chunk grappled {best['chunk_grappled_t']:.0f} t -> "
          f"delivered {best['delivered_chunk_t']:.1f} t ({best['delivery_frac']*100:.1f}%)")
    print(f"  Pre-TSI mass: {best['m0_leo_pre_tsi_t']:.0f} t")
    print()
    print(f"Result JSON: {out_dir / 'ntp_water.json'}")
    return cells


if __name__ == "__main__":
    main()
