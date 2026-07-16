# R-pitch-ev-reconciliation — does the pitch's positive expected value survive composition with the five-round chain's technology-conjunction posterior?

**Status:** scope, pre-study. Authored by iapetus, 2026-05-16. Sixth round of the iapetus reactor-program-targets campaign; directly questions the assumption that has gone unchallenged across rounds 1-5.

---

## The unchallenged assumption

Rounds 1-5 read the matrix decision point #1 as **technology-demonstrator-only** by computing the joint conjunction posterior across (US fission orbit by demonstrator window 2032-2035) × (specific power ≥ S | orbit) × (lifetime ≥ L | orbit) × (aerocapture credit X ≥ X_min | hybrid-aerocapture-aerobraking closes) × (engineering rounds close). The reading is a **probability-threshold capital-class** statement: the conjunction is below the venture-class 10 percent and corporate-growth-class 30 percent thresholds.

The pitch (`ICEBERG-pitch.md`, lines 263-282) makes a separate claim under **a different framework** — gated expected-value with capped downside:

```
Max credible loss            L  =  $1.0 billion (program writeoff)
Long-run program value       V  =  $12 billion (low) to $24 billion (high)
P(success), worst case       p  =  0.50
Net expected value           =  $5.5 billion to $11.5 billion
Upside / downside (probability-weighted) = 12x to 24x
```

These two readings appear contradictory: rounds 1-5 say "technology-demonstrator-only;" the pitch says "twelve-to-twenty-four-times asymmetric expected value, fund the venture." **Either at least one is wrong, or they measure different things.** No round so far has reconciled them.

The honest reading hinges on what each "p" measures. The pitch's gates A-C (LEO debris demo, cislunar pole demo, long-duration vacuum qual) and gate D (long-soak orbital testbed) all test the **bag-and-architecture subsystem and integrated-system reliability**. None of them tests **reactor-program delivery** or the **engineering-closure rounds** (hybrid-aerocapture-aerobraking, B-ring rendezvous survivability) — those are the gates the five-round chain has been computing posteriors for. The pitch's p = 0.50 therefore reads as conditional on technology-gates closing positively. If composed properly:

p_compound = p_technology_gates × p_pitch_p

where p_technology_gates is the five-round chain's joint conjunction posterior (≤ 0.0055 percent optimistic, ≤ 0.00006 percent conservative). The pitch's positive expected value requires p_technology_gates ≈ 1, which the chain's conservative anchors do not support.

This round composes the two frameworks, computes the composed expected value across the chain's anchor grid, and adjudicates whether the pitch's headline expected value survives.

---

## Question this round answers

For the held chunk-rendezvous architecture (axis 19) under conservative anchors (matrix state as of latest+8 plus the five-round chain's findings), and using the pitch's payoff structure (long-run program value $12-24 billion over ~20-year horizon, max credible loss $1 billion):

1. **Does the pitch explicitly compose technology-gates uncertainty into the p = 0.50 worst-case framing?** Examine the pitch's gate table and surrounding text for explicit composition.
2. **What is the composed expected value (p_technology × p_pitch × V minus (1 minus composed) × L) across the chain's anchor grid?**
3. **At what minimum p_technology does the composed expected value go positive?** Compare to the chain's max optimistic-anchor conjunction posterior.
4. **What is the reading-level reconciliation: are the two frameworks consistent, contradictory, or measuring different things requiring explicit framing?**

---

## Pre-registered hypotheses (numeric ranges + falsification bands)

| # | Hypothesis | Predicted range | Falsification band |
|---|---|---|---|
| H1 | The pitch's worst-case p = 0.50 is implicitly conditional on technology-gates closing positively. The pitch text does not explicitly compose technology-gates uncertainty into the expected value. | predicted: pitch's gates A-D test bag-and-architecture, not reactor-program delivery; the EV calculation assumes technology gates closed | H1 falsified if pitch text explicitly composes reactor-program-delivery posterior or engineering-closure posterior into p = 0.50 |
| H2 | Under proper composition with the five-round chain's joint-conjunction posterior, the composed p is ≤ 1.1 percent at the chain's most-optimistic anchor (global+ever uniform, all conditional priors at 1.0, engineering priors at baseline 0.5 × 0.30 = 0.15, multiplied by pitch's 0.50). At conservative anchors, composed p is ≤ 0.003 percent. | predicted: composed p ≤ 0.011 optimistic, ≤ 0.00003 conservative | H2 falsified if composed p exceeds 0.10 (i.e., 10 percent) under any of the three base-rate priors and any of the tested window-extensions |
| H3 | Composed expected value (p_compound × V minus (1 minus p_compound) × L) is negative at all conservative-anchor combinations using the pitch's V = $12-24 billion and L = $1 billion. | predicted: composed expected value is in the range minus $0.78 billion to minus $1.0 billion under conservative anchors; minus $0.74 billion to minus $0.86 billion under optimistic anchors | H3 falsified if any anchor combination produces composed expected value positive without invoking the pathological all-priors-at-one corner identified in round 5 |
| H4 | For the pitch's positive expected value to hold ($5.5 billion to $11.5 billion), p_technology_gates must be ≥ 50 percent. That is roughly 23 times higher than the chain's most-optimistic anchor (2.18 percent) and 9,000 times higher than the conservative-anchor estimate. | predicted: required p_technology_gates ≥ 0.50 to recover the pitch's headline expected value | H4 falsified if positive expected value holds at p_technology_gates below 0.20 |
| H5 | The two frameworks are NOT contradictory; they measure different probabilities. The pitch's p = 0.50 is p(bag-architecture validates AND Saturn ops succeed, conditional on reactor program delivered and engineering closures positive). The five-round chain's p_conjunction is p(reactor program delivered AND engineering closures positive). The honest pitch composition is p_compound = p_chain × p_pitch. Under that composition, headlines disagree because the pitch implicitly conditions on the chain's "yes" outcome. | predicted: H5 confirmed — the two are sequential gates, properly composed multiplicatively; the contradiction dissolves under composition but the pitch's headline expected value does not survive | H5 falsified if the pitch's p = 0.50 already explicitly composes reactor-program-delivery posterior, OR if the two frameworks are mutually exclusive (not sequential) |
| H6 | Reading-level conclusion (load-bearing, retrospective): the five-round H6 chain's "technology-demonstrator-only" reading is REINFORCED by composed-expected-value reconciliation, not softened. Composing the chain's joint conjunction with the pitch's payoff structure produces **negative composed expected value at every non-pathological anchor**. The honest pitch needs to either (a) bracket p over technology-gates uncertainty explicitly, (b) state that the expected value is conditional on technology-gates closing positively, or (c) source private information lifting technology-gates posteriors materially above the chain's anchors. | predicted: H6 reinforced; the matrix decision point #1 reading expands from "tech-demonstrator-only by capital class" to "tech-demonstrator-only by capital class AND pitch expected value calculations must explicitly compose technology gates to be honest" | H6 falsified if any non-pathological composed-expected-value calculation gives positive returns AND the chain's anchor underestimates p_technology_gates by a documentable amount |

---

## Method sketch

1. **Load prior-round outputs:**
   - `R_reactor_specific_power_program_targets/results/reactor_program_targets.json` — joint conjunction posterior corners (anchored 2032-2035 window)
   - `R_demonstrator_window_sensitivity/results/demonstrator_window_sensitivity.json` — window-extension sensitivity
   - `R_global_vs_us_base_rate/results/global_vs_us_base_rate.json` — base-rate widening sensitivity
   - `R_engineering_closure_sensitivity/results/engineering_closure_sensitivity.json` — engineering-prior sensitivity
   - `R_conditional_prior_sensitivity/results/conditional_prior_sensitivity.json` — subjective conditional sensitivity

2. **Encode pitch numbers** verbatim from `ICEBERG-pitch.md` lines 270-276 and lines 244-246:
   - V_low = $12 billion, V_high = $24 billion (20-year perpetuity NPV)
   - L = $1.0 billion (max credible loss)
   - p_pitch_worst = 0.50 (worst-case before-gate-credit)
   - p_pitch_post_gates = 0.70 (after gates A-C close)
   - V_floor = ship-3 floor case: 50-tonne chunk, $400M cost, $370M/yr, p_floor = 0.10-0.25
   - V_upside_A = 100-200 tonne chunk, p = 0.30
   - V_upside_B = 300 tonne chunk, p = 0.55

3. **Compose probability streams:**
   - p_compound = p_technology_gates × p_pitch
   - p_technology_gates anchors: conservative (skeptical, US-only 2032-2035 window), optimistic (global+ever uniform, max single-axis lift), pathological (all-priors-at-one corner from round 5)
   - p_pitch values: 0.10 (floor pessimistic), 0.25 (floor optimistic), 0.50 (pitch worst-case), 0.70 (post-gate)

4. **Compute composed expected value:**
   - For each (p_technology, p_pitch, V, L) combination:
     - EV = p_compound × V minus (1 minus p_compound) × L
   - Sweep across V in {12, 18, 24, 50, 100, 200} billion (pitch's headline plus induced-demand upside per line 284)
   - Sweep across L in {0.5, 1.0, 2.0} billion

5. **Identify breakeven:**
   - Solve for p_compound where EV = 0: p_breakeven = L / (V + L)
   - Compute required p_technology_gates given each p_pitch: p_tech_req = p_breakeven / p_pitch
   - Compare to chain's max conjunction posterior

6. **Reading-level synthesis:**
   - Are the two frameworks reconcilable?
   - What does the project owner need to add to the pitch for honest composition?
   - Does the chain's H6 strengthen or weaken under expected-value framing?

---

## Reading template (5-section round template, worker fills in after run)

- **Hypotheses adjudicated.** Verdict per H1-H6, predicted vs measured composed expected values.
- **Headline.** One-line: does the pitch's positive expected value survive composition with the technology-gates conjunction?
- **Reading.** Project-owner-decision level: what does the pitch need to change to be honest under composed expected-value framing?
- **Cross-learning.** Connection to rounds 1-5 of the iapetus campaign; to the pitch's gate structure; to the user-locked R-power-wonder findings on reactor-program base rates.
- **Next-round candidates.** Whether further sensitivity is needed, whether the pitch text requires explicit revision recommendations, or whether matrix decision point #1 amendment is unblocked.

---

## Worker notes

- **Round priority:** **high.** This is the first round in the iapetus campaign to question the threshold-framework assumption itself rather than testing within it. The unchallenged-assumption critique.
- **Method:** synthesis composition + decision-theoretic expected-value. No new physics; the inputs are prior-round conjunction posteriors and pitch text.
- **Out of scope:** revising the pitch (project-owner work); computing options value with kill-at-each-gate decision tree (a candidate for a follow-on round if H6 holds and the project owner wants the full gated-options framing); computing per-flight unit economics (already covered in pitch tables 313-318).
- **Methodology lessons applied:** lesson 7 (pessimistic-anchor-first), lesson 9 (anchor SCOPE on prior aggregate verdict — the five-round chain's H6 is the verdict being reconciled against), lesson 14 candidate from round 5 (distinguish single-axis from joint-axis robustness, here extended to distinguishing single-framework from composed-framework readings).
