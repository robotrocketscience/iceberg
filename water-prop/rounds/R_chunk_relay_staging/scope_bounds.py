#!/usr/bin/env python3
"""Pre-script: R-chunk-relay-staging bounds.

R179's surviving-maybe: a dive shuttle transits the +-6.7 km/s well while
the mothership waits on the staging ellipse (peri at ring, apo at Titan)
and departs via the pump-up tour. Saturn-side scope only; both
architectures share Earth-arrival handling, and the tour delivers the
exact Hohmann v-inf so the relay's heliocentric legs are no worse than
the monolithic's spread-spiral (parity assumed, stated).

Anchors: well transit 6.70 km/s each way (R179, flyby-irreducible);
MET 800 s, eta_thr 0.6; reactor specific mass kappa in {417 flown
KRUSTY 2.4 W/kg, 100 paper 10 W/kg} kg/kWe (R_arch_E_specific_power_
flown_anchored; >10 W/kg is paper-study per National Academies 2021);
monolithic state-of-record: 30 kWe chunk-fed spiral spread over the
8-yr return transit (mission_graph phase4), bus+bag 4 t; kick multiplier
5.84 (R176 2-stage); audit baseline 50 t / 40 t. Schedule: L0-05 strict
residence budget ~2.9 yr (15 - 12.1 transit), waiver budget ~12.9 yr
(25-yr ceiling), capture tour 1 yr.

Key structural facts the hypotheses register:
 - N=1 relay is strictly worse (extra mothership, same well transit,
   sortie clocked against residence instead of spread over transit);
 - at N>=2 the relay amortizes the mothership+kick and, unlike the
   monolithic, launches the reactor once for N chunks;
 - sortie tempo is power-limited; strict schedule kills multi-chunk.
"""
import math

G0 = 9.80665
VE = 800.0 * G0
ETA = 0.6
YEAR = 3.156e7
DV_WELL = 6700.0
KICK = 5.84
CHUNK = 40_000.0
BUS_BAG = 4_000.0          # monolithic bus + bag
M_SHIP_BUS = 4_000.0       # relay mothership bus (no bag, no reactor)
SHUTTLE_BUS_BAG = 2_500.0
P_MONO = 30.0              # kWe, spread-spiral state of record
T_TOUR = 1.0               # yr, capture pump-down
RES_STRICT = 15.0 - 12.1
RES_WAIVER = 25.0 - 12.1


def sortie(m_shuttle, p_kwe):
    """(water per chunk [kg], sortie time [yr]) for one down+up cycle."""
    prop_up = (m_shuttle + CHUNK) * (math.exp(DV_WELL / VE) - 1)
    prop_dn = m_shuttle * (math.exp(DV_WELL / VE) - 1)
    e = 0.5 * VE ** 2 * (prop_up + prop_dn) / ETA
    return prop_up + prop_dn, e / (p_kwe * 1e3) / YEAR


def relay(kappa, p_s, n):
    m_sh = SHUTTLE_BUS_BAG + kappa * p_s
    water, t_sortie = sortie(m_sh, p_s)
    dry = M_SHIP_BUS + m_sh
    launch = dry * KICK / 1000.0
    res = T_TOUR + n * t_sortie
    return {"launch_t": launch, "lpd": launch / (n * CHUNK / 1000),
            "water_per_chunk_t": water / 1000, "t_sortie_yr": t_sortie,
            "residence_yr": res, "strict_ok": res <= RES_STRICT,
            "waiver_ok": res <= RES_WAIVER}


def monolithic(kappa):
    dry = BUS_BAG + kappa * P_MONO
    launch = dry * KICK / 1000.0
    prop = (dry + CHUNK) * (math.exp(9000.0 / VE) - 1)
    return {"launch_t": launch, "lpd": launch / (CHUNK / 1000),
            "water_per_chunk_t": prop / 1000}


print("== monolithic baseline (spread spiral, 30 kWe) ==")
for kappa, name in ((100.0, "paper 10 W/kg"), (417.0, "flown 2.4 W/kg")):
    m = monolithic(kappa)
    print(f"kappa {name}: launch {m['launch_t']:.0f} t/mission, "
          f"launch-per-delivered {m['lpd']:.2f}, water {m['water_per_chunk_t']:.0f} t/chunk"
          f"  (audit baseline 1.25)")

print("\n== relay sweep ==")
for kappa, name in ((100.0, "paper"), (417.0, "flown")):
    for p_s in (30.0, 60.0, 117.0, 190.0):
        for n in (1, 2, 3, 4):
            r = relay(kappa, p_s, n)
            mono = monolithic(kappa)
            edge = 1 - r["lpd"] / mono["lpd"]
            print(f"{name} P_s {p_s:5.0f} N={n}: lpd {r['lpd']:.2f} "
                  f"({edge:+.0%} vs mono), sortie {r['t_sortie_yr']:.1f} yr, "
                  f"residence {r['residence_yr']:.1f} yr "
                  f"[strict {'OK' if r['strict_ok'] else 'BUST'} / "
                  f"waiver {'OK' if r['waiver_ok'] else 'BUST'}], "
                  f"water {r['water_per_chunk_t']:.0f} t/chunk")

print("\n== headline probes ==")
r = relay(100.0, 60.0, 3)
print(f"paper/60kWe/N=3: lpd {r['lpd']:.2f} vs mono {monolithic(100.0)['lpd']:.2f}")
r = relay(417.0, 60.0, 3)
print(f"flown/60kWe/N=3: lpd {r['lpd']:.2f} vs mono {monolithic(417.0)['lpd']:.2f}")
# captures per delivered chunk (bet #1 exposure), both architectures
for kappa in (100.0, 417.0):
    m = monolithic(kappa)
    rl = relay(kappa, 60.0, 3)
    print(f"kappa {kappa:.0f}: harvest per delivered chunk — mono "
          f"{(m['water_per_chunk_t']+40)/40:.1f}x chunk mass, relay "
          f"{(rl['water_per_chunk_t']+40)/40:.1f}x")
