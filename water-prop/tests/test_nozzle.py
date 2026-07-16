"""Sanity tests for waterprop.thermo.nozzle.

These are not unit tests in the strict sense — they verify physical sanity
of the nozzle expansion functions across regimes. Slow (Cantera is heavy);
not intended to run in tight loops.
"""

import math

import numpy as np
import pytest

from waterprop.constants import G0, TORR_TO_PA
from waterprop.thermo import (
    chamber_state,
    expand_equilibrium,
    expand_frozen,
    isp_from_v_e,
    v_e_from_isp,
)


def test_isp_v_e_roundtrip():
    """Isp <-> v_e conversions invert exactly."""
    for isp in [100.0, 500.0, 1000.0, 5000.0]:
        assert math.isclose(isp_from_v_e(v_e_from_isp(isp)), isp, rel_tol=1e-12)


def test_chamber_dissociation_at_high_T():
    """At chamber T=8000 K, water should be substantially dissociated."""
    gas, _, _ = chamber_state(T_c=8000.0, P_c_pa=100 * TORR_TO_PA)
    h2o_frac = gas["H2O"].X[0]
    # At 8000 K and 100 torr, equilibrium H2O mole fraction should be much
    # less than the inlet value of 1.0 -- most of the water dissociates.
    assert h2o_frac < 0.3, f"expected major dissociation, got X_H2O={h2o_frac}"


def test_equilibrium_geq_frozen():
    """Equilibrium-expansion Isp must be >= frozen-flow Isp at the same chamber state.

    This is a physical-bound check: recombination releases enthalpy that
    frozen flow leaves on the table. Violation means a numerical bug.
    """
    P_exit = 1.0
    for T_c in [4000.0, 6000.0, 8000.0]:
        for P_c_torr in [10.0, 100.0]:
            P_c = P_c_torr * TORR_TO_PA
            isp_eq, _, _ = expand_equilibrium(T_c, P_c, P_exit)
            isp_fr, _, _ = expand_frozen(T_c, P_c, P_exit)
            assert isp_eq >= isp_fr - 1.0, (  # 1 s tolerance for numerical jitter
                f"equilibrium Isp ({isp_eq:.1f}) < frozen Isp ({isp_fr:.1f}) "
                f"at T_c={T_c} K, P_c={P_c_torr} torr"
            )


def test_isp_monotonic_in_T_for_frozen():
    """Frozen-flow Isp should increase monotonically with chamber T at fixed P."""
    P_c = 100 * TORR_TO_PA
    P_exit = 1.0
    isps = []
    for T_c in [3000.0, 4000.0, 5000.0, 6000.0, 7000.0, 8000.0]:
        isp, _, _ = expand_frozen(T_c, P_c, P_exit)
        isps.append(isp)
    assert all(b > a for a, b in zip(isps, isps[1:])), \
        f"frozen-flow Isp not monotonic in T: {isps}"


def test_isp_reasonable_magnitude():
    """Sanity: water-MET-class operating point gives Isp in the 300-900 s band."""
    isp_eq, _, _ = expand_equilibrium(T_c=7000.0,
                                       P_c_pa=100 * TORR_TO_PA,
                                       P_exit_pa=1.0)
    assert 300.0 < isp_eq < 900.0, f"unexpected Isp magnitude: {isp_eq}"
