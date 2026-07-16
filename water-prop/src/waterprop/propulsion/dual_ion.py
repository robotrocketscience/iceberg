"""Dual-ion (hydrogen-ion + oxygen-ion) electric propulsion model.

Architecture: water is electrolyzed on board. The hydrogen and oxygen
streams feed two parallel gridded-ion thrusters running at the same grid
voltage. Both streams are ionized (singly-charged) and accelerated
electrostatically.

Key advantage versus pure-hydrogen-ion-with-oxygen-vented:
  100 percent of the chunk mass produces thrust (vs 11 percent if hydrogen
  alone is used and oxygen is vented). At equal grid voltage, the heavier
  oxygen ion has lower exhaust velocity, but the mass-weighted specific
  impulse is still well above any single-tech water option, and the
  chunk-delivery fraction is dramatically higher.

Key disadvantages, not modeled here, captured in the round's STUDY.md:
  - Oxygen-ion grid erosion. Pure oxygen-ion beams chemically attack every
    standard grid material (molybdenum, carbon, titanium). The mixed-water-
    plasma ion thruster grid-life problem (risk C02) is worse for pure
    oxygen-ion.
  - Required electrical power for ICEBERG-class thrust is ~200 kilowatts at
    1 kilovolt grid voltage. Sub-megawatt to megawatt-class reactor.
  - System complexity: electrolyzer plus two ion thrusters plus separate
    feed systems.

References to verify in a later round:
  - Jahn, Physics of Electric Propulsion (1968) -- chapter on
    electrostatic acceleration; pure-species ion-thruster v_e and specific
    impulse formulas.
  - For oxygen-ion grid erosion: research-stage; no flight heritage. The
    closest analog is oxygen-augmented xenon thruster work; nothing
    flight-qualified for pure oxygen-ion.
"""

from __future__ import annotations

import numpy as np

# Fundamental constants
AMU_KG = 1.66053906660e-27           # kilograms per atomic mass unit
E_CHARGE = 1.602176634e-19           # coulomb (elementary charge)
G0 = 9.80665                          # meters per second squared

# Ion masses
H_MASS_AMU = 1.00784                 # hydrogen atom
H2_MASS_AMU = 2.01588                # diatomic hydrogen
O_MASS_AMU = 15.999                  # oxygen atom
O2_MASS_AMU = 31.998                 # diatomic oxygen
H2O_MASS_AMU = 18.01528              # water molecule

# Mass fractions in water
MASS_FRAC_H_IN_WATER = 2 * H_MASS_AMU / H2O_MASS_AMU      # 0.1119
MASS_FRAC_O_IN_WATER = O_MASS_AMU / H2O_MASS_AMU          # 0.8881


def ion_exhaust_velocity_m_s(ion_mass_amu: float, grid_voltage_V: float,
                              charge_state: int = 1) -> float:
    """Exhaust velocity for an ion of given mass and charge state accelerated
    through a grid voltage.

      v_e = sqrt(2 * q * V / m)

    where q is the ion charge (charge_state * electron charge) and m is the
    ion mass.
    """
    m_kg = ion_mass_amu * AMU_KG
    q = charge_state * E_CHARGE
    return float(np.sqrt(2.0 * q * grid_voltage_V / m_kg))


def dual_ion_isp_s(grid_voltage_V: float,
                   use_h2_plus: bool = False) -> dict:
    """Mass-weighted specific impulse for a dual-ion architecture fed by
    electrolyzed water.

    Args:
      grid_voltage_V: same accelerating voltage for both species
      use_h2_plus: if True, accelerate H2+ ions (mass 2) instead of H+
                   (mass 1). H2+ is more realistic for a real ion thruster
                   because dissociating H2 -> 2H requires another step
                   beyond ionization. Reduces hydrogen-ion specific
                   impulse by sqrt(2).

    Returns:
      dict with per-species exhaust velocities, mass-weighted average
      specific impulse, and the relative jet-power-per-mass split.
    """
    h_ion_mass = H2_MASS_AMU if use_h2_plus else H_MASS_AMU
    v_e_H = ion_exhaust_velocity_m_s(h_ion_mass, grid_voltage_V)
    v_e_O = ion_exhaust_velocity_m_s(O_MASS_AMU, grid_voltage_V)

    # Mass-flow-weighted average exhaust velocity (thrust over mass flow).
    fH = MASS_FRAC_H_IN_WATER
    fO = MASS_FRAC_O_IN_WATER
    v_e_avg = fH * v_e_H + fO * v_e_O
    isp_avg = v_e_avg / G0

    # Power split: jet power per kilogram per second flow of water.
    p_per_kg_H = 0.5 * v_e_H ** 2
    p_per_kg_O = 0.5 * v_e_O ** 2
    p_per_kg_water_jet = fH * p_per_kg_H + fO * p_per_kg_O

    return {
        "grid_voltage_V": grid_voltage_V,
        "h_ion_mass_amu": h_ion_mass,
        "v_e_H_m_s": v_e_H,
        "v_e_O_m_s": v_e_O,
        "v_e_avg_m_s": v_e_avg,
        "isp_avg_s": isp_avg,
        "isp_H_s": v_e_H / G0,
        "isp_O_s": v_e_O / G0,
        "jet_power_per_kg_water_W": p_per_kg_water_jet,
    }


def dual_ion_thrust_per_kw(grid_voltage_V: float,
                            efficiency_total: float = 0.4,
                            use_h2_plus: bool = False) -> dict:
    """Thrust delivered per kilowatt of electrical power for a dual-ion
    thruster.

    For each species: F_i = m_dot_i * v_e_i. Total thrust is the sum.
    Jet power: P_jet_i = 0.5 * m_dot_i * v_e_i^2 = 0.5 * F_i * v_e_i.
    Electrical power: P_elec_i = P_jet_i / efficiency.

    For a given total electrical power split proportionally by mass flow
    (i.e., both thrusters running on the same water electrolysis output),
    the ratio of mass flows is fixed at MASS_FRAC_H_IN_WATER : MASS_FRAC_O_IN_WATER.

    Returns thrust per kilowatt electrical and the equivalent specific
    impulse from the thrust-power identity F = 2 eta P / v_e.
    """
    result = dual_ion_isp_s(grid_voltage_V, use_h2_plus=use_h2_plus)
    v_e_avg = result["v_e_avg_m_s"]

    # F = 2 eta P / v_e, where v_e is the mass-weighted exit velocity.
    # This is exact when both streams share the same total efficiency.
    thrust_per_w = 2.0 * efficiency_total / v_e_avg     # newtons per watt
    thrust_per_kw = thrust_per_w * 1000.0                # newtons per kilowatt

    result["efficiency_total"] = efficiency_total
    result["thrust_per_kw_electrical_N"] = thrust_per_kw
    return result


def delivery_fraction_chunk_fed(isp_s: float,
                                 delta_v_km_s: float) -> float:
    """For a chunk-fed propulsion architecture where the chunk is also the
    propellant tank: what fraction of the starting chunk mass is delivered
    after a burn of magnitude delta_v at given specific impulse?

    Tsiolkovsky: m_final / m_initial = exp(-delta_v / v_e).

    For a purely chunk-fed leg (no separate dry-mass overhead in this
    calculation), the delivered fraction equals m_final / m_initial.
    """
    v_e_m_s = isp_s * G0
    return float(np.exp(-delta_v_km_s * 1000.0 / v_e_m_s))
