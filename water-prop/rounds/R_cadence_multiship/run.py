"""R-cadence — IRR sensitivity to launch cadence (N ships per window).

Two flavors:
- larger_fleet: N ships per event, same ~1.08-year event spacing, total fleet
  scales with N (37 -> 74 -> 111 ships).
- compressed_schedule: total fleet pinned to ~37 ships, but N per event with
  fewer events (front-loaded into years 0..18).

Reuses R15-rerun cashflow model and R-NPV's NPV / IRR helpers.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROUND_DIR = Path(__file__).resolve().parent
ROUNDS_ROOT = ROUND_DIR.parent

# Load R15-rerun model.
R15 = ROUNDS_ROOT / "R15_rerun_audited" / "run.py"
spec = importlib.util.spec_from_file_location("r15_rerun", R15)
r15 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r15)

# Load R-NPV helpers.
NPV = ROUNDS_ROOT / "R_NPV_discount_rate" / "run.py"
spec = importlib.util.spec_from_file_location("r_npv", NPV)
r_npv = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r_npv)


HORIZON_YR = 45
BASELINE_TOTAL_FLEET = 37  # matches R15-rerun build_fleet_schedule out to year 45


def schedule_larger_fleet(n_per_event: int, horizon_yr: int = HORIZON_YR):
    """N ships per event, same ~1.08-yr spacing as R15-rerun."""
    schedule = []
    for k in range(n_per_event):
        schedule.append({"ship_no": len(schedule) + 1, "launch_year": 0,
                         "reactor_era": r15.reactor_era_for_launch_year(0)})
    for k in range(n_per_event):
        schedule.append({"ship_no": len(schedule) + 1, "launch_year": 7,
                         "reactor_era": r15.reactor_era_for_launch_year(7)})
    year = 8.0
    while year < horizon_yr:
        for k in range(n_per_event):
            schedule.append({"ship_no": len(schedule) + 1, "launch_year": year,
                             "reactor_era": r15.reactor_era_for_launch_year(int(year))})
        year += 13.0 / 12.0
    return schedule


def schedule_compressed(n_per_event: int, horizon_yr: int = HORIZON_YR,
                        total_fleet: int = BASELINE_TOTAL_FLEET):
    """N ships per event, total fleet pinned, events front-loaded."""
    n_events = max(1, total_fleet // n_per_event)
    if total_fleet % n_per_event:
        n_events += 1
    spacing = 13.0 / 12.0
    schedule = []
    event_year = 0.0
    ships_remaining = total_fleet
    for ev in range(n_events):
        n_this = min(n_per_event, ships_remaining)
        for k in range(n_this):
            ly = event_year if event_year < horizon_yr else horizon_yr - 1
            schedule.append({"ship_no": len(schedule) + 1,
                             "launch_year": ly,
                             "reactor_era": r15.reactor_era_for_launch_year(int(ly))})
        ships_remaining -= n_this
        if ev == 0:
            event_year = 7.0
        elif ev == 1:
            event_year = 8.0
        else:
            event_year += spacing
    return schedule


def cashflow_with_schedule(schedule, price_per_kg, sov_amt, sov_yr, cost_scale,
                           chunk_table, round_trip_yr=18, horizon_yr=HORIZON_YR):
    """R15-rerun cashflow_model() but with an externally supplied schedule."""
    yearly = {yr: {"cost": 0.0, "revenue": 0.0} for yr in range(horizon_yr)}
    yearly[0]["cost"] += r15.DEMONSTRATOR_NRE
    ship_cost = r15.ship_build_cost_table(cost_scale)
    for ship in schedule:
        ly = int(ship["launch_year"])
        if ly >= horizon_yr:
            continue
        yearly[ly]["cost"] += ship_cost[ship["reactor_era"]] + r15.LAUNCH_PLUS_TSI
        dy = ly + round_trip_yr
        if dy < horizon_yr:
            chunk_t = chunk_table[ship["reactor_era"]]
            yearly[dy]["revenue"] += chunk_t * 1000.0 * price_per_kg
    for yr in range(horizon_yr):
        yearly[yr]["cost"] += r15.GROUND_OPS_PER_YEAR
    if 0 < sov_amt and 0 <= sov_yr < horizon_yr:
        yearly[sov_yr]["revenue"] += sov_amt
    cum_c, cum_r = 0.0, 0.0
    be_year = None
    for yr in range(horizon_yr):
        cum_c += yearly[yr]["cost"]
        cum_r += yearly[yr]["revenue"]
        yearly[yr]["cum_cashflow"] = cum_r - cum_c
        if be_year is None and cum_r >= cum_c and yr > 0:
            be_year = yr
    return {"yearly": yearly, "breakeven_year": be_year,
            "final_cum_cashflow": yearly[horizon_yr - 1]["cum_cashflow"],
            "fleet_size": len(schedule)}


def irr_bisect(yearly, horizon, with_terminal=True):
    lo, hi = -0.05, 0.50
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        npv = r_npv.npv_from_yearly(yearly, mid, horizon)
        if with_terminal:
            npv += r_npv.perpetuity_terminal_value(yearly, mid, horizon)
        if npv > 0:
            lo = mid
        else:
            hi = mid
    return lo


def main():
    flavors = {
        "larger_fleet": schedule_larger_fleet,
        "compressed_schedule": schedule_compressed,
    }
    n_values = [1, 2, 3, 5]
    rows = []
    BEST = dict(price=10000.0, sov_amt=2e9, sov_yr=11, cost_scale="commercial_mid")

    for fname, fn in flavors.items():
        for n in n_values:
            sched = fn(n)
            cf = cashflow_with_schedule(
                sched, BEST["price"], BEST["sov_amt"], BEST["sov_yr"],
                BEST["cost_scale"], r15.AUDITED_CHUNK_DELIVERED_T,
                round_trip_yr=18, horizon_yr=HORIZON_YR,
            )
            irr_no_tv = irr_bisect(cf["yearly"], HORIZON_YR, with_terminal=False)
            irr_with_tv = irr_bisect(cf["yearly"], HORIZON_YR, with_terminal=True)
            npv_8pct = r_npv.npv_from_yearly(cf["yearly"], 0.08, HORIZON_YR) \
                       + r_npv.perpetuity_terminal_value(cf["yearly"], 0.08, HORIZON_YR)
            rows.append({
                "flavor": fname, "N_ships_per_event": n,
                "fleet_size": cf["fleet_size"],
                "irr_no_tv": irr_no_tv, "irr_with_tv": irr_with_tv,
                "npv_8pct_with_tv": npv_8pct,
                "undisc_breakeven_year": cf["breakeven_year"],
                "undisc_final_cumcf": cf["final_cum_cashflow"],
            })

    out_dir = ROUND_DIR / "results"
    out_dir.mkdir(exist_ok=True)
    with (out_dir / "cadence_irr.json").open("w") as f:
        json.dump(rows, f, indent=2)

    print("=" * 100)
    print("R-cadence — IRR vs cadence (best-case cell: $10k/kg + $2B sov yr 11 + commercial_mid)")
    print("=" * 100)
    print()
    print(f"{'flavor':<22} {'N':>3} {'fleet':>6} {'IRR (no TV)':>12} {'IRR (w/ TV)':>12} {'NPV@8% (TV) $B':>16} {'undisc BE':>10}")
    for r in rows:
        be = f"yr {r['undisc_breakeven_year']}" if r['undisc_breakeven_year'] else "never"
        print(f"  {r['flavor']:<20} {r['N_ships_per_event']:>3d} {r['fleet_size']:>6d} "
              f"{r['irr_no_tv']*100:>11.2f}% {r['irr_with_tv']*100:>11.2f}% "
              f"{r['npv_8pct_with_tv']/1e9:>16.2f} {be:>10}")
    print()

    # Full sweep at 10% commercial discount under N=3 and N=5 compressed
    PRICES = [2000.0, 3000.0, 4000.0, 5000.0, 10000.0]
    SOV_AMTS = [0.0, 1e9, 2e9]
    SOV_YEARS = [11, 15]
    COSTS = ["conops_optimistic", "commercial_mid", "commercial_high"]

    for tag, sched_fn, n in [("N=3 compressed", schedule_compressed, 3),
                              ("N=5 compressed", schedule_compressed, 5)]:
        sched = sched_fn(n)
        positives_10pct = 0
        positives_8pct = 0
        for p in PRICES:
            for sa in SOV_AMTS:
                for sy in SOV_YEARS:
                    for cs in COSTS:
                        cf = cashflow_with_schedule(
                            sched, p, sa, sy, cs,
                            r15.AUDITED_CHUNK_DELIVERED_T, 18, HORIZON_YR,
                        )
                        npv10 = r_npv.npv_from_yearly(cf["yearly"], 0.10, HORIZON_YR) \
                               + r_npv.perpetuity_terminal_value(cf["yearly"], 0.10, HORIZON_YR)
                        npv8 = r_npv.npv_from_yearly(cf["yearly"], 0.08, HORIZON_YR) \
                               + r_npv.perpetuity_terminal_value(cf["yearly"], 0.08, HORIZON_YR)
                        if npv10 > 0:
                            positives_10pct += 1
                        if npv8 > 0:
                            positives_8pct += 1
        print(f"  {tag:<20}: {positives_8pct}/90 cells NPV+TV>0 at 8%; "
              f"{positives_10pct}/90 cells NPV+TV>0 at 10%")

    print()
    # IRR scan vs N for both flavors
    print("IRR (with terminal value) vs N:")
    print(f"  {'N':>3} {'larger_fleet':>14} {'compressed':>14}")
    for n in n_values:
        rl = next(r for r in rows if r["flavor"] == "larger_fleet" and r["N_ships_per_event"] == n)
        rc = next(r for r in rows if r["flavor"] == "compressed_schedule" and r["N_ships_per_event"] == n)
        print(f"  {n:>3d} {rl['irr_with_tv']*100:>13.2f}% {rc['irr_with_tv']*100:>13.2f}%")


if __name__ == "__main__":
    main()
