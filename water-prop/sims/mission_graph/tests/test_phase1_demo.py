"""Lock the Phase 1 demo numbers — regression guard on the anchor-driven sizing.

If any of these change, either the anchors moved (titan-3 vis-viva audit,
titan-2 SOI periapsis depth, etc.) or the sizing math broke. Either case
should be intentional and visible in the diff.
"""

from mission_graph.framework import VehicleState, walk, Mission, ClosurePredicate
from mission_graph.missions.phase1_leo_to_saturn import phase1


def _starting_state():
    return VehicleState(
        mass_kg=100_000.0,
        propellant_kg=80_000.0,
        payload_kg=0.0,
        location="LEO",
        v_inf_km_s=0.0,
        time_elapsed_s=0.0,
        epoch_jd=0.0,
        power_available_kwe=30.0,
    )


def _mission_phase1_only():
    return Mission(
        mission_id="m_p1_smoke",
        objective="x",
        phase_sequence=(phase1,),
        closure_predicates=(),
    )


def test_chemical_hohmann_infeasible_at_80t_propellant():
    params = {"chemical_isp_s": 340.0, "electric_isp_s": 3000.0, "electric_thrust_n": 5.0}
    results = walk(_mission_phase1_only(), _starting_state(), params)
    hohmann = [r for r in results if "hohmann_chemical" in r.path_label and "lunar" not in r.path_label]
    assert len(hohmann) == 1
    assert not hohmann[0].is_feasible
    assert "88793" in hohmann[0].infeasible_reason  # 88.8 t required vs 80 t available


def test_hohmann_lga_infeasible_at_80t_propellant():
    params = {"chemical_isp_s": 340.0, "electric_isp_s": 3000.0, "electric_thrust_n": 5.0}
    results = walk(_mission_phase1_only(), _starting_state(), params)
    lga = [r for r in results if "lunar_gravity_assist" in r.path_label]
    assert len(lga) == 1
    assert not lga[0].is_feasible
    assert "84875" in lga[0].infeasible_reason  # 84.9 t required


def test_low_thrust_spiral_feasible_at_higher_thrust():
    """At higher thrust the burn fits in the 6.5-yr Hohmann window. The
    burn-time-vs-coast constraint added per titan-3 R-chunk-size-pareto
    blocks the 5-newton case (5.99 yr > 5.85 yr budget), but at
    50 newtons the burn completes in under a year."""
    params = {"chemical_isp_s": 340.0, "electric_isp_s": 3000.0, "electric_thrust_n": 50.0}
    results = walk(_mission_phase1_only(), _starting_state(), params)
    low_thrust = [r for r in results if "low_thrust" in r.path_label]
    assert len(low_thrust) == 1
    r = low_thrust[0]
    assert r.is_feasible
    s = r.leaf_state
    assert s.location == "saturn_approach"
    assert 63_000 < s.mass_kg < 66_000
    assert s.v_inf_km_s == 0.5


def test_low_thrust_blocked_at_5N_thrust_per_burn_time_constraint():
    """At canonical 5-newton thrust + 100-tonne vehicle, the low-thrust burn
    exceeds the available Hohmann coast. This reproduces titan-3
    R-chunk-size-pareto's matrix verdict that low-thrust + heavy mass
    doesn't close on burn-time, independent of propellant fraction."""
    params = {"chemical_isp_s": 340.0, "electric_isp_s": 3000.0, "electric_thrust_n": 5.0}
    results = walk(_mission_phase1_only(), _starting_state(), params)
    low_thrust = [r for r in results if "low_thrust" in r.path_label]
    assert len(low_thrust) == 1
    assert not low_thrust[0].is_feasible
    assert "burn time" in low_thrust[0].infeasible_reason


def test_star_kick_stage_feasible_with_correct_launch_manifest_split():
    """Star kick stage burns its OWN propellant at 286 s specific impulse,
    sized into the launch manifest. To be feasible the launch manifest must
    have a dry envelope (mass - vehicle propellant - payload) large enough
    to fit kick_dry (2.1 t) + computed kick propellant (~55 t for a 90 t
    stack pushing 2.5 km/s). Vehicle propellant must then cover the 4.8 km/s
    residual at 340 s on the post-kick mass.

    At 90 t manifest with 30 t vehicle propellant, dry envelope = 60 t.
    Kick propellant ~ 53.1 t -> kick wet ~ 55.2 t (fits). Post-kick mass
    ~34.8 t. Residual 4.8 km/s at 340 s needs ~26.5 t propellant, available
    in the 30 t vehicle tank. Leaf vehicle mass ~8.3 t.
    """
    params = {"chemical_isp_s": 340.0, "electric_isp_s": 3000.0, "electric_thrust_n": 5.0}
    # 90 t manifest, 30 t vehicle propellant, 60 t dry envelope -> Star fits.
    state_with_kick = VehicleState(
        mass_kg=90_000.0, propellant_kg=30_000.0, payload_kg=0.0,
        location="LEO", v_inf_km_s=0.0, time_elapsed_s=0.0,
        epoch_jd=0.0, power_available_kwe=30.0,
    )
    results = walk(
        Mission(
            mission_id="m", objective="x",
            phase_sequence=(phase1,), closure_predicates=(),
        ),
        state_with_kick, params,
    )
    star = [r for r in results if "falcon_heavy_plus_star_kick" in r.path_label]
    assert star[0].is_feasible, f"expected feasible, got {star[0].infeasible_reason}"
    assert star[0].leaf_state.location == "saturn_approach"
    # Vehicle propellant decremented by residual burn only (~26.5 t of 30 t).
    assert star[0].leaf_state.propellant_kg < state_with_kick.propellant_kg
    # Leaf vehicle mass roughly 8-9 t (post-kick mass minus residual burn).
    assert 6_000 < star[0].leaf_state.mass_kg < 12_000


def test_kick_stage_infeasible_when_dry_envelope_too_small():
    """Star kick wet (~55 t for 90 t stack) cannot fit in a 10 t dry envelope.
    Verify the precondition rejects with a 'kick wet exceeds dry envelope'
    reason. This is the bug-fix counterexample: under the OLD model, this
    config would have been feasible (kick was treated as free delta-v).
    """
    params = {"chemical_isp_s": 340.0, "electric_isp_s": 3000.0, "electric_thrust_n": 5.0}
    # 90 t manifest with 80 t vehicle propellant -> dry envelope only 10 t.
    # Star kick wet ~55 t. Precondition must reject.
    state = VehicleState(
        mass_kg=90_000.0, propellant_kg=80_000.0, payload_kg=0.0,
        location="LEO", v_inf_km_s=0.0, time_elapsed_s=0.0,
        epoch_jd=0.0, power_available_kwe=30.0,
    )
    results = walk(
        Mission(
            mission_id="m", objective="x",
            phase_sequence=(phase1,), closure_predicates=(),
        ),
        state, params,
    )
    star = next(r for r in results if "falcon_heavy_plus_star_kick" in r.path_label)
    assert not star.is_feasible
    assert "exceeds dry envelope" in star.infeasible_reason


def test_helios_needs_larger_dry_envelope_than_star():
    """Helios kick at 4 km/s and 330 s specific impulse needs more kick
    propellant than Star (despite higher specific impulse, the larger
    delta-v dominates). The kick wet mass is larger, so Helios needs a
    larger dry envelope to be feasible at any given launch manifest.

    At 90 t manifest with 30 t vehicle propellant (60 t dry envelope):
      Star kick wet ~ 55 t (fits)
      Helios kick wet ~ 69 t (does NOT fit)
    Verify Star is feasible and Helios is rejected with kick-wet-exceeds.
    """
    params = {"chemical_isp_s": 340.0, "electric_isp_s": 3000.0, "electric_thrust_n": 5.0}
    state = VehicleState(
        mass_kg=90_000.0, propellant_kg=30_000.0, payload_kg=0.0,
        location="LEO", v_inf_km_s=0.0, time_elapsed_s=0.0,
        epoch_jd=0.0, power_available_kwe=30.0,
    )
    results = walk(
        Mission(
            mission_id="m", objective="x",
            phase_sequence=(phase1,), closure_predicates=(),
        ),
        state, params,
    )
    star = next(r for r in results if "falcon_heavy_plus_star_kick" in r.path_label)
    helios = next(r for r in results if "falcon_heavy_plus_helios_kick" in r.path_label)
    assert star.is_feasible
    assert not helios.is_feasible
    assert "exceeds dry envelope" in helios.infeasible_reason


def test_kick_stage_rejects_non_LEO_start():
    params = {"chemical_isp_s": 340.0, "electric_isp_s": 3000.0, "electric_thrust_n": 5.0}
    state = VehicleState(
        mass_kg=90_000.0, propellant_kg=80_000.0, payload_kg=0.0,
        location="pre_launch", v_inf_km_s=0.0, time_elapsed_s=0.0,
        epoch_jd=0.0, power_available_kwe=30.0,
    )
    results = walk(
        Mission(
            mission_id="m", objective="x",
            phase_sequence=(phase1,), closure_predicates=(),
        ),
        state, params,
    )
    star = [r for r in results if "falcon_heavy_plus_star_kick" in r.path_label]
    assert not star[0].is_feasible
    assert "low-Earth-orbit" in star[0].infeasible_reason


def test_low_thrust_requires_minimum_power():
    params = {"chemical_isp_s": 340.0, "electric_isp_s": 3000.0, "electric_thrust_n": 5.0}
    weak_state = VehicleState(
        mass_kg=100_000.0,
        propellant_kg=80_000.0,
        payload_kg=0.0,
        location="LEO",
        v_inf_km_s=0.0,
        time_elapsed_s=0.0,
        epoch_jd=0.0,
        power_available_kwe=5.0,  # below 20 kWe minimum
    )
    results = walk(_mission_phase1_only(), weak_state, params)
    low_thrust = [r for r in results if "low_thrust" in r.path_label]
    assert not low_thrust[0].is_feasible
    assert "20" in low_thrust[0].infeasible_reason or "power" in low_thrust[0].infeasible_reason.lower()


def test_low_thrust_spiral_rejects_solar_thermal_power_source():
    """Solar-thermal power class cannot power the outbound low-thrust spiral
    because the trajectory crosses to Saturn where solar flux is ~1 percent
    of Earth's value. The power_source parameter gates this; default
    'fission' allows it, 'solar_thermal' rejects.

    Vehicle state and thrust are sized so fission case is feasible
    (low mass + high thrust to clear the burn-time-vs-coast constraint).
    """
    state = VehicleState(
        mass_kg=50_000.0, propellant_kg=40_000.0, payload_kg=0.0,
        location="LEO", v_inf_km_s=0.0, time_elapsed_s=0.0,
        epoch_jd=0.0, power_available_kwe=300.0,
    )
    solar_params = {
        "chemical_isp_s": 340.0, "electric_isp_s": 3000.0,
        "electric_thrust_n": 25.0, "power_source": "solar_thermal",
    }
    fission_params = {
        "chemical_isp_s": 340.0, "electric_isp_s": 3000.0,
        "electric_thrust_n": 25.0, "power_source": "fission",
    }
    solar_results = walk(_mission_phase1_only(), state, solar_params)
    fission_results = walk(_mission_phase1_only(), state, fission_params)
    solar_lt = next(r for r in solar_results if "low_thrust_spiral" in r.path_label)
    fission_lt = next(r for r in fission_results if "low_thrust_spiral" in r.path_label)
    assert not solar_lt.is_feasible
    assert "solar-thermal" in solar_lt.infeasible_reason
    assert fission_lt.is_feasible, f"expected feasible, got: {fission_lt.infeasible_reason}"
