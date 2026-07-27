# R-multi-chunk-per-mission — STUDY (execution 2, pre-registration)

**Worker:** worktree-172651, 2026-07-26 latest+29d (owner: "do them all").
SCOPE: `../SCOPE.md` (latest+29c). Prior execution adjudicated in `../README.md`
(titan-2 2026-05-16: superseded-as-economics, retained-as-mechanism-survey).
Tier 1/1.5, honest-tier labeled (Deviation 8).

## Hypotheses

| # | Hypothesis | Gate | Prediction |
|---|---|---|---|
| H-M1 | Re-rendezvous between ring chunks costs ≤ 6 months and ≤ 50 m/s per additional chunk at spacings 10–1,000 km | either exceeded falsifies | Holds easily — Hill-regime transfers are m/s- and weeks-class; capture OPERATIONS set the time |
| H-M2 | Joint capture reliability ≥ 0.80 at N ≤ 3 at the optimized harpoon point (0.961/capture, rhea-5); fails at any N ≥ 2 on the prior-mean 0.549 | numbers | Both halves hold — multi-chunk makes capture reliability THE driver, re-elevating the bench items per the owner's decision-6 caveat |
| H-M3 | Aggregate containment is per-chunk: N chunks of m/N have higher Round-J ceilings than one m-chunk (m^(−1/6)) | ceiling comparison | Holds analytically |
| H-M4 | Despin budget sub-1% of mission Δv for slow rotators; 0.28-rpm fast-rotator corner stays open | Tier-1 angular-momentum ledger | Holds, corner flagged |
| H-M5 | Corridor stays closed (≥ 30 t) with per-chunk overheads: 350 kg refurb/chunk (declared prior) + 0.25 yr ops/additional chunk | corridor cell dies falsifies | Holds — ≤ 2 t and ≤ 1 yr vs 100+ t and 6-yr slack |
| H-M6 | Aggregate 1,000–2,000 t reaches the 209-t sovereign-hurdle delivery class, NOT the 691-t corporate hurdle | delivered ≥ 209 t at ≤ ×32 | **Half-falsified expected** — best observed 169.8 t at ×32; economics round adjudicates |

## Method

(1) Hill re-rendezvous: orbit-raise Δv ≈ (v/2a)·Δa + phasing time at
a = 100,000 km, Δa ∈ {10, 100, 1,000 km}. (2) Reliability ledger: joint P for
N ∈ {2,3,5} at 0.961 / 0.549 vs L0-10 ≥ 0.80. (3) Corridor grid re-run
(saturn_water_v2 corridor posture, stage 900 s, non-aero, optimal-f from
R-per-phase-propellant-fidelity) with `bus_mass_floor_kg = 2000 + 350·N`,
N = ceil(aggregate/400 t), aggregate ∈ {500, 1,000, 2,000 t}; round-trip
+0.25·(N−1) yr post-hoc vs the 25-yr waiver. (4) Lesson-25 ledger walk at the
overhead-charged 200 kWe / 1,000 t cell. Declared priors: 350 kg/chunk refurb,
0.25 yr/chunk ops, 400-t average chunk (inside the 482-t cap).

## Deviations

- D-1: reliability numbers are Tier-1.5 posteriors + declared priors, not
  measurements (bench items remain demonstrator-track).
- D-2: re-rendezvous is closed-form Hill, no GNC sim.
