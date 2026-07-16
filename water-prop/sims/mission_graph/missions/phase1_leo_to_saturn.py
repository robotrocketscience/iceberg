"""Phase 1: low-Earth-orbit to Saturn approach.

A first try at filling in the framework blueprints. Three options:

  1. Hohmann transfer with a chemical kick stage
     - One big burn from low-Earth-orbit, then coast to Saturn.
     - Costs ~7.3 km/s of trans-Saturn-injection.
     - Coast is ~6.5 years.
     - Arrive at Saturn with ~5.44 km/s of excess speed (v-infinity).

  2. Hohmann + lunar gravity assist
     - Same idea, but use a lunar flyby to add free energy.
     - Trade ~1 km/s of departure burn for ~1-3 months of lunar tour.

  3. Continuous low-thrust spiral
     - Electric propulsion runs constantly, spiral out of Earth then arc to Saturn.
     - Higher total delta-v cost (~12-14 km/s) but much higher specific impulse
       so the propellant mass is much smaller.
     - Time of flight depends on how much thrust the reactor can support.

Sources for the anchor numbers:
  - 7.3 km/s trans-Saturn-injection from low-Earth-orbit: titan-3
    R-delta-velocity-anchor-audit, commit 42120cf (vis-viva re-derivation,
    correcting a prior 5.5 km/s informal-sketch number).
  - 5.44 km/s arrival v-infinity at Saturn sphere of influence: titan-2
    R-saturn-soi-periapsis-depth, commit 1b1b889.
  - Lunar gravity assist budget of ~1 km/s with 1-3 month tour overhead:
    aelfrice belief 1a564ee4 referencing JPL MALTO/SCOPE precedent.
"""

from __future__ import annotations

import math
from dataclasses import replace

from ..framework import Option, Phase, VehicleState
from .ephemeris_stubs import in_earth_saturn_launch_window
from .powerplant_constraints import electric_burn_hours, lifetime_ok, mass_floor_ok


SECONDS_PER_YEAR = 365.25 * 86_400
G0_KM_PER_S2 = 9.81e-3


def rocket_equation_burn(initial_mass_kg: float, delta_v_km_s: float, isp_s: float) -> tuple[float, float]:
    """Tsiolkovsky. Returns (mass_after_burn_kg, propellant_burned_kg)."""
    if isp_s <= 0:
        raise ValueError(f"isp_s must be positive, got {isp_s}")
    if delta_v_km_s < 0:
        raise ValueError(f"delta_v_km_s must be non-negative, got {delta_v_km_s}")
    exhaust_velocity = isp_s * G0_KM_PER_S2
    mass_ratio = math.exp(delta_v_km_s / exhaust_velocity)
    mass_after = initial_mass_kg / mass_ratio
    propellant_burned = initial_mass_kg - mass_after
    return mass_after, propellant_burned


def burn_time_seconds(propellant_burned_kg: float, isp_s: float, thrust_n: float) -> float:
    """Burn time at constant thrust: t = m_propellant * Isp * g_0 / F.

    For low-thrust electric propulsion this is the load-bearing constraint
    titan-3 R-chunk-size-pareto used to retire the 200-tonne anchor at
    30 kilowatt-electric: heavy mass + low thrust + large delta-velocity
    means the burn time exceeds the available Hohmann coast window.
    """
    if thrust_n <= 0:
        raise ValueError(f"thrust_n must be positive, got {thrust_n}")
    g0_m_per_s2 = 9.81
    return propellant_burned_kg * isp_s * g0_m_per_s2 / thrust_n


# -------------------------------------------------------------------- #
# Option 1: Hohmann transfer (chemical kick)
# -------------------------------------------------------------------- #

TSI_DV_HOHMANN_KM_S = 7.3
COAST_HOHMANN_YEARS = 6.5
ARRIVAL_VINF_KM_S = 5.44


def hohmann_chemical_precondition(state: VehicleState, params) -> tuple[bool, str]:
    if state.location != "LEO":
        return (False, f"Hohmann needs to start in low-Earth-orbit, got {state.location}")
    ok, why = mass_floor_ok(state, params)  # constraints 2+3: powerplant fits in dry mass
    if not ok:
        return (False, why)
    if state.epoch_jd is None or not in_earth_saturn_launch_window(state.epoch_jd):
        return (False, f"epoch_jd {state.epoch_jd} outside Earth-Saturn Hohmann launch window")
    isp = params["chemical_isp_s"]
    # Hohmann TSI delta-v can be overridden via params for sensitivity studies.
    # Default 7.3 km/s is the desk-study anchor; real value varies ~6.5-7.7
    # km/s with launch window per A7 in R_assumption_audit_2026_05_21.
    tsi_dv = params.get("tsi_hohmann_dv_km_s", TSI_DV_HOHMANN_KM_S)
    _, required_propellant = rocket_equation_burn(state.mass_kg, tsi_dv, isp)
    if state.propellant_kg < required_propellant:
        return (False, f"not enough chemical propellant: need {required_propellant:.0f} kg, have {state.propellant_kg:.0f}")
    return (True, "feasible")


def hohmann_chemical_executor(state: VehicleState, params) -> VehicleState:
    isp = params["chemical_isp_s"]
    tsi_dv = params.get("tsi_hohmann_dv_km_s", TSI_DV_HOHMANN_KM_S)
    mass_after_burn, propellant_burned = rocket_equation_burn(state.mass_kg, tsi_dv, isp)
    return replace(
        state,
        mass_kg=mass_after_burn,
        propellant_kg=state.propellant_kg - propellant_burned,
        location="saturn_approach",
        v_inf_km_s=ARRIVAL_VINF_KM_S,
        time_elapsed_s=state.time_elapsed_s + COAST_HOHMANN_YEARS * SECONDS_PER_YEAR,
    )


hohmann_chemical = Option(
    option_id="hohmann_chemical",
    description="Single chemical kick burn from low-Earth-orbit, then 6.5-year coast to Saturn.",
    phase_id="P1_LEO_to_Saturn",
    precondition=hohmann_chemical_precondition,
    executor=hohmann_chemical_executor,
    params_required=("chemical_isp_s",),
    notes="TSI = 7.3 km/s (titan-3 vis-viva audit). Arrival v_inf = 5.44 km/s (titan-2 R-saturn-soi).",
)


# -------------------------------------------------------------------- #
# Option 2: Hohmann + lunar gravity assist
# -------------------------------------------------------------------- #

LGA_BUDGET_SAVED_KM_S = 1.0
LGA_TOUR_MONTHS = 2.0
TSI_DV_HOHMANN_LGA_KM_S = TSI_DV_HOHMANN_KM_S - LGA_BUDGET_SAVED_KM_S


def hohmann_lga_precondition(state: VehicleState, params) -> tuple[bool, str]:
    if state.location != "LEO":
        return (False, f"Hohmann+LGA needs to start in low-Earth-orbit, got {state.location}")
    ok, why = mass_floor_ok(state, params)  # constraints 2+3: powerplant fits in dry mass
    if not ok:
        return (False, why)
    if state.epoch_jd is None or not in_earth_saturn_launch_window(state.epoch_jd):
        return (False, f"epoch_jd {state.epoch_jd} outside Earth-Saturn launch window")
    isp = params["chemical_isp_s"]
    _, required = rocket_equation_burn(state.mass_kg, TSI_DV_HOHMANN_LGA_KM_S, isp)
    if state.propellant_kg < required:
        return (False, f"not enough chemical propellant for reduced TSI: need {required:.0f} kg, have {state.propellant_kg:.0f}")
    return (True, "feasible")


def hohmann_lga_executor(state: VehicleState, params) -> VehicleState:
    isp = params["chemical_isp_s"]
    mass_after_burn, propellant_burned = rocket_equation_burn(state.mass_kg, TSI_DV_HOHMANN_LGA_KM_S, isp)
    extra_time = LGA_TOUR_MONTHS / 12.0 * SECONDS_PER_YEAR
    return replace(
        state,
        mass_kg=mass_after_burn,
        propellant_kg=state.propellant_kg - propellant_burned,
        location="saturn_approach",
        v_inf_km_s=ARRIVAL_VINF_KM_S,
        time_elapsed_s=state.time_elapsed_s + COAST_HOHMANN_YEARS * SECONDS_PER_YEAR + extra_time,
    )


hohmann_lga = Option(
    option_id="hohmann_lunar_gravity_assist",
    description="Smaller chemical kick (~6.3 km/s) plus a lunar flyby to get the rest of the energy free.",
    phase_id="P1_LEO_to_Saturn",
    precondition=hohmann_lga_precondition,
    executor=hohmann_lga_executor,
    params_required=("chemical_isp_s",),
    notes="LGA saves ~1 km/s of departure burn, costs ~2 months of lunar tour.",
)


# -------------------------------------------------------------------- #
# Option 3: Continuous low-thrust spiral
# -------------------------------------------------------------------- #

LOW_THRUST_TOTAL_DV_KM_S = 13.0
LOW_THRUST_MIN_POWER_KWE = 20.0


def low_thrust_precondition(state: VehicleState, params) -> tuple[bool, str]:
    if state.location != "LEO":
        return (False, f"low-thrust spiral needs to start in low-Earth-orbit, got {state.location}")
    ok, why = mass_floor_ok(state, params)  # constraints 2+3: powerplant fits in dry mass
    if not ok:
        return (False, why)
    if state.power_available_kwe < LOW_THRUST_MIN_POWER_KWE:
        return (False, f"electric thruster needs at least {LOW_THRUST_MIN_POWER_KWE} kWe, have {state.power_available_kwe} kWe")
    # Solar-thermal power class is not viable for outbound low-thrust spiral:
    # the spiral crosses out to Saturn, where solar flux drops to ~1 percent
    # of Earth's value. A solar array sized to deliver power at Saturn would
    # be ~100x larger than at Earth — not modeled here as a separate option;
    # gated by the power_source parameter.
    power_source = params.get("power_source", "fission")
    if power_source == "solar_thermal":
        return (False, f"solar-thermal power source not viable for outbound low-thrust spiral (solar flux at Saturn is ~1 percent of Earth's)")
    isp = params["electric_isp_s"]
    thrust_n = params["electric_thrust_n"]
    # delta-v can be overridden via params; default 13 km/s is the legacy
    # desk-study anchor. Edelbaum analytical lower bound for pure low-thrust
    # LEO -> Saturn approach is ~28 km/s; published Glenn Research Center
    # mission designs land in the 18-25 km/s range. See R_assumption_audit_
    # 2026_05_21/test_a2_low_thrust_delta_v.py for the derivation.
    total_dv = params.get("low_thrust_total_dv_km_s", LOW_THRUST_TOTAL_DV_KM_S)
    _, required = rocket_equation_burn(state.mass_kg, total_dv, isp)
    if state.propellant_kg < required:
        return (False, f"not enough electric propellant: need {required:.0f} kg, have {state.propellant_kg:.0f}")
    # Burn-time constraint per titan-3 R-chunk-size-pareto: low-thrust burn
    # must fit inside the Hohmann coast window (with 10% arrival margin).
    burn_s = burn_time_seconds(required, isp, thrust_n)
    coast_budget_s = 0.9 * COAST_HOHMANN_YEARS * SECONDS_PER_YEAR
    if burn_s > coast_budget_s:
        return (False, f"low-thrust burn time {burn_s/SECONDS_PER_YEAR:.2f} yr exceeds 90 percent of {COAST_HOHMANN_YEARS} yr coast window at thrust {thrust_n} N")
    # Constraint 1: outbound electric burn adds reactor full-power ON time.
    bh = electric_burn_hours(required, isp, state.power_available_kwe)
    ok, why = lifetime_ok(state, params, bh)
    if not ok:
        return (False, why)
    return (True, "feasible")


def low_thrust_executor(state: VehicleState, params) -> VehicleState:
    isp = params["electric_isp_s"]
    thrust_n = params["electric_thrust_n"]
    total_dv = params.get("low_thrust_total_dv_km_s", LOW_THRUST_TOTAL_DV_KM_S)
    mass_after_burn, propellant_burned = rocket_equation_burn(state.mass_kg, total_dv, isp)
    avg_mass = 0.5 * (state.mass_kg + mass_after_burn)
    avg_accel_km_s2 = (thrust_n * 1e-3) / avg_mass
    burn_time_s = (total_dv / avg_accel_km_s2)
    bh = electric_burn_hours(propellant_burned, isp, state.power_available_kwe)
    return replace(
        state,
        mass_kg=mass_after_burn,
        propellant_kg=state.propellant_kg - propellant_burned,
        location="saturn_approach",
        v_inf_km_s=0.5,
        time_elapsed_s=state.time_elapsed_s + burn_time_s,
        cumulative_full_power_burn_hours=state.cumulative_full_power_burn_hours + bh,
    )


low_thrust_spiral = Option(
    option_id="low_thrust_spiral",
    description="Electric thruster runs continuously, spiral out of Earth and arc to Saturn.",
    phase_id="P1_LEO_to_Saturn",
    precondition=low_thrust_precondition,
    executor=low_thrust_executor,
    params_required=("electric_isp_s", "electric_thrust_n"),
    notes="Total ~13 km/s but high Isp makes propellant cheap. Arrival v_inf small. Needs >= 20 kWe.",
)


# -------------------------------------------------------------------- #
# Option 4: Falcon Heavy + Star-class solid kick stage
# Option 5: Falcon Heavy + Impulse Helios liquid kick stage
#
# Bought-hardware kick stages do part of the trans-Saturn-injection burn so
# the vehicle does not have to spend its own propellant on it. Two effects
# the model captures:
#   - vehicle saves chemical propellant equal to the kick stage's delta-v
#     contribution (vehicle still does the remainder)
#   - kick stage dry mass was carried up by Phase 0 and is jettisoned after
#     the burn; vehicle mass drops by kick_stage_dry_mass_kg
#
# Anchor numbers:
#   - Star 48B class solid: ~2.5 km/s contribution to TSI, ~2.1 t dry mass.
#     Falcon Heavy + Star kick combo runs ~$150-180M per memory belief
#     18b686d8.
#   - Impulse Helios variant: ~4.0 km/s contribution, ~5 t dry mass.
#     Speculative; Helios is being developed for the kick-stage market but
#     has not flown a high-energy variant as of May 2026.
# -------------------------------------------------------------------- #

STAR_KICK_DV_KM_S = 2.5
STAR_KICK_DRY_MASS_KG = 2_100.0
STAR_KICK_ISP_S = 286.0

HELIOS_KICK_DV_KM_S = 4.0
HELIOS_KICK_DRY_MASS_KG = 5_000.0
HELIOS_KICK_ISP_S = 330.0


# Corrected kick-stage model (fixes a bug in the prior code):
#
#   Old behavior: treated the kick stage as "free delta-velocity with a
#   dry-mass overhead." The kick's own propellant cost was never
#   modeled; the vehicle's main chemical tank covered the residual
#   trans-Saturn-injection burn after a phantom kick delta-velocity.
#   Effect: kick options looked ~15-20 percent rosier than reality.
#
#   New behavior:
#     1. The kick stage's wet mass (kick_dry + kick_propellant) is part
#        of the launch manifest state.mass_kg at low-Earth orbit.
#     2. The kick burns its own propellant at its own specific impulse
#        to deliver kick_dv against the full launch-manifest mass.
#     3. After the kick burn, the kick dry mass is jettisoned.
#     4. The vehicle's main chemical engines then burn the residual
#        (TSI_DV_HOHMANN - kick_dv) using the vehicle's own propellant
#        tank at the vehicle's chemical specific impulse.
#
#   Precondition checks that (kick_dry + kick_propellant) fits within
#   the launch manifest's non-vehicle-propellant, non-payload envelope:
#   the kick wet mass has to come out of dry-structure budget on the
#   launch manifest.
def _kick_stage_precondition(kick_dv_km_s, kick_dry_mass_kg, kick_isp_s):
    def pre(state: VehicleState, params) -> tuple[bool, str]:
        if state.location != "LEO":
            return (False, f"kick stage trans-Saturn injection needs to start in low-Earth-orbit, got {state.location}")
        if state.epoch_jd is None or not in_earth_saturn_launch_window(state.epoch_jd):
            return (False, f"epoch_jd {state.epoch_jd} outside Earth-Saturn launch window")

        # Kick burns its own propellant at its own specific impulse against
        # the full launch-manifest mass. Compute kick propellant from
        # rocket equation.
        _, kick_propellant = rocket_equation_burn(state.mass_kg, kick_dv_km_s, kick_isp_s)
        kick_wet_mass = kick_dry_mass_kg + kick_propellant

        # Kick wet mass must fit in the launch manifest's
        # non-vehicle-propellant, non-payload envelope.
        dry_envelope = state.mass_kg - state.propellant_kg - state.payload_kg
        if dry_envelope < kick_wet_mass:
            return (
                False,
                f"kick wet mass {kick_wet_mass:.0f} kg "
                f"(dry {kick_dry_mass_kg:.0f} + propellant {kick_propellant:.0f}) "
                f"exceeds dry envelope {dry_envelope:.0f} kg of launch manifest "
                f"(mass {state.mass_kg:.0f} - vehicle propellant {state.propellant_kg:.0f} - payload {state.payload_kg:.0f})"
            )

        # Vehicle's residual trans-Saturn-injection burn at its own
        # chemical specific impulse must fit in vehicle's main propellant
        # tank.
        residual_dv = max(0.0, TSI_DV_HOHMANN_KM_S - kick_dv_km_s)
        chem_isp = params["chemical_isp_s"]
        post_kick_mass = state.mass_kg - kick_propellant - kick_dry_mass_kg
        _, vehicle_propellant_required = rocket_equation_burn(post_kick_mass, residual_dv, chem_isp)
        if state.propellant_kg < vehicle_propellant_required:
            return (
                False,
                f"not enough vehicle chemical propellant for residual "
                f"{residual_dv:.2f} km/s after kick: need "
                f"{vehicle_propellant_required:.0f} kg, have "
                f"{state.propellant_kg:.0f}"
            )
        return (True, "feasible")
    return pre


def _kick_stage_executor(kick_dv_km_s, kick_dry_mass_kg, kick_isp_s):
    def exe(state: VehicleState, params) -> VehicleState:
        # 1. Kick burns its own propellant at its own specific impulse.
        _, kick_propellant = rocket_equation_burn(state.mass_kg, kick_dv_km_s, kick_isp_s)
        # 2. Mass after kick burn (kick propellant expelled).
        mass_after_kick_burn = state.mass_kg - kick_propellant
        # 3. Jettison kick dry mass.
        mass_after_kick_jettison = mass_after_kick_burn - kick_dry_mass_kg
        # 4. Vehicle's residual chemical burn at its own specific impulse,
        #    drawing from vehicle's main propellant tank.
        residual_dv = max(0.0, TSI_DV_HOHMANN_KM_S - kick_dv_km_s)
        chem_isp = params["chemical_isp_s"]
        mass_after_residual, vehicle_propellant_burned = rocket_equation_burn(
            mass_after_kick_jettison, residual_dv, chem_isp
        )
        return replace(
            state,
            mass_kg=mass_after_residual,
            propellant_kg=state.propellant_kg - vehicle_propellant_burned,
            location="saturn_approach",
            v_inf_km_s=ARRIVAL_VINF_KM_S,
            time_elapsed_s=state.time_elapsed_s + COAST_HOHMANN_YEARS * SECONDS_PER_YEAR,
        )
    return exe


falcon_heavy_plus_star_kick = Option(
    option_id="falcon_heavy_plus_star_kick",
    description="Star-class solid kick stage delivers ~2.5 km/s of trans-Saturn injection at 286 s specific impulse; vehicle chemical burn covers the rest.",
    phase_id="P1_LEO_to_Saturn",
    precondition=_kick_stage_precondition(STAR_KICK_DV_KM_S, STAR_KICK_DRY_MASS_KG, STAR_KICK_ISP_S),
    executor=_kick_stage_executor(STAR_KICK_DV_KM_S, STAR_KICK_DRY_MASS_KG, STAR_KICK_ISP_S),
    params_required=("chemical_isp_s",),
    notes="Star-class scaled-cluster anchor: 2.5 km/s, 2.1 t dry, 286 s. Burns its own propellant from the launch manifest, NOT vehicle's chemical tank. Cost ~$150-180M combined Falcon Heavy + kick stage.",
)


falcon_heavy_plus_helios_kick = Option(
    option_id="falcon_heavy_plus_helios_kick",
    description="Impulse Helios-class liquid kick stage delivers ~4 km/s of trans-Saturn injection at 330 s specific impulse; vehicle chemical burn covers the rest.",
    phase_id="P1_LEO_to_Saturn",
    precondition=_kick_stage_precondition(HELIOS_KICK_DV_KM_S, HELIOS_KICK_DRY_MASS_KG, HELIOS_KICK_ISP_S),
    executor=_kick_stage_executor(HELIOS_KICK_DV_KM_S, HELIOS_KICK_DRY_MASS_KG, HELIOS_KICK_ISP_S),
    params_required=("chemical_isp_s",),
    notes="Helios-class speculative anchor: 4 km/s, 5 t dry, 330 s liquid bipropellant. Burns its own propellant from the launch manifest. Combo ~$80-120M if Helios delivers; not flown as of May 2026.",
)


# -------------------------------------------------------------------- #
# Phase definition
# -------------------------------------------------------------------- #

phase1 = Phase(
    phase_id="P1_LEO_to_Saturn",
    description="Trans-Saturn injection plus outbound cruise from low-Earth-orbit.",
    options=(
        hohmann_chemical,
        hohmann_lga,
        low_thrust_spiral,
        falcon_heavy_plus_star_kick,
        falcon_heavy_plus_helios_kick,
    ),
)
