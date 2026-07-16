"""R-architecture-E-no-saturn-side-electrolysis

Does dropping Saturn-side electrolysis open a higher-credibility deployment
path than the surviving 500-kilowatt-electric chemical-kick cell?

Architecture E: pure all-electric end-to-end, no electrolysis anywhere,
chunk water consumed directly as electric-thruster propellant inbound,
sub-megawatt reactor on-ship for thrust only.

Reuses rhea's MARVL-anchored mass model and corrected continuous-thrust
delta-velocities. Adds: Bayesian posterior cascade comparison, cadence/fleet
analysis, simple net-present-value sketch.

Pre-registration in STUDY.md.
"""

from __future__ import annotations

import json
import math
import random
from pathlib import Path
from statistics import median

from waterprop.constants import A_EARTH, A_SATURN, G0, GM_SUN

YEAR_S = 365.25 * 86400.0

# Operational constants (match rhea)
ETA_THR = 0.65
SATURN_OPS_YR = 1.0
ROUND_TRIP_CEILING_STRICT_YR = 15.0
ROUND_TRIP_CEILING_RELAXED_20_YR = 20.0
ROUND_TRIP_CEILING_RELAXED_25_YR = 25.0
ROUND_TRIP_CEILING_RELAXED_30_YR = 30.0

# Delta-velocities (corrected, per rhea)
DV_OUTBOUND_HE_NO_LGA_KM_S = 29.56
DV_INBOUND_TITAN_HE_LGA_KM_S = 24.7

# Sweep axes
REACTOR_POWERS_KWE = [40.0, 100.0, 200.0, 500.0, 1000.0]
CHUNK_MASSES_T = [30.0, 50.0, 100.0, 200.0]
ISP_VALUES_S = [1500.0, 2000.0, 2934.0]

# Mass models — copied from rhea's R_megawatt_marvl_radiator
MASS_MODELS: dict[str, dict] = {
    "decomposed_marvl": {
        "kind": "decomposed",
        "m_fixed_t": 5.0,
        "alpha_reactor_W_per_kg": 33.0,
        "alpha_PC_W_per_kg": 50.0,
        "alpha_radiator_kW_th_per_kg": 0.047,
        "eta_conv": 0.30,
        "f_tank": 0.05,
    },
    "bundled_10_W_per_kg": {
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
    return model["m_fixed_t"] + m_reactor + m_pc + m_rad + m_tank


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


def round_trip_E(model, reactor_kwe, chunk_t, isp_s,
                 dv_outbound_km_s=DV_OUTBOUND_HE_NO_LGA_KM_S,
                 dv_inbound_km_s=DV_INBOUND_TITAN_HE_LGA_KM_S):
    """Architecture E: pure all-electric end-to-end. Self-consistent outbound mass iteration."""
    m_tug_t = dry_mass_t(model, reactor_kwe, m_prop_t=0.0)
    converged = False
    for _ in range(40):
        burn_out = burn_from_dry_end(m_tug_t, dv_outbound_km_s, reactor_kwe, isp_s)
        new_m_tug = dry_mass_t(model, reactor_kwe, m_prop_t=burn_out["m_prop_t"])
        if abs(new_m_tug - m_tug_t) < 1e-4:
            m_tug_t = new_m_tug
            converged = True
            break
        m_tug_t = new_m_tug
    if not converged:
        return {
            "feasible": False,
            "m_tug_t": m_tug_t,
            "round_trip_yr": math.inf,
            "closes_15yr": False,
            "closes_20yr": False,
            "closes_25yr": False,
            "closes_30yr": False,
            "delivered_t": -math.inf,
            "delivered_fraction": -math.inf,
            "t_outbound_burn_yr": math.inf,
            "t_inbound_burn_yr": math.inf,
            "m_prop_outbound_t": math.inf,
            "m_prop_inbound_t": math.inf,
            "note": "tug-mass iteration did not converge",
        }
    burn_out = burn_from_dry_end(m_tug_t, dv_outbound_km_s, reactor_kwe, isp_s)
    # Inbound: chunk water = propellant. Wet mass at Saturn-departure = tug + chunk.
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
        "closes_15yr": round_trip_yr <= ROUND_TRIP_CEILING_STRICT_YR,
        "closes_20yr": round_trip_yr <= ROUND_TRIP_CEILING_RELAXED_20_YR,
        "closes_25yr": round_trip_yr <= ROUND_TRIP_CEILING_RELAXED_25_YR,
        "closes_30yr": round_trip_yr <= ROUND_TRIP_CEILING_RELAXED_30_YR,
        "delivered_t": delivered_t,
        "delivered_fraction": delivered_t / chunk_t if chunk_t > 0 else 0.0,
    }


# ---- Bayesian posterior cascade ----
# Uniform distribution sampling on (lo, hi). Each draw is the *credibility* (probability of success)
# for that subsystem. Unconditional posterior = product across draws.
def sample_uniform(lo: float, hi: float) -> float:
    return lo + (hi - lo) * random.random()


def cascade_E(reactor_kwe: float) -> float:
    # Reactor: lower scope than Variant B's 5× FSP. At 100-200 kWe, this is FSP Phase 2 baseline.
    # At 500 kWe, this is Variant B's level (5× FSP). At 1000 kWe, megawatt-class (rhea falsified
    # but include for sweep symmetry).
    if reactor_kwe <= 100.0:
        p_reactor = sample_uniform(0.30, 0.50)  # FSP Phase 2 nominal
    elif reactor_kwe <= 200.0:
        p_reactor = sample_uniform(0.20, 0.40)  # 2× FSP scope
    elif reactor_kwe <= 500.0:
        p_reactor = sample_uniform(0.10, 0.30)  # 5× FSP scope, matches Variant B
    else:
        p_reactor = sample_uniform(0.03, 0.10)  # megawatt; per matrix line 21, no defensible path

    # No Saturn-side process power factor (Architecture E has none).
    # No electrolyzer factor.
    # No cryostorage factor.

    p_water_electric = sample_uniform(0.25, 0.55)  # water-fed electric, ≥5-year cathode life on chunk water
    p_bag = sample_uniform(0.45, 0.75)
    p_rest = sample_uniform(0.55, 0.85)
    return p_reactor * p_water_electric * p_bag * p_rest


def cascade_variantB(reactor_kwe: float = 500.0) -> float:
    # Variant B as defined in matrix line 66: 500-kWe chemical-kick + electric-inbound.
    # Reactor scope = 5× FSP.
    p_reactor = sample_uniform(0.10, 0.30)
    p_electrolyzer = sample_uniform(0.25, 0.55)  # 200-kWe-class electrolyzer on chunk water, space-qualified
    p_cryo = sample_uniform(0.35, 0.65)  # 1-year H2/O2 storage at Saturn
    p_water_electric = sample_uniform(0.25, 0.55)
    p_bag = sample_uniform(0.45, 0.75)
    p_rest = sample_uniform(0.55, 0.85)
    return p_reactor * p_electrolyzer * p_cryo * p_water_electric * p_bag * p_rest


def cascade_D_fission() -> float:
    # Per round-5 cascade structure: Saturn-side fission + electrolysis + cryo + rest.
    p_reactor = sample_uniform(0.10, 0.30)  # FSP Phase 2 + scale to Saturn-side
    p_saturn_fission = sample_uniform(0.02, 0.08)  # Saturn-side fission (cascade factor from round 5)
    p_electrolyzer = sample_uniform(0.25, 0.55)
    p_cryo = sample_uniform(0.35, 0.65)
    p_water_electric = sample_uniform(0.25, 0.55)
    p_bag = sample_uniform(0.45, 0.75)
    p_rest = sample_uniform(0.55, 0.85)
    return p_reactor * p_saturn_fission * p_electrolyzer * p_cryo * p_water_electric * p_bag * p_rest


def cascade_D_solar_thermal() -> float:
    p_reactor = sample_uniform(0.10, 0.30)  # on-ship reactor (electric inbound still needs power)
    p_saturn_solar_thermal = sample_uniform(0.05, 0.15)  # large deployable mirror at Saturn (cascade factor from round 5)
    p_electrolyzer = sample_uniform(0.25, 0.55)
    p_cryo = sample_uniform(0.35, 0.65)
    p_water_electric = sample_uniform(0.25, 0.55)
    p_bag = sample_uniform(0.45, 0.75)
    p_rest = sample_uniform(0.55, 0.85)
    return p_reactor * p_saturn_solar_thermal * p_electrolyzer * p_cryo * p_water_electric * p_bag * p_rest


def monte_carlo(cascade_fn, n_samples: int = 50000, *args) -> dict:
    samples = sorted(cascade_fn(*args) for _ in range(n_samples))
    return {
        "median": samples[n_samples // 2],
        "p05": samples[int(n_samples * 0.05)],
        "p95": samples[int(n_samples * 0.95)],
        "mean": sum(samples) / n_samples,
    }


# ---- Cadence / fleet / net-present-value sketch ----
def fleet_capital(cadence_per_yr: float, round_trip_yr: float, per_vehicle_cost_M: float) -> float:
    """Steady-state fleet size in cruise = cadence × round-trip. Returns total fleet capital in $M."""
    fleet_size = cadence_per_yr * round_trip_yr
    return fleet_size * per_vehicle_cost_M


def npv_simple(
    cadence_per_yr: float,
    round_trip_yr: float,
    revenue_per_mission_M: float,
    fleet_capital_M: float,
    wacc: float = 0.087,
    horizon_yr: int = 40,
) -> dict:
    """Very simple NPV: fleet capital is upfront, revenue starts at first delivery (round_trip_yr),
    then steady cadence for the remaining horizon. Per-mission operating cost ignored (it's small
    relative to capital + finance cost at WACC=8.7% over 40 yr)."""
    # Fleet capital upfront
    pv_capital = -fleet_capital_M
    # Revenue stream: starts at year round_trip_yr, ends at year horizon_yr
    pv_revenue = 0.0
    annual_revenue = revenue_per_mission_M * cadence_per_yr
    for yr in range(int(math.ceil(round_trip_yr)), horizon_yr + 1):
        pv_revenue += annual_revenue / (1.0 + wacc) ** yr
    return {
        "pv_capital_M": pv_capital,
        "pv_revenue_M": pv_revenue,
        "npv_M": pv_capital + pv_revenue,
        "fleet_size": cadence_per_yr * round_trip_yr,
    }


def main() -> dict:
    random.seed(20260515)
    results: dict = {}

    # 1. Architecture E sweep — all reactor × chunk × Isp × mass-model cells
    sweep = []
    for mass_model_name, model in MASS_MODELS.items():
        for reactor in REACTOR_POWERS_KWE:
            for chunk in CHUNK_MASSES_T:
                for isp in ISP_VALUES_S:
                    row = round_trip_E(model, reactor, chunk, isp)
                    row.update({
                        "mass_model": mass_model_name,
                        "reactor_kwe": reactor,
                        "chunk_t": chunk,
                        "isp_s": isp,
                    })
                    sweep.append(row)
    results["sweep_architecture_E"] = sweep

    # 2. Identify closure cells at each L0-05 relaxation level
    cells_15 = [r for r in sweep if r.get("feasible") and r["closes_15yr"] and r["delivered_t"] > 0]
    cells_20 = [r for r in sweep if r.get("feasible") and r["closes_20yr"] and r["delivered_t"] > 0]
    cells_25 = [r for r in sweep if r.get("feasible") and r["closes_25yr"] and r["delivered_t"] > 0]
    cells_30 = [r for r in sweep if r.get("feasible") and r["closes_30yr"] and r["delivered_t"] > 0]
    results["closure_summary"] = {
        "n_cells_15yr": len(cells_15),
        "n_cells_20yr": len(cells_20),
        "n_cells_25yr": len(cells_25),
        "n_cells_30yr": len(cells_30),
        "n_cells_total": len(sweep),
    }

    # 3. Best Architecture E cell at each L0-05 ceiling (by delivered_t / m_LEO_t)
    def best_cell(cells: list, ceiling_label: str) -> dict | None:
        if not cells:
            return None
        return max(cells, key=lambda r: r["delivered_t"] / r["m_LEO_t"] if r["m_LEO_t"] > 0 else -math.inf)

    results["best_cells"] = {
        "ceiling_15yr": best_cell(cells_15, "15"),
        "ceiling_20yr": best_cell(cells_20, "20"),
        "ceiling_25yr": best_cell(cells_25, "25"),
        "ceiling_30yr": best_cell(cells_30, "30"),
    }

    # 4. Posterior cascade Monte Carlo
    # Architecture E at multiple reactor scales
    posterior_E = {}
    for r in [100.0, 200.0, 500.0, 1000.0]:
        posterior_E[f"E_at_{int(r)}kWe"] = monte_carlo(cascade_E, 50000, r)
    posterior_E["variantB_500kWe"] = monte_carlo(cascade_variantB, 50000)
    posterior_E["D_fission"] = monte_carlo(cascade_D_fission, 50000)
    posterior_E["D_solar_thermal"] = monte_carlo(cascade_D_solar_thermal, 50000)
    results["posterior_cascade"] = posterior_E

    # 5. Cadence / fleet / NPV analysis for best cells
    cadence_per_yr = 2.0  # L0-07 floor
    per_vehicle_cost_M_E = 300.0
    per_vehicle_cost_M_variantB = 500.0

    fleet_npv = {}
    for ceiling_yr, cell in results["best_cells"].items():
        if cell is None:
            fleet_npv[ceiling_yr] = None
            continue
        rt = cell["round_trip_yr"]
        # Fleet cost
        fleet_cap = fleet_capital(cadence_per_yr, rt, per_vehicle_cost_M_E)
        # NPV at three revenue points
        npv_at = {}
        for rev_per_mission in [100.0, 200.0, 500.0, 1000.0]:
            npv_at[f"rev_{int(rev_per_mission)}M_per_mission"] = npv_simple(
                cadence_per_yr=cadence_per_yr,
                round_trip_yr=rt,
                revenue_per_mission_M=rev_per_mission,
                fleet_capital_M=fleet_cap,
            )
        fleet_npv[ceiling_yr] = {
            "cell_reactor_kwe": cell["reactor_kwe"],
            "cell_chunk_t": cell["chunk_t"],
            "cell_isp_s": cell["isp_s"],
            "cell_round_trip_yr": rt,
            "cell_delivered_t": cell["delivered_t"],
            "cell_m_LEO_t": cell["m_LEO_t"],
            "fleet_size": cadence_per_yr * rt,
            "fleet_capital_M": fleet_cap,
            "npv_at_revenue": npv_at,
        }
    # Variant B reference (matrix's 500-kWe chemical-kick, ~14.5 yr round-trip, ≤200 t chunk).
    # Approximate per-mission delivered ≈ matrix's R-chunk-fed-chemical "100 kWe / 200 t" cell shifted:
    # at 500 kWe MARVL-mass + chemical-kick, delivered ~ 80 t per mission (placeholder; the matrix
    # has this at ~100-140 t under decomposed-mid; MARVL would reduce). Use 80 t.
    variantB_rt = 14.5
    variantB_delivered = 80.0
    fleet_cap_B = fleet_capital(cadence_per_yr, variantB_rt, per_vehicle_cost_M_variantB)
    npv_B = {}
    for rev_per_mission in [100.0, 200.0, 500.0, 1000.0]:
        npv_B[f"rev_{int(rev_per_mission)}M_per_mission"] = npv_simple(
            cadence_per_yr=cadence_per_yr,
            round_trip_yr=variantB_rt,
            revenue_per_mission_M=rev_per_mission,
            fleet_capital_M=fleet_cap_B,
        )
    fleet_npv["variantB_reference"] = {
        "round_trip_yr": variantB_rt,
        "delivered_t_assumed": variantB_delivered,
        "fleet_size": cadence_per_yr * variantB_rt,
        "fleet_capital_M": fleet_cap_B,
        "npv_at_revenue": npv_B,
    }
    results["fleet_npv"] = fleet_npv

    # 6. Hypothesis grading
    # H-E-a: At decomposed-MARVL, 200 kWe, chunk 100 t, Isp 2000 s: closes with positive
    # delivered mass and round-trip 20-28 yr.
    cell_HEa = next((r for r in sweep
                     if r["mass_model"] == "decomposed_marvl"
                     and r["reactor_kwe"] == 200.0
                     and r["chunk_t"] == 100.0
                     and r["isp_s"] == 2000.0), None)
    h_E_a_held = (cell_HEa is not None
                  and cell_HEa.get("feasible", False)
                  and cell_HEa["delivered_t"] > 0
                  and 20.0 <= cell_HEa["round_trip_yr"] <= 28.0)

    # H-E-b: sweet-spot cell at 25-yr ceiling — winner is reactor 200-500 kWe, chunk 50-100 t,
    # Isp 2000-2934 s.
    best_25 = results["best_cells"]["ceiling_25yr"]
    h_E_b_held = (best_25 is not None
                  and 200.0 <= best_25["reactor_kwe"] <= 500.0
                  and 50.0 <= best_25["chunk_t"] <= 100.0
                  and 2000.0 <= best_25["isp_s"] <= 2934.0)

    # H-E-c: E posterior median (at 200 kWe) > Variant B posterior median by 1.5-3×
    E_med = posterior_E["E_at_200kWe"]["median"]
    B_med = posterior_E["variantB_500kWe"]["median"]
    ratio = E_med / B_med if B_med > 0 else math.inf
    h_E_c_held = 1.5 <= ratio <= 3.0
    h_E_c_falsified_high = ratio > 3.0

    # H-E-d: fleet 50+ ships, $15B+ at 25-yr ceiling
    if fleet_npv.get("ceiling_25yr"):
        fleet_size_25 = fleet_npv["ceiling_25yr"]["fleet_size"]
        fleet_cap_25 = fleet_npv["ceiling_25yr"]["fleet_capital_M"]
        h_E_d_held = fleet_size_25 >= 50 and fleet_cap_25 >= 15000.0
    else:
        h_E_d_held = False
        fleet_size_25 = None
        fleet_cap_25 = None

    # H-E-e: NPV negative at $200M/mission, 8.7% WACC, 25-yr ceiling
    if fleet_npv.get("ceiling_25yr"):
        npv_at_200M = fleet_npv["ceiling_25yr"]["npv_at_revenue"]["rev_200M_per_mission"]["npv_M"]
        h_E_e_held = npv_at_200M < 0
    else:
        h_E_e_held = None
        npv_at_200M = None

    results["hypothesis_grading"] = {
        "H_E_a": {
            "predicted": "200 kWe MARVL, chunk 100 t, Isp 2000 s — closes with positive delivered, round-trip 20-28 yr",
            "actual": cell_HEa,
            "held": h_E_a_held,
        },
        "H_E_b": {
            "predicted": "Sweet-spot at 25-yr ceiling: reactor 200-500 kWe, chunk 50-100 t, Isp 2000-2934 s",
            "actual_best": best_25,
            "held": h_E_b_held,
        },
        "H_E_c": {
            "predicted": "Architecture E posterior median (200 kWe) exceeds Variant B median by 1.5-3×",
            "actual_E_med": E_med,
            "actual_B_med": B_med,
            "ratio_E_over_B": ratio,
            "held": h_E_c_held,
            "falsified_high": h_E_c_falsified_high,
        },
        "H_E_d": {
            "predicted": "Fleet 50+ ships at $15B+ fleet capital",
            "actual_fleet_size": fleet_size_25,
            "actual_fleet_capital_M": fleet_cap_25,
            "held": h_E_d_held,
        },
        "H_E_e": {
            "predicted": "NPV-negative at $200M/mission revenue, 8.7% WACC, 25-yr ceiling",
            "actual_npv_M": npv_at_200M,
            "held": h_E_e_held,
        },
    }

    # Output
    results_dir = Path(__file__).parent / "results"
    results_dir.mkdir(exist_ok=True)
    (results_dir / "architecture_E.json").write_text(json.dumps(results, indent=2, default=str))

    # Tables
    lines = []
    lines.append("# R-architecture-E-no-saturn-side-electrolysis — Results\n")
    lines.append("## Closure summary across L0-05 ceiling relaxations\n")
    lines.append(f"Of {len(sweep)} cells (5 reactor × 4 chunk × 3 specific impulse × 2 mass model):")
    lines.append(f"- closes 15-year ceiling with positive delivered: **{len(cells_15)}**")
    lines.append(f"- closes 20-year ceiling with positive delivered: **{len(cells_20)}**")
    lines.append(f"- closes 25-year ceiling with positive delivered: **{len(cells_25)}**")
    lines.append(f"- closes 30-year ceiling with positive delivered: **{len(cells_30)}**\n")

    lines.append("## Best Architecture E cell at each L0-05 ceiling (max delivered/launch-mass)\n")
    lines.append("| Ceiling | Mass model | Reactor (kWe) | Chunk (t) | Isp (s) | Round-trip (yr) | Delivered (t) | Launch (t) | Delivered/Launch |")
    lines.append("|---|---|---:|---:|---:|---:|---:|---:|---:|")
    for label, cell in results["best_cells"].items():
        if cell is None:
            lines.append(f"| {label} | — | — | — | — | — | — | — | — |")
        else:
            ratio_dl = cell["delivered_t"] / cell["m_LEO_t"] if cell["m_LEO_t"] > 0 else float("nan")
            lines.append(f"| {label} | {cell['mass_model']} | {cell['reactor_kwe']:.0f} | "
                         f"{cell['chunk_t']:.0f} | {cell['isp_s']:.0f} | "
                         f"{cell['round_trip_yr']:.2f} | {cell['delivered_t']:.1f} | "
                         f"{cell['m_LEO_t']:.1f} | {ratio_dl:.3f} |")
    lines.append("")

    lines.append("## Posterior cascade (Monte Carlo, 50,000 samples)\n")
    lines.append("| Architecture | Posterior median | 5th percentile | 95th percentile | Mean |")
    lines.append("|---|---:|---:|---:|---:|")
    for name, p in posterior_E.items():
        lines.append(f"| {name} | {p['median']*100:.2f}% | {p['p05']*100:.2f}% | {p['p95']*100:.2f}% | {p['mean']*100:.2f}% |")
    lines.append("")

    lines.append("## Fleet and net-present-value (8.7% weighted-average cost of capital, 40-yr horizon, cadence 2/yr)\n")
    lines.append("Cost assumptions: $300 million per vehicle (Architecture E), $500 million per vehicle (Variant B).\n")
    lines.append("| Architecture | Round-trip (yr) | Fleet size | Fleet capital ($M) | NPV @ $100M/mission | NPV @ $200M | NPV @ $500M | NPV @ $1000M |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|")
    for name, fn in fleet_npv.items():
        if fn is None:
            continue
        rt = fn["round_trip_yr"] if "round_trip_yr" in fn else fn["cell_round_trip_yr"]
        fs = fn["fleet_size"]
        fc = fn["fleet_capital_M"]
        npvs = fn["npv_at_revenue"]
        lines.append(f"| {name} | {rt:.2f} | {fs:.0f} | "
                     f"{fc:.0f} | {npvs['rev_100M_per_mission']['npv_M']:.0f} | "
                     f"{npvs['rev_200M_per_mission']['npv_M']:.0f} | "
                     f"{npvs['rev_500M_per_mission']['npv_M']:.0f} | "
                     f"{npvs['rev_1000M_per_mission']['npv_M']:.0f} |")
    lines.append("")

    lines.append("## Hypothesis grading\n")
    h = results["hypothesis_grading"]
    lines.append("| Sub-claim | Predicted | Actual | Held? |")
    lines.append("|---|---|---|---|")
    cell_a = h["H_E_a"]["actual"]
    if cell_a and cell_a.get("feasible"):
        actual_a_str = f"round-trip {cell_a['round_trip_yr']:.2f} yr, delivered {cell_a['delivered_t']:.1f} t"
    else:
        actual_a_str = "infeasible"
    lines.append(f"| H-E-a — 200 kWe MARVL chunk 100 t Isp 2000 s closes 20-28 yr, positive delivered | "
                 f"{h['H_E_a']['predicted']} | {actual_a_str} | "
                 f"{'yes' if h['H_E_a']['held'] else '**no**'} |")
    cell_b = h["H_E_b"]["actual_best"]
    if cell_b:
        actual_b_str = f"reactor {cell_b['reactor_kwe']:.0f} kWe, chunk {cell_b['chunk_t']:.0f} t, Isp {cell_b['isp_s']:.0f} s"
    else:
        actual_b_str = "no closure"
    lines.append(f"| H-E-b — Sweet-spot at 25-yr ceiling | "
                 f"reactor 200-500 kWe, chunk 50-100 t, Isp 2000-2934 s | "
                 f"{actual_b_str} | {'yes' if h['H_E_b']['held'] else '**no**'} |")
    lines.append(f"| H-E-c — E posterior median (200 kWe) > Variant B median by 1.5-3× | "
                 f"1.5-3× | "
                 f"E median {h['H_E_c']['actual_E_med']*100:.2f}%, B median {h['H_E_c']['actual_B_med']*100:.2f}%, ratio {h['H_E_c']['ratio_E_over_B']:.2f}× | "
                 f"{'yes' if h['H_E_c']['held'] else ('**no — falsified-high**' if h['H_E_c']['falsified_high'] else '**no — falsified-low**')} |")
    if h["H_E_d"]["actual_fleet_size"] is not None:
        actual_d_str = f"fleet {h['H_E_d']['actual_fleet_size']:.0f} ships, ${h['H_E_d']['actual_fleet_capital_M']:.0f} million"
    else:
        actual_d_str = "no 25-yr closure cell"
    lines.append(f"| H-E-d — Fleet 50+ ships, $15B+ fleet capital at 25-yr ceiling | "
                 f"50+ ships, $15B+ | {actual_d_str} | "
                 f"{'yes' if h['H_E_d']['held'] else '**no**'} |")
    if h["H_E_e"]["actual_npv_M"] is not None:
        actual_e_str = f"NPV {h['H_E_e']['actual_npv_M']:.0f} million"
    else:
        actual_e_str = "no 25-yr closure cell"
    lines.append(f"| H-E-e — NPV-negative at $200M/mission, 8.7% WACC, 25-yr ceiling | "
                 f"NPV < 0 at $200M | {actual_e_str} | "
                 f"{'yes' if h['H_E_e']['held'] else '**no**'} |")

    (results_dir / "tables.md").write_text("\n".join(lines))
    return results


if __name__ == "__main__":
    out = main()
    print("R-architecture-E-no-saturn-side-electrolysis complete.")
    print()
    print(f"Cells with positive delivered mass:")
    cs = out["closure_summary"]
    print(f"  15-yr: {cs['n_cells_15yr']}/{cs['n_cells_total']}")
    print(f"  20-yr: {cs['n_cells_20yr']}/{cs['n_cells_total']}")
    print(f"  25-yr: {cs['n_cells_25yr']}/{cs['n_cells_total']}")
    print(f"  30-yr: {cs['n_cells_30yr']}/{cs['n_cells_total']}")
    print()
    print("Best cell at each L0-05 relaxation:")
    for label, cell in out["best_cells"].items():
        if cell is None:
            print(f"  {label}: no closure")
        else:
            print(f"  {label}: reactor {cell['reactor_kwe']:.0f} kWe, chunk {cell['chunk_t']:.0f} t, "
                  f"Isp {cell['isp_s']:.0f} s, round-trip {cell['round_trip_yr']:.2f} yr, "
                  f"delivered {cell['delivered_t']:.1f} t, launch {cell['m_LEO_t']:.1f} t, "
                  f"mass-model {cell['mass_model']}")
    print()
    print("Posterior cascade medians:")
    for name, p in out["posterior_cascade"].items():
        print(f"  {name:25s}: median {p['median']*100:6.3f}%, "
              f"5-95 [{p['p05']*100:.3f}%, {p['p95']*100:.3f}%]")
    print()
    print("Hypothesis grading:")
    for k, v in out["hypothesis_grading"].items():
        held_str = "held" if v["held"] else "FALSIFIED"
        print(f"  {k}: {held_str}")
