"""Figure for R-flight-layout-tangential-authority."""
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from run import (distributed_layout, redundant_layout, aft_clustered_layout,
                 inplane_authority, TAU_TH)

dist = distributed_layout()
red = redundant_layout()
aft = aft_clustered_layout()

# worst single-fault min in-plane couple for distributed
def worst_single_fault(layout):
    worst = inplane_authority(layout)["min_inplane_couple_torque"]
    for t in list(layout):
        red_l = {k: v for k, v in layout.items() if k != t}
        a = inplane_authority(red_l)
        val = a["min_inplane_couple_torque"] if a["all_four_feasible"] else 0.0
        worst = min(worst, val)
    return worst

cases = {
    "Distributed 12\n(nominal)": inplane_authority(dist)["min_inplane_couple_torque"],
    "Distributed 12\n(worst single fault)": worst_single_fault(dist),
    "Redundant 16\n(worst single fault)": worst_single_fault(red),
    "Aft-clustered 12\n(nominal)": inplane_authority(aft)["min_inplane_couple_torque"],
}

fig, ax = plt.subplots(figsize=(9, 5.2))
labels = list(cases)
vals = [cases[k] for k in labels]
colors = ["#2471a3", "#c0392b", "#1e8449", "#7d3c98"]
bars = ax.bar(labels, vals, color=colors, width=0.6)
for b, v in zip(bars, vals):
    ax.text(b.get_x() + b.get_width() / 2, v + 0.4,
            "0 (no plume-safe\nin-plane couple)" if v == 0 else f"{v:.0f} N·m",
            ha="center", va="bottom", fontsize=9)
ax.axhline(0, color="k", lw=0.8)
ax.set_ylabel("min plume-safe in-plane couple torque (N·m)")
ax.set_ylim(0, 24)
ax.set_title("Flight-layout tangential authority for berth momentum dump\n"
             "(need > 0 about all of ±x,±y; nominal 20 N·m dumps 5000 N·m·s in 250 s)",
             fontsize=10)
ax.annotate("H-A4 FALSIFIED:\nbare 12 loses a couple\nsense on any 1 failure",
            xy=(1, 0.5), xytext=(1.0, 12), fontsize=8, color="#c0392b", ha="center",
            arrowprops=dict(arrowstyle="->", color="#c0392b"))
ax.annotate("H-A5: aft-clustered\nhas NO plume-safe\nin-plane couple",
            xy=(3, 0.5), xytext=(3.0, 10), fontsize=8, color="#7d3c98", ha="center",
            arrowprops=dict(arrowstyle="->", color="#7d3c98"))
fig.tight_layout()
fig.savefig(HERE / "results" / "layout_authority.png", dpi=130, bbox_inches="tight")
print("wrote", HERE / "results" / "layout_authority.png")
