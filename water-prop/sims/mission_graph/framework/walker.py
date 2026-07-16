"""Walker — enumerate all paths through a mission and report each leaf.

For every option in every phase, the walker:
  1. Runs the option's precondition against the current vehicle state.
  2. If infeasible, records a stub result with the path-so-far + reason.
  3. If feasible, runs the executor to produce the next state and recurses.

When the phase sequence is exhausted, the walker applies every closure
predicate to the leaf state and packages the result.

Phases with sub_phases are flattened in-place — the walker descends into
them as if they were the next entries in the main phase sequence.

This is the minimum viable walker. It does:
  - one full enumeration per call
  - no memoization
  - no parameter sweeping (one params dict per call)
  - no failure-mode layer (no nominal / abort_salvage etc.)

Those belong in v1+.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Optional, Tuple

from .labels import node_label, path_label
from .mission import Mission, ClosurePredicate
from .phase import Phase
from .state import VehicleState


@dataclass(frozen=True)
class WalkResult:
    path_label: str
    node_labels: Tuple[str, ...]
    leaf_state: Optional[VehicleState]
    closure_verdicts: Mapping[str, str]
    infeasible_at: Optional[str]
    infeasible_reason: Optional[str]

    @property
    def is_feasible(self) -> bool:
        return self.infeasible_at is None


def walk(mission: Mission, start_state: VehicleState, params: Mapping[str, float]) -> Tuple[WalkResult, ...]:
    """Enumerate all paths through `mission` from `start_state` under `params`."""
    results: list[WalkResult] = []
    _walk_phases(
        phases=tuple(mission.phase_sequence),
        state=start_state,
        params=params,
        node_labels_so_far=(),
        results=results,
        closure_predicates=mission.closure_predicates,
    )
    return tuple(results)


def _walk_phases(
    phases: Tuple[Phase, ...],
    state: VehicleState,
    params: Mapping[str, float],
    node_labels_so_far: Tuple[str, ...],
    results: list,
    closure_predicates: Tuple[ClosurePredicate, ...],
) -> None:
    if not phases:
        verdicts = {cp.name: cp.fn(state) for cp in closure_predicates}
        results.append(
            WalkResult(
                path_label=path_label(node_labels_so_far),
                node_labels=node_labels_so_far,
                leaf_state=state,
                closure_verdicts=verdicts,
                infeasible_at=None,
                infeasible_reason=None,
            )
        )
        return

    current = phases[0]
    remaining = phases[1:]

    if not current.is_leaf:
        flattened = tuple(current.sub_phases) + remaining
        _walk_phases(flattened, state, params, node_labels_so_far, results, closure_predicates)
        return

    for option in current.options:
        label = node_label(current.phase_id, option.option_id, params)
        feasible, reason = option.precondition(state, params)
        new_node_labels = node_labels_so_far + (label,)

        if not feasible:
            results.append(
                WalkResult(
                    path_label=path_label(new_node_labels),
                    node_labels=new_node_labels,
                    leaf_state=None,
                    closure_verdicts={},
                    infeasible_at=current.phase_id,
                    infeasible_reason=reason,
                )
            )
            continue

        next_state = option.executor(state, params)
        _walk_phases(remaining, next_state, params, new_node_labels, results, closure_predicates)
