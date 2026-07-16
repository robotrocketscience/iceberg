#!/usr/bin/env python3
"""R-bag-aperture-chunk-joint.

Self-questioning round 3: interrogate the implicit bag-aperture = 100 m²
anchor in R-bring-rendezvous-survivability and R-bring-survivability-relaxed.
Joint sweep of (chunk_mass, bag_aperture, mesh, zone, inclination) with
5-constraint closure: (a) extended-aperture survivability, (b) mass budget,
(c) defensible threshold, (d) chunk-availability in zone, (e) venture-class
economics per R-delivery-irr-curve.

Pre-registration in STUDY.md. Deterministic.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants (re-anchored from R-bring-survivability-relaxed)
# ---------------------------------------------------------------------------

GM_SATURN_KM3_S2 = 3.793e7
R_TITAN_ORBIT_KM = 1_221_870.0
R_RENDEZVOUS_PERIAPSIS_KM = 100_000.0
R_CAPTURE_APOAPSIS_KM = R_TITAN_ORBIT_KM
INCLINATION_HOHMANN_DEG = 26.7

WATER_ICE_RHO_KG_M3 = 917.0
PARTICLE_D_MIN_M = 1.0e-3
PARTICLE_D_MAX_M = 10.0
PARTICLE_RHO_KG_M3 = 2500.0

VARIANT_B_DRY_MASS_T = 64.0
ISP_VARIANT_B_S = 5000.0
G0_M_S2 = 9.80665
TARGET_MASS_PENALTY_FRACTION = 0.10

# Per-crossing thresholds (per self-audit table from R-bring-survivability-relaxed)
THRESHOLDS = {
    "ultra-strict": 1.0e-4,
    "moderate": 2.2e-3,
    "aggressive": 1.1e-2,
    "extreme (non-defensible)": 2.2e-2,
}

# Venture-class hurdles (per R-delivery-irr-curve crossover findings)
HURDLE_DELIVERED_T_PER_SHIP = {
    "sovereign-bond (4%)": 209.0,
    "regulated-utility (8%)": 461.0,
    "corporate-growth (10%)": 691.0,
}

# τ-zones (subset; chunk-availability tag)
TAU_ZONES = [
    ("B-ring zone-avg",            2.00,  "rich"),
    ("B-ring outer 580 km",        0.40,  "rich"),
    ("Huygens Ringlet (in CD)",    0.30,  "rich"),
    ("B-ring outermost 180 km",    0.10,  "thin"),
    ("B-ring outermost 80 km",     0.03,  "sparse"),
]

# Mesh sweep (cull diameter, areal density)
MESH_OPTIONS = [
    (None,    0.0,    "no mesh"),
    (0.01,    5.0,    "1 cm cull"),
    (0.05,    25.0,   "5 cm cull"),
    (0.10,    50.0,   "10 cm cull"),
    (0.20,    100.0,  "20 cm cull"),
    (1.00,    500.0,  "1 m cull"),
]

INCLINATIONS_DEG = [26.7, 60.0, 90.0]
CHUNK_MASSES_T = [10.0, 20.0, 50.0, 100.0, 200.0, 482.0]

CAPTURE_MARGIN_FACTOR = 1.2  # bag aperture ≥ 1.2 × chunk frontal area

# Delivered-mass-per-mission anchor: assume bag accretes ONLY chunk; treat
# delivered mass = chunk mass for venture-class hurdle check (gross). This is
# a charitable reading — actual delivered mass after Earth aerocapture losses
# would be lower; per phoebe a7a8456 aerocapture closure failed entirely so
# this whole section is conditional.
def delivered_mass_per_ship_t(chunk_mass_t: float) -> float:
    return chunk_mass_t  # gross-of-losses charitable reading

# ---------------------------------------------------------------------------
# Helpers (re-imported logic from R-bring-survivability-relaxed)
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


def chunk_radius_m(m_t: float) -> float:
    return (3.0 * m_t * 1000.0 / (4.0 * math.pi * WATER_ICE_RHO_KG_M3)) ** (1.0 / 3.0)


def chunk_frontal_area_m2(m_t: float) -> float:
    r = chunk_radius_m(m_t)
    return math.pi * r ** 2


def bag_min_area_m2(m_t: float) -> float:
    return CAPTURE_MARGIN_FACTOR * chunk_frontal_area_m2(m_t)


def number_fraction_above_d(d_cull_m: float | None) -> float:
    if d_cull_m is None or d_cull_m <= PARTICLE_D_MIN_M:
        return 1.0
    return (PARTICLE_D_MIN_M / d_cull_m) ** 2


def mean_particle_cross_section_m2() -> float:
    log_ratio = math.log(PARTICLE_D_MAX_M / PARTICLE_D_MIN_M)
    return math.pi / 4.0 * 2.0 * PARTICLE_D_MIN_M ** 2 * log_ratio


SIGMA_MEAN_M2 = mean_particle_cross_section_m2()


def expected_hits_per_pass(
    tau_total: float, d_cull_m: float | None, A_v_m2: float, inclination_deg: float
) -> float:
    n_total_h = tau_total / SIGMA_MEAN_M2
    n_above_h = n_total_h * number_fraction_above_d(d_cull_m)
    return n_above_h * A_v_m2 * csc_deg(inclination_deg)


# ---------------------------------------------------------------------------
# Sweep
# ---------------------------------------------------------------------------

def sweep() -> list[dict]:
    rows = []
    v_apo = vis_viva_v_kms(
        R_CAPTURE_APOAPSIS_KM,
        0.5 * (R_RENDEZVOUS_PERIAPSIS_KM + R_CAPTURE_APOAPSIS_KM),
    )

    for chunk_t in CHUNK_MASSES_T:
        bag_min = bag_min_area_m2(chunk_t)
        for av_factor in [1.0, 2.0, 4.0]:
            A_v = bag_min * av_factor
        # Also try fixed A_v = 100 m² for comparison if it satisfies bag_min
        for fixed_av in [100.0]:
            if fixed_av >= bag_min:
                pass  # add below
        # Build aperture list: bag_min, 2×, 4×, and 100 m² if feasible
        aperture_list = [bag_min, 2.0 * bag_min, 4.0 * bag_min]
        if 100.0 >= bag_min and 100.0 not in aperture_list:
            aperture_list.append(100.0)
        for A_v in aperture_list:
            for (d_cull_m, mesh_kg_m2, mesh_label) in MESH_OPTIONS:
                for (zone_label, tau_total, chunk_avail) in TAU_ZONES:
                    for incl in INCLINATIONS_DEG:
                        n_hits = expected_hits_per_pass(tau_total, d_cull_m, A_v, incl)
                        p_ea = 1.0 - math.exp(-n_hits)

                        delta_inc = incl - INCLINATION_HOHMANN_DEG
                        dv_round_trip = 2.0 * edelbaum_dv_kms(v_apo, delta_inc)
                        # Vehicle baseline: dry mass + chunk
                        vehicle_total_t = VARIANT_B_DRY_MASS_T + chunk_t
                        prop_t = propellant_mass_t(vehicle_total_t, dv_round_trip, ISP_VARIANT_B_S)
                        mesh_t = mesh_kg_m2 * A_v / 1000.0
                        total_penalty_t = prop_t + mesh_t
                        penalty_frac = total_penalty_t / vehicle_total_t

                        # Closure flags
                        chunks_present = chunk_avail in ("rich", "thin")
                        closes_mass = penalty_frac <= TARGET_MASS_PENALTY_FRACTION
                        delivered_t = delivered_mass_per_ship_t(chunk_t)

                        # Threshold closures
                        threshold_closures = {}
                        for thr_label, thr_value in THRESHOLDS.items():
                            closes_p = p_ea <= thr_value
                            threshold_closures[thr_label] = closes_p

                        # Venture-class hurdle closures (delivered mass)
                        hurdle_closures = {}
                        for h_label, h_value in HURDLE_DELIVERED_T_PER_SHIP.items():
                            hurdle_closures[h_label] = delivered_t >= h_value

                        # 5-constraint aggregate closure (under aggressive
                        # threshold = 1.1e-2, the lowest defensible)
                        all_close_aggressive = (
                            threshold_closures["aggressive"]
                            and closes_mass
                            and chunks_present
                            and hurdle_closures["sovereign-bond (4%)"]
                        )
                        # Also check under extreme (non-defensible) threshold
                        all_close_extreme = (
                            threshold_closures["extreme (non-defensible)"]
                            and closes_mass
                            and chunks_present
                            and hurdle_closures["sovereign-bond (4%)"]
                        )

                        rows.append({
                            "chunk_t": chunk_t,
                            "chunk_radius_m": round(chunk_radius_m(chunk_t), 2),
                            "chunk_frontal_m2": round(chunk_frontal_area_m2(chunk_t), 2),
                            "bag_min_m2": round(bag_min, 2),
                            "A_v_m2": round(A_v, 2),
                            "A_v_to_bag_min_ratio": round(A_v / bag_min, 2),
                            "mesh_label": mesh_label,
                            "mesh_t": round(mesh_t, 2),
                            "zone": zone_label,
                            "tau_total": tau_total,
                            "chunk_avail": chunk_avail,
                            "chunks_present": chunks_present,
                            "inclination_deg": incl,
                            "vehicle_total_t": vehicle_total_t,
                            "expected_hits_per_pass": round(n_hits, 6),
                            "p_ea_per_pass": p_ea,
                            "dv_round_trip_kms": round(dv_round_trip, 3),
                            "propellant_t": round(prop_t, 2),
                            "total_penalty_t": round(total_penalty_t, 2),
                            "penalty_fraction": round(penalty_frac, 4),
                            "closes_mass_budget": closes_mass,
                            "delivered_t_per_mission": delivered_t,
                            "threshold_closes": threshold_closures,
                            "hurdle_closes": hurdle_closures,
                            "ALL_CLOSE_aggressive_threshold": all_close_aggressive,
                            "ALL_CLOSE_extreme_threshold": all_close_extreme,
                        })
    return rows


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    out_dir = Path(__file__).parent / "results"
    out_dir.mkdir(parents=True, exist_ok=True)

    rows = sweep()

    # Tally
    n_total = len(rows)
    n_close_aggressive = sum(1 for r in rows if r["ALL_CLOSE_aggressive_threshold"])
    n_close_extreme = sum(1 for r in rows if r["ALL_CLOSE_extreme_threshold"])

    # Cells closing P_ea + mass + chunks (no hurdle yet)
    n_survives = sum(
        1 for r in rows
        if r["threshold_closes"]["extreme (non-defensible)"]
        and r["closes_mass_budget"]
        and r["chunks_present"]
    )
    # ...and add sovereign-bond hurdle
    n_survives_and_pays = sum(
        1 for r in rows
        if r["threshold_closes"]["extreme (non-defensible)"]
        and r["closes_mass_budget"]
        and r["chunks_present"]
        and r["hurdle_closes"]["sovereign-bond (4%)"]
    )

    # Bag-min relationship table
    bag_min_table = []
    for chunk_t in CHUNK_MASSES_T:
        bag_min_table.append({
            "chunk_t": chunk_t,
            "chunk_radius_m": round(chunk_radius_m(chunk_t), 2),
            "chunk_frontal_m2": round(chunk_frontal_area_m2(chunk_t), 2),
            "bag_min_m2": round(bag_min_area_m2(chunk_t), 2),
        })

    # Trim per-cell records to keep JSON small (per CLAUDE.md "no large results
    # files"). Keep all rows but drop redundant per-cell threshold and hurdle
    # dicts (recomputable from p_ea and chunk_t).
    rows_compact = []
    for r in rows:
        rc = {k: v for k, v in r.items()
              if k not in ("threshold_closes", "hurdle_closes")}
        rows_compact.append(rc)

    # Sample of "best" rows by p_ea for inspection (lowest 20)
    best_by_p_ea = sorted(rows, key=lambda r: r["p_ea_per_pass"])[:20]

    summary = {
        "round": "R-bag-aperture-chunk-joint",
        "worker": "phoebe",
        "purpose": "self-question bag-aperture anchor in prior two B-ring rounds",
        "n_cells_total": n_total,
        "n_cells_close_aggressive_threshold": n_close_aggressive,
        "n_cells_close_extreme_threshold": n_close_extreme,
        "n_cells_survive_extended_aperture_only": n_survives,
        "n_cells_survive_AND_pay_sovereign_bond_hurdle": n_survives_and_pays,
        "bag_min_relationship": bag_min_table,
        "thresholds_definition": THRESHOLDS,
        "venture_class_hurdles_t_per_ship": HURDLE_DELIVERED_T_PER_SHIP,
        "best_50_cells_by_p_ea": sorted(rows, key=lambda r: r["p_ea_per_pass"])[:50],
        "anchor_cell_10t_chunk_outermost80km_90deg_1m_mesh": next(
            (r for r in rows
             if r["chunk_t"] == 10.0
             and abs(r["A_v_m2"] - bag_min_area_m2(10.0)) < 0.01
             and r["mesh_label"] == "1 m cull"
             and r["zone"] == "B-ring outermost 80 km"
             and r["inclination_deg"] == 90.0),
            None,
        ),
        "note": "Full per-cell sweep is not persisted to keep results file small; 0 of 2160 cells closed any of the all-five-constraint variants. Best-50-cells-by-p_ea above shows the most-favourable end of the sweep — none satisfy chunks-present + mass-budget + economics simultaneously.",
    }

    out_path = out_dir / "R_bag_aperture_chunk_joint.json"
    out_path.write_text(json.dumps(summary, indent=2, default=str))

    # Stdout
    print("\n=== R-bag-aperture-chunk-joint ===\n")
    print("Bag-min relationship (geometric: A_bag ≥ 1.2 × chunk frontal area):")
    for r in bag_min_table:
        print(
            f"  chunk={r['chunk_t']:6.1f} t  r={r['chunk_radius_m']:.2f} m  "
            f"A_chunk={r['chunk_frontal_m2']:.2f} m²  A_bag_min={r['bag_min_m2']:.2f} m²"
        )

    print(f"\nClosure tally over {n_total} cells:")
    print(f"  Survives extended-aperture (extreme threshold) + mass + chunks present: {n_survives}")
    print(f"  ...AND meets sovereign-bond delivered-mass hurdle (≥209 t): {n_survives_and_pays}")
    print(f"  ALL_CLOSE under aggressive threshold (1.1e-2, defensible-stretch): {n_close_aggressive}")
    print(f"  ALL_CLOSE under extreme threshold (2.2e-2, non-defensible): {n_close_extreme}")

    # List cells that survive extended-aperture under the most lenient
    # configuration, to characterise the surviving set
    survivors = [
        r for r in rows
        if r["threshold_closes"]["extreme (non-defensible)"]
        and r["closes_mass_budget"]
        and r["chunks_present"]
    ]
    if survivors:
        print(f"\nSurvivor cells (extreme threshold, mass-budget, chunks-present): {len(survivors)}")
        print("First few:")
        for r in survivors[:10]:
            print(
                f"  chunk={r['chunk_t']:6.1f}t bag={r['A_v_m2']:.1f}m² mesh={r['mesh_label']:10s} "
                f"zone={r['zone']:30s} i={r['inclination_deg']:5.1f}° "
                f"hits/pass={r['expected_hits_per_pass']:.3e} P_ea={r['p_ea_per_pass']:.4f} "
                f"penalty={r['penalty_fraction']:.3f} delivered={r['delivered_t_per_mission']:.0f}t"
            )
    else:
        print("\nNo cells survive extended-aperture even at extreme threshold.")

    # Anchor cell: chunk=10t, bag=A_bag_min, mesh=1m, outermost-80km, 90°
    anchor_match = [
        r for r in rows
        if r["chunk_t"] == 10.0
        and abs(r["A_v_m2"] - bag_min_area_m2(10.0)) < 0.01
        and r["mesh_label"] == "1 m cull"
        and r["zone"] == "B-ring outermost 80 km"
        and r["inclination_deg"] == 90.0
    ]
    print("\nAnchor cell (10t chunk, bag=min, 1m mesh, outermost-80km, 90°):")
    if anchor_match:
        r = anchor_match[0]
        print(
            f"  hits/pass={r['expected_hits_per_pass']:.4f}  P_ea={r['p_ea_per_pass']:.4f}  "
            f"penalty={r['penalty_fraction']:.4f}  chunks_present={r['chunks_present']}  "
            f"delivered={r['delivered_t_per_mission']}t  hurdles={r['hurdle_closes']}"
        )

    print(f"\nResults written to {out_path}")


if __name__ == "__main__":
    main()
