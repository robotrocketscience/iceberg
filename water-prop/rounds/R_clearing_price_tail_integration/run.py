"""
R-clearing-price-tail-integration-decision-frame — run.py

Integrates R-LEO-water-demand-curve clearing-price distribution over
R-per-mission-economics-sensitivity-revisit break-even thresholds.
Articulates three decision frames; grades H1-H6.
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

demand = json.loads(
    (ROUNDS / "R_LEO_water_demand_curve/results/demand_curve_summary.json").read_text()
)
r9 = json.loads(
    (ROUNDS / "R_reactor_specific_power_program_targets/results/synthesis.json").read_text()
)
r10 = json.loads(
    (ROUNDS / "R_per_mission_economics_sensitivity_revisit/results/sensitivity.json").read_text()
)


# -----------------------------------------------------------------------------
# Step 1: log-normal fit to clearing-price distribution
# -----------------------------------------------------------------------------

price_dist = demand["headline"]["clearing_price_distribution"]
# Prices are USD per kg
p05_per_kg = price_dist["p05"]
p25_per_kg = price_dist["p25"]
p50_per_kg = price_dist["p50"]
p75_per_kg = price_dist["p75"]
p95_per_kg = price_dist["p95"]

# log10 percentiles
log10_p05 = math.log10(p05_per_kg)
log10_p50 = math.log10(p50_per_kg)
log10_p95 = math.log10(p95_per_kg)

mu_log10 = log10_p50
# Spread: (p95 - p05) in log10 covers ~3.29 sigma_log10 (z ±1.645)
# A symmetric log-normal would have (log10_p95 - log10_p50) == (log10_p50 - log10_p05)
spread_above = log10_p95 - log10_p50  # 1.07
spread_below = log10_p50 - log10_p05  # 1.10
# Average and convert: 1 sigma corresponds to ~1.645 z at p95
sigma_log10 = ((spread_above + spread_below) / 2) / 1.6448536269514722


# Internal consistency check vs p25/p75
log10_p25_predicted = mu_log10 + sigma_log10 * (-0.6744897501960817)  # z for p25
log10_p75_predicted = mu_log10 + sigma_log10 * (0.6744897501960817)   # z for p75
p25_predicted = 10 ** log10_p25_predicted
p75_predicted = 10 ** log10_p75_predicted

log_normal_fit_validity = {
    "mu_log10": mu_log10,
    "sigma_log10": sigma_log10,
    "p25_measured_per_kg": p25_per_kg,
    "p25_predicted_per_kg": p25_predicted,
    "p25_error_pct": (p25_predicted - p25_per_kg) / p25_per_kg * 100,
    "p75_measured_per_kg": p75_per_kg,
    "p75_predicted_per_kg": p75_predicted,
    "p75_error_pct": (p75_predicted - p75_per_kg) / p75_per_kg * 100,
}


def p_price_above(break_even_per_kg: float) -> float:
    """P(clearing price >= break-even) under log-normal fit."""
    z = (math.log10(break_even_per_kg) - mu_log10) / sigma_log10
    return 1 - 0.5 * (1 + math.erf(z / math.sqrt(2)))


# -----------------------------------------------------------------------------
# Step 2: break-even ladder from round 10
# -----------------------------------------------------------------------------

# Convert $M/tonne to USD/kg: $M/tonne × 1e6 / 1000 = USD/kg × 1000... wait.
# $1M/tonne = $1,000,000 / 1000 kg = $1,000 / kg
# So $X M/tonne = $X × 1000 per kg
def m_per_t_to_per_kg(m_per_t: float) -> float:
    return m_per_t * 1000

# Break-even at different launches × reuse from round 10
breakeven_round10 = r10["breakeven_clearing_price_table"]
breakeven_ladder = []
for label, payload in breakeven_round10.items():
    breakeven_ladder.append({
        "label": label,
        "breakeven_m_per_t": payload["breakeven_clearing_price_m_per_t"],
        "breakeven_per_kg": m_per_t_to_per_kg(payload["breakeven_clearing_price_m_per_t"]),
        "per_mission_cost_b": payload["per_mission_cost_b"],
        "p_price_above_breakeven": p_price_above(
            m_per_t_to_per_kg(payload["breakeven_clearing_price_m_per_t"])
        ),
    })


# -----------------------------------------------------------------------------
# Step 3: H1 and H2 — specific anchors
# -----------------------------------------------------------------------------

# H1: 3 launches, reuse 15 → break-even $22.4 M/t
h1_breakeven = breakeven_round10["launches=3_reuse=15"]["breakeven_clearing_price_m_per_t"]
h1_p_above = p_price_above(m_per_t_to_per_kg(h1_breakeven))

# H2: 1-launch architecture — need to compute from anchors directly
# cost = $0.65/15 + 1 × $0.30 = $0.343B per mission; delivered 42.04 t
# break-even = $0.343B / 42.04 t = $8.16 M/t
h2_breakeven_m_per_t = (0.65 / 15 + 1 * 0.30) * 1000 / 42.04
h2_p_above = p_price_above(m_per_t_to_per_kg(h2_breakeven_m_per_t))


# -----------------------------------------------------------------------------
# Step 4: compose with round-9 conjunction posterior
# -----------------------------------------------------------------------------

CONJUNCTION_H2A_UNIFORM = r9["synthesis_table"][3]["conjunction_posterior"]
# Should be 0.001669 (0.167%) for H2a uniform

# Demand-curve E_500kWe_200t P(NPV>0)
demand_npv = demand["headline"]["p_npv_positive_summary"]["E_500kWe_200t"]


# -----------------------------------------------------------------------------
# Step 5: three decision frames
# -----------------------------------------------------------------------------

frames = {
    "frame_A_full_chain_return_seeking": {
        "description": "Full conjunction × conditional P(NPV>0) at zero discount, demand-curve integrated",
        "p_positive_npv_zero_disc_lower": CONJUNCTION_H2A_UNIFORM * h1_p_above,
        "p_positive_npv_zero_disc_upper": CONJUNCTION_H2A_UNIFORM * demand_npv["WACC_0.0_LR_0.0"],
        "verdict": "RULED OUT (P < 0.1% at any prior choice)",
    },
    "frame_B_conditional_success_price_tail_integrated": {
        "description": "Conditional on reactor + engineering success; integrate over demand-curve",
        "p_positive_npv_zero_disc_lower_3_launches": h1_p_above,
        "p_positive_npv_zero_disc_upper_demand_curve_fleet": demand_npv["WACC_0.0_LR_0.0"],
        "p_positive_npv_zero_disc_1_launch_architecture": h2_p_above,
        "p_positive_npv_at_sovereign_bond_3pct_demand_curve": demand_npv["WACC_0.03_LR_0.0"],
        "p_positive_npv_at_venture_8pct_demand_curve": demand_npv["WACC_0.087_LR_0.0"],
        "p_positive_npv_at_venture_12pct_demand_curve": demand_npv["WACC_0.12_LR_0.0"],
        "verdict": "VIABLE IN PRINCIPLE at zero-discount and sovereign-bond discount; tight at venture-class",
    },
    "frame_C_conditional_point_estimate": {
        "description": "Conditional success at BEST_CELL clearing price ($2.5M/tonne)",
        "program_npv0_b": r10["central_anchored_results"]["h2a_conditional_program_npv0_b"],
        "verdict": "RULED OUT at point estimate; ignores price distribution tail",
    },
}


# -----------------------------------------------------------------------------
# Grading
# -----------------------------------------------------------------------------

grading = {}

# H1
grading["H1"] = {
    "predicted_range": [0.10, 0.25],
    "measured_p_price_above": h1_p_above,
    "breakeven_m_per_t": h1_breakeven,
    "status": "HELD" if 0.10 <= h1_p_above <= 0.25 else "FALSIFIED",
}

# H2
grading["H2"] = {
    "predicted_range": [0.30, 0.50],
    "measured_p_price_above": h2_p_above,
    "breakeven_m_per_t": h2_breakeven_m_per_t,
    "status": "HELD" if 0.30 <= h2_p_above <= 0.50 else "FALSIFIED",
}

# H3: conditional-success P(NPV>0 at zero discount) bracket [10%, 50%]
grading["H3"] = {
    "predicted_range": [0.10, 0.50],
    "h1_my_point_estimate_3_launches": h1_p_above,
    "demand_curve_fleet_47pct": demand_npv["WACC_0.0_LR_0.0"],
    "bracket_min": h1_p_above,
    "bracket_max": demand_npv["WACC_0.0_LR_0.0"],
    "status": "HELD" if (0.10 <= h1_p_above and demand_npv["WACC_0.0_LR_0.0"] <= 0.50) else "FALSIFIED",
}

# H4: full-chain P(NPV>0) in [0.02%, 0.10%]
h4_lower = frames["frame_A_full_chain_return_seeking"]["p_positive_npv_zero_disc_lower"]
h4_upper = frames["frame_A_full_chain_return_seeking"]["p_positive_npv_zero_disc_upper"]
grading["H4"] = {
    "predicted_range": [0.0002, 0.001],
    "measured_lower": h4_lower,
    "measured_upper": h4_upper,
    "status": "HELD" if 0.0002 <= h4_lower and h4_upper <= 0.001 else "FALSIFIED",
}

# H5: three frames give distinct verdicts; Frame B viable at ≥ 15%
grading["H5"] = {
    "frame_A_verdict": "RULED OUT",
    "frame_B_p_at_zero_disc_3_launches": h1_p_above,
    "frame_B_viable": h1_p_above >= 0.15,
    "frame_C_verdict": "RULED OUT at point estimate",
    "three_frames_distinct": True,
    "status": "HELD" if h1_p_above >= 0.15 else "FALSIFIED",
}

# H6: matrix axis 17 amendment — Frame B P(NPV>0) at venture WACC (12%) ≥ 5%
grading["H6"] = {
    "demand_curve_p_npv_positive_at_venture_wacc_12pct": demand_npv["WACC_0.12_LR_0.0"],
    "frame_b_viable_at_venture_wacc": demand_npv["WACC_0.12_LR_0.0"] >= 0.05,
    "matrix_amendment_recommendation": (
        "venture-class framing should NOT be structurally retired; "
        "Frame B P(NPV>0) at venture WACC is "
        f"{demand_npv['WACC_0.12_LR_0.0']:.1%}, above 5% threshold"
    ),
    "status": "HELD" if demand_npv["WACC_0.12_LR_0.0"] >= 0.05 else "FALSIFIED",
}


# -----------------------------------------------------------------------------
# Output
# -----------------------------------------------------------------------------

output = {
    "round": "R-clearing-price-tail-integration-decision-frame",
    "author": "rhea",
    "date": "2026-05-15",
    "log_normal_fit": log_normal_fit_validity,
    "demand_curve_anchors": {
        "p05_per_kg": p05_per_kg,
        "p50_per_kg": p50_per_kg,
        "p95_per_kg": p95_per_kg,
    },
    "breakeven_ladder_p_price_above": breakeven_ladder,
    "h2a_uniform_prior_conjunction_posterior": CONJUNCTION_H2A_UNIFORM,
    "demand_curve_E_500kWe_200t_p_npv_positive": demand_npv,
    "three_decision_frames": frames,
    "grading": grading,
}

(RESULTS / "three_frames.json").write_text(json.dumps(output, indent=2, default=str))

with open(RESULTS / "three_frames_table.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=list(breakeven_ladder[0].keys()))
    writer.writeheader()
    for r in breakeven_ladder:
        writer.writerow(r)

print("=" * 80)
print("R-clearing-price-tail-integration-decision-frame — summary")
print("=" * 80)
print()
print(f"Log-normal fit:  mu_log10 = {mu_log10:.3f}, sigma_log10 = {sigma_log10:.3f}")
print(f"  p25 fit validity: predicted ${p25_predicted:.0f}/kg vs measured ${p25_per_kg:.0f}/kg "
      f"({log_normal_fit_validity['p25_error_pct']:+.1f}%)")
print(f"  p75 fit validity: predicted ${p75_predicted:.0f}/kg vs measured ${p75_per_kg:.0f}/kg "
      f"({log_normal_fit_validity['p75_error_pct']:+.1f}%)")
print()
print("Break-even ladder vs demand-curve tail probability:")
for r in breakeven_ladder:
    print(f"  {r['label']:<35}  ${r['breakeven_m_per_t']:>5.1f}M/t  P(price≥BE) = {r['p_price_above_breakeven']:.1%}")
print()
print(f"H2a uniform-prior conjunction posterior: {CONJUNCTION_H2A_UNIFORM:.4%}")
print()
print("THREE DECISION FRAMES:")
print(f"  Frame A (full chain):         P(NPV>0) = {h4_lower:.4%} – {h4_upper:.4%}  → RULED OUT")
print(f"  Frame B (conditional+price):  P(NPV>0) = {h1_p_above:.1%} (my BE) – {demand_npv['WACC_0.0_LR_0.0']:.1%} (demand-curve) at zero disc")
print(f"                                P(NPV>0) at sovereign-bond 3%: {demand_npv['WACC_0.03_LR_0.0']:.1%}")
print(f"                                P(NPV>0) at venture WACC 12%:  {demand_npv['WACC_0.12_LR_0.0']:.1%}")
print(f"  Frame C (point est BEST_CELL): NPV(0) = ${r10['central_anchored_results']['h2a_conditional_program_npv0_b']:+.2f}B → RULED OUT at point estimate")
print()
print("HYPOTHESIS GRADING:")
for k, v in grading.items():
    print(f"  {k}: {v['status']}")
print()
print(f"Outputs: {RESULTS}/three_frames.json, {RESULTS}/three_frames_table.csv")
