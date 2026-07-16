"""Patched-conic two-body gravity-assist mechanics for an Earth-Moon
braking tour.

This is the simplest credible model for a lunar gravity assist sequence used
to brake a spacecraft arriving at Earth from a heliocentric transfer:

  1. Treat each lunar encounter as an instantaneous velocity rotation in the
     Moon-centered frame (patched-conic two-body).
  2. Between encounters, propagate the spacecraft as an Earth-centered
     Keplerian orbit (not modeled here -- we sweep over arrival epoch and
     flyby geometry instead).
  3. The lunar orbital plane and the inbound trajectory plane have a
     relative inclination that varies with epoch (the 18.6-year nodal
     regression cycle). We model this with a scalar "inclination penalty"
     cos(angle) on the in-plane component of the braking Delta-V.

What this captures:
  - The fast-flyby small-turning-angle regime: at v_inf ~ 6 km/s, the
    maximum turn at minimum altitude is only ~10 degrees, NOT 180.
  - The Moon's orbital motion (1.022 km/s) sets the maximum theoretical
    Earth-frame braking per flyby.
  - Sequential flybys compound favorably: as v_inf_earth drops, v_inf_moon
    can rise, the turn angle grows, and per-flyby braking grows.

What this does NOT capture:
  - Real Earth-Moon trajectory geometry between flybys (phasing orbits).
  - Out-of-plane (true three-dimensional) flyby effects beyond a scalar
    inclination penalty.
  - Finite-thrust effects during the flyby itself.
  - Patched-conic boundary errors.

References to verify in a later round:
  - Folta and Beckman, "Lunar gravity-assist trajectories for Earth-Moon
    system missions," NASA Goddard 2002.
  - Uphoff and Crouch, "Lunar cycler orbits...", Jet Propulsion Laboratory
    1993.
"""

from __future__ import annotations

import numpy as np

# Lunar constants
GM_MOON = 4902.800066                # km^3 / s^2 (gravitational parameter)
R_MOON = 1737.4                       # km (mean radius)
V_MOON_ORBITAL = 1.0220               # km / s (Moon's mean orbital speed around Earth)
R_LUNAR_ORBIT = 384400.0              # km (mean Earth-Moon distance)

# Earth constants (relevant for the spacecraft state at lunar distance)
GM_EARTH_KM3_S2 = 398600.4418         # km^3 / s^2


def v_sc_earth_at_lunar_distance(v_inf_earth_km_s: float) -> float:
    """Spacecraft speed in Earth's frame at lunar orbital distance, assuming
    it's arriving from infinity with v_inf = v_inf_earth.

    From energy conservation:
      (1/2) v^2 - GM_earth / r = (1/2) v_inf^2
      v = sqrt(v_inf^2 + 2 GM_earth / r)
    """
    return float(np.sqrt(v_inf_earth_km_s ** 2 + 2.0 * GM_EARTH_KM3_S2 / R_LUNAR_ORBIT))


def turning_angle(v_inf_moon_km_s: float, periapsis_altitude_km: float) -> float:
    """Gravity-turn angle (radians) for a hyperbolic flyby at the Moon.

    For a hyperbolic trajectory with periapsis radius r_p and incoming
    speed v_inf at infinity (relative to the Moon):
      eccentricity e = 1 + r_p * v_inf^2 / GM
      turning angle delta = 2 arcsin(1/e)
    """
    r_p_km = R_MOON + periapsis_altitude_km
    e = 1.0 + r_p_km * v_inf_moon_km_s ** 2 / GM_MOON
    return 2.0 * float(np.arcsin(1.0 / e))


def single_flyby_braking(
    v_inf_earth_in_km_s: float,
    periapsis_altitude_km: float,
    inclination_deg: float = 0.0,
) -> tuple[float, float]:
    """One maximum-braking lunar flyby.

    Approximate planar model: the spacecraft arrives at the Moon with
    Earth-frame velocity oriented optimally for braking (anti-parallel to
    the Moon's orbital velocity). In the Moon's frame, the gravity turn
    rotates the velocity vector by `delta`. For maximum braking, the
    rotation is oriented to take the outgoing v_inf_moon as anti-parallel
    to v_moon_orbital as the geometry permits.

    Inclination penalty: when the inbound trajectory plane and the Moon's
    orbital plane have a relative inclination phi, only the in-plane
    component of the braking Delta-V is realized. Penalty factor = cos(phi).

    Args:
      v_inf_earth_in_km_s: spacecraft v_inf relative to Earth before flyby
      periapsis_altitude_km: altitude above the lunar surface at periapsis
      inclination_deg: angle between inbound trajectory plane and the
                       Moon's orbital plane (0 = favorable, 90 = no
                       braking gain)

    Returns:
      (v_inf_earth_out_km_s, delta_v_earth_km_s): new Earth-frame v_inf
      and the magnitude of the braking Delta-V applied to the spacecraft.
    """
    U = v_inf_earth_in_km_s  # shorthand
    vM = V_MOON_ORBITAL

    # Spacecraft speed in Earth's frame at the Moon's orbital distance.
    v_sc_earth = v_sc_earth_at_lunar_distance(U)

    # Optimal-braking geometry in the planar coplanar case: approach the
    # Moon from the leading side so that v_inf_moon = v_sc_earth + v_moon.
    # In practice the geometry is constrained, but this is the theoretical
    # best-case for a single flyby.
    v_inf_moon = v_sc_earth + vM

    # Gravity turn angle in the Moon's frame.
    delta = turning_angle(v_inf_moon, periapsis_altitude_km)

    # Magnitude of the velocity change in the Moon's frame from the turn.
    delta_v_moon_frame = 2.0 * v_inf_moon * np.sin(delta / 2.0)

    # In the Earth's frame, the maximum useful component is along the
    # direction anti-parallel to v_moon. With proper alignment in the
    # planar case, this is the same magnitude as delta_v_moon_frame.
    # With out-of-plane inclination phi, only cos(phi) of this component
    # contributes to Earth-frame braking.
    incl_rad = np.deg2rad(inclination_deg)
    delta_v_earth = delta_v_moon_frame * np.cos(incl_rad)

    # New v_inf in Earth's frame after braking.
    v_inf_earth_out = max(0.0, U - delta_v_earth)

    return float(v_inf_earth_out), float(delta_v_earth)


def three_flyby_tour(
    v_inf_initial_km_s: float,
    periapsis_altitude_km: float,
    inclination_deg: float = 0.0,
) -> dict:
    """Three sequential maximum-braking lunar flybys.

    Each flyby reduces v_inf_earth; the next flyby starts from the reduced
    value. Subsequent flybys typically deliver more Delta-V because v_inf_moon
    drops, the turn angle grows, and the gravity assist becomes more
    effective.

    Returns:
      dict with per-flyby and total Delta-V values.
    """
    v_inf = v_inf_initial_km_s
    per_flyby = []
    total_delta_v = 0.0
    for i in range(3):
        v_inf_new, dv = single_flyby_braking(v_inf, periapsis_altitude_km, inclination_deg)
        per_flyby.append({
            "flyby_number": i + 1,
            "v_inf_in_km_s": v_inf,
            "v_inf_out_km_s": v_inf_new,
            "delta_v_km_s": dv,
        })
        total_delta_v += dv
        v_inf = v_inf_new
    return {
        "v_inf_initial_km_s": v_inf_initial_km_s,
        "v_inf_final_km_s": v_inf,
        "total_delta_v_km_s": total_delta_v,
        "periapsis_altitude_km": periapsis_altitude_km,
        "inclination_deg": inclination_deg,
        "per_flyby": per_flyby,
    }
