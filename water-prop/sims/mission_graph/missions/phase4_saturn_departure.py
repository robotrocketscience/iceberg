"""Phase 4: trans-Earth injection from Saturn orbit.

After chunk capture, vehicle departs Saturn for Earth. Three options:

  1. Chemical trans-Earth-injection burn.
     Single big chemical burn using remaining vehicle propellant. Costs
     ~7.7 km/s of delta-v (vis-viva-corrected anchor per titan-3
     R-delta-velocity-anchor-audit). Requires substantial propellant
     fraction relative to the now-heavier (chunk-laden) vehicle.

  2. Low-thrust chunk-fed spiral departure.
     Water-MET runs continuously on the captured chunk water as propellant.
     The chunk thus serves double duty: payload (what we want to deliver)
     and fuel (what we burn to get home). Long burn time (~2 yr to
     spiral out of Saturn SOI and arc to Earth). Burns through payload.

  3. Chemical kick then chunk-fed coast.
     Small chemical kick to clear Saturn SOI (~2 km/s), then chunk-fed
     low-thrust for the rest of the heliocentric transfer.

After-burn output state has location='earth_approach' and v_inf_km_s set to
the Earth-arrival hyperbolic excess (default ~10 km/s; reduced if Phase 5
applies a planetary gravity assist on the return leg).
"""

from __future__ import annotations

import math
from dataclasses import replace

from ..framework import Option, Phase, VehicleState
from .powerplant_constraints import electric_burn_hours, lifetime_ok


SECONDS_PER_YEAR = 365.25 * 86_400
G0_KM_PER_S2 = 9.81e-3


def rocket_eq(initial_mass_kg, delta_v_km_s, isp_s):
    exhaust = isp_s * G0_KM_PER_S2
    ratio = math.exp(delta_v_km_s / exhaust)
    mass_after = initial_mass_kg / ratio
    return mass_after, initial_mass_kg - mass_after


def burn_time_seconds(propellant_burned_kg, isp_s, thrust_n):
    """Burn time at constant thrust. Load-bearing low-thrust constraint."""
    if thrust_n <= 0:
        raise ValueError(f"thrust_n must be positive, got {thrust_n}")
    return propellant_burned_kg * isp_s * 9.81 / thrust_n


# -------------------------------------------------------------------- #
# Option 1: chemical trans-Earth injection
# -------------------------------------------------------------------- #

CHEMICAL_TEI_DV_KM_S = 7.7
CHEMICAL_TEI_COAST_YEARS = 6.5
CHEMICAL_TEI_ARRIVAL_VINF_KM_S = 10.0


def chemical_tei_pre(state: VehicleState, params) -> tuple[bool, str]:
    if state.location != "saturn_orbit":
        return (False, f"trans-Earth injection needs to start in saturn_orbit, got {state.location}")
    isp = params["chemical_isp_s"]
    _, required = rocket_eq(state.mass_kg, CHEMICAL_TEI_DV_KM_S, isp)
    if state.propellant_kg < required:
        return (False, f"not enough chemical propellant for TEI: need {required:.0f} kg, have {state.propellant_kg:.0f}")
    return (True, "feasible")


def chemical_tei_exec(state: VehicleState, params) -> VehicleState:
    isp = params["chemical_isp_s"]
    mass_after, burned = rocket_eq(state.mass_kg, CHEMICAL_TEI_DV_KM_S, isp)
    return replace(
        state,
        mass_kg=mass_after,
        propellant_kg=state.propellant_kg - burned,
        location="earth_approach",
        v_inf_km_s=CHEMICAL_TEI_ARRIVAL_VINF_KM_S,
        time_elapsed_s=state.time_elapsed_s + CHEMICAL_TEI_COAST_YEARS * SECONDS_PER_YEAR,
    )


chemical_tei = Option(
    option_id="chemical_tei",
    description="Single chemical kick from Saturn orbit, coast ~6.5 yr to Earth.",
    phase_id="P4_Saturn_departure",
    precondition=chemical_tei_pre,
    executor=chemical_tei_exec,
    params_required=("chemical_isp_s",),
    notes="vis-viva-corrected TEI = 7.7 km/s (titan-3 42120cf). Arrival v_inf 10 km/s direct.",
)


# -------------------------------------------------------------------- #
# Option 2: low-thrust chunk-fed spiral departure
# -------------------------------------------------------------------- #

CHUNK_FED_DV_KM_S = 9.0
CHUNK_FED_TRANSIT_YEARS = 8.0
CHUNK_FED_ARRIVAL_VINF_KM_S = 1.0
CHUNK_FED_MIN_POWER_KWE = 30.0


def chunk_fed_pre(state: VehicleState, params) -> tuple[bool, str]:
    if state.location != "saturn_orbit":
        return (False, f"chunk-fed departure needs to start in saturn_orbit, got {state.location}")
    if state.power_available_kwe < CHUNK_FED_MIN_POWER_KWE:
        return (False, f"chunk-fed water-MET needs power >= {CHUNK_FED_MIN_POWER_KWE} kWe, have {state.power_available_kwe}")
    # Solar-thermal power class not viable at Saturn (~1 percent Earth flux).
    power_source = params.get("power_source", "fission")
    if power_source == "solar_thermal":
        return (False, f"solar-thermal power source not viable for chunk-fed spiral departure at Saturn (solar flux is ~1 percent of Earth's)")
    isp = params["water_met_isp_s"]
    _, required = rocket_eq(state.mass_kg, CHUNK_FED_DV_KM_S, isp)
    if state.payload_kg < required:
        return (False, f"not enough chunk water for chunk-fed departure: need {required:.0f} kg, have {state.payload_kg:.0f} in payload")
    # Burn-time constraint: chunk-fed continuous-thrust burn must fit inside
    # the return transit window. Default thrust derived from power if not
    # explicit: F = 2 * P / (Isp * g_0).
    thrust_n = params.get("water_met_thrust_n")
    if thrust_n is None:
        thrust_n = 2.0 * state.power_available_kwe * 1000.0 / (isp * 9.81)
    burn_s = burn_time_seconds(required, isp, thrust_n)
    transit_budget_s = 0.9 * CHUNK_FED_TRANSIT_YEARS * SECONDS_PER_YEAR
    if burn_s > transit_budget_s:
        return (False, f"chunk-fed burn time {burn_s/SECONDS_PER_YEAR:.2f} yr exceeds 90 percent of {CHUNK_FED_TRANSIT_YEARS} yr return transit at thrust {thrust_n:.1f} N (titan-3 R-chunk-size-pareto constraint)")
    # Constraint 1: inbound chunk-fed electric burn adds reactor ON time.
    bh = electric_burn_hours(required, isp, state.power_available_kwe)
    ok, why = lifetime_ok(state, params, bh)
    if not ok:
        return (False, why)
    return (True, "feasible")


def chunk_fed_exec(state: VehicleState, params) -> VehicleState:
    isp = params["water_met_isp_s"]
    mass_after, burned = rocket_eq(state.mass_kg, CHUNK_FED_DV_KM_S, isp)
    bh = electric_burn_hours(burned, isp, state.power_available_kwe)
    return replace(
        state,
        mass_kg=mass_after,
        payload_kg=state.payload_kg - burned,
        location="earth_approach",
        v_inf_km_s=CHUNK_FED_ARRIVAL_VINF_KM_S,
        time_elapsed_s=state.time_elapsed_s + CHUNK_FED_TRANSIT_YEARS * SECONDS_PER_YEAR,
        cumulative_full_power_burn_hours=state.cumulative_full_power_burn_hours + bh,
    )


chunk_fed_spiral_departure = Option(
    option_id="chunk_fed_spiral_departure",
    description="Continuous water-MET on captured chunk water as propellant. Long burn, low arrival v_inf.",
    phase_id="P4_Saturn_departure",
    precondition=chunk_fed_pre,
    executor=chunk_fed_exec,
    params_required=("water_met_isp_s",),
    notes="Chunk is double duty: payload + propellant. Burns through payload. Needs >= 30 kWe.",
)


# -------------------------------------------------------------------- #
# Option 3: chemical kick then chunk-fed coast
# -------------------------------------------------------------------- #

KICK_THEN_CHUNK_CHEMICAL_DV_KM_S = 2.0
KICK_THEN_CHUNK_ELECTRIC_DV_KM_S = 6.0
KICK_THEN_CHUNK_TRANSIT_YEARS = 7.5
KICK_THEN_CHUNK_ARRIVAL_VINF_KM_S = 3.0


def kick_then_chunk_pre(state: VehicleState, params) -> tuple[bool, str]:
    if state.location != "saturn_orbit":
        return (False, f"hybrid departure needs to start in saturn_orbit, got {state.location}")
    if state.power_available_kwe < CHUNK_FED_MIN_POWER_KWE:
        return (False, f"electric leg needs power >= {CHUNK_FED_MIN_POWER_KWE} kWe, have {state.power_available_kwe}")
    chem_isp = params["chemical_isp_s"]
    elec_isp = params["water_met_isp_s"]
    mass_after_chem, chem_burned = rocket_eq(state.mass_kg, KICK_THEN_CHUNK_CHEMICAL_DV_KM_S, chem_isp)
    if state.propellant_kg < chem_burned:
        return (False, f"not enough chemical propellant for kick: need {chem_burned:.0f} kg, have {state.propellant_kg:.0f}")
    _, elec_burned = rocket_eq(mass_after_chem, KICK_THEN_CHUNK_ELECTRIC_DV_KM_S, elec_isp)
    if state.payload_kg < elec_burned:
        return (False, f"not enough chunk water for electric leg: need {elec_burned:.0f} kg, have {state.payload_kg:.0f}")
    # Burn-time constraint on the electric leg.
    thrust_n = params.get("water_met_thrust_n")
    if thrust_n is None:
        thrust_n = 2.0 * state.power_available_kwe * 1000.0 / (elec_isp * 9.81)
    burn_s = burn_time_seconds(elec_burned, elec_isp, thrust_n)
    transit_budget_s = 0.9 * KICK_THEN_CHUNK_TRANSIT_YEARS * SECONDS_PER_YEAR
    if burn_s > transit_budget_s:
        return (False, f"hybrid electric-leg burn time {burn_s/SECONDS_PER_YEAR:.2f} yr exceeds 90 percent of {KICK_THEN_CHUNK_TRANSIT_YEARS} yr transit at thrust {thrust_n:.1f} N (burn-time-vs-coast constraint)")
    # Constraint 1: hybrid electric leg adds reactor ON time.
    bh = electric_burn_hours(elec_burned, elec_isp, state.power_available_kwe)
    ok, why = lifetime_ok(state, params, bh)
    if not ok:
        return (False, why)
    return (True, "feasible")


def kick_then_chunk_exec(state: VehicleState, params) -> VehicleState:
    chem_isp = params["chemical_isp_s"]
    elec_isp = params["water_met_isp_s"]
    mass_after_chem, chem_burned = rocket_eq(state.mass_kg, KICK_THEN_CHUNK_CHEMICAL_DV_KM_S, chem_isp)
    mass_after_elec, elec_burned = rocket_eq(mass_after_chem, KICK_THEN_CHUNK_ELECTRIC_DV_KM_S, elec_isp)
    bh = electric_burn_hours(elec_burned, elec_isp, state.power_available_kwe)
    return replace(
        state,
        mass_kg=mass_after_elec,
        propellant_kg=state.propellant_kg - chem_burned,
        payload_kg=state.payload_kg - elec_burned,
        location="earth_approach",
        v_inf_km_s=KICK_THEN_CHUNK_ARRIVAL_VINF_KM_S,
        time_elapsed_s=state.time_elapsed_s + KICK_THEN_CHUNK_TRANSIT_YEARS * SECONDS_PER_YEAR,
        cumulative_full_power_burn_hours=state.cumulative_full_power_burn_hours + bh,
    )


chemical_kick_then_chunk_fed = Option(
    option_id="chemical_kick_then_chunk_fed",
    description="Small chemical kick (~2 km/s) to clear Saturn SOI, then water-MET for the rest of the transit.",
    phase_id="P4_Saturn_departure",
    precondition=kick_then_chunk_pre,
    executor=kick_then_chunk_exec,
    params_required=("chemical_isp_s", "water_met_isp_s"),
    notes="Hybrid splits the propellant cost across two propulsion modes; trades transit time and chemical vs chunk-water budget.",
)


# -------------------------------------------------------------------- #
# Phase definition
# -------------------------------------------------------------------- #

phase4 = Phase(
    phase_id="P4_Saturn_departure",
    description="Trans-Earth injection from Saturn orbit; chemical, chunk-fed, or hybrid.",
    options=(chemical_tei, chunk_fed_spiral_departure, chemical_kick_then_chunk_fed),
)
