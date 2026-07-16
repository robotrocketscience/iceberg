### Outbound delta-velocity derivation (first-principles)

- Low Earth orbit circular speed at 400 km altitude: 7.669 km/s
- Earth heliocentric orbital speed: 29.785 km/s
- Hohmann perihelion velocity (Earth's distance): 40.082 km/s
- v_∞ at Earth on outbound Hohmann: 10.298 km/s
- **All-electric outbound integrated Δv (Edelbaum + heliocentric): 17.966 km/s**
- Impulsive-equivalent Δv (Oberth-discounted, chemical-kick reference): 7.287 km/s
- Hohmann cruise time, each way: 6.086 years

**Assumption check:** the prompt cites ~9 km/s for outbound. That figure is the *impulsive* delta-velocity (which gets the Oberth bonus from a single high-thrust burn at perigee). All-electric continuous-thrust does NOT get the Oberth bonus; the integrated delta-velocity is substantially higher (the Edelbaum spiral alone integrates to v_circ_LEO ≈ 7.67 km/s before the spacecraft even reaches Earth-escape).


### Main sweep — all-electric round-trip per reactor class, decomposed-mid and bundled tug, chunk 200 t, electric Isp 2000 s

Round-trip = outbound burn + cruise out (Hohmann) + Saturn ops (1 yr) + inbound burn + cruise back (Hohmann).

| Reactor (kWe) | Model | m_tug (t) | t_out (yr) | cruise (yr) | t_in (yr) | Round-trip (yr) | Closes 15 yr? |
|---:|---|---:|---:|---:|---:|---:|:--:|
| 10 | bundled_10_W_per_kg | 6.2 | 3.48 | 6.09 | 53.97 | 70.62 | no |
| 40 | bundled_10_W_per_kg | 9.3 | 1.30 | 6.09 | 13.69 | 28.17 | no |
| 100 | bundled_10_W_per_kg | 15.5 | 0.87 | 6.09 | 5.64 | 19.68 | no |
| 200 | bundled_10_W_per_kg | 25.8 | 0.72 | 6.09 | 2.95 | 16.85 | no |
| 500 | bundled_10_W_per_kg | 56.7 | 0.64 | 6.09 | 1.34 | 15.15 | no |
| 1000 | bundled_10_W_per_kg | 108.2 | 0.61 | 6.09 | 0.81 | 14.59 | **yes** |
| 10 | decomposed_mid | 3.4 | 1.89 | 6.09 | 53.23 | 68.29 | no |
| 40 | decomposed_mid | 4.2 | 0.59 | 6.09 | 13.36 | 27.12 | no |
| 100 | decomposed_mid | 5.8 | 0.33 | 6.09 | 5.39 | 18.88 | no |
| 200 | decomposed_mid | 8.5 | 0.24 | 6.09 | 2.73 | 16.14 | no |
| 500 | decomposed_mid | 16.6 | 0.19 | 6.09 | 1.13 | 14.49 | **yes** |
| 1000 | decomposed_mid | 30.1 | 0.17 | 6.09 | 0.60 | 13.94 | **yes** |

### Specific-impulse sensitivity — 1 megawatt-electric, decomposed-mid, chunk 200 t

| Isp (s) | t_out (yr) | t_in (yr) | Round-trip (yr) | Closes 15 yr? |
|---:|---:|---:|---:|:--:|
| 2000 | 0.17 | 0.60 | 13.94 | **yes** |
| 3000 | 0.29 | 0.95 | 14.41 | **yes** |
| 4000 | 0.41 | 1.30 | 14.88 | **yes** |

### Chunk sensitivity — 1 megawatt-electric, decomposed-mid, Isp 2000 s

Outbound burn is chunk-independent; inbound scales linearly with chunk.

| Chunk (t) | t_out (yr) | t_in (yr) | Round-trip (yr) | Closes 15 yr? |
|---:|---:|---:|---:|:--:|
| 100 | 0.17 | 0.34 | 13.68 | **yes** |
| 200 | 0.17 | 0.60 | 13.94 | **yes** |
| 500 | 0.17 | 1.39 | 14.73 | **yes** |

### Chemical-kick multiplier re-derivation

Per R-outbound-architecture, chemical-kick versus all-electric-outbound launch mass should be ~6.9×.

Re-derivation here: M_LEO_chemkick / m_v_clean. The 6.9× R-outbound figure is M_LEO_chemkick / M_LEO_allelectric_outbound; the all-electric-outbound LEO mass already includes outbound propellant (mass ratio 1.583 at Δv = 9 km/s, Isp = 2000 s impulsive-equivalent). 10.92× / 1.583 = 6.9×. Both numbers are correct relative to their own baseline.

| m_v (t) | m_kick_dry (t) | m_kick_prop (t) | m_LEO (t) | Multiplier vs m_v_clean |
|---:|---:|---:|---:|---:|
| 5.0 | 4.9 | 44.2 | 54.6 | 10.92× |
| 14.0 | 13.7 | 123.7 | 152.9 | 10.92× |
| 29.0 | 28.5 | 256.2 | 316.8 | 10.92× |
| 105.0 | 103.1 | 927.5 | 1146.9 | 10.92× |

### Close-threshold — smallest reactor that fits inside L0-05's 15-year ceiling

| Mass model | Smallest reactor closing inside 15 yr (kWe) | Round-trip at that reactor (yr) |
|---|---:|---:|
| bundled_10_W_per_kg | 1000 | 14.59 |
| decomposed_mid | 500 | 14.49 |

### Hypothesis grading

| Sub-claim | Predicted | Actual | Held? |
|---|---|---|---|
| H-eo-a — Outbound Δv per first-principles derivation | [8.5, 9.5] km/s | 17.97 km/s | **no** |
| H-eo-b — Outbound burn at 1 MWe (decomposed-mid) | [1.5, 3.0] yr | 0.17 yr | **no** |
| H-eo-c — Outbound burn at 200 kWe (decomposed-mid) | [5.0, 9.0] yr | 0.24 yr | **no** |
| H-eo-d — Outbound burn at 40 kWe exceeds 15 yr | > 15 yr (infeasible) | 0.59 yr | **no** |
| H-eo-e — Round-trip at 1 MWe (decomposed-mid) | [12.0, 14.0] yr | 13.94 yr | yes |
| H-eo-f — Smallest reactor closing inside 15 yr (decomposed-mid) | 200 ≤ close-reactor ≤ 1000 kWe | 500.0 kWe | yes |
| H-eo-g — Bundled and decomposed-mid close within 1 reactor class | decomposed-mid and bundled close within 1 reactor class | bundled 1000.0 kWe / decomposed-mid 500.0 kWe | yes |