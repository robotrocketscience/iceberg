"""R-non-fission-baseline — does any non-fission architecture close
L0-05 + L0-09 + L0-12 simultaneously?

Three architectures:

A. Solar-electric outbound (Edelbaum spiral only) + hydrolox kick stage for
   heliocentric departure + chunk-fed chemical inbound. Inbound at either
   specific-impulse 450 s (onsite-electrolyzed hydrolox, requires Saturn-side
   power source) or 200 s (water-steam direct, no Saturn-side electrolysis).
B. All-chemical end-to-end. Impulsive Oberth-credited outbound from low Earth
   orbit, ballistic cruise, chunk-fed chemical inbound.
C. Plutonium-238 radioisotope-electric. Supply-constrained.

Reuses physics from R-megawatt-architecture-viability/run.py:
    outbound_dv_km_s (all-electric integrated)
    hohmann_cruise_yr
    constant_thrust_burn

Outputs:
    results/architecture_A.json
    results/architecture_B.json
    results/architecture_C.json
    results/bayesian_posteriors.json
    results/tables.md

Deterministic; runtime < 1 s.
"""

from __future__ import annotations

import json
import math
from pathlib import Path


# ---------------- shared physics constants ---------------- #

G0 = 9.81
GM_SUN = 1.32712440018e11
GM_EARTH = 398600.4418
R_EARTH = 6378.137
A_EARTH = 149597870.7
A_SATURN = 9.5826 * A_EARTH
YEAR_S = 365.25 * 86400.0
LEO_ALT_KM = 400.0
ETA_THR = 0.65
DV_INBOUND_KM_S = 6.42
SATURN_OPS_YR = 1.0
L0_05_CEILING_YR = 15.0
SATURN_R_AU = 9.5826

# Saturn-side electrolysis energy cost (kWh per kg of water cracked into H2/O2 and
# liquefied). Industrial alkaline electrolysis ~4-5 kWh/kg; cryogenic liquefaction
# adds 30-50%. Conservative estimate.
ELECTROLYSIS_KWH_PER_KG = 8.0
# Saturn ops period in hours (1 year).
SATURN_OPS_HR = SATURN_OPS_YR * 24.0 * 365.25


# ---------------- shared physics helpers ---------------- #

def hohmann_cruise_yr() -> float:
    a_h_km = (A_EARTH + A_SATURN) / 2.0
    return math.pi * math.sqrt(a_h_km ** 3 / GM_SUN) / YEAR_S


def heliocentric_v_inf_earth_km_s() -> float:
    """Earth-departure hyperbolic excess for a Saturn Hohmann transfer."""
    v_earth = math.sqrt(GM_SUN / A_EARTH)
    a_h = (A_EARTH + A_SATURN) / 2.0
    v_peri = math.sqrt(GM_SUN * (2.0 / A_EARTH - 1.0 / a_h))
    return v_peri - v_earth


def edelbaum_spiral_dv_km_s() -> float:
    """Integrated low-thrust delta-velocity for low Earth orbit to Earth-escape."""
    return math.sqrt(GM_EARTH / (R_EARTH + LEO_ALT_KM))


def chemical_impulsive_outbound_dv_km_s() -> float:
    """Oberth-credited impulsive outbound delta-velocity from low Earth orbit.
    `Δv = sqrt(v_escape² + v_∞²) − v_circ`."""
    v_circ = edelbaum_spiral_dv_km_s()
    v_escape = math.sqrt(2.0) * v_circ
    v_inf = heliocentric_v_inf_earth_km_s()
    return math.sqrt(v_escape ** 2 + v_inf ** 2) - v_circ


def constant_thrust_burn(m_initial_t: float, dv_km_s: float,
                         power_kwe: float, isp_s: float) -> dict:
    """Constant-thrust burn at fixed jet-power. m_initial_t is treated as the
    final (post-burn) mass; propellant is computed as m_initial × (MR − 1)."""
    v_e = isp_s * G0
    thrust_N = 2.0 * ETA_THR * power_kwe * 1000.0 / v_e
    mass_ratio = math.exp(dv_km_s * 1000.0 / v_e)
    m_prop_t = m_initial_t * (mass_ratio - 1.0)
    t_burn_s = m_prop_t * 1000.0 * v_e / thrust_N
    return {
        "m_initial_t": m_initial_t,
        "m_prop_t": m_prop_t,
        "m_total_t": m_initial_t + m_prop_t,
        "t_burn_yr": t_burn_s / YEAR_S,
        "mass_ratio": mass_ratio,
    }


def impulsive_burn(m_final_t: float, dv_km_s: float, isp_s: float) -> dict:
    """Tsiolkovsky for an impulsive chemical burn ending at m_final_t."""
    v_e = isp_s * G0
    mass_ratio = math.exp(dv_km_s * 1000.0 / v_e)
    m_initial_t = m_final_t * mass_ratio
    m_prop_t = m_initial_t - m_final_t
    return {
        "m_initial_t": m_initial_t,
        "m_final_t": m_final_t,
        "m_prop_t": m_prop_t,
        "mass_ratio": mass_ratio,
    }


def saturn_side_energy_budget(propellant_water_t: float,
                              sep_kwe_earth_vicinity: float = 0.0,
                              saturn_side_rtg_kwe: float = 0.0,
                              ops_yr: float = SATURN_OPS_YR) -> dict:
    """Check whether Saturn-side electrical power supplies the energy needed to
    electrolyze and liquefy `propellant_water_t` of water during `ops_yr`.

    Saturn-vicinity SEP power = Earth-vicinity power × (1 / 9.5826²) ≈ × 0.0109.
    """
    energy_needed_kwh = propellant_water_t * 1000.0 * ELECTROLYSIS_KWH_PER_KG
    p_at_saturn_kwe = sep_kwe_earth_vicinity * (1.0 / SATURN_R_AU ** 2)
    available_kwe = p_at_saturn_kwe + saturn_side_rtg_kwe
    available_energy_kwh = available_kwe * ops_yr * 24.0 * 365.25
    ratio = available_energy_kwh / energy_needed_kwh if energy_needed_kwh > 0 else float("inf")
    return {
        "propellant_water_t": propellant_water_t,
        "energy_needed_kwh": energy_needed_kwh,
        "sep_at_saturn_kwe": p_at_saturn_kwe,
        "rtg_kwe": saturn_side_rtg_kwe,
        "available_kwe": available_kwe,
        "available_energy_kwh": available_energy_kwh,
        "energy_supply_ratio": ratio,
        "closes_energy_budget": ratio >= 1.0,
    }


def staged_chemical_burn(m_payload_t: float, dv_km_s: float, isp_s: float,
                         n_stages: int, stage_dry_wet: float = 0.10) -> dict:
    """Multi-stage chemical kick. Divide dv evenly across stages. Each stage's
    dry/wet ratio = stage_dry_wet. Returns total wet mass at low Earth orbit
    (stack of n_stages + payload above)."""
    dv_per_stage = dv_km_s / n_stages
    v_e = isp_s * G0
    mr_per_stage = math.exp(dv_per_stage * 1000.0 / v_e)
    m_above = m_payload_t
    total_stage_dry = 0.0
    total_stage_prop = 0.0
    for _ in range(n_stages):
        # M_0 = MR × (m_above + m_stage_dry)
        # m_stage_dry = stage_dry_wet × (m_stage_dry + m_stage_prop)
        # m_stage_prop = (MR − 1) × (m_above + m_stage_dry)
        # Solve: m_stage_dry × (1 / stage_dry_wet − 1) = m_stage_prop
        #        → m_stage_dry = m_stage_prop × stage_dry_wet / (1 − stage_dry_wet)
        # Substitute: m_stage_dry × (1 − stage_dry_wet) / stage_dry_wet
        #             = (MR − 1) × (m_above + m_stage_dry)
        # Let k = (1 − stage_dry_wet) / stage_dry_wet, M = MR − 1
        # m_stage_dry × k = M × m_above + M × m_stage_dry
        # m_stage_dry × (k − M) = M × m_above
        # m_stage_dry = M × m_above / (k − M)
        # Feasible only if k > M, i.e. (1 − stage_dry_wet) / stage_dry_wet > MR − 1
        k = (1.0 - stage_dry_wet) / stage_dry_wet
        M = mr_per_stage - 1.0
        if M >= k:
            return {"feasible": False, "reason":
                    f"single-stage MR {mr_per_stage:.2f} infeasible at dry/wet {stage_dry_wet} (n_stages={n_stages})"}
        m_stage_dry = M * m_above / (k - M)
        m_stage_prop = (k * m_stage_dry)  # by definition of dry/wet ratio
        # Sanity: m_stage_prop = (MR − 1) × (m_above + m_stage_dry)
        # assert close enough
        m_above = m_above + m_stage_dry + m_stage_prop
        total_stage_dry += m_stage_dry
        total_stage_prop += m_stage_prop
    return {
        "feasible": True,
        "n_stages": n_stages,
        "dv_per_stage_km_s": dv_per_stage,
        "mr_per_stage": mr_per_stage,
        "m_payload_t": m_payload_t,
        "m_total_stage_dry_t": total_stage_dry,
        "m_total_stage_prop_t": total_stage_prop,
        "m_LEO_wet_t": m_above,
    }


# ---------------- Architecture A — SEP + chemical kick + chunk-fed chemical inbound ---------------- #

def architecture_A(
    vehicle_dry_t: float = 25.0,
    chunk_t: float = 200.0,
    sep_kwe: float = 200.0,
    sep_array_kg_per_kw: float = 5.0,  # 200 W/kg array = 5 kg/kW
    saturn_side_rtg_t: float = 0.0,
    inbound_isp_s: float = 450.0,
    kick_n_stages: int = 2,
) -> dict:
    dv_edel = edelbaum_spiral_dv_km_s()
    dv_kick_heliocentric = heliocentric_v_inf_earth_km_s()
    cruise_yr = hohmann_cruise_yr()

    sep_array_t = sep_kwe * sep_array_kg_per_kw / 1000.0

    # Inbound: chunk-fed chemical. The chunk is the propellant tank: harvested
    # mass M_chunk is partitioned into propellant burned and water delivered.
    #   m_init  = m_v + m_rtg + m_chunk
    #   m_final = m_v + m_rtg + delivered
    #   MR      = m_init / m_final  →  delivered = m_chunk/MR − (m_v+m_rtg)(1 − 1/MR)
    v_e_inbound = inbound_isp_s * G0
    mr_inbound = math.exp(DV_INBOUND_KM_S * 1000.0 / v_e_inbound)
    delivered_water_t = (chunk_t / mr_inbound
                        - (vehicle_dry_t + saturn_side_rtg_t) * (1.0 - 1.0 / mr_inbound))
    inbound_burn_propellant_t = chunk_t - delivered_water_t

    if delivered_water_t <= 0.0:
        return {
            "architecture": "A",
            "feasible": False,
            "reason": f"inbound chemical at Isp {inbound_isp_s} s consumes more than the chunk; delivered={delivered_water_t:.2f} t",
            "delivered_water_t": delivered_water_t,
        }

    # Outbound — phase 1 (SEP Edelbaum to Earth-escape). Payload at Earth-escape
    # = vehicle_dry + RTG + chemical kick stage(s) wet (to be sized below).
    # First size the kick stage given the post-kick payload.
    # After kick burn: m_above_kick = vehicle_dry + saturn_side_rtg. (Array jettisoned at Earth-escape;
    # kick stage dry jettisoned post-kick burn.)
    m_payload_after_kick = vehicle_dry_t + saturn_side_rtg_t
    kick = staged_chemical_burn(
        m_payload_t=m_payload_after_kick,
        dv_km_s=dv_kick_heliocentric,
        isp_s=450.0,
        n_stages=kick_n_stages,
    )
    if not kick["feasible"]:
        return {
            "architecture": "A",
            "feasible": False,
            "reason": f"chemical kick stage infeasible: {kick.get('reason')}",
            "kick": kick,
        }

    # At Earth-escape (post-Edelbaum spiral, array jettisoned): m_at_escape_before_array_jett
    # = m_LEO − m_SEP_prop − m_array (no, array jettisoned only at Earth-escape).
    # Cleanly: the SEP spiral final mass (post-propellant, pre-array-jettison)
    # is the kick stack + array.
    m_post_spiral = kick["m_LEO_wet_t"] + sep_array_t
    sep_burn = constant_thrust_burn(
        m_initial_t=m_post_spiral,
        dv_km_s=dv_edel,
        power_kwe=sep_kwe,
        isp_s=2000.0,
    )
    m_LEO_t = sep_burn["m_total_t"]
    sep_propellant_t = sep_burn["m_prop_t"]
    sep_burn_yr = sep_burn["t_burn_yr"]

    # Round-trip time. (Saturn ops 1 yr.) Inbound chemical burn is impulsive
    # (Isp 450 s) — burn time << year. Cruise back is Hohmann.
    round_trip_yr = sep_burn_yr + cruise_yr + SATURN_OPS_YR + 0.0 + cruise_yr
    closes_L0_05 = round_trip_yr <= L0_05_CEILING_YR

    # Launch mass per delivered tonne.
    launch_per_delivered = m_LEO_t / delivered_water_t

    # Saturn-side energy budget for Isp 450 s onsite-electrolyzed hydrolox.
    # RTG specific electrical power 5.3 W/kg system (flown General-Purpose-Heat-
    # Source MMRTG); so saturn_side_rtg_t × 5.3 kWe.
    energy_check = saturn_side_energy_budget(
        propellant_water_t=inbound_burn_propellant_t if inbound_isp_s >= 350.0 else 0.0,
        sep_kwe_earth_vicinity=sep_kwe,
        saturn_side_rtg_kwe=saturn_side_rtg_t * 5.3,
        ops_yr=SATURN_OPS_YR,
    ) if inbound_isp_s >= 350.0 else None

    return {
        "architecture": "A",
        "feasible": True,
        "vehicle_dry_t": vehicle_dry_t,
        "chunk_t": chunk_t,
        "saturn_side_rtg_t": saturn_side_rtg_t,
        "sep_kwe": sep_kwe,
        "sep_array_t": sep_array_t,
        "inbound_isp_s": inbound_isp_s,
        "kick_n_stages": kick_n_stages,
        "edelbaum_dv_km_s": dv_edel,
        "kick_heliocentric_dv_km_s": dv_kick_heliocentric,
        "kick_stage_total_dry_t": kick["m_total_stage_dry_t"],
        "kick_stage_total_prop_t": kick["m_total_stage_prop_t"],
        "m_post_spiral_t": m_post_spiral,
        "sep_propellant_t": sep_propellant_t,
        "sep_burn_yr": sep_burn_yr,
        "m_LEO_wet_t": m_LEO_t,
        "delivered_water_t": delivered_water_t,
        "inbound_burn_propellant_t": inbound_burn_propellant_t,
        "mr_inbound": mr_inbound,
        "round_trip_yr": round_trip_yr,
        "closes_L0_05": closes_L0_05,
        "launch_per_delivered_ratio": launch_per_delivered,
        "saturn_side_energy": energy_check,
    }


# ---------------- Architecture B — all-chemical end-to-end ---------------- #

def architecture_B(
    vehicle_dry_t: float = 15.0,
    chunk_t: float = 200.0,
    saturn_side_rtg_t: float = 0.0,
    inbound_isp_s: float = 450.0,
    outbound_n_stages: int = 2,
) -> dict:
    dv_outbound = chemical_impulsive_outbound_dv_km_s()
    cruise_yr = hohmann_cruise_yr()

    # Inbound — same math as architecture A.
    v_e_inbound = inbound_isp_s * G0
    mr_inbound = math.exp(DV_INBOUND_KM_S * 1000.0 / v_e_inbound)
    delivered_water_t = (chunk_t / mr_inbound
                        - (vehicle_dry_t + saturn_side_rtg_t) * (1.0 - 1.0 / mr_inbound))

    if delivered_water_t <= 0.0:
        return {
            "architecture": "B",
            "feasible": False,
            "reason": f"inbound chemical at Isp {inbound_isp_s} s consumes more than the chunk; delivered={delivered_water_t:.2f} t",
            "delivered_water_t": delivered_water_t,
        }

    # Outbound chemical kick stack.
    m_payload_after_kick = vehicle_dry_t + saturn_side_rtg_t
    outbound = staged_chemical_burn(
        m_payload_t=m_payload_after_kick,
        dv_km_s=dv_outbound,
        isp_s=450.0,
        n_stages=outbound_n_stages,
    )
    if not outbound["feasible"]:
        return {
            "architecture": "B",
            "feasible": False,
            "reason": f"outbound chemical stack infeasible: {outbound.get('reason')}",
            "outbound": outbound,
        }
    m_LEO_t = outbound["m_LEO_wet_t"]

    round_trip_yr = 0.0 + cruise_yr + SATURN_OPS_YR + 0.0 + cruise_yr
    closes_L0_05 = round_trip_yr <= L0_05_CEILING_YR
    launch_per_delivered = m_LEO_t / delivered_water_t

    # Saturn-side energy budget for hydrolox onsite electrolysis. Architecture B
    # has no SEP array — only the Saturn-side RTG (if any) supplies power.
    inbound_propellant_t = chunk_t - delivered_water_t
    energy_check = saturn_side_energy_budget(
        propellant_water_t=inbound_propellant_t if inbound_isp_s >= 350.0 else 0.0,
        sep_kwe_earth_vicinity=0.0,
        saturn_side_rtg_kwe=saturn_side_rtg_t * 5.3,
        ops_yr=SATURN_OPS_YR,
    ) if inbound_isp_s >= 350.0 else None

    return {
        "architecture": "B",
        "feasible": True,
        "vehicle_dry_t": vehicle_dry_t,
        "chunk_t": chunk_t,
        "saturn_side_rtg_t": saturn_side_rtg_t,
        "inbound_isp_s": inbound_isp_s,
        "outbound_n_stages": outbound_n_stages,
        "dv_outbound_km_s": dv_outbound,
        "outbound_stage_total_dry_t": outbound["m_total_stage_dry_t"],
        "outbound_stage_total_prop_t": outbound["m_total_stage_prop_t"],
        "m_LEO_wet_t": m_LEO_t,
        "delivered_water_t": delivered_water_t,
        "mr_inbound": mr_inbound,
        "round_trip_yr": round_trip_yr,
        "closes_L0_05": closes_L0_05,
        "launch_per_delivered_ratio": launch_per_delivered,
        "saturn_side_energy": energy_check,
    }


# ---------------- Architecture C — plutonium-238 radioisotope-electric ---------------- #

def architecture_C(power_kwe_targets: list[float]) -> dict:
    """For each target electrical power, compute plutonium-238 mass needed and
    compare against US production rate."""
    # Two bounds for plutonium-238 specific electrical power:
    #   theoretical Stirling at 6.3% efficiency × 540 W/kg thermal → 34.0 W/kg electric
    #   flown General-Purpose-Heat-Source MMRTG at 33 kg per 290 W electric → 8.8 W/kg
    pu_electrical_specific_W_per_kg_theory = 0.063 * 540.0
    pu_electrical_specific_W_per_kg_flown = 290.0 / 33.0
    us_production_kg_per_yr = 1.5  # DOE target rate ~2026 onward
    us_inventory_kg = 35.0  # cumulative as of ~2020
    cells = []
    for p_kwe in power_kwe_targets:
        pu_mass_kg_theory = p_kwe * 1000.0 / pu_electrical_specific_W_per_kg_theory
        pu_mass_kg_flown = p_kwe * 1000.0 / pu_electrical_specific_W_per_kg_flown
        cells.append({
            "power_kwe": p_kwe,
            "pu_mass_kg_theory_stirling": pu_mass_kg_theory,
            "pu_mass_kg_flown_mmrtg": pu_mass_kg_flown,
            "production_years_for_one_mission_theory": pu_mass_kg_theory / us_production_kg_per_yr,
            "production_years_for_one_mission_flown": pu_mass_kg_flown / us_production_kg_per_yr,
            "ratio_to_us_inventory_theory": pu_mass_kg_theory / us_inventory_kg,
            "ratio_to_us_inventory_flown": pu_mass_kg_flown / us_inventory_kg,
            "feasible_single_mission": pu_mass_kg_theory <= us_inventory_kg,
        })
    return {
        "architecture": "C",
        "us_production_kg_per_yr": us_production_kg_per_yr,
        "us_inventory_kg": us_inventory_kg,
        "pu_electrical_specific_W_per_kg_theory": pu_electrical_specific_W_per_kg_theory,
        "pu_electrical_specific_W_per_kg_flown": pu_electrical_specific_W_per_kg_flown,
        "cells": cells,
    }


# ---------------- Bayesian posteriors on combined-criteria closure ---------------- #

def bayesian_posteriors(structural_failure_counts: dict) -> dict:
    """Three priors; likelihood = product of (1 − p_failure) over architectures
    where p_failure is read from structural_failure_counts. Posterior reported as
    the prior's mean updated against the architecture-failure evidence.

    structural_failure_counts: dict with keys 'A', 'B', 'C' giving the count of
    failed pre-registered criteria (out of 4: L0-05, L0-09, L0-12, supply).
    """
    priors = [
        ("Beta(2,2) symmetric", 2.0, 2.0),
        ("Beta(1,4) mild skeptic", 1.0, 4.0),
        ("Beta(1,9) strong skeptic", 1.0, 9.0),
    ]
    # Likelihood treatment: each architecture's failed-count out of 4 is
    # treated as a Binomial(4, p_fail) observation, with p_fail = 1 − p_close.
    # Combine: total trials = 12 (4 criteria × 3 architectures); successes =
    # 12 − sum(failures).
    total_trials = 4 * 3
    successes = total_trials - sum(structural_failure_counts.values())
    out = []
    for name, alpha, beta in priors:
        post_alpha = alpha + successes
        post_beta = beta + (total_trials - successes)
        mean = post_alpha / (post_alpha + post_beta)
        out.append({
            "prior": name,
            "alpha_prior": alpha,
            "beta_prior": beta,
            "alpha_post": post_alpha,
            "beta_post": post_beta,
            "posterior_mean": mean,
            "successes": successes,
            "trials": total_trials,
        })
    return {
        "structural_failure_counts": structural_failure_counts,
        "priors": out,
    }


# ---------------- main: run all architectures and write outputs ---------------- #

def main() -> None:
    out_dir = Path(__file__).parent / "results"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Architecture A — sweep SEP power (200 kWe → 2 MWe), Saturn-side RTG mass
    # (proxy for inbound option), and vehicle dry mass. Inbound at Isp 450 s
    # (hydrolox onsite); Isp 200 s (water-steam) gives infeasible delivered
    # mass at any reasonable vehicle dry, so omitted from the main sweep.
    A_results = []
    for sep_kwe in (200.0, 500.0, 1000.0, 2000.0):
        for saturn_rtg in (0.0, 5.0):
            for vehicle_dry in (15.0, 25.0):
                A_results.append(architecture_A(
                    vehicle_dry_t=vehicle_dry,
                    chunk_t=200.0,
                    sep_kwe=sep_kwe,
                    sep_array_kg_per_kw=5.0,
                    saturn_side_rtg_t=saturn_rtg,
                    inbound_isp_s=450.0,
                    kick_n_stages=2,
                ))
    # Also test Isp-200 (water-steam) at a single midrange config for completeness.
    A_results.append(architecture_A(
        vehicle_dry_t=15.0, chunk_t=200.0, sep_kwe=1000.0,
        sep_array_kg_per_kw=5.0, saturn_side_rtg_t=0.0,
        inbound_isp_s=200.0, kick_n_stages=2,
    ))

    # Architecture B — sweep Saturn-side RTG mass to see how much is needed for
    # the electrolysis energy budget to close.
    B_results = []
    for inbound_isp in (200.0, 450.0):
        for vehicle_dry in (10.0, 15.0, 20.0):
            for rtg_t in (0.0, 5.0, 30.0):
                B_results.append(architecture_B(
                    vehicle_dry_t=vehicle_dry,
                    chunk_t=200.0,
                    saturn_side_rtg_t=rtg_t,
                    inbound_isp_s=inbound_isp,
                    outbound_n_stages=2,
                ))

    # Architecture C — supply analysis at a sweep of power targets.
    C_results = architecture_C(power_kwe_targets=[1.0, 10.0, 40.0, 100.0, 1000.0])

    # Bayesian posteriors — failure counts per architecture, against pre-
    # registered criteria L0-05, L0-09, L0-12, supply.
    # Architecture A: bust L0-05 (per pre-reg), L0-09 cadence (per pre-reg),
    #   L0-12 (per pre-reg launch-mass multiplier), supply OK = 3 failures.
    # Architecture B: L0-05 OK (cruise time = 13.16 yr), L0-09 cadence at risk,
    #   L0-12 (per pre-reg 30-50x multiplier), supply OK = 2 failures.
    # Architecture C: L0-05 OK in principle, L0-09 OK, L0-12 yes, supply yes = 4 failures.
    # These are pre-registration expectations; will be re-counted post-run.
    failure_counts_pre = {"A": 3, "B": 2, "C": 4}
    bayes_pre = bayesian_posteriors(failure_counts_pre)

    # Post-run failure counts will be computed in the Result section of STUDY.md
    # based on actual numbers; here we just emit the pre-registration baseline.

    (out_dir / "architecture_A.json").write_text(json.dumps(A_results, indent=2))
    (out_dir / "architecture_B.json").write_text(json.dumps(B_results, indent=2))
    (out_dir / "architecture_C.json").write_text(json.dumps(C_results, indent=2))
    (out_dir / "bayesian_posteriors.json").write_text(json.dumps(bayes_pre, indent=2))

    # Human-readable summary.
    lines = []
    lines.append("# R-non-fission-baseline — results tables\n")
    lines.append("## Shared physics\n")
    lines.append(f"- Hohmann cruise (one-way): {hohmann_cruise_yr():.3f} yr")
    lines.append(f"- Edelbaum spiral integrated dv (low Earth orbit → escape): {edelbaum_spiral_dv_km_s():.3f} km/s")
    lines.append(f"- Heliocentric v_inf (Earth → Saturn Hohmann): {heliocentric_v_inf_earth_km_s():.3f} km/s")
    lines.append(f"- Chemical impulsive outbound from LEO (Oberth-credited): {chemical_impulsive_outbound_dv_km_s():.3f} km/s")
    lines.append(f"- Inbound delta-velocity (post-Lunar-Gravity-Assist residual): {DV_INBOUND_KM_S} km/s")
    lines.append("")
    lines.append("## Architecture A — solar-electric + chemical kick + chunk-fed chemical inbound\n")
    lines.append("| SEP (kWe) | vehicle dry (t) | Saturn RTG (t) | inbound Isp (s) | SEP burn (yr) | m_LEO wet (t) | delivered water (t) | round-trip (yr) | closes L0-05 | launch/delivered | Saturn energy ratio | closes energy |")
    lines.append("|---:|---:|---:|---:|---:|---:|---:|---:|:---:|---:|---:|:---:|")
    for r in A_results:
        if not r["feasible"]:
            lines.append(f"| — | {r.get('vehicle_dry_t','?')} | {r.get('saturn_side_rtg_t','?')} | {r.get('inbound_isp_s','?')} | — | infeasible | {r.get('delivered_water_t', float('nan')):.2f} | — | — | — | — | — |")
        else:
            e = r.get("saturn_side_energy")
            if e is None:
                e_ratio = "—"
                e_closes = "—"
            else:
                e_ratio = f"{e['energy_supply_ratio']:.3g}"
                e_closes = "yes" if e["closes_energy_budget"] else "no"
            lines.append(
                f"| {r['sep_kwe']:.0f} | {r['vehicle_dry_t']:.0f} | {r['saturn_side_rtg_t']:.1f} | {r['inbound_isp_s']:.0f} | "
                f"{r['sep_burn_yr']:.2f} | {r['m_LEO_wet_t']:.1f} | {r['delivered_water_t']:.2f} | "
                f"{r['round_trip_yr']:.2f} | {'yes' if r['closes_L0_05'] else 'no'} | "
                f"{r['launch_per_delivered_ratio']:.1f} | {e_ratio} | {e_closes} |"
            )
    lines.append("")
    lines.append("## Architecture B — all-chemical end-to-end\n")
    lines.append("| vehicle dry (t) | Saturn RTG (t) | inbound Isp (s) | m_LEO wet (t) | delivered water (t) | round-trip (yr) | launch/delivered | Saturn energy ratio | closes energy |")
    lines.append("|---:|---:|---:|---:|---:|---:|---:|---:|:---:|")
    for r in B_results:
        if not r["feasible"]:
            lines.append(f"| {r.get('vehicle_dry_t','?')} | {r.get('saturn_side_rtg_t','?')} | {r.get('inbound_isp_s','?')} | infeasible | {r.get('delivered_water_t', float('nan')):.2f} | — | — | — | — |")
        else:
            e = r.get("saturn_side_energy")
            if e is None:
                e_ratio = "—"
                e_closes = "—"
            else:
                e_ratio = f"{e['energy_supply_ratio']:.3g}"
                e_closes = "yes" if e["closes_energy_budget"] else "no"
            lines.append(
                f"| {r['vehicle_dry_t']:.0f} | {r['saturn_side_rtg_t']:.1f} | {r['inbound_isp_s']:.0f} | "
                f"{r['m_LEO_wet_t']:.1f} | {r['delivered_water_t']:.2f} | "
                f"{r['round_trip_yr']:.2f} | {r['launch_per_delivered_ratio']:.1f} | "
                f"{e_ratio} | {e_closes} |"
            )
    lines.append("")
    lines.append("## Architecture C — plutonium-238 radioisotope-electric supply table\n")
    lines.append(f"- US production rate: {C_results['us_production_kg_per_yr']} kg/yr")
    lines.append(f"- US inventory ~2020: {C_results['us_inventory_kg']} kg")
    lines.append(f"- Pu-238 electrical specific power (theoretical Stirling 6.3%): {C_results['pu_electrical_specific_W_per_kg_theory']:.2f} W/kg")
    lines.append(f"- Pu-238 electrical specific power (flown MMRTG): {C_results['pu_electrical_specific_W_per_kg_flown']:.2f} W/kg")
    lines.append("")
    lines.append("| power (kWe) | Pu-238 mass theory (kg) | Pu-238 mass flown (kg) | years US production theory | years US production flown | × US inventory theory | feasible single-mission |")
    lines.append("|---:|---:|---:|---:|---:|---:|:---:|")
    for c in C_results["cells"]:
        lines.append(
            f"| {c['power_kwe']:.0f} | {c['pu_mass_kg_theory_stirling']:.1f} | {c['pu_mass_kg_flown_mmrtg']:.1f} | "
            f"{c['production_years_for_one_mission_theory']:.1f} | {c['production_years_for_one_mission_flown']:.1f} | "
            f"{c['ratio_to_us_inventory_theory']:.2f} | {'yes' if c['feasible_single_mission'] else 'no'} |"
        )
    lines.append("")
    lines.append("## Bayesian posteriors — probability that *some* non-fission architecture closes L0-05 + L0-09 + L0-12 + supply\n")
    lines.append("(pre-registration failure counts: A=3/4, B=2/4, C=4/4)\n")
    lines.append("| prior | α_post | β_post | posterior mean |")
    lines.append("|---|---:|---:|---:|")
    for p in bayes_pre["priors"]:
        lines.append(f"| {p['prior']} | {p['alpha_post']:.1f} | {p['beta_post']:.1f} | {p['posterior_mean']:.3f} |")
    lines.append("")

    (out_dir / "tables.md").write_text("\n".join(lines))
    print("Wrote:")
    for p in ("architecture_A.json", "architecture_B.json", "architecture_C.json", "bayesian_posteriors.json", "tables.md"):
        print(f"  results/{p}")


if __name__ == "__main__":
    main()
