"""Audit sweep: smaller vehicle masses x water-MET specific impulse sensitivity.

Tests two assumptions from R_assumption_audit_2026_05_21:

  A1. Water-MET specific impulse = 800 s (load-bearing for Phase 4
      chunk_fed_spiral and Phase 7 lunar_processing_and_leo_transfer)
  A12. Vehicle mass grid is anchored to launcher capacities (50-200 t),
       not to vehicle physics minimums. Project owner question: "could
       we go with a much smaller spacecraft?"

Axes:
  - vehicle_mass_kg: (10, 20, 30, 50, 63, 100, 150, 200) tonnes — extended
    DOWN to 10 t to probe the demonstrator-mission corner. 8 values.
  - water_met_isp_s: (400, 500, 600, 700, 800, 900) seconds — A1
    sensitivity test. 6 values.
  - chunk_mass_kg: (5, 10, 25, 50, 100, 200) tonnes — extended DOWN to
    5 t to probe small demonstrator chunks. 6 values.

Fixed: power_kwe=100, electric_thrust_n=5.0 (mid-grid values).

Total cells: 8 x 6 x 6 = 288. ~5 minutes runtime.

Output:
  runs/audit_smaller_vehicle_water_met/<timestamp>/cells.jsonl
  runs/audit_smaller_vehicle_water_met/<timestamp>/report.md
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
from mission_graph.analysis.sweep_report import (  # noqa: E402
    architecture_cell_counts,
    back_propagate,
    floor_close_count,
    marginal_closure,
)
from mission_graph.analysis.cell_table import (  # noqa: E402
    format_2d_closure_table,
    format_architecture_ranking,
    format_back_propagation,
    format_headline,
    format_marginal_line,
    project_to_2d,
)
from mission_graph.missions.saturn_water_v0 import saturn_water_v0


PROPELLANT_FRACTION = 0.80


def _base_state() -> VehicleState:
    return VehicleState(
        mass_kg=50_000.0,
        propellant_kg=0.0,  # state_transform sets the real value per cell
        payload_kg=0.0,
        location="pre_launch",
        v_inf_km_s=0.0,
        time_elapsed_s=0.0,
        epoch_jd=None,
        power_available_kwe=100.0,
    )


def _base_params() -> dict:
    return {
        "chemical_isp_s": 340.0,
        "electric_isp_s": 3000.0,
        "electric_thrust_n": 5.0,
        "water_met_isp_s": 800.0,  # overridden by sweep axis
        "chunk_mass_kg": 50_000.0,  # overridden by sweep axis
        "multi_falcon_launch_count": 6,
        "launch_epoch_jd": 0.0,
        "existing_leo_depot": False,
    }


def _scale_propellant(state, coords):
    target_prop = PROPELLANT_FRACTION * state.mass_kg
    return dataclasses.replace(state, propellant_kg=target_prop)


VEHICLE_AXES = [
    VehicleAxis(
        name="vehicle_mass_kg",
        values=(10_000.0, 20_000.0, 30_000.0, 50_000.0, 63_000.0, 100_000.0, 150_000.0, 200_000.0),
        state_field="mass_kg",
    ),
]

PARAM_AXES = [
    SweepAxis(
        name="water_met_isp_s",
        values=(400.0, 500.0, 600.0, 700.0, 800.0, 900.0),
    ),
    SweepAxis(
        name="chunk_mass_kg",
        values=(5_000.0, 10_000.0, 25_000.0, 50_000.0, 100_000.0, 200_000.0),
    ),
]


def run_sweep() -> tuple:
    print(f"Running audit sweep: {len(VEHICLE_AXES) + len(PARAM_AXES)} axes, "
          f"{8 * 6 * 6} cells")
    cells = sweep(
        saturn_water_v0,
        _base_state(),
        _base_params(),
        param_axes=PARAM_AXES,
        vehicle_axes=VEHICLE_AXES,
        progress_every=50,
        state_transform=_scale_propellant,
    )
    print(f"Swept {len(cells)} cells")
    return cells


def build_report(cells: tuple) -> str:
    lines = []
    lines.append("# Audit sweep — smaller-vehicle + water-MET specific-impulse sensitivity")
    lines.append("")
    lines.append("Tests assumptions A1 and A12 from R_assumption_audit_2026_05_21.")
    lines.append("")
    lines.append(
        "Axes: vehicle_mass_kg (10-200 t, 8 values) x water_met_isp_s "
        "(400-900 s, 6 values) x chunk_mass_kg (5-200 t, 6 values). "
        "Power fixed at 100 kWe, electric thrust at 5 N."
    )
    lines.append("")

    floor = floor_close_count(cells, "delivered_floor")
    total_close = sum(nc for nc, _ in floor.values())
    total_results = sum(nt for _, nt in floor.values())
    lines.append("## headline")
    lines.append("")
    lines.append(format_headline(total_close, total_results, "delivered_floor (>=30 t at depot)"))
    lines.append("")

    vehicle_values = VEHICLE_AXES[0].values
    isp_values = PARAM_AXES[0].values
    chunk_values = PARAM_AXES[1].values

    # 2D projection: vehicle x water_met_isp_s
    table_vi = project_to_2d(cells, "vehicle_mass_kg", "water_met_isp_s", floor)
    lines.append("## 2D closure table: vehicle_mass_kg (row) x water_met_isp_s (col)")
    lines.append("")
    lines.append(format_2d_closure_table(
        table_vi, "vehicle_mass_kg", "water_met_isp_s",
        vehicle_values, isp_values,
    ))
    lines.append("")

    # 2D projection: chunk x water_met_isp_s
    table_ci = project_to_2d(cells, "chunk_mass_kg", "water_met_isp_s", floor)
    lines.append("## 2D closure table: chunk_mass_kg (row) x water_met_isp_s (col)")
    lines.append("")
    lines.append(format_2d_closure_table(
        table_ci, "chunk_mass_kg", "water_met_isp_s",
        chunk_values, isp_values,
    ))
    lines.append("")

    # 2D projection: vehicle x chunk
    table_vc = project_to_2d(cells, "vehicle_mass_kg", "chunk_mass_kg", floor)
    lines.append("## 2D closure table: vehicle_mass_kg (row) x chunk_mass_kg (col)")
    lines.append("")
    lines.append(format_2d_closure_table(
        table_vc, "vehicle_mass_kg", "chunk_mass_kg",
        vehicle_values, chunk_values,
    ))
    lines.append("")

    # Marginal closure per axis
    lines.append("## marginal closure on each axis (forward propagation)")
    lines.append("")
    for axis_name in ("vehicle_mass_kg", "water_met_isp_s", "chunk_mass_kg"):
        marg = marginal_closure(cells, axis_name, "delivered_floor")
        lines.append(format_marginal_line(marg, axis_name))
        lines.append("")

    # Back-propagation
    admitting = back_propagate(cells, "delivered_floor")
    lines.append(format_back_propagation(admitting))
    lines.append("")

    # Architecture ranking
    counts = architecture_cell_counts(cells)
    lines.append(format_architecture_ranking(counts, top_n=10))
    lines.append("")

    return "\n".join(lines)


def main():
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = Path(__file__).resolve().parents[2] / "runs" / "audit_smaller_vehicle_water_met" / ts
    out_dir.mkdir(parents=True, exist_ok=True)

    cells = run_sweep()

    cells_path = out_dir / "cells.jsonl"
    print(f"Writing {cells_path}")
    save_cells_jsonl(cells, cells_path)
    size_mb = cells_path.stat().st_size / (1024 * 1024)
    print(f"  {size_mb:.1f} MB")

    report = build_report(cells)
    report_path = out_dir / "report.md"
    report_path.write_text(report)
    print(f"Wrote {report_path}")

    # Echo headline.
    floor = floor_close_count(cells, "delivered_floor")
    total_close = sum(nc for nc, _ in floor.values())
    total_results = sum(nt for _, nt in floor.values())
    print()
    print(format_headline(total_close, total_results, "delivered_floor (>=30 t at depot)"))


if __name__ == "__main__":
    main()
