#!/usr/bin/env python3
"""R-regenerative-solar-electrolysis-bank — solar-charged H2/O2 bank vs H1-H5.

Kepler harvest integral on the Hohmann transfer, zero-boil-off ledger at two
insulation tiers, mass rollup against comparators. Deterministic.
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

# --- constants / chain parameters (SCOPE) ---
LHV = 13.3e6            # J/kg stoich mix
ETA_CHG = 0.66          # electrolyzer electric -> chemical
ETA_FC = 0.55           # chemical -> electric
ARRAY_W_PER_KG_1AU = 120.0
ELEC_KW_PER_KG = 1.0
FC_W_PER_KG = 100.0
TANK_FRAC = 0.20
BATT_J_PER_KG = 250 * 3600.0
LILT_DERATE = 1.5
SATURN_R = 9.54         # AU
A_HOHMANN = (1 + SATURN_R) / 2
E_HOHMANN = (SATURN_R - 1) / (SATURN_R + 1)
T_HOHMANN_YR = A_HOHMANN ** 1.5          # full-period years; transfer = half
YEAR_S = 3.156e7
CHARGE_R_MAX = 3.0

# ZBO tiers: (heat leak W per tonne LH2, cooler input W per W lifted, cooler kg per W lifted)
TIERS = {"warm": (10.0, 150.0, 30.0), "cold": (1.5, 80.0, 50.0)}
LH2_FRAC = 1.0 / 9.0

DUTIES = [(p, mo) for p in (5.0, 10.0, 15.0) for mo in (2, 4, 6)]
BURSTS = [(p, d) for p in (50.0, 100.0) for d in (1, 3)]


def kepler_t_of_r(r_au):
    """Time (s) from perihelion to radius r on the transfer ellipse."""
    cosE = (1 - r_au / A_HOHMANN) / E_HOHMANN
    E = math.acos(max(-1.0, min(1.0, cosE)))
    M = E - E_HOHMANN * math.sin(E)
    return M / (2 * math.pi) * T_HOHMANN_YR * YEAR_S


def r_of_t_grid(n=4000):
    """(t, r) samples over the full transfer via eccentric-anomaly sweep."""
    E = np.linspace(0, math.pi, n)
    M = E - E_HOHMANN * np.sin(E)
    t = M / (2 * math.pi) * T_HOHMANN_YR * YEAR_S
    r = A_HOHMANN * (1 - E_HOHMANN * np.cos(E))
    return t, r


T_CHARGE = kepler_t_of_r(CHARGE_R_MAX)
T_CRUISE_TOTAL = T_HOHMANN_YR * YEAR_S / 2
T_DARK = T_CRUISE_TOTAL - T_CHARGE

t_grid, r_grid = r_of_t_grid()
# mean 1/r^2 over the charge window (time-weighted)
mask = t_grid <= T_CHARGE
inv_r2_mean_charge = float(np.trapezoid(1.0 / r_grid[mask] ** 2, t_grid[mask]) / T_CHARGE)

findings = {}

# --- per-duty sizing ---
rows = {}
for p_kwe, mo in DUTIES:
    e_dis = p_kwe * 1000.0 * mo * 30 * 86400.0          # J electric at Saturn
    e_chem = e_dis / ETA_FC
    reactants = e_chem / LHV                             # kg cycled
    lh2 = reactants * LH2_FRAC
    e_charge = e_chem / ETA_CHG
    p_array_1au = e_charge / (T_CHARGE * inv_r2_mean_charge)   # W rating at 1 AU
    m_array = p_array_1au / ARRAY_W_PER_KG_1AU
    m_elec = p_array_1au / 1000.0 / ELEC_KW_PER_KG
    m_fc = p_kwe * 1000.0 / FC_W_PER_KG
    m_tank = reactants * TANK_FRAC

    tier_out = {}
    for tier, (leak_w_per_t, w_in_per_w, kg_per_w) in TIERS.items():
        lift = lh2 / 1000.0 * leak_w_per_t               # W lifted
        p_zbo = lift * w_in_per_w                        # We continuous
        # array supplies ZBO where P_array(r) >= p_zbo; integrate shortfall
        dark = t_grid > T_CHARGE
        p_avail = p_array_1au / r_grid[dark] ** 2
        short = np.clip(p_zbo - p_avail, 0.0, None)
        e_short = float(np.trapezoid(short, t_grid[dark]))     # J electric from bank
        drain_chem = e_short / ETA_FC
        drain_frac = drain_chem / e_chem
        m_cooler = lift * kg_per_w
        tier_out[tier] = {
            "p_zbo_We": round(p_zbo, 1),
            "zbo_cruise_electric_GJ": round(p_zbo * T_DARK / 1e9, 2),
            "bank_chem_GJ": round(e_chem / 1e9, 2),
            "self_consumption_ratio": round(p_zbo * T_DARK / e_chem, 2),
            "drain_frac_arraysupplied": round(drain_frac, 4),
            "m_cooler_kg": round(m_cooler, 1),
        }

    m_total_cold = (m_tank + m_fc + m_array + m_elec
                    + tier_out["cold"]["m_cooler_kg"]) / 1000.0   # t
    # comparators
    m_solar_direct = p_kwe * 1000.0 / (ARRAY_W_PER_KG_1AU / SATURN_R**2 / LILT_DERATE) / 1000.0
    rows[f"{p_kwe:g}kWe_{mo}mo"] = {
        "e_dis_GJ": round(e_dis / 1e9, 1), "reactants_t": round(reactants / 1000, 2),
        "p_array_1au_kW": round(p_array_1au / 1000, 1),
        "m_array_t": round(m_array / 1000, 3),
        "m_total_cold_t": round(m_total_cold, 2),
        "m_solar_direct_t": round(m_solar_direct, 2),
        "tiers": tier_out,
    }

# --- H1 ---
worst = rows["15kWe_6mo"]
h1_mass = worst["m_array_t"] + worst["p_array_1au_kW"] / ELEC_KW_PER_KG / 1000.0
findings["H1"] = {"worst_p_array_kW": worst["p_array_1au_kW"],
                  "worst_array_plus_elec_t": round(h1_mass, 3),
                  "held": bool(worst["p_array_1au_kW"] <= 60.0 and h1_mass <= 1.0)}

# --- H2a / H2b ---
h2a_min_ratio = min(r["tiers"]["warm"]["self_consumption_ratio"] for r in rows.values())
h2b_max_drain = max(r["tiers"]["cold"]["drain_frac_arraysupplied"] for r in rows.values())
findings["H2a"] = {"min_self_consumption_ratio": h2a_min_ratio, "held": bool(h2a_min_ratio >= 1.5)}
findings["H2b"] = {"max_drain_frac": h2b_max_drain, "held": bool(h2b_max_drain <= 0.05)}

# --- H3 ---
h3a_ok = all(r["m_solar_direct_t"] / r["m_total_cold_t"] >= 2.0 for r in rows.values())
h3b_ok = True
for r in rows.values():
    if r["e_dis_GJ"] <= 100 and r["m_total_cold_t"] > 3.0:
        h3b_ok = False
    if r["e_dis_GJ"] > 140 and r["m_total_cold_t"] <= 3.0:
        h3b_ok = False
findings["H3"] = {
    "ratios_solar_over_regen": {k: round(v["m_solar_direct_t"] / v["m_total_cold_t"], 2)
                                 for k, v in rows.items()},
    "held": bool(h3a_ok and h3b_ok)}

# --- H4: bursts ---
burst_out = {}
h4_ok = True
for p_kwe, days in BURSTS:
    e = p_kwe * 1000.0 * days * 86400.0
    reactants = e / ETA_FC / LHV
    m_bank = reactants * TANK_FRAC + p_kwe * 1000.0 / FC_W_PER_KG \
        + reactants * LH2_FRAC / 1000.0 * TIERS["cold"][0] * TIERS["cold"][2]
    m_batt = e / BATT_J_PER_KG
    m_solar = p_kwe * 1000.0 / (ARRAY_W_PER_KG_1AU / SATURN_R**2 / LILT_DERATE)
    burst_out[f"{p_kwe:g}kWe_{days}d"] = {
        "bank_t": round(m_bank / 1000, 2), "batt_t": round(m_batt / 1000, 2),
        "solar_t": round(m_solar / 1000, 2),
        "adv_batt": round(m_batt / m_bank, 1), "adv_solar": round(m_solar / m_bank, 1)}
    if m_batt / m_bank < 5.0 or m_solar / m_bank < 10.0:
        h4_ok = False
findings["H4"] = {"cases": burst_out, "held": bool(h4_ok)}
findings["H5"] = {"note": "closure unchanged by citation of round 171 H4 (0 of 1,061 closing paths avoid electric legs)", "held": True}
findings["charge_window"] = {"t_charge_yr": round(T_CHARGE / YEAR_S, 2),
                             "mean_inv_r2": round(inv_r2_mean_charge, 3)}

# --- figures ---
fig, ax = plt.subplots(figsize=(9.5, 5.5))
keys = list(rows)
x = np.arange(len(keys))
ax.bar(x - 0.2, [rows[k]["m_total_cold_t"] for k in keys], 0.4,
       color="#256abf", label="regenerative bank (cold-tier cryo)")
ax.bar(x + 0.2, [rows[k]["m_solar_direct_t"] for k in keys], 0.4,
       color="#eda100", label="direct Saturn solar (LILT ×1.5)")
ax.axhspan(1.5, 3.0, color="#cbd2dc", alpha=0.5, zorder=0)
ax.text(0.05, 2.6, "Kilopower band", fontsize=8.5, color="#5a6378")
ax.set_xticks(x, keys, rotation=30, ha="right", fontsize=8)
ax.set_ylabel("system mass [t] (water cycled, credited as propellant)")
ax.set_title("Regenerative solar-electrolysis bank vs direct Saturn solar, by Saturn-ops duty")
ax.grid(True, axis="y", alpha=0.25)
ax.legend(fontsize=9)
fig.tight_layout()
fig.savefig(RESULTS / "regen_bank_mass.png", dpi=160)

fig2, ax2 = plt.subplots(figsize=(9.5, 5))
ratios_w = [rows[k]["tiers"]["warm"]["self_consumption_ratio"] for k in keys]
drains_c = [rows[k]["tiers"]["cold"]["drain_frac_arraysupplied"] * 100 for k in keys]
ax2.bar(x - 0.2, ratios_w, 0.4, color="#e34948",
        label="warm tier: cruise ZBO energy ÷ bank inventory")
ax2.bar(x + 0.2, drains_c, 0.4, color="#256abf",
        label="cold tier: bank self-drain [%] (array carries the rest)")
ax2.axhline(1.0, color="#26251f", lw=1, ls=":")
ax2.text(len(keys) - 2.4, 1.08, "bank fully consumed", fontsize=8.5, color="#26251f")
ax2.set_xticks(x, keys, rotation=30, ha="right", fontsize=8)
ax2.set_ylabel("ratio  /  percent")
ax2.set_title("The cryocooler ledger: warm-tier insulation eats the bank; cold-tier survives")
ax2.grid(True, axis="y", alpha=0.25)
ax2.legend(fontsize=9)
fig2.tight_layout()
fig2.savefig(RESULTS / "zbo_ledger.png", dpi=160)

findings["duties"] = rows
with open(RESULTS / "findings.json", "w") as fh:
    json.dump(findings, fh, indent=1)

for h in ["H1", "H2a", "H2b", "H3", "H4"]:
    print(h, "HELD" if findings[h]["held"] else "FALSIFIED")
print("charge window [yr]:", findings["charge_window"]["t_charge_yr"],
      "| mean 1/r^2:", findings["charge_window"]["mean_inv_r2"])
print("worst array [kW @1AU]:", worst["p_array_1au_kW"])
print("H2a min ratio:", h2a_min_ratio, "| H2b max drain:", h2b_max_drain)
print("mass rows:", {k: (rows[k]['m_total_cold_t'], rows[k]['m_solar_direct_t']) for k in ('5kWe_2mo', '15kWe_6mo')})
print("bursts:", burst_out)
