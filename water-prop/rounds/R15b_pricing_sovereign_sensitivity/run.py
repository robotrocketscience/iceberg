"""Round 15b — Pricing premium x sovereign-purchase x ship-cost sensitivity.

Sweeps three axes against R14 corrected per-ship chunk delivery:
- Price per kilogram (2k - 20k)
- Sovereign one-time purchase (0 - 5B at year 11/15/20)
- Ship cost basis (commercial bus pricing $200-800M, vs my R15 $200-400M baseline)

Cost basis rationale: NG MEV / Boeing 702SP / DARPA RSGS commercial
in-space tugs are the right reference, not science-flagship Cassini.
Production-scale ship at Fission Surface Power era is ~$300-500M;
megawatt era scaling pushes to ~$600-800M.
"""

from __future__ import annotations

import json
from pathlib import Path

# R14-corrected chunk delivered (tonnes)
CHUNK_DELIVERED_T = {
    "Kilopower_10kWe":     5.0,
    "FSP_40kWe":          14.0,
    "stretch_100kWe":     43.0,
    "sub_MW_200kWe":      90.0,
    "MW_500kWe":         233.0,
}

ROUND_TRIP_YR = 14
# Launch + trans-Saturn-injection chemical kick stage. Per conops:
# - Falcon Heavy expendable to LEO: ~$150M (commercial SpaceX pricing for FH expendable)
# - Vulcan-Centaur class kick stage doing 7.3 km/s trans-Saturn-injection: ~$140M
# Total per ship: ~$290M. Conops also mentions Impulse Helios as ~$80-120M speculative
# alternative. Using $250M as mid-range commercial baseline.
LAUNCH_COST_PER_SHIP = 150e6      # Falcon Heavy expendable
TSI_KICK_STAGE_COST = 140e6        # Vulcan-Centaur class chemical TSI
LAUNCH_PLUS_TSI = LAUNCH_COST_PER_SHIP + TSI_KICK_STAGE_COST  # = $290M
DEMONSTRATOR_NRE = 500e6
GROUND_OPS_PER_YEAR = 50e6


def ship_build_cost_table(scale: str):
    """Three cost scenarios anchored to commercial-bus-pricing references."""
    if scale == "conops_optimistic":  # ~$150-300M first-of-kind
        return {
            "Kilopower_10kWe":   150e6,
            "FSP_40kWe":         200e6,
            "stretch_100kWe":    250e6,
            "sub_MW_200kWe":     300e6,
            "MW_500kWe":         400e6,
        }
    elif scale == "commercial_mid":   # Boeing 702SP / MEV class scaled up
        return {
            "Kilopower_10kWe":   250e6,
            "FSP_40kWe":         350e6,
            "stretch_100kWe":    450e6,
            "sub_MW_200kWe":     550e6,
            "MW_500kWe":         700e6,
        }
    elif scale == "commercial_high":  # Conservative commercial tug + heavy reactor
        return {
            "Kilopower_10kWe":   400e6,
            "FSP_40kWe":         600e6,
            "stretch_100kWe":    750e6,
            "sub_MW_200kWe":     900e6,
            "MW_500kWe":        1200e6,
        }
    else:
        raise ValueError(f"unknown scale {scale}")


def reactor_era_for_launch_year(launch_year: int) -> str:
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


def build_fleet_schedule(horizon_yr=40):
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
    price_per_kg: float,
    sovereign_amount: float,
    sovereign_year: int,
    ship_cost_scale: str,
    horizon_yr: int = 40,
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
        dy = ly + ROUND_TRIP_YR
        if dy < horizon_yr:
            chunk_t = CHUNK_DELIVERED_T[ship["reactor_era"]]
            yearly[dy]["revenue"] += chunk_t * 1000.0 * price_per_kg

    for yr in range(horizon_yr):
        yearly[yr]["cost"] += GROUND_OPS_PER_YEAR

    # Sovereign one-time strategic purchase (revenue inflow)
    if 0 < sovereign_amount and 0 <= sovereign_year < horizon_yr:
        yearly[sovereign_year]["revenue"] += sovereign_amount

    cum_c = 0.0
    cum_r = 0.0
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
        "breakeven_year": be_year,
        "final_cum_cashflow": yearly[horizon_yr - 1]["cum_cashflow"],
        "annual_revenue_year_36_40_avg": (
            sum(yearly[yr]["revenue"] for yr in range(36, 40)) / 4.0
        ),
    }


def main():
    PRICES = [2000.0, 3000.0, 4000.0, 5000.0, 10000.0, 20000.0]
    SOVEREIGN_AMTS = [0.0, 500e6, 1e9, 2e9, 5e9]
    SOVEREIGN_YEARS = [11, 15, 20]
    COST_SCALES = ["conops_optimistic", "commercial_mid", "commercial_high"]

    cells = []
    for p in PRICES:
        for sa in SOVEREIGN_AMTS:
            for sy in SOVEREIGN_YEARS:
                for cs in COST_SCALES:
                    c = cashflow_model(p, sa, sy, cs)
                    cells.append(c)

    # Find cells that break even within investor horizons (<=25 yr)
    investor_acceptable = [c for c in cells if c["breakeven_year"] is not None
                            and c["breakeven_year"] <= 25]
    # Within 35 yr (sovereign-infrastructure tolerable)
    sovereign_acceptable = [c for c in cells if c["breakeven_year"] is not None
                             and c["breakeven_year"] <= 35]

    # Hypothesis-relevant cells
    def find(p, sa, sy, cs):
        for c in cells:
            if (c["price_per_kg"] == p and c["sovereign_amount"] == sa
                and c["sovereign_year"] == sy and c["ship_cost_scale"] == cs):
                return c
        return None

    grading = {
        "H15b_a_4kkg_no_sov_breakeven_32_38": {
            "predicted": "year 32-38",
            "conops_optimistic_cost": find(4000, 0, 11, "conops_optimistic"),
            "commercial_mid_cost": find(4000, 0, 11, "commercial_mid"),
            "verdict": "to-be-judged",
        },
        "H15b_b_4kkg_plus_1B_sov_y11": {
            "predicted": "year 25-32",
            "conops_optimistic_cost": find(4000, 1e9, 11, "conops_optimistic"),
            "commercial_mid_cost": find(4000, 1e9, 11, "commercial_mid"),
            "verdict": "to-be-judged",
        },
        "H15b_c_5kkg_plus_2B_sov_y11": {
            "predicted": "year 20-26",
            "conops_optimistic_cost": find(5000, 2e9, 11, "conops_optimistic"),
            "commercial_mid_cost": find(5000, 2e9, 11, "commercial_mid"),
            "verdict": "to-be-judged",
        },
        "H15b_d_20kkg_alone": {
            "predicted": "year 18-24",
            "conops_optimistic_cost": find(20000, 0, 11, "conops_optimistic"),
            "commercial_mid_cost": find(20000, 0, 11, "commercial_mid"),
            "verdict": "to-be-judged",
        },
        "H15b_e_2kkg_plus_5B_sov_y11": {
            "predicted": "year 28-35",
            "conops_optimistic_cost": find(2000, 5e9, 11, "conops_optimistic"),
            "commercial_mid_cost": find(2000, 5e9, 11, "commercial_mid"),
            "verdict": "to-be-judged",
        },
    }
    for key, g in grading.items():
        beys = []
        for k in ["conops_optimistic_cost", "commercial_mid_cost"]:
            if g[k] and g[k]["breakeven_year"] is not None:
                beys.append(g[k]["breakeven_year"])
        if not beys:
            g["verdict"] = "never within 40 yr"
        else:
            avg = sum(beys) / len(beys)
            if key == "H15b_a_4kkg_no_sov_breakeven_32_38":
                target_lo, target_hi = 32, 38
            elif key == "H15b_b_4kkg_plus_1B_sov_y11":
                target_lo, target_hi = 25, 32
            elif key == "H15b_c_5kkg_plus_2B_sov_y11":
                target_lo, target_hi = 20, 26
            elif key == "H15b_d_20kkg_alone":
                target_lo, target_hi = 18, 24
            else:
                target_lo, target_hi = 28, 35
            g["verdict"] = "held" if target_lo - 2 <= avg <= target_hi + 2 else "falsified"
            g["mean_breakeven_year"] = avg

    results = {
        "cells": cells,
        "investor_acceptable_25yr": investor_acceptable,
        "sovereign_acceptable_35yr": sovereign_acceptable,
        "hypothesis_grading": grading,
    }

    out_dir = Path(__file__).parent / "results"
    out_dir.mkdir(exist_ok=True)
    with (out_dir / "sensitivity.json").open("w") as f:
        json.dump(results, f, indent=2, default=str)

    # Console
    print("=" * 96)
    print("R15b — Pricing × Sovereign × Ship-cost sensitivity")
    print("=" * 96)
    print()
    print("Cost basis rationale: commercial bus pricing (Boeing 702SP / NG MEV / DARPA RSGS),")
    print("NOT science-flagship Cassini ($3B+). Production-scale ship at FSP era ~$300-500M.")
    print()

    # Headline table: break-even year for (price × cost_scale), no sovereign, at year 11
    print("Break-even year, NO sovereign purchase, conops fleet cadence:")
    print(f"  {'Price $/kg':>12} {'conops_opt':>12} {'commercial_mid':>15} {'commercial_high':>16}")
    for p in PRICES:
        c_o = find(p, 0, 11, "conops_optimistic")
        c_m = find(p, 0, 11, "commercial_mid")
        c_h = find(p, 0, 11, "commercial_high")
        def fmt(c):
            if c["breakeven_year"] is not None:
                return f"yr {c['breakeven_year']}"
            return "never"
        print(f"  {p:>10.0f}   {fmt(c_o):>10}   {fmt(c_m):>13}   {fmt(c_h):>14}")
    print()

    print("Break-even year, $1B sovereign purchase at year 11:")
    print(f"  {'Price $/kg':>12} {'conops_opt':>12} {'commercial_mid':>15} {'commercial_high':>16}")
    for p in PRICES:
        c_o = find(p, 1e9, 11, "conops_optimistic")
        c_m = find(p, 1e9, 11, "commercial_mid")
        c_h = find(p, 1e9, 11, "commercial_high")
        def fmt(c):
            if c["breakeven_year"] is not None:
                return f"yr {c['breakeven_year']}"
            return "never"
        print(f"  {p:>10.0f}   {fmt(c_o):>10}   {fmt(c_m):>13}   {fmt(c_h):>14}")
    print()

    print("Break-even year, $2B sovereign purchase at year 11:")
    print(f"  {'Price $/kg':>12} {'conops_opt':>12} {'commercial_mid':>15} {'commercial_high':>16}")
    for p in PRICES:
        c_o = find(p, 2e9, 11, "conops_optimistic")
        c_m = find(p, 2e9, 11, "commercial_mid")
        c_h = find(p, 2e9, 11, "commercial_high")
        def fmt(c):
            if c["breakeven_year"] is not None:
                return f"yr {c['breakeven_year']}"
            return "never"
        print(f"  {p:>10.0f}   {fmt(c_o):>10}   {fmt(c_m):>13}   {fmt(c_h):>14}")
    print()

    print("Break-even year, $5B sovereign purchase at year 11 (heroic):")
    print(f"  {'Price $/kg':>12} {'conops_opt':>12} {'commercial_mid':>15} {'commercial_high':>16}")
    for p in PRICES:
        c_o = find(p, 5e9, 11, "conops_optimistic")
        c_m = find(p, 5e9, 11, "commercial_mid")
        c_h = find(p, 5e9, 11, "commercial_high")
        def fmt(c):
            if c["breakeven_year"] is not None:
                return f"yr {c['breakeven_year']}"
            return "never"
        print(f"  {p:>10.0f}   {fmt(c_o):>10}   {fmt(c_m):>13}   {fmt(c_h):>14}")
    print()

    print(f"Investor-acceptable cells (break-even ≤ 25 yr): {len(investor_acceptable)} out of {len(cells)}")
    print(f"Sovereign-acceptable cells (break-even ≤ 35 yr): {len(sovereign_acceptable)} out of {len(cells)}")
    print()
    print("Hypothesis grading:")
    for h, g in grading.items():
        v = g.get("verdict", "to-be-judged")
        print(f"  {h}: {v}  (mean breakeven year {g.get('mean_breakeven_year', 'n/a')})")
    print()
    print(f"Result JSON: {out_dir / 'sensitivity.json'}")
    return results


if __name__ == "__main__":
    main()
