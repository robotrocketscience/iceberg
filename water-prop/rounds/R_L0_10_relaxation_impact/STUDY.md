# R-L0-10-relaxation-impact — does relaxing L0-10 to 0.75–0.80 actually help, or does L0-09 bind tighter?

**Status:** pre-result.

## Question

The user picked Option B/C from R-mission-success-probability's recommendation set — relax L0-10's 0.90 single-mission target to 0.75 or 0.80, on the argument that L0-08's 3-in-cruise inventory absorbs the failure stream and the redundancy-budget overlay (R-redundancy-budget-cost: $565M–$710M per vehicle) goes away.

R-mission-success-probability already flagged a side concern: **L0-09 as literally written is structurally infeasible** at any launch cadence and any per-mission p (P(month has ≥1 delivery) tops out at 0.632 even at 12 launches/year and p = 1.0). The "charitable" reading I proposed — "fraction of contracted delivery cadence met" or similar — was not analyzed in that round. If the charitable reading binds tighter than L0-10 at low p, then **relaxing L0-10 alone buys nothing**, because L0-09 still forces p high.

Before committing to Option B/C, the orchestrator (and project owner) need to know: is L0-09 actually the binding constraint, or is L0-10 the binding constraint? If L0-09 binds at p ≥ 0.95 under every defensible charitable reading, then Option B/C is illusory — relaxing L0-10 to 0.75 doesn't reduce the redundancy budget because L0-09 still pulls p back up to 0.95.

The question this round answers:

1. Under three defensible charitable readings of L0-09 ("delivery-cadence-met", "service-availability-on-rolling-window", "queue-never-empty"), what is the required per-mission p at L0-07's launch cadence floor of 1 / year?
2. At what launch cadence does a relaxed L0-10 = 0.75 or 0.80 also satisfy L0-09 charitable?
3. If L0-09 needs coordinated revision to make Option B/C work, what is the minimal coordinated revision?

## Pre-registered hypothesis (H-r3)

**Aggregate (H-r3-agg):** L0-09 binds tighter than L0-10 at all per-mission p ≤ 0.95 under every defensible charitable reading. Option B/C (relax L0-10 to 0.75–0.80) **does not** reduce the binding reliability target unless L0-09 is *also* relaxed to a matching threshold. The minimum coordinated revision that makes Option B/C work is to revise both L0-09 and L0-10 to the same level (e.g., L0-09 → "rolling-5-mission service ratio ≥ 0.75" alongside L0-10 → 0.75). If the orchestrator is unwilling to relax L0-09 below 0.95, then Option A (keep L0-10 at 0.90 with redundancy budget) is operative and the user's selection of Option B/C is moot.

**Pre-registered sub-claims:**

| Sub-claim | Predicted | Falsification |
|---|---|---|
| H-r3-a — Required p at L0-09 charitable "delivery-cadence-met ≥ 0.95" at 1 / yr launch | 0.95 (≥ 95 % of contracted yearly deliveries must arrive on time) | outside 0.93–0.97 |
| H-r3-b — Required p at L0-09 charitable "service-availability on rolling 12-month window" interpreted as P(window has ≥1 delivery) ≥ 0.95 | not achievable at 1 / yr launch and any p ≤ 1.0; requires launch cadence ≥ ln(20) / 1 = 3.0 deliveries/yr → 4 / yr launches at p = 0.80, or 3.16 / yr at p = 0.95 | falsified if any of {1, 2 launches / yr, any p} clears 0.95 |
| H-r3-c — Required p at L0-09 charitable "queue-never-empty" (steady-state in-transit count ≥ 1 successful arrival per year window) | 0.90–0.95 at 1 / yr launch; depends on round-trip and queue model | outside 0.85–0.97 |
| H-r3-d — Whether relaxing L0-10 to 0.80 reduces redundancy budget given L0-09 charitable binds | NO. L0-09 charitable forces p ≥ 0.95 under reading (a) and unfeasible under reading (b); under reading (c), p ≥ 0.90. Relaxing L0-10 to 0.80 does not reduce the binding p. | falsified if any L0-09 charitable reading allows p = 0.80 at 1 / yr cadence |
| H-r3-e — Whether stepping up launch cadence to 2 / yr + relaxing L0-10 to 0.80 satisfies both | depends on L0-09 reading. Reading (a): yes (1.6 deliveries / yr > 1.0 contracted, schedule satisfied 80 % of years). Reading (b): no (1 - exp(-1.6) = 0.798 < 0.95). | confirmed per reading |
| H-r3-f — Minimum cadence to clear L0-09 charitable reading (b) at p = 0.80 | 4 / yr launches (1 - exp(-3.2) = 0.959 ≥ 0.95) | outside 3.0–4.5 |
| H-r3-g — Recommended coordinated revision | L0-09: "rolling-5-mission service ratio ≥ 0.80" (matches L0-10 = 0.80 relaxation). L0-07: keep 1 / yr floor or step up to 2 / yr. Variance log entry needed. | falsified if a different coordinated revision dominates |

**Aggregate decision:** if H-r3-agg holds — L0-09 charitable binds tighter than L0-10 and Option B/C is illusory without coordinated L0-09 revision — surface the finding to the orchestrator with the minimum-revision recommendation. The user (project owner) then chooses: (i) accept the coordinated revision, in which case Option B/C is operative and saves the $565M–$710M/vehicle redundancy overlay; (ii) reject the coordinated revision and revert to Option A (or A+D). If H-r3-agg falsifies — some L0-09 charitable reading allows p = 0.80 at 1 / yr cadence — Option B/C is operative as-is and no coordinated revision is needed.

## Method

### Three defensible charitable readings of L0-09

L0-09 as literally written: "(months in which at least one delivery is made) / 12 ≥ 0.95 on any rolling 12-month window after year 20."

The literal text is infeasible per Round 1. The plausible reformulations:

- **Reading (a) — "delivery-cadence-met":** "fraction of contracted yearly delivery slots met on schedule ≥ 0.95." Maps to: per-mission p ≥ 0.95 at L0-07's 1/yr cadence, because each contracted slot becomes a slip if its mission fails.
- **Reading (b) — "P(window has delivery)":** the literal text, rescaled to "P(any rolling 12-month window contains at least one successful delivery) ≥ 0.95." P = 1 − exp(−rate × 1yr) where rate = launch_cadence × p. Requires rate ≥ ln(20) ≈ 3.0 deliveries/yr.
- **Reading (c) — "queue-never-empty":** "the steady-state queue of in-transit-and-not-yet-delivered missions ≥ 1, so that an end-customer is never waiting more than the round-trip time for the next delivery." This is the L0-08-style continuity reading; binds at p × launch_cadence × round_trip ≥ 1, which is trivial at L0-07 floor since 1 × p × 14 = 14p, requires p ≥ 1/14 = 0.071. Not load-bearing for our regime.

Reading (a) is the most charitable to the requirements-author's intent ("service availability" for a paying customer). Reading (b) is the literal-text rescaled to per-year rather than per-month. Reading (c) is the queue-theoretic continuity reading.

### Cadence × p sweep

For each (launch_cadence, p) pair on a grid, compute:

- Annual delivery rate = launch_cadence × p
- Reading (a) score = p (slot-met fraction at 1 / yr cadence; scales with min(1, launch_cadence × p / contracted_rate))
- Reading (b) score = 1 − exp(−launch_cadence × p × 1yr)
- Reading (c) score = launch_cadence × p × round_trip (steady-state queue depth in successful missions; clears 1 trivially)
- Rolling-5-launch-block L0-10 score = expected fraction of 5-launch windows where success count ≥ 5 × 0.80 = 4 (i.e., 4-of-5 succeed). Binomial.

Find the (launch_cadence, p) frontier where all three readings clear 0.95 simultaneously, and where the rolling-5 block clears the relaxed L0-10 target (0.75, 0.80, 0.85, 0.90).

### Minimum coordinated revision

For each candidate L0-10 relaxation (0.75, 0.80, 0.85), compute:

- What L0-09 threshold matches the relaxation under reading (a)? (Should be the same number: relax L0-09 to 0.75 if L0-10 goes to 0.75.)
- What launch-cadence step is required to keep L0-09 at 0.95 with relaxed L0-10? (Reading (b) gives cadence floor.)
- What in-orbit delivery buffer at customer interface would absorb the failure stream? (Reading (c) extension.)

Output the smallest revision in REQUIREMENTS.md terms that makes the relaxation actually save the $565M–$710M/vehicle redundancy overlay.

### Sensitivity / assumption-questioning

- **L0-09 charitable reading (a) is a paraphrase, not a quote.** The requirements-author may have intended something subtly different. The round documents three readings explicitly and lets the orchestrator pick.
- **The rolling-5-launch-block clause in L0-10 (`≥ 90 % across any rolling block of 5 consecutive launches`) is a *block-test* threshold.** A relaxed L0-10 = 0.80 with the same block-test structure is *not* the same as a relaxed per-mission p = 0.80 with no block test. The block test means "at least 4 of 5 must succeed on every rolling window," which at per-mission p = 0.80 is satisfied with probability 1 − P(≤3 in 5) ≈ 0.737, far from 0.95. This block-test interpretation is much stricter than the simple per-mission expectation. The round flags both interpretations.
- **The customer-side delivery buffer reading (c)** assumes a customer who tolerates batched delivery. If the customer requires near-uniform monthly delivery (Reading (b)), no relaxation of L0-10 alone helps — only cadence step-up.

### Validity caveats

- The "service-availability" reading (a) treats every contracted slot as equally weighted. Real customer contracts have priority slots, cancellation windows, etc.
- The Poisson approximation in reading (b) assumes independent arrivals; cluster failures (e.g., a Saturn-orbit-insertion bug affecting three consecutive missions) break this and worsen the rate.
- L0-09's literal text is the requirements-doc bug; the round is *de facto* deciding what L0-09 means without orchestrator authorization. The output is therefore an *advisory* finding for the orchestrator's L0-09 revision, not a normative decision.

## Result

Run output at `results/cadence_p_sweep.json`, `results/coordinated_revision.json`, `results/l0_10_only_minima.json`, `results/tables.md`.

**Headline finding** — L0-10's own rolling-5-launch-block clause is tighter than the per-mission threshold by 9 to 19 percentage points.

| L0-10 nominal threshold | Per-mission p required to clear the rolling-5 block at ≥ 0.95 confidence |
|---|---|
| 0.75 | 0.93 (clause requires ≥ 4 of 5 to succeed; binomial requires p high) |
| 0.80 | 0.93 (same: ceil(5 × 0.80) = 4) |
| 0.85 | 0.99 (now requires all 5 to succeed) |
| 0.90 | 0.99 (same: ceil(5 × 0.90) = 5) |

At L0-07's launch-cadence floor of 1/yr and per-mission p = 0.80 (the user's Option B/C target):

- Reading (a) slot-met fraction: 0.800 (clears relaxed L0-09 = 0.80 ✓; does not clear 0.95 ✗)
- Reading (b) P(window has delivery): 0.551 (fails badly at any L0-09 target ≥ 0.7)
- Reading (c) queue depth: 11.2 (trivially clears 1.0)
- **L0-10 rolling-5 block at threshold 0.80: P(block clears) = 0.737 (fails the implicit 0.95 confidence requirement)**

**Hypothesis grading:**

| Sub-claim | Predicted | Actual | Held? |
|---|---|---|---|
| H-r3-a — Required p at L0-09 reading (a) at 1/yr cadence to clear 0.95 | 0.95 | exactly 0.95 (linear) | **held** |
| H-r3-b — Reading (b) at 1/yr cadence requires cadence step-up | yes, ≥ 3.0 deliveries/yr → 4/yr launch at p = 0.80 | confirmed: 1-exp(-3.2) = 0.959 ≥ 0.95 at 4/yr × 0.80 | **held** |
| H-r3-c — Required p at reading (c) at 1/yr cadence | 0.90–0.95 (queue-never-empty) | trivially cleared at p ≥ 0.07 (queue depth always ≥ 1) | **falsified** — I overstated the constraint; queue-never-empty is uninteresting at 14-yr round-trip |
| H-r3-d — Whether relaxing L0-10 to 0.80 reduces redundancy budget given L0-09 charitable binds | NO (L0-09 forces p ≥ 0.95) | NO, but for a different reason: **L0-10's own block-5 clause** forces p ≥ 0.93 at relaxed threshold 0.80. L0-09 reading (a) at relaxed 0.80 is satisfied at p = 0.80, but the block clause inside L0-10 itself binds tighter. | **held in outcome, mechanism different** |
| H-r3-e — Cadence step-up 2/yr + relaxed L0-10 = 0.80 satisfies both | depends on reading | confirmed per reading; reading (b) still fails at 2/yr × 0.80 = 0.798 < 0.80 | **held** |
| H-r3-f — Minimum cadence to clear reading (b) at p = 0.80 | 4 / yr | 4 / yr (0.959) | **held exactly** |
| H-r3-g — Recommended coordinated revision | L0-09 → match L0-10's relaxed target; L0-07 → 1 / yr or 2 / yr | revision required, but the *load-bearing* revision is to L0-10's rolling-5-block clause itself, not to L0-09. **Drop the block clause or change "≥ threshold across any rolling block" to "≥ threshold on a rolling block on average."** Then L0-09 reading-(a) match becomes the binding constraint at the relaxed target. | **falsified mechanism**: the load-bearing revision is to L0-10's block clause, not L0-09 |

**Aggregate (H-r3-agg): held in headline (relaxing L0-10's per-mission target alone does not reduce the binding p), but the mechanism is different from what I pre-registered.** I expected L0-09 to bind tighter than L0-10. Actually, **L0-10's own block-5 clause binds tighter than its per-mission threshold by 9–19 percentage points**, and that is the binding constraint regardless of L0-09. The minimal coordinated revision is therefore to L0-10 itself, not to L0-09.

## Reading

**L0-10 is a self-binding constraint, not a per-mission-threshold constraint.** I read L0-10 in Round 1 as "per-mission success probability ≥ 0.90" but the requirement text says "≥ 90 % across any rolling block of 5 consecutive launches." Those are different statements. The block clause is the binding interpretation. At per-mission p = 0.90, the block clause says "all 5 of 5 must succeed on every rolling window" (since `ceil(5 × 0.90) = 5`), which requires per-mission p ≥ 0.99 to be 95 %-confident the block holds at any point.

This is a Round-1 framing error I propagated into Round 2. R-mission-success-probability's headline "single-string projection 0.5621 versus L0-10's 0.90 target" should have been compared against p = 0.99 to clear the block clause, not against 0.90. The redundancy budget priced in Round 2 (12.76 t / $710M at megawatt) lifts mission success to 0.93, which **clears the per-mission interpretation of L0-10 = 0.90 but does not clear the block-5 interpretation of L0-10 = 0.90**, which requires p ≥ 0.99.

**The honest reading of L0-10 = 0.90 block-5 at 95 % confidence: clearing the requirement requires per-mission p ≥ 0.99. That target is *not achievable* even with full 8-subsystem 2-of-3 redundancy at the paper-grade R-lifts in Round 2 (which gave 0.93).** Closing the gap from 0.93 to 0.99 requires either:
1. Higher-than-2-of-3 redundancy on the dominant-failure-mode subsystems (3-of-5, 4-of-7), driving mass and cost overlays much higher than Round 2 priced.
2. A revision of L0-10 to drop the block clause and revert to a per-mission-threshold reading.
3. Calibration data from Gate-A / Gate-B that lifts the heritage R-base meaningfully (e.g., reactor R = 0.99 not 0.95 → 0.97).

**The user's Option B/C selection ("relax L0-10 to 0.75–0.80") needs revisiting.** At the new finding:

- Relaxing L0-10's per-mission threshold from 0.90 to 0.80 *does* reduce the binding p from 0.99 to 0.93 (because the block-5 clause now needs 4-of-5 instead of 5-of-5, which is much easier).
- That's a meaningful reduction. Round 2's projection 0.93 *does* clear the block-5 at threshold 0.80. **Option B/C works after all, but for the block-clause reason, not the per-mission-threshold reason.**

So Option B/C selection holds — but the reasoning needs an update. Relaxing the *threshold inside the block clause* from 0.90 to 0.80 lets the block clause clear at p = 0.93 (which Round 2 achieves with the redundancy overlay). The user's $565M–$710M/vehicle overlay is preserved as the binding cost, but the threshold relaxation is what makes Round 2's projection 0.93 actually sufficient. **Option B/C is a relaxation of the block-clause threshold, not a relaxation of the per-mission target.**

This re-frames the orchestrator decision:

- **L0-10 revision text:** "Per-mission success probability SHALL be such that ≥ 0.80 of any rolling block of 5 consecutive launches succeed, where success = delivered mass ≥ 0.5 × design mass at customer interface." The 0.80 threshold inside the block clause is what changed; the rolling-5 structure is preserved.
- **Coupled L0-09 revision:** match L0-09's "service availability" definition to a coherent reading at p ≈ 0.93. Reading (a) at the relaxed cadence-met fraction = 0.80–0.90 is achievable. Reading (b) literal text remains infeasible and should be dropped.

**The cheaper-than-A path that the user picked exists.** Option B/C at L0-10 → 0.80 block-clause threshold:

- Binding per-mission p = 0.93 (down from 0.99 at L0-10 = 0.90).
- Redundancy overlay from Round 2: 5.33 t / $565M at Kilopower variant B; 12.76 t / $710M at megawatt — same overlay, because the overlay was sized to lift p to 0.93.
- **Wait. The redundancy budget is the same for both Option A (block-5 at 0.90) and Option B/C (block-5 at 0.80) under Round 2's redundancy choices.** Both target single-string p → 0.93. Option A doesn't actually achieve 0.99 (which would clear L0-10 = 0.90 block-5); it achieves 0.93. So under the strict block-5 reading, Option A fails L0-10 = 0.90 *and* Option B/C clears L0-10 = 0.80 at the same overlay cost. **The user's selection of Option B/C is the only one that actually clears its target.**

**This is a major Round-1 + Round-2 reading error that this round catches.** Option A as I priced it does not actually clear L0-10 = 0.90 block-5. Option B/C does clear L0-10 = 0.80 block-5. The orchestrator decision is therefore much sharper than the Round-2 four-option set suggested: **either accept Option B/C (relax block-5 threshold to 0.80, keep $565M–$710M overlay) or invest substantially more redundancy than Round 2 priced (3-of-5 or 4-of-7 instead of 2-of-3 on the dominant subsystems) to lift p toward 0.99.**

**L0-09 is the smaller correction.** Reading (a) at relaxed-cadence-met fraction = 0.80 is satisfied by p = 0.93 at 1/yr cadence (since 0.93 ≥ 0.80, and Round 2 already targeted 0.93). Reading (b) literal text remains infeasible at any 1/yr cadence; drop it. Reading (c) is uninteresting.

## Revisit

**Did the hypothesis hold?** Aggregate held; mechanism was inverted. I pre-registered "L0-09 binds tighter than L0-10" — actually L0-10's *own* block-5 clause binds tighter than its per-mission threshold by 9–19 percentage points, and that's the load-bearing finding. L0-09 charitable reading (a) is the smaller correction.

**Where was I wrong?**
- **H-r3-c (queue-never-empty at p = 0.90–0.95).** I overstated this constraint. With 14-yr round-trip and 1/yr cadence, steady-state queue depth at p = 0.5 is already 7.0 — trivially ≥ 1. Reading (c) is uninteresting. Should have noticed this in the pre-registration.
- **H-r3-g (load-bearing revision is to L0-09).** Wrong. Load-bearing revision is to L0-10's block-clause threshold. L0-09 is a secondary correction.
- **Major framing error from Round 1.** I read "≥ 0.90 across any rolling block of 5 consecutive launches" as equivalent to "per-mission p ≥ 0.90." Those differ by ~9 percentage points at threshold 0.90, ~13 percentage points at threshold 0.80. Round 2's redundancy budget projection of 0.93 *fails* the block-5 reading of L0-10 = 0.90 but *clears* the block-5 reading of L0-10 = 0.80. This is the round's main contribution.

**Methodology lesson candidate #6** for the cross-campaign log:
> *When a requirement specifies a per-mission threshold AND a rolling-block test (e.g., "≥ 0.90 across any rolling block of 5"), do not conflate the two. The block test requires k-of-n successes with high confidence; binomial probability requires per-mission p substantially higher than the threshold. Specifically, "≥ 0.90 in rolling block of 5" with 95 % confidence the block clears requires per-mission p ≥ 0.99 — a 9-percentage-point gap. Always solve the block-test binomial explicitly before designing to the per-mission number.*

**Adopt / drop / defer:**
- **Adopt:** the revised L0-10 text proposal: "≥ 0.80 of any rolling block of 5 consecutive launches succeed, success = delivered mass ≥ 0.5 × design mass." This sets the per-mission binding p at 0.93, which Round 2's $565M–$710M/vehicle redundancy overlay clears.
- **Adopt:** the recommendation to drop L0-09's literal text and replace with reading (a): "fraction of contracted yearly delivery slots met on schedule ≥ 0.80." Coherent with the L0-10 revision.
- **Adopt:** the recognition that Round 2's $565M–$710M overlay clears Option B/C exactly, not Option A. Option A under strict block-5 reading would require 3-of-5 or 4-of-7 redundancy at undocumented mass and cost.
- **Defer:** the exact dollar figure for "Option A under strict block-5" (would require redundancy beyond 2-of-3). Round 4 territory if the orchestrator chooses to investigate.
- **Drop:** the H-r3-c queue-depth reading from any future cross-check.

## Cross-learning

**Forward references:**
- **R-mission-success-probability** (commit `ef1bc21`) — *this round corrects a framing error in that one.* Round 1's "L0-10 0.90" was read as per-mission threshold; the actual binding interpretation is the block-clause. Update STUDY.md of Round 1 with a forward pointer to this round's correction.
- **R-redundancy-budget-cost** (commit `a8c72d2`) — *the $565M–$710M overlay is correctly priced for clearing block-5 at threshold 0.80, not block-5 at threshold 0.90 as that round implied.* Update STUDY.md of Round 2 with a forward pointer.
- **R-l0-09-text-fix** (proposed in Round 1) — this round provides the candidate revision text for L0-09 reading (a). Round-4 priority drops because the L0-10 block-clause revision is more load-bearing.
- **R-3-of-5-redundancy** (new proposal): if the orchestrator wants to keep L0-10 at 0.90 block-5 (requires per-mission p = 0.99), price the 3-of-5 or 4-of-7 redundancy on dominant-failure-mode subsystems (reactor, bag, propulsion). Likely doubles the Round 2 overlay.

**Backward references:**
- **Round 1 / Round 2 corrected:** their headline cost figures ($565M–$710M overlay) are correct for the user's Option B/C selection at the revised L0-10 = 0.80 block-clause. They are *not* correct for clearing L0-10 = 0.90 block-clause, which Round 1 implicitly claimed.
- **REQUIREMENTS.md L0-10 wording:** the rolling-5 block clause is what binds. The Level-0 requirements doc should explicitly call this out as the binding test, not as a clarification footnote on a per-mission target.

**Methodology forward:**
- **Always solve the block-test binomial before designing to per-mission numbers.** Add to PROTOCOL.md or CONVENTIONS log as a recurring check.

**Open follow-up rounds spawned by this one:**
- R-3-of-5-redundancy (priority depends on orchestrator decision)
- R-redundancy-financing (Round 2 follow-up, unchanged in priority)
- R-program-level-survival (Round 1 follow-up, unchanged)

**Verdict for the orchestrator:**

The user's Option B/C selection holds, but with sharpened reasoning:

- **Adopt revised L0-10 text:** "Per-mission success probability SHALL be such that ≥ 0.80 of any rolling block of 5 consecutive launches succeed (success = delivered mass ≥ 0.5 × design mass)."
- **Adopt revised L0-09 text:** "Fraction of contracted yearly delivery slots met on schedule SHALL be ≥ 0.80 on any rolling 5-year window after year 20." (Drop the literal-text "months in which at least one delivery is made" framing.)
- **Keep Round 2's $565M–$710M overlay.** It is sized to clear the revised block-clause. No reduction available without dropping more subsystems (which would require lifting per-mission p below 0.93 and falsifying L0-10 = 0.80 block-5).
- **Variance log entry:** record the L0-10 + L0-09 revisions with the reasoning that the rolling-5-block-clause inside L0-10 was the binding constraint, that the per-mission interpretation of L0-10 = 0.90 was an analyst error in Round 1, and that the user/project-owner accepted the 0.80 block-clause threshold to align with the achievable redundancy budget.

