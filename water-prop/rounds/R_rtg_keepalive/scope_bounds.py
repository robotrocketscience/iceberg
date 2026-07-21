#!/usr/bin/env python3
"""Pre-script: R-rtg-keepalive bounds.

Prices the dark keep-alive load (bus baseload + cold-tier ZBO cryocooler
input power) that R174's round-trip chain never charged, tests whether the
variant's own solar array already covers it, and sizes the MMRTG suite that
retires the shortfall. Prints every number the SCOPE registers.

ZBO semantics per R172 TIERS (cold): 1.5 W heat leak per tonne LH2,
80 We cryocooler input per W lifted, LH2 = gas/9 ->
  P_zbo = 1.5 * 80 / 9 = 13.33 We per tonne of banked gas.
Array in the dark: P = rating/r^2 / 1.5 LILT derate beyond 3 AU (R172's
Saturn-direct treatment); the bank is launched pre-charged (ground
electrolysis) -- made explicit here because R174 never checked en-route
charge feasibility and its canonical bank exceeds the outbound window.
"""
import math

import numpy as np

G0 = 9.80665
YEAR = 3.156e7
LHV = 13.3e6
ETA_FC = 0.55
ETA_CHG = 0.66
LILT = 1.5
VE_MET = 800.0 * G0
ZBO_W_PER_T = 1.5 * 80 / 9          # We input per tonne of banked gas
ZBO_KG_PER_T = 1.5 * 50 / 9
SHIP_DRY = 20_000.0
TANK = 0.20
HOTEL_GAS = 2_600.0                 # R171 active-ops duty line, unchanged
DV_DEPART = 1500.0
DV_BUDGET_IN = 4200.0
BASELINE = 50.0 / 40.0
MMRTG_W, MMRTG_KG, MMRTG_PU, MMRTG_LAM = 110.0, 45.0, 4.8, 0.019
T_OPS_YR = 1.5

SATURN_R = 9.54
A_ELL = (1 + SATURN_R) / 2
ECC = (SATURN_R - 1) / (SATURN_R + 1)
T_FULL = A_ELL ** 1.5 * YEAR
_E = np.linspace(0, math.pi, 4000)
_M = _E - ECC * np.sin(_E)
T_GRID = _M / (2 * math.pi) * T_FULL          # perihelion -> aphelion
R_GRID = A_ELL * (1 - ECC * np.cos(_E))
T_TRANSFER = T_GRID[-1]                       # 6.05 yr


def avail_array(akw, r):
    d = np.where(r > 3.0, LILT, 1.0)
    return akw * 1e3 / r ** 2 / d


def p_rtg(n, t_s):
    return n * MMRTG_W * np.exp(-MMRTG_LAM * t_s / YEAR)


def phase_energy(akw, n_rtg, t0_s, t_s, r, bank_t, pka, f=1.0):
    """Shortfall + RTG-spare electric energy [J] over one phase."""
    load = pka + ZBO_W_PER_T * bank_t
    arr = avail_array(akw, r) * f
    rtg = p_rtg(n_rtg, t0_s + t_s)
    short = np.clip(load - arr - rtg, 0.0, None)
    spare = np.clip(arr + rtg - load, 0.0, None)
    spare_rtg = np.minimum(spare, rtg)
    return float(np.trapezoid(short, t_s)), float(np.trapezoid(spare_rtg, t_s))


def lit_dv_proper(akw, chunk):
    m = R_GRID <= 4.0
    e = float(np.trapezoid(akw * 1e3 / R_GRID[m] ** 2, T_GRID[m]))
    prop = e * 0.6 / (0.5 * VE_MET ** 2)
    m1 = SHIP_DRY + chunk
    return VE_MET * math.log((m1 + prop) / m1)


def kick_wet(payload, dv, n=2, eps=0.08, ve=480.0 * G0):
    m = payload
    for _ in range(n):
        r = math.exp(dv / n / ve)
        w = m * (r - 1) / (1 - eps * r)
        m += w
    return m - payload


def chain(chunk, akw, ve_gas, dv_cap, dv_ops, pka, n_rtg, keepalive=True):
    """R174 chain + phased keep-alive draws. Returns bank, diagnostics."""
    lit = lit_dv_proper(akw, chunk)
    t_ops = np.linspace(0.0, T_OPS_YR * YEAR, 400)
    rtg_m = n_rtg * MMRTG_KG
    bank = 40_000.0
    out = {}
    for _ in range(200):
        if keepalive:
            e_out, _ = phase_energy(akw, n_rtg, 0.0, T_GRID, R_GRID,
                                    bank / 1000, pka)
            g_out = e_out / (LHV * ETA_FC)
        else:
            g_out = 0.0
        rem = bank - g_out
        m_cap = SHIP_DRY + rtg_m + max(rem, 0) * (1 + TANK)
        g_cap = m_cap * (1 - math.exp(-dv_cap / ve_gas))
        rem -= g_cap
        m_ops = SHIP_DRY + rtg_m + max(rem, 0) * (1 + TANK)
        g_ops = m_ops * (1 - math.exp(-dv_ops / ve_gas))
        rem -= g_ops + HOTEL_GAS
        if keepalive:
            e_ops, _ = phase_energy(akw, n_rtg, T_TRANSFER, t_ops,
                                    np.full_like(t_ops, SATURN_R),
                                    max(rem, 0) / 1000, pka)
            g_ka_ops = e_ops / (LHV * ETA_FC)
            rem -= g_ka_ops
        m_dep = SHIP_DRY + rtg_m + chunk + max(rem, 0) * (1 + TANK)
        g_dep = m_dep * (1 - math.exp(-DV_DEPART / ve_gas))
        rem -= g_dep
        if keepalive:
            t_in = T_GRID[-1] - T_GRID[::-1]              # aphelion -> perihelion
            bank_in = np.linspace(max(rem, 0), 0.0, len(t_in)) / 1000
            e_in, _ = phase_energy(akw, n_rtg, T_TRANSFER + T_OPS_YR * YEAR,
                                   t_in, R_GRID[::-1], bank_in, pka)
            g_ka_in = e_in / (LHV * ETA_FC)
            rem -= g_ka_in
        need = max(DV_BUDGET_IN - DV_DEPART - lit, 0.0)
        m_mid = SHIP_DRY + rtg_m + chunk + max(rem, 0) * (1 + TANK)
        g_res = m_mid * (1 - math.exp(-need / ve_gas))
        shortfall = g_res - rem
        bank += shortfall * 0.7
        if abs(shortfall) < 5:
            break
    if keepalive:
        out = {"g_out": g_out, "g_ka_ops": g_ka_ops, "g_ka_in": g_ka_in}
    return bank, out


def launch_t(bank, akw, chunk, n_rtg):
    stack = (SHIP_DRY + n_rtg * MMRTG_KG + bank * (1 + TANK)
             + bank / 1000 * ZBO_KG_PER_T + akw * 1000 / 120.0)
    return (stack + kick_wet(stack, 7300.0)) / 1000.0


# closed-form sanity anchors
print("== sanity anchors ==")
print(f"P_zbo at 80 t gas: {ZBO_W_PER_T*80:.0f} We (expect 1067)")
print(f"array 100 kW at Saturn, LILT: {100e3/SATURN_R**2/LILT:.0f} We (expect 733)")
print(f"array 300 kW at Saturn, LILT: {300e3/SATURN_R**2/LILT:.0f} We (expect 2199)")

# regression: keep-alive OFF must reproduce R174's canonical 79.8 t
b0, _ = chain(40_000.0, 100.0, 450 * G0, 1000.0, 500.0, 300.0, 0, keepalive=False)
print(f"\nregression, keep-alive OFF (R174 canonical): bank {b0/1000:.1f} t (expect ~79.8)")

# canonical, keep-alive ON, no RTG
b1, d1 = chain(40_000.0, 100.0, 450 * G0, 1000.0, 500.0, 300.0, 0)
gka = sum(d1.values())
print(f"\ncanonical keep-alive ON, no RTG: bank {b1/1000:.1f} t "
      f"(growth {b1/b0:.2f}x, +{(b1-b0)/1000:.1f} t)")
print(f"  keep-alive gas {gka/1000:.1f} t = {gka/HOTEL_GAS:.1f}x legacy hotel line "
      f"(out {d1['g_out']/1000:.1f} / ops {d1['g_ka_ops']/1000:.1f} / in {d1['g_ka_in']/1000:.1f})")
l0, l1 = launch_t(b0, 100, 40_000.0, 0), launch_t(b1, 100, 40_000.0, 0)
print(f"  launch (2-stage kick): {l0:.0f} -> {l1:.0f} t (+{l1-l0:.0f})")

# RTG suite scan at canonical: coverage of shortfall energy
e_ref = gka * LHV * ETA_FC
nstar = None
for n in range(1, 11):
    bn, dn = chain(40_000.0, 100.0, 450 * G0, 1000.0, 500.0, 300.0, n)
    e_n = sum(dn.values()) * LHV * ETA_FC
    cov = 1 - e_n / e_ref
    ln = launch_t(bn, 100, 40_000.0, n)
    print(f"  N={n}: bank {bn/1000:.1f} t, shortfall coverage {cov*100:.0f}%, "
          f"launch {ln:.0f} t (saves {l1-ln:.0f}), PuO2 {n*MMRTG_PU:.1f} kg")
    if nstar is None and cov >= 0.90:
        nstar = (n, bn, ln, cov)
print(f"N* (>=90% coverage): {nstar[0]} MMRTG, PuO2 {nstar[0]*MMRTG_PU:.1f} kg "
      f"(Cassini envelope 32.7), net launch saving {l1-nstar[2]:.0f} t")

# R176 best corner (80 t chunk, 300 kW, moon-tour, 480 s): array self-coverage
b2_off, _ = chain(80_000.0, 300.0, 480 * G0, 600.0, 300.0, 300.0, 0, keepalive=False)
b2, d2 = chain(80_000.0, 300.0, 480 * G0, 600.0, 300.0, 300.0, 0)
g2 = sum(d2.values())
print(f"\nR176-best corner keep-alive ON: bank {b2_off/1000:.1f} -> {b2/1000:.1f} t, "
      f"shortfall gas {g2/1000:.2f} t")
print(f"  launch shift: {launch_t(b2_off,300,80_000.0,0):.0f} -> "
      f"{launch_t(b2,300,80_000.0,0):.0f} t "
      f"({(launch_t(b2,300,80_000.0,0)/launch_t(b2_off,300,80_000.0,0)-1)*100:+.1f}%)")

# trickle: RTG spare watts beyond 4 AU inbound + ops, at N* suite
n = nstar[0]
t_in = T_GRID[-1] - T_GRID[::-1]
mask = R_GRID[::-1] > 4.0
_, sp_in = phase_energy(100.0, n, T_TRANSFER + T_OPS_YR * YEAR,
                        t_in[mask], R_GRID[::-1][mask],
                        np.zeros(mask.sum()), 300.0)
t_ops = np.linspace(0.0, T_OPS_YR * YEAR, 400)
_, sp_ops = phase_energy(100.0, n, T_TRANSFER, t_ops,
                         np.full_like(t_ops, SATURN_R), 50.0, 300.0)
g_trickle = (sp_in + sp_ops) * ETA_CHG / LHV
print(f"\ntrickle at N*={n} (ops + inbound r>4 AU, RTG watts only): "
      f"{g_trickle/1000:.1f} t gas from chunk water")
# reductio: bulk-charging the canonical bank by RTG alone
e_bank = b1 * LHV / ETA_CHG
n_bulk = e_bank / (MMRTG_W * 0.85 * (T_TRANSFER + (T_OPS_YR + 5.43) * YEAR))
print(f"reductio: RTG-only bulk charge of canonical bank needs {n_bulk:.0f} MMRTGs")
