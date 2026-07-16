# R-redundancy-budget-cost — results tables

## 1. Per-subsystem mass + cost overlay

| Subsystem | Kilopower-B form | MWe form | Mass +Δt KP-B | Mass +Δt MWe | Cost $M KP-B | Cost $M MWe |
|---|---|---|---|---|---|---|
| reactor_power | parallel: second 10-kWe Kilopower unit | internal: dual coolant loops + dual power conditioning + derated operation | 1.50 | 6.00 | 300 | 400 |
| primary_propulsion | spare thruster + power-processing unit | spare power-processing units; thruster redundancy structural | 0.05 | 0.30 | 50 | 30 |
| rcs | second RCS branch (block redundancy) | second RCS branch | 0.20 | 0.20 | 15 | 15 |
| gnc_compute | dual flight-computer + dual IMU + dual star-tracker | same | 0.50 | 0.50 | 40 | 40 |
| comms | dual HGA + redundant transponders | same | 0.80 | 0.80 | 60 | 60 |
| bag_harvest | dual-aperture trawl bag | dual-aperture at commercial-class scale | 1.00 | 2.00 | 50 | 80 |
| thermal_control | redundant coolant loops + redundant heat-pipes | same plus ammonia-loop redundancy | 0.50 | 1.50 | 30 | 60 |
| return_handoff | redundant valve trains + secondary docking adapter | same | 0.30 | 0.30 | 20 | 25 |

**Sum (no integration tax):** Kilopower-B = 4.85 t; megawatt = 11.60 t.
**Total overlay with 10 % integration tax:** Kilopower-B = **5.33 t**; megawatt = **12.76 t**.
**Total cost overlay:** Kilopower-B = **$565M**; megawatt = **$710M**.

## 2. Round-trip impact at L0-05 ceiling (15 yr)

Hohmann round-trip cruise = 12.17 yr (each way).

### Kilopower variant B (10 kWe, chunk-fed chemical inbound)

| Metric | Baseline | With redundancy overlay |
|---|---|---|
| Tug dry mass (tonne) | 16.00 | 21.34 |
| Outbound burn (yr) | 0.300 | 0.300 |
| Inbound burn (yr) | 6.435 | 6.731 |
| Round-trip (yr) | 19.907 | 20.203 |
| L0-05 margin (yr) | -4.907 | -5.203 |
| Clears L0-05? | NO | NO |

*Note: for Variant B, the outbound burn in this table is the all-electric calculation for cross-comparison; matrix-baseline outbound is chemical-kick which is fast and not modelled here. The relevant overlay impact for Variant B is inbound burn time + chemical-stage propellant overhead.*

### Megawatt all-electric (1 MWe decomposed-mid, all-electric inbound)

| Metric | Baseline | With redundancy overlay |
|---|---|---|
| Tug dry mass (tonne) | 29.00 | 41.76 |
| Outbound burn (yr) | 0.163 | 0.235 |
| Inbound burn (yr) | 0.600 | 0.633 |
| Round-trip (yr) | 13.935 | 14.040 |
| L0-05 margin (yr) | 1.065 | 0.960 |
| Clears L0-05? | yes | yes |

## 3. Post-redundancy mission-success projection

Single-string baseline (from R-mission-success-probability): **0.5621**
With per-subsystem R-lift from the table above (full redundancy on all 8): **0.9347**
Clears L0-10 ≥ 0.90? **yes**
