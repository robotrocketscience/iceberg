"""Round 9 — Slow-transfer trajectory family: time-of-flight vs Earth-arrival v_infinity.

Sun-centered two-body conic mechanics for Saturn -> Earth ballistic transfers,
plus lunar gravity assist v_infinity reduction (reusing existing module), plus
powered-cruise time-of-flight estimate for any v_infinity excess that lunar GA
cannot shed.

Pre-registered hypothesis: Hohmann + single lunar GA cannot close the conops'
Case C (2.85 km/s) inbound budget; powered cruise is mandatory; round-trip
exceeds 13 years.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

from waterprop.constants import G0
from waterprop.trajectory.lunar_flyby import (
    single_flyby_braking,
    three_flyby_tour,
    V_MOON_ORBITAL,
)

# --- Heliocentric constants ---
MU_SUN_KM3_S2 = 1.32712440018e11  # km^3/s^2, standard gravitational parameter of the sun
AU_KM = 1.495978707e8             # km per AU
R_SATURN_AU = 9.5826              # Saturn semi-major axis, AU
R_EARTH_AU = 1.0
V_EARTH_CIRC_KM_S = math.sqrt(MU_SUN_KM3_S2 / (R_EARTH_AU * AU_KM))   # ≈ 29.78 km/s
V_SATURN_CIRC_KM_S = math.sqrt(MU_SUN_KM3_S2 / (R_SATURN_AU * AU_KM)) # ≈ 9.62 km/s
YEAR_S = 365.25 * 86400.0


def transfer_orbit(r_a_au: float, r_p_au: float) -> dict:
    """Sun-centered conic with given aphelion and perihelion (in AU).
    Returns semi-major axis (AU), eccentricity, period (yr)."""
    a_au = (r_a_au + r_p_au) / 2.0
    e = (r_a_au - r_p_au) / (r_a_au + r_p_au) if (r_a_au + r_p_au) > 0 else 0.0
    a_km = a_au * AU_KM
    period_s = 2.0 * math.pi * math.sqrt(a_km**3 / MU_SUN_KM3_S2)
    return {"a_au": a_au, "e": e, "period_yr": period_s / YEAR_S}


def vis_viva(r_au: float, a_au: float) -> float:
    """Spacecraft helio speed at radius r on an orbit of semi-major axis a, km/s."""
    r_km = r_au * AU_KM
    a_km = a_au * AU_KM
    return math.sqrt(MU_SUN_KM3_S2 * (2.0 / r_km - 1.0 / a_km))


def kepler_tof_from_aphelion_to_radius(r_target_au: float, a_au: float, e: float) -> float:
    """Time-of-flight (years) from aphelion (true anomaly pi) inbound to radius r_target.
    Uses Kepler's equation. Sign convention: TOF is positive going from aphelion toward
    perihelion (decreasing radius)."""
    if r_target_au >= a_au * (1 + e):
        return 0.0
    if r_target_au <= a_au * (1 - e):
        # Reached perihelion: TOF = half period.
        a_km = a_au * AU_KM
        period_s = 2.0 * math.pi * math.sqrt(a_km**3 / MU_SUN_KM3_S2)
        return (period_s / 2.0) / YEAR_S
    # Solve cos(nu) = (a(1-e^2)/r - 1)/e
    p = a_au * (1.0 - e**2)
    cos_nu = (p / r_target_au - 1.0) / e
    cos_nu = max(-1.0, min(1.0, cos_nu))
    nu = math.acos(cos_nu)
    # Inbound from aphelion -> nu is on the descending branch (pi -> 0).
    # Take nu in (0, pi); for the inbound leg from aphelion to perihelion, we want
    # nu measured from perihelion direction. Two-body: at the radius r,
    # the inbound point has true anomaly = (2*pi - nu) or nu depending on branch.
    # We want the descending branch from aphelion (nu = pi) toward perihelion (nu = 0):
    # so the relevant true anomaly is nu (positive), and TOF from aphelion = TOF(pi) - TOF(nu).
    # Convert true anomaly nu to eccentric anomaly E:
    # cos(E) = (e + cos(nu)) / (1 + e*cos(nu))
    cos_E = (e + cos_nu) / (1.0 + e * cos_nu)
    cos_E = max(-1.0, min(1.0, cos_E))
    E = math.acos(cos_E)  # in (0, pi); matches nu in (0, pi)
    # Mean anomaly: M = E - e*sin(E)
    M = E - e * math.sin(E)
    a_km = a_au * AU_KM
    n = math.sqrt(MU_SUN_KM3_S2 / a_km**3)  # rad/s
    # M at aphelion = pi. Inbound, M decreases from pi toward 0 (perihelion).
    # TOF from aphelion to current point = (pi - M) / n.
    tof_s = (math.pi - M) / n
    return tof_s / YEAR_S


def v_inf_at_earth(v_helio_sc_km_s: float, flight_path_angle_rad: float) -> float:
    """Compute v_inf at Earth given spacecraft helio velocity magnitude and the
    angle between spacecraft velocity vector and Earth's velocity vector (both
    in the helio frame).

    v_inf^2 = v_sc^2 + v_earth^2 - 2 v_sc v_earth cos(angle)
    """
    v2 = (v_helio_sc_km_s**2
          + V_EARTH_CIRC_KM_S**2
          - 2.0 * v_helio_sc_km_s * V_EARTH_CIRC_KM_S * math.cos(flight_path_angle_rad))
    return math.sqrt(max(v2, 0.0))


def flight_path_angle(r_au: float, a_au: float, e: float, inbound: bool = True) -> float:
    """Flight-path angle (radians) at radius r on orbit (a, e). Sign convention:
    positive for outbound (away from perihelion), negative for inbound. For the
    inbound leg from aphelion, the velocity vector points BELOW the local horizon
    by |gamma|.

    tan(gamma) = e*sin(nu) / (1 + e*cos(nu))
    """
    p = a_au * (1.0 - e**2)
    cos_nu = (p / r_au - 1.0) / e if e > 0 else 1.0
    cos_nu = max(-1.0, min(1.0, cos_nu))
    sin_nu = math.sqrt(max(0.0, 1.0 - cos_nu**2))
    gamma = math.atan2(e * sin_nu, 1.0 + e * cos_nu)
    return -gamma if inbound else gamma


# ============================================================================
# Sub-claim H9a/H9b: Hohmann Saturn -> Earth
# ============================================================================
def hohmann_saturn_to_earth() -> dict:
    """Classic Hohmann transfer with aphelion at Saturn, perihelion at Earth."""
    orbit = transfer_orbit(r_a_au=R_SATURN_AU, r_p_au=R_EARTH_AU)
    tof_yr = orbit["period_yr"] / 2.0
    # Perihelion velocity:
    v_perihelion = vis_viva(r_au=R_EARTH_AU, a_au=orbit["a_au"])
    # At perihelion, flight-path angle = 0 (tangential), so v_inf = |v_perihelion - v_earth|
    v_inf_earth = abs(v_perihelion - V_EARTH_CIRC_KM_S)
    return {
        "transfer_a_au": orbit["a_au"],
        "transfer_e": orbit["e"],
        "tof_yr": tof_yr,
        "v_perihelion_km_s": v_perihelion,
        "v_earth_circ_km_s": V_EARTH_CIRC_KM_S,
        "v_inf_earth_km_s": v_inf_earth,
    }


# ============================================================================
# Sub-claim H9c: slow-ballistic family
# ============================================================================
def slow_ballistic_perihelion_sweep() -> list:
    """Sweep perihelion radius in [0.3, 1.0] AU with aphelion at Saturn. Compute
    Earth-crossing TOF and v_inf at Earth.
    """
    results = []
    for r_p_au in [0.3, 0.5, 0.7, 0.85, 1.0]:
        orbit = transfer_orbit(r_a_au=R_SATURN_AU, r_p_au=r_p_au)
        if r_p_au > R_EARTH_AU:
            # Perihelion above Earth: orbit never crosses Earth's orbit.
            results.append({
                "r_p_au": r_p_au,
                "r_a_au": R_SATURN_AU,
                "reaches_earth": False,
                "note": "perihelion above Earth orbit"
            })
            continue
        tof_yr = kepler_tof_from_aphelion_to_radius(R_EARTH_AU, orbit["a_au"], orbit["e"])
        v_sc = vis_viva(r_au=R_EARTH_AU, a_au=orbit["a_au"])
        gamma = flight_path_angle(r_au=R_EARTH_AU, a_au=orbit["a_au"], e=orbit["e"], inbound=True)
        # Angle between spacecraft velocity and Earth velocity is |gamma|
        # (both are tangential at perihelion if r_p = 1, otherwise spacecraft has
        # inward radial component while Earth is purely tangential).
        v_inf = v_inf_at_earth(v_sc, abs(gamma))
        results.append({
            "r_p_au": r_p_au,
            "r_a_au": R_SATURN_AU,
            "transfer_a_au": orbit["a_au"],
            "transfer_e": orbit["e"],
            "tof_yr": tof_yr,
            "v_sc_at_earth_km_s": v_sc,
            "flight_path_angle_deg": math.degrees(gamma),
            "v_inf_earth_km_s": v_inf,
            "reaches_earth": True,
        })
    return results


def slow_ballistic_aphelion_sweep() -> list:
    """Sweep aphelion in [9.58, 20] AU with perihelion at Earth. Lower-energy
    families have aphelion *beyond* Saturn but spacecraft has to be launched on
    a different orbit; included as a sensitivity exploration.
    """
    results = []
    for r_a_au in [R_SATURN_AU, 12.0, 15.0, 20.0]:
        orbit = transfer_orbit(r_a_au=r_a_au, r_p_au=R_EARTH_AU)
        tof_yr = orbit["period_yr"] / 2.0  # half-period for r_p arrival from r_a
        v_perihelion = vis_viva(r_au=R_EARTH_AU, a_au=orbit["a_au"])
        v_inf = abs(v_perihelion - V_EARTH_CIRC_KM_S)
        results.append({
            "r_a_au": r_a_au,
            "r_p_au": R_EARTH_AU,
            "transfer_a_au": orbit["a_au"],
            "transfer_e": orbit["e"],
            "tof_yr": tof_yr,
            "v_perihelion_km_s": v_perihelion,
            "v_inf_earth_km_s": v_inf,
        })
    return results


# ============================================================================
# Sub-claim H9d/H9e: lunar gravity assist v_inf reduction
# ============================================================================
def lunar_ga_reduction_at_hohmann(v_inf_initial_km_s: float) -> dict:
    """Compute single-flyby and three-flyby v_inf reduction at Hohmann arrival
    v_inf. Uses existing waterprop.trajectory.lunar_flyby module.
    """
    single_v_out, single_dv = single_flyby_braking(
        v_inf_earth_in_km_s=v_inf_initial_km_s,
        periapsis_altitude_km=100.0,
        inclination_deg=0.0,
    )
    tour = three_flyby_tour(
        v_inf_initial_km_s=v_inf_initial_km_s,
        periapsis_altitude_km=100.0,
        inclination_deg=0.0,
    )
    return {
        "v_inf_initial_km_s": v_inf_initial_km_s,
        "single_flyby": {
            "v_inf_out_km_s": single_v_out,
            "delta_v_km_s": single_dv,
        },
        "three_flyby_tour": tour,
    }


# ============================================================================
# Sub-claim H9f: powered-cruise time-of-flight cost to shed excess v_inf
# ============================================================================
def powered_cruise_tof_to_shed_v_inf(
    delta_v_to_shed_km_s: float,
    chunk_t: float = 14.0,
    dry_t: float = 5.0,
    isp_s: float = 2000.0,
    eta: float = 0.65,
    power_kwe: float = 10.0,
    duty: float = 0.5,
) -> dict:
    """Estimate cruise time to shed delta_v_to_shed using continuous low-thrust.
    Uses initial mass = chunk + dry + reactor (5 W/kg reactor at given power).
    Tsiolkovsky for propellant mass, constant-acceleration approximation.
    """
    v_e = isp_s * G0
    reactor_t = (power_kwe * 1000.0 / 5.0) / 1000.0  # at 5 W/kg
    m0_t = chunk_t + dry_t + reactor_t
    prop_frac = 1.0 - math.exp(-delta_v_to_shed_km_s * 1000.0 / v_e)
    prop_req_t = m0_t * prop_frac
    delivered_chunk_t = max(chunk_t - prop_req_t, 0.0)
    F_N = 2.0 * eta * power_kwe * 1000.0 / v_e
    m_avg_kg = (m0_t - prop_req_t / 2.0) * 1000.0
    if F_N <= 0 or m_avg_kg <= 0:
        return {
            "delta_v_km_s": delta_v_to_shed_km_s,
            "feasible": False,
            "note": "no thrust or zero mass",
        }
    accel_avg = F_N / m_avg_kg
    cruise_required_s = (delta_v_to_shed_km_s * 1000.0) / (accel_avg * duty)
    return {
        "delta_v_km_s": delta_v_to_shed_km_s,
        "isp_s": isp_s,
        "eta": eta,
        "power_kwe": power_kwe,
        "duty": duty,
        "m0_t": m0_t,
        "reactor_t": reactor_t,
        "prop_req_t": prop_req_t,
        "delivered_chunk_t": delivered_chunk_t,
        "delivery_frac": delivered_chunk_t / chunk_t if chunk_t > 0 else 0.0,
        "thrust_N": F_N,
        "accel_avg_m_s2": accel_avg,
        "cruise_required_yr": cruise_required_s / YEAR_S,
        "feasible": delivered_chunk_t > 0.0,
    }


# ============================================================================
# Main
# ============================================================================
def main() -> dict:
    # H9a + H9b: Hohmann.
    hoh = hohmann_saturn_to_earth()

    # H9c: slow ballistic sweep.
    slow_perihelion = slow_ballistic_perihelion_sweep()
    slow_aphelion = slow_ballistic_aphelion_sweep()

    # H9d + H9e: lunar gravity assist.
    lunar_ga = lunar_ga_reduction_at_hohmann(hoh["v_inf_earth_km_s"])

    # H9f: powered cruise to shed remaining v_inf beyond lunar GA.
    v_inf_after_3_flybys = lunar_ga["three_flyby_tour"]["v_inf_final_km_s"]
    # Excess to shed = (v_inf_after_3_flybys) - target Case C (2.85 km/s)
    target_case_c_km_s = 2.85
    excess_to_shed = max(v_inf_after_3_flybys - target_case_c_km_s, 0.0)
    powered_cruise = powered_cruise_tof_to_shed_v_inf(excess_to_shed)

    # Combined inbound time-of-flight:
    inbound_tof_yr = hoh["tof_yr"] + powered_cruise["cruise_required_yr"]
    # Outbound is approximately Hohmann too (or whatever the conops uses; conops
    # quotes ~6 yr).
    outbound_tof_yr = hoh["tof_yr"]
    saturn_dwell_yr = 1.0  # conops; chunk capture window.
    round_trip_yr = outbound_tof_yr + saturn_dwell_yr + inbound_tof_yr

    # Hypothesis grading.
    grading = {
        "H9a_hohmann_tof": {
            "predicted": "5.8-6.2 yr",
            "measured": hoh["tof_yr"],
            "verdict": "held" if 5.5 <= hoh["tof_yr"] <= 6.5 else "falsified",
        },
        "H9b_hohmann_v_inf": {
            "predicted": "9.5-10.5 km/s",
            "measured": hoh["v_inf_earth_km_s"],
            "verdict": "held" if 9.0 <= hoh["v_inf_earth_km_s"] <= 11.0 else "falsified",
        },
        "H9c_no_slower_ballistic": {
            "predicted": "No ballistic with TOF > 6.05 yr arrives at v_inf < 10 km/s",
            "measured": [
                {"r_p_au": s["r_p_au"], "tof_yr": s.get("tof_yr"), "v_inf_km_s": s.get("v_inf_earth_km_s")}
                for s in slow_perihelion if s.get("reaches_earth")
            ] + [
                {"r_a_au": s["r_a_au"], "tof_yr": s.get("tof_yr"), "v_inf_km_s": s.get("v_inf_earth_km_s")}
                for s in slow_aphelion
            ],
        },
        "H9d_single_flyby_le_2_km_s": {
            "predicted": "≤ 2.0 km/s",
            "measured": lunar_ga["single_flyby"]["delta_v_km_s"],
            "verdict": "held" if lunar_ga["single_flyby"]["delta_v_km_s"] <= 2.0 else "falsified",
        },
        "H9e_hohmann_plus_ga_floor_ge_8_km_s": {
            "predicted_floor": "≥ 8 km/s after single lunar GA",
            "measured_single_flyby_v_inf_out_km_s": lunar_ga["single_flyby"]["v_inf_out_km_s"],
            "verdict": "held" if lunar_ga["single_flyby"]["v_inf_out_km_s"] >= 8.0 else "falsified",
        },
        "H9f_powered_cruise_band_1_to_3_yr": {
            "predicted": "1-3 yr powered cruise added",
            "measured_cruise_yr": powered_cruise.get("cruise_required_yr"),
            "feasible": powered_cruise.get("feasible"),
            "verdict": (
                "held" if powered_cruise.get("feasible") and
                1.0 <= powered_cruise.get("cruise_required_yr", 1e9) <= 3.0
                else ("falsified-low" if powered_cruise.get("feasible") and
                      powered_cruise.get("cruise_required_yr", 1e9) < 1.0
                      else "falsified-high")
            ),
        },
        "H9_aggregate_13_yr_case_c_inconsistent": {
            "predicted": "conops 13 yr + 2.85 km/s pair is internally inconsistent",
            "round_trip_yr_estimated": round_trip_yr,
            "verdict": "held" if round_trip_yr > 13.5 else "falsified",
        },
    }

    results = {
        "inputs": {
            "R_SATURN_AU": R_SATURN_AU,
            "R_EARTH_AU": R_EARTH_AU,
            "V_EARTH_CIRC_KM_S": V_EARTH_CIRC_KM_S,
            "V_SATURN_CIRC_KM_S": V_SATURN_CIRC_KM_S,
            "MU_SUN_KM3_S2": MU_SUN_KM3_S2,
            "TARGET_CASE_C_KM_S": target_case_c_km_s,
        },
        "hohmann": hoh,
        "slow_ballistic_perihelion_sweep": slow_perihelion,
        "slow_ballistic_aphelion_sweep": slow_aphelion,
        "lunar_gravity_assist": lunar_ga,
        "powered_cruise_to_close_case_c": powered_cruise,
        "round_trip_estimate": {
            "outbound_tof_yr": outbound_tof_yr,
            "saturn_dwell_yr": saturn_dwell_yr,
            "inbound_tof_yr": inbound_tof_yr,
            "total_yr": round_trip_yr,
            "conops_headline_yr": 13.0,
        },
        "hypothesis_grading": grading,
    }

    out_dir = Path(__file__).parent / "results"
    out_dir.mkdir(exist_ok=True)
    with (out_dir / "slow_trajectory_tof.json").open("w") as f:
        json.dump(results, f, indent=2)

    # --- Console summary ---
    print("=" * 88)
    print("R9 — Slow-transfer trajectory family: TOF vs Earth-arrival v_inf")
    print("=" * 88)
    print()
    print(f"Hohmann Saturn -> Earth:")
    print(f"  semi-major axis        : {hoh['transfer_a_au']:.3f} AU")
    print(f"  eccentricity           : {hoh['transfer_e']:.4f}")
    print(f"  time-of-flight (half-T): {hoh['tof_yr']:.3f} yr")
    print(f"  v at perihelion (Earth): {hoh['v_perihelion_km_s']:.2f} km/s")
    print(f"  v_inf at Earth arrival : {hoh['v_inf_earth_km_s']:.2f} km/s")
    print()
    print("Slow-ballistic perihelion sweep (aphelion fixed at Saturn):")
    print(f"  {'r_p':>5} {'TOF':>7} {'v_sc':>7} {'gamma':>7} {'v_inf':>7}  reaches Earth?")
    for s in slow_perihelion:
        if s.get("reaches_earth"):
            print(f"  {s['r_p_au']:>4.2f}  {s['tof_yr']:>5.2f} yr {s['v_sc_at_earth_km_s']:>5.2f} km/s "
                  f"{s['flight_path_angle_deg']:>5.1f}° {s['v_inf_earth_km_s']:>5.2f} km/s  yes")
        else:
            print(f"  {s['r_p_au']:>4.2f}                                              no  ({s['note']})")
    print()
    print("Slow-ballistic aphelion sweep (perihelion = 1 AU):")
    print(f"  {'r_a':>5} {'a':>6} {'TOF':>7} {'v_peri':>7} {'v_inf':>7}")
    for s in slow_aphelion:
        print(f"  {s['r_a_au']:>5.2f} {s['transfer_a_au']:>5.2f} {s['tof_yr']:>5.2f} yr "
              f"{s['v_perihelion_km_s']:>5.2f} km/s {s['v_inf_earth_km_s']:>5.2f} km/s")
    print()
    print("Lunar gravity assist (starting from Hohmann v_inf):")
    sf = lunar_ga["single_flyby"]
    print(f"  Single flyby     : v_inf {lunar_ga['v_inf_initial_km_s']:.2f} -> "
          f"{sf['v_inf_out_km_s']:.2f} km/s (delta-v {sf['delta_v_km_s']:.2f} km/s)")
    t3 = lunar_ga["three_flyby_tour"]
    print(f"  Three flyby tour : v_inf {t3['v_inf_initial_km_s']:.2f} -> "
          f"{t3['v_inf_final_km_s']:.2f} km/s (total delta-v {t3['total_delta_v_km_s']:.2f} km/s)")
    for fb in t3["per_flyby"]:
        print(f"    flyby {fb['flyby_number']}: {fb['v_inf_in_km_s']:.2f} -> "
              f"{fb['v_inf_out_km_s']:.2f} km/s (delta-v {fb['delta_v_km_s']:.2f} km/s)")
    print()
    print(f"After 3-flyby tour, v_inf = {v_inf_after_3_flybys:.2f} km/s.")
    print(f"To reach Case C (2.85 km/s), powered cruise must shed: {excess_to_shed:.2f} km/s")
    print()
    print("Powered cruise estimate (water radio-frequency ion, 2000 s, 10 kWe, duty 0.5):")
    pc = powered_cruise
    print(f"  initial mass            : {pc['m0_t']:.1f} t (chunk 14 + dry 5 + reactor {pc['reactor_t']:.1f})")
    print(f"  propellant required     : {pc['prop_req_t']:.2f} t")
    print(f"  delivered chunk         : {pc['delivered_chunk_t']:.2f} t ({pc['delivery_frac']*100:.1f}%)")
    print(f"  thrust                  : {pc['thrust_N']:.3f} N")
    print(f"  average acceleration    : {pc['accel_avg_m_s2']:.2e} m/s^2")
    print(f"  cruise time required    : {pc['cruise_required_yr']:.2f} yr")
    print(f"  feasible (chunk>0)?     : {pc['feasible']}")
    print()
    rt = results["round_trip_estimate"]
    print(f"Estimated round trip:")
    print(f"  outbound (Hohmann)      : {rt['outbound_tof_yr']:.2f} yr")
    print(f"  Saturn dwell            : {rt['saturn_dwell_yr']:.2f} yr")
    print(f"  inbound (Hohmann + powered cruise): {rt['inbound_tof_yr']:.2f} yr")
    print(f"  TOTAL                   : {rt['total_yr']:.2f} yr  (vs conops headline {rt['conops_headline_yr']:.0f} yr)")
    print()
    print("Hypothesis grading:")
    for h, g in grading.items():
        v = g.get("verdict", g)
        if isinstance(v, str):
            print(f"  {h:<55} {v}")
        else:
            print(f"  {h:<55} (see JSON)")
    print()
    print(f"Result JSON: {out_dir / 'slow_trajectory_tof.json'}")
    return results


if __name__ == "__main__":
    main()
