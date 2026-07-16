### Unit sanity check — bug confirmation

- Scenario: m_final = 10.0 t, Δv = 9 km/s, Isp = 2000 s, power = 1 MWe.
- Mass ratio (Tsiolkovsky): 1.5823
- True wet mass at start: 15.8229 t
- True propellant: 5.8229 t
- `burn_from_dry_end(m_final)` → m_prop = 5.8229 t  (matches truth)
- `burn_from_wet(m_wet)` → m_prop = 5.8229 t  (matches truth)
- `burn_from_wet(m_final)` [the bugged call pattern] → m_prop = 3.6800 t — **understated by factor 1.5823 = mass_ratio**
- Burn-time understatement factor (same as mass): 1.5823

**Bug confirmed.** The outbound call site at R-electric-outbound `run.py:223` passes `m_tug` (dry-at-end-of-burn) to a function that interprets it as wet-at-start. Outbound propellant mass and outbound burn time are understated by factor mass-ratio. At Isp 2000 s and Δv 17.97 km/s (the all-electric outbound delta-velocity), mass-ratio ≈ 2.50, so outbound burn time is understated 2.50×.

**Inbound call site (run.py:236) is correct as written.** It passes `m_tug + chunk` which IS the wet-at-start mass in the chunk-fed electric architecture: the chunk is water ice and is the propellant supply. Mass at start of inbound burn = m_tug + chunk; mass at end = m_tug + (chunk - prop) = m_tug + delivered. No fix needed.

### Outbound delta-velocity (unchanged from R-electric-outbound)

- All-electric outbound integrated Δv: 17.966 km/s
- Hohmann cruise (each way): 6.086 years

### Sweep A — matrix inbound Δv 6.42 km/s (impulsive-equivalent), bug FIXED, Isp 2000 s, chunk 200 t

Apples-to-apples re-run of R-electric-outbound's main sweep with the outbound formula corrected. `bundled_40_W_per_kg` added for cross-reference against hyperion's 40-W/kg stretch-parameter callout.

| Reactor (kWe) | Model | m_tug (t) | t_out (yr) | t_in (yr) | Round-trip (yr) | Delivered (t) | Closes 15 yr? |
|---:|---|---:|---:|---:|---:|---:|:--:|
| 10 | bundled_10_W_per_kg | 6.5 | 9.12 | 54.05 | 76.34 | 142.4 | no |
| 40 | bundled_10_W_per_kg | 9.7 | 3.42 | 13.72 | 30.32 | 141.5 | no |
| 100 | bundled_10_W_per_kg | 16.2 | 2.28 | 5.66 | 21.11 | 139.6 | no |
| 200 | bundled_10_W_per_kg | 27.0 | 1.90 | 2.97 | 18.04 | 136.6 | no |
| 500 | bundled_10_W_per_kg | 59.5 | 1.67 | 1.36 | 16.20 | 127.6 | no |
| 1000 | bundled_10_W_per_kg | 113.5 | 1.60 | 0.82 | 15.59 | 112.5 | no |
| 10 | bundled_40_W_per_kg | 5.7 | 7.98 | 53.84 | 74.99 | 142.6 | no |
| 40 | bundled_40_W_per_kg | 6.5 | 2.28 | 13.51 | 28.96 | 142.4 | no |
| 100 | bundled_40_W_per_kg | 8.1 | 1.14 | 5.45 | 19.76 | 141.9 | no |
| 200 | bundled_40_W_per_kg | 10.8 | 0.76 | 2.76 | 16.69 | 141.2 | no |
| 500 | bundled_40_W_per_kg | 18.9 | 0.53 | 1.15 | 14.85 | 138.9 | **yes** |
| 1000 | bundled_40_W_per_kg | 32.4 | 0.46 | 0.61 | 14.24 | 135.1 | **yes** |
| 10 | decomposed_mid | 3.5 | 4.96 | 53.27 | 71.40 | 143.2 | no |
| 40 | decomposed_mid | 4.4 | 1.54 | 13.37 | 28.08 | 142.9 | no |
| 100 | decomposed_mid | 6.1 | 0.85 | 5.39 | 19.42 | 142.5 | no |
| 200 | decomposed_mid | 8.9 | 0.63 | 2.73 | 16.53 | 141.7 | no |
| 500 | decomposed_mid | 17.4 | 0.49 | 1.14 | 14.80 | 139.3 | **yes** |
| 1000 | decomposed_mid | 31.5 | 0.44 | 0.61 | 14.22 | 135.4 | **yes** |

### Sweep B — matrix inbound Δv 6.42 km/s, BUG INTACT (reproduction of R-electric-outbound), Isp 2000 s, chunk 200 t

Sanity check: reproduces R-electric-outbound's tables.md numbers for `bundled_10_W_per_kg` and `decomposed_mid` rows, confirming the rerun matches the original on identical inputs when the bug is preserved.

| Reactor (kWe) | Model | m_tug (t) | t_out (yr) | t_in (yr) | Round-trip (yr) | Delivered (t) | Closes 15 yr? |
|---:|---|---:|---:|---:|---:|---:|:--:|
| 10 | bundled_10_W_per_kg | 6.2 | 3.48 | 53.97 | 70.62 | 142.4 | no |
| 40 | bundled_10_W_per_kg | 9.3 | 1.30 | 13.69 | 28.17 | 141.6 | no |
| 100 | bundled_10_W_per_kg | 15.5 | 0.87 | 5.64 | 19.68 | 139.9 | no |
| 200 | bundled_10_W_per_kg | 25.8 | 0.72 | 2.95 | 16.85 | 137.0 | no |
| 500 | bundled_10_W_per_kg | 56.7 | 0.64 | 1.34 | 15.15 | 128.3 | no |
| 1000 | bundled_10_W_per_kg | 108.2 | 0.61 | 0.81 | 14.59 | 114.0 | **yes** |
| 10 | bundled_40_W_per_kg | 5.4 | 3.04 | 53.77 | 69.98 | 142.7 | no |
| 40 | bundled_40_W_per_kg | 6.2 | 0.87 | 13.49 | 27.53 | 142.4 | no |
| 100 | bundled_40_W_per_kg | 7.7 | 0.43 | 5.44 | 19.04 | 142.0 | no |
| 200 | bundled_40_W_per_kg | 10.3 | 0.29 | 2.75 | 16.21 | 141.3 | no |
| 500 | bundled_40_W_per_kg | 18.0 | 0.20 | 1.14 | 14.52 | 139.1 | **yes** |
| 1000 | bundled_40_W_per_kg | 30.9 | 0.17 | 0.60 | 13.95 | 135.5 | **yes** |
| 10 | decomposed_mid | 3.4 | 1.89 | 53.23 | 68.29 | 143.2 | no |
| 40 | decomposed_mid | 4.2 | 0.59 | 13.36 | 27.12 | 143.0 | no |
| 100 | decomposed_mid | 5.8 | 0.33 | 5.39 | 18.88 | 142.6 | no |
| 200 | decomposed_mid | 8.5 | 0.24 | 2.73 | 16.14 | 141.8 | no |
| 500 | decomposed_mid | 16.6 | 0.19 | 1.13 | 14.49 | 139.5 | **yes** |
| 1000 | decomposed_mid | 30.1 | 0.17 | 0.60 | 13.94 | 135.8 | **yes** |

### Sweep C — titan inbound Δv 24.7 km/s (high-elliptical Saturn departure + lunar gravity assist), bug FIXED, Isp 2000 s, chunk 200 t

Inbound delta-velocity per titan's R-inbound-dv-continuous-thrust round, best-case high-elliptical regime.

| Reactor (kWe) | Model | m_tug (t) | t_out (yr) | t_in (yr) | Round-trip (yr) | Delivered (t) | Closes 15 yr? |
|---:|---|---:|---:|---:|---:|---:|:--:|
| 10 | bundled_10_W_per_kg | 6.5 | 9.12 | 138.66 | 160.95 | 52.1 | no |
| 40 | bundled_10_W_per_kg | 9.7 | 3.42 | 35.21 | 51.80 | 49.8 | no |
| 100 | bundled_10_W_per_kg | 16.2 | 2.28 | 14.52 | 29.97 | 45.2 | no |
| 200 | bundled_10_W_per_kg | 27.0 | 1.90 | 7.62 | 22.69 | 37.4 | no |
| 500 | bundled_10_W_per_kg | 59.5 | 1.67 | 3.48 | 18.33 | 14.2 | no |
| 1000 | bundled_10_W_per_kg | 113.5 | 1.60 | 2.11 | 16.87 | -24.5 | no |
| 10 | bundled_40_W_per_kg | 5.7 | 7.98 | 138.12 | 159.27 | 52.7 | no |
| 40 | bundled_40_W_per_kg | 6.5 | 2.28 | 34.67 | 50.12 | 52.1 | no |
| 100 | bundled_40_W_per_kg | 8.1 | 1.14 | 13.98 | 28.29 | 51.0 | no |
| 200 | bundled_40_W_per_kg | 10.8 | 0.76 | 7.08 | 21.01 | 49.0 | no |
| 500 | bundled_40_W_per_kg | 18.9 | 0.53 | 2.94 | 16.64 | 43.2 | no |
| 1000 | bundled_40_W_per_kg | 32.4 | 0.46 | 1.56 | 15.19 | 33.5 | no |
| 10 | decomposed_mid | 3.5 | 4.96 | 136.67 | 154.80 | 54.2 | no |
| 40 | decomposed_mid | 4.4 | 1.54 | 34.31 | 49.02 | 53.6 | no |
| 100 | decomposed_mid | 6.1 | 0.85 | 13.84 | 27.86 | 52.4 | no |
| 200 | decomposed_mid | 8.9 | 0.63 | 7.01 | 20.81 | 50.4 | no |
| 500 | decomposed_mid | 17.4 | 0.49 | 2.92 | 16.58 | 44.3 | no |
| 1000 | decomposed_mid | 31.5 | 0.44 | 1.55 | 15.17 | 34.2 | no |

### Sweep D — titan inbound Δv 40.2 km/s (B-ring Saturn departure, no lunar gravity assist), bug FIXED, Isp 2000 s, chunk 200 t

Inbound delta-velocity per titan's R-inbound-dv-continuous-thrust round, worst-case B-ring regime — what the current ICEBERG-conops Phase 5–6 architecture actually requires.

| Reactor (kWe) | Model | m_tug (t) | t_out (yr) | t_in (yr) | Round-trip (yr) | Delivered (t) | Closes 15 yr? |
|---:|---|---:|---:|---:|---:|---:|:--:|
| 10 | bundled_10_W_per_kg | 6.5 | 9.12 | 168.68 | 190.97 | 20.1 | no |
| 40 | bundled_10_W_per_kg | 9.7 | 3.42 | 42.83 | 59.42 | 17.3 | no |
| 100 | bundled_10_W_per_kg | 16.2 | 2.28 | 17.66 | 33.11 | 11.6 | no |
| 200 | bundled_10_W_per_kg | 27.0 | 1.90 | 9.27 | 24.34 | 2.2 | no |
| 500 | bundled_10_W_per_kg | 59.5 | 1.67 | 4.24 | 19.08 | -26.0 | no |
| 1000 | bundled_10_W_per_kg | 113.5 | 1.60 | 2.56 | 17.33 | -73.1 | no |
| 10 | bundled_40_W_per_kg | 5.7 | 7.98 | 168.02 | 189.17 | 20.8 | no |
| 40 | bundled_40_W_per_kg | 6.5 | 2.28 | 42.17 | 57.62 | 20.1 | no |
| 100 | bundled_40_W_per_kg | 8.1 | 1.14 | 17.00 | 31.31 | 18.7 | no |
| 200 | bundled_40_W_per_kg | 10.8 | 0.76 | 8.61 | 22.54 | 16.3 | no |
| 500 | bundled_40_W_per_kg | 18.9 | 0.53 | 3.58 | 17.28 | 9.3 | no |
| 1000 | bundled_40_W_per_kg | 32.4 | 0.46 | 1.90 | 15.53 | -2.5 | no |
| 10 | decomposed_mid | 3.5 | 4.96 | 166.26 | 184.39 | 22.7 | no |
| 40 | decomposed_mid | 4.4 | 1.54 | 41.74 | 56.45 | 21.9 | no |
| 100 | decomposed_mid | 6.1 | 0.85 | 16.83 | 30.86 | 20.5 | no |
| 200 | decomposed_mid | 8.9 | 0.63 | 8.53 | 22.33 | 18.0 | no |
| 500 | decomposed_mid | 17.4 | 0.49 | 3.55 | 17.21 | 10.6 | no |
| 1000 | decomposed_mid | 31.5 | 0.44 | 1.89 | 15.51 | -1.7 | no |

### Close-threshold summary — smallest reactor inside L0-05's 15-year ceiling

| Sweep | Model | Smallest closing reactor (kWe) | Round-trip at close (yr) |
|---|---|---:|---:|
| matrix_inbound_6.42_corrected | bundled_10_W_per_kg | **no class closes** | — |
| matrix_inbound_6.42_corrected | bundled_40_W_per_kg | 500 | 14.85 |
| matrix_inbound_6.42_corrected | decomposed_mid | 500 | 14.80 |
| matrix_inbound_6.42_bugged | bundled_10_W_per_kg | 1000 | 14.59 |
| matrix_inbound_6.42_bugged | bundled_40_W_per_kg | 500 | 14.52 |
| matrix_inbound_6.42_bugged | decomposed_mid | 500 | 14.49 |
| titan_inbound_24.7_high_elliptical | bundled_10_W_per_kg | **no class closes** | — |
| titan_inbound_24.7_high_elliptical | bundled_40_W_per_kg | **no class closes** | — |
| titan_inbound_24.7_high_elliptical | decomposed_mid | **no class closes** | — |
| titan_inbound_40.2_b_ring | bundled_10_W_per_kg | **no class closes** | — |
| titan_inbound_40.2_b_ring | bundled_40_W_per_kg | **no class closes** | — |
| titan_inbound_40.2_b_ring | decomposed_mid | **no class closes** | — |

### Headline — 1 MWe, decomposed-mid, Isp 2000 s, chunk 200 t — across inbound regimes

| Inbound regime | Mass model | t_out (yr) | t_in (yr) | Round-trip (yr) | Delivered (t) | Closes 15 yr? |
|---|---|---:|---:|---:|---:|:--:|
| matrix_inbound_6.42_corrected_decomposed_mid_1mwe | — | 0.44 | 0.61 | 14.22 | 135.4 | **yes** |
| titan_inbound_24.7_he_decomposed_mid_1mwe | — | 0.44 | 1.55 | 15.17 | 34.2 | no |
| titan_inbound_40.2_br_decomposed_mid_1mwe | — | 0.44 | 1.89 | 15.51 | -1.7 | no |
| titan_inbound_24.7_he_bundled_40_W_per_kg_1mwe | — | 0.46 | 1.56 | 15.19 | 33.5 | no |
| titan_inbound_40.2_br_bundled_40_W_per_kg_1mwe | — | 0.46 | 1.90 | 15.53 | -2.5 | no |

### Hypothesis grading

| Sub-claim | Predicted | Actual | Held? |
|---|---|---|---|
| H-eor-a — Outbound burn time understatement at 1 MWe / decomposed-mid / Isp 2000 s | [2.0, 3.0]× | 2.621× | yes |
| H-eor-b — Corrected smallest reactor closing (decomposed-mid, matrix-inbound) | > 500 kWe (upward from original) | corrected 500.0 kWe / bugged 500.0 kWe | **no** |
| H-eor-c — No 10-W/kg cell closes at titan-inbound 24.7 km/s | no 10-W/kg cell closes at titan-inbound 24.7 km/s | any close = False | yes |
| H-eor-d — At least one 40-W/kg cell closes at titan-inbound 24.7 km/s | at least one 40-W/kg cell closes at titan-inbound 24.7 km/s | any close = False | **no** |