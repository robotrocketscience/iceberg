# R-clearing-price-tail-integration-decision-frame — findings.md

**Author:** rhea
**Date:** 2026-05-15 (latest+8, third round this sitting)

## Hypotheses adjudicated

| H | predicted | measured | status |
|---|---|---|---|
| H1 | P(price ≥ break-even at 3 launches/mission) in [10%, 25%] | 17.0% | **HELD** |
| H2 | P(price ≥ break-even at 1 launch/mission, Flagship-class architecture) in [30%, 50%] | 38.2% | **HELD** |
| H3 | conditional-success P(NPV>0 at zero discount) bracket in [10%, 50%] | bracket [17.0%, 46.6%] (my point-estimate vs demand-curve fleet) | **HELD** |
| H4 | full-chain P(NPV>0) in [0.02%, 0.10%] | bracket [0.028%, 0.078%] | **HELD** |
| H5 | three decision frames distinct; Frame B viable at ≥ 15% | Frame B 17.0% at zero discount, 29.1% at sovereign-bond | **HELD** |
| H6 | Frame B P(NPV>0) at venture WACC (12%) ≥ 5% | 3.0% | **FALSIFIED** pessimistic — venture-class retirement decision corroborated |

**Aggregate: 5 of 6 HELD, 1 falsified.** Log-normal fit to demand-curve distribution validates well (p25/p75 within 2.5% / 0.7%).

## Headline

**Three decision frames give three distinct verdicts on the round-9 H2a minimum-point.** Frame A (full chain) ruled out at 0.03–0.08%. Frame B (conditional on reactor + engineering success, demand-curve-integrated) viable at **17–47% probability of positive NPV at zero discount and 29% at sovereign-bond discount (3%)**. Frame C (conditional success at BEST_CELL point estimate) ruled out at -$22 billion. **Frame B at venture WACC (12%) is 3%** — corroborates the matrix's "venture-class framing retired" decision and falsifies H6. The load-bearing finding: **sovereign-bond-class capital is the highest-discount class at which ICEBERG H2a minimum-point closes at non-trivial probability under conditional-success + price-tail-integrated framing.**

## Reading

The three-frame distinction is the main contribution. Round 9 H6 ("technology-demonstrator only") and round 10 H5 ("two-track: return-seeking-ruled-out + sovereign-grant-viable") were both anchored on conjunction-weighted framing. Both are correct under Frame A. Both are **silent on Frame B**, which is the relevant framing for any capital class willing to underwrite reactor + engineering risk separately from market-price risk.

Frame B's verdict by capital class:
- Zero discount (sovereign-grant policy frame): 47% P(NPV>0)
- Sovereign-bond (3% WACC): 29%
- Corporate growth (8.7% WACC): 8%
- Venture (12% WACC): 3%

**The matrix's pitch posture should distinguish.** Venture-class retirement is empirically correct (3% at conditional success is below any defensible underwriting threshold). Sovereign-bond at 29% is materially financeable in principle conditional on reactor + engineering closure. Sovereign-grant at zero discount has nearly half probability of positive NPV. **The pitch differentiator is what discount rate the underwriting party imposes.**

The break-even ladder shows the launch-count dominance. At 1 launch per mission (Flagship-class architecture): P(price ≥ break-even) = 38%. At 3 launches per mission (round-10 central): 17%. At 8 launches per mission (Falcon-Heavy multi-launch): 6%. **Reducing launches-per-mission from 3 to 1 doubles Frame B's tail probability.** Worth a follow-on round on what mission architecture supports single-launch (chunk size, reactor mass, propellant stack).

The round-9 H6 reading ("technology-demonstrator-only") was correct under Frame A but obscured the Frame B viability at sovereign-bond. **Project-owner pitch posture should not retire return-seeking-capital framing entirely** — it should distinguish (a) full-chain expected-value framing where it is ruled out from (b) conditional-on-technical-success framing where it is viable at sovereign-bond and zero-discount levels but ruled out at venture WACC.

The round-9 conjunction posterior (0.167%) is what multiplies the conditional-success probabilities to produce Frame A's 0.03–0.08% full-chain P(NPV>0). **The conjunction multiplier dominates by three orders of magnitude.** Without reactor + engineering closure, neither Frame B nor Frame C exists — Frame A is the floor. Sovereign-grant capital exists specifically to underwrite the conjunction multiplier (reactor program + engineering closure) so that Frames B and C become the relevant decision frames for downstream capital.

H6 falsification corroborates the matrix's venture-class-retirement decision. Venture capital at 12% WACC has 3% P(NPV>0) at conditional success — below any reasonable underwriting bar. **Venture should stay retired.** The amendment recommendation is narrower than I pre-registered: matrix axis 17 should add Frame B language but not re-open venture-class framing.

## Cross-learning

1. **Updates round-9 H6 and round-10 H5.** Round-9 "technology-demonstrator only" and round-10 "two-track" framings are correct under Frame A but silent on Frame B. The three-frame distinction is the right framing for matrix axis 17.

2. **Updates the matrix's "venture-class framing retired" decision.** H6 was pre-registered to falsify this retirement; H6 falsified pessimistic, **so the retirement decision is corroborated at venture WACC.** Matrix axis 17 should keep venture retired but add Frame B language acknowledging sovereign-bond-class viability conditional on technical closure.

3. **Single-launch architecture matters more than I thought.** P(price ≥ break-even) doubles from 17% (3 launches) to 38% (1 launch). This is the highest-leverage architectural lever for Frame B closure. R-single-launch-architecture-feasibility is the highest-priority next round.

4. **Log-normal fit to demand-curve distribution validates.** p25/p75 within 3% of empirical values. Future rounds can use the fitted (mu_log10, sigma_log10) = (3.72, 0.66) parameters for analytical computations without re-running Monte Carlo.

5. **Methodology note (no lesson candidate yet):** stacking three rounds in one sitting (each questioning the previous) produced a refined three-frame distinction that no single round could have reached. Round 9 surfaced the conjunction-weighted floor (Frame A). Round 10 surfaced the cost-anchor magnitude correction and decision-frame distinction (Frames A vs C). Round 11 surfaced the price-distribution tail (Frame B). The successive self-questioning was productive. **Whether this should be a methodology lesson depends on whether the converse (single comprehensive round) would have been better.** Tentative read: no — each round's pre-registration discipline was preserved by separation, and the falsifications informed each subsequent round's pre-registration.

## Next-round candidates

1. **R-single-launch-architecture-feasibility.** Highest leverage per Frame B doubling at 1 launch vs 3. What architecture supports single-Starship-launch ICEBERG demonstrator? Chunk size, reactor mass, propellant stack tradeoffs.

2. **R-staged-commitment-gates-frame-B-interaction.** R-heterogeneous-cadence found staged go/no-go gates A-C HOLD as a pitch posture. Frame B framing dovetails: gates A-C are precisely the mechanism by which capital underwrites reactor + engineering risk separately from market risk. Worth a synthesis round on the interaction.

3. **R-mars-sample-return-precedent.** Sovereign-bond-class viability (29% P(NPV>0)) requires identifying a sovereign-bond underwriter. Mars Sample Return at $25-30 billion is the closest active analog. What does MSR's policy reception tell us about ICEBERG's pitchability at sovereign-bond?

4. (still queued from round 9) R-fast-cruise-impact-on-h1-floor.

5. (still queued from round 9) R-non-aerocapture-recovery-path-engineering.

## Revisit

Pre-registration accuracy: 5 of 6 HELD; 1 falsified pessimistic. **First round of the three-round sitting where pre-registration BOE arithmetic was correct.** Round 9: BOE largely correct, 9/9 HELD. Round 10: BOE error (forgot launches-per-mission multiplier), 3/6 HELD. Round 11: log-normal fit BOE explicit and validated, 5/6 HELD.

The H6 falsification is direction-correct and methodologically informative — it confirms the matrix's existing venture-retirement decision rather than overturning it. **Falsifying a hypothesis that predicted a matrix-amendment recommendation is the most useful kind of falsification** because it preserves the existing matrix state and provides corroborating numerical evidence.

Three-round sitting cumulative: 17 / 21 sub-claims HELD across rounds 9-11. Four falsifications: 1 in round 10 (arithmetic), 0 in round 9, 1 in round 11 (predicted matrix amendment over-broad). Methodology lessons surfaced: #11 (grade SCOPE against input data), #12 (cross-validate cost anchors), #13 (double-check arithmetic in pre-registration BOE).
