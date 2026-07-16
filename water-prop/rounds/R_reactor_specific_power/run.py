"""R-reactor-specific-power — does higher reactor W/kg flip the FSP-vs-megawatt trade?

Sweep reactor specific power across {5, 10, 20, 40} W/kg. For each
(specific_power, reactor_power, chunk) cell, find the best of {all-electric,
Variant B at any dv_chem} architecture by delivered-water-per-launch-mass.

Pure algebra. Reuses R-chunk-fed-chemical mass accounting.
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
TAU_BURN_MAX_YR = 7.0
M_TUG_KG = 5000.0
M_CHEM_DRY_KG = 10000.0

ETA_THR = {"Hall": 0.55, "RF_ion": 0.65, "dual_ion": 0.55}

SPECIFIC_POWERS = [5.0, 10.0, 20.0, 40.0]
REACTOR_POWERS_KWE = [10.0, 40.0, 100.0, 200.0, 500.0, 1000.0, 2000.0]
CHUNKS_T = [100.0, 200.0, 500.0]
DV_CHEM_OPTIONS = [0.0, 1.0, 2.0, 3.0]
ELECTRIC_ISPS = [1500.0, 2000.0, 2934.0, 5000.0]


def thruster_class_for_isp(isp_s: float) -> tuple[str, float]:
    if isp_s <= 1800.0:  return "Hall", ETA_THR["Hall"]
    if isp_s <= 3000.0:  return "RF_ion", ETA_THR["RF_ion"]
    return                       "dual_ion", ETA_THR["dual_ion"]


def vehicle_dry_t(reactor_kwe: float, specific_power_w_per_kg: float) -> float:
    return (M_TUG_KG + reactor_kwe * 1000.0 / specific_power_w_per_kg) / 1000.0


def outbound_LEO_t(mass_at_saturn_t: float) -> float:
    v_e = ISP_OUTBOUND_S * G0
    return mass_at_saturn_t * math.exp(DV_OUTBOUND_KM_S * 1000.0 / v_e)


def all_electric(reactor_kwe: float, chunk_t: float, isp_elec_s: float, specific_power_w_per_kg: float) -> dict:
    M_v_t = vehicle_dry_t(reactor_kwe, specific_power_w_per_kg)
    M_initial_t = M_v_t + chunk_t
    v_e = isp_elec_s * G0
    M_final_t = M_initial_t * math.exp(-DV_TOTAL_KM_S * 1000.0 / v_e)
    if M_final_t < M_v_t:
        return {"feasible": False}
    delivered_t = M_final_t - M_v_t
    m_prop_t = M_initial_t - M_final_t
    _, eta_thr = thruster_class_for_isp(isp_elec_s)
    thrust_N = 2.0 * eta_thr * reactor_kwe * 1000.0 / v_e
    tau_yr = m_prop_t * 1000.0 * v_e / thrust_N / YEAR_S
    M_LEO_t = outbound_LEO_t(M_v_t)
    return {
        "feasible": True,
        "schedule_feasible": tau_yr <= TAU_BURN_MAX_YR,
        "architecture": "all_electric",
        "dv_chem_km_s": 0.0,
        "isp_elec_s": isp_elec_s,
        "delivered_water_t": delivered_t,
        "M_LEO_t": M_LEO_t,
        "tau_burn_yr": tau_yr,
        "M_v_t": M_v_t,
        "delivered_per_LEO": delivered_t / M_LEO_t,
    }


def variant_b(reactor_kwe: float, chunk_t: float, dv_chem_km_s: float, isp_elec_s: float, specific_power_w_per_kg: float) -> dict:
    dv_elec_km_s = DV_TOTAL_KM_S - dv_chem_km_s
    if dv_elec_km_s <= 0:
        return {"feasible": False}
    M_v_t = vehicle_dry_t(reactor_kwe, specific_power_w_per_kg)
    M_initial_t = M_v_t + M_CHEM_DRY_KG / 1000.0 + chunk_t
    v_e_chem = ISP_HYDROLOX_S * G0
    M_after_chem_t = M_initial_t * math.exp(-dv_chem_km_s * 1000.0 / v_e_chem)
    chunk_consumed_t = M_initial_t - M_after_chem_t
    if chunk_consumed_t > chunk_t:
        return {"feasible": False}
    M_after_jettison_t = M_after_chem_t - M_CHEM_DRY_KG / 1000.0
    v_e_elec = isp_elec_s * G0
    M_final_t = M_after_jettison_t * math.exp(-dv_elec_km_s * 1000.0 / v_e_elec)
    if M_final_t < M_v_t:
        return {"feasible": False}
    delivered_t = M_final_t - M_v_t
    m_prop_elec_t = M_after_jettison_t - M_final_t
    _, eta_thr = thruster_class_for_isp(isp_elec_s)
    thrust_N = 2.0 * eta_thr * reactor_kwe * 1000.0 / v_e_elec
    tau_yr = m_prop_elec_t * 1000.0 * v_e_elec / thrust_N / YEAR_S
    M_at_saturn_t = M_v_t + M_CHEM_DRY_KG / 1000.0
    M_LEO_t = outbound_LEO_t(M_at_saturn_t)
    return {
        "feasible": True,
        "schedule_feasible": tau_yr <= TAU_BURN_MAX_YR,
        "architecture": "variant_b",
        "dv_chem_km_s": dv_chem_km_s,
        "isp_elec_s": isp_elec_s,
        "delivered_water_t": delivered_t,
        "M_LEO_t": M_LEO_t,
        "tau_burn_yr": tau_yr,
        "M_v_t": M_v_t,
        "delivered_per_LEO": delivered_t / M_LEO_t,
    }


def best_cell(reactor_kwe: float, chunk_t: float, specific_power: float) -> dict:
    candidates = []
    for isp_elec in ELECTRIC_ISPS:
        ae = all_electric(reactor_kwe, chunk_t, isp_elec, specific_power)
        if ae.get("feasible") and ae.get("schedule_feasible"):
            candidates.append(ae)
        for dv_c in DV_CHEM_OPTIONS:
            if dv_c == 0.0:
                continue
            vb = variant_b(reactor_kwe, chunk_t, dv_c, isp_elec, specific_power)
            if vb.get("feasible") and vb.get("schedule_feasible"):
                candidates.append(vb)
    if not candidates:
        return {"feasible": False}
    return max(candidates, key=lambda c: c["delivered_per_LEO"])


def main() -> dict:
    grid = []
    for sp in SPECIFIC_POWERS:
        for reactor in REACTOR_POWERS_KWE:
            for chunk in CHUNKS_T:
                best = best_cell(reactor, chunk, sp)
                if best.get("feasible"):
                    best.update({"specific_power_w_per_kg": sp,
                                 "reactor_kwe": reactor,
                                 "chunk_t": chunk})
                else:
                    best = {"specific_power_w_per_kg": sp,
                            "reactor_kwe": reactor,
                            "chunk_t": chunk,
                            "feasible": False}
                grid.append(best)

    # Build per-specific-power tables: peak delivered/LEO vs reactor power, by chunk
    summary = []
    for sp in SPECIFIC_POWERS:
        for chunk in CHUNKS_T:
            entries = [g for g in grid if g["specific_power_w_per_kg"] == sp
                       and g["chunk_t"] == chunk and g.get("feasible")]
            if not entries:
                continue
            peak = max(entries, key=lambda g: g["delivered_per_LEO"])
            summary.append({
                "specific_power": sp,
                "chunk_t": chunk,
                "peak_reactor_kwe": peak["reactor_kwe"],
                "peak_ratio": peak["delivered_per_LEO"],
                "peak_architecture": peak["architecture"],
                "peak_delivered_t": peak["delivered_water_t"],
                "peak_M_LEO_t": peak["M_LEO_t"],
            })

    out = {
        "axes": {
            "specific_power_w_per_kg": SPECIFIC_POWERS,
            "reactor_kwe": REACTOR_POWERS_KWE,
            "chunk_t": CHUNKS_T,
        },
        "grid": grid,
        "peak_summary": summary,
    }
    results_dir = Path(__file__).parent / "results"
    results_dir.mkdir(exist_ok=True)
    (results_dir / "specific_power.json").write_text(json.dumps(out, indent=2, default=str))

    # Markdown tables
    lines = []
    lines.append("### Peak delivered-water-per-launch-mass and optimum reactor power, by (specific power × chunk)\n")
    lines.append("| Specific power (W/kg) | Chunk (t) | Peak reactor (kWe) | Peak ratio | Architecture | Delivered (t) | Launch mass (t) |")
    lines.append("|---:|---:|---:|---:|---|---:|---:|")
    for s in summary:
        lines.append(
            f"| {s['specific_power']:.0f} | {s['chunk_t']:.0f} | "
            f"{s['peak_reactor_kwe']:.0f} | {s['peak_ratio']:.2f} | "
            f"{s['peak_architecture']} | {s['peak_delivered_t']:.1f} | {s['peak_M_LEO_t']:.0f} |"
        )

    lines.append("\n### Delivered/launch-mass ratio at 200 t chunk, sweep reactor power × specific power\n")
    lines.append("| Reactor (kWe) | 5 W/kg | 10 W/kg | 20 W/kg | 40 W/kg |")
    lines.append("|---:|---:|---:|---:|---:|")
    for reactor in REACTOR_POWERS_KWE:
        row = [f"{reactor:.0f}"]
        for sp in SPECIFIC_POWERS:
            g = next((g for g in grid if g["reactor_kwe"] == reactor
                      and g["chunk_t"] == 200.0
                      and g["specific_power_w_per_kg"] == sp), None)
            if g and g.get("feasible"):
                row.append(f"{g['delivered_per_LEO']:.2f}")
            else:
                row.append("-")
        lines.append("| " + " | ".join(row) + " |")

    lines.append("\n### Delivered/launch-mass ratio at 500 t chunk, sweep reactor power × specific power\n")
    lines.append("| Reactor (kWe) | 5 W/kg | 10 W/kg | 20 W/kg | 40 W/kg |")
    lines.append("|---:|---:|---:|---:|---:|")
    for reactor in REACTOR_POWERS_KWE:
        row = [f"{reactor:.0f}"]
        for sp in SPECIFIC_POWERS:
            g = next((g for g in grid if g["reactor_kwe"] == reactor
                      and g["chunk_t"] == 500.0
                      and g["specific_power_w_per_kg"] == sp), None)
            if g and g.get("feasible"):
                row.append(f"{g['delivered_per_LEO']:.2f}")
            else:
                row.append("-")
        lines.append("| " + " | ".join(row) + " |")

    lines.append("\n### Winning architecture at 200 t chunk, sweep reactor × specific power\n")
    lines.append("Format: architecture · Δv_chem (km/s) · electric Isp (s)\n")
    lines.append("| Reactor (kWe) | 5 W/kg | 10 W/kg | 20 W/kg | 40 W/kg |")
    lines.append("|---:|---|---|---|---|")
    for reactor in REACTOR_POWERS_KWE:
        row = [f"{reactor:.0f}"]
        for sp in SPECIFIC_POWERS:
            g = next((g for g in grid if g["reactor_kwe"] == reactor
                      and g["chunk_t"] == 200.0
                      and g["specific_power_w_per_kg"] == sp), None)
            if g and g.get("feasible"):
                row.append(f"{g['architecture']} dv_c{g['dv_chem_km_s']:.0f} Isp{g['isp_elec_s']:.0f}")
            else:
                row.append("-")
        lines.append("| " + " | ".join(row) + " |")

    (results_dir / "tables.md").write_text("\n".join(lines))
    return out


if __name__ == "__main__":
    out = main()
    print(f"Sweep complete. {len(out['grid'])} cells, {len(out['peak_summary'])} peaks.")
    print(f"  Wrote results/specific_power.json and results/tables.md")
