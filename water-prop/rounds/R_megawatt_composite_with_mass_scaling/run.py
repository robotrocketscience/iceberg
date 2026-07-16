"""Block 14 - R-megawatt-composite-with-mass-scaling.

Re-runs the Block-11 joint burn-time / mass-closure sweep with vehicle
dry mass scaled per four specific-power models from locked-memory
ICEBERG power findings 1 and 4.

  Mass models for power-subsystem mass M_power (tonnes) at P megawatt-electric:
    paper_aspirational  : 25  * P_MWe          (40 W/kg, TRL-2 aspirational)
    bottoms_up_moderate : 100 * P_MWe          (10 W/kg, KRUSTY x 4)
    krusty_anchored     : 417 * P_MWe          (2.4 W/kg, KRUSTY system-level)
    bundled_finding_4   : 5 + 100 * P_MWe      (orchestrator rule-of-thumb)

Vehicle dry mass:
    M_dry_total = M_struct_base + M_power(P) - M_jettison + M_shield
  with M_struct_base = 150 t (Block-4 200 t minus implicit ~50 t power at 500 kWe).

Closure for a cell requires (a) exit burn time <= 6 months,
(b) inbound burn time <= 6 years, (c) delivered water mass > 0.

Outputs in results/ ; hypothesis adjudication in summary.json.
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

# ---------------------------------------------------------------------------
# Constants (Block 4 / 9 / 11 nominal)
# ---------------------------------------------------------------------------

M_COLLECTED_T = 200.0
M_STRUCT_BASE_T = 150.0        # Variant B 200 t minus ~50 t implicit power at 500 kWe
M_JETTISON_T = 20.0
M_SHIELD_T = 4.13

DV_EXIT_KMS = 7.4
DV_INBOUND_NET_KMS = 23.2

ETA = 0.65
EXIT_DWELL_BUDGET_S = 6.0 * SEC_PER_MONTH
CRUISE_BUDGET_S = 6.0 * SEC_PER_YEAR

POWER_GRID_MWE = [1.0, 2.0, 5.0, 10.0]
ISP_GRID = [3000, 5000, 7000, 9000]

MASS_MODELS = {
    "paper_aspirational":  lambda p_mwe: 25.0  * p_mwe,
    "bottoms_up_moderate": lambda p_mwe: 100.0 * p_mwe,
    "krusty_anchored":     lambda p_mwe: 417.0 * p_mwe,
    "bundled_finding_4":   lambda p_mwe: 5.0 + 100.0 * p_mwe,
}

# ---------------------------------------------------------------------------
# Physics helpers
# ---------------------------------------------------------------------------

def m_dry_total(p_mwe: float, model: str) -> float:
    m_power = MASS_MODELS[model](p_mwe)
    return M_STRUCT_BASE_T + m_power - M_JETTISON_T + M_SHIELD_T


def burn_time_seconds(power_w: float, isp_s: float, dv_kms: float,
                      m_start_t: float, eta: float = ETA) -> float:
    v_e = isp_s * G0
    thrust = 2.0 * eta * power_w / v_e
    mr = exp(dv_kms * 1000.0 / v_e)
    m_prop_kg = m_start_t * 1000.0 * (1.0 - 1.0 / mr)
    flow = thrust / v_e
    return float("inf") if flow <= 0.0 else m_prop_kg / flow


def cell_result(p_mwe: float, isp_e: float, isp_i: float, model: str) -> dict:
    m_dry = m_dry_total(p_mwe, model)
    m_at_exit = m_dry + M_COLLECTED_T
    mr_e = exp(DV_EXIT_KMS * 1000.0 / (isp_e * G0))
    mr_i = exp(DV_INBOUND_NET_KMS * 1000.0 / (isp_i * G0))
    m_post_exit = m_at_exit / mr_e
    m_at_earth = m_post_exit / mr_i
    delivered_t = m_at_earth - m_dry
    df_pct = (delivered_t / M_COLLECTED_T) * 100.0
    p_w = p_mwe * 1e6
    t_exit_s = burn_time_seconds(p_w, isp_e, DV_EXIT_KMS, m_at_exit)
    t_in_s = burn_time_seconds(p_w, isp_i, DV_INBOUND_NET_KMS, m_post_exit)
    exit_closes = t_exit_s <= EXIT_DWELL_BUDGET_S
    in_closes = t_in_s <= CRUISE_BUDGET_S
    mass_closes = delivered_t > 0.0
    return {
        "mass_model":   model,
        "power_mwe":    p_mwe,
        "isp_exit_s":   isp_e,
        "isp_inbound_s": isp_i,
        "m_power_t":    f"{MASS_MODELS[model](p_mwe):.2f}",
        "m_dry_total_t": f"{m_dry:.2f}",
        "m_at_exit_t":  f"{m_at_exit:.2f}",
        "m_post_exit_t": f"{m_post_exit:.3f}",
        "m_at_earth_t": f"{m_at_earth:.3f}",
        "delivered_t":  f"{delivered_t:.3f}",
        "delivered_pct": f"{df_pct:.4f}",
        "t_exit_month": f"{t_exit_s / SEC_PER_MONTH:.3f}",
        "t_inbound_year": f"{t_in_s / SEC_PER_YEAR:.4f}",
        "exit_closes":  "yes" if exit_closes else "no",
        "inbound_closes": "yes" if in_closes else "no",
        "mass_closes":  "yes" if mass_closes else "no",
        "all_close":    "yes" if (exit_closes and in_closes and mass_closes) else "no",
    }


# ---------------------------------------------------------------------------
# Anchor-cell audit (verify pre-reg arithmetic against the run engine)
# ---------------------------------------------------------------------------

anchors = [
    ("anchor_A_5MWe_3000_9000", 5.0, 3000, 9000),
    ("anchor_B_10MWe_7000_9000", 10.0, 7000, 9000),
]
anchor_rows = []
for label, p_mwe, isp_e, isp_i in anchors:
    for model in MASS_MODELS:
        r = cell_result(p_mwe, isp_e, isp_i, model)
        r["anchor_label"] = label
        anchor_rows.append(r)

with open(OUT / "anchor_cell_audit.csv", "w", newline="") as f:
    fieldnames = ["anchor_label"] + [k for k in anchor_rows[0] if k != "anchor_label"]
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    w.writerows(anchor_rows)

# ---------------------------------------------------------------------------
# Full sweep
# ---------------------------------------------------------------------------

grid_rows: list[dict] = []
closing_rows: list[dict] = []
summary_per_model_power: dict[tuple[str, float], dict] = {}

for model in MASS_MODELS:
    for p_mwe in POWER_GRID_MWE:
        key = (model, p_mwe)
        summary_per_model_power[key] = {
            "max_df_pct": -1e18,
            "isp_exit": None,
            "isp_inbound": None,
            "delivered_t": None,
            "t_exit_month": None,
            "t_inbound_year": None,
            "n_closing_cells": 0,
        }
        for isp_e in ISP_GRID:
            for isp_i in ISP_GRID:
                r = cell_result(p_mwe, isp_e, isp_i, model)
                grid_rows.append(r)
                if r["all_close"] == "yes":
                    closing_rows.append(r)
                    summary_per_model_power[key]["n_closing_cells"] += 1
                    df = float(r["delivered_pct"])
                    if df > summary_per_model_power[key]["max_df_pct"]:
                        summary_per_model_power[key].update(
                            max_df_pct=df,
                            isp_exit=isp_e,
                            isp_inbound=isp_i,
                            delivered_t=float(r["delivered_t"]),
                            t_exit_month=float(r["t_exit_month"]),
                            t_inbound_year=float(r["t_inbound_year"]),
                        )

with open(OUT / "mass_scaled_grid.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(grid_rows[0].keys()))
    w.writeheader()
    w.writerows(grid_rows)

if closing_rows:
    with open(OUT / "closing_cells.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(closing_rows[0].keys()))
        w.writeheader()
        w.writerows(closing_rows)
else:
    (OUT / "closing_cells.csv").write_text(
        "mass_model,power_mwe,isp_exit_s,isp_inbound_s,delivered_pct\n"
        "# (no closing cells across the entire 256-cell sweep)\n"
    )

summary_rows = []
for (model, p_mwe), v in sorted(summary_per_model_power.items()):
    summary_rows.append({
        "mass_model":    model,
        "power_mwe":     p_mwe,
        "any_closure":   "yes" if v["max_df_pct"] >= 0 else "no",
        "n_closing":     v["n_closing_cells"],
        "max_df_pct":    f"{v['max_df_pct']:.4f}" if v["max_df_pct"] >= 0 else "n/a",
        "isp_exit":      v["isp_exit"] or "n/a",
        "isp_inbound":   v["isp_inbound"] or "n/a",
        "delivered_t":   f"{v['delivered_t']:.3f}" if v["delivered_t"] is not None else "n/a",
        "t_exit_month":  f"{v['t_exit_month']:.3f}" if v["t_exit_month"] is not None else "n/a",
        "t_inbound_year": f"{v['t_inbound_year']:.4f}" if v["t_inbound_year"] is not None else "n/a",
    })

with open(OUT / "summary_by_mass_model.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(summary_rows[0].keys()))
    w.writeheader()
    w.writerows(summary_rows)

# ---------------------------------------------------------------------------
# Hypothesis adjudication
# ---------------------------------------------------------------------------

def max_df(model: str, p_mwe: float) -> float:
    return summary_per_model_power[(model, p_mwe)]["max_df_pct"]


def in_band(x: float, lo: float, hi: float, marginal: float = 0.5) -> str:
    if x < 0:
        return "no_closure"
    if lo <= x <= hi:
        return "held"
    half_lo = lo * (1.0 - marginal)
    half_hi = hi * (1.0 + marginal)
    if half_lo <= x <= half_hi:
        return "marginal"
    return "falsified"


H1 = "held" if max_df("krusty_anchored", 5.0) < 0 else "falsified"
H2 = "held" if max_df("bottoms_up_moderate", 5.0) < 0 else "falsified"
H3 = in_band(max_df("paper_aspirational", 5.0), 5.0, 12.0)
H4 = "held" if max_df("bundled_finding_4", 5.0) < 0 else "falsified"
H5 = "held" if max_df("krusty_anchored", 10.0) < 0 else "falsified"
H6 = "held" if max_df("bottoms_up_moderate", 10.0) < 0 else "falsified"
H7 = in_band(max_df("paper_aspirational", 10.0), 7.0, 14.0)
H8 = "held" if max_df("bundled_finding_4", 10.0) < 0 else "falsified"

H9_any_low_power_closure = False
for model in MASS_MODELS:
    for p_mwe in (1.0, 2.0):
        if max_df(model, p_mwe) >= 0:
            H9_any_low_power_closure = True
H9 = "held" if not H9_any_low_power_closure else "falsified"

paper_5_ok = max_df("paper_aspirational", 5.0) >= 0
paper_10_ok = max_df("paper_aspirational", 10.0) >= 0
others_any = any(max_df(m, p) >= 0
                 for m in ("bottoms_up_moderate", "krusty_anchored", "bundled_finding_4")
                 for p in POWER_GRID_MWE)
if (paper_5_ok or paper_10_ok) and not others_any:
    H10 = "held_paper_only"
elif others_any:
    H10 = "falsified_other_model_closes"
else:
    H10 = "falsified_no_closure_at_all"

# H11: paper-aspirational max-df at 5 MWe within [6.1, 9.2] and at 10 MWe within [7.6, 11.4]
paper_5 = max_df("paper_aspirational", 5.0)
paper_10 = max_df("paper_aspirational", 10.0)
H11_5_ok = 6.1 <= paper_5 <= 9.2 if paper_5 >= 0 else False
H11_10_ok = 7.6 <= paper_10 <= 11.4 if paper_10 >= 0 else False
H11 = ("held" if (H11_5_ok and H11_10_ok)
       else "marginal" if (H11_5_ok or H11_10_ok)
       else "falsified")

# Verdict
if paper_5_ok or paper_10_ok:
    if others_any:
        verdict = "verdict_1_rescued_or_partial"
    else:
        verdict = "verdict_2_conditional_on_paper_aspirational"
else:
    verdict = "verdict_3_dead_under_block4_accounting"

summary = {
    "model_parameters": {
        "m_collected_t": M_COLLECTED_T,
        "m_struct_base_t": M_STRUCT_BASE_T,
        "m_jettison_t": M_JETTISON_T,
        "m_shield_t": M_SHIELD_T,
        "dv_exit_kms": DV_EXIT_KMS,
        "dv_inbound_net_kms": DV_INBOUND_NET_KMS,
        "eta": ETA,
        "exit_dwell_budget_months": 6.0,
        "cruise_budget_years": 6.0,
        "power_grid_mwe": POWER_GRID_MWE,
        "isp_grid_s": ISP_GRID,
        "mass_models": {
            "paper_aspirational":  "M_power_t = 25 * P_MWe (40 W/kg, TRL-2 aspirational)",
            "bottoms_up_moderate": "M_power_t = 100 * P_MWe (10 W/kg)",
            "krusty_anchored":     "M_power_t = 417 * P_MWe (2.4 W/kg, KRUSTY system-level)",
            "bundled_finding_4":   "M_power_t = 5 + 100 * P_MWe (orchestrator rule-of-thumb)",
        },
    },
    "headline_per_model_power": {
        f"{m}@{p}MWe": {
            "max_df_pct": summary_per_model_power[(m, p)]["max_df_pct"]
                          if summary_per_model_power[(m, p)]["max_df_pct"] >= 0 else None,
            "isp_exit":   summary_per_model_power[(m, p)]["isp_exit"],
            "isp_inbound": summary_per_model_power[(m, p)]["isp_inbound"],
            "n_closing":  summary_per_model_power[(m, p)]["n_closing_cells"],
        }
        for m in MASS_MODELS for p in POWER_GRID_MWE
    },
    "hypothesis_adjudication": {
        "H1_krusty_5MWe_zero_closure": H1,
        "H2_bottomsup_5MWe_zero_closure": H2,
        "H3_paper_5MWe_in_5_12_pct": H3,
        "H4_bundled_5MWe_zero_closure": H4,
        "H5_krusty_10MWe_zero_closure": H5,
        "H6_bottomsup_10MWe_zero_closure": H6,
        "H7_paper_10MWe_in_7_14_pct": H7,
        "H8_bundled_10MWe_zero_closure": H8,
        "H9_no_low_power_closure": H9,
        "H10_architectural_verdict": H10,
        "H11_methodology_functional_form_robust": H11,
    },
    "verdict": verdict,
    "n_total_cells": len(grid_rows),
    "n_all_closing": len(closing_rows),
}

with open(OUT / "summary.json", "w") as f:
    json.dump(summary, f, indent=2)

# ---------------------------------------------------------------------------
# Console rollup
# ---------------------------------------------------------------------------

print(f"R-megawatt-composite-with-mass-scaling: {len(grid_rows)} cells, "
      f"{len(closing_rows)} closing.")
print()
print("Headline — max delivered fraction (%) per (mass_model, power):")
print(f"{'model':<22} {'1 MWe':>10} {'2 MWe':>10} {'5 MWe':>10} {'10 MWe':>10}")
for model in MASS_MODELS:
    cells = []
    for p in POWER_GRID_MWE:
        v = summary_per_model_power[(model, p)]["max_df_pct"]
        cells.append(f"{v:>9.3f}%" if v >= 0 else f"{'no close':>10}")
    print(f"{model:<22} " + " ".join(cells))
print()
print("Hypothesis adjudication:")
for k, v in summary["hypothesis_adjudication"].items():
    print(f"  {k:<48} {v}")
print()
print(f"Verdict: {verdict}")
