# R-staged-commitment-underwriter-anchor — SCOPE

**Author:** rhea (worker session, iceberg-rhea-2 branch).
**Date:** 2026-05-15 (latest+8, sixth round this sitting; queued from R-staged-commitment-gates-frame-B-interaction priority-1 thread #1).

## Goal

Resolve round 13's pending question: **which Frame B metric does a sovereign underwriter actually anchor on, and what does that imply for the staged-vs-upfront comparison?**

Round 13 established that under demand-curve clearing-price distribution, staged commitment:
- HURTS binary P(NPV>0) by 1-8 percentage points at every cell tested.
- IMPROVES median Δ-NPV by +$3.3 billion at 2-launch sovereign-bond LR=15.

Round 13's pending thread #1 ("R-staged-commitment-EV-vs-binary-reconciliation") framed this as a binary-vs-EV dichotomy and asked which metric sovereign-bond underwriting "actually anchors on." This round dissolves that framing: **neither binary P(NPV>0) nor median EV is the metric a real-world sovereign-debt underwriter computes.** Project-finance debt anchors on expected loss and coverage ratios. Equity anchors on EV with option-value. Sovereign grants anchor on technical milestone achievement, not NPV.

The right question is: under each plausible ICEBERG capital source (development-bank-style limited-recourse debt, sovereign-grant appropriation, equity-with-gate), how does the metric ACTUALLY used by that source move under staged vs upfront? The round-13 binary-P(NPV>0) finding is then either confirmed by some metric, or shown to be an artifact of the wrong proxy.

## What this round does

1. Inherits round 13's MC harness (10,000 demand-curve clearing-price draws; same seed 20260515; 2-launch W3 LR=15 load-bearing cell; chunk 200 t; delivered 80 t per mission; cadence 2/yr; horizon 40 yr; P_demonstrator = 0.90 on staged) without re-running upstream physics.
2. Adds the following capital-source-specific metrics computed per MC draw under both regimes:
   - **Equity (anchor-investor style):** mean NPV (EV); median NPV; P(NPV > 0); P(IRR > hurdle for hurdle ∈ {0%, 3%, 8.7%, 12% VC}); option-adjusted NPV (treat gate-0 outcome as binomial; if demonstrator fails, equity loses gate-0 capex but not fleet capex).
   - **Project-finance debt (sovereign-bond / dev-bank style):** expected loss = P(default) × LGD per draw. Default model: simple — debt is amortized from first-mission revenue at year 14.5; debt service is 6% coupon on outstanding plus 5%-of-original principal annually starting year 14.5; default if year-by-year revenue insufficient to cover debt service. Compute P(default) per draw; total EL = E[P(default) × debt outstanding × (1 - 0.40 LGD recovery)]. Compute also debt-service coverage ratio (DSCR) p5 across draws — the standard project-finance covenant anchor.
   - **Sovereign grant (NASA/DOE style):** binary P(technical milestone success at gate) = P_demonstrator = 0.90. Note: independent of accounting regime. Used to anchor the comparison's null reference.
3. Reports the FULL table of metrics per regime, identifies which regime each metric prefers, and identifies any non-monotonicities (metric prefers one regime under some condition and the other regime elsewhere).
4. Maps each metric to the realistic ICEBERG capital source(s) that uses it, anchored on (a) anchor-investor locked belief `76fd04cdba8b2c3b`, (b) the FSP Phase 2 sovereign-grant context (locked belief `edcfe90912ca80e5`), and (c) standard project-finance practice (cited).
5. Produces the matrix-axis-17 amendment recommendation: which metric should the matrix's Frame B anchor on, given who's actually writing the check.

## What this round does NOT do

- Does NOT re-derive trajectory, propulsion, conjunction, reactor-mass, or specific-power inputs. All physics inherited from rounds 9-13 anchored on the locked-belief priors (radiator-mass MARVL anchor, KRUSTY 2.4 W/kg flown anchor, FSP Phase 2 not awarded as-of-2026-05, 0-of-6 base rate).
- Does NOT introduce salvage value on demonstrator failure (R-demonstrator-failure-recovery-value, queued from round 13 Priority-2 thread #3).
- Does NOT model syndicated tranche financing (round 13 Priority-2 thread #6). Single capital-source-at-a-time framing.
- Does NOT vary P_demonstrator outside 0.90 (round 13 Priority-1 thread #2 is a separate round).
- Does NOT model concession-style sovereign financing (where the sovereign keeps upside in exchange for capex guarantees). Limited to standard limited-recourse project-finance debt + standard appropriated grant + standard equity.
- Does NOT re-derive the anchor-investor pitch posture itself — that is locked in belief `76fd04cdba8b2c3b` and this round inherits it as the equity-side framing.
- Does NOT pretend to have empirical interviews with development-bank underwriters. The capital-source-to-metric mapping is anchored on cited project-finance practice (Yescombe, *Principles of Project Finance*; World Bank Group operational policy on limited-recourse lending; NASA acquisition policy on appropriated milestone-grant funding). Where cited literature isn't available the round explicitly notes the source's absence and treats the mapping as structural-inference rather than empirical.

## Why now

Round 13 falsified the working assumption that staged commitment improves Frame B binary P(NPV>0). The matrix's axis-17 currently cites "29% Frame B at sovereign-bond" (round 11 anchor); round 13 corrected that to "36.3% at upfront W3 LR15" while showing staged drops it to 31.0%. Whether the matrix amendment should adopt 36.3% upfront, 31.0% staged, or replace binary P(NPV>0) entirely depends on round 14's answer.

The anchor-investor locked framing (belief `76fd04cdba8b2c3b`) describes ICEBERG as equity-with-gates — implying the equity-side metric (EV with option-value) is the one the anchor investor actually anchors on, not binary P(NPV>0). The pitch posture should reflect that. The matrix-as-currently-written reflects the wrong proxy.

## Methodology lessons inherited (from rounds 9-13)

- **#11:** Grade SCOPE against primary input data before drafting hypotheses. *Applied below in §"Primary input grading."*
- **#13:** Double-check arithmetic in pre-registration BOE. *Applied below: every BOE bracket computed symbolically then numerically.*
- **#14 (round 13, new):** Distribution-aware BOE. For any hypothesis that brackets a value integrated over a distribution, compute BOE at p25/p50/p75 not just median.
- **#15 (round 13, new):** Sign-of-Δ at WACC=0 is revenue-dependent. *Apply to every Δ-metric prediction.*
- **#7-v5 (proposed):** Convex-hull check on distribution-aware BOE.

## Primary input grading (per lesson #11)

| Input | Source | Status | Notes |
|---|---|---|---|
| Round 13 results JSON | `R_staged_commitment_gates_frame_B/results/staged_gates_frame_B_summary.json` | exists | re-use the per-draw NPV arrays under both regimes if available; otherwise re-derive from harness |
| Round 13 run.py | `R_staged_commitment_gates_frame_B/run.py` | exists | inherit; extend with the new metrics |
| Demand-curve MC | `R_LEO_water_demand_curve/run.py` | exists | already imported by round 13 |
| Heterogeneous-cadence helpers | `R_heterogeneous_cadence/run.py` | exists | already imported by round 13 |
| anchor-investor framing | locked belief `76fd04cdba8b2c3b` | locked | cite verbatim in equity-side metric mapping |
| Reactor program priors | locked beliefs `0418e2c9ee3de422`, `edcfe90912ca80e5`, `776575c01d55ca51`, `0d5c882c13395571` | locked | inherited as conjunction multiplier upstream; NOT re-derived here |
| Yescombe / project-finance practice | external citation | needed | will cite per coverage-ratio framing in STUDY §"Capital-source-to-metric mapping" |
| World Bank IBRD lending policy | external citation | needed | cite for limited-recourse debt amortization structure |
| NASA appropriated-grant practice | external citation | needed | cite for sovereign-grant milestone-gate structure |
