"""R-variant-B-recovery-paths-economic — bake-off pricing of Variant B amendment
paths against R-delivery-irr-curve's hurdle table.

Prices five paths (extending Saturn's three-path SCOPE with two assumption-
questioning additions) against the marginal-internal-rate-of-return cashflow
model from R-reactor-roadmap, with round-trip-time-corrected cadence and
programmatic-risk overlay from R-power-bayesian-update.

Paths under test:
  1 — variant C (Earth aerocapture mandatory), 500 kilowatt-electric, specific impulse 2000 s
  2 — null cell (no surviving cell at conservative assumptions)
  3 — variant A (no recovery), chunk reduced to ≤ 150 t per hyperion's pre-registration
  4 — variant D (Saturn-egress chemical kick + Earth aerocapture), added by rhea — the only
      path inside L0-05 hard ceiling at chunk 200 t under continuous-thrust accounting
  5 — Isp 3000 s sensitivity (assumption-questioning addition)

Assumptions questioned (see STUDY.md):
  - Saturn's three-path enumeration omits variant D, which closes L0-05 hard ceiling at
    chunk 200 t (14.67 yr round-trip). Adding it as path 4 surfaces a propulsion-physics
    finding the SCOPE.md does not surface.
  - R-delivery-irr-curve's default ROUND_TRIP_YR_MARVL = 14.5 yr is used regardless of
    delivered mass. For variant C (16.32 yr) and longer round-trips at chunk-cap
    relaxation upward, the round-trip penalty materially shifts marginal IRR — this
    round overrides ROUND_TRIP_YR_MARVL per path-and-chunk.
  - The water price assumption ($10,000/kg in BEST_CELL) is held fixed (sensitivity not
    under test; flagged as separate round candidate).

See STUDY.md for the pre-registered hypothesis block.
"""

from __future__ import annotations

import importlib.util
import json
import math
import sys
from pathlib import Path

ROUND_DIR = Path(__file__).resolve().parent
WATERPROP_ROOT = ROUND_DIR.parent.parent
ROUNDS_ROOT = ROUND_DIR.parent
RESULTS_DIR = ROUND_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


sys.path.insert(0, str(WATERPROP_ROOT / "src"))
sys.path.insert(0, str(ROUNDS_ROOT / "R_reactor_roadmap"))
sys.path.insert(0, str(ROUNDS_ROOT / "R_variant_B_impulsive_vs_continuous"))

vbic = _load_module("vbic", ROUNDS_ROOT / "R_variant_B_impulsive_vs_continuous" / "run.py")
rrr = _load_module("rrr", ROUNDS_ROOT / "R_reactor_roadmap" / "run.py")


REACTOR_KWE = 500.0
DEFAULT_DEPARTURE = "high_elliptical_1Mkm"
ISP_BASELINE_S = 2000.0
ISP_SENSITIVITY_S = 3000.0
CHUNK_BASELINE_T = 200.0
CHUNK_SWEEP_T = [100.0, 150.0, 200.0, 240.0, 300.0, 400.0, 482.0]
L0_05_HARD_YR = 15.0
L0_05_SOFT_YR = 16.0

HURDLES = {
    "sovereign_bond_4pct": 0.04,
    "regulated_utility_8pct": 0.08,
    "corporate_growth_10pct": 0.10,
}


def closure_for(variant: str, chunk_t: float, isp_s: float) -> dict:
    v = vbic.variant_inbound_dv(variant, DEFAULT_DEPARTURE)
    return vbic.variant_b_closure(
        reactor_kwe=REACTOR_KWE,
        chunk_t=chunk_t,
        isp_electric_s=isp_s,
        dv_chem_outbound_km_s=vbic.DV_CHEM_OUTBOUND_KM_S,
        dv_inbound_electric_km_s=v["electric_dv_km_s"],
        dv_inbound_impulsive_km_s=v["impulsive_egress_dv_km_s"],
        aerocapture=(variant in ("C_earth_aerocapture", "D_both")),
        m_outbound_kick_dry_t=vbic.M_OUTBOUND_KICK_DRY_T,
        m_saturn_kick_dry_t=vbic.M_SATURN_KICK_DRY_T,
    )


def marginal_irr_for(delivered_t: float, round_trip_yr: float, cdf: dict) -> dict:
    """Override R-reactor-roadmap's chunk and round-trip constants and recompute
    the conditional curve and marginal internal-rate-of-return."""
    rrr.MARVL_CHUNK_DELIVERED_T["Chemical_kick_500kWe"] = float(delivered_t)
    rrr.MARVL_CHUNK_DELIVERED_T["MW_1000kWe"] = float(delivered_t)
    rrr.ROUND_TRIP_YR_MARVL = float(round_trip_yr)
    curve = rrr.conditional_irr_curve(rrr.BEST_CELL, with_tv=True)
    marg = rrr.marginal_irr(curve, cdf)
    return {
        "marginal_irr": marg["marginal_irr"],
        "p_never_branch": marg["p_never_branch"],
        "irr_at_mw_year_10": curve["10"]["irr"],
        "irr_at_mw_year_20": curve["20"]["irr"],
        "irr_never_branch": curve["never"]["irr"],
    }


def l0_05_status(round_trip_yr: float) -> str:
    if round_trip_yr <= L0_05_HARD_YR:
        return "hard_pass"
    if round_trip_yr <= L0_05_SOFT_YR:
        return "soft_pass"
    return f"over_by_{round_trip_yr - L0_05_HARD_YR:.2f}yr"


def load_programmatic_priors() -> dict:
    overlay = json.loads(
        (ROUNDS_ROOT / "R_power_bayesian_update" / "results" / "matrix_overlay.json").read_text()
    )
    var_b = overlay["variant_B_500kWe_chemical_kick_plus_electric_inbound"]
    return {
        "uniform_beta_1_1": var_b["expected_delivered_mass_by_prior"]["uniform_beta_1_1"]["p_reactor_available_by_window"],
        "jeffreys_beta_0p5_0p5": var_b["expected_delivered_mass_by_prior"]["jeffreys_beta_0p5_0p5"]["p_reactor_available_by_window"],
        "skeptical_beta_0p5_5": var_b["expected_delivered_mass_by_prior"]["skeptical_beta_0p5_5"]["p_reactor_available_by_window"],
    }


def evaluate_path(path_id: str, variant: str | None, isp_s: float, chunk_t: float,
                  cdf: dict, priors: dict) -> dict:
    if variant is None:
        return {
            "path_id": path_id,
            "variant": None,
            "isp_s": isp_s,
            "chunk_t": chunk_t,
            "feasible": False,
            "reason": "null cell — no propulsion architecture under test",
            "delivered_t": 0.0,
            "round_trip_yr": math.inf,
            "l0_05_status": "n/a",
            "marginal_irr": None,
            "hurdle_status": {h: "fail" for h in HURDLES},
            "expected_delivered_by_prior": {p: 0.0 for p in priors},
        }
    cl = closure_for(variant, chunk_t, isp_s)
    if not cl.get("feasible"):
        return {
            "path_id": path_id,
            "variant": variant,
            "isp_s": isp_s,
            "chunk_t": chunk_t,
            "feasible": False,
            "reason": cl.get("reason"),
            "delivered_t": cl.get("delivered_t", 0.0),
            "round_trip_yr": math.inf,
            "l0_05_status": "infeasible",
            "marginal_irr": None,
            "hurdle_status": {h: "infeasible" for h in HURDLES},
            "expected_delivered_by_prior": {p: 0.0 for p in priors},
        }
    deliv = cl["delivered_t"]
    rt = cl["round_trip_yr"]
    irr = marginal_irr_for(max(deliv, 0.0), rt, cdf)
    hurdle_status = {}
    for name, h in HURDLES.items():
        hurdle_status[name] = "pass" if (irr["marginal_irr"] >= h) else "fail"
    return {
        "path_id": path_id,
        "variant": variant,
        "isp_s": isp_s,
        "chunk_t": chunk_t,
        "feasible": True,
        "delivered_t": deliv,
        "round_trip_yr": rt,
        "delivered_fraction": cl["delivered_fraction"],
        "m_tug_t": cl["m_tug_t"],
        "t_inbound_burn_yr": cl["t_inbound_burn_yr"],
        "l0_05_status": l0_05_status(rt),
        "marginal_irr": irr["marginal_irr"],
        "irr_detail": irr,
        "hurdle_status": hurdle_status,
        "expected_delivered_by_prior": {p: deliv * v for p, v in priors.items()},
    }


def main() -> dict:
    cdf = rrr.load_pbr_cdf()
    priors = load_programmatic_priors()

    paths = {
        "path_1_variant_C_baseline": {"variant": "C_earth_aerocapture", "isp_s": ISP_BASELINE_S},
        "path_3_variant_A_no_recovery": {"variant": "A_as_stated", "isp_s": ISP_BASELINE_S},
        "path_4_variant_D_both_recoveries": {"variant": "D_both", "isp_s": ISP_BASELINE_S},
        "path_5a_variant_C_isp3000": {"variant": "C_earth_aerocapture", "isp_s": ISP_SENSITIVITY_S},
        "path_5b_variant_D_isp3000": {"variant": "D_both", "isp_s": ISP_SENSITIVITY_S},
    }

    # 1. Baseline (chunk = 200 t) per path
    baselines = {}
    for pid, p in paths.items():
        baselines[pid] = evaluate_path(pid, p["variant"], p["isp_s"], CHUNK_BASELINE_T, cdf, priors)
    # Path 2 (null) — explicit row
    baselines["path_2_null"] = evaluate_path("path_2_null", None, ISP_BASELINE_S, 0.0, cdf, priors)

    # 2. Chunk sweep per path
    sweeps = {}
    for pid, p in paths.items():
        rows = []
        for c in CHUNK_SWEEP_T:
            rows.append(evaluate_path(pid, p["variant"], p["isp_s"], c, cdf, priors))
        sweeps[pid] = rows

    # 3. Programmatic-risk overlay — expected delivered per path per prior
    programmatic = {}
    for pid, row in baselines.items():
        if not row["feasible"]:
            programmatic[pid] = row["expected_delivered_by_prior"]
            continue
        programmatic[pid] = row["expected_delivered_by_prior"]

    # 4. Hypothesis grading — see STUDY.md for pre-registration text.

    h = {}

    # H-vrp-a: path 1 baseline marginal IRR ∈ [-2%, 2%]
    irr_p1 = baselines["path_1_variant_C_baseline"]["marginal_irr"]
    h["H-vrp-a_path_1_baseline_irr"] = {
        "predicted_range_pct": [-2.0, 2.0],
        "measured_pct": irr_p1 * 100 if irr_p1 is not None else None,
        "held": (irr_p1 is not None) and (-0.02 <= irr_p1 <= 0.02),
    }

    # H-vrp-b: path 1 + L1-007 → 482 t marginal IRR ∈ [0%, 5%]
    p1_482 = next(r for r in sweeps["path_1_variant_C_baseline"] if r["chunk_t"] == 482.0)
    irr_p1_482 = p1_482["marginal_irr"]
    h["H-vrp-b_path_1_chunk482_irr"] = {
        "predicted_range_pct": [0.0, 5.0],
        "measured_pct": irr_p1_482 * 100 if irr_p1_482 is not None else None,
        "held": (irr_p1_482 is not None) and (0.0 <= irr_p1_482 <= 0.05),
    }

    # H-vrp-c: path 3 (variant A) at chunk ≤ 150 t — propulsion-infeasible
    p3_at_100 = next(r for r in sweeps["path_3_variant_A_no_recovery"] if r["chunk_t"] == 100.0)
    p3_at_150 = next(r for r in sweeps["path_3_variant_A_no_recovery"] if r["chunk_t"] == 150.0)
    h["H-vrp-c_path_3_chunk_le_150_infeasible"] = {
        "predicted": "variant A at chunk ≤ 150 t is propulsion-infeasible (electric inbound prop > chunk inventory)",
        "measured_p3_at_100": p3_at_100["feasible"],
        "measured_p3_at_150": p3_at_150["feasible"],
        "held": (not p3_at_100["feasible"]) and (not p3_at_150["feasible"]),
    }

    # H-vrp-d: path 4 baseline IRR ∈ [-2%, 3%] AND L0-05 hard pass
    p4_base = baselines["path_4_variant_D_both_recoveries"]
    irr_p4 = p4_base["marginal_irr"]
    h["H-vrp-d_path_4_baseline_irr_and_L0_05"] = {
        "predicted_range_pct": [-2.0, 3.0],
        "predicted_l0_05": "hard_pass",
        "measured_pct": irr_p4 * 100 if irr_p4 is not None else None,
        "measured_l0_05": p4_base["l0_05_status"],
        "held": (irr_p4 is not None) and (-0.02 <= irr_p4 <= 0.03)
                and p4_base["l0_05_status"] == "hard_pass",
    }

    # H-vrp-e: path 4 + chunk → 482 t marginal IRR ∈ [-1%, 4%] AND round-trip ≤ 17 yr
    p4_482 = next(r for r in sweeps["path_4_variant_D_both_recoveries"] if r["chunk_t"] == 482.0)
    irr_p4_482 = p4_482["marginal_irr"]
    h["H-vrp-e_path_4_chunk482"] = {
        "predicted_range_pct": [-1.0, 4.0],
        "predicted_rt_yr_max": 17.0,
        "measured_pct": irr_p4_482 * 100 if irr_p4_482 is not None else None,
        "measured_rt_yr": p4_482["round_trip_yr"],
        "held": (irr_p4_482 is not None) and (-0.01 <= irr_p4_482 <= 0.04)
                and p4_482["round_trip_yr"] <= 17.0,
    }

    # H-vrp-f: NO path clears sovereign-bond hurdle (4%) at any L0-05-acceptable (≤ soft 16 yr) configuration.
    def passes_at_l0_05(row: dict) -> bool:
        return (row.get("feasible") and row.get("round_trip_yr", math.inf) <= L0_05_SOFT_YR
                and (row.get("marginal_irr") or 0.0) >= 0.04)
    any_sov_pass = False
    for rows in sweeps.values():
        for r in rows:
            if passes_at_l0_05(r):
                any_sov_pass = True
                break
        if any_sov_pass:
            break
    h["H-vrp-f_no_path_clears_sovereign_at_l0_05"] = {
        "predicted": "no path-and-chunk in the sweep clears sovereign-bond (4%) with round-trip ≤ 16 yr (soft L0-05)",
        "measured_any_pass": any_sov_pass,
        "held": (not any_sov_pass),
    }

    # H-vrp-g: SCOPE's 3-path enumeration omits variant D. This is a framing observation,
    # held a priori; codified by the existence of path 4 in this round.
    h["H-vrp-g_scope_omits_variant_D"] = {
        "predicted": "SCOPE.md's three-path enumeration (variant C / null / chunk-reduce variant A) "
                     "omits variant D (both recoveries), which is propulsion-physically defensible "
                     "AND the only path inside L0-05 hard ceiling at chunk 200 t.",
        "measured": (p4_base.get("l0_05_status") == "hard_pass"
                     and baselines["path_1_variant_C_baseline"]["l0_05_status"] != "hard_pass"
                     and baselines["path_1_variant_C_baseline"]["l0_05_status"] != "soft_pass"),
        "held": (p4_base.get("l0_05_status") == "hard_pass"
                 and baselines["path_1_variant_C_baseline"]["l0_05_status"] != "hard_pass"
                 and baselines["path_1_variant_C_baseline"]["l0_05_status"] != "soft_pass"),
    }

    # H-vrp-h: Isp 3000 s does NOT rescue the cell at L0-05-acceptable chunks.
    # Falsified if any path 5a/5b row at chunk ≤ 482 t has marginal IRR ≥ 4% AND round-trip ≤ 16 yr.
    isp3k_rescue = False
    for pid in ("path_5a_variant_C_isp3000", "path_5b_variant_D_isp3000"):
        for r in sweeps[pid]:
            if r.get("feasible") and r["round_trip_yr"] <= L0_05_SOFT_YR \
                    and (r.get("marginal_irr") or 0.0) >= 0.04:
                isp3k_rescue = True
                break
        if isp3k_rescue:
            break
    h["H-vrp-h_isp_3000_does_not_rescue"] = {
        "predicted": "specific impulse 3000 s does NOT rescue the cell at any L0-05-acceptable chunk",
        "measured_any_rescue": isp3k_rescue,
        "held": (not isp3k_rescue),
    }

    # H-vrp-i: under uniform prior, all feasible paths have expected delivered ≤ 0.5 t/mission.
    max_expected_uniform = 0.0
    for pid, row in baselines.items():
        if not row.get("feasible"):
            continue
        max_expected_uniform = max(max_expected_uniform,
                                   row["expected_delivered_by_prior"]["uniform_beta_1_1"])
    h["H-vrp-i_programmatic_uniform_le_0p5"] = {
        "predicted_max_expected_t_per_mission": 0.5,
        "measured_max": max_expected_uniform,
        "held": max_expected_uniform <= 0.5,
    }

    # 5. Path-vs-hurdle decision table — drive the project-owner-facing recommendation.
    # For each path, identify the best (chunk, IRR, round-trip) tuple subject to L0-05 hard pass,
    # then again subject to L0-05 soft pass.
    decision_table = {}
    for pid in paths:
        rows = sweeps[pid]
        best_hard = None
        best_soft = None
        for r in rows:
            if not r.get("feasible"):
                continue
            if r["l0_05_status"] == "hard_pass":
                if best_hard is None or (r["marginal_irr"] or -1) > (best_hard["marginal_irr"] or -1):
                    best_hard = r
            if r["l0_05_status"] in ("hard_pass", "soft_pass"):
                if best_soft is None or (r["marginal_irr"] or -1) > (best_soft["marginal_irr"] or -1):
                    best_soft = r
        decision_table[pid] = {
            "best_under_L0_05_hard": best_hard,
            "best_under_L0_05_soft": best_soft,
        }

    results = {
        "config": {
            "reactor_kwe": REACTOR_KWE,
            "departure_default": DEFAULT_DEPARTURE,
            "isp_baseline_s": ISP_BASELINE_S,
            "isp_sensitivity_s": ISP_SENSITIVITY_S,
            "chunk_baseline_t": CHUNK_BASELINE_T,
            "chunk_sweep_t": CHUNK_SWEEP_T,
            "L0_05_hard_yr": L0_05_HARD_YR,
            "L0_05_soft_yr": L0_05_SOFT_YR,
            "hurdles_pct": {k: v * 100 for k, v in HURDLES.items()},
            "BEST_CELL": rrr.BEST_CELL,
        },
        "priors": priors,
        "paths_baselines": baselines,
        "paths_sweeps": sweeps,
        "decision_table_per_path": decision_table,
        "hypothesis_grading": h,
    }
    (RESULTS_DIR / "R_variant_B_recovery_paths_economic.json").write_text(
        json.dumps(results, indent=2, default=str)
    )

    # 6. Tables.md — project-owner-facing comparison
    lines = []
    lines.append("# R-variant-B-recovery-paths-economic — tables\n")
    lines.append("## Path baselines (chunk = 200 t, specific impulse 2000 s unless noted)\n")
    lines.append("| Path | Variant | Isp (s) | Delivered (t) | Round-trip (yr) | L0-05 | Marginal IRR | Sovereign 4%? | Regulated 8%? | Corporate 10%? |")
    lines.append("|---|---|---:|---:|---:|---|---:|:---:|:---:|:---:|")
    for pid, r in baselines.items():
        if not r.get("feasible"):
            reason = r.get("reason") or "n/a"
            lines.append(f"| {pid} | {r['variant']} | {r['isp_s']:.0f} | INFEASIBLE: {reason} |  |  |  |  |  |  |")
            continue
        irr = r["marginal_irr"]
        irr_str = f"{irr*100:+.2f}%" if irr is not None else "n/a"
        sov = "✓" if r["hurdle_status"]["sovereign_bond_4pct"] == "pass" else "✗"
        reg = "✓" if r["hurdle_status"]["regulated_utility_8pct"] == "pass" else "✗"
        cor = "✓" if r["hurdle_status"]["corporate_growth_10pct"] == "pass" else "✗"
        lines.append(f"| {pid} | {r['variant']} | {r['isp_s']:.0f} | {r['delivered_t']:.2f} | "
                     f"{r['round_trip_yr']:.2f} | {r['l0_05_status']} | {irr_str} | {sov} | {reg} | {cor} |")
    lines.append("")

    lines.append("## Chunk sweep per path\n")
    for pid, rows in sweeps.items():
        lines.append(f"### {pid}\n")
        lines.append("| Chunk (t) | Feasible? | Delivered (t) | Round-trip (yr) | L0-05 status | Marginal IRR | Sov 4% | Reg 8% | Cor 10% |")
        lines.append("|---:|:---:|---:|---:|---|---:|:---:|:---:|:---:|")
        for r in rows:
            if not r.get("feasible"):
                lines.append(f"| {r['chunk_t']:.0f} | no | n/a | n/a | infeasible | n/a | – | – | – |")
                continue
            irr = r["marginal_irr"]
            irr_str = f"{irr*100:+.2f}%" if irr is not None else "n/a"
            sov = "✓" if r["hurdle_status"]["sovereign_bond_4pct"] == "pass" else "✗"
            reg = "✓" if r["hurdle_status"]["regulated_utility_8pct"] == "pass" else "✗"
            cor = "✓" if r["hurdle_status"]["corporate_growth_10pct"] == "pass" else "✗"
            lines.append(f"| {r['chunk_t']:.0f} | yes | {r['delivered_t']:.2f} | {r['round_trip_yr']:.2f} | "
                         f"{r['l0_05_status']} | {irr_str} | {sov} | {reg} | {cor} |")
        lines.append("")

    lines.append("## Decision table — best (chunk, IRR) per path subject to L0-05\n")
    lines.append("| Path | Best under hard L0-05 (≤15 yr) | Best under soft L0-05 (≤16 yr) |")
    lines.append("|---|---|---|")
    for pid, dt in decision_table.items():
        bh, bs = dt["best_under_L0_05_hard"], dt["best_under_L0_05_soft"]
        def cell(r):
            if not r:
                return "no L0-05-acceptable config"
            irr = r["marginal_irr"]
            irr_str = f"{irr*100:+.2f}%" if irr is not None else "n/a"
            return f"chunk {r['chunk_t']:.0f} t → {r['delivered_t']:.1f} t / RT {r['round_trip_yr']:.2f} yr / IRR {irr_str}"
        lines.append(f"| {pid} | {cell(bh)} | {cell(bs)} |")
    lines.append("")

    lines.append("## Programmatic-risk overlay (expected delivered per mission, chunk 200 t)\n")
    lines.append("| Path | Conditional delivered (t) | Uniform 8.9% | Jeffreys 4.9% | Skeptical 2.9% |")
    lines.append("|---|---:|---:|---:|---:|")
    for pid, r in baselines.items():
        if not r.get("feasible"):
            continue
        e = r["expected_delivered_by_prior"]
        lines.append(f"| {pid} | {r['delivered_t']:.2f} | "
                     f"{e['uniform_beta_1_1']:.4f} | {e['jeffreys_beta_0p5_0p5']:.4f} | "
                     f"{e['skeptical_beta_0p5_5']:.4f} |")
    lines.append("")

    lines.append("## Hypothesis grading\n")
    lines.append("| Sub-claim | Predicted | Measured | Held? |")
    lines.append("|---|---|---|:---:|")
    for k, v in h.items():
        pred = (str(v.get("predicted_range_pct"))
                if "predicted_range_pct" in v
                else str(v.get("predicted")))
        meas = (f"{v.get('measured_pct'):.2f}%"
                if "measured_pct" in v and v.get("measured_pct") is not None
                else str({kk: vv for kk, vv in v.items() if kk.startswith("measured")}))
        held = "✓" if v["held"] else "✗"
        lines.append(f"| {k} | {pred} | {meas} | {held} |")
    lines.append("")

    (RESULTS_DIR / "tables.md").write_text("\n".join(lines))
    return results


if __name__ == "__main__":
    out = main()
    print("R-variant-B-recovery-paths-economic complete.\n")
    print("Baselines (chunk 200 t):")
    for pid, r in out["paths_baselines"].items():
        if not r.get("feasible"):
            print(f"  {pid:42s}: INFEASIBLE — {r.get('reason', 'n/a')}")
            continue
        irr = r["marginal_irr"]
        irr_str = f"{irr*100:+5.2f}%" if irr is not None else " n/a "
        print(f"  {pid:42s}: deliv={r['delivered_t']:6.2f}t  RT={r['round_trip_yr']:5.2f}yr  "
              f"L0-05={r['l0_05_status']:>14s}  IRR={irr_str}")
    print()
    print("Hypothesis grading:")
    for k, v in out["hypothesis_grading"].items():
        print(f"  {k}: {'HELD' if v['held'] else 'FALSIFIED'}")
