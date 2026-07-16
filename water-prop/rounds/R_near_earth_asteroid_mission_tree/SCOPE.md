# R-near-earth-asteroid-mission-tree — encode the NEA architecture as a second tree in the mission_graph forest, then compare to saturn_water_v0

**Status:** scope, pre-study. Authored by Saturn (orchestrator), 2026-05-22 latest+15 → 16, walking `SATURN-PUNCH-LIST-20260521.md` items M-2 + S-2 + design-axis 21.

---

## Why this round

`water-prop/sims/mission_graph/` was designed as a forest of mission graphs — multiple architectures sharing the same phase-graph substrate but using different option sets, different ephemerides, and different revenue functions. Saturn-worker implemented one tree (`saturn_water_v0`) and validated the framework against it. A second tree is now overdue for three independent reasons:

1. **Architectural comparator** (design-axis 21, created this pass). The matrix needs a side-by-side throughput comparison for Saturn-ring water versus the most-credible alternative architecture. Phoebe R-mission-architecture-pivot-survey (`bb570d7`) classified 31 of 31 candidates DEAD-ON-ARRIVAL under conservative anchors and 7 as F6-conditional WORTH-DEEP-DIVE under iapetus-style probabilistic reactor-program-availability treatment. The near-Earth-asteroid candidate is one of those 7. A dedicated mission tree closes the comparator with a quantitative throughput verdict instead of a categorical triage.
2. **Architectural-sleep insurance.** If decision points #14 + #15 resolve toward campaign-terminating options at flyable power, ICEBERG needs a successor architecture on the shelf rather than starting from scratch. Near-Earth-asteroid retrieval has flown samples (Hayabusa2, OSIRIS-REx) and has a serious reference architecture (Keck Institute for Space Studies 2012 Asteroid Retrieval Feasibility Study). This round produces the framework substrate for a successor program without committing ICEBERG to it.
3. **Framework-load test.** A second tree exercises the framework's "forest of mission graphs" abstraction. If the second tree shares >70 percent of its phase executors with `saturn_water_v0`, the framework is well-designed; if it shares <30 percent, the abstraction is leaky and the framework needs a structural redesign before more architectural rounds land on it.

**Round type:** framework engineering (encode a second mission tree) + comparator analysis (run mining_view.py across both trees and produce a Pareto-front-style comparison).

---

## The locked anchors this round must respect

These are saturn-worker wonder-pass findings (commit `030cb5e`) and design-axis 21 Current section content. The round MUST anchor against them, not litigate them:

1. **Main belt is geometrically incompatible with trawl architecture.** Particle number density is ~10^20 times lower than Saturn ring annuli; water is bound in phyllosilicate clays not free ice; only ~4 of ~700,000 catalogued main-belt objects sit below 7 kilometres-per-second rendezvous delta-velocity. **Main-belt is not a target for this round; the round encodes near-Earth-asteroid only.**
2. **Near-Earth-asteroid low-delta-velocity envelope.** 5-9 kilometres-per-second round-trip for low-delta-velocity near-Earth asteroids. **2008 EV5 at 6.29 kilometres-per-second rendezvous is the canonical low-delta-velocity target** for the Keck Institute for Space Studies reference architecture. Other candidates in the 5-9 kilometres-per-second band exist; the round may sweep across a small candidate set.
3. **Near-Earth-asteroid water content.** 1-10 percent water by mass in carbonaceous chondrite phyllosilicates per Bennu (OSIRIS-REx returned 121.6 grams 2023) and Ryugu (Hayabusa2 returned 5.4 grams 2020) sample analyses. **Water is bound, not free ice; extraction is thermal (400-700 °C) not scoop-and-melt.**
4. **Keck Institute for Space Studies 2012 reference architecture.** 28:1 in-mass-amplification to low-Earth orbit for the 7-metre, 500-tonne boulder case. Solar-electric propulsion (40-kilowatt-electric class), 6-10 year round-trip. This is the strongest single reference for the architecture; the round reproduces it as the baseline cell before sweeping variants.
5. **Lunar polar in-situ resource utilization** is the most-cited competitor (axis 21 Current). 5.6 ± 2.9 percent water best-case (LCROSS Cabeus), ~1 percent average; ~4.6 kilometres-per-second round-trip with aerobraking (axis 04 latest+15 correction). Lunar is NOT this round; it is the third tree if and when it gets a SCOPE of its own.

---

## The question this round answers

**Under current-technology constraints, does the near-Earth-asteroid architecture close at higher per-mission throughput, higher per-tonne IRR, or shorter program-NPV-positive cadence than `saturn_water_v0`, and at what L0-04 floor does each architecture cross over?**

Three decompositions:

1. **Per-mission throughput.** Delivered water mass per mission, round-trip time. Anchor on Keck Institute for Space Studies 28:1 in-mass-amplification for the 7-metre boulder case; sweep across boulder size (1-15 metres), bound-water mass fraction (1-10 percent), and thermal-extraction efficiency (60-95 percent).
2. **Per-tonne IRR.** Pricing-anchor-dependent. Use the same demand curve and clearing-price Monte Carlo as the Saturn-ring rounds; near-Earth-asteroid mission cost may be substantially lower than Saturn (no Saturn-system insertion, shorter cruise) but per-mission delivered mass is also lower (Keck Institute for Space Studies 28:1 amplification gives ~14 tonnes delivered from a 500-tonne boulder, well below L0-04 25 tonne provisional floor).
3. **Program-NPV-positive cadence.** Time-to-program-NPV-positive at fleet ramp. Faster round-trip allows more missions per unit time; smaller per-mission delivery requires more missions to meet a given annual throughput. Sweep cadence at fleet sizes 1-10 vehicles.

The round's deliverable is a **side-by-side Pareto front** comparing `saturn_water_v0` and the new `near_earth_asteroid_v0` mission tree across the three decompositions, with a Reading at the bottom identifying the L0-04 floor below which near-Earth-asteroid dominates and above which Saturn-ring dominates.

---

## Pre-registered hypotheses (worker's honest predictions)

| # | Hypothesis | Predicted range | Falsification band |
|---|---|---|---|
| H1 | Reproducing the Keck Institute for Space Studies 2012 baseline (7-metre boulder, 500 tonnes, solar-electric propulsion, 6-10 year round-trip) in the mission_graph framework yields 14 ± 4 tonnes delivered to low-Earth orbit per mission at 28:1 in-mass-amplification ratio. The 28:1 number assumes ~1.8 percent water by mass extracted at 90 percent efficiency from a 500-tonne carbonaceous-chondrite boulder. | Framework-reproduced baseline: 10-18 tonnes delivered per mission; 7-11 year round-trip. | H1 falsified if framework reproduction differs from Keck Institute for Space Studies headline by > 50 percent on delivered mass or > 30 percent on round-trip. |
| H2 | At L0-04 = 25 tonnes provisional, near-Earth-asteroid baseline does NOT close (delivers ~14 tonnes, below floor). To close the floor, near-Earth-asteroid requires either (a) a larger boulder (>~15 metre, ~3000 tonne; outside Keck Institute for Space Studies-validated envelope) or (b) a higher water-mass-fraction target (>5 percent; carbonaceous-chondrite typical is 1-3 percent, Ryugu was 0.4 percent), or (c) L0-04 waiver to ~15 tonnes. | Near-Earth-asteroid at Keck Institute for Space Studies baseline: below L0-04 = 25 tonne floor; closes at L0-04 = 15 tonnes. | H2 falsified if a credible Keck Institute for Space Studies-envelope near-Earth-asteroid configuration delivers ≥ 25 tonnes per mission. |
| H3 | Per-mission cost for near-Earth-asteroid is 30-60 percent of Saturn-ring per-mission cost. Eliminated: Saturn-system insertion (~$200M-400M Δv penalty), Saturn-cruise reactor lifetime burden (multi-year full-power burn), B-ring rendezvous hardware. Retained: vehicle bus, solar-electric propulsion, thermal extraction module, return capsule. Total per-mission cost bracket: $400M-$800M (versus Saturn-ring $1.0B-$1.5B at conservative anchors). | Near-Earth-asteroid per-mission cost: $400-$800M; per-tonne $/kg at L0-04 = 25-tonne-equivalent fleet: $20-50/kilogram. | H3 falsified if per-mission cost exceeds $1.0B (loses cost advantage) or per-tonne $/kg exceeds $80 (loses pricing-anchor competitiveness). |
| H4 | Faster round-trip cadence (~7 years near-Earth-asteroid versus ~14 years Saturn-ring) trades against smaller per-mission delivery. At a fleet of 5 vehicles, near-Earth-asteroid annual throughput is 50 tonnes per year; Saturn-ring is 75 tonnes per year (titan-3 closing band, 50-60 tonne delivered, 14-year round-trip). Saturn-ring wins on annual throughput at conservative anchors. | Near-Earth-asteroid fleet=5 annual throughput: 40-65 tonnes per year; Saturn-ring: 60-100 tonnes per year. | H4 falsified if near-Earth-asteroid annual throughput exceeds Saturn-ring at any fleet size ≤ 10. |
| H5 | Phoebe R-mission-architecture-pivot-survey's F6-conditional WORTH-DEEP-DIVE classification of near-Earth-asteroid stands at quantitative analysis. The architecture closes at credible engineering anchors but NOT at higher throughput than Saturn-ring under conservative L0-04. It is a successor-program candidate, not a Saturn-ring replacement at the same L0 requirements. | Reading-level: near-Earth-asteroid is successor-candidate-credible; not Saturn-ring-replacement-credible at L0-04 = 25 tonnes. | H5 falsified if near-Earth-asteroid dominates Saturn-ring on annual throughput AND per-tonne IRR AND program-NPV-positive cadence at L0-04 = 25 tonnes. |
| H6 (load-bearing reading) | Near-Earth-asteroid is **architecturally distinct enough** from Saturn-ring that the framework abstraction holds. >70 percent of phase executors are shared (cruise, Earth arrival, on-orbit assembly, lunar-orbit sub-mission). The new tree adds 3-4 phase executors specific to near-Earth-asteroid (rendezvous, boulder-acquisition, thermal-extraction module, near-Earth-asteroid departure to Hohmann transfer). Framework substrate validates; future architectures (lunar-polar, Mars-orbit-tug, gas-giant-system) can land as further trees without structural redesign. | Framework abstraction holds: >70 percent phase executor share between saturn_water_v0 and near_earth_asteroid_v0. | H6 falsified if shared phase-executor fraction is <30 percent (framework abstraction is leaky and needs structural redesign before further architectural rounds). |

---

## Method (worker drafts the actual implementation)

**Step 1 — Boulder-candidate set.** Identify 5-10 near-Earth asteroids in the 5-9 kilometres-per-second rendezvous-delta-velocity band. Reference: JPL Small-Body Database query, NHATS (Near-Earth Object Human Space Flight Accessible Targets Study) list. Canonical anchor: 2008 EV5 at 6.29 kilometres-per-second. Secondary candidates: 2009 BD, 2010 GA6, others below 7 kilometres-per-second.

**Step 2 — Boulder physical properties.** For each candidate, document size, estimated mass, spectral class (carbonaceous chondrite C-type is the target; M-type metallic asteroids do not have bound water), rotational state. Reference: spectrophotometry literature, Hayabusa2 / OSIRIS-REx returned-sample analyses for water-mass-fraction anchor.

**Step 3 — Encode near_earth_asteroid_v0 mission tree.** Reuse `saturn_water_v0` phase executors where applicable (Phase 0 Earth-to-LEO, Phase 0b on-orbit assembly, Phase 1 trans-Saturn-injection becomes trans-near-Earth-asteroid-injection, Phase 5 inbound cruise, Phase 6 Earth arrival, Phase 7 lunar processing). Add four near-Earth-asteroid-specific phase executors under `water-prop/sims/mission_graph/missions/phase3_nea_rendezvous.py`, `phase3b_boulder_acquisition.py`, `phase3c_thermal_extraction.py`, `phase4_nea_departure.py`. Document the shared-executor count for H6.

**Step 4 — Encode Keck Institute for Space Studies baseline cell.** Set boulder = 7 metre / 500 tonne, water-mass-fraction = 1.8 percent, thermal-extraction efficiency = 90 percent, solar-electric propulsion = 40 kilowatt-electric, round-trip target = 6-10 years. Verify the framework reproduces 14 ± 4 tonnes delivered per H1.

**Step 5 — Sweep across boulder size × water-mass-fraction × extraction efficiency × fleet size.** Cell ranges: boulder size {3, 5, 7, 10, 15} metres; water-mass-fraction {0.4 percent (Ryugu), 1.8 percent (Keck Institute for Space Studies anchor), 3 percent (carbonaceous-chondrite typical), 5 percent (high anchor), 10 percent (optimistic ceiling)}; extraction efficiency {60, 75, 90} percent; fleet size {1, 3, 5, 10}. Total ~ 5 × 5 × 3 × 4 = 300 cells.

**Step 6 — Run mining_view comparison.** Use `water-prop/sims/mission_graph/analysis/mining_view.py` (already exists, used for saturn_water_v0 sweep). Add a comparator mode that takes two mission tree sweep outputs and produces a Pareto-front-style comparison across the three decompositions (per-mission throughput, per-tonne IRR, program-NPV-positive cadence). Use the same demand curve and clearing-price Monte Carlo as enceladus-r5 R-LEO-water-demand-curve (`ed3dd58`).

**Step 7 — Cross-over identification.** For each decomposition, identify the L0-04 floor at which the two architectures cross over. Document as a small table in RESULTS.md. The cross-over is the load-bearing input for the project-owner decision on whether to file near-Earth-asteroid as a serious comparator (axis 21 Open question).

**Step 8 — Phoebe-pivot-survey reconciliation.** Cross-check the round's verdict against phoebe R-mission-architecture-pivot-survey's classification of near-Earth-asteroid as F6-conditional WORTH-DEEP-DIVE. Confirm or refine. If the quantitative analysis says near-Earth-asteroid is NOT credible even at F6-favorable, that retires the candidate; if it confirms F6-conditional credibility, the candidate stays on the shelf as a successor architecture.

---

## Out of scope

- Lunar polar in-situ resource utilization. Lunar is the third tree if and when it gets its own SCOPE.
- Main-belt water. Geometrically incompatible with trawl per locked saturn-worker wonder-pass finding; not a target.
- Combined water + platinum-group-metals mission. Saturn-worker wonder-pass found this is geophysically incoherent (where the metals are, the water isn't); not a target.
- Resolving project-owner decision points #14 or #15. This round produces a successor-architecture comparator; it does not resolve the Saturn-ring program's open architectural questions.
- Mining-economics modeling beyond what `mining_view.py` already supports. If a richer NPV model is needed, that's a separate round.

---

## Inputs to acquire (reading order)

1. `water-prop/sims/mission_graph/README.md` — framework overview.
2. `water-prop/sims/mission_graph/missions/saturn_water_v0.py` — reference tree to mimic for structure.
3. `water-prop/sims/mission_graph/analysis/mining_view.py` — comparator substrate.
4. `design-axes/21-architecture-source-comparator.md` — anchor for the comparator framing.
5. `water-prop/rounds/R_mission_architecture_pivot_survey/` (phoebe `bb570d7`) — F6-conditional classification to reconcile against.
6. Keck Institute for Space Studies 2012 Asteroid Retrieval Feasibility Study (Brophy et al., 2012 KECK-NEA-Retrieval-Architecture.pdf if accessible).
7. JPL Small-Body Database + NHATS list for boulder candidate set.
8. Hayabusa2 + OSIRIS-REx sample-analysis papers for water-mass-fraction anchor.
9. Saturn-worker wonder-pass beliefs ingestion record (commit `030cb5e`).

---

## Deliverables (in commit order)

1. `STUDY.md` — pre-registered hypotheses H1-H6 frozen before running the framework sweeps.
2. Boulder candidate set + physical properties table — `inputs/nea_candidates.csv`.
3. Phase executor implementations (Step 3) — separate commits per new executor.
4. `near_earth_asteroid_v0` mission tree — `water-prop/sims/mission_graph/missions/near_earth_asteroid_v0.py`.
5. Keck Institute for Space Studies baseline cell reproduction — `tests/test_kiss_baseline_reproduction.py`.
6. Sweep output — `results/nea_sweep.json`.
7. Comparator output — `results/comparator_pareto.csv` + `results/comparator_pareto.md`.
8. `RESULTS.md` — sweep summary + cross-over table + phoebe-pivot-survey reconciliation.
9. `READING.md` — load-bearing reading (H6 verdict); successor-architecture filing recommendation.
10. Handoff doc to orchestrator (`~/.claude/handoffs/iceberg-<worker>-<date>-nea-mission-tree.md`).

---

## Suggested worker

Any moon. Best fit: comfortable with framework engineering (mostly mimic-and-adapt from `saturn_water_v0` shape) + small-body astronomy + asteroid-mission literature. Phoebe would be a good fit (already has the pivot-survey context). Titan-3 would be a good fit (recent comfort with the framework's vis-viva machinery from R-delta-velocity-anchor-audit).

---

## Cross-references

- Matrix `water-prop/docs/ARCHITECTURE-DECISION-MATRIX.md` — new axis 21 (Architecture source comparator) entry, and High-leverage open rounds section flag for `R-near-earth-asteroid-mission-tree` (punch-list M-2 / S-2).
- Design-axes `design-axes/21-architecture-source-comparator.md` — Current and Open question sections frame this round's deliverable.
- Punch list `SATURN-PUNCH-LIST-20260521.md` items M-2 + S-2 + D-4.
- Phoebe R-mission-architecture-pivot-survey (`bb570d7`) — F6-conditional WORTH-DEEP-DIVE classification of near-Earth-asteroid.
- Saturn-worker wonder-pass commit `030cb5e` — anchors for near-Earth-asteroid delta-velocity envelope, water-mass-fraction, thermal-extraction, Keck Institute for Space Studies reference architecture.
