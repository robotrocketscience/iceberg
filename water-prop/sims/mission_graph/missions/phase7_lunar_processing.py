"""Phase 7: lunar processing + low-Earth-orbit water transfer (sub-mission).

Only invoked for paths that arrived at `lunar_orbit_intermediate` via the
Phase 6 `chemical_lunar_orbit_capture` option. For paths already at
LEO_depot (direct delivery), the passthrough option is a no-op.

The lunar-to-LEO water transfer is operationally distinct from the main
Saturn round trip — a relatively short (~3 km/s) low-thrust leg using
water-electric thrust at 800 s specific impulse on water taken from the
chunk itself. The locked project-owner framing: ICEBERG is responsible
for the entire delivery to LEO; the customer always picks up at LEO, not
lunar orbit.

Modeling assumptions for the sub-mission:
  1. Vehicle dry mass and any remaining chemical propellant stay at the
     lunar processing facility (the facility becomes part of an
     installed asset; vehicle does not return).
  2. The transfer uses water-electric (water-microwave-electrothermal)
     thrust at 800 s specific impulse on water from the processed chunk.
  3. Lunar-to-LEO delta-v: 3.0 km/s.
  4. Transfer duration: ~9 months (water-electric is slow, but lunar
     orbit is so close to LEO compared to Saturn that this is a small
     fraction of the round trip).

Real-world precedent: none directly. Cislunar logistics architectures
(e.g., NASA Gateway concept, ISRU studies) all assume chemical or
high-thrust transfer; a low-thrust water-electric shuttle has not flown
in this geometry. The propulsion physics is well-understood; the
operations are novel.
"""

from __future__ import annotations

import math
from dataclasses import replace

from ..framework import Option, Phase, VehicleState


SECONDS_PER_YEAR = 365.25 * 86_400
G0_KM_PER_S2 = 9.81e-3

LUNAR_TO_LEO_DV_KM_S = 3.0
LUNAR_TO_LEO_TRANSFER_MONTHS = 9.0
WATER_MET_LUNAR_TRANSFER_ISP_S = 800.0


# -------------------------------------------------------------------- #
# Option 1: passthrough for paths already at LEO_depot
# -------------------------------------------------------------------- #

def passthrough_pre(state: VehicleState, params) -> tuple[bool, str]:
    if state.location != "LEO_depot":
        return (False, f"passthrough only valid at LEO_depot, got {state.location}")
    return (True, "feasible")


def passthrough_exec(state: VehicleState, params) -> VehicleState:
    return state


passthrough_already_at_leo = Option(
    option_id="passthrough_already_at_leo",
    description="No-op for paths that delivered directly to LEO without lunar processing.",
    phase_id="P7_lunar_processing",
    precondition=passthrough_pre,
    executor=passthrough_exec,
    params_required=(),
    notes="Required so that direct-to-LEO paths walk through Phase 7 without rejection.",
)


# -------------------------------------------------------------------- #
# Option 2: lunar processing + LEO water transfer
# -------------------------------------------------------------------- #

def lunar_transfer_pre(state: VehicleState, params) -> tuple[bool, str]:
    if state.location != "lunar_orbit_intermediate":
        return (False, f"lunar processing + transfer requires lunar_orbit_intermediate, got {state.location}")
    if state.payload_kg <= 0:
        return (False, "no water payload to process and transfer")
    return (True, "feasible")


def lunar_transfer_exec(state: VehicleState, params) -> VehicleState:
    isp = WATER_MET_LUNAR_TRANSFER_ISP_S
    mass_ratio = math.exp(LUNAR_TO_LEO_DV_KM_S / (isp * G0_KM_PER_S2))
    water_arriving_at_leo = state.payload_kg / mass_ratio
    extra_time = LUNAR_TO_LEO_TRANSFER_MONTHS / 12.0 * SECONDS_PER_YEAR
    return replace(
        state,
        # Vehicle dry mass and remaining propellant stay at lunar facility.
        # Only processed water reaches LEO; its mass IS the new state.mass_kg.
        mass_kg=water_arriving_at_leo,
        propellant_kg=0.0,
        payload_kg=water_arriving_at_leo,
        location="LEO_depot",
        v_inf_km_s=0.0,
        time_elapsed_s=state.time_elapsed_s + extra_time,
    )


lunar_processing_and_leo_transfer = Option(
    option_id="lunar_processing_and_leo_transfer",
    description="Process the chunk safely at lunar orbit, then shuttle processed water to LEO via water-electric thrust (3 km/s at 800 s specific impulse, ~9 months). Vehicle dry mass stays at lunar processing facility.",
    phase_id="P7_lunar_processing",
    precondition=lunar_transfer_pre,
    executor=lunar_transfer_exec,
    params_required=(),
    notes="Water-MET-on-chunk-water transfer. ~32 percent of chunk mass burned as propellant during the lunar-to-LEO leg.",
)


# -------------------------------------------------------------------- #
# Phase definition
# -------------------------------------------------------------------- #

phase7 = Phase(
    phase_id="P7_lunar_processing",
    description="Sub-mission: lunar processing + LEO water transfer (no-op for direct-to-LEO paths).",
    options=(
        passthrough_already_at_leo,
        lunar_processing_and_leo_transfer,
    ),
)
