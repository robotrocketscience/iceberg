#!/usr/bin/env python3
"""Pre-script: R-bag-dynamics-envelope bounds.

R185 named it: "bag dynamics of a non-rigid 40 t load during berthing is
the single largest unknown and has no precedent anywhere." R189 found
the berth_bag stage drives BOTH the retention floor and the catastrophic
mothership tail. This round puts a lumped-parameter envelope around the
physics — it does NOT resolve stability (that needs a 6-DOF coupled sim,
named as the follow-on with the Basilisk module identified).

Lumped model (two timescales):
  1. CONTACT: capture arrests the closing rate v_c through an effective
     soft-capture stiffness k_c and the participating mass m_eff. Peak
     force F = v_c*sqrt(k_c*m_eff); arrest impulse J = m_eff*v_c.
  2. SLOSH: after contact the water keeps moving. A fraction f_s of the
     40 t sloshes as a spring-mass-damper (the classic first-mode slosh
     analog) at period T_s set by the bag's elastic restoring stiffness
     (microgravity: no gravity restoring — bag membrane tension only,
     so T_s is LONG and design-dependent; swept 10-300 s). Disturbance
     torque on the hub = m_s*x_s*omega_s^2*r_off; settling ~ 4/(zeta*omega_s).

The load (40 t) vs the mothership (4 t relay bus .. 20 t monolithic) is
a mass ratio >= 2 — the slosh mass EXCEEDS the host. This is the crux:
bag dynamics is not a small perturbation on the mothership; it is the
dominant body. "The tail wags the dog."

Anchors: water chunk 40 t, rho 1000 -> V 40 m^3 -> R_bag 2.12 m; berthing
rates 0.01-0.1 m/s (ISS berthing ~0.01-0.03, docking ~0.05-0.1); slosh
first-mode mass fraction 0.3-0.7 (classic); slosh damping zeta 0.01-0.1
(bare liquid .. lightly baffled); ACS bandwidth 0.01-0.1 Hz (large s/c);
reaction-wheel authority ~5 N*m, thruster ~50 N*m (representative);
berth window ~ tens of minutes (R185 stage). Grids SPAN run.py (R182).
"""
import math

M_WATER = 40_000.0
RHO = 1000.0
V = M_WATER / RHO
R_BAG = (3.0 * V / (4.0 * math.pi)) ** (1.0 / 3.0)
V_C = (0.01, 0.05, 0.10)               # berthing closing rates, m/s
K_C = (1e3, 1e4, 1e5)                  # soft-capture stiffness, N/m
F_S_FRAC = 0.5                         # first-mode slosh mass fraction
T_S = (10.0, 100.0, 300.0)            # slosh period band, s
ZETA = (0.01, 0.05, 0.10)
ACS_BW = (0.01, 0.10)                  # Hz
RW_AUTH, THR_AUTH = 5.0, 50.0          # N*m
BERTH_WINDOW = 30.0 * 60.0             # s
MS_DRY = {"relay_bus": 4_000.0, "monolithic": 20_000.0}
R_OFF = 2.0                            # slosh CoM offset from hub, m
X_S = 0.10                             # representative slosh amplitude, m

print(f"bag: {M_WATER/1e3:.0f} t water, V {V:.0f} m^3, R_bag {R_BAG:.2f} m")

# --- H1: contact force + impulse ---
print("\n== H1: capture contact envelope ==")
m_s = F_S_FRAC * M_WATER
for v_c in V_C:
    for k_c in K_C:
        f_peak = v_c * math.sqrt(k_c * M_WATER)
        tau = math.pi * math.sqrt(M_WATER / k_c)
        print(f"  v_c {v_c:.2f} m/s, k_c {k_c:.0e}: F_peak {f_peak/1e3:6.1f} kN, "
              f"contact {tau:5.1f} s, arrest impulse {M_WATER*v_c/1e3:.1f} kN*s")

# --- H2: slosh frequency vs ACS bandwidth ---
print("\n== H2: slosh frequency vs ACS bandwidth ==")
for t_s in T_S:
    f = 1.0 / t_s
    overlap = ACS_BW[0] <= f <= ACS_BW[1]
    print(f"  T_s {t_s:5.0f} s -> f {f:.3f} Hz  "
          f"{'OVERLAPS ACS (0.01-0.1 Hz) — CSI risk' if overlap else 'outside ACS band'}")

# --- H3: mass ratio + disturbance torque ---
print("\n== H3: mass-ratio dominance + disturbance torque ==")
for name, m_dry in MS_DRY.items():
    print(f"  vs {name} ({m_dry/1e3:.0f} t): mass ratio "
          f"{M_WATER/m_dry:.1f}:1 (slosh mass {m_s/1e3:.0f} t "
          f"{'EXCEEDS' if m_s > m_dry else 'below'} host dry)")
for t_s in T_S:
    w = 2 * math.pi / t_s
    torque = m_s * X_S * w ** 2 * R_OFF
    need = ("within RW" if torque < RW_AUTH else
            "needs thrusters" if torque < THR_AUTH else "EXCEEDS thrusters")
    print(f"  T_s {t_s:5.0f} s: disturbance torque {torque:7.1f} N*m -> {need}")

# --- H4: settling vs berth window, and the viable-corner fraction ---
print("\n== H4: slosh settling vs berth window ==")
for t_s in (100.0, 300.0):
    w = 2 * math.pi / t_s
    for zeta in ZETA:
        t_set = 4.0 / (zeta * w)
        print(f"  T_s {t_s:.0f}s, zeta {zeta:.2f}: settle {t_set/60:5.1f} min "
              f"({'> berth window (30 min) — mate an oscillating load' if t_set > BERTH_WINDOW else 'within window'})")

# is there a comfortable corner (RW-controllable AND settles in-window)?
grid_ts = [10 + i * (300 - 10) / 24 for i in range(25)]
grid_z = [0.01 + i * (0.10 - 0.01) / 14 for i in range(15)]
tot = rw_ok = thr_ok = 0
for t_s in grid_ts:
    w = 2 * math.pi / t_s
    torque = m_s * X_S * w ** 2 * R_OFF
    for zeta in grid_z:
        t_set = 4.0 / (zeta * w)
        tot += 1
        if t_set <= BERTH_WINDOW and torque <= RW_AUTH:
            rw_ok += 1
        if t_set <= BERTH_WINDOW and torque <= THR_AUTH:
            thr_ok += 1
print(f"\n  viable corner (settle<30min AND RW-controllable): "
      f"{rw_ok}/{tot} = {rw_ok/tot*100:.0f}% of the T_s x zeta grid")
print(f"  relaxed (settle<30min AND thruster-controllable): "
      f"{thr_ok}/{tot} = {thr_ok/tot*100:.0f}%")
print("  -> narrow, and it PRESCRIBES bag design (moderate compliance +")
print("     zeta>=0.1 baffling) unprecedented at 40 t. Desk bounds the")
print("     envelope; coupled STABILITY needs a Basilisk 6-DOF sim")
print("     (linearSpringMassDamper slosh particles coupled to the ACS).")
