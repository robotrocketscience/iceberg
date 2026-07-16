"""Nozzle expansion thermodynamics for water-propellant electrothermal thrusters.

Pure-physics functions: no I/O, no plotting. Study runners under ../studies/
import these and own their own CLI, sweeps, and output paths.

Two expansion limits, both isentropic from chamber to exit pressure:

  expand_equilibrium  — composition re-equilibrates chemically at each step
                        of the expansion. Releases dissociation enthalpy
                        back into kinetic energy. Optimistic (upper) bound.

  expand_frozen       — composition held at the chamber-equilibrium values
                        throughout the expansion. Dissociation enthalpy is
                        carried out as chemical potential. Conservative
                        (lower) bound.

Real-world performance lies between these bounds, biased toward `frozen` at
low chamber pressure (slow recombination kinetics) and toward `equilibrium`
at high chamber pressure (fast kinetics). The gap is the canonical
"frozen-flow penalty" that bounds water-MET Isp.
"""

from __future__ import annotations

import numpy as np
import cantera as ct
from scipy.optimize import brentq

from ..constants import G0


# Default chemistry mechanism. h2o2.yaml ships with Cantera and includes
# H2O, H2, O2, H, O, OH, HO2, H2O2 — sufficient for water dissociation
# below the ionization threshold (~10,000 K). Above ~10,000 K, an
# ionization-aware mechanism would be needed (electrons, H+, O+, etc.).
DEFAULT_MECHANISM = "h2o2.yaml"


def isp_from_v_e(v_e: float) -> float:
    """Convert exhaust velocity (m/s) to specific impulse (s)."""
    return v_e / G0


def v_e_from_isp(isp: float) -> float:
    """Convert specific impulse (s) to exhaust velocity (m/s)."""
    return isp * G0


def chamber_state(
    T_c: float,
    P_c_pa: float,
    inlet_species: str = "H2O:1",
    mechanism: str = DEFAULT_MECHANISM,
) -> tuple[ct.Solution, float, float]:
    """Set up the chamber as an HP-equilibrated gas.

    Args:
        T_c:           Initial temperature (K).
        P_c_pa:        Chamber pressure (Pa).
        inlet_species: Cantera composition string for the propellant feed
                       before equilibration. Default is pure water vapor.
        mechanism:     Cantera mechanism YAML name.

    Returns:
        (gas, h_chamber, s_chamber) — the equilibrated Cantera Solution, its
        mass-specific enthalpy (J/kg), and its mass-specific entropy
        (J/kg/K). Energy and entropy are the chamber reference values used
        by the expansion routines below.
    """
    gas = ct.Solution(mechanism)
    gas.TPX = T_c, P_c_pa, inlet_species
    gas.equilibrate("HP")
    return gas, gas.enthalpy_mass, gas.entropy_mass


def expand_equilibrium(
    T_c: float,
    P_c_pa: float,
    P_exit_pa: float,
    n_steps: int = 200,
    mechanism: str = DEFAULT_MECHANISM,
) -> tuple[float, float, float]:
    """Shifting-equilibrium isentropic expansion from chamber to exit pressure.

    At each pressure step, the gas re-equilibrates chemically at constant
    entropy. This is the upper bound on real performance (every J of
    dissociation enthalpy gets converted back to kinetic energy in the
    nozzle).

    Args:
        T_c:        Chamber temperature (K).
        P_c_pa:     Chamber pressure (Pa).
        P_exit_pa:  Exit pressure (Pa). Use ~1 Pa for vacuum approximation.
        n_steps:    Number of log-spaced pressure steps for the integration.
        mechanism:  Cantera mechanism.

    Returns:
        (Isp, T_exit, v_e) — specific impulse (s), exit temperature (K),
        exhaust velocity (m/s).
    """
    gas, h_c, s_c = chamber_state(T_c, P_c_pa, mechanism=mechanism)
    pressures = np.geomspace(P_c_pa, P_exit_pa, n_steps)
    for p in pressures[1:]:
        gas.SP = s_c, p
        gas.equilibrate("SP")
    h_exit = gas.enthalpy_mass
    v_e = float(np.sqrt(max(0.0, 2.0 * (h_c - h_exit))))
    return isp_from_v_e(v_e), float(gas.T), v_e


def expand_frozen(
    T_c: float,
    P_c_pa: float,
    P_exit_pa: float,
    mechanism: str = DEFAULT_MECHANISM,
) -> tuple[float, float, float]:
    """Frozen-flow isentropic expansion: composition held at chamber equilibrium.

    The mole fractions equilibrated at chamber conditions are held fixed
    through the expansion; only temperature and density change. Entropy is
    conserved. This is the lower bound on real performance (no
    recombination enthalpy is recovered).

    Args:
        T_c:        Chamber temperature (K).
        P_c_pa:     Chamber pressure (Pa).
        P_exit_pa:  Exit pressure (Pa).
        mechanism:  Cantera mechanism.

    Returns:
        (Isp, T_exit, v_e). Returns (nan, nan, nan) if the entropy
        residual cannot be bracketed (a sign the chamber conditions are
        outside the mechanism's validity range).
    """
    gas, h_c, s_c = chamber_state(T_c, P_c_pa, mechanism=mechanism)
    X_chamber = gas.X.copy()

    def entropy_residual(T_trial: float) -> float:
        gas.TPX = T_trial, P_exit_pa, X_chamber
        return gas.entropy_mass - s_c

    T_lo, T_hi = 100.0, T_c - 1.0
    if entropy_residual(T_lo) * entropy_residual(T_hi) > 0:
        return float("nan"), float("nan"), float("nan")

    T_exit = brentq(entropy_residual, T_lo, T_hi, xtol=0.01)
    gas.TPX = T_exit, P_exit_pa, X_chamber
    h_exit = gas.enthalpy_mass
    v_e = float(np.sqrt(max(0.0, 2.0 * (h_c - h_exit))))
    return isp_from_v_e(v_e), float(T_exit), v_e
