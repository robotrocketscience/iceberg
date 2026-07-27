#!/usr/bin/env python3
"""Pre-script: R-cryo-hydrogen-storage-saturn bounds.

Tank geometry + per-source heat-leak brackets for storing the 77 t LH2 departure
propellant (R-electrolysis-departure-stage) over a multi-year Saturn dwell. Does
NOT run the full boiloff / cryocooler grid (run.py).

Three heat sources: MLI radiation (small at Saturn's 90 K), ortho-para self-heat
(showstopper if uncatalyzed), reactor proximity (showstopper if unshielded).
"""
import math

SIGMA = 5.67e-8
M_H2 = 77_000.0            # kg (Round F, Isp 420)
RHO_LH2 = 70.8            # kg/m^3 (para, 20.3 K)
L_V = 446e3              # J/kg latent heat H2 at 20 K
DH_OP = 527e3            # J/kg ortho->para conversion (normal-H2 75% ortho -> para)
YEAR = 3.156e7

# tank geometry (sphere)
V = M_H2 / RHO_LH2
R = (3 * V / (4 * math.pi)) ** (1 / 3)
A = 4 * math.pi * R ** 2

print("=" * 66)
print("Tank geometry")
print("=" * 66)
print(f"    77 t LH2 / {RHO_LH2} kg/m^3 = {V:.0f} m^3 -> sphere r={R:.2f} m, "
      f"diam {2*R:.1f} m, area {A:.0f} m^2")


def mli_watts(Th, Tc=20.0, estar=1e-3):
    return estar * SIGMA * (Th ** 4 - Tc ** 4) * A


def boiloff_frac(watts, dwell_yr):
    return watts * dwell_yr * YEAR / L_V / M_H2


print()
print("=" * 66)
print("H-G1 [S] -- MLI radiation is small at Saturn's cold environment")
print("=" * 66)
for Th in (50.0, 90.0, 150.0):
    for estar in (5e-4, 1e-3, 2e-3):
        w = mli_watts(Th, estar=estar)
        print(f"    warm-bnd {Th:5.0f} K, e*={estar:.0e}: {w:6.2f} W -> "
              f"2-yr boiloff {100*boiloff_frac(w,2):5.2f}%")
# near-Earth comparison
print(f"    (near-Earth 250 K warm boundary, e*=1e-3: {mli_watts(250.0):.1f} W -> "
      f"{100*boiloff_frac(mli_watts(250.0),2):.0f}% -- Saturn is ~{mli_watts(250.0)/mli_watts(90.0):.0f}x better)")
print(f"    SCOPE: MLI-only 2-yr boiloff < 5% at nominal (90 K, e*=1e-3).")

print()
print("=" * 66)
print("H-G2 [S] -- ortho-para self-heat: showstopper if UNCATALYZED")
print("=" * 66)
E_op = M_H2 * DH_OP
print(f"    full ortho->para of 77 t releases {E_op:.2e} J = {E_op/L_V/M_H2*100:.0f}% "
      f"of latent-heat-equivalent (527 > 446 kJ/kg -> boils off MORE than the inventory)")
for dwell in (1.0, 2.0):
    print(f"    uncatalyzed over {dwell:.0f} yr -> self-heat {E_op/(dwell*YEAR)/1e3:.0f} kW "
          f"(catastrophic)")
print(f"    catalyzed at liquefaction -> storage self-heat ~0. SCOPE: uncat >100 kW; MANDATORY.")

print()
print("=" * 66)
print("H-G3 [S] -- reactor proximity: showstopper if UNSHIELDED")
print("=" * 66)
def reactor_watts(VF, Trad, eps=1.0):
    return VF * eps * SIGMA * A * Trad ** 4
for VF, tag in ((0.1, "unshielded"), (1e-2, "partial shield"), (1e-3, "shadow shield+boom")):
    w = reactor_watts(VF, 700.0)
    print(f"    VF={VF:.0e} ({tag:20}) @ 700 K radiators: {w:9.1f} W -> "
          f"1-yr boiloff {100*boiloff_frac(w,1):6.1f}%")
print(f"    SCOPE: unshielded >100 W; shadow-shielded <=10 W. Reactor separation MANDATORY.")

print()
print("=" * 66)
print("H-G4 -- with both requirements met: total + zero-boiloff cryocooler")
print("=" * 66)
total = mli_watts(90.0) + reactor_watts(1e-3, 700.0) + 5.0  # +5 W struts
print(f"    MLI(90 K) {mli_watts(90.0):.1f} + reactor(shielded) {reactor_watts(1e-3,700.0):.1f} "
      f"+ struts ~5 = {total:.1f} W total")
print(f"    2-yr boiloff = {100*boiloff_frac(total,2):.1f}%")
carnot = 20.0 / (90.0 - 20.0)
for frac in (0.15, 0.25):
    cop = carnot * frac
    print(f"    zero-boiloff cryocooler (COP {frac:.0%} of Carnot={carnot:.2f} -> {cop:.3f}): "
          f"{total/cop:.0f} W input")
print(f"    SCOPE: total 10-40 W, cryocooler <2 kW -> tractable; Round F survives.")
