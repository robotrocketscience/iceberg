"""Closed-loop closure sweep over saturn_water_v1 (R-vehicle-mass-closure-refactor).

The open-loop canonical sweep (saturn_water_canonical_sweep.py) treats
`vehicle_mass_kg` as a swept boundary condition. This harness drops that axis:
per cell the vehicle dry mass is DERIVED from subsystem demands
(derive_saturn_vehicle), the launch wet mass + propellant follow from the 0.80
propellant convention, and non-convergent cells are tagged and cannot close.

Axes (1 vehicle + 2 param = 6 * 5 * 5 = 150 cells, vs the open-loop 750):
  - power_kwe          (VehicleState.power_available_kwe; 6 named tech-path classes)
  - chunk_mass_kg      (params; 5 values)
  - electric_thrust_n  (params; 5 values)

The harness also runs the matched open-loop baseline (v0, vehicle_mass swept) so
the BACK_TEST can report "% of open-loop closers that survive closed-loop". The
matched comparison holds constraint settings fixed and varies ONLY mass
derivation, isolating the mass-consistency effect (load-bearing H4).

Run from project root:
  python water-prop/sims/mission_graph/missions/sweeps/saturn_water_v1_closure_sweep.py

Outputs land in runs/<timestamp>/ (jsonl is NOT committed; see project rules).
"""

from __future__ import annotations

import sys
from pathlib import Path


def _ensure_import_path():
    here = Path(__file__).resolve()
    sims_dir = here.parents[3]  # sims/
    if str(sims_dir) not in sys.path:
        sys.path.insert(0, str(sims_dir))


_ensure_import_path()


from mission_graph.framework import SweepAxis, VehicleAxis, VehicleState, sweep  # noqa: E402
from mission_graph.missions.saturn_water_v0 import saturn_water_v0  # noqa: E402
from mission_graph.missions.saturn_water_v1 import (  # noqa: E402
    saturn_water_v1,
    make_derived_mass_transform,
    context_from_coords,
)
from mission_graph.missions.saturn_mass_demands import derive_saturn_vehicle  # noqa: E402


PROPELLANT_FRACTION = 0.80

# Power-class axis shared with the open-loop canonical sweep (six named classes).
POWER_VALUES = (1.0, 10.0, 11.0, 20.0, 30.0, 55.0)
CHUNK_VALUES = (10_000.0, 25_000.0, 50_000.0, 100_000.0, 200_000.0)
THRUST_VALUES = (1.0, 2.5, 5.0, 10.0, 25.0)

# Open-loop vehicle-mass axis (wet), used ONLY for the matched baseline.
OPEN_LOOP_VEHICLE_MASS_VALUES = (50_000.0, 63_000.0, 100_000.0, 150_000.0, 200_000.0)


def base_params() -> dict:
    return {
        "chemical_isp_s": 340.0,
        "electric_isp_s": 3000.0,
        "electric_thrust_n": 5.0,
        "water_met_isp_s": 800.0,
        "chunk_mass_kg": 50_000.0,
        "multi_falcon_launch_count": 6,
        "launch_epoch_jd": 0.0,
    }


def _base_state() -> VehicleState:
    # mass_kg here is a placeholder; the derived-mass transform overrides it.
    return VehicleState(
        mass_kg=50_000.0,
        propellant_kg=0.0,
        payload_kg=0.0,
        location="pre_launch",
        v_inf_km_s=0.0,
        time_elapsed_s=0.0,
        epoch_jd=None,
        power_available_kwe=30.0,
    )


CLOSED_LOOP_VEHICLE_AXES = [
    VehicleAxis(name="power_kwe", values=POWER_VALUES, state_field="power_available_kwe"),
]
PARAM_AXES = [
    SweepAxis(name="chunk_mass_kg", values=CHUNK_VALUES),
    SweepAxis(name="electric_thrust_n", values=THRUST_VALUES),
]


def run_closed_loop(extra_params: dict | None = None):
    """Closed-loop sweep: derived dry mass, vehicle_mass axis dropped."""
    bp = base_params()
    if extra_params:
        bp.update(extra_params)
    transform = make_derived_mass_transform(bp)
    return sweep(
        saturn_water_v1,
        _base_state(),
        bp,
        param_axes=PARAM_AXES,
        vehicle_axes=CLOSED_LOOP_VEHICLE_AXES,
        state_transform=transform,
    )


def _scale_propellant(state: VehicleState, coords: dict) -> VehicleState:
    import dataclasses as _dc
    return _dc.replace(state, propellant_kg=PROPELLANT_FRACTION * state.mass_kg)


def run_open_loop(extra_params: dict | None = None):
    """Matched open-loop baseline: vehicle_mass swept (v0), same param axes."""
    bp = base_params()
    if extra_params:
        bp.update(extra_params)
    open_loop_vehicle_axes = [
        VehicleAxis(name="vehicle_mass_kg", values=OPEN_LOOP_VEHICLE_MASS_VALUES, state_field="mass_kg"),
        VehicleAxis(name="power_kwe", values=POWER_VALUES, state_field="power_available_kwe"),
    ]
    return sweep(
        saturn_water_v0,
        _base_state(),
        bp,
        param_axes=PARAM_AXES,
        vehicle_axes=open_loop_vehicle_axes,
        state_transform=_scale_propellant,
    )


def cell_closes(cell, predicate_name="delivered_floor") -> bool:
    """Did any path in this cell close under the named predicate?"""
    if cell.skipped_reason is not None:
        return False
    for r in cell.results:
        if r.is_feasible and r.closure_verdicts.get(predicate_name) in ("close", "close_strict", "close_waiver"):
            return True
    return False


def closure_count(cells, predicate_name="delivered_floor") -> int:
    return sum(1 for c in cells if cell_closes(c, predicate_name))


def derivations_table(extra_params: dict | None = None):
    """Per (power, chunk) derived dry mass + convergence, for report tables.

    Independent of electric_thrust_n at first-pass anchors (structure's thrust
    term is negligible), so reported on the power x chunk grid.
    """
    bp = base_params()
    if extra_params:
        bp.update(extra_params)
    rows = []
    for power in POWER_VALUES:
        for chunk in CHUNK_VALUES:
            coords = {"power_kwe": power, "chunk_mass_kg": chunk, "electric_thrust_n": 5.0}
            ctx = context_from_coords(coords, bp)
            r = derive_saturn_vehicle(ctx)
            rows.append({
                "power_kwe": power,
                "chunk_t": chunk / 1000.0,
                "dry_t": r.dry_mass_kg / 1000.0,
                "wet_t": (r.dry_mass_kg / (1.0 - ctx.propellant_fraction)) / 1000.0,
                "converged": r.converged,
            })
    return rows


def main():
    print("=== closed-loop (derived mass) ===")
    cl = run_closed_loop()
    print(f"cells: {len(cl)}  delivered_floor closers: {closure_count(cl)}")
    print(f"  10t closers: {closure_count(cl, 'delivered_floor_10t')}")
    print(f"  arrived_at_depot: {closure_count(cl, 'arrived_at_depot')}")
    print("=== open-loop baseline (swept mass) ===")
    ol = run_open_loop()
    print(f"cells: {len(ol)}  delivered_floor closers: {closure_count(ol)}")
    print(f"  10t closers: {closure_count(ol, 'delivered_floor_10t')}")
    print("=== derived dry mass (power x chunk), tonnes ===")
    for row in derivations_table():
        print(f"  {row['power_kwe']:5.0f} kWe  {row['chunk_t']:6.1f} t chunk  "
              f"-> dry {row['dry_t']:6.1f} t  wet {row['wet_t']:7.1f} t  "
              f"{'OK' if row['converged'] else 'NONCONVERGED'}")


if __name__ == "__main__":
    main()
