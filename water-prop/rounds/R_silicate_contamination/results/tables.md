### Silicate fraction at thruster and grid life by option × contamination level

Bag-incidental rejection ratio (R11) = 1e-4 across all options. Downstream filter rejection adds on top.

| Option | Raw silicate fraction | F_at_thruster | Grid life (yr, linear) | Grid life (yr, superlinear 1.5) |
|---|---:|---:|---:|---:|
| A_bag_only | 1.0% | 1.00e-06 | 0.34 | 0.34 |
| A_bag_only | 3.0% | 3.00e-06 | 0.13 | 0.08 |
| A_bag_only | 7.0% | 7.00e-06 | 0.06 | 0.02 |
| B_mesh_zeolite | 1.0% | 1.00e-08 | 1.65 | 1.70 |
| B_mesh_zeolite | 3.0% | 3.00e-08 | 1.53 | 1.68 |
| B_mesh_zeolite | 7.0% | 7.00e-08 | 1.34 | 1.59 |
| C_electrolysis_separation | 1.0% | 1.00e-12 | 1.71 | 1.71 |
| C_electrolysis_separation | 3.0% | 3.00e-12 | 1.71 | 1.71 |
| C_electrolysis_separation | 7.0% | 7.00e-12 | 1.71 | 1.71 |

### Isp ceilings by filtration option × thruster class

Hall and MET columns are sensitivity comparisons. The matrix-relevant column is gridded_rf_ion.

| Option | Hall (s) | Gridded/RF ion (s) | MET (s) | Matrix dual-ion (s) |
|---|---:|---:|---:|---:|
| A_bag_only | 1500 | — | 800 | — |
| B_mesh_zeolite | 1800 | 3000 | 800 | — |
| C_electrolysis_separation | 1800 | 4000 | 800 | 5000 |

### Megawatt cell (1000 kWe, 500 t chunk) delivered-per-launch-mass by option × Isp cap

Bundled 10-W/kg dry-mass formula + filtration mass penalty + power-draw derate.

| Option | Isp cap 2000 s | Isp cap 3000 s | Isp cap 5000 s |
|---|---:|---:|---:|
| A_bag_only | 0.141 (used 800 s) | 0.141 (used 800 s) | 0.141 (used 800 s) |
| B_mesh_zeolite | 0.289 (used 2000 s) | 0.332 (used 3000 s) | 0.332 (used 3000 s) |
| C_electrolysis_separation | 0.286 (used 2000 s) | 0.329 (used 3000 s) | 0.353 (used 4000 s) |

### Sub-megawatt cell (200 kWe, 500 t chunk) delivered-per-launch-mass by option × Isp cap

| Option | Isp cap 2000 s | Isp cap 3000 s | Isp cap 5000 s |
|---|---:|---:|---:|
| A_bag_only | 0.757 (used 800 s) | 0.757 (used 800 s) | 0.757 (used 800 s) |
| B_mesh_zeolite | 1.290 (used 2000 s) | 1.449 (used 3000 s) | 1.449 (used 3000 s) |
| C_electrolysis_separation | 1.244 (used 2000 s) | 1.398 (used 3000 s) | 1.482 (used 4000 s) |

### Option C breakeven check at megawatt (1000 kWe)

Does (Option C + Isp 5000 s) beat (Option B + Isp 2000 s) at megawatt-class reactor?

| Chunk (t) | Option C @ 5000 s ratio | Option B @ 2000 s ratio | C/B | C wins? |
|---:|---:|---:|---:|---|
| 100 | 0.060 | 0.037 | 1.598 | yes |
| 200 | 0.133 | 0.100 | 1.328 | yes |
| 500 | 0.353 | 0.289 | 1.223 | yes |

### Full architecture matrix re-derivation (delivered/launch-mass, chunk = 500 t)

Bundled-10-W/kg dry mass; outbound chemical-kick at 6.9× multiplier. All cells use gridded_rf_ion ceiling capped at Isp cap, except where the option/thruster combo has no viable gridded thruster (falls back to MET 800 s).

| Reactor (kWe) | Option A @ 2000 s cap | Option B @ 2000 s cap | Option B @ 3000 s cap | Option C @ 5000 s cap |
|---:|---:|---:|---:|---:|
| 10 | 3.316 (800 s, τ=42.4 yr) | 5.386 (2000 s, τ=132.5 yr) | 6.018 (3000 s, τ=209.3 yr) | 5.541 (4000 s, τ=574.2 yr) |
| 40 | 2.194 (800 s, τ=10.7 yr) | 3.602 (2000 s, τ=33.3 yr) | 4.028 (3000 s, τ=52.6 yr) | 3.874 (4000 s, τ=82.5 yr) |
| 100 | 1.296 (800 s, τ=4.3 yr) | 2.161 (2000 s, τ=13.5 yr) | 2.420 (3000 s, τ=21.3 yr) | 2.416 (4000 s, τ=30.8 yr) |
| 200 | 0.757 (800 s, τ=2.2 yr) | 1.290 (2000 s, τ=6.9 yr) | 1.449 (3000 s, τ=10.9 yr) | 1.482 (4000 s, τ=15.3 yr) |
| 500 | 0.316 (800 s, τ=0.9 yr) | 0.574 (2000 s, τ=2.9 yr) | 0.650 (3000 s, τ=4.6 yr) | 0.681 (4000 s, τ=6.4 yr) |
| 1000 | 0.141 (800 s, τ=0.5 yr) | 0.289 (2000 s, τ=1.6 yr) | 0.332 (3000 s, τ=2.5 yr) | 0.353 (4000 s, τ=3.4 yr) |
| 2000 | 0.047 (800 s, τ=0.3 yr) | 0.135 (2000 s, τ=0.9 yr) | 0.162 (3000 s, τ=1.5 yr) | 0.175 (4000 s, τ=2.0 yr) |

### Silicate inclusion particle-size distribution — Option B mechanical sufficiency

Per user hint 2026-05-15: load-bearing question for Option B is what fraction of silicate inclusions are sub-100-nm (mechanical-filter-transparent). Two PSD cases applied on top of Option B's 100 nm sintered Inconel mesh.

References: Cuzzi & Estrada 1998 (Brownlee 1–100 μm interplanetary dust delivery); Hsu et al. 2018 (Cassini Cosmic Dust Analyzer Grand Finale, nano-tail in processed particles); Hsu et al. 2015 (sub-100-nm — but E-ring origin, not B-ring resident).


Size-class bin fractions and filter efficiencies:

| Size class | Filter capture efficiency |
|---|---|
| macro_gt_10um | 0.999999 |
| micro_0p1_to_10um | 0.999900 |
| nano_lt_100nm_or_dissolved | 0.000000 |

Grid life under Option B with PSD-resolved filter pass-through:

| PSD case | Bin fractions (macro / micro / nano) | Contamination | F post-filter | Grid life (yr, linear) |
|---|---|---|---:|---:|
| nominal_brownlee_dominated | 40% / 55% / 5% | clean_B_ring (1%) | 5.01e-08 | 1.43 |
| nominal_brownlee_dominated | 40% / 55% / 5% | nominal_B_ring (3%) | 1.50e-07 | 1.07 |
| nominal_brownlee_dominated | 40% / 55% / 5% | pessimistic_B_ring (7%) | 3.50e-07 | 0.71 |
| pessimistic_nano_tail | 20% / 50% / 30% | clean_B_ring (1%) | 3.00e-07 | 0.78 |
| pessimistic_nano_tail | 20% / 50% / 30% | nominal_B_ring (3%) | 9.00e-07 | 0.37 |
| pessimistic_nano_tail | 20% / 50% / 30% | pessimistic_B_ring (7%) | 2.10e-06 | 0.18 |

**H-sc-h verdict:** worst-case (pessimistic PSD × 7% silicate) grid life = 0.18 yr. Option B mechanically INSUFFICIENT under pessimistic PSD: Option C forced regardless of matrix economics


### Hypothesis grading

| Sub-claim | Predicted | Actual | Held? |
|---|---|---|---|
| H-sc-a — B-ring silicate fraction nominal | 1–7%, central 3% | 1–7% used; 3% nominal (Cassini Cosmic Dust Analyzer, Hsu 2015) | yes (by construction) |
| H-sc-b — Option-A specific-impulse ceiling | 1500–2000 s | Hall 1500 s; gridded RF-ion not viable | yes |
| H-sc-c — Option-B gridded RF-ion ceiling | 2500–3500 s | 3000 s | yes |
| H-sc-d — Option-C dedicated-processing mass | 500–1500 kg | 1000 kg | yes |
| H-sc-e — Megawatt cell ratio drop, Option-B 2000 s vs Option-C 5000 s | 30–50% | +18.3% | **no** |
| H-sc-f — Sub-megawatt cell ratio drop, Option-B 2000 s vs Option-C 5000 s | 10–25% | +13.0% | yes |
| H-sc-g — Option C wins at 500 t chunk (megawatt) | yes | yes | yes |
| H-sc-h — Option B mechanically sufficient under realistic PSD | held if >= 7 yr | grid life 0.18 yr | **no** |