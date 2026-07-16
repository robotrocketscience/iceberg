# R-fission-surface-power-stretch-credibility — results

Seed 20260515, 100000 samples.

## Fission cascade stages

| Stage | Lo | Hi |
|---|---|---|
| phase2_awarded_by_FY27 | 0.30 | 0.65 |
| phase2_commits_10W_per_kg | 0.35 | 0.70 |
| 10W_per_kg_achieved_on_demonstrator_by_2032 | 0.10 | 0.35 |
| flight_demonstrator_launched_by_2035 | 0.15 | 0.40 |
| ICEBERG_integration_at_200_300kWe | 0.40 | 0.75 |

## Solar-thermal cascade stages (for comparison)

| Stage | Lo | Hi |
|---|---|---|
| mirror_at_30000m2_qualified_by_2035 | 0.05 | 0.35 |
| SOEC_at_200kW_space_qualified_by_2035 | 0.10 | 0.50 |
| saturn_orbit_conops_viable_for_chunk_delivery | 0.55 | 0.85 |
| ICEBERG_integration_per_mission_completion | 0.40 | 0.75 |

## Posterior comparison

| Statistic | D-fission posterior | D-solar-thermal posterior |
|---|---|---|
| Mean | 0.0089 | 0.0242 |
| Median | 0.0078 | 0.0203 |
| 5th percentile | 0.0029 | 0.0055 |
| 25th percentile | 0.0052 | 0.0120 |
| 75th percentile | 0.0114 | 0.0330 |
| 95th percentile | 0.0187 | 0.0555 |
| P(posterior > 0.02) | 0.036 | 0.509 |
| P(posterior > 0.05) | 0.000 | 0.078 |
| P(posterior > 0.10) | 0.000 | 0.000 |
| P(posterior > 0.15) | 0.000 | 0.000 |

## Falsification verdict: FALSIFIES_REFRAME_lower_than_solar_thermal

Pre-registered rule: hypothesis (D-fission and D-solar-thermal in same credibility band) 
UPHELD if median in [0.03, 0.10]. FALSIFIED below 0.02 (fission less credible) 
or above 0.15 (fission more credible). MARGINAL between [0.02, 0.03) or (0.10, 0.15].
