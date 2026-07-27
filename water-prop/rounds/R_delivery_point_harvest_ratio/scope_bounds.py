#!/usr/bin/env python3
"""Pre-script: R-delivery-point-harvest-ratio bounds.

Delivery-point Δv table (from vis-viva) + single-leg brackets. Does NOT run the
full cascade x specific-power grid (run.py).

Question: where is the depot prize? Is it "deliver to a higher Earth orbit"
(saves only the LEO-circularization part) or "don't return to Earth at all"
(saves the whole Earth-capture leg, and for a Saturn-orbit depot the departure too)?
"""
import math

G0 = 9.80665
MU_E = 398600.4418            # km^3/s^2
MU_S = 3.793e16              # m^3/s^2
R_LEO = 6578.0               # km (200 km alt)
VINF_E = 10.3                # km/s Earth-arrival hyperbolic excess (Round H / axis 04)
R_RING = 1.07e8              # m
ISP_CHEM = 420.0
VE = ISP_CHEM * G0

# Earth-capture Δv by target orbit (from v_inf = 10.3 at Earth)
v_hyp_leo = math.sqrt(VINF_E ** 2 + 2 * MU_E / R_LEO)      # speed at LEO periapsis on the hyperbola
v_circ_leo = math.sqrt(MU_E / R_LEO)
v_para_leo = math.sqrt(2 * MU_E / R_LEO)                   # parabolic (barely captured)
DV_CAP_LEO = v_hyp_leo - v_circ_leo                        # to LEO circular
DV_CAP_BARELY = v_hyp_leo - v_para_leo                     # to barely-bound high ellipse / cislunar

# Saturn-side
V_CIRC_RING = math.sqrt(MU_S / R_RING) / 1000              # km/s
DV_DEP_ESCAPE = 8.5                                        # km/s Saturn departure (Oberth impulsive)
DV_RING_DEPOT = 2.0                                        # km/s small raise to a Saturn depot orbit

print("=" * 68)
print("Delivery-point Δv table (harvested chunk from the B-ring)")
print("=" * 68)
print(f"    Earth v_inf on arrival = {VINF_E} km/s; LEO v_circ {v_circ_leo:.2f}, "
      f"v_para {v_para_leo:.2f}")
targets = {
    "Saturn ring/orbit depot": (DV_RING_DEPOT, 0.0),
    "heliocentric-at-Saturn":  (DV_DEP_ESCAPE, 0.0),
    "Earth cislunar/high-ell": (DV_DEP_ESCAPE, DV_CAP_BARELY),
    "LEO":                     (DV_DEP_ESCAPE, DV_CAP_LEO),
}
for name, (dv_dep, dv_cap) in targets.items():
    print(f"    {name:26} departure {dv_dep:4.1f} + capture {dv_cap:4.2f} = "
          f"{dv_dep+dv_cap:5.2f} km/s total")

print()
print("=" * 68)
print("H-I2 -- the departure leg (8.5) is HALF the penalty; Earth-orbit choice")
print("        only saves the capture part")
print("=" * 68)
print(f"    LEO capture {DV_CAP_LEO:.2f} vs cislunar {DV_CAP_BARELY:.2f} km/s: "
      f"Earth-orbit choice saves {DV_CAP_LEO-DV_CAP_BARELY:.2f} km/s")
print(f"    but Saturn departure {DV_DEP_ESCAPE} km/s is paid for BOTH -> "
      f"Earth-vicinity delivery stays departure-dominated")
# single-leg propellant ratios (per unit burnout mass)
for name, (dv_dep, dv_cap) in targets.items():
    r_dep = math.exp(dv_dep * 1000 / VE) - 1
    r_cap = math.exp(dv_cap * 1000 / VE) - 1
    print(f"    {name:26} dep prop {r_dep:5.2f}x/burnout, cap prop {r_cap:5.2f}x/chunk")
print(f"    SCOPE: Earth-vicinity >25:1 at flown sp; Saturn-orbit depot <=3:1.")
