# R-staged-options-with-technology-gates — does the kill-at-each-gate option value rescue any non-pathological corner?

**Status:** scope, pre-study. Authored by iapetus, 2026-05-16. Seventh round of the iapetus reactor-program-targets campaign. Direct follow-on to R-pitch-ev-reconciliation: that round's option (2) called for explicit staged-options framing; this round runs the math.

---

## The unchallenged assumption

R-pitch-ev-reconciliation (round 6) showed that the pitch's positive expected value of $5.5-11.5 billion is a **terminal-bet expected value**: spend $1 billion up-front, p=0.50 of success, payoff $12-24 billion. Under that framing, composed expected value with the technology-gates conjunction is negative across all 432 non-pathological corners.

But the pitch's actual program structure (lines 263-318) and the user-locked anchor-investment-thesis framing (belief 76fd04cdba8b2c3b: "gated by demonstrator flights every ~2 years, with explicit kill criteria at each gate") are explicitly **staged options**: the $1 billion is the maximum committed loss only if every gate passes up to first-Saturn-ship failure. If any gate fails, the program kills with cumulative-to-kill spend, not full $1 billion.

Round 6's hypothesis H6 confirmed the chain's "technology-demonstrator-only" reading under terminal-bet EV. This round tests whether the kill-at-each-gate option value materially shifts that reading. The option value is real: under correlated-prior anchors, killing at an early gate avoids the downstream spend. The question is whether the option value is large enough to flip the matrix decision point #1 reading.

**Specifically, this round questions:** the assumption baked into rounds 1-6 that the program's economic class is determined by the terminal joint conjunction posterior. If gates retire risk asymmetrically (early gates retire technology-gate risk; late gates retire flight-gate risk), the staged-options expected value can dominate the terminal-bet expected value by 5-50x. If that dominance is enough to flip from negative composed EV to positive, the reading shifts. If not, the reading is reinforced again.

---

## Question this round answers

For the held chunk-rendezvous architecture under conservative anchors (chain rounds 1-5 results), and using the pitch's gate structure (gates A-D plus technology-development gates that the pitch silently assumes):

1. **What is the staged-options expected value (decision-tree expected value with kill-at-each-gate) compared to the terminal-bet expected value computed in round 6?**
2. **What is the expected total spend under staged-options? Specifically, how does it compare to the pitch's $1 billion max-credible-loss number?**
3. **Does staged-options expected value go positive at any non-pathological anchor combination?**
4. **What is the option-value gain (staged minus terminal) as a multiple? Does it exceed 5x? 10x?**
5. **Reading-level: under staged-options, is matrix decision point #1 still "technology-demonstrator-only" by capital class, or does it shift to a defensible higher class (research-grant + private-options sleeve, sovereign-bond-with-gates)?**

---

## Decision-tree structure (pre-registered)

The program is modeled as a sequence of gates. At each gate, the program either passes (advances to the next gate with cumulative spend updated) or fails (kills with cumulative-spend-at-kill written off as loss). Pre-registered gate structure:

| Gate | Year | Cost-of-gate ($M) | Cumulative ($M) | What it gates | Probability anchored on |
|---|---|---|---|---|---|
| T1 — FSP-2 award | 1.5 | 80 | 80 | Reactor-program-availability Level-0 | chain's p_500kWe_orbit_by_window × narrow conditioning on "awarded by year 2" — fraction of full-window posterior |
| F1 — Gate A LEO debris demo | 1.5 (parallel) | 80 | 160 | Bag deployment + capture mechanism | pitch line 313 (0.75 historical first-flight rate at LEO scale) |
| T2 — Hybrid aerocapture closure | 3 | 100 | 260 | R-hybrid-aerocapture-aerobraking | P_HYBRID_AEROCAP = 0.5 (R1 baseline subjective prior) |
| F2 — Gate B cislunar demo | 3 | 180 | 440 | Bag against real ice + chunk-fed water-MET | pitch line 314 (cislunar demo, 0.80 historical) |
| T3 — B-ring rendezvous survivability | 5 | 100 | 540 | R-bring-rendezvous-survivability | P_RENDEZVOUS = 0.20-0.30 (R1 baseline; lo and hi anchors) |
| F3 — Gate C vacuum qual + Gate D long-soak | 5 | 150 | 690 | Bag MTBF + non-bag-subsystems reliability | 0.90 (ground qual is high-confidence; long-soak is lower) — composite 0.80 |
| F4 — Ship 3 commercial flight + Saturn capture | 12 | 460 | 1150 | First Saturn ship integration test | pitch line 265 (0.50 worst-case before any gate credit; 0.70 after gates A-C) |

(Ship 4 onward at $260M each is steady-state revenue-producing and not part of the kill-tree; total program max-committed at first-Saturn-arrival is $1.15 billion, matching the pitch's ~$1 billion max-credible-loss claim with small rounding.)

**Gates T1-T3 are technology-development gates** (the ones round 6 surfaced as silently-assumed). **Gates F1-F4 are flight gates** (the ones the pitch explicitly enumerates). The program kills if any gate fails. The decision-tree expected value is:

```
E[NPV] = SUM_paths [P(path) × NPV(path)]
where path is a complete sequence (T1 outcome, F1 outcome, T2 outcome, ..., F4 outcome)
NPV(path_full_success) = V minus C_total
NPV(path_kill_at_gate_k) = minus C_cumulative_to_k
```

The terminal-bet expected value used in round 6 is the special case where all gates collapse into a single "did the whole program work?" probability — losing the option value entirely.

---

## Pre-registered hypotheses (numeric ranges + falsification bands)

| # | Hypothesis | Predicted range | Falsification band |
|---|---|---|---|
| H1 | Staged-options expected value strictly dominates terminal-bet expected value at every anchor combination. The dominance multiple (E[NPV]_staged / E[NPV]_terminal) is greater than 1 for all anchors and ranges 2x-50x depending on gate-pass-probability profile. | predicted: dominance multiple ≥ 2x at every anchor; median ≈ 10x | H1 falsified if any anchor produces E[NPV]_staged ≤ E[NPV]_terminal, OR if median dominance multiple is below 2x |
| H2 | Expected total spend under staged-options at conservative anchors is bounded well below the pitch's $1 billion max-credible-loss. Under conservative-US-skeptical anchors, E[total spend] is in the range $100-300 million because gate T1 (FSP-2 award) kills the program early in most scenarios. | predicted: E[total spend] $100-300 million at conservative; $300-700 million at optimistic | H2 falsified if E[total spend] exceeds $700 million at conservative anchors OR falls below $50 million |
| H3 | At conservative-anchor staged-options, expected value is still NEGATIVE, but in the range -$50 to -$200 million rather than round 6's near-$1 billion. The reduction is the option-value gain. | predicted: E[NPV]_staged is negative but more than 5x smaller in magnitude than terminal-bet EV | H3 falsified if E[NPV]_staged is positive at conservative anchors OR more negative than -$500 million |
| H4 | At optimistic-anchor staged-options (global+ever uniform, all conditional priors at 1.0, baseline engineering), expected value crosses zero. The minimum gate-pass-probability profile that produces positive staged-options EV defines a bracket of "anchors at which staged-options is rational." | predicted: positive EV achievable at optimistic anchors with V=$24 billion; required threshold roughly 0.05-0.10 on the joint technology-gate-survival probability | H4 falsified if no non-pathological anchor produces positive staged-options EV |
| H5 | The pitch's $1 billion max-credible-loss number is approximately correct under staged-options as a max-credible-loss (worst-case-cumulative), but materially overstates the EXPECTED loss. Under conservative anchors, expected loss is ~$100-300 million; pitch's $1 billion is a maximum (path through every gate to phase-3 failure), not an expectation. | predicted: max-loss-path is approximately $1.15 billion; E[loss] is $100-300 million conservative, $300-700 million optimistic — a 4-10x ratio of max-to-expected | H5 falsified if max-loss equals expected-loss (single-path program with no option value) OR if max-loss is materially different from $1 billion |
| H6 | Reading-level (load-bearing): under staged-options framing, matrix decision point #1 SHIFTS from "technology-demonstrator-only" to "research-grant + private-options sleeve" — defensible at a sovereign-research-grant capital class because: (a) max committed loss is $1 billion (matches sovereign technology demonstrator budgets), (b) expected loss under conservative anchors is $100-300 million (matches NASA Small Business Innovation Research / SpaceWERX scale), (c) at any non-pathological anchor, the expected value is materially less negative than terminal-bet EV. The reading is no longer "do not pursue;" it becomes "pursue staged with explicit kill budget." | predicted: H6 shifts reading from "tech-demonstrator-only" to "research-grant + private-options sleeve, structured with kill budget" — a project-owner-relevant defensible upgrade | H6 falsified if staged-options EV remains so negative at conservative anchors that no defensible reading shifts (i.e., E[NPV] < -$500 million under all anchors), OR if H4 falsifies (no anchor produces positive staged-options EV anywhere) |

---

## Method sketch

1. **Encode the decision tree** as a Python function that walks each path from gate T1 through gate F4, computing path probability and path NPV.

2. **Anchor probabilities** on chain rounds 1-5 outputs:
   - p(T1: FSP-2 awarded by year 2) — anchored on chain's p_500kWe_orbit_by_window with year-2 narrow conditioning; sweep across the chain's anchor priors (skeptical/Jeffreys/uniform US; global+ever uniform).
   - p(T2: hybrid aerocapture closes) — chain's P_HYBRID_AEROCAP = 0.5 baseline.
   - p(T3: B-ring rendezvous closes) — chain's P_RENDEZVOUS_LO and P_RENDEZVOUS_HI = 0.20-0.30.
   - p(F1: Gate A LEO demo) — pitch's 0.75 for LEO debris first-flight rate.
   - p(F2: Gate B cislunar demo) — pitch's 0.80 for cislunar second-flight rate.
   - p(F3: Gate C vacuum qual + Gate D long-soak) — pitch's 0.80 composite.
   - p(F4: ship 3 commercial flight) — pitch's 0.50 worst-case before any credit, 0.70 after gates A-C close.

3. **For each anchor combination,** compute:
   - E[NPV]_staged = sum over all 2^7 = 128 paths
   - E[total spend]
   - Max-loss (worst path)
   - Compare to E[NPV]_terminal (round 6 output)

4. **Sweep V across {12, 18, 24, 50, 100, 200} billion** and L is implicit (cumulative-to-kill per path).

5. **Identify threshold anchors** that produce positive E[NPV]_staged.

6. **Reading-level synthesis:** what does the project owner need? Either (a) confirm staged-options framing defensible at sovereign-research-grant class, or (b) confirm the staged-options EV is still negative and the chain's H6 holds.

---

## Reading template (5-section, worker fills after run)

- **Hypotheses adjudicated.** Verdict per H1-H6, predicted vs measured.
- **Headline.** One-line: does staged-options EV rescue any non-pathological anchor? And what is the option-value gain?
- **Reading.** Matrix decision point #1 under staged-options framing — defensible economic class with kill budget.
- **Cross-learning.** Connection to round 6 (terminal-bet baseline), the pitch's gate structure, and the user-locked anchor-investment-thesis framing.
- **Next-round candidates.** If H6 confirmed: pitch revision recommendations + L0-13 amendment. If H6 falsified: closer look at private-information bracket or induced-demand sensitivity.

---

## Worker notes

- **Round priority:** **high.** Directly underwrites the project-owner-level pitch revision question surfaced by round 6 option (2).
- **Method:** decision-tree expected value with 128 paths (7 gates × binary outcomes). No new physics or new posteriors — anchor on chain rounds 1-5 outputs.
- **Out of scope:** options-on-options (e.g., delay-the-decision value), correlated-gate-outcomes (assume gates are independent given the conditioning), multi-ship cadence after first Saturn arrival.
- **Methodology lessons applied:** lesson 7 (pessimistic-anchor-first), lesson 9 (anchor SCOPE on prior aggregate verdict — round 6 H6), lesson 14 extended (distinguish single-framework readings from multi-framework; here from terminal-bet to staged-options).
