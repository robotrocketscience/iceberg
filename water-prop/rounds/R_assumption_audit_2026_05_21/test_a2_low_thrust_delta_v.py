"""A2 audit test: low-thrust spiral delta-v reality check.

Framework anchor: LOW_THRUST_TOTAL_DV_KM_S = 13.0 km/s for LEO -> Saturn
approach at v_inf = 0.5 km/s (per phase1_leo_to_saturn.py).

Hypothesis: 13 km/s is enough for pure low-thrust spiral from LEO to
Saturn approach.

Test method: compute the Edelbaum analytical bound for circular-to-
circular spiral transfer. This is the LOWER bound on integrated thrust
delta-v for low-thrust mission designs. Real optimized trajectories can
beat the simple Edelbaum bound by ~5-15 percent using phase-optimal
control, but cannot beat it by 2x.

Edelbaum result for circular-to-circular coplanar spiral:
    delta_v = v_initial - v_final
where v_initial and v_final are circular orbital velocities at the two
radii.

For LEO -> Saturn approach (broken into Earth-bound spiral escape +
heliocentric transfer + Saturn-bound spiral capture):
"""

import math


def circular_velocity(mu_km3_s2, radius_km):
    return math.sqrt(mu_km3_s2 / radius_km)


# Earth-bound parameters
MU_EARTH = 398_600.0  # km^3/s^2
R_LEO = 6_678.0  # km (200 km altitude)

# Heliocentric parameters
MU_SUN = 1.32712e11  # km^3/s^2
AU_KM = 1.496e8
R_EARTH_ORBIT = 1.0 * AU_KM
R_SATURN_ORBIT = 9.58 * AU_KM

# Saturn-bound parameters
MU_SATURN = 3.7931e7  # km^3/s^2
R_SATURN_LOW_ORBIT = 70_000.0  # km (above F-ring at ~75,000 km Saturn radius + 70k orbit)


def edelbaum_circular_spiral(v_initial_km_s, v_final_km_s):
    """Edelbaum analytical bound for circular-to-circular coplanar
    low-thrust spiral. Returns absolute value of velocity difference."""
    return abs(v_initial_km_s - v_final_km_s)


def main():
    print("=" * 70)
    print("A2 low-thrust spiral delta-v audit")
    print("=" * 70)
    print()

    # Phase 1: Earth-bound spiral escape from LEO
    v_leo = circular_velocity(MU_EARTH, R_LEO)
    # "Final velocity" for escape is 0 (just barely escapes at infinity)
    earth_escape_dv = edelbaum_circular_spiral(v_leo, 0.0)
    print(f"Phase A — Earth-bound spiral escape from LEO:")
    print(f"  v_LEO circular = {v_leo:.3f} km/s")
    print(f"  Edelbaum delta-v to escape = {earth_escape_dv:.3f} km/s")
    print()

    # Phase 2: Heliocentric transfer Earth orbit -> Saturn orbit
    v_earth_heliocentric = circular_velocity(MU_SUN, R_EARTH_ORBIT)
    v_saturn_heliocentric = circular_velocity(MU_SUN, R_SATURN_ORBIT)
    heliocentric_dv = edelbaum_circular_spiral(v_earth_heliocentric, v_saturn_heliocentric)
    print(f"Phase B — Heliocentric Earth-orbit to Saturn-orbit spiral:")
    print(f"  v_Earth heliocentric = {v_earth_heliocentric:.3f} km/s")
    print(f"  v_Saturn heliocentric = {v_saturn_heliocentric:.3f} km/s")
    print(f"  Edelbaum heliocentric delta-v = {heliocentric_dv:.3f} km/s")
    print()

    # Phase 3: Saturn-bound spiral capture from approach
    # If vehicle arrives at v_inf ~ 0 (low-thrust spiral leaves residual
    # ~0.5 km/s), it needs to capture into a low-Saturn orbit at LSO.
    v_lso = circular_velocity(MU_SATURN, R_SATURN_LOW_ORBIT)
    # Approximate: low-thrust spiral capture from co-orbital to LSO
    saturn_capture_dv = v_lso  # spiral down from co-orbital (v_inf=0) to LSO
    print(f"Phase C — Saturn-bound spiral capture (co-orbital to low-Saturn-orbit):")
    print(f"  v_LSO at 70,000 km Saturn radius = {v_lso:.3f} km/s")
    print(f"  Edelbaum spiral capture delta-v = {saturn_capture_dv:.3f} km/s")
    print(f"  (note: this is the Phase 2 Saturn-capture leg, not the Phase 1 LEO-to-Saturn-approach leg)")
    print()

    # Phase 1 framework anchor: LEO -> Saturn approach (NOT including capture)
    framework_anchor_dv = 13.0
    edelbaum_phase1_total = earth_escape_dv + heliocentric_dv
    print(f"=" * 70)
    print(f"Framework anchor (Phase 1 only, LEO -> Saturn approach):")
    print(f"  LOW_THRUST_TOTAL_DV_KM_S = {framework_anchor_dv} km/s")
    print()
    print(f"Edelbaum analytical lower bound (Phase A + Phase B):")
    print(f"  {earth_escape_dv:.2f} + {heliocentric_dv:.2f} = {edelbaum_phase1_total:.2f} km/s")
    print()
    print(f"Ratio (anchor / Edelbaum): {framework_anchor_dv / edelbaum_phase1_total:.3f}")
    print(f"Discrepancy: {edelbaum_phase1_total - framework_anchor_dv:.2f} km/s "
          f"({(edelbaum_phase1_total / framework_anchor_dv - 1) * 100:.0f} percent MORE delta-v needed)")
    print()

    # Implications: how much propellant does this need at 3000 s specific impulse?
    isp = 3000.0
    g0 = 9.81e-3  # km/s^2
    exhaust = isp * g0

    prop_fraction_anchor = 1 - math.exp(-framework_anchor_dv / exhaust)
    prop_fraction_real = 1 - math.exp(-edelbaum_phase1_total / exhaust)

    print(f"Propellant fraction needed at 3000 s electric specific impulse:")
    print(f"  Anchor (13 km/s):           {prop_fraction_anchor * 100:.1f} percent")
    print(f"  Edelbaum bound (~28 km/s):  {prop_fraction_real * 100:.1f} percent")
    print()
    print(f"Vehicle dry + payload + chunk-grab fraction available:")
    print(f"  Anchor:           {(1 - prop_fraction_anchor) * 100:.1f} percent of launch manifest")
    print(f"  Edelbaum bound:   {(1 - prop_fraction_real) * 100:.1f} percent of launch manifest")
    print()

    # Could a chemical kick reduce the spiral burden?
    # Real-world: chemical kick stage can provide ~3-5 km/s of TSI,
    # leaving the low-thrust spiral to cover the rest.
    chemical_kick_dv = 4.0
    spiral_after_kick = edelbaum_phase1_total - chemical_kick_dv
    print(f"=" * 70)
    print(f"With a {chemical_kick_dv} km/s chemical kick stage in addition to low-thrust:")
    print(f"  Spiral component reduces to: {spiral_after_kick:.2f} km/s")
    print(f"  Propellant fraction (spiral): {(1 - math.exp(-spiral_after_kick / exhaust)) * 100:.1f} percent")
    print(f"  Still {spiral_after_kick / framework_anchor_dv:.2f}x the framework anchor.")


if __name__ == "__main__":
    main()
