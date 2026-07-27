# R-near-earth-asteroid-mission-tree — READING (5-section template)

**Worker:** hyperion (re-spawn 2) · **Date:** 2026-05-26

## Hypotheses adjudicated

H1 **held** (model = inputs; SCOPE's 14 t headline corrected to 8.1 t at its own 1.8% input) · H2 **held** (credible Keck cell delivers 11.25 t, below 25 t floor) · **H3 held (load-bearing)** (NEA closes the closed-loop mass loop 75/75 on solar power; Saturn 0/150 on fission) · H4 **held** (NEA throughput finite/positive; Saturn closed-loop 0 — comparison moot) · H5 **held, sharpened** (successor-credible, not Saturn-replacement at 25 t) · H6 **held** (framework abstraction carried a second architecture with zero substrate change).

Predicted-vs-measured: my STUDY prior — "near-certain NEA closes the mass loop (solar beats fission), real question is whether it clears the commercial floor (prior: no)" — held on both counts. The one quantitative correction was forced by the SCOPE's own arithmetic (H1: 14 t → 8.1 t).

## Headline

**Near-Earth-asteroid is the successor architecture that survives the closed-loop mass reality Saturn does not — but at sub-commercial per-mission scale.** The discriminating axis is the powerplant: at ~1 AU, solar-electric power (~0.8 t at 40 kWe) is ~25–30× lighter than the KRUSTY fission stack (~21–26 t) that drove Saturn's self-consistent vehicle to ~121 t and its delivery inventory to 0/150. NEA's vehicle closes at ~45 t and delivers positive water. But carbonaceous-chondrite water is dilute (1–3% typical, 0.4% at Ryugu), so the Keck-validated 7 m / 500 t boulder yields only ~8–13 t water/mission — below the L0-04 = 25 t commercial floor. NEA clears 25 t only at ≥5% water fraction or boulders beyond the Keck-validated envelope.

## Reading (for the project owner)

1. **File NEA as the on-shelf successor architecture, conditional, at demonstrator/pre-commercial scale.** It is the one alternative in phoebe's pivot survey that survives the closed-loop mass test that just killed Saturn at flyable power (titan-6, 0/150). That is a genuine, decision-relevant property: if decisions #14/#15 resolve toward terminating the Saturn-ring program at flyable fission power, NEA is a real successor that does not start from a non-physical vehicle. But it is **not** a drop-in Saturn replacement at L0-04 = 25 t — it delivers ~8–13 t/mission at credible anchors.

2. **The two architectures fail in orthogonal ways — and that is the useful comparator output for axis 21.** Saturn: rich resource (~100% ice), fatal vehicle mass (fission too heavy to bring it home at flyable power). NEA: feasible vehicle mass (solar at 1 AU), dilute resource (1–3% bound water). Neither closes commercial-class at flyable power and credible anchors — but for *different* reasons, which means they are not redundant bets: a power-technology breakthrough (light flight reactor) rescues Saturn; a richer-target or higher-extraction result rescues NEA. They de-risk different futures.

3. **If NEA is pursued, the load-bearing parameter is target water fraction, not vehicle engineering.** The vehicle closes the mass loop comfortably on flown-class solar. What gates commercial-class delivery is whether a ≥5% water-fraction C-type boulder in the 5–9 km/s band exists and is characterised. That is a target-survey + spectroscopy question (and an in-situ-confirmation risk: Ryugu's measured 0.4% is a cautionary anchor — remote spectroscopy may overstate extractable water). Recommend any NEA follow-on lead with a target-water-fraction survey, not vehicle design.

## Cross-learning

- **Confirms + sharpens phoebe R-mission-architecture-pivot-survey (`bb570d7`):** NEA's F6-conditional WORTH-DEEP-DIVE is upheld with a quantitative basis — it survives closed-loop mass, fails the commercial floor on resource dilution. The "deep dive" that matters is target water fraction, not architecture.
- **Builds on + extends titan-6 R-vehicle-mass-closure-refactor (`08fbef9`):** the closed-loop framework's value is now demonstrated across two architectures. The demand-function seam (`*_mass_demands.py`) is the clean boundary; the forest abstraction holds (H6). This is the second tree the framework was designed to carry, and it landed with zero substrate change.
- **For design-axis 21 (architecture source comparator):** the comparator verdict is a *dual failure-mode* table (vehicle-mass-bound Saturn vs resource-dilution-bound NEA), not a single Pareto winner. Recommend the matrix record both as non-redundant conditional bets, with NEA as the flyable-power successor and Saturn as the breakthrough-reactor bet.
- **Methodology note (re-derive-from-inputs, PROTOCOL lesson 20):** the SCOPE's H1 carried a 14 t headline inconsistent with its own 1.8%/90%/500 t inputs (which give 8.1 t). Encoding `delivered = boulder × wf × eff` from inputs surfaced the slip immediately and showed 14 t silently assumed ~3% water. Third campaign application of re-derive-from-inputs.

## Revisit

Prediction held cleanly; the only correction was the SCOPE-headline arithmetic. One thing I framed more sharply than the STUDY anticipated: the comparator is not "which architecture wins" but "which failure mode you are betting against." Saturn and NEA are not competing answers to the same question — they are hedges against different breakthroughs (light reactor vs rich/extractable target). That reframing is the round's most useful output for the matrix, beyond the per-mission tonnage numbers.

## Deferred follow-on (if the orchestrator wants it)

- **Walker-level forest encoding:** wire the 4 NEA phase-executors (rendezvous / boulder-acquisition / thermal-extraction / NEA-departure) into a full `Mission` tree mimicking `saturn_water_v1`, for the traversal-level >70%-shared-executor test. Would not change this verdict (delivered mass + mass-loop closure are computed in the demand + delivered-water layer), but completes the SCOPE's literal step 3.
- **NEA target-water-fraction survey:** the actual gate on commercial-class NEA. Spectroscopy + in-situ-confirmation risk; Ryugu 0.4% measured vs remote-estimate cautionary anchor.
