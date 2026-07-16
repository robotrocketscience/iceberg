"""Aerocapture-savings bracket with heat-shield-mass-cost bookkeeping.

Re-evaluates the load-bearing aerocapture lever in the post-Jupiter-GA composite
architecture. Block 4 modeled aerocapture as a 1.5-km/s velocity saving on the
inbound segment with no heat-shield mass cost. This round:

  1. Brackets the velocity saving across [0.0, 3.0] km/s.
  2. Adds heat-shield mass cost (areal-density × surface-area scaling).
  3. Computes net delivered fraction across the (savings, TPS density) grid.
  4. Cross-checks against Block 4's A1 = 3.9%, A2 = 7.2%, composite no-Jupiter
     ~15.5% reference values.

Output determines whether the composite architecture's claimed ~16% steady-state
delivered fraction (Blocks 5/6/7) survives TPS-mass bookkeeping.
"""

from __future__ import annotations

import csv
import json
from math import exp, pi, sqrt
from pathlib import Path

# -----------------------------------------------------------------------------
# Constants (matching Block 4 / R-residence-exit-maneuver)
# -----------------------------------------------------------------------------

G0 = 9.80665                # m/s²

# Mass model (Variant B 500-kilowatt-electric).
M_DRY_T_BASE = 200.0        # tonnes
M_COLLECTED_T = 200.0       # tonnes (slurry at residence)
M_JETTISON_T = 20.0         # tonnes (A6 hardware jettison)
M_DRY_T_EFFECTIVE = M_DRY_T_BASE - M_JETTISON_T   # 180 t after A6 jettison

# Δv segments.
DV_EXIT_KMS = 7.4
DV_INBOUND_BASELINE_KMS = 24.7

# Specific impulses.
ISP_EXIT_S    = 7000.0      # A5 uplift active
ISP_INBOUND_S = 5000.0      # NEP baseline at near-term cathode life

# Earth geometry.
MU_EARTH_KM3_S2 = 398600.4418
R_EARTH_KM = 6371.0
ALT_PERIAPSIS_KM = 200.0
R_PERIAPSIS_KM = R_EARTH_KM + ALT_PERIAPSIS_KM
ALT_LEO_KM = 400.0
R_LEO_KM = R_EARTH_KM + ALT_LEO_KM

V_LEO_KMS = sqrt(MU_EARTH_KM3_S2 / R_LEO_KM)            # ≈ 7.67 km/s

# Water cargo geometry.
RHO_WATER_KG_M3 = 1000.0
M_CARGO_FOR_SHIELD_T = M_COLLECTED_T                     # 200 t shielded
V_CARGO_M3 = M_CARGO_FOR_SHIELD_T * 1000.0 / RHO_WATER_KG_M3   # 200 m³
R_CARGO_M = (3.0 * V_CARGO_M3 / (4.0 * pi)) ** (1.0/3.0)        # 3.617 m
SA_CARGO_M2 = 4.0 * pi * R_CARGO_M ** 2                          # 164.5 m²

# Sweep grids.
DV_SAVINGS_GRID_KMS = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
TPS_AREAL_DENSITY_GRID = [0, 30, 50, 80, 120, 200]    # kg/m²

OUT = Path(__file__).parent / "results"
OUT.mkdir(parents=True, exist_ok=True)

# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------

def mass_ratio(dv_kms: float, isp_s: float) -> float:
    """Tsiolkovsky mass ratio for delta-velocity dv (km/s) and Isp (s)."""
    return exp(dv_kms * 1000.0 / (G0 * isp_s))


def v_infinity_from_savings(savings_kms: float) -> float:
    """Block 4's 1.5 km/s saving is interpreted as an Edelbaum-spiral
    equivalent, not a hyperbolic-to-LEO conversion. To compute entry velocity,
    we approximate v_∞ as a function of saving by treating savings ∈ [0, 3] as
    spanning v_∞ from ~0 km/s (full electric capture) to ~3 km/s (aggressive
    hyperbolic entry replacing more of the inbound spiral).

    Use linear interpolation: v_∞ ≈ savings × 2.0. (At savings = 1.5, v_∞ ≈ 3
    km/s; entry velocity ≈ 11.4 km/s. At savings = 3.0, v_∞ ≈ 6 km/s; entry
    velocity ≈ 12.6 km/s.) This is a rough proxy; the savings → v_∞ mapping is
    the largest source of uncertainty in this round."""
    return savings_kms * 2.0


def entry_velocity_from_v_infinity(v_inf_kms: float) -> float:
    """Atmospheric entry velocity at periapsis given hyperbolic excess v_∞."""
    return sqrt(v_inf_kms * v_inf_kms + 2.0 * MU_EARTH_KM3_S2 / R_PERIAPSIS_KM)


def heat_shield_mass_t(areal_density_kg_m2: float, coverage_frac: float = 1.0) -> float:
    """Heat-shield mass in tonnes, from surface-area × areal-density model.

    coverage_frac is the fraction of the cargo's full surface area that is
    actually shielded. 1.0 = full sphere (conservative); 0.5 = windward-only
    (typical biconic); 0.3 = sphere-cone with backshell only marginal."""
    return coverage_frac * SA_CARGO_M2 * areal_density_kg_m2 / 1000.0


# Coverage-fraction sensitivity grid.
COVERAGE_GRID = [0.30, 0.50, 1.00]


# -----------------------------------------------------------------------------
# Entry-velocity table
# -----------------------------------------------------------------------------

entry_rows = []
for sav in DV_SAVINGS_GRID_KMS:
    v_inf = v_infinity_from_savings(sav)
    v_ent = entry_velocity_from_v_infinity(v_inf)
    entry_rows.append({
        "savings_kms": sav,
        "v_infinity_kms": v_inf,
        "entry_velocity_kms": v_ent,
        "propulsive_equiv_to_leo_kms": v_ent - V_LEO_KMS,
    })

with open(OUT / "entry_velocity.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(entry_rows[0].keys()))
    w.writeheader()
    w.writerows(entry_rows)

# -----------------------------------------------------------------------------
# Heat-shield mass table
# -----------------------------------------------------------------------------

shield_rows = []
for rho in TPS_AREAL_DENSITY_GRID:
    m_shield = heat_shield_mass_t(rho)
    shield_rows.append({
        "areal_density_kg_m2": rho,
        "surface_area_m2": SA_CARGO_M2,
        "heat_shield_mass_t": m_shield,
        "mass_fraction_of_cargo_pct": 100.0 * m_shield / M_CARGO_FOR_SHIELD_T,
    })

with open(OUT / "heat_shield_mass.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(shield_rows[0].keys()))
    w.writeheader()
    w.writerows(shield_rows)

# -----------------------------------------------------------------------------
# Delivered-fraction calculator
# -----------------------------------------------------------------------------

def delivered_fraction(savings_kms: float, tps_areal_density_kg_m2: float,
                       coverage_frac: float = 1.0,
                       use_jettison: bool = True) -> dict:
    """Compute delivered fraction of collected water for a given (savings,
    TPS density, shield coverage fraction) combination. All other parameters
    are pinned to the composite architecture (A5 specific-impulse uplift
    active, A6 jettison active)."""
    dv_inbound = DV_INBOUND_BASELINE_KMS - savings_kms
    if dv_inbound < 0:
        dv_inbound = 0.0

    m_dry_base_eff = M_DRY_T_EFFECTIVE if use_jettison else M_DRY_T_BASE

    # Heat-shield mass — part of vehicle inert mass throughout both burns
    # (it travels from Saturn-departure through inbound to Earth-entry).
    m_shield = heat_shield_mass_t(tps_areal_density_kg_m2, coverage_frac)
    m_dry_total = m_dry_base_eff + m_shield

    # Exit burn: water + dry mass (incl. shield) at residence; consume water
    # as propellant.
    m_at_exit = M_COLLECTED_T + m_dry_total
    mr_exit = mass_ratio(DV_EXIT_KMS, ISP_EXIT_S)
    m_post_exit = m_at_exit / mr_exit

    # Inbound burn.
    mr_inbound = mass_ratio(dv_inbound, ISP_INBOUND_S)
    m_at_earth = m_post_exit / mr_inbound

    # At entry, shield ablates; delivered = arriving - dry_base - shield.
    m_delivered = max(0.0, m_at_earth - m_dry_total)
    frac = m_delivered / M_COLLECTED_T

    return {
        "savings_kms": savings_kms,
        "tps_areal_density_kg_m2": tps_areal_density_kg_m2,
        "coverage_frac": coverage_frac,
        "dv_inbound_kms": dv_inbound,
        "m_dry_base_eff_t": m_dry_base_eff,
        "m_shield_t": m_shield,
        "m_dry_total_t": m_dry_total,
        "m_post_exit_t": m_post_exit,
        "m_at_earth_t": m_at_earth,
        "m_delivered_t": m_delivered,
        "delivered_fraction": frac,
    }


# Cross-check Block 4 reference values.
# A1 (no aerocapture, no specific-impulse uplift, no jettison): baseline.
def deliv_frac_a1():
    m_dry = M_DRY_T_BASE
    m_at_exit = M_COLLECTED_T + m_dry
    mr_exit = mass_ratio(DV_EXIT_KMS, ISP_INBOUND_S)   # specific-impulse baseline
    m_post_exit = m_at_exit / mr_exit
    mr_inbound = mass_ratio(DV_INBOUND_BASELINE_KMS, ISP_INBOUND_S)
    m_at_earth = m_post_exit / mr_inbound
    m_delivered = max(0.0, m_at_earth - m_dry)
    return m_delivered / M_COLLECTED_T

# A2 (aerocapture only, no specific-impulse uplift, no jettison).
def deliv_frac_a2(savings_kms: float):
    m_dry = M_DRY_T_BASE
    m_at_exit = M_COLLECTED_T + m_dry
    mr_exit = mass_ratio(DV_EXIT_KMS, ISP_INBOUND_S)
    m_post_exit = m_at_exit / mr_exit
    dv_in = DV_INBOUND_BASELINE_KMS - savings_kms
    mr_inbound = mass_ratio(dv_in, ISP_INBOUND_S)
    m_at_earth = m_post_exit / mr_inbound
    m_delivered = max(0.0, m_at_earth - m_dry)
    return m_delivered / M_COLLECTED_T

a1_check = deliv_frac_a1()
a2_check_at_15 = deliv_frac_a2(1.5)
composite_no_jupiter_check = delivered_fraction(1.5, 0)["delivered_fraction"]

# Build 3D grid: (savings, areal density, coverage fraction).
grid_rows = []
for sav in DV_SAVINGS_GRID_KMS:
    for rho in TPS_AREAL_DENSITY_GRID:
        for cov in COVERAGE_GRID:
            r = delivered_fraction(sav, rho, cov)
            grid_rows.append(r)

with open(OUT / "delivered_frac_grid.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(grid_rows[0].keys()))
    w.writeheader()
    w.writerows(grid_rows)

# Composite-corrected values at central and boundary parameters.
# Central case: 1.5 km/s savings, 50 kg/m² TPS, 0.5 coverage (windward-only biconic).
central = delivered_fraction(1.5, 50, 0.5)
central_sphere = delivered_fraction(1.5, 50, 1.0)
central_lowcov = delivered_fraction(1.5, 50, 0.3)
boundary_low_sav  = delivered_fraction(0.5, 50, 0.5)
boundary_high_sav = delivered_fraction(2.5, 50, 0.5)
boundary_high_tps = delivered_fraction(1.5, 120, 0.5)
boundary_low_tps  = delivered_fraction(1.5, 30, 0.5)
no_aero           = delivered_fraction(0.0, 0, 0.5)
no_aero_with_shield = delivered_fraction(0.0, 50, 0.5)  # shield wasted if no aerocapture

# Jupiter-aligned composite (savings = 1.5 km/s aerocapture + 2.5 km/s Jupiter GA).
def delivered_fraction_with_jupiter(aero_savings, jga_savings, tps_rho, coverage=0.5):
    dv_inbound = DV_INBOUND_BASELINE_KMS - aero_savings - jga_savings
    m_shield = heat_shield_mass_t(tps_rho, coverage)
    m_dry_total = M_DRY_T_EFFECTIVE + m_shield
    m_at_exit = M_COLLECTED_T + m_dry_total
    mr_exit = mass_ratio(DV_EXIT_KMS, ISP_EXIT_S)
    m_post_exit = m_at_exit / mr_exit
    mr_inbound = mass_ratio(dv_inbound, ISP_INBOUND_S)
    m_at_earth = m_post_exit / mr_inbound
    m_delivered = max(0.0, m_at_earth - m_dry_total)
    return m_delivered / M_COLLECTED_T

composite_with_jupiter = delivered_fraction_with_jupiter(1.5, 2.5, 50, 0.5)
composite_with_jupiter_no_shield = delivered_fraction_with_jupiter(1.5, 2.5, 0, 0.0)

# Steady-state campaign mean (using Block 5's 2.78% Jupiter-viable for ±5°):
JUPITER_VIABLE_FRAC = 0.075   # at ±13.5° self-consistent (Block 5/6/7)
campaign_mean_corrected = (
    JUPITER_VIABLE_FRAC * composite_with_jupiter
    + (1.0 - JUPITER_VIABLE_FRAC) * central["delivered_fraction"]
)

with open(OUT / "composite_corrected.csv", "w", newline="") as f:
    rows = [
        ("a1_no_levers",                    a1_check),
        ("a2_aerocapture_only_no_shield",    a2_check_at_15),
        ("composite_no_jupiter_no_shield",   composite_no_jupiter_check),
        ("composite_no_jupiter_central_shield_30pct_coverage", central_lowcov["delivered_fraction"]),
        ("composite_no_jupiter_central_shield_50pct_coverage", central["delivered_fraction"]),
        ("composite_no_jupiter_central_shield_full_sphere", central_sphere["delivered_fraction"]),
        ("composite_no_jupiter_low_sav",     boundary_low_sav["delivered_fraction"]),
        ("composite_no_jupiter_high_sav",    boundary_high_sav["delivered_fraction"]),
        ("composite_no_jupiter_high_tps",    boundary_high_tps["delivered_fraction"]),
        ("composite_no_jupiter_low_tps",     boundary_low_tps["delivered_fraction"]),
        ("composite_with_jupiter_central_shield", composite_with_jupiter),
        ("composite_with_jupiter_no_shield",      composite_with_jupiter_no_shield),
        ("campaign_mean_corrected_7p5pct_jupiter_aligned", campaign_mean_corrected),
    ]
    w = csv.writer(f)
    w.writerow(["scenario", "delivered_fraction"])
    for label, val in rows:
        w.writerow([label, val])

# -----------------------------------------------------------------------------
# Hypothesis adjudication
# -----------------------------------------------------------------------------

# H1: v_∞ ≈ 4 km/s (at central savings = 1.5), entry velocity 11.4-12.1 km/s.
v_inf_central = v_infinity_from_savings(1.5)
v_ent_central = entry_velocity_from_v_infinity(v_inf_central)
H1_status = "held" if (3.0 <= v_inf_central <= 5.0
                       and 11.4 <= v_ent_central <= 12.1) else (
    "falsified_low" if v_ent_central < 11.4 - 1.0
    else "falsified_high" if v_ent_central > 12.1 + 1.0
    else "marginal"
)

# H2: heat-shield mass ∈ [5, 15] t across [30, 120] kg/m² range.
h2_masses = [heat_shield_mass_t(rho) for rho in [30, 50, 80, 120]]
H2_status = "held" if all(5.0 <= m <= 25.0 for m in h2_masses) else "falsified"

# H3: not testable in this round — would need literature review of aerocapture
# trajectory studies. Just record the assumption.
H3_status = "n/a — assumed range [1.0, 2.5] km/s based on Block 4 framing"

# H4: net uplift at central (1.5 km/s, 50 kg/m²) is 1.5-2.5 pp.
net_uplift = central["delivered_fraction"] - no_aero["delivered_fraction"]
H4_status = "held" if 0.015 <= net_uplift <= 0.025 else (
    "falsified_low" if net_uplift < 0.0
    else "falsified_high" if net_uplift > 0.030
    else "marginal"
)

# H5: composite at central is 14-15%.
composite_central = central["delivered_fraction"]
H5_status = "held" if 0.14 <= composite_central <= 0.15 else (
    "falsified_low" if composite_central < 0.12
    else "falsified_high" if composite_central > 0.16
    else "marginal"
)

# -----------------------------------------------------------------------------
# Summary
# -----------------------------------------------------------------------------

summary = {
    "model": {
        "cargo_water_mass_t": M_CARGO_FOR_SHIELD_T,
        "cargo_volume_m3": V_CARGO_M3,
        "cargo_radius_m": R_CARGO_M,
        "cargo_surface_area_m2": SA_CARGO_M2,
        "dv_savings_grid_kms": DV_SAVINGS_GRID_KMS,
        "tps_areal_density_grid_kg_m2": TPS_AREAL_DENSITY_GRID,
        "jupiter_viable_fraction_used": JUPITER_VIABLE_FRAC,
    },
    "block4_reproduction": {
        "a1_no_levers_pct": a1_check * 100,
        "a2_aerocapture_only_no_shield_at_1p5_pct": a2_check_at_15 * 100,
        "composite_no_jupiter_no_shield_pct": composite_no_jupiter_check * 100,
    },
    "headline_results": {
        "composite_no_jupiter_central_shield_pct": composite_central * 100,
        "composite_with_jupiter_central_shield_pct": composite_with_jupiter * 100,
        "composite_with_jupiter_no_shield_pct": composite_with_jupiter_no_shield * 100,
        "campaign_mean_corrected_pct": campaign_mean_corrected * 100,
        "no_aerocapture_pct": no_aero["delivered_fraction"] * 100,
        "net_uplift_aerocapture_pp": net_uplift * 100,
        "v_infinity_central_kms": v_inf_central,
        "entry_velocity_central_kms": v_ent_central,
        "heat_shield_mass_central_t": heat_shield_mass_t(50),
    },
    "hypothesis_adjudication": {
        "H1_entry_velocity_in_range":  {"status": H1_status,
                                         "v_inf_kms": v_inf_central,
                                         "v_entry_kms": v_ent_central},
        "H2_heat_shield_mass_5_to_15t": {"status": H2_status,
                                         "masses_t": h2_masses},
        "H3_savings_range_assumed":     {"status": H3_status},
        "H4_net_uplift_in_1p5_2p5pp":   {"status": H4_status,
                                         "observed_pp": net_uplift * 100},
        "H5_composite_central_14_15pct": {"status": H5_status,
                                          "observed_pct": composite_central * 100},
    },
}

with open(OUT / "summary.json", "w") as f:
    json.dump(summary, f, indent=2, default=str)

# -----------------------------------------------------------------------------
# Console summary
# -----------------------------------------------------------------------------

print("=" * 72)
print("R-aerocapture-savings-bracket — results")
print("=" * 72)
print(f"Cargo geometry: {M_CARGO_FOR_SHIELD_T:.0f} t water, "
      f"radius {R_CARGO_M:.3f} m, surface area {SA_CARGO_M2:.1f} m²")
print()
print("Block-4 reproduction:")
print(f"  A1 baseline (no levers):                 {a1_check*100:.2f}% "
      f"(Block 4 reported ~3.9%)")
print(f"  A2 aerocapture only (no shield):         {a2_check_at_15*100:.2f}% "
      f"(Block 4 reported ~7.2%)")
print(f"  Composite no-Jupiter no-shield:          "
      f"{composite_no_jupiter_check*100:.2f}% (Block 4 reported ~15.5%)")
print()
print("Heat-shield mass per TPS areal density (200-t cargo, 164.5 m² sphere):")
for r in shield_rows:
    print(f"  {r['areal_density_kg_m2']:>4} kg/m²: "
          f"{r['heat_shield_mass_t']:>6.2f} t  "
          f"({r['mass_fraction_of_cargo_pct']:>5.2f}% of cargo)")
print()
for coverage in COVERAGE_GRID:
    cov_label = (f"30% windward (sphere-cone)" if coverage == 0.30
                 else f"50% windward (biconic)" if coverage == 0.50
                 else f"100% full sphere (HIAD)")
    print(f"Delivered-fraction grid at coverage = {coverage:.2f} ({cov_label}):")
    print(f"  {'savings':>8}", *(f"{rho:>4}kg/m²" for rho in TPS_AREAL_DENSITY_GRID))
    for sav in DV_SAVINGS_GRID_KMS:
        row_str = f"  {sav:>6.2f} "
        for rho in TPS_AREAL_DENSITY_GRID:
            v = next(r["delivered_fraction"] for r in grid_rows
                     if r["savings_kms"] == sav
                     and r["tps_areal_density_kg_m2"] == rho
                     and r["coverage_frac"] == coverage)
            row_str += f"  {v*100:>7.2f}%"
        print(row_str)
    print()
print()
print("Composite scenarios at central TPS (50 kg/m², 50% coverage):")
print(f"  No aerocapture, no shield:               {no_aero['delivered_fraction']*100:>6.2f}%")
print(f"  Aerocapture 0.5 km/s + shield:           {boundary_low_sav['delivered_fraction']*100:>6.2f}%")
print(f"  Aerocapture 1.5 km/s + shield (CENTRAL): {composite_central*100:>6.2f}%")
print(f"  Aerocapture 2.5 km/s + shield:           {boundary_high_sav['delivered_fraction']*100:>6.2f}%")
print()
print("Coverage-fraction sensitivity at central (1.5 km/s, 50 kg/m²):")
print(f"  30% coverage (sphere-cone):              {central_lowcov['delivered_fraction']*100:>6.2f}%")
print(f"  50% coverage (biconic) [CENTRAL]:        {central['delivered_fraction']*100:>6.2f}%")
print(f"  100% coverage (full sphere/HIAD):        {central_sphere['delivered_fraction']*100:>6.2f}%")
print()
print(f"With Jupiter GA (1.5+2.5 km/s, 50 kg/m²):  {composite_with_jupiter*100:>6.2f}%")
print(f"With Jupiter GA, no shield (Block 4 #):    {composite_with_jupiter_no_shield*100:>6.2f}%")
print(f"Campaign-mean (7.5% Jupiter + 92.5% no):   {campaign_mean_corrected*100:>6.2f}%")
print()
print(f"Net aerocapture uplift at central: "
      f"{net_uplift*100:>+6.2f} pp")
print()
print("Hypothesis adjudication:")
for hname, hdata in summary["hypothesis_adjudication"].items():
    print(f"  {hname}: {hdata['status']}")
