# R-hybrid-chemical-power-augmentation — does a 10-kilowatt-electric reactor baseline plus a hydrogen-oxygen gas-generator boost close any inbound cell that the 500-kilowatt-electric pure-reactor cell could not?

**Status:** scope, pre-study. Authored by Saturn (orchestrator), 2026-05-15 latest+8, in response to project-owner architectural proposal during walk-through.

## Origin of the question

The project-owner observation: "I do not think a 500-kilowatt-electric reactor is realistic. 10 kilowatts is realistic. But we could build a gas generator that burns hydrogen-oxygen to turn a turbine and supply additional electrical power on the inbound leg — net energy inefficient (you cannot beat thermodynamics) but trades brought-from-Earth chemical fuel mass for relief on the reactor scope wall."

The orchestrator's first-pass back-of-envelope (full inbound electric burn at flown anchors needs ~35 gigawatt-hours; 50 percent generator efficiency means ~18,800 tonnes of hydrolox to replace the 500-kilowatt-electric reactor entirely) addressed the **full replacement** case and found it infeasible. The project-owner's actual proposal is a **hybrid**: reactor provides continuous baseline (housekeeping + part of thruster load), gas generator provides boost during the inbound burn, and chunk mass and burn time are free parameters that trade against brought hydrolox mass. The three-way optimization across (reactor power, brought hydrolox, chunk mass) has not been run.

This round runs it.

## Context — what's already on the matrix

1. **Outbound is already chemical** in the surviving cell architecture (REQUIREMENTS-L1 v0.2). Vulcan-class or larger heavy-lift launcher delivers trans-Saturn-injection chemical kick stage. Reactor power on the outbound leg is housekeeping-class (kilowatts), not propulsion-relevant. **This round does not revisit the outbound architecture; the outbound stays chemical.**
2. **Inbound is the wall.** Per hyperion R-variant-B-impulsive-vs-continuous and titan R-inbound-dv-continuous-thrust, the inbound burn under continuous-thrust electric needs ~25 kilometres-per-second integrated delta-velocity at 500-kilowatt-electric reactor scope for 200-tonne chunk class, sustained over 8-12 years.
3. **Reactor-program walls at flown anchors:** Kilopower / Kilowatt Reactor Using Stirling Technology measured 2.4 watts-per-kilogram specific power and 28 hours cumulative full-power burn lifetime (locked aelfrice belief `0d5c882c13395571`). Per enceladus-r5 R-specific-power-cliff and R-reactor-lifetime-vs-burn-time, no current US reactor program comes close to the conjunction (≥ 5-8 watts-per-kilogram specific power × ≥ 5-10 years lifetime × ≥ 500 kilowatts-electric scope) that closes the matrix.
4. **The hybrid proposal de-risks the reactor wall** by accepting a smaller reactor (10 kilowatts-electric matches the public Kilopower-unit scope per locked aelfrice belief `a8f430e3e2bb4c55`) and importing the missing electrical energy from Earth as hydrolox in a separate tank, burned through a gas generator (Brayton turbine or fuel cell) during the inbound burn.

The trade is honest about thermodynamics: combustion + generator is ~30-50 percent efficient, electrolysis + combustion (closed loop) is ~30 percent efficient. The hybrid is not a perpetual-motion machine; it is a **mass-for-reactor-scope swap**: you pay propellant mass at Earth orbit to avoid carrying a 500-kilowatt-electric reactor.

## Question this round answers

For the held chunk-rendezvous architecture (axis 19) with outbound chemical kick locked, inbound continuous-thrust electric, and a hybrid power plant consisting of:

- One reactor of scope P_reactor (kilowatts-electric), specific power 2.4 watts-per-kilogram (Kilopower flown anchor) or 5 watts-per-kilogram (General Purpose Heat Source Radioisotope Thermoelectric Generator-class), Kilopower-design-target lifetime of 10 years cumulative
- One gas-generator with brought-from-Earth hydrolox tankage M_H2O2 (tonnes), generator efficiency η_gen ∈ {0.3, 0.5}, tank mass fraction 10 percent of propellant mass
- Optional auxiliary onboard-electrolysis loop using bag water + reactor power to extend the gas-generator runtime (energy-buffer mode, not energy-source mode)

**Determine:**

1. **Does any (P_reactor, M_H2O2, chunk_mass, burn_time) combination yield a positive delivered-fraction cell at flown-anchored reactor performance?**
2. **What is the launch-to-low-Earth-orbit mass envelope** for each surviving cell? (Vehicle + outbound chemical kick stage + brought hydrolox + reactor + tankage, before chunk capture.)
3. **At what chunk mass does the hybrid architecture cease to be infeasible?** Hypothesis: very-small-chunk demonstrator (≤ 10 tonnes) closes at hybrid with modest brought hydrolox; commercial-class chunk (≥ 200 tonnes) requires brought hydrolox in the thousands of tonnes, infeasible on current launchers.
4. **Where is the launch-mass-vs-chunk-mass cliff?** Is there a brought-hydrolox sweet spot where launch mass stays under N × Vulcan/Starship and delivered chunk stays above 10 tonnes?
5. **What does the round-trip time look like** for the surviving cells? (More brought hydrolox → more average inbound power → shorter burn → but more launch mass.)
6. **How does this compare to the matrix-empty verdict** for pure-reactor architectures at the same flown anchors?

## Pre-registered hypotheses (numeric ranges + falsification bands)

| # | Hypothesis | Predicted range | Falsification band |
|---|---|---|---|
| H1 | At P_reactor = 10 kilowatts-electric, no combination of brought hydrolox up to 1000 tonnes closes a 200-tonne-chunk commercial cell at L0-05 ≤ 15 years. | Zero close cells in (M_H2O2 ∈ [0, 1000 t]) × (chunk = 200 t) at L0-05 strict. | H1 falsified if any (M_H2O2, chunk_mass = 200 t) combination at η_gen = 0.5 closes L0-05 strict. |
| H2 | At P_reactor = 10 kilowatts-electric and chunk_mass ≤ 50 tonnes (Architecture-E scope), some (M_H2O2, burn_time) combination closes under L0-05 ≥ 25-year waiver with brought hydrolox ≤ 500 tonnes. | At least one close cell exists in the (M_H2O2 ∈ [100, 500 t]) × (chunk ≤ 50 t) × (burn_time ≤ 25 yr) cube. | H2 falsified if zero close cells exist in this cube. |
| H3 | At P_reactor = 10 kilowatts-electric and chunk_mass ≤ 10 tonnes (true demonstrator scope), reactor alone closes a 30-40 year demonstrator without brought hydrolox; hybrid is unnecessary. | Reactor-alone close at chunk ≤ 10 t for round-trip ≤ 40 years. | H3 falsified if reactor alone cannot deliver ≥ 1 tonne to low Earth orbit at any chunk mass and reasonable round-trip. |
| H4 | The launch-mass-vs-chunk-mass cliff sits between 20 and 80 tonnes delivered chunk: below 20 t delivered, brought hydrolox is < 200 t; above 80 t delivered, brought hydrolox is > 1000 t and total launch stack exceeds 5× Vulcan or 2× Starship to low Earth orbit. | Cliff in (delivered chunk) ∈ [20, 80] t. | H4 falsified if cliff lies outside this band. |
| H5 | Round-trip time for surviving hybrid cells is dominated by burn time, not coast: at P_reactor + average gas-generator power = 30-50 kilowatts-electric, burn time on a 50-tonne chunk inbound delta-velocity 25 kilometres-per-second is approximately 8-14 years; total round-trip 22-30 years. | Round-trip range 22-30 years for the surviving H2 cells. | H5 falsified if round-trip falls outside [18, 35] years for the surviving cells. |
| H6 | The brought-hydrolox-mass requirement is approximately equal to (inbound electrical energy gap) ÷ (η_gen × lower-heating-value-of-stoichiometric-hydrolox), i.e. linear in chunk mass and inversely linear in η_gen, with a ~10 percent tank-mass adder. | Linear scaling holds within ±15 percent across chunk mass [10, 200] t. | H6 falsified if the scaling is non-linear (would indicate a coupled effect such as additional reactor lifetime burden from extended electrolysis). |

## Method

This is a Tsiolkovsky-plus-energy-bookkeeping round, not a Basilisk simulation round. Inherited from rhea R-megawatt-marvl-radiator and hyperion R-variant-B-impulsive-vs-continuous in computational style.

**Variables to sweep:**
- `P_reactor` (kilowatts-electric): {1, 5, 10, 20, 50}. Flown-anchor specific power 2.4 watts-per-kilogram; flight-radioisotope-thermoelectric-generator-class 5 watts-per-kilogram (optimistic for fission unit at this scope).
- `M_H2O2` (tonnes, brought hydrolox at Earth orbit, separate from chemical kick stage propellant): {0, 100, 250, 500, 1000, 2500}.
- `chunk_mass` (tonnes): {5, 10, 50, 100, 200}. Spans demonstrator → Architecture-E → commercial.
- `η_gen` (gas-generator electrical efficiency): {0.30, 0.50}. Brayton-turbine low/high band.
- `aerocapture_credit` (kilometres-per-second): {0, 10}. Hybrid round should run both with and without R-hybrid-aerocapture-aerobraking closure assumption.

**Per cell, compute:**
1. Vehicle wet mass at Saturn departure (chunk + dry mass + propellant tankage + reactor + generator + brought-hydrolox-tank residual)
2. Inbound delta-velocity needed (continuous-thrust accounting per titan R-inbound-dv-continuous-thrust)
3. Required average electrical power for the inbound burn, given chosen burn time
4. Energy gap = (required average power × burn time) - (reactor power × burn time)
5. Brought-hydrolox mass required to close the gap at η_gen and lower-heating-value 13.4 megajoules-per-kilogram
6. Total Earth-orbit stack mass (vehicle dry + outbound kick + brought hydrolox + tankage)
7. Round-trip time (outbound + Saturn-side + inbound)
8. Delivered chunk fraction at Earth-orbit hand-off
9. Pass/fail flags: L0-05 strict (≤ 15 yr), L0-05 waiver (≤ 25 yr), L0-04 floor (delivered > 0), launchable (stack ≤ 2× Starship-to-low-Earth-orbit class)

**Mass model:**
- Reactor mass = P_reactor / specific_power (2.4 watts-per-kilogram flown, 5 watts-per-kilogram optimistic)
- Generator mass ≈ 0.05 × peak generator power (terrestrial Brayton-turbine auxiliary-power-unit heritage at ~10-50 kilograms per kilowatt; tighter at smaller scales; use 0.05 t/kW as upper-bound proxy)
- Hydrolox tankage: cryogenic tank dry-mass fraction 10 percent of propellant mass (Centaur upper-stage heritage)
- Bag + harvesting hardware mass: per L1-007 / L1-010 baselines
- Radiator mass: per locked aelfrice belief `0418e2c9ee3de422` — at megawatt scale radiators are 40-55 percent of system mass; at 30-50 kilowatts-electric the radiator fraction is smaller in absolute terms but still nontrivial. Use MARVL-anchored bundled formula scaled to gas-generator + reactor combined waste-heat load.

**Energy bookkeeping check (sanity gate):**
- Confirm that the energy delivered to electric thrusters never exceeds (reactor energy + brought-hydrolox energy × η_gen) over any mission segment. If the bookkeeping shows otherwise, the model has a bug.

## What this round does NOT test

- Solar-augmentation. Saturn-side insolation is ~1 percent of Earth orbit (locked aelfrice belief `f7e78e5c39eabc47`); solar contributes negligibly. Reactor + chemical only.
- The chemical kick stage trades (already locked outbound architecture).
- Saturn-capture mode (already chemical at 0.8 kilometres-per-second per titan-2 R-saturn-soi-periapsis-depth).
- B-ring rendezvous survivability (separate SCOPE; orthogonal to power).
- Whether a fuel-cell generator (instead of Brayton turbine) materially changes the result. The `η_gen` sweep covers the relevant band.

## Falsification of architectural relevance

The round delivers an architectural verdict of one of three forms:

1. **"Closes" — hybrid architecture restores a surviving cell at flown reactor anchors.** If true, this is a load-bearing finding: the L0 framing decisions deferred to R-reactor-specific-power-program-targets become coupled to whether a Vulcan-class launcher (or two) can deliver the brought-hydrolox stack. The framing-A pitch becomes "we trade reactor risk for launch-cadence risk."
2. **"Closes only at demonstrator scales" — hybrid works at chunk_mass ≤ 10 tonnes but not above.** If true, the surviving framing is technology-demonstrator only (framing B from the project-owner walk-through), and `R-demonstrator-power-floor` becomes the next natural round.
3. **"Does not close at any tested combination" — brought-hydrolox mass requirement is infeasible across the entire envelope.** If true, this corroborates the matrix-empty verdict and adds a third orthogonal kill (alongside specific-power and reactor-lifetime walls), but more importantly **explicitly tests the project-owner's architectural intuition** rather than dismissing it on a back-of-envelope.

## Anchors and sources

- Hydrolox lower heating value 13.4 megajoules-per-kilogram (stoichiometric mixture, lower heating value for water-vapour product). Source: standard combustion thermodynamics; cross-check against Sutton "Rocket Propulsion Elements" or NASA Glenn chemical-equilibrium database.
- Generator efficiency band 30-50 percent: terrestrial gas-turbine and aerospace auxiliary-power-unit heritage; Brayton-cycle space-rated higher end is aspirational, ~50 percent.
- Electrolysis efficiency 70-80 percent: proton-exchange-membrane current commercial state-of-the-art.
- Reactor specific power flown anchor: locked aelfrice belief `0d5c882c13395571` (Kilowatt Reactor Using Stirling Technology 2.4 watts-per-kilogram system-level).
- Inbound delta-velocity model: titan R-inbound-dv-continuous-thrust commit `58581fb`, rhea R-outbound-dv-continuous-thrust.
- Continuous-thrust accounting: titan R-conops-chunk-vs-ram-scoop commit `07b73ec`.
- Radiator mass model: locked aelfrice belief `0418e2c9ee3de422` (Modular Assembled Radiators for Very Large systems anchored bundled formula).

## Deliverables

- `STUDY.md` (this file plus expanded methodology, hypotheses, results-pre-registration).
- `run.py` — Python script implementing the Tsiolkovsky + energy-bookkeeping cell sweep, writing results as JSON and Markdown tables.
- `results/tables.md` — headline cells: at each (P_reactor, chunk_mass) corner, the minimum brought-hydrolox mass that closes (if any) and resulting round-trip time + delivered fraction.
- `results/launch_stack.json` — full sweep result with launch-mass and pass/fail flags.
- Handoff file at `~/.claude/handoffs/iceberg-NAME-YYYYMMDD-hybrid-power.md` summarising the architectural verdict for orchestrator integration.

## Suggested worker

**rhea** (has the megawatt-marvl-radiator + heterogeneous-cadence + delivery-irr-curve history; the energy-bookkeeping and Tsiolkovsky tooling is closest to rhea's earlier rounds), OR **hyperion** (has the impulsive-vs-continuous and outbound-chemical-kick-economics history; the chemical-mass-accounting is closest to hyperion's earlier rounds).

Either worker has the relevant heritage. Pick based on availability.

## Open question for project-owner if results force a follow-up

If H2 or H3 hold (hybrid closes at demonstrator-class chunk), the next decision is whether to scope `R-demonstrator-power-floor` as a separate clean-room round at demonstrator-class inheritance from REQUIREMENTS.md §7.5, or to fold demonstrator-class scoping into a hybrid-architecture follow-up. Orchestrator default: keep them separate so the architecture and the requirements-class are decoupled.
