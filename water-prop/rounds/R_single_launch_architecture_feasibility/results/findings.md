# R-single-launch-architecture-feasibility — findings.md

**Author:** rhea
**Date:** 2026-05-15 (latest+8, fourth round this sitting)

## Hypotheses adjudicated

| H | predicted | measured | status |
|---|---|---|---|
| H1 | min specific power at specific impulse 2934 seconds in [11.0, 11.5] W/kg; min specific impulse at sp=8 W/kg in [4500, 5000] s | 11.00 W/kg; 4258 s | **FALSIFIED** on Isp-axis (optimistic-direction: single-launch fits at slightly lower Isp than predicted) |
| H2 | two-Starship architecture (300 t budget) accommodates round-9 H2a baseline with 20-40% margin | 31.3% margin | **HELD** |
| H3 | reactor conjunction posterior at single-launch min-point in [0.10%, 0.30%] | 0.248% | **HELD** |
| H4 | Frame B (conditional + price-tail) at single-launch min-point in [40%, 50%] | 44.4% | **HELD** |
| H5 | full-chain Frame A at single-launch is 0.6–0.85× of 3-launch (lower) | 0.97× (single-launch ≈ 3-launch on Frame A) | **FALSIFIED** — Frame B doubling nearly compensates for conjunction-multiplier loss; ratio is much closer to 1.0 than I predicted |
| H6 | launch-count optimum is decision-frame-dependent: 3-launch wins under Frame A, 1-launch wins under Frame B | TRUE for 1-launch vs 3-launch alone; but **2-launch dominates both** on Frame A | **HELD** with refinement |

**Aggregate: 4 of 6 HELD, 2 FALSIFIED.** Both falsifications are informative — H1 falsified optimistically (single-launch easier than predicted on specific impulse axis); H5 falsified because Frame B's doubling nearly compensates for the conjunction-multiplier tightening, meaning single-launch is not as Frame-A-inferior as I framed.

## Headline

**The two-launch architecture is the Frame A optimum, not 1-launch or 3-launch.** At 2-Starship budget (300 tonnes to low-Earth-orbit), the round-9 H2a baseline (specific power 8 watts per kilogram, specific impulse 2934 seconds) fits with 31% margin. Conjunction posterior stays at 0.667% (unchanged from H2a baseline because reactor target unchanged); per-mission cost is $0.64 billion (versus $0.94 billion at 3-launch and $0.34 billion at 1-launch); break-even clearing price is $15.2 million per tonne (versus $22.4 million at 3-launch and $6.5 million at 1-launch); Frame B probability of positive net-present-value is 24.1% (versus 17.0% at 3-launch and 44.4% at 1-launch); **Frame A full-chain probability is 0.161%, beating 3-launch's 0.113% by 42% and 1-launch's 0.110% by 46%.** Two-launch is the round-9-relative free-lunch: no conjunction cost (same reactor target) AND meaningful Frame B gain.

## Reading

The launch-count optimum is unintuitive: 3-launch (round-10 anchor) is not the right Frame A optimum, but neither is 1-launch (round-11 finding). **2-launch dominates both on Frame A** because the conjunction multiplier is preserved (same reactor target as H2a baseline) while the per-mission cost drops enough to lift Frame B from 17% to 24%. The 2-launch architecture is essentially round-9 H2a with one fewer launch per mission — and the launch-count change is the only difference. The launch-cost-dominance finding from round 10 (launches drive 91% of total program cost at 3-launch) is the mechanism: dropping one launch removes 33% of the program cost without changing any other assumption.

Whether ICEBERG demonstrator can architecturally support 2 launches per mission instead of 3 is a separate physics question this round does not solve. The R-specific-power-cliff baseline at chunk 200 tonnes, specific power 8 watts per kilogram, specific impulse 2934 seconds yields m_LEO = 206 tonnes, which fits in 2 Starships (300-tonne budget) with 31% margin. **The 2-launch architecture is feasible at round-9 conservative anchors; the project should adopt 2-launch as the baseline for Frame A optimization and 1-launch as the Frame B optimization target.**

The H5 falsification is the load-bearing methodological finding. I predicted single-launch's Frame A would be 30% lower than 3-launch (ratio 0.6–0.85) because the conjunction multiplier tightens 3.5× (0.667% → 0.187%) while Frame B doubles (17% → 44%). Measured ratio is 0.97 — single-launch's Frame A is essentially equal to 3-launch's Frame A. **The Frame B doubling nearly compensates for the conjunction-multiplier tightening.** This is because Frame B is on a steeper part of the log-normal demand-curve at lower break-even prices: dropping break-even from $22.4 to $6.5 million per tonne moves the survival probability from p83 toward p56 of the distribution, a 2.6× lift. The conjunction tightening from 0.667% to 0.187% is 3.6× — slightly larger but in the same range. **The product (Frame A) is nearly invariant under launch-count changes when reactor target adjusts to keep mass-to-orbit feasible.** This is a non-obvious result that I missed in pre-registration.

Single-launch architecture is still the Frame B optimum (44% vs 24%) — but the conjunction tightening makes it a worse Frame A optimum than 2-launch. **The Frame-B-optimum 1-launch architecture is only relevant if the funding stakeholder is a sovereign-grant or sovereign-bond underwriter who funds the reactor program separately.** For any capital pricing the full chain, 2-launch is strictly better.

H1's specific-impulse axis falsification (min specific impulse 4258 seconds, not 4500–5000) is benign — the alternative lever to specific-power-lift is slightly easier than I predicted. Specific impulse 4258 seconds is still beyond current microwave-electrothermal-thruster cathode-life limits (~3000 seconds per titan-2 R-cathode-life-water-plasma) and would require either advanced cathode technology or non-water propellant (which conflicts with axis 19's chunk-water-as-propellant lever). The specific-power-lift path remains structurally more compatible with the held architecture.

## Cross-learning

1. **Updates round-10 H7 and round-11 H2.** Both rounds anchored on 3-launch. **Neither was the Frame A optimum.** At 2-launch the program-NPV(0) at conditional success improves; at 2-launch the Frame A probability of positive NPV is 42% higher than 3-launch. R-per-mission-economics-sensitivity-revisit's "central anchor" should be re-derived at 2-launch.

2. **Updates round-11 launch-count framing.** Round 11 surfaced "single-launch architecture doubles Frame B." True — but Frame A is roughly equal between 1-launch and 3-launch. **The Frame A optimum is 2-launch, not 1-launch.** Round 11's matrix-amendment recommendation should be refined: the matrix should distinguish three launch-count points (1 = Frame B optimum; 2 = Frame A optimum; 3 = round-10 central anchor, neither optimal).

3. **Refines the conjunction-multiplier-dominance reading.** Round 10 concluded "conjunction multiplier dominates" — true at Frame A. But at the architectural choice between launch counts, **Frame B can compensate for conjunction tightening if the price-distribution is steep enough at the break-even region.** The log-normal demand-curve has central density around the break-even region for both 1-launch and 3-launch architectures, which is why the compensation nearly cancels.

4. **The 2-launch architecture is the architectural sweet spot.** Worth surfacing to project owner as a matrix amendment on axis 13 (outbound launch architecture).

5. **Methodology note (no lesson candidate yet):** the H5 falsification was caused by under-predicting Frame B's responsiveness to break-even price changes. The log-normal demand-curve fit (round 11) lets me compute Frame B analytically; I should have done so during H5 pre-registration instead of estimating the ratio from "Frame B doubles vs conjunction multiplier 3.5× tightening." **Pre-register Frame B with the analytical formula, not the rule-of-thumb.** Possibly a methodology lesson candidate after more rounds confirm.

## Next-round candidates

1. **R-2-launch-architecture-matrix-amendment.** Matrix axis 13 (outbound launch architecture) currently anchors on Starship at central pricing. This round shows 2-launch is the Frame A optimum. Matrix amendment recommendation: explicitly anchor on 2-launch as the Frame A baseline, with 1-launch as the Frame B alternative (sovereign-grant-funded reactor) and 3-launch as the round-10 conservative cost ceiling. Synthesis round; no new physics.

2. **R-specific-impulse-cathode-life-revisit.** Round-11's finding that single-launch fits at specific impulse 4258 seconds at sp=8 W/kg suggests the cathode-life axis is worth re-examining. Titan-2's R-cathode-life-water-plasma found erosion concerns above 3000 seconds; the gap between 3000 and 4258 may or may not be bridgeable with different cathode materials. Engineering round.

3. **R-frame-b-funding-stakeholder-map.** Round 11 + this round together suggest a decision-frame-to-funding-stakeholder map (Frame A = return-seeking capital → 3-launch optimum; Frame B = sovereign-bond → 1-launch optimum; 2-launch dominates both for return-seeking-conditional-on-technical-closure). Synthesis round on project-owner pitch posture.

4. (still queued) R-staged-commitment-gates-frame-B-interaction.

5. (still queued) R-mars-sample-return-precedent.

## Revisit

Pre-registration accuracy: 4 of 6 HELD; 2 falsified, both informatively. **H1 falsified optimistic-direction** (single-launch fits at slightly lower specific impulse than predicted) — this is a benign falsification that tightens H1 rather than overturning it. **H5 falsified non-directional** — single-launch and 3-launch Frame A are essentially equal, not 0.6–0.85× as I predicted. This is the most methodologically informative falsification because it reveals that Frame B's responsiveness to break-even-price changes compensates for the conjunction-multiplier tightening in a way I missed.

The 2-launch sweet spot is the load-bearing finding. I did not pre-register a hypothesis on 2-launch architecture; H6's binary 1-launch-vs-3-launch framing missed it. **Recurring lesson:** when pre-registering hypotheses on architectural sweet spots, sweep the full range of the design variable, not just the endpoints. (Already implicit in methodology lesson 1 — "back-of-envelope first" — but worth restating.)

Four-round sitting cumulative: 21 of 27 sub-claims HELD across rounds 9–12. Six falsifications: 1 in round 10 (arithmetic), 1 in round 11 (matrix-amendment over-broad), 2 in round 12 (one optimistic-direction, one missed sweet spot). The cumulative falsification rate (22%) is in line with R&D campaign protocol expectations for well-pre-registered hypotheses.
