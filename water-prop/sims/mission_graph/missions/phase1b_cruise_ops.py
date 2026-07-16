"""Phase 1b: cruise operations between Earth departure and Saturn approach.

The long quiet phase. Small in option count, longest in elapsed time. Four
options spanning the trade between trajectory accuracy, propellant cost,
and use of planetary gravity assists.

Note on phase ordering: this slots between Phase 1 (trans-Saturn injection
plus nominal coast) and Phase 2 (Saturn capture). It is named "1b" rather
than "2" so the existing Phase 2 phase_id does not need to renumber.

Option set:

  1. Ballistic coast (no mid-course corrections, no gravity assist).
     Trust the initial trajectory. Realistic for one-shot probes but risky
     for a multi-ship campaign where trajectory errors compound across
     years of cruise.

  2. Mid-course correction campaign.
     Periodic small burns to correct trajectory drift. Per Cassini
     precedent ~100 m/s cumulative over the cruise.

  3. Jupiter gravity assist + mid-course corrections.
     Single-flyby slingshot. Reduces arrival v_inf at Saturn by ~2.5 km/s.
     Adds ~1 year of cruise time. Requires the vehicle to be on a ballistic
     trajectory with non-trivial arrival speed (so v_inf must be >= 2 km/s
     coming in; low-thrust spiral arrivals are excluded).

  4. Mars + Jupiter gravity assist + mid-course corrections.
     Cassini-class multi-body assist. Reduces arrival v_inf by ~4 km/s.
     Adds ~2 years of cruise time. Same cross-phase constraint as Jupiter-
     only: requires ballistic-class arrival speed coming in.

Built-in test, communications, and freeze-prevention overhead is implicit
in the time elapsed for each option. Continuous-power draw and reliability
modeling is out of scope at v0.
"""

from __future__ import annotations

import math
from dataclasses import replace

from ..framework import Option, Phase, VehicleState
from .ephemeris_stubs import (
    in_cassini_class_window,
    in_jupiter_assist_window,
    in_venus_earth_ga_window,
)


SECONDS_PER_YEAR = 365.25 * 86_400
G0_KM_PER_S2 = 9.81e-3


def rocket_equation_burn(initial_mass_kg, delta_v_km_s, isp_s):
    exhaust = isp_s * G0_KM_PER_S2
    ratio = math.exp(delta_v_km_s / exhaust)
    mass_after = initial_mass_kg / ratio
    return mass_after, initial_mass_kg - mass_after


# -------------------------------------------------------------------- #
# Option 1: Ballistic coast
# -------------------------------------------------------------------- #

def ballistic_pre(state: VehicleState, params) -> tuple[bool, str]:
    if state.location != "saturn_approach":
        return (False, f"cruise ops needs to start at saturn_approach, got {state.location}")
    return (True, "feasible")


def ballistic_exec(state: VehicleState, params) -> VehicleState:
    return replace(state, health_flags=state.health_flags | frozenset({"no_mcc_redundancy"}))


ballistic_coast = Option(
    option_id="ballistic_coast",
    description="Trust the initial trajectory; no mid-course corrections, no gravity assist.",
    phase_id="P1b_cruise_ops",
    precondition=ballistic_pre,
    executor=ballistic_exec,
    params_required=(),
    notes="Lowest propellant, highest trajectory-error risk. Adds 'no_mcc_redundancy' health flag.",
)


# -------------------------------------------------------------------- #
# Option 2: Mid-course corrections only
# -------------------------------------------------------------------- #

MCC_ONLY_DV_KM_S = 0.10


def mcc_only_pre(state: VehicleState, params) -> tuple[bool, str]:
    if state.location != "saturn_approach":
        return (False, f"cruise ops needs to start at saturn_approach, got {state.location}")
    isp = params["chemical_isp_s"]
    _, required = rocket_equation_burn(state.mass_kg, MCC_ONLY_DV_KM_S, isp)
    if state.propellant_kg < required:
        return (False, f"not enough propellant for mid-course corrections: need {required:.0f} kg, have {state.propellant_kg:.0f}")
    return (True, "feasible")


def mcc_only_exec(state: VehicleState, params) -> VehicleState:
    isp = params["chemical_isp_s"]
    mass_after, burned = rocket_equation_burn(state.mass_kg, MCC_ONLY_DV_KM_S, isp)
    return replace(state, mass_kg=mass_after, propellant_kg=state.propellant_kg - burned)


mcc_only = Option(
    option_id="mcc_only",
    description="Periodic mid-course corrections; ~100 m/s of chemical delta-v cumulative over the cruise.",
    phase_id="P1b_cruise_ops",
    precondition=mcc_only_pre,
    executor=mcc_only_exec,
    params_required=("chemical_isp_s",),
    notes="Cassini-precedent budget. Trajectory accuracy preserved, no v_inf reduction.",
)


# -------------------------------------------------------------------- #
# Option 3: Jupiter gravity assist + MCC
# -------------------------------------------------------------------- #

JUPITER_GA_MCC_DV_KM_S = 0.15
JUPITER_GA_VINF_REDUCTION_KM_S = 2.5
JUPITER_GA_EXTRA_YEARS = 1.0
JUPITER_GA_MIN_VINF_KM_S = 2.0


def jupiter_ga_pre(state: VehicleState, params) -> tuple[bool, str]:
    if state.location != "saturn_approach":
        return (False, f"cruise ops needs to start at saturn_approach, got {state.location}")
    if state.v_inf_km_s < JUPITER_GA_MIN_VINF_KM_S:
        return (False, f"Jupiter gravity assist needs ballistic-class arrival v_inf >= {JUPITER_GA_MIN_VINF_KM_S} km/s, got {state.v_inf_km_s:.2f}")
    launch_epoch = params.get("launch_epoch_jd")
    if launch_epoch is None or not in_jupiter_assist_window(launch_epoch):
        return (False, f"launch_epoch_jd {launch_epoch} outside Earth-Jupiter assist window (need ~30-day window every ~399 days)")
    isp = params["chemical_isp_s"]
    _, required = rocket_equation_burn(state.mass_kg, JUPITER_GA_MCC_DV_KM_S, isp)
    if state.propellant_kg < required:
        return (False, f"not enough propellant for Jupiter-GA MCC: need {required:.0f} kg, have {state.propellant_kg:.0f}")
    return (True, "feasible")


def jupiter_ga_exec(state: VehicleState, params) -> VehicleState:
    isp = params["chemical_isp_s"]
    mass_after, burned = rocket_equation_burn(state.mass_kg, JUPITER_GA_MCC_DV_KM_S, isp)
    new_vinf = max(0.0, state.v_inf_km_s - JUPITER_GA_VINF_REDUCTION_KM_S)
    return replace(
        state,
        mass_kg=mass_after,
        propellant_kg=state.propellant_kg - burned,
        v_inf_km_s=new_vinf,
        time_elapsed_s=state.time_elapsed_s + JUPITER_GA_EXTRA_YEARS * SECONDS_PER_YEAR,
    )


jupiter_gravity_assist = Option(
    option_id="jupiter_gravity_assist",
    description="Single-flyby Jupiter slingshot reduces Saturn arrival v_inf by ~2.5 km/s; adds ~1 yr of cruise.",
    phase_id="P1b_cruise_ops",
    precondition=jupiter_ga_pre,
    executor=jupiter_ga_exec,
    params_required=("chemical_isp_s",),
    notes="Cross-phase constraint: requires ballistic arrival (v_inf >= 2 km/s); excludes low-thrust spiral paths.",
)


# -------------------------------------------------------------------- #
# Option 4: Mars + Jupiter (Cassini-class) gravity assist + MCC
# -------------------------------------------------------------------- #

MARS_JUPITER_MCC_DV_KM_S = 0.20
MARS_JUPITER_VINF_REDUCTION_KM_S = 4.0
MARS_JUPITER_EXTRA_YEARS = 2.0
MARS_JUPITER_MIN_VINF_KM_S = 2.0


def mars_jupiter_pre(state: VehicleState, params) -> tuple[bool, str]:
    if state.location != "saturn_approach":
        return (False, f"cruise ops needs to start at saturn_approach, got {state.location}")
    if state.v_inf_km_s < MARS_JUPITER_MIN_VINF_KM_S:
        return (False, f"Mars+Jupiter gravity assist needs ballistic-class arrival v_inf >= {MARS_JUPITER_MIN_VINF_KM_S} km/s, got {state.v_inf_km_s:.2f}")
    launch_epoch = params.get("launch_epoch_jd")
    if launch_epoch is None or not in_cassini_class_window(launch_epoch):
        return (False, f"launch_epoch_jd {launch_epoch} outside Cassini-class Mars+Jupiter window (~60-day window every ~20 years)")
    isp = params["chemical_isp_s"]
    _, required = rocket_equation_burn(state.mass_kg, MARS_JUPITER_MCC_DV_KM_S, isp)
    if state.propellant_kg < required:
        return (False, f"not enough propellant for multi-body MCC: need {required:.0f} kg, have {state.propellant_kg:.0f}")
    return (True, "feasible")


def mars_jupiter_exec(state: VehicleState, params) -> VehicleState:
    isp = params["chemical_isp_s"]
    mass_after, burned = rocket_equation_burn(state.mass_kg, MARS_JUPITER_MCC_DV_KM_S, isp)
    new_vinf = max(0.0, state.v_inf_km_s - MARS_JUPITER_VINF_REDUCTION_KM_S)
    return replace(
        state,
        mass_kg=mass_after,
        propellant_kg=state.propellant_kg - burned,
        v_inf_km_s=new_vinf,
        time_elapsed_s=state.time_elapsed_s + MARS_JUPITER_EXTRA_YEARS * SECONDS_PER_YEAR,
    )


mars_jupiter_gravity_assist = Option(
    option_id="mars_jupiter_gravity_assist",
    description="Cassini-class multi-body slingshot reduces Saturn arrival v_inf by ~4 km/s; adds ~2 yr of cruise.",
    phase_id="P1b_cruise_ops",
    precondition=mars_jupiter_pre,
    executor=mars_jupiter_exec,
    params_required=("chemical_isp_s",),
    notes="Cross-phase constraint same as Jupiter-only. Window alignment is much harder; for sizing only here.",
)


# -------------------------------------------------------------------- #
# Option 5: Venus-Earth gravity assist (VEEGA-class)
# -------------------------------------------------------------------- #
#
# Venus-Earth(-Earth) gravity-assist trajectory used by Galileo (1989)
# and Cassini (1997) to reach Jupiter and Saturn with reduced launch
# energy. The spacecraft passes Venus (sometimes twice), then returns
# through one or two Earth flybys to pump up velocity for the outer leg.
# Reduces arrival v_inf at Saturn by ~2 km/s vs direct injection at the
# cost of a much longer cruise (~3-4 years extra over direct Hohmann).
#
# This option is positioned between Jupiter-GA and Mars+Jupiter-GA in
# terms of leverage and complexity. The launch window is the tight
# constraint — VEEGA needs Venus alignment that recurs every ~584 days.
# -------------------------------------------------------------------- #

VENUS_EARTH_GA_MCC_DV_KM_S = 0.17
VENUS_EARTH_GA_VINF_REDUCTION_KM_S = 2.0
VENUS_EARTH_GA_EXTRA_YEARS = 3.5
VENUS_EARTH_GA_MIN_VINF_KM_S = 2.0


def venus_earth_ga_pre(state: VehicleState, params) -> tuple[bool, str]:
    if state.location != "saturn_approach":
        return (False, f"cruise ops needs to start at saturn_approach, got {state.location}")
    if state.v_inf_km_s < VENUS_EARTH_GA_MIN_VINF_KM_S:
        return (
            False,
            f"Venus-Earth gravity assist needs ballistic-class arrival v_inf >= "
            f"{VENUS_EARTH_GA_MIN_VINF_KM_S} km/s, got {state.v_inf_km_s:.2f}"
        )
    launch_epoch = params.get("launch_epoch_jd")
    if launch_epoch is None or not in_venus_earth_ga_window(launch_epoch):
        return (
            False,
            f"launch_epoch_jd {launch_epoch} outside Venus-Earth assist "
            f"window (~20-day window every ~584 days)"
        )
    isp = params["chemical_isp_s"]
    _, required = rocket_equation_burn(state.mass_kg, VENUS_EARTH_GA_MCC_DV_KM_S, isp)
    if state.propellant_kg < required:
        return (
            False,
            f"not enough propellant for Venus-Earth-GA mid-course: "
            f"need {required:.0f} kg, have {state.propellant_kg:.0f}"
        )
    return (True, "feasible")


def venus_earth_ga_exec(state: VehicleState, params) -> VehicleState:
    isp = params["chemical_isp_s"]
    mass_after, burned = rocket_equation_burn(state.mass_kg, VENUS_EARTH_GA_MCC_DV_KM_S, isp)
    new_vinf = max(0.0, state.v_inf_km_s - VENUS_EARTH_GA_VINF_REDUCTION_KM_S)
    return replace(
        state,
        mass_kg=mass_after,
        propellant_kg=state.propellant_kg - burned,
        v_inf_km_s=new_vinf,
        time_elapsed_s=state.time_elapsed_s + VENUS_EARTH_GA_EXTRA_YEARS * SECONDS_PER_YEAR,
    )


venus_earth_gravity_assist = Option(
    option_id="venus_earth_gravity_assist",
    description="VEEGA-class Venus-Earth(-Earth) slingshot reduces Saturn arrival v_inf by ~2 km/s; adds ~3.5 yr of cruise.",
    phase_id="P1b_cruise_ops",
    precondition=venus_earth_ga_pre,
    executor=venus_earth_ga_exec,
    params_required=("chemical_isp_s",),
    notes="Galileo / Cassini heritage trajectory class. Long cruise cost is the tradeoff for reduced launch energy.",
)


# -------------------------------------------------------------------- #
# Phase definition
# -------------------------------------------------------------------- #

phase1b = Phase(
    phase_id="P1b_cruise_ops",
    description="Cruise operations: mid-course corrections, planetary gravity assists, comms / built-in-test overhead.",
    options=(
        ballistic_coast,
        mcc_only,
        jupiter_gravity_assist,
        mars_jupiter_gravity_assist,
        venus_earth_gravity_assist,
    ),
)
