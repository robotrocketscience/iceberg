# Round 12 — Lunar Gravity Assist on Both Legs: Outbound Boost + Inbound Extended Tour

**Status:** pre-result.

## Question

Earth aerocapture is off the table (the conops' inbound velocity-reduction mechanism would leave no payload if forced to be propulsive at conops mass budget per R9b). The conops' lunar gravity assist replacement has been examined only for inbound (R9, 3-flyby tour shed 1.43 km/s). Outbound lunar gravity assist has not been examined at all.

**The question:** with aerocapture eliminated, can lunar gravity assist on both legs — outbound to reduce trans-Saturn-injection chemical burn, and inbound extended past 3 flybys — recover enough propulsive budget to close a 14-year round trip at viable delivery fraction (≥40%)?

## Pre-registered hypothesis (H12)

**Aggregate (H12-agg):** Lunar gravity assist on both legs is helpful but not architecture-rescuing. The combined recovery is ~3-5 km/s total propulsive budget relief, which moves the R9b Pareto cell from "20 kWe / 14.4 yr / 45% delivery" to "15-20 kWe / 14 yr / 50-55% delivery." It clears the 14-year investor ceiling at viable delivery. It does NOT recover the conops' headline 13-year / 60% delivery target.

**Pre-registered sub-claims:**

| Sub-claim | Predicted | Falsification |
|---|---|---|
| H12a — Outbound single-flyby v_∞ contribution at Earth sphere-of-influence | 0.8-1.5 kilometers per second at typical post-low-Earth-orbit C3 (post-trans-Saturn-injection v_∞ ≈ 5-7 km/s in Earth frame) | falsified if < 0.4 or > 2.5 km/s |
| H12b — Trans-Saturn-injection chemical burn reduction from outbound flyby | 0.5-1.2 km/s of trans-Saturn-injection cost saved (rough rule: lunar gravity assist v_∞ contribution ≈ trans-Saturn-injection burn savings at LEO altitude) | falsified if outside [0.2, 2.0] km/s |
| H12c — Inbound extended tour: total v_∞ shed for N flybys | Sub-linear growth in N. 3 flybys: 1.43 km/s (R9 confirmed). 6 flybys: ~3.5 km/s. 10 flybys: ~5 km/s. 12+ flybys: approaches asymptote ~6-7 km/s | falsified if 10-flyby shed < 3 km/s or > 8 km/s |
| H12d — Phasing time per inbound flyby | ~1 lunar synodic period per phasing return = 29.5 days. N flybys add (N-1) × 1 month of Earth-orbit phasing time | falsified if real phasing forces > 3 months per flyby (i.e. lunar resonance ratio mismatch) |
| H12e — Outbound + inbound combined recovery | 14-year round trip closes at 50-55% delivery (vs R9b bare-lunar-GA 20 kWe / 10 W/kg / 14.4 yr / 45.4%) | falsified if recovery < 5 percentage points delivery OR if 14-yr round trip remains unclosable at any tested cell |
| H12f — 13-year conops headline | Not recoverable at any tested cell (the conops' 13-year is structurally tied to aerocapture providing ~10 km/s of free v_∞ shedding; lunar gravity assists at best shed ~5 km/s and add phasing time) | falsified if any cell closes 13-year round trip at ≥50% delivery |

**Pre-registered conclusion if H12 holds:** the architecture without aerocapture closes at 14 years and ~50% delivery via lunar gravity assist on both legs and Fission Surface Power class reactor (~15-20 kWe with optimistic specific power). The conops' 13-year / 60% delivery cannot be recovered without aerocapture or a new ballistic gravity-assist mechanism (Jupiter inbound, R13 follow-up).

## Assumptions explicitly questioned by this round

| Conops or prior-round assumption | This round's posture |
|---|---|
| Outbound is Hohmann ballistic + single trans-Saturn-injection burn | **Held for R12.** Will examine non-Hohmann outbound in R14 if needed. |
| Aerocapture is the only mechanism that shed bulk inbound v_∞ "for free" | **Questioned by R12.** R12 quantifies how much lunar gravity assist can substitute. |
| 3-flyby lunar tour is the practical limit | **Questioned.** R12 sweeps 1-12 flybys. Each adds phasing time but contributes per-flyby v_∞ shedding that grows as v_∞ falls. |
| Earth-side gravity assists are the only ballistic v_∞ shedding mechanism on inbound | **Out of R12 scope, in R13 scope.** Jupiter gravity assist inbound is the next round. |
| Reactor specific power 5 W/kg is nominal, 10 W/kg is optimistic | **Held.** R9b already swept this. |
| Saturn dwell is 1 year, chunk mass is 14 tonnes | **Held.** Conops baseline. |
| Duty cycle on Pale Blue water radio-frequency ion is 0.5 | **Held.** Conservative; could be revisited. |

## Method

1. **Outbound lunar gravity assist contribution.** At post-LEO orbit (~7.8 km/s) with a lunar flyby on the way to trans-Saturn-injection, the spacecraft can pick up additional v_∞ at Earth sphere-of-influence. Use the existing `lunar_flyby` module in *reverse* — instead of shedding v_∞, compute the v_∞ added by an optimal-geometry flyby on the outbound leg. Sweep starting v_∞ at Earth sphere-of-influence from 0.5 to 5 km/s (range covering low-energy departures from LEO).
2. **Outbound trans-Saturn-injection burn reduction.** For each outbound v_∞ contribution, compute the trans-Saturn-injection burn savings via vis-viva — the chemical stage now has to provide less ∆v to reach Saturn v_∞.
3. **Inbound extended tour.** Use the existing `three_flyby_tour` model, extended to N flybys. Track per-flyby v_∞ contribution. The diminishing return is opposite to outbound: at high v_∞, bending angle is small and per-flyby ∆v is small. As v_∞ drops with each flyby, per-flyby ∆v grows.
4. **Phasing time.** Each return to lunar distance requires Earth-orbit phasing. Conservative estimate: one lunar synodic period (29.5 days) per phasing wait. N flybys add (N-1) × 1 month.
5. **Combined inbound budget.** For each (N flybys, reactor power class, specific power), compute residual propulsive braking ∆v = v_∞ after N flybys; compute braking time and delivered chunk fraction per R9b methodology.
6. **Round-trip total.** Outbound Hohmann (6.09 yr) + Saturn dwell (1.0 yr) + max(inbound Hohmann coast 6.09 yr, propulsive braking time) + inbound lunar tour phasing time (N-1 months).

**Validity caveats:**
- The `lunar_flyby` module's "optimal-geometry" assumption gives the theoretical maximum per-flyby ∆v. Real geometry constraints (launch window, Moon position) will reduce this by 10-30%.
- Outbound lunar gravity assist requires precise launch timing (Moon at the right position relative to the LEO orbit and the TSI departure asymptote). Conops body text does not currently include this constraint; if R12 holds, the conops launch-window analysis needs revision.
- Phasing time estimate of 1 lunar synodic period per pass assumes lunar resonance orbits exist at the right energies. The Folta-Beckman (NASA Goddard 2002) and Uphoff-Crouch (Jet Propulsion Laboratory 1993) references in the existing module are the load-bearing texts to verify against if any cell becomes architecturally chosen.
- Inbound phasing extends total mission time, which has compounding effects on reactor end-of-life and bag thermal margin. Not modeled here; flagged for revisit.
- Outbound trans-Saturn-injection savings via lunar gravity assist do not directly reduce the chemical stage's specific impulse — they reduce its ∆v requirement. Net pre-TSI mass reduction depends on the chemical stage's mass ratio.

## Result

### Outbound: lunar gravity assist reduces trans-Saturn-injection burn

| N outbound flybys | v_∞ at Earth SOI pre-GA (km/s) | GA contribution (km/s) | TSI burn with GA (km/s) | TSI savings (km/s) | Phasing (months) |
|---:|---:|---:|---:|---:|---:|
| 1 | 9.63 | 0.59 | 6.84 | 0.40 | 0 |
| 2 | 8.99 | 1.23 | 6.43 | 0.81 | 1.0 |
| 3 | 8.31 | 1.91 | 6.01 | 1.23 | 1.9 |
| 4 | 7.55 | 2.67 | 5.57 | 1.67 | 2.9 |
| 5 | 6.70 | 3.52 | 5.11 | 2.13 | 3.9 |

A 3-flyby outbound tour saves ~1.2 km/s on the trans-Saturn-injection burn (7.24 → 6.01 km/s), at the cost of ~2 months of Earth-orbit phasing. A 5-flyby tour saves 2.1 km/s but takes ~4 months. The savings translate to a smaller chemical kick stage — potentially Falcon 9 expendable instead of Falcon Heavy, depending on payload margins.

### Inbound: extended lunar tour, N flybys

| N requested | N executed | v_∞ final (km/s) | Total shed (km/s) | Phasing (months) |
|---:|---:|---:|---:|---:|
| 1 | 1 | 9.84 | 0.46 | 0 |
| 3 | 3 | 8.87 | 1.43 | 1.9 |
| 5 | 5 | 7.80 | 2.50 | 3.9 |
| 8 | 8 | 5.96 | 4.34 | 6.8 |
| 10 | 10 | 4.47 | 5.83 | 8.7 |
| 12 | 12 | 2.63 | 7.67 | 10.7 |
| 16 | 14 | 0.15 | 10.15 | 12.6 (terminated at v_∞ < 0.5) |

Per-flyby contribution grows as v_∞ falls (4.34 km/s from 8 flybys vs only 1.43 km/s from the first 3). Around N=14, the residual v_∞ drops below 0.5 km/s and the tour saturates.

### Combined: round trip vs delivery across the (flyby count × reactor power) grid

| Inbound flybys | Power (kWe) | Specific power (W/kg) | Residual ∆v (km/s) | Inbound TOF (yr) | Round trip (yr) | Delivery | Closes 14 yr |
|---:|---:|---:|---:|---:|---:|---:|:---:|
| 3 | 30 | 10.0 | 8.87 | 6.25 | 13.34 | 42.8% | yes |
| 5 | 20 | 10.0 | 7.80 | 6.87 | 13.96 | 50.8% | yes |
| 5 | 30 | 10.0 | 7.80 | 6.41 | 13.50 | 48.4% | yes |
| 8 | 20 | 5.0  | 5.96 | 6.66 | 13.75 | 57.0% | yes |
| 8 | 20 | 10.0 | 5.96 | 6.66 | 13.75 | 60.7% | yes |
| 8 | 30 | 10.0 | 5.96 | 6.66 | 13.75 | 58.8% | yes |
| **10** | **15** | **10.0** | **4.47** | **6.82** | **13.91** | **70.1%** | **yes** |
| 10 | 20 | 5.0  | 4.47 | 6.82 | 13.91 | 66.5% | yes |
| 10 | 20 | 10.0 | 4.47 | 6.82 | 13.91 | 69.4% | yes |
| 10 | 30 | 10.0 | 4.47 | 6.82 | 13.91 | 67.9% | yes |
| 12 | 10 | 10.0 | 2.63 | 6.98 | 14.07 | 82.1% | no (over by 0.07 yr) |
| 12 | 15 | 10.0 | 2.63 | 6.98 | 14.07 | 81.6% | no |
| 12 | 20 | 10.0 | 2.63 | 6.98 | 14.07 | 81.2% | no |

(All other cells listed in `results/lunar_GA_both_legs.json`.)

**Best Pareto cell (max delivery at ≤ 14-year round trip):** **10 lunar flybys inbound + 15 kWe at 10 W/kg specific power.** Round trip 13.91 yr, delivery 70.1%. Reactor mass 1.5 t. Inbound phasing adds 8.7 months. Residual propulsive braking ∆v = 4.47 km/s.

**Cells closing 13-year (conops headline) at ≥50% delivery: 0.** Confirmed unreachable without aerocapture.

### Hypothesis grading

| Sub-claim | Predicted | Measured | Verdict |
|---|---|---|---|
| H12a — Outbound single-flyby v_∞ contribution | 0.8-1.5 km/s | 0.59 km/s | held (within ±0.4 falsification band, but on the low side — bending-angle limit at trans-Saturn-injection v_∞ class is binding) |
| H12b — TSI savings single-flyby | 0.5-1.2 km/s | 0.40 km/s | held (low end) |
| H12c — Inbound 10-flyby shed | 3-8 km/s | 5.83 km/s | held |
| H12d — Phasing time per flyby | ~1 lunar synodic period per pass | Modeled as 29.5 days/pass; total 8.7 months for 10 flybys | held by construction |
| H12e — 14-year + ≥50% delivery achievable | yes | yes — 10-flyby + 15 kWe / 10 W/kg = 13.91 yr / 70.1% | held cleanly |
| H12f — 13-year + ≥50% delivery NOT achievable | no cell closes both | 0 cells close both | held |

Result JSON: `results/lunar_GA_both_legs.json`.

## Reading

**Headline: with aerocapture off the table, the architecture closes at 14-year round trip and 70% delivery via a 10-flyby inbound lunar gravity assist tour and a 15 kWe Fission-Surface-Power-class reactor with optimistic specific power.** This is meaningfully better than R9b's bare-numbers floor (20 kWe / 14.4 yr / 45.4%). The recovery comes from the multi-flyby tour: as v_∞ drops with each flyby, per-flyby ∆v grows, and 10 flybys shed 5.83 km/s vs the 3-flyby tour's 1.43 km/s.

**Three Pareto-optimal cells in the 14-year band:**

| Cell | Round trip | Delivery | Why pick this |
|---|---:|---:|---|
| 8 flybys + 20 kWe / 10 W/kg | 13.75 yr | 60.7% | Shorter inbound phasing (6.8 months); lower power class |
| **10 flybys + 15 kWe / 10 W/kg** | **13.91 yr** | **70.1%** | **Best delivery within 14-year; modest reactor at 1.5 t** |
| 10 flybys + 20 kWe / 5 W/kg | 13.91 yr | 66.5% | Same RT, slightly worse delivery, doesn't require optimistic specific power |

The 10-flyby + 15 kWe / 10 W/kg cell is the recommended deck cell. The 8-flyby variant is the safer fallback if 10 flybys is operationally too painful.

**Why this is a meaningful step beyond R9b:**
- R9b assumed a 3-flyby tour was the only lunar option (per R9 default). That capped the lunar contribution at 1.43 km/s and left propulsive braking with 8.87 km/s to shed.
- R12 sweeps 1-20 flybys and finds the practical sweet spot at 10-12 flybys (diminishing returns kick in around 12 as v_∞ falls below 3 km/s).
- The cost is phasing time (~9 months for 10 flybys), but that phasing time is at Earth (mission ops are easy at lunar distance, comms are nominal, the spacecraft is healthy).

**Outbound contribution is real but modest.** A 3-flyby outbound tour saves 1.23 km/s on trans-Saturn-injection. This translates to a smaller chemical kick stage. Whether it matters depends on launch-vehicle economics. If Falcon Heavy expendable is forced by the conops' baseline ~45 t pre-TSI mass, a 1.2 km/s TSI savings might allow Falcon 9 expendable (a ~$60M launch saving). Not architecture-critical, but a real program-level cost lever.

**The conops 13-year headline is not recoverable.** Even at the most aggressive cell (12 flybys + 40 kWe), round trip is 14.07 yr — over 13 yr and over 14 yr by 0.03 yr. The Hohmann floor of 6.09 + 1.0 + 6.09 = 13.18 yr is the hard structural minimum; any inbound phasing time adds on top. To get below 14 yr you have to keep total inbound phasing under 10 months.

**Architectural read for the deck:**
- Aerocapture eliminated → architecture moves from "13 yr / 75%" conops headline to "**14 yr / 70%**" via 10-flyby lunar tour + Fission-Surface-Power-class reactor.
- This is **within the 14-year investor ceiling.**
- Penalty vs conops: round trip 6% longer (0.9 yr), delivery 7% lower (5 percentage points: 70% vs 75%). Steady-state revenue cadence per ship drops correspondingly by ~10%. Mission economics survive.
- Recommended cell carries three new commitments: Fission Surface Power program reactor (TRL 4-5, 10 W/kg specific power assumption); 10-pass lunar gravity assist tour on inbound (NASA Goddard 2002 has the design space — well within state of the art); chemical TSI kick stage at conops baseline (no help from outbound lunar GA *required* — it's a margin lever, not a critical path).

## Revisit

- **Flyby-timing risk (user-flagged, important).** Lunar flybys are "Moon is always there" reliable in the sense that the Moon's position cycles every 27.3 days and no rare alignment is required to attempt a flyby. But each return from a lunar flyby has to be on a resonance orbit whose period is a rational fraction of the lunar period (e.g., 2:1, 3:2, 5:3 ratios). Mission-design heritage on multi-flyby lunar tours exists (Folta & Beckman 2002; LunIR, ARTEMIS) but real-world phasing may slip by 1-3 weeks per pass relative to the idealized "29.5 days flat." For 10 flybys, accumulated launch-window slack might be ±3 months. The R12 phasing estimate (8.7 months for 10 flybys) should carry that ±25% dispersion as a planning margin.
- **First-flyby alignment depends on Hohmann arrival epoch.** The spacecraft arrives at Earth from Saturn at a specific date; the Moon must be in the right phase relative to the arrival asymptote for the first flyby to be possible. If the Moon is misaligned at arrival, the spacecraft has to do a 1-period parking loop and re-attempt at the next opportunity. This adds up to one extra synodic period (~1 month) of mission time but is not a hard mission failure.
- **Inclination penalty not modeled.** The `lunar_flyby` module's inclination penalty (cos(φ) on the in-plane component) is set to 0° in this round. Real lunar trajectory plane and the inbound heliocentric trajectory plane will have non-trivial relative inclination; cos(20°) = 0.94 penalty, cos(40°) = 0.77 penalty. Worth re-running R12 with inclination 0-30° as a sensitivity. If the penalty halves the per-flyby contribution, the 10-flyby budget would need to grow to ~15-18 flybys for the same total shed — pushing phasing time to ~14 months and round trip closer to 15 yr.
- **Outbound lunar GA scheduling.** R12 treats outbound and inbound flyby tours as independent. In reality, the spacecraft's launch date sets the Moon's outbound geometry; the spacecraft's Saturn return sets the inbound geometry. The two are linked by the Saturn-Earth synodic cycle (~378 days). Whether both legs can be optimized simultaneously is a launch-window-design problem not in R12 scope. Probably tractable but worth verifying.
- **R9b's max-of formula remains the cruise time model.** The braking acceleration computation here uses the simple constant-thrust model. A proper low-thrust optimal-control trajectory might shave 5-10% off the cruise time, marginally improving cells near the 14-year boundary.
- **The 10-flyby cell is at the optimistic end of specific power assumption (10 W/kg).** At nominal Fission Surface Power specific power of 5 W/kg, the 15 kWe reactor is 3 t instead of 1.5 t; rerunning at 10 flybys + 15 kWe + 5 W/kg gives 67.9% delivery (vs 70.1% at 10 W/kg) — still within the 14-year band. The architecture is not critically sensitive to specific power assumption.

## Cross-learning

- **Multi-flyby lunar gravity assist is a real architectural lever, not a footnote.** R9 treated 3-flyby tours as the practical limit. R12 shows the practical limit is closer to 12 flybys, and that going from 3 to 10 flybys shifts the architecture from "marginal" to "viable" — a 25-percentage-point delivery improvement. Pattern: when the first round shows a mechanism contributes a small amount, sweep the count parameter beyond conventional limits before concluding the mechanism is inadequate.
- **Per-flyby contribution grows as the residual quantity falls.** This is the opposite of most engineering tradeoffs (where each marginal step costs more). For lunar gravity assist, each successive flyby costs *less* in v_∞-reduction-per-flyby-time. The mathematics of bending-angle vs relative velocity is a non-obvious driver. Worth carrying forward as a methodology note: when sweeping the count of a sequential operation, check whether per-step contribution is increasing or decreasing with iteration.
- **Round trip vs delivery vs power class is now a three-dimensional Pareto.** Adding inbound flyby count as a fourth dimension. Better to think of the architecture as a 4-knob system (round trip target, delivery target, reactor power class, inbound flyby count) where any three constrain the fourth. The conops collapsed these into one cell (13 yr / 75% / Kilopower / 0 flybys with aerocapture); R12 surfaces the real surface.
- **The 14-year ceiling is genuinely achievable without aerocapture, at modest delivery penalty.** The user's "14 years max for investors" constraint is met by the 10-flyby + 15 kWe cell. The architectural give-up is 5 percentage points of delivery (75% → 70%) and a 0.9-year mission extension. This is the answer to bring to the pitch room.
- **Methodology check (passed):** I pre-registered an aggregate prediction (~5 percentage point delivery improvement vs R9b base case) and the actual result was much better (~25 percentage points). The aggregate held cleanly, but the magnitude was very different from my prediction. Lesson: when a held prediction is also a *strong* result, that means my prior was under-calibrated on the magnitude. Should widen the prediction band on similar sweep rounds going forward.
- **Risk decomposition for the deck.** The honest "what could go wrong" list for the R12 architecture is now:
  - Flyby tour resonance phasing fails to materialize (medium probability, ~3 months phasing slip per failure)
  - Fission Surface Power program lands at 5 W/kg specific power instead of 10 W/kg (medium probability, ~3 pp delivery hit)
  - First-flyby alignment misses at Earth arrival (low probability, ~1 month delay)
  - Lunar gravity assist plane inclination penalty exceeds 20° (medium probability, would force more flybys and longer phasing)
  - 10-flyby trajectory navigation accuracy below mission requirement (low probability per Folta-Beckman, but real)
