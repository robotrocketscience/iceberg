#!/usr/bin/env python3
"""Pre-script: R-chunk-capture-closing-velocity-window bounds.

First-cut FLOOR components (spin, Hill shear, dispersion, GNC deadband) and a
first-cut mass-scaled containment CEILING, to justify the pre-registered bands in
SCOPE.md. Does NOT run the full mass x spin-percentile x fabric x ice-strength grid
(that is run.py). Deterministic.

Question the round answers: is there a feasible closing-velocity WINDOW for
multi-tonne chunk capture -- floor (achievable, ring dynamics) below ceiling
(survivable, containment structure)? Or does floor > ceiling => no operating point?
"""
import math

# --- ring / dynamics anchors ---
RHO_ICE = 500.0                    # kg/m^3 porous ring aggregate (pessimistic-large radius)
OMEGA_BRING = 2 * math.pi / (11.0 * 3600.0)   # rad/s, B-ring orbital rate (tier_0_5: 11.0 h)
# Cassini tier_0_5 spin prior, 1-10 m bin (rpm): p50 0.01, p95 0.05, fast-rotator 0.28
SPIN_RPM = {"p50": 0.01, "p95": 0.05, "fast": 0.28}
V_DISP = 1.0e-3                    # m/s local velocity dispersion (dynamically cold B-ring)
V_GNC = 1.0e-3                     # m/s GNC control deadband (conops Hill-drift anchor)

# --- fabric anchors ---
U_ZYLON = 0.5 * 5.8e9 * 0.035 / 1540.0    # J/kg toughness (0.5*sigma*eps/rho) ~ 6.6e4
U_KEVLAR = 0.5 * 3.6e9 * 0.024 / 1440.0   # ~3.0e4
SIGMA_AREAL = 0.3                  # kg/m^2 strong ripstop bag fabric
K_BAG = 2.0                        # bag area / chunk surface (need aperture > chunk)


def radius(mass_t, rho=RHO_ICE):
    return (3.0 * mass_t * 1000.0 / (4.0 * math.pi * rho)) ** (1.0 / 3.0)


def v_spin(mass_t, rpm):
    w = rpm * 2 * math.pi / 60.0
    return w * radius(mass_t)


def v_shear(mass_t):
    dr = 2.0 * radius(mass_t)                       # capture envelope ~ chunk diameter
    return 1.5 * OMEGA_BRING * dr                    # Hill shear (3/2) Omega dr


def floor_rss(mass_t, spin_key, despun=False):
    vs = 0.0 if despun else v_spin(mass_t, SPIN_RPM[spin_key])
    return math.sqrt(vs**2 + v_shear(mass_t)**2 + V_DISP**2 + V_GNC**2)


def ceiling_energy(mass_t, U=U_ZYLON, f_part=1.0, sigma=SIGMA_AREAL):
    r = radius(mass_t)
    A_bag = K_BAG * 4 * math.pi * r**2
    m_fab = sigma * A_bag * f_part
    E = U * m_fab
    return math.sqrt(2 * E / (mass_t * 1000.0))


def main():
    print("=" * 74)
    print("FLOOR components (m/s) vs chunk mass  [un-despun, p50 spin unless noted]")
    print("=" * 74)
    print(f"    Omega_Bring = {OMEGA_BRING:.3e} rad/s ; Hill shear (3/2)Omega = "
          f"{1.5*OMEGA_BRING*1000:.3f} m/s per km")
    print(f"    {'mass(t)':>8} {'r(m)':>6} {'v_spin_p50':>11} {'v_spin_p95':>11} "
          f"{'v_shear':>9} {'floor_p50':>10} {'floor_p95':>10}")
    for m in (1, 10, 50, 200):
        r = radius(m)
        print(f"    {m:>8} {r:>6.2f} {v_spin(m,SPIN_RPM['p50'])*1e3:>9.2f}mm {v_spin(m,SPIN_RPM['p95'])*1e3:>9.2f}mm "
              f"{v_shear(m)*1e3:>7.2f}mm {floor_rss(m,'p50')*1e3:>8.2f}mm {floor_rss(m,'p95')*1e3:>8.2f}mm")

    print()
    print("=" * 74)
    print("CEILING (m/s), energy limit -- strong (Zylon,whole-bag) vs pessimistic")
    print("=" * 74)
    print(f"    U_Zylon={U_ZYLON:.2e} J/kg  U_Kevlar={U_KEVLAR:.2e} J/kg")
    print(f"    {'mass(t)':>8} {'strong':>8} {'pessim(patch+light)':>20}")
    for m in (1, 10, 50, 200):
        r = radius(m)
        f_patch = math.pi * r**2 / (K_BAG * 4 * math.pi * r**2)   # = 1/(4K) = 0.125
        strong = ceiling_energy(m, U_ZYLON, 1.0, 0.3)
        pess = ceiling_energy(m, U_KEVLAR * 0.5, f_patch, 0.1)     # lightweight ~0.5*Kevlar
        print(f"    {m:>8} {strong:>7.1f}  {pess:>18.2f}")

    print()
    print("=" * 74)
    print("WINDOW ratio ceiling/floor  (pessimistic ceiling / p95 floor)")
    print("=" * 74)
    for m in (1, 10, 50, 200):
        r = radius(m)
        f_patch = 1.0 / (4 * K_BAG)
        pess = ceiling_energy(m, U_KEVLAR * 0.5, f_patch, 0.1)
        ratio = pess / floor_rss(m, 'p95')
        print(f"    mass {m:>4} t: pessim ceiling {pess:>6.2f} m/s / p95 floor "
              f"{floor_rss(m,'p95')*1e3:>6.2f} mm/s = {ratio:>8.0f}x")
    print()
    print("    SCOPE bands: floor <=30 mm/s p50 (<=150 p95); ceiling 5-30 m/s strong")
    print("    (>=1.5 pessimistic); window ceiling/floor >=100 p50, >=10 p95-pessim.")


if __name__ == "__main__":
    main()
