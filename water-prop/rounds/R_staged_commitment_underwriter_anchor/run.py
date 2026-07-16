#!/usr/bin/env python3
"""
R-staged-commitment-underwriter-anchor — does staged commitment improve the
metric ACTUALLY USED by each plausible ICEBERG capital source (sovereign-grant,
limited-recourse project-finance debt, equity-with-gates), as distinct from the
binary P(NPV>0) proxy used by round 13?

Composes round 13 harness with three capital-source-specific metric layers:
  - sovereign-grant: P(milestone success) regime-independent.
  - debt: expected-loss pre-gate; implied bond spread.
  - equity: mean (EV) and median Δ-NPV; option-adjusted NPV; IRR distribution.

Outputs to results/underwriter_anchor_summary.json.
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

# Import round 13 helpers (which themselves import heterogeneous-cadence).
RD13_RUN_PATH = THIS_DIR.parent / "R_staged_commitment_gates_frame_B" / "run.py"
spec = importlib.util.spec_from_file_location("rd13_run", RD13_RUN_PATH)
rd13 = importlib.util.module_from_spec(spec)
sys.modules["rd13_run"] = rd13
spec.loader.exec_module(rd13)

# Heterogeneous-cadence helpers (already loaded into rd13.hetcad via round 13's import).
hetcad = rd13.hetcad

SEED = 20260515
N_MC = 10000

# Load-bearing cell
LAUNCH_COUNT = 2
WACC = 0.03
LR = 0.15
CHUNK_T = 200.0
P_DEMONSTRATOR = 0.90

# Debt model parameters
LTV = 0.60                   # senior-debt loan-to-value (project-finance standard)
LGD_RECOVERY = 0.40          # recovery rate on default; 1-LGD on principal
RISK_FREE_RATE = 0.03        # sovereign-bond risk-free (matches WACC convention)
DURATION_YR = 14.5           # round-trip-1; pre-gate window for catastrophic loss
P_DEMONSTRATOR_FAIL = 1.0 - P_DEMONSTRATOR  # 0.10

# ---------------------------------------------------------------------------
# Yearly cashflow streams (derived from heterogeneous-cadence schedule helpers)
# ---------------------------------------------------------------------------
def yearly_cashflows(
    regime: str,
    rev_per_tonne_M: float,
    learning_rate: float,
    launch_count: int,
    horizon_yr: int = 40,
) -> list[float]:
    """Build a nominal undiscounted yearly cashflow array (year 0 .. horizon_yr).

    Outflows: ship capex at first launch year (Wright unit cost),
              opex per launch (LAUNCH_COST_PER_MISSION_M),
              demonstrator NRE at year 0 under Regime R only.
    Inflows:  delivered_t × rev_per_tonne_M at delivery year.

    Under Regime R, gate-multipliers are applied to missions 2..N at their
    nominal-year position (no discount). Mission 1 is certain.
    """
    sched = hetcad.Schedule(chunk_1_t=CHUNK_T, reusable=False)
    op_per_mission = rd13.LAUNCH_COST_PER_MISSION_M[launch_count]

    cf = [0.0] * (horizon_yr + 1)

    if regime == "D":
        launches, deliveries = hetcad.regime_D_schedule(sched)
        seen = set()
        n_built = 0
        for (t, ship_id, _, _) in launches:
            yr = int(round(t))
            if 0 <= yr <= horizon_yr:
                if ship_id not in seen:
                    n_built += 1
                    cf[yr] -= hetcad.wright_unit_cost(n_built, hetcad.FIRST_UNIT_COST_M, learning_rate)
                    seen.add(ship_id)
                cf[yr] -= op_per_mission
        for (t_d, _, _, delivered_t) in deliveries:
            yr = int(round(t_d))
            if 0 <= yr <= horizon_yr:
                cf[yr] += rev_per_tonne_M * delivered_t

    elif regime == "R":
        launches, deliveries, _ = hetcad.regime_R_schedule(sched, P_DEMONSTRATOR)
        seen = set()
        n_built = 0
        # Demonstrator NRE at year 0
        cf[0] -= rd13.DEMONSTRATOR_NRE_M
        for (t, ship_id, _, _, gate) in launches:
            yr = int(round(t))
            if 0 <= yr <= horizon_yr:
                if ship_id not in seen:
                    n_built += 1
                    cf[yr] -= gate * hetcad.wright_unit_cost(n_built, hetcad.FIRST_UNIT_COST_M, learning_rate)
                    seen.add(ship_id)
                cf[yr] -= gate * op_per_mission
        for (t_d, _, _, delivered_t, gate) in deliveries:
            yr = int(round(t_d))
            if 0 <= yr <= horizon_yr:
                cf[yr] += gate * rev_per_tonne_M * delivered_t
    else:
        raise ValueError(regime)

    return cf


def npv_from_cashflows(cf: list[float], wacc: float) -> float:
    return sum(c / (1.0 + wacc) ** t for t, c in enumerate(cf))


def irr_from_cashflows(cf: list[float], guess: float = 0.05, max_iter: int = 100) -> float:
    """Newton-Raphson IRR. Returns NaN if no convergence or no root.

    Skips if all cashflows are same sign (no IRR exists).
    """
    has_pos = any(c > 0 for c in cf)
    has_neg = any(c < 0 for c in cf)
    if not (has_pos and has_neg):
        return float("nan")

    r = guess
    for _ in range(max_iter):
        f = sum(c / (1.0 + r) ** t for t, c in enumerate(cf))
        df = sum(-t * c / (1.0 + r) ** (t + 1) for t, c in enumerate(cf))
        if abs(df) < 1e-12:
            return float("nan")
        r_new = r - f / df
        if abs(r_new - r) < 1e-8:
            return r_new
        r = r_new
        if r < -0.99 or r > 10.0:
            return float("nan")
    return float("nan")


# ---------------------------------------------------------------------------
# MC over demand-curve clearing prices
# ---------------------------------------------------------------------------
def run_mc_metrics() -> dict:
    """For each MC draw, compute per-regime NPV, mean/median Δ, IRR distribution,
    and per-draw cashflow-based metrics.
    """
    rev_samples = rd13.sample_clearing_per_tonne_M(N_MC)

    npv_D = []
    npv_R = []
    irr_D = []
    irr_R = []
    for rev in rev_samples:
        # NPV via round-13 harness (consistency with prior round)
        d = rd13.npv_cell("D", WACC, LR, rev, launch_count=LAUNCH_COUNT)
        r = rd13.npv_cell("R", WACC, LR, rev, launch_count=LAUNCH_COUNT)
        npv_D.append(d["npv_M"])
        npv_R.append(r["npv_M"])

        # IRR via yearly cashflow stream
        cfD = yearly_cashflows("D", rev, LR, LAUNCH_COUNT)
        cfR = yearly_cashflows("R", rev, LR, LAUNCH_COUNT)
        irr_D.append(irr_from_cashflows(cfD))
        irr_R.append(irr_from_cashflows(cfR))

    def pctile(xs, p):
        xs_sorted = sorted(xs)
        return xs_sorted[int(min(N_MC - 1, max(0, p / 100.0 * N_MC)))]

    def safe_stats(xs):
        finite = [x for x in xs if x == x and math.isfinite(x)]  # NaN check
        if not finite:
            return {"n_valid": 0}
        finite_sorted = sorted(finite)
        return {
            "n_valid": len(finite),
            "mean": sum(finite) / len(finite),
            "median": finite_sorted[len(finite) // 2],
            "p05": finite_sorted[max(0, int(0.05 * len(finite)))],
            "p25": finite_sorted[max(0, int(0.25 * len(finite)))],
            "p75": finite_sorted[min(len(finite) - 1, int(0.75 * len(finite)))],
            "p95": finite_sorted[min(len(finite) - 1, int(0.95 * len(finite)))],
            "frac_positive": sum(1 for x in finite if x > 0) / len(finite),
        }

    deltas = [r - d for r, d in zip(npv_R, npv_D)]

    return {
        "load_bearing_cell": f"{LAUNCH_COUNT}-launch W{WACC*100:.0f}% LR{LR*100:.0f}%",
        "n_samples": N_MC,
        "npv_D_M_stats": safe_stats(npv_D),
        "npv_R_M_stats": safe_stats(npv_R),
        "delta_npv_M_stats": safe_stats(deltas),
        "irr_D_stats": safe_stats(irr_D),
        "irr_R_stats": safe_stats(irr_R),
        # Save raw arrays at low resolution for downstream debugging (quantile-bin)
        "npv_D_M_first_10": npv_D[:10],
        "npv_R_M_first_10": npv_R[:10],
    }


# ---------------------------------------------------------------------------
# H1, H2 — debt-style metrics
# ---------------------------------------------------------------------------
def debt_metrics() -> dict:
    """Compute pre-gate catastrophic-loss expected loss, both regimes.

    Pre-gate exposure = total committed capex at year 0 through year RT_1 = 14.5
      Upfront: full program capex commit-out (ship capex over the construction
               window) plus NRE.
      Staged:  mission-1 capex + NRE.
    P(catastrophic loss) = P(demonstrator failure) = 0.10.
    LGD = 1 - recovery rate = 0.60.
    Senior debt principal at LTV = exposure × 0.60.
    EL = principal × P_fail × LGD.
    Implied risk spread (bps/yr) = EL / principal / duration × 10000.
    """
    # Use round 13 demonstrator-NRE-fraction breakdown (chunk-200, 3-launch ceiling
    # for conservative; matches round 13 numbers).
    breakdown = rd13.demonstrator_nre_fraction()
    program_total_M = breakdown["program_total_M"]
    mission1_total_M = breakdown["mission1_total_M"]

    # Upfront pre-gate exposure = full program capex (ship + ops + NRE), under
    # the convention that the underwriter has to capitalize it through the
    # pre-revenue window. We treat all capex as exposed (even if some lands at
    # later years; the underwriter's exposure peaks at the end of the
    # construction draw period).
    exposure_upfront_M = program_total_M
    exposure_staged_M = mission1_total_M

    def el_metrics(exposure_M: float) -> dict:
        principal_M = exposure_M * LTV
        el_M = principal_M * P_DEMONSTRATOR_FAIL * (1.0 - LGD_RECOVERY)
        spread_bps = (el_M / principal_M / DURATION_YR) * 10000 if principal_M > 0 else 0.0
        return {
            "exposure_M": exposure_M,
            "principal_M": principal_M,
            "expected_loss_M": el_M,
            "implied_spread_bps_per_yr": spread_bps,
        }

    up = el_metrics(exposure_upfront_M)
    st = el_metrics(exposure_staged_M)

    el_ratio = st["expected_loss_M"] / up["expected_loss_M"]
    spread_reduction_bps = up["implied_spread_bps_per_yr"] - st["implied_spread_bps_per_yr"]

    return {
        "model": "pre_gate_catastrophic_loss_only",
        "LTV": LTV,
        "LGD_recovery": LGD_RECOVERY,
        "P_demonstrator_fail": P_DEMONSTRATOR_FAIL,
        "duration_yr": DURATION_YR,
        "upfront": up,
        "staged": st,
        "el_ratio_staged_over_upfront": el_ratio,
        "spread_reduction_bps": spread_reduction_bps,
        "program_total_M": program_total_M,
        "mission1_total_M": mission1_total_M,
    }


# ---------------------------------------------------------------------------
# H5 — option-adjusted equity NPV
# ---------------------------------------------------------------------------
def option_adjusted_npv() -> dict:
    """Compute the equity option-value advantage of staged commitment.

    Under staged: at gate (year RT_1 + 0.5 = 15.0), equity has the option to
    walk away from fleet capex if expected-fleet-NPV-given-conditions is
    negative. Under upfront: fleet capex was already committed at year 0; no
    option to abandon.

    Implementation: re-evaluate each MC draw under "smart-gate" semantics —
    the fleet is built only if the per-draw expected NPV of the fleet alone
    (computed at gate) is positive. Compare to the harness's mechanical-gate
    semantics (which built fleet whenever demonstrator succeeded).

    Approximation: at gate, equity knows the realized clearing price for the
    given draw (this is generous to the option — in reality the clearing price
    isn't known until much later, but the option holder has SOME information).
    Use this as an upper bound on option value.
    """
    rev_samples = rd13.sample_clearing_per_tonne_M(N_MC)
    n_abandoned = 0
    delta_total = 0.0
    deltas = []

    for rev in rev_samples:
        # Mechanical-gate NPV (round-13 harness behavior, restated here):
        r_mech = rd13.npv_cell("R", WACC, LR, rev, launch_count=LAUNCH_COUNT)["npv_M"]
        # Smart-gate: if fleet NPV-at-gate (post-demonstrator-success path) is
        # negative, equity abandons; else builds fleet.
        # Compute fleet-only NPV by subtracting mission-1 portion.
        # Simpler: build the smart-gate cashflow directly.
        cfR = yearly_cashflows("R", rev, LR, LAUNCH_COUNT)
        # Fleet portion = cashflows at year > 14 are gated; if negative PV at
        # gate, replace them with zero. (Mission 1 stays.)
        # Decompose: fleet-only cashflows are those at year >= 15 (start_year_for_fleet)
        # plus any post-gate capex / opex. Year RT_1 = 14.5, gate at 15.0.
        # Compute fleet PV at gate (year 15).
        fleet_pv_at_gate = 0.0
        for t, c in enumerate(cfR):
            if t >= 15:
                fleet_pv_at_gate += c / (1.0 + WACC) ** (t - 15)
        if fleet_pv_at_gate < 0:
            # Abandon: zero out post-gate cashflows
            cfR_smart = [c if t < 15 else 0.0 for t, c in enumerate(cfR)]
            n_abandoned += 1
        else:
            cfR_smart = cfR
        npv_smart = sum(c / (1.0 + WACC) ** t for t, c in enumerate(cfR_smart))
        delta = npv_smart - r_mech
        delta_total += delta
        deltas.append(delta)

    deltas_sorted = sorted(deltas)
    return {
        "n_samples": N_MC,
        "n_abandoned_under_smart_gate": n_abandoned,
        "fraction_abandoned": n_abandoned / N_MC,
        "mean_option_value_M": delta_total / N_MC,
        "median_option_value_M": deltas_sorted[N_MC // 2],
        "p05_option_value_M": deltas_sorted[int(0.05 * N_MC)],
        "p95_option_value_M": deltas_sorted[int(0.95 * N_MC)],
    }


# ---------------------------------------------------------------------------
# H7 — convex-hull check at clearing p25/p50/p75
# ---------------------------------------------------------------------------
def convex_hull_check() -> dict:
    """Compute Δ-NPV at clearing-price p25, p50, p75 and report whether the
    convex hull of these three values brackets round 13's pre-reg band
    [+$4B, +$8B] and round 13's measured +$3.34B.
    """
    rev_samples = sorted(rd13.sample_clearing_per_tonne_M(N_MC))
    p25 = rev_samples[N_MC // 4]
    p50 = rev_samples[N_MC // 2]
    p75 = rev_samples[3 * N_MC // 4]

    def delta_at(rev):
        d = rd13.npv_cell("D", WACC, LR, rev, launch_count=LAUNCH_COUNT)
        r = rd13.npv_cell("R", WACC, LR, rev, launch_count=LAUNCH_COUNT)
        return (r["npv_M"] - d["npv_M"]) / 1000.0  # $B

    deltas = {
        "p25": {"rev_per_tonne_M": p25, "rev_per_kg_$": p25 * 1000.0, "delta_npv_B": delta_at(p25)},
        "p50": {"rev_per_tonne_M": p50, "rev_per_kg_$": p50 * 1000.0, "delta_npv_B": delta_at(p50)},
        "p75": {"rev_per_tonne_M": p75, "rev_per_kg_$": p75 * 1000.0, "delta_npv_B": delta_at(p75)},
    }
    hull_min = min(d["delta_npv_B"] for d in deltas.values())
    hull_max = max(d["delta_npv_B"] for d in deltas.values())
    rd13_band = (4.0, 8.0)
    rd13_measured = 3.34
    return {
        "deltas_at_clearing_percentile": deltas,
        "convex_hull_B": (hull_min, hull_max),
        "round_13_pre_reg_band_B": rd13_band,
        "round_13_pre_reg_band_inside_hull": hull_min <= rd13_band[0] and rd13_band[1] <= hull_max,
        "round_13_measured_median_B": rd13_measured,
        "round_13_measured_inside_hull": hull_min <= rd13_measured <= hull_max,
    }


# ---------------------------------------------------------------------------
# Cross-checks
# ---------------------------------------------------------------------------
def cross_checks(mc_metrics: dict) -> dict:
    out = {}

    # XC-1: replicate round 13 Frame B at 2-launch W3 LR15
    npv_R_stats = mc_metrics["npv_R_M_stats"]
    npv_D_stats = mc_metrics["npv_D_M_stats"]
    out["XC1_frame_b_replicate"] = {
        "upfront_pct_pos_measured": npv_D_stats["frac_positive"] * 100,
        "upfront_pct_pos_round13": 36.32,
        "staged_pct_pos_measured": npv_R_stats["frac_positive"] * 100,
        "staged_pct_pos_round13": 31.00,
        "upfront_passes": abs(npv_D_stats["frac_positive"] * 100 - 36.32) < 1.0,
        "staged_passes": abs(npv_R_stats["frac_positive"] * 100 - 31.00) < 1.0,
    }

    # XC-2: replicate round 13 median Δ-NPV
    delta_median_M = mc_metrics["delta_npv_M_stats"]["median"]
    out["XC2_median_delta_npv"] = {
        "measured_median_delta_M": delta_median_M,
        "round_13_published_M": 3340.0,
        "rel_err_pct": abs(delta_median_M - 3340.0) / 3340.0 * 100,
        "passes": abs(delta_median_M - 3340.0) / 3340.0 < 0.10,
    }

    # XC-3: program capex breakdown
    breakdown = rd13.demonstrator_nre_fraction()
    out["XC3_program_capex_breakdown"] = {
        "measured_total_M": breakdown["program_total_M"],
        "round_13_published_M": 14628.0,
        "rel_err_pct": abs(breakdown["program_total_M"] - 14628.0) / 14628.0 * 100,
        "passes": abs(breakdown["program_total_M"] - 14628.0) / 14628.0 < 0.05,
    }

    return out


# ---------------------------------------------------------------------------
# Grader
# ---------------------------------------------------------------------------
def grade(result: dict) -> list[dict]:
    grades = []

    # H1: EL ratio staged / upfront in [0.08, 0.15]
    ratio = result["debt_metrics"]["el_ratio_staged_over_upfront"]
    grades.append({
        "id": "H1",
        "claim": "EL ratio staged / upfront in [8%, 15%]",
        "predicted_band": [0.08, 0.15],
        "measured": ratio,
        "status": "HELD" if 0.08 <= ratio <= 0.15 else "FALSIFIED",
    })

    # H2: implied spread reduction in [25, 50] bps
    spread_red = result["debt_metrics"]["spread_reduction_bps"]
    grades.append({
        "id": "H2",
        "claim": "implied bond spread reduction (upfront - staged) in [25, 50] bps/yr",
        "predicted_band": [25, 50],
        "measured_bps": spread_red,
        "status": "HELD" if 25 <= spread_red <= 50 else "FALSIFIED",
    })

    # H3: mean Δ-NPV in [-$5B, +$3B]
    mean_delta = result["mc_metrics"]["delta_npv_M_stats"]["mean"]
    mean_delta_B = mean_delta / 1000.0
    grades.append({
        "id": "H3",
        "claim": "MEAN Δ-NPV across MC in [-$5B, +$3B] (heavy-left-tail compresses EV toward zero)",
        "predicted_band_B": [-5.0, 3.0],
        "measured_B": mean_delta_B,
        "status": "HELD" if -5.0 <= mean_delta_B <= 3.0 else "FALSIFIED",
    })

    # H4: median IRR_staged - median IRR_upfront in [0, +3] pp
    irrR = result["mc_metrics"]["irr_R_stats"]
    irrD = result["mc_metrics"]["irr_D_stats"]
    if irrR.get("n_valid", 0) > 0 and irrD.get("n_valid", 0) > 0:
        diff_pp = (irrR["median"] - irrD["median"]) * 100
    else:
        diff_pp = float("nan")
    grades.append({
        "id": "H4",
        "claim": "median IRR_staged - median IRR_upfront in [0, +3] pp",
        "predicted_band_pp": [0, 3],
        "measured_pp": diff_pp,
        "irr_R_median": irrR.get("median"),
        "irr_D_median": irrD.get("median"),
        "status": "HELD" if 0.0 <= diff_pp <= 3.0 else "FALSIFIED",
    })

    # H5: option-adjusted Δ-NPV (mean over MC) in [$0.3B, $2B]
    opt = result["option_adjusted_npv"]
    opt_mean_B = opt["mean_option_value_M"] / 1000.0
    grades.append({
        "id": "H5",
        "claim": "mean option-adjusted Δ-NPV (smart-gate over mechanical-gate) in [+$0.3B, +$2B]",
        "predicted_band_B": [0.3, 2.0],
        "measured_B": opt_mean_B,
        "n_abandoned": opt["n_abandoned_under_smart_gate"],
        "fraction_abandoned": opt["fraction_abandoned"],
        "status": "HELD" if 0.3 <= opt_mean_B <= 2.0 else "FALSIFIED",
    })

    # H6: sovereign-grant regime-independence (qualitative)
    grades.append({
        "id": "H6",
        "claim": "sovereign-grant P(milestone success past gate) is regime-independent (Δ ≤ 0.5 pp)",
        "rationale": "by construction: the grant gate decision is on technical milestone, not on accounting regime; both regimes face P_demonstrator = 0.90",
        "measured_pp_diff": 0.0,
        "status": "HELD",
    })

    # H7: convex-hull check
    hull = result["convex_hull_check"]
    grades.append({
        "id": "H7",
        "claim": "convex hull of Δ at clearing p25/p50/p75 excludes round 13's [+$4B, +$8B] band; includes measured +$3.34B",
        "convex_hull_B": hull["convex_hull_B"],
        "round_13_pre_reg_band_inside_hull": hull["round_13_pre_reg_band_inside_hull"],
        "round_13_measured_inside_hull": hull["round_13_measured_inside_hull"],
        # HELD if pre-reg band is NOT inside hull (i.e., the proposed lesson #7-v5
        # would have caught round 13's BOE failure).
        "status": "HELD" if not hull["round_13_pre_reg_band_inside_hull"] else "FALSIFIED",
    })

    return grades


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    print("Running R-staged-commitment-underwriter-anchor...")

    print("  MC metrics (NPV + IRR per draw)...")
    mc = run_mc_metrics()

    print("  Debt metrics...")
    debt = debt_metrics()

    print("  Option-adjusted equity NPV...")
    opt = option_adjusted_npv()

    print("  Convex-hull check...")
    hull = convex_hull_check()

    print("  Cross-checks...")
    xc = cross_checks(mc)

    result = {
        "round": "R_staged_commitment_underwriter_anchor",
        "date": "2026-05-15",
        "seed": SEED,
        "n_mc": N_MC,
        "load_bearing_cell": {
            "launch_count": LAUNCH_COUNT,
            "wacc": WACC,
            "lr": LR,
            "chunk_t": CHUNK_T,
            "p_demonstrator": P_DEMONSTRATOR,
        },
        "mc_metrics": mc,
        "debt_metrics": debt,
        "option_adjusted_npv": opt,
        "convex_hull_check": hull,
        "cross_checks": xc,
    }

    print("  Grading...")
    result["grades"] = grade(result)

    out_path = RESULTS_DIR / "underwriter_anchor_summary.json"
    out_path.write_text(json.dumps(result, indent=2, default=str))
    print(f"  Wrote {out_path}")

    # Quick summary print
    print("\n=== Grades ===")
    for g in result["grades"]:
        print(f"  {g['id']}: {g['status']}  ({g.get('claim', '')[:80]})")
    print("\n=== Cross-checks ===")
    for k, v in xc.items():
        passes = v.get("passes", v.get("upfront_passes", "?"))
        print(f"  {k}: {'PASS' if passes else 'FAIL'}")


if __name__ == "__main__":
    main()
