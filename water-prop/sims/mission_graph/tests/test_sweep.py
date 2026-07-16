"""Tests for the sweep harness and the aggregation library."""

from dataclasses import replace
from pathlib import Path

import pytest

from mission_graph.framework import (
    ClosurePredicate,
    Mission,
    Option,
    Phase,
    SweepAxis,
    SweepCell,
    VehicleAxis,
    VehicleState,
    WalkResult,
    load_cells_jsonl,
    save_cells_jsonl,
    sweep,
)
from mission_graph.analysis.sweep_report import (
    architectures_admitted,
    architecture_cell_counts,
    back_propagate,
    best_delivery_per_cell,
    closure_by_cell,
    floor_close_count,
    marginal_closure,
)


# ----- helpers ----------------------------------------------------------- #


def _state(**overrides):
    base = dict(
        mass_kg=1000.0,
        propellant_kg=500.0,
        payload_kg=0.0,
        location="START",
        v_inf_km_s=0.0,
        time_elapsed_s=0.0,
        epoch_jd=0.0,
        power_available_kwe=10.0,
    )
    base.update(overrides)
    return VehicleState(**base)


def _always_feasible_option(option_id, phase_id, new_location="END", deliver_kg=100.0):
    """Option whose executor produces a feasible state with payload_kg=deliver_kg."""
    return Option(
        option_id=option_id,
        description="x",
        phase_id=phase_id,
        precondition=lambda s, p: (True, "ok"),
        executor=lambda s, p, _dk=deliver_kg, _loc=new_location: replace(s, location=_loc, payload_kg=_dk),
        params_required=(),
    )


def _phase(phase_id, options):
    return Phase(phase_id=phase_id, description="x", options=tuple(options))


def _trivial_mission(closure_predicates=()):
    opt = _always_feasible_option("o", "P")
    return Mission(
        mission_id="m",
        objective="x",
        phase_sequence=(_phase("P", [opt]),),
        closure_predicates=tuple(closure_predicates),
    )


# ----- 1. cross-product count ------------------------------------------- #


def test_cross_product_count():
    m = _trivial_mission()
    cells = sweep(
        m,
        _state(),
        {},
        param_axes=[SweepAxis("a", (1.0, 2.0, 3.0))],
        vehicle_axes=[VehicleAxis("m", (1000.0, 2000.0, 3000.0, 4000.0), state_field="mass_kg")],
    )
    assert len(cells) == 12


# ----- 2. zero axes yields one cell ------------------------------------- #


def test_zero_axes_yields_one_cell():
    m = _trivial_mission()
    cells = sweep(m, _state(), {})
    assert len(cells) == 1
    assert cells[0].coords == {}


# ----- 3. vehicle axis overrides state field ---------------------------- #


def test_vehicle_axis_overrides_state_field():
    m = _trivial_mission()
    cells = sweep(
        m,
        _state(),
        {},
        vehicle_axes=[VehicleAxis("mass", (1000.0, 2000.0), state_field="mass_kg")],
    )
    assert len(cells) == 2
    hashes = {c.state_hash for c in cells}
    assert len(hashes) == 2  # different state hashes for different mass values


# ----- 4. param axis overrides param ------------------------------------ #


def test_param_axis_overrides_param():
    m = _trivial_mission()
    cells = sweep(
        m,
        _state(),
        {"isp": 340.0, "other_param": 999.0},
        param_axes=[SweepAxis("isp", (340.0, 400.0))],
    )
    assert len(cells) == 2
    hashes = {c.params_hash for c in cells}
    assert len(hashes) == 2  # different params hashes per cell


# ----- 5. invalid vehicle state is skipped ------------------------------ #


def test_invalid_vehicle_state_skipped():
    m = _trivial_mission()
    # base propellant 500 kg; mass override to 100 (below propellant) violates state validation
    cells = sweep(
        m,
        _state(),
        {},
        vehicle_axes=[VehicleAxis("mass", (100.0, 2000.0), state_field="mass_kg")],
    )
    assert len(cells) == 2
    invalid = [c for c in cells if c.skipped_reason is not None]
    valid = [c for c in cells if c.skipped_reason is None]
    assert len(invalid) == 1
    assert "propellant_kg" in invalid[0].skipped_reason
    assert invalid[0].results == ()
    assert len(valid) == 1
    assert len(valid[0].results) > 0


# ----- 6. JSONL round-trip ---------------------------------------------- #


def test_jsonl_round_trip(tmp_path: Path):
    cp = ClosurePredicate(
        name="reached_end",
        description="x",
        fn=lambda s: "close" if s.location == "END" else "miss",
    )
    m = Mission(
        mission_id="m",
        objective="x",
        phase_sequence=(_phase("P", [_always_feasible_option("o", "P")]),),
        closure_predicates=(cp,),
    )
    cells = sweep(m, _state(), {}, vehicle_axes=[VehicleAxis("mass", (1000.0, 2000.0), state_field="mass_kg")])

    path = tmp_path / "cells.jsonl"
    save_cells_jsonl(cells, path)
    loaded = load_cells_jsonl(path)

    assert len(loaded) == len(cells)
    for orig, back in zip(cells, loaded):
        assert orig.cell_id == back.cell_id
        assert orig.coords == back.coords
        assert orig.params_hash == back.params_hash
        assert orig.state_hash == back.state_hash
        assert len(orig.results) == len(back.results)
        for r_orig, r_back in zip(orig.results, back.results):
            assert r_orig.path_label == r_back.path_label
            assert r_orig.is_feasible == r_back.is_feasible
            assert r_orig.closure_verdicts == r_back.closure_verdicts


# ----- 7. floor_close_count aggregates correctly ------------------------ #


def _mock_walk_result(path_label, is_feasible, verdict):
    """Hand-build a WalkResult for aggregation tests."""
    if is_feasible:
        leaf = _state(mass_kg=500.0, payload_kg=50.0)
        return WalkResult(
            path_label=path_label,
            node_labels=(path_label,),
            leaf_state=leaf,
            closure_verdicts={"floor": verdict},
            infeasible_at=None,
            infeasible_reason=None,
        )
    return WalkResult(
        path_label=path_label,
        node_labels=(path_label,),
        leaf_state=None,
        closure_verdicts={},
        infeasible_at="P",
        infeasible_reason="x",
    )


def test_floor_close_count_aggregation():
    cells = (
        SweepCell(
            cell_id=0,
            coords={"a": 1.0},
            params_hash="aaaaaa",
            state_hash="bbbbbb",
            results=(
                _mock_walk_result("p1", True, "close"),
                _mock_walk_result("p2", True, "miss"),
                _mock_walk_result("p3", False, ""),
            ),
        ),
        SweepCell(
            cell_id=1,
            coords={"a": 2.0},
            params_hash="cccccc",
            state_hash="dddddd",
            results=(
                _mock_walk_result("p1", True, "close_strict"),
                _mock_walk_result("p2", True, "close_waiver"),
            ),
        ),
    )
    counts = floor_close_count(cells, "floor")
    assert counts[0] == (1, 2)  # 1 close out of 2 feasible (p3 infeasible excluded)
    assert counts[1] == (2, 2)  # both close, both feasible


# ----- 8. marginal_closure collapses other axes -------------------------- #


def test_marginal_closure_collapses_other_axes():
    """2-axis 2x3 sweep; marginal on A sums correctly across B.

    Construct: axis A in (10, 20); axis B in (1, 2, 3). At every (A, B)
    cell, one feasible 'close' result and one feasible 'miss' result.
    Marginal on A: for each value of A there are 3 B values each
    contributing (1, 2). Total per A-value = (3, 6).
    """
    cells = []
    cid = 0
    for a in (10.0, 20.0):
        for b in (1.0, 2.0, 3.0):
            cells.append(
                SweepCell(
                    cell_id=cid,
                    coords={"a": a, "b": b},
                    params_hash=f"{cid:06d}",
                    state_hash=f"{cid:06d}",
                    results=(
                        _mock_walk_result(f"p1_c{cid}", True, "close"),
                        _mock_walk_result(f"p2_c{cid}", True, "miss"),
                    ),
                )
            )
            cid += 1

    marginal_a = marginal_closure(tuple(cells), "a", "floor")
    assert marginal_a[10.0] == (3, 6)
    assert marginal_a[20.0] == (3, 6)

    marginal_b = marginal_closure(tuple(cells), "b", "floor")
    # each b value has 2 cells (one per a); each contributes (1, 2)
    for b_val in (1.0, 2.0, 3.0):
        assert marginal_b[b_val] == (2, 4)


# ----- 9. back-propagation surfaces only admitting axis values --------- #


def test_back_propagate_returns_admitting_values():
    cells = (
        SweepCell(
            cell_id=0,
            coords={"a": 10.0, "b": 1.0},
            params_hash="000000",
            state_hash="000000",
            results=(_mock_walk_result("p", True, "miss"),),
        ),
        SweepCell(
            cell_id=1,
            coords={"a": 20.0, "b": 2.0},
            params_hash="000001",
            state_hash="000001",
            results=(_mock_walk_result("p", True, "close"),),
        ),
        SweepCell(
            cell_id=2,
            coords={"a": 30.0, "b": 3.0},
            params_hash="000002",
            state_hash="000002",
            results=(_mock_walk_result("p", True, "close_strict"),),
        ),
    )
    admitting = back_propagate(cells, "floor")
    assert admitting["a"] == {20.0, 30.0}
    assert admitting["b"] == {2.0, 3.0}


# ----- 10. architecture cell counts rank correctly ---------------------- #


def test_architecture_cell_counts():
    cells = (
        SweepCell(
            cell_id=0, coords={}, params_hash="x", state_hash="x",
            results=(
                _mock_walk_result("path_a", True, "close"),
                _mock_walk_result("path_b", True, "miss"),
            ),
        ),
        SweepCell(
            cell_id=1, coords={}, params_hash="x", state_hash="x",
            results=(
                _mock_walk_result("path_a", True, "close"),
                _mock_walk_result("path_c", False, ""),
            ),
        ),
    )
    counts = architecture_cell_counts(cells)
    assert counts["path_a"] == 2  # feasible in both cells
    assert counts["path_b"] == 1  # feasible in cell 0 only
    assert counts.get("path_c", 0) == 0  # never feasible


# ----- 11. state_transform hook scales propellant with mass ------------- #


def test_state_transform_scales_propellant_with_mass():
    """state_transform receives the post-override state + coords and may
    return a derived state. Verify propellant_kg tracks mass_kg via an
    80 percent fraction across the vehicle_mass axis."""
    m = _trivial_mission()

    def scale_prop(state, coords):
        return replace(state, propellant_kg=0.8 * state.mass_kg)

    cells = sweep(
        m,
        _state(propellant_kg=0.0),  # base propellant=0 so override never trips validation
        {},
        vehicle_axes=[VehicleAxis("vehicle_mass_kg", (50_000.0, 100_000.0, 200_000.0), state_field="mass_kg")],
        state_transform=scale_prop,
    )
    assert len(cells) == 3
    # Every cell should have produced a feasible walk (the trivial mission's
    # one option is always feasible) with the scaled propellant baked into
    # the leaf state.
    for cell in cells:
        assert cell.skipped_reason is None
        assert cell.results
        leaf = cell.results[0].leaf_state
        # Trivial mission's executor sets payload but preserves propellant_kg.
        # So leaf.propellant_kg == 0.8 * cell.coords["vehicle_mass_kg"].
        assert leaf.propellant_kg == pytest.approx(0.8 * cell.coords["vehicle_mass_kg"])


# ----- 12. reachable phase tree emitter --------------------------------- #


def test_reachable_phase_tree_excludes_precondition_rejected_edges():
    """The reachable emitter must omit option-to-option edges where the
    downstream option's precondition rejects the upstream's output state.

    Build a two-phase mission where:
      Phase A has two options: stamp_flag (sets a flag) and no_op (does not)
      Phase B has two options: requires_flag and forbids_flag
    Expected realized edges:
      stamp_flag -> requires_flag (precondition passes)
      no_op     -> forbids_flag  (precondition passes)
    Edges that must NOT appear:
      stamp_flag -> forbids_flag
      no_op     -> requires_flag
    """
    from mission_graph.framework import emit_reachable_phase_tree_mermaid

    stamp_flag = Option(
        option_id="stamp_flag",
        description="x", phase_id="PA",
        precondition=lambda s, p: (True, "ok"),
        executor=lambda s, p: replace(s, health_flags=frozenset({"flag"})),
        params_required=(),
    )
    no_op = Option(
        option_id="no_op",
        description="x", phase_id="PA",
        precondition=lambda s, p: (True, "ok"),
        executor=lambda s, p: s,
        params_required=(),
    )
    requires_flag = Option(
        option_id="requires_flag",
        description="x", phase_id="PB",
        precondition=lambda s, p: ("flag" in s.health_flags, "needs flag"),
        executor=lambda s, p: s,
        params_required=(),
    )
    forbids_flag = Option(
        option_id="forbids_flag",
        description="x", phase_id="PB",
        precondition=lambda s, p: ("flag" not in s.health_flags, "must not have flag"),
        executor=lambda s, p: s,
        params_required=(),
    )

    mission = Mission(
        mission_id="precond_check",
        objective="x",
        phase_sequence=(_phase("PA", [stamp_flag, no_op]), _phase("PB", [requires_flag, forbids_flag])),
        closure_predicates=(),
    )

    out = emit_reachable_phase_tree_mermaid(mission, _state(), {}, direction="LR")
    assert "PA__stamp_flag --> PB__requires_flag" in out
    assert "PA__no_op --> PB__forbids_flag" in out
    assert "PA__stamp_flag --> PB__forbids_flag" not in out
    assert "PA__no_op --> PB__requires_flag" not in out
