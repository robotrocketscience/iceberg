# R-l0-relaxation-envelope — does maximum spirit-preserving L0 relaxation bring back commercial closure?

**Status:** scope, pre-study. Authored by Saturn (orchestrator), 2026-05-26 latest+25.
**Predecessor:** project-owner question 2026-05-26 (how would we relax L0 requirements within the spirit of the mission); Tier 1 sanity sweep already run (`FINDINGS.md` at latest+25 reports 0 paths arrive at LEO depot at all).
**Sequencing dependency:** **gated on R-vehicle-mass-fidelity-refinement completion** — without the per-phase propellant-fraction derivation (titan D5), the closed-loop framework's bottleneck is upstream of every L0 the round would test.

## Premise

Project-owner question 2026-05-26: which L0 requirements can be relaxed while staying within the spirit of the mission (harvest Saturn-ring water, deliver to Earth orbit, support a commercial program), and what combination of relaxations would restore commercial closure?

Saturn orchestrator analysis identified the relaxation envelope:
- L0-04 mass floor: 25 t → 5-10 t (per-mission)
- L0-05 round-trip ceiling: 15 yr → 20-25 yr (patient-capital framing)
- L0-12 cost-competitive: 0.5x competitor → 0.8x competitor (or "match competitor + diversification premium")
- L0-24 reactor-on-contract: vacuous if binding architecture is non-nuclear (RTG + solar-hybrid)
- L0-07 cadence: 2/yr → 1/yr (paired with L0-09 relaxation)
- L0-05/L0-06 horizon: stretch via sovereign-research-grant capital structure

Tier 1 sanity sweep ran the existing `saturn_water_v1` closed-loop closure sweep (150 cells, 1744 paths). **Zero paths arrive at LEO depot.** Bottleneck identified: closed-loop derived wet vehicle (138-708 tonnes across cells) exceeds even multi-launch raw capacity in some cells; assembly preconditions fail on 180 paths; power-class preconditions fail on 445+408 paths. The L0 relaxations cannot be honestly tested at current framework fidelity.

The Tier 1 finding is itself load-bearing — it surfaces that the closed-loop framework as currently parameterised is more restrictive than the L0-relaxation question can probe. R-vehicle-mass-fidelity-refinement must land first (per-phase propellant fraction derivation, Wertz anchor review, path-conditional thermal protection) to give the relaxation envelope room to be tested.

## Pre-registered hypotheses (post-fidelity-refinement)

H1: **At least one cell in the saturn_water_v1.x post-fidelity-refinement framework reaches LEO depot with non-zero delivered payload under base parameters.** Falsified if even the most permissive cell (lowest-power, smallest-chunk, longest-cruise) still delivers 0 t. Reading-if-falsified: the structural-impossibility verdict survives the fidelity refinement; ICEBERG is structurally not deliverable as a commercial mission and the demonstrator-class promotion is the only remaining programmatic path.

H2: **Relaxing L0-04 from 25 t to 5 t brings closure rate above 5 percent at some L0-05 ceiling.** Falsified if closure rate at L0-04 = 5 t × L0-05 = 25 yr is below 5 percent.

H3: **Relaxing L0-05 from 15 yr to 25 yr alone (with L0-04 held at 25 t) brings closure rate above 5 percent.** Falsified if no cell closes 25 t delivered within 25 yr.

H4: **The non-nuclear regime (1-11 kilowatt-electric power, RTG-class) admits at least one closing cell at L0-04 = 10 t and L0-05 = 25 yr.** Tests whether the L0-24 vacating relaxation has real teeth. Falsified if zero closures across the non-nuclear power range at any chunk and any thrust.

H5: **The combined-relaxation envelope (L0-04 = 5 t, L0-05 = 25 yr, L0-24 vacated, L0-07 = 1/yr, L0-12 = 0.8x competitor) produces closure rate above 20 percent.** Load-bearing reading: at maximum spirit-preserving relaxation, is the commercial program viable? Falsified if below 20 percent. Sub-verdict: report the closure-rate-vs-relaxation-set sensitivity — which relaxation is the highest-leverage single lever?

H6: **The cost-of-delivered-water-at-LEO under the closed-loop framework at the relaxed L0-04 and L0-05 is competitive with lunar in-situ-resource-utilisation (~$1,000/kg projected) at scale, or no-worse-than 2x competitor.** Tests whether L0-12 relaxation is the binding economic constraint. Requires the financial model that R-pricing-anchor-revisit H7 depends on. May be deferred if the financial model isn't operative yet.

## Methodology

### Sweep design

Three sweeps:

**Sweep 1 — L0-04 sensitivity.** Hold L0-05 = 25 yr, L0-24 vacated (non-nuclear power 1-11 kWe), vary L0-04 floor {0.5, 1, 2, 5, 10, 15, 20, 25} t. Question: at what floor does closure rate cross 5%, 10%, 25%?

**Sweep 2 — L0-05 sensitivity.** Hold L0-04 = 10 t, L0-24 vacated, vary L0-05 ceiling {15, 18, 20, 22, 25, 28, 30, 35} yr. Question: at what ceiling does closure rate cross 5%, 10%, 25%?

**Sweep 3 — full combined-relaxation.** All five relaxations applied simultaneously across the chunk × thrust × power axis. Report closure rate per power class to surface which L0-24 reading dominates.

### Outputs

- Closure rate per (relaxation level, L0-04 floor, L0-05 ceiling) triple
- Highest-delivered-mass cell at each relaxation level
- Highest-leverage relaxation lever (single-relaxation sensitivity)
- Whether non-nuclear (RTG / solar-hybrid) power class produces ANY closure under relaxed L0s

### What to read from the results

If H5 holds (combined-relaxation closure rate above 20 percent), the spirit-preserving relaxation envelope is large enough to support a commercial program at the relaxed L0 set. The decision becomes whether to ratify the relaxations OR hold the original L0 set and accept commercial closure isn't there.

If H5 falsifies AND H1 holds (some path arrives but commercial closure rate stays low), the matrix verdict is "commercial program structurally non-viable even at maximum spirit-preserving relaxation." The demonstrator-class promotion is the only remaining programmatic path. The campaign should retire commercial-class as a near-term objective; ICEBERG becomes an infrastructure-class option for a future where one or more of the three engineering bets resolves favorably.

If H1 falsifies (even at maximum relaxation, no path arrives), the closed-loop framework is either over-pessimistic or the campaign's chunk-as-propellant-tank concept hits a structural wall the closed-loop revealed. Either way, the answer is "ICEBERG is not deliverable as currently conceived."

## Deliverables

1. This SCOPE.md.
2. STUDY.md with H1-H6 pre-registered.
3. `framework/relaxed_predicates.py` — closure predicates parameterised over (L0-04 floor, L0-05 ceiling).
4. `sweep_combined.py` — three sweeps + analysis script.
5. `results/closure_rate_envelope.json` — closure rate per (L0-04, L0-05, L0-24-state) triple.
6. FINDINGS.md with verdict on H1-H6 + matrix amendment specification.

## Out of scope

- Re-derivation of the financial model (R-pricing-anchor-revisit H7 territory; H6 deferred if financial model not operative).
- Contact-fidelity capture simulation (R-chunk-capture-contact-fidelity).
- Architecture search beyond the three already-evaluated capture mechanisms (harpoon, ram-scoop, everting-sleeve).
- Re-examining whether the demonstrator-class promotion was the right call.

## Predecessor work

- R-vehicle-mass-closure-refactor (titan-6, integrated 2026-05-26) — established the closed-loop framework.
- R-vehicle-mass-fidelity-refinement (Saturn orchestrator SCOPE, latest+24 — titan D5 successor) — gates this round.
- R-l0-relaxation-envelope Tier 1 sanity sweep (Saturn orchestrator, in-session 2026-05-26 latest+25) — surfaced the upstream bottleneck.
- Project-owner question 2026-05-26 — "how would we relax L0 requirements within the spirit of the mission?"
- Matrix decision #16 — L0-04 as parametric output not ratified threshold (latest+16 reframing).
- Matrix decision #15 — collapsed to (c) per hyperion R-saturn-system-water-depot-demand (latest+24). L0-04 strict + accept termination at flyable power is the operative forcing.

## Priority

**MEDIUM-HIGH, gated.** Cannot run until R-vehicle-mass-fidelity-refinement lands. After that, this round produces the definitive answer to the project-owner question "is there any combination of spirit-preserving L0 relaxations that brings back commercial closure?". The structural-verdict-stability check is load-bearing for the demonstrator-class-promotion-vs-revisit decision.

## Suggested worker

Any moon worker comfortable with the saturn_water_v1.x framework. titan-7 (re-spawn after the refactor) is the natural fit. Alternative: rhea (recent NPV-decomposition work, similar fidelity-vs-relaxation analytical style).
