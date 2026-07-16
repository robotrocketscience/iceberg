# R-mission-success-probability — results tables

## Heritage empirical rates

- Total missions in dataset: 23
- L0-10 definition (delivered >= 0.5 x design) across all: **0.739** (17/23)
- Strict definition (>= 0.9 x design) across all: **0.652**
- L0-10 definition, long-design (>= 10 yr) subset: **1.000** (7 missions)
- L0-10 definition, outer-planet subset: **1.000** (8 missions)
- Spacecraft survival to operations: **0.826**

## Required per-subsystem R to clear target mission success

Rows = mission-success target. Columns = number of critical-path subsystems N in series.
Required R = target^(1/N).

| Target \ N | 4 | 6 | 8 | 10 | 12 |
|---|---|---|---|---|---|
| 0.70 | 0.9147 | 0.9423 | 0.9564 | 0.9650 | 0.9707 |
| 0.75 | 0.9306 | 0.9532 | 0.9647 | 0.9716 | 0.9763 |
| 0.80 | 0.9457 | 0.9635 | 0.9725 | 0.9779 | 0.9816 |
| 0.85 | 0.9602 | 0.9733 | 0.9799 | 0.9839 | 0.9865 |
| 0.90 | 0.9740 | 0.9826 | 0.9869 | 0.9895 | 0.9913 |
| 0.95 | 0.9873 | 0.9915 | 0.9936 | 0.9949 | 0.9957 |

## Projected mission success at heritage per-subsystem R

Rows = per-subsystem R. Columns = N. Projected mission success = R^N.

| R \ N | 4 | 6 | 8 | 10 | 12 |
|---|---|---|---|---|---|
| 0.93 | 0.7481 | 0.6470 | 0.5596 | 0.4840 | 0.4186 |
| 0.95 | 0.8145 | 0.7351 | 0.6634 | 0.5987 | 0.5404 |
| 0.97 | 0.8853 | 0.8330 | 0.7837 | 0.7374 | 0.6938 |
| 0.99 | 0.9606 | 0.9415 | 0.9227 | 0.9044 | 0.8864 |

## ICEBERG single-string projection (8 critical-path subsystems)

Serial product of paper-estimate per-subsystem R: **0.5621**

| Subsystem | R_single | Heritage |
|---|---|---|
| reactor_power | 0.950 | NONE |
| primary_propulsion | 0.900 | ADJACENT |
| rcs | 0.970 | AVAILABLE |
| gnc_compute | 0.950 | AVAILABLE |
| comms | 0.930 | AVAILABLE |
| bag_harvest | 0.850 | NONE |
| thermal_control | 0.950 | ADJACENT |
| return_handoff | 0.950 | AVAILABLE |

## Redundancy budget to clear targets

Apply 2-of-3 parallel redundancy to the weakest single-string subsystem; repeat until target is cleared.
(Parallel redundancy lifts subsystem R from R to 1 - (1-R)^2.)

### Target = 0.90 (L0-10 as written)

| Step | Redundancy applied to | Projected mission success |
|---|---|---|
| 0 | (none — single-string) | 0.5621 |
| 1 | bag_harvest | 0.6464 |
| 2 | bag_harvest, primary_propulsion | 0.7111 |
| 3 | bag_harvest, primary_propulsion, comms | 0.7608 |
| 4 | bag_harvest, primary_propulsion, comms, reactor_power | 0.7989 |
| 5 | bag_harvest, primary_propulsion, comms, reactor_power, gnc_compute | 0.8388 |
| 6 | bag_harvest, primary_propulsion, comms, reactor_power, gnc_compute, thermal_control | 0.8808 |
| 7 | bag_harvest, primary_propulsion, comms, reactor_power, gnc_compute, thermal_control, return_handoff | 0.9248 |

**Result:** 7 subsystems need 2-of-3 redundancy to clear 0.90.

### Target = 0.80 (relaxed)

| Step | Redundancy applied to | Projected mission success |
|---|---|---|
| 0 | (none — single-string) | 0.5621 |
| 1 | bag_harvest | 0.6464 |
| 2 | bag_harvest, primary_propulsion | 0.7111 |
| 3 | bag_harvest, primary_propulsion, comms | 0.7608 |
| 4 | bag_harvest, primary_propulsion, comms, reactor_power | 0.7989 |
| 5 | bag_harvest, primary_propulsion, comms, reactor_power, gnc_compute | 0.8388 |

**Result:** 5 subsystems need 2-of-3 redundancy to clear 0.80.

### Target = 0.75 (relaxed further)

| Step | Redundancy applied to | Projected mission success |
|---|---|---|
| 0 | (none — single-string) | 0.5621 |
| 1 | bag_harvest | 0.6464 |
| 2 | bag_harvest, primary_propulsion | 0.7111 |
| 3 | bag_harvest, primary_propulsion, comms | 0.7608 |

**Result:** 3 subsystems need 2-of-3 redundancy to clear 0.75.

## L0-09 literal-text feasibility check

P(month has >=1 delivery | launch_cadence_per_yr c, per-mission p) = 1 - exp(-c*p/12).
L0-09 literal: this must be >= 0.95.

| Cadence per yr | Per-mission p | P(month has delivery) | Clears L0-09 0.95? |
|---|---|---|---|
| 1 | 0.70 | 0.0567 | no |
| 1 | 0.80 | 0.0645 | no |
| 1 | 0.90 | 0.0723 | no |
| 1 | 1.00 | 0.0800 | no |
| 2 | 0.70 | 0.1101 | no |
| 2 | 0.80 | 0.1248 | no |
| 2 | 0.90 | 0.1393 | no |
| 2 | 1.00 | 0.1535 | no |
| 4 | 0.70 | 0.2081 | no |
| 4 | 0.80 | 0.2341 | no |
| 4 | 0.90 | 0.2592 | no |
| 4 | 1.00 | 0.2835 | no |
| 12 | 0.70 | 0.5034 | no |
| 12 | 0.80 | 0.5507 | no |
| 12 | 0.90 | 0.5934 | no |
| 12 | 1.00 | 0.6321 | no |