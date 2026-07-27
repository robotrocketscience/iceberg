#!/usr/bin/env python3
"""
R-near-earth-asteroid-mission-tree — run.py

Closed-loop NEA architecture vs Saturn (titan-6 closed-loop = 0/150).

Reuses the mission-agnostic framework `derive_dry_mass` fixed-point via the new
`missions/nea_mass_demands.py` (the framework-abstraction test, H6). Computes:
  - KISS baseline reproduction (H1)
  - closed-loop mass-loop closure: does the NEA vehicle contain its own (solar)
    powerplant? (H3) — the axis on which Saturn dies (fission too heavy)
  - delivered water per mission vs L0-04 = 25 t floor (H2)
  - annual throughput at fleet sizes vs Saturn closed-loop 0 (H4)
  - cross-over floor (H5)

Deterministic; stdlib only. `python3 run.py` reproduces results/*.json byte-for-byte.
Author: hyperion (re-spawn 2), 2026-05-26.
"""
from __future__ import annotations

import csv
import json
import math
import sys
from pathlib import Path

ROUND = Path(__file__).parent
RESULTS = ROUND / "results"
RESULTS.mkdir(exist_ok=True)

# Import the closed-loop framework + the new NEA mass-demand module.
sys.path.insert(0, str((ROUND / ".." / ".." / "sims").resolve()))
from mission_graph.missions.nea_mass_demands import (  # noqa: E402
    NeaMassContext, derive_nea_vehicle, solar_powerplant_demand_kg, delivered_water_kg,
    KEY_SOLAR, KEY_THRUSTERS,
)
from mission_graph.missions.saturn_mass_demands import (  # noqa: E402
    MassContext as SaturnCtx, derive_saturn_vehicle, powerplant_demand_kg as saturn_pp,
)

# ---- anchors ----
L0_04_FLOOR_T = 25.0          # provisional commercial floor (locked belief c95626970c29aeef)
KISS_BOULDER_DIAM_M = 7.0
KISS_BOULDER_MASS_T = 500.0   # Keck KISS 2012 anchor: 7 m boulder ~ 500 t
NEA_ROUND_TRIP_YR = 7.0       # 2008 EV5 / KISS 6-10 yr band midpoint
POWER_KWE = 40.0              # KISS solar-electric class
# Per-mission cost bracket (SCOPE H3 anchors; not a derived number — labelled).
NEA_COST_B = 0.6              # $0.4-0.8B bracket midpoint
SATURN_COST_B = 1.25          # $1.0-1.5B conservative-anchor midpoint


def boulder_mass_t(diam_m: float) -> float:
    """Mass from diameter, anchored to KISS 7 m <-> 500 t, scaling as diameter^3."""
    return KISS_BOULDER_MASS_T * (diam_m / KISS_BOULDER_DIAM_M) ** 3


def nea_cell(diam_m: float, water_frac: float, extraction: float) -> dict:
    boulder_kg = boulder_mass_t(diam_m) * 1000.0
    ctx = NeaMassContext(boulder_mass_kg=boulder_kg, power_available_kwe=POWER_KWE)
    res = derive_nea_vehicle(ctx)
    pp_kg = solar_powerplant_demand_kg(ctx) + ctx.thrusters_kg_per_kwe * POWER_KWE
    delivered_t = delivered_water_kg(boulder_kg, water_frac, extraction) / 1000.0
    dry_t = res.dry_mass_kg / 1000.0
    return {
        "boulder_diam_m": diam_m,
        "boulder_mass_t": round(boulder_mass_t(diam_m), 1),
        "water_fraction": water_frac,
        "extraction_eff": extraction,
        "converged": res.converged,
        "dry_mass_t": round(dry_t, 2),
        "powerplant_t": round(pp_kg / 1000.0, 2),
        "vehicle_contains_powerplant": dry_t > pp_kg / 1000.0,
        "delivered_water_t": round(delivered_t, 2),
        "clears_25t_floor": delivered_t >= L0_04_FLOOR_T,
        "mass_loop_closes": res.converged and dry_t > pp_kg / 1000.0,
    }


def saturn_reference_cell() -> dict:
    """Saturn closed-loop reference at the canonical audit cell (titan-6: dies)."""
    ctx = SaturnCtx(chunk_mass_kg=200_000.0, power_available_kwe=30.0,
                    plans_aerocapture=True, entry_v_km_s=11.0)
    res = derive_saturn_vehicle(ctx)
    pp_kg = saturn_pp(ctx)
    return {
        "cell": "saturn canonical (200 t chunk, 30 kWe fission)",
        "converged": res.converged,
        "dry_mass_t": round(res.dry_mass_kg / 1000.0, 2),
        "powerplant_t": round(pp_kg / 1000.0, 2),
        "closed_loop_closure_inventory": "0 / 150 (titan-6 R-vehicle-mass-closure-refactor)",
        "note": "fission powerplant ~26 t at 40 kWe / ~22.8 t at 30 kWe; closers were lighter than their reactor",
    }


def main() -> None:
    # ---- H1: KISS baseline reproduction ----
    kiss = {
        "boulder": f"{KISS_BOULDER_DIAM_M} m / {KISS_BOULDER_MASS_T} t",
        "delivered_water_t_at_1.8pct_90eff": round(delivered_water_kg(KISS_BOULDER_MASS_T*1000, 0.018, 0.90)/1000, 2),
        "delivered_water_t_at_3pct_90eff": round(delivered_water_kg(KISS_BOULDER_MASS_T*1000, 0.030, 0.90)/1000, 2),
        "delivered_water_t_at_5pct_90eff": round(delivered_water_kg(KISS_BOULDER_MASS_T*1000, 0.050, 0.90)/1000, 2),
        "scope_H1_headline_claim_t": 14.0,
        "note": "SCOPE H1 says 14 t at 1.8%/90% but 500x0.018x0.9 = 8.1 t; 14 t corresponds to ~3% water. Encoded from inputs.",
    }

    # ---- H3: closed-loop mass-loop closure at KISS baseline ----
    base = nea_cell(KISS_BOULDER_DIAM_M, 0.018, 0.90)

    # ---- sweep (H2/H4/H5) ----
    diams = [3, 5, 7, 10, 15]
    wfs = [0.004, 0.018, 0.030, 0.050, 0.100]
    effs = [0.60, 0.75, 0.90]
    fleets = [1, 3, 5, 10]
    cells = []
    for d in diams:
        for wf in wfs:
            for eff in effs:
                c = nea_cell(d, wf, eff)
                for fleet in fleets:
                    annual = fleet * c["delivered_water_t"] / NEA_ROUND_TRIP_YR
                    c[f"annual_throughput_t_per_yr_fleet{fleet}"] = round(annual, 2)
                cells.append(c)

    # smallest delivered tonnage that clears 25 t (cross-over)
    clearing = [c for c in cells if c["clears_25t_floor"] and c["mass_loop_closes"]]
    n_mass_closes = sum(1 for c in cells if c["mass_loop_closes"])

    saturn = saturn_reference_cell()

    # ---- comparator (H4): NEA fleet=5 best-case annual vs Saturn 0 ----
    best_annual_f5 = max(c["annual_throughput_t_per_yr_fleet5"] for c in cells if c["mass_loop_closes"])
    # representative credible cell: 7 m, 3% water, 75% extraction
    cred = nea_cell(7, 0.030, 0.75)

    summary = {
        "round": "R-near-earth-asteroid-mission-tree",
        "author": "hyperion (re-spawn 2)",
        "date": "2026-05-26",
        "framework": "closed-loop (titan-6 R-vehicle-mass-closure-refactor); NEA reuses derive_dry_mass via nea_mass_demands.py",
        "anchors": {"power_kwe": POWER_KWE, "round_trip_yr": NEA_ROUND_TRIP_YR,
                    "L0_04_floor_t": L0_04_FLOOR_T, "kiss_boulder": f"{KISS_BOULDER_DIAM_M}m/{KISS_BOULDER_MASS_T}t"},
        "H1_kiss_baseline": kiss,
        "H3_closed_loop_mass_closure_baseline": base,
        "sweep_cell_count": len(cells),
        "n_cells_mass_loop_closes": n_mass_closes,
        "n_cells_clear_25t_floor_and_mass_closes": len(clearing),
        "credible_cell_7m_3pct_75eff": cred,
        "saturn_closed_loop_reference": saturn,
        "comparator": {
            "nea_mass_loop_closes": base["mass_loop_closes"],
            "saturn_mass_loop_closes_closed_loop": False,
            "nea_best_annual_throughput_t_per_yr_fleet5": round(best_annual_f5, 2),
            "saturn_annual_throughput_t_per_yr_closed_loop": 0.0,
            "nea_per_mission_cost_B_bracket": [0.4, 0.8],
            "saturn_per_mission_cost_B_bracket": [1.0, 1.5],
        },
        "sweep_cells": cells,
    }
    (RESULTS / "nea_sweep.json").write_text(json.dumps(summary, indent=2, default=str))

    # comparator CSV (delivered + closure by boulder x water fraction at 90% eff)
    with open(RESULTS / "comparator_pareto.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["boulder_diam_m", "boulder_mass_t", "water_fraction", "extraction_eff",
                    "dry_mass_t", "powerplant_t", "mass_loop_closes", "delivered_water_t",
                    "clears_25t_floor", "annual_t_per_yr_fleet5"])
        for c in cells:
            if c["extraction_eff"] == 0.90:
                w.writerow([c["boulder_diam_m"], c["boulder_mass_t"], c["water_fraction"],
                            c["extraction_eff"], c["dry_mass_t"], c["powerplant_t"],
                            c["mass_loop_closes"], c["delivered_water_t"],
                            c["clears_25t_floor"], c[f"annual_throughput_t_per_yr_fleet5"]])

    # ---- console ----
    print("=" * 76)
    print("R-near-earth-asteroid-mission-tree — closed-loop NEA vs Saturn (0/150)")
    print("=" * 76)
    print("\nH1 KISS baseline (delivered water = boulder x water_frac x extraction):")
    print(f"  500 t boulder @ 1.8% / 90% = {kiss['delivered_water_t_at_1.8pct_90eff']} t  "
          f"(SCOPE said 14 t; that needs ~3% -> {kiss['delivered_water_t_at_3pct_90eff']} t)")
    print(f"\nH3 closed-loop mass closure (KISS 7 m / 500 t, 40 kWe SOLAR):")
    print(f"  NEA dry mass {base['dry_mass_t']} t; solar powerplant {base['powerplant_t']} t; "
          f"converged={base['converged']}; vehicle contains powerplant={base['vehicle_contains_powerplant']}")
    print(f"  -> NEA mass loop closes: {base['mass_loop_closes']}")
    print(f"  Saturn reference: dry {saturn['dry_mass_t']} t, FISSION powerplant {saturn['powerplant_t']} t; "
          f"closed-loop inventory {saturn['closed_loop_closure_inventory']}")
    print(f"\nH2 delivered vs 25 t floor: {len(clearing)} of {len(cells)} cells clear 25 t AND close mass loop.")
    print(f"  Credible cell (7 m, 3% water, 75% eff): delivered {cred['delivered_water_t']} t, "
          f"clears 25 t = {cred['clears_25t_floor']}")
    print(f"\nH4 annual throughput fleet=5: NEA best {best_annual_f5:.1f} t/yr vs Saturn closed-loop 0 t/yr.")
    print(f"\nMass-loop closes in {n_mass_closes}/{len(cells)} NEA cells (Saturn: 0/150).")
    print(f"\nWrote {RESULTS/'nea_sweep.json'} and {RESULTS/'comparator_pareto.csv'}")


if __name__ == "__main__":
    main()
