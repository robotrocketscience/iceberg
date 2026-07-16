# R-variant-B-100t-resizing — does chunk reduction to 100 tonnes per mission rescue Variant B without aerocapture?

**Status:** scope, pre-study. Authored by Saturn (orchestrator) on 2026-05-15 late evening after hyperion's R-variant-B-impulsive-vs-continuous (commit `daaf522`) surfaced chunk reduction as a third amendment path.

**Trigger and standing:** under first-principles continuous-thrust accounting at chunk 200 tonnes (L1-007 cap), the 500-kilowatt-electric all-electric inbound cell collapses to 0.0 tonnes delivered (Variant A, hyperion's last round). Hyperion suggested chunk reduction as a path-3 amendment without computing it. This round computes it.

The hypothesis is that smaller chunks reduce the inbound integrated delta-velocity disproportionately (Tsiolkovsky mass-ratio is bounded by chunk mass), potentially re-opening the cell at 100-tonne chunks even without aerocapture.

## Question this round answers

1. **At chunk = 100 t, 500-kilowatt-electric all-electric inbound, MARVL-anchored mass, no aerocapture (Variant A architecture):** what is the integrated continuous-thrust inbound delta-velocity, round-trip time, and delivered fraction? Same accounting regime as hyperion R-variant-B-impulsive-vs-continuous, just with chunk_t = 100 instead of 200.
2. **Does the cell close inside L0-05's 15-year ceiling at chunk = 100 t?** Hyperion's chunk-200 result was 16.92 years (over by 1.92 years). Smaller chunk should improve round-trip; question is whether enough to close.
3. **What is the optimum chunk size** (mass that maximises round-trip closure under L0-05 at 500-kilowatt-electric without aerocapture)? Sweep chunk from 50 to 200 tonnes at 25-tonne steps; find the round-trip minimum and the closure boundary.
4. **At the closing chunk size (if any), what is the delivered-mass-per-mission?** This is the input to R-variant-B-recovery-paths-economic for path 3.
5. **Is the 500-kilowatt-electric optimum reactor-power finding (hyperion R-variant-B-500kWe-sizing) preserved at the smaller chunk?** Tug mass scales with reactor power; smaller chunk may move the optimum.

## Pre-registered prediction (sketch — full hypothesis grading in STUDY.md when round runs)

**Aggregate:** chunk 100 t under Variant A closes L0-05 marginally (round-trip 13.5–14.5 years), delivering 25–40 tonnes per mission. The optimum reactor power at chunk 100 t shifts to ~250 kilowatt-electric per hyperion's rule-of-thumb (~0.45 × M_c kilowatt-electric per tonne). Delivered-mass-per-mission at chunk 100 t is LOWER than path-1 aerocapture-Variant-C (32.1 tonnes-per-ship at chunk 200 t), so path 3 is dominated by path 1 on raw delivered mass. The case for path 3 is regulatory (L0-05 strict, no soft margin needed) and architectural (no aerocapture R&D dependency).

**Falsification bands and sub-claims:**

- Chunk 100 t Variant A round-trip: 13.5–14.5 years. Falsified if > 15 yr (cell collapses even at smaller chunk) or < 12 yr (smaller chunk relaxes round-trip more than predicted).
- Chunk 100 t Variant A delivered-mass: 25–40 tonnes-per-ship. Falsified if < 15 t (smaller chunk loses too much) or > 60 t (smaller chunk over-performs — flag for sign error).
- Optimum reactor power at chunk 100 t: 200–300 kilowatt-electric. Falsified if outside that band.
- Path-3 vs path-1 dominance on delivered mass: path 1 (32.1 t) > path 3. Falsified if path 3 delivers more.
- Path-3 marginal internal-rate-of-return: 0–3 percent (sub-sovereign-bond, similar to or worse than path 1 without aerocapture). Computed in R-variant-B-recovery-paths-economic, not here.

## Method sketch

1. **Run hyperion's R-variant-B-impulsive-vs-continuous run.py** with `chunk_t = 100`, all other parameters held at the worker's defaults. This is the single most important deliverable; everything else is sweeps around it.
2. **Sweep chunk from 50 to 200 t in 25-tonne steps** under Variant A (no recovery). Output: round-trip vs chunk, delivered-mass vs chunk.
3. **Find round-trip minimum and closure boundary.** The chunk at which round-trip first goes under L0-05 is the closure boundary; the chunk that maximises (delivered-mass × on-time-delivery-credit) is the operating optimum.
4. **Reactor-power optimum sweep at chunk 100 t.** Run hyperion's R-variant-B-500kWe-sizing run.py with `chunk_t = 100`, sweep reactor 100–700 kilowatt-electric in 100-kilowatt-electric steps. Output: optimum reactor power.
5. **Cross-check the rocket-equation-balance rule** (optimum reactor power ≈ 0.45 × M_c kilowatt-electric per tonne). Round-2 verifies whether the rule holds at the smaller chunk.
6. **Deterministic run.py per project convention.**

## What this round does NOT cover (deferred)

- Programmatic-risk overlay and marginal-internal-rate-of-return computation under path 3 — owned by R-variant-B-recovery-paths-economic.
- Operational consequences of doubling per-cadence-window mission count (50 t / mission instead of 200 t / mission halves throughput at the same launch cadence; recovering throughput requires doubling cadence or doubling chunk-count-per-mission — neither addressed here).
- Whether the surviving-cell verbal description ("500-kilowatt-electric chemical-kick + electric-inbound at 200 tonne chunk") needs verbatim restatement throughout the matrix and pitch under path 3. That's an orchestrator amendment, not a propulsion round.

## Cross-references

- `water-prop/rounds/R_variant_B_impulsive_vs_continuous/STUDY.md` + `run.py` — hyperion's just-shipped round. Provides the run.py this round reuses.
- `water-prop/rounds/R_variant_B_500kWe_sizing/STUDY.md` + `run.py` — hyperion's reactor-power-optimum round.
- `water-prop/rounds/R_inbound_dv_continuous_thrust/STUDY.md` — titan's underlying delta-velocity decomposition.
- `water-prop/rounds/R_variant_B_recovery_paths_economic/SCOPE.md` — the bake-off round that consumes this round's delivered-mass-per-mission output as input for path-3 marginal-internal-rate-of-return.

## Deliverables

- `water-prop/rounds/R_variant_B_100t_resizing/STUDY.md`
- `water-prop/rounds/R_variant_B_100t_resizing/run.py`
- `water-prop/rounds/R_variant_B_100t_resizing/results/`
- `water-prop/RUNNING_DOC.md` round-status entry
- Handoff at `~/.claude/handoffs/iceberg-WORKER-NAME-YYYYMMDD.md`

## Sequencing note

This round can run before, in parallel with, or after R-variant-B-recovery-paths-economic. The bake-off needs this round's delivered-mass output to compute path-3 marginal-internal-rate-of-return; the bake-off can also run path-3 itself with chunk = 100 t as a single line item if no separate R-variant-B-100t-resizing worker is assigned. Project owner's call.
