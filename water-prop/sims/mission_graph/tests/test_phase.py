"""Phase: options XOR sub_phases exclusivity, is_leaf, both-empty rejection."""

import pytest

from mission_graph.framework import Option, Phase, VehicleState


def _noop_pre(s, p):
    return (True, "ok")


def _noop_exec(s, p):
    return s


def _option(option_id="opt_a", phase_id="P_test"):
    return Option(
        option_id=option_id,
        description="test option",
        phase_id=phase_id,
        precondition=_noop_pre,
        executor=_noop_exec,
        params_required=(),
    )


def test_leaf_phase_with_options():
    opt = _option()
    ph = Phase(phase_id="P_test", description="x", options=(opt,))
    assert ph.is_leaf
    assert ph.options == (opt,)
    assert ph.sub_phases == ()


def test_nested_phase_with_sub_phases():
    leaf = Phase(phase_id="P_sub", description="x", options=(_option(),))
    nested = Phase(phase_id="P_parent", description="x", sub_phases=(leaf,))
    assert not nested.is_leaf
    assert nested.sub_phases == (leaf,)
    assert nested.options == ()


def test_rejects_both_options_and_sub_phases():
    opt = _option()
    leaf = Phase(phase_id="P_sub", description="x", options=(opt,))
    with pytest.raises(ValueError, match="both options and sub_phases"):
        Phase(
            phase_id="P_mixed",
            description="x",
            options=(opt,),
            sub_phases=(leaf,),
        )


def test_rejects_empty_phase():
    with pytest.raises(ValueError, match="neither options nor sub_phases"):
        Phase(phase_id="P_empty", description="x")


def test_phase_is_frozen():
    opt = _option()
    ph = Phase(phase_id="P_test", description="x", options=(opt,))
    with pytest.raises(Exception):
        ph.options = ()  # type: ignore[misc]
