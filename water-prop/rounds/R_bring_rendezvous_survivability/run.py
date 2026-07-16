#!/usr/bin/env python3
"""R-bring-rendezvous-survivability.

Does engineered survivability (bag-armour, particle-cull mesh, off-plane
geometry, slow-cross) close the 99-percent-per-pass impact-prob gap on
B-ring rendezvous crossings?

Pre-registration in STUDY.md. SCOPE-input audit applied (lesson 9): four
input-assumption issues called out before the sweep, central anchors
computed BOE-first.

Deterministic. No Monte Carlo. Output: results/R_bring_rendezvous_survivability.json
+ stdout-printable tables. Run from this directory or project root.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants — Saturn / B-ring geometry
# ---------------------------------------------------------------------------

GM_SATURN_KM3_S2 = 3.793e7              # standard gravitational parameter
R_SATURN_KM = 60_268.0                  # 1 bar reference
R_TITAN_ORBIT_KM = 1_221_870.0          # Titan semimajor axis
R_BRING_OUTER_KM = 117_580.0
R_BRING_INNER_KM = 92_000.0

R_RENDEZVOUS_PERIAPSIS_KM = 100_000.0   # SCOPE anchor
R_CAPTURE_APOAPSIS_KM = R_TITAN_ORBIT_KM
INCLINATION_HOHMANN_DEG = 26.7          # SCOPE anchor (Earth-to-Saturn equator)

# Per-crossing impact-probability target (per SCOPE method body 1).
# L0-10 0.8 rolling-5-mission reliability; allocated conservatively across 9
# ring-plane crossings + all other failure modes; 1e-4 per crossing.
TARGET_P_IMPACT_PER_CROSSING = 1.0e-4
TARGET_P_IMPACT_TWO_CROSSINGS = 1.0 - (1.0 - TARGET_P_IMPACT_PER_CROSSING) ** 2

# Mass-budget closure threshold (per SCOPE method body 4).
TARGET_MASS_PENALTY_FRACTION = 0.10

# Vehicle baseline (anchor on Variant-B / chunk-rendezvous architecture).
BAG_APERTURE_M2_DEFAULT = 100.0
VARIANT_B_DRY_MASS_T = 64.0             # tug dry mass per matrix Variant-B baseline
CHUNK_MASS_T_BASELINE = 200.0           # L1-007 cap
VEHICLE_TOTAL_BASELINE_T = VARIANT_B_DRY_MASS_T + CHUNK_MASS_T_BASELINE  # 264 t

# Specific impulses for Δv → mass-penalty conversion.
ISP_VARIANT_B_S = 5000.0                # megawatt-electric
ISP_CHEMICAL_S = 450.0                  # H2/O2 trim
G0_M_S2 = 9.80665

# ---------------------------------------------------------------------------
# B-ring tau zones (per fine-structure H1 + H3 verdicts; titan SOI body 3)
# ---------------------------------------------------------------------------
# Each zone: (label, r_km, tau_total, fraction_unshieldable_>1cm, chunk_availability)
# fraction_unshieldable per fine-structure H3: ~75% of tau is in particles >1cm.
# chunk_availability: "rich" (chunks plentiful), "moderate", "thin", "sparse",
# "none" (no large particles per fine-structure H1 / H2).

# Chunk-availability per fine-structure H1+H2 verdicts:
#   "rich"   = large chunks (>1m) are abundant; ICEBERG can harvest 200t chunk
#   "thin"   = few chunks, mostly dust drift from inner B-ring
#   "sparse" = essentially empty of large chunks
#   "none"   = no large particles (per fine-structure H2: Cassini Div gaps
#              including outer plateau contain few/no large particles, only
#              dust; the dense ringlets WITHIN Cassini Div at tau=0.30 have
#              chunks but are not safe-passage zones)
TAU_ZONES = [
    ("B-ring zone-avg",            100_000.0, 2.0,    0.75, "rich"),
    ("B3 core",                    107_000.0, 4.5,    0.75, "rich"),
    ("B-ring outer 580 km",        117_000.0, 0.40,   0.75, "rich"),
    ("Huygens Ringlet (in gap)",   117_900.0, 0.30,   0.75, "rich"),
    ("B-ring outermost 180 km",    117_400.0, 0.10,   0.75, "thin"),
    ("B-ring outermost 80 km",     117_500.0, 0.03,   0.75, "sparse"),
    ("Cassini Div outer plateau",  120_000.0, 0.04,   0.75, "none"),
    ("Huygens Gap",                117_680.0, 0.001,  0.75, "none"),
    ("Laplace Gap",                121_850.0, 0.001,  0.75, "none"),
]

# ---------------------------------------------------------------------------
# Helper: orbital mechanics
# ---------------------------------------------------------------------------

def vis_viva_v_kms(r_km: float, a_km: float) -> float:
    """Vehicle speed at radius r on orbit with semi-major a."""
    return math.sqrt(GM_SATURN_KM3_S2 * (2.0 / r_km - 1.0 / a_km))


def v_circular_kms(r_km: float) -> float:
    """Circular orbital speed at radius r."""
    return math.sqrt(GM_SATURN_KM3_S2 / r_km)


def edelbaum_dv_kms(v_at_burn_kms: float, delta_inc_deg: float) -> float:
    """Impulsive plane change Δv at given orbital speed.

    Δv = 2 v sin(Δi/2). Cheapest at apoapsis (lowest v).
    """
    return 2.0 * v_at_burn_kms * math.sin(math.radians(delta_inc_deg) / 2.0)


def mass_ratio_from_dv(delta_v_kms: float, isp_s: float) -> float:
    """Mass ratio (initial/final) for given Δv and Isp."""
    ve_kms = isp_s * G0_M_S2 / 1000.0
    return math.exp(delta_v_kms / ve_kms)


def propellant_mass_t(dry_t: float, delta_v_kms: float, isp_s: float) -> float:
    """Propellant mass needed to give dry-mass `dry_t` a Δv of `delta_v_kms`."""
    mr = mass_ratio_from_dv(delta_v_kms, isp_s)
    return dry_t * (mr - 1.0)


# ---------------------------------------------------------------------------
# Helper: impact probability
# ---------------------------------------------------------------------------

def p_impact_per_pass(tau_eff: float, inclination_deg: float) -> float:
    """Beer-Lambert per-pass impact probability through ring-slab.

    P = 1 - exp(-tau_eff / sin(i))
    """
    if inclination_deg <= 0.0:
        return 1.0
    return 1.0 - math.exp(-tau_eff / math.sin(math.radians(inclination_deg)))


def tau_after_mesh(tau_total: float, frac_unshieldable: float, mesh_on: bool) -> float:
    """Effective optical depth seen by bag, after particle-cull mesh.

    Mesh removes the shieldable fraction (< 1 cm particles), leaving
    `frac_unshieldable * tau_total` as the >1cm flux that hits bag.
    """
    if not mesh_on:
        return tau_total
    return frac_unshieldable * tau_total


# ---------------------------------------------------------------------------
# Helper: armour
# ---------------------------------------------------------------------------

def armour_mass_t(areal_density_kg_m2: float, aperture_m2: float) -> float:
    return areal_density_kg_m2 * aperture_m2 / 1000.0


def whipple_ballistic_limit_cm(areal_density_kg_m2: float, v_normal_km_s: float) -> float:
    """Single-bumper Whipple ballistic limit (Christiansen 2003 simplified).

    d_crit ~ 5.24 (rho_a t_b)^(1/3) (v_n rho_p^(-1/2))^(-2/3) [cm]

    For typical multi-layer Whipple at ICEBERG aluminum bumper density.
    Treat areal density as combined bumper+rear-wall mass.
    Returns critical particle diameter in cm.
    """
    if areal_density_kg_m2 <= 0.0 or v_normal_km_s <= 0.0:
        return 0.0
    rho_p_g_cm3 = 2.5  # average ring particle (water-ice + silicate)
    # In SI: areal density already kg/m^2; v in km/s
    # Christiansen multi-layer eq form (simplified, see NASA-TM-2003-211930 eq 4):
    return 5.24 * (areal_density_kg_m2 / 100.0) ** (1.0 / 3.0) * (
        v_normal_km_s * rho_p_g_cm3 ** (-0.5)
    ) ** (-2.0 / 3.0)


def mesh_mass_t(aperture_m2: float, present: bool) -> float:
    return 0.005 * aperture_m2 if present else 0.0  # 5 kg/m^2 mesh


# ---------------------------------------------------------------------------
# Helper: relative velocity vehicle-to-ring particle
# ---------------------------------------------------------------------------

def vehicle_speed_at_periapsis_kms(r_p_km: float, r_a_km: float) -> float:
    a = 0.5 * (r_p_km + r_a_km)
    return vis_viva_v_kms(r_p_km, a)


def v_rel_to_ring_particle_kms(
    r_p_km: float, r_a_km: float, inclination_deg: float
) -> float:
    """Vehicle-to-ring-particle relative velocity at r_p, accounting for inclination.

    Vehicle on capture orbit (r_p, r_a) prograde; ring particle on circular
    orbit at r_p, equatorial. Vehicle velocity at periapsis is along
    velocity-direction in inclined orbital plane. In-plane component (relative
    to ring's equatorial frame) = v_p × cos(i); out-of-plane = v_p × sin(i).
    Ring particle moves at v_circ in equatorial prograde direction.
    """
    v_p = vehicle_speed_at_periapsis_kms(r_p_km, r_a_km)
    v_circ = v_circular_kms(r_p_km)
    v_in_plane = v_p * math.cos(math.radians(inclination_deg))
    v_out_plane = v_p * math.sin(math.radians(inclination_deg))
    dv_x = v_in_plane - v_circ
    return math.sqrt(dv_x ** 2 + v_out_plane ** 2)


# ---------------------------------------------------------------------------
# Body 1 — reproduce titan baseline
# ---------------------------------------------------------------------------

def reproduce_titan_baseline() -> dict:
    """Reproduce titan SOI body 3 line 186: P_impact at zone-avg B-ring τ=2.0,
    i=26.7°.
    """
    p = p_impact_per_pass(tau_eff=2.0, inclination_deg=INCLINATION_HOHMANN_DEG)
    return {
        "tau": 2.0,
        "inclination_deg": INCLINATION_HOHMANN_DEG,
        "csc_i": 1.0 / math.sin(math.radians(INCLINATION_HOHMANN_DEG)),
        "p_impact_per_pass": p,
        "titan_published": 0.9885,
        "match_within_pct": abs(p - 0.9885) / 0.9885 * 100.0,
    }


# ---------------------------------------------------------------------------
# Body 2 — single-lever sweeps
# ---------------------------------------------------------------------------

def sweep_armour() -> list[dict]:
    rows = []
    for areal in [0.0, 10.0, 50.0, 200.0]:
        for aperture in [50.0, 100.0, 200.0]:
            d_crit_at_6kms = whipple_ballistic_limit_cm(areal, 6.6)
            d_crit_at_residence = whipple_ballistic_limit_cm(areal, 0.01)
            mass_t = armour_mass_t(areal, aperture)
            rows.append(
                {
                    "areal_density_kg_m2": areal,
                    "aperture_m2": aperture,
                    "armour_mass_t": mass_t,
                    "armour_mass_pct_of_dry": mass_t / VARIANT_B_DRY_MASS_T * 100.0,
                    "ballistic_limit_cm_at_6.6kms": round(d_crit_at_6kms, 3),
                    "ballistic_limit_cm_at_0.01kms": round(d_crit_at_residence, 3),
                    "p_impact_unchanged_at_zoneavg_i26.7": p_impact_per_pass(
                        2.0, INCLINATION_HOHMANN_DEG
                    ),
                    "note": "armour does not reduce P_impact; only post-impact survival",
                }
            )
    return rows


def sweep_mesh() -> list[dict]:
    rows = []
    for tau, label in [(2.0, "B-ring zone-avg"), (0.10, "outer-200km"), (0.03, "outermost-80km")]:
        for mesh_on in [False, True]:
            tau_eff = tau_after_mesh(tau, 0.75, mesh_on)
            p = p_impact_per_pass(tau_eff, INCLINATION_HOHMANN_DEG)
            rows.append(
                {
                    "zone": label,
                    "tau_total": tau,
                    "mesh_on": mesh_on,
                    "tau_effective": tau_eff,
                    "p_impact_per_pass_at_i26.7": p,
                    "mesh_mass_t_at_100m2": mesh_mass_t(100.0, mesh_on),
                }
            )
    return rows


def sweep_inclination() -> list[dict]:
    rows = []
    v_apo = vis_viva_v_kms(R_CAPTURE_APOAPSIS_KM, 0.5 * (R_RENDEZVOUS_PERIAPSIS_KM + R_CAPTURE_APOAPSIS_KM))
    v_peri = vehicle_speed_at_periapsis_kms(R_RENDEZVOUS_PERIAPSIS_KM, R_CAPTURE_APOAPSIS_KM)
    for i_target in [26.7, 45.0, 60.0, 75.0, 90.0]:
        delta_inc = i_target - INCLINATION_HOHMANN_DEG
        dv_at_apo = edelbaum_dv_kms(v_apo, delta_inc)
        dv_at_peri = edelbaum_dv_kms(v_peri, delta_inc)
        # Round-trip = inbound to i_target + outbound back to ecliptic-Earth-return
        dv_round_trip_apo = 2.0 * dv_at_apo
        prop_VB = propellant_mass_t(VEHICLE_TOTAL_BASELINE_T, dv_round_trip_apo, ISP_VARIANT_B_S)
        prop_chem = propellant_mass_t(VEHICLE_TOTAL_BASELINE_T, dv_round_trip_apo, ISP_CHEMICAL_S)
        rows.append(
            {
                "i_target_deg": i_target,
                "delta_inc_deg": delta_inc,
                "v_apo_kms": v_apo,
                "v_peri_kms": v_peri,
                "dv_at_apoapsis_kms_one_way": dv_at_apo,
                "dv_at_periapsis_kms_one_way": dv_at_peri,
                "dv_round_trip_apoapsis_kms": dv_round_trip_apo,
                "propellant_mass_VariantB_Isp5000_t": prop_VB,
                "propellant_mass_chemical_Isp450_t": prop_chem,
                "prop_pct_VB": prop_VB / VEHICLE_TOTAL_BASELINE_T * 100.0,
                "prop_pct_chem": prop_chem / VEHICLE_TOTAL_BASELINE_T * 100.0,
                "p_impact_zoneavg_at_this_i": p_impact_per_pass(2.0, i_target),
                "p_impact_outer_180km_at_this_i": p_impact_per_pass(0.10, i_target),
                "p_impact_outermost_80km_at_this_i": p_impact_per_pass(0.03, i_target),
            }
        )
    return rows


def sweep_slow_cross() -> list[dict]:
    """Per audit 1: slowing does not change P_impact (geometric).

    Compute v_rel-to-ring-particle for vehicle slowed in Saturn frame,
    plus residence-class case (ring-orbit-match).
    """
    rows = []
    v_circ_ring = v_circular_kms(R_RENDEZVOUS_PERIAPSIS_KM)
    v_p_capture = vehicle_speed_at_periapsis_kms(R_RENDEZVOUS_PERIAPSIS_KM, R_CAPTURE_APOAPSIS_KM)
    # Case A: capture orbit (no slow), v_rel = vehicle - ring at periapsis
    # Case B: vehicle slowed prograde to v_target in Saturn frame at i=26.7°
    # Case C: residence-match (v = v_circ_ring, equatorial)
    for label, v_target_kms, mode in [
        ("capture-orbit (no slow)", v_p_capture, "capture"),
        ("slow to 20 km/s",          20.0, "slow"),
        ("slow to 15 km/s",          15.0, "slow"),
        ("slow to 10 km/s",          10.0, "slow"),
        ("slow to 5 km/s",            5.0, "slow"),
        ("ring-orbit match (residence)", v_circ_ring, "residence"),
    ]:
        if mode == "residence":
            v_rel = 0.010  # residence-class dispersion velocity ~10 m/s
            inc = 0.0
        else:
            inc = INCLINATION_HOHMANN_DEG if mode != "residence" else 0.0
            v_in = v_target_kms * math.cos(math.radians(inc))
            v_out = v_target_kms * math.sin(math.radians(inc))
            dv_x = v_in - v_circ_ring
            v_rel = math.sqrt(dv_x ** 2 + v_out ** 2)
        # Δv to slow from capture-orbit to v_target, then re-accelerate
        if mode == "capture":
            dv_round_trip = 0.0
        else:
            dv_round_trip = 2.0 * abs(v_p_capture - v_target_kms)
        # Per-impact KE for 1cm particle (m ~ 1.5g) at v_rel
        m_1cm_kg = 1.5e-3
        ke_per_impact_J = 0.5 * m_1cm_kg * (v_rel * 1000.0) ** 2
        prop_VB = propellant_mass_t(VEHICLE_TOTAL_BASELINE_T, dv_round_trip, ISP_VARIANT_B_S)
        rows.append(
            {
                "scenario": label,
                "v_target_kms_saturn_frame": v_target_kms,
                "v_rel_to_ring_particle_kms": round(v_rel, 3),
                "dv_round_trip_kms": round(dv_round_trip, 3),
                "ke_per_impact_1cm_particle_J": round(ke_per_impact_J, 1),
                "ke_above_whipple_threshold_10kJ": ke_per_impact_J > 1.0e4,
                "prop_VariantB_Isp5000_t": round(prop_VB, 1),
                "p_impact_unchanged_per_pass_zoneavg_i26.7": p_impact_per_pass(
                    2.0, INCLINATION_HOHMANN_DEG
                ),
                "note": "P_impact does not depend on velocity (geometric only)",
            }
        )
    return rows


# ---------------------------------------------------------------------------
# Body 3 — combined sweep
# ---------------------------------------------------------------------------

def sweep_combined() -> list[dict]:
    rows = []
    armour_levels_kg_m2 = [0.0, 50.0, 200.0]
    mesh_options = [False, True]
    inclinations_deg = [26.7, 60.0, 90.0]
    aperture_m2 = BAG_APERTURE_M2_DEFAULT

    v_apo = vis_viva_v_kms(R_CAPTURE_APOAPSIS_KM, 0.5 * (R_RENDEZVOUS_PERIAPSIS_KM + R_CAPTURE_APOAPSIS_KM))

    for tau_label, tau_r, tau_total, frac_unshield, chunk_avail in TAU_ZONES:
        for armour_kg_m2 in armour_levels_kg_m2:
            for mesh_on in mesh_options:
                for incl in inclinations_deg:
                    tau_eff = tau_after_mesh(tau_total, frac_unshield, mesh_on)
                    p_per_pass = p_impact_per_pass(tau_eff, incl)
                    p_two_crossings = 1.0 - (1.0 - p_per_pass) ** 2
                    delta_inc = incl - INCLINATION_HOHMANN_DEG
                    dv_round_trip = 2.0 * edelbaum_dv_kms(v_apo, delta_inc)
                    prop_t = propellant_mass_t(
                        VEHICLE_TOTAL_BASELINE_T, dv_round_trip, ISP_VARIANT_B_S
                    )
                    armour_t = armour_mass_t(armour_kg_m2, aperture_m2)
                    mesh_t = mesh_mass_t(aperture_m2, mesh_on)
                    total_penalty_t = prop_t + armour_t + mesh_t
                    penalty_frac = total_penalty_t / VEHICLE_TOTAL_BASELINE_T

                    closes_p = p_two_crossings <= TARGET_P_IMPACT_TWO_CROSSINGS
                    closes_mass = penalty_frac <= TARGET_MASS_PENALTY_FRACTION
                    chunks_present = chunk_avail in ("rich", "thin")
                    closes_all = closes_p and closes_mass and chunks_present

                    rows.append(
                        {
                            "tau_zone": tau_label,
                            "tau_zone_r_km": tau_r,
                            "tau_total": tau_total,
                            "armour_kg_m2": armour_kg_m2,
                            "mesh_on": mesh_on,
                            "inclination_deg": incl,
                            "tau_eff": round(tau_eff, 4),
                            "p_impact_per_pass": p_per_pass,
                            "p_impact_two_crossings": p_two_crossings,
                            "dv_round_trip_kms": round(dv_round_trip, 3),
                            "propellant_t": round(prop_t, 2),
                            "armour_t": round(armour_t, 2),
                            "mesh_t": round(mesh_t, 3),
                            "total_penalty_t": round(total_penalty_t, 2),
                            "penalty_fraction": round(penalty_frac, 4),
                            "chunks_available": chunk_avail,
                            "closes_p_target": closes_p,
                            "closes_mass_budget": closes_mass,
                            "chunks_present": chunks_present,
                            "closes_all": closes_all,
                        }
                    )
    return rows


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    out_dir = Path(__file__).parent / "results"
    out_dir.mkdir(parents=True, exist_ok=True)

    baseline = reproduce_titan_baseline()
    armour_rows = sweep_armour()
    mesh_rows = sweep_mesh()
    incl_rows = sweep_inclination()
    slow_rows = sweep_slow_cross()
    combined_rows = sweep_combined()

    # Compute closure stats
    closing_cells = [r for r in combined_rows if r["closes_all"]]
    closing_p_only = [r for r in combined_rows if r["closes_p_target"]]
    closing_p_with_chunks = [
        r for r in combined_rows if r["closes_p_target"] and r["chunks_present"]
    ]

    # Find best (lowest p_per_pass) cell for each constraint subset
    def best(rows, key):
        return min(rows, key=lambda r: r[key]) if rows else None

    best_overall = best(combined_rows, "p_impact_per_pass")
    best_with_chunks = best(
        [r for r in combined_rows if r["chunks_present"]], "p_impact_per_pass"
    )

    summary = {
        "round": "R-bring-rendezvous-survivability",
        "worker": "phoebe",
        "geometry": {
            "r_periapsis_km": R_RENDEZVOUS_PERIAPSIS_KM,
            "r_apoapsis_km": R_CAPTURE_APOAPSIS_KM,
            "inclination_hohmann_deg": INCLINATION_HOHMANN_DEG,
            "v_periapsis_kms": vehicle_speed_at_periapsis_kms(
                R_RENDEZVOUS_PERIAPSIS_KM, R_CAPTURE_APOAPSIS_KM
            ),
            "v_circular_at_rendezvous_kms": v_circular_kms(R_RENDEZVOUS_PERIAPSIS_KM),
        },
        "targets": {
            "p_impact_per_crossing": TARGET_P_IMPACT_PER_CROSSING,
            "p_impact_two_crossings": TARGET_P_IMPACT_TWO_CROSSINGS,
            "mass_penalty_fraction": TARGET_MASS_PENALTY_FRACTION,
        },
        "baseline_titan_reproduction": baseline,
        "vehicle_anchor": {
            "dry_mass_t": VARIANT_B_DRY_MASS_T,
            "chunk_mass_t": CHUNK_MASS_T_BASELINE,
            "vehicle_total_baseline_t": VEHICLE_TOTAL_BASELINE_T,
            "bag_aperture_m2": BAG_APERTURE_M2_DEFAULT,
            "isp_variant_B_s": ISP_VARIANT_B_S,
        },
        "sweep_armour": armour_rows,
        "sweep_mesh": mesh_rows,
        "sweep_inclination": incl_rows,
        "sweep_slow_cross": slow_rows,
        "sweep_combined": combined_rows,
        "closure_stats": {
            "n_cells_total": len(combined_rows),
            "n_closing_all": len(closing_cells),
            "n_closing_p_only": len(closing_p_only),
            "n_closing_p_with_chunks": len(closing_p_with_chunks),
            "best_overall_cell_lowest_p_per_pass": best_overall,
            "best_with_chunks_present_lowest_p_per_pass": best_with_chunks,
        },
    }

    out_path = out_dir / "R_bring_rendezvous_survivability.json"
    out_path.write_text(json.dumps(summary, indent=2, default=str))

    # Stdout summary
    print(f"\n=== R-bring-rendezvous-survivability ===")
    print(
        f"Titan baseline reproduction: P_impact = {baseline['p_impact_per_pass']:.4f} "
        f"(titan: 0.9885, match within {baseline['match_within_pct']:.2f}%)"
    )
    print(
        f"\nVehicle at periapsis: v_p = {summary['geometry']['v_periapsis_kms']:.2f} km/s; "
        f"v_circ_ring at rendezvous = {summary['geometry']['v_circular_at_rendezvous_kms']:.2f} km/s"
    )

    print(f"\n--- Inclination-change Δv (apoapsis burn, round-trip) ---")
    for r in incl_rows:
        print(
            f"  i_target={r['i_target_deg']:5.1f}° Δi={r['delta_inc_deg']:5.1f}°  "
            f"Δv_RT_apo={r['dv_round_trip_apoapsis_kms']:6.3f} km/s  "
            f"prop_VB={r['propellant_mass_VariantB_Isp5000_t']:6.2f} t "
            f"({r['prop_pct_VB']:5.1f}% of {VEHICLE_TOTAL_BASELINE_T:.0f}t baseline) | "
            f"P_imp_zoneavg={r['p_impact_zoneavg_at_this_i']:.4f} "
            f"P_imp_out180={r['p_impact_outer_180km_at_this_i']:.4f} "
            f"P_imp_out80={r['p_impact_outermost_80km_at_this_i']:.4f}"
        )

    print(f"\n--- Slow-cross sweep (per audit 1: P_impact unchanged) ---")
    for r in slow_rows:
        print(
            f"  {r['scenario']:30s}  v_target={r['v_target_kms_saturn_frame']:5.2f} km/s "
            f"v_rel={r['v_rel_to_ring_particle_kms']:6.3f} km/s  "
            f"Δv_RT={r['dv_round_trip_kms']:6.2f} km/s  prop_VB={r['prop_VariantB_Isp5000_t']:6.1f} t  "
            f"KE/1cm-impact={r['ke_per_impact_1cm_particle_J']:.1f} J"
        )

    print(f"\n--- Combined sweep closure summary ---")
    print(f"  Total cells: {len(combined_rows)}")
    print(f"  Cells closing P_impact target only: {len(closing_p_only)}")
    print(f"  Cells closing P_impact AND with chunks present: {len(closing_p_with_chunks)}")
    print(f"  Cells closing P_impact AND mass AND chunks present: {len(closing_cells)}")
    if best_overall:
        print(
            f"\n  Lowest P_impact cell (any zone): "
            f"zone={best_overall['tau_zone']}, "
            f"τ_eff={best_overall['tau_eff']}, "
            f"i={best_overall['inclination_deg']}°, "
            f"mesh={best_overall['mesh_on']}, "
            f"P_per_pass={best_overall['p_impact_per_pass']:.6f}, "
            f"chunks={best_overall['chunks_available']}"
        )
    if best_with_chunks:
        print(
            f"\n  Lowest P_impact cell WITH chunks present: "
            f"zone={best_with_chunks['tau_zone']}, "
            f"τ_eff={best_with_chunks['tau_eff']}, "
            f"i={best_with_chunks['inclination_deg']}°, "
            f"mesh={best_with_chunks['mesh_on']}, "
            f"P_per_pass={best_with_chunks['p_impact_per_pass']:.6f}, "
            f"P_two_xings={best_with_chunks['p_impact_two_crossings']:.6f}, "
            f"penalty_frac={best_with_chunks['penalty_fraction']:.4f}"
        )

    print(f"\nResults written to {out_path}")


if __name__ == "__main__":
    main()
