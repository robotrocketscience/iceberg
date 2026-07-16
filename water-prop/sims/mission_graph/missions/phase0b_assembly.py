"""Phase 0b: on-orbit assembly.

Runs between Phase 0 (launch) and Phase 1 (trans-Saturn injection). Three
options that handle whether the vehicle needs assembly at all:

  passthrough_no_assembly  — runs only if NO multi_launch_pending_assembly_N
                             health flag is set on incoming state. Used by
                             paths that came from single-launch Phase 0
                             (Falcon Heavy expended or Starship).

  autonomous_assembly      — runs only if a pending-assembly flag IS set.
                             Adds ~90 days of assembly + integrated checkout
                             time. Deducts a docking-adapter + structural-
                             reinforcement mass penalty (~12 percent of the
                             vehicle's launch mass). Clears the flag.

  depot_relay_assembly     — runs only if a pending-assembly flag IS set and
                             params['existing_leo_depot'] is true (asserts
                             there's a depot available to host the assembly
                             campaign). Adds ~60 days (faster than autonomous
                             because the depot supplies docking + power +
                             station-keeping). Deducts only ~8 percent mass
                             penalty.

The mass penalty is deducted from `mass_kg` AND `propellant_kg` proportionally
so the propellant fraction is preserved (mass that's hardware is now extra
docking adapters; in reality those displace some payload, but for sizing
fidelity here the cleanest invariant is to preserve the fraction).
"""

from __future__ import annotations

from dataclasses import replace

from ..framework import Option, Phase, VehicleState


SECONDS_PER_DAY = 86_400


def _has_pending_assembly_flag(state: VehicleState) -> bool:
    return any(
        flag.startswith("multi_launch_pending_assembly_")
        for flag in state.health_flags
    )


def _clear_pending_flags(state: VehicleState) -> frozenset:
    return frozenset(
        f for f in state.health_flags
        if not f.startswith("multi_launch_pending_assembly_")
    )


# -------------------------------------------------------------------- #
# Option 1: passthrough (single-launch paths)
# -------------------------------------------------------------------- #

def passthrough_pre(state: VehicleState, params) -> tuple[bool, str]:
    if state.location != "LEO":
        return (False, f"assembly stage needs to start in low-Earth-orbit, got {state.location}")
    if _has_pending_assembly_flag(state):
        return (False, "pending-assembly flag is set; cannot passthrough — must use autonomous or depot-relay assembly")
    return (True, "feasible")


def passthrough_exec(state: VehicleState, params) -> VehicleState:
    return state  # nothing to do


passthrough_no_assembly = Option(
    option_id="passthrough_no_assembly",
    description="Single-launch path: no on-orbit assembly required, proceed straight to trans-Saturn injection.",
    phase_id="P0b_assembly",
    precondition=passthrough_pre,
    executor=passthrough_exec,
    params_required=(),
    notes="Runs only when Phase 0 was a single launch (Falcon Heavy expended or Starship).",
)


# -------------------------------------------------------------------- #
# Option 2: autonomous assembly
# -------------------------------------------------------------------- #

AUTONOMOUS_ASSEMBLY_DAYS = 90.0
AUTONOMOUS_MASS_PENALTY_FRACTION = 0.12


def autonomous_pre(state: VehicleState, params) -> tuple[bool, str]:
    if state.location != "LEO":
        return (False, f"assembly stage needs to start in low-Earth-orbit, got {state.location}")
    if not _has_pending_assembly_flag(state):
        return (False, "autonomous assembly requires a multi_launch_pending_assembly_N flag from a multi-launch Phase 0")
    return (True, "feasible")


def autonomous_exec(state: VehicleState, params) -> VehicleState:
    penalty_kg = state.mass_kg * AUTONOMOUS_MASS_PENALTY_FRACTION
    new_mass = state.mass_kg - penalty_kg
    new_prop = state.propellant_kg * (1.0 - AUTONOMOUS_MASS_PENALTY_FRACTION)
    return replace(
        state,
        mass_kg=new_mass,
        propellant_kg=new_prop,
        time_elapsed_s=state.time_elapsed_s + AUTONOMOUS_ASSEMBLY_DAYS * SECONDS_PER_DAY,
        health_flags=_clear_pending_flags(state) | frozenset({"assembly_complete_autonomous"}),
    )


autonomous_assembly = Option(
    option_id="autonomous_assembly",
    description="Vehicle segments rendezvous and dock autonomously in low-Earth-orbit. ~90 days plus 12 percent mass penalty for docking and structural hardware.",
    phase_id="P0b_assembly",
    precondition=autonomous_pre,
    executor=autonomous_exec,
    params_required=(),
    notes="No depot needed. Higher risk than depot-relay because every docking event is autonomous-to-autonomous. Most expensive in time + mass.",
)


# -------------------------------------------------------------------- #
# Option 3: depot-relay assembly
# -------------------------------------------------------------------- #

DEPOT_RELAY_ASSEMBLY_DAYS = 60.0
DEPOT_RELAY_MASS_PENALTY_FRACTION = 0.08


def depot_relay_pre(state: VehicleState, params) -> tuple[bool, str]:
    if state.location != "LEO":
        return (False, f"assembly stage needs to start in low-Earth-orbit, got {state.location}")
    if not _has_pending_assembly_flag(state):
        return (False, "depot-relay assembly requires a multi_launch_pending_assembly_N flag from a multi-launch Phase 0")
    if not params.get("existing_leo_depot", False):
        return (False, "depot-relay assembly requires params['existing_leo_depot']=True (an existing depot to host the campaign)")
    return (True, "feasible")


def depot_relay_exec(state: VehicleState, params) -> VehicleState:
    penalty_kg = state.mass_kg * DEPOT_RELAY_MASS_PENALTY_FRACTION
    new_mass = state.mass_kg - penalty_kg
    new_prop = state.propellant_kg * (1.0 - DEPOT_RELAY_MASS_PENALTY_FRACTION)
    return replace(
        state,
        mass_kg=new_mass,
        propellant_kg=new_prop,
        time_elapsed_s=state.time_elapsed_s + DEPOT_RELAY_ASSEMBLY_DAYS * SECONDS_PER_DAY,
        health_flags=_clear_pending_flags(state) | frozenset({"assembly_complete_depot_relay"}),
    )


depot_relay_assembly = Option(
    option_id="depot_relay_assembly",
    description="Existing low-Earth-orbit depot hosts the assembly campaign: cheaper time (60 days) and mass (8 percent penalty) because depot provides docking aids, power, station-keeping.",
    phase_id="P0b_assembly",
    precondition=depot_relay_pre,
    executor=depot_relay_exec,
    params_required=("existing_leo_depot",),
    notes="Requires an operational depot before the campaign starts. Gated by params['existing_leo_depot']. Cuts assembly time roughly in half vs autonomous and reduces docking-hardware overhead.",
)


# -------------------------------------------------------------------- #
# Phase definition
# -------------------------------------------------------------------- #

phase0b = Phase(
    phase_id="P0b_assembly",
    description="On-orbit assembly of multi-launch segments (or passthrough for single-launch paths).",
    options=(passthrough_no_assembly, autonomous_assembly, depot_relay_assembly),
)
