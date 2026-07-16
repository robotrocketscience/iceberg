"""Parameter-grid sweeper around walk().

Sweeps independent grids over (a) VehicleState fields and (b) params dict
entries, calls walk() once per grid cell, and accumulates the results as
SweepCell records. Pure outer-loop; no walker / physics / state-schema
changes.

Cells that fail VehicleState.__post_init__ validation (e.g. axis value
producing propellant_kg > mass_kg) are NOT skipped silently — they are
recorded with `skipped_reason` set and `results=()` so downstream
aggregators can count them.

JSONL persistence uses a lean schema:
  - drop `node_labels` (path_label is the canonical identifier)
  - drop `closure_verdicts` for infeasible results (always empty by design)
  - drop `leaf_state` for infeasible results (always None by design)
"""

from __future__ import annotations

import dataclasses
import hashlib
import itertools
import json
from dataclasses import dataclass, field, fields
from pathlib import Path
from typing import Callable, Iterable, Mapping, Optional, Sequence, Tuple

from .labels import canonicalize_params, params_hash
from .mission import Mission
from .state import VehicleState
from .walker import WalkResult, walk


_VEHICLE_STATE_FIELDS = {f.name for f in fields(VehicleState)}


@dataclass(frozen=True)
class SweepAxis:
    """One axis of the parameter grid."""

    name: str
    values: Tuple[float, ...]

    def __post_init__(self) -> None:
        if not self.values:
            raise ValueError(f"SweepAxis {self.name!r} needs at least one value")


@dataclass(frozen=True)
class VehicleAxis:
    """One axis of the starting-state grid. Targets a single VehicleState field."""

    name: str
    values: Tuple[float, ...]
    state_field: str

    def __post_init__(self) -> None:
        if not self.values:
            raise ValueError(f"VehicleAxis {self.name!r} needs at least one value")
        if self.state_field not in _VEHICLE_STATE_FIELDS:
            raise ValueError(
                f"VehicleAxis {self.name!r} targets unknown state field "
                f"{self.state_field!r}; valid fields: {sorted(_VEHICLE_STATE_FIELDS)}"
            )


@dataclass(frozen=True)
class SweepCell:
    """One grid point: coordinates, hashes for joinability, walk results."""

    cell_id: int
    coords: Mapping[str, float]
    params_hash: str
    state_hash: str
    results: Tuple[WalkResult, ...]
    skipped_reason: Optional[str] = None


def _state_hash(state: VehicleState, length: int = 6) -> str:
    """Short hex hash of the canonicalized VehicleState fields."""
    flat = {
        "mass_kg": state.mass_kg,
        "propellant_kg": state.propellant_kg,
        "payload_kg": state.payload_kg,
        "location": state.location,
        "v_inf_km_s": state.v_inf_km_s,
        "time_elapsed_s": state.time_elapsed_s,
        "epoch_jd": state.epoch_jd if state.epoch_jd is not None else "null",
        "power_available_kwe": state.power_available_kwe,
        "health_flags": sorted(state.health_flags),
    }
    digest = hashlib.sha256(
        json.dumps(flat, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return digest[:length]


def sweep(
    mission: Mission,
    base_state: VehicleState,
    base_params: Mapping[str, float],
    param_axes: Sequence[SweepAxis] = (),
    vehicle_axes: Sequence[VehicleAxis] = (),
    progress_every: Optional[int] = None,
    state_transform: Optional[Callable[[VehicleState, Mapping[str, float]], VehicleState]] = None,
) -> Tuple[SweepCell, ...]:
    """Cross-product sweep over the supplied axes.

    For each grid point: override base_state with the cell's vehicle-axis
    values, override base_params with the cell's param-axis values, run
    walk() and record results in a SweepCell. Cells whose state values
    violate VehicleState validation are recorded with skipped_reason set.

    state_transform (optional): callable invoked after vehicle-axis overrides
    are applied. Signature `(state, coords) -> state`. Use this to derive
    fields from sweep coordinates — for example, scaling propellant_kg with
    mass_kg so the propellant fraction stays constant across the mass axis.
    """
    v_axes = tuple(vehicle_axes)
    p_axes = tuple(param_axes)
    v_value_lists = [a.values for a in v_axes]
    p_value_lists = [a.values for a in p_axes]
    combos = itertools.product(*(v_value_lists + p_value_lists))

    cells = []
    cell_id = 0
    for combo in combos:
        v_part = combo[: len(v_axes)]
        p_part = combo[len(v_axes):]

        vehicle_overrides = {a.state_field: v for a, v in zip(v_axes, v_part)}
        param_overrides = {a.name: v for a, v in zip(p_axes, p_part)}

        coords = {a.name: v for a, v in zip(v_axes, v_part)}
        coords.update({a.name: v for a, v in zip(p_axes, p_part)})

        cell_params = {**dict(base_params), **param_overrides}
        try:
            cell_state = dataclasses.replace(base_state, **vehicle_overrides)
            if state_transform is not None:
                cell_state = state_transform(cell_state, dict(coords))
        except ValueError as exc:
            cells.append(
                SweepCell(
                    cell_id=cell_id,
                    coords=dict(coords),
                    params_hash=params_hash(cell_params),
                    state_hash="invalid",
                    results=(),
                    skipped_reason=str(exc),
                )
            )
            cell_id += 1
            continue

        results = walk(mission, cell_state, cell_params)
        cells.append(
            SweepCell(
                cell_id=cell_id,
                coords=dict(coords),
                params_hash=params_hash(cell_params),
                state_hash=_state_hash(cell_state),
                results=results,
                skipped_reason=None,
            )
        )
        cell_id += 1

        if progress_every is not None and cell_id % progress_every == 0:
            print(f"  swept {cell_id} cells")

    return tuple(cells)


def _result_to_jsonable(r: WalkResult) -> dict:
    """Lean JSON-friendly view: drop fields that are always empty/None for
    infeasible results, drop node_labels (path_label is canonical)."""
    out = {
        "path_label": r.path_label,
        "infeasible_at": r.infeasible_at,
        "infeasible_reason": r.infeasible_reason,
    }
    if r.is_feasible:
        leaf = r.leaf_state
        out["leaf_state"] = {
            "mass_kg": leaf.mass_kg,
            "propellant_kg": leaf.propellant_kg,
            "payload_kg": leaf.payload_kg,
            "location": leaf.location,
            "v_inf_km_s": leaf.v_inf_km_s,
            "time_elapsed_s": leaf.time_elapsed_s,
            "epoch_jd": leaf.epoch_jd,
            "power_available_kwe": leaf.power_available_kwe,
            "health_flags": sorted(leaf.health_flags),
        }
        out["closure_verdicts"] = dict(r.closure_verdicts)
    return out


def _jsonable_to_result(d: dict) -> WalkResult:
    if d.get("leaf_state") is not None:
        leaf_dict = dict(d["leaf_state"])
        leaf_dict["health_flags"] = frozenset(leaf_dict.get("health_flags", []))
        leaf = VehicleState(**leaf_dict)
        verdicts = dict(d.get("closure_verdicts", {}))
    else:
        leaf = None
        verdicts = {}
    return WalkResult(
        path_label=d["path_label"],
        node_labels=tuple(d["path_label"].split(" -> ")) if d["path_label"] else (),
        leaf_state=leaf,
        closure_verdicts=verdicts,
        infeasible_at=d.get("infeasible_at"),
        infeasible_reason=d.get("infeasible_reason"),
    )


def save_cells_jsonl(cells: Iterable[SweepCell], path: Path) -> None:
    """Write one JSON record per cell to `path`."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        for cell in cells:
            record = {
                "cell_id": cell.cell_id,
                "coords": dict(cell.coords),
                "params_hash": cell.params_hash,
                "state_hash": cell.state_hash,
                "skipped_reason": cell.skipped_reason,
                "results": [_result_to_jsonable(r) for r in cell.results],
            }
            f.write(json.dumps(record) + "\n")


def load_cells_jsonl(path: Path) -> Tuple[SweepCell, ...]:
    """Load cells written by save_cells_jsonl."""
    path = Path(path)
    cells = []
    with path.open("r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            d = json.loads(line)
            cells.append(
                SweepCell(
                    cell_id=d["cell_id"],
                    coords=dict(d["coords"]),
                    params_hash=d["params_hash"],
                    state_hash=d["state_hash"],
                    results=tuple(_jsonable_to_result(r) for r in d.get("results", [])),
                    skipped_reason=d.get("skipped_reason"),
                )
            )
    return tuple(cells)
