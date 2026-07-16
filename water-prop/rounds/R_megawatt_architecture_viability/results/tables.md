# R-megawatt-architecture-viability — results tables

## 1. Round-trip at megawatt all-electric across MARVL-anchored dry mass

Hohmann round-trip cruise = 12.17 yr (one-way × 2).
Outbound delta-velocity = 17.97 km/s (Edelbaum + heliocentric).
Inbound delta-velocity = 6.42 km/s.
Reactor 1000 kWe, Isp 2000 s, eta 0.65, chunk 200 t.
Redundancy overlay (from R-redundancy-budget-cost) = 12.76 t.

| Dry mass (t) | Baseline RT (yr) | Baseline margin (yr) | Clears? | + overlay RT (yr) | + overlay margin (yr) | Clears? |
|---|---|---|---|---|---|---|
| 29 | 13.93 | +1.07 | yes | 14.04 | +0.96 | yes |
| 50 | 14.11 | +0.89 | yes | 14.21 | +0.79 | yes |
| 70 | 14.27 | +0.73 | yes | 14.38 | +0.62 | yes |
| 80 | 14.36 | +0.64 | yes | 14.46 | +0.54 | yes |
| 90 | 14.44 | +0.56 | yes | 14.54 | +0.46 | yes |
| 100 | 14.52 | +0.48 | yes | 14.63 | +0.37 | yes |
| 105 | 14.56 | +0.44 | yes | 14.67 | +0.33 | yes |
| 110 | 14.60 | +0.40 | yes | 14.71 | +0.29 | yes |
| 120 | 14.68 | +0.32 | yes | 14.79 | +0.21 | yes |
| 130 | 14.77 | +0.23 | yes | 14.87 | +0.13 | yes |
| 140 | 14.85 | +0.15 | yes | 14.96 | +0.04 | yes |
| 150 | 14.93 | +0.07 | yes | 15.04 | -0.04 | NO |
| 160 | 15.01 | -0.01 | NO | 15.12 | -0.12 | NO |
| 180 | 15.18 | -0.18 | NO | 15.28 | -0.28 | NO |
| 200 | 15.34 | -0.34 | NO | 15.45 | -0.45 | NO |

**Max dry mass clearing L0-05 baseline:** 150 t.
**Max dry mass clearing L0-05 with redundancy overlay:** 140 t.

**MARVL-anchored dry-mass band 70–150 t** (per H-r4-a) — closes baseline up to 150.0 t, closes-with-overlay up to 140.0 t.

## 2. Bayesian posteriors on fission-flight delivery by 2032–2035

Three priors applied to 0-of-6 historical evidence (SNAP-10A 1965 was the only US fission reactor orbited; SP-100, Project Timberwind, Prometheus/JIMO, DARPA DRACO, Kilopower flight, FSP all failed/not-yet-awarded). FY2026 budget zero added as a 0.5 failure-equivalent for megawatt-class. Kilopower variant B gets KRUSTY ground-demo +0.5 success credit.

| Prior | Megawatt (0/6) | Megawatt (0/6 + FY2026 budget) | Kilopower-B (+ KRUSTY credit) |
|---|---|---|---|
| uniform_Beta_1_1 | 0.125 (CI [0.00, 0.35]) | 0.118 (CI [0.00, 0.33]) | 0.176 (CI [0.00, 0.42]) |
| Jeffreys_Beta_0p5_0p5 | 0.071 (CI [0.00, 0.25]) | 0.067 (CI [0.00, 0.24]) | 0.133 (CI [0.00, 0.37]) |
| weakly_favorable_Beta_2_2 | 0.200 (CI [0.00, 0.44]) | 0.190 (CI [0.00, 0.42]) | 0.238 (CI [0.00, 0.49]) |

**Reading:** posterior mean for megawatt-class delivery by 2035 sits in [0.07, 0.20] across priors with FY2026 budget evidence. Kilopower-B with KRUSTY credit is in [0.10, 0.25]. Neither is the matrix's implicit confidence (which appears to be >0.5 for both cells, given they are listed as baseline architecture options).

## 3. Cell verdict

MARVL-anchored mass + base-rate Bayesian posterior:

- **Megawatt all-electric cell:** at bundled-formula 105 t dry, round-trip = 14.56 yr baseline / 14.67 yr with overlay. L0-05 margin tight (~+0.44 yr baseline). Base-rate posterior 0.07–0.20. **Verdict: upside-only, not a defensible baseline.**
- **Kilopower variant B cell:** not modelled in this round (different architecture). Base-rate posterior 0.10–0.25 with KRUSTY credit. **Verdict: contingent on Kilopower flight program that has not been funded as of May 2026.**
- **Matrix verdict:** the clean two-cell binary collapses. Both cells carry undocumented program-risk. Spawn R-non-fission-baseline to identify an architecture that does not depend on a fission flight program that has not been funded.