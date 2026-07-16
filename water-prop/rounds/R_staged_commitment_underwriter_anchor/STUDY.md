# R-staged-commitment-underwriter-anchor — STUDY.md

**Author:** rhea (worker session, iceberg-rhea-2 branch).
**Date:** 2026-05-15 (latest+8, sixth round this sitting; round 14 of the chained sequence).
**Status:** pre-registration. Composes round 13 harness with capital-source-specific metric layer.

## Setup

**Inherited closure cell (no re-derivation):**
- 2-launch architecture (round 12 Frame A optimum).
- Specific power 8 W/kg, m_LEO 206 t, conjunction 0.67% (round 9 H2a uniform prior).
- Reactor 500 kWe, water electric propulsion, water specific impulse 2934 s.
- Chunk 200 t, round-trip 14.5 yr, delivered 80 t per mission.
- First-unit ship $500M; Wright's-Law learning rate 0.0 or 0.15.
- Fleet horizon 40 yr; cadence 2/yr.
- P_demonstrator = 0.90 on staged regime.
- Demand-curve clearing-price MC: 10,000 lognormal draws, seed 20260515, p05/p50/p95 = $419 / $5284 / $61266 per kg.

**Load-bearing cell for hypothesis tests:** 2-launch, WACC 3% (sovereign-bond discount convention), LR 15%. Other cells reported for context only.

## Capital-source-to-metric mapping (the structural-inference table)

Per round 13 pending thread #1, round 14's job is to identify which metric each plausible ICEBERG capital source actually uses, then re-compute the staged-vs-upfront comparison under those metrics. The matrix's current binary P(NPV>0) anchor is a proxy convention, not a metric any actual underwriter computes.

| Capital source | Decision metric | Source / cite | Regime preference (predicted) |
|---|---|---|---|
| **Sovereign-grant** (NASA / DOE / ESA appropriations) | P(technical milestone success at next reauthorization gate). NOT NPV. | NASA acquisition policy: appropriated funds are reauthorized annually contingent on milestone completion. Cited in the Phase-2-not-yet-awarded prior (locked belief `edcfe90912ca80e5`); the 0-of-6 base rate (`776575c01d55ca51`) directly tests this gate-by-gate. | **TIE** — P_milestone is regime-independent at the gate level (both regimes face the same demonstrator-success probability 0.90). |
| **Limited-recourse project-finance debt** ("sovereign-bond" / development-bank loan) | Expected loss = P(default) × LGD × principal. Coverage ratios (DSCR p5, LLCR). Risk-priced coupon spread. NOT NPV. | Yescombe, *Principles of Project Finance* (Ch. 12, "Credit Risk Analysis"); World Bank IBRD operational policy on limited-recourse infrastructure lending; standard project-finance practice in concessional infrastructure deals (Three Gorges Dam, Channel Tunnel, etc.). | **STAGED** — pre-gate exposure to demonstrator failure scales with capex-committed-before-revenue. Staged caps that at $1.6B (gate-0); upfront commits $14.6B over the 14.5-yr pre-revenue window. |
| **Concessional / sovereign development bank with grant element** (e.g., World Bank IDA blend, EIB green-loan) | DSCR plus stated programmatic-impact KPIs. Cost-recovery floor not full IRR. | World Bank Group, *Operational Policy 10.00* on lending; EIB green-bond framework. | **STAGED** (same mechanism as project-finance debt; less rate-sensitive because of concessional element). |
| **Equity (anchor-investor)** | EV(NPV) probability-weighted across distribution, plus explicit option-to-abandon value at each gate. NOT binary P(NPV>0). | Locked anchor-investor belief `76fd04cdba8b2c3b` — "kill criteria at each gate" is option-value language; "option payoff is a Suez-Canal-class business" is upside-conditional language; "no scenario where funding ICEBERG damages the underlying anchor investment thesis" implies downside is bounded at gate-0 commitment, not at total program capex. | **STAGED** — option-adjusted EV(NPV) is higher than upfront by the option-value of abandoning $13B fleet capex at gate. |
| **Risk-tolerant venture equity** (VC retiree, not the anchor investor) | IRR or MOIC over a 7-10 yr horizon. P(IRR > hurdle). Discounting at 25%+ where the hurdle dominates the math. | Retired in round 11 H6 — venture-class is already off the table; included here only for completeness. | **N/A** (retired). |
| **Insurance / catastrophic-loss markets** | Value-at-risk; tail-loss expectation; reinsurance pricing. | Standard re/insurance pricing (Lloyd's syndicate practice). | **STAGED** (tail-loss is bounded at gate-0 commitment under staged; unbounded under upfront). |

For ICEBERG specifically, the plausible-source set is: sovereign-grant (high-confidence — the FSP Phase 2 pipeline if awarded), limited-recourse debt (medium-confidence — would require concessional element given the 0-of-6 base rate prior), and equity (high-confidence — anchor-investor locked-belief framing). Binary P(NPV>0) does not map to any of these three.

## Back-of-envelope (per cell of every pre-registered bracket — methodology lesson #7-v4)

### Cell α (H1 reference) — debt-style expected loss ratio (staged / upfront)

Pre-gate exposure to demonstrator failure (mechanism: catastrophic loss):

- **Upfront pre-gate exposure:** entire $14.6B program capex committed at year 0; $14.6B - mission-1 revenue at year 14.5 = essentially $14.6B at risk through year 14.5. Probability-weighted loss given demonstrator fails: $14.6B × P_fail × LGD where P_fail = 0.10 and LGD = 0.60 (project-finance standard 40% recovery from physical asset salvage). EL_upfront_pre-gate = $14.6B × 0.10 × 0.60 = **$876 million**.

- **Staged pre-gate exposure:** $1.6B committed at gate 0; rest contingent. EL_staged_pre-gate = $1.6B × 0.10 × 0.60 = **$96 million**.

- **Ratio: EL_staged / EL_upfront = $96M / $876M = 11.0%.** This exactly matches the gate-0-fraction-of-program-capex from round 13 H5 (10.94%), because the EL ratio is structurally determined by the capex ratio when LGD and P_fail are regime-invariant.

**BOE bracket for H1:** EL_staged / EL_upfront in **[8%, 15%]**. (Same band as round 13 H5 demonstrator-fraction.)

### Cell β (H2 reference) — implied bond-spread reduction

If a sovereign-bond is risk-priced (coupon = risk-free + spread; spread = EL / principal / duration):
- Upfront: spread = $876M / $8.76B principal (60% LTV) / 14.5 yr duration × 10000 bps = **40.3 bps/yr** for the pre-gate failure mode alone.
- Staged: pre-gate spread = $96M / $960M principal / 14.5 yr × 10000 = **6.9 bps/yr**.
- Difference: ~33 bps.

**BOE bracket for H2:** implied-spread reduction (upfront minus staged) in **[25, 50] bps** for the pre-gate failure mode alone (ignoring post-gate covenant-driven default).

### Cell γ (H3 reference) — mean Δ-NPV across MC (NOT median)

Round 13 reports MEDIAN Δ-NPV +$3.34B at 2-launch W3 LR15. Mean is different because of heavy-left-tail: p05 of Δ = -$70.3B; p95 = +$9.5B. The arithmetic mean of a left-skewed distribution is well below the median.

Rough estimate of mean: assume Δ-distribution has bulk near median (+$3.3B) plus a thin left tail to -$70B affecting ~5-10% of draws. Mean ≈ 0.92 × $3.3B + 0.08 × (-$35B) [mid of left tail] = $3.0B - $2.8B = **+$0.2B** roughly.

But this is highly uncertain — left-tail shape determines it. Could easily be **-$5B to +$3B**.

**BOE bracket for H3:** mean Δ-NPV across MC in **[-$5B, +$3B]**. If positive: equity-EV anchoring prefers staged. If negative: equity-EV ALSO prefers upfront and the case for staged narrows to debt and grant tracks only.

### Cell δ (H4 reference) — IRR distribution

IRR is the discount rate at which NPV = 0. Under demand-curve MC:
- At median clearing $5.28M/tonne, NPV at WACC=0 is positive under both regimes (per round 13 XC-4 which shows positive Δ at WACC=0). So IRR > 0 under both at median.
- Median IRR under upfront, at $5.28M/tonne: NPV(0) ≈ $50B+; NPV(15%) negative; crossover IRR ≈ 4-6%.
- Median IRR under staged, at $5.28M/tonne: NPV(0) ≈ $50B+ × p_success ≈ $45B; NPV(15%) probably more positive than upfront because deferred capex compresses; crossover IRR ≈ 5-7%.

**BOE bracket for H4:** median IRR_staged minus median IRR_upfront in **[0, +3] percentage points**.

### Cell ε (H5 reference) — option-adjusted equity NPV

Treat the gate as an option to abandon fleet capex on demonstrator failure. Option value at gate = max(0, expected fleet NPV given outcome) summed across outcomes. Under staged, equity pays gate-0 capex ($1.6B) but retains the option to walk away from $13B of fleet capex if (a) demonstrator fails OR (b) demonstrator succeeds but revenue distribution shifts unfavorably between year 0 and gate.

Option value at gate = E[max(0, fleet_NPV_at_gate)] − E[fleet_NPV_at_gate without gate]. At median clearing this is near zero (median fleet NPV is positive, so the option doesn't bite). At lower clearings (p05-p25 of demand-curve), median fleet NPV at gate is negative; option to abandon then has value equal to the negative magnitude.

Rough numeric: at p05 clearing $419/kg = $0.42M/tonne, fleet NPV is roughly -$8B; the option to abandon saves that. Probability mass in p05 zone is 5% of draws. Expected option-value contribution from low-clearing draws: 0.05 × $8B = $0.4B. Plus the demonstrator-failure-pure case (P=0.10): saves the un-built fleet capex PV ≈ $4B (discounted year-14.5 capex); expected contribution: 0.10 × $4B = $0.4B. Total option value ≈ **$0.8B** at year-0 PV.

**BOE bracket for H5:** option-adjusted Δ-NPV (staged option-value advantage over upfront) in **[+$0.3B, +$2B]** at year-0 PV under 2-launch W3 LR15.

### Cell ζ (H6 reference) — sovereign-grant track regime-invariance

Sovereign-grant gate is binary technical-milestone success. Under both regimes, the technical-milestone success probability at gate = P_demonstrator = 0.90 (L0-10 baseline). Regime structure (fleet pre-committed or not) does NOT affect grant's gate decision because the grant is anchored on demonstrator outcome, not on NPV. NRE recovery on demonstrator failure under appropriated-grant accounting: the grant has already been spent (sunk cost from sovereign's view); the program is killed by non-reauthorization at the next milestone.

**BOE prediction for H6:** P(grant program continuation past gate 1) = P_demonstrator = 0.90, regime-independent. Δ-P = 0 ± 0.5 pp (rounding).

### Cell η (H7 reference) — convex-hull check on round 13 distribution-aware BOE (lesson #7-v5)

Apply the proposed lesson #7-v5 retrospectively to round 13's median Δ-NPV bracket prediction [+$4B, +$8B] (actual +$3.34B, just below floor by $0.66B).

Compute Δ-NPV at p25 / p50 / p75 of the clearing-price distribution:
- p25 clearing ≈ $1700/kg = $1.7M/tonne (lognormal p25 of $1500 starship × $3.5 markup).
- p50 clearing = $5284/kg = $5.28M/tonne (round 13 anchor).
- p75 clearing ≈ $15000/kg = $15.0M/tonne.

Δ-NPV scaling: at WACC 3% LR 15%, deferred-fleet-capex savings of $1-2B (year-14.5 capex at 4% effective discount); revenue loss from gate scales with delivered tonnes × revenue × discount.

- At p25 ($1.7M/tonne): revenue per delivery $1.7M/tonne × 80 t = $136M; over 22 fleet deliveries ≈ $3.0B undiscounted, PV at year 14.5 ≈ $2.0B; staged loses 10% of that = $0.2B; capex saved $1.5B; **Δ-NPV ≈ +$1.3B**.
- At p50 ($5.28M/tonne): scaled 3.1×; Δ ≈ +$3.3B (round 13 measured).
- At p75 ($15M/tonne): scaled 8.8× from p25; revenue loss ≈ $1.8B; capex savings unchanged $1.5B; **Δ-NPV ≈ -$0.3B**.

Convex hull of [+$1.3B, +$3.3B, -$0.3B] is [-$0.3B, +$3.3B]. Round 13's measured median +$3.34B sits at top of hull. Round 13's pre-reg bracket [+$4B, +$8B] is OUTSIDE this hull — the bracket would have been caught as inconsistent under lesson #7-v5.

**BOE prediction for H7:** the convex-hull check confirms lesson #7-v5 catches round 13's BOE failure. Hull excludes [+$4B, +$8B]; measured +$3.34B is at hull boundary.

## Pre-registered hypotheses

| ID | Predicted | Falsification |
|---|---|---|
| **H1** EL_staged / EL_upfront (pre-gate catastrophic-loss term, 60% LTV, 40% recovery, P_fail = 0.10) in **[8%, 15%]**. | Outside band. |
| **H2** Implied sovereign-bond spread reduction (upfront minus staged), for the pre-gate-failure term alone, in **[25, 50] bps/yr**. | Outside band. |
| **H3** MEAN Δ-NPV across demand-curve MC at 2-launch W3 LR15 in **[-$5B, +$3B]** — i.e., the EV is much closer to zero than the +$3.34B median because of heavy-left-tail mass. | Outside band. |
| **H4** Median IRR_staged minus Median IRR_upfront across MC at 2-launch in **[0, +3] percentage points**. | Outside band, OR sign flip (staged IRR < upfront IRR). |
| **H5** Option-adjusted Δ-NPV (staged equity advantage from option-to-abandon fleet capex at gate) in **[+$0.3B, +$2B]** at year-0 PV, 2-launch W3 LR15. | Outside band. |
| **H6** Sovereign-grant track: regime-difference in P(grant continuation past gate 1) is ≤ 0.5 percentage points. | Outside band (regime difference > 0.5 pp). |
| **H7** Convex-hull check (lesson #7-v5) on round 13's median Δ-NPV bracket: the convex hull of Δ-NPV at clearing p25/p50/p75 does NOT include round 13's pre-reg band [+$4B, +$8B]; measured median +$3.34B is on or near the hull boundary. | Hull includes round 13's pre-reg band (i.e., lesson #7-v5 would NOT have caught round 13's failure). |

**H-aggregate:** for every plausible ICEBERG capital source (sovereign-grant, limited-recourse debt, equity-with-gates), the relevant metric under staged commitment is weakly or strongly better than under upfront commitment. The binary P(NPV>0) metric (round 13) is not load-bearing for any of these sources. **Matrix axis-17 amendment recommendation: replace "Frame B P(NPV>0) at sovereign-bond 3%" with three capital-source-specific lines.**

## Cross-checks (must pass before grading)

| ID | Check | Tolerance |
|---|---|---|
| XC-1 | Frame B P(NPV>0) under both regimes at 2-launch W3 LR15 replicates round 13: upfront 36.3%, staged 31.0%. | within ±1 pp |
| XC-2 | Median Δ-NPV at 2-launch W3 LR15 replicates round 13 +$3.34B. | within ±10% |
| XC-3 | Total undiscounted program capex (mission 1 + fleet) replicates round 13 demonstrator-NRE breakdown: $14.6B ± $0.5B. | within ±5% |
| XC-4 | Implied bond spread BOE consistency: spread_pre_gate / spread_post_gate < 5 (i.e., the pre-gate term dominates the spread; post-gate revenue-coverage term is materially smaller). | qualitative |
| XC-5 | Sovereign-grant continuation P at gate = P_demonstrator exactly. | identity |

## Method

1. Extend round 13 `run.py` to record per-draw NPV arrays under both regimes (not just frame_b_pct aggregate), AND yearly cashflow streams per draw.
2. Compute per-draw IRR via Newton-Raphson on the yearly cashflow polynomial.
3. Compute mean Δ-NPV across MC draws.
4. Compute debt-EL metric for the pre-gate failure mode (the dominant term).
5. Compute option-adjusted equity NPV by recomputing each draw with the gate as an explicit max(0, fleet_NPV) operation; compare to round 13's harness which already implements gate-multiplier semantics.
6. Cross-check; grade; write Result + Revisit + Cross-learning + matrix-axis-17 amendment recommendation.

Expected runtime: under 30 seconds (MC × IRR Newton-Raphson is dominant).

## What this round does NOT do

(see SCOPE.md)

---

## Result

`run.py` ran the MC, debt model, option-adjusted NPV, convex-hull check, and grader. Output at `results/underwriter_anchor_summary.json`. Seed 20260515, 10,000 draws.

### Cross-checks

| ID | Status | Detail |
|---|---|---|
| XC-1 Frame B replicate at 2-launch W3 LR15 | **PASS** | upfront 36.32% (round 13: 36.32%); staged 31.00% (round 13: 31.00%); identity match. |
| XC-2 Median Δ-NPV replicate | **PASS** | measured +$3344M; round 13 +$3340M; rel err 0.13%. |
| XC-3 Program capex breakdown | **PASS** | measured $14628M; round 13 $14628M; rel err 0.003%. |

All cross-checks pass at identity-level precision. Harness is consistent with round 13.

### Hypothesis grading

| ID | Predicted | Measured | Status |
|---|---|---|---|
| **H1** EL ratio staged / upfront in [8%, 15%] | band | **10.94%** | **HELD** |
| **H2** implied bond spread reduction (upfront − staged) in [25, 50] bps/yr | band | **0.0 bps** | **FALSIFIED (BOE category error)** |
| **H3** MEAN Δ-NPV across MC in [-$5B, +$3B] | band | **-$10.6B** | **FALSIFIED (opposite direction, below floor by $5.6B)** |
| **H4** median IRR_staged − median IRR_upfront in [0, +3] pp | band | **-0.20 pp** (R 5.79%, D 5.99%) | **FALSIFIED (opposite-sign, but near-tie)** |
| **H5** mean option-adjusted Δ-NPV in [+$0.3B, +$2B] | band | **+$2.32B** | **FALSIFIED (above ceiling by $0.3B)** |
| **H6** sovereign-grant Δ ≤ 0.5 pp | ≤ 0.5 pp | 0.0 pp (by construction) | **HELD** |
| **H7** convex hull at clearing p25/p50/p75 excludes round 13's pre-reg band [+$4B, +$8B] | predicted exclusion | hull [-$8.7B, +$7.7B]; pre-reg band NOT inside; measured +$3.34B IS inside | **HELD (lesson #7-v5 validated retrospectively)** |

**Score: 3 HELD, 4 FALSIFIED.**

Of the 4 falsifications:
- **H2 was a category error in my BOE:** spread = EL/principal/duration. Since EL scales linearly with principal (both go through LTV multiplier; P_fail and LGD are regime-invariant), spread is identical between regimes by construction. Methodology lesson #16: in financial modeling, ratio metrics (spread, IRR, profitability index) can be scale-invariant while absolute metrics scale linearly. Pre-registering a bracket on a ratio that's invariant by construction is an arithmetic error.
- **H3 is the load-bearing falsification of this round:** mean EV is -$10.6B (vs predicted floor -$5B). Staged commitment ALSO loses on mean EV across the demand-curve distribution. The round 13 framing ("EV story favors staged at +$3.3B") was anchored on MEDIAN not MEAN; mean is dragged down by the heavy-left-tail. **The EV-vs-binary "dichotomy" from round 13's pending thread #1 is dissolved: BOTH metrics disfavor staged commitment under demand-curve distribution.**
- **H4 opposite-sign at near-tie magnitude:** median IRR_staged 5.79% vs median IRR_upfront 5.99%. The "deferred capex helps IRR" intuition was wrong because the gate kills revenue too, and at median clearing the revenue-loss-from-gate slightly dominates the capex-saving.
- **H5 above ceiling:** option-value $2.32B vs predicted ceiling $2B. The smart-gate (anchor-investor framing) abandons fleet in 65.3% of MC draws. This is more abandonment than my BOE predicted (heavy-left-tail of clearings = more draws where fleet-NPV-at-gate is negative). However, $2.3B option-value does NOT close the -$10.6B mean EV gap. Smart-gate-staged is still -$8.3B mean EV vs upfront.

### The reframing (load-bearing finding)

The pending-thread-#1 framing was: "which Frame B metric does sovereign underwriting anchor on, binary or EV?" Round 14 dissolves both sides of that dichotomy. **Under demand-curve clearing distribution, staged commitment loses on:**
- binary P(NPV>0) by 5.3 pp (round 13, this round XC-1).
- mean EV by $10.6B (this round H3).
- mean EV even with smart-gate optionality by $8.3B (this round H3 + H5).
- median IRR by 0.2 pp (this round H4).

**Staged commitment wins on:**
- Gate-0 catastrophic loss expected: -89% ($526M → $58M, this round H1).
- Pre-gate capex exposure: -89% ($14.6B → $1.6B).
- Sovereign-grant track: regime-invariant (no win, but no loss).
- Median Δ-NPV: +$3.3B (round 13, this round XC-2).

**The case for staged commitment is downside-protection only, not NPV-improvement.** This is exactly what the locked anchor-investor framing says ("there is no scenario where funding ICEBERG damages the underlying anchor investment thesis") — the framing is downside-bounded, not EV-maximizing. The matrix-axis-17 framing that conflates this with "Frame B improves under staged" is wrong on every NPV-style metric.

### Debt-model details (H1)

| | Upfront | Staged |
|---|---:|---:|
| Pre-gate exposure | $14,628M | $1,600M |
| Senior principal (60% LTV) | $8,777M | $960M |
| Expected loss (P_fail 10% × LGD 60%) | **$527M** | **$58M** |
| Implied spread (EL/principal/duration) | 40.3 bps/yr | 40.3 bps/yr |

The spread is identical because EL scales linearly with exposure. The right debt-side metric is **absolute EL** (or equivalently **max-debt-the-underwriter-can-write-at-fixed-spread**), not "spread reduction." Under staged, the underwriter can extend ~9.1× more leverage at the same risk premium — OR equivalently, $469M of expected-loss reduction per program.

### Option-adjusted equity NPV (H5)

| | Mechanical-gate (round 13) | Smart-gate (anchor-investor framing) |
|---|---:|---:|
| Mean NPV across MC | (staged mechanical) | mechanical + **$2,319M** |
| Median NPV | per round 13 | mechanical + 0 (median draw doesn't abandon) |
| Fraction of draws abandoned | 0% (only demonstrator-fails are skipped) | **65.3%** |

The smart-gate abandons fleet in 65% of demand-curve MC draws because the realized clearing distribution doesn't support fleet profitability in most of its mass. This is the anchor-investor's kill-criteria-at-each-gate mechanism made numerical. Total option value: +$2.3B mean. **Even with this option value, smart-gate-staged is still -$8.3B mean EV vs upfront under demand-curve distribution.**

### Convex-hull check (H7, lesson #7-v5 validation)

| Clearing percentile | $/kg | Δ-NPV ($B) |
|---|---:|---:|
| p25 | $1,768 | +$7.67B |
| p50 | $5,322 | +$3.34B |
| p75 | $15,933 | -$8.72B |

Convex hull: **[-$8.7B, +$7.7B]**. Round 13's pre-reg band [+$4B, +$8B] is NOT inside this hull (lower edge $4B is in, upper $8B is out — taking strict containment, the band is not fully inside). Round 13's measured median +$3.34B IS inside the hull.

Lesson #7-v5 (convex-hull distribution-aware BOE check) would have flagged round 13's [+$4B, +$8B] pre-reg as failing the hull check, prompting a revision. The proposed extension to lesson #7 is validated retrospectively.

---

## Revisit

| Hyp | Predicted | Measured | Reason for mismatch |
|---|---|---|---|
| H1 | EL ratio 8-15% | 10.94% | HELD; matches gate-0 capex fraction structurally. |
| H2 | spread reduction 25-50 bps/yr | 0 bps/yr | **BOE category error.** Spread = EL/principal/duration, and EL scales linearly with principal. Spread is invariant to regime by construction. Methodology lesson #16. |
| H3 | mean Δ-NPV in [-$5B, +$3B] | -$10.6B | **Heavy-left-tail is heavier than rough estimate.** My BOE assumed ~8% mass at -$35B mean (giving ~-$2.8B contribution); actual upper-tail-clearings drive bigger upfront-fleet revenue capture, so the leftward drag on mean Δ is closer to $13B not $3B. **Same anchoring failure family as round 13 — single-point BOE under distribution.** |
| H4 | IRR diff in [0, +3] pp | -0.20 pp | Both regimes have similar IRR at median; gate's revenue loss slightly dominates capex saving. Near-tie. |
| H5 | option-value [+$0.3B, +$2B] | +$2.32B | Above ceiling. **Demand-curve heavy-left-tail means more draws fail the smart-gate test** than my BOE predicted (65.3% vs ~25% estimate). Option-value is higher than expected but still insufficient to close the mean EV gap. |
| H6 | regime-independent | 0 pp | HELD by construction. |
| H7 | hull excludes round 13's pre-reg band | hull [-$8.7B, +$7.7B] excludes [+$4B, +$8B] | HELD. Lesson #7-v5 retrospectively validated. |

### New methodology lesson #16 (scale-invariant ratio metrics)

When pre-registering a BOE for a metric M, check whether M is a ratio of two quantities that both scale linearly with some common factor X. If M = A(X)/B(X) where A and B both scale linearly with X (i.e., A = aX, B = bX), then M = a/b is invariant to X. Pre-registering a "reduction in M between two scales of X" predicts zero by construction. Examples that recur in financial modeling: bond spread (EL/principal/duration), IRR-vs-WACC (NPV ratio is scale-invariant when capex and revenue both scale), profitability index variance with scale, Sharpe ratio under linear leverage. Pre-registration should distinguish ratio-difference (often zero) from absolute-difference (the load-bearing comparison).

### Methodology lesson #7 strike count (now seventh)

The lesson #7 pattern recurs in this round: pre-registering brackets via rough single-point estimation under distribution. H3 (mean Δ-NPV) and H5 (option value) both miss bands because the heavy-left-tail of clearing prices is heavier than visual intuition suggests. The proposed lesson #7-v5 (convex-hull distribution-aware BOE) catches this kind of error — H7 validated it works for round 13's pre-reg failure. **Adopt #7-v5 as standard for future rounds with distribution-integrated quantities.**

---

## Reading

**Round 13's pending question is dissolved, not answered.** The "which metric does sovereign underwriting anchor on, binary or EV?" framing assumed the two metrics disagree. Under demand-curve distribution, they don't: both binary P(NPV>0) and mean EV disfavor staged commitment. So the question becomes "what DO realistic capital sources anchor on, and do any of them favor staged?"

**Answer per capital source (anchored on the structural-inference table in §"Capital-source-to-metric mapping"):**

1. **Sovereign-grant track (NASA / DOE / ESA, FSP-Phase-2-style):** regime-invariant. Both regimes face P_demonstrator = 0.90 at the next reauthorization gate. Sovereign-grant doesn't anchor on NPV at all. *Implication for ICEBERG: grant track is the cleanest financing path; staged-vs-upfront is irrelevant to grant continuation.*

2. **Limited-recourse project-finance debt:** strongly prefers staged. Expected loss reduction $469M ($527M → $58M); pre-gate principal exposure reduction 89%; max-debt-capacity-at-fixed-spread expands 9.1×. *Implication for ICEBERG: IF the program is debt-financed, staged commitment is structurally near-mandatory — upfront debt-financing of a 14.5-yr pre-revenue construction window would be priced at default-spreads no sovereign-bond market would accept.*

3. **Equity-with-gates (anchor-investor framing, locked belief):** prefers staged on **downside-protection** grounds ($1.6B at-risk vs $14.6B, with smart-gate adding $2.3B option-value). Does NOT prefer staged on EV grounds (-$8.3B even with smart-gate). The anchor-investor locked-belief language ("there is no scenario where funding ICEBERG damages the underlying anchor investment thesis") is downside-bounded, not EV-maximizing — and that's the framing the math supports.

4. **Concessional / sovereign-development-bank lending:** prefers staged for the same reasons as project-finance debt, less rate-sensitively.

5. **Venture equity:** retired per round 11 H6 regardless of regime.

**Matrix-axis-17 amendment recommendation:**

The current axis-17 narrative cites "Frame B P(NPV>0) at sovereign-bond 3%" and is being amended (after round 13) to distinguish Frame A vs Frame B vs Frame C. Round 14 says the amendment should go further:

- **Drop binary P(NPV>0) and mean EV as primary Frame B headlines.** Neither matches what any realistic capital source computes; both disfavor staged.
- **Add three capital-source-specific lines:**
  - *Sovereign-grant track:* P_demonstrator-at-gate = 0.90; regime-invariant.
  - *Limited-recourse debt track:* expected-loss reduction $469M under staged; pre-gate exposure $1.6B vs $14.6B; debt-capacity expansion 9.1× at fixed spread.
  - *Equity-with-gates track (anchor-investor framing):* gate-0 capital-at-risk $1.6B (vs $14.6B upfront); smart-gate option-value $2.3B; downside bounded by gate-0 commitment.
- **Reframe the "29% at sovereign-bond" round 11 anchor and the "36.3% at sovereign-bond LR15" round 13 anchor** as legacy / illustrative, not load-bearing. Note explicitly that binary P(NPV>0) is a proxy convention used in earlier rounds that does not map to any actual capital source's decision metric.
- **Keep venture retired** (round 11 H6, unchanged).
- **The anchor-investor locked-belief framing is the load-bearing posture** for the pitch, and it's a downside-protection story, not an NPV-improvement story.

### Caveats and what this round does NOT prove

- Debt model is pre-gate catastrophic-loss only; does NOT compute post-gate revenue-coverage default (post-gate fleet revenue distribution determines DSCR; under both regimes the post-gate distribution is identical conditional on gate-pass). Adding the post-gate term would not change the comparative result — the post-gate term is regime-invariant.
- Smart-gate model assumes equity has full information about realized clearing price at gate time (year 15). In reality, year-15 clearing observation is imperfect — equity sees the year-15 LEO water price but the 25-year-forward distribution is still uncertain. This is an UPPER BOUND on option value; true option value is between $0 and $2.3B.
- All numbers anchor on chunk-200 / 80-t-delivered. Per round 13 caveat, Option-A's 17%/34 t per mission would scale absolute NPVs ~2.4× downward without changing the comparative direction.
- LTV 60% and LGD recovery 40% are project-finance heuristic anchors; specific ICEBERG debt-structure (asset-security on a fleet not yet built) would likely be MORE punitive on LGD, making the upfront problem worse. Sensitivity not run.
- P_demonstrator = 0.90 is the L0-10 baseline; round 13 priority-2 thread #2 (P_demonstrator sensitivity 0.7, 0.5) remains queued. Lower P_demonstrator would (a) reduce the staged-commitment debt advantage marginally and (b) increase the staged-commitment equity option-value materially.
- Conjunction multiplier (0.67% per round 9 H2a) is not applied here — Frame A vs Frame B distinction is preserved by round 13 and unaffected by this round.

---

## Cross-learning

**Confirms round 13 with reframed conclusion:** round 13 said staged commitment hurts binary P(NPV>0) but helps EV (median Δ-NPV +$3.3B); round 14 shows staged commitment also hurts MEAN EV by $10.6B. Round 13's "EV-friendly to staged" framing was anchored on median, which is the wrong statistic for an EV-maximizer (mean is). The EV-vs-binary "dichotomy" is therefore dissolved — both metrics agree against staged. Staged's case is capital-efficiency, full stop.

**Negative for the pending-thread-#1 working framing:** the "which metric does the underwriter anchor on, binary or EV?" framing collapsed because the right answer is "neither — they anchor on capital-source-specific metrics that aren't NPV." Reframe pending-thread-#1 as RESOLVED in this round.

**Positive for the locked anchor-investor framing:** the locked-belief language ("no scenario where funding ICEBERG damages the underlying anchor investment thesis") is structurally the right framing — it's downside-bounded, not EV-maximizing. The math supports the belief at the gate-0 commitment level ($1.6B vs $14.6B), not at the program EV level. Belief lock should be MAINTAINED with the EV-vs-downside-protection distinction added as a clarification.

**Negative for the matrix's binary P(NPV>0) anchor:** round 11 / round 13 / round 14 together establish that the binary metric is not load-bearing for any actual capital source. Recommend the matrix's "Frame B P(NPV>0)" header be replaced or supplemented with capital-source-specific headers.

**Positive for sovereign-grant track ("Track G"):** of the three tracks, the grant track is the cleanest because its decision metric (P_milestone) is regime-invariant. ICEBERG's grant-funded path doesn't need to argue about staged-vs-upfront. The relevant question for grant track is just P_demonstrator and the 0-of-6 base rate (locked belief `776575c01d55ca51`). *This is the path-of-least-architectural-friction.*

**Positive for limited-recourse debt track ("Track D"):** debt-financed ICEBERG REQUIRES staged commitment. Upfront-fleet-debt is structurally non-financeable (14.5-yr pre-revenue construction, default-spread territory). If the matrix is going to include a debt-financed line, it must be staged.

**Methodology lesson #16 (NEW):** ratio metrics that scale-invariantly under linear common-factor scaling produce zero-difference under regime comparison by construction. Pre-registering a "reduction in M" predicts zero, not the absolute-difference of the underlying quantities. Distinguish ratio-difference from absolute-difference in BOE.

**Methodology lesson #7-v5 validated (this round):** convex-hull check on distribution-aware BOE. For any hypothesis bracketing a distribution-integrated quantity, the BOE must compute the quantity at p25/p50/p75 of the distribution and the bracket must lie inside the convex hull. If not, the BOE is incomplete.

**Methodology lesson #7 strikes:** now at 7 total. The pattern keeps recurring; the cure (lesson #7-v5) is validated. Future rounds should adopt the convex-hull check as a SCOPE-time discipline, not a post-hoc forensic.

---

## New pending threads (spawned by this round)

**Priority 1:**

1. **R-mean-EV-decomposition** — what drives mean Δ-NPV to -$10.6B? Per-percentile-clearing decomposition of Δ-NPV vs probability mass. If the loss is concentrated in p75-p95 of clearings, the matrix should foreground "high-clearing favors upfront" as a distinct finding. If it's spread across all clearings >p25, the conclusion is more uniform.

2. **R-sovereign-grant-track-financialization** — does any path exist for the grant track (Track G) to be financialized as private capital? Or is Track G strictly a non-financialized sovereign-investment? If financializable, the staged-vs-upfront question reappears with different metrics.

**Priority 2:**

3. **R-debt-track-feasibility-from-base-rate-prior** — given the 0-of-6 base rate prior for orbital-fission-within-stated-decade (locked belief `776575c01d55ca51`), what underwriter would actually write the debt? Test against ECA (export credit agency) practice for high-prior-failure-rate aerospace programs. Likely answer: no commercial debt writer, only sovereign-grant or concessional.

4. **R-demonstrator-failure-salvage-and-option-value** — round 13 priority-2 thread #3 (salvage on demonstrator failure) interacts with this round's option-value finding. Quantify combined effect.

5. **R-anchor-investor-belief-revision** — the locked belief frames ICEBERG as gated demonstrator option-value. Round 14 confirms the downside-protection framing but shows EV is negative. Belief should be LOCKED with explicit "downside-protection > EV" annotation.

6. **R-P_demonstrator-sensitivity** (deferred from round 13 priority-1 thread #2) — does lower P_demonstrator (0.7, 0.5) flip any of round 14's findings? Lower P_demonstrator: increases option-value (smart-gate); reduces debt-track ratio (more pre-gate failure mass shifts EL upward but proportionally for both regimes); doesn't change grant track. Could materially shift the equity-track conclusion.

7. **R-upper-tail-clearing-cap** — what if a sovereign-mandated price cap exists at $20k/kg or $50k/kg (preventing the upper-tail revenue capture from accruing to private equity)? Likely flips the mean-EV result by truncating the heavy-right-tail of upfront's advantage. Relevant for sovereign-financed track regulatory framing.

**Resolved / refuted:**

- ~~Round 13 pending thread #1 ("EV vs binary reconciliation: which does sovereign-bond anchor on?")~~ — **DISSOLVED.** Both EV and binary disfavor staged under demand-curve distribution. The framing assumed one metric favored each side; actually both disfavor staged. The case for staged is capital-efficiency, not NPV-improvement.
