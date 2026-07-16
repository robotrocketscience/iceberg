"""Option = one way to execute a phase.

Each option declares:
  - a precondition predicate against incoming state + params (gates feasibility)
  - an executor that produces the outgoing state
  - the parameter names it consumes

Pruning at sweep time uses precondition; the (parent_option.output_state) is
checked against (child_option.precondition) before the child is expanded.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Mapping, Tuple

from .state import VehicleState


Params = Mapping[str, float]
PreconditionFn = Callable[[VehicleState, Params], Tuple[bool, str]]
ExecutorFn = Callable[[VehicleState, Params], VehicleState]


@dataclass(frozen=True)
class Option:
    option_id: str
    description: str
    phase_id: str

    precondition: PreconditionFn
    executor: ExecutorFn

    params_required: Tuple[str, ...]

    notes: str = ""
