### Peak delivered-water-per-launch-mass and optimum reactor power, by (specific power × chunk)

| Specific power (W/kg) | Chunk (t) | Peak reactor (kWe) | Peak ratio | Architecture | Delivered (t) | Launch mass (t) |
|---:|---:|---:|---:|---|---:|---:|
| 5 | 100 | 40 | 2.92 | all_electric | 60.0 | 21 |
| 5 | 200 | 100 | 3.47 | all_electric | 137.2 | 40 |
| 5 | 500 | 200 | 4.32 | all_electric | 307.3 | 71 |
| 10 | 100 | 40 | 4.32 | all_electric | 61.5 | 14 |
| 10 | 200 | 100 | 5.90 | all_electric | 140.0 | 24 |
| 10 | 500 | 200 | 8.94 | all_electric | 353.4 | 40 |
| 20 | 100 | 40 | 5.61 | all_electric | 62.2 | 11 |
| 20 | 200 | 100 | 8.94 | all_electric | 141.4 | 16 |
| 20 | 500 | 200 | 15.01 | all_electric | 356.2 | 24 |
| 40 | 100 | 40 | 7.42 | all_electric | 70.4 | 9 |
| 40 | 200 | 100 | 11.97 | all_electric | 142.1 | 12 |
| 40 | 500 | 200 | 22.60 | all_electric | 357.6 | 16 |

### Delivered/launch-mass ratio at 200 t chunk, sweep reactor power × specific power

| Reactor (kWe) | 5 W/kg | 10 W/kg | 20 W/kg | 40 W/kg |
|---:|---:|---:|---:|---:|
| 10 | - | - | - | - |
| 40 | 2.53 | 3.13 | 3.54 | 3.78 |
| 100 | 3.47 | 5.90 | 8.94 | 11.97 |
| 200 | 2.12 | 3.92 | 6.62 | 9.99 |
| 500 | 0.98 | 1.94 | 3.62 | 6.26 |
| 1000 | 0.46 | 0.98 | 1.94 | 3.62 |
| 2000 | 0.20 | 0.46 | 0.98 | 1.94 |

### Delivered/launch-mass ratio at 500 t chunk, sweep reactor power × specific power

| Reactor (kWe) | 5 W/kg | 10 W/kg | 20 W/kg | 40 W/kg |
|---:|---:|---:|---:|---:|
| 10 | - | - | - | - |
| 40 | - | - | - | - |
| 100 | 4.31 | 6.15 | 7.77 | 8.92 |
| 200 | 4.32 | 8.94 | 15.01 | 22.60 |
| 500 | 2.28 | 4.47 | 8.30 | 14.32 |
| 1000 | 1.27 | 2.56 | 4.96 | 9.16 |
| 2000 | 0.61 | 1.27 | 2.56 | 4.96 |

### Winning architecture at 200 t chunk, sweep reactor × specific power

Format: architecture · Δv_chem (km/s) · electric Isp (s)

| Reactor (kWe) | 5 W/kg | 10 W/kg | 20 W/kg | 40 W/kg |
|---:|---|---|---|---|
| 10 | - | - | - | - |
| 40 | variant_b dv_c2 Isp2000 | variant_b dv_c2 Isp2000 | variant_b dv_c2 Isp2000 | variant_b dv_c2 Isp2000 |
| 100 | all_electric dv_c0 Isp2000 | all_electric dv_c0 Isp2000 | all_electric dv_c0 Isp2000 | all_electric dv_c0 Isp2000 |
| 200 | all_electric dv_c0 Isp2934 | all_electric dv_c0 Isp2934 | all_electric dv_c0 Isp2934 | all_electric dv_c0 Isp2934 |
| 500 | all_electric dv_c0 Isp5000 | all_electric dv_c0 Isp5000 | all_electric dv_c0 Isp5000 | all_electric dv_c0 Isp5000 |
| 1000 | all_electric dv_c0 Isp5000 | all_electric dv_c0 Isp5000 | all_electric dv_c0 Isp5000 | all_electric dv_c0 Isp5000 |
| 2000 | all_electric dv_c0 Isp5000 | all_electric dv_c0 Isp5000 | all_electric dv_c0 Isp5000 | all_electric dv_c0 Isp5000 |