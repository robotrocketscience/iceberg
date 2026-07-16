"""Streamlit dashboard for the ICEBERG mission-graph sweep.

Loads cells.jsonl from any runs/<timestamp>/ directory and presents:
  - Headline (X of N close on a chosen closure predicate)
  - 2D closure-surface heatmap (chosen row axis x chosen column axis)
  - Marginal closure bars per axis
  - Top architectures by cell-feasibility count
  - Phase tree (Mermaid block, rendered as code)
  - Best-delivery readout for the selected filter combination

Run from water-prop/ with:
  uv run streamlit run sims/mission_graph/missions/sweeps/streamlit_app.py

Sliders re-filter the precomputed cells. The dashboard does NOT re-run
walk() — use saturn_water_canonical_sweep.py to regenerate the JSONL.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import List

import streamlit as st
import streamlit.components.v1 as components


def _ensure_import_path():
    here = Path(__file__).resolve()
    sims_dir = here.parents[3]
    if str(sims_dir) not in sys.path:
        sys.path.insert(0, str(sims_dir))


_ensure_import_path()


import plotly.express as px  # noqa: E402
import plotly.graph_objects as go  # noqa: E402

from mission_graph.framework import (  # noqa: E402
    VehicleState,
    emit_phase_tree_mermaid,
    emit_reachable_phase_tree_mermaid,
    load_cells_jsonl,
)
from mission_graph.analysis.sweep_report import (  # noqa: E402
    architecture_cell_counts,
    back_propagate,
    best_delivery_per_cell,
    floor_close_count,
    marginal_closure,
)
from mission_graph.missions.saturn_water_v0 import saturn_water_v0  # noqa: E402


RUNS_DIR = Path(__file__).resolve().parents[2] / "runs"


@st.cache_data(show_spinner=False)
def _load_run(jsonl_path: str):
    return load_cells_jsonl(Path(jsonl_path))


def _list_runs() -> List[Path]:
    if not RUNS_DIR.exists():
        return []
    return sorted(
        (d for d in RUNS_DIR.iterdir() if d.is_dir() and (d / "cells.jsonl").exists()),
        reverse=True,
    )


def _axis_values_in_cells(cells, axis_name: str):
    vals = set()
    for c in cells:
        if axis_name in c.coords:
            vals.add(c.coords[axis_name])
    return sorted(vals)


def _render_mermaid(src: str, height: int = 800) -> None:
    """Render a Mermaid block inline using mermaid.js from a CDN.

    Streamlit has no native Mermaid support, so we inject a small HTML
    document containing the diagram source plus the mermaid.js loader.
    """
    html = f"""
    <div class="mermaid" style="background: white; padding: 12px; border-radius: 6px;">
{src}
    </div>
    <script type="module">
      import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs";
      mermaid.initialize({{ startOnLoad: true, theme: "default", securityLevel: "loose" }});
    </script>
    """
    components.html(html, height=height, scrolling=True)


def main():
    st.set_page_config(
        page_title="ICEBERG closure-surface explorer",
        layout="wide",
    )
    st.title("ICEBERG closure-surface explorer")
    st.caption("Read-only view over a sweep cells.jsonl. Use saturn_water_canonical_sweep.py to regenerate.")

    runs = _list_runs()
    if not runs:
        st.error(
            f"No runs found under {RUNS_DIR}. Run "
            "`uv run python sims/mission_graph/missions/sweeps/"
            "saturn_water_canonical_sweep.py` first."
        )
        return

    with st.sidebar:
        st.header("Run")
        selected = st.selectbox(
            "sweep run",
            runs,
            format_func=lambda p: p.name,
        )
        cells = _load_run(str(selected / "cells.jsonl"))
        st.write(f"{len(cells)} cells loaded")

        # Closure-predicate choice (read off the first feasible cell to discover them).
        predicate_names = []
        for c in cells:
            for r in c.results:
                if r.is_feasible:
                    predicate_names = sorted(r.closure_verdicts.keys())
                    break
            if predicate_names:
                break
        predicate = st.selectbox("closure predicate", predicate_names, index=0)

        # Axis discovery.
        all_axes = set()
        for c in cells:
            all_axes.update(c.coords.keys())
        axis_names = sorted(all_axes)

        st.header("Heatmap")
        row_axis = st.selectbox("row axis", axis_names, index=0)
        col_axis_choices = [a for a in axis_names if a != row_axis]
        col_axis = st.selectbox("column axis", col_axis_choices, index=0)

        st.header("Filter (other axes)")
        filter_values = {}
        for ax in axis_names:
            if ax in (row_axis, col_axis):
                continue
            vals = _axis_values_in_cells(cells, ax)
            sel = st.selectbox(f"{ax}", ["(all)"] + [str(v) for v in vals], index=0)
            if sel != "(all)":
                filter_values[ax] = float(sel)

    # Apply filters.
    filtered = [
        c for c in cells
        if all(c.coords.get(k) == v for k, v in filter_values.items())
    ]
    st.write(f"**{len(filtered)} cells** after filter")

    # Headline.
    floor = floor_close_count(filtered, predicate)
    total_close = sum(nc for nc, _ in floor.values())
    total_total = sum(nt for _, nt in floor.values())
    pct = 100.0 * total_close / total_total if total_total else 0.0
    st.metric(f"{predicate} closure", f"{total_close} of {total_total}", f"{pct:.1f}%")

    # Closure heatmap.
    st.subheader(f"closure heatmap: {row_axis} (row) x {col_axis} (column)")
    rows = sorted({c.coords[row_axis] for c in filtered if row_axis in c.coords})
    cols = sorted({c.coords[col_axis] for c in filtered if col_axis in c.coords})

    grid = [[None] * len(cols) for _ in rows]
    for c in filtered:
        if row_axis not in c.coords or col_axis not in c.coords:
            continue
        r_idx = rows.index(c.coords[row_axis])
        c_idx = cols.index(c.coords[col_axis])
        nc, nt = floor.get(c.cell_id, (0, 0))
        prev = grid[r_idx][c_idx] or (0, 0)
        grid[r_idx][c_idx] = (prev[0] + nc, prev[1] + nt)

    z_close = [
        [(entry[0] if entry else 0) for entry in row]
        for row in grid
    ]
    text_labels = [
        [f"{entry[0]}/{entry[1]}" if entry else "-" for entry in row]
        for row in grid
    ]
    fig = go.Figure(
        data=go.Heatmap(
            z=z_close,
            x=[str(c) for c in cols],
            y=[str(r) for r in rows],
            text=text_labels,
            texttemplate="%{text}",
            colorbar=dict(title="n_close"),
            colorscale="Viridis",
        )
    )
    fig.update_layout(xaxis_title=col_axis, yaxis_title=row_axis, height=500)
    st.plotly_chart(fig, use_container_width=True)

    # Marginal closure on every axis (uses unfiltered cells so the marginal is global).
    st.subheader("marginal closure on each axis (unfiltered global view)")
    cols_layout = st.columns(len(axis_names))
    for col_widget, axis in zip(cols_layout, axis_names):
        marg = marginal_closure(cells, axis, predicate)
        x = sorted(marg.keys())
        y_close = [marg[v][0] for v in x]
        y_total = [marg[v][1] for v in x]
        with col_widget:
            st.caption(axis)
            fig2 = go.Figure()
            fig2.add_trace(go.Bar(x=[str(v) for v in x], y=y_total, name="total", marker_color="lightgray"))
            fig2.add_trace(go.Bar(x=[str(v) for v in x], y=y_close, name="close", marker_color="green"))
            fig2.update_layout(
                barmode="overlay",
                height=240,
                margin=dict(t=10, b=10, l=10, r=10),
                showlegend=False,
            )
            st.plotly_chart(fig2, use_container_width=True)

    # Back-propagation: which axis values admit any closing cell.
    st.subheader("back-propagation: axis values admitting any closing cell")
    admitting = back_propagate(cells, predicate)
    for axis in sorted(admitting.keys()):
        vals = sorted(admitting[axis])
        st.write(f"- **{axis}**: {{{', '.join(str(v) for v in vals)}}}")

    # Top architectures.
    st.subheader("top architectures by cell-feasibility count")
    counts = architecture_cell_counts(filtered)
    top = sorted(counts.items(), key=lambda kv: -kv[1])[:15]
    rows_tbl = []
    for path_label, count in top:
        chain = " -> ".join(p.split(".")[1] for p in path_label.split(" -> "))
        rows_tbl.append({"cells_feasible": count, "architecture": chain})
    st.dataframe(rows_tbl, use_container_width=True)

    # Best delivery per cell — show top 10.
    st.subheader("best delivery per cell (top 10 by payload at depot)")
    best = best_delivery_per_cell(filtered)
    enriched = []
    for cid, r in best.items():
        if r is None:
            continue
        cell = next(c for c in filtered if c.cell_id == cid)
        yrs = r.leaf_state.time_elapsed_s / (365.25 * 86_400)
        enriched.append({
            "cell_id": cid,
            "delivered_t": round(r.leaf_state.payload_kg / 1000, 1),
            "years": round(yrs, 2),
            **{ax: cell.coords[ax] for ax in axis_names if ax in cell.coords},
        })
    enriched.sort(key=lambda r: -r["delivered_t"])
    st.dataframe(enriched[:10], use_container_width=True)

    # Phase tree — reachable edges only, probed with user-chosen state.
    st.subheader("phase tree — reachable option-to-option edges")
    st.caption(
        "Only shows transitions where the downstream option's precondition "
        "actually passes after the upstream option's executor runs. "
        "Edges absent here are gated by some precondition. "
        "Probe state below picks the starting point — changing it can reveal "
        "or hide options (e.g., probing with a 50-tonne vehicle exposes "
        "falcon_heavy_expended; 100-tonne vehicle does not)."
    )

    probe_cols = st.columns(5)
    with probe_cols[0]:
        probe_mass = st.selectbox(
            "probe vehicle_mass_kg",
            _axis_values_in_cells(cells, "vehicle_mass_kg") or [50_000.0],
            index=0,
        )
    with probe_cols[1]:
        # Map the float effective-avg-power-kwe values to their named
        # tech-path class labels (K1, K10, K30, K1+S20, K10+S20, K30+S50)
        # for human-readable display. See POWER_CLASS_REGISTRY in
        # saturn_water_canonical_sweep.py for the full mapping.
        from mission_graph.missions.sweeps.saturn_water_canonical_sweep import (
            POWER_CLASS_REGISTRY,
        )
        _power_vals = _axis_values_in_cells(cells, "power_kwe") or [10.0]
        def _power_label(v: float) -> str:
            entry = POWER_CLASS_REGISTRY.get(v)
            if entry is None:
                return f"{v:g} kWe (unrecognized)"
            return f"{entry['label']} ({v:g} kWe avg = R:{entry['reactor_kwe']:g} + S:{entry['solar_leo_kwe']:g})"
        probe_power = st.selectbox(
            "probe power class (effective avg kWe)",
            _power_vals,
            index=min(2, len(_power_vals) - 1),
            format_func=_power_label,
        )
    with probe_cols[2]:
        probe_chunk = st.selectbox(
            "probe chunk_mass_kg",
            _axis_values_in_cells(cells, "chunk_mass_kg") or [200_000.0],
            index=len(_axis_values_in_cells(cells, "chunk_mass_kg")) - 1,
        )
    with probe_cols[3]:
        probe_thrust = st.selectbox(
            "probe electric_thrust_n",
            _axis_values_in_cells(cells, "electric_thrust_n") or [5.0],
            index=2,
        )
    with probe_cols[4]:
        probe_direction = st.selectbox("direction", ["LR", "TD"], index=0)

    probe_state = VehicleState(
        mass_kg=float(probe_mass),
        propellant_kg=0.80 * float(probe_mass),
        payload_kg=0.0,
        location="pre_launch",
        v_inf_km_s=0.0,
        time_elapsed_s=0.0,
        epoch_jd=None,
        power_available_kwe=float(probe_power),
    )
    probe_params = {
        "chemical_isp_s": 340.0,
        "electric_isp_s": 3000.0,
        "electric_thrust_n": float(probe_thrust),
        "water_met_isp_s": 800.0,
        "chunk_mass_kg": float(probe_chunk),
        "multi_falcon_launch_count": 6,
        "launch_epoch_jd": 0.0,
        "existing_leo_depot": True,
    }

    reachable_src = emit_reachable_phase_tree_mermaid(
        saturn_water_v0, probe_state, probe_params, direction=probe_direction
    )
    _render_mermaid(reachable_src, height=1500)

    with st.expander("show Mermaid source (reachable)"):
        st.code(reachable_src, language="text")

    with st.expander("show structural tree (every phase x every option, no reachability filter)"):
        structural_src = emit_phase_tree_mermaid(saturn_water_v0, direction=probe_direction)
        _render_mermaid(structural_src, height=1500)
        st.caption(
            "Structural view ignores preconditions. Useful as a catalog of "
            "available options; misleading if read as a connectivity diagram."
        )


if __name__ == "__main__":
    main()
