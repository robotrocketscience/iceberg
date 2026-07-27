# R-near-earth-asteroid-mission-tree — STUDY (pre-registration; reframed for the closed-loop framework)

**Worker:** hyperion (re-spawn 2). **Date:** 2026-05-26. **Status:** pre-registration frozen; encoding + sweep pending.
**Round type:** framework engineering (encode a near-Earth-asteroid architecture on the closed-loop mass machinery) + comparator analysis (NEA vs Saturn closed-loop).

---

## The reframe the SCOPE could not have (read first)

The SCOPE was authored 2026-05-22 latest+16, when the framework had ONE tree (`saturn_water_v0`, open-loop: vehicle dry mass is a swept boundary condition). It instructs me to mimic `saturn_water_v0` and Pareto against it.

Since then, **titan-6's R-vehicle-mass-closure-refactor landed** (merge `08fbef9`): vehicle dry mass is now a *derived* fixed point of per-subsystem mass demands (`framework/dry_mass.py` + `missions/saturn_mass_demands.py` + `missions/saturn_water_v1.py`). The headline result: **the Saturn closed-loop closure inventory is 0/150** (vs 16/150 open-loop), because "every open-loop closer was a vehicle lighter than its own powerplant" — a 40-kWe KRUSTY powerplant is ~26 t (reactor 16.7 t at 2.4 W/kg + MARVL radiator 9 t + thrusters), and the open-loop closers were lighter than that.

**Encoding NEA against the open-loop `saturn_water_v0` would reproduce exactly the non-physical closures titan-6 just discredited.** So this round encodes NEA on the **closed-loop** machinery (`derive_dry_mass` + a new `nea_mass_demands.py`), and the comparator is NEA-closed-loop vs Saturn-closed-loop (0/150). This is the honest framing; I record the deviation here and in READING.

### The load-bearing physics, stated up front (so the hypotheses are honest)

Saturn dies closed-loop on the **powerplant mass-floor**: fission at KRUSTY 2.4 W/kg. NEA's Keck reference architecture uses **40-kWe solar-electric propulsion at ~1 AU**, where flight solar arrays run ~100–200 W/kg (Roll-Out Solar Array class). A 40-kWe solar powerplant masses **~0.7–1 t** vs Saturn's ~26 t — **~25–35× lighter**. So I expect NEA to *close the mass loop* precisely where Saturn cannot. The open question this round answers is not "does NEA close the mass loop" (I'm near-certain it does) but **"does it deliver enough water per mission to clear the L0-04 = 25 t commercial floor at credible boulder/water-fraction anchors?"** — and my prior, per the Keck baseline, is no (it delivers below the floor; it's a sub-commercial successor architecture, not a Saturn replacement at the same L0).

### Pre-registration arithmetic note (re-derive-from-inputs, PROTOCOL lesson)

The SCOPE's H1 states "14 ± 4 t delivered at 1.8% water, 90% extraction, 500 t boulder." But 500 t × 1.8% × 90% = **8.1 t**, not 14 t. The 14 t figure corresponds to ~3% water (500 × 0.03 × 0.9 = 13.5 t). I encode the delivered-water model from its inputs (`delivered = boulder × water_fraction × extraction_eff`) and grade H1 against what the inputs actually give, reporting delivered water as a function of water fraction rather than a single mis-stated point.

---

## The question this round answers

Under closed-loop, self-consistent vehicle mass: (1) does the NEA architecture close the mass loop where Saturn (0/150) does not? (2) what water mass does it deliver per mission at credible anchors, and does it clear the L0-04 = 25 t floor? (3) does the framework's "forest of mission graphs" abstraction hold — i.e. does NEA reuse the framework-level closed-loop machinery with only mission-specific mass-demand functions changing?

## Locked anchors respected (saturn-worker wonder pass `030cb5e`; not litigated)

- Main belt out of scope; NEA only. Canonical target **2008 EV5 at 6.29 km/s rendezvous**.
- NEA water content **1–10% by mass** in carbonaceous-chondrite phyllosilicates (Bennu/OSIRIS-REx, Ryugu/Hayabusa2); bound, thermal extraction 400–700 °C.
- **Keck Institute for Space Studies 2012**: 28:1 boulder-to-launched-vehicle mass amplification; 7 m / ~500 t boulder; 40-kWe-class solar-electric propulsion; 6–10 yr round-trip.
- Lunar polar ISRU is the most-cited competitor (axis 21) but is a *separate* tree, not this round.

## Pre-registered hypotheses (frozen; reframed to closed-loop where the SCOPE assumed open-loop)

| # | Hypothesis | Predicted | Falsification band |
|---|---|---|---|
| H1 | The Keck baseline (7 m / 500 t boulder, 1.8% water, 90% extraction) reproduced in the closed-loop model delivers **~8 t water/mission** (= 500×0.018×0.9), NOT the SCOPE's mis-stated 14 t; round-trip 6–10 yr. Delivered water scales linearly with water fraction: ~8 t at 1.8%, ~13.5 t at 3%, ~22.5 t at 5%. | delivered water = boulder×wf×eff, reproduced within rounding; 6–11 yr round-trip | H1 (model) falsified if the encoded model departs from boulder×wf×eff by >5% (a coding error). |
| H2 | At L0-04 = 25 t, the NEA baseline does NOT close on delivered mass (delivers ~8 t at 1.8%). It clears 25 t only at high water fraction (≥5%) AND large boulder, or under an L0-04 waiver to ~10–15 t. | NEA below 25 t floor at Keck-anchor water fraction; clears at ~15 t waiver | H2 falsified if a Keck-envelope NEA cell delivers ≥ 25 t at ≤3% water fraction. |
| H3 | NEA closes the **closed-loop mass fixed point** at credible anchors (solar powerplant ~0.7–1 t at 40 kWe / 150 W/kg), where Saturn's closed-loop inventory is 0/150. The NEA vehicle is NOT lighter than its own powerplant. | NEA mass derivation converges and dry mass ≫ powerplant mass; NEA closes mass loop where Saturn does not | H3 falsified if NEA's closed-loop dry mass fails to converge or the vehicle cannot contain its solar powerplant. |
| H4 | At a fleet of 5, NEA annual throughput (faster ~7 yr round-trip, smaller ~8–14 t/mission) does NOT exceed the Saturn titan-3 closing band — and that comparison is now moot because Saturn's closed-loop band is **empty (0/150)**. So NEA's annual throughput, while modest, is **strictly greater than Saturn's closed-loop zero**. | NEA fleet=5 annual throughput finite and positive; Saturn closed-loop = 0 | H4 falsified if NEA annual throughput is also zero (mass loop fails). |
| H5 | NEA is **successor-architecture-credible** (closes the mass loop, delivers sub-commercial water) but **not a Saturn-ring replacement at L0-04 = 25 t** at Keck anchors. Phoebe's F6-conditional WORTH-DEEP-DIVE classification stands, sharpened: NEA is the architecture that *survives closed-loop mass* where Saturn doesn't, but at sub-commercial per-mission scale. | NEA successor-credible; sub-25 t at Keck anchors | H5 falsified if NEA dominates Saturn on delivered mass AND clears 25 t at credible anchors (would make it a replacement, not a successor). |
| **H6 (load-bearing)** | The framework's closed-loop abstraction **holds across architectures**: NEA reuses the framework-level `derive_dry_mass` fixed-point and the per-subsystem demand pattern with only mission-specific demand functions changing (solar powerplant replaces fission; boulder-acquisition + thermal-extraction replace trawl). The mass-demand-function layer is the clean seam; the framework substrate does not need structural redesign to carry a second architecture. | closed-loop machinery reused verbatim; only `nea_mass_demands.py` is new mission code; ≥ the SCOPE's 70%-shared intent met at the framework layer | H6 falsified if encoding NEA requires changing `framework/dry_mass.py` or the derivation contract (would mean the abstraction is leaky). |

### Scope honesty on H6

The SCOPE framed H6 as a *walker phase-executor* share test (>70% of phase executors shared between trees). Since the closed-loop refactor moved the load-bearing physics into the mass-demand layer, I test H6 at the **closed-loop-machinery + mass-demand-seam** layer: does the mission-agnostic `derive_dry_mass` carry NEA with only new mission-specific demand functions? That is the sharper abstraction test post-refactor. Wiring 4 separate walker phase-executors into a full `Mission` tree (the SCOPE's literal step 3) is deferred as a follow-on if the orchestrator wants the walker-level forest test; it would not change the closed-loop verdict (delivered mass and mass-loop closure are computed in the demand + delivered-water model, not the walker traversal).

## Method

1. Boulder candidate set (`inputs/nea_candidates.csv`) — 2008 EV5 + secondaries in 5–9 km/s, with size/mass/spectral-class/water-fraction anchors.
2. `nea_mass_demands.py` — closed-loop subsystem demands: **solar powerplant** (power_kwe / solar_specific_power + PMAD), SEP thrusters, boulder-acquisition, thermal-extraction module, structure (boulder-load), comms (1 AU, light), tankage. Reuses `framework.dry_mass.derive_dry_mass` unchanged.
3. Delivered-water model: `delivered = boulder × water_fraction × extraction_eff`; round-trip from Keck 6–10 yr anchor; per-mission cost bracket (H3 SCOPE anchors).
4. Closed-loop sweep over boulder {3,5,7,10,15} m, water fraction {0.4,1.8,3,5,10}%, extraction {60,75,90}%, fleet {1,3,5,10}.
5. Comparator vs Saturn closed-loop (0/150): mass-loop closure, delivered mass, annual throughput, cross-over floor.
6. KISS baseline reproduction test; grade H1–H6.

## Deliverables (commit order)
STUDY.md → inputs/nea_candidates.csv → nea_mass_demands.py + run harness + results → comparator → RESULTS.md → READING.md → test → handoff.

## Out of scope
Lunar tree; main belt; resolving decisions #14/#15; full walker phase-executor wiring (deferred, see H6 scope note); richer NPV than the SCOPE's cost brackets.
