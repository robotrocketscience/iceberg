#!/usr/bin/env python3
"""Pre-script: R-spent-reactor-disposal bounds.

The campaign's Kilopower-class reactor is a fission core; at end of life
it is an activated, fission-product-laden object that cannot be left to
drift in a system containing Enceladus (subsurface ocean, active plumes)
and Titan (organics, subsurface water). This round prices disposal and
surfaces the planetary-protection constraints it imposes.

Two architectures, two disposal problems:
  1. MONOLITHIC (state-of-record post-R187): the reactor powers the
     8-yr return-transit spiral, so it returns WITH the mothership and
     is disposed near Earth/delivery. PP concern shifts to cislunar —
     an activated reactor arriving in the delivery zone.
  2. FLEET / relay (R184 reactor-swap; NPV-dead but architecturally
     live): each swap leaves a SPENT core at Saturn. Those must be
     disposed into Saturn's atmosphere — the Cassini precedent.

Anchors:
  KRUSTY core (flight-relevant Kilopower): 32.2 kg fuel, 27.7 kg U-235,
    93 wt% enriched U-8Mo (tandfonline KRUSTY Reactor Design). Core is
    CRITICAL-MASS-bound, not power-bound: a bare HEU fast core needs a
    critical mass regardless of kWe, so fuel scales weakly with power.
  Cassini: deliberately flown into Saturn 2017-09-15 to deny even a
    ~1e-6 chance of striking Enceladus/Titan (NASA/JPL, SwRI).
  Saturn: mu 3.793e16, R_1bar 6.0268e7 m, mid-B-ring 1.07e8 m.
  Titan: mu 8.978e12, a 1.2217e9, R 2.5747e6; flyby alt 1000 km.
  Reactor system mass: kappa {100 paper, 417 flown} kg/kWe x P 155 kWe
    (R186 bet-#3 band).
"""
import math

MU_S = 3.793e16
R_1BAR = 6.0268e7
R_ATM = 6.1e7                  # atmosphere-grazing periapsis target
R_RING = 1.07e8
A_TITAN = 1.2217e9
MU_T = 8.978e12
R_T_BODY = 2.5747e6
ALT = 1.0e6
G0 = 9.80665
VE_MET = 800.0 * G0
U235_PER_UNIT = 27.7          # kg, KRUSTY
P_MISSION = 155.0             # kWe, R186 bet-#3 band low
KAPPA = {"paper": 100.0, "flown": 417.0}


def vis(r, a):
    return math.sqrt(MU_S * (2.0 / r - 1.0 / a))


# --- H1: disposal delta-v ---
print("== H1: disposal delta-v ==")
# (a) monolithic reactor sits co-orbital B-ring circular; controlled
#     deorbit = lower periapsis to atmosphere, apoapsis stays at ring.
v_circ = vis(R_RING, R_RING)
a_deorbit = (R_RING + R_ATM) / 2.0
dv_deorbit = v_circ - vis(R_RING, a_deorbit)
print(f"  (a) co-orbital controlled deorbit into Saturn: "
      f"{dv_deorbit/1e3:.2f} km/s")
# (b) relay mothership on staging ellipse (peri ring, apo Titan): one
#     Titan flyby lowers periapsis to atmosphere. Cost vs flyby capacity.
a_stage = (R_RING + A_TITAN) / 2.0
v_apo_stage = vis(A_TITAN, a_stage)
a_disp = (R_ATM + A_TITAN) / 2.0
v_apo_disp = vis(A_TITAN, a_disp)
dv_peri_lower = v_apo_stage - v_apo_disp
vinf_t = vis(A_TITAN, A_TITAN) - v_apo_stage
rp = R_T_BODY + ALT
flyby_cap = 2.0 * vinf_t * math.sin(
    math.asin(1.0 / (1.0 + rp * vinf_t ** 2 / MU_T)))
print(f"  (b) staging-ellipse periapsis-lower to atmosphere: "
      f"{dv_peri_lower/1e3:.3f} km/s; single Titan flyby capacity "
      f"{flyby_cap/1e3:.3f} km/s -> {'FREE (flyby covers it)' if flyby_cap > dv_peri_lower else 'needs burn'}")
print(f"  asymmetry vs R186: Titan LOWERS periapsis (disposal, free) but "
      f"cannot RAISE v_inf (departure, capped 3.3). The well helps going "
      f"down, not up.")

# --- H2: propellant to deorbit the monolithic reactor mass ---
print("\n== H2: inventory and deorbit propellant (monolithic) ==")
burnup = 500e3 * 3.0 * 3.156e7 / 3.2e-11 * 235e-3 / 6.022e23  # ~kg U fissioned
print(f"  U-235 per Kilopower unit: {U235_PER_UNIT:.1f} kg (critical-mass "
      f"bound); operational burnup over ~3 fpy at 500 kWth ~ {burnup:.2f} kg")
for tag, kap in KAPPA.items():
    m_react = kap * P_MISSION / 1000.0        # tonnes
    prop = m_react * (math.exp(dv_deorbit / VE_MET) - 1.0)
    print(f"  {tag} kappa: reactor system {m_react:.0f} t -> deorbit "
          f"propellant {prop:.1f} t ({prop/m_react*100:.0f}% of reactor mass)")

# --- H3: planetary-protection framing (qualitative + the requirement) ---
print("\n== H3: planetary protection ==")
print("  Enceladus subsurface ocean + Titan organics -> COSPAR-governed;")
print("  Cassini precedent: refused even ~1e-6 Enceladus-strike risk,")
print("  plunged into Saturn 2017. Requirement: high-probability CONTROLLED")
print("  Saturn atmospheric disposal for anything left at Saturn.")
print("  Monolithic twist: reactor RETURNS -> PP concern moves to cislunar")
print("  (activated reactor in the delivery zone) — a distinct constraint.")

# --- H4: the constraints ---
print("\n== H4: disposal is cheap+precedented, but imposes constraints ==")
print(f"  cheap: co-orbital deorbit {dv_deorbit/1e3:.1f} km/s (vs departure "
      f"8.45); free via Titan on a staging orbit. NOT a binding bet.")
print("  constraint (a): reactor must be SEPARABLE + independently")
print("     disposable (cannot depend on a mothership that may not return).")
print("  constraint (b) fleet: reserve one Titan disposal flyby per spent core.")
print("  constraint (c) monolithic: an activated reactor arrives in cislunar —")
print("     an UNPRICED delivery-zone PP/safety constraint. The sharp one.")
