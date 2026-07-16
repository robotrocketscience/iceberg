# R-aerocapture-fast-cruise-envelope — results tables

## Cross-check against R-chunk-as-heat-shield

- Predicted entry velocity: 12.60 km/s
- Computed entry velocity (aphelion 9.58, 100 t, with LGA): 13.84 km/s
- Ratio computed/predicted: 1.098
- Predicted ablation: 0.50%  vs  Computed: 3.00%
- Predicted q_peak: 180 W/cm² vs Computed: 1095 W/cm²

Cross-check inside 10% — model anchored to validated point.

## Round F closing case verdict (aphelion 11 AU, 200 t chunk, 63.8 t tug)

| Metric | No LGA | With LGA (2 km/s credit) |
|---|---:|---:|
| Velocity-at-infinity at Earth (km/s) | 10.54 | 8.54 |
| Entry velocity (km/s) | 15.29 | 13.99 |
| Ballistic coefficient (kg/m²) | 6022 | 6022 |
| Periapsis altitude (km) | 40 | 40 |
| Pulse duration (s) | 41 | 44 |
| Peak heat flux (W/cm²) | 1316 | 1007 |
| Chunk ablation per pass (%) | 2.59 | 2.17 |
| Peak g-load | 47.9 | 36.3 |
| Chunk internal stress (kPa) | 1607 | 1219 |
| Tensile margin (×) | 0.62 | 0.82 |
| Envelope pass | False | False |
| Delivered after ablation (t) | 22.86 | 22.96 |

## All cases sweep — entry velocity, ablation, envelope-pass

| r_apo (AU) | chunk (t) | LGA | v_entry (km/s) | β (kg/m²) | periapsis (km) | q_peak (W/cm²) | ablation (%) | peak g | margin × | env pass |
|---:|---:|:---:|---:|---:|---:|---:|---:|---:|---:|:---:|
| 9.58 | 100 | Y | 13.84 | 5936 | 40 | 1095 | 3.00 | 35.1 | 1.07 | False |
| 9.58 | 100 | N | 15.12 | 5936 | 40 | 1429 | 3.58 | 46.3 | 0.81 | False |
| 9.58 | 200 | Y | 13.84 | 6022 | 40 | 975 | 2.12 | 35.1 | 0.85 | False |
| 9.58 | 200 | N | 15.12 | 6022 | 40 | 1273 | 2.53 | 46.3 | 0.64 | False |
| 9.58 | 264 | Y | 13.84 | 6218 | 40 | 931 | 1.85 | 35.1 | 0.77 | False |
| 9.58 | 264 | N | 15.12 | 6218 | 40 | 1215 | 2.20 | 46.3 | 0.59 | False |
| 9.58 | 350 | Y | 13.84 | 6505 | 40 | 888 | 1.60 | 35.1 | 0.70 | False |
| 9.58 | 350 | N | 15.12 | 6505 | 40 | 1159 | 1.91 | 46.3 | 0.53 | False |
| 10.50 | 100 | Y | 13.94 | 5936 | 40 | 1119 | 3.04 | 35.9 | 1.05 | False |
| 10.50 | 100 | N | 15.23 | 5936 | 40 | 1461 | 3.63 | 47.4 | 0.79 | False |
| 10.50 | 200 | Y | 13.94 | 6022 | 40 | 997 | 2.15 | 35.9 | 0.83 | False |
| 10.50 | 200 | N | 15.23 | 6022 | 40 | 1302 | 2.57 | 47.4 | 0.63 | False |
| 10.50 | 264 | Y | 13.94 | 6218 | 40 | 952 | 1.87 | 35.9 | 0.76 | False |
| 10.50 | 264 | N | 15.23 | 6218 | 40 | 1243 | 2.24 | 47.4 | 0.57 | False |
| 10.50 | 350 | Y | 13.94 | 6505 | 40 | 908 | 1.63 | 35.9 | 0.69 | False |
| 10.50 | 350 | N | 15.23 | 6505 | 40 | 1186 | 1.94 | 47.4 | 0.52 | False |
| 11.00 | 100 | Y | 13.99 | 5936 | 40 | 1131 | 3.06 | 36.3 | 1.03 | False |
| 11.00 | 100 | N | 15.29 | 5936 | 40 | 1477 | 3.66 | 47.9 | 0.78 | False |
| 11.00 | 200 | Y | 13.99 | 6022 | 40 | 1007 | 2.17 | 36.3 | 0.82 | False |
| 11.00 | 200 | N | 15.29 | 6022 | 40 | 1316 | 2.59 | 47.9 | 0.62 | False |
| 11.00 | 264 | Y | 13.99 | 6218 | 40 | 962 | 1.89 | 36.3 | 0.75 | False |
| 11.00 | 264 | N | 15.29 | 6218 | 40 | 1257 | 2.25 | 47.9 | 0.57 | False |
| 11.00 | 350 | Y | 13.99 | 6505 | 40 | 918 | 1.64 | 36.3 | 0.68 | False |
| 11.00 | 350 | N | 15.29 | 6505 | 40 | 1199 | 1.96 | 47.9 | 0.52 | False |
| 12.00 | 100 | Y | 14.07 | 5936 | 40 | 1152 | 3.10 | 37.0 | 1.01 | False |
| 12.00 | 100 | N | 15.39 | 5936 | 40 | 1506 | 3.71 | 48.8 | 0.77 | False |
| 12.00 | 200 | Y | 14.07 | 6022 | 40 | 1026 | 2.19 | 37.0 | 0.80 | False |
| 12.00 | 200 | N | 15.39 | 6022 | 40 | 1341 | 2.62 | 48.8 | 0.61 | False |
| 12.00 | 264 | Y | 14.07 | 6218 | 40 | 980 | 1.91 | 37.0 | 0.73 | False |
| 12.00 | 264 | N | 15.39 | 6218 | 40 | 1281 | 2.28 | 48.8 | 0.56 | False |
| 12.00 | 350 | Y | 14.07 | 6505 | 40 | 935 | 1.66 | 37.0 | 0.67 | False |
| 12.00 | 350 | N | 15.39 | 6505 | 40 | 1222 | 1.98 | 48.8 | 0.51 | False |
| 14.00 | 100 | Y | 14.21 | 5936 | 40 | 1186 | 3.16 | 38.2 | 0.98 | False |
| 14.00 | 100 | N | 15.54 | 5936 | 40 | 1552 | 3.78 | 50.3 | 0.75 | False |
| 14.00 | 200 | Y | 14.21 | 6022 | 40 | 1057 | 2.24 | 38.2 | 0.78 | False |
| 14.00 | 200 | N | 15.54 | 6022 | 40 | 1383 | 2.68 | 50.3 | 0.59 | False |
| 14.00 | 264 | Y | 14.21 | 6218 | 40 | 1009 | 1.95 | 38.2 | 0.71 | False |
| 14.00 | 264 | N | 15.54 | 6218 | 40 | 1320 | 2.33 | 50.3 | 0.54 | False |
| 14.00 | 350 | Y | 14.21 | 6505 | 40 | 963 | 1.69 | 38.2 | 0.65 | False |
| 14.00 | 350 | N | 15.54 | 6505 | 40 | 1260 | 2.02 | 50.3 | 0.49 | False |

## Hypothesis grading

| Sub-claim | Central | Range | Computed | Held |
|---|---:|---|---:|:---:|
| H_afce_a | 15.4 | [14.5, 16.5] | 15.290 | True |
| H_afce_b | 330.0 | [200.0, 500.0] | 1316.079 | False |
| H_afce_c | 0.9 | [0.4, 2.5] | 2.588 | False |
| H_afce_d | 10.0 | [5.0, 18.0] | 47.868 | False |
| H_afce_e | 2.9 | [1.5, 6.0] | 0.622 | False |
| H_afce_f | 1.0 | [0.5, 4.0] | 2.588 | False |
| H_afce_g | 60.0 | [50.0, 75.0] | 40.000 | False |

**Aggregate: 1/6 sub-claims held. H-afce-agg held: False.**