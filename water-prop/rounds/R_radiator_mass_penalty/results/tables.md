### Dry-mass decomposition by reactor class and mass model (no chunk, no tank)

Tug dry mass in tonnes. Bundled = matrix's current 10 W/kg formula. Decomposed splits m_fixed / m_reactor / m_PC / m_radiator and sums.

| Reactor (kWe) | Bundled 10 W/kg (t) | Decomposed mid (t) | Decomposed conservative (t) | Decomposed stretch (t) |
|---:|---:|---:|---:|---:|
| 10 | 6.0 | 3.3 | 3.5 | 3.2 |
| 40 | 9.0 | 4.0 | 4.9 | 3.7 |
| 100 | 15.0 | 5.6 | 7.6 | 4.8 |
| 200 | 25.0 | 8.2 | 12.3 | 6.6 |
| 500 | 55.0 | 16.1 | 26.2 | 11.9 |
| 1000 | 105.0 | 29.2 | 49.3 | 20.9 |
| 2000 | 205.0 | 55.3 | 95.7 | 38.8 |

### Decomposed-mid breakdown by component at each reactor class

| Reactor (kWe) | m_fixed (t) | m_reactor (t) | m_PC (t) | m_radiator (t) | Total tug dry (t) |
|---:|---:|---:|---:|---:|---:|
| 10 | 3.0 | 0.2 | 0.1 | 0.01 | 3.3 |
| 40 | 3.0 | 0.8 | 0.2 | 0.05 | 4.0 |
| 100 | 3.0 | 2.0 | 0.5 | 0.12 | 5.6 |
| 200 | 3.0 | 4.0 | 1.0 | 0.23 | 8.2 |
| 500 | 3.0 | 10.0 | 2.5 | 0.58 | 16.1 |
| 1000 | 3.0 | 20.0 | 5.0 | 1.17 | 29.2 |
| 2000 | 3.0 | 40.0 | 10.0 | 2.33 | 55.3 |

### Delivered mass and launch mass at 500 t chunk, all mass models, 2000 s electric Isp

Launch mass under chemical-kick outbound (matrix's headline outbound architecture).

| Reactor (kWe) | Model | M_v (t) | Delivered (t) | M_LEO chemkick (t) | Delivered/M_LEO | Burn time (yr) |
|---:|---|---:|---:|---:|---:|---:|
| 10 | bundled_10_W_per_kg | 13.2 | 356.7 | 143.7 | 2.482 | 134.32 |
| 10 | decomposed_mid | 10.4 | 357.5 | 113.4 | 3.153 | 133.60 |
| 10 | decomposed_conservative | 10.6 | 357.5 | 115.6 | 3.092 | 133.65 |
| 10 | decomposed_stretch | 10.3 | 357.5 | 112.5 | 3.179 | 133.57 |
| 40 | bundled_10_W_per_kg | 16.2 | 355.9 | 176.9 | 2.012 | 33.78 |
| 40 | decomposed_mid | 11.2 | 357.3 | 122.1 | 2.927 | 33.45 |
| 40 | decomposed_conservative | 12.0 | 357.1 | 131.0 | 2.726 | 33.50 |
| 40 | decomposed_stretch | 10.8 | 357.4 | 118.4 | 3.018 | 33.43 |
| 100 | bundled_10_W_per_kg | 22.3 | 354.2 | 243.4 | 1.455 | 13.67 |
| 100 | decomposed_mid | 12.8 | 356.9 | 139.5 | 2.559 | 13.42 |
| 100 | decomposed_conservative | 14.8 | 356.3 | 161.8 | 2.202 | 13.48 |
| 100 | decomposed_stretch | 11.9 | 357.1 | 130.3 | 2.741 | 13.40 |
| 200 | bundled_10_W_per_kg | 32.4 | 351.4 | 354.1 | 0.992 | 6.97 |
| 200 | decomposed_mid | 15.4 | 356.1 | 168.4 | 2.114 | 6.75 |
| 200 | decomposed_conservative | 19.5 | 355.0 | 213.1 | 1.666 | 6.80 |
| 200 | decomposed_stretch | 13.7 | 356.6 | 150.1 | 2.376 | 6.72 |
| 500 | bundled_10_W_per_kg | 62.9 | 342.9 | 686.3 | 0.500 | 2.95 |
| 500 | decomposed_mid | 23.4 | 353.9 | 255.4 | 1.386 | 2.74 |
| 500 | decomposed_conservative | 33.6 | 351.0 | 367.0 | 0.957 | 2.79 |
| 500 | decomposed_stretch | 19.2 | 355.1 | 209.4 | 1.695 | 2.72 |
| 1000 | bundled_10_W_per_kg | 113.6 | 328.7 | 1239.9 | 0.265 | 1.61 |
| 1000 | decomposed_mid | 36.7 | 350.2 | 400.2 | 0.875 | 1.40 |
| 1000 | decomposed_conservative | 57.1 | 344.5 | 623.5 | 0.552 | 1.46 |
| 1000 | decomposed_stretch | 28.2 | 352.5 | 308.4 | 1.143 | 1.38 |
| 2000 | bundled_10_W_per_kg | 215.0 | 300.4 | 2347.1 | 0.128 | 0.94 |
| 2000 | decomposed_mid | 63.2 | 342.8 | 689.9 | 0.497 | 0.74 |
| 2000 | decomposed_conservative | 104.1 | 331.4 | 1136.5 | 0.292 | 0.79 |
| 2000 | decomposed_stretch | 46.4 | 347.5 | 506.3 | 0.686 | 0.72 |

### Pairwise degradation: decomposed-mid vs bundled-10-W/kg

Percentage drop in delivered-per-launch-mass when the radiator is explicitly counted.

| Reactor (kWe) | 100 t chunk | 200 t chunk | 500 t chunk |
|---:|---:|---:|---:|
| 10 | -60.6% | -46.0% | -27.0% |
| 40 | -94.9% | -74.2% | -45.5% |
| 100 | -143.0% | -115.6% | -75.8% |
| 200 | -194.3% | -160.9% | -113.1% |
| 500 | -286.0% | -232.6% | -177.4% |
| 1000 | -426.2% | -301.0% | -230.0% |
| 2000 | -1392.9% | -435.0% | -288.2% |

### Optimum reactor power under each mass model — 7-year burn-cap-constrained

Optimum = peak delivered-per-launch-mass at chemical-kick outbound, 2000 s electric Isp, subject to inbound burn time ≤ 7 yr.

| Mass model | 100 t chunk | 200 t chunk | 500 t chunk |
|---|---:|---:|---:|
| bundled_10_W_per_kg | 100 kWe @ 0.372 | 100 kWe @ 0.706 | 200 kWe @ 0.992 |
| decomposed_mid | 40 kWe @ 1.171 | 100 kWe @ 1.523 | 200 kWe @ 2.114 |
| decomposed_conservative | 40 kWe @ 1.016 | 100 kWe @ 1.223 | 200 kWe @ 1.666 |
| decomposed_stretch | 40 kWe @ 1.248 | 100 kWe @ 1.692 | 200 kWe @ 2.376 |

### Optimum reactor power — burn-time-unconstrained (rocket-equation-only view)

Same metric, no burn-cap. Low reactor power always wins on raw ratio because smaller vehicle → smaller mass ratio penalty; this is why the matrix uses burn-time-constrained optima.

| Mass model | 100 t chunk | 200 t chunk | 500 t chunk |
|---|---:|---:|---:|
| bundled_10_W_per_kg | 10 kWe @ 0.855 | 10 kWe @ 1.455 | 10 kWe @ 2.482 |
| decomposed_mid | 10 kWe @ 1.372 | 10 kWe @ 2.125 | 10 kWe @ 3.153 |
| decomposed_conservative | 10 kWe @ 1.314 | 10 kWe @ 2.056 | 10 kWe @ 3.092 |
| decomposed_stretch | 10 kWe @ 1.398 | 10 kWe @ 2.155 | 10 kWe @ 3.179 |

### Hypothesis grading

| Sub-claim | Predicted | Actual | Held? |
|---|---|---|---|
| H-rmp-a — 1 MWe tug dry mass (decomposed-mid, no tank) | 50–120 t | 29.2 t | **no** |
| H-rmp-b — Megawatt cell delivered-ratio degradation (500 t chunk, decomposed-mid vs bundled) | 15–40% | -230.0% | **no** |
| H-rmp-c — Optimum reactor power (500 t chunk, 7-yr cap) | shift from 1000 kWe → 200–500 kWe | bundled 200.0 kWe → decomposed-mid 200.0 kWe | (read below) |
| H-rmp-d — Kilopower (10 kWe, 100 t chunk) within ±5% | within 5% | -60.6% | **no** |