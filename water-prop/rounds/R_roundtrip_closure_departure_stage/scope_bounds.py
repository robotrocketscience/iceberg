#!/usr/bin/env python3
"""Pre-script: R-roundtrip-closure-departure-stage bounds.

Reactor-mass and single-leg cascade brackets for the round-trip comparison of the
H2/O2 departure stage vs all-electric. Does NOT run the full D x specific-power x
architecture cascade (run.py).

The competing effects: H2/O2 uses less departure propellant AND a smaller reactor
(350 vs 1248 kWe) but adds ~37 t stage; all-electric carries a megawatt reactor
whose MASS at flown specific power must itself be accelerated through the
departure rocket equation.
"""
import math

G0 = 9.80665
ISP_CHEM, ISP_ELEC = 420.0, 800.0
DV_DEP_CHEM, DV_DEP_ELEC = 8500.0, 21900.0
DV_EARTH_CAP = 7300.0
P_CHEM, P_ELEC = 350.0, 1248.0        # kWe (electrolysis vs electric-spiral)

print("=" * 66)
print("H-H2 [S] -- reactor mass at flown vs aspirational specific power")
print("=" * 66)
print(f"    {'specific power':>16} | {'H2/O2 350 kWe':>14} | {'electric 1248 kWe':>18}")
for sp in (2.4, 10.0, 40.0):
    print(f"    {sp:>13.1f} W/kg | {P_CHEM*1000/sp/1000:>11.0f} t | {P_ELEC*1000/sp/1000:>15.0f} t")
print(f"    SCOPE: at 2.4 W/kg, reactor >=100 t (H2/O2) / >=400 t (electric) -- dwarfs a 30 t chunk.")

print()
print("=" * 66)
print("H-H1/H-H3 -- single-leg departure propellant to accelerate the reactor mass")
print("=" * 66)
D = 30.0
M_DRY = 15.0
for sp in (2.4, 10.0, 40.0):
    m_react_chem = P_CHEM * 1000 / sp / 1000
    m_react_elec = P_ELEC * 1000 / sp / 1000
    # burnout mass (chunk + dry + reactor); ignore tanks in the pre-script bracket
    mf_chem = D + M_DRY + 2.7 + m_react_chem       # +2.7 plant+engine
    mf_elec = D + M_DRY + m_react_elec
    prop_chem = mf_chem * (math.exp(DV_DEP_CHEM / (ISP_CHEM * G0)) - 1)
    prop_elec = mf_elec * (math.exp(DV_DEP_ELEC / (ISP_ELEC * G0)) - 1)
    print(f"    sp={sp:4.1f} W/kg: H2/O2 departure prop {prop_chem:7.0f} t (ratio {prop_chem/D:5.1f}:1) | "
          f"electric {prop_elec:8.0f} t (ratio {prop_elec/D:6.1f}:1)")
print(f"    SCOPE: H2/O2 harvest ratio <=50:1 & electric >150:1 at 2.4 W/kg (>=3x improvement);")
print(f"    viable (<10:1) only at aspirational 40 W/kg. Earth-capture leg adds "
      f"{(math.exp(DV_EARTH_CAP/(ISP_CHEM*G0))-1):.1f}x D more.")
