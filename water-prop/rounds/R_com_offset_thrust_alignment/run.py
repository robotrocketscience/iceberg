#!/usr/bin/env python3
"""R-com-offset-thrust-alignment — RCS-fought vs steer-through-CoM, walk model, closure.

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
DV = 4200.0                 # m/s inbound chunk-fed
ISP_MAIN = 800.0
VE = ISP_MAIN * G0
ETA_THR = 0.6
SHIP_DRY = 20_000.0
POWERS_KWE = [10.0, 30.0, 100.0]
CHUNKS_T = [25, 40, 80, 200]
EPS = [0.1, 0.5, 1.0]       # m offset
LEVERS = [5.0, 10.0]        # m engine-to-CoM
RCS_ARM, RCS_ISP, RCS_ETA = 3.0, 70.0, 0.7
DENSITIES = {"solid_900": 900.0, "porous_500": 500.0}
FLOOR_KG = 25_000.0


def thrust_n(p_kwe: float) -> float:
    return 2 * ETA_THR * p_kwe * 1000.0 / VE


def inbound(chunk_kg: float):
    """Return (propellant_kg, burn_time_s, m0, m1) for the chunk-fed inbound burn."""
    m0 = SHIP_DRY + chunk_kg
    m1 = m0 * math.exp(-DV / VE)
    prop = m0 - m1
    return prop, m0, m1


def burn_time_s(p_kwe: float, m0: float, m1: float) -> float:
    # constant thrust, mass declines linearly with propellant flow: t = prop/mdot
    T = thrust_n(p_kwe)
    mdot = T / VE
    return (m0 - m1) / mdot


findings = {"H1": {"cases": {}, "held": True},
            "H2": {"cases": {}, "held": True},
            "H3": {"cases": {}, "held": True},
            "H4": {}}

# --- H1 (RCS-fought) and H2 (steer-through) over the grid ---
for mt in CHUNKS_T:
    m_c = mt * 1000.0
    prop, m0, m1 = inbound(m_c)
    for p in POWERS_KWE:
        t_burn = burn_time_s(p, m0, m1)
        T = thrust_n(p)
        for e in EPS:
            ang_imp = T * e * t_burn                       # N·m·s
            rcs_kg = ang_imp / (RCS_ARM * G0 * RCS_ISP * RCS_ETA)
            findings["H1"]["cases"][f"{mt}t_{p:g}kWe_eps{e:g}"] = round(rcs_kg, 1)
            if mt >= 25 and e >= 0.5 and rcs_kg <= 5000.0:
                findings["H1"]["held"] = False
        for l in LEVERS:
            theta = math.atan(1.0 / l) if l == 5.0 else math.atan(1.0 / l)
    # steer-through per (eps, lever): tax independent of power
    for e in EPS:
        for l in LEVERS:
            theta = math.atan(e / l)
            tax = prop * (1.0 / math.cos(theta) - 1.0)
            findings["H2"]["cases"][f"{mt}t_eps{e:g}_l{l:g}"] = {
                "theta_deg": round(math.degrees(theta), 2),
                "tax_kg": round(tax, 1),
                "tax_pct_of_inbound": round(100 * tax / prop, 3),
            }
            if math.degrees(theta) > 11.4 + 1e-9 or tax / prop > 0.02:
                findings["H2"]["held"] = False
worst = findings["H1"]["cases"].get("200t_10kWe_eps1")
findings["H1"]["worst_corner_kg"] = worst
if worst is not None and worst <= 50_000.0:
    findings["H1"]["held"] = False

# --- H3: CoM walk under one-sided draw ---
for name, rho in DENSITIES.items():
    for mt in CHUNKS_T:
        m_c = mt * 1000.0
        prop, m0, m1 = inbound(m_c)
        f = min(prop / m_c, 0.95)
        r = (3 * m_c / (4 * math.pi * rho)) ** (1.0 / 3.0)
        walk = f * (3.0 / 8.0) * r / (1.0 - f)
        findings["H3"]["cases"][f"{name}_{mt}t"] = {
            "draw_fraction": round(f, 3), "radius_m": round(r, 2), "walk_m": round(walk, 2)
        }
        if mt >= 40 and walk <= 0.5:
            findings["H3"]["held"] = False

# --- H4: closure discrimination ---
_rel = Path(__file__).resolve().parents[2] / "sims/mission_graph/runs/audit_capture_efficiency/20260522T175555Z/cells.jsonl"
cells_path = _rel if _rel.exists() else (
    Path.home() / "projects/iceberg/water-prop/sims/mission_graph/runs/audit_capture_efficiency/20260522T175555Z/cells.jsonl"
)  # sweep output is gitignored; regenerate via missions/sweeps/saturn_water_canonical_sweep.py
theta_worst = math.atan(1.0 / 5.0)
cos_factor = 1.0 / math.cos(theta_worst) - 1.0
flips_steer = flips_rcs = n_close = 0
with open(cells_path) as fh:
    for line in fh:
        cell = json.loads(line)
        best = 0.0
        for res in cell.get("results", []):
            if res.get("infeasible_at") is None:
                best = max(best, float((res.get("leaf_state") or {}).get("payload_kg", 0.0)))
        if best < FLOOR_KG:
            continue
        n_close += 1
        chunk_kg = cell["coords"]["chunk_mass_kg"]
        prop, m0, m1 = inbound(chunk_kg)
        steer_tax = prop * cos_factor
        # RCS-fought at that cell's power is unknown from coords; use 30 kWe central
        t_burn = burn_time_s(30.0, m0, m1)
        rcs_kg = thrust_n(30.0) * 1.0 * t_burn / (RCS_ARM * G0 * RCS_ISP * RCS_ETA)
        if best - steer_tax < FLOOR_KG:
            flips_steer += 1
        if best - rcs_kg < FLOOR_KG:
            flips_rcs += 1
findings["H4"] = {
    "closing_cells": n_close,
    "flips_steer_through": flips_steer,
    "flips_rcs_fought": flips_rcs,
    "held": bool(flips_steer == 0 and flips_rcs == n_close),
}

# --- figures ---
fig, ax = plt.subplots(figsize=(9, 6))
x = np.arange(len(CHUNKS_T))
width = 0.25
for i, p in enumerate(POWERS_KWE):
    vals = [findings["H1"]["cases"][f"{mt}t_{p:g}kWe_eps0.5"] / 1000.0 for mt in CHUNKS_T]
    ax.bar(x + (i - 1) * width, vals, width, label=f"RCS-fought, {p:g} kWe, ε=0.5 m")
steer = [findings["H2"]["cases"][f"{mt}t_eps1_l5"]["tax_kg"] / 1000.0 for mt in CHUNKS_T]
ax.plot(x, steer, "k^-", label="steer-through cosine tax, worst case (ε=1.0 m, l=5 m)")
ax.set_yscale("log")
ax.set_xticks(x, [f"{mt} t" for mt in CHUNKS_T])
ax.set_ylabel("attitude propellant over inbound burn [tonnes]")
ax.set_title("Pushing an offset center of mass: fight it with RCS vs steer through it")
ax.axhline(FLOOR_KG / 1000.0, color="tab:red", ls=":", lw=1)
ax.text(-0.35, 27, "entire 25 t delivery floor", color="tab:red", fontsize=8)
ax.grid(True, axis="y", which="both", alpha=0.25)
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig(RESULTS / "com_offset_costs.png", dpi=160)

fig2, ax2 = plt.subplots(figsize=(8, 5))
for name, rho in DENSITIES.items():
    walks = [findings["H3"]["cases"][f"{name}_{mt}t"]["walk_m"] for mt in CHUNKS_T]
    ax2.plot(CHUNKS_T, walks, "o-", label=f"{name.replace('_', ' ')} kg/m³")
ax2.axhline(0.5, color="tab:red", ls=":", label="ε = 0.5 m (H1's kill regime)")
ax2.set_xlabel("chunk mass [t]")
ax2.set_ylabel("cargo center-of-mass walk over inbound burn [m]")
ax2.set_title("One-sided sublimation draw walks the center of mass into the kill regime")
ax2.grid(True, alpha=0.25)
ax2.legend(fontsize=9)
fig2.tight_layout()
fig2.savefig(RESULTS / "com_walk.png", dpi=160)

with open(RESULTS / "findings.json", "w") as fh:
    json.dump(findings, fh, indent=1)

for h in ["H1", "H2", "H3", "H4"]:
    print(h, "HELD" if findings[h]["held"] else "FALSIFIED")
print("worst corner RCS-fought [t]:", round((findings['H1']['worst_corner_kg'] or 0)/1000.0, 1))
print("worst steer tax [kg]:", max(v['tax_kg'] for v in findings['H2']['cases'].values()))
print("H3 walks [m]:", {k: v['walk_m'] for k, v in findings['H3']['cases'].items() if '40t' in k or '200t' in k})
print("H4:", findings["H4"])
