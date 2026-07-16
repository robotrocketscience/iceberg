"""R15-rerun with audited assumptions.

Updates over R15 / R15b:
- Duty cycle 0.7 (Dawn / BepiColombo heritage), not 0.5
- Round-trip ceiling 18 yr (relaxed from 14 yr per audit)
- Per-ship chunk delivery from audit recompute table (duty 0.7, 18-yr ceiling,
  3-flyby tour, water radio-frequency ion thruster)
- Launch + trans-Saturn-injection cost $290M per ship
- Three ship-build-cost scenarios as in R15b
- Pricing premium and sovereign-purchase axes as in R15b
"""

from __future__ import annotations

import json
from pathlib import Path

# Audited per-ship chunk delivery (tonnes), 3-flyby tour, duty 0.7,
# 18-yr round-trip ceiling, water radio-frequency ion thruster, 10 W/kg
# specific power. From R-mid audit recompute.
AUDITED_CHUNK_DELIVERED_T = {
    "Kilopower_10kWe":     7.0,
    "FSP_40kWe":          42.0,
    "stretch_100kWe":    114.0,
    "sub_MW_200kWe":     294.0,
    "MW_500kWe":         588.0,
}

# For comparison: R15 baseline (3-flyby, duty 0.5, 14-yr ceiling)
ORIGINAL_R15_CHUNK_DELIVERED_T = {
    "Kilopower_10kWe":     5.0,
    "FSP_40kWe":          14.0,
    "stretch_100kWe":     43.0,
    "sub_MW_200kWe":      90.0,
    "MW_500kWe":         233.0,
}

ROUND_TRIP_YR = 18  # Audited: relaxed from 14 to 18
LAUNCH_PLUS_TSI = 150e6 + 140e6  # Falcon Heavy expendable + Vulcan-Centaur class
DEMONSTRATOR_NRE = 500e6
GROUND_OPS_PER_YEAR = 50e6


def ship_build_cost_table(scale: str):
    if scale == "conops_optimistic":
        return {"Kilopower_10kWe": 150e6, "FSP_40kWe": 200e6,
                "stretch_100kWe": 250e6, "sub_MW_200kWe": 300e6, "MW_500kWe": 400e6}
    elif scale == "commercial_mid":
        return {"Kilopower_10kWe": 250e6, "FSP_40kWe": 350e6,
                "stretch_100kWe": 450e6, "sub_MW_200kWe": 550e6, "MW_500kWe": 700e6}
    elif scale == "commercial_high":
        return {"Kilopower_10kWe": 400e6, "FSP_40kWe": 600e6,
                "stretch_100kWe": 750e6, "sub_MW_200kWe": 900e6, "MW_500kWe": 1200e6}
    else:
        raise ValueError(scale)


def reactor_era_for_launch_year(launch_year):
    if launch_year < 5:
        return "Kilopower_10kWe"
    elif launch_year < 12:
        return "FSP_40kWe"
    elif launch_year < 15:
        return "stretch_100kWe"
    elif launch_year < 20:
        return "sub_MW_200kWe"
    else:
        return "MW_500kWe"


def build_fleet_schedule(horizon_yr=45):
    schedule = [{"ship_no": 1, "launch_year": 0,
                 "reactor_era": reactor_era_for_launch_year(0)}]
    schedule.append({"ship_no": 2, "launch_year": 7,
                     "reactor_era": reactor_era_for_launch_year(7)})
    ship_no = 3
    year = 8.0
    while year < horizon_yr:
        schedule.append({"ship_no": ship_no, "launch_year": year,
                         "reactor_era": reactor_era_for_launch_year(int(year))})
        ship_no += 1
        year += 13.0 / 12.0
    return schedule


def cashflow_model(
    price_per_kg: float, sovereign_amount: float, sovereign_year: int,
    ship_cost_scale: str, chunk_table, round_trip_yr=ROUND_TRIP_YR,
    horizon_yr: int = 45,
) -> dict:
    schedule = build_fleet_schedule(horizon_yr)
    yearly = {yr: {"cost": 0.0, "revenue": 0.0} for yr in range(horizon_yr)}
    yearly[0]["cost"] += DEMONSTRATOR_NRE
    ship_cost = ship_build_cost_table(ship_cost_scale)

    for ship in schedule:
        ly = int(ship["launch_year"])
        if ly >= horizon_yr:
            continue
        yearly[ly]["cost"] += ship_cost[ship["reactor_era"]] + LAUNCH_PLUS_TSI
        dy = ly + round_trip_yr
        if dy < horizon_yr:
            chunk_t = chunk_table[ship["reactor_era"]]
            yearly[dy]["revenue"] += chunk_t * 1000.0 * price_per_kg

    for yr in range(horizon_yr):
        yearly[yr]["cost"] += GROUND_OPS_PER_YEAR

    if 0 < sovereign_amount and 0 <= sovereign_year < horizon_yr:
        yearly[sovereign_year]["revenue"] += sovereign_amount

    cum_c, cum_r = 0.0, 0.0
    be_year = None
    for yr in range(horizon_yr):
        cum_c += yearly[yr]["cost"]
        cum_r += yearly[yr]["revenue"]
        yearly[yr]["cum_cost"] = cum_c
        yearly[yr]["cum_revenue"] = cum_r
        yearly[yr]["cum_cashflow"] = cum_r - cum_c
        if be_year is None and cum_r >= cum_c and yr > 0:
            be_year = yr

    return {
        "price_per_kg": price_per_kg,
        "sovereign_amount": sovereign_amount,
        "sovereign_year": sovereign_year,
        "ship_cost_scale": ship_cost_scale,
        "round_trip_yr": round_trip_yr,
        "breakeven_year": be_year,
        "final_cum_cashflow": yearly[horizon_yr - 1]["cum_cashflow"],
        "annual_revenue_year_40_45_avg": (
            sum(yearly[yr]["revenue"] for yr in range(40, 45)) / 5.0
        ),
        "yearly": yearly,
    }


def main():
    PRICES = [2000.0, 3000.0, 4000.0, 5000.0, 10000.0]
    SOV_AMTS = [0.0, 1e9, 2e9]
    SOV_YEARS = [11, 15]
    COSTS = ["conops_optimistic", "commercial_mid", "commercial_high"]

    # Audited scenario: duty 0.7, 18-yr ceiling
    audited_cells = []
    for p in PRICES:
        for sa in SOV_AMTS:
            for sy in SOV_YEARS:
                for cs in COSTS:
                    c = cashflow_model(p, sa, sy, cs, AUDITED_CHUNK_DELIVERED_T, 18)
                    c.pop("yearly")  # too big
                    audited_cells.append(c)

    # Original R15 scenario for comparison: duty 0.5, 14-yr ceiling
    original_cells = []
    for p in PRICES:
        for sa in SOV_AMTS:
            for sy in SOV_YEARS:
                for cs in COSTS:
                    c = cashflow_model(p, sa, sy, cs, ORIGINAL_R15_CHUNK_DELIVERED_T, 14)
                    c.pop("yearly")
                    original_cells.append(c)

    def find(cells, p, sa, sy, cs):
        for c in cells:
            if (c["price_per_kg"] == p and c["sovereign_amount"] == sa
                and c["sovereign_year"] == sy and c["ship_cost_scale"] == cs):
                return c
        return None

    print("=" * 96)
    print("R15-rerun — audited assumptions: duty 0.7, 18-yr round trip, 3-flyby tour")
    print("=" * 96)
    print()
    print("Per-ship chunk delivery (audited vs original R15):")
    print(f"  {'Reactor':<22} {'R15 original':>15} {'R15-rerun audited':>20}")
    for era in AUDITED_CHUNK_DELIVERED_T:
        orig = ORIGINAL_R15_CHUNK_DELIVERED_T[era]
        aud = AUDITED_CHUNK_DELIVERED_T[era]
        ratio = aud / orig
        print(f"  {era:<22} {orig:>13.0f} t {aud:>18.0f} t  ({ratio:.1f}x)")
    print()

    print("Break-even year comparison, no sovereign purchase, commercial_mid cost:")
    print(f"  {'$/kg':>6} {'R15 (14yr, 0.5 duty)':>22} {'R15-rerun (18yr, 0.7 duty)':>28}")
    for p in PRICES:
        co = find(original_cells, p, 0, 11, "commercial_mid")
        ca = find(audited_cells, p, 0, 11, "commercial_mid")
        def fmt(c):
            return f"yr {c['breakeven_year']}" if c["breakeven_year"] else "never"
        print(f"  {p:>5.0f}     {fmt(co):>20}    {fmt(ca):>26}")
    print()

    print("Break-even year, $2B sovereign at year 11, commercial_mid cost:")
    print(f"  {'$/kg':>6} {'R15 (14yr, 0.5 duty)':>22} {'R15-rerun (18yr, 0.7 duty)':>28}")
    for p in PRICES:
        co = find(original_cells, p, 2e9, 11, "commercial_mid")
        ca = find(audited_cells, p, 2e9, 11, "commercial_mid")
        def fmt(c):
            return f"yr {c['breakeven_year']}" if c["breakeven_year"] else "never"
        print(f"  {p:>5.0f}     {fmt(co):>20}    {fmt(ca):>26}")
    print()

    print("Steady-state annual revenue at year 40-45 average:")
    print(f"  {'$/kg':>6} {'R15 commercial_mid':>22} {'R15-rerun commercial_mid':>27}")
    for p in PRICES:
        co = find(original_cells, p, 0, 11, "commercial_mid")
        ca = find(audited_cells, p, 0, 11, "commercial_mid")
        print(f"  {p:>5.0f}    ${co['annual_revenue_year_40_45_avg']/1e9:>5.2f}B/yr    "
              f"   ${ca['annual_revenue_year_40_45_avg']/1e9:>5.2f}B/yr")
    print()

    print("Best-case audited cell (commercial_mid cost, $10k/kg, $2B sovereign at year 11):")
    best = find(audited_cells, 10000, 2e9, 11, "commercial_mid")
    print(f"  Break-even: {'year ' + str(best['breakeven_year']) if best['breakeven_year'] else 'never'}")
    print(f"  Final cashflow: ${best['final_cum_cashflow']/1e9:+.2f}B")
    print(f"  Annual revenue at steady state: ${best['annual_revenue_year_40_45_avg']/1e9:.2f}B/year")
    print()

    # Investor-acceptable cells (breakeven <= 25 yr)
    investor_audited = [c for c in audited_cells if c["breakeven_year"] is not None and c["breakeven_year"] <= 25]
    investor_original = [c for c in original_cells if c["breakeven_year"] is not None and c["breakeven_year"] <= 25]
    sovereign_audited = [c for c in audited_cells if c["breakeven_year"] is not None and c["breakeven_year"] <= 35]
    sovereign_original = [c for c in original_cells if c["breakeven_year"] is not None and c["breakeven_year"] <= 35]
    print(f"Investor-acceptable cells (break-even ≤ 25 yr): "
          f"R15 original {len(investor_original)}/{len(original_cells)},  "
          f"R15-rerun audited {len(investor_audited)}/{len(audited_cells)}")
    print(f"Sovereign-acceptable cells (break-even ≤ 35 yr): "
          f"R15 original {len(sovereign_original)}/{len(original_cells)},  "
          f"R15-rerun audited {len(sovereign_audited)}/{len(audited_cells)}")

    out_dir = Path(__file__).parent / "results"
    out_dir.mkdir(exist_ok=True)
    with (out_dir / "rerun.json").open("w") as f:
        json.dump({"audited_cells": audited_cells, "original_cells": original_cells}, f, indent=2, default=str)
    print()
    print(f"Result JSON: {out_dir / 'rerun.json'}")


if __name__ == "__main__":
    main()
