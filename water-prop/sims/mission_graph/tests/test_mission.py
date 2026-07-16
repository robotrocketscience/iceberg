"""Mission: phase sequence required, no duplicate phase_ids."""

import pytest

from mission_graph.framework import (
    ClosurePredicate,
    Mission,
    Option,
    Phase,
)


def _option(option_id="opt", phase_id="P"):
    return Option(
        option_id=option_id,
        description="x",
        phase_id=phase_id,
        precondition=lambda s, p: (True, "ok"),
        executor=lambda s, p: s,
        params_required=(),
    )


def _phase(phase_id="P"):
    return Phase(phase_id=phase_id, description="x", options=(_option(phase_id=phase_id),))


def test_constructs_with_phases_and_predicates():
    ph = _phase()
    cp = ClosurePredicate(name="c", description="x", fn=lambda s: "close")
    m = Mission(
        mission_id="m1", objective="x", phase_sequence=(ph,), closure_predicates=(cp,)
    )
    assert m.mission_id == "m1"
    assert len(m.phase_sequence) == 1
    assert len(m.closure_predicates) == 1


def test_rejects_empty_phase_sequence():
    with pytest.raises(ValueError, match="no phases"):
        Mission(
            mission_id="m1",
            objective="x",
            phase_sequence=(),
            closure_predicates=(),
        )


def test_rejects_duplicate_phase_ids():
    p1 = _phase(phase_id="P_dup")
    p2 = _phase(phase_id="P_dup")
    with pytest.raises(ValueError, match="duplicate phase_id"):
        Mission(
            mission_id="m1",
            objective="x",
            phase_sequence=(p1, p2),
            closure_predicates=(),
        )


def test_zero_closure_predicates_is_allowed():
    Mission(
        mission_id="m1",
        objective="x",
        phase_sequence=(_phase(),),
        closure_predicates=(),
    )
