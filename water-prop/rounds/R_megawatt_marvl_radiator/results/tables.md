### Mass breakdown at 1 MWe (no propellant)

MARVL-anchored decomposed model targets the National Academies 2021 / NASA MARVL midpoints: reactor+shield ~30%, power conversion ~20%, radiator ~50% of stack mass.

| Model | m_fixed (t) | m_reactor (t) | m_PC (t) | m_radiator (t) | m_stack/total (t) | Radiator fraction |
|---|---:|---:|---:|---:|---:|---:|
| decomposed_mid | 3.0 | 20.0 | 5.0 | 1.2 | 29.2 | 4.0% |
| decomposed_marvl | 5.0 | 30.3 | 20.0 | 49.6 | 104.9 | 47.3% |
| bundled_10_W_per_kg | 5.0 | (bundled) | (bundled) | (bundled) | 105.0 | n/a |

### Sweep A — megawatt all-electric end-to-end, corrected outbound Δv 29.56 km/s (no LGA), titan inbound 24.7 km/s

All corrections applied: outbound formula bug-fix, outbound Δv symmetric correction, titan's continuous-thrust inbound, chunk-fed wet-at-start inbound. Mass model sweeps the three candidates: decomposed-mid (optimistic, R-electric-outbound baseline), decomposed-MARVL (power-finding-4 anchored), bundled 10 W/kg (closer-to-correct per power-finding-4).

| Reactor (kWe) | Mass model | m_tug (t) | t_out (yr) | t_in (yr) | Round-trip (yr) | Delivered (t) | Closes 15 yr? |
|---:|---|---:|---:|---:|---:|---:|:--:|
| 40 | decomposed_mid | 4.9 | 4.04 | 34.40 | 51.62 | 53.3 | no |
| 100 | decomposed_mid | 6.8 | 2.25 | 13.89 | 29.30 | 51.9 | no |
| 200 | decomposed_mid | 10.0 | 1.65 | 7.05 | 21.87 | 49.6 | no |
| 500 | decomposed_mid | 19.5 | 1.29 | 2.95 | 17.41 | 42.8 | no |
| 1000 | decomposed_mid | 35.4 | 1.17 | 1.58 | 15.92 | 31.4 | no |
| 2000 | decomposed_mid | 67.1 | 1.11 | 0.90 | 15.17 | 8.7 | no |
| 40 | decomposed_marvl | 10.9 | 8.99 | 35.41 | 57.57 | 49.0 | no |
| 100 | decomposed_marvl | 18.2 | 5.99 | 14.65 | 33.82 | 43.7 | no |
| 200 | decomposed_marvl | 30.3 | 4.99 | 7.73 | 25.90 | 35.1 | no |
| 500 | decomposed_marvl | 66.7 | 4.39 | 3.58 | 21.15 | 9.0 | no |
| 1000 | decomposed_marvl | 127.3 | 4.19 | 2.20 | 19.56 | -34.4 | no |
| 2000 | decomposed_marvl | 248.6 | 4.09 | 1.51 | 18.77 | -121.2 | no |
| 40 | bundled_10_W_per_kg | 10.9 | 8.99 | 35.41 | 57.57 | 48.9 | no |
| 100 | bundled_10_W_per_kg | 18.2 | 6.00 | 14.65 | 33.82 | 43.7 | no |
| 200 | bundled_10_W_per_kg | 30.3 | 5.00 | 7.73 | 25.90 | 35.0 | no |
| 500 | bundled_10_W_per_kg | 66.7 | 4.40 | 3.58 | 21.15 | 9.0 | no |
| 1000 | bundled_10_W_per_kg | 127.4 | 4.20 | 2.20 | 19.57 | -34.5 | no |
| 2000 | bundled_10_W_per_kg | 248.7 | 4.10 | 1.51 | 18.78 | -121.3 | no |

### Sweep B — best-case composite (LGA credit on BOTH outbound and inbound), titan inbound 24.7 km/s

Same as Sweep A but outbound LGA credit applied (27.56 km/s instead of 29.56). Most favorable operational case for megawatt all-electric end-to-end short of architectural changes (chunk-as-heat-shield, chunk-size reduction).

| Reactor (kWe) | Mass model | m_tug (t) | t_out (yr) | t_in (yr) | Round-trip (yr) | Delivered (t) | Closes 15 yr? |
|---:|---|---:|---:|---:|---:|---:|:--:|
| 40 | decomposed_mid | 4.8 | 3.45 | 34.38 | 51.00 | 53.3 | no |
| 100 | decomposed_mid | 6.6 | 1.91 | 13.88 | 28.96 | 52.0 | no |
| 200 | decomposed_mid | 9.7 | 1.40 | 7.04 | 21.62 | 49.8 | no |
| 500 | decomposed_mid | 19.0 | 1.10 | 2.94 | 17.21 | 43.2 | no |
| 1000 | decomposed_mid | 34.5 | 0.99 | 1.57 | 15.74 | 32.1 | no |
| 2000 | decomposed_mid | 65.4 | 0.94 | 0.89 | 15.01 | 9.9 | no |
| 40 | decomposed_marvl | 10.6 | 7.67 | 35.36 | 56.20 | 49.2 | no |
| 100 | decomposed_marvl | 17.7 | 5.11 | 14.62 | 32.90 | 44.1 | no |
| 200 | decomposed_marvl | 29.5 | 4.26 | 7.71 | 25.14 | 35.6 | no |
| 500 | decomposed_marvl | 65.0 | 3.75 | 3.56 | 20.48 | 10.2 | no |
| 1000 | decomposed_marvl | 124.0 | 3.58 | 2.18 | 18.93 | -32.1 | no |
| 2000 | decomposed_marvl | 242.1 | 3.49 | 1.48 | 18.15 | -116.6 | no |
| 40 | bundled_10_W_per_kg | 10.6 | 7.67 | 35.36 | 56.20 | 49.2 | no |
| 100 | bundled_10_W_per_kg | 17.7 | 5.11 | 14.62 | 32.91 | 44.1 | no |
| 200 | bundled_10_W_per_kg | 29.5 | 4.26 | 7.71 | 25.14 | 35.6 | no |
| 500 | bundled_10_W_per_kg | 65.0 | 3.75 | 3.56 | 20.48 | 10.2 | no |
| 1000 | bundled_10_W_per_kg | 124.1 | 3.58 | 2.18 | 18.93 | -32.1 | no |
| 2000 | bundled_10_W_per_kg | 242.3 | 3.49 | 1.48 | 18.15 | -116.7 | no |

### Sweep C — year-zero-through-fifteen architecture (chemical-kick outbound + electric inbound)

Outbound is chemical-kick (off the round-trip Δv ledger for the spacecraft's electric thrusters). Inbound is electric at the matrix's impulsive-equivalent 6.42 km/s (valid for chemical-kick architecture which preserves Oberth-bonus impulsive injection). Round-trip = cruise_out + ops + electric_inbound_burn + cruise_back. This is the architecture the Kilopower Variant B winner cell is built on.

| Reactor (kWe) | Mass model | m_tug (t) | t_out (yr) | t_in (yr) | Round-trip (yr) | Delivered (t) | Closes 15 yr? |
|---:|---|---:|---:|---:|---:|---:|:--:|
| 40 | decomposed_mid | 4.0 | — | 13.35 | 26.52 | 143.0 | no |
| 100 | decomposed_mid | 5.6 | — | 5.38 | 18.55 | 142.6 | no |
| 200 | decomposed_mid | 8.2 | — | 2.73 | 15.90 | 141.9 | no |
| 500 | decomposed_mid | 16.1 | — | 1.13 | 14.30 | 139.7 | **yes** |
| 1000 | decomposed_mid | 29.2 | — | 0.60 | 13.77 | 136.0 | **yes** |
| 2000 | decomposed_mid | 55.3 | — | 0.33 | 13.51 | 128.7 | **yes** |
| 40 | decomposed_marvl | 9.0 | — | 13.68 | 26.85 | 141.7 | no |
| 100 | decomposed_marvl | 15.0 | — | 5.63 | 18.80 | 140.0 | no |
| 200 | decomposed_marvl | 25.0 | — | 2.94 | 16.12 | 137.2 | no |
| 500 | decomposed_marvl | 55.0 | — | 1.33 | 14.51 | 128.8 | **yes** |
| 1000 | decomposed_marvl | 104.9 | — | 0.80 | 13.97 | 114.9 | **yes** |
| 2000 | decomposed_marvl | 204.9 | — | 0.53 | 13.70 | 87.0 | **yes** |
| 40 | bundled_10_W_per_kg | 9.0 | — | 13.68 | 26.85 | 141.7 | no |
| 100 | bundled_10_W_per_kg | 15.0 | — | 5.63 | 18.80 | 140.0 | no |
| 200 | bundled_10_W_per_kg | 25.0 | — | 2.94 | 16.12 | 137.2 | no |
| 500 | bundled_10_W_per_kg | 55.0 | — | 1.33 | 14.51 | 128.8 | **yes** |
| 1000 | bundled_10_W_per_kg | 105.0 | — | 0.80 | 13.97 | 114.9 | **yes** |
| 2000 | bundled_10_W_per_kg | 205.0 | — | 0.53 | 13.70 | 86.9 | **yes** |

### Hypothesis grading

| Sub-claim | Predicted | Actual | Held? |
|---|---|---|---|
| H-mr-a — MARVL-anchored 1 MWe tug mass | [95.0, 115.0] t | 104.9 t | yes |
| H-mr-b — MARVL-anchored 1 MWe / titan-24.7 round-trip > 18 yr | > 18 yr | 19.56459937950773 | yes |
| H-mr-c — MARVL-anchored 1 MWe / titan-24.7 delivered mass < 0 | < 0 t (chunk-fed insufficient) | -34.411594858825765 t | yes |
| H-mr-d — MARVL-anchored 200 kWe chemical-kick architecture closes with positive delivered | closes inside L0-05 with positive delivered mass | round-trip 16.12 yr, delivered 137.2 t | **no** |
| H-mr-e — No realistic-mass-model megawatt cell closes at LGA-both-legs | no realistic-mass-model megawatt cell closes even at LGA-both-legs | any close = False | yes |