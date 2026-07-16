"""R-delivery-architecture — parametric Tsiolkovsky comparison.

Compares four inbound-delivery architectures for Project ICEBERG:
  A: whole-chunk-to-low-Earth-orbit via lunar gravity assist (status quo)
  B: chunk-to-lunar-distant-retrograde-orbit, cislunar tug shuttles to low Earth orbit
  C: streaming delivery (multiple small parcels)
  D: aerocapture or chunk-as-heat-shield (rescue path)

Pre-registered hypotheses are in STUDY.md alongside this file.

Run from the rhea worktree root:
    PYTHONPATH=water-prop/src python water-prop/rounds/R_delivery_architecture/run.py

Output: results/results.json (machine-readable) and results/tables.md (markdown).
Deterministic; no random seeds.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, asdict
from pathlib import Path


G0 = 9.81  # standard gravity, metres per second squared

# -----------------------------------------------------------------------------
# Tsiolkovsky helpers


def delivered_fraction(delta_v_m_per_s: float, isp_s: float) -> float:
    """Fraction of wet mass delivered as dry payload after a delta-v burn."""
    ve = isp_s * G0
    return math.exp(-delta_v_m_per_s / ve)


def propellant_fraction(delta_v_m_per_s: float, isp_s: float) -> float:
    """Fraction of wet mass spent as propellant."""
    return 1.0 - delivered_fraction(delta_v_m_per_s, isp_s)


# -----------------------------------------------------------------------------
# Architecture A: whole-chunk-to-low-Earth-orbit

# Deep-space inbound delta-velocity, Architecture A.
# Source: titan R-inbound-dv-continuous-thrust, sweep over Saturn-departure
# geometry. Three cases for sensitivity.
A_DELTA_V_IMPULSIVE = 6420.0       # matrix impulsive equivalent, metres per second
A_DELTA_V_CT_HIGH_ELLIPTICAL = 24700.0  # continuous-thrust, high-elliptical Saturn departure
A_DELTA_V_CT_B_RING = 40200.0      # continuous-thrust, B-ring direct Saturn departure


def architecture_a(chunk_t: float, isp_deep_space_s: float) -> dict:
    """Architecture A: whole-chunk-to-low-Earth-orbit. Three accounting cases."""
    cases = {}
    for label, dv in [
        ("impulsive_equivalent", A_DELTA_V_IMPULSIVE),
        ("ct_high_elliptical", A_DELTA_V_CT_HIGH_ELLIPTICAL),
        ("ct_b_ring", A_DELTA_V_CT_B_RING),
    ]:
        df = delivered_fraction(dv, isp_deep_space_s)
        cases[label] = {
            "delta_v_m_per_s": dv,
            "delivered_fraction": df,
            "delivered_tonnes": chunk_t * df,
            "delivery_orbit": "low Earth orbit",
        }
    return {
        "name": "A_whole_chunk_to_leo_via_lga",
        "chunk_t": chunk_t,
        "isp_deep_space_s": isp_deep_space_s,
        "cases": cases,
    }


# -----------------------------------------------------------------------------
# Architecture B: chunk-to-lunar-distant-retrograde-orbit, cislunar tug to LEO

# Deep-space inbound delta-velocity, Architecture B. Closer to impulsive
# because lunar-flyby insertion bypasses the LEO Edelbaum spiral.
B_DELTA_V_DEEP_SPACE = 4000.0  # Saturn-departure 1.5 + cruise braking 2.0 + lunar-flyby trim 0.5
B_DELTA_V_CISLUNAR_TUG = 3500.0  # lunar distant retrograde orbit to low Earth orbit, impulsive


def architecture_b(
    chunk_t: float,
    isp_deep_space_s: float,
    isp_tug_s: float,
) -> dict:
    """Architecture B: chunk to LDRO, cislunar tug shuttles to LEO."""
    df_deep_space = delivered_fraction(B_DELTA_V_DEEP_SPACE, isp_deep_space_s)
    delivered_to_ldro_t = chunk_t * df_deep_space

    df_cislunar = delivered_fraction(B_DELTA_V_CISLUNAR_TUG, isp_tug_s)
    delivered_to_leo_t = delivered_to_ldro_t * df_cislunar

    return {
        "name": "B_chunk_to_ldro_tug_to_leo",
        "chunk_t": chunk_t,
        "isp_deep_space_s": isp_deep_space_s,
        "isp_tug_s": isp_tug_s,
        "delta_v_deep_space_m_per_s": B_DELTA_V_DEEP_SPACE,
        "delta_v_tug_m_per_s": B_DELTA_V_CISLUNAR_TUG,
        "delivered_fraction_deep_space": df_deep_space,
        "delivered_to_ldro_t": delivered_to_ldro_t,
        "delivered_fraction_cislunar": df_cislunar,
        "delivered_to_leo_t": delivered_to_leo_t,
        "total_delivered_fraction": delivered_to_leo_t / chunk_t,
    }


# -----------------------------------------------------------------------------
# Architecture C: streaming delivery


def architecture_c(
    chunk_t: float,
    n_parcels: int,
    processing_hardware_t: float = 7.5,
    per_parcel_bus_overhead_frac: float = 0.10,
    per_parcel_arrival_dv_m_per_s: float = 2000.0,
    isp_parcel_s: float = 1500.0,
) -> dict:
    """Architecture C: in-cruise processing, multiple small parcels dispatched."""
    parcel_size_t = chunk_t / n_parcels
    per_parcel_bus_overhead_t = parcel_size_t * per_parcel_bus_overhead_frac
    per_parcel_payload_after_bus_t = parcel_size_t - per_parcel_bus_overhead_t

    # Per-parcel arrival propellant (chunk-fed from each parcel's own water)
    df_arrival = delivered_fraction(per_parcel_arrival_dv_m_per_s, isp_parcel_s)
    per_parcel_delivered_t = per_parcel_payload_after_bus_t * df_arrival

    total_per_parcel_overhead_t = n_parcels * per_parcel_bus_overhead_t
    total_delivered_t = n_parcels * per_parcel_delivered_t

    # The processing-hardware mass sits on the deep-space vehicle but does not
    # subtract from chunk delivered fraction directly; it shows up as outbound
    # launch-mass penalty. For this comparison, treat it as a fixed
    # subtractor from chunk (worst case for streaming).
    chunk_after_processing_hardware_t = max(chunk_t - processing_hardware_t, 0.0)

    # Scale the streaming output by the chunk-after-processing-hardware
    # fraction, so a smaller chunk sources fewer / smaller parcels.
    scale = chunk_after_processing_hardware_t / chunk_t if chunk_t > 0 else 0
    total_delivered_t_scaled = total_delivered_t * scale

    return {
        "name": "C_streaming",
        "chunk_t": chunk_t,
        "n_parcels": n_parcels,
        "parcel_size_t": parcel_size_t,
        "processing_hardware_t": processing_hardware_t,
        "per_parcel_bus_overhead_frac": per_parcel_bus_overhead_frac,
        "per_parcel_bus_overhead_t": per_parcel_bus_overhead_t,
        "per_parcel_arrival_dv_m_per_s": per_parcel_arrival_dv_m_per_s,
        "isp_parcel_s": isp_parcel_s,
        "per_parcel_delivered_t": per_parcel_delivered_t,
        "total_delivered_t_unscaled": total_delivered_t,
        "total_delivered_t": total_delivered_t_scaled,
        "total_delivered_fraction": total_delivered_t_scaled / chunk_t,
    }


# -----------------------------------------------------------------------------
# Architecture D: aerocapture or chunk-as-heat-shield (rescue path)

# Aerocapture reduces arrival propulsive delta-velocity to ~0.5 km/s for
# post-capture trim. Heat-shield mass fraction is ~3 percent of chunk at the
# ICEBERG scale per R-aerocapture (with the chunk-as-heat-shield variant
# bringing this to near zero but requiring chunk surface ablation ~1 percent).


def architecture_d(
    chunk_t: float,
    isp_deep_space_s: float,
    heat_shield_mass_fraction: float = 0.03,
    post_capture_dv_m_per_s: float = 500.0,
) -> dict:
    """Architecture D: aerocapture rescue. Conditional on thermal-protection breakthrough."""
    # Heat-shield mass is launched outbound; counts as a chunk-side overhead.
    chunk_after_shield_t = chunk_t * (1.0 - heat_shield_mass_fraction)
    # Post-capture propulsive trim chunk-fed at the deep-space vehicle's Isp.
    df_trim = delivered_fraction(post_capture_dv_m_per_s, isp_deep_space_s)
    delivered_t = chunk_after_shield_t * df_trim
    return {
        "name": "D_aerocapture_rescue",
        "chunk_t": chunk_t,
        "isp_deep_space_s": isp_deep_space_s,
        "heat_shield_mass_fraction": heat_shield_mass_fraction,
        "post_capture_dv_m_per_s": post_capture_dv_m_per_s,
        "delivered_fraction_trim": df_trim,
        "delivered_t": delivered_t,
        "total_delivered_fraction": delivered_t / chunk_t,
        "feasibility_note": (
            "Aerocapture at ICEBERG ballistic coefficient 4000 kg/m^2 has been "
            "established as off-near-term per R-chunk-as-heat-shield + "
            "R-deployable-drag-skirt. Architecture D numbers assume the "
            "thermal-protection-system breakthrough closes; otherwise the "
            "architecture does not exist."
        ),
    }


# -----------------------------------------------------------------------------
# Sweep


def main() -> dict:
    chunk_classes = [50.0, 100.0, 200.0, 500.0]
    isp_deep_space_classes = [1500.0, 2000.0, 5000.0]
    isp_tug_classes = [320.0, 380.0, 2000.0]

    architectures = {"A": [], "B": [], "C": [], "D": []}

    for chunk_t in chunk_classes:
        for isp_ds in isp_deep_space_classes:
            architectures["A"].append(architecture_a(chunk_t, isp_ds))
            for isp_tug in isp_tug_classes:
                architectures["B"].append(architecture_b(chunk_t, isp_ds, isp_tug))
            architectures["D"].append(architecture_d(chunk_t, isp_ds))
        # Streaming: use a representative deep-space isp of 1500 s for parcels
        # and sweep over parcel count.
        for n_parcels in [5, 10, 20]:
            architectures["C"].append(architecture_c(chunk_t, n_parcels))

    # Targeted demonstrator-class closure check at Kilopower-class power
    # (10 kW-e, specific impulse 2000 s), chunk = 50 t.
    chunk_50 = 50.0
    isp_2000 = 2000.0
    isp_tug_2000 = 2000.0
    closure = {
        "demonstrator_class_check": {
            "chunk_t": chunk_50,
            "isp_deep_space_s": isp_2000,
            "isp_tug_s": isp_tug_2000,
            "A_continuous_thrust": architecture_a(chunk_50, isp_2000)["cases"]["ct_high_elliptical"],
            "B": architecture_b(chunk_50, isp_2000, isp_tug_2000),
            "C": architecture_c(chunk_50, n_parcels=10),
            "D": architecture_d(chunk_50, isp_2000),
        }
    }

    return {"architectures": architectures, "closure": closure}


# -----------------------------------------------------------------------------
# Output


def write_outputs(result: dict, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / "results.json", "w") as f:
        json.dump(result, f, indent=2, sort_keys=True)

    # Markdown table
    lines = []
    lines.append("# R-delivery-architecture — results tables\n")
    lines.append("Generated by run.py. Do not edit by hand.\n")

    lines.append("## Demonstrator-class closure check (50 t chunk, Isp 2000 s)\n")
    lines.append("| Architecture | delta-v deep-space (km/s) | delivered to LEO (t) | delivered fraction |")
    lines.append("|---|---:|---:|---:|")
    closure = result["closure"]["demonstrator_class_check"]
    a_ct = closure["A_continuous_thrust"]
    lines.append(
        f"| A (continuous-thrust, high-elliptical) | "
        f"{a_ct['delta_v_m_per_s']/1000:.1f} | "
        f"{a_ct['delivered_tonnes']:.1f} | "
        f"{a_ct['delivered_fraction']*100:.1f}% |"
    )
    b = closure["B"]
    lines.append(
        f"| B (LDRO + cislunar tug, water-MET tug Isp 2000 s) | "
        f"{b['delta_v_deep_space_m_per_s']/1000:.1f} | "
        f"{b['delivered_to_leo_t']:.1f} | "
        f"{b['total_delivered_fraction']*100:.1f}% |"
    )
    c = closure["C"]
    lines.append(
        f"| C (streaming, 10 parcels, Isp 1500 s parcels) | "
        f"n/a (per-parcel 2 km/s) | "
        f"{c['total_delivered_t']:.1f} | "
        f"{c['total_delivered_fraction']*100:.1f}% |"
    )
    d = closure["D"]
    lines.append(
        f"| D (aerocapture rescue, 3% heat shield) | "
        f"{d['post_capture_dv_m_per_s']/1000:.1f} | "
        f"{d['delivered_t']:.1f} | "
        f"{d['total_delivered_fraction']*100:.1f}% |"
    )
    lines.append("")

    # Architecture B with cislunar-tug-class sweep
    lines.append("## Architecture B — cislunar tug propulsion class sweep (50 t chunk, deep-space Isp 2000 s)\n")
    lines.append("| Tug class | tug Isp (s) | tug delta-v (km/s) | delivered to LEO (t) | total delivered fraction |")
    lines.append("|---|---:|---:|---:|---:|")
    for entry in result["architectures"]["B"]:
        if entry["chunk_t"] == 50.0 and entry["isp_deep_space_s"] == 2000.0:
            isp_tug = entry["isp_tug_s"]
            tug_class = {320: "hypergolic", 380: "methalox", 2000: "water-MET/electric"}[int(isp_tug)]
            lines.append(
                f"| {tug_class} | {int(isp_tug)} | "
                f"{entry['delta_v_tug_m_per_s']/1000:.1f} | "
                f"{entry['delivered_to_leo_t']:.1f} | "
                f"{entry['total_delivered_fraction']*100:.1f}% |"
            )
    lines.append("")

    # Architecture A all three accounting cases at the demonstrator chunk
    lines.append("## Architecture A — three accounting cases (50 t chunk, Isp 2000 s)\n")
    lines.append("| Accounting | delta-v (km/s) | delivered (t) | delivered fraction |")
    lines.append("|---|---:|---:|---:|")
    for entry in result["architectures"]["A"]:
        if entry["chunk_t"] == 50.0 and entry["isp_deep_space_s"] == 2000.0:
            for label, case in entry["cases"].items():
                lines.append(
                    f"| {label} | {case['delta_v_m_per_s']/1000:.2f} | "
                    f"{case['delivered_tonnes']:.1f} | "
                    f"{case['delivered_fraction']*100:.1f}% |"
                )
    lines.append("")

    # Architecture C streaming sweep
    lines.append("## Architecture C — streaming parcel-count sweep (50 t chunk)\n")
    lines.append("| n_parcels | parcel size (t) | per-parcel delivered (t) | total delivered (t) | total delivered fraction |")
    lines.append("|---|---:|---:|---:|---:|")
    for entry in result["architectures"]["C"]:
        if entry["chunk_t"] == 50.0:
            lines.append(
                f"| {entry['n_parcels']} | "
                f"{entry['parcel_size_t']:.1f} | "
                f"{entry['per_parcel_delivered_t']:.1f} | "
                f"{entry['total_delivered_t']:.1f} | "
                f"{entry['total_delivered_fraction']*100:.1f}% |"
            )
    lines.append("")

    # Chunk-class scan (deep-space Isp 2000 s, tug Isp 2000 s)
    lines.append("## Chunk-class scan: A continuous-thrust vs B water-MET tug vs D aerocapture\n")
    lines.append("All at deep-space Isp 2000 s; B at tug Isp 2000 s; D at 3% heat shield.\n")
    lines.append("| chunk (t) | A_CT_high_elliptical (t) | A_CT_b_ring (t) | B (t) | D (t) |")
    lines.append("|---:|---:|---:|---:|---:|")
    for chunk_t in [50.0, 100.0, 200.0, 500.0]:
        a_he = None
        a_br = None
        b_v = None
        d_v = None
        for entry in result["architectures"]["A"]:
            if entry["chunk_t"] == chunk_t and entry["isp_deep_space_s"] == 2000.0:
                a_he = entry["cases"]["ct_high_elliptical"]["delivered_tonnes"]
                a_br = entry["cases"]["ct_b_ring"]["delivered_tonnes"]
        for entry in result["architectures"]["B"]:
            if entry["chunk_t"] == chunk_t and entry["isp_deep_space_s"] == 2000.0 and entry["isp_tug_s"] == 2000.0:
                b_v = entry["delivered_to_leo_t"]
        for entry in result["architectures"]["D"]:
            if entry["chunk_t"] == chunk_t and entry["isp_deep_space_s"] == 2000.0:
                d_v = entry["delivered_t"]
        lines.append(f"| {chunk_t:.0f} | {a_he:.1f} | {a_br:.1f} | {b_v:.1f} | {d_v:.1f} |")
    lines.append("")

    with open(out_dir / "tables.md", "w") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    result = main()
    out_dir = Path(__file__).resolve().parent / "results"
    write_outputs(result, out_dir)
    print(f"wrote {out_dir}/results.json and {out_dir}/tables.md")
    closure = result["closure"]["demonstrator_class_check"]
    a_ct = closure["A_continuous_thrust"]
    b = closure["B"]
    print(f"\nDemonstrator-class closure check (50 t chunk, Isp 2000 s):")
    print(f"  A (continuous-thrust, high-elliptical): delivered {a_ct['delivered_tonnes']:.1f} t "
          f"({a_ct['delivered_fraction']*100:.1f}%)")
    print(f"  B (LDRO + water-MET cislunar tug): delivered {b['delivered_to_leo_t']:.1f} t "
          f"({b['total_delivered_fraction']*100:.1f}%)")
    print(f"  Ratio B/A: {b['delivered_to_leo_t'] / a_ct['delivered_tonnes']:.2f}x")
