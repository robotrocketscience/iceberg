# R-chunk-as-heat-shield-revisit — results tables

## Cross-check against hyperion R-aerocapture-fast-cruise-envelope

- Hyperion's Round-F STRICT no-LGA: 15.29 km/s entry, envelope FAILS.
- Phoebe's recompute (chunk=200 t, v_inf=10.55, tug=63.8 t): 15.29 km/s entry (ratio 1.000)
- STRICT pass: False; SACRIFICIAL_BAG pass: False
Cross-check inside 5% of hyperion's anchor.

## Sweep at Variant B tug mass (30 t) — 8 chunk × 5 v_inf = 40 cells

| chunk (t) | v_inf (km/s) | v_entry (km/s) | β (kg/m²) | periapsis (km) | q_peak (W/cm²) | ablation (%) | peak g | margin × | bag therm | chunk therm | chunk struct | capture | STRICT | SACR-BAG |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 25 | 3.0 | 11.47 | 5022 | 40 | 786.02 | 4.12 | 17.9 | 3.32 | N | Y | Y | N | N | N |
| 25 | 5.0 | 12.15 | 5022 | 40 | 933.66 | 4.62 | 22.4 | 2.66 | N | Y | Y | N | N | N |
| 25 | 7.0 | 13.10 | 5022 | 40 | 1170.42 | 5.37 | 29.2 | 2.04 | N | N | Y | N | N | N |
| 25 | 9.0 | 14.27 | 5022 | 40 | 1512.66 | 6.38 | 38.7 | 1.54 | N | N | Y | N | N | N |
| 25 | 11.0 | 15.61 | 5022 | 40 | 1979.69 | 7.63 | 50.9 | 1.17 | N | N | Y | N | N | N |
| 50 | 3.0 | 11.47 | 4602 | 40 | 700.27 | 2.91 | 17.9 | 2.64 | N | Y | Y | N | N | N |
| 50 | 5.0 | 12.15 | 4602 | 40 | 831.79 | 3.27 | 22.4 | 2.11 | N | Y | Y | N | N | N |
| 50 | 7.0 | 13.10 | 4602 | 40 | 1042.73 | 3.80 | 29.2 | 1.62 | N | Y | Y | N | N | N |
| 50 | 9.0 | 14.27 | 4602 | 40 | 1347.62 | 4.51 | 38.7 | 1.22 | N | Y | Y | N | N | N |
| 50 | 11.0 | 15.61 | 4602 | 40 | 1763.70 | 5.39 | 50.9 | 0.93 | N | N | N | N | N | N |
| 75 | 3.0 | 11.47 | 4609 | 40 | 654.51 | 2.38 | 17.9 | 2.30 | N | Y | Y | N | N | N |
| 75 | 5.0 | 12.15 | 4609 | 40 | 777.44 | 2.67 | 22.4 | 1.85 | N | Y | Y | N | N | N |
| 75 | 7.0 | 13.10 | 4609 | 40 | 974.59 | 3.10 | 29.2 | 1.41 | N | Y | Y | N | N | N |
| 75 | 9.0 | 14.27 | 4609 | 40 | 1259.56 | 3.68 | 38.7 | 1.07 | N | Y | Y | N | N | N |
| 75 | 11.0 | 15.61 | 4609 | 40 | 1648.45 | 4.40 | 50.9 | 0.81 | N | Y | N | N | N | N |
| 100 | 3.0 | 11.47 | 4711 | 40 | 623.87 | 2.06 | 17.9 | 2.09 | N | Y | Y | N | N | N |
| 100 | 5.0 | 12.15 | 4711 | 40 | 741.04 | 2.31 | 22.4 | 1.68 | N | Y | Y | N | N | N |
| 100 | 7.0 | 13.10 | 4711 | 40 | 928.96 | 2.69 | 29.2 | 1.28 | N | Y | Y | N | N | N |
| 100 | 9.0 | 14.27 | 4711 | 40 | 1200.60 | 3.19 | 38.7 | 0.97 | N | Y | N | N | N | N |
| 100 | 11.0 | 15.61 | 4711 | 40 | 1571.28 | 3.81 | 50.9 | 0.74 | N | Y | N | N | N | N |
| 150 | 3.0 | 11.47 | 4978 | 40 | 583.10 | 1.68 | 17.9 | 1.83 | N | Y | Y | N | N | N |
| 150 | 5.0 | 12.15 | 4978 | 40 | 692.62 | 1.89 | 22.4 | 1.47 | N | Y | Y | N | N | N |
| 150 | 7.0 | 13.10 | 4978 | 40 | 868.26 | 2.19 | 29.2 | 1.12 | N | Y | Y | N | N | N |
| 150 | 9.0 | 14.27 | 4978 | 40 | 1122.14 | 2.60 | 38.7 | 0.85 | N | Y | N | N | N | N |
| 150 | 11.0 | 15.61 | 4978 | 40 | 1468.60 | 3.11 | 50.9 | 0.64 | N | Y | N | N | N | N |
| 200 | 3.0 | 11.47 | 5250 | 40 | 555.80 | 1.46 | 17.9 | 1.66 | N | Y | Y | N | N | N |
| 200 | 5.0 | 12.15 | 5250 | 40 | 660.20 | 1.63 | 22.4 | 1.33 | N | Y | Y | N | N | N |
| 200 | 7.0 | 13.10 | 5250 | 40 | 827.61 | 1.90 | 29.2 | 1.02 | N | Y | Y | N | N | N |
| 200 | 9.0 | 14.27 | 5250 | 40 | 1069.61 | 2.25 | 38.7 | 0.77 | N | Y | N | N | N | N |
| 200 | 11.0 | 15.61 | 5250 | 40 | 1399.85 | 2.70 | 50.9 | 0.59 | N | Y | N | N | N | N |
| 300 | 3.0 | 11.47 | 5749 | 40 | 519.48 | 1.19 | 17.9 | 1.45 | N | Y | Y | N | N | N |
| 300 | 5.0 | 12.15 | 5749 | 40 | 617.06 | 1.33 | 22.4 | 1.16 | N | Y | Y | N | N | N |
| 300 | 7.0 | 13.10 | 5749 | 40 | 773.53 | 1.55 | 29.2 | 0.89 | N | Y | N | N | N | N |
| 300 | 9.0 | 14.27 | 5749 | 40 | 999.72 | 1.84 | 38.7 | 0.67 | N | Y | N | N | N | N |
| 300 | 11.0 | 15.61 | 5749 | 40 | 1308.38 | 2.20 | 50.9 | 0.51 | N | Y | N | N | N | N |
| 500 | 3.0 | 11.47 | 6568 | 40 | 477.09 | 0.92 | 17.9 | 1.22 | N | Y | Y | N | N | N |
| 500 | 5.0 | 12.15 | 6568 | 40 | 566.70 | 1.03 | 22.4 | 0.98 | N | Y | N | N | N | N |
| 500 | 7.0 | 13.10 | 6568 | 40 | 710.40 | 1.20 | 29.2 | 0.75 | N | Y | N | N | N | N |
| 500 | 9.0 | 14.27 | 6568 | 40 | 918.13 | 1.43 | 38.7 | 0.57 | N | Y | N | N | N | N |
| 500 | 11.0 | 15.61 | 6568 | 40 | 1201.60 | 1.71 | 50.9 | 0.43 | N | Y | N | N | N | N |

## Sensitivity at Variant C tug mass (63.8 t) — chunk = 200 t only

| chunk (t) | v_inf (km/s) | v_entry (km/s) | β (kg/m²) | periapsis (km) | q_peak (W/cm²) | ablation (%) | peak g | margin × | STRICT | SACR-BAG |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|:---:|
| 200 | 3.0 | 11.47 | 6022 | 40 | 555.80 | 1.46 | 17.9 | 1.66 | N | N |
| 200 | 5.0 | 12.15 | 6022 | 40 | 660.20 | 1.63 | 22.4 | 1.33 | N | N |
| 200 | 7.0 | 13.10 | 6022 | 40 | 827.61 | 1.90 | 29.2 | 1.02 | N | N |
| 200 | 9.0 | 14.27 | 6022 | 40 | 1069.61 | 2.25 | 38.7 | 0.77 | N | N |
| 200 | 11.0 | 15.61 | 6022 | 40 | 1399.85 | 2.70 | 50.9 | 0.59 | N | N |

## Architectural intersection cells

| Intersection | chunk (t) | v_inf (km/s) | tug (t) | v_entry (km/s) | periapsis (km) | q_peak (W/cm²) | ablation (%) | peak g | margin × | STRICT | SACR-BAG |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|:---:|
| Variant_C_RoundF_no_LGA | 200 | 10.55 | 63.8 | 15.29 | 40 | 1317.09 | 2.59 | 47.9 | 0.62 | N | N |
| Variant_C_RoundF_with_LGA | 200 | 8.55 | 63.8 | 13.99 | 40 | 1007.98 | 2.17 | 36.3 | 0.82 | N | N |
| Variant_B_chunk200_low_vinf | 200 | 5.00 | 30.0 | 12.15 | 40 | 660.20 | 1.63 | 22.4 | 1.33 | N | N |
| Variant_B_chunk200_mid_vinf | 200 | 7.00 | 30.0 | 13.10 | 40 | 827.61 | 1.90 | 29.2 | 1.02 | N | N |
| Variant_B_chunk200_no_LGA | 200 | 8.55 | 30.0 | 13.99 | 40 | 1007.98 | 2.17 | 36.3 | 0.82 | N | N |
| RCAHS_original_anchor | 100 | 1.50 | 30.0 | 11.17 | 40 | 576.48 | 1.95 | 16.1 | 2.33 | N | N |

## Closing-region summary

- STRICT (bag-retained) closing cells of 40: **0**
- SACRIFICIAL_BAG closing cells of 40: **0**

## Hypothesis grading

| Sub-claim | Central | Predicted range | Computed | Held |
|---|---|---|---|:---:|
| H_csa_a | empty | [0, 2] | n/a | True |
| H_csa_b_chunk | 100.0 | [75.0, 150.0] | n/a | False |
| H_csa_b_vinf | 6.0 | [5.0, 8.0] | n/a | False |
| H_csa_c | no intersection | False | n/a | True |
| H_csa_d | no intersection at chunk=200 | False | n/a | True |
| H_csa_e | small-chunk closing region exists OR is empty (qualitative) |  | n/a | n/a |
| H_csa_f | not gradable (antecedent false: no architecturally-relevant closing region) |  | n/a | not gradable |

**Aggregate H-csa-agg: HELD** (3 of 5 gradable sub-claims held)

H-csa-agg held iff: STRICT region empty (H-csa-a) AND no Variant C intersection (H-csa-c) AND no Variant B intersection (H-csa-d). H-csa-b sub-claims are about the BOUNDS of the SACRIFICIAL region and are diagnostic; the aggregate verdict turns on whether any architecturally-relevant intersection exists.