# R-mission-architecture-pivot-survey — STUDY

**Author.** phoebe
**Date.** 2026-05-18 (current campaign latest; written after iapetus latest+10 settlement of program-class)
**Round type.** Triage / pivot-survey. Worker-round-appropriate scope is enumerate-and-filter against existing campaign evidence, not deep-dive simulation. Output is decision input for the project owner.
**Anchor.** Phoebe STATE.md recommendation (2026-05-15) to promote R-mission-architecture-pivot-survey as next critical-path round, plus iapetus round-5 statement (worktree-105823 commit `af8eb91`) that "the remaining genuinely-untested questions are not worker-round-appropriate" — this round treats those as a constraint, not a contradiction, by being explicitly triage-not-deep-dive.

---

## Pre-registration anchor audit (lesson 9 application — 5th instance)

This round depends on three prior aggregate verdicts. Per methodology lesson 9, I anchor on each round's aggregate-verdict primary text, not on convenient sub-findings.

1. **Phoebe 5-round chunk-rendezvous death chain.** Aggregate held-strong over 4,808 unique closure-checks across 5 rounds. Verdict text: "the held chunk-rendezvous architecture is now five-way confirmed-non-closing... phoebe is now demonstrably out of internal levers to interrogate." Reading this round: candidate A (held chunk-rendezvous baseline) and any subordinate that depends on chunk-rendezvous capture physics is presumed DEAD-ON-ARRIVAL.

2. **Iapetus 4-round + retraction chain on `worktree-105823` (`0516f70` + `07f7674`).** Aggregate held: H6 (technology-demonstrator-only program-class) is robust under any plausible joint prior profile (each prior ≤ 0.93). Venture-class crossing requires five independent ≥ 0.93 priors simultaneously — 1378× baseline lift. **Round 5 explicitly retracts the round-4 "structurally over-determined" framing.** Reading this round: candidates do NOT need to lift program-class to venture; tech-demonstrator framing is already the anchor. Survival means "produces something at tech-demonstrator capital class" or "requires a project-owner-reframe to be evaluable."

3. **Project-owner axis-19 closure 2026-05-15 latest+6.** Axis 19 closed at chunk-rendezvous; ram-scoop residence-class explicitly retired on the grounds that +14.7 km/s Saturn-side Δv defeats ICEBERG's "chunk-as-propellant-tank" foundational lever. Reading this round: candidate B (ram-scoop) and any other architecture that violates this foundational lever is classified REQUIRES-PROJECT-OWNER-REFRAME, not DEAD-ON-ARRIVAL — the closure was a decision, not a falsification, and phoebe's chunk-rendezvous-death evidence has substantively changed the input.

## Phoebe-self-audit (lesson 9 reflexive application)

The STATE.md recommendation "promote R-mission-architecture-pivot-survey to next critical-path round" was written before phoebe knew that iapetus had settled program-class and titan had run R_deployable_drag_skirt (FALSIFIED). Two implicit phoebe-assumptions in that STATE.md that this round needs to catch:

- **Implicit assumption A1:** there exists an alternative mission architecture that closes venture-class. Iapetus's chain shows venture is structurally unreachable. The survey scope is therefore "alternatives that close tech-demonstrator," not "alternatives that close venture." Lower bar.
- **Implicit assumption A2:** R-deployable-drag-skirt is the named architectural-recovery candidate for aerocapture closure. R_deployable_drag_skirt (round commit on this worktree) shows peak heat flux 1,431 kW/m² at best-case beta=100, areal=15 kg/m² — 3–4× HIAD-2 and LOFTID heritage tolerances. So drag-skirt as a chunk-rendezvous rescue is already dead, and so is candidate H (aerocapture-conditional) unless the chunk itself is the heat shield (which is itself separately falsified by R_chunk_as_heat_shield).

Both reframings sharpen the survey: the question is not "which candidate restores venture-class," it is "which candidates produce a defensible tech-demonstrator program given the chunk-rendezvous death + drag-skirt death + ram-scoop project-owner-retirement?"

---

## Scope

Triage ~28 candidate mission architectures against 8 kill criteria derived from existing campaign evidence. Produce per-candidate verdict: **DEAD-ON-ARRIVAL** (kill criterion already met by cited evidence) / **WORTH-DEEP-DIVE** (not killed by existing data; warrants a dedicated worker round) / **REQUIRES-PROJECT-OWNER-REFRAME** (architecturally inconsistent with current L0 / project-owner-stated framing; can only be reopened by project-owner decision).

Coarse, citation-based desk study. No Basilisk, no Monte Carlo. Each (candidate × criterion) verdict cites the source round and its verdict. Round produces a recommendation table for the project owner.

## Kill criteria

| ID | Criterion | Threshold | Source round / belief |
|---|---|---|---|
| F1 | Inbound Δv closure under continuous-thrust electric | ≤ ~6.42 km/s impulsive-equivalent; phoebe round notes that under continuous thrust this is 24.7–40.2 km/s | `R_inbound_dv_continuous_thrust` |
| F2 | B-ring crossing survivability for chunk-bearing vehicle | Bag-aperture per-pass intercept ≤ 1% extended-aperture | phoebe 5-round chain (commits `abdcd35`, `45869d4`, `8a31ba9`, `75ba925`) |
| F3 | L0-05 round-trip ≤ 14 yr (strict) or ≤ 15 yr (waiver) | 14 yr strict per L0-05 | `R12_lunar_GA_both_legs` (closes), `R9_slow_trajectory_tof` (does not), `R_cruise_time_optimization` (Variant C closes) |
| F4 | Saturn-side Δv compatible with chunk-as-propellant-tank lever | Project-owner direction: residence-class +14.7 km/s defeats foundational lever | axis-19 2026-05-15 latest+6 decision; `R_conops_chunk_vs_ram_scoop` |
| F5 | Saturn-side process power feasible (~150 kWe-class for 1-yr electrolysis) | Either fission or solar-thermal-electrolysis at < 200 kg/kW conservative | `R_non_fission_baseline`, `R_saturn_side_solar_thermal` |
| F6 | Reactor program / specific-power availability for demonstrator window 2032-2035 | Posterior on megawatt-class fission delivery by 2035: 0.07–0.20 across 3 priors | `R_megawatt_architecture_viability`, locked beliefs (FSP Phase 2 not awarded; 0-of-6 US base rate; 40 W/kg paper-only; MARVL radiator 40-55% of MWe mass) |
| F7 | Foundational-lever consistency: cargo serves as inbound propellant tank | Project-owner direction (axis-19 closure) requires preservation of this lever | axis-19 history block; `R_conops_chunk_vs_ram_scoop` |
| F8 | Capital-class threshold at tech-demonstrator capital class (NOT venture) | Iapetus settlement: each subjective prior ≤ 0.93 cap; venture requires 5-fold ≥ 0.93 joint assertion | iapetus chain `0516f70` + `af8eb91` |

A candidate is **DEAD-ON-ARRIVAL** if ≥ 1 criterion fails with cited evidence AND no plausible architectural-recovery is available.

A candidate is **REQUIRES-REFRAME** if ≥ 1 criterion fails but only because it conflicts with a *project-owner-stated* anchor (F4 or F7), and the project owner could in principle reopen the relevant decision.

A candidate is **WORTH-DEEP-DIVE** if no criterion fails with cited evidence (UNKNOWN cells permitted) AND the candidate is not redundant with an existing surviving cell.

## Candidate enumeration (28 total)

### Baseline / chunk-rendezvous family (4)
- **A**: Held chunk-rendezvous (phoebe baseline)
- **A′**: Chunk-rendezvous + deployable drag-skirt aerocapture (was axis-19 named recovery)
- **A″**: Outer-ring chunk-rendezvous (A-ring τ≈0.5 or F-ring τ≈0.1)
- **H**: Aerocapture-conditional chunk-rendezvous (single-pass per `R_megawatt_aerocapture_engineering_closure`)

### Ram-scoop / residence-class family (2)
- **B**: Ram-scoop residence-class (project-owner retired)
- **B′**: Residence-class at outer-ring (A-ring/F-ring residence instead of B-ring)

### Capture-physics alternatives (3)
- **P1**: Lunar-orbit catcher (intercept chunks at lunar orbit; processing cislunar)
- **P3**: Tether-rendezvous (rotating tether passive grapple)
- **P4**: Active push-the-rock (lander → boost stage on chunk)

### Source alternatives (7)
- **S1**: Enceladus plume sampling (water from south-pole geysers)
- **S2**: Mimas surface ice mining
- **S3**: Iapetus surface ice mining
- **S4**: Hyperion surface ice mining (porous body)
- **S5**: Tethys surface ice mining
- **S6**: Phoebe surface ice (irregular satellite, comet-class composition)
- **S7**: Saturn-system Trojan / Hilda water-ice (outside ring system)

### Time-domain alternatives (2)
- **T1**: Very slow low-energy cruise (relaxes Δv; costs L0-05)
- **T2**: Chunk pre-staging at intermediate moon (Iapetus or Mimas parking orbit, then phase-2 push to Earth)

### Form-factor / delivery-target alternatives (4)
- **F1d**: Return propellant (H₂/O₂) not water (Architecture D)
- **F2d**: Return as bulk ring material aggregate (functionally ram-scoop output)
- **F3d**: Many small chunks instead of one big (heterogeneous cadence)
- **F4d**: Deliver to L4/L5/GEO/lunar-orbit instead of LEO

### Commercial-model alternatives (3)
- **C2c**: Precursor mission (smaller water target, sell heritage to follow-on)
- **C3c**: Shared launch / cost-split with other Saturn customers
- **C4c**: Data-resource mode (smaller water as proof-of-concept; primary revenue from sensor data + heritage)

### Mission-architecture alternatives (3)
- **M2m**: One-way ships (no return; deliver chunk and abandon vehicle)
- **M3m**: Tug-and-go fleet (one tug per chunk; tug stays at Saturn permanently)

### L0-reframe alternatives (4 — all REQUIRES-REFRAME by construction)
- **L1r**: Drop 14-yr round-trip cap (L0-05 waiver)
- **L2r**: Drop chunk-as-propellant-tank premise (enables F2d-class architectures)
- **L3r**: Drop 100% Earth-delivery target (deliver 30%, leave rest as in-flight propellant; closes Tsiolkovsky)
- **L4r**: Drop "Earth orbit" delivery target (lunar / L4-L5 only; supports propellant-economy customer not water-end-user)

(Note: total 32 after expansion. Candidates with the same effective physics are folded — A′ = P2-deployable-skirt, B′ ≈ partial-A″, F2d ≈ B; the run.py applies criteria uniformly.)

---

## Pre-registered hypotheses

**Convention:** H-pas-N where pas = "pivot-architecture-survey." Per PROTOCOL.md, each predicts a numeric verdict before run.

### H-pas-1: Most candidates land DEAD-ON-ARRIVAL

**Prediction:** 20-26 of 32 candidates classify DEAD-ON-ARRIVAL by ≥ 1 cited criterion. Most kills are F3 (round-trip) or F4/F7 (foundational-lever) or F6 (reactor program).

Wrong if < 15 DEAD-ON-ARRIVAL: I am over-counting the constraint-network's coverage. Wrong if > 28 DEAD-ON-ARRIVAL: the four L0-reframe candidates probably should not classify DEAD-ON-ARRIVAL by definition.

### H-pas-2: Specifically these candidates die

Per-candidate pre-registered verdict (recorded HERE before run.py executes):

| Candidate | Predicted verdict | Predicted killing criteria |
|---|---|---|
| A | DEAD-ON-ARRIVAL | F2 (phoebe 5-round chain) |
| A′ | DEAD-ON-ARRIVAL | F2 + drag-skirt thermal (R_deployable_drag_skirt) |
| A″ | UNKNOWN→WORTH-DEEP-DIVE | F2 plausibly relaxed at lower τ (F-ring τ=0.1) but rotation period / chunk-population at outer ring unverified |
| H | DEAD-ON-ARRIVAL | F2 (chunk-rendezvous unchanged) + F6 (1000 kWe per `R_megawatt_aerocapture_engineering_closure`) |
| B | REQUIRES-REFRAME | F4 + F7 (project-owner direction; +14.7 km/s defeats lever) |
| B′ | REQUIRES-REFRAME | same as B; outer-ring residence still adds Saturn-side Δv |
| P1 | DEAD-ON-ARRIVAL | F1/F3 inbound (chunks still need to reach Earth-Moon system; phoebe physics unchanged for delivery leg) |
| P3 | DEAD-ON-ARRIVAL | F2 (tether-rendezvous in B-ring same passage problem) |
| P4 | DEAD-ON-ARRIVAL | F2 (landing rendezvous requires same B-ring transit) |
| S1 | WORTH-DEEP-DIVE | Enceladus plume avoids ring crossing; new physics; not tested |
| S2-S5 | WORTH-DEEP-DIVE (provisional) | Surface mining changes the capture problem; F3 likely binding (slower cadence) |
| S6 | DEAD-ON-ARRIVAL | Phoebe is at 215 R_S (retrograde orbit); transit + capture geometry similar to Trojans S7 |
| S7 | DEAD-ON-ARRIVAL | Saturn Trojans at 5.2-9.5 AU; transit times worse than current architecture; F3 binding |
| T1 | DEAD-ON-ARRIVAL | F3 (R9_slow_trajectory_tof gives 24-yr realistic round-trip) |
| T2 | WORTH-DEEP-DIVE | Pre-staging changes commit-timing problem; not directly killed by F-criteria |
| F1d | DEAD-ON-ARRIVAL | F8 program-NPV (R_architecture_D_cost: 0/48 cells defined IRR; R_architecture_D_L1007_relaxation: program-NPV negative across 168 cells) |
| F2d | REQUIRES-REFRAME | Same as B; bulk ring material was the ram-scoop output |
| F3d | DEAD-ON-ARRIVAL | R_cadence_multiship + R_heterogeneous_cadence falsified |
| F4d | DEAD-ON-ARRIVAL | R_delivery_destination_altitude: only 5.2 pp GEO vs LEO; not architecture-changing |
| C2c | WORTH-DEEP-DIVE | Precursor framing changes capital-class anchor; not directly killed |
| C3c | WORTH-DEEP-DIVE | Shared-launch changes outbound launch-mass multiplier (R_outbound_architecture 6.9× → ?) |
| C4c | WORTH-DEEP-DIVE | Data-resource framing not yet tested |
| M2m | WORTH-DEEP-DIVE | One-way changes round-trip closure; not directly killed |
| M3m | DEAD-ON-ARRIVAL | F8 (one tug per chunk = cadence stretched dramatically; per R_cadence_multiship IRR -1.45% at N=5) |
| L1r | REQUIRES-REFRAME (by construction) | F3 relaxation = project-owner decision |
| L2r | REQUIRES-REFRAME (by construction) | F7 relaxation = project-owner decision |
| L3r | REQUIRES-REFRAME (by construction) | Foundational L0 target relaxation |
| L4r | REQUIRES-REFRAME (by construction) | Delivery target relaxation |

### H-pas-3: Aggregate worth-deep-dive count

**Prediction:** 4-7 candidates land WORTH-DEEP-DIVE after triage. Specifically, my best guess is:
- A″ (outer-ring chunk-rendezvous) — UNKNOWN-conditional on F-ring chunk population
- S1 (Enceladus plume) — UNKNOWN-conditional on plume mass-flow at vehicle-class collection rates
- S2-S5 (one or two of these) — UNKNOWN-conditional on surface-mining cadence
- T2 (pre-staging) — UNKNOWN-conditional on commit-timing
- C2c, C3c, C4c (one or two) — UNKNOWN-conditional on capital-structure inputs
- M2m (one-way ships) — UNKNOWN-conditional on revenue model

Wrong if < 2 worth-deep-dive: I'm under-counting novel architectures. Wrong if > 10: I'm under-applying the kill criteria.

### H-pas-4: Specifically these L0-reframe candidates are the load-bearing reframes

**Prediction:** Of the 4 L0-reframe candidates, exactly L1r (drop 14-yr cap) and L3r (drop 100% Earth-delivery) constitute genuinely novel decision space for the project owner that the matrix has NOT already represented as cells. L2r is the ram-scoop reframe under another name (already explicit decision-point). L4r is closely related to F4d (delivery-altitude), which is shown to be ≤ 5.2 pp.

Wrong if more than two of {L1r, L2r, L3r, L4r} land "genuinely novel": the L0 reframe space is wider than I estimated.

### H-pas-5: Aggregate aggregate

**The held chunk-rendezvous architecture has no architectural successor at tech-demonstrator-or-better capital class without at least one project-owner-level reframe.** The survey will produce ≤ 1 WORTH-DEEP-DIVE candidate that doesn't depend on a project-owner reframe in the L0 set.

Wrong if more than 1 fully-clean candidate (no project-owner reframe required, no UNKNOWN cells in kill criteria) survives: the campaign's architectural search space is more open than I think.

---

## Method

`run.py` codes the 32 candidates and 8 kill criteria as data. For each (candidate, criterion) cell:

- Apply the cited threshold to the candidate's parameter values
- Verdict ∈ {PASS, FAIL, UNKNOWN}
- Per-FAIL cell: cite source round + one-sentence rationale

Per-candidate aggregate:

- 1+ FAIL on F1-F6 → DEAD-ON-ARRIVAL
- 1+ FAIL only on F4 or F7 → REQUIRES-REFRAME
- All PASS or UNKNOWN → WORTH-DEEP-DIVE
- Mixed FAIL on (F4 or F7) AND (F1-F3 or F5-F6) → DEAD-ON-ARRIVAL (the F1-F3/F5-F6 kill dominates)

Results JSON: per-cell verdict + per-candidate aggregate + summary counts.

closure_verdict.md: hypothesis-by-hypothesis grading + aggregate verdict + WORTH-DEEP-DIVE candidates' proposed follow-on rounds.

## Pre-registered runtime

~5 minutes wall clock for the per-cell sweep (data-defined, no physics integration).

## Cross-learning preview

If H-pas-5 holds, the campaign's recommendation to the project owner is: **the architectural search has been exhausted at the worker-round level; reopening any cell requires a project-owner-level reframe of one or more L0 requirements.** This is precisely iapetus's round-5 conclusion ("project-owner-level reframing, not further worker-round sensitivity"). Phoebe's triage corroborates iapetus's conclusion from the alternative-architecture-search angle, which is the angle iapetus didn't run.

If H-pas-5 fails (≥ 2 fully-clean WORTH-DEEP-DIVE candidates), the campaign has genuinely novel architectural search space remaining and iapetus's "exhausted at worker-round level" framing is too tight.
