"""R-chunk-fed-chemical — Variant B (chunk-water as chemical propellant via on-site electrolysis).

Compare three architectures on delivered-water-per-launch-mass:
  - All-electric (R-design-envelope baseline)
  - Carried-hypergolic two-stage (R-two-stage-dv baseline)
  - Variant B: chunk-fed chemical at Saturn (electrolyze chunk water for chemical burn)

Pure algebra. No integrator. Same constant-thrust approximation as R6/R10/R10b.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

from waterprop.constants import G0

YEAR_S = 365.25 * 86400.0

DV_TOTAL_KM_S = 6.42
DV_OUTBOUND_KM_S = 9.0
ISP_OUTBOUND_S = 2000.0
ISP_HYDROLOX_S = 450.0
ISP_HYPERGOLIC_S = 320.0
TAU_BURN_MAX_YR = 7.0
SPECIFIC_POWER_W_PER_KG = 10.0
M_TUG_KG = 5000.0
M_CHEM_DRY_KG = 10000.0

ETA_THR = {
    "Hall":     0.55,
    "RF_ion":   0.65,
    "dual_ion": 0.55,
}

REACTOR_POWERS_KWE = [10.0, 40.0, 100.0, 200.0, 500.0, 1000.0]
CHUNKS_T          = [50.0, 100.0, 200.0, 500.0]
DV_CHEM_KM_S      = [0.0, 1.0, 2.0, 3.0]
ELECTRIC_ISP_S    = [1500.0, 2000.0, 2934.0, 5000.0]


def thruster_class_for_isp(isp_s: float) -> tuple[str, float]:
    if isp_s <= 1800.0:  return "Hall",     ETA_THR["Hall"]
    if isp_s <= 3000.0:  return "RF_ion",   ETA_THR["RF_ion"]
    return                       "dual_ion", ETA_THR["dual_ion"]


def vehicle_dry_kg(reactor_kwe: float) -> float:
    reactor_kg = reactor_kwe * 1000.0 / SPECIFIC_POWER_W_PER_KG
    return M_TUG_KG + reactor_kg


def outbound_LEO_mass_t(mass_at_saturn_t: float) -> float:
    """Mass at LEO required to deliver mass_at_saturn_t to Saturn arrival via all-electric outbound."""
    v_e = ISP_OUTBOUND_S * G0
    return mass_at_saturn_t * math.exp(DV_OUTBOUND_KM_S * 1000.0 / v_e)


def variant_b(reactor_kwe: float, chunk_t: float, dv_chem_km_s: float, isp_elec_s: float) -> dict:
    """Variant B: chemical Saturn-depart on electrolyzed chunk water; electric inbound on remaining chunk."""
    dv_elec_km_s = DV_TOTAL_KM_S - dv_chem_km_s
    if dv_elec_km_s <= 0:
        return {"feasible": False, "reason": "non-positive electric dv"}

    M_v_t = vehicle_dry_kg(reactor_kwe) / 1000.0
    M_initial_t = M_v_t + M_CHEM_DRY_KG / 1000.0 + chunk_t

    v_e_chem = ISP_HYDROLOX_S * G0
    M_after_chem_t = M_initial_t * math.exp(-dv_chem_km_s * 1000.0 / v_e_chem)
    chunk_consumed_chem_t = M_initial_t - M_after_chem_t  # all of it comes from chunk water
    if chunk_consumed_chem_t > chunk_t:
        return {"feasible": False, "reason": "chemical burn would consume more than chunk inventory"}

    chunk_remaining_after_chem = chunk_t - chunk_consumed_chem_t
    M_after_jettison_t = M_after_chem_t - M_CHEM_DRY_KG / 1000.0

    v_e_elec = isp_elec_s * G0
    M_after_elec_t = M_after_jettison_t * math.exp(-dv_elec_km_s * 1000.0 / v_e_elec)
    if M_after_elec_t < M_v_t:
        return {"feasible": False, "reason": "electric burn consumes vehicle dry mass"}

    delivered_water_t = M_after_elec_t - M_v_t
    m_prop_elec_t = M_after_jettison_t - M_after_elec_t

    thr_class, eta_thr = thruster_class_for_isp(isp_elec_s)
    p_jet_w = (M_initial_t * 0.0)  # placeholder; computed via thrust below
    # Burn time: thrust = m_prop * v_e / tau; so tau = m_prop * v_e / thrust;
    # thrust = 2 * eta_thr * P_e / v_e -> tau = m_prop * v_e^2 / (2 * eta_thr * P_e)
    P_elec_w = reactor_kwe * 1000.0
    thrust_N = 2.0 * eta_thr * P_elec_w / v_e_elec
    tau_burn_yr = m_prop_elec_t * 1000.0 * v_e_elec / thrust_N / YEAR_S

    schedule_feasible = tau_burn_yr <= TAU_BURN_MAX_YR

    M_at_saturn_t = M_v_t + M_CHEM_DRY_KG / 1000.0
    M_LEO_t = outbound_LEO_mass_t(M_at_saturn_t)

    return {
        "feasible": True,
        "schedule_feasible": schedule_feasible,
        "architecture": "variant_b",
        "M_v_t": M_v_t,
        "M_LEO_t": M_LEO_t,
        "delivered_water_t": delivered_water_t,
        "chunk_consumed_chem_t": chunk_consumed_chem_t,
        "m_prop_elec_t": m_prop_elec_t,
        "tau_burn_yr": tau_burn_yr,
        "delivered_per_LEO": delivered_water_t / M_LEO_t,
        "thr_class": thr_class,
    }


def all_electric(reactor_kwe: float, chunk_t: float, isp_elec_s: float) -> dict:
    """All-electric single-stage inbound at chosen specific impulse."""
    M_v_t = vehicle_dry_kg(reactor_kwe) / 1000.0
    M_initial_t = M_v_t + chunk_t

    v_e_elec = isp_elec_s * G0
    M_final_t = M_initial_t * math.exp(-DV_TOTAL_KM_S * 1000.0 / v_e_elec)
    if M_final_t < M_v_t:
        return {"feasible": False, "reason": "electric burn consumes vehicle dry mass"}

    delivered_water_t = M_final_t - M_v_t
    m_prop_elec_t = M_initial_t - M_final_t

    thr_class, eta_thr = thruster_class_for_isp(isp_elec_s)
    P_elec_w = reactor_kwe * 1000.0
    thrust_N = 2.0 * eta_thr * P_elec_w / v_e_elec
    tau_burn_yr = m_prop_elec_t * 1000.0 * v_e_elec / thrust_N / YEAR_S
    schedule_feasible = tau_burn_yr <= TAU_BURN_MAX_YR

    M_LEO_t = outbound_LEO_mass_t(M_v_t)

    return {
        "feasible": True,
        "schedule_feasible": schedule_feasible,
        "architecture": "all_electric",
        "M_v_t": M_v_t,
        "M_LEO_t": M_LEO_t,
        "delivered_water_t": delivered_water_t,
        "m_prop_elec_t": m_prop_elec_t,
        "tau_burn_yr": tau_burn_yr,
        "delivered_per_LEO": delivered_water_t / M_LEO_t,
        "thr_class": thr_class,
    }


def carried_hypergolic(reactor_kwe: float, chunk_t: float, dv_chem_km_s: float, isp_elec_s: float) -> dict:
    """Carried-hypergolic two-stage: chem prop launched from Earth, chem burn at Saturn-depart, electric inbound."""
    dv_elec_km_s = DV_TOTAL_KM_S - dv_chem_km_s
    if dv_elec_km_s <= 0:
        return {"feasible": False, "reason": "non-positive electric dv"}

    M_v_t = vehicle_dry_kg(reactor_kwe) / 1000.0
    v_e_chem = ISP_HYPERGOLIC_S * G0

    # Chemical propellant carried (rocket equation, post-burn mass = M_v + chunk + M_chem_dry)
    M_after_chem_t = M_v_t + chunk_t + M_CHEM_DRY_KG / 1000.0
    M_before_chem_t = M_after_chem_t * math.exp(dv_chem_km_s * 1000.0 / v_e_chem)
    M_chem_prop_t = M_before_chem_t - M_after_chem_t

    # Drop chemical stage dry mass after burn
    M_after_jettison_t = M_after_chem_t - M_CHEM_DRY_KG / 1000.0  # = M_v + chunk

    v_e_elec = isp_elec_s * G0
    M_after_elec_t = M_after_jettison_t * math.exp(-dv_elec_km_s * 1000.0 / v_e_elec)
    if M_after_elec_t < M_v_t:
        return {"feasible": False, "reason": "electric burn consumes vehicle dry mass"}

    delivered_water_t = M_after_elec_t - M_v_t
    m_prop_elec_t = M_after_jettison_t - M_after_elec_t

    thr_class, eta_thr = thruster_class_for_isp(isp_elec_s)
    P_elec_w = reactor_kwe * 1000.0
    thrust_N = 2.0 * eta_thr * P_elec_w / v_e_elec
    tau_burn_yr = m_prop_elec_t * 1000.0 * v_e_elec / thrust_N / YEAR_S
    schedule_feasible = tau_burn_yr <= TAU_BURN_MAX_YR

    # Outbound: must deliver M_v + M_chem_dry + M_chem_prop to Saturn
    M_at_saturn_t = M_v_t + M_CHEM_DRY_KG / 1000.0 + M_chem_prop_t
    M_LEO_t = outbound_LEO_mass_t(M_at_saturn_t)

    return {
        "feasible": True,
        "schedule_feasible": schedule_feasible,
        "architecture": "carried_hypergolic",
        "M_v_t": M_v_t,
        "M_chem_prop_t": M_chem_prop_t,
        "M_LEO_t": M_LEO_t,
        "delivered_water_t": delivered_water_t,
        "m_prop_elec_t": m_prop_elec_t,
        "tau_burn_yr": tau_burn_yr,
        "delivered_per_LEO": delivered_water_t / M_LEO_t,
        "thr_class": thr_class,
    }


def best_per_cell(reactor_kwe: float, chunk_t: float, isp_elec_s: float) -> dict:
    """Find the best of {all-electric, all Variant B dv_chem options, all carried-hypergolic dv_chem options}
    by delivered_per_LEO, requiring schedule_feasible."""
    candidates = []
    ae = all_electric(reactor_kwe, chunk_t, isp_elec_s)
    if ae.get("feasible") and ae.get("schedule_feasible"):
        ae["dv_chem_km_s"] = 0.0
        candidates.append(ae)
    for dv_chem in DV_CHEM_KM_S:
        if dv_chem == 0.0:
            continue
        vb = variant_b(reactor_kwe, chunk_t, dv_chem, isp_elec_s)
        if vb.get("feasible") and vb.get("schedule_feasible"):
            vb["dv_chem_km_s"] = dv_chem
            candidates.append(vb)
        ch = carried_hypergolic(reactor_kwe, chunk_t, dv_chem, isp_elec_s)
        if ch.get("feasible") and ch.get("schedule_feasible"):
            ch["dv_chem_km_s"] = dv_chem
            candidates.append(ch)
    if not candidates:
        return {"feasible": False, "reason": "no schedule-feasible architecture"}
    best = max(candidates, key=lambda c: c["delivered_per_LEO"])
    return best


def main() -> dict:
    cells = []
    winner_by_cell = {}
    for reactor_kwe in REACTOR_POWERS_KWE:
        for chunk_t in CHUNKS_T:
            for isp_elec in ELECTRIC_ISP_S:
                # Compute all three architectures at all dv_chem options
                row = {
                    "reactor_kwe": reactor_kwe,
                    "chunk_t": chunk_t,
                    "isp_elec_s": isp_elec,
                    "all_electric": all_electric(reactor_kwe, chunk_t, isp_elec),
                }
                for dv_chem in DV_CHEM_KM_S:
                    if dv_chem == 0.0:
                        continue
                    row[f"variant_b_dv{dv_chem}"] = variant_b(reactor_kwe, chunk_t, dv_chem, isp_elec)
                    row[f"carried_hyp_dv{dv_chem}"] = carried_hypergolic(reactor_kwe, chunk_t, dv_chem, isp_elec)
                cells.append(row)

                best = best_per_cell(reactor_kwe, chunk_t, isp_elec)
                winner_by_cell[(reactor_kwe, chunk_t, isp_elec)] = best

    # Headline: for each (reactor, chunk) at the best electric Isp, what wins?
    headline = []
    for reactor_kwe in REACTOR_POWERS_KWE:
        for chunk_t in CHUNKS_T:
            best_overall = None
            for isp_elec in ELECTRIC_ISP_S:
                cand = winner_by_cell[(reactor_kwe, chunk_t, isp_elec)]
                if not cand.get("feasible"):
                    continue
                if best_overall is None or cand["delivered_per_LEO"] > best_overall["delivered_per_LEO"]:
                    best_overall = {**cand, "isp_elec_s": isp_elec}
            if best_overall is not None:
                best_overall["reactor_kwe"] = reactor_kwe
                best_overall["chunk_t"] = chunk_t
                headline.append(best_overall)
            else:
                headline.append({
                    "reactor_kwe": reactor_kwe,
                    "chunk_t": chunk_t,
                    "feasible": False,
                })

    out = {
        "axes": {
            "reactor_kwe": REACTOR_POWERS_KWE,
            "chunk_t": CHUNKS_T,
            "dv_chem_km_s": DV_CHEM_KM_S,
            "isp_elec_s": ELECTRIC_ISP_S,
            "dv_total_km_s": DV_TOTAL_KM_S,
            "dv_outbound_km_s": DV_OUTBOUND_KM_S,
        },
        "constants": {
            "specific_power_w_per_kg": SPECIFIC_POWER_W_PER_KG,
            "m_tug_kg": M_TUG_KG,
            "m_chem_dry_kg": M_CHEM_DRY_KG,
            "tau_burn_max_yr": TAU_BURN_MAX_YR,
        },
        "all_cells": cells,
        "headline": headline,
    }
    results_dir = Path(__file__).parent / "results"
    results_dir.mkdir(exist_ok=True)
    (results_dir / "chunk_fed_chemical.json").write_text(json.dumps(out, indent=2, default=str))

    # Markdown tables
    lines = []
    lines.append("### Winning architecture by (reactor power × chunk mass)\n")
    lines.append("For each cell, the architecture (and Δv_chem) that maximizes delivered_water / launch_mass at any feasible electric specific impulse. \"-\" means no architecture closes the 7-year inbound burn time.\n")
    header = "| Reactor (kWe) |" + "".join(f" {int(c)} t |" for c in CHUNKS_T)
    lines.append(header)
    lines.append("|---:|" + "---:|" * len(CHUNKS_T))
    for reactor_kwe in REACTOR_POWERS_KWE:
        row_cells = [f"{reactor_kwe:.0f}"]
        for chunk_t in CHUNKS_T:
            h = next(
                (h for h in headline if h["reactor_kwe"] == reactor_kwe and h["chunk_t"] == chunk_t),
                None,
            )
            if h is None or not h.get("feasible"):
                row_cells.append("-")
            else:
                arch = h["architecture"]
                dpl = h["delivered_per_LEO"]
                dv = h.get("dv_chem_km_s", 0.0)
                isp = h["isp_elec_s"]
                row_cells.append(f"{arch} dv_c{dv:.0f} Isp{isp:.0f} ({dpl:.2f})")
        lines.append("| " + " | ".join(row_cells) + " |")

    lines.append("\nFormat: `architecture` + `dv_chem (km/s)` + `electric Isp (s)` + `(delivered/LEO ratio)`. Higher delivered/LEO is better.\n")

    lines.append("\n### Delivered water (t) by best architecture per cell\n")
    lines.append(header)
    lines.append("|---:|" + "---:|" * len(CHUNKS_T))
    for reactor_kwe in REACTOR_POWERS_KWE:
        row_cells = [f"{reactor_kwe:.0f}"]
        for chunk_t in CHUNKS_T:
            h = next(
                (h for h in headline if h["reactor_kwe"] == reactor_kwe and h["chunk_t"] == chunk_t),
                None,
            )
            if h is None or not h.get("feasible"):
                row_cells.append("-")
            else:
                row_cells.append(f"{h['delivered_water_t']:.1f}")
        lines.append("| " + " | ".join(row_cells) + " |")

    lines.append("\n### Launch mass to low Earth orbit (t) by best architecture per cell\n")
    lines.append(header)
    lines.append("|---:|" + "---:|" * len(CHUNKS_T))
    for reactor_kwe in REACTOR_POWERS_KWE:
        row_cells = [f"{reactor_kwe:.0f}"]
        for chunk_t in CHUNKS_T:
            h = next(
                (h for h in headline if h["reactor_kwe"] == reactor_kwe and h["chunk_t"] == chunk_t),
                None,
            )
            if h is None or not h.get("feasible"):
                row_cells.append("-")
            else:
                row_cells.append(f"{h['M_LEO_t']:.0f}")
        lines.append("| " + " | ".join(row_cells) + " |")

    lines.append("\n### Variant B vs all-electric vs carried-hypergolic at 100 t chunk, sweep reactor\n")
    lines.append("All at electric specific impulse 2000 s (water radio-frequency ion class). Δv_chem = 1 km/s for two-stage variants.\n")
    lines.append("| Reactor (kWe) | All-electric delivered (t) | Variant B delivered (t) | Carried-hyp delivered (t) | A/E LEO (t) | VB LEO (t) | CH LEO (t) | A/E ratio | VB ratio | CH ratio |")
    lines.append("|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for reactor_kwe in REACTOR_POWERS_KWE:
        ae = all_electric(reactor_kwe, 100.0, 2000.0)
        vb = variant_b(reactor_kwe, 100.0, 1.0, 2000.0)
        ch = carried_hypergolic(reactor_kwe, 100.0, 1.0, 2000.0)
        def fmt_arch(a):
            if not a.get("feasible"):
                return ("-", "-", "-")
            sched = "" if a.get("schedule_feasible") else " (slow)"
            return (
                f"{a['delivered_water_t']:.1f}{sched}",
                f"{a['M_LEO_t']:.0f}",
                f"{a['delivered_per_LEO']:.2f}",
            )
        ae_d, ae_l, ae_r = fmt_arch(ae)
        vb_d, vb_l, vb_r = fmt_arch(vb)
        ch_d, ch_l, ch_r = fmt_arch(ch)
        lines.append(
            f"| {reactor_kwe:.0f} | {ae_d} | {vb_d} | {ch_d} | "
            f"{ae_l} | {vb_l} | {ch_l} | {ae_r} | {vb_r} | {ch_r} |"
        )

    (results_dir / "tables.md").write_text("\n".join(lines))
    return out


if __name__ == "__main__":
    out = main()
    print(f"Sweep complete. {len(out['all_cells'])} cells.")
    print(f"  Wrote results/chunk_fed_chemical.json and results/tables.md")
