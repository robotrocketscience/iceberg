"""R-variant-B-100t-resizing — does chunk reduction to 100 tonnes per mission
rescue Variant B without aerocapture?

Reuses hyperion's R_variant_B_impulsive_vs_continuous closure function with
chunk_t and reactor_kwe as swept parameters. Variant A architecture only
(no aerocapture, no Saturn-egress chemical kick).

See STUDY.md for the pre-registered hypothesis block.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

# Import hyperion's closure function and constants.
_HYPERION_ROUND = (Path(__file__).parent.parent / "R_variant_B_impulsive_vs_continuous").resolve()
sys.path.insert(0, str(_HYPERION_ROUND))
from run import (  # type: ignore  # noqa: E402
    DV_SATURN_SPIRAL_KM_S,
    DV_HELIO_RETROGRADE_KM_S,
    DV_EARTH_HELIO_KM_S,
    DV_LEO_SPIRAL_KM_S,
    LGA_CREDIT_KM_S,
    ISP_ELECTRIC_S,
    DV_CHEM_OUTBOUND_KM_S,
    M_OUTBOUND_KICK_DRY_T,
    M_SATURN_KICK_DRY_T,
    ROUND_TRIP_CEILING_YR,
    ROUND_TRIP_SOFT_MARGIN_YR,
    variant_b_closure,
    variant_inbound_dv,
)

R_POWER_BAYESIAN_OVERLAY = (
    Path(__file__).parent.parent / "R_power_bayesian_update" / "results" / "matrix_overlay.json"
)

DEPARTURE_DEFAULT = "high_elliptical_1Mkm"

# Sweep ranges (per SCOPE.md method §1-§4)
CHUNK_SWEEP_T = [50.0, 75.0, 100.0, 125.0, 150.0, 175.0, 200.0]
REACTOR_SWEEP_KWE = [100.0, 200.0, 300.0, 400.0, 500.0, 600.0, 700.0]

CHUNK_TARGET_T = 100.0           # path-3 focal point
REACTOR_DEFAULT_KWE = 500.0      # for chunk sweep
SANITY_CHUNK_T = 200.0           # hyperion baseline reproduce
SANITY_REACTOR_KWE = 500.0
SANITY_HYPERION_RT_YR = 16.92
SANITY_HYPERION_DELIVERED_T = 0.0  # chunk-fully-consumed edge


def closure_variant_A(chunk_t: float, reactor_kwe: float) -> dict:
    """Variant A (no recovery): pure electric inbound, no Saturn-egress kick, no aerocapture."""
    v = variant_inbound_dv("A_as_stated", DEPARTURE_DEFAULT)
    return variant_b_closure(
        reactor_kwe=reactor_kwe,
        chunk_t=chunk_t,
        isp_electric_s=ISP_ELECTRIC_S,
        dv_chem_outbound_km_s=DV_CHEM_OUTBOUND_KM_S,
        dv_inbound_electric_km_s=v["electric_dv_km_s"],
        dv_inbound_impulsive_km_s=v["impulsive_egress_dv_km_s"],
        aerocapture=False,
        m_outbound_kick_dry_t=M_OUTBOUND_KICK_DRY_T,
        m_saturn_kick_dry_t=M_SATURN_KICK_DRY_T,
    )


def main() -> dict:
    inbound_dv = variant_inbound_dv("A_as_stated", DEPARTURE_DEFAULT)

    # === Sanity check: chunk=200, P=500 should match hyperion's published number ===
    sanity = closure_variant_A(SANITY_CHUNK_T, SANITY_REACTOR_KWE)
    if sanity.get("feasible"):
        sanity_rt = sanity["round_trip_yr"]
        sanity_delivered = sanity["delivered_t"]
    else:
        # Infeasible edge — hyperion's printed table reports 0.0 t delivered at this point,
        # but the underlying code path returns feasible=False with delivered slightly negative.
        sanity_rt = float("nan")
        sanity_delivered = sanity.get("delivered_t", float("nan"))
    sanity_check = {
        "config": {"chunk_t": SANITY_CHUNK_T, "reactor_kwe": SANITY_REACTOR_KWE},
        "hyperion_round_trip_yr": SANITY_HYPERION_RT_YR,
        "hyperion_delivered_t": SANITY_HYPERION_DELIVERED_T,
        "ours_feasible": sanity.get("feasible"),
        "ours_round_trip_yr": sanity_rt,
        "ours_delivered_t": sanity_delivered,
        "ours_m_prop_inbound_t": sanity.get("m_prop_inbound_t"),
        "ours_m_tug_t": sanity.get("m_tug_t"),
        "ours_full_result": sanity,
    }

    # === Sweep 1: chunk sweep at reactor=500 kWe, Variant A ===
    chunk_sweep_rows = []
    for chunk in CHUNK_SWEEP_T:
        r = closure_variant_A(chunk, REACTOR_DEFAULT_KWE)
        r["chunk_t"] = chunk
        r["reactor_kwe"] = REACTOR_DEFAULT_KWE
        chunk_sweep_rows.append(r)

    # === Sweep 2: reactor sweep at chunk=100 t, Variant A ===
    reactor_sweep_rows = []
    for kwe in REACTOR_SWEEP_KWE:
        r = closure_variant_A(CHUNK_TARGET_T, kwe)
        r["chunk_t"] = CHUNK_TARGET_T
        r["reactor_kwe"] = kwe
        reactor_sweep_rows.append(r)

    # === Closure boundary identification ===
    # In the chunk sweep, find the (highest, lowest) chunk that closes strict / soft, if any.
    closing_strict_chunks = [
        r["chunk_t"] for r in chunk_sweep_rows
        if r.get("feasible") and r.get("closes_strict_15yr") and r.get("delivered_t", 0) > 0
    ]
    closing_soft_chunks = [
        r["chunk_t"] for r in chunk_sweep_rows
        if r.get("feasible") and r.get("closes_soft_16yr") and r.get("delivered_t", 0) > 0
    ]

    # In the reactor sweep at chunk=100 t, find any closing reactor power.
    closing_strict_reactors = [
        r["reactor_kwe"] for r in reactor_sweep_rows
        if r.get("feasible") and r.get("closes_strict_15yr") and r.get("delivered_t", 0) > 0
    ]
    closing_soft_reactors = [
        r["reactor_kwe"] for r in reactor_sweep_rows
        if r.get("feasible") and r.get("closes_soft_16yr") and r.get("delivered_t", 0) > 0
    ]

    # Operating optimum: among closing rows, the one minimising round-trip.
    closing_rows_in_reactor_sweep = [
        r for r in reactor_sweep_rows
        if r.get("feasible") and r.get("closes_soft_16yr") and r.get("delivered_t", 0) > 0
    ]
    if closing_rows_in_reactor_sweep:
        operating_optimum = min(closing_rows_in_reactor_sweep, key=lambda r: r["round_trip_yr"])
    else:
        operating_optimum = None

    # === Programmatic-risk overlay (uniform Beta(1,1) prior) ===
    p_uniform = None
    if R_POWER_BAYESIAN_OVERLAY.exists():
        overlay = json.loads(R_POWER_BAYESIAN_OVERLAY.read_text())
        try:
            p_uniform = (
                overlay["variant_B_500kWe_chemical_kick_plus_electric_inbound"][
                    "expected_delivered_mass_by_prior"
                ]["uniform_beta_1_1"]["p_reactor_available_by_window"]
            )
        except (KeyError, TypeError):
            p_uniform = None
    for rows in (chunk_sweep_rows, reactor_sweep_rows):
        for r in rows:
            if r.get("feasible") and p_uniform is not None:
                d = max(r.get("delivered_t", 0.0), 0.0)
                r["expected_delivered_t_uniform"] = d * p_uniform

    # === Best path-3 delivered mass for path-1-vs-path-3 comparison ===
    feasible_closing_deliveries = [
        r["delivered_t"] for r in (chunk_sweep_rows + reactor_sweep_rows)
        if r.get("feasible") and r.get("closes_soft_16yr") and r.get("delivered_t", 0) > 0
    ]
    best_path3_delivered_t = max(feasible_closing_deliveries) if feasible_closing_deliveries else 0.0

    # === Hypothesis grading ===
    # H-100-a: chunk=100, 500 kWe Variant A is propellant-infeasible
    a_row = next(
        (r for r in chunk_sweep_rows if r["chunk_t"] == CHUNK_TARGET_T),
        None,
    )
    h_100_a = {
        "predicted": "propellant-infeasible (m_prop > chunk)",
        "actual_feasible": a_row.get("feasible") if a_row else None,
        "actual_m_prop_t": a_row.get("m_prop_required_t") if (a_row and not a_row.get("feasible")) else a_row.get("m_prop_inbound_t") if a_row else None,
        "actual_delivered_t": a_row.get("delivered_t") if a_row else None,
        # Phoebe pre-registered "infeasible" -> held if NOT feasible
        "held": a_row is not None and not a_row.get("feasible", True),
    }

    # H-100-b: no chunk in [50, 200] closes strict
    h_100_b_strict = {
        "predicted": "no chunk in [50, 200] t at 500 kWe Variant A closes strict 15-yr AND is feasible",
        "closing_strict_chunks": closing_strict_chunks,
        "held": len(closing_strict_chunks) == 0,
    }
    h_100_b_soft = {
        "predicted": "no chunk in [50, 200] t at 500 kWe Variant A closes soft 16-yr AND is feasible",
        "closing_soft_chunks": closing_soft_chunks,
        "held": len(closing_soft_chunks) == 0,
    }

    # H-100-c: no reactor in [100, 700] kWe at chunk=100 t closes soft 16-yr AND is feasible
    h_100_c = {
        "predicted": "no reactor power in [100, 700] kWe at chunk=100 t Variant A is feasible AND closes soft 16-yr",
        "closing_soft_reactors": closing_soft_reactors,
        "closing_strict_reactors": closing_strict_reactors,
        "held": len(closing_soft_reactors) == 0,
    }

    # H-100-d: optimum reactor power at chunk=100 t is in [200, 400] kWe IF closure exists
    if operating_optimum is not None:
        opt_kwe = operating_optimum["reactor_kwe"]
        h_100_d = {
            "predicted_range_kwe": [200.0, 400.0],
            "optimum_kwe": opt_kwe,
            "optimum_round_trip_yr": operating_optimum["round_trip_yr"],
            "optimum_delivered_t": operating_optimum["delivered_t"],
            "held": 200.0 <= opt_kwe <= 400.0,
            "gradable": True,
        }
    else:
        h_100_d = {
            "predicted_range_kwe": [200.0, 400.0],
            "optimum_kwe": None,
            "held": None,
            "gradable": False,
            "note": "no closing cell exists; H-100-d not gradable",
        }

    # H-100-e: any closing path-3 delivered < 32.1 t (hyperion's path-1 Variant C)
    HYPERION_VARIANT_C_DELIVERED_T = 32.1
    h_100_e = {
        "predicted": "best path-3 closing delivered mass < 32.1 t (hyperion Variant C, path 1)",
        "best_path3_delivered_t": best_path3_delivered_t,
        "hyperion_path1_delivered_t": HYPERION_VARIANT_C_DELIVERED_T,
        "held": best_path3_delivered_t < HYPERION_VARIANT_C_DELIVERED_T,
        "gradable": best_path3_delivered_t > 0,
    }

    results = {
        "config": {
            "departure_orbit": DEPARTURE_DEFAULT,
            "isp_electric_s": ISP_ELECTRIC_S,
            "variant": "A_as_stated (no aerocapture, no Saturn-egress kick)",
            "dv_inbound_electric_km_s": inbound_dv["electric_dv_km_s"],
            "dv_inbound_breakdown": inbound_dv,
            "chunk_sweep_t": CHUNK_SWEEP_T,
            "reactor_sweep_kwe": REACTOR_SWEEP_KWE,
            "chunk_target_t": CHUNK_TARGET_T,
            "reactor_default_kwe": REACTOR_DEFAULT_KWE,
            "ceiling_yr": ROUND_TRIP_CEILING_YR,
            "soft_margin_yr": ROUND_TRIP_SOFT_MARGIN_YR,
            "p_uniform_overlay": p_uniform,
        },
        "sanity_check_chunk200_500kWe": sanity_check,
        "chunk_sweep_at_500kWe_variantA": chunk_sweep_rows,
        "reactor_sweep_at_chunk100_variantA": reactor_sweep_rows,
        "closure_boundary": {
            "closing_strict_chunks_500kWe": closing_strict_chunks,
            "closing_soft_chunks_500kWe": closing_soft_chunks,
            "closing_strict_reactors_chunk100": closing_strict_reactors,
            "closing_soft_reactors_chunk100": closing_soft_reactors,
        },
        "operating_optimum_chunk100": operating_optimum,
        "best_path3_delivered_t": best_path3_delivered_t,
        "hypothesis_grading": {
            "H-100-a_chunk100_500kWe_infeasible": h_100_a,
            "H-100-b_strict_no_closing_chunk_at_500kWe": h_100_b_strict,
            "H-100-b_soft_no_closing_chunk_at_500kWe": h_100_b_soft,
            "H-100-c_no_closing_reactor_at_chunk100": h_100_c,
            "H-100-d_optimum_reactor_in_200_400_band": h_100_d,
            "H-100-e_path3_delivered_under_321t": h_100_e,
        },
    }

    out_dir = Path(__file__).parent / "results"
    out_dir.mkdir(exist_ok=True)
    (out_dir / "R_variant_B_100t_resizing.json").write_text(
        json.dumps(results, indent=2, default=str)
    )

    # === Tables ===
    lines = []
    lines.append(f"### Sanity check vs hyperion R-variant-B-impulsive-vs-continuous (Variant A, chunk 200 t, 500 kWe)\n")
    lines.append(f"- Hyperion published: round-trip {SANITY_HYPERION_RT_YR:.2f} yr, delivered {SANITY_HYPERION_DELIVERED_T:.2f} t.")
    lines.append(f"- Reproduced (phoebe): feasible={sanity_check['ours_feasible']}, round-trip {sanity_check['ours_round_trip_yr']} yr, delivered {sanity_check['ours_delivered_t']} t, m_prop_inbound {sanity_check.get('ours_m_prop_inbound_t', 'N/A')} t.\n")

    lines.append(f"### Inbound delta-velocity (Variant A, {DEPARTURE_DEFAULT}, with Lunar Gravity Assist credit)\n")
    lines.append(f"- Saturn spiral: {inbound_dv['saturn_spiral_km_s']:.3f} km/s")
    lines.append(f"- Heliocentric retrograde: {inbound_dv['helio_retrograde_km_s']:.3f} km/s")
    lines.append(f"- Earth heliocentric: {inbound_dv['earth_helio_km_s']:.3f} km/s")
    lines.append(f"- LEO spiral: {inbound_dv['leo_spiral_km_s']:.3f} km/s")
    lines.append(f"- LGA credit: -{inbound_dv['lga_credit_km_s']:.1f} km/s")
    lines.append(f"- **Total electric inbound DV: {inbound_dv['electric_dv_km_s']:.3f} km/s**\n")

    lines.append(f"### Sweep 1 — chunk sweep at 500 kWe Variant A (electric inbound 27.57 km/s, MARVL mass, Isp 2000 s)\n")
    lines.append("| Chunk (t) | Feasible? | Tug (t) | m_prop_inbound (t) | Delivered (t) | Fraction | t_burn (yr) | Round-trip (yr) | Strict 15? | Soft 16? | Expected (uniform, t) |")
    lines.append("|---:|:--:|---:|---:|---:|---:|---:|---:|:--:|:--:|---:|")
    for r in chunk_sweep_rows:
        if not r.get("feasible"):
            lines.append(
                f"| {r['chunk_t']:.0f} | **no** | "
                f"{r.get('m_tug_t', float('nan')):.1f} | "
                f"{r.get('m_prop_required_t', float('nan')):.1f} (required) | "
                f"{r.get('delivered_t', float('nan')):.1f} (deficit) | "
                f"— | — | ∞ | no | no | 0 |"
            )
            continue
        flag_strict = "**yes**" if r.get("closes_strict_15yr") else "no"
        flag_soft = "**yes**" if r.get("closes_soft_16yr") else "no"
        lines.append(
            f"| {r['chunk_t']:.0f} | yes | {r['m_tug_t']:.1f} | {r['m_prop_inbound_t']:.1f} | "
            f"{r['delivered_t']:.1f} | {r['delivered_fraction']:.3f} | "
            f"{r['t_inbound_burn_yr']:.2f} | {r['round_trip_yr']:.2f} | "
            f"{flag_strict} | {flag_soft} | "
            f"{r.get('expected_delivered_t_uniform', 0):.4f} |"
        )
    lines.append("")

    lines.append(f"### Sweep 2 — reactor sweep at chunk 100 t Variant A\n")
    lines.append("| Reactor (kWe) | Feasible? | Tug (t) | m_prop_inbound (t) | Delivered (t) | Fraction | t_burn (yr) | Round-trip (yr) | Strict 15? | Soft 16? | Expected (uniform, t) |")
    lines.append("|---:|:--:|---:|---:|---:|---:|---:|---:|:--:|:--:|---:|")
    for r in reactor_sweep_rows:
        if not r.get("feasible"):
            lines.append(
                f"| {r['reactor_kwe']:.0f} | **no** | "
                f"{r.get('m_tug_t', float('nan')):.1f} | "
                f"{r.get('m_prop_required_t', float('nan')):.1f} (required) | "
                f"{r.get('delivered_t', float('nan')):.1f} (deficit) | "
                f"— | — | ∞ | no | no | 0 |"
            )
            continue
        flag_strict = "**yes**" if r.get("closes_strict_15yr") else "no"
        flag_soft = "**yes**" if r.get("closes_soft_16yr") else "no"
        lines.append(
            f"| {r['reactor_kwe']:.0f} | yes | {r['m_tug_t']:.1f} | {r['m_prop_inbound_t']:.1f} | "
            f"{r['delivered_t']:.1f} | {r['delivered_fraction']:.3f} | "
            f"{r['t_inbound_burn_yr']:.2f} | {r['round_trip_yr']:.2f} | "
            f"{flag_strict} | {flag_soft} | "
            f"{r.get('expected_delivered_t_uniform', 0):.4f} |"
        )
    lines.append("")

    lines.append("### Closure boundary summary\n")
    lines.append(f"- Chunk sweep at 500 kWe: chunks that close strict 15-yr AND feasible: **{closing_strict_chunks or 'none'}**")
    lines.append(f"- Chunk sweep at 500 kWe: chunks that close soft 16-yr AND feasible: **{closing_soft_chunks or 'none'}**")
    lines.append(f"- Reactor sweep at chunk 100 t: reactor powers that close strict 15-yr AND feasible: **{closing_strict_reactors or 'none'}**")
    lines.append(f"- Reactor sweep at chunk 100 t: reactor powers that close soft 16-yr AND feasible: **{closing_soft_reactors or 'none'}**\n")

    if operating_optimum is not None:
        lines.append(f"### Operating optimum at chunk 100 t Variant A\n")
        lines.append(f"- Reactor power: {operating_optimum['reactor_kwe']:.0f} kWe")
        lines.append(f"- Round-trip: {operating_optimum['round_trip_yr']:.2f} yr")
        lines.append(f"- Delivered: {operating_optimum['delivered_t']:.2f} t")
        lines.append(f"- Tug: {operating_optimum['m_tug_t']:.1f} t")
        lines.append(f"- Expected delivered (uniform): {operating_optimum.get('expected_delivered_t_uniform', 0):.4f} t\n")
    else:
        lines.append("### Operating optimum at chunk 100 t Variant A\n")
        lines.append("- **No closing cell exists in the reactor sweep [100, 700] kWe at chunk 100 t.**\n")

    lines.append("### Hypothesis grading\n")
    lines.append("| Sub-claim | Predicted | Measured | Held? |")
    lines.append("|---|---|---|---|")
    h = results["hypothesis_grading"]
    for name, v in h.items():
        if v.get("gradable") is False:
            lines.append(f"| {name} | {v.get('predicted', v.get('predicted_range_kwe', ''))} | n/a (no closing cell) | not gradable |")
            continue
        held_flag = (
            "**yes**" if v.get("held") is True else
            "**no**" if v.get("held") is False else
            "n/a"
        )
        if "predicted_range_kwe" in v:
            lines.append(
                f"| {name} | optimum in {v['predicted_range_kwe'][0]:.0f}-{v['predicted_range_kwe'][1]:.0f} kWe | "
                f"optimum = {v.get('optimum_kwe', 'N/A')} kWe (round-trip {v.get('optimum_round_trip_yr', 'N/A')} yr, delivered {v.get('optimum_delivered_t', 'N/A')} t) | {held_flag} |"
            )
        else:
            measured_bits = []
            for k in ("actual_feasible", "actual_m_prop_t", "actual_delivered_t",
                      "closing_strict_chunks", "closing_soft_chunks",
                      "closing_soft_reactors", "closing_strict_reactors",
                      "best_path3_delivered_t"):
                if k in v and v[k] is not None:
                    measured_bits.append(f"{k}={v[k]}")
            lines.append(f"| {name} | {v.get('predicted', '')} | {'; '.join(measured_bits)} | {held_flag} |")

    (out_dir / "tables.md").write_text("\n".join(lines))
    return results


if __name__ == "__main__":
    out = main()
    print("R-variant-B-100t-resizing complete.\n")

    s = out["sanity_check_chunk200_500kWe"]
    print(f"Sanity check (chunk 200 t, 500 kWe Variant A):")
    print(f"  hyperion published: round-trip {s['hyperion_round_trip_yr']:.2f} yr, delivered {s['hyperion_delivered_t']:.2f} t")
    print(f"  phoebe reproduced:  feasible={s['ours_feasible']}, round-trip {s['ours_round_trip_yr']}, "
          f"delivered {s['ours_delivered_t']}")
    print()

    print("Chunk sweep at 500 kWe Variant A:")
    for r in out["chunk_sweep_at_500kWe_variantA"]:
        if not r.get("feasible"):
            print(f"  chunk {r['chunk_t']:6.0f} t: INFEASIBLE (m_prop required {r.get('m_prop_required_t', float('nan')):.1f} t > chunk)")
            continue
        print(f"  chunk {r['chunk_t']:6.0f} t: round-trip {r['round_trip_yr']:5.2f} yr, "
              f"delivered {r['delivered_t']:6.2f} t (frac {r['delivered_fraction']:.3f}), "
              f"closes_soft={r['closes_soft_16yr']}")
    print()

    print("Reactor sweep at chunk 100 t Variant A:")
    for r in out["reactor_sweep_at_chunk100_variantA"]:
        if not r.get("feasible"):
            print(f"  reactor {r['reactor_kwe']:5.0f} kWe: INFEASIBLE (m_prop required {r.get('m_prop_required_t', float('nan')):.1f} t > chunk 100 t)")
            continue
        print(f"  reactor {r['reactor_kwe']:5.0f} kWe: round-trip {r['round_trip_yr']:5.2f} yr, "
              f"delivered {r['delivered_t']:6.2f} t, closes_soft={r['closes_soft_16yr']}")
    print()

    print("Closure boundary:")
    cb = out["closure_boundary"]
    print(f"  chunks closing strict 15 yr at 500 kWe: {cb['closing_strict_chunks_500kWe'] or 'NONE'}")
    print(f"  chunks closing soft   16 yr at 500 kWe: {cb['closing_soft_chunks_500kWe'] or 'NONE'}")
    print(f"  reactors closing strict 15 yr at chunk 100 t: {cb['closing_strict_reactors_chunk100'] or 'NONE'}")
    print(f"  reactors closing soft   16 yr at chunk 100 t: {cb['closing_soft_reactors_chunk100'] or 'NONE'}")
    print()

    print("Hypothesis grading:")
    for k, v in out["hypothesis_grading"].items():
        held = v.get("held")
        verdict = "HELD" if held is True else "FALSIFIED" if held is False else "NOT GRADABLE"
        print(f"  {k}: {verdict}")
