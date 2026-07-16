"""R-chemical-plus-small-reactor — does small-reactor-for-process-power-only
close the matrix?

Architecture D = chemical propulsion end-to-end (Architecture B physics from
R_non_fission_baseline) + Saturn-side fission reactor at 40-150 kilowatts-
electric used purely for inbound-propellant electrolysis. Sweep reactor
specific power (KRUSTY 2.4, FSP-projected 5, FSP-stretch 10, aspirational 40
W/kg) × reactor mass (10, 20, 30, 50, 70 tonnes).

Reuses physics helpers in spirit from R_non_fission_baseline/run.py
(constant-thrust burn, hohmann_cruise_yr, staged_chemical_burn,
saturn_side_energy_budget). Reimplemented inline rather than imported to keep
the round self-contained and reproducible.

Outputs:
    results/architecture_D.json
    results/posteriors.json
    results/tables.md
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
DV_INBOUND_KM_S = 6.42
SATURN_OPS_YR = 1.0
L0_05_CEILING_YR = 15.0
ELECTROLYSIS_KWH_PER_KG = 8.0  # alkaline electrolysis + cryogenic liquefaction
ELECTROLYSIS_PLANT_T = 5.0  # fixed dry-mass overhead for the plant


# ---------------- physics helpers ---------------- #

def hohmann_cruise_yr() -> float:
    a_h_km = (A_EARTH + A_SATURN) / 2.0
    return math.pi * math.sqrt(a_h_km ** 3 / GM_SUN) / YEAR_S


def v_circ_leo() -> float:
    return math.sqrt(GM_EARTH / (R_EARTH + LEO_ALT_KM))


def heliocentric_v_inf_earth_km_s() -> float:
    v_earth = math.sqrt(GM_SUN / A_EARTH)
    a_h = (A_EARTH + A_SATURN) / 2.0
    v_peri = math.sqrt(GM_SUN * (2.0 / A_EARTH - 1.0 / a_h))
    return v_peri - v_earth


def chemical_impulsive_outbound_dv_km_s() -> float:
    v_c = v_circ_leo()
    v_e = math.sqrt(2.0) * v_c
    v_inf = heliocentric_v_inf_earth_km_s()
    return math.sqrt(v_e ** 2 + v_inf ** 2) - v_c


def staged_chemical_burn(m_payload_t: float, dv_km_s: float, isp_s: float,
                         n_stages: int, stage_dry_wet: float = 0.10) -> dict:
    dv_per_stage = dv_km_s / n_stages
    v_e = isp_s * G0
    mr_per_stage = math.exp(dv_per_stage * 1000.0 / v_e)
    m_above = m_payload_t
    total_dry, total_prop = 0.0, 0.0
    for _ in range(n_stages):
        k = (1.0 - stage_dry_wet) / stage_dry_wet
        M = mr_per_stage - 1.0
        if M >= k:
            return {"feasible": False,
                    "reason": f"single-stage MR {mr_per_stage:.2f} infeasible at dry/wet {stage_dry_wet} (n_stages={n_stages})"}
        m_stage_dry = M * m_above / (k - M)
        m_stage_prop = k * m_stage_dry
        m_above += m_stage_dry + m_stage_prop
        total_dry += m_stage_dry
        total_prop += m_stage_prop
    return {
        "feasible": True,
        "n_stages": n_stages,
        "dv_per_stage_km_s": dv_per_stage,
        "mr_per_stage": mr_per_stage,
        "m_payload_t": m_payload_t,
        "m_total_stage_dry_t": total_dry,
        "m_total_stage_prop_t": total_prop,
        "m_LEO_wet_t": m_above,
    }


def saturn_energy_budget(propellant_water_t: float, p_kwe: float,
                         ops_yr: float = SATURN_OPS_YR) -> dict:
    energy_needed_kwh = propellant_water_t * 1000.0 * ELECTROLYSIS_KWH_PER_KG
    available_kwh = p_kwe * ops_yr * 24.0 * 365.25
    ratio = available_kwh / energy_needed_kwh if energy_needed_kwh > 0 else float("inf")
    return {
        "propellant_water_t": propellant_water_t,
        "energy_needed_kwh": energy_needed_kwh,
        "p_kwe": p_kwe,
        "available_kwh": available_kwh,
        "energy_supply_ratio": ratio,
        "closes_energy_budget": ratio >= 1.0,
    }


# ---------------- Architecture D ---------------- #

def architecture_D(
    vehicle_dry_t: float = 10.0,
    chunk_t: float = 200.0,
    reactor_mass_t: float = 20.0,
    reactor_specific_power_w_per_kg: float = 5.0,
    inbound_isp_s: float = 450.0,
    outbound_n_stages: int = 2,
    electrolysis_plant_t: float = ELECTROLYSIS_PLANT_T,
) -> dict:
    dv_out = chemical_impulsive_outbound_dv_km_s()
    cruise = hohmann_cruise_yr()

    p_kwe = reactor_mass_t * 1000.0 * reactor_specific_power_w_per_kg / 1000.0
    # That simplifies to reactor_mass_t * reactor_specific_power_w_per_kg.

    # Inbound: chunk-fed chemical. The reactor + electrolysis plant + vehicle
    # are the "dry-payload-returning" mass; chunk is propellant tank.
    dry_payload_returning_t = vehicle_dry_t + reactor_mass_t + electrolysis_plant_t
    v_e_in = inbound_isp_s * G0
    mr_in = math.exp(DV_INBOUND_KM_S * 1000.0 / v_e_in)
    delivered_water_t = chunk_t / mr_in - dry_payload_returning_t * (1.0 - 1.0 / mr_in)
    inbound_prop_t = chunk_t - delivered_water_t

    if delivered_water_t <= 0.0:
        # The dry-payload-returning mass exceeds the chunk's ability to push it
        # back at the chosen specific impulse. Architecture D collapses here.
        outbound = staged_chemical_burn(dry_payload_returning_t, dv_out, 450.0, outbound_n_stages)
        return {
            "architecture": "D",
            "feasible": False,
            "reason": "chunk-fed inbound under-delivers; dry-payload-returning exceeds chunk pushing capacity",
            "vehicle_dry_t": vehicle_dry_t,
            "reactor_mass_t": reactor_mass_t,
            "reactor_specific_power_w_per_kg": reactor_specific_power_w_per_kg,
            "p_kwe": p_kwe,
            "delivered_water_t": delivered_water_t,
            "inbound_prop_t_would_be": chunk_t,
            "outbound_for_reference": outbound,
        }

    # Outbound: chemical stack pushes (vehicle + reactor + electrolysis plant).
    payload_at_escape = dry_payload_returning_t
    outbound = staged_chemical_burn(payload_at_escape, dv_out, 450.0, outbound_n_stages)
    if not outbound["feasible"]:
        return {
            "architecture": "D",
            "feasible": False,
            "reason": f"outbound chemical stack infeasible: {outbound.get('reason')}",
            "outbound": outbound,
        }
    m_LEO_t = outbound["m_LEO_wet_t"]

    # Round-trip: instant outbound burn, Hohmann, ops, instant inbound burn,
    # Hohmann (impulsive chemical → burn time << year).
    round_trip_yr = cruise + SATURN_OPS_YR + cruise
    closes_L0_05 = round_trip_yr <= L0_05_CEILING_YR

    # Saturn-side energy budget.
    energy = saturn_energy_budget(propellant_water_t=inbound_prop_t, p_kwe=p_kwe,
                                  ops_yr=SATURN_OPS_YR)

    return {
        "architecture": "D",
        "feasible": True,
        "vehicle_dry_t": vehicle_dry_t,
        "chunk_t": chunk_t,
        "reactor_mass_t": reactor_mass_t,
        "reactor_specific_power_w_per_kg": reactor_specific_power_w_per_kg,
        "p_kwe": p_kwe,
        "electrolysis_plant_t": electrolysis_plant_t,
        "inbound_isp_s": inbound_isp_s,
        "dv_outbound_km_s": dv_out,
        "outbound_n_stages": outbound_n_stages,
        "outbound_stage_total_dry_t": outbound["m_total_stage_dry_t"],
        "outbound_stage_total_prop_t": outbound["m_total_stage_prop_t"],
        "m_LEO_wet_t": m_LEO_t,
        "delivered_water_t": delivered_water_t,
        "inbound_prop_t": inbound_prop_t,
        "mr_inbound": mr_in,
        "round_trip_yr": round_trip_yr,
        "closes_L0_05": closes_L0_05,
        "launch_per_delivered_ratio": m_LEO_t / delivered_water_t,
        "saturn_side_energy": energy,
        "closes_all_criteria": closes_L0_05 and energy["closes_energy_budget"],
    }


# ---------------- Bayesian posterior — Architecture D delivery by 2035 ---------------- #

def posteriors() -> dict:
    """Three weakly-informative priors with KRUSTY/FSP Phase-1 evidence
    adjustments. Beta-distribution posterior means.

    Base prior reflects the 0-of-6 US space-fission base rate but allows for
    a non-zero success probability. Adjustments add:
      - KRUSTY ground demo as a partial-credit pseudo-success (weight 0.5 of
        an orbital success).
      - FSP Phase 1 active contracts as a +1 partial success conditional on
        Phase 2 being awarded. We model this conditionally: if FSP Phase 2 is
        awarded (probability p_phase2 ≈ 0.5–0.7 per locked beliefs about
        scope growth + funding ambiguity), then Phase 1 active contracts
        contribute +1 conditional success.
    """
    base_alpha, base_beta = 2.0, 4.0  # base symmetric-pessimistic prior
    krusty_credit = 0.5
    fsp_phase1_credit = 1.0
    p_phase2_award = 0.6  # from locked-beliefs reading

    priors = []

    # Prior A: base only (no KRUSTY, no FSP).
    a_A, b_A = base_alpha + 0.0, base_beta + 6.0  # 0-of-6 historical
    priors.append({
        "name": "Prior A (no KRUSTY, no FSP credit)",
        "alpha_post": a_A,
        "beta_post": b_A,
        "posterior_mean": a_A / (a_A + b_A),
    })

    # Prior B: + KRUSTY half-credit.
    a_B, b_B = base_alpha + krusty_credit, base_beta + 6.0 - krusty_credit
    priors.append({
        "name": "Prior B (+ KRUSTY half-credit ground demo)",
        "alpha_post": a_B,
        "beta_post": b_B,
        "posterior_mean": a_B / (a_B + b_B),
    })

    # Prior C: + KRUSTY half-credit + FSP Phase 1 active credit (probabilistic).
    a_C = base_alpha + krusty_credit + fsp_phase1_credit * p_phase2_award
    b_C = base_beta + 6.0 - krusty_credit - fsp_phase1_credit * p_phase2_award
    priors.append({
        "name": "Prior C (+ KRUSTY + FSP-Phase-1 conditional)",
        "alpha_post": a_C,
        "beta_post": b_C,
        "posterior_mean": a_C / (a_C + b_C),
    })

    return {
        "base_prior": f"Beta({base_alpha}, {base_beta})",
        "us_fission_base_rate": "0 of 6 orbital since 1965",
        "krusty_credit_weight": krusty_credit,
        "fsp_phase1_credit_weight": fsp_phase1_credit,
        "p_phase2_award_assumed": p_phase2_award,
        "priors": priors,
    }


# ---------------- main: sweep + write outputs ---------------- #

def main() -> None:
    out_dir = Path(__file__).parent / "results"
    out_dir.mkdir(parents=True, exist_ok=True)

    D_results = []
    for s_pwr in (2.4, 5.0, 10.0, 40.0):
        for reactor_mass in (10.0, 20.0, 30.0, 50.0, 70.0):
            for vehicle_dry in (10.0, 15.0):
                D_results.append(architecture_D(
                    vehicle_dry_t=vehicle_dry,
                    chunk_t=200.0,
                    reactor_mass_t=reactor_mass,
                    reactor_specific_power_w_per_kg=s_pwr,
                    inbound_isp_s=450.0,
                    outbound_n_stages=2,
                ))

    post = posteriors()

    (out_dir / "architecture_D.json").write_text(json.dumps(D_results, indent=2))
    (out_dir / "posteriors.json").write_text(json.dumps(post, indent=2))

    # Tables.
    lines = []
    lines.append("# R-chemical-plus-small-reactor — results tables\n")
    lines.append("## Shared physics\n")
    lines.append(f"- Hohmann cruise (one-way): {hohmann_cruise_yr():.3f} yr")
    lines.append(f"- Chemical impulsive outbound from low Earth orbit (Oberth-credited): "
                 f"{chemical_impulsive_outbound_dv_km_s():.3f} km/s")
    lines.append(f"- Round-trip baseline (Hohmann × 2 + 1 yr ops, impulsive burns): "
                 f"{2 * hohmann_cruise_yr() + SATURN_OPS_YR:.3f} yr")
    lines.append(f"- Electrolysis energy cost: {ELECTROLYSIS_KWH_PER_KG} kWh/kg of water")
    lines.append(f"- Electrolysis plant fixed mass: {ELECTROLYSIS_PLANT_T} t")
    lines.append("")
    lines.append("## Architecture D — chemical propulsion + Saturn-side reactor for process power only\n")
    lines.append("| reactor mass (t) | spec power (W/kg) | reactor P_kWe | vehicle dry (t) | m_LEO wet (t) | delivered (t) | round-trip (yr) | closes L0-05 | launch/delivered | Saturn energy ratio | closes energy | closes all |")
    lines.append("|---:|---:|---:|---:|---:|---:|---:|:---:|---:|---:|:---:|:---:|")
    for r in D_results:
        if not r["feasible"]:
            lines.append(
                f"| {r.get('reactor_mass_t','?')} | {r.get('reactor_specific_power_w_per_kg','?')} | "
                f"{r.get('p_kwe', float('nan')):.1f} | {r.get('vehicle_dry_t','?')} | "
                f"infeasible | {r.get('delivered_water_t', float('nan')):.2f} | — | — | — | — | — | — |"
            )
        else:
            e = r["saturn_side_energy"]
            lines.append(
                f"| {r['reactor_mass_t']:.0f} | {r['reactor_specific_power_w_per_kg']:.1f} | "
                f"{r['p_kwe']:.1f} | {r['vehicle_dry_t']:.0f} | "
                f"{r['m_LEO_wet_t']:.1f} | {r['delivered_water_t']:.2f} | "
                f"{r['round_trip_yr']:.2f} | {'yes' if r['closes_L0_05'] else 'no'} | "
                f"{r['launch_per_delivered_ratio']:.2f} | "
                f"{e['energy_supply_ratio']:.3g} | {'yes' if e['closes_energy_budget'] else 'no'} | "
                f"{'**YES**' if r['closes_all_criteria'] else 'no'} |"
            )
    lines.append("")
    lines.append("## Bayesian posteriors — Architecture D delivery by 2035\n")
    lines.append(f"- Base US space-fission rate: {post['us_fission_base_rate']}")
    lines.append(f"- Base prior: {post['base_prior']}")
    lines.append(f"- KRUSTY ground-demo credit weight: {post['krusty_credit_weight']}")
    lines.append(f"- Fission Surface Power Phase 1 active-contracts credit weight: {post['fsp_phase1_credit_weight']}")
    lines.append(f"- Probability Fission Surface Power Phase 2 award (locked-beliefs reading): {post['p_phase2_award_assumed']}")
    lines.append("")
    lines.append("| prior | α_post | β_post | posterior mean |")
    lines.append("|---|---:|---:|---:|")
    for p in post["priors"]:
        lines.append(f"| {p['name']} | {p['alpha_post']:.2f} | {p['beta_post']:.2f} | {p['posterior_mean']:.3f} |")
    lines.append("")

    (out_dir / "tables.md").write_text("\n".join(lines))

    print("Wrote:")
    for p in ("architecture_D.json", "posteriors.json", "tables.md"):
        print(f"  results/{p}")


if __name__ == "__main__":
    main()
