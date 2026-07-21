#!/usr/bin/env python3
"""Pre-script: R-waiver-value-consolidation bounds.

R182 called the L0-05 waiver "the most valuable programmatic lever." This
round prices that claim on the NPV side. Mechanism: the relay's launch-mass
advantage (R182: paper-kappa 1.02/0.36 = 2.83x, flown 2.41/1.33 = 1.81x)
is bought with delivery delay (relay returns all N chunks with the
mothership at ~23.5 yr vs the monolithic's ~13.1 yr — a 10.4-yr delay).
NPV per launched tonne: value ratio = mass_advantage / (1+d)^delay, where
d = discount + price-decay (no campaign time-path anchor for price decay
exists; swept openly as scenario). Campaign hurdles: 8 % regulated-utility,
10 % corporate-growth (R_launch_cost_sensitivity / R_NPV lineage).

Fairness lemma: per-launched-tonne NPV is cadence-invariant for the
monolithic fleet (K serial missions scale linearly), so the two-point
comparison is fleet-fair.
"""
import math

DELAY = 23.5 - 13.1
ADV = {"paper": 1.02 / 0.36, "flown": 2.41 / 1.33}

print(f"delivery delay: {DELAY:.1f} yr")
for tier, a in ADV.items():
    d_star = math.exp(math.log(a) / DELAY) - 1
    print(f"\n{tier}: mass advantage {a:.2f}x, break-even total rate "
          f"d* = {d_star*100:.1f}%")
    for d in (0.06, 0.08, 0.10, 0.12):
        for decay in (0.0, 0.03, 0.07):
            eff = (1 + d) * (1 + decay) - 1
            ratio = a / (1 + eff) ** DELAY
            tag = "WIN" if ratio > 1.05 else ("WASH" if ratio > 0.95 else "LOSE")
            print(f"  d {d*100:4.0f}% decay {decay*100:2.0f}%: NPV ratio "
                  f"{ratio:.2f} {tag}")
