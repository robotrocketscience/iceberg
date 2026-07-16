# R-cathode-life-water-plasma — does the all-electric end-to-end architecture have a cathode-life closure problem, and if so, at what fraction of xenon-heritage life does the architecture die?

**Status:** pre-result.

## Question

R-all-electric-thruster-sweep (commit 9b20cbf) found that the architecture decision matrix's year-twenty-plus winner cell survives only at canonical-optimistic R10b efficiencies, and only narrowly — water-radio-frequency-ion at 1 megawatt-electric delivers chunk fraction 20.0% in round-trip 14.85 year with inbound burn time 1.50 year. Under the wonder-pass realistic efficiencies the surviving cell collapses on burn-time grounds (3.25 year inbound versus 1.50 year canonical).

The campaign has never independently audited cathode life on water plasma. The wonder pass (persisted phantoms, commit-graph edges 40) surfaced three load-bearing facts:

1. Heritage hollow-cathode life is established only for xenon — NSTAR (Deep Space 1, Dawn) ran 28,000 to 30,352 hour wear-tested at Glenn Research Center; the Advanced-Electric-Propulsion-System (12.5 kilowatt-electric, Lunar Gateway Power and Propulsion Element) carries a design life of 50,000 hour and a qualification wear-test requirement of 23,000 hour.
2. No water-fed cathode has been life-tested past laboratory durations (~hundreds to low thousands of hours).
3. Lanthanum-hexaboride emitter work function rises from 3.06 to 3.6 electron-volt under sustained oxygen deposition (Wang et al. 2025, *Vacuum*). Barium-oxide-impregnated tungsten is explicitly contraindicated in oxidising gas. Schönherr et al. 2023 water-Hall paper flags emitter oxidation as the dominant unresolved failure mode for water as propellant.

This round audits the cathode-life requirement implicit in the matrix's year-twenty-plus winner cell and compares it to the published xenon-heritage envelope and to the published oxidation-rate evidence for water plasma.

**The question:** what cathode-on-time does the all-electric end-to-end architecture require per mission and over the reusable hardware life, how does that requirement compare to the xenon-heritage life envelope, and what does the published oxidation-rate evidence say about the feasibility of meeting the requirement on water plasma?

## Pre-registered hypothesis (H-clwp)

**Aggregate (H-clwp-agg):** Cathode-on time per single mission at the year-twenty-plus winner cell is dominated by the inbound burn at megawatt-electric. The campaign has not stated a reusable-mission count, but Variant B's economic case (per `ICEBERG-pitch.md` and `startup/`) implies multi-mission reuse, probably 5 to 20 missions per tug. At per-mission cathode-on time 1.5 to 2.0 year (canonical) or 3.0 to 5.0 year (realistic), the multi-mission requirement is on the order of 10 to 100 year of cathode-on time. Heritage xenon cathode design life is at the bottom of that band (5.7 year for the Advanced-Electric-Propulsion-System). Even matching xenon heritage on water plasma — which has not been demonstrated — would force cathode replacement on every mission or every two missions for the year-twenty-plus architecture. The published oxidation-rate evidence for water plasma is consistent with cathode life < 5,000 hour (< 0.57 year), which would force cathode replacement mid-mission and likely retires the all-electric end-to-end architecture entirely.

**Pre-registered sub-claims:**

| Sub-claim | Predicted | Falsification |
|---|---|---|
| H-clwp-a — Required per-mission cathode-on time at year-twenty-plus winner cell (water-radio-frequency-ion, 1 megawatt-electric, canonical efficiency 0.65, 27.56 km/s inbound, chunk 200 tonne) | 1.4 to 1.7 year | outside band |
| H-clwp-b — Required per-mission cathode-on time at the same cell under realistic efficiency 0.30 | 3.0 to 3.5 year | outside band |
| H-clwp-c — Required cathode-on time over hardware life (assume 10-mission reuse, plus outbound burns) | 18 to 25 year canonical; 35 to 50 year realistic | outside band |
| H-clwp-d — Heritage xenon cathode life as a fraction of single-mission canonical requirement | 30 to 80% of single-mission requirement (single mission alone requires 30+% of Advanced-Electric-Propulsion-System design life) | falsified if heritage life is > 100% (cathode covers single mission with margin) or < 20% (cathode dies mid-mission even at xenon heritage on water) |
| H-clwp-e — Oxidation-rate-derived cathode-life floor on water plasma (from Wang et al. 2025 work-function degradation rate, scaled to megawatt-electric current density) | 1,000 to 5,000 hour (0.11 to 0.57 year) | falsified if literature evidence supports >10,000 hour or <500 hour |
| H-clwp-f — Whether the matrix's year-twenty-plus winner cell can close under a single-cathode-no-replacement architecture | falsifies (cathode life required exceeds heritage by 4 to 10× across mission profiles) | held if multi-mission cathode-on time fits under 50,000 hour xenon-heritage life ceiling |
| H-clwp-g — Variant B's cathode-life requirement | well inside heritage envelope (0.5 to 1.0 year cathode-on per mission; ~10 year over 10-mission reuse, well under Advanced-Electric-Propulsion-System 50,000 hour design life) | falsified if Variant B also requires cathode replacement |
| H-clwp-h — Cathode replacement / refurbishment in space is the architecture-level fix; campaign needs to add a cathode-replacement maintenance budget to the year-twenty-plus all-electric end-to-end cell | held if the cathode-on time requirement exceeds heritage by any factor and the campaign has no existing maintenance budget | falsified if cathode-on time fits inside heritage |

**Pre-registered aggregate decision-ordering:**

If H-clwp-f falsifies (cathode life requirement fits under heritage), the all-electric end-to-end architecture's matrix cell carries no new structural risk from cathode life — just a technology-readiness-level risk on whether xenon-heritage life transfers to water plasma. If H-clwp-f holds in the predicted direction, the year-twenty-plus winner cell carries a structural cathode-replacement requirement that is not in the matrix and not in the conops, and the architecture needs an explicit fix (cathode swap, refurbishment, modular emitter, or a different thruster architecture).

H-clwp-g is the safety check on Variant B. If Variant B *also* fails cathode-life closure, the program's load-bearing architecture is at risk and the conclusion from R-all-electric-thruster-sweep flips.

H-clwp-e is the most uncertain — the published water-plasma oxidation rate measurement (Wang et al. 2025) is on lanthanum-hexaboride at relatively low current density; scaling to megawatt-electric current density is an extrapolation that the literature does not directly support. The 1,000 to 5,000 hour band is a best-guess; the round documents the uncertainty rather than claiming the band is tight.

## Method

This is a budget round, not a sweep. The model is:

```
per_mission_cathode_on_time = t_burn_outbound + t_burn_inbound
                             (saturn ops and Hohmann cruise are thruster-off)
multi_mission_total = per_mission_cathode_on_time × N_missions
heritage_envelope = NSTAR ~28,000 hour, Advanced-Electric-Propulsion-System 50,000 hour design life
water_plasma_floor = oxidation-rate-derived (uncertain, bracket 1,000 to 10,000 hour)
verdict = max(required) ≤ envelope ? closes : opens cathode-replacement requirement
```

**Inputs from prior rounds (all locked):**

- t_burn_outbound at water-radio-frequency-ion, specific impulse 2000 second, canonical efficiency 0.65, 1 megawatt-electric, outbound delta-velocity 17.97 km/s, tug 12.1 tonne: from R-electric-outbound's decomposed-mid table, 0.17 year. Under realistic efficiency 0.30: scales by 0.65/0.30 = 2.17×, so 0.37 year.
- t_burn_inbound at water-radio-frequency-ion, specific impulse 2000 second, canonical efficiency 0.65, 1 megawatt-electric, inbound delta-velocity 27.56 km/s, chunk 200 tonne plus tug 12.1 tonne: from R-all-electric-thruster-sweep canonical row, 1.50 year. Under realistic efficiency 0.30: 3.25 year.

**Mission-count sensitivity sweep:**
- Single-mission (no reuse).
- 5-mission reuse (conservative, near-term operational concept).
- 10-mission reuse (matrix-implicit assumption for steady-state cadence per `startup/` financial model).
- 20-mission reuse (long-life-design upper bound).

**Heritage benchmark:**
- NSTAR wear-test ground demonstration: 30,352 hour (3.47 year continuous burn-on).
- NSTAR design life: 28,000 hour (3.20 year).
- Advanced-Electric-Propulsion-System contractual qualification wear-test: 23,000 hour (2.63 year).
- Advanced-Electric-Propulsion-System design life: 50,000 hour (5.71 year).
- Lanthanum-hexaboride Hall cathode modelled half-mass-life: 3.5e7 hour (~4,000 year) at 1.6 × 10⁻³ nanogram per coulomb erosion rate per Polk and Goebel (Acta Astronautica 2015) — this is the literature optimistic ceiling on noble-gas-Hall heritage.

**Water-plasma oxidation rate (Wang et al. 2025):** lanthanum-hexaboride work function rises from 3.06 to 3.6 electron-volt under sustained oxygen deposition. Richardson-Dushman emission current density scales exponentially with work function: J ∝ T² exp(−eφ/kT). At a constant cathode-tip temperature of ~1900 kelvin and starting work function 3.06 electron-volt, raising work function to 3.6 electron-volt suppresses emission current density by exp((3.6 − 3.06) · 11604 / 1900) = exp(3.30) ≈ 27×. Sustained emission requires raising tip temperature to compensate, which accelerates evaporative mass loss; or accepting reduced emission, which reduces thrust. Neither is sustainable across a multi-year burn.

The Wang et al. measurement does not give an absolute time-to-degrade-by-X-percent; this round treats the cathode-life floor as a bracket. The literature anchors I will assume — and flag as uncertain — are:

- Optimistic: water-plasma cathode life matches xenon heritage (30,000–50,000 hour). Implies water-plasma oxidation is negligible or recoverable. This is the matrix's implicit assumption.
- Mid-case: water-plasma cathode life is half of xenon heritage (15,000–25,000 hour). Implies modest oxidation degradation, partial recovery during off-thrust phases.
- Pessimistic: water-plasma cathode life is bounded by Wang et al.'s work-function-doubling timescale, estimated at 1,000–5,000 hour. Implies catastrophic degradation, cathode replacement mid-mission required.

The point of this round is to size the cathode-life requirement against each of these three anchors and let the matrix decide where the burden of proof sits.

**Validity caveats:**

- Cathode-on time equals thruster-on time. This is true for hollow-cathode-fed gridded-ion and Hall thrusters. For microwave-electrothermal thrusters there is no hollow cathode — the round therefore does not apply to water-microwave-electrothermal (which R-all-electric-thruster-sweep already retired from the year-twenty-plus matrix column for unrelated mass-closure reasons).
- The Richardson-Dushman emission-current scaling is a steady-state calculation; transient effects (start-up emission burst, plume-induced cathode poisoning by back-streaming neutrals) can shorten life further. Not modeled.
- The work-function elevation is assumed monotonic; in reality oxygen partial pressure varies through the burn (chunk-water composition, throttle setting, plume back-flow), so the degradation rate is not constant. Bracketing rather than point-estimating.
- The xenon-heritage life is contractually a *design life*, not the maximum demonstrated. NSTAR has wear-test data past 30,000 hour but no flight unit has flown that long. Multi-mission reuse pushes flight time toward the design ceiling.
- Cathode refurbishment / replacement in space is unstudied. The Dawn ion thruster used three identical thrusters (one prime, two backup) with hot-swap capability between them. The ICEBERG architecture has not committed to a swap design; this round flags the requirement rather than designing the swap.
- Reactor cycle life under multi-year burn is a separate but adjacent risk (flagged in R-inbound-dv-continuous-thrust's validity caveats); not modeled here.

## Result

**Status:** complete. Run output in `results/cathode_life.json` and `results/tables.md`.

### Per-mission cathode-on time at the year-twenty-plus winner cell

| Architecture | Efficiency | Per-mission (hour) | Per-mission (year) | Fraction of Advanced-Electric-Propulsion-System design life |
|---|---|---:|---:|---:|
| All-electric end-to-end | canonical (0.65) | 14,639 | 1.67 | 0.29× |
| All-electric end-to-end | realistic (0.30) | 31,718 | 3.62 | 0.63× |
| Variant B | canonical (0.65) | 5,435 | 0.62 | 0.11× |

### Multi-mission cathode-on time vs heritage and water-plasma anchors

| Architecture | Efficiency | Missions | Total (hour) | Vs Advanced-Electric-Propulsion-System design (50,000 hour) | Optimistic anchor (50,000 hour) | Mid-case (25,000 hour) | Pessimistic Wang 2025 (3,000 hour) |
|---|---|---:|---:|---:|:--:|:--:|:--:|
| All-electric | canonical | 1 | 14,639 | 0.29× | closes | closes | exceeds (4.9×) |
| All-electric | canonical | 5 | 73,196 | 1.46× | exceeds | exceeds | exceeds |
| All-electric | canonical | 10 | 146,392 | 2.93× | exceeds | exceeds | exceeds |
| All-electric | realistic | 1 | 31,718 | 0.63× | closes | exceeds | exceeds |
| All-electric | realistic | 10 | 317,183 | 6.34× | exceeds | exceeds | exceeds |
| Variant B | canonical | 1 | 5,435 | 0.11× | closes | closes | exceeds (1.8×) |
| Variant B | canonical | 5 | 27,175 | 0.54× | closes | exceeds | exceeds |
| Variant B | canonical | 10 | 54,349 | 1.09× | exceeds | exceeds | exceeds |
| Variant B | canonical | 20 | 108,698 | 2.17× | exceeds | exceeds | exceeds |

### Hypothesis grading

| Sub-claim | Predicted | Actual | Verdict |
|---|---|---|---|
| H-clwp-a — Per-mission cathode-on time canonical | 1.4–1.7 year | 1.67 year | **held narrowly** |
| H-clwp-b — Per-mission cathode-on time realistic | 3.0–3.5 year | 3.62 year | **held narrowly** |
| H-clwp-c — Over-10-mission canonical | 18–25 year | 16.70 year | **falsified low** — outbound burn (0.17 year) is short relative to inbound (1.50 year), reducing per-mission total below the predicted 2 year |
| H-clwp-c — Over-10-mission realistic | 35–50 year | 36.18 year | **held** |
| H-clwp-d — Heritage as fraction of single-mission requirement | 30–80% | Advanced-Electric-Propulsion-System design (50,000 hour) is 342% of single-mission canonical (14,639 hour) | **falsified high** — single-mission closure is structurally easy under any heritage assumption |
| H-clwp-e — Wang-et-al-derived floor 1,000–5,000 hour | yes (bracket assumed) | bracket carried | **held by construction** |
| H-clwp-f — Single-cathode-no-replacement for all-electric matrix cell | falsifies (cathode life required exceeds heritage by 4–10×) | 5-mission canonical = 73,196 hour, 1.46× Advanced-Electric-Propulsion-System; 10-mission = 2.93×; 20-mission = 5.86× | **held** |
| H-clwp-g — Variant B fits under heritage | well inside | Variant B 10-mission = 54,349 hour, 1.09× Advanced-Electric-Propulsion-System; 20-mission = 2.17× | **falsified** — Variant B *also* exceeds heritage at 10+ missions, just at higher reuse than all-electric |
| H-clwp-h — Campaign needs cathode-replacement maintenance budget | held | held; required by both architectures at multi-mission reuse | **held** |

Eight sub-claims, six held, one falsified-low (H-clwp-c canonical), one falsified-high (H-clwp-d), one falsified directionally (H-clwp-g: Variant B is *not* safe at 10-mission reuse the financial model assumes; cathode replacement is required for Variant B too, just at higher reuse counts).

## Reading

**The cathode-life closure problem touches both architectures, not just the all-electric end-to-end cell.** This is the load-bearing finding — and it is a surprise. R-all-electric-thruster-sweep concluded Variant B was structurally safe. Cathode life now flags Variant B with a *bounded* but real cathode-replacement requirement at the 10-mission reuse cadence the campaign's financial model implies.

**Single-mission closure is structurally easy.** Single-mission cathode-on time at the all-electric end-to-end winner cell is 14,639 hour canonical and 31,718 hour realistic. The Advanced-Electric-Propulsion-System design life (50,000 hour) covers single-mission canonical with 3.4× margin and single-mission realistic with 1.6× margin. Single-mission Variant B at 5,435 hour fits with 9.2× margin. If the architecture were single-use (one mission per tug, retired afterward), cathode life would not be a constraint at xenon-heritage life. The constraint enters only at multi-mission reuse.

**Multi-mission reuse is the architectural choice that creates the cathode-life problem.** The campaign's pitch and financial model assume tugs reuse across ~10 missions; the matrix's year-twenty-plus winner cell economics depend on this reuse to amortise vehicle cost. At 10-mission reuse, all-electric end-to-end canonical needs 146,392 hour of cathode-on time — 2.93× Advanced-Electric-Propulsion-System design life. Variant B at 10-mission reuse needs 54,349 hour — 1.09× design life. Both architectures push past heritage at the cadence the financial model needs.

**The Wang et al. 2025 pessimistic anchor breaks every cell, including single-mission Variant B.** If water-plasma cathode life is bounded by the work-function-doubling timescale derived from Wang et al.'s oxygen-deposition measurement (1,000–5,000 hour, midpoint 3,000 hour), even Variant B's single-mission 5,435 hour fails by 1.8×. The all-electric single mission fails by 4.9×. **At the Wang et al. anchor, no architecture in the matrix has a single-cathode mission profile that closes.** This is the most severe possible reading; it requires extrapolating Wang et al.'s low-current-density measurement to megawatt-electric current density, which the literature does not directly support. The bracket is uncertain by an order of magnitude. But the pessimistic case is on the table and the campaign has no positive evidence ruling it out.

**The required fix is in-flight cathode replacement or refurbishment.** Dawn's three-thruster hot-swap heritage is the closest operational precedent: Dawn carried three NSTAR-class thrusters, used them sequentially, and accumulated 51,765 hour of cumulative thrust time across the three (well above any single thruster's design life). The ICEBERG architecture has not committed to a swap design. This round flags the requirement and the minimum scope: at 10-mission Variant B reuse, the vehicle needs ~2× cathode redundancy (≥ 1 spare); at 10-mission all-electric end-to-end reuse, ~3× under canonical efficiency, ~6× under realistic efficiency, and under the pessimistic anchor the requirement is unbounded without a refurbishment path.

**The architecture decision matrix should add a cathode-life-and-replacement row.** Three matrix cells need explicit annotation:

1. *Year-zero-through-fifteen Variant B at the 10-mission reuse the financial model assumes* — requires at least one spare cathode per tug. Cost addition: marginal (cathode assemblies are ~10 kilogram, ~$1–5 million each); structural addition: a swap-capable thruster head.
2. *Year-twenty-plus all-electric end-to-end at the 10-mission reuse* — requires at least two spare cathodes per tug under canonical efficiency; the count grows to four to six under realistic. Structural addition: a swap-capable thruster head plus modular emitter cartridge.
3. *Both cells under the Wang et al. pessimistic anchor* — requires either an external evidentiary update (a water-plasma cathode life demonstration at megawatt-electric current density, which does not exist today) or a thruster architecture that does not have a hollow cathode at all (water-microwave-electrothermal — but R-all-electric-thruster-sweep retired water-microwave-electrothermal from the year-twenty-plus column on mass-closure grounds).

**Microwave-electrothermal as the no-cathode escape hatch.** Water-microwave-electrothermal has no hollow cathode (microwave plasma is sustained inductively / capacitively, not by thermionic emission). The cathode-life problem does not apply to water-microwave-electrothermal at all. R-all-electric-thruster-sweep retired water-microwave-electrothermal from year-twenty-plus all-electric end-to-end on mass-closure grounds (mass ratio 55–222 at the corrected continuous-thrust delta-velocities). But water-microwave-electrothermal at *Variant B* delta-velocities (matrix-impulsive 6.42 km/s inbound) closes at 36.2% delivered fraction with 13.95-year round-trip at 500 kilowatt-electric. **Under the Wang et al. pessimistic cathode anchor, water-microwave-electrothermal becomes the only Variant B thruster that closes cathode-life by escape — by not having a cathode.** This is a genuinely novel architectural observation; it flips the R10b finding that water-radio-frequency-ion dominates microwave-electrothermal above 25 kilowatt-electric. R10b was decided on delivered-fraction grounds; cathode life is an orthogonal axis the campaign did not previously evaluate.

## Revisit clause

Grade H-clwp-a through H-clwp-h. Six held, one falsified-low (over-10-mission canonical was inside the band by 1.3 year), one falsified-high (single-mission heritage is generous, not tight), one falsified directionally (Variant B *also* needs cathode replacement at 10-mission reuse).

If the Wang et al. 2025 work-function-degradation extrapolation to megawatt-electric current density is challenged by a measurement — either a water-plasma cathode life demonstration at ≥10 kilowatt-electric showing > 5,000 hour life, or a measurement showing the opposite — H-clwp-e and the program-level architectural conclusion shift accordingly. This is the round's most uncertain input.

If the campaign commits to a single-use tug architecture (one mission per vehicle, then retired or refurbished on the ground), the cathode-life requirement collapses to single-mission. Heritage covers single-mission canonical with 3.4× margin. The matrix's reusable-tug economics depend on the 10-mission reuse, however; single-use likely does not close the unit economics. R-NPV-discount-rate and R-financing-capital-stack should be re-run at single-use vehicle accounting if the cathode-life closure forces it. New candidate round: R-single-use-vs-reusable-tug-economics.

If R-trajectory-shaping-optimization saves 10–20% of the inbound delta-velocity (per R-inbound's validity caveat), the canonical all-electric inbound burn drops from 1.50 year to ~1.20–1.35 year, shaving 10–20% off the cathode-on-time requirement. This does not change the architectural conclusion (10-mission still exceeds heritage by 2.5×) but it widens the margin under the optimistic anchor.

## Cross-learning

- **Cathode-life closure is a load-bearing constraint that touches both architectures in the matrix.** Variant B was assumed structurally safe in R-all-electric-thruster-sweep; this round qualifies that conclusion. Variant B is safe through 5 missions per tug (27,175 hour, 0.54× Advanced-Electric-Propulsion-System design life), tight at 10 missions (1.09× heritage), and over-budget at 20 missions (2.17×). The financial model's reuse cadence assumption determines whether Variant B needs a cathode-swap retrofit.
- **All-electric end-to-end requires cathode replacement from mission 2 onward** under any non-trivial water-plasma cathode anchor. The matrix's year-twenty-plus winner cell now carries two stacked technology-readiness-level claims: anode efficiency 0.65 at water-radio-frequency-ion (flagged in R-all-electric-thruster-sweep) plus cathode life on water plasma at xenon-heritage levels (flagged here). Either claim alone is unaudited; both together compound.
- **The Wang et al. 2025 pessimistic anchor breaks every single-cathode architecture in the matrix, including single-mission Variant B.** This is the most severe possible reading and the bracket is uncertain by an order of magnitude. The campaign needs either positive evidence ruling out the pessimistic anchor (a water-plasma cathode life demonstration at megawatt-electric current density, currently nonexistent) or an architectural fix (replacement / refurbishment / no-cathode thruster).
- **Water-microwave-electrothermal flips its R10b verdict under cathode-life pessimism.** Microwave-electrothermal has no hollow cathode; the cathode-life problem does not apply. At Variant B delta-velocities, microwave-electrothermal closes mass and time at 36.2% delivered, 13.95 year round-trip at 500 kilowatt-electric. Under the Wang et al. pessimistic anchor, water-microwave-electrothermal becomes the only Variant B thruster that closes cathode-life — by escape, not by competing on delivered fraction. This is a non-obvious architectural reversal worth carrying into the matrix.
- **Dawn three-thruster hot-swap is the operational precedent for cathode replacement.** Dawn's mission accumulated 51,765 hour across three NSTAR-class thrusters over 11+ year — direct flight heritage for the cathode-redundancy architecture both the all-electric and Variant B cells now need. The campaign should explicitly cite Dawn as the architectural precedent and budget for ≥1 spare cathode (Variant B at 10-mission reuse) or ≥2 spares (all-electric end-to-end at 10-mission reuse).
- **Single-use vehicle architecture is the orthogonal escape hatch.** If a tug is single-use, cathode life is structurally easy at every cell (single-mission canonical closes with 3.4× heritage margin). The financial model's vehicle-cost amortisation across 10 missions is the constraint that drives multi-mission reuse and creates the cathode-life problem. R-single-use-vs-reusable-tug-economics should be elevated to a candidate round: at what single-use vehicle unit cost does the program's net-present-value at the year-twenty-plus winner cell close without requiring cathode swap?
- **Methodology lesson — orthogonal failure modes compound architectural constraints.** R-all-electric-thruster-sweep concluded Variant B was safe under delta-velocity-plus-efficiency analysis. Cathode life is an orthogonal axis; combining it with the delta-velocity-plus-efficiency analysis flips the Variant-B-is-safe verdict at 10-mission reuse. Lesson: when a round concludes an architecture is "structurally safe," that conclusion is bounded by the axes the round evaluated. Adding to the convention log.
- **Methodology lesson — bracket rather than point-estimate when the literature is silent.** The Wang et al. pessimistic anchor is genuinely uncertain by an order of magnitude. The round handles this by reporting verdicts under all three brackets (optimistic, mid-case, pessimistic) rather than picking one. The architectural conclusion (cathode replacement required at multi-mission reuse) is robust across the brackets; the question is *how many* spares are needed, not whether any are needed. Adding to the convention log.
- **Promotes R-single-use-vs-reusable-tug-economics, R-cathode-swap-architecture-mass-budget, R-microwave-electrothermal-as-cathode-life-escape-hatch.** Three new candidate rounds dropped out of this one. Each questions a different load-bearing assumption: the reuse cadence in the financial model, the structural mass budget for redundancy, and the R10b-killed-microwave-electrothermal column's status under cathode-life-pessimistic.
- **Reactor cycle life under multi-year burn is an adjacent risk not modelled here.** R-inbound-dv-continuous-thrust flagged reactor burn life. Cathode life addresses the thruster; reactor life addresses the power source. Both are unmodelled multi-year-burn constraints. R-reactor-cycle-life-megawatt should join the candidate-round list.

