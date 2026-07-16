# R-bus-mass-anchor-sweep — headline tables

Total cells: **1920** (pure-electric inbound, single-stream Tsiolkovsky, no hydrolox).

Bus mass sweep: {2, 5, 10, 15} t. Bag mass: flat {0.5, 2, 5, 8} t OR linear (m_bag = 5% × chunk).

Cassini anchor: m_bus = 2 t. Europa Clipper anchor: m_bus ≈ 5.9 t. Full-bus prior anchor: m_bus = 15 t, m_bag = 8 t.

## All-pass-waiver count by (m_bus, m_bag) — FLAT bag, all other params marginalised

| m_bus \ m_bag | 0.5 | 2 | 5 | 8 |
|---|---|---|---|---|
| m_bus=2 | 30 | 29 | 27 | 25 |
| m_bus=5 | 28 | 27 | 25 | 25 |
| m_bus=10 | 25 | 25 | 24 | 21 |
| m_bus=15 | 24 | 22 | 20 | 17 |

## All-pass-waiver count at LINEAR bag (m_bag = 5% × chunk_t)

| m_bus | count |
|---|---|
| 2 | 29 |
| 5 | 26 |
| 10 | 25 |
| 15 | 19 |

## All-pass-waiver cells at Cassini anchor (m_bus=2 t, m_bag=5%×chunk), 29 cells

| P_kWe | chunk t | bag t | sp W/kg | aero km/s | Isp s | t_burn yr | RT yr | delivered t | LEO t | strict? | commercial? |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 500 | 200 | 10.0 | 10.0 | 10 | 2934 | 5.69 | 12.69 | 91.53 | 67.0 | True | True |
| 200 | 200 | 10.0 | 10.0 | 10 | 2000 | 7.62 | 14.62 | 74.91 | 34.0 | True | True |
| 500 | 200 | 10.0 | 5.0 | 10 | 2934 | 6.76 | 13.76 | 71.21 | 117.0 | True | True |
| 200 | 200 | 10.0 | 5.0 | 10 | 2000 | 8.28 | 15.28 | 64.22 | 54.0 | False | True |
| 500 | 200 | 10.0 | 10.0 | 10 | 2000 | 3.48 | 10.48 | 57.27 | 67.0 | True | True |
| 200 | 100 | 5.0 | 10.0 | 10 | 2934 | 6.87 | 13.87 | 47.59 | 29.0 | True | True |
| 500 | 200 | 10.0 | 10.0 | 0 | 2934 | 8.13 | 15.13 | 44.99 | 67.0 | False | True |
| 200 | 100 | 5.0 | 5.0 | 10 | 2934 | 7.94 | 14.94 | 39.47 | 49.0 | True | True |
| 500 | 100 | 5.0 | 10.0 | 10 | 2934 | 3.45 | 10.45 | 34.18 | 62.0 | True | True |
| 200 | 100 | 5.0 | 10.0 | 10 | 2000 | 4.20 | 11.20 | 31.04 | 29.0 | True | True |
| 500 | 200 | 10.0 | 5.0 | 10 | 2000 | 4.13 | 11.13 | 30.54 | 117.0 | True | True |
| 200 | 100 | 5.0 | 10.0 | 0 | 2934 | 9.82 | 16.82 | 25.11 | 29.0 | False | False |
| 200 | 100 | 5.0 | 5.0 | 10 | 2000 | 4.85 | 11.85 | 20.35 | 49.0 | True | False |
| 200 | 50 | 2.5 | 10.0 | 10 | 2934 | 4.08 | 11.08 | 18.92 | 26.5 | True | False |
| 50 | 50 | 2.5 | 10.0 | 10 | 2000 | 7.82 | 14.82 | 17.93 | 10.0 | True | False |
| 500 | 200 | 10.0 | 5.0 | 0 | 2934 | 9.66 | 16.66 | 15.96 | 117.0 | False | False |
| 50 | 50 | 2.5 | 5.0 | 10 | 2000 | 8.47 | 15.47 | 15.25 | 15.0 | False | False |
| 500 | 100 | 5.0 | 5.0 | 10 | 2934 | 4.52 | 11.52 | 13.87 | 112.0 | True | False |
| 500 | 100 | 5.0 | 10.0 | 10 | 2000 | 2.11 | 9.11 | 13.40 | 62.0 | True | False |
| 200 | 50 | 2.5 | 5.0 | 10 | 2934 | 5.14 | 12.14 | 10.80 | 46.5 | True | False |
| 200 | 50 | 2.5 | 10.0 | 10 | 2000 | 2.49 | 9.49 | 9.11 | 26.5 | True | False |
| 500 | 200 | 10.0 | 10.0 | 0 | 2000 | 4.69 | 11.69 | 7.63 | 67.0 | True | False |
| 200 | 100 | 5.0 | 10.0 | 0 | 2000 | 5.66 | 12.66 | 7.06 | 29.0 | True | False |
| 500 | 100 | 5.0 | 10.0 | 0 | 2934 | 4.93 | 11.93 | 5.95 | 62.0 | True | False |
| 200 | 50 | 2.5 | 10.0 | 0 | 2934 | 5.83 | 12.83 | 5.59 | 26.5 | True | False |
| 500 | 50 | 2.5 | 10.0 | 10 | 2934 | 2.33 | 9.33 | 5.51 | 59.5 | True | False |
| 50 | 10 | 0.5 | 10.0 | 10 | 2934 | 3.84 | 10.84 | 2.69 | 8.0 | True | False |
| 50 | 10 | 0.5 | 5.0 | 10 | 2934 | 4.90 | 11.90 | 0.66 | 13.0 | True | False |
| 50 | 10 | 0.5 | 10.0 | 10 | 2000 | 2.35 | 9.35 | 0.38 | 8.0 | True | False |

## **Cassini-anchor cells that pass L0-05 strict AND L0-09 commercial floor (delivered ≥ 30 t)**: 9

| P_kWe | chunk t | sp | aero | Isp | RT yr | delivered t |
|---|---|---|---|---|---|---|
| 500 | 200 | 10.0 | 10 | 2934 | 12.69 | 91.53 |
| 200 | 200 | 10.0 | 10 | 2000 | 14.62 | 74.91 |
| 500 | 200 | 5.0 | 10 | 2934 | 13.76 | 71.21 |
| 500 | 200 | 10.0 | 10 | 2000 | 10.48 | 57.27 |
| 200 | 100 | 10.0 | 10 | 2934 | 13.87 | 47.59 |
| 200 | 100 | 5.0 | 10 | 2934 | 14.94 | 39.47 |
| 500 | 100 | 10.0 | 10 | 2934 | 10.45 | 34.18 |
| 200 | 100 | 10.0 | 10 | 2000 | 11.20 | 31.04 |
| 500 | 200 | 5.0 | 10 | 2000 | 11.13 | 30.54 |

## Hypothesis grades

| # | predicted | measured | verdict |
|---|---|---|---|
| H1 | Cassini-anchor opens 500-kWe/200-t Arch-E cell at sp=10, aero=10, Isp=2000 | 1 of 1 cells all-pass | HELD |
| H2 | Cassini-anchor opens >= 3x more all-pass-waiver cells than full-bus | Cassini=29 all-pass-waiver, full-bus=17 all-pass-waiver, ratio=1.71 | FALSIFIED |
| H3 | at sp=5 W/kg + Cassini bus, no commercial cell (chunk>=100, delivered>=30 t) closes L0-05 strict | 1 cells satisfy commercial + L0-05 strict | FALSIFIED |
| H4 | chunk-scaled bag is more permissive at small chunks (10 t), less at large (200 t) | chunk=10: linear=4 flat-8=0; chunk=200: linear=34 flat-8=35 | HELD |
| H5 | matrix R6 Arch-E falsified verdict (23.6 yr) reverses at Cassini bus | Arch-E-R6 at Cassini-bus (m_bus=2): 1 pass waiver; at full-bus (m_bus=15): 1 pass waiver | FALSIFIED |
