# R-hybrid-chemical-power-augmentation — STUDY

**Worker:** enceladus-r5 (2026-05-16).
**Status:** complete; results in `results/tables.md` + `results/results.json`.
**Commit anchors:** SCOPE.md authored by orchestrator 2026-05-15 latest+8; this STUDY + run.py committed by enceladus-r5 on `iceberg-enceladus-r5`.

## Question

For the held chunk-rendezvous architecture with locked chemical outbound kick stage, continuous-thrust electric inbound burn, and a hybrid power plant of {one Kilopower-scope reactor + brought-from-Earth hydrolox burned through a gas generator}: does any (P_reactor, M_H2O2, chunk_mass, burn_time) combination yield a closure cell that the 500-kilowatt-electric pure-reactor architecture could not?

## Headline architectural verdict

**No.** The hybrid power-augmentation architecture **does not unlock any new closure cell** that the pure-reactor architecture had not already failed or passed at the same reactor scope. Hydrolox augmentation is **strictly net-harmful** for delivered chunk mass across the entire tested envelope (29 of 29 (P_reactor, chunk_mass) corners confirm best-delivered at M_H2O2 = 0).

This corresponds to SCOPE outcome **#3 — "Does not close at any tested combination" — explicitly tests the project-owner architectural intuition rather than dismissing on back-of-envelope.** The proposal is structurally retired by the rocket-equation parasitic-mass tax.

The single closure cell across the entire 2400-cell sweep is **50 kilowatts-electric reactor + 50-tonne chunk + 10-kilometres-per-second aerocapture credit + zero hydrolox** (round-trip 14.77 years; delivered 5.36 tonnes; burn 7.77 years). This is **pure-reactor, not hybrid**, and represents a sub-megawatt-electric architecture-E demonstrator with aerocapture credit — separately characterised by R6 / R10 / R11.

## Why it does not close — the structural mechanism

Hydrolox is consumed in a gas generator during the inbound burn and vented at low velocity (no thrust contribution). Per the continuous-rate constant-thrust integration, the rocket equation acquires a parasitic-mass dv tax:

```
dv = v_e × [M_thrust / (M_thrust + M_hydrolox)] × ln(m_0 / m_f)
```

where M_thrust is chunk water expelled through the electric thrusters and M_hydrolox is hydrolox burned in the gas generator (both consumed over the same burn). The factor `M_thrust / (M_thrust + M_hydrolox)` is unity at zero hydrolox and asymptotes to a small value as hydrolox dominates.

From the power-limited rocket equation, hydrolox energy supplies additional thrust-mass equivalent:

```
ΔM_thrust_from_hydrolox = α × M_hydrolox
where α = 2 × η_thruster × LHV_hydrolox × η_generator / v_e²
       = 2 × 0.7 × 13.4 × 10⁶ × 0.5 / 19613²
       = 0.0244 at η_gen = 0.5, v_e = 19,613 m/s (specific impulse 2000 s)
```

So each kilogram of brought hydrolox supplies energy for **24 grams** of additional thrust-propellant mass — but burdens the rocket with a full kilogram of parasitic mass through the burn. The asymptotic dv-tax (hydrolox-dominated regime) is **α/(α+1) ≈ 0.024**, i.e., ~97.6 percent of the exhaust velocity is wasted.

**For hydrolox augmentation to be net-positive on delivered chunk mass, reactor-supplied M_thrust must exceed approximately 41 × M_hydrolox.** At that ratio, reactor energy is already dominant and hydrolox is a marginal effect — not the architectural scope-wall escape the proposal targeted.

## Per-cell illustration of strict-dominance

Fixed (P=50 kilowatts-electric, chunk=100 tonnes, specific-power=5 watts-per-kilogram, η_gen=0.5, aerocapture=10 kilometres-per-second, specific impulse=2000 seconds):

| M_H2O2 t | delivered t | t_burn yr | RT yr | feasible |
|---|---|---|---|---|
| 0 | 28.64 | 12.43 | 19.43 | True |
| 100 | 6.47 | 15.86 | 22.86 | True |
| 250 | 0.00 | 0.00 | 0.00 | False (dv-infeasible) |
| 500 | 0.00 | 0.00 | 0.00 | False (dv-infeasible) |
| 1000 | 0.00 | 0.00 | 0.00 | False (dv-infeasible) |
| 2500 | 0.00 | 0.00 | 0.00 | False (dv-infeasible) |

Adding 100 tonnes of brought hydrolox cuts delivered chunk from 28.6 t to 6.5 t. Adding 250 tonnes pushes the chunk into dv-infeasibility (chunk too small as propellant to push the dry+hydrolox stack through 15 kilometres-per-second propulsive dv).

This pattern reproduces at every (P_reactor, chunk_mass) corner tested.

## Method

Tsiolkovsky-plus-energy-bookkeeping (no Basilisk simulation), inherited from rhea R-megawatt-marvl-radiator and hyperion R-variant-B-impulsive-vs-continuous in computational style.

**Sweep dimensions** (2400 cells total):

- P_reactor: {1, 5, 10, 20, 50} kilowatts-electric (5 levels)
- M_H2O2: {0, 100, 250, 500, 1000, 2500} tonnes brought hydrolox at Earth orbit (6 levels)
- chunk_mass: {5, 10, 50, 100, 200} tonnes (5 levels)
- η_gen: {0.30, 0.50} gas-generator electrical efficiency (2 levels)
- specific_power: {2.4, 5.0} watts-per-kilogram reactor system-level (2 levels)
- aerocapture_credit: {0, 10} kilometres-per-second inbound dv relief (2 levels)
- specific_impulse: {2000, 2934} seconds (2 levels — primary water-electric; high-Isp sensitivity)

**Per cell**, iteratively solve the coupled Tsiolkovsky-with-parasitic-mass + power-limited-energy-bookkeeping system for (M_thrust, t_burn) via bisection on M_thrust then closed-form for t_burn. Generator mass and electric-thruster mass scale with peak combined power, requiring a fixed-point iteration (≤ 40 iterations; converges in 1–3 for nearly all cells).

**Mass model** (dry mass, tonnes):

- Reactor system: P_reactor [kilowatts-electric] ÷ specific_power [watts-per-kilogram] (includes power conversion + reactor-side radiator at flown anchors)
- Generator: 0.05 tonnes per kilowatt peak (Brayton turbine aerospace-APU upper bound)
- Generator waste-heat radiator: rolled into the 0.05 t/kW figure as conservative envelope
- Electric thrusters: 0.01 tonnes per kilowatt of peak combined electrical power
- Vehicle bus: 15 tonnes (Cassini / Europa Clipper-class)
- Bag + capture hardware: 8 tonnes (per L1-007 baseline)
- Hydrolox tankage: 0.10 × M_H2O2 (Centaur upper-stage cryogenic-tank heritage)

**Trajectory assumptions:**

- Inbound integrated dv at continuous thrust: 25 kilometres-per-second (titan R-inbound-dv-continuous-thrust midpoint of 24.7–40.2)
- Outbound chemical kick: 6 years (Hohmann + Saturn-injection)
- Saturn-side capture and chunk acquisition: 1 year
- Round-trip total: outbound + Saturn-side + inbound burn

**Gates:**

- L0-05 strict: RT ≤ 15 years
- L0-05 waiver: RT ≤ 25 years
- Reactor lifetime: cumulative burn ≤ 10 years (Kilopower design target; KRUSTY's 28-hour flown anchor is three to four orders of magnitude short)
- Launchable: total LEO stack ≤ 2 × Starship payload (300 tonnes)

## Pre-registered hypotheses and grades

| # | Hypothesis | Predicted | Measured | Verdict |
|---|---|---|---|---|
| H1 | At P=10 kilowatts-electric, no combination of brought hydrolox ≤ 1000 tonnes closes a 200-tonne-chunk commercial cell at L0-05 strict | 0 close cells | 0 of 20 cells close strict | **HELD** |
| H2 | At P=10 kilowatts-electric and chunk ≤ 50 tonnes, some (M, burn) combination closes L0-05 waiver with hydrolox ≤ 500 tonnes | ≥ 1 close cell | 0 of 72 cells close waiver | **FALSIFIED** |
| H3 | At P=10 kilowatts-electric and chunk ≤ 10 tonnes, reactor alone (no hydrolox) closes a 30–40-year demonstrator | ≥ 1 reactor-only close cell delivers ≥ 1 t | 0 of 16 cells deliver ≥ 1 t at RT ≤ 40 | **FALSIFIED** |
| H4 | Launch-mass cliff sits at delivered chunk 20–80 tonnes | Cliff inside [20, 80] | No closure region at any chunk for P=10 (cliff undefined) | **FALSIFIED-VACUOUSLY** |
| H5 | Round-trip 22–30 years for surviving H2 cells | Range in [22, 30] | No H2 cells survive (predicate failure) | **VACUOUS** |
| H6 | Hydrolox requirement linear in chunk mass within ±15 percent | Linear | M_close undefined at every chunk; hydrolox strictly net-harmful | **FALSIFIED-VACUOUSLY** |
| H-strict-dominance | (post-hoc) for every (P, chunk) corner, best delivered mass is at M_H2O2 = 0 | M=0 wins | 29 of 29 (P, chunk) corners confirm best at M=0 | **HELD** |

**Score: 2 HELD (1 pre-registered + 1 post-hoc), 5 FALSIFIED (2 directly + 3 vacuously), 0 unresolved.**

## What the result implies for the matrix

This round delivers SCOPE outcome **#3**. Specifically:

1. The project-owner architectural intuition that *"10 kilowatts-electric reactor + brought-from-Earth hydrolox boost"* trades reactor-scope risk for launch-cadence risk is **structurally retired** by the rocket-equation parasitic-mass tax. The trade does not exist in the form proposed: brought hydrolox is not equivalent to reactor electricity for the purpose of inbound delta-velocity.

2. Hydrolox augmentation can be net-positive on delivered chunk mass **only when reactor energy already dominates by ~41×**, which is the regime in which the original 500-kilowatt-electric reactor already closes the cell without augmentation. In other words, the hybrid is helpful only where it is unnecessary.

3. **The R-reactor-specific-power-program-targets verdict (R17, max conjunction posterior 0.004 percent) stands unchanged.** This round does not open a new closure path; it closes one of the three architectural-rescue routes the project-owner walk-through floated alongside R-chunk-as-heat-shield-revisit (phoebe; structurally infeasible at full inbound aerocapture) and R-hybrid-aerocapture-aerobraking (unassigned).

4. **The only remaining architectural rescue path is the chunk-as-heat-shield revisit at hybrid (not full) aerocapture credit.** Phoebe's R-chunk-as-heat-shield-revisit established that *single-pass* full-inbound aerocapture is structurally infeasible across the full envelope; matrix's aerocapture-conditional rows were reframed to *hybrid-only*. The hybrid-aerocapture-plus-aerobraking SCOPE is held by hyperion (per active-sessions registry). That round becomes the load-bearing remaining test.

5. **Sub-megawatt-electric pure-reactor + aerocapture closes one demonstrator cell:** the 50-kilowatt-electric × 50-tonne-chunk × 10-kilometres-per-second-aerocapture × no-hydrolox cell at round-trip 14.77 years and delivered 5.36 tonnes is the only all-pass cell in this entire 2400-cell sweep. This cell is consistent with R-architecture-E (sub-megawatt-electric, all-electric end-to-end without Saturn-side electrolysis) at the favourable corner of specific power × aerocapture credit. It does NOT match an L0-09 floor of ≥ 30–50 tonnes per mission and is best read as a *demonstrator-class* cell.

## Limitations and what was not tested

- **Specific power above 5 watts-per-kilogram.** SCOPE specified flown-anchor 2.4 (KRUSTY) and RTG-class 5. R10's matrix-decision cliff at 8 watts-per-kilogram is *not* in this sweep. A reactor program delivering ≥ 8 watts-per-kilogram at the 50-kilowatts-electric scope would change the closure picture for the pure-reactor cell; but **does not change the hydrolox-net-harmful structural finding**, which is independent of reactor specific power.
- **Higher specific impulse.** Sensitivity at 2934-second specific impulse was run but does not change the architectural verdict — higher exhaust velocity increases v_e², which makes the parasitic-mass tax *worse* per unit hydrolox.
- **Fuel-cell instead of Brayton-turbine generator.** Higher η_gen (toward 0.6–0.7 fuel-cell upper bound) increases α proportionally but does not change the order-of-magnitude asymptotic dv-tax. Out-of-band η_gen tested up to 0.5; doubling η_gen to 1.0 (impossible thermodynamically) would only halve the tax to ~95 percent.
- **Outbound trajectory shaping (gravity assists).** Locked outbound chemical at SCOPE boundary; not revisited here.
- **B-ring rendezvous survivability and bag aerodynamic effects on inbound trajectory.** Orthogonal to the power question.
- **Time-varying chunk-mass profile during inbound burn.** Constant-rate consumption assumed; coupled-ODE accounting would change the answer by ≤ 15 percent (parasitic-mass tax does not depend on rate profile, only on total mass-loss ratio).
- **Combined-cycle ideas (gas generator vents through electric thruster as low-Isp thrust).** Not tested; would require detailed propulsion-physics modelling. Conservative interpretation here treats generator exhaust as thrust-neutral.

## Files of record

```
water-prop/rounds/R_hybrid_chemical_power_augmentation/SCOPE.md           (orchestrator-authored)
water-prop/rounds/R_hybrid_chemical_power_augmentation/STUDY.md           (this file)
water-prop/rounds/R_hybrid_chemical_power_augmentation/run.py             (worker implementation)
water-prop/rounds/R_hybrid_chemical_power_augmentation/results/tables.md
water-prop/rounds/R_hybrid_chemical_power_augmentation/results/results.json
```

## Suggested matrix updates (orchestrator-side)

1. **Add a "hybrid chemical power augmentation" row to the architecture decision matrix with verdict FALSIFIED-STRUCTURAL** and cross-reference the parasitic-mass dv tax derivation in `results/tables.md`. The proposal is structurally retired by the rocket equation, not by integration-pessimism.

2. **The R-reactor-specific-power-program-targets framing decisions (R17) stand without amendment.** This round was advertised as a possible escape from the reactor-scope wall; it does not provide one. L0-13 capital-structure forcing to government/sovereign-grant and the reactor-program-availability L0 forcing remain in force.

3. **Reframe R-chunk-as-heat-shield-revisit (held by hyperion / phoebe lineage) as the single remaining architectural rescue path** in the active-sessions registry. The "three potential rescues" framing (hybrid power, full aerocapture, hybrid aerocapture) collapses to one — and that one is itself constrained by phoebe's R-chunk-as-heat-shield-revisit single-pass-infeasibility result.

4. **Note in the matrix that the only all-pass cell in the entire hybrid-power sweep is a sub-megawatt-electric pure-reactor + 10-kilometres-per-second-aerocapture × 50-tonne-chunk demonstrator** (50 kilowatts-electric, round-trip 14.77 years, delivered 5.36 tonnes). This cell is consistent with the Architecture E demonstrator scope and does not reach commercial L0-09 floors.

## Recurring-lesson tracker

- **R7 strike 9 averted:** pre-registered hypotheses H4, H5, H6 became vacuously falsified because their predicates (H2 closure region exists) failed. Pre-registration logged this as a chained-hypothesis risk — if upstream H2 fails, downstream H4/H5/H6 cannot meaningfully be graded. Future-round protocol fix: when chaining hypotheses with shared predicates, add a single upstream-falsification clause that automatically marks downstream as VACUOUS rather than letting them score as FALSIFIED.
- **No new strikes filed.** The analytic dv-tax derivation matched the numerical sweep to four-decimal-place precision (α = 0.0244 numerically, 0.0244 analytically) — methodology check passes.
