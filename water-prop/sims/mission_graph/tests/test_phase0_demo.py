"""Phase 0 launch-vehicle capabilities."""

from mission_graph.framework import VehicleState, walk, Mission
from mission_graph.missions.phase0_earth_to_leo import phase0


def _ground_state(mass_kg):
    return VehicleState(
        mass_kg=mass_kg,
        propellant_kg=0.0,
        payload_kg=0.0,
        location="pre_launch",
        v_inf_km_s=0.0,
        time_elapsed_s=0.0,
        epoch_jd=None,
        power_available_kwe=0.0,
    )


def _mission_phase0_only():
    return Mission(
        mission_id="m_p0", objective="x",
        phase_sequence=(phase0,), closure_predicates=(),
    )


def test_falcon_heavy_feasible_under_cap():
    results = walk(_mission_phase0_only(), _ground_state(50_000), {"multi_falcon_launch_count": 0, "launch_epoch_jd": 0.0})
    fh = [r for r in results if "falcon_heavy_expended" in r.path_label]
    assert fh[0].is_feasible
    assert fh[0].leaf_state.location == "LEO"


def test_falcon_heavy_infeasible_over_cap():
    results = walk(_mission_phase0_only(), _ground_state(70_000), {"multi_falcon_launch_count": 0, "launch_epoch_jd": 0.0})
    fh = [r for r in results if "falcon_heavy_expended" in r.path_label]
    assert not fh[0].is_feasible
    assert "63800" in fh[0].infeasible_reason


def test_starship_feasible_at_high_mass():
    results = walk(_mission_phase0_only(), _ground_state(95_000), {"multi_falcon_launch_count": 0, "launch_epoch_jd": 0.0})
    ss = [r for r in results if "starship" in r.path_label]
    assert ss[0].is_feasible


def test_starship_infeasible_over_cap():
    results = walk(_mission_phase0_only(), _ground_state(120_000), {"multi_falcon_launch_count": 0, "launch_epoch_jd": 0.0})
    ss = [r for r in results if "starship" in r.path_label]
    assert not ss[0].is_feasible


def test_multi_falcon_2_launch_caps_at_100t():
    """2 Falcon Heavy partial-reuse launches at 50 t each = 100 t deliverable."""
    results = walk(_mission_phase0_only(), _ground_state(80_000), {"launch_epoch_jd": 0.0})
    mf = [r for r in results if "multi_falcon_2_launch" in r.path_label]
    assert mf[0].is_feasible

    results = walk(_mission_phase0_only(), _ground_state(120_000), {"launch_epoch_jd": 0.0})
    mf = [r for r in results if "multi_falcon_2_launch" in r.path_label]
    assert not mf[0].is_feasible


def test_multi_falcon_6_launch_stamps_pending_assembly_flag():
    """Multi-launch options stamp a flag the assembly phase consumes."""
    results = walk(_mission_phase0_only(), _ground_state(90_000), {"launch_epoch_jd": 0.0})
    mf = [r for r in results if "multi_falcon_6_launch" in r.path_label][0]
    assert mf.is_feasible
    assert "multi_launch_pending_assembly_6" in mf.leaf_state.health_flags
    # campaign elapsed time: (6-1) * 60 days = 300 days
    days = mf.leaf_state.time_elapsed_s / 86_400
    assert 290 < days < 310


def test_starship_does_not_stamp_assembly_flag():
    results = walk(_mission_phase0_only(), _ground_state(80_000), {"launch_epoch_jd": 0.0})
    ss = [r for r in results if "starship" in r.path_label][0]
    assert ss.is_feasible
    assert not any(f.startswith("multi_launch_pending_assembly") for f in ss.leaf_state.health_flags)
