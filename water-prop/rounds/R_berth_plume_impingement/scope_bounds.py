#!/usr/bin/env python3
"""Pre-script: R-berth-plume-impingement bounds.

THE PIVOT of the momentum-management trade (R-berth-momentum-management, b3b579c):
the A-vs-B-vs-C ranking hinges on whether firing the water cold-gas RCS to dump
the ~5000 N.m.s berth injection (leg A) damages or re-perturbs the just-settled
40 t bag (Vectran laminate + 50 kg aerogel intake) berthed a few metres forward.
  - If plume is BENIGN -> leg A is robust, CMG/GG (legs B/C) are optional risk
    reduction, and the whole trade collapses to "fire the thrusters (with a
    thruster-placement constraint)."
  - If plume DAMAGES/re-excites the bag -> leg C (geometry control) or B (GG
    desat) become mandatory, and the ~300-600 kg CMG / days-cadence cost is real.

Three failure modes tested:
  (1) mechanical  -- plume pressure vs Vectran/aerogel structural limits
  (2) re-perturb  -- plume torque on the bag vs the dump torque we just settled
  (3) icing       -- cumulative water-ice deposition on the aerogel intake over N

Plume model (parametrized far-field momentum flux; NOT DSMC -- see bug-catch):
  thrust per thruster F; exhaust v_e = Isp*g0; mdot = F/v_e.
  isotropic-over-forward-hemisphere reference pressure  P_iso(r) = F/(2 pi r^2)
  core (bag in exhaust direction):     P_core = kappa * P_iso,  kappa in [2,6]
  backflow (bag at theta>90 deg):      P_bf   = beta  * P_iso,  beta  in [2e-3,3e-2]
  For a momentum-dump COUPLE the thrusters fire tangentially; a 12-corner-thruster
  layout can keep the bag in BACKFLOW for most dump axes (design constraint).

Grids here SPAN the run grids: F in {3,5,10} N, r in {2,3,5,10} m,
kappa in {2,4,6}, beta in {2e-3,1e-2,3e-2}, N in {10,30,50}.
"""
import math

G0 = 9.80665
ISP_CG = 70.0                 # s, water cold-gas (spec / R_chunk_despin_budget)
V_E = ISP_CG * G0             # 687 m/s
# dump: tau ~ 50 N.m (sim); arm d_rcs in [5,15] m -> F in [3.3,10] N
F_GRID = (3.0, 5.0, 10.0)
R_GRID = (2.0, 3.0, 5.0, 10.0)          # bag standoff (grapple-boom length)
KAPPA = (2.0, 4.0, 6.0)                 # core peaking (momentum flux vs isotropic)
BETA = (2e-3, 1e-2, 3e-2)               # backflow / isotropic pressure ratio
BETA_M = (1e-4, 1e-3, 1e-2)             # backflow MASS fraction
N_BERTHS = (10, 30, 50)

# structural limits (conservative)
P_DAMAGE = 1.0e4              # Pa; aerogel compressive ~10 kPa (lower than Vectran)
# re-perturbation: plume torque must stay below 5% of the dump torque
TAU_DUMP = 50.0              # N.m (sim)
TAU_REPERTURB = 0.05 * TAU_DUMP        # 2.5 N.m
# geometry
A_BAG = 50.0                 # m^2 bag frontal (char length ~8 m)
R_OFF = 5.0                  # m bag arm
THETA_CORE = math.radians(25.0)        # plume core half-angle
F_INTAKE = (0.05, 0.10, 0.20)          # fraction of backflow hemisphere on intake
M_INTAKE = 50.0              # kg aerogel intake (SATURN-SHIP-SPEC.md line 40)
STICK = 1.0                  # cold-surface sticking coefficient (worst case)
T_DUMP = 100.0              # s per dump (sim: 5000 N.m.s at 50 N.m)


def p_iso(F, r):
    return F / (2 * math.pi * r ** 2)


print("=" * 72)
print("Anchors")
print("=" * 72)
print(f"  v_e (cold-gas water)              = {V_E:.0f} m/s")
print(f"  mdot @ F=5 N                      = {5.0/V_E*1e3:.2f} g/s")
print(f"  dump torque / time               = {TAU_DUMP:.0f} N.m / {T_DUMP:.0f} s")
print(f"  P_iso @ F=5,r=2                   = {p_iso(5,2):.3f} Pa")

print()
print("=" * 72)
print("H1 [S] -- plume pressure << structural limits: NO fabric/aerogel damage")
print("=" * 72)
p_core_max = KAPPA[-1] * p_iso(F_GRID[-1], R_GRID[0])   # worst: F=10,r=2,kappa=6
print(f"  worst-case CORE pressure (F=10,r=2 m,kappa=6) = {p_core_max:.2f} Pa")
print(f"  aerogel/Vectran conservative damage limit     = {P_DAMAGE:.0f} Pa")
print(f"  margin = {P_DAMAGE/p_core_max:.0f}x ({math.log10(P_DAMAGE/p_core_max):.1f} orders)")
print(f"  SCOPE: worst core pressure < 0.01*P_DAMAGE (100 Pa). Falsified if core")
print(f"  pressure at min standoff >= 100 Pa (approaches structural concern).")

print()
print("=" * 72)
print("H2 [S] -- with the bag in BACKFLOW, plume torque << dump torque: does NOT")
print("          re-excite the just-settled slosh/attitude")
print("=" * 72)
# operating point: bag in backflow, r>=3 m, central beta
tau_bf_op = BETA[1] * p_iso(F_GRID[1], 3.0) * A_BAG * R_OFF
tau_bf_worst = BETA[-1] * p_iso(F_GRID[-1], R_GRID[0]) * A_BAG * R_OFF
# core geometry (design constraint if unavoidable):
a_illum = math.pi * (R_GRID[0] * math.tan(THETA_CORE)) ** 2
tau_core = KAPPA[1] * p_iso(F_GRID[1], R_GRID[0]) * a_illum * R_OFF
print(f"  operating (backflow, r=3 m, beta=1e-2): tau_plume = {tau_bf_op:.2f} N.m")
print(f"  stress corner (backflow, r=2 m, beta=3e-2, F=10): {tau_bf_worst:.2f} N.m")
print(f"  re-perturbation threshold (5% of dump)         = {TAU_REPERTURB:.1f} N.m")
print(f"  [design constraint] if bag in CORE (r=2 m):     {tau_core:.1f} N.m "
      f"(~{tau_core/TAU_DUMP*100:.0f}% of dump -> WOULD re-excite)")
print(f"  SCOPE: backflow tau_plume < 2.5 N.m at operating point. Falsified if")
print(f"  backflow tau >= 2.5 N.m, OR if backflow geometry is unachievable so the")
print(f"  bag sits in the plume core (then leg C/B mandatory).")

print()
print("=" * 72)
print("H3 [S] -- cumulative water-ice on the aerogel intake over N berths is")
print("          grams: does NOT clog the soft-capture intake")
print("=" * 72)
# per dump: 2 thrusters, backflow mass fraction, fraction onto intake, sticking
for N in (N_BERTHS[1],):
    m_ice = 2 * (F_GRID[1] / V_E) * T_DUMP * BETA_M[1] * F_INTAKE[1] * STICK * N
m_ice_worst = 2 * (F_GRID[-1] / V_E) * T_DUMP * BETA_M[-1] * F_INTAKE[-1] * STICK * N_BERTHS[-1]
print(f"  central (F=5,beta_m=1e-3,f_intake=0.1,N=30): ice = {m_ice*1e3:.2f} g "
      f"({m_ice/M_INTAKE*100:.4f}% of 50 kg intake)")
print(f"  stress corner (F=10,beta_m=1e-2,f=0.2,N=50): ice = {m_ice_worst*1e3:.0f} g "
      f"({m_ice_worst/M_INTAKE*100:.3f}% of intake)")
print(f"  SCOPE: cumulative ice < 1% of intake mass (500 g) across the grid.")
print(f"  Falsified if deposition >= 500 g (clog threshold) OR the intake sits in")
print(f"  the plume core (deposition x kappa/beta ~ 100-1000x).")

print()
print("=" * 72)
print("H4 [W] -- synthesis: with a backflow-keeping thruster placement (feasible")
print("          with 12 corner thrusters for most dump axes), plume is NOT a")
print("          showstopper -> leg A robust; CMG/GG optional")
print("=" * 72)
print(f"  If H1-H3 hold (bag in backflow): leg A (thruster dump) survives with a")
print(f"  thruster-PLACEMENT constraint; the ~300-600 kg CMG (leg B) and the")
print(f"  geometry-control capture (leg C) become optional risk reduction, not")
print(f"  mandatory. The trade collapses to 'fire the thrusters, place them so the")
print(f"  bag is in backflow.'")
print(f"  SCOPE: plume benign at operating point AND a worst-case dump axis does")
print(f"  not force >50% core illumination of the bag. Falsified if some dump axis")
print(f"  unavoidably puts the bag in the plume core (then leg C/B mandatory, and")
print(f"  the momentum-management cost is real).")
