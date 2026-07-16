#!/usr/bin/env python3
"""R-no-atmospheric-capture-baseline.

With Earth aerocapture entirely removed (no chunk-as-heat-shield, no drag
skirt, no aerobraking), is ANY combination of (chemical-kick + electric-
inbound + Saturn power class + chunk size + transfer time) a surviving cell?

Pre-registration in STUDY.md. Anchored on PRIMARY texts of titan, rhea,
R-chunk-as-heat-shield, and Round F — not on SCOPE summaries — per recurring
lesson #N updated reading.

Deterministic. Sub-second wall clock. No randomness.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants and anchor numbers (from primary texts)
# ---------------------------------------------------------------------------

G_EARTH_M_S2 = 9.80665
EARTH_RADIUS_KM = 6378.137
EARTH_MU_KM3_S2 = 398600.4418
EARTH_V_ESCAPE_INTERFACE_KM_S = math.sqrt(2.0 * EARTH_MU_KM3_S2 / (EARTH_RADIUS_KM + 125.0))  # ~11.07
EARTH_V_CIRCULAR_LEO_KM_S = math.sqrt(EARTH_MU_KM3_S2 / (EARTH_RADIUS_KM + 400.0))  # ~7.67
EARTH_V_ORBIT_KM_S = 29.7846918

ISP_HYDROLOX_S = 450.0
ISP_ELECTRIC_S = 2000.0
ISP_HYDROLOX_M_S = ISP_HYDROLOX_S * G_EARTH_M_S2  # exhaust velocity
ISP_ELECTRIC_M_S = ISP_ELECTRIC_S * G_EARTH_M_S2

# Saturn-egress (matrix-standing values)
SATURN_EGRESS_ELECTRIC_DV_KM_S = 6.16  # high-elliptical departure (Round F config)
SATURN_OPS_DURATION_YR = 1.0

# Outbound chemical kick (matrix realistic, Round F config)
OUTBOUND_CHEM_KICK_DV_KM_S = 5.0  # realistic (vs 9 conservative)

# L0-05 ceilings
L0_05_STRICT_15YR = 15.0
L0_05_SOFT_17YR = 17.0

LGA_CREDIT_KM_S = 2.0

# Round F transfer table (cruise time and perihelion velocity at Earth)
TRANSFERS = {
    9.58: {"v_peri_km_s": 40.082, "cruise_yr": 6.086},
    10.50: {"v_peri_km_s": 40.249, "cruise_yr": 4.436},
    11.0: {"v_peri_km_s": 40.329, "cruise_yr": 4.183},
    12.0: {"v_peri_km_s": 40.469, "cruise_yr": 3.864},
}

# Saturn-departure heliocentric Δv at each transfer (Round F values)
TRANSFERS_DV_OUT = {
    9.58: 10.298,
    10.50: 10.464,
    11.0: 10.544,
    12.0: 10.685,
}

# Tug dry mass scaling (rhea MARVL baseline at 500 kWe extended)
def tug_dry_mass_t(reactor_kwe: float) -> float:
    """Linear in reactor kWe per MARVL bundled approximation."""
    return 5.0 + reactor_kwe * 0.117  # 5 t fixed + 117 kg / kWe to hit 63.8 t at 500 kWe


def tsiolkovsky_propellant_t(payload_t: float, dv_km_s: float, isp_s: float) -> float:
    """Returns propellant mass needed for a stage to deliver payload_t at given Δv."""
    exhaust_m_s = isp_s * G_EARTH_M_S2
    mass_ratio = math.exp(dv_km_s * 1000.0 / exhaust_m_s)
    return payload_t * (mass_ratio - 1.0)


def chemical_capture_dv_km_s(v_inf_km_s: float) -> float:
    """Δv for impulsive chemical capture at Earth periapsis from hyperbolic v_∞."""
    v_periapsis_hyperbolic = math.sqrt(v_inf_km_s ** 2 + EARTH_V_ESCAPE_INTERFACE_KM_S ** 2)
    return v_periapsis_hyperbolic - EARTH_V_CIRCULAR_LEO_KM_S


def electric_capture_dv_km_s(v_inf_km_s: float) -> float:
    """Continuous-thrust electric Earth-arrival Δv per titan decomposition.

    Heliocentric decelerate v_inf + LEO Edelbaum spiral v_escape.
    """
    return v_inf_km_s + EARTH_V_ESCAPE_INTERFACE_KM_S


def round_trip_time_yr(cruise_yr_one_leg: float, electric_inbound_burn_yr: float) -> float:
    """2 × cruise + Saturn ops + inbound burn time."""
    return 2.0 * cruise_yr_one_leg + SATURN_OPS_DURATION_YR + electric_inbound_burn_yr


def electric_inbound_burn_time_yr(prop_mass_t: float, reactor_kwe: float, isp_s: float) -> float:
    """Mass-flow rate from reactor power and Isp.

    P_jet = (1/2) × m_dot × v_e^2 → m_dot = 2 × P_jet / v_e^2
    Assume P_jet = 0.65 × P_electric (efficiency).
    """
    p_jet_w = 0.65 * reactor_kwe * 1000.0
    v_e = isp_s * G_EARTH_M_S2
    m_dot_kg_s = 2.0 * p_jet_w / (v_e ** 2)
    burn_time_s = (prop_mass_t * 1000.0) / m_dot_kg_s
    return burn_time_s / (365.25 * 86400.0)


# ---------------------------------------------------------------------------
# Per-cell closure check
# ---------------------------------------------------------------------------

def check_cell(
    r_apo_au: float,
    reactor_kwe: float,
    chunk_t: float,
    earth_arrival: str,  # "chemical" or "electric"
    saturn_egress: str,  # "chemical_kick" (Variant B-style) or "electric_only" (Variant A)
    use_lga: bool,
) -> dict:
    """Compute mass and time closure for a single (sweep) tuple."""
    transfer = TRANSFERS[r_apo_au]
    cruise_yr = transfer["cruise_yr"]
    v_peri = transfer["v_peri_km_s"]
    dv_helio_out = TRANSFERS_DV_OUT[r_apo_au]
    lga_credit = LGA_CREDIT_KM_S if use_lga else 0.0

    v_inf = max(0.1, v_peri - EARTH_V_ORBIT_KM_S - lga_credit)

    # Earth-arrival propellant needed for entry-mass = chunk + tug
    tug_mass_t = tug_dry_mass_t(reactor_kwe)
    entry_mass_t = chunk_t + tug_mass_t

    if earth_arrival == "chemical":
        dv_arrival = chemical_capture_dv_km_s(v_inf)
        prop_arrival = tsiolkovsky_propellant_t(entry_mass_t, dv_arrival, ISP_HYDROLOX_S)
        arrival_isp = ISP_HYDROLOX_S
    else:
        dv_arrival = electric_capture_dv_km_s(v_inf)
        prop_arrival = tsiolkovsky_propellant_t(entry_mass_t, dv_arrival, ISP_ELECTRIC_S)
        arrival_isp = ISP_ELECTRIC_S

    # Mass at start of inbound electric burn = entry_mass + arrival_propellant
    mass_at_inbound_start_t = entry_mass_t + prop_arrival

    # Inbound electric burn (Saturn-egress 6.16 km/s, Isp 2000 s) — chunk-fed
    if saturn_egress == "chemical_kick":
        # Saturn-egress from chemical kick alleviates the electric inbound by 2.09 km/s
        # per Round D matrix-impulsive-vs-continuous convention.
        dv_inbound_electric = SATURN_EGRESS_ELECTRIC_DV_KM_S - 2.09  # = 4.07 km/s
        # Plus chemical kick propellant (impulsive at Saturn)
        chemical_kick_dv = 2.09
    else:
        dv_inbound_electric = SATURN_EGRESS_ELECTRIC_DV_KM_S
        chemical_kick_dv = 0.0

    prop_inbound_electric = tsiolkovsky_propellant_t(
        mass_at_inbound_start_t, dv_inbound_electric, ISP_ELECTRIC_S
    )

    # Mass at start of chemical kick (or after) = inbound_electric_start + electric_prop
    mass_after_chemkick_t = mass_at_inbound_start_t + prop_inbound_electric
    if saturn_egress == "chemical_kick":
        prop_chemkick = tsiolkovsky_propellant_t(mass_after_chemkick_t, chemical_kick_dv, ISP_HYDROLOX_S)
    else:
        prop_chemkick = 0.0

    # Mass at Saturn departure
    mass_at_saturn_arrival_t = mass_after_chemkick_t + prop_chemkick

    # Outbound chemical kick to depart Earth → Saturn
    prop_outbound_kick = tsiolkovsky_propellant_t(
        mass_at_saturn_arrival_t, dv_helio_out, ISP_HYDROLOX_S
    )

    # Mission-1 LEO launch mass
    mass_leo_launch_t = mass_at_saturn_arrival_t + prop_outbound_kick

    # Inbound burn time (only relevant for electric arrival branch)
    if earth_arrival == "electric":
        inbound_burn_yr = electric_inbound_burn_time_yr(
            prop_inbound_electric + prop_arrival, reactor_kwe, ISP_ELECTRIC_S
        )
    else:
        inbound_burn_yr = electric_inbound_burn_time_yr(
            prop_inbound_electric, reactor_kwe, ISP_ELECTRIC_S
        )

    rt_yr = round_trip_time_yr(cruise_yr, inbound_burn_yr)

    # Delivered mass = chunk available − chunk consumed by burns
    # Approximation: assume electric inbound is chunk-fed (consumes chunk water);
    # other propellant lines are Earth-sourced (carried as separate propellant).
    chunk_consumed_t = min(chunk_t, prop_inbound_electric)
    delivered_t = chunk_t - chunk_consumed_t

    closes_strict = rt_yr <= L0_05_STRICT_15YR and delivered_t > 0
    closes_soft = rt_yr <= L0_05_SOFT_17YR and delivered_t > 0

    return {
        "r_apo_au": r_apo_au,
        "reactor_kwe": reactor_kwe,
        "chunk_t": chunk_t,
        "earth_arrival": earth_arrival,
        "saturn_egress": saturn_egress,
        "use_lga": use_lga,
        "v_inf_km_s": v_inf,
        "dv_arrival_km_s": dv_arrival,
        "arrival_isp_s": arrival_isp,
        "tug_mass_t": tug_mass_t,
        "entry_mass_t": entry_mass_t,
        "prop_arrival_t": prop_arrival,
        "mass_at_inbound_start_t": mass_at_inbound_start_t,
        "prop_inbound_electric_t": prop_inbound_electric,
        "prop_chemkick_t": prop_chemkick,
        "mass_at_saturn_arrival_t": mass_at_saturn_arrival_t,
        "prop_outbound_kick_t": prop_outbound_kick,
        "mass_leo_launch_t": mass_leo_launch_t,
        "inbound_burn_yr": inbound_burn_yr,
        "round_trip_yr": rt_yr,
        "delivered_t": delivered_t,
        "delivered_fraction": delivered_t / chunk_t if chunk_t > 0 else 0.0,
        "closes_strict_15yr": closes_strict,
        "closes_soft_17yr": closes_soft,
    }


# ---------------------------------------------------------------------------
# Sweep
# ---------------------------------------------------------------------------

def run() -> dict:
    out: dict = {"config": {
        "lga_credit_km_s": LGA_CREDIT_KM_S,
        "isp_hydrolox_s": ISP_HYDROLOX_S,
        "isp_electric_s": ISP_ELECTRIC_S,
        "saturn_egress_electric_dv_km_s": SATURN_EGRESS_ELECTRIC_DV_KM_S,
        "saturn_ops_duration_yr": SATURN_OPS_DURATION_YR,
        "outbound_chem_kick_dv_km_s": OUTBOUND_CHEM_KICK_DV_KM_S,
        "L0_05_strict_15yr": L0_05_STRICT_15YR,
        "L0_05_soft_17yr": L0_05_SOFT_17YR,
        "earth_v_escape_interface_km_s": EARTH_V_ESCAPE_INTERFACE_KM_S,
        "earth_v_circular_leo_km_s": EARTH_V_CIRCULAR_LEO_KM_S,
    }}

    transfers = list(TRANSFERS.keys())
    powers = [500.0, 1000.0, 2000.0]
    chunks = [100.0, 200.0, 350.0]
    arrivals = ["chemical", "electric"]
    egresses = ["chemical_kick", "electric_only"]
    lgas = [True, False]

    cells = []
    for r_apo in transfers:
        for power in powers:
            for chunk in chunks:
                for arrival in arrivals:
                    for egress in egresses:
                        for lga in lgas:
                            cell = check_cell(r_apo, power, chunk, arrival, egress, lga)
                            cells.append(cell)
    out["cells"] = cells

    # Closure summary
    total = len(cells)
    closes_strict = [c for c in cells if c["closes_strict_15yr"]]
    closes_soft = [c for c in cells if c["closes_soft_17yr"]]
    out["closure_summary"] = {
        "total_cells_swept": total,
        "n_close_strict_15yr": len(closes_strict),
        "n_close_soft_17yr": len(closes_soft),
        "strict_closing_cells": closes_strict[:10],
        "soft_closing_cells": closes_soft[:10],
    }

    # Anchor verification — Round F equivalent (aphelion 11, 500 kWe, 200 chunk,
    # chemical Saturn-egress, electric Earth-arrival, no LGA)
    rf_anchor = next(
        c for c in cells
        if c["r_apo_au"] == 11.0
        and c["reactor_kwe"] == 500.0
        and c["chunk_t"] == 200.0
        and c["earth_arrival"] == "electric"
        and c["saturn_egress"] == "chemical_kick"
        and not c["use_lga"]
    )

    # Anchor verification — chemical Earth-arrival at Round F closing case
    chem_anchor = next(
        c for c in cells
        if c["r_apo_au"] == 11.0
        and c["reactor_kwe"] == 500.0
        and c["chunk_t"] == 200.0
        and c["earth_arrival"] == "chemical"
        and c["saturn_egress"] == "chemical_kick"
        and not c["use_lga"]
    )

    out["anchors"] = {
        "round_f_equivalent_electric_arrival_no_lga": rf_anchor,
        "chemical_arrival_no_lga": chem_anchor,
    }

    # Hypothesis grading
    chem_prop = chem_anchor["prop_arrival_t"]
    saturn_dep_mass = chem_anchor["mass_at_saturn_arrival_t"]
    chunk_frac_of_dep = 200.0 / saturn_dep_mass * 100.0
    elec_mass_ratio = math.exp(rf_anchor["dv_arrival_km_s"] * 1000.0 / ISP_ELECTRIC_M_S)
    chunk_remaining = 200.0 / elec_mass_ratio

    grading = {}
    grading["H_nacb_a"] = {
        "central": 1219.0,
        "range": [1000.0, 1500.0],
        "computed": chem_prop,
        "held": 1000.0 <= chem_prop <= 1500.0,
    }
    grading["H_nacb_b"] = {
        "central": 2025.0,
        "range": [1700.0, 2400.0],
        "computed": saturn_dep_mass,
        "held": 1700.0 <= saturn_dep_mass <= 2400.0,
    }
    grading["H_nacb_c"] = {
        "central": 9.9,
        "range": [7.0, 13.0],
        "computed": chunk_frac_of_dep,
        "held": 7.0 <= chunk_frac_of_dep <= 13.0,
    }
    grading["H_nacb_d"] = {
        "central": 3.50,
        "range": [3.0, 4.2],
        "computed": elec_mass_ratio,
        "held": 3.0 <= elec_mass_ratio <= 4.2,
    }
    grading["H_nacb_e"] = {
        "central": 57.0,
        "range": [45.0, 80.0],
        "computed": chunk_remaining,
        "held": 45.0 <= chunk_remaining <= 80.0,
    }
    grading["H_nacb_f"] = {
        "central": 0,
        "range": [0, 2],
        "computed": len(closes_strict),
        "held": 0 <= len(closes_strict) <= 2,
    }
    grading["H_nacb_g"] = {
        "central": 0,
        "range": [0, 4],
        "computed": len(closes_soft),
        "held": 0 <= len(closes_soft) <= 4,
    }
    held_count = sum(1 for v in grading.values() if v["held"])
    grading["aggregate"] = {
        "held_count": held_count,
        "total": len(grading) - 0,
        "h_nacb_agg_held": held_count >= 5 and len(closes_strict) == 0,
    }
    out["hypothesis_grading"] = grading

    return out


def write_tables(result: dict, outdir: Path) -> None:
    lines = ["# R-no-atmospheric-capture-baseline — results", ""]

    cs = result["closure_summary"]
    lines.append("## Closure summary across full sweep")
    lines.append("")
    lines.append(f"- Total cells swept: {cs['total_cells_swept']}")
    lines.append(f"- Cells closing L0-05 strict 15 yr (round-trip ≤ 15 yr AND delivered > 0): **{cs['n_close_strict_15yr']}**")
    lines.append(f"- Cells closing L0-05 soft-margin 17 yr: **{cs['n_close_soft_17yr']}**")
    lines.append("")

    if cs["n_close_strict_15yr"] > 0:
        lines.append("### Strict-closing cells (top 10)")
        lines.append("")
        lines.append("| r_apo (AU) | kWe | chunk (t) | arrival | egress | LGA | RT (yr) | delivered (t) |")
        lines.append("|---:|---:|---:|---|---|---|---:|---:|")
        for c in cs["strict_closing_cells"]:
            lines.append(
                f"| {c['r_apo_au']} | {c['reactor_kwe']:.0f} | {c['chunk_t']:.0f} | "
                f"{c['earth_arrival']} | {c['saturn_egress']} | {c['use_lga']} | "
                f"{c['round_trip_yr']:.2f} | {c['delivered_t']:.2f} |"
            )
        lines.append("")
    else:
        lines.append("**No strict-closing cells in the full sweep. The matrix's surviving cell, with aerocapture removed, is EMPTY.**")
        lines.append("")

    if cs["n_close_soft_17yr"] > 0 and cs["n_close_strict_15yr"] != cs["n_close_soft_17yr"]:
        lines.append("### Additional soft-margin-only closing cells")
        lines.append("")
        lines.append("| r_apo (AU) | kWe | chunk (t) | arrival | egress | LGA | RT (yr) | delivered (t) |")
        lines.append("|---:|---:|---:|---|---|---|---:|---:|")
        added = 0
        for c in cs["soft_closing_cells"]:
            if not c["closes_strict_15yr"]:
                lines.append(
                    f"| {c['r_apo_au']} | {c['reactor_kwe']:.0f} | {c['chunk_t']:.0f} | "
                    f"{c['earth_arrival']} | {c['saturn_egress']} | {c['use_lga']} | "
                    f"{c['round_trip_yr']:.2f} | {c['delivered_t']:.2f} |"
                )
                added += 1
                if added >= 5:
                    break
        lines.append("")

    lines.append("## Round F equivalent anchor (aphelion 11, 500 kWe, 200 t chunk, chemical Saturn-egress + electric Earth-arrival, no LGA)")
    lines.append("")
    rfa = result["anchors"]["round_f_equivalent_electric_arrival_no_lga"]
    chem_a = result["anchors"]["chemical_arrival_no_lga"]
    lines.append("| Quantity | Electric Earth-arrival | Chemical Earth-arrival |")
    lines.append("|---|---:|---:|")
    lines.append(f"| Δv arrival (km/s) | {rfa['dv_arrival_km_s']:.2f} | {chem_a['dv_arrival_km_s']:.2f} |")
    lines.append(f"| Arrival propellant (t) | {rfa['prop_arrival_t']:.0f} | {chem_a['prop_arrival_t']:.0f} |")
    lines.append(f"| Mass at inbound burn start (t) | {rfa['mass_at_inbound_start_t']:.0f} | {chem_a['mass_at_inbound_start_t']:.0f} |")
    lines.append(f"| Saturn-departure mass (t) | {rfa['mass_at_saturn_arrival_t']:.0f} | {chem_a['mass_at_saturn_arrival_t']:.0f} |")
    lines.append(f"| Outbound kick prop (t) | {rfa['prop_outbound_kick_t']:.0f} | {chem_a['prop_outbound_kick_t']:.0f} |")
    lines.append(f"| LEO mission-1 launch mass (t) | {rfa['mass_leo_launch_t']:.0f} | {chem_a['mass_leo_launch_t']:.0f} |")
    lines.append(f"| Inbound electric burn (yr) | {rfa['inbound_burn_yr']:.2f} | {chem_a['inbound_burn_yr']:.2f} |")
    lines.append(f"| Round-trip time (yr) | {rfa['round_trip_yr']:.2f} | {chem_a['round_trip_yr']:.2f} |")
    lines.append(f"| Delivered mass (t) | {rfa['delivered_t']:.2f} | {chem_a['delivered_t']:.2f} |")
    lines.append(f"| Closes strict 15 yr | {rfa['closes_strict_15yr']} | {chem_a['closes_strict_15yr']} |")
    lines.append(f"| Closes soft 17 yr | {rfa['closes_soft_17yr']} | {chem_a['closes_soft_17yr']} |")
    lines.append("")

    lines.append("## Hypothesis grading")
    lines.append("")
    lines.append("| Sub-claim | Central | Range | Computed | Held |")
    lines.append("|---|---:|---|---:|:---:|")
    for k, v in result["hypothesis_grading"].items():
        if k == "aggregate":
            continue
        lines.append(f"| {k} | {v['central']} | {v['range']} | {v['computed']:.3f} | {v['held']} |")
    agg = result["hypothesis_grading"]["aggregate"]
    lines.append("")
    lines.append(f"**Aggregate: {agg['held_count']}/{agg['total']-1} sub-claims held. H-nacb-agg held: {agg['h_nacb_agg_held']}.**")

    (outdir / "tables.md").write_text("\n".join(lines))


def main() -> None:
    here = Path(__file__).resolve().parent
    outdir = here / "results"
    outdir.mkdir(parents=True, exist_ok=True)
    result = run()
    (outdir / "R_no_atmospheric_capture_baseline.json").write_text(
        json.dumps(result, indent=2, default=float)
    )
    write_tables(result, outdir)
    cs = result["closure_summary"]
    rfa = result["anchors"]["round_f_equivalent_electric_arrival_no_lga"]
    chem_a = result["anchors"]["chemical_arrival_no_lga"]
    print(f"Total cells swept: {cs['total_cells_swept']}")
    print(f"Closing strict 15-yr: {cs['n_close_strict_15yr']}")
    print(f"Closing soft 17-yr: {cs['n_close_soft_17yr']}")
    print(f"Round F electric arrival: RT={rfa['round_trip_yr']:.2f} yr, delivered={rfa['delivered_t']:.2f} t, strict={rfa['closes_strict_15yr']}")
    print(f"Round F chemical arrival: prop={chem_a['prop_arrival_t']:.0f} t, LEO mass={chem_a['mass_leo_launch_t']:.0f} t, delivered={chem_a['delivered_t']:.2f} t")
    grading = result["hypothesis_grading"]
    agg = grading["aggregate"]
    print(f"Hypothesis aggregate: {agg['held_count']}/{agg['total']-1} held; H-nacb-agg: {'HELD' if agg['h_nacb_agg_held'] else 'FALSIFIED'}")


if __name__ == "__main__":
    main()
