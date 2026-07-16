"""Phase 3: chunk acquisition.

Vehicle is in Saturn orbit (post-capture). It rendezvouses with a ring-particle
field, deploys the trawl, and captures water in the form of icy chunks. Output
is increased payload_kg (the captured water) and decreased propellant_kg
(station-keeping cost) and increased time_elapsed_s (fill time).

The captured chunk water is held in `payload_kg` and serves double duty:
  - At Earth arrival, what remains of payload_kg is the delivered tonnage.
  - During Phase 4+ low-thrust chunk-fed propulsion, payload_kg is consumed
    as propellant (water-MET / water-electrolysis-thruster). Cleaner schema
    would split into 'delivered_payload' and 'available_chunk_propellant'
    but at v0 they are the same field.

Option set:

  1. Single-pass trawl grab.
     Open trawl, drift through ring plane once, close. Quick (~2 weeks) but
     captures only what's in the immediate volume; needs to be in a chunk-
     dense zone for good yield.

  2. Drift-through station-keeping trawl.
     Per project owner belief d0cf2cc5: station-keep in the ring plane with
     a small radial offset relative to local Keplerian flow, let particles
     drift through a deployed intake at controlled relative velocity. Lower
     impact risk but slower fill (~3 months).

Cross-phase constraint: Phase 3 only runs from saturn_orbit (state.location
set by Phase 2). Captured chunk mass comes from params['chunk_mass_kg'].
"""

from __future__ import annotations

from dataclasses import replace

from ..framework import Option, Phase, VehicleState


SECONDS_PER_DAY = 86_400
SECONDS_PER_YEAR = 365.25 * SECONDS_PER_DAY


# -------------------------------------------------------------------- #
# Option 1: single-pass trawl grab
# -------------------------------------------------------------------- #

SINGLE_PASS_DAYS = 14.0
SINGLE_PASS_STATIONKEEP_KG = 50.0
SINGLE_PASS_CAPTURE_EFFICIENCY = 0.85


def single_pass_pre(state: VehicleState, params) -> tuple[bool, str]:
    if state.location != "saturn_orbit":
        return (False, f"chunk acquisition needs to start in saturn_orbit, got {state.location}")
    chunk = params["chunk_mass_kg"]
    if chunk <= 0:
        return (False, f"chunk_mass_kg must be positive, got {chunk}")
    if state.propellant_kg < SINGLE_PASS_STATIONKEEP_KG:
        return (False, f"single-pass trawl needs {SINGLE_PASS_STATIONKEEP_KG} kg propellant for station-keeping, have {state.propellant_kg:.0f}")
    return (True, "feasible")


def single_pass_exec(state: VehicleState, params) -> VehicleState:
    chunk = params["chunk_mass_kg"]
    # chunk_water_fraction multiplies CAPTURED mass by the usable-water
    # fraction of the chunk. Default 1.0 = 100 percent water (current
    # assumption). Real Saturn ring particles are dominantly water ice but
    # contain silicate inclusions and accreted material; A4 audit test.
    water_fraction = params.get("chunk_water_fraction", 1.0)
    # capture_efficiency_multiplier overrides the desk-study 0.65-0.85
    # efficiency anchors via params. Default 1.0 (no change). A14 audit:
    # 85 percent single-pass is an optimistic upper bound; engineering
    # decomposition of rendezvous + deploy + catch + contain + survive
    # gives ~30-50 percent joint success probability.
    eff_mult = params.get("capture_efficiency_multiplier", 1.0)
    captured = chunk * SINGLE_PASS_CAPTURE_EFFICIENCY * water_fraction * eff_mult
    return replace(
        state,
        mass_kg=state.mass_kg + captured - SINGLE_PASS_STATIONKEEP_KG,
        propellant_kg=state.propellant_kg - SINGLE_PASS_STATIONKEEP_KG,
        payload_kg=state.payload_kg + captured,
        time_elapsed_s=state.time_elapsed_s + SINGLE_PASS_DAYS * SECONDS_PER_DAY,
    )


single_pass_trawl = Option(
    option_id="single_pass_trawl",
    description="One pass through chunk-dense ring zone, deploy trawl, capture.",
    phase_id="P3_chunk_acquisition",
    precondition=single_pass_pre,
    executor=single_pass_exec,
    params_required=("chunk_mass_kg",),
    notes="85% capture efficiency, ~2 weeks, ~50 kg station-keeping propellant.",
)


# -------------------------------------------------------------------- #
# Option 2: drift-through station-keeping trawl
# -------------------------------------------------------------------- #

DRIFT_DAYS = 90.0
DRIFT_STATIONKEEP_KG = 250.0
DRIFT_CAPTURE_EFFICIENCY = 0.65


def drift_through_pre(state: VehicleState, params) -> tuple[bool, str]:
    if state.location != "saturn_orbit":
        return (False, f"chunk acquisition needs to start in saturn_orbit, got {state.location}")
    chunk = params["chunk_mass_kg"]
    if chunk <= 0:
        return (False, f"chunk_mass_kg must be positive, got {chunk}")
    if state.propellant_kg < DRIFT_STATIONKEEP_KG:
        return (False, f"drift-through trawl needs {DRIFT_STATIONKEEP_KG} kg propellant for station-keeping, have {state.propellant_kg:.0f}")
    return (True, "feasible")


def drift_through_exec(state: VehicleState, params) -> VehicleState:
    chunk = params["chunk_mass_kg"]
    water_fraction = params.get("chunk_water_fraction", 1.0)
    eff_mult = params.get("capture_efficiency_multiplier", 1.0)
    captured = chunk * DRIFT_CAPTURE_EFFICIENCY * water_fraction * eff_mult
    return replace(
        state,
        mass_kg=state.mass_kg + captured - DRIFT_STATIONKEEP_KG,
        propellant_kg=state.propellant_kg - DRIFT_STATIONKEEP_KG,
        payload_kg=state.payload_kg + captured,
        time_elapsed_s=state.time_elapsed_s + DRIFT_DAYS * SECONDS_PER_DAY,
    )


drift_through_trawl = Option(
    option_id="drift_through_trawl",
    description="Station-keep in ring plane with radial offset, let particles drift through intake aperture.",
    phase_id="P3_chunk_acquisition",
    precondition=drift_through_pre,
    executor=drift_through_exec,
    params_required=("chunk_mass_kg",),
    notes="65% capture efficiency, ~3 months, ~250 kg propellant. Lower impact risk per belief d0cf2cc5.",
)


# -------------------------------------------------------------------- #
# Option 3: F-G gap rendezvous
# -------------------------------------------------------------------- #
# Smaller particles in the F-G gap; lower yield per pass but lower impact
# risk. Per matrix axis 11: F-G gap is the ring-avoidance choice tied to
# argument-of-periapsis lock from Saturn SOI burn.

FG_GAP_DAYS = 60.0
FG_GAP_STATIONKEEP_KG = 150.0
FG_GAP_CAPTURE_EFFICIENCY = 0.55


def fg_gap_rendezvous_pre(state: VehicleState, params) -> tuple[bool, str]:
    if state.location != "saturn_orbit":
        return (False, f"chunk acquisition needs to start in saturn_orbit, got {state.location}")
    chunk = params["chunk_mass_kg"]
    if chunk <= 0:
        return (False, f"chunk_mass_kg must be positive, got {chunk}")
    if state.propellant_kg < FG_GAP_STATIONKEEP_KG:
        return (False, f"F-G gap rendezvous needs {FG_GAP_STATIONKEEP_KG} kg propellant for station-keeping, have {state.propellant_kg:.0f}")
    return (True, "feasible")


def fg_gap_rendezvous_exec(state: VehicleState, params) -> VehicleState:
    chunk = params["chunk_mass_kg"]
    water_fraction = params.get("chunk_water_fraction", 1.0)
    eff_mult = params.get("capture_efficiency_multiplier", 1.0)
    captured = chunk * FG_GAP_CAPTURE_EFFICIENCY * water_fraction * eff_mult
    return replace(
        state,
        mass_kg=state.mass_kg + captured - FG_GAP_STATIONKEEP_KG,
        propellant_kg=state.propellant_kg - FG_GAP_STATIONKEEP_KG,
        payload_kg=state.payload_kg + captured,
        time_elapsed_s=state.time_elapsed_s + FG_GAP_DAYS * SECONDS_PER_DAY,
    )


fg_gap_rendezvous_trawl = Option(
    option_id="fg_gap_rendezvous_trawl",
    description="F-G gap rendezvous: lower-density zone, lower yield, lower impact risk.",
    phase_id="P3_chunk_acquisition",
    precondition=fg_gap_rendezvous_pre,
    executor=fg_gap_rendezvous_exec,
    params_required=("chunk_mass_kg",),
    notes="55% capture efficiency, ~2 months, 150 kg propellant. Matches Saturn-orbit-insertion axis 11.",
)


# -------------------------------------------------------------------- #
# Option 4: B-ring direct rendezvous (high-yield, falsified survivability)
# -------------------------------------------------------------------- #
# Per phoebe R-bring-rendezvous-survivability (abdcd35): zone-averaged
# optical depth ~2 gives ~99% per-pass impact probability. The framework
# models this as effective_capture = chunk_mass * 0.01 (the surviving
# fraction across the run) and stamps a 'b_ring_survival_risk' health
# flag. The framework allows the option but the math makes it unattractive
# unless project-owner overrides via a different survival assumption.

B_RING_DAYS = 30.0
B_RING_STATIONKEEP_KG = 200.0
B_RING_SURVIVAL_PROBABILITY = 0.01
B_RING_RAW_YIELD_MULTIPLIER = 1.5  # would be best yield IF survival weren't 1%


def b_ring_direct_pre(state: VehicleState, params) -> tuple[bool, str]:
    if state.location != "saturn_orbit":
        return (False, f"chunk acquisition needs to start in saturn_orbit, got {state.location}")
    chunk = params["chunk_mass_kg"]
    if chunk <= 0:
        return (False, f"chunk_mass_kg must be positive, got {chunk}")
    if state.propellant_kg < B_RING_STATIONKEEP_KG:
        return (False, f"B-ring direct needs {B_RING_STATIONKEEP_KG} kg propellant for station-keeping, have {state.propellant_kg:.0f}")
    return (True, "feasible")


def b_ring_direct_exec(state: VehicleState, params) -> VehicleState:
    chunk = params["chunk_mass_kg"]
    # raw yield in dense B-ring is high, but engineered survivability is 1%
    water_fraction = params.get("chunk_water_fraction", 1.0)
    eff_mult = params.get("capture_efficiency_multiplier", 1.0)
    expected_captured = chunk * B_RING_RAW_YIELD_MULTIPLIER * B_RING_SURVIVAL_PROBABILITY * water_fraction * eff_mult
    return replace(
        state,
        mass_kg=state.mass_kg + expected_captured - B_RING_STATIONKEEP_KG,
        propellant_kg=state.propellant_kg - B_RING_STATIONKEEP_KG,
        payload_kg=state.payload_kg + expected_captured,
        time_elapsed_s=state.time_elapsed_s + B_RING_DAYS * SECONDS_PER_DAY,
        health_flags=state.health_flags | frozenset({"b_ring_survival_risk"}),
    )


b_ring_direct_rendezvous = Option(
    option_id="b_ring_direct_rendezvous",
    description="Direct rendezvous in dense B-ring zone. High raw yield, but engineered survivability falsified.",
    phase_id="P3_chunk_acquisition",
    precondition=b_ring_direct_pre,
    executor=b_ring_direct_exec,
    params_required=("chunk_mass_kg",),
    notes="Per phoebe abdcd35: ~1% survival across mitigation levers. Framework models expected-value capture, flags survival risk.",
)


# -------------------------------------------------------------------- #
# Phase definition
# -------------------------------------------------------------------- #

phase3 = Phase(
    phase_id="P3_chunk_acquisition",
    description="Rendezvous with ring particles, deploy trawl, capture water chunks.",
    options=(
        single_pass_trawl,
        drift_through_trawl,
        fg_gap_rendezvous_trawl,
        b_ring_direct_rendezvous,
    ),
)
