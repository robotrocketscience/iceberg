#!/usr/bin/env python3
"""Pre-script: derive SCOPE bounds for R-inbound-dark-leg-energy.

Run BEFORE writing SCOPE.md; its printed numbers become the registered bounds
(convention adopted after four hand-arithmetic falsifications, R172 Revisit).
"""
import math

import numpy as np

G0 = 9.80665
YEAR = 3.156e7
SATURN_R = 9.54
A = (1 + SATURN_R) / 2
ECC = (SATURN_R - 1) / (SATURN_R + 1)
T_FULL = A ** 1.5 * YEAR                       # full ellipse period, s
VE_MET = 800.0 * G0
VE_CHEM = 450.0 * G0
ETA_THR = 0.6
ETA_CHG = 0.66
ARRAY_KW_1AU = 83.0                            # already aboard per R172
SHIP_DRY = 20_000.0
CHUNK = 40_000.0                               # canonical case
DV_DEPART = 1500.0
DV_BRAKE = 2000.0
DV_TRIM = 500.0

# time inside r_lim on the return ellipse (same geometry as outbound, mirrored)
def t_inside(r_lim):
    cosE = (1 - r_lim / A) / ECC
    E = math.acos(max(-1, min(1, cosE)))
    M = E - ECC * math.sin(E)
    return M / (2 * math.pi) * T_FULL

for r in (2.0, 3.0, 3.5, 4.0):
    print(f"time inside {r} AU on return: {t_inside(r)/YEAR:.2f} yr")

# lit-leg MET throughput: array power over the inside-3.5AU window
n = 3000
E = np.linspace(0, math.pi, n)
M = E - ECC * np.sin(E)
t = M / (2 * math.pi) * T_FULL
r = A * (1 - ECC * np.cos(E))
mask = r <= 3.5
e_harvest = np.trapezoid(ARRAY_KW_1AU * 1e3 / r[mask] ** 2, t[mask])
prop_lit = e_harvest * ETA_THR / (0.5 * VE_MET ** 2)
m1 = SHIP_DRY + CHUNK                          # stack near arrival (pre-trim)
dv_lit = VE_MET * math.log((m1 + prop_lit) / m1)
print(f"lit-window harvest: {e_harvest/1e9:.0f} GJ -> {prop_lit/1000:.1f} t MET propellant")
print(f"lit-leg dv capability on {m1/1000:.0f} t stack: {dv_lit:.0f} m/s")

# banked-gas Saturn departure: stack at departure ~ ship + chunk (+ bank)
def gas_for_departure(bank_guess):
    m0 = SHIP_DRY + CHUNK + bank_guess * 1.2   # gas + 20% tanks aboard at burn
    gas = m0 * (1 - math.exp(-DV_DEPART / VE_CHEM))
    return gas

gas = 15_000.0
for _ in range(20):
    gas = gas_for_departure(gas)
print(f"banked gas for {DV_DEPART} m/s departure: {gas/1000:.1f} t")
charge = gas * 13.3e6 / ETA_CHG
print(f"charge energy: {charge/1e9:.0f} GJ vs outbound-window harvest at this array: "
      f"{np.trapezoid(ARRAY_KW_1AU*1e3/r[r<=3.0]**2, t[r<=3.0])/1e9:.0f} GJ (r<3 AU, 0.62 yr)")
arr_needed = charge / np.trapezoid(1.0 / r[r <= 3.0] ** 2, t[r <= 3.0]) / 1e3
print(f"array needed to charge in outbound window: {arr_needed:.0f} kW at 1 AU")

# dark residual after departure-by-gas and lit braking
dark_resid = DV_DEPART + DV_BRAKE + DV_TRIM - DV_DEPART - dv_lit
print(f"dark residual dv (brake+trim minus lit capability): {dark_resid:.0f} m/s")
# launch-mass penalty: gas water + tanks + ZBO cooler (~R172 cold tier)
lh2 = gas / 9
penalty = gas + gas * 0.2 + lh2 / 1000 * 1.5 * 50
print(f"non-fission variant launch-mass penalty: {penalty/1000:.1f} t "
      f"(vs Kilopower band 1.5-3 t)")
