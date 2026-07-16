# R-architecture-E-no-saturn-side-electrolysis — Results

## Closure summary across L0-05 ceiling relaxations

Of 120 cells (5 reactor × 4 chunk × 3 specific impulse × 2 mass model):
- closes 15-year ceiling with positive delivered: **0**
- closes 20-year ceiling with positive delivered: **0**
- closes 25-year ceiling with positive delivered: **18**
- closes 30-year ceiling with positive delivered: **30**

## Best Architecture E cell at each L0-05 ceiling (max delivered/launch-mass)

| Ceiling | Mass model | Reactor (kWe) | Chunk (t) | Isp (s) | Round-trip (yr) | Delivered (t) | Launch (t) | Delivered/Launch |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| ceiling_15yr | — | — | — | — | — | — | — | — |
| ceiling_20yr | — | — | — | — | — | — | — | — |
| ceiling_25yr | decomposed_marvl | 500 | 200 | 2934 | 23.60 | 50.0 | 168.7 | 0.296 |
| ceiling_30yr | decomposed_marvl | 200 | 100 | 2934 | 25.55 | 26.6 | 76.7 | 0.346 |

## Posterior cascade (Monte Carlo, 50,000 samples)

| Architecture | Posterior median | 5th percentile | 95th percentile | Mean |
|---|---:|---:|---:|---:|
| E_at_100kWe | 6.44% | 3.65% | 10.86% | 6.74% |
| E_at_200kWe | 4.78% | 2.60% | 8.40% | 5.04% |
| E_at_500kWe | 3.13% | 1.48% | 6.02% | 3.36% |
| E_at_1000kWe | 1.02% | 0.46% | 2.00% | 1.10% |
| variantB_500kWe | 0.60% | 0.25% | 1.34% | 0.67% |
| D_fission | 0.03% | 0.01% | 0.08% | 0.03% |
| D_solar_thermal | 0.06% | 0.02% | 0.15% | 0.07% |

## Fleet and net-present-value (8.7% weighted-average cost of capital, 40-yr horizon, cadence 2/yr)

Cost assumptions: $300 million per vehicle (Architecture E), $500 million per vehicle (Variant B).

| Architecture | Round-trip (yr) | Fleet size | Fleet capital ($M) | NPV @ $100M/mission | NPV @ $200M | NPV @ $500M | NPV @ $1000M |
|---|---:|---:|---:|---:|---:|---:|---:|
| ceiling_25yr | 23.60 | 47 | 14159 | -13903 | -13648 | -12880 | -11602 |
| ceiling_30yr | 25.55 | 51 | 15330 | -15126 | -14922 | -14310 | -13291 |
| variantB_reference | 14.50 | 29 | 14500 | -13867 | -13233 | -11334 | -8167 |

## Hypothesis grading

| Sub-claim | Predicted | Actual | Held? |
|---|---|---|---|
| H-E-a — 200 kWe MARVL chunk 100 t Isp 2000 s closes 20-28 yr, positive delivered | 200 kWe MARVL, chunk 100 t, Isp 2000 s — closes with positive delivered, round-trip 20-28 yr | round-trip 22.54 yr, delivered 6.7 t | yes |
| H-E-b — Sweet-spot at 25-yr ceiling | reactor 200-500 kWe, chunk 50-100 t, Isp 2000-2934 s | reactor 500 kWe, chunk 200 t, Isp 2934 s | **no** |
| H-E-c — E posterior median (200 kWe) > Variant B median by 1.5-3× | 1.5-3× | E median 4.78%, B median 0.60%, ratio 8.00× | **no — falsified-high** |
| H-E-d — Fleet 50+ ships, $15B+ fleet capital at 25-yr ceiling | 50+ ships, $15B+ | fleet 47 ships, $14159 million | **no** |
| H-E-e — NPV-negative at $200M/mission, 8.7% WACC, 25-yr ceiling | NPV < 0 at $200M | NPV -13648 million | yes |