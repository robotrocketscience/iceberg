"""Round 8 — Inbound delta-velocity budget audit for the ICEBERG return leg.

Reconciles three competing budgets for the chunk-fed inbound delta-velocity:
  (1) The ICEBERG conops 3.7 km/s total water-microwave-electrothermal-thruster allocation.
  (2) R2's revised 5.2 km/s chunk-fed inbound budget after the lunar gravity
      assist falsification.
  (3) First-principles patched-conic rebuild from Hohmann transfer endpoint
      velocities, Saturn-side gravity-well egress, and lunar-gravity-assist
      arrival capability.

Hypothesis pre-registered in STUDY.md before this script runs.

Closed-form only; no integration. Saturn orbit eccentricity and inclination
neglected (sensitivity caveats in STUDY.md).
"""

from __future__ import annotations

import json
import math
from pathlib import Path

from waterprop.constants import (
    A_EARTH,
    A_SATURN,
    G0,
    GM_EARTH,
    GM_SATURN,
    GM_SUN,
)

# Inputs (locked before run; mirrors conops + R-prior numbers)
SATURN_BRING_RADIUS_KM = 1.35e5  # mid-B-ring orbit radius; conops Phase 5
SATURN_CAPTURE_DV_KM_S = 0.6  # conops Phase 4
SATURN_RENDEZVOUS_IN_DV_KM_S = 1.49  # conops Phase 5 ("ring rendezvous")
CONOPS_TOTAL_WATERMET_DV_KM_S = 3.7  # conops "11 km/s round-trip minus 7.3 TSI"

CONOPS_TSI_DV_KM_S = 7.3  # conops Phase 2
R6_REVISED_CHUNKFED_INBOUND_DV_KM_S = 5.2  # R6 input table
R2_LGA_AT_VINF_6_KM_S = 2.15  # midpoint of R2 result 2.0-2.3 at v_inf 6
R2_LGA_AT_VINF_4_KM_S = 3.24  # R2 result at v_inf 4

WATER_MET_ISP_S = 500.0  # mid-band per R0 (416-558 s for water microwave electrothermal)
GRAPPLED_CHUNK_T = 14.0  # conops Phase 6 stated chunk mass
DRY_SPACECRAFT_T = 5.0  # conops "operator-side mass ~5 t at Saturn arrival"


def hohmann_endpoint_velocities(a1_km: float, a2_km: float) -> dict[str, float]:
    """Patched-conic Hohmann transfer endpoint velocities between heliocentric a1 and a2.

    Returns velocities relative to the Sun at perihelion and aphelion.
    """
    a_inner = min(a1_km, a2_km)
    a_outer = max(a1_km, a2_km)
    a_transfer = 0.5 * (a_inner + a_outer)
    v_perihelion = math.sqrt(GM_SUN * (2.0 / a_inner - 1.0 / a_transfer))
    v_aphelion = math.sqrt(GM_SUN * (2.0 / a_outer - 1.0 / a_transfer))
    v_body_inner = math.sqrt(GM_SUN / a_inner)
    v_body_outer = math.sqrt(GM_SUN / a_outer)
    return {
        "a_transfer_km": a_transfer,
        "v_perihelion_km_s": v_perihelion,
        "v_aphelion_km_s": v_aphelion,
        "v_inner_orbital_km_s": v_body_inner,
        "v_outer_orbital_km_s": v_body_outer,
        "v_inf_at_inner_km_s": abs(v_perihelion - v_body_inner),
        "v_inf_at_outer_km_s": abs(v_aphelion - v_body_outer),
    }


def saturn_escape_dv_from_circular_orbit(r_burn_km: float, v_inf_km_s: float) -> dict[str, float]:
    """Impulsive single-burn delta-velocity from a circular Saturn orbit to a
    hyperbolic trajectory with the given velocity-at-infinity at Saturn.
    """
    v_circ = math.sqrt(GM_SATURN / r_burn_km)
    v_burn = math.sqrt(v_inf_km_s ** 2 + 2.0 * GM_SATURN / r_burn_km)
    return {
        "r_burn_km": r_burn_km,
        "v_circ_km_s": v_circ,
        "v_burn_km_s": v_burn,
        "delta_v_km_s": v_burn - v_circ,
        "v_esc_km_s": math.sqrt(2.0 * GM_SATURN / r_burn_km),
    }


def saturn_hohmann_from_bring_to_ellipse(r_ring_km: float, r_apo_km: float) -> dict[str, float]:
    """Patched-conic Hohmann transfer within Saturn's gravity well.

    From B-ring circular orbit (r_ring) up to apoapsis at r_apo. Returns the
    burn-1 delta-velocity at the B-ring radius.
    """
    a_t = 0.5 * (r_ring_km + r_apo_km)
    v_circ_ring = math.sqrt(GM_SATURN / r_ring_km)
    v_peri = math.sqrt(GM_SATURN * (2.0 / r_ring_km - 1.0 / a_t))
    return {
        "r_ring_km": r_ring_km,
        "r_apo_km": r_apo_km,
        "v_circ_ring_km_s": v_circ_ring,
        "v_peri_km_s": v_peri,
        "burn1_dv_km_s": v_peri - v_circ_ring,
    }


def tsiolkovsky_propellant_fraction(delta_v_m_s: float, v_e_m_s: float) -> float:
    """Propellant mass fraction = 1 - exp(-dV / v_e). Pure function."""
    return 1.0 - math.exp(-delta_v_m_s / v_e_m_s)


def main() -> dict:
    results: dict = {"inputs": {
        "saturn_bring_radius_km": SATURN_BRING_RADIUS_KM,
        "saturn_capture_dv_km_s": SATURN_CAPTURE_DV_KM_S,
        "saturn_rendezvous_in_dv_km_s": SATURN_RENDEZVOUS_IN_DV_KM_S,
        "conops_total_watermet_dv_km_s": CONOPS_TOTAL_WATERMET_DV_KM_S,
        "conops_tsi_dv_km_s": CONOPS_TSI_DV_KM_S,
        "r6_revised_chunkfed_inbound_dv_km_s": R6_REVISED_CHUNKFED_INBOUND_DV_KM_S,
        "r2_lga_at_vinf_6_km_s": R2_LGA_AT_VINF_6_KM_S,
        "water_met_isp_s": WATER_MET_ISP_S,
        "grappled_chunk_t": GRAPPLED_CHUNK_T,
        "dry_spacecraft_t": DRY_SPACECRAFT_T,
    }}

    # --- H8a, H8b: Hohmann transfer velocity-at-infinity at both endpoints ---
    hohmann = hohmann_endpoint_velocities(A_EARTH, A_SATURN)
    results["heliocentric_hohmann"] = hohmann
    v_inf_earth_hohmann = hohmann["v_inf_at_inner_km_s"]
    v_inf_saturn_hohmann = hohmann["v_inf_at_outer_km_s"]

    # --- Saturn-side egress reconstruction (chunk-fed) ---
    # Conops: post-capture into highly elliptical orbit, then Hohmann drop +
    # phasing to B-ring (1.49 km/s total). On the way out, assume mirror.
    # We rebuild the drop alone (without phasing) for the Hohmann piece.
    # Highly elliptical capture orbit apoapsis: assumed near Saturn's sphere of
    # influence (~6.5e7 km) for the lowest-energy capture; iterate to find
    # apoapsis that produces a 0.6 km/s capture burn given v_inf_saturn = 5.4.
    # For this audit, use the conops-stated 1.49 km/s as the round-trip-out
    # Saturn-system maneuvering cost (Hohmann drop + phasing). Saturn-system
    # exit on the way out: mirror of capture, ~0.6 km/s from elliptical orbit.

    # Standalone consistency: at v_inf_saturn = 5.4 (conops), capture burn into
    # an orbit with apoapsis r_apo from impulsive insertion at periapsis r_peri:
    # we don't iterate; we report the conops phase numbers and compare to
    # patched-conic for sanity.

    # Sanity: B-ring circular orbit velocity at Saturn.
    bring_circ = math.sqrt(GM_SATURN / SATURN_BRING_RADIUS_KM)
    bring_esc = math.sqrt(2.0 * GM_SATURN / SATURN_BRING_RADIUS_KM)
    results["saturn_bring_kinematics"] = {
        "v_circ_km_s": bring_circ,
        "v_esc_km_s": bring_esc,
    }

    # Saturn departure from B-ring directly to v_inf 5.4 (single impulsive burn,
    # unrealistic but bracket).
    saturn_dep_direct = saturn_escape_dv_from_circular_orbit(
        SATURN_BRING_RADIUS_KM, v_inf_saturn_hohmann
    )
    results["saturn_departure_direct_bracket"] = saturn_dep_direct

    # More realistic: spacecraft returns to highly elliptical orbit first
    # (mirror of 1.49 km/s rendezvous-in), then escapes (mirror of 0.6 km/s
    # capture). Total Saturn-side egress: ~2.1 km/s, chunk-fed.
    saturn_egress_mirror_km_s = SATURN_RENDEZVOUS_IN_DV_KM_S + SATURN_CAPTURE_DV_KM_S
    results["saturn_egress_mirror_km_s"] = saturn_egress_mirror_km_s

    # --- Earth-side inbound braking requirement ---
    # Lunar gravity assist absorbs some of the inbound v_inf. At Hohmann
    # arrival v_inf ~10 km/s, the R2 lookup table was only run for v_inf 4-8;
    # the moon's effectiveness drops as v_inf rises, so at 10 km/s it absorbs
    # less than the 2.15 km/s at v_inf 6. Conservative estimate: 1.0-1.5 km/s.
    # The "remainder" must be eliminated by the chunk-fed propulsion OR by
    # arrival at a lower v_inf via slower-than-Hohmann trajectory.

    # Cases studied:
    # (case A) Hohmann return + single-pass LGA + chunk-fed braking
    # (case B) Slower transfer arriving at v_inf = 6 km/s + single-pass LGA at
    #          R2's 2.15 km/s + chunk-fed braking for the residual
    # (case C) Slower transfer arriving at v_inf = 4 km/s + single-pass LGA at
    #          R2's 3.24 km/s + chunk-fed braking for the residual
    # (case D) Hohmann return + 5-flyby LGA tour absorbing 3 km/s (per R2
    #          flag for extended tour) + chunk-fed braking for the residual

    # Approximate LGA capability at v_inf 10 km/s: extrapolate R2 trend.
    # Two-body lunar flyby max single-pass dv at high v_inf scales as
    # 2 * v_moon * v_inf / (v_inf + v_moon). v_moon ~ 1.022 km/s.
    def lga_max_single_pass(v_inf_km_s: float) -> float:
        v_moon = 1.022
        return 2.0 * v_moon * v_inf_km_s / (v_inf_km_s + v_moon)

    cases = []
    for label, v_inf_arrive, lga_dv in [
        ("A_hohmann_lga1", v_inf_earth_hohmann, lga_max_single_pass(v_inf_earth_hohmann)),
        ("B_slow_vinf6_lga1", 6.0, R2_LGA_AT_VINF_6_KM_S),
        ("C_slow_vinf4_lga1", 4.0, R2_LGA_AT_VINF_4_KM_S),
        ("D_hohmann_lga5", v_inf_earth_hohmann, 3.0),  # speculative 5-flyby tour
    ]:
        residual_dv = v_inf_arrive - lga_dv
        chunk_fed_inbound_total_km_s = (
            saturn_egress_mirror_km_s + max(residual_dv, 0.0)
        )
        # Mass closure: chunk + dry initial mass; how much propellant required?
        # m_initial = chunk + dry; after burn m_final = (m_initial) * exp(-dV/ve)
        # propellant = m_initial - m_final. If propellant > chunk, the chunk
        # is fully consumed and the dry spacecraft also has to be reduced.
        v_e_m_s = WATER_MET_ISP_S * G0
        m0_t = GRAPPLED_CHUNK_T + DRY_SPACECRAFT_T
        prop_frac = tsiolkovsky_propellant_fraction(
            chunk_fed_inbound_total_km_s * 1000.0, v_e_m_s
        )
        prop_req_t = m0_t * prop_frac
        delivered_chunk_t = max(GRAPPLED_CHUNK_T - prop_req_t, 0.0)
        delivered_chunk_frac = delivered_chunk_t / GRAPPLED_CHUNK_T

        cases.append({
            "label": label,
            "v_inf_arrive_km_s": v_inf_arrive,
            "lga_dv_km_s": lga_dv,
            "residual_after_lga_km_s": residual_dv,
            "chunk_fed_inbound_total_km_s": chunk_fed_inbound_total_km_s,
            "v_e_m_s": v_e_m_s,
            "m0_t": m0_t,
            "prop_frac": prop_frac,
            "prop_req_t": prop_req_t,
            "delivered_chunk_t": delivered_chunk_t,
            "delivered_chunk_frac": delivered_chunk_frac,
        })

    results["inbound_cases"] = cases

    # --- H8c: conops reconciliation ---
    # Conops itemized: capture 0.6 + rendezvous-in 1.49 = 2.09. Total water-MET
    # allocated 3.7. Implicit chunk-fed remainder: 1.61 km/s.
    conops_explicit_watermet = SATURN_CAPTURE_DV_KM_S + SATURN_RENDEZVOUS_IN_DV_KM_S
    conops_implicit_chunkfed = CONOPS_TOTAL_WATERMET_DV_KM_S - conops_explicit_watermet

    # First-principles chunk-fed minimum (Saturn egress mirror + LGA-case-A
    # residual = pessimistic bracket; LGA-case-C residual = optimistic).
    first_principles_pessimistic = cases[0]["chunk_fed_inbound_total_km_s"]
    first_principles_optimistic = cases[2]["chunk_fed_inbound_total_km_s"]
    conops_hole_pessimistic = first_principles_pessimistic - conops_implicit_chunkfed
    conops_hole_optimistic = first_principles_optimistic - conops_implicit_chunkfed

    results["conops_reconciliation"] = {
        "conops_total_watermet_dv_km_s": CONOPS_TOTAL_WATERMET_DV_KM_S,
        "conops_explicit_watermet_km_s": conops_explicit_watermet,
        "conops_implicit_chunkfed_km_s": conops_implicit_chunkfed,
        "first_principles_chunkfed_pessimistic_km_s": first_principles_pessimistic,
        "first_principles_chunkfed_optimistic_km_s": first_principles_optimistic,
        "conops_hole_pessimistic_km_s": conops_hole_pessimistic,
        "conops_hole_optimistic_km_s": conops_hole_optimistic,
    }

    # --- Hypothesis grading ---
    grading = {}
    grading["H8a"] = {
        "predicted_range_km_s": [9.0, 11.0],
        "measured_km_s": v_inf_earth_hohmann,
        "held": 9.0 <= v_inf_earth_hohmann <= 11.0,
    }
    grading["H8b"] = {
        "predicted_range_km_s": [5.0, 5.8],
        "measured_km_s": v_inf_saturn_hohmann,
        "held": 5.0 <= v_inf_saturn_hohmann <= 5.8,
    }
    grading["H8c"] = {
        "predicted_threshold": "held if conops vs first-principles gap ≤ 0.5 km/s",
        "pessimistic_gap_km_s": conops_hole_pessimistic,
        "optimistic_gap_km_s": conops_hole_optimistic,
        "verdict": (
            "load-bearing" if conops_hole_pessimistic > 2.0
            else "falsified" if conops_hole_pessimistic > 0.5
            else "held"
        ),
    }
    # H8d: inbound braking after LGA at v_inf 6, target v_inf 0 (LEO insertion).
    # The case-B residual after LGA at v_inf 6.
    case_b = cases[1]
    grading["H8d"] = {
        "predicted_range_km_s": [5.5, 7.5],
        "measured_km_s": case_b["chunk_fed_inbound_total_km_s"],
        "held": 5.5 <= case_b["chunk_fed_inbound_total_km_s"] <= 7.5,
    }
    # H8e: mass closure at H8d delta-velocity.
    grading["H8e"] = {
        "predicted": "falsified (chunk arrives < 25% delivered)",
        "measured_delivered_frac": case_b["delivered_chunk_frac"],
        "held": case_b["delivered_chunk_frac"] < 0.25,
    }

    results["hypothesis_grading"] = grading

    # --- Output ---
    out_dir = Path(__file__).parent / "results"
    out_dir.mkdir(exist_ok=True)
    with (out_dir / "budget_audit.json").open("w") as f:
        json.dump(results, f, indent=2)

    # Console summary
    print("=" * 70)
    print("R8 — Inbound Delta-Velocity Budget Audit")
    print("=" * 70)
    print()
    print("Heliocentric Hohmann transfer Earth↔Saturn:")
    print(f"  Semi-major axis of Hohmann ellipse = {hohmann['a_transfer_km']/A_EARTH:.3f} AU")
    print(f"  Velocity-at-infinity at Earth     = {v_inf_earth_hohmann:.3f} km/s (H8a predicted 9.0-11.0)")
    print(f"  Velocity-at-infinity at Saturn    = {v_inf_saturn_hohmann:.3f} km/s (H8b predicted 5.0-5.8, conops 5.4)")
    print()
    print("Saturn-side chunk-fed egress:")
    print(f"  B-ring circular velocity = {bring_circ:.2f} km/s")
    print(f"  Mirror-of-ingress egress = {saturn_egress_mirror_km_s:.2f} km/s")
    print(f"  Direct-burn B-ring → v_inf {v_inf_saturn_hohmann:.1f} = {saturn_dep_direct['delta_v_km_s']:.2f} km/s (impulsive bracket)")
    print()
    print("Earth-side inbound braking cases:")
    print(f"  {'case':<22} {'v_inf':>8} {'LGA':>6} {'residual':>10} {'chunk-fed':>11} {'deliv chunk':>12}")
    for c in cases:
        print(
            f"  {c['label']:<22} {c['v_inf_arrive_km_s']:>6.2f} km/s "
            f"{c['lga_dv_km_s']:>4.2f} km/s "
            f"{c['residual_after_lga_km_s']:>8.2f} km/s "
            f"{c['chunk_fed_inbound_total_km_s']:>9.2f} km/s "
            f"{c['delivered_chunk_frac']*100:>10.1f}%"
        )
    print()
    print("Conops reconciliation:")
    print(f"  Conops total water-MET                  = {CONOPS_TOTAL_WATERMET_DV_KM_S:.2f} km/s")
    print(f"  Conops explicit water-MET (capture+rzvs)= {conops_explicit_watermet:.2f} km/s")
    print(f"  Implicit chunk-fed remainder            = {conops_implicit_chunkfed:.2f} km/s")
    print(f"  First-principles chunk-fed pessimistic  = {first_principles_pessimistic:.2f} km/s")
    print(f"  First-principles chunk-fed optimistic   = {first_principles_optimistic:.2f} km/s")
    print(f"  Conops hole (pessimistic)               = {conops_hole_pessimistic:.2f} km/s")
    print(f"  Conops hole (optimistic)                = {conops_hole_optimistic:.2f} km/s")
    print()
    print("Hypothesis grading:")
    for h, g in grading.items():
        held_label = "HELD" if g.get("held") else g.get("verdict", "FALSIFIED")
        print(f"  {h}: {held_label}")
    print()
    print(f"Result JSON written to {out_dir / 'budget_audit.json'}")

    return results


if __name__ == "__main__":
    main()
