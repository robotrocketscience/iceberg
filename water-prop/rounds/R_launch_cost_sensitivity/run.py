"""R-launch-cost-sensitivity — sweep launch+kick cost across reuse scenarios.

Builds on R-conops-phase12-reuse's reuse-aware cashflow framework.
Adds LAUNCH_PLUS_TSI as a primary sweep axis.

Outputs:
- (launch_cost, reuse_scenario, delivery) → IRR
- Hurdle crossovers (launch_cost at which IRR = 4%, 8%, 10%, 15%)
- Pre-registration grading for H-lcs-a..g
"""

from __future__ import annotations

import json
from pathlib import Path

ROUND_DIR = Path(__file__).resolve().parent
RESULTS_DIR = ROUND_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)


# ---------------------------------------------------------------------------
# Constants (from R-reactor-roadmap / R-conops-phase12-reuse; one is now a sweep axis)
# ---------------------------------------------------------------------------

DEMONSTRATOR_NRE = 500e6
GROUND_OPS_PER_YEAR = 50e6
ROUND_TRIP_YR_MARVL = 14.5
HORIZON_YR = 45

SHIP_COST_NEW = 650e6

PRICE_PER_KG = 10000.0
SOVEREIGN_AMOUNT = 2e9
SOVEREIGN_YEAR = 11

DELIVERY_SWEEP_T = [128.8, 200.0, 482.0]
LAUNCH_COST_SWEEP_M = [0, 30, 50, 60, 100, 150, 200, 290]  # millions

REUSE_SCENARIOS = [
    {"name": "single_use_baseline", "reuse_factor": 1, "refurb_cost": 0.0},
    {"name": "reuse_2x_basic_200M",  "reuse_factor": 2, "refurb_cost": 200e6},
    {"name": "reuse_2x_reactor_500M", "reuse_factor": 2, "refurb_cost": 500e6},
    {"name": "reuse_3x_two_reactor_swaps", "reuse_factor": 3, "refurb_cost": 500e6},
    {"name": "reuse_4x_three_reactor_swaps", "reuse_factor": 4, "refurb_cost": 500e6},
]


# ---------------------------------------------------------------------------
# Fleet schedule (copied verbatim from R-conops-phase12-reuse)
# ---------------------------------------------------------------------------

def build_fleet_schedule(horizon_yr: int = HORIZON_YR) -> list[dict]:
    schedule = [{"ship_no": 1, "launch_year": 0.0}]
    schedule.append({"ship_no": 2, "launch_year": 7.0})
    ship_no = 3
    year = 8.0
    while year < horizon_yr:
        schedule.append({"ship_no": ship_no, "launch_year": year})
        ship_no += 1
        year += 13.0 / 12.0
    return schedule


def assign_build_or_refurb(schedule: list[dict], reuse_factor: int) -> list[dict]:
    M = ROUND_TRIP_YR_MARVL
    ships: list[list[float]] = []
    augmented = []
    for launch in schedule:
        ly = launch["launch_year"]
        available = None
        for i, missions in enumerate(ships):
            if (missions[-1] + M) <= ly and len(missions) < reuse_factor:
                available = i
                break
        if available is not None:
            ships[available].append(ly)
            augmented.append({**launch, "kind": "refurb"})
        else:
            ships.append([ly])
            augmented.append({**launch, "kind": "build"})
    return augmented


# ---------------------------------------------------------------------------
# Cashflow (launch-cost-aware)
# ---------------------------------------------------------------------------

def cashflow_yearly(
    delivery_t: float,
    reuse_factor: int,
    refurb_cost: float,
    launch_plus_tsi: float,
    horizon_yr: int = HORIZON_YR,
    demonstrator_nre: float = DEMONSTRATOR_NRE,
    ground_ops: float = GROUND_OPS_PER_YEAR,
) -> dict[int, dict]:
    schedule = assign_build_or_refurb(build_fleet_schedule(horizon_yr), reuse_factor)
    yearly = {yr: {"cost": 0.0, "revenue": 0.0} for yr in range(horizon_yr)}
    yearly[0]["cost"] += demonstrator_nre

    for ship in schedule:
        ly = int(ship["launch_year"])
        if ly >= horizon_yr:
            continue
        if ship["kind"] == "build":
            yearly[ly]["cost"] += SHIP_COST_NEW + launch_plus_tsi
        else:
            yearly[ly]["cost"] += refurb_cost + launch_plus_tsi
        dy = ly + int(round(ROUND_TRIP_YR_MARVL))
        if dy < horizon_yr:
            yearly[dy]["revenue"] += delivery_t * 1000.0 * PRICE_PER_KG

    for yr in range(horizon_yr):
        yearly[yr]["cost"] += ground_ops

    if SOVEREIGN_AMOUNT > 0 and 0 <= SOVEREIGN_YEAR < horizon_yr:
        yearly[SOVEREIGN_YEAR]["revenue"] += SOVEREIGN_AMOUNT

    return yearly


def npv(yearly: dict, rate: float, horizon: int = HORIZON_YR) -> float:
    return sum(
        (yearly[t]["revenue"] - yearly[t]["cost"]) / ((1.0 + rate) ** t)
        for t in range(horizon)
    )


def perpetuity_terminal_value(yearly: dict, rate: float, horizon: int = HORIZON_YR) -> float:
    last5 = [yearly[t]["revenue"] - yearly[t]["cost"] for t in range(horizon - 5, horizon)]
    cf_terminal = sum(last5) / 5.0
    if cf_terminal <= 0 or rate <= 0:
        return 0.0
    return cf_terminal / rate / ((1.0 + rate) ** horizon)


def irr_bisect(yearly: dict, horizon: int = HORIZON_YR) -> float | None:
    def f(r: float) -> float:
        return npv(yearly, r, horizon) + perpetuity_terminal_value(yearly, r, horizon)
    lo, hi = 1e-4, 0.50  # bumped ceiling to 50% since launch=$0 may exceed prior 30% cap
    if f(lo) <= 0:
        return None
    if f(hi) > 0:
        return hi
    for _ in range(70):
        mid = 0.5 * (lo + hi)
        if f(mid) > 0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


# ---------------------------------------------------------------------------
# Hurdle crossover bisection (on launch cost)
# ---------------------------------------------------------------------------

def find_launch_cost_for_irr(
    target_irr: float, delivery_t: float, reuse_factor: int, refurb_cost: float,
    lo_M: float = 0.0, hi_M: float = 500.0,
) -> float | None:
    """Find launch+kick cost (in M$) at which IRR crosses target_irr.
    Lower launch cost -> higher IRR. We seek the largest launch cost giving IRR >= target.
    """
    def irr_at(cost_M: float) -> float:
        y = cashflow_yearly(delivery_t, reuse_factor, refurb_cost, cost_M * 1e6)
        irr = irr_bisect(y)
        return irr if irr is not None else 0.0

    irr_lo = irr_at(lo_M)  # cheapest launch, highest IRR
    irr_hi = irr_at(hi_M)  # most expensive launch, lowest IRR
    if irr_lo < target_irr:
        return None  # even free launches don't reach target
    if irr_hi >= target_irr:
        return hi_M  # even expensive launches clear (saturated)

    for _ in range(40):
        mid = 0.5 * (lo_M + hi_M)
        if irr_at(mid) >= target_irr:
            lo_M = mid
        else:
            hi_M = mid
    return 0.5 * (lo_M + hi_M)


# ---------------------------------------------------------------------------
# Theoretical-max cell (zero fixed costs)
# ---------------------------------------------------------------------------

def theoretical_max_irr(delivery_t: float) -> float | None:
    yearly = cashflow_yearly(
        delivery_t=delivery_t,
        reuse_factor=1,
        refurb_cost=0.0,
        launch_plus_tsi=0.0,
        demonstrator_nre=0.0,
        ground_ops=0.0,
    )
    return irr_bisect(yearly)


# ---------------------------------------------------------------------------
# Main sweep
# ---------------------------------------------------------------------------

def main() -> None:
    rows = []
    for delivery in DELIVERY_SWEEP_T:
        for launch_M in LAUNCH_COST_SWEEP_M:
            for scenario in REUSE_SCENARIOS:
                yearly = cashflow_yearly(
                    delivery_t=delivery,
                    reuse_factor=scenario["reuse_factor"],
                    refurb_cost=scenario["refurb_cost"],
                    launch_plus_tsi=launch_M * 1e6,
                )
                irr = irr_bisect(yearly)
                rows.append({
                    "delivery_t": delivery,
                    "launch_cost_M": launch_M,
                    "scenario": scenario["name"],
                    "reuse_factor": scenario["reuse_factor"],
                    "refurb_cost_M": scenario["refurb_cost"] / 1e6,
                    "irr": irr,
                    "irr_pct": round(irr * 100, 2) if irr else None,
                })

    # Hurdle crossover bisection for single-use baseline
    crossovers = {}
    for delivery in DELIVERY_SWEEP_T:
        crossovers[str(delivery)] = {}
        for target_irr, target_name in [(0.04, "sovereign_bond_4pct"), (0.08, "regulated_utility_8pct"),
                                          (0.10, "corporate_growth_10pct"), (0.15, "venture_class_15pct")]:
            launch_at_crossover = find_launch_cost_for_irr(target_irr, delivery, 1, 0.0)
            crossovers[str(delivery)][target_name] = launch_at_crossover

    # Theoretical max (zero fixed costs)
    theoretical = {str(d): {"irr_pct": round(theoretical_max_irr(d) * 100, 2)
                            if theoretical_max_irr(d) else None}
                   for d in DELIVERY_SWEEP_T}

    # Pre-registration grading
    grading = grade_predictions(rows, crossovers, theoretical)

    result = {
        "rows": rows,
        "crossovers": crossovers,
        "theoretical_max": theoretical,
        "grading": grading,
        "constants": {
            "ship_cost_new_M": SHIP_COST_NEW / 1e6,
            "round_trip_yr": ROUND_TRIP_YR_MARVL,
            "horizon_yr": HORIZON_YR,
            "price_per_kg": PRICE_PER_KG,
            "sovereign_amount_M": SOVEREIGN_AMOUNT / 1e6,
            "sovereign_year": SOVEREIGN_YEAR,
            "demonstrator_nre_M": DEMONSTRATOR_NRE / 1e6,
            "ground_ops_per_yr_M": GROUND_OPS_PER_YEAR / 1e6,
        },
    }

    out_path = RESULTS_DIR / "launch_cost_sensitivity.json"
    with out_path.open("w") as f:
        json.dump(result, f, indent=2)

    # Console: single-use table across launch costs, all deliveries
    print("\nSINGLE-USE IRR ACROSS LAUNCH COSTS\n")
    print(f"{'Launch+TSI ($M)':>17}  {'128.8 t':>10}  {'200 t':>10}  {'482 t':>10}")
    for launch_M in LAUNCH_COST_SWEEP_M:
        line = f"{launch_M:>17}  "
        for d in DELIVERY_SWEEP_T:
            r = next(x for x in rows if x["delivery_t"] == d and x["launch_cost_M"] == launch_M
                                     and x["scenario"] == "single_use_baseline")
            line += f"{r['irr_pct']:>9.2f}%  " if r["irr"] is not None else "    None  "
        print(line)

    # Console: reuse uplift at delivery=200 across launch costs
    print("\nIRR UPLIFT FROM 2x BASIC-REFURB REUSE (delivery = 200 t/ship)\n")
    print(f"{'Launch+TSI ($M)':>17}  {'single-use':>11}  {'2x basic':>10}  {'uplift':>9}")
    for launch_M in LAUNCH_COST_SWEEP_M:
        r_base = next(x for x in rows if x["delivery_t"] == 200.0 and x["launch_cost_M"] == launch_M
                                       and x["scenario"] == "single_use_baseline")
        r_reuse = next(x for x in rows if x["delivery_t"] == 200.0 and x["launch_cost_M"] == launch_M
                                        and x["scenario"] == "reuse_2x_basic_200M")
        uplift = r_reuse["irr_pct"] - r_base["irr_pct"]
        print(f"{launch_M:>17}  {r_base['irr_pct']:>10.2f}%  {r_reuse['irr_pct']:>9.2f}%  {uplift:>+8.2f}pp")

    # Console: hurdle crossovers
    print("\nLAUNCH-COST AT WHICH SINGLE-USE IRR CROSSES HURDLE\n")
    print(f"{'Delivery (t)':>13}  {'4% sovereign':>14}  {'8% reg-util':>13}  {'10% corp-growth':>16}  {'15% venture':>13}")
    for d in DELIVERY_SWEEP_T:
        c = crossovers[str(d)]
        def fmt(x):
            if x is None:
                return "  unreachable"
            elif x >= 500:
                return f"  >${x:.0f}M (sat)"
            return f"  ${x:.0f}M"
        print(f"{d:>13.1f}  {fmt(c['sovereign_bond_4pct']):>14}  {fmt(c['regulated_utility_8pct']):>13}  {fmt(c['corporate_growth_10pct']):>16}  {fmt(c['venture_class_15pct']):>13}")

    print("\nTHEORETICAL MAX IRR (zero launch + ground-ops + demonstrator NRE)\n")
    for d in DELIVERY_SWEEP_T:
        print(f"  {d:.1f} t/ship: {theoretical[str(d)]['irr_pct']:.2f}%")

    print("\nPre-registration grading:")
    for hid, g in grading.items():
        print(f"  {hid}: {g['verdict']:<25} — {g['note']}")


# ---------------------------------------------------------------------------
# Pre-registration grading
# ---------------------------------------------------------------------------

def grade_predictions(rows: list[dict], crossovers: dict, theoretical: dict) -> dict:
    out = {}

    def find(scenario, delivery, launch_M):
        return next((r for r in rows if r["scenario"] == scenario
                     and r["delivery_t"] == delivery and r["launch_cost_M"] == launch_M), None)

    def grade_range(obs, pred_lo, pred_hi, fals_lo, fals_hi, units=""):
        if pred_lo <= obs <= pred_hi:
            return "held"
        if fals_lo <= obs <= fals_hi:
            return "wrong-but-informative"
        return "wrong-and-load-bearing"

    # H-lcs-a: single-use at delivery=200, launch=$50M, IRR ∈ [10, 13]
    r = find("single_use_baseline", 200.0, 50)
    obs = r["irr_pct"]
    v = grade_range(obs, 10, 13, 8.5, 14.5)
    out["H-lcs-a"] = {"observed_pct": obs, "predicted_pct": [10, 13], "verdict": v,
                       "note": f"single-use at 200 t/ship, $50M launch: {obs:.2f}%"}

    # H-lcs-b: single-use at delivery=200, launch=$150M, IRR ∈ [7.5, 9.5]
    r = find("single_use_baseline", 200.0, 150)
    obs = r["irr_pct"]
    v = grade_range(obs, 7.5, 9.5, 6.0, 11.0)
    out["H-lcs-b"] = {"observed_pct": obs, "predicted_pct": [7.5, 9.5], "verdict": v,
                       "note": f"single-use at 200 t/ship, $150M launch: {obs:.2f}%"}

    # H-lcs-c: 2x basic uplift at delivery=200, launch=$50M ∈ [1.0, 1.5] pp
    r_base = find("single_use_baseline", 200.0, 50)
    r_reuse = find("reuse_2x_basic_200M", 200.0, 50)
    obs = r_reuse["irr_pct"] - r_base["irr_pct"]
    v = grade_range(obs, 1.0, 1.5, 0.5, 2.0)
    out["H-lcs-c"] = {"observed_pp": round(obs, 3), "predicted_pp": [1.0, 1.5], "verdict": v,
                       "note": f"2x basic reuse uplift at 200 t/ship, $50M launch: +{obs:.2f}pp"}

    # H-lcs-d: launch threshold for IRR=10% at delivery=200 ∈ [$30, $80]
    threshold = crossovers["200.0"]["corporate_growth_10pct"]
    if threshold is None:
        v = "wrong-and-load-bearing"
        note = "unreachable even at free launches"
        obs_val = None
    else:
        obs_val = threshold
        v = grade_range(threshold, 30, 80, 0, 150)
        note = f"launch cost at 10% crossover, 200 t/ship: ${threshold:.0f}M"
    out["H-lcs-d"] = {"observed_M": obs_val, "predicted_M": [30, 80], "verdict": v, "note": note}

    # H-lcs-e: launch-cost uplift from $290M to $50M at delivery=200 ∈ [4.5, 6.0] pp
    r_high = find("single_use_baseline", 200.0, 290)
    r_low = find("single_use_baseline", 200.0, 50)
    obs = r_low["irr_pct"] - r_high["irr_pct"]
    v = grade_range(obs, 4.5, 6.0, 3.0, 7.5)
    out["H-lcs-e"] = {"observed_pp": round(obs, 3), "predicted_pp": [4.5, 6.0], "verdict": v,
                       "note": f"launch-cost uplift $290M→$50M at 200 t/ship: +{obs:.2f}pp"}

    # H-lcs-f: at delivery=482, launch=$50M, single-use IRR ∈ [14, 18]
    r = find("single_use_baseline", 482.0, 50)
    obs = r["irr_pct"]
    held = 14 <= obs <= 18
    v = "held" if held else ("wrong-but-informative" if 12 <= obs <= 20 else "wrong-and-load-bearing")
    out["H-lcs-f"] = {"observed_pct": obs, "predicted_pct": [14, 18], "verdict": v,
                       "note": f"single-use at 482 t/ship, $50M launch: {obs:.2f}% (target: cross 15% venture-class)"}

    # H-lcs-g: theoretical max at delivery=200 < 20%
    theo = theoretical["200.0"]["irr_pct"]
    held = theo is not None and theo < 20.0
    v = "held" if held else "falsified"
    out["H-lcs-g"] = {"theoretical_max_pct": theo, "predicted_below": 20.0, "verdict": v,
                       "note": f"theoretical max (zero fixed cost) at 200 t/ship: {theo:.2f}% (predicted < 20%)"}

    return out


if __name__ == "__main__":
    main()
