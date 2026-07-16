#!/usr/bin/env python3
"""
R-LEO-water-demand-curve — what fraction of plausible 2030s clearing-price
scenarios make ICEBERG NPV-positive?

10,000-sample Monte Carlo over (Starship $/kg-to-LEO, in-space markup),
combined as clearing_price = Starship × markup. Maps clearing price to
revenue per mission via per-architecture delivered mass, then checks
against round-7 break-even thresholds.

Deterministic; seeded for reproducibility. Round-7 break-even table is
hard-coded from `R_fleet_ramp_NPV/results/fleet_ramp_npv_summary.json`
(headline_table) for traceability.

Author: enceladus-r5, 2026-05-15 (round 8).
"""
from __future__ import annotations

import csv
import json
import math
import random
from dataclasses import dataclass
from pathlib import Path

RESULTS_DIR = Path(__file__).parent / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

SEED = 20260515
N_SAMPLES = 10000


# ---------------------------------------------------------------------------
# Architectures with per-mission delivered mass (anchored to round-7)
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class Architecture:
    name: str
    delivered_t: float  # tonnes per mission


ARCHITECTURES = [
    Architecture("E_500kWe_200t", 50.0),
    Architecture("E_200kWe_100t", 30.0),
    Architecture("VariantB_500kWe", 80.0),
]


# ---------------------------------------------------------------------------
# Round-7 break-even revenue per mission ($M)
# Sourced from R_fleet_ramp_NPV/results/fleet_ramp_npv_summary.json
# (single-flight, NRE=0, op-cost=0).
# Format: [architecture_name][wacc][learning_rate] = break-even in $M/mission
# ---------------------------------------------------------------------------
ROUND7_BREAKEVEN_M = {
    "E_500kWe_200t": {
        0.000: {0.00: 300,  0.10: 167,  0.15: 167,  0.20: 136},
        0.030: {0.00: 603,  0.10: 346,  0.15: 346,  0.20: 285},
        0.060: {0.00: 1187, 0.10: 700,  0.15: 700,  0.20: 583},
        0.087: {0.00: 2149, 0.10: 1298, 0.15: 1298, 0.20: 1090},
        0.120: {0.00: 4352, 0.10: 2701, 0.15: 2701, 0.20: 2293},
    },
    "E_200kWe_100t": {
        0.000: {0.00: 250,  0.10: 138,  0.15: 138,  0.20: 112},
        0.030: {0.00: 487,  0.10: 276,  0.15: 276,  0.20: 227},
        0.060: {0.00: 930,  0.10: 544,  0.15: 544,  0.20: 451},
        0.087: {0.00: 1639, 0.10: 983,  0.15: 983,  0.20: 824},
        0.120: {0.00: 3216, 0.10: 1985, 0.15: 1985, 0.20: 1682},
    },
    "VariantB_500kWe": {
        0.000: {0.00: 500,  0.10: 253,  0.15: 253,  0.20: 199},
        0.030: {0.00: 768,  0.10: 407,  0.15: 407,  0.20: 326},
        0.060: {0.00: 1164, 0.10: 645,  0.15: 645,  0.20: 525},
        0.087: {0.00: 1676, 0.10: 964,  0.15: 964,  0.20: 797},
        0.120: {0.00: 2586, 0.10: 1549, 0.15: 1549, 0.20: 1300},
    },
}
# NOTE: Round-7 headline table reports LR={0, 15, 20} only. LR=10 is interpolated
# (linear in log-space) for sweep continuity. LR=15 row uses LR=10 value as a
# proxy where round-7 didn't compute it — left as LR=10 == LR=15 above and
# corrected below.

# Fix: re-derive LR=10 by interpolation between LR=0 and LR=15:
# Wright's-Law cumulative-average cost factor is monotonic in LR.
# Just use linear interpolation for the break-even values for LR=10:
for arch_name, w_dict in ROUND7_BREAKEVEN_M.items():
    for wacc, lr_dict in w_dict.items():
        if 0.0 in lr_dict and 0.15 in lr_dict:
            lr_dict[0.10] = round(lr_dict[0.0] + (lr_dict[0.15] - lr_dict[0.0]) * (0.10 / 0.15))


# ---------------------------------------------------------------------------
# Log-normal sampler
# ---------------------------------------------------------------------------
def sample_lognormal(rng: random.Random, p05_value: float, p95_value: float,
                      median: float) -> float:
    """Sample from a log-normal whose 5th and 95th percentiles match the given
    values. median is used for sanity / sigma calc."""
    # mu = ln(median); sigma = (ln(p95) - ln(p05)) / (2 * 1.645)
    mu = math.log(median)
    sigma = (math.log(p95_value) - math.log(p05_value)) / (2.0 * 1.645)
    # Sample normal then exponentiate
    z = rng.gauss(0.0, 1.0)
    return math.exp(mu + sigma * z)


# ---------------------------------------------------------------------------
# Monte Carlo: clearing price distribution
# ---------------------------------------------------------------------------
def run_monte_carlo(rng: random.Random, n_samples: int = N_SAMPLES) -> list[dict]:
    """Draw n_samples of (starship, markup, clearing) and compute revenue per
    architecture."""
    rows = []
    for i in range(n_samples):
        starship = sample_lognormal(rng, 200.0, 15000.0, 1500.0)
        markup = sample_lognormal(rng, 1.2, 15.0, 3.5)
        clearing = starship * markup
        row = {
            "sample_idx": i,
            "starship_per_kg": starship,
            "markup": markup,
            "clearing_per_kg": clearing,
        }
        for arch in ARCHITECTURES:
            row[f"revenue_M_{arch.name}"] = clearing * arch.delivered_t * 1000.0 / 1e6
        rows.append(row)
    return rows


def percentiles(values: list[float], pcts: list[float]) -> dict:
    sorted_vals = sorted(values)
    out = {}
    n = len(sorted_vals)
    for p in pcts:
        idx = min(n - 1, max(0, int(p * n)))
        out[f"p{int(p*100):02d}"] = sorted_vals[idx]
    return out


# ---------------------------------------------------------------------------
# NPV-positive probability per (arch, wacc, lr)
# ---------------------------------------------------------------------------
def compute_p_npv_positive(rows: list[dict]) -> dict:
    """For each (arch, wacc, lr) cell in round-7 break-even table, count what
    fraction of MC samples have revenue ≥ break-even."""
    out = {}
    for arch in ARCHITECTURES:
        out[arch.name] = {}
        for wacc, lr_dict in ROUND7_BREAKEVEN_M[arch.name].items():
            out[arch.name][wacc] = {}
            for lr, be_M in lr_dict.items():
                rev_key = f"revenue_M_{arch.name}"
                n_pos = sum(1 for r in rows if r[rev_key] >= be_M)
                out[arch.name][wacc][lr] = {
                    "breakeven_M": be_M,
                    "p_npv_positive": n_pos / len(rows),
                    "n_samples_above": n_pos,
                }
    return out


def compute_p_any_arch_positive(rows: list[dict]) -> dict:
    """For each (wacc, lr), probability that AT LEAST ONE architecture is
    NPV-positive."""
    out = {}
    for wacc in sorted(ROUND7_BREAKEVEN_M["E_500kWe_200t"].keys()):
        out[wacc] = {}
        for lr in sorted(ROUND7_BREAKEVEN_M["E_500kWe_200t"][wacc].keys()):
            n_any = 0
            for r in rows:
                any_pos = False
                for arch in ARCHITECTURES:
                    be = ROUND7_BREAKEVEN_M[arch.name][wacc][lr]
                    if r[f"revenue_M_{arch.name}"] >= be:
                        any_pos = True
                        break
                if any_pos:
                    n_any += 1
            out[wacc][lr] = n_any / len(rows)
    return out


# ---------------------------------------------------------------------------
# Cross-checks
# ---------------------------------------------------------------------------
def run_crosschecks(rows: list[dict]) -> dict:
    out = {}

    # CC1: Reference draw α (median scenario). Sample where Starship ≈ $1,500
    # and markup ≈ 3.5 → clearing ≈ $5,250/kg. Verify revenue / mission.
    median_starship = sorted(r["starship_per_kg"] for r in rows)[len(rows) // 2]
    median_markup = sorted(r["markup"] for r in rows)[len(rows) // 2]
    median_clearing = sorted(r["clearing_per_kg"] for r in rows)[len(rows) // 2]
    out["cc1_median_inputs"] = {
        "expected_starship_per_kg": 1500.0,
        "measured_starship_p50": median_starship,
        "expected_markup": 3.5,
        "measured_markup_p50": median_markup,
        "expected_clearing_per_kg_at_independent_median": 1500.0 * 3.5,
        "measured_clearing_p50": median_clearing,
        # Note: median of product ≠ product of medians for independent log-normals
        # in general; for log-normals the median of product IS the product of medians.
        "passes_starship": abs(median_starship - 1500.0) / 1500.0 < 0.05,
        "passes_markup": abs(median_markup - 3.5) / 3.5 < 0.05,
    }

    # CC2: Verify percentile bands of input distributions are close to specification.
    starship_pcts = percentiles([r["starship_per_kg"] for r in rows], [0.05, 0.50, 0.95])
    markup_pcts = percentiles([r["markup"] for r in rows], [0.05, 0.50, 0.95])
    clearing_pcts = percentiles([r["clearing_per_kg"] for r in rows], [0.05, 0.50, 0.95])
    out["cc2_input_percentiles"] = {
        "starship": {"expected": {"p05": 200, "p50": 1500, "p95": 15000}, "measured": starship_pcts},
        "markup": {"expected": {"p05": 1.2, "p50": 3.5, "p95": 15}, "measured": markup_pcts},
        "clearing": {"measured": clearing_pcts,
                     "expected_p50": 5250.0,
                     "expected_p05_rough": 200.0 * 1.2,
                     "expected_p95_rough": 15000.0 * 15.0},
    }

    # CC3: Independent verification of reference draw β (favorable, $24,000/kg)
    # → Variant B revenue $1,920M, clears corp 8.7% LR 15% ($964M)
    be_b_corp_lr15 = ROUND7_BREAKEVEN_M["VariantB_500kWe"][0.087][0.15]
    rev_b_at_24k = 24000.0 * 80.0 * 1000.0 / 1e6  # = $1,920M
    out["cc3_reference_draw_beta"] = {
        "clearing_per_kg": 24000.0,
        "computed_VariantB_revenue_M": rev_b_at_24k,
        "VariantB_BE_corp_LR15_M": be_b_corp_lr15,
        "clears_corp_LR15": rev_b_at_24k >= be_b_corp_lr15,
        "expected_clears": True,
    }

    return out


# ---------------------------------------------------------------------------
# Hypothesis grading
# ---------------------------------------------------------------------------
def grade_hypotheses(rows: list[dict], p_npv: dict, p_any: dict, crosschecks: dict) -> dict:
    grades = {}

    # H-8-a: Median clearing price 5,000-7,500
    median_clearing = sorted(r["clearing_per_kg"] for r in rows)[len(rows) // 2]
    grades["H8a"] = {
        "predicted_band": [5000, 7500],
        "measured": median_clearing,
        "held": 5000 <= median_clearing <= 7500,
    }

    # H-8-b: 5th-95th percentile spread
    p05 = sorted(r["clearing_per_kg"] for r in rows)[int(0.05 * len(rows))]
    p95 = sorted(r["clearing_per_kg"] for r in rows)[int(0.95 * len(rows))]
    grades["H8b"] = {
        "predicted_band_p05": [200, 500],  # ~$200-500/kg
        "predicted_band_p95": [50000, 150000],  # ~$50k-$150k/kg
        "measured_p05": p05,
        "measured_p95": p95,
        "held": (200 <= p05 <= 500) and (50000 <= p95 <= 150000),
    }

    # H-8-c: P(VariantB NPV+ at sov 3%, LR 15%) in 50-65%
    p_b_sov = p_npv["VariantB_500kWe"][0.030][0.15]["p_npv_positive"]
    grades["H8c"] = {
        "predicted_band_pct": [50, 65],
        "measured_pct": p_b_sov * 100,
        "held": 0.50 <= p_b_sov <= 0.65,
    }

    # H-8-d: P(VariantB NPV+ at corp 8.7%, LR 15%) in 20-35%
    p_b_corp = p_npv["VariantB_500kWe"][0.087][0.15]["p_npv_positive"]
    grades["H8d"] = {
        "predicted_band_pct": [20, 35],
        "measured_pct": p_b_corp * 100,
        "held": 0.20 <= p_b_corp <= 0.35,
    }

    # H-8-e: P(E_500 NPV+ at sov 3%, LR 15%) in 40-55%
    p_e500_sov = p_npv["E_500kWe_200t"][0.030][0.15]["p_npv_positive"]
    grades["H8e"] = {
        "predicted_band_pct": [40, 55],
        "measured_pct": p_e500_sov * 100,
        "held": 0.40 <= p_e500_sov <= 0.55,
    }

    # H-8-f: P(E_500 NPV+ at corp 8.7%, LR 15%) in 10-25%
    p_e500_corp = p_npv["E_500kWe_200t"][0.087][0.15]["p_npv_positive"]
    grades["H8f"] = {
        "predicted_band_pct": [10, 25],
        "measured_pct": p_e500_corp * 100,
        "held": 0.10 <= p_e500_corp <= 0.25,
    }

    # H-8-g: P(E_200 NPV+ at sov 3%, LR 15%) in 35-50%
    p_e200_sov = p_npv["E_200kWe_100t"][0.030][0.15]["p_npv_positive"]
    grades["H8g"] = {
        "predicted_band_pct": [35, 50],
        "measured_pct": p_e200_sov * 100,
        "held": 0.35 <= p_e200_sov <= 0.50,
    }

    # H-8-h: P(at least one arch NPV+ at corp 8.7% LR 15%) in 25-40%
    p_any_corp = p_any[0.087][0.15]
    grades["H8h"] = {
        "predicted_band_pct": [25, 40],
        "measured_pct": p_any_corp * 100,
        "held": 0.25 <= p_any_corp <= 0.40,
    }

    # H-8-i: P(at least one arch NPV+ at sov 3% LR 15%) in 55-75%
    p_any_sov = p_any[0.030][0.15]
    grades["H8i"] = {
        "predicted_band_pct": [55, 75],
        "measured_pct": p_any_sov * 100,
        "held": 0.55 <= p_any_sov <= 0.75,
    }

    # H-8-j: Expected (mean) revenue per mission for VariantB in $700M-$1,500M
    mean_rev_b = sum(r["revenue_M_VariantB_500kWe"] for r in rows) / len(rows)
    grades["H8j"] = {
        "predicted_band_M": [700, 1500],
        "measured_M": mean_rev_b,
        "held": 700 <= mean_rev_b <= 1500,
    }

    # H-8-k: P(Starship ≤ $1,000/kg) in 30-45%
    n_starship_le_1000 = sum(1 for r in rows if r["starship_per_kg"] <= 1000.0)
    p_starship_le_1000 = n_starship_le_1000 / len(rows)
    grades["H8k"] = {
        "predicted_band_pct": [30, 45],
        "measured_pct": p_starship_le_1000 * 100,
        "held": 0.30 <= p_starship_le_1000 <= 0.45,
    }

    # H-8-l: VariantB dominates E_500 on P(NPV+) at all 3 WACC levels
    dominates = []
    for wacc in [0.030, 0.060, 0.087]:
        p_b = p_npv["VariantB_500kWe"][wacc][0.15]["p_npv_positive"]
        p_e = p_npv["E_500kWe_200t"][wacc][0.15]["p_npv_positive"]
        dominates.append((wacc, p_b > p_e, p_b, p_e))
    all_dominate = all(d[1] for d in dominates)
    grades["H8l"] = {
        "predicted": "VariantB > E_500 at all 3 WACC",
        "by_wacc": dominates,
        "held": all_dominate,
    }

    return grades


# ---------------------------------------------------------------------------
# Headline reports
# ---------------------------------------------------------------------------
def headline(rows: list[dict], p_npv: dict, p_any: dict) -> dict:
    clearing_pcts = percentiles([r["clearing_per_kg"] for r in rows], [0.05, 0.25, 0.50, 0.75, 0.95])
    return {
        "clearing_price_distribution": clearing_pcts,
        "p_npv_positive_summary": {
            arch: {
                f"WACC_{wacc}_LR_{lr}": d["p_npv_positive"]
                for wacc, lr_dict in p_npv[arch].items()
                for lr, d in lr_dict.items()
                if lr in [0.0, 0.15]
            }
            for arch in p_npv
        },
        "p_any_arch_positive": {
            f"WACC_{wacc}_LR_{lr}": p_any[wacc][lr]
            for wacc in p_any
            for lr in p_any[wacc]
            if lr in [0.0, 0.15]
        },
    }


def main() -> None:
    rng = random.Random(SEED)

    print(f"Running Monte Carlo with seed {SEED}, {N_SAMPLES} samples...")
    rows = run_monte_carlo(rng, N_SAMPLES)

    print("\nRunning cross-checks...")
    cc = run_crosschecks(rows)
    for name, c in cc.items():
        print(f"  {name}: {c}")

    print("\nComputing P(NPV+) per (arch, WACC, LR)...")
    p_npv = compute_p_npv_positive(rows)
    p_any = compute_p_any_arch_positive(rows)

    print("\nP(NPV+) summary at LR=0.15:")
    print(f"{'arch':>20} {'WACC':>6} {'BE_$M':>10} {'P(NPV+)':>10}")
    for arch_name in p_npv:
        for wacc in sorted(p_npv[arch_name]):
            d = p_npv[arch_name][wacc][0.15]
            print(f"{arch_name:>20} {wacc:>6.3f} {d['breakeven_M']:>10} {d['p_npv_positive']*100:>9.1f}%")

    print("\nP(any arch NPV+) at LR=0.15:")
    for wacc in sorted(p_any):
        print(f"  WACC {wacc:.3f}: {p_any[wacc][0.15]*100:.1f}%")

    print("\nGrading hypotheses...")
    grades = grade_hypotheses(rows, p_npv, p_any, cc)
    for name, g in grades.items():
        held = g.get("held", False)
        flag = "HELD" if held else "FALSIFIED"
        print(f"  {name}: {flag} — {g}")

    head = headline(rows, p_npv, p_any)

    summary = {
        "round": "R-LEO-water-demand-curve",
        "author": "enceladus-r5",
        "date": "2026-05-15",
        "seed": SEED,
        "n_samples": N_SAMPLES,
        "crosschecks": cc,
        "headline": head,
        "p_npv_positive": p_npv,
        "p_any_arch_positive": p_any,
        "grades": grades,
        "input_distributions": {
            "starship_per_kg": {"p05": 200, "p50": 1500, "p95": 15000, "type": "log-normal"},
            "markup": {"p05": 1.2, "p50": 3.5, "p95": 15.0, "type": "log-normal"},
        },
        "architectures": [{"name": a.name, "delivered_t": a.delivered_t} for a in ARCHITECTURES],
    }
    json_path = RESULTS_DIR / "demand_curve_summary.json"
    with open(json_path, "w") as f:
        json.dump(summary, f, indent=2, default=str)
    print(f"\nWrote {json_path}")

    # Write per-sample CSV (small; 10k rows × 7 cols ≈ 700 KB)
    csv_path = RESULTS_DIR / "demand_curve_samples.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {csv_path}")


if __name__ == "__main__":
    main()
