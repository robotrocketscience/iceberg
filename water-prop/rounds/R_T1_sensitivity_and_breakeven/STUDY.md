# R-T1-sensitivity-and-breakeven — STUDY

**Author.** iapetus
**Date.** 2026-05-16 (latest+10)
**Anchor SCOPE.** `SCOPE.md`. Eighth round of the iapetus reactor-program-targets campaign. Direct follow-on to round 7 surfaced T1 dominance.
**Pre-registered hypotheses.** H1-H6 (see `SCOPE.md`).

---

## Inputs

Round 7 staged-options decision tree (7 gates, 128 paths) plus public-evidence Bayes-factor compounding using user-locked R-power-wonder findings (May 2026):

| Source | Path / Reference | What it gives |
|---|---|---|
| R-staged-options-with-technology-gates | `R_staged_options_with_technology_gates/results/staged_options_with_technology_gates.json` | Gate structure, baseline non-T1 probabilities, total program cost $1.15 billion |
| user-locked R-power-wonder finding 2 | (May 2026) | 0-of-6 US base rate, FSP-2 status |
| user-locked R-power-wonder finding 3 | (May 2026) | Draft AFP issued Aug 2025, Duffy directive scope 100 kWe, schedule slip, FY26 budget zeroed NEP/NTP, DRACO cancelled |

Sweep T1 across {0.0001, 0.001, 0.005, 0.01, 0.05, 0.1, 0.2, 0.3, 0.5}. Hold F1, T2, F2, T3, F3, F4 at round 7 baseline (chain conservative anchors).

---

## Hypotheses adjudicated

### H1 — Breakeven T1 at V=$24 billion in [0.15, 0.30]

**Verdict: CONFIRMED.**

Measured breakeven T1 at V=$24 billion: **0.250** (binary search converged). Within predicted range [0.15, 0.30].

Full breakeven table:

| V ($ billion) | Breakeven T1 |
|---:|---:|
| 12 | none (staged EV negative even at T1=1.0) |
| 18 | 0.454 |
| 24 | 0.250 |
| 50 | 0.085 |
| 100 | 0.037 |
| 200 | 0.018 |

**Notable: at V=$12 billion (the pitch's low headline), staged EV remains negative even at T1 = 1.0.** The downstream gates (T2 at 0.5, T3 at 0.2, F1-F4 at chain baselines) kill enough paths that V=$12 billion is insufficient. The program is structurally unviable at the pitch's low headline regardless of FSP-2 outcome.

### H2 — Breakeven T1 at V=$200 billion in [0.02, 0.05]

**Verdict: PARTIALLY-CONFIRMED.**

Measured breakeven T1 at V=$200 billion: **0.018**. Just below the predicted lower bound of 0.02. Within the falsification band [0.005, 0.10]. The prediction was slightly miscalibrated on the optimistic side; the actual breakeven is even more favorable than predicted.

### H3 — Next binding gate is T2; T2 lift to 1.0 with T1=0.5 produces positive EV at V=$24B in [+$30M, +$80M]

**Verdict: PARTIALLY-CONFIRMED with substantive surprise.**

Post-T1-lift (T1=0.5) gate kill probabilities at V=$24 billion:

| Gate | p_kill at T1=0.5 | Position in chain |
|---|---:|---|
| T1_fsp2_award | 0.500 | 1st (still dominant) |
| **T2_hybrid_aerocap** | **0.188** | **3rd (next binding gate by kill prob)** |
| F1_gate_a_leo_debris | 0.125 | 2nd |
| T3_bring_rendezvous | 0.120 | 5th |
| F2_gate_b_cislunar | 0.038 | 4th |
| F3_gate_c_d_qual | 0.005 | 6th |
| F4_ship3_saturn_commit | 0.005 | 7th |

The hypothesis correctly identified T2 as the next binding gate by kill probability. But the predicted lift magnitude was **off by a factor of about 4x to 16x** depending on which gate is lifted. Measured EV at V=$24 billion under combined lifts (T1=0.5 baseline):

- T1=0.5 only: EV = $-50 million
- T1=0.5, T2=1.0 (all else baseline): EV = **$+317 million** (predicted: $+30 to $+80 million — 4x to 10x larger than predicted)
- T1=0.5, T3=1.0 (all else baseline): EV = **$+1,225 million** (T3 lift has more impact than T2 lift)
- T1=0.5, T2=1.0, T3=1.0 (all else baseline): EV = **$+2,608 million**

**Substantive methodology surprise: T3 lift has 4x more EV impact than T2 lift,** even though T2 has higher kill probability. The cause: T3 starts at 0.20 baseline (low rendezvous-survivability anchor) so the lift to 1.0 is a 5x probability gain. T2 starts at 0.50 so the lift to 1.0 is only 2x. The conditional probability of reaching T3 (after T1, F1, T2, F2 all pass) compounds: at T1=0.5 × F1=0.75 × T2=0.5 × F2=0.80 = 0.15 reach probability. Lifting T3 from 0.20 to 1.0 takes that 0.15 × 0.20 = 3 percent full-success probability to 0.15 × 1.0 = 15 percent — a 5x boost in success probability, while T2 lift would only take 0.5 × 0.5 = 0.25 to 0.5 × 1.0 = 0.5, a 2x boost.

**Methodology learning surfaced: distinguish "dominant kill gate" (highest p_kill) from "highest leverage gate" (largest EV per unit probability lift).** Round 7's identification of T1 as dominant by kill probability was right; round 8's identification of T3 as highest-leverage gate is also right; they're different things.

### H4 — Public-evidence-supported Bayes factor in [1.5, 3.0]; T1 posterior in [0.0002, 0.005]

**Verdict: CONFIRMED.**

Bayes-factor compounding from documented evidence (May 2026):

| Evidence | Direction | Bayes factor (low/point/high) |
|---|---|---:|
| Draft AFP issued Aug 29, 2025 | positive | 2.0 / 3.0 / 4.5 |
| Duffy directive scope to 100 kWe + FY30 deployment intent | positive | 1.2 / 1.5 / 2.0 |
| Final AFP schedule slip (anticipated early 2026, not yet) | negative | 0.6 / 0.75 / 0.85 |
| FY26 NEP/NTP budget zero | negative | 0.8 / 0.85 / 0.9 |
| DARPA DRACO cancelled May 2025 | negative | 0.8 / 0.85 / 0.9 |

**Compounded Bayes factor:** point 2.44, low 0.92, high 6.20. Point estimate within predicted [1.5, 3.0].

T1 posterior from conservative US-skeptical prior (0.0001): point 0.00024, high 0.00062.
T1 posterior from optimistic global+ever uniform prior (0.0037): point 0.00902, high 0.02293.

Even at the highest-end public-evidence Bayes factor on the optimistic prior, public-evidence-supported T1 is **0.023** — exceeds the V=$200 billion breakeven (0.018) but is still well below the V=$24 billion breakeven (0.25).

### H5 — Required private-information lift over public-evidence T1 in [100x, 300x]

**Verdict: PARTIALLY-CONFIRMED.**

Measured required lift at V=$24 billion = 0.250 / 0.02293 ≈ **10.9x**.

The prediction (100x-300x) was too pessimistic. The required lift is **one order of magnitude smaller**, but still meaningful. A 10-11x private-information lift to bridge from public-evidence T1 = 0.023 to breakeven T1 = 0.25 at V=$24 billion is plausible-but-non-trivial:

- A single strong private signal (e.g., FSP-2 contract negotiation at term-sheet stage) could conceivably justify a 3-5x lift.
- Combining with a named-contractor commitment could add another 2-3x.
- 10x compounding requires multiple-source corroboration but is within the bracket of "documentable private information."

### H6 — Public-evidence-supported T1 lift alone insufficient at pitch headline V=$24 billion

**Verdict: CONFIRMED.**

Public-evidence-high T1 (0.02293) is below the V=$24 billion breakeven (0.25). Gap remains 10.9x at headline V. At V=$200 billion (induced-demand upside), the gap closes on public evidence alone (T1 high 0.023 > breakeven 0.018). At intermediate V (V=$50-100 billion), the gap is 1-2x — small enough that a single weakly-positive private signal could plausibly close it.

---

## Headline

Under staged-options framing with all gates except T1 at chain anchors, the **breakeven T1 at the pitch's headline V=$24 billion is 0.250** — a 10.9x lift over the high-end public-evidence-supported T1 of 0.023. **The pitch's low headline V=$12 billion is structurally unviable** even at T1 = 1.0 because downstream gates (T2=0.5, T3=0.2) kill enough paths that $12 billion V is insufficient. **At V=$200 billion induced-demand upside, public-evidence-supported T1 alone closes the gap** (T1 high 0.023 > breakeven 0.018). The highest-leverage gate-lift target after T1 is T3 (B-ring rendezvous survivability), not T2 (hybrid aerocapture closure) — substantive surprise: T3 lift produces 4x more expected-value gain than T2 lift at equal probability change.

---

## Reading

**Matrix decision point #1 reading at headline V:** technology-demonstrator-only by capital class (rounds 1-7); sovereign-research-grant + private-options sleeve by expected-value framing (round 7). **At V=$24 billion, the project owner needs 10.9x private-information T1 lift over public-evidence-supported T1 (0.023 → 0.25) to make staged-options positive-EV.** That lift is plausible-but-non-trivial; achievable through compounding 2-3 documentable private signals.

**At V=$50-100 billion (mid-range of pitch's induced-demand bracket), the gap is much smaller** — 1-2x lift suffices. A single weakly-positive private signal on FSP-2 negotiation status would close it.

**At V=$200 billion (full induced-demand upside), public evidence alone closes the gap.** No private information required if the project owner can defend the $200 billion V framing.

**Project-owner pitch revision implications:**

1. **The pitch's low headline V=$12 billion is structurally unviable under staged-options framing.** Either drop it as the floor and lead with V=$24-50 billion as the floor, or accept that the floor case is sovereign-research-grant-only (zero positive option value).

2. **The pitch's high headline V=$24 billion is viable at 10.9x private-information T1 lift over public evidence.** This is the operating-band assumption: project-owner sources 2-3 corroborating private signals on FSP-2 status, documents them transparently, and presents a positive-EV pitch with explicit T1-probability disclosure. **The pitch becomes economically defensible without overclaiming on probability.**

3. **The pitch's induced-demand V=$50-200 billion bracket is increasingly self-sufficient.** At V=$100 billion, public evidence is approximately at breakeven (T1 high 0.023, breakeven 0.037 — 1.6x gap). At V=$200 billion, public evidence alone clears. This is the "narrative-defensible upside path" — if the project owner can credibly defend the induced-demand framing, staged-options EV is positive on public evidence alone.

4. **Gate T3 (B-ring rendezvous survivability) is the highest-leverage technology-gate after T1.** A successful round on R-bring-rendezvous-survivability that lifts T3 from 0.20 to 0.5+ would push staged EV at headline V=$24 billion materially positive even at modest T1 lifts. **This is a high-yield round for orchestrator scheduling.**

5. **L0-13 capital structure: the staged-options framing is research-grant tranche 1 + private-options-sleeve tranches 2-3.** This stands regardless of T1 outcome.

---

## Cross-learning

- **Round 7 T1-dominance insight quantified.** Round 7 surfaced that T1 dominates the decision tree under conservative anchors. Round 8 quantifies: under public-evidence-supported T1, the gap to breakeven at headline V is one order of magnitude, not three. The pitch's positive-EV claim is achievable but requires private-information lift.
- **The user-locked R-power-wonder findings are load-bearing on the Bayes-factor compounding.** Without findings 2 and 3 (specifically: draft AFP issuance, Duffy directive, schedule slip, FY26 budget, DRACO cancellation), the public-evidence T1 estimate would be much closer to the chain's conservative anchor 0.0001. The May 2026 evidence shifts T1 by 2.4x point estimate, 6.2x high estimate.
- **Methodology learning surfaced.** Distinguish "dominant kill gate" (highest p_kill) from "highest leverage gate" (largest EV per unit probability lift). They are different. T3 has both lower kill probability and higher leverage; T2 has both higher kill probability and lower leverage. Lift-leverage scales as (1 - p_baseline) × reach_probability; kill probability scales as (1 - p_gate) × reach_probability. The two are not the same function. **Methodology lesson 15 candidate.**
- **Round 6 reading further refined.** Round 6 showed pitch's positive-EV claim requires p_technology_gates ≈ 1.0 unconditionally. Round 8 shows: the "1.0" can be reduced via gate-by-gate sensitivity. At V=$24 billion, breakeven requires (T1 ≥ 0.25 OR a combination of partial-T1 with T2/T3 lifts). The pitch's headline is not unconditionally requiring p=1.0; it requires a specific combination of gate lifts that the project owner could plausibly stake out.
- **R-bring-rendezvous-survivability round is highest-leverage open round.** Round 8 surfaced this. If that round closes with a defensible T3 prior at 0.5+, the staged-options EV picture at headline V=$24 billion shifts materially. The round was already in the open-SCOPE list (active-sessions); promoting its priority is the pitch-yield action.

---

## Next-round candidates

1. **Pitch revision recommendation document** (project-owner deliverable, not a research round). With rounds 6, 7, 8 in hand, write specific recommended revisions to ICEBERG-pitch.md lines 263-285 and 311-318. Specifically: drop V=$12 billion as floor; explicit T1-probability disclosure with public-evidence-supported point estimate (0.009) and high estimate (0.023); explicit gate-leverage table identifying T3 as highest-leverage; staged-options budget with tranche structure.
2. **Promote R-bring-rendezvous-survivability execution** to high priority. T3 is the highest-leverage gate after T1. A defensible T3 lift from 0.20 to 0.5+ shifts headline V staged EV positive at modest T1.
3. **R-public-evidence-rigorous-bayes-factor** — sharpen the Bayes-factor estimates in this round with more rigorous decomposition. Each evidence piece could be its own posterior calculation; the rough 1.5-3.0 bracket may be tightenable.
4. **R-correlated-gate-outcomes** — round 7 assumed independence; round 8 surfaced that T3 leverage is high. If gate outcomes are positively correlated (a successful reactor program signals capability across the chain), the optimistic-side EV is understated.
5. **R-V-defensibility-bracket** — what V framing is defensible to a sophisticated capital allocator? At V=$200 billion, the pitch's induced-demand upside, public evidence alone closes the gap. But is V=$200 billion defensible? That is an economics question, not a probability question — its own round.

---

## Methodology notes (lessons applied)

- **Lesson 7 (pessimistic-anchor-first).** T1 conservative anchor at 0.0001 used as the prior for Bayes-factor compounding.
- **Lesson 9 (anchor SCOPE on prior aggregate verdict).** Round 8 anchored on round 7's H6 reading and on the user-locked R-power-wonder findings as documented public evidence.
- **Lesson 14 extension (distinguish single-axis from joint-axis sensitivity).** Round 8 single-axis on T1; rounds 6, 7 multi-framework; rounds 1-5 single-axis on conditional priors and engineering priors.
- **Lesson 15 candidate (from this round).** Distinguish dominant-kill-gate from highest-leverage-gate. They are different functions of the gate-pass-probability vector and can yield different priority orderings for follow-on rounds. Round 8's substantive surprise on H3 was driven by conflating these two concepts in the prediction.

---

## Files

- `SCOPE.md` — pre-registration
- `run.py` — T1 sweep across [0.0001, 0.5] × V across [$12, $200 billion]; breakeven binary search; post-T1-lift gate-kill-probability ranking; T2/T3 lift sensitivity; public-evidence Bayes-factor compounding
- `results/T1_sensitivity_and_breakeven.json` — full output with sweep table, breakeven table, public-evidence T1 posterior, hypothesis verdicts
