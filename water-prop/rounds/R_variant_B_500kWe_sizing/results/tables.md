### Variant B at MARVL-anchored mass — conservative chemical-kick (9 km/s), inbound 6.42 km/s, chunk 200 t, specific impulse 2000 s

| Reactor (kWe) | Tug dry (t) | Kick prop (t) | LEO mission-1 (t) | LEO missionN (t) | Inbound prop (t) | t_in (yr) | Round-trip (yr) | Delivered (t) | Fraction | Closes strict 15? | Closes soft 16? | Expected (uniform, t) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|:--:|:--:|---:|
| 500 | 58.6 | 458.6 | 527.1 | 68.6 | 72.2 | 1.35 | 14.53 | 127.8 | 0.639 | **yes** | **yes** | 0.1662 |
| 750 | 83.9 | 628.0 | 721.9 | 93.9 | 79.3 | 0.99 | 14.16 | 120.7 | 0.604 | **yes** | **yes** | 0.1570 |
| 1000 | 109.3 | 797.4 | 916.7 | 119.3 | 86.3 | 0.81 | 13.98 | 113.7 | 0.568 | **yes** | **yes** | 0.1478 |

### Variant B at MARVL-anchored mass — realistic chemical-kick (5 km/s; 3.6 trans-Saturn injection + 1.4 Saturn capture), other parameters identical

| Reactor (kWe) | Tug dry (t) | Kick prop (t) | LEO mission-1 (t) | LEO missionN (t) | Inbound prop (t) | t_in (yr) | Round-trip (yr) | Delivered (t) | Fraction | Closes strict 15? | Closes soft 16? | Expected (uniform, t) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|:--:|:--:|---:|
| 500 | 58.6 | 144.4 | 213.0 | 68.6 | 72.2 | 1.35 | 14.53 | 127.8 | 0.639 | **yes** | **yes** | 0.1662 |
| 750 | 83.9 | 197.7 | 291.6 | 93.9 | 79.3 | 0.99 | 14.16 | 120.7 | 0.604 | **yes** | **yes** | 0.1570 |
| 1000 | 109.3 | 251.1 | 370.3 | 119.3 | 86.3 | 0.81 | 13.98 | 113.7 | 0.568 | **yes** | **yes** | 0.1478 |

### MARVL mass breakdown at each reactor power (no propellant)

| Reactor (kWe) | m_fixed (t) | m_reactor (t) | m_PC (t) | m_radiator (t) | Total (t) | Radiator fraction |
|---:|---:|---:|---:|---:|---:|---:|
| 500 | 5.0 | 15.2 | 10.0 | 24.8 | 55.0 | 45.2% |
| 750 | 5.0 | 22.7 | 15.0 | 37.2 | 80.0 | 46.6% |
| 1000 | 5.0 | 30.3 | 20.0 | 49.6 | 104.9 | 47.3% |

### Programmatic-risk overlay (Round A propagation)

P(500-kilowatt-electric class reactor on orbit by 2035) per prior:

- Uniform Beta(1,7) posterior: 0.0013
- Jeffreys Beta(0.5,6.5) posterior: 0.0003
- Skeptical Beta(0.5,11.5) posterior: 0.0001

### Hypothesis grading

| Sub-claim | Predicted | Measured | Held? |
|---|---|---|---|
| H-vbs-a — 500 kWe round-trip (yr) | 12.5-14.5 (point 13.5) | 14.53 | **no** |
| H-vbs-b — 500 kWe delivered (t) | 80-110 (point 95) | 127.8 | **no** |
| H-vbs-c — 1000 kWe round-trip 12.0-13.5 yr AND delivered 100-125 t | see ranges | round-trip 13.98 yr, delivered 113.7 t | **no** |
| H-vbs-d — 500 kWe LEO mission-1 launch mass (t) | 350-550 (point 450) | 527.1 | yes |
| H-vbs-e — 500 kWe expected delivered, uniform prior (t) | 0.10-0.15 (point 0.12) | 0.1662 | **no** |