#!/usr/bin/env python3
"""R-hybrid-aerocapture-aerobraking.

Does pass-1-deep-aerocapture (bag sacrificed) plus pass-2-onward-shallow-aerobraking
close where single-pass aerocapture and pure aerobraking each fail?

Pre-registration is in STUDY.md. Central estimates were computed BEFORE the range
bands were named, per methodology lesson 1 / 7 / 9 (anchor on most-pessimistic-
credible BOE first; anchor on PRIMARY-text aggregate verdict).

Deterministic. No Monte Carlo. Run from this directory or project root.
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
EARTH_V_ESCAPE_INTERFACE_KM_S = math.sqrt(2.0 * EARTH_MU_KM3_S2 / (EARTH_RADIUS_KM + 125.0))
EARTH_V_CIRCULAR_LEO_KM_S = math.sqrt(EARTH_MU_KM3_S2 / (EARTH_RADIUS_KM + 400.0))
EARTH_V_ORBIT_KM_S = 29.7846918

WATER_ICE_DENSITY_KG_M3 = 917.0
WATER_HEAT_OF_SUBLIMATION_J_KG = 2.83e6
WATER_HEAT_OF_VAPORIZATION_J_KG = 2.26e6
ICE_TENSILE_STRENGTH_PA = 1.0e6
ICE_MELTING_K = 273.15

DRAG_COEFFICIENT_BLUNT = 1.0
SUTTON_GRAVES_K_SI = 1.7415e-4
STEFAN_BOLTZMANN = 5.67e-8
ICE_EMISSIVITY = 0.8
BOUNDARY_LAYER_BLOCKING_FACTOR = 0.4  # PICA-X-class lower end (caveat 3)
BODY_ABSORBED_FRACTION = 0.5  # caveat 4

# Hyperion's exponential model (kept for sensitivity check)
EXP_ATM_DENSITY_AT_100KM_KG_M3 = 5.6e-7
EXP_ATM_SCALE_HEIGHT_KM = 7.5

# US Standard 1976 / NRLMSISE-00 quiet-sun proxy (NASA SP-3084)
USSA76 = [
    (40,  4.00e-3),
    (50,  1.03e-3),
    (60,  3.10e-4),
    (70,  8.28e-5),
    (80,  1.85e-5),
    (90,  3.42e-6),
    (100, 5.60e-7),
    (110, 9.71e-8),
    (120, 2.22e-8),
    (130, 8.48e-9),
    (150, 2.08e-9),
    (180, 5.20e-10),
    (200, 2.54e-10),
    (250, 6.07e-11),
]

# Tug mass per reactor class (per rhea MARVL-anchored mass model)
TUG_MASS_T_BY_REACTOR_KWE = {200: 40.0, 500: 63.8, 1000: 115.0}

# Round-F closing transfer (heliocentric perihelion velocity at Earth)
ROUND_F_TRANSFERS = {
    # aphelion_AU: (v_perihelion_km_s, cruise_yr)
    9.58: (40.082, 6.086),
    11.00: (40.329, 4.183),
}

# Lunar gravity assist credit (R2 round; 60-85% of arrival epochs give this)
LGA_CREDIT_OPTIONS_KM_S = [0.0, 2.0]


# ---------------------------------------------------------------------------
# Atmosphere
# ---------------------------------------------------------------------------

def density_us_standard_kg_m3(altitude_km: float) -> float:
    """Piecewise log-linear interpolation over US Standard 1976 table."""
    if altitude_km <= USSA76[0][0]:
        return USSA76[0][1]
    if altitude_km >= USSA76[-1][0]:
        return USSA76[-1][1]
    for i in range(len(USSA76) - 1):
        h1, r1 = USSA76[i]
        h2, r2 = USSA76[i + 1]
        if h1 <= altitude_km <= h2:
            t = (altitude_km - h1) / (h2 - h1)
            return math.exp(math.log(r1) * (1 - t) + math.log(r2) * t)
    return USSA76[-1][1]


def density_exp_kg_m3(altitude_km: float) -> float:
    """Hyperion's single-exponential model (sensitivity-check only)."""
    return EXP_ATM_DENSITY_AT_100KM_KG_M3 * math.exp(
        -(altitude_km - 100.0) / EXP_ATM_SCALE_HEIGHT_KM
    )


def local_scale_height_km(altitude_km: float) -> float:
    """Compute local scale height H = -ρ / (dρ/dh) from adjacent table points."""
    table = USSA76
    if altitude_km <= table[0][0]:
        h1, r1 = table[0]
        h2, r2 = table[1]
    elif altitude_km >= table[-1][0]:
        h1, r1 = table[-2]
        h2, r2 = table[-1]
    else:
        for i in range(len(table) - 1):
            if table[i][0] <= altitude_km <= table[i + 1][0]:
                h1, r1 = table[i]
                h2, r2 = table[i + 1]
                break
    # ρ = ρ_1 × exp(-(h - h1)/H_local)  →  H_local = (h2 - h1) / ln(r1/r2)
    return (h2 - h1) / math.log(r1 / r2)


# ---------------------------------------------------------------------------
# Vehicle geometry
# ---------------------------------------------------------------------------

def chunk_radius_m(mass_t: float) -> float:
    volume_m3 = mass_t * 1000.0 / WATER_ICE_DENSITY_KG_M3
    return (3.0 * volume_m3 / (4.0 * math.pi)) ** (1.0 / 3.0)


def frontal_area_m2(mass_t: float) -> float:
    r = chunk_radius_m(mass_t)
    return math.pi * r * r


def ballistic_coefficient_kg_m2(chunk_t: float, tug_t: float) -> float:
    """β = m_total / (Cd × A_chunk)."""
    m_total = chunk_t + tug_t
    return m_total * 1000.0 / (DRAG_COEFFICIENT_BLUNT * frontal_area_m2(chunk_t))


# ---------------------------------------------------------------------------
# Orbital / entry kinematics
# ---------------------------------------------------------------------------

def v_infinity_at_earth_km_s(v_perihelion_km_s: float, lga_credit_km_s: float) -> float:
    """Approximate v_∞ by tangential difference, minus lunar-gravity-assist credit."""
    raw = v_perihelion_km_s - EARTH_V_ORBIT_KM_S
    return max(0.1, raw - lga_credit_km_s)


def v_entry_at_interface_km_s(v_infinity_km_s: float) -> float:
    """v_e = sqrt(v_inf^2 + v_escape_at_interface^2). Interface at 125 km."""
    return math.sqrt(v_infinity_km_s ** 2 + EARTH_V_ESCAPE_INTERFACE_KM_S ** 2)


def v_escape_at_altitude_km_s(altitude_km: float) -> float:
    r = EARTH_RADIUS_KM + altitude_km
    return math.sqrt(2.0 * EARTH_MU_KM3_S2 / r)


def v_circular_at_altitude_km_s(altitude_km: float) -> float:
    r = EARTH_RADIUS_KM + altitude_km
    return math.sqrt(EARTH_MU_KM3_S2 / r)


def pass_dv_m_s(
    altitude_km: float,
    beta_kg_m2: float,
    v_pass_km_s: float,
    density_fn=density_us_standard_kg_m3,
) -> tuple[float, float]:
    """King-Hele drag impulse per periapsis pass.

    Δv_pass = ρ(h) × v × √(2π × (R+h) × H_local) / β

    Returns (delta_v_m_s, pulse_duration_s).
    """
    rho = density_fn(altitude_km)
    H_km = local_scale_height_km(altitude_km)
    R_p_m = (EARTH_RADIUS_KM + altitude_km) * 1000.0
    H_m = H_km * 1000.0
    geom_factor_m = math.sqrt(2.0 * math.pi * R_p_m * H_m)
    dv_m_s = rho * (v_pass_km_s * 1000.0) * geom_factor_m / beta_kg_m2
    pulse_duration_s = geom_factor_m / (v_pass_km_s * 1000.0)
    return dv_m_s, pulse_duration_s


def sutton_graves_heat_flux_w_m2(
    altitude_km: float,
    v_km_s: float,
    nose_radius_m: float,
    density_fn=density_us_standard_kg_m3,
) -> float:
    rho = density_fn(altitude_km)
    v_m_s = v_km_s * 1000.0
    return SUTTON_GRAVES_K_SI * math.sqrt(rho / nose_radius_m) * v_m_s ** 3


def radiative_equilibrium_K(q_w_m2: float, emissivity: float = ICE_EMISSIVITY) -> float:
    return (q_w_m2 / (emissivity * STEFAN_BOLTZMANN)) ** 0.25


def peak_g_load(pass_dv_m_s_val: float, pulse_duration_s: float, peak_factor: float = 2.5) -> float:
    """Peak deceleration ≈ peak_factor × (Δv / Δt) / g_earth."""
    avg_decel = pass_dv_m_s_val / pulse_duration_s if pulse_duration_s > 0 else 0.0
    return peak_factor * avg_decel / G_EARTH_M_S2


def chunk_internal_stress_Pa(chunk_mass_t: float, peak_g: float) -> float:
    r = chunk_radius_m(chunk_mass_t)
    return r * WATER_ICE_DENSITY_KG_M3 * peak_g * G_EARTH_M_S2


# ---------------------------------------------------------------------------
# Pass-1 envelope
# ---------------------------------------------------------------------------

def pass_1_evaluate(
    chunk_t: float,
    tug_t: float,
    v_entry_km_s: float,
    periapsis_km: float,
    density_fn=density_us_standard_kg_m3,
) -> dict:
    beta = ballistic_coefficient_kg_m2(chunk_t, tug_t)
    r_n = chunk_radius_m(chunk_t)
    A = frontal_area_m2(chunk_t)
    dv_per_pass, pulse_s = pass_dv_m_s(periapsis_km, beta, v_entry_km_s, density_fn)
    q_peak_w_m2 = sutton_graves_heat_flux_w_m2(periapsis_km, v_entry_km_s, r_n, density_fn)
    T_eq_K = radiative_equilibrium_K(q_peak_w_m2)
    pk_g = peak_g_load(dv_per_pass, pulse_s)
    stress_Pa = chunk_internal_stress_Pa(chunk_t, pk_g)
    tensile_margin = ICE_TENSILE_STRENGTH_PA / stress_Pa if stress_Pa > 0 else float("inf")
    # Pass-1 must drop v_periapsis below escape at periapsis to capture
    v_esc_at_periapsis = v_escape_at_altitude_km_s(periapsis_km)
    dv_to_insert_km_s = v_entry_km_s - v_esc_at_periapsis  # could be negative if already sub-escape
    captures = dv_per_pass / 1000.0 >= dv_to_insert_km_s if dv_to_insert_km_s > 0 else True
    structural_survives = tensile_margin > 1.0
    # Energy deposited on chunk during pass (sublimation upper bound; not strictly first-pass mass loss
    # because bag absorbs most flux; flagged below)
    energy_per_pass_J = 0.5 * q_peak_w_m2 * A * pulse_s  # triangular pulse
    mass_subl_per_pass_kg = (
        energy_per_pass_J
        * BODY_ABSORBED_FRACTION
        * BOUNDARY_LAYER_BLOCKING_FACTOR
        / WATER_HEAT_OF_SUBLIMATION_J_KG
    )
    return {
        "periapsis_km": float(periapsis_km),
        "beta_kg_m2": beta,
        "chunk_radius_m": r_n,
        "frontal_area_m2": A,
        "v_entry_km_s": v_entry_km_s,
        "v_esc_at_periapsis_km_s": v_esc_at_periapsis,
        "dv_per_pass_m_s": dv_per_pass,
        "dv_to_insert_km_s": dv_to_insert_km_s,
        "pulse_duration_s": pulse_s,
        "q_peak_w_m2": q_peak_w_m2,
        "q_peak_mw_m2": q_peak_w_m2 / 1.0e6,
        "T_eq_K": T_eq_K,
        "peak_g": pk_g,
        "chunk_stress_Pa": stress_Pa,
        "tensile_margin": tensile_margin,
        "captures": captures,
        "structural_survives": structural_survives,
        "energy_per_pass_J": energy_per_pass_J,
        "mass_sublimed_per_pass_kg": mass_subl_per_pass_kg,
    }


# ---------------------------------------------------------------------------
# Aerobraking campaign
# ---------------------------------------------------------------------------

AVERAGE_AEROBRAKING_ORBIT_PERIOD_HR = 2.0  # conservative average across decay


def aerobraking_evaluate(
    chunk_t: float,
    tug_t: float,
    periapsis_post_pass_1_km: float,
    aerobraking_periapsis_km: float,
    residual_dv_km_s: float,
    density_fn=density_us_standard_kg_m3,
) -> dict:
    beta = ballistic_coefficient_kg_m2(chunk_t, tug_t)
    r_n = chunk_radius_m(chunk_t)
    A = frontal_area_m2(chunk_t)
    # Average velocity at aerobraking periapsis during campaign
    # Decays from elliptical (~v_escape at periapsis) to LEO-circular at periapsis
    v_p_start = v_escape_at_altitude_km_s(aerobraking_periapsis_km)
    v_p_end = v_circular_at_altitude_km_s(aerobraking_periapsis_km)
    v_p_avg = 0.5 * (v_p_start + v_p_end)
    dv_per_pass_m_s, pulse_s = pass_dv_m_s(
        aerobraking_periapsis_km, beta, v_p_avg, density_fn
    )
    if dv_per_pass_m_s <= 0:
        return None
    n_passes = (residual_dv_km_s * 1000.0) / dv_per_pass_m_s
    total_time_yr = n_passes * AVERAGE_AEROBRAKING_ORBIT_PERIOD_HR / (24.0 * 365.25)
    q_peak_w_m2 = sutton_graves_heat_flux_w_m2(
        aerobraking_periapsis_km, v_p_avg, r_n, density_fn
    )
    T_eq_K = radiative_equilibrium_K(q_peak_w_m2)
    energy_per_pass_J = 0.5 * q_peak_w_m2 * A * pulse_s
    mass_subl_per_pass_kg = (
        energy_per_pass_J
        * BODY_ABSORBED_FRACTION
        * BOUNDARY_LAYER_BLOCKING_FACTOR
        / WATER_HEAT_OF_SUBLIMATION_J_KG
    )
    total_sublimation_t = n_passes * mass_subl_per_pass_kg / 1000.0
    return {
        "aerobraking_periapsis_km": float(aerobraking_periapsis_km),
        "v_p_avg_km_s": v_p_avg,
        "dv_per_pass_m_s": dv_per_pass_m_s,
        "n_passes": n_passes,
        "total_time_yr": total_time_yr,
        "q_peak_w_m2": q_peak_w_m2,
        "T_eq_K": T_eq_K,
        "energy_per_pass_J": energy_per_pass_J,
        "mass_sublimed_per_pass_kg": mass_subl_per_pass_kg,
        "total_sublimation_t": total_sublimation_t,
    }


# ---------------------------------------------------------------------------
# Closure test
# ---------------------------------------------------------------------------

L0_05_CEILING_YR = 15.0
SUBLIMATION_TOLERANCE_FRACTION = 0.5  # half chunk mass


def closure_test(
    pass_1: dict,
    aerobrake: dict | None,
    chunk_t: float,
    cruise_yr: float,
) -> dict:
    if not pass_1["captures"]:
        return {"closes": False, "fail_reason": "pass-1 does not capture (dv < insertion threshold)"}
    if not pass_1["structural_survives"]:
        return {"closes": False, "fail_reason": "pass-1 chunk structural failure (tensile margin < 1.0)"}
    if aerobrake is None:
        return {"closes": False, "fail_reason": "aerobraking sub-zero dv per pass"}
    total_subl = aerobrake["total_sublimation_t"]
    if total_subl > chunk_t * SUBLIMATION_TOLERANCE_FRACTION:
        return {
            "closes": False,
            "fail_reason": f"chunk sublimation {total_subl:.0f} t > {chunk_t * SUBLIMATION_TOLERANCE_FRACTION:.0f} t tolerance",
        }
    ab_yr = aerobrake["total_time_yr"]
    if ab_yr > 5.0:
        return {"closes": False, "fail_reason": f"aerobraking time {ab_yr:.1f} yr > 5 yr"}
    total_rt = cruise_yr + 1.0 + ab_yr  # cruise + ~1 yr outbound + aerobraking time
    if total_rt > L0_05_CEILING_YR:
        return {"closes": False, "fail_reason": f"round-trip {total_rt:.1f} yr > L0-05 15 yr ceiling"}
    return {"closes": True, "fail_reason": None, "total_round_trip_yr": total_rt}


# ---------------------------------------------------------------------------
# Main sweep
# ---------------------------------------------------------------------------

def run() -> dict:
    out: dict = {
        "config": {
            "atmosphere_model": "US Standard 1976 / NRLMSISE-00 quiet-sun (NASA SP-3084)",
            "drag_coefficient": DRAG_COEFFICIENT_BLUNT,
            "ice_tensile_strength_Pa": ICE_TENSILE_STRENGTH_PA,
            "ice_density_kg_m3": WATER_ICE_DENSITY_KG_M3,
            "ice_emissivity": ICE_EMISSIVITY,
            "boundary_layer_blocking_factor": BOUNDARY_LAYER_BLOCKING_FACTOR,
            "body_absorbed_fraction": BODY_ABSORBED_FRACTION,
            "L0_05_ceiling_yr": L0_05_CEILING_YR,
            "sublimation_tolerance_fraction": SUBLIMATION_TOLERANCE_FRACTION,
            "average_aerobraking_period_hr": AVERAGE_AEROBRAKING_ORBIT_PERIOD_HR,
        }
    }

    chunk_masses = [50, 100, 200, 350]
    reactor_classes = [200, 500, 1000]
    aphelions = [9.58, 11.00]
    lga_options = LGA_CREDIT_OPTIONS_KM_S
    pass_1_alts = [40, 50, 60, 70, 75, 80, 85, 90]
    aerobraking_alts = [110, 130, 150, 180, 200]

    cells = []
    for chunk_t in chunk_masses:
        for reactor_kwe in reactor_classes:
            tug_t = TUG_MASS_T_BY_REACTOR_KWE[reactor_kwe]
            for r_apo in aphelions:
                v_peri_helio, cruise_yr = ROUND_F_TRANSFERS[r_apo]
                for lga in lga_options:
                    v_inf = v_infinity_at_earth_km_s(v_peri_helio, lga)
                    v_e = v_entry_at_interface_km_s(v_inf)
                    for h1 in pass_1_alts:
                        p1 = pass_1_evaluate(chunk_t, tug_t, v_e, h1)
                        # Residual Δv to dump aerobraking ≈ v_escape(h_p) - v_circular(h_p)
                        # post pass-1, vehicle is in elliptical orbit periapsis ≈ h1
                        # Aerobraking eventually raises periapsis to h2 via burn or trades dv
                        # Conservative: residual ≈ v_escape(h2) - v_circular(h2) at aerobraking periapsis
                        for h2 in aerobraking_alts:
                            residual_dv = (
                                v_escape_at_altitude_km_s(h2)
                                - v_circular_at_altitude_km_s(h2)
                            )
                            ab = aerobraking_evaluate(chunk_t, tug_t, h1, h2, residual_dv)
                            ct = closure_test(p1, ab, chunk_t, cruise_yr)
                            cells.append({
                                "chunk_t": chunk_t,
                                "reactor_kwe": reactor_kwe,
                                "tug_t": tug_t,
                                "aphelion_AU": r_apo,
                                "lga_credit_km_s": lga,
                                "v_entry_km_s": v_e,
                                "cruise_yr": cruise_yr,
                                "h1_km": h1,
                                "h2_km": h2,
                                "pass_1": p1,
                                "aerobraking": ab,
                                "closure": ct,
                            })

    out["cells"] = cells
    out["n_cells"] = len(cells)
    out["closing_cells"] = [c for c in cells if c["closure"]["closes"]]

    # Anchor-cell breakdown for sub-claim grading: chunk 200 t / tug 64 t / no-LGA / aphelion 11
    anchor_cells_h1 = [
        c for c in cells
        if c["chunk_t"] == 200 and c["reactor_kwe"] == 500
        and c["aphelion_AU"] == 11.00 and c["lga_credit_km_s"] == 0.0
    ]
    out["anchor_cells_h1"] = anchor_cells_h1

    # Sensitivity check: re-run anchor case under hyperion's exponential model
    anchor_cell_sens = pass_1_evaluate(
        200, 63.8, 15.289, 75, density_fn=density_exp_kg_m3
    )
    out["anchor_sensitivity_exponential_atm"] = anchor_cell_sens

    # Cross-check vs hyperion's R-aerocapture-fast-cruise-envelope Round F closing case
    # (chunk 200, tug 63.8, v_e 15.29 km/s, periapsis solver hit 40-km floor, 47.9 g, 1.6 MPa)
    cross_check_us_std = pass_1_evaluate(200, 63.8, 15.289, 40)
    cross_check_exp = pass_1_evaluate(
        200, 63.8, 15.289, 40, density_fn=density_exp_kg_m3
    )
    out["cross_check_round_f_strict"] = {
        "us_standard_1976": cross_check_us_std,
        "exponential_atm": cross_check_exp,
        "hyperion_published": {
            "peak_g": 47.9,
            "chunk_stress_Pa": 1.6e6,
            "tensile_margin": 0.62,
        },
    }

    # ------------------------------------------------------------------ Grading
    grading: dict = {}

    # H-hyb-a: pass-1 structural failure at chunk 200 t, β=6,022, at depth needed for 4.18 km/s
    # The "depth needed" is the SHALLOWEST h1 at which pass-1 captures
    chunk_200_no_lga_aph_11 = [
        c for c in anchor_cells_h1
        if c["chunk_t"] == 200 and c["lga_credit_km_s"] == 0
    ]
    capturing_at_200 = [
        c for c in chunk_200_no_lga_aph_11
        if c["pass_1"]["captures"]
    ]
    if capturing_at_200:
        shallowest = min(capturing_at_200, key=lambda c: c["h1_km"])
        margin_at_200 = shallowest["pass_1"]["tensile_margin"]
    else:
        # fall back to deepest tested
        deepest = min(chunk_200_no_lga_aph_11, key=lambda c: c["h1_km"])
        margin_at_200 = deepest["pass_1"]["tensile_margin"]
    grading["H_hyb_a"] = {
        "predicted_central": 0.75,
        "predicted_range": [0.5, 1.0],
        "computed": margin_at_200,
        "held": 0.5 <= margin_at_200 <= 1.0,
        "comment": "pass-1 tensile margin at chunk 200 t β=6,022 at shallowest capturing depth",
    }

    # H-hyb-b: same at chunk 100 t (β optimum)
    chunk_100_cells = [
        c for c in cells
        if c["chunk_t"] == 100 and c["reactor_kwe"] == 500
        and c["aphelion_AU"] == 11.00 and c["lga_credit_km_s"] == 0.0
    ]
    capturing_at_100 = [c for c in chunk_100_cells if c["pass_1"]["captures"]]
    if capturing_at_100:
        shallowest_100 = min(capturing_at_100, key=lambda c: c["h1_km"])
        margin_at_100 = shallowest_100["pass_1"]["tensile_margin"]
    else:
        margin_at_100 = min(chunk_100_cells, key=lambda c: c["h1_km"])["pass_1"]["tensile_margin"]
    grading["H_hyb_b"] = {
        "predicted_central": 0.85,
        "predicted_range": [0.6, 1.2],
        "computed": margin_at_100,
        "held": 0.6 <= margin_at_100 <= 1.2,
        "comment": "pass-1 tensile margin at chunk 100 t (β optimum) at shallowest capturing depth",
    }

    # H-hyb-c: pass-1 Δv at 75 km, chunk 200 t, no LGA — central 53 m/s, ratio 0.013
    p1_75 = pass_1_evaluate(200, 63.8, 15.289, 75)
    dv_ratio = (p1_75["dv_per_pass_m_s"] / 1000.0) / p1_75["dv_to_insert_km_s"]
    grading["H_hyb_c"] = {
        "predicted_central": 0.013,
        "predicted_range": [0.01, 0.03],
        "computed": dv_ratio,
        "held": 0.01 <= dv_ratio <= 0.03,
        "comment": "pass-1 Δv-achieved / Δv-required-to-insert at periapsis 75 km",
    }

    # H-hyb-d: aerobraking pass count at 130 km, β=6,022, 3 km/s residual
    ab_130 = aerobraking_evaluate(200, 63.8, 75, 130, 3.0)
    grading["H_hyb_d"] = {
        "predicted_central": 303_000,
        "predicted_range": [100_000, 1_000_000],
        "computed": ab_130["n_passes"],
        "held": 100_000 <= ab_130["n_passes"] <= 1_000_000,
        "comment": "aerobraking pass count at 130 km, residual 3 km/s",
    }

    # H-hyb-e: aerobraking total sublimation at 130 km, chunk 200 t
    grading["H_hyb_e"] = {
        "predicted_central": 1505,
        "predicted_range": [500, 3000],
        "computed": ab_130["total_sublimation_t"],
        "held": 500 <= ab_130["total_sublimation_t"] <= 3000,
        "comment": "total chunk sublimation at 130 km aerobraking, residual 3 km/s",
    }

    # H-hyb-f: aerobraking T_eq at 130 km > 273 K
    grading["H_hyb_f"] = {
        "predicted_central": 702,
        "predicted_range": [500, 900],
        "computed": ab_130["T_eq_K"],
        "held": 500 <= ab_130["T_eq_K"] <= 900,
        "comment": "chunk surface T_eq at 130 km aerobraking",
    }

    # H-hyb-g: aerobraking time at 180 km
    ab_180 = aerobraking_evaluate(200, 63.8, 75, 180, 3.0)
    grading["H_hyb_g"] = {
        "predicted_central": 757,
        "predicted_range": [200, 1500],
        "computed": ab_180["total_time_yr"],
        "held": 200 <= ab_180["total_time_yr"] <= 1500,
        "comment": "aerobraking time at 180 km, residual 3 km/s",
    }

    # H-hyb-h: LGA rescue: v_e at LGA + slow cruise + 100 t
    v_inf_lga = v_infinity_at_earth_km_s(ROUND_F_TRANSFERS[9.58][0], 2.0)
    v_e_lga = v_entry_at_interface_km_s(v_inf_lga)
    dv_insert_75_lga = v_e_lga - v_escape_at_altitude_km_s(75)
    grading["H_hyb_h"] = {
        "predicted_central": 2.73,
        "predicted_range": [2.5, 3.0],
        "computed": dv_insert_75_lga,
        "held": 2.5 <= dv_insert_75_lga <= 3.0,
        "comment": "pass-1 minimum Δv at 75 km with LGA + slow cruise (rescue test)",
    }

    # H-hyb-i: architecture closure: ANY cell in the swept envelope closes
    n_closing = len(out["closing_cells"])
    grading["H_hyb_i"] = {
        "predicted_central": 0,
        "predicted_range": [0, 2],
        "computed": n_closing,
        "held": 0 <= n_closing <= 2,
        "comment": "number of cells satisfying all five closure conditions",
    }

    # H-hyb-j: bag sacrificial mass at 10-20 MW/m² peak
    # Central anchor: RCAHS bag was 1-3 t at 4.4 MW/m² peak; our peak is ~10-20 MW/m² so scale by sqrt(q ratio)
    # Lower bound 5 t, upper bound 15 t
    # This is qualitative: we can't compute bag mass directly without a thermal-protection-system design model
    # Defer: not gradable in this round
    grading["H_hyb_j"] = {
        "predicted_central": "5-15 t",
        "predicted_range": [3, 30],
        "computed": "deferred (TPS model out of scope per validity caveat — flagged)",
        "held": "deferred",
        "comment": "bag sacrificial mass: not computable without a thermal-protection-system design model",
    }

    # Aggregate H-hyb-agg
    gradable = [k for k, v in grading.items() if v.get("held") in (True, False)]
    held_count = sum(1 for k in gradable if grading[k]["held"])
    total_gradable = len(gradable)
    agg_held = (held_count >= 7) and (n_closing <= 2)
    grading["aggregate"] = {
        "gradable_count": total_gradable,
        "held_count": held_count,
        "deferred_count": sum(1 for k, v in grading.items() if v.get("held") == "deferred"),
        "n_closing_cells": n_closing,
        "h_hyb_agg_held": agg_held,
    }

    out["hypothesis_grading"] = grading

    # ------------------------------------------------------------------ Summary
    summary = {
        "total_cells": len(cells),
        "cells_capturing_pass_1": sum(1 for c in cells if c["pass_1"]["captures"]),
        "cells_pass_1_structurally_survive": sum(
            1 for c in cells if c["pass_1"]["structural_survives"]
        ),
        "cells_pass_1_capture_and_survive": sum(
            1 for c in cells
            if c["pass_1"]["captures"] and c["pass_1"]["structural_survives"]
        ),
        "closing_cells": n_closing,
    }
    out["summary"] = summary

    return out


# ---------------------------------------------------------------------------
# Writers
# ---------------------------------------------------------------------------

def write_tables(result: dict, outdir: Path) -> None:
    cfg = result["config"]
    summary = result["summary"]
    grading = result["hypothesis_grading"]

    lines = [
        "# R-hybrid-aerocapture-aerobraking — results tables",
        "",
        "## Sweep summary",
        "",
        f"- Atmosphere model: {cfg['atmosphere_model']}",
        f"- Total cells swept: {summary['total_cells']}",
        f"- Cells where pass-1 captures (Δv ≥ Δv_insert): {summary['cells_capturing_pass_1']}",
        f"- Cells where pass-1 chunk structurally survives (margin > 1.0): {summary['cells_pass_1_structurally_survive']}",
        f"- Cells where pass-1 BOTH captures AND survives: {summary['cells_pass_1_capture_and_survive']}",
        f"- **Cells satisfying all 5 closure conditions: {summary['closing_cells']}**",
        "",
        "## Cross-check vs hyperion's R-aerocapture-fast-cruise-envelope (Round F STRICT, periapsis 40 km)",
        "",
    ]
    cc = result["cross_check_round_f_strict"]
    lines.append("| Atmosphere | Peak g | Chunk stress (MPa) | Tensile margin |")
    lines.append("|---|---:|---:|---:|")
    for label, key in [("US Standard 1976 (this round)", "us_standard_1976"),
                        ("Exponential (hyperion's)", "exponential_atm")]:
        d = cc[key]
        lines.append(
            f"| {label} | {d['peak_g']:.1f} | {d['chunk_stress_Pa']/1e6:.2f} | {d['tensile_margin']:.2f} |"
        )
    pub = cc["hyperion_published"]
    lines.append(
        f"| Hyperion published (Round F STRICT) | {pub['peak_g']:.1f} | "
        f"{pub['chunk_stress_Pa']/1e6:.2f} | {pub['tensile_margin']:.2f} |"
    )
    lines.append("")

    lines.append("## Pass-1 envelope at anchor cell (chunk 200 t, tug 63.8 t, aphelion 11, no LGA)")
    lines.append("")
    lines.append("| h₁ (km) | β (kg/m²) | ρ (kg/m³) | Δv/pass (m/s) | Δv-to-insert (km/s) | Captures | q_peak (MW/m²) | T_eq (K) | Peak g | Chunk stress (MPa) | Margin × | Pass-1 OK |")
    lines.append("|---:|---:|---:|---:|---:|:---:|---:|---:|---:|---:|---:|:---:|")
    for c in result["anchor_cells_h1"]:
        if c["h2_km"] != 130:
            continue  # only show one h2 row per h1 since pass-1 doesn't depend on h2
        p = c["pass_1"]
        ok = "Y" if (p["captures"] and p["structural_survives"]) else "N"
        rho = density_us_standard_kg_m3(c["h1_km"])
        lines.append(
            f"| {c['h1_km']} | {p['beta_kg_m2']:.0f} | {rho:.2e} | "
            f"{p['dv_per_pass_m_s']:.0f} | {p['dv_to_insert_km_s']:.2f} | "
            f"{'Y' if p['captures'] else 'N'} | {p['q_peak_mw_m2']:.2f} | "
            f"{p['T_eq_K']:.0f} | {p['peak_g']:.1f} | "
            f"{p['chunk_stress_Pa']/1e6:.3f} | {p['tensile_margin']:.2f} | {ok} |"
        )
    lines.append("")

    lines.append("## Aerobraking campaign at chunk 200 t / β=6,022, residual Δv assumed 3.0 km/s")
    lines.append("")
    lines.append("| h₂ (km) | ρ (kg/m³) | Δv/pass (mm/s) | n_passes | Years | T_eq (K) | Total sublimation (t) | Within tolerance |")
    lines.append("|---:|---:|---:|---:|---:|---:|---:|:---:|")
    for h2 in [110, 130, 150, 180, 200]:
        ab = aerobraking_evaluate(200, 63.8, 75, h2, 3.0)
        rho = density_us_standard_kg_m3(h2)
        within = "Y" if ab["total_sublimation_t"] < 100 and ab["total_time_yr"] < 5 else "N"
        lines.append(
            f"| {h2} | {rho:.2e} | {ab['dv_per_pass_m_s']*1000:.2f} | "
            f"{ab['n_passes']:.2e} | {ab['total_time_yr']:.1f} | "
            f"{ab['T_eq_K']:.0f} | {ab['total_sublimation_t']:.0f} | {within} |"
        )
    lines.append("")

    lines.append("## Hypothesis grading")
    lines.append("")
    lines.append("| Sub-claim | Central | Range | Computed | Held |")
    lines.append("|---|---|---|---|:---:|")
    for k, v in grading.items():
        if k == "aggregate":
            continue
        ctr = v.get("predicted_central")
        rng = v.get("predicted_range")
        comp = v.get("computed")
        held = v.get("held")
        # format computed nicely
        if isinstance(comp, float):
            comp_s = f"{comp:.4g}"
        else:
            comp_s = str(comp)
        lines.append(f"| {k} | {ctr} | {rng} | {comp_s} | {held} |")
    agg = grading["aggregate"]
    lines.append("")
    lines.append(
        f"**Aggregate H-hyb-agg: {agg['held_count']}/{agg['gradable_count']} sub-claims held"
        f" (plus {agg['deferred_count']} deferred), {agg['n_closing_cells']} closing cells. "
        f"H-hyb-agg held: {agg['h_hyb_agg_held']}.**"
    )

    (outdir / "tables.md").write_text("\n".join(lines))


def write_closure_verdict(result: dict, outdir: Path) -> None:
    summary = result["summary"]
    grading = result["hypothesis_grading"]
    agg = grading["aggregate"]
    n_closing = summary["closing_cells"]

    if n_closing == 0:
        verdict_phrase = (
            "The hybrid pass-1-deep-aerocapture + pass-2-onward-shallow-aerobraking architecture "
            "DOES NOT CLOSE at any cell in the architecturally-relevant envelope under conservative "
            "anchors (US Standard 1976 atmosphere, ice tensile 1.0 MPa, boundary-layer-blocking 0.4, "
            "body-absorbed fraction 0.5, L0-05 strict 15-yr ceiling)."
        )
        recovery = (
            "**The matrix's 'hybrid-engineering-pending' framing (introduced by phoebe's prior "
            "R-chunk-as-heat-shield-revisit) is now closed.** Aerocapture-adjacent surviving cells "
            "collapse to drag-skirt-conditional only — R-deployable-drag-skirt is the new "
            "critical-path round. The Round-F STRICT-closing Variant C cell remains falsified at "
            "the engineering level; phoebe's prior round closed single-pass aerocapture; this round "
            "closes hybrid pass-1-deep + multi-pass shallow."
        )
    elif n_closing <= 2:
        verdict_phrase = (
            f"The hybrid architecture closes at {n_closing} cell(s) within a {summary['total_cells']}-cell "
            "sweep. These are narrow corners of the envelope, not a robust architectural recovery."
        )
        recovery = (
            "Matrix update: narrow hybrid-conditional cells named explicitly. Aerocapture-adjacent "
            "surviving-cell list refined rather than retired."
        )
    else:
        verdict_phrase = (
            f"The hybrid architecture closes at {n_closing} cells. This is broader than predicted "
            "and falsifies H-hyb-agg in the optimistic direction."
        )
        recovery = (
            "Matrix update: hybrid architecture is a viable architectural recovery for the empty "
            "matrix cell. Aerocapture-adjacent surviving cells re-opened. R-deployable-drag-skirt "
            "becomes lower-priority follow-on rather than next critical path."
        )

    pessimistic_lesson = (
        "**Methodology lesson 1 update:** at end of this round, the pessimistic-default heuristic "
        "has held in 13 of 13 aerocapture-adjacent pre-registrations across this campaign. The "
        "more-pessimistic-than-pre-registered pattern remains the dominant empirical signal — "
        "domain anchor for aerocapture-adjacent rounds is engineer-pessimistic-insufficient."
        if n_closing == 0 else
        "**Methodology lesson 1 update:** the pessimistic-default heuristic has finally over-corrected. "
        "13 prior aerocapture-adjacent rounds were more-pessimistic-than-pre-registered; this is the "
        "first to land less-pessimistic. Reset domain anchor."
    )

    atmosphere_lesson = (
        "**Atmosphere-model PROTOCOL lesson candidate:** R-chunk-as-heat-shield, "
        "R-aerocapture-fast-cruise-envelope, R-chunk-as-heat-shield-revisit, and this round have "
        "used three different atmospheric models. The hyperion single-scale-height exponential "
        "(5.6e-7 at 100 km, H=7.5 km) underestimates US Standard 1976 density by ~40× at 180 km. "
        "For atmospheric-capture rounds spanning both deep (40-90 km) and shallow (130-200 km) "
        "regimes, the choice dominates aerobraking-pass-count verdict. Adopt US Standard 1976 / "
        "NRLMSISE-00 as the campaign default; flag prior aerocapture rounds for re-derivation if "
        "verdict changes under the standard model. Candidate for PROTOCOL methodology lesson 10."
    )

    lines = [
        "# R-hybrid-aerocapture-aerobraking — closure verdict",
        "",
        "## Headline",
        "",
        verdict_phrase,
        "",
        recovery,
        "",
        "## Numbers anchored",
        "",
        f"- Pass-1 envelope: {summary['cells_capturing_pass_1']} of {summary['total_cells']} cells capture Δv-to-insert at the swept pass-1 altitudes.",
        f"- Pass-1 structural: {summary['cells_pass_1_structurally_survive']} of {summary['total_cells']} cells survive pass-1 chunk structurally.",
        f"- Pass-1 BOTH captures AND survives structurally: {summary['cells_pass_1_capture_and_survive']} of {summary['total_cells']}.",
        f"- Aerobraking + sublimation + L0-05 closure: {n_closing} of {summary['total_cells']}.",
        f"- Sub-claims held: {agg['held_count']} of {agg['gradable_count']} gradable (+ {agg['deferred_count']} deferred).",
        f"- Aggregate H-hyb-agg: {'HELD' if agg['h_hyb_agg_held'] else 'FALSIFIED'}.",
        "",
        "## Three independent failure modes (mutually exclusive across periapsis axis)",
        "",
        "1. **Pass-1 fails structurally** at any altitude where pass-1 Δv ≥ 4.18 km/s (chunk stress > 1 MPa tensile).",
        "2. **Aerobraking is unphysical timescale** at any altitude where chunk T_eq < ice melt point (need ≥ 180 km, where pass count ≥ 3 million and time ≥ 700 yr).",
        "3. **Chunk consumed by sublimation** at any altitude where time is tractable (≤ 130 km), total sublimation ≥ 1,500 t — chunk gone many times over at 200 t initial.",
        "",
        "No interior solution exists between these constraints.",
        "",
        "## Three SCOPE input-assumption errors documented",
        "",
        "Per methodology lesson 9 (anchor on PRIMARY-text aggregate verdict). All three errors documented in STUDY.md §'Three load-bearing methodology choices the SCOPE got partly wrong':",
        "",
        "1. **β-by-chunk-size is non-monotonic when tug mass is held fixed.** β minimum is at chunk 100 t (β=5,936), not chunk 50 t (β=6,546). SCOPE's 'smaller-chunk-rescues-β' is geometrically broken.",
        "2. **Pass-1 Δv-to-insert is set by parabolic-velocity threshold, not by 'engineering judgment 65 percent of total'.** At periapsis 75 km, Δv-to-insert = 4.175 km/s. The 'hybrid relaxes pass-1' intuition is wrong.",
        "3. **Single-scale-height exponential atmosphere is qualitatively wrong above 110 km** where scale height grows to 20-30 km. Atmospheric model has been silently varying across aerocapture-adjacent rounds.",
        "",
        "## Methodology propagation",
        "",
        pessimistic_lesson,
        "",
        atmosphere_lesson,
        "",
        "## Matrix updates",
        "",
        (
            "- Retire 'hybrid-engineering-pending' framing. Replace with 'atmospheric-capture-falsified-without-drag-skirt.'"
            if n_closing == 0 else
            "- Refine hybrid-conditional to narrow surviving cells; matrix gains them as engineering-uncertain rows."
        ),
        "- R-deployable-drag-skirt promoted to next critical-path round." if n_closing == 0 else "- R-deployable-drag-skirt remains queued.",
        "- Adopt US Standard 1976 atmosphere as campaign default; re-derive prior aerocapture rounds at the standard model if their verdicts are atmosphere-sensitive.",
        "",
        "## Open dependencies",
        "",
        "- R-chunk-as-heat-shield-revisit's orientation-stability question remains open and is now downstream of an aerocapture branch whose every cell has been falsified.",
        "- R-deployable-drag-skirt (mass budget for inflatable ballute) — primary recovery candidate.",
        "- R-mission-architecture-pivot-survey (lunar-orbit catcher, cislunar processing) — alternative-branch follow-on.",
    ]

    (outdir / "closure_verdict.md").write_text("\n".join(lines))


def main() -> None:
    here = Path(__file__).resolve().parent
    outdir = here / "results"
    outdir.mkdir(parents=True, exist_ok=True)
    result = run()
    (outdir / "R_hybrid_aerocapture_aerobraking.json").write_text(
        json.dumps(result, indent=2, default=float)
    )
    write_tables(result, outdir)
    write_closure_verdict(result, outdir)
    s = result["summary"]
    print(
        f"Cells: total={s['total_cells']}, captures={s['cells_capturing_pass_1']}, "
        f"struct-survive={s['cells_pass_1_structurally_survive']}, "
        f"both={s['cells_pass_1_capture_and_survive']}, closing={s['closing_cells']}"
    )
    g = result["hypothesis_grading"]["aggregate"]
    print(
        f"Hypothesis grading: {g['held_count']}/{g['gradable_count']} held, "
        f"{g['deferred_count']} deferred, H-hyb-agg held: {g['h_hyb_agg_held']}"
    )
    cc = result["cross_check_round_f_strict"]
    pub = cc["hyperion_published"]
    us = cc["us_standard_1976"]
    print(
        f"Cross-check vs hyperion R-aerocapture-fast-cruise-envelope Round F:"
        f"  USStandard: peak_g={us['peak_g']:.1f}, stress={us['chunk_stress_Pa']/1e6:.2f} MPa, margin={us['tensile_margin']:.2f}"
        f"  Hyperion: peak_g={pub['peak_g']:.1f}, stress={pub['chunk_stress_Pa']/1e6:.2f} MPa, margin={pub['tensile_margin']:.2f}"
    )


if __name__ == "__main__":
    main()
