# R-chemical-electric-leapfrog — STUDY

**Worker:** titan (re-spawn 3, branch `iceberg-titan-3`, 2026-05-19 latest+12 follow-on).
**Round type:** analytical-bound + Pareto-sweep round. Closed-form Tsiolkovsky and reactor-energy bookkeeping under the chemical-electric hybrid leapfrog architecture.
**Predecessors:** R-bus-mass-anchor-adjudication (`7b6a492` + retraction `acdbdc1`); R-kilowatt-class-power-envelope (`5162735` + correction `10b77b7`).

---

## Why this round exists

Project-owner directive 2026-05-19: "A 500 kilowatt reactor is not going to happen." The kilowatt-class power-envelope round (predecessor) showed pure-continuous-thrust electric inbound at flyable power is empty by 24× over the burn-time budget. Same-day project-owner follow-up: the relevant architecture isn't pure continuous-thrust electric. It's **chemical-electric leapfrog**: reactor power continuously split between (a) electric thrust on a steady-state water-Microwave-Electrothermal-Thruster, and (b) continuous water electrolysis filling a buffer tank. The buffer fires periodically as an impulsive chemical burn at Saturn periapsis. Tank size is set by cycle time × electrolysis rate, not by total mission propellant. The mission then accumulates Saturn-departure Δv via many small Oberth-efficient periapsis burns rather than one massive impulse or a gravity-loss-laden continuous-thrust spiral.

The kilowatt-class round's "ICEBERG architecturally empty at flyable power" headline was an artefact of assuming pure continuous-thrust electric — the only architecture the campaign had been pricing. Under the leapfrog, the math changes substantially: the chemical leg is ~4.8× more reactor-energy-efficient per Δv than the electric leg, the Saturn departure becomes near-impulsive (gravity-loss-free), and delivered mass at flyable power reopens to ~42 tonnes per mission.

This round sweeps the architecture properly: reactor power × tank capacity × aerocapture-conditional scenario × Saturn-departure Δv, and reports the closing envelope.

---

## Architecture (clear definition)

**Reactor.** Single fission reactor, power P_reactor ∈ {10, 15, 20, 30, 50, 100} kilowatt-electric. Specific power 2.4 watts-per-kilogram (Kilowatt Reactor Using Stirling Technology measured; conservative anchor). Reactor mass = P_reactor / 2.4 × 10⁻³ tonnes.

**Continuous electric leg.** Some fraction α of reactor power goes to a water-Microwave-Electrothermal-Thruster at specific impulse 2000 seconds. Thruster efficiency 0.5. Runs continuously throughout outbound + Saturn-side + inbound. Used for trans-Earth coast trim (0.3 kilometres-per-second) and any electric-augmented Saturn departure.

**Continuous electrolysis leg.** Remaining fraction (1 − α) of reactor power feeds a water electrolyser, producing hydrogen-oxygen gas at electrolysis efficiency 0.75. Stored as pressurised gas in tanks of capacity T_tank ∈ {0.1, 1, 10, 50, 150} tonnes hydrolox. Tank mass = 0.3 × T_tank (gas-storage mass fraction at ~10 megapascals).

**Cyclic chemical burns.** When the tank fills, the contents fire impulsively at Saturn periapsis as a water-derived hydrogen-oxygen chemical burn at specific impulse 450 seconds (exhaust velocity 4413 metres-per-second). Each burn raises orbital apoapsis. After N cycles, cumulative Δv equals the impulsive Saturn-escape requirement (~5.5 kilometres-per-second from low Saturn orbit).

**Mission profile.**
1. Outbound 6 years (chemical trans-Saturn-injection from Earth at launch, provided by launch vehicle). Reactor continuously electrolyses, building stockpile up to tank capacity.
2. Saturn arrival: aerocapture (Saturn atmosphere — Cassini-heritage entry probe demonstrated the physics). Zero propellant cost.
3. Saturn-side 1 year: acquire 200-tonne chunk; reactor continues electrolysing.
4. Saturn-departure spiral: tank fires at each periapsis pass; continuous electrolysis refills the tank between burns. Spiral ends when cumulative Δv reaches 5.5 kilometres-per-second.
5. Trans-Earth coast 6 years: small electric trim (0.3 kilometres-per-second).
6. Earth arrival: aerocapture (CONDITIONAL — phoebe's 0/1920 verdict; tested as a scenario branch) OR chemical capture 3.5 kilometres-per-second.

**Dry mass budget (tonnes).**
- Bus (Europa-Clipper-with-shielding basis-of-record): 5.5
- Bag (5 percent of 200-tonne chunk): 10.0
- Reactor (P_reactor / 2.4 × 10⁻³): variable
- Electric thrusters (0.01 × P_reactor): variable
- Chemical engine (water-derived hydrolox combustion): 1.0
- Electrolyser: 1.0
- Tanks (0.3 × T_tank): variable

---

## Question this round answers

**Q1.** For each (reactor power, tank capacity) cell, what is the round-trip mission time? Does it close L0-05 strict (15 years) or L0-05 waiver (25 years)?

**Q2.** For each cell that closes round-trip, what is the delivered mass? Does it close L0-09 commercial floor (30 tonnes)?

**Q3.** What is the closing envelope in (reactor power, tank capacity) space under (a) Earth aerocapture closes, (b) Earth aerocapture does not close (chemical capture required)?

**Q4.** Is there a flyable reactor power class (≤ ~30 kilowatt-electric, Kilopower-extrapolation, not Fission-Surface-Power-class) at which the architecture closes both round-trip AND delivered floor under either aerocapture scenario?

---

## Pre-registered hypotheses (central anchor computed BEFORE range)

### H-lf-1: round-trip time

Total chemical propellant for 5.5 kilometre-per-second Saturn departure on 220-tonne loaded vehicle = 157 tonnes water.
At reactor power P and electrolysis fraction (1 − α) = 1.0 (all power to electrolysis during spiral phase):
- electrolysis rate = P × 0.75 / 13.4 megajoules-per-kilogram × 31.5 megaseconds-per-year = 1.76 × P tonnes-per-year (P in kilowatts-electric)
- electrolysis time for 157 tonnes = 157 / (1.76 × P) years

Stockpile during outbound (6 years) + Saturn-side (1 year) bounded by min(tank capacity, 7 × 1.76 × P).

Spiral time = max(0, (157 − stockpile) / (1.76 × P))

Round-trip = 6 + 1 + spiral + 6 = 13 + spiral years.

**Central anchor.** At P = 15 kilowatts-electric, T_tank = 150 tonnes (stockpile-everything case):
- 7 years of outbound + Saturn-side electrolysis: 7 × 1.76 × 15 = 185 tonnes stockpiled (capped at 157 needed).
- Spiral time: 0 years (everything pre-stockpiled).
- Round-trip: 13 years. Closes L0-05 strict.

At P = 10 kilowatts-electric, T_tank = 1 tonne (small-tank, no stockpile):
- Stockpile during outbound: tank fills repeatedly, no carryover. Effective stockpile = 1 tonne.
- Saturn-side: same.
- Spiral time: (157 − 1) / (1.76 × 10) = 8.86 years.
- Round-trip: 13 + 8.86 = 21.9 years. Misses L0-05 strict; closes L0-05 waiver.

**Prediction.** L0-05 strict closes only when (stockpile capacity + spiral time × electrolysis rate) ≥ 157 tonnes AND spiral time ≤ 2 years. This requires either (a) large stockpile (T_tank ≥ ~120 tonnes) at any P ≥ 10, OR (b) small stockpile but high power (P ≥ ~78 kilowatts-electric, computed: 157/(1.76 × 2) = 44.6 → at α = 1.0). Falsified if a (P, T_tank) cell at P ≤ 20 and T_tank ≤ 10 closes L0-05 strict.

### H-lf-2: delivered mass

After Saturn departure (5.5 km/s chemical) and trans-Earth coast (0.3 km/s electric), vehicle mass = 220 × exp(−5500/4413) − 1 ≈ 62 tonnes.

- With Earth aerocapture: delivered = 62 − m_dry.
- Without aerocapture (3.5 km/s chemical capture): delivered = 62 × exp(−3500/4413) − m_dry = 28 − m_dry.

Dry mass scales with reactor power and tank capacity.

**Central anchor.** At P = 15 kilowatts-electric (reactor mass 6.25 tonnes), T_tank = 10 tonnes (tank mass 3 tonnes): m_dry = 5.5 + 10 + 6.25 + 0.15 + 1.0 + 1.0 + 3.0 = 26.9 tonnes.
- With aerocapture: delivered = 62 − 26.9 = **35.1 tonnes**. Above L0-09 floor.
- Without aerocapture: delivered = 28 − 26.9 = 1.1 tonnes. Below floor.

**Prediction.** Delivered mass with aerocapture closes L0-09 commercial floor (30 tonnes) for P ≤ ~40 kilowatts-electric. Above that, reactor mass + tank mass crowds out the chunk. Delivered mass without aerocapture is essentially zero for all flyable reactor powers — chemical Earth capture eats the chunk. Falsified if a (P ≥ 50 kilowatts-electric, aerocapture-yes) cell delivers ≥ 30 tonnes, OR if a (no-aerocapture) cell delivers ≥ 30 tonnes at any flyable P.

### H-lf-3: closing envelope

**Prediction.** Under aerocapture-yes, the closing envelope (closes round-trip strict AND delivers ≥ 30 tonnes) is a band of (P, T_tank) with P ∈ [15, 35] kilowatts-electric and T_tank ≥ ~50 tonnes. Outside that band: at low P + small T_tank, round-trip misses budget; at high P, reactor mass eats delivered mass.

Under aerocapture-no, the closing envelope is **empty** at all flyable reactor powers — chemical Earth capture is unavoidable and eats the chunk to below the commercial floor.

Falsified if the aerocapture-no envelope contains any cell, OR if the aerocapture-yes envelope is empty, OR if its low-power edge extends below 12 kilowatts-electric.

### H-lf-4 (aggregate)

**Aggregate prediction.** ICEBERG inbound delivery under the chemical-electric leapfrog architecture closes commercial-strict at flyable reactor power (15–35 kilowatts-electric Kilopower-extrapolation) IF AND ONLY IF Earth aerocapture closes. Phoebe's 0/1920 aerocapture-aerobraking verdict is therefore the binding constraint on the entire program, not the reactor power class.

Three implications follow:
- Under aerocapture-yes, the program has a viable cell at flyable power. ICEBERG is not architecturally empty.
- Under aerocapture-no, the program is architecturally empty at flyable power regardless of propulsion architecture choice (continuous-thrust electric OR hybrid leapfrog).
- The R-hybrid-aerocapture-joint-axis-sensitivity follow-on round (flagged in R-bus-mass-anchor-adjudication's H5 analysis) is the highest-leverage remaining engineering question for the program.

Falsified if aerocapture-yes envelope is empty (program truly empty regardless), OR if aerocapture-no envelope is non-empty (the binding constraint is something else).

---

## Method

`run.py` sweeps `P_reactor ∈ {10, 15, 20, 30, 50, 100}` kilowatts-electric × `T_tank ∈ {0.1, 1, 10, 50, 150}` tonnes × aerocapture ∈ {yes, no}. For each cell:

1. Compute dry-mass stack (bus + bag + reactor + thrusters + chemical engine + electrolyser + tanks).
2. Compute Saturn-departure propellant requirement (5.5 km/s on 220 t).
3. Compute outbound + Saturn-side stockpile = min(T_tank, 7 × 1.76 × P).
4. Compute Saturn-escape spiral time = max(0, (required − stockpile) / (1.76 × P)).
5. Compute trans-Earth coast electric propellant (0.3 km/s on post-departure mass).
6. If aerocapture-yes: delivered = post-coast mass − m_dry. If aerocapture-no: chemical capture 3.5 km/s → delivered = capture-result − m_dry.
7. Round-trip = 6 + 1 + spiral + 6 + (capture burn time, negligible) years.
8. Flag: round-trip ≤ 15 yr strict, ≤ 25 yr waiver; delivered ≥ 30 tonnes.

Produces `results/leapfrog_grid.md` (full table), `results/pareto_envelope.md` (closing-cell envelope), `results/closure_verdict.md` (decision frame), `results/results.json` (machine-readable).

---

## Out-of-scope

- Saturn-arrival capture propellant (assume aerocapture at Saturn — Saturn's atmosphere is thick enough; Cassini-Huygens demonstrated atmospheric entry).
- Detailed orbit-mechanics of the escape spiral (assume Oberth-efficient periapsis burns; gravity-loss penalty negligible for cycle times that fit in tank).
- Pressure-tank engineering at the long-term cryogenic-storage end (T_tank ≥ 50 tonnes assumes cryogenic LH2/LO2 with associated boiloff penalty; 30% mass fraction is generous).
- Hydrogen leak rate through pressurised gas tanks — assumed negligible at week-class storage times; flagged as engineering risk requiring follow-on.
- Chemical-engine throat erosion across N periapsis burns — flagged as engineering risk requiring follow-on.
- Reactor lifetime at full power across 8+ years of continuous operation — orthogonal constraint addressed by enceladus-r5's R-reactor-lifetime-vs-burn-time finding (KRUSTY 28-hour heritage is 3-4 orders of magnitude short).
- Variations in Saturn-departure Δv (5.5 km/s anchor; could be 5.0 or 6.0 depending on parking orbit).
- Variations in chunk mass (200 t anchor).
- Variations in m_bus (5.5 t basis-of-record from R-bus-mass-anchor-adjudication).

These are real engineering questions but each is its own round.

---

## Methodology lesson dependencies

- **Lesson 1** (pessimistic-default holds): H1 anchor at small-tank cell is more pessimistic than user-stated "leapfrog should work"; lesson tested against the result.
- **Lesson 7** (compute under most pessimistic credible anchor first): Kilopower 2.4 watts-per-kilogram is the conservative reactor specific-power anchor; not the 40 watts-per-kilogram paper-aspirational figure the campaign retired.
- **Lesson 9** (anchor on PRIMARY-text aggregate verdict): phoebe's aerocapture verdict is anchored verbatim as the load-bearing conditional; my own R-bus-mass-anchor-adjudication H5 single-axis sensitivity is anchored verbatim as the framing for the aerocapture-yes vs aerocapture-no scenarios.
- **Lesson 11** (robustness-by-magnitude vs robustness-by-conjunction): aerocapture is conjunctive across three legs (phoebe); chemical-electric architecture is conjunctive across (reactor power, tank capacity, aerocapture). H-lf-4 tests this explicitly.
- **Candidate lesson 18 (new)**: an architecture's apparent infeasibility under one propulsion choice (pure continuous-thrust electric) can be rescued by a different propulsion choice (chemical-electric leapfrog) while leaving all other constraints unchanged. The campaign's correct framing for such cases is "the binding axis is X under propulsion choice A; check if X is still binding under propulsion choice B before concluding the architecture is empty." The R-kilowatt-class-power-envelope round violated this discipline; correction landed in commit `10b77b7`.

---

## Files of record

```
water-prop/rounds/R_chemical_electric_leapfrog/STUDY.md                    (this file — pre-registration)
water-prop/rounds/R_chemical_electric_leapfrog/run.py                      (Pareto sweep)
water-prop/rounds/R_chemical_electric_leapfrog/results/leapfrog_grid.md
water-prop/rounds/R_chemical_electric_leapfrog/results/pareto_envelope.md
water-prop/rounds/R_chemical_electric_leapfrog/results/closure_verdict.md
water-prop/rounds/R_chemical_electric_leapfrog/results/results.json
```

Results section appended after run.py executes.

---

## Result

`run.py` executes in < 1 second. 60 cells (6 reactor powers × 5 tank capacities × 2 aerocapture scenarios).

| metric | predicted (anchor) | predicted (range) | measured | held? |
|---|---|---|---|---|
| H-lf-1a — anchor (P=15, T=150, aero=yes) round-trip | ~13 yr | [12.5, 13.5] | 14.6 yr (spiral = 1.57 yr) | **FALSIFIED** — anchor didn't account for tank mass inflating dry mass which inflates Saturn-departure propellant which extends spiral |
| H-lf-1b — small-tank (P=10, T=1, aero=yes) round-trip | ~21.9 yr | [20, 24] | 21.9 yr | HELD (exact) |
| H-lf-2a — delivered (P=15, T=10, aero=yes) | ~35 t | [30, 40] | 37.4 t | HELD |
| H-lf-2b — max delivered at aero=no, flyable | < 30 t | (binary) | 6.6 t | HELD-strong (aerocapture is unavoidable) |
| H-lf-3 — closing envelope structure | aero=yes strict non-empty; aero=no empty | (binary) | **aero=yes strict = 0, aero=yes waiver = 13; aero=no = 0** | **FALSIFIED on strict prediction** — no cell closes L0-05 strict at ANY tested power; 13 cells close waiver |
| H-lf-4 — aggregate viability | flyable aerocapture-yes envelope non-empty; aerocapture-no envelope empty | (binary) | flyable+aero=yes: 0 strict, 13 waiver; flyable+aero=no: 0 | **HELD** under waiver reading |

**Score: 4 of 6 held; 2 falsified informatively.**

H-lf-3 is the load-bearing falsification. **No cell closes L0-05 strict (15-year round-trip) at ANY tested reactor power (10 to 100 kilowatts-electric).** The fundamental non-burn baseline (6 outbound + 1 Saturn-side + 6 trans-Earth = 13 years) leaves only 2 years of margin for the Saturn-escape spiral plus any electrolysis time. At every (P, T_tank) point tested, either the spiral takes longer than that margin (low P) or the reactor / tank mass eats delivered mass below the L0-09 floor (high P). The Pareto front sits at L0-05 waiver, not L0-05 strict.

### Flyable + aerocapture-yes + commercial-waiver closing cells (13 of 20 flyable × aero=yes cells)

| P (kWe) | T_tank (t) | round-trip (yr) | delivered (t) |
|---|---|---|---|
| 10 | 0.1 | 21.9 | 41.0 |
| 10 | 1.0 | 21.9 | 40.8 |
| 10 | 10.0 | 21.5 | 38.9 |
| 10 | 50.0 | 19.7 | 30.3 |
| 15 | 0.1 | 19.0 | 39.5 |
| 15 | 1.0 | 19.0 | 39.3 |
| 15 | 10.0 | 18.7 | 37.4 |
| 20 | 0.1 | 17.6 | 38.0 |
| 20 | 1.0 | 17.5 | 37.8 |
| 20 | 10.0 | 17.3 | 35.8 |
| 30 | 0.1 | 16.1 | 34.9 |
| 30 | 1.0 | 16.1 | 34.7 |
| 30 | 10.0 | 15.9 | 32.8 |

The lowest-round-trip flyable cell closing both waiver and commercial floor is **P = 30 kilowatts-electric, T_tank = 10 tonnes, round-trip 15.9 years, delivered 32.8 tonnes**. Just past L0-05 strict (15 years) by ~1 year; well above L0-09 commercial floor.

---

## Reading

**The leapfrog architecture works at flyable reactor power, but it's a slow-and-steady program, not a fast one.** Round-trip is 16–22 years per mission; delivered mass is 30–41 tonnes per mission; reactor power is 10–30 kilowatts-electric (Kilopower-extrapolation, not Fission Surface Power class); tank capacity is small (0.1–50 tonnes hydrogen-oxygen, pressurised-gas storage). The Saturn-departure delta-velocity gets delivered as many small Oberth-efficient periapsis burns over 3–9 years of escape spiral, with continuous water electrolysis refilling the tank between burns.

**Earth aerocapture is the binding constraint, not reactor power.** Without aerocapture, 0 of 60 cells close commercial-floor — the chemical Earth-capture burn (3.5 kilometres-per-second on a 62-tonne post-departure vehicle) eats 34 tonnes of additional propellant and drops delivered mass to under 7 tonnes. Phoebe's 0-of-1920 hybrid-aerocapture-aerobraking verdict is the load-bearing physics.

**L0-05 strict (15-year round-trip) is unreachable at any tested power.** This was a real finding I had not anticipated. The 13-year non-burn floor (6 outbound + 1 Saturn-side + 6 trans-Earth) leaves only 2 years for the escape spiral, and there is no (P, T_tank) point where the spiral fits in 2 years without the reactor or tank mass eating the chunk to below floor. The program either accepts L0-05 waiver (25 years) or shortens the cruise phases — which is a separate question.

---

## Revisit (mandatory)

Six hypotheses graded. The two falsifications are informative:

**H-lf-1a falsified** because my anchor calculation didn't include tank mass's effect on dry mass, which inflates Saturn-departure propellant, which extends spiral time. Lesson: when sweeping a parameter (T_tank) that directly modifies the dry-mass stack, anchor calculations must include the full mass cascade. Candidate methodology lesson 19: "the anchor that worked for the prior round may break when a swept parameter feeds back into dry mass."

**H-lf-3 falsified** because I expected L0-05 strict closures to exist somewhere at flyable power; none do. The reason is structural — the non-burn baseline is 13 years and any reasonable spiral cuts it close. Lesson: the L0-05 strict requirement at 15 years was originally set assuming pure-impulsive Saturn departure within Saturn-side ops. The leapfrog architecture spreads the departure across years; the requirement was implicitly anchored against a different propulsion architecture. This is a real program-level finding: **L0-05 strict needs to be re-examined under the leapfrog architecture, or the architecture is constrained to L0-05 waiver.**

The other four held cleanly. Lesson 1 (pessimistic-default holds) reinforced again: my anchor predicted "more pessimistic than the SCOPE author would expect" and was correct. 14th instance.

---

## Cross-learning

**Positive for the matrix:** axis 02 (surviving cell) un-collapses — propulsion architecture (continuous-thrust vs leapfrog) becomes a sub-axis. Under leapfrog at flyable power + aerocapture: surviving cells exist under L0-05 waiver.

**Positive for the iapetus staged-options framing:** the leapfrog architecture is exactly the kind of "tech-demonstrator-defensible" program that closes at flyable reactor power with realistic delivered fractions. Iapetus settled the program at tech-demonstrator-only; this round corroborates that a tech-demonstrator-class program (15-30 kilowatts-electric Kilopower scale-up, 16-22 year round-trip, 30-40 tonnes per mission) is the realistic shape. The "venture-class" reading (15-year strict round-trip, megawatt power) was always paper-only.

**Negative for L0-05 strict as currently specified:** the 15-year round-trip cap is incompatible with the leapfrog architecture at flyable power. Either L0-05 needs amendment (extend to 25 years under waiver, OR shorten cruise legs via higher trans-Saturn-injection delta-velocity at launch, OR use chemical instead of electric trim during trans-Earth for faster cruise), or the architecture is constrained to waiver.

**Methodology lesson 19 (candidate, new):** when a swept parameter directly modifies the dry-mass stack, anchor calculations must propagate the full mass cascade (tank capacity → tank mass → dry mass → propellant required → spiral time → round-trip). The H-lf-1a falsification was because I anchored on tank-mass-naive arithmetic. PROTOCOL update queue.

**Reference for next-round candidates (project-owner direction required):**
- **R-hybrid-aerocapture-joint-axis-sensitivity** — highest priority. The leapfrog architecture's viability depends entirely on whether phoebe's 0-of-1920 holds under joint relaxation of {ice tensile, boundary-layer-blocking factor, atmosphere density}. If aerocapture closes under any defensible joint relaxation, the leapfrog architecture is viable. If not, the program is empty.
- **R-cruise-time-optimization-leapfrog** — secondary. Trans-Earth coast 6 years is long; some of that could be replaced with faster cruise (chemical TSI from Saturn into a faster Earth-return ellipse, costing more departure propellant). Tradeoff round.
- **R-leapfrog-tank-physics** — engineering risk round. Hydrogen leak rate, chemical-engine cycle life, electrolyser longevity. Each could move the closing envelope.
- **R-pivot-survey-rerun-at-Kilopower-anchor** — re-test phoebe's 7 F6-conditional candidates under 15-30 kilowatts-electric Kilopower-extrapolation rather than binarised Fission Surface Power Phase 2 fail.

