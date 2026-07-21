#!/usr/bin/env python3
"""R-chunk-despin-budget — de-spin propellant/time budget vs pre-registered H1-H5.

Deterministic (seed=0). Writes results/ next to this file.
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
RPM = 2 * math.pi / 60.0  # rad/s per rpm

# --- registered parameters (SCOPE §Method) ---
CHUNK_T = [10, 25, 40, 80, 200]           # tonnes
DENSITIES = {"solid_900": 900.0, "porous_500": 500.0}
K_TUMBLE = 1.5
D_EFF = 3.0                                # m, envelope-corner couple arm
ETA = 0.7
ISP = {"coldgas_70": 70.0, "met_800": 800.0}
MU_ICE_FABRIC = 0.1
CINCH_PA = [1.0, 10.0, 100.0]
SHIP_T = 50.0
OFFSET_L = 5.0                             # m, chunk-ship CoM separation
N_MC = 20_000
FLOOR_KG = 25_000.0

# Tier 0.5 size-conditioned spin priors (log-normal on rpm)
# 1-10 m class (chunks <= 40 t): median 0.01 rpm; 10-100 m class: median 0.002 rpm.
# sigma_log = 0.4 dex -> sigma_ln = 0.4 * ln(10)
SIG_LN = 0.4 * math.log(10)


def prior_median_rpm(mass_t: float) -> float:
    return 0.01 if mass_t <= 40 else 0.002


def radius_m(mass_kg: float, rho: float) -> float:
    return (3 * mass_kg / (4 * math.pi * rho)) ** (1.0 / 3.0)


def inertia(mass_kg: float, rho: float) -> float:
    return 0.4 * mass_kg * radius_m(mass_kg, rho) ** 2


def despin_prop_kg(L: float, isp: float) -> float:
    return L * K_TUMBLE / (D_EFF * G0 * isp * ETA)


rng = np.random.default_rng(0)
findings = {"H1": {}, "H2": {}, "H3": {}, "H4": {}, "H5": {}}

# --- H1: Monte Carlo over prior, cold-gas, both densities, p95 per chunk mass ---
h1_p95 = {}
for name, rho in DENSITIES.items():
    for mt in CHUNK_T:
        m = mt * 1000.0
        med = prior_median_rpm(mt)
        spins = np.exp(rng.normal(math.log(med), SIG_LN, N_MC))  # rpm
        L = inertia(m, rho) * spins * RPM
        prop = despin_prop_kg(L, ISP["coldgas_70"])
        h1_p95[f"{name}_{mt}t"] = {
            "p50_kg": float(np.percentile(prop, 50)),
            "p95_kg": float(np.percentile(prop, 95)),
            "p99_kg": float(np.percentile(prop, 99)),
        }
findings["H1"] = {
    "cases": h1_p95,
    "max_p95_kg": max(v["p95_kg"] for v in h1_p95.values()),
    "held": all(v["p95_kg"] < 1.0 for v in h1_p95.values()),
}

# --- H2: deterministic 1 rpm stress on 200 t porous ---
m200 = 200_000.0
L_stress = inertia(m200, 500.0) * 1.0 * RPM
h2_cold = despin_prop_kg(L_stress, ISP["coldgas_70"])
h2_met = despin_prop_kg(L_stress, ISP["met_800"])
findings["H2"] = {
    "L_Nms": L_stress,
    "coldgas_kg": h2_cold,
    "met_kg": h2_met,
    "held": bool(h2_cold < 125.0 and h2_met < 15.0),
}

# --- H3: fabric-friction damping time, worst case in envelope ---
h3 = {}
worst_time = 0.0
for pc in CINCH_PA:
    for name, rho in DENSITIES.items():
        for mt in [10, 200]:
            m = mt * 1000.0
            r = radius_m(m, rho)
            A = 2 * math.pi * r * r          # half-sphere contact
            tau = MU_ICE_FABRIC * pc * A * (2.0 / 3.0) * r
            L1 = inertia(m, rho) * 1.0 * RPM  # 1 rpm stress
            t = L1 / tau
            h3[f"p{pc:g}_{name}_{mt}t"] = {"tau_Nm": tau, "t_damp_s": t}
            worst_time = max(worst_time, t)
findings["H3"] = {"worst_damp_s": worst_time, "held": worst_time < 3600.0}

# --- H4: stack spin-up ---
h4 = {}
ok4 = True
for name, rho in DENSITIES.items():
    for mt in CHUNK_T:
        m = mt * 1000.0
        m_ship = SHIP_T * 1000.0
        mu_red = m * m_ship / (m + m_ship)
        I_stack = inertia(m, rho) + 0.4 * m_ship * 2.5**2 + mu_red * OFFSET_L**2
        for label, spin in [("median", prior_median_rpm(mt)), ("stress_1rpm", 1.0)]:
            L = inertia(m, rho) * spin * RPM
            w = L / I_stack / RPM * 6.0  # rad/s -> deg/s: *180/pi ; rpm*6 = deg/s
            w_degs = L / I_stack * 180.0 / math.pi
            h4[f"{name}_{mt}t_{label}"] = w_degs
            lim = 0.1 if label == "median" else 5.0
            if w_degs > lim:
                ok4 = False
findings["H4"] = {"cases_deg_s": h4, "held": ok4}

# --- H5: closure impact on audit sweep ---
_rel = Path(__file__).resolve().parents[2] / "sims/mission_graph/runs/audit_capture_efficiency/20260522T175555Z/cells.jsonl"
cells_path = _rel if _rel.exists() else (
    Path.home() / "projects/iceberg/water-prop/sims/mission_graph/runs/audit_capture_efficiency/20260522T175555Z/cells.jsonl"
)  # sweep output is gitignored; regenerate via missions/sweeps/saturn_water_canonical_sweep.py
worst_p95 = findings["H1"]["max_p95_kg"]
flips = 0
n_close_before = n_close_after = 0
with open(cells_path) as fh:
    for line in fh:
        cell = json.loads(line)
        best = 0.0
        for res in cell.get("results", []):
            # bug-catch 2026-07-20: first version read res["delivered_mass_kg"],
            # a field that does not exist -> every cell scored 0 and H5 was
            # vacuously "held". Delivered water is leaf_state.payload_kg.
            if res.get("infeasible_at") is None:
                dm = (res.get("leaf_state") or {}).get("payload_kg", 0.0)
                best = max(best, float(dm))
        before = best >= FLOOR_KG
        after = (best - worst_p95) >= FLOOR_KG
        n_close_before += before
        n_close_after += after
        flips += before != after
findings["H5"] = {
    "cells_close_before": n_close_before,
    "cells_close_after": n_close_after,
    "flips": flips,
    "despin_charge_kg": worst_p95,
    "held": flips == 0,
}

# --- figures ---
spin_grid = np.logspace(-3, 0, 200)  # rpm
fig, ax = plt.subplots(figsize=(9, 6))
colors = plt.cm.viridis(np.linspace(0.15, 0.9, len(CHUNK_T)))
for c, mt in zip(colors, CHUNK_T):
    m = mt * 1000.0
    L = inertia(m, 500.0) * spin_grid * RPM  # porous = conservative
    ax.loglog(spin_grid, despin_prop_kg(L, ISP["coldgas_70"]), color=c,
              label=f"{mt} t chunk (cold-gas 70 s)")
    ax.loglog(spin_grid, despin_prop_kg(L, ISP["met_800"]), color=c, ls="--", alpha=0.6)
ax.axvspan(0.0005, 0.05, color="tab:blue", alpha=0.12,
           label="Tier 0.5 prior 90% band")
ax.axvline(0.28, color="tab:red", ls=":", lw=1,
           label="CIRS slow-rotator bound (1 m class)")
ax.axhline(125, color="gray", lw=0.8, ls="-.")
ax.text(0.3, 140, "H2 bound 125 kg", fontsize=8, color="gray")
ax.set_xlabel("chunk spin rate [rpm]")
ax.set_ylabel("de-spin propellant [kg]  (solid = cold-gas 70 s, dashed = MET 800 s)")
ax.set_title("De-spin propellant vs spin rate — porous 500 kg/m³, tumbling ×1.5, arm 3 m, η 0.7")
ax.grid(True, which="both", alpha=0.25)
ax.legend(fontsize=8, loc="upper left")
fig.tight_layout()
fig.savefig(RESULTS / "despin_budget.png", dpi=160)

fig2, ax2 = plt.subplots(figsize=(9, 5))
for pc, ls in zip(CINCH_PA, ["-", "--", ":"]):
    times = []
    for s in spin_grid:
        m = 200_000.0
        r = radius_m(m, 500.0)
        tau = MU_ICE_FABRIC * pc * (2 * math.pi * r * r) * (2.0 / 3.0) * r
        times.append(inertia(m, 500.0) * s * RPM / tau)
    ax2.loglog(spin_grid, times, ls=ls, label=f"cinch pressure {pc:g} Pa")
ax2.axhline(3600, color="tab:red", lw=1, ls="-.", label="H3 bound: 1 hour")
ax2.axvspan(0.0005, 0.05, color="tab:blue", alpha=0.12)
ax2.set_xlabel("chunk spin rate [rpm]")
ax2.set_ylabel("passive fabric-friction damping time [s]")
ax2.set_title("Passive de-spin inside the cinched bag — 200 t porous chunk, μ = 0.1")
ax2.grid(True, which="both", alpha=0.25)
ax2.legend(fontsize=8)
fig2.tight_layout()
fig2.savefig(RESULTS / "despin_time_fabric.png", dpi=160)

with open(RESULTS / "despin_findings.json", "w") as fh:
    json.dump(findings, fh, indent=1)

for h in ["H1", "H2", "H3", "H4", "H5"]:
    print(h, "HELD" if findings[h]["held"] else "FALSIFIED")
print("H1 max p95 [kg]:", round(findings["H1"]["max_p95_kg"], 4))
print("H2 cold/met [kg]:", round(h2_cold, 1), "/", round(h2_met, 2))
print("H3 worst damp [s]:", round(worst_time, 1))
print("H4 worst median case [deg/s]:", round(max(v for k, v in h4.items() if k.endswith("median")), 5))
print("H5 flips:", flips, "of", n_close_before, "closing cells")
