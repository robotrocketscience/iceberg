---
axis: "Chunk-mass cap (L1-007)"
status: open
confidence: high
last_revised: 2026-05-22
related:
  - "[[program-class]]"
  - "[[saturn-side-capture-mode]]"
  - "[[surviving-cell]]"
  - "[[reactor-power-floor]]"
  - "[[round-trip-ceiling]]"
---

# Chunk-mass cap (L1-007)

## Current

**2026-05-21 (Saturn worker, mission-graph framework canonical sweep):** the chunk-mass cap question is now framed by the mission-graph framework rather than by titan-3 anchors. Per the assumption audit at L0-04 = 25 t provisional floor, **only chunk_mass_kg = 200,000 closes** in the canonical sweep — at chunks of 100 t or smaller, after ~80 percent rocket-equation losses during chunk-fed-spiral departure, the delivered mass at LEO does not reach the L0-04 floor. The 200-tonne chunk anchor is **REINSTATED as the closure-target chunk mass** under the corrected mission_graph model that uses 80 percent propellant fraction + properly accounted kick-stage mass + chunk-fed-spiral-return architecture. Best architecture at L0-04 = 25 t delivers 39.5 tonnes from a 200-tonne chunk over 11.93 yr round-trip.

**2026-05-19 latest+13 INVERSION (titan-3 R-chunk-size-pareto `1997a51`) PRESERVED BUT SUPERSEDED:** the titan-3 result that closing chunk-mass band is 40-80 tonnes assumed an architecture that differed from the current mission_graph model. Specifically: titan-3 used hybrid chemical-electric leapfrog + R12 lunar-gravity-assist inbound + 30 kilowatt-electric Kilopower-extrapolation; the mission_graph framework uses chunk-fed-spiral departure + direct propulsive or hybrid aerocapture inbound + variable power. The two frameworks make different predictions because they model different architectures. **Open: which architecture is the right operational baseline?** Mission_graph's chunk-fed-spiral closure is anchored on water-electrothermal specific impulse (A1 audit = plausible-provisional); titan-3's chemical-electric leapfrog is anchored on the corrected vis-viva delta-velocity anchors (`42120cf`). Per the project-owner directive "a 500 kilowatt reactor is not going to happen", the operational baseline must close at flyable power; both frameworks now claim to do so but with different chunk-mass bands.

**2026-05-21 latest+15 framework-parity flag:** the 200-tonne-mission_graph versus 40-80-tonne-titan-3 split is a **framework-parity item**. The mission_graph framework does not yet encode three of the constraints the titan-3 result was bound by: reactor lifetime versus cumulative full-power burn time (axis 20), Modular Assembled Radiators for Very Large systems bundled radiator-mass formula (locked belief `0418e2c9`), and the corrected vis-viva delta-velocity anchors at Saturn-departure 7.7 kilometres-per-second + Earth-arrival 4.2 kilometres-per-second post-R12 lunar-gravity-assist (latest+13). When the framework gains those constraints, expect mission_graph's closing chunk-mass to shift down toward the titan-3 band.

**2026-05-22 latest+18 — FRAMEWORK-PARITY RESOLVED (titan-4 R-framework-matrix-parity `0eb11a7`):** worker encoded all four matrix-carried constraints (reactor lifetime versus cumulative burn; Modular Assembled Radiators for Very Large systems bundled radiator mass; conservative 2000-kilogram bus floor; vis-viva LEO capture burn) into `water-prop/sims/mission_graph/`. The result: under full-round-trip accounting, **both the titan-3 40-80 tonne band and the mission_graph 200-tonne single-cell collapse**. Constraints-ON, 0 surviving cells at conservative anchors across the 1-55 kilowatt-electric flyable envelope. titan-3 reproducibility — scope mismatch, NOT a framework bug: titan-3's 4 strict cells (50-60-tonne chunk → 35.6-45.4 t delivered) do not reproduce. Framework delivers ~half (50-tonne chunk → 19.4 t) even constraints-OFF at Isp 2000 s. **Root cause: titan-3 modeled the inbound leg only** (vehicle already at Saturn; chunk as sole propellant; no Earth-launched propellant; no powerplant mass throughout; no reactor-lifetime constraint). Framework models the full round-trip carrying the powerplant the whole way. titan-3's cells preserved as valid inbound-leg analysis. The mission_graph 200-tonne closure cell from the assumption-audit canonical sweep was also constraints-OFF and is similarly reframed: it survives the framework's pre-encoding baseline (16 cells, 200-tonne chunk only) but collapses under full constraints. **M-3 (75-percent chunk-tow delivery) retired as a delivery anchor** per the same round — it is inbound-leg chunk retention (60-t chunk → 45.4 t delivered = 75.7 percent, ~25 percent burned as propellant on the way home at Isp 2000 s), not end-to-end delivery. Full-round-trip delivery ratio is ~20 percent of nominal chunk constraints-OFF and 0 percent under conservative constraints.

## Open question

L1-007 should be re-derived around the 40-80 tonne closure band, not the 200-tonne legacy anchor. Relaxation UPWARD (prior framing) no longer applies under the 500 kilowatt-electric retirement — relaxation DOWNWARD to 40-80 tonnes is the right move. Open follow-ons: (1) re-run rhea R-heterogeneous-cadence and R-delivery-irr-curve under 40-80 tonne chunks to refresh hurdle crossovers (the rhea verdict "chunk-shrinking loses NPV in every regime tested" was at constant 200-tonne baseline with chunk shrinking OVER TIME, not at a 40-80 tonne homogeneous program — orthogonal test); (2) does R12 14-tonne demonstrator chunk fit anywhere in the 40-80 tonne closure band, or is the demonstrator out-of-envelope?

## Last touched by

- titan R-inbound-dv-continuous-thrust — `58581fb`
- titan-2 R-multi-chunk-per-mission — `c4c7ca7`
- titan-2 R-HE-graze-feasibility — `b2e7a35`
- worktree-110450 R-delivery-irr-curve — `6068140` [hurdle crossovers now moot]
- phoebe R-variant-B-100t-resizing — `b5d37a9` [data preserved; propellant-infeasibility at 500 kilowatt-electric now moot]
- rhea R-architecture-D-L1007-relaxation — `cca831c` [now moot]
- titan-3 R-chunk-size-pareto — `1997a51`
- Saturn worker R_assumption_audit_2026_05_21 + canonical mission_graph sweep `20260521T193329Z`
- titan-4 R-framework-matrix-parity — `0eb11a7` (framework full-round-trip collapses both titan-3 40-80-t band and mission_graph 200-t cell; titan-3 cells revealed as inbound-only; 75-percent M-3 anchor retired)

## HISTORY

### 2026-05-21 — Saturn worker canonical mission_graph sweep at L0-04 = 25 t — 200-tonne chunk REINSTATED as closure-target

Mission_graph framework canonical sweep (vehicle mass × power × chunk mass × electric thrust, 625 cells) at the L0-04 provisional floor of 25 tonnes (REQUIREMENTS.md v0.13) shows only chunk_mass_kg = 200,000 closes. Smaller chunks (5/10/25/50/100 t) deliver below the 25-tonne floor after ~80 percent rocket-equation losses during chunk-fed-spiral departure. Best architecture: 39.5 t delivered from a 200-tonne chunk in 11.93 yr round-trip. Closing axis values: chunk = 200 t; vehicle 50/63/100 t; power 30-1000 kWe; electric thrust 5/10/25 N. Architecturally distinct from titan-3 R-chunk-size-pareto: mission_graph uses chunk-fed-spiral departure (water-electrothermal at 800 s) + direct propulsive or hybrid aerocapture inbound; titan-3 used chemical-electric leapfrog + R12 lunar gravity assist. **Both frameworks claim closure at flyable power; the operational-baseline question is which architecture to develop**. See `water-prop/rounds/R_assumption_audit_2026_05_21/BEST_ARCHITECTURES_25T.md`.

### 2026-05-15 — Initial scaffold from `ARCHITECTURE-DECISION-MATRIX.md` current-decision-state table

Status: open. Confidence: high.

Current state and open question captured from the matrix's top section as of commit `9704700`. Full audit trail of how this axis arrived at its current state is in the matrix HISTORY section (`water-prop/docs/ARCHITECTURE-DECISION-MATRIX.md`).

---

<!-- Append-only HISTORY entries go below this line. Each entry: ### YYYY-MM-DD — round-name or commit-hash — one-line summary -->

### 2026-05-22 latest+18 — titan-4 R-framework-matrix-parity (`0eb11a7`) — framework full-round-trip collapses both chunk-mass cells; titan-3 cells revealed as inbound-only; M-3 75-percent anchor retired

Worker encoded all four matrix-carried constraints into `water-prop/sims/mission_graph/`. Under constraints-ON full-round-trip accounting, neither the titan-3 40-80-tonne band nor the mission_graph 200-tonne cell survives at conservative anchors across the 1-55 kilowatt-electric flyable envelope. titan-3's 4 strict cells (50-60-t chunk → 35.6-45.4 t) do not reproduce; framework delivers ~half (50-t chunk → 19.4 t) even constraints-OFF at Isp 2000. Root cause is scope mismatch (titan-3 inbound-leg-only versus framework full-round-trip), NOT a framework bug. titan-3's cells preserved as valid inbound-leg analysis.

M-3 (75-percent chunk-tow delivery) retired as a delivery anchor per the same round. The 75-percent figure is inbound-leg chunk retention from titan-3's model (60-t chunk → 45.4 t delivered, ~25 percent burned as propellant on the way home at Isp 2000 s), not end-to-end delivery. Framework full-round-trip delivery ratio is ~20 percent of nominal chunk constraints-OFF and 0 percent under conservative constraints. R-pitch-arithmetic-audit can now anchor on framework-derived numbers.

Status held at open / high. The 40-80-tonne L1-007 re-derivation question (latest+13) is moot under the framework verdict — no chunk-mass band closes at flyable power under full-round-trip accounting. Substantive options collapse to matrix decision #15 (b) Saturn-system depot waiver (drops the round-trip requirement; needs R-saturn-system-water-depot-demand) or (c) campaign termination at flyable power softened by decision #16 parametric L0-04-floor sweep.

### 2026-05-21 latest+15 — Saturn worker / orchestrator framework-parity flag — mission_graph 200-tonne vs titan-3 40-80-tonne split assigned to R-framework-matrix-parity

The framework-versus-matrix divergence on closing chunk-mass band is the load-bearing reading for `R-framework-matrix-parity` (open round, punch-list item M-4 / S-1; not yet SCOPE'd as directory). Saturn-worker shipped the mission_graph framework (`d8dd956`) and ran the canonical sweep (`20260521T193329Z`) that surfaces 200-tonne closure under chunk-fed-spiral departure. titan-3 R-chunk-size-pareto's 40-80-tonne closure band stands at hybrid chemical-electric leapfrog + R12 lunar-gravity-assist + corrected vis-viva anchors. Three constraints not-yet-encoded in mission_graph: reactor lifetime versus cumulative full-power burn (axis 20), MARVL bundled radiator-mass formula (locked belief `0418e2c9`), and the corrected vis-viva anchors. When those land in the framework, expect mission_graph's closing chunk-mass to shift down toward the titan-3 band. Status held at open / high; the addition is framework-parity context, not a new decision.

### 2026-05-19 latest+13 — titan-3 R-chunk-size-pareto (`1997a51`) — 200-tonne anchor retired as overscale; 40-80 tonne closure band surfaces

Under the project-owner 2026-05-19 directive retiring 500 kilowatt-electric and titan-3's vis-viva-corrected delta-velocity anchors, the chunk-mass cap inverts. titan-3 R-chunk-size-pareto swept chunk_t ∈ {10, 20, 30, 40, 50, 60, 80, 100, 120, 150, 200} × P_reactor_kw ∈ {10, 15, 20, 30} × specific_power ∈ {2.4, 10.0} (88 cells) at corrected anchors (Saturn-departure 7.7 kilometres-per-second; Earth-arrival residual 4.47 kilometres-per-second after R12 10-flyby lunar-gravity-assist tour). 4 cells close L0-05 strict + L0-09 floor at chunk 50-60 tonnes / P=30 kilowatt-electric; 30 cells close at L0-05 waiver across 50-150 tonnes / 20-30 kilowatt-electric. Delivered 30-60 tonnes per mission, round-trip 14-22 years.

The 200-tonne commercial-chunk anchor that propagated through matrix, pitch deck, REQUIREMENTS, and rhea financial rounds is now overscale at flyable power. L1-007 should be re-derived around the 40-80 tonne closure band. Open follow-on: refresh rhea hurdle crossovers (sovereign-bond at 209 t / regulated-utility 461 t / corporate-growth 691 t) under the new chunk scale — at 50-60 tonne strict band, none of those hurdles cross.

Status held at open / high. Resolution depends on project-owner reading of decision points #14 (reactor power class for closure cell) and #15 (L0-04 strict).
