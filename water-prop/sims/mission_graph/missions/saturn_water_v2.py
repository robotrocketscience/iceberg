"""Saturn-water mission v2: v1 closed-loop + electrolysis H2/O2 departure stage.

Identical to saturn_water_v1 except:
  1. Phase 4 is the extended variant (all three v0 departure options PLUS
     `electrolysis_kick_departure` from phase4_electrolysis).
  2. The derived-mass transform sets `electrolysis_stage=True` in the
     MassContext, so the fixed point charges the ISRU plant (20 kg/kWe
     first-pass) and dry-dependent cryo tankage (6 percent of the P4
     propellant estimate).

Closure predicates are reused from v1 verbatim (same convergence gating).
v1 and v0 stay untouched; any closure-surface difference between v1 and v2
at matched parameters is attributable solely to the departure-stage encoding.

Pre-registration: rounds/R_saturn_water_v2_electrolysis_departure/STUDY.md.
"""

from __future__ import annotations

from dataclasses import replace
from typing import Mapping

from ..framework import Mission, VehicleState, launch_wet_and_propellant
from .saturn_mass_demands import MassContext, derive_saturn_vehicle
from .saturn_water_v0 import saturn_water_v0
from .saturn_water_v1 import saturn_water_v1, NONCONVERGED_FLAG, context_from_coords
from .phase4_electrolysis import phase4_v2


def _v2_phase_sequence():
    """v0 phase tuple with Phase 4 swapped for the extended variant."""
    seq = []
    for ph in saturn_water_v0.phase_sequence:
        if ph.phase_id == "P4_Saturn_departure":
            seq.append(phase4_v2)
        else:
            seq.append(ph)
    return tuple(seq)


saturn_water_v2 = Mission(
    mission_id="saturn_water_v2",
    objective=(
        "Capture water at Saturn rings, deliver to low-Earth-orbit depot. "
        "Closed-loop v1 plus electrolysis H2/O2 impulsive departure stage."
    ),
    phase_sequence=_v2_phase_sequence(),
    closure_predicates=saturn_water_v1.closure_predicates,
)


def context_from_coords_v2(coords: Mapping[str, float], base_params: Mapping[str, float]) -> MassContext:
    """v1 context with the electrolysis stage switched on (and overridable)."""
    base = context_from_coords(coords, base_params)
    return replace(
        base,
        electrolysis_stage=True,
        electrolysis_plant_kg_per_kwe=float(base_params.get("electrolysis_plant_kg_per_kwe", 20.0)),
        electrolysis_cryo_tank_fraction=float(base_params.get("electrolysis_cryo_tank_fraction", 0.06)),
        electrolysis_tei_dv_km_s=float(base_params.get("electrolysis_tei_dv_km_s", 8.51)),
        electrolysis_isp_s=float(base_params.get("electrolysis_isp_s", 450.0)),
    )


def make_derived_mass_transform_v2(base_params: Mapping[str, float]):
    """v2 sweep state_transform: derived dry mass including the ISRU stage."""
    def transform(state: VehicleState, coords: Mapping[str, float]) -> VehicleState:
        ctx = context_from_coords_v2(coords, base_params)
        result = derive_saturn_vehicle(ctx)
        wet, propellant = launch_wet_and_propellant(result.dry_mass_kg, ctx.propellant_fraction)
        flags = state.health_flags
        if not result.converged:
            flags = flags | frozenset({NONCONVERGED_FLAG})
        return replace(state, mass_kg=wet, propellant_kg=propellant, health_flags=flags)

    return transform
