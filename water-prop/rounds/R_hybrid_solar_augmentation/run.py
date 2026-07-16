"""R-hybrid-solar-augmentation — reactor plus deployable solar array.

Closed-form harmonic-mean calculation of trajectory-time-averaged power for
a hybrid reactor-plus-solar power bus along an Edelbaum circular-to-circular
spiral between Earth (1 astronomical unit) and Saturn (9.58 astronomical units).

Pre-registered hypotheses in water-prop/HYPOTHESES.md and STUDY.md alongside.
Deterministic; no random seeds. Outputs tables to results/.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

RESULTS_DIR = Path(__file__).parent / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# Trajectory bounds (astronomical units).
R_EARTH_AU = 1.0
R_SATURN_AU = 9.58

# Grid for trajectory integration.
N_GRID = 1000
R_GRID = np.linspace(R_EARTH_AU, R_SATURN_AU, N_GRID)

# Trajectory weighting per Edelbaum: time-spent-per-radial-bin proportional to
# r-to-the-negative-one-and-a-half divided by local power. The numerator below
# is the "time density per unit power."
TIME_DENSITY = R_GRID ** -1.5

# Solar array model.
ARRAY_POWER_PER_M2_AT_1AU = 300.0  # watts per square meter, Roll-Out Solar Array class
ARRAY_AREAL_DENSITY_KG_PER_M2_DEFAULT = 3.0  # current Roll-Out Solar Array


def low_intensity_low_temperature_derate(r_au: np.ndarray) -> np.ndarray:
    """Linear derate from 1.0 at 1 astronomical unit to 0.79 at 9.58 astronomical units.

    Anchored on Juno mission data at 5.2 astronomical units (derate ~0.88) and
    extrapolated linearly to Saturn distance. Conservative compared with
    Lucy mission's measured performance.
    """
    return 1.0 - 0.025 * (r_au - 1.0)


def array_power_at_r(area_m2: float, r_au: np.ndarray) -> np.ndarray:
    """Array power in kilowatts-electric at heliocentric distance r."""
    irradiance_ratio = 1.0 / (r_au ** 2)
    derate = low_intensity_low_temperature_derate(r_au)
    return area_m2 * ARRAY_POWER_PER_M2_AT_1AU * irradiance_ratio * derate / 1000.0


def time_averaged_power_kwe(reactor_kwe: float, array_area_m2: float) -> float:
    """Harmonic mean of P(r) weighted by trajectory time density.

    Returns the trajectory-time-averaged effective power in kilowatts-electric.
    """
    p_total_kwe = reactor_kwe + array_power_at_r(array_area_m2, R_GRID)
    weight = TIME_DENSITY
    # Harmonic-mean weighted average: sum(weight) divided by sum(weight divided by P).
    return float(np.sum(weight) / np.sum(weight / p_total_kwe))


def chunk_mass_tonnes_for_power(power_kwe: float) -> float:
    """Conops heuristic: 1 kilowatt-electric supports ~25 tonnes of delivered chunk."""
    return 25.0 * power_kwe


def main() -> None:
    # Sweep 1: reactor power class with fixed 200-square-meter array.
    reactor_classes_kwe = [1.0, 3.0, 10.0, 30.0, 100.0, 300.0, 1000.0]
    array_area_m2 = 200.0
    array_power_at_1au_kwe = (
        array_area_m2 * ARRAY_POWER_PER_M2_AT_1AU / 1000.0
    )  # ~60 kilowatts-electric

    sweep_reactor = []
    for r_kwe in reactor_classes_kwe:
        p_reactor_only = r_kwe
        p_hybrid = time_averaged_power_kwe(r_kwe, array_area_m2)
        gain_factor = p_hybrid / p_reactor_only
        sweep_reactor.append(
            {
                "reactor_kwe": r_kwe,
                "p_reactor_only_kwe": p_reactor_only,
                "p_hybrid_time_averaged_kwe": p_hybrid,
                "gain_factor": gain_factor,
            }
        )

    # Sweep 2: where does hybrid gain factor cross 1.5? (sub-claim H-hsa-d)
    r_fine_kwe = np.geomspace(1.0, 1000.0, 200)
    gain_curve = [
        time_averaged_power_kwe(float(r), array_area_m2) / float(r) for r in r_fine_kwe
    ]
    threshold_idx = next(
        (i for i, g in enumerate(gain_curve) if g < 1.5), len(gain_curve) - 1
    )
    reactor_class_at_gain_1p5_threshold = float(r_fine_kwe[threshold_idx])

    # Sub-claim H-hsa-e: net chunk-mass deliverable gain at 10-kilowatt-electric
    # Kilopower plus 200-square-meter array, subtracting array dry-mass penalty.
    reactor_kwe_eval = 10.0
    p_reactor_only = reactor_kwe_eval
    p_hybrid = time_averaged_power_kwe(reactor_kwe_eval, array_area_m2)
    chunk_reactor_only_t = chunk_mass_tonnes_for_power(p_reactor_only)
    chunk_hybrid_gross_t = chunk_mass_tonnes_for_power(p_hybrid)
    array_mass_kg = array_area_m2 * ARRAY_AREAL_DENSITY_KG_PER_M2_DEFAULT
    array_mass_t = array_mass_kg / 1000.0
    chunk_hybrid_net_t = chunk_hybrid_gross_t - array_mass_t
    chunk_gain_pct = (chunk_hybrid_net_t - chunk_reactor_only_t) / chunk_reactor_only_t * 100.0

    # Sub-claim H-hsa-f: areal density break-even. Find the kilograms-per-square-meter
    # at which hybrid loses to a slightly larger pure reactor at the same total
    # power-subsystem mass.
    # Reactor specific power assumed at Kilopower mid-band: 5 watts-per-kilogram.
    reactor_specific_power_w_per_kg = 5.0
    reactor_subsystem_mass_kg = reactor_kwe_eval * 1000.0 / reactor_specific_power_w_per_kg

    breakeven_density_kg_per_m2 = None
    for density in np.linspace(1.0, 30.0, 300):
        array_mass = array_area_m2 * density
        total_power_subsystem_mass = reactor_subsystem_mass_kg + array_mass
        # Alternative: spend all mass on bigger reactor.
        alt_reactor_kwe = total_power_subsystem_mass * reactor_specific_power_w_per_kg / 1000.0
        p_hybrid_at_density = time_averaged_power_kwe(reactor_kwe_eval, array_area_m2)
        p_alt = alt_reactor_kwe
        if p_alt > p_hybrid_at_density:
            breakeven_density_kg_per_m2 = float(density)
            break

    # Sub-claim H-hsa-g: concentrated-burn case at 1.2 astronomical units.
    r_burn_au = 1.2
    array_power_at_burn = array_area_m2 * ARRAY_POWER_PER_M2_AT_1AU * (1.0 / r_burn_au ** 2) * low_intensity_low_temperature_derate(np.array([r_burn_au]))[0] / 1000.0
    p_reactor_at_burn = 10.0
    p_hybrid_at_burn = p_reactor_at_burn + array_power_at_burn
    concentrated_burn_gain = p_hybrid_at_burn / p_reactor_at_burn

    # Compile pre-registration grading.
    h_hsa_a = next(x for x in sweep_reactor if x["reactor_kwe"] == 10.0)["gain_factor"]
    h_hsa_b = next(x for x in sweep_reactor if x["reactor_kwe"] == 100.0)["gain_factor"]
    h_hsa_c = next(x for x in sweep_reactor if x["reactor_kwe"] == 1000.0)["gain_factor"]
    h_hsa_d = reactor_class_at_gain_1p5_threshold
    h_hsa_e = chunk_gain_pct
    h_hsa_f = breakeven_density_kg_per_m2 if breakeven_density_kg_per_m2 is not None else float("inf")
    h_hsa_g = concentrated_burn_gain

    pre_reg = {
        "H-hsa-a": (h_hsa_a, 1.5, 2.2),
        "H-hsa-b": (h_hsa_b, 1.05, 1.20),
        "H-hsa-c": (h_hsa_c, 1.00, 1.02),
        "H-hsa-d": (h_hsa_d, 15.0, 40.0),
        "H-hsa-e": (h_hsa_e, 25.0, 55.0),
        "H-hsa-f": (h_hsa_f, 6.0, 15.0),
        "H-hsa-g": (h_hsa_g, 4.0, 6.5),
    }

    summary = {
        "trajectory": {
            "r_min_au": R_EARTH_AU,
            "r_max_au": R_SATURN_AU,
            "n_grid": N_GRID,
            "weighting": "time_density_proportional_to_r_to_the_minus_one_and_a_half",
            "harmonic_mean_interpretation": "P_avg_time = sum(weight) / sum(weight / P)",
        },
        "solar_array": {
            "power_per_m2_at_1au_w": ARRAY_POWER_PER_M2_AT_1AU,
            "areal_density_kg_per_m2_default": ARRAY_AREAL_DENSITY_KG_PER_M2_DEFAULT,
            "lilt_derate": "linear_1p0_at_1au_to_0p79_at_9p58au",
        },
        "fixed_array_size_m2": array_area_m2,
        "fixed_array_power_at_1au_kwe": array_power_at_1au_kwe,
        "sweep_reactor": sweep_reactor,
        "chunk_mass_at_10kwe_kilopower": {
            "p_reactor_only_kwe": p_reactor_only,
            "p_hybrid_time_averaged_kwe": p_hybrid,
            "chunk_reactor_only_tonnes": chunk_reactor_only_t,
            "chunk_hybrid_gross_tonnes": chunk_hybrid_gross_t,
            "array_mass_tonnes": array_mass_t,
            "chunk_hybrid_net_tonnes": chunk_hybrid_net_t,
            "chunk_gain_percent": chunk_gain_pct,
        },
        "concentrated_burn_at_1p2au": {
            "r_au": r_burn_au,
            "array_power_at_burn_kwe": array_power_at_burn,
            "p_reactor_at_burn_kwe": p_reactor_at_burn,
            "p_hybrid_at_burn_kwe": p_hybrid_at_burn,
            "gain_factor": concentrated_burn_gain,
        },
        "hypothesis_grading": {
            name: {
                "measured": float(meas),
                "lo": float(lo),
                "hi": float(hi),
                "held": bool(lo <= meas <= hi),
            }
            for name, (meas, lo, hi) in pre_reg.items()
        },
    }

    out_path = RESULTS_DIR / "R_hybrid_solar_augmentation_summary.json"
    out_path.write_text(json.dumps(summary, indent=2))
    print(f"wrote {out_path}")

    print("\nReactor-power sweep (200-square-meter array, 60-kilowatt-electric at 1 astronomical unit):")
    print(f"{'reactor_kWe':>12} {'P_only':>10} {'P_hybrid':>10} {'gain':>8}")
    for row in sweep_reactor:
        print(
            f"{row['reactor_kwe']:>12.1f} "
            f"{row['p_reactor_only_kwe']:>10.2f} "
            f"{row['p_hybrid_time_averaged_kwe']:>10.2f} "
            f"{row['gain_factor']:>8.3f}"
        )

    print("\nPre-registration grading:")
    print(f"{'claim':<10} {'measured':>12} {'lo':>10} {'hi':>10} {'held?':>10}")
    for name, (meas, lo, hi) in pre_reg.items():
        held = lo <= meas <= hi
        marker = "HELD" if held else "FALSIFIED"
        print(f"{name:<10} {meas:>12.4g} {lo:>10.3g} {hi:>10.3g} {marker:>10}")


if __name__ == "__main__":
    main()
