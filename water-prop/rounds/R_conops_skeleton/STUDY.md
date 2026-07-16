# R-conops-skeleton — clean-room concept-of-operations rebuild from first principles

**Status:** structural sketch; load-bearing assumptions enumerated and queued as downstream rounds.

**Spawned:** 2026-05-16, Titan (re-spawn), user-directed.

## Why this round exists

Yesterday's marathon falsified the year-twenty-plus megawatt all-electric end-to-end cell and re-anchored radiator mass to NASA Modular Assembled Radiators numbers. R-reactor-roadmap and R-delivery-irr-curve then showed the marginal internal-rate-of-return on ICEBERG is 1.45 percent (sub-sovereign-bond) under MARVL-anchored mass, with sovereign-bond-floor crossover at ~220 tonnes per ship and corporate-growth crossover structurally unreachable on single-chunk-per-mission because B-ring single-chunk physical cap is ~482 tonnes.

The architecture matrix is in flux. The project owner asked to rebuild concept-of-operations from first principles — technology-neutral, requirement-shaped — so that subsequent architecture decisions get evaluated against a stable mission skeleton rather than against the prior matrix's assumptions.

This round documents the rebuild. The numbered-phase skeleton is the project owner's wording; the augmentation pass is Titan's recommendation; the load-bearing assumptions enumerated at the end are the queue for downstream rounds.

## The basic skeleton (project owner, technology-neutral)

| Phase | Event | Duration class |
|---|---|---|
| 1 | Earth surface → low Earth orbit | hours |
| 2 | Low Earth orbit → Saturn transfer maneuver (departure) | hours-to-months |
| 3 | Outbound cruise: trajectory adjustments, live telemetry | years |
| 4 | Arrive at Saturn, capture into Saturnian orbit | hours-to-months |
| 5 | Deploy ice chunk capture mechanism | hours-to-days |
| 6 | Capture ice chunk | hours-to-days |
| 7 | Start feeding main propulsion system from ice chunk | continuous |
| 8 | Saturn orbit → Earth transfer maneuver (departure) | hours-to-months |
| 9 | Inbound cruise: trajectory adjustments, live telemetry | years |
| 10 | Arrive at Earth, capture into Earth orbit | hours-to-months |

This is the contract. Each phase must happen for the mission to succeed. Phases are technology-neutral — they do not prescribe chemical vs electric vs nuclear, do not prescribe capture mechanism, do not prescribe orbit choice.

## Augmentations from the shake-test

Titan flags six gaps in the basic skeleton. Each is justified below; the augmented numbered list follows.

**Augmentation A — Phase 11 added (customer handoff).** Project requirement L0-02 specifies delivery to a customer interface in low or medium Earth orbit (250 to 35,786 kilometres altitude). "Arrive at Earth, capture into Earth orbit" is not the same event as "deliver water to a customer." The orbit a returning interplanetary vehicle can cheaply capture into (high-elliptical Earth orbit, or aerocapture into a phasing orbit) is almost never the customer's working orbit. Phase 11 is the propulsive (or aerodynamic) transfer from captured Earth orbit to customer interface orbit, plus the physical hand-off itself. Magnitude of the delta-velocity gap is the load-bearing question — pre-registered round queued below as R-conops-phase11-dv.

**Augmentation B — Phase 6.5 added (chunk processing).** Phase 7 as written ("start feeding main propulsion system from ice chunk") assumes the captured solid ice can become thruster-feedable propellant. Between solid chunk and thruster propellant there is at minimum: melt (chunk core temperature ~80 K at B-ring distance, needs to reach liquid for any flow), sieve / filter contaminants per L0-03 limits (≤ 1 ppm metals, ≤ 100 ppm organics), and store in a feedable form (tank with thermal management or sublimation buffer). Phase 6.5 carries its own power and thermal load profile and its own mass budget for the processing plant. Round 11 (silicate contamination) touched grid-life implications; the plant mass and continuous-thermal-power penalty are still open.

**Augmentation C — Phase 7 is a state, not an event.** Once phase 7 starts (chunk-fed propellant), it persists continuously through phases 8 and 9 and into phase 10. Under continuous-thrust electric architecture this is literally a months-to-years state. Under chemical-kick architecture it is a discrete propellant draw at phase 8 and again at phase 10. Either way, "start feeding" is a regime switch from Earth-launched propellant (used on phases 1, 2, optionally 3 / 4 / 5 / 6) to chunk-sourced propellant. Phase 7 in the augmented diagram is therefore drawn as a state-transition marker, with phases 8 / 9 / 10 happening *under* phase 7's regime.

**Augmentation D — Phase 4 sub-decision on capture location.** "Capture into Saturnian orbit" is at least three sub-decisions: (a) heliocentric arrival velocity reduction strategy (propulsive vs Titan aerocapture vs ring-grazing aerobraking); (b) target orbit family (Saturn-centric high-elliptical vs Saturn-centric low-circular vs moon-centric); (c) which orbit minimises phase-5-6 acquisition delta-velocity to B-ring while staying inside the project's mass and reliability budget. Sub-decision (a) sets the inbound impulsive delta-velocity at Saturn (range ~5–8 kilometres per second depending on encounter geometry); sub-decisions (b) and (c) bind the loiter time and the ring-traverse delta-velocity. Currently un-disambiguated in the basic conops.

**Augmentation E — End-of-mission state.** What does the vehicle do after phase 11? Re-enters and is destroyed (cheap, throws away ~$500 million per ship in built hardware). Parks in a graveyard orbit (mass-budget free, no further capability). Refuels at Earth and goes back to Saturn (steady-state cadence economics depend on this; L0-07's 2-per-year cadence with 13-year round-trips implies ~26 ships in flight simultaneously if every vehicle is single-use; ~13 if reused once). Decision binds vehicle design lifetime (radiation total dose, thermal cycling, structural fatigue) and the per-mission allocated cost basis. Open round candidate.

**Augmentation F — Contingency phases.** Phases 4 and 6 have non-trivial failure probabilities per R-mission-success-probability (single-string projected ~0.56 per-mission success). Specifically: phase 6 (ice capture) can fail because the chunk fragments, the bag tears, or the rendezvous geometry fails. The conops needs an explicit phase-6-abort branch: (a) attempt re-capture on a different chunk (cheap if still in B-ring orbit), (b) return empty (expensive; pays the inbound cruise but delivers zero water; potentially recoverable as a "cargo dry-run" demonstrator), (c) abandon vehicle at Saturn (cheapest in propellant, total write-off of capital). The conops as written assumes phase 6 succeeds first-pass.

## The augmented skeleton

| Phase | Event | Duration class | New? |
|---|---|---|---|
| 1 | Earth surface → low Earth orbit | hours | |
| 2 | Low Earth orbit → Saturn transfer maneuver | hours-to-months | |
| 3 | Outbound cruise: trajectory adjustments, live telemetry | years | |
| 4 | Arrive at Saturn — sub-decision on capture orbit family (3 sub-axes) | hours-to-months | sub-decisions called out (D) |
| 5 | Deploy ice chunk capture mechanism | hours-to-days | |
| 6 | Capture ice chunk | hours-to-days | |
| 6.5 | Process chunk into thruster-feedable propellant (melt / sieve / store) | continuous, starts here | **new (B)** |
| 7 | Regime switch: main propulsion system fed from chunk-sourced propellant | state, persists 7 → 10 | redrawn as state (C) |
| 8 | Saturn orbit → Earth transfer maneuver | hours-to-months | |
| 9 | Inbound cruise: trajectory adjustments, live telemetry | years | |
| 10 | Arrive at Earth, capture into Earth orbit | hours-to-months | |
| 11 | Transfer from captured Earth orbit to customer interface orbit; hand-off | hours-to-weeks | **new (A)** |
| 12 | End-of-mission state: re-enter / park / refuel-and-return | varies | **new (E)** |
| C1 | Phase-6 contingency: re-capture / return-empty / abandon-at-Saturn | as needed | **new (F)** |

That is the contract Titan recommends. Numbered phases 1–12 happen in sequence on a nominal mission. Contingency C1 is a branch off phase 6, present-but-dormant on a nominal mission.

## Load-bearing assumptions newly exposed by the augmentation

The augmented conops surfaces six assumptions that are either un-tested or worth re-testing under the new framing. Each is a candidate downstream R&D round.

| Assumption ID | Statement | Why load-bearing | Existing coverage | Round status |
|---|---|---|---|---|
| **A-ph11-dv** | Delta-velocity from cheap-capture Earth orbit to customer orbit gives phase-11 propellant < 5 percent of delivered chunk mass. | If false, phase 11 consumes 20–60 percent of delivered chunk mass and the L0-04 floor must absorb the loss. | **R-delivery-architecture** prices Architecture B's separate cislunar-tug leg (~Phase 11 equivalent) — 60–75 percent total delivered fraction with water-electric tug; 25–35 percent with hypergolic. **R-delivery-destination-altitude** establishes geostationary customer dissolves the continuous-thrust Edelbaum spiral and collapses phase 11 into phase 9. Titan's augmentation A is therefore architecture-conditional: phase 11 only exists as a separate phase under impulsive-capture architectures, not under all-electric-inbound (the project-owner-locked surviving cell). | **superseded — covered** |
| **A-ph6.5-mass** | Chunk processing plant (melt + sieve + storage) ≤ 5 tonnes per vehicle and ≤ 50 kilowatts continuous thermal. | Plant mass propagates into deep-space-vehicle dry mass, which compounds through Tsiolkovsky into propellant fraction. | **R-silicate-contamination** and **R-thermal-cooling** touch the sieve and thermal-management questions but not the plant-mass aggregate. Back-of-envelope thermal demand at 500-kilowatt-electric / 2000-second-specific-impulse mass flow is ~2 kilowatts continuous (melt-rate-bounded), so the 50-kilowatt ceiling is generous. Plant-mass figure is genuinely un-litigated but the hypothesis is plausibly held by a wide margin — low-value round. | **superseded — low-leverage** |
| **A-ph7-regime** | Phase 7 as continuous-state is compatible with both continuous-thrust electric and chemical-kick architectures. | Surviving cell is now all-electric-inbound per rhea-2 round 3; chemical-kick at Earth-arrival was falsified. Phase 7 regime under the locked architecture is well-defined. | **R-chunk-fed-chemical** + **R-chemical-trim-vs-all-electric-earth-arrival** resolve this. | **superseded — covered** |
| **A-ph4-orbit** | Cheapest Saturn capture orbit (high-elliptical, periapsis at B-ring) is also cheapest staging orbit for phase 5–6. | If false, an intra-Saturn delta-velocity penalty applies between phase 4 and phase 5. | **R-saturn-shadow-and-station-location** addresses station-orbit choice; **R-aerocapture** touches Saturn aerocapture; neither sweeps the phase-4 → phase-5 transfer specifically. Possible follow-on but moderate leverage. | **queued — moderate-leverage** |
| **A-ph12-reuse** | Vehicle reuse for a second mission saves more than refurbishment + refuelling cost. Steady-state fleet size at 2-per-year cadence with 13-year round-trip implies 26 vehicles in flight if single-use, ~9 if reused twice. | Drives per-mission capex amortization. Feeds directly into the R-reactor-roadmap and R-delivery-irr-curve numerator. Existing internal-rate-of-return rounds implicitly assume single-use (or never name the assumption). Reactor lifetime, radiator thermal cycling, and thruster grid erosion are the binding constraints — none are flagged in existing rounds. | **R-cadence-multiship** and **R-fleet-ramp-breakeven** look at fleet sizing but neither prices vehicle-reuse vs build-new. Un-litigated. | **running this session — R-conops-phase12-reuse** |
| **A-c1-contingency** | Phase-6 first-pass success probability is high enough that contingency C1 is not load-bearing on mission economics. | If contingency C1 fires > 20 percent of missions, marginal-internal-rate-of-return weighting needs the empty-return outcome explicitly. | **R-mission-success-probability** projects 0.56 per-mission. The 0.44 failure fraction includes phase-6 capture failure but does not weight the C1 sub-branch economics. Partial coverage. | **queued — moderate-leverage** |

## Round being run this session

**R-conops-phase12-reuse** — see `../R_conops_phase12_reuse/STUDY.md`.

Picked because it is the only one of Titan's six augmentations that is genuinely un-litigated by existing rounds, it directly tests Titan's own conops recommendation (phase 12 explicit), and the answer feeds straight into the R-delivery-irr-curve numerator which is currently the binding constraint on the program's economic case. If reuse is impossible (e.g., reactor lifetime caps at one mission), the marginal-internal-rate-of-return numbers in R-reactor-roadmap and R-delivery-irr-curve are roughly correct as-is. If reuse for 2–3 missions is viable, the program's economic case improves materially without any architecture change.

The cross-reference exercise above is itself a finding: of Titan's six conops augmentations, three are already covered by existing rounds (A-ph11-dv, A-ph7-regime, A-ph6.5-mass effectively), two are moderate-leverage queueable items (A-ph4-orbit, A-c1-contingency), and one is genuinely uncovered and high-leverage (A-ph12-reuse). The conops-from-first-principles exercise produced 1 of 6 net new R&D directions — modest but non-zero. The remaining value is the audit trail showing which augmentations were already addressed and where to look.

## Cross-learning

This round produces no numeric finding by itself. Its deliverable is the augmented skeleton above plus the queue of downstream rounds. Cross-learning lands as those rounds complete.

One methodology note: the basic-skeleton-then-augmentation discipline is a deliberate counter to the architecture-matrix style of the prior week. The matrix grew by accretion (rows added as the project owner discovered new technology choices); the conops here grows by enumeration of what the mission *requires* regardless of technology. When matrix rows die (as the year-twenty-plus megawatt row did yesterday), the conops is unaffected. When conops phases change (as Phase 11 just did by being added), every matrix row must answer the new requirement. The conops is the more stable layer.
