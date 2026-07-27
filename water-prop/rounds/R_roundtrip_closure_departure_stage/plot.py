"""Figure for R-roundtrip-closure-departure-stage."""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
r = json.load(open(HERE / "results" / "roundtrip.json"))
g = r["grid"]


def row(sp, chem):
    return next(x for x in g if x["D_t"] == 30 and x["sp"] == sp and x["chem"] == chem)


sps = [2.4, 10.0, 40.0]
h2o2 = [row(sp, True)["harvest_ratio"] for sp in sps]
elec = [row(sp, False)["harvest_ratio"] for sp in sps]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.2))

# Panel 1: harvest ratio vs specific power, both architectures
x = np.arange(len(sps))
ax1.bar(x - 0.2, elec, 0.4, color="#c0392b", label="all-electric departure")
ax1.bar(x + 0.2, h2o2, 0.4, color="#2471a3", label="H₂/O₂ departure stage")
for xi, v in zip(x - 0.2, elec):
    ax1.text(xi, v * 1.05, f"{v:.0f}:1", ha="center", fontsize=8, color="#c0392b")
for xi, v in zip(x + 0.2, h2o2):
    ax1.text(xi, v * 1.08, f"{v:.0f}:1", ha="center", fontsize=8, color="#2471a3")
ax1.axhspan(1, 10, color="#1e8449", alpha=0.12)
ax1.text(0.1, 6, "viable band (<10:1)\n— never reached", color="#1e8449", fontsize=8)
ax1.set_yscale("log")
ax1.set_xticks(x)
ax1.set_xticklabels([f"{sp}\nW/kg" for sp in sps])
ax1.set_xlabel("reactor specific power  (flown → aspirational)")
ax1.set_ylabel("harvest ratio  (t water harvested / t delivered)")
ax1.set_title("H₂/O₂ helps 7× — but never reaches viable (<10:1)\nchunk-return is intrinsically ~20–73:1")
ax1.legend(fontsize=8, loc="upper right")
ax1.grid(alpha=0.3, which="both", axis="y")

# Panel 2: where the mass goes (H2/O2, 2.4 vs 40 W/kg), D=30
cats = ["reactor", "departure\npropellant", "Earth-capture\npropellant"]
c24 = row(2.4, True); c40 = row(40.0, True)
v24 = [c24["reactor_t"], c24["dep_prop_t"], c24["cap_prop_t"]]
v40 = [c40["reactor_t"], c40["dep_prop_t"], c40["cap_prop_t"]]
x2 = np.arange(len(cats))
ax2.bar(x2 - 0.2, v24, 0.4, color="#7d3c98", label="flown 2.4 W/kg")
ax2.bar(x2 + 0.2, v40, 0.4, color="#e67e22", label="aspirational 40 W/kg")
for xi, v in zip(x2 - 0.2, v24):
    ax2.text(xi, v + 30, f"{v:.0f} t", ha="center", fontsize=8, color="#7d3c98")
for xi, v in zip(x2 + 0.2, v40):
    ax2.text(xi, v + 30, f"{v:.0f} t", ha="center", fontsize=8, color="#e67e22")
ax2.axhline(30, ls=":", color="k", lw=1.2)
ax2.text(2.3, 55, "delivered chunk 30 t", fontsize=7, ha="right")
ax2.set_xticks(x2); ax2.set_xticklabels(cats, fontsize=8)
ax2.set_ylabel("mass (t)  for 30 t delivered")
ax2.set_title("Where the harvest goes (H₂/O₂)\nEarth-capture Δv is the un-removable floor")
ax2.legend(fontsize=8)
ax2.grid(alpha=0.3, axis="y")

fig.suptitle("R-roundtrip-closure-departure-stage — the departure lever helps 7× but the deep-well "
             "two-end Δv floor is ~20–25:1", fontsize=10.5, y=1.00)
fig.tight_layout()
fig.savefig(HERE / "results" / "roundtrip.png", dpi=130, bbox_inches="tight")
print("wrote", HERE / "results" / "roundtrip.png")
