"""VehicleState construction + validation."""

from dataclasses import replace, FrozenInstanceError

import pytest

from mission_graph.framework import VehicleState


def _good_state(**overrides):
    base = dict(
        mass_kg=100_000.0,
        propellant_kg=80_000.0,
        payload_kg=0.0,
        location="LEO",
        v_inf_km_s=0.0,
        time_elapsed_s=0.0,
        epoch_jd=None,
        power_available_kwe=30.0,
    )
    base.update(overrides)
    return VehicleState(**base)


def test_constructs_with_valid_fields():
    s = _good_state()
    assert s.mass_kg == 100_000.0
    assert s.location == "LEO"


def test_is_frozen():
    s = _good_state()
    with pytest.raises(FrozenInstanceError):
        s.mass_kg = 50_000.0  # type: ignore[misc]


def test_is_hashable():
    s = _good_state()
    {s}  # would raise if unhashable


def test_replace_produces_new_instance():
    s = _good_state()
    s2 = replace(s, mass_kg=90_000.0)
    assert s.mass_kg == 100_000.0
    assert s2.mass_kg == 90_000.0


def test_rejects_negative_mass():
    with pytest.raises(ValueError, match="mass_kg"):
        _good_state(mass_kg=-1.0)


def test_rejects_negative_propellant():
    with pytest.raises(ValueError, match="propellant_kg"):
        _good_state(propellant_kg=-1.0)


def test_rejects_propellant_exceeding_mass():
    with pytest.raises(ValueError, match="propellant_kg.*cannot exceed mass_kg"):
        _good_state(mass_kg=100.0, propellant_kg=200.0)


def test_rejects_negative_payload():
    with pytest.raises(ValueError, match="payload_kg"):
        _good_state(payload_kg=-1.0)


def test_rejects_negative_power():
    with pytest.raises(ValueError, match="power_available_kwe"):
        _good_state(power_available_kwe=-0.1)


def test_propellant_equal_to_mass_is_allowed():
    _good_state(mass_kg=100.0, propellant_kg=100.0)


def test_zero_payload_is_allowed():
    _good_state(payload_kg=0.0)


def test_health_flags_default_to_empty_frozenset():
    s = _good_state()
    assert s.health_flags == frozenset()
