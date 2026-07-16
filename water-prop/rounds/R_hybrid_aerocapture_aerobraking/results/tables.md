# R-hybrid-aerocapture-aerobraking — results tables

## Sweep summary

- Atmosphere model: US Standard 1976 / NRLMSISE-00 quiet-sun (NASA SP-3084)
- Total cells swept: 1920
- Cells where pass-1 captures (Δv ≥ Δv_insert): 230
- Cells where pass-1 chunk structurally survives (margin > 1.0): 1780
- Cells where pass-1 BOTH captures AND survives: 90
- **Cells satisfying all 5 closure conditions: 0**

## Cross-check vs hyperion's R-aerocapture-fast-cruise-envelope (Round F STRICT, periapsis 40 km)

| Atmosphere | Peak g | Chunk stress (MPa) | Tensile margin |
|---|---:|---:|---:|
| US Standard 1976 (this round) | 39.6 | 1.33 | 0.75 |
| Exponential (hyperion's) | 16.5 | 0.55 | 1.80 |
| Hyperion published (Round F STRICT) | 47.9 | 1.60 | 0.62 |

## Pass-1 envelope at anchor cell (chunk 200 t, tug 63.8 t, aphelion 11, no LGA)

| h₁ (km) | β (kg/m²) | ρ (kg/m³) | Δv/pass (m/s) | Δv-to-insert (km/s) | Captures | q_peak (MW/m²) | T_eq (K) | Peak g | Chunk stress (MPa) | Margin × | Pass-1 OK |
|---:|---:|---:|---:|---:|:---:|---:|---:|---:|---:|---:|:---:|
| 40 | 6022 | 4.00e-03 | 5537 | 4.14 | Y | 20.37 | 4604 | 39.6 | 1.329 | 0.75 | N |
| 50 | 6022 | 1.03e-03 | 1427 | 4.15 | N | 10.34 | 3885 | 10.2 | 0.342 | 2.92 | N |
| 60 | 6022 | 3.10e-04 | 457 | 4.16 | N | 5.67 | 3344 | 3.1 | 0.103 | 9.71 | N |
| 70 | 6022 | 8.28e-05 | 116 | 4.17 | N | 2.93 | 2835 | 0.8 | 0.028 | 36.34 | N |
| 75 | 6022 | 3.91e-05 | 52 | 4.17 | N | 2.02 | 2582 | 0.4 | 0.013 | 76.89 | N |
| 80 | 6022 | 1.85e-05 | 24 | 4.18 | N | 1.39 | 2351 | 0.2 | 0.006 | 162.66 | N |
| 85 | 6022 | 7.95e-06 | 10 | 4.18 | N | 0.91 | 2115 | 0.1 | 0.003 | 378.32 | N |
| 90 | 6022 | 3.42e-06 | 4 | 4.19 | N | 0.60 | 1904 | 0.0 | 0.001 | 879.89 | N |

## Aerobraking campaign at chunk 200 t / β=6,022, residual Δv assumed 3.0 km/s

| h₂ (km) | ρ (kg/m³) | Δv/pass (mm/s) | n_passes | Years | T_eq (K) | Total sublimation (t) | Within tolerance |
|---:|---:|---:|---:|---:|---:|---:|:---:|
| 110 | 9.71e-08 | 73.58 | 4.08e+04 | 9.3 | 851 | 77 | N |
| 130 | 8.48e-09 | 8.67 | 3.46e+05 | 78.9 | 627 | 259 | N |
| 150 | 2.08e-09 | 2.49 | 1.21e+06 | 275.0 | 525 | 521 | N |
| 180 | 5.20e-10 | 0.77 | 3.91e+06 | 892.0 | 441 | 1040 | N |
| 200 | 2.54e-10 | 0.43 | 7.05e+06 | 1607.9 | 403 | 1486 | N |

## Hypothesis grading

| Sub-claim | Central | Range | Computed | Held |
|---|---|---|---|:---:|
| H_hyb_a | 0.75 | [0.5, 1.0] | 0.7523 | True |
| H_hyb_b | 0.85 | [0.6, 1.2] | 0.9343 | True |
| H_hyb_c | 0.013 | [0.01, 0.03] | 0.01238 | True |
| H_hyb_d | 303000 | [100000, 1000000] | 3.46e+05 | True |
| H_hyb_e | 1505 | [500, 3000] | 258.5 | False |
| H_hyb_f | 702 | [500, 900] | 626.7 | True |
| H_hyb_g | 757 | [200, 1500] | 892 | True |
| H_hyb_h | 2.73 | [2.5, 3.0] | 2.721 | True |
| H_hyb_i | 0 | [0, 2] | 0 | True |
| H_hyb_j | 5-15 t | [3, 30] | deferred (TPS model out of scope per validity caveat — flagged) | deferred |

**Aggregate H-hyb-agg: 8/9 sub-claims held (plus 1 deferred), 0 closing cells. H-hyb-agg held: True.**