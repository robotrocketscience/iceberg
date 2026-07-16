"""Audit sweep: low-thrust spiral delta-v sensitivity (A2).

Test A2 from R_assumption_audit_2026_05_21. The framework anchors Phase 1
low_thrust_spiral on LOW_THRUST_TOTAL_DV_KM_S = 13.0 km/s. Edelbaum
analytical lower bound for pure low-thrust LEO -> Saturn approach is
~28 km/s; published Glenn Research Center designs land in 18-25 km/s.

This sweep tests the closure surface across a range of low-thrust
delta-v values: 13 (anchor), 18, 22, 25, 28 km/s.

Other axes minimal to keep cell count low:
  - vehicle_mass_kg: (10, 30, 50, 100) t
  - chunk_mass_kg: (50, 100, 200) t (the only chunk sizes that close)
  - low_thrust_total_dv_km_s: (13, 18, 22, 25, 28) km/s

Fixed: power=100 kWe, electric thrust=5 N, water-MET specific impulse=800 s.

Total cells: 4 x 3 x 5 = 60. ~1 minute runtime.
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
    floor_close_count,
    marginal_closure,
)
from mission_graph.analysis.cell_table import (  # noqa: E402
    format_2d_closure_table,
    format_headline,
    format_marginal_line,
    project_to_2d,
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
        "low_thrust_total_dv_km_s": 13.0,
        "multi_falcon_launch_count": 6,
        "launch_epoch_jd": 0.0,
        "existing_leo_depot": False,
    }


def _scale_propellant(state, coords):
    return dataclasses.replace(state, propellant_kg=PROPELLANT_FRACTION * state.mass_kg)


VEHICLE_AXES = [
    VehicleAxis(
        name="vehicle_mass_kg",
        values=(10_000.0, 30_000.0, 50_000.0, 100_000.0),
        state_field="mass_kg",
    ),
]

PARAM_AXES = [
    SweepAxis(
        name="chunk_mass_kg",
        values=(50_000.0, 100_000.0, 200_000.0),
    ),
    SweepAxis(
        name="low_thrust_total_dv_km_s",
        values=(13.0, 18.0, 22.0, 25.0, 28.0),
    ),
]


def main():
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = Path(__file__).resolve().parents[2] / "runs" / "audit_low_thrust_delta_v" / ts
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Running A2 audit sweep: 4 x 3 x 5 = 60 cells")
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
    size_mb = cells_path.stat().st_size / (1024 * 1024)
    print(f"Wrote {cells_path} ({size_mb:.1f} MB)")

    floor = floor_close_count(cells, "delivered_floor")
    total_close = sum(nc for nc, _ in floor.values())
    total_results = sum(nt for _, nt in floor.values())

    lines = []
    lines.append("# A2 audit — low-thrust spiral delta-v sensitivity")
    lines.append("")
    lines.append("Framework anchor: LOW_THRUST_TOTAL_DV_KM_S = 13.0 km/s.")
    lines.append("Edelbaum bound: ~28 km/s. Glenn Research Center realistic: 18-25 km/s.")
    lines.append("")
    lines.append(format_headline(total_close, total_results, "delivered_floor (>=30 t at depot)"))
    lines.append("")

    dv_values = PARAM_AXES[1].values
    vehicle_values = VEHICLE_AXES[0].values
    chunk_values = PARAM_AXES[0].values

    # 2D: vehicle x dv
    table_vd = project_to_2d(cells, "vehicle_mass_kg", "low_thrust_total_dv_km_s", floor)
    lines.append("## 2D closure table: vehicle_mass_kg (row) x low_thrust_total_dv_km_s (col)")
    lines.append("")
    lines.append(format_2d_closure_table(
        table_vd, "vehicle_mass_kg", "low_thrust_total_dv_km_s",
        vehicle_values, dv_values,
    ))
    lines.append("")

    # 2D: chunk x dv
    table_cd = project_to_2d(cells, "chunk_mass_kg", "low_thrust_total_dv_km_s", floor)
    lines.append("## 2D closure table: chunk_mass_kg (row) x low_thrust_total_dv_km_s (col)")
    lines.append("")
    lines.append(format_2d_closure_table(
        table_cd, "chunk_mass_kg", "low_thrust_total_dv_km_s",
        chunk_values, dv_values,
    ))
    lines.append("")

    lines.append("## marginal closure on low_thrust_total_dv_km_s")
    lines.append("")
    marg = marginal_closure(cells, "low_thrust_total_dv_km_s", "delivered_floor")
    lines.append(format_marginal_line(marg, "low_thrust_total_dv_km_s"))
    lines.append("")

    report = "\n".join(lines)
    report_path = out_dir / "report.md"
    report_path.write_text(report)
    print(f"Wrote {report_path}")
    print()
    print(format_headline(total_close, total_results, "delivered_floor"))


if __name__ == "__main__":
    main()
