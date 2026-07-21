#!/usr/bin/env python3
"""R-array-spare-regeneration — spare-watt allocation sweep vs H1-H4.

Deterministic. Chain per R177 + three spare-watt mechanisms per SCOPE.
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
ETA_THR = 0.6
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
MMRTG_W, MMRTG_KG, MMRTG_LAM = 110.0, 45.0, 0.019

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
IN_MASK = R_IN > 4.0


def avail_array(akw, r):
    return akw * 1e3 / r ** 2 / np.where(r > 3.0, LILT, 1.0)


def p_rtg(n, t_s):
    return n * MMRTG_W * np.exp(-MMRTG_LAM * t_s / YEAR)


def phase_energy(akw, n_rtg, t0_s, t_s, r, bank_t, pka, f=1.0):
    load = pka + ZBO_W_PER_T * bank_t
    arr = avail_array(akw, r) * f
    rtg = p_rtg(n_rtg, t0_s + t_s)
    short = np.clip(load - arr - rtg, 0.0, None)
    spare = np.clip(arr + rtg - load, 0.0, None)
    sp_rtg = np.minimum(spare, rtg)
    return (float(np.trapezoid(short, t_s)), float(np.trapezoid(sp_rtg, t_s)),
            float(np.trapezoid(spare - sp_rtg, t_s)))


_LIT = {}


def lit_dv_proper(akw, chunk):
    if (akw, chunk) not in _LIT:
        m = R_GRID <= 4.0
        e = float(np.trapezoid(akw * 1e3 / R_GRID[m] ** 2, T_GRID[m]))
        prop = e * ETA_THR / (0.5 * VE_MET ** 2)
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
          mode="regen", phi=1.0):
    lit = lit_dv_proper(akw, chunk)
    t_ops = np.linspace(0.0, t_ops_yr * YEAR, 400)
    r_ops = np.full_like(t_ops, SATURN_R)
    rtg_m = n_rtg * MMRTG_KG
    use_ops = mode in ("rtg", "regen", "mix")
    use_in = mode in ("rtg", "regen", "mix")
    use_ep = mode in ("ep", "mix")
    bank = 40_000.0
    credit_ops = credit_in = prop_ep = dv_dark = 0.0
    for _ in range(200):
        e_out, _, _ = phase_energy(akw, n_rtg, 0.0, T_GRID, R_GRID,
                                   bank / 1000, pka)
        g_out = e_out / (LHV * ETA_FC)
        rem = bank - g_out
        m_cap = SHIP_DRY + rtg_m + max(rem, 0) * (1 + TANK)
        g_cap = m_cap * (1 - math.exp(-dv_cap / ve_gas))
        rem -= g_cap
        m_ops = SHIP_DRY + rtg_m + max(rem, 0) * (1 + TANK)
        g_ops = m_ops * (1 - math.exp(-dv_ops / ve_gas))
        rem -= g_ops + HOTEL_GAS
        e_ko, sr_o, sa_o = phase_energy(akw, n_rtg, T_TRANSFER, t_ops, r_ops,
                                        max(rem, 0) / 1000, pka, f_ops)
        rem -= e_ko / (LHV * ETA_FC)
        m_dep = SHIP_DRY + rtg_m + chunk + max(rem, 0) * (1 + TANK)
        g_dep = m_dep * (1 - math.exp(-DV_DEPART / ve_gas))
        sp_ops = (sr_o if mode == "rtg" else sr_o + sa_o) if use_ops else 0.0
        credit_ops = min(sp_ops * ETA_CHG / LHV, g_dep)
        rem += credit_ops - g_dep
        bank_in = np.linspace(max(rem, 0), 0.0, len(T_IN)) / 1000
        e_ki, sr_i, sa_i = phase_energy(akw, n_rtg,
                                        T_TRANSFER + t_ops_yr * YEAR,
                                        T_IN[IN_MASK], R_IN[IN_MASK],
                                        bank_in[IN_MASK], pka)
        g_ka_in = e_ki / (LHV * ETA_FC)
        rem -= g_ka_in
        sp_in_all = (sr_i if mode == "rtg" else sr_i + sa_i)
        m_mid = SHIP_DRY + rtg_m + chunk + max(rem, 0) * (1 + TANK)
        need_base = max(DV_BUDGET_IN - DV_DEPART - lit, 0.0)
        e_ep = 0.0
        if use_ep:
            prop_full = sp_in_all * ETA_THR / (0.5 * VE_MET ** 2)
            m1 = SHIP_DRY + rtg_m + chunk
            dv_avail = VE_MET * math.log((m1 + prop_full) / m1)
            dv_dark = min(dv_avail, need_base * (phi if mode == "mix" else 1.0))
            prop_ep = m1 * (math.exp(dv_dark / VE_MET) - 1)
            e_ep = prop_ep * 0.5 * VE_MET ** 2 / ETA_THR
        need = max(need_base - dv_dark, 0.0)
        g_res = m_mid * (1 - math.exp(-need / ve_gas))
        if use_in:
            cap = (g_res + g_ka_in) * LHV / ETA_CHG
            credit_in = min(max(sp_in_all - e_ep, 0.0), cap) * ETA_CHG / LHV
            rem += credit_in
        shortfall = g_res - rem
        bank += shortfall * 0.7
        if abs(shortfall) < 5:
            break
    stack = (SHIP_DRY + rtg_m + bank * (1 + TANK)
             + bank / 1000 * ZBO_KG_PER_T + akw * 1000 / 120.0)
    launch = (stack + kick_wet(stack, 7300.0)) / 1000.0
    delivered = (chunk - credit_ops - credit_in - prop_ep) / 1000.0
    return {"bank_t": round(bank / 1000, 1), "launch_t": round(launch, 0),
            "credit_ops_t": round(credit_ops / 1000, 2),
            "credit_in_t": round(credit_in / 1000, 2),
            "prop_ep_t": round(prop_ep / 1000, 2), "dv_dark": round(dv_dark),
            "delivered_t": round(delivered, 1),
            "ratio": round((launch / delivered) / BASELINE, 2)}


BEST = dict(chunk=80_000.0, akw=300.0, ve_gas=480 * G0, dv_cap=600.0,
            dv_ops=300.0, pka=300.0, f_ops=1.0)
CANON = dict(chunk=40_000.0, akw=100.0, ve_gas=450 * G0, dv_cap=1000.0,
             dv_ops=500.0, pka=300.0, f_ops=1.0)
MID = dict(chunk=80_000.0, akw=200.0, ve_gas=480 * G0, dv_cap=600.0,
           dv_ops=300.0, pka=300.0, f_ops=1.0)


def fine_mix(corner, n_rtg=0, t_ops_yr=1.5):
    out = None
    for i in range(21):
        r = chain(**corner, n_rtg=n_rtg, t_ops_yr=t_ops_yr, mode="mix",
                  phi=i / 20)
        if out is None or r["ratio"] < out[1]["ratio"]:
            out = (i / 20, r)
    return out


# --- sweep ---
rows = []
for chunk in (40_000.0, 80_000.0):
    for akw in (100.0, 200.0, 300.0):
        for relief, (dv_cap, dv_ops) in {"nominal": (1000.0, 500.0),
                                          "moon-tour": (600.0, 300.0)}.items():
            for isp in (450.0, 480.0):
                for pka in (150.0, 300.0, 600.0):
                    for t_ops in (1.0, 1.5, 2.0, 3.0):
                        for f_ops in (1.0, 0.5):
                            for n in (0, 4):
                                kw = dict(chunk=chunk, akw=akw,
                                          ve_gas=isp * G0, dv_cap=dv_cap,
                                          dv_ops=dv_ops, pka=pka, f_ops=f_ops)
                                modes = {m: chain(**kw, n_rtg=n,
                                                  t_ops_yr=t_ops, mode=m)
                                         for m in ("off", "regen", "ep")}
                                mixes = [chain(**kw, n_rtg=n, t_ops_yr=t_ops,
                                               mode="mix", phi=p)
                                         for p in (0.25, 0.5, 0.75)]
                                modes["mix"] = min(mixes,
                                                   key=lambda r: r["ratio"])
                                rows.append({"chunk_t": chunk / 1000,
                                             "array_kW": akw, "relief": relief,
                                             "isp": isp, "pka_We": pka,
                                             "t_ops_yr": t_ops, "f_ops": f_ops,
                                             "n_rtg": n, "modes": modes})


def cell(chunk_t, akw, relief, isp, pka, t_ops, f_ops, n):
    return next(r for r in rows if r["chunk_t"] == chunk_t
                and r["array_kW"] == akw and r["relief"] == relief
                and r["isp"] == isp and r["pka_We"] == pka
                and r["t_ops_yr"] == t_ops and r["f_ops"] == f_ops
                and r["n_rtg"] == n)


c_cell = cell(40, 100, "nominal", 450, 300, 1.5, 1.0, 0)["modes"]
m_cell = cell(80, 200, "moon-tour", 480, 300, 1.5, 1.0, 0)["modes"]
b_cell = cell(80, 300, "moon-tour", 480, 300, 1.5, 1.0, 0)["modes"]

# --- H1 ---
rtg4 = chain(**CANON, n_rtg=4, t_ops_yr=1.5, mode="rtg")
regen_n4 = chain(**CANON, n_rtg=4, t_ops_yr=1.5, mode="regen")
rtg_marginal = (c_cell["regen"]["launch_t"] - regen_n4["launch_t"]) / 4
h1 = (abs(c_cell["off"]["bank_t"] - 91.3) <= 0.5
      and abs(c_cell["off"]["launch_t"] - 767) <= 4
      and abs(rtg4["launch_t"] - 619) / 619 <= 0.015
      and 17.0 <= rtg_marginal <= 22.0)
findings = {"H1": {"off_canonical": c_cell["off"], "rtg_n4_launch_t":
                   rtg4["launch_t"], "rtg_marginal_after_regen_t":
                   round(rtg_marginal, 1), "held": bool(h1)}}

# --- H2 ---
slopes = []
prev = None
for t_ops in (1.0, 1.5, 2.0, 3.0):
    L = cell(80, 300, "moon-tour", 480, 300, t_ops, 1.0, 0)["modes"]["regen"]["launch_t"]
    if prev:
        slopes.append((prev[1] - L) / (t_ops - prev[0]))
    prev = (t_ops, L)
h2 = (495.0 <= b_cell["regen"]["launch_t"] <= 509.0
      and 5.15 <= b_cell["regen"]["ratio"] <= 5.35
      and all(26.0 <= s <= 36.0 for s in slopes))
findings["H2"] = {"best_regen": b_cell["regen"], "slopes_t_per_yr":
                  [round(s, 1) for s in slopes],
                  "hybrid_translated_headline": round(3.57 * b_cell["regen"]["launch_t"] / b_cell["off"]["launch_t"], 2),
                  "held": bool(h2)}

# --- H3 ---
rec_c = c_cell["off"]["launch_t"] - c_cell["regen"]["launch_t"]
rec_m = m_cell["off"]["launch_t"] - m_cell["regen"]["launch_t"]
h3 = 190.0 <= rec_c <= 230.0 and 130.0 <= rec_m <= 165.0
findings["H3"] = {"canonical_recovery_t": rec_c, "mid_recovery_t": rec_m,
                  "held": bool(h3)}

# --- H4 ---
ep_best_delta = b_cell["ep"]["launch_t"] - b_cell["off"]["launch_t"]
gap = c_cell["regen"]["ratio"] - c_cell["ep"]["ratio"]
probes = {}
h4c = True
for name, corner, cl in (("canonical", CANON, c_cell), ("mid", MID, m_cell),
                          ("best", BEST, b_cell)):
    phi, mx = fine_mix(corner)
    ref = min(cl["regen"]["ratio"], cl["ep"]["ratio"])
    probes[name] = {"phi": phi, "mix_ratio": mx["ratio"], "ref": ref}
    if mx["ratio"] > ref + 0.02:
        h4c = False
h4 = abs(ep_best_delta) <= 2.0 and 0.1 <= gap <= 0.4 and h4c
findings["H4"] = {"ep_best_delta_t": ep_best_delta,
                  "canonical_ratio_gap_regen_minus_ep": round(gap, 2),
                  "mix_probes": probes,
                  "session_claim_electrolysis_dominates": "falsified on ratio metric" if gap >= 0.1 else "held",
                  "held": bool(h4)}

# --- figure ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 5.2))
corners = [("canonical\n40 t / 100 kW", c_cell), ("mid\n80 t / 200 kW", m_cell),
           ("best\n80 t / 300 kW", b_cell)]
x = np.arange(3)
w = 0.26
for i, (mode, color, label) in enumerate(
        (("regen", "#256abf", "electrolysis (ops + inbound)"),
         ("ep", "#eda100", "dark-leg EP only (owner's proposal)"),
         ("mix", "#e34948", "composite (best split)"))):
    vals = [cl[mode]["ratio"] / cl["off"]["ratio"] for _, cl in corners]
    bars = ax1.bar(x + (i - 1) * w, vals, w, color=color, label=label)
    for b, (_, cl) in zip(bars, corners):
        ax1.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.008,
                 f"{cl[mode]['ratio']:.2f}", ha="center", fontsize=7.5)
ax1.axhline(1.0, color="#26251f", lw=1, ls=":")
ax1.text(0.62, 1.012, "no spare-watt use = 1.0", fontsize=8)
ax1.set_xticks(x, [n for n, _ in corners])
ax1.set_ylim(0.80, 1.10)
ax1.set_ylabel("launch-per-delivered ratio, ÷ same corner with no credits")
ax1.set_title("Who gets the spare joule, by corner")
ax1.grid(True, axis="y", alpha=0.25)
ax1.legend(fontsize=8.5, loc="upper left")

tops_grid = [1.0, 1.5, 2.0, 3.0]
L_best = [cell(80, 300, "moon-tour", 480, 300, t, 1.0, 0)["modes"]["regen"]["launch_t"]
          for t in tops_grid]
ax2.plot(tops_grid, L_best, "o-", color="#256abf", lw=1.8)
ax2.text(1.02, L_best[3] + 6,
         f"~{np.mean(slopes):.0f} t launch per added ops year\n"
         "(chunk water electrolyzed at the ring,\nserving the departure burn)",
         fontsize=8.5, va="bottom")
ax2.axvline(3.0, color="#26251f", lw=1, ls=":")
ax2.text(2.95, (L_best[0] + L_best[2]) / 2, "schedule 13.4 yr vs L0-05 15 yr",
         fontsize=8, rotation=90, va="center", ha="right")
ax2.set_xlabel("ring-ops duration [yr]")
ax2.set_ylabel("launch mass [t] (2-stage kick)")
ax2.set_title("Best corner: the ops-extension trade")
ax2.grid(True, alpha=0.25)
fig.tight_layout()
fig.savefig(RESULTS / "spare_watt_allocation.png", dpi=160)

with open(RESULTS / "findings.json", "w") as fh:
    json.dump({"findings": findings, "sweep": rows}, fh, indent=1, default=float)

for h in ("H1", "H2", "H3", "H4"):
    print(h, "HELD" if findings[h]["held"] else "FALSIFIED")
print("H1 rtg marginal:", findings["H1"]["rtg_marginal_after_regen_t"], "t/unit")
print("H2 best regen:", b_cell["regen"]["launch_t"], "t, ratio",
      b_cell["regen"]["ratio"], "| slopes:", findings["H2"]["slopes_t_per_yr"],
      "| translated:", findings["H2"]["hybrid_translated_headline"], "x")
print("H3 recovery canonical/mid:", rec_c, "/", rec_m, "t")
print("H4 ep@best:", ep_best_delta, "t | gap:", round(gap, 2),
      "| mix probes:", probes)
