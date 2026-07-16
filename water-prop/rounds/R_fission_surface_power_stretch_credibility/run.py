"""R-fission-surface-power-stretch-credibility — Bayesian cascade Monte Carlo.

Five-stage conditional cascade for Architecture-D-fission's specific-power
condition met by 2035. Uniform priors over pre-registered ranges from the
locked-belief evidence and policy context (Fission-Surface-Power Phase 1
status, August 2025 Duffy directive, August 2025 Draft Announcement, US
space-fission base rate 0-of-6 since 1965).

100,000-sample Monte Carlo. Deterministic given seed.
"""

from __future__ import annotations

import json
import random
import statistics
from pathlib import Path

SEED = 20260515
N_SAMPLES = 100_000

# Pre-registered conditional probability ranges (uniform priors).
STAGES = [
    ("phase2_awarded_by_FY27", 0.30, 0.65),
    ("phase2_commits_10W_per_kg", 0.35, 0.70),
    ("10W_per_kg_achieved_on_demonstrator_by_2032", 0.10, 0.35),
    ("flight_demonstrator_launched_by_2035", 0.15, 0.40),
    ("ICEBERG_integration_at_200_300kWe", 0.40, 0.75),
]

# Solar-thermal credibility band from rounds 1-2 cascade (round-2 STATE.md):
# P(mirror-at-scale qualified) 0.05-0.35
# P(SOEC space-qualified)      0.10-0.50
# P(Saturn-orbit conops)       0.55-0.85
# P(per-mission completion)    0.40-0.75
SOLAR_THERMAL_STAGES = [
    ("mirror_at_30000m2_qualified_by_2035", 0.05, 0.35),
    ("SOEC_at_200kW_space_qualified_by_2035", 0.10, 0.50),
    ("saturn_orbit_conops_viable_for_chunk_delivery", 0.55, 0.85),
    ("ICEBERG_integration_per_mission_completion", 0.40, 0.75),
]


def run_cascade(stages, rng):
    posteriors = []
    for _ in range(N_SAMPLES):
        p = 1.0
        for _, lo, hi in stages:
            p *= rng.uniform(lo, hi)
        posteriors.append(p)
    return posteriors


def summarize(samples):
    samples_sorted = sorted(samples)

    def pct(q):
        idx = int(q * len(samples_sorted))
        idx = max(0, min(idx, len(samples_sorted) - 1))
        return samples_sorted[idx]

    return {
        "mean": statistics.mean(samples),
        "median": pct(0.5),
        "p05": pct(0.05),
        "p25": pct(0.25),
        "p75": pct(0.75),
        "p95": pct(0.95),
        "p_above_0p02": sum(1 for s in samples if s > 0.02) / len(samples),
        "p_above_0p05": sum(1 for s in samples if s > 0.05) / len(samples),
        "p_above_0p10": sum(1 for s in samples if s > 0.10) / len(samples),
        "p_above_0p15": sum(1 for s in samples if s > 0.15) / len(samples),
    }


def classify_credibility(median: float) -> str:
    if median > 0.15:
        return "FALSIFIES_REFRAME_higher_than_solar_thermal"
    if median < 0.02:
        return "FALSIFIES_REFRAME_lower_than_solar_thermal"
    if 0.03 <= median <= 0.10:
        return "UPHOLDS_same_credibility_band"
    return "MARGINAL_between_bands"


def main():
    rng_fission = random.Random(SEED)
    rng_solar = random.Random(SEED + 1)

    fission = run_cascade(STAGES, rng_fission)
    solar = run_cascade(SOLAR_THERMAL_STAGES, rng_solar)

    fis_sum = summarize(fission)
    sol_sum = summarize(solar)

    fis_sum["classification_vs_solar_thermal_band"] = classify_credibility(
        fis_sum["median"]
    )

    out_dir = Path(__file__).resolve().parent / "results"
    out_dir.mkdir(parents=True, exist_ok=True)

    payload = {
        "seed": SEED,
        "n_samples": N_SAMPLES,
        "fission_stages_uniform_prior_ranges": STAGES,
        "solar_thermal_stages_uniform_prior_ranges": SOLAR_THERMAL_STAGES,
        "fission_posterior": fis_sum,
        "solar_thermal_posterior": sol_sum,
    }
    (out_dir / "cascade_montecarlo.json").write_text(json.dumps(payload, indent=2))

    lines = [
        "# R-fission-surface-power-stretch-credibility — results\n",
        f"Seed {SEED}, {N_SAMPLES} samples.\n",
        "## Fission cascade stages",
        "",
        "| Stage | Lo | Hi |",
        "|---|---|---|",
    ]
    for name, lo, hi in STAGES:
        lines.append(f"| {name} | {lo:.2f} | {hi:.2f} |")
    lines.extend([
        "",
        "## Solar-thermal cascade stages (for comparison)",
        "",
        "| Stage | Lo | Hi |",
        "|---|---|---|",
    ])
    for name, lo, hi in SOLAR_THERMAL_STAGES:
        lines.append(f"| {name} | {lo:.2f} | {hi:.2f} |")

    lines.extend([
        "",
        "## Posterior comparison",
        "",
        "| Statistic | D-fission posterior | D-solar-thermal posterior |",
        "|---|---|---|",
        f"| Mean | {fis_sum['mean']:.4f} | {sol_sum['mean']:.4f} |",
        f"| Median | {fis_sum['median']:.4f} | {sol_sum['median']:.4f} |",
        f"| 5th percentile | {fis_sum['p05']:.4f} | {sol_sum['p05']:.4f} |",
        f"| 25th percentile | {fis_sum['p25']:.4f} | {sol_sum['p25']:.4f} |",
        f"| 75th percentile | {fis_sum['p75']:.4f} | {sol_sum['p75']:.4f} |",
        f"| 95th percentile | {fis_sum['p95']:.4f} | {sol_sum['p95']:.4f} |",
        f"| P(posterior > 0.02) | {fis_sum['p_above_0p02']:.3f} | {sol_sum['p_above_0p02']:.3f} |",
        f"| P(posterior > 0.05) | {fis_sum['p_above_0p05']:.3f} | {sol_sum['p_above_0p05']:.3f} |",
        f"| P(posterior > 0.10) | {fis_sum['p_above_0p10']:.3f} | {sol_sum['p_above_0p10']:.3f} |",
        f"| P(posterior > 0.15) | {fis_sum['p_above_0p15']:.3f} | {sol_sum['p_above_0p15']:.3f} |",
        "",
        f"## Falsification verdict: {fis_sum['classification_vs_solar_thermal_band']}",
        "",
        "Pre-registered rule: hypothesis (D-fission and D-solar-thermal in same credibility band) ",
        "UPHELD if median in [0.03, 0.10]. FALSIFIED below 0.02 (fission less credible) ",
        "or above 0.15 (fission more credible). MARGINAL between [0.02, 0.03) or (0.10, 0.15].",
    ])

    (out_dir / "tables.md").write_text("\n".join(lines) + "\n")

    print(f"D-fission posterior: mean {fis_sum['mean']:.4f}, median {fis_sum['median']:.4f}")
    print(f"  5/25/75/95: {fis_sum['p05']:.4f} / {fis_sum['p25']:.4f} / {fis_sum['p75']:.4f} / {fis_sum['p95']:.4f}")
    print(f"  P(>0.02)={fis_sum['p_above_0p02']:.3f}, P(>0.05)={fis_sum['p_above_0p05']:.3f}, P(>0.10)={fis_sum['p_above_0p10']:.3f}")
    print()
    print(f"D-solar-thermal posterior: mean {sol_sum['mean']:.4f}, median {sol_sum['median']:.4f}")
    print(f"  5/25/75/95: {sol_sum['p05']:.4f} / {sol_sum['p25']:.4f} / {sol_sum['p75']:.4f} / {sol_sum['p95']:.4f}")
    print(f"  P(>0.02)={sol_sum['p_above_0p02']:.3f}, P(>0.05)={sol_sum['p_above_0p05']:.3f}, P(>0.10)={sol_sum['p_above_0p10']:.3f}")
    print()
    print(f"Falsification verdict: {fis_sum['classification_vs_solar_thermal_band']}")


if __name__ == "__main__":
    main()
