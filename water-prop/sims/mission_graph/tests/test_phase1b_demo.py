"""Phase 1b cruise ops: ballistic / MCC / Jupiter GA / Mars+Jupiter GA."""

from mission_graph.framework import VehicleState, walk, Mission
from mission_graph.missions.phase1b_cruise_ops import phase1b


def _approach_state(v_inf_km_s=5.44, mass_kg=50_000, propellant_kg=10_000):
    return VehicleState(
        mass_kg=mass_kg,
        propellant_kg=propellant_kg,
        payload_kg=0.0,
        location="saturn_approach",
        v_inf_km_s=v_inf_km_s,
        time_elapsed_s=6.5 * 365.25 * 86_400,
        epoch_jd=None,
        power_available_kwe=30.0,
    )


def _mission():
    return Mission(
        mission_id="m_p1b", objective="x",
        phase_sequence=(phase1b,), closure_predicates=(),
    )


def test_ballistic_coast_is_no_op_on_state_but_adds_health_flag():
    params = {"chemical_isp_s": 340.0, "launch_epoch_jd": 0.0}
    state_in = _approach_state()
    results = walk(_mission(), state_in, params)
    ballistic = [r for r in results if "ballistic_coast" in r.path_label][0]
    assert ballistic.is_feasible
    assert ballistic.leaf_state.mass_kg == state_in.mass_kg
    assert ballistic.leaf_state.propellant_kg == state_in.propellant_kg
    assert ballistic.leaf_state.v_inf_km_s == state_in.v_inf_km_s
    assert "no_mcc_redundancy" in ballistic.leaf_state.health_flags


def test_mcc_costs_propellant_without_changing_v_inf():
    params = {"chemical_isp_s": 340.0, "launch_epoch_jd": 0.0}
    state_in = _approach_state()
    results = walk(_mission(), state_in, params)
    mcc = [r for r in results if "mcc_only" in r.path_label][0]
    assert mcc.is_feasible
    assert mcc.leaf_state.propellant_kg < state_in.propellant_kg
    assert mcc.leaf_state.v_inf_km_s == state_in.v_inf_km_s


def test_jupiter_ga_reduces_v_inf():
    params = {"chemical_isp_s": 340.0, "launch_epoch_jd": 0.0}
    state_in = _approach_state(v_inf_km_s=5.44)
    results = walk(_mission(), state_in, params)
    jga = [r for r in results if "jupiter_gravity_assist" in r.path_label][0]
    assert jga.is_feasible
    # 5.44 - 2.5 = 2.94
    assert abs(jga.leaf_state.v_inf_km_s - 2.94) < 0.01


def test_jupiter_ga_blocked_at_low_v_inf():
    """Cross-phase compatibility: low-thrust spiral arrivals (v_inf 0.5) cannot
    use a planetary gravity assist."""
    params = {"chemical_isp_s": 340.0, "launch_epoch_jd": 0.0}
    state_in = _approach_state(v_inf_km_s=0.5)
    results = walk(_mission(), state_in, params)
    jga = [r for r in results if "jupiter_gravity_assist" in r.path_label][0]
    assert not jga.is_feasible
    assert "v_inf" in jga.infeasible_reason


def test_mars_jupiter_ga_reduces_v_inf_more_than_jupiter_only():
    params = {"chemical_isp_s": 340.0, "launch_epoch_jd": 0.0}
    state_in = _approach_state(v_inf_km_s=5.44)
    results = walk(_mission(), state_in, params)
    jga = next(r for r in results if "jupiter_gravity_assist" in r.path_label and "mars" not in r.path_label)
    mjga = next(r for r in results if "mars_jupiter" in r.path_label)
    assert jga.is_feasible and mjga.is_feasible
    assert mjga.leaf_state.v_inf_km_s < jga.leaf_state.v_inf_km_s


def test_ga_options_cost_more_time():
    params = {"chemical_isp_s": 340.0, "launch_epoch_jd": 0.0}
    state_in = _approach_state(v_inf_km_s=5.44)
    results = walk(_mission(), state_in, params)
    ballistic = next(r for r in results if "ballistic_coast" in r.path_label)
    mjga = next(r for r in results if "mars_jupiter" in r.path_label)
    # Mars+Jupiter adds 2 years vs ballistic no-op
    assert mjga.leaf_state.time_elapsed_s - ballistic.leaf_state.time_elapsed_s > 1.9 * 365.25 * 86_400


def test_venus_earth_ga_reduces_v_inf_and_costs_long_cruise():
    """Venus-Earth gravity assist reduces Saturn arrival v_inf by ~2 km/s
    at the cost of ~3.5 years of extra cruise — the long-cruise penalty
    is the canonical trade for VEEGA-class trajectories."""
    params = {"chemical_isp_s": 340.0, "launch_epoch_jd": 0.0}
    state_in = _approach_state(v_inf_km_s=5.44)
    results = walk(_mission(), state_in, params)
    veega = next(r for r in results if "venus_earth_gravity_assist" in r.path_label)
    ballistic = next(r for r in results if "ballistic_coast" in r.path_label)
    assert veega.is_feasible
    assert veega.leaf_state.v_inf_km_s < state_in.v_inf_km_s - 1.5
    extra = veega.leaf_state.time_elapsed_s - ballistic.leaf_state.time_elapsed_s
    assert 3.4 * 365.25 * 86_400 < extra < 3.6 * 365.25 * 86_400


def test_venus_earth_ga_blocked_out_of_launch_window():
    """Venus-Earth launch window is tight (~20-day window every ~584 days).
    Outside the window, the option must reject."""
    # Epoch JD 100 is outside any 20-day window for a 584-day synodic period.
    params = {"chemical_isp_s": 340.0, "launch_epoch_jd": 100.0}
    state_in = _approach_state(v_inf_km_s=5.44)
    results = walk(_mission(), state_in, params)
    veega = next(r for r in results if "venus_earth_gravity_assist" in r.path_label)
    assert not veega.is_feasible
    assert "Venus-Earth" in veega.infeasible_reason or "window" in veega.infeasible_reason
