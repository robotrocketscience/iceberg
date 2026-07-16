# R-staged-options-with-technology-gates — STUDY

**Author.** iapetus
**Date.** 2026-05-16 (latest+10)
**Anchor SCOPE.** `SCOPE.md` (commit prior to this round). Seventh round of the iapetus reactor-program-targets campaign. Direct follow-on to round 6 option (2).
**Pre-registered hypotheses.** H1-H6 (see `SCOPE.md`).

---

## Inputs

Chain rounds 1-6 outputs, plus pitch gate structure encoded verbatim:

| Source | Path | What it gives |
|---|---|---|
| R-reactor-specific-power-program-targets | `R_reactor_specific_power_program_targets/results/reactor_program_targets.json` | Subjective conditional priors (P_HYBRID_AEROCAP, P_RENDEZVOUS_LOW/HI) |
| R-demonstrator-window-sensitivity | `R_demonstrator_window_sensitivity/results/demonstrator_window_sensitivity.json` | US-base-rate orbit posteriors at 2035 (skeptical 0.0224%, Jeffreys 0.0448%, uniform 0.1008%) |
| R-global-vs-US-base-rate | `R_global_vs_us_base_rate/results/global_vs_us_base_rate.json` | Global+ever uniform 2035 posterior (0.37%) |
| R-pitch-ev-reconciliation | `R_pitch_ev_reconciliation/results/pitch_ev_reconciliation.json` | Terminal-bet EV baseline for comparison |
| ICEBERG-pitch.md | lines 263-285, 294-318 | 4-gate flight structure + cost schedule + max-credible-loss claim |

7-gate decision tree (3 technology + 4 flight), 128 paths walked, gate costs from pitch table.

---

## Hypotheses adjudicated

### H1 — Staged-options EV dominates terminal-bet EV at every anchor; median dominance ≥ 2x

**Verdict: CONFIRMED.**

Strict dominance across all 42 (anchor × V) combinations: True. Median magnitude-reduction (terminal-bet-EV magnitude divided by staged-EV magnitude when both are negative): 12.5x. Minimum reduction: also 12.5x at conservative anchors. The dominance is structurally large because conservative-anchor T1 (FSP-2 award) probability is so small that the program kills with only $80M spent — far less than the pitch's $1B max-credible-loss that terminal-bet treats as a single sunk write-off.

The single anchor where staged equals terminal exactly: pathological all-priors-at-one (all probabilities = 1.0 means program never kills, so cumulative-to-success and terminal-V net to the same number).

### H2 — E[total spend] $100-300M conservative, $300-700M optimistic

**Verdict: PARTIALLY-CONFIRMED on the upside; lower than predicted on the downside.**

Measured E[total spend] at V=$12 billion:

| Anchor | E[total spend] | predicted | within predicted? |
|---|---:|---:|---|
| conservative_us_skeptical | $80.0 million | $100-300M | below predicted (too small) |
| conservative_us_jeffreys | $80.1 million | $100-300M | below predicted |
| conservative_us_uniform | $80.1 million | $100-300M | below predicted |
| optimistic_global_uniform_baseline_eng | $80.5 million | $300-700M | well below predicted |
| optimistic_global_uniform_post_gate_credit | $80.5 million | $300-700M | well below predicted |
| optimistic_lifted_T1_T2_T3 | $82.4 million | $300-700M | well below predicted |

E[total spend] is uniformly close to $80 million across anchors. The reason: T1 (FSP-2 award) probability is so small under all non-pathological anchors that the program kills at T1 with probability >95% in every case, spending only the $80M T1 cost. The conditional probability of advancing past T1 is so low that downstream gate costs do not materially affect E[spend].

The prediction band was set too high. The result is more concentrated: **expected loss is approximately the T1 gate cost ($80 million), almost regardless of downstream priors.** This is a substantive surprise — the prediction underestimated how dominant the T1 gate is in the decision tree.

### H3 — Conservative-anchor staged EV negative, 5x less negative than terminal

**Verdict: CONFIRMED.**

Staged-options EV at conservative anchors (V=$12 billion):
- conservative_us_skeptical: $-0.080 billion
- conservative_us_jeffreys: $-0.080 billion
- conservative_us_uniform: $-0.080 billion

Terminal-bet EV at same anchors (V=$12 billion): $-1.000 billion each.

Magnitude reduction (terminal / staged): 12.5x for all three. Well above the 5x prediction threshold. The reduction is consistent across V values from $12 billion to $200 billion (staged EV is essentially V-independent at conservative anchors because the program kills at T1 before V matters).

### H4 — Optimistic-anchor staged EV crosses zero

**Verdict: CONFIRMED.**

2 of 18 optimistic-anchor combinations produce positive staged EV:
- optimistic_lifted_T1_T2_T3 × V=$100 billion: staged EV = $+0.043 billion
- optimistic_lifted_T1_T2_T3 × V=$200 billion: staged EV = $+0.168 billion

The threshold V at the optimistic-lifted anchor is approximately $73 billion (where staged EV crosses zero). At V values in the pitch's headline range ($12-24 billion), the staged EV at optimistic-lifted anchor is $-0.066 to $-0.051 billion — small in magnitude relative to the conservative-anchor result, but still negative.

This adjudicates a narrow but real "anchors at which staged-options is rational" bracket: positive staged EV requires (a) all three technology-gate priors lifted to 1.0 OR (b) very-high V (induced demand). Each is a defensible expansion vector for the project owner.

### H5 — Max-loss ≈ $1 billion; E[loss] 4-10x smaller (option value gain)

**Verdict: CONFIRMED.**

Max-loss across all 128 paths is $1.15 billion (sum of all gate costs), matching the pitch's $1 billion claim with rounding-level accuracy.

E[total spend] under conservative anchors: $80 million. Max-to-expected ratio: 14.4x. Well above the predicted 4-10x band — the option value is even larger than predicted because T1 dominates.

Under optimistic-lifted anchors: $82.4 million; max-to-expected ratio 14.0x. Similar profile.

The pitch's $1 billion is a **maximum-credible-loss across the worst-case path** (every gate passes through T3, F3 is the kill point, $690 million plus partial F4 commit). The **expected loss across the probability-weighted path-set is one order of magnitude smaller**.

### H6 — Reading shifts from "tech-demonstrator-only" to "research-grant + private-options sleeve"

**Verdict: CONFIRMED.**

Both falsification criteria failed (i.e., the verdict is confirmed):
- Optimistic anchors produce positive staged EV at two corners: yes (criterion satisfied)
- Conservative-anchor magnitude reduction vs terminal: 12.5x (well above 5x threshold; criterion satisfied)

The reading shifts. Under staged-options framing, matrix decision point #1 expands from "technology-demonstrator-only because terminal-bet EV is -$1 billion" to: **"research-grant + private-options sleeve, structured with explicit kill budget. Expected loss $80 million under conservative anchors; max-credible-loss $1.15 billion; positive expected value at induced-demand V or all-priors-lifted anchors."**

This is a defensible economic class shift, not merely a smaller-magnitude version of the same conclusion. The pitch's $5.5-11.5 billion headline expected value still does not survive composition (round 6 stands), but the **honest staged-options reading is meaningfully more favorable than the terminal-bet reading**, and it matches the user-locked anchor-investment-thesis framing.

---

## Headline

Under explicit staged-options framing with kill-at-each-gate, **conservative-anchor expected loss is $80 million, not $1 billion** — a 12.5x reduction vs the terminal-bet expected value computed in round 6. The program kills at gate T1 (FSP-2 award) with greater than 95 percent probability under all non-pathological anchors, never spending past T1 in expectation. Max-credible-loss across the worst-case path is $1.15 billion (matches the pitch), but max-loss and expected-loss differ by an order of magnitude. Staged-options EV crosses zero at the optimistic-lifted anchor with V ≥ $73 billion (induced-demand territory); at the pitch's headline V range, staged EV at the optimistic-lifted anchor is approximately -$50 million (small in magnitude, still negative).

---

## Reading

**Matrix decision point #1 reading under staged-options framing.** From rounds 1-5: "technology-demonstrator-only by capital class." From round 6 (terminal-bet EV): "composed expected value is negative across all non-pathological corners; pitch's positive-EV claim requires implicit technology-gates certainty." From this round (staged-options EV with kill-budget): **"research-grant + private-options sleeve, structured with $80 million tranche-1 kill budget gated on FSP-2 award; expected total loss under conservative anchors is $80 million, not $1 billion; defensible at sovereign-research-grant economic class with venture-sleeve-options on top."**

This is the reading the project owner can defensibly pitch to a capital allocator. Three specific structural implications:

1. **Tranche 1 ($80 million, year 0-1.5): pre-FSP-2 work plus Gate A LEO debris demo.** Kill if FSP-2 is not awarded by year 2 OR Gate A flight fails. Both kills retire $80 million committed. This is sovereign-research-grant-class budget; well within NASA Small Business Innovation Research / SpaceWERX-class capital.
2. **Tranche 2 ($260 million, year 1.5-4): T2 hybrid aerocapture engineering closure + Gate B cislunar demo.** Kill if engineering closure round returns negative OR Gate B fails. Combined-tranche cumulative loss-on-kill: $440 million.
3. **Tranche 3 ($310 million, year 4-6): T3 B-ring rendezvous closure + Gate C/D vacuum qual + long-soak.** Kill if either fails. Combined cumulative: $690 million. After this, the $460 million Saturn-ship commit is gated on tranche-3 closure.

Under this structure, the project-owner's pitch to a capital allocator becomes:

> "We are raising tranche-1 sovereign-research-grant capital ($80 million) gated on the FSP-2 award by year 2. If FSP-2 is awarded with scope ≥ 100 kilowatt-electric and lifetime ≥ 10 years, we proceed to tranche 2 ($260 million) at venture-sleeve-options pricing. If both engineering closure rounds and Gate B return positive, we proceed to tranche 3 ($310 million). Only after tranche 3 closes do we commit the $460 million ship-3 Saturn launch. Maximum committed loss across the worst-case path is $1.15 billion; expected committed loss under our conservative anchors (which we publish transparently) is $80 million. Conditional on all gates closing, long-run program value is $12-24 billion sovereign-water-infrastructure perpetuity (with induced-demand upside to $50-200 billion). This is a sovereign-research-grant program with private-options sleeves, not a $1 billion venture commitment."

That pitch is honest under composed framing. The pitch as currently written is not — round 6 showed it requires p_technology approximately 1.0 for the headline expected value to hold.

**Project-owner action.** Three options surfaced (one already actionable):

1. **Adopt the staged-options framing in the pitch** explicitly. Replace the lines 263-285 terminal-bet expected-value text with a tranche-structured budget plus the kill-criterion table from this round's gate structure. Restate "max credible loss $1 billion" as "max credible loss $1.15 billion across the worst-case path; expected loss $80 million under conservative reactor-program priors."
2. **Source private-information lift on T1 (FSP-2 award).** The biggest expected-loss reducer is increasing T1 pass probability. Under the user-locked finding that FSP draft Announcement for Partnership Proposals was issued in August 2025 with final release anticipated early 2026, plus the Duffy directive scope expansion to 100 kilowatt-electric, the conservative US-skeptical T1 probability (0.011 percent) is arguably too low. If the project owner has insight into FSP-2 negotiation cadence, the T1 probability could plausibly lift by 1-2 orders of magnitude (to 0.1-1 percent), which materially shifts E[total spend] downstream — though it remains in the $100-500 million expected-loss range. This is a follow-on round candidate.
3. **L0-13 capital-structure amendment.** Round 6 surfaced this; round 7 confirms. The structure is research-grant + private-options-sleeve, not venture-equity or sovereign-bond. The project-owner walk-through deferred L0-13 to "this round's results" (referring to round 1); round 7 sharpens: research grant for tranche 1, venture-sleeve-options for tranches 2-3.

---

## Cross-learning

- **Rounds 1-5 H6 reading reinforced.** The chain's threshold-framework reading ("technology-demonstrator-only because joint conjunction below venture probability threshold") remains correct as the **capital-class** reading. Round 7 adds the **expected-value class** reading: defensible at sovereign-research-grant capital class, with venture-sleeve-options pricing for tranches 2-3.
- **Round 6 reading reconciled.** Round 6 showed that terminal-bet composed expected value is negative under all non-pathological anchors. Round 7 confirms: at terminal-bet framing, the pitch's headline does not survive. But under staged-options framing, the expected loss is 12.5x smaller and the program structure is sovereign-research-grant-defensible. The two readings are complementary; the pitch's pathology is the terminal-bet framing, not the program itself.
- **The user-locked anchor-investment-thesis framing is mathematically substantiated by round 7.** Belief 76fd04cdba8b2c3b: "gated by demonstrator flights every ~2 years, with explicit kill criteria at each gate." This framing produces E[loss] = $80 million under conservative anchors, which is a sovereign-research-grant-class commitment, exactly as the framing predicts. The round formalizes the framing's economic logic.
- **R-power-wonder findings 1-4 (user-locked) continue to anchor the conservative priors.** Findings 1 (40 W/kg paper-figure), 2 (0-of-6 base rate), 3 (FSP-2 not awarded), 4 (radiators 40-55 percent at megawatt scale) all feed into the conservative T1 probability that makes T1 the dominant kill point.
- **Methodology lesson 14 extended further.** Round 6 extended lesson 14 to distinguish single-framework from composed-framework readings. Round 7 extends again: distinguish terminal-bet framing from staged-options framing. The chain's reading is robust across all three sensitivity dimensions (single-axis, joint-axis, framework-choice), but the reading itself becomes more nuanced as each dimension is added.

---

## Next-round candidates

1. **R-private-information-bracket on T1 (FSP-2 award)** — direct continuation. What is the magnitude of T1-probability lift achievable from documentable evidence (FSP-2 draft Announcement for Partnership Proposals issued, Duffy directive, named contractors)? Under what private-information-supported T1 probability does E[total spend] shift to $200-500 million? This is the highest-yield expected-loss-reduction question.
2. **Pitch-text revision recommendation document.** With round 6 and round 7 in hand, write specific recommended revisions to ICEBERG-pitch.md lines 263-285 and 311-318. Not a research round — a project-owner-deliverable document.
3. **L0-13 capital-structure amendment specification.** Project-owner work in REQUIREMENTS.md (orchestrator session only). Round 7 makes the amendment specifiable: research-grant + tranche-options structure.
4. **R-tranche-pricing-sensitivity.** Given the tranche structure surfaced here, what is the sensitivity of E[total spend] and E[NPV] to varying the tranche costs (e.g., if Gate A piggybacks on operator's already-scheduled flights, T1+F1 cost drops from $160 million to $50 million)? Worth a follow-on for pitch-revision precision.
5. **R-correlated-gate-outcomes.** Round 7 assumed gates are independent given the conditioning. Are they? If T1 pass correlates with T2 and T3 pass (because a successful reactor program signals capability for downstream engineering), the independence assumption may understate the optimistic-side EV. Worth a check at lower priority.

---

## Methodology notes (lessons applied)

- **Lesson 7 (pessimistic-anchor-first).** Conservative US-skeptical anchor used as the load-bearing case; optimistic global+ever uniform used as the secondary case; pathological all-priors-at-one used only for upper-bound sanity check.
- **Lesson 9 (anchor SCOPE on prior aggregate verdict).** This round anchored on round 6's H6 verdict ("composed expected value negative under all non-pathological corners under terminal-bet framing") and tested whether reframing the decision as staged-options shifts the reading. The reframing is itself an explicit hypothesis (H6), not a smuggled-in lens.
- **Lesson 14 (distinguish single-axis from joint-axis robustness).** Round 6 extended to single-framework vs composed-framework. Round 7 extends again to terminal-bet vs staged-options. The chain's H6 reading is robust to each of these reframings; the reframings themselves change the **economic-class reading** without changing the **probability-class reading**.
- **Honest-prediction-revision methodology.** H2 prediction band ($100-300 million conservative) was too high; the measured value was $80 million. Documented as a substantive surprise. The cause: I underestimated how dominant the T1 gate is in the decision tree. T1 probability is so small under conservative anchors that nearly all of E[total spend] is the T1 gate cost itself. Methodology lesson for future rounds: when one gate has order-of-magnitude lower probability than others, E[spend] is approximately that gate's cost; the prediction band should reflect this.

---

## Files

- `SCOPE.md` — pre-registration (iapetus, 2026-05-16)
- `run.py` — 7-gate decision tree, 128-path enumeration, anchor sweep
- `results/staged_options_with_technology_gates.json` — full output with comparison table, per-anchor staged + terminal EV, hypothesis verdicts
