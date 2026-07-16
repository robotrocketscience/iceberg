# R-heterogeneous-cadence — run.py usage

Original round (rhea, 2026-05-15): does a fast-small mission 1 followed by larger-slower
missions 2..N improve program NPV vs the homogeneous Variant B baseline? See `STUDY.md`.

## Default run (aggregate summary)

```bash
water-prop/.venv/bin/python water-prop/rounds/R_heterogeneous_cadence/run.py
```

Writes `results/het_cadence_summary.json` (cross-checks, H1–H8 grades, H-5 Monte Carlo
aggregate: `het_pct_npv_positive` 46.26%, `hom_pct_npv_positive` 50.83%). Unchanged behaviour.

## Per-sample trajectory emit (R-rhea-per-mission-output-extension, 2026-05-26)

```bash
water-prop/.venv/bin/python water-prop/rounds/R_heterogeneous_cadence/run.py --emit-trajectories
# optional: --n-per-class N   (trajectories per cadence-class; default 50 => 100 total)
```

**Additive** — does not change `het_cadence_summary.json` (verified byte-identical). Writes
`results/per_sample_trajectories.json`: per-sample per-mission cumulative-NPV trajectories for
the first `--n-per-class` Monte-Carlo samples, balanced across the two cadence-classes:

- **het** = Regime R, chunk_1 = 50 t, p_success = 0.90 (heterogeneous cadence)
- **hom** = Regime D, chunk_1 = 200 t (homogeneous baseline)

both at WACC 3% / LR 15%, with the clearing price from R-LEO-water-demand-curve. Trajectory
sample i replays the **identical** seeded clearing-price draw as Monte-Carlo aggregate sample i.

### Output schema (`per_sample_trajectories.json`)

Top level: `n_records`, `reconciliation_max_abs_err_M` (per-mission sum vs aggregate
`npv_regime_*`; gated < $0.01M), `schema`, and `trajectories` (list). Each trajectory record:

| field | meaning |
|---|---|
| `sample_id` | Monte-Carlo sample index (0-based) |
| `cadence_class` | `"het"` or `"hom"` |
| `regime` | `"R"` or `"D"` (Monte-Carlo regime label) |
| `clearing_per_kg`, `rev_per_tonne_M` | sampled clearing price for this sample |
| `chunk_schedule` | per-mission chunk mass (t), launch order |
| `n_missions` | trajectory length N |
| `per_mission_cumulative_npv_M_usd` | **value series for Hamiltonian Layer 1** (signed, discounted, cumulative) |
| `per_mission_revenue_M_usd`, `per_mission_cost_M_usd` | raw nominal per-mission revenue / Wright unit cost |
| `per_mission` | full per-mission records (launch/delivery year, gate, net PV, cumulative) |
| `final_program_npv_M_usd` | reconciles to `npv_regime_*` aggregate |

### Hamiltonian Layer 1 invocation

```
Trajectory data source: water-prop/rounds/R_heterogeneous_cadence/results/per_sample_trajectories.json
  time_field: "mission_number"   value_field: "cumulative_npv_M_usd"   log_space: false
```

Batch analysis over all 100 trajectories is implemented in
`water-prop/rounds/R_rhea_per_mission_output_extension/hamiltonian_layer1.py`
(skill Steps 1–5); see that round's `RESULTS.md` / `READING.md` for the verdict.
