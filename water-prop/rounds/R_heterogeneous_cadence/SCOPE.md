# R-heterogeneous-cadence — does a fast-small mission 1 followed by larger-slower missions 2..N improve program NPV vs the homogeneous Variant B baseline?

**Status:** scope. Authored 2026-05-15 by rhea (re-spawn, sixth re-entry).
**Trigger:** project owner USER-NOTES block in `design-axes/02-surviving-cell.md` lines 18-20:
> "how about mission 1 is return a chunk, any size chunk, as fast as possible, using water as the propellant, and keeping everything else constant, but then subsequent vehicles can take longer round trips, which would eventually get us into the green right? lets test this hypothesis"

## Hypothesis under test

A heterogeneous mission schedule — small chunk in mission 1 (returned as fast as possible), then progressively larger chunks in missions 2..N — improves program-level NPV vs the homogeneous baseline (every mission is identical Variant B 500-kWe / 200-t chunk / 14.5-yr round-trip / 80 t delivered). The proposed mechanism is **discount-rate front-loading**: pulling revenue earlier in the program is worth more in present-value terms.

The counter-mechanism is **delivered-mass loss**: a smaller mission 1 chunk delivers a much smaller absolute mass; the smaller-revenue mission must be more than compensated by the earlier-arrival discount-rate gain. Quantitative bracket on this trade is the first task this round must do (lessons #1, #5, #8).

A secondary mechanism, which the project owner did not explicitly cite but which is the natural reason this question is worth asking: **real-options gating**. If missions 2..N are conditional on mission-1 success (in the sense that the fleet capex for missions 2..N is committed only after mission 1 demonstrates closure), the fleet-build PV outflow shifts later in time AND is probability-weighted by P(mission 1 succeeds). This is a different structural NPV move than pure front-loading and is included as a separate hypothesis arm.

## What this round answers

1. Under deterministic accounting (mission 2..N fleet capex committed at year 0 in the build ramp regardless of mission 1 outcome), does a fast-small mission 1 schedule improve program NPV vs the homogeneous Variant B baseline at any (WACC, learning-rate, clearing-price) combination tested?
2. Under real-options accounting (mission 2..N fleet capex contingent on mission-1 success, probability-weighted by P(mission 1 succeeds)), does the schedule improve program NPV?
3. What does the minimum-time mission-1 trip look like for the Variant B vehicle architecture (500 kWe, water electric propulsion, water-as-only-propellant constraint)? Specifically: at what chunk mass is mission-1 round-trip minimized, and what is that minimum?
4. Is there a heterogeneous schedule that crosses sovereign-bond NPV (WACC 3%) at clearing prices where the homogeneous baseline does not? Per R-LEO-water-demand-curve (commit `ed3dd58`), Variant B homogeneous clears 51% of the 2030s clearing-price distribution at sovereign WACC 3% with LR 15% — so the test is whether the heterogeneous schedule lifts that fraction.

## What this round does NOT do

- Does not change the **propulsion physics** of Variant B. The vehicle is 500-kWe water-electric per project-owner Option A lock. No chemical kick, no higher-Isp ion, no alternate working fluid.
- Does not test architectures other than Variant B. Architecture E (200/500 kWe, longer round-trips, smaller-or-equal chunks) is not the target of the user-notes hypothesis (user said "everything else constant" — Variant B is the surviving cell to which "constant" most plausibly refers).
- Does not vary the chunk-mass cap upward. L1-007 stands at 200 t. Mission 1 chunks are ≤ 200 t; missions 2..N also ≤ 200 t.
- Does not model time-evolution of clearing price (R-clearing-price-time-evolution carryover from R-LEO-water-demand-curve thread #25 is still pending).
- Does not model staged commitment with continuous decision points (real-options arm here is binary: gate at mission 1, decide go/no-go for whole fleet). A more sophisticated real-options model is **R-staged-commitment-NPV** (R-fleet-ramp-NPV pending thread #20).
- Does not credit chunk-as-heat-shield, aerocapture, or aerobraking for any mission. Variant B is all-electric end-to-end per the surviving-cell definition.
- Does not address per-mission reliability (L0-10) beyond using P(mission 1 succeeds) as a real-options arm input. The 90% per-mission reliability stays as the per-mission baseline.
- Does not propose changes to L1-007, L0-05, or any other requirement.

## Method sketch (full pre-registration in STUDY.md)

1. **Build a single-knob chunk-vs-round-trip-vs-delivered-mass parametric for Variant B at 500 kWe, water Isp 2000 s, all-electric end-to-end.** Derive scaling from R_inbound_dv_continuous_thrust at 1 MWe (which has a chunk-mass sensitivity sweep at 100/200/500 t) and scale by power. Cross-check against R_fleet_ramp_NPV Variant B baseline (chunk 200 t / 14.5 yr / 80 t delivered).
2. **Define heterogeneous schedules.** Sweep mission-1 chunk mass ∈ {25, 50, 100, 150, 200} t; for each, compute (round-trip-1-yr, delivered-1-t). Missions 2..N stay at baseline (200 t / 14.5 yr / 80 t). Schedule cadence: 2/yr.
3. **Extend R_fleet_ramp_NPV's engine to support a per-mission schedule** rather than a homogeneous one. Single-flight first; reusable as sensitivity.
4. **Sweep:** mission-1 chunk × WACC × Wright's-Law LR × clearing-price × accounting-regime (deterministic vs real-options). Compute program NPV per cell.
5. **Compare:** heterogeneous program NPV vs homogeneous program NPV at the same (WACC, LR, clearing-price). Heterogeneous wins if Δ-NPV > 0 with sign-flip on financing eligibility ranking.
6. **Cross-checks:** at mission-1 chunk = 200 t (homogeneous limit), Δ-NPV must equal zero within machine precision. At WACC = 0 the discount-rate-gain mechanism must vanish; only delivered-mass-difference dominates.

## Deliverables

- `water-prop/rounds/R_heterogeneous_cadence/STUDY.md` — pre-registration + result + grading + reading.
- `water-prop/rounds/R_heterogeneous_cadence/run.py` — deterministic sweep.
- `water-prop/rounds/R_heterogeneous_cadence/results/` — JSON summary committed; CSV gitignored.
- Handoff at `~/.claude/handoffs/iceberg-rhea-YYYYMMDD-het-cadence.md`.

## Cross-references

- `design-axes/02-surviving-cell.md` USER-NOTES lines 18-20 — origin of the hypothesis.
- `water-prop/rounds/R_fleet_ramp_NPV/run.py` and STUDY.md — NPV engine to extend; homogeneous baseline reference cells.
- `water-prop/rounds/R_LEO_water_demand_curve/STUDY.md` — clearing-price distribution under which to evaluate Δ-NPV; specifically the headline 51% / 29% sovereign / corporate P(NPV+) for homogeneous Variant B.
- `water-prop/rounds/R_inbound_dv_continuous_thrust/STUDY.md` — chunk-mass sensitivity for round-trip and delivered fraction (at 1 MWe; scale to 500 kWe).
- `water-prop/rounds/R_variant_B_500kWe_sizing/STUDY.md` (hyperion) — 500-kWe-is-optimum-for-Variant-B finding; constrains the reactor-power knob.
- `water-prop/rounds/R_variant_B_100t_resizing/SCOPE.md` (phoebe, not run) — closely related question at chunk 100 t under Variant A (no recovery). Different from this round (Variant B vs Variant A, single-chunk sweep vs schedule comparison).

## Sequencing

This round can run in parallel with R-expected-NPV-posterior-times-clearing-price (the other load-bearing follow-on from R-LEO-water-demand-curve). Output of this round feeds the matrix axis 02-surviving-cell and axis 17-pitch-capital-framing if Δ-NPV is materially positive in any arm.
