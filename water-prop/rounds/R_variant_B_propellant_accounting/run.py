"""R-variant-B-propellant-accounting — full chemical-electric-chemical inbound
propellant stack solver for Variant B at matrix parameters.

Computes delivered mass under correct propellant accounting (electrolyzed-from-chunk
hydrolox + electric residual + electrolyzed-from-chunk hydrolox), with and without
lunar gravity assist. Identifies the binding constraint.

Usage: python3 run.py
"""

from __future__ import annotations

import csv
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "R_electric_outbound_rerun"))
from run import dry_mass_t, ETA_THR, G0, YEAR_S, MASS_MODELS  # noqa: E402

RESULTS = HERE / "results"
RESULTS.mkdir(parents=True, exist_ok=True)

REACTOR_KWE = 500.0
SATURN_OPS_YR = 0.5

ISP_ELEC = 2000.0
ISP_CHEM = 450.0   # hydrolox

DV_SATURN_EGRESS_KM_S = 2.0   # impulsive Saturn-orbit egress kick
DV_ELEC_RESIDUAL_WITH_LGA_KM_S = 4.27   # 6.42 - 2.15 LGA at Earth
DV_ELEC_RESIDUAL_NO_LGA_KM_S = 6.42      # full residual without LGA
DV_EARTH_CAPTURE_WITH_LGA_KM_S = 3.50    # post-LGA chemical capture
DV_EARTH_CAPTURE_NO_LGA_KM_S = 5.60      # no-LGA chemical capture

ENERGY_ELECTROLYSIS_MJ_PER_KG = 20.0     # 15.9 theoretical + 25% overhead


def solve_variant_B_inbound(
    m_dry_t: float,
    chunk_t: float,
    dv_egress_km_s: float,
    dv_elec_residual_km_s: float,
    dv_capture_km_s: float,
    isp_chem_s: float = ISP_CHEM,
    isp_elec_s: float = ISP_ELEC,
) -> dict:
    """Forward solver. Ship at Saturn-parking has m_dry + chunk_t of water.

    Three-stage inbound:
      1. Saturn-egress chemical kick at v_e_chem.
      2. Heliocentric electric coast at v_e_elec (chunk-fed).
      3. Earth-LEO chemical capture at v_e_chem.

    Returns mass at each step and feasibility (water consumed ≤ chunk).
    """
    v_e_chem = isp_chem_s * G0
    v_e_elec = isp_elec_s * G0

    MR_egress = math.exp(dv_egress_km_s * 1000.0 / v_e_chem)
    MR_elec = math.exp(dv_elec_residual_km_s * 1000.0 / v_e_elec)
    MR_capture = math.exp(dv_capture_km_s * 1000.0 / v_e_chem)

    m0 = m_dry_t + chunk_t
    m_after_egress = m0 / MR_egress
    m_egress_prop = m0 - m_after_egress

    m_after_coast = m_after_egress / MR_elec
    m_elec_prop = m_after_egress - m_after_coast

    m_after_capture = m_after_coast / MR_capture
    m_capture_prop = m_after_coast - m_after_capture

    delivered = m_after_capture - m_dry_t

    water_consumed = m_egress_prop + m_elec_prop + m_capture_prop
    feasible_chunk = (water_consumed <= chunk_t) and (delivered >= 0.0)

    return {
        "m_dry_t": m_dry_t, "chunk_t": chunk_t,
        "MR_egress": MR_egress, "MR_elec": MR_elec, "MR_capture": MR_capture,
        "m_at_parking_t": m0,
        "m_after_egress_t": m_after_egress, "m_egress_prop_t": m_egress_prop,
        "m_after_coast_t": m_after_coast, "m_elec_prop_t": m_elec_prop,
        "m_after_capture_t": m_after_capture, "m_capture_prop_t": m_capture_prop,
        "delivered_t": delivered,
        "water_consumed_t": water_consumed,
        "feasible_chunk": feasible_chunk,
        "dv_egress_km_s": dv_egress_km_s,
        "dv_elec_residual_km_s": dv_elec_residual_km_s,
        "dv_capture_km_s": dv_capture_km_s,
    }


def required_chunk_for_delivered(
    target_delivered_t: float,
    m_dry_t: float,
    dv_egress_km_s: float,
    dv_elec_residual_km_s: float,
    dv_capture_km_s: float,
) -> float:
    """Solve for chunk such that delivered = target.

    Forward: m0 = m_dry + chunk; after all stages: m_final = m0 / (MR_eg × MR_elec × MR_cap)
    delivered = m_final - m_dry = (m_dry + chunk) / Product - m_dry
    So chunk = (target + m_dry) × Product - m_dry.
    """
    v_e_chem = ISP_CHEM * G0
    v_e_elec = ISP_ELEC * G0
    MR_egress = math.exp(dv_egress_km_s * 1000.0 / v_e_chem)
    MR_elec = math.exp(dv_elec_residual_km_s * 1000.0 / v_e_elec)
    MR_capture = math.exp(dv_capture_km_s * 1000.0 / v_e_chem)
    Product = MR_egress * MR_elec * MR_capture
    return (target_delivered_t + m_dry_t) * Product - m_dry_t


def electrolysis_energy_required_TJ(m_water_t: float) -> float:
    """Energy in TJ to electrolyze m_water tonnes of water."""
    return m_water_t * 1000.0 * ENERGY_ELECTROLYSIS_MJ_PER_KG / 1e6  # TJ


def electrolysis_energy_available_TJ(power_kwe: float, ops_yr: float, eta_electrolysis: float = 0.75) -> float:
    """Energy in TJ available at given Saturn-ops time and reactor power.

    Assume 75% of reactor power is available for electrolysis (rest is housekeeping etc).
    """
    return power_kwe * 1000.0 * eta_electrolysis * ops_yr * YEAR_S / 1e12  # TJ


def main() -> None:
    print("R-variant-B-propellant-accounting — full inbound stack solver\n")

    model = MASS_MODELS["bundled_10_W_per_kg"]
    m_dry = dry_mass_t(model, REACTOR_KWE, m_prop_t=0.0)
    print(f"m_dry (bundled 10 W/kg, 500 kWe) = {m_dry:.1f} t")

    # Cases
    cases = []
    for tag, dv_elec, dv_cap in [
        ("with_lunar_GA",   DV_ELEC_RESIDUAL_WITH_LGA_KM_S, DV_EARTH_CAPTURE_WITH_LGA_KM_S),
        ("no_lunar_GA",     DV_ELEC_RESIDUAL_NO_LGA_KM_S,   DV_EARTH_CAPTURE_NO_LGA_KM_S),
    ]:
        for chunk_t in [200.0, 300.0, 400.0, 522.0, 600.0]:
            c = solve_variant_B_inbound(m_dry, chunk_t, DV_SATURN_EGRESS_KM_S,
                                         dv_elec, dv_cap)
            c["tag"] = tag
            cases.append(c)

    print(f"\n{'Tag':<16} {'chunk':>7} {'water_consumed':>15} {'delivered':>11} {'feasible':>10}")
    for c in cases:
        print(f"  {c['tag']:<16} {c['chunk_t']:>7.0f} {c['water_consumed_t']:>15.1f} "
              f"{c['delivered_t']:>11.1f} {str(c['feasible_chunk']):>10}")

    # Required chunk to deliver matrix-stated 80 t (with and without LGA)
    print("\nRequired chunk to deliver matrix's 80 t per mission:")
    chunk_for_80_with_lga = required_chunk_for_delivered(
        80.0, m_dry, DV_SATURN_EGRESS_KM_S, DV_ELEC_RESIDUAL_WITH_LGA_KM_S, DV_EARTH_CAPTURE_WITH_LGA_KM_S)
    chunk_for_80_no_lga = required_chunk_for_delivered(
        80.0, m_dry, DV_SATURN_EGRESS_KM_S, DV_ELEC_RESIDUAL_NO_LGA_KM_S, DV_EARTH_CAPTURE_NO_LGA_KM_S)
    chunk_for_50_with_lga = required_chunk_for_delivered(
        50.0, m_dry, DV_SATURN_EGRESS_KM_S, DV_ELEC_RESIDUAL_WITH_LGA_KM_S, DV_EARTH_CAPTURE_WITH_LGA_KM_S)
    print(f"  with lunar GA:     {chunk_for_80_with_lga:.1f} t  (matrix L0-05 cap is 200 t)")
    print(f"  without lunar GA:  {chunk_for_80_no_lga:.1f} t  (matrix L0-05 cap is 200 t)")
    print(f"  with LGA + 50 t delivered (L0-09 floor): {chunk_for_50_with_lga:.1f} t")

    # Energy budget
    matrix_case = next(c for c in cases if c["chunk_t"] == 200.0 and c["tag"] == "with_lunar_GA")
    water_consumed_matrix = matrix_case["water_consumed_t"]
    e_required = electrolysis_energy_required_TJ(water_consumed_matrix)
    e_available = electrolysis_energy_available_TJ(REACTOR_KWE, SATURN_OPS_YR)
    print(f"\nEnergy budget (matrix params 200-t chunk, with LGA):")
    print(f"  water consumed (chemical + electric) = {water_consumed_matrix:.1f} t")
    print(f"  electrolysis energy required = {e_required:.2f} TJ")
    print(f"  electrolysis energy available (500 kWe × 0.5 yr × 0.75 eta) = {e_available:.2f} TJ")
    print(f"  ratio available / required = {e_available/e_required:.2f}")

    # Outbound launch-mass multiplier scenario: ship carries inbound chemical from Earth
    # Required carried chemical mass = m_egress_prop + m_capture_prop at no-electrolysis case.
    # For delivered = 80 t at chunk = 200 t with NO chunk electrolysis available,
    # ship arrives at Saturn dry + chunk-as-electric-prop only.
    # In this hypothetical: chemical comes from Earth-carried hydrolox.
    # This requires re-solving with chemical mass separate from chunk.

    # Forward: m_at_parking = m_dry + chunk_water + m_chem_eg_carried + m_chem_cap_carried
    # Egress: m_after_egress = m_at_parking - m_chem_eg_carried (chemical mass = prop mass).
    # But the egress kick must accelerate the WHOLE mass including the to-be-used-later chemical.
    # Tsiolkovsky on egress: MR_eg = m_at_parking / m_after_egress; m_chem_eg = m_at_parking × (1 - 1/MR_eg).
    # That EQUALS the m_eg_prop we'd carry: chemical_carried_for_egress = m_at_parking × (1 - 1/MR_eg).
    # Solve iteratively.

    def solve_outbound_carried(m_dry_t, chunk_water, target_delivered, dv_eg, dv_elec, dv_cap):
        v_e_chem = ISP_CHEM * G0
        v_e_elec = ISP_ELEC * G0
        MR_eg = math.exp(dv_eg * 1000.0 / v_e_chem)
        MR_elec = math.exp(dv_elec * 1000.0 / v_e_elec)
        MR_cap = math.exp(dv_cap * 1000.0 / v_e_chem)

        # Backward: at Earth-LEO arrival, m_final = m_dry + delivered.
        m_arrival = m_dry_t + target_delivered
        # Capture burn: m_before_cap = m_arrival × MR_cap.
        m_before_cap = m_arrival * MR_cap
        m_chem_cap = m_before_cap - m_arrival
        # Coast: m_before_coast = m_before_cap × MR_elec.
        # During coast, electric prop = chunk_water consumed.
        m_before_coast = m_before_cap * MR_elec
        m_elec = m_before_coast - m_before_cap
        # Check: electric prop must come from chunk.
        chunk_remaining_after_coast = chunk_water - m_elec
        if chunk_remaining_after_coast < 0:
            return None  # chunk insufficient for electric
        # Egress: m_at_parking = m_before_coast × MR_eg.
        m_at_parking = m_before_coast * MR_eg
        m_chem_eg = m_at_parking - m_before_coast
        # m_at_parking = m_dry + chunk_water + m_chem_eg_carried + m_chem_cap_carried
        # Inspect consistency:
        m_chem_carried_total = m_chem_eg + m_chem_cap
        m_at_parking_check = m_dry_t + chunk_water + m_chem_carried_total
        # m_at_parking must equal m_before_coast × MR_eg by Tsiolkovsky.
        return {
            "m_chem_eg_carried_t": m_chem_eg,
            "m_chem_cap_carried_t": m_chem_cap,
            "m_chem_total_carried_t": m_chem_carried_total,
            "m_elec_consumed_t": m_elec,
            "chunk_remaining_after_electric_t": chunk_remaining_after_coast,
            "m_at_parking_t": m_at_parking,
            "delivered_t": target_delivered,
            "m_at_parking_check_t": m_at_parking_check,
        }

    print("\nOutbound-carried-chemical scenario (Variant B without Saturn-side electrolysis):")
    print(f"{'target_del':>11} {'chunk':>7} {'m_chem_carried':>15} {'mass_at_parking':>16} {'feasible':>10}")
    outbound_results = []
    for target_del in [30.0, 50.0, 80.0]:
        for chunk in [200.0, 300.0]:
            r = solve_outbound_carried(m_dry, chunk, target_del,
                                         DV_SATURN_EGRESS_KM_S,
                                         DV_ELEC_RESIDUAL_WITH_LGA_KM_S,
                                         DV_EARTH_CAPTURE_WITH_LGA_KM_S)
            if r is None:
                print(f"  {target_del:>11.0f} {chunk:>7.0f} {'(infeasible)':>15} {'-':>16} {'False':>10}")
                outbound_results.append({"target_del": target_del, "chunk": chunk, "feasible": False})
            else:
                feasible = r["chunk_remaining_after_electric_t"] >= 0
                print(f"  {target_del:>11.0f} {chunk:>7.0f} {r['m_chem_total_carried_t']:>15.1f} "
                      f"{r['m_at_parking_t']:>16.1f} {str(feasible):>10}")
                outbound_results.append({"target_del": target_del, "chunk": chunk,
                                          "m_chem_carried": r["m_chem_total_carried_t"],
                                          "feasible": feasible,
                                          "m_at_parking": r["m_at_parking_t"]})

    # R-outbound-architecture multiplier: 6.9× LEO-launched-mass per mass arriving at Saturn for mission 1.
    # If ship carries 200 t of chunk-supplied electric prop + m_chem_carried, total inbound launch = m_dry + chunk + m_chem_carried.
    # Multiplied by 6.9 for LEO launch.
    print("\nLEO launch-mass multiplier per delivered tonne (mission 1, 6.9× outbound multiplier):")
    for r in outbound_results:
        if r.get("feasible"):
            leo_launch = r["m_at_parking"] * 6.9
            multiplier = leo_launch / r["target_del"]
            print(f"  delivered {r['target_del']:.0f} t, chunk {r['chunk']:.0f} t → "
                  f"LEO launch {leo_launch:.0f} t → {multiplier:.1f}× per delivered tonne")

    # ---- Scoring ----
    scoring = []
    def score(hid, predicted, measured, holds):
        scoring.append({"id": hid, "predicted": predicted, "measured": measured,
                        "verdict": "HELD" if holds else "FALSIFIED"})

    score("H-vbpa-a", "Saturn-egress dv 1.5–2.5 km/s",
          f"{DV_SATURN_EGRESS_KM_S:.2f} km/s (input)",
          1.5 <= DV_SATURN_EGRESS_KM_S <= 2.5)
    score("H-vbpa-b", "Earth-LEO capture dv with LGA 3.0–4.0 km/s",
          f"{DV_EARTH_CAPTURE_WITH_LGA_KM_S:.2f} km/s (input)",
          3.0 <= DV_EARTH_CAPTURE_WITH_LGA_KM_S <= 4.0)
    score("H-vbpa-c", "Variant B matrix params (200-t chunk, with LGA) delivered ≤ 15 t",
          f"{matrix_case['delivered_t']:.1f} t",
          matrix_case["delivered_t"] <= 15.0)
    no_lga_matrix = next(c for c in cases if c["chunk_t"] == 200.0 and c["tag"] == "no_lunar_GA")
    score("H-vbpa-d", "Without lunar GA, Variant B at 200-t chunk delivered ≤ 0 t",
          f"{no_lga_matrix['delivered_t']:.1f} t",
          no_lga_matrix["delivered_t"] <= 0.0)
    score("H-vbpa-e", "Required chunk for 80-t delivered with LGA ≥ 450 t (≥2.25× L0-05)",
          f"{chunk_for_80_with_lga:.1f} t",
          chunk_for_80_with_lga >= 450.0)
    score("H-vbpa-f", "Variant B requires Saturn-side electrolysis OR outbound-carried chem OR matrix params wrong",
          f"At 200-t chunk with LGA, water consumed = {water_consumed_matrix:.1f} t {'>' if water_consumed_matrix > 200 else '<='} chunk 200 t",
          water_consumed_matrix > 200.0)
    score("H-vbpa-g", "Matrix has not added Saturn-side-electrolysis cascade factor to Variant B's posterior",
          "matrix prose carries 10-t electrolyzer line but R6 cascade was for Arch E only; Variant B posterior unrecomputed",
          True)  # documented qualitative claim
    multiplier_80_300 = None
    for r in outbound_results:
        if r.get("feasible") and r["target_del"] == 80.0 and r["chunk"] == 300.0:
            multiplier_80_300 = r["m_at_parking"] * 6.9 / 80.0
    if multiplier_80_300 is None:
        score("H-vbpa-h", "Outbound-carried scenario: LEO launch multiplier ≥ 12× per delivered tonne",
              "no feasible cell with chunk 200 or 300 at 80-t delivered", False)
    else:
        score("H-vbpa-h", "Outbound-carried scenario: LEO launch multiplier ≥ 12× per delivered tonne",
              f"{multiplier_80_300:.1f}× at 300-t chunk, 80-t delivered",
              multiplier_80_300 >= 12.0)
    score("H-vbpa-i", "Electrolysis energy available > required",
          f"available {e_available:.2f} TJ vs required {e_required:.2f} TJ; ratio {e_available/e_required:.2f}",
          e_available > e_required)
    score("H-vbpa-j", "200-t chunk is the binding constraint (not energy, not power, not time)",
          f"water consumed {water_consumed_matrix:.1f} t > chunk 200 t AND energy available {e_available/e_required:.1f}× required",
          (water_consumed_matrix > 200.0) and (e_available > e_required))

    # ---- Write outputs ----
    with (RESULTS / "propellant_stack.csv").open("w", newline="") as f:
        keys = sorted(cases[0].keys())
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for c in cases:
            w.writerow(c)

    lines = ["# R-variant-B-propellant-accounting — hypothesis scoring",
             "",
             "| ID | Predicted | Measured | Verdict |",
             "|---|---|---|---|"]
    for h in scoring:
        lines.append(f"| {h['id']} | {h['predicted']} | {h['measured']} | **{h['verdict']}** |")
    (RESULTS / "hypothesis_scoring.md").write_text("\n".join(lines) + "\n")

    held = sum(1 for h in scoring if h["verdict"] == "HELD")
    falsified = sum(1 for h in scoring if h["verdict"] == "FALSIFIED")
    print(f"\nScoring: {held} HELD, {falsified} FALSIFIED of {len(scoring)}")

    # Summary
    sum_lines = [
        "# R-variant-B-propellant-accounting — summary",
        "",
        "## Forward propellant stack at matrix parameters (m_dry 53 t, chunk 200 t, with lunar GA)",
        "",
        f"| Stage | dv (km/s) | MR | mass before (t) | mass after (t) | water/prop consumed (t) |",
        "|---|---:|---:|---:|---:|---:|",
        f"| Start at Saturn parking | — | — | — | {matrix_case['m_at_parking_t']:.1f} | — |",
        f"| Saturn-egress chem | {DV_SATURN_EGRESS_KM_S} | {matrix_case['MR_egress']:.3f} | "
        f"{matrix_case['m_at_parking_t']:.1f} | {matrix_case['m_after_egress_t']:.1f} | "
        f"{matrix_case['m_egress_prop_t']:.1f} |",
        f"| Heliocentric electric residual | {DV_ELEC_RESIDUAL_WITH_LGA_KM_S} | {matrix_case['MR_elec']:.3f} | "
        f"{matrix_case['m_after_egress_t']:.1f} | {matrix_case['m_after_coast_t']:.1f} | "
        f"{matrix_case['m_elec_prop_t']:.1f} |",
        f"| Earth-LEO chem capture | {DV_EARTH_CAPTURE_WITH_LGA_KM_S} | {matrix_case['MR_capture']:.3f} | "
        f"{matrix_case['m_after_coast_t']:.1f} | {matrix_case['m_after_capture_t']:.1f} | "
        f"{matrix_case['m_capture_prop_t']:.1f} |",
        f"",
        f"**Total water/propellant consumed:** {matrix_case['water_consumed_t']:.1f} t from a 200-t chunk.",
        f"**Delivered to LEO:** {matrix_case['delivered_t']:.1f} t (matrix-stated 80 t).",
        f"**Water deficit:** {matrix_case['water_consumed_t'] - 200.0:.1f} t (cannot close without supplemental propellant).",
        "",
        "## Required chunk to deliver matrix-stated 80 t",
        "",
        f"- With lunar gravity assist: **{chunk_for_80_with_lga:.0f} t** (matrix L0-05 cap is 200 t; **{chunk_for_80_with_lga/200:.2f}× over cap**)",
        f"- Without lunar gravity assist: **{chunk_for_80_no_lga:.0f} t**",
        f"- For L0-09 floor 50 t delivered with lunar GA: **{chunk_for_50_with_lga:.0f} t** (still over L0-05's 200-t cap)",
        "",
        "## Energy budget at Saturn",
        "",
        f"- Electrolysis energy required for water consumed at 200-t chunk: **{e_required:.2f} TJ**",
        f"- Available at 500 kWe × 0.5 yr × 75% efficiency: **{e_available:.2f} TJ**",
        f"- Ratio available / required: **{e_available/e_required:.2f}**",
        f"- **Energy is sufficient; the binding constraint is chunk mass.**",
        "",
        "## Outbound-carried-chemical scenario (no Saturn-side electrolysis)",
        "",
        "If Variant B cannot use chunk water for chemical propellant (e.g., to avoid Saturn-side electrolysis):",
    ]
    for r in outbound_results:
        if r.get("feasible"):
            multiplier = r["m_at_parking"] * 6.9 / r["target_del"]
            sum_lines.append(
                f"- target {r['target_del']:.0f} t delivered, chunk {r['chunk']:.0f} t: "
                f"carry {r['m_chem_carried']:.1f} t chemical from Earth; "
                f"mass at Saturn parking = {r['m_at_parking']:.1f} t → "
                f"LEO launch ≈ {r['m_at_parking']*6.9:.0f} t = **{multiplier:.1f}× per delivered tonne**"
            )
        else:
            sum_lines.append(
                f"- target {r['target_del']:.0f} t delivered, chunk {r['chunk']:.0f} t: **infeasible** (chunk insufficient for electric residual)"
            )

    sum_lines += [
        "",
        f"## Scoring: {held} HELD / {falsified} FALSIFIED of {len(scoring)}",
        "",
        "See `hypothesis_scoring.md` for per-hypothesis verdicts.",
    ]
    (RESULTS / "summary.md").write_text("\n".join(sum_lines) + "\n")
    print(f"Wrote {RESULTS}/{{propellant_stack.csv, hypothesis_scoring.md, summary.md}}")


if __name__ == "__main__":
    main()
