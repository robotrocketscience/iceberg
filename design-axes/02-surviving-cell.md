---
axis: "Surviving cell at conservative anchors"
status: open
confidence: high
last_revised: 2026-05-22
related:
  - "[[program-class]]"
  - "[[round-trip-ceiling]]"
  - "[[saturn-side-process-power]]"
  - "[[chunk-mass-cap]]"
  - "[[reactor-power-floor]]"
---

# Surviving cell at conservative anchors

## Current

**2026-05-22 latest+18 RETIRED-AS-FULL-ROUND-TRIP-CLOSURE:** titan-4 R-framework-matrix-parity (`0eb11a7`) encodes the four matrix-carried constraints (reactor lifetime versus cumulative burn; Modular Assembled Radiators for Very Large systems bundled radiator mass; conservative 2000-kilogram bus floor; vis-viva LEO capture burn) into `water-prop/sims/mission_graph/` and shows that titan-3's closure cells were **inbound-only accounting**. Framework full-round-trip delivers ~half titan-3's stated tonnage (50-tonne chunk → 19.4 tonnes constraints-OFF vs titan-3's 35.6 tonnes), and constraints-ON the 200-tonne closure cell collapses to **0 surviving cells at conservative anchors** across the entire 1-55 kilowatt-electric flyable envelope. Two independent killers: powerplant dry-mass floor (50 t vehicle / 10 t dry cannot carry 22.8 t reactor at 30 kilowatt-electric / 2.4 watts-per-kilogram; bigger vehicles don't deliver ≥30 t even baseline); reactor lifetime (200-t chunk at 30 kilowatt-electric needs 14-16 yr cumulative burn). H1 + H2 both fall at every L ∈ {5, 10, 15, ∞} × specific power ∈ {2.4, 5, 10}. The framework brackets cleanly between titan-3 (generous, inbound-only) and enceladus-r5 (pessimistic, shielding-penalised; +16 percent reproduction). **titan-3's cells are preserved as valid inbound-leg analysis** but are not full-round-trip closure cells. **Under both strict and soft readings of the locked-memory directive, no full-round-trip cell survives at flyable power.** Prior closure-history (latest+13) preserved below.

**latest+13 INBOUND-ONLY CLOSURE (preserved as data input, no longer state-of-record):** A surviving cell exists at 40-80 tonne chunks + 20-30 kilowatt-electric Kilopower-extrapolation + R12 lunar-gravity-assist Earth-arrival + corrected vis-viva delta-velocity anchors (titan-3 R-chunk-size-pareto `1997a51`, 2026-05-19) — **inbound-leg only, not full round-trip.** 4 cells close L0-05 strict + L0-09 commercial floor at chunk 50-60 tonnes / P=30 kilowatt-electric; 30 cells close at L0-05 waiver across 50-150 tonnes / 20-30 kilowatt-electric. Delivered 30-60 tonnes per mission, round-trip 14-22 years. **Three tensions:** (1) 30 kilowatt-electric is outside titan-3's own 1-10 kilowatt-electric "flyable Kilopower-extrapolation" envelope from R-kilowatt-class-power-envelope earlier the same day, and outside the locked-memory "Kilopower-class single-kilowatt at best" envelope — whether 30 kilowatt-electric is defensibly Kilopower-extrapolation or quietly re-imports the retired 500 kilowatt-electric fantasy is a project-owner call (see decision point #14 in matrix); (2) the closure architecture is pure-electric throughout with R12 lunar-gravity-assist Earth-arrival, NOT hybrid chemical-electric leapfrog (the leapfrog headline was retracted by R-delta-velocity-anchor-audit at 200-tonne scale); (3) Earth aerocapture is NOT in the closing architecture — phoebe's 0-of-1920 verdict is irrelevant to this cell, but the 10-flyby lunar-gravity-assist tour has its own per-flyby risk budget that has not yet been audited. **Under STRICT reading of the locked-memory directive (single-kilowatt Kilopower at best), the surviving cell does NOT exist in the actually-flyable power envelope and the prior "none at conservative anchors" reading still holds.** Prior closure history preserved: hyperion R-no-atmospheric-capture-baseline (`1ce7c89`) found 0 cells across 288-cell sweep with aerocapture removed; phoebe R-hybrid-aerocapture-aerobraking (`1623cca`) 0 of 1920 cells under three failure modes; phoebe pivot-survey (`bb570d7`) 31/31 DEAD-ON-ARRIVAL under conservative anchors.

## Open question

Whether titan-3's 40-80 tonne / 30 kilowatt-electric closure cell counts as a surviving cell under the locked-memory directive is the load-bearing project-owner question. Soft reading ("30 kilowatt-electric Kilopower-extrapolation is acceptable; the directive was specifically about 500 kilowatt-electric"): a surviving cell exists; axis 02 status should bump to closed at the conservative anchor 30 kilowatt-electric Kilopower-extrapolation; pitch / matrix / requirements all re-derive around 40-80 tonne chunks. Strict reading ("Kilopower-class single-kilowatt at best per the feedback memory"): the surviving cell does NOT exist in the actually-flyable envelope; axis 02 stays open and the prior "none at conservative anchors" reading holds. Architecture E remains falsified under flown-anchored specific power (enceladus-r5 `62f7079`).

## Last touched by

- hyperion R-no-atmospheric-capture-baseline — `1ce7c89` (kill-shot under aerocapture-removed assumption)
- enceladus-r5 R-fleet-ramp-NPV — `253345a` (revenue-conditional finding)
- rhea R-variant-B-recovery-paths-economic — `5fe5dd5`
- enceladus-r5 R-architecture-E — `448505e`
- enceladus-r5 R-arch-E-specific-power-flown-anchored — `62f7079` (Architecture E falsified)
- phoebe R-hybrid-aerocapture-aerobraking — `1623cca` (Earth aerocapture closed-negative; irrelevant to titan-3 closure cell)
- phoebe R-bring-rendezvous-survivability + relaxed + bag-aperture-joint — `abdcd35` / `45869d4` / `8a31ba9` (B-ring rendezvous engineering survivability closed-negative; irrelevant to titan-3 closure cell, which uses Saturn aerocapture + Hohmann-coast + B-ring acquisition with smaller chunk and different risk budget)
- titan-3 R-kilowatt-class-power-envelope — `5162735` + `10b77b7` (0 of 36 cells at 1-30 kilowatt-electric + 200 tonne chunk)
- titan-3 R-delta-velocity-anchor-audit — `42120cf` (two anchors corrected; chemical-electric-leapfrog 13-cells headline retracted at 200 tonne scale)
- titan-3 R-chunk-size-pareto — `1997a51` (closure cell at 40-80 tonne chunk / 30 kilowatt-electric / R12 lunar-gravity-assist — preserved as inbound-only analysis)
- titan-4 R-framework-matrix-parity — `0eb11a7` (framework full-round-trip collapses 200-tonne cell to 0 surviving cells at conservative anchors; titan-3 cells revealed as inbound-only)

## HISTORY

### 2026-05-15 — Initial scaffold from `ARCHITECTURE-DECISION-MATRIX.md` current-decision-state table

Status: open. Confidence: medium.

Current state and open question captured from the matrix's top section as of commit `9704700`. Full audit trail of how this axis arrived at its current state is in the matrix HISTORY section (`water-prop/docs/ARCHITECTURE-DECISION-MATRIX.md`).

---

<!-- Append-only HISTORY entries go below this line. Each entry: ### YYYY-MM-DD — round-name or commit-hash — one-line summary -->

### 2026-05-22 latest+18 — titan-4 R-framework-matrix-parity (`0eb11a7`) — framework full-round-trip collapses 200-t cell to 0 surviving cells; titan-3 cells revealed as inbound-only accounting

Worker encoded the four matrix-carried constraints into `water-prop/sims/mission_graph/` and ran the canonical 750-cell sweep both ways. Constraints-OFF reproduces the pre-encoding baseline exactly (16 cells, 200-t chunk only). Constraints-ON the cell collapses to 0 surviving cells at conservative anchors across 1-55 kilowatt-electric flyable envelope. Two independent killers, each sufficient: powerplant dry-mass floor (a launch-feasible 50-t small vehicle with 10 t dry mass cannot carry 22.8-t reactor at 30 kilowatt-electric / 2.4 watts-per-kilogram; bigger vehicles ≥150 t don't deliver ≥30 t even baseline); reactor lifetime (200-t chunk at 30 kilowatt-electric needs 14-16 yr cumulative burn, over any plausible ceiling). H1 + H2 both fall at every L ∈ {5, 10, 15, ∞} × specific power ∈ {2.4, 5, 10}.

titan-3 reproducibility — scope mismatch, NOT a framework bug. titan-3's 4 strict cells (50-60-t chunk → 35.6-45.4 t delivered) do not reproduce; framework delivers ~half (50-t chunk → 19.4 t) even constraints-OFF. Root cause: titan-3 modeled the inbound leg only (vehicle already at Saturn; chunk as sole propellant; no Earth-launched propellant; no powerplant mass throughout; no reactor-lifetime constraint). Framework models the full round-trip carrying the powerplant the whole way. Framework is the stricter, more-complete model and reproduces titan-3's qualitative cliff, not its cell tonnage. enceladus-r5 (500 kilowatt-electric, RETIRED) reproduces within +16 percent constraints-OFF. Framework brackets cleanly between titan-3 (generous, inbound-only) and enceladus-r5 (pessimistic, shielding-penalised). titan-3's cells preserved as valid inbound-leg analysis.

Status held at open / high. The strict and soft readings of the locked-memory directive both yield no full-round-trip surviving cell at flyable power. Substantive options collapse to matrix decision #15 (b) Saturn-system depot waiver or (c) campaign termination at flyable power softened by decision #16 parametric L0-04-floor sweep.

### 2026-05-15 — R-no-atmospheric-capture-baseline (commit `1ce7c89`) — kill-shot, zero cells in 288-cell sweep without aerocapture

### 2026-05-15 — R-fleet-ramp-NPV (commit `253345a`) — trilemma is revenue-conditional not architecture-intrinsic; R-LEO-water-demand-curve becomes parallel reopener

### 2026-05-18 latest+8 — phoebe rounds 3-6 (merge `b5c5d61`) — sole open structural-reopener falsified

Phoebe R-hybrid-aerocapture-aerobraking (`1623cca`, 0 of 1920 cells) closes the matrix's sole open structural-reopener on the held chunk-rendezvous architecture. Three independent failure modes mutually exclusive across the periapsis axis (pass-1 chunk shatter at Δv ≥ 4.18 km/s, aerobraking unphysical timescale where chunk T_eq < ice melt point, sublimation consumes chunk at tractable altitudes). Companion phoebe rounds (`abdcd35` + `45869d4` + `8a31ba9`) close B-ring rendezvous survivability at all four mitigation levers + bag-aperture × chunk-mass joint relaxation. **The matrix has no remaining open structural-reopener on the held chunk-rendezvous architecture.** Phoebe recommends retire as venture-class with very high confidence; named R-mission-architecture-pivot-survey + R-program-class-reframe-2 as next critical-path rounds (both SCOPE'd this pass). Status bumped open / medium → open / high.

### 2026-05-19 latest+13 — titan-3 R-chunk-size-pareto (`1997a51`) — surviving cell surfaces at 40-80 tonne / 30 kilowatt-electric

Project-owner directive 2026-05-19 retired the 500 kilowatt-electric power class as fantasy-conditioned. titan-3 ran five rounds (merge `3be9ce0`) in response. The first three (R-bus-mass-anchor-adjudication, R-kilowatt-class-power-envelope, R-chemical-electric-leapfrog) found 0 cells closing at 1-30 kilowatt-electric + 200-tonne commercial chunk. The fourth (R-delta-velocity-anchor-audit) vis-viva-corrected two delta-velocity anchors carried unverified across multiple prior rounds, retracting the leapfrog headline at 200-tonne scale. The fifth (R-chunk-size-pareto) found that at **40-80 tonne chunks** the architecture closes: 4 cells L0-05 strict + L0-09 floor at chunk 50-60 tonnes / P=30 kilowatt-electric; 30 cells L0-05 waiver across 50-150 tonnes / 20-30 kilowatt-electric. Architecture is pure-electric throughout with R12 10-flyby lunar-gravity-assist tour at Earth-arrival shedding 5.83 kilometres-per-second of v∞.

Three tensions flagged for project-owner decision (matrix decision points #14-#15): (1) 30 kilowatt-electric is 3× outside titan-3's own 1-10 kilowatt-electric "flyable Kilopower-extrapolation" envelope from R-kilowatt-class-power-envelope earlier the same day, and outside the locked-memory "Kilopower-class single-kilowatt at best" envelope — soft vs strict reading of the directive determines whether the cell is a surviving cell or a fantasy-conditioned headline; (2) closure is pure-electric + lunar-gravity-assist, not hybrid leapfrog (which was retracted at 200-tonne scale); (3) Earth aerocapture is NOT in the closing architecture, but the 10-flyby lunar-gravity-assist tour has its own per-flyby risk budget that has not yet been audited.

Status held at open / high. Resolution depends on project-owner reading of the locked-memory directive (#14) and L0-04 strict (#15).

### 2026-05-18 latest+11 — phoebe pivot-survey + hybrid-chemical (`bb570d7` + `a969aa6`) + iapetus reactor-program-targets (`eab4b13`) — architectural search space exhausted at worker level

Three independent lines of evidence converge to close the architectural-search-space at worker-round level: (a) phoebe R-mission-architecture-pivot-survey (`bb570d7`) — 31 candidates × 8 kill criteria, 31/31 DEAD-ON-ARRIVAL under conservative anchors; 7 F6-conditional WORTH-DEEP-DIVE under iapetus-style probabilistic F6, all gated on the reactor-program-availability question; (b) phoebe R-hybrid-chemical-power-augmentation (`a969aa6`) — fourth orthogonal kill on held chunk-rendezvous, 0/1800 close joint-strict at audit-conditional anchors, hybrid mechanism functionally inert; (c) iapetus R-reactor-specific-power-program-targets (`eab4b13`) — bayesian conjunction of specific-power ≥ 5 W/kg × lifetime ≥ 10 yr × scope ≥ 500 kWe in 2032-2035 window has posterior ≤ 0.13% under uniform prior, ≤ 0.0001% under skeptical.

Plus phoebe R-particle-distribution-q-sensitivity (`75ba925`, 2026-05-16 backfill-handoff) — 0/540 cells across literature q ∈ [2.5, 4.0]. Cumulative phoebe falsification arc on held chunk-rendezvous: 5 rounds × 8,559+ closure-checks, all negative.

Both phoebe-named critical-path rounds (R-mission-architecture-pivot-survey, R-program-class-reframe-2) are now closed — pivot-survey directly, reframe-2 via supersession by iapetus rounds 6-7-8. R-deployable-drag-skirt remains phoebe-named as residual recovery candidate; not yet SCOPE'd.

Restoring any surviving cell requires F6 to resolve favorably (FSP-2 awarded + reactor-program delivers specific-power × lifetime targets) — neither in hand. Axis status held at open; confidence high.
