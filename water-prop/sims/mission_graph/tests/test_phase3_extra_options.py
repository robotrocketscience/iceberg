"""Phase 3 extended option set: F-G gap rendezvous, B-ring direct rendezvous."""

from mission_graph.framework import VehicleState, walk, Mission
from mission_graph.missions.phase3_chunk_acquisition import phase3


def _saturn_orbit_state(propellant_kg=10_000.0):
    return VehicleState(
        mass_kg=20_000.0,
        propellant_kg=propellant_kg,
        payload_kg=0.0,
        location="saturn_orbit",
        v_inf_km_s=0.0,
        time_elapsed_s=0.0,
        epoch_jd=0.0,
        power_available_kwe=30.0,
    )


def _mission():
    return Mission(
        mission_id="m_p3", objective="x",
        phase_sequence=(phase3,), closure_predicates=(),
    )


def test_fg_gap_rendezvous_captures_at_55pct_efficiency():
    params = {"chunk_mass_kg": 100_000.0}
    results = walk(_mission(), _saturn_orbit_state(), params)
    fg = [r for r in results if "fg_gap_rendezvous_trawl" in r.path_label][0]
    assert fg.is_feasible
    # 100 t chunk * 0.55 = 55 t captured
    assert 54_000 < fg.leaf_state.payload_kg < 56_000


def test_b_ring_direct_captures_only_1pct_via_survival_probability():
    """Per phoebe falsification: B-ring direct rendezvous expected capture
    is chunk * 1.5 raw yield * 0.01 survival = 1.5% of chunk."""
    params = {"chunk_mass_kg": 100_000.0}
    results = walk(_mission(), _saturn_orbit_state(), params)
    br = [r for r in results if "b_ring_direct_rendezvous" in r.path_label][0]
    assert br.is_feasible
    # 100 t * 1.5 * 0.01 = 1.5 t
    assert 1_400 < br.leaf_state.payload_kg < 1_600


def test_b_ring_direct_stamps_survival_risk_flag():
    params = {"chunk_mass_kg": 100_000.0}
    results = walk(_mission(), _saturn_orbit_state(), params)
    br = [r for r in results if "b_ring_direct_rendezvous" in r.path_label][0]
    assert "b_ring_survival_risk" in br.leaf_state.health_flags


def test_phase3_now_has_four_options():
    """Verifies the extended phase has all 4 options enumerated."""
    params = {"chunk_mass_kg": 50_000.0}
    results = walk(_mission(), _saturn_orbit_state(), params)
    option_ids = {r.node_labels[0].split(".")[1] for r in results}
    assert option_ids == {
        "single_pass_trawl",
        "drift_through_trawl",
        "fg_gap_rendezvous_trawl",
        "b_ring_direct_rendezvous",
    }
