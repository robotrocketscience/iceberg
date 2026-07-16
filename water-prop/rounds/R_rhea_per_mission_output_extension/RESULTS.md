# RESULTS — rhea per-mission output extension

**Round:** R-rhea-per-mission-output-extension
**Session:** rhea (re-spawn), branch `iceberg-rhea-4`
**Date:** 2026-05-26
**Artifacts:** `R_heterogeneous_cadence/run.py` (extended), `R_heterogeneous_cadence/results/per_sample_trajectories.json`, `hamiltonian_layer1.py`, `results/hamiltonian_layer1_per_sample.json`.

## Deliverables built

- `per_mission_trajectory()` + `capture_trajectories()` + `--emit-trajectories` flag added to het-cadence `run.py` (additive). **Aggregate `het_cadence_summary.json` is byte-for-byte unchanged** (verified by `git diff` after re-run: empty). Same RNG seed; trajectory sample i uses the same clearing price as Monte-Carlo aggregate sample i.
- 100 trajectories emitted (50 het = Regime R chunk_1=50 p=0.90; 50 hom = Regime D chunk_1=200), at WACC 3% / LR 15%, clearing price from R-LEO-water-demand-curve. **Per-mission cumulative NPV reconciles to the aggregate `npv_regime_*` to 8.7e-11 M** (machine zero).
- Hamiltonian Layer 1 (skill Steps 1-5, linear q-space) run over all 100. Trajectory lengths: het N=27 missions, hom N=52 (both far above the N≥10 skill threshold).

## Verdicts

| # | Hypothesis | Verdict | Evidence |
|---|---|---|---|
| H1 | Extension ~30–60 lines additive | **FALSIFIED** | 168 insertions. The SCOPE assumed per-mission cumulative-NPV was already computed in the MC loop; it is **not** — the evaluators return only PV aggregates, so the per-mission cashflow decomposition had to be built fresh. Still additive (aggregate unchanged), same seed. |
| H2 | 25–50% of samples MOMENTUM-DEPENDENT | **FALSIFIED (low)** | 14% MOMENTUM-DEPENDENT across 100. Trajectories are mostly MIXED (40) or NO-GAINS (41); only 14 MOMENTUM, 5 STABLE. (rhea pre-registered this as at-risk-low.) |
| H3 | het MOMENTUM-DEP fraction 5–20 pp > hom | **FALSIFIED** | het 16% vs hom 12% = **+4 pp** — correct direction, below the +5 pp band. |
| H4 | conservation label predicts NPV-positive at AUC > 0.7 | **FALSIFIED** | AUC 0.689. Conservation slope weakly tracks outcome but below threshold. |
| H5 | Layer 1 surfaces a finding beyond the aggregate | **HELD** | It does — by ruling OUT the momentum hypothesis and revealing the variance is price-driven (see READING). A decision-actionable negative result. |
| H6 (load-bearing) | het's 46.26% NPV+ is **concentration-driven** | **FALSIFIED** | het is **not** concentration/momentum-driven; NPV sign is a deterministic function of the exogenous clearing-price draw crossing a fixed breakeven (~$6.5k/kg het, ~$5–6k/kg hom). The risk is price, not concentration. |

## The decisive cross-check

NPV sign separates **cleanly** on clearing price, with zero overlap:

| Cadence | Highest NPV-negative clearing | Lowest NPV-positive clearing | Breakeven |
|---|---|---|---|
| het (Regime R, chunk_1=50) | $6,051/kg | $6,476/kg | ~$6.3k/kg |
| hom (Regime D, chunk_1=200) | $4,959/kg | $6,051/kg | ~$5.5k/kg |

NPV-positive ⟺ sampled clearing price > a fixed per-cadence breakeven. Within each program the missions are near-identical, so there is no "windfall mission" to concentrate on. **41 of 51 NPV-negative trajectories are pure monotonic decline (NO-GAINS) — cost-dominated programs that never had a positive-gain mission.**

het's breakeven sits ~$0.5–1.5k/kg **above** hom's: that is the entire het penalty, expressed as price. Mission 1 delivering 20 t instead of 80 t raises the price at which the program clears — a steady structural drag, not a momentum effect. This is consistent with rhea's existing het-cadence verdict (chunk-shrinking loses NPV) and adds the mechanism: it loses by **shifting the breakeven price up**, not by concentrating revenue into rare windfalls.

## Methodological caveat (honest)

Hamiltonian Layer 1 on a smooth, near-homogeneous cumulative-NPV-by-mission trajectory produces regime labels partly **mechanically**: per-mission increments decline over mission index (later deliveries discounted more), so early missions score high-T → MOMENTUM and late missions low-T → ACCUMULATION regardless of economics. The conservation slope is dominated by the (dq)² term and is DISSIPATIVE for 93/100 almost by construction. The specific regime percentages are therefore weakly informative; the **load-bearing outputs are the het≈hom near-equality and the clean price-threshold separation**, both robust to the labeling artifact (it applies identically to both cadence-classes). The value of running Layer 1 here was to falsify the concentration hypothesis, not to discover a regime structure.
