#!/usr/bin/env python3
"""R-aerocapture-fast-cruise-envelope.

Does Round F's STRICT-closing Variant C cell survive the Earth aerocapture
engineering envelope under chunk-as-heat-shield?

Pre-registration is in STUDY.md. Central estimates were computed BEFORE the
range bands were named, per recurring-lesson #N intervention.

Deterministic. No Monte Carlo. Run from project root or from this directory.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

G_EARTH_M_S2 = 9.80665
EARTH_RADIUS_KM = 6378.137
EARTH_MU_KM3_S2 = 398600.4418
EARTH_V_ESCAPE_SURFACE_KM_S = math.sqrt(2.0 * EARTH_MU_KM3_S2 / EARTH_RADIUS_KM)  # ~11.18
EARTH_V_ESCAPE_INTERFACE_KM_S = math.sqrt(2.0 * EARTH_MU_KM3_S2 / (EARTH_RADIUS_KM + 125.0))  # ~11.07
EARTH_V_CIRCULAR_LEO_KM_S = math.sqrt(EARTH_MU_KM3_S2 / (EARTH_RADIUS_KM + 400.0))  # ~7.67
EARTH_V_ORBIT_KM_S = 29.7846918  # heliocentric

WATER_ICE_DENSITY_KG_M3 = 917.0
WATER_HEAT_OF_VAPORIZATION_J_KG = 2.26e6
ICE_TENSILE_STRENGTH_PA = 1.0e6  # 1 megapascal, cold polycrystalline ice

DRAG_COEFFICIENT_BLUNT = 1.0
SUTTON_GRAVES_K_SI = 1.7415e-4  # W / (m^2) per (kg/m^3)^0.5 / (m/s)^3 with nose-radius in m

# Exponential atmosphere parameters above 80 km (US Standard Atmosphere fit)
ATM_DENSITY_AT_100KM_KG_M3 = 5.6e-7
ATM_SCALE_HEIGHT_KM = 7.5
ATM_REFERENCE_ALTITUDE_KM = 100.0

# Round F output anchors (from results/R_cruise_time_optimization.json)
ROUND_F_TUG_MASS_T = 63.8  # 500 kWe MARVL-anchored
LGA_CREDIT_KM_S = 2.0

# Round F transfers — perihelion velocity at Earth orbit (heliocentric)
ROUND_F_TRANSFERS = {
    9.58: {"v_perihelion_km_s": 40.082, "cruise_yr": 6.086, "delivered_t": 32.14},
    10.50: {"v_perihelion_km_s": 40.249, "cruise_yr": 4.436, "delivered_t": 26.01},
    11.00: {"v_perihelion_km_s": 40.329, "cruise_yr": 4.183, "delivered_t": 23.47},
    12.00: {"v_perihelion_km_s": 40.469, "cruise_yr": 3.864, "delivered_t": 19.45},
    14.00: {"v_perihelion_km_s": 40.694, "cruise_yr": 3.517, "delivered_t": 13.92},
}

# R-chunk-as-heat-shield anchor — used for cross-check
RCAHS_ENTRY_VELOCITY_KM_S = 12.6
RCAHS_ABLATION_PCT = 0.5
RCAHS_HEAT_FLUX_W_CM2 = 180.0  # implied from R-chunk-as-heat-shield closure


# ---------------------------------------------------------------------------
# Geometry and aerothermal helpers
# ---------------------------------------------------------------------------

def chunk_radius_m(mass_t: float) -> float:
    """Sphere-equivalent radius of an ice chunk of given mass in tonnes."""
    volume_m3 = mass_t * 1000.0 / WATER_ICE_DENSITY_KG_M3
    return (3.0 * volume_m3 / (4.0 * math.pi)) ** (1.0 / 3.0)


def frontal_area_m2(mass_t: float) -> float:
    r = chunk_radius_m(mass_t)
    return math.pi * r * r


def ballistic_coefficient(mass_t: float, total_mass_t: float | None = None) -> float:
    """β = m_total / (Cd × A_chunk).

    Tug rides behind chunk so frontal area is chunk's only.
    """
    m_total = total_mass_t if total_mass_t is not None else mass_t
    return m_total * 1000.0 / (DRAG_COEFFICIENT_BLUNT * frontal_area_m2(mass_t))


def atmosphere_density(altitude_km: float) -> float:
    """Exponential atmosphere above 80 km."""
    return ATM_DENSITY_AT_100KM_KG_M3 * math.exp(
        -(altitude_km - ATM_REFERENCE_ALTITUDE_KM) / ATM_SCALE_HEIGHT_KM
    )


def v_infinity_at_earth_km_s(v_perihelion_km_s: float, lga_credit_km_s: float = 0.0) -> float:
    """Approximate v_infinity by tangential-difference, minus lunar-gravity-assist credit."""
    raw = v_perihelion_km_s - EARTH_V_ORBIT_KM_S
    return max(0.1, raw - lga_credit_km_s)


def entry_velocity_at_interface_km_s(v_infinity_km_s: float) -> float:
    """v_e = sqrt(v_inf^2 + v_esc^2) at 125 km interface."""
    return math.sqrt(v_infinity_km_s ** 2 + EARTH_V_ESCAPE_INTERFACE_KM_S ** 2)


def required_periapsis_altitude_km(
    v_entry_km_s: float, ballistic_coef_kg_m2: float, target_dv_km_s: float
) -> tuple[float, float]:
    """Find periapsis altitude such that drag impulse equals target_dv across pulse.

    Approximate: pulse pass length L ≈ 2 × sqrt(2 × R_earth × scale_height),
    average density ≈ atmosphere_density(periapsis_alt),
    drag delta-v ≈ rho × L × v / β.

    Returns (periapsis_altitude_km, pulse_duration_s).
    """
    # Iterate on altitude.
    target_dv_m_s = target_dv_km_s * 1000.0
    v_entry_m_s = v_entry_km_s * 1000.0
    # Pulse path length through dense atmosphere (geometric, scale-height anchored)
    # L ≈ 2 × sqrt(2 × (R + h) × H) where H is scale height
    for alt_km in range(40, 121):
        rho = atmosphere_density(float(alt_km))
        path_length_m = 2.0 * math.sqrt(2.0 * (EARTH_RADIUS_KM + alt_km) * 1000.0 * ATM_SCALE_HEIGHT_KM * 1000.0)
        # Drag delta-v per pass ≈ (rho × L / β) × v_entry, integrated naively
        dv_m_s = (rho * path_length_m / ballistic_coef_kg_m2) * v_entry_m_s
        if dv_m_s >= target_dv_m_s:
            pulse_duration_s = path_length_m / v_entry_m_s
            return float(alt_km), pulse_duration_s
    # Failed to capture even at lowest altitude (40 km)
    rho = atmosphere_density(40.0)
    path_length_m = 2.0 * math.sqrt(2.0 * (EARTH_RADIUS_KM + 40.0) * 1000.0 * ATM_SCALE_HEIGHT_KM * 1000.0)
    pulse_duration_s = path_length_m / v_entry_m_s
    return 40.0, pulse_duration_s


def sutton_graves_peak_w_cm2(v_entry_km_s: float, periapsis_alt_km: float, nose_radius_m: float) -> float:
    """Peak stagnation-point heat flux per Sutton-Graves."""
    rho = atmosphere_density(periapsis_alt_km)
    v_m_s = v_entry_km_s * 1000.0
    q_w_m2 = SUTTON_GRAVES_K_SI * math.sqrt(rho / nose_radius_m) * v_m_s ** 3
    return q_w_m2 / 1.0e4  # convert W/m^2 to W/cm^2


def total_heat_load_J_per_m2(q_peak_w_cm2: float, pulse_duration_s: float) -> float:
    """Time-integrated heat load (rectangular peak approximation upper-bounded)."""
    q_peak_w_m2 = q_peak_w_cm2 * 1.0e4
    # Approximate as triangular pulse with peak at midpoint: integral = 0.5 × q_peak × duration
    return 0.5 * q_peak_w_m2 * pulse_duration_s


def chunk_ablation_pct(
    total_heat_load_J_m2: float, frontal_area_m2_val: float, chunk_mass_t: float
) -> float:
    """Ablation as percent of chunk mass.

    Total energy = heat load × area. Mass ablated = energy / heat-of-vaporization.
    """
    total_energy_J = total_heat_load_J_m2 * frontal_area_m2_val
    mass_ablated_kg = total_energy_J / WATER_HEAT_OF_VAPORIZATION_J_KG
    return 100.0 * mass_ablated_kg / (chunk_mass_t * 1000.0)


def peak_g(v_entry_km_s: float, pulse_duration_s: float, peak_factor: float = 2.5) -> float:
    """Peak g-loading: average × empirical peak-factor."""
    avg_decel_m_s2 = (v_entry_km_s - EARTH_V_CIRCULAR_LEO_KM_S) * 1000.0 / pulse_duration_s
    return peak_factor * avg_decel_m_s2 / G_EARTH_M_S2


def chunk_internal_stress_Pa(chunk_mass_t: float, peak_g_load: float) -> float:
    r = chunk_radius_m(chunk_mass_t)
    return r * WATER_ICE_DENSITY_KG_M3 * peak_g_load * G_EARTH_M_S2


# ---------------------------------------------------------------------------
# Main sweep
# ---------------------------------------------------------------------------

def run() -> dict:
    out: dict = {"config": {
        "lga_credit_km_s": LGA_CREDIT_KM_S,
        "round_f_tug_mass_t": ROUND_F_TUG_MASS_T,
        "drag_coefficient": DRAG_COEFFICIENT_BLUNT,
        "ice_tensile_strength_Pa": ICE_TENSILE_STRENGTH_PA,
        "water_heat_of_vaporization_J_kg": WATER_HEAT_OF_VAPORIZATION_J_KG,
        "atmosphere_density_at_100km_kg_m3": ATM_DENSITY_AT_100KM_KG_M3,
        "atmosphere_scale_height_km": ATM_SCALE_HEIGHT_KM,
        "earth_v_escape_interface_km_s": EARTH_V_ESCAPE_INTERFACE_KM_S,
        "earth_v_circular_leo_km_s": EARTH_V_CIRCULAR_LEO_KM_S,
    }}

    chunk_masses = [100.0, 200.0, 263.8, 350.0]
    aphelion_aus = [9.58, 10.5, 11.0, 12.0, 14.0]
    lga_modes = [True, False]

    cases = []
    for r_apo in aphelion_aus:
        if r_apo not in ROUND_F_TRANSFERS:
            continue
        v_peri = ROUND_F_TRANSFERS[r_apo]["v_perihelion_km_s"]
        cruise_yr = ROUND_F_TRANSFERS[r_apo]["cruise_yr"]
        delivered_t = ROUND_F_TRANSFERS[r_apo]["delivered_t"]
        for chunk_t in chunk_masses:
            # Tug mass scales with reactor — keep at Round F's 500 kWe value (63.8 t)
            # for chunk_t = 200 (closing case). For other chunk masses, keep tug at same
            # absolute mass (simplification — tug mass doesn't depend on chunk mass).
            total_mass_t = chunk_t + ROUND_F_TUG_MASS_T
            for lga in lga_modes:
                lga_cred = LGA_CREDIT_KM_S if lga else 0.0
                v_inf = v_infinity_at_earth_km_s(v_peri, lga_cred)
                v_e = entry_velocity_at_interface_km_s(v_inf)
                # Capture target: bleed from v_e to v_circular_LEO
                target_dv = v_e - EARTH_V_CIRCULAR_LEO_KM_S
                beta = ballistic_coefficient(chunk_t, total_mass_t)
                periapsis_alt, pulse_duration = required_periapsis_altitude_km(
                    v_e, beta, target_dv
                )
                nose_r = chunk_radius_m(chunk_t)
                front_area = frontal_area_m2(chunk_t)
                q_peak = sutton_graves_peak_w_cm2(v_e, periapsis_alt, nose_r)
                heat_load = total_heat_load_J_per_m2(q_peak, pulse_duration)
                ablation_pct = chunk_ablation_pct(heat_load, front_area, chunk_t)
                pk_g = peak_g(v_e, pulse_duration)
                stress_pa = chunk_internal_stress_Pa(chunk_t, pk_g)
                tensile_margin = ICE_TENSILE_STRENGTH_PA / stress_pa if stress_pa > 0 else float("inf")
                # Survives if ablation < 5% AND tensile margin > 1.0 AND periapsis > 50 km
                envelope_pass = (
                    ablation_pct < 5.0
                    and tensile_margin > 1.0
                    and periapsis_alt > 50.0
                )
                cases.append({
                    "r_apo_AU": r_apo,
                    "cruise_yr": cruise_yr,
                    "chunk_t": chunk_t,
                    "total_mass_t": total_mass_t,
                    "lga_credit": lga_cred,
                    "v_perihelion_helio_km_s": v_peri,
                    "v_infinity_km_s": v_inf,
                    "v_entry_km_s": v_e,
                    "ballistic_coef_kg_m2": beta,
                    "chunk_radius_m": nose_r,
                    "periapsis_alt_km": periapsis_alt,
                    "pulse_duration_s": pulse_duration,
                    "q_peak_w_cm2": q_peak,
                    "ablation_pct_per_pass": ablation_pct,
                    "peak_g_load": pk_g,
                    "internal_stress_Pa": stress_pa,
                    "tensile_margin": tensile_margin,
                    "envelope_pass": envelope_pass,
                    "round_f_delivered_baseline_t": delivered_t,
                    "delivered_after_ablation_t": delivered_t * (1.0 - ablation_pct / 100.0),
                })
    out["cases"] = cases

    # Cross-check against R-chunk-as-heat-shield (aphelion 9.58, mass 100, with LGA)
    cross_check = next(
        c for c in cases
        if c["r_apo_AU"] == 9.58 and c["chunk_t"] == 100.0 and c["lga_credit"] == LGA_CREDIT_KM_S
    )
    out["cross_check_vs_RCAHS"] = {
        "predicted_v_entry_km_s": RCAHS_ENTRY_VELOCITY_KM_S,
        "computed_v_entry_km_s": cross_check["v_entry_km_s"],
        "ratio": cross_check["v_entry_km_s"] / RCAHS_ENTRY_VELOCITY_KM_S,
        "predicted_ablation_pct": RCAHS_ABLATION_PCT,
        "computed_ablation_pct": cross_check["ablation_pct_per_pass"],
        "ablation_ratio": cross_check["ablation_pct_per_pass"] / RCAHS_ABLATION_PCT,
        "predicted_q_peak_w_cm2": RCAHS_HEAT_FLUX_W_CM2,
        "computed_q_peak_w_cm2": cross_check["q_peak_w_cm2"],
    }

    # Round F closing-case verdict: aphelion 11, mass 200 (chunk) + 63.8 (tug) = 263.8, no LGA
    closing_case = next(
        c for c in cases
        if c["r_apo_AU"] == 11.0 and c["chunk_t"] == 200.0 and c["lga_credit"] == 0.0
    )
    closing_case_with_lga = next(
        c for c in cases
        if c["r_apo_AU"] == 11.0 and c["chunk_t"] == 200.0 and c["lga_credit"] == LGA_CREDIT_KM_S
    )
    out["round_f_closing_case_verdict"] = {
        "no_lga": closing_case,
        "with_lga": closing_case_with_lga,
        "envelope_pass_no_lga": closing_case["envelope_pass"],
        "envelope_pass_with_lga": closing_case_with_lga["envelope_pass"],
    }

    # Hypothesis grading
    grading = {}
    closing = closing_case  # no-LGA case is the conservative anchor

    grading["H_afce_a"] = {
        "central": 15.4,
        "range": [14.5, 16.5],
        "computed": closing["v_entry_km_s"],
        "held": 14.5 <= closing["v_entry_km_s"] <= 16.5,
    }
    grading["H_afce_b"] = {
        "central": 330.0,
        "range": [200.0, 500.0],
        "computed": closing["q_peak_w_cm2"],
        "held": 200.0 <= closing["q_peak_w_cm2"] <= 500.0,
    }
    grading["H_afce_c"] = {
        "central": 0.9,
        "range": [0.4, 2.5],
        "computed": closing["ablation_pct_per_pass"],
        "held": 0.4 <= closing["ablation_pct_per_pass"] <= 2.5,
    }
    grading["H_afce_d"] = {
        "central": 10.0,
        "range": [5.0, 18.0],
        "computed": closing["peak_g_load"],
        "held": 5.0 <= closing["peak_g_load"] <= 18.0,
    }
    grading["H_afce_e"] = {
        "central": 2.9,
        "range": [1.5, 6.0],
        "computed": closing["tensile_margin"],
        "held": 1.5 <= closing["tensile_margin"] <= 6.0,
    }
    delivered_pct_drop = (
        100.0 * (closing["round_f_delivered_baseline_t"] - closing["delivered_after_ablation_t"])
        / closing["round_f_delivered_baseline_t"]
    )
    grading["H_afce_f"] = {
        "central_pct_drop": 1.0,
        "range_pct_drop": [0.5, 4.0],
        "computed_pct_drop": delivered_pct_drop,
        "envelope_passed": closing["envelope_pass"],
        "held": (
            0.5 <= delivered_pct_drop <= 4.0
            and closing["envelope_pass"]
        ),
    }
    grading["H_afce_g"] = {
        "central": 60.0,
        "range": [50.0, 75.0],
        "computed": closing["periapsis_alt_km"],
        "held": 50.0 <= closing["periapsis_alt_km"] <= 75.0,
    }
    held_count = sum(1 for v in grading.values() if v["held"])
    grading["aggregate"] = {
        "held_count": held_count,
        "total": len(grading) - 0,
        "h_afce_agg_held": held_count >= 5,
    }
    out["hypothesis_grading"] = grading

    return out


def write_tables(result: dict, outdir: Path) -> None:
    lines = ["# R-aerocapture-fast-cruise-envelope — results tables", ""]

    cc = result["cross_check_vs_RCAHS"]
    lines.append("## Cross-check against R-chunk-as-heat-shield")
    lines.append("")
    lines.append(f"- Predicted entry velocity: {cc['predicted_v_entry_km_s']:.2f} km/s")
    lines.append(f"- Computed entry velocity (aphelion 9.58, 100 t, with LGA): {cc['computed_v_entry_km_s']:.2f} km/s")
    lines.append(f"- Ratio computed/predicted: {cc['ratio']:.3f}")
    lines.append(f"- Predicted ablation: {cc['predicted_ablation_pct']:.2f}%  vs  Computed: {cc['computed_ablation_pct']:.2f}%")
    lines.append(f"- Predicted q_peak: {cc['predicted_q_peak_w_cm2']:.0f} W/cm² vs Computed: {cc['computed_q_peak_w_cm2']:.0f} W/cm²")
    lines.append("")
    if cc['ratio'] > 1.10 or cc['ratio'] < 0.90:
        lines.append("**Cross-check shows model disagreement with R-chunk-as-heat-shield > 10%.** "
                     "Either model setup differs (different lunar-gravity-assist credit, different "
                     "atmosphere model, different periapsis assumption) or one of the two rounds "
                     "is wrong. See discussion in closure_verdict.md.")
        lines.append("")
    else:
        lines.append("Cross-check inside 10% — model anchored to validated point.")
        lines.append("")

    lines.append("## Round F closing case verdict (aphelion 11 AU, 200 t chunk, 63.8 t tug)")
    lines.append("")
    cv_no = result["round_f_closing_case_verdict"]["no_lga"]
    cv_w = result["round_f_closing_case_verdict"]["with_lga"]
    lines.append("| Metric | No LGA | With LGA (2 km/s credit) |")
    lines.append("|---|---:|---:|")
    lines.append(f"| Velocity-at-infinity at Earth (km/s) | {cv_no['v_infinity_km_s']:.2f} | {cv_w['v_infinity_km_s']:.2f} |")
    lines.append(f"| Entry velocity (km/s) | {cv_no['v_entry_km_s']:.2f} | {cv_w['v_entry_km_s']:.2f} |")
    lines.append(f"| Ballistic coefficient (kg/m²) | {cv_no['ballistic_coef_kg_m2']:.0f} | {cv_w['ballistic_coef_kg_m2']:.0f} |")
    lines.append(f"| Periapsis altitude (km) | {cv_no['periapsis_alt_km']:.0f} | {cv_w['periapsis_alt_km']:.0f} |")
    lines.append(f"| Pulse duration (s) | {cv_no['pulse_duration_s']:.0f} | {cv_w['pulse_duration_s']:.0f} |")
    lines.append(f"| Peak heat flux (W/cm²) | {cv_no['q_peak_w_cm2']:.0f} | {cv_w['q_peak_w_cm2']:.0f} |")
    lines.append(f"| Chunk ablation per pass (%) | {cv_no['ablation_pct_per_pass']:.2f} | {cv_w['ablation_pct_per_pass']:.2f} |")
    lines.append(f"| Peak g-load | {cv_no['peak_g_load']:.1f} | {cv_w['peak_g_load']:.1f} |")
    lines.append(f"| Chunk internal stress (kPa) | {cv_no['internal_stress_Pa']/1000:.0f} | {cv_w['internal_stress_Pa']/1000:.0f} |")
    lines.append(f"| Tensile margin (×) | {cv_no['tensile_margin']:.2f} | {cv_w['tensile_margin']:.2f} |")
    lines.append(f"| Envelope pass | {cv_no['envelope_pass']} | {cv_w['envelope_pass']} |")
    lines.append(f"| Delivered after ablation (t) | {cv_no['delivered_after_ablation_t']:.2f} | {cv_w['delivered_after_ablation_t']:.2f} |")
    lines.append("")

    lines.append("## All cases sweep — entry velocity, ablation, envelope-pass")
    lines.append("")
    lines.append("| r_apo (AU) | chunk (t) | LGA | v_entry (km/s) | β (kg/m²) | periapsis (km) | q_peak (W/cm²) | ablation (%) | peak g | margin × | env pass |")
    lines.append("|---:|---:|:---:|---:|---:|---:|---:|---:|---:|---:|:---:|")
    for c in result["cases"]:
        lga = "Y" if c["lga_credit"] > 0 else "N"
        lines.append(
            f"| {c['r_apo_AU']:.2f} | {c['chunk_t']:.0f} | {lga} | "
            f"{c['v_entry_km_s']:.2f} | {c['ballistic_coef_kg_m2']:.0f} | "
            f"{c['periapsis_alt_km']:.0f} | {c['q_peak_w_cm2']:.0f} | "
            f"{c['ablation_pct_per_pass']:.2f} | {c['peak_g_load']:.1f} | "
            f"{c['tensile_margin']:.2f} | {c['envelope_pass']} |"
        )
    lines.append("")

    lines.append("## Hypothesis grading")
    lines.append("")
    lines.append("| Sub-claim | Central | Range | Computed | Held |")
    lines.append("|---|---:|---|---:|:---:|")
    for k, v in result["hypothesis_grading"].items():
        if k == "aggregate":
            continue
        if "central" in v:
            ctr = v["central"]
            rng = v.get("range", [None, None])
            comp = v["computed"]
            lines.append(f"| {k} | {ctr} | [{rng[0]}, {rng[1]}] | {comp:.3f} | {v['held']} |")
        else:
            comp = v.get("computed_pct_drop", "n/a")
            ctr = v.get("central_pct_drop", "n/a")
            rng = v.get("range_pct_drop", [None, None])
            lines.append(f"| {k} | {ctr} | [{rng[0]}, {rng[1]}] | {comp:.3f} | {v['held']} |")
    agg = result["hypothesis_grading"]["aggregate"]
    lines.append("")
    lines.append(f"**Aggregate: {agg['held_count']}/{agg['total']-1} sub-claims held. H-afce-agg held: {agg['h_afce_agg_held']}.**")

    (outdir / "tables.md").write_text("\n".join(lines))


def write_verdict(result: dict, outdir: Path) -> None:
    cv = result["round_f_closing_case_verdict"]
    closing = cv["no_lga"]
    closing_lga = cv["with_lga"]
    grading = result["hypothesis_grading"]
    agg = grading["aggregate"]

    if closing["envelope_pass"]:
        verdict = "Round F STRICT-closing cell SURVIVES the aerocapture envelope (no-LGA case)."
    elif closing_lga["envelope_pass"]:
        verdict = (
            "Round F STRICT-closing cell SURVIVES only if 2 km/s lunar-gravity-assist credit is "
            "available; without LGA, fails. Closure becomes LGA-conditional."
        )
    else:
        verdict = "Round F STRICT-closing cell FAILS the aerocapture envelope. Variant C closure verdict at faster cruise is FALSIFIED at the engineering level."

    held_list = [k for k, v in grading.items() if k != "aggregate" and v["held"]]
    falsified_list = [k for k, v in grading.items() if k != "aggregate" and not v["held"]]

    lines = [
        "# R-aerocapture-fast-cruise-envelope — closure verdict",
        "",
        f"**Verdict:** {verdict}",
        "",
        "## Hypothesis grading summary",
        "",
        f"- Held: {', '.join(held_list) if held_list else 'none'}",
        f"- Falsified: {', '.join(falsified_list) if falsified_list else 'none'}",
        f"- Aggregate H-afce-agg: {'HELD' if agg['h_afce_agg_held'] else 'FALSIFIED'} ({agg['held_count']}/{agg['total']-1})",
        "",
        "## Recurring-lesson #N reading",
        "",
    ]

    if agg["h_afce_agg_held"]:
        lines.append(
            "Pre-registration intuition HELD this round. First held aggregate in seven hyperion-2 "
            "rounds (six prior all falsified in the same direction). The intervention — compute "
            "anchor numbers BEFORE pre-registering ranges — appears to have worked. The bias was "
            "not in the intuition itself but in the asymmetric range-naming around it. Continue "
            "this discipline next round."
        )
    else:
        falsified = [k for k in falsified_list if k.startswith("H_afce_")]
        lines.append(
            f"Pre-registration intuition FALSIFIED again this round on {falsified}. Seven-for-seven "
            "now. Recurring lesson #N updates: hyperion's anchor estimates themselves are biased, "
            "not just the range-naming. Possible mechanism: anchoring to R-chunk-as-heat-shield's "
            "12.6 km/s / 100 t result and naively scaling. Real engineering envelopes are "
            "non-linear in mass and velocity. Future hyperion sessions should pull engineering "
            "envelopes from primary literature (Stardust, Apollo, Genesis, Hayabusa) rather than "
            "scaling from analogous internal rounds."
        )

    lines.extend([
        "",
        "## Implications",
        "",
    ])
    if closing["envelope_pass"] and closing_lga["envelope_pass"]:
        lines.append(
            "Round F's STRICT closure verdict is robust to aerocapture envelope. Matrix can quote "
            "Variant C at faster cruise (aphelion 11 AU) as a closing cell with delivered "
            f"{closing['delivered_after_ablation_t']:.1f} t (after {closing['ablation_pct_per_pass']:.1f}% "
            "ablation), round-trip 12.7 yr. Aerocapture risk persists at the orientation-stability "
            "level (R-chunk-as-heat-shield-revisit's binding open question) — this round did NOT "
            "close that question."
        )
    elif closing_lga["envelope_pass"]:
        lines.append(
            "Round F closure is conditional on 2 km/s lunar-gravity-assist credit. Matrix should "
            "carry an arrival-epoch sensitivity row: 60–85% of arrival epochs give favorable LGA "
            "geometry (per R2 lunar-gravity-assist trajectory analysis); 15–40% of epochs would "
            "fail. Mission planning needs to wait for favorable launch windows, narrowing launch "
            "cadence."
        )
    else:
        lines.append(
            "Round F's STRICT closure verdict is FALSIFIED at the engineering level. Variant C "
            "at faster cruise does not actually deliver the matrix's stated mass — or worse, the "
            "vehicle does not survive the pulse. Matrix must revert to Hohmann or near-Hohmann "
            "cruise (lower entry velocity), giving up the round-trip-time gain. Surviving cell "
            "shifts back to soft-margin closure (16.3 yr at 32 t delivered). Recommend orchestrator "
            "revisit Round F's headline before integration."
        )

    lines.extend([
        "",
        "## Open follow-ons",
        "",
        "- **R-chunk-as-heat-shield-revisit (Saturn-scoped, deferred to future worker):** orientation "
        "stability through 200-second pulse. Not closed by this round.",
        "- **R-tug-thermal-survival:** what happens to the tug if chunk orientation fails or chunk "
        "disintegrates mid-pulse? This round assumes tug survives behind chunk; not validated.",
        "- **R-aerocapture-economic-cost-of-LGA-wait:** if closure is LGA-conditional, what's the "
        "mission-cadence penalty from waiting for favorable lunar-Earth-Saturn geometry?",
        "- **R-outbound-kick-economics (orthogonal but related):** Round F uses 715 t of hydrolox "
        "per outbound mission. At Earth-launch costs, this propellant alone may dwarf mission "
        "revenue. Closing this would reframe \"Variant C closes\" at the economic level "
        "regardless of aerocapture envelope.",
    ])

    (outdir / "closure_verdict.md").write_text("\n".join(lines))


def main() -> None:
    here = Path(__file__).resolve().parent
    outdir = here / "results"
    outdir.mkdir(parents=True, exist_ok=True)
    result = run()
    (outdir / "R_aerocapture_fast_cruise_envelope.json").write_text(
        json.dumps(result, indent=2, default=float)
    )
    write_tables(result, outdir)
    # write_verdict is disabled: the verdict file is hand-written because the
    # auto-generated text could not capture the upstream-misread finding that
    # cascaded from Saturn's SCOPE.md cherry-pick of R-chunk-as-heat-shield.
    # Re-running this script will NOT overwrite results/closure_verdict.md.
    _ = write_verdict
    # Print a brief summary to stdout for terminal observation
    cv = result["round_f_closing_case_verdict"]
    closing = cv["no_lga"]
    print(f"Closing case (aphelion 11 AU, no LGA): v_entry={closing['v_entry_km_s']:.2f} km/s, "
          f"q_peak={closing['q_peak_w_cm2']:.0f} W/cm², ablation={closing['ablation_pct_per_pass']:.2f}%, "
          f"peak_g={closing['peak_g_load']:.1f}, margin×={closing['tensile_margin']:.2f}, "
          f"envelope_pass={closing['envelope_pass']}")
    cc = result["cross_check_vs_RCAHS"]
    print(f"Cross-check vs R-chunk-as-heat-shield: ratio v_entry={cc['ratio']:.3f}, "
          f"q_peak {cc['computed_q_peak_w_cm2']:.0f} vs predicted {cc['predicted_q_peak_w_cm2']:.0f}")
    grading = result["hypothesis_grading"]
    agg = grading["aggregate"]
    print(f"Hypothesis aggregate: {agg['held_count']}/{agg['total']-1} held; "
          f"H-afce-agg: {'HELD' if agg['h_afce_agg_held'] else 'FALSIFIED'}")


if __name__ == "__main__":
    main()
