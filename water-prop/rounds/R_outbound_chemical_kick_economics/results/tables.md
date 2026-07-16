# R-outbound-chemical-kick-economics — Tables

## Per-cell variant_b_closure (PRIMARY-text source)

| Path | Variant | Chunk (t) | Tug (t) | Out kick prop (t) | LEO mission-1 (t) | Egress prop (t) | Chunk after egress (t) | Inbound prop (t) | Delivered (t) | Round-trip (yr) | L0-05 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|
| path_1_variant_C | C — Earth aerocapture only | 200 | 63.4 | 154.4 | 227.8 | 0.0 | 200.0 | 167.9 | 32.13 | 16.32 | fail |
| path_1_variant_C | C — Earth aerocapture only | 482 | 72.7 | 174.0 | 256.6 | 0.0 | 482.0 | 353.5 | 128.47 | 19.80 | fail |
| path_4_variant_D | D — Saturn-egress chemical kick + Earth aerocapture | 200 | 59.0 | 145.2 | 214.2 | 100.0 | 100.0 | 80.1 | 19.96 | 14.67 | hard |
| path_4_variant_D | D — Saturn-egress chemical kick + Earth aerocapture | 482 | 63.5 | 154.7 | 228.3 | 206.3 | 275.7 | 170.8 | 104.85 | 16.38 | fail |

## Per-market launch+TSI per ship (mission 1, no depot)

Compares to rhea bake-off / R-reactor-roadmap inherited LAUNCH_PLUS_TSI = $290M/ship.

| Path | Chunk (t) | LEO mass (t) | Market | n launches | Launch USD | Total launch+TSI USD | Implied $/kg | Ratio vs $290M |
|---|---:|---:|---|---:|---:|---:|---:|---:|
| path_1_variant_C | 200 | 227.8 | starship_floor_$100/kg | 2 | $40M | $180M | $176/kg | 0.62× |
| path_1_variant_C | 200 | 227.8 | starship_target_$200/kg | 1 | $100M | $240M | $439/kg | 0.83× |
| path_1_variant_C | 200 | 227.8 | starship_pessimistic_$500/kg | 3 | $300M | $440M | $1317/kg | 1.52× |
| path_1_variant_C | 200 | 227.8 | falcon_heavy_realistic_$1500/kg | 3 | $450M | $590M | $1975/kg | 2.03× |
| path_1_variant_C | 200 | 227.8 | falcon_heavy_expendable_published | 4 | $600M | $740M | $2634/kg | 2.55× |
| path_1_variant_C | 200 | 227.8 | SLS_class_$5000/kg | 3 | $1425M | $1565M | $6255/kg | 5.40× |
| path_1_variant_C | 482 | 256.6 | starship_floor_$100/kg | 2 | $40M | $180M | $156/kg | 0.62× |
| path_1_variant_C | 482 | 256.6 | starship_target_$200/kg | 2 | $200M | $340M | $779/kg | 1.17× |
| path_1_variant_C | 482 | 256.6 | starship_pessimistic_$500/kg | 3 | $300M | $440M | $1169/kg | 1.52× |
| path_1_variant_C | 482 | 256.6 | falcon_heavy_realistic_$1500/kg | 3 | $450M | $590M | $1753/kg | 2.03× |
| path_1_variant_C | 482 | 256.6 | falcon_heavy_expendable_published | 5 | $750M | $890M | $2922/kg | 3.07× |
| path_1_variant_C | 482 | 256.6 | SLS_class_$5000/kg | 3 | $1425M | $1565M | $5553/kg | 5.40× |
| path_4_variant_D | 200 | 214.2 | starship_floor_$100/kg | 2 | $40M | $180M | $187/kg | 0.62× |
| path_4_variant_D | 200 | 214.2 | starship_target_$200/kg | 1 | $100M | $240M | $467/kg | 0.83× |
| path_4_variant_D | 200 | 214.2 | starship_pessimistic_$500/kg | 3 | $300M | $440M | $1401/kg | 1.52× |
| path_4_variant_D | 200 | 214.2 | falcon_heavy_realistic_$1500/kg | 3 | $450M | $590M | $2101/kg | 2.03× |
| path_4_variant_D | 200 | 214.2 | falcon_heavy_expendable_published | 4 | $600M | $740M | $2801/kg | 2.55× |
| path_4_variant_D | 200 | 214.2 | SLS_class_$5000/kg | 3 | $1425M | $1565M | $6653/kg | 5.40× |
| path_4_variant_D | 482 | 228.3 | starship_floor_$100/kg | 2 | $40M | $180M | $175/kg | 0.62× |
| path_4_variant_D | 482 | 228.3 | starship_target_$200/kg | 1 | $100M | $240M | $438/kg | 0.83× |
| path_4_variant_D | 482 | 228.3 | starship_pessimistic_$500/kg | 3 | $300M | $440M | $1314/kg | 1.52× |
| path_4_variant_D | 482 | 228.3 | falcon_heavy_realistic_$1500/kg | 3 | $450M | $590M | $1971/kg | 2.03× |
| path_4_variant_D | 482 | 228.3 | falcon_heavy_expendable_published | 4 | $600M | $740M | $2629/kg | 2.55× |
| path_4_variant_D | 482 | 228.3 | SLS_class_$5000/kg | 3 | $1425M | $1565M | $6243/kg | 5.40× |

## Marginal IRR sweep — passes/fails sovereign-bond (4 percent IRR)

| Path | Chunk (t) | Market | Water $/kg | Sovereign | Delivered (t) | RT (yr) | L0-05 | Marg IRR | Pass sov-bond hard? | Pass sov-bond soft? |
|---|---:|---|---:|---|---:|---:|:---:|---:|:---:|:---:|
| path_1_variant_C | 200 | starship_floor_$100/kg | 2000 | no_sovereign | 32.13 | 16.32 | over_by_1.32yr | 0.0000 | ✗ | ✗ |
| path_1_variant_C | 200 | starship_floor_$100/kg | 2000 | sovereign_2B_y11 | 32.13 | 16.32 | over_by_1.32yr | 0.0000 | ✗ | ✗ |
| path_1_variant_C | 200 | starship_floor_$100/kg | 10000 | no_sovereign | 32.13 | 16.32 | over_by_1.32yr | 0.0000 | ✗ | ✗ |
| path_1_variant_C | 200 | starship_floor_$100/kg | 10000 | sovereign_2B_y11 | 32.13 | 16.32 | over_by_1.32yr | 0.0000 | ✗ | ✗ |
| path_1_variant_C | 200 | starship_target_$200/kg | 2000 | no_sovereign | 32.13 | 16.32 | over_by_1.32yr | 0.0000 | ✗ | ✗ |
| path_1_variant_C | 200 | starship_target_$200/kg | 2000 | sovereign_2B_y11 | 32.13 | 16.32 | over_by_1.32yr | 0.0000 | ✗ | ✗ |
| path_1_variant_C | 200 | starship_target_$200/kg | 10000 | no_sovereign | 32.13 | 16.32 | over_by_1.32yr | 0.0000 | ✗ | ✗ |
| path_1_variant_C | 200 | starship_target_$200/kg | 10000 | sovereign_2B_y11 | 32.13 | 16.32 | over_by_1.32yr | 0.0000 | ✗ | ✗ |
| path_1_variant_C | 200 | starship_pessimistic_$500/kg | 2000 | no_sovereign | 32.13 | 16.32 | over_by_1.32yr | 0.0000 | ✗ | ✗ |
| path_1_variant_C | 200 | starship_pessimistic_$500/kg | 2000 | sovereign_2B_y11 | 32.13 | 16.32 | over_by_1.32yr | 0.0000 | ✗ | ✗ |
| path_1_variant_C | 200 | starship_pessimistic_$500/kg | 10000 | no_sovereign | 32.13 | 16.32 | over_by_1.32yr | 0.0000 | ✗ | ✗ |
| path_1_variant_C | 200 | starship_pessimistic_$500/kg | 10000 | sovereign_2B_y11 | 32.13 | 16.32 | over_by_1.32yr | 0.0000 | ✗ | ✗ |
| path_1_variant_C | 200 | falcon_heavy_realistic_$1500/kg | 2000 | no_sovereign | 32.13 | 16.32 | over_by_1.32yr | 0.0000 | ✗ | ✗ |
| path_1_variant_C | 200 | falcon_heavy_realistic_$1500/kg | 2000 | sovereign_2B_y11 | 32.13 | 16.32 | over_by_1.32yr | 0.0000 | ✗ | ✗ |
| path_1_variant_C | 200 | falcon_heavy_realistic_$1500/kg | 10000 | no_sovereign | 32.13 | 16.32 | over_by_1.32yr | 0.0000 | ✗ | ✗ |
| path_1_variant_C | 200 | falcon_heavy_realistic_$1500/kg | 10000 | sovereign_2B_y11 | 32.13 | 16.32 | over_by_1.32yr | 0.0000 | ✗ | ✗ |
| path_1_variant_C | 200 | falcon_heavy_expendable_published | 2000 | no_sovereign | 32.13 | 16.32 | over_by_1.32yr | 0.0000 | ✗ | ✗ |
| path_1_variant_C | 200 | falcon_heavy_expendable_published | 2000 | sovereign_2B_y11 | 32.13 | 16.32 | over_by_1.32yr | 0.0000 | ✗ | ✗ |
| path_1_variant_C | 200 | falcon_heavy_expendable_published | 10000 | no_sovereign | 32.13 | 16.32 | over_by_1.32yr | 0.0000 | ✗ | ✗ |
| path_1_variant_C | 200 | falcon_heavy_expendable_published | 10000 | sovereign_2B_y11 | 32.13 | 16.32 | over_by_1.32yr | 0.0000 | ✗ | ✗ |
| path_1_variant_C | 200 | SLS_class_$5000/kg | 2000 | no_sovereign | 32.13 | 16.32 | over_by_1.32yr | 0.0000 | ✗ | ✗ |
| path_1_variant_C | 200 | SLS_class_$5000/kg | 2000 | sovereign_2B_y11 | 32.13 | 16.32 | over_by_1.32yr | 0.0000 | ✗ | ✗ |
| path_1_variant_C | 200 | SLS_class_$5000/kg | 10000 | no_sovereign | 32.13 | 16.32 | over_by_1.32yr | 0.0000 | ✗ | ✗ |
| path_1_variant_C | 200 | SLS_class_$5000/kg | 10000 | sovereign_2B_y11 | 32.13 | 16.32 | over_by_1.32yr | 0.0000 | ✗ | ✗ |
| path_1_variant_C | 482 | starship_floor_$100/kg | 2000 | no_sovereign | 128.47 | 19.80 | over_by_4.80yr | 0.0000 | ✗ | ✗ |
| path_1_variant_C | 482 | starship_floor_$100/kg | 2000 | sovereign_2B_y11 | 128.47 | 19.80 | over_by_4.80yr | 0.0000 | ✗ | ✗ |
| path_1_variant_C | 482 | starship_floor_$100/kg | 10000 | no_sovereign | 128.47 | 19.80 | over_by_4.80yr | 0.0188 | ✗ | ✗ |
| path_1_variant_C | 482 | starship_floor_$100/kg | 10000 | sovereign_2B_y11 | 128.47 | 19.80 | over_by_4.80yr | 0.0209 | ✗ | ✗ |
| path_1_variant_C | 482 | starship_target_$200/kg | 2000 | no_sovereign | 128.47 | 19.80 | over_by_4.80yr | 0.0000 | ✗ | ✗ |
| path_1_variant_C | 482 | starship_target_$200/kg | 2000 | sovereign_2B_y11 | 128.47 | 19.80 | over_by_4.80yr | 0.0000 | ✗ | ✗ |
| path_1_variant_C | 482 | starship_target_$200/kg | 10000 | no_sovereign | 128.47 | 19.80 | over_by_4.80yr | 0.0106 | ✗ | ✗ |
| path_1_variant_C | 482 | starship_target_$200/kg | 10000 | sovereign_2B_y11 | 128.47 | 19.80 | over_by_4.80yr | 0.0116 | ✗ | ✗ |
| path_1_variant_C | 482 | starship_pessimistic_$500/kg | 2000 | no_sovereign | 128.47 | 19.80 | over_by_4.80yr | 0.0000 | ✗ | ✗ |
| path_1_variant_C | 482 | starship_pessimistic_$500/kg | 2000 | sovereign_2B_y11 | 128.47 | 19.80 | over_by_4.80yr | 0.0000 | ✗ | ✗ |
| path_1_variant_C | 482 | starship_pessimistic_$500/kg | 10000 | no_sovereign | 128.47 | 19.80 | over_by_4.80yr | 0.0060 | ✗ | ✗ |
| path_1_variant_C | 482 | starship_pessimistic_$500/kg | 10000 | sovereign_2B_y11 | 128.47 | 19.80 | over_by_4.80yr | 0.0066 | ✗ | ✗ |
| path_1_variant_C | 482 | falcon_heavy_realistic_$1500/kg | 2000 | no_sovereign | 128.47 | 19.80 | over_by_4.80yr | 0.0000 | ✗ | ✗ |
| path_1_variant_C | 482 | falcon_heavy_realistic_$1500/kg | 2000 | sovereign_2B_y11 | 128.47 | 19.80 | over_by_4.80yr | 0.0000 | ✗ | ✗ |
| path_1_variant_C | 482 | falcon_heavy_realistic_$1500/kg | 10000 | no_sovereign | 128.47 | 19.80 | over_by_4.80yr | 0.0000 | ✗ | ✗ |
| path_1_variant_C | 482 | falcon_heavy_realistic_$1500/kg | 10000 | sovereign_2B_y11 | 128.47 | 19.80 | over_by_4.80yr | 0.0000 | ✗ | ✗ |
| path_1_variant_C | 482 | falcon_heavy_expendable_published | 2000 | no_sovereign | 128.47 | 19.80 | over_by_4.80yr | 0.0000 | ✗ | ✗ |
| path_1_variant_C | 482 | falcon_heavy_expendable_published | 2000 | sovereign_2B_y11 | 128.47 | 19.80 | over_by_4.80yr | 0.0000 | ✗ | ✗ |
| path_1_variant_C | 482 | falcon_heavy_expendable_published | 10000 | no_sovereign | 128.47 | 19.80 | over_by_4.80yr | 0.0000 | ✗ | ✗ |
| path_1_variant_C | 482 | falcon_heavy_expendable_published | 10000 | sovereign_2B_y11 | 128.47 | 19.80 | over_by_4.80yr | 0.0000 | ✗ | ✗ |
| path_1_variant_C | 482 | SLS_class_$5000/kg | 2000 | no_sovereign | 128.47 | 19.80 | over_by_4.80yr | 0.0000 | ✗ | ✗ |
| path_1_variant_C | 482 | SLS_class_$5000/kg | 2000 | sovereign_2B_y11 | 128.47 | 19.80 | over_by_4.80yr | 0.0000 | ✗ | ✗ |
| path_1_variant_C | 482 | SLS_class_$5000/kg | 10000 | no_sovereign | 128.47 | 19.80 | over_by_4.80yr | 0.0000 | ✗ | ✗ |
| path_1_variant_C | 482 | SLS_class_$5000/kg | 10000 | sovereign_2B_y11 | 128.47 | 19.80 | over_by_4.80yr | 0.0000 | ✗ | ✗ |
| path_4_variant_D | 200 | starship_floor_$100/kg | 2000 | no_sovereign | 19.96 | 14.67 | hard_pass | 0.0000 | ✗ | ✗ |
| path_4_variant_D | 200 | starship_floor_$100/kg | 2000 | sovereign_2B_y11 | 19.96 | 14.67 | hard_pass | 0.0000 | ✗ | ✗ |
| path_4_variant_D | 200 | starship_floor_$100/kg | 10000 | no_sovereign | 19.96 | 14.67 | hard_pass | 0.0000 | ✗ | ✗ |
| path_4_variant_D | 200 | starship_floor_$100/kg | 10000 | sovereign_2B_y11 | 19.96 | 14.67 | hard_pass | 0.0000 | ✗ | ✗ |
| path_4_variant_D | 200 | starship_target_$200/kg | 2000 | no_sovereign | 19.96 | 14.67 | hard_pass | 0.0000 | ✗ | ✗ |
| path_4_variant_D | 200 | starship_target_$200/kg | 2000 | sovereign_2B_y11 | 19.96 | 14.67 | hard_pass | 0.0000 | ✗ | ✗ |
| path_4_variant_D | 200 | starship_target_$200/kg | 10000 | no_sovereign | 19.96 | 14.67 | hard_pass | 0.0000 | ✗ | ✗ |
| path_4_variant_D | 200 | starship_target_$200/kg | 10000 | sovereign_2B_y11 | 19.96 | 14.67 | hard_pass | 0.0000 | ✗ | ✗ |
| path_4_variant_D | 200 | starship_pessimistic_$500/kg | 2000 | no_sovereign | 19.96 | 14.67 | hard_pass | 0.0000 | ✗ | ✗ |
| path_4_variant_D | 200 | starship_pessimistic_$500/kg | 2000 | sovereign_2B_y11 | 19.96 | 14.67 | hard_pass | 0.0000 | ✗ | ✗ |
| path_4_variant_D | 200 | starship_pessimistic_$500/kg | 10000 | no_sovereign | 19.96 | 14.67 | hard_pass | 0.0000 | ✗ | ✗ |
| path_4_variant_D | 200 | starship_pessimistic_$500/kg | 10000 | sovereign_2B_y11 | 19.96 | 14.67 | hard_pass | 0.0000 | ✗ | ✗ |
| path_4_variant_D | 200 | falcon_heavy_realistic_$1500/kg | 2000 | no_sovereign | 19.96 | 14.67 | hard_pass | 0.0000 | ✗ | ✗ |
| path_4_variant_D | 200 | falcon_heavy_realistic_$1500/kg | 2000 | sovereign_2B_y11 | 19.96 | 14.67 | hard_pass | 0.0000 | ✗ | ✗ |
| path_4_variant_D | 200 | falcon_heavy_realistic_$1500/kg | 10000 | no_sovereign | 19.96 | 14.67 | hard_pass | 0.0000 | ✗ | ✗ |
| path_4_variant_D | 200 | falcon_heavy_realistic_$1500/kg | 10000 | sovereign_2B_y11 | 19.96 | 14.67 | hard_pass | 0.0000 | ✗ | ✗ |
| path_4_variant_D | 200 | falcon_heavy_expendable_published | 2000 | no_sovereign | 19.96 | 14.67 | hard_pass | 0.0000 | ✗ | ✗ |
| path_4_variant_D | 200 | falcon_heavy_expendable_published | 2000 | sovereign_2B_y11 | 19.96 | 14.67 | hard_pass | 0.0000 | ✗ | ✗ |
| path_4_variant_D | 200 | falcon_heavy_expendable_published | 10000 | no_sovereign | 19.96 | 14.67 | hard_pass | 0.0000 | ✗ | ✗ |
| path_4_variant_D | 200 | falcon_heavy_expendable_published | 10000 | sovereign_2B_y11 | 19.96 | 14.67 | hard_pass | 0.0000 | ✗ | ✗ |
| path_4_variant_D | 200 | SLS_class_$5000/kg | 2000 | no_sovereign | 19.96 | 14.67 | hard_pass | 0.0000 | ✗ | ✗ |
| path_4_variant_D | 200 | SLS_class_$5000/kg | 2000 | sovereign_2B_y11 | 19.96 | 14.67 | hard_pass | 0.0000 | ✗ | ✗ |
| path_4_variant_D | 200 | SLS_class_$5000/kg | 10000 | no_sovereign | 19.96 | 14.67 | hard_pass | 0.0000 | ✗ | ✗ |
| path_4_variant_D | 200 | SLS_class_$5000/kg | 10000 | sovereign_2B_y11 | 19.96 | 14.67 | hard_pass | 0.0000 | ✗ | ✗ |
| path_4_variant_D | 482 | starship_floor_$100/kg | 2000 | no_sovereign | 104.85 | 16.38 | over_by_1.38yr | 0.0000 | ✗ | ✗ |
| path_4_variant_D | 482 | starship_floor_$100/kg | 2000 | sovereign_2B_y11 | 104.85 | 16.38 | over_by_1.38yr | 0.0000 | ✗ | ✗ |
| path_4_variant_D | 482 | starship_floor_$100/kg | 10000 | no_sovereign | 104.85 | 16.38 | over_by_1.38yr | 0.0088 | ✗ | ✗ |
| path_4_variant_D | 482 | starship_floor_$100/kg | 10000 | sovereign_2B_y11 | 104.85 | 16.38 | over_by_1.38yr | 0.0099 | ✗ | ✗ |
| path_4_variant_D | 482 | starship_target_$200/kg | 2000 | no_sovereign | 104.85 | 16.38 | over_by_1.38yr | 0.0000 | ✗ | ✗ |
| path_4_variant_D | 482 | starship_target_$200/kg | 2000 | sovereign_2B_y11 | 104.85 | 16.38 | over_by_1.38yr | 0.0000 | ✗ | ✗ |
| path_4_variant_D | 482 | starship_target_$200/kg | 10000 | no_sovereign | 104.85 | 16.38 | over_by_1.38yr | 0.0055 | ✗ | ✗ |
| path_4_variant_D | 482 | starship_target_$200/kg | 10000 | sovereign_2B_y11 | 104.85 | 16.38 | over_by_1.38yr | 0.0061 | ✗ | ✗ |
| path_4_variant_D | 482 | starship_pessimistic_$500/kg | 2000 | no_sovereign | 104.85 | 16.38 | over_by_1.38yr | 0.0000 | ✗ | ✗ |
| path_4_variant_D | 482 | starship_pessimistic_$500/kg | 2000 | sovereign_2B_y11 | 104.85 | 16.38 | over_by_1.38yr | 0.0000 | ✗ | ✗ |
| path_4_variant_D | 482 | starship_pessimistic_$500/kg | 10000 | no_sovereign | 104.85 | 16.38 | over_by_1.38yr | 0.0000 | ✗ | ✗ |
| path_4_variant_D | 482 | starship_pessimistic_$500/kg | 10000 | sovereign_2B_y11 | 104.85 | 16.38 | over_by_1.38yr | 0.0000 | ✗ | ✗ |
| path_4_variant_D | 482 | falcon_heavy_realistic_$1500/kg | 2000 | no_sovereign | 104.85 | 16.38 | over_by_1.38yr | 0.0000 | ✗ | ✗ |
| path_4_variant_D | 482 | falcon_heavy_realistic_$1500/kg | 2000 | sovereign_2B_y11 | 104.85 | 16.38 | over_by_1.38yr | 0.0000 | ✗ | ✗ |
| path_4_variant_D | 482 | falcon_heavy_realistic_$1500/kg | 10000 | no_sovereign | 104.85 | 16.38 | over_by_1.38yr | 0.0000 | ✗ | ✗ |
| path_4_variant_D | 482 | falcon_heavy_realistic_$1500/kg | 10000 | sovereign_2B_y11 | 104.85 | 16.38 | over_by_1.38yr | 0.0000 | ✗ | ✗ |
| path_4_variant_D | 482 | falcon_heavy_expendable_published | 2000 | no_sovereign | 104.85 | 16.38 | over_by_1.38yr | 0.0000 | ✗ | ✗ |
| path_4_variant_D | 482 | falcon_heavy_expendable_published | 2000 | sovereign_2B_y11 | 104.85 | 16.38 | over_by_1.38yr | 0.0000 | ✗ | ✗ |
| path_4_variant_D | 482 | falcon_heavy_expendable_published | 10000 | no_sovereign | 104.85 | 16.38 | over_by_1.38yr | 0.0000 | ✗ | ✗ |
| path_4_variant_D | 482 | falcon_heavy_expendable_published | 10000 | sovereign_2B_y11 | 104.85 | 16.38 | over_by_1.38yr | 0.0000 | ✗ | ✗ |
| path_4_variant_D | 482 | SLS_class_$5000/kg | 2000 | no_sovereign | 104.85 | 16.38 | over_by_1.38yr | 0.0000 | ✗ | ✗ |
| path_4_variant_D | 482 | SLS_class_$5000/kg | 2000 | sovereign_2B_y11 | 104.85 | 16.38 | over_by_1.38yr | 0.0000 | ✗ | ✗ |
| path_4_variant_D | 482 | SLS_class_$5000/kg | 10000 | no_sovereign | 104.85 | 16.38 | over_by_1.38yr | 0.0000 | ✗ | ✗ |
| path_4_variant_D | 482 | SLS_class_$5000/kg | 10000 | sovereign_2B_y11 | 104.85 | 16.38 | over_by_1.38yr | 0.0000 | ✗ | ✗ |

## Hypothesis grading

| Sub-claim | Predicted | Measured | Held? |
|---|---|---|:---:|
| H-ock-a | real outbound prop per mission < 200 t (715 claim overstated by >= 4x) | measured_max_t=173.98041843081836 | ✓ |
| H-ock-b | implied launch cost in [1200, 1400] $/kg | measured_USD_per_kg=1273.0064137383124 | ✓ |
| H-ock-c | central LEO mass / FH expendable capacity >= 2.5 (i.e., >= 3 launches) | measured_ratio=3.5706454393315723 | ✓ |
| H-ock-d | marginal IRR remains <= 0 under FH realistic launch; matches rhea bake-off floor |  | ✓ |
| H-ock-e | no Starship-class config crosses sovereign-bond at L0-05 hard | measured_any_passes=False | ✓ |
| H-ock-f | zero rows cross sovereign-bond at L0-05 hard | measured_count=0 | ✓ |
| H-ock-g | at most 1 row passes at L0-05 soft; if so, requires Starship-class launch | measured_soft_only_count=0 | ✓ |
| H-ock-h | rhea bake-off LAUNCH_PLUS_TSI internally inconsistent with MARVL ship LEO mass | measured_consistency=INCONSISTENT | ✓ |
| H-ock-i | round produces calibration finding, NOT independent kill-shot | measured_kill_shot_signal=True | ✓ |

## Aggregate

- All sub-claims held: **True**
- Kill-shot status: **retired**
- Matrix amendment required: **True**
