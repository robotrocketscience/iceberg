#!/usr/bin/env python3
"""Static close/not-close matrix from the audit capture-efficiency sweep.

Reads runs/audit_capture_efficiency/<ts>/cells.jsonl, renders a 2x2 faceted
matrix (vehicle mass x chunk mass; inner axes capture-efficiency multiplier x
specific impulse), cell color = best delivered mass on a diverging scale whose
neutral midpoint is pinned at the 25 t commercial floor. Closing cells carry an
ink ring. Writes plots/17_closure_matrix.png at the repo root.
"""
import json
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
from matplotlib.patches import Rectangle

REPO = Path(__file__).resolve().parents[2]
RUN = (Path.home() / "projects/iceberg/water-prop/sims/mission_graph/runs/"
       "audit_capture_efficiency/20260522T175555Z/cells.jsonl")
OUT = REPO / "plots" / "17_closure_matrix.png"

FLOOR_T = 25.0
SURFACE = "#fcfcfb"
INK = "#26251f"
MUTED = "#6f6c64"
# diverging: red arm (below floor) -> neutral -> blue arm (above floor)
CMAP = LinearSegmentedColormap.from_list(
    "closure", ["#b53332", "#e34948", "#f2b6b0", "#f0efec", "#9ec5f4", "#3987e5", "#184f95"]
)

cells = {}
vmax = FLOOR_T
for line in open(RUN):
    c = json.loads(line)
    k = c["coords"]
    best = 0.0
    for res in c.get("results", []):
        if res.get("infeasible_at") is None:
            best = max(best, float((res.get("leaf_state") or {}).get("payload_kg", 0.0)))
    key = (k["vehicle_mass_kg"], k["chunk_mass_kg"],
           k["capture_efficiency_multiplier"], k["water_met_isp_s"])
    cells[key] = best / 1000.0
    vmax = max(vmax, best / 1000.0)

vehicles = sorted({k[0] for k in cells})
chunks = sorted({k[1] for k in cells})
capts = sorted({k[2] for k in cells}, reverse=True)   # rows, best at top
isps = sorted({k[3] for k in cells})

norm = TwoSlopeNorm(vmin=0.0, vcenter=FLOOR_T, vmax=math.ceil(vmax))

fig, axes = plt.subplots(len(vehicles), len(chunks), figsize=(10.5, 9.2),
                         facecolor=SURFACE)
fig.suptitle("Does the mission close?  Best delivered water per cell, audit sweep "
             "(sweep 20260522T175555Z)", color=INK, fontsize=13, y=0.98)

for vi, veh in enumerate(vehicles):
    for ci, ch in enumerate(chunks):
        ax = axes[vi][ci]
        ax.set_facecolor(SURFACE)
        grid = np.array([[cells[(veh, ch, ca, isp)] for isp in isps] for ca in capts])
        ax.imshow(grid, cmap=CMAP, norm=norm, aspect="auto")
        for r in range(len(capts)):
            for col in range(len(isps)):
                v = grid[r][col]
                closes = v >= FLOOR_T
                ax.text(col, r, f"{v:.1f} t" if v > 0 else "—",
                        ha="center", va="center", fontsize=9,
                        color=INK if 8 < v < 34 else SURFACE,
                        fontweight="bold" if closes else "normal")
                if closes:
                    ax.add_patch(Rectangle((col - 0.47, r - 0.47), 0.94, 0.94,
                                           fill=False, edgecolor=INK, lw=2.2))
        ax.set_xticks(range(len(isps)), [f"{int(i)} s" for i in isps],
                      fontsize=8, color=MUTED)
        ax.set_yticks(range(len(capts)), [f"×{ca:g}" for ca in capts],
                      fontsize=8, color=MUTED)
        if vi == len(vehicles) - 1:
            ax.set_xlabel("water-thruster specific impulse", fontsize=9, color=INK)
        if ci == 0:
            ax.set_ylabel("capture-efficiency multiplier\n(× the 0.85 desk anchor)",
                          fontsize=9, color=INK)
        ax.set_title(f"vehicle {int(veh/1000)} t  ·  chunk {int(ch/1000)} t",
                     fontsize=10, color=INK)
        for s in ax.spines.values():
            s.set_visible(False)

sm = plt.cm.ScalarMappable(cmap=CMAP, norm=norm)
cbar = fig.colorbar(sm, ax=axes, shrink=0.75, pad=0.02)
cbar.set_label("best delivered water [t] — neutral pinned at the 25 t commercial floor",
               fontsize=9, color=INK)
cbar.ax.axhline(FLOOR_T, color=INK, lw=1.5)
cbar.ax.tick_params(labelsize=8, colors=MUTED)

fig.text(0.5, 0.015,
         "Ink-ringed cells close at the 25 t floor (5 of 48). Every closing cell needs the capture "
         "multiplier at ×0.75 or better and 800 s or better — the two flight-unproven bets.",
         ha="center", fontsize=9, color=MUTED)

fig.savefig(OUT, dpi=160, bbox_inches="tight", facecolor=SURFACE)
print("wrote", OUT)
n_close = sum(1 for v in cells.values() if v >= FLOOR_T)
print(f"{n_close} of {len(cells)} cells close at {FLOOR_T:g} t")
