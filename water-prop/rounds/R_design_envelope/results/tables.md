### Required Isp (s) by (delivered fraction × inbound Δv)

Rocket equation Isp = -Δv / (g₀ · ln η). Chunk-mass independent.

| η delivered | Δv = 4.47 km/s | Δv = 6.42 km/s | Δv = 8.87 km/s |
|---:|---:|---:|---:|
| 0.5 | 658 | 944 | 1305 |
| 0.6 | 892 | 1282 | 1771 |
| 0.7 | 1278 | 1835 | 2536 |
| 0.8 | 2043 | 2934 | 4053 |
| 0.9 | 4326 | 6214 | 8585 |

### Required thrust (N) by (delivered fraction × chunk), at Δv = 6.42 km/s, τ_burn = 5 yr

| η | 10 t | 25 t | 50 t | 100 t | 200 t | 350 t | 500 t |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.5 | 0.29 | 0.73 | 1.47 | 2.93 | 5.87 | 10.27 | 14.67 |
| 0.6 | 0.32 | 0.80 | 1.59 | 3.19 | 6.37 | 11.15 | 15.93 |
| 0.7 | 0.34 | 0.86 | 1.71 | 3.42 | 6.84 | 11.98 | 17.11 |
| 0.8 | 0.36 | 0.91 | 1.82 | 3.65 | 7.29 | 12.76 | 18.23 |
| 0.9 | 0.39 | 0.97 | 1.93 | 3.86 | 7.72 | 13.52 | 19.31 |

### Required electrical power (kWe) by (delivered fraction × chunk), thruster class auto-chosen by required Isp band, η_thr per class, Δv = 6.42 km/s, τ_burn = 5 yr

| η | 10 t | 25 t | 50 t | 100 t | 200 t | 350 t | 500 t |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.5 | 5 | 11 | 23 | 45 | 91 | 159 | 227 |
| 0.6 | 4 | 9 | 18 | 36 | 73 | 127 | 182 |
| 0.7 | 5 | 12 | 24 | 47 | 95 | 166 | 237 |
| 0.8 | 8 | 20 | 40 | 81 | 161 | 282 | 404 |
| 0.9 | 21 | 53 | 107 | 214 | 428 | 749 | 1070 |

### Known thruster maximum delivered fraction at each Δv

Maximum η achievable for that thruster's Isp (so any column showing η ≥ target means the thruster reaches it).

| Thruster | Isp (s) | η_max at Δv 4.47 | η_max at Δv 6.42 | η_max at Δv 8.87 |
|---|---:|---:|---:|---:|
| water_MET | 700 | 0.521 | 0.392 | 0.275 |
| water_Hall | 1500 | 0.738 | 0.646 | 0.547 |
| water_RF_ion | 2000 | 0.796 | 0.721 | 0.636 |
| water_dual_ion | 5000 | 0.913 | 0.877 | 0.835 |
| H2_NTP_solid_core | 900 | 0.603 | 0.483 | 0.366 |

### Coverage: which (Isp band, power band) cell each (η, chunk) lands in (Δv = 6.42 km/s, τ_burn = 5 yr)

- **Hall class, 50-200 kWe** → 3 cell(s): (0.6, 200t), (0.6, 350t), (0.6, 500t)
- **Hall class, <=50 kWe** → 4 cell(s): (0.6, 10t), (0.6, 25t), (0.6, 50t), (0.6, 100t)
- **MET class, 200-500 kWe** → 1 cell(s): (0.5, 500t)
- **MET class, 50-200 kWe** → 2 cell(s): (0.5, 200t), (0.5, 350t)
- **MET class, <=50 kWe** → 4 cell(s): (0.5, 10t), (0.5, 25t), (0.5, 50t), (0.5, 100t)
- **RF_ion class, 200-500 kWe** → 3 cell(s): (0.7, 500t), (0.8, 350t), (0.8, 500t)
- **RF_ion class, 50-200 kWe** → 4 cell(s): (0.7, 200t), (0.7, 350t), (0.8, 100t), (0.8, 200t)
- **RF_ion class, <=50 kWe** → 7 cell(s): (0.7, 10t), (0.7, 25t), (0.7, 50t), (0.7, 100t), (0.8, 10t), (0.8, 25t), (0.8, 50t)
- **dual_ion class, 200-500 kWe** → 2 cell(s): (0.9, 100t), (0.9, 200t)
- **dual_ion class, 50-200 kWe** → 2 cell(s): (0.9, 25t), (0.9, 50t)
- **dual_ion class, 500 kWe - 2 MWe** → 2 cell(s): (0.9, 350t), (0.9, 500t)
- **dual_ion class, <=50 kWe** → 1 cell(s): (0.9, 10t)