#!/usr/bin/env python3
"""Pre-script: R-lunar-ga-arrival-fidelity prediction bands.

Computes ONLY (a) the R12 baseline it reproduces and (b) the analytic v-infinity
globe bound. It does NOT run the honest vectorial per-flyby optimizer or the
flyby-count sweep -- those live in run.py and adjudicate the hypotheses.

The claim under test: R12's inbound lunar tour (src/waterprop/trajectory/
lunar_flyby.py) sheds 5.83 km/s of a 10.30 km/s Earth arrival in 10 flybys and
feeds the axis-10 strict L0-05 closure. R12 recomputes the Moon-relative speed
U_m from the REDUCED Earth-frame v_inf each flyby, violating v-infinity
conservation; a lunar flyby only ROTATES v_inf_moon at fixed magnitude U_m.
With U_m conserved, min Earth-frame speed = |U_m - v_M|, so max total shed
= v_sc - 2 v_M -- about 2 km/s, not 5.83.
"""
import math

# Lunar / Earth constants (identical to lunar_flyby.py)
GM_MOON = 4902.800066
R_MOON = 1737.4
V_MOON = 1.0220
R_LUNAR_ORBIT = 384400.0
GM_EARTH = 398600.4418

V_INF_ARRIVAL = 10.30          # km/s, R12 V_INF_INBOUND_KM_S (Hohmann arrival excess)
PERI_ALT = 100.0               # km, R12 default


def v_sc_at_moon(v_inf_E):
    """Earth-frame spacecraft speed at lunar distance from Earth-frame v_inf."""
    return math.sqrt(v_inf_E ** 2 + 2.0 * GM_EARTH / R_LUNAR_ORBIT)


def v_inf_E_from_speed(v_sc):
    """Invert: Earth-frame v_inf from Earth-frame speed at lunar distance."""
    arg = v_sc ** 2 - 2.0 * GM_EARTH / R_LUNAR_ORBIT
    return math.sqrt(arg) if arg > 0 else 0.0


def delta_max(U_m):
    """Flyby turn angle (rad): 2 arcsin(1/(1 + r_p U_m^2 / GM_moon))."""
    r_p = R_MOON + PERI_ALT
    e = 1.0 + r_p * U_m ** 2 / GM_MOON
    return 2.0 * math.asin(1.0 / e)


def r12_first_flyby_shed(v_inf_E):
    """Reproduce R12 single_flyby_braking's Earth-frame braking (its OWN formula:
    U_m = v_sc + v_M leading-side; brake = full 2 U_m sin(delta/2))."""
    v_sc = v_sc_at_moon(v_inf_E)
    U_m = v_sc + V_MOON
    delta = delta_max(U_m)
    return 2.0 * U_m * math.sin(delta / 2.0)


print("=" * 72)
print("BASELINE -- reproduce R12's inbound lunar tour claim")
print("=" * 72)
v_sc0 = v_sc_at_moon(V_INF_ARRIVAL)
print(f"    arrival v_inf (Earth) = {V_INF_ARRIVAL:.2f} km/s")
print(f"    v_sc at lunar distance = {v_sc0:.3f} km/s; v_Moon orbital = {V_MOON} km/s")
print(f"    R12 first-flyby Earth-frame braking = {r12_first_flyby_shed(V_INF_ARRIVAL):.3f} km/s")
print(f"    (R12 STUDY table: 1 flyby 10.30->9.84 = 0.46; 10 flybys shed 5.83; residual 4.47)")

print()
print("=" * 72)
print("H-B1 [S] -- honest first-flyby braking <= 0.20 km/s (>=2x below R12 0.458)")
print("=" * 72)
# honest scale: brake ~ delta_max * v_M * sin(geom). Use U_m = v_sc - v_M (min, most
# favourable) and U_m = v_sc + v_M (max relative speed). delta_max * v_M is the scale.
for label, U_m in (("min U_m = v_sc - v_M", v_sc0 - V_MOON),
                   ("max U_m = v_sc + v_M", v_sc0 + V_MOON)):
    dm = delta_max(U_m)
    scale = dm * V_MOON     # rough per-flyby Earth-frame braking scale
    print(f"    {label:22} = {U_m:6.3f} km/s  delta_max={math.degrees(dm):.2f} deg  "
          f"~braking scale delta_max*v_M = {scale:.3f} km/s")
print(f"    SCOPE: honest first-flyby braking <= 0.20 km/s. Falsified if > 0.25 or < 0.01.")

print()
print("=" * 72)
print("H-B2 [S] -- v-infinity globe bound: max TOTAL shed ~2 km/s regardless of N")
print("=" * 72)
# U_m conserved => min Earth-frame speed = |U_m - v_M|; minimize over arrival geometry
# at U_m = v_sc - v_M  =>  min speed = v_sc - 2 v_M.
v_sc_floor = v_sc0 - 2.0 * V_MOON
vinf_floor = v_inf_E_from_speed(v_sc_floor)
max_shed = V_INF_ARRIVAL - vinf_floor
print(f"    min reachable Earth-frame speed = v_sc - 2 v_M = {v_sc0:.3f} - {2*V_MOON:.3f} "
      f"= {v_sc_floor:.3f} km/s")
print(f"    -> v_inf floor = {vinf_floor:.3f} km/s")
print(f"    -> MAX TOTAL SHED = {V_INF_ARRIVAL:.2f} - {vinf_floor:.2f} = {max_shed:.3f} km/s")
print(f"    SCOPE: honest tour sheds <= 2.3 km/s at ANY N (predicted {max_shed:.2f}).")
print(f"    Falsified if honest tour sheds > 2.5 km/s. R12 claims 5.83 -> IMPOSSIBLE if bound holds.")

print()
print("=" * 72)
print("H-B3 [S] -- flyby-count blowup: >= 40 flybys to reach the ~2 km/s bound")
print("=" * 72)
# To rotate v_inf_moon a cumulative ~180 deg (aligned->anti-aligned with v_M) at
# <= delta_max per flyby. Use U_m = v_sc - v_M (the min-U_m tour that reaches the floor).
U_m_tour = v_sc0 - V_MOON
dm_tour = delta_max(U_m_tour)
n_flybys = math.pi / dm_tour
print(f"    tour U_m = {U_m_tour:.3f} km/s; delta_max = {math.degrees(dm_tour):.2f} deg/flyby")
print(f"    cumulative rotation needed ~180 deg -> N >= pi/delta_max = {n_flybys:.0f} flybys")
print(f"    SCOPE: honest model needs >= 40 flybys (predicted ~{n_flybys:.0f}). "
      f"Falsified if within 0.1 km/s of bound in <= 25 flybys.")
print(f"    phasing at ~1 synodic month/flyby: {n_flybys:.0f} flybys ~ "
      f"{n_flybys*29.5/365.25:.1f} yr of inbound phasing.")

print()
print("=" * 72)
print("H-B5 [S] -- axis-10 strict L0-05 closure does NOT survive honest residual")
print("=" * 72)
G0 = 9.80665
ISP, ETA, DUTY = 2000.0, 0.65, 0.5
CHUNK_T, DRY_T = 14.0, 5.0
v_e = ISP * G0
print(f"    R12 best cell: residual 4.47 km/s, 10 flybys, 0.7 yr phasing -> 70% delivery / 13.9 yr")
print(f"    honest: residual ~{vinf_floor:.1f} km/s, ~{n_flybys:.0f} flybys, "
      f"~{n_flybys*29.5/365.25:.1f} yr phasing")
for res in (4.47, vinf_floor):
    reactor_t = (15_000.0) / 10.0 / 1000.0    # 15 kWe @ 10 W/kg = 1.5 t (R12 best cell)
    m0 = CHUNK_T + DRY_T + reactor_t
    prop_frac = 1.0 - math.exp(-res * 1000.0 / v_e)
    prop = m0 * prop_frac
    delivered = max(CHUNK_T - prop, 0.0)
    print(f"    residual {res:5.2f} km/s: prop {prop:5.2f} t of chunk 14 t -> "
          f"delivered {delivered:5.2f} t ({100*delivered/CHUNK_T:.0f}%)")
print(f"    + inbound phasing ~{n_flybys*29.5/365.25:.1f} yr pushes round trip "
      f"(6.09+1.0+6.09 floor = 13.2 yr) well past strict 15 yr.")
print(f"    SCOPE: 0 cells close strict-15yr at >=30% delivery. Falsified if >=1 does.")
