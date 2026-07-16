# R-hybrid-power-generator-exhaust-revisit — headline tables

**Revisits R-hybrid-chemical-power-augmentation (commit `98a9ded`).** The prior round assumed gas-generator exhaust contributes zero thrust. This round runs the two-stream rocket equation with hydrolox-chemical thrust at the post-turbine residual specific impulse.

## Two-stream rocket equation

At Isp 2000 s: v_e_water = 19613 m/s. At η_gen=0.5 + η_nozzle=0.85: v_e_hydrolox = 3375 m/s. At η_gen=0.0 (pure chemical): v_e_hydrolox = 4773 m/s (~Isp 487 s, close to actual stoichiometric H2/O2 chemical-rocket performance).

η_thruster revised down to **0.5** (water-electric MET / arcjet class; prior round used 0.7 = Hall-class, optimistic for water propellant).

## Closure counts (total cells = 5040)

| Gate | Count |
|---|---|
| Feasible | 1037 |
| Pass L0-05 strict (≤15 yr) | 0 |
| Pass L0-05 waiver (≤25 yr) | 55 |
| Pass reactor life (≤10 yr) | 5 |
| Launchable (≤300 t LEO stack) | 795 |
| **All-pass waiver** | **5** |
| **All-pass strict** | **0** |

## All-pass-waiver cells (top 30 by delivered chunk)

| P_kWe | M_h t | chunk t | η_gen | sp W/kg | aero km/s | isp s | bus | v_e_eff m/s | t_burn yr | RT yr | delivered t | LEO t |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 50 | 0 | 50 | 0.00 | 5.0 | 10 | 2000 | demo | 19613 | 8.80 | 15.80 | 13.92 | 18 |
| 50 | 0 | 50 | 0.30 | 5.0 | 10 | 2000 | demo | 19613 | 8.80 | 15.80 | 13.92 | 18 |
| 50 | 0 | 50 | 0.50 | 5.0 | 10 | 2000 | demo | 19613 | 8.80 | 15.80 | 13.92 | 18 |
| 50 | 50 | 50 | 0.00 | 5.0 | 10 | 2000 | demo | 11352 | 9.71 | 16.71 | 10.18 | 72 |
| 50 | 50 | 50 | 0.30 | 5.0 | 10 | 2000 | demo | 11037 | 9.88 | 16.88 | 8.94 | 73 |

## Hydrolox sweep at P=10 kWe, chunk=50, aero=10 km/s, full bus, sp=5 W/kg, Isp=2000

| η_gen | M_h t | feasible | dv_ach m/s | t_burn yr | RT yr | delivered t | LEO t |
|---|---|---|---|---|---|---|---|
| 0.00 | 0 | True | 15000 | 48.94 | 55.94 | 9.85 | 25 |
| 0.00 | 50 | True | 15000 | 53.57 | 60.57 | 6.06 | 80 |
| 0.00 | 100 | True | 15000 | 57.14 | 64.14 | 3.12 | 135 |
| 0.00 | 250 | False | 14087 | 0.00 | 0.00 | 0.00 | 300 |
| 0.00 | 500 | False | 12972 | 0.00 | 0.00 | 0.00 | 575 |
| 0.00 | 1000 | False | 12274 | 0.00 | 0.00 | 0.00 | 1125 |
| 0.00 | 2500 | False | 11794 | 0.00 | 0.00 | 0.00 | 2775 |
| 0.30 | 0 | True | 15000 | 48.94 | 55.94 | 9.85 | 25 |
| 0.30 | 50 | True | 15000 | 54.43 | 61.43 | 4.83 | 80 |
| 0.30 | 100 | True | 15000 | 58.72 | 65.72 | 0.79 | 135 |
| 0.30 | 250 | False | 12824 | 0.00 | 0.00 | 0.00 | 300 |
| 0.30 | 500 | False | 11471 | 0.00 | 0.00 | 0.00 | 575 |
| 0.30 | 1000 | False | 10611 | 0.00 | 0.00 | 0.00 | 1125 |
| 0.30 | 2500 | False | 10014 | 0.00 | 0.00 | 0.00 | 2775 |
| 0.50 | 0 | True | 15000 | 48.94 | 55.94 | 9.85 | 25 |
| 0.50 | 50 | True | 15000 | 55.19 | 62.19 | 3.85 | 80 |
| 0.50 | 100 | False | 14609 | 0.00 | 0.00 | 0.00 | 135 |
| 0.50 | 250 | False | 11822 | 0.00 | 0.00 | 0.00 | 300 |
| 0.50 | 500 | False | 10279 | 0.00 | 0.00 | 0.00 | 575 |
| 0.50 | 1000 | False | 9292 | 0.00 | 0.00 | 0.00 | 1125 |
| 0.50 | 2500 | False | 8602 | 0.00 | 0.00 | 0.00 | 2775 |

## Hypothesis grades

| # | predicted | measured | verdict |
|---|---|---|---|
| H1 | P=10 kWe + chunk=50 t + aero=10 km/s + full bus closes some M_h | 0 of 28 cells all-pass | FALSIFIED |
| H2 | P=10 kWe + chunk=200 + eta=0.5: no L0-05-strict all-pass closure | 0 of 28 cells all-pass strict | HELD |
| H3 | optimal eta_gen is interior (in (0, 0.5)) | 0 of 4 cells show interior optimum; details=[{"P": 10.0, "chunk": 100.0, "M_h": 250.0, "best_eta_gen": 0.0, "best_delivered": 17.684013671875007}, {"P": 10.0, "chunk": 100.0, "M_h": 500.0, "best_eta_g... | FALSIFIED |
| H4 | demonstrator-class (chunk<=10, demo bus, aero=10): some closure | 0 of 168 cells all-pass | FALSIFIED |
| H5 | at 200-t chunk + 10 kWe, hybrid still fails L0-05 strict | 0 of 84 cells all-pass strict | HELD |
| H6 | prior-round 'M_h=0 strictly dominates' is FALSIFIED at two-stream physics | best M_h at primary regime = 0.0 (delivered 9.85 t) | FALSIFIED |
