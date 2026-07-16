# R-saturn-shadow-and-station-location — results

Target useful electrolysis output: 200.0 kW.
Thermal-storage specific energy: 100.0 Wh/kg (latent-heat phase-change material, conservative — laboratory salts achieve 200–400 Wh/kg).

Fission benchmarks (kg/kW): {'FSP_stretch_10W_per_kg': 100.0, 'FSP_phase1_contracted_5W_per_kg': 200.0, 'KRUSTY_demonstrated_2p4W_per_kg': 416.0}

| station | f_dark | t_dark_h | duty | storage_t | total_t | kg/kW | vs_fission | conops |
|---|---|---|---|---|---|---|---|---|
| saturn_sun_L1_halo | 0.00 | 0.0 | 1.00 | 0.0 | 20.3 | 101 | beats_FSP_phase1_baseline | yes |
| high_eccentric_saturn_orbit | 0.03 | 4.0 | 1.03 | 8.0 | 28.5 | 142 | beats_FSP_phase1_baseline | yes |
| low_equatorial_saturn_orbit | 0.40 | 2.5 | 1.67 | 5.0 | 30.0 | 150 | beats_FSP_phase1_baseline | yes |
| titan_surface | 0.50 | 192.0 | 2.00 | 384.0 | 411.4 | 2057 | worse_than_KRUSTY | yes |
| enceladus_surface | 0.50 | 16.4 | 2.00 | 32.8 | 60.2 | 301 | beats_KRUSTY_demonstrated | yes |
