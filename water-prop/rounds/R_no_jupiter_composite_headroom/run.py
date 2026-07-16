"""No-Jupiter composite-architecture headroom against Option A's 17 percent.

Extends Block 8's R-aerocapture-savings-bracket Tsiolkovsky framework with six
levers (L1-L6) and three stacks (engineering-credible-only, plus-water-ablator,
all-with-conditionals).

Baseline (reproduces Block 8 central):
- M_collected = 200 t, M_dry_base = 200 t, jettison 20 t
- DV_exit = 7.4 km/s at Isp_exit = 7000 s
- DV_inbound = 24.7 km/s - 1.5 km/s aerocapture = 23.2 km/s at Isp_inbound = 5000 s
- TPS = 50 kg/m^2, 50% windward coverage, carried as inert mass through both burns

Expected baseline: 15.37 percent (within +/-0.05 of Block 8).
"""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass, replace
from math import exp, pi
from pathlib import Path

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------

G0 = 9.80665                            # m/s^2
RHO_WATER_KG_M3 = 1000.0

OUT = Path(__file__).parent / "results"
OUT.mkdir(parents=True, exist_ok=True)


# -----------------------------------------------------------------------------
# Configuration object
# -----------------------------------------------------------------------------

@dataclass(frozen=True)
class Config:
    """Composite-architecture configuration; baseline = Block 8 central."""
    m_collected_t: float = 200.0            # water collected at residence
    m_dry_base_t: float = 200.0             # 500-kWe spacecraft dry mass
    m_jettison_t: float = 20.0              # hardware jettisoned at residence
    dv_exit_kms: float = 7.4
    dv_inbound_kms: float = 24.7
    aero_savings_kms: float = 1.5           # aerocapture velocity savings
    isp_exit_s: float = 7000.0
    isp_inbound_s: float = 5000.0
    tps_areal_density_kg_m2: float = 50.0
    tps_coverage_frac: float = 0.50         # 50% windward biconic
    cargo_density_kg_m3: float = RHO_WATER_KG_M3   # water-bag


def cargo_surface_area_m2(c: Config) -> float:
    """Spherical cargo surface area for TPS sizing."""
    v_m3 = c.m_collected_t * 1000.0 / c.cargo_density_kg_m3
    r_m = (3.0 * v_m3 / (4.0 * pi)) ** (1.0 / 3.0)
    return 4.0 * pi * r_m * r_m


def heat_shield_mass_t(c: Config) -> float:
    return c.tps_coverage_frac * cargo_surface_area_m2(c) * c.tps_areal_density_kg_m2 / 1000.0


def mass_ratio(dv_kms: float, isp_s: float) -> float:
    return exp(dv_kms * 1000.0 / (G0 * isp_s))


def delivered_fraction(c: Config) -> dict:
    """Composite-architecture delivered fraction with all configured levers.

    Heat shield is carried as inert mass through both burns per Block 8 bug-fix.
    """
    dv_in = max(0.0, c.dv_inbound_kms - c.aero_savings_kms)
    m_shield = heat_shield_mass_t(c)
    m_dry_after_jet = c.m_dry_base_t - c.m_jettison_t
    m_dry_total = m_dry_after_jet + m_shield

    m_at_exit = c.m_collected_t + m_dry_total
    mr_exit = mass_ratio(c.dv_exit_kms, c.isp_exit_s)
    m_post_exit = m_at_exit / mr_exit

    mr_inbound = mass_ratio(dv_in, c.isp_inbound_s)
    m_at_earth = m_post_exit / mr_inbound

    m_delivered = max(0.0, m_at_earth - m_dry_total)

    return {
        "m_shield_t":        m_shield,
        "m_dry_total_t":     m_dry_total,
        "m_post_exit_t":     m_post_exit,
        "m_at_earth_t":      m_at_earth,
        "m_delivered_t":     m_delivered,
        "delivered_fraction": m_delivered / c.m_collected_t,
    }


# -----------------------------------------------------------------------------
# Baseline reproduction
# -----------------------------------------------------------------------------

baseline = Config()
b = delivered_fraction(baseline)
baseline_pct = b["delivered_fraction"] * 100.0
print(f"Block 8 baseline reproduction: {baseline_pct:.3f} percent "
      f"(expected ~15.37)")
assert 15.30 <= baseline_pct <= 15.45, (
    f"Block 8 reproduction outside tolerance: {baseline_pct:.3f}"
)


# -----------------------------------------------------------------------------
# Individual levers (each in isolation, all others at Block 8 baseline)
# -----------------------------------------------------------------------------

LEVERS = {
    "L1_tps_coverage_30pct":  replace(baseline, tps_coverage_frac=0.30),
    "L2_water_as_ablator":    replace(baseline, tps_areal_density_kg_m2=0.0),
    "L3_exit_isp_9000":       replace(baseline, isp_exit_s=9000.0),
    "L4_jettison_40t":        replace(baseline, m_jettison_t=40.0),
    "L5_dry_mass_160t":       replace(baseline, m_dry_base_t=160.0),
    "L6_fill_250t":           replace(baseline, m_collected_t=250.0),
}

# Pre-registered ranges for adjudication (in percentage points of uplift).
UPLIFT_PREDICTED_PP = {
    "L1_tps_coverage_30pct":  (0.4, 0.8, 0.1, 1.0),   # held-low, held-high, falsified-low, falsified-high
    "L2_water_as_ablator":    (0.8, 1.2, 0.5, 1.7),
    "L3_exit_isp_9000":       (0.4, 0.8, 0.2, 1.0),
    "L4_jettison_40t":        (0.3, 0.6, 0.1, 0.9),
    "L5_dry_mass_160t":       (0.5, 1.0, 0.3, 1.5),
    "L6_fill_250t":           (0.5, 1.2, 0.0, 2.5),    # H6 uplift in delivered fraction
}

individual_rows = []
individual_results = {}
for name, cfg in LEVERS.items():
    r = delivered_fraction(cfg)
    pct = r["delivered_fraction"] * 100.0
    uplift = pct - baseline_pct
    pred_low, pred_high, fals_low, fals_high = UPLIFT_PREDICTED_PP[name]
    if fals_low <= uplift <= fals_high:
        if pred_low <= uplift <= pred_high:
            status = "held"
        else:
            status = "marginal"
    else:
        status = "falsified_low" if uplift < fals_low else "falsified_high"
    individual_results[name] = {
        "delivered_pct": pct,
        "uplift_pp": uplift,
        "predicted_uplift_pp": [pred_low, pred_high],
        "status": status,
        "m_delivered_t": r["m_delivered_t"],
    }
    individual_rows.append({
        "lever":           name,
        "baseline_pct":    f"{baseline_pct:.3f}",
        "with_lever_pct":  f"{pct:.3f}",
        "uplift_pp":       f"{uplift:+.3f}",
        "predicted_low":   pred_low,
        "predicted_high":  pred_high,
        "status":          status,
        "m_delivered_t":   f"{r['m_delivered_t']:.2f}",
    })


with open(OUT / "lever_individual.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(individual_rows[0].keys()))
    w.writeheader()
    w.writerows(individual_rows)


# -----------------------------------------------------------------------------
# Stacks
# -----------------------------------------------------------------------------

# Honest-floor stack: L1 alone. TPS coverage is geometry-only, no implicit
# conditions; L3 was originally categorised engineering-credible but cathode-
# life bookkeeping (R-cathode-life-water-plasma + Block 4 §validity caveat on
# Isp uplift) shows Isp_exit beyond 7000 s consumes proportionally more cathode
# hours per mission. Re-categorising L3 as conditional surfaces L1 as the only
# truly free lever.
stack_honest_floor = replace(
    baseline,
    tps_coverage_frac=0.30,
)

# H7: engineering-credible-only (L1 + L3). Note: L1 is realism, not an "extra"
# lever — Block 8's full-sphere assumption was conservative. L3 is Isp uplift
# but with the cathode-life caveat surfaced separately.
stack_H7 = replace(
    baseline,
    tps_coverage_frac=0.30,
    isp_exit_s=9000.0,
)

# H8: H7 + water-as-ablator (L2). This zeros TPS mass entirely.
stack_H8 = replace(
    stack_H7,
    tps_areal_density_kg_m2=0.0,
)

# H9: all six levers at their pre-registered ceilings.
stack_H9 = replace(
    baseline,
    tps_coverage_frac=0.30,
    tps_areal_density_kg_m2=0.0,
    isp_exit_s=9000.0,
    m_jettison_t=40.0,
    m_dry_base_t=160.0,
    m_collected_t=250.0,
)

STACKS = {
    "honest_floor_L1_only":                stack_honest_floor,
    "H7_engineering_credible_only_L1_L3":  stack_H7,
    "H8_plus_water_ablator_L1_L2_L3":       stack_H8,
    "H9_all_credible_with_conditionals":    stack_H9,
}

STACK_PREDICTED = {
    "honest_floor_L1_only":                (15.4, 16.0, 15.2, 16.5),
    "H7_engineering_credible_only_L1_L3":  (16.0, 16.8, 15.5, 17.2),
    "H8_plus_water_ablator_L1_L2_L3":       (16.8, 17.4, 16.3, 17.8),
    "H9_all_credible_with_conditionals":    (17.5, 19.5, 16.5, 21.0),
}

stack_rows = []
stack_results = {}
for name, cfg in STACKS.items():
    r = delivered_fraction(cfg)
    pct = r["delivered_fraction"] * 100.0
    pred_low, pred_high, fals_low, fals_high = STACK_PREDICTED[name]
    if fals_low <= pct <= fals_high:
        if pred_low <= pct <= pred_high:
            status = "held"
        else:
            status = "marginal"
    else:
        status = "falsified_low" if pct < fals_low else "falsified_high"
    stack_results[name] = {
        "delivered_pct": pct,
        "predicted_pct": [pred_low, pred_high],
        "status":        status,
        "m_delivered_t": r["m_delivered_t"],
    }
    stack_rows.append({
        "stack":           name,
        "delivered_pct":   f"{pct:.3f}",
        "uplift_vs_baseline_pp": f"{pct - baseline_pct:+.3f}",
        "predicted_low":   pred_low,
        "predicted_high":  pred_high,
        "status":          status,
        "m_delivered_t":   f"{r['m_delivered_t']:.2f}",
        "m_collected_t":   cfg.m_collected_t,
    })


with open(OUT / "lever_stacks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(stack_rows[0].keys()))
    w.writeheader()
    w.writerows(stack_rows)


# -----------------------------------------------------------------------------
# H7 sensitivity sweep (aerocapture saving and TPS areal density)
# -----------------------------------------------------------------------------

sensitivity_rows = []
for aero in [1.0, 1.5, 2.0]:
    for rho in [30.0, 50.0, 80.0]:
        cfg = replace(stack_H7, aero_savings_kms=aero,
                      tps_areal_density_kg_m2=rho)
        r = delivered_fraction(cfg)
        sensitivity_rows.append({
            "aero_savings_kms":   aero,
            "tps_areal_density":  rho,
            "delivered_pct":      f"{r['delivered_fraction']*100:.3f}",
            "m_delivered_t":      f"{r['m_delivered_t']:.2f}",
        })

with open(OUT / "stack_sensitivity.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(sensitivity_rows[0].keys()))
    w.writeheader()
    w.writerows(sensitivity_rows)


# -----------------------------------------------------------------------------
# Architecture claim H10 adjudication
# -----------------------------------------------------------------------------

honest_floor_pct = stack_results["honest_floor_L1_only"]["delivered_pct"]
h7_pct = stack_results["H7_engineering_credible_only_L1_L3"]["delivered_pct"]
h8_pct = stack_results["H8_plus_water_ablator_L1_L2_L3"]["delivered_pct"]
h9_pct = stack_results["H9_all_credible_with_conditionals"]["delivered_pct"]

# H10 says: NO engineering-credible-only stack robustly clears 17%. With L3
# re-categorised as conditional on cathode-life budget (Block 4 caveat surfaced),
# the only truly free lever is L1 (TPS geometry). So H10's adjudication should
# look at honest_floor_pct (L1 only), not at H7 (which embeds the cathode-life-
# conditional L3).
if honest_floor_pct > 17.0:
    h10_status = "falsified"
    h10_note = (
        f"L1-only honest floor at {honest_floor_pct:.2f}% > 17.0; TPS-geometry "
        "realism alone closes the gap. Architecture has genuine remaining "
        "headroom in no-Jupiter case under the strictest accounting."
    )
elif honest_floor_pct < 17.0:
    h10_status = "held"
    h10_note = (
        f"L1-only honest floor at {honest_floor_pct:.2f}% < 17.0. Architecture "
        "is Option-A-equivalent under honest-only accounting; crossing 17% "
        "requires Isp-exit uplift (L3 — cathode-life-conditional), water-as-"
        "ablator (L2 — engineering-validation-pending), or one of the L4/L5/L6 "
        "conditional rounds to close favourably."
    )
else:
    h10_status = "indeterminate"
    h10_note = "Unexpected combination; manual inspection required."


# -----------------------------------------------------------------------------
# Summary JSON
# -----------------------------------------------------------------------------

summary = {
    "baseline": {
        "config": "Block 8 central (1.5 km/s aero, 50 kg/m^2 TPS, 50% coverage, "
                  "Isp_exit 7000 s, Isp_inbound 5000 s, jettison 20 t, "
                  "200 t collected, 200 t dry)",
        "delivered_pct": baseline_pct,
        "expected_from_block8_pct": 15.37,
        "shield_mass_t": b["m_shield_t"],
        "m_delivered_t": b["m_delivered_t"],
    },
    "individual_levers": individual_results,
    "stacks": stack_results,
    "architecture_claim_H10": {
        "status": h10_status,
        "note": h10_note,
        "honest_floor_L1_only_pct": honest_floor_pct,
        "H7_pct": h7_pct,
        "H8_pct": h8_pct,
        "H9_pct": h9_pct,
        "option_a_target_pct": 17.0,
    },
}

with open(OUT / "summary.json", "w") as f:
    json.dump(summary, f, indent=2, default=str)


# -----------------------------------------------------------------------------
# Console summary
# -----------------------------------------------------------------------------

print()
print("=" * 72)
print("R-no-jupiter-composite-headroom -- results")
print("=" * 72)
print(f"Block 8 baseline reproduction: {baseline_pct:.3f} percent "
      f"(Block 8 reported 15.37 percent)")
print(f"  Shield mass: {b['m_shield_t']:.2f} t, delivered: {b['m_delivered_t']:.2f} t")
print()
print("Individual lever uplift vs baseline:")
print(f"  {'lever':<26}  {'pct':>8}  {'uplift':>9}  {'predicted':>14}  status")
for name, r in individual_results.items():
    print(f"  {name:<26}  {r['delivered_pct']:>7.3f}%  "
          f"{r['uplift_pp']:>+8.3f}pp  "
          f"[{r['predicted_uplift_pp'][0]:.2f},{r['predicted_uplift_pp'][1]:.2f}]pp  "
          f"{r['status']}")
print()
print("Stacks vs baseline:")
print(f"  {'stack':<40}  {'pct':>8}  {'predicted':>15}  status")
for name, r in stack_results.items():
    print(f"  {name:<40}  {r['delivered_pct']:>7.3f}%  "
          f"[{r['predicted_pct'][0]:.2f},{r['predicted_pct'][1]:.2f}]%  "
          f"{r['status']}")
print()
print("H10 architecture claim:", h10_status)
print(f"  {h10_note}")
print()
print(f"Option A target: 17.0 percent")
print(f"  Honest floor (L1 only, TPS geometry only):  "
      f"{honest_floor_pct:.2f}%  "
      f"{'>= 17' if honest_floor_pct >= 17 else '< 17'}")
print(f"  H7 (L1 + L3 Isp-uplift, cathode-cond'l):    "
      f"{h7_pct:.2f}%  "
      f"{'>= 17' if h7_pct >= 17 else '< 17'}")
print(f"  H8 (+ L2 water-ablator):                     "
      f"{h8_pct:.2f}%  "
      f"{'>= 17' if h8_pct >= 17 else '< 17'}")
print(f"  H9 (all six levers at credible ceilings):    "
      f"{h9_pct:.2f}%  "
      f"{'>= 17' if h9_pct >= 17 else '< 17'}")
