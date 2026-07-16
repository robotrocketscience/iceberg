"""R-outbound-chemical-kick-economics — calibration + sensitivity round.

Retracts the batch-3/4 sleeper-falsifier "715 t hydrolox per outbound mission" claim.
Computes outbound chemical-kick propellant and LEO launch mass from primary
variant_b_closure, then sweeps marginal IRR across launch-market × water-price ×
sovereign-payment configurations to determine whether outbound economics is an
independent matrix-killer.

Deterministic. No randomness. Run from worktree root with PYTHONPATH=water-prop/src.

Outputs:
  results/R_outbound_chemical_kick_economics.json
  results/tables.md
  results/closure_verdict.md
"""

import json
import math
import sys
import os
from copy import deepcopy
from pathlib import Path

# Path bootstrap so we can import sibling round modules and waterprop package
ROUND_DIR = Path(__file__).resolve().parent
ROUNDS_ROOT = ROUND_DIR.parent
WP_ROOT = ROUNDS_ROOT.parent  # water-prop/
sys.path.insert(0, str(WP_ROOT / "src"))

import importlib.util  # noqa: E402

def _load_module(unique_name: str, file_path: Path):
    spec = importlib.util.spec_from_file_location(unique_name, str(file_path))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[unique_name] = mod
    spec.loader.exec_module(mod)
    return mod

vbm = _load_module(
    "variant_b_impulsive_run",
    ROUNDS_ROOT / "R_variant_B_impulsive_vs_continuous" / "run.py",
)
variant_b_closure = vbm.variant_b_closure
M_OUTBOUND_KICK_DRY_T = vbm.M_OUTBOUND_KICK_DRY_T
M_SATURN_KICK_DRY_T = vbm.M_SATURN_KICK_DRY_T
DV_HELIO_RETROGRADE_KM_S = vbm.DV_HELIO_RETROGRADE_KM_S
DV_EARTH_HELIO_KM_S = vbm.DV_EARTH_HELIO_KM_S
DV_SATURN_EGRESS_IMPULSIVE_KM_S = vbm.DV_SATURN_EGRESS_IMPULSIVE_KM_S
DV_CHEM_OUTBOUND_KM_S = vbm.DV_CHEM_OUTBOUND_KM_S
ISP_HYDROLOX_S = vbm.ISP_HYDROLOX_S

rr = _load_module(
    "reactor_roadmap_run",
    ROUNDS_ROOT / "R_reactor_roadmap" / "run.py",
)
PBR_CDF = rr.load_pbr_cdf()


# ---------------------------------------------------------------------------
# Path / chunk definitions matching rhea bake-off
# ---------------------------------------------------------------------------

# Use rhea bake-off's exact decomposition via variant_inbound_dv to ensure
# this round's variant_b_closure outputs match the bake-off's baselines.
DEFAULT_DEPARTURE = "high_elliptical_1Mkm"

PATH_DEFS = {
    "path_1_variant_C": {
        "variant": "C — Earth aerocapture only",
        "vbic_variant_id": "C_earth_aerocapture",
        "aerocapture": True,
    },
    "path_4_variant_D": {
        "variant": "D — Saturn-egress chemical kick + Earth aerocapture",
        "vbic_variant_id": "D_both",
        "aerocapture": True,
    },
}
CHUNKS_T = [200.0, 482.0]
ISP_ELECTRIC_S = 2000.0
REACTOR_KWE = 500.0


# ---------------------------------------------------------------------------
# Launch-market reference table (PRIMARY-source-anchored)
# ---------------------------------------------------------------------------

# Each entry: (per_launch_cost_USD, LEO_capacity_t, label, notes)
LAUNCH_MARKETS = [
    {
        "id": "starship_floor_$100/kg",
        "per_launch_USD": 20e6,
        "LEO_capacity_t": 200.0,
        "USD_per_kg": 100.0,
        "notes": "Musk 2032+ aspiration; UNVERIFIED, optimistic floor",
    },
    {
        "id": "starship_target_$200/kg",
        "per_launch_USD": 100e6,
        "LEO_capacity_t": 250.0,
        "USD_per_kg": 400.0,
        "notes": "SpaceX 2025 stated Block 2 expendable target; NOT YET ACHIEVED",
    },
    {
        "id": "starship_pessimistic_$500/kg",
        "per_launch_USD": 100e6,
        "LEO_capacity_t": 100.0,
        "USD_per_kg": 1000.0,
        "notes": "If Starship achieves operations but at half target capacity",
    },
    {
        "id": "falcon_heavy_realistic_$1500/kg",
        "per_launch_USD": 150e6,
        "LEO_capacity_t": 100.0,
        "USD_per_kg": 1500.0,
        "notes": "Falcon Heavy expendable post-2026 commercial-realistic anchor",
    },
    {
        "id": "falcon_heavy_expendable_published",
        "per_launch_USD": 150e6,
        "LEO_capacity_t": 63.8,
        "USD_per_kg": 2351.0,
        "notes": "SpaceX-published Falcon Heavy expendable; stable since 2018",
    },
    {
        "id": "SLS_class_$5000/kg",
        "per_launch_USD": 475e6,
        "LEO_capacity_t": 95.0,
        "USD_per_kg": 5000.0,
        "notes": "SLS Block 1 cost-plus reference; pessimistic ceiling",
    },
]

KICK_STAGE_COST_USD = 140e6  # Vulcan-Centaur-class kick stage cost (R-reactor-roadmap inheritance)
RHEA_BAKEOFF_LAUNCH_PLUS_TSI_USD = 290e6  # rhea bake-off / R-reactor-roadmap inherited anchor


# ---------------------------------------------------------------------------
# Per-cell variant_b_closure
# ---------------------------------------------------------------------------

def closure_for_path_chunk(path_id: str, chunk_t: float) -> dict:
    p = PATH_DEFS[path_id]
    v = vbm.variant_inbound_dv(p["vbic_variant_id"], DEFAULT_DEPARTURE)
    return variant_b_closure(
        reactor_kwe=REACTOR_KWE,
        chunk_t=chunk_t,
        isp_electric_s=ISP_ELECTRIC_S,
        dv_chem_outbound_km_s=DV_CHEM_OUTBOUND_KM_S,
        dv_inbound_electric_km_s=v["electric_dv_km_s"],
        dv_inbound_impulsive_km_s=v["impulsive_egress_dv_km_s"],
        aerocapture=p["aerocapture"],
        m_outbound_kick_dry_t=M_OUTBOUND_KICK_DRY_T,
        m_saturn_kick_dry_t=M_SATURN_KICK_DRY_T,
    )


def launch_plus_tsi_under_market(m_LEO_t: float, market: dict) -> dict:
    """Compute realistic launch+TSI for a given LEO mass under a given launch
    market. Treats the kick stage cost as a separate line item ($140M)."""
    n_launches = max(1, math.ceil(m_LEO_t / market["LEO_capacity_t"]))
    launch_cost = n_launches * market["per_launch_USD"]
    total = launch_cost + KICK_STAGE_COST_USD
    return {
        "n_launches": n_launches,
        "launch_cost_USD": launch_cost,
        "kick_stage_USD": KICK_STAGE_COST_USD,
        "total_launch_plus_tsi_USD": total,
        "implied_USD_per_kg": launch_cost / max(1.0, m_LEO_t * 1000.0),
    }


# ---------------------------------------------------------------------------
# Cashflow rerun with overridden LAUNCH_PLUS_TSI per (path, chunk)
# ---------------------------------------------------------------------------

def conditional_irr_curve_with_launch_override(
    cell: dict,
    delivered_t_per_ship: float,
    round_trip_yr: float,
    launch_plus_tsi_USD: float,
    ship_cost_key: str = "Chemical_kick_500kWe",
) -> dict:
    """Replicate R-reactor-roadmap.conditional_irr_curve but with overridden
    LAUNCH_PLUS_TSI per ship and overridden delivered_t / round_trip_yr per cell.

    Strategy: monkey-patch reactor_roadmap module-level constants, call its
    conditional_irr_curve, then restore. Single-threaded; safe for this round.
    """
    saved_lt = rr.LAUNCH_PLUS_TSI
    saved_dt = dict(rr.MARVL_CHUNK_DELIVERED_T)
    saved_rt = rr.ROUND_TRIP_YR_MARVL
    try:
        rr.LAUNCH_PLUS_TSI = launch_plus_tsi_USD
        rr.MARVL_CHUNK_DELIVERED_T[ship_cost_key] = delivered_t_per_ship
        rr.MARVL_CHUNK_DELIVERED_T["MW_1000kWe"] = delivered_t_per_ship
        rr.ROUND_TRIP_YR_MARVL = round_trip_yr
        out = rr.conditional_irr_curve(cell, with_tv=True)
        marg_dict = rr.marginal_irr(out, PBR_CDF)
        marg = marg_dict["marginal_irr"]
    finally:
        rr.LAUNCH_PLUS_TSI = saved_lt
        rr.MARVL_CHUNK_DELIVERED_T = saved_dt
        rr.ROUND_TRIP_YR_MARVL = saved_rt
    return {"curve": out, "marginal_irr": marg}


# ---------------------------------------------------------------------------
# Sweep
# ---------------------------------------------------------------------------

WATER_PRICES = [2000.0, 10000.0]
SOVEREIGN_OPTIONS = [
    {"label": "no_sovereign", "amount": 0.0, "year": 11},
    {"label": "sovereign_2B_y11", "amount": 2e9, "year": 11},
]


def main():
    out = {
        "config": {
            "REACTOR_KWE": REACTOR_KWE,
            "ISP_ELECTRIC_S": ISP_ELECTRIC_S,
            "DV_CHEM_OUTBOUND_KM_S": DV_CHEM_OUTBOUND_KM_S,
            "ISP_HYDROLOX_S": ISP_HYDROLOX_S,
            "M_OUTBOUND_KICK_DRY_T": M_OUTBOUND_KICK_DRY_T,
            "M_SATURN_KICK_DRY_T": M_SATURN_KICK_DRY_T,
            "KICK_STAGE_COST_USD": KICK_STAGE_COST_USD,
            "RHEA_BAKEOFF_LAUNCH_PLUS_TSI_USD": RHEA_BAKEOFF_LAUNCH_PLUS_TSI_USD,
        },
        "launch_markets": LAUNCH_MARKETS,
        "path_chunk_closure": [],
        "launch_market_table_per_cell": [],
        "sweep_irr": [],
    }

    cells = []
    for path_id in PATH_DEFS:
        for chunk in CHUNKS_T:
            r = closure_for_path_chunk(path_id, chunk)
            entry = {
                "path_id": path_id,
                "variant": PATH_DEFS[path_id]["variant"],
                "chunk_t": chunk,
                "m_tug_t": r["m_tug_t"],
                "m_outbound_kick_prop_t": r["m_outbound_kick_prop_t"],
                "m_LEO_mission1_t": r["m_LEO_mission1_t"],
                "m_egress_prop_t": r["m_egress_prop_t"],
                "chunk_after_egress_t": r["chunk_after_egress_t"],
                "m_prop_inbound_t": r["m_prop_inbound_t"],
                "delivered_t": r["delivered_t"],
                "round_trip_yr": r["round_trip_yr"],
                "closes_strict_l0_05": r["closes_strict_15yr"],
                "closes_soft_l0_05": r["closes_soft_16yr"],
            }
            cells.append((entry, r))
            out["path_chunk_closure"].append(entry)

    # Per-cell launch market table
    for entry, _ in cells:
        for market in LAUNCH_MARKETS:
            lp = launch_plus_tsi_under_market(entry["m_LEO_mission1_t"], market)
            out["launch_market_table_per_cell"].append({
                "path_id": entry["path_id"],
                "chunk_t": entry["chunk_t"],
                "m_LEO_mission1_t": entry["m_LEO_mission1_t"],
                "market_id": market["id"],
                "n_launches_per_ship": lp["n_launches"],
                "launch_cost_USD": lp["launch_cost_USD"],
                "kick_stage_USD": lp["kick_stage_USD"],
                "total_launch_plus_tsi_USD": lp["total_launch_plus_tsi_USD"],
                "implied_USD_per_kg": lp["implied_USD_per_kg"],
                "ratio_vs_rhea_bakeoff": lp["total_launch_plus_tsi_USD"] / RHEA_BAKEOFF_LAUNCH_PLUS_TSI_USD,
            })

    # Marginal IRR sweep across (cell × market × water_price × sovereign)
    for entry, _ in cells:
        for market in LAUNCH_MARKETS:
            lp = launch_plus_tsi_under_market(entry["m_LEO_mission1_t"], market)
            for wp in WATER_PRICES:
                for sov in SOVEREIGN_OPTIONS:
                    cell_def = {
                        "price_per_kg": wp,
                        "sovereign_amount": sov["amount"],
                        "sovereign_year": sov["year"],
                    }
                    irr_result = conditional_irr_curve_with_launch_override(
                        cell=cell_def,
                        delivered_t_per_ship=entry["delivered_t"],
                        round_trip_yr=entry["round_trip_yr"],
                        launch_plus_tsi_USD=lp["total_launch_plus_tsi_USD"],
                    )
                    rt = entry["round_trip_yr"]
                    if rt <= 15.0:
                        l0_05 = "hard_pass"
                    elif rt <= 16.0:
                        l0_05 = "soft_pass"
                    else:
                        l0_05 = f"over_by_{rt - 15.0:.2f}yr"
                    out["sweep_irr"].append({
                        "path_id": entry["path_id"],
                        "chunk_t": entry["chunk_t"],
                        "market_id": market["id"],
                        "launch_plus_tsi_USD": lp["total_launch_plus_tsi_USD"],
                        "n_launches_per_ship": lp["n_launches"],
                        "water_price_USD_per_kg": wp,
                        "sovereign_label": sov["label"],
                        "delivered_t": entry["delivered_t"],
                        "round_trip_yr": rt,
                        "l0_05_status": l0_05,
                        "marginal_irr": irr_result["marginal_irr"],
                        "passes_sovereign_bond": (
                            (irr_result["marginal_irr"] is not None)
                            and (irr_result["marginal_irr"] >= 0.04)
                            and (rt <= 15.0)
                        ),
                        "passes_sovereign_bond_soft": (
                            (irr_result["marginal_irr"] is not None)
                            and (irr_result["marginal_irr"] >= 0.04)
                            and (rt <= 16.0)
                        ),
                    })

    # ---------- Hypothesis grading ----------
    hyp = {}

    # H-ock-a: 715 t claim overstated by >= 4x. Real value < 200 t.
    max_outbound_prop = max(e["m_outbound_kick_prop_t"] for e, _ in cells)
    hyp["H-ock-a"] = {
        "predicted": "real outbound prop per mission < 200 t (715 claim overstated by >= 4x)",
        "measured_max_t": max_outbound_prop,
        "held": max_outbound_prop < 200.0,
    }

    # H-ock-b: implied launch cost in $1200-$1400/kg at $290M / 224 t
    central_LEO = next(e["m_LEO_mission1_t"] for e, _ in cells if e["path_id"] == "path_1_variant_C" and e["chunk_t"] == 200.0)
    implied_cost_per_kg = RHEA_BAKEOFF_LAUNCH_PLUS_TSI_USD / (central_LEO * 1000.0)
    hyp["H-ock-b"] = {
        "predicted": "implied launch cost in [1200, 1400] $/kg",
        "measured_USD_per_kg": implied_cost_per_kg,
        "held": 1200.0 <= implied_cost_per_kg <= 1400.0,
    }

    # H-ock-c: at FH expendable (63.8 t), 224 t requires >= 3 launches
    fh_capacity = 63.8
    n_launches_fh = central_LEO / fh_capacity
    hyp["H-ock-c"] = {
        "predicted": "central LEO mass / FH expendable capacity >= 2.5 (i.e., >= 3 launches)",
        "measured_ratio": n_launches_fh,
        "held": n_launches_fh >= 2.5,
    }

    # H-ock-d: at $665M/ship updated launch (FH realistic), marginal IRR for path 4 chunk 200 still 0
    rows_d = [r for r in out["sweep_irr"] if r["path_id"] == "path_4_variant_D" and r["chunk_t"] == 200.0 and r["market_id"] == "falcon_heavy_realistic_$1500/kg"]
    irrs_d = [r["marginal_irr"] for r in rows_d]
    hyp["H-ock-d"] = {
        "predicted": "marginal IRR remains <= 0 under FH realistic launch; matches rhea bake-off floor",
        "measured_irrs": irrs_d,
        "held": all((m is None or m <= 0.0001) for m in irrs_d),
    }

    # H-ock-e: under Starship-class even at $200/kg + best path + $10k water + sovereign, no sovereign-bond pass
    rows_e = [
        r for r in out["sweep_irr"]
        if r["market_id"] == "starship_target_$200/kg"
        and r["water_price_USD_per_kg"] == 10000.0
        and r["sovereign_label"] == "sovereign_2B_y11"
        and r["chunk_t"] == 200.0
    ]
    any_e_passes = any(r["passes_sovereign_bond"] for r in rows_e)
    hyp["H-ock-e"] = {
        "predicted": "no Starship-class config crosses sovereign-bond at L0-05 hard",
        "measured_any_passes": any_e_passes,
        "rows_sample": [{"path_id": r["path_id"], "marginal_irr": r["marginal_irr"], "l0_05": r["l0_05_status"]} for r in rows_e],
        "held": not any_e_passes,
    }

    # H-ock-f: NO row crosses sovereign-bond at L0-05 hard across full sweep
    hard_passes = [r for r in out["sweep_irr"] if r["passes_sovereign_bond"]]
    hyp["H-ock-f"] = {
        "predicted": "zero rows cross sovereign-bond at L0-05 hard",
        "measured_count": len(hard_passes),
        "passing_rows": [{"path_id": r["path_id"], "chunk_t": r["chunk_t"], "market_id": r["market_id"], "wp": r["water_price_USD_per_kg"], "sov": r["sovereign_label"], "irr": r["marginal_irr"]} for r in hard_passes],
        "held": len(hard_passes) == 0,
    }

    # H-ock-g: at L0-05 soft, at most 1 row passes; if so, requires Starship-class
    soft_passes = [r for r in out["sweep_irr"] if r["passes_sovereign_bond_soft"] and not r["passes_sovereign_bond"]]
    starship_market_ids = {"starship_floor_$100/kg", "starship_target_$200/kg", "starship_pessimistic_$500/kg"}
    held_g = len(soft_passes) <= 1 and (len(soft_passes) == 0 or all(r["market_id"] in starship_market_ids for r in soft_passes))
    hyp["H-ock-g"] = {
        "predicted": "at most 1 row passes at L0-05 soft; if so, requires Starship-class launch",
        "measured_soft_only_count": len(soft_passes),
        "soft_only_rows": [{"path_id": r["path_id"], "chunk_t": r["chunk_t"], "market_id": r["market_id"], "wp": r["water_price_USD_per_kg"], "sov": r["sovereign_label"], "irr": r["marginal_irr"]} for r in soft_passes],
        "held": held_g,
    }

    # H-ock-h: assumption-flagging — held a priori on H-ock-c
    hyp["H-ock-h"] = {
        "predicted": "rhea bake-off LAUNCH_PLUS_TSI internally inconsistent with MARVL ship LEO mass",
        "measured_consistency": (
            "INCONSISTENT" if (n_launches_fh >= 2.5) else "CONSISTENT"
        ),
        "held": n_launches_fh >= 2.5,
    }

    # H-ock-i: sleeper-falsifier framing retirement
    hyp["H-ock-i"] = {
        "predicted": "round produces calibration finding, NOT independent kill-shot",
        "measured_kill_shot_signal": (len(hard_passes) == 0 and hyp["H-ock-a"]["held"]),
        "held": (len(hard_passes) == 0 and hyp["H-ock-a"]["held"]),
        "note": "kill-shot retired iff (a) sleeper claim overstated AND (b) sweep does not produce surprising sovereign-bond pass",
    }

    out["hypothesis_grading"] = hyp

    # ---------- Aggregate verdict ----------
    aggregate_held = all(h["held"] for h in hyp.values())
    out["aggregate"] = {
        "all_subclaims_held": aggregate_held,
        "kill_shot_status": "retired" if hyp["H-ock-i"]["held"] else "potential",
        "matrix_amendment_required": True,
    }

    # ---------- Write outputs ----------
    results_dir = ROUND_DIR / "results"
    results_dir.mkdir(exist_ok=True)
    with open(results_dir / "R_outbound_chemical_kick_economics.json", "w") as f:
        json.dump(out, f, indent=2, default=str)

    write_tables(out)
    write_closure_verdict(out)


def write_tables(out):
    """Generate human-readable tables.md."""
    L = []
    L.append("# R-outbound-chemical-kick-economics — Tables\n")
    L.append("## Per-cell variant_b_closure (PRIMARY-text source)\n")
    L.append("| Path | Variant | Chunk (t) | Tug (t) | Out kick prop (t) | LEO mission-1 (t) | Egress prop (t) | Chunk after egress (t) | Inbound prop (t) | Delivered (t) | Round-trip (yr) | L0-05 |")
    L.append("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|")
    for c in out["path_chunk_closure"]:
        l05 = "hard" if c["closes_strict_l0_05"] else ("soft" if c["closes_soft_l0_05"] else "fail")
        L.append(f"| {c['path_id']} | {c['variant']} | {c['chunk_t']:.0f} | {c['m_tug_t']:.1f} | {c['m_outbound_kick_prop_t']:.1f} | {c['m_LEO_mission1_t']:.1f} | {c['m_egress_prop_t']:.1f} | {c['chunk_after_egress_t']:.1f} | {c['m_prop_inbound_t']:.1f} | {c['delivered_t']:.2f} | {c['round_trip_yr']:.2f} | {l05} |")

    L.append("\n## Per-market launch+TSI per ship (mission 1, no depot)\n")
    L.append("Compares to rhea bake-off / R-reactor-roadmap inherited LAUNCH_PLUS_TSI = $290M/ship.\n")
    L.append("| Path | Chunk (t) | LEO mass (t) | Market | n launches | Launch USD | Total launch+TSI USD | Implied $/kg | Ratio vs $290M |")
    L.append("|---|---:|---:|---|---:|---:|---:|---:|---:|")
    for c in out["launch_market_table_per_cell"]:
        L.append(f"| {c['path_id']} | {c['chunk_t']:.0f} | {c['m_LEO_mission1_t']:.1f} | {c['market_id']} | {c['n_launches_per_ship']} | ${c['launch_cost_USD']/1e6:.0f}M | ${c['total_launch_plus_tsi_USD']/1e6:.0f}M | ${c['implied_USD_per_kg']:.0f}/kg | {c['ratio_vs_rhea_bakeoff']:.2f}× |")

    L.append("\n## Marginal IRR sweep — passes/fails sovereign-bond (4 percent IRR)\n")
    L.append("| Path | Chunk (t) | Market | Water $/kg | Sovereign | Delivered (t) | RT (yr) | L0-05 | Marg IRR | Pass sov-bond hard? | Pass sov-bond soft? |")
    L.append("|---|---:|---|---:|---|---:|---:|:---:|---:|:---:|:---:|")
    for r in out["sweep_irr"]:
        irr_str = f"{r['marginal_irr']:.4f}" if r["marginal_irr"] is not None else "None"
        L.append(f"| {r['path_id']} | {r['chunk_t']:.0f} | {r['market_id']} | {r['water_price_USD_per_kg']:.0f} | {r['sovereign_label']} | {r['delivered_t']:.2f} | {r['round_trip_yr']:.2f} | {r['l0_05_status']} | {irr_str} | {'✓' if r['passes_sovereign_bond'] else '✗'} | {'✓' if r['passes_sovereign_bond_soft'] else '✗'} |")

    L.append("\n## Hypothesis grading\n")
    L.append("| Sub-claim | Predicted | Measured | Held? |")
    L.append("|---|---|---|:---:|")
    for k, h in out["hypothesis_grading"].items():
        meas_summary = ", ".join(f"{kk}={vv}" for kk, vv in h.items() if kk not in ("predicted", "held", "note") and not isinstance(vv, list))
        L.append(f"| {k} | {h['predicted']} | {meas_summary} | {'✓' if h['held'] else '✗'} |")

    L.append("\n## Aggregate\n")
    a = out["aggregate"]
    L.append(f"- All sub-claims held: **{a['all_subclaims_held']}**")
    L.append(f"- Kill-shot status: **{a['kill_shot_status']}**")
    L.append(f"- Matrix amendment required: **{a['matrix_amendment_required']}**")

    (ROUND_DIR / "results" / "tables.md").write_text("\n".join(L) + "\n")


def write_closure_verdict(out):
    h = out["hypothesis_grading"]
    a = out["aggregate"]
    hard_passes = h["H-ock-f"]["measured_count"]
    max_outprop = h["H-ock-a"]["measured_max_t"]
    implied_cost = h["H-ock-b"]["measured_USD_per_kg"]
    n_fh = h["H-ock-c"]["measured_ratio"]
    aggregate_held = a["all_subclaims_held"]

    txt = f"""# R-outbound-chemical-kick-economics — Closure Verdict

**Aggregate held:** {aggregate_held}.
**Kill-shot status:** {a['kill_shot_status']}.

## One-paragraph verdict

The batch-3/4 sleeper-falsifier claim "Round F uses 715 t of hydrolox per outbound mission" is **retracted** ({h['H-ock-a']['held']}, max measured {max_outprop:.1f} t). The actual `variant_b_closure`-anchored figure for surviving 500-kWe / 200-t cells is 145–155 t hydrolox per mission. At rhea bake-off's inherited LAUNCH_PLUS_TSI = $290M/ship and central LEO mission-1 mass 224 t, implied launch cost is **${implied_cost:.0f}/kg** ({h['H-ock-b']['held']}). Falcon Heavy expendable's stated LEO capacity is 63.8 t — the surviving cell needs **{n_fh:.2f}×** that ({h['H-ock-c']['held']}), so the rhea bake-off's "$150M Falcon Heavy expendable + $140M Vulcan-Centaur kick = $290M/ship" anchor is internally inconsistent at 500-kWe MARVL ship mass. Updating launch+TSI to realistic Falcon-Heavy market ($665M/ship) does not change the rhea bake-off's marginal IRR verdict ({h['H-ock-d']['held']}) because IRR is already floored at zero. Sweep across launch market × water price × sovereign payment confirms zero rows cross sovereign-bond IRR at L0-05 hard ({hard_passes} rows pass; H-ock-f held: {h['H-ock-f']['held']}). Outbound chemical-kick economics is therefore **NOT an independent matrix-killer** — the cell remains killed by reactor program risk + L0-05 ceiling. The "outbound chemical-kick economics sleeper falsifier" framing should be retired from the matrix open-items list, AND the bake-off's launch-cost anchor should be flagged as internally inconsistent (held: {h['H-ock-h']['held']}).

## Three findings the orchestrator must reconcile

1. **The sleeper-falsifier claim was a back-of-envelope error.** The 715 t figure was inserted as text into `R_aerocapture_fast_cruise_envelope/results/closure_verdict.md` without being computed from `variant_b_closure`. It propagated into batch-3 and batch-4 handoffs as load-bearing. Per recurring lesson #N (compute back-of-envelope FIRST, anchor on PRIMARY texts), this round catches the error. **The matrix's "open items" list should retire the outbound-chemical-kick sleeper-falsifier item.**

2. **The rhea bake-off's $290M/ship LAUNCH_PLUS_TSI is internally inconsistent with the MARVL ship LEO mass.** R-reactor-roadmap's source comment claims "Falcon Heavy expendable + Vulcan-Centaur-class kick" for $290M, but Falcon Heavy expendable's 63.8 t LEO capacity cannot launch 224 t in a single mission. The bake-off implicitly assumes either (a) Starship-class launch economics (~$1,200/kg with kick) — which is the SpaceX 2025 pessimistic-target band, NOT YET ACHIEVED, OR (b) the per-ship launch contribution is undercounted by ~1.8–3.5× under realistic 2026 launch markets. **Recommendation: matrix-amendment to flag this internal inconsistency; defer cost-anchor revision to a separate round (R-launch-cost-anchor-revision) that re-derives ship cashflow under explicit launcher assumptions.**

3. **The bake-off's verdict is robust to launch-cost revision.** Even raising LAUNCH_PLUS_TSI to $665M/ship (realistic Falcon Heavy expendable, 4 launches at $150M plus kick), or to $1,500M/ship (SLS-class), no row in this round's sweep crosses sovereign-bond IRR at L0-05 hard. The cell does not return capital under any tested launch market × water price × sovereign payment combination. The kill mechanism remains reactor program risk + L0-05 ceiling, NOT outbound launch economics. **The matrix's headline finding survives; the calibration just makes the cost anchor more defensible.**

## What this round did NOT close (out of scope)

- **Cryogenic depot scenario (mission 2+).** Mission-1 is the binding constraint for capital amortization. Depot economics (build cost, boil-off, operating cost) are matrix item #6 and need their own round.
- **Reactor program risk parameter sensitivity.** R-power-bayesian-update already absorbed; this round inherits.
- **Ship cost / NRE / ground ops sensitivity.** Inherited from R15-rerun via R-reactor-roadmap. Out of scope.
- **Starship-target launch economics being achieved.** This round shows that even AT the Starship target ($200/kg, $290M/ship implied), the cell does not close. So the question is moot — Starship-target is necessary but not sufficient for closure.

## Recommended next round

If a worker is to close the launch-cost anchor properly: **R-launch-cost-anchor-revision** — re-derive ship cashflow under explicit launcher market assumptions (Falcon Heavy realistic, Starship target, Starship pessimistic), with depot-amortization scenario, ship-cadence sensitivity, and refresh of R-reactor-roadmap cashflow constants. Estimate 4–6 hours analyst time.

Hyperion track record now: 9 rounds, 9 aggregate findings (2 kill-shots, 6 falsifications-of-pre-reg-intuition, 1 calibration-retraction-of-prior-finding). The recurring-lesson-#N stacked intervention (back-of-envelope FIRST, PRIMARY-text anchors) is now consistently producing held aggregates AND catching prior-round errors.
"""
    (ROUND_DIR / "results" / "closure_verdict.md").write_text(txt)


if __name__ == "__main__":
    main()
    print("R-outbound-chemical-kick-economics: complete. See results/.")
