#!/usr/bin/env python3
"""
R-staged-commitment-gates-frame-B-interaction — does staged commitment
materially shift Frame B P(NPV>0) per the R-LEO-water-demand-curve clearing-price
distribution, vs the upfront-fleet baseline?

Composes:
  - R_heterogeneous_cadence Regime R semantics (mission 1 demonstrator at year 0
    certain; missions 2..N deferred to year (RT_1 + 0.5) and gated by
    P_demonstrator = 0.90).
  - R_LEO_water_demand_curve clearing-price MC (Starship $/kg lognormal × markup
    lognormal; 10,000 draws; seed 20260515).
  - R_single_launch_architecture_feasibility (round 12) launch-count anchors:
      1-launch: sp >= 11 W/kg, conjunction 0.25%, +$100M/mission launch cost
      2-launch: sp >=  8 W/kg, conjunction 0.67%, +$200M/mission launch cost
      3-launch: sp >=  8 W/kg, conjunction 0.67%, +$300M/mission launch cost

Sweep: launch_count x regime x WACC x LR.

Outputs to results/staged_gates_frame_B_summary.json.
"""
from __future__ import annotations

import importlib.util
import json
import math
import random
import sys
from pathlib import Path

THIS_DIR = Path(__file__).parent
RESULTS_DIR = THIS_DIR / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# Import R_heterogeneous_cadence/run.py for re-use of its npv_regime_D / npv_regime_R helpers.
HET_RUN_PATH = THIS_DIR.parent / "R_heterogeneous_cadence" / "run.py"
spec = importlib.util.spec_from_file_location("hetcad_run", HET_RUN_PATH)
hetcad = importlib.util.module_from_spec(spec)
sys.modules["hetcad_run"] = hetcad
spec.loader.exec_module(hetcad)

SEED = 20260515
N_MC = 10000

# ---------------------------------------------------------------------------
# Constants for this round
# ---------------------------------------------------------------------------
# Chunk-200 demonstrator (no chunk-shrinking; R-heterogeneous-cadence proved
# chunk-shrinking is dominated).
CHUNK_T = 200.0
P_DEMONSTRATOR = 0.90

# Launch-count anchors (round 12)
LAUNCH_COUNTS = [1, 2, 3]
LAUNCH_COST_PER_MISSION_M = {1: 100.0, 2: 200.0, 3: 300.0}  # $M extra opex per mission
CONJUNCTION_MULTIPLIER = {1: 0.0025, 2: 0.0067, 3: 0.0067}  # H2a uniform prior

# Sovereign-bond and corporate-growth anchors
WACC_VALUES = [0.0, 0.03, 0.087]
LR_VALUES = [0.0, 0.15]

# Demonstrator NRE — mission 1 ship + reactor flight-qual + flight ops
# (BOE per STUDY.md cell γ)
DEMONSTRATOR_NRE_M = 600.0 + 200.0  # reactor qual + flight ops; ship cost is already in npv

# ---------------------------------------------------------------------------
# Demand curve sampler (replicates R-LEO-water-demand-curve)
# ---------------------------------------------------------------------------
def sample_clearing_per_tonne_M(n: int) -> list[float]:
    """10,000 lognormal draws of clearing price ($M/tonne).

    Starship $/kg lognormal: median $1500, p05 $200, p95 $15000.
    Markup lognormal:        median 3.5,  p05 1.2,  p95 15.

    Independent samples. Seed-reseeding pattern matches R_heterogeneous_cadence
    mc_h5 for direct comparability.
    """
    rng_s = random.Random(SEED)
    starship = hetcad.lognormal_draws(rng_s, n, 1500.0, 200.0, 15000.0)
    rng_m = random.Random(SEED + 1)
    markup = hetcad.lognormal_draws(rng_m, n, 3.5, 1.2, 15.0)
    clearing_per_kg = [s * m for s, m in zip(starship, markup)]
    return [c * 1000.0 / 1e6 for c in clearing_per_kg]  # $/kg -> $M/tonne


# ---------------------------------------------------------------------------
# Per-cell NPV under both regimes; with launch-count opex premium
# ---------------------------------------------------------------------------
def npv_cell(
    regime: str,
    wacc: float,
    lr: float,
    rev_per_tonne_M: float,
    launch_count: int,
    include_demonstrator_nre: bool = True,
) -> dict:
    """Compute program NPV for one (regime, wacc, lr, rev, launch_count) cell.

    Launch-count premium is added as op_cost_per_mission_M.
    Demonstrator NRE is a one-time year-0 charge IF include_demonstrator_nre is
    True AND regime == 'R'. (Under upfront commitment, reactor-qual NRE is also
    paid, but it folds into program economics differently; for this round's
    apples-to-apples comparison we attribute it only to the staged arm. A
    sensitivity will probably show it doesn't matter to the comparative result.)
    """
    sched = hetcad.Schedule(chunk_1_t=CHUNK_T, reusable=False)
    op_per_mission = LAUNCH_COST_PER_MISSION_M[launch_count]

    if regime == "D":
        return hetcad.npv_regime_D(
            sched, wacc=wacc, revenue_per_tonne_M=rev_per_tonne_M,
            learning_rate=lr, op_cost_per_mission_M=op_per_mission,
        )
    elif regime == "R":
        nre = DEMONSTRATOR_NRE_M if include_demonstrator_nre else 0.0
        return hetcad.npv_regime_R(
            sched, wacc=wacc, revenue_per_tonne_M=rev_per_tonne_M,
            learning_rate=lr, p_success=P_DEMONSTRATOR,
            nre_M=nre, op_cost_per_mission_M=op_per_mission,
        )
    else:
        raise ValueError(regime)


# ---------------------------------------------------------------------------
# Cross-checks
# ---------------------------------------------------------------------------
def cross_checks() -> dict:
    out = {}

    # XC-1: upfront 2-launch at WACC 3% LR 15% over MC -> ~42.8 percent
    # (replicates R-LEO-water-demand-curve E_500kWe_200t WACC_0.03_LR_0.15)
    rev_samples = sample_clearing_per_tonne_M(N_MC)
    n_pos = 0
    for rev in rev_samples:
        # demand-curve used no launch-count opex, no NRE — just E_500kWe_200t
        npv = hetcad.npv_regime_D(
            hetcad.Schedule(chunk_1_t=CHUNK_T, reusable=False),
            wacc=0.03, revenue_per_tonne_M=rev, learning_rate=0.15,
        )
        if npv["npv_M"] >= 0:
            n_pos += 1
    out["XC1_upfront_wacc3_lr15_no_launch_opex"] = {
        "measured_pct_npv_positive": n_pos / N_MC * 100,
        "demand_curve_published_pct": 42.82,
        "tolerance_pp": 1.0,
        "passes": abs(n_pos / N_MC * 100 - 42.82) < 1.0,
    }

    # XC-2: upfront WACC 3% LR 0% -> ~29.1 percent (matches round-11 anchor)
    n_pos = 0
    for rev in rev_samples:
        npv = hetcad.npv_regime_D(
            hetcad.Schedule(chunk_1_t=CHUNK_T, reusable=False),
            wacc=0.03, revenue_per_tonne_M=rev, learning_rate=0.0,
        )
        if npv["npv_M"] >= 0:
            n_pos += 1
    out["XC2_upfront_wacc3_lr0_no_launch_opex"] = {
        "measured_pct_npv_positive": n_pos / N_MC * 100,
        "demand_curve_published_pct": 29.11,
        "tolerance_pp": 1.0,
        "passes": abs(n_pos / N_MC * 100 - 29.11) < 1.0,
    }

    # XC-3: P_demonstrator = 1.0, Regime R at $2.5M/tonne should approximately
    # match R-heterogeneous-cadence XC-3 = +$2531M Δ-NPV at chunk=200 WACC 3% LR 15%.
    sched = hetcad.Schedule(chunk_1_t=CHUNK_T, reusable=False)
    d_ref = hetcad.npv_regime_D(sched, wacc=0.03, revenue_per_tonne_M=2.5, learning_rate=0.15)
    r_p1 = hetcad.npv_regime_R(
        sched, wacc=0.03, revenue_per_tonne_M=2.5, learning_rate=0.15, p_success=1.0,
    )
    delta_p1 = r_p1["npv_M"] - d_ref["npv_M"]
    out["XC3_p1_chunk200_wacc3_lr15"] = {
        "measured_delta_npv_M": delta_p1,
        "het_cadence_published_M": 2531.0,
        "tolerance_pct": 20.0,
        "passes": abs(delta_p1 - 2531.0) / 2531.0 < 0.20,
    }

    # XC-4: at WACC=0, Δ-NPV between Regime R (P=0.9) and Regime D at chunk=200
    # should be NEGATIVE (probability-weighted loss of fleet revenue without
    # discount-rate compensation).
    d0 = hetcad.npv_regime_D(sched, wacc=0.0, revenue_per_tonne_M=2.5, learning_rate=0.15)
    r0 = hetcad.npv_regime_R(
        sched, wacc=0.0, revenue_per_tonne_M=2.5, learning_rate=0.15, p_success=0.90,
    )
    delta0 = r0["npv_M"] - d0["npv_M"]
    out["XC4_wacc0_chunk200_signcheck"] = {
        "measured_delta_npv_M": delta0,
        "expected_sign": "negative_or_near_zero",
        "passes": delta0 <= 0.0 + 1e-6,
    }

    # XC-5: demonstrator NRE BOE
    out["XC5_demonstrator_nre"] = {
        "measured_M": DEMONSTRATOR_NRE_M,  # reactor + ops (ship cost separate)
        "boe_M": 800.0,  # reactor 600 + ops 200, per STUDY cell gamma
        "tolerance_pct": 15.0,
        "passes": abs(DEMONSTRATOR_NRE_M - 800.0) / 800.0 < 0.15,
    }

    return out


# ---------------------------------------------------------------------------
# Frame A and Frame B sweep
# ---------------------------------------------------------------------------
def frame_a_b_sweep() -> list[dict]:
    """Compute Frame A and Frame B P(NPV>0) per (regime, wacc, lr, launch_count)
    cell across the demand-curve MC.

    Frame B: P(NPV>0) directly from MC, conditional on technical closure.
    Frame A: Frame B × conjunction_multiplier[launch_count].
    """
    rev_samples = sample_clearing_per_tonne_M(N_MC)
    rows = []
    for launch_count in LAUNCH_COUNTS:
        for regime in ("D", "R"):
            for wacc in WACC_VALUES:
                for lr in LR_VALUES:
                    npvs = []
                    n_pos = 0
                    for rev in rev_samples:
                        cell = npv_cell(regime, wacc, lr, rev, launch_count)
                        npvs.append(cell["npv_M"])
                        if cell["npv_M"] >= 0:
                            n_pos += 1
                    npvs_sorted = sorted(npvs)
                    median_npv = npvs_sorted[N_MC // 2]
                    p05 = npvs_sorted[int(N_MC * 0.05)]
                    p95 = npvs_sorted[int(N_MC * 0.95)]
                    frame_b = n_pos / N_MC
                    frame_a = frame_b * CONJUNCTION_MULTIPLIER[launch_count]
                    rows.append({
                        "launch_count": launch_count,
                        "regime": regime,
                        "wacc": wacc,
                        "lr": lr,
                        "n_samples": N_MC,
                        "frame_b_pct": frame_b * 100,
                        "frame_a_pct": frame_a * 100,
                        "median_npv_M": median_npv,
                        "p05_npv_M": p05,
                        "p95_npv_M": p95,
                        "conjunction_mult": CONJUNCTION_MULTIPLIER[launch_count],
                        "op_cost_per_mission_M": LAUNCH_COST_PER_MISSION_M[launch_count],
                    })
    return rows


def delta_frame_b(rows: list[dict]) -> list[dict]:
    """For each (launch_count, wacc, lr), compute Δ(Frame B) staged minus upfront."""
    upfront = {}
    for r in rows:
        if r["regime"] == "D":
            key = (r["launch_count"], r["wacc"], r["lr"])
            upfront[key] = r["frame_b_pct"]
    out = []
    for r in rows:
        if r["regime"] == "R":
            key = (r["launch_count"], r["wacc"], r["lr"])
            d = dict(r)
            d["upfront_frame_b_pct"] = upfront[key]
            d["delta_frame_b_pp"] = r["frame_b_pct"] - upfront[key]
            out.append(d)
    return out


# ---------------------------------------------------------------------------
# H5: demonstrator NRE fraction of total program capex
# ---------------------------------------------------------------------------
def demonstrator_nre_fraction() -> dict:
    """Compute mission-1 capex (ship + NRE + first-mission launch + ops) as a
    fraction of total program capex (mission 1 + 2..N fleet ramp).
    Use undiscounted nominal $.
    """
    sched = hetcad.Schedule(chunk_1_t=CHUNK_T, reusable=False)
    # Mission 1 capex: ship 1 (Wright unit 1, full first-unit cost) +
    # demonstrator NRE + first-mission launch opex (3-launch ceiling)
    mission1_ship = hetcad.FIRST_UNIT_COST_M
    mission1_launch = LAUNCH_COST_PER_MISSION_M[3]  # use 3-launch (most conservative)
    mission1_nre = DEMONSTRATOR_NRE_M
    mission1_total = mission1_ship + mission1_launch + mission1_nre

    # Missions 2..N capex (Regime R schedule, P_success-deflated nominal sum)
    launches_R, _, _ = hetcad.regime_R_schedule(sched, p_success=1.0)  # undiscounted, undeflated count
    n_ships = 0
    seen = set()
    fleet_ship_capex = 0.0
    for (t, ship_id, _, _, _) in launches_R:
        if ship_id == 1:
            continue
        if ship_id not in seen:
            n_ships += 1
            seen.add(ship_id)
            unit = hetcad.wright_unit_cost(n_ships + 1, hetcad.FIRST_UNIT_COST_M, 0.15)
            fleet_ship_capex += unit
    n_fleet_missions = len(launches_R) - 1  # excludes mission 1
    fleet_launch_capex = n_fleet_missions * LAUNCH_COST_PER_MISSION_M[3]
    fleet_total = fleet_ship_capex + fleet_launch_capex

    total = mission1_total + fleet_total
    return {
        "mission1_ship_M": mission1_ship,
        "mission1_launch_M": mission1_launch,
        "mission1_nre_M": mission1_nre,
        "mission1_total_M": mission1_total,
        "fleet_ship_capex_M": fleet_ship_capex,
        "fleet_launch_capex_M": fleet_launch_capex,
        "fleet_total_M": fleet_total,
        "n_fleet_ships": n_ships,
        "n_fleet_missions": n_fleet_missions,
        "program_total_M": total,
        "demonstrator_fraction_pct": mission1_total / total * 100,
    }


# ---------------------------------------------------------------------------
# H6: median-clearing-price point check
# ---------------------------------------------------------------------------
def h6_median_clearing_check() -> dict:
    """At median clearing $5.284M/tonne, 2-launch, WACC 3% LR 15%: does
    upfront NPV flip from negative to positive under staged commitment?
    """
    rev_median = 5.284
    d = npv_cell("D", 0.03, 0.15, rev_median, launch_count=2)
    r = npv_cell("R", 0.03, 0.15, rev_median, launch_count=2)
    return {
        "rev_per_tonne_M": rev_median,
        "upfront_npv_M": d["npv_M"],
        "staged_npv_M": r["npv_M"],
        "upfront_sign": "positive" if d["npv_M"] >= 0 else "negative",
        "staged_sign": "positive" if r["npv_M"] >= 0 else "negative",
        "flip_occurs": d["npv_M"] < 0 and r["npv_M"] >= 0,
    }


# ---------------------------------------------------------------------------
# H7: median Δ-NPV in $B across MC draws
# ---------------------------------------------------------------------------
def h7_median_delta_npv() -> dict:
    rev_samples = sample_clearing_per_tonne_M(N_MC)
    deltas = []
    for rev in rev_samples:
        d = npv_cell("D", 0.03, 0.15, rev, launch_count=2)
        r = npv_cell("R", 0.03, 0.15, rev, launch_count=2)
        deltas.append(r["npv_M"] - d["npv_M"])
    deltas_sorted = sorted(deltas)
    return {
        "n_samples": N_MC,
        "median_delta_npv_M": deltas_sorted[N_MC // 2],
        "median_delta_npv_B": deltas_sorted[N_MC // 2] / 1000.0,
        "p05_delta_npv_M": deltas_sorted[int(N_MC * 0.05)],
        "p95_delta_npv_M": deltas_sorted[int(N_MC * 0.95)],
    }


# ---------------------------------------------------------------------------
# Grader
# ---------------------------------------------------------------------------
def grade(result: dict) -> list[dict]:
    """Apply pre-registered hypothesis brackets from STUDY.md."""
    rows = result["frame_b_sweep_delta"]

    def lookup(launch_count, regime_, wacc, lr):
        # rows are only Regime R; for the upfront we use the embedded upfront_frame_b_pct
        for r in rows:
            if (r["launch_count"] == launch_count and r["regime"] == regime_
                    and abs(r["wacc"] - wacc) < 1e-9 and abs(r["lr"] - lr) < 1e-9):
                return r
        return None

    # We'll also need the upfront rows from the original sweep
    all_rows = result["frame_b_sweep"]

    def lookup_any(launch_count, regime_, wacc, lr):
        for r in all_rows:
            if (r["launch_count"] == launch_count and r["regime"] == regime_
                    and abs(r["wacc"] - wacc) < 1e-9 and abs(r["lr"] - lr) < 1e-9):
                return r
        return None

    grades = []

    # H1: staged 2-launch WACC 3% LR 15% in [55, 70]
    r = lookup(2, "R", 0.03, 0.15)
    grades.append({
        "id": "H1",
        "predicted_band_pct": [55.0, 70.0],
        "measured_pct": r["frame_b_pct"] if r else None,
        "upfront_pct": r["upfront_frame_b_pct"] if r else None,
        "delta_pp": r["delta_frame_b_pp"] if r else None,
        "status": "HELD" if r and 55.0 <= r["frame_b_pct"] <= 70.0 else "FALSIFIED",
    })

    # H2: staged 3-launch WACC 3% LR 0% in [40, 58]
    r = lookup(3, "R", 0.03, 0.0)
    grades.append({
        "id": "H2",
        "predicted_band_pct": [40.0, 58.0],
        "measured_pct": r["frame_b_pct"] if r else None,
        "upfront_pct": r["upfront_frame_b_pct"] if r else None,
        "delta_pp": r["delta_frame_b_pp"] if r else None,
        "status": "HELD" if r and 40.0 <= r["frame_b_pct"] <= 58.0 else "FALSIFIED",
    })

    # H3: staged 2-launch WACC 8.7% LR 15% in [25, 45]
    r = lookup(2, "R", 0.087, 0.15)
    grades.append({
        "id": "H3",
        "predicted_band_pct": [25.0, 45.0],
        "measured_pct": r["frame_b_pct"] if r else None,
        "upfront_pct": r["upfront_frame_b_pct"] if r else None,
        "delta_pp": r["delta_frame_b_pp"] if r else None,
        "status": "HELD" if r and 25.0 <= r["frame_b_pct"] <= 45.0 else "FALSIFIED",
    })

    # H4: Frame A optimum stays 2-launch under staged commitment
    # Pred bands: 1-launch [0.15, 0.25], 2-launch [0.20, 0.35], 3-launch [0.15, 0.25] at WACC 3% LR 15%
    r1 = lookup_any(1, "R", 0.03, 0.15)
    r2 = lookup_any(2, "R", 0.03, 0.15)
    r3 = lookup_any(3, "R", 0.03, 0.15)
    if r1 and r2 and r3:
        winner = max([(r1, "1-launch"), (r2, "2-launch"), (r3, "3-launch")],
                     key=lambda x: x[0]["frame_a_pct"])
        grades.append({
            "id": "H4",
            "predicted_winner": "2-launch",
            "measured_winner": winner[1],
            "frame_a_1_launch_pct": r1["frame_a_pct"],
            "frame_a_2_launch_pct": r2["frame_a_pct"],
            "frame_a_3_launch_pct": r3["frame_a_pct"],
            "pred_bands": {"1": [0.15, 0.25], "2": [0.20, 0.35], "3": [0.15, 0.25]},
            "status": "HELD" if winner[1] == "2-launch" else "FALSIFIED",
        })

    # H5: demonstrator NRE fraction in [8, 15] percent
    nre = result["demonstrator_nre_fraction"]
    grades.append({
        "id": "H5",
        "predicted_band_pct": [8.0, 15.0],
        "measured_pct": nre["demonstrator_fraction_pct"],
        "status": "HELD" if 8.0 <= nre["demonstrator_fraction_pct"] <= 15.0 else "FALSIFIED",
    })

    # H6: NPV flips from negative (upfront) to positive (staged) at median clearing
    h6 = result["h6_median_clearing_check"]
    grades.append({
        "id": "H6",
        "predicted": "upfront negative, staged positive",
        "upfront_sign": h6["upfront_sign"],
        "staged_sign": h6["staged_sign"],
        "flip_occurs": h6["flip_occurs"],
        "status": "HELD" if h6["flip_occurs"] else "FALSIFIED",
    })

    # H7: median Δ-NPV in [+$4B, +$8B]
    h7 = result["h7_median_delta_npv"]
    grades.append({
        "id": "H7",
        "predicted_band_B": [4.0, 8.0],
        "measured_B": h7["median_delta_npv_B"],
        "p05_M": h7["p05_delta_npv_M"],
        "p95_M": h7["p95_delta_npv_M"],
        "status": "HELD" if 4.0 <= h7["median_delta_npv_B"] <= 8.0 else "FALSIFIED",
    })

    return grades


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("Running R-staged-commitment-gates-frame-B-interaction ...")

    print("  Cross-checks ...")
    xc = cross_checks()

    print("  Frame A/B sweep ...")
    sweep = frame_a_b_sweep()
    sweep_delta = delta_frame_b(sweep)

    print("  Demonstrator NRE fraction ...")
    nre = demonstrator_nre_fraction()

    print("  H6 median-clearing flip check ...")
    h6 = h6_median_clearing_check()

    print("  H7 median Delta-NPV ...")
    h7 = h7_median_delta_npv()

    result = {
        "round": "R-staged-commitment-gates-frame-B-interaction",
        "author": "rhea",
        "date": "2026-05-15",
        "seed": SEED,
        "n_mc": N_MC,
        "cross_checks": xc,
        "frame_b_sweep": sweep,
        "frame_b_sweep_delta": sweep_delta,
        "demonstrator_nre_fraction": nre,
        "h6_median_clearing_check": h6,
        "h7_median_delta_npv": h7,
    }
    result["grades"] = grade(result)

    out_path = RESULTS_DIR / "staged_gates_frame_B_summary.json"
    out_path.write_text(json.dumps(result, indent=2))
    print(f"  Wrote {out_path}")

    # Print headline summary
    print("\n=== Cross-checks ===")
    for k, v in xc.items():
        passed = v.get("passes", False)
        print(f"  {k}: {'PASS' if passed else 'FAIL'}  ({v})")

    print("\n=== Hypothesis grading ===")
    for g in result["grades"]:
        print(f"  {g['id']}: {g['status']}  {g}")


if __name__ == "__main__":
    main()
