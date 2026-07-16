"""R-power-bayesian-update — three-prior sensitivity bracket on the
Fission-Surface-Power-Phase-2-to-flight posterior, plus matrix programmatic-risk
overlay.

Reuses the upstream R-power-base-rate Monte Carlo machinery verbatim, but
sweeps three priors (uniform, Jeffreys, skeptical) and produces a
matrix-overlay JSON the orchestrator can drop into the architecture-decision
matrix.

See STUDY.md for the pre-registered hypothesis block and method.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

RESULTS_DIR = Path(__file__).parent / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

N_TRAJECTORIES = 10_000
SEED = 0
BASE_YEAR = 2026

# Three priors, all evaluated against the same 0-of-6 likelihood. The posterior
# in each case is Beta(alpha + 0, beta + 6) — no observed successes since SNAP-10A.
PRIORS = {
    "uniform_beta_1_1": (1.0, 1.0),
    "jeffreys_beta_0p5_0p5": (0.5, 0.5),
    "skeptical_beta_0p5_5": (0.5, 5.0),
}

# Fission-Surface-Power-specific likelihood multipliers (copied from R_power_base_rate).
FSP_LIKELIHOOD_FACTORS = [
    ("phase1_awarded_2022", 1.40, 0.10),
    ("phase1_extended_2024", 0.85, 0.10),
    ("duffy_directive_2025_scope_grew", 0.90, 0.15),
    ("draft_afpp_aug_2025", 1.25, 0.10),
    ("no_phase2_contract_may_2026", 0.80, 0.10),
    ("fy26_budget_zeroed_nep_ntp", 0.70, 0.15),
]

# Megawatt-program waiting-time parameters (copied from R_power_base_rate).
FSP_TO_MW_GAP_MEAN = 7.0
FSP_TO_MW_GAP_STDEV = 3.0
P_MW_FUNDED_GIVEN_FSP = 0.45

# 500-kilowatt-electric scale-up (Variant B's reactor floor) is treated as
# materially less ambitious than megawatt-class. Pre-registered:
P_500_FUNDED_GIVEN_FSP = 0.6  # 5x scope grow vs 25x for megawatt
FSP_TO_500_GAP_MEAN = 4.0  # shorter gap; less of a clean-sheet redesign
FSP_TO_500_GAP_STDEV = 2.0

# Matrix-cell delivered-mass figures, conditional on reactor available.
# Sources:
#   - 90 t Variant B 500-kilowatt-electric: rhea R_megawatt_marvl_radiator
#     surviving cell (chemical-kick + electric-inbound at 500 kilowatt-electric)
#   - 0 t megawatt all-electric: falsified by rhea
#   - 0 t year-twenty-plus megawatt end-to-end: falsified by rhea + locked findings
MATRIX_CELLS_CONDITIONAL = {
    "variant_B_500kWe_chemical_kick_plus_electric_inbound": {
        "delivered_mass_t_per_mission": 90.0,
        "reactor_class": "fsp_derivative_500kWe",
    },
    "all_electric_megawatt": {
        "delivered_mass_t_per_mission": 0.0,
        "reactor_class": "megawatt",
    },
    "year_20plus_megawatt_end_to_end": {
        "delivered_mass_t_per_mission": 0.0,
        "reactor_class": "megawatt",
    },
}

DEMONSTRATOR_WINDOW_YEAR = 2035 - BASE_YEAR  # 9-year horizon


def run_one_prior(alpha_prior: float, beta_prior: float, rng: np.random.Generator) -> dict:
    """Run the upstream Monte Carlo with one prior and return CDF + headline numbers."""
    alpha_post = alpha_prior + 0.0  # 0 successes
    beta_post = beta_prior + 6.0  # 6 failures

    # Sample per-decade fission-program success rate from posterior.
    lam_decade = rng.beta(alpha_post, beta_post, size=N_TRAJECTORIES)
    # Convert to annual hazard via 1 - exp(-10 * lam_annual) = lam_decade.
    # Clip to avoid log(0).
    lam_decade_clipped = np.clip(lam_decade, 1e-6, 0.999)
    lam_annual = -np.log(1.0 - lam_decade_clipped) / 10.0

    # Fission-Surface-Power multiplier product.
    fsp_product = np.ones(N_TRAJECTORIES)
    for _name, factor, stdev in FSP_LIKELIHOOD_FACTORS:
        sampled = rng.normal(loc=factor, scale=stdev, size=N_TRAJECTORIES)
        sampled = np.clip(sampled, 0.05, 5.0)
        fsp_product *= sampled
    fsp_adjusted_lam = lam_annual * fsp_product

    # Fission-Surface-Power-class orbit year via exponential waiting time.
    fsp_year_offset = rng.exponential(
        scale=1.0 / np.maximum(fsp_adjusted_lam, 1e-6), size=N_TRAJECTORIES
    )
    fsp_year_offset = np.minimum(fsp_year_offset, 50.0)
    fsp_succeeded = fsp_year_offset < 50.0

    # Megawatt-class arrival, conditional on Fission-Surface-Power success and program funding.
    mw_funded = rng.uniform(size=N_TRAJECTORIES) < P_MW_FUNDED_GIVEN_FSP
    mw_attempt_starts = fsp_year_offset + np.maximum(
        rng.normal(loc=FSP_TO_MW_GAP_MEAN, scale=FSP_TO_MW_GAP_STDEV, size=N_TRAJECTORIES),
        2.0,
    )
    mw_lam_decade = rng.beta(alpha_post, beta_post, size=N_TRAJECTORIES)
    mw_lam_decade_clipped = np.clip(mw_lam_decade, 1e-6, 0.999)
    mw_lam_annual = -np.log(1.0 - mw_lam_decade_clipped) / 10.0
    mw_orbit_after_start = rng.exponential(
        scale=1.0 / np.maximum(mw_lam_annual, 1e-6), size=N_TRAJECTORIES
    )
    mw_orbit_after_start = np.minimum(mw_orbit_after_start, 30.0)
    mw_year_offset = mw_attempt_starts + mw_orbit_after_start
    mw_arrives = fsp_succeeded & mw_funded & (mw_orbit_after_start < 30.0)
    mw_year_offset = np.where(mw_arrives, mw_year_offset, np.inf)

    # 500-kilowatt-electric class arrival, conditional on Fission-Surface-Power success
    # and 500-kilowatt-electric scale-up program funding (less penalized than megawatt).
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

    def p_by_offset(arr: np.ndarray, offset: float) -> float:
        return float(np.mean(arr <= offset))

    p_fsp_by_2032 = p_by_offset(fsp_year_offset, 2032 - BASE_YEAR)
    p_fsp_by_2035 = p_by_offset(fsp_year_offset, 2035 - BASE_YEAR)
    p_fsp_by_2040 = p_by_offset(fsp_year_offset, 2040 - BASE_YEAR)
    p_500_by_2035 = p_by_offset(fsp500_year_offset, 2035 - BASE_YEAR)
    p_500_by_2040 = p_by_offset(fsp500_year_offset, 2040 - BASE_YEAR)
    p_mw_by_2040 = p_by_offset(mw_year_offset, 2040 - BASE_YEAR)
    p_mw_by_2045 = p_by_offset(mw_year_offset, 2045 - BASE_YEAR)
    p_mw_ever = float(np.mean(np.isfinite(mw_year_offset)))

    finite_mw = mw_year_offset[np.isfinite(mw_year_offset)]
    median_mw_year_offset = float(np.median(finite_mw)) if finite_mw.size > 0 else float("inf")
    finite_fsp = fsp_year_offset[fsp_succeeded]
    median_fsp_year_offset = float(np.median(finite_fsp)) if finite_fsp.size > 0 else float("inf")

    return {
        "alpha_prior": alpha_prior,
        "beta_prior": beta_prior,
        "alpha_posterior": alpha_post,
        "beta_posterior": beta_post,
        "posterior_mean_per_decade_rate": alpha_post / (alpha_post + beta_post),
        "p_fsp_orbit_by_2032": p_fsp_by_2032,
        "p_fsp_orbit_by_2035": p_fsp_by_2035,
        "p_fsp_orbit_by_2040": p_fsp_by_2040,
        "p_500kWe_orbit_by_2035": p_500_by_2035,
        "p_500kWe_orbit_by_2040": p_500_by_2040,
        "p_megawatt_orbit_by_2040": p_mw_by_2040,
        "p_megawatt_orbit_by_2045": p_mw_by_2045,
        "p_megawatt_ever_in_50yr_horizon": p_mw_ever,
        "median_fsp_year_offset_given_success": median_fsp_year_offset,
        "median_megawatt_year_offset_given_arrival": median_mw_year_offset,
    }


def main() -> None:
    rng = np.random.default_rng(SEED)

    per_prior = {}
    for prior_name, (alpha, beta) in PRIORS.items():
        # Each prior gets its own independent stream from the master rng.
        # Use a sub-rng seeded deterministically from the prior name to keep results
        # reproducible across reruns even if PRIORS dict is reordered.
        sub_seed = abs(hash(prior_name)) % (2**32)
        sub_rng = np.random.default_rng(sub_seed)
        per_prior[prior_name] = run_one_prior(alpha, beta, sub_rng)

    # Build matrix overlay: for each architecture cell, weight conditional delivered mass
    # by the relevant reactor-class probability under each prior.
    overlay = {}
    for cell_name, cell_data in MATRIX_CELLS_CONDITIONAL.items():
        cell_overlay = {
            "delivered_mass_conditional_t": cell_data["delivered_mass_t_per_mission"],
            "reactor_class": cell_data["reactor_class"],
            "expected_delivered_mass_by_prior": {},
        }
        for prior_name in PRIORS:
            r = per_prior[prior_name]
            if cell_data["reactor_class"] == "fsp_derivative_500kWe":
                p_avail = r["p_500kWe_orbit_by_2035"]
            elif cell_data["reactor_class"] == "megawatt":
                p_avail = r["p_megawatt_orbit_by_2040"]  # generous: 5y past window
            else:
                p_avail = 0.0
            cell_overlay["expected_delivered_mass_by_prior"][prior_name] = {
                "p_reactor_available_by_window": p_avail,
                "expected_delivered_mass_t": p_avail * cell_data["delivered_mass_t_per_mission"],
            }
        overlay[cell_name] = cell_overlay

    # Headline summary: prior-bracket on P(any United States fission orbit by 2035).
    headline = {
        prior_name: per_prior[prior_name]["p_fsp_orbit_by_2035"] for prior_name in PRIORS
    }
    bracket_ratio = (
        headline["uniform_beta_1_1"] / headline["skeptical_beta_0p5_5"]
        if headline["skeptical_beta_0p5_5"] > 0
        else float("inf")
    )

    # Pre-registration grading.
    pre_reg = {
        "H-pbu-a_uniform_p_fission_by_2035": (headline["uniform_beta_1_1"], 0.07, 0.14, 0.10),
        "H-pbu-b_jeffreys_p_fission_by_2035": (headline["jeffreys_beta_0p5_0p5"], 0.04, 0.09, 0.06),
        "H-pbu-c_skeptical_p_fission_by_2035": (headline["skeptical_beta_0p5_5"], 0.02, 0.06, 0.035),
        "H-pbu-d_bracket_ratio_uniform_over_skeptical": (bracket_ratio, 2.0, 4.5, 2.9),
        "H-pbu-e_variant_B_500kWe_overlay_t_uniform": (
            overlay["variant_B_500kWe_chemical_kick_plus_electric_inbound"][
                "expected_delivered_mass_by_prior"
            ]["uniform_beta_1_1"]["expected_delivered_mass_t"],
            10.0,
            35.0,
            18.0,
        ),
    }

    summary = {
        "seed": SEED,
        "n_trajectories": N_TRAJECTORIES,
        "base_year": BASE_YEAR,
        "demonstrator_window_year_offset": DEMONSTRATOR_WINDOW_YEAR,
        "priors_swept": {k: list(v) for k, v in PRIORS.items()},
        "fsp_likelihood_factors": FSP_LIKELIHOOD_FACTORS,
        "p_500kWe_funded_given_fsp": P_500_FUNDED_GIVEN_FSP,
        "p_megawatt_funded_given_fsp": P_MW_FUNDED_GIVEN_FSP,
        "headline_p_fission_orbit_by_2035_by_prior": headline,
        "bracket_ratio_uniform_over_skeptical": bracket_ratio,
        "per_prior_full": per_prior,
        "pre_registration_grading": {
            name: {
                "measured": meas,
                "lo": lo,
                "hi": hi,
                "point_estimate": pe,
                "held": lo <= meas <= hi,
            }
            for name, (meas, lo, hi, pe) in pre_reg.items()
        },
    }
    out_path = RESULTS_DIR / "R_power_bayesian_update_summary.json"
    out_path.write_text(json.dumps(summary, indent=2))
    print(f"wrote {out_path}")

    overlay_path = RESULTS_DIR / "matrix_overlay.json"
    overlay_path.write_text(json.dumps(overlay, indent=2))
    print(f"wrote {overlay_path}")

    # Console print.
    print("\nThree-prior bracket on P(any United States fission orbit by 2035):")
    for prior_name in PRIORS:
        r = per_prior[prior_name]
        print(
            f"  {prior_name:<28} alpha+0={r['alpha_posterior']:.2f} beta+6={r['beta_posterior']:.2f}"
            f"  posterior-mean-per-decade={r['posterior_mean_per_decade_rate']:.3f}"
            f"  P(by 2035)={r['p_fsp_orbit_by_2035']:.3f}"
        )
    print(f"\nBracket ratio (uniform / skeptical): {bracket_ratio:.2f}")

    print("\nMatrix overlay — expected delivered mass per mission (uniform prior):")
    for cell_name, cell in overlay.items():
        u = cell["expected_delivered_mass_by_prior"]["uniform_beta_1_1"]
        print(
            f"  {cell_name:<55} cond={cell['delivered_mass_conditional_t']:.1f}t"
            f"  P(reactor)={u['p_reactor_available_by_window']:.3f}"
            f"  expected={u['expected_delivered_mass_t']:.2f}t"
        )

    print("\nPre-registration grading:")
    print(f"  {'claim':<48} {'measured':>10} {'lo':>8} {'hi':>8} {'PE':>8} {'held?':>10}")
    for name, (meas, lo, hi, pe) in pre_reg.items():
        marker = "HELD" if lo <= meas <= hi else "FALSIFIED"
        print(f"  {name:<48} {meas:>10.4g} {lo:>8.3g} {hi:>8.3g} {pe:>8.3g} {marker:>10}")


if __name__ == "__main__":
    main()
