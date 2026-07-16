"""R-radiator-mass-penalty — decomposed tug dry mass vs bundled 10 W/kg figure.

Build a power-class-dependent dry mass model:

    m_tug(P_el) = m_fixed + m_reactor(P_el) + m_PC(P_el) + m_radiator(P_el) + m_tank(m_prop)

Compare against the architecture matrix's current bundled formula

    m_tug = 5 t + P_el_kWe × 0.1 t          (10 W/kg total electrical specific power)

and re-derive delivered mass / launch mass / delivered-per-launch for each
(reactor_kWe, chunk_t, mass_model) cell. Headline question: does the megawatt
cell still beat sub-megawatt once the radiator is explicitly counted?
"""

from __future__ import annotations

import json
import math
from pathlib import Path

from waterprop.constants import G0

YEAR_S = 365.25 * 86400.0

# Mission constants (same as R-reactor-specific-power)
DV_TOTAL_KM_S = 6.42
DV_OUTBOUND_KM_S = 9.0
ISP_OUTBOUND_S = 2000.0
ISP_ELEC_S = 2000.0          # representative electric specific impulse for cross-cell comparison
TAU_BURN_MAX_YR = 7.0
ETA_THR = 0.65               # RF ion thruster efficiency at 2000 s
CHEMICAL_KICK_MULTIPLIER = 6.9   # from R-outbound-architecture

# Decomposed-model parameters (three cases)
MASS_MODELS: dict[str, dict] = {
    "bundled_10_W_per_kg": {
        "kind": "bundled",
        "m_fixed_t": 5.0,
        "specific_power_total_w_per_kg": 10.0,
    },
    "decomposed_mid": {
        "kind": "decomposed",
        "m_fixed_t": 3.0,
        "alpha_reactor_W_per_kg": 50.0,        # electrical-equivalent specific power of reactor stack alone
        "alpha_PC_W_per_kg": 200.0,            # power conversion (Brayton at 5 kg/kWe)
        "alpha_radiator_kW_th_per_kg": 2.0,    # 10 kW_th/m² × 5 kg/m² → 0.5 kg/kW_th
        "eta_conv": 0.30,
        "f_tank": 0.05,
    },
    "decomposed_conservative": {
        "kind": "decomposed",
        "m_fixed_t": 3.0,
        "alpha_reactor_W_per_kg": 30.0,
        "alpha_PC_W_per_kg": 100.0,            # Stirling at 10 kg/kWe
        "alpha_radiator_kW_th_per_kg": 1.0,    # 5 kW_th/m² × 5 kg/m² → 1.0 kg/kW_th
        "eta_conv": 0.25,
        "f_tank": 0.05,
    },
    "decomposed_stretch": {
        "kind": "decomposed",
        "m_fixed_t": 3.0,
        "alpha_reactor_W_per_kg": 80.0,
        "alpha_PC_W_per_kg": 200.0,
        "alpha_radiator_kW_th_per_kg": 4.0,    # 20 kW_th/m² × 5 kg/m² → 0.25 kg/kW_th
        "eta_conv": 0.40,
        "f_tank": 0.05,
    },
}

REACTOR_POWERS_KWE = [10.0, 40.0, 100.0, 200.0, 500.0, 1000.0, 2000.0]
CHUNKS_T = [100.0, 200.0, 500.0]


def dry_mass_components_t(model: dict, reactor_kwe: float, m_prop_t: float | None = None) -> dict:
    """Return the dry-mass decomposition (in tonnes) for a given model and reactor power.

    If m_prop_t is not provided, tank mass is left out (caller can iterate).
    """
    if model["kind"] == "bundled":
        # The matrix's current rule: total electrical specific power lumps reactor + PC + radiator.
        m_reactor_stack_t = reactor_kwe / model["specific_power_total_w_per_kg"]
        return {
            "m_fixed_t": model["m_fixed_t"],
            "m_reactor_t": m_reactor_stack_t,         # bundled with PC + radiator
            "m_PC_t": 0.0,
            "m_radiator_t": 0.0,
            "m_tank_t": (m_prop_t or 0.0) * 0.05,
            "m_tug_t": model["m_fixed_t"] + m_reactor_stack_t + (m_prop_t or 0.0) * 0.05,
        }
    # Decomposed
    eta = model["eta_conv"]
    p_th_waste_kw = reactor_kwe * (1.0 - eta) / eta
    m_reactor_t = reactor_kwe / model["alpha_reactor_W_per_kg"]
    m_pc_t = reactor_kwe / model["alpha_PC_W_per_kg"]
    m_rad_t = p_th_waste_kw / model["alpha_radiator_kW_th_per_kg"] / 1000.0
    # NOTE: alpha_radiator is in kW_th/kg; m_rad in kg = p_th_waste_kw / alpha → /1000 to tonnes
    m_tank_t = (m_prop_t or 0.0) * model["f_tank"]
    return {
        "m_fixed_t": model["m_fixed_t"],
        "m_reactor_t": m_reactor_t,
        "m_PC_t": m_pc_t,
        "m_radiator_t": m_rad_t,
        "m_tank_t": m_tank_t,
        "m_tug_t": model["m_fixed_t"] + m_reactor_t + m_pc_t + m_rad_t + m_tank_t,
    }


def all_electric_delivered(model: dict, reactor_kwe: float, chunk_t: float,
                           isp_elec_s: float = ISP_ELEC_S) -> dict:
    """Compute all-electric delivered mass and launch mass under chemical-kick outbound.

    Iteration: tank mass depends on m_prop, m_prop depends on rocket equation, which
    depends on dry mass. Do a quick fixed-point iteration (converges in 2-3 steps).
    """
    v_e = isp_elec_s * G0
    # First pass: ignore tank
    comp = dry_mass_components_t(model, reactor_kwe, m_prop_t=0.0)
    m_v_t = comp["m_tug_t"]
    for _ in range(4):
        m_initial_t = m_v_t + chunk_t
        m_final_t = m_initial_t * math.exp(-DV_TOTAL_KM_S * 1000.0 / v_e)
        if m_final_t < m_v_t:
            return {
                "feasible": False,
                "m_v_t": m_v_t,
                "components": comp,
                "model_name": None,
            }
        m_prop_t = m_initial_t - m_final_t
        comp = dry_mass_components_t(model, reactor_kwe, m_prop_t=m_prop_t)
        new_m_v_t = comp["m_tug_t"]
        if abs(new_m_v_t - m_v_t) < 1e-4:
            m_v_t = new_m_v_t
            break
        m_v_t = new_m_v_t

    delivered_t = m_final_t - m_v_t
    # Outbound: all-electric LEO mass = m_v × exp(dv_out / v_e_out)
    v_e_out = ISP_OUTBOUND_S * G0
    m_leo_allelectric_t = m_v_t * math.exp(DV_OUTBOUND_KM_S * 1000.0 / v_e_out)
    m_leo_chemkick_t = m_leo_allelectric_t * CHEMICAL_KICK_MULTIPLIER
    # Burn time check
    thrust_N = 2.0 * ETA_THR * reactor_kwe * 1000.0 / v_e
    tau_yr = m_prop_t * 1000.0 * v_e / thrust_N / YEAR_S
    return {
        "feasible": True,
        "schedule_feasible_7yr": tau_yr <= TAU_BURN_MAX_YR,
        "m_v_t": m_v_t,
        "components": comp,
        "m_prop_t": m_prop_t,
        "delivered_t": delivered_t,
        "m_LEO_allelectric_outbound_t": m_leo_allelectric_t,
        "m_LEO_chemkick_outbound_t": m_leo_chemkick_t,
        "delivered_per_LEO_allelectric": delivered_t / m_leo_allelectric_t,
        "delivered_per_LEO_chemkick": delivered_t / m_leo_chemkick_t,
        "tau_burn_yr": tau_yr,
        "thrust_N": thrust_N,
    }


def main() -> dict:
    results: dict = {"models": {}, "cells": [], "headline": {}}

    # First: per-model dry-mass table at each reactor class, no chunk dependence (tank=0)
    dry_mass_table = []
    for reactor in REACTOR_POWERS_KWE:
        row = {"reactor_kwe": reactor, "models": {}}
        for name, model in MASS_MODELS.items():
            comp = dry_mass_components_t(model, reactor, m_prop_t=0.0)
            row["models"][name] = comp
        dry_mass_table.append(row)
    results["dry_mass_table"] = dry_mass_table

    # Second: full sweep at fixed 2000 s electric Isp
    for name, model in MASS_MODELS.items():
        for reactor in REACTOR_POWERS_KWE:
            for chunk in CHUNKS_T:
                cell = all_electric_delivered(model, reactor, chunk)
                cell.update({"mass_model": name, "reactor_kwe": reactor, "chunk_t": chunk,
                             "isp_elec_s": ISP_ELEC_S})
                results["cells"].append(cell)

    # Third: pairwise comparison — for each (reactor, chunk), bundled vs decomposed-mid
    pair_compare = []
    cell_idx = {(c["mass_model"], c["reactor_kwe"], c["chunk_t"]): c for c in results["cells"]}
    for reactor in REACTOR_POWERS_KWE:
        for chunk in CHUNKS_T:
            b = cell_idx[("bundled_10_W_per_kg", reactor, chunk)]
            m = cell_idx[("decomposed_mid", reactor, chunk)]
            c = cell_idx[("decomposed_conservative", reactor, chunk)]
            s = cell_idx[("decomposed_stretch", reactor, chunk)]
            if not all(x.get("feasible") for x in (b, m, c, s)):
                pair_compare.append({
                    "reactor_kwe": reactor, "chunk_t": chunk, "feasible": False,
                })
                continue
            pair_compare.append({
                "reactor_kwe": reactor,
                "chunk_t": chunk,
                "feasible": True,
                "m_v_t_bundled": b["m_v_t"],
                "m_v_t_mid": m["m_v_t"],
                "m_v_t_conservative": c["m_v_t"],
                "m_v_t_stretch": s["m_v_t"],
                "delivered_bundled_t": b["delivered_t"],
                "delivered_mid_t": m["delivered_t"],
                "delivered_conservative_t": c["delivered_t"],
                "delivered_stretch_t": s["delivered_t"],
                "ratio_bundled": b["delivered_per_LEO_chemkick"],
                "ratio_mid": m["delivered_per_LEO_chemkick"],
                "ratio_conservative": c["delivered_per_LEO_chemkick"],
                "ratio_stretch": s["delivered_per_LEO_chemkick"],
                "degradation_mid_pct": (1 - m["delivered_per_LEO_chemkick"] / b["delivered_per_LEO_chemkick"]) * 100.0,
                "degradation_conservative_pct": (1 - c["delivered_per_LEO_chemkick"] / b["delivered_per_LEO_chemkick"]) * 100.0,
            })
    results["pair_compare"] = pair_compare

    # Fourth: for each mass model, find the optimum reactor power at each chunk size
    # under the 7-year inbound burn-time constraint (consistent with rest of matrix).
    optima = []
    for name in MASS_MODELS.keys():
        for chunk in CHUNKS_T:
            entries = [c for c in results["cells"]
                       if c["mass_model"] == name and c["chunk_t"] == chunk and c.get("feasible")]
            schedule_ok = [c for c in entries if c.get("schedule_feasible_7yr")]
            if not entries:
                continue
            peak = max(entries, key=lambda x: x["delivered_per_LEO_chemkick"])
            peak_ok = max(schedule_ok, key=lambda x: x["delivered_per_LEO_chemkick"]) if schedule_ok else None
            optima.append({
                "mass_model": name,
                "chunk_t": chunk,
                "peak_reactor_kwe_unconstrained": peak["reactor_kwe"],
                "peak_ratio_unconstrained": peak["delivered_per_LEO_chemkick"],
                "peak_reactor_kwe_7yr": peak_ok["reactor_kwe"] if peak_ok else None,
                "peak_ratio_7yr": peak_ok["delivered_per_LEO_chemkick"] if peak_ok else None,
                "peak_m_v_t_7yr": peak_ok["m_v_t"] if peak_ok else None,
                "peak_tau_burn_yr_7yr": peak_ok["tau_burn_yr"] if peak_ok else None,
            })
    results["optima"] = optima

    # Hypothesis grading
    # H-rmp-a: 1 MWe tug dry mass at decomposed-mid (chunk-independent component, no tank)
    mid_1mwe = next(r["models"]["decomposed_mid"] for r in dry_mass_table if r["reactor_kwe"] == 1000.0)
    bundled_1mwe = next(r["models"]["bundled_10_W_per_kg"] for r in dry_mass_table if r["reactor_kwe"] == 1000.0)

    # H-rmp-b: megawatt-cell delivered-fraction degradation, decomposed-mid vs bundled, at 500 t chunk
    mw500 = next(p for p in pair_compare if p["reactor_kwe"] == 1000.0 and p["chunk_t"] == 500.0)

    # H-rmp-c: where does the optimum sit?
    # H-rmp-d: Kilopower cell: 10 kWe at 100 t chunk
    kp100 = next(p for p in pair_compare if p["reactor_kwe"] == 10.0 and p["chunk_t"] == 100.0)

    results["headline"] = {
        "H_rmp_a_mwe_tug_dry_mass_bundled_t": bundled_1mwe["m_tug_t"],
        "H_rmp_a_mwe_tug_dry_mass_decomposed_mid_t": mid_1mwe["m_tug_t"],
        "H_rmp_a_predicted_band_t": [50.0, 120.0],
        "H_rmp_a_held": 50.0 <= mid_1mwe["m_tug_t"] <= 120.0,
        "H_rmp_b_mw_500t_degradation_pct": mw500["degradation_mid_pct"] if mw500.get("feasible") else None,
        "H_rmp_b_predicted_band_pct": [15.0, 40.0],
        "H_rmp_b_held": (
            mw500.get("feasible")
            and 15.0 <= mw500["degradation_mid_pct"] <= 40.0
        ),
        "H_rmp_c_optimum_kwe_decomposed_mid_unconstrained": {
            f"chunk_{int(o['chunk_t'])}_t": o["peak_reactor_kwe_unconstrained"]
            for o in optima if o["mass_model"] == "decomposed_mid"
        },
        "H_rmp_c_optimum_kwe_bundled_unconstrained": {
            f"chunk_{int(o['chunk_t'])}_t": o["peak_reactor_kwe_unconstrained"]
            for o in optima if o["mass_model"] == "bundled_10_W_per_kg"
        },
        "H_rmp_c_optimum_kwe_decomposed_mid_7yr": {
            f"chunk_{int(o['chunk_t'])}_t": o["peak_reactor_kwe_7yr"]
            for o in optima if o["mass_model"] == "decomposed_mid"
        },
        "H_rmp_c_optimum_kwe_bundled_7yr": {
            f"chunk_{int(o['chunk_t'])}_t": o["peak_reactor_kwe_7yr"]
            for o in optima if o["mass_model"] == "bundled_10_W_per_kg"
        },
        "H_rmp_d_kilopower_degradation_pct": kp100["degradation_mid_pct"] if kp100.get("feasible") else None,
        "H_rmp_d_held": (
            kp100.get("feasible")
            and abs(kp100["degradation_mid_pct"]) <= 5.0
        ),
    }

    results_dir = Path(__file__).parent / "results"
    results_dir.mkdir(exist_ok=True)
    (results_dir / "radiator_penalty.json").write_text(json.dumps(results, indent=2, default=str))

    # Markdown tables
    lines = []
    lines.append("### Dry-mass decomposition by reactor class and mass model (no chunk, no tank)\n")
    lines.append("Tug dry mass in tonnes. Bundled = matrix's current 10 W/kg formula. Decomposed splits m_fixed / m_reactor / m_PC / m_radiator and sums.\n")
    lines.append("| Reactor (kWe) | Bundled 10 W/kg (t) | Decomposed mid (t) | Decomposed conservative (t) | Decomposed stretch (t) |")
    lines.append("|---:|---:|---:|---:|---:|")
    for r in dry_mass_table:
        lines.append(
            f"| {r['reactor_kwe']:.0f} | "
            f"{r['models']['bundled_10_W_per_kg']['m_tug_t']:.1f} | "
            f"{r['models']['decomposed_mid']['m_tug_t']:.1f} | "
            f"{r['models']['decomposed_conservative']['m_tug_t']:.1f} | "
            f"{r['models']['decomposed_stretch']['m_tug_t']:.1f} |"
        )

    lines.append("\n### Decomposed-mid breakdown by component at each reactor class\n")
    lines.append("| Reactor (kWe) | m_fixed (t) | m_reactor (t) | m_PC (t) | m_radiator (t) | Total tug dry (t) |")
    lines.append("|---:|---:|---:|---:|---:|---:|")
    for r in dry_mass_table:
        c = r["models"]["decomposed_mid"]
        lines.append(
            f"| {r['reactor_kwe']:.0f} | "
            f"{c['m_fixed_t']:.1f} | {c['m_reactor_t']:.1f} | {c['m_PC_t']:.1f} | "
            f"{c['m_radiator_t']:.2f} | {c['m_tug_t']:.1f} |"
        )

    lines.append("\n### Delivered mass and launch mass at 500 t chunk, all mass models, 2000 s electric Isp\n")
    lines.append("Launch mass under chemical-kick outbound (matrix's headline outbound architecture).\n")
    lines.append("| Reactor (kWe) | Model | M_v (t) | Delivered (t) | M_LEO chemkick (t) | Delivered/M_LEO | Burn time (yr) |")
    lines.append("|---:|---|---:|---:|---:|---:|---:|")
    for reactor in REACTOR_POWERS_KWE:
        for name in MASS_MODELS.keys():
            c = cell_idx.get((name, reactor, 500.0))
            if not c or not c.get("feasible"):
                lines.append(f"| {reactor:.0f} | {name} | — | — | — | — | — |")
                continue
            lines.append(
                f"| {reactor:.0f} | {name} | "
                f"{c['m_v_t']:.1f} | {c['delivered_t']:.1f} | "
                f"{c['m_LEO_chemkick_outbound_t']:.1f} | "
                f"{c['delivered_per_LEO_chemkick']:.3f} | "
                f"{c['tau_burn_yr']:.2f} |"
            )

    lines.append("\n### Pairwise degradation: decomposed-mid vs bundled-10-W/kg\n")
    lines.append("Percentage drop in delivered-per-launch-mass when the radiator is explicitly counted.\n")
    lines.append("| Reactor (kWe) | 100 t chunk | 200 t chunk | 500 t chunk |")
    lines.append("|---:|---:|---:|---:|")
    for reactor in REACTOR_POWERS_KWE:
        cells = {p["chunk_t"]: p for p in pair_compare
                 if p["reactor_kwe"] == reactor}
        row = [f"{reactor:.0f}"]
        for chunk in CHUNKS_T:
            cell = cells.get(chunk)
            if cell and cell.get("feasible"):
                row.append(f"{cell['degradation_mid_pct']:+.1f}%")
            else:
                row.append("—")
        lines.append("| " + " | ".join(row) + " |")

    lines.append("\n### Optimum reactor power under each mass model — 7-year burn-cap-constrained\n")
    lines.append("Optimum = peak delivered-per-launch-mass at chemical-kick outbound, 2000 s electric Isp, subject to inbound burn time ≤ 7 yr.\n")
    lines.append("| Mass model | 100 t chunk | 200 t chunk | 500 t chunk |")
    lines.append("|---|---:|---:|---:|")
    for name in MASS_MODELS.keys():
        opt_for_chunk = {o["chunk_t"]: o for o in optima if o["mass_model"] == name}
        row = [name]
        for chunk in CHUNKS_T:
            o = opt_for_chunk.get(chunk)
            if o and o.get("peak_reactor_kwe_7yr") is not None:
                row.append(f"{o['peak_reactor_kwe_7yr']:.0f} kWe @ {o['peak_ratio_7yr']:.3f}")
            else:
                row.append("—")
        lines.append("| " + " | ".join(row) + " |")

    lines.append("\n### Optimum reactor power — burn-time-unconstrained (rocket-equation-only view)\n")
    lines.append("Same metric, no burn-cap. Low reactor power always wins on raw ratio because smaller vehicle → smaller mass ratio penalty; this is why the matrix uses burn-time-constrained optima.\n")
    lines.append("| Mass model | 100 t chunk | 200 t chunk | 500 t chunk |")
    lines.append("|---|---:|---:|---:|")
    for name in MASS_MODELS.keys():
        opt_for_chunk = {o["chunk_t"]: o for o in optima if o["mass_model"] == name}
        row = [name]
        for chunk in CHUNKS_T:
            o = opt_for_chunk.get(chunk)
            if o:
                row.append(f"{o['peak_reactor_kwe_unconstrained']:.0f} kWe @ {o['peak_ratio_unconstrained']:.3f}")
            else:
                row.append("—")
        lines.append("| " + " | ".join(row) + " |")

    lines.append("\n### Hypothesis grading\n")
    h = results["headline"]
    lines.append("| Sub-claim | Predicted | Actual | Held? |")
    lines.append("|---|---|---|---|")
    lines.append(f"| H-rmp-a — 1 MWe tug dry mass (decomposed-mid, no tank) | 50–120 t | {h['H_rmp_a_mwe_tug_dry_mass_decomposed_mid_t']:.1f} t | {'yes' if h['H_rmp_a_held'] else '**no**'} |")
    deg_b = h['H_rmp_b_mw_500t_degradation_pct']
    deg_b_str = f"{deg_b:+.1f}%" if deg_b is not None else "n/a"
    lines.append(f"| H-rmp-b — Megawatt cell delivered-ratio degradation (500 t chunk, decomposed-mid vs bundled) | 15–40% | {deg_b_str} | {'yes' if h['H_rmp_b_held'] else '**no**'} |")
    opt_bundled = h['H_rmp_c_optimum_kwe_bundled_7yr'].get('chunk_500_t', 'n/a')
    opt_mid = h['H_rmp_c_optimum_kwe_decomposed_mid_7yr'].get('chunk_500_t', 'n/a')
    lines.append(f"| H-rmp-c — Optimum reactor power (500 t chunk, 7-yr cap) | shift from 1000 kWe → 200–500 kWe | bundled {opt_bundled} kWe → decomposed-mid {opt_mid} kWe | (read below) |")
    deg_d = h['H_rmp_d_kilopower_degradation_pct']
    deg_d_str = f"{deg_d:+.1f}%" if deg_d is not None else "n/a"
    lines.append(f"| H-rmp-d — Kilopower (10 kWe, 100 t chunk) within ±5% | within 5% | {deg_d_str} | {'yes' if h['H_rmp_d_held'] else '**no**'} |")

    (results_dir / "tables.md").write_text("\n".join(lines))
    return results


if __name__ == "__main__":
    out = main()
    h = out["headline"]
    print("R-radiator-mass-penalty complete.")
    print(f"  Bundled 10 W/kg @ 1 MWe: tug dry = {h['H_rmp_a_mwe_tug_dry_mass_bundled_t']:.1f} t")
    print(f"  Decomposed-mid @ 1 MWe : tug dry = {h['H_rmp_a_mwe_tug_dry_mass_decomposed_mid_t']:.1f} t")
    deg = h.get("H_rmp_b_mw_500t_degradation_pct")
    print(f"  Megawatt cell (500 t chunk) delivered/launch degradation: {deg:+.1f}%" if deg is not None else "  (megawatt cell infeasible)")
    print(f"  Optimum reactor power (7-yr burn cap):")
    print(f"    bundled:        {h['H_rmp_c_optimum_kwe_bundled_7yr']}")
    print(f"    decomposed-mid: {h['H_rmp_c_optimum_kwe_decomposed_mid_7yr']}")
    print(f"  Kilopower degradation: {h['H_rmp_d_kilopower_degradation_pct']:+.2f}% (held: {h['H_rmp_d_held']})")
