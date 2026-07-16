# R-dv-anchor-audit — corrected Pareto envelope

Re-run of R-chemical-electric-leapfrog with two delta-velocity anchor corrections plus one new scenario.

Saturn departure: **7.7 km/s** (was 5.5 km/s in prior round; vis-viva from B-ring elliptical parking orbit).
Earth chemical capture (direct, no lunar GA): **7.3 km/s** (was 3.5 km/s; vis-viva from Hohmann v_inf 10.3 km/s).
Earth chemical capture after lunar gravity assist (R12 10-flyby tour): **4.2 km/s** (new scenario).
Lunar gravity assist phasing: **0.72 years** (8.7 months, R12 anchor).

## Scenario: aerocapture

| P (kWe) | T_tank (t) | m_dry (t) | prop_dep (t) | prop_cap (t) | spiral (yr) | RT (yr) | delivered (t) | strict? | floor? | commercial-strict? |
|---|---|---|---|---|---|---|---|---|---|---|
| 10 | 0.1 | 21.8 | 183.1 | 0.0 | 10.36 | 23.4 | 16.4 | no | no | no |
| 10 | 1.0 | 22.1 | 183.3 | 0.0 | 10.32 | 23.3 | 16.1 | no | no | no |
| 10 | 10.0 | 24.8 | 185.5 | 0.0 | 9.94 | 22.9 | 13.9 | no | no | no |
| 10 | 50.0 | 36.8 | 195.4 | 0.0 | 8.23 | 21.2 | 4.0 | no | no | no |
| 10 | 150.0 | 66.8 | 220.2 | 0.0 | 5.47 | 18.5 | 0.0 | no | no | no |
| 15 | 0.1 | 23.9 | 184.8 | 0.0 | 6.97 | 20.0 | 14.6 | no | no | no |
| 15 | 1.0 | 24.2 | 185.0 | 0.0 | 6.95 | 19.9 | 14.4 | no | no | no |
| 15 | 10.0 | 26.9 | 187.3 | 0.0 | 6.69 | 19.7 | 12.1 | no | no | no |
| 15 | 50.0 | 38.9 | 197.2 | 0.0 | 5.55 | 18.6 | 2.2 | no | no | no |
| 15 | 150.0 | 68.9 | 221.9 | 0.0 | 2.71 | 15.7 | 0.0 | no | no | no |
| 20 | 0.1 | 26.1 | 186.6 | 0.0 | 5.28 | 18.3 | 12.8 | no | no | no |
| 20 | 1.0 | 26.3 | 186.8 | 0.0 | 5.26 | 18.3 | 12.6 | no | no | no |
| 20 | 10.0 | 29.0 | 189.0 | 0.0 | 5.07 | 18.1 | 10.4 | no | no | no |
| 20 | 50.0 | 41.0 | 198.9 | 0.0 | 4.22 | 17.2 | 0.4 | no | no | no |
| 20 | 150.0 | 71.0 | 223.7 | 0.0 | 2.09 | 15.1 | 0.0 | no | no | no |
| 30 | 0.1 | 30.3 | 190.1 | 0.0 | 3.59 | 16.6 | 9.3 | no | no | no |
| 30 | 1.0 | 30.6 | 190.3 | 0.0 | 3.57 | 16.6 | 9.1 | no | no | no |
| 30 | 10.0 | 33.3 | 192.5 | 0.0 | 3.45 | 16.4 | 6.8 | no | no | no |
| 30 | 50.0 | 45.3 | 202.5 | 0.0 | 2.88 | 15.9 | 0.0 | no | no | no |
| 30 | 150.0 | 75.3 | 227.2 | 0.0 | 1.46 | 14.5 | 0.0 | YES | no | no |
| 50 | 0.1 | 38.9 | 197.1 | 0.0 | 2.23 | 15.2 | 2.2 | no | no | no |
| 50 | 1.0 | 39.1 | 197.4 | 0.0 | 2.22 | 15.2 | 2.0 | no | no | no |
| 50 | 10.0 | 41.8 | 199.6 | 0.0 | 2.15 | 15.1 | 0.0 | no | no | no |
| 50 | 50.0 | 53.8 | 209.5 | 0.0 | 1.81 | 14.8 | 0.0 | YES | no | no |
| 50 | 150.0 | 83.8 | 234.3 | 0.0 | 0.95 | 14.0 | 0.0 | YES | no | no |
| 100 | 0.1 | 60.2 | 214.7 | 0.0 | 1.22 | 14.2 | 0.0 | YES | no | no |
| 100 | 1.0 | 60.5 | 215.0 | 0.0 | 1.21 | 14.2 | 0.0 | YES | no | no |
| 100 | 10.0 | 63.2 | 217.2 | 0.0 | 1.17 | 14.2 | 0.0 | YES | no | no |
| 100 | 50.0 | 75.2 | 227.1 | 0.0 | 1.00 | 14.0 | 0.0 | YES | no | no |
| 100 | 150.0 | 105.2 | 251.9 | 0.0 | 0.58 | 13.6 | 0.0 | YES | no | no |

## Scenario: chemical_direct

| P (kWe) | T_tank (t) | m_dry (t) | prop_dep (t) | prop_cap (t) | spiral (yr) | RT (yr) | delivered (t) | strict? | floor? | commercial-strict? |
|---|---|---|---|---|---|---|---|---|---|---|
| 10 | 0.1 | 21.8 | 183.1 | 30.9 | 10.36 | 23.4 | 0.0 | no | no | no |
| 10 | 1.0 | 22.1 | 183.3 | 30.9 | 10.32 | 23.3 | 0.0 | no | no | no |
| 10 | 10.0 | 24.8 | 185.5 | 31.3 | 9.94 | 22.9 | 0.0 | no | no | no |
| 10 | 50.0 | 36.8 | 195.4 | 32.9 | 8.23 | 21.2 | 0.0 | no | no | no |
| 10 | 150.0 | 66.8 | 220.2 | 37.1 | 5.47 | 18.5 | 0.0 | no | no | no |
| 15 | 0.1 | 23.9 | 184.8 | 31.2 | 6.97 | 20.0 | 0.0 | no | no | no |
| 15 | 1.0 | 24.2 | 185.0 | 31.2 | 6.95 | 19.9 | 0.0 | no | no | no |
| 15 | 10.0 | 26.9 | 187.3 | 31.6 | 6.69 | 19.7 | 0.0 | no | no | no |
| 15 | 50.0 | 38.9 | 197.2 | 33.2 | 5.55 | 18.6 | 0.0 | no | no | no |
| 15 | 150.0 | 68.9 | 221.9 | 37.4 | 2.71 | 15.7 | 0.0 | no | no | no |
| 20 | 0.1 | 26.1 | 186.6 | 31.5 | 5.28 | 18.3 | 0.0 | no | no | no |
| 20 | 1.0 | 26.3 | 186.8 | 31.5 | 5.26 | 18.3 | 0.0 | no | no | no |
| 20 | 10.0 | 29.0 | 189.0 | 31.9 | 5.07 | 18.1 | 0.0 | no | no | no |
| 20 | 50.0 | 41.0 | 198.9 | 33.5 | 4.22 | 17.2 | 0.0 | no | no | no |
| 20 | 150.0 | 71.0 | 223.7 | 37.7 | 2.09 | 15.1 | 0.0 | no | no | no |
| 30 | 0.1 | 30.3 | 190.1 | 32.0 | 3.59 | 16.6 | 0.0 | no | no | no |
| 30 | 1.0 | 30.6 | 190.3 | 32.1 | 3.57 | 16.6 | 0.0 | no | no | no |
| 30 | 10.0 | 33.3 | 192.5 | 32.5 | 3.45 | 16.4 | 0.0 | no | no | no |
| 30 | 50.0 | 45.3 | 202.5 | 34.1 | 2.88 | 15.9 | 0.0 | no | no | no |
| 30 | 150.0 | 75.3 | 227.2 | 38.3 | 1.46 | 14.5 | 0.0 | YES | no | no |
| 50 | 0.1 | 38.9 | 197.1 | 33.2 | 2.23 | 15.2 | 0.0 | no | no | no |
| 50 | 1.0 | 39.1 | 197.4 | 33.3 | 2.22 | 15.2 | 0.0 | no | no | no |
| 50 | 10.0 | 41.8 | 199.6 | 33.6 | 2.15 | 15.1 | 0.0 | no | no | no |
| 50 | 50.0 | 53.8 | 209.5 | 35.3 | 1.81 | 14.8 | 0.0 | YES | no | no |
| 50 | 150.0 | 83.8 | 234.3 | 39.5 | 0.95 | 14.0 | 0.0 | YES | no | no |
| 100 | 0.1 | 60.2 | 214.7 | 36.2 | 1.22 | 14.2 | 0.0 | YES | no | no |
| 100 | 1.0 | 60.5 | 215.0 | 36.2 | 1.21 | 14.2 | 0.0 | YES | no | no |
| 100 | 10.0 | 63.2 | 217.2 | 36.6 | 1.17 | 14.2 | 0.0 | YES | no | no |
| 100 | 50.0 | 75.2 | 227.1 | 38.3 | 1.00 | 14.0 | 0.0 | YES | no | no |
| 100 | 150.0 | 105.2 | 251.9 | 42.5 | 0.58 | 13.6 | 0.0 | YES | no | no |

## Scenario: lunar_ga_chemical

| P (kWe) | T_tank (t) | m_dry (t) | prop_dep (t) | prop_cap (t) | spiral (yr) | RT (yr) | delivered (t) | strict? | floor? | commercial-strict? |
|---|---|---|---|---|---|---|---|---|---|---|
| 10 | 0.1 | 21.8 | 183.1 | 23.4 | 10.36 | 24.1 | 0.0 | no | no | no |
| 10 | 1.0 | 22.1 | 183.3 | 23.5 | 10.32 | 24.0 | 0.0 | no | no | no |
| 10 | 10.0 | 24.8 | 185.5 | 23.7 | 9.94 | 23.7 | 0.0 | no | no | no |
| 10 | 50.0 | 36.8 | 195.4 | 25.0 | 8.23 | 22.0 | 0.0 | no | no | no |
| 10 | 150.0 | 66.8 | 220.2 | 28.2 | 5.47 | 19.2 | 0.0 | no | no | no |
| 15 | 0.1 | 23.9 | 184.8 | 23.6 | 6.97 | 20.7 | 0.0 | no | no | no |
| 15 | 1.0 | 24.2 | 185.0 | 23.7 | 6.95 | 20.7 | 0.0 | no | no | no |
| 15 | 10.0 | 26.9 | 187.3 | 24.0 | 6.69 | 20.4 | 0.0 | no | no | no |
| 15 | 50.0 | 38.9 | 197.2 | 25.2 | 5.55 | 19.3 | 0.0 | no | no | no |
| 15 | 150.0 | 68.9 | 221.9 | 28.4 | 2.71 | 16.4 | 0.0 | no | no | no |
| 20 | 0.1 | 26.1 | 186.6 | 23.9 | 5.28 | 19.0 | 0.0 | no | no | no |
| 20 | 1.0 | 26.3 | 186.8 | 23.9 | 5.26 | 19.0 | 0.0 | no | no | no |
| 20 | 10.0 | 29.0 | 189.0 | 24.2 | 5.07 | 18.8 | 0.0 | no | no | no |
| 20 | 50.0 | 41.0 | 198.9 | 25.5 | 4.22 | 17.9 | 0.0 | no | no | no |
| 20 | 150.0 | 71.0 | 223.7 | 28.6 | 2.09 | 15.8 | 0.0 | no | no | no |
| 30 | 0.1 | 30.3 | 190.1 | 24.3 | 3.59 | 17.3 | 0.0 | no | no | no |
| 30 | 1.0 | 30.6 | 190.3 | 24.4 | 3.57 | 17.3 | 0.0 | no | no | no |
| 30 | 10.0 | 33.3 | 192.5 | 24.6 | 3.45 | 17.2 | 0.0 | no | no | no |
| 30 | 50.0 | 45.3 | 202.5 | 25.9 | 2.88 | 16.6 | 0.0 | no | no | no |
| 30 | 150.0 | 75.3 | 227.2 | 29.1 | 1.46 | 15.2 | 0.0 | no | no | no |
| 50 | 0.1 | 38.9 | 197.1 | 25.2 | 2.23 | 16.0 | 0.0 | no | no | no |
| 50 | 1.0 | 39.1 | 197.4 | 25.3 | 2.22 | 15.9 | 0.0 | no | no | no |
| 50 | 10.0 | 41.8 | 199.6 | 25.5 | 2.15 | 15.9 | 0.0 | no | no | no |
| 50 | 50.0 | 53.8 | 209.5 | 26.8 | 1.81 | 15.5 | 0.0 | no | no | no |
| 50 | 150.0 | 83.8 | 234.3 | 30.0 | 0.95 | 14.7 | 0.0 | YES | no | no |
| 100 | 0.1 | 60.2 | 214.7 | 27.5 | 1.22 | 14.9 | 0.0 | YES | no | no |
| 100 | 1.0 | 60.5 | 215.0 | 27.5 | 1.21 | 14.9 | 0.0 | YES | no | no |
| 100 | 10.0 | 63.2 | 217.2 | 27.8 | 1.17 | 14.9 | 0.0 | YES | no | no |
| 100 | 50.0 | 75.2 | 227.1 | 29.1 | 1.00 | 14.7 | 0.0 | YES | no | no |
| 100 | 150.0 | 105.2 | 251.9 | 32.2 | 0.58 | 14.3 | 0.0 | YES | no | no |

## Hypothesis grades

| H | Predicted | Measured | Verdict |
|---|---|---|---|
| H-anchor-1 | max delivered at flyable+aerocapture under corrected anchors < 30 t | 16.4 t | HELD |
| H-anchor-2 | chemical_direct at flyable power delivered ≤ 0 t (vehicle can't close mass) | max delivered = 0.0 t | HELD |
| H-anchor-3 | lunar_ga + chemical at flyable power max delivered ≤ 5 t | 0.0 t | HELD |
| H-anchor-4 | 0 cells close L0-09 commercial floor at flyable power under corrected anchors | 0 cells close floor at flyable power | HELD |

## Minimum reactor power to close L0-09 commercial floor per scenario (bisection)

| Scenario | min reactor power (kWe) | Notes |
|---|---|---|
| aerocapture | not achievable up to 500 kWe | architecture is empty even at FSP-class |
| chemical_direct | not achievable up to 500 kWe | architecture is empty even at FSP-class |
| lunar_ga_chemical | not achievable up to 500 kWe | architecture is empty even at FSP-class |
