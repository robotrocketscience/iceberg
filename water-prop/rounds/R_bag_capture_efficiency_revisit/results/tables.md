# R-bag-capture-efficiency-revisit — tables

Hohmann cruise each way: **6.09 yr**.


## Composite η_c per era (extends bag-engineering doc §6)

| Era | η_bag | η_feed | η_pre | η_thr range | Composite η_c (lo / mid / hi) |
|---|---:|---:|---:|---|---|
| Kilopower MET (bag-eng doc baseline) | 0.97 | 0.95 | 0.921 | 0.75–0.92 | 0.691 / 0.769 / 0.848 |
| Kilopower Variant B inbound (RF ion) | 0.97 | 0.95 | 0.921 | 0.65–0.75 | 0.599 / 0.645 / 0.691 |
| Stretch / Sub-megawatt (RF ion) | 0.97 | 0.95 | 0.921 | 0.65–0.75 | 0.599 / 0.645 / 0.691 |
| Megawatt (dual-ion, RF ion + MET hybrid) | 0.97 | 0.95 | 0.921 | 0.65–0.75 | 0.599 / 0.645 / 0.691 |

## Per-cell η_c sweep (mid mode: η_pre = η_thr = √η_c)


### Kilopower Variant B (10 kWe, 100 t chunk, chemical kick + electric inbound)

Tug dry mass (decomposed-mid): **3.97 t**

Critical η_c floor (mid mode, delivered = 0): **0.55**

| η_c | Mode | η_pre | η_thr | Delivered (t) | Burn (yr) | Round-trip (yr) | Closes 15 yr? |
|---:|---|---:|---:|---:|---:|---:|:--:|
| 0.55 | mid | 0.742 | 0.742 | 59.6 | 7.51 | 20.68 | no |
| 0.55 | pure_pre | 0.550 | 1.000 | 46.6 | 7.84 | 21.01 | no |
| 0.55 | pure_thr | 1.000 | 0.550 | 74.8 | 7.16 | 20.33 | no |
| 0.60 | mid | 0.775 | 0.775 | 62.9 | 8.21 | 21.38 | no |
| 0.60 | pure_pre | 0.600 | 1.000 | 50.9 | 8.51 | 21.68 | no |
| 0.60 | pure_thr | 1.000 | 0.600 | 76.6 | 7.90 | 21.07 | no |
| 0.65 | mid | 0.806 | 0.806 | 66.0 | 8.91 | 22.08 | no |
| 0.65 | pure_pre | 0.650 | 1.000 | 55.2 | 9.17 | 22.34 | no |
| 0.65 | pure_thr | 1.000 | 0.650 | 78.2 | 8.64 | 21.81 | no |
| 0.70 | mid | 0.837 | 0.837 | 69.0 | 9.61 | 22.78 | no |
| 0.70 | pure_pre | 0.700 | 1.000 | 59.5 | 9.84 | 23.01 | no |
| 0.70 | pure_thr | 1.000 | 0.700 | 79.6 | 9.38 | 22.55 | no |
| 0.75 | mid | 0.866 | 0.866 | 71.9 | 10.31 | 23.48 | no |
| 0.75 | pure_pre | 0.750 | 1.000 | 63.8 | 10.50 | 23.67 | no |
| 0.75 | pure_thr | 1.000 | 0.750 | 80.8 | 10.12 | 23.29 | no |
| 0.80 | mid | 0.894 | 0.894 | 74.8 | 11.01 | 24.19 | no |
| 0.80 | pure_pre | 0.800 | 1.000 | 68.1 | 11.17 | 24.34 | no |
| 0.80 | pure_thr | 1.000 | 0.800 | 81.9 | 10.86 | 24.03 | no |
| 0.85 | mid | 0.922 | 0.922 | 77.5 | 11.72 | 24.89 | no |
| 0.85 | pure_pre | 0.850 | 1.000 | 72.4 | 11.83 | 25.00 | no |
| 0.85 | pure_thr | 1.000 | 0.850 | 82.9 | 11.60 | 24.77 | no |
| 0.90 | mid | 0.949 | 0.949 | 80.2 | 12.42 | 25.59 | no |
| 0.90 | pure_pre | 0.900 | 1.000 | 76.7 | 12.50 | 25.67 | no |
| 0.90 | pure_thr | 1.000 | 0.900 | 83.7 | 12.34 | 25.51 | no |
| 0.95 | mid | 0.975 | 0.975 | 82.7 | 13.12 | 26.30 | no |
| 0.95 | pure_pre | 0.950 | 1.000 | 81.0 | 13.16 | 26.33 | no |
| 0.95 | pure_thr | 1.000 | 0.950 | 84.5 | 13.08 | 26.26 | no |
| 1.00 | mid | 1.000 | 1.000 | 85.3 | 13.83 | 27.00 | no |
| 1.00 | pure_pre | 1.000 | 1.000 | 85.3 | 13.83 | 27.00 | no |
| 1.00 | pure_thr | 1.000 | 1.000 | 85.3 | 13.83 | 27.00 | no |

Divergence at η_c=0.65 (pure_pre vs pure_thr): pure_pre delivers **55.2 t**, pure_thr delivers **78.2 t**, relative diff **29.4%**.


### Stretch 100 kWe sweet spot (100 kWe, 200 t chunk, all-electric)

Tug dry mass (decomposed-mid): **8.41 t**

Critical η_c floor (mid mode, delivered = 0): **0.55**

| η_c | Mode | η_pre | η_thr | Delivered (t) | Burn (yr) | Round-trip (yr) | Closes 15 yr? |
|---:|---|---:|---:|---:|---:|---:|:--:|
| 0.55 | mid | 0.742 | 0.742 | 92.4 | 2.88 | 21.26 | no |
| 0.55 | pure_pre | 0.550 | 1.000 | 76.9 | 3.10 | 21.47 | no |
| 0.55 | pure_thr | 1.000 | 0.550 | 106.5 | 2.65 | 21.02 | no |
| 0.60 | mid | 0.775 | 0.775 | 98.6 | 3.17 | 21.54 | no |
| 0.60 | pure_pre | 0.600 | 1.000 | 84.2 | 3.36 | 21.73 | no |
| 0.60 | pure_thr | 1.000 | 0.600 | 112.4 | 2.96 | 21.33 | no |
| 0.65 | mid | 0.806 | 0.806 | 104.6 | 3.45 | 21.82 | no |
| 0.65 | pure_pre | 0.650 | 1.000 | 91.4 | 3.62 | 21.99 | no |
| 0.65 | pure_thr | 1.000 | 0.650 | 117.5 | 3.27 | 21.64 | no |
| 0.70 | mid | 0.837 | 0.837 | 110.4 | 3.73 | 22.11 | no |
| 0.70 | pure_pre | 0.700 | 1.000 | 98.6 | 3.88 | 22.26 | no |
| 0.70 | pure_thr | 1.000 | 0.700 | 122.2 | 3.58 | 21.95 | no |
| 0.75 | mid | 0.866 | 0.866 | 116.0 | 4.02 | 22.39 | no |
| 0.75 | pure_pre | 0.750 | 1.000 | 105.8 | 4.15 | 22.52 | no |
| 0.75 | pure_thr | 1.000 | 0.750 | 126.3 | 3.89 | 22.26 | no |
| 0.80 | mid | 0.894 | 0.894 | 121.5 | 4.31 | 22.68 | no |
| 0.80 | pure_pre | 0.800 | 1.000 | 113.0 | 4.41 | 22.78 | no |
| 0.80 | pure_thr | 1.000 | 0.800 | 130.0 | 4.20 | 22.57 | no |
| 0.85 | mid | 0.922 | 0.922 | 126.8 | 4.59 | 22.96 | no |
| 0.85 | pure_pre | 0.850 | 1.000 | 120.2 | 4.67 | 23.04 | no |
| 0.85 | pure_thr | 1.000 | 0.850 | 133.4 | 4.51 | 22.88 | no |
| 0.90 | mid | 0.949 | 0.949 | 131.9 | 4.88 | 23.25 | no |
| 0.90 | pure_pre | 0.900 | 1.000 | 127.4 | 4.93 | 23.30 | no |
| 0.90 | pure_thr | 1.000 | 0.900 | 136.5 | 4.83 | 23.20 | no |
| 0.95 | mid | 0.975 | 0.975 | 136.9 | 5.17 | 23.54 | no |
| 0.95 | pure_pre | 0.950 | 1.000 | 134.6 | 5.19 | 23.57 | no |
| 0.95 | pure_thr | 1.000 | 0.950 | 139.3 | 5.14 | 23.51 | no |
| 1.00 | mid | 1.000 | 1.000 | 141.8 | 5.46 | 23.83 | no |
| 1.00 | pure_pre | 1.000 | 1.000 | 141.8 | 5.46 | 23.83 | no |
| 1.00 | pure_thr | 1.000 | 1.000 | 141.8 | 5.46 | 23.83 | no |

Divergence at η_c=0.65 (pure_pre vs pure_thr): pure_pre delivers **91.4 t**, pure_thr delivers **117.5 t**, relative diff **22.3%**.


### Sub-megawatt (200 kWe, 500 t chunk, all-electric, Isp 2934)

Tug dry mass (decomposed-mid): **13.23 t**

Critical η_c floor (mid mode, delivered = 0): **0.55**

| η_c | Mode | η_pre | η_thr | Delivered (t) | Burn (yr) | Round-trip (yr) | Closes 15 yr? |
|---:|---|---:|---:|---:|---:|---:|:--:|
| 0.55 | mid | 0.742 | 0.742 | 271.0 | 5.54 | 21.31 | no |
| 0.55 | pure_pre | 0.550 | 1.000 | 217.4 | 5.82 | 21.59 | no |
| 0.55 | pure_thr | 1.000 | 0.550 | 328.8 | 5.22 | 21.00 | no |
| 0.60 | mid | 0.775 | 0.775 | 287.1 | 6.07 | 21.84 | no |
| 0.60 | pure_pre | 0.600 | 1.000 | 237.4 | 6.32 | 22.09 | no |
| 0.60 | pure_thr | 1.000 | 0.600 | 340.6 | 5.79 | 21.56 | no |
| 0.65 | mid | 0.806 | 0.806 | 302.5 | 6.60 | 22.37 | no |
| 0.65 | pure_pre | 0.650 | 1.000 | 257.4 | 6.83 | 22.60 | no |
| 0.65 | pure_thr | 1.000 | 0.650 | 350.9 | 6.36 | 22.13 | no |
| 0.70 | mid | 0.837 | 0.837 | 317.3 | 7.14 | 22.91 | no |
| 0.70 | pure_pre | 0.700 | 1.000 | 277.4 | 7.33 | 23.10 | no |
| 0.70 | pure_thr | 1.000 | 0.700 | 359.9 | 6.93 | 22.70 | no |
| 0.75 | mid | 0.866 | 0.866 | 331.7 | 7.67 | 23.44 | no |
| 0.75 | pure_pre | 0.750 | 1.000 | 297.4 | 7.83 | 23.61 | no |
| 0.75 | pure_thr | 1.000 | 0.750 | 367.9 | 7.50 | 23.27 | no |
| 0.80 | mid | 0.894 | 0.894 | 345.6 | 8.21 | 23.98 | no |
| 0.80 | pure_pre | 0.800 | 1.000 | 317.4 | 8.34 | 24.11 | no |
| 0.80 | pure_thr | 1.000 | 0.800 | 375.1 | 8.07 | 23.84 | no |
| 0.85 | mid | 0.922 | 0.922 | 359.0 | 8.74 | 24.51 | no |
| 0.85 | pure_pre | 0.850 | 1.000 | 337.4 | 8.84 | 24.61 | no |
| 0.85 | pure_thr | 1.000 | 0.850 | 381.5 | 8.64 | 24.41 | no |
| 0.90 | mid | 0.949 | 0.949 | 372.2 | 9.28 | 25.05 | no |
| 0.90 | pure_pre | 0.900 | 1.000 | 357.4 | 9.35 | 25.12 | no |
| 0.90 | pure_thr | 1.000 | 0.900 | 387.3 | 9.21 | 24.98 | no |
| 0.95 | mid | 0.975 | 0.975 | 384.9 | 9.82 | 25.59 | no |
| 0.95 | pure_pre | 0.950 | 1.000 | 377.4 | 9.85 | 25.62 | no |
| 0.95 | pure_thr | 1.000 | 0.950 | 392.6 | 9.78 | 25.55 | no |
| 1.00 | mid | 1.000 | 1.000 | 397.4 | 10.36 | 26.13 | no |
| 1.00 | pure_pre | 1.000 | 1.000 | 397.4 | 10.36 | 26.13 | no |
| 1.00 | pure_thr | 1.000 | 1.000 | 397.4 | 10.36 | 26.13 | no |

Divergence at η_c=0.65 (pure_pre vs pure_thr): pure_pre delivers **257.4 t**, pure_thr delivers **350.9 t**, relative diff **26.7%**.


### Megawatt all-electric (1000 kWe, 500 t chunk, Isp 5000)

Tug dry mass (decomposed-mid): **32.23 t**

Critical η_c floor (mid mode, delivered = 0): **0.55**

| η_c | Mode | η_pre | η_thr | Delivered (t) | Burn (yr) | Round-trip (yr) | Closes 15 yr? |
|---:|---|---:|---:|---:|---:|---:|:--:|
| 0.55 | mid | 0.742 | 0.742 | 305.6 | 2.10 | 15.79 | no |
| 0.55 | pure_pre | 0.550 | 1.000 | 237.3 | 2.21 | 15.90 | no |
| 0.55 | pure_thr | 1.000 | 0.550 | 387.3 | 2.00 | 15.69 | no |
| 0.60 | mid | 0.775 | 0.775 | 322.1 | 2.29 | 15.99 | no |
| 0.60 | pure_pre | 0.600 | 1.000 | 259.2 | 2.39 | 16.08 | no |
| 0.60 | pure_thr | 1.000 | 0.600 | 395.7 | 2.20 | 15.89 | no |
| 0.65 | mid | 0.806 | 0.806 | 337.9 | 2.49 | 16.18 | no |
| 0.65 | pure_pre | 0.650 | 1.000 | 281.2 | 2.57 | 16.26 | no |
| 0.65 | pure_thr | 1.000 | 0.650 | 402.9 | 2.40 | 16.10 | no |
| 0.70 | mid | 0.837 | 0.837 | 353.1 | 2.68 | 16.37 | no |
| 0.70 | pure_pre | 0.700 | 1.000 | 303.1 | 2.75 | 16.44 | no |
| 0.70 | pure_thr | 1.000 | 0.700 | 409.2 | 2.61 | 16.30 | no |
| 0.75 | mid | 0.866 | 0.866 | 367.7 | 2.87 | 16.56 | no |
| 0.75 | pure_pre | 0.750 | 1.000 | 325.0 | 2.93 | 16.62 | no |
| 0.75 | pure_thr | 1.000 | 0.750 | 414.7 | 2.81 | 16.50 | no |
| 0.80 | mid | 0.894 | 0.894 | 381.9 | 3.06 | 16.75 | no |
| 0.80 | pure_pre | 0.800 | 1.000 | 347.0 | 3.11 | 16.80 | no |
| 0.80 | pure_thr | 1.000 | 0.800 | 419.6 | 3.01 | 16.71 | no |
| 0.85 | mid | 0.922 | 0.922 | 395.7 | 3.25 | 16.94 | no |
| 0.85 | pure_pre | 0.850 | 1.000 | 368.9 | 3.29 | 16.98 | no |
| 0.85 | pure_thr | 1.000 | 0.850 | 424.0 | 3.22 | 16.91 | no |
| 0.90 | mid | 0.949 | 0.949 | 409.0 | 3.44 | 17.14 | no |
| 0.90 | pure_pre | 0.900 | 1.000 | 390.8 | 3.47 | 17.16 | no |
| 0.90 | pure_thr | 1.000 | 0.900 | 427.9 | 3.42 | 17.11 | no |
| 0.95 | mid | 0.975 | 0.975 | 422.0 | 3.64 | 17.33 | no |
| 0.95 | pure_pre | 0.950 | 1.000 | 412.8 | 3.65 | 17.34 | no |
| 0.95 | pure_thr | 1.000 | 0.950 | 431.5 | 3.62 | 17.32 | no |
| 1.00 | mid | 1.000 | 1.000 | 434.7 | 3.83 | 17.52 | no |
| 1.00 | pure_pre | 1.000 | 1.000 | 434.7 | 3.83 | 17.52 | no |
| 1.00 | pure_thr | 1.000 | 1.000 | 434.7 | 3.83 | 17.52 | no |

Divergence at η_c=0.65 (pure_pre vs pure_thr): pure_pre delivers **281.2 t**, pure_thr delivers **402.9 t**, relative diff **30.2%**.


## Depot-fill mission ramp (Stretch 100 kWe / 200 t sweet spot)

Target: 273 t at low Earth orbit (R-outbound-architecture chemical-kick re-fill).

| η_c (mid) | Delivered (t) | Missions to fill |
|---:|---:|---:|
| 0.55 | 92.4 | 3 |
| 0.60 | 98.6 | 3 |
| 0.65 | 104.6 | 3 |
| 0.70 | 110.4 | 3 |
| 0.75 | 116.0 | 3 |
| 0.80 | 121.5 | 3 |
| 0.85 | 126.8 | 3 |
| 0.90 | 131.9 | 3 |
| 0.95 | 136.9 | 2 |
| 1.00 | 141.8 | 2 |

## Hypothesis grading

| Sub-claim | Predicted | Actual | Held? |
|---|---|---|---|
| H-bcer-a — megawatt-era composite η_c mid | [0.6, 0.7] | 0.645 | yes |
| H-bcer-b — megawatt delivered reduction at composite η_c=0.65 | [35.0, 55.0]% | 22.3% | **no** |
| H-bcer-c — megawatt round-trip Δ at η_c=0.65 | [-1.0, 1.0] yr | -1.34 yr | **no** |
| H-bcer-d — Variant B critical floor | [0.2, 0.4] | 0.55 | **no** |
| H-bcer-e — Stretch depot ramp at η_c=0.80 | [2, 4] missions | 3 missions | yes |
| H-bcer-f — at least one matrix winner flips L0-05 | true (at least one cell flips) | flipped (stretch closes=False, megawatt closes=False) | yes |
| H-bcer-g — pure_pre vs pure_thr divergence > 5% (m_tug > 10% chunk) | divergence > 5% where m_tug > 10% of chunk | max relative divergence 30.2% | **no** |