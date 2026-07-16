"""R-hybrid-chemical-power-augmentation — sweep.

Tsiolkovsky-plus-energy-bookkeeping closure check for the project-owner's hybrid
power architecture: a small reactor (1-100 kilowatts-electric) plus a brought-
from-Earth hydrolox gas-generator that supplies extra electrical power to the
Hall thruster during the inbound burn.

Model documented in STUDY.md §2. Pre-registered hypotheses in STUDY.md §3.

Outputs:
  results/launch_stack.json  - full sweep
  results/tables.md          - headline tables and sanity-anchor cells
"""

from __future__ import annotations

import json
import math
import os
from dataclasses import dataclass, asdict
from typing import Iterable

# ---------------------------------------------------------------------------
# Physical constants and architectural anchors

G0 = 9.80665                       # standard gravity, metres per second squared
LHV_HYDROLOX_J_PER_KG = 1.34e7     # lower heating value, joules per kilogram (water-vapour product)
ETA_THR = 0.65                     # Hall thruster electrical-to-jet efficiency
V_E_CHEM = 4414.0                  # chemical upper-stage exhaust velocity (hydrolox Isp 450 s)
DV_TSI = 7.0e3                     # trans-Saturn injection delta-velocity from low Earth orbit, metres per second
T_OUTBOUND_YR = 6.09               # Hohmann cruise time, Earth to Saturn, years
T_SATURN_OPS_YR = 0.5              # Saturn-side rendezvous + grapple + stow window, years
KICK_STAGE_DRY_FRAC = 0.10         # chemical-kick stage dry mass / propellant mass

YEAR_S = 365.25 * 24 * 3600        # seconds per Julian year

# Sub-system mass coefficients (see STUDY.md §2.6)
M_BAG_T = 50.0                     # bag plus harvesting hardware, tonnes
M_STRUCTURE_T = 30.0               # structure, avionics, residual tankage, tonnes
HALL_T_PER_KW = 0.01               # Hall thruster mass per kilowatt peak electric
GEN_T_PER_KW = 0.05                # gas-generator subsystem mass per kilowatt peak electric output
RADIATOR_T_PER_KW_WASTE = 0.10     # radiator mass per kilowatt of waste-heat shed (kilowatt-class anchor)
TANK_FRAC_HYDROLOX = 0.10          # cryogenic hydrolox tank dry mass / propellant mass

# Saturn-capture chemical (axis-18 locked anchor; 0.8 km/s impulsive at Isp 320 s)
DV_SAT_CAP = 0.8e3
V_E_SAT_CAP = 320.0 * G0
SAT_CAP_TANK_FRAC = 0.10

# Pass/fail thresholds
L0_05_STRICT_YR = 15.0
L0_05_WAIVER_YR = 25.0
LEO_STACK_LIMIT_T_FOR_ARCHITECTURALLY_PLAUSIBLE = 5000.0  # ~33 Starships per mission

# ---------------------------------------------------------------------------
# Sweep grid (per SCOPE §"Variables to sweep" plus sanity anchors)

P_REACTOR_KW = [1, 5, 10, 20, 50, 100]
M_H2O2_T = [0, 100, 250, 500, 1000, 2500, 5000]
M_CHUNK_T = [5, 10, 50, 100, 200]
ETA_GEN = [0.30, 0.50]
ISP_E_S = [2000, 5000]
AEROCAP_KMPS = [0, 10]
SPEC_POWER_W_PER_KG = [2.4, 5.0]    # reactor specific power: flown / optimistic
DV_INBOUND_BASE_KMPS = 25.0          # orchestrator central per SCOPE §3.2


# ---------------------------------------------------------------------------
# Core physics

def solve_chunk_propellant(
    dv_inbound: float,
    v_e_hall: float,
    m_chunk: float,
    m_h2o2: float,
    m_dry_inbound: float,
) -> float | None:
    """Solve Tsiolkovsky for chunk-water propellant consumed during inbound burn.

    Bookkeeping (open-cycle, STUDY.md §2.2):
        m_initial = m_dry_inbound + m_chunk + m_h2o2
        m_final   = m_dry_inbound + (m_chunk - m_p)
        v_e_eff   = v_e_hall * m_p / (m_p + m_h2o2)
        dv        = v_e_eff * ln(m_initial / m_final)

    Returns m_p (tonnes) if a positive solution with m_p < m_chunk exists;
    None if no feasible m_p in (0, m_chunk).

    Caveat: with non-zero m_h2o2, v_e_eff depends on m_p, so this is solved by
    bisection. At m_h2o2 = 0, v_e_eff = v_e_hall and the equation collapses
    to the standard Tsiolkovsky form.
    """
    if m_h2o2 == 0:
        # Pure-electric. Closed form.
        mass_ratio = math.exp(dv_inbound / v_e_hall)
        m_final = m_dry_inbound  # chunk fully consumed in worst case
        m_initial_required = (m_dry_inbound + m_chunk) * 1.0  # vehicle + chunk at start
        # m_p such that (m_dry + m_chunk) / (m_dry + m_chunk - m_p) = mass_ratio
        m_p = (m_dry_inbound + m_chunk) * (1 - 1 / mass_ratio)
        if m_p >= m_chunk or m_p <= 0:
            return None
        return m_p

    # Define f(m_p) = v_e_eff(m_p) * ln(m_initial / m_final) - dv_inbound, find root in (0, m_chunk).
    def residual(m_p: float) -> float:
        if m_p <= 0:
            return -dv_inbound  # large negative
        m_initial = m_dry_inbound + m_chunk + m_h2o2
        m_final = m_dry_inbound + (m_chunk - m_p)
        if m_final <= 0:
            return float("inf")
        v_e_eff = v_e_hall * m_p / (m_p + m_h2o2)
        return v_e_eff * math.log(m_initial / m_final) - dv_inbound

    # Bracket. At m_p -> 0+, v_e_eff -> 0, dv achievable -> 0; residual negative.
    # At m_p -> m_chunk-, residual large positive (m_final small).
    lo, hi = 1e-6, m_chunk * (1 - 1e-9)
    if residual(hi) < 0:
        # Even consuming the entire chunk does not achieve dv_inbound.
        return None
    if residual(lo) > 0:
        # Trivially closes with tiny propellant - means m_h2o2 alone gives the dv (impossible since v_e_eff -> 0).
        # Should not happen with the bookkeeping above.
        return lo
    for _ in range(100):
        mid = 0.5 * (lo + hi)
        r = residual(mid)
        if abs(r) < 1e-3:  # within 1 mm/s
            return mid
        if r < 0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def fixed_point_cell(
    p_reactor_kw: float,
    m_h2o2_t: float,
    m_chunk_t: float,
    eta_gen: float,
    isp_e_s: float,
    aerocap_kmps: float,
    spec_power_w_per_kg: float,
    dv_inbound_base_kmps: float,
) -> dict:
    """Solve one cell by fixed-point iteration on dry mass."""
    dv_inbound = (dv_inbound_base_kmps - aerocap_kmps) * 1e3   # metres per second
    v_e_hall = isp_e_s * G0

    # Initial dry-mass guess: bag + structure + reactor + tank + nominal generator
    m_dry_guess = (
        M_BAG_T
        + M_STRUCTURE_T
        + p_reactor_kw / spec_power_w_per_kg / 1e3 * 1e3  # tonnes from W/(W/kg)/1000
        + TANK_FRAC_HYDROLOX * m_h2o2_t
        + 5.0  # nominal gas-gen
    )
    # Note: reactor mass = p_reactor_kw [kW] / (spec_power_w_per_kg) [W/kg] = p_reactor_kw * 1000 / spec_power [kg]
    # = p_reactor_kw / spec_power [tonnes].
    m_reactor_t = p_reactor_kw / spec_power_w_per_kg
    m_tank_h2o2_t = TANK_FRAC_HYDROLOX * m_h2o2_t

    feasible = True
    failure_reason = ""
    m_p_t = None
    t_burn_yr = None
    p_gen_peak_kw = 0.0
    m_dry_inbound_t = 0.0

    for _ in range(20):  # fixed-point iteration on dry mass / generator size
        # Estimate Saturn-capture chemical prop assuming full vehicle + chunk + hydrolox arrives at Saturn.
        # Wet at Saturn (post-Hohmann coast, pre-Saturn-capture burn).
        m_wet_pre_satcap_t = m_dry_guess + m_chunk_t + m_h2o2_t
        # Wait, chunk is not aboard pre-capture. Chunk is captured at Saturn AFTER capture burn.
        # So pre-capture: m_dry + m_h2o2 only.
        m_pre_capture_t = m_dry_guess + m_h2o2_t
        mr_satcap = math.exp(DV_SAT_CAP / V_E_SAT_CAP)
        m_satcap_prop_t = m_pre_capture_t * (mr_satcap - 1)
        m_satcap_tank_t = SAT_CAP_TANK_FRAC * m_satcap_prop_t
        # Saturn-capture stage dry burns away post-capture; tank stays with vehicle (small).
        # For mass bookkeeping we fold m_satcap_tank_t into vehicle dry; it's small.

        m_dry_inbound_t = m_dry_guess + m_satcap_tank_t  # vehicle dry as it begins the inbound burn

        # Solve Tsiolkovsky for chunk propellant consumed in inbound burn.
        m_p_t = solve_chunk_propellant(
            dv_inbound=dv_inbound,
            v_e_hall=v_e_hall,
            m_chunk=m_chunk_t,
            m_h2o2=m_h2o2_t,
            m_dry_inbound=m_dry_inbound_t,
        )
        if m_p_t is None:
            feasible = False
            failure_reason = "Tsiolkovsky infeasible (chunk too small for dv even fully consumed, or model degenerate)"
            break

        # Energy balance. Solve for t_burn.
        e_elec_total_j = 0.5 * (m_p_t * 1e3) * v_e_hall ** 2 / ETA_THR
        e_hydrolox_j = eta_gen * (m_h2o2_t * 1e3) * LHV_HYDROLOX_J_PER_KG
        e_reactor_needed_j = e_elec_total_j - e_hydrolox_j

        if e_reactor_needed_j <= 0:
            # Hydrolox alone over-supplies energy. We'd burn it slower or dump excess - either way
            # the bottleneck is then thruster peak power, not energy. For Hall sized to consume
            # the energy in a sensible burn time, we pick t_burn such that average gen power = 2 x
            # average needed (overdriven generator burns hydrolox fast); but the SIMPLE bound is:
            # t_burn = duration over which hydrolox is consumed at burn rate matching power demand.
            # In this regime, take t_burn = e_elec_total / max_admissible_p_elec, where we cap
            # max p_elec at the value that empties the hydrolox in roughly 1 yr (engineering plausibility).
            # For minimum t_burn, assume hydrolox burns over ~1 yr; this just sets a lower bound.
            t_burn_s = e_elec_total_j / (e_hydrolox_j / YEAR_S)  # consume hydrolox in 1 yr; t_burn ~ 1 yr.
            t_burn_yr = t_burn_s / YEAR_S
        else:
            # Reactor supplies the gap; burn duration = gap / reactor power.
            t_burn_s = e_reactor_needed_j / (p_reactor_kw * 1e3)
            t_burn_yr = t_burn_s / YEAR_S

        if t_burn_yr <= 0 or not math.isfinite(t_burn_yr):
            feasible = False
            failure_reason = f"t_burn non-positive/non-finite: {t_burn_yr}"
            break

        # Peak generator power: average over t_burn for hydrolox consumption
        p_gen_peak_kw = (e_hydrolox_j / 1e3) / (t_burn_yr * YEAR_S)  # kW average
        p_gen_peak_kw = max(p_gen_peak_kw, 0.0)
        p_elec_peak_kw = p_reactor_kw + p_gen_peak_kw

        # Waste-heat shed (reactor included in reactor mass via specific power, but gas-gen waste extra)
        p_waste_gen_kw = p_gen_peak_kw * (1 - eta_gen) / eta_gen if eta_gen > 0 else 0.0
        m_radiator_extra_t = RADIATOR_T_PER_KW_WASTE * p_waste_gen_kw

        m_gen_t = GEN_T_PER_KW * p_gen_peak_kw
        m_hall_t = HALL_T_PER_KW * p_elec_peak_kw

        m_dry_new = (
            M_BAG_T
            + M_STRUCTURE_T
            + m_reactor_t
            + m_tank_h2o2_t
            + m_gen_t
            + m_radiator_extra_t
            + m_hall_t
        )
        if abs(m_dry_new - m_dry_guess) < 0.05:  # 50 kg convergence
            m_dry_guess = m_dry_new
            break
        m_dry_guess = m_dry_new
    else:
        # Fixed-point did not converge; mark and proceed with last guess.
        feasible = False
        failure_reason = "fixed-point did not converge in 20 iterations"

    if not feasible or m_p_t is None or t_burn_yr is None:
        return {
            "feasible": False,
            "failure_reason": failure_reason,
            "p_reactor_kw": p_reactor_kw,
            "m_h2o2_t": m_h2o2_t,
            "m_chunk_t": m_chunk_t,
            "eta_gen": eta_gen,
            "isp_e_s": isp_e_s,
            "aerocap_kmps": aerocap_kmps,
            "spec_power_w_per_kg": spec_power_w_per_kg,
        }

    delivered_chunk_t = m_chunk_t - m_p_t
    round_trip_yr = T_OUTBOUND_YR + T_SATURN_OPS_YR + t_burn_yr

    # LEO stack: chemical-kick TSI of (vehicle + h2o2 + chunk-capture-prop) ... but chunk is not aboard at LEO.
    # At LEO, the stack is: vehicle dry + hydrolox + Saturn-capture chemical prop + tankage.
    # Then chemical kick adds TSI prop on top to provide 7 km/s from LEO to trans-Saturn trajectory.
    m_pre_capture_t = m_dry_guess + m_h2o2_t
    m_satcap_prop_t = m_pre_capture_t * (math.exp(DV_SAT_CAP / V_E_SAT_CAP) - 1)
    m_injected_t = m_pre_capture_t + m_satcap_prop_t  # mass injected into trans-Saturn trajectory
    mr_tsi = math.exp(DV_TSI / V_E_CHEM)
    m_tsi_prop_t = m_injected_t * (mr_tsi - 1)
    m_tsi_kick_dry_t = KICK_STAGE_DRY_FRAC * m_tsi_prop_t
    m_leo_stack_t = m_injected_t + m_tsi_prop_t + m_tsi_kick_dry_t

    # Energy sanity gate
    e_elec_total_j = 0.5 * (m_p_t * 1e3) * v_e_hall ** 2 / ETA_THR
    e_supplied_j = p_reactor_kw * 1e3 * t_burn_yr * YEAR_S + eta_gen * (m_h2o2_t * 1e3) * LHV_HYDROLOX_J_PER_KG
    energy_balance_ratio = e_supplied_j / max(e_elec_total_j, 1e-9)

    # Pass/fail flags
    delivered_positive = delivered_chunk_t > 0
    l0_05_strict = round_trip_yr <= L0_05_STRICT_YR
    l0_05_waiver = round_trip_yr <= L0_05_WAIVER_YR
    launchable = m_leo_stack_t <= LEO_STACK_LIMIT_T_FOR_ARCHITECTURALLY_PLAUSIBLE
    delivered_above_10t = delivered_chunk_t > 10.0
    closes_h1 = (delivered_chunk_t > 10.0) and l0_05_strict

    return {
        "feasible": True,
        "failure_reason": "",
        # Inputs
        "p_reactor_kw": p_reactor_kw,
        "m_h2o2_t": m_h2o2_t,
        "m_chunk_t": m_chunk_t,
        "eta_gen": eta_gen,
        "isp_e_s": isp_e_s,
        "aerocap_kmps": aerocap_kmps,
        "spec_power_w_per_kg": spec_power_w_per_kg,
        # Derived
        "dv_inbound_kmps": (DV_INBOUND_BASE_KMPS - aerocap_kmps),
        "m_dry_t": round(m_dry_guess, 3),
        "m_reactor_t": round(m_reactor_t, 3),
        "m_chunk_prop_t": round(m_p_t, 3),
        "delivered_chunk_t": round(delivered_chunk_t, 3),
        "t_burn_yr": round(t_burn_yr, 3),
        "round_trip_yr": round(round_trip_yr, 3),
        "p_gen_peak_kw": round(p_gen_peak_kw, 1),
        "p_elec_peak_kw": round(p_reactor_kw + p_gen_peak_kw, 1),
        "m_leo_stack_t": round(m_leo_stack_t, 1),
        "m_tsi_prop_t": round(m_tsi_prop_t, 1),
        "energy_balance_ratio": round(energy_balance_ratio, 4),
        # Pass/fail
        "delivered_positive": delivered_positive,
        "delivered_above_10t": delivered_above_10t,
        "l0_05_strict": l0_05_strict,
        "l0_05_waiver": l0_05_waiver,
        "launchable": launchable,
        "closes_h1": closes_h1,
    }


# ---------------------------------------------------------------------------
# Sweep driver

def sweep() -> list[dict]:
    rows = []
    for p_r in P_REACTOR_KW:
        for m_h in M_H2O2_T:
            for m_c in M_CHUNK_T:
                for eg in ETA_GEN:
                    for ie in ISP_E_S:
                        for ac in AEROCAP_KMPS:
                            for sp in SPEC_POWER_W_PER_KG:
                                row = fixed_point_cell(
                                    p_reactor_kw=p_r,
                                    m_h2o2_t=m_h,
                                    m_chunk_t=m_c,
                                    eta_gen=eg,
                                    isp_e_s=ie,
                                    aerocap_kmps=ac,
                                    spec_power_w_per_kg=sp,
                                    dv_inbound_base_kmps=DV_INBOUND_BASE_KMPS,
                                )
                                rows.append(row)
    return rows


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.join(here, "results")
    os.makedirs(out_dir, exist_ok=True)

    rows = sweep()
    n_total = len(rows)
    n_feasible = sum(1 for r in rows if r.get("feasible"))
    n_delivered_positive = sum(1 for r in rows if r.get("delivered_positive"))
    n_delivered_10t = sum(1 for r in rows if r.get("delivered_above_10t"))
    n_l0_05_strict = sum(1 for r in rows if r.get("l0_05_strict") and r.get("delivered_positive"))
    n_l0_05_waiver = sum(1 for r in rows if r.get("l0_05_waiver") and r.get("delivered_positive"))
    n_closes_h1 = sum(1 for r in rows if r.get("closes_h1"))
    n_launchable = sum(1 for r in rows if r.get("launchable") and r.get("delivered_positive"))

    # Sanity gate: every feasible row's energy_balance_ratio must be >= 1 (within numerical noise)
    sanity_violations = [r for r in rows if r.get("feasible") and r.get("energy_balance_ratio", 0) < 0.999]
    sanity_pass = len(sanity_violations) == 0

    with open(os.path.join(out_dir, "launch_stack.json"), "w") as f:
        json.dump({
            "summary": {
                "n_total": n_total,
                "n_feasible": n_feasible,
                "n_delivered_positive": n_delivered_positive,
                "n_delivered_above_10t": n_delivered_10t,
                "n_l0_05_strict_with_positive_delivered": n_l0_05_strict,
                "n_l0_05_waiver_with_positive_delivered": n_l0_05_waiver,
                "n_closes_h1": n_closes_h1,
                "n_launchable_with_positive_delivered": n_launchable,
                "sanity_pass": sanity_pass,
                "sanity_violation_count": len(sanity_violations),
            },
            "rows": rows,
        }, f, indent=2)

    # Tables
    with open(os.path.join(out_dir, "tables.md"), "w") as f:
        f.write("# R-hybrid-chemical-power-augmentation — results tables\n\n")
        f.write("Generated by `run.py`. See `STUDY.md` §2 for the model and §3 for the pre-registered hypotheses.\n\n")
        f.write("## Sweep summary\n\n")
        f.write(f"- Total cells swept: {n_total}\n")
        f.write(f"- Tsiolkovsky-feasible cells (positive chunk-propellant solution in (0, M_chunk)): {n_feasible}\n")
        f.write(f"- Cells with positive delivered chunk: {n_delivered_positive}\n")
        f.write(f"- Cells with delivered chunk > 10 t: {n_delivered_10t}\n")
        f.write(f"- Cells passing L0-05 strict (round-trip <= 15 yr) with delivered > 0: {n_l0_05_strict}\n")
        f.write(f"- Cells passing L0-05 waiver (round-trip <= 25 yr) with delivered > 0: {n_l0_05_waiver}\n")
        f.write(f"- Cells passing H1 (delivered > 10 t AND L0-05 strict): {n_closes_h1}\n")
        f.write(f"- Cells passing launchable (LEO stack <= 5000 t) AND positive delivered: {n_launchable}\n")
        f.write(f"- Energy-balance sanity gate: {'PASS' if sanity_pass else 'FAIL'} ({len(sanity_violations)} violations)\n\n")

        # H1 corner: P_reactor = 10 kWe, M_chunk = 200 t, eta_gen = 0.50
        f.write("## H1 corner — P_reactor = 10 kWe, M_chunk = 200 t, eta_gen = 0.50, spec_power = 2.4 W/kg, aerocap = 0\n\n")
        f.write("| M_H2O2 (t) | Isp (s) | Tsiolkovsky | m_p (t) | delivered (t) | t_burn (yr) | RT (yr) | LEO stack (t) | passes H1? |\n")
        f.write("|---|---|---|---|---|---|---|---|---|\n")
        for ie in ISP_E_S:
            for m_h in M_H2O2_T:
                row = next(
                    (r for r in rows if r["p_reactor_kw"] == 10 and r["m_chunk_t"] == 200 and r["eta_gen"] == 0.50
                     and r["isp_e_s"] == ie and r["aerocap_kmps"] == 0 and r["m_h2o2_t"] == m_h
                     and r["spec_power_w_per_kg"] == 2.4),
                    None,
                )
                if row is None:
                    continue
                if not row["feasible"]:
                    f.write(f"| {m_h} | {ie} | infeasible: {row['failure_reason'][:40]} | - | - | - | - | - | no |\n")
                else:
                    f.write(
                        f"| {m_h} | {ie} | OK | {row['m_chunk_prop_t']:.1f} | {row['delivered_chunk_t']:.1f} | "
                        f"{row['t_burn_yr']:.2f} | {row['round_trip_yr']:.2f} | {row['m_leo_stack_t']:.0f} | "
                        f"{'**YES**' if row['closes_h1'] else 'no'} |\n"
                    )

        # H2 corner: chunk = 50 t (Architecture-E scope), L0-05 waiver
        f.write("\n## H2 corner — P_reactor = 10 kWe, M_chunk = 50 t, eta_gen = 0.50, spec_power = 2.4 W/kg, aerocap = 0\n\n")
        f.write("| M_H2O2 (t) | Isp (s) | Tsiolkovsky | delivered (t) | t_burn (yr) | RT (yr) | LEO stack (t) | L0-05 waiver? | launchable? |\n")
        f.write("|---|---|---|---|---|---|---|---|---|\n")
        for ie in ISP_E_S:
            for m_h in M_H2O2_T:
                row = next(
                    (r for r in rows if r["p_reactor_kw"] == 10 and r["m_chunk_t"] == 50 and r["eta_gen"] == 0.50
                     and r["isp_e_s"] == ie and r["aerocap_kmps"] == 0 and r["m_h2o2_t"] == m_h
                     and r["spec_power_w_per_kg"] == 2.4),
                    None,
                )
                if row is None:
                    continue
                if not row["feasible"]:
                    f.write(f"| {m_h} | {ie} | infeasible | - | - | - | - | no | no |\n")
                else:
                    f.write(
                        f"| {m_h} | {ie} | OK | {row['delivered_chunk_t']:.1f} | "
                        f"{row['t_burn_yr']:.2f} | {row['round_trip_yr']:.2f} | {row['m_leo_stack_t']:.0f} | "
                        f"{'yes' if row['l0_05_waiver'] else 'no'} | {'yes' if row['launchable'] else 'no'} |\n"
                    )

        # H3 corner: pure-reactor, M_H2O2 = 0
        f.write("\n## H3 corner — pure reactor (M_H2O2 = 0), eta_gen ignored, spec_power = 2.4 W/kg, aerocap = 0\n\n")
        f.write("| P_reactor (kWe) | M_chunk (t) | Isp (s) | Tsiolkovsky | delivered (t) | t_burn (yr) | RT (yr) | L0-05 strict? | RT <= 40 yr? |\n")
        f.write("|---|---|---|---|---|---|---|---|---|\n")
        for p_r in P_REACTOR_KW:
            for m_c in M_CHUNK_T:
                for ie in ISP_E_S:
                    row = next(
                        (r for r in rows if r["p_reactor_kw"] == p_r and r["m_chunk_t"] == m_c
                         and r["isp_e_s"] == ie and r["aerocap_kmps"] == 0 and r["m_h2o2_t"] == 0
                         and r["spec_power_w_per_kg"] == 2.4 and r["eta_gen"] == 0.50),  # eta_gen unused at m_h=0
                        None,
                    )
                    if row is None:
                        continue
                    if not row["feasible"]:
                        f.write(f"| {p_r} | {m_c} | {ie} | infeasible | - | - | - | no | no |\n")
                    else:
                        f.write(
                            f"| {p_r} | {m_c} | {ie} | OK | {row['delivered_chunk_t']:.1f} | "
                            f"{row['t_burn_yr']:.2f} | {row['round_trip_yr']:.2f} | "
                            f"{'yes' if row['l0_05_strict'] else 'no'} | "
                            f"{'yes' if row['round_trip_yr'] <= 40.0 else 'no'} |\n"
                        )

        # H5: minimum LEO stack of any cell that passes L0-05 waiver with positive delivered
        f.write("\n## H5 corner — minimum LEO stack among cells passing L0-05 waiver with positive delivered chunk\n\n")
        waiver_rows = [r for r in rows if r.get("feasible") and r["l0_05_waiver"] and r["delivered_positive"]]
        waiver_rows.sort(key=lambda r: r["m_leo_stack_t"])
        f.write(f"Cells satisfying both: {len(waiver_rows)}\n\n")
        if waiver_rows:
            f.write("Top 10 cells by minimum LEO stack:\n\n")
            f.write("| P_r (kWe) | M_H2O2 (t) | M_chunk (t) | Isp (s) | eta_gen | aerocap (km/s) | spec_pow (W/kg) | delivered (t) | RT (yr) | LEO stack (t) |\n")
            f.write("|---|---|---|---|---|---|---|---|---|---|\n")
            for r in waiver_rows[:10]:
                f.write(
                    f"| {r['p_reactor_kw']} | {r['m_h2o2_t']} | {r['m_chunk_t']} | {r['isp_e_s']} | {r['eta_gen']} | "
                    f"{r['aerocap_kmps']} | {r['spec_power_w_per_kg']} | {r['delivered_chunk_t']:.2f} | "
                    f"{r['round_trip_yr']:.2f} | {r['m_leo_stack_t']:.0f} |\n"
                )
        else:
            f.write("No cells satisfy L0-05 waiver with positive delivered chunk.\n")

        # H1-closing cells (delivered > 10 t AND L0-05 strict)
        h1_rows = [r for r in rows if r.get("closes_h1")]
        f.write(f"\n## H1-closing cells — delivered > 10 t AND L0-05 strict (round-trip <= 15 yr)\n\n")
        f.write(f"Total: {len(h1_rows)}\n\n")
        if h1_rows:
            h1_rows.sort(key=lambda r: r["m_leo_stack_t"])
            f.write("| P_r (kWe) | M_H2O2 (t) | M_chunk (t) | Isp (s) | eta_gen | aerocap | spec_pow | delivered (t) | RT (yr) | LEO stack (t) |\n")
            f.write("|---|---|---|---|---|---|---|---|---|---|\n")
            for r in h1_rows[:20]:
                f.write(
                    f"| {r['p_reactor_kw']} | {r['m_h2o2_t']} | {r['m_chunk_t']} | {r['isp_e_s']} | {r['eta_gen']} | "
                    f"{r['aerocap_kmps']} | {r['spec_power_w_per_kg']} | {r['delivered_chunk_t']:.2f} | "
                    f"{r['round_trip_yr']:.2f} | {r['m_leo_stack_t']:.0f} |\n"
                )

    print(json.dumps({
        "n_total": n_total,
        "n_feasible": n_feasible,
        "n_delivered_positive": n_delivered_positive,
        "n_delivered_above_10t": n_delivered_10t,
        "n_l0_05_strict_with_positive_delivered": n_l0_05_strict,
        "n_l0_05_waiver_with_positive_delivered": n_l0_05_waiver,
        "n_closes_h1": n_closes_h1,
        "n_launchable_with_positive_delivered": n_launchable,
        "sanity_pass": sanity_pass,
        "sanity_violation_count": len(sanity_violations),
    }, indent=2))


if __name__ == "__main__":
    main()
