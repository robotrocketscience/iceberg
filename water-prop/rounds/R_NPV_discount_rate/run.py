"""R-NPV — apply discount rate to ICEBERG cashflow.

Reuses the R15-rerun cashflow model (audited assumptions: duty cycle 0.7,
18-yr round trip, 3-flyby tour, water radio-frequency ion). Adds a discount
rate sweep to compute NPV at year 0:

    NPV = sum_{t=0..H-1} (revenue_t - cost_t) / (1 + r)^t

Sweep: 5 prices x 3 sovereign amounts x 2 sovereign years x 3 ship-cost
scales x 5 discount rates = 450 cells. Output: NPV per cell, plus undiscounted
break-even and final-cumulative-cashflow for cross-check vs R15-rerun.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Reuse R15-rerun cashflow model directly.
RERUN = Path(__file__).resolve().parents[1] / "R15_rerun_audited" / "run.py"
sys.path.insert(0, str(RERUN.parent))
import importlib.util
spec = importlib.util.spec_from_file_location("r15_rerun", RERUN)
r15 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r15)


HORIZON_YR = 45
DISCOUNT_RATES = {
    "sovereign_3pct":      0.03,
    "infrastructure_5pct": 0.05,
    "commercial_8pct":     0.08,
    "growth_10pct":        0.10,
    "venture_15pct":       0.15,
}

PRICES = [2000.0, 3000.0, 4000.0, 5000.0, 10000.0]
SOV_AMTS = [0.0, 1e9, 2e9]
SOV_YEARS = [11, 15]
COSTS = ["conops_optimistic", "commercial_mid", "commercial_high"]


def npv_from_yearly(yearly: dict, rate: float, horizon: int) -> float:
    npv = 0.0
    for t in range(horizon):
        cf = yearly[t]["revenue"] - yearly[t]["cost"]
        npv += cf / ((1.0 + rate) ** t)
    return npv


def perpetuity_terminal_value(yearly: dict, rate: float, horizon: int,
                              growth: float = 0.0) -> float:
    """Gordon-growth terminal value using avg of last 5 years' cashflow."""
    last5 = [yearly[t]["revenue"] - yearly[t]["cost"]
             for t in range(horizon - 5, horizon)]
    cf_terminal = sum(last5) / 5.0
    if cf_terminal <= 0 or rate <= growth:
        return 0.0
    tv_at_horizon = cf_terminal * (1.0 + growth) / (rate - growth)
    return tv_at_horizon / ((1.0 + rate) ** horizon)


def run_cell(price, sov_amt, sov_yr, cost_scale, rate_name, rate):
    cell = r15.cashflow_model(
        price, sov_amt, sov_yr, cost_scale,
        r15.AUDITED_CHUNK_DELIVERED_T,
        round_trip_yr=18, horizon_yr=HORIZON_YR,
    )
    yearly = cell["yearly"]
    npv = npv_from_yearly(yearly, rate, HORIZON_YR)
    tv = perpetuity_terminal_value(yearly, rate, HORIZON_YR, growth=0.0)
    npv_with_tv = npv + tv

    return {
        "price_per_kg": price,
        "sovereign_amount": sov_amt,
        "sovereign_year": sov_yr,
        "ship_cost_scale": cost_scale,
        "discount_rate_name": rate_name,
        "discount_rate": rate,
        "npv": npv,
        "terminal_value_pv": tv,
        "npv_with_terminal": npv_with_tv,
        "undiscounted_breakeven_year": cell["breakeven_year"],
        "undiscounted_final_cumcf": cell["final_cum_cashflow"],
        "ssr_yr40_45_avg": cell["annual_revenue_year_40_45_avg"],
    }


def main():
    cells = []
    for p in PRICES:
        for sa in SOV_AMTS:
            for sy in SOV_YEARS:
                for cs in COSTS:
                    for rn, r in DISCOUNT_RATES.items():
                        cells.append(run_cell(p, sa, sy, cs, rn, r))

    out_dir = Path(__file__).parent / "results"
    out_dir.mkdir(exist_ok=True)
    with (out_dir / "npv_cells.json").open("w") as f:
        json.dump(cells, f, indent=2)

    print("=" * 96)
    print("R-NPV — discount-rate NPV of ICEBERG cashflow (audited assumptions)")
    print("=" * 96)
    print()
    print(f"Horizon: {HORIZON_YR} years.  Total cells: {len(cells)}.")
    print(f"Discount rates: {', '.join(f'{n}={r:.0%}' for n, r in DISCOUNT_RATES.items())}")
    print()

    # H-NPV-a..d: best-case audited cell + conops-baseline cell at each rate
    def find(p, sa, sy, cs, rn):
        for c in cells:
            if (c["price_per_kg"] == p and c["sovereign_amount"] == sa
                and c["sovereign_year"] == sy and c["ship_cost_scale"] == cs
                and c["discount_rate_name"] == rn):
                return c
        return None

    print("Best-case audited cell ($10k/kg + $2B sovereign yr 11 + commercial_mid):")
    print(f"  {'rate':<22} {'NPV ($B)':>12} {'NPV+TV ($B)':>14} {'undisc BE':>12}")
    for rn in DISCOUNT_RATES:
        c = find(10000.0, 2e9, 11, "commercial_mid", rn)
        be = f"yr {c['undiscounted_breakeven_year']}" if c['undiscounted_breakeven_year'] else "never"
        print(f"  {rn:<22} {c['npv']/1e9:>12.2f} {c['npv_with_terminal']/1e9:>14.2f} {be:>12}")
    print()

    print("Conops-baseline cell ($2k/kg + no sovereign + commercial_mid):")
    print(f"  {'rate':<22} {'NPV ($B)':>12} {'NPV+TV ($B)':>14} {'undisc BE':>12}")
    for rn in DISCOUNT_RATES:
        c = find(2000.0, 0.0, 11, "commercial_mid", rn)
        be = f"yr {c['undiscounted_breakeven_year']}" if c['undiscounted_breakeven_year'] else "never"
        print(f"  {rn:<22} {c['npv']/1e9:>12.2f} {c['npv_with_terminal']/1e9:>14.2f} {be:>12}")
    print()

    # H-NPV-e/f/g: positive-NPV cell counts at each rate
    print("Positive-NPV cell counts (out of 90 price x sov x cost cells per rate):")
    print(f"  {'rate':<22} {'NPV>0':>8} {'NPV+TV>0':>10}")
    for rn, r in DISCOUNT_RATES.items():
        rate_cells = [c for c in cells if c["discount_rate_name"] == rn]
        pos = sum(1 for c in rate_cells if c["npv"] > 0)
        pos_tv = sum(1 for c in rate_cells if c["npv_with_terminal"] > 0)
        print(f"  {rn:<22} {pos:>8d} {pos_tv:>10d}")
    print()

    # Hurdle-rate scan: minimum discount rate for each cell to be NPV-positive
    print("Best-case audited cell — break-even discount rate (NPV=0):")
    base = find(10000.0, 2e9, 11, "commercial_mid", "sovereign_3pct")
    yearly = r15.cashflow_model(
        10000.0, 2e9, 11, "commercial_mid",
        r15.AUDITED_CHUNK_DELIVERED_T, 18, HORIZON_YR,
    )["yearly"]
    lo, hi = 0.0, 0.30
    for _ in range(50):
        mid = 0.5 * (lo + hi)
        npv_mid = npv_from_yearly(yearly, mid, HORIZON_YR)
        if npv_mid > 0:
            lo = mid
        else:
            hi = mid
    print(f"  Internal-rate-of-return (no terminal value): {lo*100:.2f}%")
    print()

    # Same with terminal value
    lo, hi = 0.0, 0.30
    for _ in range(50):
        mid = 0.5 * (lo + hi)
        npv_mid = npv_from_yearly(yearly, mid, HORIZON_YR) \
                  + perpetuity_terminal_value(yearly, mid, HORIZON_YR)
        if npv_mid > 0:
            lo = mid
        else:
            hi = mid
    print(f"  Internal-rate-of-return (with perpetuity terminal value, g=0): {lo*100:.2f}%")
    print()

    # Reality-check at 8% across the full price range, no sovereign, commercial_mid
    print("NPV at 8% commercial discount, no sovereign, commercial_mid ship cost:")
    print(f"  {'$/kg':>6} {'NPV ($B)':>12} {'NPV+TV ($B)':>14}")
    for p in PRICES:
        c = find(p, 0.0, 11, "commercial_mid", "commercial_8pct")
        print(f"  {p:>5.0f} {c['npv']/1e9:>12.2f} {c['npv_with_terminal']/1e9:>14.2f}")


if __name__ == "__main__":
    main()
