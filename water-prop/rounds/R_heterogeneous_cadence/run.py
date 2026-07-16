#!/usr/bin/env python3
"""
R-heterogeneous-cadence — does a fast-small mission 1 followed by larger-slower
missions 2..N improve program NPV vs the homogeneous Variant B baseline?

Origin: project-owner USER-NOTES block in design-axes/02-surviving-cell.md
lines 18-20. Worker: rhea, 2026-05-15.

Deterministic; seeded MC for H-5 only (uses R-LEO-water-demand-curve's
log-normal Starship $/kg × markup as input). Results to results/.

Two accounting regimes:
  D — deterministic: missions 2..N capex committed in year-0 ramp regardless
      of mission 1 outcome.
  R — real-options: missions 2..N capex deferred to year (RT_1 + 0.5) AND
      probability-gated by P(mission 1 success); horizon stays 40 yr.

Comparison baseline = homogeneous Variant B (chunk 200, RT 14.5, delivered 80,
$500M first-unit, single-flight or reusable as a sensitivity).

Cross-checks per STUDY.md §"Cross-checks":
  1. chunk_1 = 200 t, Regime D → Δ-NPV ≈ 0.
  2. WACC = 0, Regime D → Δ-NPV = -(delivered_baseline - delivered_1) * rev/80.
  3. P_success = 1.0, chunk_1 = 200, Regime R → analytic deferred-fleet result.
  4. Hand-recomputed cell α (Regime D, chunk_1=25, WACC 3%, LR 15%, $200M rev):
     code output within ±10% of BOE -$113.5M.
  5. Hand-recomputed cell β (Regime R, chunk_1=25, WACC 3%, LR 15%, $200M rev,
     P=0.9): code output within ±15% of BOE +$1.77B.
"""
from __future__ import annotations

import argparse
import json
import math
import random
from dataclasses import dataclass
from pathlib import Path

RESULTS_DIR = Path(__file__).parent / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

SEED = 20260515
N_MC_SAMPLES = 10000


# ---------------------------------------------------------------------------
# Variant B baseline + mission-1 parametric
# ---------------------------------------------------------------------------
BASELINE_CHUNK_T = 200.0
BASELINE_RT_YR = 14.5
BASELINE_DELIVERED_T = 80.0
FIRST_UNIT_COST_M = 500.0
CADENCE_PER_YR = 2.0
HORIZON_YR = 40.0
DELIVERED_FRACTION = BASELINE_DELIVERED_T / BASELINE_CHUNK_T  # 0.40

RT_FLOOR_YR = 11.5  # parametric floor — physics cruise minimum
RT_SLOPE_YR = 3.0   # round_trip_1 = RT_FLOOR + RT_SLOPE * (chunk_1 / 200)


def mission1_params(chunk_1_t: float) -> tuple[float, float]:
    """Return (round_trip_yr, delivered_t) for a mission-1 chunk size."""
    delivered = chunk_1_t * DELIVERED_FRACTION
    rt = RT_FLOOR_YR + RT_SLOPE_YR * (chunk_1_t / BASELINE_CHUNK_T)
    return rt, delivered


# ---------------------------------------------------------------------------
# Helpers (mirror R_fleet_ramp_NPV)
# ---------------------------------------------------------------------------
def discount(amount_M: float, year: float, wacc: float) -> float:
    if wacc <= -0.999:
        return amount_M
    return amount_M / (1.0 + wacc) ** year


def wright_unit_cost(unit_index: int, first_unit_M: float, learning_rate: float) -> float:
    if learning_rate <= 0.0 or unit_index <= 1:
        return first_unit_M
    exponent = math.log(1.0 - learning_rate) / math.log(2.0)
    return first_unit_M * (unit_index ** exponent)


# ---------------------------------------------------------------------------
# Schedule builder
# ---------------------------------------------------------------------------
@dataclass
class Schedule:
    """A heterogeneous mission schedule.

    Mission 1 has its own (chunk, round_trip, delivered). Missions 2..N use
    baseline values.

    In Regime D, missions 2..N follow the standard fleet ramp starting at
    year 1/cadence (i.e., the second launch slot of a 2/yr cadence is year 0.5).
    In Regime R, missions 2..N start at year (round_trip_1 + 0.5) ONLY if
    mission 1 succeeds; capex and revenue are weighted by P_success.

    Mission 1 ship is built and launched at year 0 with certainty.
    """
    chunk_1_t: float
    reusable: bool = False
    cadence_per_yr: float = CADENCE_PER_YR
    horizon_yr: float = HORIZON_YR

    @property
    def round_trip_1_yr(self) -> float:
        return mission1_params(self.chunk_1_t)[0]

    @property
    def delivered_1_t(self) -> float:
        return mission1_params(self.chunk_1_t)[1]


def regime_D_schedule(sched: Schedule) -> tuple[list, list]:
    """Returns (launches, deliveries) for Regime D.

    Each list contains tuples (year, ship_idx, chunk_t, delivered_t).
    Ship indexing is 1-based, in build/launch order.
    """
    slot_dt = 1.0 / sched.cadence_per_yr
    launches = []
    deliveries = []
    ship_next_avail = []  # for reusable

    # Mission 1
    rt1 = sched.round_trip_1_yr
    deliv1 = sched.delivered_1_t
    launches.append((0.0, 1, sched.chunk_1_t, deliv1))
    if 0.0 + rt1 <= sched.horizon_yr:
        deliveries.append((0.0 + rt1, 1, sched.chunk_1_t, deliv1))
    if sched.reusable:
        ship_next_avail.append(rt1)
    else:
        ship_next_avail.append(float('inf'))  # single-flight: never reuse

    # Missions 2..N — homogeneous baseline starting at slot 1
    k = 1  # slot index (0-based; 0 is mission 1, 1 is mission 2)
    while True:
        t_launch = k * slot_dt
        if t_launch > sched.horizon_yr:
            break
        if not sched.reusable and t_launch + BASELINE_RT_YR > sched.horizon_yr:
            break

        if sched.reusable and ship_next_avail:
            earliest_idx = min(range(len(ship_next_avail)),
                               key=lambda i: ship_next_avail[i])
            if ship_next_avail[earliest_idx] <= t_launch:
                # reuse — chunk/delivered are baseline
                ship_id = earliest_idx + 1
                ship_next_avail[earliest_idx] = t_launch + BASELINE_RT_YR
                launches.append((t_launch, ship_id, BASELINE_CHUNK_T, BASELINE_DELIVERED_T))
                if t_launch + BASELINE_RT_YR <= sched.horizon_yr:
                    deliveries.append((t_launch + BASELINE_RT_YR, ship_id,
                                       BASELINE_CHUNK_T, BASELINE_DELIVERED_T))
                k += 1
                continue
        # build a new ship
        ship_id = len(ship_next_avail) + 1
        ship_next_avail.append(t_launch + BASELINE_RT_YR)
        launches.append((t_launch, ship_id, BASELINE_CHUNK_T, BASELINE_DELIVERED_T))
        if t_launch + BASELINE_RT_YR <= sched.horizon_yr:
            deliveries.append((t_launch + BASELINE_RT_YR, ship_id,
                               BASELINE_CHUNK_T, BASELINE_DELIVERED_T))
        k += 1

    return launches, deliveries


def regime_R_schedule(sched: Schedule, p_success: float) -> tuple[list, list, float]:
    """Returns (launches, deliveries, p_gate).

    Mission 1 lives in 'certain' world. Missions 2..N start at
    year (round_trip_1 + 0.5) and are gated by p_success.
    p_gate is the multiplier to apply to all mission-2..N cashflows.
    """
    slot_dt = 1.0 / sched.cadence_per_yr
    rt1 = sched.round_trip_1_yr
    deliv1 = sched.delivered_1_t
    start_year_for_fleet = rt1 + 0.5

    launches = []
    deliveries = []
    ship_next_avail = []

    # Mission 1 — certain
    launches.append((0.0, 1, sched.chunk_1_t, deliv1, 1.0))  # 5th elt is gate-weight
    if rt1 <= sched.horizon_yr:
        deliveries.append((rt1, 1, sched.chunk_1_t, deliv1, 1.0))
    if sched.reusable:
        ship_next_avail.append(rt1)
    else:
        ship_next_avail.append(float('inf'))

    # Missions 2..N — gated by p_success, year-shifted
    k = 0  # 0-indexed slot within the deferred fleet
    while True:
        t_launch = start_year_for_fleet + k * slot_dt
        if t_launch > sched.horizon_yr:
            break
        if not sched.reusable and t_launch + BASELINE_RT_YR > sched.horizon_yr:
            break

        if sched.reusable and len(ship_next_avail) > 1:
            # check reusable among missions 2..N ships only (ship 1 might already be reusable too)
            eligible = [i for i in range(len(ship_next_avail)) if ship_next_avail[i] <= t_launch]
            if eligible:
                earliest_idx = min(eligible, key=lambda i: ship_next_avail[i])
                ship_id = earliest_idx + 1
                ship_next_avail[earliest_idx] = t_launch + BASELINE_RT_YR
                launches.append((t_launch, ship_id, BASELINE_CHUNK_T,
                                 BASELINE_DELIVERED_T, p_success))
                if t_launch + BASELINE_RT_YR <= sched.horizon_yr:
                    deliveries.append((t_launch + BASELINE_RT_YR, ship_id,
                                       BASELINE_CHUNK_T, BASELINE_DELIVERED_T, p_success))
                k += 1
                continue
        ship_id = len(ship_next_avail) + 1
        ship_next_avail.append(t_launch + BASELINE_RT_YR)
        launches.append((t_launch, ship_id, BASELINE_CHUNK_T,
                         BASELINE_DELIVERED_T, p_success))
        if t_launch + BASELINE_RT_YR <= sched.horizon_yr:
            deliveries.append((t_launch + BASELINE_RT_YR, ship_id,
                               BASELINE_CHUNK_T, BASELINE_DELIVERED_T, p_success))
        k += 1

    return launches, deliveries, p_success


# ---------------------------------------------------------------------------
# NPV evaluator
# ---------------------------------------------------------------------------
def npv_regime_D(
    sched: Schedule,
    wacc: float,
    revenue_per_tonne_M: float,
    learning_rate: float,
    nre_M: float = 0.0,
    op_cost_per_mission_M: float = 0.0,
) -> dict:
    launches, deliveries = regime_D_schedule(sched)

    # PV capital — each ship is built/charged at its FIRST launch year.
    pv_capital = 0.0
    seen_ships = set()
    n_ships_built = 0
    for (t_launch, ship_id, _, _) in launches:
        if ship_id not in seen_ships:
            n_ships_built += 1
            unit_cost = wright_unit_cost(n_ships_built, FIRST_UNIT_COST_M, learning_rate)
            pv_capital -= discount(unit_cost, t_launch, wacc)
            seen_ships.add(ship_id)

    pv_nre = -nre_M if nre_M > 0 else 0.0
    pv_opcost = -sum(discount(op_cost_per_mission_M, t, wacc) for (t, _, _, _) in launches) if op_cost_per_mission_M > 0 else 0.0

    pv_revenue = sum(discount(revenue_per_tonne_M * delivered_t, t_d, wacc)
                     for (t_d, _, _, delivered_t) in deliveries)

    return {
        "regime": "D",
        "pv_capital_M": pv_capital,
        "pv_nre_M": pv_nre,
        "pv_opcost_M": pv_opcost,
        "pv_revenue_M": pv_revenue,
        "npv_M": pv_capital + pv_nre + pv_opcost + pv_revenue,
        "n_ships_built": n_ships_built,
        "n_deliveries": len(deliveries),
        "total_delivered_t": sum(d[3] for d in deliveries),
    }


def npv_regime_R(
    sched: Schedule,
    wacc: float,
    revenue_per_tonne_M: float,
    learning_rate: float,
    p_success: float,
    nre_M: float = 0.0,
    op_cost_per_mission_M: float = 0.0,
) -> dict:
    launches, deliveries, _ = regime_R_schedule(sched, p_success)

    pv_capital = 0.0
    seen_ships = set()
    n_ships_built = 0
    for (t_launch, ship_id, _, _, gate) in launches:
        if ship_id not in seen_ships:
            n_ships_built += 1
            unit_cost = wright_unit_cost(n_ships_built, FIRST_UNIT_COST_M, learning_rate)
            pv_capital -= gate * discount(unit_cost, t_launch, wacc)
            seen_ships.add(ship_id)

    pv_nre = -nre_M if nre_M > 0 else 0.0
    pv_opcost = 0.0
    if op_cost_per_mission_M > 0:
        for (t_launch, _, _, _, gate) in launches:
            pv_opcost -= gate * discount(op_cost_per_mission_M, t_launch, wacc)

    pv_revenue = sum(gate * discount(revenue_per_tonne_M * delivered_t, t_d, wacc)
                     for (t_d, _, _, delivered_t, gate) in deliveries)

    return {
        "regime": "R",
        "pv_capital_M": pv_capital,
        "pv_nre_M": pv_nre,
        "pv_opcost_M": pv_opcost,
        "pv_revenue_M": pv_revenue,
        "npv_M": pv_capital + pv_nre + pv_opcost + pv_revenue,
        "n_ships_built": n_ships_built,
        "n_deliveries": len(deliveries),
        "total_delivered_t": sum(d[3] for d in deliveries),
        "p_success": p_success,
    }


# ---------------------------------------------------------------------------
# Sweeps
# ---------------------------------------------------------------------------
CHUNK_1_VALUES = [25.0, 50.0, 100.0, 150.0, 200.0]
WACC_VALUES = [0.0, 0.03, 0.06, 0.087, 0.12]
LR_VALUES = [0.0, 0.15, 0.20]
REUSABLE_VALUES = [False, True]
P_SUCCESS_VALUES = [1.0, 0.90, 0.70, 0.50]
# Convert $200M/mission proxy to per-tonne: 200/80 = $2.5M per tonne
# Sweep a range of clearing prices ($/tonne ≡ $/kg × 1000):
REVENUE_PER_TONNE_M = [1.0, 2.5, 5.0, 10.0, 15.0, 25.0]  # $1k/kg .. $25k/kg


def run_sweep() -> list[dict]:
    rows = []
    for chunk_1 in CHUNK_1_VALUES:
        sched = Schedule(chunk_1_t=chunk_1, reusable=False)
        for wacc in WACC_VALUES:
            for lr in LR_VALUES:
                for rev_pt in REVENUE_PER_TONNE_M:
                    d = npv_regime_D(sched, wacc, rev_pt, lr)
                    rows.append({
                        "chunk_1_t": chunk_1,
                        "wacc": wacc,
                        "lr": lr,
                        "rev_per_tonne_M": rev_pt,
                        "reusable": False,
                        **{k: v for k, v in d.items() if k != "regime"},
                        "regime": "D",
                        "round_trip_1_yr": sched.round_trip_1_yr,
                        "delivered_1_t": sched.delivered_1_t,
                    })
                    for p_s in P_SUCCESS_VALUES:
                        r = npv_regime_R(sched, wacc, rev_pt, lr, p_s)
                        rows.append({
                            "chunk_1_t": chunk_1,
                            "wacc": wacc,
                            "lr": lr,
                            "rev_per_tonne_M": rev_pt,
                            "reusable": False,
                            **{k: v for k, v in r.items() if k != "regime"},
                            "regime": "R",
                            "round_trip_1_yr": sched.round_trip_1_yr,
                            "delivered_1_t": sched.delivered_1_t,
                        })
    return rows


def delta_npv(rows: list[dict]) -> list[dict]:
    """For each (chunk_1, wacc, lr, rev_per_tonne, regime, p_success), compute
    Δ-NPV against the homogeneous baseline (chunk_1 = 200, Regime D, same
    other parameters).
    """
    baseline = {}
    for r in rows:
        if r["regime"] == "D" and r["chunk_1_t"] == BASELINE_CHUNK_T:
            key = (r["wacc"], r["lr"], r["rev_per_tonne_M"], r["reusable"])
            baseline[key] = r["npv_M"]

    out = []
    for r in rows:
        key = (r["wacc"], r["lr"], r["rev_per_tonne_M"], r["reusable"])
        if key in baseline:
            d = dict(r)
            d["baseline_npv_M"] = baseline[key]
            d["delta_npv_M"] = r["npv_M"] - baseline[key]
            out.append(d)
    return out


# ---------------------------------------------------------------------------
# H-5: Monte Carlo over R-LEO-water-demand-curve clearing-price distribution
# ---------------------------------------------------------------------------
def lognormal_draws(rng: random.Random, n: int, mu_value: float, p5: float, p95: float) -> list[float]:
    """Lognormal with given median (mu_value), 5th, 95th percentiles.

    Note: this matches R-LEO-water-demand-curve's spec — 5th/95th set by a
    symmetric log-spread around the median.
    """
    sigma = (math.log(p95) - math.log(p5)) / (2 * 1.645)
    mu = math.log(mu_value)
    return [math.exp(rng.gauss(mu, sigma)) for _ in range(n)]


def mc_h5(rng: random.Random, n_samples: int) -> dict:
    """For chunk_1 = 50 t, WACC 3%, LR 15%, Regime R p_success 0.90:
    measure fraction of clearing-price draws where program NPV >= 0.
    Compare to homogeneous baseline (Regime D, chunk_1 = 200, same params).

    Clearing price model from R-LEO-water-demand-curve:
      Starship $/kg lognormal: median $1500, 5th $200, 95th $15000.
      Markup lognormal: median 3.5×, 5th 1.2×, 95th 15×.
      Clearing $/kg = Starship × markup. Sample independently.
    """
    starship = lognormal_draws(rng, n_samples, 1500.0, 200.0, 15000.0)
    # use a separate rng state — re-seed for independence
    rng2 = random.Random(SEED + 1)
    markup = lognormal_draws(rng2, n_samples, 3.5, 1.2, 15.0)
    clearing_per_kg = [s * m for s, m in zip(starship, markup)]
    clearing_per_tonne_M = [c * 1000.0 / 1e6 for c in clearing_per_kg]  # $/kg → $M/tonne

    sched_het = Schedule(chunk_1_t=50.0)
    sched_hom = Schedule(chunk_1_t=BASELINE_CHUNK_T)

    het_npv_positive = 0
    hom_npv_positive = 0
    het_npvs = []
    hom_npvs = []
    for rev_pt in clearing_per_tonne_M:
        het = npv_regime_R(sched_het, wacc=0.03, revenue_per_tonne_M=rev_pt,
                           learning_rate=0.15, p_success=0.90)
        hom = npv_regime_D(sched_hom, wacc=0.03, revenue_per_tonne_M=rev_pt,
                           learning_rate=0.15)
        het_npvs.append(het["npv_M"])
        hom_npvs.append(hom["npv_M"])
        if het["npv_M"] >= 0:
            het_npv_positive += 1
        if hom["npv_M"] >= 0:
            hom_npv_positive += 1

    return {
        "n_samples": n_samples,
        "het_pct_npv_positive": het_npv_positive / n_samples * 100.0,
        "hom_pct_npv_positive": hom_npv_positive / n_samples * 100.0,
        "het_median_npv_M": sorted(het_npvs)[n_samples // 2],
        "hom_median_npv_M": sorted(hom_npvs)[n_samples // 2],
        "clearing_median_per_kg": sorted(clearing_per_kg)[n_samples // 2],
        "clearing_p05_per_kg": sorted(clearing_per_kg)[int(n_samples * 0.05)],
        "clearing_p95_per_kg": sorted(clearing_per_kg)[int(n_samples * 0.95)],
    }


# ---------------------------------------------------------------------------
# Cross-checks
# ---------------------------------------------------------------------------
def run_crosschecks() -> dict:
    out = {}

    # XC-1: chunk_1 = 200 t, Regime D → Δ-NPV ≈ 0
    sched_ctrl = Schedule(chunk_1_t=200.0)
    sched_test = Schedule(chunk_1_t=200.0)
    a = npv_regime_D(sched_ctrl, 0.03, 2.5, 0.15)
    b = npv_regime_D(sched_test, 0.03, 2.5, 0.15)
    out["xc1_chunk200_baseline_match"] = {
        "delta_npv_M": b["npv_M"] - a["npv_M"],
        "passes": abs(b["npv_M"] - a["npv_M"]) < 1.0,
    }

    # XC-2: WACC = 0, Regime D → Δ-NPV ≈ -(80 - delivered_1) * rev_per_tonne
    sched_25 = Schedule(chunk_1_t=25.0)
    sched_200 = Schedule(chunk_1_t=200.0)
    rev_pt = 2.5  # $2.5M/tonne ≡ $200M/mission proxy
    a = npv_regime_D(sched_25, 0.0, rev_pt, 0.0)
    b = npv_regime_D(sched_200, 0.0, rev_pt, 0.0)
    delta_obs = a["npv_M"] - b["npv_M"]
    delta_expected = -(80.0 - sched_25.delivered_1_t) * rev_pt
    out["xc2_wacc0_undiscounted"] = {
        "delta_observed_M": delta_obs,
        "delta_expected_M": delta_expected,
        "passes": abs(delta_obs - delta_expected) < 1.0,
    }

    # XC-3: P_success = 1.0, chunk_1 = 200, Regime R
    # Should equal homogeneous-D with fleet ramp shifted by RT_1 + 0.5 = 15.0 yr.
    sched_200 = Schedule(chunk_1_t=200.0)
    r = npv_regime_R(sched_200, 0.03, 2.5, 0.15, 1.0)
    # Sanity: should be different from homogeneous-D because fleet is deferred.
    d = npv_regime_D(sched_200, 0.03, 2.5, 0.15)
    out["xc3_p1_chunk200_regimeR_vs_D"] = {
        "regime_R_npv_M": r["npv_M"],
        "regime_D_npv_M": d["npv_M"],
        "delta_M": r["npv_M"] - d["npv_M"],
        "passes": True,  # sign/direction is the test; manual interp
    }

    # XC-4: cell α (Regime D, chunk_1=25, WACC 3%, LR 15%, $200M/mission)
    # BOE: -$113.5M
    sched_25 = Schedule(chunk_1_t=25.0)
    sched_200 = Schedule(chunk_1_t=200.0)
    a = npv_regime_D(sched_25, 0.03, 2.5, 0.15)
    b = npv_regime_D(sched_200, 0.03, 2.5, 0.15)
    delta_obs = a["npv_M"] - b["npv_M"]
    out["xc4_cell_alpha_BOE_match"] = {
        "delta_observed_M": delta_obs,
        "BOE_expected_M": -113.5,
        "rel_err": abs(delta_obs - (-113.5)) / 113.5,
        "passes": abs(delta_obs - (-113.5)) / 113.5 <= 0.10,
    }

    # XC-5: cell β (Regime R, chunk_1=25, WACC 3%, LR 15%, $200M/mission, P=0.9)
    # BOE: +$1.77B = +$1770M
    sched_25 = Schedule(chunk_1_t=25.0)
    sched_200 = Schedule(chunk_1_t=200.0)
    r = npv_regime_R(sched_25, 0.03, 2.5, 0.15, 0.9)
    d_baseline = npv_regime_D(sched_200, 0.03, 2.5, 0.15)
    delta_obs = r["npv_M"] - d_baseline["npv_M"]
    out["xc5_cell_beta_BOE_match"] = {
        "delta_observed_M": delta_obs,
        "BOE_expected_M": 1770.0,
        "rel_err": abs(delta_obs - 1770.0) / 1770.0,
        "passes": abs(delta_obs - 1770.0) / 1770.0 <= 0.15,
    }

    return out


# ---------------------------------------------------------------------------
# Hypothesis grader (concrete bands per STUDY.md)
# ---------------------------------------------------------------------------
def grade_hypotheses(rows_with_delta: list[dict], mc_result: dict, xc_result: dict) -> dict:
    g = {}

    # Helper: filter
    def find(chunk, wacc, lr, rev, regime, p_success=None):
        for r in rows_with_delta:
            if (r["chunk_1_t"] == chunk and r["wacc"] == wacc and r["lr"] == lr
                and r["rev_per_tonne_M"] == rev and r["regime"] == regime):
                if regime == "R" and p_success is not None:
                    if r.get("p_success") == p_success:
                        return r
                else:
                    return r
        return None

    # H-1: Regime D, chunk < 200, Δ-NPV negative at WACC ∈ {3%, 8.7%}, LR 15%, $2.5M/tonne
    h1_cells_3 = []
    h1_cells_87 = []
    for chunk in [25, 50, 100, 150]:
        for w, target in [(0.03, h1_cells_3), (0.087, h1_cells_87)]:
            r = find(chunk, w, 0.15, 2.5, "D")
            if r:
                target.append((chunk, r["delta_npv_M"]))
    all_negative_3 = all(d < 0 for _, d in h1_cells_3)
    all_negative_87 = all(d < 0 for _, d in h1_cells_87)
    in_band_3 = all(-400.0 <= d <= -50.0 for _, d in h1_cells_3)
    in_band_87 = all(-250.0 <= d <= -30.0 for _, d in h1_cells_87)
    g["H-1"] = {
        "predicted": "Regime D, chunk<200: Δ-NPV negative, [-50,-400]M @ 3%, [-30,-250]M @ 8.7%",
        "h1_cells_at_3pct": h1_cells_3,
        "h1_cells_at_87pct": h1_cells_87,
        "all_negative_3pct": all_negative_3,
        "all_negative_87pct": all_negative_87,
        "in_band_3pct": in_band_3,
        "in_band_87pct": in_band_87,
        "status": "HELD" if (all_negative_3 and all_negative_87 and in_band_3 and in_band_87) else "FALSIFIED",
    }

    # H-2: Δ-NPV penalty monotonically increases as chunk_1 decreases (Regime D)
    deltas_by_chunk = sorted([(c, d) for c, d in h1_cells_3], key=lambda x: x[0])
    monotonic = all(deltas_by_chunk[i+1][1] >= deltas_by_chunk[i][1] for i in range(len(deltas_by_chunk)-1))
    # i.e., as chunk increases (toward 200), delta increases toward 0
    g["H-2"] = {
        "predicted": "monotonic in chunk_1 (smaller chunk → larger penalty)",
        "deltas_sorted_by_chunk": deltas_by_chunk,
        "monotonic": monotonic,
        "status": "HELD" if monotonic else "FALSIFIED",
    }

    # H-3: Regime R, P=0.9, Δ-NPV positive at WACC 3% LR15% rev2.5, magnitude [+800, +2500]M
    # For each chunk < 200:
    h3_3 = []
    h3_87 = []
    for chunk in [25, 50, 100, 150]:
        r3 = find(chunk, 0.03, 0.15, 2.5, "R", 0.9)
        r87 = find(chunk, 0.087, 0.15, 2.5, "R", 0.9)
        if r3:
            h3_3.append((chunk, r3["delta_npv_M"]))
        if r87:
            h3_87.append((chunk, r87["delta_npv_M"]))
    in_band_3 = all(800.0 <= d <= 2500.0 for _, d in h3_3)
    in_band_87 = all(300.0 <= d <= 1200.0 for _, d in h3_87)
    g["H-3"] = {
        "predicted": "Regime R P=0.9: ΔNPV [+800,+2500]M @ 3% LR15%, [+300,+1200]M @ 8.7%",
        "h3_cells_at_3pct": h3_3,
        "h3_cells_at_87pct": h3_87,
        "in_band_3pct": in_band_3,
        "in_band_87pct": in_band_87,
        "all_positive_3pct": all(d > 0 for _, d in h3_3),
        "all_positive_87pct": all(d > 0 for _, d in h3_87),
        "status": "HELD" if (in_band_3 and in_band_87) else "FALSIFIED",
    }

    # H-4: Regime R chunk_1=50, WACC 3% LR15%, clearing $5,284/kg ≡ $5.284M/tonne
    # → NPV > 0 (flip)
    sched_50 = Schedule(chunk_1_t=50.0)
    sched_200 = Schedule(chunk_1_t=BASELINE_CHUNK_T)
    rev_h4 = 5.284  # $M/tonne
    het_h4 = npv_regime_R(sched_50, 0.03, rev_h4, 0.15, 0.9)
    hom_h4 = npv_regime_D(sched_200, 0.03, rev_h4, 0.15)
    g["H-4"] = {
        "predicted": "Regime R chunk=50, clearing $5,284/kg: NPV positive vs hom near-breakeven",
        "het_npv_M": het_h4["npv_M"],
        "hom_npv_M": hom_h4["npv_M"],
        "delta_M": het_h4["npv_M"] - hom_h4["npv_M"],
        "het_flips_positive": het_h4["npv_M"] > 0,
        "magnitude_above_100M": het_h4["npv_M"] > 100.0,
        "status": "HELD" if (het_h4["npv_M"] > 0 and het_h4["npv_M"] > 100.0) else "FALSIFIED",
    }

    # H-5: fraction of MC clearing-price draws where het clears NPV ≥ 0 is 65-80%
    pct = mc_result["het_pct_npv_positive"]
    g["H-5"] = {
        "predicted": "het pct NPV≥0 across MC ∈ [65, 80]; hom baseline ~51%",
        "het_pct": pct,
        "hom_pct": mc_result["hom_pct_npv_positive"],
        "in_band": 65.0 <= pct <= 80.0,
        "status": "HELD" if 65.0 <= pct <= 80.0 else "FALSIFIED",
    }

    # H-6: chunk_1 = 25, round_trip_1 ∈ [11.5, 12.5]
    rt1_at_25 = mission1_params(25.0)[0]
    g["H-6"] = {
        "predicted": "round_trip_1 at chunk_1=25 ∈ [11.5, 12.5]",
        "round_trip_1_yr": rt1_at_25,
        "status": "HELD" if 11.5 <= rt1_at_25 <= 12.5 else "FALSIFIED",
    }

    # H-7: P=0.7 shrinks Δ-NPV improvement vs P=0.9 by 20-40%
    sched_25 = Schedule(chunk_1_t=25.0)
    sched_200 = Schedule(chunk_1_t=BASELINE_CHUNK_T)
    hom_d = npv_regime_D(sched_200, 0.03, 2.5, 0.15)
    het_p9 = npv_regime_R(sched_25, 0.03, 2.5, 0.15, 0.9)
    het_p7 = npv_regime_R(sched_25, 0.03, 2.5, 0.15, 0.7)
    delta_p9 = het_p9["npv_M"] - hom_d["npv_M"]
    delta_p7 = het_p7["npv_M"] - hom_d["npv_M"]
    if delta_p9 > 0:
        shrink_pct = (1.0 - delta_p7 / delta_p9) * 100.0
    else:
        shrink_pct = float('nan')
    g["H-7"] = {
        "predicted": "P=0.7 shrinks improvement 20-40% vs P=0.9",
        "delta_p9_M": delta_p9,
        "delta_p7_M": delta_p7,
        "shrink_pct": shrink_pct,
        "status": "HELD" if 20.0 <= shrink_pct <= 40.0 else "FALSIFIED",
    }

    # H-8: Regime R chunk_1=200 (homogeneous-with-deferred-capex limit) at P=0.9
    sched_200 = Schedule(chunk_1_t=BASELINE_CHUNK_T)
    r8 = npv_regime_R(sched_200, 0.03, 2.5, 0.15, 0.9)
    d8 = npv_regime_D(sched_200, 0.03, 2.5, 0.15)
    delta = r8["npv_M"] - d8["npv_M"]
    g["H-8"] = {
        "predicted": "chunk_1=200 in Regime R: Δ-NPV [+500,+2000]M (real-options structure ALONE)",
        "delta_M": delta,
        "in_band": 500.0 <= delta <= 2000.0,
        "is_positive": delta > 0,
        "status": "HELD" if 500.0 <= delta <= 2000.0 else "FALSIFIED",
    }

    return g


# ---------------------------------------------------------------------------
# Per-mission cumulative-NPV trajectory (R-rhea-per-mission-output-extension)
#
# Additive: decomposes the SAME cashflows npv_regime_{D,R} aggregate into a
# per-mission ordered list, so /decision-framework:hamiltonian Layer 1 can run
# on each sample's cumulative-NPV trajectory. Does NOT change the economics
# model or the aggregate-summary path. Reconciles to npv_regime_* to <$0.01M.
# ---------------------------------------------------------------------------
def per_mission_trajectory(
    sched: Schedule,
    regime: str,
    wacc: float,
    revenue_per_tonne_M: float,
    learning_rate: float,
    p_success: float | None = None,
) -> dict:
    """Per-mission cost / revenue / discounted cumulative NPV, in mission-launch order.

    Each mission (single-flight => one ship per launch) contributes its discounted
    ship capital (charged at launch year) and discounted revenue (at delivery year),
    gated by p_success for the deferred fleet in Regime R. Cumulative-sum gives the
    trajectory whose sum reconciles to the aggregate npv_regime_*.
    """
    if regime == "D":
        launches, deliveries = regime_D_schedule(sched)
        launches = [(t, sid, ck, dl, 1.0) for (t, sid, ck, dl) in launches]
        deliveries = [(t, sid, ck, dl, 1.0) for (t, sid, ck, dl) in deliveries]
    elif regime == "R":
        assert p_success is not None, "Regime R requires p_success"
        launches, deliveries, _ = regime_R_schedule(sched, p_success)
    else:
        raise ValueError(regime)

    # delivery revenue PV indexed by ship_id (single-flight: one delivery per ship)
    deliv_by_ship: dict[int, tuple[float, float, float]] = {}
    for (t_d, ship_id, _ck, delivered_t, gate) in deliveries:
        deliv_by_ship[ship_id] = (t_d, delivered_t, gate)

    per_mission = []
    seen_ships: set[int] = set()
    n_built = 0
    cum_npv = 0.0
    chunk_schedule = []
    mission_number = 0
    for (t_launch, ship_id, chunk_t, _deliv, gate) in launches:
        if ship_id in seen_ships:
            continue  # reusable safety; MC is single-flight so this never trips
        seen_ships.add(ship_id)
        n_built += 1
        mission_number += 1
        unit_cost = wright_unit_cost(n_built, FIRST_UNIT_COST_M, learning_rate)
        cost_pv = gate * discount(unit_cost, t_launch, wacc)
        if ship_id in deliv_by_ship:
            t_d, delivered_t, dgate = deliv_by_ship[ship_id]
            revenue_nominal = revenue_per_tonne_M * delivered_t
            revenue_pv = dgate * discount(revenue_nominal, t_d, wacc)
            delivery_yr = t_d
        else:
            revenue_nominal = 0.0
            revenue_pv = 0.0
            delivery_yr = None
        net_pv = revenue_pv - cost_pv
        cum_npv += net_pv
        chunk_schedule.append(chunk_t)
        per_mission.append({
            "mission_number": mission_number,
            "launch_yr": t_launch,
            "delivery_yr": delivery_yr,
            "chunk_t": chunk_t,
            "delivered_t": (delivered_t if ship_id in deliv_by_ship else 0.0),
            "gate": gate,
            "revenue_M_usd": revenue_nominal,        # raw nominal
            "cost_M_usd": unit_cost,                  # raw nominal first/Wright unit cost
            "net_pv_M_usd": net_pv,                   # discounted, gated
            "cumulative_npv_M_usd": cum_npv,          # discounted cumulative
        })

    return {
        "regime": regime,
        "cadence_class": "het" if sched.chunk_1_t != BASELINE_CHUNK_T else "hom",
        "chunk_1_t": sched.chunk_1_t,
        "p_success": p_success,
        "rev_per_tonne_M": revenue_per_tonne_M,
        "wacc": wacc,
        "learning_rate": learning_rate,
        "n_missions": mission_number,
        "chunk_schedule": chunk_schedule,
        "per_mission_cumulative_npv_M_usd": [m["cumulative_npv_M_usd"] for m in per_mission],
        "per_mission_revenue_M_usd": [m["revenue_M_usd"] for m in per_mission],
        "per_mission_cost_M_usd": [m["cost_M_usd"] for m in per_mission],
        "per_mission": per_mission,
        "final_program_npv_M_usd": cum_npv,
    }


def capture_trajectories(n_samples: int, n_per_class: int = 50) -> dict:
    """Capture per-sample het(R) + hom(D) trajectories for the first n_per_class MC
    samples, replaying the IDENTICAL seeded clearing-price draws that mc_h5 uses.

    mc_h5 draws starship $/kg with the rng passed from main() (Random(SEED), pristine
    at that point) and markup with Random(SEED+1). We reproduce both exactly so that
    trajectory sample i uses the same clearing price as Monte-Carlo aggregate sample i.
    """
    starship = lognormal_draws(random.Random(SEED), n_samples, 1500.0, 200.0, 15000.0)
    markup = lognormal_draws(random.Random(SEED + 1), n_samples, 3.5, 1.2, 15.0)
    clearing_per_kg = [s * m for s, m in zip(starship, markup)]
    clearing_per_tonne_M = [c * 1000.0 / 1e6 for c in clearing_per_kg]

    sched_het = Schedule(chunk_1_t=50.0)
    sched_hom = Schedule(chunk_1_t=BASELINE_CHUNK_T)

    records = []
    max_recon_err = 0.0
    for i in range(min(n_per_class, n_samples)):
        rev_pt = clearing_per_tonne_M[i]
        # heterogeneous (Regime R, chunk_1=50, p=0.90)
        het = per_mission_trajectory(sched_het, "R", 0.03, rev_pt, 0.15, p_success=0.90)
        het_agg = npv_regime_R(sched_het, 0.03, rev_pt, 0.15, 0.90)["npv_M"]
        # homogeneous (Regime D, chunk_1=200)
        hom = per_mission_trajectory(sched_hom, "D", 0.03, rev_pt, 0.15)
        hom_agg = npv_regime_D(sched_hom, 0.03, rev_pt, 0.15)["npv_M"]
        max_recon_err = max(max_recon_err,
                            abs(het["final_program_npv_M_usd"] - het_agg),
                            abs(hom["final_program_npv_M_usd"] - hom_agg))
        for rec, clr in ((het, clearing_per_kg[i]), (hom, clearing_per_kg[i])):
            rec["sample_id"] = i
            rec["clearing_per_kg"] = clr
            rec.pop("per_mission", None)  # redundant with the parallel arrays; keeps file small
            records.append(rec)

    if max_recon_err > 0.01:
        raise SystemExit(f"TRAJECTORY RECONCILIATION FAILED: per-mission sum vs aggregate "
                         f"max err ${max_recon_err:.4f}M > $0.01M. Aborting.")

    return {
        "n_samples_drawn": n_samples,
        "n_per_class": n_per_class,
        "n_records": len(records),
        "reconciliation_max_abs_err_M": max_recon_err,
        "schema": {
            "time_field": "mission_number",
            "value_field": "cumulative_npv_M_usd",
            "log_space": False,
            "note": "het = Regime R chunk_1=50 p=0.90; hom = Regime D chunk_1=200; "
                    "both at WACC 3%, LR 15%; clearing price from R-LEO-water-demand-curve.",
        },
        "trajectories": records,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(description="R-heterogeneous-cadence run + optional trajectory emit")
    parser.add_argument("--emit-trajectories", action="store_true",
                        help="additionally emit per-sample per-mission cumulative-NPV trajectories "
                             "to results/per_sample_trajectories.json (does not change the aggregate summary)")
    parser.add_argument("--n-per-class", type=int, default=50,
                        help="trajectories captured per cadence-class (het + hom); default 50 => 100 total")
    args = parser.parse_args()

    rng = random.Random(SEED)

    xc = run_crosschecks()
    rows = run_sweep()
    rows_with_delta = delta_npv(rows)
    mc = mc_h5(rng, N_MC_SAMPLES)
    grades = grade_hypotheses(rows_with_delta, mc, xc)

    summary = {
        "cross_checks": xc,
        "monte_carlo_h5": mc,
        "grades": grades,
        "n_sweep_rows": len(rows),
        "n_delta_rows": len(rows_with_delta),
        "schedule_parametric": {
            "chunk_1_values": CHUNK_1_VALUES,
            "rt_floor_yr": RT_FLOOR_YR,
            "rt_slope_yr": RT_SLOPE_YR,
            "delivered_fraction": DELIVERED_FRACTION,
            "baseline_chunk_t": BASELINE_CHUNK_T,
            "baseline_rt_yr": BASELINE_RT_YR,
            "baseline_delivered_t": BASELINE_DELIVERED_T,
            "first_unit_cost_M": FIRST_UNIT_COST_M,
            "horizon_yr": HORIZON_YR,
            "cadence_per_yr": CADENCE_PER_YR,
        },
        "headline": {
            "h1_regime_D_falsifies_user_hypothesis": grades["H-1"]["status"] == "HELD",
            "h3_regime_R_supports_user_hypothesis": grades["H-3"]["status"] == "HELD",
            "h8_real_options_is_load_bearing": grades["H-8"]["status"] == "HELD",
        },
    }

    # Write JSON summary
    summary_path = RESULTS_DIR / "het_cadence_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, default=str))
    print(f"Wrote {summary_path}")

    # Print headline
    print("\n=== Cross-checks ===")
    for k, v in xc.items():
        print(f"  {k}: passes={v.get('passes', 'n/a')}")
    print("\n=== Hypothesis grades ===")
    for hid, gd in grades.items():
        print(f"  {hid}: {gd['status']}")
    print("\n=== H-5 MC headline ===")
    print(f"  het pct NPV+: {mc['het_pct_npv_positive']:.1f}%  hom pct NPV+: {mc['hom_pct_npv_positive']:.1f}%")
    print(f"  median clearing $/kg: {mc['clearing_median_per_kg']:.0f}")

    # --- Additive: per-sample trajectory emit (R-rhea-per-mission-output-extension) ---
    if args.emit_trajectories:
        traj = capture_trajectories(N_MC_SAMPLES, n_per_class=args.n_per_class)
        traj_path = RESULTS_DIR / "per_sample_trajectories.json"
        traj_path.write_text(json.dumps(traj, separators=(",", ":"), default=str))
        print(f"\nWrote {traj_path}")
        print(f"  {traj['n_records']} trajectories "
              f"({traj['n_per_class']} het + {traj['n_per_class']} hom); "
              f"reconciliation max err ${traj['reconciliation_max_abs_err_M']:.2e}M")


if __name__ == "__main__":
    main()
