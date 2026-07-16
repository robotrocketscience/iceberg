"""A14 audit: Phase 3 capture-efficiency sensitivity.

The framework hardcodes:
  SINGLE_PASS_CAPTURE_EFFICIENCY = 0.85
  DRIFT_CAPTURE_EFFICIENCY = 0.65
  FG_GAP_CAPTURE_EFFICIENCY = 0.85
  B_RING_RAW_YIELD_MULTIPLIER * B_RING_SURVIVAL_PROBABILITY = 0.01

These are desk-study anchors. A bottoms-up engineering decomposition
(rendezvous + deploy + catch + contain + survive) gives joint success
~30-50 percent — much lower than the 0.85 anchors.

Test: sweep a capture_efficiency_multiplier that scales all anchors
together. Multiplier values:
  0.25 = pessimistic engineering decomposition (~22 percent net)
  0.50 = moderate (~42 percent net)
  0.75 = optimistic (~64 percent net)
  1.00 = current desk-study anchor (~85 percent net)

Axes:
  - vehicle_mass_kg: (50, 100) tonnes (single-launch capable)
  - chunk_mass_kg: (100, 200) tonnes
  - water_met_isp_s: (700, 800, 900) seconds (the cliff band)
  - capture_efficiency_multiplier: (0.25, 0.50, 0.75, 1.00)

Total: 2 x 2 x 3 x 4 = 48 cells. All 5 floor predicates evaluated.
"""

from __future__ import annotations

import dataclasses
import sys
from datetime import datetime, timezone
from pathlib import Path


def _ensure_import_path():
    here = Path(__file__).resolve()
    sims_dir = here.parents[3]
    if str(sims_dir) not in sys.path:
        sys.path.insert(0, str(sims_dir))


_ensure_import_path()


from mission_graph.framework import (  # noqa: E402
    SweepAxis,
    VehicleAxis,
    VehicleState,
    save_cells_jsonl,
    sweep,
)
from mission_graph.missions.saturn_water_v0 import saturn_water_v0


PROPELLANT_FRACTION = 0.80


def _base_state() -> VehicleState:
    return VehicleState(
        mass_kg=50_000.0, propellant_kg=0.0, payload_kg=0.0,
        location="pre_launch", v_inf_km_s=0.0, time_elapsed_s=0.0,
        epoch_jd=None, power_available_kwe=100.0,
    )


def _base_params() -> dict:
    return {
        "chemical_isp_s": 340.0,
        "electric_isp_s": 3000.0,
        "electric_thrust_n": 5.0,
        "water_met_isp_s": 800.0,
        "chunk_mass_kg": 200_000.0,
        "capture_efficiency_multiplier": 1.0,
        "multi_falcon_launch_count": 6,
        "launch_epoch_jd": 0.0,
        "existing_leo_depot": False,
    }


def _scale_propellant(state, coords):
    return dataclasses.replace(state, propellant_kg=PROPELLANT_FRACTION * state.mass_kg)


VEHICLE_AXES = [
    VehicleAxis(
        name="vehicle_mass_kg",
        values=(50_000.0, 100_000.0),
        state_field="mass_kg",
    ),
]

PARAM_AXES = [
    SweepAxis(name="chunk_mass_kg", values=(100_000.0, 200_000.0)),
    SweepAxis(name="water_met_isp_s", values=(700.0, 800.0, 900.0)),
    SweepAxis(name="capture_efficiency_multiplier", values=(0.25, 0.50, 0.75, 1.00)),
]


def main():
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = Path(__file__).resolve().parents[2] / "runs" / "audit_capture_efficiency" / ts
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Running A14 capture-efficiency audit: 2 x 2 x 3 x 4 = 48 cells")
    cells = sweep(
        saturn_water_v0,
        _base_state(),
        _base_params(),
        param_axes=PARAM_AXES,
        vehicle_axes=VEHICLE_AXES,
        progress_every=10,
        state_transform=_scale_propellant,
    )
    print(f"Swept {len(cells)} cells")

    cells_path = out_dir / "cells.jsonl"
    save_cells_jsonl(cells, cells_path)

    # Aggregate closure rates at each floor x capture efficiency.
    predicates = [
        ("delivered_floor_10t", "10 t"),
        ("delivered_floor_20t", "20 t"),
        ("delivered_floor", "30 t"),
        ("delivered_floor_50t", "50 t"),
    ]
    eff_values = (0.25, 0.50, 0.75, 1.00)

    lines = []
    lines.append("# A14 audit — capture-efficiency sensitivity")
    lines.append("")
    lines.append("The framework's Phase 3 capture-efficiency anchors (0.85 for single-pass,")
    lines.append("0.65 for drift-through) are desk-study upper bounds. Engineering")
    lines.append("decomposition (rendezvous + deploy + catch + contain + survive) suggests")
    lines.append("joint success of ~30-50 percent — significantly lower.")
    lines.append("")
    lines.append("This sweep scales all Phase 3 efficiency anchors by a multiplier and")
    lines.append("observes the closure-surface shift.")
    lines.append("")
    lines.append("## Closure rate by floor x capture-efficiency-multiplier")
    lines.append("")
    lines.append("| floor | mult=0.25 | mult=0.50 | mult=0.75 | mult=1.00 |")
    lines.append("|---|---:|---:|---:|---:|")
    for pred, label in predicates:
        row = [f"| {label} |"]
        for eff in eff_values:
            close = 0
            total = 0
            for c in cells:
                if abs(c.coords.get("capture_efficiency_multiplier", 0) - eff) > 0.01:
                    continue
                for r in c.results:
                    if r.is_feasible:
                        total += 1
                        if r.closure_verdicts.get(pred) == "close":
                            close += 1
            pct = 100.0 * close / total if total else 0
            row.append(f" {pct:.1f}% ({close}/{total}) |")
        lines.append("".join(row))
    lines.append("")

    # Best delivered tonnage at each multiplier.
    lines.append("## Maximum delivered tonnage at each capture-efficiency multiplier")
    lines.append("")
    lines.append("| multiplier | best delivered (t) | round-trip (yr) |")
    lines.append("|---:|---:|---:|")
    for eff in eff_values:
        best = 0.0
        best_yr = 0.0
        for c in cells:
            if abs(c.coords.get("capture_efficiency_multiplier", 0) - eff) > 0.01:
                continue
            for r in c.results:
                if r.is_feasible and r.leaf_state.location == "LEO_depot":
                    if r.leaf_state.payload_kg > best:
                        best = r.leaf_state.payload_kg
                        best_yr = r.leaf_state.time_elapsed_s / (365.25 * 86_400)
        lines.append(f"| {eff} | {best/1000:.1f} | {best_yr:.2f} |")
    lines.append("")

    report_path = out_dir / "report.md"
    report_path.write_text("\n".join(lines))
    print(f"\nWrote {report_path}")
    print()
    for line in lines[5:]:
        print(line)


if __name__ == "__main__":
    main()
