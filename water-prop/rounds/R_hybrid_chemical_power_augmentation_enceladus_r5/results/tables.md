# R-hybrid-chemical-power-augmentation — headline tables

Total cells swept: **2400**.

## Closure counts

| Gate | Count | of feasible |
|---|---|---|
| Feasible (delivered > 0) | 460 | 460/2400 |
| Pass L0-05 strict (RT ≤ 15 yr) | 2 | 2/460 |
| Pass L0-05 waiver (RT ≤ 25 yr) | 18 | 18/460 |
| Pass reactor life (burn ≤ 10 yr) | 2 | 2/460 |
| Launchable (LEO stack ≤ 2× Starship = 300 t) | 386 | 386/460 |
| **All three (waiver+life+launchable)** | **2** | **2/460** |

## Minimum hydrolox to close (P_reactor = 10 kWe, eta=0.5, sp=5 W/kg, isp=2000s)

| Chunk t | aero=0, min M(t) close waiver | aero=10, min M(t) close waiver | min M close strict |
|---|---|---|---|
| 5 | none | none | none |
| 10 | none | none | none |
| 50 | none | none | none |
| 100 | none | none | none |
| 200 | none | none | none |

## All-pass cells (closure on waiver + life + launchable)

| P_kWe | M_H2O2 t | chunk t | η_gen | sp W/kg | aero km/s | isp s | t_burn yr | RT yr | delivered t | LEO stack t |
|---|---|---|---|---|---|---|---|---|---|---|
| 50 | 0 | 50 | 0.30 | 5.0 | 10 | 2000 | 7.77 | 14.77 | 5.36 | 33.5 |
| 50 | 0 | 50 | 0.50 | 5.0 | 10 | 2000 | 7.77 | 14.77 | 5.36 | 33.5 |

## Hydrolox is strictly net-harmful — illustrative sweep (P=50 kWe, chunk=100 t, sp=5, η=0.5, aero=10, isp=2000)

| M_H2O2 t | delivered t | t_burn yr | RT yr | feasible |
|---|---|---|---|---|
| 0 | 28.64 | 12.43 | 19.43 | True |
| 100 | 6.47 | 15.86 | 22.86 | True |
| 250 | 0.00 | 0.00 | 0.00 | False |
| 500 | 0.00 | 0.00 | 0.00 | False |
| 1000 | 0.00 | 0.00 | 0.00 | False |
| 2500 | 0.00 | 0.00 | 0.00 | False |

## Best delivered chunk (any M_H2O2) at sp=5, η=0.5, aero=10, isp=2000

Demonstrates pure-reactor architecture dominates hybrid across the entire (P, chunk) grid.

| P kWe | chunk t | best delivered t | best M_H2O2 | RT yr | t_burn yr | closure? |
|---|---|---|---|---|---|---|
| 1 | 5 | infeasible | — | — | — | — |
| 1 | 10 | infeasible | — | — | — | — |
| 1 | 50 | 10.86 | 0 | 347.75 | 340.75 | False |
| 1 | 100 | 34.14 | 0 | 580.48 | 573.48 | False |
| 1 | 200 | 80.68 | 0 | 1045.93 | 1038.93 | False |
| 5 | 5 | infeasible | — | — | — | — |
| 5 | 10 | infeasible | — | — | — | — |
| 5 | 50 | 10.42 | 0 | 75.93 | 68.93 | False |
| 5 | 100 | 33.69 | 0 | 122.48 | 115.48 | False |
| 5 | 200 | 80.23 | 0 | 215.57 | 208.57 | False |
| 10 | 5 | infeasible | — | — | — | — |
| 10 | 10 | infeasible | — | — | — | — |
| 10 | 50 | 9.85 | 0 | 41.96 | 34.96 | False |
| 10 | 100 | 33.13 | 0 | 65.23 | 58.23 | False |
| 10 | 200 | 79.67 | 0 | 111.77 | 104.77 | False |
| 20 | 5 | infeasible | — | — | — | — |
| 20 | 10 | infeasible | — | — | — | — |
| 20 | 50 | 8.73 | 0 | 24.97 | 17.97 | False |
| 20 | 100 | 32.00 | 0 | 36.60 | 29.60 | False |
| 20 | 200 | 78.55 | 0 | 59.87 | 52.87 | False |
| 50 | 5 | infeasible | — | — | — | — |
| 50 | 10 | infeasible | — | — | — | — |
| 50 | 50 | 5.36 | 0 | 14.77 | 7.77 | True |
| 50 | 100 | 28.64 | 0 | 19.43 | 12.43 | False |
| 50 | 200 | 75.18 | 0 | 28.74 | 21.74 | False |

## Analytic dv-tax derivation

Parasitic-mass Tsiolkovsky: `dv = v_e × [M_thrust / (M_thrust + M_hydrolox)] × ln(m_0/m_f)`.

Hydrolox supplies energy proportional to its mass: `E_gen = M_hydrolox × LHV × η_gen`.

From power-limited rocket equation, M_thrust-equivalent from hydrolox energy: `ΔM_thrust = α × M_hydrolox`, where 
`α = 2 × η_thr × LHV × η_gen / v_e² = 2 × 0.7 × 1.34e+07 × 0.5 / (19613)² = **0.0244**` at η_gen=0.5, v_e=19613 m/s.

Asymptotic dv-tax: as M_hydrolox → ∞ (reactor irrelevant), max ratio of dv per unit v_e → α/(α+1) ≈ 0.024, i.e., ~97.6% of v_e wasted.

**Interpretation:** at v_e ≈ 20 km/s, every kg of brought hydrolox supplies energy for ~24 g of additional thrust-propellant mass, but burdens the rocket with 1 kg of parasitic mass through the burn. The break-even point requires reactor-supplied M_thrust >> 41 × M_hydrolox — at which point reactor energy is dominant and hydrolox is a marginal effect, not architectural.

## Hypothesis grades

| # | predicted | measured | verdict |
|---|---|---|---|
| H1 | 0 close at L0-05 strict (200t chunk, 10 kWe) | 0 of 20 cells close strict | HELD |
| H2 | >=1 close cell at chunk<=50, M in [100,500], RT<=25 yr | 0 of 72 cells close waiver | FALSIFIED |
| H3 | >=1 reactor-only cell delivers >=1t at chunk<=10, RT<=40 yr | 0 of 16 cells deliver >=1t under RT<=40 | FALSIFIED |
| H4 | cliff (M_close > 1000 t) at delivered chunk in [20, 80] t | no closure at any chunk for P=10 kWe (cliff undefined) | FALSIFIED-VACUOUSLY (no closure region exists at P=10 kWe regardless of chunk) |
| H5 | surviving H2-cell RT in [22, 30] yr | no surviving H2 cells (predicate-failure) | VACUOUS (H2 falsified; RT range undefined) |
| H6 | M_close linear in chunk_mass within +/-15% | M_close undefined at every chunk for P=10 kWe; hydrolox is strictly net-harmful for dv (parasitic-mass tax dominates) | FALSIFIED-VACUOUSLY (M_close undefined; linearity meaningless) |
| H-strict-dominance | (post-hoc) for every (P, chunk) cell, best delivered mass is at M_H2O2 = 0 | 29 of 29 (P, chunk) cells confirm best at M=0 | HELD |
