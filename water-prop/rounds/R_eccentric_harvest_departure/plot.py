"""Figure for R-eccentric-harvest-departure."""
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from run import v_peri, V_CIRC, R_RING, R_TITAN

r = json.load(open(HERE / "results" / "eccentric_harvest.json"))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.2))

# Panel 1: ring relative velocity vs apoapsis (H-D1)
mults = np.linspace(1.0, 11.4, 200)
vrel = [(v_peri(m * R_RING) - V_CIRC) / 1000 for m in mults]
ax1.plot(mults, vrel, color="#c0392b", lw=2)
ax1.axhline(0.001, ls="--", color="#1e8449", lw=1.5, label="capture threshold ~1 m/s (locked finding 1)")
ax1.fill_between(mults, 0, 0.001, color="#1e8449", alpha=0.15)
ax1.scatter([1.3], [(v_peri(1.3 * R_RING) - V_CIRC) / 1000], color="#c0392b", zorder=5)
ax1.annotate("1.19 km/s at just 1.3× r_p\n= 1000× the capture threshold",
             (1.3, 1.19), xytext=(3, 3.5), fontsize=8, color="#c0392b",
             arrowprops=dict(arrowstyle="->", color="#c0392b"))
ax1.set_xlabel("harvest-orbit apoapsis (× r_p)")
ax1.set_ylabel("relative velocity at the ring (km/s)")
ax1.set_title("H-D1: harvest-from-eccentric is hypervelocity\n(gentle harvest needs a near-circular orbit)")
ax1.set_yscale("symlog", linthresh=0.001)
ax1.legend(fontsize=8, loc="lower right")
ax1.grid(alpha=0.3)

# Panel 2: departure peak power — the duty-vs-Oberth tension
strategies = ["impulsive\n(chemical only)\n8.5 km/s", "continuous spiral\n(Round C)\n21.9 km/s, duty 1",
              "periapsis burn\n8.5 km/s, duty ~1%\n(2-3 yr)"]
vals = [175, 1248, 1961]
colors = ["#7f8c8d", "#2471a3", "#c0392b"]
bars = ax2.bar(strategies, vals, color=colors, width=0.6)
for b, v in zip(bars, vals):
    ax2.text(b.get_x() + b.get_width() / 2, v + 40, f"{v} kWe", ha="center", fontsize=10)
ax2.axhspan(500, 2100, color="#c0392b", alpha=0.06)
ax2.text(0.0, 1950, "megawatt band\n(retired as fantasy)", color="#c0392b", fontsize=8)
ax2.annotate("H-D3 FALSIFIED:\nperiapsis-burn does NOT\nrescue below megawatt\n(duty collapse offsets Oberth)",
             (2, 1961), xytext=(0.7, 1450), fontsize=8, color="#c0392b",
             arrowprops=dict(arrowstyle="->", color="#c0392b"))
ax2.set_ylabel("departure reactor peak power (kWe)")
ax2.set_title("Departure power by thrust strategy\n(only a high-thrust/chemical stage reaches 175 kWe)")
ax2.set_ylim(0, 2150)
ax2.grid(alpha=0.3, axis="y")

fig.suptitle("R-eccentric-harvest-departure — option 4 closes: no harvest-compatible electric "
             "departure below ~1250 kWe", fontsize=11, y=1.00)
fig.tight_layout()
fig.savefig(HERE / "results" / "eccentric_harvest.png", dpi=130, bbox_inches="tight")
print("wrote", HERE / "results" / "eccentric_harvest.png")
