# R-mission-architecture-pivot-survey — what alternative mission architectures may restore a surviving cell after held chunk-rendezvous is retired?

**Status:** scope, pre-study. Authored by Saturn (orchestrator), 2026-05-18 latest+8, immediately after the matrix amendment integrating phoebe rounds 3-6 (`b5c5d61`).

**Context.** Phoebe rounds 3-6 close both load-bearing engineering questions on the held chunk-rendezvous architecture (axis 19): hybrid-aerocapture (axis 11, `1623cca`, 0/1920) and B-ring rendezvous survivability (axis 12, `abdcd35` + `45869d4` + `8a31ba9`, 0/162 + 0/126 + 0/2160 under bag-aperture × chunk-mass joint relaxation). Phoebe explicitly recommends retiring the held architecture as venture-class with very high confidence and named this round (R-mission-architecture-pivot-survey) as the next critical-path follow-on. The titan-2 ram-scoop residence-class reframe is already project-owner-retired (latest+6). With both engineering reopeners and the architectural pivot already foreclosed, the matrix has no remaining open structural-reopener on the held architecture.

**This round does not attempt deep physics on any single alternative.** It is a survey: first-pass architecture sketch + Δv accounting + binding-constraint identification + go/no-go-for-deep-round verdict per candidate.

---

## Question this round answers

Given the falsification of the held chunk-rendezvous architecture, **which architectural pivots (if any) deserve deep follow-on rounds**? For each candidate, the round produces a one-page architectural sketch with: (a) first-pass Δv budget, (b) first-pass mass budget, (c) the binding constraint phoebe's findings would predict (chunk-population vs safe-passage, atmospheric-capture ballistic coefficient, B-ring rendezvous geometric impact-prob, residence-velocity Δv penalty), (d) does the binding constraint disappear, soften, or transfer to a new failure mode under the pivot, (e) go-for-deep-round / no-go verdict with one-paragraph justification.

**Architecturally-credible candidates** (phoebe-named in R-bring-rendezvous-survivability verdict §"Next-round candidates" plus matrix axis-19 latest+6 record):

1. **Catcher-at-Saturn.** Chunk delivered to a pre-positioned Saturn-orbit catcher vehicle, then transferred to Earth-return tug. Splits the harvest mission and the return mission into two separate vehicles. Catcher absorbs the B-ring rendezvous risk in slow-cross / residence mode (architecture-fatal risk concentrates into one expendable asset that operates indefinitely on station rather than a return-vehicle that must survive 14 years of cruise after). Return-tug never crosses the B-ring; takes delivery in the F-G gap or in catcher's parking orbit.
2. **Processor-at-Saturn.** Saturn-side electrolysis on a stationed processor vehicle; Earth-bound product is hydrogen + oxygen separately, or compressed water already in customer-loadable form. The titan-2 ram-scoop residence-class architecture's Saturn-side electrolysis was a per-mission cost that contributed to the 14.7 km/s Δv penalty; if processing happens on a permanently-stationed asset, the per-mission Earth-return Δv is paid only on the return leg. This is an architectural cousin to Architecture D (enceladus-r5) but with the processor moved off-moon-surface to orbit and out of falsified Architecture-D bake-off.
3. **Lower-energy-trajectory architecture.** Ballistic-capture + Jovian-or-Titan gravity-assist tour replacing chemical Saturn-orbit-insertion. Cuts SOI Δv from 0.8 km/s (titan-2 R-saturn-soi-periapsis-depth `1b1b889`) to ~0 at the cost of years added to outbound cruise. Phoebe-named candidate but with a known cost: years already at the L0-05 ceiling.
4. **Alternative-source.** Mimas (water-ice moon, 396 km diameter, 0.16 km/s escape, surface-accessible without B-ring transit). Phoebe (200 km diameter, ~0.10 km/s escape, captured-asteroid-class, irregular). Enceladus south-polar plumes (already mapped, water+organics, but planetary-protection category-restricted per L0-16). Trade: source is smaller / different composition; B-ring rendezvous risk is gone; Saturn-side Δv changes; planetary-protection profile changes.

**Out-of-scope for this round (declared up front).** R-deployable-drag-skirt as a chunk-rendezvous rescue, R-bag-armour-multi-layer-deep, R-bring-fine-structure-deep, R-lower-inclination-arrival — all phoebe-named "if rejected by project owner" candidates. Those are within-chunk-rendezvous rescues; the survey assumes the architecture is retired and tests pivots. If the project owner rejects the retire-decision, the survey is moot.

---

## Pre-registered hypotheses (numeric ranges + falsification bands)

| # | Hypothesis | Predicted range | Falsification band |
|---|---|---|---|
| H1 | **Catcher-at-Saturn.** The split-vehicle architecture survives the B-ring impact-prob constraint because the catcher operates in residence-class velocity (slow-cross of B-ring at v_rel ≤ 1 km/s; per-impact KE drops to ≤ 1 kJ per phoebe R-bring-rendezvous-survivability table); the return-tug picks up product in F-G gap and never crosses B-ring. Trade: two vehicles per mission, ~2× per-mission capital cost. Per-mission Earth-return Δv is ≤ 1.5× single-vehicle baseline because the return-tug carries no inbound-cruise propellant for the harvest leg. | catcher closes B-ring constraint (per-pass impact-prob ≤ 0.01% on return-tug); per-mission capital cost ratio 1.5-2.5× single-vehicle | H1 falsified if (a) catcher cannot achieve slow-cross residence at v_rel ≤ 5 km/s within Saturn-side Δv budget ≤ 8 km/s, OR (b) per-mission capital cost ratio > 3× single-vehicle |
| H2 | **Processor-at-Saturn.** Per-mission Earth-return mass under processed-product (H₂ + O₂ separately, or compressed water in customer-load form) is ≤ 80% of raw-chunk delivered mass because of the propellant cost to deliver process power and Saturn-side electrolysis throughput. Net delivered to LEO is positive only if processing power infrastructure is amortised across ≥ 8 missions; below that, the processor's own delivery + power-system mass exceeds the per-mission product mass uplift. | processed-product delivered fraction 50-80% of raw-chunk; break-even amortisation 5-12 missions | H2 falsified if (a) processed-product delivered fraction < 30% (processor architecture is mass-inverse), OR (b) break-even amortisation > 20 missions (no plausible program scale supports it) |
| H3 | **Lower-energy-trajectory.** Ballistic-capture + Titan flyby tour reduces SOI Δv from 0.8 km/s to ≤ 0.1 km/s but costs 4-8 years added to outbound cruise. L0-05 15-yr round-trip target is unreachable; ≥ 25-yr waiver becomes necessary (same as Architecture E latest+5 condition, now-falsified). Round-trip in 14-22 yr range. | added outbound 4-8 yr; round-trip 18-22 yr | H3 falsified if (a) added outbound ≤ 2 yr (lower-energy is cheap and the round becomes meaningful for L0-05 strict), OR (b) added outbound > 12 yr (architecture is dead on round-trip alone) |
| H4 | **Alternative-source: Mimas surface harvest.** Mimas-surface ice harvest at sub-km equatorial sites avoids B-ring transit entirely. Saturn-side Δv from Mimas-orbit to Earth-return ≤ 2 km/s (Mimas escape 0.16 km/s + Saturn-escape-from-Mimas-orbit ~5 km/s minus Titan-gravity-assist benefit). Per-mission delivered chunk-equivalent is ≤ 50 t at the 500 kWe / Variant-B power floor because surface-harvest throughput is lower than chunk capture. Per-mission delivered ≤ 25% of B-ring chunk-rendezvous, but P(closure) jumps from 0% to a meaningful number. | Mimas per-mission delivered 25-50 t; closure-probability rises to 20-50% under R-power-base-rate priors | H4 falsified if (a) Mimas per-mission delivered < 10 t (architecture is too small to clear L0-04), OR (b) Saturn-side Δv > 6 km/s (architecture pays the residence-class Δv penalty after all) |
| H5 | **Alternative-source: Phoebe surface harvest.** Phoebe is captured-asteroid-class, irregular, retrograde orbit at 12.9 million km from Saturn (Saturn-escape from Phoebe orbit is cheap, 0.6 km/s). Per-mission delivered constrained by Phoebe's water-ice fraction (Cassini VIMS confirmed water-ice surface but mixed with carbonaceous material; ~50-70% water-ice mass fraction). Per-mission delivered 100-150 t at 500 kWe (higher than Mimas because Saturn-orbit-escape is cheaper). Trade: Phoebe is far from Saturn, so the inbound-from-Phoebe-orbit segment takes ~3 yr longer than B-ring orbit cycle. | Phoebe per-mission delivered 100-150 t; cycle 3-4 yr longer than B-ring | H5 falsified if (a) water-ice mass fraction < 30% (per-mission delivered drops below 50 t), OR (b) cycle extension > 8 yr (round-trip exceeds L0-05 strict + L0-06 first-delivery) |
| H6 | **Aggregate verdict.** Across the four candidates, at least one (probably catcher-at-Saturn or alternative-source Mimas) survives the pre-screen as a go-for-deep-round candidate. Probability ≥ 70% that the survey produces ≥ 1 deep-round-deserving candidate; probability ≥ 30% that it produces ≥ 2. If the survey produces 0 candidates, the program-class is forced to technology-demonstrator only (matrix decision point #1, technology-demonstrator option). | ≥ 1 deep-round candidate with probability ≥ 70% | H6 falsified if survey produces 0 deep-round candidates (program-class is forced) OR ≥ 3 candidates (survey under-screened, candidates need re-pruning) |

---

## Method sketch (worker drafts the actual code in `run.py`)

1. **For each candidate**, write a one-page architectural sketch in `results/sketches/<candidate>.md`. Sections: (a) concept-of-operations one-paragraph, (b) Δv budget table (outbound, SOI, Saturn-side, Earth-return), (c) mass budget table (vehicle dry + propellant + payload at one or two cardinal cells), (d) binding-constraint identification under phoebe's framework (atmospheric-capture / B-ring rendezvous / residence-Δv / chunk-population co-location / planetary-protection), (e) does the constraint disappear, soften, or transfer, (f) deep-round dependencies (what would the deep round have to test?).

2. **Δv accounting** uses the same continuous-thrust electric framework as titan R-inbound-dv-continuous-thrust. Reference cell: 500 kWe reactor (Variant B optimum), Isp 5000 s, MET specific impulse from `vehicle/` specs. Where chemical kick stages appear, use hyperion R-outbound-chemical-kick-economics anchors (145-174 t hydrolox per outbound mission).

3. **Mass accounting** uses bundled formula at megawatt scale (locked aelfrice finding 4: 40-55% radiator + reactor/shield 25-35% + power-conversion 15-25%). Where Architecture D / Variant B parallels apply, cross-reference rhea R-megawatt-marvl-radiator + R-architecture-D-L1007-relaxation.

4. **Constraint propagation** is rule-based: for each candidate, check the explicit phoebe failure modes and report which are foreclosed by the pivot's geometry vs which transfer to new failure modes. Example: catcher-at-Saturn eliminates the return-tug's B-ring crossings (axis 12 closed for return-tug) but the catcher itself is a residence-class asset that has the same failure mode for the harvest leg — does it close at residence Δv ≤ 8 km/s applied once-at-station-establishment instead of per-mission? That's a quantitative question the sketch must answer.

5. **Go-for-deep-round verdict** is a 4-cell table per candidate: (a) does the pivot foreclose phoebe's binding constraint? (b) does it transfer the constraint to something even worse? (c) does it satisfy L0-04 / L0-05 / L0-06 at one or more cardinal cells? (d) what's the binding open question a deep round would need to adjudicate? Verdict is one of: GO (worth a deep round, axis-by-axis sketch closes); CONDITIONAL (worth a deep round if a specific upstream resolves, e.g. planetary-protection waiver for Enceladus); NO-GO (sketch surfaces a fatal binding constraint that the deep round would only re-confirm).

6. **Aggregate verdict on H6** is the count of GO + CONDITIONAL candidates. Report the decision-frame implication for matrix decision point #1 (program-class).

---

## Out-of-scope for this round (declared)

- **Deep economics.** Per-mission and program-NPV deep-dive belongs in the candidate-specific deep round, not the survey. Sketch-level "approximate cost ratio to Variant B" is sufficient.
- **Detailed launch-vehicle sizing.** Per-candidate outbound launch mass should reference titan-2 R-launch-cost-sensitivity but does not need re-derivation at SLS pricing (decision point #4 still open).
- **R-deployable-drag-skirt, R-bag-armour-multi-layer-deep, etc.** All within-chunk-rendezvous rescues. These are R-program-class-reframe-2's territory under the "reject one or both phoebe verdicts" option.
- **Crew-rated variants.** REQUIREMENTS.md §8 explicit out-of-scope at L0.

---

## Methodology lesson dependencies

- **Lesson 1** (pessimistic-prediction default). Apply to each candidate's H — anchor on the engineer-pessimistic-insufficient pattern phoebe corroborated 13/13 times.
- **Lesson 7** (compute under most pessimistic credible anchor first). For Δv and mass, use bundled MARVL formula + MIRA-locked specific power floor (locked aelfrice findings 1+4).
- **Lesson 9** (anchor-from-PRIMARY-text). Each candidate's architectural sketch must cite the PRIMARY round it draws from (titan / hyperion / rhea / enceladus-r5 / phoebe), not downstream summaries.
- **Candidate lesson 11** (self-questioning rounds as campaign-default). After the survey, if any candidate passes the GO bar, the deep-round SCOPE should be authored with a built-in self-question on the binding constraint.

---

## Worker assignment

This SCOPE is a survey round — broad and rule-based. Either a fresh worker (e.g. dione, tethys, mimas) or any existing worker on resume. Phoebe is the most-natural candidate given session-continuity with the rounds that surfaced this work, but project-owner direction supersedes.

Expected effort: 2-3 sketches in detail + 1-2 in summary; ~one full session; produces `STUDY.md` pre-registration, `run.py` constraint-propagation logic, `results/sketches/<candidate>.md` per candidate, `results/closure_verdict.md` aggregate.

---

## Matrix axes touched

- Axis 02 (Surviving cell) — directly. If any candidate is GO, axis 02 reopens with the candidate as new surviving-cell-conditional.
- Axis 12 (Saturn-side capture mode) — alternative-source candidates moot the B-ring rendezvous question.
- Axis 13 (Outbound launch architecture) — catcher-at-Saturn likely doubles per-mission outbound mass.
- Axis 14 (Cruise trajectory) — lower-energy-trajectory candidate directly touches.
- Axis 19 (Capture architecture) — if any candidate is GO, axis 19's "held chunk-rendezvous" framing must be amended or retired.
- Axis 16 (Concept-of-operations document) — titan-2 conops rebuild target shifts from chunk-rendezvous to whichever candidate(s) survive.
