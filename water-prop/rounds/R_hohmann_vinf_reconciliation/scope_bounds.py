#!/usr/bin/env python3
"""Pre-script: R-hohmann-vinf-reconciliation bounds.

The campaign carries VINF_DEP = 6.21 km/s as "the Hohmann-return hyperbolic
excess" at Saturn (R179 `R_departure_anchor_reconciliation` scope_bounds.py line 31;
R186 `R_titan_tour_ephemeris` uses the same). A clean two-body Saturn->Earth Hohmann
gives ~5.44 km/s. This round reconciles the 0.77 km/s (14%) gap from first
principles and propagates it through the departure-Delta-v -> reactor-power-floor
chain and the R186 Titan bound-chain cap, to determine whether anything downstream
is sensitive to it. (Flagged corrections-live-forward in design-axes/04, latest+25.)

Physics:
  Heliocentric Hohmann Saturn->Earth: aphelion at r_S, perihelion at r_E.
    v_S      = sqrt(mu_sun / r_S)              # Saturn circular speed
    v_aph    = sqrt(mu_sun (2/r_S - 1/a_t)),  a_t = (r_S + r_E)/2
    vinf     = v_S - v_aph                      # heliocentric departure excess
  Saturn-centric single-burn escape from co-orbital B-ring to that vinf:
    dv       = sqrt(vinf^2 + 2 mu_S / R_ring) - v_circ_ring   (Oberth quadrature)
  Reactor floor (R179 model, reproduced): 2-yr chunk-fed MET burn, 100 t final:
    prop = m_f (exp(dv/ve) - 1); P = 0.5 ve^2 prop / eta / (2 yr)

Grids here SPAN the run grids: a_S in {9.537, 9.5388, 9.582} AU (source spread),
vinf in {5.44, 6.21} km/s, dv-model in {impulsive-single-burn, R179 9.0 spiral}.
"""
import math

MU_SUN = 1.32712440018e20      # m^3/s^2
AU = 1.495978707e11            # m
R_E = 1.0 * AU
A_SAT_VALUES = {"9.537 (NASA a)": 9.537, "9.5388 (campaign)": 9.5388,
                "9.582 (NASA fact sheet)": 9.582}

# Saturn-centric (R179 anchors, reproduced exactly)
MU_S = 3.793e16
R_RING = 1.07e8
G0 = 9.80665
VE_MET = 800.0 * G0
ETA = 0.6
YEAR = 3.156e7
V_CIRC = math.sqrt(MU_S / R_RING)

def hohmann_vinf(a_sat_au):
    r_S = a_sat_au * AU
    v_S = math.sqrt(MU_SUN / r_S)
    a_t = (r_S + R_E) / 2.0
    v_aph = math.sqrt(MU_SUN * (2.0 / r_S - 1.0 / a_t))
    return v_S - v_aph

def dv_single_burn(vinf):
    return math.sqrt(vinf ** 2 + 2 * MU_S / R_RING) - V_CIRC

def reactor_kwe(dv, m_f=100_000.0):
    prop = m_f * (math.exp(dv / VE_MET) - 1.0)
    e_jet = 0.5 * VE_MET ** 2 * prop
    return e_jet / ETA / (2 * YEAR) / 1e3

print("=" * 70)
print("H1 [S] -- two-body Hohmann Saturn->Earth vinf = 5.44 km/s (robust)")
print("=" * 70)
for tag, a in A_SAT_VALUES.items():
    print(f"  a_Saturn = {tag:24}: vinf = {hohmann_vinf(a):.3f} km/s"
          .replace("km/s", "").rstrip() + f"  ({hohmann_vinf(a)/1000:.3f} km/s)")
vinf_min = hohmann_vinf(9.5388) / 1000.0
print(f"  -> minimum-energy Hohmann vinf = {vinf_min:.2f} km/s (SCOPE band [5.3,5.6]);"
      f" robust to a_Saturn source (9.537-9.582 AU all give 5.44).")

print()
print("=" * 70)
print("H2 [S] -- 6.21 km/s is NOT the tangent minimum; it is a faster transfer")
print("=" * 70)
# Solve: keep aphelion at r_S, lower perihelion q until vinf = 6.21.
r_S = 9.5388 * AU
v_S = math.sqrt(MU_SUN / r_S)
target = 6210.0
v_aph_needed = v_S - target
# v_aph^2 = mu(2/r_S - 1/a) -> 1/a = 2/r_S - v_aph^2/mu
inv_a = 2.0 / r_S - v_aph_needed ** 2 / MU_SUN
a = 1.0 / inv_a
q = 2 * a - r_S
print(f"  v_Saturn (circular)          = {v_S/1000:.3f} km/s")
print(f"  v_aph for vinf=6.21          = {v_aph_needed/1000:.3f} km/s")
print(f"  -> transfer perihelion q     = {q/AU:.3f} AU (vs 1.000 AU for the")
print(f"     tangent Hohmann). 6.21 corresponds to a FASTER transfer dipping")
print(f"     to ~{q/AU:.2f} AU perihelion -- conservative by 14%, not the minimum.")
print(f"  SCOPE: q in [0.55, 0.75] AU -> 6.21 is a faster-transfer vinf, mislabeled")
print(f"  'Hohmann'. Falsified if q >= 0.95 AU (i.e. 6.21 IS ~tangent).")

print()
print("=" * 70)
print("H3 [S] -- departure Delta-v barely moves (Oberth quadrature suppresses it)")
print("=" * 70)
dv_621 = dv_single_burn(6210.0)
dv_544 = dv_single_burn(vinf_min * 1000.0)
print(f"  v_circ at B-ring             = {V_CIRC/1000:.2f} km/s (v_esc "
      f"{math.sqrt(2)*V_CIRC/1000:.2f})")
print(f"  single-burn escape @ vinf 6.21 = {dv_621/1000:.3f} km/s "
      f"(reproduces R179's 8.51)")
print(f"  single-burn escape @ vinf 5.44 = {dv_544/1000:.3f} km/s")
print(f"  -> departure Delta-v change    = {(dv_621-dv_544)/1000:.3f} km/s "
      f"({(dv_621-dv_544)/dv_621*100:.1f}%). SCOPE band [0.10, 0.25] km/s.")
print(f"  d(dv)/d(vinf) = vinf/sqrt(v_esc^2+vinf^2) = "
      f"{6210.0/math.sqrt((math.sqrt(2)*V_CIRC)**2+6210**2):.2f} "
      f"(a 0.77 km/s vinf error -> ~0.17 km/s dv). Falsified if change > 0.4 km/s.")

print()
print("=" * 70)
print("H4 [S] -- reactor floor moves a few kWe, stays in the 155-175 band;")
print("         Titan cap (~3.2 km/s) still << 5.44 so R186 revocation holds")
print("=" * 70)
p_621 = reactor_kwe(dv_621)
p_544 = reactor_kwe(dv_544)
p_spiral_90 = reactor_kwe(9000.0)     # R179 headline: 9.0 spiral -> 175
print(f"  reactor P @ impulsive dv(6.21)={dv_621/1000:.2f}: {p_621:.0f} kWe")
print(f"  reactor P @ impulsive dv(5.44)={dv_544/1000:.2f}: {p_544:.0f} kWe  "
      f"(change {p_621-p_544:.0f} kWe = {(p_621-p_544)/p_621*100:.1f}%)")
print(f"  reactor P @ R179 9.0 spiral (state-of-record headline): {p_spiral_90:.0f} kWe")
print(f"  -> the vinf correction moves the floor by ~{p_621-p_544:.0f} kWe, INSIDE")
print(f"     the existing 155-175 band. Impulsive is the UPPER bound on the")
print(f"     fractional effect (low-thrust spiral is even less vinf-sensitive).")
TITAN_CAP = 3.2
print(f"  Titan bound-chain cap (R186) ~{TITAN_CAP} km/s << 5.44 (min-energy) "
      f"<< 6.21 -> the Titan pump-up lever stays revoked either way.")
print(f"  SCOPE: floor in [150,175] kWe at 5.44; |change| < 10 kWe; Titan cap < 5.44.")
print(f"  Falsified if the floor drops below 120 kWe or the Titan cap reaches vinf.")
