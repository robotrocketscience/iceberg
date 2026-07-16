"""Jupiter-return-gravity-assist viability under Saturn-exit-delta-velocity flexibility.

Questions Block 5's pessimistic conclusion (2.78% Jupiter-viable at ±5°) by
adding a trajectory degree of freedom: vary the chunk's heliocentric ellipse by
changing the Saturn-exit retrograde delta-velocity, which changes the perihelion
distance and therefore the time-of-flight to Jupiter's orbital radius. The
line-of-apsides direction stays fixed (tangential Saturn-exit burn), so
Jupiter-crossing *longitude* is unchanged from the Hohmann case, but the
*crossing time* varies, sliding Jupiter into or out of position.

Output verifies whether Saturn-exit-flexibility materially expands the
Jupiter-viable launch-window fraction.
"""

from __future__ import annotations

import csv
import json
from math import atan2, cos, pi, sin, sqrt, acos
from pathlib import Path

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------

T_EARTH   = 1.0000
T_JUPITER = 11.8618
T_SATURN  = 29.4571

A_EARTH   = 1.0000
A_JUPITER = 5.2030
A_SATURN  = 9.5549

TAU_ES = 1.0 / (1.0 / T_EARTH - 1.0 / T_SATURN)  # ≈ 1.0352 yr

T_OUTBOUND  = 6.04
T_RESIDENCE = 0.50

# Kepler-units conversion: 1 AU/yr = 4.7404 km/s.
KM_PER_AU = 1.495978707e8
SEC_PER_YR = 3.15576e7
AU_PER_YR_TO_KMS = KM_PER_AU / SEC_PER_YR

# Perihelion grid for the trajectory family.
PERIHELION_GRID_AU = [0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.00]

# Tolerance and budget sweeps.
TOLERANCES_DEG = [2.0, 5.0, 10.0, 15.0]
BUDGETS_KMS    = [0.0, 0.25, 0.50, 1.00, 1.50, 2.00]

NUM_LAUNCHES = 58       # 60-yr span
PHASE_GRID_N = 360      # 1° resolution for ensemble averaging

# Composite delivered fractions from Block 4 / Block 5.
DELIV_FRAC_WITH_JUPITER    = 0.218
DELIV_FRAC_WITHOUT_JUPITER = 0.155

OUT = Path(__file__).parent / "results"
OUT.mkdir(parents=True, exist_ok=True)

# -----------------------------------------------------------------------------
# Utilities
# -----------------------------------------------------------------------------

def wrap360(deg: float) -> float:
    d = deg % 360.0
    if d < 0.0:
        d += 360.0
    return d


def signed_diff_deg(a: float, b: float) -> float:
    d = (a - b) % 360.0
    if d > 180.0:
        d -= 360.0
    return d


# -----------------------------------------------------------------------------
# Trajectory family: per-perihelion geometry
# -----------------------------------------------------------------------------

V_SATURN_HELIO = 2.0 * pi * A_SATURN / T_SATURN  # AU/yr at Saturn's circular orbit
V_SATURN_HELIO_KMS = V_SATURN_HELIO * AU_PER_YR_TO_KMS

def ellipse_params(perihelion_au: float) -> dict:
    """Compute heliocentric ellipse parameters for a chunk leaving Saturn
    tangentially-retrograde to a perihelion at perihelion_au, with aphelion at
    A_SATURN."""
    aphelion = A_SATURN
    a = (perihelion_au + aphelion) / 2.0
    e = (aphelion - perihelion_au) / (aphelion + perihelion_au)
    p = a * (1.0 - e * e)
    period_yr = a ** 1.5

    # Heliocentric speed at Saturn aphelion: v² = μ(2/r - 1/a); μ = 4π² in
    # AU³/yr² (Kepler units).
    v_at_aphelion = 2.0 * pi * sqrt(2.0 / aphelion - 1.0 / a)   # AU/yr

    # Saturn-exit retrograde delta-velocity (chunk slows from V_SATURN_HELIO to
    # v_at_aphelion in the retrograde direction).
    dv_saturn_exit = V_SATURN_HELIO - v_at_aphelion   # AU/yr (positive)
    dv_saturn_exit_kms = dv_saturn_exit * AU_PER_YR_TO_KMS

    # True anomaly at radius A_JUPITER on the descending leg.
    # r = p / (1 + e cos ν)  → cos ν = (p/r - 1) / e
    cos_nu = (p / A_JUPITER - 1.0) / e
    cos_nu = max(-1.0, min(1.0, cos_nu))
    nu_asc_rad = acos(cos_nu)
    nu_desc_rad = 2.0 * pi - nu_asc_rad
    nu_desc_deg = nu_desc_rad * 180.0 / pi

    # Time from aphelion to ν_desc via Kepler's equation.
    E_rad = 2.0 * atan2(
        sqrt(1.0 - e) * sin(nu_desc_rad / 2.0),
        sqrt(1.0 + e) * cos(nu_desc_rad / 2.0),
    )
    if E_rad < 0.0:
        E_rad += 2.0 * pi
    M_rad = E_rad - e * sin(E_rad)
    n_motion = 2.0 * pi / period_yr
    t_from_perihelion = M_rad / n_motion
    t_from_aphelion = t_from_perihelion - period_yr / 2.0

    return {
        "perihelion_au": perihelion_au,
        "a_au": a,
        "e": e,
        "period_yr": period_yr,
        "v_at_saturn_kms": v_at_aphelion * AU_PER_YR_TO_KMS,
        "dv_saturn_exit_kms": dv_saturn_exit_kms,
        "nu_jup_crossing_deg": nu_desc_deg,
        "t_aphelion_to_jup_yr": t_from_aphelion,
    }


# Compute trajectory family table.
family = [ellipse_params(rp) for rp in PERIHELION_GRID_AU]
hohmann = family[-1]  # perihelion = 1.0 AU
DV_HOHMANN = hohmann["dv_saturn_exit_kms"]

for row in family:
    row["dv_premium_kms"] = row["dv_saturn_exit_kms"] - DV_HOHMANN

with open(OUT / "trajectory_family.csv", "w", newline="") as f:
    fieldnames = list(family[0].keys())
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    w.writerows(family)

# H1 check: crossing longitude variance across perihelion grid.
# Chunk at true anomaly ν is at heliocentric longitude θ_perihelion + ν, where
# θ_perihelion = θ_saturn_at_exit + 180° (perihelion is at antipode of
# Saturn-exit aphelion). So crossing longitude = θ_saturn_at_exit + 180° + ν.
# Variance is just variance of ν across perihelion grid.
crossing_nu_range_deg = max(r["nu_jup_crossing_deg"] for r in family) - min(r["nu_jup_crossing_deg"] for r in family)

# H2 check: crossing time-of-flight range.
t_jup_range = (max(r["t_aphelion_to_jup_yr"] for r in family)
               - min(r["t_aphelion_to_jup_yr"] for r in family))

# H3 check: maximum delta-velocity premium.
dv_premium_max = max(r["dv_premium_kms"] for r in family)

# -----------------------------------------------------------------------------
# Per-launch sweep over the perihelion grid
# -----------------------------------------------------------------------------

def viable_fraction(theta0_jup_deg: float, tol_deg: float, budget_kms: float) -> float:
    """Fraction of NUM_LAUNCHES launches where at least one perihelion in the
    grid achieves Jupiter alignment within tolerance AND Saturn-exit-premium
    within budget."""
    count = 0
    for n in range(NUM_LAUNCHES):
        t_launch = n * TAU_ES
        t_exit = t_launch + T_OUTBOUND + T_RESIDENCE
        theta_saturn_at_exit = wrap360(360.0 * t_exit / T_SATURN)
        theta_perihelion = wrap360(theta_saturn_at_exit + 180.0)

        any_viable = False
        for row in family:
            if row["dv_premium_kms"] > budget_kms:
                continue
            theta_chunk = wrap360(theta_perihelion + row["nu_jup_crossing_deg"])
            t_cross = t_exit + row["t_aphelion_to_jup_yr"]
            theta_jupiter = wrap360(theta0_jup_deg + 360.0 * t_cross / T_JUPITER)
            sep = abs(signed_diff_deg(theta_chunk, theta_jupiter))
            if sep <= tol_deg:
                any_viable = True
                break
        if any_viable:
            count += 1
    return count / NUM_LAUNCHES if NUM_LAUNCHES else 0.0


# Phase grid for ensemble averaging.
PHASE_GRID = [i * (360.0 / PHASE_GRID_N) for i in range(PHASE_GRID_N)]

# Compute (tolerance, budget) grid of phase-averaged viable fractions.
grid_rows = []
for tol in TOLERANCES_DEG:
    for budget in BUDGETS_KMS:
        fracs = [viable_fraction(p, tol, budget) for p in PHASE_GRID]
        mean_frac = sum(fracs) / len(fracs)
        # Campaign-mean delivered fraction at this (tol, budget):
        # viable windows get Jupiter, non-viable get no-Jupiter composite.
        deliv_frac = (mean_frac * DELIV_FRAC_WITH_JUPITER
                      + (1.0 - mean_frac) * DELIV_FRAC_WITHOUT_JUPITER)
        grid_rows.append({
            "tolerance_deg": tol,
            "budget_kms": budget,
            "viable_fraction": mean_frac,
            "campaign_mean_deliv_frac": deliv_frac,
        })

with open(OUT / "viable_fraction_grid.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(grid_rows[0].keys()))
    w.writeheader()
    w.writerows(grid_rows)

# Also write a separate campaign-mean-grid file for convenience.
with open(OUT / "campaign_mean_grid.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["tolerance_deg", "budget_kms",
                                       "viable_fraction", "campaign_mean_deliv_frac"])
    w.writeheader()
    w.writerows(grid_rows)

# -----------------------------------------------------------------------------
# Per-window minimum-cost record (for one realistic initial Jupiter phase = 0)
# -----------------------------------------------------------------------------

theta0_for_record = 0.0
per_window = []
for n in range(NUM_LAUNCHES):
    t_launch = n * TAU_ES
    t_exit = t_launch + T_OUTBOUND + T_RESIDENCE
    theta_saturn_at_exit = wrap360(360.0 * t_exit / T_SATURN)
    theta_perihelion = wrap360(theta_saturn_at_exit + 180.0)

    best_per_tol = {}
    for tol in TOLERANCES_DEG:
        min_premium = None
        best_perihelion = None
        for row in family:
            theta_chunk = wrap360(theta_perihelion + row["nu_jup_crossing_deg"])
            t_cross = t_exit + row["t_aphelion_to_jup_yr"]
            theta_jupiter = wrap360(theta0_for_record + 360.0 * t_cross / T_JUPITER)
            sep = abs(signed_diff_deg(theta_chunk, theta_jupiter))
            if sep <= tol:
                if min_premium is None or row["dv_premium_kms"] < min_premium:
                    min_premium = row["dv_premium_kms"]
                    best_perihelion = row["perihelion_au"]
        best_per_tol[f"min_premium_kms_tol{int(tol)}"] = (
            min_premium if min_premium is not None else float("inf")
        )
        best_per_tol[f"best_perihelion_tol{int(tol)}"] = (
            best_perihelion if best_perihelion is not None else float("nan")
        )

    per_window.append({
        "n": n,
        "t_launch_yr": t_launch,
        "t_exit_yr": t_exit,
        **best_per_tol,
    })

with open(OUT / "per_window_min_cost.csv", "w", newline="") as f:
    fieldnames = list(per_window[0].keys())
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    w.writerows(per_window)

# -----------------------------------------------------------------------------
# Hypothesis adjudication
# -----------------------------------------------------------------------------

# H1: crossing-longitude variance < 5°.
# Crossing longitude = θ_perihelion_dir + ν, and θ_perihelion_dir is fixed for
# fixed Saturn-exit position. So crossing-longitude variation = ν variation.
H1_status = "held" if crossing_nu_range_deg < 5.0 else "falsified"

# H2: crossing time-of-flight range ≥ 1.5 yr.
H2_status = (
    "held" if t_jup_range >= 1.5
    else "falsified_low" if t_jup_range < 1.0
    else "ambiguous"
)

# H3: max premium < 1.0 km/s.
H3_status = "held" if dv_premium_max < 1.0 else (
    "falsified_high" if dv_premium_max > 1.5 else "marginal"
)

# H4: combined fraction at ±5° and ≤ 1 km/s ≥ 0.20.
viable_5_1 = next(r["viable_fraction"] for r in grid_rows
                  if r["tolerance_deg"] == 5.0 and r["budget_kms"] == 1.0)
H4_status = "held" if 0.20 <= viable_5_1 <= 0.50 else (
    "falsified_low" if viable_5_1 < 0.15
    else "falsified_high" if viable_5_1 > 0.50 else "marginal")

# H5: campaign-mean at ±5° and ≤ 1 km/s ∈ [0.17, 0.20].
deliv_5_1 = next(r["campaign_mean_deliv_frac"] for r in grid_rows
                  if r["tolerance_deg"] == 5.0 and r["budget_kms"] == 1.0)
H5_status = "held" if 0.17 <= deliv_5_1 <= 0.20 else (
    "falsified_low" if deliv_5_1 < 0.16
    else "falsified_high" if deliv_5_1 > 0.21 else "marginal")

# Block 5 reproduction check: viable fraction at ±5°, budget = 0.
block5_repro = next(r["viable_fraction"] for r in grid_rows
                    if r["tolerance_deg"] == 5.0 and r["budget_kms"] == 0.0)
# Note: Block 5 baseline is perihelion = 1.0 (Hohmann) only, which is in our
# grid; budget = 0 means only Hohmann allowed, so we should reproduce ~2.78%.

summary = {
    "model": {
        "perihelion_grid_au": PERIHELION_GRID_AU,
        "tolerances_deg": TOLERANCES_DEG,
        "budgets_kms": BUDGETS_KMS,
        "num_launches": NUM_LAUNCHES,
        "phase_grid_n": PHASE_GRID_N,
    },
    "trajectory_family_stats": {
        "v_saturn_circular_kms": V_SATURN_HELIO_KMS,
        "dv_hohmann_at_saturn_kms": DV_HOHMANN,
        "crossing_nu_range_deg": crossing_nu_range_deg,
        "crossing_t_range_yr": t_jup_range,
        "dv_premium_max_kms": dv_premium_max,
        "dv_premium_at_perihelion_05": next(
            r["dv_premium_kms"] for r in family if r["perihelion_au"] == 0.50
        ),
    },
    "block5_reproduction": {
        "viable_fraction_5deg_budget_0kms": block5_repro,
        "block5_expected_at_5deg": 0.0278,
        "matches": abs(block5_repro - 0.0278) < 0.005,
    },
    "headline_results": {
        "viable_fraction_5deg_at_budgets_kms": {
            f"{r['budget_kms']:.2f}": r["viable_fraction"]
            for r in grid_rows if r["tolerance_deg"] == 5.0
        },
        "viable_fraction_10deg_at_budgets_kms": {
            f"{r['budget_kms']:.2f}": r["viable_fraction"]
            for r in grid_rows if r["tolerance_deg"] == 10.0
        },
        "campaign_mean_deliv_5deg_at_budgets_kms": {
            f"{r['budget_kms']:.2f}": r["campaign_mean_deliv_frac"]
            for r in grid_rows if r["tolerance_deg"] == 5.0
        },
    },
    "hypothesis_adjudication": {
        "H1_crossing_longitude_variance_lt_5deg": {
            "status": H1_status, "observed_nu_range_deg": crossing_nu_range_deg
        },
        "H2_crossing_time_range_ge_1p5yr": {
            "status": H2_status, "observed_t_range_yr": t_jup_range
        },
        "H3_premium_lt_1kms": {
            "status": H3_status, "observed_max_premium_kms": dv_premium_max
        },
        "H4_viable_fraction_5deg_1kms_in_0p2_to_0p5": {
            "status": H4_status, "observed": viable_5_1
        },
        "H5_campaign_mean_5deg_1kms_in_0p17_to_0p20": {
            "status": H5_status, "observed": deliv_5_1
        },
    },
}

with open(OUT / "summary.json", "w") as f:
    json.dump(summary, f, indent=2, default=str)

# -----------------------------------------------------------------------------
# Console summary
# -----------------------------------------------------------------------------

print("=" * 72)
print("R-jupiter-ga-saturn-exit-flexibility — results")
print("=" * 72)
print(f"Saturn circular orbit speed (km/s): {V_SATURN_HELIO_KMS:.3f}")
print(f"Hohmann Saturn-exit retrograde Δv (km/s): {DV_HOHMANN:.3f}")
print()
print("Trajectory family table (perihelion sweep):")
print(f"  {'perih(AU)':>10}  {'nu_jup(°)':>10}  {'t_to_jup(yr)':>13}"
      f"  {'v@Saturn(km/s)':>15}  {'Δv premium(km/s)':>17}")
for row in family:
    print(f"  {row['perihelion_au']:>10.2f}  "
          f"{row['nu_jup_crossing_deg']:>10.2f}  "
          f"{row['t_aphelion_to_jup_yr']:>13.3f}  "
          f"{row['v_at_saturn_kms']:>15.3f}  "
          f"{row['dv_premium_kms']:>17.3f}")
print()
print(f"H1 — crossing-longitude variance across perihelion grid: "
      f"{crossing_nu_range_deg:.2f}° ({'< 5°: held' if crossing_nu_range_deg < 5 else '≥ 5°: falsified'})")
print(f"H2 — crossing time-of-flight range: {t_jup_range:.2f} yr")
print(f"H3 — max Δv premium (at perihelion 0.5 AU): {dv_premium_max:.2f} km/s")
print()
print("Phase-averaged viable fraction grid:")
print(f"  {'tol':>5}", *(f"  budget {b:.2f}kms" for b in BUDGETS_KMS))
for tol in TOLERANCES_DEG:
    row_str = f"  ±{tol:>3.0f}°"
    for budget in BUDGETS_KMS:
        v = next(r["viable_fraction"] for r in grid_rows
                 if r["tolerance_deg"] == tol and r["budget_kms"] == budget)
        row_str += f"   {v*100:>9.2f}%"
    print(row_str)
print()
print("Campaign-mean delivered fraction grid:")
for tol in TOLERANCES_DEG:
    row_str = f"  ±{tol:>3.0f}°"
    for budget in BUDGETS_KMS:
        v = next(r["campaign_mean_deliv_frac"] for r in grid_rows
                 if r["tolerance_deg"] == tol and r["budget_kms"] == budget)
        row_str += f"   {v*100:>9.2f}%"
    print(row_str)
print()
print(f"Block-5 reproduction (perihelion = 1.0 / budget = 0 / ±5°): "
      f"{block5_repro*100:.2f}% (expected ~2.78%)")
print()
print("Hypothesis adjudication:")
for hname, hdata in summary["hypothesis_adjudication"].items():
    print(f"  {hname}: {hdata['status']}")
