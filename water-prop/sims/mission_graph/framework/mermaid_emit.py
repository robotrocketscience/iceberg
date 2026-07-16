"""Emit Mermaid graph blocks describing a Mission's phase-option structure.

Two emitters:

  emit_phase_tree_mermaid(mission)
      Structural view: every phase shows every option, phase-to-phase edges.
      Useful for "what options exist where" but does NOT show which option
      transitions are actually reachable given preconditions.

  emit_reachable_phase_tree_mermaid(mission, probe_state, probe_params)
      Reachable view: each option becomes a node, edges only between option
      pairs (option_i, option_{i+1}) whose preconditions actually pass under
      a walker probe from probe_state with probe_params. This is the
      semantically-correct picture — e.g., it shows that
      multi_falcon_6_launch only transitions to autonomous_assembly /
      depot_relay_assembly, NOT to passthrough_no_assembly, because the
      passthrough precondition requires the absence of a pending-assembly
      health flag that multi-launch options stamp.

Output of both emitters is plain text ready to drop between
```` ```mermaid ```` fences.
"""

from __future__ import annotations

from typing import Dict, List, Mapping, Set, Tuple

from .mission import Mission
from .phase import Phase
from .state import VehicleState
from .walker import walk


def _slug(s: str) -> str:
    """Make an id safe for Mermaid node ids (alphanum + underscore)."""
    return "".join(c if c.isalnum() else "_" for c in s)


def _flatten_phases(phases) -> Tuple[Phase, ...]:
    """Inline sub-phases as the walker does, returning only leaf phases."""
    out: List[Phase] = []
    for p in phases:
        if p.is_leaf:
            out.append(p)
        else:
            out.extend(_flatten_phases(p.sub_phases))
    return tuple(out)


def _emit_phase(phase: Phase, indent: int, lines: List[str], header_ids: List[str]) -> None:
    pad = "  " * indent
    phase_id = _slug(phase.phase_id)
    header_ids.append(phase_id)
    lines.append(f"{pad}subgraph {phase_id}[\"{phase.phase_id}\"]")

    if phase.is_leaf:
        for opt in phase.options:
            node_id = f"{phase_id}__{_slug(opt.option_id)}"
            label = opt.option_id.replace("_", " ")
            lines.append(f"{pad}  {node_id}[\"{label}\"]")
    else:
        for sub in phase.sub_phases:
            _emit_phase(sub, indent + 1, lines, header_ids)

    lines.append(f"{pad}end")


def emit_phase_tree_mermaid(mission: Mission, direction: str = "TD") -> str:
    """Return a Mermaid graph block describing the mission's phase-option
    structure. Phase-to-phase edges only — does NOT show which option-to-
    option transitions are reachable. For the semantically-correct picture
    see emit_reachable_phase_tree_mermaid."""
    if direction not in ("TD", "LR", "BT", "RL"):
        raise ValueError(f"direction must be one of TD/LR/BT/RL, got {direction!r}")

    lines: List[str] = [f"graph {direction}"]
    header_ids: List[str] = []
    for phase in mission.phase_sequence:
        _emit_phase(phase, indent=1, lines=lines, header_ids=header_ids)

    for upstream, downstream in zip(header_ids, header_ids[1:]):
        lines.append(f"  {upstream} --> {downstream}")

    return "\n".join(lines)


def emit_phase_tree_markdown(mission: Mission, direction: str = "TD") -> str:
    """Return the structural Mermaid block wrapped in a fenced
    ```mermaid block, ready to drop into a markdown report."""
    inner = emit_phase_tree_mermaid(mission, direction=direction)
    return f"```mermaid\n{inner}\n```"


def _node_key(label: str) -> str:
    """Strip the params-hash suffix from a walker node label.

    `P0_Earth_to_LEO.falcon_heavy_expended.b1c2d3` -> `P0_Earth_to_LEO.falcon_heavy_expended`
    """
    parts = label.split(".")
    if len(parts) >= 2:
        return f"{parts[0]}.{parts[1]}"
    return label


def emit_reachable_phase_tree_mermaid(
    mission: Mission,
    probe_state,
    probe_params,
    direction: str = "TD",
) -> str:
    """Return a Mermaid graph showing only realized option-to-option edges.

    Walks the mission from one or more probe states / params, then collects
    every (option_i, option_{i+1}) transition the walker actually allowed.
    An infeasibility at option_{i+1} means the precondition rejected the
    transition — that pair is excluded.

    Each leaf option becomes its own node. Phases are still grouped into
    subgraphs for visual organization. Edges are option-to-option.

    probe_state can be a single VehicleState or a sequence of VehicleStates;
    probe_params similarly. If both are sequences they must have the same
    length and are paired positionally. If one is a sequence and the other
    a single value, the single value is broadcast. The reachable edge set
    is the UNION across all probes — useful for surfacing options that
    only appear under specific starting conditions.
    """
    if direction not in ("TD", "LR", "BT", "RL"):
        raise ValueError(f"direction must be one of TD/LR/BT/RL, got {direction!r}")

    # Normalize probe inputs to parallel sequences.
    if isinstance(probe_state, VehicleState):
        probe_states = (probe_state,)
    else:
        probe_states = tuple(probe_state)
    if isinstance(probe_params, Mapping):
        probe_params_list = (probe_params,) * len(probe_states)
    else:
        probe_params_list = tuple(probe_params)
    if len(probe_states) != len(probe_params_list):
        if len(probe_states) == 1:
            probe_states = probe_states * len(probe_params_list)
        elif len(probe_params_list) == 1:
            probe_params_list = probe_params_list * len(probe_states)
        else:
            raise ValueError(
                f"probe_state ({len(probe_states)}) and probe_params "
                f"({len(probe_params_list)}) must be the same length or "
                f"one must be a single value"
            )

    realized_edges: Set[Tuple[str, str]] = set()
    reachable_nodes: Set[str] = set()
    for ps, pp in zip(probe_states, probe_params_list):
        walk_results = walk(mission, ps, pp)
        for r in walk_results:
            labels = r.node_labels
            if not labels:
                continue
            node_keys = tuple(_node_key(lab) for lab in labels)
            n = len(node_keys)
            if r.is_feasible:
                for i in range(n - 1):
                    realized_edges.add((node_keys[i], node_keys[i + 1]))
                reachable_nodes.update(node_keys)
            else:
                # Last node is the one whose precondition rejected the
                # transition INTO it. Earlier edges are realized.
                for i in range(n - 2):
                    realized_edges.add((node_keys[i], node_keys[i + 1]))
                # All nodes except the rejected one are reachable as starts.
                reachable_nodes.update(node_keys[:-1])

    # Group reachable nodes by phase for the subgraph layout.
    by_phase: Dict[str, List[str]] = {}
    for node_key in reachable_nodes:
        phase_id, option_id = node_key.split(".", 1)
        by_phase.setdefault(phase_id, []).append(option_id)

    lines: List[str] = [f"graph {direction}"]
    for phase in _flatten_phases(mission.phase_sequence):
        phase_id = phase.phase_id
        opts = sorted(set(by_phase.get(phase_id, [])))
        if not opts:
            continue
        lines.append(f'  subgraph {_slug(phase_id)}["{phase_id}"]')
        for opt_id in opts:
            node_id = f"{_slug(phase_id)}__{_slug(opt_id)}"
            lines.append(f'    {node_id}["{opt_id.replace("_", " ")}"]')
        lines.append("  end")

    for src, dst in sorted(realized_edges):
        src_phase, src_opt = src.split(".", 1)
        dst_phase, dst_opt = dst.split(".", 1)
        src_id = f"{_slug(src_phase)}__{_slug(src_opt)}"
        dst_id = f"{_slug(dst_phase)}__{_slug(dst_opt)}"
        lines.append(f"  {src_id} --> {dst_id}")

    return "\n".join(lines)


def emit_reachable_phase_tree_markdown(
    mission: Mission,
    probe_state: VehicleState,
    probe_params: Mapping[str, float],
    direction: str = "TD",
) -> str:
    """Return the reachable Mermaid block wrapped in a fenced
    ```mermaid block, ready to drop into a markdown report."""
    inner = emit_reachable_phase_tree_mermaid(
        mission, probe_state, probe_params, direction=direction
    )
    return f"```mermaid\n{inner}\n```"
