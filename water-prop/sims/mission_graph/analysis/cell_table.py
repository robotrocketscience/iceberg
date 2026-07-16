"""ASCII / markdown formatters for sweep aggregation output.

Pure presentation. Takes already-aggregated dicts from sweep_report and
emits strings. No I/O, no mutation. Missing-cell glyph is '-' to match
the campaign matrix convention.
"""

from __future__ import annotations

from typing import Mapping, Sequence, Set, Tuple

from ..framework import SweepCell


_MISSING = "-"


def format_headline(n_close: int, n_total: int, label: str) -> str:
    """The matrix's standard 'X of N close at conditions Y' line."""
    if n_total == 0:
        return f"{label}: {_MISSING}"
    pct = 100.0 * n_close / n_total
    return f"{label}: {n_close} of {n_total} close ({pct:.1f}%)"


def format_marginal_line(
    marginal: Mapping[float, Tuple[int, int]],
    axis_name: str,
) -> str:
    """One-axis bar: 'axis=v: n/N (pct%)'."""
    lines = [f"## marginal closure on {axis_name}"]
    for axis_val in sorted(marginal.keys()):
        n_close, n_total = marginal[axis_val]
        if n_total == 0:
            lines.append(f"  {axis_name}={axis_val}: {_MISSING}")
            continue
        pct = 100.0 * n_close / n_total
        lines.append(
            f"  {axis_name}={axis_val}: {n_close}/{n_total} ({pct:.1f}%)"
        )
    return "\n".join(lines)


def format_back_propagation(admitting: Mapping[str, Set[float]]) -> str:
    """Bulleted list of 'axis: {v1, v2, ...}' showing values that admit
    at least one closing path."""
    lines = ["## back-propagation: axis values that admit closure"]
    if not admitting:
        lines.append("  (no axis value admits any closing path)")
        return "\n".join(lines)
    for axis_name in sorted(admitting.keys()):
        values = sorted(admitting[axis_name])
        val_str = ", ".join(str(v) for v in values)
        lines.append(f"  {axis_name}: {{{val_str}}}")
    return "\n".join(lines)


def project_to_2d(
    cells: Sequence[SweepCell],
    row_axis: str,
    col_axis: str,
    closure: Mapping[int, Tuple[int, int]],
) -> dict:
    """Project sweep cells into a 2D map of (row_val, col_val) ->
    (n_close, n_total), collapsing all other axes by summation.

    `closure` is the per-cell closure dict from floor_close_count.
    Cells missing one of the projection axes are dropped.
    """
    out: dict = {}
    for cell in cells:
        if row_axis not in cell.coords or col_axis not in cell.coords:
            continue
        key = (cell.coords[row_axis], cell.coords[col_axis])
        prev = out.get(key, (0, 0))
        n_close, n_total = closure.get(cell.cell_id, (0, 0))
        out[key] = (prev[0] + n_close, prev[1] + n_total)
    return out


def format_2d_closure_table(
    table: Mapping[Tuple[float, float], Tuple[int, int]],
    row_axis: str,
    col_axis: str,
    row_values: Sequence[float],
    col_values: Sequence[float],
) -> str:
    """Markdown table with n_close/n_total per cell. Sorted row + column
    axes. Missing cells render as '-'."""
    header_cells = [f"{row_axis} \\ {col_axis}"] + [str(c) for c in col_values]
    sep = ["---"] * len(header_cells)

    lines = []
    lines.append("| " + " | ".join(header_cells) + " |")
    lines.append("| " + " | ".join(sep) + " |")
    for row_val in row_values:
        row_cells = [str(row_val)]
        for col_val in col_values:
            entry = table.get((row_val, col_val))
            if entry is None or entry[1] == 0:
                row_cells.append(_MISSING)
                continue
            n_close, n_total = entry
            row_cells.append(f"{n_close}/{n_total}")
        lines.append("| " + " | ".join(row_cells) + " |")
    return "\n".join(lines)


def format_architecture_ranking(
    counts: Mapping[str, int],
    top_n: int = 10,
) -> str:
    """Top-N architectures by cell-feasibility count. Tracks 'which paths
    work across the broadest swath of the parameter space'."""
    lines = ["## architectures admitted by cell count (top N)"]
    sorted_paths = sorted(counts.items(), key=lambda kv: -kv[1])[:top_n]
    if not sorted_paths:
        lines.append("  (no feasible paths anywhere in sweep)")
        return "\n".join(lines)
    for path_label, count in sorted_paths:
        # strip phase hash suffixes for readability
        chain = " -> ".join(p.split(".")[1] for p in path_label.split(" -> "))
        if len(chain) > 100:
            chain = chain[:97] + "..."
        lines.append(f"  {count:>4d}  {chain}")
    return "\n".join(lines)
