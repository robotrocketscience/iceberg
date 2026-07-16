"""
R-global-vs-US-base-rate — does broadening the fission-orbit base rate to a
global set (US + USSR/Russia + China) flip H6 from R-reactor-specific-power-
program-targets?

Re-runs Bayesian Monte Carlo at a global program-level base rate (3 successes
in 11 programs), adjusts the scope conditional downward to account for the
historical reality that all orbited fission reactors have been ≤ 6 kilowatt-
electric, and propagates through the conditional-prior chain.

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

PRIOR_ROUND_TARGETS = json.loads(
    (PROJECT_ROOT / "R_reactor_specific_power_program_targets" / "results" / "reactor_program_targets.json").read_text()
)
PRIOR_ROUND_WINDOW = json.loads(
    (PROJECT_ROOT / "R_demonstrator_window_sensitivity" / "results" / "demonstrator_window_sensitivity.json").read_text()
)


# ---------------------------------------------------------------------------
# Bayesian Monte Carlo with global base rate
# ---------------------------------------------------------------------------

N_TRAJECTORIES = 10_000
SEED = 0
BASE_YEAR = 2026

# US-only base rate (anchored on locked belief 2)
US_ONLY_SUCCESSES = 0   # 0 successful US fission orbits since SNAP-10A (excluding SNAP-10A itself)
US_ONLY_FAILURES = 6    # SP-100, Timberwind, Prometheus, DRACO, Kilopower-flight, FSP-Phase-2-pending

# Global base rate at program-level (this round)
#  US contributions: 0 successes, 6 failures (above)
#  USSR/Russia: BUK (1 success — sustained orbital deployment), TOPAZ (1 success), Zeus (0 successes, 1 failure-still-pending)
#  China: CASC-megawatt (0 successes, 1 failure-still-pending)
GLOBAL_SUCCESSES = 2    # BUK + TOPAZ
GLOBAL_FAILURES = 8     # 6 US + Zeus + China-megawatt
# (SNAP-10A itself counted as "1 historical success" but we exclude it from both base rates because the prior anchor
#  in the R-power-bayesian-update is "since SNAP-10A".)

PRIORS = {
    "uniform_beta_1_1":      (1.0, 1.0),
    "jeffreys_beta_0p5_0p5": (0.5, 0.5),
    "skeptical_beta_0p5_5":  (0.5, 5.0),
}

# Likelihood multipliers — for the global model these no longer all apply
# (FSP-specific factors are US-specific). For global, we apply only the
# scope-and-funding factor reflecting that programs that have made the most
# progress recently (FSP Phase 1, China megawatt roadmap) are not on a
# guaranteed-orbit trajectory.
# Conservative: apply a NET likelihood factor of 0.9 (slightly negative from
# the FY26-budget-zero-for-NEP/NTP and absence of any orbital-flight contract).
GLOBAL_LIKELIHOOD_NET = 0.9

# US-only likelihood (from hyperion)
US_LIKELIHOOD_FACTORS = [
    ("phase1_awarded_2022",             1.40, 0.10),
    ("phase1_extended_2024",            0.85, 0.10),
    ("duffy_directive_2025_scope_grew", 0.90, 0.15),
    ("draft_afpp_aug_2025",             1.25, 0.10),
    ("no_phase2_contract_may_2026",     0.80, 0.10),
    ("fy26_budget_zeroed_nep_ntp",      0.70, 0.15),
]

# Scope conditional: probability that an orbited reactor in the demonstrator window
# is ≥ 500 kilowatt-electric, given orbit-by-window.
# US-only (hyperion's anchor): 0.6 — assumes Fission-Surface-Power Phase-2 derivative scope-grew.
# But Aug 2025 Duffy directive set Phase-2 scope at 100 kilowatt-electric, NOT 500+.
# Honest scope conditional for prospective US programs: 100/(100+anything-else) ≈ low.
# Adjusted prospective scope conditional given currently-pending programs:
#   - FSP Phase-2 derivative: 100 kilowatt-electric scope (below 500)
#   - Zeus (Russia): 500-1000 kilowatt-electric (at/above threshold)
#   - China-megawatt: ≥ 1000 kilowatt-electric (above threshold)
#   - BUK/TOPAZ retro-counterfactual: 3-6 kilowatt-electric (below threshold)
P_500_FUNDED_GIVEN_ORBIT_GLOBAL = 0.40   # primary anchor for global
P_500_FUNDED_GIVEN_ORBIT_GLOBAL_LOW = 0.30  # sensitivity-low
P_500_FUNDED_GIVEN_ORBIT_GLOBAL_HIGH = 0.50 # sensitivity-high

# US-only scope conditional (hyperion): 0.6
P_500_FUNDED_GIVEN_ORBIT_US = 0.6

FSP_TO_500_GAP_MEAN = 4.0
FSP_TO_500_GAP_STDEV = 2.0


def sample_orbit_500_year_offsets(
    alpha_prior: float,
    beta_prior: float,
    n_successes_observed: int,
    n_failures_observed: int,
    p_500_given_orbit: float,
    likelihood_factors: list | float,
    rng: np.random.Generator,
) -> dict:
    """
    Returns the year-offset distribution for (orbit ≥ 500 kilowatt-electric)
    under the specified base-rate model.
    """
    alpha_post = alpha_prior + n_successes_observed
    beta_post = beta_prior + n_failures_observed

    lam_decade = rng.beta(alpha_post, beta_post, size=N_TRAJECTORIES)
    lam_decade_clipped = np.clip(lam_decade, 1e-6, 0.999)
    lam_annual = -np.log(1.0 - lam_decade_clipped) / 10.0

    # Apply likelihood multipliers
    if isinstance(likelihood_factors, float):
        adj_lam = lam_annual * likelihood_factors
    else:
        product = np.ones(N_TRAJECTORIES)
        for _name, factor, stdev in likelihood_factors:
            sampled = rng.normal(loc=factor, scale=stdev, size=N_TRAJECTORIES)
            sampled = np.clip(sampled, 0.05, 5.0)
            product *= sampled
        adj_lam = lam_annual * product

    # Any-orbit year-offset
    orbit_year_offset = rng.exponential(scale=1.0 / np.maximum(adj_lam, 1e-6), size=N_TRAJECTORIES)
    orbit_year_offset = np.minimum(orbit_year_offset, 50.0)
    orbit_succeeded = orbit_year_offset < 50.0

    # Scope conditional gate
    scope_funded = rng.uniform(size=N_TRAJECTORIES) < p_500_given_orbit
    scope_attempt_starts = orbit_year_offset + np.maximum(
        rng.normal(loc=FSP_TO_500_GAP_MEAN, scale=FSP_TO_500_GAP_STDEV, size=N_TRAJECTORIES),
        1.0,
    )
    scope_lam_decade = rng.beta(alpha_post, beta_post, size=N_TRAJECTORIES)
    scope_lam_decade_clipped = np.clip(scope_lam_decade, 1e-6, 0.999)
    scope_lam_annual = -np.log(1.0 - scope_lam_decade_clipped) / 10.0
    scope_orbit_after_start = rng.exponential(
        scale=1.0 / np.maximum(scope_lam_annual, 1e-6), size=N_TRAJECTORIES
    )
    scope_orbit_after_start = np.minimum(scope_orbit_after_start, 30.0)
    scope_year_offset = scope_attempt_starts + scope_orbit_after_start
    scope_arrives = orbit_succeeded & scope_funded & (scope_orbit_after_start < 30.0)
    scope_year_offset = np.where(scope_arrives, scope_year_offset, np.inf)

    return {
        "orbit_year_offset": orbit_year_offset,
        "orbit_succeeded": orbit_succeeded,
        "scope_year_offset": scope_year_offset,
    }


def p_by_year(scope_year_offset: np.ndarray, year_or_ever) -> float:
    if year_or_ever == "ever":
        return float(np.mean(np.isfinite(scope_year_offset)))
    offset = year_or_ever - BASE_YEAR
    return float(np.mean(scope_year_offset <= offset))


WINDOW_YEARS = [2032, 2035, 2040, 2045, 2050, 2055, 2060, "ever"]


# Run US-only (sanity check vs hyperion)
us_only_results: dict[str, dict] = {}
for prior_name, (a, b) in PRIORS.items():
    sub_rng = np.random.default_rng(SEED + hash("us_" + prior_name) % 1000)
    r = sample_orbit_500_year_offsets(
        a, b, US_ONLY_SUCCESSES, US_ONLY_FAILURES, P_500_FUNDED_GIVEN_ORBIT_US,
        US_LIKELIHOOD_FACTORS, sub_rng,
    )
    us_only_results[prior_name] = {
        "p_orbit_by_year": {str(y): p_by_year(r["orbit_year_offset"], y) for y in WINDOW_YEARS},
        "p_500_by_year": {str(y): p_by_year(r["scope_year_offset"], y) for y in WINDOW_YEARS},
    }

# Run global
global_results: dict[str, dict] = {}
for prior_name, (a, b) in PRIORS.items():
    sub_rng = np.random.default_rng(SEED + hash("global_" + prior_name) % 1000)
    r = sample_orbit_500_year_offsets(
        a, b, GLOBAL_SUCCESSES, GLOBAL_FAILURES, P_500_FUNDED_GIVEN_ORBIT_GLOBAL,
        GLOBAL_LIKELIHOOD_NET, sub_rng,
    )
    global_results[prior_name] = {
        "p_orbit_by_year": {str(y): p_by_year(r["orbit_year_offset"], y) for y in WINDOW_YEARS},
        "p_500_by_year": {str(y): p_by_year(r["scope_year_offset"], y) for y in WINDOW_YEARS},
    }

# Sensitivity: global with scope conditional 0.30 (low) and 0.50 (high)
global_low_results: dict[str, dict] = {}
global_high_results: dict[str, dict] = {}
for prior_name, (a, b) in PRIORS.items():
    sub_rng = np.random.default_rng(SEED + hash("global_low_" + prior_name) % 1000)
    r = sample_orbit_500_year_offsets(
        a, b, GLOBAL_SUCCESSES, GLOBAL_FAILURES, P_500_FUNDED_GIVEN_ORBIT_GLOBAL_LOW,
        GLOBAL_LIKELIHOOD_NET, sub_rng,
    )
    global_low_results[prior_name] = {
        "p_500_by_year": {str(y): p_by_year(r["scope_year_offset"], y) for y in WINDOW_YEARS},
    }
    sub_rng2 = np.random.default_rng(SEED + hash("global_high_" + prior_name) % 1000)
    r2 = sample_orbit_500_year_offsets(
        a, b, GLOBAL_SUCCESSES, GLOBAL_FAILURES, P_500_FUNDED_GIVEN_ORBIT_GLOBAL_HIGH,
        GLOBAL_LIKELIHOOD_NET, sub_rng2,
    )
    global_high_results[prior_name] = {
        "p_500_by_year": {str(y): p_by_year(r2["scope_year_offset"], y) for y in WINDOW_YEARS},
    }


# ---------------------------------------------------------------------------
# Apply R-reactor-specific-power-program-targets conditional-prior chain
# ---------------------------------------------------------------------------

SP_PRIOR = {float(k): v for k, v in PRIOR_ROUND_TARGETS["subjective_priors"]["p_sp_geq_given_orbit_500kWe"].items()}
L_PRIOR_RAW = PRIOR_ROUND_TARGETS["subjective_priors"]["p_L_geq_given_orbit_500kWe"]
L_PRIOR = {float("inf") if k == "inf" else float(k): v for k, v in L_PRIOR_RAW.items()}
X_PRIOR = {float(k): v for k, v in PRIOR_ROUND_TARGETS["subjective_priors"]["p_X_geq_given_hybrid_closes"].items()}
P_HYBRID_AEROCAP = PRIOR_ROUND_TARGETS["subjective_priors"]["P_HYBRID_AEROCAP"]
P_RENDEZVOUS_LOW = PRIOR_ROUND_TARGETS["subjective_priors"]["P_RENDEZVOUS_LOW"]
P_RENDEZVOUS_HI  = PRIOR_ROUND_TARGETS["subjective_priors"]["P_RENDEZVOUS_HI"]
MIN_CORNERS = PRIOR_ROUND_TARGETS["min_corner_table"]

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


def conjunction_at_corner(corner: dict, p_500_orbit: float, rend_prior: float) -> float:
    sp = corner["min_sp_w_per_kg"]
    X = corner["X_km_s"]
    L_yr = corner["L_yr"]
    L_key = float("inf") if L_yr == "inf" else float(L_yr)
    p_sp = SP_PRIOR[sp]
    p_L = L_PRIOR[L_key]
    p_aero = (P_HYBRID_AEROCAP * X_PRIOR[X]) if X > 0 else 1.0
    return p_500_orbit * p_sp * p_L * p_aero * rend_prior


def max_conjunction(p_500_orbit: float, rend_prior: float) -> tuple[float, dict | None]:
    best_p, best_c = 0.0, None
    for c in MIN_CORNERS:
        p = conjunction_at_corner(c, p_500_orbit, rend_prior)
        if p > best_p:
            best_p = p
            best_c = c
    return best_p, best_c


def build_table(base_results: dict[str, dict]) -> list[dict]:
    table = []
    for y in WINDOW_YEARS:
        row: dict = {"window_year": y}
        for prior_name in PRIORS:
            p_500 = base_results[prior_name]["p_500_by_year"][str(y)]
            row[f"{prior_name}_p_500"] = p_500
            for rend_label, rend in (("rend_low", P_RENDEZVOUS_LOW), ("rend_hi", P_RENDEZVOUS_HI)):
                mp, _ = max_conjunction(p_500, rend)
                row[f"{prior_name}_{rend_label}_max_conjunction"] = mp
                row[f"{prior_name}_{rend_label}_capital_class"] = capital_class(mp)
        table.append(row)
    return table


us_table = build_table(us_only_results)
global_table = build_table(global_results)
global_low_table = build_table({k: {"p_500_by_year": v["p_500_by_year"]} for k, v in global_low_results.items()})
global_high_table = build_table({k: {"p_500_by_year": v["p_500_by_year"]} for k, v in global_high_results.items()})


# ---------------------------------------------------------------------------
# Breakeven and comparison
# ---------------------------------------------------------------------------

def first_year_above(table: list[dict], threshold: float, prior_name: str, rend_label: str):
    for row in table:
        if row[f"{prior_name}_{rend_label}_max_conjunction"] >= threshold:
            return row["window_year"]
    return "never_in_horizon"


VENTURE_T = 0.10
CORP_GROWTH_T = 0.30

global_breakevens = {}
for prior_name in PRIORS:
    for rend_label in ("rend_low", "rend_hi"):
        global_breakevens[f"{prior_name}_{rend_label}_venture_breakeven"] = first_year_above(global_table, VENTURE_T, prior_name, rend_label)
        global_breakevens[f"{prior_name}_{rend_label}_corp_growth_breakeven"] = first_year_above(global_table, CORP_GROWTH_T, prior_name, rend_label)


# ---------------------------------------------------------------------------
# Hypotheses
# ---------------------------------------------------------------------------

# H1: global per-decade rate / US rate ≥ 3× at uniform prior
us_uniform_orbit_2035 = us_only_results["uniform_beta_1_1"]["p_orbit_by_year"]["2035"]
global_uniform_orbit_2035 = global_results["uniform_beta_1_1"]["p_orbit_by_year"]["2035"]
h1_ratio = global_uniform_orbit_2035 / us_uniform_orbit_2035 if us_uniform_orbit_2035 > 0 else None
h1_verdict = "CONFIRMED" if (h1_ratio is not None and h1_ratio >= 3.0) else "FALSIFIED"

# H2: global scope conditional / US-only scope conditional ≤ 0.33
h2_ratio = P_500_FUNDED_GIVEN_ORBIT_GLOBAL / P_500_FUNDED_GIVEN_ORBIT_US
h2_verdict = "CONFIRMED" if h2_ratio <= 0.33 else "FALSIFIED"

# H3: net conjunction at 2032-2035 in [0.0028%, 0.011%] under global
row_2035_global = next(r for r in global_table if r["window_year"] == 2035)
h3_uniform_rend_hi = row_2035_global["uniform_beta_1_1_rend_hi_max_conjunction"]
h3_verdict = "CONFIRMED" if 0.000028 <= h3_uniform_rend_hi <= 0.00011 else "FALSIFIED"

# H4: H6 holds — venture never crossed in horizon under global base rate
h4_uniform_breakeven = global_breakevens["uniform_beta_1_1_rend_hi_venture_breakeven"]
h4_jeffreys_breakeven = global_breakevens["jeffreys_beta_0p5_0p5_rend_hi_venture_breakeven"]
h4_skeptical_breakeven = global_breakevens["skeptical_beta_0p5_5_rend_hi_venture_breakeven"]
h4_verdict = "CONFIRMED" if all(b == "never_in_horizon" for b in [h4_uniform_breakeven, h4_jeffreys_breakeven, h4_skeptical_breakeven]) else "FALSIFIED"

# H5: conjunction shift |global - US| / US within ±50% at 2032-2035 window
row_2035_us = next(r for r in us_table if r["window_year"] == 2035)
us_2035 = row_2035_us["uniform_beta_1_1_rend_hi_max_conjunction"]
global_2035 = row_2035_global["uniform_beta_1_1_rend_hi_max_conjunction"]
h5_ratio = abs(global_2035 - us_2035) / us_2035 if us_2035 > 0 else None
h5_verdict = "CONFIRMED" if (h5_ratio is not None and h5_ratio <= 0.50) else "FALSIFIED"


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

out = {
    "round": "R-global-vs-US-base-rate",
    "author": "iapetus",
    "date": "2026-05-15",
    "pre_registration": "SCOPE.md (H1-H5)",
    "base_rate_models": {
        "us_only": {
            "successes": US_ONLY_SUCCESSES,
            "failures": US_ONLY_FAILURES,
            "likelihood_factors": "FSP-specific six-factor product (hyperion)",
            "p_500_funded_given_orbit": P_500_FUNDED_GIVEN_ORBIT_US,
        },
        "global": {
            "successes": GLOBAL_SUCCESSES,
            "failures": GLOBAL_FAILURES,
            "likelihood_net": GLOBAL_LIKELIHOOD_NET,
            "p_500_funded_given_orbit": P_500_FUNDED_GIVEN_ORBIT_GLOBAL,
            "p_500_funded_given_orbit_low": P_500_FUNDED_GIVEN_ORBIT_GLOBAL_LOW,
            "p_500_funded_given_orbit_high": P_500_FUNDED_GIVEN_ORBIT_GLOBAL_HIGH,
            "rationale_for_count": "US 0/6 + USSR BUK 1 success + USSR TOPAZ 1 success + Russia Zeus 0/1 + China megawatt 0/1 = 2 of 10",
        },
    },
    "us_only_table": us_table,
    "global_table": global_table,
    "global_scope_low_table": global_low_table,
    "global_scope_high_table": global_high_table,
    "us_only_orbit_posterior_2035": us_uniform_orbit_2035,
    "global_orbit_posterior_2035": global_uniform_orbit_2035,
    "h1_ratio_orbit_global_over_us_2035": h1_ratio,
    "h2_ratio_scope_global_over_us": h2_ratio,
    "global_breakevens": global_breakevens,
    "hypotheses": {
        "H1": {
            "hypothesis": "global / US orbit rate ratio ≥ 3× under uniform prior at 2035",
            "ratio": h1_ratio,
            "verdict": h1_verdict,
        },
        "H2": {
            "hypothesis": "global / US scope conditional ratio ≤ 0.33",
            "ratio": h2_ratio,
            "verdict": h2_verdict,
        },
        "H3": {
            "hypothesis": "global net conjunction at 2032-2035 in [0.0028%, 0.011%]",
            "actual": h3_uniform_rend_hi,
            "verdict": h3_verdict,
        },
        "H4": {
            "hypothesis": "venture never crossed in horizon under global base rate",
            "uniform_breakeven": h4_uniform_breakeven,
            "jeffreys_breakeven": h4_jeffreys_breakeven,
            "skeptical_breakeven": h4_skeptical_breakeven,
            "verdict": h4_verdict,
        },
        "H5": {
            "hypothesis": "conjunction shift |global - US| / US ≤ 50% at 2035 under uniform",
            "ratio": h5_ratio,
            "verdict": h5_verdict,
        },
    },
}

(RESULTS_DIR / "global_vs_us_base_rate.json").write_text(json.dumps(out, indent=2))
print(f"Wrote {RESULTS_DIR / 'global_vs_us_base_rate.json'}")
print()
print("=== Orbit posteriors at 2035 (uniform prior) ===")
print(f"  US-only orbit: {us_uniform_orbit_2035:.4%}")
print(f"  Global orbit:  {global_uniform_orbit_2035:.4%}")
print(f"  Ratio: {h1_ratio:.2f}×" if h1_ratio else "  Ratio: undef")
print()
print("=== Scope conditional (p_500_funded_given_orbit) ===")
print(f"  US-only: {P_500_FUNDED_GIVEN_ORBIT_US:.2f}")
print(f"  Global:  {P_500_FUNDED_GIVEN_ORBIT_GLOBAL:.2f}")
print(f"  Ratio: {h2_ratio:.2f}")
print()
print("=== p_500 by (window, prior, model) — uniform Beta(1,1) ===")
print(f"  {'window':>8}  {'US-only':>10}  {'global':>10}  {'glob-low':>10}  {'glob-high':>10}")
for y in WINDOW_YEARS:
    us_p = us_only_results["uniform_beta_1_1"]["p_500_by_year"][str(y)]
    gl_p = global_results["uniform_beta_1_1"]["p_500_by_year"][str(y)]
    gl_lo = global_low_results["uniform_beta_1_1"]["p_500_by_year"][str(y)]
    gl_hi = global_high_results["uniform_beta_1_1"]["p_500_by_year"][str(y)]
    print(f"  {str(y):>8}  {us_p:>10.4%}  {gl_p:>10.4%}  {gl_lo:>10.4%}  {gl_hi:>10.4%}")
print()
print("=== Max full-conjunction posterior (rendezvous-hi, uniform prior) ===")
print(f"  {'window':>8}  {'US-only':>12}  {'global':>12}  {'glob-low':>12}  {'glob-high':>12}")
for i, y in enumerate(WINDOW_YEARS):
    us_v = us_table[i]["uniform_beta_1_1_rend_hi_max_conjunction"]
    gl_v = global_table[i]["uniform_beta_1_1_rend_hi_max_conjunction"]
    gl_lo_v = global_low_table[i]["uniform_beta_1_1_rend_hi_max_conjunction"]
    gl_hi_v = global_high_table[i]["uniform_beta_1_1_rend_hi_max_conjunction"]
    print(f"  {str(y):>8}  {us_v:>12.4%}  {gl_v:>12.4%}  {gl_lo_v:>12.4%}  {gl_hi_v:>12.4%}")
print()
print("=== Global breakevens (rendezvous-hi) ===")
for prior_name in PRIORS:
    v = global_breakevens[f"{prior_name}_rend_hi_venture_breakeven"]
    cg = global_breakevens[f"{prior_name}_rend_hi_corp_growth_breakeven"]
    print(f"  {prior_name:>28}: venture={v}, corp-growth={cg}")
print()
print("=== Hypotheses verdicts ===")
for h, v in out["hypotheses"].items():
    print(f"  {h}: {v['verdict']}")
