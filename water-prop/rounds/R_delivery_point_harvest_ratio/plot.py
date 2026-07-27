"""Figure for R-delivery-point-harvest-ratio."""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
r = json.load(open(HERE / "results" / "delivery_point.json"))

order = ["Saturn ring/orbit\ndepot", "heliocentric-\nat-Saturn", "Earth cislunar /\nhigh-ellipse", "LEO"]
keys = ["Saturn ring/orbit depot", "heliocentric-at-Saturn", "Earth cislunar/high-ell", "LEO"]
r24 = [r["grid"]["sp_2.4"][k]["harvest_ratio"] for k in keys]
r40 = [r["grid"]["sp_40.0"][k]["harvest_ratio"] for k in keys]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.2))

# Panel 1: harvest ratio by delivery point
x = np.arange(len(order))
ax1.plot(x, r24, "o-", color="#c0392b", lw=2, label="flown 2.4 W/kg")
ax1.plot(x, r40, "s-", color="#2471a3", lw=2, label="aspirational 40 W/kg")
ax1.axhspan(1, 10, color="#1e8449", alpha=0.12)
ax1.text(0.05, 6, "viable band (<10:1)", color="#1e8449", fontsize=8)
for xi, v in zip(x, r24):
    ax1.text(xi, v * 1.12, f"{v:.0f}:1", ha="center", fontsize=8, color="#c0392b")
ax1.annotate("only the Saturn-orbit depot\nescapes the well-climb penalty\n(4.2:1 flown, ~1:1 reused)",
             (0, 4.2), xytext=(0.6, 40), fontsize=8, color="#1e8449",
             arrowprops=dict(arrowstyle="->", color="#1e8449"))
ax1.annotate("Earth-vicinity delivery is ~67–73:1\nregardless of orbit (LEO→cislunar = 1.05×)",
             (3, 72.8), xytext=(1.2, 90), fontsize=8, color="#c0392b",
             arrowprops=dict(arrowstyle="->", color="#c0392b"))
ax1.set_yscale("log")
ax1.set_xticks(x); ax1.set_xticklabels(order, fontsize=8)
ax1.set_ylabel("harvest ratio (t water harvested / t delivered)")
ax1.set_title("The depot prize is 'don't leave Saturn orbit'\n— not 'deliver closer to Earth'")
ax1.legend(fontsize=8, loc="lower left")
ax1.grid(alpha=0.3, which="both", axis="y")

# Panel 2: penalty decomposition (departure vs capture) at flown sp
dep = [r["grid"]["sp_2.4"][k]["dep_prop_t"] for k in keys]
cap = [r["grid"]["sp_2.4"][k]["cap_prop_t"] for k in keys]
ax2.bar(x, dep, 0.55, color="#c0392b", label="Saturn-departure propellant")
ax2.bar(x, cap, 0.55, bottom=dep, color="#e67e22", label="Earth-capture propellant")
for xi, (d, c) in enumerate(zip(dep, cap)):
    ax2.text(xi, d + c + 40, f"{d+c:.0f} t", ha="center", fontsize=8)
ax2.set_xticks(x); ax2.set_xticklabels(order, fontsize=8)
ax2.set_ylabel("harvested water (t) for 30 t delivered")
ax2.set_title("The Saturn-departure leg is ~90% of the penalty\n(it carries the 146 t reactor out of the well)")
ax2.legend(fontsize=8, loc="upper left")
ax2.grid(alpha=0.3, axis="y")

fig.suptitle("R-delivery-point-harvest-ratio — the deep-well penalty is Saturn-escape, not Earth-return; "
             "only a Saturn-orbit depot escapes it", fontsize=10, y=1.00)
fig.tight_layout()
fig.savefig(HERE / "results" / "delivery_point.png", dpi=130, bbox_inches="tight")
print("wrote", HERE / "results" / "delivery_point.png")
