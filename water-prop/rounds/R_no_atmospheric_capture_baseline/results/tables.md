# R-no-atmospheric-capture-baseline — results

## Closure summary across full sweep

- Total cells swept: 288
- Cells closing L0-05 strict 15 yr (round-trip ≤ 15 yr AND delivered > 0): **0**
- Cells closing L0-05 soft-margin 17 yr: **0**

**No strict-closing cells in the full sweep. The matrix's surviving cell, with aerocapture removed, is EMPTY.**

## Round F equivalent anchor (aphelion 11, 500 kWe, 200 t chunk, chemical Saturn-egress + electric Earth-arrival, no LGA)

| Quantity | Electric Earth-arrival | Chemical Earth-arrival |
|---|---:|---:|
| Δv arrival (km/s) | 21.62 | 7.62 |
| Arrival propellant (t) | 530 | 1218 |
| Mass at inbound burn start (t) | 793 | 1482 |
| Saturn-departure mass (t) | 1568 | 2928 |
| Outbound kick prop (t) | 15528 | 29006 |
| LEO mission-1 launch mass (t) | 17096 | 31934 |
| Inbound electric burn (yr) | 13.37 | 6.41 |
| Round-trip time (yr) | 22.73 | 15.77 |
| Delivered mass (t) | 17.06 | 0.00 |
| Closes strict 15 yr | False | False |
| Closes soft 17 yr | False | False |

## Hypothesis grading

| Sub-claim | Central | Range | Computed | Held |
|---|---:|---|---:|:---:|
| H_nacb_a | 1219.0 | [1000.0, 1500.0] | 1218.269 | True |
| H_nacb_b | 2025.0 | [1700.0, 2400.0] | 2928.090 | False |
| H_nacb_c | 9.9 | [7.0, 13.0] | 6.830 | False |
| H_nacb_d | 3.5 | [3.0, 4.2] | 3.011 | True |
| H_nacb_e | 57.0 | [45.0, 80.0] | 66.433 | True |
| H_nacb_f | 0 | [0, 2] | 0.000 | True |
| H_nacb_g | 0 | [0, 4] | 0.000 | True |

**Aggregate: 5/6 sub-claims held. H-nacb-agg held: True.**