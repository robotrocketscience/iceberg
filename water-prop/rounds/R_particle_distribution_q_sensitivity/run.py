#!/usr/bin/env python3
"""R-particle-distribution-q-sensitivity.

Fourth self-questioning round of session. Interrogates the N(D) ∝ D⁻³
particle-size-distribution exponent anchor used in three prior phoebe
rounds. Literature q range is [2.5, 4.0] across B-ring radial locations;
prior anchor at q=3 was the central value. Tests whether the verdict
(0 chunk-bearing cells close on all-five-constraint) survives across the
full literature range.

Pre-registration in STUDY.md. Deterministic.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants (re-anchored from R-bag-aperture-chunk-joint)
# ---------------------------------------------------------------------------

GM_SATURN_KM3_S2 = 3.793e7
R_TITAN_ORBIT_KM = 1_221_870.0
R_RENDEZVOUS_PERIAPSIS_KM = 100_000.0
R_CAPTURE_APOAPSIS_KM = R_TITAN_ORBIT_KM
INCLINATION_HOHMANN_DEG = 26.7

PARTICLE_D_MIN_M = 1.0e-3
PARTICLE_D_MAX_M = 10.0

VARIANT_B_DRY_MASS_T = 64.0
CHUNK_MASS_T = 200.0  # like-for-like with R-bag-aperture-chunk-joint baseline
VEHICLE_TOTAL_T = VARIANT_B_DRY_MASS_T + CHUNK_MASS_T  # 264 t
ISP_VARIANT_B_S = 5000.0
G0_M_S2 = 9.80665
BAG_APERTURE_M2 = 100.0
TARGET_MASS_PENALTY_FRACTION = 0.10

THRESHOLDS = {
    "ultra-strict": 1.0e-4,
    "strict": 1.0e-3,
    "moderate": 2.2e-3,
    "aggressive": 1.1e-2,
    "extreme (non-defensible)": 2.2e-2,
}

# Cassini-anchored literature q range
Q_VALUES = [2.5, 2.7, 3.0, 3.3, 3.5, 4.0]

TAU_ZONES = [
    ("B-ring zone-avg",            2.00,  "rich"),
    ("B-ring outer 580 km",        0.40,  "rich"),
    ("Huygens Ringlet (in CD)",    0.30,  "rich"),
    ("B-ring outermost 180 km",    0.10,  "thin"),
    ("B-ring outermost 80 km",     0.03,  "sparse"),
]

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
# Helpers — particle distribution math for arbitrary q
# ---------------------------------------------------------------------------

def mean_d_squared_for_q(q: float, d_min: float = PARTICLE_D_MIN_M,
                          d_max: float = PARTICLE_D_MAX_M) -> float:
    """⟨D²⟩ = ∫ D² × D^(-q) dD / ∫ D^(-q) dD over [d_min, d_max].

    Numerator integral: D^(3-q). Denominator integral: D^(1-q).
    """
    # Numerator: ∫ D^(2-q) dD = D^(3-q) / (3-q) if q ≠ 3; else ln(D)
    if abs(q - 3.0) < 1e-9:
        num = math.log(d_max / d_min)
    else:
        e_n = 3.0 - q
        num = (d_max ** e_n - d_min ** e_n) / e_n
    # Denominator: ∫ D^(-q) dD = D^(1-q) / (1-q) if q ≠ 1
    if abs(q - 1.0) < 1e-9:
        den = math.log(d_max / d_min)
    else:
        e_d = 1.0 - q
        den = (d_max ** e_d - d_min ** e_d) / e_d
    return num / den


def tau_fraction_above_d(d_cull: float | None, q: float) -> float:
    """Fraction of total τ contributed by particles with diameter > d_cull.

    τ contribution from size band is proportional to D² × N(D) dD =
    D² × D^(-q) dD = D^(2-q) dD. Cumulative integral above d_cull:
    """
    if d_cull is None or d_cull <= PARTICLE_D_MIN_M:
        return 1.0
    if d_cull >= PARTICLE_D_MAX_M:
        return 0.0
    if abs(q - 3.0) < 1e-9:
        return math.log(PARTICLE_D_MAX_M / d_cull) / math.log(PARTICLE_D_MAX_M / PARTICLE_D_MIN_M)
    e = 3.0 - q
    num = PARTICLE_D_MAX_M ** e - d_cull ** e
    den = PARTICLE_D_MAX_M ** e - PARTICLE_D_MIN_M ** e
    return num / den


def number_fraction_above_d(d_cull: float | None, q: float) -> float:
    """Fraction of total number of particles with diameter > d_cull.

    n(>d) ∝ ∫_d D^(-q) dD = D^(1-q) / (1-q).
    """
    if d_cull is None or d_cull <= PARTICLE_D_MIN_M:
        return 1.0
    if d_cull >= PARTICLE_D_MAX_M:
        return 0.0
    if abs(q - 1.0) < 1e-9:
        return math.log(PARTICLE_D_MAX_M / d_cull) / math.log(PARTICLE_D_MAX_M / PARTICLE_D_MIN_M)
    e = 1.0 - q
    num = PARTICLE_D_MAX_M ** e - d_cull ** e
    den = PARTICLE_D_MAX_M ** e - PARTICLE_D_MIN_M ** e
    return num / den


def csc_deg(i_deg: float) -> float:
    return 1.0 / math.sin(math.radians(i_deg))


def vis_viva_v_kms(r_km: float, a_km: float) -> float:
    return math.sqrt(GM_SATURN_KM3_S2 * (2.0 / r_km - 1.0 / a_km))


def edelbaum_dv_kms(v_at_burn_kms: float, delta_inc_deg: float) -> float:
    return 2.0 * v_at_burn_kms * math.sin(math.radians(delta_inc_deg) / 2.0)


def propellant_mass_t(dry_t: float, dv_kms: float, isp_s: float) -> float:
    ve_kms = isp_s * G0_M_S2 / 1000.0
    return dry_t * (math.exp(dv_kms / ve_kms) - 1.0)


# ---------------------------------------------------------------------------
# Body 1 — q-dependence reference table at outermost-180km × 90° × bag=100m²
# ---------------------------------------------------------------------------

def body1_q_reference() -> list[dict]:
    """Print P_ea sensitivity at the prior-round's marginal closure cell."""
    rows = []
    tau_zone = 0.10  # outermost 180 km
    inclination = 90.0
    A_v = 100.0

    for q in Q_VALUES:
        d2_mean = mean_d_squared_for_q(q)
        sigma_mean = math.pi / 4.0 * d2_mean
        n_total_h = tau_zone / sigma_mean
        for (d_cull, mesh_kg_m2, mesh_label) in MESH_OPTIONS:
            n_above_fraction = number_fraction_above_d(d_cull, q)
            n_above_h = n_total_h * n_above_fraction
            hits_per_pass = n_above_h * A_v * csc_deg(inclination)
            p_ea = 1.0 - math.exp(-hits_per_pass)
            rows.append({
                "q": q,
                "zone": "B-ring outermost 180 km",
                "mesh": mesh_label,
                "mesh_kg_m2": mesh_kg_m2,
                "inclination_deg": inclination,
                "sigma_mean_m2": sigma_mean,
                "n_total_h_per_m2": n_total_h,
                "n_above_fraction": n_above_fraction,
                "hits_per_pass": hits_per_pass,
                "p_ea_per_pass": p_ea,
            })
    return rows


# ---------------------------------------------------------------------------
# Body 2 — combined sweep
# ---------------------------------------------------------------------------

def body2_combined_sweep() -> list[dict]:
    rows = []
    v_apo = vis_viva_v_kms(
        R_CAPTURE_APOAPSIS_KM,
        0.5 * (R_RENDEZVOUS_PERIAPSIS_KM + R_CAPTURE_APOAPSIS_KM),
    )

    for q in Q_VALUES:
        d2_mean = mean_d_squared_for_q(q)
        sigma_mean = math.pi / 4.0 * d2_mean
        for (zone_label, tau_total, chunk_avail) in TAU_ZONES:
            n_total_h = tau_total / sigma_mean
            for (d_cull, mesh_kg_m2, mesh_label) in MESH_OPTIONS:
                n_above_fraction = number_fraction_above_d(d_cull, q)
                n_above_h = n_total_h * n_above_fraction
                for incl in INCLINATIONS_DEG:
                    hits_per_pass = n_above_h * BAG_APERTURE_M2 * csc_deg(incl)
                    p_ea = 1.0 - math.exp(-hits_per_pass)

                    delta_inc = incl - INCLINATION_HOHMANN_DEG
                    dv_round_trip = 2.0 * edelbaum_dv_kms(v_apo, delta_inc)
                    prop_t = propellant_mass_t(VEHICLE_TOTAL_T, dv_round_trip, ISP_VARIANT_B_S)
                    mesh_t = mesh_kg_m2 * BAG_APERTURE_M2 / 1000.0
                    total_penalty_t = prop_t + mesh_t
                    penalty_frac = total_penalty_t / VEHICLE_TOTAL_T

                    chunks_present = chunk_avail in ("rich", "thin")
                    closes_mass = penalty_frac <= TARGET_MASS_PENALTY_FRACTION

                    # Closure under each threshold (single-crossing for simplicity;
                    # extended-aperture treatment)
                    threshold_codes = {}
                    for thr_label, thr_value in THRESHOLDS.items():
                        threshold_codes[thr_label] = p_ea <= thr_value

                    # All-five-constraint at moderate threshold (the most
                    # defensible non-strict threshold; f_other ~= 0.90)
                    all_close_moderate = (
                        threshold_codes["moderate"]
                        and closes_mass
                        and chunks_present
                    )
                    # All-five at strict threshold (f_other ~ 0.95)
                    all_close_strict = (
                        threshold_codes["strict"]
                        and closes_mass
                        and chunks_present
                    )

                    rows.append({
                        "q": q,
                        "zone": zone_label,
                        "tau_total": tau_total,
                        "chunk_avail": chunk_avail,
                        "chunks_present": chunks_present,
                        "mesh": mesh_label,
                        "inclination_deg": incl,
                        "hits_per_pass": hits_per_pass,
                        "p_ea_per_pass": p_ea,
                        "penalty_fraction": round(penalty_frac, 4),
                        "closes_mass_budget": closes_mass,
                        "closes_strict_threshold": threshold_codes["strict"],
                        "closes_moderate_threshold": threshold_codes["moderate"],
                        "closes_aggressive_threshold": threshold_codes["aggressive"],
                        "ALL_CLOSE_strict": all_close_strict,
                        "ALL_CLOSE_moderate": all_close_moderate,
                    })
    return rows


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    out_dir = Path(__file__).parent / "results"
    out_dir.mkdir(parents=True, exist_ok=True)

    q_ref = body1_q_reference()
    sweep_rows = body2_combined_sweep()

    n_close_strict = sum(1 for r in sweep_rows if r["ALL_CLOSE_strict"])
    n_close_moderate = sum(1 for r in sweep_rows if r["ALL_CLOSE_moderate"])

    # Find the closing cells per q
    closing_per_q_strict = {}
    closing_per_q_moderate = {}
    for q in Q_VALUES:
        closing_per_q_strict[q] = [r for r in sweep_rows
                                    if r["q"] == q and r["ALL_CLOSE_strict"]]
        closing_per_q_moderate[q] = [r for r in sweep_rows
                                      if r["q"] == q and r["ALL_CLOSE_moderate"]]

    # Best chunk-bearing cell per q (lowest p_ea)
    best_chunk_per_q = {}
    for q in Q_VALUES:
        chunk_cells = [r for r in sweep_rows
                       if r["q"] == q and r["chunks_present"]
                       and r["closes_mass_budget"]]
        if chunk_cells:
            best_chunk_per_q[q] = min(chunk_cells, key=lambda r: r["p_ea_per_pass"])

    summary = {
        "round": "R-particle-distribution-q-sensitivity",
        "worker": "phoebe",
        "purpose": "self-question the N(D) ∝ D⁻³ particle-size-distribution anchor",
        "q_values_swept": Q_VALUES,
        "literature_q_range": "[2.5, 4.0] per Cuzzi/Tiscareno/Hedman Cassini measurements",
        "anchor_bag_aperture_m2": BAG_APERTURE_M2,
        "anchor_chunk_mass_t": CHUNK_MASS_T,
        "anchor_vehicle_total_t": VEHICLE_TOTAL_T,
        "n_cells_total": len(sweep_rows),
        "n_cells_ALL_CLOSE_strict_threshold": n_close_strict,
        "n_cells_ALL_CLOSE_moderate_threshold": n_close_moderate,
        "closing_cells_per_q_strict": {
            str(q): closing_per_q_strict[q] for q in Q_VALUES
        },
        "closing_cells_per_q_moderate": {
            str(q): closing_per_q_moderate[q] for q in Q_VALUES
        },
        "best_chunk_bearing_cell_per_q": {
            str(q): best_chunk_per_q.get(q) for q in Q_VALUES
        },
        "body1_q_reference_outermost180km_90deg_bag100m2": q_ref,
    }

    out_path = out_dir / "R_particle_distribution_q_sensitivity.json"
    out_path.write_text(json.dumps(summary, indent=2, default=str))

    # Stdout
    print("\n=== R-particle-distribution-q-sensitivity ===\n")
    print("Body 1 — q-reference at outermost-180km × 90° × bag=100m²:")
    print(f"  {'q':5s} {'mesh':12s} {'⟨σ⟩':10s} {'n_above_frac':14s} {'hits/pass':12s} {'P_ea':10s}")
    for r in q_ref:
        print(
            f"  {r['q']:5.2f} {r['mesh']:12s} "
            f"{r['sigma_mean_m2']:.3e}  {r['n_above_fraction']:.4e}  "
            f"{r['hits_per_pass']:.4e}  {r['p_ea_per_pass']:.4e}"
        )

    print(f"\nCombined sweep ({len(sweep_rows)} cells):")
    print(f"  ALL_CLOSE at STRICT threshold (1e-3): {n_close_strict}")
    print(f"  ALL_CLOSE at MODERATE threshold (2.2e-3): {n_close_moderate}")

    print(f"\nClosing cells per q (STRICT threshold):")
    for q in Q_VALUES:
        cells = closing_per_q_strict[q]
        if cells:
            print(f"  q={q}: {len(cells)} cells closing. Examples:")
            for r in cells[:5]:
                print(
                    f"    zone={r['zone']:30s} mesh={r['mesh']:10s} "
                    f"i={r['inclination_deg']:5.1f}° P_ea={r['p_ea_per_pass']:.4e} "
                    f"penalty={r['penalty_fraction']:.3f} chunks={r['chunk_avail']}"
                )
        else:
            print(f"  q={q}: 0 cells closing.")

    print(f"\nBest chunk-bearing cell per q (closes_mass AND chunks_present, lowest P_ea):")
    for q in Q_VALUES:
        r = best_chunk_per_q.get(q)
        if r:
            print(
                f"  q={q}: zone={r['zone']:30s} mesh={r['mesh']:10s} "
                f"i={r['inclination_deg']:5.1f}° P_ea={r['p_ea_per_pass']:.4e} "
                f"penalty={r['penalty_fraction']:.3f}"
            )
        else:
            print(f"  q={q}: no chunk-bearing cell satisfies mass budget.")

    print(f"\nResults written to {out_path}")


if __name__ == "__main__":
    main()
