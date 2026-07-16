"""Saturn-water vehicle subsystem mass-demand functions (closed-loop refactor).

Concrete mission-level demand functions consumed by the generic
`framework.dry_mass.derive_dry_mass` iterator. Each function reports a
subsystem's dry mass (kg). The Saturn vehicle's self-consistent dry mass is
the fixed point of the margined sum of these.

Anchors (SCOPE §"Per-phase mass-demand functions — first-pass forms"), with
one deliberate deviation recorded in STUDY.md decision D1:

  POWERPLANT (reactor + MARVL radiator + thrusters): REUSES
  `powerplant_constraints.required_powerplant_mass_kg`, the locked-belief
  state-of-record (KRUSTY 2.4 W/kg reactor per power finding 1 / belief
  0d5c8822; MARVL bundled radiator 5 t + 0.1 t/kWe per belief 0418e2c9;
  thrusters 10 kg/kWe per titan-3). The SCOPE's first-pass reactor anchor
  (5000 + 0.2*kWe) understates the locked KRUSTY figure by ~2.5x at 30 kWe
  (5 t vs 12.5 t) and is NOT used. This keeps the closed-loop framework
  consistent with the matrix-parity constraint encoding rather than forking a
  second, lighter reactor model.

  BUS: conservative 2000 kg anchor (constraint 3; Cassini heritage ~600 kg).

  CAPTURE: the SCOPE's three archetypes (harpoon / ram-scoop / everting) belong
  to R_chunk_capture_monte_carlo, NOT to saturn_water_v0's Phase 3 (single-pass
  / drift / F-G / B-ring trawls). The default `ram_scoop` bag form is used for
  the trawl bag + frame; the other archetypes are selectable via capture_arch
  for cross-use by the monte-carlo round. Mismatch noted in FINDINGS.

  TPS / STRUCTURE / COMMS / TANKAGE: SCOPE first-pass forms verbatim.

All anchors are first-pass and bounded; fidelity refinement against Wertz SMAD
subsystem mass models is the explicit follow-on R-vehicle-mass-fidelity-refinement.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from ..framework import DemandFn, DerivationResult, derive_dry_mass
from .powerplant_constraints import required_powerplant_mass_kg


# Subsystem dictionary keys (stable; report tables and tests join on these).
KEY_POWERPLANT = "powerplant"        # reactor + MARVL radiator + thrusters
KEY_BUS = "bus"                      # bus + guidance baseline (constraint 3)
KEY_CAPTURE = "capture_mechanism"
KEY_TPS = "aerocapture_tps"
KEY_STRUCTURE = "primary_structure"
KEY_COMMS = "comms_guidance_computer"
KEY_TANKAGE = "tankage"


@dataclass(frozen=True)
class MassContext:
    """Inputs to the Saturn vehicle dry-mass derivation for one sweep cell.

    Swept per cell: chunk_mass_kg, power_available_kwe, electric_thrust_n.
    Held from base params: specific power, bus floor, propellant fraction,
    capture archetype, aerocapture intent + entry velocity, dry margin.
    """

    chunk_mass_kg: float
    power_available_kwe: float
    electric_thrust_n: float = 5.0

    reactor_specific_power_w_per_kg: float = 2.4   # KRUSTY-measured (locked belief)
    bus_mass_floor_kg: float = 2000.0              # conservative (constraint 3)

    propellant_fraction: float = 0.80              # existing sweep convention
    dry_margin: float = 0.20                       # NASA Class-B

    capture_arch: str = "ram_scoop"                # trawl bag default
    aperture_area_m2: float = 50.0

    plans_aerocapture: bool = True                 # conservative: carry TPS
    entry_v_km_s: float = 11.0                     # Earth-arrival worst case for TPS sizing

    comms_floor_kg: float = 2000.0


# -------------------------------------------------------------------- #
# Per-subsystem demand forms (kg). Chunk/power/thrust-driven terms are
# independent of the trial dry mass; only tankage depends on it.
# -------------------------------------------------------------------- #

def powerplant_demand_kg(ctx: MassContext) -> float:
    """Reactor + MARVL radiator + thrusters (locked-belief anchors; D1)."""
    return required_powerplant_mass_kg(
        ctx.power_available_kwe,
        {"reactor_specific_power_w_per_kg": ctx.reactor_specific_power_w_per_kg},
    )


def capture_demand_kg(ctx: MassContext) -> float:
    """Capture-mechanism mass for the selected archetype (SCOPE forms)."""
    chunk = ctx.chunk_mass_kg
    arch = ctx.capture_arch
    if arch == "harpoon":
        return 500.0 + 0.05 * chunk
    if arch == "everting_sleeve":
        return 2000.0 + 0.10 * chunk
    # default: ram-scoop bag + frame (also models the saturn_water_v0 trawl bag)
    return 1000.0 + 0.08 * chunk + 50.0 * ctx.aperture_area_m2


def tps_demand_kg(ctx: MassContext) -> float:
    """Earth-aerocapture thermal-protection mass (chunk + entry-velocity driven).

    Charged only when the architecture plans an aerocapture/aerobraking Earth
    arrival. v1 defaults `plans_aerocapture=True` (conservative: every vehicle
    carries TPS). Path-conditional TPS (charge only on aerocapture paths) is a
    fidelity follow-on; see STUDY.md D3.
    """
    if not ctx.plans_aerocapture:
        return 0.0
    return 0.10 * ctx.chunk_mass_kg + 200.0 * ctx.entry_v_km_s


def structure_demand_kg(ctx: MassContext) -> float:
    """Primary structure: chunk-scaled backbone + max-load term (SCOPE form).

    max_load_kN here is the electric-thruster steady load (thrust_n / 1000),
    which is negligible (<= 0.025 kN at 25 N). Chemical impulsive burn loads are
    NOT modeled as a force in the framework; structure is therefore chunk-
    dominated. Flagged for the fidelity follow-on.
    """
    max_load_kn = ctx.electric_thrust_n / 1000.0
    return 0.05 * ctx.chunk_mass_kg + 100.0 * max_load_kn


def comms_demand_kg(ctx: MassContext) -> float:
    """Communications + guidance + computer floor (invariant deep-space minimum)."""
    return ctx.comms_floor_kg


def tankage_demand_kg(propellant_kg: float) -> float:
    """Propellant tankage: 5 percent of propellant mass (SCOPE anchor).

    This is the only dry-mass -> propellant -> dry-mass coupling, and the term
    that makes the fixed point non-trivial. propellant_kg is itself a function
    of the trial dry mass via launch_wet_and_propellant.
    """
    return 0.05 * propellant_kg


# -------------------------------------------------------------------- #
# Demand function + derivation
# -------------------------------------------------------------------- #

def make_saturn_demand_fn(ctx: MassContext) -> DemandFn:
    """Build the demand_fn(dry_mass_kg) -> {subsystem: kg} for `ctx`.

    All terms except tankage are independent of the trial dry mass. Tankage is
    computed from the launch propellant implied by the trial dry mass and the
    propellant fraction (payload is zero at launch, so wet = dry + propellant).
    """
    f = ctx.propellant_fraction
    fixed: Dict[str, float] = {
        KEY_POWERPLANT: powerplant_demand_kg(ctx),
        KEY_BUS: ctx.bus_mass_floor_kg,
        KEY_CAPTURE: capture_demand_kg(ctx),
        KEY_TPS: tps_demand_kg(ctx),
        KEY_STRUCTURE: structure_demand_kg(ctx),
        KEY_COMMS: comms_demand_kg(ctx),
    }

    def demand_fn(dry_mass_kg: float) -> Dict[str, float]:
        # propellant = f/(1-f) * dry at launch (payload = 0)
        propellant = (f / (1.0 - f)) * dry_mass_kg
        out = dict(fixed)
        out[KEY_TANKAGE] = tankage_demand_kg(propellant)
        return out

    return demand_fn


def derive_saturn_vehicle(
    ctx: MassContext,
    initial_guess_kg: float = 50_000.0,
    tol: float = 1e-3,
    max_iter: int = 50,
) -> DerivationResult:
    """Solve the self-consistent Saturn vehicle dry mass for `ctx`."""
    return derive_dry_mass(
        make_saturn_demand_fn(ctx),
        initial_guess_kg=initial_guess_kg,
        dry_margin=ctx.dry_margin,
        tol=tol,
        max_iter=max_iter,
    )
