# R-electric-outbound-rerun — Hyperion bug fix + Titan-inbound layered re-evaluation

**Round:** R-electric-outbound-rerun
**Started:** 2026-05-15
**Worker:** Rhea (orchestrator: Saturn)
**Branch:** iceberg-rhea
**Status:** complete, graded, committed

---

## Phase question

After fixing Hyperion's reported outbound-burn bug AND adopting Titan's continuous-thrust inbound delta-velocity (24.7–40.2 km/s instead of the matrix's impulsive 6.42 km/s), does the architecture-decision-matrix's year-twenty-plus megawatt all-electric end-to-end winner cell survive inside L0-05's 15-year round-trip ceiling?

Two specific-power variants in scope per Hyperion's stretch-parameter callout: 10 watts-per-kilogram (conservative) and 40 watts-per-kilogram (stretch).

## Hypothesis (pre-registered before run)

Four sub-claims:

- **H-eor-a — Outbound burn time understatement factor.** At 1 megawatt-electric, decomposed-mid mass model, Isp 2000 s, chunk 200 t, the corrected outbound burn time will be **2.0×–3.0×** the bugged result. (Tsiolkovsky mass ratio at Isp 2000 s and outbound Δv 17.97 km/s is ≈ 2.50; the bug understates by exactly the mass-ratio factor.)
- **H-eor-b — Smallest reactor closing inside 15 yr, decomposed-mid, matrix-inbound (6.42 km/s).** The corrected smallest-closing-reactor will be **strictly greater than 500 kWe** (upward shift from the original R-electric-outbound result).
- **H-eor-c — Titan-inbound 24.7 km/s at 10 W/kg.** **No 10-W/kg cell** in the matrix sweep will close inside the 15-year ceiling at titan's high-elliptical inbound delta-velocity.
- **H-eor-d — Titan-inbound 24.7 km/s at 40 W/kg.** At the 40-W/kg specific-power stretch parameter, **at least one cell** will close inside 15 years at titan's high-elliptical inbound, recovering the megawatt all-electric architecture.

## Test

`run.py` builds four sweeps over (reactor 10–1000 kWe) × (mass model: bundled_10_W_per_kg, bundled_40_W_per_kg, decomposed_mid), Isp 2000 s, chunk 200 t:

- **Sweep A** — matrix inbound Δv 6.42 km/s, **bug FIXED**.
- **Sweep B** — matrix inbound Δv 6.42 km/s, **bug INTACT** (reproduction sanity check against original R-electric-outbound tables.md).
- **Sweep C** — titan inbound Δv 24.7 km/s (high-elliptical + lunar gravity assist), **bug FIXED**.
- **Sweep D** — titan inbound Δv 40.2 km/s (B-ring, no lunar gravity assist), **bug FIXED**.

Plus a unit-test-style sanity check (`unit_sanity_check`) verifying the formula correction against an analytic Tsiolkovsky case and confirming the bugged-call understatement equals the mass ratio.

Pre-bug-fix Sweep B reproduces R-electric-outbound's tables.md numbers row-for-row for the two mass models that round had (bundled_10_W_per_kg, decomposed_mid), establishing the rerun is layered cleanly on top of the original methodology.

## Result

### Bug confirmation (unit sanity check)

Scenario: m_final = 10 t, Δv = 9 km/s, Isp 2000 s, 1 MWe. Tsiolkovsky mass ratio = 1.582.

| Call pattern | Computed m_prop (t) | Matches truth? |
|---|---:|:---:|
| `burn_from_dry_end(10 t)` [corrected] | 5.822 | yes |
| `burn_from_wet(15.82 t)` [used correctly] | 5.822 | yes |
| `burn_from_wet(10 t)` [the bugged call pattern] | 3.680 | **understated by 1.582× = mass_ratio** |

Burn-time understatement factor = mass-ratio (same as propellant-mass understatement, because burn time is linear in propellant mass at constant thrust).

**Bug confirmed.** Outbound call site `run.py:223` passes `m_tug_t` (dry mass at end of burn — the tug after escape, with no propellant left) to a function that interprets its first argument as wet-at-start. Outbound propellant and outbound burn time are understated by Tsiolkovsky mass ratio, which at Isp 2000 s and outbound Δv 17.97 km/s is **2.50×**.

### Inbound call site is NOT bugged (Hyperion's earlier read holds)

Saturn flagged `run.py:236` for verification (`constant_thrust_burn(m_tug + chunk_t, DV_INBOUND, ...)`). I worked through it and Hyperion's original read is correct, for a reason that deserves to be in the record:

The ICEBERG inbound propulsion is **chunk-fed electric** — water sublimated from the captured ice mass is fed to the electric thrusters. The chunk IS the propellant tank. Therefore at start of inbound burn, the wet mass is m_tug + chunk_t (tug plus the entire ice block including all its water). At end of inbound burn, the dry mass is m_tug + (chunk_t − prop_inbound) = m_tug + delivered. The function is called with the wet-at-start mass, which is exactly what it expects. No fix needed.

This is the "subtly defensible" reading the assignment asked me to look for. The function is being abused on the outbound side (where outbound prop comes from a separate tank attached to the dry tug, so m_tug really is dry-at-end) but used correctly on the inbound side (where the chunk and propellant are the same thing).

### Headline numbers — 1 MWe, decomposed-mid, Isp 2000 s, chunk 200 t, across inbound regimes

| Inbound regime | Mass model | t_out (yr) | t_in (yr) | Round-trip (yr) | Delivered (t) | Closes 15 yr? |
|---|---|---:|---:|---:|---:|:--:|
| Matrix 6.42 km/s (corrected) | decomposed-mid | 0.44 | 0.61 | **14.22** | 135.4 | **yes** |
| Titan 24.7 km/s (high-elliptical + lunar gravity assist) | decomposed-mid | 0.44 | 1.55 | 15.17 | 34.2 | no |
| Titan 24.7 km/s (high-elliptical) | bundled 40 W/kg | 0.46 | 1.56 | 15.19 | 33.5 | no |
| Titan 40.2 km/s (B-ring) | decomposed-mid | 0.44 | 1.89 | 15.51 | **−1.7** | no |
| Titan 40.2 km/s (B-ring) | bundled 40 W/kg | 0.46 | 1.90 | 15.53 | **−2.5** | no |

### Close-threshold table

| Sweep | bundled_10_W_per_kg | bundled_40_W_per_kg | decomposed_mid |
|---|---|---|---|
| Matrix-inbound 6.42 km/s, bugged (R-electric-outbound's original) | 1000 kWe / 14.59 yr | 500 kWe / 14.52 yr | 500 kWe / 14.49 yr |
| Matrix-inbound 6.42 km/s, **bug fixed** | **no class closes** | 500 kWe / 14.85 yr | 500 kWe / 14.80 yr |
| Titan-inbound 24.7 km/s, high-elliptical | **no class closes** | **no class closes** | **no class closes** |
| Titan-inbound 40.2 km/s, B-ring | **no class closes** | **no class closes** | **no class closes** |

### Hypothesis grading

| Sub-claim | Predicted | Actual | Held? |
|---|---|---|---|
| H-eor-a | 2.0–3.0× burn-time understatement at 1 MWe decomposed-mid | 2.62× | yes |
| H-eor-b | corrected close-reactor decomposed-mid > 500 kWe | corrected 500 kWe (same as bugged) | **no** — falsified |
| H-eor-c | no 10-W/kg cell closes at titan 24.7 km/s | no cell closes (any of 10-W/kg, 40-W/kg, decomposed-mid) | yes |
| H-eor-d | at least one 40-W/kg cell closes at titan 24.7 km/s | no 40-W/kg cell closes either | **no** — falsified |

## Reading

**Bug-fix-only impact is asymmetric across mass models.** The bug fix DID matter — but not in the direction I pre-registered. At decomposed-mid, the smallest closing reactor stays at 500 kWe (corrected round-trip 14.80 yr vs bugged 14.49 yr — both close, just less margin). H-eor-b is cleanly falsified at decomposed-mid. But the bug fix flips `bundled_10_W_per_kg` from "closes at 1000 kWe" (bugged) to "no class closes inside 15 yr" (corrected). So the bundled 10-W/kg row of the matrix DOES collapse on the bug fix alone — the decomposed-mid row, which has a much lighter tug at 1 MWe (30 t vs 108 t bundled), absorbs the bug-fix penalty without crossing the 15-year boundary.

The H-eor-b prediction was too narrow. I asked "does decomposed-mid's smallest-closing-reactor shift upward?" when I should have asked "does any mass model's closing threshold shift?" The bundled-10 collapse is the real bug-fix headline.

**Titan-inbound is the architecture killer, not the bug.** At titan's best-case 24.7 km/s inbound (high-elliptical Saturn departure + lunar gravity assist credit), the 1 MWe / decomposed-mid round-trip is 15.17 years — only 0.17 years (62 days) past the L0-05 ceiling. Tantalizingly close, but past the requirement. And **even at 40 W/kg specific power**, no cell closes inside 15 years at titan-inbound 24.7 km/s. H-eor-d is cleanly falsified. The hypothesis that "40 W/kg recovers the architecture" turns out to be wrong. The 40-W/kg savings show up mostly in lower tug mass (decomposed-mid is already near the floor on tug mass), not in changing the inbound burn time which is what's killing the round-trip.

**At titan-inbound 40.2 km/s (B-ring, no lunar gravity assist) the chunk-fed economics invert.** At 1 MWe (either decomposed-mid or 40 W/kg), the inbound burn at 40.2 km/s consumes more propellant than the chunk itself contains — delivered mass goes negative. The 200-t chunk cannot fuel its own return at 40.2 km/s with the chunk-fed-electric architecture at Isp 2000 s. This is a hard structural constraint, not a margin issue: it means **the current ICEBERG-conops B-ring chunk-departure architecture is incompatible with all-electric end-to-end at megawatt class.** The only way to deliver mass under B-ring departure is to either (a) raise specific impulse (which Titan showed blows the burn-time budget further), (b) raise reactor power well beyond 1 MWe (orders of magnitude that we'd have to re-baseline), or (c) shrink the chunk.

**Combined headline.** With Hyperion's bug fix applied AND Titan's continuous-thrust inbound delta-velocity adopted, **no tested cell in the year-twenty-plus megawatt all-electric end-to-end winner column closes inside L0-05 at any tested specific power**. The matrix's year-twenty-plus winner cell is structurally falsified at conservative assumptions across all three mass models I tested. The miss is small (0.17 yr at decomposed-mid 1 MWe, titan high-elliptical) but cleanly outside the requirement.

**This does not retire the megawatt all-electric architecture wholesale** — there are escape paths:

1. Move chunk operations to high-elliptical Saturn orbit (engineering change to bag/capture mechanism). This is titan's recommendation. Brings inbound to 24.7 km/s minimum.
2. Relax L0-05 from 15 years to ~17 years. Decomposed-mid at 1 MWe / titan 24.7 km/s closes in 15.17 yr, so a 2-year requirements amendment buys this cell back. (REQUIREMENTS.md change — orchestrator decision.)
3. Shrink the chunk below 200 t. Halving to 100 t would reduce inbound prop demand proportionally; the inbound burn time at 24.7 km/s would drop from 1.55 yr to ~0.78 yr at decomposed-mid 1 MWe → round-trip ~14.4 yr → closes. **But that's a different architectural decision** — halving delivered mass per mission changes the economics fundamentally.
4. Adopt the R-chunk-as-heat-shield revisit candidate. If the Earth-side aerocapture works, it collapses ~18 km/s of inbound budget to one aerodynamic pass, restoring the L0-05 margin.

Of these, (1) and (4) are the structurally clean paths. (2) is a requirements-side rescue and should be a deliberate decision. (3) trades architecture for the 70% delivered-fraction claim that's already under pressure from titan's 20% finding.

## Revisit

H-eor-a held cleanly (2.62× understatement vs predicted 2.0–3.0). The pre-registered range was based on the Tsiolkovsky mass-ratio analytic; the small overage came from the fixed-point iteration on tank mass that grows with corrected (larger) propellant load.

H-eor-b falsified because I confused two questions:
- "Does the bug fix change the smallest closing reactor?" — depends on the mass model.
- "Does the bug fix change the smallest closing reactor *at decomposed-mid specifically*?" — no, because the 1 MWe decomposed-mid tug is light enough (30 t) that the corrected outbound prop is still affordable.

The right pre-registration would have been across mass models — bundled_10_W_per_kg in particular DOES shift (from 1000 kWe-closing to no-class-closing). Methodology note: when an effect is mass-model-dependent and the proportional understatement is universal, pre-register at the *most-sensitive* mass model, not the default one. Adding to convention log under "lesson #7 — cheapest path vs only viable path" family — closest variant is "pre-register at the model that maximizes the effect, not the model you find most plausible."

H-eor-c held strongly. Not even close — bundled-10 at 1 MWe titan-inbound 24.7 misses by 1.87 yr, bundled-40 at 1 MWe titan-inbound 24.7 misses by 0.19 yr, decomposed-mid at 1 MWe titan-inbound 24.7 misses by 0.17 yr.

H-eor-d falsified — I expected 40 W/kg to recover the architecture. It does not, because at 1 MWe decomposed-mid the tug is already only 30 t and the dominant time-cost is inbound burn (chunk-fed at 24.7 km/s is ~1.5 years), which is set by Isp and power, not tug mass. Lighter tug (40 W/kg bundled) saves less than 1% round-trip time. The 40-W/kg parameter buys reactor-stack mass margin, not round-trip time at this operating point.

This is a genuinely surprising finding. Hyperion noted that the matrix's round-trip-time promises lean on 40 W/kg, and I came in expecting that to be the load-bearing assumption. It isn't, at megawatt class — the load-bearing assumption is **inbound delta-velocity**, which is the territory titan exposed. The 40-W/kg sensitivity matters at sub-megawatt class where tug mass dominates and where bundled-10 falls apart on bug-fix alone, but at megawatt-class with titan's inbound numbers it does not move the L0-05 needle.

## Cross-learning

- **Positive for R-electric-outbound revisit:** the bug fix is confirmed (2.50× mass-ratio understatement at Isp 2000 / Δv 17.97). Orchestrator should decide whether to patch the original round on main or keep it as a known-bugged audit-trail record with a forward pointer to this rerun.
- **Positive for titan's R-inbound-dv-continuous-thrust:** titan's headline holds load-bearing. Combined with the corrected outbound, megawatt all-electric end-to-end does NOT close inside L0-05 at any tested specific power. Titan's recommendation to move chunk operations to high-elliptical is necessary but not sufficient.
- **Negative for matrix's year-twenty-plus megawatt all-electric column:** the cell needs *either* a requirements amendment (L0-05 → 17 yr), *or* a chunk-size reduction (200 t → ~100 t), *or* a chunk-as-heat-shield rescue path (R-chunk-as-heat-shield revisit). The current matrix language presumes none of these.
- **Negative for hyperion's "40-W/kg recovers the architecture" implication:** falsified at megawatt class. 40-W/kg matters at sub-megawatt class but does not retrieve the year-twenty-plus L0-05 closure.
- **Positive for R-chunk-as-heat-shield revisit (currently a deferred round):** titan called this a high-priority follow-on. This rerun reinforces that — chunk-as-heat-shield is the architecturally clean rescue path because it collapses ~18 km/s of inbound budget rather than chasing year-fraction margin at the L0-05 boundary.
- **Methodology note (added to convention log):** when an effect's magnitude is mass-model-dependent and the underlying mechanism is universal (here: outbound prop understated by mass-ratio across all models), pre-register at the model where the effect is largest, not the median model. Decomposed-mid was the wrong place to test H-eor-b — bundled-10 would have surfaced the effect cleanly.

## Files of record

```
water-prop/rounds/R_electric_outbound_rerun/STUDY.md                          # this file
water-prop/rounds/R_electric_outbound_rerun/run.py                            # deterministic; uv run python rounds/R_electric_outbound_rerun/run.py
water-prop/rounds/R_electric_outbound_rerun/results/electric_outbound_rerun.json
water-prop/rounds/R_electric_outbound_rerun/results/tables.md
```

## Out of scope (per assignment)

- Did not edit `water-prop/rounds/R_electric_outbound/` (the bugged original is preserved as an audit-trail record; orchestrator decides whether/how to patch it on main).
- Did not edit shared docs: ARCHITECTURE-DECISION-MATRIX.md, REQUIREMENTS.md, REQUIREMENTS-L1.md, ICEBERG-pitch.md, ICEBERG-conops.md, ICEBERG-bag-engineering.md, .planning/amendment-scaffold-titan-handoff.md. All findings flow back via handoff.
- Did not audit the 40-W/kg specific-power assumption itself — treated it as a matrix parameter as instructed.
- Did not investigate chunk-size reduction or chunk-as-heat-shield in detail — flagged as cross-learning items, not pursued.
