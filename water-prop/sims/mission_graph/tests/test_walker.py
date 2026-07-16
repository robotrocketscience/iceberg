"""Walker traversal behavior: enumeration, infeasibility, sub-phase recursion,
closure-predicate application."""

from dataclasses import replace

import pytest

from mission_graph.framework import (
    ClosurePredicate,
    Mission,
    Option,
    Phase,
    VehicleState,
    walk,
)


def _state(**overrides):
    base = dict(
        mass_kg=1000.0,
        propellant_kg=500.0,
        payload_kg=0.0,
        location="START",
        v_inf_km_s=0.0,
        time_elapsed_s=0.0,
        epoch_jd=None,
        power_available_kwe=10.0,
    )
    base.update(overrides)
    return VehicleState(**base)


def _always_feasible_option(option_id="ok", phase_id="P", new_location="END"):
    return Option(
        option_id=option_id,
        description="x",
        phase_id=phase_id,
        precondition=lambda s, p: (True, "ok"),
        executor=lambda s, p: replace(s, location=new_location),
        params_required=(),
    )


def _always_infeasible_option(option_id="no", phase_id="P", reason="nope"):
    return Option(
        option_id=option_id,
        description="x",
        phase_id=phase_id,
        precondition=lambda s, p, reason=reason: (False, reason),
        executor=lambda s, p: s,
        params_required=(),
    )


def _phase(phase_id="P", options=None):
    return Phase(
        phase_id=phase_id,
        description="x",
        options=tuple(options or [_always_feasible_option(phase_id=phase_id)]),
    )


# ----- single-phase basics -----


def test_single_phase_single_feasible_option_returns_one_feasible_result():
    m = Mission(
        mission_id="m",
        objective="x",
        phase_sequence=(_phase(),),
        closure_predicates=(),
    )
    results = walk(m, _state(), {})
    assert len(results) == 1
    assert results[0].is_feasible
    assert results[0].leaf_state.location == "END"
    assert results[0].infeasible_at is None


def test_single_phase_single_infeasible_option_records_reason():
    opt = _always_infeasible_option(reason="no fuel")
    m = Mission(
        mission_id="m",
        objective="x",
        phase_sequence=(_phase(phase_id="P", options=[opt]),),
        closure_predicates=(),
    )
    results = walk(m, _state(), {})
    assert len(results) == 1
    assert not results[0].is_feasible
    assert results[0].leaf_state is None
    assert results[0].infeasible_at == "P"
    assert results[0].infeasible_reason == "no fuel"


def test_multiple_options_each_enumerated():
    opts = [
        _always_feasible_option(option_id=f"opt_{i}", phase_id="P")
        for i in range(3)
    ]
    m = Mission(
        mission_id="m",
        objective="x",
        phase_sequence=(_phase(phase_id="P", options=opts),),
        closure_predicates=(),
    )
    results = walk(m, _state(), {})
    assert len(results) == 3
    option_ids = {r.node_labels[0].split(".")[1] for r in results}
    assert option_ids == {"opt_0", "opt_1", "opt_2"}


# ----- multi-phase chaining -----


def test_two_phases_state_threads_through():
    p1 = _phase(phase_id="P1", options=[_always_feasible_option(phase_id="P1", new_location="MID")])
    p2 = _phase(phase_id="P2", options=[_always_feasible_option(phase_id="P2", new_location="END")])
    m = Mission(
        mission_id="m",
        objective="x",
        phase_sequence=(p1, p2),
        closure_predicates=(),
    )
    results = walk(m, _state(), {})
    assert len(results) == 1
    assert results[0].leaf_state.location == "END"
    assert len(results[0].node_labels) == 2


def test_infeasibility_at_later_phase_terminates_that_branch_only():
    feasible_p1 = _always_feasible_option(option_id="go", phase_id="P1")
    bad_p2 = _always_infeasible_option(option_id="bad", phase_id="P2", reason="blocked")
    good_p2 = _always_feasible_option(option_id="good", phase_id="P2")

    p1 = _phase(phase_id="P1", options=[feasible_p1])
    p2 = _phase(phase_id="P2", options=[bad_p2, good_p2])
    m = Mission(
        mission_id="m",
        objective="x",
        phase_sequence=(p1, p2),
        closure_predicates=(),
    )
    results = walk(m, _state(), {})
    assert len(results) == 2
    feasible = [r for r in results if r.is_feasible]
    infeasible = [r for r in results if not r.is_feasible]
    assert len(feasible) == 1 and len(infeasible) == 1
    assert infeasible[0].infeasible_at == "P2"
    assert infeasible[0].infeasible_reason == "blocked"


# ----- sub-phase recursion -----


def test_sub_phases_flatten_during_traversal():
    inner_a = _phase(phase_id="P_inner_a", options=[_always_feasible_option(phase_id="P_inner_a", new_location="A_DONE")])
    inner_b = _phase(phase_id="P_inner_b", options=[_always_feasible_option(phase_id="P_inner_b", new_location="B_DONE")])
    nested = Phase(phase_id="P_outer", description="x", sub_phases=(inner_a, inner_b))

    m = Mission(
        mission_id="m",
        objective="x",
        phase_sequence=(nested,),
        closure_predicates=(),
    )
    results = walk(m, _state(), {})
    assert len(results) == 1
    assert results[0].leaf_state.location == "B_DONE"
    assert len(results[0].node_labels) == 2  # two leaf options traversed


# ----- closure predicates -----


def test_closure_predicates_applied_to_feasible_leaves():
    cp = ClosurePredicate(
        name="reached_end",
        description="x",
        fn=lambda s: "close" if s.location == "END" else "miss",
    )
    m = Mission(
        mission_id="m",
        objective="x",
        phase_sequence=(_phase(),),
        closure_predicates=(cp,),
    )
    results = walk(m, _state(), {})
    assert results[0].closure_verdicts == {"reached_end": "close"}


def test_closure_predicates_not_applied_to_infeasible_paths():
    cp = ClosurePredicate(
        name="reached_end", description="x", fn=lambda s: "close"
    )
    opt = _always_infeasible_option(reason="nope")
    m = Mission(
        mission_id="m",
        objective="x",
        phase_sequence=(_phase(phase_id="P", options=[opt]),),
        closure_predicates=(cp,),
    )
    results = walk(m, _state(), {})
    assert results[0].closure_verdicts == {}


def test_multiple_closure_predicates_all_evaluated():
    cps = (
        ClosurePredicate(name="cp1", description="x", fn=lambda s: "v1"),
        ClosurePredicate(name="cp2", description="x", fn=lambda s: "v2"),
    )
    m = Mission(
        mission_id="m",
        objective="x",
        phase_sequence=(_phase(),),
        closure_predicates=cps,
    )
    results = walk(m, _state(), {})
    assert results[0].closure_verdicts == {"cp1": "v1", "cp2": "v2"}


# ----- determinism -----


def test_repeat_walks_produce_identical_path_labels():
    m = Mission(
        mission_id="m",
        objective="x",
        phase_sequence=(_phase(),),
        closure_predicates=(),
    )
    r1 = walk(m, _state(), {})
    r2 = walk(m, _state(), {})
    assert [r.path_label for r in r1] == [r.path_label for r in r2]


def test_different_params_produce_different_labels():
    m = Mission(
        mission_id="m",
        objective="x",
        phase_sequence=(_phase(),),
        closure_predicates=(),
    )
    r1 = walk(m, _state(), {"isp": 340.0})
    r2 = walk(m, _state(), {"isp": 320.0})
    assert r1[0].path_label != r2[0].path_label
