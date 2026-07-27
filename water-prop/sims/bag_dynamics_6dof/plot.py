#!/usr/bin/env python3
"""Render the bag-dynamics 6-DOF figure from results/bag_6dof_findings.json.
Runs locally (matplotlib); no Basilisk needed."""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

R = Path(__file__).resolve().parent / "results"
d = json.load(open(R / "bag_6dof_findings.json"))
TS = [60.0, 100.0, 140.0, 180.0]
ZE = [0.02, 0.05, 0.10, 0.20]


def grid(mode, host, key):
    m = np.full((len(ZE), len(TS)), np.nan)
    for c in d[mode]["cells"]:
        if c.get("host") != host or "error" in c:
            continue
        i, j = ZE.index(c["zeta"]), TS.index(c["T_s"])
        m[i, j] = c[key]
    return m


fig, axes = plt.subplots(1, 3, figsize=(15, 4.6))

# panel 1: capture-impulse peak attitude (monolithic) -- all tumble
ax = axes[0]
M = grid("capture_impulse", "monolithic_20t", "peak_attitude_deg")
im = ax.imshow(M, origin="lower", cmap="inferno_r", vmin=0, vmax=180, aspect="auto")
ax.set_xticks(range(len(TS))); ax.set_xticklabels([f"{t:.0f}" for t in TS])
ax.set_yticks(range(len(ZE))); ax.set_yticklabels([f"{z:.2f}" for z in ZE])
ax.set_xlabel("slosh period T_s (s)"); ax.set_ylabel("damping ζ")
for i in range(len(ZE)):
    for j in range(len(TS)):
        ax.text(j, i, f"{M[i,j]:.0f}", ha="center", va="center", color="w", fontsize=8)
ax.set_title("Realistic berth (net-L capture):\npeak attitude — ALL tumble to 180°")
fig.colorbar(im, ax=ax, fraction=0.046, label="peak attitude (deg)")

# panel 2: displacement viable corner (monolithic vs relay)
ax = axes[1]
Vm = grid("displacement", "monolithic_20t", "rw_viable")
Vr = grid("displacement", "relay_4t", "rw_viable")
# encode: 2=both viable, 1=mono only, 0=neither
enc = Vm.astype(float) + Vr.astype(float)  # 0,1,2
im = ax.imshow(enc, origin="lower", cmap="RdYlGn", vmin=0, vmax=2, aspect="auto")
ax.set_xticks(range(len(TS))); ax.set_xticklabels([f"{t:.0f}" for t in TS])
ax.set_yticks(range(len(ZE))); ax.set_yticklabels([f"{z:.2f}" for z in ZE])
ax.set_xlabel("slosh period T_s (s)"); ax.set_ylabel("damping ζ")
for i in range(len(ZE)):
    for j in range(len(TS)):
        lab = {2: "mono+relay", 1: "mono", 0: "neither"}[int(enc[i, j])]
        ax.text(j, i, lab, ha="center", va="center", fontsize=7)
ax.set_title("Mean-zero slosh (R191 picture):\nRW-viable corner (monolithic vs relay)")

# panel 3: the momentum crux
ax = axes[2]
inj = d["anchors"]["capture_injected_L_Nms"]
cap = 3 * d["anchors"]["rw_maxmom_Nms"]     # 3 wheels
labels = ["injected by\n5 cm/s berth", "3× RW\ncapacity", "thruster dump\n(50 N·m, 100 s)"]
vals = [inj, cap, inj]
colors = ["#c44", "#88a", "#2a7"]
bars = ax.bar(labels, vals, color=colors)
ax.set_yscale("log")
for b, v in zip(bars, vals):
    ax.text(b.get_x() + b.get_width() / 2, v, f"{v:.0f}", ha="center", va="bottom", fontsize=9)
ax.set_ylabel("angular momentum (N·m·s, log)")
ax.set_title("The gate is momentum, not torque:\ninjected 5000 ≫ RW store 300 → thrusters")

fig.tight_layout()
fig.savefig(R / "bag_6dof.png", dpi=150)
print("figure ->", R / "bag_6dof.png")
