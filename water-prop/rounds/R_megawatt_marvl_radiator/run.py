"""R-megawatt-marvl-radiator — does the matrix's year-twenty-plus megawatt
all-electric end-to-end winner cell survive when the megawatt mass model is
re-anchored to National Academies 2021 / NASA Modular Assembled Radiators for
Very Large systems (MARVL) breakdown instead of decomposed-mid?

Locked R-power-wonder finding (May 2026): at megawatt-electric scale, the
radiator subsystem is 40–55 percent of total system mass — not the ~4 percent
that decomposed-mid implies. Anchors:
  - National Academies 2021 Space Nuclear Propulsion report
  - NASA Modular Assembled Radiators for Very Large systems (MARVL) studies
  - Reactor + shield: 25–35 percent of system mass at 1 MWe
  - Power conversion (Brayton at high efficiency): 15–25 percent
  - Radiators: 40–55 percent (waste heat at high Brayton temperatures demands
    enormous radiating area; structural mass scales unfavorably with area)
  - The bundled formula (5 t + reactor_kWe × 0.1 t/kWe) was closer to correct
    at megawatt scale than decomposed-mid. Decomposed-mid is the OPTIMISTIC
    model, not the realistic one.

This round constructs a `decomposed_marvl` mass model with alpha values that
reproduce the MARVL breakdown midpoints at 1 MWe, then re-runs the megawatt
round-trip composition with R-electric-outbound-rerun's bug fix AND
R-outbound-dv-continuous-thrust's corrected outbound delta-velocity AND
titan's corrected inbound delta-velocity all applied. Round-trip computed at
each reactor class to find where (if anywhere) MARVL-anchored architecture
closes L0-05.

Headline question: at MARVL-anchored mass model, with all upstream corrections
applied, does any reactor power class close inside L0-05? If yes, at what
delivered fraction? If no, what's the closest miss?

Sub-question (year-zero-through-fifteen path): does sub-megawatt (Kilopower-
class, ~100–200 kWe) close at the year-zero-through-fifteen Variant B
architecture's chemical-kick outbound + electric-inbound assumption? That's
the architecturally clean path if megawatt all-electric is structurally
falsified at MARVL realism.

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

LEO_ALT_KM = 400.0
ETA_THR = 0.65
SATURN_OPS_YR = 1.0
ROUND_TRIP_CEILING_YR = 15.0

# Saturn arrival/departure orbits
SATURN_HIGH_ELLIPTICAL_KM = 1.0e6

# Delta-velocities (corrected, from R-electric-outbound-rerun + R-outbound-dv-
# continuous-thrust + titan)
DV_OUTBOUND_HE_NO_LGA_KM_S = 29.56
DV_OUTBOUND_HE_WITH_LGA_KM_S = 27.56
DV_INBOUND_TITAN_HE_LGA_KM_S = 24.7

# Matrix-impulsive 6.42 km/s for year-zero-through-fifteen chemical-kick reference
DV_INBOUND_MATRIX_IMPULSIVE_KM_S = 6.42

# Reactor sweep
REACTOR_POWERS_KWE = [40.0, 100.0, 200.0, 500.0, 1000.0, 2000.0]
ISP_BASELINE_S = 2000.0
CHUNK_BASELINE_T = 200.0

# Mass models
MASS_MODELS: dict[str, dict] = {
    "decomposed_mid": {
        # Original decomposed-mid (R-radiator-mass-penalty's optimistic model)
        "kind": "decomposed",
        "m_fixed_t": 3.0,
        "alpha_reactor_W_per_kg": 50.0,
        "alpha_PC_W_per_kg": 200.0,
        "alpha_radiator_kW_th_per_kg": 2.0,
        "eta_conv": 0.30,
        "f_tank": 0.05,
    },
    "decomposed_marvl": {
        # MARVL-anchored at 1 MWe: reactor+shield 30%, PC 20%, radiator 50% of stack.
        # At 1 MWe stack target ~100 t (matches bundled_10_W_per_kg):
        #   alpha_reactor = 1000 / 30 = 33.3 W/kg
        #   alpha_PC = 1000 / 20 = 50 W/kg
        #   For radiator: waste heat at 1 MWe / eta=0.3 = 2.333 MW_th;
        #   radiator mass = 50 t → 2333 / 50 / 1000 = 0.047 kW_th/kg.
        # Tighten m_fixed and f_tank to match a realistic Saturn-mission stack.
        "kind": "decomposed",
        "m_fixed_t": 5.0,
        "alpha_reactor_W_per_kg": 33.0,
        "alpha_PC_W_per_kg": 50.0,
        "alpha_radiator_kW_th_per_kg": 0.047,
        "eta_conv": 0.30,
        "f_tank": 0.05,
    },
    "bundled_10_W_per_kg": {
        # Original bundled — 10 W/kg specific power. Per power-finding-4, this is
        # closer-to-correct at megawatt scale.
        "kind": "bundled",
        "m_fixed_t": 5.0,
        "specific_power_total_w_per_kg": 10.0,
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
    return (model["m_fixed_t"] + m_reactor + m_pc + m_rad + m_tank)


def mass_breakdown(model: dict, reactor_kwe: float, m_prop_t: float = 0.0) -> dict:
    if model["kind"] == "bundled":
        return {
            "m_fixed_t": model["m_fixed_t"],
            "m_stack_t": reactor_kwe / model["specific_power_total_w_per_kg"],
            "m_tank_t": m_prop_t * 0.05,
            "total_t": dry_mass_t(model, reactor_kwe, m_prop_t),
        }
    eta = model["eta_conv"]
    p_th_waste_kw = reactor_kwe * (1.0 - eta) / eta
    m_reactor = reactor_kwe / model["alpha_reactor_W_per_kg"]
    m_pc = reactor_kwe / model["alpha_PC_W_per_kg"]
    m_rad = p_th_waste_kw / model["alpha_radiator_kW_th_per_kg"] / 1000.0
    m_tank = m_prop_t * model["f_tank"]
    total = model["m_fixed_t"] + m_reactor + m_pc + m_rad + m_tank
    return {
        "m_fixed_t": model["m_fixed_t"],
        "m_reactor_t": m_reactor,
        "m_PC_t": m_pc,
        "m_radiator_t": m_rad,
        "m_tank_t": m_tank,
        "total_t": total,
        "radiator_fraction_of_total": m_rad / total if total > 0 else 0.0,
    }


def burn_from_dry_end(m_final_t, dv_km_s, power_kwe, isp_s, eta=ETA_THR):
    v_e = isp_s * G0
    thrust_N = 2.0 * eta * power_kwe * 1000.0 / v_e
    mass_ratio = math.exp(dv_km_s * 1000.0 / v_e)
    m_prop_t = m_final_t * (mass_ratio - 1.0)
    t_burn_s = m_prop_t * 1000.0 * v_e / thrust_N
    return {"thrust_N": thrust_N, "m_prop_t": m_prop_t, "mass_ratio": mass_ratio,
             "t_burn_s": t_burn_s, "t_burn_yr": t_burn_s / YEAR_S}


def burn_from_wet(m_initial_t, dv_km_s, power_kwe, isp_s, eta=ETA_THR):
    v_e = isp_s * G0
    thrust_N = 2.0 * eta * power_kwe * 1000.0 / v_e
    mass_ratio = math.exp(dv_km_s * 1000.0 / v_e)
    m_prop_t = m_initial_t * (1.0 - 1.0 / mass_ratio)
    t_burn_s = m_prop_t * 1000.0 * v_e / thrust_N
    return {"thrust_N": thrust_N, "m_prop_t": m_prop_t, "mass_ratio": mass_ratio,
             "t_burn_s": t_burn_s, "t_burn_yr": t_burn_s / YEAR_S}


def hohmann_cruise_yr() -> float:
    a_h_km = (A_EARTH + A_SATURN) / 2.0
    return math.pi * math.sqrt(a_h_km ** 3 / GM_SUN) / YEAR_S


def round_trip(model, reactor_kwe, chunk_t, isp_s, dv_outbound_km_s, dv_inbound_km_s):
    # Self-consistent iteration on outbound tug mass
    m_tug_t = dry_mass_t(model, reactor_kwe, m_prop_t=0.0)
    for _ in range(40):
        burn_out = burn_from_dry_end(m_tug_t, dv_outbound_km_s, reactor_kwe, isp_s)
        new_m_tug = dry_mass_t(model, reactor_kwe, m_prop_t=burn_out["m_prop_t"])
        if abs(new_m_tug - m_tug_t) < 1e-4:
            m_tug_t = new_m_tug
            break
        m_tug_t = new_m_tug
    else:
        # Iteration failed — likely runaway. Mark explicitly.
        return {
            "feasible": False,
            "m_tug_t": m_tug_t,
            "round_trip_yr": math.inf,
            "closes_15yr": False,
            "delivered_t": -math.inf,
            "delivered_fraction": -math.inf,
            "reactor_kwe": reactor_kwe,
            "mass_model": model.get("_name", "?"),
            "t_outbound_burn_yr": math.inf,
            "t_inbound_burn_yr": math.inf,
            "m_prop_outbound_t": math.inf,
            "m_prop_inbound_t": math.inf,
            "mass_ratio_outbound": math.inf,
            "mass_ratio_inbound": math.inf,
            "thrust_N": 0.0,
            "note": "tug-mass iteration did not converge — tank-fraction positive feedback ran away",
        }
    burn_out = burn_from_dry_end(m_tug_t, dv_outbound_km_s, reactor_kwe, isp_s)
    burn_in = burn_from_wet(m_tug_t + chunk_t, dv_inbound_km_s, reactor_kwe, isp_s)
    t_cruise_yr = hohmann_cruise_yr()
    round_trip_yr = (burn_out["t_burn_yr"] + t_cruise_yr + SATURN_OPS_YR
                     + burn_in["t_burn_yr"] + t_cruise_yr)
    delivered_t = chunk_t - burn_in["m_prop_t"]
    return {
        "feasible": True,
        "m_tug_t": m_tug_t,
        "m_prop_outbound_t": burn_out["m_prop_t"],
        "m_LEO_t": m_tug_t + burn_out["m_prop_t"],
        "thrust_N": burn_out["thrust_N"],
        "mass_ratio_outbound": burn_out["mass_ratio"],
        "m_prop_inbound_t": burn_in["m_prop_t"],
        "mass_ratio_inbound": burn_in["mass_ratio"],
        "t_outbound_burn_yr": burn_out["t_burn_yr"],
        "t_cruise_each_yr": t_cruise_yr,
        "t_saturn_ops_yr": SATURN_OPS_YR,
        "t_inbound_burn_yr": burn_in["t_burn_yr"],
        "round_trip_yr": round_trip_yr,
        "closes_15yr": round_trip_yr <= ROUND_TRIP_CEILING_YR,
        "delivered_t": delivered_t,
        "delivered_fraction": delivered_t / chunk_t if chunk_t > 0 else 0.0,
    }


def main() -> dict:
    results: dict = {}

    # 1. Mass breakdown sanity check at 1 MWe (no propellant)
    breakdown_1mwe = {name: mass_breakdown(model, 1000.0, m_prop_t=0.0)
                      for name, model in MASS_MODELS.items()}
    results["mass_breakdown_1mwe_no_prop"] = breakdown_1mwe

    # 2. Megawatt all-electric end-to-end sweep — corrected outbound DV (high-elliptical no-LGA)
    # + titan inbound (high-elliptical with LGA, 24.7 km/s) + chunk 200 t + Isp 2000 s.
    sweep_corrected_megawatt = []
    for name, model in MASS_MODELS.items():
        model_named = {**model, "_name": name}
        for reactor in REACTOR_POWERS_KWE:
            row = round_trip(model_named, reactor, CHUNK_BASELINE_T, ISP_BASELINE_S,
                              DV_OUTBOUND_HE_NO_LGA_KM_S, DV_INBOUND_TITAN_HE_LGA_KM_S)
            row.update({"mass_model": name, "reactor_kwe": reactor})
            sweep_corrected_megawatt.append(row)
    results["sweep_megawatt_corrected"] = sweep_corrected_megawatt

    # 3. Best-case megawatt sweep — outbound LGA credit applied too
    sweep_best_case = []
    for name, model in MASS_MODELS.items():
        model_named = {**model, "_name": name}
        for reactor in REACTOR_POWERS_KWE:
            row = round_trip(model_named, reactor, CHUNK_BASELINE_T, ISP_BASELINE_S,
                              DV_OUTBOUND_HE_WITH_LGA_KM_S, DV_INBOUND_TITAN_HE_LGA_KM_S)
            row.update({"mass_model": name, "reactor_kwe": reactor})
            sweep_best_case.append(row)
    results["sweep_megawatt_best_case_lga_both_legs"] = sweep_best_case

    # 4. Year-zero-through-fifteen chemical-kick + electric-inbound check
    # In that architecture the outbound is chemical (not the spacecraft's
    # electric thrusters), so the outbound burn time isn't on the L0-05 budget;
    # the inbound is electric at the matrix's impulsive-equivalent 6.42 km/s
    # (matches actual chemical-kick impulsive injection, which IS valid for the
    # chemical-kick architecture). So we only need to check inbound burn time
    # under each mass model at the matrix-impulsive inbound.
    sweep_kilopower_chemkick = []
    cruise_yr = hohmann_cruise_yr()
    # For chemical-kick, outbound time is short (~Hohmann cruise plus minimal
    # injection burn). Use ~Hohmann cruise only on outbound for round-trip
    # budgeting: outbound_burn ≈ 0, cruise out, ops, electric inbound, cruise back.
    for name, model in MASS_MODELS.items():
        for reactor in REACTOR_POWERS_KWE:
            m_tug_t = dry_mass_t(model, reactor, m_prop_t=0.0)
            burn_in = burn_from_wet(m_tug_t + CHUNK_BASELINE_T,
                                     DV_INBOUND_MATRIX_IMPULSIVE_KM_S,
                                     reactor, ISP_BASELINE_S)
            round_trip_yr = cruise_yr + SATURN_OPS_YR + burn_in["t_burn_yr"] + cruise_yr
            delivered_t = CHUNK_BASELINE_T - burn_in["m_prop_t"]
            sweep_kilopower_chemkick.append({
                "mass_model": name,
                "reactor_kwe": reactor,
                "m_tug_t": m_tug_t,
                "t_inbound_burn_yr": burn_in["t_burn_yr"],
                "round_trip_yr": round_trip_yr,
                "closes_15yr": round_trip_yr <= ROUND_TRIP_CEILING_YR,
                "delivered_t": delivered_t,
                "delivered_fraction": delivered_t / CHUNK_BASELINE_T,
            })
    results["sweep_kilopower_chemkick_outbound"] = sweep_kilopower_chemkick

    # 5. Hypothesis grading
    # Find 1 MWe MARVL row
    def find(sweep, model_name, reactor):
        for r in sweep:
            if r["mass_model"] == model_name and r["reactor_kwe"] == reactor:
                return r
        return None

    marvl_1mwe_total = breakdown_1mwe["decomposed_marvl"]["total_t"]
    h_mr_a_predicted = [95.0, 115.0]
    h_mr_a_held = h_mr_a_predicted[0] <= marvl_1mwe_total <= h_mr_a_predicted[1]

    r_marvl_1mwe = find(sweep_corrected_megawatt, "decomposed_marvl", 1000.0)
    h_mr_b_predicted = "> 18 yr"
    h_mr_b_held = r_marvl_1mwe["round_trip_yr"] > 18.0 if r_marvl_1mwe["feasible"] else True

    h_mr_c_predicted = "< 0 t (chunk-fed insufficient)"
    h_mr_c_held = r_marvl_1mwe["delivered_t"] < 0 if r_marvl_1mwe["feasible"] else True

    # H-mr-d: at 200 kWe MARVL-anchored, chemical-kick + electric-inbound closes
    # at chunk 200 t.
    r_marvl_200kwe_chemkick = find(sweep_kilopower_chemkick, "decomposed_marvl", 200.0)
    h_mr_d_predicted = "closes inside L0-05 with positive delivered mass"
    h_mr_d_held = r_marvl_200kwe_chemkick["closes_15yr"] and r_marvl_200kwe_chemkick["delivered_t"] > 0

    # H-mr-e: NO megawatt all-electric cell closes inside L0-05 across all
    # tested mass models, even at LGA-both-legs best case.
    any_close_best_case_megawatt_decomposed_marvl_or_bundled = any(
        r["closes_15yr"] for r in sweep_best_case
        if r["mass_model"] in ("decomposed_marvl", "bundled_10_W_per_kg")
        and r["reactor_kwe"] >= 1000.0
    )
    h_mr_e_predicted = "no realistic-mass-model megawatt cell closes even at LGA-both-legs"
    h_mr_e_held = not any_close_best_case_megawatt_decomposed_marvl_or_bundled

    results["hypothesis_grading"] = {
        "H_mr_a": {"predicted_t": h_mr_a_predicted, "actual_t": marvl_1mwe_total, "held": h_mr_a_held},
        "H_mr_b": {"predicted": h_mr_b_predicted,
                    "actual_yr": r_marvl_1mwe["round_trip_yr"] if r_marvl_1mwe["feasible"] else "infeasible",
                    "held": h_mr_b_held},
        "H_mr_c": {"predicted": h_mr_c_predicted,
                    "actual_delivered_t": r_marvl_1mwe["delivered_t"] if r_marvl_1mwe["feasible"] else "infeasible",
                    "held": h_mr_c_held},
        "H_mr_d": {"predicted": h_mr_d_predicted,
                    "actual_yr": r_marvl_200kwe_chemkick["round_trip_yr"],
                    "actual_delivered_t": r_marvl_200kwe_chemkick["delivered_t"],
                    "held": h_mr_d_held},
        "H_mr_e": {"predicted": h_mr_e_predicted,
                    "actual_any_close": any_close_best_case_megawatt_decomposed_marvl_or_bundled,
                    "held": h_mr_e_held},
    }

    # Write JSON
    results_dir = Path(__file__).parent / "results"
    results_dir.mkdir(exist_ok=True)
    (results_dir / "megawatt_marvl.json").write_text(json.dumps(results, indent=2, default=str))

    # Tables
    lines = []
    lines.append("### Mass breakdown at 1 MWe (no propellant)\n")
    lines.append("MARVL-anchored decomposed model targets the National Academies 2021 / NASA MARVL "
                  "midpoints: reactor+shield ~30%, power conversion ~20%, radiator ~50% of stack mass.\n")
    lines.append("| Model | m_fixed (t) | m_reactor (t) | m_PC (t) | m_radiator (t) | m_stack/total (t) | Radiator fraction |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|")
    for name, b in breakdown_1mwe.items():
        if "m_reactor_t" in b:
            lines.append(
                f"| {name} | {b['m_fixed_t']:.1f} | {b['m_reactor_t']:.1f} | "
                f"{b['m_PC_t']:.1f} | {b['m_radiator_t']:.1f} | {b['total_t']:.1f} | "
                f"{b['radiator_fraction_of_total']*100:.1f}% |"
            )
        else:
            lines.append(
                f"| {name} | {b['m_fixed_t']:.1f} | (bundled) | (bundled) | (bundled) | "
                f"{b['total_t']:.1f} | n/a |"
            )
    lines.append("")

    def emit_sweep(title: str, rows: list, note: str = "") -> None:
        lines.append(f"### {title}\n")
        if note:
            lines.append(note + "\n")
        lines.append("| Reactor (kWe) | Mass model | m_tug (t) | t_out (yr) | t_in (yr) | Round-trip (yr) | Delivered (t) | Closes 15 yr? |")
        lines.append("|---:|---|---:|---:|---:|---:|---:|:--:|")
        for r in rows:
            flag = "**yes**" if r.get("closes_15yr") else "no"
            rt = r["round_trip_yr"]
            rt_str = f"{rt:.2f}" if r.get("feasible", True) and math.isfinite(rt) else "infeasible"
            t_out = r.get("t_outbound_burn_yr", float("nan"))
            t_out_str = f"{t_out:.2f}" if math.isfinite(t_out) else "—"
            t_in = r["t_inbound_burn_yr"]
            t_in_str = f"{t_in:.2f}" if math.isfinite(t_in) else "—"
            deliv = r["delivered_t"]
            deliv_str = f"{deliv:.1f}" if math.isfinite(deliv) else "—"
            m_tug_str = f"{r['m_tug_t']:.1f}" if math.isfinite(r['m_tug_t']) else "—"
            lines.append(
                f"| {r['reactor_kwe']:.0f} | {r['mass_model']} | "
                f"{m_tug_str} | {t_out_str} | {t_in_str} | "
                f"{rt_str} | {deliv_str} | {flag} |"
            )
        lines.append("")

    emit_sweep(
        "Sweep A — megawatt all-electric end-to-end, corrected outbound Δv 29.56 km/s (no LGA), titan inbound 24.7 km/s",
        sweep_corrected_megawatt,
        "All corrections applied: outbound formula bug-fix, outbound Δv symmetric correction, titan's "
        "continuous-thrust inbound, chunk-fed wet-at-start inbound. Mass model sweeps the three "
        "candidates: decomposed-mid (optimistic, R-electric-outbound baseline), decomposed-MARVL "
        "(power-finding-4 anchored), bundled 10 W/kg (closer-to-correct per power-finding-4).",
    )

    emit_sweep(
        "Sweep B — best-case composite (LGA credit on BOTH outbound and inbound), titan inbound 24.7 km/s",
        sweep_best_case,
        "Same as Sweep A but outbound LGA credit applied (27.56 km/s instead of 29.56). Most favorable "
        "operational case for megawatt all-electric end-to-end short of architectural changes (chunk-as-"
        "heat-shield, chunk-size reduction).",
    )

    emit_sweep(
        "Sweep C — year-zero-through-fifteen architecture (chemical-kick outbound + electric inbound)",
        sweep_kilopower_chemkick,
        "Outbound is chemical-kick (off the round-trip Δv ledger for the spacecraft's electric thrusters). "
        "Inbound is electric at the matrix's impulsive-equivalent 6.42 km/s (valid for chemical-kick "
        "architecture which preserves Oberth-bonus impulsive injection). Round-trip = cruise_out + ops + "
        "electric_inbound_burn + cruise_back. This is the architecture the Kilopower Variant B winner cell "
        "is built on.",
    )

    lines.append("### Hypothesis grading\n")
    h = results["hypothesis_grading"]
    lines.append("| Sub-claim | Predicted | Actual | Held? |")
    lines.append("|---|---|---|---|")
    lines.append(f"| H-mr-a — MARVL-anchored 1 MWe tug mass | {h['H_mr_a']['predicted_t']} t | "
                  f"{h['H_mr_a']['actual_t']:.1f} t | "
                  f"{'yes' if h['H_mr_a']['held'] else '**no**'} |")
    lines.append(f"| H-mr-b — MARVL-anchored 1 MWe / titan-24.7 round-trip > 18 yr | "
                  f"{h['H_mr_b']['predicted']} | "
                  f"{h['H_mr_b']['actual_yr']} | "
                  f"{'yes' if h['H_mr_b']['held'] else '**no**'} |")
    lines.append(f"| H-mr-c — MARVL-anchored 1 MWe / titan-24.7 delivered mass < 0 | "
                  f"{h['H_mr_c']['predicted']} | "
                  f"{h['H_mr_c']['actual_delivered_t']} t | "
                  f"{'yes' if h['H_mr_c']['held'] else '**no**'} |")
    lines.append(f"| H-mr-d — MARVL-anchored 200 kWe chemical-kick architecture closes with positive delivered | "
                  f"{h['H_mr_d']['predicted']} | "
                  f"round-trip {h['H_mr_d']['actual_yr']:.2f} yr, delivered {h['H_mr_d']['actual_delivered_t']:.1f} t | "
                  f"{'yes' if h['H_mr_d']['held'] else '**no**'} |")
    lines.append(f"| H-mr-e — No realistic-mass-model megawatt cell closes at LGA-both-legs | "
                  f"{h['H_mr_e']['predicted']} | "
                  f"any close = {h['H_mr_e']['actual_any_close']} | "
                  f"{'yes' if h['H_mr_e']['held'] else '**no**'} |")

    (results_dir / "tables.md").write_text("\n".join(lines))
    return results


if __name__ == "__main__":
    out = main()
    print("R-megawatt-marvl-radiator complete.")
    print()
    print("  1-MWe mass breakdowns (no prop):")
    for name, b in out["mass_breakdown_1mwe_no_prop"].items():
        if "m_radiator_t" in b:
            print(f"    {name:25s}: total {b['total_t']:.1f} t  "
                  f"(reactor {b['m_reactor_t']:.1f} + PC {b['m_PC_t']:.1f} + "
                  f"rad {b['m_radiator_t']:.1f}; radiator share {b['radiator_fraction_of_total']*100:.0f}%)")
        else:
            print(f"    {name:25s}: total {b['total_t']:.1f} t  (bundled formula)")
    print()
    print("  Megawatt all-electric corrected (Sweep A) — 1 MWe rows:")
    for r in out["sweep_megawatt_corrected"]:
        if r["reactor_kwe"] == 1000.0:
            rt = r["round_trip_yr"] if math.isfinite(r["round_trip_yr"]) else "INF"
            print(f"    {r['mass_model']:25s}: round-trip {rt}, delivered {r['delivered_t']:.1f} t, closes={r['closes_15yr']}")
    print()
    print("  Chemical-kick architecture (Sweep C) — close-threshold per mass model:")
    for name in ["decomposed_mid", "decomposed_marvl", "bundled_10_W_per_kg"]:
        closing = [r for r in out["sweep_kilopower_chemkick_outbound"]
                    if r["mass_model"] == name and r["closes_15yr"] and r["delivered_t"] > 0]
        if closing:
            pick = min(closing, key=lambda r: r["reactor_kwe"])
            print(f"    {name:25s}: smallest reactor closing with positive delivered = {pick['reactor_kwe']:.0f} kWe "
                  f"(round-trip {pick['round_trip_yr']:.2f} yr, delivered {pick['delivered_t']:.1f} t)")
        else:
            print(f"    {name:25s}: NO class closes inside 15 yr with positive delivered")
    print()
    print("  Hypothesis grading:")
    for k, v in out["hypothesis_grading"].items():
        print(f"    {k}: {'held' if v['held'] else 'FALSIFIED'}")
