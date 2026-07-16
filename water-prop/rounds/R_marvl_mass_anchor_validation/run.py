"""R-marvl-mass-anchor-validation — sweep three plausible MARVL-anchored mass
parameterizations (pessimistic / rhea-baseline / optimistic) and re-run Round D
Variant C closure. Tests whether the surviving cell's verdict depends on
rhea's specific picks within the locked-finding-4 ranges.

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
ROUND_TRIP_SOFT_MARGIN_YR = 1.0
ROUND_TRIP_DOUBLE_SOFT_MARGIN_YR = 2.0  # for cell-survives-pessimistic check

ISP_ELECTRIC_S = 2000.0
CHUNK_BASELINE_T = 200.0
M_FIXED_T = 5.0
F_TANK = 0.05

# Round D Variant C corrected inbound delta-velocity (high-elliptical, with LGA, aerocapture)
DV_INBOUND_VARIANT_C_KM_S = 19.90  # segments 1+2+4 minus LGA from titan's decomposition

# Outbound chemical kick (realistic 5 km/s)
DV_CHEM_OUTBOUND_KM_S = 5.0
ISP_HYDROLOX_S = 450.0
M_OUTBOUND_KICK_DRY_T = 10.0

REACTOR_POWERS_KWE = [500.0, 750.0, 1000.0]

# High-temperature deployable radiator surface conductance (locked-finding-4 framing)
RADIATOR_SURFACE_CONDUCTANCE_W_TH_PER_M2 = 700.0


def derive_alphas_from_percentages(
    pct_reactor: float, pct_pc: float, pct_radiator: float, eta_conv: float, m_fixed_t: float = M_FIXED_T,
) -> dict:
    """Given subsystem percentages of total stack mass at 1 megawatt-electric and the
    Brayton conversion efficiency, derive (alpha_reactor, alpha_pc, alpha_radiator)
    such that the decomposed mass model reproduces those percentages.

    At 1 MWe (no propellant):
      m_reactor = 1000 / alpha_reactor
      m_PC = 1000 / alpha_PC
      P_th_waste = 1000 * (1 - eta) / eta
      m_radiator = P_th_waste / alpha_radiator / 1000  (alpha_radiator in kW_th/kg)
      total = m_fixed + m_reactor + m_PC + m_radiator

    We want m_reactor / total = pct_reactor (etc). The system is implicit
    because total appears on both sides. Solve iteratively or algebraically.

    Algebra: let f_other = 1 - pct_reactor - pct_pc - pct_radiator.
    f_other × total = m_fixed → total = m_fixed / f_other.
    Then:
      m_reactor = pct_reactor × total = pct_reactor × m_fixed / f_other
      alpha_reactor = 1000 / m_reactor
      similarly for PC.
      m_radiator = pct_radiator × total
      P_th_waste = 1000 × (1 - eta) / eta
      alpha_radiator = P_th_waste / (m_radiator × 1000) = P_th_waste / m_radiator / 1000
                      [m_radiator in tonnes; alpha in kW_th/kg]
    """
    f_other = 1.0 - pct_reactor - pct_pc - pct_radiator
    if f_other <= 0:
        raise ValueError(f"percentages sum to {pct_reactor + pct_pc + pct_radiator}; need < 1")
    total_t_at_1mwe = m_fixed_t / f_other
    m_reactor = pct_reactor * total_t_at_1mwe
    m_pc = pct_pc * total_t_at_1mwe
    m_rad = pct_radiator * total_t_at_1mwe
    p_th_waste_kw = 1000.0 * (1.0 - eta_conv) / eta_conv
    alpha_reactor_w_per_kg = 1000.0 / m_reactor  # 1000 kW / mass-in-tonnes-times-1000 = W/kg
    alpha_pc_w_per_kg = 1000.0 / m_pc
    alpha_rad_kw_th_per_kg = p_th_waste_kw / (m_rad * 1000.0)
    return {
        "pct_reactor": pct_reactor,
        "pct_pc": pct_pc,
        "pct_radiator": pct_radiator,
        "eta_conv": eta_conv,
        "m_fixed_t": m_fixed_t,
        "total_t_at_1mwe": total_t_at_1mwe,
        "alpha_reactor_W_per_kg": alpha_reactor_w_per_kg,
        "alpha_PC_W_per_kg": alpha_pc_w_per_kg,
        "alpha_radiator_kW_th_per_kg": alpha_rad_kw_th_per_kg,
        "f_tank": F_TANK,
    }


# Parameterizations chosen to span the locked-finding-4 ranges while keeping
# percentages summing < 1 (m_fixed claims the remainder). The total stack mass
# at 1 megawatt-electric falls out of m_fixed / (1 - sum of subsystem fractions).
#
# Pessimistic: 31% / 21% / 45% / eta 0.27 (high reactor, mid-high PC, high radiator,
#              low conversion efficiency). Sum = 97%; m_fixed = 3% → total ~167 t.
# Optimistic:  28% / 18% / 46% / eta 0.32 (low-mid reactor, low-mid PC, mid radiator,
#              high conversion efficiency). Sum = 92%; m_fixed = 8% → total ~63 t.
# Both stay inside locked-finding-4 ranges (reactor 25-35%, PC 15-25%, radiator 40-55%).
PARAM_PESSIMISTIC = derive_alphas_from_percentages(0.31, 0.21, 0.45, 0.27)
PARAM_RHEA_BASELINE = {
    "m_fixed_t": M_FIXED_T,
    "alpha_reactor_W_per_kg": 33.0,
    "alpha_PC_W_per_kg": 50.0,
    "alpha_radiator_kW_th_per_kg": 0.047,
    "eta_conv": 0.30,
    "f_tank": F_TANK,
    "_label": "rhea_baseline",
}
PARAM_OPTIMISTIC = derive_alphas_from_percentages(0.28, 0.18, 0.46, 0.32)


def dry_mass_t(params: dict, reactor_kwe: float, m_prop_t: float = 0.0) -> float:
    eta = params["eta_conv"]
    p_th_waste_kw = reactor_kwe * (1.0 - eta) / eta
    m_reactor = reactor_kwe / params["alpha_reactor_W_per_kg"]
    m_pc = reactor_kwe / params["alpha_PC_W_per_kg"]
    m_rad = p_th_waste_kw / params["alpha_radiator_kW_th_per_kg"] / 1000.0
    m_tank = m_prop_t * params["f_tank"]
    return params["m_fixed_t"] + m_reactor + m_pc + m_rad + m_tank


def mass_breakdown(params: dict, reactor_kwe: float, m_prop_t: float = 0.0) -> dict:
    eta = params["eta_conv"]
    p_th_waste_kw = reactor_kwe * (1.0 - eta) / eta
    m_reactor = reactor_kwe / params["alpha_reactor_W_per_kg"]
    m_pc = reactor_kwe / params["alpha_PC_W_per_kg"]
    m_rad = p_th_waste_kw / params["alpha_radiator_kW_th_per_kg"] / 1000.0
    m_tank = m_prop_t * params["f_tank"]
    total = params["m_fixed_t"] + m_reactor + m_pc + m_rad + m_tank
    return {
        "m_fixed_t": params["m_fixed_t"],
        "m_reactor_t": m_reactor,
        "m_PC_t": m_pc,
        "m_radiator_t": m_rad,
        "m_tank_t": m_tank,
        "total_t": total,
        "p_th_waste_kw": p_th_waste_kw,
        "fractions": {
            "reactor": m_reactor / total if total > 0 else 0,
            "PC": m_pc / total if total > 0 else 0,
            "radiator": m_rad / total if total > 0 else 0,
        },
    }


def hohmann_cruise_yr() -> float:
    a_h_km = (A_EARTH + A_SATURN) / 2.0
    return math.pi * math.sqrt(a_h_km ** 3 / GM_SUN) / YEAR_S


def variant_C_closure(params: dict, reactor_kwe: float) -> dict:
    """Variant C closure: chemical-kick outbound + electric heliocentric inbound + Earth aerocapture."""
    m_tug_t = dry_mass_t(params, reactor_kwe, m_prop_t=0.0)

    # Iterate on tug mass for inbound tank fraction
    for _ in range(20):
        v_e_elec = ISP_ELECTRIC_S * G0
        m_initial_inbound_t = m_tug_t + CHUNK_BASELINE_T
        mr_inbound = math.exp(DV_INBOUND_VARIANT_C_KM_S * 1000.0 / v_e_elec)
        m_prop_inbound_t = m_initial_inbound_t * (1.0 - 1.0 / mr_inbound)
        if m_prop_inbound_t > CHUNK_BASELINE_T:
            return {
                "feasible": False,
                "reason": f"electric inbound burn requires {m_prop_inbound_t:.1f} t but chunk has {CHUNK_BASELINE_T} t",
                "reactor_kwe": reactor_kwe,
                "m_tug_t": m_tug_t,
                "round_trip_yr": math.inf,
                "delivered_t": -math.inf,
            }
        new_tug = dry_mass_t(params, reactor_kwe, m_prop_t=m_prop_inbound_t)
        if abs(new_tug - m_tug_t) < 1e-4:
            m_tug_t = new_tug
            break
        m_tug_t = new_tug
    else:
        new_tug = dry_mass_t(params, reactor_kwe, m_prop_t=m_prop_inbound_t)
        m_tug_t = new_tug

    delivered_t = CHUNK_BASELINE_T - m_prop_inbound_t

    # Inbound burn time
    P_elec_w = reactor_kwe * 1000.0
    thrust_inbound_N = 2.0 * ETA_THR_ELECTRIC * P_elec_w / v_e_elec
    t_inbound_burn_s = m_prop_inbound_t * 1000.0 * v_e_elec / thrust_inbound_N
    t_inbound_burn_yr = t_inbound_burn_s / YEAR_S

    # Outbound chemical kick (Round C parameters, realistic 5 km/s)
    v_e_chem = ISP_HYDROLOX_S * G0
    mr_chem = math.exp(DV_CHEM_OUTBOUND_KM_S * 1000.0 / v_e_chem)
    m_at_start_kick_t = (m_tug_t + M_OUTBOUND_KICK_DRY_T) * mr_chem
    m_outbound_kick_prop_t = m_at_start_kick_t - (m_tug_t + M_OUTBOUND_KICK_DRY_T)
    m_LEO_mission1_t = m_at_start_kick_t

    cruise_yr = hohmann_cruise_yr()
    round_trip_yr = cruise_yr + SATURN_OPS_YR + t_inbound_burn_yr + cruise_yr

    closes_strict = (round_trip_yr <= ROUND_TRIP_CEILING_YR) and (delivered_t > 0)
    closes_soft1 = (round_trip_yr <= ROUND_TRIP_CEILING_YR + ROUND_TRIP_SOFT_MARGIN_YR
                    and delivered_t > 0)
    closes_soft2 = (round_trip_yr <= ROUND_TRIP_CEILING_YR + ROUND_TRIP_DOUBLE_SOFT_MARGIN_YR
                    and delivered_t > 0)

    return {
        "feasible": True,
        "reactor_kwe": reactor_kwe,
        "m_tug_t": m_tug_t,
        "m_outbound_kick_prop_t": m_outbound_kick_prop_t,
        "m_LEO_mission1_t": m_LEO_mission1_t,
        "m_prop_inbound_t": m_prop_inbound_t,
        "delivered_t": delivered_t,
        "delivered_fraction": delivered_t / CHUNK_BASELINE_T,
        "thrust_inbound_N": thrust_inbound_N,
        "mass_ratio_inbound": mr_inbound,
        "t_inbound_burn_yr": t_inbound_burn_yr,
        "round_trip_yr": round_trip_yr,
        "closes_strict_15yr": closes_strict,
        "closes_soft_16yr": closes_soft1,
        "closes_double_soft_17yr": closes_soft2,
    }


def main() -> dict:
    PARAMS = {
        "pessimistic": PARAM_PESSIMISTIC,
        "rhea_baseline": PARAM_RHEA_BASELINE,
        "optimistic": PARAM_OPTIMISTIC,
    }

    # 1. 1-megawatt-electric mass breakdowns for each parameterization
    breakdowns = {}
    for label, params in PARAMS.items():
        breakdowns[label] = mass_breakdown(params, 1000.0, m_prop_t=0.0)

    # 2. Variant C closure for each parameterization × reactor power
    closures = {}
    for label, params in PARAMS.items():
        rows = []
        for kwe in REACTOR_POWERS_KWE:
            row = variant_C_closure(params, kwe)
            row["parameterization"] = label
            rows.append(row)
        closures[label] = rows

    # 3. Radiator areal density check at 500 kilowatt-electric for each parameterization
    areal_density = {}
    for label, params in PARAMS.items():
        b = mass_breakdown(params, 500.0, m_prop_t=0.0)
        m_rad_kg = b["m_radiator_t"] * 1000.0
        p_waste_kw = b["p_th_waste_kw"]
        # Surface area = waste heat / surface conductance
        area_m2 = p_waste_kw * 1000.0 / RADIATOR_SURFACE_CONDUCTANCE_W_TH_PER_M2
        areal_kg_per_m2 = m_rad_kg / area_m2 if area_m2 > 0 else float("inf")
        areal_density[label] = {
            "m_radiator_t": b["m_radiator_t"],
            "p_th_waste_kw": p_waste_kw,
            "radiator_area_m2": area_m2,
            "implied_areal_density_kg_per_m2": areal_kg_per_m2,
            "alpha_radiator_kW_th_per_kg": params["alpha_radiator_kW_th_per_kg"],
            "eta_conv": params["eta_conv"],
        }

    # 4. Hypothesis grading
    h_mmav_a = {
        "predicted_range_t": [130.0, 160.0],
        "point_t": 145.0,
        "actual_t": breakdowns["pessimistic"]["total_t"],
        "held": 130.0 <= breakdowns["pessimistic"]["total_t"] <= 160.0,
    }
    h_mmav_b = {
        "predicted_range_t": [70.0, 95.0],
        "point_t": 80.0,
        "actual_t": breakdowns["optimistic"]["total_t"],
        "held": 70.0 <= breakdowns["optimistic"]["total_t"] <= 95.0,
    }
    pess_500 = closures["pessimistic"][0]
    h_mmav_c = {
        "predicted": "closes ±2 yr soft margin with delivered 10-30 t, round-trip 16.5-17.0 yr",
        "actual_round_trip_yr": pess_500.get("round_trip_yr", math.inf),
        "actual_delivered_t": pess_500.get("delivered_t", -math.inf),
        "actual_closes_double_soft": pess_500.get("closes_double_soft_17yr", False),
        "held": (pess_500.get("closes_double_soft_17yr", False)
                 and 10.0 <= pess_500.get("delivered_t", -1) <= 30.0
                 and 16.5 <= pess_500.get("round_trip_yr", math.inf) <= 17.0),
    }
    opt_500 = closures["optimistic"][0]
    h_mmav_d = {
        "predicted": "closes with delivered 40-55 t, round-trip 16.0-16.3 yr",
        "actual_round_trip_yr": opt_500.get("round_trip_yr", math.inf),
        "actual_delivered_t": opt_500.get("delivered_t", -math.inf),
        "actual_closes_soft": opt_500.get("closes_soft_16yr", False),
        "held": (40.0 <= opt_500.get("delivered_t", -1) <= 55.0
                 and 16.0 <= opt_500.get("round_trip_yr", math.inf) <= 16.3),
    }
    rhea_areal = areal_density["rhea_baseline"]["implied_areal_density_kg_per_m2"]
    h_mmav_e = {
        "predicted_range_kg_per_m2": [2.5, 3.5],
        "point_kg_per_m2": 3.0,
        "actual_kg_per_m2": rhea_areal,
        "held": 2.5 <= rhea_areal <= 3.5,
    }

    results = {
        "config": {
            "isp_electric_s": ISP_ELECTRIC_S,
            "chunk_t": CHUNK_BASELINE_T,
            "dv_inbound_km_s": DV_INBOUND_VARIANT_C_KM_S,
            "dv_chem_outbound_km_s": DV_CHEM_OUTBOUND_KM_S,
            "radiator_surface_conductance_W_th_per_m2": RADIATOR_SURFACE_CONDUCTANCE_W_TH_PER_M2,
        },
        "parameterizations": {
            label: {k: v for k, v in p.items() if k != "_label"}
            for label, p in PARAMS.items()
        },
        "mass_breakdowns_at_1mwe": breakdowns,
        "variant_C_closures": closures,
        "radiator_areal_density_at_500kwe": areal_density,
        "hypothesis_grading": {
            "H-mmav-a_pessimistic_1mwe_mass": h_mmav_a,
            "H-mmav-b_optimistic_1mwe_mass": h_mmav_b,
            "H-mmav-c_pessimistic_500kwe_closure": h_mmav_c,
            "H-mmav-d_optimistic_500kwe_closure": h_mmav_d,
            "H-mmav-e_rhea_areal_density": h_mmav_e,
        },
    }
    out_dir = Path(__file__).parent / "results"
    out_dir.mkdir(exist_ok=True)
    (out_dir / "R_marvl_mass_anchor_validation.json").write_text(
        json.dumps(results, indent=2, default=str)
    )

    # Tables
    lines = []
    lines.append("### Three MARVL parameterizations and their mass breakdowns at 1 megawatt-electric (no propellant)\n")
    lines.append("| Parameterization | alpha_reactor (W/kg) | alpha_PC (W/kg) | alpha_radiator (kW_th/kg) | eta_conv | m_reactor (t) | m_PC (t) | m_radiator (t) | Total (t) | Reactor% | PC% | Radiator% |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for label in ("pessimistic", "rhea_baseline", "optimistic"):
        p = PARAMS[label]
        b = breakdowns[label]
        lines.append(
            f"| {label} | {p['alpha_reactor_W_per_kg']:.1f} | "
            f"{p['alpha_PC_W_per_kg']:.1f} | {p['alpha_radiator_kW_th_per_kg']:.4f} | "
            f"{p['eta_conv']:.2f} | {b['m_reactor_t']:.1f} | {b['m_PC_t']:.1f} | "
            f"{b['m_radiator_t']:.1f} | {b['total_t']:.1f} | "
            f"{b['fractions']['reactor']*100:.1f}% | {b['fractions']['PC']*100:.1f}% | "
            f"{b['fractions']['radiator']*100:.1f}% |"
        )
    lines.append("")

    lines.append("### Variant C (Earth aerocapture, no Saturn-egress kick) closure under each parameterization\n")
    for label in ("pessimistic", "rhea_baseline", "optimistic"):
        lines.append(f"#### {label}\n")
        lines.append("| Reactor (kWe) | Tug (t) | Inbound prop (t) | Delivered (t) | Fraction | t_inbound (yr) | Round-trip (yr) | Closes ±1 yr (16)? | Closes ±2 yr (17)? |")
        lines.append("|---:|---:|---:|---:|---:|---:|---:|:--:|:--:|")
        for r in closures[label]:
            if not r.get("feasible"):
                lines.append(f"| {r['reactor_kwe']:.0f} | INFEASIBLE: {r.get('reason', '?')} |")
                continue
            f1 = "**yes**" if r["closes_soft_16yr"] else "no"
            f2 = "**yes**" if r["closes_double_soft_17yr"] else "no"
            lines.append(
                f"| {r['reactor_kwe']:.0f} | {r['m_tug_t']:.1f} | "
                f"{r['m_prop_inbound_t']:.1f} | {r['delivered_t']:.1f} | "
                f"{r['delivered_fraction']:.3f} | {r['t_inbound_burn_yr']:.2f} | "
                f"{r['round_trip_yr']:.2f} | {f1} | {f2} |"
            )
        lines.append("")

    lines.append(f"### Implied radiator areal density at 500 kilowatt-electric (surface conductance {RADIATOR_SURFACE_CONDUCTANCE_W_TH_PER_M2:.0f} W_th/m²)\n")
    lines.append("Standard high-temperature deployable radiator areal density is ~3 kg/m². Sub-1 kg/m² is physically infeasible under known materials.\n")
    lines.append("| Parameterization | Radiator mass (t) | Waste heat (kW_th) | Implied area (m²) | **Areal density (kg/m²)** | Inside ~3 kg/m² standard? |")
    lines.append("|---|---:|---:|---:|---:|:--:|")
    for label in ("pessimistic", "rhea_baseline", "optimistic"):
        a = areal_density[label]
        flag = "**yes**" if a["implied_areal_density_kg_per_m2"] >= 1.5 else "**no (sub-1.5)**"
        lines.append(
            f"| {label} | {a['m_radiator_t']:.2f} | {a['p_th_waste_kw']:.0f} | "
            f"{a['radiator_area_m2']:.0f} | **{a['implied_areal_density_kg_per_m2']:.2f}** | "
            f"{flag} |"
        )
    lines.append("")

    lines.append("### Hypothesis grading\n")
    lines.append("| Sub-claim | Predicted | Measured | Held? |")
    lines.append("|---|---|---|---|")
    h = results["hypothesis_grading"]
    a = h["H-mmav-a_pessimistic_1mwe_mass"]
    lines.append(f"| H-mmav-a — pessimistic 1 MWe stack | 130-160 t (point 145) | "
                 f"{a['actual_t']:.1f} t | {'yes' if a['held'] else '**no**'} |")
    b = h["H-mmav-b_optimistic_1mwe_mass"]
    lines.append(f"| H-mmav-b — optimistic 1 MWe stack | 70-95 t (point 80) | "
                 f"{b['actual_t']:.1f} t | {'yes' if b['held'] else '**no**'} |")
    c = h["H-mmav-c_pessimistic_500kwe_closure"]
    lines.append(f"| H-mmav-c — pessimistic Variant C @ 500 kWe ±2 yr closes with 10-30 t | "
                 f"{c['predicted']} | round-trip {c['actual_round_trip_yr']:.2f} yr, "
                 f"delivered {c['actual_delivered_t']:.1f} t, closes_double_soft="
                 f"{c['actual_closes_double_soft']} | {'yes' if c['held'] else '**no**'} |")
    d = h["H-mmav-d_optimistic_500kwe_closure"]
    lines.append(f"| H-mmav-d — optimistic Variant C @ 500 kWe closes with 40-55 t | "
                 f"{d['predicted']} | round-trip {d['actual_round_trip_yr']:.2f} yr, "
                 f"delivered {d['actual_delivered_t']:.1f} t, closes_soft={d['actual_closes_soft']} | "
                 f"{'yes' if d['held'] else '**no**'} |")
    e = h["H-mmav-e_rhea_areal_density"]
    lines.append(f"| H-mmav-e — rhea-baseline areal density at 500 kWe | "
                 f"2.5-3.5 kg/m² (point 3.0) | {e['actual_kg_per_m2']:.2f} | "
                 f"{'yes' if e['held'] else '**no**'} |")

    (out_dir / "tables.md").write_text("\n".join(lines))
    return results


if __name__ == "__main__":
    out = main()
    print("R-marvl-mass-anchor-validation complete.\n")
    print("1-megawatt-electric stack mass per parameterization:")
    for label, b in out["mass_breakdowns_at_1mwe"].items():
        f = b["fractions"]
        print(f"  {label:15s}: total {b['total_t']:6.1f} t  "
              f"(reactor {f['reactor']*100:.1f}%, PC {f['PC']*100:.1f}%, "
              f"radiator {f['radiator']*100:.1f}%)")
    print()
    print("Variant C closure at 500 kWe per parameterization:")
    for label, rows in out["variant_C_closures"].items():
        r = rows[0]
        if not r.get("feasible"):
            print(f"  {label:15s}: INFEASIBLE — {r.get('reason', '?')}")
            continue
        print(f"  {label:15s}: round-trip {r['round_trip_yr']:5.2f} yr, "
              f"delivered {r['delivered_t']:6.1f} t (frac {r['delivered_fraction']:.3f}), "
              f"closes_soft_16={r['closes_soft_16yr']}, closes_double_soft_17={r['closes_double_soft_17yr']}")
    print()
    print("Radiator areal density at 500 kWe per parameterization:")
    for label, a in out["radiator_areal_density_at_500kwe"].items():
        flag = "OK" if a["implied_areal_density_kg_per_m2"] >= 1.5 else "BELOW physical floor"
        print(f"  {label:15s}: {a['implied_areal_density_kg_per_m2']:.2f} kg/m² ({flag})")
    print()
    print("Hypothesis grading:")
    for k, v in out["hypothesis_grading"].items():
        print(f"  {k}: {'HELD' if v['held'] else 'FALSIFIED'}")
