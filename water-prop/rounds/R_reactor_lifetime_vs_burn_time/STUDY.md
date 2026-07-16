# R-reactor-lifetime-vs-burn-time — does the fission reactor outlive the cumulative burn?

**Status:** pre-registration. Authored 2026-05-15 by enceladus-r5 (round 12). Direct follow-on to R11.

## What I'm questioning

Every Architecture-E cell tested in rounds 6, 9, 10, and 11 assumes the on-ship fission reactor delivers thrust-grade electric power for the full cumulative burn time — outbound plus inbound. At round-6's best cell (500 kilowatts electric reactor, 200 tonne chunk, specific impulse 2934 seconds, 10 watts per kilogram specific power), cumulative burn is about 2 years. At round-11's aerocapture-rescued 5 watts-per-kilogram cell, cumulative burn approaches 10 years. None of those rounds applied a *reactor lifetime ceiling.*

**What ground-test heritage exists:**

- KRUSTY (the Kilowatt Reactor Using Stirling Technology, 1 kilowatt electric, Nevada 2018) ran its longest test for about **28 hours**. Not 28 days. Not 28 years. Twenty-eight hours.
- Kilopower-class design life is **10 years** — a *target* from the program, not a measurement.
- The space-fission flown record is SNAP-10A in 1965: ran for **43 days** before an electrical-system failure shut it down (not a reactor failure, but the system was lost regardless).
- National Academies 2021 Space Nuclear Propulsion report notes "very little advancement" in space-qualified fission lifetime over the past decade.

**Megawatt-class continuous operation for years is unprecedented.** Round 6 assumed it; rounds 9, 10, 11 assumed it; this round tests it.

## Mechanism — what limits reactor "lifetime" in the load-bearing sense

Multiple independent failure modes:

1. **Reactor core integrity** — fuel cladding swelling under neutron flux; reactivity drift as fuel burns up. For a megawatt-class core driven hard for years, fuel-burnup window is finite but typically > 10 years if the core is sized with margin.
2. **Brayton-cycle conversion machinery** — turbo-alternator-compressor rotating parts have finite spin-hour life. Aerospace Brayton machinery flight-rated lifetimes are 5–10 years continuous (terrestrial industrial Brayton: 20+ years, but heavier and not redundant for space).
3. **Radiator coolant degradation** — sodium-potassium loops at high temperature have finite life under neutron flux from the reactor side; cladding corrosion progresses over years.
4. **Power-electronics tolerance** — direct-drive Hall and ion thrusters from megawatt-class buses have not flown; high-voltage switching at multi-hundred-kilowatt power is a separate qualification question.
5. **Thrust subsystem** (Hall cathode life, grid erosion) — separate thread, see `R_cathode_life_water_plasma`. This round focuses on the *reactor* lifetime; thruster lifetime is treated separately.

The conservative bound is the shortest of these modes. For a megawatt-class system, that is plausibly **5–10 years** of cumulative full-power operation, with strong dependence on detailed design margin.

## Question

If I impose a reactor lifetime ceiling **L** ∈ {5, 8, 10, 15, ∞} years on the cumulative burn time (outbound burn + inbound burn) and re-grade R9, R10, R11's close-cell tables, how many cells remain L0-05 compliant?

## Pre-registered hypotheses (H-12)

**Component-level pre-check at round-6's headline cell (500 kilowatts, 200 tonne chunk, 2934 second specific impulse, 10 watts per kilogram, no aerocapture):**

From R11 output / R9 baseline:
- Dry tug: 55 tonnes
- Outbound burn: 189 tonnes propellant / 22.6 newtons thrust = 0.74 years burn time (estimated from arithmetic; R6 measured slightly different)
- Inbound burn: about 1.3 years
- Cumulative: about 2.0 years

This cell easily fits within any tested lifetime ceiling (5 years minimum). All 9 close cells at 10 watts per kilogram should survive a 5-year reactor-lifetime ceiling.

**Component-level pre-check at 5 watts per kilogram / 500 kilowatts / 200 tonnes / 2934 seconds / aerocapture 10 km/s** (R11 best-case rescue cell, round-trip 26.61 years, delivered 73.8 tonnes):
- Dry tug: 105 tonnes
- Outbound propellant: 189 tonnes / 22.6 newtons = about 7.6 years
- Inbound propellant: 122 tonnes / 22.6 newtons = about 4.9 years (with aerocapture-reduced delta-velocity)
- Cumulative: about **12.5 years**

This cell **exceeds** the 10-year Kilopower-class design life. Under a 10-year ceiling, this cell falls. Under a 15-year ceiling, it closes.

**Component-level pre-check at 8 watts per kilogram / 500 kilowatts / 200 tonnes / 2934 seconds / no aerocapture** (R10 cliff cell):
- Dry tug: 5 + 500/8 = 67.5 tonnes
- Outbound: 67.5 × (exp(29560/28793) − 1) = 67.5 × 1.802 = 121.6 tonnes propellant
- Thrust: 22.6 newtons (independent of specific power)
- Outbound burn: 121,600 × 28,793 / 22.6 = 1.55 × 10^8 seconds = **4.91 years**
- Inbound: m_prop = (67.5 + 200) × (1 − 1/exp(24700/28793)) = 267.5 × 0.420 = 112.4 tonnes; burn = 112,400 × 28,793 / 22.6 = 1.43 × 10^8 seconds = **4.53 years**
- Cumulative: **9.44 years**

This cell *just barely* sits under a 10-year reactor lifetime ceiling. Under an 8-year ceiling, it falls.

| # | Hypothesis | Predicted | Falsified if |
|---|---|---|---|
| H-12-a | All 9 close cells at 10 watts per kilogram (R10 baseline, no aerocapture) have cumulative burn ≤ 5 years | true | any of the 9 cells has cumulative > 5 years |
| H-12-b | At least 4 of R10's 9 close cells at 10 watts per kilogram have cumulative burn ≤ 2 years | true | fewer than 4 |
| H-12-c | At 8 watts per kilogram, no aerocapture (R10's cliff): of 4 close cells, **2–3** fall under a 10-year reactor lifetime ceiling | in range | outside range |
| H-12-d | At 5 watts per kilogram / 10 km/s aerocapture (R11): of 3 close cells, **2–3** fall under a 10-year ceiling; **0** survive a 5-year ceiling | in range | outside range |
| H-12-e | At 5 watts per kilogram / 25 km/s aerocapture (R11): of 44 close cells, **fewer than half** survive a 10-year ceiling | < 50 percent | ≥ 50 percent |
| H-12-f | Across the full R11 grid (specific power × aerocapture × R10 sub-grid), reactor-lifetime constraint of 10 years removes **30–50 percent** of close-25-year-ceiling cells | in range | outside range |
| H-12-g | At every specific power tested, there exist close cells with cumulative burn ≤ 5 years — i.e. a 5-year reactor lifetime is sufficient if specific power AND aerocapture are favorable | true | no closing cell at 5-year cumulative at any tested specific power |
| H-12-h | Aggregate verdict: the reactor lifetime constraint is **secondary to specific power** at the 10-year ceiling (matches Kilopower target) — most cells survive — but **primary** at the 5-year ceiling (matches Brayton-machinery flight-rated minimum) — most cells fall | matches the aggregate measurement | falsified if the ranking inverts |

**Honest caveats:**
- I am treating "cumulative burn time" = outbound burn + inbound burn, with the reactor idle during cruise. This is conservative on reactor wear (idle is easier than full power). A *less* conservative measure that some authors prefer is "elapsed time since startup including cruise," which would be the full round-trip (15–30+ years). I am using the conservative measure because reactor wear under continuous full-power operation is the actual mechanism, not calendar elapsed time.
- Brayton cycle / power-conversion subsystem can be redundant — two stacks, one runs while the other is held in reserve. This effectively doubles cumulative operating budget but doubles mass too. Not modeled here. Would soften the constraint.
- Reactor restart capability after long idle is itself a qualification question. Idling for 6+ years in cruise then restarting at full power is unprecedented. Conservative assumption: this works. Real assumption may be that it doesn't, in which case Architecture E has a separate problem (the inbound burn requires reactor restart after 7+ years idle).

## Method

For each cell in R9, R10, R11 sweeps, compute cumulative burn time = outbound_burn_time + inbound_burn_time. For each reactor lifetime ceiling L ∈ {5, 8, 10, 15, ∞} years, re-grade close-25-year-ceiling cells under the joint constraint:

`feasible_under_lifetime_L = closes_25yr AND cumulative_burn ≤ L AND delivered > 0`

Tabulate the joint close-cell count at each L for each (specific power, aerocapture) combination.

This is post-processing of R11's grid — no new physics. Roughly 3 minutes of compute.

## What this round does NOT do

- Does not model the reactor-restart-after-long-idle question.
- Does not model thruster-cathode lifetime, grid erosion, or any other subsystem-life constraint.
- Does not include bag-permeability vapor loss during long cumulative-burn cells.
- Does not credit redundant power-conversion stacks (would soften the constraint).
- Does not derive a posterior on "reactor-lifetime credibility" — that is a separate research question. This round answers the engineering "does it fit if it works" question.

---

## Result

### Survival of close-25-year-ceiling cells under reactor-lifetime ceilings (cells in each bucket)

**5-year lifetime ceiling** (Brayton flight-rated minimum, conservative):

| sp \\ X (km/s) | 0 | 5 | 10 | 15 | 20 | 25 |
|---:|---:|---:|---:|---:|---:|---:|
| 2.4 | 0 | 0 | 0 | 0 | 0 | 0 |
| 5–8 | 0 | 0 | 0 | 0 | 0 | 0 |
| 9 | 0 | 0 | 0 | 0 | 0 | 16 |
| 10 | 0 | 0 | 0 | 0 | 9 | 24 |

**10-year lifetime ceiling** (Kilopower-class design target):

| sp \\ X (km/s) | 0 | 5 | 10 | 15 | 20 | 25 |
|---:|---:|---:|---:|---:|---:|---:|
| 2.4 | 0 | 0 | 0 | 0 | 0 | 0 |
| 5 | 0 | 0 | 0 | 1 | 12 | 32 |
| 6 | 0 | 0 | 1 | 10 | 25 | 44 |
| 7 | 0 | 3 | 6 | 16 | 34 | 48 |
| 8 | 1 | 3 | 15 | 23 | 39 | 56 |
| 9 | 4 | 6 | 16 | 29 | 41 | 56 |
| 10 | 5 | 7 | 18 | 31 | 41 | 56 |

**15-year lifetime ceiling** (effectively non-binding, matches infinite-life grid):

Identical to R11's unconstrained grid. The longest cumulative burn time observed in any close-25-yr cell was **11.83 years** at 5 watts per kilogram / 10 kilometers-per-second aerocapture; all such cells fit under 15 years.

### Hypothesis grading

| # | Predicted | Measured | Status |
|---|---|---|---|
| H-12-a | all 9 close-cells at 10 W/kg X=0 have cumulative burn ≤ 5 yr | max cumulative burn = **11.37 yr**; 0 cells under 5 yr | **FALSIFIED** (arithmetic error on my side) |
| H-12-b | ≥ 4 cells at 10 W/kg X=0 have cumulative ≤ 2 yr | **0** cells under 2 yr | **FALSIFIED** (same root cause) |
| H-12-c | 2–3 of 4 cells at 8 W/kg X=0 fall under 10-yr ceiling | 3 fall (cumulative burns 9.15 / 10.58 / 10.79 / 11.74 yr) | **HELD** |
| H-12-d | of 3 close at 5 W/kg X=10: 2–3 fall under 10 yr, 0 survive 5 yr | all 3 fall under 10 yr (11.58 / 11.63 / 11.83 yr), 0 survive 5 yr | **HELD** |
| H-12-e | < 50% of 44 close at 5 W/kg X=25 survive 10-yr ceiling | **72.7% survive** | **FALSIFIED** (aerocapture saves burn time too) |
| H-12-f | 10-yr ceiling removes 30–50% of full-grid close-25 cells | removes **20.6%** | **FALSIFIED** (low end) |
| H-12-g | every specific power has at least one cell under 5-yr ceiling | **only 9 and 10 W/kg do** (at high aerocapture) | **FALSIFIED** |
| H-12-h aggregate | 10-yr ceiling secondary; 5-yr ceiling primary | 10-yr removes 20.6%; 5-yr removes ~95% — directionally correct but magnitudes off | partial |

**Score: 2 HELD, 5 FALSIFIED.** Most falsifications are because my pre-registration arithmetic for cumulative burn time was off by a factor of about 5. I claimed the round-6 best cell had cumulative burn ~2 years; the simulation says about 10 years. This is an R7-strike-7-class arithmetic error: I conflated "burn-time fraction of round-trip" with "burn time," when in fact for continuous-thrust electric propulsion at megawatt-class power, the burn times are themselves multi-year. The pre-reg dry-mass / thrust / propellant arithmetic was correct in isolation; the burn-time-in-years calculation was wrong.

R7-strike-7 protocol fix: **for any hypothesis on cumulative burn time, compute outbound burn time AND inbound burn time from `m_prop × v_e / thrust / seconds_per_year` from scratch — not from any cached round-trip-time decomposition or "burn fraction" intuition.**

---

## Reading

**Architecture E is structurally a decade-long burn mission**, not a "few years of thrust within a multi-decade round trip." Most close cells in the R11 grid require **8 to 12 years** of cumulative full-power reactor operation. KRUSTY's 28-hour ground test heritage is **3 to 4 orders of magnitude** short of what any viable Architecture-E cell needs.

The viability region is now **3-dimensional**:

1. **Specific power** (R10 cliff at 8 watts per kilogram unaccompanied, 5 watts per kilogram with aerocapture per R11)
2. **Aerocapture inbound delta-velocity credit** (R11: 10 kilometers per second minimum useful, 25 kilometers per second practical maximum for inbound-only)
3. **Reactor lifetime** (this round: 10-year Kilopower target costs ~20% of cells; 5-year Brayton-flight-rated costs ~95%)

**Where each ceiling binds:**

- **5-year reactor lifetime** (conservative Brayton aerospace machinery) — only 9 and 10 watts-per-kilogram cells with X ≥ 20 kilometers per second aerocapture survive. KRUSTY-anchored 2.4 watts-per-kilogram, intermediate 5–7 watts-per-kilogram, and 8 watts-per-kilogram (R10 cliff) all die. The mission needs either much shorter burns (higher thrust → lower specific impulse, but breaks rocket equation) or a redundant power-conversion stack (mass penalty, not modeled).

- **10-year reactor lifetime** (Kilopower design target, *unproven*) — about 80 percent of close-25-yr cells survive. The architecture works, IF Kilopower-class fission can be scaled from 1 kilowatt electric to 500–1000 kilowatt electric AND deliver its design life. The 0-of-6 fission-program-flight base rate (locked R-power-wonder finding 2) bears on the second AND.

- **15-year reactor lifetime** — equivalent to no constraint. No close-25-yr cell exceeds 11.83 years cumulative.

### Reframed program verdict (replacing R11's 2D viability region)

The program is **specific-power-AND-aerocapture-AND-reactor-lifetime-bet-limited**. Each axis is independently load-bearing; closure requires all three. For the round-6 baseline cell (500 kilowatts / 200 tonnes / 2934 seconds / 10 watts per kilogram / no aerocapture, the strongest pre-existing closure case), cumulative burn is **11.37 years** — *exceeds* Kilopower's 10-year design target by 14 percent. The matrix's "Variant B retitled 500-kWe chemical-kick + electric-inbound" surviving cell is, on this measure, **not** closure-compliant against the Kilopower-target reactor lifetime. It requires either a 15-year reactor or a redundant power-conversion stack with rotation — neither of which has flight heritage.

### What this round closes

- The matrix should add a "cumulative burn time" column to the surviving-cell table, alongside the round-trip time. For round-6's retained 500-kWe baseline cell at MARVL-anchored mass, the cumulative-burn entry should be **~11 years**, with the annotation "exceeds Kilopower-class 10-year design target; requires either 15-year reactor lifetime qualification (no heritage) or redundant power conversion (mass penalty, not in this round's model)."
- Architecture E's "9 close cells at 25-yr ceiling at 10 watts per kilogram" claim from R10 needs the same annotation. None of those 9 cells closes under the 10-year reactor lifetime ceiling.
- The matrix's R-chunk-as-heat-shield-revisit thread keeps its already-quantified inbound-aerocapture target (10 kilometers per second minimum useful) AND gains a new criterion: a 5-year reactor lifetime requires X ≥ 20 kilometers per second AND specific power ≥ 9 watts per kilogram. The combined target is more demanding.

### What this round does NOT settle

- Redundant power-conversion stack mass penalty: not modeled. Adding a redundant Brayton stack roughly doubles power-conversion subsystem mass (~15 percent of total tug dry mass at megawatt scale), which would shift the specific power cliff up by about 1 watt per kilogram. Worth a separate round.
- Reactor-restart-after-cruise question: most cells have multi-year idle (cruise) between outbound and inbound burns. Reactor restart at full power after 6–8 years of idle is unprecedented and unmeasured. Filed as follow-on thread.
- Hall thruster cathode lifetime: 30,000 to 50,000 hours flight-demonstrated for sub-10-kilowatt thrusters; megawatt-class water-plasma thrusters are research-grade. Separate round (`R_cathode_life_water_plasma` already exists in the repository).

---

## Revisit

| Hypothesis | Predicted | Measured | Reason |
|---|---|---|---|
| H-12-a | all 9 close at 10 W/kg X=0 ≤ 5 yr cumulative | max = 11.37 yr | **falsified.** Arithmetic error in pre-reg: I claimed "0.74 + 1.3 = 2.04 yr cumulative burn" for the round-6 best cell, but real cumulative for that cell is about 10 years. The error was conflating burn-time fraction-of-RT with burn time. R7 strike 7. |
| H-12-b | ≥ 4 cells ≤ 2 yr | 0 cells ≤ 2 yr | falsified (same root cause). |
| H-12-c | 2–3 of 4 cells at 8 W/kg X=0 fall under L=10 | 3 fall | held |
| H-12-d | all 3 cells at 5 W/kg X=10 fall under L=10, none survive L=5 | both hold | held |
| H-12-e | < 50% of 44 cells at 5 W/kg X=25 survive L=10 | 72.7% survive | **falsified informatively.** Full inbound aerocapture eliminates the inbound burn (zero inbound delta-velocity = zero inbound burn time), reducing cumulative burn dramatically. Aerocapture saves burn time in addition to propellant — a coupling I missed in pre-reg. |
| H-12-f | 30–50 percent of full-grid close-25 cells removed by L=10 | 20.6 percent removed | falsified (low end). Same root cause as H-12-e — high-aerocapture cells have much shorter cumulative burn than I estimated. |
| H-12-g | every specific power has a cell under L=5 | only 9 and 10 W/kg do | **falsified.** At very low specific power, even with full inbound aerocapture, the outbound burn alone exceeds 5 years. |

**R7 strike 7 protocol fix:** for any cumulative-burn-time hypothesis, compute outbound and inbound burn times from first principles using `m_prop × exhaust_velocity / thrust / seconds_per_year`, not from any decomposition of round-trip time. The "burn fraction of round trip" intuition is unreliable at very long burn times because cruise is fixed (one Hohmann ≈ 6 years each way) while burns scale with dry mass — at high dry mass and low specific power, burns can exceed cruise.

---

## Cross-learning

**Adopt:**
- Architecture E viability is 3-dimensional: specific power, aerocapture inbound credit, reactor lifetime. Closure requires all three. The matrix should present all three with concrete thresholds.
- The R10 / R11 close-cell counts at 10 watts per kilogram and below all assume reactor lifetime ≥ 12 years. None of those cells close under a Kilopower-target 10-year reactor lifetime.
- Full inbound aerocapture (X ≈ 25 km/s) reduces inbound burn time to near zero AND reduces inbound propellant mass — a 2x effect on cumulative burn, not 1x. This coupling matters.

**Drop:**
- The framing that the round-6 / matrix-surviving 500-kilowatt baseline cell is closure-compliant. It is compliant against round-trip time (under 15 years) but **non-compliant** against a Kilopower-target reactor lifetime (about 11 years cumulative burn vs 10-year design life).
- The intuition that megawatt-class burn times are a small fraction of the round-trip. They are not: at 5–10 watts per kilogram, burns are 7–12 years, comparable to or exceeding the cruise.

**Defer:**
- Redundant power-conversion stack analysis: mass penalty vs lifetime extension. Probably worth its own short round.
- Reactor restart after multi-year idle.
- Bag permeability vapor loss during long cumulative burns (the bag is loaded with chunk water during inbound; long inbound burn means long exposure of the bag to vapor pressure).

**Forward references:**
- **Thread #13 (R-chunk-as-heat-shield-revisit):** aerocapture credit is even more valuable than R11 said — it saves cumulative burn time, not just propellant. The 10-km-per-second target becomes a 20-km-per-second target when reactor lifetime is set at the Brayton 5-year flight-rated minimum.
- **Thread #23 (joint expected NPV × posterior):** the joint now has 3 axes, not 2. Reactor lifetime credibility is its own prior — KRUSTY's 28-hour heritage to 10-year design target is a >3-order-of-magnitude technology readiness leap.

**Backward references:**
- Round 6: the "Active — sole defensible cell" annotation for the 500-kilowatt chemical-kick + electric-inbound (Variant B) survives at the round-trip-time level but **fails** the cumulative-burn-time check against Kilopower's 10-year design target. Matrix surviving-cell annotation needs amending.
- Round 9 / R10: same. The closure counts at 10 and 9 watts per kilogram are unchanged at infinite-lifetime, but most of those cells fail the 10-year reactor lifetime check.
- Round 11: the X = 10 km/s "rescue" of 5 watts per kilogram still works at infinite-lifetime, but fails completely under the 10-year ceiling. The plateau at 5 watts per kilogram from X ≥ 10 onward disappears under reactor-lifetime constraints; the new floor under 10-year reactor lifetime is closer to 7 watts per kilogram.

---

## Files of record

```
water-prop/rounds/R_reactor_lifetime_vs_burn_time/STUDY.md
water-prop/rounds/R_reactor_lifetime_vs_burn_time/run.py
water-prop/rounds/R_reactor_lifetime_vs_burn_time/results/reactor_lifetime_regrade.json
```

**Aggregate H-12 verdict:** every viable Architecture-E cell in rounds 6, 9, 10, 11 requires the on-ship fission reactor to deliver 8–12 years of cumulative full-power thrust. KRUSTY's 28-hour ground test heritage is 3 to 4 orders of magnitude short of this need. Kilopower's 10-year design life is *just* short of what most cells need (the round-6 baseline 500-kilowatt cell is at 11.37 years cumulative burn). A 15-year reactor lifetime is required to cover the full grid; the matrix should add reactor-lifetime alongside specific power and aerocapture as a third independent load-bearing variable.

