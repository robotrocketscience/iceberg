"""Closed-loop vehicle dry-mass derivation (R-vehicle-mass-closure-refactor).

The open-loop framework treats vehicle dry mass as a sweep boundary condition:
the sweep picks `VehicleState.mass_kg`, the walker walks forward, and nothing
checks that the assumed mass is consistent with the dry-mass *demands* the
chosen subsystems impose. That lets a 10-tonne-dry vehicle "close" while
carrying a 30-kilowatt-electric reactor it physically cannot contain.

This module supplies the generic machinery to make dry mass a *derived*
quantity: a demand function reports each subsystem's mass for a trial dry
mass, and a fixed-point iterator solves for the self-consistent dry mass.
The coupling that makes the iteration non-trivial is that some subsystems
(tankage especially) scale with propellant load, which scales with the
launch wet mass, which scales with the dry mass.

Layering: this module is framework-level and mission-agnostic. It knows
nothing about Saturn, reactors, or trawls. The concrete subsystem demand
functions live in `missions/` (e.g. `missions/saturn_mass_demands.py`),
where they may reuse mission-specific anchors such as
`powerplant_constraints.required_powerplant_mass_kg`. The iterator here only
sees a `demand_fn(dry_mass_kg) -> {subsystem: kg}` callable.

Non-convergence is a first-class result, not an error to be clipped. A demand
function whose fixed-point map is not a contraction (for example, an extreme
propellant fraction where tankage growth outruns the dry-mass it is added to)
returns `converged=False`. That is the correct answer for a self-inconsistent
design choice (SCOPE open-coordination note).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, Mapping, Tuple


# A demand function maps a trial dry mass (kg) to a per-subsystem mass
# breakdown (kg). It closes over whatever mission context it needs.
DemandFn = Callable[[float], Mapping[str, float]]


@dataclass(frozen=True)
class DerivationResult:
    """Outcome of a dry-mass fixed-point solve.

    dry_mass_kg     -- self-consistent vehicle dry mass (last iterate; only
                       meaningful when `converged` is True, but always populated
                       with the last value so callers can inspect divergence).
    converged       -- True iff the relative step fell below `tol` within
                       `max_iter` iterations and the iterate stayed finite.
    iterations      -- number of fixed-point steps actually taken.
    breakdown       -- per-subsystem mass (kg) evaluated at the final dry mass,
                       BEFORE the dry margin is applied. Sums to
                       dry_mass_kg / (1 + dry_margin) when converged.
    dry_margin      -- the margin fraction used (echoed for report tables).
    nonconvergence_reason -- short human string when not converged, else "".
    """

    dry_mass_kg: float
    converged: bool
    iterations: int
    breakdown: Mapping[str, float]
    dry_margin: float
    nonconvergence_reason: str = ""

    @property
    def subsystem_subtotal_kg(self) -> float:
        return sum(self.breakdown.values())


# Solver guard rails. A dry mass above this ceiling (1000 t) is taken as
# divergence regardless of step size — no plausible single vehicle dry mass
# is a kilotonne, so a map climbing past it is not contracting.
_DIVERGENCE_CEILING_KG = 1_000_000.0


def derive_dry_mass(
    demand_fn: DemandFn,
    initial_guess_kg: float = 50_000.0,
    dry_margin: float = 0.20,
    tol: float = 1e-3,
    max_iter: int = 50,
) -> DerivationResult:
    """Solve dry_mass = (1 + dry_margin) * sum(demand_fn(dry_mass)).

    Plain fixed-point (Picard) iteration. `demand_fn(D)` returns the subsystem
    breakdown for a trial dry mass D; the next iterate is the margined sum.
    Converges when the relative change between iterates is below `tol`.

    Returns a DerivationResult. `converged=False` is returned (not raised) when:
      - the iterate exceeds the divergence ceiling (map is not contracting), or
      - `max_iter` is reached without the relative step falling below `tol`.

    Args:
        demand_fn: trial-dry-mass -> {subsystem_name: mass_kg}.
        initial_guess_kg: starting dry mass for the iteration.
        dry_margin: fractional margin applied to the subsystem subtotal
            (0.20 = NASA Class-B design margin per SCOPE).
        tol: relative-change convergence threshold.
        max_iter: iteration cap before declaring non-convergence.

    Raises:
        ValueError: on non-positive initial guess or negative margin/tol — these
            are programming errors, distinct from physical non-convergence.
    """
    if initial_guess_kg <= 0:
        raise ValueError(f"initial_guess_kg must be > 0, got {initial_guess_kg}")
    if dry_margin < 0:
        raise ValueError(f"dry_margin must be >= 0, got {dry_margin}")
    if tol <= 0:
        raise ValueError(f"tol must be > 0, got {tol}")
    if max_iter < 1:
        raise ValueError(f"max_iter must be >= 1, got {max_iter}")

    dry = float(initial_guess_kg)
    breakdown: Dict[str, float] = {}

    for it in range(1, max_iter + 1):
        raw = demand_fn(dry)
        breakdown = {k: float(v) for k, v in raw.items()}
        subtotal = sum(breakdown.values())
        if subtotal < 0:
            return DerivationResult(
                dry_mass_kg=dry,
                converged=False,
                iterations=it,
                breakdown=breakdown,
                dry_margin=dry_margin,
                nonconvergence_reason=f"negative subsystem subtotal {subtotal:.1f} kg",
            )
        new_dry = (1.0 + dry_margin) * subtotal

        if new_dry > _DIVERGENCE_CEILING_KG:
            return DerivationResult(
                dry_mass_kg=new_dry,
                converged=False,
                iterations=it,
                breakdown=breakdown,
                dry_margin=dry_margin,
                nonconvergence_reason=(
                    f"dry mass {new_dry / 1000.0:.0f} t exceeded divergence ceiling "
                    f"{_DIVERGENCE_CEILING_KG / 1000.0:.0f} t (map not contracting; "
                    f"propellant/tankage coupling likely unstable)"
                ),
            )

        rel_step = abs(new_dry - dry) / dry if dry > 0 else float("inf")
        dry = new_dry
        if rel_step < tol:
            # Re-evaluate the breakdown at the converged dry mass so it is
            # exactly consistent with the reported dry_mass_kg.
            raw = demand_fn(dry)
            breakdown = {k: float(v) for k, v in raw.items()}
            return DerivationResult(
                dry_mass_kg=dry,
                converged=True,
                iterations=it,
                breakdown=breakdown,
                dry_margin=dry_margin,
                nonconvergence_reason="",
            )

    return DerivationResult(
        dry_mass_kg=dry,
        converged=False,
        iterations=max_iter,
        breakdown=breakdown,
        dry_margin=dry_margin,
        nonconvergence_reason=f"did not reach tol={tol} within max_iter={max_iter}",
    )


def launch_wet_and_propellant(dry_mass_kg: float, propellant_fraction: float) -> Tuple[float, float]:
    """Launch wet mass and propellant from dry mass at a fixed propellant fraction.

    At launch payload is zero, so wet = dry + propellant and
    propellant = propellant_fraction * wet. Hence:
        wet = dry / (1 - propellant_fraction)
        propellant = propellant_fraction * wet

    This preserves the existing sweep convention (`_scale_propellant`,
    PROPELLANT_FRACTION = 0.80) so the closed-loop refactor changes only how
    dry mass is obtained, not the chunk-as-propellant-tank physics (SCOPE
    out-of-scope item). Re-deriving propellant from the delta-v schedule is a
    follow-on round.

    Raises:
        ValueError: if propellant_fraction is not in [0, 1).
    """
    if not (0.0 <= propellant_fraction < 1.0):
        raise ValueError(
            f"propellant_fraction must be in [0, 1), got {propellant_fraction}"
        )
    wet = dry_mass_kg / (1.0 - propellant_fraction)
    propellant = propellant_fraction * wet
    return wet, propellant
