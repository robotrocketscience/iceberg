# R-ramscoop-foundational-premise-revisit — does the Tier-1 capture lead survive the chunk-as-propellant-tank delta-velocity penalty?

**Status:** scope, pre-study. Authored by Saturn (orchestrator), 2026-05-26.
**Predecessor:** R-chunk-capture-monte-carlo Tier 1 result + project-owner direction 2026-05-26.

## Premise

R-chunk-capture-monte-carlo Tier 1 (`464927e`, 2026-05-26) returned ram-scoop residence-class as the Tier-1 capture-efficiency leader (median 0.405; 90% credible interval [0.327, 0.491]), ahead of single-chunk harpoon (0.365 [0.136, 0.497]) and everting-sleeve (0.246 [0.130, 0.418]). All three failed the H6 threshold at L0-04 = 25 t, but ram-scoop's relative position is robust to plausible re-parameterisations of the closed-form model.

This creates a tension with the latest+6 (2026-05-15) project-owner decision that retired ram-scoop on **foundational-premise** grounds: ram-scoop adds approximately +14.7 km/s of Saturn-side delta-velocity (residence-class capture in B-ring requires circularising into the ring plane and back out), which defeats ICEBERG's foundational premise of delta-velocity-minimisation-via-chunk-as-propellant-tank. The chunk-fed exit-Δv penalty was independently confirmed by titan-2 R-conops-chunk-vs-ram-scoop (`07b73ec`, 2026-05-15 latest+7): delivered fraction collapses from 17 percent to 3.5 percent (a 5x drop) under continuous-thrust accounting with chunk-fed propulsion.

The Tier 1 capture-efficiency model **does not carry the chunk-as-propellant-tank delta-velocity bookkeeping**. The Tier-1 leadership of ram-scoop is therefore conditional, not absolute. This round closes that gap with a single coupled model.

## The question

Given:
- Ram-scoop Tier 1 capture-probability posterior median 0.405 (vs harpoon 0.365)
- Ram-scoop delivered-fraction penalty from chunk-fed exit-Δv: 17% → 3.5% (5x relative drop vs harpoon-class architectures)
- The matrix verdict is on **delivered mass per mission**, not on capture probability alone

**Does the Tier-1 capture lead survive the delta-velocity penalty when both are carried in one model?**

Concretely: with chunk mass M and capture probability p_capture, expected captured mass is p_capture × M. After Tsiolkovsky and continuous-thrust bookkeeping with the architecture's exit-Δv, delivered mass is p_capture × M × η_delta_v, where η_delta_v is the fraction of captured mass remaining after the exit burn. Ram-scoop η_delta_v is ~0.21 (3.5% of 17%); harpoon η_delta_v is the 17% reference (or whatever the chunk-fed harpoon exit-Δv comes out to under the same accounting).

Naive arithmetic: ram-scoop 0.405 × 0.21 = 0.085; harpoon 0.365 × 0.17 = 0.062. Ram-scoop wins by ~37 percent on the product. But these numbers are not directly comparable — η_delta_v in the titan-2 round was relative to a 200 t chunk, and chunk size couples to capture mechanics in different ways for the two architectures. **This round produces the apples-to-apples comparison.**

## Pre-registered hypotheses

H1: **Ram-scoop's Tier-1 capture lead is preserved after delta-velocity bookkeeping.** Falsified if delivered-mass posterior median for ram-scoop is below harpoon's.

H2: **The 5x delivered-fraction drop in titan-2 R-conops-chunk-vs-ram-scoop holds at the Tier-1 capture priors.** Falsified if the relative penalty at Tier-1-prior-anchored chunk-mass distribution is below 3x or above 8x.

H3 (load-bearing): **Even with ram-scoop carried, no architecture clears the L0-04 = 25 t commercial floor at Tier 1 delivered-mass posterior.** This re-tests H6 from R-chunk-capture-monte-carlo with delta-velocity bookkeeping. Falsified if any architecture's delivered-mass posterior median equals or exceeds 25 t at any operating chunk-mass.

H4: **The architecture trade is chunk-mass-dependent.** Falsified if the better architecture is the same across the full chunk-mass range [10 t, 200 t]. (Hypothesis: ram-scoop is better at large chunks where the capture advantage dominates; harpoon is better at small chunks where the delta-velocity penalty matters less because chunks are smaller anyway.)

## Methodology

1. Take the Tier 1 capture-probability posterior samples from `results/tier1_results.json` for harpoon and ram-scoop.
2. For each sample, apply the architecture's chunk-fed exit-Δv to produce a delivered-mass sample, using the titan-2 R-conops-chunk-vs-ram-scoop continuous-thrust bookkeeping. **Do not re-derive the delta-velocity numbers — anchor on the published rounds and audit any inconsistency.**
3. Marginalise over chunk mass with the Tier 1 prior (log-uniform [10, 200] t).
4. Produce delivered-mass posteriors per architecture; compare medians and credible intervals; verdict on H1-H4.

Out of scope: contact-fidelity simulation, new physics. This is a single coupled-model round on existing posteriors plus existing delta-velocity bookkeeping. Budget: 2-4 hours of analyst time. No new Monte Carlo runs required (the Tier-1 samples are reused).

## Deliverables

1. This SCOPE.md.
2. STUDY.md with H1-H4 pre-registered.
3. `coupled_delivered_mass.py` reusing the Tier-1 JSON.
4. FINDINGS.md with verdict on H1-H4 and matrix amendment specification if the verdict moves H3.

## Predecessor work

- R-chunk-capture-monte-carlo Tier 1 (commit `464927e`) — capture-probability posteriors per architecture.
- titan-2 R-conops-chunk-vs-ram-scoop (commit `07b73ec`) — ram-scoop delivered-fraction penalty under continuous-thrust accounting.
- Project-owner decision latest+6 (2026-05-15) — foundational-premise retirement of ram-scoop.
- Project-owner decision 2026-05-26 — H6 cascade promoting demonstrator-class; the foundational-premise revisit is the predicate for whether ram-scoop is the commercial-class follow-on candidate.

## Priority

**MEDIUM-HIGH.** Gates the matrix's open SCOPE R-chunk-capture-contact-fidelity (ram-scoop only). If H1 falsifies (ram-scoop loses after delta-velocity bookkeeping), the contact-fidelity follow-on should target harpoon instead. If H3 holds (no architecture clears 25 t even with delta-velocity carried), the demonstrator-class pivot stands unconditionally. Either way, this round resolves a load-bearing ambiguity in the matrix amendment.

## Suggested worker

Any moon worker comfortable with Tsiolkovsky + continuous-thrust delta-velocity bookkeeping AND reading the Tier-1 posterior JSON. Best fit: titan, rhea, or hyperion (all have prior delta-velocity-bookkeeping rounds in their history).
