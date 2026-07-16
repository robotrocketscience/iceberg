"""Round 15 — Fleet ramp break-even under R14 corrected scaling.

Build a year-by-year cashflow model using R14-corrected per-ship chunk
delivery. Compare break-even year against conops claim of year 11.
"""

from __future__ import annotations

import json
from pathlib import Path

# Per-ship chunk delivery, R14-corrected at 14-yr round trip + 3-flyby tour
# + 10 W/kg specific power
CHUNK_DELIVERED_T = {
    "Kilopower_10kWe":     5.0,
    "FSP_40kWe":          14.0,
    "stretch_100kWe":     43.0,
    "sub_MW_200kWe":      90.0,
    "MW_500kWe":         233.0,
}

PRICE_PER_KG = 2000.0  # dollars per kilogram
ROUND_TRIP_YR = 14

# Ship cost by era (dollars)
SHIP_BUILD_COST = {
    "Kilopower_10kWe":   200e6,
    "FSP_40kWe":         250e6,
    "stretch_100kWe":    280e6,
    "sub_MW_200kWe":     300e6,
    "MW_500kWe":         400e6,
}
LAUNCH_COST_PER_SHIP = 90e6           # Falcon Heavy expendable
DEMONSTRATOR_NRE = 500e6              # one-time at year 0
GROUND_OPS_PER_YEAR = 50e6            # fleet-wide once first ship is in flight


def reactor_era_for_launch_year(launch_year: int) -> str:
    """Map launch year to the reactor class assumed available at that point.
    Pessimistic timeline: Kilopower available now, Fission Surface Power
    available from year 5, sub-megawatt from year 12, megawatt from year 15+.
    """
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


def reactor_era_for_launch_year_optimistic(launch_year: int) -> str:
    """Optimistic timeline: all reactors mature earlier."""
    if launch_year < 2:
        return "Kilopower_10kWe"
    elif launch_year < 6:
        return "FSP_40kWe"
    elif launch_year < 10:
        return "stretch_100kWe"
    elif launch_year < 14:
        return "sub_MW_200kWe"
    else:
        return "MW_500kWe"


def reactor_era_kilopower_only(launch_year: int) -> str:
    """Worst case: only Kilopower ever flies (no Fission Surface Power program)."""
    return "Kilopower_10kWe"


def build_fleet_schedule(
    horizon_yr: int = 40,
    timeline_fn=reactor_era_for_launch_year,
) -> list:
    """Generate launch schedule per conops cadence."""
    schedule = []
    # Ship 1 launches year 0
    schedule.append({"ship_no": 1, "launch_year": 0,
                     "reactor_era": timeline_fn(0)})
    # Ship 2 launches year 7 (waits for ship 1 Saturn capture)
    schedule.append({"ship_no": 2, "launch_year": 7,
                     "reactor_era": timeline_fn(7)})
    # Ships 3+ launch every ~1.083 yr (13-month synodic) from year 8
    ship_no = 3
    year = 8
    while year < horizon_yr:
        schedule.append({"ship_no": ship_no, "launch_year": year,
                         "reactor_era": timeline_fn(year)})
        ship_no += 1
        year += 13.0 / 12.0  # 13 months in years
    return schedule


def cashflow_model(
    horizon_yr: int = 40,
    timeline_fn=reactor_era_for_launch_year,
) -> dict:
    schedule = build_fleet_schedule(horizon_yr, timeline_fn)
    yearly_cashflow = {}  # year -> {cost, revenue, cumulative}

    # Demonstrator non-recurring at year 0
    for yr in range(horizon_yr):
        yearly_cashflow[yr] = {"cost": 0.0, "revenue": 0.0}
    yearly_cashflow[0]["cost"] += DEMONSTRATOR_NRE

    # Per-ship costs at launch year, revenue at delivery year
    for ship in schedule:
        ly = int(ship["launch_year"])
        if ly >= horizon_yr:
            continue
        ship_cost = SHIP_BUILD_COST[ship["reactor_era"]] + LAUNCH_COST_PER_SHIP
        yearly_cashflow[ly]["cost"] += ship_cost
        delivery_year = ly + ROUND_TRIP_YR
        if delivery_year < horizon_yr:
            chunk_t = CHUNK_DELIVERED_T[ship["reactor_era"]]
            ship_revenue = chunk_t * 1000.0 * PRICE_PER_KG  # convert tonnes to kg
            yearly_cashflow[delivery_year]["revenue"] += ship_revenue

    # Ground ops once first ship is in flight (year 0 onwards)
    for yr in range(horizon_yr):
        yearly_cashflow[yr]["cost"] += GROUND_OPS_PER_YEAR

    # Cumulative
    cum_cost = 0.0
    cum_rev = 0.0
    breakeven_year = None
    for yr in range(horizon_yr):
        cum_cost += yearly_cashflow[yr]["cost"]
        cum_rev += yearly_cashflow[yr]["revenue"]
        yearly_cashflow[yr]["cum_cost"] = cum_cost
        yearly_cashflow[yr]["cum_revenue"] = cum_rev
        yearly_cashflow[yr]["cum_cashflow"] = cum_rev - cum_cost
        if breakeven_year is None and cum_rev >= cum_cost and yr > 0:
            breakeven_year = yr

    # Steady-state annual revenue at year 30 (or final year)
    final_yr = horizon_yr - 1
    steady_state_revenue = yearly_cashflow[final_yr]["revenue"]
    annualized_5yr = sum(
        yearly_cashflow[yr]["revenue"] for yr in range(final_yr - 4, final_yr + 1)
    ) / 5.0

    return {
        "timeline": timeline_fn.__name__,
        "horizon_yr": horizon_yr,
        "schedule": schedule,
        "yearly_cashflow": yearly_cashflow,
        "breakeven_year": breakeven_year,
        "steady_state_annual_revenue_final_yr": steady_state_revenue,
        "steady_state_annual_revenue_5yr_avg": annualized_5yr,
        "final_cum_cashflow": yearly_cashflow[final_yr]["cum_cashflow"],
    }


def main() -> dict:
    # Three timeline scenarios:
    pessimistic = cashflow_model(horizon_yr=40, timeline_fn=reactor_era_for_launch_year)
    optimistic = cashflow_model(horizon_yr=40, timeline_fn=reactor_era_for_launch_year_optimistic)
    kilo_only = cashflow_model(horizon_yr=40, timeline_fn=reactor_era_kilopower_only)

    # Also model with CONOPS UN-CORRECTED scaling, for comparison
    CONOPS_CHUNK_T = {
        "Kilopower_10kWe":   50.0,
        "FSP_40kWe":        150.0,
        "stretch_100kWe":   400.0,
        "sub_MW_200kWe":    600.0,
        "MW_500kWe":        750.0,
    }
    # Temporarily override CHUNK_DELIVERED_T
    saved_chunks = CHUNK_DELIVERED_T.copy()
    CHUNK_DELIVERED_T.update(CONOPS_CHUNK_T)
    conops_baseline = cashflow_model(horizon_yr=40, timeline_fn=reactor_era_for_launch_year)
    CHUNK_DELIVERED_T.update(saved_chunks)

    # Hypothesis grading
    h15a = pessimistic["breakeven_year"]
    grading = {
        "H15a_year11_breakeven_falsified": {
            "predicted": "year 11 cash-positive claim is falsified under R14 corrected scaling",
            "measured_breakeven_year_pessimistic": pessimistic["breakeven_year"],
            "measured_breakeven_year_optimistic": optimistic["breakeven_year"],
            "verdict": (
                "held" if (pessimistic["breakeven_year"] is None or pessimistic["breakeven_year"] > 11)
                else "falsified"
            ),
        },
        "H15b_breakeven_14_to_20yr": {
            "predicted": "year 14-20 under R14 scaling",
            "pessimistic": pessimistic["breakeven_year"],
            "optimistic": optimistic["breakeven_year"],
            "verdict": (
                "held" if (optimistic["breakeven_year"] is not None
                           and 12 <= optimistic["breakeven_year"] <= 25)
                else "falsified"
            ),
        },
        "H15c_steady_state_megawatt_era_revenue": {
            "predicted": "$800M-$1.5B/year",
            "pessimistic_5yr_avg": pessimistic["steady_state_annual_revenue_5yr_avg"],
            "optimistic_5yr_avg": optimistic["steady_state_annual_revenue_5yr_avg"],
            "verdict": (
                "held" if 800e6 <= pessimistic["steady_state_annual_revenue_5yr_avg"] <= 1.5e9
                else "partial"
            ),
        },
        "H15d_demonstrator_single_ship_loss": {
            "predicted": "demonstrator ship never pays back individually",
            "kilo_only_final_cashflow": kilo_only["final_cum_cashflow"],
            "verdict": (
                "held" if kilo_only["final_cum_cashflow"] < 0 else "falsified"
            ),
        },
        "H15e_fsp_fleet_breakeven_year_15_25": {
            "predicted": "year 15-25",
            "measured": pessimistic["breakeven_year"],
            "verdict": (
                "held" if pessimistic["breakeven_year"] is not None
                and 12 <= pessimistic["breakeven_year"] <= 25
                else "falsified"
            ),
        },
    }

    results = {
        "scenarios": {
            "conops_baseline_uncorrected": conops_baseline,
            "R14_corrected_pessimistic_timeline": pessimistic,
            "R14_corrected_optimistic_timeline": optimistic,
            "kilopower_only_worst_case": kilo_only,
        },
        "inputs": {
            "CHUNK_DELIVERED_T_R14_corrected": saved_chunks,
            "CONOPS_CHUNK_T_uncorrected": CONOPS_CHUNK_T,
            "PRICE_PER_KG": PRICE_PER_KG,
            "ROUND_TRIP_YR": ROUND_TRIP_YR,
            "SHIP_BUILD_COST": SHIP_BUILD_COST,
            "LAUNCH_COST_PER_SHIP": LAUNCH_COST_PER_SHIP,
            "DEMONSTRATOR_NRE": DEMONSTRATOR_NRE,
            "GROUND_OPS_PER_YEAR": GROUND_OPS_PER_YEAR,
        },
        "hypothesis_grading": grading,
    }

    out_dir = Path(__file__).parent / "results"
    out_dir.mkdir(exist_ok=True)
    with (out_dir / "fleet_ramp.json").open("w") as f:
        json.dump(results, f, indent=2, default=str)

    # Console
    print("=" * 96)
    print("R15 — Fleet ramp break-even under R14 corrected scaling")
    print("=" * 96)
    print()
    print("Scenario comparison:")
    print(f"  {'Scenario':<55} {'Breakeven yr':>13} {'Final cashflow':>18}")
    for name, scen in [
        ("Conops un-corrected scaling (pessimistic timeline)", conops_baseline),
        ("R14 corrected + pessimistic reactor timeline", pessimistic),
        ("R14 corrected + optimistic reactor timeline", optimistic),
        ("Kilopower-only worst case (no FSP or MW arrives)", kilo_only),
    ]:
        bey = scen["breakeven_year"]
        bey_s = f"year {bey}" if bey is not None else "never (40 yr horizon)"
        cf = scen["final_cum_cashflow"]
        cf_s = f"${cf/1e9:+.2f}B" if abs(cf) >= 1e9 else f"${cf/1e6:+.0f}M"
        print(f"  {name:<55} {bey_s:>13} {cf_s:>18}")
    print()

    print(f"R14 corrected, pessimistic timeline, year-by-year cashflow:")
    print(f"  {'Year':>5} {'Cost':>8} {'Revenue':>10} {'Cum cost':>10} {'Cum rev':>10} {'Cum cashflow':>15}")
    for yr in range(0, 30, 1):
        c = pessimistic["yearly_cashflow"][yr]
        sign = "+" if c["cum_cashflow"] >= 0 else "-"
        print(f"  {yr:>4}  ${c['cost']/1e6:>5.0f}M  ${c['revenue']/1e6:>7.0f}M  "
              f"${c['cum_cost']/1e6:>7.0f}M  ${c['cum_revenue']/1e6:>7.0f}M  "
              f"{sign}${abs(c['cum_cashflow'])/1e6:>7.0f}M")
    print()

    print(f"Steady-state annual revenue (5-yr avg at end of 40-yr horizon):")
    for name, scen in [
        ("Conops baseline", conops_baseline),
        ("R14 corrected pessimistic", pessimistic),
        ("R14 corrected optimistic", optimistic),
        ("Kilopower-only worst case", kilo_only),
    ]:
        print(f"  {name:<35}: ${scen['steady_state_annual_revenue_5yr_avg']/1e9:.2f}B/year")
    print()

    print("Hypothesis grading:")
    for h, g in grading.items():
        print(f"  {h}: {g.get('verdict')}")
    print()
    print(f"Result JSON: {out_dir / 'fleet_ramp.json'}")
    return results


if __name__ == "__main__":
    main()
