"""R-two-stage-dv — does a chemical Saturn-departure stage relax the inbound-electric requirement?

Sweep the chemical/electric delta-v split. Hold total inbound delta-v = 6.42 km/s
(R10b 7-flyby case). Vary chemical share in {0..5} km/s. Vary chemical specific
impulse across hypergolic (320 s), cryogenic methalox (360 s), cryogenic
hydrolox (450 s). For each cell compute required electric specific impulse,
chemical propellant mass carried at Saturn-departure, required electric thrust,
and required electric power.

Pure algebra. No integrator. Dry mass neglected.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

from waterprop.constants import G0

YEAR_S = 365.25 * 86400.0
DV_TOTAL_KM_S = 6.42
TAU_BURN_YR = 5.0

ETAS = [0.5, 0.6, 0.7, 0.8, 0.9]
CHUNKS_T = [50.0, 100.0, 200.0, 350.0, 500.0]
DV_CHEM_KM_S = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0]
ISP_CHEM_S = {
    "hypergolic_MMH_NTO":   320.0,
    "cryogenic_methalox":   360.0,
    "cryogenic_hydrolox":   450.0,
}

# Outbound penalty assumption (for interpretation only — not part of sizing math)
ISP_ELEC_OUTBOUND_S = 2000.0
DV_OUTBOUND_KM_S = 9.0


def thruster_class_for_isp(isp_s: float) -> tuple[str, float]:
    if isp_s <= 1000.0:  return "MET_class",       0.30
    if isp_s <= 1800.0:  return "Hall_class",      0.55
    if isp_s <= 3000.0:  return "RF_ion_class",    0.65
    return                       "dual_ion_class", 0.55


def two_stage(eta: float, chunk_t: float, dv_chem_km_s: float, isp_chem_s: float) -> dict:
    if eta <= 0.0 or eta >= 1.0:
        return {"feasible": False}
    dv_elec_km_s = DV_TOTAL_KM_S - dv_chem_km_s
    if dv_elec_km_s < 0:
        return {"feasible": False}

    v_e_chem = isp_chem_s * G0
    # Chemical propellant carried at Saturn-depart (dry stage neglected; chunk-only after burn)
    m_chem_prop_t = chunk_t * (math.exp(dv_chem_km_s * 1000.0 / v_e_chem) - 1.0)

    if dv_elec_km_s > 0:
        v_e_elec_req = -dv_elec_km_s * 1000.0 / math.log(eta)
        isp_elec_req = v_e_elec_req / G0
        m_prop_elec_t = chunk_t * (1.0 - eta)
        thrust_N = m_prop_elec_t * 1000.0 * v_e_elec_req / (TAU_BURN_YR * YEAR_S)
        p_jet_kw = thrust_N * v_e_elec_req / 2.0 / 1000.0
        thr_class, eta_thr = thruster_class_for_isp(isp_elec_req)
        p_elec_kw = p_jet_kw / eta_thr
    else:
        v_e_elec_req = 0.0
        isp_elec_req = 0.0
        m_prop_elec_t = 0.0
        thrust_N = 0.0
        p_jet_kw = 0.0
        p_elec_kw = 0.0
        thr_class = "none_all_chemical"

    delivered_chunk_t = chunk_t * eta

    # Outbound launch penalty (illustrative): mass needed at Earth-low-orbit to deliver
    # m_chem_prop_t out to Saturn under electric outbound at v_e_elec_outbound = Isp 2000 s
    v_e_out = ISP_ELEC_OUTBOUND_S * G0
    pf_out = 1.0 - math.exp(-DV_OUTBOUND_KM_S * 1000.0 / v_e_out)
    earth_LEO_mass_for_chem_t = m_chem_prop_t / (1.0 - pf_out) if pf_out < 1.0 else float("inf")

    return {
        "feasible": True,
        "eta": eta,
        "chunk_t": chunk_t,
        "dv_chem_km_s": dv_chem_km_s,
        "dv_elec_km_s": dv_elec_km_s,
        "isp_chem_s": isp_chem_s,
        "isp_elec_required_s": isp_elec_req,
        "thruster_class": thr_class,
        "m_chem_prop_t": m_chem_prop_t,
        "chem_to_chunk_ratio": m_chem_prop_t / chunk_t if chunk_t > 0 else 0.0,
        "m_prop_elec_t": m_prop_elec_t,
        "thrust_N": thrust_N,
        "p_jet_kw": p_jet_kw,
        "p_electrical_kw": p_elec_kw,
        "delivered_chunk_t": delivered_chunk_t,
        "earth_LEO_mass_for_chem_t": earth_LEO_mass_for_chem_t,
    }


def main() -> dict:
    cells = []
    for eta in ETAS:
        for chunk in CHUNKS_T:
            for dv_chem in DV_CHEM_KM_S:
                for chem_name, isp_chem in ISP_CHEM_S.items():
                    cell = two_stage(eta, chunk, dv_chem, isp_chem)
                    cell["chem_chemistry"] = chem_name
                    cells.append(cell)

    # Headline table: required electric Isp by (eta x dv_chem), chemistry-independent
    isp_elec_table = []
    for eta in ETAS:
        row = {"eta": eta}
        for dv_chem in DV_CHEM_KM_S:
            dv_elec = DV_TOTAL_KM_S - dv_chem
            v_e = -dv_elec * 1000.0 / math.log(eta) if dv_elec > 0 else 0.0
            row[f"isp_elec_dv_chem_{dv_chem}"] = v_e / G0
        isp_elec_table.append(row)

    # Thruster-class auto-pick by (eta x dv_chem)
    thr_class_table = []
    for eta in ETAS:
        row = {"eta": eta}
        for dv_chem in DV_CHEM_KM_S:
            dv_elec = DV_TOTAL_KM_S - dv_chem
            if dv_elec <= 0:
                row[f"cls_dv_chem_{dv_chem}"] = "none_all_chemical"
            else:
                v_e = -dv_elec * 1000.0 / math.log(eta)
                cls, _ = thruster_class_for_isp(v_e / G0)
                row[f"cls_dv_chem_{dv_chem}"] = cls
        thr_class_table.append(row)

    # Chemical propellant mass by (chunk x dv_chem) at hypergolic
    chem_prop_table = []
    for chunk in CHUNKS_T:
        row = {"chunk_t": chunk}
        for dv_chem in DV_CHEM_KM_S:
            cell = two_stage(0.7, chunk, dv_chem, ISP_CHEM_S["hypergolic_MMH_NTO"])
            row[f"m_chem_prop_dv_chem_{dv_chem}"] = cell["m_chem_prop_t"]
            row[f"ratio_dv_chem_{dv_chem}"] = cell["chem_to_chunk_ratio"]
        chem_prop_table.append(row)

    # Optimum dv_chem per (eta) minimizing required electric Isp subject to chem-to-chunk ratio <= 1
    # (use hypergolic as base; with cryogenic the constraint relaxes slightly)
    optima = []
    for eta in ETAS:
        for chem_name, isp_chem in ISP_CHEM_S.items():
            best = None
            for dv_chem in DV_CHEM_KM_S:
                cell = two_stage(eta, 100.0, dv_chem, isp_chem)
                if cell["chem_to_chunk_ratio"] <= 1.0 and (
                    best is None or cell["isp_elec_required_s"] < best["isp_elec_required_s"]
                ):
                    best = cell
            if best is not None:
                optima.append({
                    "eta": eta,
                    "chem_chemistry": chem_name,
                    "best_dv_chem_km_s": best["dv_chem_km_s"],
                    "isp_elec_required_s": best["isp_elec_required_s"],
                    "thruster_class": best["thruster_class"],
                    "chem_to_chunk_ratio": best["chem_to_chunk_ratio"],
                    "p_electrical_kw_at_chunk_100t": best["p_electrical_kw"],
                })

    out = {
        "axes": {
            "eta": ETAS, "chunk_t": CHUNKS_T,
            "dv_chem_km_s": DV_CHEM_KM_S,
            "isp_chem_s": ISP_CHEM_S,
            "dv_total_km_s": DV_TOTAL_KM_S, "tau_burn_yr": TAU_BURN_YR,
        },
        "isp_elec_required_by_eta_x_dv_chem": isp_elec_table,
        "thruster_class_by_eta_x_dv_chem": thr_class_table,
        "chem_prop_mass_by_chunk_x_dv_chem_hypergolic": chem_prop_table,
        "optima_min_electric_isp_subject_chem_ratio_le_1": optima,
        "all_cells": cells,
    }

    results_dir = Path(__file__).parent / "results"
    results_dir.mkdir(exist_ok=True)
    (results_dir / "two_stage.json").write_text(json.dumps(out, indent=2))

    # Markdown tables
    lines = []
    lines.append("### Required electric specific impulse (s) by (delivered fraction × chemical delta-v offload)\n")
    lines.append(f"Total inbound delta-v = {DV_TOTAL_KM_S} km/s. Chemical specific impulse is irrelevant for this table (electric specific impulse only depends on delta-v_elec and η).\n")
    header = "| η |" + "".join(f" Δv_chem = {dv} km/s |" for dv in DV_CHEM_KM_S)
    lines.append(header)
    lines.append("|---:|" + "---:|" * len(DV_CHEM_KM_S))
    for r in isp_elec_table:
        cells_str = "".join(
            f" {r[f'isp_elec_dv_chem_{dv}']:.0f} |" if r[f'isp_elec_dv_chem_{dv}'] > 0 else " - |"
            for dv in DV_CHEM_KM_S
        )
        lines.append(f"| {r['eta']:.1f} |{cells_str}")

    lines.append("\n### Required thruster class by (delivered fraction × chemical delta-v offload)\n")
    lines.append(header)
    lines.append("|---:|" + "---:|" * len(DV_CHEM_KM_S))
    for r in thr_class_table:
        cells_str = "".join(f" {r[f'cls_dv_chem_{dv}']} |" for dv in DV_CHEM_KM_S)
        lines.append(f"| {r['eta']:.1f} |{cells_str}")

    lines.append("\n### Hypergolic chemical-propellant mass (tonnes) by (chunk × chemical delta-v offload), Isp_chem = 320 s\n")
    lines.append(header.replace("η", "chunk").replace("|", "| ", 1))
    lines.append("|---:|" + "---:|" * len(DV_CHEM_KM_S))
    for r in chem_prop_table:
        cells_str = "".join(
            f" {r[f'm_chem_prop_dv_chem_{dv}']:.0f} ({r[f'ratio_dv_chem_{dv}']:.2f}×) |"
            for dv in DV_CHEM_KM_S
        )
        lines.append(f"| {r['chunk_t']:.0f} t |{cells_str}")

    lines.append("\nRatio in parentheses is chemical-propellant-mass / chunk-mass. Ratio > 1 means more chemical propellant than chunk.\n")

    lines.append("\n### Optimum chemical delta-v offload per delivered-fraction target, subject to chem-propellant ≤ chunk-mass constraint\n")
    lines.append("Chunk = 100 t reference. The constraint chem_to_chunk_ratio ≤ 1 limits how much chemical offload is realistic from a launch-mass standpoint.\n")
    lines.append("| η | chemistry | optimum Δv_chem (km/s) | required electric Isp (s) | thruster class | chem-to-chunk ratio | electric power (kWe) |")
    lines.append("|---:|---|---:|---:|---|---:|---:|")
    for o in optima:
        lines.append(
            f"| {o['eta']:.1f} | {o['chem_chemistry']} | "
            f"{o['best_dv_chem_km_s']:.1f} | {o['isp_elec_required_s']:.0f} | "
            f"{o['thruster_class']} | {o['chem_to_chunk_ratio']:.2f} | "
            f"{o['p_electrical_kw_at_chunk_100t']:.0f} |"
        )

    (results_dir / "tables.md").write_text("\n".join(lines))
    return out


if __name__ == "__main__":
    out = main()
    print(f"Sweep complete. {len(out['all_cells'])} cells.")
    print(f"  Wrote results/two_stage.json and results/tables.md")
