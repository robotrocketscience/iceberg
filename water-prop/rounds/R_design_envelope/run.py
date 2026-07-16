"""R-design-envelope — required (Isp, thrust, power) per (delivered fraction, chunk mass) cell.

Inverts the forward-design rounds (R6, R10, R10b). Given a target delivered
fraction and a grappled chunk mass, compute the required specific impulse,
thrust, and electrical power from rocket-equation + constant-thrust algebra.

Pure algebra. No integrator. Dry-mass neglected at this layer (flagged in STUDY.md).
"""

from __future__ import annotations

import json
import math
from pathlib import Path

from waterprop.constants import G0

YEAR_S = 365.25 * 86400.0

# Sweep axes
ETAS = [0.5, 0.6, 0.7, 0.8, 0.9]
CHUNKS_T = [10.0, 25.0, 50.0, 100.0, 200.0, 350.0, 500.0]
DV_KM_S = [4.47, 6.42, 8.87]  # R10b 10-/7-/3-flyby inbound residuals
TAU_YR = [3.0, 5.0, 7.0]
ETA_THR = {"MET_class": 0.30, "Hall_class": 0.55, "RF_ion_class": 0.65}

# Existing thruster classes for the mapping back to known tech
KNOWN_THRUSTERS = [
    {"name": "water_MET",         "isp_s":  700.0, "eta_thr": 0.30},
    {"name": "water_Hall",        "isp_s": 1500.0, "eta_thr": 0.55},
    {"name": "water_RF_ion",      "isp_s": 2000.0, "eta_thr": 0.65},
    {"name": "water_dual_ion",    "isp_s": 5000.0, "eta_thr": 0.55},
    {"name": "H2_NTP_solid_core", "isp_s":  900.0, "eta_thr": 1.00},  # thermal; jet power == reactor thermal
]


def required(eta: float, chunk_t: float, dv_km_s: float, tau_yr: float) -> dict:
    """Rocket-equation + constant-thrust algebra for one cell."""
    if eta <= 0.0 or eta >= 1.0:
        return {"feasible": False}
    dv = dv_km_s * 1000.0
    tau = tau_yr * YEAR_S
    v_e = -dv / math.log(eta)             # ve to hit eta at given dv
    isp_s = v_e / G0
    m_prop_kg = chunk_t * 1000.0 * (1.0 - eta)
    f_n = m_prop_kg * v_e / tau           # constant-thrust over tau seconds
    p_jet_w = f_n * v_e / 2.0
    # Electrical power for each thruster class (only meaningful for electric)
    p_e = {label: p_jet_w / eff for label, eff in ETA_THR.items()}
    return {
        "feasible": True,
        "isp_s": isp_s,
        "v_e_m_s": v_e,
        "thrust_N": f_n,
        "m_prop_t": m_prop_kg / 1000.0,
        "p_jet_kw": p_jet_w / 1000.0,
        "p_electrical_kw": {k: v / 1000.0 for k, v in p_e.items()},
    }


def known_thruster_max_eta(thr: dict, dv_km_s: float) -> float:
    """Given a thruster's Isp, what delivered fraction does it support at this dv?"""
    v_e = thr["isp_s"] * G0
    return math.exp(-dv_km_s * 1000.0 / v_e)


def fmt(x: float, w: int = 8, dp: int = 1) -> str:
    if x >= 1e6:
        return f"{x/1e6:>{w-1}.{dp}f}M"
    if x >= 1e3:
        return f"{x/1e3:>{w-1}.{dp}f}k"
    return f"{x:>{w}.{dp}f}"


def main() -> dict:
    cells = []
    for eta in ETAS:
        for chunk in CHUNKS_T:
            for dv in DV_KM_S:
                for tau in TAU_YR:
                    cell = required(eta, chunk, dv, tau)
                    cell.update({"eta_delivered": eta, "chunk_t": chunk,
                                 "dv_km_s": dv, "tau_burn_yr": tau})
                    cells.append(cell)

    # Headline table 1: required Isp by (eta x dv). Chunk-independent.
    isp_table = []
    for eta in ETAS:
        row = {"eta_delivered": eta}
        for dv in DV_KM_S:
            v_e = -dv * 1000.0 / math.log(eta)
            row[f"isp_dv{dv}"] = v_e / G0
        isp_table.append(row)

    # Headline table 2: required thrust by (eta x chunk) at representative dv=6.42, tau=5 yr.
    thrust_table = []
    for eta in ETAS:
        row = {"eta_delivered": eta}
        for chunk in CHUNKS_T:
            c = required(eta, chunk, 6.42, 5.0)
            row[f"thrust_M{int(chunk)}"] = c["thrust_N"]
        thrust_table.append(row)

    # Headline table 3: required electrical power at representative dv=6.42, tau=5 yr,
    # thruster class chosen by the required Isp band.
    def thruster_for_isp(isp: float) -> tuple[str, float]:
        # Stratification: MET to 1000 s; Hall 1000-1800; RF-ion 1800-3000; dual-ion 3000+
        if isp <= 1000.0:  return "MET_class",      0.30
        if isp <= 1800.0:  return "Hall_class",     0.55
        if isp <= 3000.0:  return "RF_ion_class",   0.65
        return                   "dual_ion_class",  0.55

    power_table = []
    for eta in ETAS:
        row = {"eta_delivered": eta}
        for chunk in CHUNKS_T:
            c = required(eta, chunk, 6.42, 5.0)
            cls, eff = thruster_for_isp(c["isp_s"])
            p_e_kw = c["p_jet_kw"] / eff
            row[f"pe_M{int(chunk)}_kw"] = p_e_kw
            row[f"cls_M{int(chunk)}"] = cls
        power_table.append(row)

    # Known thrusters: what fraction can each deliver at each dv?
    known_eta_table = []
    for thr in KNOWN_THRUSTERS:
        row = {"name": thr["name"], "isp_s": thr["isp_s"]}
        for dv in DV_KM_S:
            row[f"eta_dv{dv}"] = known_thruster_max_eta(thr, dv)
        known_eta_table.append(row)

    # Coverage check: at dv=6.42, tau=5 yr, eta_thr_class auto-chosen,
    # how many (eta, M) cells fall under each (Isp_band, F_band, P_band)?
    bands_isp = [(0, 1000, "MET"),
                 (1000, 1800, "Hall"),
                 (1800, 3000, "RF_ion"),
                 (3000, 1e6, "dual_ion")]
    bands_pow_kw = [(0, 50, "<=50 kWe"),
                    (50, 200, "50-200 kWe"),
                    (200, 500, "200-500 kWe"),
                    (500, 2000, "500 kWe - 2 MWe"),
                    (2000, 1e9, ">2 MWe")]
    coverage = {}
    for eta in ETAS:
        for chunk in CHUNKS_T:
            c = required(eta, chunk, 6.42, 5.0)
            cls, eff = thruster_for_isp(c["isp_s"])
            p_e_kw = c["p_jet_kw"] / eff
            isp_band = next(name for lo, hi, name in bands_isp if lo <= c["isp_s"] < hi)
            pow_band = next(name for lo, hi, name in bands_pow_kw if lo <= p_e_kw < hi)
            coverage.setdefault((isp_band, pow_band), []).append((eta, chunk))

    out = {
        "axes": {
            "eta": ETAS, "chunk_t": CHUNKS_T,
            "dv_km_s": DV_KM_S, "tau_yr": TAU_YR,
            "eta_thr_classes": ETA_THR,
        },
        "isp_required_by_eta_x_dv": isp_table,
        "thrust_required_by_eta_x_chunk_at_dv6.42_tau5": thrust_table,
        "power_required_by_eta_x_chunk_at_dv6.42_tau5": power_table,
        "known_thruster_max_eta": known_eta_table,
        "coverage_by_isp_pow_band_at_dv6.42_tau5": {
            f"{i}|{p}": cells for (i, p), cells in coverage.items()
        },
        "all_cells": cells,
    }

    results_dir = Path(__file__).parent / "results"
    results_dir.mkdir(exist_ok=True)
    (results_dir / "design_envelope.json").write_text(json.dumps(out, indent=2))

    # Markdown tables for the STUDY.md Result section
    lines = []
    lines.append("### Required Isp (s) by (delivered fraction × inbound Δv)\n")
    lines.append("Rocket equation Isp = -Δv / (g₀ · ln η). Chunk-mass independent.\n")
    lines.append("| η delivered | Δv = 4.47 km/s | Δv = 6.42 km/s | Δv = 8.87 km/s |")
    lines.append("|---:|---:|---:|---:|")
    for r in isp_table:
        lines.append(f"| {r['eta_delivered']:.1f} | "
                     f"{r['isp_dv4.47']:.0f} | {r['isp_dv6.42']:.0f} | {r['isp_dv8.87']:.0f} |")

    lines.append("\n### Required thrust (N) by (delivered fraction × chunk), at Δv = 6.42 km/s, τ_burn = 5 yr\n")
    lines.append("| η | 10 t | 25 t | 50 t | 100 t | 200 t | 350 t | 500 t |")
    lines.append("|---:|---:|---:|---:|---:|---:|---:|---:|")
    for r in thrust_table:
        row = [f"{r['eta_delivered']:.1f}"]
        for chunk in CHUNKS_T:
            row.append(f"{r[f'thrust_M{int(chunk)}']:.2f}")
        lines.append("| " + " | ".join(row) + " |")

    lines.append("\n### Required electrical power (kWe) by (delivered fraction × chunk), thruster class auto-chosen by required Isp band, η_thr per class, Δv = 6.42 km/s, τ_burn = 5 yr\n")
    lines.append("| η | 10 t | 25 t | 50 t | 100 t | 200 t | 350 t | 500 t |")
    lines.append("|---:|---:|---:|---:|---:|---:|---:|---:|")
    for r in power_table:
        row = [f"{r['eta_delivered']:.1f}"]
        for chunk in CHUNKS_T:
            row.append(f"{r[f'pe_M{int(chunk)}_kw']:.0f}")
        lines.append("| " + " | ".join(row) + " |")

    lines.append("\n### Known thruster maximum delivered fraction at each Δv\n")
    lines.append("Maximum η achievable for that thruster's Isp (so any column showing η ≥ target means the thruster reaches it).\n")
    lines.append("| Thruster | Isp (s) | η_max at Δv 4.47 | η_max at Δv 6.42 | η_max at Δv 8.87 |")
    lines.append("|---|---:|---:|---:|---:|")
    for r in known_eta_table:
        lines.append(f"| {r['name']} | {r['isp_s']:.0f} | "
                     f"{r['eta_dv4.47']:.3f} | {r['eta_dv6.42']:.3f} | {r['eta_dv8.87']:.3f} |")

    lines.append("\n### Coverage: which (Isp band, power band) cell each (η, chunk) lands in (Δv = 6.42 km/s, τ_burn = 5 yr)\n")
    for (i, p), cell_list in sorted(coverage.items()):
        cells_str = ", ".join(f"({e:.1f}, {int(m)}t)" for e, m in cell_list)
        lines.append(f"- **{i} class, {p}** → {len(cell_list)} cell(s): {cells_str}")

    (results_dir / "tables.md").write_text("\n".join(lines))
    return out


if __name__ == "__main__":
    out = main()
    print("Sweep complete.")
    print(f"  Cells computed: {len(out['all_cells'])}")
    print(f"  Wrote results/design_envelope.json and results/tables.md")
