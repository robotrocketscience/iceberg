#!/usr/bin/env python3
"""Pre-script: R-eccentric-harvest-departure bounds.

Computes the ring relative-velocity vs eccentricity (H-D1) and the reactor-floor
brackets (H-D3). Does NOT run the periapsis-burn departure simulation (run.py).

Two assumptions under test: (1) harvest-from-eccentric is killed by the km/s
ring relative velocity (gentle capture needs velocity-matching ~ m/s); (2)
periapsis-burn departure from the required circular orbit recovers Oberth
(Δv ~ 8.5 not 21.9 km/s), softening Round C's 1248 kWe, but the duty-cycle
peak-power penalty keeps the floor in the high-hundreds of kWe.
"""
import math

G0 = 9.80665
MU_S = 3.793e16
R_RING = 1.07e8
R_TITAN = 1.2217e9
VINF = 6210.0
VE_MET = 800.0 * G0
ETA = 0.6
YEAR = 3.156e7
M = 100_000.0

V_CIRC = math.sqrt(MU_S / R_RING)
V_ESC = math.sqrt(2 * MU_S / R_RING)


def v_peri(r_a):
    a = (R_RING + r_a) / 2.0
    return math.sqrt(MU_S * (2.0 / R_RING - 1.0 / a))


def reactor_kwe(dv, burn_years=2.0, m=M, ve=VE_MET):
    prop = m * (math.exp(dv / ve) - 1.0)
    return 0.5 * ve ** 2 * prop / ETA / (burn_years * YEAR) / 1e3


print("=" * 68)
print("H-D1 [S] -- harvest-from-eccentric killed by ring relative velocity")
print("=" * 68)
print(f"    ring particle circular velocity v_circ = {V_CIRC/1000:.2f} km/s")
print(f"    capture works at mm/s - low-m/s (locked finding 1); threshold ~ m/s")
for mult in (1.0, 1.1, 1.3, 2.0, 5.0, R_TITAN / R_RING):
    r_a = mult * R_RING
    vrel = v_peri(r_a) - V_CIRC
    tag = "circular" if mult == 1.0 else (f"apoapsis {mult:.0f}x r_p" if mult < 20
                                          else "apoapsis at Titan")
    print(f"    {tag:22} -> periapsis v {v_peri(r_a)/1000:5.2f} km/s, "
          f"v_rel at ring = {vrel/1000:6.3f} km/s = {vrel:.0f} m/s")
print(f"    SCOPE: v_rel >= 1 km/s (>=1000x the m/s threshold) for apoapsis >= ~1.3x r_p.")
print(f"    Harvest orbit MUST be near-circular. Falsified if v_rel < 0.1 km/s at 2x r_p.")

print()
print("=" * 68)
print("H-D2/H-D3 -- periapsis-burn departure: Oberth recovered, but peak-power penalty")
print("=" * 68)
DV_IMPULSIVE = math.sqrt(VINF ** 2 + 2 * MU_S / R_RING) - V_CIRC
print(f"    impulsive-at-ring (all burns at r_p, Oberth-optimal) Δv = {DV_IMPULSIVE/1000:.2f} km/s")
print(f"    continuous spiral (Round C) Δv = 21.9 km/s -> 1248 kWe")
print(f"    reactor floor at the periapsis-burn Δv, by DUTY CYCLE (peak = avg/duty):")
avg_kwe = reactor_kwe(DV_IMPULSIVE)
print(f"      average (duty=1, if it could be spread continuously) = {avg_kwe:.0f} kWe")
for duty in (1.0, 0.5, 0.3, 0.2, 0.1):
    print(f"      duty {duty:.2f} -> peak {avg_kwe/duty:6.0f} kWe")
print(f"    SCOPE: min peak power (2-yr window, periapsis burns) in [300, 900] kWe")
print(f"    (below Round C 1248, above R179 175). run.py's sim pins the duty.")
print(f"    Falsified if min peak < 250 kWe (rescues to R179) or > 1248 (worse than spiral).")

print()
print("=" * 68)
print("H-D4 [W] -- bet #3 not relieved to Kilopower class")
print("=" * 68)
print(f"    eccentric harvest impossible (H-D1); best electric departure (periapsis-")
print(f"    burn from circular) is high-hundreds kWe (H-D3). Sub-300-kWe departure")
print(f"    remains a chemical kick stage only (non-electric). Falsified if some")
print(f"    harvest-compatible strategy yields < 250 kWe without a chemical stage.")
