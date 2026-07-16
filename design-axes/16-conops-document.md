---
axis: "Concept-of-operations document"
status: open
confidence: medium
last_revised: 2026-05-22
related:
  - "[[outbound-launch-architecture]]"
---

# Concept-of-operations document

## Current

`ICEBERG-conops.md` is legacy; titan-2 has begun a clean-room rebuild via R-conops-skeleton. Project owner has annotated the legacy conops with nine review notes (seven plot-quality, two substantive: Starship-vs-SLS framing, 750-tonne feasibility).

**2026-05-22 latest+18 — DEMONSTRATOR CONOPS SKETCH AVAILABLE (hyperion R-demonstrator-mission-concept `61afe0c`):** non-nuclear scaled-down demonstrator with vehicle dry 4-6 tonnes, low-Earth-orbit launch 15-30 tonnes on one Falcon Heavy partial-reuse, target chunk at Saturn 5-10 tonnes, delivered to low-Earth orbit 1-3 tonnes (any non-zero per REQUIREMENTS §7.5), round-trip 12-15 years, power RTG ~1-3 kilowatt or solar-inner + RTG-Saturn hybrid (bet #3 deferred — non-nuclear). **Propulsion test article: commercial water RF-ion (2000 s) + bag sublimation-distillation filtration stack on dirty chunk water — NOT the power-appropriate MET (~543 s) a small low-power vehicle would naturally fly.** Demonstrator sequence: (1) Earth-orbit catch-and-contain proxy with deployable target mass — pre-cruise — retires deployment + catch + containment at mm/s; (2) continuous-months RF-ion run on bag-filtered chunk water during the Saturn cruise — dominant-kill long pole, demonstrator IS bet-#2's test article; (3) reactor deferred off the critical path. Full sketch at `water-prop/rounds/R_demonstrator_mission_concept/results/conops_sketch.md`. This is a NEW companion conops document distinct from `ICEBERG-conops.md` (commercial-class) and from titan-2's clean-room rebuild — it is the demonstrator-class conops for the internal-demonstrator tranche-1 path matrix decision #13 latest+18 amendment specifies.

## Open question

When does titan-2's rebuild reach a state that can replace the legacy conops?

## Last touched by

- titan-2 R-conops-skeleton — `6aec601`
- titan-2 R-conops-phase12-reuse — `d29a4d9`
- project-owner conops review notes 2026-05-15
- hyperion R-demonstrator-mission-concept — `61afe0c` (demonstrator conops sketch: non-nuclear, vehicle 4-6 t / chunk 5-10 t / commercial RF-ion + bag, Earth-orbit proxy FIRST then Saturn small-chunk)

## HISTORY

### 2026-05-15 — Initial scaffold from `ARCHITECTURE-DECISION-MATRIX.md` current-decision-state table

Status: open. Confidence: medium.

Current state and open question captured from the matrix's top section as of commit `9704700`. Full audit trail of how this axis arrived at its current state is in the matrix HISTORY section (`water-prop/docs/ARCHITECTURE-DECISION-MATRIX.md`).

---

<!-- Append-only HISTORY entries go below this line. Each entry: ### YYYY-MM-DD — round-name or commit-hash — one-line summary -->
