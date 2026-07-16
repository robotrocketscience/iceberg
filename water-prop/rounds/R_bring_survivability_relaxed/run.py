#!/usr/bin/env python3
"""R-bring-survivability-relaxed.

Self-questioning follow-up to R-bring-rendezvous-survivability (commit
`abdcd35`). Interrogates prior verdict on four axes that could plausibly
flip it: closure threshold, mesh capability, extended-aperture treatment,
single-vs-double crossing.

Pre-registration in STUDY.md. BOE central anchors computed first.

Deterministic. Run from this directory or project root.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

GM_SATURN_KM3_S2 = 3.793e7
R_TITAN_ORBIT_KM = 1_221_870.0
R_RENDEZVOUS_PERIAPSIS_KM = 100_000.0
R_CAPTURE_APOAPSIS_KM = R_TITAN_ORBIT_KM
INCLINATION_HOHMANN_DEG = 26.7

# Closure thresholds (per-B-ring-crossing impact-prob budget) — sweep
THRESHOLD_LEVELS = {
    "ultra-strict (SCOPE prior)": 1.0e-4,         # f_other = 0.995
    "strict": 1.0e-3,                              # f_other = 0.95
    "moderate": 2.2e-3,                            # f_other = 0.90 (per self-audit table)
    "aggressive (50% budget to B-ring)": 1.1e-2,  # f_other = 0.50
    "extreme (full budget to B-ring)": 2.2e-2,    # f_other = 0.0
}

TARGET_MASS_PENALTY_FRACTION = 0.10

VARIANT_B_DRY_MASS_T = 64.0
CHUNK_MASS_T_BASELINE = 200.0
VEHICLE_TOTAL_BASELINE_T = VARIANT_B_DRY_MASS_T + CHUNK_MASS_T_BASELINE
ISP_VARIANT_B_S = 5000.0
G0_M_S2 = 9.80665
BAG_APERTURE_M2_DEFAULT = 100.0

# Particle size distribution N(D) ∝ D⁻³ over [D_min, D_max] (per fine-structure H3)
PARTICLE_D_MIN_M = 1.0e-3        # 1 mm
PARTICLE_D_MAX_M = 10.0           # 10 m

# Particle density (rocky-icy mixture)
PARTICLE_RHO_KG_M3 = 2500.0

# ---------------------------------------------------------------------------
# τ-zones (subset of prior round; chunk-availability tag)
# ---------------------------------------------------------------------------

TAU_ZONES = [
    ("B-ring zone-avg",            100_000.0, 2.00,  "rich"),
    ("B-ring outer 580 km",        117_000.0, 0.40,  "rich"),
    ("Huygens Ringlet (in CD)",    117_900.0, 0.30,  "rich"),
    ("B-ring outermost 180 km",    117_400.0, 0.10,  "thin"),
    ("B-ring outermost 80 km",     117_500.0, 0.03,  "sparse"),
    ("Cassini Div outer plateau",  120_000.0, 0.04,  "none"),
    ("Huygens Gap",                117_680.0, 0.001, "none"),
]

# ---------------------------------------------------------------------------
# Mesh capability sweep
# ---------------------------------------------------------------------------
# (cull_size_m, areal_density_kg_m2, label)
MESH_OPTIONS = [
    (None,    0.0,    "no mesh"),
    (0.01,    5.0,    "1 cm cull"),
    (0.05,    25.0,   "5 cm cull"),
    (0.10,    50.0,   "10 cm cull"),
    (0.20,    100.0,  "20 cm cull"),
    (1.00,    500.0,  "1 m cull"),
]

INCLINATIONS_DEG = [26.7, 60.0, 90.0]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def vis_viva_v_kms(r_km: float, a_km: float) -> float:
    return math.sqrt(GM_SATURN_KM3_S2 * (2.0 / r_km - 1.0 / a_km))


def edelbaum_dv_kms(v_at_burn_kms: float, delta_inc_deg: float) -> float:
    return 2.0 * v_at_burn_kms * math.sin(math.radians(delta_inc_deg) / 2.0)


def propellant_mass_t(dry_t: float, dv_kms: float, isp_s: float) -> float:
    ve_kms = isp_s * G0_M_S2 / 1000.0
    return dry_t * (math.exp(dv_kms / ve_kms) - 1.0)


def csc_deg(i_deg: float) -> float:
    return 1.0 / math.sin(math.radians(i_deg))


def tau_fraction_above_d(d_cull_m: float | None,
                          d_min: float = PARTICLE_D_MIN_M,
                          d_max: float = PARTICLE_D_MAX_M) -> float:
    """Fraction of total τ contributed by particles with diameter > d_cull.

    For N(D) ∝ D⁻³, τ contribution is dominated by ln(D_max/D_min)-weighted
    integrand: τ(>D) / τ_total = ln(D_max / D) / ln(D_max / D_min).
    """
    if d_cull_m is None or d_cull_m <= d_min:
        return 1.0
    if d_cull_m >= d_max:
        return 0.0
    return math.log(d_max / d_cull_m) / math.log(d_max / d_min)


def number_fraction_above_d(d_cull_m: float | None,
                             d_min: float = PARTICLE_D_MIN_M) -> float:
    """Fraction of total NUMBER of particles with diameter > d_cull.

    For N(D) ∝ D⁻³, n(>D) ∝ ∫_D D⁻³ dD ∝ D⁻², so n(>D)/n_total ≈ (D_min/D)²
    for D >> D_min.
    """
    if d_cull_m is None or d_cull_m <= d_min:
        return 1.0
    return (d_min / d_cull_m) ** 2


def mean_particle_cross_section_m2() -> float:
    """Mean σ = π/4 × ⟨D²⟩ for N(D) ∝ D⁻³ over [D_min, D_max].

    ⟨D²⟩ = ∫ D² N dD / ∫ N dD ≈ 2 D_min² ln(D_max/D_min).
    """
    log_ratio = math.log(PARTICLE_D_MAX_M / PARTICLE_D_MIN_M)
    d2_mean = 2.0 * PARTICLE_D_MIN_M ** 2 * log_ratio
    return math.pi / 4.0 * d2_mean


# Cache mean cross-section
SIGMA_MEAN_M2 = mean_particle_cross_section_m2()


def n_total_h_per_m2(tau_total: float) -> float:
    """Number-density × ring-thickness for total particle population.

    From τ_total = (n_total × h) × ⟨σ⟩.
    """
    return tau_total / SIGMA_MEAN_M2


def expected_hits_per_pass_above_d(
    tau_total: float, d_cull_m: float | None, aperture_m2: float, inclination_deg: float
) -> float:
    """Extended-aperture expected hit count from particles > d_cull per pass."""
    n_total_h = n_total_h_per_m2(tau_total)
    n_above_h = n_total_h * number_fraction_above_d(d_cull_m)
    path_length_factor = csc_deg(inclination_deg)
    return n_above_h * aperture_m2 * path_length_factor


def particle_mass_kg(d_m: float) -> float:
    return PARTICLE_RHO_KG_M3 * (4.0 / 3.0) * math.pi * (d_m / 2.0) ** 3


def particle_ke_J(d_m: float, v_rel_km_s: float) -> float:
    return 0.5 * particle_mass_kg(d_m) * (v_rel_km_s * 1000.0) ** 2


def p_impact_point_vehicle(tau_eff: float, inclination_deg: float) -> float:
    return 1.0 - math.exp(-tau_eff * csc_deg(inclination_deg))


# ---------------------------------------------------------------------------
# Body 1 — threshold-sensitivity table
# ---------------------------------------------------------------------------

def body1_threshold_table() -> list[dict]:
    rows = []
    L0_10 = 0.8
    per_mission_failure_budget = 1.0 - L0_10 ** (1.0 / 5.0)  # 0.0437
    for label, threshold in THRESHOLD_LEVELS.items():
        per_mission_to_bring = 2.0 * threshold  # 2 crossings
        f_other = 1.0 - per_mission_to_bring / per_mission_failure_budget
        rows.append({
            "threshold_label": label,
            "per_crossing_threshold": threshold,
            "per_mission_allocation_to_2_brings": per_mission_to_bring,
            "L0_10_per_mission_failure_budget": per_mission_failure_budget,
            "implied_f_other": round(max(0.0, f_other), 4),
            "defensible_label": (
                "non-defensible (no budget for other failures)" if f_other < 0.30
                else "stretched (≥ 30% budget for others)" if f_other < 0.70
                else "comfortable (≥ 70% budget for others)"
            ),
        })
    return rows


# ---------------------------------------------------------------------------
# Body 2 — point-vehicle vs extended-aperture combined sweep
# ---------------------------------------------------------------------------

def body2_combined_sweep() -> list[dict]:
    rows = []
    aperture_m2 = BAG_APERTURE_M2_DEFAULT
    v_apo = vis_viva_v_kms(R_CAPTURE_APOAPSIS_KM, 0.5 * (R_RENDEZVOUS_PERIAPSIS_KM + R_CAPTURE_APOAPSIS_KM))
    # v_rel for hypervelocity hit-energy estimate (HE-graze residual ~6.6 km/s)
    v_rel_km_s = 6.6

    for (tau_label, tau_r, tau_total, chunk_avail) in TAU_ZONES:
        for (d_cull_m, mesh_kg_m2, mesh_label) in MESH_OPTIONS:
            for incl in INCLINATIONS_DEG:
                # Effective τ on bag (after mesh removes < d_cull particles)
                tau_eff = tau_total * tau_fraction_above_d(d_cull_m)

                # Point-vehicle P_impact
                p_pv = p_impact_point_vehicle(tau_eff, incl)

                # Extended-aperture expected hits (only counting particles > d_cull
                # which mesh does NOT stop)
                n_hits_above = expected_hits_per_pass_above_d(
                    tau_total, d_cull_m, aperture_m2, incl
                )
                # Extended-aperture P(at least one large hit) = 1 - exp(-n_hits)
                p_ea = 1.0 - math.exp(-n_hits_above)

                # Mass penalty: inclination-Δv + mesh
                delta_inc = incl - INCLINATION_HOHMANN_DEG
                dv_round_trip = 2.0 * edelbaum_dv_kms(v_apo, delta_inc)
                prop_t = propellant_mass_t(VEHICLE_TOTAL_BASELINE_T, dv_round_trip, ISP_VARIANT_B_S)
                mesh_t = mesh_kg_m2 * aperture_m2 / 1000.0
                total_penalty_t = prop_t + mesh_t
                penalty_frac = total_penalty_t / VEHICLE_TOTAL_BASELINE_T

                # Per-impact KE for the smallest unshielded particle (just above d_cull)
                d_eff_for_ke = d_cull_m if d_cull_m is not None else PARTICLE_D_MIN_M
                ke_smallest_unshielded_J = particle_ke_J(d_eff_for_ke, v_rel_km_s)

                rows.append({
                    "tau_zone": tau_label,
                    "tau_zone_r_km": tau_r,
                    "tau_total": tau_total,
                    "chunk_availability": chunk_avail,
                    "chunks_present": chunk_avail in ("rich", "thin"),
                    "mesh_label": mesh_label,
                    "mesh_cull_m": d_cull_m,
                    "mesh_kg_m2": mesh_kg_m2,
                    "inclination_deg": incl,
                    "tau_eff_on_bag": round(tau_eff, 5),
                    "p_impact_pointvehicle_per_pass": p_pv,
                    "expected_hits_per_pass_extended_aperture": n_hits_above,
                    "p_impact_extended_aperture_per_pass": p_ea,
                    "ke_per_smallest_unshielded_hit_J": round(ke_smallest_unshielded_J, 1),
                    "dv_round_trip_kms": round(dv_round_trip, 3),
                    "propellant_t": round(prop_t, 2),
                    "mesh_t": round(mesh_t, 2),
                    "total_penalty_t": round(total_penalty_t, 2),
                    "penalty_fraction": round(penalty_frac, 4),
                })
    return rows


# ---------------------------------------------------------------------------
# Body 3 — closure verdict under each threshold × {point-vehicle, extended}
#          × {single-crossing, double-crossing}
# ---------------------------------------------------------------------------

def closure_verdicts(rows: list[dict]) -> list[dict]:
    """For each cell, declare closure under every (threshold × treatment × crossings).

    Records a "best closure label" for each row.
    """
    out = []
    for row in rows:
        per_threshold = {}
        for thr_label, thr_value in THRESHOLD_LEVELS.items():
            for treatment in ["pointvehicle", "extended"]:
                p_per_pass = (
                    row["p_impact_pointvehicle_per_pass"] if treatment == "pointvehicle"
                    else row["p_impact_extended_aperture_per_pass"]
                )
                # Two-crossings target: 2P (linear approx) for small P, or 1-(1-P)^2
                p_two = 1.0 - (1.0 - p_per_pass) ** 2
                target_two_xings = 1.0 - (1.0 - thr_value) ** 2
                closes_double = (
                    p_two <= target_two_xings
                    and row["penalty_fraction"] <= TARGET_MASS_PENALTY_FRACTION
                    and row["chunks_present"]
                )
                closes_single = (
                    p_per_pass <= thr_value
                    and row["penalty_fraction"] <= TARGET_MASS_PENALTY_FRACTION
                    and row["chunks_present"]
                )
                # Compact bitfield key: D=double-crossing, S=single-crossing
                # Example: "DS" = closes both, "S" = single only, "" = neither
                code = ("D" if closes_double else "") + ("S" if closes_single else "")
                per_threshold[f"{thr_label}|{treatment}"] = code
        new_row = dict(row)
        new_row["closure_verdicts"] = per_threshold
        out.append(new_row)
    return out


# ---------------------------------------------------------------------------
# Body 4 — find flip-threshold per cell
# ---------------------------------------------------------------------------

def find_flip_thresholds(rows: list[dict]) -> list[dict]:
    """For each cell, find the minimum threshold required to flip to closure under
    each treatment × crossings option. Returns enriched rows.
    """
    L0_10 = 0.8
    per_mission_budget = 1.0 - L0_10 ** (1.0 / 5.0)
    enriched = []
    for row in rows:
        if not row["chunks_present"] or row["penalty_fraction"] > TARGET_MASS_PENALTY_FRACTION:
            row["flip_threshold_pointvehicle_double"] = None
            row["flip_threshold_extended_double"] = None
            row["flip_threshold_pointvehicle_single"] = None
            row["flip_threshold_extended_single"] = None
            row["flip_implied_f_other_pointvehicle_double"] = None
            enriched.append(row)
            continue

        p_pv = row["p_impact_pointvehicle_per_pass"]
        p_ea = row["p_impact_extended_aperture_per_pass"]

        def f_other_for(per_crossing_thr):
            per_mission_to_bring = 2.0 * per_crossing_thr
            return max(0.0, 1.0 - per_mission_to_bring / per_mission_budget)

        # For double-crossing: flip-threshold is per-crossing value such that
        # 1-(1-thr)^2 = 1-(1-P)^2, i.e. thr = P
        row["flip_threshold_pointvehicle_double"] = p_pv
        row["flip_threshold_extended_double"] = p_ea
        row["flip_threshold_pointvehicle_single"] = p_pv  # same magnitude with single crossing
        row["flip_threshold_extended_single"] = p_ea

        row["flip_implied_f_other_pointvehicle_double"] = round(f_other_for(p_pv), 4)
        row["flip_implied_f_other_extended_double"] = round(f_other_for(p_ea), 4)
        enriched.append(row)
    return enriched


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    out_dir = Path(__file__).parent / "results"
    out_dir.mkdir(parents=True, exist_ok=True)

    threshold_rows = body1_threshold_table()
    sweep_rows = body2_combined_sweep()
    verdict_rows = closure_verdicts(sweep_rows)
    flip_rows = find_flip_thresholds(verdict_rows)

    # Closure stats per (threshold × treatment × crossings)
    closure_stats = {}
    for thr_label in THRESHOLD_LEVELS:
        for treatment in ["pointvehicle", "extended"]:
            key = f"{thr_label}|{treatment}"
            n_closes_double = sum(
                1 for r in flip_rows if "D" in r["closure_verdicts"][key]
            )
            n_closes_single = sum(
                1 for r in flip_rows if "S" in r["closure_verdicts"][key]
            )
            closure_stats[key] = {
                "n_closes_double_crossing": n_closes_double,
                "n_closes_single_crossing": n_closes_single,
            }

    # Find best (lowest flip-threshold) chunk-bearing cells
    chunk_cells_with_flip = [
        r for r in flip_rows
        if r["chunks_present"]
        and r["penalty_fraction"] <= TARGET_MASS_PENALTY_FRACTION
        and r["flip_threshold_pointvehicle_double"] is not None
    ]

    if chunk_cells_with_flip:
        best_pv = min(chunk_cells_with_flip, key=lambda r: r["flip_threshold_pointvehicle_double"])
        best_ea = min(chunk_cells_with_flip, key=lambda r: r["flip_threshold_extended_double"])
    else:
        best_pv = None
        best_ea = None

    summary = {
        "round": "R-bring-survivability-relaxed",
        "worker": "phoebe",
        "purpose": "self-questioning follow-up to R-bring-rendezvous-survivability",
        "particle_size_distribution": {
            "law": "N(D) ∝ D⁻³",
            "D_min_m": PARTICLE_D_MIN_M,
            "D_max_m": PARTICLE_D_MAX_M,
            "particle_density_kg_m3": PARTICLE_RHO_KG_M3,
            "mean_particle_cross_section_m2": SIGMA_MEAN_M2,
        },
        "thresholds": THRESHOLD_LEVELS,
        "threshold_sensitivity_table": threshold_rows,
        "closure_stats_by_threshold_treatment": closure_stats,
        "n_cells_total": len(flip_rows),
        "best_chunk_cell_pointvehicle": best_pv,
        "best_chunk_cell_extended_aperture": best_ea,
        "all_cells": flip_rows,
    }

    out_path = out_dir / "R_bring_survivability_relaxed.json"
    out_path.write_text(json.dumps(summary, indent=2, default=str))

    # Stdout
    print("\n=== R-bring-survivability-relaxed ===\n")
    print("Threshold derivation table:")
    for r in threshold_rows:
        print(
            f"  {r['threshold_label']:45s}  thr={r['per_crossing_threshold']:.2e}  "
            f"per-mission to B-ring={r['per_mission_allocation_to_2_brings']:.4f}  "
            f"f_other={r['implied_f_other']:.3f}  ({r['defensible_label']})"
        )

    print("\nClosure stats per (threshold × treatment × crossings):")
    for thr_label in THRESHOLD_LEVELS:
        print(f"\n  Threshold: {thr_label} ({THRESHOLD_LEVELS[thr_label]:.2e})")
        for treatment in ["pointvehicle", "extended"]:
            key = f"{thr_label}|{treatment}"
            stats = closure_stats[key]
            print(
                f"    {treatment:15s}  closes (2 crossings): {stats['n_closes_double_crossing']:4d}/{len(flip_rows)}  "
                f"closes (1 crossing): {stats['n_closes_single_crossing']:4d}/{len(flip_rows)}"
            )

    print(f"\nBest chunk-bearing cell flip-threshold (point-vehicle, double-crossing):")
    if best_pv:
        print(
            f"  zone={best_pv['tau_zone']}, mesh={best_pv['mesh_label']}, i={best_pv['inclination_deg']}°"
        )
        print(
            f"  P_per_pass(pv)={best_pv['p_impact_pointvehicle_per_pass']:.4f}  "
            f"flip_threshold={best_pv['flip_threshold_pointvehicle_double']:.4f}  "
            f"implied f_other={best_pv['flip_implied_f_other_pointvehicle_double']:.3f}  "
            f"penalty={best_pv['penalty_fraction']:.4f}"
        )

    print(f"\nBest chunk-bearing cell flip-threshold (extended-aperture, double-crossing):")
    if best_ea:
        print(
            f"  zone={best_ea['tau_zone']}, mesh={best_ea['mesh_label']}, i={best_ea['inclination_deg']}°"
        )
        print(
            f"  expected_hits/pass={best_ea['expected_hits_per_pass_extended_aperture']:.4e}  "
            f"P_per_pass(ea)={best_ea['p_impact_extended_aperture_per_pass']:.6f}  "
            f"flip_threshold={best_ea['flip_threshold_extended_double']:.6f}  "
            f"implied f_other={best_ea['flip_implied_f_other_extended_double']:.4f}  "
            f"penalty={best_ea['penalty_fraction']:.4f}"
        )

    # Also print the highest-mesh-capability cell at outermost 80 km × 90°
    print("\nHigh-mesh-capability spotlight cells (outermost 80 km × 90°):")
    for r in flip_rows:
        if (r["tau_zone"] == "B-ring outermost 80 km"
                and r["inclination_deg"] == 90.0):
            print(
                f"  mesh={r['mesh_label']:10s} mass={r['mesh_t']:.2f}t  pen={r['penalty_fraction']:.4f}  "
                f"P_pv={r['p_impact_pointvehicle_per_pass']:.4e}  "
                f"hits/pass(ea)={r['expected_hits_per_pass_extended_aperture']:.4e}  "
                f"P_ea={r['p_impact_extended_aperture_per_pass']:.6f}  "
                f"chunks={r['chunk_availability']}"
            )

    print(f"\nResults written to {out_path}")


if __name__ == "__main__":
    main()
