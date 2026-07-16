#!/usr/bin/env python3
"""
Back-of-envelope ΔV / mass-ratio / trip-time analysis for the towed-chunk
ISRU concept. Edelbaum + Tsiolkovsky + impulsive baselines.

Run: python3 saturn_isru_boe.py
"""

import math

# ---------------------------------------------------------------------------
# Constants (SI / km units)
# ---------------------------------------------------------------------------
GM_SUN    = 1.32712440018e11   # km^3/s^2
GM_EARTH  = 3.986004418e5      # km^3/s^2
GM_SATURN = 3.7931187e7        # km^3/s^2
AU        = 1.495978707e8      # km
G0        = 9.80665e-3         # km/s^2 (for Isp -> v_e in km/s)

R_EARTH   = 6378.137            # km
R_SATURN  = 60268.0             # km
ALT_LEO   = 400.0               # km
R_LEO     = R_EARTH + ALT_LEO

a_earth   = 1.0 * AU
a_saturn  = 9.5826 * AU         # Saturn semi-major axis

# Generic NEA target (representative)
a_nea     = 1.05 * AU           # near-Earth-asteroid ~1.05 AU heliocentric
v_inf_nea = 1.5                 # km/s typical NEA arrival/departure V_inf

# Power for low-thrust assumption
P_BOL_EARTH = 5000.0            # W BOL solar array sized at 1 AU
ETA         = 0.5               # MET electrical-to-jet efficiency

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def v_circ(GM, r):
    return math.sqrt(GM / r)

def v_esc(GM, r):
    return math.sqrt(2 * GM / r)

def hohmann_dv(GM, r1, r2):
    """Heliocentric Hohmann ΔV breakdown."""
    a_t = (r1 + r2) / 2
    v1  = math.sqrt(GM * (2/r1 - 1/a_t)) - math.sqrt(GM/r1)   # at r1
    v2  = math.sqrt(GM/r2) - math.sqrt(GM * (2/r2 - 1/a_t))   # at r2
    tof = math.pi * math.sqrt(a_t**3 / GM)
    return v1, v2, tof

def dv_from_orbit_to_vinf(GM, r, v_inf):
    """ΔV from circular orbit at r to hyperbolic escape with given V_inf."""
    v_p_hyp = math.sqrt(v_inf**2 + 2*GM/r)
    return v_p_hyp - math.sqrt(GM/r)

def tsiolkovsky_mass_ratio(dv_kms, isp_s):
    v_e = isp_s * G0   # km/s
    return math.exp(dv_kms / v_e)

def thrust_from_power(P, isp_s, eta=ETA):
    v_e = isp_s * G0 * 1000.0   # m/s
    F   = 2 * P * eta / v_e     # N
    return F

# ---------------------------------------------------------------------------
# 1. IMPULSIVE BASELINE — Earth -> Saturn
# ---------------------------------------------------------------------------
print("=" * 72)
print("1. IMPULSIVE BASELINE (chemical-style, instantaneous burns)")
print("=" * 72)

dv_helio_dep, dv_helio_arr, tof_helio = hohmann_dv(GM_SUN, a_earth, a_saturn)
print(f"Heliocentric Hohmann to Saturn:")
print(f"  V_inf at Earth departure = {dv_helio_dep:6.2f} km/s")
print(f"  V_inf at Saturn arrival  = {dv_helio_arr:6.2f} km/s")
print(f"  Cruise time              = {tof_helio/3.156e7:6.2f} years (one-way)")

# Earth departure from LEO
dv_leo_to_dep = dv_from_orbit_to_vinf(GM_EARTH, R_LEO, dv_helio_dep)
print(f"\nEarth-departure burn:")
print(f"  ΔV from LEO to V_inf={dv_helio_dep:.2f} km/s = {dv_leo_to_dep:6.2f} km/s")

# Saturn capture into highly elliptical (just sub-escape at r_p = 1.5 R_S)
r_p_saturn = 1.5 * R_SATURN
v_periapsis_arrival = math.sqrt(dv_helio_arr**2 + 2*GM_SATURN/r_p_saturn)
v_escape_at_rp      = v_esc(GM_SATURN, r_p_saturn)
dv_saturn_capture   = v_periapsis_arrival - v_escape_at_rp + 0.1   # +0.1 km/s margin under escape
print(f"\nSaturn capture into highly elliptical at r_p = 1.5 R_S:")
print(f"  V at periapsis on arrival  = {v_periapsis_arrival:6.2f} km/s")
print(f"  V_escape at periapsis      = {v_escape_at_rp:6.2f} km/s")
print(f"  ΔV to capture (just below escape) = {dv_saturn_capture:6.2f} km/s")

# Saturn departure from same elliptical
dv_saturn_departure = v_periapsis_arrival - v_escape_at_rp + 0.1
print(f"\nSaturn departure (mirror):")
print(f"  ΔV ≈ {dv_saturn_departure:6.2f} km/s (sym.)")

# Earth arrival - propulsive vs aerocapture
dv_earth_propulsive = dv_from_orbit_to_vinf(GM_EARTH, R_LEO, dv_helio_dep)
dv_earth_aerocap    = 0.5  # trim only
print(f"\nEarth arrival back at LEO:")
print(f"  Propulsive (full insertion) = {dv_earth_propulsive:6.2f} km/s")
print(f"  Aerocapture trim only       = {dv_earth_aerocap:6.2f} km/s")

dv_total_imp_propulsive = (dv_leo_to_dep + dv_saturn_capture + dv_saturn_departure
                           + dv_earth_propulsive)
dv_total_imp_aerocap    = (dv_leo_to_dep + dv_saturn_capture + dv_saturn_departure
                           + dv_earth_aerocap)
print(f"\n  IMPULSIVE round-trip ΔV (full propulsive) = {dv_total_imp_propulsive:6.2f} km/s")
print(f"  IMPULSIVE round-trip ΔV (aerocapture)     = {dv_total_imp_aerocap:6.2f} km/s")

# ---------------------------------------------------------------------------
# 2. LOW-THRUST EDELBAUM EQUIVALENT
# ---------------------------------------------------------------------------
print()
print("=" * 72)
print("2. LOW-THRUST (Edelbaum / continuous-spiral)")
print("=" * 72)

v_earth_helio  = math.sqrt(GM_SUN/a_earth)
v_saturn_helio = math.sqrt(GM_SUN/a_saturn)
print(f"Heliocentric circular speeds:")
print(f"  Earth      = {v_earth_helio:6.2f} km/s")
print(f"  Saturn     = {v_saturn_helio:6.2f} km/s")

# Earth escape spiral (rule of thumb: ΔV ≈ V_circ_LEO)
v_circ_leo  = v_circ(GM_EARTH, R_LEO)
dv_lt_earth_esc = v_circ_leo
print(f"\nEarth-escape spiral from LEO: ΔV ≈ V_circ = {v_circ_leo:6.2f} km/s")

# Heliocentric coplanar Edelbaum: ΔV = |v1 - v2|
dv_lt_helio = abs(v_earth_helio - v_saturn_helio)
print(f"Heliocentric Edelbaum (Earth->Saturn): ΔV = {dv_lt_helio:6.2f} km/s")

# Saturn capture spiral (NOT all the way to circular at 1.5 R_S — into high ellipse)
# For low-thrust capture into a highly elliptical Saturn orbit, the gravitational
# capture is essentially free if you arrive matched to Saturn's orbit. Add a small
# ΔV for shaping / rendezvous.
dv_lt_saturn_shape = 1.0
print(f"Saturn arrival shaping ΔV: ~{dv_lt_saturn_shape:.1f} km/s")

# Return mirror
dv_lt_return_helio = dv_lt_helio    # symmetric
dv_lt_earth_arr_aerocap = 0.5       # aerocapture trim
print(f"Return Heliocentric Edelbaum: {dv_lt_return_helio:6.2f} km/s")
print(f"Earth arrival aerocapture trim: {dv_lt_earth_arr_aerocap:6.2f} km/s")

dv_lt_total = (dv_lt_earth_esc + dv_lt_helio + dv_lt_saturn_shape
               + dv_lt_saturn_shape + dv_lt_return_helio + dv_lt_earth_arr_aerocap)
print(f"\n  LOW-THRUST round-trip ΔV (with aerocapture) = {dv_lt_total:6.2f} km/s")
print(f"  Penalty over impulsive: {dv_lt_total/dv_total_imp_aerocap:.2f}x")

# ---------------------------------------------------------------------------
# 3. MASS RATIOS — water MET vs chemical vs ion
# ---------------------------------------------------------------------------
print()
print("=" * 72)
print("3. MASS RATIO COMPARISON — outbound only")
print("=" * 72)

cases = [
    ("Chemical (LOX/RP-1)",    320,  dv_total_imp_propulsive * 0.5),  # rough split
    ("Chemical (LOX/LH2)",     450,  dv_total_imp_propulsive * 0.5),
    ("Water MET, plasma mode", 700,  dv_lt_total * 0.5),
    ("Water MET, optimistic",  900,  dv_lt_total * 0.5),
    ("Hall thruster",          1800, dv_lt_total * 0.5),
    ("Ion (NEXT-class)",       3500, dv_lt_total * 0.5),
]
print(f"{'Propulsion':<26} {'Isp [s]':>8} {'ΔV [km/s]':>10} {'Mass ratio':>11} {'Prop frac':>10}")
for name, isp, dv in cases:
    mr = tsiolkovsky_mass_ratio(dv, isp)
    pf = (mr - 1) / mr
    print(f"{name:<26} {isp:>8} {dv:>10.2f} {mr:>11.2f} {pf:>10.1%}")

# ---------------------------------------------------------------------------
# 4. THE POWER PROBLEM AT SATURN
# ---------------------------------------------------------------------------
print()
print("=" * 72)
print("4. SOLAR POWER vs HELIOCENTRIC DISTANCE")
print("=" * 72)
flux_at_earth = 1361   # W/m^2
print(f"{'Distance [AU]':<14} {'Solar flux ratio':>18} {'5kW@Earth -> ':>20}")
for r in [1.0, 1.5, 2.5, 5.2, 9.58, 19.2]:
    ratio = 1 / r**2
    print(f"{r:<14.2f} {ratio:>18.4f} {5000*ratio:>15.1f} W")

print("\nImplication: at Saturn (9.58 AU), a 5 kW Earth-orbit array produces ~55 W.")
print("That is **insufficient power for meaningful low-thrust propulsion** at Saturn.")
print("Saturn-class missions need RTG / nuclear electric power (Cassini = 880 W RTG BOL).")

# ---------------------------------------------------------------------------
# 5. THRUST + TRIP TIME
# ---------------------------------------------------------------------------
print()
print("=" * 72)
print("5. THRUST AND TRIP TIME (low-thrust spiral, Earth-region only)")
print("=" * 72)
m_dry = 1000.0  # kg
m_wet = 5000.0  # kg, outbound LEO mass
isp_test = 700
F = thrust_from_power(P_BOL_EARTH, isp_test)
m_avg = (m_dry + m_wet) / 2
a_avg = F / m_avg   # m/s^2
print(f"Assumptions: P = {P_BOL_EARTH:.0f} W, Isp = {isp_test} s, dry/wet = {m_dry:.0f}/{m_wet:.0f} kg")
print(f"Thrust: {F:.3f} N")
print(f"Average accel: {a_avg*1000:.3f} mm/s^2")

dv_outbound = dv_lt_earth_esc + dv_lt_helio   # km/s
t_outbound = (dv_outbound * 1000) / a_avg   # seconds
print(f"Outbound ΔV {dv_outbound:.2f} km/s under continuous thrust:")
print(f"  -> {t_outbound/3.156e7:.2f} years of continuous thrusting")
print("(Real missions throttle and coast; treat this as a soft upper bound.)")

# ---------------------------------------------------------------------------
# 6. THE NEA-FIRST CASE — what actually closes
# ---------------------------------------------------------------------------
print()
print("=" * 72)
print("6. NEA-FIRST CASE (round-trip to ~1.05 AU water-bearing NEA)")
print("=" * 72)
# Heliocentric Hohmann from Earth's orbit to a slightly-different orbit
dv_helio_dep_nea, dv_helio_arr_nea, tof_nea = hohmann_dv(GM_SUN, a_earth, a_nea)
print(f"Heliocentric Hohmann Earth -> NEA at {a_nea/AU:.2f} AU:")
print(f"  V_inf at Earth dep   = {dv_helio_dep_nea:6.3f} km/s")
print(f"  V_inf at NEA arrival = {dv_helio_arr_nea:6.3f} km/s")
print(f"  Cruise (one-way)     = {tof_nea/3.156e7:6.2f} years")

# LEO escape + heliocentric injection
dv_leo_dep_nea = dv_from_orbit_to_vinf(GM_EARTH, R_LEO, dv_helio_dep_nea)
# NEA rendezvous (low-gravity, basically just match V_inf)
dv_nea_match  = v_inf_nea
# Return: similar ΔV mirrored
dv_total_nea_imp = 2 * dv_leo_dep_nea + 2 * dv_nea_match
dv_total_nea_aero = dv_leo_dep_nea + 2 * dv_nea_match + 0.5  # aerocap on return
print(f"\nImpulsive round-trip from LEO (propulsive): ~{dv_total_nea_imp:6.2f} km/s")
print(f"Impulsive round-trip with aerocapture:      ~{dv_total_nea_aero:6.2f} km/s")

mr_nea_water_met = tsiolkovsky_mass_ratio(dv_total_nea_aero, 700)
print(f"\nMass ratio (water MET, Isp=700, aerocap):   {mr_nea_water_met:.2f}")
print(f"  -> Propellant fraction: {(mr_nea_water_met-1)/mr_nea_water_met:.1%}")

# Towed-chunk return leg only — this is where leverage shows up
dv_return_nea = dv_nea_match + 0.5   # depart NEA + aerocap
mr_return_nea = tsiolkovsky_mass_ratio(dv_return_nea, 700)
print(f"\nReturn-leg with chunk (aerocap): ΔV = {dv_return_nea:.2f} km/s")
print(f"  Mass ratio: {mr_return_nea:.2f}")
print(f"  Delivered fraction of grappled chunk: {1/mr_return_nea:.1%}")
print(f"  100 t grappled -> {100/mr_return_nea:.1f} t delivered to LEO depot")
print(f"  500 t grappled -> {500/mr_return_nea:.1f} t delivered")
print(f"  1000 t grappled -> {1000/mr_return_nea:.1f} t delivered")

# ---------------------------------------------------------------------------
# 7. SUMMARY / KEY FINDINGS
# ---------------------------------------------------------------------------
print()
print("=" * 72)
print("KEY FINDINGS")
print("=" * 72)
print(f"""
1. Impulsive Saturn round-trip with aerocapture:
   ~{dv_total_imp_aerocap:.1f} km/s (was 14-16 in earlier sketch — earlier sketch double-counted some legs).

2. Low-thrust Saturn round-trip:
   ~{dv_lt_total:.1f} km/s. This is a {dv_lt_total/dv_total_imp_aerocap:.1f}x penalty over impulsive.

3. Water MET at Isp=700s for the FULL Saturn round-trip:
   Mass ratio outbound alone = {tsiolkovsky_mass_ratio(dv_lt_total*0.5, 700):.1f}
   -> propellant fraction {(tsiolkovsky_mass_ratio(dv_lt_total*0.5, 700)-1)/tsiolkovsky_mass_ratio(dv_lt_total*0.5, 700):.1%}.
   The Saturn version DOES NOT CLOSE on water MET alone. Needs hybrid
   chemical for trans-Saturn injection, or higher Isp (Hall/ion), or
   nuclear-thermal/electric.

4. Solar power at Saturn (9.58 AU) is ~1.1% of Earth flux. A 5 kW Earth
   array gives ~55 W at Saturn — insufficient for low-thrust capture.
   Saturn-class water-tug needs RTG / fission power (or chemical capture).

5. **NEA-first version closes cleanly.**
   Round-trip ΔV (aerocapture) = ~{dv_total_nea_aero:.1f} km/s
   Propellant fraction at Isp=700 = ~{(mr_nea_water_met-1)/mr_nea_water_met:.0%}
   100 t chunk -> {100/mr_return_nea:.0f} t delivered. 1000 t chunk -> {1000/mr_return_nea:.0f} t.

6. Implication: the architecture pattern is right, but the right
   FIRST target is a water-bearing NEA, not Saturn. Cislunar / NEA water
   delivery is what the current MET tug class can actually do. The
   Saturn version becomes credible once a higher-Isp variant or
   fission-electric upgrade is available — that's the 2040s, not the 2030s.

The trade-study version of this analysis is the stronger framing: it
shows what the current hardware class can and can't do.
""")
