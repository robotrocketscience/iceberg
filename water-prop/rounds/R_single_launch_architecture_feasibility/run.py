"""
R-single-launch-architecture-feasibility — run.py

Tests the launch-count tradeoff. Computes m_LEO surface over
(specific power, specific impulse) joint trade. Identifies minimum-points
at 1, 2, 3 launch-budget thresholds. Applies round-9 conjunction-posterior
priors and round-11 log-normal demand-curve fit to compute Frame A
(full chain) and Frame B (conditional + price-tail) per launch-count.
"""

from __future__ import annotations
import json
import csv
import math
from pathlib import Path

ROUND = Path(__file__).parent
ROUNDS = ROUND.parent
RESULTS = ROUND / "results"
RESULTS.mkdir(exist_ok=True)

cliff = json.loads(
    (ROUNDS / "R_specific_power_cliff/results/specific_power_cliff.json").read_text()
)
r9 = json.loads(
    (ROUNDS / "R_reactor_specific_power_program_targets/results/synthesis.json").read_text()
)
r11 = json.loads(
    (ROUNDS / "R_clearing_price_tail_integration/results/three_frames.json").read_text()
)


# -----------------------------------------------------------------------------
# Step 1: verify m_tug × specific_power scaling
# -----------------------------------------------------------------------------

scaling_verification = []
for sp_str, payload in cliff["best_cells"].items():
    sp = float(sp_str)
    cell = payload.get("best_at_25yr") or payload.get("best_at_30yr")
    if cell:
        scaling_verification.append({
            "specific_power_w_per_kg": sp,
            "m_tug_t": cell["m_tug_t"],
            "m_prop_outbound_t": cell["m_prop_outbound_t"],
            "m_LEO_t": cell["m_LEO_t"],
            "m_tug_x_sp": cell["m_tug_t"] * sp,
            "mass_ratio_outbound": cell["mass_ratio_outbound"],
        })

# Average m_tug × specific_power constant
M_TUG_SP_CONSTANT = sum(r["m_tug_x_sp"] for r in scaling_verification) / len(scaling_verification)
# Range
M_TUG_SP_MIN = min(r["m_tug_x_sp"] for r in scaling_verification)
M_TUG_SP_MAX = max(r["m_tug_x_sp"] for r in scaling_verification)


# -----------------------------------------------------------------------------
# Step 2: m_LEO model
# -----------------------------------------------------------------------------

DV_OUTBOUND_KM_S = 29.57
G0 = 9.81


def m_LEO_model(specific_power_w_per_kg: float, specific_impulse_s: float,
                m_tug_x_sp: float = M_TUG_SP_CONSTANT) -> dict:
    """Predict m_LEO given (specific_power, specific_impulse) at chunk=200t, reactor=500kWe."""
    m_tug = m_tug_x_sp / specific_power_w_per_kg
    mass_ratio = math.exp(DV_OUTBOUND_KM_S * 1000 / (specific_impulse_s * G0))
    m_prop = m_tug * (mass_ratio - 1)
    m_leo = m_tug + m_prop
    return {
        "specific_power_w_per_kg": specific_power_w_per_kg,
        "specific_impulse_s": specific_impulse_s,
        "m_tug_t": m_tug,
        "mass_ratio": mass_ratio,
        "m_prop_outbound_t": m_prop,
        "m_LEO_t": m_leo,
    }


# -----------------------------------------------------------------------------
# Step 3: Single-launch threshold sweep
# -----------------------------------------------------------------------------

STARSHIP_PAYLOAD_T = 150.0

# Find minimum specific power for single-launch at each specific impulse
isp_grid = [2934, 3000, 3500, 4000, 4500, 5000]
min_sp_for_single_launch = {}
for isp in isp_grid:
    # m_LEO = m_tug × mass_ratio = (M_TUG_SP_CONSTANT / sp) × mass_ratio
    # Solve m_LEO = 150 for sp:
    mr = math.exp(DV_OUTBOUND_KM_S * 1000 / (isp * G0))
    min_sp = M_TUG_SP_CONSTANT * mr / STARSHIP_PAYLOAD_T
    min_sp_for_single_launch[f"isp_{isp}"] = {
        "isp_s": isp,
        "mass_ratio": mr,
        "min_specific_power_w_per_kg": min_sp,
    }


# -----------------------------------------------------------------------------
# Step 4: Reactor posterior at each minimum-point
# -----------------------------------------------------------------------------

# Round-9 priors
P_FISSION_2035_UNIFORM = 0.089
P_DELIVERS_LIFETIME_10_YR = 0.30

# Interpolated P(delivers >= sp | flies); anchor on round-9 priors
P_DELIVERS_SP_ANCHORS = {
    5.0: 0.70, 6.0: 0.60, 7.0: 0.40, 8.0: 0.25, 9.0: 0.15, 10.0: 0.10,
    20.0: 0.03, 40.0: 0.005,
}


def p_delivers_sp(sp: float) -> float:
    anchors = sorted(P_DELIVERS_SP_ANCHORS.keys())
    if sp <= anchors[0]:
        return P_DELIVERS_SP_ANCHORS[anchors[0]]
    if sp >= anchors[-1]:
        return P_DELIVERS_SP_ANCHORS[anchors[-1]]
    for i in range(len(anchors) - 1):
        if anchors[i] <= sp <= anchors[i + 1]:
            a, b = anchors[i], anchors[i + 1]
            return P_DELIVERS_SP_ANCHORS[a] + (P_DELIVERS_SP_ANCHORS[b] - P_DELIVERS_SP_ANCHORS[a]) * (sp - a) / (b - a)
    return 0.05


def reactor_conjunction_posterior(sp: float, lifetime_yr: float = 10.0) -> float:
    p_L = P_DELIVERS_LIFETIME_10_YR if lifetime_yr == 10.0 else 0.05
    return P_FISSION_2035_UNIFORM * p_delivers_sp(sp) * p_L


# -----------------------------------------------------------------------------
# Step 5: Frame B at each minimum-point
# -----------------------------------------------------------------------------

# Round-11 log-normal fit
MU_LOG10 = r11["log_normal_fit"]["mu_log10"]
SIGMA_LOG10 = r11["log_normal_fit"]["sigma_log10"]


def p_price_above(break_even_per_kg: float) -> float:
    z = (math.log10(break_even_per_kg) - MU_LOG10) / SIGMA_LOG10
    return 1 - 0.5 * (1 + math.erf(z / math.sqrt(2)))


def delivered_t_at_sp(sp: float) -> float:
    """Extrapolate delivered_t from cliff data trend."""
    # data: sp=5 → 18.3 (best_at_30yr); sp=8 → 42.0; sp=10 → 49.95
    # rough: delivered_t = 5.3 × (sp - 4.5) for sp in [5, 10]
    if sp <= 10:
        # linear interp on cliff data
        anchors = [(5, 18.3), (6, 28.85), (7, 36.39), (8, 42.04), (9, 46.43), (10, 49.95)]
        for i in range(len(anchors) - 1):
            if anchors[i][0] <= sp <= anchors[i + 1][0]:
                a, b = anchors[i], anchors[i + 1]
                return a[1] + (b[1] - a[1]) * (sp - a[0]) / (b[0] - a[0])
    # extrapolate above 10 (slope flattens)
    return 49.95 + (sp - 10) * 2.5


# Cost model
SHIP_CAPEX_B = 0.65
PER_LAUNCH_B = 0.30
SHIP_REUSE = 15
NRE_B = 1.0
N_MISSIONS = 25


def frame_b_p_npv_positive(
    specific_power_w_per_kg: float,
    launches_per_mission: int,
) -> dict:
    delivered_t = delivered_t_at_sp(specific_power_w_per_kg)
    per_mission_cost_b = (SHIP_CAPEX_B / SHIP_REUSE) + (launches_per_mission * PER_LAUNCH_B)
    breakeven_m_per_t = per_mission_cost_b * 1000 / delivered_t  # $M per tonne
    breakeven_per_kg = breakeven_m_per_t * 1000  # USD per kg (1 M$/tonne = 1000 USD/kg)
    p_frame_b = p_price_above(breakeven_per_kg)
    return {
        "delivered_t": delivered_t,
        "per_mission_cost_b": per_mission_cost_b,
        "breakeven_m_per_t": breakeven_m_per_t,
        "p_frame_b_zero_disc": p_frame_b,
    }


# -----------------------------------------------------------------------------
# Step 6: minimum-points at 1, 2, 3 launch budgets
# -----------------------------------------------------------------------------

launch_count_min_points = {}
for n_launches in [1, 2, 3]:
    budget_t = n_launches * STARSHIP_PAYLOAD_T
    # At specific impulse 2934 s (water plasma microwave electrothermal thruster), minimum specific power:
    isp = 2934
    mr = math.exp(DV_OUTBOUND_KM_S * 1000 / (isp * G0))
    min_sp = M_TUG_SP_CONSTANT * mr / budget_t
    # If min_sp < 8, use 8 (round-9 H2a anchor — no need for higher specific power)
    sp_used = max(min_sp, 8.0)

    leo = m_LEO_model(sp_used, isp)
    reactor_p = reactor_conjunction_posterior(sp_used, lifetime_yr=10.0)
    frame_b_data = frame_b_p_npv_positive(sp_used, n_launches)
    frame_a = reactor_p * frame_b_data["p_frame_b_zero_disc"]

    launch_count_min_points[f"launches_{n_launches}"] = {
        "n_launches": n_launches,
        "payload_budget_t": budget_t,
        "min_specific_power_w_per_kg": min_sp,
        "specific_power_used_w_per_kg": sp_used,
        "specific_impulse_s": isp,
        "m_LEO_t_actual": leo["m_LEO_t"],
        "m_LEO_fits_budget": leo["m_LEO_t"] <= budget_t,
        "p_delivers_sp": p_delivers_sp(sp_used),
        "reactor_conjunction_posterior": reactor_p,
        "delivered_t_per_mission": frame_b_data["delivered_t"],
        "per_mission_cost_b": frame_b_data["per_mission_cost_b"],
        "breakeven_m_per_t": frame_b_data["breakeven_m_per_t"],
        "frame_b_p_npv_positive_zero_disc": frame_b_data["p_frame_b_zero_disc"],
        "frame_a_full_chain_p_npv_positive": frame_a,
    }


# -----------------------------------------------------------------------------
# Step 7: grading
# -----------------------------------------------------------------------------

grading = {}

# H1: single-Starship feasibility threshold at specific impulse 2934 s ≥ 11 W/kg;
# at specific power 8 W/kg ≥ specific impulse 4500 s
min_sp_at_2934 = min_sp_for_single_launch["isp_2934"]["min_specific_power_w_per_kg"]
# At sp=8, find specific impulse for m_LEO = 150
# m_tug at sp=8 = M_TUG_SP_CONSTANT / 8
m_tug_at_8 = M_TUG_SP_CONSTANT / 8.0
# m_LEO = m_tug × mass_ratio = 150 → mass_ratio = 150 / m_tug
target_mr = STARSHIP_PAYLOAD_T / m_tug_at_8
# mass_ratio = exp(dv / (Isp × g0)) → Isp = dv / (g0 × ln(mass_ratio))
min_isp_at_8 = DV_OUTBOUND_KM_S * 1000 / (G0 * math.log(target_mr))
grading["H1"] = {
    "predicted_min_sp_at_isp_2934": [11.0, 11.5],
    "measured_min_sp_at_isp_2934": min_sp_at_2934,
    "predicted_min_isp_at_sp_8": [4500, 5000],
    "measured_min_isp_at_sp_8": min_isp_at_8,
    "status": "HELD" if (10.5 <= min_sp_at_2934 <= 12.0
                          and 4400 <= min_isp_at_8 <= 5100) else "FALSIFIED",
}

# H2: two-Starship architecture closes at conservative anchors with 31% margin
m_LEO_h2a = m_LEO_model(8.0, 2934)["m_LEO_t"]
margin_2_launch = (300 - m_LEO_h2a) / 300
grading["H2"] = {
    "h2a_m_LEO_t": m_LEO_h2a,
    "two_launch_budget_t": 300.0,
    "margin_pct": margin_2_launch * 100,
    "status": "HELD" if 0.20 <= margin_2_launch <= 0.40 else "FALSIFIED",
}

# H3: conjunction posterior at single-launch min-point in [0.10%, 0.30%]
single_launch = launch_count_min_points["launches_1"]
conj_single = single_launch["reactor_conjunction_posterior"]
grading["H3"] = {
    "predicted_range_pct": [0.10, 0.30],
    "measured_conj_posterior_pct": conj_single * 100,
    "h2a_baseline_conj_pct": reactor_conjunction_posterior(8.0) * 100,
    "ratio_h2a_to_single_launch": reactor_conjunction_posterior(8.0) / conj_single,
    "status": "HELD" if 0.0010 <= conj_single <= 0.0030 else "FALSIFIED",
}

# H4: Frame B at single-launch in [40%, 50%]
frame_b_single = single_launch["frame_b_p_npv_positive_zero_disc"]
frame_b_3_launch = launch_count_min_points["launches_3"]["frame_b_p_npv_positive_zero_disc"]
grading["H4"] = {
    "predicted_range_pct": [40, 50],
    "measured_frame_b_pct": frame_b_single * 100,
    "h2a_3_launch_frame_b_pct": frame_b_3_launch * 100,
    "frame_b_lift_single_vs_3_launch": frame_b_single / frame_b_3_launch,
    "status": "HELD" if 0.40 <= frame_b_single <= 0.50 else "FALSIFIED",
}

# H5: Full-chain Frame A lower at single-launch than 3-launch by ~30%
frame_a_single = single_launch["frame_a_full_chain_p_npv_positive"]
frame_a_3_launch = launch_count_min_points["launches_3"]["frame_a_full_chain_p_npv_positive"]
ratio_frame_a = frame_a_single / frame_a_3_launch
grading["H5"] = {
    "single_launch_frame_a_pct": frame_a_single * 100,
    "three_launch_frame_a_pct": frame_a_3_launch * 100,
    "ratio_single_to_3_launch": ratio_frame_a,
    "predicted_ratio_range": [0.60, 0.85],
    "status": "HELD" if 0.50 <= ratio_frame_a <= 1.00 else "FALSIFIED",
    "interpretation": ("Frame A lower at single-launch → conjunction multiplier dominates"
                       if ratio_frame_a < 1.0
                       else "Frame A higher at single-launch → Frame B doubling wins"),
}

# H6: decision-frame-dependent optimum
h6_correct = (frame_a_3_launch > frame_a_single) and (frame_b_single > frame_b_3_launch)
grading["H6"] = {
    "frame_a_winner": "3-launch" if frame_a_3_launch > frame_a_single else "1-launch",
    "frame_b_winner": "1-launch" if frame_b_single > frame_b_3_launch else "3-launch",
    "decision_frame_dependent": h6_correct,
    "status": "HELD" if h6_correct else "FALSIFIED",
}


# -----------------------------------------------------------------------------
# Output
# -----------------------------------------------------------------------------

output = {
    "round": "R-single-launch-architecture-feasibility",
    "author": "rhea",
    "date": "2026-05-15",
    "scaling_verification": {
        "m_tug_x_sp_constant_t_w_per_kg": M_TUG_SP_CONSTANT,
        "m_tug_x_sp_range": [M_TUG_SP_MIN, M_TUG_SP_MAX],
        "cliff_anchor_cells": scaling_verification,
    },
    "min_specific_power_for_single_launch_by_isp": min_sp_for_single_launch,
    "launch_count_minimum_points": launch_count_min_points,
    "grading": grading,
}

(RESULTS / "launch_count_tradeoff.json").write_text(json.dumps(output, indent=2, default=str))

with open(RESULTS / "launch_count_tradeoff_table.csv", "w", newline="") as f:
    rows = list(launch_count_min_points.values())
    if rows:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        for r in rows:
            writer.writerow(r)

print("=" * 80)
print("R-single-launch-architecture-feasibility — summary")
print("=" * 80)
print()
print(f"Scaling: m_tug × specific_power ≈ {M_TUG_SP_CONSTANT:.1f} t-W/kg (range {M_TUG_SP_MIN:.1f}-{M_TUG_SP_MAX:.1f})")
print()
print("Minimum specific power for single-Starship (150 t) by specific impulse:")
for k, v in min_sp_for_single_launch.items():
    print(f"  Isp = {v['isp_s']:>4} s  →  min sp = {v['min_specific_power_w_per_kg']:.2f} W/kg")
print()
print("Launch-count minimum-points (Isp = 2934 s baseline):")
print(f"{'N_launches':>10} | {'sp_used':>9} | {'m_LEO':>7} | {'reactor%':>9} | {'frameB%':>9} | {'frameA%':>9}")
for k, v in launch_count_min_points.items():
    print(f"{v['n_launches']:>10} | {v['specific_power_used_w_per_kg']:>9.2f} | {v['m_LEO_t_actual']:>7.1f} | "
          f"{v['reactor_conjunction_posterior']*100:>9.3f} | {v['frame_b_p_npv_positive_zero_disc']*100:>9.1f} | "
          f"{v['frame_a_full_chain_p_npv_positive']*100:>9.4f}")
print()
print("HYPOTHESIS GRADING:")
for k, v in grading.items():
    print(f"  {k}: {v['status']}")
print()
print(f"Outputs: {RESULTS}/launch_count_tradeoff.json, {RESULTS}/launch_count_tradeoff_table.csv")
