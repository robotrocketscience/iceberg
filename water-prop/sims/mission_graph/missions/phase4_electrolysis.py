"""Phase 4 variant: electrolysis H2/O2 kick departure (saturn_water_v2).

Encodes the R-electrolysis-departure-stage architecture: over a Saturn dwell
the reactor electrolyzes harvested chunk water into hydrogen and oxygen
(including liquefaction with mandatory ortho-para catalysis), then departs on
a single impulsive Oberth-optimized periapsis burn at chemical Isp. The chunk
serves as propellant feedstock, but the burn is IMPULSIVE — it exploits the
Oberth effect a continuous-thrust spiral cannot (7.7-8.5 km/s vs 18-21.9 km/s),
which is the entire attraction.

Anchors (all from the analytic three-round chain, latest+26):
  - departure delta-v 8.51 km/s: Oberth periapsis burn from B-ring residence
    (R-eccentric-harvest-departure).
  - electrolysis energy 6.7 kWh per kg of water processed: 20 MJ/kg
    electrolysis at ~70 percent stack efficiency (~5.6 kWh/kg) plus ~1.1 kWh/kg
    hydrogen liquefaction incl. ortho-para conversion (DOE liquefaction-cost
    band scaled to the H2 mass fraction of water).
  - Isp 450 s: LH2/LOX vacuum class.
  - dwell ceiling 3 yr: the analytic round's 146-437 kWe band corresponds to
    1-3 yr production dwells; just-in-time electrolysis (no dwell) was killed
    analytically (887-5,325 kWe peak power).

NOT modeled (STUDY pre-registered exclusions): tank jettison after the burn,
return-coast boiloff (0.35 percent per 2 yr passive at Saturn given the
reactor-shadow constraint, treated as met), shadow-shield placement.
"""

from __future__ import annotations

from dataclasses import replace

from ..framework import Option, Phase, VehicleState
from .powerplant_constraints import lifetime_ok
from .phase4_saturn_departure import (
    chemical_tei,
    chunk_fed_spiral_departure,
    chemical_kick_then_chunk_fed,
    rocket_eq,
    SECONDS_PER_YEAR,
)


ELECTROLYSIS_TEI_DV_KM_S = 8.51
ELECTROLYSIS_ISP_S = 450.0
ELECTROLYSIS_ENERGY_KWH_PER_KG = 6.7
ELECTROLYSIS_MAX_DWELL_YEARS = 3.0
ELECTROLYSIS_COAST_YEARS = 6.5
ELECTROLYSIS_ARRIVAL_VINF_KM_S = 10.0


def electrolysis_kick_pre(state: VehicleState, params) -> tuple[bool, str]:
    if state.location != "saturn_orbit":
        return (False, f"electrolysis departure needs to start in saturn_orbit, got {state.location}")
    power_source = params.get("power_source", "fission")
    if power_source == "solar_thermal":
        return (False, "solar-thermal power source not viable for electrolysis production at Saturn (~1 percent Earth flux)")
    if state.power_available_kwe <= 0:
        return (False, "electrolysis production needs electrical power")
    dv = params.get("electrolysis_tei_dv_km_s", ELECTROLYSIS_TEI_DV_KM_S)
    isp = params.get("electrolysis_isp_s", ELECTROLYSIS_ISP_S)
    _, required = rocket_eq(state.mass_kg, dv, isp)
    if state.payload_kg < required:
        return (False, f"not enough chunk water to electrolyze for departure: need {required:.0f} kg, have {state.payload_kg:.0f} in payload")
    # Production-time gate: the reactor must electrolyze + liquefy the full
    # propellant load within the dwell ceiling.
    kwh_per_kg = params.get("electrolysis_energy_kwh_per_kg", ELECTROLYSIS_ENERGY_KWH_PER_KG)
    production_hours = required * kwh_per_kg / state.power_available_kwe
    max_dwell_years = params.get("electrolysis_max_dwell_years", ELECTROLYSIS_MAX_DWELL_YEARS)
    if production_hours > max_dwell_years * 8760.0:
        return (False, f"electrolysis production {production_hours / 8760.0:.1f} yr exceeds dwell ceiling {max_dwell_years:.1f} yr at {state.power_available_kwe:.0f} kWe (Kilopower-class cannot electrolyze fast enough)")
    # Reactor-lifetime hook: production runs the reactor at full power.
    ok, why = lifetime_ok(state, params, production_hours)
    if not ok:
        return (False, why)
    return (True, "feasible")


def electrolysis_kick_exec(state: VehicleState, params) -> VehicleState:
    dv = params.get("electrolysis_tei_dv_km_s", ELECTROLYSIS_TEI_DV_KM_S)
    isp = params.get("electrolysis_isp_s", ELECTROLYSIS_ISP_S)
    mass_after, burned = rocket_eq(state.mass_kg, dv, isp)
    kwh_per_kg = params.get("electrolysis_energy_kwh_per_kg", ELECTROLYSIS_ENERGY_KWH_PER_KG)
    production_hours = burned * kwh_per_kg / state.power_available_kwe
    dwell_s = production_hours * 3600.0
    return replace(
        state,
        mass_kg=mass_after,
        payload_kg=state.payload_kg - burned,
        location="earth_approach",
        v_inf_km_s=ELECTROLYSIS_ARRIVAL_VINF_KM_S,
        time_elapsed_s=state.time_elapsed_s + dwell_s + ELECTROLYSIS_COAST_YEARS * SECONDS_PER_YEAR,
        cumulative_full_power_burn_hours=state.cumulative_full_power_burn_hours + production_hours,
    )


electrolysis_kick_departure = Option(
    option_id="electrolysis_kick_departure",
    description=(
        "Reactor electrolyzes chunk water to H2/O2 over a Saturn dwell, then a "
        "single impulsive Oberth periapsis burn (8.51 km/s at 450 s) departs for Earth."
    ),
    phase_id="P4_Saturn_departure",
    precondition=electrolysis_kick_pre,
    executor=electrolysis_kick_exec,
    params_required=(),
    notes=(
        "saturn_water_v2 lever: impulsive chemistry dodges the 18-21.9 km/s "
        "electric-spiral penalty. Hot arrival (v_inf 10 km/s) re-raises the "
        "Earth-arrival wall (R8). Dwell/power coupling per "
        "R-electrolysis-departure-stage."
    ),
)


phase4_v2 = Phase(
    phase_id="P4_Saturn_departure",
    description="Trans-Earth injection from Saturn orbit; chemical, chunk-fed, hybrid, or electrolysis H2/O2 kick.",
    options=(
        chemical_tei,
        chunk_fed_spiral_departure,
        chemical_kick_then_chunk_fed,
        electrolysis_kick_departure,
    ),
)
