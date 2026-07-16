### Sanity check vs hyperion R-variant-B-impulsive-vs-continuous (Variant A, chunk 200 t, 500 kWe)

- Hyperion published: round-trip 16.92 yr, delivered 0.00 t.
- Reproduced (phoebe): feasible=True, round-trip 16.92215308710872 yr, delivered 0.014750671062614629 t, m_prop_inbound 199.98524932893739 t.

### Inbound delta-velocity (Variant A, high_elliptical_1Mkm, with Lunar Gravity Assist credit)

- Saturn spiral: 6.159 km/s
- Heliocentric retrograde: 5.439 km/s
- Earth heliocentric: 10.298 km/s
- LEO spiral: 7.669 km/s
- LGA credit: -2.0 km/s
- **Total electric inbound DV: 27.565 km/s**

### Sweep 1 — chunk sweep at 500 kWe Variant A (electric inbound 27.57 km/s, MARVL mass, Isp 2000 s)

| Chunk (t) | Feasible? | Tug (t) | m_prop_inbound (t) | Delivered (t) | Fraction | t_burn (yr) | Round-trip (yr) | Strict 15? | Soft 16? | Expected (uniform, t) |
|---:|:--:|---:|---:|---:|---:|---:|---:|:--:|:--:|---:|
| 50 | **no** | 55.0 | 79.2 (required) | -29.2 (deficit) | — | — | ∞ | no | no | 0 |
| 75 | **no** | 55.0 | 98.1 (required) | -23.1 (deficit) | — | — | ∞ | no | no | 0 |
| 100 | **no** | 55.0 | 117.0 (required) | -17.0 (deficit) | — | — | ∞ | no | no | 0 |
| 125 | **no** | 55.0 | 135.8 (required) | -10.8 (deficit) | — | — | ∞ | no | no | 0 |
| 150 | **no** | 55.0 | 154.7 (required) | -4.7 (deficit) | — | — | ∞ | no | no | 0 |
| 175 | **no** | 63.7 | 180.1 (required) | -5.1 (deficit) | — | — | ∞ | no | no | 0 |
| 200 | yes | 65.0 | 200.0 | 0.0 | 0.000 | 3.75 | 16.92 | no | no | 0.0000 |

### Sweep 2 — reactor sweep at chunk 100 t Variant A

| Reactor (kWe) | Feasible? | Tug (t) | m_prop_inbound (t) | Delivered (t) | Fraction | t_burn (yr) | Round-trip (yr) | Strict 15? | Soft 16? | Expected (uniform, t) |
|---:|:--:|---:|---:|---:|---:|---:|---:|:--:|:--:|---:|
| 100 | yes | 19.5 | 90.2 | 9.8 | 0.098 | 8.46 | 21.63 | no | no | 0.0127 |
| 200 | yes | 29.9 | 98.0 | 2.0 | 0.020 | 4.60 | 17.77 | no | no | 0.0026 |
| 300 | **no** | 35.0 | 101.9 (required) | -1.9 (deficit) | — | — | ∞ | no | no | 0 |
| 400 | **no** | 45.0 | 109.4 (required) | -9.4 (deficit) | — | — | ∞ | no | no | 0 |
| 500 | **no** | 55.0 | 117.0 (required) | -17.0 (deficit) | — | — | ∞ | no | no | 0 |
| 600 | **no** | 65.0 | 124.5 (required) | -24.5 (deficit) | — | — | ∞ | no | no | 0 |
| 700 | **no** | 75.0 | 132.1 (required) | -32.1 (deficit) | — | — | ∞ | no | no | 0 |

### Closure boundary summary

- Chunk sweep at 500 kWe: chunks that close strict 15-yr AND feasible: **none**
- Chunk sweep at 500 kWe: chunks that close soft 16-yr AND feasible: **none**
- Reactor sweep at chunk 100 t: reactor powers that close strict 15-yr AND feasible: **none**
- Reactor sweep at chunk 100 t: reactor powers that close soft 16-yr AND feasible: **none**

### Operating optimum at chunk 100 t Variant A

- **No closing cell exists in the reactor sweep [100, 700] kWe at chunk 100 t.**

### Hypothesis grading

| Sub-claim | Predicted | Measured | Held? |
|---|---|---|---|
| H-100-a_chunk100_500kWe_infeasible | propellant-infeasible (m_prop > chunk) | actual_feasible=False; actual_m_prop_t=116.96475890878853; actual_delivered_t=-16.964758908788525 | **yes** |
| H-100-b_strict_no_closing_chunk_at_500kWe | no chunk in [50, 200] t at 500 kWe Variant A closes strict 15-yr AND is feasible | closing_strict_chunks=[] | **yes** |
| H-100-b_soft_no_closing_chunk_at_500kWe | no chunk in [50, 200] t at 500 kWe Variant A closes soft 16-yr AND is feasible | closing_soft_chunks=[] | **yes** |
| H-100-c_no_closing_reactor_at_chunk100 | no reactor power in [100, 700] kWe at chunk=100 t Variant A is feasible AND closes soft 16-yr | closing_soft_reactors=[]; closing_strict_reactors=[] | **yes** |
| H-100-d_optimum_reactor_in_200_400_band | [200.0, 400.0] | n/a (no closing cell) | not gradable |
| H-100-e_path3_delivered_under_321t | best path-3 closing delivered mass < 32.1 t (hyperion Variant C, path 1) | n/a (no closing cell) | not gradable |