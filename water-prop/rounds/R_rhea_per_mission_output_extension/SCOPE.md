# R-rhea-per-mission-output-extension — emit per-mission cumulative NPV per Monte Carlo sample from rhea het-cadence

**Status:** scope, pre-study. Authored by Saturn (orchestrator), 2026-05-22 latest+17, after `/decision-framework:hamiltonian` end-to-end test on the capture-efficiency sweep returned schema-valid but result-uninformative output due to N=4 trajectory length.

---

## Why this round

The `/decision-framework:hamiltonian` skill (authored this session) needs a per-mission cumulative-NPV trajectory across the 10-20-mission fleet to produce a load-bearing reading. Skill caveat: trajectories with N<10 are noise-dominated; the per-step regime classification and conservation test become artifact-laden.

The rhea R-heterogeneous-cadence round (`2e85d4f`, integrated 2026-05-15 latest+7) already runs a 10,000-sample Monte Carlo on per-mission economics across a 10-mission fleet. The Monte Carlo aggregates are saved to `results/het_cadence_summary.json` — but **per-trajectory cumulative-NPV points are not emitted**. The summary carries only:

- `het_pct_npv_positive`: 46.26% (aggregate across 10,000 samples)
- `hom_pct_npv_positive`: 50.83%
- `het_median_npv_M`, `hom_median_npv_M`
- per-chunk H1 deltas (4 chunk values × 2 LR rates = 8 cells)
- per-chunk H3 deltas

Per-sample trajectories are computed internally during the Monte Carlo loop but discarded after the aggregate is summarized. **This round extends the run.py to optionally emit per-sample per-mission cumulative-NPV trajectories** for a small subset (100 representative samples) so Hamiltonian Layer 1 can run on each.

**Round type:** small extension to existing rhea run.py (~725 lines). Add output emit; re-run; produce new output JSON.

---

## What needs to change in `R_heterogeneous_cadence/run.py`

1. **Add a `--emit-trajectories` flag** (or equivalent mechanism) that triggers per-sample trajectory capture.
2. **During the Monte Carlo loop, store per-sample per-mission cumulative NPV** for the first N_traj samples (default 100). For each sample, save:
   - `sample_id` (0-99)
   - `regime` ("R" or "D" — Monte Carlo regime label)
   - `chunk_schedule` (the per-mission chunk-mass sequence used for that sample)
   - `per_mission_cumulative_npv_M_usd`: list of N=10 cumulative-NPV values, one per mission in sequence
   - `per_mission_revenue_M_usd`: list of N=10 raw per-mission revenue
   - `per_mission_cost_M_usd`: list of N=10 raw per-mission cost
   - `final_program_npv_M_usd`: the aggregate (same as currently computed)
3. **Emit `results/per_sample_trajectories.json`** with the list of 100 sample records.
4. **Preserve existing summary output unchanged.** This is an additive extension; do not modify the existing Monte Carlo aggregate-summary path.
5. **Document in README** how to enable trajectory capture and what the schema means.

The 100 representative samples should span the regime mix (~46 heterogeneous-NPV+ and ~51 homogeneous-NPV+ at full distribution; reasonable subsample: 50 heterogeneous, 50 homogeneous, or weight-proportional).

---

## The downstream invocation this round enables

Once per-sample trajectories are emitted:

```
/decision-framework:hamiltonian invocation:

Trajectory data source: water-prop/rounds/R_heterogeneous_cadence/results/per_sample_trajectories.json
Schema mapping:
  time_field: "mission_number" (1 through N=10)
  value_field: "cumulative_npv_M_usd" (signed; negative early, may become positive late if program closes)
  log_space: false (NPV can cross zero; additive)
Domain context: ICEBERG 10-mission program-NPV trajectory across the heterogeneous-cadence schedule. STABLE vs MOMENTUM-DEPENDENT tells us whether the program-NPV-positive verdict is robust accumulation across missions or rests on a single windfall mission.
Layer 1 only (no state-velocity pair available).

Expected questions Hamiltonian Layer 1 answers:
- Is the program's NPV-positive verdict driven by accumulation (steady per-mission contribution) or by momentum (rare high-revenue missions dragging the median above zero)?
- What fraction of samples are MOMENTUM-DEPENDENT (sustainability < 0.3) vs STABLE (>= 0.6)?
- Does the het-cadence schedule shift the regime mix vs homogeneous?
- Conservation slope: are most samples DISSIPATIVE (winning) or ENERGY-INJECTING (losing)?
```

The output of this combined run becomes a load-bearing input to **decision #13** (pitch staged-options reframe) and to the **iapetus tranche-1 expected-loss number** — does the $80M expected-loss anchor survive when each per-sample trajectory is regime-classified?

---

## Pre-registered hypotheses (worker's honest predictions)

| # | Hypothesis | Predicted range | Falsification band |
|---|---|---|---|
| H1 | The run.py extension is ~30-60 lines of additive code. The Monte Carlo loop's internal state already computes per-mission cumulative-NPV; the extension is to capture-and-emit, not to re-derive. | 30-60 line diff. | H1 falsified if the extension exceeds 100 lines or requires re-running with a different RNG seed. |
| H2 | Of 100 representative samples, between 25 and 50 percent are MOMENTUM-DEPENDENT (Hamiltonian sustainability < 0.3). The Monte Carlo aggregate shows median NPV near the break-even line; the underlying trajectories are likely heterogeneous in their accumulation pattern. | 25-50% MOMENTUM-DEPENDENT. | H2 falsified if <10% or >70% are MOMENTUM-DEPENDENT. |
| H3 | Heterogeneous-cadence samples have a HIGHER fraction of MOMENTUM-DEPENDENT trajectories than homogeneous-cadence samples (chunk-shrinking concentrates revenue in early-large-chunk missions). | Heterogeneous MOMENTUM-DEPENDENT fraction is 5-20 pp higher than homogeneous. | H3 falsified if the two regimes have the same or inverted fraction. |
| H4 | The conservation test produces meaningful labels at N=10 (above skill caveat threshold). Most NPV-positive samples produce DISSIPATIVE slopes; most NPV-negative samples produce ENERGY-INJECTING. | Conservation label correlates with NPV-positive outcome at AUC > 0.7. | H4 falsified if the conservation label has no useful predictive relationship to outcome. |
| H5 | Hamiltonian Layer 1 produces decision-actionable findings on this data. The output gives the project owner a defensible answer to "is the program-NPV-positive verdict robust accumulation or rare-windfall?" beyond what the Monte Carlo aggregate alone tells. | Reading-level: Hamiltonian Layer 1 surfaces a finding the aggregate-summary does not. | H5 falsified if Hamiltonian output adds no information beyond `het_pct_npv_positive`. |
| H6 (load-bearing reading) | Het-cadence is more MOMENTUM-DEPENDENT than homogeneous-cadence; the 46.26 percent NPV-positive figure for heterogeneous is therefore lower-quality than the 50.83 percent for homogeneous in a way the aggregate does not show. This is consistent with rhea's existing verdict that chunk-shrinking loses NPV in every regime tested — but adds new evidence on _how_ it loses (concentration in fewer windfall trajectories). | Reading-level: het-cadence's NPV-positive figure is concentration-driven, not accumulation-driven. | H6 falsified if H3 falsifies. |

---

## Out of scope

- Modifying the underlying NPV computation. This round captures-and-emits what rhea already computes; it does not change the economics model.
- Running a NEW Monte Carlo with different parameters. Use the same parameter grid rhea already runs on; just emit the trajectories.
- Authoring the Hamiltonian invocation itself. The skill exists at `~/.claude/commands/decision-framework/hamiltonian.md`; this round produces the data the skill consumes, not the skill output.
- Cross-skill composition (Hamiltonian Layer 2, dual-matrix on regime split). Those are follow-ons after Layer 1 produces a regime classification per sample.

---

## Inputs to acquire (reading order)

1. `water-prop/rounds/R_heterogeneous_cadence/run.py` (the 725-line existing run.py to extend)
2. `water-prop/rounds/R_heterogeneous_cadence/results/het_cadence_summary.json` (existing output structure)
3. `~/.claude/commands/decision-framework/hamiltonian.md` (the skill that consumes the output)
4. `water-prop/rounds/R_LEO_water_demand_curve/run.py` and `results/demand_curve_summary.json` (clearing-price model that rhea uses; understand the cashflow inputs)
5. Locked beliefs for context: `5535179f` (three engineering bets), `c95626970c` (L0-04 = 25 t provisional)

---

## Deliverables (in commit order)

1. `STUDY.md` — pre-registered hypotheses H1-H6 frozen before the extension lands.
2. Run.py extension commit (additive; preserves existing summary output).
3. README amendment documenting the new flag + output schema.
4. `results/per_sample_trajectories.json` (re-running Monte Carlo with extension; ~100 samples).
5. Hamiltonian Layer 1 invocation on the trajectory data; output saved to `results/hamiltonian_layer1_per_sample.json` with per-sample regime classification + sustainability + conservation labels.
6. Aggregate Hamiltonian summary (`RESULTS.md`): regime distribution across samples; fraction MOMENTUM-DEPENDENT per cadence-class (heterogeneous vs homogeneous); H6 verdict.
7. `READING.md` — load-bearing reading; cross-reference to matrix decision #13 (iapetus tranche-1 expected-loss number) and existing rhea R-heterogeneous-cadence verdict.
8. Handoff doc to orchestrator (`~/.claude/handoffs/iceberg-<worker>-<date>-rhea-per-mission-output-extension.md`).

---

## Suggested worker

Any moon. Best fit: comfortable reading rhea's existing run.py + understanding the Monte Carlo internals + light Python extension work. **Rhea** is the natural fit (re-spawn from existing iceberg-rhea-2 branch context). Mimas would also fit (already extended Python AST + framework-internal work in R-shared-physics-audit).

Estimated worker time: 1-2 hours for extension + Monte Carlo re-run + Hamiltonian invocation + READING.md.

---

## Cross-references

- `~/.claude/commands/decision-framework/hamiltonian.md` — the skill this round produces data for.
- `water-prop/rounds/R_heterogeneous_cadence/` — existing rhea round being extended.
- Matrix decision #13 (pitch staged-options reframe; tranche-1 expected-loss number) — load-bearing on this round's H6 verdict.
- iapetus R-staged-options-with-technology-gates (`7ffc1e6`) — produces the $80M tranche-1 expected-loss anchor; this round's output stress-tests its accumulation-vs-momentum dependence.
- Mimas R-shared-physics-audit READING.md — similar precedent for extending existing rhea code without changing the underlying model.
