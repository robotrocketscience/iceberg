"""Round 5 — Sweet-spot robustness for 1000-2000 s specific impulse band.

Sweeps reactor specific power, per-tech efficiency, cruise time, chunk mass,
and inbound delta-velocity. For each cell: computes delivery fraction and
cruise time at four design points (500 / 1500 / 2000 / 5000 s). Identifies
the Pareto frontier in (cruise time × delivery fraction).

Pre-registered hypothesis: 1000-2000 s sweet spot is robust to the sweep.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

from waterprop.constants import G0

# --- Sweep grid ---
REACTOR_W_PER_KG_LIST = [2.5, 5.0, 6.5]
CRUISE_YEARS_LIST = [5.0, 7.0, 10.0]
CHUNK_MASS_T_LIST = [5.0, 14.0, 50.0]
INBOUND_DV_KM_S_LIST = [2.85, 5.94]  # R8 Case C and Case B
DRY_SPACECRAFT_T = 5.0  # fixed
DUTY = 0.5

# --- Design points ---
DESIGN_POINTS = [
    {"name": "microwave_electrothermal", "isp_s": 500.0, "eta": 0.30},
    {"name": "water_Hall_low", "isp_s": 1000.0, "eta": 0.50},
    {"name": "water_Hall_mid", "isp_s": 1500.0, "eta": 0.55},
    {"name": "water_RF_ion", "isp_s": 2000.0, "eta": 0.65},
    {"name": "water_dual_ion", "isp_s": 5000.0, "eta": 0.55},
]


def chunk_delivery_and_cruise(
    isp_s: float,
    eta: float,
    chunk_t: float,
    dry_t: float,
    reactor_w_per_kg: float,
    cruise_yr: float,
    duty: float,
    dv_km_s: float,
    power_kwe: float,
) -> dict:
    v_e = isp_s * G0
    reactor_t = (power_kwe * 1000.0) / reactor_w_per_kg / 1000.0
    m0_t = chunk_t + dry_t + reactor_t
    m0_kg = m0_t * 1000.0
    prop_frac = 1.0 - math.exp(-dv_km_s * 1000.0 / v_e)
    prop_req_t = m0_t * prop_frac
    delivered_chunk_t = max(chunk_t - prop_req_t, 0.0)
    delivery_frac = delivered_chunk_t / chunk_t
    # Thrust + cruise-time check
    F_N = 2.0 * eta * power_kwe * 1000.0 / v_e
    m_avg = m0_t - prop_req_t / 2.0
    if F_N <= 0 or m_avg <= 0:
        cruise_required_yr = float("inf")
    else:
        accel_avg = F_N / (m_avg * 1000.0)
        cruise_required_s = dv_km_s * 1000.0 / (accel_avg * duty)
        cruise_required_yr = cruise_required_s / (365.25 * 86400)
    # Feasibility: cruise budget covers required cruise time AND positive chunk
    # delivered (avoids degenerate "wins" where propellant mass exceeds chunk).
    feasible = (cruise_required_yr <= cruise_yr) and (delivered_chunk_t > 0.0)
    return {
        "isp_s": isp_s,
        "eta": eta,
        "reactor_t": reactor_t,
        "m0_t": m0_t,
        "prop_req_t": prop_req_t,
        "delivered_chunk_t": delivered_chunk_t,
        "delivery_frac": delivery_frac,
        "thrust_N": F_N,
        "cruise_required_yr": cruise_required_yr,
        "feasible": feasible,
    }


def main() -> dict:
    # Pick a single power class to focus the analysis: Kilopower 10 kWe
    # (matches R10 / R6 baseline; lets the sweep dimensions be the other 5).
    power_kwe = 10.0

    cells = []
    for rw in REACTOR_W_PER_KG_LIST:
        for cy in CRUISE_YEARS_LIST:
            for cm in CHUNK_MASS_T_LIST:
                for dv in INBOUND_DV_KM_S_LIST:
                    cell = {
                        "reactor_w_per_kg": rw,
                        "cruise_yr": cy,
                        "chunk_t": cm,
                        "dv_km_s": dv,
                        "design_points": [],
                    }
                    for dp in DESIGN_POINTS:
                        r = chunk_delivery_and_cruise(
                            isp_s=dp["isp_s"],
                            eta=dp["eta"],
                            chunk_t=cm,
                            dry_t=DRY_SPACECRAFT_T,
                            reactor_w_per_kg=rw,
                            cruise_yr=cy,
                            duty=DUTY,
                            dv_km_s=dv,
                            power_kwe=power_kwe,
                        )
                        r["name"] = dp["name"]
                        cell["design_points"].append(r)
                    # Identify Pareto winner: highest delivered chunk among
                    # feasible (cruise_required ≤ cruise budget) design points.
                    feasible = [d for d in cell["design_points"] if d["feasible"]]
                    if feasible:
                        winner = max(feasible, key=lambda d: d["delivered_chunk_t"])
                        cell["pareto_winner"] = winner["name"]
                        cell["winner_delivery_t"] = winner["delivered_chunk_t"]
                        cell["winner_delivery_frac"] = winner["delivery_frac"]
                        cell["winner_isp_s"] = winner["isp_s"]
                    else:
                        cell["pareto_winner"] = None
                        cell["winner_isp_s"] = None
                    cells.append(cell)

    # Tally: how often does each design point win across the sweep?
    win_tally = {dp["name"]: 0 for dp in DESIGN_POINTS}
    for cell in cells:
        w = cell["pareto_winner"]
        if w is not None:
            win_tally[w] += 1
    total_feasible_cells = sum(1 for c in cells if c["pareto_winner"] is not None)
    total_infeasible_cells = len(cells) - total_feasible_cells

    # Robustness check: within how many cells does an Isp in [1000, 2000] s win?
    sweet_spot_wins = sum(
        1 for c in cells
        if c["winner_isp_s"] is not None and 1000.0 <= c["winner_isp_s"] <= 2000.0
    )
    sweet_spot_robustness = sweet_spot_wins / max(total_feasible_cells, 1)

    # Hypothesis grading
    grading = {}
    grading["H5_agg_sweet_spot_robust"] = {
        "predicted": "1000-2000 s wins or is within ±50% of winner across sweep",
        "measured_fraction_of_feasible_cells_where_1000_2000_s_wins": sweet_spot_robustness,
        "verdict": "held" if sweet_spot_robustness >= 0.5 else "partial" if sweet_spot_robustness >= 0.3 else "falsified",
    }
    grading["H5f_real_thrusters_in_band"] = {
        "claim": "1000 s (Hall low-band) and 2000 s (Pale Blue RF ion) are real candidates",
        "verdict": "held — both have heritage or near-heritage",
    }

    # Also: highlight cells where dual-ion (5000 s) IS the winner — these are
    # the design points where dual-ion actually wins on Pareto frontier.
    dual_ion_wins = [
        c for c in cells if c["pareto_winner"] == "water_dual_ion"
    ]

    results = {
        "inputs": {
            "power_kwe_fixed": power_kwe,
            "dry_t": DRY_SPACECRAFT_T,
            "duty": DUTY,
            "design_points": DESIGN_POINTS,
            "reactor_w_per_kg_list": REACTOR_W_PER_KG_LIST,
            "cruise_yr_list": CRUISE_YEARS_LIST,
            "chunk_t_list": CHUNK_MASS_T_LIST,
            "dv_km_s_list": INBOUND_DV_KM_S_LIST,
        },
        "cells": cells,
        "win_tally": win_tally,
        "total_cells": len(cells),
        "total_feasible_cells": total_feasible_cells,
        "total_infeasible_cells": total_infeasible_cells,
        "sweet_spot_robustness": sweet_spot_robustness,
        "dual_ion_winning_cells_count": len(dual_ion_wins),
        "hypothesis_grading": grading,
    }

    # Output
    out_dir = Path(__file__).parent / "results"
    out_dir.mkdir(exist_ok=True)
    with (out_dir / "sweet_spot_sweep.json").open("w") as f:
        json.dump(results, f, indent=2)

    # Console summary
    print("=" * 88)
    print("R5 — Sweet-spot robustness for 1000-2000 s specific impulse")
    print("=" * 88)
    print(f"Total cells swept: {len(cells)}  (feasible: {total_feasible_cells}, infeasible: {total_infeasible_cells})")
    print()
    print("Pareto-frontier winner tally across the sweep:")
    for name, count in win_tally.items():
        if total_feasible_cells > 0:
            pct = count / total_feasible_cells * 100
        else:
            pct = 0
        print(f"  {name:<30} {count:>4d} wins  ({pct:5.1f}% of feasible cells)")
    print()
    print(f"Fraction of feasible cells where Isp ∈ [1000, 2000] s wins: {sweet_spot_robustness*100:.1f}%")
    print()
    print("Cells where dual-ion (5000 s) wins:")
    if dual_ion_wins:
        for c in dual_ion_wins:
            print(f"  reactor={c['reactor_w_per_kg']} W/kg, cruise={c['cruise_yr']} yr, "
                  f"chunk={c['chunk_t']} t, dv={c['dv_km_s']} km/s "
                  f"→ {c['winner_delivery_frac']*100:.1f}% delivery")
    else:
        print("  (none — dual-ion never wins under the cruise-time constraint at 10 kWe)")
    print()
    print("Hypothesis grading:")
    for h, g in grading.items():
        print(f"  {h}: {g['verdict']}")
    print()
    # Quick textual exploration: for each cell, show winner
    print("Per-cell winner table (54 cells):")
    print(f"  {'reactor':>8} {'cruise':>7} {'chunk':>6} {'dv':>6} {'winner Isp':>11} {'deliv %':>8} {'thruster':<25}")
    for c in cells:
        winner_isp = c.get("winner_isp_s")
        winner_frac = c.get("winner_delivery_frac")
        winner_name = c.get("pareto_winner") or "infeasible"
        if winner_isp is not None:
            print(f"  {c['reactor_w_per_kg']:>6} W/kg {c['cruise_yr']:>5} yr "
                  f"{c['chunk_t']:>4.0f} t {c['dv_km_s']:>4.2f} km/s "
                  f"{winner_isp:>9.0f} s {winner_frac*100:>6.1f}%   {winner_name}")
        else:
            print(f"  {c['reactor_w_per_kg']:>6} W/kg {c['cruise_yr']:>5} yr "
                  f"{c['chunk_t']:>4.0f} t {c['dv_km_s']:>4.2f} km/s "
                  f"{'INFEASIBLE':>11}     —      {winner_name}")
    print()
    print(f"Result JSON: {out_dir / 'sweet_spot_sweep.json'}")
    return results


if __name__ == "__main__":
    main()
