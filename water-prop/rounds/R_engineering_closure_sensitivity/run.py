"""
R-engineering-closure-sensitivity — what (P_HYBRID, P_RENDEZVOUS) compound is
required to flip H6 from the prior three iapetus rounds?

Sweeps engineering-closure priors over plausible ranges at each base-rate ×
window combination from the prior rounds. Finds breakeven curves and reports
whether plausible engineering priors can lift conjunction above any non-
technology-demonstrator threshold.

Author: iapetus, 2026-05-15 (latest+9)
Pre-registration: SCOPE.md (H1-H5)
"""

from __future__ import annotations

import json
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
# Conditional priors held fixed (from R-reactor-specific-power-program-targets)
# ---------------------------------------------------------------------------

SP_PRIOR = {float(k): v for k, v in PRIOR_TARGETS["subjective_priors"]["p_sp_geq_given_orbit_500kWe"].items()}
L_PRIOR_RAW = PRIOR_TARGETS["subjective_priors"]["p_L_geq_given_orbit_500kWe"]
L_PRIOR = {float("inf") if k == "inf" else float(k): v for k, v in L_PRIOR_RAW.items()}
X_PRIOR = {float(k): v for k, v in PRIOR_TARGETS["subjective_priors"]["p_X_geq_given_hybrid_closes"].items()}
MIN_CORNERS = PRIOR_TARGETS["min_corner_table"]

# ---------------------------------------------------------------------------
# Base-rate × window p_500_orbit posteriors (from prior rounds)
# ---------------------------------------------------------------------------

# Pull p_500_by_year from each base-rate model.
# US-only (uniform Beta(1,1)) — from R-demonstrator-window-sensitivity (since that
# round re-derived with the same MC machinery; use its values for consistency).
us_p_500 = PRIOR_WINDOW["p_500kWe_orbit_by_window_and_prior"]["uniform_beta_1_1"]
# Global (uniform Beta(1,1), scope=0.40) — from R-global-vs-US-base-rate global_table
global_table = PRIOR_GLOBAL["global_table"]
global_p_500 = {str(r["window_year"]): r["uniform_beta_1_1_p_500"] for r in global_table}

# ---------------------------------------------------------------------------
# Sweep parameters
# ---------------------------------------------------------------------------

P_HYBRID_SWEEP = [0.10, 0.30, 0.50, 0.70, 0.90, 1.00]
P_RENDEZVOUS_SWEEP = [0.10, 0.20, 0.30, 0.50, 0.70, 0.90, 1.00]
WINDOW_YEARS_SWEPT = ["2035", "2045", "2055", "ever"]

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


def conjunction_at_corner(corner: dict, p_500_orbit: float, p_hybrid: float, p_rendezvous: float) -> float:
    sp = corner["min_sp_w_per_kg"]
    X = corner["X_km_s"]
    L_yr = corner["L_yr"]
    L_key = float("inf") if L_yr == "inf" else float(L_yr)
    p_sp = SP_PRIOR[sp]
    p_L = L_PRIOR[L_key]
    p_aero = (p_hybrid * X_PRIOR[X]) if X > 0 else 1.0
    return p_500_orbit * p_sp * p_L * p_aero * p_rendezvous


def max_conjunction(p_500_orbit: float, p_hybrid: float, p_rendezvous: float, x_floor: float = 0.0) -> tuple[float, dict | None]:
    best_p, best_c = 0.0, None
    for c in MIN_CORNERS:
        if c["X_km_s"] < x_floor:
            continue
        p = conjunction_at_corner(c, p_500_orbit, p_hybrid, p_rendezvous)
        if p > best_p:
            best_p = p
            best_c = c
    return best_p, best_c


# ---------------------------------------------------------------------------
# Heatmap: (base-rate × window) → 2D grid of (P_HYBRID × P_RENDEZVOUS) → conjunction
# ---------------------------------------------------------------------------

heatmaps: dict[str, dict] = {}
for base_rate_label, p_500_by_year in (("us_only_uniform", us_p_500), ("global_uniform", global_p_500)):
    heatmaps[base_rate_label] = {}
    for window_year in WINDOW_YEARS_SWEPT:
        p_500_orbit = p_500_by_year[window_year]
        grid = []
        for p_h in P_HYBRID_SWEEP:
            row = {"p_hybrid": p_h, "cells": []}
            for p_r in P_RENDEZVOUS_SWEEP:
                max_p, max_c = max_conjunction(p_500_orbit, p_h, p_r)
                row["cells"].append({
                    "p_rendezvous": p_r,
                    "max_conjunction": max_p,
                    "capital_class": capital_class(max_p),
                })
            grid.append(row)
        heatmaps[base_rate_label][window_year] = {
            "p_500_orbit": p_500_orbit,
            "grid": grid,
        }

# ---------------------------------------------------------------------------
# Breakeven curve search: for each (base-rate × window × threshold), find the
# minimum (P_HYBRID × P_RENDEZVOUS) compound where the threshold is crossed.
# ---------------------------------------------------------------------------

THRESHOLDS = {
    "venture": 0.10,
    "corp_growth": 0.30,
    "regulated_utility": 0.50,
    "sovereign_bond": 0.80,
}


def find_minimum_compound(base_rate: str, window: str, threshold: float) -> dict:
    """Find the minimum P_HYBRID × P_RENDEZVOUS compound that crosses threshold."""
    p_500_orbit = heatmaps[base_rate][window]["p_500_orbit"]
    crossing_points = []
    for p_h in P_HYBRID_SWEEP:
        for p_r in P_RENDEZVOUS_SWEEP:
            max_p, _ = max_conjunction(p_500_orbit, p_h, p_r)
            if max_p >= threshold:
                crossing_points.append({
                    "p_hybrid": p_h,
                    "p_rendezvous": p_r,
                    "compound": p_h * p_r,
                    "max_conjunction": max_p,
                })
    if not crossing_points:
        return {"crossable_in_sweep": False, "min_compound": None}
    crossing_points.sort(key=lambda c: c["compound"])
    return {
        "crossable_in_sweep": True,
        "min_compound": crossing_points[0]["compound"],
        "min_p_hybrid": crossing_points[0]["p_hybrid"],
        "min_p_rendezvous": crossing_points[0]["p_rendezvous"],
        "n_crossing_points": len(crossing_points),
    }


breakevens = {}
for base_rate in ("us_only_uniform", "global_uniform"):
    breakevens[base_rate] = {}
    for window in WINDOW_YEARS_SWEPT:
        breakevens[base_rate][window] = {}
        for thresh_name, thresh_value in THRESHOLDS.items():
            breakevens[base_rate][window][thresh_name] = find_minimum_compound(base_rate, window, thresh_value)


# ---------------------------------------------------------------------------
# X=0 corner-restricted variant (H4): aerocapture-credit not in chain → only P_RENDEZVOUS matters
# ---------------------------------------------------------------------------

def find_minimum_p_r_at_x0(base_rate: str, window: str, threshold: float) -> dict:
    """At X=0 corner, P_HYBRID is unused. Find min P_RENDEZVOUS to cross threshold."""
    p_500_orbit = heatmaps[base_rate][window]["p_500_orbit"]
    crossing_points = []
    for p_r in P_RENDEZVOUS_SWEEP:
        # X=0 corner sweep — find best X=0 corner, then test threshold
        max_p, max_c = max_conjunction(p_500_orbit, 1.0, p_r, x_floor=0.0)  # x_floor 0 includes X=0
        # Restrict to X=0 only
        best_p = 0.0
        for c in MIN_CORNERS:
            if c["X_km_s"] != 0.0:
                continue
            p = conjunction_at_corner(c, p_500_orbit, 1.0, p_r)
            if p > best_p:
                best_p = p
        if best_p >= threshold:
            crossing_points.append({"p_rendezvous": p_r, "max_conjunction": best_p})
    if not crossing_points:
        return {"crossable_in_sweep": False, "min_p_r": None}
    crossing_points.sort(key=lambda c: c["p_rendezvous"])
    return {"crossable_in_sweep": True, "min_p_r": crossing_points[0]["p_rendezvous"]}


x0_breakevens = {}
for base_rate in ("us_only_uniform", "global_uniform"):
    x0_breakevens[base_rate] = {}
    for window in WINDOW_YEARS_SWEPT:
        x0_breakevens[base_rate][window] = {}
        for thresh_name, thresh_value in THRESHOLDS.items():
            x0_breakevens[base_rate][window][thresh_name] = find_minimum_p_r_at_x0(base_rate, window, thresh_value)


# ---------------------------------------------------------------------------
# Hypotheses adjudication
# ---------------------------------------------------------------------------

# H1: under US-only baseline at 2035, venture compound breakeven ≥ 0.95
h1_compound = breakevens["us_only_uniform"]["2035"]["venture"]
h1_holds = (not h1_compound["crossable_in_sweep"]) or (h1_compound.get("min_compound", 0) >= 0.95)
h1_verdict = "CONFIRMED" if h1_holds else "FALSIFIED"

# H2: under global+ever, venture compound breakeven ≥ 0.30
h2_compound = breakevens["global_uniform"]["ever"]["venture"]
h2_holds = (not h2_compound["crossable_in_sweep"]) or (h2_compound.get("min_compound", 0) >= 0.30)
h2_verdict = "CONFIRMED" if h2_holds else "FALSIFIED"

# H3: under global+ever, corp-growth (30%) unreachable even at perfect engineering closure (compound ≤ 1.0)
h3_compound = breakevens["global_uniform"]["ever"]["corp_growth"]
h3_holds = not h3_compound["crossable_in_sweep"]
h3_verdict = "CONFIRMED" if h3_holds else "FALSIFIED"

# H4: X=0 corner venture-breakeven P_RENDEZVOUS = unreachable
h4_x0 = x0_breakevens["global_uniform"]["ever"]["venture"]
h4_holds = not h4_x0["crossable_in_sweep"]
h4_verdict = "CONFIRMED" if h4_holds else "FALSIFIED"

# H5: engineering-prior lift bounded — max lift from (0.5×0.3=0.15) to (1.0×1.0=1.0) is 6.67×
us_2035_at_baseline = max_conjunction(us_p_500["2035"], 0.5, 0.3)[0]
us_2035_at_max = max_conjunction(us_p_500["2035"], 1.0, 1.0)[0]
h5_lift = us_2035_at_max / us_2035_at_baseline if us_2035_at_baseline > 0 else None
h5_holds = h5_lift is not None and h5_lift <= 10.0
h5_verdict = "CONFIRMED" if h5_holds else "FALSIFIED"


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

out = {
    "round": "R-engineering-closure-sensitivity",
    "author": "iapetus",
    "date": "2026-05-15",
    "pre_registration": "SCOPE.md (H1-H5)",
    "p_hybrid_sweep": P_HYBRID_SWEEP,
    "p_rendezvous_sweep": P_RENDEZVOUS_SWEEP,
    "window_years_swept": WINDOW_YEARS_SWEPT,
    "p_500_orbit_anchors": {
        "us_only_uniform_by_window": us_p_500,
        "global_uniform_by_window": global_p_500,
    },
    "heatmaps": heatmaps,
    "breakevens_by_base_rate_window_threshold": breakevens,
    "x0_corner_only_breakevens": x0_breakevens,
    "engineering_prior_lift_baseline_to_max": {
        "baseline_value_us_2035": us_2035_at_baseline,
        "max_value_us_2035": us_2035_at_max,
        "lift_factor": h5_lift,
    },
    "hypotheses": {
        "H1": {
            "hypothesis": "Under US-only + 2035, venture compound breakeven ≥ 0.95",
            "min_compound": h1_compound,
            "verdict": h1_verdict,
        },
        "H2": {
            "hypothesis": "Under global + ever-50yr, venture compound breakeven ≥ 0.30",
            "min_compound": h2_compound,
            "verdict": h2_verdict,
        },
        "H3": {
            "hypothesis": "Under global + ever-50yr, corp-growth (30%) unreachable at compound ≤ 1.0",
            "compound_data": h3_compound,
            "verdict": h3_verdict,
        },
        "H4": {
            "hypothesis": "X=0 corner: venture unreachable at any P_RENDEZVOUS ≤ 1.0 under global+ever",
            "x0_data": h4_x0,
            "verdict": h4_verdict,
        },
        "H5": {
            "hypothesis": "Engineering-prior lift from baseline to max < 10×",
            "lift_factor": h5_lift,
            "verdict": h5_verdict,
        },
    },
}

out_path = RESULTS_DIR / "engineering_closure_sensitivity.json"
out_path.write_text(json.dumps(out, indent=2))


# ---------------------------------------------------------------------------
# Console summary
# ---------------------------------------------------------------------------

print(f"Wrote {out_path}")
print()
print("=== Breakeven (min P_HYBRID × P_RENDEZVOUS compound) per (base-rate, window, threshold) ===")
print(f"  {'base-rate':>20} {'window':>6} {'threshold':>16} {'min compound':>14} {'crossable':>10}")
for base_rate, by_window in breakevens.items():
    for window, by_thresh in by_window.items():
        for thresh_name, info in by_thresh.items():
            comp = info.get("min_compound", "n/a")
            comp_s = f"{comp:.3f}" if isinstance(comp, float) else str(comp)
            print(f"  {base_rate:>20} {window:>6} {thresh_name:>16} {comp_s:>14} {str(info['crossable_in_sweep']):>10}")
print()
print("=== Heatmap: max conjunction under global+ever (rendezvous_hi values shown across P_RENDEZVOUS axis) ===")
print(f"  {'P_HYBRID':>10}  " + "  ".join(f"{p_r:>10.2f}" for p_r in P_RENDEZVOUS_SWEEP))
for row in heatmaps["global_uniform"]["ever"]["grid"]:
    p_h = row["p_hybrid"]
    cells = row["cells"]
    line = f"  {p_h:>10.2f}  " + "  ".join(f"{c['max_conjunction']:>10.4%}" for c in cells)
    print(line)
print()
print("=== Capital-class assignment under global+ever, P_HYBRID × P_RENDEZVOUS sweep ===")
print(f"  {'P_HYBRID':>10}  " + "  ".join(f"{p_r:>14.2f}" for p_r in P_RENDEZVOUS_SWEEP))
for row in heatmaps["global_uniform"]["ever"]["grid"]:
    p_h = row["p_hybrid"]
    cells = row["cells"]
    line = f"  {p_h:>10.2f}  " + "  ".join(f"{c['capital_class'][:14]:>14}" for c in cells)
    print(line)
print()
print("=== Hypotheses verdicts ===")
for h, v in out["hypotheses"].items():
    print(f"  {h}: {v['verdict']}")
