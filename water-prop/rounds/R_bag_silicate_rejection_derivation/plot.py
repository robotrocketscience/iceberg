"""Figure for R-bag-silicate-rejection-derivation."""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
r = json.load(open(HERE / "results" / "bag_rejection.json"))
temps = [200, 220, 250, 273]
d_max_nm = [r["vapor"][str(T)]["d_max_nm"] for T in temps]
fpass_1um = [r["f_pass_gas"][str(T)]["rmax_1um"] for T in temps]
fpass_100um = [r["f_pass_gas"][str(T)]["rmax_100um"] for T in temps]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.5, 5.4))

# Panel 1: carryover vs temperature (left y) + cutoff d_max (right y)
x = np.arange(len(temps))
ax1.plot(x, np.maximum(fpass_1um, 1e-9), "o-", color="#c0392b", lw=2, label="carryover f_pass (PSD r_max=1 µm)")
ax1.plot(x, np.maximum(fpass_100um, 1e-9), "s-", color="#e67e22", lw=2, label="carryover f_pass (PSD r_max=100 µm)")
ax1.axhline(1e-4, color="#2471a3", ls="--", lw=1.5)
ax1.text(0.03, 1.3e-4, "R11/R_silicate ASSUMED 1e-4", color="#2471a3", fontsize=8)
ax1.axhspan(1e-9, 3e-4, color="#1e8449", alpha=0.08)
ax1.text(2.1, 3e-8, "grid survives", color="#1e8449", fontsize=8)
ax1.axhspan(3e-3, 1.0, color="#c0392b", alpha=0.06)
ax1.text(0.03, 0.2, "grid LIFE-LIMITED", color="#c0392b", fontsize=8)
ax1.set_yscale("log"); ax1.set_ylim(1e-8, 2)
ax1.set_xticks(x); ax1.set_xticklabels([f"{T} K" for T in temps])
ax1.set_xlabel("bag sublimation temperature")
ax1.set_ylabel("derived carryover f_pass (silicate reaching grid)")
ax1.set_title("The rejection factor is DERIVED and temperature-gated —\nnot an intrinsic 1e-4")
ax1.legend(fontsize=7.6, loc="lower right")
ax1.grid(alpha=0.3, which="both", axis="y")
ax1b = ax1.twinx()
ax1b.plot(x, d_max_nm, "^:", color="#7d3c98", lw=1.6, label="entrainment cutoff d_max")
ax1b.set_yscale("log"); ax1b.set_ylabel("free-molecular cutoff d_max (nm)", color="#7d3c98")
ax1b.tick_params(axis="y", labelcolor="#7d3c98")
ax1b.legend(fontsize=7.6, loc="upper left")

# Panel 2: grid consumed by corner
corners = ["cold200_smallnano_opt", "r11_assumed_central", "cold200_hsu_pessim",
           "warm273_hsu_pessim", "warm273_powerlaw_1um"]
labels = ["cold bag +\nsmall nano-tail", "R11 assumed\n(1e-4)", "cold bag +\nHsu nano-tail\n(electrostatic)",
          "warm bag +\nHsu nano-tail", "warm bag +\npower-law"]
consumed = [r["corners"][c]["grid_consumed"] * 100 for c in corners]
colors = ["#1e8449" if r["corners"][c]["grid_consumed"] <= 1 else "#c0392b" for c in corners]
xb = np.arange(len(corners))
ax2.bar(xb, np.maximum(consumed, 0.05), color=colors, alpha=0.85)
ax2.axhline(100, color="#000", ls="--", lw=1.2)
ax2.text(0.0, 130, "grid fails within the burn (100%)", fontsize=8)
for xi, c in zip(xb, consumed):
    ax2.text(xi, max(c, 0.05) * 1.3, f"{c:.2g}%", ha="center", fontsize=7.5)
ax2.set_yscale("log"); ax2.set_ylim(0.05, 5e4)
ax2.set_xticks(xb); ax2.set_xticklabels(labels, fontsize=7.2)
ax2.set_ylabel("RF-ion grid life consumed over the burn (%)")
ax2.set_title("R11's 'silicate not a grid-life-limiter' holds ONLY at\ncold bag + small nano-tail — everything else fails")
ax2.grid(alpha=0.3, which="both", axis="y")

fig.suptitle("R-bag-silicate-rejection-derivation — the bet-#2 conjunction's biggest driver is a DERIVED quantity "
             "gated on one unmeasured input: the sub-100-nm silicate inclusion PSD of ring ice",
             fontsize=9.3, y=1.005)
fig.tight_layout()
fig.savefig(HERE / "results" / "bag_rejection.png", dpi=130, bbox_inches="tight")
print("wrote", HERE / "results" / "bag_rejection.png")
