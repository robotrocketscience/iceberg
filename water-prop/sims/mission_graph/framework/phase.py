"""Phase = a node in the mission timeline carrying its option set.

Granularity is per-phase: cruise phases stay flat; proximity-ops phases may
nest sub-phases (rendezvous / close-approach / grapple under a single
"capture" phase). Walker recurses through sub_phases when present.

A phase with sub_phases ignores its own options field. A phase with options
ignores sub_phases. Mixed is rejected.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple

from .option import Option


@dataclass(frozen=True)
class Phase:
    phase_id: str
    description: str

    options: Tuple[Option, ...] = field(default_factory=tuple)
    sub_phases: Tuple["Phase", ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if self.options and self.sub_phases:
            raise ValueError(
                f"Phase {self.phase_id} has both options and sub_phases; pick one"
            )
        if not self.options and not self.sub_phases:
            raise ValueError(
                f"Phase {self.phase_id} has neither options nor sub_phases"
            )

    @property
    def is_leaf(self) -> bool:
        return bool(self.options)
