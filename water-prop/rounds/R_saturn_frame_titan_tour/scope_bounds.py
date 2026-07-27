#!/usr/bin/env python3
"""Pre-script: R-saturn-frame-titan-tour bounds.

Chases the crack R-ephemeris-departure-anchor opened: R186 revoked the Titan
departure-pump lever via a magnitude bound (~3.3 km/s), but the ephemeris round
showed the Saturn-centric departure excess REACHES the 5.44 km/s heliocentric
requirement at Titan-relative excess vinf_T >= 4.01 km/s. Open question: can a
patient multi-flyby Saturn-system tour actually REACH vinf_T >= 4 at Titan (and
in the right departure direction), which would partially re-open the lever and
put the Titan reactor-floor branch back on the table?

This re-hosts trajectory-bot's flyby/Tisserand primitives in a Saturn-CENTRIC
frame (Titan + Rhea + Dione + Tethys + Iapetus). Central physics:
  - vinf_T (spacecraft velocity relative to a moon at its orbit) is CONSERVED by
    that moon's flybys (Tisserand) -- flybys ROTATE vinf, they do not grow |vinf|.
  - So vinf_T is set by the ARRIVAL orbit. The spacecraft harvests at the B-ring
    (r ~ 107,000 km, deep inside Titan's 1.22e6 km orbit). The minimal transfer
    from the B-ring to a moon (periapsis at B-ring, apoapsis at the moon) fixes
    the arrival vinf at that moon.
  - Max Saturn-centric departure excess from a single-moon pump (vinf aligned
    prograde with the moon): sqrt((v_moon + vinf_moon)^2 - 2 mu_S / a_moon).
  - To grow vinf_T beyond the B-ring value you must either pre-spend propellant
    (= supplying the departure energy yourself, R186's point) or hand off to
    another moon (which conserves a DIFFERENT moon's vinf).

Grids that SPAN the run grid: moon in {Titan,Rhea,Dione,Tethys,Iapetus};
flyby peri altitude in {500,1000,2000} km; requirement 5.44 km/s.
"""
import math

MU_S = 3.793e7                 # km^3/s^2 (Saturn)
R_RING = 107_000.0             # km (B-ring, campaign R_RING 1.07e8 m)
REQ = 5.44                     # km/s heliocentric departure v_inf needed

# moon: (semi-major axis km, GM km^3/s^2, body radius km)  [Titan from
# trajectory-bot tisserand_3d; others standard JPL/IAU]
MOONS = {
    "Tethys":  (294_619.0,  41.2,   531.0),
    "Dione":   (377_396.0,  73.11,  561.4),
    "Rhea":    (527_108.0,  153.94, 763.8),
    "Titan":   (1_221_870.0, 8978.14, 2574.7),
    "Iapetus": (3_560_820.0, 120.5,  734.5),
}


def v_circ(a):
    return math.sqrt(MU_S / a)


def vinf_from_bring(a_moon):
    """spacecraft vinf relative to the moon, arriving on the minimal B-ring->moon
    transfer (periapsis at B-ring, apoapsis at the moon; tangential at apoapsis)."""
    a_t = (R_RING + a_moon) / 2.0
    v_sc_apo = math.sqrt(MU_S * (2.0 / a_moon - 1.0 / a_t))
    return v_circ(a_moon) - v_sc_apo     # both tangential, prograde


def departure_excess(a_moon, vinf_moon):
    """max Saturn-centric hyperbolic excess when the flyby aligns vinf prograde."""
    v_at = v_circ(a_moon) + vinf_moon
    arg = v_at ** 2 - 2 * MU_S / a_moon
    return math.sqrt(arg) if arg > 0 else 0.0


def delta_max(vinf, mu_moon, r_p):
    return 2.0 * math.asin(1.0 / (1.0 + r_p * vinf ** 2 / mu_moon))


print("=" * 72)
print("H1 [S] -- vinf_T reachable from the B-ring is ~3.3 km/s (Tisserand-fixed),")
print("          NOT the 4.0 the departure threshold needs")
print("=" * 72)
vinf_T = vinf_from_bring(MOONS["Titan"][0])
print(f"    v_Titan (circular)              = {v_circ(MOONS['Titan'][0]):.2f} km/s")
print(f"    spacecraft speed at Titan orbit (B-ring apoapsis) = "
      f"{v_circ(MOONS['Titan'][0]) - vinf_T:.2f} km/s")
print(f"    -> vinf_T from B-ring            = {vinf_T:.2f} km/s")
print(f"    SCOPE: vinf_T from B-ring in [3.0, 3.6] km/s (reproduces R186 ~3.3);")
print(f"    Titan flybys CONSERVE |vinf_T|, so this is the ceiling absent a burn.")
print(f"    Falsified if vinf_T from B-ring >= 4.0 (crack would be real).")

print()
print("=" * 72)
print("H2 [S] -- best single-moon departure excess is Titan ~4.1 km/s < 5.44:")
print("          the Saturn-system gravity-assist cap is short of the requirement")
print("=" * 72)
caps = {}
for name, (a, mu, R) in MOONS.items():
    vi = vinf_from_bring(a)
    de = departure_excess(a, vi)
    caps[name] = de
    print(f"    {name:8}: vinf={vi:.2f} km/s, max departure excess = {de:.2f} km/s")
best = max(caps, key=caps.get)
print(f"    -> best moon = {best} at {caps[best]:.2f} km/s (vs 5.44 required)")
print(f"    SCOPE: best single-moon departure excess in [3.8, 4.5] km/s < 5.44.")
print(f"    Falsified if any single moon reaches 5.44 km/s.")

print()
print("=" * 72)
print("H3 [S] -- inner moons and Iapetus are WORSE, not better; no moon helps")
print("=" * 72)
print(f"    inner moons (Rhea/Dione/Tethys) are deeper in Saturn's well -> need")
print(f"    more to escape -> lower departure excess despite higher v_moon.")
print(f"    Iapetus is far/slow -> lower absolute excess.")
print(f"    SCOPE: max over ALL moons < 5.0 km/s. Falsified if any >= 5.44.")

print()
print("=" * 72)
print("H4 [W] -- even the magnitude aside, reaching vinf_T=4 requires PRE-SPENDING")
print("          the departure energy (chicken-and-egg) -> R186 revocation CONFIRMED")
print("=" * 72)
# to arrive at Titan with vinf_T = 4 (instead of 3.3) needs a higher-energy orbit;
# the extra Saturn-centric speed at Titan orbit must be supplied propulsively.
v_needed_at_titan = v_circ(MOONS["Titan"][0]) - 4.0   # if slower -> higher vinf_T
# actually higher vinf_T from a MORE energetic (faster, radial) crossing:
# vinf_T=4 aligned-retro slow crossing needs v_sc = v_Titan - 4 = 1.57 (very high
# apoapsis, slow) OR a fast radial crossing. Either way the orbit differs from the
# minimal B-ring transfer and costs energy to set up.
print(f"    vinf_T from B-ring = {vinf_T:.2f}; threshold to reach 5.44 = 4.01.")
print(f"    Gap {4.01 - vinf_T:.2f} km/s of vinf_T. Titan flybys CONSERVE vinf_T,")
print(f"    so only a NON-Titan (inner-moon) handoff could pump it -- but the")
print(f"    inner moons are too small to turn the spacecraft:")
for name in ("Rhea", "Dione", "Tethys"):
    a, mu, R = MOONS[name]
    vi = vinf_from_bring(a)
    dm = math.degrees(delta_max(vi, mu, R + 1000.0))
    print(f"      {name:7}: mu={mu:6.1f} km^3/s^2 -> per-flyby turn {dm:.2f} deg "
          f"(negligible pumping)")
print(f"    -> the 0.67 km/s vinf_T gap is unbridgeable without propulsion")
print(f"    (= supplying the departure energy yourself, R186's conclusion).")
print(f"    SCOPE: best reachable departure excess < 5.44 AND inner-moon per-flyby")
print(f"    turn < 2 deg (cannot pump vinf_T). Falsified if a reachable tour hits 5.44.")
