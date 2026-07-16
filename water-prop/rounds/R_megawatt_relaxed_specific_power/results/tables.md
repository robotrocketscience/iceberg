### Specific-power sweep (1 megawatt-electric, chunk 200 t, specific impulse 2000 s, outbound 29.56 km/s, inbound 24.7 km/s)

| Specific power (W/kg) | m_stack (t) | m_tug (t) | t_outbound (yr) | t_inbound (yr) | Round-trip (yr) | Delivered (t) | Delivered fraction | Closes 15 yr & delivers > 0? | Expected (uniform, t) |
|---:|---:|---:|---:|---:|---:|---:|---:|:--:|---:|
| 10 | 100.00 | 127.38 | 4.20 | 2.20 | 19.57 | -34.5 | -0.172 | no | 0.0000 |
| 20 | 50.00 | 66.72 | 2.20 | 1.79 | 17.16 | 9.0 | 0.045 | no | 0.0117 |
| 30 | 33.33 | 46.50 | 1.53 | 1.66 | 16.36 | 23.5 | 0.117 | no | 0.0305 |
| 40 | 25.00 | 36.39 | 1.20 | 1.59 | 15.96 | 30.7 | 0.154 | no | 0.0399 |
| 50 | 20.00 | 30.33 | 1.00 | 1.55 | 15.72 | 35.0 | 0.175 | no | 0.0456 |
| 60 | 16.67 | 26.28 | 0.87 | 1.52 | 15.56 | 37.9 | 0.190 | no | 0.0493 |
| 80 | 12.50 | 21.23 | 0.70 | 1.49 | 15.36 | 41.6 | 0.208 | no | 0.0540 |
| 100 | 10.00 | 18.20 | 0.60 | 1.47 | 15.24 | 43.7 | 0.219 | no | 0.0569 |
| 150 | 6.67 | 14.15 | 0.47 | 1.44 | 15.08 | 46.6 | 0.233 | no | 0.0606 |
| 200 | 5.00 | 12.13 | 0.40 | 1.42 | 15.00 | 48.1 | 0.240 | **yes** | 0.0625 |
| 300 | 3.33 | 10.11 | 0.33 | 1.41 | 14.92 | 49.5 | 0.248 | **yes** | 0.0644 |

**Closure threshold:** 200.0 W/kg (smallest swept specific power that closes inside 15 yr with positive delivered mass).

### Programmatic-risk overlay

Priors carried from Round A (R-power-bayesian-update). P(megawatt-class reactor on orbit by 2040) under each prior:

- Uniform Beta(1,7) posterior: 0.0013
- Jeffreys Beta(0.5,6.5) posterior: 0.0004
- Skeptical Beta(0.5,11.5) posterior: 0.0001

Expected-delivered-mass column in the sweep table above uses the uniform prior.
Multiply by (jeffreys / uniform) = 0.31× to get Jeffreys, by (skeptical / uniform) = 0.08× to get skeptical.

### Hypothesis grading

| Sub-claim | Predicted | Measured | Held? |
|---|---|---|---|
| H-mrsp-a — 60 W/kg closes (11-14 yr, 5-40 t) | closes (round-trip 11-14 yr, delivered 5-40 t) | round-trip 15.56 yr, delivered 37.9 t | **no** |
| H-mrsp-b — 80 W/kg closes (9-13 yr, 30-80 t) | closes (round-trip 9-13 yr, delivered 30-80 t) | round-trip 15.36 yr, delivered 41.6 t | **no** |
| H-mrsp-c — closure threshold W/kg | 40-60 (point 50) | 200.0 | **no** |
| H-mrsp-d — delivered fraction at 80 W/kg | 0.15-0.40 (point 0.25) | N/A | **no** |
| H-mrsp-e — programmatic-risk-adjusted delivered at 60 W/kg, uniform prior | 0.005-0.05 t (point 0.02) | 0.0493 t | yes |