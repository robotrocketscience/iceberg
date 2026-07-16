# R-arch-E-specific-power-flown-anchored — stress-test round 6's "conservative" 10 W/kg bookend against flown-system data

**Status:** pre-registration. Authored 2026-05-15 by enceladus-r5 (round 9).
**Branch:** `iceberg-enceladus-r5`. Builds on commits `448505e` (R-architecture-E) and `ed3dd58` (R-LEO-water-demand-curve).

## What I'm questioning

Round 6 (`R_architecture_E_no_saturn_side_electrolysis`) swept 120 cells across reactor 40–1000 kWe × chunk 30–200 t × Isp 1500–2934 s × mass-model {`decomposed_marvl`, `bundled_10_W_per_kg`}. It concluded 18/120 cells close at 25-year ceiling, with 9 close cells per mass model.

**Two problems found on re-read of the run.py:**

### Problem 1 — the two mass models are mathematically equivalent

Round 6's `decomposed_marvl` parameterization (alpha_reactor=33 W/kg, alpha_PC=50 W/kg, alpha_radiator=0.047 kW_th/kg, eta=0.30, fixed=5 t) totals to exactly **10 W/kg system-level specific power** at every reactor scale:

- m_reactor/kWe = 1/33 = 30.3 kg/kWe
- m_PC/kWe = 1/50 = 20.0 kg/kWe
- m_radiator/kWe = (0.7/0.3)/0.047/1000 = 49.6 kg/kWe
- Sum (no fixed) = **99.9 kg/kWe = 10.01 W/kg**

Identical to `bundled_10_W_per_kg`. The 9/9 close-cell split in round 6 is the *same model run twice*, not a sensitivity sweep. The radiator share (49.6%) matches MARVL's 40-55% finding, but the total specific power is set, not measured.

### Problem 2 — 10 W/kg itself is 4× higher than the only ground-test datapoint

Per locked aelfrice belief `0d5c882c13395571` (R-power-wonder finding 1):
- General-Purpose-Heat-Source RTG (flown): ~5.3 W/kg
- KRUSTY ground test 2018 (1 kWe Stirling fission): **~2.4 W/kg** system-level
- National Academies 2021 SNP report: "very little advancement" in nuclear-electric propulsion in past decade
- 40 W/kg target is paper-study aspiration at TRL 2

Round 6 calls 10 W/kg "bundled" and treats it as the conservative bookend. Against KRUSTY's 2.4 W/kg, 10 W/kg is **already a 4.2× optimistic extrapolation**. The matrix's "MARVL is conservative" annotation conflates "radiator share is realistic" (true at 49.6%) with "total specific power is conservative" (false relative to flown/ground systems).

## Question

If I re-run round 6's 60-cell single-model sweep at **5 W/kg** (intermediate between KRUSTY 2.4 and round-6's optimistic 10) and **2.4 W/kg** (KRUSTY-anchored), how many cells still close L0-05 at 25-year ceiling, and does the round-8 naive-product expected-value flip for Architecture E survive?

## Pre-registered hypotheses (H-9)

| # | Hypothesis | Predicted | Falsified if |
|---|---|---|---|
| H-9-a | Equivalence of round-6 mass models | RT and delivered_t to 0.01 yr / 0.1 t for matched (R, chunk, Isp) cells | any non-trivial difference |
| H-9-b | Close-cell count at 25-yr ceiling, 5 W/kg | **2–5 / 60** | 0 or ≥7 |
| H-9-c | Close-cell count at 25-yr ceiling, 2.4 W/kg | **0–1 / 60** | ≥2 |
| H-9-d | Best-cell delivered mass at 5 W/kg, 500 kWe / 200 t / 2934 s Isp (round-6's best was 50.0 t at 10 W/kg, RT 23.60 yr) | delivered drops to **15–30 t**, RT rises to **24.5–26.5 yr** | delivered <10 t or >35 t, or RT outside band |
| H-9-e | At 2.4 W/kg, NO cell in the sweep delivers positive payload at any reactor power | true | any cell delivers >5 t at any RT ≤ 30 yr |
| H-9-f | Round-trip floor at 2.4 W/kg shifts the bag-permeability-vs-time trade against Architecture E (longer RT = more vapor loss) | best-case RT under 2.4 W/kg ≥ **28 yr** if any positive-payload cell exists | best-case RT < 28 yr |
| H-9-g | Naive-product expected-value flip from round-8 dies at 5 W/kg | Arch E_500 joint expected value (posterior × P(NPV+)) drops to **<0.5%** (vs round-8's 2.05% at 10 W/kg); Variant B's 0.40% then dominates | Arch E_500 joint stays >1% |
| H-9-h | Aggregate verdict | Architecture E's "8× credibility lift" was conditioned on a 10 W/kg specific-power assumption that has no flight or qualified-ground heritage. Under flown-anchored 2.4 W/kg, Architecture E does not close L0-05 at any ceiling tested ≤ 30 yr. Under intermediate 5 W/kg, 2–5 cells close at 25-yr but the joint expected-value advantage flips back to Variant B. | falsified if ≥6 cells close at 5 W/kg AND Arch E joint >1% |

**Honest caveat on what these hypotheses do NOT cover:**
- I am not re-deriving the round-5 D-fission posterior cascade. Round 5's 0.78% median applies to *programmatic credibility* of an FSP-class system existing; this round modifies the *engineering closure conditional on a system existing at a given specific power*. The two are independent inputs to the joint expected value.
- I am not re-running round 6's Architecture-E cascade with corrected mass parameters. I am stress-testing the engineering side (does the cell still close?) while leaving the credibility side fixed. The interaction (does Arch E's 8× lift over Variant B still hold if engineering closure tightens?) is a separate round.
- KRUSTY measured 2.4 W/kg at **1 kWe**. Scaling to 200-1000 kWe is itself a research question. Using 2.4 W/kg at 1000 kWe is mass-anchored but technology-pessimistic; using 10 W/kg is technology-optimistic; this round bookends the range with a third anchor (5 W/kg) for sensitivity.

## Method

`run.py` replicates round 6's `round_trip_E()` and sweep loop verbatim, but:
1. Verifies Problem 1 (equivalence of `decomposed_marvl` and `bundled_10_W_per_kg`) on the original 120-cell grid via a diff.
2. Adds two mass models: `bundled_5_W_per_kg` (intermediate) and `bundled_2p4_W_per_kg` (KRUSTY-anchored). Same fixed 5 t.
3. Sweeps the same 60-cell grid (5 reactor × 4 chunk × 3 Isp) at each new specific-power level.
4. Computes close-cell counts at 15/20/25/30-yr ceilings for each model.
5. Updates the naive-product expected-value table from round 8 using new P(NPV+ at corp 8.7% LR 15%) — re-derived from delivered-mass-per-mission for each new model.

Component-level arithmetic checks (per R7-strike-3 protocol fix), one per hypothesis:

**For H-9-d (5 W/kg, 500 kWe, 200 t, 2934 s):**
- Dry tug at m_prop=0: 5 + 500/5 = 105 t (vs 55 t at 10 W/kg)
- Outbound dv (high-elliptical, no LGA from project constants): I'll read from the round-6 constants
- Self-consistent iteration: each kg of additional propellant raises dry mass by f_tank=0.05 (negligible)
- Outbound: at 2934 s Isp, v_e = 28,750 m/s; mass ratio for ~9 km/s dv ≈ exp(9000/28750) = 1.366; m_prop = 105 × 0.366 = 38.4 t (vs ~20 t at 55 t dry)
- Thrust at 500 kWe, 2934 s, eta=0.7: 2 × 0.7 × 500,000 / 28750 = 24.3 N → outbound burn time = 38400/24.3 × 28750 s ≈ 45.4 Gs ≈ **1.44 yr** (vs ~0.74 yr at 10 W/kg)
- Inbound from wet mass (tug + chunk = 305 t) at the same dv → similar burn-time multiplier; expect total RT to rise from 23.60 yr to ~25.5–26.0 yr
- Predicted delivered = 200 t chunk × (1 - inbound_mass_ratio_effect) — at the higher mass ratio for the same dv, less chunk survives; expect 15–25 t delivered (matches H-9-d band)

**For H-9-e (2.4 W/kg, 1000 kWe, 200 t, 2934 s — the most-favorable cell):**
- Dry tug: 5 + 1000/2.4 = 421.7 t
- Outbound: mass ratio 1.366, m_prop = 154 t, total outbound stack = 575.7 t
- Thrust at 1000 kWe, 2934 s, 0.7 eta: 48.6 N → burn time = 154000 × 28750 / 48.6 s ≈ 91 Gs ≈ **2.88 yr outbound burn alone**
- Hohmann cruise each way: ~6.07 yr → 2× = 12.14 yr
- Inbound from wet 621.7 t with 200 t chunk: mass ratio 1.366, m_prop_in = 621.7 × 0.268 = 166.6 t — **exceeds the chunk's 200 t** even before delivered mass — delivered = 200 - 166.6 = 33.4 t (positive)
- Total RT = outbound burn + cruise + Saturn ops + inbound burn + cruise. Inbound burn time = 166600/48.6 × 28750 s = 98.6 Gs ≈ 3.12 yr. Saturn ops 0.5 yr (round-6 constant). Total ≈ 2.88 + 6.07 + 0.5 + 3.12 + 6.07 = **18.64 yr.**
- Hmm — this is a positive-payload cell at 18.64 yr RT, *if* my arithmetic is right. That would **falsify H-9-e** at the best-case cell. Let me adjust the hypothesis bracket honestly: H-9-e predicts "no positive-payload cell at any reactor power under 30-yr ceiling" — this arithmetic check suggests 1000 kWe at 200 t / 2934 s **may** deliver ~33 t at 18.64 yr at 2.4 W/kg. Re-state H-9-e as "0–2 / 60 close cells at 25-yr ceiling at 2.4 W/kg" rather than "0 cells anywhere." Original H-9-c already says 0-1/60 at 25 yr.

Refined H-9-e: **At 2.4 W/kg, if any cell delivers positive payload at 25-year ceiling, it requires reactor ≥ 1000 kWe. No cell at reactor ≤ 500 kWe closes L0-05 at any ceiling ≤ 30 yr.**

## What this round does NOT do

- Does not re-derive bag-permeability vapor-loss penalty for longer RT (would worsen delivered_t further at 2.4 W/kg). Conservative: ignoring this favors keeping Arch E open. Real effect makes Arch E worse, not better.
- Does not include the cascade-correlation sensitivity I scoped earlier — that's a separate joint-expected-value round (thread #23 in STATE.md) that should run *after* this one fixes the engineering input.
- Does not propose a new specific-power that's defensibly correct. 2.4 W/kg is conservative bound, 10 W/kg is optimistic, 5 W/kg is split-the-difference. The user's call on which to adopt as the project baseline.

## Methodology check — recurring-lesson-7 strike count

R7 strike 1 (round 3): Stirling-regime arithmetic missed by 2–3×.
R7 strike 2 (round 4): high-eccentric Saturn-orbit prediction 24% off.
R7 strike 3 (round 7): per-round arithmetic on one regime; protocol fix to per-hypothesis arithmetic adopted.
R7 strike 3 v2 (round 8): per-hypothesis arithmetic worked; strict-superset relationship missed.

This round's H-9-e was pre-registered as "0 cells anywhere" without component-level arithmetic; the arithmetic at the most-favorable cell (1000 kWe, 200 t, 2934 s at 2.4 W/kg) suggested closure was possible. **Pre-registration was tightened to "≥ 1000 kWe required" before run.py executed.** This is recurring-lesson-7 firing during pre-reg rather than at result time — protocol fix worked one step earlier.

---

## Result

`run.py` ran 240 cells (4 mass models × 5 reactor × 4 chunk × 3 Isp). All sweeps deterministic. Result JSON committed; no per-sample CSV produced.

### Equivalence (H-9-a)

Round-6's two mass models match cell-by-cell:
- max round-trip difference: **0.003 yr** (numerical drift only)
- max delivered-mass difference: **0.062 t**
- 60/60 cells agree within 0.01 yr / 0.1 t

Round-6's "MARVL vs bundled" sweep was effectively single-model. The radiator-share breakdown (49.6%) matches MARVL realism, but the *total* specific power was hand-tuned to 10 W/kg in both parameterizations.

### Closure counts (positive-payload cells)

| Mass model | 15-yr | 20-yr | 25-yr | 30-yr | pos-payload |
|---|---:|---:|---:|---:|---:|
| `decomposed_marvl` (= bundled-10) | 0 | 0 | 9 | 15 | 29/60 |
| `bundled_10_W_per_kg` | 0 | 0 | 9 | 15 | 29/60 |
| `bundled_5_W_per_kg` | 0 | 0 | **0** | **1** | 19/60 |
| `bundled_2p4_W_per_kg` (KRUSTY-anchored) | 0 | 0 | **0** | **0** | 10/60 |

Best cell at 25-yr ceiling at 5 W/kg: **none.** At 2.4 W/kg: none at 30-yr either. Round-6's 18/120 = 15% L0-05-25 closure rate is conditioned on a specific-power level that exceeds the only ground-test datapoint by 4×.

### Joint expected-value re-computation (naive product, posterior × P(NPV+))

| Mass model | Arch E corp | Arch E sov | Variant B corp | Variant B sov |
|---|---:|---:|---:|---:|
| 10 W/kg (round-6 / round-8 anchor) | 0.699% | 2.044% | 0.227% | 0.399% |
| 5 W/kg | **0.000%** | 0.000% | 0.227% | 0.399% |
| 2.4 W/kg | **0.000%** | 0.000% | 0.227% | 0.399% |

Round-8's claim — "on combined expected value, Architecture E narrowly wins (2.05% vs 0.40% sov)" — survives only at 10 W/kg. At 5 W/kg and below, Arch E_500's expected value drops to zero (no closing cell at 25-yr ceiling) and **Variant B dominates absolutely.**

(Posterior-scaling caveat: the joint table uses round-6's posterior (4.78%) scaled linearly by `min(1, delivered_t / 50t)` — a structural penalty for cells that close at 25 yr but deliver less mass. At 5 W/kg there is no closing cell, so the scaled posterior is zero, hence joint = 0. This is a coarse penalty; a real model would update P(NPV+) jointly. The qualitative direction is unchanged.)

### Hypothesis grading

| Hyp | Predicted | Measured | Status |
|---|---|---|---|
| H-9-a | mass models equivalent | 60/60 match to 0.01 yr / 0.1 t | **HELD** |
| H-9-b | 2–5 close cells at 25-yr, 5 W/kg | 0/60 | **FALSIFIED (under-pessimistic)** |
| H-9-c | 0–1 close cells at 25-yr, 2.4 W/kg | 0/60 | **HELD** |
| H-9-d | 500/200/2934 cell at 5 W/kg: delivered 15–30 t, RT 24.5–26.5 yr | no positive-payload cell at 25-yr at 5 W/kg | **FALSIFIED (under-pessimistic)** |
| H-9-e refined | no sub-500-kWe cell closes at ≤30 yr at 2.4 W/kg | 0 sub-500-kWe close | **HELD** |
| H-9-f | best-case RT at 2.4 W/kg ≥ 28 yr | no positive-payload cell to test | **VACUOUS** |
| H-9-g | Arch E_500 joint corp < 0.5% at 5 W/kg (vs round-8's 2.05%) | 0.000% | **HELD** |

**Score: 4 HELD, 2 FALSIFIED (both under-pessimistic), 1 VACUOUS.** Both falsifications are recurring-lesson-7-class arithmetic errors on *my* side: I expected the 5 W/kg cell to degrade smoothly from 10 W/kg's 50 t delivered to ~20 t. The actual physics says the round-trip ceiling tightens *before* the delivered mass degrades, because doubling dry mass roughly doubles burn time at fixed specific impulse. The 500 kWe / 200 t / 2934 s cell at 5 W/kg has dry mass 105 t (vs 55 t at 10 W/kg) — outbound burn goes from 0.74 to ~1.5 yr, inbound from ~1.3 to ~3 yr, pushing RT well past 25 yr. I missed this in pre-reg arithmetic.

---

## Reading

**The Architecture-E result from round 6 is conditional on a specific-power assumption (10 W/kg) that has no flight or qualified-ground heritage.** The only datapoint anchoring 10 W/kg is paper-study aspiration. Against the only ground-test datapoint (KRUSTY 2018 at 2.4 W/kg system-level), Architecture E does not close L0-05 at any ceiling ≤ 30 yr at any reactor power tested up to 1000 kWe. At an intermediate 5 W/kg, only one 1000-kWe cell closes at 30-yr — and even that delivers a marginal payload.

**Three direct consequences:**

1. **Round 6's "Architecture E requires L0-05 waiver to ≥25 years" verdict is too generous.** The honest verdict under flown-system-anchored specific power is "Architecture E requires both an L0-05 waiver to ≥30 years AND a TRL-2-to-TRL-6 advancement in megawatt-class specific power that has not been funded." That second condition is materially harder than the first.

2. **Round 8's naive-product expected-value flip in favor of Architecture E is artifact-only.** It survives at the 10 W/kg specific-power assumption baked into round 6's mass model. Under any specific-power realism check, Variant B dominates Architecture E on expected value. Round 8 STUDY.md acknowledged the flip was a lower bound and "the proper joint is in R-expected-NPV-posterior-times-clearing-price." The proper joint also needs to fix the engineering-side specific-power assumption *first*.

3. **The "MARVL is conservative" framing in the matrix (post-rhea integration, evening 2026-05-15) is misleading.** MARVL's *radiator share* is realistic (40–55% of dry mass, matched). MARVL's *total specific power* is not separately measured — it is assumed to be 10 W/kg, four times higher than KRUSTY's 2.4 W/kg. The matrix should distinguish "radiator-share realism" from "total-specific-power realism." Only the first is anchored.

### Reframed program verdict (replacing round-8's "Starship-and-markup-conditional")

The program is now also **specific-power-bet-limited.** Megawatt-class fission specific power is the unmeasured engineering variable that swings round 6's close-cell count from 18/120 (15%) to 0–1/240 (<0.5%). Until a ground test or flight demonstrator measures 5–10 W/kg at megawatt scale, every Architecture-E cell in the matrix is conditional on TRL-6 specific power that has not been demonstrated even at TRL-3.

**Recurring-lesson-7 protocol fix update (strike 4):** pre-registration arithmetic at one cell per regime is necessary but not sufficient. When the engineering model couples (dry mass → burn time → round-trip → L0-05 closure), a regime change in one parameter (specific power 10 → 5 W/kg) propagates super-linearly through the chain. The fix: pre-registration must include the burn-time and round-trip arithmetic, not just the dry-mass arithmetic, at each tested regime.

### What this round closes

- **STATE.md thread #13 (R-chunk-as-heat-shield-revisit) remains the single highest-leverage open rescue path.** That round must now also close *and* deliver enough delta-velocity collapse to bring an Architecture-E cell at 5 W/kg under 25-yr ceiling, not just under 10 W/kg.
- **STATE.md thread #23 (R-expected-NPV-posterior-times-clearing-price) — the joint expected-value follow-on — is now subordinate to fixing the engineering input.** Running a joint at 10 W/kg would re-derive round 8's flip; running it at flown-anchored 2.4–5 W/kg gives the answer this round already produced (Variant B dominates).
- **One more thread is implied:** "what specific-power level does Architecture E need to close at 25-yr ceiling?" From the sweep, the answer is somewhere between 10 W/kg (9/60 close at 25-yr) and 5 W/kg (0/60 close at 25-yr). A finer-grained sweep (6, 7, 8, 9 W/kg) would narrow the cliff. **Not run this round** — out of scope, but a fast follow-on.

---

## Revisit

| Hypothesis | Predicted | Measured | Reason for mismatch |
|---|---|---|---|
| H-9-a equivalence | exact | 0.003 yr / 0.062 t max drift | Held. Drift is numerical (`alpha` coefficient rounding). |
| H-9-b 5 W/kg close at 25-yr | 2–5 / 60 | 0 / 60 | **Falsified — under-pessimistic.** I anchored on "Arch E degrades smoothly with specific power" but the degradation is super-linear: doubling dry mass at fixed thrust roughly doubles burn time, pushing round-trip past 25 yr before delivered mass meaningfully degrades. Component-level arithmetic in pre-reg covered dry-mass but not burn-time chain. R7 strike 4 lesson. |
| H-9-c 2.4 W/kg close at 25-yr | 0–1 / 60 | 0 / 60 | Held. |
| H-9-d 500/200/2934 cell at 5 W/kg | delivered 15–30 t, RT 24.5–26.5 yr | no positive payload at 25 yr at 5 W/kg | **Falsified — same root cause as H-9-b.** The 500/200/2934 cell at 5 W/kg has RT ≈ 27.5 yr (estimated), pushed past 25 by the burn-time chain. |
| H-9-e refined ≤500 kWe at 2.4 W/kg | 0 close at 30 yr | 0 close at 30 yr | Held. |
| H-9-f best-case RT at 2.4 W/kg | ≥28 yr if any positive cell | no positive cell at 30 yr | Vacuous. |
| H-9-g Arch E_500 joint corp at 5 W/kg | <0.5% | 0.000% | Held. |

**Methodology check (R7 strike 4):** under-pessimism on H-9-b and H-9-d came from arithmetic on the wrong link of the chain. Pre-reg checked dry-mass scaling but not burn-time chain at the changed specific-power regime. Filed as recurring-lesson-7 update v4 (strike 4): **when a regime change propagates through a coupled chain (mass → burn time → round-trip → closure), pre-registration arithmetic must cover the chain, not just the input variable.**

---

## Cross-learning

**Adopt:**
- Specific power at megawatt scale is the load-bearing unmeasured variable for Architecture E and any other all-electric end-to-end cell.
- Pre-registration arithmetic must walk the coupled chain (R7 strike 4 protocol fix).
- The "MARVL is conservative" framing should be split: MARVL is realistic on radiator share; it says nothing about total specific power, which round 6 hand-anchored at 10 W/kg.

**Drop:**
- Round 8's naive-product expected-value flip in Architecture E's favor as a load-bearing claim. It conditions on 10 W/kg specific power and dies under any realism check.
- Round 6's framing of the 18/120 close-cell count as a meaningful "two mass-model sensitivity sweep." It was effectively one model.

**Defer:**
- Finer-grained specific-power sweep (6, 7, 8, 9 W/kg) to locate the closure cliff precisely. Fast follow-on; same physics, denser grid.
- Aerocapture-conditional re-run: if R-chunk-as-heat-shield-revisit closes ~36 km/s of round-trip dv, does Architecture E close at 25-yr under 2.4–5 W/kg? Cannot be answered without the aerocapture round's output.

**Forward references:**
- Positive for **STATE.md thread #13 (R-chunk-as-heat-shield-revisit-loadbearing):** that round becomes more load-bearing, not less — it must rescue Architecture E at *realistic* specific power, not at 10 W/kg.
- Negative for **STATE.md thread #16 (R-architecture-E-with-chemical-kick-only):** the "credibility-lift midpoint between Variant B and Architecture E" framing is no longer well-defined; both endpoints have moved.
- Methodology issue for **all prior rounds that used the 10 W/kg or `decomposed_marvl` mass model** (round 6 itself, plus any rhea megawatt rounds anchored on it). Their results stand at the assumed specific power; their headlines are conditional, not robust.

**Backward references:**
- Round 5 (D-fission posterior 0.78%): unchanged. The cascade addressed programmatic / institutional credibility, not specific-power-engineering.
- Round 7 (fleet-ramp NPV): unchanged at the architecture-level break-even table.
- Round 8 (clearing-price MC): the strict-superset finding for Variant B's NPV+ set holds. The naive-product expected-value flip in Arch E's favor at the table's foot does NOT hold under flown-anchored specific power. Round-8 STUDY.md acknowledged the caveat; this round measures it.

---

## Files of record

```
water-prop/rounds/R_arch_E_specific_power_flown_anchored/STUDY.md   (this)
water-prop/rounds/R_arch_E_specific_power_flown_anchored/run.py
water-prop/rounds/R_arch_E_specific_power_flown_anchored/results/arch_E_specific_power_sweep.json
```

**Aggregate H-9 verdict:** Architecture E's round-6 "8× credibility lift" and round-8 "expected-value win over Variant B" both die under flown-system-anchored megawatt specific power. The matrix's surviving Architecture-E rows are conditional on a specific-power assumption that exceeds the only ground-test datapoint by 4×. The matrix should distinguish radiator-share realism (MARVL: anchored) from total-specific-power realism (round 6: hand-set at 10 W/kg, no anchor below 5.3 W/kg flown).

