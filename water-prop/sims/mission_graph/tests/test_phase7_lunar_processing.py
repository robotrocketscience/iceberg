"""Phase 7 lunar processing + low-Earth-orbit water transfer tests."""

import math

from mission_graph.framework import VehicleState, walk, Mission
from mission_graph.missions.phase7_lunar_processing import (
    phase7,
    LUNAR_TO_LEO_DV_KM_S,
    WATER_MET_LUNAR_TRANSFER_ISP_S,
)


def _mission():
    return Mission(
        mission_id="m_p7", objective="x",
        phase_sequence=(phase7,), closure_predicates=(),
    )


def _state_at_lunar_orbit(payload_kg=200_000.0):
    return VehicleState(
        mass_kg=210_000.0, propellant_kg=5_000.0, payload_kg=payload_kg,
        location="lunar_orbit_intermediate", v_inf_km_s=0.0,
        time_elapsed_s=0.0, epoch_jd=None, power_available_kwe=30.0,
    )


def _state_at_leo():
    return VehicleState(
        mass_kg=50_000.0, propellant_kg=10_000.0, payload_kg=40_000.0,
        location="LEO_depot", v_inf_km_s=0.0,
        time_elapsed_s=0.0, epoch_jd=None, power_available_kwe=30.0,
    )


def test_passthrough_at_leo_is_a_no_op():
    """Direct-to-LEO paths should pass through Phase 7 without state change."""
    state = _state_at_leo()
    results = walk(_mission(), state, {})
    passthrough = next(r for r in results if "passthrough_already_at_leo" in r.path_label)
    assert passthrough.is_feasible
    assert passthrough.leaf_state.location == "LEO_depot"
    assert passthrough.leaf_state.payload_kg == state.payload_kg
    assert passthrough.leaf_state.mass_kg == state.mass_kg


def test_lunar_transfer_burns_32_percent_of_chunk_water():
    """Water-electric thrust at 800 s specific impulse for a 3 km/s
    lunar-to-LEO transfer has a mass ratio of exp(3/(800*0.00981)) =
    1.466. Fraction of chunk water arriving at LEO is 1/1.466 = 68.2
    percent; 31.8 percent is consumed as propellant during the shuttle
    leg. Verify a 200-tonne chunk delivers ~136 tonnes to LEO."""
    state = _state_at_lunar_orbit(payload_kg=200_000.0)
    results = walk(_mission(), state, {})
    transfer = next(r for r in results if "lunar_processing_and_leo_transfer" in r.path_label)
    assert transfer.is_feasible
    assert transfer.leaf_state.location == "LEO_depot"
    expected_mass_ratio = math.exp(LUNAR_TO_LEO_DV_KM_S / (WATER_MET_LUNAR_TRANSFER_ISP_S * 0.00981))
    expected_arriving = 200_000.0 / expected_mass_ratio
    assert abs(transfer.leaf_state.payload_kg - expected_arriving) < 100
    # ~136 tonnes arrives
    assert 135_000 < transfer.leaf_state.payload_kg < 137_000


def test_lunar_transfer_rejects_paths_not_at_lunar_orbit():
    """The transfer option only runs from lunar_orbit_intermediate."""
    state = _state_at_leo()
    results = walk(_mission(), state, {})
    transfer = next(r for r in results if "lunar_processing_and_leo_transfer" in r.path_label)
    assert not transfer.is_feasible
    assert "lunar_orbit_intermediate" in transfer.infeasible_reason


def test_passthrough_rejects_non_leo_states():
    """Passthrough is only valid for paths already at LEO_depot."""
    state = _state_at_lunar_orbit()
    results = walk(_mission(), state, {})
    passthrough = next(r for r in results if "passthrough_already_at_leo" in r.path_label)
    assert not passthrough.is_feasible
    assert "LEO_depot" in passthrough.infeasible_reason
