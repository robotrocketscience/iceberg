---
axis: "Saturn-side capture mode"
status: falsified
confidence: high
last_revised: 2026-05-22
related:
  - "[[09-chunk-mass-cap]]"
  - "[[01-program-class]]"
  - "[[19-capture-architecture]]"
---

# Saturn-side capture mode

## Current

B-ring direct (BR-direct) is the only operationally accessible soft-capture orbit at zero relative velocity. High-eccentric-Saturn-graze (HE-graze) is falsified (titan-2 R-HE-graze-feasibility `b2e7a35`).

**B-ring rendezvous crossings give ~99 percent per-pass impact probability** under zone-averaged optical-depth ~ 2 (titan-2 R-saturn-soi-periapsis-depth H5, `1b1b889`). **Engineered survivability falsified at all four mitigation levers** (phoebe R-bring-rendezvous-survivability `abdcd35`, 2026-05-16 merge `b5c5d61`: 0 of 162 cells; bag-armour does not change geometric impact probability; cull-mesh drops it only to ≥ 7.2% per pass in chunk-bearing zones; off-plane Δv to 90° costs 4.55 km/s round-trip but lowest impact prob still 720× target; slow-cross is non-monotonic with floor at relative velocity 9 km/s above Whipple limit). Verdict robust under self-questioning: R-bring-survivability-relaxed (`45869d4`, 0 of 126 cells × 5 thresholds × 2 treatments × 2 crossings) confirms even allocating the entire L0-10 budget to B-ring crossings (non-defensible) does not flip any chunk-bearing cell; extended-aperture treatment **sharpens** the verdict by 4-6 orders of magnitude. R-bag-aperture-chunk-joint (`8a31ba9`, 0 of 2160 cells) confirms bag-aperture × chunk-mass joint relaxation does not rescue any cell.

**Binding obstruction:** chunk-population vs safe-passage co-location problem — chunk-bearing zones (B-ring τ ≥ 0.30) stay impact probability ≥ 20% per pass even at 90° + cull-mesh; safe-passage zones (Cassini-Division gaps, outermost edge) contain no large particles. The only configuration with non-fatal per-impact kinetic energy is ring-orbit-match (residence-class, 14.7 km/s round-trip Saturn-side Δv), which was project-owner-retired at latest+6 because it defeats the chunk-as-propellant-tank delta-velocity-minimization lever.

**2026-05-22 latest+18 — Earth-orbit catch-and-contain proxy is the highest-leverage pre-cruise retirement of A14 chunk-capture risk (hyperion R-demonstrator-mission-concept `61afe0c`):** per lesson-16 classification, bet #1 (chunk capture) is the highest-leverage gate (cheap, pre-cruise, Earth-orbit catch-and-contain proxy with deployable target mass lifts A14 joint from 0.53 to 0.69 by retiring 3-of-5 sub-steps — deployment, catch, containment — without leaving low-Earth orbit). The demonstrator sequence is (1) Earth-orbit proxy FIRST; (2) Saturn small-chunk capture (1-10 tonne) with full telemetry retires rendezvous-at-Saturn + short-duration survive. Note this is the demonstrator-class retirement path; the underlying B-ring rendezvous engineering-survivability falsification (held chunk-rendezvous architecture) is NOT relieved by the demonstrator. The demonstrator retires capture-mechanism risk in a smaller-chunk lower-energy regime; the B-ring impact-probability problem is geometric and architecturally distinct. Axis 12 status held at falsified on the held architecture; the Earth-orbit proxy is the lesson-16-highest-leverage way to retire A14 risk in a different regime, not a rescue of the held architecture's B-ring problem.

## Open question

**Engineering survivability closed-negative at all defensible thresholds and all mitigation levers.** Axis is closed-negative on the held chunk-rendezvous architecture. The only remaining substantive Saturn-side capture mode is residence-class (project-owner-retired latest+6) or a pivot architecture (e.g. catcher-at-Saturn, alternative-source) per R-mission-architecture-pivot-survey — both displace this axis rather than resolving it.

Status was "closed" pre-2026-05-15 latest+5, "open" at latest+5 when the B-ring impact-prob risk surfaced, and now "falsified" at latest+8 after engineering survivability closes at all four mitigation levers + bag-aperture-chunk-mass joint relaxation.

## Last touched by

- titan-2 R-HE-graze-feasibility — `b2e7a35`
- titan-2 R-saturn-soi-periapsis-depth — `1b1b889` (H5 surfaced B-ring rendezvous impact-prob risk)
- titan-2 R-bring-fine-structure-rendezvous — `201e2c2` (ram-scoop reframe surfaced and retired per project-owner direction)
- Project-owner decision 2026-05-15 latest+6 (matrix decision point #6 resolution)
- phoebe R-bring-rendezvous-survivability — `abdcd35` (engineered survivability falsified at all four mitigation levers)
- phoebe R-bring-survivability-relaxed — `45869d4` (verdict robust under self-questioning at thresholds + treatments + crossings)
- phoebe R-bag-aperture-chunk-joint — `8a31ba9` (bag-aperture × chunk-mass joint relaxation does not rescue any cell)
- hyperion R-demonstrator-mission-concept — `61afe0c` (Earth-orbit catch-and-contain proxy is lesson-16-highest-leverage pre-cruise retirement of A14 risk; not a B-ring rescue, a regime-distinct demonstrator)

## HISTORY

### 2026-05-15 — Initial scaffold from `ARCHITECTURE-DECISION-MATRIX.md` current-decision-state table

Status: closed. Confidence: high.

Current state and open question captured from the matrix's top section as of commit `9704700`. Full audit trail of how this axis arrived at its current state is in the matrix HISTORY section (`water-prop/docs/ARCHITECTURE-DECISION-MATRIX.md`).

### 2026-05-15 latest+5 — titan-2 R-saturn-soi-periapsis-depth (`1b1b889`) — B-ring rendezvous impact-prob risk surfaced

H5 of the SOI round computed B-ring rendezvous crossing impact probability under zone-averaged optical-depth ~ 2. Result: ~99 percent per-pass. Orthogonal to HE-graze falsification (the HE-graze finding was about relative velocity at periapsis; this is about geometric impact prob at the rendezvous orbit). Status flipped from closed to open: new load-bearing engineering question added.

### 2026-05-15 latest+6 — Project-owner decision on capture architecture

Project owner directed: hold chunk-rendezvous architecture (axis 19 capture-architecture, see that axis file). Ram-scoop reframe retired. This axis remains open on the B-ring-rendezvous-impact-prob engineering question, which is now inherited as a load-bearing engineering risk on the held chunk-rendezvous architecture.

---

<!-- Append-only HISTORY entries go below this line. Each entry: ### YYYY-MM-DD — round-name or commit-hash — one-line summary -->

### 2026-05-18 latest+8 — phoebe rounds 3-6 (merge `b5c5d61`) — engineered survivability falsified at all four mitigation levers + bag-aperture × chunk-mass joint relaxation

Three commits address the engineering question surfaced in latest+5. R-bring-rendezvous-survivability (`abdcd35`, 0 of 162 cells): no combination of bag-armour + cull-mesh + off-plane inclination + slow-cross closes the impact-prob target. Lowest chunk-bearing impact prob 7.23% per pass (B-ring outermost 180 km × cull-mesh × 90° inclination), 723× the per-crossing target. Binding obstruction is the chunk-population vs safe-passage co-location problem (chunk-bearing zones τ ≥ 0.30 keep impact prob ≥ 20% per pass even at 90° + mesh; safe-passage zones — Cassini-Division gaps, outermost edge — contain no large particles). R-bring-survivability-relaxed (`45869d4`, 0 of 126 cells across 5 thresholds × 2 treatments × 2 crossings): verdict robust to self-questioning; even allocating the entire L0-10 mission-failure budget to B-ring crossings (non-defensible) does not flip any chunk-bearing cell. Extended-aperture treatment SHARPENS the verdict by 4-6 orders of magnitude (point-vehicle treatment understates real risk). R-bag-aperture-chunk-joint (`8a31ba9`, 0 of 2160 cells): bag-aperture × chunk-mass joint relaxation does not rescue any cell on the 5-constraint aggregate. Status flipped open / high → falsified / high.

### 2026-05-18 latest+11 — phoebe R-particle-distribution-q-sensitivity (`75ba925`, 2026-05-16 backfilled 2026-05-18) — verdict robust across literature q range; fifth convergent falsification

Self-questioning round 4 (= phoebe round 7 of session) interrogated the N(D) ∝ D⁻³ particle-size-distribution exponent anchor used in three prior phoebe rounds. 540-cell sweep across q ∈ {2.5, 2.7, 3.0, 3.3, 3.5, 4.0} per Cassini Cuzzi/Tiscareno/Hedman measurements × τ-zone × mesh × inclination. **0 of 540 cells close at strict or moderate threshold at any q.** "Target high-q location" architectural-rescue path foreclosed because high-q B-ring locations (B3 core q ≈ 3.3 per Hedman & Stark 2015) also carry τ ≈ 4.5, which overwhelms the q-rescue even with 1m mesh.

Two opposing direction-of-bias effects partially cancel and produce smaller-than-predicted sensitivity to q. Methodology footnote candidate: interrogate symmetric-looking assumptions because the sensitivity may surprise you.

Cumulative phoebe falsification arc on held chunk-rendezvous architecture now five-way convergent (threshold, mesh, extended-aperture, single-vs-double crossing, bag-aperture × chunk-mass joint, particle-size-distribution exponent). Phoebe demonstrably out of internal-assumption levers to interrogate. Axis status held at falsified/high.
