"""R-chemical-trim-vs-all-electric-earth-arrival — what propulsion does the
matrix's surviving cell actually require?

Tests whether the matrix's "500-kWe chemical-kick + electric-inbound" cell
closes under continuous-thrust accounting, with and without a chemical-trim
burn at Earth capture. Five scenarios A–E vary the split between chemical
(Isp 450 s, hydrolox chunk-fed) and electric (Isp 2000 s, integrated
continuous-thrust) across the five inbound segments per titan's
decomposition.

Run from the rhea worktree:
    python water-prop/rounds/R_chemical_trim_vs_all_electric_earth_arrival/run.py

Deterministic; no random seeds.
"""

from __future__ import annotations

import json
import math
from pathlib import Path


G0 = 9.81  # standard gravity, metres per second squared

# --- Specific impulses
ISP_CHEM_S = 450.0     # hydrolox, chunk-fed
ISP_ELEC_S = 2000.0    # matrix default

VE_CHEM_KM_S = ISP_CHEM_S * G0 / 1000.0   # ~4.41 km/s
VE_ELEC_KM_S = ISP_ELEC_S * G0 / 1000.0   # ~19.62 km/s

# --- Inbound delta-velocity segment values (km/s, high-elliptical Saturn-departure case per titan)
DV_SAT_DEPARTURE_CHEM = 3.0     # segment (1) — chemical kick at high-elliptical Saturn-departure (matrix Variant B)
DV_HEL_SATURN = 5.44             # segment (2) — heliocentric Saturn-to-Hohmann-aphelion decel, integrated continuous-thrust
DV_HEL_EARTH_NO_LGA = 10.30      # segment (4) — heliocentric Earth-side decel, integrated continuous-thrust
DV_LGA_CREDIT = 2.0              # lunar gravity assist credit applied to segment (4)
DV_HEL_EARTH = DV_HEL_EARTH_NO_LGA - DV_LGA_CREDIT  # 8.30
DV_EARTH_CAPTURE_IMPULSIVE = 2.42  # segment (5a) — chemical impulsive capture from v_inf=3 km/s to e=0.33 elliptical at 300 km
DV_EARTH_EDELBAUM_SMALL = 1.18     # segment (5b) — Edelbaum from elliptical periapsis (0.33 e) to circular at 300 km
DV_EARTH_EDELBAUM_FULL = 7.67      # combined (5a)+(5b) electric continuous-thrust integrated (titan's number)


def tsiolkovsky_mass_ratio(dv_km_s: float, ve_km_s: float) -> float:
    """Return m_initial / m_final for a burn of delta-velocity dv at exhaust velocity ve."""
    return math.exp(dv_km_s / ve_km_s)


def apply_burn(m_in_t: float, dv_km_s: float, ve_km_s: float) -> float:
    """Apply Tsiolkovsky in delivery order: input mass, produce post-burn mass."""
    return m_in_t / tsiolkovsky_mass_ratio(dv_km_s, ve_km_s)


def scenario(name: str, segments: list[tuple[str, float, float]], chunk_t: float) -> dict:
    """Compute Tsiolkovsky chain across an ordered list of burns.

    Each segment is (label, dv_km_s, ve_km_s). Burns applied in order from
    chunk-grappled mass to delivered mass.
    """
    m_running = chunk_t
    chain = []
    dv_chem = 0.0
    dv_elec = 0.0
    for label, dv, ve in segments:
        m_post = apply_burn(m_running, dv, ve)
        chain.append({
            "label": label,
            "dv_km_s": dv,
            "ve_km_s": ve,
            "mass_before_t": m_running,
            "mass_after_t": m_post,
            "propellant_burned_t": m_running - m_post,
        })
        if abs(ve - VE_CHEM_KM_S) < 1e-6:
            dv_chem += dv
        else:
            dv_elec += dv
        m_running = m_post

    return {
        "scenario": name,
        "chunk_t": chunk_t,
        "delivered_t": m_running,
        "delivered_fraction": m_running / chunk_t,
        "dv_chemical_km_s": dv_chem,
        "dv_electric_km_s": dv_elec,
        "dv_total_km_s": dv_chem + dv_elec,
        "chain": chain,
    }


# -----------------------------------------------------------------------------
# Scenario definitions per STUDY.md table

def build_scenario_A(chunk_t: float) -> dict:
    """Matrix-literal: heliocentric segments treated as Hohmann-free (impulsive accounting).

    Only segments (1) Saturn-departure chemical, (5a) Earth-capture chemical, (5b)
    Edelbaum electric are paid. This reproduces the matrix's stated 6.42 km/s
    inbound number.
    """
    return scenario(
        "A — matrix literal (impulsive Hohmann + chemical Earth-capture)",
        [
            ("(1) Saturn-departure chemical", DV_SAT_DEPARTURE_CHEM, VE_CHEM_KM_S),
            ("(5a) Earth-capture chemical (impulsive)", DV_EARTH_CAPTURE_IMPULSIVE, VE_CHEM_KM_S),
            ("(5b) Edelbaum electric (small spiral)", DV_EARTH_EDELBAUM_SMALL, VE_ELEC_KM_S),
        ],
        chunk_t,
    )


def build_scenario_B(chunk_t: float) -> dict:
    """All-electric inbound (matrix cell as labelled): every post-Saturn-departure
    segment paid electric continuous-thrust.
    """
    return scenario(
        "B — all-electric inbound (matrix cell as written)",
        [
            ("(1) Saturn-departure chemical", DV_SAT_DEPARTURE_CHEM, VE_CHEM_KM_S),
            ("(2) Heliocentric Saturn-to-Hohmann electric", DV_HEL_SATURN, VE_ELEC_KM_S),
            ("(4) Heliocentric Earth-side electric (with LGA)", DV_HEL_EARTH, VE_ELEC_KM_S),
            ("(5) Earth Edelbaum capture-spiral electric (full)", DV_EARTH_EDELBAUM_FULL, VE_ELEC_KM_S),
        ],
        chunk_t,
    )


def build_scenario_C(chunk_t: float) -> dict:
    """Chemical-trim at Earth-capture only. Heliocentric segments are electric;
    Earth-capture impulsive is chemical; small Edelbaum after capture is electric.
    """
    return scenario(
        "C — chemical-trim Earth-capture + electric elsewhere",
        [
            ("(1) Saturn-departure chemical", DV_SAT_DEPARTURE_CHEM, VE_CHEM_KM_S),
            ("(2) Heliocentric Saturn-to-Hohmann electric", DV_HEL_SATURN, VE_ELEC_KM_S),
            ("(4) Heliocentric Earth-side electric (with LGA)", DV_HEL_EARTH, VE_ELEC_KM_S),
            ("(5a) Earth-capture chemical (impulsive)", DV_EARTH_CAPTURE_IMPULSIVE, VE_CHEM_KM_S),
            ("(5b) Edelbaum electric (small spiral)", DV_EARTH_EDELBAUM_SMALL, VE_ELEC_KM_S),
        ],
        chunk_t,
    )


def build_scenario_D(chunk_t: float) -> dict:
    """Full chemical Earth-arrival. Heliocentric segments electric; both Earth
    capture and Edelbaum circularisation chemical.
    """
    return scenario(
        "D — full chemical Earth-arrival (capture + Edelbaum chemical)",
        [
            ("(1) Saturn-departure chemical", DV_SAT_DEPARTURE_CHEM, VE_CHEM_KM_S),
            ("(2) Heliocentric Saturn-to-Hohmann electric", DV_HEL_SATURN, VE_ELEC_KM_S),
            ("(4) Heliocentric Earth-side electric (with LGA)", DV_HEL_EARTH, VE_ELEC_KM_S),
            ("(5a) Earth-capture chemical (impulsive)", DV_EARTH_CAPTURE_IMPULSIVE, VE_CHEM_KM_S),
            ("(5b) Edelbaum chemical (small spiral)", DV_EARTH_EDELBAUM_SMALL, VE_CHEM_KM_S),
        ],
        chunk_t,
    )


def build_scenario_E(chunk_t: float) -> dict:
    """Pure chemical inbound (worst case bracketing). Every segment chemical."""
    return scenario(
        "E — pure chemical inbound (bracketing only)",
        [
            ("(1) Saturn-departure chemical", DV_SAT_DEPARTURE_CHEM, VE_CHEM_KM_S),
            ("(2) Heliocentric Saturn-to-Hohmann chemical", DV_HEL_SATURN, VE_CHEM_KM_S),
            ("(4) Heliocentric Earth-side chemical (with LGA)", DV_HEL_EARTH, VE_CHEM_KM_S),
            ("(5a) Earth-capture chemical (impulsive)", DV_EARTH_CAPTURE_IMPULSIVE, VE_CHEM_KM_S),
            ("(5b) Edelbaum chemical (small spiral)", DV_EARTH_EDELBAUM_SMALL, VE_CHEM_KM_S),
        ],
        chunk_t,
    )


SCENARIO_BUILDERS = {
    "A": build_scenario_A,
    "B": build_scenario_B,
    "C": build_scenario_C,
    "D": build_scenario_D,
    "E": build_scenario_E,
}


def main() -> dict:
    base_chunk_t = 50.0

    base_case = {name: builder(base_chunk_t) for name, builder in SCENARIO_BUILDERS.items()}

    # H-chem-g — sensitivity on chunk mass (Tsiolkovsky should be mass-ratio invariant)
    chunk_sweep = {}
    for chunk in [25.0, 50.0, 100.0, 200.0]:
        chunk_sweep[f"chunk_{chunk:.0f}t"] = {
            name: builder(chunk) for name, builder in SCENARIO_BUILDERS.items()
        }

    # Sensitivity on lunar gravity assist credit — does removing LGA matter?
    # Re-run scenarios B, C with LGA=0 (worst case)
    def with_no_lga(chunk_t: float, base_builder):
        # Patch DV_HEL_EARTH globally is hacky; re-create scenarios inline
        if base_builder is build_scenario_B:
            return scenario(
                "B (no-LGA) — all-electric inbound",
                [
                    ("(1) Saturn-departure chemical", DV_SAT_DEPARTURE_CHEM, VE_CHEM_KM_S),
                    ("(2) Heliocentric Saturn-to-Hohmann electric", DV_HEL_SATURN, VE_ELEC_KM_S),
                    ("(4) Heliocentric Earth-side electric (no LGA)", DV_HEL_EARTH_NO_LGA, VE_ELEC_KM_S),
                    ("(5) Earth Edelbaum capture-spiral electric (full)", DV_EARTH_EDELBAUM_FULL, VE_ELEC_KM_S),
                ],
                chunk_t,
            )
        if base_builder is build_scenario_C:
            return scenario(
                "C (no-LGA) — chemical-trim Earth-capture",
                [
                    ("(1) Saturn-departure chemical", DV_SAT_DEPARTURE_CHEM, VE_CHEM_KM_S),
                    ("(2) Heliocentric Saturn-to-Hohmann electric", DV_HEL_SATURN, VE_ELEC_KM_S),
                    ("(4) Heliocentric Earth-side electric (no LGA)", DV_HEL_EARTH_NO_LGA, VE_ELEC_KM_S),
                    ("(5a) Earth-capture chemical (impulsive)", DV_EARTH_CAPTURE_IMPULSIVE, VE_CHEM_KM_S),
                    ("(5b) Edelbaum electric (small spiral)", DV_EARTH_EDELBAUM_SMALL, VE_ELEC_KM_S),
                ],
                chunk_t,
            )
        raise ValueError("unknown builder")

    no_lga = {
        "B_no_lga": with_no_lga(base_chunk_t, build_scenario_B),
        "C_no_lga": with_no_lga(base_chunk_t, build_scenario_C),
    }

    return {
        "constants": {
            "isp_chemical_s": ISP_CHEM_S,
            "isp_electric_s": ISP_ELEC_S,
            "ve_chemical_km_s": VE_CHEM_KM_S,
            "ve_electric_km_s": VE_ELEC_KM_S,
            "dv_saturn_departure_chem_km_s": DV_SAT_DEPARTURE_CHEM,
            "dv_heliocentric_saturn_km_s": DV_HEL_SATURN,
            "dv_heliocentric_earth_no_lga_km_s": DV_HEL_EARTH_NO_LGA,
            "dv_lga_credit_km_s": DV_LGA_CREDIT,
            "dv_heliocentric_earth_with_lga_km_s": DV_HEL_EARTH,
            "dv_earth_capture_impulsive_km_s": DV_EARTH_CAPTURE_IMPULSIVE,
            "dv_earth_edelbaum_small_km_s": DV_EARTH_EDELBAUM_SMALL,
            "dv_earth_edelbaum_full_km_s": DV_EARTH_EDELBAUM_FULL,
            "matrix_stated_inbound_dv_km_s": 6.42,
        },
        "base_case_50t": base_case,
        "chunk_sensitivity": chunk_sweep,
        "lga_sensitivity": no_lga,
    }


def write_outputs(result: dict, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / "results.json", "w") as f:
        json.dump(result, f, indent=2, sort_keys=True)

    lines = []
    lines.append("# R-chemical-trim-vs-all-electric-earth-arrival — results tables\n")
    lines.append("Generated by run.py. Do not edit by hand.\n")

    lines.append("## Base case (50 t chunk, Isp_chem 450 s, Isp_elec 2000 s, with 2.0 km/s LGA credit)\n")
    lines.append("| Scenario | chemical dv (km/s) | electric dv (km/s) | total dv (km/s) | delivered (t) | delivered fraction |")
    lines.append("|---|---:|---:|---:|---:|---:|")
    for name in ["A", "B", "C", "D", "E"]:
        s = result["base_case_50t"][name]
        lines.append(
            f"| {s['scenario']} | {s['dv_chemical_km_s']:.2f} | {s['dv_electric_km_s']:.2f} | "
            f"{s['dv_total_km_s']:.2f} | {s['delivered_t']:.2f} | {s['delivered_fraction']*100:.1f}% |"
        )
    lines.append("")

    lines.append("## Per-scenario burn chain (50 t chunk)\n")
    for name in ["A", "B", "C", "D"]:
        s = result["base_case_50t"][name]
        lines.append(f"### Scenario {name}: {s['scenario']}\n")
        lines.append("| Segment | dv (km/s) | ve (km/s) | mass before (t) | mass after (t) | propellant (t) |")
        lines.append("|---|---:|---:|---:|---:|---:|")
        for step in s["chain"]:
            lines.append(
                f"| {step['label']} | {step['dv_km_s']:.2f} | {step['ve_km_s']:.2f} | "
                f"{step['mass_before_t']:.2f} | {step['mass_after_t']:.2f} | "
                f"{step['propellant_burned_t']:.2f} |"
            )
        lines.append("")

    lines.append("## Chunk-size sensitivity (delivered fraction should be Tsiolkovsky-invariant)\n")
    lines.append("| Scenario | 25 t | 50 t | 100 t | 200 t |")
    lines.append("|---|---:|---:|---:|---:|")
    for name in ["A", "B", "C", "D", "E"]:
        row = [name]
        for chunk in [25, 50, 100, 200]:
            df = result["chunk_sensitivity"][f"chunk_{chunk}t"][name]["delivered_fraction"]
            row.append(f"{df*100:.1f}%")
        lines.append("| " + " | ".join(row) + " |")
    lines.append("")

    lines.append("## Lunar gravity assist credit sensitivity (50 t chunk)\n")
    lines.append("| Scenario | With LGA (2.0 km/s credit) | Without LGA | Delta in delivered fraction |")
    lines.append("|---|---:|---:|---:|")
    for short, no_lga_key in [("B", "B_no_lga"), ("C", "C_no_lga")]:
        with_df = result["base_case_50t"][short]["delivered_fraction"]
        wo_df = result["lga_sensitivity"][no_lga_key]["delivered_fraction"]
        lines.append(f"| {short} | {with_df*100:.1f}% | {wo_df*100:.1f}% | {(with_df - wo_df)*100:+.1f} ppt |")
    lines.append("")

    with open(out_dir / "tables.md", "w") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    result = main()
    out_dir = Path(__file__).resolve().parent / "results"
    write_outputs(result, out_dir)
    print(f"wrote {out_dir}/results.json and {out_dir}/tables.md")
    print()
    print("Base case (50 t chunk):")
    for name in ["A", "B", "C", "D", "E"]:
        s = result["base_case_50t"][name]
        print(
            f"  Scenario {name}: dv_chem={s['dv_chemical_km_s']:5.2f} km/s  "
            f"dv_elec={s['dv_electric_km_s']:5.2f} km/s  "
            f"dv_total={s['dv_total_km_s']:5.2f} km/s  "
            f"delivered={s['delivered_t']:5.2f} t  "
            f"({s['delivered_fraction']*100:5.1f}%)"
        )
