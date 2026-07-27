#!/usr/bin/env python3
"""Pre-script: R-electrolysis-departure-stage bounds.

Compares harvested-water propellant and electrolysis reactor power for the
electric low-thrust spiral departure (baseline, Round C) vs a reactor-charged
H2/O2 chemical impulsive departure. Does NOT run the added-mass / delivered-
payload model (run.py).

Lever: the reactor electrolyzes harvested water into H2/O2 over the Saturn dwell
(average power), then a high-thrust H2/O2 engine does the Oberth-efficient
impulsive 8.5 km/s departure -- decoupling departure from the low-thrust cruise
engine that forced the megawatt spiral.
"""
import math

G0 = 9.80665
MU_S = 3.793e16
R_RING = 1.07e8
VINF = 6210.0
YEAR = 3.156e7

V_CIRC = math.sqrt(MU_S / R_RING)
V_HYP = math.sqrt(VINF ** 2 + 2 * MU_S / R_RING)
DV_IMPULSIVE = V_HYP - V_CIRC        # chemical high-thrust from circular ring (Oberth)
DV_ELECTRIC_SPIRAL = 21900.0        # Round C continuous electric spiral
M_F = 100_000.0                     # kg final mass
E_ELECTROLYSIS = 20e6               # J/kg water (~70% efficient; ideal HHV 15.9)


def prop(dv, isp):
    return M_F * (math.exp(dv / (isp * G0)) - 1.0)


print("=" * 70)
print("H-F1 [S] -- H2/O2 chemical departure uses LESS water than electric spiral")
print("=" * 70)
p_elec = prop(DV_ELECTRIC_SPIRAL, 800.0)
print(f"    electric spiral: Δv {DV_ELECTRIC_SPIRAL/1000:.1f} km/s, Isp 800 -> "
      f"{p_elec/1000:.0f} t water")
print(f"    chemical impulsive: Δv {DV_IMPULSIVE/1000:.2f} km/s (Oberth at ring):")
for isp in (380.0, 420.0, 450.0):
    p = prop(DV_IMPULSIVE, isp)
    print(f"      Isp {isp:.0f} s -> {p/1000:5.0f} t water  ({p/p_elec:.2f}x electric)")
print(f"    SCOPE: chemical < electric (Oberth Δv factor 2.6x beats Isp factor 2x).")

print()
print("=" * 70)
print("H-F2 [S] -- electrolysis reactor power is few-hundred kWe, NOT Kilopower")
print("=" * 70)
for isp in (420.0,):
    p = prop(DV_IMPULSIVE, isp)
    E = p * E_ELECTROLYSIS
    print(f"    Isp {isp:.0f}: {p/1000:.0f} t water -> electrolysis energy {E:.2e} J")
    for dwell_yr in (1.0, 2.0, 3.0):
        kwe = E / (dwell_yr * YEAR) / 1e3
        print(f"      dwell {dwell_yr:.0f} yr -> reactor {kwe:5.0f} kWe "
              f"({kwe/1248:.2f}x electric-spiral 1248 kWe)")
    # Kilopower window
    dwell_30kwe = E / 30e3 / YEAR
    print(f"    dwell needed for 30-kWe (Kilopower-class) electrolysis = "
          f"{dwell_30kwe:.0f} yr (absurd)")
print(f"    SCOPE: 200-600 kWe at 1-2 yr dwell; not Kilopower. Falsified if <100 or >=1248.")

print()
print("=" * 70)
print("H-F3 [S] -- added dry mass + cryo-H2 storage problem")
print("=" * 70)
p = prop(DV_IMPULSIVE, 420.0)
m_h2 = p * 2 / 18
m_o2 = p * 16 / 18
print(f"    H2/O2 propellant {p/1000:.0f} t = {m_h2/1000:.0f} t H2 + {m_o2/1000:.0f} t O2")
print(f"    H2 is 11% by mass and boils at 20 K -> cryo storage over the dwell OR")
print(f"    just-in-time electrolysis (spikes reactor power). Saturn ~90 K ambient")
print(f"    helps O2 (bp 90 K) but not H2. SCOPE: added dry mass >= several t;")
print(f"    boiloff/power-spike first-order. Falsified if added mass <1 t.")
