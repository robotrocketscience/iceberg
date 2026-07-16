"""R-bag-capture-efficiency-revisit — propagate η_c < 1.0 through the matrix.

For each cell in the architecture decision matrix's surviving-winner set and the
sub-megawatt sweet spot, compute delivered customer mass, inbound burn time, and
round-trip closure status across the realistic η_c range, separating two physical
loss mechanisms:

  η_pre  — mass loss before burn (bag escape + un-re-sublimable frost)
  η_thr  — Isp degradation during burn (thruster utilization)

η_c (composite) = η_pre × η_thr.

Three decomposition modes per composite η_c:
  pure-pre  : η_pre = η_c, η_thr = 1
  pure-thr  : η_pre = 1, η_thr = η_c
  mid       : η_pre = η_thr = sqrt(η_c)
"""

from __future__ import annotations

import json
import math
from pathlib import Path

# Physical constants (inline; this round is self-contained).
G0 = 9.80665                                    # m/s^2
YEAR_S = 365.25 * 86400.0                       # s/yr
GM_SUN = 1.32712440018e11                       # km^3/s^2
GM_EARTH = 3.986004418e5                        # km^3/s^2
AU_KM = 1.495978707e8                           # km
A_SATURN_AU = 9.5826
R_LEO_KM = 6378.137 + 400.0                     # km, low-Earth-orbit reference

ETA_THRUSTER = 0.65                             # RF ion / dual-ion power-to-jet efficiency
ROUND_TRIP_CEILING_YR = 15.0                    # L0-05
SATURN_OPS_YR = 1.0

# Bag-engineering doc realistic ranges (read out of ICEBERG-bag-engineering.md §6)
ETA_BAG_RANGE = (0.95, 0.99)                    # cold-wall capture
ETA_FEED_RANGE = (0.95, 0.99)                   # frost re-sublimation
# Thruster efficiency depends on cell:
ETA_MET_RANGE = (0.75, 0.92)                    # microwave electrothermal (bag-eng doc)
ETA_RF_ION_RANGE = (0.65, 0.75)                 # radio-frequency ion (NASA Evolutionary Xenon Thruster scaled to water)

# Composite η_c sweep
ETA_C_SWEEP = [0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.00]


def dry_mass_decomposed_mid_t(reactor_kwe: float, m_prop_t: float = 0.0) -> float:
    """Decomposed-mid tug dry mass (tonnes). Copied from R-radiator-mass-penalty
    convention for cross-round consistency.

    Components: fixed bus + reactor + power-conditioning + radiator + tank-fraction.
    """
    m_fixed = 3.0                                       # t — bus, avionics, structure
    alpha_reactor = 50.0                                # W/kg
    alpha_pc = 200.0                                    # W/kg
    alpha_rad_kw_th_per_kg = 2.0                        # kW_thermal/kg radiator
    eta_conv = 0.30                                     # electric/thermal
    f_tank = 0.05                                       # tank as fraction of propellant

    m_reactor = reactor_kwe / alpha_reactor             # tonnes (kWe / (W/kg) = kg → t since kWe/W/kg = 1000kg, /1000 = t)
    m_pc = reactor_kwe / alpha_pc
    p_th_waste_kw = reactor_kwe * (1.0 - eta_conv) / eta_conv
    m_rad = p_th_waste_kw / alpha_rad_kw_th_per_kg / 1000.0  # kg → t
    m_tank = m_prop_t * f_tank
    return m_fixed + m_reactor + m_pc + m_rad + m_tank


def hohmann_transfer_time_yr(a_au: float = A_SATURN_AU) -> float:
    """Hohmann transfer Earth to target body, one-way, years."""
    a_h_km = (1.0 + a_au) / 2.0 * AU_KM
    t_s = math.pi * math.sqrt(a_h_km**3 / GM_SUN)
    return t_s / YEAR_S


def cell_inbound(
    m_chunk_intended_t: float,
    m_tug_t: float,
    dv_inbound_km_s: float,
    isp_nominal_s: float,
    eta_pre: float,
    eta_thr: float,
    p_electric_kwe: float,
) -> dict:
    """Compute inbound-burn outcomes given decomposed η_c.

    Returns delivered customer mass, propellant burned, burn time, and a closes flag.
    """
    v_e_nominal_m_s = isp_nominal_s * G0
    v_e_eff_m_s = eta_thr * v_e_nominal_m_s
    if v_e_eff_m_s <= 0:
        return {"delivered_t": float("-inf"), "burn_yr": float("inf"), "valid": False}

    m_chunk_captured_t = eta_pre * m_chunk_intended_t
    m_initial_t = m_tug_t + m_chunk_captured_t
    mass_ratio = math.exp(dv_inbound_km_s * 1000.0 / v_e_eff_m_s)
    m_final_t = m_initial_t / mass_ratio
    delivered_t = m_final_t - m_tug_t
    m_prop_burned_t = m_initial_t - m_final_t

    # Constant-thrust burn time: F = 2·η·P/v_e (jet eq); t = m_prop / mdot; mdot = F / v_e_eff
    p_electric_w = p_electric_kwe * 1000.0
    thrust_n = 2.0 * ETA_THRUSTER * p_electric_w / v_e_eff_m_s
    mdot_kg_s = thrust_n / v_e_eff_m_s
    if mdot_kg_s <= 0:
        return {"delivered_t": delivered_t, "burn_yr": float("inf"), "valid": False}
    t_burn_s = (m_prop_burned_t * 1000.0) / mdot_kg_s
    t_burn_yr = t_burn_s / YEAR_S

    return {
        "delivered_t": delivered_t,
        "m_chunk_captured_t": m_chunk_captured_t,
        "m_initial_t": m_initial_t,
        "m_final_t": m_final_t,
        "m_prop_burned_t": m_prop_burned_t,
        "mass_ratio": mass_ratio,
        "v_e_eff_m_s": v_e_eff_m_s,
        "burn_yr": t_burn_yr,
        "valid": True,
    }


def cell_round_trip_yr(
    inbound_burn_yr: float,
    outbound_burn_yr: float,
    cruise_yr: float,
    saturn_ops_yr: float = SATURN_OPS_YR,
) -> float:
    return outbound_burn_yr + cruise_yr + saturn_ops_yr + inbound_burn_yr + cruise_yr


# Outbound burn times per cell — held constant from R-electric-outbound (these are
# η_c-independent because the vehicle is empty going out). Values quoted from
# R-electric-outbound decomposed-mid.
OUTBOUND_BURN_YR = {
    10: 99.0,        # Kilopower all-electric outbound — exceeds L0-05 (Variant B uses chemical kick instead)
    100: 5.20,       # Stretch sweet spot
    200: 2.60,
    1000: 0.52,
}


# Cell definitions — matrix winners + sub-megawatt sweet spot.
# For Variant B, only the *electric inbound leg* is η_c-sensitive (chemical kick
# uses fully-consumed propellant; jettisoned post-burn). Outbound is chemical kick
# (model is dominated by chemical-stack performance not electric tug); we use the
# R-outbound-architecture chemical-kick outbound conops (assume ~0 yr burn for kick stage;
# Hohmann cruise applies post-kick) — round-trip for Variant B is therefore
# cruise + Saturn ops + cruise + electric inbound burn.

def variant_b_round_trip_yr(inbound_burn_yr: float) -> float:
    """Variant B (chunk-fed chemical departure, electric inbound at residual Δv)."""
    return hohmann_transfer_time_yr() + SATURN_OPS_YR + hohmann_transfer_time_yr() + inbound_burn_yr


CELLS = [
    {
        "name": "Kilopower Variant B (10 kWe, 100 t chunk, chemical kick + electric inbound)",
        "key": "variant_b_10_100",
        "p_electric_kwe": 10.0,
        "m_chunk_intended_t": 100.0,
        "dv_inbound_km_s": 3.0,        # post-chemical-offload electric residual (matrix Variant B definition)
        "isp_nominal_s": 2000.0,
        "thruster": "RF ion",
        "outbound_type": "chemical_kick",
    },
    {
        "name": "Stretch 100 kWe sweet spot (100 kWe, 200 t chunk, all-electric)",
        "key": "stretch_100_200",
        "p_electric_kwe": 100.0,
        "m_chunk_intended_t": 200.0,
        "dv_inbound_km_s": 6.42,
        "isp_nominal_s": 2000.0,
        "thruster": "RF ion",
        "outbound_type": "all_electric",
    },
    {
        "name": "Sub-megawatt (200 kWe, 500 t chunk, all-electric, Isp 2934)",
        "key": "submeg_200_500",
        "p_electric_kwe": 200.0,
        "m_chunk_intended_t": 500.0,
        "dv_inbound_km_s": 6.42,
        "isp_nominal_s": 2934.0,
        "thruster": "RF ion",
        "outbound_type": "all_electric",
    },
    {
        "name": "Megawatt all-electric (1000 kWe, 500 t chunk, Isp 5000)",
        "key": "megawatt_1000_500",
        "p_electric_kwe": 1000.0,
        "m_chunk_intended_t": 500.0,
        "dv_inbound_km_s": 6.42,
        "isp_nominal_s": 5000.0,
        "thruster": "dual-ion (RF ion + MET hybrid)",
        "outbound_type": "all_electric",
    },
]


def composite_eta_per_era() -> list[dict]:
    """Re-derive the bag-engineering document's η_c per era using realistic per-era
    thruster efficiencies — extends the doc's MET-only table to RF-ion and dual-ion.
    """
    eras = [
        ("Kilopower MET (bag-eng doc baseline)", 0.97, 0.95, ETA_MET_RANGE),
        ("Kilopower Variant B inbound (RF ion)", 0.97, 0.95, ETA_RF_ION_RANGE),
        ("Stretch / Sub-megawatt (RF ion)", 0.97, 0.95, ETA_RF_ION_RANGE),
        ("Megawatt (dual-ion, RF ion + MET hybrid)", 0.97, 0.95, ETA_RF_ION_RANGE),  # use RF-ion bound; dual-ion is conservative
    ]
    out = []
    for name, eta_bag, eta_feed, (thr_lo, thr_hi) in eras:
        eta_pre = eta_bag * eta_feed
        comp_lo = eta_pre * thr_lo
        comp_hi = eta_pre * thr_hi
        comp_mid = eta_pre * (thr_lo + thr_hi) / 2.0
        out.append({
            "era": name,
            "eta_bag": eta_bag,
            "eta_feed": eta_feed,
            "eta_pre": eta_pre,
            "eta_thr_lo": thr_lo,
            "eta_thr_hi": thr_hi,
            "composite_eta_c_lo": comp_lo,
            "composite_eta_c_mid": comp_mid,
            "composite_eta_c_hi": comp_hi,
        })
    return out


def main():
    results_dir = Path(__file__).parent / "results"
    results_dir.mkdir(exist_ok=True)

    cruise_yr = hohmann_transfer_time_yr()

    cell_results: list[dict] = []
    for cell in CELLS:
        # Tug mass uses approximate propellant placeholder (iterate later if needed).
        # First pass: estimate m_prop at η_c=1.0 to get tug, then hold tug fixed.
        v_e_nominal = cell["isp_nominal_s"] * G0
        mr_nominal = math.exp(cell["dv_inbound_km_s"] * 1000.0 / v_e_nominal)
        m_chunk = cell["m_chunk_intended_t"]
        m_prop_est = (m_chunk) * (1.0 - 1.0 / mr_nominal)  # rough — ignores tug mass
        m_tug_t = dry_mass_decomposed_mid_t(cell["p_electric_kwe"], m_prop_est)

        sweep_rows = []
        for eta_c in ETA_C_SWEEP:
            for mode, (eta_pre, eta_thr) in {
                "mid": (math.sqrt(eta_c), math.sqrt(eta_c)),
                "pure_pre": (eta_c, 1.0),
                "pure_thr": (1.0, eta_c),
            }.items():
                rec = cell_inbound(
                    m_chunk_intended_t=m_chunk,
                    m_tug_t=m_tug_t,
                    dv_inbound_km_s=cell["dv_inbound_km_s"],
                    isp_nominal_s=cell["isp_nominal_s"],
                    eta_pre=eta_pre,
                    eta_thr=eta_thr,
                    p_electric_kwe=cell["p_electric_kwe"],
                )
                if cell["outbound_type"] == "chemical_kick":
                    rt = variant_b_round_trip_yr(rec["burn_yr"])
                else:
                    rt = cell_round_trip_yr(
                        inbound_burn_yr=rec["burn_yr"],
                        outbound_burn_yr=OUTBOUND_BURN_YR[int(cell["p_electric_kwe"])],
                        cruise_yr=cruise_yr,
                    )
                closes = (rt <= ROUND_TRIP_CEILING_YR) and (rec["delivered_t"] > 0)
                sweep_rows.append({
                    "eta_c": eta_c,
                    "mode": mode,
                    "eta_pre": eta_pre,
                    "eta_thr": eta_thr,
                    "delivered_t": rec["delivered_t"],
                    "burn_yr": rec["burn_yr"],
                    "round_trip_yr": rt,
                    "closes": closes,
                    "v_e_eff_m_s": rec["v_e_eff_m_s"],
                    "mass_ratio": rec["mass_ratio"],
                })

        # Critical η_c floor (mid mode) — where delivered_t = 0.
        floor = None
        for r in sorted([s for s in sweep_rows if s["mode"] == "mid"], key=lambda x: x["eta_c"]):
            if r["delivered_t"] > 0:
                floor = r["eta_c"]
                break

        # Mass-loss-mode divergence: (pure_pre delivered) - (pure_thr delivered) at η_c=0.65
        rec65 = {s["mode"]: s for s in sweep_rows if abs(s["eta_c"] - 0.65) < 1e-9}
        if rec65:
            divergence = rec65["pure_pre"]["delivered_t"] - rec65["pure_thr"]["delivered_t"]
            rel = abs(divergence) / max(abs(rec65["pure_pre"]["delivered_t"]),
                                        abs(rec65["pure_thr"]["delivered_t"]), 1e-9)
        else:
            divergence = None
            rel = None

        cell_results.append({
            "cell": cell["name"],
            "key": cell["key"],
            "m_tug_t": m_tug_t,
            "sweep": sweep_rows,
            "critical_floor_eta_c_mid": floor,
            "divergence_at_eta_c_065": {
                "pure_pre_delivered_t": rec65["pure_pre"]["delivered_t"] if rec65 else None,
                "pure_thr_delivered_t": rec65["pure_thr"]["delivered_t"] if rec65 else None,
                "absolute_diff_t": divergence,
                "relative_diff": rel,
            },
        })

    composite = composite_eta_per_era()

    # Depot-fill mission ramp impact for Stretch 100 kWe / 200 t cell.
    # Matrix table says 1 mission at η_c=1.0 (depot fills itself).
    # New ramp = ceil(depot_fill_target / delivered_at_eta_c).
    # From R-outbound-architecture, depot fill target ≈ 273 t (chemical-kick m_LEO for the next mission).
    DEPOT_FILL_TARGET_T = 273.0
    stretch = next(r for r in cell_results if r["key"] == "stretch_100_200")
    ramp_table = []
    for eta_c in ETA_C_SWEEP:
        mid_row = next(s for s in stretch["sweep"] if abs(s["eta_c"] - eta_c) < 1e-9 and s["mode"] == "mid")
        if mid_row["delivered_t"] <= 0:
            ramp = None
        else:
            ramp = math.ceil(DEPOT_FILL_TARGET_T / mid_row["delivered_t"])
        ramp_table.append({
            "eta_c": eta_c,
            "delivered_t": mid_row["delivered_t"],
            "missions_to_fill_depot": ramp,
        })

    # Hypothesis grading
    grading = grade_hypotheses(cell_results, composite, ramp_table)

    out = {
        "cells": cell_results,
        "composite_eta_per_era": composite,
        "depot_ramp_stretch_100_200": ramp_table,
        "hohmann_cruise_yr_each_way": cruise_yr,
        "hypothesis_grading": grading,
    }
    (results_dir / "bag_capture_efficiency.json").write_text(json.dumps(out, indent=2))
    write_tables_md(out, results_dir)
    return out


def grade_hypotheses(cells, composite, ramp):
    g = {}

    # H-bcer-a — composite η_c at megawatt era, mid thruster efficiency
    meg = next(c for c in composite if c["era"].startswith("Megawatt"))
    g["H_bcer_a"] = {
        "predicted_band": [0.60, 0.70],
        "actual_mid": meg["composite_eta_c_mid"],
        "held": 0.60 <= meg["composite_eta_c_mid"] <= 0.70,
    }

    # H-bcer-b — megawatt delivered at composite η_c=0.65 (mid mode)
    meg_cell = next(c for c in cells if c["key"] == "megawatt_1000_500")
    base = next(s for s in meg_cell["sweep"] if abs(s["eta_c"] - 1.0) < 1e-9 and s["mode"] == "mid")
    at65 = next(s for s in meg_cell["sweep"] if abs(s["eta_c"] - 0.65) < 1e-9 and s["mode"] == "mid")
    pct_reduction = (base["delivered_t"] - at65["delivered_t"]) / base["delivered_t"] * 100.0
    g["H_bcer_b"] = {
        "predicted_band_pct": [35.0, 55.0],
        "actual_pct_reduction": pct_reduction,
        "held": 35.0 <= pct_reduction <= 55.0,
    }

    # H-bcer-c — megawatt round-trip change at η_c=0.65
    delta_rt = at65["round_trip_yr"] - base["round_trip_yr"]
    g["H_bcer_c"] = {
        "predicted_band_yr": [-1.0, 1.0],
        "actual_delta_yr": delta_rt,
        "held": -1.0 <= delta_rt <= 1.0,
    }

    # H-bcer-d — Kilopower Variant B critical floor
    vb = next(c for c in cells if c["key"] == "variant_b_10_100")
    g["H_bcer_d"] = {
        "predicted_band": [0.20, 0.40],
        "actual_floor": vb["critical_floor_eta_c_mid"],
        "held": (
            vb["critical_floor_eta_c_mid"] is not None
            and 0.20 <= vb["critical_floor_eta_c_mid"] <= 0.40
        ),
    }

    # H-bcer-e — stretch depot ramp at η_c=0.78 (Kilopower-era mid)
    # closest sweep point is 0.80; use that
    r80 = next(r for r in ramp if abs(r["eta_c"] - 0.80) < 1e-9)
    g["H_bcer_e"] = {
        "predicted_band_missions": [2, 4],
        "actual_at_eta_c_080": r80["missions_to_fill_depot"],
        "held": r80["missions_to_fill_depot"] is not None and 2 <= r80["missions_to_fill_depot"] <= 4,
    }

    # H-bcer-f — at least one matrix cell flips L0-05 status
    # Check megawatt and stretch (the all-electric winners) at composite η_c = mid for their era.
    stretch_cell = next(c for c in cells if c["key"] == "stretch_100_200")
    stretch_realistic_eta = next(c for c in composite if "Stretch" in c["era"])["composite_eta_c_mid"]
    # closest sweep point
    nearest = min(ETA_C_SWEEP, key=lambda e: abs(e - stretch_realistic_eta))
    stretch_r = next(s for s in stretch_cell["sweep"]
                     if abs(s["eta_c"] - nearest) < 1e-9 and s["mode"] == "mid")
    meg_realistic = meg["composite_eta_c_mid"]
    nearest_m = min(ETA_C_SWEEP, key=lambda e: abs(e - meg_realistic))
    meg_r = next(s for s in meg_cell["sweep"]
                 if abs(s["eta_c"] - nearest_m) < 1e-9 and s["mode"] == "mid")
    flipped = (not stretch_r["closes"]) or (not meg_r["closes"])
    g["H_bcer_f"] = {
        "predicted": "true (at least one cell flips)",
        "stretch_closes_at_realistic_eta_c": stretch_r["closes"],
        "megawatt_closes_at_realistic_eta_c": meg_r["closes"],
        "stretch_realistic_eta_c": stretch_realistic_eta,
        "megawatt_realistic_eta_c": meg_realistic,
        "actual": "flipped" if flipped else "no_flip",
        "held": flipped,
    }

    # H-bcer-g — pure_pre vs pure_thr divergence at η_c=0.65 for cells where m_tug > 10% of chunk
    divergences = []
    for c in cells:
        div = c["divergence_at_eta_c_065"]["relative_diff"]
        if div is not None:
            divergences.append({"cell": c["key"], "m_tug_t": c["m_tug_t"],
                                "rel_div": div, "m_tug_pct_of_chunk": c["m_tug_t"] /
                                next(cell["m_chunk_intended_t"] for cell in CELLS if cell["key"] == c["key"]) * 100.0})
    any_divergent = any(d["rel_div"] > 0.05 for d in divergences if d["m_tug_pct_of_chunk"] > 10.0)
    g["H_bcer_g"] = {
        "predicted": "divergence > 5% where m_tug > 10% of chunk",
        "divergences": divergences,
        "held": any_divergent,
    }

    return g


def write_tables_md(results, results_dir: Path):
    lines = []
    lines.append("# R-bag-capture-efficiency-revisit — tables\n")
    lines.append(f"Hohmann cruise each way: **{results['hohmann_cruise_yr_each_way']:.2f} yr**.\n")

    lines.append("\n## Composite η_c per era (extends bag-engineering doc §6)\n")
    lines.append("| Era | η_bag | η_feed | η_pre | η_thr range | Composite η_c (lo / mid / hi) |")
    lines.append("|---|---:|---:|---:|---|---|")
    for e in results["composite_eta_per_era"]:
        lines.append(
            f"| {e['era']} | {e['eta_bag']:.2f} | {e['eta_feed']:.2f} | {e['eta_pre']:.3f} | "
            f"{e['eta_thr_lo']:.2f}–{e['eta_thr_hi']:.2f} | "
            f"{e['composite_eta_c_lo']:.3f} / {e['composite_eta_c_mid']:.3f} / {e['composite_eta_c_hi']:.3f} |"
        )

    lines.append("\n## Per-cell η_c sweep (mid mode: η_pre = η_thr = √η_c)\n")
    for c in results["cells"]:
        lines.append(f"\n### {c['cell']}\n")
        lines.append(f"Tug dry mass (decomposed-mid): **{c['m_tug_t']:.2f} t**\n")
        lines.append(f"Critical η_c floor (mid mode, delivered = 0): "
                     f"**{c['critical_floor_eta_c_mid']}**\n")
        lines.append("| η_c | Mode | η_pre | η_thr | Delivered (t) | Burn (yr) | Round-trip (yr) | Closes 15 yr? |")
        lines.append("|---:|---|---:|---:|---:|---:|---:|:--:|")
        for s in c["sweep"]:
            flag = "**yes**" if s["closes"] else "no"
            lines.append(
                f"| {s['eta_c']:.2f} | {s['mode']} | {s['eta_pre']:.3f} | {s['eta_thr']:.3f} | "
                f"{s['delivered_t']:.1f} | {s['burn_yr']:.2f} | {s['round_trip_yr']:.2f} | {flag} |"
            )
        dv = c["divergence_at_eta_c_065"]
        lines.append(f"\nDivergence at η_c=0.65 (pure_pre vs pure_thr): "
                     f"pure_pre delivers **{dv['pure_pre_delivered_t']:.1f} t**, "
                     f"pure_thr delivers **{dv['pure_thr_delivered_t']:.1f} t**, "
                     f"relative diff **{dv['relative_diff']*100.0:.1f}%**.\n")

    lines.append("\n## Depot-fill mission ramp (Stretch 100 kWe / 200 t sweet spot)\n")
    lines.append("Target: 273 t at low Earth orbit (R-outbound-architecture chemical-kick re-fill).\n")
    lines.append("| η_c (mid) | Delivered (t) | Missions to fill |")
    lines.append("|---:|---:|---:|")
    for r in results["depot_ramp_stretch_100_200"]:
        ramp = r["missions_to_fill_depot"] if r["missions_to_fill_depot"] is not None else "negative-delivery"
        lines.append(f"| {r['eta_c']:.2f} | {r['delivered_t']:.1f} | {ramp} |")

    lines.append("\n## Hypothesis grading\n")
    g = results["hypothesis_grading"]
    lines.append("| Sub-claim | Predicted | Actual | Held? |")
    lines.append("|---|---|---|---|")
    lines.append(f"| H-bcer-a — megawatt-era composite η_c mid | "
                 f"{g['H_bcer_a']['predicted_band']} | "
                 f"{g['H_bcer_a']['actual_mid']:.3f} | "
                 f"{'yes' if g['H_bcer_a']['held'] else '**no**'} |")
    lines.append(f"| H-bcer-b — megawatt delivered reduction at composite η_c=0.65 | "
                 f"{g['H_bcer_b']['predicted_band_pct']}% | "
                 f"{g['H_bcer_b']['actual_pct_reduction']:.1f}% | "
                 f"{'yes' if g['H_bcer_b']['held'] else '**no**'} |")
    lines.append(f"| H-bcer-c — megawatt round-trip Δ at η_c=0.65 | "
                 f"{g['H_bcer_c']['predicted_band_yr']} yr | "
                 f"{g['H_bcer_c']['actual_delta_yr']:.2f} yr | "
                 f"{'yes' if g['H_bcer_c']['held'] else '**no**'} |")
    lines.append(f"| H-bcer-d — Variant B critical floor | "
                 f"{g['H_bcer_d']['predicted_band']} | "
                 f"{g['H_bcer_d']['actual_floor']} | "
                 f"{'yes' if g['H_bcer_d']['held'] else '**no**'} |")
    lines.append(f"| H-bcer-e — Stretch depot ramp at η_c=0.80 | "
                 f"{g['H_bcer_e']['predicted_band_missions']} missions | "
                 f"{g['H_bcer_e']['actual_at_eta_c_080']} missions | "
                 f"{'yes' if g['H_bcer_e']['held'] else '**no**'} |")
    lines.append(f"| H-bcer-f — at least one matrix winner flips L0-05 | "
                 f"{g['H_bcer_f']['predicted']} | "
                 f"{g['H_bcer_f']['actual']} (stretch closes={g['H_bcer_f']['stretch_closes_at_realistic_eta_c']}, "
                 f"megawatt closes={g['H_bcer_f']['megawatt_closes_at_realistic_eta_c']}) | "
                 f"{'yes' if g['H_bcer_f']['held'] else '**no**'} |")
    lines.append(f"| H-bcer-g — pure_pre vs pure_thr divergence > 5% (m_tug > 10% chunk) | "
                 f"{g['H_bcer_g']['predicted']} | "
                 f"max relative divergence "
                 f"{max(d['rel_div'] for d in g['H_bcer_g']['divergences'])*100.0:.1f}% | "
                 f"{'yes' if g['H_bcer_g']['held'] else '**no**'} |")

    (results_dir / "tables.md").write_text("\n".join(lines))


if __name__ == "__main__":
    out = main()
    print("R-bag-capture-efficiency-revisit complete.")
    print()
    print("Composite η_c per era (re-derived with realistic per-era thruster eff):")
    for e in out["composite_eta_per_era"]:
        print(f"  {e['era']:50s}  mid η_c = {e['composite_eta_c_mid']:.3f} "
              f"(range {e['composite_eta_c_lo']:.3f}–{e['composite_eta_c_hi']:.3f})")
    print()
    print("Critical η_c floors (mid mode, delivered_t = 0):")
    for c in out["cells"]:
        print(f"  {c['key']:25s}  floor = {c['critical_floor_eta_c_mid']}")
    print()
    print("L0-05 closure at realistic-era η_c (mid mode):")
    g = out["hypothesis_grading"]["H_bcer_f"]
    print(f"  stretch:  realistic η_c={g['stretch_realistic_eta_c']:.3f}, closes={g['stretch_closes_at_realistic_eta_c']}")
    print(f"  megawatt: realistic η_c={g['megawatt_realistic_eta_c']:.3f}, closes={g['megawatt_closes_at_realistic_eta_c']}")
    print()
    print("Hypothesis grading:")
    for k, v in out["hypothesis_grading"].items():
        print(f"  {k}: {'held' if v['held'] else 'FALSIFIED'}")
