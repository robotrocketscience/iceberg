#!/usr/bin/env python3
"""Figure for R-berth-dump-axis-geometry. Reads results/geometry_findings.json."""
import json
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, Circle, FancyArrow

RESULTS = Path(__file__).resolve().parent / "results"
F = json.loads((RESULTS / "geometry_findings.json").read_text())

fig, ax = plt.subplots(2, 2, figsize=(13, 9))
fig.suptitle("R-berth-dump-axis-geometry — the last question, closed (all H1–H4 HELD): "
             "a plume-safe dump couple exists for every required axis",
             fontsize=12, fontweight="bold")

# -- Panel 1 (H2): bag-plume torque vs dump azimuth --
a = ax[0, 0]
sweep = F["H2"]["sweep_boom3"]
deg = [d for d, _ in sweep]
tau = [t for _, t in sweep]
a.plot(deg, tau, color="#5fa8d3", lw=2, label="tangential couple, boom=3 m")
a.axhline(2.5, color="#c1121f", ls="--", lw=1.5, label="re-perturb threshold (2.5 N·m)")
a.fill_between(deg, 0, tau, color="#8ac926", alpha=0.3)
a.set_ylim(0, 2.8)
a.set_xlim(0, 355)
a.set_xlabel("required dump-axis azimuth φ (deg, in-plane)")
a.set_ylabel("bag-plume torque (N·m)")
a.set_title("H2 [S] — every in-plane dump axis is plume-safe (66× margin)",
            fontsize=10)
a.annotate("max 0.038 N·m\n(1/66 of threshold)", (180, 0.35), fontsize=8.5,
           color="#5a8a12", ha="center")
a.legend(fontsize=8, loc="upper right")
a.grid(alpha=0.3)

# -- Panel 2: geometry schematic (x-z projection) --
a = ax[0, 1]
a.set_aspect("equal")
# envelope box
a.add_patch(Rectangle((-4, -4), 8, 8, fill=False, ec="0.3", lw=1.5))
a.text(0, 0, "vehicle\nenvelope", ha="center", va="center", fontsize=8, color="0.4")
# bag up at +z
a.add_patch(Circle((0, 10), 3, fc="#a8d0e6", ec="#1b4965", lw=1.5, alpha=0.7))
a.text(0, 10, "40 t\nbag", ha="center", va="center", fontsize=8.5, color="#1b4965")
a.plot([0, 0], [4, 7], color="#1b4965", lw=2)          # boom
a.text(0.4, 5.5, "boom ≥ 3 m", fontsize=8, color="#1b4965")
# tangential thrusters (top): sideways plume (safe)
for (x, sign) in [(-4, -1), (4, 1)]:
    a.add_patch(FancyArrow(x, 4, sign * 2.4, 0, width=0.15, head_width=0.6,
                           head_length=0.6, color="#5fa8d3", length_includes_head=True))
a.text(-6.6, 4.8, "tangential plume\n(sideways → backflow, safe)", fontsize=7.5,
       color="#2a7ab0")
# retro thruster (bottom corner): plume toward bag (danger)
a.add_patch(FancyArrow(3.2, -4, -3.0, 12.5, width=0.12, head_width=0.6,
                       head_length=0.7, color="#c1121f", length_includes_head=True,
                       alpha=0.65))
a.text(3.6, -2.5, "retro plume\n(→ bag core,\ndanger; avoided)", fontsize=7.5,
       color="#c1121f")
a.set_xlim(-8, 8)
a.set_ylim(-6, 14)
a.set_xlabel("x (m)")
a.set_ylabel("z / boom axis (m)")
a.set_title("Geometry: injected L ⊥ boom → dump about in-plane axis;\n"
            "tangential couples fire sideways, away from the +z bag", fontsize=9.5)

# -- Panel 3 (H3): per-thruster bag-plume torque by type --
a = ax[1, 0]
g = F["H3"]["groups"]
labels = ["tangential\n(T2)", "prograde +z\n(P0)", "retro −z\n(R0)"]
vals = [g["T2"]["torque_Nm"], g["P0"]["torque_Nm"], g["R0"]["torque_Nm"]]
cols = ["#5fa8d3", "#8ac926", "#c1121f"]
bars = a.bar(labels, vals, color=cols, width=0.6)
for b, v, gg in zip(bars, vals, ["T2", "P0", "R0"]):
    a.text(b.get_x() + b.get_width() / 2, v + 0.05,
           f"{v:.2f} N·m\n{g[gg]['angle_deg']:.0f}° ({g[gg]['regime']})",
           ha="center", fontsize=8)
a.axhline(2.5, color="0.2", ls="--", lw=1.3, label="re-perturb threshold (2.5 N·m)")
a.set_ylim(0, 2.9)
a.set_ylabel("bag-plume torque (N·m)")
a.set_title("H3 [S] — retro (−z) is the lone danger; tangential/prograde safe "
            "& span the in-plane axes", fontsize=9.5)
a.legend(fontsize=8)
a.grid(alpha=0.3, axis="y")

# -- Panel 4: thread closure --
a = ax[1, 1]
a.axis("off")
a.set_title("H4 [W] — the momentum-management thread CLOSES", fontsize=10)
txt = (
    "The thread, end to end:\n"
    "  bag-6dof sim (7a716f3)\n"
    "    → berth gate is momentum, not torque; RWs saturate\n"
    "  momentum trade (b3b579c)\n"
    "    → 3 legs: thruster-dump / GG-desat / geometry-ctrl\n"
    "  plume-impingement (a418d4d)\n"
    "    → plume benign in backflow; leg A viable *if placement*\n"
    "  dump-axis geometry (this round)\n"
    "    → L ⊥ boom ⇒ dump always in-plane ⇒ tangential couple\n"
    "       is plume-safe for EVERY required axis (66× margin)\n\n"
    "CLOSE:  leg A (thruster dump) is UNCONDITIONALLY viable,\n"
    "secured by a cheap plume-aware control-allocation rule\n"
    "(build the couple from tangential thrusters, deprioritize\n"
    "retro) + grapple boom ≥ 3 m.  NO new hardware.\n\n"
    "→ CMG (leg B, ~300–600 kg) and precision-capture (leg C)\n"
    "  are retired to OPTIONAL risk reduction.\n\n"
    "Residual (named): flight-layout confirmation of tangential\n"
    "authority about both in-plane axes — generic for any\n"
    "3-axis-couple RCS.")
a.text(0.02, 0.98, txt, transform=a.transAxes, va="top", ha="left",
       fontsize=8.6, family="monospace")

fig.tight_layout(rect=(0, 0, 1, 0.96))
out = RESULTS / "geometry.png"
fig.savefig(out, dpi=130)
print(f"wrote {out}")
