#!/usr/bin/env python3
"""Figure for R-berth-momentum-management. Reads results/berth_momentum_findings.json."""
import json
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

RESULTS = Path(__file__).resolve().parent / "results"
F = json.loads((RESULTS / "berth_momentum_findings.json").read_text())

MU_S, R_RING = 3.793e16, 1.07e8
T_ORB = F["anchors"]["T_orbit_s"]
BAG_T = 40_000.0
L_BERTH = F["anchors"]["L_berth_Nms"]

fig, ax = plt.subplots(2, 2, figsize=(13, 9))
fig.suptitle("R-berth-momentum-management — the 3-leg momentum trade at berth "
             "(all H1–H4 HELD)", fontsize=13, fontweight="bold")

# -- Panel 1 (H1): GG clear-time vs r_off, per eta_gg --
a = ax[0, 0]
r_offs = np.linspace(1, 10, 60)
for eta, col in zip((0.15, 0.30, 0.50), ("#1b4965", "#5fa8d3", "#a8d0e6")):
    days = []
    for r in r_offs:
        di = BAG_T * r ** 2
        tau = (3 * MU_S / (2 * R_RING ** 3)) * di
        shed = eta * tau * T_ORB
        L = 20_000.0 * 0.05 * r          # injection also scales with r_off
        days.append(L / shed * T_ORB / 86400.0)
    a.plot(r_offs, days, color=col, lw=2, label=f"η_gg = {eta:.2f}")
a.axhline(30, ls="--", color="#c1121f", lw=1.3, label="falsify (30 d)")
a.axvline(5, ls=":", color="0.5", lw=1)
a.annotate("sim anchor\nr_off = 5 m", (5, 12), fontsize=8, color="0.35")
a.set_xlabel("capture arm r_off (m)")
a.set_ylabel("GG desaturation clear-time (days)")
a.set_title("H1 [S] — GG clears one berth injection in days (boulder-strengthened)",
            fontsize=10)
a.legend(fontsize=8, loc="upper left")
a.grid(alpha=0.3)

# -- Panel 2 (H2): mass comparison bars --
a = ax[0, 1]
c = F["H2"]["cases"]
groups = ["thruster\ndump (CG)", "thruster\ndump (MET)", "CMG buffer\n(×1)",
          "CMG buffer\n(×2 redun)"]
sim = [c["sim_20t"]["thruster_kg_coldgas"], c["sim_20t"]["thruster_kg_met"],
       c["sim_20t"]["cmg_buffer_kg"], c["sim_20t"]["cmg_buffer_x2_kg"]]
full = [c["full_bag"]["thruster_kg_coldgas"], c["full_bag"]["thruster_kg_met"],
        c["full_bag"]["cmg_buffer_kg"], c["full_bag"]["cmg_buffer_x2_kg"]]
x = np.arange(len(groups))
a.bar(x - 0.2, sim, 0.38, color="#5fa8d3", label="L = 5000 (sim 20 t half)")
a.bar(x + 0.2, full, 0.38, color="#1b4965", label="L = 10000 (full 40 t bag)")
for xi, v in zip(x - 0.2, sim):
    a.text(xi, v + 15, f"{v:.0f}", ha="center", fontsize=7.5)
for xi, v in zip(x + 0.2, full):
    a.text(xi, v + 15, f"{v:.0f}", ha="center", fontsize=7.5)
a.set_xticks(x)
a.set_xticklabels(groups, fontsize=8)
a.set_ylabel("mass cost (kg)")
a.set_title("H2 [S] — GG-desat buffer (CMG) ≫ thruster propellant: it buys "
            "plume-avoidance, not mass", fontsize=9.5)
a.legend(fontsize=8)
a.grid(alpha=0.3, axis="y")

# -- Panel 3 (H3): RW-only geometry corner --
a = ax[1, 0]
r = np.linspace(0.5, 12, 120)
vc_lo = (100.0 / 20_000.0) / r * 1000     # mm/s
vc_hi = (150.0 / 20_000.0) / r * 1000
a.fill_between(r, 0, vc_lo, color="#8ac926", alpha=0.35,
               label="RW-only (no dump) — feasible")
a.plot(r, vc_lo, color="#5a8a12", lw=1.5)
a.plot(r, vc_hi, color="#8ac926", lw=1.5, ls="--",
       label="cluster upper bound (150 N·m·s)")
a.axhline(1.0, color="#c1121f", ls="--", lw=1.2,
          label="capture-control floor ~1 mm/s")
a.axvline(5, ls=":", color="0.5", lw=1)
a.scatter([5], [50], color="#c1121f", zorder=5, marker="x", s=70)
a.annotate("sim anchor: r_off=5 m,\nv_c=50 mm/s → L=5000\n(RWs saturate, tumble)",
           (4.7, 50), (6.2, 60), fontsize=7.5, color="#c1121f",
           arrowprops=dict(arrowstyle="->", color="#c1121f", lw=0.8))
a.set_yscale("log")
a.set_ylim(0.3, 120)
a.set_xlabel("capture arm r_off (m)")
a.set_ylabel("max closing rate v_c for RW-only (mm/s, log)")
a.set_title("H3 [S] — capture-geometry control kills the dump: r_off ≤ 2 m at "
            "a few mm/s", fontsize=9.5)
a.legend(fontsize=7.5, loc="lower left")
a.grid(alpha=0.3, which="both")

# -- Panel 4 (H4): synthesis table --
a = ax[1, 1]
a.axis("off")
legs = F["H4"]["legs"]
rows = [["leg", "prop\n(kg)", "plume\nat bag", "+dry\n(kg)", "cadence\nfloor (d)"]]
disp = {"A_thruster": "A: thruster", "B_gg_desat": "B: GG-desat",
        "C_geometry": "C: geometry"}
for k in ("C_geometry", "B_gg_desat", "A_thruster"):
    v = legs[k]
    rows.append([disp[k], f"{v['propellant_kg']:.0f}",
                 "yes" if v["plume_at_bag"] else "no",
                 f"{v['extra_dry_kg']:.0f}", f"{v['cadence_floor_days']:.1f}"])
tbl = a.table(cellText=rows[1:], colLabels=rows[0], loc="center",
              cellLoc="center", colWidths=[0.30, 0.15, 0.17, 0.15, 0.20])
tbl.auto_set_font_size(False)
tbl.set_fontsize(9)
tbl.scale(1, 2.2)
for j in range(5):
    tbl[0, j].set_facecolor("#1b4965")
    tbl[0, j].set_text_props(color="white", fontweight="bold")
tbl[1, 0].set_facecolor("#c8e6a0")   # leg C preferred
a.set_title("H4 [W] — leg C < B < A: geometry control preferred where reachable; "
            "\nthrusters the robust fallback; GG-desat only if plume is a "
            "showstopper", fontsize=9.5)
a.text(0.5, 0.06, "propellant 0.042% of wet mass (immaterial) · GG clear 2.5–8.3 d "
       "· sim: RWs saturate at berth so SOME sink is required",
       transform=a.transAxes, ha="center", fontsize=7.8, color="0.4")

fig.tight_layout(rect=(0, 0, 1, 0.96))
out = RESULTS / "berth_momentum.png"
fig.savefig(out, dpi=130)
print(f"wrote {out}")
