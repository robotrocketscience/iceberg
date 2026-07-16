"""Jupiter-return-gravity-assist viability under Saturn-residence-time flexibility.

Tests whether residence-time extension (zero delta-velocity cost; calendar cost
only) materially expands Jupiter-viable fraction. The 0.5-year residence
assumption from Block 4 was arbitrary — accretion fill takes seconds (Finding 5),
so residence is mostly engineering-checkout time. Extending residence shifts
Jupiter-Saturn relative geometry by 18.1°/year, potentially widening the
effective Jupiter-alignment window.
"""

from __future__ import annotations

import csv
import json
from math import atan2, cos, pi, sin, sqrt, acos
from pathlib import Path

# Constants
T_EARTH   = 1.0000
T_JUPITER = 11.8618
T_SATURN  = 29.4571

A_EARTH   = 1.0000
A_JUPITER = 5.2030
A_SATURN  = 9.5549

TAU_ES = 1.0 / (1.0 / T_EARTH - 1.0 / T_SATURN)
T_OUTBOUND = 6.04
T_RESIDENCE_BASE = 0.50          # baseline; extension is on top of this

# Hohmann inbound parameters.
A_HOH = (A_SATURN + A_EARTH) / 2.0
E_HOH = (A_SATURN - A_EARTH) / (A_SATURN + A_EARTH)
P_HOH = A_HOH * (1.0 - E_HOH * E_HOH)
T_HOH = A_HOH ** 1.5

# Jupiter-crossing true-anomaly on Hohmann inbound (computed below).
def _nu_at_radius_descending(r):
    cos_nu = (P_HOH / r - 1.0) / E_HOH
    cos_nu = max(-1.0, min(1.0, cos_nu))
    return 2.0 * pi - acos(cos_nu)

NU_JUP_RAD = _nu_at_radius_descending(A_JUPITER)
NU_JUP_DEG = NU_JUP_RAD * 180.0 / pi

# Time from aphelion to ν via Kepler.
def _t_from_aphelion(nu_rad):
    E_rad = 2.0 * atan2(
        sqrt(1.0 - E_HOH) * sin(nu_rad / 2.0),
        sqrt(1.0 + E_HOH) * cos(nu_rad / 2.0),
    )
    if E_rad < 0.0:
        E_rad += 2.0 * pi
    M_rad = E_rad - E_HOH * sin(E_rad)
    n = 2.0 * pi / T_HOH
    return M_rad / n - T_HOH / 2.0

T_JUP_FROM_EXIT = _t_from_aphelion(NU_JUP_RAD)  # ~4.63 yr

# Round-trip baseline (for mission-duration percent).
T_INBOUND_HALF = T_HOH / 2.0
T_ROUND_TRIP_BASE = T_OUTBOUND + T_RESIDENCE_BASE + T_INBOUND_HALF  # ~12.6 yr

# Sweep parameters.
NUM_LAUNCHES = 58
PHASE_GRID_N = 360
RESIDENCE_GRID = [0.5 + 0.05 * i for i in range(0, 61)]   # 0.50 to 3.50 yr
TOLERANCES_DEG = [2.0, 5.0, 10.0, 15.0]
BUDGETS_YR     = [0.0, 0.25, 0.5, 1.0, 2.0, 3.0]

DELIV_FRAC_WITH_JUPITER    = 0.218
DELIV_FRAC_WITHOUT_JUPITER = 0.155

OUT = Path(__file__).parent / "results"
OUT.mkdir(parents=True, exist_ok=True)


def wrap360(d):
    d %= 360.0
    return d + 360.0 if d < 0.0 else d


def signed_diff_deg(a, b):
    d = (a - b) % 360.0
    return d - 360.0 if d > 180.0 else d


def viable_at_launch(n, tol_deg, budget_yr, theta0_jup_deg):
    """Returns (viable_bool, min_extension_yr_for_viability)."""
    t_launch = n * TAU_ES
    min_ext = None
    res_max = T_RESIDENCE_BASE + budget_yr
    for tau in RESIDENCE_GRID:
        if tau > res_max + 1e-9:
            break
        t_exit = t_launch + T_OUTBOUND + tau
        t_cross = t_exit + T_JUP_FROM_EXIT
        theta_saturn_at_exit = wrap360(360.0 * t_exit / T_SATURN)
        theta_perihelion = wrap360(theta_saturn_at_exit + 180.0)
        theta_chunk = wrap360(theta_perihelion + NU_JUP_DEG)
        theta_jupiter = wrap360(theta0_jup_deg + 360.0 * t_cross / T_JUPITER)
        sep = abs(signed_diff_deg(theta_chunk, theta_jupiter))
        if sep <= tol_deg:
            ext = tau - T_RESIDENCE_BASE
            if min_ext is None or ext < min_ext:
                min_ext = ext
    return (min_ext is not None, min_ext)


# H1: phase-shift per residence-year. Saturn moves 360/T_SATURN deg/yr; Jupiter
# at the chunk's Jupiter-crossing time. Extending residence by Δτ shifts:
#   theta_saturn_at_exit by 360/T_SATURN * Δτ
#   theta_chunk by the same amount (chunk crosses 4.63 yr later, regardless of τ)
#   theta_jupiter at t_cross by 360/T_JUPITER * Δτ
# Separation shift per Δτ year = (360/T_SATURN - 360/T_JUPITER)
phase_shift_per_year = 360.0 / T_SATURN - 360.0 / T_JUPITER
phase_shift_per_year_abs = abs(phase_shift_per_year)

# Phase-averaged viable-fraction and duration-impact grid.
PHASE_GRID = [i * 360.0 / PHASE_GRID_N for i in range(PHASE_GRID_N)]

grid_rows = []
for tol in TOLERANCES_DEG:
    for budget in BUDGETS_YR:
        fracs = []
        ext_means = []
        for theta0 in PHASE_GRID:
            viable_count = 0
            ext_sum = 0.0
            for n in range(NUM_LAUNCHES):
                v, ext = viable_at_launch(n, tol, budget, theta0)
                if v:
                    viable_count += 1
                    ext_sum += ext
            frac = viable_count / NUM_LAUNCHES
            mean_ext = (ext_sum / viable_count) if viable_count > 0 else 0.0
            fracs.append(frac)
            ext_means.append(mean_ext)
        mean_frac = sum(fracs) / len(fracs)
        mean_ext_overall = sum(ext_means) / len(ext_means)
        deliv = mean_frac * DELIV_FRAC_WITH_JUPITER + (1 - mean_frac) * DELIV_FRAC_WITHOUT_JUPITER
        duration_pct = 100.0 * mean_ext_overall / T_ROUND_TRIP_BASE
        grid_rows.append({
            "tolerance_deg": tol,
            "budget_yr": budget,
            "viable_fraction": mean_frac,
            "campaign_mean_deliv_frac": deliv,
            "mean_extension_per_viable_yr": mean_ext_overall,
            "duration_impact_pct": duration_pct,
        })

with open(OUT / "viable_fraction_grid.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(grid_rows[0].keys()))
    w.writeheader()
    w.writerows(grid_rows)

with open(OUT / "campaign_mean_grid.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["tolerance_deg", "budget_yr",
                                       "viable_fraction", "campaign_mean_deliv_frac"],
                       extrasaction="ignore")
    w.writeheader()
    w.writerows(grid_rows)

with open(OUT / "duration_impact.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["tolerance_deg", "budget_yr",
                                       "mean_extension_per_viable_yr",
                                       "duration_impact_pct"],
                       extrasaction="ignore")
    w.writeheader()
    w.writerows(grid_rows)

# Per-window record at Jupiter initial phase = 0.
per_window = []
for n in range(NUM_LAUNCHES):
    row = {"n": n, "t_launch_yr": n * TAU_ES}
    for tol in TOLERANCES_DEG:
        v, ext = viable_at_launch(n, tol, 3.0, 0.0)  # max budget 3 yr at phase 0
        row[f"viable_tol{int(tol)}"] = int(v)
        row[f"min_extension_tol{int(tol)}_yr"] = ext if ext is not None else float("nan")
    per_window.append(row)

with open(OUT / "per_window_min_extension.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(per_window[0].keys()))
    w.writeheader()
    w.writerows(per_window)

# Hypothesis adjudication.
H1_status = "held" if 15.0 <= phase_shift_per_year_abs <= 22.0 else (
    "falsified_low" if phase_shift_per_year_abs < 15.0
    else "falsified_high")

viable_5_1 = next(r["viable_fraction"] for r in grid_rows
                  if r["tolerance_deg"] == 5.0 and r["budget_yr"] == 1.0)
H2_status = "held" if 0.30 <= viable_5_1 <= 0.55 else (
    "falsified_low" if viable_5_1 < 0.20
    else "falsified_high" if viable_5_1 > 0.55
    else "marginal")

viable_5_3 = next(r["viable_fraction"] for r in grid_rows
                  if r["tolerance_deg"] == 5.0 and r["budget_yr"] == 3.0)
H3_status = "held" if 0.50 <= viable_5_3 <= 0.85 else (
    "falsified_low" if viable_5_3 < 0.50
    else "falsified_high")

deliv_5_1 = next(r["campaign_mean_deliv_frac"] for r in grid_rows
                  if r["tolerance_deg"] == 5.0 and r["budget_yr"] == 1.0)
H4_status = "held" if 0.18 <= deliv_5_1 <= 0.21 else (
    "falsified_low" if deliv_5_1 < 0.17
    else "falsified_high" if deliv_5_1 > 0.22
    else "marginal")

dur_5_1 = next(r["duration_impact_pct"] for r in grid_rows
                if r["tolerance_deg"] == 5.0 and r["budget_yr"] == 1.0)
H5_status = "held" if 2.0 <= dur_5_1 <= 6.0 else (
    "falsified_low" if dur_5_1 < 2.0
    else "falsified_high")

# Block 5 reproduction: viable fraction at ±5°, budget = 0.
block5_repro = next(r["viable_fraction"] for r in grid_rows
                    if r["tolerance_deg"] == 5.0 and r["budget_yr"] == 0.0)

summary = {
    "model": {
        "num_launches": NUM_LAUNCHES,
        "tolerances_deg": TOLERANCES_DEG,
        "budgets_yr": BUDGETS_YR,
        "residence_grid_resolution_yr": 0.05,
        "t_round_trip_base_yr": T_ROUND_TRIP_BASE,
    },
    "phase_shift_per_year_deg": phase_shift_per_year_abs,
    "block5_reproduction": {
        "viable_fraction_5deg_budget_0yr": block5_repro,
        "block5_expected": 0.0278,
        "matches": abs(block5_repro - 0.0278) < 0.005,
    },
    "headline_results": {
        "viable_fraction_5deg_by_budget_yr": {
            f"{r['budget_yr']:.2f}": r["viable_fraction"]
            for r in grid_rows if r["tolerance_deg"] == 5.0
        },
        "campaign_mean_deliv_5deg_by_budget_yr": {
            f"{r['budget_yr']:.2f}": r["campaign_mean_deliv_frac"]
            for r in grid_rows if r["tolerance_deg"] == 5.0
        },
        "duration_impact_pct_5deg_by_budget_yr": {
            f"{r['budget_yr']:.2f}": r["duration_impact_pct"]
            for r in grid_rows if r["tolerance_deg"] == 5.0
        },
    },
    "hypothesis_adjudication": {
        "H1_phase_shift_per_year_in_15_22deg": {
            "status": H1_status, "observed_deg": phase_shift_per_year_abs
        },
        "H2_viable_fraction_5deg_1yr_ge_0p30": {
            "status": H2_status, "observed": viable_5_1
        },
        "H3_viable_fraction_5deg_3yr_in_0p5_to_0p85": {
            "status": H3_status, "observed": viable_5_3
        },
        "H4_campaign_mean_5deg_1yr_in_0p18_0p21": {
            "status": H4_status, "observed": deliv_5_1
        },
        "H5_duration_impact_5deg_1yr_in_2_6pct": {
            "status": H5_status, "observed_pct": dur_5_1
        },
    },
}

with open(OUT / "summary.json", "w") as f:
    json.dump(summary, f, indent=2, default=str)

# Console summary
print("=" * 72)
print("R-residence-time-flexibility — results")
print("=" * 72)
print(f"Saturn-Jupiter relative phase shift per residence-year: "
      f"{phase_shift_per_year_abs:.3f}° / yr")
print(f"Round-trip baseline mission duration: {T_ROUND_TRIP_BASE:.2f} yr")
print()
print(f"Block-5 reproduction (budget = 0, ±5°): {block5_repro*100:.2f}%  "
      f"(expected 2.78%)")
print()
print("Viable fraction grid (phase-averaged):")
hdr = "  " + " " * 5
for budget in BUDGETS_YR:
    hdr += f"  bgt {budget:.2f}yr"
print(hdr)
for tol in TOLERANCES_DEG:
    row_str = f"  ±{tol:>3.0f}°"
    for budget in BUDGETS_YR:
        v = next(r["viable_fraction"] for r in grid_rows
                 if r["tolerance_deg"] == tol and r["budget_yr"] == budget)
        row_str += f"   {v*100:>7.2f}%"
    print(row_str)
print()
print("Campaign-mean delivered fraction:")
for tol in TOLERANCES_DEG:
    row_str = f"  ±{tol:>3.0f}°"
    for budget in BUDGETS_YR:
        v = next(r["campaign_mean_deliv_frac"] for r in grid_rows
                 if r["tolerance_deg"] == tol and r["budget_yr"] == budget)
        row_str += f"   {v*100:>7.2f}%"
    print(row_str)
print()
print("Duration-impact (% of 12.6-yr round trip):")
for tol in TOLERANCES_DEG:
    row_str = f"  ±{tol:>3.0f}°"
    for budget in BUDGETS_YR:
        v = next(r["duration_impact_pct"] for r in grid_rows
                 if r["tolerance_deg"] == tol and r["budget_yr"] == budget)
        row_str += f"   {v:>7.2f}%"
    print(row_str)
print()
print("Hypothesis adjudication:")
for hname, hdata in summary["hypothesis_adjudication"].items():
    print(f"  {hname}: {hdata['status']}")
