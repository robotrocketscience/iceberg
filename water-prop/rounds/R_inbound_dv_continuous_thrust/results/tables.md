### Hohmann baseline and spiral endpoints

- Hohmann perihelion velocity at Earth: 40.082 km/s
- Hohmann aphelion velocity at Saturn: 4.183 km/s
- Earth heliocentric orbital speed: 29.785 km/s
- Saturn heliocentric orbital speed: 9.622 km/s
- Velocity-at-infinity at Earth from Hohmann return: 10.298 km/s
- Velocity-at-infinity at Saturn from Hohmann return: 5.439 km/s
- Low-Earth-orbit Edelbaum capture spiral integrated delta-velocity: 7.669 km/s
- Hohmann cruise time, each way: 6.09 years


### Continuous-thrust inbound delta-velocity decomposition (no lunar gravity assist credit)

| Saturn departure | Saturn spiral | Saturn helio | Earth helio | LEO spiral | Total |
|---|---:|---:|---:|---:|---:|
| B_ring (r = 1.35e+05 km) | 16.76 | 5.44 | 10.30 | 7.67 | **40.17** km/s |
| high_elliptical_1Mkm (r = 1.00e+06 km) | 6.16 | 5.44 | 10.30 | 7.67 | **29.56** km/s |
| Iapetus_distance (r = 3.56e+06 km) | 3.26 | 5.44 | 10.30 | 7.67 | **26.67** km/s |

### With lunar gravity assist credit (2.0 km/s shaved off Earth phase)

| Saturn departure | Saturn spiral | Saturn helio | Earth phase post-LGA | Total |
|---|---:|---:|---:|---:|
| B_ring | 16.76 | 5.44 | 15.97 | **38.17** km/s |
| high_elliptical_1Mkm | 6.16 | 5.44 | 15.97 | **27.56** km/s |
| Iapetus_distance | 3.26 | 5.44 | 15.97 | **24.67** km/s |

### Headline comparison — matrix value versus continuous-thrust

| Case | Inbound delta-velocity (km/s) | Multiple of matrix 6.42 |
|---|---:|---:|
| Matrix assumed | 6.42 | 1.00× |
| B ring no lga | 40.17 | 6.26× |
| B ring with lga | 38.17 | 5.95× |
| high elliptical no lga | 29.56 | 4.60× |
| high elliptical with lga | 27.56 | 4.29× |
| Iapetus no lga | 26.67 | 4.15× |
| Iapetus with lga | 24.67 | 3.84× |

### Megawatt all-electric end-to-end round-trip under each delta-velocity case

Reactor 1000 kWe, Isp 2000 s, chunk 200 t. Outbound + 2× cruise + Saturn ops + inbound.

| Case | dv_inbound (km/s) | mass ratio | m_prop (t) | delivered (t) | t_inbound (yr) | round-trip (yr) | closes 15 yr? |
|---|---:|---:|---:|---:|---:|---:|:--:|
| matrix_6_42 | 6.42 | 1.39 | 59.2 | 140.8 | 0.56 | 13.90 | **yes** |
| B_ring_no_lga | 40.17 | 7.75 | 184.7 | 15.3 | 1.73 | 15.07 | **no** |
| B_ring_with_lga | 38.17 | 7.00 | 181.8 | 18.2 | 1.70 | 15.05 | **no** |
| high_elliptical_no_lga | 29.56 | 4.51 | 165.1 | 34.9 | 1.55 | 14.89 | **yes** |
| high_elliptical_with_lga | 27.56 | 4.08 | 160.1 | 39.9 | 1.50 | 14.84 | **yes** |
| Iapetus_no_lga | 26.67 | 3.90 | 157.6 | 42.4 | 1.48 | 14.82 | **yes** |
| Iapetus_with_lga | 24.67 | 3.52 | 151.8 | 48.2 | 1.42 | 14.77 | **yes** |

### Power sensitivity at most-favorable continuous-thrust architecture (high-elliptical Saturn departure with lunar gravity assist credit)

Inbound delta-velocity = 27.56 km/s. Isp 2000 s, chunk 200 t.

| Reactor (kWe) | m_tug (t) | m_prop (t) | delivered (t) | delivered frac | t_inbound (yr) | round-trip (yr) | closes 15 yr? |
|---:|---:|---:|---:|---:|---:|---:|:--:|
| 100 | 5.5 | 155.1 | 44.9 | 22.5% | 14.54 | 28.07 | **no** |
| 200 | 7.5 | 156.6 | 43.4 | 21.7% | 7.34 | 20.75 | **no** |
| 500 | 10.0 | 158.5 | 41.5 | 20.8% | 2.97 | 16.32 | **no** |
| 1000 | 12.1 | 160.1 | 39.9 | 20.0% | 1.50 | 14.84 | **yes** |
| 2000 | 16.4 | 163.3 | 36.7 | 18.3% | 0.77 | 14.10 | **yes** |

### Specific-impulse sensitivity at 1000 kWe, high-elliptical with LGA, chunk 200 t

| Isp (s) | mass ratio | m_prop (t) | delivered frac | t_inbound (yr) | round-trip (yr) | closes 15 yr? |
|---:|---:|---:|---:|---:|---:|:--:|
| 2000 | 4.08 | 160.1 | 20.0% | 1.50 | 14.84 | **yes** |
| 3000 | 2.55 | 129.0 | 35.5% | 2.72 | 16.06 | **no** |
| 4000 | 2.02 | 107.1 | 46.5% | 4.02 | 17.36 | **no** |

### Chunk-mass sensitivity at 1000 kWe, Isp 2000 s, high-elliptical with LGA

| Chunk (t) | m_prop (t) | delivered (t) | delivered frac | t_inbound (yr) | round-trip (yr) | closes 15 yr? |
|---:|---:|---:|---:|---:|---:|:--:|
| 100 | 84.6 | 15.4 | 15.4% | 0.79 | 14.14 | **yes** |
| 200 | 160.1 | 39.9 | 20.0% | 1.50 | 14.84 | **yes** |
| 500 | 386.5 | 113.5 | 22.7% | 3.62 | 16.97 | **no** |

### Hypothesis grading

| Sub-claim | Predicted | Actual | Held? |
|---|---|---|---|
| H-it-a — Saturn spiral-out (B-ring) | [14.0, 18.0] km/s | 16.76 km/s | yes |
| H-it-b — Saturn-side heliocentric drop | [5.0, 5.8] km/s | 5.44 km/s | yes |
| H-it-c — Earth-side heliocentric drop | [10.0, 10.6] km/s | 10.30 km/s | yes |
| H-it-d — Earth Edelbaum capture spiral | [7.5, 7.9] km/s | 7.67 km/s | yes |
| H-it-e — Total dv, B-ring no LGA | [36.0, 42.0] km/s | 40.17 km/s | yes |
| H-it-f — Total dv, B-ring with LGA | [34.0, 40.0] km/s | 38.17 km/s | yes |
| H-it-g — Doubled-from-impulsive (10–14) | [10.0, 14.0] km/s | B-ring 40.17, high-elliptical 29.56 km/s | **no** (load-bearing falsified high: True) |
| H-it-h — Megawatt round-trip ≤ 15.5 yr | ≤ 15.5 yr | B-ring/LGA 15.05 yr, high-elliptical/LGA 14.84 yr | B-ring: yes; high-elliptical: yes |
| H-it-i — Delivered fraction 25–55% | [25, 55]% | B-ring/LGA 9.1%, high-elliptical/LGA 20.0% | B-ring: **no**; high-elliptical: **no** |