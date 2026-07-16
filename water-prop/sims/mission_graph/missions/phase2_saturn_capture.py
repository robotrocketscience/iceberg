"""Phase 2: Saturn-orbit insertion (capture into a bound orbit at Saturn).

Four options spanning the chemical / low-thrust / ring-geometry trades the
campaign matrix carries:

  1. Direct chemical capture: single big burn at periapsis (~1.55 km/s).
  2. Sub-D-ring periapsis + Titan pump-up: ~0.8 km/s with margin per
     titan-2's R-saturn-soi-periapsis-depth (commit 1b1b889).
  3. F-G gap periapsis variant: same idea, periapsis placed to avoid main
     ring crossings; ~0.8 km/s ballpark.
  4. Low-thrust spiral capture: continuous-thrust electric, only feasible
     when arrival v_inf is small.

The cross-phase compatibility check appears in option 4's precondition:
low-thrust spiral capture can only start from a slow arrival (v_inf <= ~1
km/s), which means it is reachable only when Phase 1 was the low-thrust
spiral, NOT when Phase 1 was Hohmann or Hohmann + lunar gravity assist
(both of which arrive at v_inf ~ 5.44 km/s).
"""

from __future__ import annotations

import math
from dataclasses import replace

from ..framework import Option, Phase, VehicleState
from .powerplant_constraints import electric_burn_hours, lifetime_ok


SECONDS_PER_YEAR = 365.25 * 86_400
G0_KM_PER_S2 = 9.81e-3


def rocket_equation_burn(initial_mass_kg: float, delta_v_km_s: float, isp_s: float) -> tuple[float, float]:
    exhaust_velocity = isp_s * G0_KM_PER_S2
    mass_ratio = math.exp(delta_v_km_s / exhaust_velocity)
    mass_after = initial_mass_kg / mass_ratio
    propellant_burned = initial_mass_kg - mass_after
    return mass_after, propellant_burned


# -------------------------------------------------------------------- #
# Option 1: Direct chemical capture
# -------------------------------------------------------------------- #

DIRECT_CHEM_DV_KM_S = 1.55


def direct_chemical_pre(state: VehicleState, params) -> tuple[bool, str]:
    if state.location != "saturn_approach":
        return (False, f"capture needs to start at saturn_approach, got {state.location}")
    isp = params["chemical_isp_s"]
    _, required = rocket_equation_burn(state.mass_kg, DIRECT_CHEM_DV_KM_S, isp)
    if state.propellant_kg < required:
        return (False, f"not enough chemical propellant for direct capture: need {required:.0f} kg, have {state.propellant_kg:.0f}")
    return (True, "feasible")


def direct_chemical_exec(state: VehicleState, params) -> VehicleState:
    isp = params["chemical_isp_s"]
    mass_after, burned = rocket_equation_burn(state.mass_kg, DIRECT_CHEM_DV_KM_S, isp)
    return replace(
        state,
        mass_kg=mass_after,
        propellant_kg=state.propellant_kg - burned,
        location="saturn_orbit",
        v_inf_km_s=0.0,
        time_elapsed_s=state.time_elapsed_s + 3600.0,
    )


direct_chemical_capture = Option(
    option_id="direct_chemical_capture",
    description="Single chemical burn at periapsis, ~1.55 km/s. Fast but propellant-heavy.",
    phase_id="P2_Saturn_capture",
    precondition=direct_chemical_pre,
    executor=direct_chemical_exec,
    params_required=("chemical_isp_s",),
    notes="Legacy baseline; retired in matrix as too propellant-expensive at current bus masses.",
)


# -------------------------------------------------------------------- #
# Option 2: Sub-D-ring periapsis + Titan pump-up
# -------------------------------------------------------------------- #

SUBDRING_DV_KM_S = 0.8
SUBDRING_TITAN_TOUR_MONTHS = 6.0


def subdring_pre(state: VehicleState, params) -> tuple[bool, str]:
    if state.location != "saturn_approach":
        return (False, f"capture needs to start at saturn_approach, got {state.location}")
    isp = params["chemical_isp_s"]
    _, required = rocket_equation_burn(state.mass_kg, SUBDRING_DV_KM_S, isp)
    if state.propellant_kg < required:
        return (False, f"not enough chemical propellant for sub-D-ring capture: need {required:.0f} kg, have {state.propellant_kg:.0f}")
    return (True, "feasible")


def subdring_exec(state: VehicleState, params) -> VehicleState:
    isp = params["chemical_isp_s"]
    mass_after, burned = rocket_equation_burn(state.mass_kg, SUBDRING_DV_KM_S, isp)
    extra = SUBDRING_TITAN_TOUR_MONTHS / 12.0 * SECONDS_PER_YEAR
    return replace(
        state,
        mass_kg=mass_after,
        propellant_kg=state.propellant_kg - burned,
        location="saturn_orbit",
        v_inf_km_s=0.0,
        time_elapsed_s=state.time_elapsed_s + extra,
    )


subdring_periapsis_capture = Option(
    option_id="subdring_periapsis_capture",
    description="Periapsis below D-ring at ~63,000 km, then Titan flybys to circularize. ~0.8 km/s with margin.",
    phase_id="P2_Saturn_capture",
    precondition=subdring_pre,
    executor=subdring_exec,
    params_required=("chemical_isp_s",),
    notes="Matrix current-of-record per titan-2 R-saturn-soi-periapsis-depth (1b1b889).",
)


# -------------------------------------------------------------------- #
# Option 3: F-G gap periapsis variant
# -------------------------------------------------------------------- #

FG_GAP_DV_KM_S = 0.85
FG_GAP_TITAN_TOUR_MONTHS = 6.0


def fg_gap_pre(state: VehicleState, params) -> tuple[bool, str]:
    if state.location != "saturn_approach":
        return (False, f"capture needs to start at saturn_approach, got {state.location}")
    isp = params["chemical_isp_s"]
    _, required = rocket_equation_burn(state.mass_kg, FG_GAP_DV_KM_S, isp)
    if state.propellant_kg < required:
        return (False, f"not enough chemical propellant for F-G gap capture: need {required:.0f} kg, have {state.propellant_kg:.0f}")
    return (True, "feasible")


def fg_gap_exec(state: VehicleState, params) -> VehicleState:
    isp = params["chemical_isp_s"]
    mass_after, burned = rocket_equation_burn(state.mass_kg, FG_GAP_DV_KM_S, isp)
    extra = FG_GAP_TITAN_TOUR_MONTHS / 12.0 * SECONDS_PER_YEAR
    return replace(
        state,
        mass_kg=mass_after,
        propellant_kg=state.propellant_kg - burned,
        location="saturn_orbit",
        v_inf_km_s=0.0,
        time_elapsed_s=state.time_elapsed_s + extra,
    )


fg_gap_periapsis_capture = Option(
    option_id="fg_gap_periapsis_capture",
    description="Periapsis placed between F and G rings, slight extra delta-v vs sub-D-ring for cleaner ring avoidance.",
    phase_id="P2_Saturn_capture",
    precondition=fg_gap_pre,
    executor=fg_gap_exec,
    params_required=("chemical_isp_s",),
    notes="Different argument-of-periapsis lock requirements vs sub-D-ring; matrix axis 11 carries this trade.",
)


# -------------------------------------------------------------------- #
# Option 4: Low-thrust spiral capture
# -------------------------------------------------------------------- #

LOW_THRUST_CAPTURE_VINF_MAX_KM_S = 1.0
LOW_THRUST_CAPTURE_DV_KM_S = 1.2
LOW_THRUST_CAPTURE_MIN_POWER_KWE = 30.0
LOW_THRUST_CAPTURE_YEARS = 1.5


def low_thrust_capture_pre(state: VehicleState, params) -> tuple[bool, str]:
    if state.location != "saturn_approach":
        return (False, f"capture needs to start at saturn_approach, got {state.location}")
    if state.v_inf_km_s > LOW_THRUST_CAPTURE_VINF_MAX_KM_S:
        return (False, f"low-thrust capture needs v_inf <= {LOW_THRUST_CAPTURE_VINF_MAX_KM_S} km/s, got {state.v_inf_km_s:.2f}")
    if state.power_available_kwe < LOW_THRUST_CAPTURE_MIN_POWER_KWE:
        return (False, f"low-thrust capture needs power >= {LOW_THRUST_CAPTURE_MIN_POWER_KWE} kWe, have {state.power_available_kwe}")
    # Solar-thermal power class not viable at Saturn (~1 percent Earth flux).
    power_source = params.get("power_source", "fission")
    if power_source == "solar_thermal":
        return (False, f"solar-thermal power source not viable for low-thrust capture at Saturn (solar flux is ~1 percent of Earth's)")
    isp = params["electric_isp_s"]
    _, required = rocket_equation_burn(state.mass_kg, LOW_THRUST_CAPTURE_DV_KM_S, isp)
    if state.propellant_kg < required:
        return (False, f"not enough electric propellant for capture: need {required:.0f} kg, have {state.propellant_kg:.0f}")
    # Constraint 1: electric capture burn adds reactor full-power ON time.
    bh = electric_burn_hours(required, isp, state.power_available_kwe)
    ok, why = lifetime_ok(state, params, bh)
    if not ok:
        return (False, why)
    return (True, "feasible")


def low_thrust_capture_exec(state: VehicleState, params) -> VehicleState:
    isp = params["electric_isp_s"]
    mass_after, burned = rocket_equation_burn(state.mass_kg, LOW_THRUST_CAPTURE_DV_KM_S, isp)
    bh = electric_burn_hours(burned, isp, state.power_available_kwe)
    return replace(
        state,
        mass_kg=mass_after,
        propellant_kg=state.propellant_kg - burned,
        location="saturn_orbit",
        v_inf_km_s=0.0,
        time_elapsed_s=state.time_elapsed_s + LOW_THRUST_CAPTURE_YEARS * SECONDS_PER_YEAR,
        cumulative_full_power_burn_hours=state.cumulative_full_power_burn_hours + bh,
    )


low_thrust_capture = Option(
    option_id="low_thrust_capture",
    description="Continuous electric thrust into Saturn orbit. Cheap propellant, slow, only works at low arrival speed.",
    phase_id="P2_Saturn_capture",
    precondition=low_thrust_capture_pre,
    executor=low_thrust_capture_exec,
    params_required=("electric_isp_s",),
    notes="Cross-phase compatibility: requires Phase 1 to have been low-thrust spiral (gives v_inf ~ 0.5); blocks Hohmann arrivals.",
)


# -------------------------------------------------------------------- #
# Option 5: Titan gravity-assist capture (single dedicated tour)
# -------------------------------------------------------------------- #
#
# Titan is Saturn's dominant moon (1/4226 of Saturn's mass, 5.6 km/s
# orbital velocity, deep in the Saturn gravity well). A dedicated Titan
# flyby tour can bleed substantial arrival v_inf over multiple close
# passes, mirroring the lunar gravity-assist pattern used for Earth
# return (locked belief 1a564ee4) but at Saturn.
#
# Anchors (post-R-saturn-moon-ga-ephemeris, phoebe 2026-05-26 latest+23):
#   - Achievable v_inf reduction = arrival v_inf itself (full capture to
#     v_inf=0). Per-Titan-flyby Δv is ~1.0-1.34 km/s realistic, ceiling
#     ~1.585 km/s. A 3-4 pass tour bleeds 3-5 km/s if arrival v_inf
#     supports it. TITAN_GA_VINF_REDUCTION_KM_S below is UNUSED by the
#     executor (which sets v_inf_km_s=0.0 directly) — kept as documentation.
#   - Minimum arrival v_inf gate (~3.5 km/s) is an OPERATIONAL HEURISTIC,
#     NOT a physics limit. Capture is *easier* at lower v_inf, not harder
#     (per phoebe FINDINGS §H6). The gate keeps the option from being
#     selected when residual v_inf is already small enough that a chemical
#     trim alone is cheaper than the multi-pass tour.
#   - Tour duration: ~8 months for a 3-4 pass capture sequence. Well-
#     calibrated / mildly conservative; could be made arrival-v_inf-
#     dependent (~2 months at v_inf 3 → ~7 months at v_inf 6.5).
#   - Small chemical trim burn (~0.3 km/s) at the end of the tour to
#     park in a science orbit. Physically plausible.
# -------------------------------------------------------------------- #

TITAN_GA_VINF_REDUCTION_KM_S = 4.0  # UNUSED — see note above; executor full-captures
TITAN_GA_MIN_VINF_KM_S = 3.5  # operational heuristic, not a physics limit
TITAN_GA_TOUR_MONTHS = 8.0
TITAN_GA_TRIM_DV_KM_S = 0.3


def titan_ga_pre(state: VehicleState, params) -> tuple[bool, str]:
    if state.location != "saturn_approach":
        return (False, f"Titan gravity-assist capture needs to start at saturn_approach, got {state.location}")
    if state.v_inf_km_s < TITAN_GA_MIN_VINF_KM_S:
        return (
            False,
            f"Titan gravity-assist capture needs arrival v_inf >= "
            f"{TITAN_GA_MIN_VINF_KM_S} km/s for useful flyby geometry, "
            f"got {state.v_inf_km_s:.2f}"
        )
    isp = params["chemical_isp_s"]
    _, required = rocket_equation_burn(state.mass_kg, TITAN_GA_TRIM_DV_KM_S, isp)
    if state.propellant_kg < required:
        return (
            False,
            f"not enough chemical propellant for post-Titan-tour trim: "
            f"need {required:.0f} kg, have {state.propellant_kg:.0f}"
        )
    return (True, "feasible")


def titan_ga_exec(state: VehicleState, params) -> VehicleState:
    isp = params["chemical_isp_s"]
    mass_after, burned = rocket_equation_burn(state.mass_kg, TITAN_GA_TRIM_DV_KM_S, isp)
    extra_time = TITAN_GA_TOUR_MONTHS / 12.0 * SECONDS_PER_YEAR
    return replace(
        state,
        mass_kg=mass_after,
        propellant_kg=state.propellant_kg - burned,
        location="saturn_orbit",
        v_inf_km_s=0.0,
        time_elapsed_s=state.time_elapsed_s + extra_time,
    )


titan_gravity_assist_capture = Option(
    option_id="titan_gravity_assist_capture",
    description="Multi-pass Titan flyby tour bleeds ~4 km/s of arrival v_inf for free; small chemical trim into science orbit.",
    phase_id="P2_Saturn_capture",
    precondition=titan_ga_pre,
    executor=titan_ga_exec,
    params_required=("chemical_isp_s",),
    notes="Desk-study constant-delta-v anchor. Ephemeris-driven version deferred to SCOPE R_saturn_moon_ga_ephemeris.",
)


# -------------------------------------------------------------------- #
# Option 6: Rhea gravity-assist capture (smaller leverage)
# -------------------------------------------------------------------- #
#
# Rhea is the second-largest Saturnian moon (~5 percent of Titan's mass).
# Useful as a secondary in a multi-moon tour or alone if the trajectory
# doesn't pass Titan favorably. Lower delta-v per pass, more passes
# needed; longer tour overall.
#
# Anchors:
#   - Max v_inf reduction: ~1.5 km/s over a dedicated tour
#   - Minimum arrival v_inf: ~4.0 km/s (tighter geometry budget)
#   - Tour duration: ~12 months
#   - Larger chemical trim (~0.7 km/s residual) because tour leaves
#     more residual v_inf to kill at periapsis.
# -------------------------------------------------------------------- #

# PHOEBE FINDINGS 2026-05-26 latest+23: Rhea is NOT a credible STANDALONE
# capture mechanism. Per-flyby Δv is ~0.085 km/s; 34+ flybys needed to
# bleed 3 km/s. The 1.5 km/s / 12-month anchor below is the desk-study
# starting point; the realistic standalone tour is multi-year or never
# converges. Treat this option as a *Rhea phasing assist* layered into a
# Titan-led tour, not as a standalone capture.
RHEA_GA_VINF_REDUCTION_KM_S = 1.5  # UNUSED — see Titan note; executor full-captures
RHEA_GA_MIN_VINF_KM_S = 4.0  # operational heuristic, not a physics limit
RHEA_GA_TOUR_MONTHS = 12.0  # under-estimates standalone tour by ~2x at high v_inf
RHEA_GA_TRIM_DV_KM_S = 0.7


def rhea_ga_pre(state: VehicleState, params) -> tuple[bool, str]:
    if state.location != "saturn_approach":
        return (False, f"Rhea gravity-assist capture needs to start at saturn_approach, got {state.location}")
    if state.v_inf_km_s < RHEA_GA_MIN_VINF_KM_S:
        return (
            False,
            f"Rhea gravity-assist capture needs arrival v_inf >= "
            f"{RHEA_GA_MIN_VINF_KM_S} km/s, got {state.v_inf_km_s:.2f}"
        )
    isp = params["chemical_isp_s"]
    _, required = rocket_equation_burn(state.mass_kg, RHEA_GA_TRIM_DV_KM_S, isp)
    if state.propellant_kg < required:
        return (
            False,
            f"not enough chemical propellant for post-Rhea-tour trim: "
            f"need {required:.0f} kg, have {state.propellant_kg:.0f}"
        )
    return (True, "feasible")


def rhea_ga_exec(state: VehicleState, params) -> VehicleState:
    isp = params["chemical_isp_s"]
    mass_after, burned = rocket_equation_burn(state.mass_kg, RHEA_GA_TRIM_DV_KM_S, isp)
    extra_time = RHEA_GA_TOUR_MONTHS / 12.0 * SECONDS_PER_YEAR
    return replace(
        state,
        mass_kg=mass_after,
        propellant_kg=state.propellant_kg - burned,
        location="saturn_orbit",
        v_inf_km_s=0.0,
        time_elapsed_s=state.time_elapsed_s + extra_time,
    )


rhea_gravity_assist_capture = Option(
    option_id="rhea_gravity_assist_capture",
    description="Multi-pass Rhea flyby tour bleeds ~1.5 km/s of arrival v_inf; larger chemical trim covers residual.",
    phase_id="P2_Saturn_capture",
    precondition=rhea_ga_pre,
    executor=rhea_ga_exec,
    params_required=("chemical_isp_s",),
    notes="Desk-study anchor. Useful when trajectory geometry favors Rhea over Titan; otherwise dominated by Titan tour.",
)


# -------------------------------------------------------------------- #
# Option 7: Cassini-class multi-moon gravity-assist tour
# -------------------------------------------------------------------- #
#
# Multi-moon tour through Titan + Rhea + Dione + Tethys + Enceladus +
# Mimas (or some subset). Cumulative v_inf reduction over a longer tour;
# the most aggressive desk-study capture option. Mirrors Cassini's
# actual 2-year orbit refinement tour, but used HERE as the capture
# mechanism itself rather than for post-capture science.
#
# Anchors:
#   - Max v_inf reduction over the full tour: ~5.5 km/s. The biggest
#     gains come from Titan; the smaller moons contribute fractional
#     km/s each but compound across many flybys.
#   - Minimum arrival v_inf: ~3.0 km/s. More flexible than single-moon
#     options because multiple targets give the trajectory designer
#     more geometry to work with.
#   - Tour duration: ~24 months. This is the cost.
#   - Near-zero chemical trim (~0.2 km/s residual) because the tour
#     leaves v_inf close to zero.
#
# PHOEBE FINDINGS 2026-05-26 latest+23: the "multi-moon" framing is
# misleading. Per-flyby Δv at Saturn's small moons is leverage-inert:
# Rhea 0.085 → Iapetus 0.067 → Dione 0.058 → Tethys 0.046 → Mimas 0.003
# km/s. Bleeding 1 km/s costs 12 Rhea flybys or 334 Mimas flybys.
# This option is MECHANICALLY A TITAN TOUR with small-moon flybys as
# phasing aids, not as leverage contributors. Consider this option
# dominated by `titan_gravity_assist_capture` (same capture, ~1/3 the
# time, comparable trim). The 24-month anchor should be reduced to
# ~10-14 months if kept as a distinct option.
#
# Engineering caveat: this is more aggressive than Cassini ever
# attempted. Cassini did a chemical capture burn at Saturn first, then
# used moon flybys for science. Using moon flybys AS the capture
# mechanism (no propulsive capture burn) is theoretically sound but has
# never flown.
# -------------------------------------------------------------------- #

CASSINI_TOUR_VINF_REDUCTION_KM_S = 5.5  # UNUSED — see Titan note; executor full-captures
CASSINI_TOUR_MIN_VINF_KM_S = 3.0  # operational heuristic, not a physics limit
CASSINI_TOUR_MONTHS = 24.0  # over-states Titan-led capture by ~3x per phoebe 2026-05-26
CASSINI_TOUR_TRIM_DV_KM_S = 0.2


def cassini_tour_pre(state: VehicleState, params) -> tuple[bool, str]:
    if state.location != "saturn_approach":
        return (False, f"Cassini-class tour capture needs to start at saturn_approach, got {state.location}")
    if state.v_inf_km_s < CASSINI_TOUR_MIN_VINF_KM_S:
        return (
            False,
            f"Cassini-class multi-moon tour needs arrival v_inf >= "
            f"{CASSINI_TOUR_MIN_VINF_KM_S} km/s, got {state.v_inf_km_s:.2f}"
        )
    isp = params["chemical_isp_s"]
    _, required = rocket_equation_burn(state.mass_kg, CASSINI_TOUR_TRIM_DV_KM_S, isp)
    if state.propellant_kg < required:
        return (
            False,
            f"not enough chemical propellant for post-Cassini-tour trim: "
            f"need {required:.0f} kg, have {state.propellant_kg:.0f}"
        )
    return (True, "feasible")


def cassini_tour_exec(state: VehicleState, params) -> VehicleState:
    isp = params["chemical_isp_s"]
    mass_after, burned = rocket_equation_burn(state.mass_kg, CASSINI_TOUR_TRIM_DV_KM_S, isp)
    extra_time = CASSINI_TOUR_MONTHS / 12.0 * SECONDS_PER_YEAR
    return replace(
        state,
        mass_kg=mass_after,
        propellant_kg=state.propellant_kg - burned,
        location="saturn_orbit",
        v_inf_km_s=0.0,
        time_elapsed_s=state.time_elapsed_s + extra_time,
    )


cassini_class_multi_moon_tour = Option(
    option_id="cassini_class_multi_moon_tour",
    description="Multi-moon flyby tour (Titan, Rhea, Dione, Tethys, Enceladus, Mimas) bleeds ~5.5 km/s of arrival v_inf over ~24 months.",
    phase_id="P2_Saturn_capture",
    precondition=cassini_tour_pre,
    executor=cassini_tour_exec,
    params_required=("chemical_isp_s",),
    notes="Most aggressive desk-study capture option. Time penalty is the trade. Real-world precedent: Cassini's tour was post-capture science, not the capture itself.",
)


# -------------------------------------------------------------------- #
# Phase definition
# -------------------------------------------------------------------- #

phase2 = Phase(
    phase_id="P2_Saturn_capture",
    description="Insert into Saturn orbit from heliocentric approach.",
    options=(
        direct_chemical_capture,
        subdring_periapsis_capture,
        fg_gap_periapsis_capture,
        low_thrust_capture,
        titan_gravity_assist_capture,
        rhea_gravity_assist_capture,
        cassini_class_multi_moon_tour,
    ),
)
