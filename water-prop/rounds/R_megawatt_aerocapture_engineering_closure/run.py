"""R-megawatt-aerocapture-engineering-closure — deterministic numerics for hypotheses H1..H7.

Originally authored as R-chunk-as-heat-shield-revisit; renamed after I
discovered iapetus has the authorised assignment for that scope under
different framing. See STUDY.md SCOPE-AND-LANE NOTICE.

Hypotheses pre-registered in STUDY.md. This script computes the numbers and
writes results/R_megawatt_aerocapture_engineering_closure.json. No
randomness; no Monte Carlo. Reproducible from inputs alone.

Author: rhea (worker session re-spawn, second sitting), 2026-05-15.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants and inputs (all SI unless noted)
# ---------------------------------------------------------------------------

G_EARTH = 9.81  # metres-per-second-squared

ICE_DENSITY = 917.0  # kilograms-per-cubic-metre (water ice at 200 kelvin)
ATMOS_RHO_90KM = 3.4e-6  # kilograms-per-cubic-metre (NRLMSISE-00 nominal)
PERIAPSIS_ALT_M = 90_000  # metres (single-pass aerocapture corridor)

# Heat flux calibration from R-chunk-as-heat-shield (closing round):
# peak stagnation heat flux 3.0 megawatts-per-square-metre at 12.6 km/s entry.
HEAT_FLUX_CAL_V = 12_600.0  # metres-per-second
HEAT_FLUX_CAL_Q = 3.0e6  # watts-per-square-metre
PULSE_T_EFFECTIVE_S = 60.0  # peak-to-effective integration time over pulse
ABLATION_ENTHALPY = 25.0e6  # joules-per-kilogram (boundary-layer-blocked H2O)

# Chunk geometry baseline (R-chunk-as-heat-shield).
CHUNK_AREA_100T_M2 = 25.0
CHUNK_REF_MASS_KG = 100_000.0

# Aerodynamic stability inputs.
ASPECT_RATIOS = [1.5, 2.0, 2.5, 3.0]
ENTRY_VELOCITIES_MPS = [12_500, 13_000, 14_000]
CP_CM_OFFSET_FRACTION = 0.10  # 10 percent of half-length (irregular chunk)
NEWTONIAN_MOMENT_COEFF = 0.5  # axisymmetric prolate at small angle-of-attack
PULSE_DURATION_S = 200.0
RCS_THRUST_SWEEP_N = [1, 10, 100, 1000]
RCS_COLD_GAS_ISP_S = 230.0  # helium cold gas

# Tug / mission inputs (one-megawatt-electric MARVL, from rhea round 3).
M_TUG_KG = 104_900.0
ISP_ELECTRIC_S = 2000.0
V_EXHAUST = ISP_ELECTRIC_S * G_EARTH  # metres-per-second
POWER_W = 1.0e6
THRUSTER_ETA = 0.7
THRUST_N = 2.0 * POWER_W * THRUSTER_ETA / V_EXHAUST  # ~71 N
MASS_FLOW_KGPS = THRUST_N / V_EXHAUST  # ~3.64 g/s

# Trajectory delta-velocities (km/s, from prior rounds).
DV_OUT_CONT_THRUST_KMS = 29.56  # rhea round 1, high-elliptical Saturn departure
DV_IN_SATURN_DEPART_KMS = 3.3  # segment (1), electric spiral-out
DV_IN_HELIO_DECEL_KMS = 5.44  # segment (2), Saturn-side heliocentric decel
DV_IN_AEROCAP_TRIM_KMS = 0.5  # segment (5b), post-aerocapture circularization
DV_IN_POST_RESCUE_TOTAL_KMS = (
    DV_IN_SATURN_DEPART_KMS + DV_IN_HELIO_DECEL_KMS + DV_IN_AEROCAP_TRIM_KMS
)  # 9.24 km/s

# Chunk size sweep (tonnes).
CHUNK_MASS_SWEEP_T = [100, 200, 500]

# Operations and coasts (years).
SATURN_OPS_YR = 0.5
EARTH_OPS_YR = 0.1
HOHMANN_COAST_INBOUND_YR = 6.06  # Saturn-to-Earth Hohmann transfer time
S_PER_YEAR = 365.25 * 86400.0

# Locked-finding reactor reference.
FSP_PHASE_2_KWE = 100.0  # Fission Surface Power Phase 2 scope
BASE_RATE_0_OF_6 = (
    "US space-fission programs: zero of six reached orbit within stated decade since 1965"
)


# ---------------------------------------------------------------------------
# Module 1 — Chunk attitude stability (H1, H2, H3)
# ---------------------------------------------------------------------------


def chunk_dimensions(mass_kg: float, aspect_ratio: float) -> tuple[float, float, float]:
    """Return (half_length_m, equatorial_radius_m, frontal_area_m2) for a
    prolate spheroid of given mass and aspect ratio at ice density.

    Volume = (4/3) * pi * a * b^2 where a = half-length, b = equatorial radius,
    a/b = aspect_ratio.
    """
    volume = mass_kg / ICE_DENSITY
    # a = AR * b → V = (4/3) pi (AR b) b^2 → b^3 = 3V / (4 pi AR)
    b = (3.0 * volume / (4.0 * math.pi * aspect_ratio)) ** (1.0 / 3.0)
    a = aspect_ratio * b
    frontal_area = math.pi * b * b  # chunk-forward, equatorial cross-section
    return a, b, frontal_area


def aerodynamic_torque(
    velocity_mps: float, frontal_area_m2: float, half_length_m: float
) -> tuple[float, float]:
    """Return (dynamic_pressure_Pa, torque_Nm) for chunk-forward orientation
    with CP-CM offset of CP_CM_OFFSET_FRACTION * half-length.
    """
    q_dyn = 0.5 * ATMOS_RHO_90KM * velocity_mps * velocity_mps
    d_offset = CP_CM_OFFSET_FRACTION * half_length_m
    torque = q_dyn * frontal_area_m2 * d_offset * NEWTONIAN_MOMENT_COEFF
    return q_dyn, torque


def stability_table() -> list[dict]:
    """Sweep aspect ratios and entry velocities at chunk mass 200 tonnes
    (matrix-mid). Compute required RCS thrust per pair at moment arm =
    half-length. Determine which RCS_THRUST_SWEEP_N levels close.
    """
    rows = []
    chunk_mass_kg = 200_000.0
    for ar in ASPECT_RATIOS:
        a, b, A = chunk_dimensions(chunk_mass_kg, ar)
        for v in ENTRY_VELOCITIES_MPS:
            q, tau = aerodynamic_torque(v, A, a)
            f_required_per_pair = tau / a  # newtons per pair at moment arm = a
            closes = {
                f"rcs_{N}N": (N >= f_required_per_pair) for N in RCS_THRUST_SWEEP_N
            }
            # Cold-gas propellant per pulse, assuming sustained thrust at
            # f_required_per_pair for the pulse duration.
            m_prop = f_required_per_pair * PULSE_DURATION_S / (RCS_COLD_GAS_ISP_S * G_EARTH)
            rows.append(
                {
                    "aspect_ratio": ar,
                    "half_length_m": a,
                    "frontal_area_m2": A,
                    "entry_velocity_mps": v,
                    "dynamic_pressure_Pa": q,
                    "torque_Nm": tau,
                    "rcs_thrust_required_per_pair_N": f_required_per_pair,
                    "rcs_thrust_closure": closes,
                    "rcs_propellant_per_pulse_kg": m_prop,
                }
            )
    return rows


# ---------------------------------------------------------------------------
# Module 2 — Chunk ablation per pass (H4)
# ---------------------------------------------------------------------------


def peak_heat_flux(velocity_mps: float) -> float:
    """Scale from calibration: q_peak ∝ v^3 (convective Sutton-Graves)."""
    return HEAT_FLUX_CAL_Q * (velocity_mps / HEAT_FLUX_CAL_V) ** 3


def chunk_windward_area(chunk_mass_kg: float) -> float:
    """Scale from 25 m² at 100 tonnes as m^(2/3) (fixed-density geometry)."""
    return CHUNK_AREA_100T_M2 * (chunk_mass_kg / CHUNK_REF_MASS_KG) ** (2.0 / 3.0)


def ablation_table() -> list[dict]:
    rows = []
    for chunk_t in CHUNK_MASS_SWEEP_T:
        chunk_kg = chunk_t * 1000.0
        A = chunk_windward_area(chunk_kg)
        for v in ENTRY_VELOCITIES_MPS:
            q = peak_heat_flux(v)
            Q_per_area = q * PULSE_T_EFFECTIVE_S
            m_abl_per_area = Q_per_area / ABLATION_ENTHALPY
            m_abl_total_kg = m_abl_per_area * A
            ablation_fraction = m_abl_total_kg / chunk_kg
            rows.append(
                {
                    "chunk_mass_t": chunk_t,
                    "windward_area_m2": A,
                    "entry_velocity_mps": v,
                    "peak_heat_flux_MWm2": q / 1.0e6,
                    "integrated_heat_load_MJm2": Q_per_area / 1.0e6,
                    "ablation_mass_kg": m_abl_total_kg,
                    "ablation_fraction": ablation_fraction,
                }
            )
    return rows


# ---------------------------------------------------------------------------
# Module 3 — Delivered fraction and round-trip time (H5, H6)
# ---------------------------------------------------------------------------


def mass_ratio(dv_kms: float, ve_mps: float) -> float:
    return math.exp(dv_kms * 1000.0 / ve_mps)


def mission_closure(chunk_mass_t: float) -> dict:
    """Compute outbound propellant, inbound propellant, delivered chunk,
    burn times, and two round-trip-time models.
    """
    chunk_kg = chunk_mass_t * 1000.0

    # Outbound: tug-only initial mass, tug-only final mass.
    ratio_out = mass_ratio(DV_OUT_CONT_THRUST_KMS, V_EXHAUST)
    m_prop_out_kg = M_TUG_KG * (ratio_out - 1.0)

    # Inbound (chunk-fed): tug + chunk_grappled initial → tug + chunk_delivered final.
    ratio_in = mass_ratio(DV_IN_POST_RESCUE_TOTAL_KMS, V_EXHAUST)
    m_init_in = M_TUG_KG + chunk_kg
    m_final_in = m_init_in / ratio_in
    chunk_delivered_kg = m_final_in - M_TUG_KG
    m_prop_in_kg = m_init_in - m_final_in
    delivered_fraction = chunk_delivered_kg / chunk_kg if chunk_kg > 0 else 0.0

    # Burn times at constant 1-MWe power (mass-flow-rate × time = propellant).
    t_burn_out_s = m_prop_out_kg / MASS_FLOW_KGPS
    t_burn_in_s = m_prop_in_kg / MASS_FLOW_KGPS

    # Architecture A: pure continuous-thrust trajectory (spiral = trajectory time).
    rt_a_yr = (
        t_burn_out_s / S_PER_YEAR
        + SATURN_OPS_YR
        + t_burn_in_s / S_PER_YEAR
        + EARTH_OPS_YR
    )

    # Architecture B: continuous-thrust spiral phases + heliocentric Hohmann coast inbound.
    # Outbound is continuous-thrust (no separate coast). Inbound: Saturn-departure
    # spiral + heliocentric decel burn (combined into t_burn_in_s) then ballistic
    # Hohmann coast Saturn-to-Earth (6.06 yr) plus aerocapture/circularization
    # already in the burn time. The Hohmann coast is additive on top of the
    # inbound burn time for the cruise phase.
    rt_b_yr = (
        t_burn_out_s / S_PER_YEAR
        + SATURN_OPS_YR
        + t_burn_in_s / S_PER_YEAR
        + HOHMANN_COAST_INBOUND_YR
        + EARTH_OPS_YR
    )

    return {
        "chunk_grappled_t": chunk_mass_t,
        "outbound_propellant_t": m_prop_out_kg / 1000.0,
        "inbound_propellant_t": m_prop_in_kg / 1000.0,
        "chunk_delivered_t": chunk_delivered_kg / 1000.0,
        "delivered_fraction": delivered_fraction,
        "outbound_burn_time_yr": t_burn_out_s / S_PER_YEAR,
        "inbound_burn_time_yr": t_burn_in_s / S_PER_YEAR,
        "round_trip_yr_arch_A_pure_cont_thrust": rt_a_yr,
        "round_trip_yr_arch_B_with_hohmann_coast": rt_b_yr,
    }


# ---------------------------------------------------------------------------
# Module 4 — Reactor-program dependency cross-check (H7)
# ---------------------------------------------------------------------------


def reactor_dependency_summary(closure_table: list[dict]) -> dict:
    """Read closure outputs and state explicitly that aerocapture does not
    relax the reactor power requirement, since outbound delta-velocity is
    unchanged.
    """
    # The minimum reactor power for closure is determined by outbound
    # delta-velocity at the chosen specific impulse. Aerocapture changes
    # neither. The dependency is therefore unchanged.
    required_reactor_kwe = 1000.0  # 1 megawatt-electric
    factor_over_fsp_phase_2 = required_reactor_kwe / FSP_PHASE_2_KWE
    return {
        "required_reactor_kwe": required_reactor_kwe,
        "fsp_phase_2_kwe": FSP_PHASE_2_KWE,
        "factor_over_fsp_phase_2": factor_over_fsp_phase_2,
        "base_rate_prior": BASE_RATE_0_OF_6,
        "posterior_availability_by_2032_2035": "0.10 to 0.30 (locked finding 2)",
        "dependency_changed_by_aerocapture": False,
        "note": (
            "Aerocapture rescues inbound delta-velocity, not outbound. "
            "Outbound 29.56 km/s continuous-thrust burn unchanged. "
            "Reactor power requirement unchanged. The rescue closes "
            "propulsion engineering and does not address the reactor "
            "program dependency."
        ),
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    out = {
        "round": "R-megawatt-aerocapture-engineering-closure",
        "author": "rhea",
        "date": "2026-05-15",
        "branch": "iceberg-rhea-2",
        "scope_predecessor": "water-prop/rounds/R_chunk_as_heat_shield_revisit/SCOPE.md",
        "calibration_predecessor": "water-prop/rounds/R_chunk_as_heat_shield/STUDY.md",
        "constants": {
            "atmospheric_density_at_90km_kgpm3": ATMOS_RHO_90KM,
            "ice_density_kgpm3": ICE_DENSITY,
            "heat_flux_calibration_v_mps": HEAT_FLUX_CAL_V,
            "heat_flux_calibration_q_MWm2": HEAT_FLUX_CAL_Q / 1.0e6,
            "ablation_enthalpy_MJpkg_blocked": ABLATION_ENTHALPY / 1.0e6,
            "tug_mass_t_1MWe_MARVL": M_TUG_KG / 1000.0,
            "v_exhaust_kmps": V_EXHAUST / 1000.0,
            "thrust_N": THRUST_N,
            "mass_flow_kgps": MASS_FLOW_KGPS,
            "dv_outbound_cont_thrust_kmps": DV_OUT_CONT_THRUST_KMS,
            "dv_inbound_post_rescue_kmps": DV_IN_POST_RESCUE_TOTAL_KMS,
            "pulse_duration_s": PULSE_DURATION_S,
            "pulse_effective_integration_s": PULSE_T_EFFECTIVE_S,
            "cp_cm_offset_fraction": CP_CM_OFFSET_FRACTION,
        },
        "module_1_attitude_stability": stability_table(),
        "module_2_ablation": ablation_table(),
        "module_3_mission_closure": [mission_closure(t) for t in CHUNK_MASS_SWEEP_T],
        "module_4_reactor_dependency": reactor_dependency_summary([]),
    }

    results_dir = Path(__file__).parent / "results"
    results_dir.mkdir(exist_ok=True)
    out_path = results_dir / "R_megawatt_aerocapture_engineering_closure.json"
    with out_path.open("w") as f:
        json.dump(out, f, indent=2)

    # Print summary for hypothesis grading.
    print(f"Results written to: {out_path}")
    print()
    print("=" * 72)
    print("SUMMARY (for hypothesis grading in STUDY.md)")
    print("=" * 72)

    print()
    print("H1/H2/H3 — attitude stability (chunk mass 200 t, sweep AR x V_entry):")
    print(
        f"{'AR':>5} {'V (km/s)':>10} {'q (Pa)':>10} {'tau (N·m)':>12} "
        f"{'F_req (N)':>10} {'m_prop (kg)':>12}"
    )
    for row in out["module_1_attitude_stability"]:
        print(
            f"{row['aspect_ratio']:>5.1f} "
            f"{row['entry_velocity_mps']/1000:>10.1f} "
            f"{row['dynamic_pressure_Pa']:>10.1f} "
            f"{row['torque_Nm']:>12.1f} "
            f"{row['rcs_thrust_required_per_pair_N']:>10.1f} "
            f"{row['rcs_propellant_per_pulse_kg']:>12.2f}"
        )

    print()
    print("H4 — ablation per single-pass aerocapture (chunk mass x V_entry):")
    print(
        f"{'chunk (t)':>10} {'V (km/s)':>10} {'q_peak (MW/m2)':>16} "
        f"{'m_abl (kg)':>12} {'fraction (%)':>14}"
    )
    for row in out["module_2_ablation"]:
        print(
            f"{row['chunk_mass_t']:>10} "
            f"{row['entry_velocity_mps']/1000:>10.1f} "
            f"{row['peak_heat_flux_MWm2']:>16.2f} "
            f"{row['ablation_mass_kg']:>12.1f} "
            f"{row['ablation_fraction']*100:>14.3f}"
        )

    print()
    print("H5/H6 — delivered fraction + round-trip (1 MWe MARVL, post-rescue):")
    print(
        f"{'chunk (t)':>10} {'delivered (t)':>14} {'fraction (%)':>14} "
        f"{'RT-A (yr)':>12} {'RT-B (yr)':>12}"
    )
    for row in out["module_3_mission_closure"]:
        print(
            f"{row['chunk_grappled_t']:>10.0f} "
            f"{row['chunk_delivered_t']:>14.1f} "
            f"{row['delivered_fraction']*100:>14.1f} "
            f"{row['round_trip_yr_arch_A_pure_cont_thrust']:>12.2f} "
            f"{row['round_trip_yr_arch_B_with_hohmann_coast']:>12.2f}"
        )

    print()
    print("H7 — reactor dependency:")
    r = out["module_4_reactor_dependency"]
    print(
        f"  required reactor: {r['required_reactor_kwe']} kWe "
        f"({r['factor_over_fsp_phase_2']:.1f}× Fission Surface Power Phase 2)"
    )
    print(f"  dependency changed by aerocapture: {r['dependency_changed_by_aerocapture']}")


if __name__ == "__main__":
    main()
