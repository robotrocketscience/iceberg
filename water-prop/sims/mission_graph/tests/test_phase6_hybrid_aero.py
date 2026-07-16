"""Phase 6 hybrid aerocapture-aerobraking option (the phoebe-falsified one)."""

from mission_graph.framework import VehicleState, walk, Mission
from mission_graph.missions.phase6_earth_arrival import phase6


def _approach_state(v_inf_km_s=5.0, payload_kg=20_000.0):
    return VehicleState(
        mass_kg=40_000.0,
        propellant_kg=5_000.0,
        payload_kg=payload_kg,
        location="earth_approach",
        v_inf_km_s=v_inf_km_s,
        time_elapsed_s=0.0,
        epoch_jd=0.0,
        power_available_kwe=30.0,
    )


def _mission():
    return Mission(
        mission_id="m_p6", objective="x",
        phase_sequence=(phase6,), closure_predicates=(),
    )


def test_hybrid_aerocapture_tolerates_higher_vinf_than_single_pass():
    """Single-pass aerocapture rejects v_inf > 6 km/s. Hybrid allows up to 8."""
    params = {"chemical_isp_s": 340.0, "water_met_isp_s": 800.0}
    results = walk(_mission(), _approach_state(v_inf_km_s=7.5), params)
    hybrid = [r for r in results if "hybrid_aerocapture_aerobraking" in r.path_label][0]
    single = [r for r in results if r.path_label.endswith("aerocapture.")
              or (r.node_labels and r.node_labels[0].split(".")[1] == "aerocapture")][0]
    assert hybrid.is_feasible
    assert not single.is_feasible


def test_hybrid_aerocapture_blocked_at_excessive_payload():
    """Per phoebe falsification: at chunk-bearing 200+ t the sublimation
    budget across 3 passes is exhausted. Framework caps at 100 t."""
    params = {"chemical_isp_s": 340.0, "water_met_isp_s": 800.0}
    results = walk(_mission(), _approach_state(payload_kg=150_000.0), params)
    hybrid = [r for r in results if "hybrid_aerocapture_aerobraking" in r.path_label][0]
    assert not hybrid.is_feasible
    assert "sublimation" in hybrid.infeasible_reason.lower() or "payload" in hybrid.infeasible_reason.lower()


def test_hybrid_aerocapture_loses_10pct_payload_to_sublimation():
    """Per design: 10% of payload sublimated across the multi-pass thermal load."""
    params = {"chemical_isp_s": 340.0, "water_met_isp_s": 800.0}
    state_in = _approach_state(v_inf_km_s=4.0, payload_kg=50_000.0)
    results = walk(_mission(), state_in, params)
    hybrid = [r for r in results if "hybrid_aerocapture_aerobraking" in r.path_label][0]
    assert hybrid.is_feasible
    # 50_000 * (1 - 0.10) = 45_000
    assert 44_500 < hybrid.leaf_state.payload_kg < 45_500


def test_phase6_has_all_options():
    """Verifies the extended Phase 6 has all options. Started at 5 then
    grew to 7 when Earth-gravity-assist slowdown and chemical-lunar-
    orbit-capture were added (the latter feeds Phase 7 sub-mission)."""
    params = {"chemical_isp_s": 340.0, "water_met_isp_s": 800.0}
    results = walk(_mission(), _approach_state(v_inf_km_s=4.0), params)
    option_ids = {r.node_labels[0].split(".")[1] for r in results}
    assert option_ids == {
        "direct_propulsive_capture",
        "lunar_gravity_assist_capture",
        "aerocapture",
        "low_thrust_earth_capture",
        "hybrid_aerocapture_aerobraking",
        "earth_gravity_assist_slowdown",
        "chemical_lunar_orbit_capture",
    }
