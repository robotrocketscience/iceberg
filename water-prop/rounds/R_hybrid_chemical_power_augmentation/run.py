"""R-hybrid-chemical-power-augmentation — phoebe, latest+11.

Does a small reactor plus a brought-from-Earth hydrogen-oxygen gas-generator boost
close any inbound cell that the 500-kilowatt-electric pure-reactor cell could not?

Tsiolkovsky + energy bookkeeping + mass model. 5 x 6 x 5 x 2 x 2 x 3 = 1,800 cells in
the SCOPE-as-written sweep. Inner derivation over Isp (SCOPE method discusses Isp = 3000 s
as central anchor; phoebe sweeps {2000, 3000, 4000} to bracket the Edelbaum-optimum band).

Lesson-9 audit (fifth phoebe application) added five SCOPE-input-assumption corrections
documented in STUDY.md before this script ran. Headline corrections that affect cell
classification:
  (i) chunk-as-propellant constraint: m_prop_from_chunk must be <= chunk_initial; cells
      with prop > chunk classify CHUNK-EATEN and deliver zero regardless of power.
  (ii) Saturn departure orbit: SCOPE's 25 km/s anchor corresponds to Iapetus-distance + LGA;
       audit-extension sweep adds B-ring no-LGA (40 km/s) at headline cells.
  (iii) Reactor lifetime: SCOPE quotes Kilopower 10-yr design target, but flown anchor
        (KRUSTY) is 28 hr; run reports both flags.
  (iv) Hydrolox tank-mass fraction: SCOPE 10 percent is Centaur-hours, not multi-year;
       audit-extension sweep adds 25 and 40 percent at headline cells.
  (v) Aerocapture credit conditional on R-hybrid-aerocapture-aerobraking closure (0/1920 cells);
      retained as SCOPE axis but flagged conditional in output.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


# ----- Physical constants ----------------------------------------------------
G0 = 9.81  # m/s^2
LHV_HYDROLOX = 13.4e6  # J/kg, stoichiometric mixture, lower heating value (water-vapor product)
YEAR_S = 365.25 * 86400.0

# ----- Mission anchors -------------------------------------------------------
# Inbound delta-velocity anchors from R-inbound-dv-continuous-thrust commit 58581fb.
DV_INBOUND_KM_S = {
    ("Iapetus_distance", True): 24.67,    # SCOPE-as-written anchor
    ("Iapetus_distance", False): 26.67,
    ("high_elliptical_1Mkm", True): 27.56,
    ("high_elliptical_1Mkm", False): 29.56,
    ("B_ring", True): 38.17,
    ("B_ring", False): 40.17,             # Surviving-cell architecture operating zone
}

# Mission timing pieces (R-inbound-dv-continuous-thrust, R-outbound-chemical-kick-economics)
HOHMANN_CRUISE_YR = 6.086
OUTBOUND_BURN_YR = 0.5    # Chemical kick stage to trans-Saturn injection; hyperion anchor
SATURN_OPS_YR = 1.0       # Bag fill + grapple + Saturn-side maneuvering

# Vehicle bus mass excluding reactor + power (SATURN-SHIP-SPEC.md bottom-up minus reactor+power 1.6 t).
# SATURN-SHIP-SPEC.md total dry mass 3.5 t includes a 1.6-t reactor+power+radiator at 6.25 W/kg
# (Kilopower paper-study anchor), but the flown-anchor specific power is KRUSTY's 2.4 W/kg system-level
# (locked aelfrice belief 0d5c882c13395571). Phoebe-conservatism: use KRUSTY anchor, so reactor mass
# at 10 kWe is 4.17 t (not 1.6 t). Bus = total_spec - reactor_spec = 3.5 - 1.6 = 1.9 t.
DRY_BUS_T = 1.9  # Bus (avionics, bag, harvesting, structure, propulsion thrusters, RCS, etc.); reactor counted separately.
REACTOR_SPECIFIC_W_PER_KG = 2.4  # KRUSTY flown anchor (locked aelfrice belief 0d5c882c13395571)
GENERATOR_T_PER_KWE = 0.05  # 50 kg/kWe peak generator power; Brayton turbine APU heritage
ETA_THR = 0.65              # Electric thruster efficiency (titan/rhea anchor)
CHEMICAL_KICK_STAGE_T = 150.0  # Outbound chemical kick stage at Earth orbit, hyperion anchor

# ----- SCOPE-as-written sweep axes ------------------------------------------
P_REACTOR_KWE = [1.0, 5.0, 10.0, 20.0, 50.0]
M_H2O2_T = [0.0, 100.0, 250.0, 500.0, 1000.0, 2500.0]
CHUNK_T = [5.0, 10.0, 50.0, 100.0, 200.0]
ETA_GEN = [0.30, 0.50]
AEROCAPTURE_KM_S = [0.0, 10.0]
ISP_S = [2000.0, 3000.0, 4000.0]

# ----- Audit-extension axes (phoebe-side, not in SCOPE-original) ------------
SATURN_DEPARTURE_AND_LGA = [("Iapetus_distance", True), ("B_ring", False)]
TANK_FRAC = [0.10, 0.25, 0.40]

# ----- L0-05 / lifetime thresholds ------------------------------------------
L0_05_STRICT_YR = 15.0
L0_05_WAIVER_YR = 25.0
DEMONSTRATOR_CEILING_YR = 40.0
LIFETIME_GROUND_HR = 28.0
LIFETIME_GROUND_YR = LIFETIME_GROUND_HR / (365.25 * 24.0)  # ~0.0032 yr
LIFETIME_DESIGN_YR = 10.0
LIFETIME_ASPIRATIONAL_YR = 30.0

# Launch envelope (Earth-orbit stack mass)
STARSHIP_1X_T = 150.0
STARSHIP_2X_T = 300.0


def dry_bundle_t(
    p_reactor_kwe: float,
    m_hydrolox_t: float,
    eta_gen: float,
    tank_frac: float,
) -> dict[str, float]:
    """Vehicle dry mass + power-plant + generator + tank mass at Earth-orbit injection.

    DRY_BUS_T excludes reactor+power (which scales with P_reactor at KRUSTY's flown anchor).
    Reactor sized at REACTOR_SPECIFIC_W_PER_KG = 2.4 W/kg system-level (locked aelfrice
    belief). Generator sized at average electrical-output power assuming hydrolox burns
    over a 5-yr nominal burn (sets peak gen power independent of actual burn time).
    """
    reactor_t = p_reactor_kwe * 1e3 / REACTOR_SPECIFIC_W_PER_KG / 1e3  # = p_kw / 2.4

    # Peak generator power proxy: average over a 5-yr burn at full hydrolox throughput.
    avg_gen_power_kw = (m_hydrolox_t * 1e3 * LHV_HYDROLOX * eta_gen / (5.0 * YEAR_S)) / 1e3 if m_hydrolox_t > 0 else 0.0
    generator_t = avg_gen_power_kw * GENERATOR_T_PER_KWE

    tank_t = m_hydrolox_t * tank_frac
    total_t = DRY_BUS_T + reactor_t + generator_t + tank_t
    return {
        "bus_t": DRY_BUS_T,
        "reactor_t": reactor_t,
        "generator_t": generator_t,
        "tank_t": tank_t,
        "total_t": total_t,
    }


def tsiolkovsky_from_chunk(
    chunk_t: float,
    dry_bundle_total_t: float,
    isp_s: float,
    dv_m_s: float,
) -> dict[str, float]:
    """Harvested-water Tsiolkovsky from the chunk.

    Burn starts with vehicle holding chunk (= harvested water reservoir) and dry bundle.
    Propellant is consumed from chunk during burn. If required propellant exceeds chunk,
    classify CHUNK-EATEN and report negative deliverable.
    """
    v_exh = isp_s * G0
    m_init_t = chunk_t + dry_bundle_total_t
    f_prop = 1.0 - math.exp(-dv_m_s / v_exh)
    m_prop_t = m_init_t * f_prop
    chunk_eaten = m_prop_t > chunk_t
    chunk_delivered_t = max(0.0, chunk_t - m_prop_t) if not chunk_eaten else 0.0
    # Electrical energy required: integrate kinetic energy delivered to exhaust at thruster efficiency.
    energy_req_j = m_prop_t * 1e3 * 0.5 * v_exh * v_exh / ETA_THR
    return {
        "v_exh_m_s": v_exh,
        "m_initial_t": m_init_t,
        "f_propellant": f_prop,
        "m_prop_t": m_prop_t,
        "chunk_eaten": chunk_eaten,
        "chunk_delivered_t": chunk_delivered_t,
        "electrical_energy_j": energy_req_j,
    }


def solve_burn_time_yr(
    energy_req_j: float,
    p_reactor_kwe: float,
    m_hydrolox_t: float,
    eta_gen: float,
) -> dict[str, float]:
    """Solve for burn time given reactor + hydrolox energy budget.

    Both run continuously during burn: E_req = P_reactor * t + M_H2O2 * LHV * eta_gen.
    Time-component for hydrolox is exhausted-when-fuel-out; we assume the gas generator
    runs for the same burn duration at average power M_H2O2 * LHV * eta_gen / burn_time.
    Substituting: burn_time = (E_req - E_hydrolox_total) / P_reactor, with E_hydrolox a
    one-time energy contribution. If E_hydrolox >= E_req, burn closes on gas-gen alone
    at gas-gen-peak-power runtime (reactor not strictly required, but we keep it on
    for housekeeping).
    """
    e_hydrolox_j = m_hydrolox_t * 1e3 * LHV_HYDROLOX * eta_gen
    if p_reactor_kwe <= 0:
        # Reactor-zero degenerate case: shouldn't happen with sweep, but handle.
        if e_hydrolox_j <= 0:
            return {"e_hydrolox_j": 0.0, "e_reactor_at_burn_j": 0.0, "burn_time_yr": math.inf, "feasible": False}
        # Gas-gen-only at fixed 1-yr arbitrary peak; not realistic, just for grid completeness.
        return {"e_hydrolox_j": e_hydrolox_j, "e_reactor_at_burn_j": 0.0, "burn_time_yr": 1.0, "feasible": e_hydrolox_j >= energy_req_j}
    e_gap_j = energy_req_j - e_hydrolox_j
    if e_gap_j <= 0:
        # Hydrolox over-budgeted: gas generator alone (plus housekeeping reactor) closes.
        # Burn time set by gas-generator pace; assume average gen power = avg_gen_power_kw from dry-bundle sizing.
        # For closure check we just confirm energy is sufficient; burn_time recipe is loose here.
        burn_time_yr = energy_req_j / (p_reactor_kwe * 1e3 + e_hydrolox_j / (5.0 * YEAR_S)) / YEAR_S
        return {
            "e_hydrolox_j": e_hydrolox_j,
            "e_reactor_at_burn_j": p_reactor_kwe * 1e3 * burn_time_yr * YEAR_S,
            "burn_time_yr": burn_time_yr,
            "feasible": True,
        }
    burn_time_s = e_gap_j / (p_reactor_kwe * 1e3)
    burn_time_yr = burn_time_s / YEAR_S
    return {
        "e_hydrolox_j": e_hydrolox_j,
        "e_reactor_at_burn_j": p_reactor_kwe * 1e3 * burn_time_s,
        "burn_time_yr": burn_time_yr,
        "feasible": True,
    }


def evaluate_cell(
    p_reactor_kwe: float,
    m_hydrolox_t: float,
    chunk_t: float,
    eta_gen: float,
    aerocapture_credit_km_s: float,
    isp_s: float,
    saturn_dep: str,
    lga: bool,
    tank_frac: float,
) -> dict[str, Any]:
    """Evaluate one cell against the joint pass/fail flag set."""
    dv_inbound_km_s = DV_INBOUND_KM_S[(saturn_dep, lga)] - aerocapture_credit_km_s
    dv_inbound_m_s = dv_inbound_km_s * 1000.0
    dry = dry_bundle_t(p_reactor_kwe, m_hydrolox_t, eta_gen, tank_frac)
    tsiol = tsiolkovsky_from_chunk(chunk_t, dry["total_t"], isp_s, dv_inbound_m_s)
    burn = solve_burn_time_yr(tsiol["electrical_energy_j"], p_reactor_kwe, m_hydrolox_t, eta_gen)
    round_trip_yr = OUTBOUND_BURN_YR + HOHMANN_CRUISE_YR * 2 + SATURN_OPS_YR + burn["burn_time_yr"]
    # Earth-orbit stack mass: vehicle dry + chunk (initial, before harvesting) + hydrolox + tankage already in dry["tank_t"] + chemical kick stage
    earth_orbit_stack_t = dry["total_t"] + chunk_t + m_hydrolox_t + CHEMICAL_KICK_STAGE_T
    # Pass/fail flags
    delivers_positive = (not tsiol["chunk_eaten"]) and tsiol["chunk_delivered_t"] > 0.0
    closes_strict = round_trip_yr <= L0_05_STRICT_YR
    closes_waiver = round_trip_yr <= L0_05_WAIVER_YR
    closes_demo = round_trip_yr <= DEMONSTRATOR_CEILING_YR
    launchable_2x = earth_orbit_stack_t <= STARSHIP_2X_T
    launchable_1x = earth_orbit_stack_t <= STARSHIP_1X_T
    lifetime_design_ok = burn["burn_time_yr"] <= LIFETIME_DESIGN_YR
    lifetime_aspirational_ok = burn["burn_time_yr"] <= LIFETIME_ASPIRATIONAL_YR
    lifetime_ground_ok = burn["burn_time_yr"] <= LIFETIME_GROUND_YR
    # Joint flags (phoebe-aggregate hypothesis)
    closes_joint_strict = (
        delivers_positive
        and closes_strict
        and launchable_1x
        and lifetime_design_ok
    )
    closes_joint_demo = (
        delivers_positive
        and closes_demo
        and launchable_2x
        and lifetime_aspirational_ok
    )
    # Sanity check: thruster energy bounded by sources
    e_source = burn["e_reactor_at_burn_j"] + burn["e_hydrolox_j"]
    energy_sanity_ok = e_source + 1.0 >= tsiol["electrical_energy_j"]
    return {
        "p_reactor_kwe": p_reactor_kwe,
        "m_hydrolox_t": m_hydrolox_t,
        "chunk_t": chunk_t,
        "eta_gen": eta_gen,
        "aerocapture_credit_km_s": aerocapture_credit_km_s,
        "isp_s": isp_s,
        "saturn_dep": saturn_dep,
        "lga": lga,
        "tank_frac": tank_frac,
        "dv_inbound_km_s": dv_inbound_km_s,
        "dry_total_t": dry["total_t"],
        "m_prop_t": tsiol["m_prop_t"],
        "chunk_eaten": tsiol["chunk_eaten"],
        "chunk_delivered_t": tsiol["chunk_delivered_t"],
        "electrical_energy_TJ": tsiol["electrical_energy_j"] / 1e12,
        "e_reactor_at_burn_TJ": burn["e_reactor_at_burn_j"] / 1e12,
        "e_hydrolox_TJ": burn["e_hydrolox_j"] / 1e12,
        "burn_time_yr": burn["burn_time_yr"],
        "round_trip_yr": round_trip_yr,
        "earth_orbit_stack_t": earth_orbit_stack_t,
        "delivers_positive": delivers_positive,
        "closes_strict_15yr": closes_strict,
        "closes_waiver_25yr": closes_waiver,
        "closes_demo_40yr": closes_demo,
        "launchable_1x_starship": launchable_1x,
        "launchable_2x_starship": launchable_2x,
        "lifetime_ground_28hr_ok": lifetime_ground_ok,
        "lifetime_design_10yr_ok": lifetime_design_ok,
        "lifetime_aspirational_30yr_ok": lifetime_aspirational_ok,
        "closes_joint_strict": closes_joint_strict,
        "closes_joint_demonstrator": closes_joint_demo,
        "energy_sanity_ok": energy_sanity_ok,
    }


def run_scope_as_written() -> list[dict[str, Any]]:
    """SCOPE-as-written sweep: 5 x 6 x 5 x 2 x 2 x 3 = 1,800 cells.

    Saturn departure fixed at Iapetus-distance + LGA (SCOPE's implicit 25 km/s anchor).
    Tank fraction fixed at 0.10 (SCOPE).
    """
    cells = []
    for p in P_REACTOR_KWE:
        for m in M_H2O2_T:
            for chunk in CHUNK_T:
                for eg in ETA_GEN:
                    for ac in AEROCAPTURE_KM_S:
                        for isp in ISP_S:
                            cells.append(
                                evaluate_cell(
                                    p_reactor_kwe=p,
                                    m_hydrolox_t=m,
                                    chunk_t=chunk,
                                    eta_gen=eg,
                                    aerocapture_credit_km_s=ac,
                                    isp_s=isp,
                                    saturn_dep="Iapetus_distance",
                                    lga=True,
                                    tank_frac=0.10,
                                )
                            )
    return cells


def run_audit_extensions() -> dict[str, list[dict[str, Any]]]:
    """Audit-extension sweeps at headline cells: Saturn departure + tank fraction."""
    headline_chunks = [10.0, 50.0, 200.0]
    headline_hydrolox = [0.0, 250.0, 1000.0]
    headline_p_reactor = [10.0]
    headline_eta_gen = [0.5]
    headline_isp = [3000.0]
    headline_ac = [0.0]

    by_saturn_dep = []
    for sd, lga in SATURN_DEPARTURE_AND_LGA:
        for p in headline_p_reactor:
            for m in headline_hydrolox:
                for chunk in headline_chunks:
                    for eg in headline_eta_gen:
                        for ac in headline_ac:
                            for isp in headline_isp:
                                by_saturn_dep.append(
                                    evaluate_cell(p, m, chunk, eg, ac, isp, sd, lga, 0.10)
                                )

    by_tank_frac = []
    for tf in TANK_FRAC:
        for p in headline_p_reactor:
            for m in headline_hydrolox:
                for chunk in headline_chunks:
                    for eg in headline_eta_gen:
                        for ac in headline_ac:
                            for isp in headline_isp:
                                by_tank_frac.append(
                                    evaluate_cell(p, m, chunk, eg, ac, isp, "Iapetus_distance", True, tf)
                                )

    return {"saturn_departure": by_saturn_dep, "tank_fraction": by_tank_frac}


def summarize_scope(cells: list[dict[str, Any]]) -> dict[str, Any]:
    n = len(cells)
    n_chunk_eaten = sum(1 for c in cells if c["chunk_eaten"])
    n_delivers_positive = sum(1 for c in cells if c["delivers_positive"])
    n_closes_strict = sum(1 for c in cells if c["closes_strict_15yr"])
    n_closes_waiver = sum(1 for c in cells if c["closes_waiver_25yr"])
    n_closes_demo = sum(1 for c in cells if c["closes_demo_40yr"])
    n_launchable_1x = sum(1 for c in cells if c["launchable_1x_starship"])
    n_launchable_2x = sum(1 for c in cells if c["launchable_2x_starship"])
    n_lifetime_design = sum(1 for c in cells if c["lifetime_design_10yr_ok"])
    n_lifetime_ground = sum(1 for c in cells if c["lifetime_ground_28hr_ok"])
    n_closes_joint_strict = sum(1 for c in cells if c["closes_joint_strict"])
    n_closes_joint_demo = sum(1 for c in cells if c["closes_joint_demonstrator"])
    n_energy_sanity_violations = sum(1 for c in cells if not c["energy_sanity_ok"])
    # Best cells
    surviving_joint_strict = [c for c in cells if c["closes_joint_strict"]]
    surviving_joint_demo = [c for c in cells if c["closes_joint_demonstrator"]]
    return {
        "total_cells": n,
        "chunk_eaten": n_chunk_eaten,
        "delivers_positive": n_delivers_positive,
        "closes_strict_15yr": n_closes_strict,
        "closes_waiver_25yr": n_closes_waiver,
        "closes_demo_40yr": n_closes_demo,
        "launchable_1x_starship": n_launchable_1x,
        "launchable_2x_starship": n_launchable_2x,
        "lifetime_design_10yr_ok": n_lifetime_design,
        "lifetime_ground_28hr_ok": n_lifetime_ground,
        "closes_joint_strict": n_closes_joint_strict,
        "closes_joint_demonstrator": n_closes_joint_demo,
        "energy_sanity_violations": n_energy_sanity_violations,
        "surviving_joint_strict_cells": surviving_joint_strict,
        "surviving_joint_demonstrator_cells": surviving_joint_demo,
    }


def format_table_summary(summary: dict[str, Any]) -> str:
    """Tabular markdown summary of SCOPE-as-written sweep aggregate counts."""
    lines = [
        "## SCOPE-as-written sweep — aggregate counts",
        "",
        f"Total cells evaluated: **{summary['total_cells']}**",
        "",
        "| Flag | Count | Fraction |",
        "|---|---:|---:|",
    ]
    flags = [
        ("CHUNK-EATEN (m_prop > chunk_initial)", "chunk_eaten"),
        ("delivers_positive (chunk_delivered > 0)", "delivers_positive"),
        ("closes L0-05 strict (round-trip <= 15 yr)", "closes_strict_15yr"),
        ("closes L0-05 waiver (round-trip <= 25 yr)", "closes_waiver_25yr"),
        ("closes demonstrator (round-trip <= 40 yr)", "closes_demo_40yr"),
        ("launchable 1x Starship (stack <= 150 t)", "launchable_1x_starship"),
        ("launchable 2x Starship (stack <= 300 t)", "launchable_2x_starship"),
        ("reactor lifetime ok at Kilopower design (10 yr)", "lifetime_design_10yr_ok"),
        ("reactor lifetime ok at KRUSTY ground (28 hr)", "lifetime_ground_28hr_ok"),
        ("**closes JOINT STRICT (phoebe-aggregate H-pa)**", "closes_joint_strict"),
        ("**closes JOINT DEMONSTRATOR (relaxed)**", "closes_joint_demonstrator"),
        ("energy-bookkeeping sanity violations", "energy_sanity_violations"),
    ]
    for label, key in flags:
        n = summary[key]
        frac = n / summary["total_cells"] if summary["total_cells"] else 0.0
        lines.append(f"| {label} | {n} | {frac:.1%} |")
    return "\n".join(lines)


def format_surviving_cells(summary: dict[str, Any]) -> str:
    lines = ["", "## Surviving cells (joint pass/fail)", ""]

    for joint_name, key in [
        ("Joint STRICT (delivers + L0-05 strict + 1x Starship + lifetime 10 yr)", "surviving_joint_strict_cells"),
        ("Joint DEMONSTRATOR (delivers + 40 yr + 2x Starship + lifetime 30 yr)", "surviving_joint_demonstrator_cells"),
    ]:
        cells = summary[key]
        lines.append(f"### {joint_name}: {len(cells)} cell(s)")
        lines.append("")
        if not cells:
            lines.append("*(no surviving cells)*")
            lines.append("")
            continue
        lines.append("| chunk (t) | P_reactor (kWe) | M_H2O2 (t) | Isp (s) | eta_gen | aerocapture (km/s) | dv_inbound (km/s) | chunk_delivered (t) | burn (yr) | round-trip (yr) | Earth-orbit stack (t) |")
        lines.append("|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
        for c in cells[:30]:
            lines.append(
                f"| {c['chunk_t']:.0f} | {c['p_reactor_kwe']:.0f} | {c['m_hydrolox_t']:.0f} "
                f"| {c['isp_s']:.0f} | {c['eta_gen']:.2f} | {c['aerocapture_credit_km_s']:.0f} "
                f"| {c['dv_inbound_km_s']:.2f} | {c['chunk_delivered_t']:.2f} "
                f"| {c['burn_time_yr']:.2f} | {c['round_trip_yr']:.2f} | {c['earth_orbit_stack_t']:.0f} |"
            )
        if len(cells) > 30:
            lines.append(f"| ... | ({len(cells) - 30} more cells) | | | | | | | | | |")
        lines.append("")
    return "\n".join(lines)


def format_headline_grid(cells: list[dict[str, Any]]) -> str:
    """Headline 2D grid at P_reactor = 10 kWe, Isp = 3000 s, eta_gen = 0.5, ac = 0: min hydrolox that closes each constraint."""
    lines = [
        "",
        "## Headline grid — P_reactor = 10 kWe, Isp = 3000 s, eta_gen = 0.5, aerocapture = 0 km/s",
        "",
        "Row: chunk_mass. Columns: pass/fail flag at each available M_H2O2 (least required for each level).",
        "",
        "| chunk (t) | M_H2O2 needed (delivers_positive) | M_H2O2 needed (closes_demo) | M_H2O2 needed (closes_waiver) | M_H2O2 needed (closes_strict) | M_H2O2 needed (joint_strict) |",
        "|---:|---:|---:|---:|---:|---:|",
    ]
    target_chunks = [5.0, 10.0, 50.0, 100.0, 200.0]
    for chunk in target_chunks:
        row = [f"{chunk:.0f}"]
        for flag in ["delivers_positive", "closes_demo_40yr", "closes_waiver_25yr", "closes_strict_15yr", "closes_joint_strict"]:
            candidates = [
                c["m_hydrolox_t"]
                for c in cells
                if c["chunk_t"] == chunk
                and c["p_reactor_kwe"] == 10.0
                and c["isp_s"] == 3000.0
                and c["eta_gen"] == 0.5
                and c["aerocapture_credit_km_s"] == 0.0
                and c[flag]
            ]
            row.append(f"{min(candidates):.0f}" if candidates else "—")
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def format_audit_extension(ax_cells: dict[str, list[dict[str, Any]]]) -> str:
    lines = ["", "## Audit-extension — Saturn departure and tank fraction", ""]
    lines.append("### Saturn departure sensitivity (P_reactor = 10 kWe, Isp = 3000 s, eta_gen = 0.5, aerocapture = 0 km/s, tank = 0.10)")
    lines.append("")
    lines.append("| Saturn dep | LGA | dv_inbound (km/s) | chunk (t) | M_H2O2 (t) | chunk_delivered (t) | burn (yr) | round-trip (yr) | stack (t) |")
    lines.append("|---|---|---:|---:|---:|---:|---:|---:|---:|")
    for c in ax_cells["saturn_departure"]:
        lines.append(
            f"| {c['saturn_dep']} | {c['lga']} | {c['dv_inbound_km_s']:.2f} | {c['chunk_t']:.0f} "
            f"| {c['m_hydrolox_t']:.0f} | {c['chunk_delivered_t']:.2f} | {c['burn_time_yr']:.2f} "
            f"| {c['round_trip_yr']:.2f} | {c['earth_orbit_stack_t']:.0f} |"
        )
    lines.append("")
    lines.append("### Tank fraction sensitivity (P_reactor = 10 kWe, Isp = 3000 s, eta_gen = 0.5, aerocapture = 0 km/s, Iapetus-distance + LGA)")
    lines.append("")
    lines.append("| tank_frac | chunk (t) | M_H2O2 (t) | dry_total (t) | chunk_delivered (t) | burn (yr) | round-trip (yr) | stack (t) |")
    lines.append("|---:|---:|---:|---:|---:|---:|---:|---:|")
    for c in ax_cells["tank_fraction"]:
        lines.append(
            f"| {c['tank_frac']:.2f} | {c['chunk_t']:.0f} | {c['m_hydrolox_t']:.0f} | {c['dry_total_t']:.2f} "
            f"| {c['chunk_delivered_t']:.2f} | {c['burn_time_yr']:.2f} | {c['round_trip_yr']:.2f} | {c['earth_orbit_stack_t']:.0f} |"
        )
    return "\n".join(lines)


def grade_hypotheses(cells: list[dict[str, Any]]) -> str:
    lines = ["", "## Hypothesis grading", ""]
    # H1
    h1_cells = [
        c for c in cells
        if c["chunk_t"] == 200.0
        and c["p_reactor_kwe"] == 10.0
        and c["m_hydrolox_t"] <= 1000.0
        and c["eta_gen"] == 0.5
        and c["closes_strict_15yr"]
    ]
    h1_held = len(h1_cells) == 0
    lines.append(f"**H1** (200-t commercial closes L0-05 strict at M_H2O2 <= 1000 t @ eta_gen=0.5? predicted: zero cells): observed **{len(h1_cells)}** cells. {'HELD' if h1_held else 'FALSIFIED'}.")
    # H2
    h2_cells = [
        c for c in cells
        if c["chunk_t"] <= 50.0
        and c["p_reactor_kwe"] == 10.0
        and c["m_hydrolox_t"] <= 500.0
        and c["closes_waiver_25yr"]
        and c["delivers_positive"]
    ]
    h2_held = len(h2_cells) > 0
    lines.append(f"**H2** (chunk <= 50 t closes L0-05 waiver at M_H2O2 <= 500 t? predicted: at least one): observed **{len(h2_cells)}** cells. {'HELD' if h2_held else 'FALSIFIED'}.")
    # H3
    h3_cells = [
        c for c in cells
        if c["chunk_t"] <= 10.0
        and c["m_hydrolox_t"] == 0.0
        and c["closes_demo_40yr"]
        and c["delivers_positive"]
    ]
    h3_held = len(h3_cells) > 0
    lines.append(f"**H3** (chunk <= 10 t closes 30-40 yr demonstrator at M_H2O2 = 0? predicted: yes): observed **{len(h3_cells)}** cells. {'HELD' if h3_held else 'FALSIFIED'}.")
    # H4
    delivered_at_chunk = {}
    for chunk_target in [5.0, 10.0, 20.0, 50.0, 100.0, 200.0]:
        sub = [c for c in cells if c["chunk_t"] == chunk_target and c["closes_joint_strict"]]
        delivered_at_chunk[chunk_target] = sub
    h4_cliff_at = None
    for chunk_target in [5.0, 10.0, 50.0, 100.0, 200.0]:
        sub = [c for c in cells if c["chunk_t"] == chunk_target and c["m_hydrolox_t"] <= 1000.0 and c["closes_demo_40yr"] and c["delivers_positive"]]
        if not sub and h4_cliff_at is None:
            h4_cliff_at = chunk_target
    lines.append(f"**H4** (cliff in delivered chunk in [20, 80] t? predicted: yes): first chunk_mass where hydrolox > 1000 t needed for demo closure = {h4_cliff_at}. {'HELD' if h4_cliff_at and 20.0 <= h4_cliff_at <= 80.0 else 'FALSIFIED'}.")
    # H5
    surviving = [c for c in cells if c["closes_joint_demonstrator"]]
    if surviving:
        rt_range = (min(c["round_trip_yr"] for c in surviving), max(c["round_trip_yr"] for c in surviving))
        h5_held = 22.0 <= rt_range[0] and rt_range[1] <= 30.0
        lines.append(f"**H5** (round-trip 22-30 yr for surviving cells? predicted): observed range [{rt_range[0]:.1f}, {rt_range[1]:.1f}] yr across {len(surviving)} surviving cell(s). {'HELD' if h5_held else 'FALSIFIED'}.")
    else:
        lines.append("**H5** (round-trip 22-30 yr for surviving cells? predicted): **not gradable — zero surviving cells under joint demonstrator constraint.**")
    # H6 — Linear scaling: at fixed Isp, eta_gen, M_H2O2 to close varies linearly with chunk?
    h6_pairs = []
    for isp in [3000.0]:
        for eg in [0.5]:
            for chunk in [10.0, 50.0, 100.0, 200.0]:
                sub = [c for c in cells if c["chunk_t"] == chunk and c["isp_s"] == isp and c["eta_gen"] == eg and c["p_reactor_kwe"] == 10.0 and c["delivers_positive"] and c["closes_demo_40yr"]]
                if sub:
                    min_m = min(s["m_hydrolox_t"] for s in sub)
                    h6_pairs.append((chunk, min_m))
    if len(h6_pairs) >= 2:
        # Linear fit check: slope (M_H2O2 / chunk_t) variance < 15%?
        slopes = [m / c for c, m in h6_pairs if c > 0 and m > 0]
        if slopes:
            avg = sum(slopes) / len(slopes)
            dev = max(abs(s - avg) / avg for s in slopes) if avg > 0 else 0.0
            h6_held = dev <= 0.15
            lines.append(f"**H6** (M_H2O2 scales linearly with chunk? predicted: yes within +/-15%): slopes={[f'{s:.1f}' for s in slopes]}, deviation={dev:.1%}. {'HELD' if h6_held else 'FALSIFIED'}.")
        else:
            lines.append("**H6** (linear scaling): not gradable — surviving cells require zero hydrolox (reactor-only).")
    else:
        lines.append(f"**H6** (linear scaling): not gradable — fewer than 2 closing cells in fit set ({len(h6_pairs)} found).")

    # H-pa-aggregate
    joint_strict = sum(1 for c in cells if c["closes_joint_strict"])
    joint_demo = sum(1 for c in cells if c["closes_joint_demonstrator"])
    lines.append("")
    lines.append(f"**H-pa-aggregate (phoebe)** (0 cells close joint-strict; 1-4 cells close joint-demonstrator): observed **{joint_strict}** joint-strict, **{joint_demo}** joint-demonstrator.")
    return "\n".join(lines)


def main() -> None:
    out_dir = Path(__file__).parent / "results"
    out_dir.mkdir(parents=True, exist_ok=True)

    print("Running SCOPE-as-written sweep (1,800 cells)...")
    scope_cells = run_scope_as_written()
    scope_summary = summarize_scope(scope_cells)

    print("Running audit-extension sweeps (Saturn departure + tank fraction)...")
    audit_cells = run_audit_extensions()

    # Write tables.md
    tables_md = []
    tables_md.append("# R-hybrid-chemical-power-augmentation — results tables")
    tables_md.append("")
    tables_md.append(f"Generated by `run.py`. SCOPE-as-written: 1,800 cells. Audit-extension: {len(audit_cells['saturn_departure']) + len(audit_cells['tank_fraction'])} cells.")
    tables_md.append("")
    tables_md.append(format_table_summary(scope_summary))
    tables_md.append(format_surviving_cells(scope_summary))
    tables_md.append(format_headline_grid(scope_cells))
    tables_md.append(format_audit_extension(audit_cells))
    tables_md.append(grade_hypotheses(scope_cells))
    (out_dir / "tables.md").write_text("\n".join(tables_md))
    print(f"Wrote {out_dir / 'tables.md'}")

    # Write full sweep JSON
    full_dump = {
        "scope_summary": {k: v for k, v in scope_summary.items() if k not in {"surviving_joint_strict_cells", "surviving_joint_demonstrator_cells"}},
        "scope_cells": scope_cells,
        "audit_extensions": audit_cells,
    }
    (out_dir / "launch_stack.json").write_text(json.dumps(full_dump, indent=2))
    print(f"Wrote {out_dir / 'launch_stack.json'} ({len(scope_cells)} SCOPE cells, audit_extensions included)")

    # Console headline
    print()
    print("=" * 72)
    print("HEADLINE")
    print("=" * 72)
    print(f"Total cells: {scope_summary['total_cells']}")
    print(f"CHUNK-EATEN: {scope_summary['chunk_eaten']}  (cells where harvested-water Tsiolkovsky consumes entire chunk)")
    print(f"delivers_positive: {scope_summary['delivers_positive']}")
    print(f"closes_strict_15yr: {scope_summary['closes_strict_15yr']}")
    print(f"closes_waiver_25yr: {scope_summary['closes_waiver_25yr']}")
    print(f"closes_demo_40yr: {scope_summary['closes_demo_40yr']}")
    print(f"closes_joint_strict (H-pa-aggregate prediction = 0): {scope_summary['closes_joint_strict']}")
    print(f"closes_joint_demonstrator (H-pa-aggregate prediction = 1-4): {scope_summary['closes_joint_demonstrator']}")
    print(f"energy_sanity_violations (model-bug indicator; predicted 0): {scope_summary['energy_sanity_violations']}")


if __name__ == "__main__":
    main()
