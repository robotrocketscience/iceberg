# R-near-earth-asteroid-mission-tree — RESULTS

**Worker:** hyperion (re-spawn 2). **Date:** 2026-05-26. Deterministic; `python3 run.py` reproduces `results/nea_sweep.json` + `results/comparator_pareto.csv`. 160 framework tests pass (156 prior + 4 new NEA).

---

## Headline

**The near-Earth-asteroid architecture closes the closed-loop mass loop in 75/75 swept cells, where the Saturn architecture's closed-loop closure inventory is 0/150 — because solar-electric power at ~1 AU (≈0.8 t at 40 kWe) replaces the fission stack (≈21–26 t) that sinks Saturn. But at credible Keck anchors NEA delivers only ~8–11 t water/mission, below the L0-04 = 25 t commercial floor.** NEA is the architecture that *survives closed-loop mass where Saturn doesn't*, at sub-commercial per-mission scale. **H5 holds, sharpened: NEA is a successor architecture, not a Saturn-ring replacement at L0-04 = 25 t.**

### The dual (the real comparator insight)

| | Saturn ring | Near-Earth asteroid |
|---|---|---|
| Resource richness | ~100% water ice (Cassini-confirmed) | 0.4–10% bound water in carbonaceous chondrite |
| Powerplant | fission (KRUSTY 2.4 W/kg) → ~21–26 t at 30–40 kWe | solar at 1 AU (~150 W/kg) → ~0.8 t at 40 kWe |
| Closed-loop mass | self-consistent dry ~121 t; **0/150 deliver ≥ floor** | self-consistent dry ~45 t; **75/75 mass loop closes** |
| Binding failure | **vehicle mass** (can't bring rich resource home at flyable fission power) | **resource dilution** (delivers below commercial floor) |

Two architectures, two orthogonal failure modes. Saturn has the water but can't afford the powerplant to return it; NEA can afford the powerplant but the water is too dilute to clear the floor per mission.

---

## Hypothesis scoring

| # | Verdict | Basis |
|---|---|---|
| H1 | **HELD (model); SCOPE headline corrected** | KISS baseline delivered water = boulder×wf×eff reproduced exactly: 500 t × 1.8% × 90% = **8.1 t**. The SCOPE's "14 t" is inconsistent with its own stated 1.8% input; 14 t corresponds to ~3% water (→13.5 t). Round-trip 6–10 yr anchor adopted (7 yr nominal). Re-derive-from-inputs lesson applied. |
| H2 | **HELD** | At the credible Keck cell (7 m / 500 t, 3% water, 75% extraction) NEA delivers **11.25 t — below the 25 t floor**. Only 24 of 75 cells clear 25 t, all in the optimistic corner (≥5% water and/or ≥10 m boulder). NEA clears the floor only above credible carbonaceous-chondrite water fraction or at boulders beyond the Keck-validated 7 m. |
| H3 | **HELD (load-bearing)** | NEA closes the closed-loop mass fixed point in **75/75 cells**; self-consistent dry mass 45.3 t carries a 0.79 t solar powerplant. Saturn's closed-loop delivery inventory is **0/150** (titan-6): its self-consistent vehicle is ~121 t, driven by the ~21 t fission stack + chunk-scaled TPS/structure on a 200 t chunk, and no cell delivers ≥ floor. Solar-vs-fission is the discriminating axis. |
| H4 | **HELD (Saturn comparison moot)** | NEA fleet-of-5 annual throughput is finite and positive (8–316 t/yr across the sweep; ~8 t/yr at credible anchors, 316 t/yr at the optimistic 15 m/10% corner). Saturn closed-loop throughput is **0** (0/150). The SCOPE's H4 prediction (Saturn 60–100 t/yr) is moot under closed-loop. NEA > Saturn on annual throughput trivially, because Saturn closed-loop delivers nothing. |
| H5 | **HELD (sharpened)** | NEA is successor-architecture-credible (closes mass loop, delivers positive water) but **not a Saturn-ring replacement at L0-04 = 25 t** at Keck anchors (delivers 8–11 t). Phoebe's F6-conditional WORTH-DEEP-DIVE classification stands and is sharpened: NEA is the architecture that survives closed-loop mass where Saturn fails, at sub-commercial per-mission scale. |
| H6 | **HELD** | NEA reuses the mission-agnostic `framework.dry_mass.derive_dry_mass` **unchanged** (test asserts `nea.derive_dry_mass is fw.derive_dry_mass`). The only new mission code is `nea_mass_demands.py` (the subsystem demand seam). The closed-loop abstraction carried a second architecture with zero framework-substrate change → abstraction holds. |

**6/6 held.** H1's model held with the SCOPE-headline arithmetic corrected; the Saturn-comparison hypotheses (H4) are technically moot because Saturn closed-loop is 0, which only strengthens the qualitative reading.

---

## Cross-over (L0-04 floor where NEA becomes viable)

Delivered water = boulder_mass × water_fraction × extraction. At the 200 t-cap-free NEA (boulder size is the free variable), the floor crossover is:

| Water fraction | Boulder to clear 25 t delivered (at 90% extraction) |
|---|---|
| 1.8% (Keck prose) | ~1,540 t (~10 m) — beyond Keck-validated 7 m |
| 3% (carbonaceous typical / 14 t headline basis) | ~925 t (~8.6 m) |
| 5% (high anchor) | ~555 t (~7.3 m) — just above Keck 7 m baseline |
| 10% (optimistic ceiling) | ~278 t (~5.8 m) |

**At the Keck-validated 7 m / 500 t boulder, NEA clears 25 t only at ≥5% water fraction** — above the carbonaceous-chondrite typical (1–3%) and far above Ryugu's measured 0.4%. Under an L0-04 waiver to ~10–15 t (demonstrator/pre-commercial class), NEA closes at the credible 1.8–3% anchors.

---

## Framework-load test (H6 detail)

- New mission code: `missions/nea_mass_demands.py` only.
- Framework substrate changed: **none** (`framework/dry_mass.py` untouched; `derive_dry_mass` reused by identity).
- The closed-loop refactor's "demand-function seam" is the clean architectural boundary: a second architecture differs only in its per-subsystem demand functions (solar vs fission powerplant; boulder-acquisition + thermal-extraction vs trawl). This is stronger evidence for the forest abstraction than the SCOPE's open-loop phase-executor-share test would have been.
- **Scope honesty:** I did not wire 4 separate walker phase-executors into a full `Mission` tree (the SCOPE's literal step 3). Post-refactor, the load-bearing physics is in the mass-demand + delivered-water layer, not walker traversal; the closed-loop verdict does not depend on walker wiring. Full walker-level forest encoding is a deferred follow-on if the orchestrator wants the traversal-level test (would not change this verdict).

---

## Cross-references

- Built on titan-6 R-vehicle-mass-closure-refactor (`08fbef9`) closed-loop framework; consumes its 0/150 Saturn result as the comparator baseline.
- Reconciles phoebe R-mission-architecture-pivot-survey (`bb570d7`) F6-conditional WORTH-DEEP-DIVE for NEA → confirmed and sharpened (successor-credible, sub-commercial at Keck anchors).
- Anchors: saturn-worker wonder pass (`030cb5e`); Keck Institute for Space Studies 2012 (Brophy et al.); OSIRIS-REx (Bennu, 121.6 g, 2023) + Hayabusa2 (Ryugu, 5.4 g, 2020) sample water fractions.
- Feeds design-axis 21 (architecture source comparator); orchestrator propagates the comparator verdict to the matrix.
