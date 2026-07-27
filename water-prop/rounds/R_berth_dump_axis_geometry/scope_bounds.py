#!/usr/bin/env python3
"""Pre-script: R-berth-dump-axis-geometry bounds. The LAST question standing in
the momentum-management thread: does a plume-safe (bag-in-backflow) thruster
couple exist for EVERY physically-required momentum-dump axis, given the fixed
12-corner RCS layout and the fixed forward grapple position?

Structural insight (drives H1): the capture arm r_off is along the boom (+z).
The injected momentum is L = r_off_vec x (m_s v_c_vec). With r_off_vec || z-hat,
L = r_off*m_s*(v_x*yhat - v_y*xhat) -- ALWAYS in the boom-perpendicular (x-y)
plane; the along-boom component of v_c contributes nothing. So every required
dump axis (-L_hat) lies in the x-y plane. In-plane torque couples can be built
from TANGENTIAL thrusts (in x-y) at z-offset, whose plumes point sideways --
away from the forward bag at high +z. The only plume-dangerous thrusters are the
retro (-z) ones, whose plume points at the +z bag; they are AVOIDABLE for
in-plane dumps.

Model: envelope box half-size a=4 m (x,y), top/bottom at z=+/-h (h=4 m). Bag
grappled forward at (0,0,z_bag), z_bag = h + boom + r_bag (boom>=3 m grapple
standoff, r_bag~3 m). 12 thrusters: 8 tangential (top+bottom faces, +/-x,+/-y)
+ 4 axial (2 prograde +z / plume away from bag = SAFE, 2 retro -z / plume at bag
= DANGER). Plume pressure P(theta,r) = P_iso*kappa*cos^n(theta) forward,
P_iso*beta backflow; torque on bag = P * A_eff * r_off.

Grids: boom in {3,5,7} m; dump-axis phi in [0,360) in-plane; boom-sway
misalignment alpha in {0,10,20} deg (tilts L out of plane).
"""
import math

G0 = 9.80665
V_E = 70.0 * G0
F = 5.0                       # N per thruster (tau_dump 50 / arm 10)
A = 4.0                       # m envelope half-size
H = 4.0                       # m envelope half-height
R_BAG = 3.0                   # m bag radius (40 t at ~500 kg/m^3)
A_BAG = math.pi * R_BAG ** 2  # ~28 m^2
R_OFF = 5.0                   # m momentum arm
KAPPA, BETA, NEXP = 4.0, 1e-2, 4.0
THETA_C = math.radians(25.0)
TAU_TH = 2.5                  # N.m re-perturbation threshold (5% of 50 N.m dump)

# 12-thruster layout: (position, thrust unit-dir)
TANGENTIAL = [
    ((+A, 0, +H), (0, +1, 0)), ((-A, 0, +H), (0, -1, 0)),
    ((0, +A, +H), (+1, 0, 0)), ((0, -A, +H), (-1, 0, 0)),
    ((+A, 0, -H), (0, -1, 0)), ((-A, 0, -H), (0, +1, 0)),
    ((0, +A, -H), (-1, 0, 0)), ((0, -A, -H), (+1, 0, 0)),
]
PROGRADE = [((+A, +A, +H), (0, 0, +1)), ((-A, -A, +H), (0, 0, +1))]  # plume -z SAFE
RETRO = [((+A, -A, -H), (0, 0, -1)), ((-A, +A, -H), (0, 0, -1))]     # plume +z DANGER


def vsub(p, q): return tuple(p[i] - q[i] for i in range(3))
def vnorm(p): return math.sqrt(sum(x * x for x in p))
def vdot(p, q): return sum(p[i] * q[i] for i in range(3))


def p_iso(r): return F / (2 * math.pi * r ** 2)


def bag_plume_torque(pos, thrust_dir, z_bag):
    """torque on the bag from one firing thruster."""
    plume_dir = tuple(-d for d in thrust_dir)          # exhaust opposite thrust
    to_bag = vsub((0, 0, z_bag), pos)
    r = vnorm(to_bag)
    cos_th = vdot(plume_dir, to_bag) / r
    cos_th = max(-1.0, min(1.0, cos_th))
    if cos_th > 0:                                     # forward hemisphere
        P = p_iso(r) * KAPPA * cos_th ** NEXP
    else:                                              # backflow
        P = p_iso(r) * BETA
    a_eff = min(A_BAG, math.pi * (r * math.tan(THETA_C)) ** 2)
    return P * a_eff * R_OFF, math.degrees(math.acos(cos_th)), r


print("=" * 72)
print("H1 [S] -- the injected momentum is structurally IN-PLANE (r_off || boom);")
print("          every required dump axis lies in the boom-perpendicular plane")
print("=" * 72)
for alpha in (0, 10, 20):
    # boom sway alpha tilts r_off off z; along-boom fraction of L ~ sin(alpha)
    frac = math.sin(math.radians(alpha))
    print(f"    boom sway alpha={alpha:2d} deg -> along-boom fraction of L "
          f"~ {frac:.2f}")
print(f"    SCOPE: |L.boom|/|L| = 0 exactly at alpha=0; < 0.35 for alpha<=20 deg.")
print(f"    Falsified if realistic capture geometry puts >0.5 of L along boom.")

print()
print("=" * 72)
print("H2 [S] -- in-plane couples from TANGENTIAL thrusters keep the bag in")
print("          backflow: max bag-plume torque << 2.5 N.m for boom>=3 m")
print("=" * 72)
for boom in (3, 5, 7):
    z_bag = H + boom + R_BAG
    worst = max(bag_plume_torque(p, d, z_bag)[0] for p, d in TANGENTIAL)
    worst_ang = min(bag_plume_torque(p, d, z_bag)[1] for p, d in TANGENTIAL)
    print(f"    boom={boom} m (z_bag={z_bag} m): max tangential bag-plume torque "
          f"= {worst:.3f} N.m (min plume-bag angle {worst_ang:.0f} deg)")
print(f"    SCOPE: max tangential bag-plume torque < 2.5 N.m for all in-plane")
print(f"    axes at boom>=3 m. Falsified if any tangential couple exceeds 2.5 N.m.")

print()
print("=" * 72)
print("H3 [S] -- the RETRO (-z) thrusters are the only plume-dangerous ones, and")
print("          they are avoidable: in-plane axes remain controllable without them")
print("=" * 72)
z_bag = H + 3 + R_BAG
for tag, group in (("prograde +z (SAFE)", PROGRADE), ("retro -z (DANGER)", RETRO)):
    t, ang, r = bag_plume_torque(*group[0], z_bag)
    print(f"    {tag:22}: bag-plume torque {t:.2f} N.m at {ang:.0f} deg "
          f"({'core' if ang < 25 else 'wing/backflow'}), r={r:.0f} m")
# controllability: tangential set spans in-plane torque axes (x and y)?
# torque of a thruster = r x (F d). Check tangential set produces +/- tau_x, tau_y.
def torque(p, d): return (p[1]*d[2]-p[2]*d[1], p[2]*d[0]-p[0]*d[2], p[0]*d[1]-p[1]*d[0])
tx = [torque(p, d)[0] for p, d in TANGENTIAL]
ty = [torque(p, d)[1] for p, d in TANGENTIAL]
print(f"    tangential set torque_x range: [{min(tx):.0f},{max(tx):.0f}] "
      f"(N.m per unit F.arm) -> +/- controllable")
print(f"    tangential set torque_y range: [{min(ty):.0f},{max(ty):.0f}] "
      f"-> +/- controllable")
print(f"    SCOPE: excluding retro thrusters, +/- torque about x AND y still")
print(f"    spanned by tangential set. Falsified if an in-plane axis is lost.")

print()
print("=" * 72)
print("H4 [W] -- synthesis: dump is always in-plane + in-plane couples are")
print("          tangential/plume-safe -> leg A UNCONDITIONALLY viable for the")
print("          required dump axes; momentum thread CLOSES")
print("=" * 72)
print(f"    The constraint reduces to a cheap plume-aware control-allocation rule:")
print(f"    'build the dump couple from tangential thrusters (deprioritize retro),")
print(f"    keep grapple boom >= 3 m.' No new hardware; CMG (leg B) and precision-")
print(f"    capture (leg C) fully OPTIONAL.")
print(f"    SCOPE: leg A plume-safe for all in-plane axes at boom>=3 m AND the")
print(f"    along-boom residual (boom sway) stays plume-manageable. Falsified if")
print(f"    a realistic geometry forces a core hit on some required axis.")
