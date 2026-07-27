# R-k2-bus-architecture-study — STUDY (pre-registration)

**Worker:** hyperion (re-spawn 2). **Date:** 2026-05-26. **Status:** pre-registration frozen; analysis pending.
**Round type:** research / business-strategy (no mission_graph code per SCOPE out-of-scope). Public-source; every external fact cited with a link.

**Question (from SCOPE):** can the ICEBERG vehicle be a stack of N K2 Space buses via on-orbit assembly, and what does that imply for the framework's `vehicle_mass_kg` / `power_kwe` axes — procure vs build?

The SCOPE (authored 2026-05-21) did not pre-register hypotheses. I add them here per PROTOCOL, and I anchor the round to a finding that did not exist when the SCOPE was written: **R-near-earth-asteroid-mission-tree (this session) showed solar-electric power at ~1 AU closes the closed-loop mass loop (75/75) where Saturn fission does not (0/150), because solar at 1 AU is ~25–30× lighter per kWe than KRUSTY fission.** K2 is a mass-produced solar-electric bus. So the K2 question is really: *is the buyable, flown solar-bus chassis the natural ICEBERG-successor (inner-system / NEA) vehicle, while Saturn remains the one architecture K2 cannot serve (solar dead at 9 AU)?*

## Frozen source set
- K2 public specs + funding (SpaceNews, Via Satellite, K2 site, DCD/Payload). Verified 2026-05-26.
- Locked power beliefs: flown RTG ~5.3 W/kg; KRUSTY ~2.4 W/kg system; 40 W/kg MW-NEP aspirational at TRL 2 (beliefs `0d5c8822`, `0418e2c9`).
- Closed-loop mass machinery + NEA result (this session): `nea_mass_demands.py`; titan-6 Saturn 0/150.
- Comparable bus landscape: Maxar 1300, LM-2100, Northrop GEOStar, Boeing 702 (SCOPE list; surveyed at ROM level).

## Pre-registered hypotheses (honest predictions before the comparison table is built)

| # | Hypothesis | Predicted | Falsification |
|---|---|---|---|
| H1 | K2 Mega's flown system specific power is **10–20 W/kg** (20 kW / ~2 t wet to ~1 t dry-bus) — above flown RTG (5.3) and KRUSTY fission (2.4), below the 40 W/kg MW-NEP aspiration. | Mega ∈ [10, 20] W/kg | Falsified if Mega < 8 or > 25 W/kg on a defensible mass basis. |
| H2 | K2 buses are a **literal chassis only for the inner-system / NEA ICEBERG successor**, not for Saturn: at 9 AU a 20-kW (1 AU) array yields ~0.2 kW, two orders of magnitude short. The solar-at-Saturn gap is **fundamental physics, not a contractual gap**. | K2 viable inner-system, dead at Saturn; gap is physical | Falsified if a credible K2 power path delivers ≥ kilowatts at Saturn (it cannot, absent a grafted reactor — which is no longer "a K2 bus"). |
| H3 | A K2-derived 40-kWe inner-system vehicle's whole power-bus mass (~2–3 t at 15 W/kg system) sits **comfortably inside the NEA closed-loop dry-mass budget (~45 t)** — i.e. K2-anchored numbers **corroborate, do not break, the NEA mass-loop closure**. | K2-anchored power-bus ≪ NEA dry mass; corroborates | Falsified if K2-anchored power-bus mass would push the NEA vehicle to non-closure. |
| H4 | Procure-vs-build favors **procure for the demonstrator** (K2 is flown, mass-produced, cheaper than a clean-sheet bus) but the deep-space-heritage gap (7-yr cruise; K2 has LEO/MEO/cislunar heritage only) is the binding risk, not cost. | procure cheaper; heritage is the binding gap | Falsified if a clean-sheet bus is both cheaper AND faster to deep-space-qualify. |
| **H5 (load-bearing)** | The right framework action is **NOT** a new `vehicle_bus_architecture` enum axis. K2 vs clean-sheet is a **cost/heritage/supply-chain** distinction that does not change the closed-loop *physics* (mass, power, delivered water) the framework computes. K2 belongs in the demonstrator cost/heritage narrative and the NEA-successor conops, not as a new sweep axis. Recommend a documented `power_source ∈ {solar, fission}` toggle on the mass-demand layer (which the NEA round already de facto introduced) rather than a bus-vendor axis. | no bus-vendor axis; power_source toggle suffices | Falsified if K2 vs clean-sheet changes a framework-computed closure output (would justify a real axis). |

### Honest prior
I expect H1–H5 to hold and the round to conclude: **K2 is strategically important as the off-the-shelf chassis for the NEA / inner-system successor architecture and for the demonstrator, but it is not a framework-physics change and it does nothing for Saturn.** The useful deliverables are the comparison table, the procure-vs-build recommendation, and the conops sketch — not a new sweep axis.

## Deliverables
COMPARISON.md (clean-sheet vs K2 Giga stack vs hybrid table + specific-power + closed-loop cross-check) → RESULTS.md (H1–H5 verdicts + framework-param recommendation) → READING.md (K2↔NEA synthesis + conops sketch) → handoff. No run.py (SCOPE: no code).
