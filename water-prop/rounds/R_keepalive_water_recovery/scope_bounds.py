#!/usr/bin/env python3
"""Pre-script: R-keepalive-water-recovery bounds.

R177's STUDY named "keep-alive product-water recovery (zero-PuO2 attack on
the H1 liability)" as a follow-on. This round adjudicates that suggestion
— and the pre-script indicates it dies on a structural theorem:

  In the chain model, instantaneous spare power and keep-alive shortfall
  are mutually exclusive (spare = max(0, avail - load) > 0 iff
  short = max(0, load - avail) = 0). Recovery can therefore never re-split
  product water with energy that coexists with the draw; it can only
  time-shift feedstock. Feedstock is scarce only OUTBOUND (no chunk), and
  with monotone-declining outbound avail against a constant load there is
  a single crossing radius: the spare window closes at exactly the point
  the draw opens. The re-split credit is identically zero — not small.

What remains to price: (a) the crossing structure across corners,
(b) the retention penalty if product water is hauled instead of vented
(the R177/178 venting convention adjudicated as optimal, not merely
conservative), (c) the condenser/recovery hardware dead mass.
"""
import math

import numpy as np

G0 = 9.80665
YEAR = 3.156e7
LHV = 13.3e6
ETA_FC = 0.55
LILT = 1.5
ZBO_W_PER_T = 1.5 * 80 / 9
SATURN_R = 9.54
A_ELL = (1 + SATURN_R) / 2
ECC = (SATURN_R - 1) / (SATURN_R + 1)
T_FULL = A_ELL ** 1.5 * YEAR
_E = np.linspace(0, math.pi, 4000)
_M = _E - ECC * np.sin(_E)
T_GRID = _M / (2 * math.pi) * T_FULL
R_GRID = A_ELL * (1 - ECC * np.cos(_E))
VE_GAS = 450.0 * G0
TANK = 0.20


def avail(akw, r):
    return akw * 1e3 / r ** 2 / np.where(r > 3.0, LILT, 1.0)


print("== crossing structure (outbound), per corner ==")
for akw in (100.0, 200.0, 300.0):
    for pka, bank_t in ((300.0, 91.3), (600.0, 91.3), (150.0, 40.0)):
        load = pka + ZBO_W_PER_T * bank_t
        a = avail(akw, R_GRID)
        spare = np.clip(a - load, 0, None)
        short = np.clip(load - a, 0, None)
        overlap = float(np.trapezoid(spare * (np.cumsum(short) > 0), T_GRID))
        r_cross = math.sqrt(akw * 1e3 / LILT / load) if load > akw * 1e3 / LILT / SATURN_R ** 2 else None
        draw_t = float(np.trapezoid(short, T_GRID)) / (LHV * ETA_FC) / 1000
        print(f"akw {akw:5.0f} pka {pka:3.0f} bank {bank_t:5.1f}: crossing "
              f"{'none (no draw)' if r_cross is None or r_cross > SATURN_R else f'{r_cross:.2f} AU'}"
              f" | draw {draw_t:5.2f} t | spare-x-accrued overlap {overlap:.1f} J")

print("\n== retention penalty at canonical (haul product water vs vent) ==")
# 9.8 t of product water accrues on the outbound leg (R177 canonical draw);
# if retained, it rides through capture + ops + departure + residual burns.
W = 9.8e3
extra = 0.0
for dv in (1000.0, 500.0, 1500.0, 845.0):
    extra += W * (1 - math.exp(-dv / VE_GAS)) * math.exp(dv / VE_GAS)
# simpler exact: extra gas = W * (e^(dv_total/ve) - 1)
dv_tot = 1000.0 + 500.0 + 1500.0 + 845.0
extra_exact = W * (math.exp(dv_tot / VE_GAS) - 1)
kick = 5.84
print(f"retained {W/1e3:.1f} t through {dv_tot/1e3:.2f} km/s of burns: extra gas "
      f"{extra_exact/1e3:.2f} t -> extra bank ~{extra_exact*1.3/1e3:.2f} t -> "
      f"extra launch ~{extra_exact*1.3*1.2*kick/1e3:.1f} t")
print("condenser/recovery hardware allowance: 50-100 kg dead mass -> "
      f"{0.075*1.2*kick:.1f} t launch, buys nothing (credit = 0)")
print("\nverdict shape: venting is OPTIMAL, not merely conservative; the "
      "R177 follow-on dies unless an unpriced role (shielding, abort "
      "feedstock, transient interleaving) is invoked — named, not claimed")
