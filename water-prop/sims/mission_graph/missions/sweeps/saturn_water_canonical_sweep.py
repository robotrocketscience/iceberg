"""Canonical 4-axis sweep over saturn_water_v0.

Axes (5 + 6 + 5 + 5 = 750 cells):
  - vehicle_mass_kg  (VehicleState.mass_kg field; 5 values)
  - power_kwe        (VehicleState.power_available_kwe field; 6 named tech-path
                      classes — see POWER_CLASS_REGISTRY)
  - chunk_mass_kg    (params dict; 5 values)
  - electric_thrust_n (params dict; 5 values)

Outputs:
  runs/<timestamp>/cells.jsonl   (one record per cell, lean schema)
  runs/<timestamp>/report.md     (markdown summary tables)
  runs/<timestamp>/summary.txt   (one-line headlines)

Run from project root:
  uv run python water-prop/sims/mission_graph/missions/sweeps/saturn_water_canonical_sweep.py
"""

from __future__ import annotations

import dataclasses
import sys
from datetime import datetime, timezone
from pathlib import Path


def _ensure_import_path():
    here = Path(__file__).resolve()
    sims_dir = here.parents[3]  # sims/
    if str(sims_dir) not in sys.path:
        sys.path.insert(0, str(sims_dir))


_ensure_import_path()


from mission_graph.framework import (  # noqa: E402
    SweepAxis,
    VehicleAxis,
    VehicleState,
    emit_phase_tree_markdown,
    emit_reachable_phase_tree_markdown,
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
from mission_graph.missions.saturn_water_v0 import saturn_water_v0  # noqa: E402


PROPELLANT_FRACTION = 0.80


# Maps effective_avg_kwe (the float used as the sweep axis value) to a label
# and the (reactor_kwe, solar_panel_leo_kwe) breakdown. Imported by the
# Streamlit dashboard for human-readable display of which tech-path class
# a cell corresponds to. See the power_kwe VehicleAxis docstring below for
# the half-trip-average derivation.
POWER_CLASS_REGISTRY: dict = {
    1.0:  {"label": "K1",      "reactor_kwe": 1.0,  "solar_leo_kwe": 0.0,  "type": "pure"},
    10.0: {"label": "K10",     "reactor_kwe": 10.0, "solar_leo_kwe": 0.0,  "type": "pure"},
    30.0: {"label": "K30",     "reactor_kwe": 30.0, "solar_leo_kwe": 0.0,  "type": "pure"},
    11.0: {"label": "K1+S20",  "reactor_kwe": 1.0,  "solar_leo_kwe": 20.0, "type": "hybrid"},
    20.0: {"label": "K10+S20", "reactor_kwe": 10.0, "solar_leo_kwe": 20.0, "type": "hybrid"},
    55.0: {"label": "K30+S50", "reactor_kwe": 30.0, "solar_leo_kwe": 50.0, "type": "hybrid"},
}


def _base_state() -> VehicleState:
    """Mid-of-grid starting state. Vehicle axes override mass_kg and
    power_available_kwe. The state_transform below derives propellant_kg
    from the per-cell mass_kg so the propellant fraction stays at
    PROPELLANT_FRACTION across the whole mass axis."""
    return VehicleState(
        mass_kg=100_000.0,
        propellant_kg=0.0,  # set to 0 so VehicleState validation never trips
                            # on mass_kg override < base propellant_kg.
                            # _scale_propellant sets the real value per cell.
        payload_kg=0.0,
        location="pre_launch",
        v_inf_km_s=0.0,
        time_elapsed_s=0.0,
        epoch_jd=None,
        power_available_kwe=30.0,
    )


def _scale_propellant(state: VehicleState, coords: dict) -> VehicleState:
    """Set propellant_kg = PROPELLANT_FRACTION * vehicle_mass_kg per cell."""
    import dataclasses as _dc
    target_prop = PROPELLANT_FRACTION * state.mass_kg
    return _dc.replace(state, propellant_kg=target_prop)


def _base_params() -> dict:
    return {
        "chemical_isp_s": 340.0,
        "electric_isp_s": 3000.0,
        "electric_thrust_n": 5.0,
        "water_met_isp_s": 800.0,
        "chunk_mass_kg": 50_000.0,
        "multi_falcon_launch_count": 6,
        "launch_epoch_jd": 0.0,
    }


VEHICLE_AXES = [
    VehicleAxis(
        name="vehicle_mass_kg",
        # Anchored to launcher capacities to low-Earth orbit:
        #   50 t  ~ one Falcon Heavy partial-reuse
        #   63 t  ~ one Falcon Heavy fully expendable
        #   100 t ~ one Starship (advertised lower bound)
        #   150 t ~ one Starship (advertised upper bound) / 3x Falcon Heavy partial
        #   200 t ~ 4x Falcon Heavy partial / 2x Starship
        values=(50_000.0, 63_000.0, 100_000.0, 150_000.0, 200_000.0),
        state_field="mass_kg",
    ),
    VehicleAxis(
        name="power_kwe",
        # Effective average power-at-thrust across the round-trip.
        # Six named technology-path classes per locked-memory directive
        # (Kilopower-class at best; megawatt retired 2026-05-19 latest+13).
        # Three pure-reactor classes + three hybrid (reactor + solar) classes.
        #
        # Hybrid classes assume reactor + 0.5 x LEO-equivalent-solar averaged
        # across the round-trip — half-time near Saturn (0.011 x solar at 9.5 AU)
        # and half-time on inbound (~1.0 x solar at Earth approach). The hybrid
        # story matters most on the inbound leg where trajectory refinement and
        # lunar-gravity-assist setup need extra thrust authority; the reactor
        # provides baseline at Saturn departure.
        #
        # POWER_CLASS_REGISTRY (effective_avg_kwe -> reactor_kwe + solar_panel_leo_kwe):
        #    1.0 = K1     - Kilopower 1 kWe (KRUSTY flown anchor)
        #   10.0 = K10    - Kilopower 10 kWe (titan-3 R-kilowatt-class envelope)
        #   30.0 = K30    - Kilopower 30 kWe (titan-3 closure cell; matrix decision #14 audit-pending)
        #   11.0 = K1+S20 - K1 + 20-kW-LEO-equivalent solar (half-trip avg ~= 1 + 0.5*20 = 11)
        #   20.0 = K10+S20 - K10 + 20-kW-LEO solar (10 + 0.5*20 = 20)
        #   55.0 = K30+S50 - K30 + 50-kW-LEO solar (30 + 0.5*50 = 55)
        #
        # Retired megawatt-class values (100, 300, 1000) are NOT in this axis
        # per project-owner directive 2026-05-19 ("a 500 kilowatt reactor is
        # not going to happen; stop accounting for it").
        #
        # Full hybrid modeling — where effective power varies with heliocentric
        # distance per phase rather than being a flat round-trip average —
        # requires R-solar-thermal-hybrid-power framework extension (separate
        # SCOPE in Open SCOPEs queue).
        values=(1.0, 10.0, 11.0, 20.0, 30.0, 55.0),
        state_field="power_available_kwe",
    ),
]

PARAM_AXES = [
    SweepAxis(
        name="chunk_mass_kg",
        values=(10_000.0, 25_000.0, 50_000.0, 100_000.0, 200_000.0),
    ),
    SweepAxis(
        name="electric_thrust_n",
        values=(1.0, 2.5, 5.0, 10.0, 25.0),
    ),
]


def run_sweep() -> tuple:
    total_cells = 1
    for ax in VEHICLE_AXES + PARAM_AXES:
        total_cells *= len(ax.values)
    print(f"Running 4-axis canonical sweep: {len(VEHICLE_AXES) + len(PARAM_AXES)} axes, "
          f"{total_cells} cells")
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
    """Produce the markdown summary."""
    lines = []
    lines.append("# saturn_water_v0 canonical sweep report")
    lines.append("")
    lines.append("Generated by `missions/sweeps/saturn_water_canonical_sweep.py`")
    lines.append("")

    # Phase tree — reachable option-to-option edges from the union of
    # multiple probes. Different starting conditions expose different
    # reachable options:
    #   - 50 t vehicle exposes falcon_heavy_expended (max 63 t to LEO)
    #   - 150 t vehicle with low-thrust spiral exposes Phase 1 low_thrust
    #   - 90 t / 80%-propellant exposes generic mid-grid behavior
    #   - 200 t / 89%-propellant chemical Hohmann exposes ballistic-arrival
    #     (v_inf ~5.44 km/s) which is the gate for moon gravity assists at
    #     Phase 2 and Jupiter / Venus gravity assists at Phase 1b.
    # Union them so the diagram shows every option reachable from *some*
    # plausible starting condition.
    probe_small_lowthrust = _scale_propellant(
        dataclasses.replace(_base_state(), mass_kg=50_000.0),
        coords={"vehicle_mass_kg": 50_000.0},
    )
    probe_large_lowthrust = _scale_propellant(
        dataclasses.replace(_base_state(), mass_kg=150_000.0, power_available_kwe=300.0),
        coords={"vehicle_mass_kg": 150_000.0},
    )
    probe_mid = _scale_propellant(
        dataclasses.replace(_base_state(), mass_kg=90_000.0),
        coords={"vehicle_mass_kg": 90_000.0},
    )
    # Bypass _scale_propellant for the chemical-Hohmann probe: chemical
    # Hohmann at 7.3 km/s and 340 s specific impulse needs ~89 percent
    # propellant fraction. 80 percent (the sweep default) is too low.
    probe_chemical = dataclasses.replace(
        _base_state(), mass_kg=200_000.0, propellant_kg=178_000.0,
    )
    probes = (probe_small_lowthrust, probe_large_lowthrust, probe_mid, probe_chemical)
    probe_params = {**_base_params(), "chunk_mass_kg": 200_000.0, "existing_leo_depot": True}
    lines.append("## phase tree — reachable option-to-option edges (union of probes)")
    lines.append("")
    lines.append(
        "Only transitions where the downstream option's precondition "
        "passes after the upstream option's executor runs. Union of three "
        "probes: 50-tonne low-thrust, 150-tonne high-power low-thrust, "
        "90-tonne chemical Hohmann. Surfaces every option reachable from "
        "*some* plausible starting condition."
    )
    lines.append("")
    lines.append(emit_reachable_phase_tree_markdown(saturn_water_v0, probes, probe_params, direction="LR"))
    lines.append("")

    lines.append("## phase tree — structural (every phase x every option)")
    lines.append("")
    lines.append(
        "Ignores preconditions. Useful as an option catalog; misleading if "
        "read as a connectivity diagram."
    )
    lines.append("")
    lines.append(emit_phase_tree_markdown(saturn_water_v0))
    lines.append("")

    # Per-cell delivered-floor closure counts.
    floor = floor_close_count(cells, "delivered_floor")
    total_close = sum(nc for nc, _ in floor.values())
    total_results = sum(nt for _, nt in floor.values())
    lines.append("## headline")
    lines.append("")
    lines.append(format_headline(total_close, total_results, "delivered_floor (>=30 t at depot)"))
    lines.append("")
    skipped = [c for c in cells if c.skipped_reason is not None]
    if skipped:
        lines.append(f"Skipped {len(skipped)} cells due to invalid VehicleState overrides.")
        lines.append("")

    # 2D projections of closure rate.
    chunk_values = [a.values for a in PARAM_AXES if a.name == "chunk_mass_kg"][0]
    power_values = [a.values for a in VEHICLE_AXES if a.name == "power_kwe"][0]
    mass_values = [a.values for a in VEHICLE_AXES if a.name == "vehicle_mass_kg"][0]
    thrust_values = [a.values for a in PARAM_AXES if a.name == "electric_thrust_n"][0]

    table_cp = project_to_2d(cells, "chunk_mass_kg", "power_kwe", floor)
    lines.append("## 2D closure table: chunk_mass_kg (row) x power_kwe (col)")
    lines.append("")
    lines.append(format_2d_closure_table(table_cp, "chunk_mass_kg", "power_kwe",
                                          chunk_values, power_values))
    lines.append("")

    table_ct = project_to_2d(cells, "chunk_mass_kg", "electric_thrust_n", floor)
    lines.append("## 2D closure table: chunk_mass_kg (row) x electric_thrust_n (col)")
    lines.append("")
    lines.append(format_2d_closure_table(table_ct, "chunk_mass_kg", "electric_thrust_n",
                                          chunk_values, thrust_values))
    lines.append("")

    table_mc = project_to_2d(cells, "vehicle_mass_kg", "chunk_mass_kg", floor)
    lines.append("## 2D closure table: vehicle_mass_kg (row) x chunk_mass_kg (col)")
    lines.append("")
    lines.append(format_2d_closure_table(table_mc, "vehicle_mass_kg", "chunk_mass_kg",
                                          mass_values, chunk_values))
    lines.append("")

    # Marginal closure on each axis.
    lines.append("## marginal closure on each axis (forward propagation)")
    lines.append("")
    for axis_name in ("vehicle_mass_kg", "power_kwe", "chunk_mass_kg", "electric_thrust_n"):
        marg = marginal_closure(cells, axis_name, "delivered_floor")
        lines.append(format_marginal_line(marg, axis_name))
        lines.append("")

    # Back propagation: which axis values admit any closing cell.
    admitting = back_propagate(cells, "delivered_floor")
    lines.append(format_back_propagation(admitting))
    lines.append("")

    # Architecture ranking.
    counts = architecture_cell_counts(cells)
    lines.append(format_architecture_ranking(counts, top_n=10))
    lines.append("")

    return "\n".join(lines)


def main():
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = Path(__file__).resolve().parents[2] / "runs" / ts
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

    # Also emit a standalone phase-tree.md with both views. Use the same
    # union-of-probes pattern as the inline report for the reachable
    # section so single-launcher and multi-launcher architectures both
    # surface in the diagram.
    probe_small = _scale_propellant(
        dataclasses.replace(_base_state(), mass_kg=50_000.0),
        coords={"vehicle_mass_kg": 50_000.0},
    )
    probe_large = _scale_propellant(
        dataclasses.replace(_base_state(), mass_kg=150_000.0, power_available_kwe=300.0),
        coords={"vehicle_mass_kg": 150_000.0},
    )
    probe_mid = _scale_propellant(
        dataclasses.replace(_base_state(), mass_kg=90_000.0),
        coords={"vehicle_mass_kg": 90_000.0},
    )
    probes = (probe_small, probe_large, probe_mid)
    probe_params = {**_base_params(), "chunk_mass_kg": 200_000.0, "existing_leo_depot": True}
    tree_path = out_dir / "phase-tree.md"
    tree_path.write_text(
        "# saturn_water_v0 phase tree\n\n"
        "## reachable (union of three probes: 50 t low-thrust, 150 t high-power low-thrust, 90 t chemical)\n\n"
        + emit_reachable_phase_tree_markdown(saturn_water_v0, probes, probe_params, direction="LR")
        + "\n\n## structural (every phase x every option)\n\n"
        + emit_phase_tree_markdown(saturn_water_v0)
        + "\n"
    )
    print(f"Wrote {tree_path}")

    # Echo headline to stdout for fast feedback.
    floor = floor_close_count(cells, "delivered_floor")
    total_close = sum(nc for nc, _ in floor.values())
    total_results = sum(nt for _, nt in floor.values())
    print()
    print(format_headline(total_close, total_results, "delivered_floor (>=30 t at depot)"))


if __name__ == "__main__":
    main()
