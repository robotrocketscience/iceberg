"""R-megawatt-relaxed-specific-power — sweep bundled-formula specific power
to identify the closure threshold for the megawatt all-electric end-to-end
cell, and propagate Round A's reactor-availability prior into expected
delivered mass.

Reuses rhea's R-megawatt-marvl-radiator round-trip closure machinery
(self-consistent tug-mass iteration, corrected delta-velocities, chunk-fed
wet-at-start inbound, Hohmann cruise + 1-year Saturn ops). See STUDY.md for
pre-registered hypothesis block and method.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

from waterprop.constants import A_EARTH, A_SATURN, G0, GM_SUN

YEAR_S = 365.25 * 86400.0

ETA_THR = 0.65
SATURN_OPS_YR = 1.0
ROUND_TRIP_CEILING_YR = 15.0

# Corrected delta-velocities (rhea, R-megawatt-marvl-radiator)
DV_OUTBOUND_HE_NO_LGA_KM_S = 29.56
DV_INBOUND_TITAN_HE_LGA_KM_S = 24.7

# Configuration held fixed (rhea's closest-miss configuration)
REACTOR_KWE_FIXED = 1000.0
ISP_BASELINE_S = 2000.0
CHUNK_BASELINE_T = 200.0
M_FIXED_T = 5.0
F_TANK = 0.05

# Specific-power sweep (watts-per-kilogram, bundled total system)
SPECIFIC_POWER_GRID = [10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 80.0, 100.0, 150.0, 200.0, 300.0]

# Round A reactor-availability priors (uniform / Jeffreys / skeptical at 2040 horizon)
# Loaded from R_power_bayesian_update results.
R_POWER_BAYESIAN_OVERLAY = (
    Path(__file__).parent.parent / "R_power_bayesian_update" / "results" / "matrix_overlay.json"
)


def dry_mass_t(specific_power_w_per_kg: float, reactor_kwe: float, m_prop_t: float) -> float:
    m_stack = reactor_kwe / specific_power_w_per_kg
    m_tank = m_prop_t * F_TANK
    return M_FIXED_T + m_stack + m_tank


def burn_from_dry_end(m_final_t: float, dv_km_s: float, power_kwe: float, isp_s: float) -> dict:
    v_e = isp_s * G0
    thrust_N = 2.0 * ETA_THR * power_kwe * 1000.0 / v_e
    mass_ratio = math.exp(dv_km_s * 1000.0 / v_e)
    m_prop_t = m_final_t * (mass_ratio - 1.0)
    t_burn_s = m_prop_t * 1000.0 * v_e / thrust_N
    return {"thrust_N": thrust_N, "m_prop_t": m_prop_t, "mass_ratio": mass_ratio,
            "t_burn_s": t_burn_s, "t_burn_yr": t_burn_s / YEAR_S}


def burn_from_wet(m_initial_t: float, dv_km_s: float, power_kwe: float, isp_s: float) -> dict:
    v_e = isp_s * G0
    thrust_N = 2.0 * ETA_THR * power_kwe * 1000.0 / v_e
    mass_ratio = math.exp(dv_km_s * 1000.0 / v_e)
    m_prop_t = m_initial_t * (1.0 - 1.0 / mass_ratio)
    t_burn_s = m_prop_t * 1000.0 * v_e / thrust_N
    return {"thrust_N": thrust_N, "m_prop_t": m_prop_t, "mass_ratio": mass_ratio,
            "t_burn_s": t_burn_s, "t_burn_yr": t_burn_s / YEAR_S}


def hohmann_cruise_yr() -> float:
    a_h_km = (A_EARTH + A_SATURN) / 2.0
    return math.pi * math.sqrt(a_h_km ** 3 / GM_SUN) / YEAR_S


def round_trip_at_specific_power(
    specific_power_w_per_kg: float,
    reactor_kwe: float,
    chunk_t: float,
    isp_s: float,
    dv_outbound_km_s: float,
    dv_inbound_km_s: float,
) -> dict:
    """Self-consistent tug-mass iteration on outbound, then chunk-fed wet-at-start inbound."""
    m_tug_t = dry_mass_t(specific_power_w_per_kg, reactor_kwe, m_prop_t=0.0)
    converged = False
    for _ in range(60):
        burn_out = burn_from_dry_end(m_tug_t, dv_outbound_km_s, reactor_kwe, isp_s)
        new_m_tug = dry_mass_t(specific_power_w_per_kg, reactor_kwe, m_prop_t=burn_out["m_prop_t"])
        if abs(new_m_tug - m_tug_t) < 1e-4:
            m_tug_t = new_m_tug
            converged = True
            break
        m_tug_t = new_m_tug
    if not converged:
        return {
            "feasible": False,
            "specific_power_w_per_kg": specific_power_w_per_kg,
            "reactor_kwe": reactor_kwe,
            "m_tug_t": m_tug_t,
            "round_trip_yr": math.inf,
            "delivered_t": -math.inf,
            "delivered_fraction": -math.inf,
            "closes_15yr": False,
            "note": "tug-mass iteration did not converge",
        }
    burn_out = burn_from_dry_end(m_tug_t, dv_outbound_km_s, reactor_kwe, isp_s)
    burn_in = burn_from_wet(m_tug_t + chunk_t, dv_inbound_km_s, reactor_kwe, isp_s)
    cruise_yr = hohmann_cruise_yr()
    round_trip_yr = (
        burn_out["t_burn_yr"] + cruise_yr + SATURN_OPS_YR + burn_in["t_burn_yr"] + cruise_yr
    )
    delivered_t = chunk_t - burn_in["m_prop_t"]
    return {
        "feasible": True,
        "specific_power_w_per_kg": specific_power_w_per_kg,
        "reactor_kwe": reactor_kwe,
        "m_tug_t": m_tug_t,
        "m_stack_t": reactor_kwe / specific_power_w_per_kg,
        "m_prop_outbound_t": burn_out["m_prop_t"],
        "m_LEO_t": m_tug_t + burn_out["m_prop_t"],
        "thrust_N": burn_out["thrust_N"],
        "mass_ratio_outbound": burn_out["mass_ratio"],
        "mass_ratio_inbound": burn_in["mass_ratio"],
        "t_outbound_burn_yr": burn_out["t_burn_yr"],
        "t_cruise_each_yr": cruise_yr,
        "t_saturn_ops_yr": SATURN_OPS_YR,
        "t_inbound_burn_yr": burn_in["t_burn_yr"],
        "round_trip_yr": round_trip_yr,
        "closes_15yr": (round_trip_yr <= ROUND_TRIP_CEILING_YR) and (delivered_t > 0),
        "delivered_t": delivered_t,
        "delivered_fraction": delivered_t / chunk_t if chunk_t > 0 else 0.0,
        "m_prop_inbound_t": burn_in["m_prop_t"],
    }


def main() -> dict:
    # Sweep specific power.
    sweep = [
        round_trip_at_specific_power(
            sp, REACTOR_KWE_FIXED, CHUNK_BASELINE_T, ISP_BASELINE_S,
            DV_OUTBOUND_HE_NO_LGA_KM_S, DV_INBOUND_TITAN_HE_LGA_KM_S,
        )
        for sp in SPECIFIC_POWER_GRID
    ]

    # Closure threshold = smallest specific power in grid where closes_15yr.
    closing = [r for r in sweep if r["closes_15yr"]]
    threshold_w_per_kg = min((r["specific_power_w_per_kg"] for r in closing), default=None)

    # Specific lookups for hypothesis grading.
    def at_sp(sp: float) -> dict | None:
        for r in sweep:
            if math.isclose(r["specific_power_w_per_kg"], sp):
                return r
        return None

    r60 = at_sp(60.0)
    r80 = at_sp(80.0)

    # Programmatic-risk overlay: load Round A megawatt-by-2040 probabilities.
    overlay = json.loads(R_POWER_BAYESIAN_OVERLAY.read_text())
    mw_avail = overlay["all_electric_megawatt"]["expected_delivered_mass_by_prior"]
    p_uniform = mw_avail["uniform_beta_1_1"]["p_reactor_available_by_window"]
    p_jeffreys = mw_avail["jeffreys_beta_0p5_0p5"]["p_reactor_available_by_window"]
    p_skeptical = mw_avail["skeptical_beta_0p5_5"]["p_reactor_available_by_window"]

    # Apply overlay to each sweep row.
    for r in sweep:
        if not r.get("feasible"):
            continue
        d = max(r["delivered_t"], 0.0)  # negative deliveries are technical-impossible, not just risky
        r["expected_delivered_t_uniform"] = d * p_uniform
        r["expected_delivered_t_jeffreys"] = d * p_jeffreys
        r["expected_delivered_t_skeptical"] = d * p_skeptical

    # Hypothesis grading.
    h_mrsp_a = {
        "predicted": "closes (round-trip 11-14 yr, delivered 5-40 t)",
        "actual_round_trip_yr": r60["round_trip_yr"] if r60 else None,
        "actual_delivered_t": r60["delivered_t"] if r60 else None,
        "actual_closes": r60["closes_15yr"] if r60 else False,
        "held": (r60 is not None and r60["closes_15yr"]
                 and 11.0 <= r60["round_trip_yr"] <= 14.0
                 and 5.0 <= r60["delivered_t"] <= 40.0),
    }
    h_mrsp_b = {
        "predicted": "closes (round-trip 9-13 yr, delivered 30-80 t)",
        "actual_round_trip_yr": r80["round_trip_yr"] if r80 else None,
        "actual_delivered_t": r80["delivered_t"] if r80 else None,
        "actual_closes": r80["closes_15yr"] if r80 else False,
        "held": (r80 is not None and r80["closes_15yr"]
                 and 9.0 <= r80["round_trip_yr"] <= 13.0
                 and 30.0 <= r80["delivered_t"] <= 80.0),
    }
    h_mrsp_c = {
        "predicted_range_w_per_kg": [40.0, 60.0],
        "predicted_point_w_per_kg": 50.0,
        "actual_threshold_w_per_kg": threshold_w_per_kg,
        "held": (threshold_w_per_kg is not None
                 and 40.0 <= threshold_w_per_kg <= 60.0),
    }
    delivered_fraction_at_80 = r80["delivered_fraction"] if r80 and r80["closes_15yr"] else None
    h_mrsp_d = {
        "predicted_range": [0.15, 0.40],
        "predicted_point": 0.25,
        "actual_delivered_fraction_at_80wpkg": delivered_fraction_at_80,
        "held": (delivered_fraction_at_80 is not None
                 and 0.15 <= delivered_fraction_at_80 <= 0.40),
    }
    expected_delivered_at_60_uniform = r60["expected_delivered_t_uniform"] if r60 else None
    h_mrsp_e = {
        "predicted_range_t": [0.005, 0.05],
        "predicted_point_t": 0.02,
        "actual_expected_delivered_t_uniform": expected_delivered_at_60_uniform,
        "held": (expected_delivered_at_60_uniform is not None
                 and 0.005 <= expected_delivered_at_60_uniform <= 0.05),
    }

    results = {
        "config": {
            "reactor_kwe_fixed": REACTOR_KWE_FIXED,
            "chunk_t": CHUNK_BASELINE_T,
            "isp_s": ISP_BASELINE_S,
            "m_fixed_t": M_FIXED_T,
            "f_tank": F_TANK,
            "eta_thr": ETA_THR,
            "dv_outbound_km_s": DV_OUTBOUND_HE_NO_LGA_KM_S,
            "dv_inbound_km_s": DV_INBOUND_TITAN_HE_LGA_KM_S,
            "ceiling_yr": ROUND_TRIP_CEILING_YR,
        },
        "specific_power_grid_w_per_kg": SPECIFIC_POWER_GRID,
        "sweep": sweep,
        "closure_threshold_w_per_kg": threshold_w_per_kg,
        "programmatic_risk_overlay_priors": {
            "p_megawatt_avail_by_2040_uniform": p_uniform,
            "p_megawatt_avail_by_2040_jeffreys": p_jeffreys,
            "p_megawatt_avail_by_2040_skeptical": p_skeptical,
        },
        "hypothesis_grading": {
            "H-mrsp-a_60wpkg_closes": h_mrsp_a,
            "H-mrsp-b_80wpkg_closes": h_mrsp_b,
            "H-mrsp-c_closure_threshold_wpkg": h_mrsp_c,
            "H-mrsp-d_delivered_fraction_at_80": h_mrsp_d,
            "H-mrsp-e_expected_delivered_t_at_60_uniform": h_mrsp_e,
        },
    }

    out_dir = Path(__file__).parent / "results"
    out_dir.mkdir(exist_ok=True)
    (out_dir / "R_megawatt_relaxed_specific_power.json").write_text(
        json.dumps(results, indent=2, default=str)
    )

    # Tables artifact.
    lines = []
    lines.append("### Specific-power sweep (1 megawatt-electric, chunk 200 t, specific impulse 2000 s, "
                 "outbound 29.56 km/s, inbound 24.7 km/s)\n")
    lines.append("| Specific power (W/kg) | m_stack (t) | m_tug (t) | t_outbound (yr) | t_inbound (yr) | "
                 "Round-trip (yr) | Delivered (t) | Delivered fraction | Closes 15 yr & delivers > 0? | "
                 "Expected (uniform, t) |")
    lines.append("|---:|---:|---:|---:|---:|---:|---:|---:|:--:|---:|")
    for r in sweep:
        if not r.get("feasible"):
            lines.append(f"| {r['specific_power_w_per_kg']:.0f} | infeasible (mass-iteration runaway) | "
                         f"— | — | — | — | — | — | no | — |")
            continue
        flag = "**yes**" if r["closes_15yr"] else "no"
        lines.append(
            f"| {r['specific_power_w_per_kg']:.0f} | {r['m_stack_t']:.2f} | {r['m_tug_t']:.2f} | "
            f"{r['t_outbound_burn_yr']:.2f} | {r['t_inbound_burn_yr']:.2f} | "
            f"{r['round_trip_yr']:.2f} | {r['delivered_t']:.1f} | {r['delivered_fraction']:.3f} | "
            f"{flag} | {r['expected_delivered_t_uniform']:.4f} |"
        )
    lines.append("")
    lines.append(f"**Closure threshold:** {threshold_w_per_kg} W/kg (smallest swept specific power "
                 f"that closes inside 15 yr with positive delivered mass).\n")

    lines.append("### Programmatic-risk overlay\n")
    lines.append(f"Priors carried from Round A (R-power-bayesian-update). P(megawatt-class reactor on "
                 f"orbit by 2040) under each prior:\n")
    lines.append(f"- Uniform Beta(1,7) posterior: {p_uniform:.4f}")
    lines.append(f"- Jeffreys Beta(0.5,6.5) posterior: {p_jeffreys:.4f}")
    lines.append(f"- Skeptical Beta(0.5,11.5) posterior: {p_skeptical:.4f}\n")
    lines.append("Expected-delivered-mass column in the sweep table above uses the uniform prior.")
    lines.append("Multiply by (jeffreys / uniform) = "
                 f"{p_jeffreys / p_uniform:.2f}× to get Jeffreys, "
                 f"by (skeptical / uniform) = {p_skeptical / p_uniform:.2f}× to get skeptical.\n")

    lines.append("### Hypothesis grading\n")
    lines.append("| Sub-claim | Predicted | Measured | Held? |")
    lines.append("|---|---|---|---|")
    h = results["hypothesis_grading"]
    a = h["H-mrsp-a_60wpkg_closes"]
    lines.append(f"| H-mrsp-a — 60 W/kg closes (11-14 yr, 5-40 t) | {a['predicted']} | "
                 f"round-trip {a['actual_round_trip_yr']:.2f} yr, delivered {a['actual_delivered_t']:.1f} t | "
                 f"{'yes' if a['held'] else '**no**'} |")
    b = h["H-mrsp-b_80wpkg_closes"]
    lines.append(f"| H-mrsp-b — 80 W/kg closes (9-13 yr, 30-80 t) | {b['predicted']} | "
                 f"round-trip {b['actual_round_trip_yr']:.2f} yr, delivered {b['actual_delivered_t']:.1f} t | "
                 f"{'yes' if b['held'] else '**no**'} |")
    c = h["H-mrsp-c_closure_threshold_wpkg"]
    lines.append(f"| H-mrsp-c — closure threshold W/kg | 40-60 (point 50) | "
                 f"{c['actual_threshold_w_per_kg']} | "
                 f"{'yes' if c['held'] else '**no**'} |")
    d = h["H-mrsp-d_delivered_fraction_at_80"]
    deliv_str = f"{d['actual_delivered_fraction_at_80wpkg']:.3f}" if d['actual_delivered_fraction_at_80wpkg'] is not None else "N/A"
    lines.append(f"| H-mrsp-d — delivered fraction at 80 W/kg | 0.15-0.40 (point 0.25) | "
                 f"{deliv_str} | "
                 f"{'yes' if d['held'] else '**no**'} |")
    e = h["H-mrsp-e_expected_delivered_t_at_60_uniform"]
    exp_str = f"{e['actual_expected_delivered_t_uniform']:.4f}" if e['actual_expected_delivered_t_uniform'] is not None else "N/A"
    lines.append(f"| H-mrsp-e — programmatic-risk-adjusted delivered at 60 W/kg, uniform prior | "
                 f"0.005-0.05 t (point 0.02) | {exp_str} t | "
                 f"{'yes' if e['held'] else '**no**'} |")

    (out_dir / "tables.md").write_text("\n".join(lines))
    return results


if __name__ == "__main__":
    out = main()
    print("R-megawatt-relaxed-specific-power complete.")
    print()
    print(f"  Closure threshold: {out['closure_threshold_w_per_kg']} W/kg")
    print()
    print("  Sweep (1 MWe, chunk 200 t, isp 2000 s):")
    print(f"    {'W/kg':>5} {'m_stack':>8} {'m_tug':>8} {'t_out':>6} {'t_in':>6} "
          f"{'RT_yr':>6} {'deliv':>7} {'frac':>6} {'closes':>8} {'exp_uni':>10}")
    for r in out["sweep"]:
        if not r.get("feasible"):
            print(f"    {r['specific_power_w_per_kg']:>5.0f}  INFEASIBLE")
            continue
        print(f"    {r['specific_power_w_per_kg']:>5.0f} {r['m_stack_t']:>8.2f} {r['m_tug_t']:>8.2f} "
              f"{r['t_outbound_burn_yr']:>6.2f} {r['t_inbound_burn_yr']:>6.2f} "
              f"{r['round_trip_yr']:>6.2f} {r['delivered_t']:>7.1f} {r['delivered_fraction']:>6.3f} "
              f"{'yes' if r['closes_15yr'] else 'no':>8} {r['expected_delivered_t_uniform']:>10.4f}")
    print()
    print("  Hypothesis grading:")
    for k, v in out["hypothesis_grading"].items():
        print(f"    {k}: {'HELD' if v['held'] else 'FALSIFIED'}")
