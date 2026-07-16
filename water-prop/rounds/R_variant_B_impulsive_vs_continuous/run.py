"""R-variant-B-impulsive-vs-continuous — re-derive Variant B inbound delta-velocity
from first principles. The matrix-impulsive 6.42 km/s assumption is
architecturally incoherent for an electric inbound burn; substitute titan's
continuous-thrust segment decomposition and re-run Round C closure under each
of four architectural recovery variants.

See STUDY.md for the pre-registered hypothesis block.
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

# Titan's segment decomposition (R_inbound_dv_continuous_thrust results).
# Saturn departure orbit dependence is in segment 1 only.
DV_SATURN_SPIRAL_KM_S = {
    "B_ring": 16.762,
    "high_elliptical_1Mkm": 6.159,
    "Iapetus_distance": 3.264,
}
DV_HELIO_RETROGRADE_KM_S = 5.439  # segment 2 (Saturn helio -> Hohmann aphelion)
DV_EARTH_HELIO_KM_S = 10.298       # segment 4 (Hohmann perihelion -> Earth helio)
DV_LEO_SPIRAL_KM_S = 7.669         # segment 5 (Earth-escape -> LEO 400 km)
LGA_CREDIT_KM_S = 2.0              # applied to Earth-side segment(s)

# Saturn-egress impulsive chemical-kick figure (matrix's number)
DV_SATURN_EGRESS_IMPULSIVE_KM_S = 2.09
ISP_HYDROLOX_S = 450.0
M_SATURN_KICK_DRY_T = 10.0  # author-asserted; matches outbound kick stage

# Inherit Round C / rhea defaults
DV_CHEM_OUTBOUND_KM_S = 5.0  # realistic chemical-kick outbound (3.6 TSI + 1.4 capture)
ISP_ELECTRIC_S = 2000.0
M_OUTBOUND_KICK_DRY_T = 10.0
CHUNK_BASELINE_T = 200.0
REACTOR_POWERS_KWE = [500.0, 750.0, 1000.0]

# MARVL-anchored mass model (rhea / Round C)
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


def marvl_dry_mass_t(reactor_kwe: float, m_prop_t: float = 0.0) -> float:
    eta = MARVL_MODEL["eta_conv"]
    p_th_waste_kw = reactor_kwe * (1.0 - eta) / eta
    m_reactor = reactor_kwe / MARVL_MODEL["alpha_reactor_W_per_kg"]
    m_pc = reactor_kwe / MARVL_MODEL["alpha_PC_W_per_kg"]
    m_rad = p_th_waste_kw / MARVL_MODEL["alpha_radiator_kW_th_per_kg"] / 1000.0
    m_tank = m_prop_t * MARVL_MODEL["f_tank"]
    return MARVL_MODEL["m_fixed_t"] + m_reactor + m_pc + m_rad + m_tank


def hohmann_cruise_yr() -> float:
    a_h_km = (A_EARTH + A_SATURN) / 2.0
    return math.pi * math.sqrt(a_h_km ** 3 / GM_SUN) / YEAR_S


def variant_inbound_dv(variant: str, departure_orbit: str) -> dict:
    """Compute the corrected inbound delta-velocity for one architecture variant.

    Variants:
      A — as-stated (no recovery): segments 1+2+4+5 minus LGA credit on Earth side
      B — Saturn-egress chemical kick: segments 2+4+5 minus LGA, plus impulsive Saturn-egress
      C — Earth aerocapture: segments 1+2+4 minus LGA (on segment 4)
      D — both: segments 2+4 minus LGA, plus impulsive Saturn-egress
    """
    saturn_spiral = DV_SATURN_SPIRAL_KM_S[departure_orbit]
    helio_retro = DV_HELIO_RETROGRADE_KM_S
    earth_helio = DV_EARTH_HELIO_KM_S
    leo_spiral = DV_LEO_SPIRAL_KM_S

    if variant == "A_as_stated":
        electric_dv = saturn_spiral + helio_retro + earth_helio + leo_spiral - LGA_CREDIT_KM_S
        impulsive_dv = 0.0
    elif variant == "B_saturn_egress_kick":
        electric_dv = helio_retro + earth_helio + leo_spiral - LGA_CREDIT_KM_S
        impulsive_dv = DV_SATURN_EGRESS_IMPULSIVE_KM_S
    elif variant == "C_earth_aerocapture":
        electric_dv = saturn_spiral + helio_retro + earth_helio - LGA_CREDIT_KM_S
        impulsive_dv = 0.0
    elif variant == "D_both":
        electric_dv = helio_retro + earth_helio - LGA_CREDIT_KM_S
        impulsive_dv = DV_SATURN_EGRESS_IMPULSIVE_KM_S
    else:
        raise ValueError(f"unknown variant {variant}")

    return {
        "variant": variant,
        "departure_orbit": departure_orbit,
        "saturn_spiral_km_s": saturn_spiral,
        "helio_retrograde_km_s": helio_retro,
        "earth_helio_km_s": earth_helio,
        "leo_spiral_km_s": leo_spiral,
        "lga_credit_km_s": LGA_CREDIT_KM_S,
        "electric_dv_km_s": electric_dv,
        "impulsive_egress_dv_km_s": impulsive_dv,
        "matrix_baseline_dv_km_s": 6.42,
        "ratio_to_matrix": electric_dv / 6.42,
    }


def variant_b_closure(
    reactor_kwe: float,
    chunk_t: float,
    isp_electric_s: float,
    dv_chem_outbound_km_s: float,
    dv_inbound_electric_km_s: float,
    dv_inbound_impulsive_km_s: float,
    aerocapture: bool,
    m_outbound_kick_dry_t: float,
    m_saturn_kick_dry_t: float,
) -> dict:
    """Variant B closure with corrected inbound delta-velocity decomposition."""
    # 1) Tug dry mass
    m_tug_t = marvl_dry_mass_t(reactor_kwe, m_prop_t=0.0)

    # 2) Saturn-egress impulsive kick (consumes chunk water as hydrolox propellant
    # if dv_inbound_impulsive_km_s > 0). The kick stage dry mass adds to the
    # mass that must be accelerated, then is jettisoned.
    if dv_inbound_impulsive_km_s > 0:
        v_e_chem = ISP_HYDROLOX_S * G0
        # Wet mass at start of Saturn-egress kick = tug + saturn-kick-dry + chunk
        m_at_start_egress_t = (m_tug_t + m_saturn_kick_dry_t + chunk_t)
        # Solve for kick-prop required to give dv_impulsive
        # m_after = m_before / mass_ratio; mass_ratio = exp(dv/v_e)
        # m_prop = m_before * (1 - 1/mass_ratio)
        mr_egress = math.exp(dv_inbound_impulsive_km_s * 1000.0 / v_e_chem)
        # Need m_after_egress = (m_tug + m_saturn_kick_dry + chunk_minus_egress_prop)
        # And m_at_start = m_after × mass_ratio
        # Equivalently: m_egress_prop = m_at_start × (1 - 1/mass_ratio)
        m_egress_prop_t = m_at_start_egress_t * (1.0 - 1.0 / mr_egress)
        if m_egress_prop_t > chunk_t:
            return {
                "feasible": False,
                "reason": "Saturn-egress chemical kick would consume more than chunk inventory",
            }
        chunk_after_egress_t = chunk_t - m_egress_prop_t
        # Jettison the Saturn-kick stage dry mass
        m_after_egress_t = m_tug_t + chunk_after_egress_t  # kick stage dry mass discarded
    else:
        m_egress_prop_t = 0.0
        chunk_after_egress_t = chunk_t
        m_after_egress_t = m_tug_t + chunk_t

    # 3) Electric inbound burn (continuous-thrust)
    # Iterate on tug-mass for tank fraction
    chunk_at_inbound_start = chunk_after_egress_t
    for _ in range(20):
        v_e_elec = isp_electric_s * G0
        m_initial_inbound_t = m_tug_t + chunk_at_inbound_start
        mr_inbound = math.exp(dv_inbound_electric_km_s * 1000.0 / v_e_elec)
        m_prop_inbound_t = m_initial_inbound_t * (1.0 - 1.0 / mr_inbound)
        if m_prop_inbound_t > chunk_at_inbound_start:
            return {
                "feasible": False,
                "reason": "electric inbound burn requires more propellant than chunk has",
                "m_prop_required_t": m_prop_inbound_t,
                "chunk_at_inbound_start_t": chunk_at_inbound_start,
                "m_tug_t": m_tug_t,
                "delivered_t": chunk_at_inbound_start - m_prop_inbound_t,
                "round_trip_yr": math.inf,
            }
        new_tug = marvl_dry_mass_t(reactor_kwe, m_prop_t=m_prop_inbound_t)
        if abs(new_tug - m_tug_t) < 1e-4:
            m_tug_t = new_tug
            break
        m_tug_t = new_tug

    delivered_at_earth_arrival_t = chunk_at_inbound_start - m_prop_inbound_t

    # If aerocapture: the LEO-spiral segment is replaced by atmosphere; no electric
    # propellant cost (already excluded from dv_inbound_electric_km_s above).
    delivered_t = delivered_at_earth_arrival_t

    # 4) Inbound burn time
    P_elec_w = reactor_kwe * 1000.0
    thrust_inbound_N = 2.0 * ETA_THR_ELECTRIC * P_elec_w / v_e_elec
    t_inbound_burn_s = m_prop_inbound_t * 1000.0 * v_e_elec / thrust_inbound_N
    t_inbound_burn_yr = t_inbound_burn_s / YEAR_S

    # 5) Outbound chemical kick mass + propellant (Round C-style, realistic 5 km/s)
    v_e_chem_out = ISP_HYDROLOX_S * G0
    mr_chem_out = math.exp(dv_chem_outbound_km_s * 1000.0 / v_e_chem_out)
    m_at_start_kick_t = (m_tug_t + m_outbound_kick_dry_t) * mr_chem_out
    m_outbound_kick_prop_t = m_at_start_kick_t - (m_tug_t + m_outbound_kick_dry_t)
    m_LEO_mission1_t = m_at_start_kick_t  # outbound kick prop launched from Earth

    # 6) Round-trip time
    cruise_yr = hohmann_cruise_yr()
    # Outbound chemical kick is impulsive (off time budget). Outbound = cruise.
    # Saturn-egress impulsive kick (if present) is impulsive. Inbound = electric
    # burn time + cruise. Aerocapture replaces LEO spiral cleanly; assume 1 day
    # negligible.
    round_trip_yr = cruise_yr + SATURN_OPS_YR + t_inbound_burn_yr + cruise_yr

    closes_strict = (round_trip_yr <= ROUND_TRIP_CEILING_YR) and (delivered_t > 0)
    closes_soft = (round_trip_yr <= ROUND_TRIP_CEILING_YR + ROUND_TRIP_SOFT_MARGIN_YR
                   and delivered_t > 0)

    return {
        "feasible": True,
        "reactor_kwe": reactor_kwe,
        "chunk_t": chunk_t,
        "isp_electric_s": isp_electric_s,
        "dv_inbound_electric_km_s": dv_inbound_electric_km_s,
        "dv_inbound_impulsive_km_s": dv_inbound_impulsive_km_s,
        "aerocapture": aerocapture,
        "m_tug_t": m_tug_t,
        "m_outbound_kick_prop_t": m_outbound_kick_prop_t,
        "m_LEO_mission1_t": m_LEO_mission1_t,
        "m_egress_prop_t": m_egress_prop_t,
        "chunk_after_egress_t": chunk_after_egress_t,
        "m_prop_inbound_t": m_prop_inbound_t,
        "delivered_t": delivered_t,
        "delivered_fraction": delivered_t / chunk_t,
        "thrust_inbound_N": thrust_inbound_N,
        "mass_ratio_inbound": mr_inbound,
        "t_outbound_burn_yr": 0.0,
        "t_cruise_each_yr": cruise_yr,
        "t_saturn_ops_yr": SATURN_OPS_YR,
        "t_inbound_burn_yr": t_inbound_burn_yr,
        "round_trip_yr": round_trip_yr,
        "closes_strict_15yr": closes_strict,
        "closes_soft_16yr": closes_soft,
    }


def main() -> dict:
    departure_default = "high_elliptical_1Mkm"

    # 1. Build the four variants' inbound delta-velocities at the default departure orbit.
    variants = {
        "A_as_stated": variant_inbound_dv("A_as_stated", departure_default),
        "B_saturn_egress_kick": variant_inbound_dv("B_saturn_egress_kick", departure_default),
        "C_earth_aerocapture": variant_inbound_dv("C_earth_aerocapture", departure_default),
        "D_both": variant_inbound_dv("D_both", departure_default),
    }

    # 2. Run Round C closure for each variant at 500 / 750 / 1000 kWe.
    closures = {}
    for vname, vdata in variants.items():
        rows = []
        for kwe in REACTOR_POWERS_KWE:
            row = variant_b_closure(
                reactor_kwe=kwe,
                chunk_t=CHUNK_BASELINE_T,
                isp_electric_s=ISP_ELECTRIC_S,
                dv_chem_outbound_km_s=DV_CHEM_OUTBOUND_KM_S,
                dv_inbound_electric_km_s=vdata["electric_dv_km_s"],
                dv_inbound_impulsive_km_s=vdata["impulsive_egress_dv_km_s"],
                aerocapture=(vname in ("C_earth_aerocapture", "D_both")),
                m_outbound_kick_dry_t=M_OUTBOUND_KICK_DRY_T,
                m_saturn_kick_dry_t=M_SATURN_KICK_DRY_T,
            )
            row["variant"] = vname
            rows.append(row)
        closures[vname] = rows

    # 3. Departure-orbit sensitivity at 500 kWe, variant A (worst case for matrix's claim)
    sens_dep_orbit = {}
    for orbit_name in DV_SATURN_SPIRAL_KM_S:
        v = variant_inbound_dv("A_as_stated", orbit_name)
        row = variant_b_closure(
            reactor_kwe=500.0,
            chunk_t=CHUNK_BASELINE_T,
            isp_electric_s=ISP_ELECTRIC_S,
            dv_chem_outbound_km_s=DV_CHEM_OUTBOUND_KM_S,
            dv_inbound_electric_km_s=v["electric_dv_km_s"],
            dv_inbound_impulsive_km_s=v["impulsive_egress_dv_km_s"],
            aerocapture=False,
            m_outbound_kick_dry_t=M_OUTBOUND_KICK_DRY_T,
            m_saturn_kick_dry_t=M_SATURN_KICK_DRY_T,
        )
        row["departure_orbit"] = orbit_name
        row["dv_inbound_electric_km_s"] = v["electric_dv_km_s"]
        sens_dep_orbit[orbit_name] = row

    # 4. Programmatic-risk overlay
    overlay = json.loads(R_POWER_BAYESIAN_OVERLAY.read_text())
    var_b_avail = overlay["variant_B_500kWe_chemical_kick_plus_electric_inbound"][
        "expected_delivered_mass_by_prior"
    ]
    p_uniform = var_b_avail["uniform_beta_1_1"]["p_reactor_available_by_window"]
    for vname, rows in closures.items():
        for r in rows:
            if not r.get("feasible"):
                continue
            d = max(r["delivered_t"], 0.0)
            r["expected_delivered_t_uniform"] = d * p_uniform

    # 5. Hypothesis grading.
    h_vbic_a = {
        "predicted_range_km_s": [24.0, 30.0],
        "point_km_s": 27.0,
        "actual_km_s": variants["A_as_stated"]["electric_dv_km_s"],
        "held": 24.0 <= variants["A_as_stated"]["electric_dv_km_s"] <= 30.0,
    }
    h_vbic_b = {
        "predicted_range_km_s": [20.0, 24.0],
        "point_km_s": 21.4,
        "actual_km_s": variants["B_saturn_egress_kick"]["electric_dv_km_s"],
        "held": 20.0 <= variants["B_saturn_egress_kick"]["electric_dv_km_s"] <= 24.0,
    }
    h_vbic_c = {
        "predicted_range_km_s": [18.0, 22.0],
        "point_km_s": 19.9,
        "actual_km_s": variants["C_earth_aerocapture"]["electric_dv_km_s"],
        "held": 18.0 <= variants["C_earth_aerocapture"]["electric_dv_km_s"] <= 22.0,
    }
    h_vbic_d = {
        "predicted_range_km_s": [12.0, 16.0],
        "point_km_s": 13.7,
        "actual_km_s": variants["D_both"]["electric_dv_km_s"],
        "held": 12.0 <= variants["D_both"]["electric_dv_km_s"] <= 16.0,
    }
    # H-vbic-e: Variant A at 500 kWe — does NOT close inside soft margin
    closure_A_500 = closures["A_as_stated"][0]  # 500 kWe is first
    h_vbic_e = {
        "predicted": "round-trip 16-18 yr (over soft ceiling), delivered 0-25 t, cell does NOT close",
        "actual_round_trip_yr": closure_A_500.get("round_trip_yr", math.inf),
        "actual_delivered_t": closure_A_500.get("delivered_t", -math.inf),
        "actual_closes_soft": closure_A_500.get("closes_soft_16yr", False),
        "held": (closure_A_500.get("closes_soft_16yr", False) is False
                 and 0.0 <= closure_A_500.get("delivered_t", -1) <= 25.0
                 and 16.0 <= closure_A_500.get("round_trip_yr", math.inf) <= 18.0),
    }
    # H-vbic-f: Variant D at 500 kWe — closes inside soft margin
    closure_D_500 = closures["D_both"][0]
    h_vbic_f = {
        "predicted": "closes inside soft margin with delivered 80-110 t, round-trip ~14.5 yr",
        "actual_round_trip_yr": closure_D_500.get("round_trip_yr", math.inf),
        "actual_delivered_t": closure_D_500.get("delivered_t", -math.inf),
        "actual_closes_soft": closure_D_500.get("closes_soft_16yr", False),
        "held": (closure_D_500.get("closes_soft_16yr", False)
                 and 80.0 <= closure_D_500.get("delivered_t", -1) <= 110.0
                 and 13.5 <= closure_D_500.get("round_trip_yr", math.inf) <= 15.5),
    }

    results = {
        "config": {
            "departure_default": departure_default,
            "isp_electric_s": ISP_ELECTRIC_S,
            "isp_hydrolox_s": ISP_HYDROLOX_S,
            "dv_chem_outbound_km_s": DV_CHEM_OUTBOUND_KM_S,
            "dv_saturn_egress_impulsive_km_s": DV_SATURN_EGRESS_IMPULSIVE_KM_S,
            "lga_credit_km_s": LGA_CREDIT_KM_S,
            "matrix_baseline_dv_inbound_km_s": 6.42,
            "chunk_t": CHUNK_BASELINE_T,
            "ceiling_yr": ROUND_TRIP_CEILING_YR,
            "soft_margin_yr": ROUND_TRIP_SOFT_MARGIN_YR,
        },
        "inbound_dv_per_variant": variants,
        "closures_per_variant": closures,
        "departure_orbit_sensitivity_variant_A_500kWe": sens_dep_orbit,
        "hypothesis_grading": {
            "H-vbic-a_variant_A_inbound_dv": h_vbic_a,
            "H-vbic-b_variant_B_inbound_dv": h_vbic_b,
            "H-vbic-c_variant_C_inbound_dv": h_vbic_c,
            "H-vbic-d_variant_D_inbound_dv": h_vbic_d,
            "H-vbic-e_variant_A_500kWe_does_not_close": h_vbic_e,
            "H-vbic-f_variant_D_500kWe_closes": h_vbic_f,
        },
    }
    out_dir = Path(__file__).parent / "results"
    out_dir.mkdir(exist_ok=True)
    (out_dir / "R_variant_B_impulsive_vs_continuous.json").write_text(
        json.dumps(results, indent=2, default=str)
    )

    # Tables
    lines = []
    lines.append("### Inbound delta-velocity per architecture variant (high-elliptical 1 Mkm Saturn departure, with Lunar Gravity Assist credit)\n")
    lines.append("| Variant | Description | Saturn spiral | Helio retro | Earth helio | LEO spiral | LGA | Saturn-egress kick | **Electric DV total** | Ratio to matrix 6.42 |")
    lines.append("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    var_descs = {
        "A_as_stated": "as-stated (no recovery)",
        "B_saturn_egress_kick": "+ chemical Saturn egress",
        "C_earth_aerocapture": "+ Earth aerocapture",
        "D_both": "+ both recoveries",
    }
    for vname, v in variants.items():
        sat_spi = v["saturn_spiral_km_s"] if vname in ("A_as_stated", "C_earth_aerocapture") else "n/a (kick)"
        leo_sp = v["leo_spiral_km_s"] if vname in ("A_as_stated", "B_saturn_egress_kick") else "n/a (aero)"
        lines.append(f"| {vname} | {var_descs[vname]} | {sat_spi} | "
                     f"{v['helio_retrograde_km_s']:.2f} | {v['earth_helio_km_s']:.2f} | "
                     f"{leo_sp} | -{v['lga_credit_km_s']:.1f} | "
                     f"{v['impulsive_egress_dv_km_s']:.2f} (impulsive) | "
                     f"**{v['electric_dv_km_s']:.2f}** | {v['ratio_to_matrix']:.2f}× |")
    lines.append("")

    lines.append("### Variant B closure under each corrected delta-velocity, MARVL-anchored mass, chunk 200 t, specific impulse 2000 s\n")
    for vname, rows in closures.items():
        lines.append(f"#### {vname} ({var_descs[vname]}, electric inbound DV = {variants[vname]['electric_dv_km_s']:.2f} km/s)\n")
        lines.append("| Reactor (kWe) | Tug (t) | Egress prop (t, chem) | Inbound prop (t, elec) | Delivered (t) | Fraction | t_inbound (yr) | Round-trip (yr) | Strict 15? | Soft 16? | Expected (uniform, t) |")
        lines.append("|---:|---:|---:|---:|---:|---:|---:|---:|:--:|:--:|---:|")
        for r in rows:
            if not r.get("feasible"):
                lines.append(f"| {r.get('reactor_kwe', '?')} | INFEASIBLE: {r.get('reason', 'unknown')} |")
                continue
            flag_strict = "**yes**" if r["closes_strict_15yr"] else "no"
            flag_soft = "**yes**" if r["closes_soft_16yr"] else "no"
            lines.append(
                f"| {r['reactor_kwe']:.0f} | {r['m_tug_t']:.1f} | "
                f"{r.get('m_egress_prop_t', 0):.1f} | {r['m_prop_inbound_t']:.1f} | "
                f"{r['delivered_t']:.1f} | {r['delivered_fraction']:.3f} | "
                f"{r['t_inbound_burn_yr']:.2f} | {r['round_trip_yr']:.2f} | "
                f"{flag_strict} | {flag_soft} | "
                f"{r.get('expected_delivered_t_uniform', 0):.4f} |"
            )
        lines.append("")

    lines.append("### Departure-orbit sensitivity, variant A, 500 kWe\n")
    lines.append("| Departure orbit | Saturn spiral DV (km/s) | Total electric inbound DV (km/s) | Round-trip (yr) | Delivered (t) | Closes soft 16? |")
    lines.append("|---|---:|---:|---:|---:|:--:|")
    for orbit, r in sens_dep_orbit.items():
        if not r.get("feasible"):
            lines.append(f"| {orbit} | {DV_SATURN_SPIRAL_KM_S[orbit]:.2f} | {r.get('dv_inbound_electric_km_s', 0):.2f} | INFEASIBLE | INFEASIBLE | no |")
            continue
        flag = "**yes**" if r["closes_soft_16yr"] else "no"
        lines.append(f"| {orbit} | {DV_SATURN_SPIRAL_KM_S[orbit]:.2f} | "
                     f"{r['dv_inbound_electric_km_s']:.2f} | "
                     f"{r['round_trip_yr']:.2f} | {r['delivered_t']:.1f} | {flag} |")
    lines.append("")

    lines.append("### Hypothesis grading\n")
    lines.append("| Sub-claim | Predicted | Measured | Held? |")
    lines.append("|---|---|---|---|")
    h = results["hypothesis_grading"]
    for name, v in h.items():
        if "predicted_range_km_s" in v:
            lines.append(f"| {name} | {v['predicted_range_km_s'][0]:.1f}-{v['predicted_range_km_s'][1]:.1f} km/s | "
                         f"{v['actual_km_s']:.2f} km/s | {'yes' if v['held'] else '**no**'} |")
        else:
            lines.append(f"| {name} | {v['predicted']} | "
                         f"round-trip {v.get('actual_round_trip_yr', 'N/A')} yr, "
                         f"delivered {v.get('actual_delivered_t', 'N/A')} t, "
                         f"closes soft {v.get('actual_closes_soft', 'N/A')} | "
                         f"{'yes' if v['held'] else '**no**'} |")

    (out_dir / "tables.md").write_text("\n".join(lines))
    return results


if __name__ == "__main__":
    out = main()
    print("R-variant-B-impulsive-vs-continuous complete.\n")
    print("Inbound DV per architecture variant (high-elliptical Saturn departure, LGA):")
    for vname, v in out["inbound_dv_per_variant"].items():
        print(f"  {vname:30s}: electric DV = {v['electric_dv_km_s']:6.2f} km/s "
              f"(impulsive {v['impulsive_egress_dv_km_s']:.2f}; ratio to matrix 6.42 = "
              f"{v['ratio_to_matrix']:.2f}x)")
    print()
    print("Variant B closure at 500 kWe under each variant:")
    for vname, rows in out["closures_per_variant"].items():
        r = rows[0]  # 500 kWe
        if not r.get("feasible"):
            print(f"  {vname:30s}: INFEASIBLE — {r.get('reason', '?')}")
            continue
        print(f"  {vname:30s}: round-trip {r['round_trip_yr']:5.2f} yr, "
              f"delivered {r['delivered_t']:6.1f} t (frac {r['delivered_fraction']:.3f}), "
              f"closes_soft={r['closes_soft_16yr']}")
    print()
    print("Hypothesis grading:")
    for k, v in out["hypothesis_grading"].items():
        print(f"  {k}: {'HELD' if v['held'] else 'FALSIFIED'}")
