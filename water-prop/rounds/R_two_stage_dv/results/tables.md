### Required electric specific impulse (s) by (delivered fraction × chemical delta-v offload)

Total inbound delta-v = 6.42 km/s. Chemical specific impulse is irrelevant for this table (electric specific impulse only depends on delta-v_elec and η).

| η | Δv_chem = 0.0 km/s | Δv_chem = 1.0 km/s | Δv_chem = 2.0 km/s | Δv_chem = 3.0 km/s | Δv_chem = 4.0 km/s | Δv_chem = 5.0 km/s |
|---:|---:|---:|---:|---:|---:|---:|
| 0.5 | 944 | 797 | 650 | 503 | 356 | 209 |
| 0.6 | 1282 | 1082 | 882 | 683 | 483 | 283 |
| 0.7 | 1835 | 1550 | 1264 | 978 | 692 | 406 |
| 0.8 | 2934 | 2477 | 2020 | 1563 | 1106 | 649 |
| 0.9 | 6214 | 5246 | 4278 | 3310 | 2342 | 1374 |

### Required thruster class by (delivered fraction × chemical delta-v offload)

| η | Δv_chem = 0.0 km/s | Δv_chem = 1.0 km/s | Δv_chem = 2.0 km/s | Δv_chem = 3.0 km/s | Δv_chem = 4.0 km/s | Δv_chem = 5.0 km/s |
|---:|---:|---:|---:|---:|---:|---:|
| 0.5 | MET_class | MET_class | MET_class | MET_class | MET_class | MET_class |
| 0.6 | Hall_class | Hall_class | MET_class | MET_class | MET_class | MET_class |
| 0.7 | RF_ion_class | Hall_class | Hall_class | MET_class | MET_class | MET_class |
| 0.8 | RF_ion_class | RF_ion_class | RF_ion_class | Hall_class | Hall_class | MET_class |
| 0.9 | dual_ion_class | dual_ion_class | dual_ion_class | dual_ion_class | RF_ion_class | Hall_class |

### Hypergolic chemical-propellant mass (tonnes) by (chunk × chemical delta-v offload), Isp_chem = 320 s

|  chunk | Δv_chem = 0.0 km/s | Δv_chem = 1.0 km/s | Δv_chem = 2.0 km/s | Δv_chem = 3.0 km/s | Δv_chem = 4.0 km/s | Δv_chem = 5.0 km/s |
|---:|---:|---:|---:|---:|---:|---:|
| 50 t | 0 (0.00×) | 19 (0.38×) | 45 (0.89×) | 80 (1.60×) | 129 (2.58×) | 196 (3.92×) |
| 100 t | 0 (0.00×) | 38 (0.38×) | 89 (0.89×) | 160 (1.60×) | 258 (2.58×) | 392 (3.92×) |
| 200 t | 0 (0.00×) | 75 (0.38×) | 178 (0.89×) | 320 (1.60×) | 515 (2.58×) | 784 (3.92×) |
| 350 t | 0 (0.00×) | 131 (0.38×) | 312 (0.89×) | 560 (1.60×) | 902 (2.58×) | 1372 (3.92×) |
| 500 t | 0 (0.00×) | 188 (0.38×) | 446 (0.89×) | 801 (1.60×) | 1289 (2.58×) | 1960 (3.92×) |

Ratio in parentheses is chemical-propellant-mass / chunk-mass. Ratio > 1 means more chemical propellant than chunk.


### Optimum chemical delta-v offload per delivered-fraction target, subject to chem-propellant ≤ chunk-mass constraint

Chunk = 100 t reference. The constraint chem_to_chunk_ratio ≤ 1 limits how much chemical offload is realistic from a launch-mass standpoint.

| η | chemistry | optimum Δv_chem (km/s) | required electric Isp (s) | thruster class | chem-to-chunk ratio | electric power (kWe) |
|---:|---|---:|---:|---|---:|---:|
| 0.5 | hypergolic_MMH_NTO | 2.0 | 650 | MET_class | 0.89 | 21 |
| 0.5 | cryogenic_methalox | 2.0 | 650 | MET_class | 0.76 | 21 |
| 0.5 | cryogenic_hydrolox | 3.0 | 503 | MET_class | 0.97 | 13 |
| 0.6 | hypergolic_MMH_NTO | 2.0 | 882 | MET_class | 0.89 | 32 |
| 0.6 | cryogenic_methalox | 2.0 | 882 | MET_class | 0.76 | 32 |
| 0.6 | cryogenic_hydrolox | 3.0 | 683 | MET_class | 0.97 | 19 |
| 0.7 | hypergolic_MMH_NTO | 2.0 | 1264 | Hall_class | 0.89 | 27 |
| 0.7 | cryogenic_methalox | 2.0 | 1264 | Hall_class | 0.76 | 27 |
| 0.7 | cryogenic_hydrolox | 3.0 | 978 | MET_class | 0.97 | 29 |
| 0.8 | hypergolic_MMH_NTO | 2.0 | 2020 | RF_ion_class | 0.89 | 38 |
| 0.8 | cryogenic_methalox | 2.0 | 2020 | RF_ion_class | 0.76 | 38 |
| 0.8 | cryogenic_hydrolox | 3.0 | 1563 | Hall_class | 0.97 | 27 |
| 0.9 | hypergolic_MMH_NTO | 2.0 | 4278 | dual_ion_class | 0.89 | 101 |
| 0.9 | cryogenic_methalox | 2.0 | 4278 | dual_ion_class | 0.76 | 101 |
| 0.9 | cryogenic_hydrolox | 3.0 | 3310 | dual_ion_class | 0.97 | 61 |