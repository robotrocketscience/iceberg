"""Figure for R-lowthrust-spiral-departure."""
import json
import math
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from run import reactor_kwe, V_CIRC, VINF, DV_IMPULSIVE, VE_MET

r = json.load(open(HERE / "results" / "spiral_departure.json"))
dv_spiral = r["HC2"]["numerical_spiral_dv_to_vinf"]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.2))

# Panel 1: reactor floor vs departure Δv
dvs = np.linspace(6000, 26000, 200)
kwe = [reactor_kwe(d) for d in dvs]
ax1.plot(dvs / 1000, kwe, color="#34495e", lw=2)
ax1.axhspan(500, 2200, color="#c0392b", alpha=0.08)
ax1.text(7, 1900, "megawatt band\n(retired as fantasy)", color="#c0392b", fontsize=8)
ax1.scatter([9.0], [reactor_kwe(9000)], color="#2471a3", zorder=5)
ax1.annotate("R179 impulsive\n9.0 km/s → 175 kWe", (9.0, 175), xytext=(10.5, 350),
             fontsize=8, color="#2471a3", arrowprops=dict(arrowstyle="->", color="#2471a3"))
ax1.scatter([dv_spiral / 1000], [reactor_kwe(dv_spiral)], color="#c0392b", zorder=5)
ax1.annotate(f"honest electric spiral\n{dv_spiral/1000:.1f} km/s → {reactor_kwe(dv_spiral):.0f} kWe",
             (dv_spiral / 1000, reactor_kwe(dv_spiral)), xytext=(13, 1250),
             fontsize=8, color="#c0392b", arrowprops=dict(arrowstyle="->", color="#c0392b"))
ax1.axvline(V_CIRC / 1000, ls=":", color="gray", lw=1)
ax1.text(V_CIRC / 1000 + 0.2, 60, "v_circ 18.8", color="gray", fontsize=7, rotation=90)
ax1.set_xlabel("departure Δv (km/s)")
ax1.set_ylabel("departure reactor floor (kWe)")
ax1.set_title("Reactor floor vs departure Δv (R179's own formula)")
ax1.set_ylim(0, 2200)
ax1.grid(alpha=0.3)

# Panel 2: impulsive vs low-thrust-spiral schematic Δv breakdown
labels = ["R179\nimpulsive\n(Oberth)", "honest electric\nlow-thrust spiral"]
vals = [9.0, dv_spiral / 1000]
colors = ["#2471a3", "#c0392b"]
bars = ax2.bar(labels, vals, color=colors, width=0.55)
for b, v in zip(bars, vals):
    ax2.text(b.get_x() + b.get_width() / 2, v + 0.4, f"{v:.1f} km/s", ha="center", fontsize=10)
ax2.axhline(8.5, ls=":", color="#2471a3", lw=1)
ax2.text(1.4, 8.7, "impulsive floor 8.5", color="#2471a3", fontsize=7, ha="right")
ax2.axhline(V_CIRC / 1000, ls=":", color="#c0392b", lw=1)
ax2.text(1.4, V_CIRC / 1000 + 0.2, "v_circ 18.8 (escape term)", color="#c0392b", fontsize=7, ha="right")
ax2.annotate("2.44× — the Oberth\nbenefit a low-thrust\nengine cannot use", (1, 21.9),
             xytext=(0.3, 16), fontsize=8, color="#c0392b",
             arrowprops=dict(arrowstyle="->", color="#c0392b"))
ax2.set_ylabel("departure Δv (km/s)")
ax2.set_title("Same departure, two propulsion modes\n(2294-rev spiral at mission thrust-to-weight)")
ax2.set_ylim(0, 26)
ax2.grid(alpha=0.3, axis="y")

fig.suptitle("R-lowthrust-spiral-departure — electric low-thrust departure is megawatt-class, "
             "not 175 kWe", fontsize=11, y=1.00)
fig.tight_layout()
fig.savefig(HERE / "results" / "spiral_departure.png", dpi=130, bbox_inches="tight")
print("wrote", HERE / "results" / "spiral_departure.png")
