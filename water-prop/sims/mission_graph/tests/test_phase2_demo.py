"""Phase 2 capture options — cross-phase preconditions on v_inf and power."""

from mission_graph.framework import VehicleState, walk, Mission
from mission_graph.missions.phase2_saturn_capture import phase2


def _saturn_approach_state(v_inf_km_s=5.44, mass_kg=50_000, propellant_kg=25_000, power_kwe=30.0):
    return VehicleState(
        mass_kg=mass_kg,
        propellant_kg=propellant_kg,
        payload_kg=0.0,
        location="saturn_approach",
        v_inf_km_s=v_inf_km_s,
        time_elapsed_s=0.0,
        epoch_jd=None,
        power_available_kwe=power_kwe,
    )


def _mission_phase2_only():
    return Mission(
        mission_id="m_p2", objective="x",
        phase_sequence=(phase2,), closure_predicates=(),
    )


def test_direct_chemical_capture_works_with_adequate_propellant():
    params = {"chemical_isp_s": 340.0, "electric_isp_s": 3000.0}
    results = walk(_mission_phase2_only(), _saturn_approach_state(), params)
    direct = [r for r in results if "direct_chemical_capture" in r.path_label]
    assert direct[0].is_feasible
    assert direct[0].leaf_state.location == "saturn_orbit"


def test_subdring_cheaper_than_direct_chemical():
    """0.8 km/s burn at sub-D-ring vs 1.55 direct should leave more mass."""
    params = {"chemical_isp_s": 340.0, "electric_isp_s": 3000.0}
    results = walk(_mission_phase2_only(), _saturn_approach_state(), params)
    direct = next(r for r in results if "direct_chemical_capture" in r.path_label)
    subdring = next(r for r in results if "subdring" in r.path_label)
    assert subdring.leaf_state.mass_kg > direct.leaf_state.mass_kg


def test_low_thrust_capture_blocked_at_high_v_inf():
    """Hohmann arrival (v_inf ~5.44) cannot use low-thrust capture."""
    params = {"chemical_isp_s": 340.0, "electric_isp_s": 3000.0}
    results = walk(_mission_phase2_only(), _saturn_approach_state(v_inf_km_s=5.44), params)
    lt = [r for r in results if "low_thrust_capture" in r.path_label]
    assert not lt[0].is_feasible
    assert "v_inf" in lt[0].infeasible_reason


def test_low_thrust_capture_feasible_at_low_v_inf():
    """Low-thrust arrival (v_inf 0.5) can use low-thrust capture."""
    params = {"chemical_isp_s": 340.0, "electric_isp_s": 3000.0}
    results = walk(_mission_phase2_only(), _saturn_approach_state(v_inf_km_s=0.5), params)
    lt = [r for r in results if "low_thrust_capture" in r.path_label]
    assert lt[0].is_feasible


def test_low_thrust_capture_blocked_by_insufficient_power():
    """Even at low v_inf, low-thrust capture needs >=30 kWe."""
    params = {"chemical_isp_s": 340.0, "electric_isp_s": 3000.0}
    state = _saturn_approach_state(v_inf_km_s=0.5, power_kwe=10.0)
    results = walk(_mission_phase2_only(), state, params)
    lt = [r for r in results if "low_thrust_capture" in r.path_label]
    assert not lt[0].is_feasible
    assert "power" in lt[0].infeasible_reason.lower()


def test_capture_requires_saturn_approach_location():
    """Phase 2 options reject states not at saturn_approach."""
    params = {"chemical_isp_s": 340.0, "electric_isp_s": 3000.0}
    state = VehicleState(
        mass_kg=50_000, propellant_kg=10_000, payload_kg=0.0,
        location="LEO", v_inf_km_s=0.0, time_elapsed_s=0.0,
        epoch_jd=None, power_available_kwe=30.0,
    )
    results = walk(_mission_phase2_only(), state, params)
    for r in results:
        assert not r.is_feasible
        assert "saturn_approach" in r.infeasible_reason


def test_titan_ga_capture_feasible_at_hohmann_arrival_v_inf():
    """Titan gravity-assist capture should work at Hohmann arrival v_inf
    (5.44 km/s) since that exceeds the 3.5 km/s minimum."""
    params = {"chemical_isp_s": 340.0, "electric_isp_s": 3000.0}
    results = walk(_mission_phase2_only(), _saturn_approach_state(v_inf_km_s=5.44), params)
    titan = next(r for r in results if "titan_gravity_assist_capture" in r.path_label)
    assert titan.is_feasible
    assert titan.leaf_state.location == "saturn_orbit"
    assert titan.leaf_state.v_inf_km_s == 0.0
    expected_time = 8.0 / 12.0 * 365.25 * 86_400
    assert abs(titan.leaf_state.time_elapsed_s - expected_time) < 1.0


def test_titan_ga_capture_blocked_at_low_v_inf():
    """Titan gravity-assist capture must reject arrival v_inf below 3.5
    km/s — the flyby geometry doesn't have enough leverage."""
    params = {"chemical_isp_s": 340.0, "electric_isp_s": 3000.0}
    results = walk(_mission_phase2_only(), _saturn_approach_state(v_inf_km_s=2.0), params)
    titan = next(r for r in results if "titan_gravity_assist_capture" in r.path_label)
    assert not titan.is_feasible
    assert "v_inf" in titan.infeasible_reason


def test_rhea_ga_capture_needs_higher_v_inf_than_titan():
    """Rhea gravity-assist capture has a tighter geometry budget. At
    v_inf 3.7 km/s, Titan is feasible but Rhea is not."""
    params = {"chemical_isp_s": 340.0, "electric_isp_s": 3000.0}
    results = walk(_mission_phase2_only(), _saturn_approach_state(v_inf_km_s=3.7), params)
    titan = next(r for r in results if "titan_gravity_assist_capture" in r.path_label)
    rhea = next(r for r in results if "rhea_gravity_assist_capture" in r.path_label)
    assert titan.is_feasible
    assert not rhea.is_feasible


def test_cassini_class_tour_has_lower_v_inf_floor_than_titan_alone():
    """Cassini-class multi-moon tour can be set up at lower arrival v_inf
    (>= 3.0 km/s) because multiple targets give more geometry. At v_inf
    3.2 km/s, Cassini-class is feasible while Titan-alone is not."""
    params = {"chemical_isp_s": 340.0, "electric_isp_s": 3000.0}
    results = walk(_mission_phase2_only(), _saturn_approach_state(v_inf_km_s=3.2), params)
    titan = next(r for r in results if "titan_gravity_assist_capture" in r.path_label)
    cassini = next(r for r in results if "cassini_class_multi_moon_tour" in r.path_label)
    assert not titan.is_feasible
    assert cassini.is_feasible
    expected_time = 24.0 / 12.0 * 365.25 * 86_400
    assert abs(cassini.leaf_state.time_elapsed_s - expected_time) < 1.0
