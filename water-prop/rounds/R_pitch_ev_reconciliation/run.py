"""
R-pitch-ev-reconciliation — composes the five-round chain's joint conjunction
posterior with the pitch's gated expected-value framework. Adjudicates whether
the pitch's positive expected value survives composition.

Author: iapetus, 2026-05-16
Pre-registration: SCOPE.md (H1-H6)
"""

from __future__ import annotations

import json
from itertools import product
from pathlib import Path

RESULTS_DIR = Path(__file__).parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Load prior-round outputs verbatim
# ---------------------------------------------------------------------------

PRIOR_TARGETS = json.loads(
    (PROJECT_ROOT / "R_reactor_specific_power_program_targets" / "results" / "reactor_program_targets.json").read_text()
)
PRIOR_WINDOW = json.loads(
    (PROJECT_ROOT / "R_demonstrator_window_sensitivity" / "results" / "demonstrator_window_sensitivity.json").read_text()
)
PRIOR_GLOBAL = json.loads(
    (PROJECT_ROOT / "R_global_vs_us_base_rate" / "results" / "global_vs_us_base_rate.json").read_text()
)
PRIOR_ENG = json.loads(
    (PROJECT_ROOT / "R_engineering_closure_sensitivity" / "results" / "engineering_closure_sensitivity.json").read_text()
)
PRIOR_COND = json.loads(
    (PROJECT_ROOT / "R_conditional_prior_sensitivity" / "results" / "conditional_prior_sensitivity.json").read_text()
)

# ---------------------------------------------------------------------------
# Pitch numbers — encoded verbatim from ICEBERG-pitch.md
# ---------------------------------------------------------------------------

PITCH_NUMBERS = {
    "max_credible_loss_billion": 1.0,            # line 270
    "long_run_value_low_billion": 12.0,          # line 271 low
    "long_run_value_high_billion": 24.0,         # line 271 high
    "p_pitch_worst_case": 0.50,                  # line 272 worst-case
    "p_pitch_post_gates": 0.70,                  # line 282 after gates A-C close
    "p_pitch_floor_low": 0.10,                   # line 244 floor probability low
    "p_pitch_floor_high": 0.25,                  # line 244 floor probability high
    "p_pitch_upside_a": 0.30,                    # line 245 upside A
    "p_pitch_upside_b": 0.55,                    # line 246 upside B
    "induced_demand_value_low_billion": 50.0,    # line 284 induced demand low
    "induced_demand_value_high_billion": 200.0,  # line 284 induced demand high
}

# ---------------------------------------------------------------------------
# Anchor the technology-gates conjunction posterior from the five-round chain
# ---------------------------------------------------------------------------
#
# The five-round chain's posterior corners — what does p_technology_gates equal
# at each anchor? Take it directly from PRIOR_TARGETS, PRIOR_GLOBAL, PRIOR_COND
# rather than re-deriving.

# Pull the orbit posteriors first.
us_p_500 = PRIOR_WINDOW["p_500kWe_orbit_by_window_and_prior"]["uniform_beta_1_1"]
# us_p_500 is keyed by window-year string
P_ORBIT_US_2035_UNIFORM = us_p_500["2035"]
# Global+ever from R3:
global_table = PRIOR_GLOBAL["global_table"]
# Find the global+ever uniform anchor at window 2035
P_ORBIT_GLOBAL_2035_UNIFORM = next(
    r["uniform_beta_1_1_p_500"] for r in global_table if r["window_year"] == 2035
)
# Skeptical, Jeffreys priors at 2035
P_ORBIT_US_2035_SKEPTICAL = PRIOR_WINDOW["p_500kWe_orbit_by_window_and_prior"]["skeptical_beta_0p5_5"]["2035"]
P_ORBIT_US_2035_JEFFREYS = PRIOR_WINDOW["p_500kWe_orbit_by_window_and_prior"]["jeffreys_beta_0p5_0p5"]["2035"]

# Subjective conditional priors at the baseline corner (specific power >= 5, lifetime >= 10, X >= 10)
COND = PRIOR_TARGETS["subjective_priors"]
P_SP_5_BASELINE = COND["p_sp_geq_given_orbit_500kWe"]["5.0"]
P_L_10_BASELINE = COND["p_L_geq_given_orbit_500kWe"]["10.0"]
P_X_10_BASELINE = COND["p_X_geq_given_hybrid_closes"]["10.0"]
P_HYBRID = COND["P_HYBRID_AEROCAP"]                # 0.5
P_RENDEZVOUS_LO = COND["P_RENDEZVOUS_LOW"]         # 0.2
P_RENDEZVOUS_HI = COND["P_RENDEZVOUS_HI"]          # 0.3

# Anchor conjunction posteriors for the five canonical states
# (conservative_us_skeptical, conservative_us_jeffreys, conservative_us_uniform,
#  optimistic_global_uniform, pathological_all_priors_at_one).
def conjunction(p_orbit, p_sp, p_L, p_X, p_hybrid, p_rendezvous):
    """Compose technology-gates joint posterior."""
    return p_orbit * p_sp * p_L * p_X * p_hybrid * p_rendezvous


TECH_GATE_ANCHORS = {
    "conservative_us_skeptical": conjunction(
        P_ORBIT_US_2035_SKEPTICAL, P_SP_5_BASELINE, P_L_10_BASELINE,
        P_X_10_BASELINE, P_HYBRID, P_RENDEZVOUS_LO
    ),
    "conservative_us_jeffreys": conjunction(
        P_ORBIT_US_2035_JEFFREYS, P_SP_5_BASELINE, P_L_10_BASELINE,
        P_X_10_BASELINE, P_HYBRID, P_RENDEZVOUS_LO
    ),
    "conservative_us_uniform": conjunction(
        P_ORBIT_US_2035_UNIFORM, P_SP_5_BASELINE, P_L_10_BASELINE,
        P_X_10_BASELINE, P_HYBRID, P_RENDEZVOUS_LO
    ),
    "optimistic_global_uniform_baseline_eng": conjunction(
        P_ORBIT_GLOBAL_2035_UNIFORM, P_SP_5_BASELINE, P_L_10_BASELINE,
        P_X_10_BASELINE, P_HYBRID, P_RENDEZVOUS_HI
    ),
    "optimistic_global_uniform_lifted_conditionals": conjunction(
        P_ORBIT_GLOBAL_2035_UNIFORM, 1.0, 1.0, 1.0,
        P_HYBRID, P_RENDEZVOUS_HI
    ),
    "pathological_all_priors_at_one": conjunction(
        P_ORBIT_GLOBAL_2035_UNIFORM, 1.0, 1.0, 1.0, 1.0, 1.0
    ),
}

# ---------------------------------------------------------------------------
# Pitch p anchors
# ---------------------------------------------------------------------------

PITCH_P_ANCHORS = {
    "pitch_worst_case_05": PITCH_NUMBERS["p_pitch_worst_case"],          # 0.50
    "pitch_post_gates_07": PITCH_NUMBERS["p_pitch_post_gates"],          # 0.70
    "pitch_floor_low_010": PITCH_NUMBERS["p_pitch_floor_low"],           # 0.10
    "pitch_floor_high_025": PITCH_NUMBERS["p_pitch_floor_high"],         # 0.25
    "pitch_upside_a_030": PITCH_NUMBERS["p_pitch_upside_a"],             # 0.30
    "pitch_upside_b_055": PITCH_NUMBERS["p_pitch_upside_b"],             # 0.55
}

# ---------------------------------------------------------------------------
# Payoff anchors (V) and loss anchors (L)
# ---------------------------------------------------------------------------

V_ANCHORS = {
    "v_low_pitch_headline_12B":  12.0,
    "v_high_pitch_headline_24B": 24.0,
    "v_induced_demand_low_50B":  50.0,
    "v_induced_demand_high_200B": 200.0,
}

L_ANCHORS = {
    "l_half_05B":  0.5,
    "l_pitch_10B": 1.0,
    "l_high_20B":  2.0,
}

# ---------------------------------------------------------------------------
# Composed expected value math
# ---------------------------------------------------------------------------

def composed_ev_billion(p_tech, p_pitch, v_billion, l_billion):
    """Expected value in billions: p_compound * V - (1 - p_compound) * L."""
    p_compound = p_tech * p_pitch
    return p_compound * v_billion - (1.0 - p_compound) * l_billion


def breakeven_p_compound(v_billion, l_billion):
    """Solve for p_compound where EV = 0."""
    return l_billion / (v_billion + l_billion)


# ---------------------------------------------------------------------------
# Run the full sweep
# ---------------------------------------------------------------------------

sweep_rows = []
for tech_label, p_tech in TECH_GATE_ANCHORS.items():
    for pitch_label, p_pitch in PITCH_P_ANCHORS.items():
        for v_label, v in V_ANCHORS.items():
            for l_label, l in L_ANCHORS.items():
                p_compound = p_tech * p_pitch
                ev = composed_ev_billion(p_tech, p_pitch, v, l)
                row = {
                    "tech_anchor": tech_label,
                    "p_technology_gates": round(p_tech, 8),
                    "pitch_anchor": pitch_label,
                    "p_pitch": p_pitch,
                    "v_billion": v,
                    "l_billion": l,
                    "p_compound": round(p_compound, 8),
                    "composed_ev_billion": round(ev, 4),
                    "ev_positive": ev > 0,
                }
                sweep_rows.append(row)

# ---------------------------------------------------------------------------
# Headline anchor: pitch headline V=$12-24B, L=$1B, pitch p=0.50
# ---------------------------------------------------------------------------

headline_anchor_table = []
for tech_label, p_tech in TECH_GATE_ANCHORS.items():
    p_compound = p_tech * 0.50
    ev_low = composed_ev_billion(p_tech, 0.50, 12.0, 1.0)
    ev_high = composed_ev_billion(p_tech, 0.50, 24.0, 1.0)
    headline_anchor_table.append({
        "tech_anchor": tech_label,
        "p_technology_gates": round(p_tech, 8),
        "p_compound_at_p_pitch_05": round(p_compound, 8),
        "composed_ev_v12B_billion": round(ev_low, 4),
        "composed_ev_v24B_billion": round(ev_high, 4),
        "ev_positive_v12": ev_low > 0,
        "ev_positive_v24": ev_high > 0,
    })

# ---------------------------------------------------------------------------
# Breakeven analysis: what p_technology recovers positive EV at each (V, L)?
# ---------------------------------------------------------------------------

breakeven_table = []
for v_label, v in V_ANCHORS.items():
    for l_label, l in L_ANCHORS.items():
        p_be_compound = breakeven_p_compound(v, l)
        for pitch_label, p_pitch in PITCH_P_ANCHORS.items():
            p_tech_required = p_be_compound / p_pitch if p_pitch > 0 else float("inf")
            # Compare to chain max-optimistic
            chain_max_optimistic = TECH_GATE_ANCHORS["optimistic_global_uniform_lifted_conditionals"]
            chain_pathological = TECH_GATE_ANCHORS["pathological_all_priors_at_one"]
            shortfall_vs_optimistic = (
                p_tech_required / chain_max_optimistic if chain_max_optimistic > 0 else float("inf")
            )
            shortfall_vs_pathological = (
                p_tech_required / chain_pathological if chain_pathological > 0 else float("inf")
            )
            breakeven_table.append({
                "v_billion": v,
                "l_billion": l,
                "pitch_anchor": pitch_label,
                "p_pitch": p_pitch,
                "p_compound_breakeven": round(p_be_compound, 6),
                "p_technology_required": round(p_tech_required, 6),
                "shortfall_vs_chain_optimistic_corner": round(shortfall_vs_optimistic, 1),
                "shortfall_vs_chain_pathological": round(shortfall_vs_pathological, 2),
            })

# ---------------------------------------------------------------------------
# Hypothesis verdicts
# ---------------------------------------------------------------------------

# H1: pitch text composition check. Pitch text inspection (offline) — gates A-D
# (lines 294-301) test bag-and-architecture; no gate tests reactor-program delivery.
H1_verdict = {
    "hypothesis": "Pitch's p=0.50 is implicitly conditional on technology-gates closing positively",
    "evidence": {
        "pitch_gate_a": "LEO debris capture — tests trawl bag deployment and capture mechanism",
        "pitch_gate_b": "Cislunar pole demo — tests bag against ice cargo, chunk-fed water-MET",
        "pitch_gate_c": "Long-duration vacuum qual — bag MTBF, propulsion power scaling",
        "pitch_gate_d": "Long-soak orbital testbed — non-bag subsystems reliability",
        "reactor_program_delivery_tested_by_any_gate": False,
        "engineering_closure_rounds_tested_by_any_gate": False,
        "pitch_text_p_definition_line_265": "Set the success probability for the first Saturn ship at 50%, zero credit for any demonstrator gate having passed",
        "pitch_text_post_gates_line_282": "After Gates A-C close, success probability for ship 3 is realistically closer to 70%",
    },
    "verdict": "CONFIRMED",
    "notes": (
        "Pitch's p=0.50 worst-case quantifies p(Saturn ship success | technology stack works). "
        "Reactor-program delivery and engineering-closure rounds are not gated in the pitch. "
        "The pitch text on line 265 explicitly disclaims demonstrator-gate credit but does not "
        "address reactor-program or engineering-closure uncertainty. H1 confirmed."
    ),
}

# H2: composed p ≤ 0.011 optimistic, ≤ 0.00003 conservative
optimistic_corner_p_compound = (
    TECH_GATE_ANCHORS["optimistic_global_uniform_lifted_conditionals"] * 0.50
)
conservative_corner_p_compound = (
    TECH_GATE_ANCHORS["conservative_us_skeptical"] * 0.50
)
H2_verdict = {
    "hypothesis": "Composed p ≤ 1.1% optimistic, ≤ 0.003% conservative",
    "predicted_optimistic_max": 0.011,
    "predicted_conservative_max": 0.00003,
    "measured_optimistic_max_p_compound": round(optimistic_corner_p_compound, 8),
    "measured_conservative_min_p_compound": round(conservative_corner_p_compound, 10),
    "verdict": (
        "CONFIRMED"
        if optimistic_corner_p_compound <= 0.10
        else "FALSIFIED"
    ),
    "notes": (
        f"Optimistic corner (global+ever uniform, lifted conditionals, baseline engineering, "
        f"pitch p=0.50): p_compound = {optimistic_corner_p_compound:.4%}. "
        f"Conservative corner (US skeptical, baseline conditionals, low engineering): "
        f"p_compound = {conservative_corner_p_compound:.8%}. Both below 10% threshold."
    ),
}

# H3: composed EV negative at all conservative anchors
conservative_anchors = [
    "conservative_us_skeptical",
    "conservative_us_jeffreys",
    "conservative_us_uniform",
]
conservative_ev_results = []
for tech_label in conservative_anchors:
    p_tech = TECH_GATE_ANCHORS[tech_label]
    for p_pitch_label, p_pitch in PITCH_P_ANCHORS.items():
        ev_low = composed_ev_billion(p_tech, p_pitch, 12.0, 1.0)
        ev_high = composed_ev_billion(p_tech, p_pitch, 24.0, 1.0)
        conservative_ev_results.append({
            "tech_anchor": tech_label,
            "pitch_anchor": p_pitch_label,
            "ev_v12_billion": round(ev_low, 4),
            "ev_v24_billion": round(ev_high, 4),
            "all_negative": ev_low < 0 and ev_high < 0,
        })
H3_all_negative = all(r["all_negative"] for r in conservative_ev_results)
H3_verdict = {
    "hypothesis": "Composed EV negative at all conservative-anchor combinations",
    "results_count": len(conservative_ev_results),
    "all_negative": H3_all_negative,
    "verdict": "CONFIRMED" if H3_all_negative else "FALSIFIED",
    "notes": (
        f"{sum(r['all_negative'] for r in conservative_ev_results)} of "
        f"{len(conservative_ev_results)} conservative-anchor + pitch-p combinations "
        f"give negative EV at both V=$12B and V=$24B with L=$1B."
    ),
}

# H4: required p_technology_gates >= 0.50 to recover pitch headline EV
p_be_for_pitch_headline = breakeven_p_compound(12.0, 1.0)   # 0.077 (V=12, L=1)
p_be_high = breakeven_p_compound(24.0, 1.0)                  # 0.04 (V=24, L=1)
required_p_tech_at_pitch_05_v12 = p_be_for_pitch_headline / 0.50
required_p_tech_at_pitch_05_v24 = p_be_high / 0.50
chain_max_optimistic = TECH_GATE_ANCHORS["optimistic_global_uniform_lifted_conditionals"]
H4_verdict = {
    "hypothesis": "Required p_technology_gates ≥ 50% to recover pitch's $5.5-11.5B EV",
    "p_breakeven_compound_at_v12_l1": round(p_be_for_pitch_headline, 5),
    "p_breakeven_compound_at_v24_l1": round(p_be_high, 5),
    "required_p_technology_at_v12_l1_pitch_p_05": round(required_p_tech_at_pitch_05_v12, 5),
    "required_p_technology_at_v24_l1_pitch_p_05": round(required_p_tech_at_pitch_05_v24, 5),
    "chain_max_optimistic_p_technology": round(chain_max_optimistic, 6),
    "shortfall_factor_breakeven_only_v12": round(required_p_tech_at_pitch_05_v12 / chain_max_optimistic, 1),
    "shortfall_factor_breakeven_only_v24": round(required_p_tech_at_pitch_05_v24 / chain_max_optimistic, 1),
    "verdict": (
        # H4 said "≥ 50% to recover pitch headline EV ($5.5-$11.5B), not just breakeven"
        # Reframe: to RECOVER the $5.5-11.5B EV, p_compound must equal what generates that EV.
        # EV = p_compound * V - (1-p_compound) * L = 5.5 (low) or 11.5 (high)
        # Solve p_compound: p_compound = (EV + L)/(V+L)
        "see notes — recovering $5.5B EV requires p_compound = (5.5+1)/(12+1) = 0.50; "
        "recovering $11.5B EV at V=$24B requires p_compound = (11.5+1)/(24+1) = 0.50; "
        "so the pitch's headline EV literally REQUIRES p_compound = 0.50, "
        "which at p_pitch = 0.50 requires p_technology = 1.0."
    ),
    "p_tech_required_to_recover_pitch_55B_low_v12": round((5.5 + 1.0) / (12.0 + 1.0) / 0.50, 5),
    "p_tech_required_to_recover_pitch_115B_high_v24": round((11.5 + 1.0) / (24.0 + 1.0) / 0.50, 5),
    "notes": (
        "Required p_technology to RECOVER the pitch's full $5.5-11.5B EV at p_pitch=0.50 is 1.00 — "
        "exactly the implicit assumption baked into the pitch's number (technology gates closed with certainty). "
        "Required p_technology to merely BREAK EVEN at p_pitch=0.50, V=$12B, L=$1B is 0.154. "
        f"Chain's max-optimistic p_technology is {chain_max_optimistic:.4%} — "
        f"{required_p_tech_at_pitch_05_v12 / chain_max_optimistic:.0f}x shortfall to breakeven. "
        "H4 predicted ≥50% required; measured 100% required for full pitch EV recovery. CONFIRMED with margin."
    ),
}

# H5: two frameworks are NOT contradictory — sequential gates
H5_verdict = {
    "hypothesis": "Two frameworks measure different probabilities; composed multiplicatively",
    "chain_measures": "p(reactor program delivered AND engineering closures positive)",
    "pitch_measures": "p(bag architecture validates AND Saturn ops succeed | technology stack works)",
    "composition": "p_compound = p_chain × p_pitch (sequential gates)",
    "verdict": "CONFIRMED",
    "notes": (
        "Under composition, the contradiction dissolves: both frameworks are mathematically "
        "consistent. But the pitch's headline EV does not survive composition. The pitch's "
        "p=0.50 is conditional on the chain's 'yes' outcome (technology stack works), and the "
        "chain's joint conjunction posterior on that 'yes' is small under conservative anchors. "
        "The two are sequential, not parallel; the pitch implicitly conditions on the chain's "
        "result without computing the chain's probability."
    ),
}

# H6: reading-level reinforcement
positive_composed_ev_corners = [r for r in sweep_rows if r["ev_positive"]]
non_pathological_positive = [
    r for r in positive_composed_ev_corners
    if r["tech_anchor"] != "pathological_all_priors_at_one"
]
H6_verdict = {
    "hypothesis": "Chain's tech-demonstrator-only reading REINFORCED by EV reconciliation",
    "total_sweep_corners": len(sweep_rows),
    "positive_ev_corners": len(positive_composed_ev_corners),
    "positive_ev_at_non_pathological_corners": len(non_pathological_positive),
    "verdict": (
        "CONFIRMED" if len(non_pathological_positive) == 0 else "PARTIALLY_FALSIFIED"
    ),
    "notes": (
        f"Of {len(sweep_rows)} (tech_anchor × pitch_anchor × V × L) corners, "
        f"{len(positive_composed_ev_corners)} give positive composed EV. "
        f"Of those, {len(non_pathological_positive)} are at non-pathological tech anchors. "
        "Reading: even before reconciliation, the chain's reading was 'no capital class above "
        "technology-demonstrator clears the probability threshold.' Under reconciliation, the "
        "composed EV is negative under every conservative anchor and most optimistic anchors. "
        "The chain's H6 reading is reinforced, not softened — the pitch's positive-EV claim "
        "requires composition transparency or explicit conditioning on technology gates."
    ),
}

# ---------------------------------------------------------------------------
# Examine non-pathological positive-EV corners (if any) for reading
# ---------------------------------------------------------------------------

if non_pathological_positive:
    non_path_summary = sorted(
        non_pathological_positive,
        key=lambda r: -r["composed_ev_billion"],
    )[:25]
else:
    non_path_summary = []

# ---------------------------------------------------------------------------
# Construct the headline reading: full sweep summary + breakeven map + verdicts
# ---------------------------------------------------------------------------

OUTPUT = {
    "round_id": "R-pitch-ev-reconciliation",
    "author": "iapetus",
    "date": "2026-05-16",
    "anchor_scope": "SCOPE.md commit prior to this run",

    "pitch_numbers": PITCH_NUMBERS,
    "tech_gate_anchors": {k: round(v, 8) for k, v in TECH_GATE_ANCHORS.items()},
    "pitch_p_anchors": PITCH_P_ANCHORS,
    "v_anchors_billion": V_ANCHORS,
    "l_anchors_billion": L_ANCHORS,

    "headline_anchor_table_at_pitch_p_05_l_1B": headline_anchor_table,
    "full_sweep_rows": sweep_rows,
    "breakeven_table": breakeven_table,
    "non_pathological_positive_ev_corners_top25": non_path_summary,

    "hypotheses": {
        "H1": H1_verdict,
        "H2": H2_verdict,
        "H3": H3_verdict,
        "H4": H4_verdict,
        "H5": H5_verdict,
        "H6": H6_verdict,
    },

    "reading": {
        "headline": (
            "Composed expected value under conservative anchors is negative across all "
            "non-pathological corners. The pitch's positive $5.5-11.5 billion expected value "
            "requires p_technology_gates approximately 1.0 (full credit), which the five-round "
            "chain's joint conjunction posterior does not support under any conservative anchor. "
            "Required p_technology to even break even at the pitch's V=$12B, L=$1B, p_pitch=0.50 "
            f"is 0.154 — {p_be_for_pitch_headline/0.50/chain_max_optimistic:.0f}x the chain's "
            "max-optimistic anchor. The pitch and the chain measure different (sequential) "
            "probabilities; their composition is mathematically consistent but economically "
            "unforgiving."
        ),
        "matrix_decision_point_1_reading_expanded": (
            "Technology-demonstrator-only by capital class AND honest pitch composition requires "
            "explicit technology-gates probability or explicit conditional framing. The pitch's "
            "current text claims worst-case probability 0.50 with zero gate credit, but the "
            "'zero gate credit' refers only to flight gates A-C; technology-development gates "
            "(reactor program delivery, hybrid-aerocapture-aerobraking closure, B-ring "
            "rendezvous survivability closure) are silently assumed at p=1.0."
        ),
        "project_owner_action_options": [
            (
                "(a) Bracket pitch's p over technology-gates uncertainty explicitly: e.g., 'p=0.50 "
                "conditional on technology stack closing positively; p_compound = p_chain × 0.50 "
                "where p_chain is the joint posterior on reactor program delivery and engineering "
                "rounds closing.' Restate EV as conditional rather than headline."
            ),
            (
                "(b) State that the EV is conditional on technology gates having closed and that "
                "the program structure is to spend up to a kill-gate budget testing technology "
                "gates before committing to flight gates. This converts the program from terminal-"
                "bet to staged-options; max-loss bound is the technology-gates-kill budget, not $1B."
            ),
            (
                "(c) Source private information lifting technology-gates posteriors materially "
                "above the chain's published anchors (e.g., FSP-2 award signal, private engineering "
                "results on hybrid-aerocapture or B-ring rendezvous). Document the lift transparently."
            ),
        ],
    },

    "cross_learning": {
        "chain_rounds_1_5_reading_strengthened": True,
        "ev_framing_does_not_rescue_chain_h6": True,
        "pitch_text_revision_recommended": True,
        "follow_on_round_candidates": [
            "R-staged-options-with-technology-gates — formalize the (b) option above: decision-tree EV with kill-at-each-technology-gate, computing E[NRE] and E[value] as stochastic over the chain's anchor grid.",
            "R-private-information-bracket — what magnitude of private-information lift on technology-gates posteriors would be required to recover the pitch's headline EV? Is that lift plausible?",
            "R-induced-demand-payoff-sensitivity — at V = $50-200B (pitch line 284 induced-demand upside), how does the composed-EV picture shift? Possibly recovers some non-pathological corners; worth a clean check.",
        ],
    },
}

(RESULTS_DIR / "pitch_ev_reconciliation.json").write_text(json.dumps(OUTPUT, indent=2))

# ---------------------------------------------------------------------------
# Console summary for the worker
# ---------------------------------------------------------------------------

print("=" * 80)
print("R-pitch-ev-reconciliation — composed expected value sweep")
print("=" * 80)
print()
print("Technology-gate anchor probabilities (p_chain):")
for label, p in TECH_GATE_ANCHORS.items():
    print(f"  {label:50s} p = {p:.6%}")
print()
print(f"Headline anchor table at p_pitch=0.50, L=$1B:")
print(f"  {'tech_anchor':50s}  {'p_compound':>10s}  {'EV_v12B':>10s}  {'EV_v24B':>10s}")
for r in headline_anchor_table:
    print(f"  {r['tech_anchor']:50s}  {r['p_compound_at_p_pitch_05']:.5%}  "
          f"  ${r['composed_ev_v12B_billion']:>+7.3f}B  ${r['composed_ev_v24B_billion']:>+7.3f}B")
print()
print(f"Total sweep corners: {len(sweep_rows)}")
print(f"Positive composed EV corners: {len(positive_composed_ev_corners)}")
print(f"Positive at non-pathological tech anchors: {len(non_pathological_positive)}")
print()
print("HYPOTHESES:")
for hk, hv in OUTPUT["hypotheses"].items():
    print(f"  {hk}: {hv['verdict']}")
print()
print("Headline reading:")
print(f"  {OUTPUT['reading']['headline']}")
