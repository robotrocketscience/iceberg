"""R-saturn-side-solar-thermal — deployed-mass model.

Parametric model: deployed mass of a Saturn-side solar-thermal-electrolysis
stack vs useful electrolysis output, compared to fission benchmarks.

Deterministic given inputs. No randomness. Writes JSON + a markdown table.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Iterable

SOLAR_FLUX_EARTH_W_PER_M2 = 1361.0
SATURN_DISTANCE_AU = 9.58
SOLAR_FLUX_SATURN_W_PER_M2 = SOLAR_FLUX_EARTH_W_PER_M2 / SATURN_DISTANCE_AU**2


def stack_mass(
    target_kw_useful: float,
    mirror_areal_density_kg_per_m2: float,
    conversion_path: str,
    duty_cycle_factor: float,
    optical_efficiency: float = 0.80,
    eta_stirling: float = 0.28,
    eta_pem_electrolyzer: float = 0.70,
    eta_soec: float = 0.50,
    structure_overhead_factor: float = 1.0,
    receiver_fraction_of_mirror: float = 0.10,
    stirling_kg_per_kwe: float = 10.0,
    pem_kg_per_kwe: float = 5.0,
    soec_kg_per_kwth: float = 8.0,
    radiator_kg_per_kwth_waste: float = 50.0,
) -> dict:
    """Compute deployed mass for the Saturn-side solar-thermal stack.

    target_kw_useful: useful electrolysis output in kilowatts-electric-equivalent
        (i.e. the rate at which chemical energy is being deposited in H2+O2
        product). For Stirling path this is power_thermal * eta_stirling *
        eta_pem. For SOEC path this is power_thermal * eta_soec.
    """
    if conversion_path not in {"stirling", "soec"}:
        raise ValueError(f"unknown conversion_path: {conversion_path}")

    if conversion_path == "stirling":
        eta_thermal_to_useful = eta_stirling * eta_pem_electrolyzer
        waste_heat_fraction = 1.0 - eta_stirling
    else:  # soec — direct high-temperature electrolysis, no power cycle
        eta_thermal_to_useful = eta_soec
        waste_heat_fraction = 1.0 - eta_soec

    flux_useful_per_m2 = (
        SOLAR_FLUX_SATURN_W_PER_M2 * optical_efficiency * eta_thermal_to_useful
    )

    a_mirror_m2 = (target_kw_useful * 1000.0 / flux_useful_per_m2) * duty_cycle_factor

    m_mirror_kg = a_mirror_m2 * mirror_areal_density_kg_per_m2
    m_structure_kg = m_mirror_kg * structure_overhead_factor
    m_receiver_kg = m_mirror_kg * receiver_fraction_of_mirror

    if conversion_path == "stirling":
        kwe = target_kw_useful / eta_pem_electrolyzer
        m_conversion_kg = kwe * stirling_kg_per_kwe + kwe * pem_kg_per_kwe
    else:
        kwth_input = target_kw_useful / eta_soec
        m_conversion_kg = kwth_input * soec_kg_per_kwth

    p_thermal_total_kw = target_kw_useful / eta_thermal_to_useful
    p_waste_thermal_kw = p_thermal_total_kw * waste_heat_fraction
    m_radiator_kg = p_waste_thermal_kw * radiator_kg_per_kwth_waste

    m_total_kg = (
        m_mirror_kg + m_structure_kg + m_receiver_kg + m_conversion_kg + m_radiator_kg
    )

    return {
        "target_kw_useful": target_kw_useful,
        "mirror_areal_density_kg_per_m2": mirror_areal_density_kg_per_m2,
        "conversion_path": conversion_path,
        "duty_cycle_factor": duty_cycle_factor,
        "a_mirror_m2": a_mirror_m2,
        "p_thermal_total_kw": p_thermal_total_kw,
        "p_waste_thermal_kw": p_waste_thermal_kw,
        "m_mirror_kg": m_mirror_kg,
        "m_structure_kg": m_structure_kg,
        "m_receiver_kg": m_receiver_kg,
        "m_conversion_kg": m_conversion_kg,
        "m_radiator_kg": m_radiator_kg,
        "m_total_kg": m_total_kg,
        "m_total_tonnes": m_total_kg / 1000.0,
        "kg_per_kw_useful": m_total_kg / target_kw_useful,
    }


def sweep() -> list[dict]:
    results: list[dict] = []
    for target_kw in (150.0, 200.0, 300.0, 500.0):
        for areal in (0.1, 0.3, 0.5, 1.0):
            for path in ("stirling", "soec"):
                for duty in (1.0, 1.5):
                    results.append(
                        stack_mass(
                            target_kw_useful=target_kw,
                            mirror_areal_density_kg_per_m2=areal,
                            conversion_path=path,
                            duty_cycle_factor=duty,
                        )
                    )
    return results


FISSION_BENCHMARKS_KG_PER_KW = {
    "FSP_stretch_10W_per_kg": 100.0,
    "FSP_phase1_contracted_5W_per_kg": 200.0,
    "KRUSTY_demonstrated_2p4W_per_kg": 416.0,
}


def classify(kg_per_kw: float) -> str:
    if kg_per_kw < FISSION_BENCHMARKS_KG_PER_KW["FSP_stretch_10W_per_kg"]:
        return "beats_FSP_stretch"
    elif kg_per_kw < FISSION_BENCHMARKS_KG_PER_KW["FSP_phase1_contracted_5W_per_kg"]:
        return "beats_FSP_phase1_baseline"
    elif kg_per_kw < FISSION_BENCHMARKS_KG_PER_KW["KRUSTY_demonstrated_2p4W_per_kg"]:
        return "beats_KRUSTY_demonstrated"
    else:
        return "worse_than_KRUSTY"


def write_results(results: Iterable[dict], outdir: Path) -> None:
    outdir.mkdir(parents=True, exist_ok=True)

    results_list = list(results)
    for r in results_list:
        r["fission_comparison"] = classify(r["kg_per_kw_useful"])

    payload = {
        "saturn_solar_flux_W_per_m2": SOLAR_FLUX_SATURN_W_PER_M2,
        "fission_benchmarks_kg_per_kw": FISSION_BENCHMARKS_KG_PER_KW,
        "results": results_list,
    }
    (outdir / "solar_thermal_grid.json").write_text(json.dumps(payload, indent=2))

    headers = [
        "target_kW",
        "areal_kg/m²",
        "path",
        "duty",
        "A_mirror_m²",
        "m_mirror_t",
        "m_radiator_t",
        "m_total_t",
        "kg/kW_useful",
        "vs_fission",
    ]
    lines = ["| " + " | ".join(headers) + " |",
             "|" + "|".join(["---"] * len(headers)) + "|"]
    for r in results_list:
        lines.append(
            "| {tk:.0f} | {ar:.1f} | {p} | {d:.1f} | {am:.0f} | {mm:.2f} | {mr:.2f} | {mt:.2f} | {kk:.0f} | {fc} |".format(
                tk=r["target_kw_useful"],
                ar=r["mirror_areal_density_kg_per_m2"],
                p=r["conversion_path"],
                d=r["duty_cycle_factor"],
                am=r["a_mirror_m2"],
                mm=r["m_mirror_kg"] / 1000.0,
                mr=r["m_radiator_kg"] / 1000.0,
                mt=r["m_total_tonnes"],
                kk=r["kg_per_kw_useful"],
                fc=r["fission_comparison"],
            )
        )

    (outdir / "tables.md").write_text(
        "# R-saturn-side-solar-thermal — results\n\n"
        f"Saturn solar flux: {SOLAR_FLUX_SATURN_W_PER_M2:.2f} W/m² (at {SATURN_DISTANCE_AU} AU)\n\n"
        f"Fission benchmarks (kg per kW-useful): {FISSION_BENCHMARKS_KG_PER_KW}\n\n"
        "Falsification rule: hypothesis upheld if conservative scenario "
        "(stirling, areal=1.0 kg/m², duty=1.5) yields kg/kW < 200. "
        "Falsified if conservative > 400. Middle band = same risk-class as FSP stretch.\n\n"
        + "\n".join(lines)
        + "\n"
    )


def main() -> None:
    here = Path(__file__).resolve().parent
    outdir = here / "results"
    results = sweep()
    write_results(results, outdir)

    print(f"Wrote {len(results)} rows to {outdir}/tables.md and solar_thermal_grid.json")
    print()
    print("Conservative scenarios (areal=1.0 kg/m², stirling, duty=1.5):")
    for r in results:
        if (
            r["mirror_areal_density_kg_per_m2"] == 1.0
            and r["conversion_path"] == "stirling"
            and r["duty_cycle_factor"] == 1.5
        ):
            print(
                f"  target {r['target_kw_useful']:.0f} kW: "
                f"total {r['m_total_tonnes']:.2f} t, "
                f"{r['kg_per_kw_useful']:.0f} kg/kW, "
                f"{r['fission_comparison']}"
            )
    print()
    print("Optimistic scenarios (areal=0.1 kg/m², soec, duty=1.0):")
    for r in results:
        if (
            r["mirror_areal_density_kg_per_m2"] == 0.1
            and r["conversion_path"] == "soec"
            and r["duty_cycle_factor"] == 1.0
        ):
            print(
                f"  target {r['target_kw_useful']:.0f} kW: "
                f"total {r['m_total_tonnes']:.2f} t, "
                f"{r['kg_per_kw_useful']:.0f} kg/kW, "
                f"{r['fission_comparison']}"
            )


if __name__ == "__main__":
    main()
