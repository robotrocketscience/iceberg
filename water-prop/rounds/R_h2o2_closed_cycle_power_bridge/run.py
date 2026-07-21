#!/usr/bin/env python3
"""R-h2o2-closed-cycle-power-bridge — chemical energy bank vs H1-H4.

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
LHV = 13.3e6          # J per kg stoichiometric H2/O2 mix
ETA_FC = 0.55         # fuel-cell electrical efficiency (0.60 for H1 bound)
ETA_TURB = 0.30       # Rankine turbogenerator variant
ETA_THR = 0.6         # thruster jet efficiency
VE_CHEM = 450.0 * G0  # direct H2/O2 burn
PLANT_W_PER_KG = 100.0
TANK_FRAC = 0.20
BOILOFF_FRAC = 0.10
BATT_J_PER_KG = 250 * 3600.0
POWERS_KWE = [5.0, 10.0, 15.0]
MONTHS = [2, 4, 6]
FLOOR_KG = 25_000.0

findings = {"H1": {}, "H2": {"cases": {}, "held": True},
            "H3": {"cases": {}, "held": True}, "H4": {}}

# --- H1: impulse per kg reactant, direct burn vs via-electricity MET ---
isps = np.arange(600, 1001, 50)
ratios = {}
worst_ratio = 1e9
for isp in isps:
    ve = isp * G0
    e_jet_per_kg_prop = 0.5 * ve * ve            # J per kg propellant
    e_elec_per_kg_reactant = LHV * 0.60          # H1 bound uses eta_fc = 0.60
    prop_powered = e_elec_per_kg_reactant * ETA_THR / e_jet_per_kg_prop
    impulse_via = prop_powered * ve              # N·s per kg reactant
    ratio = VE_CHEM / impulse_via
    ratios[int(isp)] = round(ratio, 2)
    worst_ratio = min(worst_ratio, ratio)
findings["H1"] = {"direct_over_via_electric": {k: float(v) for k, v in ratios.items()},
                  "worst_ratio": float(round(worst_ratio, 2)),
                  "held": bool(worst_ratio >= 3.0)}

# --- H2: bridge sizing over the hotel duty grid ---
net_grid = {}
worst_net = 0.0
for p in POWERS_KWE:
    for mo in MONTHS:
        e = p * 1000.0 * mo * 30 * 86400.0       # J electric
        reactants = e / (LHV * ETA_FC)
        plant = p * 1000.0 / PLANT_W_PER_KG
        net = reactants * (TANK_FRAC + BOILOFF_FRAC) + plant
        key = f"{p:g}kWe_{mo}mo"
        net_grid[key] = {"reactants_t": round(reactants / 1000, 2),
                         "net_penalty_t": round(net / 1000, 2)}
        worst_net = max(worst_net, net)
        if net > 6000.0:
            findings["H2"]["held"] = False
corner = net_grid["5kWe_2mo"]["net_penalty_t"]
if corner > 1.5:
    findings["H2"]["held"] = False
findings["H2"]["cases"] = net_grid
findings["H2"]["worst_net_t"] = round(worst_net / 1000, 2)
findings["H2"]["corner_5kWe_2mo_t"] = corner

# --- H3: vs batteries ---
worst_adv = 1e9
for p in POWERS_KWE:
    for mo in MONTHS:
        e = p * 1000.0 * mo * 30 * 86400.0
        m_batt = e / BATT_J_PER_KG
        m_fc_store = e / (LHV * ETA_FC)          # reactants only (storage medium)
        adv = m_batt / m_fc_store
        findings["H3"]["cases"][f"{p:g}kWe_{mo}mo"] = round(adv, 1)
        worst_adv = min(worst_adv, adv)
if worst_adv < 6.0:
    findings["H3"]["held"] = False
findings["H3"]["worst_advantage"] = round(worst_adv, 1)

# --- H4: closure with propulsion-phase power deleted ---
_rel = Path(__file__).resolve().parents[2] / "sims/mission_graph/runs/audit_capture_efficiency/20260522T175555Z/cells.jsonl"
cells_path = _rel if _rel.exists() else (
    Path.home() / "projects/iceberg/water-prop/sims/mission_graph/runs/audit_capture_efficiency/20260522T175555Z/cells.jsonl"
)
ELECTRIC_MARKERS = ("low_thrust_spiral", "chunk_fed_spiral", "met_", "electric")
n_close_with_reactor = n_close_without = 0
with open(cells_path) as fh:
    for line in fh:
        cell = json.loads(line)
        for res in cell.get("results", []):
            if res.get("infeasible_at") is not None:
                continue
            payload = float((res.get("leaf_state") or {}).get("payload_kg", 0.0))
            if payload < FLOOR_KG:
                continue
            n_close_with_reactor += 1
            label = res.get("path_label", "")
            uses_electric = any(m in label for m in ELECTRIC_MARKERS)
            if not uses_electric:
                n_close_without += 1
findings["H4"] = {"closing_paths_with_reactor": n_close_with_reactor,
                  "closing_paths_without_electric_legs": n_close_without,
                  "held": n_close_without == 0}

# --- figures ---
fig, ax = plt.subplots(figsize=(9, 5.5))
x = np.arange(len(MONTHS))
w = 0.25
for i, p in enumerate(POWERS_KWE):
    nets = [net_grid[f"{p:g}kWe_{mo}mo"]["net_penalty_t"] for mo in MONTHS]
    ax.bar(x + (i - 1) * w, nets, w, label=f"{p:g} kWe hotel load")
ax.axhspan(1.5, 3.0, color="#cbd2dc", alpha=0.5, zorder=0)
ax.text(1.62, 2.2, "Kilopower-class reactor system band (1.5–3 t)",
        fontsize=8.5, color="#5a6378", va="center")
ax.set_xticks(x, [f"{mo} months" for mo in MONTHS])
ax.set_ylabel("net bridge mass penalty [t]\n(tankage + plant + boil-off; reactants credited as propellant)")
ax.set_title("H2/O2 fuel-cell energy bank: Saturn-ops hotel bridge, net of the water credit")
ax.grid(True, axis="y", alpha=0.25)
ax.legend(fontsize=9)
fig.tight_layout()
fig.savefig(RESULTS / "h2o2_bridge.png", dpi=160)

fig2, ax2 = plt.subplots(figsize=(9, 5))
ax2.plot(list(ratios.keys()), list(ratios.values()), "o-", color="#256abf")
ax2.axhline(1.0, color="#26251f", lw=1)
ax2.axhline(3.0, color="#b53332", ls=":", lw=1.2)
ax2.text(610, 3.12, "H1 bound: direct burn wins by ≥3×", fontsize=8.5, color="#b53332")
ax2.set_xlabel("water-thruster specific impulse [s]")
ax2.set_ylabel("impulse per kg of H2/O2:\ndirect 450 s burn ÷ via fuel-cell electricity")
ax2.set_title("Why a chemical energy bank cannot feed electric propulsion")
ax2.grid(True, alpha=0.25)
fig2.tight_layout()
fig2.savefig(RESULTS / "energy_wall.png", dpi=160)

with open(RESULTS / "findings.json", "w") as fh:
    json.dump(findings, fh, indent=1)

for h in ["H1", "H2", "H3", "H4"]:
    print(h, "HELD" if findings[h]["held"] else "FALSIFIED")
print("H1 worst ratio:", findings["H1"]["worst_ratio"])
print("H2 worst net [t]:", findings["H2"]["worst_net_t"], "| corner:", corner)
print("H3 worst advantage:", findings["H3"]["worst_advantage"])
print("H4:", findings["H4"])
