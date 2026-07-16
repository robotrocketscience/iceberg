"""R-power-base-rate — Bayesian prior on space-fission reactor arrival year.

Pre-registered hypotheses in water-prop/HYPOTHESES.md and STUDY.md alongside.

Deterministic Monte Carlo with seed=0. Outputs cumulative-distribution-function
tables to results/ and a JSON summary keyed for the Revisit clause.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

RESULTS_DIR = Path(__file__).parent / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# Pre-registered prior parameters and FSP-specific likelihood multipliers.
# All numbers are documented in STUDY.md; changing them changes the
# pre-registration and must be flagged in the Revisit clause.

N_TRAJECTORIES = 10_000
SEED = 0
BASE_YEAR = 2026  # all forward-time outputs measured from here

# Beta(alpha, beta) prior on per-decade success rate.
# Six observations of program failure (SP-100, Timberwind, Prometheus,
# Kilopower-flight, DRACO, FSP-as-of-2026), one pseudo-count of success.
PRIOR_ALPHA = 1.0
PRIOR_BETA = 7.0

# FSP-specific likelihood multipliers on prior probability of FSP-class orbit by year Y.
# Each entry is (description, multiplicative factor on prior, factor uncertainty stdev for MC).
FSP_LIKELIHOOD_FACTORS = [
    ("phase1_awarded_2022", 1.40, 0.10),
    ("phase1_extended_2024", 0.85, 0.10),
    ("duffy_directive_2025_scope_grew", 0.90, 0.15),
    ("draft_afpp_aug_2025", 1.25, 0.10),
    ("no_phase2_contract_may_2026", 0.80, 0.10),
    ("fy26_budget_zeroed_nep_ntp", 0.70, 0.15),
]

# Gap (years) between FSP-class flight and megawatt-class flight, given FSP succeeds.
# Historical median between SNAP-class ground demo and follow-on flight program.
FSP_TO_MW_GAP_MEAN = 7.0
FSP_TO_MW_GAP_STDEV = 3.0

# Probability that a megawatt program is funded after FSP succeeds. Includes
# political-budget risk; FY26 NEP zero-out is the dominant signal here.
P_MW_FUNDED_GIVEN_FSP = 0.45

# Probability that a funded megawatt program reaches orbit within its decade
# of attempt, given it is funded (independent draw from the base-rate prior).
# Computed during MC from each trajectory's sampled lambda.


def main() -> None:
    rng = np.random.default_rng(SEED)

    # 1) Sample per-decade success rate from the Beta(alpha, beta) prior.
    lam_decade = rng.beta(PRIOR_ALPHA, PRIOR_BETA, size=N_TRAJECTORIES)
    # Convert to annual hazard rate via 1 - exp(-10*lam_annual) = lam_decade.
    lam_annual = -np.log(1.0 - lam_decade) / 10.0

    # 2) Sample FSP-specific likelihood multipliers and combine.
    fsp_product = np.ones(N_TRAJECTORIES)
    for _name, factor, stdev in FSP_LIKELIHOOD_FACTORS:
        sampled = rng.normal(loc=factor, scale=stdev, size=N_TRAJECTORIES)
        sampled = np.clip(sampled, 0.05, 5.0)  # avoid degenerate values
        fsp_product *= sampled
    fsp_adjusted_lam = lam_annual * fsp_product

    # 3) Sample FSP-class orbit year via exponential waiting time.
    # P(no orbit by year y) = exp(-lambda * y); orbit-year ~ Exp(lambda).
    fsp_year_offset = rng.exponential(scale=1.0 / fsp_adjusted_lam, size=N_TRAJECTORIES)
    # Censor at 50 years for tractability — outside that horizon the program is dead.
    fsp_year_offset = np.minimum(fsp_year_offset, 50.0)
    fsp_succeeded = fsp_year_offset < 50.0

    # 4) Megawatt-class arrival, conditional on FSP success and MW-program funding.
    mw_funded = rng.uniform(size=N_TRAJECTORIES) < P_MW_FUNDED_GIVEN_FSP
    mw_attempt_starts = fsp_year_offset + np.maximum(
        rng.normal(loc=FSP_TO_MW_GAP_MEAN, scale=FSP_TO_MW_GAP_STDEV, size=N_TRAJECTORIES),
        2.0,
    )
    # Given MW program funded, probability of orbit within decade follows lam_decade
    # sampled from same prior (independent draw).
    mw_lam_decade = rng.beta(PRIOR_ALPHA, PRIOR_BETA, size=N_TRAJECTORIES)
    mw_lam_annual = -np.log(1.0 - mw_lam_decade) / 10.0
    mw_orbit_after_start = rng.exponential(scale=1.0 / mw_lam_annual, size=N_TRAJECTORIES)
    mw_orbit_after_start = np.minimum(mw_orbit_after_start, 30.0)
    mw_year_offset = mw_attempt_starts + mw_orbit_after_start
    # MW arrives only if FSP succeeded, MW funded, and orbit within 30 years of attempt.
    mw_arrives = fsp_succeeded & mw_funded & (mw_orbit_after_start < 30.0)
    mw_year_offset = np.where(mw_arrives, mw_year_offset, np.inf)

    # 5) Compute CDF probabilities for the pre-registered hypotheses.
    def p_by_offset(arr: np.ndarray, offset: float) -> float:
        return float(np.mean(arr <= offset))

    h_pbr_a = p_by_offset(fsp_year_offset, 2032 - BASE_YEAR)
    h_pbr_b = p_by_offset(fsp_year_offset, 2035 - BASE_YEAR)
    h_pbr_c = h_pbr_b  # FSP class IS the 40+ kWe class in this model
    h_pbr_d = p_by_offset(mw_year_offset, 2040 - BASE_YEAR)
    h_pbr_e = p_by_offset(mw_year_offset, 2045 - BASE_YEAR)

    # Median MW-arrival-year measured from base year.
    finite_mw = mw_year_offset[np.isfinite(mw_year_offset)]
    h_pbr_f = float(np.median(finite_mw)) if finite_mw.size > 0 else float("inf")

    h_pbr_g = p_by_offset(mw_year_offset, 20.0)  # R15-rerun baseline year

    p_mw_ever = float(np.mean(np.isfinite(mw_year_offset)))

    # 6) Build full CDF tables for arrival-year sweep.
    year_grid = np.arange(0, 51, 1)
    fsp_cdf = [p_by_offset(fsp_year_offset, y) for y in year_grid]
    mw_cdf = [p_by_offset(mw_year_offset, y) for y in year_grid]

    summary = {
        "seed": SEED,
        "n_trajectories": N_TRAJECTORIES,
        "base_year": BASE_YEAR,
        "prior": {"alpha": PRIOR_ALPHA, "beta": PRIOR_BETA},
        "fsp_likelihood_factors": FSP_LIKELIHOOD_FACTORS,
        "fsp_to_mw_gap_mean": FSP_TO_MW_GAP_MEAN,
        "p_mw_funded_given_fsp": P_MW_FUNDED_GIVEN_FSP,
        "hypotheses": {
            "H-pbr-a_P_fission_by_2032": h_pbr_a,
            "H-pbr-b_P_fission_by_2035": h_pbr_b,
            "H-pbr-c_P_40kWe_by_2035": h_pbr_c,
            "H-pbr-d_P_MW_by_2040": h_pbr_d,
            "H-pbr-e_P_MW_by_2045": h_pbr_e,
            "H-pbr-f_median_MW_year_offset": h_pbr_f,
            "H-pbr-g_P_MW_by_year_20": h_pbr_g,
        },
        "p_megawatt_ever_in_50yr_horizon": p_mw_ever,
        "fsp_cdf_by_year_offset": dict(zip([int(y) for y in year_grid], fsp_cdf)),
        "mw_cdf_by_year_offset": dict(zip([int(y) for y in year_grid], mw_cdf)),
    }

    out_path = RESULTS_DIR / "R_power_base_rate_summary.json"
    out_path.write_text(json.dumps(summary, indent=2))
    print(f"wrote {out_path}")

    # Print pre-registration grading.
    pre_reg = {
        "H-pbr-a": (h_pbr_a, 0.05, 0.20),
        "H-pbr-b": (h_pbr_b, 0.15, 0.40),
        "H-pbr-c": (h_pbr_c, 0.05, 0.25),
        "H-pbr-d": (h_pbr_d, 0.02, 0.10),
        "H-pbr-e": (h_pbr_e, 0.05, 0.20),
        "H-pbr-f": (h_pbr_f, 22.0, 35.0),
        "H-pbr-g": (h_pbr_g, 0.01, 0.08),
    }
    print("\nPre-registration grading:")
    print(f"{'claim':<10} {'measured':>10} {'lo':>8} {'hi':>8} {'held?':>8}")
    for name, (meas, lo, hi) in pre_reg.items():
        held = lo <= meas <= hi
        marker = "HELD" if held else "FALSIFIED"
        print(f"{name:<10} {meas:>10.4g} {lo:>8.3g} {hi:>8.3g} {marker:>8}")


if __name__ == "__main__":
    main()
