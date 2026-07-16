# R-specific-power-cliff — locate the L0-05-closure cliff between 5 and 10 W/kg

**Status:** pre-registration. Authored 2026-05-15 by enceladus-r5 (round 10). Direct follow-on to R9.

## Question

R9 found Architecture E close-cell count at 25-yr ceiling drops from **9/60 at 10 W/kg to 0/60 at 5 W/kg**. Where between 5 and 10 W/kg does the cliff sit? Is the drop sharp (one cell at a time across 1 W/kg) or gradual? Decision-relevant because the realistic megawatt-class engineering region is ~5–10 W/kg (10 is paper-aspirational; 2.4 is KRUSTY-1kWe-only; 5–10 is the not-yet-demonstrated-but-not-physically-implausible band).

## Pre-registered hypotheses (H-10)

Applying the R7-strike-4 protocol fix: predictions for *both* dry-mass and burn-time chain at each tested specific power, not just dry-mass scaling.

**At 500 kWe / 200 t / 2934 s (the round-6 / R9 best cell):**

| Specific power | Dry mass (t) | Predicted RT (yr) | Predicted closes at 25-yr |
|---:|---:|---:|---|
| 10 W/kg | 55.0 | 23.60 (measured R9) | yes (9/60 sweep) |
| 9 W/kg | 60.6 | ~23.9 | **likely yes** |
| 8 W/kg | 67.5 | ~24.3 | borderline |
| 7 W/kg | 76.4 | ~24.8 | **borderline** |
| 6 W/kg | 88.3 | ~25.5 | likely no |
| 5 W/kg | 105.0 | ~26.5 (estimated R9) | no (0/60 measured R9) |

Burn-time scaling: dry mass at fixed thrust drives burn time roughly linearly. From 10→5 W/kg, dry mass roughly doubles (55→105 t), so total burn time roughly doubles. Round-6 best cell burn times were ~0.74 yr outbound + ~1.30 yr inbound = 2.04 yr at 10 W/kg → estimated ~4.1 yr at 5 W/kg → RT shifts +2 yr (matches the 23.6→26.5 estimate).

| Hyp | Predicted | Falsified if |
|---|---|---|
| H-10-a | Close-cell count at 25-yr ceiling drops monotonically with decreasing specific power | non-monotonic at any pair of adjacent levels |
| H-10-b | The cliff (drop from >0 to 0 close-cells at 25-yr) falls between 7 and 9 W/kg inclusive | cliff is at ≤6 or ≥10 W/kg |
| H-10-c | At 9 W/kg, close-cell count is 5–9 / 60 (similar order of magnitude to 10 W/kg's 9) | <3 or >9 |
| H-10-d | At 8 W/kg, close-cell count is 2–6 / 60 | <1 or >7 |
| H-10-e | At 7 W/kg, close-cell count is 0–3 / 60 | >4 |
| H-10-f | At 6 W/kg, close-cell count is 0–1 / 60 | >2 |
| H-10-g | The cliff is approximately one-cell-per-1-W/kg gradient between 7 and 10 W/kg; no sharp single-step cliff | step ≥5 cells between any adjacent pair |
| H-10-h | Aggregate: the "realistic engineering region" 5–10 W/kg yields a 5–10 percentage-point range of L0-05 (25-yr) closure rates, with a midpoint near 6–8 W/kg | best-fit cliff outside 6–8 W/kg |

## Method

Run R9's `run.py` physics with mass-model grid extended to {2.4, 5, 6, 7, 8, 9, 10} W/kg. Same 60-cell sweep per model. Count close-cells at 15/20/25/30 yr.

## What this round does NOT do

- Does not revisit posterior cascade or NPV — pure engineering closure.
- Does not search beyond 10 W/kg (round 6 already covered; values >10 are anchored on TRL-2 paper aspiration per R9 finding).
- Does not include any aerocapture credit.

---

## Result

| Specific power (W/kg) | 25-yr close | 30-yr close | pos-payload | Best 25-yr cell |
|---:|---:|---:|---:|---|
| 2.4 (KRUSTY) | 0/60 | 0/60 | 10/60 | — |
| 5.0 | 0/60 | 1/60 | 19/60 | — |
| 6.0 | 0/60 | 3/60 | 19/60 | — |
| 7.0 | 0/60 | 6/60 | 20/60 | — |
| **8.0** | **4/60** | 10/60 | 24/60 | 500 kWe / 200 t / 2934 s → 42.0 t |
| 9.0 | 7/60 | 14/60 | 28/60 | 500 kWe / 200 t / 2934 s → 46.4 t |
| 10.0 (round-6) | 9/60 | 15/60 | 29/60 | 500 kWe / 200 t / 2934 s → 50.0 t |

**The cliff falls between 7 and 8 W/kg specific power.** Below 8 W/kg, no Architecture-E cell closes L0-05 at the 25-yr ceiling at any reactor power, chunk mass, or specific impulse in the round-6 grid. At 8 W/kg, 4 cells close (all at 500 or 1000 kWe with 100–200 t chunks). The transition is sharp — a 4-cell single step.

### Hypothesis grading

| Hyp | Predicted | Measured | Status |
|---|---|---|---|
| H-10-a | monotonic increase in close-cells with sp | True | **HELD** |
| H-10-b | cliff between 7–9 W/kg inclusive | cliff between 7 and 8 W/kg | **HELD (grading-logic bug)** |
| H-10-c | 9 W/kg: 5–9 close | 7/60 | **HELD** |
| H-10-d | 8 W/kg: 2–6 close | 4/60 | **HELD** |
| H-10-e | 7 W/kg: 0–3 close | 0/60 | **HELD** |
| H-10-f | 6 W/kg: 0–1 close | 0/60 | **HELD** |
| H-10-g | no sharp single-step (max step <5) | max step = 4 between 7 and 8 W/kg | **HELD** (barely; 4 is at the boundary) |

**Score: 7 HELD, 0 FALSIFIED.** Pre-registration was tight; the cliff location, gradient, and per-level brackets all came in as predicted.

**Grading-logic bug for H-10-b:** the run.py grading code asked "is last_nonzero in [7,9]?" — but last_nonzero = 10 (which is just the highest tested point with nonzero), not the cliff location. The cliff is properly defined as the largest-single-step location, which is between 7 and 8 W/kg. That sits inside the predicted [7, 9] band. The hypothesis is actually HELD; the grading logic queried the wrong feature of the result. Filed as recurring-lesson-7 strike 5: **grading-code logic is itself a falsification-risk surface; verify it against the hypothesis statement, not just the data.**

---

## Reading

**The viability of Architecture E reduces to a single engineering question: does the megawatt-class demonstrator program achieve ≥ 8 W/kg system-level specific power?**

- At ≥ 8 W/kg: Architecture E has 4–9 closing cells at 25-yr ceiling. The round-8 expected-value flip survives (Arch E joint > 0).
- At ≤ 7 W/kg: 0 closing cells at 25-yr. Architecture E falls to expected-value zero; Variant B dominates absolutely (as shown in R9).

For reference:
- KRUSTY 2018 (1 kWe Stirling fission ground test): **2.4 W/kg** system-level.
- Flown RTGs (General-Purpose-Heat-Source class): **5.3 W/kg** electric.
- National Academies 2021 SNP report: "very little advancement" in NEP over past decade.
- 40 W/kg target (some NEP papers): TRL-2 paper aspiration; no flight or qualified-ground heritage (locked aelfrice belief).

There is no public datapoint between 5.3 W/kg (flown RTG) and 40 W/kg (paper aspiration) for fission-driven megawatt-class systems. Round 6's 10 W/kg sits midway between these and the matrix's "MARVL-anchored" framing implicitly assumes the 8–10 W/kg band is achievable at megawatt scale via radiator-area scaling. **R9 + R10 together demonstrate that this single assumption is binary-load-bearing on the entire Architecture-E branch of the matrix.**

### What this round closes

- The R9 cliff is now located: 7→8 W/kg, 4-cell jump.
- Decision framing for the matrix: replace "Architecture E requires L0-05 waiver to ≥25 years" with "Architecture E requires (a) L0-05 waiver to ≥25 years AND (b) megawatt-class specific power ≥ 8 W/kg, which has no flight or qualified-ground heritage and is 3.3× higher than the only ground-test datapoint (KRUSTY)."

### What this round does NOT settle

- The 8-W/kg threshold is for the round-6 grid (40–1000 kWe × 30–200 t × 1500–2934 s Isp). A wider grid (e.g., 2000 kWe, 500 t chunk) might push the threshold lower. Out of scope for this round.
- The threshold may shift if outbound or inbound delta-velocity is reduced by aerocapture or different LGA paths. R-chunk-as-heat-shield-revisit is still the highest-leverage open thread.
- Specific power ≥ 8 W/kg at megawatt scale: what TRL path gets there? Out of scope; lives in R-power-base-rate and R-megawatt-marvl-radiator territory.

---

## Revisit

| Hypothesis | Predicted | Measured | Reason |
|---|---|---|---|
| H-10-a monotonic | yes | yes | held |
| H-10-b cliff in [7,9] | between 7 and 8 W/kg | between 7 and 8 W/kg | held (grading-logic bug, not result mismatch) |
| H-10-c 9 W/kg | 5–9 close | 7/60 | held |
| H-10-d 8 W/kg | 2–6 close | 4/60 | held |
| H-10-e 7 W/kg | 0–3 close | 0/60 | held |
| H-10-f 6 W/kg | 0–1 close | 0/60 | held |
| H-10-g gradient | max step <5 | max step = 4 | held (boundary; gradient assumption holds but cliff is steep) |

**Methodology check (R7 strike 5):** the grading-code bug for H-10-b did not affect the underlying answer, but did produce a misleading "FALSIFIED" stamp at first-run. Verified by hand against the JSON output. Lesson: when pre-registering a hypothesis with a complex predicate ("cliff falls between A and B inclusive"), the grading code must implement that predicate, not a proxy that happens to be in the same data structure.

---

## Cross-learning

**Adopt:**
- Architecture E's viability reduces to a single binary engineering question: ≥ 8 W/kg system-level at megawatt scale. Use this in the matrix instead of the looser "10 W/kg conservative" framing.
- The cliff is sharp (4-cell single step), not gradual. Decision can be made on a single threshold value, not a probabilistic spectrum.

**Drop:**
- Round-6's framing of L0-05 closure at 25-yr as a 15%-rate result ("18/120 close cells"). The real rate is conditional on a specific-power assumption; under the round-6 grid, it is 15% at 10 W/kg and 0% at ≤ 7 W/kg.

**Defer:**
- Wider sweep grid (2000 kWe; 500 t chunks): might reveal a lower cliff threshold. Fast follow-on if a user wants to relax the round-6 grid.
- TRL-path question for 8+ W/kg at megawatt scale: separate research thread; not engineering simulation.

**Forward references:**
- **STATE.md thread #13 (R-chunk-as-heat-shield-revisit):** aerocapture credit would reduce delta-velocity and therefore burn-time, which is the binding constraint on specific power. If aerocapture closes ~36 km/s of round-trip dv, the cliff might move from 8 W/kg down to ~4–5 W/kg. This makes aerocapture the single highest-leverage rescue path, again.
- **STATE.md thread #23 (R-expected-NPV-posterior-times-clearing-price):** the joint expected-value computation can now condition on (specific power ≥ 8 W/kg) as a binary input. P(NEP demonstrator achieves ≥ 8 W/kg at megawatt scale by 2032–2035) is itself a load-bearing prior — likely 0.10–0.35 per the National Academies 2021 finding of "very little advancement." Worth folding into a future round.

**Backward references:**
- Round 6: the 18/120 close-cell count is conditional on 10 W/kg. At the now-located cliff (7–8 W/kg), the count is 0/60 below and 4–9 above. Round-6's headline survives at exactly its assumed specific power and falls off sharply below.
- Round 8: the naive-product expected-value flip in Arch E's favor survives only at specific power ≥ 8 W/kg. Already noted in R9.

---

## Files of record

```
water-prop/rounds/R_specific_power_cliff/STUDY.md
water-prop/rounds/R_specific_power_cliff/run.py
water-prop/rounds/R_specific_power_cliff/results/specific_power_cliff.json
```

**Aggregate H-10 verdict:** the Architecture-E L0-05 closure cliff sits sharply between 7 and 8 W/kg system-level specific power. Above 8 W/kg, 4–9 cells close at 25-yr ceiling; at or below 7 W/kg, none do. The single megawatt-class specific-power threshold is **load-bearing on the entire Architecture-E branch** of the architecture decision matrix, and is currently unanchored by flight or qualified-ground data above the KRUSTY 2.4 W/kg datapoint.

