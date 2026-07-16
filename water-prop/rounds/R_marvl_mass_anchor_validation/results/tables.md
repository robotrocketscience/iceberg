### Three MARVL parameterizations and their mass breakdowns at 1 megawatt-electric (no propellant)

| Parameterization | alpha_reactor (W/kg) | alpha_PC (W/kg) | alpha_radiator (kW_th/kg) | eta_conv | m_reactor (t) | m_PC (t) | m_radiator (t) | Total (t) | Reactor% | PC% | Radiator% |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| pessimistic | 19.4 | 28.6 | 0.0360 | 0.27 | 51.7 | 35.0 | 75.0 | 166.7 | 31.0% | 21.0% | 45.0% |
| rhea_baseline | 33.0 | 50.0 | 0.0470 | 0.30 | 30.3 | 20.0 | 49.6 | 104.9 | 28.9% | 19.1% | 47.3% |
| optimistic | 57.1 | 88.9 | 0.0739 | 0.32 | 17.5 | 11.2 | 28.7 | 62.5 | 28.0% | 18.0% | 46.0% |

### Variant C (Earth aerocapture, no Saturn-egress kick) closure under each parameterization

#### pessimistic

| Reactor (kWe) | Tug (t) | Inbound prop (t) | Delivered (t) | Fraction | t_inbound (yr) | Round-trip (yr) | Closes ±1 yr (16)? | Closes ±2 yr (17)? |
|---:|---:|---:|---:|---:|---:|---:|:--:|:--:|
| 500 | 95.2 | 188.2 | 11.8 | 0.059 | 3.53 | 16.70 | no | **yes** |
| 750 | INFEASIBLE: electric inbound burn requires 208.0 t but chunk has 200.0 t |
| 1000 | INFEASIBLE: electric inbound burn requires 233.7 t but chunk has 200.0 t |

#### rhea_baseline

| Reactor (kWe) | Tug (t) | Inbound prop (t) | Delivered (t) | Fraction | t_inbound (yr) | Round-trip (yr) | Closes ±1 yr (16)? | Closes ±2 yr (17)? |
|---:|---:|---:|---:|---:|---:|---:|:--:|:--:|
| 500 | 63.4 | 167.9 | 32.1 | 0.161 | 3.15 | 16.32 | no | **yes** |
| 750 | 89.2 | 184.3 | 15.7 | 0.078 | 2.30 | 15.48 | **yes** | **yes** |
| 1000 | INFEASIBLE: electric inbound burn requires 200.6 t but chunk has 200.0 t |

#### optimistic

| Reactor (kWe) | Tug (t) | Inbound prop (t) | Delivered (t) | Fraction | t_inbound (yr) | Round-trip (yr) | Closes ±1 yr (16)? | Closes ±2 yr (17)? |
|---:|---:|---:|---:|---:|---:|---:|:--:|:--:|
| 500 | 41.4 | 153.9 | 46.1 | 0.230 | 2.89 | 16.06 | no | **yes** |
| 750 | 56.3 | 163.4 | 36.6 | 0.183 | 2.04 | 15.21 | **yes** | **yes** |
| 1000 | 71.1 | 172.8 | 27.2 | 0.136 | 1.62 | 14.79 | **yes** | **yes** |

### Implied radiator areal density at 500 kilowatt-electric (surface conductance 700 W_th/m²)

Standard high-temperature deployable radiator areal density is ~3 kg/m². Sub-1 kg/m² is physically infeasible under known materials.

| Parameterization | Radiator mass (t) | Waste heat (kW_th) | Implied area (m²) | **Areal density (kg/m²)** | Inside ~3 kg/m² standard? |
|---|---:|---:|---:|---:|:--:|
| pessimistic | 37.50 | 1352 | 1931 | **19.42** | **yes** |
| rhea_baseline | 24.82 | 1167 | 1667 | **14.89** | **yes** |
| optimistic | 14.37 | 1062 | 1518 | **9.47** | **yes** |

### Hypothesis grading

| Sub-claim | Predicted | Measured | Held? |
|---|---|---|---|
| H-mmav-a — pessimistic 1 MWe stack | 130-160 t (point 145) | 166.7 t | **no** |
| H-mmav-b — optimistic 1 MWe stack | 70-95 t (point 80) | 62.5 t | **no** |
| H-mmav-c — pessimistic Variant C @ 500 kWe ±2 yr closes with 10-30 t | closes ±2 yr soft margin with delivered 10-30 t, round-trip 16.5-17.0 yr | round-trip 16.70 yr, delivered 11.8 t, closes_double_soft=True | yes |
| H-mmav-d — optimistic Variant C @ 500 kWe closes with 40-55 t | closes with delivered 40-55 t, round-trip 16.0-16.3 yr | round-trip 16.06 yr, delivered 46.1 t, closes_soft=False | yes |
| H-mmav-e — rhea-baseline areal density at 500 kWe | 2.5-3.5 kg/m² (point 3.0) | 14.89 | **no** |