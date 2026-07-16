"""Phase 6: Earth arrival and depot delivery.

Final phase. Vehicle is on Earth approach with some v_inf. Goal: end up in
a depot orbit (low-Earth-orbit at 28.5 deg, eccentricity ~0). Four options:

  1. Direct propulsive capture.
     Single chemical burn at Earth periapsis to convert hyperbolic excess
     into a bound orbit and then circularize to depot. Costs chemical
     propellant proportional to v_inf.

  2. Lunar-gravity-assist tour then propulsive trim.
     Per memory belief 1a564ee4: ~3-6 month tour, 10 lunar flybys can bleed
     ~5.83 km/s of v_inf for free. Vehicle then needs a smaller propulsive
     burn for final depot insertion.

  3. Aerocapture.
     Single atmospheric pass to bleed v_inf via drag. Falsified for the
     chunk-bearing 200-tonne anchor per phoebe R-hybrid-aerocapture-
     aerobraking (0/1920 cells), but may be feasible at smaller payload.
     Cross-phase: requires v_inf <= some threshold (otherwise pass-1 shatter)
     and payload_kg <= some threshold (otherwise sublimation budget).

  4. Low-thrust spiral capture.
     Continuous chunk-fed (or remaining vehicle electric prop) to spiral
     into depot orbit. Only feasible at very low arrival v_inf.

After this phase, location='LEO_depot' and payload_kg is the delivered tonnage.
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


# -------------------------------------------------------------------- #
# Option 1: Direct propulsive capture
# -------------------------------------------------------------------- #

# Low-Earth-orbit reference (6578 km radius ~= 200 km altitude). GM_Earth =
# 398600 km^3/s^2. v_circ = sqrt(GM/r) = 7.78 km/s; v_esc = sqrt(2)*v_circ = 11.0.
V_CIRC_LEO_KM_S = 7.78
V_ESC_LEO_KM_S = 11.0


def direct_propulsive_capture_dv(v_inf_km_s, params=None):
    """Chemical burn to capture a hyperbolic arrival into the LEO depot orbit.

    Constraint 4 (R-framework-matrix-parity). When params['visviva_capture'] is
    True, use the physically correct vis-viva capture burn
        dv = sqrt(v_inf^2 + v_esc_LEO^2) - v_circ_LEO
    which reproduces titan-3 R-delta-velocity-anchor-audit's 7.3 km/s direct
    (v_inf ~10.3) and 4.2 km/s post-lunar-GA (v_inf ~4.47). The legacy default
    (0.4*v_inf + 0.3) understated the burn by ~2.5-3 km/s, biggest at low v_inf
    (0.7 vs 3.2 km/s at v_inf = 1) — it ignored the escape-velocity floor of a
    LEO capture. Default keeps the legacy formula so the constraints-off baseline
    and existing tests are unchanged.
    """
    if params is not None and params.get("visviva_capture", False):
        return math.sqrt(v_inf_km_s ** 2 + V_ESC_LEO_KM_S ** 2) - V_CIRC_LEO_KM_S
    return 0.4 * v_inf_km_s + 0.3


def direct_propulsive_pre(state: VehicleState, params) -> tuple[bool, str]:
    if state.location != "earth_approach":
        return (False, f"Earth arrival needs to start at earth_approach, got {state.location}")
    dv = direct_propulsive_capture_dv(state.v_inf_km_s, params)
    isp = params["chemical_isp_s"]
    _, required = rocket_eq(state.mass_kg, dv, isp)
    if state.propellant_kg < required:
        return (False, f"not enough chemical propellant for direct capture at v_inf {state.v_inf_km_s:.2f}: need {required:.0f} kg, have {state.propellant_kg:.0f}")
    return (True, "feasible")


def direct_propulsive_exec(state: VehicleState, params) -> VehicleState:
    dv = direct_propulsive_capture_dv(state.v_inf_km_s, params)
    isp = params["chemical_isp_s"]
    mass_after, burned = rocket_eq(state.mass_kg, dv, isp)
    return replace(
        state,
        mass_kg=mass_after,
        propellant_kg=state.propellant_kg - burned,
        location="LEO_depot",
        v_inf_km_s=0.0,
        time_elapsed_s=state.time_elapsed_s + 3600.0,
    )


direct_propulsive_capture = Option(
    option_id="direct_propulsive_capture",
    description="Single chemical burn at Earth periapsis to capture into low-Earth-orbit depot.",
    phase_id="P6_Earth_arrival",
    precondition=direct_propulsive_pre,
    executor=direct_propulsive_exec,
    params_required=("chemical_isp_s",),
    notes="Burn scales with arrival v_inf: high v_inf means propellant-heavy.",
)


# -------------------------------------------------------------------- #
# Option 2: Lunar gravity assist tour + propulsive trim
# -------------------------------------------------------------------- #

LGA_TOUR_VINF_REDUCTION_KM_S = 5.83
LGA_TOUR_MONTHS = 4.5
LGA_RESIDUAL_VINF_FLOOR_KM_S = 0.5
LGA_TOUR_MIN_VINF_KM_S = 2.0


def lga_propulsive_pre(state: VehicleState, params) -> tuple[bool, str]:
    if state.location != "earth_approach":
        return (False, f"Earth arrival needs to start at earth_approach, got {state.location}")
    if state.v_inf_km_s < LGA_TOUR_MIN_VINF_KM_S:
        return (False, f"lunar GA tour wants v_inf >= {LGA_TOUR_MIN_VINF_KM_S} km/s, got {state.v_inf_km_s:.2f}")
    residual_vinf = max(LGA_RESIDUAL_VINF_FLOOR_KM_S, state.v_inf_km_s - LGA_TOUR_VINF_REDUCTION_KM_S)
    dv = direct_propulsive_capture_dv(residual_vinf, params)
    isp = params["chemical_isp_s"]
    _, required = rocket_eq(state.mass_kg, dv, isp)
    if state.propellant_kg < required:
        return (False, f"not enough chemical propellant for post-LGA trim: need {required:.0f} kg, have {state.propellant_kg:.0f}")
    return (True, "feasible")


def lga_propulsive_exec(state: VehicleState, params) -> VehicleState:
    residual_vinf = max(LGA_RESIDUAL_VINF_FLOOR_KM_S, state.v_inf_km_s - LGA_TOUR_VINF_REDUCTION_KM_S)
    dv = direct_propulsive_capture_dv(residual_vinf, params)
    isp = params["chemical_isp_s"]
    mass_after, burned = rocket_eq(state.mass_kg, dv, isp)
    extra_time = LGA_TOUR_MONTHS / 12.0 * SECONDS_PER_YEAR
    return replace(
        state,
        mass_kg=mass_after,
        propellant_kg=state.propellant_kg - burned,
        location="LEO_depot",
        v_inf_km_s=0.0,
        time_elapsed_s=state.time_elapsed_s + extra_time,
    )


lunar_gravity_assist_capture = Option(
    option_id="lunar_gravity_assist_capture",
    description="Lunar GA tour bleeds ~5.83 km/s of arrival v_inf for free, then small chemical trim into depot.",
    phase_id="P6_Earth_arrival",
    precondition=lga_propulsive_pre,
    executor=lga_propulsive_exec,
    params_required=("chemical_isp_s",),
    notes="Per belief 1a564ee4 (JPL MALTO/SCOPE LGA tour, ~4.5 months, 10 flybys).",
)


# -------------------------------------------------------------------- #
# Option 3: Aerocapture
# -------------------------------------------------------------------- #

AEROCAPTURE_MAX_VINF_KM_S = 6.0
AEROCAPTURE_MAX_PAYLOAD_KG = 30_000.0
AEROCAPTURE_RESIDUAL_VINF_KM_S = 0.3


def aerocapture_pre(state: VehicleState, params) -> tuple[bool, str]:
    if state.location != "earth_approach":
        return (False, f"Earth arrival needs to start at earth_approach, got {state.location}")
    if state.v_inf_km_s > AEROCAPTURE_MAX_VINF_KM_S:
        return (False, f"aerocapture pass-1 fails at v_inf > {AEROCAPTURE_MAX_VINF_KM_S} km/s (chunk shatter), got {state.v_inf_km_s:.2f}")
    if state.payload_kg > AEROCAPTURE_MAX_PAYLOAD_KG:
        return (False, f"aerocapture cannot survive payload > {AEROCAPTURE_MAX_PAYLOAD_KG/1000:.0f} t (sublimation budget exceeded), have {state.payload_kg/1000:.1f} t")
    return (True, "feasible")


def aerocapture_exec(state: VehicleState, params) -> VehicleState:
    sublimation_loss_kg = 0.05 * state.payload_kg  # 5% sublimation budget
    return replace(
        state,
        mass_kg=state.mass_kg - sublimation_loss_kg,
        payload_kg=state.payload_kg - sublimation_loss_kg,
        location="LEO_depot",
        v_inf_km_s=0.0,
        time_elapsed_s=state.time_elapsed_s + 7 * 86_400,  # ~1 week
    )


aerocapture = Option(
    option_id="aerocapture",
    description="Single atmospheric pass at Earth bleeds v_inf via drag. Sublimation budget 5% of payload.",
    phase_id="P6_Earth_arrival",
    precondition=aerocapture_pre,
    executor=aerocapture_exec,
    params_required=(),
    notes="Falsified at >= 200 t chunk per phoebe; allowed at <= 30 t. Per phoebe 9b3d29e + 1623cca.",
)


# -------------------------------------------------------------------- #
# Option 4: Low-thrust spiral capture
# -------------------------------------------------------------------- #

LT_CAPTURE_MAX_VINF_KM_S = 1.5
LT_CAPTURE_DV_KM_S = 2.0
LT_CAPTURE_MIN_POWER_KWE = 30.0
LT_CAPTURE_MONTHS = 6.0


def lt_capture_pre(state: VehicleState, params) -> tuple[bool, str]:
    if state.location != "earth_approach":
        return (False, f"Earth arrival needs to start at earth_approach, got {state.location}")
    if state.v_inf_km_s > LT_CAPTURE_MAX_VINF_KM_S:
        return (False, f"low-thrust spiral capture needs v_inf <= {LT_CAPTURE_MAX_VINF_KM_S} km/s, got {state.v_inf_km_s:.2f}")
    if state.power_available_kwe < LT_CAPTURE_MIN_POWER_KWE:
        return (False, f"low-thrust capture needs power >= {LT_CAPTURE_MIN_POWER_KWE} kWe, have {state.power_available_kwe}")
    isp = params["water_met_isp_s"]
    _, required = rocket_eq(state.mass_kg, LT_CAPTURE_DV_KM_S, isp)
    if state.payload_kg < required:
        return (False, f"not enough chunk water for low-thrust Earth capture: need {required:.0f} kg, have {state.payload_kg:.0f}")
    # Constraint 1: electric Earth-capture spiral adds reactor ON time.
    bh = electric_burn_hours(required, isp, state.power_available_kwe)
    ok, why = lifetime_ok(state, params, bh)
    if not ok:
        return (False, why)
    return (True, "feasible")


def lt_capture_exec(state: VehicleState, params) -> VehicleState:
    isp = params["water_met_isp_s"]
    mass_after, burned = rocket_eq(state.mass_kg, LT_CAPTURE_DV_KM_S, isp)
    bh = electric_burn_hours(burned, isp, state.power_available_kwe)
    extra_time = LT_CAPTURE_MONTHS / 12.0 * SECONDS_PER_YEAR
    return replace(
        state,
        mass_kg=mass_after,
        payload_kg=state.payload_kg - burned,
        location="LEO_depot",
        v_inf_km_s=0.0,
        time_elapsed_s=state.time_elapsed_s + extra_time,
        cumulative_full_power_burn_hours=state.cumulative_full_power_burn_hours + bh,
    )


low_thrust_earth_capture = Option(
    option_id="low_thrust_earth_capture",
    description="Continuous chunk-fed spiral into low-Earth-orbit depot.",
    phase_id="P6_Earth_arrival",
    precondition=lt_capture_pre,
    executor=lt_capture_exec,
    params_required=("water_met_isp_s",),
    notes="Burns chunk water. Cross-phase compatibility: needs slow arrival (v_inf <= 1.5 km/s).",
)


# -------------------------------------------------------------------- #
# Option 5: Hybrid aerocapture + aerobraking
# -------------------------------------------------------------------- #
# Multi-pass at Earth: first pass bleeds enough v_inf for capture, then
# subsequent shallower passes circularize. Per phoebe 1623cca: at chunk-
# bearing 200+ t payload, 0 of 1920 cells close (chunk shatter at pass-1,
# unphysical aerobraking timescale, or sublimation budget exhausted). The
# framework models this as feasible up to a higher v_inf and a higher
# payload cap than single-pass aerocapture, but with a steeper sublimation
# budget (10% rather than 5%) reflecting the multi-pass thermal stress.

HYBRID_AERO_MAX_VINF_KM_S = 8.0
HYBRID_AERO_MAX_PAYLOAD_KG = 100_000.0
HYBRID_AERO_SUBLIMATION_FRACTION = 0.10
HYBRID_AERO_PASS_COUNT = 3
HYBRID_AERO_DAYS = 14.0


def hybrid_aero_pre(state: VehicleState, params) -> tuple[bool, str]:
    if state.location != "earth_approach":
        return (False, f"Earth arrival needs to start at earth_approach, got {state.location}")
    if state.v_inf_km_s > HYBRID_AERO_MAX_VINF_KM_S:
        return (False, f"hybrid aerocapture pass-1 fails at v_inf > {HYBRID_AERO_MAX_VINF_KM_S} km/s, got {state.v_inf_km_s:.2f}")
    if state.payload_kg > HYBRID_AERO_MAX_PAYLOAD_KG:
        return (False, f"hybrid aerocapture cannot survive payload > {HYBRID_AERO_MAX_PAYLOAD_KG/1000:.0f} t (sublimation budget across {HYBRID_AERO_PASS_COUNT} passes exceeded), have {state.payload_kg/1000:.1f} t")
    return (True, "feasible")


def hybrid_aero_exec(state: VehicleState, params) -> VehicleState:
    sublimation_loss = HYBRID_AERO_SUBLIMATION_FRACTION * state.payload_kg
    return replace(
        state,
        mass_kg=state.mass_kg - sublimation_loss,
        payload_kg=state.payload_kg - sublimation_loss,
        location="LEO_depot",
        v_inf_km_s=0.0,
        time_elapsed_s=state.time_elapsed_s + HYBRID_AERO_DAYS * 86_400,
    )


hybrid_aerocapture_aerobraking = Option(
    option_id="hybrid_aerocapture_aerobraking",
    description="Multi-pass: aerocapture + aerobraking. Higher v_inf and payload tolerance than single-pass; 10% sublimation budget.",
    phase_id="P6_Earth_arrival",
    precondition=hybrid_aero_pre,
    executor=hybrid_aero_exec,
    params_required=(),
    notes="Per phoebe 1623cca: falsified at chunk-bearing 200+ t under conservative anchors; framework models the optimistic edge.",
)


# -------------------------------------------------------------------- #
# Option 6: Earth gravity-assist slowdown (alternative to aerocapture)
# -------------------------------------------------------------------- #
#
# Multi-flyby Earth gravity-assist tour to slow the arriving spacecraft
# without atmospheric entry. Cassini did Earth flyby for SPEED-UP in
# 1999 (the reverse geometry — Earth GA for SLOWDOWN — is rarer but
# geometrically sound). For ICEBERG, this is the fallback path when the
# chunk is too big for aerocapture (aerocapture caps at 30 tonnes
# payload in the current model) but the vehicle does not have enough
# propellant for direct propulsive capture.
#
# Anchors:
#   - v_inf reduction: ~3 km/s over 2-3 close flybys
#   - Minimum arrival v_inf: 2 km/s (below that the geometry is too tight)
#   - Tour duration: ~4 months
#   - Chemical trim burn at the end: residual v_inf -> 0 at depot orbit
#   - NO payload mass limit (unlike aerocapture)
#
# Engineering caveat: Earth-GA slowdown is unflown. Cassini's 1999
# Earth flyby was a speed-up; the reverse-direction geometry exists in
# trajectory-optimization papers but has no operational heritage.
# -------------------------------------------------------------------- #

EARTH_GA_SLOWDOWN_VINF_REDUCTION_KM_S = 3.0
EARTH_GA_SLOWDOWN_MIN_VINF_KM_S = 2.0
EARTH_GA_SLOWDOWN_MONTHS = 4.0
EARTH_GA_SLOWDOWN_RESIDUAL_VINF_FLOOR_KM_S = 0.5


def earth_ga_slowdown_pre(state: VehicleState, params) -> tuple[bool, str]:
    if state.location != "earth_approach":
        return (False, f"Earth arrival needs to start at earth_approach, got {state.location}")
    if state.v_inf_km_s < EARTH_GA_SLOWDOWN_MIN_VINF_KM_S:
        return (
            False,
            f"Earth gravity-assist slowdown wants v_inf >= "
            f"{EARTH_GA_SLOWDOWN_MIN_VINF_KM_S} km/s, got {state.v_inf_km_s:.2f}"
        )
    residual_vinf = max(
        EARTH_GA_SLOWDOWN_RESIDUAL_VINF_FLOOR_KM_S,
        state.v_inf_km_s - EARTH_GA_SLOWDOWN_VINF_REDUCTION_KM_S,
    )
    dv = direct_propulsive_capture_dv(residual_vinf, params)
    isp = params["chemical_isp_s"]
    _, required = rocket_eq(state.mass_kg, dv, isp)
    if state.propellant_kg < required:
        return (
            False,
            f"not enough chemical propellant for post-Earth-GA trim: "
            f"need {required:.0f} kg, have {state.propellant_kg:.0f}"
        )
    return (True, "feasible")


def earth_ga_slowdown_exec(state: VehicleState, params) -> VehicleState:
    residual_vinf = max(
        EARTH_GA_SLOWDOWN_RESIDUAL_VINF_FLOOR_KM_S,
        state.v_inf_km_s - EARTH_GA_SLOWDOWN_VINF_REDUCTION_KM_S,
    )
    dv = direct_propulsive_capture_dv(residual_vinf, params)
    isp = params["chemical_isp_s"]
    mass_after, burned = rocket_eq(state.mass_kg, dv, isp)
    extra_time = EARTH_GA_SLOWDOWN_MONTHS / 12.0 * SECONDS_PER_YEAR
    return replace(
        state,
        mass_kg=mass_after,
        propellant_kg=state.propellant_kg - burned,
        location="LEO_depot",
        v_inf_km_s=0.0,
        time_elapsed_s=state.time_elapsed_s + extra_time,
    )


earth_gravity_assist_slowdown = Option(
    option_id="earth_gravity_assist_slowdown",
    description="Multi-flyby Earth GA bleeds ~3 km/s of arrival v_inf; small chemical trim into depot. NO payload mass limit (unlike aerocapture).",
    phase_id="P6_Earth_arrival",
    precondition=earth_ga_slowdown_pre,
    executor=earth_ga_slowdown_exec,
    params_required=("chemical_isp_s",),
    notes="Fallback path for chunks too big for aerocapture's 30 t payload limit. Unflown geometry (Cassini's 1999 Earth flyby was a speed-up; reverse-direction slowdown is geometrically sound but lacks operational heritage).",
)


# -------------------------------------------------------------------- #
# Option 7: Lunar-orbit delivery (contamination mitigation)
# -------------------------------------------------------------------- #
#
# Deliver the chunk to lunar orbit (e.g., low-lunar orbit or a Lagrange-
# point parking orbit) instead of low-Earth orbit. Motivation:
#
#   1. CONTAMINATION. A 200-tonne ice chunk failure near low-Earth orbit
#      could seed Kessler-syndrome-class debris. Lunar orbit is far from
#      the operational LEO + GEO infrastructure; even catastrophic
#      breakup at the Moon does not threaten Earth orbit.
#   2. PROPELLANT. Insertion into a lunar parking orbit from the Earth
#      approach trajectory needs only ~0.85 km/s vs ~3.5 km/s for low-
#      Earth-orbit insertion. That is ~75 percent less propellant.
#
# Business trade-off (NOT modeled here): water at lunar orbit is worth
# less per kilogram than water at low-Earth orbit because the buyer pays
# the cislunar transit leg. Closure predicate `delivered_floor_lunar_orbit`
# tracks lunar-delivery tonnage separately so the matrix can read both
# surfaces independently.
# -------------------------------------------------------------------- #

LUNAR_ORBIT_CAPTURE_DV_KM_S = 0.85
LUNAR_ORBIT_DELIVERY_HOURS = 24.0  # transit from earth_approach to lunar orbit


def lunar_orbit_chemical_pre(state: VehicleState, params) -> tuple[bool, str]:
    if state.location != "earth_approach":
        return (False, f"Earth arrival needs to start at earth_approach, got {state.location}")
    isp = params["chemical_isp_s"]
    _, required = rocket_eq(state.mass_kg, LUNAR_ORBIT_CAPTURE_DV_KM_S, isp)
    if state.propellant_kg < required:
        return (
            False,
            f"not enough chemical propellant for lunar-orbit insertion: "
            f"need {required:.0f} kg, have {state.propellant_kg:.0f}"
        )
    return (True, "feasible")


def lunar_orbit_chemical_exec(state: VehicleState, params) -> VehicleState:
    isp = params["chemical_isp_s"]
    mass_after, burned = rocket_eq(state.mass_kg, LUNAR_ORBIT_CAPTURE_DV_KM_S, isp)
    return replace(
        state,
        mass_kg=mass_after,
        propellant_kg=state.propellant_kg - burned,
        location="lunar_orbit_intermediate",
        v_inf_km_s=0.0,
        time_elapsed_s=state.time_elapsed_s + LUNAR_ORBIT_DELIVERY_HOURS * 3600.0,
    )


chemical_lunar_orbit_capture = Option(
    option_id="chemical_lunar_orbit_capture",
    description="Single chemical burn (~0.85 km/s) inserts vehicle into lunar parking orbit. Intermediate state — NOT a delivery target. Phase 7 (lunar processing + LEO transfer) handles the rest of the sub-mission.",
    phase_id="P6_Earth_arrival",
    precondition=lunar_orbit_chemical_pre,
    executor=lunar_orbit_chemical_exec,
    params_required=("chemical_isp_s",),
    notes="Sets location='lunar_orbit_intermediate'. Phase 7 finishes the sub-mission: process chunk + transfer water to LEO_depot. LEO is the only sale point per project owner; lunar orbit is processing-only.",
)


# -------------------------------------------------------------------- #
# Phase definition
# -------------------------------------------------------------------- #

phase6 = Phase(
    phase_id="P6_Earth_arrival",
    description="Earth arrival and depot delivery: propulsive, lunar GA + propulsive, aerocapture variants, low-thrust spiral, Earth GA slowdown, or lunar-orbit delivery (contamination mitigation).",
    options=(
        direct_propulsive_capture,
        lunar_gravity_assist_capture,
        aerocapture,
        low_thrust_earth_capture,
        hybrid_aerocapture_aerobraking,
        earth_gravity_assist_slowdown,
        chemical_lunar_orbit_capture,
    ),
)
