# R-microwave-electrothermal-as-cathode-life-escape-hatch — tables

## Crossover per-swap failure probability (radio-frequency-ion ties microwave-electrothermal)

| Life anchor | N missions | Failure mode | Swaps required | p_crit | At p_crit, microwave-electrothermal wins if real p > | At p_crit, radio-frequency-ion wins if real p < |
|---|---:|---|---:|---:|:---|:---|
| optimistic_50000_hr | 1 | mission_loss_per_failure | 0 | no crossover (radio-frequency-ion always wins) | microwave-electrothermal | radio-frequency-ion |
| optimistic_50000_hr | 1 | tug_loss_per_failure | 0 | no crossover (radio-frequency-ion always wins) | microwave-electrothermal | radio-frequency-ion |
| optimistic_50000_hr | 5 | mission_loss_per_failure | 0 | no crossover (radio-frequency-ion always wins) | microwave-electrothermal | radio-frequency-ion |
| optimistic_50000_hr | 5 | tug_loss_per_failure | 0 | no crossover (radio-frequency-ion always wins) | microwave-electrothermal | radio-frequency-ion |
| optimistic_50000_hr | 10 | mission_loss_per_failure | 1 | 0.4942 | microwave-electrothermal | radio-frequency-ion |
| optimistic_50000_hr | 10 | tug_loss_per_failure | 1 | 0.4942 | microwave-electrothermal | radio-frequency-ion |
| optimistic_50000_hr | 20 | mission_loss_per_failure | 2 | 0.2888 | microwave-electrothermal | radio-frequency-ion |
| optimistic_50000_hr | 20 | tug_loss_per_failure | 2 | 0.2888 | microwave-electrothermal | radio-frequency-ion |
| mid_case_25000_hr | 1 | mission_loss_per_failure | 0 | no crossover (radio-frequency-ion always wins) | microwave-electrothermal | radio-frequency-ion |
| mid_case_25000_hr | 1 | tug_loss_per_failure | 0 | no crossover (radio-frequency-ion always wins) | microwave-electrothermal | radio-frequency-ion |
| mid_case_25000_hr | 5 | mission_loss_per_failure | 1 | 0.4942 | microwave-electrothermal | radio-frequency-ion |
| mid_case_25000_hr | 5 | tug_loss_per_failure | 1 | 0.4942 | microwave-electrothermal | radio-frequency-ion |
| mid_case_25000_hr | 10 | mission_loss_per_failure | 2 | 0.2888 | microwave-electrothermal | radio-frequency-ion |
| mid_case_25000_hr | 10 | tug_loss_per_failure | 2 | 0.2888 | microwave-electrothermal | radio-frequency-ion |
| mid_case_25000_hr | 20 | mission_loss_per_failure | 4 | 0.1566 | microwave-electrothermal | radio-frequency-ion |
| mid_case_25000_hr | 20 | tug_loss_per_failure | 4 | 0.1566 | microwave-electrothermal | radio-frequency-ion |
| pessimistic_3000_hr | 1 | mission_loss_per_failure | 1 | 0.4942 | microwave-electrothermal | radio-frequency-ion |
| pessimistic_3000_hr | 1 | tug_loss_per_failure | 1 | 0.4942 | microwave-electrothermal | radio-frequency-ion |
| pessimistic_3000_hr | 5 | mission_loss_per_failure | 9 | 0.0729 | microwave-electrothermal | radio-frequency-ion |
| pessimistic_3000_hr | 5 | tug_loss_per_failure | 9 | 0.0729 | microwave-electrothermal | radio-frequency-ion |
| pessimistic_3000_hr | 10 | mission_loss_per_failure | 18 | 0.0371 | microwave-electrothermal | radio-frequency-ion |
| pessimistic_3000_hr | 10 | tug_loss_per_failure | 18 | 0.0371 | microwave-electrothermal | radio-frequency-ion |
| pessimistic_3000_hr | 20 | mission_loss_per_failure | 36 | 0.0187 | microwave-electrothermal | radio-frequency-ion |
| pessimistic_3000_hr | 20 | tug_loss_per_failure | 36 | 0.0187 | microwave-electrothermal | radio-frequency-ion |

## Lifetime delivered chunk, mission-loss-per-failure model (Dawn-realistic)

Per mission baseline: microwave-electrothermal 35.6% × 200 t = 71.2 t; radio-frequency-ion 70.4% × 200 t = 140.8 t (before spare-mass penalty)

| Life anchor | N missions | Thruster | Swaps | p_swap | Per-mission % | Lifetime delivered (t) |
|---|---:|---|---:|---:|---:|---:|
| optimistic_50000_hr | 10 | water_microwave_electrothermal | 0 | 0.00 | 35.6% | 712.0 |
| optimistic_50000_hr | 10 | water_microwave_electrothermal | 0 | 0.01 | 35.6% | 712.0 |
| optimistic_50000_hr | 10 | water_microwave_electrothermal | 0 | 0.05 | 35.6% | 712.0 |
| optimistic_50000_hr | 10 | water_microwave_electrothermal | 0 | 0.10 | 35.6% | 712.0 |
| optimistic_50000_hr | 10 | water_radio_frequency_ion | 1 | 0.00 | 70.4% | 1407.8 |
| optimistic_50000_hr | 10 | water_radio_frequency_ion | 1 | 0.01 | 70.4% | 1393.7 |
| optimistic_50000_hr | 10 | water_radio_frequency_ion | 1 | 0.05 | 70.4% | 1337.4 |
| optimistic_50000_hr | 10 | water_radio_frequency_ion | 1 | 0.10 | 70.4% | 1267.0 |
| mid_case_25000_hr | 10 | water_microwave_electrothermal | 0 | 0.00 | 35.6% | 712.0 |
| mid_case_25000_hr | 10 | water_microwave_electrothermal | 0 | 0.01 | 35.6% | 712.0 |
| mid_case_25000_hr | 10 | water_microwave_electrothermal | 0 | 0.05 | 35.6% | 712.0 |
| mid_case_25000_hr | 10 | water_microwave_electrothermal | 0 | 0.10 | 35.6% | 712.0 |
| mid_case_25000_hr | 10 | water_radio_frequency_ion | 2 | 0.00 | 70.4% | 1407.6 |
| mid_case_25000_hr | 10 | water_radio_frequency_ion | 2 | 0.01 | 70.4% | 1379.6 |
| mid_case_25000_hr | 10 | water_radio_frequency_ion | 2 | 0.05 | 70.4% | 1270.4 |
| mid_case_25000_hr | 10 | water_radio_frequency_ion | 2 | 0.10 | 70.4% | 1140.2 |
| pessimistic_3000_hr | 10 | water_microwave_electrothermal | 0 | 0.00 | 35.6% | 712.0 |
| pessimistic_3000_hr | 10 | water_microwave_electrothermal | 0 | 0.01 | 35.6% | 712.0 |
| pessimistic_3000_hr | 10 | water_microwave_electrothermal | 0 | 0.05 | 35.6% | 712.0 |
| pessimistic_3000_hr | 10 | water_microwave_electrothermal | 0 | 0.10 | 35.6% | 712.0 |
| pessimistic_3000_hr | 10 | water_radio_frequency_ion | 18 | 0.00 | 70.3% | 1405.4 |
| pessimistic_3000_hr | 10 | water_radio_frequency_ion | 18 | 0.01 | 70.3% | 1172.8 |
| pessimistic_3000_hr | 10 | water_radio_frequency_ion | 18 | 0.05 | 70.3% | 558.2 |
| pessimistic_3000_hr | 10 | water_radio_frequency_ion | 18 | 0.10 | 70.3% | 210.9 |

## Direct head-to-head at Wang pessimistic 3,000-hour life, 10-mission reuse, mission-loss model

| p_swap | microwave-electrothermal lifetime (t) | radio-frequency-ion lifetime (t) | Verdict |
|---:|---:|---:|:---|
| 0.00 | 712.0 | 1405.4 | radio-frequency-ion |
| 0.01 | 712.0 | 1172.8 | radio-frequency-ion |
| 0.05 | 712.0 | 558.2 | microwave-electrothermal |
| 0.10 | 712.0 | 210.9 | microwave-electrothermal |
| 0.25 | 712.0 | 7.9 | microwave-electrothermal |
