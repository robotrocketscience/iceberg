"""R-variant-B-burn-consistency — first-principles audit of the matrix's "sole
defensible cell" (Variant B at 500 kWe / ISP 2000 s / chunk 200 t / 14.5-yr
round-trip / 80 t delivered / 7.5-yr inbound burn) against burn-time +
propellant arithmetic, and extension of R12's reactor-lifetime axis from Arch E
to Variant B.

Usage: python3 run.py
"""

from __future__ import annotations

import csv
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "R_electric_outbound_rerun"))
from run import dry_mass_t, ETA_THR, G0, YEAR_S, hohmann_cruise_yr, MASS_MODELS  # noqa: E402

RESULTS = HERE / "results"
RESULTS.mkdir(parents=True, exist_ok=True)

ISP_VARIANT_B = 2000.0
ISP_ARCH_E = 2934.0
CHUNK_T = 200.0
REACTOR_KWE = 500.0
SATURN_OPS_YR = 0.5

DV_INBOUND_IMPULSIVE = 6.42  # matrix
DV_INBOUND_CT_LOW = 24.7     # titan low
DV_INBOUND_CT_MID = 32.0     # midpoint
DV_INBOUND_CT_HIGH = 40.2    # titan high
DV_OUTBOUND_ARCH_E = 29.56   # rhea high-elliptical

KILOPOWER_TARGET_YR = 10.0
FSP_TARGET_YR = 15.0


def thrust_N(reactor_kwe: float, isp_s: float, eta: float = ETA_THR) -> float:
    v_e = isp_s * G0
    return 2.0 * eta * reactor_kwe * 1000.0 / v_e


def burn_chunk_fed_inbound(reactor_kwe: float, isp_s: float, dv_km_s: float,
                            chunk_t: float, m_dry_t: float) -> dict:
    """Chunk-fed electric inbound: m_initial = m_dry + chunk; chunk is propellant.

    Returns burn time, m_prop, delivered = chunk - m_prop, feasibility flag.
    """
    v_e = isp_s * G0
    T = thrust_N(reactor_kwe, isp_s)
    mdot = T / v_e
    m_init_t = m_dry_t + chunk_t
    mr = math.exp(dv_km_s * 1000.0 / v_e)
    m_prop_t = m_init_t * (1.0 - 1.0 / mr)
    t_burn_s = m_prop_t * 1000.0 / mdot
    t_burn_yr = t_burn_s / YEAR_S
    delivered_t = chunk_t - m_prop_t
    feasible = (m_prop_t <= chunk_t) and (delivered_t >= 0.0)
    return {
        "v_e_m_s": v_e, "thrust_N": T, "mdot_kg_s": mdot,
        "m_init_t": m_init_t, "mass_ratio": mr,
        "m_prop_t": m_prop_t, "t_burn_s": t_burn_s, "t_burn_yr": t_burn_yr,
        "delivered_t": delivered_t, "feasible": feasible,
    }


def burn_electric_outbound_from_dry_end(reactor_kwe: float, isp_s: float,
                                         dv_km_s: float, m_dry_end_t: float) -> dict:
    v_e = isp_s * G0
    T = thrust_N(reactor_kwe, isp_s)
    mdot = T / v_e
    mr = math.exp(dv_km_s * 1000.0 / v_e)
    m_prop_t = m_dry_end_t * (mr - 1.0)
    t_burn_s = m_prop_t * 1000.0 / mdot
    return {"m_prop_t": m_prop_t, "t_burn_yr": t_burn_s / YEAR_S, "mass_ratio": mr}


def variant_B_cell(dv_inbound_km_s: float) -> dict:
    """Variant B at matrix parameters: chemical-kick outbound (zero reactor burn
    for propulsion), electric chunk-fed inbound at given dv."""
    model = MASS_MODELS["bundled_10_W_per_kg"]
    m_dry = dry_mass_t(model, REACTOR_KWE, m_prop_t=0.0)
    inbound = burn_chunk_fed_inbound(REACTOR_KWE, ISP_VARIANT_B, dv_inbound_km_s,
                                     CHUNK_T, m_dry)
    t_cruise = hohmann_cruise_yr()
    round_trip_yr = (
        0.0                          # chemical outbound burn ~ minutes
        + t_cruise                   # outbound cruise
        + SATURN_OPS_YR              # ops
        + inbound["t_burn_yr"]       # inbound burn
        + t_cruise                   # inbound cruise (free-flight after burn-stop OR concurrent; treat as additive ceiling)
    )
    return {
        "dv_inbound_km_s": dv_inbound_km_s, "m_dry_t": m_dry, "inbound": inbound,
        "t_cruise_each_yr": t_cruise, "round_trip_yr": round_trip_yr,
        "cumulative_reactor_burn_yr": inbound["t_burn_yr"],  # chemical out = 0
    }


def arch_E_cell(dv_outbound_km_s: float, dv_inbound_km_s: float) -> dict:
    """Architecture E all-electric: electric outbound + electric inbound at 500 kWe / ISP 2934 s."""
    model = MASS_MODELS["bundled_10_W_per_kg"]
    m_dry = dry_mass_t(model, REACTOR_KWE, m_prop_t=0.0)
    out = burn_electric_outbound_from_dry_end(REACTOR_KWE, ISP_ARCH_E, dv_outbound_km_s, m_dry)
    inbound = burn_chunk_fed_inbound(REACTOR_KWE, ISP_ARCH_E, dv_inbound_km_s, CHUNK_T, m_dry)
    t_cruise = hohmann_cruise_yr()
    round_trip_yr = (
        out["t_burn_yr"] + t_cruise + SATURN_OPS_YR + inbound["t_burn_yr"] + t_cruise
    )
    return {
        "m_dry_t": m_dry, "outbound": out, "inbound": inbound,
        "t_cruise_each_yr": t_cruise, "round_trip_yr": round_trip_yr,
        "cumulative_reactor_burn_yr": out["t_burn_yr"] + inbound["t_burn_yr"],
    }


def required_chunk_for_delivered(target_delivered_t: float, dv_km_s: float,
                                  m_dry_t: float, isp_s: float) -> float:
    """Solve for chunk_t such that chunk_t - m_prop = target_delivered.
    m_prop = (m_dry + chunk) × (1 - 1/MR)
    delivered = chunk - m_prop = chunk × (1/MR) - m_dry × (1 - 1/MR)
    target = chunk/MR - m_dry × (1 - 1/MR)
    chunk = MR × (target + m_dry × (1 - 1/MR))
    """
    v_e = isp_s * G0
    mr = math.exp(dv_km_s * 1000.0 / v_e)
    chunk = mr * (target_delivered_t + m_dry_t * (1.0 - 1.0 / mr))
    return chunk


def main() -> None:
    print("R-variant-B-burn-consistency — running")

    # ---- Variant B at four dv regimes ----
    print("\nVariant B (500 kWe, ISP 2000 s, chunk 200 t, MARVL-bundled m_dry):")
    vb_cells = {}
    for dv in [DV_INBOUND_IMPULSIVE, DV_INBOUND_CT_LOW, DV_INBOUND_CT_MID, DV_INBOUND_CT_HIGH]:
        c = variant_B_cell(dv)
        vb_cells[dv] = c
        ib = c["inbound"]
        print(f"  dv_in={dv:>5.2f} km/s | thrust={ib['thrust_N']:.2f} N | "
              f"m_prop={ib['m_prop_t']:6.1f} t | delivered={ib['delivered_t']:7.1f} t | "
              f"burn={ib['t_burn_yr']:5.2f} yr | RT={c['round_trip_yr']:5.2f} yr | "
              f"feasible={ib['feasible']}")

    # ---- Arch E cross-check ----
    print("\nArch E (500 kWe, ISP 2934 s, dv_out 29.56 km/s, dv_in {24.7, 32, 40.2}):")
    ae_cells = {}
    for dv_in in [DV_INBOUND_CT_LOW, DV_INBOUND_CT_MID, DV_INBOUND_CT_HIGH]:
        c = arch_E_cell(DV_OUTBOUND_ARCH_E, dv_in)
        ae_cells[dv_in] = c
        out, inb = c["outbound"], c["inbound"]
        print(f"  dv_in={dv_in:>5.2f} km/s | out_burn={out['t_burn_yr']:5.2f} yr | "
              f"in_burn={inb['t_burn_yr']:5.2f} yr | "
              f"cumulative_burn={c['cumulative_reactor_burn_yr']:5.2f} yr | "
              f"delivered={inb['delivered_t']:6.1f} t | RT={c['round_trip_yr']:5.2f} yr")

    # ---- Reactor-lifetime axis comparison ----
    print("\nReactor-lifetime axis:")
    vb_imp_cum = vb_cells[DV_INBOUND_IMPULSIVE]["cumulative_reactor_burn_yr"]
    ae_ct_low_cum = ae_cells[DV_INBOUND_CT_LOW]["cumulative_reactor_burn_yr"]
    print(f"  Variant B (impulsive inbound 6.42 km/s) cumulative burn: {vb_imp_cum:.2f} yr "
          f"= {vb_imp_cum/KILOPOWER_TARGET_YR*100:.1f}% of 10-yr Kilopower target")
    print(f"  Arch E_500   (CT_low 24.7 km/s inbound)   cumulative burn: {ae_ct_low_cum:.2f} yr "
          f"= {ae_ct_low_cum/KILOPOWER_TARGET_YR*100:.1f}% of 10-yr Kilopower target")
    ratio_vb_ae = vb_imp_cum / ae_ct_low_cum
    print(f"  Ratio VB / E = {ratio_vb_ae:.3f}")

    # ---- Required-chunk sensitivity (Variant B at continuous-thrust 24.7) ----
    model = MASS_MODELS["bundled_10_W_per_kg"]
    m_dry = dry_mass_t(model, REACTOR_KWE, m_prop_t=0.0)
    required_chunk_30t = required_chunk_for_delivered(30.0, DV_INBOUND_CT_LOW, m_dry, ISP_VARIANT_B)
    required_chunk_50t = required_chunk_for_delivered(50.0, DV_INBOUND_CT_LOW, m_dry, ISP_VARIANT_B)
    print(f"\nRequired chunk for Variant B at CT_low 24.7 km/s to deliver:")
    print(f"  30 t to LEO → chunk = {required_chunk_30t:.1f} t  (L0-05 cap is 200 t)")
    print(f"  50 t to LEO → chunk = {required_chunk_50t:.1f} t  (L0-05 cap is 200 t)")

    # ---- Hypothesis scoring ----
    scoring = []
    def score(hid, predicted, measured, holds):
        scoring.append({"id": hid, "predicted": predicted, "measured": measured,
                        "verdict": "HELD" if holds else "FALSIFIED"})

    vb_imp = vb_cells[DV_INBOUND_IMPULSIVE]["inbound"]
    vb_ct_low = vb_cells[DV_INBOUND_CT_LOW]["inbound"]
    vb_ct_high = vb_cells[DV_INBOUND_CT_HIGH]["inbound"]
    vb_rt_imp = vb_cells[DV_INBOUND_IMPULSIVE]["round_trip_yr"]

    # H-vbrc-a: VB impulsive inbound burn 1.0–1.5 yr
    score("H-vbrc-a", "Variant B inbound burn at impulsive 6.42 km/s: 1.0–1.5 yr",
          f"{vb_imp['t_burn_yr']:.2f} yr",
          1.0 <= vb_imp["t_burn_yr"] <= 1.5)
    # H-vbrc-b: VB impulsive delivered 120–135 t
    score("H-vbrc-b", "Variant B delivered at impulsive 6.42 km/s: 120–135 t",
          f"{vb_imp['delivered_t']:.1f} t",
          120.0 <= vb_imp["delivered_t"] <= 135.0)
    # H-vbrc-c: VB CT 24.7 propellant ≥ 180 t (exceeds chunk near-misses)
    score("H-vbrc-c", "Variant B m_prop at CT 24.7 km/s ≥ 180 t",
          f"{vb_ct_low['m_prop_t']:.1f} t",
          vb_ct_low["m_prop_t"] >= 180.0)
    # H-vbrc-d: VB CT 40.2 delivered < 0
    score("H-vbrc-d", "Variant B delivered at CT 40.2 km/s < 0 t",
          f"{vb_ct_high['delivered_t']:.1f} t",
          vb_ct_high["delivered_t"] < 0.0)
    # H-vbrc-e: matrix-stated 7.5-yr inbound burn doesn't reproduce within ±20% in ANY regime
    matrix_burn = 7.5
    burns = [vb_cells[dv]["inbound"]["t_burn_yr"] for dv in
             [DV_INBOUND_IMPULSIVE, DV_INBOUND_CT_LOW, DV_INBOUND_CT_MID, DV_INBOUND_CT_HIGH]]
    reproduces_e = any(abs(b - matrix_burn) / matrix_burn <= 0.20 for b in burns)
    score("H-vbrc-e", "Matrix's 7.5-yr inbound burn does NOT reproduce (within ±20%) in any regime",
          f"burns at dv {{6.42, 24.7, 32, 40.2}} = {[f'{b:.2f}' for b in burns]}",
          not reproduces_e)
    # H-vbrc-f: matrix-stated 80-t delivered doesn't reproduce within ±15% in any regime
    matrix_del = 80.0
    delivereds = [vb_cells[dv]["inbound"]["delivered_t"] for dv in
                  [DV_INBOUND_IMPULSIVE, DV_INBOUND_CT_LOW, DV_INBOUND_CT_MID, DV_INBOUND_CT_HIGH]]
    reproduces_f = any(abs(d - matrix_del) / matrix_del <= 0.15 for d in delivereds)
    score("H-vbrc-f", "Matrix's 80-t delivered does NOT reproduce (within ±15%) in any regime",
          f"delivered at dv {{6.42, 24.7, 32, 40.2}} = {[f'{d:.1f}' for d in delivereds]}",
          not reproduces_f)
    # H-vbrc-g: VB RT at impulsive in [13.5, 15.0]
    score("H-vbrc-g", "Variant B round-trip at impulsive 6.42 km/s: 13.5–15.0 yr",
          f"{vb_rt_imp:.2f} yr", 13.5 <= vb_rt_imp <= 15.0)
    # H-vbrc-h: VB cumulative burn 1.0–1.5 yr at impulsive
    score("H-vbrc-h", "Variant B cumulative burn at impulsive: 1.0–1.5 yr",
          f"{vb_imp_cum:.2f} yr", 1.0 <= vb_imp_cum <= 1.5)
    # H-vbrc-i: VB / Arch E cumulative ratio ≤ 0.20 at matched 500 kWe + 200-t chunk
    score("H-vbrc-i", "Variant B / Arch E cumulative burn ratio ≤ 0.20",
          f"{ratio_vb_ae:.3f}", ratio_vb_ae <= 0.20)
    # H-vbrc-j: VB clears Kilopower 10-yr target by ≥ 8-yr margin
    margin_vb = KILOPOWER_TARGET_YR - vb_imp_cum
    score("H-vbrc-j", "Variant B reactor-life margin vs 10-yr Kilopower target ≥ 8 yr",
          f"{margin_vb:.2f} yr margin", margin_vb >= 8.0)
    # H-vbrc-k: Arch E cumulative reproduces R12's 11.37 yr within ±25%
    score("H-vbrc-k", "Arch E_500 cumulative burn 8.5–14.2 yr (R12 stated 11.37 yr ± 25%)",
          f"{ae_ct_low_cum:.2f} yr",
          8.5 <= ae_ct_low_cum <= 14.2)
    # H-vbrc-l: no self-consistent VB cell at continuous-thrust dv (24.7, 32, 40.2)
    ct_feasibilities = [vb_cells[dv]["inbound"]["feasible"] for dv in
                        [DV_INBOUND_CT_LOW, DV_INBOUND_CT_MID, DV_INBOUND_CT_HIGH]]
    score("H-vbrc-l", "No self-consistent Variant B cell at any of CT inbound dv ∈ {24.7, 32, 40.2}",
          f"feasibilities = {ct_feasibilities}",
          not any(ct_feasibilities))
    # H-vbrc-m: impulsive yields self-consistent cell; continuous-thrust does not
    imp_feasible = vb_cells[DV_INBOUND_IMPULSIVE]["inbound"]["feasible"]
    score("H-vbrc-m", "Impulsive cell feasible AND all continuous-thrust cells infeasible",
          f"imp_feasible={imp_feasible}, CT feasibilities={ct_feasibilities}",
          imp_feasible and not any(ct_feasibilities))
    # H-vbrc-n: required chunk for self-consistency at CT 24.7 km/s with delivered ≥ 30 t is ≥ 250 t
    score("H-vbrc-n", "Required chunk for VB at CT 24.7 km/s + delivered ≥ 30 t is ≥ 250 t",
          f"required chunk = {required_chunk_30t:.1f} t",
          required_chunk_30t >= 250.0)

    # ---- Write outputs ----
    with (RESULTS / "burn_consistency.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["arch", "dv_inbound_km_s", "m_dry_t", "thrust_N",
                    "m_prop_t", "delivered_t", "t_burn_yr",
                    "cumulative_reactor_burn_yr", "round_trip_yr", "feasible"])
        for dv, c in vb_cells.items():
            ib = c["inbound"]
            w.writerow(["VariantB", dv, c["m_dry_t"], ib["thrust_N"],
                        ib["m_prop_t"], ib["delivered_t"], ib["t_burn_yr"],
                        c["cumulative_reactor_burn_yr"], c["round_trip_yr"], ib["feasible"]])
        for dv_in, c in ae_cells.items():
            out, inb = c["outbound"], c["inbound"]
            w.writerow(["ArchE_500", dv_in, c["m_dry_t"], inb["thrust_N"],
                        inb["m_prop_t"], inb["delivered_t"],
                        out["t_burn_yr"] + inb["t_burn_yr"],
                        c["cumulative_reactor_burn_yr"], c["round_trip_yr"], inb["feasible"]])

    lines = ["# R-variant-B-burn-consistency — hypothesis scoring",
             "",
             "| ID | Predicted | Measured | Verdict |",
             "|---|---|---|---|"]
    for h in scoring:
        lines.append(f"| {h['id']} | {h['predicted']} | {h['measured']} | **{h['verdict']}** |")
    (RESULTS / "hypothesis_scoring.md").write_text("\n".join(lines) + "\n")

    held = sum(1 for h in scoring if h["verdict"] == "HELD")
    falsified = sum(1 for h in scoring if h["verdict"] == "FALSIFIED")
    print(f"\nScoring: {held} HELD, {falsified} FALSIFIED of {len(scoring)}")


if __name__ == "__main__":
    main()
