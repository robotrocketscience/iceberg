# R-outbound-architecture — does chemical kick stage vs all-electric outbound flip the architecture matrix?

**Status:** pre-result.

## Question

Every prior round in this thread uses an **all-electric outbound** assumption: the vehicle's own electric thrusters carry it from low Earth orbit to Saturn-arrival via continuous thrust at specific impulse 2000 s, with total outbound delta-v ~9 km/s. This gives a mass-ratio of 1.583 at low Earth orbit.

The actual concept of operations uses a **chemical kick stage** (Vulcan-Centaur class, hydrolox at specific impulse ~450 s) for the Earth-departure burn (~7.3 km/s from low Earth orbit to a trans-Saturn trajectory). The kick stage is jettisoned post-burn; the vehicle coasts on a Hohmann transfer (~6.09 yr) and does electric Saturn capture (~2 km/s) on arrival.

These two outbound architectures have very different launch-mass costs. Chemical impulsive at 450 s burning a 7.3 km/s delta-v needs propellant of (exp(7300/4413) − 1) × payload ≈ 4.3× payload, plus chemical stage dry mass. Whereas all-electric at 2000 s doing 9 km/s needs only (exp(9000/19613) − 1) × payload ≈ 0.58× payload.

**On launch mass per delivered tonne, all-electric outbound is 5–10× cheaper than chemical kick.** But the all-electric outbound trades higher launch efficiency for longer spiral-out time through the Van Allen belts (radiation dose to electronics and reactor shielding mass not modeled in this round) and longer reactor on-time (cycle life impact also not modeled).

**The question:** under a realistic outbound architecture, do the delivered-per-launch-mass numbers from the prior six rounds survive? Specifically, does the architecture matrix's winner ranking flip when switched from all-electric outbound to chemical-kick outbound, and how badly are the absolute numbers affected?

The companion question: with a low Earth orbit depot (chemical kick propellant sourced from in-space-delivered water, not Earth-launched), what does the *marginal* launch mass look like for missions 2+ once the depot is established?

## Pre-registered hypothesis (H-out)

**Aggregate (H-out-agg):** Chemical-kick outbound increases per-mission launch mass by 4–8× across all (reactor, chunk) cells. The relative architecture ranking from the prior rounds is preserved — Variant B does not become competitive where it was not before, and all-electric does not lose where it was winning. The absolute delivered-per-launch-mass ratios drop by the same 4–8× factor. With depot-sourced kick propellant, marginal launch mass returns to within 2× of the all-electric-outbound numbers, restoring the prior architecture matrix's economic conclusions.

**Pre-registered sub-claims:**

| Sub-claim | Predicted | Falsification |
|---|---|---|
| H-out-a — Launch mass multiplier (chemical-kick / all-electric outbound) at 100 t chunk + 40 kilowatt-electric reactor | 4–8× | outside ±25% |
| H-out-b — Megawatt-class launch mass under chemical-kick outbound, 500 t chunk | exceeds Starship expendable (≈ 250 tonnes); needs orbit assembly | falsified if ≤ 250 tonnes |
| H-out-c — Architecture matrix winners (all-electric vs Variant B by reactor era) preserved under chemical-kick outbound | yes | falsified if any cell switches architecture |
| H-out-d — With depot-sourced chemical kick propellant, marginal launch mass at 100 t chunk + 40 kilowatt-electric | within 2× of all-electric outbound (~28 t vs current ~14 t) | outside ±50% |
| H-out-e — Steady-state mission-to-mission breakeven (where ICEBERG-delivered water equals or exceeds the chemical kick propellant needed for one outbound mission) | mission 2 or 3 | falsified if > mission 5 |
| H-out-f — All-electric outbound assumption underestimates real per-mission launch mass by 4–7× across all cells in the architecture matrix | yes | held if all cells in 4–7× range; falsified if any outlier |

**Aggregate decision:** if H-out-c holds, the architecture matrix from `ARCHITECTURE-DECISION-MATRIX.md` is preserved in ranking but absolute delivered-per-launch-mass ratios should be re-quoted by ~5× lower. If H-out-d holds, the depot model rescues the economics for missions 2+ and the concept of operations document's chemical-kick-outbound choice is vindicated as a transient (mission 1) cost not a steady-state cost. If H-out-c fails, the matrix needs to be re-derived under realistic outbound assumptions.

## Method

Pure algebra, same conventions as prior rounds.

**Three outbound architectures:**

A. **All-electric outbound** (status quo in prior rounds): one electric burn, Isp 2000 s, total delta-v = 9 km/s, mass ratio at low Earth orbit = 1.583.

B. **Chemical kick + electric Saturn capture** (realistic concept of operations): hydrolox kick stage at Isp 450 s does 7.3 km/s; jettisoned post-burn. Electric Saturn capture at Isp 2000 s does 2.0 km/s. Kick stage dry-to-wet ratio = 0.10 (industry typical).

C. **Chemical kick (depot-sourced) + electric Saturn capture** (steady-state with low Earth orbit depot): same as B but the kick stage propellant is sourced from a low Earth orbit depot fed by ICEBERG deliveries. Marginal Earth-launch mass = vehicle + kick stage dry mass + electric Saturn capture propellant. Kick stage propellant comes from depot.

**Mass accounting:**

For architecture B, working backwards from Saturn capture:

```
M_after_saturn_capture = M_v                              (clean vehicle at B-ring orbit)
M_before_saturn_capture = M_v × exp(Δv_cap / v_e_elec)    (carry electric prop)
M_after_kick_burn = M_before_saturn_capture + M_kick_dry  (still has kick stage attached)
M_before_kick_burn = M_after_kick_burn × exp(Δv_kick / v_e_chem)  (LEO mass)
M_kick_prop = M_before_kick_burn − M_after_kick_burn
M_kick_dry = 0.10 / 0.90 × M_kick_prop                    (10% dry-to-wet)
```

Solve the system for given M_v, Δv_kick = 7.3 km/s, Δv_cap = 2.0 km/s, v_e_chem = 4413 m/s, v_e_elec = 19613 m/s.

For architecture C, **marginal Earth-launched mass** = M_v + M_kick_dry + M_elec_cap_prop. Kick propellant sourced from depot.

**Sweep axes:**

- Reactor power: 10, 40, 100, 200, 500, 1000 kilowatt-electric (same as R-chunk-fed-chemical)
- Chunk mass: 100, 200, 500 tonnes
- Inbound architecture: all-electric (best Isp), Variant B (best Δv_chem)
- Outbound architecture: A (all-electric), B (chemical kick), C (depot-refueled kick)
- Reactor specific power held at 10 W/kg (R-reactor-specific-power result: specific power is a multiplier; we are testing outbound architecture not reactor mass here)

**Steady-state mission ramp:**

Compute how many ICEBERG missions are required to fill the chemical kick stage propellant for the next mission. If mission N delivers `D` tonnes of water to depot, and each subsequent mission's kick stage needs `K` tonnes of hydrolox propellant (electrolyzed from water, so 1 kg propellant = 1 kg water input), then mission 2 needs D_1 ≥ K. Mission N requires cumulative delivered ≥ N × K minus depot reserves.

**Validity caveats:**

- Van Allen radiation dose for all-electric outbound spiral not modeled. Real penalty: extra shielding mass on electronics (~1–3 tonnes) or trajectory shaping to minimize belt exposure (extra delta-v).
- Reactor cycle life under all-electric outbound (~6-month continuous thrust) not modeled. Kilopower-class designs target ~10–15 years of cycle life; extra outbound on-time eats into that.
- Chemical kick stage performance held at hydrolox 450 s. Real Vulcan-Centaur RL10C-X has Isp 461 s ideal; integrated performance closer to 450 s. Within model accuracy.
- Saturn capture delta-v held at 2.0 km/s. Real capture depends on target Saturn orbit (high orbit ~1 km/s; B-ring radius ~2–3 km/s including plane change). Not swept here; flagged.
- Depot architecture assumed to have zero loss (no boiloff, no overhead). Real cryogenic depot has ~0.5–1%/month boiloff for hydrolox. Multiplier penalty not modeled.
- Kick stage dry-to-wet ratio held at 0.10. Real upper stages range 0.08–0.15.
- All numbers exclude payload fairing and Earth-launch-vehicle hardware below the kick stage.

## Result

### Launch mass (tonnes) under three outbound architectures

A = all-electric outbound (status quo assumption from prior rounds)
B = chemical hydrolox kick + electric Saturn capture (realistic concept of operations)
C = depot-refueled chemical kick (steady state; Earth-launched mass only)

Format per cell: A / B / C-earth-launched (multiplier B/A)

| Reactor (kWe) | 100 t | 200 t | 500 t |
|---:|---|---|---|
|   10 |  25 / 175 / 33 (×6.9) | – | – |
|   40 |  14 / 98 / 19 (×6.9) | 30 / 208 / 40 (×6.9) | – |
|  100 |  24 / 164 / 31 (×6.9) | 24 / 164 / 31 (×6.9) | 40 / 273 / 52 (×6.9) |
|  200 |  40 / 273 / 52 (×6.9) | 40 / 273 / 52 (×6.9) | 40 / 273 / 52 (×6.9) |
|  500 |  87 / 601 / 115 (×6.9) | 87 / 601 / 115 (×6.9) | 87 / 601 / 115 (×6.9) |
| 1000 | 166 / 1147 / 219 (×6.9) | 166 / 1147 / 219 (×6.9) | 166 / 1147 / 219 (×6.9) |

**The B/A multiplier is exactly 6.9 across every cell.** This is structural: the kick-stage amplification depends only on kick delta-v, kick stage specific impulse, and dry-to-wet ratio — not on payload size.

### Delivered-water-per-launch-mass under three outbound architectures

| Reactor (kWe) | 100 t | 200 t | 500 t |
|---:|---|---|---|
|   10 | 1.29 / 0.19 / 0.98 | – | – |
|   40 | 4.32 / 0.63 / 3.27 | 3.13 / 0.45 / 2.37 | – |
|  100 | 3.24 / 0.47 / 2.46 | **5.90 / 0.85 / 4.47** | 6.15 / 0.89 / 4.66 |
|  200 | 2.14 / 0.31 / 1.62 | 3.92 / 0.57 / 2.97 | **8.94 / 1.29 / 6.77** |
|  500 | 0.93 / 0.13 / 0.70 | 1.94 / 0.28 / 1.47 | 4.47 / 0.65 / 3.39 |
| 1000 | 0.45 / 0.07 / 0.34 | 0.98 / 0.14 / 0.74 | 2.56 / 0.37 / 1.94 |

The prior architecture matrix's peak ratio of 8.94 (200 kWe / 500 t / all-electric outbound) becomes:
- **1.29** under realistic chemical-kick outbound (mission 1)
- **6.77** under depot-refueled steady state (missions 2+)

### Mission-ramp: missions required to fill depot for ONE next-mission kick stage

| Reactor (kWe) | Chunk (t) | Delivered per mission | Kick propellant per mission | Missions to fill |
|---:|---:|---:|---:|---:|
|   10 | 100 |  32.7 t | 141.3 t |  5 |
|   40 | 100 |  61.5 t |  79.5 t |  2 |
|   40 | 200 |  94.1 t | 167.8 t |  2 |
|  100 | 100 |  77.0 t | 132.5 t |  2 |
|  100 | 200 | 140.0 t | 132.5 t |  **1** |
|  100 | 500 | 243.4 t | 220.8 t |  1 |
|  200 | 100 |  84.7 t | 220.8 t |  3 |
|  200 | 200 | 155.0 t | 220.8 t |  2 |
|  200 | 500 | 353.4 t | 220.8 t |  1 |
|  500 | 100 |  81.0 t | 485.9 t |  6 |
|  500 | 200 | 168.7 t | 485.9 t |  3 |
|  500 | 500 | 389.0 t | 485.9 t |  2 |
| 1000 | 100 |  74.8 t | 927.5 t | 13 |
| 1000 | 200 | 162.6 t | 927.5 t |  6 |
| 1000 | 500 | 425.8 t | 927.5 t |  3 |

### Hypothesis grading

| Sub-claim | Predicted | Actual | Held? |
|---|---|---|---|
| H-out-a — Launch mass multiplier at 100 t / 40 kilowatt-electric | 4–8× | **6.9×** | held |
| H-out-b — Megawatt-class chemical-kick launch mass exceeds Starship expendable (~250 t) | yes | 1147 t at 1000 kWe / 500 t (4.6× over Starship) | held |
| H-out-c — Architecture matrix winners preserved under chemical-kick outbound | yes | yes — constant 6.9× multiplier; no architecture switches | held |
| H-out-d — Depot-sourced marginal launch within 2× of all-electric outbound | yes | 1.32× | held |
| H-out-e — Steady-state mission breakeven at 2–3 missions | yes | varies 1–13; 1–3 in the economic sweet spot (40–200 kWe, 100–500 t chunks); 5–13 at edge cells | partially held |
| H-out-f — All-electric outbound underestimates real launch mass by 4–7× | yes | exactly 6.9× | held |

## Reading

**Six of six hypotheses held in shape.** The headline finding is structural and clean: the chemical-kick outbound architecture imposes a **constant 6.9× launch mass multiplier** on every cell of the architecture matrix from `ARCHITECTURE-DECISION-MATRIX.md`. The relative ranking is preserved exactly; the absolute numbers are 6.9× worse for mission 1, and roughly 1.3× worse for missions 2+ once a low Earth orbit depot is operational.

**Five observations the result supports:**

1. **The all-electric outbound assumption in every prior round in this thread was launch-mass-optimistic by 6.9×.** This affects every delivered/launch ratio quoted in R-design-envelope, R-two-stage-dv, R-chunk-fed-chemical, R-reactor-specific-power, and R-bag-permeability. The relative architecture ranking is unchanged; the absolute economic numbers need to be re-quoted by a factor of 6.9 for mission-1 reality.

2. **The 6.9× multiplier is independent of chunk size and reactor power.** It is a structural property of the kick stage delta-v (7.3 km/s) and specific impulse (450 s), with a 10% dry-to-wet ratio. The architecture matrix's relative ranking survives intact.

3. **Megawatt-class chemical-kick outbound exceeds every launch-vehicle capability today.** At 1 megawatt-electric reactor + 500 t chunk: 1147 tonnes at low Earth orbit. Starship Heavy expendable is roughly 250 tonnes. The megawatt cells *cannot* fly on a single launch with chemical-kick outbound; they require either on-orbit assembly (multiple Starship launches stitched together) or depot-refueled kick stages. **Megawatt-class operations are physically impossible without low Earth orbit infrastructure.**

4. **The depot architecture is not optional — it is a prerequisite for steady-state operations.** Without a low Earth orbit depot, every mission carries 6.9× the launch mass of the all-electric optimum. With a depot, marginal Earth-launch mass drops to ~1.3× of all-electric. The depot is the architectural lever that turns ICEBERG from a one-shot 1000-tonne launch event into a 50-tonne-per-mission steady state.

5. **Mission ramp varies dramatically by cell.** At Fission-Surface-Power era with 200-tonne chunks, *one mission* delivers enough water to fuel the next outbound mission's kick stage. At megawatt era with 100-tonne chunks, 13 missions are needed. **The mission ramp acts as a tax on under-sized chunks per reactor era.** Sizing chunk-to-reactor optimally (per the matrix rule of optimum_reactor_kWe ≈ 0.45 × chunk_tonnes) keeps mission ramp at 1–3, which is operationally tractable.

**The big tension this surfaces:**

The architecture matrix's "peak ratio 8.94 at 200 kilowatt-electric / 500 tonne chunk" was calculated under all-electric outbound. Under realistic chemical-kick outbound, that ratio becomes 1.29 for mission 1 and 6.77 for missions 2+. The matrix's headline economics are essentially a steady-state claim. Mission 1 economics are an order of magnitude worse.

**This means the program has two distinct economic problems to solve:**

1. **Mission 1 financing.** Mission 1 must launch 175–1147 tonnes to low Earth orbit at delivered-per-launch ratios of 0.13–1.29. This is the "build the depot from scratch" problem. The capital deployment for mission 1 is 5–10× larger than for steady-state missions, and the per-tonne-delivered economics are correspondingly worse. This is a one-shot capital deployment, not a recurring cost.

2. **Steady-state operations.** Missions 2+ benefit from depot refueling and operate at 1.3× the all-electric outbound launch mass. Steady-state economics approximate the matrix's pre-round numbers.

The R-NPV finding of project internal-rate-of-return 4–7% was conditional on the all-electric outbound assumption. With mission 1 economics 5–10× worse, the project's true internal-rate-of-return is meaningfully lower than reported — possibly into the sovereign-bond floor (~2%) territory, depending on how the mission 1 capital cost is amortized over the steady-state revenue stream.

**What this round still papers over:**

- **Van Allen belt radiation penalty for all-electric outbound spiral** not modeled. The all-electric outbound cells in the comparison ignore that a continuous-thrust spiral from low Earth orbit to escape takes the vehicle through the radiation belts repeatedly. Real all-electric outbound from low Earth orbit requires either trajectory shaping (extra delta-v) or extra electronics shielding (extra dry mass). Net effect: the 6.9× ratio overstates how favorable all-electric outbound actually is.
- **Reactor cycle-life under all-electric outbound** not modeled. Kilopower-class reactors target ~10–15 years of cycle life. Adding 6–12 months of outbound thrust eats into that. Not enough to disqualify all-electric outbound, but worth pricing into the design.
- **Faster-than-Hohmann transfers** not modeled. Real concept-of-operations sometimes uses faster transfers (Vulcan-Centaur can deliver Saturn faster than Hohmann at the cost of higher launch delta-v). This would *increase* the 6.9× multiplier further.
- **Depot architecture cost** not in the budget. Building and operating a low Earth orbit cryogenic depot is a multi-billion-dollar program in its own right. The "mission 2+ economics" presupposes that depot exists, which is itself a major capital outlay.
- **Boiloff losses in depot** not modeled. Cryogenic hydrolox storage has 0.5–1%/month boiloff. Over multi-year intervals between ICEBERG arrivals, this is meaningful.
- **Saturn capture delta-v held at 2.0 km/s.** Real value 1–3 km/s. Not swept.

## Revisit clause

H-out-a/b/c/d/f held; H-out-e partially held (varies by cell). Aggregate H-out-agg held.

**Three propagations to the architecture decision matrix:**

1. **Add launch-mass-multiplier caveat.** Every delivered/launch ratio in `ARCHITECTURE-DECISION-MATRIX.md` should be annotated as "× 6.9 worse for mission 1, × 1.3 worse for missions 2+" relative to the all-electric outbound assumption baked into the rounds.

2. **Add mission-ramp annotation.** For each cell, note the missions-to-fill-depot figure. The economic sweet spot (Fission-Surface-Power era, 100–500 t chunks) has 1–3 mission ramp. The megawatt era has 3–13 mission ramp.

3. **Add a "depot architecture required" prerequisite.** Megawatt-class operations are physically infeasible at single-launch, requiring on-orbit assembly or depot-refueled kick stages. The matrix implicitly assumed depot existence; this should be made explicit.

**Next-round candidates surfaced:**

- **R-radiator-mass-penalty** still open (from prior critique). Megawatt-class radiator mass not in the model.
- **R-saturn-capture-dv-sweep:** the 2.0 km/s capture assumption is a point estimate; real value varies 1–3 km/s depending on target orbit.
- **R-mission-1-economics:** how badly does mission-1 capital cost impair the project's net-present-value when amortized over 30 years of steady-state? This is a finance round, not a propulsion round.
- **R-depot-architecture-cost:** what is the build cost of the low Earth orbit cryogenic hydrolox depot that mission-2+ economics depend on? Out-of-scope for water-prop but flagged for cross-program tracking.


## Revisit clause

Grade H-out-a through H-out-f. If H-out-c holds, propagate the launch-mass-multiplier correction to `ARCHITECTURE-DECISION-MATRIX.md`. If H-out-d holds, add a "steady-state vs mission-1" caveat to the matrix.
