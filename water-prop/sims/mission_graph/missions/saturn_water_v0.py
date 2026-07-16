"""Saturn-water mission v0: end-to-end seven-phase concept of operations.

Phases:
  P0  Earth surface -> low-Earth-orbit parking
  P1  Trans-Saturn injection (TSI burn + nominal coast lumped)
  P1b Outbound cruise operations (corrections / gravity assists)
  P2  Saturn-orbit insertion
  P3  Chunk acquisition (ring rendezvous + trawl)
  P4  Trans-Earth injection (Saturn departure)
  P5  Inbound cruise operations
  P6  Earth arrival and depot delivery

The closure predicates apply to the final leaf state at low-Earth-orbit
depot:
  - arrived_at_depot:        location == 'LEO_depot'
  - delivered_floor:         payload_kg >= 30 t (L0-09 commercial floor)
  - round_trip_under_strict: time_elapsed_s <= 15 yr (L0-05 strict)
  - round_trip_under_waiver: time_elapsed_s <= 25 yr (L0-05 waiver)
"""

from __future__ import annotations

from ..framework import ClosurePredicate, Mission
from .phase0_earth_to_leo import phase0
from .phase0b_assembly import phase0b
from .phase1_leo_to_saturn import phase1
from .phase1b_cruise_ops import phase1b
from .phase2_saturn_capture import phase2
from .phase3_chunk_acquisition import phase3
from .phase4_saturn_departure import phase4
from .phase5_inbound_cruise_ops import phase5
from .phase6_earth_arrival import phase6
from .phase7_lunar_processing import phase7


SECONDS_PER_YEAR = 365.25 * 86_400


def _arrived_at_depot(state) -> str:
    """Final delivery is ALWAYS at low-Earth-orbit. Lunar-orbit arrival
    is an intermediate (Phase 6 + Phase 7 sub-mission): vehicle parks
    in lunar orbit for safe processing, then transfers water-only to
    LEO. The end state must be LEO_depot."""
    return "close" if state.location == "LEO_depot" else "miss"


def _delivered_floor(state) -> str:
    """At least 30 t of payload at the low-Earth-orbit depot. LEO is the
    only valid sale point; lunar orbit is processing-only.

    Note: 30 t is sticky shorthand from titan-3 R-chunk-size-pareto, NOT
    an anchored requirement. L0-04 commercial-class floor in
    REQUIREMENTS.md is OPEN/TBD. The five _delivered_floor_*t variants
    below let us sweep the floor; per R_assumption_audit_2026_05_21
    assumption A11."""
    if state.location == "LEO_depot" and state.payload_kg >= 30_000:
        return "close"
    return "miss"


def _delivered_floor_10t(state) -> str:
    if state.location == "LEO_depot" and state.payload_kg >= 10_000:
        return "close"
    return "miss"


def _delivered_floor_20t(state) -> str:
    if state.location == "LEO_depot" and state.payload_kg >= 20_000:
        return "close"
    return "miss"


def _delivered_floor_50t(state) -> str:
    if state.location == "LEO_depot" and state.payload_kg >= 50_000:
        return "close"
    return "miss"


def _delivered_floor_100t(state) -> str:
    if state.location == "LEO_depot" and state.payload_kg >= 100_000:
        return "close"
    return "miss"


def _round_trip_strict(state) -> str:
    years = state.time_elapsed_s / SECONDS_PER_YEAR
    if years <= 15.0:
        return "close_strict"
    if years <= 25.0:
        return "close_waiver"
    return "miss"


saturn_water_v0 = Mission(
    mission_id="saturn_water_v0",
    objective="Capture water at Saturn rings, deliver to low-Earth-orbit depot.",
    phase_sequence=(phase0, phase0b, phase1, phase1b, phase2, phase3, phase4, phase5, phase6, phase7),
    closure_predicates=(
        ClosurePredicate(
            name="arrived_at_depot",
            description="Did the path reach LEO_depot?",
            fn=_arrived_at_depot,
        ),
        ClosurePredicate(
            name="delivered_floor",
            description="At least 30 t of payload at LEO depot. Note: 30 t is sticky working anchor, not an anchored requirement. L0-04 is TBD.",
            fn=_delivered_floor,
        ),
        ClosurePredicate(
            name="delivered_floor_10t",
            description="At least 10 t at LEO depot (demonstrator-class threshold).",
            fn=_delivered_floor_10t,
        ),
        ClosurePredicate(
            name="delivered_floor_20t",
            description="At least 20 t at LEO depot (pre-commercial-class threshold).",
            fn=_delivered_floor_20t,
        ),
        ClosurePredicate(
            name="delivered_floor_50t",
            description="At least 50 t at LEO depot (higher-than-current commercial-class threshold).",
            fn=_delivered_floor_50t,
        ),
        ClosurePredicate(
            name="delivered_floor_100t",
            description="At least 100 t at LEO depot (annual demand at 1 mission per year).",
            fn=_delivered_floor_100t,
        ),
        ClosurePredicate(
            name="round_trip_time",
            description="Total mission round-trip time vs L0-05 strict 15 yr / waiver 25 yr.",
            fn=_round_trip_strict,
        ),
    ),
)
