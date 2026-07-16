# R-aerocapture-cliff-shift — how much aerocapture credit moves the specific-power cliff?

**Status:** pre-registration. Authored 2026-05-15 by enceladus-r5 (round 11). Direct follow-on to R10.

## Question

R10 located the Architecture-E L0-05-25 closure cliff at 7–8 W/kg system-level specific power. The matrix annotation on R-chunk-as-heat-shield-revisit (the year-20+ aerocapture-conditional row) says "Earth-side ~36 km/s of round-trip delta-velocity collapses to aerodynamic passes." That number is aggressive — it would require both outbound AND inbound aerocapture credit (or perhaps Saturn-arrival aerobraking too).

**Without claiming any specific aerocapture credit is achievable**, this round maps the parameter space:

- At what aerocapture inbound dv credit X km/s does the cliff move from 8 W/kg down to 5.3 W/kg (flown-RTG anchor)?
- At what X does it move to 2.4 W/kg (KRUSTY ground-test anchor)?
- Does the matrix's "~36 km/s" claim land the cliff below 2.4 W/kg, or is it still above?

The chunk-as-heat-shield people get a quantitative target from this round: "to make Architecture E viable at flown-anchored specific power, deliver X km/s of aerocapture inbound dv credit."

## Modeling choice

Aerocapture credits the **inbound** leg only. The chunk-as-heat-shield idea is that the chunk (200 t of water) serves as the ablative heat shield for the tug+chunk stack arriving at Earth. Outbound, the spacecraft departs LEO with no atmosphere to brake against; that part of the trajectory cannot be aero-replaced. Saturn-arrival aerobraking is a separate question (Titan has a thick atmosphere, but the chunk must come from the rings, not from a Titan approach) — out of scope.

I reduce the inbound continuous-thrust dv from R6's `DV_INBOUND_TITAN_HE_LGA_KM_S = 24.7 km/s` by X ∈ {0, 5, 10, 15, 20, 25} km/s. At X = 24.7, inbound dv = 0 (full aerocapture). This is a *parametric sweep*, not a physics claim.

## Pre-registered hypotheses (H-11)

| # | Hypothesis | Predicted | Falsified if |
|---|---|---|---|
| H-11-a | The cliff is monotonic in X: as aerocapture credit increases, the minimum specific power for ≥1 close-25-yr cell decreases | true | non-monotonic at any pair |
| H-11-b | The relationship between X and minimum-specific-power-for-closure is approximately linear with slope d(sp_min)/d(X) ≈ **−0.20 to −0.35 W/kg per km/s** | slope in [−0.35, −0.20] | slope outside [−0.4, −0.15] |
| H-11-c | To push cliff to ≤ 5.3 W/kg (flown-RTG anchor), required X ∈ **[7, 15] km/s** | in range | outside range |
| H-11-d | To push cliff to ≤ 2.4 W/kg (KRUSTY anchor), required X ∈ **[15, 25] km/s** | in range | outside range OR achievable at X ≤ 25 (interpretation: hypothesis covers achievability) |
| H-11-e | At X = 24.7 km/s (full inbound aerocapture, inbound continuous-thrust dv = 0), there exists ≥ 1 close-25-yr cell at **all** tested specific powers down to 2.4 W/kg | true at 2.4 W/kg under X = 24.7 | falsified if no cell closes at any sp at X=24.7 |
| H-11-f | The matrix's "~36 km/s round-trip collapse" claim cannot be tested by this round (only inbound modeled); inbound credit of 24.7 km/s is the maximum testable from R6's grid | structural — out of scope | n/a |
| H-11-g | Round-trip time at the new closing cells under aerocapture credit shortens by approximately t_inbound_burn × (1 − X/24.7) at fixed reactor and Isp — i.e. roughly proportional to burn-time reduction; predicted RT delta at X = 10 km/s, 500 kWe / 200 t / 2934 s / 5 W/kg: **−0.8 to −1.4 yr** vs no-aerocapture baseline | in range | outside range |

**Honest caveats:**
- This round does NOT model the heat-load constraint on chunk-as-heat-shield. The chunk is 200 t of frozen water; ablating water into vapor at Earth-entry energies might consume some chunk mass. Not modeled here. **If chunk-as-heat-shield is feasible, this round gives the parametric trade space.**
- I do not include the *outbound* aerocapture share of the "36 km/s" claim. To match that fully would require modeling outbound Earth-escape aerocapture, which I don't have time for in this round.
- The R7-strike-4 chain-arithmetic protocol applies: I will pre-compute the burn-time chain at one cell per regime before grading H-11-g.

### Component-level pre-check at 500 kWe / 200 t / 2934 s / 5 W/kg, X = 10 km/s

- Dry tug at 5 W/kg, 500 kWe = 5 + 100 = 105 t (R9 baseline)
- Inbound dv = 24.7 − 10 = 14.7 km/s
- Inbound v_e = 2934 × 9.81 = 28,793 m/s
- Inbound mass ratio at chunk-as-propellant = exp(14700/28793) = 1.667
- Inbound m_prop = (105 + 200) × (1 − 1/1.667) = 305 × 0.400 = 122 t
- Delivered = 200 − 122 = **78 t** (vs 50 t at X=0, 10 W/kg — improves!)
- Inbound burn time = 122 × 1000 × 28793 / (2 × 0.65 × 500000 / 28793) = 122000 × 28793 / 22.6 N = 1.55 × 10^8 s = 4.93 yr
- Outbound at 5 W/kg / 500 kWe / 2934 s: dry 105 t, outbound dv 29.56 km/s → m_prop = 105 × (exp(29560/28793) − 1) = 105 × (2.802 − 1) = 189 t; thrust 22.6 N; outbound burn = 189000 × 28793 / 22.6 = 2.4 × 10^8 s = 7.63 yr
- Cruise 2× 6.07 yr + Saturn ops 1 yr = 13.14 yr
- **Total RT = 7.63 + 6.07 + 1 + 4.93 + 6.07 = 25.7 yr** (still over 25-yr ceiling!)
- Delivered 78 t at RT 25.7 yr — close but does not close at 25-yr.

So at X = 10 km/s, 5 W/kg, even the best cell may not close at 25-yr. The cliff at X = 10 might still sit above 5 W/kg. Hypothesis H-11-c (cliff ≤ 5.3 W/kg requires X ∈ [7, 15]) is going to be **tested in real arithmetic** by this calculation. Let me check at X = 15 km/s:

- Inbound dv = 9.7 km/s → mass ratio = exp(9700/28793) = 1.404; inbound m_prop = 305 × 0.288 = 87.8 t; delivered = 200 − 87.8 = 112 t
- Inbound burn = 87800 × 28793 / 22.6 = 1.12 × 10^8 s = 3.55 yr
- **Total RT = 7.63 + 6.07 + 1 + 3.55 + 6.07 = 24.3 yr** ← closes at 25-yr ceiling, delivered 112 t.

So at X = 15 km/s, 5 W/kg, 500 kWe, 200 t chunk, 2934 s Isp: cliff is below 5 W/kg. H-11-c (range [7, 15] for 5.3 W/kg cliff) is plausible; this arithmetic suggests the X-for-5.3-W/kg cliff is probably between 10 and 15 km/s.

Re-state H-11-c with tightened brackets given this pre-check: **cliff at ≤ 5.3 W/kg requires X ∈ [10, 15] km/s**.

## Method

Sweep R6 grid (60 cells per specific-power level) over:
- Specific powers: {2.4, 5, 6, 7, 8, 9, 10} W/kg (R10's set)
- Aerocapture inbound dv credit X: {0, 5, 10, 15, 20, 25} km/s

At each (sp, X) combo, count close-25 cells. Map cliff location (lowest sp with ≥1 close-25 cell) at each X.

## What this round does NOT do

- Does not model heat-load constraint on chunk-mass loss during aerocapture.
- Does not model outbound aerocapture share.
- Does not model bag-permeability vapor loss during longer cruises (would worsen results at high X, slightly).
- Does not re-derive posterior or NPV — pure engineering closure with one new parameter.

---

## Result

### Close-25-yr cell count grid

| sp \\ X (km/s) | 0 | 5 | 10 | 15 | 20 | 25 |
|---:|---:|---:|---:|---:|---:|---:|
| 2.4 | 0 | 0 | 0 | 0 | 0 | 0 |
| 5.0 | 0 | 0 | 3 | 11 | 25 | 44 |
| 6.0 | 0 | 3 | 8 | 19 | 36 | 56 |
| 7.0 | 0 | 6 | 13 | 25 | 41 | 56 |
| 8.0 | 4 | 7 | 20 | 29 | 42 | 56 |
| 9.0 | 7 | 10 | 21 | 32 | 44 | 56 |
| 10.0 | 9 | 11 | 23 | 34 | 44 | 60 |

### Cliff location (lowest specific power with ≥1 close-25 cell) at each aerocapture credit

| X (km/s) | min specific power (W/kg) |
|---:|---:|
| 0 | 8.0 (R10 baseline) |
| 5 | 6.0 |
| 10 | 5.0 |
| 15 | 5.0 |
| 20 | 5.0 |
| 25 | 5.0 |

**The cliff drops sharply from 8 → 6 → 5 W/kg over X = 0–10 km/s, then plateaus at 5 W/kg from X ≥ 10 onward.** No aerocapture credit in the tested range (up to 25 km/s, near-full inbound) brings the cliff down to KRUSTY's 2.4 W/kg.

### Hypothesis grading

| Hyp | Predicted | Measured | Status |
|---|---|---|---|
| H-11-a monotonic | non-increasing | [8, 6, 5, 5, 5, 5] | **HELD** |
| H-11-b slope | linear, slope in [-0.35, -0.20] | slope = -0.103 (plateau-shaped) | **FALSIFIED** (framing error) |
| H-11-c cliff to 5.3 W/kg | X ∈ [10, 15] km/s | X = 10 km/s | **HELD** |
| H-11-d cliff to 2.4 W/kg | X ∈ [15, 25] km/s | never reached at X ≤ 25 | **FALSIFIED** |
| H-11-e full aerocapture at 2.4 W/kg | ≥1 close cell | 0 close | **FALSIFIED** |
| H-11-g RT delta | [-1.4, -0.8] yr | -2.24 yr | **FALSIFIED** (pre-reg arithmetic off) |

**Score: 2 HELD, 4 FALSIFIED.** Both the framing of H-11-b (assumed linear over a plateau region) and H-11-d/e (assumed inbound aerocapture alone was sufficient at KRUSTY-scale specific power) were wrong in important and informative ways.

---

## Reading

**The matrix's "Megawatt + chunk-as-heat-shield rescue" footnote is partially validated and partially refuted by this round.**

**Validated:** at intermediate specific powers (5–8 W/kg), aerocapture credit X ∈ [5, 15] km/s rescues Architecture E from "0 close cells at 25-yr" to "11–34 close cells at 25-yr." A modest 10 km/s of inbound aerocapture credit moves the cliff from 8 W/kg down to 5 W/kg — a 3-W/kg reduction in the unmeasured engineering threshold.

**Refuted:** at KRUSTY-anchored 2.4 W/kg specific power, **no amount of inbound aerocapture credit (up to 25 km/s, near-full)** brings any cell to L0-05-25 closure. The bottleneck at very low specific power is the **outbound** burn time, not the inbound. At 2.4 W/kg, 500 kWe gives dry mass 5 + 500/2.4 = 213 t; at 1000 kWe, dry mass = 421.7 t. Outbound continuous-thrust burn at 29.56 km/s on those dry masses is years long — eating the 25-yr budget before inbound aerocapture saves anything.

**The cliff plateau at 5 W/kg from X ≥ 10 km/s** is partly a grid artifact (I didn't test specific powers between 2.4 and 5 W/kg). A finer grid {2.4, 3, 3.5, 4, 4.5, 5} would resolve whether the curve continues to drop slowly or hits a hard floor. Either way, the qualitative finding holds: **flown-system-anchored specific powers near KRUSTY are not rescuable by inbound-only aerocapture.**

### Decision-relevant framing for thread #13 (R-chunk-as-heat-shield-revisit)

- **Aerocapture target inbound dv credit X ≈ 10 km/s** is the minimum useful value: it moves the closure threshold from 8 W/kg down to 5 W/kg, bringing Architecture E within reach of plausible-megawatt (but still TRL-uncertain) specific powers.
- **Aerocapture target X ≈ 25 km/s** is the upper useful value for inbound-only: it opens 44–60 cells per specific-power level above 5 W/kg, but does NOT open KRUSTY-anchored cells.
- **To access KRUSTY-anchored specific power (2.4 W/kg) requires outbound aerocapture too.** That is a much harder engineering proposition (Earth-departure aerocapture has no obvious mechanism — the spacecraft is *leaving* Earth's atmosphere, not arriving).
- **The matrix's "Earth-side ~36 km/s of round-trip dv collapse" claim** would require: ~24.7 km/s of inbound aerocapture (full) + ~12 km/s of outbound credit (mechanism unspecified). This round only validates the inbound 24.7 km/s share.

### Reframed program verdict (replacing R10's "8 W/kg specific power binary threshold")

The program is now best described as **specific-power-AND-aerocapture-bet-limited**:
- Architecture E viable at ≥ 8 W/kg WITHOUT aerocapture, OR
- Architecture E viable at ≥ 5 W/kg WITH inbound aerocapture credit X ≥ 10 km/s, OR
- Architecture E NOT viable at KRUSTY-anchored 2.4 W/kg under any tested inbound-aerocapture credit ≤ 25 km/s.

Both axes must close. Round 5 measured posterior 0.78% for the FSP-class fission programmatic-credibility axis; the chunk-as-heat-shield aerocapture-credibility axis is separately unmeasured but should not be assumed at parity.

---

## Revisit

| Hypothesis | Predicted | Measured | Reason |
|---|---|---|---|
| H-11-a monotonic | yes | yes | held |
| H-11-b slope linear | -0.35 to -0.20 W/kg per km/s | -0.103 (plateau-dominated) | **falsified — framing error.** I assumed the cliff curve over X would be approximately linear over [0, 25]. In fact it drops fast over [0, 10] then plateaus at 5 W/kg over [10, 25] because no tested specific power lies between 2.4 and 5. The plateau itself may be a grid artifact OR a real outbound-burn-bottleneck. Falsified, but informatively. |
| H-11-c cliff to 5.3 W/kg at X ∈ [10, 15] | X = 10 | held at lower edge | held |
| H-11-d cliff to 2.4 W/kg at X ∈ [15, 25] | never reached | **falsified — substantive.** Inbound aerocapture alone cannot rescue KRUSTY-anchored specific power because the outbound burn time at 2.4 W/kg dry stack (213 t at 500 kWe, 421 t at 1000 kWe) eats the round-trip budget before inbound aerocapture saves anything. New decision-relevant finding. |
| H-11-e at X=25, 2.4 W/kg has ≥1 close cell | 0 close | **falsified — substantive.** Same root cause as H-11-d. |
| H-11-g RT delta at 5 W/kg, X=0 vs X=10 | [-1.4, -0.8] yr | -2.24 yr | **falsified — pre-reg arithmetic off.** Same R7 strike-4 class: I estimated the inbound-burn-time differential without recomputing the full inbound burn from scratch under the changed dv. The delivered-mass change from 18.3 → 73.8 t is also much larger than I expected — aerocapture credit acts on BOTH burn time AND propellant mass via the rocket equation. Filed as recurring-lesson-7 strike 6: **for delta-hypotheses, compute both endpoints fully; never estimate the differential.** |

---

## Cross-learning

**Adopt:**
- Aerocapture credit and specific power are jointly load-bearing on Architecture E viability; neither alone is sufficient. The matrix should present them as a 2D viability region: ≥ 8 W/kg OR (≥ 5 W/kg AND ≥ 10 km/s inbound aerocapture).
- Inbound-only aerocapture cannot rescue flown-system-anchored (≤ 5 W/kg) specific power; the outbound burn becomes binding.
- For delta-hypotheses, R7 strike 6 protocol fix: compute endpoints fully, never estimate the differential.

**Drop:**
- The framing that aerocapture is a single-axis rescue that "would unlock" Architecture E. It would unlock the 5–8 W/kg specific-power band but does not unlock the 2.4–5 W/kg band under inbound-only aerocapture.

**Defer:**
- Finer specific-power grid between 2.4 and 5 W/kg to resolve the plateau (is it 4.5 W/kg or 3.5 W/kg that becomes the new floor under X = 25 km/s?). Fast follow-on.
- Outbound aerocapture modeling. Out of scope for parallel session — likely needs trajectory-physics expertise.

**Forward references:**
- **STATE.md thread #13 (R-chunk-as-heat-shield-revisit-loadbearing):** now reframed quantitatively. The thread's load-bearing question becomes: "can inbound aerocapture credit X ≥ 10 km/s be physically achieved, and at what stack-mass scale?" This is a much more concrete target than "does aerocapture close?"
- **STATE.md thread #23 (R-expected-NPV-posterior-times-clearing-price):** now has a 2D viability region to integrate over, not just a 1D specific-power axis.

**Backward references:**
- R10 cliff at 8 W/kg: holds under X = 0 (no aerocapture).
- R9 specific-power dominance over MARVL-vs-bundled mass-model framing: re-confirmed.
- Round-6 18/120 close-cell count: corresponds to (sp = 10 W/kg, X = 0) cell in this round's grid, which is 9 close-25 (matches R10 9/60 at 10 W/kg; the factor of 2 difference is because round 6 had 120 cells = 60 × 2-mass-models and reported both, which R9 found was double-counting).

---

## Files of record

```
water-prop/rounds/R_aerocapture_cliff_shift/STUDY.md
water-prop/rounds/R_aerocapture_cliff_shift/run.py
water-prop/rounds/R_aerocapture_cliff_shift/results/aerocapture_cliff_shift.json
```

**Aggregate H-11 verdict:** the Architecture-E viability region is 2D. ≥ 8 W/kg specific power without aerocapture, or ≥ 5 W/kg specific power with ≥ 10 km/s inbound aerocapture credit. KRUSTY-anchored 2.4 W/kg specific power is not rescuable by inbound aerocapture alone, regardless of credit magnitude up to 25 km/s, because the outbound burn-time becomes binding. R-chunk-as-heat-shield-revisit thread now has a concrete inbound-credit target (10 km/s minimum, 25 km/s practical maximum).

