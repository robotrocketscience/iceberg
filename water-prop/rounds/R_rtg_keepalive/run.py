#!/usr/bin/env python3
"""R-rtg-keepalive — keep-alive pricing + MMRTG suite sweep vs H1-H4.

Deterministic. Chain and constants per R174/R176; ZBO cold-tier spec per
R172 TIERS. Bank launched pre-charged (SCOPE clarification 4).
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
YEAR = 3.156e7
LHV = 13.3e6
ETA_FC = 0.55
ETA_CHG = 0.66
LILT = 1.5
VE_MET = 800.0 * G0
ZBO_W_PER_T = 1.5 * 80 / 9
ZBO_KG_PER_T = 1.5 * 50 / 9
SHIP_DRY = 20_000.0
TANK = 0.20
HOTEL_GAS = 2_600.0
DV_DEPART = 1500.0
DV_BUDGET_IN = 4200.0
BASELINE = 50.0 / 40.0
MMRTG_W, MMRTG_KG, MMRTG_PU, MMRTG_LAM = 110.0, 45.0, 4.8, 0.019

SATURN_R = 9.54
A_ELL = (1 + SATURN_R) / 2
ECC = (SATURN_R - 1) / (SATURN_R + 1)
T_FULL = A_ELL ** 1.5 * YEAR
_E = np.linspace(0, math.pi, 4000)
_M = _E - ECC * np.sin(_E)
T_GRID = _M / (2 * math.pi) * T_FULL
R_GRID = A_ELL * (1 - ECC * np.cos(_E))
T_TRANSFER = T_GRID[-1]
T_IN = T_GRID[-1] - T_GRID[::-1]
R_IN = R_GRID[::-1]


def avail_array(akw, r):
    return akw * 1e3 / r ** 2 / np.where(r > 3.0, LILT, 1.0)


def p_rtg(n, t_s):
    return n * MMRTG_W * np.exp(-MMRTG_LAM * t_s / YEAR)


def phase_energy(akw, n_rtg, t0_s, t_s, r, bank_t, pka, f=1.0):
    load = pka + ZBO_W_PER_T * bank_t
    arr = avail_array(akw, r) * f
    rtg = p_rtg(n_rtg, t0_s + t_s)
    short = np.clip(load - arr - rtg, 0.0, None)
    spare_rtg = np.minimum(np.clip(arr + rtg - load, 0.0, None), rtg)
    return float(np.trapezoid(short, t_s)), float(np.trapezoid(spare_rtg, t_s))


_LIT = {}


def lit_dv_proper(akw, chunk):
    if (akw, chunk) not in _LIT:
        m = R_GRID <= 4.0
        e = float(np.trapezoid(akw * 1e3 / R_GRID[m] ** 2, T_GRID[m]))
        prop = e * 0.6 / (0.5 * VE_MET ** 2)
        m1 = SHIP_DRY + chunk
        _LIT[(akw, chunk)] = VE_MET * math.log((m1 + prop) / m1)
    return _LIT[(akw, chunk)]


def kick_wet(payload, dv, n=2, eps=0.08, ve=480.0 * G0):
    m = payload
    for _ in range(n):
        r = math.exp(dv / n / ve)
        w = m * (r - 1) / (1 - eps * r)
        m += w
    return m - payload


def chain(chunk, akw, ve_gas, dv_cap, dv_ops, pka, n_rtg, t_ops_yr, f_ops,
          keepalive=True):
    lit = lit_dv_proper(akw, chunk)
    t_ops = np.linspace(0.0, t_ops_yr * YEAR, 400)
    r_ops = np.full_like(t_ops, SATURN_R)
    rtg_m = n_rtg * MMRTG_KG
    in_mask = R_IN > 4.0                      # lit-thrust overlap excluded
    bank = 40_000.0
    g_out = g_ka_ops = g_ka_in = trickle = 0.0
    for _ in range(200):
        if keepalive:
            e_out, _ = phase_energy(akw, n_rtg, 0.0, T_GRID, R_GRID,
                                    bank / 1000, pka)
            g_out = e_out / (LHV * ETA_FC)
        rem = bank - g_out
        m_cap = SHIP_DRY + rtg_m + max(rem, 0) * (1 + TANK)
        g_cap = m_cap * (1 - math.exp(-dv_cap / ve_gas))
        rem -= g_cap
        m_ops = SHIP_DRY + rtg_m + max(rem, 0) * (1 + TANK)
        g_ops = m_ops * (1 - math.exp(-dv_ops / ve_gas))
        rem -= g_ops + HOTEL_GAS
        if keepalive:
            e_ops, sp_ops = phase_energy(akw, n_rtg, T_TRANSFER, t_ops, r_ops,
                                         max(rem, 0) / 1000, pka, f_ops)
            g_ka_ops = e_ops / (LHV * ETA_FC)
            rem -= g_ka_ops
        m_dep = SHIP_DRY + rtg_m + chunk + max(rem, 0) * (1 + TANK)
        g_dep = m_dep * (1 - math.exp(-DV_DEPART / ve_gas))
        rem -= g_dep
        if keepalive:
            bank_in = np.linspace(max(rem, 0), 0.0, len(T_IN)) / 1000
            e_in, sp_in = phase_energy(akw, n_rtg,
                                       T_TRANSFER + t_ops_yr * YEAR,
                                       T_IN[in_mask], R_IN[in_mask],
                                       bank_in[in_mask], pka)
            g_ka_in = e_in / (LHV * ETA_FC)
            rem -= g_ka_in
        need = max(DV_BUDGET_IN - DV_DEPART - lit, 0.0)
        m_mid = SHIP_DRY + rtg_m + chunk + max(rem, 0) * (1 + TANK)
        g_res = m_mid * (1 - math.exp(-need / ve_gas))
        if keepalive and n_rtg > 0:
            g_tr = (sp_ops + sp_in) * ETA_CHG / LHV
            trickle = min(g_tr, g_res + g_ka_in)   # post-departure demand only
            rem += trickle
        shortfall = g_res - rem
        bank += shortfall * 0.7
        if abs(shortfall) < 5:
            break
    ka_gas = g_out + g_ka_ops + g_ka_in
    stack = (SHIP_DRY + rtg_m + bank * (1 + TANK)
             + bank / 1000 * ZBO_KG_PER_T + akw * 1000 / 120.0)
    launch = (stack + kick_wet(stack, 7300.0)) / 1000.0
    delivered = (chunk - trickle) / 1000.0
    return {"bank_t": round(bank / 1000, 1), "ka_gas_t": round(ka_gas / 1000, 2),
            "trickle_t": round(trickle / 1000, 2), "launch_t": round(launch, 0),
            "ratio": round((launch / delivered) / BASELINE, 2),
            "ka_parts_t": [round(x / 1000, 2) for x in (g_out, g_ka_ops, g_ka_in)]}


CANON = dict(chunk=40_000.0, akw=100.0, ve_gas=450 * G0, dv_cap=1000.0,
             dv_ops=500.0, pka=300.0, t_ops_yr=1.5, f_ops=1.0)
BEST176 = dict(chunk=80_000.0, akw=300.0, ve_gas=480 * G0, dv_cap=600.0,
               dv_ops=300.0, pka=300.0, t_ops_yr=1.5, f_ops=1.0)

# --- sweep ---
rows = []
for chunk in (40_000.0, 80_000.0):
    for akw in (100.0, 200.0, 300.0):
        for relief, (dv_cap, dv_ops) in {"nominal": (1000.0, 500.0),
                                          "moon-tour": (600.0, 300.0)}.items():
            for isp in (450.0, 480.0):
                for pka in (150.0, 300.0, 600.0):
                    for t_ops in (1.0, 1.5, 2.0):
                        for f_ops in (1.0, 0.5):
                            for n in (0, 2, 4, 5, 6, 8):
                                c = chain(chunk, akw, isp * G0, dv_cap, dv_ops,
                                          pka, n, t_ops, f_ops)
                                c.update({"chunk_t": chunk / 1000, "array_kW": akw,
                                          "relief": relief, "isp": isp, "pka_We": pka,
                                          "t_ops_yr": t_ops, "f_ops": f_ops, "n_rtg": n})
                                rows.append(c)

# --- H1: canonical, keep-alive ON vs OFF, N=0 ---
c_off = chain(**CANON, n_rtg=0, keepalive=False)
c_on = chain(**CANON, n_rtg=0)
ka_ratio = c_on["ka_gas_t"] * 1000 / HOTEL_GAS
d_launch = c_on["launch_t"] - c_off["launch_t"]
h1 = (85.0 <= c_on["bank_t"] <= 98.0 and 3.0 <= ka_ratio <= 5.5
      and 60.0 <= d_launch <= 100.0)
findings = {"H1": {"bank_off_t": c_off["bank_t"], "bank_on_t": c_on["bank_t"],
                   "ka_gas_t": c_on["ka_gas_t"], "ka_over_hotel": round(ka_ratio, 1),
                   "ka_parts_t": c_on["ka_parts_t"], "delta_launch_t": d_launch,
                   "held": bool(h1)}}

# --- H2: 300 kW / f_ops=1.0 corners self-cover; R176 headline shift ---
cells_300 = [r for r in rows if r["array_kW"] == 300 and r["f_ops"] == 1.0
             and r["n_rtg"] == 0]
worst_300 = max(cells_300, key=lambda r: r["ka_gas_t"])
b_off = chain(**BEST176, n_rtg=0, keepalive=False)
b_on = chain(**BEST176, n_rtg=0)
shift = b_on["launch_t"] / b_off["launch_t"] - 1
h2 = worst_300["ka_gas_t"] <= 1.5 and abs(shift) <= 0.02
findings["H2"] = {"worst_300kW_ka_gas_t": worst_300["ka_gas_t"],
                  "worst_300kW_cell": {k: worst_300[k] for k in
                                       ("chunk_t", "relief", "isp", "pka_We",
                                        "t_ops_yr")},
                  "best176_launch_shift": round(shift, 4), "held": bool(h2)}

# --- H3: N* scan at canonical ---
e_ref = c_on["ka_gas_t"]
scan = {}
nstar = None
for n in range(1, 11):
    cn = chain(**CANON, n_rtg=n)
    cov = 1 - cn["ka_gas_t"] / e_ref
    scan[n] = {"bank_t": cn["bank_t"], "coverage": round(cov, 2),
               "launch_t": cn["launch_t"],
               "saving_t": round(c_on["launch_t"] - cn["launch_t"], 0),
               "pu_kg": round(n * MMRTG_PU, 1), "trickle_t": cn["trickle_t"]}
    if nstar is None and cov >= 0.90:
        nstar = n
n_opt = min(scan, key=lambda n: scan[n]["launch_t"])
interior = scan[8]["launch_t"] > scan[n_opt]["launch_t"]
h3 = (nstar is not None and 4 <= nstar <= 6 and nstar * MMRTG_PU <= 32.7
      and 55.0 <= scan[nstar]["saving_t"] <= 90.0 and interior)
findings["H3"] = {"n_star": nstar, "n_star_pu_kg": round(nstar * MMRTG_PU, 1),
                  "n_star_saving_t": scan[nstar]["saving_t"], "n_opt": n_opt,
                  "interior_optimum": bool(interior), "scan": scan, "held": bool(h3)}

# --- H4: trickle band at N*; bulk reductio ---
tr = scan[nstar]["trickle_t"]
e_bank = c_on["bank_t"] * 1000 * LHV / ETA_CHG
n_bulk = e_bank / (MMRTG_W * 0.85 * (T_TRANSFER + (1.5 + 5.43) * YEAR))
h4 = 3.0 <= tr <= 6.0 and n_bulk >= 40.0
findings["H4"] = {"trickle_at_nstar_t": tr, "conversational_claim_le_2t": False,
                  "bulk_reductio_mmrtg": round(n_bulk, 0), "held": bool(h4)}

# --- figure ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 5.2))
bank_c = c_on["bank_t"]
t_mission, p_arr, p_load = [], [], []
segs = [(T_GRID, R_GRID, bank_c, 0.0),
        (T_TRANSFER + np.linspace(0, 1.5 * YEAR, 200),
         np.full(200, SATURN_R), bank_c * 0.55, T_TRANSFER),
        (T_TRANSFER + 1.5 * YEAR + T_IN, R_IN, bank_c * 0.15, 0.0)]
for t, r, b, _ in segs:
    t_mission.append(t / YEAR)
    p_arr.append(avail_array(100.0, r))
    p_load.append(300.0 + ZBO_W_PER_T * b * np.ones_like(t))
t_m = np.concatenate(t_mission)
p_a = np.concatenate(p_arr)
p_l = np.concatenate(p_load)
p_r = p_rtg(nstar, t_m * YEAR)
ax1.plot(t_m, p_l, color="#26251f", lw=1.8, label="keep-alive load (bus + ZBO)")
ax1.plot(t_m, p_a, color="#eda100", lw=1.8, label="array (100 kW-rated, LILT)")
ax1.plot(t_m, p_a + p_r, color="#256abf", lw=1.8,
         label=f"array + {nstar} MMRTG (decaying)")
ax1.fill_between(t_m, p_a, p_l, where=p_l > p_a, color="#e34948", alpha=0.35,
                 label="shortfall: burned from the bank")
ax1.set_ylim(0, 3200)
ax1.set_xlabel("mission time [yr]")
ax1.set_ylabel("electric power [We]")
ax1.set_title("Canonical corner: where the dark keep-alive gap lives")
ax1.legend(fontsize=8.5, loc="upper center")
ax1.grid(True, alpha=0.25)

ns = [0, 2, 4, 5, 6, 8]
l_canon = [c_on["launch_t"] if n == 0 else scan[n]["launch_t"] for n in ns]
l_300 = [next(r["launch_t"] for r in rows if r["n_rtg"] == n
              and r["chunk_t"] == 80 and r["array_kW"] == 300
              and r["relief"] == "moon-tour" and r["isp"] == 480
              and r["pka_We"] == 300 and r["t_ops_yr"] == 1.5
              and r["f_ops"] == 1.0) for n in ns]
ax2.plot(ns, l_canon, "o-", color="#e34948", lw=1.8,
         label="canonical corner (100 kW array)")
ax2.plot(ns, l_300, "s-", color="#256abf", lw=1.8,
         label="R176 best corner (300 kW array)")
ax2.annotate("~19 t launch saved per MMRTG\n(trickle regeneration; cap ~N=11)",
             (5, scan[5]["launch_t"]), textcoords="offset points",
             xytext=(10, 16), fontsize=8.5, color="#e34948")
ax2.annotate("array already covers keep-alive:\nRTG is pure dead mass here",
             (4, l_300[2]), textcoords="offset points", xytext=(6, -26),
             fontsize=8.5, color="#256abf")
ax2.set_xlabel("MMRTG suite size")
ax2.set_ylabel("launch mass [t] (2-stage kick)")
ax2.set_title("What the RTG suite buys, by corner")
ax2.grid(True, alpha=0.25)
ax2.legend(fontsize=8.5)
fig.tight_layout()
fig.savefig(RESULTS / "rtg_keepalive.png", dpi=160)

with open(RESULTS / "findings.json", "w") as fh:
    json.dump({"findings": findings, "sweep": rows}, fh, indent=1, default=float)

for h in ("H1", "H2", "H3", "H4"):
    print(h, "HELD" if findings[h]["held"] else "FALSIFIED")
print("H1:", {k: findings["H1"][k] for k in ("bank_on_t", "ka_over_hotel", "delta_launch_t")})
print("H2 worst 300 kW cell:", worst_300["ka_gas_t"], "t | shift:", round(shift, 4))
print("H3 N*:", nstar, "| opt:", n_opt, "| saving:", scan[nstar]["saving_t"], "t")
print("H4 trickle:", tr, "t | bulk reductio:", round(n_bulk), "MMRTGs")
