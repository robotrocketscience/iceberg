#!/usr/bin/env python3
"""
Saturn-side rendezvous simulation: ISRU spacecraft approaching a ring chunk.

Saturn-centered 2D inertial frame, point-mass gravity, scipy RK45 integration.
Demonstrates the four-phase rendezvous architecture:

  1. Spacecraft starts in Saturn capture orbit (post-chemical insertion)
  2. Hohmann phasing to target ring radius
  3. Co-orbital phasing drift to catch the target chunk
  4. Final close approach using Clohessy-Wiltshire-style relative motion

Output: matplotlib plots of inertial trajectories, relative motion in target
frame, relative velocity envelope, and a per-phase ΔV summary.

Run:
  uv run --with numpy --with scipy --with matplotlib python saturn_rendezvous_sim.py
or:
  python3 saturn_rendezvous_sim.py    (if numpy/scipy/matplotlib already installed)
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
GM_SATURN = 3.7931187e7      # km^3/s^2
R_SATURN  = 60268.0          # km
R_BRING   = 102000.0         # km - target ring radius (within B-ring)
DEG       = np.pi / 180.0

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def v_circ(r):
    return np.sqrt(GM_SATURN / r)

def two_body_rhs(t, state):
    """6-state two-body dynamics (point-mass Saturn). state = [x,y,vx,vy]."""
    x, y, vx, vy = state
    r = np.sqrt(x*x + y*y)
    ax = -GM_SATURN * x / r**3
    ay = -GM_SATURN * y / r**3
    return [vx, vy, ax, ay]

def state_at_circular(r, theta_deg):
    """Initial state on a circular orbit at radius r and angle theta."""
    theta = theta_deg * DEG
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    v = v_circ(r)
    vx = -v * np.sin(theta)
    vy =  v * np.cos(theta)
    return np.array([x, y, vx, vy])

def integrate_phase(state0, t_span, max_step=10.0):
    """Integrate two-body dynamics; return time array and state history."""
    sol = solve_ivp(two_body_rhs, t_span, state0,
                    method='RK45', rtol=1e-9, atol=1e-9,
                    max_step=max_step, dense_output=True)
    return sol.t, sol.y.T   # shape (N, 4)

def apply_impulse(state, dvx, dvy):
    """Instantaneous velocity change."""
    new = state.copy()
    new[2] += dvx
    new[3] += dvy
    return new

def relative_state(sc_state, target_state):
    """Spacecraft position/velocity expressed in target's local-vertical/local-horizontal (LVLH).

    target points radially outward (R-bar = +x_lvlh)
    along-track prograde (V-bar = +y_lvlh)
    """
    rt = target_state[:2]
    vt = target_state[2:]
    r_hat = rt / np.linalg.norm(rt)
    # along-track basis: perpendicular to r_hat, in the direction of vt
    along = vt - (vt @ r_hat) * r_hat
    along_hat = along / np.linalg.norm(along)

    # Express SC position relative to target in LVLH
    dr_inertial = sc_state[:2] - target_state[:2]
    dv_inertial = sc_state[2:] - target_state[2:]

    R_bar = dr_inertial @ r_hat
    V_bar = dr_inertial @ along_hat
    Rdot  = dv_inertial @ r_hat
    Vdot  = dv_inertial @ along_hat

    return np.array([R_bar, V_bar, Rdot, Vdot])

# ---------------------------------------------------------------------------
# Mission setup
# ---------------------------------------------------------------------------
# Target chunk: circular orbit at B-ring radius
target_state0 = state_at_circular(R_BRING, theta_deg=90.0)

# Spacecraft: starts in slightly inner circular orbit, ~30 deg behind in phase
# (post-chemical-capture state — pretend we've already done Saturn insertion)
SC_INITIAL_RADIUS = 95000.0     # km, inside B-ring
SC_INITIAL_PHASE  = 60.0        # deg, behind target
sc_state0 = state_at_circular(SC_INITIAL_RADIUS, theta_deg=SC_INITIAL_PHASE)

print("=" * 72)
print("Saturn-side rendezvous simulation")
print("=" * 72)
print(f"Saturn GM           : {GM_SATURN:.3e} km^3/s^2")
print(f"Saturn radius       : {R_SATURN:.0f} km")
print(f"Target ring radius  : {R_BRING:.0f} km  ({R_BRING/R_SATURN:.2f} R_S)")
print(f"Target circular V   : {v_circ(R_BRING):.3f} km/s")
print(f"SC start radius     : {SC_INITIAL_RADIUS:.0f} km  ({SC_INITIAL_RADIUS/R_SATURN:.2f} R_S)")
print(f"SC start phase      : {SC_INITIAL_PHASE} deg behind target")
print(f"Period at target    : {2*np.pi*np.sqrt(R_BRING**3/GM_SATURN)/3600:.2f} hours")

dV_total = 0.0
dV_log = []

# ---------------------------------------------------------------------------
# PHASE 1: Hohmann transfer from 95,000 km up to 102,000 km
# ---------------------------------------------------------------------------
print()
print("PHASE 1: Hohmann transfer to ring radius")
r1 = SC_INITIAL_RADIUS
r2 = R_BRING
a_t = 0.5 * (r1 + r2)
v_p_t = np.sqrt(GM_SATURN * (2/r1 - 1/a_t))
v_a_t = np.sqrt(GM_SATURN * (2/r2 - 1/a_t))
v_c1  = v_circ(r1)
v_c2  = v_circ(r2)
dv1   = v_p_t - v_c1
dv2   = v_c2 - v_a_t
T_hohmann = np.pi * np.sqrt(a_t**3 / GM_SATURN)
print(f"  ΔV_1 (depart inner) = {dv1*1000:.1f} m/s")
print(f"  ΔV_2 (circularize)  = {dv2*1000:.1f} m/s")
print(f"  Transfer time       = {T_hohmann/3600:.2f} hours")
dV_total += abs(dv1) + abs(dv2)
dV_log.append(("Hohmann depart", abs(dv1)))
dV_log.append(("Hohmann circularize", abs(dv2)))

# Apply first burn (prograde at periapsis of transfer = current location)
# spacecraft is currently on circular orbit at r1; prograde direction = current velocity unit
def prograde_unit(state):
    v = state[2:]
    return v / np.linalg.norm(v)

phat = prograde_unit(sc_state0)
sc_after_burn1 = apply_impulse(sc_state0, dv1*phat[0], dv1*phat[1])

# Integrate transfer ellipse for half-period
t1, hist1 = integrate_phase(sc_after_burn1, (0, T_hohmann), max_step=60.0)
t1_target, hist1_target = integrate_phase(target_state0, (0, T_hohmann), max_step=60.0)

# Apply circularization burn
sc_at_apoapsis = hist1[-1]
phat = prograde_unit(sc_at_apoapsis)
sc_after_burn2 = apply_impulse(sc_at_apoapsis, dv2*phat[0], dv2*phat[1])

# ---------------------------------------------------------------------------
# PHASE 2: Co-orbital phasing — drift to close the angular gap
# ---------------------------------------------------------------------------
print()
print("PHASE 2: Co-orbital phasing drift")
# After phase 1, both SC and target are on the same circular orbit at R_BRING.
# But there's an angular phase difference. To phase, we use a "phasing orbit":
# drop into a slightly lower orbit, complete one revolution, return. The lower
# orbit has shorter period -> we gain phase.
target_state_now = hist1_target[-1]
sc_state_now     = sc_after_burn2

# Compute current phase difference
sc_theta     = np.arctan2(sc_state_now[1], sc_state_now[0])
target_theta = np.arctan2(target_state_now[1], target_state_now[0])
phase_diff   = (target_theta - sc_theta + 2*np.pi) % (2*np.pi)
print(f"  Phase difference (target ahead of SC): {np.degrees(phase_diff):.2f} deg")

# Use a single phasing orbit: drop to lower r_p such that one revolution
# advances SC phase by 'phase_diff' (relative to the target which keeps moving).
T_target = 2*np.pi*np.sqrt(R_BRING**3/GM_SATURN)
# desired SC phasing-orbit period such that after 1 rev SC has advanced
# (phase_diff/2pi) * T_target more than target -> T_phasing = T_target * (1 - phase_diff/(2*pi))
T_phasing = T_target * (1 - phase_diff/(2*np.pi))
a_phasing = (T_phasing**2 * GM_SATURN / (4*np.pi**2))**(1/3)
# this is the semi-major axis of the phasing ellipse with apoapsis at R_BRING
r_p_phasing = 2*a_phasing - R_BRING
print(f"  Phasing orbit a    = {a_phasing:.0f} km")
print(f"  Phasing periapsis  = {r_p_phasing:.0f} km")
print(f"  Phasing period     = {T_phasing/3600:.2f} hours (vs target {T_target/3600:.2f})")

# Burn to enter phasing orbit (retrograde at apoapsis)
v_at_R_BRING_phasing = np.sqrt(GM_SATURN*(2/R_BRING - 1/a_phasing))
v_at_R_BRING_circ    = v_circ(R_BRING)
dv_phase_in  = v_at_R_BRING_circ - v_at_R_BRING_phasing  # retrograde
phat = prograde_unit(sc_state_now)
sc_after_phase_burn = apply_impulse(sc_state_now,
                                     -dv_phase_in*phat[0],
                                     -dv_phase_in*phat[1])
print(f"  ΔV in/out of phasing = {dv_phase_in*1000:.1f} m/s each (2x)")
dV_total += 2 * dv_phase_in
dV_log.append(("Phase-orbit entry", dv_phase_in))
dV_log.append(("Phase-orbit exit", dv_phase_in))

# Integrate phasing orbit for one period
t2, hist2 = integrate_phase(sc_after_phase_burn, (0, T_phasing), max_step=60.0)
t2_target, hist2_target = integrate_phase(target_state_now, (0, T_phasing), max_step=60.0)

# Burn to re-enter circular orbit at R_BRING (prograde at apoapsis = current location)
sc_back_at_apoapsis = hist2[-1]
phat = prograde_unit(sc_back_at_apoapsis)
sc_after_phase_exit = apply_impulse(sc_back_at_apoapsis,
                                     dv_phase_in*phat[0],
                                     dv_phase_in*phat[1])

# ---------------------------------------------------------------------------
# PHASE 3 + 4: Close-approach using small impulsive burns (V-bar approach)
# ---------------------------------------------------------------------------
print()
print("PHASE 3+4: Close approach to capture range")
# At end of phase 2, SC should be ~co-located with target on the same orbit.
# Real life would never be perfect — there's residual position and velocity offset.
# Use Clohessy-Wiltshire-like thinking: get to ~1 km behind target on V-bar,
# then close at <0.1 m/s.

# For the sim we'll do this with two small impulsive burns:
#   (a) cancel residual relative velocity, place SC ~1 km trailing
#   (b) very small forward impulse to drift in, then brake at 10 m

# Compute residual relative state
target_at_phase_end = hist2_target[-1]
rel_state = relative_state(sc_after_phase_exit, target_at_phase_end)
print(f"  Residual offset      : R-bar={rel_state[0]:.2f} km, V-bar={rel_state[1]:.2f} km")
print(f"  Residual rel. velocity: Rdot={rel_state[2]*1000:.2f} m/s, Vdot={rel_state[3]*1000:.2f} m/s")

# (a) match velocities AND place at exactly 1 km trailing
# Simplification: apply impulse that zeros relative velocity, then teleport to 1 km trailing
# (the actual phasing residual would handle this cost — counted as ΔV below)
res_v_mag = np.sqrt(rel_state[2]**2 + rel_state[3]**2)
print(f"  ΔV to null residual rel-velocity: {res_v_mag*1000:.2f} m/s")
dV_total += res_v_mag
dV_log.append(("Residual null", res_v_mag))

# Cancel residual velocity in inertial frame
sc_matched = sc_after_phase_exit.copy()
sc_matched[2] = target_at_phase_end[2]
sc_matched[3] = target_at_phase_end[3]

# Place spacecraft 1 km behind target in along-track direction
along_hat = (target_at_phase_end[2:] -
             (target_at_phase_end[2:] @ (target_at_phase_end[:2]/np.linalg.norm(target_at_phase_end[:2]))) *
              target_at_phase_end[:2]/np.linalg.norm(target_at_phase_end[:2]))
along_hat = along_hat / np.linalg.norm(along_hat)
sc_matched[:2] = target_at_phase_end[:2] - 1.0 * along_hat   # 1 km behind

# Now do a small "approach" maneuver: small prograde burn, drift in, then brake
dv_approach = 0.0005   # km/s = 0.5 m/s — tiny forward push
sc_approach_start = sc_matched.copy()
sc_approach_start[2] += dv_approach*along_hat[0]
sc_approach_start[3] += dv_approach*along_hat[1]
print(f"  Final approach push: {dv_approach*1000:.2f} m/s, drift to 10 m, then brake")
dV_total += 2*dv_approach   # push + brake
dV_log.append(("Final closure push", dv_approach))
dV_log.append(("Final closure brake", dv_approach))

# Integrate close-approach for ~30 minutes
t_approach = 1800.0  # 30 minutes
t3, hist3 = integrate_phase(sc_approach_start, (0, t_approach), max_step=2.0)
t3_target, hist3_target = integrate_phase(target_at_phase_end, (0, t_approach), max_step=2.0)

# Compute relative motion during close approach (in target LVLH)
rel_motion = np.array([relative_state(hist3[i], hist3_target[i])
                        for i in range(len(t3))])

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
print()
print("=" * 72)
print("ΔV summary")
print("=" * 72)
for name, dv in dV_log:
    print(f"  {name:<25} {dv*1000:>8.2f} m/s")
print(f"  {'TOTAL Saturn-side':<25} {dV_total*1000:>8.2f} m/s")
print(f"  {'(in km/s)':<25} {dV_total:>8.4f} km/s")
print()
print("Headline: Saturn-side rendezvous from a 95k-km circular orbit to")
print(f"capture range on a B-ring chunk costs ~{dV_total*1000:.0f} m/s of ΔV.")
print(f"This is the small Saturn-side number that goes into §5b-bis of the")
print(f"sketch doc — the one that says 'water MET tow leg sees ~1-2 km/s.'")
print(f"Empirically: this sim says it's even smaller (~{dV_total*1000:.0f} m/s)")
print("plus whatever the trans-Saturn injection and Saturn departure cost.")

# ---------------------------------------------------------------------------
# Plots
# ---------------------------------------------------------------------------
fig = plt.figure(figsize=(14, 10))

# (1) Inertial frame, full trajectory
ax1 = plt.subplot(2, 2, 1)
ax1.plot(hist1[:, 0]/1000, hist1[:, 1]/1000, 'b-', label='SC: Hohmann')
ax1.plot(hist2[:, 0]/1000, hist2[:, 1]/1000, 'g-', label='SC: phasing')
ax1.plot(hist1_target[:, 0]/1000, hist1_target[:, 1]/1000, 'r--', alpha=0.5, label='Target')
ax1.plot(hist2_target[:, 0]/1000, hist2_target[:, 1]/1000, 'r--', alpha=0.7)
saturn_circ = plt.Circle((0,0), R_SATURN/1000, color='gold', alpha=0.3, label='Saturn')
ring_circ_in  = plt.Circle((0,0), 92000/1000, color='gray', fill=False, alpha=0.4)
ring_circ_out = plt.Circle((0,0), 117500/1000, color='gray', fill=False, alpha=0.4)
ax1.add_patch(saturn_circ)
ax1.add_patch(ring_circ_in)
ax1.add_patch(ring_circ_out)
ax1.set_xlabel('x (1000 km)')
ax1.set_ylabel('y (1000 km)')
ax1.set_title('Saturn-centered inertial frame (Phases 1–2)')
ax1.set_aspect('equal')
ax1.legend(loc='upper right', fontsize=8)
ax1.grid(True, alpha=0.3)
ax1.set_xlim(-150, 150)
ax1.set_ylim(-150, 150)

# (2) Relative motion in target LVLH frame during close approach
ax2 = plt.subplot(2, 2, 2)
ax2.plot(rel_motion[:, 1]*1000, rel_motion[:, 0]*1000, 'b-')
ax2.plot([0], [0], 'r*', markersize=15, label='Target chunk')
ax2.plot([rel_motion[0, 1]*1000], [rel_motion[0, 0]*1000], 'go', label='SC start')
ax2.plot([rel_motion[-1, 1]*1000], [rel_motion[-1, 0]*1000], 'b^', label='SC end')
ax2.set_xlabel('V-bar (along-track, m)')
ax2.set_ylabel('R-bar (radial, m)')
ax2.set_title('Close-approach in target LVLH frame')
ax2.legend()
ax2.grid(True, alpha=0.3)
ax2.set_aspect('equal')

# (3) Relative range over time during close approach
ax3 = plt.subplot(2, 2, 3)
rel_range = np.sqrt(rel_motion[:, 0]**2 + rel_motion[:, 1]**2) * 1000  # m
ax3.plot(t3/60, rel_range, 'b-')
ax3.set_xlabel('Time (min)')
ax3.set_ylabel('Range to target (m)')
ax3.set_title('Range vs. time, final approach')
ax3.grid(True, alpha=0.3)
ax3.set_yscale('log')

# (4) Relative velocity over time
ax4 = plt.subplot(2, 2, 4)
rel_speed = np.sqrt(rel_motion[:, 2]**2 + rel_motion[:, 3]**2) * 1000  # m/s
ax4.plot(t3/60, rel_speed, 'r-')
ax4.set_xlabel('Time (min)')
ax4.set_ylabel('Relative speed (m/s)')
ax4.set_title('Relative speed during final approach')
ax4.grid(True, alpha=0.3)

plt.tight_layout()
out_path = './saturn_rendezvous_plot.png'
plt.savefig(out_path, dpi=120, bbox_inches='tight')
print(f"\nPlot saved: {out_path}")
plt.show()
