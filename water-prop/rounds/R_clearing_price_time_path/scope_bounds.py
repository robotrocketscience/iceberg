#!/usr/bin/env python3
"""Pre-script: R-clearing-price-time-path bounds.

R183 swept water-price decay as a free parameter and flagged: "the
price-decay path has NO campaign anchor." This round supplies it from
external data, and finds the empirical value sits deep inside R183's
kill zone.

The load-bearing economic claim: ICEBERG sells water at a destination.
At any Earth-ACCESSIBLE destination (LEO / cislunar), the clearing price
is bounded above by the cheapest substitute — Earth-launched propellant.
That substitute's price rides the launch-cost experience curve, which is
falling fast. So the price ICEBERG can charge DECAYS on the launch curve,
over the mission's own multi-decade decision-to-delivery timeline.

External anchors (cited in SCOPE):
  P_LEO_0  water/propellant clearing price in LEO, 2025:
           $3,000-4,000/kg (Earth launch ~$3,868/kg 2025; lunar
           propellant valued at 25% discount ~$3,000/kg in LEO).
  decline  launch $/kg to LEO: $3,868 (2025) -> ~$273 (2040) median
           (PNAS Nexus experience curve; Starlust). Conservative: -45%
           by 2030 / -75% by 2040. Bull (Citi): ~$30/kg by 2040.
  R183     3%/yr price decay ALONE sinks even the paper-kappa relay at
           the 8% hurdle (its kill threshold).

Timeline anchors (inherited): round trip ~13 yr; R183 full paper
decision-to-first-delivery 23.5 yr; development lead alone ~10 yr.
Hurdles: 8% utility / 10% growth (R183). Deep-space substitute: Earth
LEO->destination rocket-equation multiplier at chemical Isp 450 s
(VE 4414 m/s) over delta-v {10, 15, 20} km/s.

Grids here SPAN the run grids (R182 lesson): rate in [0.03, 0.32],
T in [10, 23.5], dv_deep in [10, 20] km/s.
"""
import math

# --- H1: the LEO clearing-price anchor ---
LAUNCH_2025 = 3868.0            # $/kg to LEO, 2025 (PNAS/Starlust)
DISCOUNT = 0.25                 # ISRU price concession vs Earth-launched
P_LEO_LO = 3000.0
P_LEO_HI = 4000.0
p_leo_0 = LAUNCH_2025 * (1.0 - DISCOUNT)   # ~2901; ~= band floor 3000
p_leo_central = 3500.0
print("== H1: LEO water/propellant clearing price, 2025 ==")
print(f"  Earth launch 2025 {LAUNCH_2025:.0f} $/kg; ISRU at {DISCOUNT:.0%} "
      f"discount -> {p_leo_0:.0f} $/kg; band {P_LEO_LO:.0f}-{P_LEO_HI:.0f}, "
      f"central {p_leo_central:.0f}")

# --- H2: the decline rate from the experience curve ---
LAUNCH_2040_MED = 273.0        # $/kg to LEO, 2040 median
YRS = 2040 - 2025
rate_med = math.log(LAUNCH_2025 / LAUNCH_2040_MED) / YRS
rate_cons = -math.log(0.25) / YRS          # -75% by 2040 = factor 4
rate_bull = math.log(LAUNCH_2025 / 30.0) / YRS
rate_central = math.sqrt(rate_med * rate_cons)   # geometric mid
R183_KILL = 0.03
print("\n== H2: launch-cost experience-curve decline rate ==")
print(f"  conservative (-75% by 2040): {rate_cons*100:.1f}%/yr")
print(f"  median ({LAUNCH_2025:.0f}->{LAUNCH_2040_MED:.0f}): "
      f"{rate_med*100:.1f}%/yr")
print(f"  bull (->$30/kg): {rate_bull*100:.1f}%/yr")
print(f"  central (geo-mid cons/med): {rate_central*100:.1f}%/yr")
print(f"  R183 kill threshold: {R183_KILL*100:.0f}%/yr -> empirical is "
      f"{rate_cons/R183_KILL:.1f}-{rate_med/R183_KILL:.1f}x the rate that "
      f"already sinks the waiver NPV")

# --- H3: the timeline multiplier and the combined effective rate ---
print("\n== H3: price at delivery, and the effective revenue discount ==")
for T, tag in ((13.0, "round trip only"), (23.5, "R183 full timeline")):
    for r, rtag in ((rate_cons, "cons"), (rate_central, "central"),
                    (rate_med, "median")):
        fall = math.exp(r * T)
        print(f"  T={T:>4} yr ({tag:<18}) {rtag:>7} {r*100:4.1f}%/yr: "
              f"substitute price falls {fall:5.1f}x "
              f"(delivery price = {1/fall*100:4.1f}% of decision-time)")
print("  combined effective revenue rate = hurdle + decline:")
for h, htag in ((0.08, "8% utility"), (0.10, "10% growth")):
    eff = h + rate_central
    df = math.exp(-eff * 23.5)
    print(f"    {htag}: {eff*100:.1f}%/yr -> revenue discount factor over "
          f"23.5 yr = {df*100:.2f}% (decline ALONE {rate_central*100:.0f}% "
          f"> hurdle {h*100:.0f}%)")

# --- H4 [W]: the dilemma — deep-space substitute price, but no market ---
print("\n== H4: the surviving niche (deep-space substitute price) ==")
VE_CHEM = 450.0 * 9.80665
for dv in (10e3, 15e3, 20e3):
    mult = math.exp(dv / VE_CHEM)
    print(f"  Earth-LEO->deep-space at {dv/1e3:.0f} km/s: rocket-eq "
          f"multiplier {mult:5.1f}x -> substitute price "
          f"{p_leo_central*mult/1000:6.0f} k$/kg at destination")
mult15 = math.exp(15e3 / VE_CHEM)
print(f"  deep-space clearing price ~{mult15:.0f}x LEO — but that market "
      f"requires outer-system demand absent in the window and itself gated "
      f"on cheap launch. The dilemma: sell cheap (LEO, racing substitute) "
      f"or dear (deep space, no customers).")

# --- break-even decline rate at each hurdle (keystone) ---
print("\n== keystone: max tolerable decline rate ==")
print("  R183's waiver NPV needs decline < 3%/yr at the 8% hurdle; the "
      "monolithic (state-of-record post-R187) needs revenue over a 23.5-yr "
      f"timeline to beat capital, i.e. decline << hurdle. Empirical central "
      f"{rate_central*100:.0f}%/yr exceeds BOTH hurdles outright.")
