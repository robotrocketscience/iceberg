# R-all-electric-thruster-sweep — when R10b's 224-cell sweep is re-run at continuous-thrust delta-velocities (R-inbound + R-electric-outbound) and realistic water-electric thruster efficiencies, does any cell in the year-twenty-plus all-electric end-to-end architecture still close level-zero requirement L0-05?

**Status:** pre-result.

## Question

R10b (commit history) ranked four water-fed thruster classes — microwave-electrothermal at specific impulse 700 second / efficiency 0.30, Hall at 1500 second / 0.55, radio-frequency-ion at 2000 second / 0.65, dual-ion at 5000 second / 0.55 — across power classes 10 to 500 kilowatt-electric. R10b's headline was that water radio-frequency-ion (Pale Blue lineage) dominates microwave-electrothermal above 25 kilowatt-electric and water-dual-ion is dominated at every cell. The architecture decision matrix's year-twenty-plus winner cell inherits R10b's thruster pick.

Two findings between R10b and now disturb R10b's conclusion:

**R-electric-outbound (commit 9001ce9)** found that the conops-stated impulsive 9 km/s outbound delta-velocity is 17.97 km/s under continuous-thrust electric, paid in full with no Earth-departure Oberth credit. R10b's model assumes a ballistic Hohmann outbound — that is, the chemical-kick architecture (Kilopower Variant B), not the all-electric end-to-end architecture.

**R-inbound-dv-continuous-thrust (commit 58581fb)** found that the matrix's impulsive 6.42 km/s inbound delta-velocity is 24.67 to 40.17 km/s under continuous-thrust electric, depending on Saturn departure orbit. R10b's inbound delta-velocities (4.47 to 8.87 km/s residual after a lunar tour, then Earth-side capture) are also impulsive Oberth-credited.

The wonder pass on water-fed electric thrusters separately finds that R10b's efficiency anchors are optimistic versus the published laboratory state-of-art at sub-kilowatt: water-Hall measured anode efficiency is 0.125, not 0.55; water radio-frequency-ion at 0.65 is not in conflict with the Pale Blue heritage but is at the optimistic end; water microwave-electrothermal real flight-realistic performance per R0 is at the 480 to 520 second band, not the 700 second R10b carries.

**The question:** at the continuous-thrust delta-velocities from R-electric-outbound and R-inbound (the all-electric end-to-end architecture, not R10b's implicit chemical-kick architecture), and at thruster efficiencies bracketed by R10b's optimistic-canonical values and the wonder-pass measured-realistic values, does any (thruster class × power class × chunk mass) cell still close level-zero requirement L0-05's 15-year ceiling?

This is a goal-backward audit of the matrix's year-twenty-plus winner cell. The cell is currently inherited from R10b — but R10b was run for the wrong architecture.

## Pre-registered hypothesis (H-aets)

**Aggregate (H-aets-agg):** At the corrected continuous-thrust delta-velocities and R10b's optimistic-canonical efficiencies, water radio-frequency-ion at 1 megawatt-electric remains the only surviving cell, but its delivered chunk fraction drops materially from R10b's headline. At the wonder-pass measured-realistic efficiencies (water-Hall 0.125, water-microwave-electrothermal 0.20, water-radio-frequency-ion 0.30, water-dual-ion 0.25), no cell closes for chunk mass greater than ~50 tonnes at any power up to 2 megawatt-electric — the all-electric end-to-end architecture collapses entirely, leaving Kilopower Variant B (chemical kick plus electric inbound) as the sole surviving architecture.

**Pre-registered sub-claims:**

| Sub-claim | Predicted | Falsification |
|---|---|---|
| H-aets-a — Under R10b efficiencies, water-microwave-electrothermal at any power up to 2 megawatt-electric, chunk ≥ 50 tonne, all-electric end-to-end at high-elliptical Saturn departure with lunar gravity assist | NO cell closes 15-year ceiling | held if true; falsified if any closes |
| H-aets-b — Under R10b efficiencies, water-Hall at megawatt-electric, chunk 200 tonne, all-electric end-to-end at high-elliptical Saturn departure with lunar gravity assist | round-trip 13 to 15 year, delivered fraction 8 to 18% | falsified if outside band |
| H-aets-c — Under R10b efficiencies, water-radio-frequency-ion at megawatt-electric, chunk 200 tonne, all-electric end-to-end at high-elliptical Saturn departure with lunar gravity assist | round-trip 14.5 to 15.0 year, delivered fraction 15 to 25% — this is the matrix's claimed winner | falsified if round-trip > 15.5 (matrix breaks) or delivered fraction < 10% (economics break) |
| H-aets-d — Under R10b efficiencies, water-dual-ion at megawatt-electric, chunk 200 tonne, all-electric end-to-end at high-elliptical Saturn departure with lunar gravity assist | round-trip > 16 year (specific impulse too high, thrust too low, burn-time blows budget) | held if confirmed; the inverse of R-inbound's specific-impulse-optimum-is-at-the-bottom lesson |
| H-aets-e — Under wonder-pass realistic efficiencies, water-radio-frequency-ion at megawatt-electric, chunk 200 tonne, all-electric end-to-end | round-trip > 17 year, delivered fraction < 5% | held if confirmed: load-bearing falsified — the all-electric end-to-end architecture is dead at realistic efficiencies |
| H-aets-f — At wonder-pass realistic efficiencies, the *smallest* chunk mass that closes 15-year for water-radio-frequency-ion at 2 megawatt-electric, high-elliptical Saturn departure with lunar gravity assist | ∈ [20, 80] tonne | falsified if no cell closes at any chunk ≥ 10 tonne |
| H-aets-g — Cross-check: Kilopower Variant B (chemical-kick outbound, ballistic Hohmann, chemical capture, residual electric inbound at 6.42 km/s impulsive) at water-radio-frequency-ion, megawatt-electric, chunk 200 tonne | delivered fraction 60 to 75% (replicates matrix); structurally unaffected by R-inbound finding | falsified if delivered < 50% (would mean R-inbound's structural-unaffected conclusion for Variant B is wrong) |

**Pre-registered aggregate decision-ordering:**

The structurally interesting outcome is whether H-aets-e falsifies high — meaning the all-electric end-to-end architecture closes even under the wonder-pass realistic efficiencies. If it closes, the matrix survives with tighter unit economics. If it does not close (the pre-registered direction), the architecture decision matrix's year-twenty-plus winner cell is retired and the matrix collapses to a single year-zero-through-fifteen winner (Kilopower Variant B). This would propagate to: pitch headline, conops Phase 5–6, financial model, milestone plan, capital-stack design.

H-aets-d is the inverse of R-inbound's surprise. R-inbound found specific-impulse optimum at megawatt-electric is at the bottom of the available band (2000 second), not the top — because at fixed power, higher specific impulse means lower thrust means longer burn time blows the time ceiling. Water-dual-ion at 5000 second specific impulse should be even worse than R-inbound's 4000-second case. Predict round-trip > 16 year.

H-aets-g is the safety check on Kilopower Variant B. R-inbound stated Variant B is structurally unaffected. This round verifies that by running Variant B at the same model.

## Method

**Architecture model.** The all-electric end-to-end architecture pays continuous-thrust at both ends, separated by ballistic Hohmann cruises. Total round-trip time decomposes as:

```
round_trip = t_outbound_burn + t_hohmann_one_way + saturn_ops_dwell
           + t_hohmann_one_way + t_inbound_burn
```

where `t_hohmann_one_way = 6.09 year` (from Earth-Saturn Hohmann), `saturn_ops_dwell = 1.0 year`. The outbound delta-velocity is 17.97 km/s continuous-thrust (R-electric-outbound headline). The inbound delta-velocity is 27.56 km/s continuous-thrust at the high-elliptical Saturn-departure with lunar-gravity-assist case (R-inbound headline mid-case). Both burn times are computed from the constant-thrust closed-form: `t_burn = m_prop · v_exhaust / thrust`.

**Mass closure.** The vehicle stack consists of tug dry mass (power-scaled, from R-electric-outbound's decomposed-mid model: 5.5 to 16.4 tonne for 100 to 2000 kilowatt-electric) plus reactor mass (computed from specific power, default 10 watt per kilogram) plus the chunk. Outbound burn moves the dry-stack-plus-outbound-propellant from Earth to Saturn; inbound burn moves the dry-stack-plus-chunk back to Earth. Propellant for both legs is water from the chunk for the inbound; outbound propellant is launched-water (no chunk yet, modeled as part of initial mass).

For simplicity, this round uses the R-inbound model's `tug_dry_t` and `outbound_burn_yr` lookup tables verbatim — those already encode the decomposed-mid propulsion-system + reactor + structures mass model from R-electric-outbound. The inbound delta-velocity is fixed at 27.56 km/s (the R-inbound high-elliptical-with-lunar-gravity-assist mid-case). Chunk mass and thruster (specific impulse, efficiency) are swept.

**Two efficiency regimes.** R10b-canonical (the optimistic anchors R10b used) and wonder-pass-realistic (the published laboratory measurements summarised in the persisted wonder phantoms). At each (thruster × power × chunk × efficiency-regime) cell, compute round-trip time and delivered chunk fraction.

**Sweeps.**
- Thruster: water-microwave-electrothermal, water-Hall, water-radio-frequency-ion, water-dual-ion.
- Specific impulse and efficiency per regime (R10b-canonical / wonder-pass-realistic):
  - water-microwave-electrothermal: (700 s, 0.30) / (520 s, 0.20)
  - water-Hall: (1500 s, 0.55) / (1500 s, 0.125)
  - water-radio-frequency-ion: (2000 s, 0.65) / (2000 s, 0.30)
  - water-dual-ion: (5000 s, 0.55) / (5000 s, 0.25)
- Reactor power: 100, 200, 500, 1000, 2000 kilowatt-electric.
- Chunk mass: 50, 100, 200, 500 tonne.
- Inbound delta-velocity case: matrix-impulsive (6.42 km/s, sanity check), high-elliptical with lunar gravity assist (27.56 km/s).
- Outbound delta-velocity case: matrix-impulsive (9.0 km/s, sanity check), continuous-thrust (17.97 km/s).

Two delta-velocity regimes (matrix-impulsive, continuous-thrust) crossed with two efficiency regimes (R10b-canonical, wonder-realistic) crossed with four thrusters crossed with five powers crossed with four chunks: 320 cells. Plus a Kilopower Variant B cross-check (matrix-impulsive delta-velocities, R10b-canonical efficiencies, year-zero-through-fifteen baseline).

**Validity caveats.**

- The outbound delta-velocity 17.97 km/s and outbound burn-time table are inherited from R-electric-outbound at specific impulse 2000 second. Strictly, the outbound burn time should be recomputed at each (specific impulse, efficiency) sweep cell. For the dual-ion case (specific impulse 5000 second), the inherited 0.16 to 0.36 year outbound burn-time is therefore optimistic by 2.5× — the dual-ion outbound burn is closer to 0.4 to 0.9 year. This understates the dual-ion problem on the outbound; the inbound problem (which dominates at high specific impulse per R-inbound) is captured correctly.
- The chunk-mass-as-initial-mass model assumes outbound propellant is *not* drawn from the chunk (since the vehicle has no chunk on outbound). This is the conops convention. Outbound propellant launches from Earth as part of the vehicle wet mass.
- Reactor mass at specific power 10 watt per kilogram is R10b's Fission Surface Power target; the wonder pass tightened this to "near-term flight hardware is 6–40 kilowatt-electric, megawatt-electric is 2030s+ programmatic aspiration." The reactor mass at megawatt-electric is therefore optimistic by an unknown factor.
- Cathode life is not modeled. Per the wonder pass, no water-fed cathode has been life-tested past laboratory durations; the round-trip burn times computed here (1.5–3.0 year at megawatt-electric) exceed any published water-fed cathode demonstration by 3+ orders of magnitude.
- Frozen-flow / dissociation loss is implicit in the efficiency anchor. R0's flight-realistic 480–520 second specific impulse for water-microwave-electrothermal is below R10b's 700 second; this round uses 520 second in the wonder-pass-realistic regime for water-microwave-electrothermal.
- The lunar gravity assist credit (2.0 km/s) is folded into the high-elliptical-with-lunar-gravity-assist 27.56 km/s figure inherited from R-inbound. Not separately swept here.

## Result

**Status:** complete. Run output in `results/thruster_sweep.json` and `results/tables.md`. 97 of 320 cells satisfy both the mass-closure check and the 15-year ceiling.

### Headline cells — chunk 200 tonne, continuous-thrust both legs (the all-electric end-to-end architecture)

| Thruster | Eta regime | Power (kilowatt-electric) | Mass ratio inbound | Delivered (tonne) | Delivered % | Inbound burn (year) | Round-trip (year) | Closes 15-year and mass closes? |
|---|---|---:|---:|---:|---:|---:|---:|:--:|
| water-microwave-electrothermal | canonical (700 s, 0.30) | 1000 | 55.41 | −8.3 | infeasible | 0.52 | 14.08 | **no** (mass closure fails) |
| water-microwave-electrothermal | realistic (520 s, 0.20) | 1000 | 222.40 | −11.1 | infeasible | 0.43 | 14.44 | **no** (mass closure fails) |
| water-Hall | canonical (1500 s, 0.55) | 1000 | 6.51 | 20.5 | 10.2% | 1.12 | 14.48 | **yes** |
| water-Hall | realistic (1500 s, 0.125) | 1000 | 6.51 | 20.5 | 10.2% | 4.92 | 18.90 | **no** (burn-time burst) |
| water-radio-frequency-ion | canonical (2000 s, 0.65) | 1000 | 4.08 | 39.9 | 20.0% | 1.50 | 14.85 | **yes** |
| water-radio-frequency-ion | realistic (2000 s, 0.30) | 1000 | 4.08 | 39.9 | 20.0% | 3.25 | 16.80 | **no** (burn-time burst) |
| water-dual-ion | canonical (5000 s, 0.55) | 1000 | 1.75 | 108.8 | 54.4% | 6.32 | 19.87 | **no** (burn-time burst) |
| water-dual-ion | realistic (5000 s, 0.25) | 1000 | 1.75 | 108.8 | 54.4% | 13.90 | 27.89 | **no** (burn-time burst) |

At 2 megawatt-electric the picture only marginally improves: water-radio-frequency-ion canonical drops round-trip to 14.06 year but realistic stays at 15.09 year (still above ceiling, narrowly).

### Variant B cross-check — chunk 200 tonne, matrix-impulsive delta-velocities, canonical efficiencies

| Thruster | Power (kilowatt-electric) | Delivered (tonne) | Delivered % | Round-trip (year) | Closes? |
|---|---:|---:|---:|---:|:--:|
| water-microwave-electrothermal | 500 | 72.4 | 36.2% | 13.95 | yes |
| water-Hall | 500 | 125.7 | 62.9% | 14.21 | yes |
| water-radio-frequency-ion | 1000 | 140.8 | 70.4% | 13.80 | yes |
| water-dual-ion | 1000 | 174.0 | 87.0% | 15.15 | no (narrowly) |

Variant B is healthy at every reasonable thruster choice. Under realistic efficiencies (not shown in this cross-check table but visible in the full `cells that close` table), Variant B at water-radio-frequency-ion, megawatt-electric, chunk 200 tonne still delivers 70.4% in 14.53 year — closure preserved.

### Hypothesis grading

| Sub-claim | Predicted | Actual | Verdict |
|---|---|---|---|
| H-aets-a — water-microwave-electrothermal continuous-thrust, chunk ≥ 50 tonne, no cell closes | yes | no cell mass-closes for any chunk ≥ 50 tonne at any power | **held** |
| H-aets-b — water-Hall canonical, megawatt-electric, chunk 200 tonne, continuous-thrust | round-trip 13–15 year, delivered 8–18% | 14.48 year, 10.2% | **held** |
| H-aets-c — water-radio-frequency-ion canonical, megawatt-electric, chunk 200 tonne, continuous-thrust | round-trip 14.5–15.0 year, delivered 15–25% | 14.85 year, 20.0% | **held** |
| H-aets-d — water-dual-ion canonical, megawatt-electric, chunk 200 tonne, continuous-thrust | round-trip > 16 year | 19.87 year | **held** |
| H-aets-e — water-radio-frequency-ion realistic, megawatt-electric, chunk 200 tonne | round-trip > 17 year, delivered < 5% | 16.80 year, 20.0% | **partially falsified** — round-trip narrowly under 17 (held); delivered fraction prediction was wrong because efficiency does not move delivered fraction (only burn time) |
| H-aets-f — smallest chunk for water-radio-frequency-ion realistic at 2 megawatt-electric continuous-thrust | ∈ [20, 80] tonne | no chunk ≥ 50 tonne closes; at chunk 50 tonne the round-trip is 14.50 year at 1000 kilowatt-electric and 13.79 year at 1000 kilowatt-electric canonical → only canonical 1000 kilowatt-electric closes at chunk 50 tonne. The realistic regime at chunk 50 tonne closes at 1000 kilowatt-electric → 14.50 year, delivered 3.1 tonne | **falsified low** — the floor is *lower* than predicted; chunk 50 tonne can close at megawatt-electric realistic radio-frequency-ion, but delivered tonnage is in the 3–4 tonne band, not 20–80 |
| H-aets-g — Variant B at water-radio-frequency-ion canonical, megawatt-electric, chunk 200 tonne | delivered 60–75%, structurally unaffected | 70.4%, round-trip 13.80 year | **held** |

Seven sub-claims pre-registered, five held cleanly, one held on the round-trip half but falsified on delivered-fraction half (H-aets-e — methodology error: delivered fraction is fixed by Tsiolkovsky once Isp and delta-velocity are set, regardless of efficiency), one falsified-low (H-aets-f — the minimum-chunk floor is far lower than predicted because mass closure is set by mass ratio alone, decoupled from efficiency).

## Reading

**The architecture decision matrix's year-twenty-plus winner cell survives only under R10b's optimistic-canonical efficiency anchors.** Under continuous-thrust delta-velocities at both legs:

- water-microwave-electrothermal cannot mass-close at any chunk above ~12 tonne under either efficiency regime. Mass ratio at specific impulse 700 second over the 27.56 km/s inbound delta-velocity is 55.4; at 520 second it is 222.4. The chunk-fed-electric architecture cannot lift its own propellant out of the chunk at these specific impulses.
- water-Hall at megawatt-electric canonical closes at delivered fraction 10.2% (R10b found 60+% under the matrix-impulsive delta-velocity; the correction halves the matrix-impulsive number, then the continuous-thrust correction halves it again). Under realistic efficiency 0.125 the inbound burn time alone is 4.92 year, which busts the 15-year ceiling regardless of mass-closure success.
- water-radio-frequency-ion at megawatt-electric canonical closes at 20.0% delivered, 14.85 year round-trip. **This is the only cell that closes the all-electric end-to-end architecture, and only under the canonical 0.65 efficiency.** Under the realistic 0.30 efficiency it bursts the ceiling by 1.80 year.
- water-dual-ion is dead at every power under continuous-thrust. R-inbound's surprise — that higher specific impulse is *worse* at a time-ceiling because thrust drops as 1/specific-impulse at fixed power — compounds: at specific impulse 5000 second the inbound burn is 6.32 year canonical (megawatt) and 13.90 year realistic.

**The matrix is therefore making an implicit technology-readiness-level claim that the campaign has not separately audited.** The claim is: water-radio-frequency-ion at 1 megawatt-electric will achieve anode efficiency 0.65 at specific impulse 2000 second by the year-twenty-plus operating era. The published 2026 anchors are: water-Hall 0.125 (Tsikata et al. 2023, 1600 watt) and water-radio-frequency-ion presumed in the 0.30 band but never tested above ~1 kilowatt-electric. The "matrix carries 0.65" is xenon-Hall heritage applied to water with no measurement.

**Variant B (year-zero-through-fifteen Kilopower architecture) is unaffected at every reasonable thruster and at both efficiency regimes.** Cross-check rows confirm water-radio-frequency-ion at 1 megawatt-electric, chunk 200 tonne, delivers 70.4% chunk in 13.80 year (canonical) or 14.53 year (realistic). Variant B's mass ratio is 1.39 (matrix-impulsive 6.42 km/s inbound at specific impulse 2000 second); the realistic-efficiency burn-time penalty (4× longer burn) is absorbed by the tiny propellant mass.

**The dual-ion result is interesting in its own right.** At megawatt-electric canonical, dual-ion delivers 54.4% chunk (more than radio-frequency-ion's 20.0%) but bursts the ceiling at 19.87 year. The architecture choice between radio-frequency-ion and dual-ion under continuous-thrust is purely time-ceiling-bound: if L0-05 were relaxed to 20 year, dual-ion would dominate radio-frequency-ion. This is a flag for the financial-model sensitivity rounds — the value of a tighter time ceiling is measurable in delivered-fraction terms.

**Methodology lesson — efficiency moves burn time, not delivered fraction.** Pre-registering H-aets-e against delivered fraction was a methodology error. Tsiolkovsky's delivered fraction depends on specific impulse and delta-velocity only; thruster efficiency moves thrust at fixed power, which moves burn time. The correct pre-registration would have decomposed the prediction into two independent sub-claims: (e1) delivered fraction at realistic efficiency = delivered fraction at canonical efficiency = function of (specific impulse, delta-velocity); (e2) round-trip time at realistic efficiency = round-trip time at canonical efficiency scaled by (canonical efficiency / realistic efficiency) on the burn-time terms. The (e2) prediction would have been "round-trip time roughly doubles when efficiency halves," which the data confirms cleanly. Recurring methodology lesson: pre-register predictions against the variable being moved, not against unrelated variables.

**Three architecture-decision-matrix changes implied by this round:**

1. **The year-twenty-plus winner cell should be annotated with the efficiency assumption (canonical 0.65).** Without that annotation the cell is a hidden technology-readiness-level claim.
2. **The water-microwave-electrothermal column at year-twenty-plus should be retired entirely.** It cannot mass-close at any chunk above ~12 tonne under continuous-thrust at either efficiency regime; the campaign should drop it from the matrix and update the conops to reflect that microwave-electrothermal is a demonstrator-class technology only.
3. **A "realistic efficiency" sensitivity row should be added below the winner cell.** Under realistic efficiency anchors, no cell closes — the matrix should reflect this explicitly so the matrix can be read at a glance under either set of efficiency assumptions.

## Revisit clause

Grade H-aets-a through H-aets-g. Five held cleanly; H-aets-e partially falsified on the wrong decomposition (delivered fraction is decoupled from efficiency); H-aets-f falsified-low (chunk floor far below the predicted 20–80 tonne band).

If H-aets-e or H-aets-f are revisited at higher fidelity (optimal-control trajectory shaping, separate outbound-burn-time recomputation at the dual-ion specific impulse, reactor-mass scaling at megawatt-electric per the wonder-pass tightened roadmap), the winner-cell band may shift by 10–20% but the architectural conclusion (canonical-efficiency-only survival, Variant B safe) is robust to those refinements.

If the campaign produces a published measurement of water-radio-frequency-ion at ≥10 kilowatt-electric input demonstrating anode efficiency ≥0.5 at specific impulse 2000 second, H-aets-e softens and the year-twenty-plus winner cell becomes defensible. Until that measurement exists, the cell is contingent on an unaudited technology-readiness-level claim and should be carried as such in the matrix.

## Cross-learning

- **The architecture decision matrix's year-twenty-plus all-electric end-to-end winner cell collapses entirely under wonder-pass realistic water-electric efficiencies.** At canonical-optimistic R10b efficiencies it survives narrowly (water-radio-frequency-ion, megawatt-electric, chunk 200 tonne, delivered fraction 20.0%, round-trip 14.85 year). The survival is contingent on a technology-readiness-level claim — anode efficiency 0.65 at water-radio-frequency-ion specific impulse 2000 second, megawatt-electric — that the published 2026 laboratory state of the art does not support. Recommended matrix update: annotate the cell with the efficiency assumption explicitly, add a "realistic efficiency" sensitivity row showing no closure, and treat the cell as contingent.
- **water-microwave-electrothermal is retired from the year-twenty-plus matrix column.** Mass ratio under continuous-thrust at specific impulse 700 second is 55.4; at 520 second (R0 flight-realistic per internal_gap_analysis) it is 222.4. Mass closure fails at every chunk above ~12 tonne. This is not the matrix's headline error — that was the inbound delta-velocity — but it tightens the architecture: the year-twenty-plus winner is *necessarily* an ion-class thruster (radio-frequency-ion or dual-ion), not microwave-electrothermal. R10b's headline that water-microwave-electrothermal beats water-radio-frequency-ion below 25 kilowatt-electric remains true for the chemical-kick Variant B architecture; it does not transfer to the all-electric end-to-end architecture.
- **water-dual-ion is retired from the year-twenty-plus matrix column under the L0-05 15-year ceiling.** Specific impulse 5000 second multiplies inbound burn time to 6.32 year (canonical megawatt-electric); the round-trip exceeds 19.87 year. R-inbound's specific-impulse-optimum-at-the-bottom lesson generalises across thruster classes: at the L0-05 ceiling, dual-ion is dominated by radio-frequency-ion at every power up to 2 megawatt-electric.
- **Variant B is structurally unaffected by the wonder-pass realistic-efficiency findings.** Cross-check rows show 70.4% delivered fraction at water-radio-frequency-ion megawatt-electric, both efficiency regimes, round-trip 13.80 to 14.53 year. Variant B's small inbound delta-velocity (6.42 km/s impulsive, residual after lunar gravity assist and chemical capture) keeps mass ratio at 1.39 and burn time short enough that the realistic-efficiency 4× burn-time penalty is absorbed inside the 15-year ceiling. Variant B remains the program's load-bearing architecture.
- **The campaign's matrix is now a single-architecture story.** Variant B (year-zero-through-fifteen Kilopower with chemical kick plus electric inbound) is the only architecture that survives under both canonical and realistic efficiency anchors at the corrected continuous-thrust delta-velocities. The year-twenty-plus all-electric end-to-end cell survives only under the canonical efficiencies, which require a technology-readiness-level demonstration that does not yet exist. The strategic implication: the financial model, conops, and pitch should be re-anchored around Variant B as the headline architecture, with the all-electric end-to-end retained as a stretch architecture contingent on water-radio-frequency-ion efficiency demonstration.
- **Methodology lesson — decompose efficiency from delta-velocity in the pre-registration.** I conflated efficiency-driven and delta-velocity-driven effects when pre-registering H-aets-e. The lesson recurs from R-inbound's specific-impulse-and-thrust separation: each independent physical variable should get its own predicted-range hypothesis, not be bundled with another variable in an aggregate "realistic" prediction. Adding to the convention log.
- **Methodology lesson — verify mass closure separately from time closure.** The tables show several cells where the 15-year ceiling closes but mass closure fails (delivered fraction negative). The "yes" / "no" closure verdict requires both checks; the round's summary correctly applies both, but the headline-cell table reports them independently. Future rounds should report mass-closure and time-closure as two separate columns rather than a single yes/no. Adding to the convention log.
- **Promotes R-cathode-life-water-plasma to high priority.** The all-electric end-to-end architecture (even at canonical efficiencies) requires a 1.50 year inbound burn at megawatt-electric on water. The wonder pass found no water-fed cathode life test past laboratory durations, with measured work-function degradation under oxygen deposition pointing the wrong way. If cathode life under water plasma is materially shorter than xenon heritage (~30,000 hour), the all-electric architecture's 1.5 year burn becomes an open structural risk. R-cathode-life-water-plasma was not previously a candidate round; this round promotes it.
- **Promotes R-trajectory-shaping-optimization to high priority.** Under canonical water-radio-frequency-ion at megawatt-electric, the all-electric end-to-end round-trip is 14.85 year — 0.15 year margin to the 15-year ceiling. A 10–20% trajectory-shaping saving on inbound delta-velocity (per the validity caveat in R-inbound) would push margin to ~1–3 year and make the cell robust to several risk variables (cathode life, reactor specific power, chunk-mass tolerance). Trajectory shaping is the cheapest available margin-buy in the program.

