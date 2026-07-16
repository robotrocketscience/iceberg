# R-megawatt-marvl-radiator — does the megawatt all-electric winner cell survive MARVL-anchored radiator mass?

**Round:** R-megawatt-marvl-radiator
**Started:** 2026-05-15
**Worker:** Rhea
**Branch:** iceberg-rhea
**Status:** complete, graded, committed

---

## Phase question

Locked R-power-wonder finding (May 2026): at megawatt-electric scale, the radiator subsystem is 40–55 percent of total system mass (per National Academies 2021 Space Nuclear Propulsion report and NASA Modular Assembled Radiators for Very Large systems studies), not the ~4 percent that decomposed-mid's `alpha_radiator = 2 kW-thermal/kg` implies. The bundled formula (5 t + reactor_kWe × 0.1 t/kWe) is closer-to-correct at megawatt scale; decomposed-mid is the optimistic-wrong model.

Question: when the megawatt mass model is re-anchored to MARVL realism, and all upstream corrections from R-electric-outbound-rerun and R-outbound-dv-continuous-thrust and titan's R-inbound-dv-continuous-thrust are applied — does any reactor power class close inside L0-05 at all-electric end-to-end? And does the year-zero-through-fifteen chemical-kick + electric-inbound architecture survive MARVL realism?

## Hypothesis (pre-registered)

- **H-mr-a** — MARVL-anchored decomposed model 1 megawatt-electric dry tug mass (no propellant) is **95–115 tonnes** (close to bundled 10 W/kg's 105 tonnes; far from decomposed-mid's 29 tonnes).
- **H-mr-b** — MARVL-anchored 1 megawatt-electric round-trip at corrected outbound delta-velocity high-elliptical + titan inbound 24.7 km/s exceeds **18 years**.
- **H-mr-c** — Delivered mass at MARVL-anchored 1 megawatt-electric / titan-inbound-24.7 / 200-tonne chunk is **negative** (chunk-fed propellant insufficient).
- **H-mr-d** — At 200 kilowatt-electric MARVL-anchored under chemical-kick + electric-inbound architecture, round-trip closes inside L0-05 with positive delivered mass.
- **H-mr-e** — No realistic-mass-model (decomposed-MARVL or bundled-10) megawatt all-electric cell closes inside L0-05, even at lunar-gravity-assist-credit-on-both-legs best case.

## Test

`run.py` constructs three mass models:
- `decomposed_mid` (R-electric-outbound's original, kept for cross-comparison)
- `decomposed_marvl` (MARVL-anchored: reactor+shield ~30%, power-conversion ~20%, radiator ~50% at 1 megawatt-electric; alpha_reactor 33 W/kg, alpha_PC 50 W/kg, alpha_radiator 0.047 kW-thermal/kg)
- `bundled_10_W_per_kg` (the 0.1 t/kWe formula, closer-to-correct per power-finding-4)

Three sweeps over (reactor 40–2000 kWe) × (mass model) at Isp 2000 s, chunk 200 t:
- **Sweep A** — megawatt all-electric, corrected outbound delta-velocity 29.56 km/s (no lunar gravity assist) + titan inbound 24.7 km/s
- **Sweep B** — same as A but lunar gravity assist credit on BOTH legs (outbound 27.56 km/s, inbound 24.7 km/s — most favorable composite)
- **Sweep C** — year-zero-through-fifteen architecture (chemical-kick outbound, off-ledger from the spacecraft electric thrusters' Δv budget; electric inbound at the matrix-impulsive 6.42 km/s, which IS valid for chemical-kick because chemical-kick preserves Oberth-bonus impulsive injection)

## Result

### Mass breakdown at 1 megawatt-electric (no propellant)

| Model | m_fixed (t) | m_reactor (t) | m_PC (t) | m_radiator (t) | Total (t) | Radiator fraction |
|---|---:|---:|---:|---:|---:|---:|
| decomposed_mid | 3.0 | 20.0 | 5.0 | 1.2 | 29.2 | 4% |
| decomposed_marvl | 5.0 | 30.3 | 20.0 | 49.6 | 104.9 | 47% |
| bundled_10_W_per_kg | 5.0 | (bundled) | (bundled) | (bundled) | 105.0 | — |

**MARVL-anchored matches bundled-10 within 0.1 tonnes at 1 megawatt-electric.** Power-finding-4 confirmed by reproduction.

### Megawatt all-electric corrected (Sweep A) at 1 megawatt-electric

| Mass model | m_tug (t) | t_out (yr) | t_in (yr) | Round-trip (yr) | Delivered (t) | Closes 15 yr? |
|---|---:|---:|---:|---:|---:|:--:|
| decomposed_mid | 34.5 | 0.99 | 1.57 | 15.92 | 32.1 | no |
| decomposed_marvl | 124.0 | 3.58 | 2.18 | **19.56** | **−34.4** | no |
| bundled_10_W_per_kg | 124.1 | 3.58 | 2.18 | 19.57 | −34.5 | no |

### Year-zero-through-fifteen architecture (Sweep C) — close threshold per mass model

| Mass model | Smallest reactor closing with positive delivered (kWe) | Round-trip at close (yr) | Delivered (t) |
|---|---:|---:|---:|
| decomposed_mid | 500 | 14.30 | 139.7 |
| decomposed_marvl | 500 | 14.51 | 128.8 |
| bundled_10_W_per_kg | 500 | 14.51 | 128.8 |

### Hypothesis grading

| Sub-claim | Predicted | Actual | Held? |
|---|---|---|---|
| H-mr-a — MARVL 1 MWe tug mass | 95–115 t | 104.9 t | yes |
| H-mr-b — MARVL 1 MWe / titan-24.7 round-trip > 18 yr | > 18 yr | 19.56 yr | yes |
| H-mr-c — Delivered mass < 0 | < 0 | −34.4 t | yes |
| H-mr-d — MARVL 200 kWe chemical-kick closes | closes positive | 16.12 yr (does not close); closes at 500 kWe | **falsified** |
| H-mr-e — No realistic-mass-model megawatt cell closes at LGA-both-legs | no cell closes | no cell closes (decomposed-MARVL or bundled) | yes |

## Reading

**Decomposed-mid is the optimistic-wrong model at megawatt scale.** MARVL-anchored gives 104.9 tonnes at 1 megawatt-electric, matching the bundled formula's 105 tonnes within rounding. Power-finding-4 fully confirmed by reproduction here. The earlier R-radiator-mass-penalty round had concluded "bundled over-counts megawatt stack by 3×"; that conclusion is inverted under MARVL anchoring — bundled was right at megawatt scale, decomposed was wrong by 3×. The matrix's year-twenty-plus winner cell was carried on the decomposed-mid number; that cell needs to be carried on the bundled (or MARVL-anchored) number going forward.

**Megawatt all-electric end-to-end is structurally falsified at MARVL realism.** Round-trip at 1 megawatt-electric / decomposed-MARVL / corrected outbound / titan-inbound = 19.56 years, missing L0-05 by 4.56 years. Delivered mass is −34.4 tonnes (chunk-fed propellant supply runs out before completing the inbound burn). Even at 2 megawatt-electric and lunar-gravity-assist on both legs (Sweep B): round-trip 18.15 years, delivered −116.6 tonnes. The architecture is comfortably falsified, not marginally.

**The year-zero-through-fifteen chemical-kick architecture survives MARVL realism but only at ≥ 500 kilowatt-electric.** H-mr-d falsified my pre-registration: I had predicted 200 kilowatt-electric closes, but the smallest reactor closing in this architecture is 500 kilowatt-electric across all three mass models (and the closure is comfortable: round-trip 14.30–14.51 years, delivered 128–140 tonnes). 200 kilowatt-electric misses L0-05 at 16.12 years.

**The 500-kilowatt-electric architecture floor is well beyond FSP Phase 2's 100-kilowatt-electric scope** (per locked power-finding-3: FSP Phase 2 not awarded as of May 2026, scope grown to 100 kilowatt-electric, FY2026 budget zeroed NEP/NTP technology lines). And per power-finding-1, 40 W/kg specific power is a TRL-2 paper-study aspirational figure, not anchored to flight or extrapolation of KRUSTY ground-test data (which measured ~2.4 W/kg system-level). And per power-finding-2, US space-fission programs have a 0-of-6 base rate of reaching orbit within their originally-stated decade since 1965 with ~$1.7B post-SNAP spent and zero orbital outcomes.

Put together: **the year-zero-through-fifteen chemical-kick + 500-kilowatt-electric architecture is the ONLY surviving cell**, and even it sits well outside any currently-funded US fission program. The matrix's year-twenty-plus megawatt all-electric end-to-end winner cell is falsified; the matrix's year-zero-through-fifteen Variant B winner cell needs a 500-kilowatt-electric reactor that doesn't exist on the current FSP roadmap.

## Revisit

H-mr-a, b, c, e all held. H-mr-d falsified — I had implicitly assumed the chemical-kick architecture closes at 200 kilowatt-electric because that's a roughly Kilopower-class number that fits the "Kilopower Variant B" naming. Actually the chemical-kick architecture closes at 500 kilowatt-electric across all tested mass models; 200 kilowatt-electric misses by 1.12 years. Lesson: don't conflate the naming of a matrix cell (Kilopower Variant B) with the actual reactor power required for the architecture to close at L0-05. The matrix label and the closure floor can be different numbers.

This is the second methodology mistake of the same shape from today (the first was H-od-d in R-outbound-dv-continuous-thrust). Both falsifications came from numeric ranges set without doing the arithmetic. Adding to convention log: **pre-register numeric ranges only after running the back-of-envelope calculation, not before.**

## Cross-learning

- **Negative for matrix's year-twenty-plus megawatt all-electric end-to-end winner cell:** under MARVL-anchored mass + corrected outbound delta-velocity + titan's corrected inbound, the cell is falsified at every tested operating point including 2 megawatt-electric + lunar-gravity-assist-both-legs best case. Cell should be marked "infeasible under current FSP roadmap and conservative mass anchoring; revisit if chunk-as-heat-shield rescue closes."
- **Negative for matrix's year-zero-through-fifteen Variant B winner cell at FSP-scale reactor (100 kilowatt-electric):** under MARVL realism, this architecture closes only at ≥ 500 kilowatt-electric. The "Kilopower Variant B" labeling is misleading — the architecture needs roughly a 5× scale-up from FSP Phase 2's current scope.
- **Positive for promoting R-chunk-as-heat-shield-revisit (deferred → high priority):** even more strongly than R-outbound-dv-continuous-thrust's reading. Chunk-as-heat-shield collapses the Earth-side Δv terms (segments 4+5 inbound, 4'+5' outbound = ~36 km/s of round-trip Δv) into aerodynamic passes; that's exactly the savings that would let the architecture close at lower reactor power.
- **Positive for revisiting R-radiator-mass-penalty:** the prior conclusion that "bundled over-counts by 3×" was anchored against optimistic decomposed numbers. Re-run the comparison against MARVL-anchored decomposed; the conclusion likely inverts. Round candidate for orchestrator.
- **Methodology lesson:** when an external authoritative finding lands (here, locked R-power-wonder finding 4 from National Academies / MARVL), audit every downstream round that uses the now-known-wrong number, not just the one that introduced it. R-radiator-mass-penalty introduced decomposed-mid; R-electric-outbound used it; R-electric-outbound-rerun used it; R-inbound-dv-continuous-thrust used it. The drift compounds when the upstream optimism is small (4% radiator share) but pervasive.

## Files of record

```
water-prop/rounds/R_megawatt_marvl_radiator/STUDY.md
water-prop/rounds/R_megawatt_marvl_radiator/run.py
water-prop/rounds/R_megawatt_marvl_radiator/results/megawatt_marvl.json
water-prop/rounds/R_megawatt_marvl_radiator/results/tables.md
```

## Out of scope

- Did not propagate to ICEBERG-pitch, ICEBERG-bag-engineering, ICEBERG-conops, ARCHITECTURE-DECISION-MATRIX, REQUIREMENTS — shared docs, orchestrator-owned.
- Did not audit chunk-size reduction at MARVL — likely positive for closure but a separate round.
- Did not investigate non-Hohmann low-thrust trajectories — likely marginal at L0-05; trajectory-optimization is a follow-on round.
- Did not investigate whether FSP-style sub-megawatt fission at higher specific impulse closes — Isp sweep at MARVL is a follow-on round candidate.
