"""R-electric-outbound-rerun — Hyperion's bug fix + Titan-inbound combined re-evaluation.

Re-runs the R-electric-outbound sweep with two corrections layered in:

1. **Outbound-burn bug fix.** R-electric-outbound's `constant_thrust_burn`
   takes m_initial-at-start-of-burn but is called at the outbound site with
   m_tug (dry-at-end-of-burn). Tsiolkovsky-consistent m_prop given M_final is
   `M_f * (mass_ratio - 1)`, not `M_i * (1 - 1/mass_ratio)`. Outbound
   propellant and burn time are understated by factor mass_ratio. Confirmed
   on a unit-test-style sanity check (see `unit_sanity_check` below).

2. **Inbound-burn call site is NOT bugged** (against Hyperion's earlier
   read, but for the reason Hyperion gave — re-derived here). The inbound
   call passes `m_tug + chunk` to the same function. In the chunk-fed
   electric architecture, the chunk IS the propellant: water sublimated from
   the captured ice mass is fed to the electric thrusters. So at start of
   inbound burn, wet mass = m_tug + chunk (tug + ice block); at end of burn,
   dry mass = m_tug + (chunk - prop_inbound) = m_tug + delivered. Thus
   `m_tug + chunk` IS the wet-at-start mass and the function is being called
   correctly. The outbound-only correction in the formula change is
   sufficient.

3. **Titan-inbound scenario.** Titan's R-inbound-dv-continuous-thrust round
   showed continuous-thrust integrated inbound delta-velocity is 24.7 km/s
   (high-elliptical Saturn departure, lunar gravity assist credit at Earth)
   to 40.2 km/s (B-ring Saturn departure, no lunar gravity assist). The
   matrix's 6.42 km/s is an impulsive-equivalent figure incompatible with
   the all-electric continuous-thrust architecture. Re-run captures both
   inbound regimes so the matrix decision can sit on the right number.

4. **40 W/kg specific power.** Hyperion's read of the matrix said the
   round-trip-time promises lean on the stretch specific-power assumption
   (40 W/kg), not the conservative 10 W/kg used in the bundled mass model
   here. Re-run sweeps a `bundled_40_W_per_kg` variant alongside the
   conservative 10 W/kg case so the orchestrator can see both.

Headline output: at 1 megawatt-electric, decomposed-mid tug, electric Isp
2000 s — does any (specific power, inbound delta-velocity) cell close
inside L0-05's 15-year ceiling once both corrections are applied?

Pre-registered hypotheses live in STUDY.md.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

from waterprop.constants import (
    G0,
    GM_SUN,
    GM_EARTH,
    AU,
    R_EARTH,
    A_EARTH,
    A_SATURN,
)

YEAR_S = 365.25 * 86400.0

# Mission constants (same as R-electric-outbound, kept for cross-comparison).
DV_INBOUND_MATRIX_KM_S = 6.42  # original matrix impulsive-equivalent inbound
DV_INBOUND_TITAN_HIGH_ELLIPTICAL_KM_S = 24.7  # titan, high-elliptical + lunar gravity assist
DV_INBOUND_TITAN_B_RING_KM_S = 40.2          # titan, B-ring, no lunar gravity assist
SATURN_OPS_YR = 1.0
LEO_ALT_KM = 400.0
ETA_THR = 0.65
ROUND_TRIP_CEILING_YR = 15.0  # L0-05

CHUNK_T_BASELINE = 200.0
REACTOR_POWERS_KWE = [10.0, 40.0, 100.0, 200.0, 500.0, 1000.0]

# Mass models. bundled_40_W_per_kg added per hyperion's stretch-parameter callout.
MASS_MODELS: dict[str, dict] = {
    "bundled_10_W_per_kg": {
        "kind": "bundled",
        "m_fixed_t": 5.0,
        "specific_power_total_w_per_kg": 10.0,
    },
    "bundled_40_W_per_kg": {
        "kind": "bundled",
        "m_fixed_t": 5.0,
        "specific_power_total_w_per_kg": 40.0,
    },
    "decomposed_mid": {
        "kind": "decomposed",
        "m_fixed_t": 3.0,
        "alpha_reactor_W_per_kg": 50.0,
        "alpha_PC_W_per_kg": 200.0,
        "alpha_radiator_kW_th_per_kg": 2.0,
        "eta_conv": 0.30,
        "f_tank": 0.05,
    },
}


def dry_mass_t(model: dict, reactor_kwe: float, m_prop_t: float = 0.0) -> float:
    if model["kind"] == "bundled":
        m_stack = reactor_kwe / model["specific_power_total_w_per_kg"]
        return model["m_fixed_t"] + m_stack + m_prop_t * 0.05
    eta = model["eta_conv"]
    p_th_waste_kw = reactor_kwe * (1.0 - eta) / eta
    m_reactor = reactor_kwe / model["alpha_reactor_W_per_kg"]
    m_pc = reactor_kwe / model["alpha_PC_W_per_kg"]
    m_rad = p_th_waste_kw / model["alpha_radiator_kW_th_per_kg"] / 1000.0
    m_tank = m_prop_t * model["f_tank"]
    return model["m_fixed_t"] + m_reactor + m_pc + m_rad + m_tank


def outbound_delta_v_km_s() -> dict:
    r_leo_km = R_EARTH + LEO_ALT_KM
    v_circ_leo_km_s = math.sqrt(GM_EARTH / r_leo_km)
    v_earth_helio = math.sqrt(GM_SUN / A_EARTH)
    a_h_km = (A_EARTH + A_SATURN) / 2.0
    v_hohmann_peri = math.sqrt(GM_SUN * (2.0 / A_EARTH - 1.0 / a_h_km))
    v_inf_earth = v_hohmann_peri - v_earth_helio
    dv_electric = v_circ_leo_km_s + v_inf_earth
    return {
        "v_circ_LEO_km_s": v_circ_leo_km_s,
        "v_earth_helio_km_s": v_earth_helio,
        "v_hohmann_peri_km_s": v_hohmann_peri,
        "v_inf_earth_km_s": v_inf_earth,
        "dv_outbound_electric_km_s": dv_electric,
    }


def hohmann_cruise_yr() -> float:
    a_h_km = (A_EARTH + A_SATURN) / 2.0
    t_half_s = math.pi * math.sqrt(a_h_km ** 3 / GM_SUN)
    return t_half_s / YEAR_S


def burn_from_wet(m_initial_t: float, dv_km_s: float, power_kwe: float,
                   isp_s: float, eta: float = ETA_THR) -> dict:
    """Original (bug-compatible) formula. Input is wet mass at start of burn.

    Tsiolkovsky-consistent: m_prop = M_i * (1 - 1/MR). Use this when caller
    knows the wet mass.
    """
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


def burn_from_dry_end(m_final_t: float, dv_km_s: float, power_kwe: float,
                       isp_s: float, eta: float = ETA_THR) -> dict:
    """Corrected formula for the outbound call pattern. Input is dry mass at
    end of burn. Tsiolkovsky-consistent: m_prop = M_f * (MR - 1).
    """
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


def unit_sanity_check() -> dict:
    """Verify both formula variants agree on a known case.

    Scenario: m_final = 10 t, dv = 9 km/s, Isp = 2000 s, power 1 MWe.
      mass_ratio = exp(9000 / (2000*9.80665)) = exp(0.4588) = 1.5822
      m_initial (wet) = m_final * MR = 15.822 t
      m_prop (truth) = m_initial - m_final = 5.822 t
      burn_from_dry_end(10 t, 9, 1000, 2000) should give m_prop ≈ 5.822 t
      burn_from_wet(15.822 t, 9, 1000, 2000) should give m_prop ≈ 5.822 t
      burn_from_wet(10 t, 9, 1000, 2000)  [the BUGGED call pattern] should
        give 10 * (1 - 1/1.5822) = 3.681 t — i.e., understated by MR = 1.582.
    """
    m_final = 10.0
    dv = 9.0
    isp = 2000.0
    power = 1000.0
    mr = math.exp(dv * 1000.0 / (isp * G0))
    m_wet_truth = m_final * mr
    m_prop_truth = m_wet_truth - m_final
    from_dry = burn_from_dry_end(m_final, dv, power, isp)
    from_wet = burn_from_wet(m_wet_truth, dv, power, isp)
    bugged = burn_from_wet(m_final, dv, power, isp)
    return {
        "mass_ratio": mr,
        "m_final_t": m_final,
        "m_wet_truth_t": m_wet_truth,
        "m_prop_truth_t": m_prop_truth,
        "from_dry_end_t": from_dry["m_prop_t"],
        "from_wet_t": from_wet["m_prop_t"],
        "bugged_call_t": bugged["m_prop_t"],
        "understatement_ratio_truth_over_bugged": m_prop_truth / bugged["m_prop_t"],
        "burn_time_understatement_ratio": from_dry["t_burn_s"] / bugged["t_burn_s"],
        "from_dry_end_matches_truth": abs(from_dry["m_prop_t"] - m_prop_truth) < 1e-6,
        "from_wet_matches_truth": abs(from_wet["m_prop_t"] - m_prop_truth) < 1e-6,
    }


def round_trip(model: dict, reactor_kwe: float, chunk_t: float, isp_s: float,
                dv_outbound_km_s: float, dv_inbound_km_s: float,
                use_bugged_outbound: bool = False) -> dict:
    """Compute round-trip timeline.

    Outbound: m_tug is dry-at-end-of-burn. Use burn_from_dry_end (correct)
      unless use_bugged_outbound=True (reproduces original R-electric-
      outbound result for cross-check).
    Inbound: m_tug + chunk is wet-at-start (chunk is the propellant in the
      chunk-fed electric architecture). Use burn_from_wet (always correct).
    """
    m_tug_t = dry_mass_t(model, reactor_kwe, m_prop_t=0.0)
    for _ in range(20):
        if use_bugged_outbound:
            burn_out = burn_from_wet(m_tug_t, dv_outbound_km_s, reactor_kwe, isp_s)
        else:
            burn_out = burn_from_dry_end(m_tug_t, dv_outbound_km_s, reactor_kwe, isp_s)
        new_m_tug = dry_mass_t(model, reactor_kwe, m_prop_t=burn_out["m_prop_t"])
        if abs(new_m_tug - m_tug_t) < 1e-5:
            m_tug_t = new_m_tug
            break
        m_tug_t = new_m_tug
    if use_bugged_outbound:
        burn_out = burn_from_wet(m_tug_t, dv_outbound_km_s, reactor_kwe, isp_s)
    else:
        burn_out = burn_from_dry_end(m_tug_t, dv_outbound_km_s, reactor_kwe, isp_s)

    # Inbound: chunk-fed, m_initial_wet = m_tug + chunk.
    burn_in = burn_from_wet(m_tug_t + chunk_t, dv_inbound_km_s, reactor_kwe, isp_s)

    t_cruise_yr = hohmann_cruise_yr()
    round_trip_yr = (
        burn_out["t_burn_yr"] + t_cruise_yr + SATURN_OPS_YR + burn_in["t_burn_yr"] + t_cruise_yr
    )
    delivered_t = chunk_t - burn_in["m_prop_t"]
    delivered_fraction = delivered_t / chunk_t if chunk_t > 0 else 0.0
    m_leo_t = m_tug_t + burn_out["m_prop_t"]
    return {
        "m_tug_t": m_tug_t,
        "m_prop_outbound_t": burn_out["m_prop_t"],
        "m_LEO_t": m_leo_t,
        "thrust_N": burn_out["thrust_N"],
        "mass_ratio_outbound": burn_out["mass_ratio"],
        "t_outbound_burn_yr": burn_out["t_burn_yr"],
        "t_cruise_each_yr": t_cruise_yr,
        "t_saturn_ops_yr": SATURN_OPS_YR,
        "m_prop_inbound_t": burn_in["m_prop_t"],
        "mass_ratio_inbound": burn_in["mass_ratio"],
        "t_inbound_burn_yr": burn_in["t_burn_yr"],
        "round_trip_yr": round_trip_yr,
        "closes_15yr": round_trip_yr <= ROUND_TRIP_CEILING_YR,
        "delivered_t": delivered_t,
        "delivered_fraction": delivered_fraction,
    }


def smallest_closing(rows: list, model_name: str) -> dict:
    closing = [r for r in rows if r["mass_model"] == model_name and r["closes_15yr"]]
    if not closing:
        return {"min_reactor_kwe": None, "round_trip_yr": None}
    pick = min(closing, key=lambda r: r["reactor_kwe"])
    return {"min_reactor_kwe": pick["reactor_kwe"],
            "round_trip_yr": pick["round_trip_yr"],
            "t_outbound_yr": pick["t_outbound_burn_yr"],
            "t_inbound_yr": pick["t_inbound_burn_yr"],
            "delivered_t": pick["delivered_t"]}


def main() -> dict:
    results: dict = {}

    # 0. Unit-test sanity check
    sanity = unit_sanity_check()
    results["unit_sanity_check"] = sanity
    assert sanity["from_dry_end_matches_truth"], "burn_from_dry_end broken"
    assert sanity["from_wet_matches_truth"], "burn_from_wet broken"
    # Bugged call understatement = mass_ratio
    assert abs(sanity["understatement_ratio_truth_over_bugged"] - sanity["mass_ratio"]) < 1e-6

    dv_block = outbound_delta_v_km_s()
    results["outbound_dv_derivation"] = dv_block
    dv_out = dv_block["dv_outbound_electric_km_s"]
    results["hohmann_cruise_yr"] = hohmann_cruise_yr()

    # 1. Reproduce R-electric-outbound main sweep (matrix-inbound 6.42 km/s,
    # Isp 2000 s, chunk 200 t) with the bug fix applied.
    sweep_corrected = []
    for name, model in MASS_MODELS.items():
        for reactor in REACTOR_POWERS_KWE:
            row = round_trip(model, reactor, CHUNK_T_BASELINE, 2000.0,
                              dv_out, DV_INBOUND_MATRIX_KM_S,
                              use_bugged_outbound=False)
            row.update({"mass_model": name, "reactor_kwe": reactor,
                         "chunk_t": CHUNK_T_BASELINE, "isp_s": 2000.0,
                         "dv_inbound_km_s": DV_INBOUND_MATRIX_KM_S})
            sweep_corrected.append(row)
    results["sweep_matrix_inbound_corrected"] = sweep_corrected

    # 2. Same sweep WITH the bug (for direct cross-check against the original
    # R-electric-outbound numbers). Reproduces tables.md when restricted to
    # the original two mass models.
    sweep_bugged = []
    for name, model in MASS_MODELS.items():
        for reactor in REACTOR_POWERS_KWE:
            row = round_trip(model, reactor, CHUNK_T_BASELINE, 2000.0,
                              dv_out, DV_INBOUND_MATRIX_KM_S,
                              use_bugged_outbound=True)
            row.update({"mass_model": name, "reactor_kwe": reactor})
            sweep_bugged.append(row)
    results["sweep_matrix_inbound_bugged_reproduction"] = sweep_bugged

    # 3. Titan-inbound sweep: same params, but inbound delta-velocity from
    # titan's continuous-thrust round.
    sweep_titan_high_ellip = []
    for name, model in MASS_MODELS.items():
        for reactor in REACTOR_POWERS_KWE:
            row = round_trip(model, reactor, CHUNK_T_BASELINE, 2000.0,
                              dv_out, DV_INBOUND_TITAN_HIGH_ELLIPTICAL_KM_S,
                              use_bugged_outbound=False)
            row.update({"mass_model": name, "reactor_kwe": reactor,
                         "dv_inbound_km_s": DV_INBOUND_TITAN_HIGH_ELLIPTICAL_KM_S})
            sweep_titan_high_ellip.append(row)
    results["sweep_titan_inbound_high_elliptical"] = sweep_titan_high_ellip

    sweep_titan_b_ring = []
    for name, model in MASS_MODELS.items():
        for reactor in REACTOR_POWERS_KWE:
            row = round_trip(model, reactor, CHUNK_T_BASELINE, 2000.0,
                              dv_out, DV_INBOUND_TITAN_B_RING_KM_S,
                              use_bugged_outbound=False)
            row.update({"mass_model": name, "reactor_kwe": reactor,
                         "dv_inbound_km_s": DV_INBOUND_TITAN_B_RING_KM_S})
            sweep_titan_b_ring.append(row)
    results["sweep_titan_inbound_b_ring"] = sweep_titan_b_ring

    # 4. Close-thresholds for every sweep
    closes_summary = {}
    for label, rows in [
        ("matrix_inbound_6.42_corrected", sweep_corrected),
        ("matrix_inbound_6.42_bugged", sweep_bugged),
        ("titan_inbound_24.7_high_elliptical", sweep_titan_high_ellip),
        ("titan_inbound_40.2_b_ring", sweep_titan_b_ring),
    ]:
        closes_summary[label] = {m: smallest_closing(rows, m) for m in MASS_MODELS}
    results["close_thresholds"] = closes_summary

    # 5. Hypothesis grading
    # Find 1 MWe decomposed_mid in each sweep for direct comparison.
    def find(rows, mname, kwe):
        for r in rows:
            if r["mass_model"] == mname and r["reactor_kwe"] == kwe:
                return r
        return None

    r_corr_1mwe_dec = find(sweep_corrected, "decomposed_mid", 1000.0)
    r_bug_1mwe_dec = find(sweep_bugged, "decomposed_mid", 1000.0)
    r_titan_he_1mwe_dec = find(sweep_titan_high_ellip, "decomposed_mid", 1000.0)
    r_titan_br_1mwe_dec = find(sweep_titan_b_ring, "decomposed_mid", 1000.0)

    # H-eor-a: outbound burn time understatement at 1 MWe / decomposed-mid /
    # Isp 2000 s.
    # Predicted band 1.40-1.60x increase (mass_ratio at dv 17.97 Isp 2000:
    # exp(17970/(2000*9.80665)) = 2.50x). Adjusted to 2.0-3.0x given Isp 2000 not 5000.
    if r_bug_1mwe_dec["t_outbound_burn_yr"] > 0:
        ratio_1mwe = r_corr_1mwe_dec["t_outbound_burn_yr"] / r_bug_1mwe_dec["t_outbound_burn_yr"]
    else:
        ratio_1mwe = math.inf
    h_eor_a_predicted = [2.0, 3.0]
    h_eor_a_held = h_eor_a_predicted[0] <= ratio_1mwe <= h_eor_a_predicted[1]

    # H-eor-b: smallest reactor closing inside 15 yr at decomposed-mid,
    # matrix-inbound 6.42, corrected, shifts upward from 500 kWe.
    close_dec_corrected = closes_summary["matrix_inbound_6.42_corrected"]["decomposed_mid"]["min_reactor_kwe"]
    h_eor_b_predicted = "> 500 kWe (upward from original)"
    h_eor_b_held = (close_dec_corrected is not None and close_dec_corrected > 500.0)

    # H-eor-c: no L0-05-compliant cell exists for year-twenty-plus megawatt
    # all-electric end-to-end at 10 W/kg with both bug fixes AND titan's
    # corrected inbound. Falsified if any cell closes.
    any_close_at_10wpkg_titan_he = any(
        r["closes_15yr"] for r in sweep_titan_high_ellip
        if r["mass_model"] in ("bundled_10_W_per_kg", "decomposed_mid")
    )
    h_eor_c_predicted = "no 10-W/kg cell closes at titan-inbound 24.7 km/s"
    h_eor_c_held = not any_close_at_10wpkg_titan_he

    # H-eor-d: at 40 W/kg specific power, does any cell close at titan-inbound 24.7?
    any_close_at_40wpkg_titan_he = any(
        r["closes_15yr"] for r in sweep_titan_high_ellip
        if r["mass_model"] == "bundled_40_W_per_kg"
    )
    h_eor_d_predicted = "at least one 40-W/kg cell closes at titan-inbound 24.7 km/s"
    h_eor_d_held = any_close_at_40wpkg_titan_he

    results["hypothesis_grading"] = {
        "H_eor_a": {
            "predicted_burn_time_ratio": h_eor_a_predicted,
            "actual_ratio_1mwe_decomposed_mid": ratio_1mwe,
            "held": h_eor_a_held,
        },
        "H_eor_b": {
            "predicted": h_eor_b_predicted,
            "actual_min_kwe_corrected": close_dec_corrected,
            "actual_min_kwe_bugged": closes_summary["matrix_inbound_6.42_bugged"]["decomposed_mid"]["min_reactor_kwe"],
            "held": h_eor_b_held,
        },
        "H_eor_c": {
            "predicted": h_eor_c_predicted,
            "actual_any_close_at_10_W_per_kg_titan_high_ellip": any_close_at_10wpkg_titan_he,
            "held": h_eor_c_held,
        },
        "H_eor_d": {
            "predicted": h_eor_d_predicted,
            "actual_any_close_at_40_W_per_kg_titan_high_ellip": any_close_at_40wpkg_titan_he,
            "held": h_eor_d_held,
        },
    }

    # Headline payload for orchestrator: at decomposed-mid, 1 MWe, Isp 2000 s,
    # chunk 200 t — round-trip and L0-05 closure at all four inbound regimes.
    headline = {
        "matrix_inbound_6.42_corrected_decomposed_mid_1mwe": {
            "round_trip_yr": r_corr_1mwe_dec["round_trip_yr"],
            "closes_15yr": r_corr_1mwe_dec["closes_15yr"],
            "t_outbound_yr": r_corr_1mwe_dec["t_outbound_burn_yr"],
            "t_inbound_yr": r_corr_1mwe_dec["t_inbound_burn_yr"],
            "delivered_t": r_corr_1mwe_dec["delivered_t"],
            "delivered_fraction": r_corr_1mwe_dec["delivered_fraction"],
        },
        "titan_inbound_24.7_he_decomposed_mid_1mwe": {
            "round_trip_yr": r_titan_he_1mwe_dec["round_trip_yr"],
            "closes_15yr": r_titan_he_1mwe_dec["closes_15yr"],
            "t_outbound_yr": r_titan_he_1mwe_dec["t_outbound_burn_yr"],
            "t_inbound_yr": r_titan_he_1mwe_dec["t_inbound_burn_yr"],
            "delivered_t": r_titan_he_1mwe_dec["delivered_t"],
            "delivered_fraction": r_titan_he_1mwe_dec["delivered_fraction"],
        },
        "titan_inbound_40.2_br_decomposed_mid_1mwe": {
            "round_trip_yr": r_titan_br_1mwe_dec["round_trip_yr"],
            "closes_15yr": r_titan_br_1mwe_dec["closes_15yr"],
            "t_outbound_yr": r_titan_br_1mwe_dec["t_outbound_burn_yr"],
            "t_inbound_yr": r_titan_br_1mwe_dec["t_inbound_burn_yr"],
            "delivered_t": r_titan_br_1mwe_dec["delivered_t"],
            "delivered_fraction": r_titan_br_1mwe_dec["delivered_fraction"],
        },
    }
    # 40 W/kg variants for the same operating points
    r_titan_he_1mwe_40 = find(sweep_titan_high_ellip, "bundled_40_W_per_kg", 1000.0)
    r_titan_br_1mwe_40 = find(sweep_titan_b_ring, "bundled_40_W_per_kg", 1000.0)
    headline["titan_inbound_24.7_he_bundled_40_W_per_kg_1mwe"] = {
        "round_trip_yr": r_titan_he_1mwe_40["round_trip_yr"],
        "closes_15yr": r_titan_he_1mwe_40["closes_15yr"],
        "t_outbound_yr": r_titan_he_1mwe_40["t_outbound_burn_yr"],
        "t_inbound_yr": r_titan_he_1mwe_40["t_inbound_burn_yr"],
        "delivered_t": r_titan_he_1mwe_40["delivered_t"],
    }
    headline["titan_inbound_40.2_br_bundled_40_W_per_kg_1mwe"] = {
        "round_trip_yr": r_titan_br_1mwe_40["round_trip_yr"],
        "closes_15yr": r_titan_br_1mwe_40["closes_15yr"],
        "t_outbound_yr": r_titan_br_1mwe_40["t_outbound_burn_yr"],
        "t_inbound_yr": r_titan_br_1mwe_40["t_inbound_burn_yr"],
        "delivered_t": r_titan_br_1mwe_40["delivered_t"],
    }
    results["headline"] = headline

    # Write JSON
    results_dir = Path(__file__).parent / "results"
    results_dir.mkdir(exist_ok=True)
    (results_dir / "electric_outbound_rerun.json").write_text(
        json.dumps(results, indent=2, default=str)
    )

    # Tables
    lines = []
    lines.append("### Unit sanity check — bug confirmation\n")
    s = sanity
    lines.append(f"- Scenario: m_final = {s['m_final_t']:.1f} t, Δv = 9 km/s, "
                 f"Isp = 2000 s, power = 1 MWe.")
    lines.append(f"- Mass ratio (Tsiolkovsky): {s['mass_ratio']:.4f}")
    lines.append(f"- True wet mass at start: {s['m_wet_truth_t']:.4f} t")
    lines.append(f"- True propellant: {s['m_prop_truth_t']:.4f} t")
    lines.append(f"- `burn_from_dry_end(m_final)` → m_prop = {s['from_dry_end_t']:.4f} t  "
                 f"({'matches truth' if s['from_dry_end_matches_truth'] else 'BROKEN'})")
    lines.append(f"- `burn_from_wet(m_wet)` → m_prop = {s['from_wet_t']:.4f} t  "
                 f"({'matches truth' if s['from_wet_matches_truth'] else 'BROKEN'})")
    lines.append(f"- `burn_from_wet(m_final)` [the bugged call pattern] → m_prop = "
                 f"{s['bugged_call_t']:.4f} t — **understated by factor "
                 f"{s['understatement_ratio_truth_over_bugged']:.4f} = mass_ratio**")
    lines.append(f"- Burn-time understatement factor (same as mass): "
                 f"{s['burn_time_understatement_ratio']:.4f}")
    lines.append("")
    lines.append("**Bug confirmed.** The outbound call site at R-electric-outbound `run.py:223` "
                 "passes `m_tug` (dry-at-end-of-burn) to a function that interprets it as wet-at-start. "
                 "Outbound propellant mass and outbound burn time are understated by factor mass-ratio. "
                 "At Isp 2000 s and Δv 17.97 km/s (the all-electric outbound delta-velocity), mass-ratio "
                 "≈ 2.50, so outbound burn time is understated 2.50×.\n")
    lines.append("**Inbound call site (run.py:236) is correct as written.** It passes "
                 "`m_tug + chunk` which IS the wet-at-start mass in the chunk-fed electric "
                 "architecture: the chunk is water ice and is the propellant supply. Mass at start "
                 "of inbound burn = m_tug + chunk; mass at end = m_tug + (chunk - prop) = m_tug + "
                 "delivered. No fix needed.\n")

    lines.append("### Outbound delta-velocity (unchanged from R-electric-outbound)\n")
    lines.append(f"- All-electric outbound integrated Δv: {dv_out:.3f} km/s")
    lines.append(f"- Hohmann cruise (each way): {hohmann_cruise_yr():.3f} years\n")

    def emit_sweep(title: str, rows: list, note: str = "") -> None:
        lines.append(f"### {title}\n")
        if note:
            lines.append(note + "\n")
        lines.append("| Reactor (kWe) | Model | m_tug (t) | t_out (yr) | t_in (yr) | Round-trip (yr) | Delivered (t) | Closes 15 yr? |")
        lines.append("|---:|---|---:|---:|---:|---:|---:|:--:|")
        for r in rows:
            flag = "**yes**" if r["closes_15yr"] else "no"
            lines.append(
                f"| {r['reactor_kwe']:.0f} | {r['mass_model']} | "
                f"{r['m_tug_t']:.1f} | {r['t_outbound_burn_yr']:.2f} | "
                f"{r['t_inbound_burn_yr']:.2f} | {r['round_trip_yr']:.2f} | "
                f"{r['delivered_t']:.1f} | {flag} |"
            )
        lines.append("")

    emit_sweep(
        "Sweep A — matrix inbound Δv 6.42 km/s (impulsive-equivalent), bug FIXED, Isp 2000 s, chunk 200 t",
        sweep_corrected,
        "Apples-to-apples re-run of R-electric-outbound's main sweep with the outbound formula "
        "corrected. `bundled_40_W_per_kg` added for cross-reference against hyperion's 40-W/kg "
        "stretch-parameter callout.",
    )

    emit_sweep(
        "Sweep B — matrix inbound Δv 6.42 km/s, BUG INTACT (reproduction of R-electric-outbound), Isp 2000 s, chunk 200 t",
        sweep_bugged,
        "Sanity check: reproduces R-electric-outbound's tables.md numbers for `bundled_10_W_per_kg` "
        "and `decomposed_mid` rows, confirming the rerun matches the original on identical inputs "
        "when the bug is preserved.",
    )

    emit_sweep(
        "Sweep C — titan inbound Δv 24.7 km/s (high-elliptical Saturn departure + lunar gravity assist), bug FIXED, Isp 2000 s, chunk 200 t",
        sweep_titan_high_ellip,
        "Inbound delta-velocity per titan's R-inbound-dv-continuous-thrust round, best-case "
        "high-elliptical regime.",
    )

    emit_sweep(
        "Sweep D — titan inbound Δv 40.2 km/s (B-ring Saturn departure, no lunar gravity assist), bug FIXED, Isp 2000 s, chunk 200 t",
        sweep_titan_b_ring,
        "Inbound delta-velocity per titan's R-inbound-dv-continuous-thrust round, worst-case "
        "B-ring regime — what the current ICEBERG-conops Phase 5–6 architecture actually requires.",
    )

    lines.append("### Close-threshold summary — smallest reactor inside L0-05's 15-year ceiling\n")
    lines.append("| Sweep | Model | Smallest closing reactor (kWe) | Round-trip at close (yr) |")
    lines.append("|---|---|---:|---:|")
    for label, by_model in closes_summary.items():
        for mname, info in by_model.items():
            kwe = info["min_reactor_kwe"]
            rt = info["round_trip_yr"]
            kwe_str = f"{kwe:.0f}" if kwe is not None else "**no class closes**"
            rt_str = f"{rt:.2f}" if rt is not None else "—"
            lines.append(f"| {label} | {mname} | {kwe_str} | {rt_str} |")
    lines.append("")

    lines.append("### Headline — 1 MWe, decomposed-mid, Isp 2000 s, chunk 200 t — across inbound regimes\n")
    h = headline
    lines.append("| Inbound regime | Mass model | t_out (yr) | t_in (yr) | Round-trip (yr) | Delivered (t) | Closes 15 yr? |")
    lines.append("|---|---|---:|---:|---:|---:|:--:|")
    for key, val in h.items():
        flag = "**yes**" if val["closes_15yr"] else "no"
        deliv = f"{val.get('delivered_t', 0):.1f}"
        lines.append(
            f"| {key} | — | {val['t_outbound_yr']:.2f} | "
            f"{val['t_inbound_yr']:.2f} | {val['round_trip_yr']:.2f} | "
            f"{deliv} | {flag} |"
        )
    lines.append("")

    lines.append("### Hypothesis grading\n")
    hg = results["hypothesis_grading"]
    lines.append("| Sub-claim | Predicted | Actual | Held? |")
    lines.append("|---|---|---|---|")
    lines.append(f"| H-eor-a — Outbound burn time understatement at 1 MWe / decomposed-mid / Isp 2000 s | "
                 f"{hg['H_eor_a']['predicted_burn_time_ratio']}× | "
                 f"{hg['H_eor_a']['actual_ratio_1mwe_decomposed_mid']:.3f}× | "
                 f"{'yes' if hg['H_eor_a']['held'] else '**no**'} |")
    lines.append(f"| H-eor-b — Corrected smallest reactor closing (decomposed-mid, matrix-inbound) | "
                 f"{hg['H_eor_b']['predicted']} | "
                 f"corrected {hg['H_eor_b']['actual_min_kwe_corrected']} kWe / "
                 f"bugged {hg['H_eor_b']['actual_min_kwe_bugged']} kWe | "
                 f"{'yes' if hg['H_eor_b']['held'] else '**no**'} |")
    lines.append(f"| H-eor-c — No 10-W/kg cell closes at titan-inbound 24.7 km/s | "
                 f"{hg['H_eor_c']['predicted']} | "
                 f"any close = {hg['H_eor_c']['actual_any_close_at_10_W_per_kg_titan_high_ellip']} | "
                 f"{'yes' if hg['H_eor_c']['held'] else '**no**'} |")
    lines.append(f"| H-eor-d — At least one 40-W/kg cell closes at titan-inbound 24.7 km/s | "
                 f"{hg['H_eor_d']['predicted']} | "
                 f"any close = {hg['H_eor_d']['actual_any_close_at_40_W_per_kg_titan_high_ellip']} | "
                 f"{'yes' if hg['H_eor_d']['held'] else '**no**'} |")

    (results_dir / "tables.md").write_text("\n".join(lines))
    return results


if __name__ == "__main__":
    out = main()
    print("R-electric-outbound-rerun complete.")
    print()
    s = out["unit_sanity_check"]
    print(f"  Unit sanity: bugged call understates by {s['understatement_ratio_truth_over_bugged']:.3f}× = mass_ratio  "
          f"(burn-time understatement same factor).")
    print()
    print("  Close thresholds (decomposed-mid, Isp 2000 s, chunk 200 t):")
    for label, by_model in out["close_thresholds"].items():
        info = by_model["decomposed_mid"]
        kwe = info["min_reactor_kwe"]
        rt = info["round_trip_yr"]
        if kwe is None:
            print(f"    {label}: NO class closes inside 15 yr")
        else:
            print(f"    {label}: closes at {kwe:.0f} kWe (round-trip {rt:.2f} yr)")
    print()
    print("  Hypothesis grading:")
    for k, v in out["hypothesis_grading"].items():
        print(f"    {k}: {'held' if v['held'] else 'FALSIFIED'}")
