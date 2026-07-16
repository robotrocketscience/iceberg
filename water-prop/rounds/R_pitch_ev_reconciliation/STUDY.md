# R-pitch-ev-reconciliation — STUDY

**Author.** iapetus
**Date.** 2026-05-16 (latest+10)
**Anchor SCOPE.** `SCOPE.md` (commit prior to this round). Sixth round of the reactor-program-targets campaign. First round to question the threshold-framework assumption itself rather than test within it.
**Pre-registered hypotheses.** H1-H6 (see `SCOPE.md` §"Pre-registered hypotheses").

---

## Inputs

Five prior rounds' results, plus pitch text encoded verbatim:

| Source | Path | What it gives |
|---|---|---|
| R-reactor-specific-power-program-targets | `R_reactor_specific_power_program_targets/results/reactor_program_targets.json` | Joint conjunction posterior corners, subjective conditional priors anchor |
| R-demonstrator-window-sensitivity | `R_demonstrator_window_sensitivity/results/demonstrator_window_sensitivity.json` | Window-extension US-base-rate posteriors at 2035 (skeptical 0.0224%, Jeffreys 0.0448%, uniform 0.1008%) |
| R-global-vs-US-base-rate | `R_global_vs_us_base_rate/results/global_vs_us_base_rate.json` | Global+ever uniform posterior at 2035 (0.37%) |
| R-engineering-closure-sensitivity | `R_engineering_closure_sensitivity/results/engineering_closure_sensitivity.json` | Engineering-prior sensitivity grid |
| R-conditional-prior-sensitivity | `R_conditional_prior_sensitivity/results/conditional_prior_sensitivity.json` | All-priors-at-one pathological corner (referenced) |
| ICEBERG-pitch.md | lines 244-246, 263-285, 311-319 | Pitch's gated expected-value framework, gate structure A-D, per-flight unit economics |

No new physics. Composition with the pitch's payoff structure (V, L, p_pitch).

---

## Hypotheses adjudicated

### H1 — Pitch's p=0.50 is implicitly conditional on technology-gates closing positively

**Verdict: CONFIRMED.**

The pitch's gate structure (lines 294-301) tests:
- Gate A (year 1.5): LEO debris capture — bag deployment and capture mechanism
- Gate B (year 3): Cislunar pole demo — bag against ice, chunk-fed water-MET feeding
- Gate C (year 5): Long-duration vacuum qualification — bag MTBF, propulsion power scaling, autonomy
- Gate D (year 2-8 parallel): Long-soak orbital testbed — non-bag subsystems

**None of these gates tests reactor-program delivery.** None tests the engineering-closure rounds (hybrid-aerocapture-aerobraking, B-ring rendezvous survivability). The pitch's line 265 explicitly disclaims demonstrator-gate credit: "Set the success probability for the first Saturn ship at 50%, zero credit for any demonstrator gate having passed." But the "zero credit" refers only to gates A-D — technology gates (reactor program, engineering closures) are silently assumed at probability one.

The post-gates uplift to 0.70 (line 282) explicitly conditions on gates A-C closing, but those are bag-and-architecture flight gates, not technology-development gates. The reactor-program-delivery probability is never composed into the pitch's expected-value math.

### H2 — Composed p ≤ 1.1% optimistic, ≤ 0.003% conservative

**Verdict: CONFIRMED.**

Measured at the chain's anchor corners with pitch p=0.50:

| Anchor | p_chain | p_compound (× 0.50) |
|---|---:|---:|
| conservative_us_skeptical | 0.000224% | 0.00011% |
| conservative_us_jeffreys | 0.000448% | 0.00022% |
| conservative_us_uniform | 0.001008% | 0.00050% |
| optimistic_global_uniform_baseline_eng | 0.006216% | 0.00311% |
| optimistic_global_uniform_lifted_conditionals | 0.055500% | 0.02775% |
| pathological_all_priors_at_one | 0.370000% | 0.18500% |

The optimistic-corner composed p (0.028%) is well below the predicted 1.1% upper bound; the conservative corner (0.0001-0.0005%) is well below the predicted 0.003% upper bound. Both bands held; none of the bands approached the 10 percent threshold that would have falsified H2.

### H3 — Composed expected value negative at all conservative-anchor combinations

**Verdict: CONFIRMED.**

Conservative-anchor expected value at headline payoff (V=$12-24 billion, L=$1 billion):

| Anchor | EV (V=$12B) | EV (V=$24B) |
|---|---:|---:|
| conservative_us_skeptical (× p_pitch=0.50) | $-1.000 billion | $-1.000 billion |
| conservative_us_jeffreys | $-1.000 billion | $-1.000 billion |
| conservative_us_uniform | $-1.000 billion | $-1.000 billion |
| optimistic_global_uniform_baseline_eng | $-1.000 billion | $-0.999 billion |
| optimistic_global_uniform_lifted_conditionals | $-0.996 billion | $-0.993 billion |
| pathological_all_priors_at_one | $-0.976 billion | $-0.954 billion |

18 of 18 conservative-anchor × pitch-p combinations produce negative composed expected value at headline V and L. The composed expected value is approximately equal to $-L$ across all conservative anchors because the composed probability is so small that the (1-p_compound) loss-weight dominates.

### H4 — Required p_technology_gates ≥ 0.50 to recover pitch's $5.5-11.5 billion headline expected value

**Verdict: CONFIRMED with margin.**

Solving for p_compound that produces the pitch's headline expected value:
- Recovering $5.5 billion expected value at V=$12 billion: p_compound = (5.5 + 1) / (12 + 1) = 0.50
- Recovering $11.5 billion expected value at V=$24 billion: p_compound = (11.5 + 1) / (24 + 1) = 0.50

At p_pitch=0.50, both require p_technology_gates = 1.00 — i.e., full technology-gates certainty, exactly the implicit assumption baked into the pitch's headline.

Breakeven (EV=$0) at p_pitch=0.50, V=$12 billion, L=$1 billion: required p_technology_gates = 0.154. The chain's max-optimistic anchor (global+ever uniform, lifted conditionals, baseline engineering) gives p_technology = 0.000555 — **a 277x shortfall to breakeven, 1,800x shortfall to recover the pitch's headline expected value.**

The shortfall is not survivable under any of the chain's anchor adjustments tested in rounds 1-5. To close it, p_technology_gates must lift by approximately three orders of magnitude.

### H5 — Two frameworks measure different probabilities; sequential composition is consistent

**Verdict: CONFIRMED.**

The five-round chain measures p(reactor program delivered AND engineering closures positive); the pitch's worst-case p measures p(bag-architecture validates AND Saturn ops succeed | technology stack works). Mathematically, these are sequential gates: p_compound = p_chain × p_pitch. The contradiction in headline readings — "tech-demonstrator-only" vs. "twelve-to-twenty-four-times asymmetric" — dissolves under composition.

But that dissolution does not rescue the pitch's headline. The composition produces composed expected values that are uniformly negative under conservative anchors and only marginally positive (+$19 million) at a single pathological corner (all-priors-at-one × p_pitch=0.70 × V=$200B induced-demand × L=$0.5B). The composition is mathematically consistent; the economic implication is unforgiving.

### H6 — Chain's tech-demonstrator-only reading REINFORCED, not softened

**Verdict: CONFIRMED.**

Full sweep statistics:
- 432 (tech_anchor × pitch_anchor × V × L) corners tested
- 1 corner produces positive composed expected value (+$19 million)
- 0 corners produce positive expected value at non-pathological tech anchors

The single positive corner is the pathological all-priors-at-one tech anchor combined with the pitch's post-gates p=0.70 and induced-demand V=$200 billion and lowest L=$0.5 billion. It is a worst-case-of-pessimism-meets-best-case-of-optimism artifact, not a defensible decision case.

The chain's H6 reading from rounds 1-5 was "technology-demonstrator-only by capital class because joint conjunction is below venture-class probability threshold." Under expected-value reconciliation, that reading expands to: "technology-demonstrator-only by capital class AND composed expected value is negative under conservative anchors AND the pitch's headline expected value requires technology-gates certainty that the chain's anchors do not support."

The reading is reinforced, not softened.

---

## Headline

Under composed expected-value framing (the pitch's $5.5-11.5 billion headline composed with the five-round chain's joint conjunction posterior on technology gates), **composed expected value is negative across all 432 sweep corners except a single pathological corner (+$19 million)**. The pitch's positive expected value requires p_technology_gates approximately 1.0, which the chain's anchors do not support: max-optimistic anchor delivers 0.0555 percent, a 1,800x shortfall to recover the headline expected value and a 277x shortfall to even break even. The pitch and the chain measure different (sequential) probabilities; composition is mathematically consistent but economically unforgiving.

---

## Reading

**Matrix decision point #1 reading expands.** From rounds 1-5: "technology-demonstrator-only by capital class because conjunction posterior is below venture probability threshold." From this round: "technology-demonstrator-only by capital class AND composed expected value under headline payoff structure is negative under every non-pathological anchor AND the pitch's positive-expected-value claim depends on an implicit technology-gates certainty assumption that the conservative anchors do not support."

**The pitch is not wrong, but its EV calculation conditions on the chain's "yes" outcome without computing the chain's probability.** That is a publishable accounting gap. Three project-owner options surfaced (preserving order from the SCOPE):

1. **Bracket the pitch's p over technology-gates uncertainty explicitly.** Restate the headline as: "p_compound = p_technology × 0.50, where p_technology is the joint posterior on reactor program delivery, hybrid-aerocapture-aerobraking closure, and B-ring rendezvous survivability closure. Expected value as a function of p_technology is shown in a bracket figure." The pitch becomes honest at the cost of replacing one number with a curve.

2. **State that the expected value is conditional on technology gates having closed and that the program is structured to spend up to a technology-gates kill budget before committing to flight gates.** This converts the program from terminal-bet to staged-options, bounds max-loss at the technology-gates kill budget rather than at $1 billion, and gives a different (likely smaller-magnitude but positive-expected-value) headline. The staged-options framing matches the user-locked anchor-investment-thesis framing: "incremental capital allocated to ICEBERG as a sleeve within the larger anchor round, with separate milestone reporting and separate go/no-go decisions at each demonstrator."

3. **Source private information lifting technology-gates posteriors materially above the chain's published anchors.** If the project owner has access to (a) an FSP-2 award signal at the contract-near-issuance stage, (b) private engineering results on hybrid aerocapture, or (c) a closure path on B-ring rendezvous survivability — each could plausibly lift p_technology by an order of magnitude. Multiple such lifts compound. The information has to be documented transparently and the recomposed expected value reported with that documentation; otherwise the lift looks like motivated reasoning to a reviewing capital allocator.

**Project-owner recommendation:** option (2) is the highest-yield revision. It matches the gated-options structure already articulated in the anchor-investment framing, makes the pitch defensible to a sophisticated capital allocator, and surfaces the technology-gates-kill budget as the load-bearing financial commitment. Option (1) is a transparency upgrade. Option (3) is conditional on the project owner having the private information; if so, it is the pitch's most powerful move, but it requires explicit framing.

---

## Cross-learning

- **Rounds 1-5 strengthened, not softened.** The five-round threshold-framework chain converged on "technology-demonstrator-only." Composed expected-value framing reinforces that reading. Far from being a different lens that softens the conclusion, it tightens it: the pitch's positive-expected-value claim is shown to depend on an implicit assumption that the chain's anchors do not support.
- **The pitch's lines 263-282 are honest about the framing it uses.** The line 282 disclosure "before any credit for the gates that actually retire the technical risk" is candid about the demonstrator-gate exclusion. But the disclosure does not extend to technology-development gates. The honest revision is to extend the disclosure: "before any credit for the gates that actually retire the technical risk AND assuming technology stack works."
- **The user-locked anchor-investment framing already articulates option (2).** Belief 76fd04cdba8b2c3b: "ICEBERG is structured as an additional capital line on top of that core trajectory — funded specifically for the long-horizon Saturn-class play, gated by demonstrator flights every ~2 years, with explicit kill criteria at each gate." This is the structure that, formalized as an options-with-gates decision tree, would supersede the pitch's terminal-bet expected-value math. Round 7 candidate is the formal options-tree round.
- **R-power-bayesian-update (hyperion)** is the upstream anchor on US-fission orbit posteriors. This round propagates that posterior through to the composed expected value, confirming that the Bayesian floor is dominant in every conjunction. No update to hyperion's bracket required.
- **R-power-wonder findings (user-locked May 2026)** all feed into the chain's conservative anchors. Findings 1 (40 W/kg is paper-figure), 2 (0-of-6 US base rate), 3 (FSP Phase 2 not awarded), 4 (radiators are 40-55 percent of mass at megawatt scale) collectively make the conservative anchor the load-bearing one. Composing it with the pitch's payoff structure produces the negative-expected-value result.
- **Methodology lesson 14 candidate (from round 5).** Distinguish single-axis from joint-axis robustness. This round adds: distinguish single-framework from composed-framework readings. The five-round chain's H6 was robust to single-framework lifts (window, base-rate, conditional priors, engineering priors). It is also robust to composed-framework reconciliation with the pitch's payoff structure.

---

## Next-round candidates

1. **R-staged-options-with-technology-gates.** Formalize option (2) above as a decision-tree expected value with kill-at-each-technology-gate. Each gate has a closure probability anchored on the chain's outputs; cumulative spend at each kill point is bounded; conditional on reaching the next gate, the program advances. Expected NRE and expected value computed as stochastic over the chain's anchor grid. Worth running. This is the round that would directly underwrite the project-owner's anchor-investment-thesis framing.

2. **R-induced-demand-payoff-sensitivity.** At V=$50-200 billion (pitch line 284 induced-demand upside), how does the composed-expected-value picture shift? This round's single positive corner suggests the picture might brighten at very-high V, but only at pathological tech anchors. Worth a clean check to see whether non-pathological anchors recover at induced-demand V. Lower priority than #1 but lower-cost too.

3. **R-private-information-bracket.** What magnitude of private-information lift on technology-gates posteriors would be required to recover the pitch's headline expected value? Express as: at p_pitch=0.50, V=$12-24 billion, L=$1 billion, the breakeven p_technology is 0.077-0.154. The required lift over the chain's max-optimistic anchor is 139x-277x. Is that lift plausible from any single private-information channel (FSP-2 signal, engineering closure, etc.)? Could be a follow-on synthesis.

4. **Pitch-text revision recommendation document.** If the project owner accepts option (1) or (2), the pitch lines 263-285 and the campaign-gates table (lines 311-318) need specific revision. A deliverable document for project-owner work — not a worker round.

---

## Methodology notes (lessons applied)

- **Lesson 7 (pessimistic-anchor-first).** Conservative US-base-rate skeptical prior used as the load-bearing anchor; optimistic global+ever uniform used as the secondary anchor; pathological all-priors-at-one used only for upper-bound sensitivity.
- **Lesson 9 (anchor SCOPE on prior aggregate verdict).** This round anchors on the five-round chain's H6 verdict aggregate (rounds 1-5) and reconciles it against the pitch's headline expected value. No cherry-picking of a single sub-finding.
- **Lesson 14 candidate (round 5).** Distinguish single-axis from joint-axis robustness — extended here to: distinguish single-framework from composed-framework readings. The chain's H6 is robust to both kinds of sensitivity.

---

## Files

- `SCOPE.md` — pre-registration (iapetus, 2026-05-16)
- `run.py` — composition + sweep + breakeven analysis
- `results/pitch_ev_reconciliation.json` — full sweep (432 corners), breakeven table, hypothesis verdicts
