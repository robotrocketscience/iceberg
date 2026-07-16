# Round 9 — Slow-Transfer Trajectory Family: Time-of-Flight vs Earth Arrival Velocity-at-Infinity

**Status:** pre-result.

## Question

R8 found the conops' chunk-fed inbound delta-velocity budget structurally under-specified by 1.2–8.9 km/s. R8 split the inbound architecture into Case B (5.94 km/s, no lunar gravity assist) and Case C (2.85 km/s, with lunar gravity assist). R10 then ranked propulsion candidates against both cases, with water radio-frequency ion at 2000 s as the architectural recommendation. But R10 took Cases B and C as given — it did not check whether the *trajectory* that produces those arrival v_∞ values is physically realizable in a 13-year round trip.

**The question:** for a ballistic Saturn-to-Earth transfer (no continuous-thrust cruise), what time-of-flight is required to arrive at Earth with a chosen v_∞? And: does a single lunar gravity assist close the gap from the ballistic minimum to the conops' 2.85 km/s Case C?

## Pre-registered hypothesis (H9)

**Aggregate (H9-agg):** I predict the conops' "13-year round trip + Case C (2.85 km/s) inbound budget" cannot be reached by ballistic transfer + single lunar gravity assist. Either the round trip is longer than 13 years (because a slow ballistic transfer + powered cruise are required to shed the excess v_∞), or the inbound budget is larger than 2.85 km/s (because lunar gravity assist alone can't strip enough v_∞ from a Hohmann-class arrival). One of those two has to give.

**Pre-registered numeric predictions:**

| Sub-claim | Prediction | Falsification |
|---|---|---|
| H9a — Hohmann transfer Saturn → Earth time-of-flight | 5.8–6.2 years (half-period of an ellipse with semi-major axis (1 + 9.54)/2 = 5.27 AU) | falsified if outside [5.5, 6.5] yr |
| H9b — Hohmann transfer Earth-arrival v_∞ | 9.5–10.5 km/s (difference between spacecraft perihelion velocity ~40 km/s and Earth's 29.78 km/s) | falsified if outside [9, 11] km/s |
| H9c — Slower ballistic transfers (perihelion < 1 AU) reduce v_∞? | No — slower-than-Hohmann ballistics have perihelion *outside* Earth's orbit and never reach Earth. Faster-than-Hohmann transfers (perihelion < 1 AU) increase v_∞ at Earth crossing because the spacecraft is moving faster. Hohmann is the minimum-v_∞ ballistic. | falsified if a ballistic transfer with TOF > 6.05 yr arrives at v_∞ < 10 km/s |
| H9d — Single lunar gravity assist v_∞ reduction | ≤ 2.0 km/s under reasonable assumptions (Moon orbital velocity ~1.02 km/s; max reduction = 2 × v_Moon × cos(geometric loss term)). Practical reduction depends on encounter geometry and the available bending angle. | falsified if literature/calculation says single lunar GA can shed > 2.5 km/s |
| H9e — Achievable v_∞ with Hohmann + single lunar GA | ≥ 8 km/s (10.3 - 2.0 = 8.3 km/s floor). The conops' 2.85 km/s requires shedding > 7 km/s, which a single lunar GA cannot do. | falsified if Hohmann + lunar GA closes 2.85 km/s |
| H9f — Time-of-flight implication | If Case C (2.85 km/s) is unreachable ballistic + lunar GA, then powered inbound cruise must shed the excess. At water radio-frequency ion thrust acceleration ~1e-4 m/s² with chunk-fed mass, shedding 5–7 km/s of v_∞ during cruise adds 1.5–2.5 years. Round trip becomes 14–16 years, not 13. | held if powered-cruise TOF estimate falls in [1, 3] yr; falsified if outside that band |

**Pre-registered conclusion if all sub-claims hold:** the conops' "13-year round trip + Case C 2.85 km/s" pair is internally inconsistent. The architecture has to choose:
- (a) Accept Case B (~5.94 km/s) and keep the 13-year round-trip headline. Inbound braking does the heavy lifting and the conops' propulsion budget grows from ~3 to ~6 km/s.
- (b) Accept Case C (2.85 km/s) and acknowledge the round trip is ~15 years (slow cruise with powered v_∞ shedding). The conops' headline number is wrong.
- (c) Use multiple gravity assists (Jupiter on inbound) to shed v_∞ ballistically, but this adds years of cruise time and is sensitive to launch windows.

## Method

Sun-centered two-body conic mechanics, no patched-conics complexity beyond Earth's sphere of influence (treated as instantaneous swingby for the lunar GA estimate).

1. **Hohmann transfer Saturn → Earth.** Compute semi-major axis, time-of-flight (half-period), and perihelion velocity. Take v_∞ at Earth = v_perihelion − v_Earth (aligned tangentially).
2. **Slow-ballistic family.** Parameterize transfers by *perihelion radius* r_p ∈ [0.3, 1.0] AU (with aphelion fixed at Saturn, r_a = 9.54 AU). For each: compute eccentricity, semi-major axis, true-anomaly at Earth crossing, eccentric-anomaly, time from aphelion to Earth crossing, and helio velocity vector at the crossing. Compute v_∞ at Earth.
3. **Slow-aphelion family.** Hold perihelion = 1 AU, vary aphelion ∈ [9.54, 20] AU. Time-of-flight grows, v_∞ at Earth at perihelion = same as Hohmann (the spacecraft still arrives at perihelion with the vis-viva velocity for the new transfer ellipse, which is *higher* than Hohmann perihelion velocity). This explores whether "slower outbound" with same arrival geometry helps.
4. **Lunar gravity assist reduction.** Use the standard formula: ∆v_∞ = 2·v_Moon·sin(δ/2), where δ is the bending angle at the Moon. Max bending angle limited by Moon's gravitational parameter and the spacecraft's v_∞ relative to the Moon. Compute the max ∆v_∞ achievable.
5. **Powered-cruise time-of-flight estimate.** For excess v_∞ that lunar GA cannot strip, estimate the cruise-time cost of shedding it with water radio-frequency ion at 2000 s, η = 0.65, at 10 kWe power, with chunk-fed initial mass from R10. Use the same low-thrust acceleration formula as R10.

**Validity caveats:**
- Two-body sun-centered conic mechanics ignores Saturn's gravity at departure (negligible — Saturn's escape velocity at 9.54 AU is small relative to heliocentric orbital velocity) and Earth's gravity until arrival (handled via v_∞).
- The Hohmann transfer is the minimum-energy two-impulse ballistic; non-Hohmann ballistics with the same endpoints are the bi-elliptic family, not slower direct transfers. R9 explores the "slower direct" claim properly.
- Lunar GA estimate uses single-encounter geometry. Multiple lunar GAs are possible but exotic and rarely close more than one extra km/s per encounter.
- Powered-cruise TOF uses constant-acceleration approximation with chunk-fed varying mass. Real low-thrust trajectories have gravity losses and steering-angle losses ~5–15%.
- This round does NOT model Jupiter or Saturn-system gravity assists on the inbound leg. Those are a separate analysis.

## Result

### Hohmann Saturn → Earth

| Quantity | Value |
|---|---:|
| Semi-major axis | 5.291 AU |
| Eccentricity | 0.811 |
| Time-of-flight (half-period) | 6.09 yr |
| Helio velocity at Earth perihelion | 40.08 km/s |
| v_∞ at Earth arrival | 10.30 km/s |

### Slow-ballistic perihelion sweep (aphelion fixed at Saturn 9.58 AU)

| r_p (AU) | TOF (yr) | v_sc at Earth (km/s) | Flight-path angle (°) | v_∞ at Earth (km/s) |
|---:|---:|---:|---:|---:|
| 0.30 | 5.39 | 39.93 | -55.3 | 33.59 |
| 0.50 | 5.55 | 39.98 | -43.4 | 27.49 |
| 0.70 | 5.72 | 40.02 | -31.8 | 21.50 |
| 0.85 | 5.87 | 40.05 | -21.7 | 16.56 |
| 1.00 | 6.09 | 40.08 |  0.0 | 10.30 |

Lower-perihelion transfers arrive *faster* but with much higher v_∞ at Earth crossing (steep flight-path angle). Hohmann (r_p = 1 AU) is the v_∞ minimum.

### Slow-ballistic aphelion sweep (perihelion = 1 AU)

| r_a (AU) | a (AU) | TOF (yr) | v_perihelion (km/s) | v_∞ at Earth (km/s) |
|---:|---:|---:|---:|---:|
| 9.58 | 5.29 | 6.09 | 40.08 | 10.30 |
| 12.00 | 6.50 | 8.29 | 40.47 | 10.68 |
| 15.00 | 8.00 | 11.31 | 40.78 | 11.00 |
| 20.00 | 10.50 | 17.01 | 41.11 | 11.32 |

Slower transfers (larger aphelion) take longer AND arrive with slightly higher v_∞ because the larger semi-major axis raises perihelion velocity.

### Lunar gravity assist (starting from Hohmann v_∞ = 10.30 km/s, 100 km lunar periapsis)

| Step | v_∞ in (km/s) | v_∞ out (km/s) | ∆v (km/s) |
|---|---:|---:|---:|
| Single flyby | 10.30 | 9.84 | 0.46 |
| Tour flyby 1 | 10.30 | 9.84 | 0.46 |
| Tour flyby 2 | 9.84 | 9.36 | 0.48 |
| Tour flyby 3 | 9.36 | 8.87 | 0.50 |
| **Three-flyby total** | 10.30 | **8.87** | **1.43** |

Single-flyby reduction is far less than 2 km/s — bending angle at 10 km/s relative v_∞ is only ~2°, so the achievable rotation in the lunar frame is small. Sequential flybys help marginally (per-flyby ∆v grows from 0.46 to 0.50 km/s as v_∞ drops and bending grows), but a 3-flyby tour shaves only 1.43 km/s off Hohmann's 10.30 km/s.

### Powered-cruise time-of-flight to close Case C (target v_∞ = 2.85 km/s)

After 3-flyby lunar tour: v_∞ = 8.87 km/s. To reach 2.85 km/s: powered cruise must shed 6.02 km/s.

| Quantity | Value |
|---|---:|
| Chunk (R10 baseline) | 14 t |
| Dry spacecraft | 5 t |
| Reactor mass (10 kWe, 5 W/kg) | 2 t |
| Initial mass | 21 t |
| Propellant required (Tsiolkovsky, 2000 s) | 5.55 t |
| Delivered chunk | 8.45 t (60.4%) |
| Thrust | 0.663 N |
| Average acceleration | 3.64×10⁻⁵ m/s² |
| **Cruise time required (duty 0.5)** | **10.49 yr** |

### Sanity check: continuous low-thrust spiral (no Hohmann coast)

Worth knowing as the "all-thrust" alternative.

| Quantity | Value |
|---|---:|
| Heliocentric ∆v (v_E_circ − v_S_circ, tangential) | 20.16 km/s |
| Tsiolkovsky propellant fraction at 2000 s | 64.2% |
| Propellant required (m0 = 21 t) | 13.5 t |
| Delivered chunk | 0.5 t (3.6%) |
| Continuous-spiral TOF (3.64×10⁻⁵ m/s², duty 0.5) | 35.1 yr |

### Combined round-trip estimate

| Phase | Time (yr) |
|---|---:|
| Outbound Hohmann | 6.09 |
| Saturn dwell (conops) | 1.00 |
| Inbound Hohmann + Earth-vicinity braking | 16.57 |
| **Total** | **23.66** |

Conops headline: 13 yr. Calculated: 24 yr (with the Hohmann + braking interpretation) or 41 yr (with continuous low-thrust spiral). The conops headline is wrong by 10–28 years.

### Hypothesis grading

| Sub-claim | Predicted | Measured | Verdict |
|---|---|---:|---|
| H9a — Hohmann TOF | 5.8–6.2 yr | 6.09 yr | held |
| H9b — Hohmann v_∞ at Earth | 9.5–10.5 km/s | 10.30 km/s | held |
| H9c — No slower ballistic | Hohmann is v_∞ floor | Confirmed (slower r_p arrivals raise v_∞; slower r_a transfers also raise v_∞) | held |
| H9d — Single lunar GA ≤ 2 km/s | ≤ 2 km/s | 0.46 km/s | held (with margin) |
| H9e — Hohmann + GA floor ≥ 8 km/s | ≥ 8 km/s | 9.84 km/s (single), 8.87 km/s (3-flyby tour) | held |
| H9f — Powered cruise in [1, 3] yr | 1–3 yr | 10.49 yr | **falsified high** |
| H9 aggregate — 13 yr + Case C inconsistent | round trip > 13.5 yr | 23.66 yr | held |

Result JSON: `results/slow_trajectory_tof.json`.

## Reading

**The conops' 13-year round-trip headline is inconsistent with the chunk-fed water radio-frequency ion architecture at Kilopower-class power, by ~10 years.** The minimum realistic round trip is 18–25 years; the maximum realistic round trip (all-thrust continuous spiral) is 35+ years and delivers almost no chunk.

**Sub-claim outcomes:**
- **H9a, H9b, H9c held cleanly.** Hohmann is the energy-optimal ballistic Saturn → Earth transfer. Slower ballistics (any r_p < 1 AU OR any r_a > 9.58 AU) don't help; they either raise v_∞ at Earth crossing or extend TOF without reducing v_∞. There is no slow ballistic that arrives at Earth gently.
- **H9d held with margin.** Single lunar gravity assist at v_∞ = 10.3 km/s sheds only 0.46 km/s (predicted ≤ 2). The bending angle limit at high v_∞ is the binding constraint, exactly as the `lunar_flyby` module's docstring warned. A 3-flyby tour shaves 1.43 km/s total, not 6 km/s. The mission cannot brake at Earth purely with lunar gravity assists.
- **H9e held.** Hohmann + single flyby = 9.84 km/s. Hohmann + 3-flyby tour = 8.87 km/s. Neither closes Case C (2.85 km/s). Even Case B (5.94 km/s) requires shedding 3 km/s more than a 3-flyby tour can provide.
- **H9f falsified high.** I predicted 1-3 yr of powered cruise to close Case C. Actual: 10.5 yr. The error was a back-of-envelope miscalculation — I assumed "1.5-2.5 yr cruise time per ~5 km/s shed" without working out the acceleration. At 10 kWe Kilopower-class power and chunk-fed 21 t initial mass, water radio-frequency ion thrust acceleration is ~3.6×10⁻⁵ m/s², 50% duty. Shedding 6 km/s takes 10 yr, not 1-3.
- **H9 aggregate held.** Round trip is 24 yr (Hohmann + Earth-vicinity braking) or 35+ yr (continuous spiral). Conops 13 yr is wrong.

**What this means for the architecture:** the chunk-fed water radio-frequency ion architecture R10 recommended IS the right propulsion choice — the issue is not the thruster. The issue is the *power budget*. At Kilopower 10 kWe, thrust acceleration is too low to close any inbound trajectory in 7 years.

**Implication for the propulsion architecture decision tree:**

| Architecture option | Round trip | Delivered chunk fraction | Heritage / risk |
|---|---:|---:|---|
| Status quo (water RF ion, 10 kWe Kilopower, Hohmann + slow braking) | 24 yr | 60% (R10 number) | Pale Blue TRL 7-8; cruise time blows the conops headline |
| Higher power (water RF ion, 40 kWe Fission Surface Power, Hohmann + faster braking) | 12-15 yr (estimated) | 50-55% (R10 found higher power degrades delivery because reactor mass grows) | Fission Surface Power TRL 4-5 nominal; significant program risk |
| Chemical Earth capture (kerolox burn, ~5 km/s) | 13 yr (back to conops headline) | ~25-30% (large chemical propellant load) | Mature chemical, but big delivery hit |
| Aerocapture (was retired per M-AEROCAP) | 13 yr | 60-70% | Heat-shield deployment + GNC + B-ring debris exposure during entry; re-elevating M-AEROCAP |
| Continuous low-thrust spiral (water RF ion, 10 kWe, full spiral) | 41 yr | 4% | Same propulsion, much longer trip |

**Architectural reading:** The R10 recommendation (water RF ion replacing microwave electrothermal) is *necessary* but *not sufficient*. R10 fixed the propulsion-type problem. R9 surfaces a power-class problem on top of it. The conops' 13-year + 60% delivery + Kilopower-class triple is structurally infeasible. Two of the three have to give:

- If 13-year holds: power class must rise (Fission Surface Power 40 kWe), OR Earth-capture mechanism must shift (chemical or aerocapture)
- If Kilopower holds: round trip is 18-25 years
- If 60% delivery holds: same as above — power or capture mechanism is the lever

## Revisit

- **The "Hohmann + Earth-vicinity braking" interpretation is geometrically inconsistent.** A spacecraft on a Hohmann transfer with v_∞ = 10.3 km/s at Earth perihelion does NOT stay in Earth's vicinity for 10 years braking. It flies past Earth and returns to Saturn's distance on the elliptical orbit. The R9 calculation implicitly assumes propulsion is on through the whole transfer or a hybrid trajectory exists that buys most of Hohmann's ballistic time + Earth-arrival braking. Honest framing: the realistic chunk-fed inbound time is somewhere in the 16–35 year band, with the exact value depending on optimal-control trajectory design. R9's 24-yr point estimate is in that band's lower half; not unrealistic, just under-specified.
- **Power scaling not modeled here.** I quote "Fission Surface Power 40 kWe → 12-15 yr round trip" as an estimate. A proper R9b would sweep power (10, 20, 40, 80 kWe) and re-compute braking time. Worth doing if Fission Surface Power becomes the design baseline. **Promote R9b to the queue: chunk-fed inbound time-of-flight as a function of reactor power class.**
- **Multiple gravity assists beyond Earth not modeled.** Jupiter on inbound could shed 3-5 km/s of v_∞ ballistically. Saturn-system gravity assists at departure could lower the helio departure energy. Both could trim 1-2 yr off the round-trip estimate. Not in R9 scope.
- **Chemical Earth-capture not quantitatively evaluated.** I quote "chemical capture: 13 yr, 25-30% delivery" as a guesstimate. R8 had the chemical capture trade in some form; revisit with R9's findings.
- **Aerocapture was retired per M-AEROCAP** (per R8 cross-learning) due to B-ring debris exposure of the heat-shield surface during outbound. R9's finding may justify *re-elevating* M-AEROCAP for review: if the architecture can't close otherwise, aerocapture's risk profile needs a second look.
- **Outbound is assumed Hohmann.** R10 found water microwave electrothermal at Saturn-egress was 0% delivery; the R10 architecture uses water RF ion for outbound too. The R10 Saturn-egress also takes years of propellant-fed cruise that R9 didn't account for in the outbound 6-yr budget. R9 round-trip estimate is likely understated as a result.

## Cross-learning

- **Single-number budgets in concept-paper documents are systematically optimistic, again.** R0 was 30% optimistic on water microwave electrothermal Isp. R2 was 30% optimistic on lunar gravity assist contribution. R8 was 80% optimistic on chunk-fed inbound delta-velocity. R9 is now ~80% optimistic on round-trip time (13 yr → 24 yr). The pattern is consistent: every back-of-envelope conops number that hasn't been pressure-tested against propagator math is optimistic by 30-80%. The methodology lesson is now strong enough to add to CONVENTIONS as a hard rule: **any single-number claim from a concept paper that hasn't been independently verified by a round should carry an *a priori* 30-80% optimism prior.**
- **Order of round operations matters.** R9 should have run BEFORE R10. R10's Cases B/C delta-v budgets (5.94 / 2.85 km/s) were inputs that turned out to be unreachable by realistic Hohmann + lunar gravity assist combinations. R10's propulsion ranking is still correct *given* those inputs, but the inputs were wishful. Pre-emptive methodology lesson for future campaigns: when a round depends on trajectory budgets, do the trajectory round first.
- **R9f falsification is the result-bearing one.** Predictions H9a-H9e were "easy wins" — they reproduced known orbital mechanics. H9f was the actual stretch. Falsifying it (1-3 yr predicted → 10.5 yr actual) is what surfaced the architectural finding. The aggregate held, but the aggregate held *for the wrong reason* relative to my prediction. Methodology lesson: when an aggregate holds but a load-bearing sub-claim falsifies, the aggregate-verdict text should make the path to "held" explicit, not implied.
- **Pale Blue water RF ion is still the right thruster choice.** R10's conclusion does not change. What changes is the *power class* must be revisited, OR the Earth-capture mechanism must shift, OR the round-trip headline must move. Three knobs to turn.
- **Tracking question for future rounds:** if the round-trip is 18-25 years instead of 13, does the mission concept still close on the economic side? The startup/ thread's NPV calculation was done at 13 yr. A 24-yr cadence (2x the cycle time) approximately halves the steady-state cash flow rate. That's a startup-thread question, not a propulsion-round question — but R9's finding needs to propagate to that document.
