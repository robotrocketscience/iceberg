"""R-aerocapture — does Earth aerocapture eliminate the propulsive inbound burden?

Compute heat shield mass at entry conditions (Sutton-Graves stagnation-point
approximation), then re-evaluate the architecture matrix with reduced inbound
delta-v and added heat shield mass.

Headline comparison: per-cell delivered mass with vs without aerocapture.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

from waterprop.constants import G0, GM_EARTH, R_EARTH

YEAR_S = 365.25 * 86400.0

# Atmospheric / entry parameters
V_INF_KM_S = 6.0                    # post-lunar-tour Earth approach velocity
PERIAPSIS_ALTITUDE_KM = 90.0        # aerocapture periapsis (mid-atmosphere)
RHO_ATM_PERIAPSIS_KG_M3 = 1.0e-4    # atmospheric density at 90 km (mid-range)
R_NOSE_EFFECTIVE_M = 1.3            # effective nose radius for 10 m² area
T_PULSE_S = 200.0                   # aerocapture heat pulse duration
HEAT_SHIELD_AREA_M2 = 10.0
K_SUTTON_GRAVES = 1.74e-4           # W·m⁻²·(kg·m⁻³)⁻⁰·⁵·(m/s)⁻³
Q_ABLATIVE_SPECIFIC_J_PER_KG = 3.0e7  # ~30 MJ/kg for PICA-X-class ablatives

# Inbound and outbound conventions (matching prior rounds)
DV_INBOUND_NO_AERO_KM_S = 6.42
DV_INBOUND_AERO_TRIM_DEFAULT = 0.5  # km/s
DV_OUTBOUND_KM_S = 9.0
ISP_OUTBOUND_S = 2000.0
SPECIFIC_POWER_W_PER_KG = 10.0
M_TUG_KG = 5000.0
TAU_BURN_MAX_INBOUND_YR = 7.0

ETA_THR = {"Hall": 0.55, "RF_ion": 0.65, "dual_ion": 0.55}

REACTORS_KWE = [10.0, 40.0, 100.0, 200.0, 500.0, 1000.0]
CHUNKS_T = [100.0, 200.0, 500.0]
HEAT_SHIELD_FRACTIONS = [0.05, 0.10, 0.15]
DV_TRIM_SWEEP_KM_S = [0.3, 0.5, 1.0]
ELECTRIC_ISPS = [1500.0, 2000.0, 2934.0, 5000.0]


def thruster_class(isp_s: float) -> tuple[str, float]:
    if isp_s <= 1800.0:  return "Hall", ETA_THR["Hall"]
    if isp_s <= 3000.0:  return "RF_ion", ETA_THR["RF_ion"]
    return                       "dual_ion", ETA_THR["dual_ion"]


def vehicle_dry_t(reactor_kwe: float) -> float:
    return (M_TUG_KG + reactor_kwe * 1000.0 / SPECIFIC_POWER_W_PER_KG) / 1000.0


def entry_velocity_m_s(v_inf_km_s: float, periapsis_altitude_km: float) -> float:
    r_p = (R_EARTH + periapsis_altitude_km) * 1000.0  # m
    v_inf = v_inf_km_s * 1000.0
    GM = GM_EARTH * 1e9  # convert km^3/s^2 to m^3/s^2
    return math.sqrt(v_inf * v_inf + 2.0 * GM / r_p)


def peak_heat_flux_W_per_m2(v_entry_m_s: float, rho_atm: float, R_nose_m: float) -> float:
    """Sutton-Graves stagnation-point approximation."""
    return K_SUTTON_GRAVES * math.sqrt(rho_atm / R_nose_m) * v_entry_m_s ** 3


def heat_shield_mass_kg(v_inf_km_s: float, area_m2: float, t_pulse_s: float,
                       rho_atm: float = RHO_ATM_PERIAPSIS_KG_M3,
                       R_nose: float = R_NOSE_EFFECTIVE_M,
                       Q_specific: float = Q_ABLATIVE_SPECIFIC_J_PER_KG) -> dict:
    v_entry = entry_velocity_m_s(v_inf_km_s, PERIAPSIS_ALTITUDE_KM)
    q_dot_peak = peak_heat_flux_W_per_m2(v_entry, rho_atm, R_nose)
    # Integrated load: approximate as q_dot_peak × t_pulse × 0.6 (peak-to-average factor)
    Q_total_J_per_m2 = q_dot_peak * t_pulse_s * 0.6
    shield_mass_per_area = Q_total_J_per_m2 / Q_specific
    shield_mass_kg = shield_mass_per_area * area_m2
    return {
        "v_entry_m_s": v_entry,
        "q_dot_peak_W_per_m2": q_dot_peak,
        "Q_total_J_per_m2": Q_total_J_per_m2,
        "shield_mass_per_area_kg_per_m2": shield_mass_per_area,
        "shield_mass_kg": shield_mass_kg,
    }


def all_electric_inbound(reactor_kwe: float, chunk_t: float, isp_s: float,
                         dv_inbound_km_s: float, heat_shield_t: float = 0.0) -> dict:
    M_v_t = vehicle_dry_t(reactor_kwe) + heat_shield_t
    M_initial_t = M_v_t + chunk_t
    v_e = isp_s * G0
    M_final_t = M_initial_t * math.exp(-dv_inbound_km_s * 1000.0 / v_e)
    if M_final_t < M_v_t:
        return {"feasible": False}
    delivered_t = M_final_t - M_v_t
    m_prop_t = M_initial_t - M_final_t
    _, eta = thruster_class(isp_s)
    thrust_N = 2.0 * eta * reactor_kwe * 1000.0 / v_e
    tau_yr = m_prop_t * 1000.0 * v_e / thrust_N / YEAR_S
    M_LEO_t = M_v_t * math.exp(DV_OUTBOUND_KM_S * 1000.0 / (ISP_OUTBOUND_S * G0))
    return {
        "feasible": tau_yr <= TAU_BURN_MAX_INBOUND_YR,
        "schedule_feasible": tau_yr <= TAU_BURN_MAX_INBOUND_YR,
        "isp_s": isp_s,
        "delivered_water_t": delivered_t,
        "burn_time_yr": tau_yr,
        "M_v_t": M_v_t,
        "M_LEO_t": M_LEO_t,
        "delivered_per_LEO": delivered_t / M_LEO_t if M_LEO_t > 0 else 0.0,
    }


def best_all_electric(reactor_kwe: float, chunk_t: float, dv_inbound_km_s: float,
                      heat_shield_t: float = 0.0, ignore_burn_time: bool = False) -> dict | None:
    """Find best (max delivered) all-electric cell. If ignore_burn_time, accept any burn time
    so we can report the would-be-best architecture even when burn time exceeds 7 yr."""
    candidates = []
    for isp in ELECTRIC_ISPS:
        ae = all_electric_inbound(reactor_kwe, chunk_t, isp, dv_inbound_km_s, heat_shield_t)
        # Mass-feasibility check (M_final >= M_v): use the underlying feasibility-ignore-time
        mass_feasible = ae.get("M_v_t") is not None and not ae.get("infeasible_mass", False)
        if "delivered_water_t" not in ae:
            continue
        if ignore_burn_time or ae.get("schedule_feasible"):
            candidates.append(ae)
    if not candidates:
        return None
    return max(candidates, key=lambda c: c["delivered_water_t"])


def main() -> dict:
    # Heat shield characterization at v_inf 6 km/s
    shield_at_v6 = heat_shield_mass_kg(V_INF_KM_S, HEAT_SHIELD_AREA_M2, T_PULSE_S)

    # Cross-check: shield mass at other v_inf
    shield_sweep = {}
    for v_inf in [4.0, 5.0, 6.0, 8.0, 10.0]:
        shield_sweep[v_inf] = heat_shield_mass_kg(v_inf, HEAT_SHIELD_AREA_M2, T_PULSE_S)

    # Architecture grid: with vs without aerocapture.
    # For baseline, ignore burn time so we can compare delivered mass even when
    # baseline burn exceeds 7 yr (aerocapture's main value is making those cells feasible).
    grid = []
    for reactor in REACTORS_KWE:
        for chunk in CHUNKS_T:
            base = best_all_electric(reactor, chunk, DV_INBOUND_NO_AERO_KM_S,
                                     heat_shield_t=0.0, ignore_burn_time=True)
            aero_cells = {}
            for hs_frac in HEAT_SHIELD_FRACTIONS:
                for trim_dv in DV_TRIM_SWEEP_KM_S:
                    M_entry_t = chunk + vehicle_dry_t(reactor)
                    hs_t = hs_frac * M_entry_t
                    aero = best_all_electric(reactor, chunk, trim_dv, heat_shield_t=hs_t)
                    aero_cells[(hs_frac, trim_dv)] = aero
            grid.append({
                "reactor_kwe": reactor,
                "chunk_t": chunk,
                "baseline_no_aero": base,
                "aero_cells": aero_cells,
            })

    # Headline: best aerocapture cell per (reactor, chunk) at hs_frac=0.10, trim_dv=0.5
    headline = []
    for g in grid:
        base = g["baseline_no_aero"]
        aero = g["aero_cells"].get((0.10, 0.5))
        if base and aero:
            base_d = base.get("delivered_water_t", 0.0)
            aero_d = aero.get("delivered_water_t", 0.0)
            base_burn = base.get("burn_time_yr", 0.0)
            aero_burn = aero.get("burn_time_yr", 0.0)
            improvement_pct = ((aero_d - base_d) / base_d * 100.0) if base_d > 0 else None
            headline.append({
                "reactor_kwe": g["reactor_kwe"],
                "chunk_t": g["chunk_t"],
                "baseline_delivered_t": base_d,
                "aero_delivered_t": aero_d,
                "improvement_pct": improvement_pct,
                "baseline_burn_yr": base_burn,
                "aero_burn_yr": aero_burn,
                "baseline_feasible_7yr": base.get("schedule_feasible", False),
                "aero_feasible_7yr": aero.get("schedule_feasible", False),
                "baseline_isp": base.get("isp_s"),
                "aero_isp": aero.get("isp_s"),
            })

    out = {
        "constants": {
            "v_inf_km_s": V_INF_KM_S,
            "periapsis_altitude_km": PERIAPSIS_ALTITUDE_KM,
            "rho_atm_kg_m3": RHO_ATM_PERIAPSIS_KG_M3,
            "R_nose_effective_m": R_NOSE_EFFECTIVE_M,
            "t_pulse_s": T_PULSE_S,
            "heat_shield_area_m2": HEAT_SHIELD_AREA_M2,
            "Q_specific_J_per_kg": Q_ABLATIVE_SPECIFIC_J_PER_KG,
            "dv_inbound_no_aero_km_s": DV_INBOUND_NO_AERO_KM_S,
            "dv_outbound_km_s": DV_OUTBOUND_KM_S,
        },
        "shield_at_v_inf_6": shield_at_v6,
        "shield_sweep_v_inf": {f"{v}km_s": s for v, s in shield_sweep.items()},
        "grid": grid,
        "headline": headline,
    }
    results_dir = Path(__file__).parent / "results"
    results_dir.mkdir(exist_ok=True)
    # Convert tuple keys in aero_cells to strings for JSON serialization
    out_serializable = {**out}
    out_serializable["grid"] = [
        {**g, "aero_cells": {f"hs_{k[0]:.2f}_dv_{k[1]:.1f}": v for k, v in g["aero_cells"].items()}}
        for g in grid
    ]
    (results_dir / "aerocapture.json").write_text(json.dumps(out_serializable, indent=2, default=str))

    # Markdown tables
    lines = []
    lines.append("### Heat shield characterization at v_∞ = 6 km/s\n")
    s = shield_at_v6
    lines.append(f"- Entry velocity (at 90 km periapsis): **{s['v_entry_m_s']/1000:.2f} km/s**")
    lines.append(f"- Peak stagnation-point heat flux (Sutton-Graves): **{s['q_dot_peak_W_per_m2']/1e6:.2f} MW/m²**")
    lines.append(f"- Total heat load (integrated over 200 s pulse, 0.6 peak-to-average): **{s['Q_total_J_per_m2']/1e6:.1f} MJ/m²**")
    lines.append(f"- Shield mass per unit area (at PICA-X-class Q_specific = 30 MJ/kg): **{s['shield_mass_per_area_kg_per_m2']:.2f} kg/m²**")
    lines.append(f"- Total shield mass for 10 m² windward area: **{s['shield_mass_kg']:.0f} kg = {s['shield_mass_kg']/1000:.2f} tonnes**")
    lines.append(f"- As fraction of 100 t entry mass: **{s['shield_mass_kg']/1000/100*100:.2f}%**")

    lines.append("\n### Heat shield mass sweep across v_∞ (10 m² area, 200 s pulse)\n")
    lines.append("| v_∞ (km/s) | Entry v (km/s) | Peak q_dot (MW/m²) | Total Q (MJ/m²) | Shield mass (t) |")
    lines.append("|---:|---:|---:|---:|---:|")
    for v_inf, s_data in shield_sweep.items():
        lines.append(
            f"| {v_inf:.1f} | {s_data['v_entry_m_s']/1000:.2f} | "
            f"{s_data['q_dot_peak_W_per_m2']/1e6:.2f} | "
            f"{s_data['Q_total_J_per_m2']/1e6:.1f} | "
            f"{s_data['shield_mass_kg']/1000:.2f} |"
        )

    lines.append("\n### Delivered water (tonnes) — baseline vs aerocapture (10% shield, 0.5 km/s trim)\n")
    lines.append("| Reactor (kWe) | Chunk (t) | Baseline delivered (no aero) | Aerocapture delivered | Improvement | Baseline 7-yr feasible? | Aero 7-yr feasible? |")
    lines.append("|---:|---:|---:|---:|---:|:--:|:--:|")
    for h in headline:
        impr = f"+{h['improvement_pct']:.0f}%" if h['improvement_pct'] is not None else "-"
        base_feas = "yes" if h.get("baseline_feasible_7yr") else "no"
        aero_feas = "yes" if h.get("aero_feasible_7yr") else "no"
        lines.append(
            f"| {h['reactor_kwe']:.0f} | {h['chunk_t']:.0f} | "
            f"{h['baseline_delivered_t']:.1f} | {h['aero_delivered_t']:.1f} | "
            f"{impr} | {base_feas} | {aero_feas} |"
        )

    lines.append("\n### Inbound burn time (years) — baseline vs aerocapture\n")
    lines.append("| Reactor (kWe) | Chunk (t) | Baseline burn (yr) | Aero burn (yr) | Reduction |")
    lines.append("|---:|---:|---:|---:|---:|")
    for h in headline:
        red_str = "infeasible→feasible" if h.get("baseline_burn_yr", 0) > 7.0 and h.get("aero_feasible_7yr") else f"{(h.get('baseline_burn_yr', 0) - h.get('aero_burn_yr', 0)):.1f} yr"
        lines.append(
            f"| {h['reactor_kwe']:.0f} | {h['chunk_t']:.0f} | "
            f"{h.get('baseline_burn_yr', 0):.2f} | {h.get('aero_burn_yr', 0):.2f} | {red_str} |"
        )

    lines.append("\n### Aerocapture sensitivity: shield fraction × trim Δv at 100 t chunk / 40 kWe\n")
    g = next(g for g in grid if g["reactor_kwe"] == 40.0 and g["chunk_t"] == 100.0)
    lines.append("| Shield % of entry mass | Trim Δv = 0.3 km/s | Trim Δv = 0.5 km/s | Trim Δv = 1.0 km/s |")
    lines.append("|---:|---:|---:|---:|")
    for hs in HEAT_SHIELD_FRACTIONS:
        row = [f"{hs*100:.0f}%"]
        for dv in DV_TRIM_SWEEP_KM_S:
            cell = g["aero_cells"].get((hs, dv))
            if cell and cell.get("feasible"):
                row.append(f"{cell['delivered_water_t']:.1f} t")
            else:
                row.append("-")
        lines.append("| " + " | ".join(row) + " |")

    (results_dir / "tables.md").write_text("\n".join(lines))
    return out


if __name__ == "__main__":
    out = main()
    print(f"Sweep complete. {len(out['grid'])} cells.")
    print(f"  Wrote results/aerocapture.json and results/tables.md")
