"""Figure for R-cryo-hydrogen-storage-saturn."""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
r = json.load(open(HERE / "results" / "cryo_h2.json"))

SIGMA = 5.67e-8
A = r["tank"]["area_m2"]
L_V, M_H2, YEAR = 446e3, 77000.0, 3.156e7

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.2))

# Panel 1: reactor heat vs effective view factor (the dominant source)
vf = np.logspace(-7, -1, 200)
w = vf * SIGMA * A * 700.0 ** 4
ax1.loglog(vf, w, color="#c0392b", lw=2, label="reactor (700 K radiators)")
ax1.axhline(1.9, ls="--", color="#2471a3", lw=1.2, label="MLI @ Saturn 90 K (1.9 W)")
ax1.axhspan(0.1, 10, color="#1e8449", alpha=0.12)
ax1.text(2e-7, 3, "benign (<10 W)\n<2%/yr boiloff", color="#1e8449", fontsize=8)
for vfe, tag in ((1e-3, "1-layer\nshadow"), (1e-5, "JWST-class"), (1e-6, "extreme /\ndeep shadow")):
    wv = vfe * SIGMA * A * 700.0 ** 4
    ax1.scatter([vfe], [wv], color="#c0392b", zorder=5)
    ax1.annotate(tag, (vfe, wv), fontsize=7, ha="center",
                 xytext=(vfe, wv * 4), color="#c0392b")
ax1.axvline(1.4e-6, ls=":", color="k", lw=1)
ax1.text(1.4e-6, 2e5, "required\nVF_eff 1.4e-6", fontsize=7, ha="center")
ax1.set_xlabel("effective view factor (geometry × shield attenuation)")
ax1.set_ylabel("heat into LH₂ tank (W)")
ax1.set_title("Reactor dominates: a 1-layer shield leaves 7 kW\n(H-G3 falsified: predicted ≤10 W)")
ax1.legend(fontsize=8, loc="lower right")
ax1.grid(alpha=0.3, which="both")

# Panel 2: total heat + cryocooler by shield class
labels = ["1-layer\nshadow\n(VF 1e-3)", "JWST-class\n(VF 1e-5)", "extreme\n(VF 1e-6)"]
sc = r["HG4"]["scenarios"]
totals = [sc["1-layer shadow VF1e-3"]["total_W"], sc["JWST-class VF1e-5"]["total_W"],
          sc["extreme VF1e-6"]["total_W"]]
cryos = [sc["1-layer shadow VF1e-3"]["cryocooler_kW"], sc["JWST-class VF1e-5"]["cryocooler_kW"],
         sc["extreme VF1e-6"]["cryocooler_kW"]]
x = np.arange(3)
ax2b = ax2.twinx()
ax2.bar(x - 0.2, totals, 0.4, color="#c0392b", label="total heat (W)")
ax2b.bar(x + 0.2, cryos, 0.4, color="#7d3c98", label="zero-boiloff cryocooler (kW)")
ax2.set_yscale("log"); ax2b.set_yscale("log")
for xi, v in zip(x - 0.2, totals):
    ax2.text(xi, v * 1.3, f"{v:.0f} W", ha="center", fontsize=8, color="#c0392b")
for xi, v in zip(x + 0.2, cryos):
    ax2b.text(xi, v * 1.4, f"{v} kW", ha="center", fontsize=8, color="#7d3c98")
ax2.set_xticks(x); ax2.set_xticklabels(labels, fontsize=8)
ax2.set_ylabel("total heat into tank (W)", color="#c0392b")
ax2b.set_ylabel("cryocooler input (kW)", color="#7d3c98")
ax2.set_ylim(5, 2e4); ax2b.set_ylim(0.1, 300)
ax2.set_title("Only a multilayer shadow shield keeps the\ncryocooler small (else 122 kW erodes Round F)")

fig.suptitle("R-cryo-hydrogen-storage-saturn — reactor-dominated, not environment-dominated; "
             "needs the tank in the reactor's thermal shadow", fontsize=10.5, y=1.00)
fig.tight_layout()
fig.savefig(HERE / "results" / "cryo_h2.png", dpi=130, bbox_inches="tight")
print("wrote", HERE / "results" / "cryo_h2.png")
