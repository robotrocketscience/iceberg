"""Mission = an ordered phase sequence plus the closure predicates that
classify a completed path.

One Mission per mission objective (Saturn-water, low-Earth-orbit debris demo,
cislunar pathfinder, etc.). Phases that recur across missions should be
defined once and referenced, not copied.

Closure predicates are applied to the final state after the last phase
executes. They return a verdict tag (e.g., "close_strict", "close_waiver",
"miss") so a single sweep can be re-classified under different L-requirement
policies without re-running.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Tuple

from .phase import Phase
from .state import VehicleState


ClosurePredicateFn = Callable[[VehicleState], str]


@dataclass(frozen=True)
class ClosurePredicate:
    name: str
    description: str
    fn: ClosurePredicateFn


@dataclass(frozen=True)
class Mission:
    mission_id: str
    objective: str
    phase_sequence: Tuple[Phase, ...]
    closure_predicates: Tuple[ClosurePredicate, ...]

    def __post_init__(self) -> None:
        if not self.phase_sequence:
            raise ValueError(f"Mission {self.mission_id} has no phases")
        seen = set()
        for phase in self.phase_sequence:
            if phase.phase_id in seen:
                raise ValueError(
                    f"Mission {self.mission_id} has duplicate phase_id {phase.phase_id}"
                )
            seen.add(phase.phase_id)
