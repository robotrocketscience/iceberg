#!/usr/bin/env python3
"""Pre-script: R-lowthrust-spiral-departure bounds.

Reproduces R179's impulsive single-burn departure Δv, the analytic v_circ
low-thrust spiral escape, and the rocket-equation reactor-floor scaling. Does
NOT run the numerical spiral integration or the Isp sweep (run.py).

Claim under test: R179's 175 kWe departure floor uses an IMPULSIVE-Oberth Δv
(9.0 km/s ~ hyp_v(ring,v∞) − v_circ) fed through a CONTINUOUS-THRUST electric
powerplant. A low-thrust electric departure cannot exploit Oberth; it spirals,
paying Δv ~ v_circ ~ 18.8 km/s (~2x), which through the rocket equation
multiplies the floor several-fold.
"""
import math

G0 = 9.80665
MU_S = 3.793e16        # m^3/s^2  (Saturn; R179)
R_RING = 1.07e8        # m        (B-ring; R179)
VINF = 6210.0          # m/s      (campaign departure v_inf)
VE_MET = 800.0 * G0    # m/s      (water electrothermal, R179)
ETA = 0.6              # R179
YEAR = 3.156e7         # s        R179
M_F = 100_000.0        # kg final mass (R179)
BURN_YEARS = 2.0


def vis(r, a):
    return math.sqrt(MU_S * (2.0 / r - 1.0 / a))


def hyp_v(r, vinf):
    return math.sqrt(vinf ** 2 + 2.0 * MU_S / r)


def reactor_kwe(dv, m_f=M_F, ve=VE_MET, burn_years=BURN_YEARS):
    prop = m_f * (math.exp(dv / ve) - 1.0)
    return 0.5 * ve ** 2 * prop / ETA / (burn_years * YEAR) / 1e3


V_CIRC = vis(R_RING, R_RING)
V_ESC = math.sqrt(2 * MU_S / R_RING)
DV_IMPULSIVE = hyp_v(R_RING, VINF) - V_CIRC
DV_SPIRAL_ESC = V_CIRC                       # low-thrust escape (to parabolic)
DV_SPIRAL_TOT = V_CIRC + VINF                # + hyperbolic completion (upper)

print("=" * 68)
print("H-C1 [S] -- R179's 9.0 km/s is the IMPULSIVE single-burn, not a spiral")
print("=" * 68)
print(f"    v_circ(B-ring)      = {V_CIRC:8.0f} m/s = {V_CIRC/1000:.2f} km/s")
print(f"    v_esc(B-ring)       = {V_ESC:8.0f} m/s = {V_ESC/1000:.2f} km/s")
print(f"    impulsive single    = hyp_v - v_circ = {DV_IMPULSIVE:.0f} m/s "
      f"= {DV_IMPULSIVE/1000:.2f} km/s")
print(f"    R179 chunk_fed_9.0  = 9000 m/s  -> matches impulsive within "
      f"{100*abs(9000-DV_IMPULSIVE)/DV_IMPULSIVE:.0f}% (rounding)")
print(f"    SCOPE: |9.0 - impulsive| < 30%. Falsified if > 30% (9.0 was a spiral).")

print()
print("=" * 68)
print("H-C2 [S] -- honest low-thrust spiral departure Δv >= v_circ (~2x R179 9.0)")
print("=" * 68)
print(f"    spiral escape (to parabolic) = v_circ = {DV_SPIRAL_ESC/1000:.2f} km/s")
print(f"    + hyperbolic v_inf completion -> total in "
      f"[{DV_SPIRAL_ESC/1000:.1f}, {DV_SPIRAL_TOT/1000:.1f}] km/s")
print(f"    ratio to R179 9.0 km/s: {DV_SPIRAL_ESC/9000:.2f}x - {DV_SPIRAL_TOT/9000:.2f}x")
print(f"    SCOPE: honest spiral Δv >= 15 km/s. Falsified if < 15 km/s.")

print()
print("=" * 68)
print("H-C3 [S] -- honest spiral Δv raises the departure reactor floor to >=500 kWe")
print("=" * 68)
for tag, dv in (("impulsive 8.5 (R179)", DV_IMPULSIVE),
                ("R179 hardcoded 9.0", 9000.0),
                ("spiral escape v_circ 18.8", DV_SPIRAL_ESC),
                ("spiral total v_circ+v_inf 25.0", DV_SPIRAL_TOT)):
    p = reactor_kwe(dv)
    print(f"    Δv {tag:32} -> {p:7.0f} kWe  ({p/reactor_kwe(9000.0):.2f}x R179)")
print(f"    SCOPE: floor at honest spiral Δv >= 500 kWe (pred ~810 at v_circ,")
print(f"    ~1900 at v_circ+v_inf). Falsified if < 300 kWe.")

print()
print("=" * 68)
print("Alternative: hold 175 kWe, let burn time absorb the higher Δv")
print("=" * 68)
# burn time scales with prop (exp(dv/ve)-1) at fixed power
for tag, dv in (("v_circ 18.8", DV_SPIRAL_ESC), ("v_circ+v_inf 25.0", DV_SPIRAL_TOT)):
    ratio = (math.exp(dv / VE_MET) - 1) / (math.exp(9000.0 / VE_MET) - 1)
    print(f"    Δv {tag:18} at 175 kWe -> burn {BURN_YEARS*ratio:.1f} yr "
          f"(vs {BURN_YEARS:.0f} yr at 9.0 km/s)")
print(f"    -> a ~9 yr departure burn blows the round-trip ceiling AND reactor life.")

print()
print("=" * 68)
print("H-C4 [W] -- Isp sensitivity: even RF-ion 2000 s keeps floor >= 2x R179")
print("=" * 68)
for isp in (800.0, 2000.0):
    ve = isp * G0
    base = reactor_kwe(9000.0, ve=ve)
    spir = reactor_kwe(DV_SPIRAL_ESC, ve=ve)
    print(f"    Isp {isp:.0f} s: 9.0 km/s -> {base:.0f} kWe ; spiral v_circ -> "
          f"{spir:.0f} kWe ({spir/base:.2f}x)")
print(f"    SCOPE: spiral floor >= 2x the same-Isp 9.0-km/s floor. Falsified if")
print(f"    some flyable Isp keeps spiral floor within 1.3x.")
