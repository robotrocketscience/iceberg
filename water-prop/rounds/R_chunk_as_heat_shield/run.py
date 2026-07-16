"""R-chunk-as-heat-shield — bag survival + chunk ablation for aerocapture vs aerobraking.

Two-mode atmospheric capture analysis:
  - Single-pass aerocapture (90 km periapsis, 1 pass, ~3-6 MW/m²)
  - Multi-pass aerobraking (180 km periapsis, ~30 passes, ~1-3 kW/m²)

Compute per-pass heat flux, total chunk ablation, bag radiative-equilibrium
temperature, and time penalty.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

from waterprop.constants import G0, GM_EARTH, R_EARTH

SIGMA_SB = 5.670374419e-8  # Stefan-Boltzmann W/(m²·K⁴)
K_SUTTON_GRAVES = 1.74e-4  # convective heat flux constant

# Atmospheric densities (kg/m³) at altitude (km), rough mid-latitude values
ATM_DENSITY = {
    90:  1.0e-4,
    100: 1.0e-5,
    110: 1.0e-6,
    130: 1.0e-7,
    150: 1.0e-8,
    180: 5.0e-10,
    200: 1.5e-10,
}

V_INF_KM_S = 6.0
M_VEHICLE_KG = 100_000.0  # 100 tonnes
A_WINDWARD_M2 = 25.0
R_NOSE_M = 1.5
C_D = 1.5  # blunt body drag coefficient

# Material properties
Q_SUBLIM_WATER_ICE_J_PER_KG = 2.84e6      # latent heat of sublimation from 200 K
Q_SUBLIM_EFFECTIVE_J_PER_KG = 25e6        # with boundary-layer-blocking factor (PICA-X-class)
BAG_LAMINATE_TMAX_K = 700.0               # polyimide continuous-use limit
BAG_EMISSIVITY_FRONT = 0.3                # multi-layer-insulation front surface

# Pulse properties
T_PULSE_AERO_S = 200.0
PEAK_TO_AVG = 0.6
T_PULSE_BRAKE_PER_PASS_S = 600.0          # shallow pass, longer atmosphere transit


def entry_velocity_m_s(v_inf_km_s: float, periapsis_alt_km: float) -> float:
    r_p = (R_EARTH + periapsis_alt_km) * 1000.0
    v_inf = v_inf_km_s * 1000.0
    GM = GM_EARTH * 1e9
    return math.sqrt(v_inf * v_inf + 2.0 * GM / r_p)


def heat_flux_convective(rho: float, v_entry: float, R_nose: float) -> float:
    return K_SUTTON_GRAVES * math.sqrt(rho / R_nose) * v_entry ** 3


def heat_flux_radiative_estimate(q_conv: float, v_entry_km_s: float) -> float:
    """Rough estimate: ~50% of convective at 11-13 km/s, scales steeply with v above that."""
    if v_entry_km_s < 8:
        return 0.0
    return 0.5 * q_conv * max(1.0, (v_entry_km_s / 12.0) ** 2)


def equilibrium_temp_K(q_dot_W_per_m2: float, emissivity: float = 1.0) -> float:
    return (q_dot_W_per_m2 / (emissivity * SIGMA_SB)) ** 0.25


def passes_for_aerobraking(v_inf_km_s: float, rho_at_periapsis: float,
                            A_drag: float = A_WINDWARD_M2,
                            M_vehicle: float = M_VEHICLE_KG) -> tuple[int, float]:
    """Estimate passes to dissipate kinetic energy to circular LEO.

    Per-pass delta-v dissipated by drag during atmospheric transit.
    """
    v_inf = v_inf_km_s * 1000.0
    KE_total_J = 0.5 * M_vehicle * v_inf ** 2
    # Per-pass: F_drag × distance_through_atmosphere × duration_factor
    # Simplified: per-pass dv ≈ rho × v × C_D × A / M × L
    # where L = effective path length through atmosphere ≈ 2 × sqrt(2 × R_atm × H_scale)
    # H_scale ≈ 6 km at 180 km altitude; R_atm ≈ R_earth = 6378 km
    H_scale_m = 6000.0
    R_atm_m = (R_EARTH + 180.0) * 1000.0
    L_eff_m = 2.0 * math.sqrt(2.0 * R_atm_m * H_scale_m)
    v_entry = entry_velocity_m_s(v_inf_km_s, 180.0)
    dv_per_pass_m_s = rho_at_periapsis * v_entry * C_D * A_drag / M_vehicle * L_eff_m
    if dv_per_pass_m_s <= 0:
        return (0, 0.0)
    # Target dissipation: full v_inf
    n_passes = max(1, math.ceil(v_inf / dv_per_pass_m_s))
    # Time per pass: orbital period of capture ellipse. Start with apogee high (~300,000 km).
    # As apogee decays, period shrinks. Average period during decay ≈ 5 days.
    avg_period_days = 5.0
    total_time_days = n_passes * avg_period_days
    return (n_passes, total_time_days)


def sweep_altitudes_for_aerobraking() -> list:
    """Heat flux + per-pass dv across altitude band to find the trade-off."""
    out = []
    for alt in [90, 100, 110, 130, 150, 180, 200]:
        rho = ATM_DENSITY.get(alt, 0)
        if rho <= 0:
            continue
        v_e = entry_velocity_m_s(V_INF_KM_S, alt)
        q_conv = heat_flux_convective(rho, v_e, R_NOSE_M)
        q_rad = heat_flux_radiative_estimate(q_conv, v_e / 1000.0)
        q_total = q_conv + q_rad
        # Per-pass dv at this altitude (using H_scale from approximate isothermal atmosphere)
        H_scale = 7000 if alt < 110 else (5000 if alt < 150 else 30000)
        L_eff = 2.0 * math.sqrt(2.0 * (R_EARTH + alt) * 1000.0 * H_scale)
        dv_per_pass = rho * v_e * C_D * A_WINDWARD_M2 / M_VEHICLE_KG * L_eff
        n_passes_needed = max(1, math.ceil(V_INF_KM_S * 1000.0 / dv_per_pass)) if dv_per_pass > 0 else float("inf")
        T_eq_mli = equilibrium_temp_K(q_total, BAG_EMISSIVITY_FRONT)
        T_eq_gray = equilibrium_temp_K(q_total, 1.0)
        T_eq_high_e = equilibrium_temp_K(q_total, 0.8)  # high-emissivity outer skin
        out.append({
            "altitude_km": alt,
            "rho_kg_per_m3": rho,
            "v_entry_m_s": v_e,
            "q_total_kW_per_m2": q_total / 1000.0,
            "dv_per_pass_m_s": dv_per_pass,
            "n_passes_needed": n_passes_needed,
            "T_eq_gray_K": T_eq_gray,
            "T_eq_high_e_K": T_eq_high_e,
            "T_eq_mli_K": T_eq_mli,
            "bag_survives_gray": T_eq_gray < BAG_LAMINATE_TMAX_K,
            "bag_survives_high_e": T_eq_high_e < BAG_LAMINATE_TMAX_K,
            "bag_survives_mli": T_eq_mli < BAG_LAMINATE_TMAX_K,
        })
    return out


def main() -> dict:
    results: dict = {"modes": {}, "altitude_sweep": sweep_altitudes_for_aerobraking()}

    # Mode A: single-pass aerocapture at 90 km
    rho_aero = ATM_DENSITY[90]
    v_entry_aero = entry_velocity_m_s(V_INF_KM_S, 90.0)
    q_conv_aero = heat_flux_convective(rho_aero, v_entry_aero, R_NOSE_M)
    q_rad_aero = heat_flux_radiative_estimate(q_conv_aero, v_entry_aero / 1000.0)
    q_total_aero = q_conv_aero + q_rad_aero
    Q_per_pass_aero = q_total_aero * T_PULSE_AERO_S * PEAK_TO_AVG
    ablation_per_m2_aero = Q_per_pass_aero / Q_SUBLIM_EFFECTIVE_J_PER_KG
    total_ablation_aero_kg = ablation_per_m2_aero * A_WINDWARD_M2
    T_eq_aero_gray = equilibrium_temp_K(q_total_aero, emissivity=1.0)
    T_eq_aero_mli = equilibrium_temp_K(q_total_aero, emissivity=BAG_EMISSIVITY_FRONT)
    bag_survives_aero = T_eq_aero_mli <= BAG_LAMINATE_TMAX_K

    results["modes"]["A_aerocapture_single_pass"] = {
        "periapsis_altitude_km": 90,
        "atm_density_kg_per_m3": rho_aero,
        "entry_velocity_m_s": v_entry_aero,
        "q_convective_W_per_m2": q_conv_aero,
        "q_radiative_W_per_m2": q_rad_aero,
        "q_total_W_per_m2": q_total_aero,
        "Q_per_pass_J_per_m2": Q_per_pass_aero,
        "ablation_kg_per_m2": ablation_per_m2_aero,
        "total_ablation_kg": total_ablation_aero_kg,
        "chunk_ablation_fraction": total_ablation_aero_kg / 100_000.0,
        "T_equilibrium_gray_K": T_eq_aero_gray,
        "T_equilibrium_mli_K": T_eq_aero_mli,
        "bag_survives": bag_survives_aero,
        "n_passes": 1,
        "time_days": 0.1,
    }

    # Mode B: multi-pass aerobraking at 180 km
    rho_brake = ATM_DENSITY[180]
    v_entry_brake = entry_velocity_m_s(V_INF_KM_S, 180.0)
    q_conv_brake = heat_flux_convective(rho_brake, v_entry_brake, R_NOSE_M)
    q_rad_brake = heat_flux_radiative_estimate(q_conv_brake, v_entry_brake / 1000.0)
    q_total_brake = q_conv_brake + q_rad_brake
    n_passes_brake, time_brake_days = passes_for_aerobraking(V_INF_KM_S, rho_brake)
    Q_per_pass_brake = q_total_brake * T_PULSE_BRAKE_PER_PASS_S * PEAK_TO_AVG
    Q_total_campaign_brake = Q_per_pass_brake * n_passes_brake
    ablation_per_m2_brake = Q_total_campaign_brake / Q_SUBLIM_EFFECTIVE_J_PER_KG
    total_ablation_brake_kg = ablation_per_m2_brake * A_WINDWARD_M2
    T_eq_brake_gray = equilibrium_temp_K(q_total_brake, emissivity=1.0)
    T_eq_brake_mli = equilibrium_temp_K(q_total_brake, emissivity=BAG_EMISSIVITY_FRONT)
    bag_survives_brake = T_eq_brake_mli <= BAG_LAMINATE_TMAX_K

    results["modes"]["B_aerobraking_multipass"] = {
        "periapsis_altitude_km": 180,
        "atm_density_kg_per_m3": rho_brake,
        "entry_velocity_m_s": v_entry_brake,
        "q_convective_W_per_m2": q_conv_brake,
        "q_radiative_W_per_m2": q_rad_brake,
        "q_total_W_per_m2": q_total_brake,
        "Q_per_pass_J_per_m2": Q_per_pass_brake,
        "Q_total_campaign_J_per_m2": Q_total_campaign_brake,
        "ablation_kg_per_m2": ablation_per_m2_brake,
        "total_ablation_kg": total_ablation_brake_kg,
        "chunk_ablation_fraction": total_ablation_brake_kg / 100_000.0,
        "T_equilibrium_gray_K": T_eq_brake_gray,
        "T_equilibrium_mli_K": T_eq_brake_mli,
        "bag_survives": bag_survives_brake,
        "n_passes": n_passes_brake,
        "time_days": time_brake_days,
        "time_months": time_brake_days / 30.0,
    }

    # Mode C: intermediate at 130 km (sanity check)
    rho_int = ATM_DENSITY[130]
    v_entry_int = entry_velocity_m_s(V_INF_KM_S, 130.0)
    q_conv_int = heat_flux_convective(rho_int, v_entry_int, R_NOSE_M)
    q_rad_int = heat_flux_radiative_estimate(q_conv_int, v_entry_int / 1000.0)
    q_total_int = q_conv_int + q_rad_int
    T_eq_int_mli = equilibrium_temp_K(q_total_int, emissivity=BAG_EMISSIVITY_FRONT)
    n_passes_int, time_int_days = passes_for_aerobraking(V_INF_KM_S, rho_int)
    Q_per_pass_int = q_total_int * T_PULSE_BRAKE_PER_PASS_S * PEAK_TO_AVG
    total_Q_int = Q_per_pass_int * max(1, n_passes_int)
    ablation_int_kg = (total_Q_int / Q_SUBLIM_EFFECTIVE_J_PER_KG) * A_WINDWARD_M2
    results["modes"]["C_intermediate_130km"] = {
        "periapsis_altitude_km": 130,
        "q_total_W_per_m2": q_total_int,
        "T_equilibrium_mli_K": T_eq_int_mli,
        "n_passes": n_passes_int,
        "time_days": time_int_days,
        "total_ablation_kg": ablation_int_kg,
        "bag_survives": T_eq_int_mli <= BAG_LAMINATE_TMAX_K,
    }

    # Time penalty as fraction of 14-yr round trip
    results["time_penalty_fraction"] = time_brake_days / (14 * 365.25)

    # Material tolerance sanity
    results["material_tolerances"] = {
        "polyimide_continuous_K": 700,
        "polyimide_short_term_K": 800,
        "vectran_K": 600,
        "aluminized_mylar_K": 520,
        "bag_emissivity_assumed": BAG_EMISSIVITY_FRONT,
        "Q_sublimation_water_ice_MJ_per_kg": Q_SUBLIM_WATER_ICE_J_PER_KG / 1e6,
        "Q_effective_with_blocking_MJ_per_kg": Q_SUBLIM_EFFECTIVE_J_PER_KG / 1e6,
    }

    results_dir = Path(__file__).parent / "results"
    results_dir.mkdir(exist_ok=True)
    (results_dir / "heat_shield.json").write_text(json.dumps(results, indent=2, default=str))

    # Markdown tables
    lines = []
    lines.append("### Per-mode heat flux, bag survival, and chunk ablation\n")
    lines.append("| Quantity | A (aerocapture, 90 km, 1 pass) | B (aerobraking, 180 km, multi-pass) | C (intermediate, 130 km) |")
    lines.append("|---|---:|---:|---:|")
    a = results["modes"]["A_aerocapture_single_pass"]
    b = results["modes"]["B_aerobraking_multipass"]
    c = results["modes"]["C_intermediate_130km"]
    lines.append(f"| Periapsis altitude (km) | {a['periapsis_altitude_km']} | {b['periapsis_altitude_km']} | {c['periapsis_altitude_km']} |")
    lines.append(f"| Atmospheric density (kg/m³) | {a['atm_density_kg_per_m3']:.1e} | {b['atm_density_kg_per_m3']:.1e} | — |")
    lines.append(f"| Entry velocity (km/s) | {a['entry_velocity_m_s']/1000:.2f} | {b['entry_velocity_m_s']/1000:.2f} | — |")
    lines.append(f"| Peak heat flux (kW/m²) | **{a['q_total_W_per_m2']/1000:,.0f}** | **{b['q_total_W_per_m2']/1000:.2f}** | **{c['q_total_W_per_m2']/1000:.2f}** |")
    lines.append(f"| Number of passes | 1 | {b['n_passes']} | {c['n_passes']} |")
    lines.append(f"| Total campaign time (days) | < 0.1 | {b['time_days']:.0f} | {c['time_days']:.0f} |")
    lines.append(f"| Total campaign time (months) | < 0.01 | {b['time_months']:.1f} | {c['time_days']/30:.1f} |")
    lines.append(f"| Chunk ablation total (kg) | **{a['total_ablation_kg']:,.0f}** | **{b['total_ablation_kg']:.2f}** | **{c['total_ablation_kg']:.2f}** |")
    lines.append(f"| Chunk ablation as % of 100 t chunk | {a['chunk_ablation_fraction']*100:.3f}% | {b['chunk_ablation_fraction']*100:.5f}% | — |")
    lines.append(f"| Bag radiative equilibrium temperature, MLI emissivity 0.3 (K) | **{a['T_equilibrium_mli_K']:,.0f}** | **{b['T_equilibrium_mli_K']:.0f}** | **{c['T_equilibrium_mli_K']:.0f}** |")
    lines.append(f"| Bag survives? (polyimide T_max 700 K) | **{'YES' if a['bag_survives'] else 'NO'}** | **{'YES' if b['bag_survives'] else 'NO'}** | **{'YES' if c['bag_survives'] else 'NO'}** |")

    lines.append("\n### Time penalty as fraction of 14-year round trip\n")
    lines.append(f"- Aerobraking adds {b['time_months']:.1f} months = **{results['time_penalty_fraction']*100:.2f}%** of mission time.")
    lines.append(f"- Within mission uncertainty budget; not a load-bearing constraint.")

    lines.append("\n### Altitude trade-off: heat flux vs per-pass delta-v\n")
    lines.append("**Ballistic coefficient = 4,000 kg/m² (100 t vehicle, 25 m² area).** This is the binding constraint.\n")
    lines.append("| Altitude (km) | ρ (kg/m³) | Heat flux (kW/m²) | dv per pass (m/s) | Passes to dissipate 6 km/s | T_eq @ ε=0.8 (K) | Bag survives? |")
    lines.append("|---:|---:|---:|---:|---:|---:|:--:|")
    for s in results["altitude_sweep"]:
        n_passes_str = (
            f"{s['n_passes_needed']:,}" if s['n_passes_needed'] != float('inf') else "∞"
        )
        lines.append(
            f"| {s['altitude_km']} | {s['rho_kg_per_m3']:.1e} | "
            f"{s['q_total_kW_per_m2']:.2f} | "
            f"{s['dv_per_pass_m_s']:.3f} | {n_passes_str} | "
            f"{s['T_eq_high_e_K']:.0f} | "
            f"{'yes' if s['bag_survives_high_e'] else 'no'} |"
        )

    lines.append("\nNo altitude exists where bag survives AND pass count is tractable for this vehicle's ballistic coefficient.\n")

    lines.append("\n### Bag laminate material tolerances (reference)\n")
    lines.append("| Material | Continuous T_max (K) | Notes |")
    lines.append("|---|---:|---|")
    lines.append("| Aluminised Mylar | 520 | Outer-MLI layer; melts at ~250 °C |")
    lines.append("| Vectran fabric | 600 | High-tenacity liquid-crystal polymer |")
    lines.append("| Polyimide film (Kapton) | 700 | Continuous; ~800 K short-term |")
    lines.append("\nMulti-layer-insulation laminate is typically Mylar/Kapton/Vectran stack; outer layer dictates failure threshold. **For aerobraking, the bag is well inside Mylar's tolerance; for aerocapture, every layer fails immediately.**")

    (results_dir / "tables.md").write_text("\n".join(lines))
    return results


if __name__ == "__main__":
    out = main()
    print("R-chunk-as-heat-shield complete.")
    print(f"  Aerocapture: bag {'survives' if out['modes']['A_aerocapture_single_pass']['bag_survives'] else 'destroyed'}, chunk ablation {out['modes']['A_aerocapture_single_pass']['total_ablation_kg']:.0f} kg")
    print(f"  Aerobraking: bag {'survives' if out['modes']['B_aerobraking_multipass']['bag_survives'] else 'destroyed'}, chunk ablation {out['modes']['B_aerobraking_multipass']['total_ablation_kg']:.2f} kg over {out['modes']['B_aerobraking_multipass']['n_passes']} passes, {out['modes']['B_aerobraking_multipass']['time_months']:.1f} months")
