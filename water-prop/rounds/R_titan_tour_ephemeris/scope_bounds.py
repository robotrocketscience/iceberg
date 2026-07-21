#!/usr/bin/env python3
"""Pre-script: R-titan-tour-ephemeris bounds.

R179 adopted the Titan pump-up departure tour as a reactor-mission lever
(floor 7.0 km/s = raise 6.70 + 300 m/s trims, "v_inf pumped free", -33%
reactor power) and its own Revisit demanded an ephemeris check before
baselining. This pre-script runs that check in patched conics with the
phoebe round's verified constants (R_saturn_moon_ga_ephemeris) and finds
the mechanism cannot work:

  1. A flyby conserves v_inf relative to Titan (Tisserand); every orbit
     BETWEEN flybys must remain bound to re-encounter Titan. So the
     departure v_inf,S a pure flyby chain can build is capped by ONE
     final kick from a barely-bound orbit:
         v_inf,S(exit) = sqrt(v_sc(alpha_esc - delta)^2 - v_esc^2)
     maximized over the contour v_inf,T. That ceiling is ~3.2 km/s --
     roughly HALF the required 6.21 km/s Hohmann-return excess.
  2. The repair is propulsive, and the Tisserand-contour structure
     removes every free lunch: raising to a "better" contour costs at
     the same Oberth rate the contour later saves. Honest Titan-assisted
     floors land within a few hundred m/s of the direct 8.45 km/s.

Strategies priced (all reach v_inf,S = 6.21 km/s from co-orbital B-ring):
  S0  direct single-burn / far-bi-elliptic (R179 anchors, echoed)
  S2  raise(r_a) + free pump + best exit kick + post-escape linear burn
  S3  raise(r_a) + free pump + POWERED final flyby (burn at Titan peri)
  S4  peri burn to hyperbolic + single outbound kick (radial geometry)
  S5  raise(r_a) + free pump to the contour's barely-bound member +
      residual burn at that member's OWN periapsis (deep-peri Oberth)
Tour strategies (S2/S3/S5) carry the R179 trim allowance (300 m/s);
single-flyby S4 carries 50 m/s targeting.

Constants: phoebe round verified vs JPL Horizons (Titan GM 8978.14
km^3/s^2, a 1,221,870 km, e 0.0288, R 2574.7 km, P 15.945 d); flyby
altitude 1000 km nominal / 1500 sensitivity (phoebe convention);
Saturn obliquity 26.73 deg, equinox 2025.37, year 29.457 yr.
Grids here SPAN the run.py grids (R182 lesson): r_a/r_T in [1.001, 20],
v_inf,S0 in [0, 6.21], Titan radius {peri, mean, apo}.
"""
import math

G0 = 9.80665
MU_S = 3.7931206e16
R_RING = 1.07e8
A_TITAN = 1.22187e9
E_TITAN = 0.0288
MU_T = 8.97814e12
R_T_BODY = 2.5747e6
ALT_NOM = 1.0e6
ALT_SENS = 1.5e6
VINF_DEP = 6210.0
TRIMS_TOUR = 300.0
TRIMS_ONE = 50.0
VE_MET = 800.0 * G0
ETA_THR = 0.6
YEAR = 3.156e7
T_TITAN_D = 15.945
OBLIQ = 26.73
T_SAT_YR = 29.457
T_EQUINOX = 2025.37

DV_DIRECT = 8.45e3       # R179 far-bi-elliptic minimum (echoed anchor)
DV_SINGLE = 8.51e3
R179_FLOOR = 7.0e3
R179_RAISE = 6.70e3


def vis(r, a):
    return math.sqrt(MU_S * (2.0 / r - 1.0 / a))


def v_esc_at(r):
    return math.sqrt(2.0 * MU_S / r)


def turn(vinf_t, rp):
    return 2.0 * math.asin(1.0 / (1.0 + rp * vinf_t ** 2 / MU_T))


def exit_vinf(vinf_t, r_enc, rp):
    """Max heliocentric-departure v_inf,S from a pure flyby chain whose
    orbits stay bound: one kick from the bound limit (alpha_esc), turned
    by delta toward alignment."""
    v_t = vis(r_enc, A_TITAN)
    vesc = v_esc_at(r_enc)
    ca = (vesc ** 2 - v_t ** 2 - vinf_t ** 2) / (2.0 * v_t * vinf_t)
    if ca > 1.0:
        return 0.0           # v_T + v_inf,T < v_esc: no escape at all
    a_esc = math.acos(max(ca, -1.0))
    a_out = max(a_esc - turn(vinf_t, rp), 0.0)
    v2 = v_t ** 2 + vinf_t ** 2 + 2.0 * v_t * vinf_t * math.cos(a_out)
    return math.sqrt(max(v2 - vesc ** 2, 0.0)) if v2 > vesc ** 2 else 0.0


def raise_state(ra, r_enc):
    """Peri burn at ring to (peri=ring, apo=ra); crossing state at r_enc."""
    a = (R_RING + ra) / 2.0
    dv = vis(R_RING, a) - vis(R_RING, R_RING)
    if ra < r_enc:
        return dv, None
    v_sc = vis(r_enc, a)
    v_th = R_RING * vis(R_RING, a) / r_enc
    v_r = math.sqrt(max(v_sc ** 2 - v_th ** 2, 0.0))
    v_t = vis(r_enc, A_TITAN)
    return dv, math.hypot(v_th - v_t, v_r)


def s3_powered(vinf_t, r_enc, rp):
    """Powered final flyby from the bound limit: burn dv_p at Titan
    periapsis; exit alignment limited by the powered hyperbola's turn."""
    v_t = vis(r_enc, A_TITAN)
    vesc = v_esc_at(r_enc)
    ca = (vesc ** 2 - v_t ** 2 - vinf_t ** 2) / (2.0 * v_t * vinf_t)
    if ca > 1.0:
        return None
    a_esc = math.acos(max(ca, -1.0))
    target = VINF_DEP ** 2 + vesc ** 2
    lo, hi = 0.0, 6000.0
    for _ in range(60):
        dv_p = 0.5 * (lo + hi)
        vp_in = math.sqrt(vinf_t ** 2 + 2.0 * MU_T / rp)
        vout = math.sqrt(max((vp_in + dv_p) ** 2 - 2.0 * MU_T / rp, 0.0))
        half = math.asin(1.0 / (1.0 + rp * vinf_t ** 2 / MU_T)) \
            + math.asin(1.0 / (1.0 + rp * vout ** 2 / MU_T))
        a_out = max(a_esc - half, 0.0)
        v2 = v_t ** 2 + vout ** 2 + 2.0 * v_t * vout * math.cos(a_out)
        if v2 < target:
            lo = dv_p
        else:
            hi = dv_p
    return hi if hi < 5999.0 else None


def s5_contour_peri(vinf_t, r_enc):
    """Barely-bound member of the v_inf,T contour; residual burn at ITS
    periapsis to reach VINF_DEP."""
    v_t = vis(r_enc, A_TITAN)
    h = (MU_S / r_enc - (vinf_t ** 2 - v_t ** 2) / 2.0) * r_enc / v_t
    if h <= 0.0:
        return None
    r_pb = h ** 2 / (2.0 * MU_S)
    if r_pb < R_RING or r_pb > r_enc:
        return None
    v_pb = math.sqrt(2.0 * MU_S / r_pb)
    return math.sqrt(VINF_DEP ** 2 + 2.0 * MU_S / r_pb) - v_pb


def sweep(r_enc, rp, n=400):
    v_circ = vis(R_RING, R_RING)
    best = {"S2": None, "S3": None, "S5": None}
    ceil_vs = 0.0
    for i in range(n):
        ra = r_enc * (1.001 * (20.0 / 1.001) ** (i / (n - 1.0)))
        dv_r, vinf_t = raise_state(ra, r_enc)
        if vinf_t is None or vinf_t <= 0.0:
            continue
        ve = exit_vinf(vinf_t, r_enc, rp)
        ceil_vs = max(ceil_vs, ve)
        s2 = dv_r + max(0.0, VINF_DEP - ve) + TRIMS_TOUR
        if best["S2"] is None or s2 < best["S2"][0]:
            best["S2"] = (s2, ra / r_enc, vinf_t)
        p = s3_powered(vinf_t, r_enc, rp)
        if p is not None:
            s3 = dv_r + p + TRIMS_TOUR
            if best["S3"] is None or s3 < best["S3"][0]:
                best["S3"] = (s3, ra / r_enc, vinf_t)
        res = s5_contour_peri(vinf_t, r_enc)
        if res is not None:
            s5 = dv_r + res + TRIMS_TOUR
            if best["S5"] is None or s5 < best["S5"][0]:
                best["S5"] = (s5, ra / r_enc, vinf_t)
    # S4: hyperbolic peri burn + one outbound kick
    s4_best = None
    for i in range(n):
        v0 = VINF_DEP * i / (n - 1.0)
        v_peri = math.sqrt(v0 ** 2 + 2.0 * MU_S / R_RING)
        dv1 = v_peri - v_circ
        v_sc = math.sqrt(v0 ** 2 + 2.0 * MU_S / r_enc)
        v_th = R_RING * v_peri / r_enc
        v_r = math.sqrt(max(v_sc ** 2 - v_th ** 2, 0.0))
        v_t = vis(r_enc, A_TITAN)
        vinf_t = math.hypot(v_th - v_t, v_r)
        kick = 2.0 * vinf_t * math.sin(turn(vinf_t, rp) / 2.0)
        v1 = math.sqrt(max((v_sc + kick) ** 2 - 2.0 * MU_S / r_enc, 0.0))
        tot = dv1 + max(0.0, VINF_DEP - v1) + TRIMS_ONE
        if s4_best is None or tot < s4_best[0]:
            s4_best = (tot, v0, vinf_t, v1)
    return ceil_vs, best, s4_best


print("== H1: pure-flyby exit ceiling (the killing bound) ==")
for r_enc, tag in ((A_TITAN * (1 - E_TITAN), "Titan@peri"),
                   (A_TITAN, "Titan@mean"),
                   (A_TITAN * (1 + E_TITAN), "Titan@apo")):
    for rp, atag in ((R_T_BODY + ALT_NOM, "1000km"),
                     (R_T_BODY + ALT_SENS, "1500km")):
        best_v, best_vt = 0.0, 0.0
        for j in range(400):
            vt = 2350.0 + (9000.0 - 2350.0) * j / 399.0
            ve = exit_vinf(vt, r_enc, rp)
            if ve > best_v:
                best_v, best_vt = ve, vt
        print(f"  {tag} alt {atag}: max exit v_inf,S = {best_v/1e3:.2f} km/s "
              f"at v_inf,T = {best_vt/1e3:.2f} (required: 6.21)")

print("\n== H2: honest strategy floor (all reach v_inf,S 6.21) ==")
print(f"  S0 direct: bi-elliptic {DV_DIRECT/1e3:.2f} / single {DV_SINGLE/1e3:.2f}")
print(f"  R179 shipped claim (falsified mechanism): {R179_FLOOR/1e3:.2f}")
floors, ceilings = {}, {}
for r_enc, tag in ((A_TITAN * (1 - E_TITAN), "peri"), (A_TITAN, "mean"),
                   (A_TITAN * (1 + E_TITAN), "apo")):
    ceil_vs, best, s4 = sweep(r_enc, R_T_BODY + ALT_NOM)
    parts = [f"S{k[-1]} {v[0]/1e3:.2f} (ra/rT {v[1]:.2f})"
             for k, v in best.items() if v is not None]
    print(f"  Titan@{tag}: " + " | ".join(parts))
    print(f"           S4 {s4[0]/1e3:.2f} (v_inf,S0 {s4[1]/1e3:.2f}, "
          f"v_inf,T {s4[2]/1e3:.2f})")
    floors[tag] = min([v[0] for v in best.values() if v is not None]
                      + [s4[0]])
    ceilings[tag] = ceil_vs
    print(f"           honest Titan-assisted floor: {floors[tag]/1e3:.2f} "
          f"km/s (saving vs direct {(DV_DIRECT-floors[tag])/1e3:+.2f})")

print("\n== H3: the -33% reactor lever, repriced ==")
# chunk-fed (low-thrust) honest: gravity-loss factor from the campaign's
# own anchor pair (spiral 9.0 vs impulsive 8.45) applied to the raise;
# exit kick capped by H1's ceiling; residual bought linearly post-escape.
GRAV_LOSS = 9000.0 / DV_DIRECT
dv_raise_h = vis(R_RING, (R_RING + A_TITAN) / 2.0) - vis(R_RING, R_RING)
dv_lt = dv_raise_h * GRAV_LOSS + (VINF_DEP - ceilings["mean"]) + TRIMS_TOUR
m_f = 100_000.0
for name, dv in (("direct spiral (R179/mission_graph)", 9000.0),
                 ("Titan-assisted impulsive-hybrid best", floors["mean"]),
                 ("Titan-assisted low-thrust honest", dv_lt),
                 ("R179 claimed Titan floor (dead)", 7000.0)):
    prop = m_f * (math.exp(dv / VE_MET) - 1.0)
    p_req = 0.5 * VE_MET ** 2 * prop / ETA_THR / (2.0 * YEAR) / 1e3
    print(f"  {name}: dv {dv/1e3:.2f} -> P(2-yr burn) = {p_req:.0f} kWe")

print("\n== H4: what survives ==")
v_circ = vis(R_RING, R_RING)
dv_circ = vis(R_RING, (R_RING + A_TITAN) / 2.0) - v_circ
print(f"  capture-side ring circularization (Hohmann-tangential bound, "
      f"flyby-irreducible): {dv_circ/1e3:.2f} km/s -- R179 number stands")
rt = floors["mean"] + dv_circ
print(f"  honest max-assist round trip: {rt/1e3:.2f} km/s "
      f"(R179 said 13.7; retired axis-19: 14.7)")
# pump-rotation schedule on the Hohmann contour (worked example)
dv_r, vinf_h = raise_state(A_TITAN, A_TITAN)
if vinf_h is None:
    _, vinf_h = raise_state(A_TITAN * 1.0000001, A_TITAN)
v_t = vis(A_TITAN, A_TITAN)
v_apo_h = vis(A_TITAN, (R_RING + A_TITAN) / 2.0)
a0 = math.acos((v_apo_h - v_t) / vinf_h) if vinf_h else 0.0
d_h = turn(vinf_h, R_T_BODY + ALT_NOM)
ca = (v_esc_at(A_TITAN) ** 2 - v_t ** 2 - vinf_h ** 2) / (2 * v_t * vinf_h)
a_esc = math.acos(max(min(ca, 1.0), -1.0))
n_fly = math.ceil((a0 - a_esc) / d_h)
print(f"  pump rotation (Hohmann contour): alpha {math.degrees(a0):.0f} -> "
      f"{math.degrees(a_esc):.0f} deg at {math.degrees(d_h):.1f} deg/flyby = "
      f"{n_fly} flybys ~ {n_fly*2*T_TITAN_D/365.25:.2f} yr (phoebe 2xT conv)")
for yr in (2032.7, 2036.0, 2040.1):
    dec = OBLIQ * abs(math.cos(2 * math.pi * (yr - T_EQUINOX) / T_SAT_YR))
    print(f"  declination crank at {yr}: {dec:.1f} deg -> "
          f"{dec/math.degrees(d_h):.1f} flybys-worth of crank")
# Iapetus trim on the way out (post-Titan)
R_IAP, MU_IAP, RP_IAP = 3.5613e9, 1.205e11, 8.35e5
v_out = math.sqrt(3.2e3 ** 2 + 2 * MU_S / R_IAP)
v_iap = math.sqrt(MU_S / R_IAP)
vinf_i = v_out - v_iap
kick_i = 2 * vinf_i * math.sin(
    math.asin(1.0 / (1.0 + RP_IAP * vinf_i ** 2 / MU_IAP)))
v1 = math.sqrt((v_out + kick_i) ** 2 - 2 * MU_S / R_IAP)
print(f"  Iapetus post-Titan trim: kick {kick_i:.0f} m/s -> exit v_inf,S "
      f"{v1/1e3:.2f} (from 3.20) -- a trim, not a bridge")
