# R-chunk-capture-monte-carlo — FINDINGS (Tier 1)

**Round:** R-chunk-capture-monte-carlo
**Date:** 2026-05-26
**Status:** Tier 1 (closed-form) complete. Tiers 2 + 3 (contact-fidelity) SCOPE'd, not run in session.
**Author:** Saturn (orchestrator, in-session execution)
**Inputs:** SCOPE.md, STUDY.md, tier_0_5_spin_prior.md, tier1_closed_form.py
**Raw results:** `results/tier1_results.json`

## Headline

**H6 (the load-bearing hypothesis) is FALSIFIED at the Tier-1 closed-form level for all three architectures.** No architecture's posterior median crosses the 0.544 threshold (0.64 × 0.85 desk-study anchor) that the matrix verdict at L0-04 = 25 tonnes requires.

This is a Tier-1, closed-form, parametric result. Tiers 2 + 3 (contact-fidelity Monte Carlo with MuJoCo / Drake) stay SCOPE'd. Any contact-fidelity result outside the Tier-1 90 % credible intervals would update the verdict. **But on the available evidence today, the L0-04 floor is structurally unviable at all three architectures.**

## Tier-1 posteriors (n = 8000 per architecture)

| Architecture | Median capture prob | 90 % credible interval | H6 (≥ 0.544) |
|---|---:|---:|---|
| Single-chunk harpoon  | 0.365 | [0.136, 0.497] | fails |
| Ram-scoop residence   | 0.405 | [0.327, 0.491] | fails |
| Everting-sleeve       | 0.246 | [0.130, 0.418] | fails |

Ram-scoop is the leader on both posterior median and tightness of the credible interval. Everting-sleeve is the laggard, with eversion-kinematics at 200-tonne-chunk scale dragging the joint posterior down.

## Hypothesis verdicts

### H1 — posterior is a distribution conditioned on spin rate, not a scalar

**HELD for harpoon, FALSIFIED for ram-scoop and everting-sleeve.** Spin rate dominates harpoon's variance budget (Morris rank 1). For ram-scoop, sensor noise dominates (spin rank 4). For everting, eversion-misalignment dominates (spin rank 4). The architecture choice determines whether the posterior needs to be conditioned on spin.

### H2 — spin rate is the dominant uncertainty axis

**Architecture-dependent. HELD for harpoon only.**

- Harpoon: top axis = `spin_rate_rpm` (rank 1)
- Ram-scoop: top axis = `sensor_noise_m` (spin at rank 4)
- Everting: top axis = `eversion_misalign_deg` (spin at rank 4)

This is itself an informative finding: the wondering's literature-anchored prediction that "spin dominates" generalises from the active-debris-removal / robotic-grapple literature, which corresponds best to ICEBERG's harpoon framing. Ram-scoop and everting-sleeve are different physics; their dominant axes are different.

The Tier 0.5 spin prior (decameter-marginal log-uniform [0.0005, 0.05] rpm, 1-2 orders of magnitude slower than the asteroid analog) explains why spin does not dominate the other two architectures: the slow ring-chunk spin distribution lets sensor noise and eversion mechanics rise to the top of the rank.

### H3 — n ≈ 1200 contact-fidelity runs for ± 0.02 binomial half-width

**Not tested in session.** Tier-3 contact-fidelity work stays SCOPE'd. The Tier-1 posterior 90 % CIs are 0.10 to 0.36 wide — broader than the 0.04 contact-fidelity target — because the closed-form model carries the full prior variance into the posterior. Contact-fidelity narrows the credible interval only at a specific operating point.

### H4 — contact-engine choice doesn't move posterior by more than 0.05

**Not tested in session.** No contact-fidelity baseline exists yet.

### H5 — closed-form over-estimates relative to contact fidelity

**Not testable in session.** The Tier-1 medians (0.246 to 0.405) are already below the matrix-required 0.544. If H5 holds in the contact-fidelity follow-on, the gap widens — the contact-fidelity numbers would be even lower, strengthening the H6 falsification.

### H6 — at least one architecture survives the L0-04 floor

**FALSIFIED at Tier 1.** Threshold = 0.544. All three posterior medians fall below: harpoon 0.365, ram-scoop 0.405, everting-sleeve 0.246.

**Reading.** L0-04 = 25 tonnes is structurally unviable at all three current architectures, at the Tier-1 closed-form fidelity. The matrix's open SCOPEs cascade through this finding. The project-owner-pending decision per locked belief `c95626970c29aeef` becomes load-bearing: ratify L0-04 = 25 t and accept that no current architecture closes, or override the floor downward.

**Caveat: the closed-form model is parametric.** Functional forms calibrate to the audit's ~ 46 % bottoms-up reference for harpoon at the prior central anchor. Different choices for the per-stage failure functions would shift the absolute numbers — though the *relative ordering* (ram-scoop > harpoon > everting) is robust to most plausible re-parameterisations because it reflects the architecture-specific Morris dominances.

### H7 — everting-sleeve transfers from the satellite-capture application

**FALSIFIED.** Everting-sleeve median = 0.246; best other = ram-scoop at 0.405; penalty = 0.159 > 0.10 threshold.

**Reading.** The sleeve mechanism studied for cooperative satellite capture is satellite-specific. The 200-tonne-chunk-scale eversion-kinematics stage (size-dependent failure mode at ten-of-metres deployable scale, zero flight heritage) drives the joint posterior down. Cross-project memo recommended: the sleeve is not chunk-transferable per this Tier-1 reading.

### H8 — eversion-kinematics dominates the everting-sleeve architecture

**HELD.** The eversion stage is the variance-dominant stage in the everting-sleeve posterior. The Morris dominance of `eversion_misalign_deg` corroborates: eversion-kinematics is both the highest-variance stage and the highest-sensitivity axis for this architecture.

**Reading.** Engineering follow-on for the everting-sleeve architecture, if pursued, must demonstrate eversion at 200-tonne-chunk scale. The other four stages (rendezvous, envelopment, cinch, decel-and-carry) are not the bottleneck.

## Cross-architecture comparison

| Metric | Harpoon | Ram-scoop | Everting-sleeve |
|---|---:|---:|---:|
| Posterior median | 0.365 | **0.405** | 0.246 |
| 90 % CI width | 0.361 | **0.164** | 0.288 |
| Dominant axis | spin_rate | sensor_noise | eversion_misalign |
| H6 (≥ 0.544) | fails | fails | fails |
| Engineering follow-on if leader | despin / impact off-axis | navigation precision | eversion at scale |

Ram-scoop wins on both posterior median (highest) and credible-interval tightness (narrowest). Its dominant axis is sensor noise (navigation precision in the radial-offset station-keeping phase), which is a known, mature engineering problem — not a novel demonstrator hurdle.

## Variance log entry — to be appended to ARCHITECTURE-DECISION-MATRIX.md

```
2026-05-26: R-chunk-capture-monte-carlo Tier 1 closed-form finds H6 FALSIFIED across all three
architectures at L0-04 = 25 t (medians: harpoon 0.365, ram-scoop 0.405, everting 0.246; threshold
0.544). Ram-scoop leads on both posterior median and credible interval. Everting-sleeve
satellite-capture transfer FALSIFIED at Tier 1 (H7, penalty 0.159). Tier 0.5 Cassini-anchored spin
prior is 1-2 orders of magnitude slower than asteroid analog; H2 (spin dominance) holds only for
harpoon. Tiers 2+3 contact-fidelity SCOPE'd, not run. Matrix open SCOPEs cascade through this
finding pending project-owner direction.
```

## Matrix amendment specification

The H6 falsification at L0-04 = 25 t triggers the cascade flagged in the SCOPE:

1. **Design-axis 19** (capture architecture, currently falsified-no-replacement) — set to **ram-scoop residence-class as the Tier-1 leader**, with status `provisional pending Tier 2 + 3 contact-fidelity`. Confidence: medium.
2. **Decision point #1** (program class) — Tier 1 says no architecture closes the commercial-class L0-04 floor as currently set. The demonstrator-class path (R-demonstrator-mission-concept, §7.5 waiver) becomes the more defensible programmatic story until contact-fidelity revises.
3. **Decision point #2** (round-trip ceiling) — unchanged by this round.
4. **L0-04 floor** (locked belief `c95626970c29aeef`) — project-owner-pending: ratify the 25 t floor and accept that no current architecture closes, OR override downward (10 t closes 52 % of paths at canonical architecture per the audit's sensitivity sweep).
5. **Open SCOPEs queue** — R-everting-sleeve-feasibility downgraded to "retire pending H7 contact-fidelity check"; ram-scoop refinement SCOPEs promoted.

## Mental-model risks logged at study time — post-hoc audit

Per STUDY.md, the load-bearing risks were:

1. **Spin-rate-prior wrongness.** Mitigated by Tier 0.5; the new prior shifted the spin contribution and revealed H2's architecture-dependence. *Result: mitigation worked.*
2. **Closed-form independence assumption.** Stages still treated independently; this is the SCOPE'd contact-fidelity gap. *Result: open per design; flagged in H5.*
3. **Everting-sleeve unknown-unknowns.** Eversion-kinematics modelled with a size-dependent penalty term; H8 held; H7 falsified. *Result: the architecture's penalty is exposed.*
4. **Surface-friction prior wrongness.** Wide prior carried; surface friction was not a dominant axis in any architecture (mid-rank everywhere). *Result: low-leverage, prior breadth is fine.*
5. **Architecture-of-record decomposition completeness.** No missing failure mode surfaced in the closed-form model. Contact-fidelity may surface dust contamination, decel-liner punctures, etc. *Result: open per design.*

## Bounds on this Tier-1 reading

What this round establishes:
- A defensible Tier-1 axis ranking per architecture (Morris elementary effects, r=30 trajectories).
- A defensible Tier-1 posterior under the closed-form failure-product model.
- A Tier-0.5-anchored, ring-environment-specific spin prior that supersedes the asteroid analog.
- Falsification of H6, H7; HELD on H8; architecture-dependent reading on H1, H2.

What this round does NOT establish:
- Contact-fidelity posterior (H3, H4 untested).
- Failure-mode independence assumption (H5 untested).
- Specific operating-point recommendations for engineering follow-on (requires Tier 2 PCE on the Tier-1 winner).

## Recommended next moves

1. **Surface H6 falsification to the project owner immediately.** This is the load-bearing finding and changes the matrix open-SCOPEs queue.
2. **Spawn or schedule the contact-fidelity follow-on (Tiers 2 + 3)** for ram-scoop only, as the Tier-1 leader. Harpoon and everting-sleeve get retired at Tier 1 unless project-owner overrides.
3. **Update REQUIREMENTS.md variance log** with the Tier-1 closed-form L0-04 verdict.
4. **Cross-project memo** that the everting-sleeve does not transfer to chunk capture (H7 falsified).
