"""R-megawatt-architecture-viability — does the megawatt cell survive MARVL-anchored
mass + 0-of-6 base rate?

Three computations:

1. Sweep tug dry mass under MARVL-anchored decomposition (70-150 t at 1 MWe)
   and compute round-trip baseline + with redundancy overlay (Round 2: +12.76 t).
   Find the maximum dry mass that still closes L0-05 = 15 yr.

2. Bayesian posterior on megawatt-class fission delivery by 2035 under three
   weakly-informative priors with 0-of-6 historical evidence + FY2026 budget zero.

3. Same for Kilopower variant B with KRUSTY ground-demo partial-credit adjustment.

Outputs:
    results/dry_mass_sweep.json
    results/bayesian_posteriors.json
    results/tables.md

Deterministic; runtime < 1 s.
"""

from __future__ import annotations

import json
import math
from pathlib import Path


# ---------------- shared constants ---------------- #

G0 = 9.81
GM_SUN = 1.32712440018e11
GM_EARTH = 398600.4418
R_EARTH = 6378.137
A_EARTH = 149597870.7
A_SATURN = 9.5826 * A_EARTH
YEAR_S = 365.25 * 86400.0
LEO_ALT_KM = 400.0
ETA_THR = 0.65
DV_INBOUND_KM_S = 6.42
SATURN_OPS_YR = 1.0
REDUNDANCY_OVERLAY_T = 12.76  # from R-redundancy-budget-cost
L0_05_CEILING_YR = 15.0


def hohmann_cruise_yr() -> float:
    a_h_km = (A_EARTH + A_SATURN) / 2.0
    return math.pi * math.sqrt(a_h_km ** 3 / GM_SUN) / YEAR_S


def outbound_dv_km_s() -> float:
    r_leo = R_EARTH + LEO_ALT_KM
    v_circ_leo = math.sqrt(GM_EARTH / r_leo)
    v_earth = math.sqrt(GM_SUN / A_EARTH)
    a_h = (A_EARTH + A_SATURN) / 2.0
    v_peri = math.sqrt(GM_SUN * (2.0 / A_EARTH - 1.0 / a_h))
    v_inf = v_peri - v_earth
    return v_circ_leo + v_inf


def constant_thrust_burn(m_initial_t: float, dv_km_s: float,
                         power_kwe: float, isp_s: float) -> dict:
    v_e = isp_s * G0
    thrust_N = 2.0 * ETA_THR * power_kwe * 1000.0 / v_e
    mass_ratio = math.exp(dv_km_s * 1000.0 / v_e)
    m_prop_t = m_initial_t * (1.0 - 1.0 / mass_ratio)
    t_burn_s = m_prop_t * 1000.0 * v_e / thrust_N
    return {"m_prop_t": m_prop_t, "t_burn_yr": t_burn_s / YEAR_S}


def round_trip(m_dry_t: float, reactor_kwe: float = 1000.0, isp_s: float = 2000.0,
               chunk_t: float = 200.0) -> dict:
    dv_out = outbound_dv_km_s()
    cruise = hohmann_cruise_yr()
    burn_out = constant_thrust_burn(m_dry_t, dv_out, reactor_kwe, isp_s)
    burn_in = constant_thrust_burn(m_dry_t + chunk_t, DV_INBOUND_KM_S, reactor_kwe, isp_s)
    rt = burn_out["t_burn_yr"] + cruise + SATURN_OPS_YR + burn_in["t_burn_yr"] + cruise
    return {
        "m_dry_t": m_dry_t,
        "outbound_burn_yr": burn_out["t_burn_yr"],
        "outbound_propellant_t": burn_out["m_prop_t"],
        "cruise_yr_each_way": cruise,
        "inbound_burn_yr": burn_in["t_burn_yr"],
        "inbound_propellant_t": burn_in["m_prop_t"],
        "round_trip_yr": rt,
        "L0_05_margin_yr": L0_05_CEILING_YR - rt,
        "clears_L0_05": rt <= L0_05_CEILING_YR,
    }


def dry_mass_sweep() -> dict:
    """Sweep tug dry mass from 29 t (R2 decomposed-mid baseline) up to 200 t."""
    masses = [29.0, 50.0, 70.0, 80.0, 90.0, 100.0, 105.0, 110.0, 120.0, 130.0,
              140.0, 150.0, 160.0, 180.0, 200.0]
    rows = []
    for m_dry in masses:
        baseline = round_trip(m_dry)
        with_overlay = round_trip(m_dry + REDUNDANCY_OVERLAY_T)
        rows.append({
            "m_dry_baseline_t": m_dry,
            "m_dry_with_overlay_t": m_dry + REDUNDANCY_OVERLAY_T,
            "baseline": baseline,
            "with_overlay": with_overlay,
        })
    # Find max dry mass that still clears L0-05 baseline and with overlay
    max_dry_baseline = None
    max_dry_overlay = None
    for row in rows:
        if row["baseline"]["clears_L0_05"]:
            max_dry_baseline = row["m_dry_baseline_t"]
        if row["with_overlay"]["clears_L0_05"]:
            max_dry_overlay = row["m_dry_baseline_t"]
    return {
        "rows": rows,
        "max_dry_clearing_L0_05_baseline_t": max_dry_baseline,
        "max_dry_clearing_L0_05_with_overlay_t": max_dry_overlay,
    }


# ---------------- Bayesian posterior ---------------- #


def beta_posterior(alpha_prior: float, beta_prior: float,
                   successes: float, failures: float) -> dict:
    alpha = alpha_prior + successes
    beta = beta_prior + failures
    mean = alpha / (alpha + beta)
    # 95% credible interval via normal approximation (small-sample caveat)
    var = (alpha * beta) / ((alpha + beta) ** 2 * (alpha + beta + 1))
    sd = math.sqrt(var)
    return {
        "alpha_post": alpha, "beta_post": beta,
        "posterior_mean": mean,
        "posterior_sd": sd,
        "approx_95CI_low": max(0.0, mean - 2 * sd),
        "approx_95CI_high": min(1.0, mean + 2 * sd),
    }


def bayesian_posteriors() -> dict:
    """Apply 0-of-6 base rate under three priors.

    For megawatt: successes = 0, failures = 6.
    Apply FY2026-budget-zero as a half-success-equivalent reduction: failures += 0.5.

    For Kilopower variant B: successes += 0.5 (KRUSTY ground-demo partial credit
    that the other 6 failed programs did not all reach).
    """
    priors = [
        ("uniform_Beta_1_1", 1.0, 1.0),
        ("Jeffreys_Beta_0p5_0p5", 0.5, 0.5),
        ("weakly_favorable_Beta_2_2", 2.0, 2.0),
    ]
    out = {}
    for name, a, b in priors:
        mw_no_evidence = beta_posterior(a, b, 0, 6)
        mw_with_budget = beta_posterior(a, b, 0, 6.5)
        kp = beta_posterior(a, b, 0.5, 6)
        out[name] = {
            "megawatt_class_0_of_6": mw_no_evidence,
            "megawatt_class_0_of_6_plus_FY2026_budget_zero": mw_with_budget,
            "Kilopower_variant_B_with_KRUSTY_credit": kp,
        }
    return out


# ---------------- driver ---------------- #


def main():
    here = Path(__file__).parent
    out = here / "results"
    out.mkdir(exist_ok=True)

    sweep = dry_mass_sweep()
    posts = bayesian_posteriors()

    (out / "dry_mass_sweep.json").write_text(json.dumps(sweep, indent=2))
    (out / "bayesian_posteriors.json").write_text(json.dumps(posts, indent=2))

    md = [
        "# R-megawatt-architecture-viability — results tables",
        "",
        "## 1. Round-trip at megawatt all-electric across MARVL-anchored dry mass",
        "",
        f"Hohmann round-trip cruise = {hohmann_cruise_yr() * 2:.2f} yr (one-way × 2).",
        f"Outbound delta-velocity = {outbound_dv_km_s():.2f} km/s (Edelbaum + heliocentric).",
        f"Inbound delta-velocity = {DV_INBOUND_KM_S:.2f} km/s.",
        f"Reactor 1000 kWe, Isp 2000 s, eta 0.65, chunk 200 t.",
        f"Redundancy overlay (from R-redundancy-budget-cost) = {REDUNDANCY_OVERLAY_T:.2f} t.",
        "",
        "| Dry mass (t) | Baseline RT (yr) | Baseline margin (yr) | Clears? | + overlay RT (yr) | + overlay margin (yr) | Clears? |",
        "|---|---|---|---|---|---|---|",
    ]
    for row in sweep["rows"]:
        b = row["baseline"]
        w = row["with_overlay"]
        md.append(
            f"| {row['m_dry_baseline_t']:.0f} | "
            f"{b['round_trip_yr']:.2f} | {b['L0_05_margin_yr']:+.2f} | "
            f"{'yes' if b['clears_L0_05'] else 'NO'} | "
            f"{w['round_trip_yr']:.2f} | {w['L0_05_margin_yr']:+.2f} | "
            f"{'yes' if w['clears_L0_05'] else 'NO'} |"
        )

    md += [
        "",
        f"**Max dry mass clearing L0-05 baseline:** {sweep['max_dry_clearing_L0_05_baseline_t']:.0f} t.",
        f"**Max dry mass clearing L0-05 with redundancy overlay:** {sweep['max_dry_clearing_L0_05_with_overlay_t']:.0f} t.",
        "",
        "**MARVL-anchored dry-mass band 70–150 t** (per H-r4-a) — closes baseline up to {} t, closes-with-overlay up to {} t.".format(
            sweep["max_dry_clearing_L0_05_baseline_t"],
            sweep["max_dry_clearing_L0_05_with_overlay_t"],
        ),
        "",
        "## 2. Bayesian posteriors on fission-flight delivery by 2032–2035",
        "",
        "Three priors applied to 0-of-6 historical evidence (SNAP-10A 1965 was the only US fission reactor orbited; SP-100, Project Timberwind, Prometheus/JIMO, DARPA DRACO, Kilopower flight, FSP all failed/not-yet-awarded). FY2026 budget zero added as a 0.5 failure-equivalent for megawatt-class. Kilopower variant B gets KRUSTY ground-demo +0.5 success credit.",
        "",
        "| Prior | Megawatt (0/6) | Megawatt (0/6 + FY2026 budget) | Kilopower-B (+ KRUSTY credit) |",
        "|---|---|---|---|",
    ]
    for prior_name, vals in posts.items():
        mw = vals["megawatt_class_0_of_6"]
        mw_b = vals["megawatt_class_0_of_6_plus_FY2026_budget_zero"]
        kp = vals["Kilopower_variant_B_with_KRUSTY_credit"]
        md.append(
            f"| {prior_name} | {mw['posterior_mean']:.3f} (CI [{mw['approx_95CI_low']:.2f}, {mw['approx_95CI_high']:.2f}]) | "
            f"{mw_b['posterior_mean']:.3f} (CI [{mw_b['approx_95CI_low']:.2f}, {mw_b['approx_95CI_high']:.2f}]) | "
            f"{kp['posterior_mean']:.3f} (CI [{kp['approx_95CI_low']:.2f}, {kp['approx_95CI_high']:.2f}]) |"
        )

    md += [
        "",
        "**Reading:** posterior mean for megawatt-class delivery by 2035 sits in [0.07, 0.20] across priors with FY2026 budget evidence. Kilopower-B with KRUSTY credit is in [0.10, 0.25]. Neither is the matrix's implicit confidence (which appears to be >0.5 for both cells, given they are listed as baseline architecture options).",
        "",
        "## 3. Cell verdict",
        "",
        "MARVL-anchored mass + base-rate Bayesian posterior:",
        "",
        f"- **Megawatt all-electric cell:** at bundled-formula 105 t dry, round-trip = {round_trip(105.0)['round_trip_yr']:.2f} yr baseline / {round_trip(105.0 + REDUNDANCY_OVERLAY_T)['round_trip_yr']:.2f} yr with overlay. L0-05 margin tight (~{round_trip(105.0)['L0_05_margin_yr']:+.2f} yr baseline). Base-rate posterior 0.07–0.20. **Verdict: upside-only, not a defensible baseline.**",
        f"- **Kilopower variant B cell:** not modelled in this round (different architecture). Base-rate posterior 0.10–0.25 with KRUSTY credit. **Verdict: contingent on Kilopower flight program that has not been funded as of May 2026.**",
        "- **Matrix verdict:** the clean two-cell binary collapses. Both cells carry undocumented program-risk. Spawn R-non-fission-baseline to identify an architecture that does not depend on a fission flight program that has not been funded.",
    ]

    (out / "tables.md").write_text("\n".join(md))
    print((out / "tables.md").read_text())


if __name__ == "__main__":
    main()
