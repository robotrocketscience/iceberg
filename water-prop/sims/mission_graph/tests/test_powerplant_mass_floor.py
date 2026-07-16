"""Constraints 2 + 3 (powerplant + bus dry-mass floor) tests.

R-framework-matrix-parity (titan-4). The framework previously charged ZERO for
the powerplant; these tests pin the reactor + MARVL radiator + thruster (+ bus)
mass and the "powerplant must fit in dry mass" precondition.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from mission_graph.framework import VehicleState  # noqa: E402
from mission_graph.missions.powerplant_constraints import (  # noqa: E402
    mass_floor_ok,
    required_dry_mass_kg,
    required_powerplant_mass_kg,
)


def _leo_state(mass_t: float, prop_frac: float, power_kwe: float) -> VehicleState:
    return VehicleState(
        mass_kg=mass_t * 1000.0,
        propellant_kg=mass_t * 1000.0 * prop_frac,
        payload_kg=0.0,
        location="LEO",
        v_inf_km_s=0.0,
        time_elapsed_s=0.0,
        epoch_jd=None,
        power_available_kwe=power_kwe,
    )


def test_powerplant_mass_at_30kwe_2p4_specific_power():
    # reactor 30000/2.4 = 12500 kg; radiator 5000 + 30*100 = 8000; thrusters 300.
    m = required_powerplant_mass_kg(30.0, {"reactor_specific_power_w_per_kg": 2.4})
    assert abs(m - (12500.0 + 8000.0 + 300.0)) < 1.0


def test_powerplant_mass_lighter_at_higher_specific_power():
    # titan-3 also swept sp = 10 W/kg (Kilopower extrapolation): reactor 3000 kg.
    m = required_powerplant_mass_kg(30.0, {"reactor_specific_power_w_per_kg": 10.0})
    assert abs(m - (3000.0 + 8000.0 + 300.0)) < 1.0


def test_required_dry_mass_adds_conservative_bus_floor():
    # Constraint 3: dry-mass floor = 2000 kg bus + powerplant.
    params = {"enforce_mass_floor": True, "reactor_specific_power_w_per_kg": 2.4}
    plant = required_powerplant_mass_kg(30.0, params)
    dry = required_dry_mass_kg(30.0, params)
    assert abs(dry - (plant + 2000.0)) < 1.0


def test_required_dry_mass_zero_when_floor_off():
    assert required_dry_mass_kg(30.0, {}) == 0.0


def test_bus_floor_overridable():
    params = {"enforce_mass_floor": True, "reactor_specific_power_w_per_kg": 2.4,
              "bus_mass_floor_kg": 600.0}  # Cassini heritage
    plant = required_powerplant_mass_kg(30.0, params)
    assert abs(required_dry_mass_kg(30.0, params) - (plant + 600.0)) < 1.0


def test_mass_floor_off_by_default():
    # 50 t vehicle, 80% propellant -> 10 t dry, far below a 30 kWe powerplant.
    # With the floor OFF (default), still feasible.
    ok, _ = mass_floor_ok(_leo_state(50.0, 0.80, 30.0), {})
    assert ok is True


def test_mass_floor_rejects_underpowered_small_vehicle():
    # 50 t vehicle at 80% propellant = 10 t dry < 20.8 t powerplant at 30 kWe/2.4.
    params = {"enforce_mass_floor": True, "reactor_specific_power_w_per_kg": 2.4}
    ok, why = mass_floor_ok(_leo_state(50.0, 0.80, 30.0), params)
    assert ok is False
    assert "powerplant" in why


def test_mass_floor_passes_large_enough_vehicle():
    # 200 t vehicle at 80% propellant = 40 t dry > 20.8 t powerplant at 30 kWe/2.4.
    params = {"enforce_mass_floor": True, "reactor_specific_power_w_per_kg": 2.4}
    ok, _ = mass_floor_ok(_leo_state(200.0, 0.80, 30.0), params)
    assert ok is True


def test_mass_floor_passes_small_vehicle_at_high_specific_power():
    # sp = 10 W/kg shrinks the reactor; 50 t vehicle now carries a 30 kWe plant
    # (3 + 8 + 0.3 = 11.3 t < 10 t? no -> still fails at 80% prop). Drop prop to
    # 70% -> 15 t dry > 11.3 t -> passes.
    params = {"enforce_mass_floor": True, "reactor_specific_power_w_per_kg": 10.0}
    ok, _ = mass_floor_ok(_leo_state(50.0, 0.70, 30.0), params)
    assert ok is True
