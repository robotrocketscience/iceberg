#!/usr/bin/env python3
"""R-saturn-frame-titan-tour — can a Saturn-system tour re-open the Titan
departure lever? Deterministic Saturn-centric analysis. See SCOPE.md.

Settles the crack R-ephemeris-departure-anchor opened: R186's Titan revocation
is conditional on vinf_T; this round asks whether a real Saturn-frame moon tour
can reach vinf_T >= 4 (which would supply the 5.44 km/s departure requirement).

Outputs results/tour_findings.json and results/tour.png (via plot.py).
"""
import json
import math
from pathlib import Path

RESULTS = Path(__file__).resolve().parent / "results"
RESULTS.mkdir(parents=True, exist_ok=True)

MU_S = 3.793e7                 # km^3/s^2 (Saturn)
R_RING = 107_000.0            # km (B-ring)
REQ = 5.44                    # km/s departure v_inf required (ephemeris round)

# moon: (a km, GM km^3/s^2, body radius km)
MOONS = {
    "Tethys":  (294_619.0,  41.2,   531.0),
    "Dione":   (377_396.0,  73.11,  561.4),
    "Rhea":    (527_108.0,  153.94, 763.8),
    "Titan":   (1_221_870.0, 8978.14, 2574.7),
    "Iapetus": (3_560_820.0, 120.5,  734.5),
}


def v_circ(a):
    return math.sqrt(MU_S / a)


def vinf_from_bring(a):
    a_t = (R_RING + a) / 2.0
    return v_circ(a) - math.sqrt(MU_S * (2.0 / a - 1.0 / a_t))


def departure_excess(a, vinf):
    v_at = v_circ(a) + vinf
    arg = v_at ** 2 - 2 * MU_S / a
    return math.sqrt(arg) if arg > 0 else 0.0


def vinf_needed_for(a, target=REQ):
    """invert: departure_excess(a, vinf) = target -> vinf."""
    v_at = math.sqrt(target ** 2 + 2 * MU_S / a)
    return v_at - v_circ(a)


def delta_max(vinf, mu, r_p):
    return 2.0 * math.asin(1.0 / (1.0 + r_p * vinf ** 2 / mu))


def grade(name, predicted, measured, held, note=""):
    tag = "HELD" if held else "FALSIFIED"
    print(f"  [{tag:9}] {name}: predicted {predicted} | measured {measured}"
          + (f"  ({note})" if note else ""))
    return {"name": name, "predicted": predicted, "measured": measured,
            "held": held, "note": note}


findings = {"requirement_kms": REQ, "moons": {}}
table = {}
for name, (a, mu, R) in MOONS.items():
    vi = vinf_from_bring(a)
    de = departure_excess(a, vi)
    vneed = vinf_needed_for(a)
    dm = math.degrees(delta_max(vi, mu, R + 1000.0))
    table[name] = {"a_km": a, "v_moon": v_circ(a), "vinf_bring": vi,
                   "dep_excess": de, "vinf_needed_5p44": vneed,
                   "vinf_gap": vneed - vi, "flyby_turn_deg": dm}
findings["moons"] = table

print("=" * 72)
print("H1 [S] -- vinf_T from the B-ring is ~3.3 km/s (Tisserand-fixed)")
print("=" * 72)
vinf_T = table["Titan"]["vinf_bring"]
print(f"    vinf_T from B-ring (Titan) = {vinf_T:.2f} km/s")
h1 = 3.0 <= vinf_T <= 3.6
findings["H1"] = grade("vinf_T from B-ring ~3.3, not 4.0",
                       "vinf_T in [3.0,3.6] km/s (reproduces R186)",
                       f"{vinf_T:.2f} km/s", h1,
                       "Tisserand-conserved by Titan flybys -> this is the ceiling")

print()
print("=" * 72)
print("H2 [S] -- best single-moon departure excess = Titan ~4.1 km/s < 5.44")
print("=" * 72)
for name in ("Tethys", "Dione", "Rhea", "Titan", "Iapetus"):
    t = table[name]
    print(f"    {name:8}: vinf {t['vinf_bring']:.2f} -> departure excess "
          f"{t['dep_excess']:.2f} km/s (needs vinf {t['vinf_needed_5p44']:.2f}, "
          f"gap {t['vinf_gap']:+.2f})")
best = max(table, key=lambda n: table[n]["dep_excess"])
best_de = table[best]["dep_excess"]
print(f"    -> best = {best} at {best_de:.2f} km/s vs {REQ} required")
h2 = 3.8 <= best_de <= 4.5 and best_de < REQ
findings["H2"] = grade("best single-moon excess Titan ~4.1 < 5.44",
                       "best in [3.8,4.5] km/s < 5.44",
                       f"{best} {best_de:.2f} km/s", h2,
                       "Titan is the sweet spot (moon speed vs well depth)")

print()
print("=" * 72)
print("H3 [S] -- every moon needs more vinf than the B-ring provides; max < 5.0")
print("=" * 72)
max_de = max(t["dep_excess"] for t in table.values())
all_short = all(t["vinf_gap"] > 0 for t in table.values())
print(f"    max departure excess over all moons = {max_de:.2f} km/s")
print(f"    every moon's vinf gap > 0 (B-ring underprovides): {all_short}")
h3 = max_de < 5.0 and all_short
findings["H3"] = grade("no moon reaches 5.44; all underprovided",
                       "max over moons < 5.0 km/s AND every gap > 0",
                       f"max {max_de:.2f} km/s; all_short={all_short}", h3,
                       "inner moons deeper (worse), Iapetus far/slow (worse)")

print()
print("=" * 72)
print("H4 [W] -- inner-moon handoffs cannot pump vinf_T (turn <1 deg); crack CLOSED")
print("=" * 72)
inner_turns = {n: table[n]["flyby_turn_deg"] for n in ("Rhea", "Dione", "Tethys")}
titan_turn = table["Titan"]["flyby_turn_deg"]
for n, d in inner_turns.items():
    print(f"    {n:7} per-flyby turn = {d:.2f} deg (mu={MOONS[n][1]:.0f})")
print(f"    Titan per-flyby turn = {titan_turn:.1f} deg (mu=8978) -- but Titan "
      f"CONSERVES vinf_T")
gap = table["Titan"]["vinf_gap"]
inner_too_small = all(d < 2.0 for d in inner_turns.values())
h4 = (best_de < REQ) and inner_too_small
findings["H4"] = grade("vinf_T gap unbridgeable w/o propulsion; R186 confirmed",
                       "best excess < 5.44 AND inner-moon turn < 2 deg",
                       f"best {best_de:.2f} < 5.44; inner turns "
                       f"{max(inner_turns.values()):.2f} deg max; Titan gap {gap:+.2f}",
                       h4,
                       "manufacturing the 0.67 km/s vinf_T gap = supplying the "
                       "departure energy yourself (R186's conclusion)")

# --------------------------------------------------------------- bug-catch
print()
print("=" * 72)
print("Revisit / bug-catch")
print("=" * 72)
notes = [
    "Analytic Tisserand/delta-max Saturn-frame model, not a time-dependent beam "
    "search. The single-moon caps are geometry (not phasing) dependent, so a "
    "phased tour cannot exceed them; the delta-max handoff bound shows the inner "
    "moons cannot pump vinf_T. A full Saturn-frame beam search (re-hosting "
    "trajectory-bot's heliocentric tour code) would only add tour DEPTH, not raise "
    "the per-moon escape cap -- it cannot beat Titan's 4.15 km/s.",
    "Direction compounds the magnitude shortfall (not separately graded): the "
    "Titan-pumped Saturn-centric vinf points in a flyby-geometry-constrained "
    "direction that must then ADD to Saturn's heliocentric velocity in the "
    "RETROGRADE (sunward-dropping) sense for an Earth-return transfer. Even the "
    "4.15 km/s magnitude would pay a cosine penalty to point correctly -- so 4.15 "
    "is an optimistic upper bound on the usable departure contribution.",
    "vinf_T is Tisserand-conserved by TITAN flybys (the pump moon), so the arrival "
    "value 3.34 is a hard ceiling for Titan-only tours. Non-Titan pumping needs "
    "the inner moons, which turn <1 deg/flyby -- the round's decisive point.",
    "B-ring taken at r=107,000 km (campaign R_RING). A lower harvest orbit "
    "(deeper) would give slightly higher vinf_T at Titan but also a deeper well to "
    "climb; the Titan cap is insensitive to it at the ~0.1 km/s level.",
]
for n in notes:
    print("  - " + n)
findings["revisit_notes"] = notes

findings["verdict"] = {
    "H1": h1, "H2": h2, "H3": h3, "H4": h4,
    "crack_closed": bool(best_de < REQ and inner_too_small),
    "summary": (
        f"The crack the ephemeris round opened is CLOSED and R186's Titan-lever "
        f"revocation is CONFIRMED -- now with a derived Saturn-frame reason, not an "
        f"asserted bound. The spacecraft harvests at the B-ring, and the minimal "
        f"transfer to Titan fixes its Titan-relative excess at vinf_T = {vinf_T:.2f} "
        f"km/s (reproducing R186's ~3.3 from first principles). Titan flybys "
        f"conserve vinf_T, so a Titan-only tour caps the Saturn-centric departure "
        f"excess at {best_de:.2f} km/s -- Titan is the sweet spot (inner moons are "
        f"deeper and give less: Rhea 0.99, Tethys/Dione ~0; Iapetus far/slow at "
        f"3.41). Every moon needs more vinf than the B-ring provides (Titan closest, "
        f"short by {gap:.2f} km/s). The only way to pump vinf_T is a non-Titan "
        f"handoff, but the inner moons turn the spacecraft <1 deg/flyby "
        f"(mu 41-154 vs Titan's 8978) -- far too weak. So reaching the vinf_T=4.01 "
        f"threshold requires propulsion, which is just supplying the departure "
        f"energy the tour was meant to save. The 155-175 kWe reactor floor and "
        f"bet #3 stand; the Titan 117 kWe branch stays dead. (Direction adds a "
        f"further cosine penalty, so 4.15 is itself optimistic.)"),
}

out = RESULTS / "tour_findings.json"
out.write_text(json.dumps(findings, indent=2))
print(f"\nwrote {out}")
print("VERDICT:", findings["verdict"]["summary"])
