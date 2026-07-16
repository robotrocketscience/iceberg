"""Vehicle state at a phase boundary.

Carried between phase executors. Frozen so it can hash for sweep memoization.
Phases produce a new state via dataclasses.replace rather than mutating.

Fields are deliberately minimal at v0. Add only when a phase needs them and
multiple phases will read them. Anything single-phase belongs in that phase's
local scratch, not here.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import FrozenSet, Optional


@dataclass(frozen=True)
class VehicleState:
    mass_kg: float
    propellant_kg: float
    payload_kg: float

    location: str
    v_inf_km_s: float

    time_elapsed_s: float
    epoch_jd: Optional[float]

    power_available_kwe: float

    health_flags: FrozenSet[str] = field(default_factory=frozenset)

    # Cumulative reactor full-power ON time across the mission, in hours.
    # Accumulated by electric-propulsion executors (reactor-driven thrust legs
    # only; chemical burns do not add to it). Read by the reactor-lifetime
    # precondition (R-framework-matrix-parity constraint 1): an electric option
    # is infeasible when projected cumulative burn would exceed
    # params['reactor_lifetime_years'] * 8760. Defaults to 0.0 so all existing
    # VehicleState constructions and the lifetime-off baseline are unchanged.
    cumulative_full_power_burn_hours: float = 0.0

    def __post_init__(self) -> None:
        if self.mass_kg < 0:
            raise ValueError(f"mass_kg must be >= 0, got {self.mass_kg}")
        if self.propellant_kg < 0:
            raise ValueError(f"propellant_kg must be >= 0, got {self.propellant_kg}")
        if self.propellant_kg > self.mass_kg:
            raise ValueError(
                f"propellant_kg ({self.propellant_kg}) cannot exceed mass_kg ({self.mass_kg})"
            )
        if self.payload_kg < 0:
            raise ValueError(f"payload_kg must be >= 0, got {self.payload_kg}")
        if self.power_available_kwe < 0:
            raise ValueError(
                f"power_available_kwe must be >= 0, got {self.power_available_kwe}"
            )
        if self.cumulative_full_power_burn_hours < 0:
            raise ValueError(
                f"cumulative_full_power_burn_hours must be >= 0, got "
                f"{self.cumulative_full_power_burn_hours}"
            )
