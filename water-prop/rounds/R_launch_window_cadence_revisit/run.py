"""Launch-window cadence under the Jupiter-return-gravity-assist constraint.

R-residence-exit-maneuver (Block 4) closed the residence-class architecture at
21.8% central delivered fraction, where ~2.5 km/s of inbound delta-velocity
reduction comes from a Jupiter return gravity-assist. STUDY.md guessed
"roughly half" of Earth-Saturn launch windows have a useful Jupiter swing-by;
this round computes the fraction and translates it to effective cadence.

Model:
  - Coplanar circular orbits: Earth (1.0 AU, 1.0 yr), Jupiter (5.2 AU, 11.862 yr),
    Saturn (9.55 AU, 29.457 yr).
  - Earth-Saturn synodic launch cadence τ_ES = 1.0352 yr.
  - Per mission: outbound 6.04 yr (Hohmann), residence 0.5 yr, inbound Hohmann
    from Saturn (aphelion) to Earth (perihelion).
  - Inbound chunk crosses Jupiter's orbit (5.2 AU) at true anomaly 216.8° (descending
    leg from ν=180° at aphelion). Time and heliocentric longitude from Kepler.
  - For each launch n in [0, 57] (60-year span), compute Jupiter's heliocentric
    longitude at the chunk's Jupiter-orbit-crossing epoch. Angular separation =
    chunk longitude minus Jupiter longitude, signed in [-180°, +180°].
  - Window is Jupiter-viable at tolerance T° if |separation| ≤ T°.

Beyond the deterministic 60-yr run, we also compute:
  - Phase-ensemble (Monte Carlo over Jupiter's initial heliocentric longitude)
    to remove finite-sample noise from the deterministic single-phase run.
  - Cruise-delta-velocity cost curve: angular tolerance vs the cross-track
    delta-velocity required to actively redirect the chunk by that angle at
    Jupiter's orbital radius. Connects tolerance to cost so the Jupiter-GA
    net-benefit accounting closes.

Outputs:
  results/per_window.csv        — every launch: index, year, exit year, Jupiter
                                  crossing year, chunk and Jupiter heliocentric
                                  longitudes, separation, viable-at-each-tolerance
                                  flags.
  results/tolerance_sweep.csv   — Jupiter-viable fraction at ±2°, ±5°, ±10°,
                                  ±15°, ±30° (deterministic single-phase).
  results/ensemble_sweep.csv    — phase-ensemble mean fraction at each tolerance.
  results/cruise_dv_cost.csv    — cruise-delta-velocity required to enable each
                                  angular-tolerance window, and net Jupiter-GA
                                  benefit after subtracting the reshape cost.
  results/clustering.csv        — run-length encoding of Jupiter-viable / unaligned
                                  sequences at ±5° tolerance (for H2).
  results/cadence_policies.csv  — under skip-unaligned vs fly-all-windows policy,
                                  effective cadence and campaign-mean delivered
                                  fraction at each tolerance.
  results/summary.json          — headline numbers and hypothesis adjudication.
"""

from __future__ import annotations

import csv
import json
from math import atan2, cos, pi, sin, sqrt
from pathlib import Path

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------

# Orbital periods (Julian years; sidereal periods from NASA JPL HORIZONS).
T_EARTH   = 1.0000
T_JUPITER = 11.8618
T_SATURN  = 29.4571

# Semi-major axes (astronomical units).
A_EARTH   = 1.0000
A_JUPITER = 5.2030
A_SATURN  = 9.5549

# Earth-Saturn synodic period (yr).
TAU_ES = 1.0 / (1.0 / T_EARTH - 1.0 / T_SATURN)  # ≈ 1.0352 yr

# Mission timeline.
T_OUTBOUND  = 6.04   # yr; Hohmann Earth->Saturn (semi-major-axis 5.275 AU, half-period)
T_RESIDENCE = 0.50   # yr; Saturn residence operations
# Inbound is computed below from the Hohmann ellipse.

# Hohmann ellipse parameters for Saturn->Earth inbound.
A_HOH = (A_SATURN + A_EARTH) / 2.0              # semi-major-axis (AU)
E_HOH = (A_SATURN - A_EARTH) / (A_SATURN + A_EARTH)  # eccentricity
P_HOH = A_HOH * (1.0 - E_HOH * E_HOH)           # semi-latus rectum
T_HOH = A_HOH ** 1.5                            # period of the full ellipse (yr)
T_INBOUND_HALF = T_HOH / 2.0                    # aphelion->perihelion (yr); should be ~6.04

# Run parameters.
NUM_LAUNCHES = 58                # 58 launches × 1.0352 yr ≈ 60.04 yr
TOLERANCES_DEG = [2.0, 5.0, 10.0, 15.0, 30.0]

# Composite delivered fractions for cadence-policy computation
# (from R-residence-exit-maneuver/results/composite_a3_a5_a6.csv summary):
DELIV_FRAC_WITH_JUPITER    = 0.218   # A2+A3+A5+A6 central
DELIV_FRAC_WITHOUT_JUPITER = 0.155   # A2+A5+A6 only (no Jupiter gravity-assist), central

# Initial-condition phase offsets (deg). All zero is the worst-case baseline; the
# answer is invariant to a rigid rotation of all three orbital phases, so we
# report the result at this baseline plus average over an init-phase ensemble.
THETA0_EARTH   = 0.0
THETA0_JUPITER = 0.0
THETA0_SATURN  = 0.0

OUT = Path(__file__).parent / "results"
OUT.mkdir(parents=True, exist_ok=True)

# -----------------------------------------------------------------------------
# Kepler solver and Hohmann inbound geometry
# -----------------------------------------------------------------------------


def wrap360(deg: float) -> float:
    """Wrap angle to [0, 360)."""
    d = deg % 360.0
    if d < 0.0:
        d += 360.0
    return d


def signed_diff_deg(a: float, b: float) -> float:
    """Signed difference a - b wrapped into (-180, +180]."""
    d = (a - b) % 360.0
    if d > 180.0:
        d -= 360.0
    return d


def true_anom_at_radius_descending(r: float) -> float:
    """True anomaly (deg) where the Hohmann ellipse crosses radius r on the
    descending leg from aphelion (ν=180°) to perihelion (ν=360°)."""
    cos_nu = (P_HOH / r - 1.0) / E_HOH
    cos_nu = max(-1.0, min(1.0, cos_nu))
    # The "ascending" solution is in (0°, 180°); the descending solution is
    # 360° - that.
    nu_asc_rad = abs((cos_nu).__class__.__call__(0))  # placeholder; recompute below
    # Use math.acos via re-import to avoid name shadowing.
    from math import acos
    nu_asc = acos(cos_nu)  # radians in [0, π]
    nu_desc = 2.0 * pi - nu_asc  # descending leg
    return nu_desc * 180.0 / pi


def time_from_aphelion_to_nu(nu_deg: float) -> float:
    """Time (yr) on the Hohmann ellipse from aphelion (ν=180°) to true anomaly
    ν (deg). Uses Kepler's equation."""
    nu_rad = nu_deg * pi / 180.0
    # Eccentric anomaly E via half-angle (quadrant-safe).
    E_rad = 2.0 * atan2(
        sqrt(1.0 - E_HOH) * sin(nu_rad / 2.0),
        sqrt(1.0 + E_HOH) * cos(nu_rad / 2.0),
    )
    # atan2 returns in (-π, π]; we want positive E in the same revolution as ν.
    if E_rad < 0.0:
        E_rad += 2.0 * pi
    # Mean anomaly.
    M_rad = E_rad - E_HOH * sin(E_rad)
    # Mean motion n = 2π / T_HOH (per yr).
    n = 2.0 * pi / T_HOH
    t_from_perihelion = M_rad / n
    # Aphelion is at t = T_HOH / 2 from perihelion.
    t_from_aphelion = t_from_perihelion - T_HOH / 2.0
    # We want positive time elapsed; descending leg has ν in (180°, 360°), so
    # E in (π, 2π), so M in (π, 2π), so t_from_perihelion in (T/2, T), so
    # t_from_aphelion in (0, T/2). Good.
    return t_from_aphelion


# Pre-compute Jupiter-orbit-crossing geometry on the Hohmann inbound.
NU_JUP_CROSS_DEG = true_anom_at_radius_descending(A_JUPITER)   # ≈ 216.8°
T_JUP_CROSS_FROM_EXIT = time_from_aphelion_to_nu(NU_JUP_CROSS_DEG)  # yr

# -----------------------------------------------------------------------------
# Per-launch computation
# -----------------------------------------------------------------------------


def compute_window(n: int) -> dict:
    """Compute all per-window quantities for launch index n."""
    t_launch = n * TAU_ES                                   # yr (from t=0)
    t_exit   = t_launch + T_OUTBOUND + T_RESIDENCE          # yr
    t_cross  = t_exit + T_JUP_CROSS_FROM_EXIT               # yr (chunk at Jupiter orbit)

    # Saturn heliocentric longitude at Saturn-exit.
    theta_saturn_at_exit = wrap360(THETA0_SATURN + 360.0 * t_exit / T_SATURN)

    # The Hohmann inbound ellipse has aphelion at Saturn-exit and perihelion at
    # Earth-arrival. Heliocentric longitude of the line of apsides (perihelion
    # direction) is θ_Saturn_at_exit + 180°. True anomaly is measured from
    # perihelion, so heliocentric longitude of the chunk at ν is
    # θ_perihelion_dir + ν. (Both ν and longitude increase prograde for an
    # ascending inbound on the standard prograde orbit.)
    theta_perihelion_dir = wrap360(theta_saturn_at_exit + 180.0)
    theta_chunk_at_cross = wrap360(theta_perihelion_dir + NU_JUP_CROSS_DEG)

    # Jupiter heliocentric longitude at t_cross.
    theta_jupiter_at_cross = wrap360(THETA0_JUPITER + 360.0 * t_cross / T_JUPITER)

    # Angular separation (signed, chunk - Jupiter).
    sep_deg = signed_diff_deg(theta_chunk_at_cross, theta_jupiter_at_cross)

    return {
        "n": n,
        "t_launch_yr": t_launch,
        "t_exit_yr": t_exit,
        "t_jup_cross_yr": t_cross,
        "theta_saturn_at_exit_deg": theta_saturn_at_exit,
        "theta_chunk_at_cross_deg": theta_chunk_at_cross,
        "theta_jupiter_at_cross_deg": theta_jupiter_at_cross,
        "separation_deg": sep_deg,
        "abs_separation_deg": abs(sep_deg),
    }


# -----------------------------------------------------------------------------
# Write per-window CSV
# -----------------------------------------------------------------------------

per_window = [compute_window(n) for n in range(NUM_LAUNCHES)]

with open(OUT / "per_window.csv", "w", newline="") as f:
    fieldnames = [
        "n", "t_launch_yr", "t_exit_yr", "t_jup_cross_yr",
        "theta_saturn_at_exit_deg", "theta_chunk_at_cross_deg",
        "theta_jupiter_at_cross_deg", "separation_deg", "abs_separation_deg",
    ] + [f"viable_{int(t)}deg" for t in TOLERANCES_DEG]
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    for row in per_window:
        out = {k: row[k] for k in row}
        for tol in TOLERANCES_DEG:
            out[f"viable_{int(tol)}deg"] = int(row["abs_separation_deg"] <= tol)
        w.writerow(out)

# -----------------------------------------------------------------------------
# Tolerance sweep: Jupiter-viable fraction per tolerance
# -----------------------------------------------------------------------------

tolerance_rows = []
for tol in TOLERANCES_DEG:
    viable = [r for r in per_window if r["abs_separation_deg"] <= tol]
    frac = len(viable) / len(per_window)
    tolerance_rows.append({
        "tolerance_deg": tol,
        "viable_count": len(viable),
        "total_count": len(per_window),
        "viable_fraction": frac,
    })

with open(OUT / "tolerance_sweep.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["tolerance_deg", "viable_count",
                                       "total_count", "viable_fraction"])
    w.writeheader()
    w.writerows(tolerance_rows)

# -----------------------------------------------------------------------------
# Clustering analysis (H2): run-length encoding at ±5° tolerance
# -----------------------------------------------------------------------------

REF_TOL = 5.0
flags = [int(r["abs_separation_deg"] <= REF_TOL) for r in per_window]

runs = []
if flags:
    cur_val = flags[0]
    cur_len = 1
    cur_start = 0
    for i in range(1, len(flags)):
        if flags[i] == cur_val:
            cur_len += 1
        else:
            runs.append((cur_start, cur_val, cur_len))
            cur_val = flags[i]
            cur_len = 1
            cur_start = i
    runs.append((cur_start, cur_val, cur_len))

with open(OUT / "clustering.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["start_index", "start_year", "type", "run_length_windows",
                "run_length_years"])
    for start, val, length in runs:
        kind = "viable" if val == 1 else "unaligned"
        w.writerow([
            start,
            f"{start * TAU_ES:.3f}",
            kind,
            length,
            f"{length * TAU_ES:.3f}",
        ])

# -----------------------------------------------------------------------------
# Cadence-policy computation
# -----------------------------------------------------------------------------

policy_rows = []
total_span_yr = NUM_LAUNCHES * TAU_ES
for tol in TOLERANCES_DEG:
    viable_count = sum(1 for r in per_window if r["abs_separation_deg"] <= tol)
    viable_frac = viable_count / NUM_LAUNCHES if NUM_LAUNCHES else 0.0
    # Policy A: skip-unaligned. Effective cadence = total_span / viable_count.
    eff_cadence_skip = total_span_yr / viable_count if viable_count else float("inf")
    # Policy A campaign-mean delivered fraction per launched ship = with-Jupiter
    # (because every launched ship has the Jupiter gravity-assist).
    deliv_per_ship_skip = DELIV_FRAC_WITH_JUPITER
    # Annualised delivered-fraction-per-year proxy (relative to baseline).
    baseline_annual = DELIV_FRAC_WITH_JUPITER / TAU_ES
    skip_annual = (deliv_per_ship_skip / eff_cadence_skip) if eff_cadence_skip != float("inf") else 0.0

    # Policy B: fly-all-windows. Cadence stays τ_ES. Campaign-mean delivered
    # fraction per ship = weighted average of with/without-Jupiter.
    deliv_per_ship_fly = (viable_frac * DELIV_FRAC_WITH_JUPITER
                          + (1.0 - viable_frac) * DELIV_FRAC_WITHOUT_JUPITER)
    fly_annual = deliv_per_ship_fly / TAU_ES

    policy_rows.append({
        "tolerance_deg": tol,
        "viable_fraction": viable_frac,
        "policy_skip_effective_cadence_yr": eff_cadence_skip,
        "policy_skip_deliv_frac_per_ship": deliv_per_ship_skip,
        "policy_skip_annualised_deliv_frac": skip_annual,
        "policy_fly_effective_cadence_yr": TAU_ES,
        "policy_fly_deliv_frac_per_ship": deliv_per_ship_fly,
        "policy_fly_annualised_deliv_frac": fly_annual,
        "baseline_annualised_deliv_frac_for_ref": baseline_annual,
    })

with open(OUT / "cadence_policies.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(policy_rows[0].keys()))
    w.writeheader()
    w.writerows(policy_rows)

# -----------------------------------------------------------------------------
# Phase ensemble: vary Jupiter's initial heliocentric longitude to remove
# finite-sample noise. The deterministic single-phase run can over- or
# under-count by chance, especially at small tolerances.
# -----------------------------------------------------------------------------

def viable_fraction_at_phase(theta0_jup_deg: float, tol_deg: float) -> float:
    """Fraction of NUM_LAUNCHES Earth-Saturn synodics that are Jupiter-viable at
    tolerance tol_deg, given Jupiter's initial heliocentric longitude theta0_jup_deg.

    Earth and Saturn initial phases are held at 0 (their relative phase is what
    sets the Earth-Saturn synodic; rotating both by the same angle does not
    affect the answer)."""
    count = 0
    for n in range(NUM_LAUNCHES):
        t_launch = n * TAU_ES
        t_exit   = t_launch + T_OUTBOUND + T_RESIDENCE
        t_cross  = t_exit + T_JUP_CROSS_FROM_EXIT
        theta_saturn_at_exit = wrap360(360.0 * t_exit / T_SATURN)
        theta_chunk_at_cross = wrap360(theta_saturn_at_exit + 180.0 + NU_JUP_CROSS_DEG)
        theta_jupiter_at_cross = wrap360(theta0_jup_deg + 360.0 * t_cross / T_JUPITER)
        sep = abs(signed_diff_deg(theta_chunk_at_cross, theta_jupiter_at_cross))
        if sep <= tol_deg:
            count += 1
    return count / NUM_LAUNCHES if NUM_LAUNCHES else 0.0


# Sample Jupiter's initial phase on a fine deterministic grid (no PRNG needed).
PHASE_GRID = [i * (360.0 / 360) for i in range(360)]  # 1° resolution, 360 samples
ensemble_rows = []
for tol in TOLERANCES_DEG:
    fracs = [viable_fraction_at_phase(p, tol) for p in PHASE_GRID]
    mean_frac = sum(fracs) / len(fracs)
    min_frac = min(fracs)
    max_frac = max(fracs)
    analytic = (2.0 * tol) / 360.0     # uniform-spacing limit
    ensemble_rows.append({
        "tolerance_deg": tol,
        "mean_fraction": mean_frac,
        "min_fraction":  min_frac,
        "max_fraction":  max_frac,
        "analytic_fraction": analytic,
    })

with open(OUT / "ensemble_sweep.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(ensemble_rows[0].keys()))
    w.writeheader()
    w.writerows(ensemble_rows)

# -----------------------------------------------------------------------------
# Cruise-delta-velocity cost of widening the tolerance.
#
# Heliocentric speed at the Jupiter-orbit crossing (Hohmann inbound from Saturn).
# v = (2π AU/yr) × sqrt(2/r - 1/a)   in AU/yr; convert to km/s via 1 AU/yr =
# 4.7404 km/s.
#
# Time available to redirect from Saturn exit (aphelion) to Jupiter crossing
# is T_JUP_CROSS_FROM_EXIT (about 4.63 yr).
#
# Cross-track displacement required at Jupiter (5.2 AU) for an angular shift
# Δθ is r_jup × sin(Δθ) ≈ r_jup × Δθ for small Δθ. With constant cross-track
# acceleration over the cruise, displacement = ½ a t² and Δv = a t, so the
# required Δv for displacement d in time t is Δv_min = 2 d / t (under constant
# acceleration; impulsive-midcourse can be cheaper by factor ≤ 2, but constant
# acceleration is the right rough proxy for an electric-propulsion vehicle).
# -----------------------------------------------------------------------------

KM_PER_AU = 1.495978707e8
SEC_PER_YR = 3.15576e7

v_hel_at_jup = 2 * pi * sqrt(2.0 / A_JUPITER - 1.0 / A_HOH)        # AU/yr
v_hel_at_jup_kms = v_hel_at_jup * (KM_PER_AU / SEC_PER_YR)         # km/s

# Cross-track Δv to redirect by Δθ at Jupiter (km/s).
def cruise_dv_for_angular_shift_kms(delta_theta_deg: float) -> float:
    if delta_theta_deg <= 0:
        return 0.0
    d_km = A_JUPITER * KM_PER_AU * sin(delta_theta_deg * pi / 180.0)
    t_sec = T_JUP_CROSS_FROM_EXIT * SEC_PER_YR
    return 2.0 * d_km / t_sec

# Effective inbound delta-velocity saving from Jupiter gravity-assist (km/s):
# anchored to R-residence-exit-maneuver's 2.5 km/s.
JUPITER_GA_DV_SAVING = 2.5

dv_cost_rows = []
for tol in TOLERANCES_DEG:
    cruise_dv = cruise_dv_for_angular_shift_kms(tol)
    net_benefit = JUPITER_GA_DV_SAVING - cruise_dv
    dv_cost_rows.append({
        "tolerance_deg": tol,
        "cruise_dv_required_kms": cruise_dv,
        "jupiter_ga_saving_kms": JUPITER_GA_DV_SAVING,
        "net_benefit_kms": net_benefit,
        "net_positive": int(net_benefit > 0),
    })

with open(OUT / "cruise_dv_cost.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(dv_cost_rows[0].keys()))
    w.writeheader()
    w.writerows(dv_cost_rows)

# Self-consistent tolerance: the largest tolerance at which cruise reshape is
# still net-positive (cost < Jupiter-GA benefit).
self_consistent_tol = None
for row in dv_cost_rows:
    if row["net_benefit_kms"] > 0:
        self_consistent_tol = row["tolerance_deg"]
# Refine via bisection between adjacent tolerances if last positive < first negative.
# (Simple sweep over 0.5° grid for the figure-of-merit.)
fine_grid = [0.5 * i for i in range(1, 121)]  # 0.5° to 60.0°
fine_self_consistent_deg = 0.0
for tol in fine_grid:
    if JUPITER_GA_DV_SAVING - cruise_dv_for_angular_shift_kms(tol) > 0:
        fine_self_consistent_deg = tol

# Phase-ensemble viable fraction at the self-consistent tolerance.
self_consistent_frac = sum(
    viable_fraction_at_phase(p, fine_self_consistent_deg) for p in PHASE_GRID
) / len(PHASE_GRID)

# -----------------------------------------------------------------------------
# H2 adjudication: clustering test.
#
# A "clustered" pattern means Jupiter-viable windows arrive in short bursts with
# long droughts between, set by the Jupiter-Saturn synodic (~19.86 yr). Use
# coefficient of variation (CV) of inter-viable spacing: CV > ~0.5 indicates
# clustering vs Poisson-like uniform.
# -----------------------------------------------------------------------------

viable_indices = [r["n"] for r in per_window if r["abs_separation_deg"] <= REF_TOL]
spacings = [viable_indices[i+1] - viable_indices[i] for i in range(len(viable_indices) - 1)]
if spacings:
    mean_sp = sum(spacings) / len(spacings)
    var_sp = sum((s - mean_sp) ** 2 for s in spacings) / len(spacings)
    sd_sp = sqrt(var_sp)
    cv_sp = sd_sp / mean_sp if mean_sp > 0 else 0.0
else:
    mean_sp = sd_sp = cv_sp = 0.0

# Find longest viable run and longest drought.
longest_viable_run = max((length for start, val, length in runs if val == 1), default=0)
longest_unaligned_run = max((length for start, val, length in runs if val == 0), default=0)

# -----------------------------------------------------------------------------
# Hypothesis adjudication for summary.json
# -----------------------------------------------------------------------------

# H1: viable fraction at ±5° in [0.20, 0.50]?
viable_frac_5 = next(r["viable_fraction"] for r in policy_rows if r["tolerance_deg"] == 5.0)
H1_status = (
    "held" if 0.20 <= viable_frac_5 <= 0.50
    else "falsified_low" if viable_frac_5 < 0.20
    else "falsified_high"
)

# H2: clustering. Held if CV > 0.5 and a drought ≥ 5 synodics exists.
H2_status = (
    "held" if cv_sp > 0.5 and longest_unaligned_run >= 5
    else "falsified"
)

# H3: skip-unaligned effective cadence at ±5° in [4.0, 10.0] yr?
eff_cad_5_skip = next(r["policy_skip_effective_cadence_yr"]
                     for r in policy_rows if r["tolerance_deg"] == 5.0)
H3_status = (
    "held" if 4.0 <= eff_cad_5_skip <= 10.0
    else "falsified_low" if eff_cad_5_skip < 4.0
    else "falsified_high"
)

# H4: fly-all-windows campaign-mean delivered fraction at ±5° in [0.16, 0.19]?
deliv_5_fly = next(r["policy_fly_deliv_frac_per_ship"]
                  for r in policy_rows if r["tolerance_deg"] == 5.0)
H4_status = (
    "held" if 0.16 <= deliv_5_fly <= 0.19
    else "falsified_low" if deliv_5_fly < 0.16
    else "falsified_high"
)

# H5: at ±15° (proxy for ≤ 0.5 km/s reshape), viable fraction ≥ 0.70?
viable_frac_15 = next(r["viable_fraction"] for r in policy_rows if r["tolerance_deg"] == 15.0)
H5_status = "held" if viable_frac_15 >= 0.70 else "falsified"

summary = {
    "model": {
        "earth_period_yr": T_EARTH,
        "jupiter_period_yr": T_JUPITER,
        "saturn_period_yr": T_SATURN,
        "earth_saturn_synodic_yr": TAU_ES,
        "hohmann_inbound_half_period_yr": T_INBOUND_HALF,
        "nu_jupiter_crossing_deg": NU_JUP_CROSS_DEG,
        "t_jupiter_crossing_from_exit_yr": T_JUP_CROSS_FROM_EXIT,
        "num_launches": NUM_LAUNCHES,
        "total_span_yr": total_span_yr,
        "tolerances_deg": TOLERANCES_DEG,
        "deliv_frac_with_jupiter_central": DELIV_FRAC_WITH_JUPITER,
        "deliv_frac_without_jupiter_central": DELIV_FRAC_WITHOUT_JUPITER,
    },
    "results": {
        "viable_fraction_by_tolerance_deterministic": {
            f"{int(r['tolerance_deg'])}deg": r["viable_fraction"]
            for r in tolerance_rows
        },
        "viable_fraction_by_tolerance_ensemble_mean": {
            f"{int(r['tolerance_deg'])}deg": r["mean_fraction"]
            for r in ensemble_rows
        },
        "viable_fraction_by_tolerance_analytic_limit": {
            f"{int(r['tolerance_deg'])}deg": r["analytic_fraction"]
            for r in ensemble_rows
        },
        "skip_unaligned_effective_cadence_yr_by_tolerance": {
            f"{int(r['tolerance_deg'])}deg": r["policy_skip_effective_cadence_yr"]
            for r in policy_rows
        },
        "fly_all_deliv_frac_per_ship_by_tolerance": {
            f"{int(r['tolerance_deg'])}deg": r["policy_fly_deliv_frac_per_ship"]
            for r in policy_rows
        },
        "clustering_at_5deg": {
            "viable_count": len(viable_indices),
            "spacing_mean_synodics": mean_sp,
            "spacing_sd_synodics": sd_sp,
            "spacing_cv": cv_sp,
            "longest_viable_run_synodics": longest_viable_run,
            "longest_unaligned_run_synodics": longest_unaligned_run,
        },
        "cruise_dv_cost": {
            "heliocentric_speed_at_jupiter_kms": v_hel_at_jup_kms,
            "cruise_time_saturn_to_jupiter_yr": T_JUP_CROSS_FROM_EXIT,
            "jupiter_ga_saving_kms": JUPITER_GA_DV_SAVING,
            "cruise_dv_by_tolerance_kms": {
                f"{int(r['tolerance_deg'])}deg": r["cruise_dv_required_kms"]
                for r in dv_cost_rows
            },
            "net_benefit_by_tolerance_kms": {
                f"{int(r['tolerance_deg'])}deg": r["net_benefit_kms"]
                for r in dv_cost_rows
            },
            "self_consistent_max_tolerance_deg": fine_self_consistent_deg,
            "self_consistent_phase_avg_viable_fraction": self_consistent_frac,
        },
    },
    "hypothesis_adjudication": {
        "H1_fraction_at_5deg_in_0p2_to_0p5":  {"status": H1_status, "observed": viable_frac_5},
        "H2_clustering":                     {"status": H2_status,
                                              "cv_spacing": cv_sp,
                                              "longest_drought_synodics": longest_unaligned_run},
        "H3_skip_eff_cadence_5deg_in_4_to_10yr": {"status": H3_status, "observed_yr": eff_cad_5_skip},
        "H4_fly_deliv_frac_5deg_in_0p16_to_0p19": {"status": H4_status, "observed": deliv_5_fly},
        "H5_15deg_proxy_fraction_ge_0p70":    {"status": H5_status, "observed": viable_frac_15},
    },
}

with open(OUT / "summary.json", "w") as f:
    json.dump(summary, f, indent=2)

# -----------------------------------------------------------------------------
# Console summary
# -----------------------------------------------------------------------------

print("=" * 72)
print("R-launch-window-cadence-revisit — results")
print("=" * 72)
print(f"Earth-Saturn synodic (yr): {TAU_ES:.4f}")
print(f"Hohmann inbound half-period (yr): {T_INBOUND_HALF:.4f}")
print(f"Jupiter-orbit-crossing true anomaly (deg): {NU_JUP_CROSS_DEG:.3f}")
print(f"Time from Saturn-exit to Jupiter crossing (yr): {T_JUP_CROSS_FROM_EXIT:.4f}")
print(f"Total mission outbound+residence+to-Jupiter (yr): "
      f"{T_OUTBOUND + T_RESIDENCE + T_JUP_CROSS_FROM_EXIT:.3f}")
print()
print("Viable fractions by tolerance:")
print(f"  {'tol':>5}    {'determ':>7}    {'ensemble':>9}    {'analytic':>9}")
for r, e in zip(tolerance_rows, ensemble_rows):
    print(f"  ±{r['tolerance_deg']:>4.0f}°   {r['viable_fraction']*100:>6.2f}%   "
          f"{e['mean_fraction']*100:>8.2f}%   {e['analytic_fraction']*100:>8.2f}%")
print()
print("Cruise-Δv cost vs Jupiter-GA benefit (2.5 km/s saving):")
print(f"  {'tol':>5}    {'cruise Δv':>10}    {'net':>7}    positive?")
for row in dv_cost_rows:
    sign = "yes" if row["net_positive"] else "NO"
    print(f"  ±{row['tolerance_deg']:>4.0f}°   {row['cruise_dv_required_kms']:>8.2f} km/s   "
          f"{row['net_benefit_kms']:>5.2f} km/s   {sign}")
print()
print(f"Self-consistent max angular tolerance (net Δv-positive): "
      f"±{fine_self_consistent_deg:.1f}°")
print(f"Phase-averaged viable fraction at self-consistent tolerance: "
      f"{self_consistent_frac*100:.2f}%")
print()
print("Cadence under skip-unaligned policy (yr per launched ship):")
for r in policy_rows:
    print(f"  ±{r['tolerance_deg']:>4.0f}°   effective cadence "
          f"{r['policy_skip_effective_cadence_yr']:>6.2f} yr")
print()
print("Campaign-mean delivered fraction under fly-all-windows policy:")
for r in policy_rows:
    print(f"  ±{r['tolerance_deg']:>4.0f}°   deliv-frac/ship "
          f"{r['policy_fly_deliv_frac_per_ship']*100:>5.2f}%")
print()
print(f"Clustering at ±{REF_TOL:.0f}° (Jupiter-viable run-length statistics):")
print(f"  viable count           : {len(viable_indices)}/{NUM_LAUNCHES}")
print(f"  inter-viable spacing   : mean {mean_sp:.2f} synodics, sd {sd_sp:.2f}, "
      f"CV {cv_sp:.2f}")
print(f"  longest viable run     : {longest_viable_run} consecutive synodics")
print(f"  longest unaligned run  : {longest_unaligned_run} consecutive synodics "
      f"(= {longest_unaligned_run * TAU_ES:.1f} yr drought)")
print()
print("Hypothesis adjudication:")
for hname, hdata in summary["hypothesis_adjudication"].items():
    print(f"  {hname}: {hdata['status']}")
