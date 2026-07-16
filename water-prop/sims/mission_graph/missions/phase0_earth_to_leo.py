"""Phase 0: Earth surface to low-Earth-orbit.

Three launch-vehicle options. The executor's job is to confirm the
payload fits the launch vehicle's mass cap, and then place the vehicle
in low-Earth-orbit. No propulsion work happens here — the launch vehicle
does it and is gone.

Anchor sources for capability numbers:
  - Falcon Heavy fully expended: ~64 t to LEO at 28.5 deg
    (SpaceX user guide; conservative number, real flights have been lower
    but no commercial demand has driven a max-expended cargo flight)
  - Starship full stack: ~100+ t to LEO claimed; not flown operationally
    to LEO as of May 2026, so this row is aspirational
  - Multi-Falcon-9 co-manifest with on-orbit assembly: total deliverable
    is multiplied by launch count minus assembly mass overhead; gated on
    a separate on-orbit rendezvous and joining campaign that is also TRL-
    sensitive
"""

from __future__ import annotations

from dataclasses import replace

from ..framework import Option, Phase, VehicleState


# -------------------------------------------------------------------- #
# Option 1: Falcon Heavy fully expended
# -------------------------------------------------------------------- #

FALCON_HEAVY_EXPENDED_CAP_KG = 63_800.0


def falcon_heavy_pre(state: VehicleState, params) -> tuple[bool, str]:
    if state.location != "pre_launch":
        return (False, f"launch needs to start at pre_launch, got {state.location}")
    if state.mass_kg > FALCON_HEAVY_EXPENDED_CAP_KG:
        return (False, f"payload {state.mass_kg:.0f} kg exceeds Falcon Heavy expended cap {FALCON_HEAVY_EXPENDED_CAP_KG:.0f} kg")
    return (True, "feasible")


def falcon_heavy_exec(state: VehicleState, params) -> VehicleState:
    return replace(state, location="LEO", epoch_jd=params["launch_epoch_jd"])


falcon_heavy_expended = Option(
    option_id="falcon_heavy_expended",
    description="Single Falcon Heavy fully expended, ~64 t to low-Earth-orbit.",
    phase_id="P0_Earth_to_LEO",
    precondition=falcon_heavy_pre,
    executor=falcon_heavy_exec,
    params_required=("launch_epoch_jd",),
    notes="Established launch vehicle; high heritage; per-flight cost ~$130-150M.",
)


# -------------------------------------------------------------------- #
# Option 2: Starship full stack
# -------------------------------------------------------------------- #

STARSHIP_CAP_KG = 100_000.0


def starship_pre(state: VehicleState, params) -> tuple[bool, str]:
    if state.location != "pre_launch":
        return (False, f"launch needs to start at pre_launch, got {state.location}")
    if state.mass_kg > STARSHIP_CAP_KG:
        return (False, f"payload {state.mass_kg:.0f} kg exceeds Starship cap {STARSHIP_CAP_KG:.0f} kg")
    return (True, "feasible")


def starship_exec(state: VehicleState, params) -> VehicleState:
    return replace(state, location="LEO", epoch_jd=params["launch_epoch_jd"])


starship = Option(
    option_id="starship",
    description="Single Starship full stack, ~100 t claimed to low-Earth-orbit.",
    phase_id="P0_Earth_to_LEO",
    precondition=starship_pre,
    executor=starship_exec,
    params_required=("launch_epoch_jd",),
    notes="Aspirational as of May 2026; not flown operationally to LEO yet.",
)


# -------------------------------------------------------------------- #
# Options 3-5: Multi-Falcon-Heavy campaign (segments delivered separately,
# assembled in Phase 0b before trans-Saturn injection).
#
# Each multi-launch option stamps a `multi_launch_pending_assembly_N` health
# flag where N is the launch count, and advances time_elapsed_s by
# (N-1) * 60 days to reflect inter-launch cadence at Cape Canaveral. The
# mass-overhead deduction for docking adapters and structural reinforcement
# is applied in Phase 0b's assembly executor, NOT here -- this option just
# delivers raw payload to low-Earth orbit across N separate launches.
#
# Single-launch options (falcon_heavy_expended, starship) do NOT stamp the
# flag; Phase 0b's passthrough_no_assembly option handles them.
# -------------------------------------------------------------------- #

FALCON_HEAVY_PARTIAL_REUSE_CAP_KG = 50_000.0
INTER_LAUNCH_DAYS = 60.0
SECONDS_PER_DAY = 86_400


def _multi_falcon_pre(n_launches, per_launch_cap_kg):
    def pre(state: VehicleState, params) -> tuple[bool, str]:
        if state.location != "pre_launch":
            return (False, f"launch needs to start at pre_launch, got {state.location}")
        deliverable = n_launches * per_launch_cap_kg
        if state.mass_kg > deliverable:
            return (False, f"payload {state.mass_kg:.0f} kg exceeds {n_launches}-Falcon-Heavy raw deliverable {deliverable:.0f} kg")
        return (True, "feasible")
    return pre


def _multi_falcon_exec(n_launches):
    def exe(state: VehicleState, params) -> VehicleState:
        campaign_seconds = (n_launches - 1) * INTER_LAUNCH_DAYS * SECONDS_PER_DAY
        return replace(
            state,
            location="LEO",
            epoch_jd=params["launch_epoch_jd"],
            time_elapsed_s=state.time_elapsed_s + campaign_seconds,
            health_flags=state.health_flags | frozenset({f"multi_launch_pending_assembly_{n_launches}"}),
        )
    return exe


multi_falcon_2_launch = Option(
    option_id="multi_falcon_2_launch",
    description="Two Falcon Heavy launches; segments rendezvous and dock in low-Earth orbit (assembly in Phase 0b).",
    phase_id="P0_Earth_to_LEO",
    precondition=_multi_falcon_pre(2, FALCON_HEAVY_PARTIAL_REUSE_CAP_KG),
    executor=_multi_falcon_exec(2),
    params_required=("launch_epoch_jd",),
    notes="2 launches at ~50 t each (Falcon Heavy partial reuse); 60-day inter-launch cadence; campaign elapsed = 60 days. Stamps pending-assembly flag.",
)


multi_falcon_4_launch = Option(
    option_id="multi_falcon_4_launch",
    description="Four Falcon Heavy launches plus on-orbit assembly of segments in low-Earth orbit.",
    phase_id="P0_Earth_to_LEO",
    precondition=_multi_falcon_pre(4, FALCON_HEAVY_PARTIAL_REUSE_CAP_KG),
    executor=_multi_falcon_exec(4),
    params_required=("launch_epoch_jd",),
    notes="4 launches at ~50 t each; campaign elapsed = 180 days. Higher campaign-failure risk than single launch.",
)


multi_falcon_6_launch = Option(
    option_id="multi_falcon_6_launch",
    description="Six Falcon Heavy launches plus on-orbit assembly. Largest assembled-vehicle option.",
    phase_id="P0_Earth_to_LEO",
    precondition=_multi_falcon_pre(6, FALCON_HEAVY_PARTIAL_REUSE_CAP_KG),
    executor=_multi_falcon_exec(6),
    params_required=("launch_epoch_jd",),
    notes="6 launches at ~50 t each; campaign elapsed = 300 days. P(all 6 succeed at 95 percent each) approximately 0.74.",
)


# -------------------------------------------------------------------- #
# Phase definition
# -------------------------------------------------------------------- #

phase0 = Phase(
    phase_id="P0_Earth_to_LEO",
    description="Launch from Earth surface to low-Earth-orbit parking.",
    options=(
        falcon_heavy_expended,
        starship,
        multi_falcon_2_launch,
        multi_falcon_4_launch,
        multi_falcon_6_launch,
    ),
)
