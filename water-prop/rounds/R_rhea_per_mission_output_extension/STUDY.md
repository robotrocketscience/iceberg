# Round — rhea per-mission output extension: emit per-sample cumulative-NPV trajectories + Hamiltonian Layer 1

**Status:** pre-result (H1–H6 frozen before the extension lands and before Hamiltonian Layer 1 runs).

**Round directory:** `water-prop/rounds/R_rhea_per_mission_output_extension/`.

**Owning session:** rhea (re-spawn), branch `iceberg-rhea-4` (based on `origin/main` 3e0ad81 — this round depends only on integrated work: the het-cadence `run.py` and this round's SCOPE.md, both on main).

**Date:** 2026-05-26.

**Predecessor / inputs:**
- rhea R-heterogeneous-cadence (`2e85d4f`, integrated latest+7) — the 10,000-sample Monte Carlo on per-mission economics being extended. Existing aggregate output: `het_pct_npv_positive` 46.26%, `hom_pct_npv_positive` 50.83%.
- `/decision-framework:hamiltonian` skill (`~/.claude/commands/decision-framework/hamiltonian.md`) — Layer 1 regime diagnostics (kinetic/potential decomposition, conservation test, sustainability ratio). N<10 trajectories are noise-dominated per the skill caveat.
- SCOPE: `SCOPE.md` (this dir) — authored by Saturn latest+17.

## Question

The het-cadence Monte Carlo reports only aggregate program-NPV statistics. It cannot answer **whether the program-NPV-positive verdict is robust accumulation across missions or rests on a single windfall mission** — that requires the per-mission cumulative-NPV *trajectory* per sample, run through Hamiltonian Layer 1. This round emits those trajectories (additively, without changing the existing aggregate) and classifies each sample's regime.

## Coupled approach

1. **Per-mission decomposition.** The existing NPV evaluators return only PV totals. I add a `per_mission_trajectory(...)` that decomposes the same cashflows: each mission contributes `−PV(ship capital at launch year) + PV(revenue at delivery year)`, gated by `p_success` for the deferred fleet in Regime R. Cumulative-sum over missions (launch order) gives the trajectory. **Validation gate:** sum of per-mission net PV must reconcile to the aggregate `npv_regime_*` to < $0.01M, else abort.
2. **Identical clearing prices.** Trajectory capture replays the *same seeded* lognormal clearing-price draws the Monte Carlo uses (`Random(SEED)` for Starship $/kg, `Random(SEED+1)` for markup), so trajectory sample i uses the same clearing price as MC sample i. The existing aggregate path is left byte-for-byte unchanged (re-verified by diffing `het_cadence_summary.json`).
3. **100 representative samples**, balanced 50 heterogeneous (Regime R, chunk_1=50, p=0.9) + 50 homogeneous (Regime D, chunk_1=200), from the first 50 MC samples (both cadence-classes per sample).
4. **Hamiltonian Layer 1** (skill Steps 1–5, implemented in code for batch over 100 trajectories; linear q-space since NPV is additive/signed): per-sample sustainability ratio + label, conservation slope + label, regime distribution. Aggregate by cadence-class.

## Pre-registered hypotheses (frozen from SCOPE; predictions are the analyst's)

| # | Hypothesis | Falsification band | rhea prediction |
|---|---|---|---|
| H1 | Extension is ~30–60 lines additive; no RNG-seed change. | >100 lines or different seed. | HELD (~40–80 lines incl. trajectory decomposition; same seed). |
| H2 | 25–50% of 100 samples are MOMENTUM-DEPENDENT (sustainability < 0.3). | <10% or >70%. | **AT RISK of falsifying LOW.** Fleet missions 2..N are identical baseline; per-mission contributions differ only by discounting + Wright learning, so trajectories may be smooth → mostly ACCUMULATION → <10%. The het mission-1 (smaller, earlier delivery) is the only "different" step. |
| H3 | Heterogeneous MOMENTUM-DEPENDENT fraction is 5–20 pp higher than homogeneous. | same or inverted. | HELD direction (het has the odd-one-out mission 1; hom is uniform), magnitude uncertain. |
| H4 | Conservation label correlates with NPV-positive outcome at AUC > 0.7. | no useful relationship (AUC ≤ ~0.6). | HELD — DISSIPATIVE (gains accumulate, V pulls H down) should track NPV-positive. |
| H5 | Hamiltonian Layer 1 surfaces a finding the aggregate-summary does not. | adds nothing beyond `het_pct_npv_positive`. | HELD — accumulation-vs-momentum character is not in the aggregate. |
| H6 (load-bearing) | Het-cadence's 46.26% NPV-positive is **concentration-driven**, not accumulation-driven; lower-quality than hom's 50.83% in a way the aggregate hides. | falsified if H3 falsifies. | Held conditional on H3; reported honestly either way. |

## Method

1. `STUDY.md` (this file) — freeze H1–H6.
2. Extend `R_heterogeneous_cadence/run.py` additively: `per_mission_trajectory()`, `capture_trajectories()`, `--emit-trajectories` CLI flag. Preserve aggregate output.
3. Run with `--emit-trajectories` → `R_heterogeneous_cadence/results/per_sample_trajectories.json`. Verify `het_cadence_summary.json` unchanged.
4. `hamiltonian_layer1.py` (this dir) — implements skill Layer 1 over all 100 trajectories → `results/hamiltonian_layer1_per_sample.json`.
5. `RESULTS.md` — regime distribution, MOMENTUM-DEPENDENT fraction per cadence-class, H1–H6 verdicts.
6. `READING.md` — load-bearing reading; cross-reference matrix decision #13 (iapetus tranche-1 expected-loss) + existing rhea het-cadence verdict.

### Validity caveats

- Additive extension only; the underlying NPV/economics model is **not** modified. This round captures-and-emits what rhea already computes.
- Hamiltonian Layer 1 is **descriptive, not predictive** (skill caveat 1). Regime labels characterise the trajectory; they do not forecast.
- Trajectory length N is whatever the schedule produces (het Regime R ≈ 27 missions, hom Regime D ≈ 52 missions — both well above the N≥10 skill threshold). Report N per class.
- Linear q-space (NPV is additive and crosses zero); log-space would be wrong here (skill caveat 5).
- Workers do not edit shared docs; RESULTS/READING specify orchestrator follow-ups.
