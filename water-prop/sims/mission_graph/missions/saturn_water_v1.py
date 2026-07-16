"""Saturn-water mission v1: closed-loop vehicle dry mass (R-vehicle-mass-closure-refactor).

Identical phase tree to `saturn_water_v0` — the refactor is bookkeeping, not a
change to the concept of operations. The ONE difference is how the launch
vehicle mass is obtained:

  v0 (open-loop): the sweep's `vehicle_mass_kg` VehicleAxis sets
      `VehicleState.mass_kg` directly. Dry mass is whatever the axis happens to
      pick (0.2 * wet under the 0.80 propellant convention) — never checked
      against subsystem demands.

  v1 (closed-loop): `vehicle_mass_kg` is dropped from the sweep. Per cell, the
      vehicle dry mass is DERIVED by `derive_saturn_vehicle` (fixed-point over
      subsystem demands), the launch wet mass + propellant follow from the 0.80
      propellant convention, and a cell whose derivation did not converge is
      tagged `mass_nonconverged` and cannot close.

The phase sequence, options, and physics are reused verbatim from v0 so any
closure-surface difference is attributable solely to self-consistent mass.

v0 stays immutable as the open-loop baseline; this module imports its phases.
"""

from __future__ import annotations

from dataclasses import replace
from typing import Mapping

from ..framework import ClosurePredicate, Mission, VehicleState, launch_wet_and_propellant
from .saturn_mass_demands import MassContext, derive_saturn_vehicle
from .saturn_water_v0 import (
    saturn_water_v0,
    _arrived_at_depot,
    _delivered_floor,
    _delivered_floor_10t,
    _delivered_floor_20t,
    _delivered_floor_50t,
    _delivered_floor_100t,
    _round_trip_strict,
)


# Health flag stamped on the launch state when the dry-mass derivation did not
# converge. A flagged cell is mutually inconsistent (its assumed mass cannot be
# made consistent with its subsystem demands) and is counted as a non-closure.
NONCONVERGED_FLAG = "mass_nonconverged"


def _gate_on_convergence(predicate):
    """Wrap a v0 closure predicate so a non-converged cell always misses.

    The wrapped predicate returns the predicate's own "miss" verdict when the
    leaf carries NONCONVERGED_FLAG, otherwise delegates to the v0 predicate.
    """
    def wrapped(state: VehicleState) -> str:
        if NONCONVERGED_FLAG in state.health_flags:
            return "miss"
        return predicate(state)
    return wrapped


saturn_water_v1 = Mission(
    mission_id="saturn_water_v1",
    objective=(
        "Capture water at Saturn rings, deliver to low-Earth-orbit depot. "
        "Closed-loop: vehicle dry mass derived from subsystem demands, not swept."
    ),
    phase_sequence=saturn_water_v0.phase_sequence,
    closure_predicates=(
        ClosurePredicate("arrived_at_depot", "Did the path reach LEO_depot (converged mass only)?",
                         _gate_on_convergence(_arrived_at_depot)),
        ClosurePredicate("delivered_floor", ">= 30 t at LEO depot (converged mass only).",
                         _gate_on_convergence(_delivered_floor)),
        ClosurePredicate("delivered_floor_10t", ">= 10 t at LEO depot (converged mass only).",
                         _gate_on_convergence(_delivered_floor_10t)),
        ClosurePredicate("delivered_floor_20t", ">= 20 t at LEO depot (converged mass only).",
                         _gate_on_convergence(_delivered_floor_20t)),
        ClosurePredicate("delivered_floor_50t", ">= 50 t at LEO depot (converged mass only).",
                         _gate_on_convergence(_delivered_floor_50t)),
        ClosurePredicate("delivered_floor_100t", ">= 100 t at LEO depot (converged mass only).",
                         _gate_on_convergence(_delivered_floor_100t)),
        ClosurePredicate("round_trip_time", "Round-trip vs L0-05 strict 15 yr / waiver 25 yr.",
                         _gate_on_convergence(_round_trip_strict)),
    ),
)


def context_from_coords(coords: Mapping[str, float], base_params: Mapping[str, float]) -> MassContext:
    """Build a MassContext from sweep coordinates + base params.

    Swept per cell (coords): power_kwe, chunk_mass_kg, electric_thrust_n.
    Held (base_params): reactor specific power, bus floor, propellant fraction,
    capture archetype, aerocapture intent + entry velocity, dry margin.
    """
    return MassContext(
        chunk_mass_kg=float(coords.get("chunk_mass_kg", base_params.get("chunk_mass_kg", 50_000.0))),
        power_available_kwe=float(coords.get("power_kwe", base_params.get("power_kwe", 30.0))),
        electric_thrust_n=float(coords.get("electric_thrust_n", base_params.get("electric_thrust_n", 5.0))),
        reactor_specific_power_w_per_kg=float(base_params.get("reactor_specific_power_w_per_kg", 2.4)),
        bus_mass_floor_kg=float(base_params.get("bus_mass_floor_kg", 2000.0)),
        propellant_fraction=float(base_params.get("propellant_fraction", 0.80)),
        dry_margin=float(base_params.get("dry_margin", 0.20)),
        capture_arch=str(base_params.get("capture_arch", "ram_scoop")),
        aperture_area_m2=float(base_params.get("aperture_area_m2", 50.0)),
        plans_aerocapture=bool(base_params.get("plans_aerocapture", True)),
        entry_v_km_s=float(base_params.get("entry_v_km_s", 11.0)),
    )


def make_derived_mass_transform(base_params: Mapping[str, float]):
    """Build a sweep `state_transform` that sets launch mass from the derived dry mass.

    Returned callable has signature `(state, coords) -> state` (the sweep
    contract). It derives the self-consistent dry mass for the cell, sets
    `mass_kg` = launch wet mass and `propellant_kg` accordingly, and stamps
    NONCONVERGED_FLAG when the derivation did not converge.

    Closing over `base_params` is necessary because the sweep does not pass
    params to `state_transform`; the per-cell swept values arrive via `coords`.
    """
    def transform(state: VehicleState, coords: Mapping[str, float]) -> VehicleState:
        ctx = context_from_coords(coords, base_params)
        result = derive_saturn_vehicle(ctx)
        wet, propellant = launch_wet_and_propellant(result.dry_mass_kg, ctx.propellant_fraction)
        flags = state.health_flags
        if not result.converged:
            flags = flags | frozenset({NONCONVERGED_FLAG})
        return replace(state, mass_kg=wet, propellant_kg=propellant, health_flags=flags)

    return transform
