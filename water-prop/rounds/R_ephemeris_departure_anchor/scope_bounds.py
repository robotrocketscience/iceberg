#!/usr/bin/env python3
"""Pre-script: R-ephemeris-departure-anchor bounds.

FIRST real-JPL-ephemeris round in the ICEBERG campaign. Every prior Saturn-
departure anchor was hand-derived vis-viva (5.44 km/s min-energy Hohmann; 6.21
campaign faster-transfer), carrying the flagged methodology weakness
"vis-viva-default anchoring when no primary-text source" (design-axes/04,
Methodology lesson 20). This round replaces the hand anchor with a real
ephemeris-based Lambert porkchop, using JPL Horizons state vectors (fetched via
trajectory-bot's astroquery pipeline; Saturn 699 + Earth 399, heliocentric
ecliptic, 2035-2056) and a vendored pure-numpy universal-variable Lambert
solver (Curtis Alg 5.2). It also reproduces R186's Titan-flyby pump cap from
trajectory-bot's `tisserand_3d` Titan@Saturn constants.

This scope_bounds.py computes ONLY the hand-derived prediction bands (no
porkchop): the circular-coplanar Hohmann v_inf at Saturn's REAL heliocentric
distance range (9.07-10.02 AU, from the fetched ephemeris), and the Titan
single-flyby / bound-chain pump cap. run.py then computes the real Lambert
porkchop and grades against these bands.

Grids that SPAN the run grid: r_Saturn in {9.07, 9.54, 10.02} AU (real range),
Titan flyby peri altitude in {500, 1000, 2000} km, v_inf_T in {2, 3, 4} km/s.
"""
import math

MU_SUN = 1.32712440018e11      # km^3/s^2
AU = 1.495978707e8             # km
R_E = 1.0 * AU
# Saturn real heliocentric-distance range from the fetched ephemeris (2035-2046)
R_SAT_RANGE_AU = {"perihelion 9.07": 9.07, "mean 9.54": 9.54, "aphelion 10.02": 10.02}

# Titan@Saturn constants (trajectory-bot scripts/tisserand_3d.py BODIES table)
MU_S = 3.793e7                 # km^3/s^2 (Saturn; = 3.793e16 m^3/s^2, R179)
MU_TITAN = 8978.14             # km^3/s^2
R_TITAN_BODY = 2574.7          # km
V_TITAN = 5.57                 # km/s (Titan orbital speed; = sqrt(MU_S/r_Titan_orbit))
R_TITAN_ORBIT = MU_S / V_TITAN ** 2   # km (~1.22e6)

VINF_MIN_HAND = 5.44           # km/s, hand min-energy Hohmann
VINF_CAMPAIGN = 6.21           # km/s, campaign faster-transfer anchor


def hohmann_vinf(r_S_km):
    v_S = math.sqrt(MU_SUN / r_S_km)
    a_t = (r_S_km + R_E) / 2.0
    v_aph = math.sqrt(MU_SUN * (2.0 / r_S_km - 1.0 / a_t))
    return v_S - v_aph


def delta_max(vinf_T, r_p):
    """max flyby turn angle (rad): 2 arcsin(1/(1 + r_p vinf^2 / mu))."""
    return 2.0 * math.asin(1.0 / (1.0 + r_p * vinf_T ** 2 / MU_TITAN))


def saturn_centric_vinf(vinf_T):
    """max Saturn-centric hyperbolic excess reachable when a Titan flyby chain
    aligns vinf_T with v_Titan: v_at_orbit = v_Titan + vinf_T, then
    vinf_Saturn = sqrt(v_at^2 - 2 mu_S / r_Titan_orbit)."""
    v_at = V_TITAN + vinf_T
    arg = v_at ** 2 - 2 * MU_S / R_TITAN_ORBIT
    return math.sqrt(arg) if arg > 0 else 0.0


print("=" * 72)
print("H1 [S] -- real-ephemeris min departure v_inf brackets the hand 5.44 km/s")
print("=" * 72)
band = [hohmann_vinf(a * AU) for a in (9.07, 10.02)]
for tag, a in R_SAT_RANGE_AU.items():
    print(f"    circular-coplanar Hohmann v_inf @ r_S={tag:16} AU = "
          f"{hohmann_vinf(a*AU):.3f} km/s")
print(f"    -> across Saturn's real distance range: v_inf in "
      f"[{min(band):.2f}, {max(band):.2f}] km/s (all ~5.4-5.5, tight around 5.44)")
print(f"    SCOPE: real-ephemeris porkchop MINIMUM v_inf in [5.0, 6.0] km/s")
print(f"    (inclination 2.5 deg + phasing raise it slightly above coplanar).")
print(f"    Falsified if the ephemeris minimum < 4.8 or > 6.3 (hand anchor wrong).")

print()
print("=" * 72)
print("H2 [S] -- the campaign's 6.21 km/s is a realizable faster-transfer value,")
print("          not below the achievable minimum")
print("=" * 72)
print(f"    hand min-energy 5.44 <= campaign 6.21 -> 6.21 is faster-than-minimum")
print(f"    SCOPE: 6.21 lies within the porkchop v_inf range (>= min). Falsified")
print(f"    if 6.21 < ephemeris minimum (would make 6.21 unphysically low).")

print()
print("=" * 72)
print("H3 [S] -- Titan pump cap is vinf_T-DEPENDENT: reproduces R186's ~3.3 km/s")
print("          at the natural capture-orbit vinf_T~3, but the revocation is")
print("          CONDITIONAL on vinf_T (a nuance R186's bound did not quantify)")
print("=" * 72)
print(f"    r_Titan orbit = {R_TITAN_ORBIT:.3e} km; v_Titan(check) = "
      f"{math.sqrt(MU_S/R_TITAN_ORBIT):.2f} km/s (given 5.57)")
print(f"    Saturn escape speed at Titan orbit = {math.sqrt(2*MU_S/R_TITAN_ORBIT):.2f} km/s")
for vinf_T in (2.0, 3.0, 4.0):
    r_p = R_TITAN_BODY + 1000.0
    dm = math.degrees(delta_max(vinf_T, r_p))
    vs = saturn_centric_vinf(vinf_T)
    print(f"    vinf_T={vinf_T:.0f} km/s (peri alt 1000 km): per-flyby turn "
          f"{dm:.1f} deg -> max Saturn-centric departure excess {vs:.2f} km/s")
# threshold vinf_T where the chain reaches the 5.44 requirement
vth = None
x = 3.0
while x < 5.0:
    if saturn_centric_vinf(x) >= 5.44:
        vth = x
        break
    x += 0.01
print(f"    -> Titan chain reaches the 5.44 km/s heliocentric requirement only at")
print(f"       vinf_T >= {vth:.2f} km/s (a slow, near-apoapsis Titan crossing on a")
print(f"       highly eccentric bound Saturn orbit).")
print(f"    SCOPE: (a) reproduce R186 -- cap = 3.38 km/s at the natural vinf_T=3;")
print(f"    (b) vinf_T threshold to reach 5.44 in [3.8, 4.2] km/s. FINDING (honest):")
print(f"    R186's revocation HOLDS at nominal capture-orbit vinf_T (~3) but is")
print(f"    CONDITIONAL on vinf_T <~ 3.5 -- a patient high-vinf_T Titan tour is a")
print(f"    candidate re-open R186's magnitude-bound did not address. This does NOT")
print(f"    change the reactor floor (the departure burn still supplies v_inf if")
print(f"    Titan does not), but it re-opens a design question. Falsified if the")
print(f"    cap at vinf_T=3 is NOT ~3.3 (would break the R186 reproduction).")

print()
print("=" * 72)
print("H4 [W] -- reactor floor barely moves: real v_inf vs 6.21 stays 155-175 kWe")
print("=" * 72)
# Oberth quadrature suppression (R179/R-hohmann model), reproduced in run.py
R_RING = 1.07e8               # m
VE_MET = 800 * 9.80665        # m/s
ETA, YEAR = 0.6, 3.156e7
V_CIRC = math.sqrt(3.793e16 / R_RING)


def dv_single_burn(vinf_ms):
    return math.sqrt(vinf_ms ** 2 + 2 * 3.793e16 / R_RING) - V_CIRC


def reactor_kwe(dv, m_f=100_000.0):
    prop = m_f * (math.exp(dv / VE_MET) - 1.0)
    return 0.5 * VE_MET ** 2 * prop / ETA / (2 * YEAR) / 1e3


for tag, vinf in (("hand 5.44", 5440.0), ("campaign 6.21", 6210.0)):
    print(f"    v_inf {tag}: dv={dv_single_burn(vinf)/1000:.2f} km/s -> "
          f"{reactor_kwe(dv_single_burn(vinf)):.0f} kWe")
print(f"    SCOPE: floor at the real-ephemeris min v_inf stays in [150,180] kWe")
print(f"    (Oberth quadrature suppresses the v_inf spread). Falsified if outside.")
