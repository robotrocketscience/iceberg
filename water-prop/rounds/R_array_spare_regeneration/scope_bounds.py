#!/usr/bin/env python3
"""Pre-script: R-array-spare-regeneration bounds.

Prices ALL spare watts (array above keep-alive; RTG optional) through three
mechanisms, per owner direction (2026-07-21 mid-round message):

  (a) ops-phase regeneration: electrolyze chunk water at the ring station,
      credited against departure gas (pre-departure sink);
  (b) inbound regeneration beyond 4 AU: credited against residual +
      inbound keep-alive gas demand (post-departure sinks only);
  (c) dark-leg EP: spare watts beyond 4 AU inbound drive the MET directly
      (the owner's "run the EP on 2.2 kW" proposal), reducing residual dv.

Allocation rule (closed form): impulse per spare joule is
  electrolysis->480 s burn: (0.66/13.3e6 kg/J) * 4709 m/s = 2.34e-4 N s/J
  MET at 800 s, eta 0.6:     2*0.6/7848            = 1.53e-4 N s/J
so spare joules go to electrolysis until gas demand caps out, remainder to
the MET. Modes: off / rtg (R177 regression) / regen (a+b) / ep (c only,
the owner's proposal isolated) / full (a+b+c with allocation).

Mass ledger: regenerated gas and dark-leg MET propellant are chunk water
(debited from delivered); dark-leg propellant is carried through the
departure burn (fixing, for this new line only, the harvest-margin mass
that R173/R174 never carried; predecessor convention flagged, not
relitigated). Departure stack mass is unchanged by regeneration itself
(chunk mass moved into already-launched empty tanks). Outbound: no
feedstock, no credit. 3-4 AU inbound stays with the lit-thrust integral
(no double count).
"""
import math

import numpy as np

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
    sp_in_all = 0.0
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
            # gated EP: thrust only while dv is still owed; chunk water aboard
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
            credit_in = min(sp_in_all - e_ep, cap) * ETA_CHG / LHV
            rem += credit_in
        shortfall = g_res - rem
        bank += shortfall * 0.7
        if abs(shortfall) < 5:
            break
    stack = (SHIP_DRY + rtg_m + bank * (1 + TANK)
             + bank / 1000 * ZBO_KG_PER_T + akw * 1000 / 120.0)
    launch = (stack + kick_wet(stack, 7300.0)) / 1000.0
    delivered = (chunk - credit_ops - credit_in - prop_ep) / 1000.0
    return {"bank_t": bank / 1000, "launch_t": launch,
            "credit_ops_t": credit_ops / 1000, "credit_in_t": credit_in / 1000,
            "prop_ep_t": prop_ep / 1000, "dv_dark": dv_dark,
            "sp_in_pot_t": sp_in_all * ETA_CHG / LHV / 1000,
            "delivered_t": delivered,
            "ratio": (launch / delivered) / BASELINE}


BEST = dict(chunk=80_000.0, akw=300.0, ve_gas=480 * G0, dv_cap=600.0,
            dv_ops=300.0, pka=300.0, f_ops=1.0)
CANON = dict(chunk=40_000.0, akw=100.0, ve_gas=450 * G0, dv_cap=1000.0,
             dv_ops=500.0, pka=300.0, f_ops=1.0)
MID = dict(chunk=80_000.0, akw=200.0, ve_gas=480 * G0, dv_cap=600.0,
           dv_ops=300.0, pka=300.0, f_ops=1.0)

print("== closed-form allocation constants ==")
print(f"impulse/J electrolysis->480s: {ETA_CHG/LHV*4709:.3e}  MET: {2*ETA_THR/VE_MET:.3e}"
      f"  ratio {ETA_CHG/LHV*4709/(2*ETA_THR/VE_MET):.2f}")

print("\n== regression vs R177 ==")
c = chain(**CANON, n_rtg=0, t_ops_yr=1.5, mode="off")
print(f"canonical N=0 off: bank {c['bank_t']:.1f} (91.3) launch {c['launch_t']:.0f} (767)")
c4 = chain(**CANON, n_rtg=4, t_ops_yr=1.5, mode="rtg")
print(f"canonical N=4 rtg: bank {c4['bank_t']:.1f} (70.2) launch {c4['launch_t']:.0f} (619)")

for name, corner in (("BEST 300kW", BEST), ("MID 200kW", MID), ("CANON 100kW", CANON)):
    print(f"\n== {name} ==")
    base = chain(**corner, n_rtg=0, t_ops_yr=1.5, mode="off")
    for mode in ("regen", "ep"):
        r = chain(**corner, n_rtg=0, t_ops_yr=1.5, mode=mode)
        print(f"  {mode:5s}: launch {base['launch_t']:.0f}->{r['launch_t']:.0f} "
              f"({r['launch_t']-base['launch_t']:+.0f} t) | credits ops "
              f"{r['credit_ops_t']:.1f} in {r['credit_in_t']:.1f} | EP "
              f"{r['prop_ep_t']:.1f} t / {r['dv_dark']:.0f} m/s | "
              f"ratio {base['ratio']:.2f}->{r['ratio']:.2f} | "
              f"delivered {r['delivered_t']:.1f}")

print("\n== RTG marginal AFTER array regen (revises R177 H3) ==")
cr0 = chain(**CANON, n_rtg=0, t_ops_yr=1.5, mode="regen")
cr4 = chain(**CANON, n_rtg=4, t_ops_yr=1.5, mode="regen")
print(f"canonical: N=0 regen {cr0['launch_t']:.0f} t -> N=4 regen {cr4['launch_t']:.0f} t "
      f"({(cr0['launch_t']-cr4['launch_t'])/4:.1f} t per MMRTG; R177 said ~19)")

print("\n== T_ops slope at best corner (mode regen) ==")
prev = None
for tops in (1.0, 1.5, 2.0, 3.0):
    b = chain(**BEST, n_rtg=0, t_ops_yr=tops, mode="regen")
    s = f", slope {(prev['launch_t']-b['launch_t'])/ (tops-prev['t']):.0f} t/yr" if prev else ""
    print(f"  T_ops {tops}: launch {b['launch_t']:.0f} t, ops credit "
          f"{b['credit_ops_t']:.1f} t{s}")
    prev = {"launch_t": b["launch_t"], "t": tops}
print("schedule: 11.93 - 1.5 + 3.0 = 13.4 yr vs L0-05 15 yr")

print("\n== RTG stacking at best corner (N=4 regen vs N=0 regen) ==")
b0 = chain(**BEST, n_rtg=0, t_ops_yr=1.5, mode="regen")
b4 = chain(**BEST, n_rtg=4, t_ops_yr=1.5, mode="regen")
print(f"  launch {b0['launch_t']:.0f} -> {b4['launch_t']:.0f} ({b4['launch_t']-b0['launch_t']:+.0f} t)")

print("\n== mixed allocation (phi = share of residual dv retired by EP) ==")
for name, corner in (("CANON 100kW", CANON), ("MID 200kW", MID)):
    best_mix = None
    for i in range(21):
        phi = i / 20
        r = chain(**corner, n_rtg=0, t_ops_yr=1.5, mode="mix", phi=phi)
        if best_mix is None or r["ratio"] < best_mix[1]["ratio"]:
            best_mix = (phi, r)
    phi, r = best_mix
    print(f"  {name}: best phi {phi:.2f} -> launch {r['launch_t']:.0f} t, "
          f"ratio {r['ratio']:.2f}, delivered {r['delivered_t']:.1f} t "
          f"(EP {r['prop_ep_t']:.1f} t / {r['dv_dark']:.0f} m/s, regen in "
          f"{r['credit_in_t']:.1f} t)")
