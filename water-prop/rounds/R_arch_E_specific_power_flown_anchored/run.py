"""R-arch-E-specific-power-flown-anchored — round 9.

Replicates round-6 Architecture-E sweep physics exactly, but sweeps THREE
specific-power anchors instead of two equivalent ones:

  - bundled_10_W_per_kg     — round-6's "conservative" bookend (= decomposed_marvl)
  - bundled_5_W_per_kg      — intermediate
  - bundled_2p4_W_per_kg    — KRUSTY-2018 ground-test anchor

Also verifies round-6's two mass models are mathematically equivalent.

Pre-registration in STUDY.md (H-9-a through H-9-h).
"""

from __future__ import annotations

import json
import math
from pathlib import Path

from waterprop.constants import A_EARTH, A_SATURN, G0, GM_SUN

YEAR_S = 365.25 * 86400.0
ETA_THR = 0.65
SATURN_OPS_YR = 1.0
DV_OUTBOUND_HE_NO_LGA_KM_S = 29.56
DV_INBOUND_TITAN_HE_LGA_KM_S = 24.7

REACTOR_POWERS_KWE = [40.0, 100.0, 200.0, 500.0, 1000.0]
CHUNK_MASSES_T = [30.0, 50.0, 100.0, 200.0]
ISP_VALUES_S = [1500.0, 2000.0, 2934.0]

MASS_MODELS: dict[str, dict] = {
    "decomposed_marvl": {  # round-6 model; verified equivalent to bundled_10
        "kind": "decomposed",
        "m_fixed_t": 5.0,
        "alpha_reactor_W_per_kg": 33.0,
        "alpha_PC_W_per_kg": 50.0,
        "alpha_radiator_kW_th_per_kg": 0.047,
        "eta_conv": 0.30,
        "f_tank": 0.05,
    },
    "bundled_10_W_per_kg": {
        "kind": "bundled",
        "m_fixed_t": 5.0,
        "specific_power_total_w_per_kg": 10.0,
    },
    "bundled_5_W_per_kg": {  # NEW — intermediate between KRUSTY and round-6
        "kind": "bundled",
        "m_fixed_t": 5.0,
        "specific_power_total_w_per_kg": 5.0,
    },
    "bundled_2p4_W_per_kg": {  # NEW — KRUSTY-2018 ground-test system-level
        "kind": "bundled",
        "m_fixed_t": 5.0,
        "specific_power_total_w_per_kg": 2.4,
    },
}


def dry_mass_t(model: dict, reactor_kwe: float, m_prop_t: float = 0.0) -> float:
    if model["kind"] == "bundled":
        m_stack = reactor_kwe / model["specific_power_total_w_per_kg"]
        return model["m_fixed_t"] + m_stack + m_prop_t * 0.05
    eta = model["eta_conv"]
    p_th_waste_kw = reactor_kwe * (1.0 - eta) / eta
    m_reactor = reactor_kwe / model["alpha_reactor_W_per_kg"]
    m_pc = reactor_kwe / model["alpha_PC_W_per_kg"]
    m_rad = p_th_waste_kw / model["alpha_radiator_kW_th_per_kg"] / 1000.0
    m_tank = m_prop_t * model["f_tank"]
    return model["m_fixed_t"] + m_reactor + m_pc + m_rad + m_tank


def burn_from_dry_end(m_final_t, dv_km_s, power_kwe, isp_s, eta=ETA_THR):
    v_e = isp_s * G0
    thrust_N = 2.0 * eta * power_kwe * 1000.0 / v_e
    mass_ratio = math.exp(dv_km_s * 1000.0 / v_e)
    m_prop_t = m_final_t * (mass_ratio - 1.0)
    t_burn_s = m_prop_t * 1000.0 * v_e / thrust_N
    return {"thrust_N": thrust_N, "m_prop_t": m_prop_t, "mass_ratio": mass_ratio,
            "t_burn_s": t_burn_s, "t_burn_yr": t_burn_s / YEAR_S}


def burn_from_wet(m_initial_t, dv_km_s, power_kwe, isp_s, eta=ETA_THR):
    v_e = isp_s * G0
    thrust_N = 2.0 * eta * power_kwe * 1000.0 / v_e
    mass_ratio = math.exp(dv_km_s * 1000.0 / v_e)
    m_prop_t = m_initial_t * (1.0 - 1.0 / mass_ratio)
    t_burn_s = m_prop_t * 1000.0 * v_e / thrust_N
    return {"thrust_N": thrust_N, "m_prop_t": m_prop_t, "mass_ratio": mass_ratio,
            "t_burn_s": t_burn_s, "t_burn_yr": t_burn_s / YEAR_S}


def hohmann_cruise_yr() -> float:
    a_h_km = (A_EARTH + A_SATURN) / 2.0
    return math.pi * math.sqrt(a_h_km ** 3 / GM_SUN) / YEAR_S


def round_trip_E(model, reactor_kwe, chunk_t, isp_s,
                 dv_outbound_km_s=DV_OUTBOUND_HE_NO_LGA_KM_S,
                 dv_inbound_km_s=DV_INBOUND_TITAN_HE_LGA_KM_S):
    """Architecture E: pure all-electric end-to-end. Self-consistent outbound mass."""
    m_tug_t = dry_mass_t(model, reactor_kwe, m_prop_t=0.0)
    converged = False
    for _ in range(80):
        burn_out = burn_from_dry_end(m_tug_t, dv_outbound_km_s, reactor_kwe, isp_s)
        new_m_tug = dry_mass_t(model, reactor_kwe, m_prop_t=burn_out["m_prop_t"])
        if abs(new_m_tug - m_tug_t) < 1e-4:
            m_tug_t = new_m_tug
            converged = True
            break
        m_tug_t = new_m_tug
    if not converged:
        return {"feasible": False, "round_trip_yr": math.inf, "delivered_t": -math.inf,
                "closes_15yr": False, "closes_20yr": False, "closes_25yr": False,
                "closes_30yr": False, "m_tug_t": m_tug_t, "note": "no convergence"}
    burn_out = burn_from_dry_end(m_tug_t, dv_outbound_km_s, reactor_kwe, isp_s)
    burn_in = burn_from_wet(m_tug_t + chunk_t, dv_inbound_km_s, reactor_kwe, isp_s)
    t_cruise_yr = hohmann_cruise_yr()
    round_trip_yr = (burn_out["t_burn_yr"] + t_cruise_yr + SATURN_OPS_YR
                     + burn_in["t_burn_yr"] + t_cruise_yr)
    delivered_t = chunk_t - burn_in["m_prop_t"]
    return {
        "feasible": True,
        "m_tug_t": m_tug_t,
        "m_prop_outbound_t": burn_out["m_prop_t"],
        "m_LEO_t": m_tug_t + burn_out["m_prop_t"],
        "thrust_N": burn_out["thrust_N"],
        "mass_ratio_outbound": burn_out["mass_ratio"],
        "m_prop_inbound_t": burn_in["m_prop_t"],
        "mass_ratio_inbound": burn_in["mass_ratio"],
        "t_outbound_burn_yr": burn_out["t_burn_yr"],
        "t_cruise_each_yr": t_cruise_yr,
        "t_saturn_ops_yr": SATURN_OPS_YR,
        "t_inbound_burn_yr": burn_in["t_burn_yr"],
        "round_trip_yr": round_trip_yr,
        "closes_15yr": round_trip_yr <= 15.0,
        "closes_20yr": round_trip_yr <= 20.0,
        "closes_25yr": round_trip_yr <= 25.0,
        "closes_30yr": round_trip_yr <= 30.0,
        "delivered_t": delivered_t,
        "delivered_fraction": delivered_t / chunk_t if chunk_t > 0 else 0.0,
    }


def run_sweep(model_name: str, model: dict) -> list[dict]:
    rows = []
    for r in REACTOR_POWERS_KWE:
        for c in CHUNK_MASSES_T:
            for isp in ISP_VALUES_S:
                cell = round_trip_E(model, r, c, isp)
                cell.update({
                    "mass_model": model_name,
                    "reactor_kwe": r,
                    "chunk_t": c,
                    "isp_s": isp,
                })
                rows.append(cell)
    return rows


def verify_equivalence(rows_marvl: list[dict], rows_b10: list[dict]) -> dict:
    """H-9-a: check decomposed_marvl == bundled_10_W_per_kg cell-by-cell."""
    max_rt_diff = 0.0
    max_del_diff = 0.0
    n_match = 0
    for a, b in zip(rows_marvl, rows_b10):
        assert (a["reactor_kwe"], a["chunk_t"], a["isp_s"]) == \
               (b["reactor_kwe"], b["chunk_t"], b["isp_s"]), "grid mismatch"
        rt_a = a["round_trip_yr"] if math.isfinite(a["round_trip_yr"]) else 999.0
        rt_b = b["round_trip_yr"] if math.isfinite(b["round_trip_yr"]) else 999.0
        rt_diff = abs(rt_a - rt_b)
        if rt_a < 100 and rt_b < 100:  # only meaningful where both feasible
            del_diff = abs(a["delivered_t"] - b["delivered_t"])
        else:
            del_diff = 0.0
        max_rt_diff = max(max_rt_diff, rt_diff)
        max_del_diff = max(max_del_diff, del_diff)
        if rt_diff < 0.01 and del_diff < 0.1:
            n_match += 1
    return {
        "max_round_trip_diff_yr": max_rt_diff,
        "max_delivered_diff_t": max_del_diff,
        "n_match_at_0p01yr_0p1t": n_match,
        "n_cells": len(rows_marvl),
        "equivalent": max_rt_diff < 0.01 and max_del_diff < 0.1,
    }


def closure_counts(rows: list[dict]) -> dict:
    pos_payload = [r for r in rows if r.get("delivered_t", -math.inf) > 0]
    return {
        "n_cells_total": len(rows),
        "n_pos_payload": len(pos_payload),
        "n_close_15yr": sum(1 for r in pos_payload if r["closes_15yr"]),
        "n_close_20yr": sum(1 for r in pos_payload if r["closes_20yr"]),
        "n_close_25yr": sum(1 for r in pos_payload if r["closes_25yr"]),
        "n_close_30yr": sum(1 for r in pos_payload if r["closes_30yr"]),
    }


def best_cell(rows: list[dict], ceiling_yr: float) -> dict | None:
    candidates = [r for r in rows
                  if r.get("round_trip_yr", math.inf) <= ceiling_yr
                  and r.get("delivered_t", -math.inf) > 0]
    if not candidates:
        return None
    return max(candidates, key=lambda r: r["delivered_t"])


# --------- Round-8 joint expected-value recompute ---------

def revenue_to_npv_positive_prob(delivered_t_per_mission: float) -> dict:
    """Map delivered_t to P(NPV+) via round-8 break-even tables.

    Round-8 corp 8.7% LR 15% break-even revenue per mission:
      Arch E_500 (50 t):     $1,298M  → $25,960/kg
      Arch E_200 (30 t):       $983M  → $32,767/kg
    Linear-scale Arch E_500 break-even revenue by delivered_t: BE_$/kg held constant.
    Then compute P(clearing_price >= BE_$/kg) from round-8's log-normal Starship × markup.
    Round-8 measured: P(clearing ≥ $25,960/kg) = 14.4% at corp 8.7%, LR15.
                      P(clearing ≥ $12,050/kg, Variant B) = 29.1%.
                      P(clearing ≥ $6,920/kg, E_500 sov 3% LR15) = 42.8%.
    Use a log-normal CDF anchored to round-8's measured points (Starship × markup MC).
    """
    if delivered_t_per_mission <= 0:
        return {"p_npv_corp_8p7_LR15": 0.0, "p_npv_sov_3_LR15": 0.0,
                "be_dollar_per_kg_corp": float("inf"),
                "be_dollar_per_kg_sov": float("inf")}
    # Round-8 fixed per-arch break-evens — same ship-cost structure preserved at E_500's 50t baseline.
    # For new delivered_t, ship cost & burn structure differ; we keep the per-mission $/kg threshold
    # at Arch-E_500's value as a first-order anchor (held constant per protocol).
    be_dollar_per_kg_corp = 25960.0
    be_dollar_per_kg_sov = 6920.0
    # Re-derive P(NPV+) by integrating round-8 lognormal clearing-price distribution.
    # Round-8: Starship ~ LN(mu=ln(1500), sigma=1.31), markup ~ LN(mu=ln(3.5), sigma=0.768)
    # clearing = Starship × markup → LN(mu_c, sigma_c) where mu_c = ln(1500)+ln(3.5),
    # sigma_c = sqrt(1.31^2 + 0.768^2)
    mu_c = math.log(1500.0) + math.log(3.5)
    sigma_c = math.sqrt(1.31 ** 2 + 0.768 ** 2)

    def lognormal_sf(threshold):  # P(X >= threshold) for X ~ LN(mu_c, sigma_c)
        if threshold <= 0:
            return 1.0
        z = (math.log(threshold) - mu_c) / sigma_c
        # SF = 0.5 * erfc(z / sqrt(2))
        return 0.5 * math.erfc(z / math.sqrt(2.0))

    return {
        "p_npv_corp_8p7_LR15": lognormal_sf(be_dollar_per_kg_corp),
        "p_npv_sov_3_LR15": lognormal_sf(be_dollar_per_kg_sov),
        "be_dollar_per_kg_corp": be_dollar_per_kg_corp,
        "be_dollar_per_kg_sov": be_dollar_per_kg_sov,
    }


def joint_expected_value(round6_posterior_arch_E: float,
                         round5_posterior_variant_B: float,
                         p_npv_corp: float, p_npv_sov: float) -> dict:
    """Naive product of posterior × P(NPV+). Mirrors round 8 STUDY.md table."""
    return {
        "arch_E_corp": round6_posterior_arch_E * p_npv_corp,
        "arch_E_sov": round6_posterior_arch_E * p_npv_sov,
        "variant_B_corp": round5_posterior_variant_B * 0.291,  # round-8 P(NPV+ corp)
        "variant_B_sov": round5_posterior_variant_B * 0.511,   # round-8 P(NPV+ sov)
    }


# --------- Main ---------

def main():
    out: dict = {
        "round": "R-arch-E-specific-power-flown-anchored",
        "author": "enceladus-r5",
        "date": "2026-05-15",
        "pre_registration": "STUDY.md (H-9-a..h)",
        "mass_models": {k: v for k, v in MASS_MODELS.items()},
        "constants": {
            "eta_thr": ETA_THR,
            "saturn_ops_yr": SATURN_OPS_YR,
            "dv_outbound_km_s": DV_OUTBOUND_HE_NO_LGA_KM_S,
            "dv_inbound_km_s": DV_INBOUND_TITAN_HE_LGA_KM_S,
            "hohmann_cruise_yr": hohmann_cruise_yr(),
        },
        "sweep_axes": {
            "reactor_kwe": REACTOR_POWERS_KWE,
            "chunk_t": CHUNK_MASSES_T,
            "isp_s": ISP_VALUES_S,
        },
    }

    # Run all 4 sweeps
    sweeps = {name: run_sweep(name, model) for name, model in MASS_MODELS.items()}

    # H-9-a: equivalence check
    equiv = verify_equivalence(sweeps["decomposed_marvl"], sweeps["bundled_10_W_per_kg"])
    out["H_9_a_equivalence_check"] = equiv

    # Closure counts per model
    closures = {name: closure_counts(rows) for name, rows in sweeps.items()}
    out["closure_counts"] = closures

    # Best cells per model at each ceiling
    bests = {}
    for name, rows in sweeps.items():
        bests[name] = {
            f"best_at_{c}yr": best_cell(rows, c)
            for c in (15, 20, 25, 30)
        }
    out["best_cells"] = bests

    # Joint expected value re-compute per specific-power anchor
    # Use round-6's posterior (Architecture E_500): 4.78%
    # Use round-5's posterior (Variant B applied to chemical-kick path): 0.78%
    POSTERIOR_ARCH_E = 0.0478
    POSTERIOR_VARIANT_B = 0.0078

    joint_per_model = {}
    for name, rows in sweeps.items():
        best_25 = best_cell(rows, 25.0)
        if best_25 is None:
            joint_per_model[name] = {
                "best_25yr_delivered_t": None,
                "p_npv": {"p_npv_corp_8p7_LR15": 0.0, "p_npv_sov_3_LR15": 0.0},
                "joint_naive_product": joint_expected_value(0.0, POSTERIOR_VARIANT_B, 0.0, 0.0),
                "note": "no positive-payload cell at 25-yr ceiling",
            }
            continue
        delivered = best_25["delivered_t"]
        # Scale Arch-E posterior by closure-quality: if delivered < 50 t (round-6 best),
        # P(NPV+) drops proportionally. Use the round-8 anchored P(NPV+) at corp/sov.
        p_npv = revenue_to_npv_positive_prob(delivered)
        # Scale posterior down: if the best cell delivers only X/50 of round-6's 50t,
        # treat posterior as effectively that-fraction. This is a structural caveat,
        # not a clean Bayesian update — recorded transparently for review.
        post_scaled = POSTERIOR_ARCH_E * min(1.0, delivered / 50.0)
        joint_per_model[name] = {
            "best_25yr_delivered_t": delivered,
            "best_25yr_round_trip_yr": best_25["round_trip_yr"],
            "best_25yr_cell": {k: best_25[k] for k in
                ("reactor_kwe", "chunk_t", "isp_s")},
            "posterior_arch_E_unscaled": POSTERIOR_ARCH_E,
            "posterior_arch_E_scaled_by_delivery": post_scaled,
            "p_npv": p_npv,
            "joint_naive_product": joint_expected_value(
                post_scaled, POSTERIOR_VARIANT_B,
                p_npv["p_npv_corp_8p7_LR15"], p_npv["p_npv_sov_3_LR15"]),
        }
    out["joint_expected_value"] = joint_per_model

    # ---- Hypothesis grading ----
    grading = {}
    # H-9-a
    grading["H_9_a"] = {
        "predicted": "decomposed_marvl == bundled_10_W_per_kg cell-by-cell to 0.01 yr / 0.1 t",
        "measured": f"max_rt_diff={equiv['max_round_trip_diff_yr']:.4f} yr, "
                    f"max_del_diff={equiv['max_delivered_diff_t']:.4f} t, "
                    f"{equiv['n_match_at_0p01yr_0p1t']}/{equiv['n_cells']} match",
        "status": "HELD" if equiv["equivalent"] else "FALSIFIED",
    }
    # H-9-b: 2-5 close at 25-yr at 5 W/kg
    n5 = closures["bundled_5_W_per_kg"]["n_close_25yr"]
    grading["H_9_b"] = {
        "predicted": "2-5 close cells at 25-yr, 5 W/kg",
        "measured": f"{n5}/60",
        "status": "HELD" if 2 <= n5 <= 5 else "FALSIFIED",
    }
    # H-9-c: 0-1 close at 25-yr at 2.4 W/kg
    n2p4 = closures["bundled_2p4_W_per_kg"]["n_close_25yr"]
    grading["H_9_c"] = {
        "predicted": "0-1 close cells at 25-yr, 2.4 W/kg",
        "measured": f"{n2p4}/60",
        "status": "HELD" if 0 <= n2p4 <= 1 else "FALSIFIED",
    }
    # H-9-d: best cell at 5 W/kg vs round-6's (50 t, 23.60 yr at 10 W/kg)
    best_5 = best_cell(sweeps["bundled_5_W_per_kg"], 25.0)
    if best_5 is not None:
        d5 = best_5["delivered_t"]; rt5 = best_5["round_trip_yr"]
        # Check whether the corresponding cell is 500 kWe / 200 t / 2934 s
        is_same_cell = (best_5.get("reactor_kwe") == 500.0
                        and best_5.get("chunk_t") == 200.0
                        and best_5.get("isp_s") == 2934.0)
        grading["H_9_d"] = {
            "predicted": "at 500 kWe / 200 t / 2934 s Isp at 5 W/kg: delivered 15-30 t, RT 24.5-26.5 yr",
            "measured": f"best cell {best_5.get('reactor_kwe')} kWe / {best_5.get('chunk_t')} t / "
                        f"{best_5.get('isp_s')} s; delivered {d5:.1f} t, RT {rt5:.2f} yr; "
                        f"matches round-6's best-cell coordinates: {is_same_cell}",
            "status": ("HELD" if (15 <= d5 <= 30 and 24.5 <= rt5 <= 26.5) else "FALSIFIED"),
        }
    else:
        grading["H_9_d"] = {
            "predicted": "best cell at 5 W/kg exists with delivered 15-30 t",
            "measured": "no positive-payload cell at 25-yr ceiling at 5 W/kg",
            "status": "FALSIFIED",
        }
    # H-9-e refined: at 2.4 W/kg, no cell at reactor <= 500 kWe closes at any ceiling <= 30 yr
    sub500_close = [r for r in sweeps["bundled_2p4_W_per_kg"]
                    if r["reactor_kwe"] <= 500.0
                    and r.get("round_trip_yr", math.inf) <= 30.0
                    and r.get("delivered_t", -math.inf) > 0]
    grading["H_9_e_refined"] = {
        "predicted": "at 2.4 W/kg, NO cell at reactor <= 500 kWe closes at any ceiling <= 30 yr",
        "measured": f"{len(sub500_close)} sub-500-kWe cells close at <= 30 yr at 2.4 W/kg",
        "status": "HELD" if len(sub500_close) == 0 else "FALSIFIED",
    }
    # H-9-f: best-case RT under 2.4 W/kg, if positive-payload cell exists, is >= 28 yr
    best_2p4_30 = best_cell(sweeps["bundled_2p4_W_per_kg"], 30.0)
    if best_2p4_30 is None:
        grading["H_9_f"] = {
            "predicted": "best-case RT at 2.4 W/kg >= 28 yr",
            "measured": "no positive-payload cell at <= 30 yr",
            "status": "VACUOUS (no cell to test)",
        }
    else:
        # Best by lowest RT — i.e. minimum round-trip cell with positive payload, any ceiling
        all_pos = [r for r in sweeps["bundled_2p4_W_per_kg"]
                   if r.get("delivered_t", -math.inf) > 0
                   and math.isfinite(r.get("round_trip_yr", math.inf))]
        if not all_pos:
            grading["H_9_f"] = {
                "predicted": "best-case RT at 2.4 W/kg >= 28 yr",
                "measured": "no positive-payload cell at all",
                "status": "VACUOUS",
            }
        else:
            min_rt = min(r["round_trip_yr"] for r in all_pos)
            grading["H_9_f"] = {
                "predicted": "best-case (min-RT) positive-payload cell at 2.4 W/kg >= 28 yr",
                "measured": f"min RT = {min_rt:.2f} yr",
                "status": "HELD" if min_rt >= 28.0 else "FALSIFIED",
            }
    # H-9-g: Arch E_500 joint corp drops <0.5% at 5 W/kg
    j5 = joint_per_model["bundled_5_W_per_kg"]["joint_naive_product"]
    grading["H_9_g"] = {
        "predicted": "Arch E_500 joint corp at 5 W/kg < 0.5% (vs round-8's 2.05% at 10 W/kg)",
        "measured": f"Arch E_500 joint corp = {j5['arch_E_corp']*100:.3f}%, "
                    f"Variant B joint corp = {j5['variant_B_corp']*100:.3f}%",
        "status": "HELD" if j5["arch_E_corp"] < 0.005 else "FALSIFIED",
    }
    # H-9-h: aggregate
    n10 = closures["bundled_10_W_per_kg"]["n_close_25yr"]
    grading["H_9_h_aggregate"] = {
        "predicted": "Architecture E's 8x credibility lift was conditioned on 10 W/kg, "
                     "which has no flight or qualified-ground heritage. Under 2.4 W/kg, "
                     "no L0-05 closure at any ceiling tested <= 30 yr.",
        "measured": f"close-cells (25 yr): 10 W/kg={n10}, 5 W/kg={n5}, 2.4 W/kg={n2p4}. "
                    f"At 2.4 W/kg: sub-500-kWe close-cells (30 yr) = {len(sub500_close)}",
        "status_short": "see component hypotheses H-9-a through H-9-g",
    }

    out["hypothesis_grading"] = grading

    # Write JSON
    out_path = Path(__file__).parent / "results" / "arch_E_specific_power_sweep.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2, default=str)

    # Print headline
    print("\n=== R-arch-E-specific-power-flown-anchored — RESULTS ===")
    print(f"\nH-9-a equivalence: {grading['H_9_a']['status']} "
          f"({grading['H_9_a']['measured']})")
    print("\nClose-cell counts at 25-yr ceiling (positive-payload only):")
    for name in MASS_MODELS:
        c = closures[name]
        print(f"  {name:25s}: {c['n_close_25yr']:3d}/{c['n_cells_total']:3d} "
              f"(pos-payload {c['n_pos_payload']:3d})")
    print("\nClose-cell counts at 30-yr ceiling:")
    for name in MASS_MODELS:
        c = closures[name]
        print(f"  {name:25s}: {c['n_close_30yr']:3d}/{c['n_cells_total']:3d}")
    print("\nBest cell at 25-yr ceiling per model:")
    for name in MASS_MODELS:
        b = bests[name]["best_at_25yr"]
        if b is None:
            print(f"  {name:25s}: NONE")
        else:
            print(f"  {name:25s}: R={b['reactor_kwe']:.0f} chunk={b['chunk_t']:.0f} "
                  f"Isp={b['isp_s']:.0f} -> RT={b['round_trip_yr']:.2f}yr "
                  f"deliv={b['delivered_t']:.1f}t")
    print("\nHypothesis grading:")
    for k, v in grading.items():
        print(f"  {k}: {v['status'] if 'status' in v else v.get('status_short', '?')}")
        print(f"    measured: {v['measured']}")

    # Joint expected-value table
    print("\nJoint expected value (naive product, posterior × P(NPV+)):")
    print(f"{'model':25s} {'ArchE-corp':>10s} {'ArchE-sov':>10s} "
          f"{'VarB-corp':>10s} {'VarB-sov':>10s}")
    for name in MASS_MODELS:
        j = joint_per_model[name]["joint_naive_product"]
        print(f"{name:25s} {j['arch_E_corp']*100:>9.3f}% {j['arch_E_sov']*100:>9.3f}% "
              f"{j['variant_B_corp']*100:>9.3f}% {j['variant_B_sov']*100:>9.3f}%")
    print(f"\nResults written to {out_path}")


if __name__ == "__main__":
    main()
