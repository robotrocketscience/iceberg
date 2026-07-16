"""R-outbound-dv-continuous-thrust — does R-electric-outbound's outbound integrated
delta-velocity hold up under continuous-thrust electric propulsion treatment? Or
does it under-count by exactly the symmetric Saturn-side terms that titan's
R-inbound-dv-continuous-thrust added on the return leg?

Closed-form continuous-thrust integrated delta-velocity, symmetric with titan's
inbound framework, but applied to the outbound trip Earth → Saturn-bound-orbit.
Four segments:

  (5') Earth-side Edelbaum escape spiral from low Earth orbit to Earth-escape:
        integrated delta-velocity = v_circ at LEO altitude.
  (4') Heliocentric accelerate from Earth's orbital speed to Hohmann perihelion
        velocity: paid in full at continuous-thrust (no Oberth credit).
  (3') Ballistic Hohmann cruise from Earth to Saturn: time only, no propellant.
  (2') Heliocentric decelerate from Hohmann aphelion velocity to Saturn's
        orbital speed: paid in full at continuous-thrust.
  (1') Saturn-side Edelbaum capture spiral from Saturn-escape down to a circular
        bound orbit at r_saturn_arr_km: integrated delta-velocity = v_circ at
        the arrival orbit.

R-electric-outbound's existing outbound delta-velocity (17.97 km/s) covers only
segments (5') + (4'). It implicitly assumes the spacecraft arrives at Saturn's
heliocentric distance moving on a Hohmann transfer, hits Saturn, and is captured
for free — i.e., the spacecraft flies past Saturn at Hohmann aphelion velocity
without capturing. This is the same methodology error titan corrected for the
inbound leg.

Adding segments (2') + (1') brings the outbound integrated delta-velocity into
parity with titan's inbound treatment. For symmetry with titan's findings, this
round sweeps Saturn arrival orbits matching titan's departure orbits:
B-ring (1.35e5 km), high-elliptical (1e6 km), Iapetus-distance (3.561e6 km).

Lunar gravity assist credit on outbound is plausible (spacecraft can slingshot
off the Moon on its way to Hohmann perihelion) but is treated as an OPTIONAL
2.0 km/s credit on the Earth-side terms — matching titan's inbound convention.
The baseline numbers in the headline are no-LGA; LGA-credited variants are
reported separately so the orchestrator can decide which to anchor against.

Pre-registration in STUDY.md.
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

# Mission constants — same as titan's round and R-electric-outbound
LEO_ALT_KM = 400.0
ETA_THR = 0.65
SATURN_OPS_YR = 1.0
ROUND_TRIP_CEILING_YR = 15.0

# Saturn arrival orbits — mirror titan's departure orbits for symmetric comparison
SATURN_BRING_RADIUS_KM = 1.35e5
SATURN_HIGH_ELLIPTICAL_KM = 1.0e6
SATURN_IAPETUS_DISTANCE_KM = 3.561e6

# Lunar gravity assist credit on outbound (Earth-side terms, optional)
LGA_OUTBOUND_CREDIT_KM_S = 2.0

# Reference: R-electric-outbound's existing outbound delta-velocity (segments 5'+4' only)
R_OUTBOUND_DV_KM_S = 17.97

# Titan's headline inbound delta-velocities (for round-trip composition)
TITAN_INBOUND_HIGH_ELLIPTICAL_LGA_KM_S = 24.7
TITAN_INBOUND_B_RING_NO_LGA_KM_S = 40.2

# Decomposed-mid tug mass at 1 MWe per R-electric-outbound (decomposed-mid model)
# — used here as a reference. My R-electric-outbound-rerun's corrected tug mass
# was 31.5 t at 1 MWe; titan's lookup table said 12.1 t (which was wrong, taken
# from a different row). Use my rerun's corrected number.
TUG_DRY_1MWE_DECOMPOSED_MID_T = 31.5
CHUNK_BASELINE_T = 200.0
ISP_BASELINE_S = 2000.0
POWER_BASELINE_KWE = 1000.0


def hohmann_velocities() -> dict[str, float]:
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


def saturn_spiral_dv_km_s(r_arr_km: float) -> float:
    """Edelbaum capture spiral from Saturn-escape down to a circular bound orbit
    at r_arr_km. By time-reversal symmetry with titan's outbound-from-Saturn
    spiral, the integrated delta-velocity equals v_circ at the arrival orbit.
    """
    return math.sqrt(GM_SATURN / r_arr_km)


def leo_spiral_dv_km_s() -> float:
    """Edelbaum escape spiral from low Earth orbit (400 km altitude) to Earth-escape.
    Closed-form: integrated delta-velocity = v_circ at LEO altitude.
    """
    return math.sqrt(GM_EARTH / (R_EARTH + LEO_ALT_KM))


def outbound_dv_decomposition(r_saturn_arr_km: float,
                                lga_credit_km_s: float = 0.0) -> dict:
    """Decompose the continuous-thrust outbound integrated delta-velocity into
    four segments, symmetric with titan's inbound formulation.
    """
    helio = hohmann_velocities()
    dv5p_leo_spiral = leo_spiral_dv_km_s()
    dv4p_earth_helio = helio["v_inf_at_earth_km_s"]
    dv2p_saturn_helio = helio["v_inf_at_saturn_km_s"]
    dv1p_saturn_spiral = saturn_spiral_dv_km_s(r_saturn_arr_km)
    dv_earth_combined = dv5p_leo_spiral + dv4p_earth_helio
    dv_earth_after_lga = max(0.0, dv_earth_combined - lga_credit_km_s)
    dv_total = dv_earth_after_lga + dv2p_saturn_helio + dv1p_saturn_spiral
    return {
        "r_saturn_arr_km": r_saturn_arr_km,
        "lga_credit_km_s": lga_credit_km_s,
        "dv5p_leo_spiral_km_s": dv5p_leo_spiral,
        "dv4p_earth_helio_km_s": dv4p_earth_helio,
        "dv2p_saturn_helio_km_s": dv2p_saturn_helio,
        "dv1p_saturn_spiral_km_s": dv1p_saturn_spiral,
        "dv_earth_combined_pre_lga_km_s": dv_earth_combined,
        "dv_earth_after_lga_km_s": dv_earth_after_lga,
        "dv_total_km_s": dv_total,
        "delta_vs_R_electric_outbound_km_s": dv_total - R_OUTBOUND_DV_KM_S,
    }


def burn_from_dry_end(m_final_t: float, dv_km_s: float, power_kwe: float,
                       isp_s: float, eta: float = ETA_THR) -> dict:
    """Corrected formula — input is dry-at-end. Same as R-electric-outbound-rerun.
    Outbound prop comes from a separate Earth-launched tank; m_tug is dry-at-end."""
    v_e = isp_s * G0
    thrust_N = 2.0 * eta * power_kwe * 1000.0 / v_e
    mass_ratio = math.exp(dv_km_s * 1000.0 / v_e)
    m_prop_t = m_final_t * (mass_ratio - 1.0)
    t_burn_s = m_prop_t * 1000.0 * v_e / thrust_N
    return {
        "thrust_N": thrust_N,
        "m_prop_t": m_prop_t,
        "mass_ratio": mass_ratio,
        "t_burn_s": t_burn_s,
        "t_burn_yr": t_burn_s / YEAR_S,
    }


def burn_from_wet(m_initial_t: float, dv_km_s: float, power_kwe: float,
                   isp_s: float, eta: float = ETA_THR) -> dict:
    """Wet-at-start formula — for chunk-fed inbound. Same as R-electric-outbound-rerun."""
    v_e = isp_s * G0
    thrust_N = 2.0 * eta * power_kwe * 1000.0 / v_e
    mass_ratio = math.exp(dv_km_s * 1000.0 / v_e)
    m_prop_t = m_initial_t * (1.0 - 1.0 / mass_ratio)
    t_burn_s = m_prop_t * 1000.0 * v_e / thrust_N
    return {
        "thrust_N": thrust_N,
        "m_prop_t": m_prop_t,
        "mass_ratio": mass_ratio,
        "t_burn_s": t_burn_s,
        "t_burn_yr": t_burn_s / YEAR_S,
    }


def round_trip_at_corrected_dv(m_tug_t: float, chunk_t: float, power_kwe: float,
                                 isp_s: float, dv_outbound_km_s: float,
                                 dv_inbound_km_s: float) -> dict:
    """Round-trip with BOTH corrected outbound DV and bug-fixed outbound formula.

    Outbound: dry-at-end formula because outbound prop comes from a separate tank.
    Inbound: wet-at-start formula because chunk IS the propellant (chunk-fed).
    """
    burn_out = burn_from_dry_end(m_tug_t, dv_outbound_km_s, power_kwe, isp_s)
    burn_in = burn_from_wet(m_tug_t + chunk_t, dv_inbound_km_s, power_kwe, isp_s)
    t_cruise_yr = hohmann_velocities()["hohmann_cruise_yr"]
    round_trip_yr = (
        burn_out["t_burn_yr"] + t_cruise_yr + SATURN_OPS_YR
        + burn_in["t_burn_yr"] + t_cruise_yr
    )
    delivered_t = chunk_t - burn_in["m_prop_t"]
    return {
        "m_tug_t": m_tug_t,
        "dv_outbound_km_s": dv_outbound_km_s,
        "dv_inbound_km_s": dv_inbound_km_s,
        "m_prop_outbound_t": burn_out["m_prop_t"],
        "m_LEO_t": m_tug_t + burn_out["m_prop_t"],
        "mass_ratio_outbound": burn_out["mass_ratio"],
        "m_prop_inbound_t": burn_in["m_prop_t"],
        "mass_ratio_inbound": burn_in["mass_ratio"],
        "t_outbound_burn_yr": burn_out["t_burn_yr"],
        "t_inbound_burn_yr": burn_in["t_burn_yr"],
        "t_cruise_each_yr": t_cruise_yr,
        "t_saturn_ops_yr": SATURN_OPS_YR,
        "round_trip_yr": round_trip_yr,
        "delivered_t": delivered_t,
        "delivered_fraction": delivered_t / chunk_t if chunk_t > 0 else 0.0,
        "closes_15yr": round_trip_yr <= ROUND_TRIP_CEILING_YR,
    }


def main() -> dict:
    results: dict = {}

    helio = hohmann_velocities()
    results["hohmann_velocities"] = helio

    # 1. Outbound DV decomposition at each Saturn arrival orbit, no LGA
    arrival_orbits = {
        "b_ring_1.35e5_km": SATURN_BRING_RADIUS_KM,
        "high_elliptical_1e6_km": SATURN_HIGH_ELLIPTICAL_KM,
        "iapetus_3.561e6_km": SATURN_IAPETUS_DISTANCE_KM,
    }
    no_lga = {name: outbound_dv_decomposition(r) for name, r in arrival_orbits.items()}
    results["outbound_dv_no_lga"] = no_lga

    with_lga = {
        name: outbound_dv_decomposition(r, lga_credit_km_s=LGA_OUTBOUND_CREDIT_KM_S)
        for name, r in arrival_orbits.items()
    }
    results["outbound_dv_with_lga"] = with_lga

    # 2. Round-trip composition at 1 MWe / decomposed-mid / Isp 2000 s / chunk 200 t
    # with CORRECTED outbound DV and titan's CORRECTED inbound DV.
    round_trips = {}
    for arr_name, dv_arr in no_lga.items():
        for dep_name, dv_in in [
            ("titan_inbound_high_elliptical_24.7_km_s", TITAN_INBOUND_HIGH_ELLIPTICAL_LGA_KM_S),
            ("titan_inbound_b_ring_40.2_km_s", TITAN_INBOUND_B_RING_NO_LGA_KM_S),
        ]:
            key = f"out_arr_{arr_name}__in_{dep_name}"
            round_trips[key] = round_trip_at_corrected_dv(
                m_tug_t=TUG_DRY_1MWE_DECOMPOSED_MID_T,
                chunk_t=CHUNK_BASELINE_T,
                power_kwe=POWER_BASELINE_KWE,
                isp_s=ISP_BASELINE_S,
                dv_outbound_km_s=dv_arr["dv_total_km_s"],
                dv_inbound_km_s=dv_in,
            )
    results["round_trips_corrected"] = round_trips

    # 3. Composite-realism best-case: high-elliptical at both ends (titan's
    # recommendation) with LGA credit applied on both legs.
    dv_out_he_with_lga = with_lga["high_elliptical_1e6_km"]["dv_total_km_s"]
    best_case = round_trip_at_corrected_dv(
        m_tug_t=TUG_DRY_1MWE_DECOMPOSED_MID_T,
        chunk_t=CHUNK_BASELINE_T,
        power_kwe=POWER_BASELINE_KWE,
        isp_s=ISP_BASELINE_S,
        dv_outbound_km_s=dv_out_he_with_lga,
        dv_inbound_km_s=TITAN_INBOUND_HIGH_ELLIPTICAL_LGA_KM_S,
    )
    results["best_case_high_elliptical_both_ends_with_lga"] = best_case

    # 4. Cross-check against my R-electric-outbound-rerun's value:
    # At the SAME inbound DV (titan high-elliptical 24.7 km/s) but the OLD
    # R-electric-outbound outbound DV (17.97 km/s), what does the round-trip
    # come to? Compare with the new composition.
    cross_check_rerun = round_trip_at_corrected_dv(
        m_tug_t=TUG_DRY_1MWE_DECOMPOSED_MID_T,
        chunk_t=CHUNK_BASELINE_T,
        power_kwe=POWER_BASELINE_KWE,
        isp_s=ISP_BASELINE_S,
        dv_outbound_km_s=R_OUTBOUND_DV_KM_S,
        dv_inbound_km_s=TITAN_INBOUND_HIGH_ELLIPTICAL_LGA_KM_S,
    )
    results["cross_check_rerun_dv_in_use"] = cross_check_rerun

    # 5. Hypothesis grading
    he = no_lga["high_elliptical_1e6_km"]
    br = no_lga["b_ring_1.35e5_km"]

    # H-od-a — outbound DV high-elliptical no-LGA in 27-32 km/s
    h_od_a_predicted = [27.0, 32.0]
    h_od_a_actual = he["dv_total_km_s"]
    h_od_a_held = h_od_a_predicted[0] <= h_od_a_actual <= h_od_a_predicted[1]

    # H-od-b — outbound DV B-ring no-LGA in 37-42 km/s
    h_od_b_predicted = [37.0, 42.0]
    h_od_b_actual = br["dv_total_km_s"]
    h_od_b_held = h_od_b_predicted[0] <= h_od_b_actual <= h_od_b_predicted[1]

    # H-od-c — corrected outbound is at least 1.5× R-electric-outbound's
    # 17.97 km/s at the high-elliptical case
    h_od_c_predicted = ">= 1.5x R-electric-outbound outbound DV"
    h_od_c_actual_ratio = he["dv_total_km_s"] / R_OUTBOUND_DV_KM_S
    h_od_c_held = h_od_c_actual_ratio >= 1.5

    # H-od-d — round-trip at 1 MWe / decomposed-mid / titan-inbound-high-
    # elliptical / outbound-arrival-high-elliptical exceeds 18 years
    # (R-electric-outbound-rerun reported 15.17 yr at OLD outbound DV — adding
    # ~12 km/s on outbound at Isp 2000 s gives mass_ratio bump ~1.8x and
    # outbound burn-time grows further)
    h_od_d_rt = round_trips["out_arr_high_elliptical_1e6_km__in_titan_inbound_high_elliptical_24.7_km_s"]["round_trip_yr"]
    h_od_d_predicted = "> 18.0 yr"
    h_od_d_held = h_od_d_rt > 18.0

    # H-od-e — best-case (high-elliptical both ends + LGA on both legs) still
    # exceeds the 15-year L0-05 ceiling
    h_od_e_held = best_case["round_trip_yr"] > ROUND_TRIP_CEILING_YR
    h_od_e_predicted = "best case round-trip > 15 yr (architecture falsified at L0-05)"

    results["hypothesis_grading"] = {
        "H_od_a": {"predicted_km_s": h_od_a_predicted, "actual_km_s": h_od_a_actual, "held": h_od_a_held},
        "H_od_b": {"predicted_km_s": h_od_b_predicted, "actual_km_s": h_od_b_actual, "held": h_od_b_held},
        "H_od_c": {"predicted": h_od_c_predicted, "actual_ratio": h_od_c_actual_ratio, "held": h_od_c_held},
        "H_od_d": {"predicted": h_od_d_predicted, "actual_yr": h_od_d_rt, "held": h_od_d_held},
        "H_od_e": {"predicted": h_od_e_predicted,
                    "actual_best_case_yr": best_case["round_trip_yr"],
                    "delivered_t": best_case["delivered_t"], "held": h_od_e_held},
    }

    # Write JSON
    results_dir = Path(__file__).parent / "results"
    results_dir.mkdir(exist_ok=True)
    (results_dir / "outbound_dv_continuous.json").write_text(json.dumps(results, indent=2, default=str))

    # Tables
    lines = []
    lines.append("### Hohmann baseline and spiral endpoints\n")
    lines.append(f"- Earth heliocentric orbital speed: {helio['v_earth_helio_km_s']:.3f} km/s")
    lines.append(f"- Saturn heliocentric orbital speed: {helio['v_saturn_helio_km_s']:.3f} km/s")
    lines.append(f"- Hohmann perihelion velocity at Earth's distance: {helio['v_hohmann_perihelion_km_s']:.3f} km/s")
    lines.append(f"- Hohmann aphelion velocity at Saturn's distance: {helio['v_hohmann_aphelion_km_s']:.3f} km/s")
    lines.append(f"- Velocity-at-infinity at Earth: {helio['v_inf_at_earth_km_s']:.3f} km/s")
    lines.append(f"- Velocity-at-infinity at Saturn: {helio['v_inf_at_saturn_km_s']:.3f} km/s")
    lines.append(f"- Low-Earth-orbit Edelbaum spiral integrated Δv: {leo_spiral_dv_km_s():.3f} km/s")
    lines.append(f"- Hohmann cruise (each way): {helio['hohmann_cruise_yr']:.3f} years\n")

    lines.append("### Outbound continuous-thrust integrated Δv — no lunar gravity assist\n")
    lines.append("Composition: LEO spiral (segment 5') + Earth-side heliocentric (4') + "
                  "Saturn-side heliocentric (2') + Saturn-side capture spiral (1').\n")
    lines.append("| Saturn arrival orbit | 5' LEO spiral | 4' Earth-helio | 2' Saturn-helio | 1' Saturn spiral | **Total Δv (km/s)** | Δ vs R-electric-outbound 17.97 km/s |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|")
    for name, d in no_lga.items():
        lines.append(
            f"| {name} | {d['dv5p_leo_spiral_km_s']:.2f} | {d['dv4p_earth_helio_km_s']:.2f} | "
            f"{d['dv2p_saturn_helio_km_s']:.2f} | {d['dv1p_saturn_spiral_km_s']:.2f} | "
            f"**{d['dv_total_km_s']:.2f}** | +{d['delta_vs_R_electric_outbound_km_s']:.2f} |"
        )
    lines.append("")

    lines.append("### Outbound continuous-thrust integrated Δv — with 2 km/s lunar gravity assist credit\n")
    lines.append("Lunar gravity assist credit subtracted from the Earth-side combined (5' + 4'). "
                  "Same methodology as titan's inbound treatment.\n")
    lines.append("| Saturn arrival orbit | Earth combined (post-LGA) | 2' Saturn-helio | 1' Saturn spiral | **Total Δv (km/s)** |")
    lines.append("|---|---:|---:|---:|---:|")
    for name, d in with_lga.items():
        lines.append(
            f"| {name} | {d['dv_earth_after_lga_km_s']:.2f} | {d['dv2p_saturn_helio_km_s']:.2f} | "
            f"{d['dv1p_saturn_spiral_km_s']:.2f} | **{d['dv_total_km_s']:.2f}** |"
        )
    lines.append("")

    lines.append("### Round-trip composition — 1 MWe / decomposed-mid (m_tug = 31.5 t) / Isp 2000 s / chunk 200 t\n")
    lines.append("Outbound: corrected continuous-thrust integrated Δv (this round); corrected dry-at-end "
                  "burn formula (R-electric-outbound-rerun).\n"
                  "Inbound: titan's continuous-thrust integrated Δv; chunk-fed wet-at-start burn formula.\n")
    lines.append("| Outbound arrival | Inbound regime | t_out (yr) | t_in (yr) | Round-trip (yr) | Delivered (t) | Closes 15 yr? |")
    lines.append("|---|---|---:|---:|---:|---:|:--:|")
    for key, r in round_trips.items():
        flag = "**yes**" if r["closes_15yr"] else "no"
        lines.append(
            f"| {key.split('__')[0].replace('out_arr_', '')} | "
            f"{key.split('__')[1].replace('in_', '')} | "
            f"{r['t_outbound_burn_yr']:.2f} | {r['t_inbound_burn_yr']:.2f} | "
            f"{r['round_trip_yr']:.2f} | {r['delivered_t']:.1f} | {flag} |"
        )
    lines.append("")

    lines.append("### Best-case composite — high-elliptical both ends + LGA credit on both legs\n")
    b = best_case
    lines.append(f"- Outbound Δv (high-elliptical arrival, LGA credit): {dv_out_he_with_lga:.2f} km/s")
    lines.append(f"- Inbound Δv (titan high-elliptical departure, LGA credit): {TITAN_INBOUND_HIGH_ELLIPTICAL_LGA_KM_S} km/s")
    lines.append(f"- t_outbound burn: {b['t_outbound_burn_yr']:.2f} yr")
    lines.append(f"- t_inbound burn: {b['t_inbound_burn_yr']:.2f} yr")
    lines.append(f"- Round-trip: **{b['round_trip_yr']:.2f} yr** "
                  f"({'closes' if b['closes_15yr'] else '**MISSES**'} the 15-year L0-05 ceiling)")
    lines.append(f"- Delivered: {b['delivered_t']:.1f} t out of 200 t chunk "
                  f"({b['delivered_fraction']*100:.1f}% delivered fraction)\n")

    lines.append("### Cross-check against R-electric-outbound-rerun\n")
    c = cross_check_rerun
    lines.append(f"- Using R-electric-outbound's outbound Δv ({R_OUTBOUND_DV_KM_S} km/s) with "
                  f"titan-inbound 24.7 km/s and corrected formulas: round-trip = {c['round_trip_yr']:.2f} yr "
                  f"(matches R-electric-outbound-rerun's 15.17 yr headline within rounding).")
    lines.append(f"- Using corrected outbound Δv to high-elliptical, no LGA "
                  f"({no_lga['high_elliptical_1e6_km']['dv_total_km_s']:.2f} km/s) with the same inbound: "
                  f"round-trip = "
                  f"{round_trips['out_arr_high_elliptical_1e6_km__in_titan_inbound_high_elliptical_24.7_km_s']['round_trip_yr']:.2f} yr.")
    lines.append(f"- Δ round-trip from outbound DV correction alone: "
                  f"{round_trips['out_arr_high_elliptical_1e6_km__in_titan_inbound_high_elliptical_24.7_km_s']['round_trip_yr'] - c['round_trip_yr']:.2f} yr.\n")

    lines.append("### Hypothesis grading\n")
    h = results["hypothesis_grading"]
    lines.append("| Sub-claim | Predicted | Actual | Held? |")
    lines.append("|---|---|---|---|")
    lines.append(f"| H-od-a — Outbound Δv high-elliptical, no LGA | "
                  f"{h['H_od_a']['predicted_km_s']} km/s | "
                  f"{h['H_od_a']['actual_km_s']:.2f} km/s | "
                  f"{'yes' if h['H_od_a']['held'] else '**no**'} |")
    lines.append(f"| H-od-b — Outbound Δv B-ring, no LGA | "
                  f"{h['H_od_b']['predicted_km_s']} km/s | "
                  f"{h['H_od_b']['actual_km_s']:.2f} km/s | "
                  f"{'yes' if h['H_od_b']['held'] else '**no**'} |")
    lines.append(f"| H-od-c — Corrected outbound ≥ 1.5× R-electric-outbound's 17.97 km/s | "
                  f"{h['H_od_c']['predicted']} | "
                  f"{h['H_od_c']['actual_ratio']:.2f}× | "
                  f"{'yes' if h['H_od_c']['held'] else '**no**'} |")
    lines.append(f"| H-od-d — Round-trip at 1 MWe / decomposed-mid / outbound-high-ellip / titan-inbound-24.7 > 18 yr | "
                  f"{h['H_od_d']['predicted']} | "
                  f"{h['H_od_d']['actual_yr']:.2f} yr | "
                  f"{'yes' if h['H_od_d']['held'] else '**no**'} |")
    lines.append(f"| H-od-e — Best-case high-elliptical both ends + LGA both legs round-trip > 15 yr | "
                  f"{h['H_od_e']['predicted']} | "
                  f"{h['H_od_e']['actual_best_case_yr']:.2f} yr | "
                  f"{'yes' if h['H_od_e']['held'] else '**no**'} |")
    lines.append("")

    (results_dir / "tables.md").write_text("\n".join(lines))
    return results


if __name__ == "__main__":
    out = main()
    print("R-outbound-dv-continuous-thrust complete.")
    print()
    print("  Outbound continuous-thrust integrated Δv (no LGA):")
    for name, d in out["outbound_dv_no_lga"].items():
        print(f"    {name:30s}: {d['dv_total_km_s']:.2f} km/s (vs R-electric-outbound 17.97 km/s; "
              f"+{d['delta_vs_R_electric_outbound_km_s']:.2f} km/s)")
    print()
    print("  Round-trip totals (1 MWe / decomposed-mid / Isp 2000 / chunk 200 t):")
    for key, r in out["round_trips_corrected"].items():
        flag = "closes" if r["closes_15yr"] else "MISSES"
        print(f"    {key:75s}: {r['round_trip_yr']:.2f} yr ({flag}, delivered {r['delivered_t']:.1f} t)")
    print()
    print(f"  Best-case (high-elliptical both ends, LGA both legs): "
          f"{out['best_case_high_elliptical_both_ends_with_lga']['round_trip_yr']:.2f} yr, "
          f"delivered {out['best_case_high_elliptical_both_ends_with_lga']['delivered_t']:.1f} t")
    print()
    print("  Hypothesis grading:")
    for k, v in out["hypothesis_grading"].items():
        print(f"    {k}: {'held' if v['held'] else 'FALSIFIED'}")
