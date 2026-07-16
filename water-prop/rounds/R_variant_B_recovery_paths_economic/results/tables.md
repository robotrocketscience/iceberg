# R-variant-B-recovery-paths-economic — tables

## Path baselines (chunk = 200 t, specific impulse 2000 s unless noted)

| Path | Variant | Isp (s) | Delivered (t) | Round-trip (yr) | L0-05 | Marginal IRR | Sovereign 4%? | Regulated 8%? | Corporate 10%? |
|---|---|---:|---:|---:|---|---:|:---:|:---:|:---:|
| path_1_variant_C_baseline | C_earth_aerocapture | 2000 | 32.13 | 16.32 | over_by_1.32yr | +0.00% | ✗ | ✗ | ✗ |
| path_3_variant_A_no_recovery | A_as_stated | 2000 | 0.01 | 16.92 | over_by_1.92yr | +0.00% | ✗ | ✗ | ✗ |
| path_4_variant_D_both_recoveries | D_both | 2000 | 19.96 | 14.67 | hard_pass | +0.00% | ✗ | ✗ | ✗ |
| path_5a_variant_C_isp3000 | C_earth_aerocapture | 3000 | 71.52 | 18.59 | over_by_3.59yr | +0.00% | ✗ | ✗ | ✗ |
| path_5b_variant_D_isp3000 | D_both | 3000 | 41.11 | 15.66 | soft_pass | +0.00% | ✗ | ✗ | ✗ |
| path_2_null | None | 2000 | INFEASIBLE: null cell — no propulsion architecture under test |  |  |  |  |  |  |

## Chunk sweep per path

### path_1_variant_C_baseline

| Chunk (t) | Feasible? | Delivered (t) | Round-trip (yr) | L0-05 status | Marginal IRR | Sov 4% | Reg 8% | Cor 10% |
|---:|:---:|---:|---:|---|---:|:---:|:---:|:---:|
| 100 | no | n/a | n/a | infeasible | n/a | – | – | – |
| 150 | yes | 15.05 | 15.70 | soft_pass | +0.00% | ✗ | ✗ | ✗ |
| 200 | yes | 32.13 | 16.32 | over_by_1.32yr | +0.00% | ✗ | ✗ | ✗ |
| 240 | yes | 45.80 | 16.81 | over_by_1.81yr | +0.00% | ✗ | ✗ | ✗ |
| 300 | yes | 66.30 | 17.55 | over_by_2.55yr | +0.00% | ✗ | ✗ | ✗ |
| 400 | yes | 100.46 | 18.79 | over_by_3.79yr | +0.08% | ✗ | ✗ | ✗ |
| 482 | yes | 128.47 | 19.80 | over_by_4.80yr | +1.44% | ✗ | ✗ | ✗ |

### path_3_variant_A_no_recovery

| Chunk (t) | Feasible? | Delivered (t) | Round-trip (yr) | L0-05 status | Marginal IRR | Sov 4% | Reg 8% | Cor 10% |
|---:|:---:|---:|---:|---|---:|:---:|:---:|:---:|
| 100 | no | n/a | n/a | infeasible | n/a | – | – | – |
| 150 | no | n/a | n/a | infeasible | n/a | – | – | – |
| 200 | yes | 0.01 | 16.92 | over_by_1.92yr | +0.00% | ✗ | ✗ | ✗ |
| 240 | yes | 8.64 | 17.51 | over_by_2.51yr | +0.00% | ✗ | ✗ | ✗ |
| 300 | yes | 21.58 | 18.39 | over_by_3.39yr | +0.00% | ✗ | ✗ | ✗ |
| 400 | yes | 43.15 | 19.86 | over_by_4.86yr | +0.00% | ✗ | ✗ | ✗ |
| 482 | yes | 60.83 | 21.07 | over_by_6.07yr | +0.00% | ✗ | ✗ | ✗ |

### path_4_variant_D_both_recoveries

| Chunk (t) | Feasible? | Delivered (t) | Round-trip (yr) | L0-05 status | Marginal IRR | Sov 4% | Reg 8% | Cor 10% |
|---:|:---:|---:|---:|---|---:|:---:|:---:|:---:|
| 100 | no | n/a | n/a | infeasible | n/a | – | – | – |
| 150 | yes | 4.91 | 14.37 | hard_pass | +0.00% | ✗ | ✗ | ✗ |
| 200 | yes | 19.96 | 14.67 | hard_pass | +0.00% | ✗ | ✗ | ✗ |
| 240 | yes | 32.00 | 14.91 | hard_pass | +0.00% | ✗ | ✗ | ✗ |
| 300 | yes | 50.06 | 15.28 | soft_pass | +0.00% | ✗ | ✗ | ✗ |
| 400 | yes | 80.16 | 15.88 | soft_pass | +0.00% | ✗ | ✗ | ✗ |
| 482 | yes | 104.85 | 16.38 | over_by_1.38yr | +0.32% | ✗ | ✗ | ✗ |

### path_5a_variant_C_isp3000

| Chunk (t) | Feasible? | Delivered (t) | Round-trip (yr) | L0-05 status | Marginal IRR | Sov 4% | Reg 8% | Cor 10% |
|---:|:---:|---:|---:|---|---:|:---:|:---:|:---:|
| 100 | yes | 21.91 | 16.47 | over_by_1.47yr | +0.00% | ✗ | ✗ | ✗ |
| 150 | yes | 46.72 | 17.53 | over_by_2.53yr | +0.00% | ✗ | ✗ | ✗ |
| 200 | yes | 71.52 | 18.59 | over_by_3.59yr | +0.00% | ✗ | ✗ | ✗ |
| 240 | yes | 91.37 | 19.44 | over_by_4.44yr | +0.00% | ✗ | ✗ | ✗ |
| 300 | yes | 121.14 | 20.72 | over_by_5.72yr | +1.12% | ✗ | ✗ | ✗ |
| 400 | yes | 170.75 | 22.85 | over_by_7.85yr | +2.95% | ✗ | ✗ | ✗ |
| 482 | yes | 211.43 | 24.59 | over_by_9.59yr | +4.06% | ✓ | ✗ | ✗ |

### path_5b_variant_D_isp3000

| Chunk (t) | Feasible? | Delivered (t) | Round-trip (yr) | L0-05 status | Marginal IRR | Sov 4% | Reg 8% | Cor 10% |
|---:|:---:|---:|---:|---|---:|:---:|:---:|:---:|
| 100 | yes | 2.51 | 14.66 | hard_pass | +0.00% | ✗ | ✗ | ✗ |
| 150 | yes | 21.81 | 15.16 | soft_pass | +0.00% | ✗ | ✗ | ✗ |
| 200 | yes | 41.11 | 15.66 | soft_pass | +0.00% | ✗ | ✗ | ✗ |
| 240 | yes | 56.55 | 16.06 | over_by_1.06yr | +0.00% | ✗ | ✗ | ✗ |
| 300 | yes | 79.71 | 16.66 | over_by_1.66yr | +0.00% | ✗ | ✗ | ✗ |
| 400 | yes | 118.31 | 17.66 | over_by_2.66yr | +0.99% | ✗ | ✗ | ✗ |
| 482 | yes | 149.96 | 18.48 | over_by_3.48yr | +2.26% | ✗ | ✗ | ✗ |

## Decision table — best (chunk, IRR) per path subject to L0-05

| Path | Best under hard L0-05 (≤15 yr) | Best under soft L0-05 (≤16 yr) |
|---|---|---|
| path_1_variant_C_baseline | no L0-05-acceptable config | chunk 150 t → 15.1 t / RT 15.70 yr / IRR +0.00% |
| path_3_variant_A_no_recovery | no L0-05-acceptable config | no L0-05-acceptable config |
| path_4_variant_D_both_recoveries | chunk 150 t → 4.9 t / RT 14.37 yr / IRR +0.00% | chunk 150 t → 4.9 t / RT 14.37 yr / IRR +0.00% |
| path_5a_variant_C_isp3000 | no L0-05-acceptable config | no L0-05-acceptable config |
| path_5b_variant_D_isp3000 | chunk 100 t → 2.5 t / RT 14.66 yr / IRR +0.00% | chunk 100 t → 2.5 t / RT 14.66 yr / IRR +0.00% |

## Programmatic-risk overlay (expected delivered per mission, chunk 200 t)

| Path | Conditional delivered (t) | Uniform 8.9% | Jeffreys 4.9% | Skeptical 2.9% |
|---|---:|---:|---:|---:|
| path_1_variant_C_baseline | 32.13 | 0.0418 | 0.0096 | 0.0032 |
| path_3_variant_A_no_recovery | 0.01 | 0.0000 | 0.0000 | 0.0000 |
| path_4_variant_D_both_recoveries | 19.96 | 0.0259 | 0.0060 | 0.0020 |
| path_5a_variant_C_isp3000 | 71.52 | 0.0930 | 0.0215 | 0.0072 |
| path_5b_variant_D_isp3000 | 41.11 | 0.0534 | 0.0123 | 0.0041 |

## Hypothesis grading

| Sub-claim | Predicted | Measured | Held? |
|---|---|---|:---:|
| H-vrp-a_path_1_baseline_irr | [-2.0, 2.0] | 0.00% | ✓ |
| H-vrp-b_path_1_chunk482_irr | [0.0, 5.0] | 1.44% | ✓ |
| H-vrp-c_path_3_chunk_le_150_infeasible | variant A at chunk ≤ 150 t is propulsion-infeasible (electric inbound prop > chunk inventory) | {'measured_p3_at_100': False, 'measured_p3_at_150': False} | ✓ |
| H-vrp-d_path_4_baseline_irr_and_L0_05 | [-2.0, 3.0] | 0.00% | ✓ |
| H-vrp-e_path_4_chunk482 | [-1.0, 4.0] | 0.32% | ✓ |
| H-vrp-f_no_path_clears_sovereign_at_l0_05 | no path-and-chunk in the sweep clears sovereign-bond (4%) with round-trip ≤ 16 yr (soft L0-05) | {'measured_any_pass': False} | ✓ |
| H-vrp-g_scope_omits_variant_D | SCOPE.md's three-path enumeration (variant C / null / chunk-reduce variant A) omits variant D (both recoveries), which is propulsion-physically defensible AND the only path inside L0-05 hard ceiling at chunk 200 t. | {'measured': True} | ✓ |
| H-vrp-h_isp_3000_does_not_rescue | specific impulse 3000 s does NOT rescue the cell at any L0-05-acceptable chunk | {'measured_any_rescue': False} | ✓ |
| H-vrp-i_programmatic_uniform_le_0p5 | None | {'measured_max': 0.09298229369834844} | ✓ |
