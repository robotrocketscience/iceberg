"""Joint burn-time closure for residence-class composite.

For each (power, isp_exit, isp_inbound) cell:
  - exit_burn_time at exit_power, isp_exit, dv 7.4 km/s, m_at_exit 380 t
  - inbound_burn_time at inbound_power, isp_inbound, dv 23.2 km/s, m_after_exit
  - delivered_fraction via Block 9 Tsiolkovsky calculator (4.13 t shield, 20 t jettison)

A cell *closes* if exit_time <= 6 months AND inbound_time <= 6 years.
"""

from __future__ import annotations

import csv
import json
from math import exp
from pathlib import Path

G0 = 9.80665
SEC_PER_MONTH = 30.4375 * 86400.0
SEC_PER_YEAR = 365.25 * 86400.0

OUT = Path(__file__).parent / "results"
OUT.mkdir(parents=True, exist_ok=True)

# Composite parameters (Block 4 / Block 9 nominal)
M_COLLECTED_T = 200.0
M_DRY_BASE_T = 200.0
M_JETTISON_T = 20.0
M_SHIELD_T = 4.13
M_DRY_TOTAL_T = M_DRY_BASE_T - M_JETTISON_T + M_SHIELD_T   # 184.13
M_AT_EXIT_T = M_COLLECTED_T + M_DRY_TOTAL_T                # 384.13

DV_EXIT_KMS = 7.4
DV_INBOUND_NET_KMS = 23.2

ETA = 0.65
EXIT_DWELL_BUDGET_S = 6.0 * SEC_PER_MONTH
CRUISE_BUDGET_S = 6.0 * SEC_PER_YEAR

# Sweep grids
POWER_GRID_MWE = [0.5, 1.0, 2.0, 5.0, 10.0]      # megawatt-electric (single reactor)
ISP_GRID = [1000, 2000, 3000, 5000, 7000, 9000]   # s


def burn_time_seconds(power_w: float, isp_s: float, dv_kms: float,
                      m_start_t: float, eta: float = ETA) -> float:
    v_e = isp_s * G0
    thrust = 2.0 * eta * power_w / v_e
    mr = exp(dv_kms * 1000.0 / v_e)
    m_prop_kg = m_start_t * 1000.0 * (1.0 - 1.0 / mr)
    flow = thrust / v_e
    if flow <= 0.0:
        return float("inf")
    return m_prop_kg / flow


def delivered_fraction(isp_exit: float, isp_inbound: float) -> float:
    """Block 9 formula: water-only delivered (shield ablates, dry returns)."""
    mr_e = exp(DV_EXIT_KMS * 1000.0 / (isp_exit * G0))
    mr_i = exp(DV_INBOUND_NET_KMS * 1000.0 / (isp_inbound * G0))
    m_post_exit = M_AT_EXIT_T / mr_e
    m_at_earth = m_post_exit / mr_i
    m_delivered = max(0.0, m_at_earth - M_DRY_TOTAL_T)
    return m_delivered / M_COLLECTED_T


# -----------------------------------------------------------------------------
# Sweep
# -----------------------------------------------------------------------------

grid_rows = []
closing_rows = []
max_per_power = {p: {"max_df_pct": -1.0, "isp_exit": None,
                      "isp_inbound": None, "t_exit_mo": None,
                      "t_inbound_yr": None} for p in POWER_GRID_MWE}

for p_mwe in POWER_GRID_MWE:
    p_w = p_mwe * 1e6
    for isp_e in ISP_GRID:
        # m_after_exit depends on isp_e
        mr_e = exp(DV_EXIT_KMS * 1000.0 / (isp_e * G0))
        m_after_exit_t = M_AT_EXIT_T / mr_e
        t_exit_s = burn_time_seconds(p_w, isp_e, DV_EXIT_KMS, M_AT_EXIT_T)
        for isp_i in ISP_GRID:
            t_in_s = burn_time_seconds(p_w, isp_i, DV_INBOUND_NET_KMS,
                                       m_after_exit_t)
            df_pct = delivered_fraction(isp_e, isp_i) * 100.0
            exit_closes = t_exit_s <= EXIT_DWELL_BUDGET_S
            in_closes = t_in_s <= CRUISE_BUDGET_S
            both_close = exit_closes and in_closes
            t_exit_mo = t_exit_s / SEC_PER_MONTH
            t_in_yr = t_in_s / SEC_PER_YEAR
            row = {
                "power_mwe":    p_mwe,
                "isp_exit_s":   isp_e,
                "isp_inbound_s": isp_i,
                "t_exit_month": f"{t_exit_mo:.2f}",
                "t_inbound_year": f"{t_in_yr:.3f}",
                "exit_closes":  "yes" if exit_closes else "no",
                "inbound_closes": "yes" if in_closes else "no",
                "both_close":   "yes" if both_close else "no",
                "delivered_pct": f"{df_pct:.3f}",
            }
            grid_rows.append(row)
            if both_close:
                closing_rows.append(row)
                if df_pct > max_per_power[p_mwe]["max_df_pct"]:
                    max_per_power[p_mwe] = {
                        "max_df_pct": df_pct,
                        "isp_exit": isp_e,
                        "isp_inbound": isp_i,
                        "t_exit_mo": t_exit_mo,
                        "t_inbound_yr": t_in_yr,
                    }

with open(OUT / "closure_grid.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(grid_rows[0].keys()))
    w.writeheader()
    w.writerows(grid_rows)

with open(OUT / "closing_cells.csv", "w", newline="") as f:
    if closing_rows:
        w = csv.DictWriter(f, fieldnames=list(closing_rows[0].keys()))
        w.writeheader()
        w.writerows(closing_rows)

max_rows = []
for p_mwe in POWER_GRID_MWE:
    r = max_per_power[p_mwe]
    max_rows.append({
        "power_mwe":     p_mwe,
        "any_closure":   "yes" if r["max_df_pct"] >= 0 else "no",
        "max_df_pct":    f"{r['max_df_pct']:.3f}" if r["max_df_pct"] >= 0 else "n/a",
        "isp_exit":      r["isp_exit"] or "n/a",
        "isp_inbound":   r["isp_inbound"] or "n/a",
        "t_exit_month":  f"{r['t_exit_mo']:.2f}" if r["t_exit_mo"] is not None else "n/a",
        "t_inbound_year": f"{r['t_inbound_yr']:.3f}" if r["t_inbound_yr"] is not None else "n/a",
    })

with open(OUT / "max_delivered_per_power.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(max_rows[0].keys()))
    w.writeheader()
    w.writerows(max_rows)


# -----------------------------------------------------------------------------
# Hypothesis adjudication
# -----------------------------------------------------------------------------

# H1: at 500 kilowatt-electric, no closing regime delivers > 3.9%
closing_at_500kwe = [r for r in closing_rows if r["power_mwe"] == 0.5]
max_df_500kwe = max((float(r["delivered_pct"]) for r in closing_at_500kwe),
                    default=-1.0)
H1_status = ("held" if max_df_500kwe < 3.9 else
             "marginal" if max_df_500kwe < 6.0 else "falsified")

# H2: at 500 kilowatt-electric, closure at Isp_exit <= 1000 AND Isp_inbound <= 2000
# AND delivered < 8%
h2_closure = [r for r in closing_at_500kwe
              if r["isp_exit_s"] <= 1000 and r["isp_inbound_s"] <= 2000]
H2_status = ("held" if h2_closure
             and all(float(r["delivered_pct"]) < 8.0 for r in h2_closure)
             else "marginal" if h2_closure
             else "falsified_no_low_isp_closure")

# H3: min power for joint closure at Isp_exit=7000 / Isp_inbound=5000 is in [5, 15] MWe
h3_cells = [r for r in grid_rows
            if r["isp_exit_s"] == 7000 and r["isp_inbound_s"] == 5000
            and r["both_close"] == "yes"]
min_p_h3 = min((r["power_mwe"] for r in h3_cells), default=float("inf"))
H3_status = ("held" if 5.0 <= min_p_h3 <= 15.0
             else "marginal" if 2.0 <= min_p_h3 <= 25.0
             else "falsified")

# H4: 1 megawatt-electric has a closure regime; max delivered 8-14%
max_df_1mwe = max_per_power[1.0]["max_df_pct"]
H4_status = ("held" if 8.0 <= max_df_1mwe <= 14.0
             else "marginal" if max_df_1mwe >= 0 and (
                 5.0 <= max_df_1mwe <= 18.0)
             else "falsified")

# H5: architecture verdict
# Held if H1 held and H3 held (resolution requires 5-15 MWe, no 500-kWe save)
H5_status = ("held" if H1_status == "held" and H3_status in ("held", "marginal")
             else "falsified")

# Cross-reference: what's the max delivered at any closing regime overall?
max_df_overall = max((float(r["delivered_pct"]) for r in closing_rows),
                     default=-1.0)

summary = {
    "model_parameters": {
        "m_at_exit_t": M_AT_EXIT_T,
        "m_dry_total_t": M_DRY_TOTAL_T,
        "dv_exit_kms": DV_EXIT_KMS,
        "dv_inbound_net_kms": DV_INBOUND_NET_KMS,
        "eta": ETA,
        "exit_dwell_budget_months": 6.0,
        "cruise_budget_years": 6.0,
    },
    "power_grid_mwe": POWER_GRID_MWE,
    "isp_grid_s": ISP_GRID,
    "max_delivered_per_power": {str(k): v for k, v in max_per_power.items()},
    "max_delivered_overall_pct": max_df_overall,
    "count_closing_cells": len(closing_rows),
    "count_total_cells": len(grid_rows),
    "hypothesis_adjudication": {
        "H1_no_closure_above_baseline_at_500kWe": {
            "status": H1_status,
            "max_df_500kwe_pct": max_df_500kwe,
        },
        "H2_low_isp_closure_at_500kWe_below_8pct": {
            "status": H2_status,
        },
        "H3_min_power_optimal_isp_5_to_15_MWe": {
            "status": H3_status,
            "min_power_mwe": min_p_h3,
        },
        "H4_1MWe_closure_at_8_to_14pct": {
            "status": H4_status,
            "max_df_1mwe_pct": max_df_1mwe,
        },
        "H5_architecture_conditional_on_megawatt_or_reframe": {
            "status": H5_status,
        },
    },
}

with open(OUT / "summary.json", "w") as f:
    json.dump(summary, f, indent=2, default=str)


# -----------------------------------------------------------------------------
# Console summary
# -----------------------------------------------------------------------------

print("=" * 72)
print("R-composite-burn-time-closure -- results")
print("=" * 72)
print()
print(f"Total cells:    {len(grid_rows)}")
print(f"Closing cells:  {len(closing_rows)}")
print(f"Max delivered fraction across any closing cell: {max_df_overall:.2f}%")
print()
print("Max delivered fraction per power class (at closing regimes):")
print(f"  {'P (MWe)':<10}  {'any closure?':<14}  {'max delivered':<14}  "
      f"  isp_exit / isp_inbound  exit_mo  inbound_yr")
for p_mwe in POWER_GRID_MWE:
    r = max_per_power[p_mwe]
    closure_str = "yes" if r["max_df_pct"] >= 0 else "no"
    max_str = (f"{r['max_df_pct']:.2f}%" if r["max_df_pct"] >= 0
               else "(no closure)")
    isp_str = (f"{r['isp_exit']} / {r['isp_inbound']}"
               if r["isp_exit"] else "n/a")
    exit_mo = f"{r['t_exit_mo']:.1f}" if r["t_exit_mo"] else "n/a"
    in_yr = f"{r['t_inbound_yr']:.2f}" if r["t_inbound_yr"] else "n/a"
    print(f"  {p_mwe:<10.1f}  {closure_str:<14}  {max_str:<14}  "
          f"  {isp_str:<18}  {exit_mo:<7}  {in_yr}")

print()
print("Hypothesis adjudication:")
for hname, hdata in summary["hypothesis_adjudication"].items():
    print(f"  {hname}: {hdata['status']}")
print()
print(f"H1 details: max delivered fraction at 500 kWe = {max_df_500kwe:.2f}% "
      f"(closing cells: {len(closing_at_500kwe)})")
print(f"H3 details: min power for Isp_exit=7000 / Isp_inbound=5000 closure "
      f"= {min_p_h3} MWe")
print(f"H4 details: max delivered fraction at 1 MWe closing regime "
      f"= {max_df_1mwe:.2f}%")
