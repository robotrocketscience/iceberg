"""R-HE-graze-feasibility — physical check on Case HE-graze from R-multi-chunk-departure-orbit.

Tests whether a high-elliptical Saturn orbit grazing the B-ring at periapsis
can soft-capture chunks. Computes:
- Relative velocity at periapsis between spacecraft and ring particles
- Kinetic energy of capture impact at that velocity
- Circularisation delta-velocity required to soft-capture
- Periapsis-pass duration

Conclusion grade against pre-registered H-hgf-a..f.
"""

from __future__ import annotations

import math
import json
from pathlib import Path

ROUND_DIR = Path(__file__).resolve().parent
RESULTS_DIR = ROUND_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)


# Constants
GM_SATURN = 3.793e7        # km³/s²
B_RING_INNER_KM = 92000.0
B_RING_OUTER_KM = 117500.0

# Reference HE-graze orbit
R_PERIAPSIS_KM = 105000.0  # mid-B-ring
R_APOAPSIS_KM = 1_000_000.0

# Chunk mass for kinetic-energy calculation
CHUNK_MASS_T = 482.0

# Bag soft-capture limits (engineering rough order)
BAG_ENERGY_ABSORPTION_J_LIMITS = {
    "conservative_10MJ": 10e6,
    "moderate_100MJ":    100e6,
    "aspirational_1GJ":  1e9,
}


def orbital_velocity_at_r(r_km: float, a_km: float) -> float:
    """vis-viva: v² = GM(2/r − 1/a)"""
    return math.sqrt(GM_SATURN * (2.0 / r_km - 1.0 / a_km))


def circular_velocity_at_r(r_km: float) -> float:
    return math.sqrt(GM_SATURN / r_km)


def orbital_period_s(a_km: float) -> float:
    return 2 * math.pi * math.sqrt(a_km ** 3 / GM_SATURN)


def time_in_radial_range(r_p_km: float, r_a_km: float, r_max_km: float) -> float:
    """Time spent at radius ∈ [r_p, r_max] in one orbit (both periapsis crossing).

    For r_p < r_max <= r_a, the spacecraft is in this radial range twice per orbit
    (once descending toward periapsis, once ascending). Use Kepler's equation.
    """
    a = (r_p_km + r_a_km) / 2.0
    e = (r_a_km - r_p_km) / (r_a_km + r_p_km)
    p = a * (1 - e * e)  # semi-latus rectum

    # True anomaly at r_max: r = p / (1 + e cos θ) → cos θ = (p/r - 1)/e
    cos_theta = (p / r_max_km - 1.0) / e
    cos_theta = max(-1.0, min(1.0, cos_theta))
    theta_max = math.acos(cos_theta)  # rad, in [0, π]

    # Eccentric anomaly: tan(E/2) = sqrt((1-e)/(1+e)) tan(θ/2)
    E = 2 * math.atan2(math.sqrt(1 - e) * math.sin(theta_max / 2),
                        math.sqrt(1 + e) * math.cos(theta_max / 2))
    # Mean anomaly: M = E − e sin E
    M_max = E - e * math.sin(E)

    T = orbital_period_s(a)
    # Time from periapsis to true anomaly θ_max: T × M_max / (2π)
    # Time spent at r ∈ [r_p, r_max] is 2 × that (symmetric around periapsis)
    t_in_range = 2 * T * M_max / (2 * math.pi)
    return t_in_range


def main() -> None:
    # 1. Orbital geometry
    a = (R_PERIAPSIS_KM + R_APOAPSIS_KM) / 2.0
    e = (R_APOAPSIS_KM - R_PERIAPSIS_KM) / (R_APOAPSIS_KM + R_PERIAPSIS_KM)
    T = orbital_period_s(a)

    # 2. Velocities at periapsis
    v_p_spacecraft = orbital_velocity_at_r(R_PERIAPSIS_KM, a)
    v_p_particle = circular_velocity_at_r(R_PERIAPSIS_KM)
    v_rel = abs(v_p_spacecraft - v_p_particle)

    # 3. Kinetic energy of impact
    chunk_mass_kg = CHUNK_MASS_T * 1000.0
    v_rel_m_s = v_rel * 1000.0
    KE_J = 0.5 * chunk_mass_kg * v_rel_m_s ** 2

    # 4. Circularisation delta-velocity (same as relative velocity, magnitude-wise)
    dv_circ_km_s = v_rel

    # 5. Maximum v_rel at which bag can absorb the energy
    max_v_rel = {}
    for label, E_lim in BAG_ENERGY_ABSORPTION_J_LIMITS.items():
        v_max_m_s = math.sqrt(2 * E_lim / chunk_mass_kg)
        max_v_rel[label] = round(v_max_m_s, 1)  # m/s

    # 6. Periapsis-pass duration
    t_in_upper_b_ring_s = time_in_radial_range(R_PERIAPSIS_KM, R_APOAPSIS_KM, B_RING_OUTER_KM)

    # 7. Sweep over apoapsis to see how relative velocity changes
    apoapsis_sweep_km = [200000, 500000, 1_000_000, 2_000_000, 5_000_000]
    apoapsis_table = []
    for r_a in apoapsis_sweep_km:
        a_sweep = (R_PERIAPSIS_KM + r_a) / 2
        v_sc = orbital_velocity_at_r(R_PERIAPSIS_KM, a_sweep)
        v_rel_sweep = abs(v_sc - v_p_particle)
        KE_sweep = 0.5 * chunk_mass_kg * (v_rel_sweep * 1000.0) ** 2
        T_sweep = orbital_period_s(a_sweep)
        t_in_ring = time_in_radial_range(R_PERIAPSIS_KM, r_a, B_RING_OUTER_KM)
        apoapsis_table.append({
            "r_apoapsis_km": r_a,
            "v_spacecraft_periapsis_km_s": round(v_sc, 2),
            "v_relative_km_s": round(v_rel_sweep, 2),
            "kinetic_energy_TJ_for_482t": round(KE_sweep / 1e12, 2),
            "orbital_period_days": round(T_sweep / 86400.0, 2),
            "time_in_upper_b_ring_minutes": round(t_in_ring / 60.0, 1),
        })

    # Pre-registration grading
    grading = grade_predictions(v_rel, KE_J, max_v_rel, dv_circ_km_s, t_in_upper_b_ring_s)

    result = {
        "reference_orbit": {
            "r_periapsis_km": R_PERIAPSIS_KM,
            "r_apoapsis_km": R_APOAPSIS_KM,
            "semi_major_axis_km": a,
            "eccentricity": round(e, 3),
            "period_days": round(T / 86400.0, 2),
        },
        "velocities": {
            "v_p_spacecraft_km_s": round(v_p_spacecraft, 2),
            "v_p_b_ring_particle_km_s": round(v_p_particle, 2),
            "v_relative_km_s": round(v_rel, 2),
        },
        "impact_kinetic_energy_for_482t_chunk": {
            "joules": round(KE_J, 0),
            "terajoules": round(KE_J / 1e12, 2),
            "equivalent_tons_tnt": round(KE_J / 4.184e9, 1),
        },
        "circularisation_dv_km_s": round(dv_circ_km_s, 2),
        "max_v_rel_for_bag_capture_m_s": max_v_rel,
        "periapsis_pass_duration_minutes": round(t_in_upper_b_ring_s / 60.0, 1),
        "apoapsis_sweep": apoapsis_table,
        "grading": grading,
        "constants": {
            "GM_saturn_km3_s2": GM_SATURN,
            "b_ring_inner_km": B_RING_INNER_KM,
            "b_ring_outer_km": B_RING_OUTER_KM,
            "chunk_mass_t": CHUNK_MASS_T,
            "bag_energy_absorption_J_limits": BAG_ENERGY_ABSORPTION_J_LIMITS,
        },
    }

    with (RESULTS_DIR / "he_graze_check.json").open("w") as f:
        json.dump(result, f, indent=2)

    print("\nHE-graze reference orbit (periapsis 105k km, apoapsis 1M km):")
    print(f"  Spacecraft velocity at periapsis: {v_p_spacecraft:.2f} km/s")
    print(f"  B-ring particle velocity at periapsis: {v_p_particle:.2f} km/s")
    print(f"  Relative velocity: {v_rel:.2f} km/s")
    print(f"  Orbital period: {T/86400:.2f} days")
    print(f"  Time in upper B-ring per pass: {t_in_upper_b_ring_s/60:.1f} minutes")
    print(f"\nImpact kinetic energy for 482-tonne chunk at relative velocity {v_rel:.2f} km/s:")
    print(f"  KE = {KE_J:.2e} J = {KE_J/1e12:.2f} terajoules = {KE_J/4.184e9:.1f} tons TNT equivalent")
    print(f"\nCircularisation delta-velocity required: {dv_circ_km_s:.2f} km/s")
    print(f"  (Identical to relative velocity — a periapsis prograde-retrograde burn to match particle orbit)")
    print(f"\nMaximum relative velocity for soft-capture (482-tonne chunk):")
    for label, v in max_v_rel.items():
        print(f"  {label}: {v:.1f} m/s")
    print(f"\nApoapsis sweep — relative velocity vs apoapsis:")
    print(f"{'apoapsis (km)':>14} {'v_rel (km/s)':>13} {'KE (TJ)':>10} {'period (days)':>14} {'time in upper B-ring (min)':>28}")
    for row in apoapsis_table:
        print(f"{row['r_apoapsis_km']:>14,} {row['v_relative_km_s']:>13.2f} {row['kinetic_energy_TJ_for_482t']:>10.2f} {row['orbital_period_days']:>14.2f} {row['time_in_upper_b_ring_minutes']:>28.1f}")

    print("\nPre-registration grading:")
    for hid, g in grading.items():
        print(f"  {hid}: {g['verdict']:<25} — {g['note']}")


def grade_predictions(v_rel_km_s, KE_J, max_v_rel_dict, dv_circ_km_s, t_pass_s):
    out = {}

    def grade_range(obs, lo, hi, flo, fhi):
        if lo <= obs <= hi:
            return "held"
        if flo <= obs <= fhi:
            return "wrong-but-informative"
        return "wrong-and-load-bearing"

    # H-hgf-a: v_rel ∈ [7, 8] km/s; falsified outside [5, 10]
    out["H-hgf-a"] = {"observed_km_s": round(v_rel_km_s, 2),
                       "predicted_km_s": [7, 8],
                       "verdict": grade_range(v_rel_km_s, 7, 8, 5, 10),
                       "note": f"relative velocity at HE-graze periapsis: {v_rel_km_s:.2f} km/s"}

    # H-hgf-b: KE ∈ [10, 15] TJ
    KE_TJ = KE_J / 1e12
    out["H-hgf-b"] = {"observed_TJ": round(KE_TJ, 2),
                       "predicted_TJ": [10, 15],
                       "verdict": grade_range(KE_TJ, 10, 15, 5, 25),
                       "note": f"capture kinetic energy at 482 t chunk: {KE_TJ:.2f} TJ"}

    # H-hgf-c: max v_rel for bag capture < 100 m/s (under moderate 100MJ bag limit)
    v_max = max_v_rel_dict["moderate_100MJ"]
    held = v_max < 1000  # if bag can tolerate > 1 km/s, falsified
    out["H-hgf-c"] = {"observed_m_s": v_max,
                       "predicted_below_m_s": 100,
                       "verdict": "held" if v_max < 100 else ("wrong-but-informative" if v_max < 1000 else "falsified"),
                       "note": f"max v_rel for moderate (100 MJ) bag capture: {v_max:.1f} m/s"}

    # H-hgf-d: circularisation delta-velocity ∈ [6, 8] km/s
    out["H-hgf-d"] = {"observed_km_s": round(dv_circ_km_s, 2),
                       "predicted_km_s": [6, 8],
                       "verdict": grade_range(dv_circ_km_s, 6, 8, 5, 10),
                       "note": f"circularisation delta-velocity from HE-graze to B-ring circular: {dv_circ_km_s:.2f} km/s"}

    # H-hgf-e: periapsis-pass duration ∈ [90, 150] min
    t_min = t_pass_s / 60.0
    out["H-hgf-e"] = {"observed_minutes": round(t_min, 1),
                       "predicted_minutes": [90, 150],
                       "verdict": grade_range(t_min, 90, 150, 60, 200),
                       "note": f"time in upper B-ring per pass: {t_min:.1f} minutes"}

    # H-hgf-f: HE-graze falsified as operational mode for soft capture
    # held = (v_rel >> bag capacity AND no obvious workaround)
    bag_max = max_v_rel_dict["aspirational_1GJ"]  # aspirational limit
    falsified = v_rel_km_s * 1000.0 > bag_max
    out["H-hgf-f"] = {"v_rel_m_s": round(v_rel_km_s * 1000, 0),
                       "aspirational_bag_max_m_s": bag_max,
                       "verdict": "held" if falsified else "needs-investigation",
                       "note": f"HE-graze v_rel ({v_rel_km_s*1000:.0f} m/s) exceeds aspirational bag tolerance ({bag_max:.0f} m/s) by factor {v_rel_km_s*1000/bag_max:.1f}× — falsified as soft-capture mode"
                            if falsified else "v_rel within bag tolerance — operational mode plausibly accessible"}

    return out


if __name__ == "__main__":
    main()
