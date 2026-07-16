"""R-saturn-shadow-and-station-location — duty-cycle and storage model.

Replaces round-1's flat 1.5x duty-cycle hack with a station-location-specific
shadow model plus a thermal-storage mass term to bridge dark periods.
Reuses round-1's solar-thermal stack model.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROUND_1 = Path(__file__).resolve().parent.parent / "R_saturn_side_solar_thermal"
sys.path.insert(0, str(ROUND_1))
from run import stack_mass  # noqa: E402  - sibling module import by design

THERMAL_STORAGE_WH_PER_KG = 100.0  # latent-heat phase-change, conservative

# Station-location definitions
# f_dark: time-average fraction in darkness
# t_dark_h: longest continuous dark interval in hours
STATIONS = {
    "saturn_sun_L1_halo": {
        "f_dark": 0.0,
        "t_dark_h": 0.0,
        "conops_plausible": True,
        "note": "continuous sunlight; chunk-delivery cost from rings not modeled here",
    },
    "high_eccentric_saturn_orbit": {
        "f_dark": 0.03,
        "t_dark_h": 4.0,
        "conops_plausible": True,
        "note": "periapsis at rings, apoapsis far out; Saturn shadow brief per orbit",
    },
    "low_equatorial_saturn_orbit": {
        "f_dark": 0.40,
        "t_dark_h": 2.5,
        "conops_plausible": True,
        "note": "near rings; Saturn shadow ~40% of each ~10-h orbit",
    },
    "titan_surface": {
        "f_dark": 0.50,
        "t_dark_h": 192.0,
        "conops_plausible": True,
        "note": "tidally locked; 8 days dark each 15.95-day cycle",
    },
    "enceladus_surface": {
        "f_dark": 0.50,
        "t_dark_h": 16.4,
        "conops_plausible": True,
        "note": "tidally locked; 16.4 h dark each 1.37-day cycle",
    },
}

# Useful electrolysis target
TARGET_KW_USEFUL = 200.0

# Round-1 optimistic stack parameters
OPTIMISTIC = dict(
    mirror_areal_density_kg_per_m2=0.1,
    conversion_path="soec",
    optical_efficiency=0.80,
    structure_overhead_factor=1.0,
)


def with_shadow(station_name: str, station: dict) -> dict:
    """Compute total mass for a station, including shadow + storage penalty."""
    f_dark = station["f_dark"]
    t_dark_h = station["t_dark_h"]

    # Duty-cycle factor: to deliver time-averaged P_useful, collection during
    # sunlit periods must supply (1 / (1 - f_dark)) * P_useful AND recharge
    # storage. Simplification: collection during sunlit periods covers both
    # instantaneous demand and storage charge; the storage capacity sets the
    # peak instantaneous discharge. We use the standard duty-cycle bump on
    # collection area:
    duty_cycle_factor = 1.0 / (1.0 - f_dark) if f_dark < 1.0 else float("inf")

    base = stack_mass(
        target_kw_useful=TARGET_KW_USEFUL,
        duty_cycle_factor=duty_cycle_factor,
        **OPTIMISTIC,
    )

    # Thermal storage to bridge the longest dark period at the useful power
    # rate. Energy stored = TARGET_KW_USEFUL * t_dark_h (in kWh). Mass at
    # THERMAL_STORAGE_WH_PER_KG = 100 Wh/kg = 0.1 kWh/kg.
    storage_kwh = TARGET_KW_USEFUL * t_dark_h
    m_storage_kg = storage_kwh / (THERMAL_STORAGE_WH_PER_KG / 1000.0)

    total_kg = base["m_total_kg"] + m_storage_kg
    return {
        "station": station_name,
        "conops_plausible": station["conops_plausible"],
        "note": station["note"],
        "f_dark": f_dark,
        "t_dark_h": t_dark_h,
        "duty_cycle_factor": duty_cycle_factor,
        "base_total_kg": base["m_total_kg"],
        "storage_kwh": storage_kwh,
        "m_storage_kg": m_storage_kg,
        "total_kg": total_kg,
        "total_tonnes": total_kg / 1000.0,
        "kg_per_kw_useful": total_kg / TARGET_KW_USEFUL,
        "mirror_area_m2": base["a_mirror_m2"],
    }


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


def main() -> None:
    out_dir = Path(__file__).resolve().parent / "results"
    out_dir.mkdir(parents=True, exist_ok=True)

    rows = []
    for name, st in STATIONS.items():
        r = with_shadow(name, st)
        r["fission_comparison"] = classify(r["kg_per_kw_useful"])
        rows.append(r)

    payload = {
        "target_kw_useful": TARGET_KW_USEFUL,
        "thermal_storage_Wh_per_kg": THERMAL_STORAGE_WH_PER_KG,
        "fission_benchmarks_kg_per_kw": FISSION_BENCHMARKS_KG_PER_KW,
        "results": rows,
    }
    (out_dir / "station_locations.json").write_text(json.dumps(payload, indent=2))

    lines = [
        "| station | f_dark | t_dark_h | duty | storage_t | total_t | kg/kW | vs_fission | conops |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        lines.append(
            "| {s} | {fd:.2f} | {td:.1f} | {duty:.2f} | {ms:.1f} | {tt:.1f} | {kk:.0f} | {fc} | {cp} |".format(
                s=r["station"],
                fd=r["f_dark"],
                td=r["t_dark_h"],
                duty=r["duty_cycle_factor"],
                ms=r["m_storage_kg"] / 1000.0,
                tt=r["total_tonnes"],
                kk=r["kg_per_kw_useful"],
                fc=r["fission_comparison"],
                cp="yes" if r["conops_plausible"] else "no",
            )
        )

    (out_dir / "tables.md").write_text(
        "# R-saturn-shadow-and-station-location — results\n\n"
        f"Target useful electrolysis output: {TARGET_KW_USEFUL} kW.\n"
        f"Thermal-storage specific energy: {THERMAL_STORAGE_WH_PER_KG} Wh/kg "
        "(latent-heat phase-change material, conservative — laboratory salts achieve 200–400 Wh/kg).\n\n"
        f"Fission benchmarks (kg/kW): {FISSION_BENCHMARKS_KG_PER_KW}\n\n"
        + "\n".join(lines)
        + "\n"
    )

    print(f"Wrote {len(rows)} stations to {out_dir}/tables.md")
    print()
    print("Summary:")
    for r in rows:
        print(
            f"  {r['station']:35s}: {r['total_tonnes']:7.1f} t total, "
            f"{r['kg_per_kw_useful']:6.0f} kg/kW, {r['fission_comparison']}"
        )


if __name__ == "__main__":
    main()
