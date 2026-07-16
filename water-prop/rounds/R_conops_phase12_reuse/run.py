"""R-conops-phase12-reuse — does deep-space-vehicle reuse change the marginal-IRR picture?

Reuses R-reactor-roadmap's cashflow framework with one modification: per-launch
ship cost depends on whether the ship is new (full SHIP_COST) or refurbished
(REFURB_COST). Refurbishments occur every N missions for reuse-factor N.

Outputs:
- Per-(reuse, refurb_cost, delivery) IRR
- Uplift vs single-use baseline
- Pre-registration grading for H-ph12-a..g
"""

from __future__ import annotations

import json
from pathlib import Path

ROUND_DIR = Path(__file__).resolve().parent
RESULTS_DIR = ROUND_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)


# ---------------------------------------------------------------------------
# Constants (copied from R_reactor_roadmap/run.py, held identical)
# ---------------------------------------------------------------------------

LAUNCH_PLUS_TSI = 150e6 + 140e6
DEMONSTRATOR_NRE = 500e6
GROUND_OPS_PER_YEAR = 50e6
ROUND_TRIP_YR_MARVL = 14.5
HORIZON_YR = 45

SHIP_COST_NEW = 650e6          # Chemical_kick_500kWe new-build cost (R-reactor-roadmap)

# Best-case audited cell from R-NPV / R-reactor-roadmap.
PRICE_PER_KG = 10000.0
SOVEREIGN_AMOUNT = 2e9
SOVEREIGN_YEAR = 11

# Delivery sweep (R-delivery-irr-curve points of interest).
DELIVERY_SWEEP_T = [128.8, 200.0, 482.0]

# Reuse scenarios:
#   R = reuse factor (1 = single-use baseline; 2 = ship does 2 missions, etc.)
#   refurb_cost = cost billed between missions of the same ship
REUSE_SCENARIOS = [
    {"name": "single_use_baseline", "reuse_factor": 1, "refurb_cost": 0.0},
    {"name": "reuse_2x_basic_200M",  "reuse_factor": 2, "refurb_cost": 200e6},
    {"name": "reuse_2x_reactor_500M", "reuse_factor": 2, "refurb_cost": 500e6},
    {"name": "reuse_3x_two_reactor_swaps", "reuse_factor": 3, "refurb_cost": 500e6},
    {"name": "reuse_4x_three_reactor_swaps", "reuse_factor": 4, "refurb_cost": 500e6},
]


# ---------------------------------------------------------------------------
# Fleet schedule (matches R-reactor-roadmap; mw_year=inf branch — chemical-kick fleet only).
# ---------------------------------------------------------------------------

def build_fleet_schedule(horizon_yr: int = HORIZON_YR) -> list[dict]:
    """Same cadence as R-reactor-roadmap mw_year=inf branch: every 13/12 yr after year 7."""
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
    """For each launch in the schedule, decide whether the ship is new or refurbished.

    Ship lifecycle: built at year y0, missions at y0, y0+M, y0+2M, ..., y0+(R-1)*M.
    Between missions: refurbishment (charged at the mission-start year).

    Greedy assignment: first available retired/just-returned ship is reused;
    otherwise a new ship is built. With deterministic launch cadence and constant
    M = ROUND_TRIP_YR_MARVL, this produces a simple steady-state mix.
    """
    M = ROUND_TRIP_YR_MARVL  # mission duration (round trip)
    # Track each existing ship: list of mission years it has flown
    ships: list[list[float]] = []
    augmented = []

    for launch in schedule:
        ly = launch["launch_year"]
        # Find a ship whose last mission completed by ly and has remaining reuses
        available = None
        for i, missions in enumerate(ships):
            last_mission_year = missions[-1]
            if (last_mission_year + M) <= ly and len(missions) < reuse_factor:
                available = i
                break
        if available is not None:
            ships[available].append(ly)
            mission_index = len(ships[available])  # 2 = second mission, etc.
            augmented.append({**launch, "kind": "refurb", "mission_index": mission_index})
        else:
            ships.append([ly])
            augmented.append({**launch, "kind": "build", "mission_index": 1})
    return augmented


# ---------------------------------------------------------------------------
# Cashflow (reuse-aware).
# ---------------------------------------------------------------------------

def cashflow_yearly(
    delivery_t: float,
    reuse_factor: int,
    refurb_cost: float,
    horizon_yr: int = HORIZON_YR,
) -> dict[int, dict]:
    schedule = assign_build_or_refurb(build_fleet_schedule(horizon_yr), reuse_factor)
    yearly = {yr: {"cost": 0.0, "revenue": 0.0} for yr in range(horizon_yr)}
    yearly[0]["cost"] += DEMONSTRATOR_NRE

    for ship in schedule:
        ly = int(ship["launch_year"])
        if ly >= horizon_yr:
            continue
        # Build or refurbish cost at launch year
        if ship["kind"] == "build":
            yearly[ly]["cost"] += SHIP_COST_NEW + LAUNCH_PLUS_TSI
        else:
            yearly[ly]["cost"] += refurb_cost + LAUNCH_PLUS_TSI
        # Delivery revenue at launch + round-trip
        dy = ly + int(round(ROUND_TRIP_YR_MARVL))
        if dy < horizon_yr:
            yearly[dy]["revenue"] += delivery_t * 1000.0 * PRICE_PER_KG

    for yr in range(horizon_yr):
        yearly[yr]["cost"] += GROUND_OPS_PER_YEAR

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

    lo, hi = 1e-4, 0.30
    f_lo, f_hi = f(lo), f(hi)
    if f_lo <= 0:
        return None
    if f_hi > 0:
        return hi
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if f(mid) > 0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


# ---------------------------------------------------------------------------
# Diagnostic: capex per mission across the fleet schedule
# ---------------------------------------------------------------------------

def capex_per_mission(reuse_factor: int, refurb_cost: float) -> dict:
    schedule = assign_build_or_refurb(build_fleet_schedule(), reuse_factor)
    in_horizon = [s for s in schedule if s["launch_year"] < HORIZON_YR]
    n_missions = len(in_horizon)
    n_builds = sum(1 for s in in_horizon if s["kind"] == "build")
    n_refurbs = sum(1 for s in in_horizon if s["kind"] == "refurb")
    total_capex = n_builds * SHIP_COST_NEW + n_refurbs * refurb_cost
    return {
        "n_missions": n_missions,
        "n_builds": n_builds,
        "n_refurbs": n_refurbs,
        "total_ship_capex": total_capex,
        "avg_capex_per_mission": total_capex / max(1, n_missions),
    }


# ---------------------------------------------------------------------------
# Main sweep
# ---------------------------------------------------------------------------

def main() -> None:
    rows = []
    for delivery in DELIVERY_SWEEP_T:
        for scenario in REUSE_SCENARIOS:
            yearly = cashflow_yearly(
                delivery_t=delivery,
                reuse_factor=scenario["reuse_factor"],
                refurb_cost=scenario["refurb_cost"],
            )
            irr = irr_bisect(yearly)
            capex = capex_per_mission(scenario["reuse_factor"], scenario["refurb_cost"])
            rows.append({
                "scenario": scenario["name"],
                "reuse_factor": scenario["reuse_factor"],
                "refurb_cost_M": scenario["refurb_cost"] / 1e6,
                "delivery_t": delivery,
                "irr": irr,
                "capex_per_mission_M": capex["avg_capex_per_mission"] / 1e6,
                "n_builds": capex["n_builds"],
                "n_refurbs": capex["n_refurbs"],
                "n_missions": capex["n_missions"],
            })

    # Compute uplifts vs single-use baseline at same delivery
    baseline_by_delivery = {
        r["delivery_t"]: r for r in rows if r["scenario"] == "single_use_baseline"
    }
    for r in rows:
        b = baseline_by_delivery[r["delivery_t"]]
        r["irr_uplift_pp"] = None if (r["irr"] is None or b["irr"] is None) else (r["irr"] - b["irr"]) * 100
        r["capex_reduction_pct"] = (
            (1 - r["capex_per_mission_M"] / b["capex_per_mission_M"]) * 100
            if b["capex_per_mission_M"] > 0 else None
        )

    # Pre-registration grading
    grading = grade_predictions(rows)

    result = {
        "rows": rows,
        "grading": grading,
        "constants": {
            "ship_cost_new_M": SHIP_COST_NEW / 1e6,
            "round_trip_yr": ROUND_TRIP_YR_MARVL,
            "horizon_yr": HORIZON_YR,
            "price_per_kg": PRICE_PER_KG,
            "sovereign_amount_M": SOVEREIGN_AMOUNT / 1e6,
            "sovereign_year": SOVEREIGN_YEAR,
        },
    }

    out_path = RESULTS_DIR / "reuse_sweep.json"
    with out_path.open("w") as f:
        json.dump(result, f, indent=2)

    # Console summary
    print(f"{'scenario':<32} {'delivery':>8} {'IRR':>8} {'uplift':>8} {'capex/M':>10} {'cap_red':>8}")
    print("-" * 80)
    for r in rows:
        irr_s = f"{r['irr']*100:.2f}%" if r['irr'] is not None else "  None"
        uplift_s = f"{r['irr_uplift_pp']:+.2f}pp" if r['irr_uplift_pp'] is not None else "   N/A"
        red_s = f"{r['capex_reduction_pct']:+.1f}%" if r['capex_reduction_pct'] is not None else "  N/A"
        print(f"{r['scenario']:<32} {r['delivery_t']:>8.1f} {irr_s:>8} {uplift_s:>8} ${r['capex_per_mission_M']:>7.0f}M  {red_s:>8}")

    print("\nPre-registration grading:")
    for hid, g in grading.items():
        print(f"  {hid}: {g['verdict']:<12} — {g['note']}")


# ---------------------------------------------------------------------------
# Pre-registration grading
# ---------------------------------------------------------------------------

def grade_predictions(rows: list[dict]) -> dict:
    out = {}

    def find(scenario, delivery):
        return next((r for r in rows if r["scenario"] == scenario and r["delivery_t"] == delivery), None)

    # H-ph12-a: 2x reuse + basic refurb, capex reduction at delivery=128.8 (representative)
    r = find("reuse_2x_basic_200M", 128.8)
    pred_lo, pred_hi = 35, 45
    fals_lo, fals_hi = 30, 50
    obs = r["capex_reduction_pct"]
    verdict = (
        "held" if pred_lo <= obs <= pred_hi else
        "wrong-but-informative" if fals_lo <= obs <= fals_hi else
        "wrong-and-load-bearing"
    )
    out["H-ph12-a"] = {"observed_pct": round(obs, 2), "predicted_pct": [pred_lo, pred_hi], "verdict": verdict,
                       "note": f"2x reuse + $200M basic refurb: capex {obs:.1f}% lower"}

    # H-ph12-b: 2x reuse + $500M reactor-replacement refurb
    r = find("reuse_2x_reactor_500M", 128.8)
    pred_lo, pred_hi = 10, 25
    fals_lo, fals_hi = 5, 30
    obs = r["capex_reduction_pct"]
    verdict = (
        "held" if pred_lo <= obs <= pred_hi else
        "wrong-but-informative" if fals_lo <= obs <= fals_hi else
        "wrong-and-load-bearing"
    )
    out["H-ph12-b"] = {"observed_pct": round(obs, 2), "predicted_pct": [pred_lo, pred_hi], "verdict": verdict,
                       "note": f"2x reuse + $500M reactor-swap: capex {obs:.1f}% lower"}

    # H-ph12-c: 2x reuse + reactor-replacement uplift at delivery=200
    r = find("reuse_2x_reactor_500M", 200.0)
    obs = r["irr_uplift_pp"]
    pred_lo, pred_hi = 0.6, 1.4
    verdict = (
        "held" if pred_lo <= obs <= pred_hi else
        "wrong-but-informative" if abs(obs - (pred_lo+pred_hi)/2) <= 1.0 else
        "wrong-and-load-bearing"
    )
    out["H-ph12-c"] = {"observed_pp": round(obs, 3), "predicted_pp": [pred_lo, pred_hi], "verdict": verdict,
                       "note": f"2x reuse + reactor-swap at 200 t/ship: +{obs:.2f}pp"}

    # H-ph12-d: 3x reuse uplift at delivery=200
    r = find("reuse_3x_two_reactor_swaps", 200.0)
    obs = r["irr_uplift_pp"]
    pred_lo, pred_hi = 1.0, 2.0
    verdict = (
        "held" if pred_lo <= obs <= pred_hi else
        "wrong-but-informative" if abs(obs - (pred_lo+pred_hi)/2) <= 1.0 else
        "wrong-and-load-bearing"
    )
    out["H-ph12-d"] = {"observed_pp": round(obs, 3), "predicted_pp": [pred_lo, pred_hi], "verdict": verdict,
                       "note": f"3x reuse + 2 reactor swaps at 200 t/ship: +{obs:.2f}pp"}

    # H-ph12-e: 2x reuse + basic refurb uplift at delivery=200
    r = find("reuse_2x_basic_200M", 200.0)
    obs = r["irr_uplift_pp"]
    pred_lo, pred_hi = 1.8, 2.8
    verdict = (
        "held" if pred_lo <= obs <= pred_hi else
        "wrong-but-informative" if abs(obs - (pred_lo+pred_hi)/2) <= 1.0 else
        "wrong-and-load-bearing"
    )
    out["H-ph12-e"] = {"observed_pp": round(obs, 3), "predicted_pp": [pred_lo, pred_hi], "verdict": verdict,
                       "note": f"2x reuse + basic refurb at 200 t/ship: +{obs:.2f}pp (upside case)"}

    # H-ph12-f: no reuse scenario crosses 4% at delivery=200
    irrs_at_200 = [r["irr"] for r in rows if r["delivery_t"] == 200.0 and r["irr"] is not None]
    max_irr_at_200 = max(irrs_at_200) if irrs_at_200 else None
    held = max_irr_at_200 is None or max_irr_at_200 < 0.04
    out["H-ph12-f"] = {"max_irr_at_200t": round(max_irr_at_200*100, 2) if max_irr_at_200 else None,
                       "threshold_pct": 4.0,
                       "verdict": "held" if held else "falsified",
                       "note": f"max IRR at 200 t/ship across all reuse scenarios: {max_irr_at_200*100:.2f}%" if max_irr_at_200 else "no IRR converged"}

    # H-ph12-g: 482 t/ship with reuse — does it clear regulated-utility (8%) by ≥ 1 pp?
    irrs_at_482 = [(r["scenario"], r["irr"]) for r in rows if r["delivery_t"] == 482.0 and r["irr"] is not None]
    max_irr_at_482 = max(irr for _, irr in irrs_at_482) if irrs_at_482 else None
    obs = max_irr_at_482 * 100 if max_irr_at_482 else None
    pred_lo, pred_hi = 9.5, 11.5
    held = obs is not None and pred_lo - 1.0 <= obs <= pred_hi + 1.0
    out["H-ph12-g"] = {"max_irr_at_482t_pct": round(obs, 2) if obs else None,
                       "predicted_pct": [pred_lo, pred_hi],
                       "verdict": "held" if held else "falsified",
                       "note": f"max IRR at 482 t/ship with reuse: {obs:.2f}%" if obs else "no IRR converged"}

    return out


if __name__ == "__main__":
    main()
