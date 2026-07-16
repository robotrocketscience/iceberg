"""Best-architecture report at the new provisional L0-04 floor of 25 tonnes.

Reads the latest canonical sweep cells.jsonl, finds all feasible paths
that deliver >= 25 t at LEO_depot, ranks them by delivered tonnage and
by frequency (cell count), and writes a markdown report.
"""

from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve()
SIMS = HERE.parents[2] / "sims"
sys.path.insert(0, str(SIMS))

from mission_graph.framework import load_cells_jsonl  # noqa: E402

CANONICAL_RUN = HERE.parents[2] / "sims/mission_graph/runs/20260521T193329Z/cells.jsonl"
FLOOR_KG = 25_000.0


def main():
    cells = load_cells_jsonl(CANONICAL_RUN)
    print(f"Loaded {len(cells)} cells from {CANONICAL_RUN.name}")

    # Find all feasible paths >= 25 t at LEO_depot.
    qualifying = []
    for cell in cells:
        for r in cell.results:
            if not r.is_feasible:
                continue
            if r.leaf_state.location != "LEO_depot":
                continue
            if r.leaf_state.payload_kg < FLOOR_KG:
                continue
            qualifying.append((cell, r))

    print(f"\nFound {len(qualifying)} feasible paths delivering >= 25 t at LEO_depot")

    if not qualifying:
        print("No qualifying paths. Exiting.")
        return

    # Aggregate by architecture (path_label).
    arch_counts = defaultdict(int)
    arch_best_payload = defaultdict(float)
    arch_best_time = defaultdict(float)
    arch_coords = defaultdict(list)
    for cell, r in qualifying:
        # Strip params-hash to get the architecture signature.
        arch = " -> ".join(lab.split(".")[1] for lab in r.node_labels)
        arch_counts[arch] += 1
        if r.leaf_state.payload_kg > arch_best_payload[arch]:
            arch_best_payload[arch] = r.leaf_state.payload_kg
            arch_best_time[arch] = r.leaf_state.time_elapsed_s
        arch_coords[arch].append(dict(cell.coords))

    # Top 10 by frequency.
    top_by_freq = sorted(arch_counts.items(), key=lambda kv: -kv[1])[:10]

    # Top 10 by best delivered payload.
    top_by_payload = sorted(arch_best_payload.items(), key=lambda kv: -kv[1])[:10]

    out_lines = []
    out_lines.append("# Best architectures at L0-04 floor = 25 tonnes")
    out_lines.append("")
    out_lines.append(f"Source: `{CANONICAL_RUN.relative_to(HERE.parents[2])}` (4-axis canonical sweep, 625 cells).")
    out_lines.append(f"Total feasible paths delivering >= 25 t at LEO_depot: **{len(qualifying)}**.")
    out_lines.append(f"Total unique architectures: **{len(arch_counts)}**.")
    out_lines.append("")
    out_lines.append("## Top 10 architectures by cell-coverage (most robust across sweep)")
    out_lines.append("")
    out_lines.append("| rank | cells | best payload (t) | round-trip (yr) | architecture |")
    out_lines.append("|---:|---:|---:|---:|---|")
    for i, (arch, count) in enumerate(top_by_freq, 1):
        best_t = arch_best_payload[arch] / 1000
        best_yr = arch_best_time[arch] / (365.25 * 86_400)
        out_lines.append(f"| {i} | {count} | {best_t:.1f} | {best_yr:.2f} | {arch} |")
    out_lines.append("")
    out_lines.append("## Top 10 architectures by maximum delivered payload")
    out_lines.append("")
    out_lines.append("| rank | best payload (t) | round-trip (yr) | cells | architecture |")
    out_lines.append("|---:|---:|---:|---:|---|")
    for i, (arch, payload) in enumerate(top_by_payload, 1):
        out_lines.append(
            f"| {i} | {payload/1000:.1f} | {arch_best_time[arch] / (365.25 * 86_400):.2f} | "
            f"{arch_counts[arch]} | {arch} |"
        )
    out_lines.append("")

    # Which axis values appear in qualifying cells?
    out_lines.append("## Axis values that admit >= 25-tonne delivery")
    out_lines.append("")
    axis_values = defaultdict(set)
    for cell, r in qualifying:
        for axis, val in cell.coords.items():
            axis_values[axis].add(val)
    for axis in sorted(axis_values.keys()):
        vals = sorted(axis_values[axis])
        out_lines.append(f"- **{axis}**: {{{', '.join(str(v) for v in vals)}}}")
    out_lines.append("")

    # Specific concrete example: the best single architecture/cell pair.
    best_cell, best_r = max(qualifying, key=lambda cr: cr[1].leaf_state.payload_kg)
    out_lines.append("## Highest-delivery single path")
    out_lines.append("")
    out_lines.append(f"- **Delivered: {best_r.leaf_state.payload_kg / 1000:.2f} tonnes at LEO_depot**")
    out_lines.append(f"- Round-trip time: {best_r.leaf_state.time_elapsed_s / (365.25 * 86_400):.2f} years")
    out_lines.append(f"- Architecture: `{' -> '.join(lab.split('.')[1] for lab in best_r.node_labels)}`")
    out_lines.append(f"- Cell coordinates:")
    for k, v in sorted(best_cell.coords.items()):
        out_lines.append(f"  - {k}: {v}")
    out_lines.append("")

    report_path = HERE.parent / "BEST_ARCHITECTURES_25T.md"
    report_path.write_text("\n".join(out_lines))
    print(f"\nWrote {report_path}")

    # Echo the highlights.
    print()
    print(f"Highest-delivery: {best_r.leaf_state.payload_kg / 1000:.1f} t / {best_r.leaf_state.time_elapsed_s/(365.25*86_400):.1f} yr")
    print(f"Most robust (top-frequency) architecture: {top_by_freq[0][0]}")
    print(f"  appears in {top_by_freq[0][1]} cells; best payload {arch_best_payload[top_by_freq[0][0]]/1000:.1f} t")


if __name__ == "__main__":
    main()
