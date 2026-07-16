# Best architectures at L0-04 floor = 25 tonnes

Source: `sims/mission_graph/runs/20260521T193329Z/cells.jsonl` (4-axis canonical sweep, 625 cells).
Total feasible paths delivering >= 25 t at LEO_depot: **5656**.
Total unique architectures: **322**.

## Top 10 architectures by cell-coverage (most robust across sweep)

| rank | cells | best payload (t) | round-trip (yr) | architecture |
|---:|---:|---:|---:|---|
| 1 | 32 | 37.7 | 11.47 | multi_falcon_2_launch -> autonomous_assembly -> low_thrust_spiral -> ballistic_coast -> direct_chemical_capture -> single_pass_trawl -> chunk_fed_spiral_departure -> inbound_ballistic -> hybrid_aerocapture_aerobraking -> passthrough_already_at_leo |
| 2 | 32 | 37.7 | 11.47 | multi_falcon_2_launch -> autonomous_assembly -> low_thrust_spiral -> ballistic_coast -> direct_chemical_capture -> single_pass_trawl -> chunk_fed_spiral_departure -> inbound_mcc -> hybrid_aerocapture_aerobraking -> passthrough_already_at_leo |
| 3 | 32 | 38.0 | 11.47 | multi_falcon_2_launch -> autonomous_assembly -> low_thrust_spiral -> mcc_only -> direct_chemical_capture -> single_pass_trawl -> chunk_fed_spiral_departure -> inbound_ballistic -> hybrid_aerocapture_aerobraking -> passthrough_already_at_leo |
| 4 | 32 | 38.0 | 11.47 | multi_falcon_2_launch -> autonomous_assembly -> low_thrust_spiral -> mcc_only -> direct_chemical_capture -> single_pass_trawl -> chunk_fed_spiral_departure -> inbound_mcc -> hybrid_aerocapture_aerobraking -> passthrough_already_at_leo |
| 5 | 32 | 37.7 | 11.79 | multi_falcon_4_launch -> autonomous_assembly -> low_thrust_spiral -> ballistic_coast -> direct_chemical_capture -> single_pass_trawl -> chunk_fed_spiral_departure -> inbound_ballistic -> hybrid_aerocapture_aerobraking -> passthrough_already_at_leo |
| 6 | 32 | 37.7 | 11.79 | multi_falcon_4_launch -> autonomous_assembly -> low_thrust_spiral -> ballistic_coast -> direct_chemical_capture -> single_pass_trawl -> chunk_fed_spiral_departure -> inbound_mcc -> hybrid_aerocapture_aerobraking -> passthrough_already_at_leo |
| 7 | 32 | 38.0 | 11.79 | multi_falcon_4_launch -> autonomous_assembly -> low_thrust_spiral -> mcc_only -> direct_chemical_capture -> single_pass_trawl -> chunk_fed_spiral_departure -> inbound_ballistic -> hybrid_aerocapture_aerobraking -> passthrough_already_at_leo |
| 8 | 32 | 38.0 | 11.79 | multi_falcon_4_launch -> autonomous_assembly -> low_thrust_spiral -> mcc_only -> direct_chemical_capture -> single_pass_trawl -> chunk_fed_spiral_departure -> inbound_mcc -> hybrid_aerocapture_aerobraking -> passthrough_already_at_leo |
| 9 | 32 | 37.7 | 12.12 | multi_falcon_6_launch -> autonomous_assembly -> low_thrust_spiral -> ballistic_coast -> direct_chemical_capture -> single_pass_trawl -> chunk_fed_spiral_departure -> inbound_ballistic -> hybrid_aerocapture_aerobraking -> passthrough_already_at_leo |
| 10 | 32 | 37.7 | 12.12 | multi_falcon_6_launch -> autonomous_assembly -> low_thrust_spiral -> ballistic_coast -> direct_chemical_capture -> single_pass_trawl -> chunk_fed_spiral_departure -> inbound_mcc -> hybrid_aerocapture_aerobraking -> passthrough_already_at_leo |

## Top 10 architectures by maximum delivered payload

| rank | best payload (t) | round-trip (yr) | cells | architecture |
|---:|---:|---:|---:|---|
| 1 | 39.5 | 11.93 | 24 | multi_falcon_2_launch -> autonomous_assembly -> low_thrust_spiral -> mcc_only -> fg_gap_periapsis_capture -> single_pass_trawl -> chunk_fed_spiral_departure -> inbound_ballistic -> direct_propulsive_capture -> passthrough_already_at_leo |
| 2 | 39.5 | 12.26 | 24 | multi_falcon_4_launch -> autonomous_assembly -> low_thrust_spiral -> mcc_only -> fg_gap_periapsis_capture -> single_pass_trawl -> chunk_fed_spiral_departure -> inbound_ballistic -> direct_propulsive_capture -> passthrough_already_at_leo |
| 3 | 39.5 | 12.58 | 24 | multi_falcon_6_launch -> autonomous_assembly -> low_thrust_spiral -> mcc_only -> fg_gap_periapsis_capture -> single_pass_trawl -> chunk_fed_spiral_departure -> inbound_ballistic -> direct_propulsive_capture -> passthrough_already_at_leo |
| 4 | 39.3 | 11.93 | 24 | multi_falcon_2_launch -> autonomous_assembly -> low_thrust_spiral -> mcc_only -> subdring_periapsis_capture -> single_pass_trawl -> chunk_fed_spiral_departure -> inbound_ballistic -> direct_propulsive_capture -> passthrough_already_at_leo |
| 5 | 39.3 | 12.26 | 24 | multi_falcon_4_launch -> autonomous_assembly -> low_thrust_spiral -> mcc_only -> subdring_periapsis_capture -> single_pass_trawl -> chunk_fed_spiral_departure -> inbound_ballistic -> direct_propulsive_capture -> passthrough_already_at_leo |
| 6 | 39.3 | 12.58 | 24 | multi_falcon_6_launch -> autonomous_assembly -> low_thrust_spiral -> mcc_only -> subdring_periapsis_capture -> single_pass_trawl -> chunk_fed_spiral_departure -> inbound_ballistic -> direct_propulsive_capture -> passthrough_already_at_leo |
| 7 | 39.1 | 11.93 | 24 | multi_falcon_2_launch -> autonomous_assembly -> low_thrust_spiral -> ballistic_coast -> fg_gap_periapsis_capture -> single_pass_trawl -> chunk_fed_spiral_departure -> inbound_ballistic -> direct_propulsive_capture -> passthrough_already_at_leo |
| 8 | 39.1 | 11.93 | 24 | multi_falcon_2_launch -> autonomous_assembly -> low_thrust_spiral -> ballistic_coast -> fg_gap_periapsis_capture -> single_pass_trawl -> chunk_fed_spiral_departure -> inbound_mcc -> direct_propulsive_capture -> passthrough_already_at_leo |
| 9 | 39.1 | 12.26 | 24 | multi_falcon_4_launch -> autonomous_assembly -> low_thrust_spiral -> ballistic_coast -> fg_gap_periapsis_capture -> single_pass_trawl -> chunk_fed_spiral_departure -> inbound_ballistic -> direct_propulsive_capture -> passthrough_already_at_leo |
| 10 | 39.1 | 12.26 | 24 | multi_falcon_4_launch -> autonomous_assembly -> low_thrust_spiral -> ballistic_coast -> fg_gap_periapsis_capture -> single_pass_trawl -> chunk_fed_spiral_departure -> inbound_mcc -> direct_propulsive_capture -> passthrough_already_at_leo |

## Axis values that admit >= 25-tonne delivery

- **chunk_mass_kg**: {200000.0}
- **electric_thrust_n**: {5.0, 10.0, 25.0}
- **power_kwe**: {30.0, 100.0, 300.0, 1000.0}
- **vehicle_mass_kg**: {50000.0, 63000.0, 100000.0}

## Highest-delivery single path

- **Delivered: 39.52 tonnes at LEO_depot**
- Round-trip time: 11.93 years
- Architecture: `multi_falcon_2_launch -> autonomous_assembly -> low_thrust_spiral -> mcc_only -> fg_gap_periapsis_capture -> single_pass_trawl -> chunk_fed_spiral_departure -> inbound_ballistic -> direct_propulsive_capture -> passthrough_already_at_leo`
- Cell coordinates:
  - chunk_mass_kg: 200000.0
  - electric_thrust_n: 5.0
  - power_kwe: 30.0
  - vehicle_mass_kg: 50000.0
