"""Powerplant constraints shared across phase executors.

R-framework-matrix-parity (titan-4, 2026-05-22). Encodes the matrix-carried
constraints that the framework did not previously model. Every constraint is
OFF by default (non-binding) and turns ON only when the relevant param is set,
so the 121 framework tests and the constraints-off sweep reproduce the
pre-encoding baseline (runs/20260522T193231Z) exactly.

Constraint 1 — reactor lifetime vs cumulative full-power burn.
  electric_burn_hours() gives the reactor ON-time for one electric burn.
  lifetime_ok() rejects an electric option when projected cumulative burn would
  exceed params['reactor_lifetime_years'] * 8760 h. Ground truth: enceladus-r5
  R-reactor-lifetime-vs-burn-time (KRUSTY 28-h heritage; Kilopower 10-yr design
  target; ~11-12 yr cumulative burn at the megawatt cells it falsified).

Constraints 2 + 3 — powerplant + bus dry-mass floor.
  required_dry_mass_kg() is the minimum vehicle dry mass that must contain bus
  (constraint 3, conservative 2000 kg anchor) + reactor (constraint 2,
  power_kwe / specific_power) + MARVL bundled radiator (constraint 2,
  5 t + 0.1 t/kWe per locked belief 0418e2c9) + thrusters (10 kg/kWe per
  titan-3 R-chunk-size-pareto). Charged as a precondition: a vehicle whose dry
  mass cannot contain its own powerplant is infeasible. OFF unless
  params['enforce_mass_floor'] is True.
"""

from __future__ import annotations

import math

from ..framework import VehicleState


HOURS_PER_YEAR = 8760.0
G0 = 9.80665


# -------------------------------------------------------------------- #
# Constraint 1 — reactor lifetime
# -------------------------------------------------------------------- #

def electric_burn_hours(propellant_burned_kg: float, isp_s: float, power_kwe: float) -> float:
    """Reactor full-power ON time for one electric burn, in hours.

    Uses the framework's thrust-from-power convention F = 2*P/v_e (same factor
    as phase1/phase4 derived thrust), so burn time = m_prop * v_e / F =
    m_prop * v_e^2 / (2 * P_elec). Returns 0 for non-electric / zero-power legs.
    """
    if power_kwe <= 0 or propellant_burned_kg <= 0:
        return 0.0
    v_e = isp_s * G0  # m/s
    thrust_n = 2.0 * power_kwe * 1000.0 / v_e
    burn_s = propellant_burned_kg * v_e / thrust_n
    return burn_s / 3600.0


def lifetime_ok(state: VehicleState, params, this_burn_hours: float) -> tuple[bool, str]:
    """Feasibility of an electric option under the reactor-lifetime ceiling.

    Non-binding (always True) when params['reactor_lifetime_years'] is absent or
    infinite — the default, which preserves the constraints-off baseline.
    """
    lifetime_years = params.get("reactor_lifetime_years", math.inf)
    if lifetime_years == math.inf:
        return (True, "feasible")
    ceiling_hours = lifetime_years * HOURS_PER_YEAR
    projected = state.cumulative_full_power_burn_hours + this_burn_hours
    if projected > ceiling_hours:
        return (
            False,
            f"cumulative reactor burn {projected / HOURS_PER_YEAR:.2f} yr exceeds "
            f"reactor lifetime {lifetime_years:.0f} yr "
            f"(constraint 1; enceladus-r5 R-reactor-lifetime-vs-burn-time)",
        )
    return (True, "feasible")


# -------------------------------------------------------------------- #
# Constraints 2 + 3 — powerplant + bus dry-mass floor
# -------------------------------------------------------------------- #

def required_powerplant_mass_kg(power_kwe: float, params) -> float:
    """Reactor + MARVL bundled radiator + thruster mass for a power class, kg.

    Constraint 2. Charged on power_available_kwe — exact for the pure-reactor
    classes (K1/K10/K30, which are the matrix-parity cells) and conservative
    (over-charging) for the hybrid reactor+solar classes, since the framework
    does not yet split reactor from solar-panel mass. Bus mass is added
    separately by constraint 3 in required_dry_mass_kg().

      reactor  = power_kwe / specific_power            (titan-3 R-chunk-size-pareto)
      radiator = 5 t + 0.1 t/kWe                       (MARVL bundled, locked 0418e2c9)
      thrusters = 10 kg/kWe                            (titan-3)
    """
    sp = params.get("reactor_specific_power_w_per_kg", 2.4)  # KRUSTY-measured default
    reactor_kg = power_kwe * 1000.0 / sp
    radiator_kg = 5000.0 + power_kwe * 100.0
    thrusters_kg = 10.0 * power_kwe
    return reactor_kg + radiator_kg + thrusters_kg


def required_dry_mass_kg(power_kwe: float, params) -> float:
    """Minimum vehicle dry mass: bus (constraint 3) + powerplant (constraint 2).

    Constraint 3 — conservative bus-mass anchor. The matrix basis-of-record per
    latest+12 retraction is a ~2000 kg conservative bus, NOT the ~600 kg heritage
    Cassini bus. Overridable via params['bus_mass_floor_kg']. Returns 0 when
    mass-floor charging is off (default), preserving the constraints-off baseline.
    """
    if not params.get("enforce_mass_floor", False):
        return 0.0
    bus_kg = params.get("bus_mass_floor_kg", 2000.0)  # conservative anchor (Cassini heritage ~600 kg)
    return bus_kg + required_powerplant_mass_kg(power_kwe, params)


def mass_floor_ok(state: VehicleState, params) -> tuple[bool, str]:
    """Reject a vehicle whose dry mass cannot contain its own powerplant (+ bus).

    Dry mass = mass - propellant - payload. Evaluated at the post-assembly,
    pre-chunk-acquisition state (Phase 1). OFF unless params['enforce_mass_floor']
    is True, preserving the constraints-off baseline.
    """
    if not params.get("enforce_mass_floor", False):
        return (True, "feasible")
    dry_kg = state.mass_kg - state.propellant_kg - state.payload_kg
    required_kg = required_dry_mass_kg(state.power_available_kwe, params)
    if dry_kg < required_kg:
        return (
            False,
            f"vehicle dry mass {dry_kg / 1000.0:.1f} t cannot contain its "
            f"{required_kg / 1000.0:.1f} t bus + powerplant at "
            f"{state.power_available_kwe:.0f} kWe (constraints 2+3; "
            f"bus + reactor + MARVL radiator + thrusters)",
        )
    return (True, "feasible")
