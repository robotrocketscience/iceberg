"""
R-conditional-prior-sensitivity — flexes the subjective conditional priors
(p_sp, p_L, p_X) that I held fixed across rounds 1-4. Qualifies the round 4
"structurally over-determined" claim.

Author: iapetus, 2026-05-15 (latest+9)
Pre-registration: SCOPE.md (H1-H5)
"""

from __future__ import annotations

import json
from itertools import product
from pathlib import Path

RESULTS_DIR = Path(__file__).parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

PRIOR_TARGETS = json.loads(
    (PROJECT_ROOT / "R_reactor_specific_power_program_targets" / "results" / "reactor_program_targets.json").read_text()
)
PRIOR_WINDOW = json.loads(
    (PROJECT_ROOT / "R_demonstrator_window_sensitivity" / "results" / "demonstrator_window_sensitivity.json").read_text()
)
PRIOR_GLOBAL = json.loads(
    (PROJECT_ROOT / "R_global_vs_us_base_rate" / "results" / "global_vs_us_base_rate.json").read_text()
)

# ---------------------------------------------------------------------------
# Baseline values from round 1 (the anchors I'm now flexing)
# ---------------------------------------------------------------------------

BASELINE_SP_PRIOR = {float(k): v for k, v in PRIOR_TARGETS["subjective_priors"]["p_sp_geq_given_orbit_500kWe"].items()}
BASELINE_L_PRIOR_RAW = PRIOR_TARGETS["subjective_priors"]["p_L_geq_given_orbit_500kWe"]
BASELINE_L_PRIOR = {float("inf") if k == "inf" else float(k): v for k, v in BASELINE_L_PRIOR_RAW.items()}
BASELINE_X_PRIOR = {float(k): v for k, v in PRIOR_TARGETS["subjective_priors"]["p_X_geq_given_hybrid_closes"].items()}
MIN_CORNERS = PRIOR_TARGETS["min_corner_table"]

P_HYBRID_BASELINE = PRIOR_TARGETS["subjective_priors"]["P_HYBRID_AEROCAP"]   # 0.5
P_RENDEZVOUS_HI_BASELINE = PRIOR_TARGETS["subjective_priors"]["P_RENDEZVOUS_HI"]  # 0.3

# ---------------------------------------------------------------------------
# Base-rate × window p_500_orbit posteriors
# ---------------------------------------------------------------------------

us_p_500 = PRIOR_WINDOW["p_500kWe_orbit_by_window_and_prior"]["uniform_beta_1_1"]
global_p_500 = {str(r["window_year"]): r["uniform_beta_1_1_p_500"] for r in PRIOR_GLOBAL["global_table"]}

# ---------------------------------------------------------------------------
# Conditional-prior sweep
# ---------------------------------------------------------------------------

P_SP_AT_5 = [0.40, 0.60, 0.80, 0.95, 1.00]    # baseline 0.40
P_L_AT_10 = [0.40, 0.60, 0.80, 0.95, 1.00]    # baseline 0.40
P_X_AT_10 = [0.70, 0.85, 0.95, 1.00]          # baseline 0.70

CAPITAL_CLASSES = [
    ("technology_demonstrator", 0.0),
    ("venture",                 0.10),
    ("corporate_growth",        0.30),
    ("regulated_utility",       0.50),
    ("sovereign_bond",          0.80),
]


def capital_class(p: float) -> str:
    last = "infeasible"
    for name, threshold in CAPITAL_CLASSES:
        if p >= threshold:
            last = name
    return last


def conjunction_for_overrides(
    p_500_orbit: float,
    p_sp_at_5: float,
    p_L_at_10: float,
    p_X_at_10: float,
    p_hybrid: float,
    p_rendezvous: float,
) -> tuple[float, dict | None]:
    """Max conjunction over min-corners with the given overrides on (sp=5, L=10, X=10) priors."""
    sp_prior = dict(BASELINE_SP_PRIOR)
    sp_prior[5.0] = p_sp_at_5
    L_prior = dict(BASELINE_L_PRIOR)
    L_prior[10.0] = p_L_at_10
    x_prior = dict(BASELINE_X_PRIOR)
    x_prior[10.0] = p_X_at_10

    best_p, best_c = 0.0, None
    for c in MIN_CORNERS:
        sp = c["min_sp_w_per_kg"]
        X = c["X_km_s"]
        L_yr = c["L_yr"]
        L_key = float("inf") if L_yr == "inf" else float(L_yr)
        p_sp = sp_prior[sp]
        p_L = L_prior[L_key]
        p_aero = (p_hybrid * x_prior[X]) if X > 0 else 1.0
        p = p_500_orbit * p_sp * p_L * p_aero * p_rendezvous
        if p > best_p:
            best_p = p
            best_c = c
    return best_p, best_c


# ---------------------------------------------------------------------------
# Full sweep: conditional priors × base-rate × window (engineering at baseline)
# ---------------------------------------------------------------------------

BASE_RATE_WINDOWS = [
    ("us_only_uniform", "2035", us_p_500["2035"]),
    ("us_only_uniform", "ever", us_p_500["ever"]),
    ("global_uniform",  "2035", global_p_500["2035"]),
    ("global_uniform",  "ever", global_p_500["ever"]),
]

sweep_results = []
for base_rate, window, p_500 in BASE_RATE_WINDOWS:
    for p_sp, p_L, p_X in product(P_SP_AT_5, P_L_AT_10, P_X_AT_10):
        conj, _ = conjunction_for_overrides(p_500, p_sp, p_L, p_X, P_HYBRID_BASELINE, P_RENDEZVOUS_HI_BASELINE)
        compound_conditional = p_sp * p_L * p_X
        sweep_results.append({
            "base_rate": base_rate,
            "window": window,
            "p_500_orbit": p_500,
            "p_sp_at_5": p_sp,
            "p_L_at_10": p_L,
            "p_X_at_10": p_X,
            "conditional_compound": compound_conditional,
            "max_conjunction": conj,
            "capital_class": capital_class(conj),
        })


# ---------------------------------------------------------------------------
# Single-axis-lift analysis (H4): hold two priors at baseline, sweep one
# ---------------------------------------------------------------------------

single_axis = {}
for base_rate, window, p_500 in BASE_RATE_WINDOWS:
    label = f"{base_rate}_{window}"
    single_axis[label] = {"p_500_orbit": p_500}

    # Lift only p_sp at sp=5 from baseline 0.40 to 1.00
    sp_lift_results = []
    for p_sp in P_SP_AT_5:
        conj, _ = conjunction_for_overrides(p_500, p_sp, 0.40, 0.70, P_HYBRID_BASELINE, P_RENDEZVOUS_HI_BASELINE)
        sp_lift_results.append({"p_sp_at_5": p_sp, "max_conjunction": conj, "capital_class": capital_class(conj)})
    single_axis[label]["sp_lift_only"] = sp_lift_results

    # Lift only p_L at L=10
    l_lift_results = []
    for p_L in P_L_AT_10:
        conj, _ = conjunction_for_overrides(p_500, 0.40, p_L, 0.70, P_HYBRID_BASELINE, P_RENDEZVOUS_HI_BASELINE)
        l_lift_results.append({"p_L_at_10": p_L, "max_conjunction": conj, "capital_class": capital_class(conj)})
    single_axis[label]["L_lift_only"] = l_lift_results

    # Lift only p_X at X=10
    x_lift_results = []
    for p_X in P_X_AT_10:
        conj, _ = conjunction_for_overrides(p_500, 0.40, 0.40, p_X, P_HYBRID_BASELINE, P_RENDEZVOUS_HI_BASELINE)
        x_lift_results.append({"p_X_at_10": p_X, "max_conjunction": conj, "capital_class": capital_class(conj)})
    single_axis[label]["X_lift_only"] = x_lift_results


# ---------------------------------------------------------------------------
# Find conditional-prior compound breakevens
# ---------------------------------------------------------------------------

THRESHOLDS = {"venture": 0.10, "corp_growth": 0.30, "regulated_utility": 0.50}


def find_compound_breakeven(base_rate: str, window: str, threshold: float) -> dict:
    """Find the minimum conditional-prior compound that crosses threshold."""
    candidates = [r for r in sweep_results if r["base_rate"] == base_rate and r["window"] == window and r["max_conjunction"] >= threshold]
    if not candidates:
        return {"crossable": False, "min_compound": None}
    candidates.sort(key=lambda r: r["conditional_compound"])
    cmin = candidates[0]
    return {
        "crossable": True,
        "min_compound": cmin["conditional_compound"],
        "min_p_sp_at_5": cmin["p_sp_at_5"],
        "min_p_L_at_10": cmin["p_L_at_10"],
        "min_p_X_at_10": cmin["p_X_at_10"],
        "max_conjunction_at_min": cmin["max_conjunction"],
    }


breakevens = {}
for base_rate, window, _ in BASE_RATE_WINDOWS:
    breakevens[f"{base_rate}_{window}"] = {}
    for tname, tval in THRESHOLDS.items():
        breakevens[f"{base_rate}_{window}"][tname] = find_compound_breakeven(base_rate, window, tval)


# ---------------------------------------------------------------------------
# Combined-axis sanity check (H3): all conditionals at 1.0 + baseline engineering
# ---------------------------------------------------------------------------

combined_max_at_baseline_engineering = {}
for base_rate, window, p_500 in BASE_RATE_WINDOWS:
    conj, _ = conjunction_for_overrides(p_500, 1.0, 1.0, 1.0, P_HYBRID_BASELINE, P_RENDEZVOUS_HI_BASELINE)
    combined_max_at_baseline_engineering[f"{base_rate}_{window}"] = {
        "p_500_orbit": p_500,
        "max_conjunction_all_conditionals_1": conj,
        "capital_class": capital_class(conj),
    }


# ---------------------------------------------------------------------------
# Hypotheses adjudication
# ---------------------------------------------------------------------------

# H1: under US-only at 2035 baseline, breakeven compound ≥ 5.0 (unreachable)
h1 = breakevens["us_only_uniform_2035"]["venture"]
h1_verdict = "CONFIRMED" if not h1["crossable"] else "FALSIFIED"

# H2: under global+ever, breakeven compound ≥ 0.69 (plausibility-edge)
h2 = breakevens["global_uniform_ever"]["venture"]
h2_compound = h2.get("min_compound") if h2["crossable"] else None
h2_verdict = "CONFIRMED" if (h2["crossable"] and h2_compound >= 0.69) or (not h2["crossable"]) else "FALSIFIED"

# H3: all conditionals at 1.0 + baseline engineering ≤ 3% at global+ever
h3_conjunction = combined_max_at_baseline_engineering["global_uniform_ever"]["max_conjunction_all_conditionals_1"]
h3_verdict = "CONFIRMED" if h3_conjunction <= 0.03 else "FALSIFIED"

# H4: no single-axis lift crosses venture at US-only+2035 baseline
h4_us_2035 = single_axis["us_only_uniform_2035"]
h4_any_single_crosses = any(
    r["max_conjunction"] >= 0.10
    for axis in ("sp_lift_only", "L_lift_only", "X_lift_only")
    for r in h4_us_2035[axis]
)
h4_verdict = "CONFIRMED" if not h4_any_single_crosses else "FALSIFIED"

# H5: combined-lift requirement ≥ 16× at global+ever
# Compute current baseline conjunction at global+ever then ratio against breakeven-conjunction-equivalent
baseline_conj_global_ever, _ = conjunction_for_overrides(
    global_p_500["ever"], 0.40, 0.40, 0.70, P_HYBRID_BASELINE, P_RENDEZVOUS_HI_BASELINE,
)
# venture-equivalent lift = 0.10 / baseline_conj
h5_lift_factor = 0.10 / baseline_conj_global_ever if baseline_conj_global_ever > 0 else None
h5_verdict = "CONFIRMED" if (h5_lift_factor is not None and h5_lift_factor >= 16.0) else "FALSIFIED"


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

out = {
    "round": "R-conditional-prior-sensitivity",
    "author": "iapetus",
    "date": "2026-05-15",
    "pre_registration": "SCOPE.md (H1-H5)",
    "honest_meta": "This round qualifies round 4's 'structurally over-determined' claim. The over-determination only held under conservative conditional-prior anchors; this round flexes them.",
    "p_sp_at_5_sweep": P_SP_AT_5,
    "p_L_at_10_sweep": P_L_AT_10,
    "p_X_at_10_sweep": P_X_AT_10,
    "engineering_priors_held": {
        "P_HYBRID": P_HYBRID_BASELINE,
        "P_RENDEZVOUS_HI": P_RENDEZVOUS_HI_BASELINE,
    },
    "base_rate_window_anchors": [{"base_rate": br, "window": w, "p_500_orbit": p} for br, w, p in BASE_RATE_WINDOWS],
    "single_axis_lift_table": single_axis,
    "combined_all_conditionals_1_at_baseline_engineering": combined_max_at_baseline_engineering,
    "breakevens_compound": breakevens,
    "hypotheses": {
        "H1": {
            "hypothesis": "Under US-only at 2035 + baseline engineering, venture compound breakeven >= 5.0 (unreachable)",
            "breakeven": h1,
            "verdict": h1_verdict,
        },
        "H2": {
            "hypothesis": "Under global+ever + baseline engineering, venture compound breakeven >= 0.69",
            "breakeven": h2,
            "verdict": h2_verdict,
        },
        "H3": {
            "hypothesis": "All conditionals at 1.0 + baseline engineering: max conjunction at global+ever <= 3%",
            "max_conjunction": h3_conjunction,
            "verdict": h3_verdict,
        },
        "H4": {
            "hypothesis": "No single-axis lift crosses venture at US-only + 2035 baseline",
            "verdict": h4_verdict,
            "any_single_lift_crosses_venture": h4_any_single_crosses,
        },
        "H5": {
            "hypothesis": "Combined-lift requirement at global+ever >= 16x",
            "lift_factor_needed": h5_lift_factor,
            "verdict": h5_verdict,
        },
    },
}

(RESULTS_DIR / "conditional_prior_sensitivity.json").write_text(json.dumps(out, indent=2))
print(f"Wrote {RESULTS_DIR / 'conditional_prior_sensitivity.json'}")

# ---------------------------------------------------------------------------
# Console summary
# ---------------------------------------------------------------------------

print()
print("=== Compound-conditional breakevens (engineering at baseline 0.5 × 0.30) ===")
print(f"  {'base-rate × window':>30}  {'threshold':>14}  {'min compound':>14}  {'p_sp,p_L,p_X at min':>24}")
for label_key, by_thresh in breakevens.items():
    for tname, info in by_thresh.items():
        if info["crossable"]:
            comp = f"{info['min_compound']:.3f}"
            triple = f"({info['min_p_sp_at_5']},{info['min_p_L_at_10']},{info['min_p_X_at_10']})"
        else:
            comp = "unreachable"
            triple = "—"
        print(f"  {label_key:>30}  {tname:>14}  {comp:>14}  {triple:>24}")
print()
print("=== Single-axis-lift analysis ===")
for label_key, axes in single_axis.items():
    print(f"  -- {label_key} (p_500 = {axes['p_500_orbit']:.4%}) --")
    for axis_label in ("sp_lift_only", "L_lift_only", "X_lift_only"):
        sweeps = axes[axis_label]
        crosses = any(r["max_conjunction"] >= 0.10 for r in sweeps)
        max_val = max(r["max_conjunction"] for r in sweeps)
        print(f"    {axis_label:>14}: max conjunction = {max_val:.4%}; crosses venture = {crosses}")
print()
print("=== Combined: ALL conditionals at 1.0, engineering at baseline (0.5 × 0.30) ===")
for label_key, info in combined_max_at_baseline_engineering.items():
    print(f"  {label_key:>30}: max conjunction = {info['max_conjunction_all_conditionals_1']:.4%} ({info['capital_class']})")
print()
print("=== Hypotheses verdicts ===")
for h, v in out["hypotheses"].items():
    print(f"  {h}: {v['verdict']}")
