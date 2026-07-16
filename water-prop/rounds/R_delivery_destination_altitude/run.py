"""R-delivery-destination-altitude — integrated continuous-thrust delta-velocity
versus destination altitude.

Tests whether titan's continuous-thrust inbound penalty (24.7 to 40.2
kilometres per second to low Earth orbit) is destination-conditional. If
the chunk is delivered to a higher-altitude staging orbit within L0-02's
admitted range (up to geostationary at 35,786 km altitude), the Edelbaum
spiral terminates at lower circular-velocity altitude and the integrated
penalty drops.

Run from the rhea worktree:
    python water-prop/rounds/R_delivery_destination_altitude/run.py

Deterministic; no random seeds.
"""

from __future__ import annotations

import json
import math
from pathlib import Path


G0 = 9.81  # standard gravity, metres per second squared
MU_EARTH_KM3_S2 = 3.986e5  # Earth gravitational parameter, km^3/s^2
R_EARTH_KM = 6378.0  # equatorial radius


def v_circular_km_per_s(orbital_radius_km: float) -> float:
    return math.sqrt(MU_EARTH_KM3_S2 / orbital_radius_km)


def v_hyperbolic_km_per_s(orbital_radius_km: float, v_inf_km_per_s: float) -> float:
    """Hyperbolic velocity at a given orbital radius for arrival v_inf."""
    v_esc_sq = 2.0 * MU_EARTH_KM3_S2 / orbital_radius_km
    return math.sqrt(v_inf_km_per_s ** 2 + v_esc_sq)


def delivered_fraction(delta_v_km_per_s: float, isp_s: float) -> float:
    ve_km_per_s = isp_s * G0 / 1000.0
    return math.exp(-delta_v_km_per_s / ve_km_per_s)


# -----------------------------------------------------------------------------
# Destination orbits


DESTINATIONS = {
    "LEO_300km": {"altitude_km": 300.0, "label": "Low Earth orbit (300 km altitude)"},
    "MEO_8000km": {"altitude_km": 8000.0, "label": "Medium Earth orbit (8000 km altitude)"},
    "MEO_20000km": {"altitude_km": 20000.0, "label": "Medium Earth orbit (20000 km altitude)"},
    "GEO": {"altitude_km": 35786.0, "label": "Geostationary (35786 km altitude)"},
}


def evaluate_destination(
    altitude_km: float,
    v_inf_km_per_s: float = 3.0,
    pre_destination_chunk_fed_dv_km_per_s: float = 3.5,
    isp_deep_space_s: float = 2000.0,
    chunk_t: float = 50.0,
) -> dict:
    """Compute delta-velocity components and delivered mass for one destination.

    Pre-destination chunk-fed delta-velocity (Saturn departure + cruise
    braking) is shared across destinations at 3.5 km/s. The destination-
    dependent components are:
      - Impulsive capture from v_inf into high-elliptical orbit at the
        destination altitude (one-burn periapsis-raise).
      - Continuous-thrust Edelbaum spiral from high-elliptical down to
        circular at the destination altitude.

    Returns a dict with delta-velocity breakdown and delivered mass.
    """
    orbital_radius_km = R_EARTH_KM + altitude_km
    v_circ_km_per_s = v_circular_km_per_s(orbital_radius_km)
    v_hyp_km_per_s = v_hyperbolic_km_per_s(orbital_radius_km, v_inf_km_per_s)

    # Impulsive capture into a high-elliptical orbit whose periapsis is at
    # the destination altitude. Pay the hyperbolic-to-elliptical velocity
    # difference; approximate by capturing into a stable orbit with
    # apoapsis at twice the destination altitude (eccentricity ~0.33). A
    # tighter capture is possible if there is a downstream circularisation
    # step that can absorb the higher eccentricity.
    e_capture = 0.33
    a_capture_km = orbital_radius_km / (1.0 - e_capture)
    v_peri_capture_km_per_s = math.sqrt(MU_EARTH_KM3_S2 * (2.0 / orbital_radius_km - 1.0 / a_capture_km))
    capture_dv_km_per_s = v_hyp_km_per_s - v_peri_capture_km_per_s

    # Continuous-thrust Edelbaum from the captured elliptical to circular
    # at the destination altitude. Approximate as the velocity difference
    # between the captured-orbit periapsis velocity and the final circular
    # velocity (this is the Edelbaum integrated delta-velocity for
    # circularisation at constant inclination).
    edelbaum_dv_km_per_s = abs(v_peri_capture_km_per_s - v_circ_km_per_s)

    # Total destination-dependent chunk-fed delta-velocity.
    destination_chunk_fed_dv_km_per_s = capture_dv_km_per_s + edelbaum_dv_km_per_s

    # Plus the destination-independent share (Saturn departure + cruise
    # braking).
    total_chunk_fed_dv_km_per_s = pre_destination_chunk_fed_dv_km_per_s + destination_chunk_fed_dv_km_per_s

    # Tsiolkovsky.
    df = delivered_fraction(total_chunk_fed_dv_km_per_s, isp_deep_space_s)
    delivered_t = chunk_t * df

    return {
        "altitude_km": altitude_km,
        "orbital_radius_km": orbital_radius_km,
        "v_circular_km_per_s": v_circ_km_per_s,
        "v_hyperbolic_at_destination_km_per_s": v_hyp_km_per_s,
        "v_inf_km_per_s": v_inf_km_per_s,
        "capture_dv_km_per_s": capture_dv_km_per_s,
        "edelbaum_circularisation_dv_km_per_s": edelbaum_dv_km_per_s,
        "destination_chunk_fed_dv_km_per_s": destination_chunk_fed_dv_km_per_s,
        "pre_destination_chunk_fed_dv_km_per_s": pre_destination_chunk_fed_dv_km_per_s,
        "total_chunk_fed_dv_km_per_s": total_chunk_fed_dv_km_per_s,
        "isp_deep_space_s": isp_deep_space_s,
        "chunk_t": chunk_t,
        "delivered_fraction": df,
        "delivered_t": delivered_t,
    }


def main() -> dict:
    base_chunk_t = 50.0
    base_isp_s = 2000.0
    base_v_inf_km_per_s = 3.0  # after lunar-gravity-assist tour

    results = {}
    for key, info in DESTINATIONS.items():
        results[key] = {
            "label": info["label"],
            "result": evaluate_destination(
                altitude_km=info["altitude_km"],
                v_inf_km_per_s=base_v_inf_km_per_s,
                isp_deep_space_s=base_isp_s,
                chunk_t=base_chunk_t,
            ),
        }

    # Sensitivity sweep on residual v_inf after LGA
    sensitivity = {}
    for v_inf in [1.0, 3.0, 6.0]:
        sensitivity[f"v_inf_{v_inf}_km_per_s"] = {
            key: evaluate_destination(
                altitude_km=info["altitude_km"],
                v_inf_km_per_s=v_inf,
                isp_deep_space_s=base_isp_s,
                chunk_t=base_chunk_t,
            )
            for key, info in DESTINATIONS.items()
        }

    return {
        "base_case": {
            "chunk_t": base_chunk_t,
            "isp_deep_space_s": base_isp_s,
            "v_inf_post_lga_km_per_s": base_v_inf_km_per_s,
            "pre_destination_chunk_fed_dv_km_per_s": 3.5,
            "destinations": results,
        },
        "sensitivity_v_inf": sensitivity,
    }


def write_outputs(result: dict, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / "results.json", "w") as f:
        json.dump(result, f, indent=2, sort_keys=True)

    lines = []
    lines.append("# R-delivery-destination-altitude — results tables\n")
    lines.append("Generated by run.py. Do not edit by hand.\n")

    lines.append("## Base case (50 t chunk, Isp 2000 s, v_inf 3 km/s post-LGA)\n")
    lines.append("| Destination | altitude (km) | v_circ (km/s) | capture dv (km/s) | Edelbaum dv (km/s) | total chunk-fed dv (km/s) | delivered (t) | delivered fraction |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|")
    for key, entry in result["base_case"]["destinations"].items():
        r = entry["result"]
        lines.append(
            f"| {entry['label']} | {r['altitude_km']:.0f} | "
            f"{r['v_circular_km_per_s']:.2f} | {r['capture_dv_km_per_s']:.2f} | "
            f"{r['edelbaum_circularisation_dv_km_per_s']:.2f} | "
            f"{r['total_chunk_fed_dv_km_per_s']:.2f} | "
            f"{r['delivered_t']:.1f} | "
            f"{r['delivered_fraction']*100:.1f}% |"
        )
    lines.append("")

    lines.append("## Sensitivity on residual v_inf after lunar-gravity-assist tour\n")
    lines.append("All at 50 t chunk, Isp 2000 s.\n")
    lines.append("| Destination | v_inf 1 km/s | v_inf 3 km/s | v_inf 6 km/s |")
    lines.append("|---|---:|---:|---:|")
    for key, info in DESTINATIONS.items():
        v1 = result["sensitivity_v_inf"]["v_inf_1.0_km_per_s"][key]["delivered_t"]
        v3 = result["sensitivity_v_inf"]["v_inf_3.0_km_per_s"][key]["delivered_t"]
        v6 = result["sensitivity_v_inf"]["v_inf_6.0_km_per_s"][key]["delivered_t"]
        lines.append(f"| {info['label']} | {v1:.1f} t | {v3:.1f} t | {v6:.1f} t |")
    lines.append("")

    with open(out_dir / "tables.md", "w") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    result = main()
    out_dir = Path(__file__).resolve().parent / "results"
    write_outputs(result, out_dir)
    print(f"wrote {out_dir}/results.json and {out_dir}/tables.md")
    print()
    print("Base case (50 t chunk, Isp 2000 s, v_inf 3 km/s post-LGA):")
    for key, entry in result["base_case"]["destinations"].items():
        r = entry["result"]
        print(
            f"  {entry['label']:55s} dv={r['total_chunk_fed_dv_km_per_s']:5.2f} km/s "
            f"delivered={r['delivered_t']:5.1f} t ({r['delivered_fraction']*100:5.1f}%)"
        )
