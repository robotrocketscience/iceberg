"""Figure for R-chunk-capture-closing-velocity-window."""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
r = json.load(open(HERE / "results" / "closing_velocity_window.json"))
masses = [1, 10, 50, 200]
g = r["grid"]

floor_p50 = [g[f"{m}t"]["floor_mms"]["p50"] / 1e3 for m in masses]
floor_p95 = [g[f"{m}t"]["floor_mms"]["p95"] / 1e3 for m in masses]
floor_fast = [g[f"{m}t"]["floor_mms"]["fast"] / 1e3 for m in masses]
ceil_strong = [g[f"{m}t"]["ceiling_ms"]["strong_zylon_wholebag"] for m in masses]
ceil_pessim = [g[f"{m}t"]["ceiling_ms"]["pessim_patch_light"] for m in masses]
frag = r["fragmentation_ms"]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.5, 5.4))
x = np.arange(len(masses))

# Panel 1: the window (log y) -- floor band vs ceiling band
ax1.fill_between(x, floor_p50, ceil_pessim, color="#1e8449", alpha=0.10)
ax1.plot(x, ceil_strong, "s-", color="#2471a3", lw=2, label="containment ceiling — strong (Zylon, whole-bag)")
ax1.plot(x, ceil_pessim, "s--", color="#5dade2", lw=1.6, label="containment ceiling — pessimistic (patch, lightweight)")
ax1.plot(x, floor_fast, "^-", color="#b7950b", lw=1.6, label="floor — fast-rotator (0.28 rpm)")
ax1.plot(x, floor_p95, "o-", color="#c0392b", lw=1.8, label="floor — p95 spin")
ax1.plot(x, floor_p50, "o--", color="#e59866", lw=1.4, label="floor — p50 spin")
ax1.axhline(frag["weak_1kPa"], color="#7d3c98", ls=":", lw=1.4)
ax1.text(0.02, frag["weak_1kPa"] * 1.08, f"chunk fragmentation, weak ice 1 kPa ({frag['weak_1kPa']} m/s)",
         color="#7d3c98", fontsize=7.5)
ax1.annotate("FEASIBLE WINDOW\n(floor mm/s  ≪  ceiling m/s)", (1.5, 0.15), fontsize=10,
             color="#1e8449", ha="center", weight="bold")
ax1.set_yscale("log")
ax1.set_xticks(x); ax1.set_xticklabels([f"{m} t" for m in masses])
ax1.set_ylabel("closing velocity (m/s, log)")
ax1.set_xlabel("chunk mass")
ax1.set_title("A feasible closing-velocity window exists at every chunk mass\n"
              "containment ceiling sits 40×–15000× above the ring-dynamics floor")
ax1.legend(fontsize=7.2, loc="center right")
ax1.grid(alpha=0.3, which="both", axis="y")

# Panel 2: window ratio (ceiling/floor) by mass, with the 10x / 100x guides
ratio_p50 = [g[f"{m}t"]["window_ratio"]["strong_over_floor_p50"] for m in masses]
ratio_p95 = [g[f"{m}t"]["window_ratio"]["pessim_over_floor_p95"] for m in masses]
ratio_fast = [g[f"{m}t"]["window_ratio"]["pessim_over_floor_fast"] for m in masses]
ax2.plot(x, ratio_p50, "o-", color="#2471a3", lw=2, label="strong ceiling / p50 floor (nominal)")
ax2.plot(x, ratio_p95, "o-", color="#c0392b", lw=2, label="pessim ceiling / p95 floor")
ax2.plot(x, ratio_fast, "^--", color="#b7950b", lw=1.8, label="pessim ceiling / fast-rotator floor")
ax2.axhline(100, color="#1e8449", ls="--", lw=1, alpha=0.7)
ax2.axhline(10, color="#c0392b", ls="--", lw=1, alpha=0.7)
ax2.text(0.02, 110, "100× (H-J3)", color="#1e8449", fontsize=8)
ax2.text(0.02, 11, "10× (H-J5)", color="#c0392b", fontsize=8)
ax2.annotate("fast-rotator 200 t under worst containment\n→ 7.4× (H-J5 falsified here — despin the\nlargest fast rotators)",
             (3, ratio_fast[-1]), xytext=(1.15, 25), fontsize=7.6, color="#b7950b",
             arrowprops=dict(arrowstyle="->", color="#b7950b"))
ax2.set_yscale("log")
ax2.set_xticks(x); ax2.set_xticklabels([f"{m} t" for m in masses])
ax2.set_ylabel("window ratio  ceiling / floor")
ax2.set_xlabel("chunk mass")
ax2.set_title("Window margin: robust everywhere except the\nfast-rotator + largest-mass + worst-containment corner")
ax2.legend(fontsize=7.6, loc="upper right")
ax2.grid(alpha=0.3, which="both", axis="y")

fig.suptitle("R-chunk-capture-closing-velocity-window — bet #1 containment is a GNC/mechanism wall, "
             "not a structural/energy wall (the physics ceiling is 40×–15000× above the achievable floor)",
             fontsize=9.5, y=1.005)
fig.tight_layout()
fig.savefig(HERE / "results" / "closing_velocity_window.png", dpi=130, bbox_inches="tight")
print("wrote", HERE / "results" / "closing_velocity_window.png")
