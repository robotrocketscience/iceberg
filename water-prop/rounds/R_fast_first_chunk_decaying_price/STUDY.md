# R-fast-first-chunk-decaying-price — STUDY

**Round:** R-fast-first-chunk-decaying-price (worktree-115637, 2026-07-21 latest+25)
**One line:** The project-owner "fast small first chunk, longer later round-trips" hypothesis, re-tested under R188's *decaying* clearing price — the one input `R_heterogeneous_cadence` explicitly deferred. **Re-confirmed falsified even under the most favorable (decaying) price; the two [W]/compound falsifications sharpen the real lever: defer capex, don't compress it.**

## Hypotheses (pre-registered in SCOPE.md; bounds in scope_bounds.py)

**Test.** `run.py` folds R188's `price(t)=P0·exp(−rate·t)` into `R_heterogeneous_cadence`'s exact engine (schedule builders copied verbatim; only the revenue term changed). Deterministic. Regime-D Δ-NPV is closed-form (mission-1 delivery term only, since missions 2..N are identical between het and homogeneous schedules); Regime-R uses the full fleet engine.

## Result

| ID | Predicted (SCOPE band) | Measured | Held? |
|---|---|---|---|
| **H1 [XC]** decay-off reproduces het | cell α ∈ [−130,−95]; chunk-200 = 0; monotonic | closed-form = full-engine = **−112.7** (het α exact); chunk-200 = 0.0; monotonic −112.7/−95.5/−62.2/−30.4/0 | **HELD** |
| **H2 [S]** decay on: still loses, penalty collapses | Δ<0 at all anchored rates; central penalty [−40,−8]M; flip ~[65,90]%/yr | chunk-25 Δ = −39.8/−23.1/−11.0/−1.1M (cons/central/median/bull) all <0; central band [−26.4,−19.8]M; **flip = 76%/yr** | **HELD** |
| **H3 [S]** time dominates mass | per-mission gain [$4,10]M **and** fleet-compression dwarfs chunk-shrink | per-mission **$4.9M** (in band) ✓; but **fleet compression = −$206M** (capex −$269M, revenue +$63M) — naive compression is net-NEGATIVE | **FALSIFIED (compound)** |
| **H4 [W]** Regime-R advantage shrinks, stays + | positive, [+300,+2000]M, below static | **+$5,626M** — positive but **GROWS** above static (+$1,450M) and exceeds band | **FALSIFIED (in direction)** |

**Score: 2 HELD, 2 FALSIFIED** (both falsifications informative and mutually coherent). Figure: `results/fast_first_decay.png`. Data: `results/findings.json`.

### Cross-checks (internal consistency)
- Closed-form Regime-D Δ == full-engine Δ at rate 0 (−112.7 both) → engine faithful.
- Regime-R advantage at P0=$2.5/t, rate 0 == **+$2,733M**, reproducing het_cadence's headline exactly → the fleet engine is verified against the prior round.
- chunk-200 (homogeneous limit) Δ = 0 exactly.

## Reading

**The user's chunk-shrinking hypothesis is re-confirmed dead — and this time under the price assumption most generous to it.** A decaying clearing price is the strongest case *for* front-loading (deliver early, before the price craters). Even so:

1. **H2 — it still loses at every anchored decay rate.** Decay *collapses* the chunk-25 penalty from −$158M (static) to −$23M (central), an 85-89% narrowing, because the fast mission-1 delivers 2.6 yr earlier into a higher price. But it never flips: the break-even decay is **76%/yr**, more than double the bull-case 32.4%. The 8× delivered-mass loss of a 25-t vs 200-t mission-1 dominates the timing gain at any credible rate.

2. **H3/H4 — the two falsifications tell one coherent story.** The per-mission revenue-timing gain is real ($4.9M) and confirms chunk-shrinking is a dominated micro-optimization. But you **cannot bank it at fleet scale by compressing the schedule** (H3): pulling the whole committed fleet 1 yr earlier is *net-negative* (−$206M) because it un-discounts capex (−$269M) faster than it rescues already-decayed revenue (+$63M). The value is not in compressing committed capex — it is in **deferring capex you may not need** (H4): under decay, stage-gating the same fleet on mission-1 success grows *more* valuable (+$1,450M → +$5,626M), because Regime D sinks full capex into later missions whose delivered-water revenue the decay has already erased. **Decay reinforces het_cadence's original answer** ("stage-gate the same fleet") rather than reviving the chunk-shrink proposal.

**Net for the USER-NOTES hypothesis:** *fast first chunk* is right only in the trivial sense that the demonstrator returns a small chunk quickly (already state-of-record, REQUIREMENTS §7.5). *"Later vehicles take longer round-trips into the green"* is falsified: longer, later, decayed deliveries are worth less, not more, and shrinking the first chunk to go faster loses on mass. The lever is capital timing (defer via staging), not chunk size or schedule compression.

## Revisit (mandatory)

- **H1 held exactly** — the closed-form identity (Regime-D Δ = mission-1 delivery term) was verified against het cell α and the full engine; high confidence the port is faithful.
- **H2 held**, including the 76%/yr flip rate derived in the pre-script and reproduced in run.py.
- **H3 falsified as a compound claim — I over-reached in pre-registration.** The per-mission timing gain (part a) held in band; the "applied across the ~28-delivery fleet it dwarfs" extrapolation (part b) was wrong: I implicitly assumed you could compress the fleet to bank 28× the per-mission gain, but compression pulls capex forward too, and under decay+discount that un-discounting dominates. **Lesson: a per-mission revenue-timing BOE does not extrapolate to a whole-program compression value — capex timing must be carried in the same calculation.** (Recurring methodology-lesson-7 family: per-endpoint BOE.)
- **H4 falsified in direction — an honest [W] miss with a clean mechanism.** I predicted the Regime-R advantage would *shrink* under decay (deferred revenue decays). It *grows*, because the decay hurts the committed-fleet baseline (Regime D) more than it hurts the gated, deferred fleet (Regime R). I under-weighted that Regime D's *late* deliveries are the ones decay destroys, and Regime D pays their capex regardless. Kept as FALSIFIED; no goalpost move.

## Bug-catch

- **Grading-code bug (caught, fixed pre-STUDY):** run.py v1 graded H3 by comparing the *per-mission* gain ($4.9M) to the chunk-shrink loss ($23M) — apples-to-oranges, and not what SCOPE registered. SCOPE's H3 text registered the *fleet-level* comparison. Fixed run.py to compute the actual fleet-compression value (whole-schedule shift with capex + revenue decomposed). The fix *changed the H3 verdict's basis* but not honestly its outcome — H3 is falsified either way; the fix makes the falsification mechanism explicit (capex un-discounting) rather than hiding it behind a mismatched criterion. Documented per "corrections live forward."
- **Floor artifact check:** the compression test floors shifted launch years at 0; the −$206M is not a floor artifact — the capex/revenue decomposition (−$269M / +$63M) shows the sign is driven by capex un-discounting, robust to the floor.
- No NaN/precision issues (deterministic closed forms + finite schedule sums).

## Cross-learning

- **Backward to `R_heterogeneous_cadence`:** its verdict survives the strongest counter-assumption (decaying price). Positive: adopt its "stage-gate the same fleet, don't shrink the chunk" reading as decay-robust.
- **Backward to R188 `R_clearing_price_time_path`:** the decay's schedule-level consequence is now priced — it does not revive front-loading; it *strengthens* the case for capital deferral (staging) over fleet commitment.
- **Forward to design-axes 02 / 10:** the USER-NOTES fleet hypothesis is re-confirmed falsified under decay; axis 10's "round-trip duration = revenue-decay exposure" gains the sharper reading that *committing* the fleet up front (not just the duration) is the exposure, and staging is the mitigant.
- **Methodology (flagged, not fixed here):** a real-options / Monte-Carlo version over R188's *distribution* of decay rates (not just the point path) is a named follow-on — **R-staged-commitment-under-decay-distribution** — if the project owner wants the probabilistic envelope. Not SCOPE'd.
