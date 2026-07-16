"""
R-demonstrator-window-sensitivity — does extending the demonstrator window flip
the H6 reading from R-reactor-specific-power-program-targets?

Re-runs the R-power-bayesian-update Bayesian Monte Carlo with a swept window
endpoint, then re-applies the R-reactor-specific-power-program-targets
conditional-prior chain at each endpoint.

Author: iapetus, 2026-05-15 (latest+9)
Pre-registration: SCOPE.md (H1-H5)
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

RESULTS_DIR = Path(__file__).parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

PRIOR_ROUND = json.loads((PROJECT_ROOT / "R_reactor_specific_power_program_targets" / "results" / "reactor_program_targets.json").read_text())

# ---------------------------------------------------------------------------
# Bayesian Monte Carlo (verbatim re-implementation of R-power-bayesian-update)
# ---------------------------------------------------------------------------

N_TRAJECTORIES = 10_000
SEED = 0
BASE_YEAR = 2026

PRIORS = {
    "uniform_beta_1_1":      (1.0, 1.0),
    "jeffreys_beta_0p5_0p5": (0.5, 0.5),
    "skeptical_beta_0p5_5":  (0.5, 5.0),
}

FSP_LIKELIHOOD_FACTORS = [
    ("phase1_awarded_2022",             1.40, 0.10),
    ("phase1_extended_2024",            0.85, 0.10),
    ("duffy_directive_2025_scope_grew", 0.90, 0.15),
    ("draft_afpp_aug_2025",             1.25, 0.10),
    ("no_phase2_contract_may_2026",     0.80, 0.10),
    ("fy26_budget_zeroed_nep_ntp",      0.70, 0.15),
]

P_500_FUNDED_GIVEN_FSP = 0.6
FSP_TO_500_GAP_MEAN = 4.0
FSP_TO_500_GAP_STDEV = 2.0


def sample_fsp_500_year_offsets(alpha_prior: float, beta_prior: float, rng: np.random.Generator) -> np.ndarray:
    """Return the 500-kilowatt-electric scope year-offset (from BASE_YEAR) for N_TRAJECTORIES samples."""
    alpha_post = alpha_prior + 0.0
    beta_post = beta_prior + 6.0
    lam_decade = rng.beta(alpha_post, beta_post, size=N_TRAJECTORIES)
    lam_decade_clipped = np.clip(lam_decade, 1e-6, 0.999)
    lam_annual = -np.log(1.0 - lam_decade_clipped) / 10.0
    fsp_product = np.ones(N_TRAJECTORIES)
    for _name, factor, stdev in FSP_LIKELIHOOD_FACTORS:
        sampled = rng.normal(loc=factor, scale=stdev, size=N_TRAJECTORIES)
        sampled = np.clip(sampled, 0.05, 5.0)
        fsp_product *= sampled
    fsp_adjusted_lam = lam_annual * fsp_product
    fsp_year_offset = rng.exponential(scale=1.0 / np.maximum(fsp_adjusted_lam, 1e-6), size=N_TRAJECTORIES)
    fsp_year_offset = np.minimum(fsp_year_offset, 50.0)
    fsp_succeeded = fsp_year_offset < 50.0

    fsp500_funded = rng.uniform(size=N_TRAJECTORIES) < P_500_FUNDED_GIVEN_FSP
    fsp500_attempt_starts = fsp_year_offset + np.maximum(
        rng.normal(loc=FSP_TO_500_GAP_MEAN, scale=FSP_TO_500_GAP_STDEV, size=N_TRAJECTORIES),
        1.0,
    )
    fsp500_lam_decade = rng.beta(alpha_post, beta_post, size=N_TRAJECTORIES)
    fsp500_lam_decade_clipped = np.clip(fsp500_lam_decade, 1e-6, 0.999)
    fsp500_lam_annual = -np.log(1.0 - fsp500_lam_decade_clipped) / 10.0
    fsp500_orbit_after_start = rng.exponential(
        scale=1.0 / np.maximum(fsp500_lam_annual, 1e-6), size=N_TRAJECTORIES
    )
    fsp500_orbit_after_start = np.minimum(fsp500_orbit_after_start, 30.0)
    fsp500_year_offset = fsp500_attempt_starts + fsp500_orbit_after_start
    fsp500_arrives = fsp_succeeded & fsp500_funded & (fsp500_orbit_after_start < 30.0)
    fsp500_year_offset = np.where(fsp500_arrives, fsp500_year_offset, np.inf)
    return fsp500_year_offset


# ---------------------------------------------------------------------------
# Window sweep
# ---------------------------------------------------------------------------

WINDOW_YEARS = [2032, 2035, 2040, 2045, 2050, 2055, 2060, 2070, "ever"]


def p_500_by_year(fsp500_year_offset: np.ndarray, year_or_ever) -> float:
    if year_or_ever == "ever":
        return float(np.mean(np.isfinite(fsp500_year_offset)))
    offset = year_or_ever - BASE_YEAR
    return float(np.mean(fsp500_year_offset <= offset))


rng = np.random.default_rng(SEED)
prior_year_grid: dict[str, dict] = {}
for prior_name, (a, b) in PRIORS.items():
    sub_rng = np.random.default_rng(SEED + hash(prior_name) % 1000)
    offsets = sample_fsp_500_year_offsets(a, b, sub_rng)
    prior_year_grid[prior_name] = {
        str(year): p_500_by_year(offsets, year) for year in WINDOW_YEARS
    }

# ---------------------------------------------------------------------------
# Re-apply the R-reactor-specific-power-program-targets conditional-prior chain
# ---------------------------------------------------------------------------

# Pull subjective priors from prior round's output (single source of truth).
SP_PRIOR = {float(k): v for k, v in PRIOR_ROUND["subjective_priors"]["p_sp_geq_given_orbit_500kWe"].items()}
L_PRIOR_RAW = PRIOR_ROUND["subjective_priors"]["p_L_geq_given_orbit_500kWe"]
L_PRIOR = {float("inf") if k == "inf" else float(k): v for k, v in L_PRIOR_RAW.items()}
X_PRIOR = {float(k): v for k, v in PRIOR_ROUND["subjective_priors"]["p_X_geq_given_hybrid_closes"].items()}
P_HYBRID_AEROCAP = PRIOR_ROUND["subjective_priors"]["P_HYBRID_AEROCAP"]
P_RENDEZVOUS_LOW = PRIOR_ROUND["subjective_priors"]["P_RENDEZVOUS_LOW"]
P_RENDEZVOUS_HI  = PRIOR_ROUND["subjective_priors"]["P_RENDEZVOUS_HI"]

MIN_CORNERS = PRIOR_ROUND["min_corner_table"]

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


def conjunction_at_corner(corner: dict, p_500_orbit_in_window: float, rendezvous_prior: float) -> float:
    sp = corner["min_sp_w_per_kg"]
    X = corner["X_km_s"]
    L_yr = corner["L_yr"]
    L_key = float("inf") if L_yr == "inf" else float(L_yr)
    p_sp = SP_PRIOR[sp]
    p_L = L_PRIOR[L_key]
    if X > 0:
        p_aero = P_HYBRID_AEROCAP * X_PRIOR[X]
    else:
        p_aero = 1.0
    return p_500_orbit_in_window * p_sp * p_L * p_aero * rendezvous_prior


# Sensitivity table: rows = window year, columns = (prior × rendezvous-prior) → max conjunction over corners
sensitivity = []
for year_label in WINDOW_YEARS:
    row = {"window_year": year_label}
    for prior_name in PRIORS:
        p_orbit = prior_year_grid[prior_name][str(year_label)]
        row[f"{prior_name}_p_500_orbit"] = p_orbit
        for rend_label, rend in (("rend_low", P_RENDEZVOUS_LOW), ("rend_hi", P_RENDEZVOUS_HI)):
            best = 0.0
            best_corner = None
            for c in MIN_CORNERS:
                p = conjunction_at_corner(c, p_orbit, rend)
                if p > best:
                    best = p
                    best_corner = c
            row[f"{prior_name}_{rend_label}_max_conjunction"] = best
            row[f"{prior_name}_{rend_label}_capital_class"] = capital_class(best)
    sensitivity.append(row)


# ---------------------------------------------------------------------------
# Breakeven year search
# ---------------------------------------------------------------------------

VENTURE_T = 0.10
CORP_GROWTH_T = 0.30
REGULATED_UTILITY_T = 0.50

def first_year_above(threshold: float, prior_name: str, rend_label: str) -> str | int:
    for row in sensitivity:
        if row[f"{prior_name}_{rend_label}_max_conjunction"] >= threshold:
            return row["window_year"]
    return "never_in_horizon"


breakevens = {}
for prior_name in PRIORS:
    for rend_label in ("rend_low", "rend_hi"):
        breakevens[f"{prior_name}_{rend_label}_venture_breakeven"] = first_year_above(VENTURE_T, prior_name, rend_label)
        breakevens[f"{prior_name}_{rend_label}_corp_growth_breakeven"] = first_year_above(CORP_GROWTH_T, prior_name, rend_label)
        breakevens[f"{prior_name}_{rend_label}_regulated_utility_breakeven"] = first_year_above(REGULATED_UTILITY_T, prior_name, rend_label)


# ---------------------------------------------------------------------------
# First-delivery-year impact (H3)
# ---------------------------------------------------------------------------

ICEBERG_ROUND_TRIP_YR = 14  # SCOPE-anchored; the 14-yr mission from spawn to first-revenue Earth-LEO delivery


def first_delivery_year(window_year) -> str | int:
    if isinstance(window_year, str):
        return "ever+14_uncomputable"
    return window_year + ICEBERG_ROUND_TRIP_YR


first_delivery_at_breakeven = {}
for k, v in breakevens.items():
    if k.endswith("_breakeven"):
        first_delivery_at_breakeven[k.replace("_breakeven", "_first_delivery_year")] = first_delivery_year(v)


# ---------------------------------------------------------------------------
# Hypotheses adjudication
# ---------------------------------------------------------------------------

# Sanity check: my re-derived uniform p_500kWe at 2035 should ≈ hyperion's 0.0013
sanity_check = {
    "iapetus_uniform_p_500_2035": prior_year_grid["uniform_beta_1_1"]["2035"],
    "hyperion_uniform_p_500_2035": 0.0013,
    "delta_pct": (prior_year_grid["uniform_beta_1_1"]["2035"] - 0.0013) / 0.0013 if 0.0013 != 0 else None,
}

# H1: venture breakeven year ≥ 2055 under uniform; never under others
h1_uniform_breakeven = breakevens["uniform_beta_1_1_rend_hi_venture_breakeven"]
h1_jeffreys_breakeven = breakevens["jeffreys_beta_0p5_0p5_rend_hi_venture_breakeven"]
h1_skeptical_breakeven = breakevens["skeptical_beta_0p5_5_rend_hi_venture_breakeven"]
h1_pred_holds = (
    (h1_uniform_breakeven == "never_in_horizon" or (isinstance(h1_uniform_breakeven, int) and h1_uniform_breakeven >= 2055))
    and h1_jeffreys_breakeven == "never_in_horizon"
    and h1_skeptical_breakeven == "never_in_horizon"
)

# H2: at ever-50yr, max conjunction < 30% (corp-growth) under all priors
ever_row = next(r for r in sensitivity if r["window_year"] == "ever")
h2_max_at_ever = max(
    ever_row["uniform_beta_1_1_rend_hi_max_conjunction"],
    ever_row["jeffreys_beta_0p5_0p5_rend_hi_max_conjunction"],
    ever_row["skeptical_beta_0p5_5_rend_hi_max_conjunction"],
)
h2_holds = h2_max_at_ever < 0.30

# H3: at uniform breakeven, first-delivery year ≥ 2065
h3_first_delivery = first_delivery_at_breakeven.get("uniform_beta_1_1_rend_hi_venture_first_delivery_year")
h3_holds = (isinstance(h3_first_delivery, int) and h3_first_delivery >= 2065) or h3_first_delivery == "ever+14_uncomputable"

# H4: max conjunction at 2045 < 10% under all priors
row_2045 = next(r for r in sensitivity if r["window_year"] == 2045)
h4_max_at_2045 = max(
    row_2045["uniform_beta_1_1_rend_hi_max_conjunction"],
    row_2045["jeffreys_beta_0p5_0p5_rend_hi_max_conjunction"],
    row_2045["skeptical_beta_0p5_5_rend_hi_max_conjunction"],
)
h4_holds = h4_max_at_2045 < 0.10

# H5: uniform lift 2035 → 2045 ≤ 4×
row_2035 = next(r for r in sensitivity if r["window_year"] == 2035)
lift_2035_to_2045_uniform = (
    row_2045["uniform_beta_1_1_rend_hi_max_conjunction"]
    / row_2035["uniform_beta_1_1_rend_hi_max_conjunction"]
    if row_2035["uniform_beta_1_1_rend_hi_max_conjunction"] > 0 else None
)
h5_holds = lift_2035_to_2045_uniform is not None and lift_2035_to_2045_uniform <= 4.0


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

out = {
    "round": "R-demonstrator-window-sensitivity",
    "author": "iapetus",
    "date": "2026-05-15",
    "pre_registration": "SCOPE.md (H1-H5)",
    "anchor_priors_from": "R-reactor-specific-power-program-targets",
    "monte_carlo_n_trajectories": N_TRAJECTORIES,
    "seed": SEED,
    "window_years_swept": [str(y) for y in WINDOW_YEARS],
    "sanity_check_vs_hyperion_2035": sanity_check,
    "p_500kWe_orbit_by_window_and_prior": prior_year_grid,
    "sensitivity_table": sensitivity,
    "breakeven_years": breakevens,
    "first_delivery_year_at_breakeven": first_delivery_at_breakeven,
    "hypotheses": {
        "H1": {
            "hypothesis": "Venture breakeven ≥ 2055 (uniform); never (Jeffreys, skeptical)",
            "uniform_breakeven_year": h1_uniform_breakeven,
            "jeffreys_breakeven_year": h1_jeffreys_breakeven,
            "skeptical_breakeven_year": h1_skeptical_breakeven,
            "verdict": "CONFIRMED" if h1_pred_holds else "FALSIFIED",
        },
        "H2": {
            "hypothesis": "Max conjunction at ever-50yr horizon < 30% (corp-growth) under all priors",
            "max_conjunction_at_ever": h2_max_at_ever,
            "verdict": "CONFIRMED" if h2_holds else "FALSIFIED",
        },
        "H3": {
            "hypothesis": "At uniform breakeven, first-delivery year ≥ 2065",
            "first_delivery_year_at_uniform_breakeven": h3_first_delivery,
            "verdict": "CONFIRMED" if h3_holds else "FALSIFIED",
        },
        "H4": {
            "hypothesis": "Max conjunction at 2045 window < 10% (venture) under all priors — H6 robust to 10-yr extension",
            "max_conjunction_at_2045": h4_max_at_2045,
            "verdict": "CONFIRMED" if h4_holds else "FALSIFIED",
        },
        "H5": {
            "hypothesis": "Uniform lift 2035 → 2045 ≤ 4×",
            "lift_factor": lift_2035_to_2045_uniform,
            "verdict": "CONFIRMED" if h5_holds else "FALSIFIED",
        },
    },
}

out_path = RESULTS_DIR / "demonstrator_window_sensitivity.json"
out_path.write_text(json.dumps(out, indent=2))


# ---------------------------------------------------------------------------
# Console summary
# ---------------------------------------------------------------------------

print(f"Wrote {out_path}")
print()
print("=== Sanity check vs hyperion R-power-bayesian-update at 2035 (uniform) ===")
print(f"  iapetus re-derived = {sanity_check['iapetus_uniform_p_500_2035']:.4%}")
print(f"  hyperion reported  = {sanity_check['hyperion_uniform_p_500_2035']:.4%}")
print(f"  delta = {sanity_check['delta_pct']*100:.1f}% (Monte-Carlo noise)" if sanity_check['delta_pct'] is not None else "  (zero)")
print()
print("=== p_500kWe_orbit by (window, prior) ===")
print(f"  {'window':>8}  {'skeptical':>12}  {'jeffreys':>12}  {'uniform':>12}")
for y in WINDOW_YEARS:
    s = prior_year_grid["skeptical_beta_0p5_5"][str(y)]
    j = prior_year_grid["jeffreys_beta_0p5_0p5"][str(y)]
    u = prior_year_grid["uniform_beta_1_1"][str(y)]
    print(f"  {str(y):>8}  {s:>12.4%}  {j:>12.4%}  {u:>12.4%}")
print()
print("=== Max full-conjunction posterior by (window, prior, rendezvous-hi) ===")
print(f"  {'window':>8}  {'skeptical':>12}  {'jeffreys':>12}  {'uniform':>12}")
for row in sensitivity:
    s = row["skeptical_beta_0p5_5_rend_hi_max_conjunction"]
    j = row["jeffreys_beta_0p5_0p5_rend_hi_max_conjunction"]
    u = row["uniform_beta_1_1_rend_hi_max_conjunction"]
    s_cls = row["skeptical_beta_0p5_5_rend_hi_capital_class"]
    j_cls = row["jeffreys_beta_0p5_0p5_rend_hi_capital_class"]
    u_cls = row["uniform_beta_1_1_rend_hi_capital_class"]
    print(f"  {str(row['window_year']):>8}  {s:>9.4%} {s_cls[:3]}  {j:>9.4%} {j_cls[:3]}  {u:>9.4%} {u_cls[:3]}")
print()
print("=== Breakeven years (rendezvous-hi, the most favourable assumption) ===")
for prior_name in PRIORS:
    venture = breakevens[f"{prior_name}_rend_hi_venture_breakeven"]
    corp = breakevens[f"{prior_name}_rend_hi_corp_growth_breakeven"]
    util = breakevens[f"{prior_name}_rend_hi_regulated_utility_breakeven"]
    print(f"  {prior_name:>28}: venture={venture}, corp-growth={corp}, regulated-utility={util}")
print()
print("=== Hypotheses verdicts ===")
for h, v in out["hypotheses"].items():
    print(f"  {h}: {v['verdict']}")
