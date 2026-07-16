"""R-variant-B-500kWe-sizing — clean closure on Variant B (chemical-kick
outbound + electric-inbound) at 500 / 750 / 1000 kilowatt-electric, with
Modular-Assembled-Radiators-anchored mass model.

Reuses rhea's R-megawatt-marvl-radiator MARVL-anchored mass model and the
matrix-impulsive 6.42 kilometers-per-second inbound. See STUDY.md for the
pre-registered hypothesis block.

L0-05 closure interpreted with +/- 1 year soft margin per user clarification
(2026-05-15).
"""

from __future__ import annotations

import json
import math
from pathlib import Path

from waterprop.constants import A_EARTH, A_SATURN, G0, GM_SUN

YEAR_S = 365.25 * 86400.0

ETA_THR_ELECTRIC = 0.65
SATURN_OPS_YR = 1.0
ROUND_TRIP_CEILING_YR = 15.0
ROUND_TRIP_SOFT_MARGIN_YR = 1.0  # user-clarified 2026-05-15

# Inbound electric at the matrix-impulsive 6.42 km/s (chemical-kick architecture
# preserves Oberth-bonus impulsive efficiency).
DV_INBOUND_MATRIX_IMPULSIVE_KM_S = 6.42

# Chemical-kick configuration. Two scenarios reported:
#   - Conservative 9 km/s (matches matrix's all-electric-outbound delta-velocity)
#   - Realistic 5 km/s (3.6 trans-Saturn injection + 1.4 Saturn capture)
DV_CHEM_CONSERVATIVE_KM_S = 9.0
DV_CHEM_REALISTIC_KM_S = 5.0

ISP_HYDROLOX_S = 450.0
ISP_ELECTRIC_S = 2000.0
M_KICK_DRY_T = 10.0  # matches R_chunk_fed_chemical M_CHEM_DRY_KG

CHUNK_BASELINE_T = 200.0
REACTOR_POWERS_KWE = [500.0, 750.0, 1000.0]

# MARVL-anchored mass model (rhea, R_megawatt_marvl_radiator).
MARVL_MODEL = {
    "m_fixed_t": 5.0,
    "alpha_reactor_W_per_kg": 33.0,
    "alpha_PC_W_per_kg": 50.0,
    "alpha_radiator_kW_th_per_kg": 0.047,
    "eta_conv": 0.30,
    "f_tank": 0.05,
}

R_POWER_BAYESIAN_OVERLAY = (
    Path(__file__).parent.parent / "R_power_bayesian_update" / "results" / "matrix_overlay.json"
)


def marvl_dry_mass_t(reactor_kwe: float, m_prop_t: float = 0.0) -> dict:
    eta = MARVL_MODEL["eta_conv"]
    p_th_waste_kw = reactor_kwe * (1.0 - eta) / eta
    m_reactor = reactor_kwe / MARVL_MODEL["alpha_reactor_W_per_kg"]
    m_pc = reactor_kwe / MARVL_MODEL["alpha_PC_W_per_kg"]
    m_rad = p_th_waste_kw / MARVL_MODEL["alpha_radiator_kW_th_per_kg"] / 1000.0
    m_tank = m_prop_t * MARVL_MODEL["f_tank"]
    total = MARVL_MODEL["m_fixed_t"] + m_reactor + m_pc + m_rad + m_tank
    return {
        "m_fixed_t": MARVL_MODEL["m_fixed_t"],
        "m_reactor_t": m_reactor,
        "m_PC_t": m_pc,
        "m_radiator_t": m_rad,
        "m_tank_t": m_tank,
        "total_t": total,
        "radiator_fraction_of_total": m_rad / total if total > 0 else 0.0,
    }


def hohmann_cruise_yr() -> float:
    a_h_km = (A_EARTH + A_SATURN) / 2.0
    return math.pi * math.sqrt(a_h_km ** 3 / GM_SUN) / YEAR_S


def variant_b_closure(
    reactor_kwe: float,
    chunk_t: float,
    isp_electric_s: float,
    dv_chem_km_s: float,
    dv_inbound_km_s: float,
    m_kick_dry_t: float,
) -> dict:
    """Variant B closure: chemical kick outbound, electric inbound, MARVL mass."""
    # 1) Tug dry mass (no propellant yet).
    tug_breakdown = marvl_dry_mass_t(reactor_kwe, m_prop_t=0.0)
    m_tug_dry_t = tug_breakdown["total_t"]

    # 2) Inbound burn: chunk-fed wet-at-start at Saturn.
    # Wet mass at Saturn = tug + chunk (kick stage already jettisoned).
    # Iterate on tug mass to account for tank fraction on inbound propellant
    # (small effect at f_tank = 0.05; one or two passes converge).
    m_tug_t = m_tug_dry_t
    for _ in range(20):
        v_e_elec = isp_electric_s * G0
        m_initial_inbound_t = m_tug_t + chunk_t
        mass_ratio_in = math.exp(dv_inbound_km_s * 1000.0 / v_e_elec)
        m_prop_inbound_t = m_initial_inbound_t * (1.0 - 1.0 / mass_ratio_in)
        new_tug = marvl_dry_mass_t(reactor_kwe, m_prop_t=m_prop_inbound_t)["total_t"]
        if abs(new_tug - m_tug_t) < 1e-4:
            m_tug_t = new_tug
            break
        m_tug_t = new_tug
    m_initial_inbound_t = m_tug_t + chunk_t
    mass_ratio_in = math.exp(dv_inbound_km_s * 1000.0 / v_e_elec)
    m_prop_inbound_t = m_initial_inbound_t * (1.0 - 1.0 / mass_ratio_in)
    delivered_t = chunk_t - m_prop_inbound_t

    # 3) Inbound burn time.
    P_elec_w = reactor_kwe * 1000.0
    thrust_inbound_N = 2.0 * ETA_THR_ELECTRIC * P_elec_w / v_e_elec
    t_inbound_burn_s = m_prop_inbound_t * 1000.0 * v_e_elec / thrust_inbound_N
    t_inbound_burn_yr = t_inbound_burn_s / YEAR_S

    # 4) Chemical kick stage sizing: kick must accelerate (tug + kick_dry +
    # kick_prop + chunk_at_arrival_inferred=0 for outbound — chunk is
    # acquired at Saturn). Wet mass at start of chemical kick is tug + kick_dry
    # + kick_prop. Final mass after kick is tug + kick_dry. Solve for kick_prop.
    v_e_chem = ISP_HYDROLOX_S * G0
    mass_ratio_chem = math.exp(dv_chem_km_s * 1000.0 / v_e_chem)
    m_at_start_kick_t = (m_tug_t + m_kick_dry_t) * mass_ratio_chem
    m_kick_prop_t = m_at_start_kick_t - (m_tug_t + m_kick_dry_t)
    # Low-Earth-orbit launch mass for mission 1: total wet at Earth departure.
    m_LEO_mission1_t = m_at_start_kick_t
    # Mission-N depot-staged: kick propellant supplied by depot; only tug + kick_dry
    # need launching from Earth (matrix's 1.3x multiplier footnote on missions 2+).
    m_LEO_missionN_t = m_tug_t + m_kick_dry_t

    # 5) Round-trip time decomposition.
    cruise_yr = hohmann_cruise_yr()
    # Chemical kick is impulsive (~minutes); off the time budget. Outbound time
    # is just Hohmann cruise.
    round_trip_yr = cruise_yr + SATURN_OPS_YR + t_inbound_burn_yr + cruise_yr

    closes_strict = round_trip_yr <= ROUND_TRIP_CEILING_YR and delivered_t > 0
    closes_soft = (round_trip_yr <= ROUND_TRIP_CEILING_YR + ROUND_TRIP_SOFT_MARGIN_YR
                   and delivered_t > 0)

    return {
        "reactor_kwe": reactor_kwe,
        "chunk_t": chunk_t,
        "isp_electric_s": isp_electric_s,
        "dv_chem_km_s": dv_chem_km_s,
        "dv_inbound_km_s": dv_inbound_km_s,
        "m_kick_dry_t": m_kick_dry_t,
        "tug_breakdown": tug_breakdown,
        "m_tug_t_with_tank": m_tug_t,
        "m_kick_prop_t": m_kick_prop_t,
        "m_LEO_mission1_t": m_LEO_mission1_t,
        "m_LEO_missionN_t": m_LEO_missionN_t,
        "leo_multiplier_mission1": m_LEO_mission1_t / chunk_t,
        "mass_ratio_chem": mass_ratio_chem,
        "mass_ratio_inbound": mass_ratio_in,
        "thrust_inbound_N": thrust_inbound_N,
        "m_prop_inbound_t": m_prop_inbound_t,
        "delivered_t": delivered_t,
        "delivered_fraction": delivered_t / chunk_t if chunk_t > 0 else 0.0,
        "t_outbound_burn_yr": 0.0,  # impulsive
        "t_cruise_each_yr": cruise_yr,
        "t_saturn_ops_yr": SATURN_OPS_YR,
        "t_inbound_burn_yr": t_inbound_burn_yr,
        "round_trip_yr": round_trip_yr,
        "closes_strict_15yr": closes_strict,
        "closes_soft_16yr": closes_soft,
    }


def main() -> dict:
    # Reactor sweep at conservative + realistic chemical-kick delta-velocity.
    rows_conservative = [
        variant_b_closure(
            r, CHUNK_BASELINE_T, ISP_ELECTRIC_S,
            DV_CHEM_CONSERVATIVE_KM_S, DV_INBOUND_MATRIX_IMPULSIVE_KM_S, M_KICK_DRY_T,
        )
        for r in REACTOR_POWERS_KWE
    ]
    rows_realistic = [
        variant_b_closure(
            r, CHUNK_BASELINE_T, ISP_ELECTRIC_S,
            DV_CHEM_REALISTIC_KM_S, DV_INBOUND_MATRIX_IMPULSIVE_KM_S, M_KICK_DRY_T,
        )
        for r in REACTOR_POWERS_KWE
    ]

    # Programmatic-risk overlay: load Round A 500-kilowatt-electric-by-2035 probabilities.
    overlay = json.loads(R_POWER_BAYESIAN_OVERLAY.read_text())
    var_b_avail = overlay["variant_B_500kWe_chemical_kick_plus_electric_inbound"][
        "expected_delivered_mass_by_prior"
    ]
    p_uniform = var_b_avail["uniform_beta_1_1"]["p_reactor_available_by_window"]
    p_jeffreys = var_b_avail["jeffreys_beta_0p5_0p5"]["p_reactor_available_by_window"]
    p_skeptical = var_b_avail["skeptical_beta_0p5_5"]["p_reactor_available_by_window"]

    for rows in (rows_conservative, rows_realistic):
        for r in rows:
            d = max(r["delivered_t"], 0.0)
            r["expected_delivered_t_uniform"] = d * p_uniform
            r["expected_delivered_t_jeffreys"] = d * p_jeffreys
            r["expected_delivered_t_skeptical"] = d * p_skeptical

    # Lookups for hypothesis grading (conservative scenario, since pre-registration
    # was anchored at 9 km/s).
    def at_kwe(rows, kwe):
        for r in rows:
            if math.isclose(r["reactor_kwe"], kwe):
                return r
        return None

    r500_cons = at_kwe(rows_conservative, 500.0)
    r1000_cons = at_kwe(rows_conservative, 1000.0)

    h_vbs_a = {
        "predicted_round_trip_yr": [12.5, 14.5],
        "point": 13.5,
        "actual_round_trip_yr": r500_cons["round_trip_yr"],
        "held": 12.5 <= r500_cons["round_trip_yr"] <= 14.5,
    }
    h_vbs_b = {
        "predicted_delivered_t": [80.0, 110.0],
        "point": 95.0,
        "actual_delivered_t": r500_cons["delivered_t"],
        "held": 80.0 <= r500_cons["delivered_t"] <= 110.0,
    }
    h_vbs_c = {
        "predicted_round_trip_yr_at_1000": [12.0, 13.5],
        "predicted_delivered_t_at_1000": [100.0, 125.0],
        "actual_round_trip_yr_at_1000": r1000_cons["round_trip_yr"],
        "actual_delivered_t_at_1000": r1000_cons["delivered_t"],
        "held": (12.0 <= r1000_cons["round_trip_yr"] <= 13.5
                 and 100.0 <= r1000_cons["delivered_t"] <= 125.0),
    }
    h_vbs_d = {
        "predicted_LEO_t": [350.0, 550.0],
        "point": 450.0,
        "actual_LEO_mission1_t": r500_cons["m_LEO_mission1_t"],
        "held": 350.0 <= r500_cons["m_LEO_mission1_t"] <= 550.0,
    }
    h_vbs_e = {
        "predicted_expected_delivered_t": [0.10, 0.15],
        "point": 0.12,
        "actual_expected_delivered_t_uniform": r500_cons["expected_delivered_t_uniform"],
        "held": 0.10 <= r500_cons["expected_delivered_t_uniform"] <= 0.15,
    }

    results = {
        "config": {
            "isp_electric_s": ISP_ELECTRIC_S,
            "isp_hydrolox_s": ISP_HYDROLOX_S,
            "dv_inbound_km_s": DV_INBOUND_MATRIX_IMPULSIVE_KM_S,
            "dv_chem_conservative_km_s": DV_CHEM_CONSERVATIVE_KM_S,
            "dv_chem_realistic_km_s": DV_CHEM_REALISTIC_KM_S,
            "chunk_t": CHUNK_BASELINE_T,
            "m_kick_dry_t": M_KICK_DRY_T,
            "ceiling_yr": ROUND_TRIP_CEILING_YR,
            "soft_margin_yr": ROUND_TRIP_SOFT_MARGIN_YR,
            "marvl_model": MARVL_MODEL,
        },
        "rows_conservative_dv_chem_9km_s": rows_conservative,
        "rows_realistic_dv_chem_5km_s": rows_realistic,
        "programmatic_risk_overlay_priors": {
            "p_500kWe_avail_by_2035_uniform": p_uniform,
            "p_500kWe_avail_by_2035_jeffreys": p_jeffreys,
            "p_500kWe_avail_by_2035_skeptical": p_skeptical,
        },
        "hypothesis_grading": {
            "H-vbs-a_500kWe_round_trip": h_vbs_a,
            "H-vbs-b_500kWe_delivered": h_vbs_b,
            "H-vbs-c_1000kWe_slope": h_vbs_c,
            "H-vbs-d_500kWe_LEO_launch_mass": h_vbs_d,
            "H-vbs-e_expected_delivered_500kWe_uniform": h_vbs_e,
        },
    }

    out_dir = Path(__file__).parent / "results"
    out_dir.mkdir(exist_ok=True)
    (out_dir / "R_variant_B_500kWe_sizing.json").write_text(
        json.dumps(results, indent=2, default=str)
    )

    # Tables
    lines = []
    lines.append("### Variant B at MARVL-anchored mass — conservative chemical-kick "
                 "(9 km/s), inbound 6.42 km/s, chunk 200 t, specific impulse 2000 s\n")
    lines.append("| Reactor (kWe) | Tug dry (t) | Kick prop (t) | LEO mission-1 (t) | "
                 "LEO missionN (t) | Inbound prop (t) | t_in (yr) | Round-trip (yr) | "
                 "Delivered (t) | Fraction | Closes strict 15? | Closes soft 16? | "
                 "Expected (uniform, t) |")
    lines.append("|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|:--:|:--:|---:|")
    for r in rows_conservative:
        flag_strict = "**yes**" if r["closes_strict_15yr"] else "no"
        flag_soft = "**yes**" if r["closes_soft_16yr"] else "no"
        lines.append(
            f"| {r['reactor_kwe']:.0f} | {r['m_tug_t_with_tank']:.1f} | "
            f"{r['m_kick_prop_t']:.1f} | {r['m_LEO_mission1_t']:.1f} | "
            f"{r['m_LEO_missionN_t']:.1f} | {r['m_prop_inbound_t']:.1f} | "
            f"{r['t_inbound_burn_yr']:.2f} | {r['round_trip_yr']:.2f} | "
            f"{r['delivered_t']:.1f} | {r['delivered_fraction']:.3f} | "
            f"{flag_strict} | {flag_soft} | {r['expected_delivered_t_uniform']:.4f} |"
        )
    lines.append("")

    lines.append("### Variant B at MARVL-anchored mass — realistic chemical-kick "
                 "(5 km/s; 3.6 trans-Saturn injection + 1.4 Saturn capture), other parameters identical\n")
    lines.append("| Reactor (kWe) | Tug dry (t) | Kick prop (t) | LEO mission-1 (t) | "
                 "LEO missionN (t) | Inbound prop (t) | t_in (yr) | Round-trip (yr) | "
                 "Delivered (t) | Fraction | Closes strict 15? | Closes soft 16? | "
                 "Expected (uniform, t) |")
    lines.append("|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|:--:|:--:|---:|")
    for r in rows_realistic:
        flag_strict = "**yes**" if r["closes_strict_15yr"] else "no"
        flag_soft = "**yes**" if r["closes_soft_16yr"] else "no"
        lines.append(
            f"| {r['reactor_kwe']:.0f} | {r['m_tug_t_with_tank']:.1f} | "
            f"{r['m_kick_prop_t']:.1f} | {r['m_LEO_mission1_t']:.1f} | "
            f"{r['m_LEO_missionN_t']:.1f} | {r['m_prop_inbound_t']:.1f} | "
            f"{r['t_inbound_burn_yr']:.2f} | {r['round_trip_yr']:.2f} | "
            f"{r['delivered_t']:.1f} | {r['delivered_fraction']:.3f} | "
            f"{flag_strict} | {flag_soft} | {r['expected_delivered_t_uniform']:.4f} |"
        )
    lines.append("")

    lines.append("### MARVL mass breakdown at each reactor power (no propellant)\n")
    lines.append("| Reactor (kWe) | m_fixed (t) | m_reactor (t) | m_PC (t) | m_radiator (t) | "
                 "Total (t) | Radiator fraction |")
    lines.append("|---:|---:|---:|---:|---:|---:|---:|")
    for r in rows_conservative:
        b = r["tug_breakdown"]
        lines.append(
            f"| {r['reactor_kwe']:.0f} | {b['m_fixed_t']:.1f} | {b['m_reactor_t']:.1f} | "
            f"{b['m_PC_t']:.1f} | {b['m_radiator_t']:.1f} | {b['total_t']:.1f} | "
            f"{b['radiator_fraction_of_total']*100:.1f}% |"
        )
    lines.append("")

    lines.append("### Programmatic-risk overlay (Round A propagation)\n")
    lines.append(f"P(500-kilowatt-electric class reactor on orbit by 2035) per prior:\n")
    lines.append(f"- Uniform Beta(1,7) posterior: {p_uniform:.4f}")
    lines.append(f"- Jeffreys Beta(0.5,6.5) posterior: {p_jeffreys:.4f}")
    lines.append(f"- Skeptical Beta(0.5,11.5) posterior: {p_skeptical:.4f}\n")

    lines.append("### Hypothesis grading\n")
    lines.append("| Sub-claim | Predicted | Measured | Held? |")
    lines.append("|---|---|---|---|")
    h = results["hypothesis_grading"]
    a = h["H-vbs-a_500kWe_round_trip"]
    lines.append(f"| H-vbs-a — 500 kWe round-trip (yr) | 12.5-14.5 (point 13.5) | "
                 f"{a['actual_round_trip_yr']:.2f} | {'yes' if a['held'] else '**no**'} |")
    b = h["H-vbs-b_500kWe_delivered"]
    lines.append(f"| H-vbs-b — 500 kWe delivered (t) | 80-110 (point 95) | "
                 f"{b['actual_delivered_t']:.1f} | {'yes' if b['held'] else '**no**'} |")
    c = h["H-vbs-c_1000kWe_slope"]
    lines.append(f"| H-vbs-c — 1000 kWe round-trip 12.0-13.5 yr AND delivered 100-125 t | "
                 f"see ranges | round-trip {c['actual_round_trip_yr_at_1000']:.2f} yr, "
                 f"delivered {c['actual_delivered_t_at_1000']:.1f} t | "
                 f"{'yes' if c['held'] else '**no**'} |")
    d = h["H-vbs-d_500kWe_LEO_launch_mass"]
    lines.append(f"| H-vbs-d — 500 kWe LEO mission-1 launch mass (t) | 350-550 (point 450) | "
                 f"{d['actual_LEO_mission1_t']:.1f} | {'yes' if d['held'] else '**no**'} |")
    e = h["H-vbs-e_expected_delivered_500kWe_uniform"]
    lines.append(f"| H-vbs-e — 500 kWe expected delivered, uniform prior (t) | "
                 f"0.10-0.15 (point 0.12) | {e['actual_expected_delivered_t_uniform']:.4f} | "
                 f"{'yes' if e['held'] else '**no**'} |")

    (out_dir / "tables.md").write_text("\n".join(lines))
    return results


if __name__ == "__main__":
    out = main()
    print("R-variant-B-500kWe-sizing complete.")
    print()
    print("  Conservative chem-kick 9 km/s:")
    print(f"    {'kWe':>5} {'tug':>6} {'kick_p':>7} {'LEO_m1':>7} {'inb_p':>7} "
          f"{'t_in':>6} {'RT_yr':>6} {'deliv':>7} {'frac':>6} {'strict':>7} {'soft':>6}")
    for r in out["rows_conservative_dv_chem_9km_s"]:
        print(f"    {r['reactor_kwe']:>5.0f} {r['m_tug_t_with_tank']:>6.1f} "
              f"{r['m_kick_prop_t']:>7.1f} {r['m_LEO_mission1_t']:>7.1f} "
              f"{r['m_prop_inbound_t']:>7.1f} {r['t_inbound_burn_yr']:>6.2f} "
              f"{r['round_trip_yr']:>6.2f} {r['delivered_t']:>7.1f} "
              f"{r['delivered_fraction']:>6.3f} "
              f"{'yes' if r['closes_strict_15yr'] else 'no':>7} "
              f"{'yes' if r['closes_soft_16yr'] else 'no':>6}")
    print()
    print("  Realistic chem-kick 5 km/s:")
    for r in out["rows_realistic_dv_chem_5km_s"]:
        print(f"    {r['reactor_kwe']:>5.0f} {r['m_tug_t_with_tank']:>6.1f} "
              f"{r['m_kick_prop_t']:>7.1f} {r['m_LEO_mission1_t']:>7.1f} "
              f"{r['m_prop_inbound_t']:>7.1f} {r['t_inbound_burn_yr']:>6.2f} "
              f"{r['round_trip_yr']:>6.2f} {r['delivered_t']:>7.1f} "
              f"{r['delivered_fraction']:>6.3f} "
              f"{'yes' if r['closes_strict_15yr'] else 'no':>7} "
              f"{'yes' if r['closes_soft_16yr'] else 'no':>6}")
    print()
    print("  Hypothesis grading (against conservative 9 km/s scenario):")
    for k, v in out["hypothesis_grading"].items():
        print(f"    {k}: {'HELD' if v['held'] else 'FALSIFIED'}")
