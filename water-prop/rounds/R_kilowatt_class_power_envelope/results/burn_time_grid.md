# Sub-procedure — kilowatt-class power-envelope burn-time grid

Vehicle: bus = 5.5 t (Europa-Clipper-with-medium-shielding basis-of-record from R-bus-mass-anchor-adjudication); bag = 5% of chunk (linear, floor 0.5 t); reactor mass = P_kWe × 1000 / specific power; thrusters = 10 kg/kWe.
Δv inbound: 25 km/s continuous-thrust (campaign anchor).
L0-05 strict inbound-burn budget: ≤ 8 yr (15 yr total − 7 yr outbound + Saturn-side).
L0-05 waiver inbound-burn budget: ≤ 18 yr.
L0-09 commercial floor: ≥ 30 t delivered.

## Burn-time grid (years)

| P (kWe) | chunk (t) | Isp (s) | sp (W/kg) | m_reactor (t) | m_w (t) | delivered (t) | t_burn (yr) | × strict budget | strict? | waiver? |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 30 | 2000 | 2.4 | 0.42 | 27.0 | 3.0 | 328.7 | 41.1× | no | no |
| 1 | 30 | 2000 | 5.3 | 0.19 | 26.8 | 3.2 | 326.7 | 40.8× | no | no |
| 1 | 30 | 5000 | 2.4 | 0.42 | 14.9 | 15.1 | 1138.9 | 142.4× | no | no |
| 1 | 30 | 5000 | 5.3 | 0.19 | 14.9 | 15.1 | 1132.0 | 141.5× | no | no |
| 1 | 100 | 2000 | 2.4 | 0.42 | 79.9 | 20.1 | 974.2 | 121.8× | no | no |
| 1 | 100 | 2000 | 5.3 | 0.19 | 79.8 | 20.2 | 972.2 | 121.5× | no | no |
| 1 | 100 | 5000 | 2.4 | 0.42 | 44.3 | 55.7 | 3375.5 | 421.9× | no | no |
| 1 | 100 | 5000 | 5.3 | 0.19 | 44.2 | 55.8 | 3368.6 | 421.1× | no | no |
| 1 | 200 | 2000 | 2.4 | 0.42 | 155.6 | 44.4 | 1896.4 | 237.0× | no | no |
| 1 | 200 | 2000 | 5.3 | 0.19 | 155.4 | 44.6 | 1894.4 | 236.8× | no | no |
| 1 | 200 | 5000 | 2.4 | 0.42 | 86.2 | 113.8 | 6570.7 | 821.3× | no | no |
| 1 | 200 | 5000 | 5.3 | 0.19 | 86.2 | 113.8 | 6563.8 | 820.5× | no | no |
| 5 | 30 | 2000 | 2.4 | 2.08 | 28.2 | 1.8 | 68.7 | 8.6× | no | no |
| 5 | 30 | 2000 | 5.3 | 0.94 | 27.4 | 2.6 | 66.7 | 8.3× | no | no |
| 5 | 30 | 5000 | 2.4 | 2.08 | 15.6 | 14.4 | 238.2 | 29.8× | no | no |
| 5 | 30 | 5000 | 5.3 | 0.94 | 15.2 | 14.8 | 231.2 | 28.9× | no | no |
| 5 | 100 | 2000 | 2.4 | 2.08 | 81.1 | 18.9 | 197.8 | 24.7× | no | no |
| 5 | 100 | 2000 | 5.3 | 0.94 | 80.3 | 19.7 | 195.8 | 24.5× | no | no |
| 5 | 100 | 5000 | 2.4 | 2.08 | 45.0 | 55.0 | 685.5 | 85.7× | no | no |
| 5 | 100 | 5000 | 5.3 | 0.94 | 44.5 | 55.5 | 678.6 | 84.8× | no | no |
| 5 | 200 | 2000 | 2.4 | 2.08 | 156.8 | 43.2 | 382.3 | 47.8× | no | no |
| 5 | 200 | 2000 | 5.3 | 0.94 | 156.0 | 44.0 | 380.3 | 47.5× | no | no |
| 5 | 200 | 5000 | 2.4 | 2.08 | 86.9 | 113.1 | 1324.5 | 165.6× | no | no |
| 5 | 200 | 5000 | 5.3 | 0.94 | 86.5 | 113.5 | 1317.6 | 164.7× | no | no |
| 10 | 30 | 2000 | 2.4 | 4.17 | 29.7 | 0.3 | 36.2 | 4.5× | no | no |
| 10 | 30 | 2000 | 5.3 | 1.89 | 28.1 | 1.9 | 34.2 | 4.3× | no | no |
| 10 | 30 | 5000 | 2.4 | 4.17 | 16.5 | 13.5 | 125.6 | 15.7× | no | no |
| 10 | 30 | 5000 | 5.3 | 1.89 | 15.6 | 14.4 | 118.6 | 14.8× | no | no |
| 10 | 100 | 2000 | 2.4 | 4.17 | 82.7 | 17.3 | 100.8 | 12.6× | no | no |
| 10 | 100 | 2000 | 5.3 | 1.89 | 81.0 | 19.0 | 98.8 | 12.3× | no | no |
| 10 | 100 | 5000 | 2.4 | 4.17 | 45.8 | 54.2 | 349.2 | 43.7× | no | no |
| 10 | 100 | 5000 | 5.3 | 1.89 | 44.9 | 55.1 | 342.3 | 42.8× | no | no |
| 10 | 200 | 2000 | 2.4 | 4.17 | 158.3 | 41.7 | 193.0 | 24.1× | no | no |
| 10 | 200 | 2000 | 5.3 | 1.89 | 156.7 | 43.3 | 191.0 | 23.9× | no | no |
| 10 | 200 | 5000 | 2.4 | 4.17 | 87.8 | 112.2 | 668.8 | 83.6× | no | no |
| 10 | 200 | 5000 | 5.3 | 1.89 | 86.9 | 113.1 | 661.8 | 82.7× | no | no |

## Closing-chunk search per (P, Isp, sp)

What chunk mass would close L0-05 strict (8 yr inbound burn)? Bisection.

| P (kWe) | Isp (s) | sp (W/kg) | closing chunk (t) | meets L0-09 floor 30 t? |
|---|---|---|---|---|
| 1 | 2000 | 2.4 | no chunk closes | NO |
| 1 | 2000 | 5.3 | no chunk closes | NO |
| 1 | 5000 | 2.4 | no chunk closes | NO |
| 1 | 5000 | 5.3 | no chunk closes | NO |
| 5 | 2000 | 2.4 | no chunk closes | NO |
| 5 | 2000 | 5.3 | no chunk closes | NO |
| 5 | 5000 | 2.4 | no chunk closes | NO |
| 5 | 5000 | 5.3 | no chunk closes | NO |
| 10 | 2000 | 2.4 | no chunk closes | NO |
| 10 | 2000 | 5.3 | 1.12 | NO |
| 10 | 5000 | 2.4 | no chunk closes | NO |
| 10 | 5000 | 5.3 | no chunk closes | NO |

## Hypothesis grades

| H | predicted | measured | verdict |
|---|---|---|---|
| H-kw-1 | burn time at 10 kWe / Isp 2000 / chunk 200 / sp 2.4 ∈ [150, 250] yr | 193.0 yr | HELD |
| H-kw-2 | Isp 5000 burn time > Isp 2000 burn time at same (P, chunk, sp) | Isp 5000 = 669 yr vs Isp 2000 = 193 yr | HELD |
| H-kw-3 | no chunk ≥ 30 t closes L0-05 strict at 10 kWe / Isp 2000 | no chunk closes at any size | HELD |
| H-kw-5 | 0 of 36 cells close L0-05 strict AND L0-09 commercial | 0 of 36 close strict; 0 close waiver | HELD |

**Aggregate.** 0 of 36 cells close L0-05 strict; 0 of 36 close L0-05 waiver. ICEBERG inbound-delivery architecture at the actually-flyable power envelope is empty.
