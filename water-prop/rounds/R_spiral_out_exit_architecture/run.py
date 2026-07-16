"""R-spiral-out-exit-architecture — spiral-out reframe of composite exit burn.

Reframes Block 4's "impulsive 7.4 km/s exit during 6-month residence dwell" as
"continuous-thrust spiral-out from residence orbit at ~18 km/s Edelbaum-style,
extending into heliocentric cruise leg".

For each (P_reactor, Isp_spiral, Isp_inbound, dv_spiral) cell, computes:
  - mass after spiral, mass at Earth, delivered fraction
  - spiral burn time, inbound burn time, total propulsion time
  - L0-05 strict (total mission <= 15 yr -> burn budget 8.5 yr)
  - L0-05 waiver (total mission <= 25 yr -> burn budget 18.5 yr)
  - mass-closure flag (delivered > 0)
  - L0-04 floor (delivered >= 5 t)

Outputs: closure_grid.csv, closing_cells.csv, summary.json, spiral_vs_block11_compare.csv.
"""

from __future__ import annotations

import csv
import json
from math import exp
from pathlib import Path

G0 = 9.80665
SEC_PER_YEAR = 365.25 * 86400.0

OUT = Path(__file__).parent / "results"
OUT.mkdir(parents=True, exist_ok=True)

# Composite parameters (matched to Block 11 for direct comparability)
M_COLLECTED_T = 200.0
M_DRY_BASE_T = 200.0
M_JETTISON_T = 20.0
M_SHIELD_T = 4.13
M_DRY_TOTAL_T = M_DRY_BASE_T - M_JETTISON_T + M_SHIELD_T   # 184.13 t (returned dry)
M_AT_START_T = M_COLLECTED_T + M_DRY_TOTAL_T               # 384.13 t

DV_INBOUND_NET_KMS = 23.2
ETA = 0.65

# Mission-duration budgets (constant outbound+capture overhead = 6.5 yr).
# L0-05 strict 15 yr total -> propulsion budget 8.5 yr.
# L0-05 waiver 25 yr total -> propulsion budget 18.5 yr.
OUTBOUND_OVERHEAD_YR = 6.5
T_STRICT_BUDGET_YR = 15.0 - OUTBOUND_OVERHEAD_YR    # 8.5
T_WAIVER_BUDGET_YR = 25.0 - OUTBOUND_OVERHEAD_YR    # 18.5

# Operational minimum delivered mass for L0-04 floor (tonnes).
L0_04_FLOOR_T = 5.0

# Sweep grids
POWER_GRID_MWE = [0.5, 1.0, 2.0, 5.0]
ISP_GRID = [3000, 5000, 7000, 9000]
DV_SPIRAL_GRID_KMS = [14.0, 18.0, 19.5]    # low / baseline / high (sensitivity)

# Block 11 reference (impulsive 7.4 km/s exit, 6-month dwell constraint)
# Included as a single-cell counterfactual to show what changes.
DV_IMPULSIVE_EXIT_REF_KMS = 7.4


def burn_segment(power_w: float, isp_s: float, dv_kms: float,
                 m_start_t: float, eta: float = ETA) -> dict:
    """Tsiolkovsky + power-limited burn-time bookkeeping."""
    v_e = isp_s * G0
    thrust = 2.0 * eta * power_w / v_e
    mr = exp(dv_kms * 1000.0 / v_e)
    m_prop_t = m_start_t * (1.0 - 1.0 / mr)
    m_end_t = m_start_t / mr
    mdot = thrust / v_e                                # kg/s
    if mdot <= 0.0:
        return {"mr": mr, "m_prop_t": m_prop_t, "m_end_t": m_end_t,
                "t_s": float("inf"), "thrust_N": thrust, "v_e": v_e}
    t_s = (m_prop_t * 1000.0) / mdot
    return {"mr": mr, "m_prop_t": m_prop_t, "m_end_t": m_end_t,
            "t_s": t_s, "thrust_N": thrust, "v_e": v_e}


def evaluate_cell(p_mwe: float, isp_spiral: float, isp_inbound: float,
                  dv_spiral: float) -> dict:
    p_w = p_mwe * 1e6

    spiral = burn_segment(p_w, isp_spiral, dv_spiral, M_AT_START_T)
    inbound = burn_segment(p_w, isp_inbound, DV_INBOUND_NET_KMS, spiral["m_end_t"])

    m_at_earth = inbound["m_end_t"]
    m_delivered = max(0.0, m_at_earth - M_DRY_TOTAL_T)
    delivered_pct = (m_delivered / M_COLLECTED_T) * 100.0

    t_spiral_yr = spiral["t_s"] / SEC_PER_YEAR
    t_inbound_yr = inbound["t_s"] / SEC_PER_YEAR
    t_total_burn_yr = t_spiral_yr + t_inbound_yr
    t_total_mission_yr = OUTBOUND_OVERHEAD_YR + t_total_burn_yr

    mass_closes = m_delivered > 0
    l0_04_pass = m_delivered >= L0_04_FLOOR_T
    strict_pass = mass_closes and l0_04_pass and t_total_burn_yr <= T_STRICT_BUDGET_YR
    waiver_pass = mass_closes and l0_04_pass and t_total_burn_yr <= T_WAIVER_BUDGET_YR

    if strict_pass:
        tier = "STRICT"
    elif waiver_pass:
        tier = "WAIVER"
    elif mass_closes:
        tier = "MARGINAL"
    else:
        tier = "FAIL"

    return {
        "power_mwe": p_mwe,
        "isp_spiral_s": isp_spiral,
        "isp_inbound_s": isp_inbound,
        "dv_spiral_kms": dv_spiral,
        "mr_spiral": round(spiral["mr"], 4),
        "mr_inbound": round(inbound["mr"], 4),
        "m_prop_spiral_t": round(spiral["m_prop_t"], 2),
        "m_prop_inbound_t": round(inbound["m_prop_t"], 2),
        "m_after_spiral_t": round(spiral["m_end_t"], 2),
        "m_at_earth_t": round(m_at_earth, 2),
        "m_delivered_t": round(m_delivered, 3),
        "delivered_pct": round(delivered_pct, 3),
        "t_spiral_yr": round(t_spiral_yr, 3),
        "t_inbound_yr": round(t_inbound_yr, 3),
        "t_total_burn_yr": round(t_total_burn_yr, 3),
        "t_total_mission_yr": round(t_total_mission_yr, 3),
        "mass_closes": "yes" if mass_closes else "no",
        "l0_04_pass": "yes" if l0_04_pass else "no",
        "strict_pass": "yes" if strict_pass else "no",
        "waiver_pass": "yes" if waiver_pass else "no",
        "tier": tier,
    }


# ----------------------------------------------------------------------------
# Main sweep
# ----------------------------------------------------------------------------

rows = []
for p_mwe in POWER_GRID_MWE:
    for isp_s in ISP_GRID:
        for isp_i in ISP_GRID:
            for dv_sp in DV_SPIRAL_GRID_KMS:
                rows.append(evaluate_cell(p_mwe, isp_s, isp_i, dv_sp))

with open(OUT / "closure_grid.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)

closing = [r for r in rows if r["tier"] in ("STRICT", "WAIVER")]
with open(OUT / "closing_cells.csv", "w", newline="") as f:
    if closing:
        w = csv.DictWriter(f, fieldnames=list(closing[0].keys()))
        w.writeheader()
        w.writerows(closing)
    else:
        f.write("# no cells achieved WAIVER or STRICT tier\n")


# ----------------------------------------------------------------------------
# Counterfactual: Block 11's impulsive-exit reference at 500 kWe with no dwell
# (this is what Block 11 would have shown if dwell constraint had been dropped
# but Δv had been kept at the unrealistic impulsive 7.4 km/s)
# ----------------------------------------------------------------------------

impulsive_rows = []
for isp_s in ISP_GRID:
    for isp_i in ISP_GRID:
        r = evaluate_cell(0.5, isp_s, isp_i, DV_IMPULSIVE_EXIT_REF_KMS)
        r["note"] = "impulsive_exit_ref_no_dwell"
        impulsive_rows.append(r)

with open(OUT / "impulsive_exit_no_dwell_reference.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(impulsive_rows[0].keys()))
    w.writeheader()
    w.writerows(impulsive_rows)


# ----------------------------------------------------------------------------
# Hypothesis adjudication
# ----------------------------------------------------------------------------

# Filter to the baseline spiral Δv for headline hypotheses
baseline = [r for r in rows if r["dv_spiral_kms"] == 18.0]
b500 = [r for r in baseline if r["power_mwe"] == 0.5]

# H1: zero STRICT cells at 500 kWe / 18 km/s
h1_strict_cells = [r for r in b500 if r["tier"] == "STRICT"]
H1_status = "held" if len(h1_strict_cells) == 0 else "falsified"

# H2: >= 1 WAIVER cell with delivered >= 10% at 500 kWe / 18 km/s
h2_waiver_cells = [r for r in b500
                   if r["tier"] in ("WAIVER", "STRICT")
                   and r["delivered_pct"] >= 10.0]
H2_status = "held" if len(h2_waiver_cells) >= 1 else "falsified"

# H3: optimal cell at 500 kWe / 18 km/s under waiver lies at
# Isp_spiral [5000, 7000], Isp_inbound [7000, 9000], delivered [8, 15]%
waiver_or_strict_500 = [r for r in b500 if r["tier"] in ("WAIVER", "STRICT")]
if waiver_or_strict_500:
    optimal = max(waiver_or_strict_500, key=lambda r: r["delivered_pct"])
    in_isp_s_band = 5000 <= optimal["isp_spiral_s"] <= 7000
    in_isp_i_band = 7000 <= optimal["isp_inbound_s"] <= 9000
    in_df_band = 8.0 <= optimal["delivered_pct"] <= 15.0
    in_loose_df_band = 4.0 <= optimal["delivered_pct"] <= 20.0
    h3_status = (
        "held" if (in_isp_s_band and in_isp_i_band and in_df_band)
        else "marginal" if (in_loose_df_band)
        else "falsified"
    )
else:
    optimal = None
    h3_status = "falsified_no_closure"
H3_status = h3_status

# H4: net spiral-vs-Block-11 delta at 500 kWe is +2 to +8 pp
# Block 11 best at 500 kWe was 0 (no closure at all). So delta = optimal df.
if waiver_or_strict_500:
    h4_delta_pp = optimal["delivered_pct"] - 0.0
    H4_status = ("held" if 2.0 <= h4_delta_pp <= 8.0
                 else "marginal" if 0.0 <= h4_delta_pp <= 12.0
                 else "falsified")
else:
    h4_delta_pp = 0.0
    H4_status = "falsified"

# H5: architecture verdict — H1 held + H2 held + H3 in band + H4 in band
H5_status = "held" if all(s in ("held", "marginal")
                           for s in (H1_status, H2_status, H3_status, H4_status)
                          ) and H2_status == "held" else "falsified"

# H6: Δv_spiral 14 km/s -> optimal delivered ~ 2x the 18 km/s case
b14 = [r for r in rows if r["dv_spiral_kms"] == 14.0 and r["power_mwe"] == 0.5]
waiver_b14 = [r for r in b14 if r["tier"] in ("WAIVER", "STRICT")]
if waiver_b14 and waiver_or_strict_500:
    opt_14 = max(waiver_b14, key=lambda r: r["delivered_pct"])
    if optimal and optimal["delivered_pct"] > 0:
        ratio = opt_14["delivered_pct"] / optimal["delivered_pct"]
    else:
        ratio = float("inf")
    H6_status = ("held" if 1.3 <= ratio <= 3.0
                 else "marginal" if 1.1 <= ratio <= 4.0
                 else "falsified")
    H6_ratio = ratio
elif waiver_b14 and not waiver_or_strict_500:
    # Block 11-equivalent (18 km/s) failed but 14 km/s closes -> high sensitivity
    H6_status = "held_strongly_or_threshold_effect"
    H6_ratio = float("inf")
else:
    H6_status = "no_closure_at_14_km_s_either"
    H6_ratio = 0.0

# ----------------------------------------------------------------------------
# Spiral-vs-Block-11 comparison rows
# ----------------------------------------------------------------------------

compare = []
for p_mwe in POWER_GRID_MWE:
    cells_for_p = [r for r in baseline if r["power_mwe"] == p_mwe
                   and r["tier"] in ("STRICT", "WAIVER")]
    if cells_for_p:
        best = max(cells_for_p, key=lambda r: r["delivered_pct"])
        compare.append({
            "power_mwe": p_mwe,
            "spiral_tier": best["tier"],
            "spiral_max_df_pct": best["delivered_pct"],
            "spiral_isp_combo": f"{best['isp_spiral_s']} / {best['isp_inbound_s']}",
            "spiral_t_total_burn_yr": best["t_total_burn_yr"],
            "spiral_t_total_mission_yr": best["t_total_mission_yr"],
            "spiral_m_delivered_t": best["m_delivered_t"],
        })
    else:
        compare.append({
            "power_mwe": p_mwe,
            "spiral_tier": "FAIL",
            "spiral_max_df_pct": 0.0,
            "spiral_isp_combo": "n/a",
            "spiral_t_total_burn_yr": "n/a",
            "spiral_t_total_mission_yr": "n/a",
            "spiral_m_delivered_t": 0.0,
        })

# Block 11's max-delivered per power class (from R_composite_burn_time_closure summary)
block11_ref = {
    0.5: {"max_df_pct": 0.0, "isp_combo": "n/a (no closure at any Isp)"},
    1.0: {"max_df_pct": 0.0, "isp_combo": "n/a (mass closure fails)"},
    2.0: {"max_df_pct": 0.0, "isp_combo": "n/a (mass closure fails)"},
    5.0: {"max_df_pct": 22.76, "isp_combo": "3000 / 9000"},
}
for c in compare:
    p = c["power_mwe"]
    if p in block11_ref:
        c["block11_max_df_pct"] = block11_ref[p]["max_df_pct"]
        c["block11_isp_combo"] = block11_ref[p]["isp_combo"]
        c["delta_pp"] = round(c["spiral_max_df_pct"] - block11_ref[p]["max_df_pct"], 3)
    else:
        c["block11_max_df_pct"] = "n/a"
        c["block11_isp_combo"] = "n/a"
        c["delta_pp"] = "n/a"

with open(OUT / "spiral_vs_block11_compare.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(compare[0].keys()))
    w.writeheader()
    w.writerows(compare)


# ----------------------------------------------------------------------------
# Summary JSON
# ----------------------------------------------------------------------------

summary = {
    "model_parameters": {
        "m_at_start_t": M_AT_START_T,
        "m_dry_total_t": M_DRY_TOTAL_T,
        "dv_inbound_net_kms": DV_INBOUND_NET_KMS,
        "eta": ETA,
        "outbound_overhead_yr": OUTBOUND_OVERHEAD_YR,
        "burn_budget_strict_yr": T_STRICT_BUDGET_YR,
        "burn_budget_waiver_yr": T_WAIVER_BUDGET_YR,
        "l0_04_floor_t": L0_04_FLOOR_T,
    },
    "grids": {
        "power_mwe": POWER_GRID_MWE,
        "isp_grid_s": ISP_GRID,
        "dv_spiral_grid_kms": DV_SPIRAL_GRID_KMS,
        "impulsive_exit_ref_kms": DV_IMPULSIVE_EXIT_REF_KMS,
    },
    "totals": {
        "cell_count": len(rows),
        "closing_cell_count_any_tier": len(closing),
        "strict_cell_count": sum(1 for r in rows if r["tier"] == "STRICT"),
        "waiver_cell_count": sum(1 for r in rows if r["tier"] == "WAIVER"),
        "marginal_cell_count": sum(1 for r in rows if r["tier"] == "MARGINAL"),
        "fail_cell_count": sum(1 for r in rows if r["tier"] == "FAIL"),
    },
    "baseline_500kWe_18kms_optimal": optimal,
    "hypothesis_adjudication": {
        "H1_zero_STRICT_at_500kWe_18kms": {
            "status": H1_status,
            "strict_cell_count": len(h1_strict_cells),
        },
        "H2_at_least_one_WAIVER_above_10pct_at_500kWe_18kms": {
            "status": H2_status,
            "waiver_above_10pct_count": len(h2_waiver_cells),
        },
        "H3_optimal_at_isp_spiral_5k_7k_inbound_7k_9k_df_8_15pct": {
            "status": H3_status,
        },
        "H4_net_spiral_vs_block11_delta_500kWe_2_to_8pp": {
            "status": H4_status,
            "delta_pp": h4_delta_pp,
        },
        "H5_architecture_verdict_waiver_save_only": {
            "status": H5_status,
        },
        "H6_dv_spiral_14kms_doubles_delivered": {
            "status": H6_status,
            "ratio_14_to_18": H6_ratio,
        },
    },
}

with open(OUT / "summary.json", "w") as f:
    json.dump(summary, f, indent=2, default=str)


# ----------------------------------------------------------------------------
# Console summary
# ----------------------------------------------------------------------------

print("=" * 78)
print("R-spiral-out-exit-architecture -- results")
print("=" * 78)
print()
print(f"Cells:           {len(rows)}  "
      f"(STRICT {summary['totals']['strict_cell_count']}, "
      f"WAIVER {summary['totals']['waiver_cell_count']}, "
      f"MARGINAL {summary['totals']['marginal_cell_count']}, "
      f"FAIL {summary['totals']['fail_cell_count']})")
print()
print(f"Constraint relaxation: Block 11 = 6-month dwell on exit. "
      f"Here = mission ≤ {T_STRICT_BUDGET_YR + OUTBOUND_OVERHEAD_YR:.0f} yr strict, "
      f"≤ {T_WAIVER_BUDGET_YR + OUTBOUND_OVERHEAD_YR:.0f} yr waiver (sum of burns).")
print(f"Δv penalty:           Block 11 = impulsive 7.4 km/s exit. "
      f"Here = {DV_SPIRAL_GRID_KMS[1]:.1f} km/s spiral baseline.")
print()
print("Spiral-out vs Block 11 (composite burn-time closure) by power class:")
print(f"  {'P (MWe)':<10}  {'B11 max df':<12}  "
      f"{'spiral max df':<14}  {'Δ pp':<8}  "
      f"{'spiral tier':<10}  {'spiral mission (yr)':<18}")
for c in compare:
    print(f"  {c['power_mwe']:<10.1f}  "
          f"{c['block11_max_df_pct']:<12}  "
          f"{c['spiral_max_df_pct']:<14}  "
          f"{c['delta_pp']:<8}  "
          f"{c['spiral_tier']:<10}  "
          f"{c['spiral_t_total_mission_yr']}")
print()
print(f"Headline cell — 500 kWe, Δv_spiral 18 km/s, optimal:")
if optimal:
    print(f"  Isp_spiral / Isp_inbound:   {optimal['isp_spiral_s']} / {optimal['isp_inbound_s']} s")
    print(f"  delivered fraction:          {optimal['delivered_pct']:.2f}%  "
          f"({optimal['m_delivered_t']:.2f} t)")
    print(f"  total burn time:             {optimal['t_total_burn_yr']:.2f} yr "
          f"(spiral {optimal['t_spiral_yr']:.2f} + inbound {optimal['t_inbound_yr']:.2f})")
    print(f"  total mission duration:      {optimal['t_total_mission_yr']:.2f} yr  "
          f"(tier {optimal['tier']})")
else:
    print("  (no closing cell at 500 kWe / 18 km/s spiral)")
print()
print("Hypothesis adjudication:")
for name, data in summary["hypothesis_adjudication"].items():
    print(f"  {name}: {data['status']}")
print()
print(f"H6 sensitivity ratio (Δv_spiral 14 km/s vs 18 km/s optimal df): "
      f"{H6_ratio if isinstance(H6_ratio, float) and H6_ratio != float('inf') else H6_ratio}")
