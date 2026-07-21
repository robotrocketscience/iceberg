#!/usr/bin/env python3
"""Pre-script: R-leo-depot-bootstrap bounds.

Water interest rate = depot water consumed per tonne delivered, per outbound
mode. Break-even dv where the rate hits 1.0. Prints SCOPE bounds.
"""
import math

G0 = 9.80665
VE_MET = 800.0 * G0
DELIVERED = {"canonical": 40_000.0, "big": 80_000.0}
# non-fission hardware through outbound, from R174 corners (ship+bank+tanks+array)
HW = {"canonical": 20_000.0 + 79.8e3 * 1.2 + 2_500.0,
      "big": 20_000.0 + 58.8e3 * 1.2 + 2_500.0}
MODES = {
    "lit_spiral_800s": (15_700.0, VE_MET),
    "depot_kick_450s": (7_300.0, 450.0 * G0),
    "depot_kick_480s": (7_300.0, 480.0 * G0),
}

for case, dm in DELIVERED.items():
    m_dry = HW[case]
    for mode, (dv, ve) in MODES.items():
        prop = m_dry * (math.exp(dv / ve) - 1)
        # electrolysis water for kick gas is 1:1 by mass (gas mass = water mass)
        rate = prop / dm
        print(f"{case:9s} {mode:16s}: outbound propellant {prop/1000:6.0f} t, "
              f"interest rate {rate:5.1f} water-consumed per t delivered")

for ve, name in ((VE_MET, "800 s"), (480 * G0, "480 s")):
    for case, dm in DELIVERED.items():
        be = ve * math.log(1 + dm / HW[case])
        print(f"break-even outbound dv at {name}, {case}: {be:.0f} m/s")

# salvage: depot water for LEO-ops + arrival trim only (<= 1000 m/s at 800 s
# on the arrival stack ship+chunk)
for case, dm in DELIVERED.items():
    m1 = 20_000.0 + dm
    prop = m1 * (1 - math.exp(-1000.0 / VE_MET))
    print(f"salvage rate ({case}, 1 km/s ops at 800 s): {prop/dm:.3f}")
