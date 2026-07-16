#!/usr/bin/env python3
"""R-chunk-as-heat-shield-revisit (phoebe, reframed scope).

Does ANY (chunk-mass, entry-velocity) configuration close chunk-as-heat-shield
AND intersect a surviving variant cell?

Pre-registration is in STUDY.md. Central back-of-envelope estimates were
derived BEFORE range bands per recurring-lesson #N. Pessimistic-default per
Methodology lesson 1.

Reuses hyperion's R_aerocapture_fast_cruise_envelope physics functions
verbatim (import, not copy-paste). Sweeps a broader (chunk, v_infinity) cube
than hyperion did, computes closure flags and architectural intersection,
grades H-csa-* sub-claims.

Deterministic. Sub-second wall clock.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

# Import hyperion's verified physics functions
HERE = Path(__file__).resolve().parent
HYPERION_DIR = HERE.parent / "R_aerocapture_fast_cruise_envelope"
sys.path.insert(0, str(HYPERION_DIR))
import run as hyperion  # noqa: E402

# ---------------------------------------------------------------------------
# Phoebe pre-registered closure thresholds (from STUDY.md)
# ---------------------------------------------------------------------------

BAG_THERMAL_LIMIT_W_CM2 = 1.1  # Stefan-Boltzmann at 700 K, emissivity 0.8
ABLATION_LIMIT_PCT = 5.0  # delivered-fraction-degrading threshold
TENSILE_MARGIN_LIMIT = 1.0  # chunk shatters if margin < 1.0
PERIAPSIS_FLOOR_KM = 50.0  # hyperion's solver floor 40 + 10 km margin

# Tug mass anchors
TUG_T_VARIANT_B = 30.0  # 500 kWe MARVL-decomposed approximate
TUG_T_VARIANT_C = 63.8  # Round-F STRICT closing case anchor

# Sweep cube
CHUNK_T_VALUES = [25.0, 50.0, 75.0, 100.0, 150.0, 200.0, 300.0, 500.0]
V_INF_VALUES = [3.0, 5.0, 7.0, 9.0, 11.0]

# Architectural intersection probe cells
INTERSECTIONS = [
    {"name": "Variant_C_RoundF_no_LGA", "chunk_t": 200.0, "v_inf": 10.55, "tug_t": 63.8},
    {"name": "Variant_C_RoundF_with_LGA", "chunk_t": 200.0, "v_inf": 8.55, "tug_t": 63.8},
    {"name": "Variant_B_chunk200_low_vinf", "chunk_t": 200.0, "v_inf": 5.0, "tug_t": 30.0},
    {"name": "Variant_B_chunk200_mid_vinf", "chunk_t": 200.0, "v_inf": 7.0, "tug_t": 30.0},
    {"name": "Variant_B_chunk200_no_LGA", "chunk_t": 200.0, "v_inf": 8.55, "tug_t": 30.0},
    {"name": "RCAHS_original_anchor", "chunk_t": 100.0, "v_inf": 1.5, "tug_t": 30.0},
]


# ---------------------------------------------------------------------------
# Per-cell aerocapture envelope
# ---------------------------------------------------------------------------

def shallowest_viable_periapsis_km(
    v_entry_km_s: float, ballistic_coef_kg_m2: float, target_dv_km_s: float
) -> tuple[float, float]:
    """Find the SHALLOWEST (highest-altitude) periapsis where capture is feasible.

    Aerocapture optimum is the shallowest viable periapsis: minimum altitude
    that still provides target_dv, since deeper periapses give equal-or-more
    dv at higher heating cost.

    Hyperion's `required_periapsis_altitude_km` returns the *first* altitude in
    a 40→120 iteration where dv >= target. Because density decreases with
    altitude, that returns the *deepest* viable periapsis (40 km if achievable),
    which is the worst case thermally. Phoebe's broader sweep includes low-beta
    cells where the shallowest viable periapsis can be much higher than 40 km;
    this override returns the correct optimum.

    Returns (periapsis_altitude_km, pulse_duration_s). If no altitude in
    [40, 120] km satisfies target, returns (40, pulse_duration_at_40) and the
    caller's capture_feasible flag will catch it.
    """
    target_dv_m_s = target_dv_km_s * 1000.0
    v_entry_m_s = v_entry_km_s * 1000.0
    # Iterate DOWNWARD from 120 km. First altitude where dv >= target is the
    # shallowest viable periapsis.
    for alt_km in range(120, 39, -1):
        rho = hyperion.atmosphere_density(float(alt_km))
        path_length_m = 2.0 * math.sqrt(
            2.0 * (hyperion.EARTH_RADIUS_KM + alt_km) * 1000.0
            * hyperion.ATM_SCALE_HEIGHT_KM * 1000.0
        )
        dv_m_s = (rho * path_length_m / ballistic_coef_kg_m2) * v_entry_m_s
        if dv_m_s >= target_dv_m_s:
            pulse_duration_s = path_length_m / v_entry_m_s
            return float(alt_km), pulse_duration_s
    # No altitude in [40, 120] captures — fall through to floor with same
    # convention as hyperion (capture_feasible flag will be False)
    rho = hyperion.atmosphere_density(40.0)
    path_length_m = 2.0 * math.sqrt(
        2.0 * (hyperion.EARTH_RADIUS_KM + 40.0) * 1000.0
        * hyperion.ATM_SCALE_HEIGHT_KM * 1000.0
    )
    pulse_duration_s = path_length_m / v_entry_m_s
    return 40.0, pulse_duration_s


def evaluate_cell(chunk_t: float, v_inf: float, tug_t: float) -> dict:
    """Evaluate a single (chunk, velocity-at-infinity, tug) configuration."""
    total_t = chunk_t + tug_t
    v_e = hyperion.entry_velocity_at_interface_km_s(v_inf)
    beta = hyperion.ballistic_coefficient(chunk_t, total_t)
    target_dv = v_e - hyperion.EARTH_V_CIRCULAR_LEO_KM_S
    periapsis_alt, pulse_duration = shallowest_viable_periapsis_km(
        v_e, beta, target_dv
    )
    nose_r = hyperion.chunk_radius_m(chunk_t)
    front_area = hyperion.frontal_area_m2(chunk_t)
    q_peak = hyperion.sutton_graves_peak_w_cm2(v_e, periapsis_alt, nose_r)
    heat_load = hyperion.total_heat_load_J_per_m2(q_peak, pulse_duration)
    ablation_pct = hyperion.chunk_ablation_pct(heat_load, front_area, chunk_t)
    pk_g = hyperion.peak_g(v_e, pulse_duration)
    stress_pa = hyperion.chunk_internal_stress_Pa(chunk_t, pk_g)
    tensile_margin = (
        hyperion.ICE_TENSILE_STRENGTH_PA / stress_pa if stress_pa > 0 else float("inf")
    )

    bag_thermal_survives = q_peak <= BAG_THERMAL_LIMIT_W_CM2
    chunk_thermal_survives = ablation_pct <= ABLATION_LIMIT_PCT
    chunk_structural_survives = tensile_margin >= TENSILE_MARGIN_LIMIT
    capture_feasible = periapsis_alt >= PERIAPSIS_FLOOR_KM

    strict_pass = (
        bag_thermal_survives
        and chunk_thermal_survives
        and chunk_structural_survives
        and capture_feasible
    )
    sacrificial_bag_pass = (
        chunk_thermal_survives
        and chunk_structural_survives
        and capture_feasible
    )

    return {
        "chunk_t": chunk_t,
        "v_inf_km_s": v_inf,
        "tug_t": tug_t,
        "total_mass_t": total_t,
        "v_entry_km_s": v_e,
        "ballistic_coef_kg_m2": beta,
        "chunk_radius_m": nose_r,
        "periapsis_alt_km": periapsis_alt,
        "pulse_duration_s": pulse_duration,
        "q_peak_w_cm2": q_peak,
        "ablation_pct_per_pass": ablation_pct,
        "peak_g_load": pk_g,
        "internal_stress_kPa": stress_pa / 1000.0,
        "tensile_margin": tensile_margin,
        "bag_thermal_survives": bag_thermal_survives,
        "chunk_thermal_survives": chunk_thermal_survives,
        "chunk_structural_survives": chunk_structural_survives,
        "capture_feasible": capture_feasible,
        "STRICT_pass": strict_pass,
        "SACRIFICIAL_BAG_pass": sacrificial_bag_pass,
    }


# ---------------------------------------------------------------------------
# Main sweep
# ---------------------------------------------------------------------------

def run() -> dict:
    out: dict = {
        "config": {
            "bag_thermal_limit_w_cm2": BAG_THERMAL_LIMIT_W_CM2,
            "ablation_limit_pct": ABLATION_LIMIT_PCT,
            "tensile_margin_limit": TENSILE_MARGIN_LIMIT,
            "periapsis_floor_km": PERIAPSIS_FLOOR_KM,
            "tug_t_variant_B": TUG_T_VARIANT_B,
            "tug_t_variant_C": TUG_T_VARIANT_C,
            "chunk_t_sweep": CHUNK_T_VALUES,
            "v_inf_sweep_km_s": V_INF_VALUES,
            "drag_coefficient": hyperion.DRAG_COEFFICIENT_BLUNT,
            "ice_tensile_strength_Pa": hyperion.ICE_TENSILE_STRENGTH_PA,
            "earth_v_escape_interface_km_s": hyperion.EARTH_V_ESCAPE_INTERFACE_KM_S,
            "earth_v_circular_leo_km_s": hyperion.EARTH_V_CIRCULAR_LEO_KM_S,
        }
    }

    # Base sweep at Variant B tug mass (30 t)
    cells_b = []
    for chunk_t in CHUNK_T_VALUES:
        for v_inf in V_INF_VALUES:
            cells_b.append(evaluate_cell(chunk_t, v_inf, TUG_T_VARIANT_B))
    out["sweep_variant_B_tug"] = cells_b

    # Sensitivity sweep at Variant C tug mass (63.8 t) for chunk = 200 only
    cells_c = []
    for v_inf in V_INF_VALUES:
        cells_c.append(evaluate_cell(200.0, v_inf, TUG_T_VARIANT_C))
    out["sensitivity_variant_C_tug_chunk200"] = cells_c

    # Architectural intersection cells
    intersections = []
    for spec in INTERSECTIONS:
        cell = evaluate_cell(spec["chunk_t"], spec["v_inf"], spec["tug_t"])
        cell["intersection_name"] = spec["name"]
        intersections.append(cell)
    out["intersections"] = intersections

    # Cross-check vs hyperion's Round-F STRICT case (no-LGA)
    hyp_anchor = next(
        c for c in intersections if c["intersection_name"] == "Variant_C_RoundF_no_LGA"
    )
    out["cross_check_vs_hyperion"] = {
        "predicted_v_entry_km_s": 15.29,
        "computed_v_entry_km_s": hyp_anchor["v_entry_km_s"],
        "ratio": hyp_anchor["v_entry_km_s"] / 15.29,
        "predicted_envelope_pass": False,
        "computed_STRICT_pass": hyp_anchor["STRICT_pass"],
        "computed_SACRIFICIAL_BAG_pass": hyp_anchor["SACRIFICIAL_BAG_pass"],
    }

    # ---- Closing-region characterisation ----

    strict_passes_b = [c for c in cells_b if c["STRICT_pass"]]
    sacrificial_passes_b = [c for c in cells_b if c["SACRIFICIAL_BAG_pass"]]

    if sacrificial_passes_b:
        chunk_upper_bound = max(c["chunk_t"] for c in sacrificial_passes_b)
        v_inf_upper_bound = max(c["v_inf_km_s"] for c in sacrificial_passes_b)
        chunk_lower_bound = min(c["chunk_t"] for c in sacrificial_passes_b)
        v_inf_lower_bound = min(c["v_inf_km_s"] for c in sacrificial_passes_b)
    else:
        chunk_upper_bound = None
        v_inf_upper_bound = None
        chunk_lower_bound = None
        v_inf_lower_bound = None

    out["closing_region_summary"] = {
        "STRICT_pass_count_of_40": len(strict_passes_b),
        "STRICT_pass_cells": [
            {"chunk_t": c["chunk_t"], "v_inf_km_s": c["v_inf_km_s"]}
            for c in strict_passes_b
        ],
        "SACRIFICIAL_BAG_pass_count_of_40": len(sacrificial_passes_b),
        "SACRIFICIAL_BAG_pass_cells": [
            {"chunk_t": c["chunk_t"], "v_inf_km_s": c["v_inf_km_s"]}
            for c in sacrificial_passes_b
        ],
        "chunk_upper_bound_t": chunk_upper_bound,
        "v_inf_upper_bound_km_s": v_inf_upper_bound,
        "chunk_lower_bound_t": chunk_lower_bound,
        "v_inf_lower_bound_km_s": v_inf_lower_bound,
    }

    # ---- Hypothesis grading ----

    grading: dict = {}

    # H-csa-a: STRICT closing region area
    grading["H_csa_a"] = {
        "central": "empty",
        "range_count_of_40": [0, 2],
        "computed_count": len(strict_passes_b),
        "held": len(strict_passes_b) <= 2,
    }

    # H-csa-b-bound: SACRIFICIAL_BAG closing region upper bound on chunk
    if chunk_upper_bound is not None:
        held_b_chunk = 75.0 <= chunk_upper_bound <= 150.0
    else:
        held_b_chunk = False  # If no closing region exists at all, the sub-claim is vacuously not-held
    grading["H_csa_b_chunk"] = {
        "central": 100.0,
        "range_t": [75.0, 150.0],
        "computed": chunk_upper_bound,
        "held": held_b_chunk,
        "note": "vacuously not-held if SACRIFICIAL_BAG region is empty (no chunk upper bound to grade)",
    }

    # H-csa-b-vinf: SACRIFICIAL_BAG closing region upper bound on v_inf
    if v_inf_upper_bound is not None:
        held_b_vinf = 5.0 <= v_inf_upper_bound <= 8.0
    else:
        held_b_vinf = False
    grading["H_csa_b_vinf"] = {
        "central": 6.0,
        "range_km_s": [5.0, 8.0],
        "computed": v_inf_upper_bound,
        "held": held_b_vinf,
        "note": "vacuously not-held if SACRIFICIAL_BAG region is empty",
    }

    # H-csa-c: Variant C intersection (chunk 200, v_inf 8.55, tug 63.8)
    var_c_cell = next(
        c for c in intersections if c["intersection_name"] == "Variant_C_RoundF_with_LGA"
    )
    grading["H_csa_c"] = {
        "central": "no intersection",
        "predicted_SACRIFICIAL_BAG_pass": False,
        "computed_SACRIFICIAL_BAG_pass": var_c_cell["SACRIFICIAL_BAG_pass"],
        "computed_STRICT_pass": var_c_cell["STRICT_pass"],
        "held": not var_c_cell["SACRIFICIAL_BAG_pass"],
    }

    # H-csa-d: Variant B intersection (chunk 200, sweep low/mid/no-LGA v_inf)
    var_b_cells = [
        c for c in intersections
        if c["intersection_name"].startswith("Variant_B_chunk200")
    ]
    var_b_any_pass = any(c["SACRIFICIAL_BAG_pass"] for c in var_b_cells)
    var_b_passing_v_inf = [
        c["v_inf_km_s"] for c in var_b_cells if c["SACRIFICIAL_BAG_pass"]
    ]
    grading["H_csa_d"] = {
        "central": "no intersection at chunk=200",
        "predicted_SACRIFICIAL_BAG_pass": False,
        "computed_any_SACRIFICIAL_BAG_pass": var_b_any_pass,
        "computed_passing_v_inf_km_s": var_b_passing_v_inf,
        "held": not var_b_any_pass,
    }

    # H-csa-e: small-chunk multi-mission alternative (qualitative — flag if H-csa-b
    # opens a closing region at chunk <= 50 t)
    small_chunk_passing = [
        c for c in sacrificial_passes_b if c["chunk_t"] <= 50.0
    ]
    grading["H_csa_e"] = {
        "central": "small-chunk closing region exists OR is empty (qualitative)",
        "computed_chunk_le_50t_passing_count": len(small_chunk_passing),
        "computed_chunk_le_50t_v_inf_max": (
            max((c["v_inf_km_s"] for c in small_chunk_passing), default=None)
        ),
        "follow_on_flagged": len(small_chunk_passing) > 0,
        "note": "qualitative — full multi-mission cadence vs L0-05 not in scope",
    }

    # H-csa-f: orientation-stability conditional — only gradable if H-csa-c OR H-csa-d
    # is falsified (architecturally-relevant intersection exists)
    orientation_gradable = (
        not grading["H_csa_c"]["held"] or not grading["H_csa_d"]["held"]
    )
    grading["H_csa_f"] = {
        "central": "not gradable (antecedent false: no architecturally-relevant closing region)",
        "gradable_iff_intersection_exists": orientation_gradable,
        "held": "not gradable",
        "note": (
            "Conditional. Per phoebe's prior R-variant-B-100t-resizing convention: "
            "antecedent-false conditional sub-claims report 'not gradable', not "
            "'held-vacuous'."
        ),
    }

    # Aggregate H-csa-agg
    held_count = sum(
        1 for k, v in grading.items()
        if k != "aggregate" and isinstance(v.get("held"), bool) and v["held"]
    )
    gradable_count = sum(
        1 for k, v in grading.items()
        if k != "aggregate" and isinstance(v.get("held"), bool)
    )
    grading["aggregate"] = {
        "held_count": held_count,
        "gradable_count": gradable_count,
        "h_csa_agg_held": (
            grading["H_csa_a"]["held"]
            and grading["H_csa_c"]["held"]
            and grading["H_csa_d"]["held"]
        ),
        "note": (
            "H-csa-agg held iff: STRICT region empty (H-csa-a) AND no Variant C "
            "intersection (H-csa-c) AND no Variant B intersection (H-csa-d). "
            "H-csa-b sub-claims are about the BOUNDS of the SACRIFICIAL region "
            "and are diagnostic; the aggregate verdict turns on whether any "
            "architecturally-relevant intersection exists."
        ),
    }
    out["hypothesis_grading"] = grading

    return out


# ---------------------------------------------------------------------------
# Tables and writeup
# ---------------------------------------------------------------------------

def write_tables(result: dict, outdir: Path) -> None:
    lines = ["# R-chunk-as-heat-shield-revisit — results tables", ""]

    cc = result["cross_check_vs_hyperion"]
    lines.append("## Cross-check against hyperion R-aerocapture-fast-cruise-envelope")
    lines.append("")
    lines.append(f"- Hyperion's Round-F STRICT no-LGA: 15.29 km/s entry, envelope FAILS.")
    lines.append(f"- Phoebe's recompute (chunk=200 t, v_inf=10.55, tug=63.8 t): "
                 f"{cc['computed_v_entry_km_s']:.2f} km/s entry "
                 f"(ratio {cc['ratio']:.3f})")
    lines.append(f"- STRICT pass: {cc['computed_STRICT_pass']}; "
                 f"SACRIFICIAL_BAG pass: {cc['computed_SACRIFICIAL_BAG_pass']}")
    if abs(cc["ratio"] - 1.0) > 0.05:
        lines.append("**Cross-check disagrees with hyperion by > 5%.** Investigate before continuing.")
    else:
        lines.append("Cross-check inside 5% of hyperion's anchor.")
    lines.append("")

    lines.append("## Sweep at Variant B tug mass (30 t) — 8 chunk × 5 v_inf = 40 cells")
    lines.append("")
    lines.append("| chunk (t) | v_inf (km/s) | v_entry (km/s) | β (kg/m²) | periapsis (km) | "
                 "q_peak (W/cm²) | ablation (%) | peak g | margin × | bag therm | chunk therm | "
                 "chunk struct | capture | STRICT | SACR-BAG |")
    lines.append("|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|:---:|:---:|:---:|:---:|:---:|")
    for c in result["sweep_variant_B_tug"]:
        lines.append(
            f"| {c['chunk_t']:.0f} | {c['v_inf_km_s']:.1f} | {c['v_entry_km_s']:.2f} | "
            f"{c['ballistic_coef_kg_m2']:.0f} | {c['periapsis_alt_km']:.0f} | "
            f"{c['q_peak_w_cm2']:.2f} | {c['ablation_pct_per_pass']:.2f} | "
            f"{c['peak_g_load']:.1f} | {c['tensile_margin']:.2f} | "
            f"{'Y' if c['bag_thermal_survives'] else 'N'} | "
            f"{'Y' if c['chunk_thermal_survives'] else 'N'} | "
            f"{'Y' if c['chunk_structural_survives'] else 'N'} | "
            f"{'Y' if c['capture_feasible'] else 'N'} | "
            f"{'Y' if c['STRICT_pass'] else 'N'} | "
            f"{'Y' if c['SACRIFICIAL_BAG_pass'] else 'N'} |"
        )
    lines.append("")

    lines.append("## Sensitivity at Variant C tug mass (63.8 t) — chunk = 200 t only")
    lines.append("")
    lines.append("| chunk (t) | v_inf (km/s) | v_entry (km/s) | β (kg/m²) | periapsis (km) | "
                 "q_peak (W/cm²) | ablation (%) | peak g | margin × | STRICT | SACR-BAG |")
    lines.append("|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|:---:|")
    for c in result["sensitivity_variant_C_tug_chunk200"]:
        lines.append(
            f"| {c['chunk_t']:.0f} | {c['v_inf_km_s']:.1f} | {c['v_entry_km_s']:.2f} | "
            f"{c['ballistic_coef_kg_m2']:.0f} | {c['periapsis_alt_km']:.0f} | "
            f"{c['q_peak_w_cm2']:.2f} | {c['ablation_pct_per_pass']:.2f} | "
            f"{c['peak_g_load']:.1f} | {c['tensile_margin']:.2f} | "
            f"{'Y' if c['STRICT_pass'] else 'N'} | "
            f"{'Y' if c['SACRIFICIAL_BAG_pass'] else 'N'} |"
        )
    lines.append("")

    lines.append("## Architectural intersection cells")
    lines.append("")
    lines.append("| Intersection | chunk (t) | v_inf (km/s) | tug (t) | v_entry (km/s) | "
                 "periapsis (km) | q_peak (W/cm²) | ablation (%) | peak g | margin × | STRICT | SACR-BAG |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|:---:|")
    for c in result["intersections"]:
        lines.append(
            f"| {c['intersection_name']} | {c['chunk_t']:.0f} | {c['v_inf_km_s']:.2f} | "
            f"{c['tug_t']:.1f} | {c['v_entry_km_s']:.2f} | "
            f"{c['periapsis_alt_km']:.0f} | {c['q_peak_w_cm2']:.2f} | "
            f"{c['ablation_pct_per_pass']:.2f} | "
            f"{c['peak_g_load']:.1f} | {c['tensile_margin']:.2f} | "
            f"{'Y' if c['STRICT_pass'] else 'N'} | "
            f"{'Y' if c['SACRIFICIAL_BAG_pass'] else 'N'} |"
        )
    lines.append("")

    lines.append("## Closing-region summary")
    lines.append("")
    cr = result["closing_region_summary"]
    lines.append(f"- STRICT (bag-retained) closing cells of 40: **{cr['STRICT_pass_count_of_40']}**")
    if cr["STRICT_pass_count_of_40"] > 0:
        lines.append(f"  - Cells: {cr['STRICT_pass_cells']}")
    lines.append(f"- SACRIFICIAL_BAG closing cells of 40: **{cr['SACRIFICIAL_BAG_pass_count_of_40']}**")
    if cr["SACRIFICIAL_BAG_pass_count_of_40"] > 0:
        lines.append(f"  - Chunk bound: [{cr['chunk_lower_bound_t']:.0f}, "
                     f"{cr['chunk_upper_bound_t']:.0f}] t")
        lines.append(f"  - v_inf bound: [{cr['v_inf_lower_bound_km_s']:.1f}, "
                     f"{cr['v_inf_upper_bound_km_s']:.1f}] km/s")
    lines.append("")

    lines.append("## Hypothesis grading")
    lines.append("")
    lines.append("| Sub-claim | Central | Predicted range | Computed | Held |")
    lines.append("|---|---|---|---|:---:|")
    for k, v in result["hypothesis_grading"].items():
        if k == "aggregate":
            continue
        ctr = v.get("central", "?")
        rng = (
            v.get("range_count_of_40")
            or v.get("range_t")
            or v.get("range_km_s")
            or v.get("predicted_SACRIFICIAL_BAG_pass", "")
        )
        comp = (
            v.get("computed")
            or v.get("computed_count")
            or v.get("computed_SACRIFICIAL_BAG_pass")
            or v.get("computed_any_SACRIFICIAL_BAG_pass")
            or v.get("computed_chunk_le_50t_passing_count")
            or "n/a"
        )
        held = v.get("held", "n/a")
        lines.append(f"| {k} | {ctr} | {rng} | {comp} | {held} |")
    agg = result["hypothesis_grading"]["aggregate"]
    lines.append("")
    lines.append(f"**Aggregate H-csa-agg: {'HELD' if agg['h_csa_agg_held'] else 'FALSIFIED'}** "
                 f"({agg['held_count']} of {agg['gradable_count']} gradable sub-claims held)")
    lines.append("")
    lines.append(agg["note"])

    (outdir / "tables.md").write_text("\n".join(lines))


def main() -> None:
    outdir = HERE / "results"
    outdir.mkdir(parents=True, exist_ok=True)
    result = run()
    (outdir / "R_chunk_as_heat_shield_revisit.json").write_text(
        json.dumps(result, indent=2, default=float)
    )
    write_tables(result, outdir)

    # Console summary
    cc = result["cross_check_vs_hyperion"]
    print(f"Cross-check vs hyperion Round-F STRICT no-LGA: "
          f"v_entry {cc['computed_v_entry_km_s']:.2f} km/s "
          f"(ratio {cc['ratio']:.3f}), "
          f"STRICT pass = {cc['computed_STRICT_pass']}, "
          f"SACR-BAG pass = {cc['computed_SACRIFICIAL_BAG_pass']}")

    cr = result["closing_region_summary"]
    print(f"Closing region: STRICT {cr['STRICT_pass_count_of_40']}/40, "
          f"SACR-BAG {cr['SACRIFICIAL_BAG_pass_count_of_40']}/40")
    if cr["SACRIFICIAL_BAG_pass_count_of_40"] > 0:
        print(f"  SACR-BAG chunk bound: [{cr['chunk_lower_bound_t']:.0f}, "
              f"{cr['chunk_upper_bound_t']:.0f}] t; "
              f"v_inf bound: [{cr['v_inf_lower_bound_km_s']:.1f}, "
              f"{cr['v_inf_upper_bound_km_s']:.1f}] km/s")

    g = result["hypothesis_grading"]
    print(f"Hypothesis grading: H-csa-a={g['H_csa_a']['held']}, "
          f"H-csa-b-chunk={g['H_csa_b_chunk']['held']}, "
          f"H-csa-b-vinf={g['H_csa_b_vinf']['held']}, "
          f"H-csa-c={g['H_csa_c']['held']}, "
          f"H-csa-d={g['H_csa_d']['held']}, "
          f"H-csa-f={g['H_csa_f']['held']}")
    agg = g["aggregate"]
    print(f"Aggregate H-csa-agg: {'HELD' if agg['h_csa_agg_held'] else 'FALSIFIED'} "
          f"({agg['held_count']}/{agg['gradable_count']} gradable held)")


if __name__ == "__main__":
    main()
