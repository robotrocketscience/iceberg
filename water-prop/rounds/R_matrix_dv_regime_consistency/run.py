"""R-matrix-dv-regime-consistency — does the matrix's verdict depend on dv-regime
choice? Sweep (Variant B, Arch E_500) × (impulsive, continuous-thrust) inbound
dv at 500 kWe / 200-t chunk.

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

REACTOR_KWE = 500.0
CHUNK_T = 200.0
SATURN_OPS_YR = 0.5
L0_05_CEILING_YR = 15.0
L0_09_FLOOR_T = 50.0
KILOPOWER_LIFE_YR = 10.0

# DV regimes
DV_INBOUND_IMPULSIVE = 6.42       # matrix Variant B
DV_INBOUND_CT_LOW = 24.7          # titan low
DV_OUTBOUND_IMPULSIVE = 9.0       # matrix pre-rhea outbound impulsive
DV_OUTBOUND_CT = 29.56            # rhea high-elliptical continuous-thrust

ISP_VARIANT_B = 2000.0
ISP_ARCH_E = 2934.0
ISP_HYDROLOX = 450.0  # for H-mdvc-l


def thrust_and_mdot(power_kwe: float, isp_s: float, eta: float = ETA_THR):
    v_e = isp_s * G0
    T = 2.0 * eta * power_kwe * 1000.0 / v_e
    return v_e, T, T / v_e


def chunk_fed_inbound(power_kwe: float, isp_s: float, dv_km_s: float,
                       chunk_t: float, m_dry_t: float) -> dict:
    v_e, T, mdot = thrust_and_mdot(power_kwe, isp_s)
    m_init = m_dry_t + chunk_t
    mr = math.exp(dv_km_s * 1000.0 / v_e)
    m_prop = m_init * (1.0 - 1.0 / mr)
    burn_yr = (m_prop * 1000.0 / mdot) / YEAR_S
    return {"m_prop_t": m_prop, "delivered_t": chunk_t - m_prop,
            "t_burn_yr": burn_yr, "feasible": (m_prop <= chunk_t) and (chunk_t - m_prop >= 0)}


def electric_outbound_dry_end(power_kwe: float, isp_s: float, dv_km_s: float,
                                m_dry_t: float) -> dict:
    v_e, T, mdot = thrust_and_mdot(power_kwe, isp_s)
    mr = math.exp(dv_km_s * 1000.0 / v_e)
    m_prop = m_dry_t * (mr - 1.0)
    burn_yr = (m_prop * 1000.0 / mdot) / YEAR_S
    return {"m_prop_t": m_prop, "t_burn_yr": burn_yr, "mass_ratio": mr}


def chemical_inbound_propellant_required(dv_km_s: float, m_dry_t: float,
                                           chunk_t: float, isp_s: float) -> float:
    """For an impulsive chemical inbound braking, m_init_wet includes m_dry + chunk
    (carried back) + m_prop_chemical. Solve for m_prop_chemical.

    Tsiolkovsky: m_init / m_final = MR; m_init = m_dry + chunk + m_chem;
                  m_final = m_dry + chunk. So MR = 1 + m_chem / (m_dry + chunk).
    Therefore m_chem = (m_dry + chunk) × (MR - 1).
    """
    v_e = isp_s * G0
    mr = math.exp(dv_km_s * 1000.0 / v_e)
    return (m_dry_t + chunk_t) * (mr - 1.0)


def case(name: str, *, m_dry_t: float, isp_s: float,
          outbound_kind: str, dv_outbound_km_s: float,
          dv_inbound_km_s: float) -> dict:
    """outbound_kind ∈ {'chemical', 'electric'}.
    For 'chemical', outbound burn time = 0 (instantaneous; reactor not used for propulsion).
    """
    if outbound_kind == "chemical":
        out_burn_yr = 0.0
        out_m_prop_t = float("nan")  # not relevant; chemical prop carried separately
    elif outbound_kind == "electric":
        out = electric_outbound_dry_end(REACTOR_KWE, isp_s, dv_outbound_km_s, m_dry_t)
        out_burn_yr = out["t_burn_yr"]
        out_m_prop_t = out["m_prop_t"]
    else:
        raise ValueError(outbound_kind)
    inb = chunk_fed_inbound(REACTOR_KWE, isp_s, dv_inbound_km_s, CHUNK_T, m_dry_t)
    t_cruise = hohmann_cruise_yr()
    round_trip = out_burn_yr + t_cruise + SATURN_OPS_YR + inb["t_burn_yr"] + t_cruise
    cumulative_reactor_burn = out_burn_yr + inb["t_burn_yr"]
    return {
        "name": name, "m_dry_t": m_dry_t, "isp_s": isp_s,
        "outbound_kind": outbound_kind, "dv_outbound_km_s": dv_outbound_km_s,
        "dv_inbound_km_s": dv_inbound_km_s,
        "out_burn_yr": out_burn_yr, "out_m_prop_t": out_m_prop_t,
        "in_burn_yr": inb["t_burn_yr"], "in_m_prop_t": inb["m_prop_t"],
        "delivered_t": inb["delivered_t"], "feasible_prop": inb["feasible"],
        "round_trip_yr": round_trip,
        "cumulative_reactor_burn_yr": cumulative_reactor_burn,
        "L0_05_compliant": round_trip <= L0_05_CEILING_YR,
        "L0_09_compliant": inb["delivered_t"] >= L0_09_FLOOR_T,
        "reactor_life_compliant": cumulative_reactor_burn <= KILOPOWER_LIFE_YR,
    }


def main() -> None:
    print("R-matrix-dv-regime-consistency")
    model = MASS_MODELS["bundled_10_W_per_kg"]
    m_dry = dry_mass_t(model, REACTOR_KWE, m_prop_t=0.0)
    print(f"  m_dry (bundled 10 W/kg, 500 kWe) = {m_dry:.1f} t\n")

    cases = [
        case("VariantB_impulsive",
             m_dry_t=m_dry, isp_s=ISP_VARIANT_B,
             outbound_kind="chemical", dv_outbound_km_s=0.0,
             dv_inbound_km_s=DV_INBOUND_IMPULSIVE),
        case("VariantB_continuous_thrust",
             m_dry_t=m_dry, isp_s=ISP_VARIANT_B,
             outbound_kind="chemical", dv_outbound_km_s=0.0,
             dv_inbound_km_s=DV_INBOUND_CT_LOW),
        case("ArchE_impulsive",
             m_dry_t=m_dry, isp_s=ISP_ARCH_E,
             outbound_kind="electric", dv_outbound_km_s=DV_OUTBOUND_IMPULSIVE,
             dv_inbound_km_s=DV_INBOUND_IMPULSIVE),
        case("ArchE_continuous_thrust",
             m_dry_t=m_dry, isp_s=ISP_ARCH_E,
             outbound_kind="electric", dv_outbound_km_s=DV_OUTBOUND_CT,
             dv_inbound_km_s=DV_INBOUND_CT_LOW),
    ]

    print(f"  {'Case':<32} {'out_burn':>9} {'in_burn':>9} {'RT_yr':>7} {'delivered':>10} {'cum_burn':>9} {'L0-05':>6} {'L0-09':>6} {'Rlife':>6}")
    for c in cases:
        print(f"  {c['name']:<32} {c['out_burn_yr']:>9.2f} {c['in_burn_yr']:>9.2f} "
              f"{c['round_trip_yr']:>7.2f} {c['delivered_t']:>10.1f} "
              f"{c['cumulative_reactor_burn_yr']:>9.2f} "
              f"{'OK' if c['L0_05_compliant'] else 'FAIL':>6} "
              f"{'OK' if c['L0_09_compliant'] else 'FAIL':>6} "
              f"{'OK' if c['reactor_life_compliant'] else 'FAIL':>6}")

    # H-mdvc-l: chemical inbound braking mass for Variant B at impulsive
    m_chem_required = chemical_inbound_propellant_required(
        DV_INBOUND_IMPULSIVE, m_dry, CHUNK_T, ISP_HYDROLOX)
    print(f"\nChemical inbound braking at impulsive 6.42 km/s, hydrolox ISP 450 s:")
    print(f"  m_dry + chunk = {m_dry + CHUNK_T:.1f} t")
    print(f"  required chemical propellant = {m_chem_required:.1f} t  "
          f"({'> 200-t chunk' if m_chem_required > CHUNK_T else '<= 200-t chunk'})")

    # ---- Hypothesis scoring ----
    by_name = {c["name"]: c for c in cases}
    arch_E_imp = by_name["ArchE_impulsive"]
    arch_E_ct = by_name["ArchE_continuous_thrust"]
    vb_imp = by_name["VariantB_impulsive"]
    vb_ct = by_name["VariantB_continuous_thrust"]

    scoring = []
    def score(hid, predicted, measured, holds):
        scoring.append({"id": hid, "predicted": predicted, "measured": measured,
                        "verdict": "HELD" if holds else "FALSIFIED"})

    score("H-mdvc-a", "Arch E_500 RT at impulsive 14.5–16.0 yr",
          f"{arch_E_imp['round_trip_yr']:.2f} yr",
          14.5 <= arch_E_imp["round_trip_yr"] <= 16.0)
    score("H-mdvc-b", "Arch E RT_impulsive ≤ 18.6 yr (≥ 5 yr shorter than CT 23.6)",
          f"{arch_E_imp['round_trip_yr']:.2f} yr vs CT {arch_E_ct['round_trip_yr']:.2f} yr",
          arch_E_imp["round_trip_yr"] <= 18.6)
    score("H-mdvc-c", "Arch E cumulative burn at impulsive ≤ 4 yr",
          f"{arch_E_imp['cumulative_reactor_burn_yr']:.2f} yr",
          arch_E_imp["cumulative_reactor_burn_yr"] <= 4.0)
    score("H-mdvc-d", "Arch E delivered at impulsive > 60 t",
          f"{arch_E_imp['delivered_t']:.1f} t",
          arch_E_imp["delivered_t"] > 60.0)
    score("H-mdvc-e", "Variant B RT at CT 24.7 km/s in [15.5, 16.5] yr",
          f"{vb_ct['round_trip_yr']:.2f} yr",
          15.5 <= vb_ct["round_trip_yr"] <= 16.5)
    score("H-mdvc-f", "Variant B delivered at CT 24.7 km/s ≤ 25 t",
          f"{vb_ct['delivered_t']:.1f} t",
          vb_ct["delivered_t"] <= 25.0)
    ratio_burn = vb_ct["cumulative_reactor_burn_yr"] / arch_E_ct["cumulative_reactor_burn_yr"]
    score("H-mdvc-g", "Variant B / Arch E cumulative burn ratio at CT ≤ 0.45",
          f"{ratio_burn:.3f}", ratio_burn <= 0.45)
    score("H-mdvc-h", "At CT, both architectures L0-05-non-compliant",
          f"VB_RT={vb_ct['round_trip_yr']:.2f}, E_RT={arch_E_ct['round_trip_yr']:.2f}",
          (vb_ct["round_trip_yr"] > 15.0) and (arch_E_ct["round_trip_yr"] > 15.0))
    only_vb_close_impulsive = vb_imp["L0_05_compliant"] and not arch_E_imp["L0_05_compliant"]
    score("H-mdvc-i", "At impulsive, only Variant B closes L0-05",
          f"VB_compliant={vb_imp['L0_05_compliant']}, E_compliant={arch_E_imp['L0_05_compliant']}",
          only_vb_close_impulsive)
    rt_diff = arch_E_ct["round_trip_yr"] - arch_E_imp["round_trip_yr"]
    score("H-mdvc-j", "Arch E RT swing between impulsive and CT ≥ 5 yr",
          f"{rt_diff:.2f} yr swing",
          rt_diff >= 5.0)
    any_full_compliant = any(c["L0_05_compliant"] and c["L0_09_compliant"] for c in cases)
    score("H-mdvc-k", "No (arch, regime) cell satisfies L0-05 AND L0-09 ≥ 50 t at 500 kWe / 200-t",
          f"any_full_compliant={any_full_compliant}",
          not any_full_compliant)
    score("H-mdvc-l", "Required chemical inbound prop > 200-t chunk at impulsive 6.42 km/s",
          f"{m_chem_required:.1f} t",
          m_chem_required > 200.0)

    # ---- Write outputs ----
    with (RESULTS / "regime_grid.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(cases[0].keys()))
        w.writeheader()
        for c in cases:
            w.writerow(c)

    lines = ["# R-matrix-dv-regime-consistency — hypothesis scoring",
             "",
             "| ID | Predicted | Measured | Verdict |",
             "|---|---|---|---|"]
    for h in scoring:
        lines.append(f"| {h['id']} | {h['predicted']} | {h['measured']} | **{h['verdict']}** |")
    (RESULTS / "hypothesis_scoring.md").write_text("\n".join(lines) + "\n")

    held = sum(1 for h in scoring if h["verdict"] == "HELD")
    falsified = sum(1 for h in scoring if h["verdict"] == "FALSIFIED")
    print(f"\nScoring: {held} HELD, {falsified} FALSIFIED of {len(scoring)}")

    # ---- Summary ----
    sum_lines = [
        "# R-matrix-dv-regime-consistency — summary",
        "",
        "## The 2×2 grid",
        "",
        "| Case | out_burn (yr) | in_burn (yr) | RT (yr) | delivered (t) | cum_burn (yr) | L0-05 | L0-09 | R-life |",
        "|---|---:|---:|---:|---:|---:|:-:|:-:|:-:|",
    ]
    for c in cases:
        sum_lines.append(
            f"| {c['name']} | {c['out_burn_yr']:.2f} | {c['in_burn_yr']:.2f} | "
            f"{c['round_trip_yr']:.2f} | {c['delivered_t']:.1f} | "
            f"{c['cumulative_reactor_burn_yr']:.2f} | "
            f"{'OK' if c['L0_05_compliant'] else 'FAIL'} | "
            f"{'OK' if c['L0_09_compliant'] else 'FAIL'} | "
            f"{'OK' if c['reactor_life_compliant'] else 'FAIL'} |"
        )
    sum_lines += [
        "",
        f"## Chemical inbound braking sanity (H-mdvc-l)",
        "",
        f"Required hydrolox propellant for 6.42 km/s impulsive inbound = **{m_chem_required:.1f} t**.",
        f"Chunk available = 200 t. **{'Exceeds' if m_chem_required > 200 else 'Within'} the chunk-as-chemical-prop capacity.**",
        "",
        f"## Scoring: {held} HELD / {falsified} FALSIFIED of {len(scoring)}",
        "",
        "See `hypothesis_scoring.md` for per-hypothesis verdicts.",
    ]
    (RESULTS / "summary.md").write_text("\n".join(sum_lines) + "\n")
    print(f"Wrote {RESULTS}/{{regime_grid.csv, hypothesis_scoring.md, summary.md}}")


if __name__ == "__main__":
    main()
