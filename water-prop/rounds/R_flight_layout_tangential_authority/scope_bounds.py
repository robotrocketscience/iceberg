#!/usr/bin/env python3
"""Pre-script: R-flight-layout-tangential-authority bounds.

Reproduces the idealized-ring baseline (berth-dump R-berth-dump-axis-geometry)
and states the corner-layout predictions. It does NOT build the corner layout or
run the failure/aft-clustered sweeps -- those live in run.py.

The residual under test (SATURN-SHIP-SPEC §7): the flight thruster layout has
plume-safe tangential authority about BOTH in-plane axes -- claimed 'a generic
property of any 3-axis-couple RCS'. This round argues it is generic only for a
+/-z-distributed layout and fails for an aft-clustered one.
"""
import math

F = 5.0                       # N per thruster (berth rounds)
A, H = 4.0, 4.0               # idealized-ring radius / half-height (berth-dump)
L_BERTH = 5000.0              # N.m.s injection (R-berth-momentum-management)
TAU_TH = 2.5                  # N.m re-perturbation threshold (berth-dump)
ISP_CG = 70.0                 # s cold-gas (R-berth-momentum-management)
DESPIN_CG_AT_15000 = 125.0    # kg at 15000 N.m.s (R_chunk_despin_budget H2)

print("=" * 70)
print("BASELINE -- idealized-ring couple authority (berth-dump reproduction)")
print("=" * 70)
# idealized ring: a +x couple from {T1@(-A,0,+H) fires -y, T5@(-A,0,-H) fires +y}
# torque about x = sum r x F. |tau| = 2 * F * H (moment arm H about x for a y-force
# separated by 2H in z). Actually couple torque = F * (2H) for two y-forces at +/-H.
tau_inplane_ring = F * (2 * H)
print(f"    in-plane pure-couple torque (ring, arm 2H={2*H} m) = {tau_inplane_ring:.1f} N.m")
print(f"    dump time for {L_BERTH:.0f} N.m.s = {L_BERTH/tau_inplane_ring:.0f} s")

print()
print("=" * 70)
print("H-A3 [W] -- authority/dump-time/propellant predictions (corner layout)")
print("=" * 70)
az = 2.0                      # bus half-height (corner layout)
# corner in-plane couple: two tangential thrusters separated by 2*az in z.
# tangential force component in-plane ~ F; torque about in-plane axis ~ F*(2*az)*k
# where k<=1 is the fraction of the tangential force aligned to make the couple.
tau_corner = F * (2 * az)     # optimistic (k=1); run.py computes the real k
print(f"    corner in-plane couple torque (arm 2*az={2*az} m, k<=1) <= {tau_corner:.1f} N.m")
print(f"    dump time <= {L_BERTH/tau_corner:.0f} s  (SCOPE: <=1800 s, torque>=10 N.m)")
prop = DESPIN_CG_AT_15000 * L_BERTH / 15000.0
print(f"    propellant (despin-scaled) = {prop:.0f} kg  (SCOPE: ~42 kg)")

print()
print("=" * 70)
print("H-A5 [S] -- aft-clustered layout has NO plume-safe in-plane couple")
print("=" * 70)
print("    In-plane couple needs a force-pair separated in z. Aft-clustered")
print("    (|dz|~0) can only make an in-plane torque with +/-z (axial) thrusters")
print("    separated in x or y -- and the +z member fires its plume INTO the")
print("    bag at high +z (cos_th>0, plume core). So no plume-safe in-plane")
print("    couple. SCOPE: aft-clustered fails H-A2; genericity is conditional")
print("    on +/-z distribution. Falsified if aft-clustered yields a safe couple.")

print()
print("SCOPE summary: H-A1/A2/A3 predicted HOLD (residual clears on real layout);")
print("H-A5 predicted HOLD (converts 'generic' into a +/-z-distribution constraint);")
print("H-A4 (single-fault) is the genuine unknown -- corner layout has fewer")
print("redundant tangential thrusters per in-plane axis than the ring.")
