#!/usr/bin/env python3
"""Pre-script: R-shuttle-reuse-fleet bounds.

R182 named shuttle reuse (leave the reactor at Saturn) as the fleet
multiplier, implying steady-state launch-per-delivered near the
mothership-only 0.15 t/t. The reactor-lifetime anchor says otherwise:
Kilopower-class design life is a 10-year TARGET, not a measurement
(R_reactor_lifetime_vs_burn_time; National Academies: little lifetime
advancement) — and the currency is full-power-years (fpy). R182's own
winning cell burns 60 kWe for 10.4 fpy in ONE mission: the optimum
already sits past the design-life target.

Model: sortie fpy = sortie time (full power). Reactor serves sorties
until life L is exhausted; replacement reactor modules (kappa x P_s)
ride subsequent motherships; shuttle bus+bag (2.5 t) is the reusable
part. Mission size lifetime-capped. Kick 5.84, chunk 40 t, paper
kappa = 100 kg/kWe primary (flown 417 sensitivity), waiver schedule.
"""
import math

G0 = 9.80665
VE = 800.0 * G0
ETA = 0.6
YEAR = 3.156e7
KICK = 5.84
CHUNK = 40_000.0
R_WELL = math.exp(6700.0 / VE) - 1
RES_WAIVER = 12.9


def sortie_fpy(m_shuttle, p_kwe):
    prop = (m_shuttle + CHUNK) * R_WELL + m_shuttle * R_WELL
    return 0.5 * VE ** 2 * prop / ETA / (p_kwe * 1e3) / YEAR


print("== H1: lifetime adjudication of R182's optima (L = 10 fpy target) ==")
for name, kappa, p_s, n182 in (("paper", 100.0, 60.0, 5), ("flown", 417.0, 50.0, 3)):
    m_sh = 2500.0 + kappa * p_s
    t_s = sortie_fpy(m_sh, p_s)
    fpy = n182 * t_s
    n_cap = min(int(10.0 // t_s), int((RES_WAIVER - 1.0) // t_s))
    launch = (4000.0 + m_sh) * KICK / 1000
    print(f"{name}: R182 cell N={n182} -> {fpy:.1f} fpy "
          f"({'BUSTS' if fpy > 10 else 'ok'} 10-yr target); lifetime-capped "
          f"N={n_cap}, lpd {launch/(n_cap*40):.2f} (was {launch/(n182*40):.2f})")

print("\n== H2: steady-state with reactor-swap modules (paper, 60 kWe, N=4) ==")
m_sh = 2500.0 + 6000.0
t_s = sortie_fpy(m_sh, 60.0)
first = (4000.0 + m_sh) * KICK / 1000
swap = (4000.0 + 6000.0) * KICK / 1000
print(f"sortie {t_s:.2f} fpy; first mission {first:.0f} t -> lpd {first/160:.2f}")
print(f"swap mission {swap:.0f} t -> steady lpd {swap/160:.3f}")
print(f"reactor share of recurring launch: {6000*KICK/1000/swap:.0%}")
print(f"naive reactor-immortal dream: {4000.0*KICK/1000/160:.3f} (registered comparator)")
for k in (2, 3, 5):
    avg = (first + (k - 1) * swap) / (k * 160)
    print(f"fleet-average over K={k}: {avg:.3f}")

print("\n== H3: design-life sensitivity (steady-state lpd) ==")
for L in (10.0, 15.0, 20.0, 40.0):
    sorties_per_reactor = L / t_s
    reactors_per_mission = 4.0 / sorties_per_reactor
    steady = (4000.0 + reactors_per_mission * 6000.0) * KICK / 1000 / 160
    print(f"L {L:4.0f} fpy: {sorties_per_reactor:.1f} sorties/reactor, "
          f"{reactors_per_mission:.2f} reactors/mission, steady lpd {steady:.3f}")

print("\n== cross-cite R183 ==")
d_star = math.exp(math.log(1.02 / (swap / 160)) / 10.4) - 1
print(f"steady-state advantage vs monolithic: {1.02/(swap/160):.2f}x -> "
      f"waiver break-even d* {d_star*100:.1f}% (restores the R183 octant "
      f"boundary toward 10.5%)")
