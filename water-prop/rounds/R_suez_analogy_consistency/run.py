#!/usr/bin/env python3
"""
R-Suez-analogy-consistency-check — apply SCA-style margin-fraction regulation
(33-40 percent of alternative-route savings captured) to ICEBERG's MC draws.
Report the implied clearing-price-cap distribution and compare to R15's
sign-flip threshold of $18.6k/kg (clearing p79).

Empirical anchors (cited in STUDY.md):
- SCA toll per large container transit: $580-800k (post-2025).
- Cape route additional cost: $1-2M per large container round-trip.
- Implied SCA margin fraction = toll / route-cost-differential ≈ 33-40 percent.

ICEBERG marginal cost (per delivered kg):
- 2-launch: $200M opex / 80,000 kg delivered = $2,500/kg.
- 3-launch: $300M opex / 80,000 kg = $3,750/kg.

Apply per-draw cap: cap_per_kg = ICEBERG_MC + margin_fraction × max(0, Starship - ICEBERG_MC).
"""
from __future__ import annotations

import importlib.util
import json
import math
import random
import sys
from pathlib import Path

THIS_DIR = Path(__file__).parent
RESULTS_DIR = THIS_DIR / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# Import R14 (which transitively loads R13 and hetcad).
RD14_RUN_PATH = THIS_DIR.parent / "R_staged_commitment_underwriter_anchor" / "run.py"
spec = importlib.util.spec_from_file_location("rd14_run", RD14_RUN_PATH)
rd14 = importlib.util.module_from_spec(spec)
sys.modules["rd14_run"] = rd14
spec.loader.exec_module(rd14)

rd13 = rd14.rd13
hetcad = rd14.hetcad

SEED = rd14.SEED  # 20260515
N_MC = rd14.N_MC  # 10000
LAUNCH_COUNT = rd14.LAUNCH_COUNT  # 2
WACC = rd14.WACC  # 0.03
LR = rd14.LR  # 0.15
CHUNK_T = rd14.CHUNK_T  # 200

# Empirical Suez margin-fraction anchors
SUEZ_MARGIN_LOW = 0.33
SUEZ_MARGIN_HIGH = 0.40
SUEZ_MARGIN_MID = 0.365  # midpoint for primary table

# ICEBERG marginal cost per delivered kg
# 2-launch: LAUNCH_COST_PER_MISSION_M[2] = $200M opex per mission; delivered = 80,000 kg/mission
ICEBERG_MC_M_PER_TONNE = rd13.LAUNCH_COST_PER_MISSION_M[LAUNCH_COUNT] / 80.0  # $M/tonne = $/kg / 1000 × 1000
# 80 t per mission = 80,000 kg; $200M / 80,000 kg = $2,500/kg = $2.5M/tonne
# In hetcad/rd13 units, revenue is in $M/tonne. So:
# $200M / 80 tonnes = $2.5 M/tonne. Sanity: $/kg = M/tonne × 1000 / 1000 = M/tonne. So $2.5M/tonne = $2,500/kg. OK.
ICEBERG_MC_PER_KG = ICEBERG_MC_M_PER_TONNE * 1000.0  # = $2500


def sample_starship_per_kg(n: int) -> list[float]:
    """Re-draw the underlying Starship $/kg samples used by sample_clearing_per_tonne_M.

    Uses identical seed pattern so draws are aligned 1:1 with the clearing distribution.
    """
    rng_s = random.Random(SEED)
    return hetcad.lognormal_draws(rng_s, n, 1500.0, 200.0, 15000.0)


def sample_markup(n: int) -> list[float]:
    rng_m = random.Random(SEED + 1)
    return hetcad.lognormal_draws(rng_m, n, 3.5, 1.2, 15.0)


def pctile(xs: list[float], p: float) -> float:
    xs_sorted = sorted(xs)
    idx = int(p * len(xs_sorted))
    return xs_sorted[min(len(xs_sorted) - 1, max(0, idx))]


def main() -> None:
    print("Running R-Suez-analogy-consistency-check...")

    starship = sample_starship_per_kg(N_MC)
    markup = sample_markup(N_MC)
    clearing_per_kg = [s * m for s, m in zip(starship, markup)]

    # Compute Suez-implied cap per draw at three margin fractions
    cap_low = [ICEBERG_MC_PER_KG + SUEZ_MARGIN_LOW * max(0.0, s - ICEBERG_MC_PER_KG) for s in starship]
    cap_mid = [ICEBERG_MC_PER_KG + SUEZ_MARGIN_MID * max(0.0, s - ICEBERG_MC_PER_KG) for s in starship]
    cap_high = [ICEBERG_MC_PER_KG + SUEZ_MARGIN_HIGH * max(0.0, s - ICEBERG_MC_PER_KG) for s in starship]

    # Fraction of draws where original clearing exceeds Suez-implied cap (i.e., the cap binds)
    frac_capped_mid = sum(1 for o, c in zip(clearing_per_kg, cap_mid) if o > c) / N_MC

    # Distribution of caps and originals
    print(f"  Starship $/kg: p05={pctile(starship, 0.05):.0f}, p50={pctile(starship, 0.50):.0f}, p95={pctile(starship, 0.95):.0f}")
    print(f"  ICEBERG marginal cost: ${ICEBERG_MC_PER_KG:.0f}/kg")
    print(f"  Original clearing: p05={pctile(clearing_per_kg, 0.05):.0f}, p50={pctile(clearing_per_kg, 0.50):.0f}, p95={pctile(clearing_per_kg, 0.95):.0f}")
    print(f"  Suez-implied cap (mid 36.5%): p05={pctile(cap_mid, 0.05):.0f}, p50={pctile(cap_mid, 0.50):.0f}, p95={pctile(cap_mid, 0.95):.0f}")
    print(f"  Fraction of draws where cap binds (clearing > cap): {frac_capped_mid:.1%}")

    # Where does the Suez-implied cap sit relative to R15's sign-flip threshold ($18,600/kg = clearing p79)?
    R15_SIGN_FLIP_PER_KG = 18600.0  # from R15 cap-sweep linear interpolation
    cap_above_signflip_low = sum(1 for c in cap_low if c >= R15_SIGN_FLIP_PER_KG) / N_MC
    cap_above_signflip_mid = sum(1 for c in cap_mid if c >= R15_SIGN_FLIP_PER_KG) / N_MC
    cap_above_signflip_high = sum(1 for c in cap_high if c >= R15_SIGN_FLIP_PER_KG) / N_MC

    print(f"  Fraction of Suez-implied caps that exceed R15 sign-flip threshold ($18.6k/kg):")
    print(f"    margin 33%: {cap_above_signflip_low:.2%}")
    print(f"    margin 36.5%: {cap_above_signflip_mid:.2%}")
    print(f"    margin 40%: {cap_above_signflip_high:.2%}")

    # NPV under Suez-strict regulated clearing
    # Per draw: clearing capped at Suez-implied cap (cap_mid). Recompute Δ-NPV.
    deltas_suez = []
    deltas_uncap = []
    npv_D_suez = []
    npv_R_suez = []
    npv_D_uncap = []
    npv_R_uncap = []
    for orig_clr_kg, cap_kg in zip(clearing_per_kg, cap_mid):
        # Convert $/kg back to $M/tonne for rd13.npv_cell
        capped_clearing_M_per_tonne = min(orig_clr_kg, cap_kg) * 1000.0 / 1e6
        uncap_clearing_M_per_tonne = orig_clr_kg * 1000.0 / 1e6
        d_suez = rd13.npv_cell("D", WACC, LR, capped_clearing_M_per_tonne, launch_count=LAUNCH_COUNT)["npv_M"]
        r_suez = rd13.npv_cell("R", WACC, LR, capped_clearing_M_per_tonne, launch_count=LAUNCH_COUNT)["npv_M"]
        d_uncap = rd13.npv_cell("D", WACC, LR, uncap_clearing_M_per_tonne, launch_count=LAUNCH_COUNT)["npv_M"]
        r_uncap = rd13.npv_cell("R", WACC, LR, uncap_clearing_M_per_tonne, launch_count=LAUNCH_COUNT)["npv_M"]
        deltas_suez.append(r_suez - d_suez)
        deltas_uncap.append(r_uncap - d_uncap)
        npv_D_suez.append(d_suez)
        npv_R_suez.append(r_suez)
        npv_D_uncap.append(d_uncap)
        npv_R_uncap.append(r_uncap)

    def mean(xs):
        return sum(xs) / len(xs)

    def median(xs):
        s = sorted(xs)
        n = len(s)
        return s[n // 2] if n % 2 else 0.5 * (s[n // 2 - 1] + s[n // 2])

    print(f"\n  Mean Δ-NPV under Suez-strict regulation (margin 36.5%): ${mean(deltas_suez)/1000:.2f} B")
    print(f"  Mean Δ-NPV uncapped (sanity vs R15 -$10.6 B): ${mean(deltas_uncap)/1000:.2f} B")
    print(f"  Mean D-NPV under Suez: ${mean(npv_D_suez)/1000:.2f} B; Mean R-NPV under Suez: ${mean(npv_R_suez)/1000:.2f} B")
    print(f"  Fraction D-NPV positive under Suez: {sum(1 for x in npv_D_suez if x > 0) / N_MC:.2%}")
    print(f"  Fraction R-NPV positive under Suez: {sum(1 for x in npv_R_suez if x > 0) / N_MC:.2%}")
    print(f"  Mean program revenue per delivered kg under Suez cap (=mean capped clearing): ${mean([min(o, c) for o, c in zip(clearing_per_kg, cap_mid)]):.0f}/kg")
    print(f"  Mean capped clearing in $M/tonne: ${mean([min(o, c) * 1000 / 1e6 for o, c in zip(clearing_per_kg, cap_mid)]):.3f}")

    # Compare cap_mid to R15's clearing distribution
    cap_mid_per_tonne_M = [c / 1000.0 for c in cap_mid]  # $/kg -> $M/tonne (kg/1000=tonne; /1e6=M)
    # Wait: cap in $/kg. Convert to $M/tonne: $X/kg × 1000 kg/tonne × 1/1e6 = X/1000 $M/tonne. So $2500/kg = $2.5M/tonne.
    cap_mid_M_per_tonne = [c * 1000 / 1e6 for c in cap_mid]

    # What percentile of the R15 clearing distribution does the median Suez cap correspond to?
    median_suez_cap = median(cap_mid)
    sorted_clearing_per_kg = sorted(clearing_per_kg)
    median_cap_percentile = sum(1 for c in sorted_clearing_per_kg if c < median_suez_cap) / N_MC

    print(f"\n  Median Suez-implied cap (${median_suez_cap:.0f}/kg) sits at percentile {median_cap_percentile*100:.1f} of R15 clearing distribution")
    print(f"  R15 sign-flip threshold (~$18.6k/kg) sits at percentile 79 of R15 clearing distribution")

    result = {
        "round": "R_suez_analogy_consistency",
        "date": "2026-05-16",
        "seed": SEED,
        "n_mc": N_MC,
        "empirical_anchors": {
            "suez_margin_fraction_low": SUEZ_MARGIN_LOW,
            "suez_margin_fraction_mid": SUEZ_MARGIN_MID,
            "suez_margin_fraction_high": SUEZ_MARGIN_HIGH,
            "iceberg_marginal_cost_$_per_kg": ICEBERG_MC_PER_KG,
            "iceberg_marginal_cost_M_per_tonne": ICEBERG_MC_M_PER_TONNE,
            "r15_sign_flip_threshold_$_per_kg": R15_SIGN_FLIP_PER_KG,
        },
        "distributions": {
            "starship_$_per_kg": {
                "p05": pctile(starship, 0.05),
                "p50": pctile(starship, 0.50),
                "p95": pctile(starship, 0.95),
            },
            "original_clearing_$_per_kg": {
                "p05": pctile(clearing_per_kg, 0.05),
                "p50": pctile(clearing_per_kg, 0.50),
                "p95": pctile(clearing_per_kg, 0.95),
            },
            "suez_cap_mid_36.5pct_$_per_kg": {
                "p05": pctile(cap_mid, 0.05),
                "p50": pctile(cap_mid, 0.50),
                "p95": pctile(cap_mid, 0.95),
            },
        },
        "cap_binding_analysis": {
            "fraction_draws_where_cap_binds_margin_36_5pct": frac_capped_mid,
            "fraction_caps_above_signflip_margin_33pct": cap_above_signflip_low,
            "fraction_caps_above_signflip_margin_36_5pct": cap_above_signflip_mid,
            "fraction_caps_above_signflip_margin_40pct": cap_above_signflip_high,
            "median_suez_cap_$_per_kg": median_suez_cap,
            "median_suez_cap_at_r15_clearing_percentile": median_cap_percentile,
        },
        "npv_under_suez_regulation": {
            "mean_delta_npv_M": mean(deltas_suez),
            "mean_delta_npv_B": mean(deltas_suez) / 1000.0,
            "median_delta_npv_M": median(deltas_suez),
            "mean_npv_D_M": mean(npv_D_suez),
            "mean_npv_R_M": mean(npv_R_suez),
            "frac_npv_D_positive": sum(1 for x in npv_D_suez if x > 0) / N_MC,
            "frac_npv_R_positive": sum(1 for x in npv_R_suez if x > 0) / N_MC,
        },
        "npv_uncapped_baseline": {
            "mean_delta_npv_M": mean(deltas_uncap),
            "mean_delta_npv_B": mean(deltas_uncap) / 1000.0,
            "matches_r14_r15": abs(mean(deltas_uncap) / 1000.0 - (-10.6)) < 0.1,
        },
    }

    out_path = RESULTS_DIR / "suez_analogy_summary.json"
    out_path.write_text(json.dumps(result, indent=2, default=str))
    print(f"\n  Wrote {out_path}")


if __name__ == "__main__":
    main()
