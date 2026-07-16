### Winning architecture by (reactor power × chunk mass)

For each cell, the architecture (and Δv_chem) that maximizes delivered_water / launch_mass at any feasible electric specific impulse. "-" means no architecture closes the 7-year inbound burn time.

| Reactor (kWe) | 50 t | 100 t | 200 t | 500 t |
|---:|---:|---:|---:|---:|
| 10 | variant_b dv_c2 Isp2000 (0.77) | variant_b dv_c3 Isp1500 (1.29) | - | - |
| 40 | all_electric dv_c0 Isp2934 (2.68) | all_electric dv_c0 Isp1500 (4.32) | variant_b dv_c2 Isp2000 (3.13) | - |
| 100 | all_electric dv_c0 Isp5000 (1.77) | all_electric dv_c0 Isp2934 (3.24) | all_electric dv_c0 Isp2000 (5.90) | variant_b dv_c2 Isp2000 (6.15) |
| 200 | all_electric dv_c0 Isp5000 (1.03) | all_electric dv_c0 Isp5000 (2.14) | all_electric dv_c0 Isp2934 (3.92) | all_electric dv_c0 Isp2000 (8.94) |
| 500 | all_electric dv_c0 Isp5000 (0.43) | all_electric dv_c0 Isp5000 (0.93) | all_electric dv_c0 Isp5000 (1.94) | all_electric dv_c0 Isp2934 (4.47) |
| 1000 | all_electric dv_c0 Isp5000 (0.19) | all_electric dv_c0 Isp5000 (0.45) | all_electric dv_c0 Isp5000 (0.98) | all_electric dv_c0 Isp5000 (2.56) |

Format: `architecture` + `dv_chem (km/s)` + `electric Isp (s)` + `(delivered/LEO ratio)`. Higher delivered/LEO is better.


### Delivered water (t) by best architecture per cell

| Reactor (kWe) | 50 t | 100 t | 200 t | 500 t |
|---:|---:|---:|---:|---:|
| 10 | 19.5 | 32.7 | - | - |
| 40 | 38.2 | 61.5 | 94.1 | - |
| 100 | 42.0 | 77.0 | 140.0 | 243.4 |
| 200 | 40.8 | 84.7 | 155.0 | 353.4 |
| 500 | 37.1 | 81.0 | 168.7 | 389.0 |
| 1000 | 31.0 | 74.8 | 162.6 | 425.8 |

### Launch mass to low Earth orbit (t) by best architecture per cell

| Reactor (kWe) | 50 t | 100 t | 200 t | 500 t |
|---:|---:|---:|---:|---:|
| 10 | 25 | 25 | - | - |
| 40 | 14 | 14 | 30 | - |
| 100 | 24 | 24 | 24 | 40 |
| 200 | 40 | 40 | 40 | 40 |
| 500 | 87 | 87 | 87 | 87 |
| 1000 | 166 | 166 | 166 | 166 |

### Variant B vs all-electric vs carried-hypergolic at 100 t chunk, sweep reactor

All at electric specific impulse 2000 s (water radio-frequency ion class). Δv_chem = 1 km/s for two-stage variants.

| Reactor (kWe) | All-electric delivered (t) | Variant B delivered (t) | Carried-hyp delivered (t) | A/E LEO (t) | VB LEO (t) | CH LEO (t) | A/E ratio | VB ratio | CH ratio |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 10 | 70.4 (slow) | 56.6 (slow) | 74.4 (slow) | 9 | 25 | 94 | 7.42 | 2.23 | 0.79 |
| 40 | 69.6 (slow) | 55.4 | 73.7 | 14 | 30 | 101 | 4.89 | 1.84 | 0.73 |
| 100 | 67.9 | 53.0 | 72.2 | 24 | 40 | 114 | 2.86 | 1.34 | 0.63 |
| 200 | 65.1 | 49.1 | 69.8 | 40 | 55 | 136 | 1.65 | 0.89 | 0.52 |
| 500 | 56.7 | 37.2 | 62.6 | 87 | 103 | 201 | 0.65 | 0.36 | 0.31 |
| 1000 | 42.8 | 17.4 | 50.5 | 166 | 182 | 310 | 0.26 | 0.10 | 0.16 |