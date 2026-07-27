"""Near-Earth-asteroid vehicle subsystem mass-demand functions (closed-loop).

The near-Earth-asteroid (NEA) analogue of `saturn_mass_demands.py`. Consumed by
the SAME mission-agnostic `framework.dry_mass.derive_dry_mass` fixed-point
iterator — that reuse is the framework-abstraction test (R-near-earth-asteroid
H6). Only the mission-specific demand functions change between architectures.

THE LOAD-BEARING DIFFERENCE FROM SATURN — powerplant:

  Saturn (`saturn_mass_demands.powerplant_demand_kg`) charges a *fission*
  powerplant via `required_powerplant_mass_kg`: reactor at KRUSTY 2.4 W/kg +
  MARVL bundled radiator (5 t + 0.1 t/kWe) + thrusters. At 40 kWe that is
  ~26 t, which is why titan-6's closed-loop Saturn inventory is 0/150 (the
  vehicle is lighter than its own reactor).

  NEA operates at ~1 AU, where the Keck Institute for Space Studies 2012
  reference architecture uses 40-kWe-class SOLAR-electric propulsion. Flight
  roll-out solar arrays run ~100-200 W/kg (ROSA ~150 W/kg). A 40-kWe solar
  powerplant is ~0.27 t of array + PMAD + thrusters ~ 0.7-1 t total — roughly
  25-35x lighter than the fission stack. No Brayton/Stirling waste-heat radiator
  is needed (PV is direct-conversion; only modest PMAD thermal). This is the
  axis on which NEA closes the closed-loop mass fixed point where Saturn cannot.

All other anchors are first-pass and bounded (saturn_mass_demands convention).
Boulder is processed in situ and water is returned as payload (variant (b));
the whole-boulder-retrieval Keck literal (variant (a)) is noted in RESULTS.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from ..framework import DemandFn, DerivationResult, derive_dry_mass


# Subsystem keys (stable; report tables / tests join on these).
KEY_SOLAR = "solar_powerplant"        # PV array + PMAD (replaces fission+MARVL)
KEY_THRUSTERS = "sep_thrusters"       # solar-electric thrusters
KEY_CAPTURE = "boulder_acquisition"   # confinement bag / arms / anchoring
KEY_EXTRACTION = "thermal_extraction" # heat + condense bound water (400-700 C)
KEY_STRUCTURE = "primary_structure"   # tug backbone, boulder-load driven
KEY_COMMS = "comms_guidance_computer" # 1 AU: light vs Saturn 9 AU
KEY_RETURN = "return_capsule"
KEY_TANKAGE = "tankage"


@dataclass(frozen=True)
class NeaMassContext:
    """Inputs to the NEA vehicle dry-mass derivation for one cell.

    Swept per cell: boulder_mass_kg, power_available_kwe.
    Held: solar specific power, PMAD, extraction/capture/structure/comms anchors,
    propellant fraction, dry margin.
    """

    boulder_mass_kg: float
    power_available_kwe: float = 40.0          # Keck KISS solar-electric class

    solar_specific_power_w_per_kg: float = 150.0  # ROSA-class flight array
    pmad_kg_per_kwe: float = 3.0                  # power mgmt + distribution + modest thermal
    thrusters_kg_per_kwe: float = 10.0            # SEP thrusters (titan-3 anchor, reused)

    # Boulder-driven subsystem coefficients (first-pass; fidelity follow-on).
    capture_fixed_kg: float = 1000.0
    capture_per_boulder: float = 0.02            # confinement/anchoring scales weakly with boulder
    extraction_fixed_kg: float = 2000.0
    extraction_per_boulder: float = 0.010        # processing plant throughput
    structure_per_boulder: float = 0.030         # tug backbone to react boulder load
    comms_floor_kg: float = 500.0                # 1 AU deep-space minimum (vs Saturn 2000)
    return_capsule_kg: float = 500.0

    # SEP at high Isp + modest NEA dv -> low propellant fraction (vs Saturn 0.80).
    propellant_fraction: float = 0.45
    tankage_frac_of_propellant: float = 0.08     # xenon high-pressure tankage
    dry_margin: float = 0.20                      # NASA Class-B


# -------------------------------------------------------------------- #
# Per-subsystem demand forms (kg).
# -------------------------------------------------------------------- #

def solar_powerplant_demand_kg(ctx: NeaMassContext) -> float:
    """Solar PV array + PMAD for the SEP power class (the load-bearing term).

    array  = power_kwe * 1000 / solar_specific_power   (W / (W/kg) = kg)
    pmad   = pmad_kg_per_kwe * power_kwe
    NO fission reactor, NO MARVL waste-heat radiator (PV is direct-conversion).
    """
    array_kg = ctx.power_available_kwe * 1000.0 / ctx.solar_specific_power_w_per_kg
    pmad_kg = ctx.pmad_kg_per_kwe * ctx.power_available_kwe
    return array_kg + pmad_kg


def thrusters_demand_kg(ctx: NeaMassContext) -> float:
    return ctx.thrusters_kg_per_kwe * ctx.power_available_kwe


def capture_demand_kg(ctx: NeaMassContext) -> float:
    return ctx.capture_fixed_kg + ctx.capture_per_boulder * ctx.boulder_mass_kg


def extraction_demand_kg(ctx: NeaMassContext) -> float:
    """Thermal-extraction plant (400-700 C bound-water release), throughput-sized."""
    return ctx.extraction_fixed_kg + ctx.extraction_per_boulder * ctx.boulder_mass_kg


def structure_demand_kg(ctx: NeaMassContext) -> float:
    """Primary structure / tug backbone, sized by the boulder load it reacts."""
    return ctx.structure_per_boulder * ctx.boulder_mass_kg


def comms_demand_kg(ctx: NeaMassContext) -> float:
    return ctx.comms_floor_kg


def tankage_demand_kg(propellant_kg: float, ctx: NeaMassContext) -> float:
    """Propellant tankage: the only dry->propellant->dry coupling (fixed point)."""
    return ctx.tankage_frac_of_propellant * propellant_kg


# -------------------------------------------------------------------- #
# Demand function + derivation
# -------------------------------------------------------------------- #

def make_nea_demand_fn(ctx: NeaMassContext) -> DemandFn:
    """Build demand_fn(dry_mass_kg) -> {subsystem: kg} for `ctx`.

    All terms except tankage are independent of the trial dry mass. Tankage is
    computed from the launch propellant implied by the trial dry mass and the
    propellant fraction (payload zero at launch: wet = dry + propellant).
    """
    f = ctx.propellant_fraction
    fixed: Dict[str, float] = {
        KEY_SOLAR: solar_powerplant_demand_kg(ctx),
        KEY_THRUSTERS: thrusters_demand_kg(ctx),
        KEY_CAPTURE: capture_demand_kg(ctx),
        KEY_EXTRACTION: extraction_demand_kg(ctx),
        KEY_STRUCTURE: structure_demand_kg(ctx),
        KEY_COMMS: comms_demand_kg(ctx),
        KEY_RETURN: ctx.return_capsule_kg,
    }

    def demand_fn(dry_mass_kg: float) -> Dict[str, float]:
        propellant = (f / (1.0 - f)) * dry_mass_kg
        out = dict(fixed)
        out[KEY_TANKAGE] = tankage_demand_kg(propellant, ctx)
        return out

    return demand_fn


def derive_nea_vehicle(
    ctx: NeaMassContext,
    initial_guess_kg: float = 20_000.0,
    tol: float = 1e-3,
    max_iter: int = 50,
) -> DerivationResult:
    """Solve the self-consistent NEA vehicle dry mass for `ctx`."""
    return derive_dry_mass(
        make_nea_demand_fn(ctx),
        initial_guess_kg=initial_guess_kg,
        dry_margin=ctx.dry_margin,
        tol=tol,
        max_iter=max_iter,
    )


# -------------------------------------------------------------------- #
# Delivered-water + powerplant-floor helpers (used by the round harness)
# -------------------------------------------------------------------- #

def delivered_water_kg(boulder_mass_kg: float, water_fraction: float,
                       extraction_efficiency: float) -> float:
    """Water returned to LEO = boulder mass x bound-water fraction x extraction eff.

    In-situ processing (variant b): the boulder is processed at the asteroid and
    water is the returned payload. Encoded straight from inputs (re-derive-from-
    inputs lesson); no hidden amplification factor.
    """
    return boulder_mass_kg * water_fraction * extraction_efficiency
