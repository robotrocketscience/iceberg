#!/usr/bin/env python3
"""R-harvest-draw-symmetrization — polar port + barbecue roll vs the CoM walk.

Closed form, deterministic. Writes results/ next to this file.
"""
import json
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
RESULTS.mkdir(exist_ok=True)

G0 = 9.80665
DV = 4200.0
ISP_MAIN = 800.0
VE = ISP_MAIN * G0
ETA_THR = 0.6
SHIP_DRY = 20_000.0
CHUNKS_T = [25, 40, 80, 200]
DENS = {"solid_900": 900.0, "porous_500": 500.0}
POWERS = [10.0, 30.0, 100.0]
SUN_SPLITS = [0.6, 0.8, 1.0]
DELTA_PORT = 0.3          # m port placement tolerance
ROLL_PERIOD = 86400.0     # s (1 rev/day)
SLEW_RATE = math.radians(3.0) / 86400.0   # 3 deg/day tracking, generous
RCS_ARM, RCS_ISP, RCS_ETA = 3.0, 70.0, 0.7


def radius(m, rho):
    return (3 * m / (4 * math.pi * rho)) ** (1 / 3)


def draw_fraction(chunk_kg):
    m0 = SHIP_DRY + chunk_kg
    prop = m0 * (1 - math.exp(-DV / VE))
    return min(prop / chunk_kg, 0.95), prop


def thrust(p_kwe):
    return 2 * ETA_THR * p_kwe * 1000.0 / VE


f_ = {"H1": {"cases": {}, "held": True}, "H2": {"cases": {}, "held": True},
      "H3": {"cases": {}, "held": True}, "H4": {"cases": {}, "held": True}}

for name, rho in DENS.items():
    for mt in CHUNKS_T:
        m = mt * 1000.0
        r = radius(m, rho)
        f, prop = draw_fraction(m)

        # H1: polar-port draw walk with placement tolerance
        walk1 = f * DELTA_PORT / (1 - f)
        f_["H1"]["cases"][f"{name}_{mt}t"] = round(walk1, 3)
        if walk1 >= 0.25:
            f_["H1"]["held"] = False

        # H2: no-roll sun-side ablation walk at s >= 0.6
        for s in SUN_SPLITS:
            walk2 = f * (2 * s - 1) * (3 / 8) * r / (1 - f)
            f_["H2"]["cases"][f"{name}_{mt}t_s{s:g}"] = round(walk2, 2)
        if name == "porous_500" and mt >= 40:
            w06 = f * (2 * 0.6 - 1) * (3 / 8) * r / (1 - f)
            if w06 <= 0.5:
                f_["H2"]["held"] = False

        # H3: residual walk with roll — one uncancelled revolution of ablated mass
        for p in POWERS:
            mdot = thrust(p) / VE
            for s in SUN_SPLITS:
                dm_rev = mdot * ROLL_PERIOD
                resid = (dm_rev / m) * (3 / 8) * r * (2 * s - 1) / (1 - f)
                key = f"{name}_{mt}t_{p:g}kWe_s{s:g}"
                f_["H3"]["cases"][key] = round(resid, 5)
                if resid >= 0.05:
                    f_["H3"]["held"] = False

        # H4: gyroscopic tax of slewing the rolling stack
        i_ax = 0.4 * m * r * r + 0.4 * SHIP_DRY * 2.5**2
        omega_roll = 2 * math.pi / ROLL_PERIOD
        L_roll = i_ax * omega_roll
        for p in POWERS:
            t_burn = prop / (thrust(p) / VE)
            tau_prec = SLEW_RATE * L_roll                     # N·m
            ang_imp = tau_prec * t_burn
            rcs_kg = ang_imp / (RCS_ARM * G0 * RCS_ISP * RCS_ETA)
            f_["H4"]["cases"][f"{name}_{mt}t_{p:g}kWe"] = round(rcs_kg, 4)
            if rcs_kg >= 1.0:
                f_["H4"]["held"] = False

# figure: three strategies per chunk (porous, worst density; s=1.0 for no-roll)
fig, ax = plt.subplots(figsize=(9, 5.5))
x = np.arange(len(CHUNKS_T))
one_sided, polar, rolled = [], [], []
for mt in CHUNKS_T:
    m = mt * 1000.0
    r = radius(m, 500.0)
    f, _ = draw_fraction(m)
    one_sided.append(f * (3 / 8) * r / (1 - f))
    polar.append(f * DELTA_PORT / (1 - f))
    mdot = thrust(10.0) / VE
    rolled.append(max((mdot * ROLL_PERIOD / m) * (3 / 8) * r / (1 - f),
                      1e-4))
w = 0.26
ax.bar(x - w, one_sided, w, color="#e34948", label="side port, no roll (round-169 default)")
ax.bar(x, polar, w, color="#eda100", label="polar port, δ = 0.3 m placement")
ax.bar(x + w, rolled, w, color="#256abf", label="polar port + 1 rev/day roll (sun channel)")
ax.axhline(0.5, color="#26251f", ls=":", lw=1.2)
ax.text(2.35, 0.56, "kill regime begins (ε = 0.5 m)", fontsize=8, color="#26251f")
ax.axhline(0.2, color="#6f6c64", ls="--", lw=1)
ax.text(2.5, 0.14, "3° gimbal suffices below 0.2 m", fontsize=8, color="#6f6c64")
ax.set_yscale("log")
ax.set_xticks(x, [f"{mt} t" for mt in CHUNKS_T])
ax.set_ylabel("transverse center-of-mass walk [m]")
ax.set_title("Draw geometry, not gimbal range, controls the walk — porous chunk, worst case")
ax.grid(True, axis="y", which="both", alpha=0.25)
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig(RESULTS / "walk_strategies.png", dpi=160)

with open(RESULTS / "findings.json", "w") as fh:
    json.dump(f_, fh, indent=1)

for h in ["H1", "H2", "H3", "H4"]:
    print(h, "HELD" if f_[h]["held"] else "FALSIFIED")
print("H1 worst walk [m]:", max(f_["H1"]["cases"].values()))
print("H2 s=0.6 porous 40t+ [m]:", {k: v for k, v in f_["H2"]["cases"].items() if "porous" in k and "s0.6" in k})
print("H3 worst residual [m]:", max(f_["H3"]["cases"].values()))
print("H4 worst rcs [kg]:", max(f_["H4"]["cases"].values()))
