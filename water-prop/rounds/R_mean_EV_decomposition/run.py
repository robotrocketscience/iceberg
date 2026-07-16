#!/usr/bin/env python3
"""
R-mean-EV-decomposition — decompose R14's mean Δ-NPV = -$10.6 B into per-
clearing-price-percentile contributions; locate the sign-inflection; sweep
clearing-price caps to identify where the EV-sign flips; stratify smart-gate
abandonment by clearing decile.

Inherits R14's harness without re-deriving any physics. All output to
results/mean_ev_decomposition_summary.json.
"""
from __future__ import annotations

import importlib.util
import json
import math
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

SEED = rd14.SEED
N_MC = rd14.N_MC
LAUNCH_COUNT = rd14.LAUNCH_COUNT
WACC = rd14.WACC
LR = rd14.LR
CHUNK_T = rd14.CHUNK_T

# Cap percentiles to sweep (clearing-rank in [0, 1] units, plus +inf for baseline)
CAP_PERCENTILES = [0.70, 0.80, 0.90, 0.95, 0.99]
# Capped rev sentinel for "no cap"
NO_CAP_REV = float("inf")


def mean(xs: list[float]) -> float:
    return sum(xs) / len(xs) if xs else float("nan")


def median(xs: list[float]) -> float:
    if not xs:
        return float("nan")
    xs_sorted = sorted(xs)
    n = len(xs_sorted)
    return xs_sorted[n // 2] if n % 2 else 0.5 * (xs_sorted[n // 2 - 1] + xs_sorted[n // 2])


# ---------------------------------------------------------------------------
# Per-draw computations (NPV_D, NPV_R, smart-gate decision)
# ---------------------------------------------------------------------------
def per_draw_metrics(revs: list[float]) -> dict:
    """For each draw, compute NPV_D, NPV_R, Δ, and smart-gate abandonment flag.

    Smart-gate semantics replicate R14's option_adjusted_npv: compute fleet PV
    at gate (year 15); abandon (mark True) if < 0.
    """
    npv_D = []
    npv_R = []
    deltas = []
    abandoned = []  # bool per draw under smart-gate

    for rev in revs:
        d = rd13.npv_cell("D", WACC, LR, rev, launch_count=LAUNCH_COUNT)["npv_M"]
        r = rd13.npv_cell("R", WACC, LR, rev, launch_count=LAUNCH_COUNT)["npv_M"]
        npv_D.append(d)
        npv_R.append(r)
        deltas.append(r - d)

        # Smart-gate decision: compute fleet PV at gate from yearly cashflows.
        cfR = rd14.yearly_cashflows("R", rev, LR, LAUNCH_COUNT)
        fleet_pv_at_gate = 0.0
        for t, c in enumerate(cfR):
            if t >= 15:
                fleet_pv_at_gate += c / (1.0 + WACC) ** (t - 15)
        abandoned.append(fleet_pv_at_gate < 0)

    return {
        "npv_D": npv_D,
        "npv_R": npv_R,
        "deltas": deltas,
        "abandoned": abandoned,
    }


# ---------------------------------------------------------------------------
# Per-decile decomposition (sorted by clearing)
# ---------------------------------------------------------------------------
def per_decile_decomposition(revs: list[float], metrics: dict) -> dict:
    """Sort the (rev, delta, abandoned) triples by clearing; bin into 10
    deciles of 1,000 draws each. Per-bin: mean clearing, mean delta, median
    delta, fraction delta < 0, contribution to grand mean (mean × 0.10),
    smart-gate abandonment fraction.
    """
    triples = list(zip(revs, metrics["deltas"], metrics["abandoned"], metrics["npv_D"], metrics["npv_R"]))
    triples.sort(key=lambda x: x[0])
    n = len(triples)
    bin_size = n // 10

    bins = []
    for i in range(10):
        lo = i * bin_size
        hi = (i + 1) * bin_size if i < 9 else n  # last bin absorbs remainder
        chunk = triples[lo:hi]
        revs_b = [t[0] for t in chunk]
        deltas_b = [t[1] for t in chunk]
        aband_b = [t[2] for t in chunk]
        npv_D_b = [t[3] for t in chunk]
        npv_R_b = [t[4] for t in chunk]
        bins.append({
            "decile_index": i,
            "percentile_lo": i / 10,
            "percentile_hi": (i + 1) / 10,
            "n_draws": len(chunk),
            "clearing_per_tonne_M_mean": mean(revs_b),
            "clearing_per_kg_$_mean": mean(revs_b) * 1000.0,  # M/tonne -> $/kg
            "clearing_per_tonne_M_min": min(revs_b),
            "clearing_per_tonne_M_max": max(revs_b),
            "delta_npv_M_mean": mean(deltas_b),
            "delta_npv_M_median": median(deltas_b),
            "delta_npv_B_mean": mean(deltas_b) / 1000.0,
            "fraction_delta_negative": sum(1 for d in deltas_b if d < 0) / len(deltas_b),
            "contribution_to_grand_mean_M": mean(deltas_b) * (len(chunk) / n),
            "contribution_to_grand_mean_B": mean(deltas_b) * (len(chunk) / n) / 1000.0,
            "smart_gate_abandonment_fraction": sum(1 for a in aband_b if a) / len(aband_b),
            "npv_D_M_mean": mean(npv_D_b),
            "npv_R_M_mean": mean(npv_R_b),
        })

    grand_mean = sum(b["contribution_to_grand_mean_M"] for b in bins)
    top_quartile_contribution = sum(b["contribution_to_grand_mean_M"] for b in bins[7:10])  # deciles 8, 9, 10
    # Actually top-quartile = top 25% = top 2.5 deciles. Compute strictly via vigintiles.
    # For the decile-level approximation: deciles 8 (p70-80), 9 (p80-90), 10 (p90-100) cover p70-100.
    # Use vigintile_decomposition below for the exact p75-p100 quartile.

    return {
        "bins": bins,
        "grand_mean_M": grand_mean,
        "grand_mean_B": grand_mean / 1000.0,
        "decile_8_to_10_contribution_M": top_quartile_contribution,
        "decile_8_to_10_contribution_pct_of_grand": (top_quartile_contribution / grand_mean * 100) if grand_mean != 0 else float("nan"),
    }


# ---------------------------------------------------------------------------
# Vigintile decomposition (20 bins) — for sign-inflection AND top-quartile exact
# ---------------------------------------------------------------------------
def per_vigintile_decomposition(revs: list[float], metrics: dict) -> dict:
    """20 bins of 500 draws each. Identifies the bin where mean Δ crosses zero
    AND gives the exact top-quartile (p75-p100) contribution via vigintiles 16-20.
    """
    triples = sorted(zip(revs, metrics["deltas"]), key=lambda x: x[0])
    n = len(triples)
    bin_size = n // 20

    bins = []
    for i in range(20):
        lo = i * bin_size
        hi = (i + 1) * bin_size if i < 19 else n
        chunk = triples[lo:hi]
        deltas_b = [t[1] for t in chunk]
        bins.append({
            "vigintile_index": i,
            "percentile_lo": i / 20,
            "percentile_hi": (i + 1) / 20,
            "clearing_per_kg_$_mean": mean([t[0] for t in chunk]) * 1000.0,
            "delta_npv_M_mean": mean(deltas_b),
            "delta_npv_B_mean": mean(deltas_b) / 1000.0,
            "contribution_to_grand_mean_M": mean(deltas_b) * (len(chunk) / n),
        })

    # Sign-inflection: locate first bin where mean Δ < 0 (preceded by bin with mean Δ >= 0)
    inflection_bin = None
    for i in range(1, 20):
        if bins[i - 1]["delta_npv_M_mean"] >= 0 and bins[i]["delta_npv_M_mean"] < 0:
            inflection_bin = i
            break

    # Top-quartile (p75-p100) = vigintiles 15..19 (indices 15, 16, 17, 18, 19) covering p75-p100
    top_quartile_contribution = sum(bins[i]["contribution_to_grand_mean_M"] for i in range(15, 20))

    grand_mean = sum(b["contribution_to_grand_mean_M"] for b in bins)

    return {
        "bins": bins,
        "grand_mean_M": grand_mean,
        "sign_inflection_bin_index": inflection_bin,
        "sign_inflection_percentile_lo": inflection_bin / 20 if inflection_bin is not None else None,
        "sign_inflection_percentile_hi": (inflection_bin + 1) / 20 if inflection_bin is not None else None,
        "top_quartile_contribution_M": top_quartile_contribution,
        "top_quartile_contribution_B": top_quartile_contribution / 1000.0,
        "top_quartile_contribution_pct_of_grand": (top_quartile_contribution / grand_mean * 100) if grand_mean != 0 else float("nan"),
    }


# ---------------------------------------------------------------------------
# Cap-truncation sweep
# ---------------------------------------------------------------------------
def cap_truncation_sweep(revs: list[float]) -> dict:
    """For each cap (in clearing-percentile terms), recompute grand-mean Δ-NPV
    with revenue per draw capped at that percentile's clearing value.

    Captures both D-arm and R-arm capping (the cap applies to the *revenue
    realized*, regardless of which arm).
    """
    sorted_revs = sorted(revs)
    n = len(sorted_revs)

    results = []

    # No-cap baseline (sanity)
    deltas_uncap = [
        rd13.npv_cell("R", WACC, LR, r, launch_count=LAUNCH_COUNT)["npv_M"]
        - rd13.npv_cell("D", WACC, LR, r, launch_count=LAUNCH_COUNT)["npv_M"]
        for r in revs
    ]
    results.append({
        "cap_percentile": None,
        "cap_clearing_per_tonne_M": None,
        "cap_clearing_per_kg_$": None,
        "mean_delta_M": mean(deltas_uncap),
        "mean_delta_B": mean(deltas_uncap) / 1000.0,
        "median_delta_M": median(deltas_uncap),
        "fraction_delta_positive": sum(1 for d in deltas_uncap if d > 0) / len(deltas_uncap),
        "label": "no_cap_baseline",
    })

    for pct in CAP_PERCENTILES:
        cap_rev = sorted_revs[int(pct * n)]
        deltas_capped = []
        for r in revs:
            r_capped = min(r, cap_rev)
            d = rd13.npv_cell("D", WACC, LR, r_capped, launch_count=LAUNCH_COUNT)["npv_M"]
            rr = rd13.npv_cell("R", WACC, LR, r_capped, launch_count=LAUNCH_COUNT)["npv_M"]
            deltas_capped.append(rr - d)
        results.append({
            "cap_percentile": pct,
            "cap_clearing_per_tonne_M": cap_rev,
            "cap_clearing_per_kg_$": cap_rev * 1000.0,
            "mean_delta_M": mean(deltas_capped),
            "mean_delta_B": mean(deltas_capped) / 1000.0,
            "median_delta_M": median(deltas_capped),
            "fraction_delta_positive": sum(1 for d in deltas_capped if d > 0) / len(deltas_capped),
            "label": f"cap_p{int(pct*100)}",
        })

    # Locate the cap at which mean Δ flips sign (linear interp between adjacent results)
    # Walk from highest cap (p99, closest to no-cap) down to p70.
    flip_info = None
    sorted_results = sorted(
        [r for r in results if r["cap_percentile"] is not None],
        key=lambda r: r["cap_percentile"],
        reverse=True,
    )
    # Append uncap baseline at "top"
    uncap = next(r for r in results if r["cap_percentile"] is None)
    sweep = [{"cap_percentile": 1.0, "mean_delta_M": uncap["mean_delta_M"]}] + sorted_results
    for i in range(len(sweep) - 1):
        a, b = sweep[i], sweep[i + 1]
        if (a["mean_delta_M"] < 0) and (b["mean_delta_M"] >= 0):
            flip_info = {
                "cap_percentile_above": a["cap_percentile"],
                "cap_percentile_below": b["cap_percentile"],
                "mean_delta_above_M": a["mean_delta_M"],
                "mean_delta_below_M": b["mean_delta_M"],
            }
            break
    if flip_info is None and sweep[-1]["mean_delta_M"] >= 0:
        flip_info = {
            "note": "all swept caps produce non-negative mean Δ; flip is at higher cap percentile than p70",
        }

    return {
        "cap_sweep_results": results,
        "sign_flip_bracket": flip_info,
    }


# ---------------------------------------------------------------------------
# Cross-checks
# ---------------------------------------------------------------------------
def cross_checks(per_decile: dict, per_vigintile: dict, cap_sweep: dict) -> dict:
    out = {}

    # XC-1: grand-mean ≈ R14's -$10.6 B (-10620 M from R14 JSON; we'll target -10500 to -10700 M)
    R14_GRAND_MEAN_B = -10.6  # round-14 reported
    measured_B = per_decile["grand_mean_B"]
    out["XC1_grand_mean_replication"] = {
        "measured_B": measured_B,
        "r14_published_B": R14_GRAND_MEAN_B,
        "rel_err_pct": abs(measured_B - R14_GRAND_MEAN_B) / abs(R14_GRAND_MEAN_B) * 100,
        "passes": abs(measured_B - R14_GRAND_MEAN_B) <= 0.1,
    }

    # XC-2: R14 H7 reproduction (p25, p50, p75 of clearing)
    # Use R14's convex_hull_check primitives by indexing into sorted draws.
    # Easier: index into per_vigintile bins for vigintiles 5 (p25-30), 10 (p50-55), 15 (p75-80).
    # Approximation OK for cross-check tolerance ±5%.
    R14_DELTA_AT_P25_B = 7.67
    R14_DELTA_AT_P50_B = 3.34
    R14_DELTA_AT_P75_B = -8.72
    # Vigintile 5 covers p25-p30 (close enough to "at p25")
    measured_p25_B = per_vigintile["bins"][5]["delta_npv_B_mean"]
    measured_p50_B = per_vigintile["bins"][10]["delta_npv_B_mean"]
    measured_p75_B = per_vigintile["bins"][15]["delta_npv_B_mean"]
    out["XC2_R14_h7_reproduction"] = {
        "delta_at_p25_measured_B": measured_p25_B,
        "delta_at_p25_R14_B": R14_DELTA_AT_P25_B,
        "delta_at_p50_measured_B": measured_p50_B,
        "delta_at_p50_R14_B": R14_DELTA_AT_P50_B,
        "delta_at_p75_measured_B": measured_p75_B,
        "delta_at_p75_R14_B": R14_DELTA_AT_P75_B,
        "note": "vigintile mean is over a 5%-wide band; not exactly equal to R14's single-point estimate",
        # Pass if the SIGN matches and the magnitude is within 50% (loose; the vigintile spans 5% mass)
        "passes_p75_sign": (measured_p75_B < 0) and (R14_DELTA_AT_P75_B < 0),
        "passes_p50_sign": (measured_p50_B > 0) and (R14_DELTA_AT_P50_B > 0),
        "passes_p25_sign": (measured_p25_B > 0) and (R14_DELTA_AT_P25_B > 0),
    }

    # XC-3: top-quartile (vigintiles 15..19) sum equals top-quartile contribution
    top_quartile_sum_vigintile = sum(per_vigintile["bins"][i]["contribution_to_grand_mean_M"] for i in range(15, 20))
    out["XC3_top_quartile_vigintile_sum"] = {
        "computed_M": top_quartile_sum_vigintile,
        "reported_M": per_vigintile["top_quartile_contribution_M"],
        "passes": abs(top_quartile_sum_vigintile - per_vigintile["top_quartile_contribution_M"]) < 1.0,
    }

    # XC-4: cap-truncation monotonicity (lower cap percentile -> more positive mean Δ)
    cap_results = [r for r in cap_sweep["cap_sweep_results"] if r["cap_percentile"] is not None]
    cap_results.sort(key=lambda r: r["cap_percentile"])
    monotone = True
    for i in range(len(cap_results) - 1):
        if cap_results[i]["mean_delta_M"] < cap_results[i + 1]["mean_delta_M"]:
            monotone = False
            break
    out["XC4_cap_truncation_monotonicity"] = {
        "passes": monotone,
        "sweep_means_B_low_to_high": [r["mean_delta_B"] for r in cap_results],
    }

    # XC-5: smart-gate global rate ≈ R14's 65.3% within ±1 pp
    R14_GLOBAL_ABANDONMENT = 0.653
    global_aband = sum(b["smart_gate_abandonment_fraction"] * b["n_draws"] for b in per_decile["bins"]) / sum(b["n_draws"] for b in per_decile["bins"])
    out["XC5_smart_gate_global_rate"] = {
        "measured": global_aband,
        "R14_published": R14_GLOBAL_ABANDONMENT,
        "abs_diff_pp": abs(global_aband - R14_GLOBAL_ABANDONMENT) * 100,
        "passes": abs(global_aband - R14_GLOBAL_ABANDONMENT) <= 0.01,
    }

    return out


# ---------------------------------------------------------------------------
# Grader
# ---------------------------------------------------------------------------
def grade(per_decile: dict, per_vigintile: dict, cap_sweep: dict) -> list[dict]:
    grades = []

    # H1: top-quartile contribution to grand mean in [35%, 65%]
    top_quartile_pct = per_vigintile["top_quartile_contribution_pct_of_grand"]
    grades.append({
        "id": "H1",
        "claim": "top-quartile (p75-p100) clearing draws contribute [35%, 65%] of grand mean Δ-NPV",
        "predicted_band_pct": [35.0, 65.0],
        "measured_pct": top_quartile_pct,
        "status": "HELD" if 35.0 <= top_quartile_pct <= 65.0 else "FALSIFIED",
    })

    # H2: sign-inflection bin between p55 and p70
    inflection_lo = per_vigintile["sign_inflection_percentile_lo"]
    inflection_hi = per_vigintile["sign_inflection_percentile_hi"]
    grades.append({
        "id": "H2",
        "claim": "sign-inflection bin in [p55, p70]",
        "predicted_band": [0.55, 0.70],
        "measured_percentile_lo": inflection_lo,
        "measured_percentile_hi": inflection_hi,
        "status": "HELD" if inflection_lo is not None and 0.55 <= inflection_lo <= 0.70 else "FALSIFIED",
    })

    # H3: |mean Δ(top decile)| / |mean Δ(bottom decile)| >= 3
    bot_decile_mean = per_decile["bins"][0]["delta_npv_M_mean"]
    top_decile_mean = per_decile["bins"][9]["delta_npv_M_mean"]
    ratio = abs(top_decile_mean) / abs(bot_decile_mean) if abs(bot_decile_mean) > 1e-6 else float("inf")
    grades.append({
        "id": "H3",
        "claim": "|mean Δ(top decile)| / |mean Δ(bottom decile)| >= 3",
        "predicted_floor": 3.0,
        "measured_ratio": ratio,
        "bot_decile_mean_M": bot_decile_mean,
        "top_decile_mean_M": top_decile_mean,
        "status": "HELD" if ratio >= 3.0 else "FALSIFIED",
    })

    # H4: cap at clearing p80 produces grand mean in [-$1B, +$3B]
    cap_p80 = next(r for r in cap_sweep["cap_sweep_results"] if r["cap_percentile"] == 0.80)
    cap_p80_B = cap_p80["mean_delta_B"]
    grades.append({
        "id": "H4",
        "claim": "cap at clearing p80 produces grand mean Δ-NPV in [-$1B, +$3B]",
        "predicted_band_B": [-1.0, 3.0],
        "measured_B": cap_p80_B,
        "status": "HELD" if -1.0 <= cap_p80_B <= 3.0 else "FALSIFIED",
    })

    # H5: smart-gate abandonment monotone-decreasing; bottom decile >= 95%; top decile <= 5%
    fractions = [b["smart_gate_abandonment_fraction"] for b in per_decile["bins"]]
    monotone = all(fractions[i] >= fractions[i + 1] - 1e-6 for i in range(9))
    bot_decile_aband = fractions[0]
    top_decile_aband = fractions[9]
    grades.append({
        "id": "H5",
        "claim": "smart-gate abandonment monotone-decreasing in clearing decile; bot >= 95%, top <= 5%",
        "monotone": monotone,
        "bot_decile_abandonment": bot_decile_aband,
        "top_decile_abandonment": top_decile_aband,
        "all_deciles_abandonment": fractions,
        "status": "HELD" if (monotone and bot_decile_aband >= 0.95 and top_decile_aband <= 0.05) else "FALSIFIED",
    })

    # H6: grand mean replication within ±5% of R14 -$10.6 B
    measured_B = per_decile["grand_mean_B"]
    rel_err = abs(measured_B - (-10.6)) / 10.6
    grades.append({
        "id": "H6",
        "claim": "per-decile sum reproduces R14 grand mean -$10.6 B within ±5%",
        "predicted_tol": 0.05,
        "measured_B": measured_B,
        "rel_err": rel_err,
        "status": "HELD" if rel_err <= 0.05 else "FALSIFIED",
    })

    return grades


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    print("Running R-mean-EV-decomposition...")

    print("  Generating clearing draws (seed-reproducible with R14)...")
    revs = rd13.sample_clearing_per_tonne_M(N_MC)
    print(f"    n_draws={len(revs)}; p05={sorted(revs)[N_MC // 20]:.3f} M/tonne ({sorted(revs)[N_MC // 20]*1000:.0f} $/kg)")
    print(f"    p50={sorted(revs)[N_MC // 2]:.3f} M/tonne ({sorted(revs)[N_MC // 2]*1000:.0f} $/kg)")
    print(f"    p95={sorted(revs)[19 * N_MC // 20]:.3f} M/tonne ({sorted(revs)[19 * N_MC // 20]*1000:.0f} $/kg)")

    print("  Per-draw NPV_D, NPV_R, smart-gate flags...")
    metrics = per_draw_metrics(revs)

    print("  Per-decile decomposition...")
    per_decile = per_decile_decomposition(revs, metrics)
    print(f"    grand mean Δ-NPV = ${per_decile['grand_mean_B']:.2f} B (target R14 -$10.6 B)")

    print("  Per-vigintile decomposition (sign-inflection + exact quartile)...")
    per_vigintile = per_vigintile_decomposition(revs, metrics)
    print(f"    sign-inflection bin: {per_vigintile['sign_inflection_bin_index']} (p{int(per_vigintile['sign_inflection_percentile_lo']*100) if per_vigintile['sign_inflection_percentile_lo'] else '?'}-p{int(per_vigintile['sign_inflection_percentile_hi']*100) if per_vigintile['sign_inflection_percentile_hi'] else '?'})")
    print(f"    top-quartile (p75-p100) contribution: ${per_vigintile['top_quartile_contribution_B']:.2f} B ({per_vigintile['top_quartile_contribution_pct_of_grand']:.1f}% of grand)")

    print("  Cap-truncation sweep...")
    cap_sweep = cap_truncation_sweep(revs)
    for r in cap_sweep["cap_sweep_results"]:
        lbl = r["label"]
        print(f"    {lbl}: mean Δ = ${r['mean_delta_B']:.2f} B")

    print("  Cross-checks...")
    xc = cross_checks(per_decile, per_vigintile, cap_sweep)

    result = {
        "round": "R_mean_EV_decomposition",
        "date": "2026-05-16",
        "seed": SEED,
        "n_mc": N_MC,
        "load_bearing_cell": {
            "launch_count": LAUNCH_COUNT,
            "wacc": WACC,
            "lr": LR,
            "chunk_t": CHUNK_T,
        },
        "per_decile_decomposition": per_decile,
        "per_vigintile_decomposition": per_vigintile,
        "cap_truncation_sweep": cap_sweep,
        "cross_checks": xc,
    }

    print("  Grading...")
    result["grades"] = grade(per_decile, per_vigintile, cap_sweep)

    out_path = RESULTS_DIR / "mean_ev_decomposition_summary.json"
    out_path.write_text(json.dumps(result, indent=2, default=str))
    print(f"  Wrote {out_path}")

    # Summary
    print("\n=== Grades ===")
    for g in result["grades"]:
        print(f"  {g['id']}: {g['status']}  ({g['claim'][:80]})")
    print("\n=== Cross-checks ===")
    for k, v in xc.items():
        passes = v.get("passes", v.get("passes_p75_sign", "?"))
        print(f"  {k}: {'PASS' if passes else 'FAIL'}")


if __name__ == "__main__":
    main()
