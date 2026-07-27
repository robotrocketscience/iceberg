# R-multi-chunk-per-mission — SCOPE (pre-registration; RUN GATED on project-owner go)

**Authorized:** project owner, 2026-07-26 latest+29b ratification pass
(decision 3: "Authorize SCOPE" — pre-registration only; execution awaits a
separate go). **Status: scope, pre-study.**

## Why now (what changed since this round was queued ~2026-05-15)

Originally queued as the only path past the 482-t B-ring single-chunk cap to
the 691-t corporate-growth hurdle — an economics upside question. As of
latest+29c it is **load-bearing for the only corridor that closes the 30-t
commercial floor under honest resolved physics**: the electrolysis-fed
nuclear-thermal departure needs **500–1,000 t of harvested water per mission**
(self-consistent grid: 32.6 t delivered at 500 t harvest / 150 kWe / ×16
launch; 89.2 t at 1,000 t / 200 kWe), and R-departure-anchor-resolution killed
the electric alternative (integrated 22.5–24.2 km/s departure). Multi-chunk is
no longer optional upside; it is the capture-side half of the surviving
corridor.

## Question

Can a single vehicle capture, aggregate, and process 2–5 chunks (aggregate
500–2,000 t) per mission within the 25-yr waiver ceiling, at a reliability and
mass cost that keeps the corridor closed?

## Hypotheses (candidate set — STUDY will finalize gates)

| # | Hypothesis | Sketch of gate |
|---|---|---|
| H-M1 | Sequential capture of N ≤ 5 chunks costs ≤ 6 months per additional chunk (re-rendezvous within the ring at mm/s relative velocities) | dwell model vs the electrolysis production dwell (~2.7 yr at 200 kWe) — captures can overlap production |
| H-M2 | Repeat-capture reliability: joint P(all N captures) stays ≥ the single-capture prior at N ≤ 3 with mechanism refurbishment margins (harpoon reload / bag re-rig) | decomposition + rhea-5 posterior reuse; links to the demonstrator-track bench items (cinch reliability, porous-ice penetration) |
| H-M3 | Aggregate containment at 500–1,000 t: Round J ceilings scale m^(−1/6) per chunk, not per aggregate — N separate contained chunks avoid the single-500-t-bag penalty | mass-scaled ceiling table extension |
| H-M4 | Despin/handling budget for N chunks does not exceed the RCS budget (links to the 115637 despin follow-on for the 0.28-rpm fast-rotator corner) | Tier-1 angular-momentum ledger |
| H-M5 | The corridor stays closed with multi-chunk overheads charged (capture-mechanism refurbishment mass, inter-chunk transit propellant, aggregation structure) — framework encoding via a per-chunk overhead term in P3 + a chunk-count axis | closed-loop sweep with `n_chunks` axis; lesson-25 ledger walk mandatory (new closure surface) |
| H-M6 | 1,000–2,000 t aggregate unlocks the 691-t corporate-growth hurdle delivery class (169.8 t at ×32/500 kWe already observed) | economics re-read only; no new financial model |

## Method sketch

Tier 1/1.5 desk: (1) ring re-rendezvous Δv/time model between chunk sites
(Hill-regime drift, mm/s class); (2) reliability decomposition anchored on the
Tier-1.5 capture posteriors; (3) framework encoding: `n_chunks` param axis in
phase 3 with per-chunk time/mass/reliability overheads, aggregate payload
feeding the v2 departure; (4) re-run the self-consistent corridor grid with
overheads charged; (5) mandatory single-path mass-ledger walk (lesson 25).

## Deviations (anticipated)

- Mechanism-reliability numbers remain bench-gated (demonstrator-track per the
  latest+29b confirmation); this round carries them as declared priors, not
  measurements.
- No MuJoCo/contact fidelity — Tier 1/1.5 only, honest-tier labeled
  (Deviation 8).

## Run gate

Execution requires explicit project-owner go. Estimated effort: one session
(the framework hooks and the corridor grid already exist; the new physics is
the re-rendezvous model and the overhead terms).
