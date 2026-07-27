"""Regression tests for the self-consistent kick-stage model.

Pins the second kick-model correction (rhea-5 R-closing-path-self-consistency,
2026-06-12): the kick stage rides the manifest alongside the vehicle, pushes
itself plus the vehicle, and is gated on total stack mass. The vehicle's own
mass must never drop below what its residual burn alone accounts for — the
prior model burned the vehicle's derived hardware as kick propellant.
"""

import math

import pytest

from mission_graph.framework import VehicleState
from mission_graph.missions.phase1_leo_to_saturn import (
    HELIOS_KICK_DRY_MASS_KG,
    HELIOS_KICK_DV_KM_S,
    HELIOS_KICK_ISP_S,
    MAX_KICK_MANIFEST_KG,
    TSI_DV_HOHMANN_KM_S,
    _kick_stack_propellant_kg,
    falcon_heavy_plus_helios_kick,
    rocket_equation_burn,
)

PARAMS = {"chemical_isp_s": 340.0, "launch_epoch_jd": 0.0}


def _leo_state(wet_kg: float, propellant_kg: float) -> VehicleState:
    return VehicleState(
        mass_kg=wet_kg, propellant_kg=propellant_kg, payload_kg=0.0,
        location="LEO", v_inf_km_s=0.0, time_elapsed_s=0.0,
        epoch_jd=0.0, power_available_kwe=30.0,
    )


def test_stack_propellant_solves_implicit_equation():
    """kick_prop = (vehicle + kick_dry + kick_prop) * f_burn, exactly."""
    vehicle = 116_500.0
    kp = _kick_stack_propellant_kg(
        vehicle, HELIOS_KICK_DV_KM_S, HELIOS_KICK_DRY_MASS_KG, HELIOS_KICK_ISP_S)
    f_burn = 1.0 - math.exp(-HELIOS_KICK_DV_KM_S * 1000.0 / (9.81 * HELIOS_KICK_ISP_S))
    assert kp == pytest.approx((vehicle + HELIOS_KICK_DRY_MASS_KG + kp) * f_burn, rel=1e-9)


def test_closing_cell_vehicle_is_rejected_on_stack_mass():
    """The fidelity-round closing cell (116.5 t wet vehicle) must NOT pass:
    the self-consistent Helios stack is ~490 t against the 300 t manifest."""
    state = _leo_state(116_500.0, 23_300.0)
    kp = _kick_stack_propellant_kg(
        state.mass_kg, HELIOS_KICK_DV_KM_S, HELIOS_KICK_DRY_MASS_KG, HELIOS_KICK_ISP_S)
    assert state.mass_kg + HELIOS_KICK_DRY_MASS_KG + kp > MAX_KICK_MANIFEST_KG
    ok, why = falcon_heavy_plus_helios_kick.precondition(state, PARAMS)
    assert not ok
    assert "exceeds most-permissive launch manifest" in why


def test_small_vehicle_passes_and_keeps_its_own_mass():
    """A vehicle light enough for the stack gate loses ONLY its residual-burn
    propellant — never kick wet mass (the prior model's bug).

    40 t wet / 26 t propellant: Helios residual 3.3 km/s at 340 s needs
    ~25.1 t — fits the 26 t tank."""
    wet = 40_000.0
    state = _leo_state(wet, 26_000.0)
    ok, why = falcon_heavy_plus_helios_kick.precondition(state, PARAMS)
    assert ok, why
    out = falcon_heavy_plus_helios_kick.executor(state, PARAMS)
    residual_dv = TSI_DV_HOHMANN_KM_S - HELIOS_KICK_DV_KM_S
    expected_mass, expected_burn = rocket_equation_burn(wet, residual_dv, 340.0)
    assert out.mass_kg == pytest.approx(expected_mass)
    assert out.propellant_kg == pytest.approx(26_000.0 - expected_burn)
    # Invariant: executor never removes more than the residual burn.
    assert out.mass_kg >= wet - expected_burn - 1e-6
