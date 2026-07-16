"""Phase 5: inbound cruise operations.

Mirror of Phase 1b cruise ops, applied to the return leg. Same option
shape: ballistic / mid-course corrections / Jupiter gravity assist / Mars
+ Jupiter assist. The gravity-assist options here reduce Earth-arrival
v_inf, which makes downstream Phase 6 (Earth capture) cheaper.

Cross-phase constraint: same as outbound; gravity-assist options need
v_inf >= 2 km/s on entry (ballistic-class arrival) so a low-thrust spiral
departure (Phase 4 chunk-fed) which arrives with v_inf ~ 1 km/s cannot
use a return-leg GA.
"""

from __future__ import annotations

import math
from dataclasses import replace

from ..framework import Option, Phase, VehicleState


SECONDS_PER_YEAR = 365.25 * 86_400
G0_KM_PER_S2 = 9.81e-3


def rocket_eq(initial_mass_kg, delta_v_km_s, isp_s):
    exhaust = isp_s * G0_KM_PER_S2
    ratio = math.exp(delta_v_km_s / exhaust)
    mass_after = initial_mass_kg / ratio
    return mass_after, initial_mass_kg - mass_after


# -------------------------------------------------------------------- #
# Option 1: Ballistic inbound coast
# -------------------------------------------------------------------- #

def inbound_ballistic_pre(state: VehicleState, params) -> tuple[bool, str]:
    if state.location != "earth_approach":
        return (False, f"inbound cruise needs to start at earth_approach, got {state.location}")
    return (True, "feasible")


def inbound_ballistic_exec(state: VehicleState, params) -> VehicleState:
    return replace(state, health_flags=state.health_flags | frozenset({"no_inbound_mcc"}))


inbound_ballistic = Option(
    option_id="inbound_ballistic",
    description="No mid-course corrections, no gravity assist on the return leg.",
    phase_id="P5_inbound_cruise_ops",
    precondition=inbound_ballistic_pre,
    executor=inbound_ballistic_exec,
    params_required=(),
    notes="Cheap but adds 'no_inbound_mcc' health flag.",
)


# -------------------------------------------------------------------- #
# Option 2: Inbound mid-course corrections
# -------------------------------------------------------------------- #

INBOUND_MCC_DV_KM_S = 0.10


def inbound_mcc_pre(state: VehicleState, params) -> tuple[bool, str]:
    if state.location != "earth_approach":
        return (False, f"inbound cruise needs to start at earth_approach, got {state.location}")
    isp = params["chemical_isp_s"]
    _, required = rocket_eq(state.mass_kg, INBOUND_MCC_DV_KM_S, isp)
    if state.propellant_kg < required:
        return (False, f"not enough chemical propellant for inbound MCC: need {required:.0f} kg, have {state.propellant_kg:.0f}")
    return (True, "feasible")


def inbound_mcc_exec(state: VehicleState, params) -> VehicleState:
    isp = params["chemical_isp_s"]
    mass_after, burned = rocket_eq(state.mass_kg, INBOUND_MCC_DV_KM_S, isp)
    return replace(state, mass_kg=mass_after, propellant_kg=state.propellant_kg - burned)


inbound_mcc = Option(
    option_id="inbound_mcc",
    description="Periodic mid-course corrections on the return leg; ~100 m/s cumulative.",
    phase_id="P5_inbound_cruise_ops",
    precondition=inbound_mcc_pre,
    executor=inbound_mcc_exec,
    params_required=("chemical_isp_s",),
    notes="Better trajectory accuracy; no v_inf change.",
)


# -------------------------------------------------------------------- #
# Option 3: Inbound Jupiter gravity assist
# -------------------------------------------------------------------- #

INBOUND_JUPITER_MIN_VINF_KM_S = 2.0
INBOUND_JUPITER_DV_KM_S = 0.15
INBOUND_JUPITER_VINF_REDUCTION_KM_S = 3.0
INBOUND_JUPITER_EXTRA_YEARS = 1.0


def inbound_jupiter_pre(state: VehicleState, params) -> tuple[bool, str]:
    if state.location != "earth_approach":
        return (False, f"inbound cruise needs to start at earth_approach, got {state.location}")
    if state.v_inf_km_s < INBOUND_JUPITER_MIN_VINF_KM_S:
        return (False, f"inbound Jupiter assist needs ballistic-class arrival v_inf >= {INBOUND_JUPITER_MIN_VINF_KM_S} km/s, got {state.v_inf_km_s:.2f}")
    isp = params["chemical_isp_s"]
    _, required = rocket_eq(state.mass_kg, INBOUND_JUPITER_DV_KM_S, isp)
    if state.propellant_kg < required:
        return (False, f"not enough propellant for inbound Jupiter MCC: need {required:.0f} kg, have {state.propellant_kg:.0f}")
    return (True, "feasible")


def inbound_jupiter_exec(state: VehicleState, params) -> VehicleState:
    isp = params["chemical_isp_s"]
    mass_after, burned = rocket_eq(state.mass_kg, INBOUND_JUPITER_DV_KM_S, isp)
    new_vinf = max(0.0, state.v_inf_km_s - INBOUND_JUPITER_VINF_REDUCTION_KM_S)
    return replace(
        state,
        mass_kg=mass_after,
        propellant_kg=state.propellant_kg - burned,
        v_inf_km_s=new_vinf,
        time_elapsed_s=state.time_elapsed_s + INBOUND_JUPITER_EXTRA_YEARS * SECONDS_PER_YEAR,
    )


inbound_jupiter_gravity_assist = Option(
    option_id="inbound_jupiter_gravity_assist",
    description="Inbound Jupiter slingshot reduces Earth-arrival v_inf by ~3 km/s; adds ~1 yr.",
    phase_id="P5_inbound_cruise_ops",
    precondition=inbound_jupiter_pre,
    executor=inbound_jupiter_exec,
    params_required=("chemical_isp_s",),
    notes="Same cross-phase constraint as outbound: needs ballistic arrival.",
)


# -------------------------------------------------------------------- #
# Phase definition
# -------------------------------------------------------------------- #

phase5 = Phase(
    phase_id="P5_inbound_cruise_ops",
    description="Inbound cruise operations: trajectory corrections and optional return-leg gravity assist.",
    options=(inbound_ballistic, inbound_mcc, inbound_jupiter_gravity_assist),
)
