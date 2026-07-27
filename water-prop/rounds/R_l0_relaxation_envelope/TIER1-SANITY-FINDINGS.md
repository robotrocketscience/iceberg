# R-l0-relaxation-envelope — Tier 1 in-session findings

**Round:** R-l0-relaxation-envelope (Tier 1 sanity sweep, in-session)
**Date:** 2026-05-26 latest+25
**Author:** Saturn (orchestrator, in-session execution)
**Predecessor:** project-owner question 2026-05-26 — "how would we relax L0 requirements while still being within the spirit of the mission?"
**Tier:** sanity check only. Proper pre-registered round SCOPE'd separately.

## Headline

**No combination of L0 relaxations brings back commercial closure under the closed-loop framework as currently parameterised. Zero paths even arrive at the Earth-orbit depot — across all 1,744 attempted paths in the 150-cell saturn_water_v1 closure sweep, every path fails at some upstream precondition.** The L0-04 (mass floor), L0-05 (round-trip ceiling), and L0-24 (reactor-on-contract) relaxations are moot at the current framework fidelity because the bottleneck is upstream of every L0 they would relax.

## What was tested

Ran `saturn_water_v1` closed-loop closure sweep:
- 6 power-class values: 1, 10, 11, 20, 30, 55 kilowatts-electric (covers RTG-class through Kilopower-extrapolation)
- 5 chunk-mass values: 10, 25, 50, 100, 200 tonnes
- 5 electric-thrust values: 1, 2.5, 5, 10, 25 newtons
- 150 cells total, 1,744 paths total

Closure checked against L0-04 floors of {10, 20, 30, 50, 100} tonnes crossed with L0-05 ceilings of {15, 20, 25, 30, no-ceiling} years.

## Closure table — closed-loop framework

```
 floor_t | <=15yr | <=20yr | <=25yr | <=30yr | any RT
-----------------------------------------------------
    10t |      0 |      0 |      0 |      0 |      0
    20t |      0 |      0 |      0 |      0 |      0
    30t |      0 |      0 |      0 |      0 |      0
    50t |      0 |      0 |      0 |      0 |      0
   100t |      0 |      0 |      0 |      0 |      0
```

Zero closures everywhere. Zero paths even arrive at LEO depot.

## Where the paths die

Failure distribution across the 1,744 attempted paths:

| Phase | Paths failed here | Top failure reasons |
|---|---:|---|
| P0 Earth-to-LEO | 660 | wet vehicle exceeds launcher capacity (Falcon Heavy 63.8 t, Starship 100 t, 2x-Falcon-Heavy 100 t) |
| P1 LEO-to-Saturn cruise out | 445 | electric thruster minimum power (>= 20 kilowatts-electric required, available 1-11 kWe at some cells); chemical propellant insufficient for trans-Saturn injection delta-v |
| P4 Saturn departure | 408 | chunk-fed water-electrothermal needs power >= 30 kilowatts-electric (have 20); chemical propellant insufficient for trans-Earth injection |
| P0b assembly | 180 | passthrough-no-assembly flag set when assembly required; depot-relay assembly requires existing LEO depot |
| P2 Saturn capture | 36 | gravity-assist arrival velocity below minimum thresholds |
| P1b cruise ops | 15 | gravity-assist phase preconditions |

**Zero paths reach inbound cruise (P5), Earth arrival (P6), or LEO depot (P7).**

## Why — the structural issue

The closed-loop framework derives vehicle dry mass from per-subsystem demands (titan-6's refactor). Combined with the framework's frozen 0.80 propellant fraction, this gives derived wet mass per cell:

| Power kWe | Chunk 10 t | Chunk 50 t | Chunk 200 t |
|---:|---:|---:|---:|
| 1 (RTG-class) | 138 t | 211 t | 483 t |
| 10 | 176 t | 248 t | 521 t |
| 30 (Kilopower-extrapolation) | 259 t | 332 t | 604 t |
| 55 | 363 t | 436 t | 708 t |

**No cell produces a wet vehicle under the single Falcon Heavy expended cap (63.8 t).** Even the smallest case (1 kWe RTG + 10 t chunk) is 138 t wet — over 2x Falcon Heavy capacity, over 1.4x Starship capacity, over 1.4x 2-Falcon-Heavy multi-launch raw capacity.

Multi-launch + on-orbit autonomous assembly is the only way to get a 138+ tonne vehicle to LEO. The base parameters use `multi_falcon_launch_count = 6` (382 t LEO capacity, enough for everything except the 55 kWe / 200 t cell at 708 t). But the framework's path-walker hits assembly preconditions that don't pass cleanly — 180 paths die on assembly-flag mismatches.

Paths that DO get past assembly then fail on power-class preconditions: electric thrusters require >= 20 kilowatts-electric for cruise legs, and chunk-fed exit propulsion requires >= 30 kilowatts-electric. At lower power classes (1, 10, 11 kWe — the non-nuclear regime), most propulsion phases reject the cell as infeasible regardless of L0 relaxation.

## Implications for the L0 relaxation question

The relaxations I sketched in the previous orchestrator analysis (drop L0-04 to 5-10 t, stretch L0-05 to 20-25 yr, vacate L0-24 via non-nuclear power, relax L0-07 cadence, relax L0-12 cost-competitive) **cannot be tested against the closed-loop framework at current fidelity** because zero paths even arrive at the L0-04 / L0-05 / L0-12 measurement point.

The bottleneck has moved upstream:

1. **Vehicle wet mass dominates.** Even the smallest credible configuration (RTG + 10 t chunk) needs multi-launch + assembly, and the framework's current assembly logic doesn't pass cleanly.
2. **Power-class preconditions on propulsion phases are tight.** The non-nuclear regime (1-11 kWe) fails most electric-cruise phases that require 20+ kWe.
3. **The 0.80 propellant fraction is doing real work.** Titan's D5 coordination flag at handoff: "the 0 cells arrive is sensitive to the frozen 0.80 propellant fraction (heavier dry mass cannot do the 7.3 km/s chemical departure at 80%). Collapse direction is robust; completeness is not convention-independent." This finding corroborates titan's flag.

**Until R-vehicle-mass-fidelity-refinement runs (titan's D5 successor — derive propellant per-phase from delta-velocity, audit Wertz anchors, path-conditional thermal protection), the L0-relaxation question is not answerable at the closed-loop framework fidelity.**

The honest reading: structural verdict (the closed-loop framework finds the campaign's commercial closure space empty) survives. The "even smaller-floor cells might close" softener from decision #16 is now also under threat — those cells need to ARRIVE before closure floor matters, and zero arrive.

## What this means for the campaign

Three readings, ranked by confidence:

1. **The closed-loop framework is over-pessimistic at current fidelity** (titan D5 flag): the 0.80 propellant fraction is too tight for the heavier closed-loop dry mass, and per-phase propellant fraction derivation would relax this. R-vehicle-mass-fidelity-refinement H1 tests this directly. Most likely reading; the relaxations probably DO bring back some closure once propellant accounting is honest.

2. **Multi-launch assembly logic in the framework has a configuration issue** that's making paths fail prematurely. Worth a fresh look from titan or hyperion — maybe a one-line fix to the assembly preconditions, maybe a missing precondition match.

3. **The structural verdict is even stronger than titan-6 reported**: not just "no cell closes L0-04 = 25 t" but "no cell delivers anything anywhere even with maximum spirit-preserving L0 relaxations." Less likely (lessons 21 + 22 say the closed-loop is more honest than open-loop, not necessarily over-pessimistic), but worth flagging as a possibility.

## Recommended next moves

1. **Proper round R-l0-relaxation-envelope (pre-registered, post-fidelity-refinement)** — SCOPE'd this pass, waits for R-vehicle-mass-fidelity-refinement to land first.
2. **Quick framework audit on the assembly preconditions** — is `multi_falcon_launch + autonomous_assembly` actually reachable on the canonical path? 180 path failures at P0b suggest a configuration issue worth a 30-minute investigation.
3. **The strategic answer remains:** demonstrator-class under §7.5 waiver is the operative programmatic path. The commercial-class L0-relaxation analysis is a sensitivity test on a verdict that's already been called.

## Limits + threats to validity

- The 0.80 propellant fraction is a framework convention, not physics. Test sensitivity in R-vehicle-mass-fidelity-refinement before treating this round's verdict as final.
- The P0b assembly precondition behavior may be a framework bug rather than a physics finding. Worth confirming before publishing.
- L0-12 (cost-competitive) and L0-07 (cadence) relaxations were not directly testable here — the framework doesn't carry pricing or production-rate axes at the cell level. Those relaxations remain in the proper-round SCOPE.

## Artifacts

- `relaxation_sweep.py` — the sanity-check script
- `results/relaxation_sweep.json` — raw closure table
- `SCOPE.md` (next file) — proper pre-registered round, gated on R-vehicle-mass-fidelity-refinement
