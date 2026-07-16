# R-chunk-capture-contact-fidelity — Tier 2 + Tier 3 contact-fidelity Monte Carlo for both harpoon and ram-scoop

**Status:** scope, pre-study. Authored by Saturn (orchestrator), 2026-05-26 latest+25.
**Predecessors:** R-chunk-capture-monte-carlo Tier 1 closed-form (latest+23); R-ramscoop-foundational-premise-revisit (rhea-3, latest+23); R-vehicle-mass-closure-refactor (titan-6, latest+23).

## Premise

R-chunk-capture-monte-carlo Tier 1 closed-form Monte Carlo (Saturn orchestrator, in-session 2026-05-26) produced posterior medians on single-pass capture probability for three architectures:
- Single-chunk harpoon: 0.365 [0.136, 0.497]
- Ram-scoop residence-class: 0.405 [0.327, 0.491]
- Everting-sleeve active enclosure: 0.246 [0.130, 0.418]

Rhea's R-ramscoop-foundational-premise-revisit coupled Tier 1 capture posteriors with chunk-as-propellant-tank delta-velocity bookkeeping (titan-2 R-conops-chunk-vs-ram-scoop continuous-thrust). H1 falsified — ram-scoop's Tier-1 capture lead does NOT survive delta-velocity bookkeeping; harpoon delivers 4.3x more mass.

**Project-owner direction 2026-05-26: contact-fidelity follow-on carries BOTH harpoon AND ram-scoop in parallel** rather than retiring one at Tier 1. Higher cost (~36-72 hours MacBook); produces defensible side-by-side artifact regardless of how titan's refactor + fidelity refinement shifts absolute numbers. Everting-sleeve was retired pre-contact-fidelity per H7 falsification + 200-tonne-scale eversion-kinematics flight-heritage gap.

Tier 1 stayed open on H3 (n ~ 1200 contact-fidelity Bernoulli runs gives +/- 0.02 binomial half-width), H4 (contact-engine choice — MuJoCo vs Drake — doesn't move posterior by more than 0.05), and H5 (closed-form over-estimates relative to contact fidelity). This round tests all three for both architectures.

## Pre-registered hypotheses

H1 (per architecture, two instances): **A binomial credible interval of half-width at most 0.02 at the 95 percent level requires approximately 1200 contact-fidelity Bernoulli runs at the operating point.** Falsified if the half-width target requires more than 5000 runs (would imply the outcome is not effectively Bernoulli).

H2 (per architecture): **The contact-engine choice (MuJoCo as primary vs Drake as cross-check) does not move the posterior median by more than 0.05.** Falsified if cross-engine A/B at n=200 each shows posterior medians separated by more than 0.05. If falsified, the contact-engine choice itself becomes a project-owner decision point.

H3 (per architecture; load-bearing): **The closed-form product decomposition over-estimates joint capture success relative to the contact-fidelity Monte Carlo by at least 0.05.** Reasoning: closed-form products treat stages as independent, but failure modes co-vary (high spin both raises catch failure and raises containment failure). Falsified if contact-fidelity result is within 0.02 of the closed-form result.

H4 (cross-architecture; project-owner load-bearing): **Harpoon's relative lead over ram-scoop in delivered mass (rhea's 4.3x at Tier 1) is preserved at contact fidelity, OR it inverts.** The Tier 1 relative ranking is the load-bearing matrix input on capture-architecture. Falsified if the contact-fidelity posterior medians for harpoon and ram-scoop overlap within their 90 percent credible intervals (i.e., the ranking is not statistically separable).

H5 (sensitivity preservation): **The Tier 0.5 spin-rate prior dominance (per Tier 1 H2 reading for harpoon) is preserved at contact fidelity.** Tests whether the contact-fidelity sampler honors the Cassini-anchored slow-spin prior the same way the closed-form did. Falsified if spin-rate sensitivity (total-order sensitivity index at contact-fidelity) shifts by more than 0.20 from the Tier 1 closed-form value.

H6 (load-bearing): **At contact fidelity, at least one of the two architectures achieves a posterior median of capture probability times delivered-mass fraction (per rhea's coupled model) above the L0-04 = 25 t threshold at any chunk-mass / power-class combination.** This re-tests R-chunk-capture-monte-carlo's H6 + rhea's H3 under contact-fidelity. Falsified if both architectures stay below 25 t delivered.

## Methodology

### Contact-fidelity tooling

**Primary engine: MuJoCo.** Per wondering precedent (Chen et al. 2024 J. Spacecraft & Rockets tether-net Monte Carlo). Build a parameterised contact-event model per architecture:

- **Harpoon model:** rigid spacecraft + projectile + chunk. Hertz contact model on first impact; locking mechanism modeled as a kinematic constraint after grip-time threshold. Failure modes: glance-off (no penetration), tear-out (penetration but constraint fails to lock), tether-snap (constraint locks but post-impulse load exceeds tether limit).
- **Ram-scoop model:** rigid spacecraft + deployable aperture (parameterised as a Hertz-contact ring with adjustable compliance) + flow-through chunks (10-100 chunks per Monte Carlo run, sampled from a power-law size distribution per Cuzzi 2010). Failure modes: bounce-out (chunk exits aperture before cinch), drag-overload (aperture-frame tear under cumulative chunk-stream momentum), cinch-fail (drawstring actuator unable to close on bulk mass).

**Cross-check engine: Drake.** Same model topology, different contact solver (Drake's Newton solver on complementarity vs MuJoCo's convex-relaxed). Used only at the operating point for H2 cross-engine A/B.

**Outer loop: Basilisk.** Hands state to MuJoCo at "first contact" and resumes after capture-mechanism stabilises. The Basilisk-MJScene bridge is documented as [BETA]; expect to fall back to manual state hand-off at the contact instant if MJScene proves unreliable.

### Sweep design

**Tier 2 — Morris screening + Polynomial Chaos Expansion per architecture.**
- Morris elementary effects: r=10 trajectories over 8 axes (harpoon) or 10 axes (ram-scoop), ~90-110 runs per architecture. Drops second-order axes from the Tier 3 fidelity work.
- Polynomial Chaos Expansion on surviving 4-5 axes: ~500 runs per architecture. Output: total-order sensitivity indices per axis per architecture.

**Tier 3 — defensible binomial posterior per architecture.**
- n=1200 contact-fidelity Bernoulli runs at the operating point identified by Tier 2 (chunk mass + power class + thrust where the closed-form posterior median was highest). Output: posterior median + 95 percent credible interval per architecture.

**Cross-architecture comparison.**
- Compute delivered-mass posterior per architecture by applying titan-2 R-conops-chunk-vs-ram-scoop delta-velocity bookkeeping to each architecture's contact-fidelity capture-probability posterior (matches rhea's coupled-model methodology). Output: side-by-side delivered-mass posteriors with relative-ranking confidence.

### Operating point — gated on titan's refactor

The "operating point" for Tier 3 should be the cell that maximises capture-probability posterior median UNDER THE CLOSED-LOOP FRAMEWORK. Coordinate with titan-7's R-vehicle-mass-fidelity-refinement: ideally Tier 3 runs after the fidelity refinement lands so the contact-fidelity numbers are anchored on self-consistent vehicle mass and per-phase propellant fraction. If titan-7's round is slower than this one, run Tier 3 on the closed-loop framework's most-permissive cell and explicitly flag the result as pending-refinement.

## Deliverables

1. This SCOPE.md.
2. STUDY.md with H1-H6 pre-registered per architecture.
3. `mujoco_harpoon.py` + `mujoco_ramscoop.py` — contact-fidelity models per architecture.
4. `tier2_morris_pce.ipynb` (papermill-pinned) — screening + Polynomial Chaos Expansion per architecture.
5. `tier3_binomial.ipynb` (papermill-pinned) — defensible binomial posterior per architecture, ~1200 runs each.
6. `cross_engine_ab.ipynb` — MuJoCo vs Drake A/B at n=200 each per architecture.
7. `delivered_mass_coupling.py` — applies rhea's delta-velocity bookkeeping to contact-fidelity posteriors.
8. FINDINGS.md with per-architecture verdicts on H1-H6 + cross-architecture comparison + matrix amendment specification.

## Out of scope

- Everting-sleeve architecture (retired pre-contact-fidelity per H7 falsification).
- Vehicle-mass closure (depends on titan-7's R-vehicle-mass-fidelity-refinement).
- New uncertainty axes beyond the eight Tier 1 already used (chunk mass, spin rate, surface friction, approach velocity, sensor noise, contact geometry, catcher compliance, controller delay).
- Re-deriving the Tier 0.5 Cassini-anchored spin prior (preserved as Tier 1 product).

## Predecessor work

- R-chunk-capture-monte-carlo Tier 1 (Saturn orchestrator, latest+23): closed-form posteriors per architecture.
- R-ramscoop-foundational-premise-revisit (rhea-3, latest+23): coupled delta-velocity bookkeeping; H1 falsified ram-scoop's lead.
- Tier 0.5 spin-rate prior (Saturn orchestrator, latest+23): Cassini-anchored decameter-marginal log-uniform 0.0005-0.05 rpm.
- R-vehicle-mass-closure-refactor (titan-6, latest+23): closed-loop dry-mass framework.
- Project-owner direction 2026-05-26: carry both architectures in parallel.

## Priority

**MEDIUM-HIGH.** Gates the matrix's design-axis 19 (capture architecture) state-of-record. The Tier 1 ranking (harpoon-leads-after-delta-velocity) is the current operative reading; contact-fidelity confirms or revises.

Independent of R-vehicle-mass-fidelity-refinement at the capture-probability level. Coupled to it at the delivered-mass level — wait for fidelity refinement before publishing absolute delivered-mass numbers, but capture-probability posteriors can land before.

## Suggested worker

hyperion-3 — multi-round Bayesian-synthesis experience, recent A14 engineering-decomposition work, MuJoCo/Drake comfort plausible. Alternative: titan-7 if their fidelity-refinement round finishes first (unlikely given the multi-day budget).
