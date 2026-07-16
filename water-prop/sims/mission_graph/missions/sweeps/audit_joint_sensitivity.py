"""Audit sweep: joint sensitivity to four parameters at once.

Tests assumptions A1 (water-electrothermal Isp), A4 (chunk water
fraction), A7 (Hohmann TSI delta-v), A11 (delivered floor) jointly.

Axes:
  - water_met_isp_s: (600, 700, 800, 900) s — A1, includes the cliff edge
  - chunk_water_fraction: (0.6, 0.8, 1.0) — A4
  - tsi_hohmann_dv_km_s: (6.5, 7.3, 8.0) km/s — A7

Fixed: vehicle 50 t (peak closure mass), chunk 200 t (only closing chunk),
power 100 kWe, electric thrust 5 N. 5 floor predicates computed
simultaneously (10/20/30/50/100 t).

Total cells: 4 x 3 x 3 = 36. ~1 minute runtime.

Goal: pin down which combinations of these four assumptions invert the
matrix verdict and which are robust to joint perturbation.
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
        "tsi_hohmann_dv_km_s": 7.3,
        "chunk_water_fraction": 1.0,
        "multi_falcon_launch_count": 6,
        "launch_epoch_jd": 0.0,
        "existing_leo_depot": False,
    }


def _scale_propellant(state, coords):
    return dataclasses.replace(state, propellant_kg=PROPELLANT_FRACTION * state.mass_kg)


PARAM_AXES = [
    SweepAxis(
        name="water_met_isp_s",
        values=(600.0, 700.0, 800.0, 900.0),
    ),
    SweepAxis(
        name="chunk_water_fraction",
        values=(0.6, 0.8, 1.0),
    ),
    SweepAxis(
        name="tsi_hohmann_dv_km_s",
        values=(6.5, 7.3, 8.0),
    ),
]


def main():
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = Path(__file__).resolve().parents[2] / "runs" / "audit_joint_sensitivity" / ts
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Running joint-sensitivity sweep: 4 x 3 x 3 = 36 cells")
    cells = sweep(
        saturn_water_v0,
        _base_state(),
        _base_params(),
        param_axes=PARAM_AXES,
        vehicle_axes=[],
        progress_every=5,
        state_transform=_scale_propellant,
    )
    print(f"Swept {len(cells)} cells")

    cells_path = out_dir / "cells.jsonl"
    save_cells_jsonl(cells, cells_path)
    print(f"Wrote {cells_path} ({cells_path.stat().st_size / (1024*1024):.1f} MB)")

    # Aggregate closure rates at each floor.
    print()
    print("=" * 60)
    print("Closure rate at each delivered-floor threshold:")
    print("=" * 60)
    predicates = [
        ("delivered_floor_10t", "10 t (demonstrator-class)"),
        ("delivered_floor_20t", "20 t (pre-commercial)"),
        ("delivered_floor", "30 t (sticky anchor)"),
        ("delivered_floor_50t", "50 t (above engineering ceiling)"),
        ("delivered_floor_100t", "100 t (annual demand at 1/yr)"),
    ]
    summary_lines = []
    summary_lines.append("# Joint sensitivity audit sweep — closure rate by floor")
    summary_lines.append("")
    summary_lines.append("Axes: water_met_isp_s (4) x chunk_water_fraction (3) x tsi_hohmann_dv_km_s (3) = 36 cells")
    summary_lines.append("Fixed: vehicle 50 t, chunk 200 t, power 100 kWe, electric thrust 5 N.")
    summary_lines.append("")
    summary_lines.append("## Closure rate at each delivered-floor threshold")
    summary_lines.append("")
    summary_lines.append("| floor | close / total feasible | rate |")
    summary_lines.append("|---|---:|---:|")
    for pred, label in predicates:
        close = 0
        total = 0
        for c in cells:
            for r in c.results:
                if r.is_feasible:
                    total += 1
                    if r.closure_verdicts.get(pred) == "close":
                        close += 1
        pct = 100.0 * close / total if total else 0
        line = f"| {label} | {close} / {total} | {pct:.1f}% |"
        summary_lines.append(line)
        print(f"  {label:>30}: {close:>5d} / {total:>5d} ({pct:.1f}%)")

    # 3D analysis: how does each parameter shift closure at 30-tonne floor?
    print()
    print("Marginal closure rate at 30-tonne floor for each parameter value:")
    print()
    summary_lines.append("")
    summary_lines.append("## Marginal closure at 30-tonne floor by parameter")
    summary_lines.append("")
    for axis_name in ("water_met_isp_s", "chunk_water_fraction", "tsi_hohmann_dv_km_s"):
        summary_lines.append(f"### {axis_name}")
        summary_lines.append("")
        per_value = {}
        for c in cells:
            v = c.coords.get(axis_name)
            if v is None:
                continue
            per_value.setdefault(v, [0, 0])
            for r in c.results:
                if r.is_feasible:
                    per_value[v][1] += 1
                    if r.closure_verdicts.get("delivered_floor") == "close":
                        per_value[v][0] += 1
        print(f"  axis: {axis_name}")
        for v in sorted(per_value.keys()):
            close, total = per_value[v]
            pct = 100.0 * close / total if total else 0
            print(f"    {v:>10}: {close:>4d} / {total:>4d} ({pct:.1f}%)")
            summary_lines.append(f"  - {v}: {close} / {total} ({pct:.1f}%)")
        summary_lines.append("")

    report_path = out_dir / "report.md"
    report_path.write_text("\n".join(summary_lines))
    print(f"\nWrote {report_path}")


if __name__ == "__main__":
    main()
