"""R-reactor-roadmap (second pre-registration) —
   marginal internal-rate-of-return integrated over reactor-arrival distribution.

Inputs:
- R15-rerun cashflow framework (sibling round R15_rerun_audited)
- MARVL-anchored per-ship deliverable mass (R-megawatt-marvl-radiator)
- R-power-base-rate megawatt-class arrival cumulative-distribution-function

Outputs:
- conditional internal-rate-of-return curve as a function of megawatt-arrival-year
- marginal internal-rate-of-return integrated against R-power-base-rate's
  measured cumulative-distribution-function
- aggressive-program counterfactual (median megawatt-arrival = year 10)
- per-claim pre-registration grading vs H-rxr2-a..g
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROUND_DIR = Path(__file__).resolve().parent
WATERPROP_ROUNDS = ROUND_DIR.parent
RESULTS_DIR = ROUND_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)


# ---------------------------------------------------------------------------
# Inputs from upstream rounds (locked at the time of this round).
# ---------------------------------------------------------------------------

# MARVL-anchored per-ship chunk delivery (tonnes) per reactor era.
# Replaces R15-rerun's AUDITED_CHUNK_DELIVERED_T table.
# Justification in STUDY.md "Method" section.
MARVL_CHUNK_DELIVERED_T = {
    "Kilopower_10kWe":               0.0,  # mission fails — chemical-kick floor is 500 kWe
    "FSP_40kWe":                     0.0,  # mission fails — chemical-kick floor is 500 kWe
    "stretch_100kWe":                0.0,
    "sub_MW_200kWe":                 0.0,  # chemical-kick closes at 16.12 yr, exceeds L0-05 ceiling
    "Chemical_kick_500kWe":        128.8,  # R-megawatt-marvl-radiator H-mr-d (14.51-yr round trip)
    "MW_1000kWe":                  128.8,  # held flat — see STUDY.md validity caveat 1
}

# Cashflow constants from R15-rerun (held constant for this round).
LAUNCH_PLUS_TSI = 150e6 + 140e6           # Falcon Heavy expendable + Vulcan-Centaur-class kick
DEMONSTRATOR_NRE = 500e6
GROUND_OPS_PER_YEAR = 50e6
ROUND_TRIP_YR_MARVL = 14.5                # R-megawatt-marvl-radiator chemical-kick architecture closure
HORIZON_YR = 45

# Ship-cost scales (commercial_mid is the central audited case).
SHIP_COST = {
    "Chemical_kick_500kWe": 650e6,        # interpolated between R15-rerun's 550M (sub-MW) and 700M (MW)
    "MW_1000kWe":           700e6,
    # Lower eras kept in dict so cashflow_model can look them up even though
    # delivered chunk is zero — preserves R15-rerun's accounting shape.
    "Kilopower_10kWe":      250e6,
    "FSP_40kWe":            350e6,
    "stretch_100kWe":       450e6,
    "sub_MW_200kWe":        550e6,
}


# ---------------------------------------------------------------------------
# Reactor-era schedule, parameterized by megawatt-arrival year.
# ---------------------------------------------------------------------------

def reactor_era_for_launch_year(launch_year: float, mw_year: float) -> str:
    """Return the highest-class reactor era available at `launch_year`,
    given megawatt-arrival-year `mw_year`. Relative era spacing held constant.

    A non-finite `mw_year` (megawatt-never branch) caps the ladder at the
    500-kilowatt-electric chemical-kick era, which is modeled to arrive at
    year 12 (no-megawatt branch validity caveat 3 in STUDY.md).
    """
    if mw_year == float("inf"):
        kp_year, fsp_year, stretch_year, sub_mw_year, chem500_year = 0, 12 - 13, 12 - 8, 12 - 5, 12
        mw_year_eff = float("inf")
    else:
        kp_year = 0
        fsp_year = mw_year - 13
        stretch_year = mw_year - 8
        sub_mw_year = mw_year - 5
        chem500_year = mw_year - 3
        mw_year_eff = mw_year

    if launch_year >= mw_year_eff:
        return "MW_1000kWe"
    if launch_year >= chem500_year:
        return "Chemical_kick_500kWe"
    if launch_year >= sub_mw_year:
        return "sub_MW_200kWe"
    if launch_year >= stretch_year:
        return "stretch_100kWe"
    if launch_year >= fsp_year:
        return "FSP_40kWe"
    return "Kilopower_10kWe"


def build_fleet_schedule(mw_year: float, horizon_yr: int = HORIZON_YR) -> list[dict]:
    """Same launch cadence as R15-rerun: ship 1 at year 0, ship 2 at year 7,
    then steady-state every 13/12 years until horizon.
    """
    schedule = [{"ship_no": 1, "launch_year": 0.0}]
    schedule.append({"ship_no": 2, "launch_year": 7.0})
    ship_no = 3
    year = 8.0
    while year < horizon_yr:
        schedule.append({"ship_no": ship_no, "launch_year": year})
        ship_no += 1
        year += 13.0 / 12.0
    for ship in schedule:
        ship["reactor_era"] = reactor_era_for_launch_year(ship["launch_year"], mw_year)
    return schedule


# ---------------------------------------------------------------------------
# Cashflow model (adapted from R15-rerun + R-NPV).
# ---------------------------------------------------------------------------

def cashflow_yearly(
    price_per_kg: float,
    sovereign_amount: float,
    sovereign_year: int,
    mw_year: float,
    round_trip_yr: float = ROUND_TRIP_YR_MARVL,
    horizon_yr: int = HORIZON_YR,
) -> dict[int, dict]:
    schedule = build_fleet_schedule(mw_year, horizon_yr)
    yearly = {yr: {"cost": 0.0, "revenue": 0.0} for yr in range(horizon_yr)}
    yearly[0]["cost"] += DEMONSTRATOR_NRE

    for ship in schedule:
        ly = int(ship["launch_year"])
        if ly >= horizon_yr:
            continue
        era = ship["reactor_era"]
        yearly[ly]["cost"] += SHIP_COST[era] + LAUNCH_PLUS_TSI
        dy = ly + int(round(round_trip_yr))
        if dy < horizon_yr:
            chunk_t = MARVL_CHUNK_DELIVERED_T[era]
            yearly[dy]["revenue"] += chunk_t * 1000.0 * price_per_kg

    for yr in range(horizon_yr):
        yearly[yr]["cost"] += GROUND_OPS_PER_YEAR

    if sovereign_amount > 0 and 0 <= sovereign_year < horizon_yr:
        yearly[sovereign_year]["revenue"] += sovereign_amount

    return yearly


def npv(yearly: dict, rate: float, horizon: int = HORIZON_YR) -> float:
    return sum(
        (yearly[t]["revenue"] - yearly[t]["cost"]) / ((1.0 + rate) ** t)
        for t in range(horizon)
    )


def perpetuity_terminal_value(
    yearly: dict, rate: float, horizon: int = HORIZON_YR, growth: float = 0.0
) -> float:
    last5 = [yearly[t]["revenue"] - yearly[t]["cost"]
             for t in range(horizon - 5, horizon)]
    cf_terminal = sum(last5) / 5.0
    if cf_terminal <= 0 or rate <= growth:
        return 0.0
    tv_at_horizon = cf_terminal * (1.0 + growth) / (rate - growth)
    return tv_at_horizon / ((1.0 + rate) ** horizon)


def irr_bisect(yearly: dict, with_tv: bool, horizon: int = HORIZON_YR) -> float | None:
    """Bisect the discount rate for which net-present-value (optionally + perpetuity
    terminal value at growth = 0) equals zero. Returns None if even at a near-zero
    discount rate the discounted value is negative (i.e., bare net-present-value is
    deeply negative and the perpetuity tail cannot rescue it). Returns 0.30 if
    internal-rate-of-return exceeds the search ceiling.

    At rate = 0 with growth = 0 the perpetuity formula has a divide-by-zero, so the
    lower probe is at rate = 1e-4 instead of rate = 0.
    """
    def f(r: float) -> float:
        return npv(yearly, r, horizon) + (perpetuity_terminal_value(yearly, r, horizon) if with_tv else 0.0)

    lo, hi = 1e-4, 0.30
    f_lo, f_hi = f(lo), f(hi)
    if f_lo <= 0:
        return None  # even at near-zero discount the cashflow does not close
    if f_hi > 0:
        return hi  # internal-rate-of-return exceeds 30% — implausibly high for this campaign
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if f(mid) > 0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


# ---------------------------------------------------------------------------
# Conditional and marginal internal-rate-of-return computations.
# ---------------------------------------------------------------------------

# Best-case audited cell, matching R-NPV's H-NPV-anchor cell.
BEST_CELL = {
    "price_per_kg": 10000.0,
    "sovereign_amount": 2e9,
    "sovereign_year": 11,
}
# Conops-baseline cell for cross-check.
CONOPS_BASE = {
    "price_per_kg": 2000.0,
    "sovereign_amount": 0.0,
    "sovereign_year": 11,
}

MW_YEARS = [8, 10, 12, 15, 18, 20, 22, 25, 28, 30, float("inf")]


def conditional_irr_curve(cell: dict, with_tv: bool = True) -> dict:
    out = {}
    for my in MW_YEARS:
        yearly = cashflow_yearly(
            cell["price_per_kg"], cell["sovereign_amount"], cell["sovereign_year"], my
        )
        irr_val = irr_bisect(yearly, with_tv=with_tv)
        out[str(my) if my != float("inf") else "never"] = {
            "mw_year": ("inf" if my == float("inf") else my),
            "irr": irr_val,
            "npv_at_0pct": npv(yearly, 0.0),
            "npv_at_5pct_with_tv": npv(yearly, 0.05) + perpetuity_terminal_value(yearly, 0.05),
            "npv_at_8pct_with_tv": npv(yearly, 0.08) + perpetuity_terminal_value(yearly, 0.08),
        }
    return out


def load_pbr_cdf() -> dict:
    """Load R-power-base-rate megawatt cumulative-distribution-function."""
    path = WATERPROP_ROUNDS / "R_power_base_rate" / "results" / "R_power_base_rate_summary.json"
    with path.open() as f:
        summary = json.load(f)
    return {int(k): float(v) for k, v in summary["mw_cdf_by_year_offset"].items()}


def density_from_cdf(cdf: dict[int, float]) -> dict[int, float]:
    """First-difference the cumulative-distribution-function to recover per-year
    probability density. Domain: year offsets 1..50.
    """
    years = sorted(cdf.keys())
    density = {}
    for i in range(1, len(years)):
        density[years[i]] = max(0.0, cdf[years[i]] - cdf[years[i - 1]])
    # Special: the cumulative-distribution-function has a final-year jump to 1.0
    # (R-power-base-rate censoring artifact). That jump represents "never within
    # 50-year horizon," not "all arrives at year 50." Reassign it to "never."
    p_within_49 = cdf[49]
    p_never = 1.0 - p_within_49
    density[50] = 0.0  # zero out the censoring artifact at year 50
    return density, p_never


def shifted_cdf_aggressive(baseline_cdf: dict[int, float]) -> dict[int, float]:
    """Build aggressive-program counterfactual: shift the megawatt cumulative-distribution-function
    so the median offset drops from 40.8 yr to 10 yr (a 4.08× compression).

    Compression in time -> divide year axis by 4.08. cumulative-distribution-function value
    at year y_new = baseline cumulative-distribution-function at year y_new × 4.08.
    """
    compression = 40.8 / 10.0  # ~4.08
    shifted = {}
    for y in sorted(baseline_cdf.keys()):
        y_baseline = y * compression
        # Linear interpolation on baseline cumulative-distribution-function
        yb_lo = int(y_baseline)
        yb_hi = min(yb_lo + 1, 50)
        frac = y_baseline - yb_lo
        if yb_lo >= 50:
            v = baseline_cdf[49]
        else:
            v = baseline_cdf[yb_lo] * (1 - frac) + baseline_cdf[yb_hi] * frac
        # The final year-50 jump-to-1.0 censoring artifact: re-create at year 50.
        if y == 50:
            shifted[y] = 1.0
        else:
            shifted[y] = v
    return shifted


def marginal_irr(conditional_curve: dict, cdf: dict[int, float]) -> dict:
    """Integrate conditional internal-rate-of-return against the cumulative-distribution-function.
    Treats megawatt-arrival year y as a delta distribution; the never-branch
    catches censoring mass.

    Conditional curve is sparse (megawatt-years in MW_YEARS). For years not in the curve,
    use piecewise-constant interpolation: assign each year to the nearest tested
    megawatt-arrival-year column.
    """
    density, p_never = density_from_cdf(cdf)

    # Map every year offset 1..49 to the nearest tested megawatt-arrival-year in
    # MW_YEARS (excluding 'never').
    tested = sorted([y for y in MW_YEARS if y != float("inf")])
    def nearest(y_int: int) -> int:
        return min(tested, key=lambda t: abs(t - y_int))

    expected_irr = 0.0
    expected_irr_floor_at_zero = 0.0  # treat None internal-rate-of-return as 0% for averaging
    weight_total = 0.0
    for y, p in density.items():
        if y > 49:
            continue
        col = nearest(y)
        irr_at_col = conditional_curve[str(col)]["irr"]
        irr_floored = 0.0 if irr_at_col is None else irr_at_col
        expected_irr += p * irr_floored
        expected_irr_floor_at_zero += p * irr_floored
        weight_total += p

    irr_never = conditional_curve["never"]["irr"]
    irr_never_floored = 0.0 if irr_never is None else irr_never
    expected_irr += p_never * irr_never_floored
    expected_irr_floor_at_zero += p_never * irr_never_floored
    weight_total += p_never

    return {
        "marginal_irr": expected_irr,
        "p_never_branch": p_never,
        "p_megawatt_branch": 1.0 - p_never,
        "total_weight_used": weight_total,
        "irr_never_branch": irr_never,
    }


# ---------------------------------------------------------------------------
# Main entry point.
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 92)
    print("R-reactor-roadmap (second pre-registration) — marginal internal-rate-of-return")
    print("=" * 92)
    print()

    # H-rxr2-a — per-ship chunk delivery at megawatt class under MARVL.
    print("H-rxr2-a (per-ship chunk delivery, megawatt class, MARVL chemical-kick architecture):")
    print(f"  500 kilowatt-electric: {MARVL_CHUNK_DELIVERED_T['Chemical_kick_500kWe']:.1f} t")
    print(f"  1 megawatt-electric:   {MARVL_CHUNK_DELIVERED_T['MW_1000kWe']:.1f} t")
    print("  (vs R15-rerun under decomposed_mid: MW = 588 t — falsified by R-megawatt-marvl-radiator)")
    print()

    # Conditional internal-rate-of-return curves.
    print("Conditional internal-rate-of-return vs megawatt-arrival-year (best-case audited cell, with perpetuity terminal value):")
    best_curve = conditional_irr_curve(BEST_CELL, with_tv=True)
    print(f"  {'megawatt-year':<14} {'internal-rate-of-return':>22}")
    for k, v in best_curve.items():
        irr_str = f"{v['irr'] * 100:.2f}%" if v["irr"] is not None else "n/a (net-present-value < 0 at 0%)"
        print(f"  {k:<14} {irr_str:>22}")
    print()

    print("Conditional internal-rate-of-return vs megawatt-arrival-year (conops-baseline cell, with perpetuity terminal value):")
    conops_curve = conditional_irr_curve(CONOPS_BASE, with_tv=True)
    print(f"  {'megawatt-year':<14} {'internal-rate-of-return':>22}")
    for k, v in conops_curve.items():
        irr_str = f"{v['irr'] * 100:.2f}%" if v["irr"] is not None else "n/a (net-present-value < 0 at 0%)"
        print(f"  {k:<14} {irr_str:>22}")
    print()

    # H-rxr2-e — first year at which conditional internal-rate-of-return crosses 8%.
    print("H-rxr2-e (year at which conditional internal-rate-of-return crosses 8% under MARVL):")
    found = None
    for my in [my for my in MW_YEARS if my != float("inf")]:
        v = best_curve[str(my)]
        if v["irr"] is not None and v["irr"] >= 0.08:
            found = my
            break
    print(f"  best-case audited cell first 8% crossover at megawatt-year = {found}")
    print()

    # H-rxr2-f / H-rxr2-g — marginal internal-rate-of-return integration.
    baseline_cdf = load_pbr_cdf()
    print(f"R-power-base-rate megawatt cumulative-distribution-function: P(megawatt by year 20) = {baseline_cdf[20] * 100:.2f}%, "
          f"P(megawatt by year 30) = {baseline_cdf[30] * 100:.2f}%")
    print()

    print("H-rxr2-f (marginal internal-rate-of-return, baseline R-power-base-rate cumulative-distribution-function):")
    marg = marginal_irr(best_curve, baseline_cdf)
    print(f"  best-case audited cell, marginal internal-rate-of-return = {marg['marginal_irr'] * 100:.2f}%")
    print(f"  P(never-branch) = {marg['p_never_branch'] * 100:.2f}%, "
          f"P(megawatt-branch) = {marg['p_megawatt_branch'] * 100:.2f}%")
    irr_never_str = (
        f"{marg['irr_never_branch'] * 100:.2f}%"
        if marg["irr_never_branch"] is not None
        else "n/a (net-present-value < 0 at 0%)"
    )
    print(f"  Conditional internal-rate-of-return on never-branch = {irr_never_str}")
    print()

    print("H-rxr2-g (marginal internal-rate-of-return uplift from aggressive program — median megawatt-arrival shifted to year 10):")
    aggressive_cdf = shifted_cdf_aggressive(baseline_cdf)
    marg_aggressive = marginal_irr(best_curve, aggressive_cdf)
    uplift_pp = (marg_aggressive["marginal_irr"] - marg["marginal_irr"]) * 100
    print(f"  aggressive median = year 10, "
          f"shifted P(megawatt by year 20) = {aggressive_cdf[20] * 100:.2f}%, "
          f"P(megawatt by year 30) = {aggressive_cdf[30] * 100:.2f}%")
    print(f"  marginal internal-rate-of-return under aggressive program = "
          f"{marg_aggressive['marginal_irr'] * 100:.2f}%")
    print(f"  uplift over baseline = {uplift_pp:+.2f} percentage points")
    print()

    # Persist full record.
    record = {
        "marvl_chunk_delivered_t": MARVL_CHUNK_DELIVERED_T,
        "ship_cost": SHIP_COST,
        "round_trip_yr_marvl": ROUND_TRIP_YR_MARVL,
        "horizon_yr": HORIZON_YR,
        "best_case_cell": BEST_CELL,
        "conops_baseline_cell": CONOPS_BASE,
        "conditional_curve_best": best_curve,
        "conditional_curve_conops": conops_curve,
        "irr_8pct_crossover_megawatt_year": found,
        "baseline_cdf_summary": {
            "p_mw_by_y20": baseline_cdf[20],
            "p_mw_by_y30": baseline_cdf[30],
            "p_mw_by_y49": baseline_cdf[49],
        },
        "marginal_baseline": marg,
        "marginal_aggressive": marg_aggressive,
        "uplift_pp": uplift_pp,
    }
    out_path = RESULTS_DIR / "roadmap.json"
    with out_path.open("w") as f:
        json.dump(record, f, indent=2, default=str)
    print(f"Result JSON: {out_path}")

    # Pre-registration grading.
    print()
    print("Pre-registration grading (H-rxr2):")

    def grade(name: str, measured, lo, hi):
        if measured is None:
            verdict = "n/a"
        elif lo <= measured <= hi:
            verdict = "HELD"
        else:
            verdict = "FALSIFIED"
        meas_str = f"{measured}" if measured is not None else "n/a"
        print(f"  {name:<10} measured={meas_str}  range=[{lo}, {hi}]  -> {verdict}")

    grade("H-rxr2-a", MARVL_CHUNK_DELIVERED_T["MW_1000kWe"], 80, 250)

    def irr_pp(v: dict) -> float | None:
        return v["irr"] * 100 if v["irr"] is not None else None

    grade("H-rxr2-b", irr_pp(best_curve["8"]), 6.5, 8.5)
    grade("H-rxr2-c", irr_pp(best_curve["20"]), 4.0, 6.0)
    grade("H-rxr2-d", irr_pp(best_curve["never"]), 3.0, 5.0)
    grade("H-rxr2-e (8% crossover)", found if found is not None else 0, -1, 5)
    grade("H-rxr2-f", marg["marginal_irr"] * 100, 3.0, 5.0)
    grade("H-rxr2-g", uplift_pp, 0.3, 1.5)


if __name__ == "__main__":
    main()
