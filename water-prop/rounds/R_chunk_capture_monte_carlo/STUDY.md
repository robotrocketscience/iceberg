# R-chunk-capture-monte-carlo — pre-registered study

**Round:** R-chunk-capture-monte-carlo
**Date:** 2026-05-26
**Author:** Saturn (orchestrator, in-session execution)
**Status:** pre-study — hypotheses locked before any runs.

This document is the falsifier-bearing record for the round. It is pre-registered: H1..H8 are stated below with explicit pass/fail thresholds, BEFORE any Monte Carlo runs. Any later result that contradicts the threshold falsifies the hypothesis; any result inside the threshold holds it. Reading is in FINDINGS.md.

## Architecture-of-record

Three parallel decomposition trees (per SCOPE.md):

- **Single-chunk harpoon** — rendezvous, deploy harpoon, catch, contain, survive grab loads.
- **Ram-scoop residence-class** — radial-offset station-keep, open aperture, decelerate incoming particles, cinch / outlier-reject, retain over coast.
- **Everting-sleeve active enclosure** — rendezvous, evert sleeve, envelop chunk, cinch, decelerate + carry.

The eversion-kinematics stage is given its own slot in the everting-sleeve decomposition because eversion at 200-tonne-chunk scale has zero flight heritage and is itself an engineering risk (per project-owner direction 2026-05-26).

## Pre-registered hypotheses

### H1 — posterior is a distribution conditioned on spin rate, not a scalar

**Claim:** The defensible posterior on single-pass capture efficiency is a distribution conditioned on target spin rate, not a scalar anchor.

**Falsifier:** total-order sensitivity index for spin rate is below 0.10 across the operating envelope, for all three architectures.

**Reading-if-held:** the 0.85 desk-study anchor must be replaced by a spin-rate-conditioned distribution in the matrix. Decision points #1 and #2 inherit the new framing.

**Reading-if-falsified:** spin rate is not the bottleneck; the anchor can remain scalar but must be re-derived from whichever axis actually dominates.

### H2 — spin rate is the dominant uncertainty axis

**Claim:** Target spin rate is the single largest contributor to capture-success variance, with the highest total-order sensitivity index among the eight to ten candidate axes.

**Falsifier:** Any other axis (chunk mass, surface friction, approach velocity, sensor noise, contact geometry, catcher compliance, controller delay, or for everting-sleeve eversion-completion-rate / eversion-asymmetry-misalignment) shows a higher total-order index than spin rate in the closed-form Tier 1 result for at least one architecture.

**Reading-if-held:** spin handling becomes a top-tier engineering priority for the architecture(s) where it dominates.

**Reading-if-falsified:** spin handling is overrated by the literature analog; the actual dominant axis is what drives engineering priority instead. (This would be a surprising result and would update the campaign's reading of the space-robotics literature.)

### H3 — n ~ 1200 is the right binomial budget for a defensible posterior

**Claim:** A binomial credible interval of half-width at most 0.02 at the 95 percent level, at the operating point, requires approximately 1200 contact-fidelity Bernoulli runs.

**Falsifier:** The half-width target requires more than 5000 runs in the contact-fidelity work. This would imply the outcome is not effectively Bernoulli (heavy tail in success metric, non-binary outcomes, hidden conditional structure).

**In-session note:** H3 is not tested by the closed-form Tier 1; it gates the contact-fidelity work that stays SCOPE'd.

### H4 — contact-engine choice does not dominate the posterior

**Claim:** The contact-engine choice (MuJoCo vs Drake, or in this session: closed-form vs hypothetical contact-fidelity) does not move the posterior median by more than 0.05.

**Falsifier:** Cross-engine A/B at n=200 each shows posterior medians separated by more than 0.05.

**In-session note:** not tested in this session. The closed-form Tier 1 produces a Tier-1 posterior to compare contact-fidelity results against later.

### H5 — closed-form product over-estimates relative to contact fidelity

**Claim:** The five-stage product decomposition over-estimates joint capture success relative to the contact-fidelity Monte Carlo by at least 0.05. Reasoning: closed-form products treat stages as independent, but failure modes co-vary (high spin both raises catch failure and raises containment failure).

**Falsifier:** Closed-form result is within 0.02 of the contact-fidelity result.

**In-session note:** not testable in this session (no contact-fidelity baseline). H5 stays open for the follow-on work.

### H6 — at least one architecture survives the L0-04 floor

**Claim:** At least one of the three architectures produces a posterior median single-pass capture probability greater than or equal to 0.64 × the desk-study anchor reference. The matrix verdict at L0-04 = 25 tonnes requires this.

**Falsifier:** All three architectures' posterior medians fall below 0.64.

**Reading-if-held:** the surviving architecture(s) become(s) the matrix's reference for design-axis 19 (capture architecture). Cascade to decision points #1, #2.

**Reading-if-falsified:** L0-04 = 25 tonnes is structurally unviable at current architecture and the matrix's open SCOPEs cascade. Project-owner decision required: retire L0-04, search for a fourth architecture, or terminate the chunk-capture path entirely.

### H7 — everting-sleeve transfers from the satellite-capture application

**Claim:** The everting-sleeve mechanism previously studied for cooperative satellite capture (beliefs `ae7031e288c1ce59`, `839a793587c9f84c`, `606187f2f970cc2f`, `3ac3f0245c2e5044`) transfers to ring-chunk capture without a posterior penalty greater than 0.10 versus the better of the other two architectures.

**Falsifier:** Everting-sleeve posterior median is more than 0.10 below the best other architecture's posterior median.

**Reading-if-held:** the sleeve-capture concept is dual-use and informs ICEBERG planning.

**Reading-if-falsified:** the sleeve mechanism is satellite-specific and does not generalize to chunk capture; flagged in a cross-project memo.

### H8 — eversion-kinematics dominates the everting-sleeve architecture

**Claim:** For the everting-sleeve architecture, the eversion-kinematics stage (slot 2 of its five-stage decomposition) is the dominant single-stage failure mode — it contributes more to total joint-failure probability than any of the other four stages.

**Falsifier:** variance-based sensitivity decomposition over the five-stage product shows another stage (rendezvous, envelopment, cinch, or decel-and-carry) with a larger single-stage failure-rate share.

**Sub-question:** How does eversion-kinematics failure rate scale with chunk size — sub-linearly (favours architecture at large chunks), linearly, or super-linearly (retires architecture at scale)?

**Reading-if-held:** engineering follow-on for everting-sleeve is "demonstrate eversion at scale," not "improve grip."

**Reading-if-falsified:** engineering priority shifts to whichever stage actually dominates.

## Architecture-of-record under the load-bearing reading

H6 is the load-bearing hypothesis. Sub-readings for the round:

- **Best case:** all three architectures hold at posterior median greater than or equal to 0.64. Matrix gets to pick on engineering risk, not on closure margin. Comparison memo is the deliverable.
- **Most likely case (per wondering precedent):** one architecture clearly leads, one is marginal, one falls below 0.64. Comparison memo recommends the leader; the other two are documented but retired.
- **Worst case:** all three fall below 0.64. Matrix amendment cascade triggers. Project-owner decision required.

## Reading methodology

- **Tier 0.5 (Cassini spin prior):** literature review, no Monte Carlo. Output is a memo + revised prior table.
- **Tier 1 (in-session, closed-form):** Morris elementary effects over 8-10 axes × 3 architectures using a parameterised failure-product model. Output is axis ranking (tests H2, contributes to H1) and a closed-form posterior (Tier-1-equivalent for H6).
- **Tier 1 results inform** the contact-fidelity SCOPE that follows (which axes to refine, where the operating point sits).
- **Tiers 2 + 3 (contact-fidelity)** stay SCOPE'd. H3, H4, H5 cannot be tested in-session.

## Variance log entry (deferred to FINDINGS)

When FINDINGS.md lands, it gets a variance-log entry against the matrix at the operating point for each architecture. The matrix amendment specification follows from the H6 verdict.

## Mental-model risks logged before runs

Per campaign lesson 9 (mental-model error logging), the load-bearing risks are flagged before runs so post-hoc rationalisation is harder:

1. **Spin-rate-prior wrongness.** The asteroid-anchored prior is plausibly wrong by an order of magnitude in either direction for ring chunks. Tier 0.5 is the mitigation.
2. **Closed-form independence assumption** (H5). Stages probably co-vary; the closed-form likely over-estimates. Documented; H5 stays open.
3. **Everting-sleeve unknown-unknowns.** Eversion at 200-tonne scale has no precedent at all. H8 makes the dominant-failure-mode assumption testable; H7 makes the transfer assumption testable.
4. **Surface-friction prior for ice-on-fabric** is bracketed against terrestrial values; cryogenic ice on Saturn-thermal fabric is unmeasured. Wide prior.
5. **Architecture-of-record decomposition completeness.** The five-stage trees are best-effort; if the Monte Carlo surfaces a missing failure mode (e.g., dust contamination of a harvest port), it goes in the variance log and the decomposition is amended in a follow-on round, not silently in this one.
