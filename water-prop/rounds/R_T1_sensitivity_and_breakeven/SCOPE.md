# R-T1-sensitivity-and-breakeven — at what T1 (FSP-2 award) probability does the staged-options EV cross zero, and what's the next bottleneck?

**Status:** scope, pre-study. Authored by iapetus, 2026-05-16. Eighth round of the iapetus reactor-program-targets campaign. Direct follow-on to round 7: T1 is the dominant gate; quantify the breakeven and identify what becomes binding after a T1 lift.

---

## The unchallenged assumption

Round 7 surfaced a striking result: under conservative anchors, E[total spend] for the staged-options program is approximately $80 million — essentially just the T1 gate cost — because the program kills at T1 with greater than 99.99 percent probability under the conservative US skeptical anchor. **T1 dominates the entire decision tree.** Downstream gates barely affect E[spend] because conditional probability of advancing past T1 is so small.

This dominance has a corollary: **a T1 lift, even a modest one, can materially shift the staged-options EV picture without requiring lifts on any other gate.** Conversely, if T1 is anchored too conservatively, the whole staged-options framing is uninformative (it just says "we will probably spend $80M and then quit").

What's the right T1 anchor? Round 7 used 0.5 × P(US fission orbit by 2035) as the year-2 narrow conditioning. That gives 0.011 percent for the skeptical prior. But the user-locked R-power-wonder findings (May 2026) document **public evidence** that should update T1 upward from the 0-of-6-base-rate anchor:

- **POSITIVE evidence:** FSP draft Announcement for Partnership Proposals issued August 29, 2025. Historically, draft AFPs precede contracts within 1-2 years. Bayes factor on T1: meaningful positive.
- **POSITIVE evidence:** Duffy directive August 4, 2025 raised FSP scope to 100 kilowatt-electric with stated Q1 FY2030 deployment intent. Scope expansion at the policy level is positive signal.
- **NEGATIVE evidence:** Final AFP anticipated "early 2026" — as of May 2026, no final AFP issued. Schedule slip of 4-6 months. Bayes factor: slight drag.
- **NEGATIVE evidence:** FY2026 budget request zeroed NASA nuclear-electric-propulsion and nuclear-thermal-propulsion technology lines. Bayes factor: policy headwind, but FSP (fission surface power) is a separate budget line not directly affected.
- **NEGATIVE evidence:** DARPA DRACO cancelled May 30, 2025. Sector headwind for space fission generally.

The mixed evidence does NOT zero-out the chain's prior; it modestly updates it. The question is: **at what T1 probability does staged-options EV cross zero, and is that lift achievable on documentable public evidence alone, or does it require private information lift?**

This round answers that question, quantitatively, and identifies what gate becomes binding after T1 is lifted.

---

## Question this round answers

For the held chunk-rendezvous architecture under round 7's staged-options framing, holding all gates other than T1 at chain anchors:

1. **What is the breakeven T1 probability** at which staged-options EV crosses zero, evaluated at V = $12 billion, $18 billion, $24 billion (pitch headline), and $50-200 billion (induced-demand)?
2. **After a hypothetical T1 lift,** what gate becomes the next binding bottleneck (i.e., the dominant kill gate)?
3. **What is the magnitude of the T1 lift** required, expressed as a multiple over the chain's conservative US-skeptical anchor (T1 = 0.0001) and over the chain's optimistic global+ever uniform anchor (T1 = 0.0037)?
4. **How does the breakeven T1 compare to public-evidence-supported T1 estimates** (the Bayes-factor compounding from draft AFP issuance, Duffy directive, FSP-2 schedule status as of May 2026)?
5. **Reading-level:** is the breakeven T1 achievable on public evidence alone, or does it require private information?

---

## Pre-registered hypotheses (numeric ranges + falsification bands)

| # | Hypothesis | Predicted range | Falsification band |
|---|---|---|---|
| H1 | Breakeven T1 at pitch headline V = $24 billion, with all other gates at chain anchors, is in the range 0.15-0.30 — well above any plausible public-evidence Bayes-factor-compounded estimate (which is in the 0.001-0.02 range). | predicted: breakeven T1 in [0.15, 0.30] at V=$24B; achievable on documentable public evidence only at the lower bound or below | H1 falsified if breakeven T1 is below 0.05 OR above 0.50 |
| H2 | At V = $200 billion (induced-demand upside), breakeven T1 drops to the range 0.02-0.05 — within the high end of public-evidence-supported estimates. | predicted: breakeven T1 at V=$200B in [0.02, 0.05] | H2 falsified if breakeven T1 at V=$200B is below 0.005 OR above 0.10 |
| H3 | After T1 lift, the next binding gate is T2 (hybrid aerocapture closure at 0.5 baseline). Holding T1 at 0.5 (coin-flip) and T2 at 0.5, the staged-options EV at V=$24 billion is approximately -$5 to -$30 million — close to but not yet positive. Lifting T2 to 1.0 with T1 at 0.5 pushes EV to positive in the range +$30 to +$80 million. | predicted: T2 is the next binding gate after T1 lift; T2 lift to 1.0 with T1 at 0.5 produces positive EV at V=$24B | H3 falsified if T3 or F4 emerges as the next binding gate instead of T2, OR if T2 lift to 1.0 with T1=0.5 does not produce positive EV at V=$24B |
| H4 | Public-evidence-supported T1 lift compounding (draft AFP × Duffy directive × schedule slip × FY26 budget × DRACO cancellation) produces a Bayes factor in the range 1.5-3.0 over the chain's conservative US-skeptical prior. Resulting T1 estimate is in the range 0.0002-0.005. This is materially below the breakeven T1 even at induced-demand V. | predicted: public-evidence-supported T1 in [0.0002, 0.005] | H4 falsified if a defensible public-evidence Bayes-factor compounding produces T1 above 0.02 |
| H5 | Required private-information lift to recover positive staged EV at V=$24 billion is in the 100x-300x range over the public-evidence-supported T1 (i.e., 0.0002-0.005 → 0.05-1.5). That is materially larger than would be supported by any single private-information channel (FSP-2 negotiation signal, named-contractor commitment, etc.). Multiple compounding private signals would be needed. | predicted: required private-information T1 multiple in [100x, 300x] over public T1; multiple-signal compounding required | H5 falsified if required multiple is below 50x OR if single-channel private information can plausibly provide a 100x+ lift |
| H6 | Reading-level (load-bearing): the public-evidence-supported T1 lift does NOT close the gap to positive staged EV at headline V. **Project-owner pitch revision cannot rest on T1 lift alone.** Three options: (a) commit to induced-demand V framing in the pitch (and accept the lower-probability event class); (b) source private-information T1 lift in the 100x-300x range and document it transparently; (c) accept that the program economically lands in the sovereign-research-grant class with positive option value only conditional on T1 closure, not unconditionally. | predicted: H6 confirmed — T1 lift alone insufficient; project-owner must combine T1 lift with V uplift or other-gate lift to cross zero at headline V | H6 falsified if a defensible public-evidence-only T1 lift produces positive staged EV at V=$24 billion |

---

## Method sketch

1. **Replicate round 7's staged-options decision tree** with all gates at chain anchors except T1.

2. **Sweep T1** across:
   - 0.0001 (chain US skeptical conservative; round 7 baseline)
   - 0.001 (1 order of magnitude lift)
   - 0.005 (modest public-evidence credit — Bayes factor approximately 50x)
   - 0.01 (more aggressive public-evidence credit)
   - 0.05 (5 percent — high public-evidence credit OR single private signal)
   - 0.1 (10 percent — multiple private signals)
   - 0.2 (20 percent)
   - 0.3, 0.5 (very high credit; venture-class private information)

3. **For each T1 value, compute staged-options EV** across V = $12, $18, $24, $50, $100, $200 billion. Identify the breakeven T1 at each V.

4. **Identify the post-T1-lift dominant kill gate** by computing the per-gate kill probability table at T1 = 0.5 (coin flip). Identify which gate has the largest p_kill.

5. **Lift T2 (and separately T3) to 1.0** while holding T1 at 0.5 and other gates at chain anchors. Recompute EV. Confirm or falsify H3.

6. **Estimate the public-evidence-supported T1 using Bayes-factor compounding** of the documented evidence. Compute the compounded T1 estimate and compare to the breakeven.

7. **Reading-level synthesis:** does the gap close on public evidence? On private information? At what V does the gap become closeable?

---

## Reading template (5-section, worker fills after run)

- **Hypotheses adjudicated.** Verdict per H1-H6.
- **Headline.** One-line: at what T1 does staged-options EV go positive, and what's the next bottleneck?
- **Reading.** Project-owner action: which option from (a), (b), (c) of H6 is the right move, conditional on the data.
- **Cross-learning.** Connection to rounds 6, 7; to user-locked R-power-wonder findings; to the pitch's $1B max-loss claim.
- **Next-round candidates.** Whether to compute the T2-and-T3 lift sensitivities as their own rounds, or whether the campaign is now saturated and the right move is the handoff + project-owner pitch revision.

---

## Worker notes

- **Round priority:** **medium-high.** Closes the T1-dominance question raised by round 7. Tells project owner whether the next pitch revision should be (a) headline V framing, (b) private-information sourcing, or (c) accept the sovereign-research-grant ceiling.
- **Method:** sensitivity sweep on the round-7 decision tree. No new physics; varying one parameter at a time.
- **Out of scope:** detailed Bayes-factor estimation for each piece of public evidence (use rough 1.5-3.0 bracket and call it transparent; a more rigorous public-evidence Bayesian update could be its own follow-on round).
- **Methodology lessons applied:** lesson 7 (pessimistic anchor first — T1 conservative anchor at 0.0001), lesson 9 (anchor SCOPE on prior aggregate verdict — round 7 surfaced T1 dominance, this round quantifies it), lesson 14 extension (distinguish single-axis sensitivity from joint-axis sensitivity — here single-axis on T1).
