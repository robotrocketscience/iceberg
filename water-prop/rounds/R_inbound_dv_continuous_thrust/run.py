"""R-inbound-dv-continuous-thrust — does the matrix's 6.42 km/s inbound delta-velocity
hold up under continuous-thrust electric propulsion, or does the megawatt all-electric
end-to-end architecture lose level-zero requirement L0-05 compliance?

Closed-form continuous-thrust integrated delta-velocity, mirroring R-electric-outbound's
framework on the inbound leg. Four segments:

  (1) Saturn-side Edelbaum spiral from a circular bound orbit to Saturn-escape:
        integrated delta-velocity = v_circ at the starting orbit.
  (2) Heliocentric retrograde from Saturn's orbital speed to Hohmann aphelion velocity:
        paid in full at continuous-thrust (no Oberth credit).
  (3) Ballistic Hohmann cruise from Saturn to Earth: time only, no propellant.
  (4) Earth-side heliocentric decelerate from Hohmann perihelion velocity to Earth's
        orbital speed: paid in full at continuous-thrust.
  (5) Earth-side Edelbaum capture spiral from Earth-escape down to low Earth orbit:
        integrated delta-velocity = v_circ at low Earth orbit.

Lunar-gravity-assist credit is applied as an optional 2.0 km/s reduction off the Earth
phase (segments 4 plus 5 combined), reflecting what a thrust-off coast through the
lunar sphere of influence can plausibly buy under continuous-thrust electric.

Pre-registration: see STUDY.md for hypothesis H-it-a through H-it-i, locked before run.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

from waterprop.constants import (
    A_EARTH,
    A_SATURN,
    G0,
    GM_EARTH,
    GM_SATURN,
    GM_SUN,
    R_EARTH,
)


YEAR_S = 365.25 * 86400.0

# Mission constants (shared with prior rounds for cross-comparison)
LEO_ALT_KM = 400.0
SATURN_OPS_YR = 1.0
ROUND_TRIP_CEILING_YR = 15.0
ETA_THR = 0.65

# Saturn-side departure orbits to sweep
SATURN_BRING_RADIUS_KM = 1.35e5          # B-ring; conops Phase 5
SATURN_HIGH_ELLIPTICAL_KM = 1.0e6        # mid-case high-elliptical capture
SATURN_IAPETUS_DISTANCE_KM = 3.561e6     # Iapetus orbital radius (high-energy capture)

# Matrix reference number
MATRIX_INBOUND_DV_KM_S = 6.42

# Lunar gravity assist credit under continuous-thrust (thrust-off coast through lunar SOI)
LGA_CREDIT_KM_S = 2.0

# Sweep axes
REACTOR_POWERS_KWE = [100.0, 200.0, 500.0, 1000.0, 2000.0]
ISP_SWEEP_S = [2000.0, 3000.0, 4000.0]
CHUNK_SENSITIVITY_T = [100.0, 200.0, 500.0]
CHUNK_BASELINE_T = 200.0

# Outbound burn times at each reactor power (from R-electric-outbound decomposed-mid, Isp 2000 s)
# Used here for round-trip composition only. See R-electric-outbound/results/electric_outbound.json
# main_sweep rows with mass_model == "decomposed_mid".
OUTBOUND_BURN_YR_BY_KWE = {
    100.0: 0.36,    # interpolation between R-electric-outbound rows; documented in §validity
    200.0: 0.24,
    500.0: 0.18,
    1000.0: 0.17,
    2000.0: 0.16,
}

# Tug dry mass at each reactor power, decomposed-mid model from R-electric-outbound
TUG_DRY_T_BY_KWE = {
    100.0: 5.5,
    200.0: 7.5,
    500.0: 10.0,
    1000.0: 12.1,
    2000.0: 16.4,
}


def hohmann_velocities() -> dict[str, float]:
    """Compute Hohmann transfer endpoint velocities and heliocentric body speeds."""
    a_h_km = (A_EARTH + A_SATURN) / 2.0
    v_perihelion = math.sqrt(GM_SUN * (2.0 / A_EARTH - 1.0 / a_h_km))
    v_aphelion = math.sqrt(GM_SUN * (2.0 / A_SATURN - 1.0 / a_h_km))
    v_earth_helio = math.sqrt(GM_SUN / A_EARTH)
    v_saturn_helio = math.sqrt(GM_SUN / A_SATURN)
    cruise_yr = math.pi * math.sqrt(a_h_km ** 3 / GM_SUN) / YEAR_S
    return {
        "a_hohmann_km": a_h_km,
        "v_hohmann_perihelion_km_s": v_perihelion,
        "v_hohmann_aphelion_km_s": v_aphelion,
        "v_earth_helio_km_s": v_earth_helio,
        "v_saturn_helio_km_s": v_saturn_helio,
        "v_inf_at_earth_km_s": v_perihelion - v_earth_helio,
        "v_inf_at_saturn_km_s": v_saturn_helio - v_aphelion,
        "hohmann_cruise_yr": cruise_yr,
    }


def saturn_spiral_dv_km_s(r_dep_km: float) -> float:
    """Edelbaum spiral integrated delta-velocity from circular Saturn orbit to escape.

    Equal to the starting circular orbital speed under the planar tangential-thrust
    closed-form (Edelbaum 1961).
    """
    return math.sqrt(GM_SATURN / r_dep_km)


def leo_spiral_dv_km_s() -> float:
    """Edelbaum capture spiral integrated delta-velocity from Earth-escape down to LEO.

    By time-reversal symmetry with the outbound spiral, equal to v_circ at LEO altitude.
    """
    return math.sqrt(GM_EARTH / (R_EARTH + LEO_ALT_KM))


def inbound_dv_decomposition(r_saturn_dep_km: float,
                              lga_credit_km_s: float = 0.0) -> dict:
    """Decompose the continuous-thrust inbound integrated delta-velocity into segments.

    Segments:
      (1) Saturn spiral-out from circular bound orbit at r_saturn_dep_km
      (2) Saturn-side heliocentric retrograde (Saturn orbital speed → Hohmann aphelion)
      (4) Earth-side heliocentric decelerate (Hohmann perihelion → Earth orbital speed)
      (5) Earth-side Edelbaum capture spiral (Earth-escape → low Earth orbit)

    Segment (3) is ballistic cruise; not part of delta-velocity ledger.

    Lunar gravity assist credit is subtracted from the (4) + (5) Earth-side sum.
    """
    helio = hohmann_velocities()
    dv1_saturn_spiral = saturn_spiral_dv_km_s(r_saturn_dep_km)
    dv2_saturn_helio = helio["v_inf_at_saturn_km_s"]
    dv4_earth_helio = helio["v_inf_at_earth_km_s"]
    dv5_leo_spiral = leo_spiral_dv_km_s()
    dv_earth_combined = dv4_earth_helio + dv5_leo_spiral
    dv_earth_after_lga = max(0.0, dv_earth_combined - lga_credit_km_s)
    dv_total = dv1_saturn_spiral + dv2_saturn_helio + dv_earth_after_lga
    return {
        "r_saturn_dep_km": r_saturn_dep_km,
        "lga_credit_km_s": lga_credit_km_s,
        "dv1_saturn_spiral_km_s": dv1_saturn_spiral,
        "dv2_saturn_helio_km_s": dv2_saturn_helio,
        "dv4_earth_helio_km_s": dv4_earth_helio,
        "dv5_leo_spiral_km_s": dv5_leo_spiral,
        "dv_earth_combined_pre_lga_km_s": dv_earth_combined,
        "dv_earth_after_lga_km_s": dv_earth_after_lga,
        "dv_total_km_s": dv_total,
    }


def constant_thrust_burn(m_initial_t: float, dv_km_s: float, power_kwe: float,
                          isp_s: float, eta: float = ETA_THR) -> dict:
    """Propellant mass and burn time for a constant-thrust electric burn.

    Tsiolkovsky for propellant; constant-thrust approximation for burn time
    (thrust held while mass decreases). Matches R-electric-outbound formulation.
    """
    v_e_m_s = isp_s * G0
    thrust_n = 2.0 * eta * power_kwe * 1000.0 / v_e_m_s
    mass_ratio = math.exp(dv_km_s * 1000.0 / v_e_m_s)
    m_prop_t = m_initial_t * (1.0 - 1.0 / mass_ratio)
    t_burn_s = m_prop_t * 1000.0 * v_e_m_s / thrust_n
    return {
        "thrust_N": thrust_n,
        "m_prop_t": m_prop_t,
        "mass_ratio": mass_ratio,
        "t_burn_s": t_burn_s,
        "t_burn_yr": t_burn_s / YEAR_S,
    }


def round_trip_at(power_kwe: float, isp_s: float, chunk_t: float,
                   dv_inbound_km_s: float) -> dict:
    """Compose a round-trip timeline for a given (power, isp, chunk, inbound delta-v)."""
    m_tug_t = TUG_DRY_T_BY_KWE[power_kwe]
    burn_in = constant_thrust_burn(m_tug_t + chunk_t, dv_inbound_km_s, power_kwe, isp_s)
    delivered_t = chunk_t - burn_in["m_prop_t"]
    delivered_frac = max(0.0, delivered_t) / chunk_t
    t_out_yr = OUTBOUND_BURN_YR_BY_KWE[power_kwe]
    t_cruise_yr = hohmann_velocities()["hohmann_cruise_yr"]
    round_trip_yr = (
        t_out_yr + t_cruise_yr + SATURN_OPS_YR + burn_in["t_burn_yr"] + t_cruise_yr
    )
    return {
        "power_kwe": power_kwe,
        "isp_s": isp_s,
        "chunk_t": chunk_t,
        "dv_inbound_km_s": dv_inbound_km_s,
        "m_tug_t": m_tug_t,
        "mass_ratio": burn_in["mass_ratio"],
        "m_prop_inbound_t": burn_in["m_prop_t"],
        "delivered_t": max(0.0, delivered_t),
        "delivered_frac": delivered_frac,
        "thrust_N": burn_in["thrust_N"],
        "t_outbound_burn_yr": t_out_yr,
        "t_cruise_each_yr": t_cruise_yr,
        "t_saturn_ops_yr": SATURN_OPS_YR,
        "t_inbound_burn_yr": burn_in["t_burn_yr"],
        "round_trip_yr": round_trip_yr,
        "closes_15yr": round_trip_yr <= ROUND_TRIP_CEILING_YR,
    }


def main() -> dict:
    results: dict = {}

    # 1. Hohmann velocity baseline and Edelbaum/spiral endpoints
    helio = hohmann_velocities()
    results["hohmann_baseline"] = helio
    results["leo_spiral_dv_km_s"] = leo_spiral_dv_km_s()

    # 2. Delta-velocity decomposition under three Saturn-departure orbits, no LGA
    saturn_dep_cases = {
        "B_ring": SATURN_BRING_RADIUS_KM,
        "high_elliptical_1Mkm": SATURN_HIGH_ELLIPTICAL_KM,
        "Iapetus_distance": SATURN_IAPETUS_DISTANCE_KM,
    }
    dv_no_lga = {name: inbound_dv_decomposition(r, lga_credit_km_s=0.0)
                 for name, r in saturn_dep_cases.items()}
    results["dv_decomposition_no_lga"] = dv_no_lga

    # 3. Same with LGA credit applied
    dv_with_lga = {name: inbound_dv_decomposition(r, lga_credit_km_s=LGA_CREDIT_KM_S)
                   for name, r in saturn_dep_cases.items()}
    results["dv_decomposition_with_lga"] = dv_with_lga

    # 4. Headline continuous-thrust inbound delta-velocity numbers
    dv_headline = {
        "B_ring_no_lga_km_s": dv_no_lga["B_ring"]["dv_total_km_s"],
        "B_ring_with_lga_km_s": dv_with_lga["B_ring"]["dv_total_km_s"],
        "high_elliptical_no_lga_km_s": dv_no_lga["high_elliptical_1Mkm"]["dv_total_km_s"],
        "high_elliptical_with_lga_km_s": dv_with_lga["high_elliptical_1Mkm"]["dv_total_km_s"],
        "Iapetus_no_lga_km_s": dv_no_lga["Iapetus_distance"]["dv_total_km_s"],
        "Iapetus_with_lga_km_s": dv_with_lga["Iapetus_distance"]["dv_total_km_s"],
        "matrix_assumed_km_s": MATRIX_INBOUND_DV_KM_S,
    }
    results["dv_headline"] = dv_headline

    # 5. Megawatt all-electric end-to-end round trip under each delta-velocity case
    #    Chunk 200 t baseline; Isp 2000 s baseline; reactor 1000 kWe
    megawatt_round_trip_cases = {}
    for case_label, dv_block in [
        ("matrix_6_42", MATRIX_INBOUND_DV_KM_S),
        ("B_ring_no_lga", dv_no_lga["B_ring"]["dv_total_km_s"]),
        ("B_ring_with_lga", dv_with_lga["B_ring"]["dv_total_km_s"]),
        ("high_elliptical_no_lga", dv_no_lga["high_elliptical_1Mkm"]["dv_total_km_s"]),
        ("high_elliptical_with_lga", dv_with_lga["high_elliptical_1Mkm"]["dv_total_km_s"]),
        ("Iapetus_no_lga", dv_no_lga["Iapetus_distance"]["dv_total_km_s"]),
        ("Iapetus_with_lga", dv_with_lga["Iapetus_distance"]["dv_total_km_s"]),
    ]:
        megawatt_round_trip_cases[case_label] = round_trip_at(
            power_kwe=1000.0, isp_s=2000.0, chunk_t=CHUNK_BASELINE_T,
            dv_inbound_km_s=dv_block,
        )
    results["megawatt_round_trip_cases"] = megawatt_round_trip_cases

    # 6. Power sensitivity at high-elliptical Saturn departure with LGA
    #    (the most-favorable architecture configuration for continuous-thrust)
    dv_best_continuous = dv_with_lga["high_elliptical_1Mkm"]["dv_total_km_s"]
    power_sweep = []
    for power in REACTOR_POWERS_KWE:
        row = round_trip_at(power_kwe=power, isp_s=2000.0, chunk_t=CHUNK_BASELINE_T,
                             dv_inbound_km_s=dv_best_continuous)
        power_sweep.append(row)
    results["power_sweep_best_dv_continuous"] = power_sweep

    # 7. Isp sensitivity at 1000 kWe, high-elliptical with LGA, chunk 200 t
    isp_sweep = []
    for isp in ISP_SWEEP_S:
        row = round_trip_at(power_kwe=1000.0, isp_s=isp, chunk_t=CHUNK_BASELINE_T,
                             dv_inbound_km_s=dv_best_continuous)
        isp_sweep.append(row)
    results["isp_sweep_1mwe_best_dv"] = isp_sweep

    # 8. Chunk sensitivity at 1000 kWe, Isp 2000 s, high-elliptical with LGA
    chunk_sweep = []
    for chunk in CHUNK_SENSITIVITY_T:
        row = round_trip_at(power_kwe=1000.0, isp_s=2000.0, chunk_t=chunk,
                             dv_inbound_km_s=dv_best_continuous)
        chunk_sweep.append(row)
    results["chunk_sweep_1mwe_best_dv"] = chunk_sweep

    # 9. Hypothesis grading
    dv_block_b_no_lga = dv_no_lga["B_ring"]
    dv_total_b_no = dv_block_b_no_lga["dv_total_km_s"]
    dv_total_b_lga = dv_with_lga["B_ring"]["dv_total_km_s"]
    megawatt_b_lga = round_trip_at(1000.0, 2000.0, CHUNK_BASELINE_T,
                                    dv_with_lga["B_ring"]["dv_total_km_s"])
    megawatt_he_lga = round_trip_at(1000.0, 2000.0, CHUNK_BASELINE_T,
                                     dv_with_lga["high_elliptical_1Mkm"]["dv_total_km_s"])

    def in_band(value: float, low: float, high: float) -> bool:
        return low <= value <= high

    grading = {
        "H_it_a": {
            "predicted_band_km_s": [14.0, 18.0],
            "actual_km_s": dv_block_b_no_lga["dv1_saturn_spiral_km_s"],
            "held": in_band(dv_block_b_no_lga["dv1_saturn_spiral_km_s"], 14.0, 18.0),
        },
        "H_it_b": {
            "predicted_band_km_s": [5.0, 5.8],
            "actual_km_s": dv_block_b_no_lga["dv2_saturn_helio_km_s"],
            "held": in_band(dv_block_b_no_lga["dv2_saturn_helio_km_s"], 5.0, 5.8),
        },
        "H_it_c": {
            "predicted_band_km_s": [10.0, 10.6],
            "actual_km_s": dv_block_b_no_lga["dv4_earth_helio_km_s"],
            "held": in_band(dv_block_b_no_lga["dv4_earth_helio_km_s"], 10.0, 10.6),
        },
        "H_it_d": {
            "predicted_band_km_s": [7.5, 7.9],
            "actual_km_s": dv_block_b_no_lga["dv5_leo_spiral_km_s"],
            "held": in_band(dv_block_b_no_lga["dv5_leo_spiral_km_s"], 7.5, 7.9),
        },
        "H_it_e": {
            "predicted_band_km_s": [36.0, 42.0],
            "actual_km_s": dv_total_b_no,
            "held": in_band(dv_total_b_no, 36.0, 42.0),
        },
        "H_it_f": {
            "predicted_band_km_s": [34.0, 40.0],
            "actual_km_s": dv_total_b_lga,
            "held": in_band(dv_total_b_lga, 34.0, 40.0),
        },
        "H_it_g_doubled_from_impulsive": {
            "predicted_band_km_s": [10.0, 14.0],
            "actual_km_s_b_ring": dv_total_b_no,
            "actual_km_s_high_elliptical": dv_no_lga["high_elliptical_1Mkm"]["dv_total_km_s"],
            "held": in_band(dv_total_b_no, 10.0, 14.0),
            "load_bearing_falsified_high": dv_total_b_no > 20.0,
        },
        "H_it_h_megawatt_round_trip": {
            "predicted_max_yr": 15.5,
            "actual_yr_B_ring_with_lga": megawatt_b_lga["round_trip_yr"],
            "actual_yr_high_elliptical_with_lga": megawatt_he_lga["round_trip_yr"],
            "held_B_ring": megawatt_b_lga["round_trip_yr"] <= 15.5,
            "held_high_elliptical": megawatt_he_lga["round_trip_yr"] <= 15.5,
            "load_bearing_falsified": megawatt_b_lga["round_trip_yr"] > 16.0
                                      and megawatt_he_lga["round_trip_yr"] > 16.0,
        },
        "H_it_i_delivered_fraction": {
            "predicted_band": [0.25, 0.55],
            "actual_B_ring_with_lga": megawatt_b_lga["delivered_frac"],
            "actual_high_elliptical_with_lga": megawatt_he_lga["delivered_frac"],
            "held_B_ring": in_band(megawatt_b_lga["delivered_frac"], 0.25, 0.55),
            "held_high_elliptical": in_band(megawatt_he_lga["delivered_frac"], 0.25, 0.55),
            "load_bearing_falsified": (megawatt_b_lga["delivered_frac"] < 0.10
                                       and megawatt_he_lga["delivered_frac"] < 0.10),
        },
    }
    results["hypothesis_grading"] = grading

    # Write JSON
    results_dir = Path(__file__).parent / "results"
    results_dir.mkdir(exist_ok=True)
    (results_dir / "inbound_dv_continuous.json").write_text(
        json.dumps(results, indent=2, default=str)
    )

    # Tables
    lines: list[str] = []
    lines.append("### Hohmann baseline and spiral endpoints\n")
    lines.append(f"- Hohmann perihelion velocity at Earth: {helio['v_hohmann_perihelion_km_s']:.3f} km/s")
    lines.append(f"- Hohmann aphelion velocity at Saturn: {helio['v_hohmann_aphelion_km_s']:.3f} km/s")
    lines.append(f"- Earth heliocentric orbital speed: {helio['v_earth_helio_km_s']:.3f} km/s")
    lines.append(f"- Saturn heliocentric orbital speed: {helio['v_saturn_helio_km_s']:.3f} km/s")
    lines.append(f"- Velocity-at-infinity at Earth from Hohmann return: {helio['v_inf_at_earth_km_s']:.3f} km/s")
    lines.append(f"- Velocity-at-infinity at Saturn from Hohmann return: {helio['v_inf_at_saturn_km_s']:.3f} km/s")
    lines.append(f"- Low-Earth-orbit Edelbaum capture spiral integrated delta-velocity: {leo_spiral_dv_km_s():.3f} km/s")
    lines.append(f"- Hohmann cruise time, each way: {helio['hohmann_cruise_yr']:.2f} years\n")

    lines.append("\n### Continuous-thrust inbound delta-velocity decomposition (no lunar gravity assist credit)\n")
    lines.append("| Saturn departure | Saturn spiral | Saturn helio | Earth helio | LEO spiral | Total |")
    lines.append("|---|---:|---:|---:|---:|---:|")
    for name, blk in dv_no_lga.items():
        lines.append(
            f"| {name} (r = {blk['r_saturn_dep_km']:.2e} km) | "
            f"{blk['dv1_saturn_spiral_km_s']:.2f} | "
            f"{blk['dv2_saturn_helio_km_s']:.2f} | "
            f"{blk['dv4_earth_helio_km_s']:.2f} | "
            f"{blk['dv5_leo_spiral_km_s']:.2f} | "
            f"**{blk['dv_total_km_s']:.2f}** km/s |"
        )

    lines.append("\n### With lunar gravity assist credit (2.0 km/s shaved off Earth phase)\n")
    lines.append("| Saturn departure | Saturn spiral | Saturn helio | Earth phase post-LGA | Total |")
    lines.append("|---|---:|---:|---:|---:|")
    for name, blk in dv_with_lga.items():
        lines.append(
            f"| {name} | {blk['dv1_saturn_spiral_km_s']:.2f} | "
            f"{blk['dv2_saturn_helio_km_s']:.2f} | "
            f"{blk['dv_earth_after_lga_km_s']:.2f} | "
            f"**{blk['dv_total_km_s']:.2f}** km/s |"
        )

    lines.append("\n### Headline comparison — matrix value versus continuous-thrust\n")
    lines.append("| Case | Inbound delta-velocity (km/s) | Multiple of matrix 6.42 |")
    lines.append("|---|---:|---:|")
    lines.append(f"| Matrix assumed | {MATRIX_INBOUND_DV_KM_S:.2f} | 1.00× |")
    for label, val in dv_headline.items():
        if label.endswith("_km_s") and label != "matrix_assumed_km_s":
            lines.append(f"| {label.replace('_km_s', '').replace('_', ' ')} | {val:.2f} | {val / MATRIX_INBOUND_DV_KM_S:.2f}× |")

    lines.append("\n### Megawatt all-electric end-to-end round-trip under each delta-velocity case\n")
    lines.append("Reactor 1000 kWe, Isp 2000 s, chunk 200 t. Outbound + 2× cruise + Saturn ops + inbound.\n")
    lines.append("| Case | dv_inbound (km/s) | mass ratio | m_prop (t) | delivered (t) | t_inbound (yr) | round-trip (yr) | closes 15 yr? |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|:--:|")
    for label, row in megawatt_round_trip_cases.items():
        flag = "**yes**" if row["closes_15yr"] else "**no**"
        lines.append(
            f"| {label} | {row['dv_inbound_km_s']:.2f} | {row['mass_ratio']:.2f} | "
            f"{row['m_prop_inbound_t']:.1f} | {row['delivered_t']:.1f} | "
            f"{row['t_inbound_burn_yr']:.2f} | {row['round_trip_yr']:.2f} | {flag} |"
        )

    lines.append("\n### Power sensitivity at most-favorable continuous-thrust architecture (high-elliptical Saturn departure with lunar gravity assist credit)\n")
    lines.append(f"Inbound delta-velocity = {dv_best_continuous:.2f} km/s. Isp 2000 s, chunk 200 t.\n")
    lines.append("| Reactor (kWe) | m_tug (t) | m_prop (t) | delivered (t) | delivered frac | t_inbound (yr) | round-trip (yr) | closes 15 yr? |")
    lines.append("|---:|---:|---:|---:|---:|---:|---:|:--:|")
    for row in power_sweep:
        flag = "**yes**" if row["closes_15yr"] else "**no**"
        lines.append(
            f"| {row['power_kwe']:.0f} | {row['m_tug_t']:.1f} | "
            f"{row['m_prop_inbound_t']:.1f} | {row['delivered_t']:.1f} | "
            f"{row['delivered_frac']*100:.1f}% | "
            f"{row['t_inbound_burn_yr']:.2f} | {row['round_trip_yr']:.2f} | {flag} |"
        )

    lines.append("\n### Specific-impulse sensitivity at 1000 kWe, high-elliptical with LGA, chunk 200 t\n")
    lines.append("| Isp (s) | mass ratio | m_prop (t) | delivered frac | t_inbound (yr) | round-trip (yr) | closes 15 yr? |")
    lines.append("|---:|---:|---:|---:|---:|---:|:--:|")
    for row in isp_sweep:
        flag = "**yes**" if row["closes_15yr"] else "**no**"
        lines.append(
            f"| {row['isp_s']:.0f} | {row['mass_ratio']:.2f} | "
            f"{row['m_prop_inbound_t']:.1f} | {row['delivered_frac']*100:.1f}% | "
            f"{row['t_inbound_burn_yr']:.2f} | {row['round_trip_yr']:.2f} | {flag} |"
        )

    lines.append("\n### Chunk-mass sensitivity at 1000 kWe, Isp 2000 s, high-elliptical with LGA\n")
    lines.append("| Chunk (t) | m_prop (t) | delivered (t) | delivered frac | t_inbound (yr) | round-trip (yr) | closes 15 yr? |")
    lines.append("|---:|---:|---:|---:|---:|---:|:--:|")
    for row in chunk_sweep:
        flag = "**yes**" if row["closes_15yr"] else "**no**"
        lines.append(
            f"| {row['chunk_t']:.0f} | {row['m_prop_inbound_t']:.1f} | "
            f"{row['delivered_t']:.1f} | {row['delivered_frac']*100:.1f}% | "
            f"{row['t_inbound_burn_yr']:.2f} | {row['round_trip_yr']:.2f} | {flag} |"
        )

    lines.append("\n### Hypothesis grading\n")
    g = grading
    lines.append("| Sub-claim | Predicted | Actual | Held? |")
    lines.append("|---|---|---|---|")
    lines.append(f"| H-it-a — Saturn spiral-out (B-ring) | {g['H_it_a']['predicted_band_km_s']} km/s | "
                 f"{g['H_it_a']['actual_km_s']:.2f} km/s | {'yes' if g['H_it_a']['held'] else '**no**'} |")
    lines.append(f"| H-it-b — Saturn-side heliocentric drop | {g['H_it_b']['predicted_band_km_s']} km/s | "
                 f"{g['H_it_b']['actual_km_s']:.2f} km/s | {'yes' if g['H_it_b']['held'] else '**no**'} |")
    lines.append(f"| H-it-c — Earth-side heliocentric drop | {g['H_it_c']['predicted_band_km_s']} km/s | "
                 f"{g['H_it_c']['actual_km_s']:.2f} km/s | {'yes' if g['H_it_c']['held'] else '**no**'} |")
    lines.append(f"| H-it-d — Earth Edelbaum capture spiral | {g['H_it_d']['predicted_band_km_s']} km/s | "
                 f"{g['H_it_d']['actual_km_s']:.2f} km/s | {'yes' if g['H_it_d']['held'] else '**no**'} |")
    lines.append(f"| H-it-e — Total dv, B-ring no LGA | {g['H_it_e']['predicted_band_km_s']} km/s | "
                 f"{g['H_it_e']['actual_km_s']:.2f} km/s | {'yes' if g['H_it_e']['held'] else '**no**'} |")
    lines.append(f"| H-it-f — Total dv, B-ring with LGA | {g['H_it_f']['predicted_band_km_s']} km/s | "
                 f"{g['H_it_f']['actual_km_s']:.2f} km/s | {'yes' if g['H_it_f']['held'] else '**no**'} |")
    lines.append(f"| H-it-g — Doubled-from-impulsive (10–14) | {g['H_it_g_doubled_from_impulsive']['predicted_band_km_s']} km/s | "
                 f"B-ring {g['H_it_g_doubled_from_impulsive']['actual_km_s_b_ring']:.2f}, "
                 f"high-elliptical {g['H_it_g_doubled_from_impulsive']['actual_km_s_high_elliptical']:.2f} km/s | "
                 f"{'yes' if g['H_it_g_doubled_from_impulsive']['held'] else '**no** (load-bearing falsified high: '
                 + str(g['H_it_g_doubled_from_impulsive']['load_bearing_falsified_high']) + ')'} |")
    lines.append(f"| H-it-h — Megawatt round-trip ≤ 15.5 yr | "
                 f"≤ {g['H_it_h_megawatt_round_trip']['predicted_max_yr']} yr | "
                 f"B-ring/LGA {g['H_it_h_megawatt_round_trip']['actual_yr_B_ring_with_lga']:.2f} yr, "
                 f"high-elliptical/LGA {g['H_it_h_megawatt_round_trip']['actual_yr_high_elliptical_with_lga']:.2f} yr | "
                 f"B-ring: {'yes' if g['H_it_h_megawatt_round_trip']['held_B_ring'] else '**no**'}; "
                 f"high-elliptical: {'yes' if g['H_it_h_megawatt_round_trip']['held_high_elliptical'] else '**no**'} |")
    lines.append(f"| H-it-i — Delivered fraction 25–55% | "
                 f"{[int(v*100) for v in g['H_it_i_delivered_fraction']['predicted_band']]}% | "
                 f"B-ring/LGA {g['H_it_i_delivered_fraction']['actual_B_ring_with_lga']*100:.1f}%, "
                 f"high-elliptical/LGA {g['H_it_i_delivered_fraction']['actual_high_elliptical_with_lga']*100:.1f}% | "
                 f"B-ring: {'yes' if g['H_it_i_delivered_fraction']['held_B_ring'] else '**no**'}; "
                 f"high-elliptical: {'yes' if g['H_it_i_delivered_fraction']['held_high_elliptical'] else '**no**'} |")

    (results_dir / "tables.md").write_text("\n".join(lines))
    return results


if __name__ == "__main__":
    out = main()
    print("R-inbound-dv-continuous-thrust complete.")
    print()
    print("  Continuous-thrust inbound delta-velocity (no LGA):")
    for name, blk in out["dv_decomposition_no_lga"].items():
        print(f"    {name:30s}: {blk['dv_total_km_s']:6.2f} km/s "
              f"({blk['dv_total_km_s']/MATRIX_INBOUND_DV_KM_S:.2f}× the matrix's 6.42 km/s)")
    print()
    print("  With LGA credit of 2.0 km/s:")
    for name, blk in out["dv_decomposition_with_lga"].items():
        print(f"    {name:30s}: {blk['dv_total_km_s']:6.2f} km/s "
              f"({blk['dv_total_km_s']/MATRIX_INBOUND_DV_KM_S:.2f}×)")
    print()
    print("  Megawatt all-electric round-trip:")
    for label, row in out["megawatt_round_trip_cases"].items():
        flag = "CLOSES" if row["closes_15yr"] else "BURSTS"
        print(f"    {label:30s}: {row['round_trip_yr']:6.2f} yr "
              f"(delivered {row['delivered_frac']*100:5.1f}%) [{flag} 15 yr]")
    print()
    print("  Hypothesis grading:")
    for k, v in out["hypothesis_grading"].items():
        held_field = v.get("held")
        if held_field is None:
            # Composite hypothesis with multiple held flags
            held_str = ", ".join(f"{kk}={vv}" for kk, vv in v.items()
                                 if kk.startswith("held"))
            print(f"    {k}: {held_str}")
        else:
            print(f"    {k}: {'held' if held_field else 'FALSIFIED'}")
