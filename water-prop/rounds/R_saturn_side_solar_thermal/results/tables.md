# R-saturn-side-solar-thermal — results

Saturn solar flux: 14.83 W/m² (at 9.58 AU)

Fission benchmarks (kg per kW-useful): {'FSP_stretch_10W_per_kg': 100.0, 'FSP_phase1_contracted_5W_per_kg': 200.0, 'KRUSTY_demonstrated_2p4W_per_kg': 416.0}

Falsification rule: hypothesis upheld if conservative scenario (stirling, areal=1.0 kg/m², duty=1.5) yields kg/kW < 200. Falsified if conservative > 400. Middle band = same risk-class as FSP stretch.

| target_kW | areal_kg/m² | path | duty | A_mirror_m² | m_mirror_t | m_radiator_t | m_total_t | kg/kW_useful | vs_fission |
|---|---|---|---|---|---|---|---|---|---|
| 150 | 0.1 | stirling | 1.0 | 64509 | 6.45 | 27.55 | 44.31 | 295 | beats_KRUSTY_demonstrated |
| 150 | 0.1 | stirling | 1.5 | 96763 | 9.68 | 27.55 | 51.09 | 341 | beats_KRUSTY_demonstrated |
| 150 | 0.1 | soec | 1.0 | 25287 | 2.53 | 7.50 | 15.21 | 101 | beats_FSP_phase1_baseline |
| 150 | 0.1 | soec | 1.5 | 37931 | 3.79 | 7.50 | 17.87 | 119 | beats_FSP_phase1_baseline |
| 150 | 0.3 | stirling | 1.0 | 64509 | 19.35 | 27.55 | 71.41 | 476 | worse_than_KRUSTY |
| 150 | 0.3 | stirling | 1.5 | 96763 | 29.03 | 27.55 | 91.73 | 612 | worse_than_KRUSTY |
| 150 | 0.3 | soec | 1.0 | 25287 | 7.59 | 7.50 | 25.83 | 172 | beats_FSP_phase1_baseline |
| 150 | 0.3 | soec | 1.5 | 37931 | 11.38 | 7.50 | 33.80 | 225 | beats_KRUSTY_demonstrated |
| 150 | 0.5 | stirling | 1.0 | 64509 | 32.25 | 27.55 | 98.50 | 657 | worse_than_KRUSTY |
| 150 | 0.5 | stirling | 1.5 | 96763 | 48.38 | 27.55 | 132.37 | 882 | worse_than_KRUSTY |
| 150 | 0.5 | soec | 1.0 | 25287 | 12.64 | 7.50 | 36.45 | 243 | beats_KRUSTY_demonstrated |
| 150 | 0.5 | soec | 1.5 | 37931 | 18.97 | 7.50 | 49.73 | 332 | beats_KRUSTY_demonstrated |
| 150 | 1.0 | stirling | 1.0 | 64509 | 64.51 | 27.55 | 166.23 | 1108 | worse_than_KRUSTY |
| 150 | 1.0 | stirling | 1.5 | 96763 | 96.76 | 27.55 | 233.97 | 1560 | worse_than_KRUSTY |
| 150 | 1.0 | soec | 1.0 | 25287 | 25.29 | 7.50 | 63.00 | 420 | worse_than_KRUSTY |
| 150 | 1.0 | soec | 1.5 | 37931 | 37.93 | 7.50 | 89.56 | 597 | worse_than_KRUSTY |
| 200 | 0.1 | stirling | 1.0 | 86012 | 8.60 | 36.73 | 59.08 | 295 | beats_KRUSTY_demonstrated |
| 200 | 0.1 | stirling | 1.5 | 129017 | 12.90 | 36.73 | 68.11 | 341 | beats_KRUSTY_demonstrated |
| 200 | 0.1 | soec | 1.0 | 33717 | 3.37 | 10.00 | 20.28 | 101 | beats_FSP_phase1_baseline |
| 200 | 0.1 | soec | 1.5 | 50575 | 5.06 | 10.00 | 23.82 | 119 | beats_FSP_phase1_baseline |
| 200 | 0.3 | stirling | 1.0 | 86012 | 25.80 | 36.73 | 95.21 | 476 | worse_than_KRUSTY |
| 200 | 0.3 | stirling | 1.5 | 129017 | 38.71 | 36.73 | 122.30 | 612 | worse_than_KRUSTY |
| 200 | 0.3 | soec | 1.0 | 33717 | 10.11 | 10.00 | 34.44 | 172 | beats_FSP_phase1_baseline |
| 200 | 0.3 | soec | 1.5 | 50575 | 15.17 | 10.00 | 45.06 | 225 | beats_KRUSTY_demonstrated |
| 200 | 0.5 | stirling | 1.0 | 86012 | 43.01 | 36.73 | 131.33 | 657 | worse_than_KRUSTY |
| 200 | 0.5 | stirling | 1.5 | 129017 | 64.51 | 36.73 | 176.49 | 882 | worse_than_KRUSTY |
| 200 | 0.5 | soec | 1.0 | 33717 | 16.86 | 10.00 | 48.60 | 243 | beats_KRUSTY_demonstrated |
| 200 | 0.5 | soec | 1.5 | 50575 | 25.29 | 10.00 | 66.30 | 332 | beats_KRUSTY_demonstrated |
| 200 | 1.0 | stirling | 1.0 | 86012 | 86.01 | 36.73 | 221.64 | 1108 | worse_than_KRUSTY |
| 200 | 1.0 | stirling | 1.5 | 129017 | 129.02 | 36.73 | 311.96 | 1560 | worse_than_KRUSTY |
| 200 | 1.0 | soec | 1.0 | 33717 | 33.72 | 10.00 | 84.00 | 420 | worse_than_KRUSTY |
| 200 | 1.0 | soec | 1.5 | 50575 | 50.57 | 10.00 | 119.41 | 597 | worse_than_KRUSTY |
| 300 | 0.1 | stirling | 1.0 | 129017 | 12.90 | 55.10 | 88.62 | 295 | beats_KRUSTY_demonstrated |
| 300 | 0.1 | stirling | 1.5 | 193526 | 19.35 | 55.10 | 102.17 | 341 | beats_KRUSTY_demonstrated |
| 300 | 0.1 | soec | 1.0 | 50575 | 5.06 | 15.00 | 30.42 | 101 | beats_FSP_phase1_baseline |
| 300 | 0.1 | soec | 1.5 | 75862 | 7.59 | 15.00 | 35.73 | 119 | beats_FSP_phase1_baseline |
| 300 | 0.3 | stirling | 1.0 | 129017 | 38.71 | 55.10 | 142.81 | 476 | worse_than_KRUSTY |
| 300 | 0.3 | stirling | 1.5 | 193526 | 58.06 | 55.10 | 183.45 | 612 | worse_than_KRUSTY |
| 300 | 0.3 | soec | 1.0 | 50575 | 15.17 | 15.00 | 51.66 | 172 | beats_FSP_phase1_baseline |
| 300 | 0.3 | soec | 1.5 | 75862 | 22.76 | 15.00 | 67.59 | 225 | beats_KRUSTY_demonstrated |
| 300 | 0.5 | stirling | 1.0 | 129017 | 64.51 | 55.10 | 197.00 | 657 | worse_than_KRUSTY |
| 300 | 0.5 | stirling | 1.5 | 193526 | 96.76 | 55.10 | 264.73 | 882 | worse_than_KRUSTY |
| 300 | 0.5 | soec | 1.0 | 50575 | 25.29 | 15.00 | 72.90 | 243 | beats_KRUSTY_demonstrated |
| 300 | 0.5 | soec | 1.5 | 75862 | 37.93 | 15.00 | 99.46 | 332 | beats_KRUSTY_demonstrated |
| 300 | 1.0 | stirling | 1.0 | 129017 | 129.02 | 55.10 | 332.47 | 1108 | worse_than_KRUSTY |
| 300 | 1.0 | stirling | 1.5 | 193526 | 193.53 | 55.10 | 467.94 | 1560 | worse_than_KRUSTY |
| 300 | 1.0 | soec | 1.0 | 50575 | 50.57 | 15.00 | 126.01 | 420 | worse_than_KRUSTY |
| 300 | 1.0 | soec | 1.5 | 75862 | 75.86 | 15.00 | 179.11 | 597 | worse_than_KRUSTY |
| 500 | 0.1 | stirling | 1.0 | 215029 | 21.50 | 91.84 | 147.71 | 295 | beats_KRUSTY_demonstrated |
| 500 | 0.1 | stirling | 1.5 | 322543 | 32.25 | 91.84 | 170.29 | 341 | beats_KRUSTY_demonstrated |
| 500 | 0.1 | soec | 1.0 | 84291 | 8.43 | 25.00 | 50.70 | 101 | beats_FSP_phase1_baseline |
| 500 | 0.1 | soec | 1.5 | 126437 | 12.64 | 25.00 | 59.55 | 119 | beats_FSP_phase1_baseline |
| 500 | 0.3 | stirling | 1.0 | 215029 | 64.51 | 91.84 | 238.02 | 476 | worse_than_KRUSTY |
| 500 | 0.3 | stirling | 1.5 | 322543 | 96.76 | 91.84 | 305.75 | 612 | worse_than_KRUSTY |
| 500 | 0.3 | soec | 1.0 | 84291 | 25.29 | 25.00 | 86.10 | 172 | beats_FSP_phase1_baseline |
| 500 | 0.3 | soec | 1.5 | 126437 | 37.93 | 25.00 | 112.66 | 225 | beats_KRUSTY_demonstrated |
| 500 | 0.5 | stirling | 1.0 | 215029 | 107.51 | 91.84 | 328.33 | 657 | worse_than_KRUSTY |
| 500 | 0.5 | stirling | 1.5 | 322543 | 161.27 | 91.84 | 441.22 | 882 | worse_than_KRUSTY |
| 500 | 0.5 | soec | 1.0 | 84291 | 42.15 | 25.00 | 121.51 | 243 | beats_KRUSTY_demonstrated |
| 500 | 0.5 | soec | 1.5 | 126437 | 63.22 | 25.00 | 165.76 | 332 | beats_KRUSTY_demonstrated |
| 500 | 1.0 | stirling | 1.0 | 215029 | 215.03 | 91.84 | 554.11 | 1108 | worse_than_KRUSTY |
| 500 | 1.0 | stirling | 1.5 | 322543 | 322.54 | 91.84 | 779.89 | 1560 | worse_than_KRUSTY |
| 500 | 1.0 | soec | 1.0 | 84291 | 84.29 | 25.00 | 210.01 | 420 | worse_than_KRUSTY |
| 500 | 1.0 | soec | 1.5 | 126437 | 126.44 | 25.00 | 298.52 | 597 | worse_than_KRUSTY |
