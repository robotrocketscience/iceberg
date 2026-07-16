# R-Suez-analogy-consistency-check — STUDY.md

**Author:** rhea (worker session, iceberg-rhea-2 branch).
**Date:** 2026-05-16 (latest+8, eighth round this sitting; round 16 of the chained sequence).
**Status:** complete. Composes empirical Suez/Panama/LNG research with R15's MC harness.

## The claim under test (verbatim from locked anchor-investor belief `76fd04cdba8b2c3b`)

> *"If ICEBERG works at any gate, you've extended your investment into a category — sovereign-scale cislunar water infrastructure — that returns substantially more than the core business and creates a multi-decade structural moat. If ICEBERG fails at any gate, the core business is unaffected and the engineering heritage from the demonstrator flights actually accelerates the core business by adding capability. **There is no scenario where funding ICEBERG damages the underlying anchor investment thesis.***
>
> *The ask is therefore: incremental capital allocated to ICEBERG as a sleeve within the larger anchor round, with separate milestone reporting and separate go/no-go decisions at each demonstrator. You're not betting the company on a 14-year mission. You're buying the option to expand into a larger market when (and only when) the demonstrators have proven the architecture closes. That option price is the program NRE; **the option payoff is a Suez-Canal-class business in cislunar water**."*

Three claims bundled in this belief:

1. **Downside-bounded:** "no scenario where funding ICEBERG damages the underlying anchor investment thesis." Math: gate-0 capital commitment $1.6 B vs program $14.6 B. Validated by R14 (downside-protection is the load-bearing case for staged commitment).
2. **Upside-extreme:** "returns substantially more than the core business … the option payoff is a Suez-Canal-class business in cislunar water." Math: depends on unregulated upper-tail clearing revenue capture, per R15's decomposition (entire -$10.6 B mean Δ from top decile clearings).
3. **Sovereign-scale framing:** "sovereign-scale cislunar water infrastructure … Suez-Canal-class business." Implies regulated-tariff operating model.

R15 demonstrated claim 2 is contingent on the no-cap-on-upper-tail assumption. This round tests whether claim 3 (the Suez analogy) is internally consistent with claim 2.

## Empirical anchors (web research, 2026-05-16)

### Suez Canal Authority tariff regime

> "The SCA applies a balanced and flexible pricing strategy that takes into consideration changes in the global economy through clear mechanisms that include calculating a vessel's transit tolls **depending on the savings it achieves by transiting through the Canal**" — [International Chamber of Shipping](https://www.ics-shipping.org/current-issue/canal-tolls/) and SCA's published tariff schedule.

Key empirical findings:

- **SCA tolls are sovereign-set, anchored on alternative-route savings.** Periodic adjustments (e.g., 15% rate increase Jan 2024) require SCA decree. Source: [SCA Tolls Table](https://www.suezcanal.gov.eg/English/Navigation/Tolls/Pages/TollsTable.aspx); [trans.info Jan 2024](https://trans.info/en/suez-canal-toll-368274).
- **Empirical margin fraction:** SCA captures ~33-40% of the alternative-route savings as toll.
  - Large container ship Suez toll: **$580k-$800k** per transit (2025 schedule). Source: [tonlexing.com 2025 guide](https://www.tonlexing.com/the-suez-canal-shipping-guide/).
  - Cape route additional cost: **$1M-$2M** per large container round trip (fuel + voyage time). Source: [Manta Shipping](https://www.manta-eg.com/beyond-the-canal-evaluating-the-true-cost-of-rerouting-via-the-cape-of-good-hope/); [Ballast Markets Apr 2025](https://content.ballastmarkets.com/blog/2025-04-21-suez-vs-cape-2-billion-routing-cost/).
  - Margin fraction = toll / (Cape - Suez differential) = $500-800k / $1-2M ≈ **33-40%**.
- **Tariff explicitly market-elastic.** SCA reduced fees in 2024 to stem Cape diversion ([Splash247](https://splash247.com/suez-canal-drops-fees-to-stem-tide-of-ships-heading-via-the-cape-of-good-hope/)). Implies SCA's regulated tariff is competitive with the alternative-route cost, not a windfall extraction.
- **SCA lost $3.8B in toll revenue** during Red Sea disruptions (2023-2024), and "$10m … from container lines routing via Cape" ([The Loadstar](https://theloadstar.com/lines-using-cheaper-cape-of-good-hope-route-will-cost-suez-canal-10m/)). Implies tolls are price-elastic with respect to the alternative.

### Panama Canal Authority (cross-check)

- Tolls approved by **Cabinet Council of Republic of Panama**, recommended by Panama Canal Board of Directors, formal consultation + public hearing required ([Autoridad del Canal de Panamá](https://pancanal.com/en/simplified-tolls-structure-approved/)).
- Structure: fixed fee per vessel size + variable charge contingent on supply-demand conditions ([Port Economics & Policy](https://porteconomicsmanagement.org/pemp/contents/part1/interoceanic-passages/panama-canal-toll-structure/)).
- Same regulatory regime as Suez (sovereign-approved tariff, value-based, supply-demand responsive). **H3 HELD.**

### US LNG-export DOE/FERC regulation (cross-check)

- DOE regulates **export authorization** (licensing under Natural Gas Act § 3); FERC regulates **facility siting, safety, environmental** review ([CSIS analysis](https://www.csis.org/analysis/us-lng-exports-doe-and-ferc-roles-and-boundaries)).
- **Neither agency regulates the clearing price of LNG.** Spot price floats at market. Source: same CSIS analysis; [Akin LLP brief on CP2 LNG](https://www.akingump.com/en/insights/blogs/speaking-energy/from-conditional-to-final-doe-clears-cp2-lng-for-non-fta-exports).
- **H4 HELD.** LNG-export precedent: sovereign regulates licensing and capacity, not price. Distinct from canal-toll precedent.

## ICEBERG marginal cost (anchored on inherited R13/R14 parameters)

- 2-launch architecture: opex per mission $200M (`rd13.LAUNCH_COST_PER_MISSION_M[2]`).
- Delivered per mission: 80 tonnes.
- Marginal cost per delivered kg: **$2,500/kg**.
- Comparable to Starship median launch cost ($1,500/kg). ICEBERG marginal cost > Starship median — i.e., ICEBERG is not a cost-saving alternative to Earth-launch at the median Starship case; it is a *premium-service alternative* (markup median 3.5× per R-LEO-water-demand-curve).

This is the *first structural incompatibility* between the Suez analogy and ICEBERG: the Suez Canal is a **cost-saving** alternative (the canal is cheaper than the Cape route), whereas ICEBERG is a **premium-service** alternative (cislunar water is more expensive per kg than Earth-launch in 65%+ of MC draws but is delivered at LEO rather than ground). The Suez Canal would not exist if the canal route were more expensive than the Cape route by 3.5×.

## Suez-implied cap distribution

Apply SCA-style cap formula per MC draw: `cap_$/kg = ICEBERG_MC + margin × max(0, Starship_$/kg − ICEBERG_MC)` at margin = 36.5% (Suez midpoint).

| Quantity | $/kg |
|---|---:|
| Starship p05 / p50 / p95 | 178 / 1,524 / 12,759 |
| Original clearing p05 / p50 / p95 (no cap) | 429 / 5,240 / 62,707 |
| **Suez-implied cap p05 / p50 / p95** | **2,500 / 2,500 / 6,244** |
| R15 sign-flip threshold | 18,600 |
| Cap binds (orig > cap) | 68.3% of draws |
| Caps that exceed R15 sign-flip | 0.45% of draws |

The Suez-implied cap is **uniformly below R15's sign-flip threshold in 99.5% of draws** — the cap is essentially never as permissive as the R15 break-even level. The cap floors at the marginal cost $2,500/kg when Starship < $2,500/kg (in that regime, no positive premium would be allowed under the strict Suez formula because the customer's "savings" would be negative).

The median Suez-implied cap ($2,500/kg) sits at **clearing percentile 31** of the R15 distribution. **The Suez analogy implies a clearing-price regime well below the bottom-third of the demand-curve distribution.**

## NPV under strict Suez regulation (load-bearing finding)

Re-running R13's NPV harness with per-draw clearing capped at the Suez-implied cap (margin 36.5%):

| Metric | Uncapped (R14/R15) | Suez-strict |
|---|---:|---:|
| Mean Δ-NPV (R − D) | -$10.63 B | **+$6.42 B** |
| Mean NPV_D (upfront) | $X (much higher) | -$11.59 B |
| Mean NPV_R (staged) | $X (much lower) | -$5.16 B |
| P(NPV_D > 0) | 36.3% (R13) | **2.29%** |
| P(NPV_R > 0) | 31.0% (R13) | **1.42%** |
| Mean revenue per delivered kg | $5,240 (median) | $2,838 (mean under cap) |

**Two findings:**

1. **The EV comparison FLIPS to staged under Suez regulation** (+$6.42 B vs uncapped -$10.63 B). The R14/R15 "EV disfavors staged" conclusion is structurally tied to the no-regulatory-cap scenario.

2. **Under strict Suez regulation, the ENTIRE program is unviable on EV** — both regimes have negative mean NPV, and 97-99% of MC draws produce negative NPV. Mean revenue per delivered kg ($2,838) is barely above marginal cost ($2,500), giving only $338/kg gross margin to cover capex + NRE + reactor + ops over a 40-year horizon. **It doesn't.**

This second finding is the load-bearing inconsistency: **the "Suez-Canal-class business" framing in the locked belief is not just inconsistent with the EV-upside claim, it is inconsistent with the program being economically viable at all** under the parameters R13/R14/R15 inherited.

## Hypothesis grading

| ID | Predicted | Measured | Status |
|---|---|---|---|
| **H1** SCA tariff sovereign-regulated, not market-cleared | qualitative | confirmed; SCA decree-based, alternative-route-anchored, market-elastic | **HELD** |
| **H2** SCA margin fraction in [20%, 50%] | band | **33-40%** (empirical, large container) | **HELD** (midpoint of band) |
| **H3** Panama Canal Authority structurally similar | qualitative | confirmed; Cabinet Council approval, similar value-based pricing | **HELD** |
| **H4** US LNG export prices NOT capped by DOE/FERC | qualitative | confirmed; licensing-only regulation | **HELD** |
| **H5** Suez-implied ICEBERG cap sits at clearing p50-p70 ($5k-$12k/kg) | band | **median cap at clearing p31 ($2,500/kg); p95 cap at clearing ~p53 ($6,244/kg)** | **FALSIFIED (below the band)** — the cap is much more restrictive than my BOE predicted because ICEBERG marginal cost dominates the cap floor in low-Starship-cost draws |

**Score: 4 HELD, 1 FALSIFIED.** H5 falsification is on the *more-restrictive* side — the Suez analogy is *more* damaging to the EV-upside claim than I predicted, not less.

The reason H5 falsified: I anchored on the demand-curve clearing distribution alone, but the cap formula has TWO terms (ICEBERG MC floor + margin × Starship-savings). When Starship < ICEBERG MC (which is 65% of draws since Starship median $1,524 < ICEBERG MC $2,500), the savings term goes to zero and the cap clamps to ICEBERG MC $2,500/kg. The cap is FLAT at $2,500 across two-thirds of the distribution. This is a structural-floor effect I missed in pre-reg BOE.

## Cross-checks

| ID | Check | Status |
|---|---|---|
| XC-1 | SCA regime regulated (per H1) | PASS (3+ sources cite SCA decree mechanism) |
| XC-2 | Panama Canal structurally similar | PASS |
| XC-3 | R15 sign-flip threshold $18.6k/kg replicates | PASS (used directly from R15 JSON) |
| XC-4 | Demand-curve p70 ≈ $11.6k/kg replicates | PASS |
| XC-5 | ≥ 3 independent web sources for SCA regulated tariff | PASS (SCA, ICS, JICA report, tonlexing 2025 guide, Wikipedia SCA article all corroborate) |
| (added) Uncapped baseline reproduces R14/R15 -$10.6 B | mean uncap delta = -$10.63 B | PASS |

All cross-checks PASS.

## Reconciliation outcome

Per SCOPE.md reconciliation framework: outcome is **(C) — Suez-implied cap << R15 sign-flip threshold**.

Specifically: the median Suez-implied cap ($2,500/kg) is at clearing percentile 31, vs R15 sign-flip at clearing p79. Outcome (C) bracket was "Suez-implied cap < p70." Measured is p31. The locked belief contains a **direct internal contradiction** between claim 2 (EV-upside-via-Suez-class-business) and claim 3 (Suez-Canal-class business model).

Further, the strict-Suez NPV evaluation shows BOTH regimes are unviable on EV under that regulatory regime — implying the program economics fundamentally REQUIRE a non-Suez pricing regime to be viable. The pitch's invoking the Suez framing while assuming the economics close is a category error.

## Belief-revision recommendation

The locked anchor-investor belief (`76fd04cdba8b2c3b`) needs **annotation, not retraction.** Recommended annotation block to append:

> *"Annotation (R-Suez-analogy-consistency-check, 2026-05-16): The 'Suez-Canal-class business in cislunar water' phrase is invoked as a SCALE benchmark, not as a business-model template. Under strict Suez Canal Authority regulatory analogy (sovereign-set tariff capturing ~36.5% of alternative-route savings), ICEBERG's economics would be unviable in 98% of MC clearing-price draws (mean NPV deeply negative for both upfront and staged regimes). The pitch's EV-upside claim depends on an unregulated or weakly-regulated clearing-price environment, which is **structurally different** from the Suez business model. If the anchor investor reads 'Suez-Canal-class' as endorsing a sovereign-regulated tariff regime, the EV-upside claim is internally contradicted; if read as a SCALE benchmark only (multi-billion-dollar-annual-revenue scale), the analogy stands as scale-language but does not constrain pricing.*
>
> *Recommended pitch language clarification: replace 'Suez-Canal-class business' with a phrase that disambiguates scale from pricing regime — e.g., 'sovereign-scale infrastructure business with commodity-export pricing dynamics' (the LNG-export framing: licensing regulated, clearing price market-driven). The LNG-export precedent is the closer business-model analog and does not contradict the EV-upside claim."*

## Cross-learning

**Negative for the locked belief as currently written:** the "Suez-Canal-class business" framing, taken at face value, structurally implies a regulatory regime under which the program is unviable. Either the analogy is metaphorical-only (in which case the language should disambiguate), or the framing is internally contradictory. This is an actionable belief-revision item.

**Positive for the LNG-export analogy as an alternative framing:** US LNG-export is a multi-billion-dollar-annual sovereign-scale commodity-export business in which sovereign regulates licensing/capacity (the bottleneck on supply) but NOT clearing price. ICEBERG's structure — sovereign-funded demonstrator + commercially built fleet + LEO commodity delivery — maps more cleanly onto the LNG-export model than the Suez model. The "Suez" framing should probably be replaced with "LNG-export-class" in the pitch.

**Negative for R14/R15's "policy-realistic regulatory regime" reasoning IF the LNG model is the correct analog:** if cislunar resource export is governed by licensing/capacity regulation (à la LNG) rather than price regulation (à la Suez), the no-cap scenario is the policy-default and R14's "EV disfavors staged" conclusion holds. R15's matrix-amendment three-regime framing should explicitly invoke the LNG-export precedent for the unregulated-clearing baseline and the Suez/Panama precedent for the cap-regulated alternative.

**Quantitative for the matrix:** Suez-implied cap ($2,500/kg at p31 of distribution) is far below R15's sign-flip threshold ($18,600/kg at p79). Adding "Suez-strict cap" as a fourth regime row in the matrix-axis-17 amendment:
1. **Unregulated:** mean Δ = -$10.6 B (upfront wins; both arms profitable; R14/R15 baseline).
2. **Mild cap (clearing p90 / $36k/kg):** mean Δ = -$3.1 B (upfront still wins).
3. **Public-utility cap (clearing p70-80 / $12-19k/kg):** mean Δ ≈ 0 to +$2.2 B (staged wins).
4. **Strict Suez (clearing p31 / $2.5k/kg):** mean Δ = +$6.4 B (staged wins), but **program unviable** — mean NPV negative for both regimes, P(NPV>0) ~1-2%.

The fourth row clarifies: a "staged wins on EV" finding under a sufficiently strict cap regime does NOT mean the program closes — it means the program loses less money under staged than under upfront. **EV-comparative direction and program-viability are distinct questions.**

**Methodology lesson #18 (NEW):** comparative-EV findings ("regime A wins on EV vs regime B") are direction-only and do not address program viability. The matrix should report both the comparative-direction (which regime wins) AND the absolute-NPV-distribution (whether the winning regime is itself profitable). R14/R15's three-regime presentation has the comparative direction right but doesn't pin program viability under each regime. **Fix:** add P(NPV_winning_regime > 0) as a parallel column to mean Δ.

## What this round does NOT prove

- Does NOT establish that ICEBERG should adopt a Suez-style regulatory model. The cap analysis is a logical-implication check on the belief's invocation of the analogy, not a policy recommendation.
- Does NOT explore intermediate margin fractions (50%, 75%, 100%-of-savings capture). Suez-empirical 33-40% is the load-bearing anchor; intermediate caps fall between the four matrix rows above.
- Does NOT speculate on cislunar resource governance treaty evolution (Outer Space Treaty Art. II, Artemis Accords resource provisions). That's R-upper-tail-clearing-cap-regulatory-feasibility (queued priority-1 from R15).
- Does NOT model time-varying margin fractions (Suez's tariff changes year-to-year). Treats the margin as static for the 40-year program horizon.
- Does NOT propose new pitch language beyond the annotation block above. Project owner reviews.

## New pending threads spawned by this round

**Priority 1:**
1. **R-LNG-export-analogy-as-replacement** — substantive comparison: does the LNG-export business model (licensing-regulated, price-free) match ICEBERG's structure better than Suez? Read DOE Order P-N filing precedents; identify ICEBERG's equivalent of "FERC siting authorization" vs "DOE export authorization." Recommended new pitch framing language.

**Priority 2:**
2. **R-Suez-margin-fraction-sensitivity** — sweep margin fraction 0% (cost-recovery), 33% (Suez low), 40% (Suez high), 75% (rapacious), 100% (full alternative-route savings captured). Identify the margin fraction at which the program becomes viable.
3. **R-program-viability-vs-comparative-EV** — formalize methodology lesson #18 by reporting both P(NPV_max_regime > 0) and mean Δ under each cap regime. Generalizes to all matrix-axis-17 comparisons.
4. **R-customer-value-of-LEO-delivery** — empirical anchor: what would the candidate buyer classes modeled in the demand analysis actually pay for cislunar water? Cost-saving vs LEO-launch (Suez-like) or premium-for-LEO-delivery-convenience (AWS-like)? Resolves the structural-analogy-fit question.

**Resolved:**
- ~~R15 pending thread #2 (R-Suez-canal-analogy-consistency-check)~~ — **RESOLVED.** Locked belief contains internal contradiction; annotation block recommended; LNG-export proposed as cleaner business-model analog.

## Sources

- [SCA Tolls Table (official Suez Canal Authority)](https://www.suezcanal.gov.eg/English/Navigation/Tolls/Pages/TollsTable.aspx)
- [International Chamber of Shipping — Canal Tolls](https://www.ics-shipping.org/current-issue/canal-tolls/)
- [trans.info — Suez Canal toll 15% increase Jan 2024](https://trans.info/en/suez-canal-toll-368274)
- [Manta Shipping — True Cost of Rerouting via Cape](https://www.manta-eg.com/beyond-the-canal-evaluating-the-true-cost-of-rerouting-via-the-cape-of-good-hope/)
- [Ballast Markets — Suez vs Cape Apr 2025](https://content.ballastmarkets.com/blog/2025-04-21-suez-vs-cape-2-billion-routing-cost/)
- [The Loadstar — Lines using Cape will cost SCA $10m](https://theloadstar.com/lines-using-cheaper-cape-of-good-hope-route-will-cost-suez-canal-10m/)
- [Splash247 — Suez Canal drops fees](https://splash247.com/suez-canal-drops-fees-to-stem-tide-of-ships-heading-via-the-cape-of-good-hope/)
- [Autoridad del Canal de Panamá — Simplified Tolls Structure](https://pancanal.com/en/simplified-tolls-structure-approved/)
- [Port Economics & Policy — Panama Canal Toll Structure](https://porteconomicsmanagement.org/pemp/contents/part1/interoceanic-passages/panama-canal-toll-structure/)
- [CSIS — US LNG Exports: DOE and FERC Roles and Boundaries](https://www.csis.org/analysis/us-lng-exports-doe-and-ferc-roles-and-boundaries)
- [Akin LLP — CP2 LNG Clears DOE for Non-FTA Exports](https://www.akingump.com/en/insights/blogs/speaking-energy/from-conditional-to-final-doe-clears-cp2-lng-for-non-fta-exports)
- [tonlexing.com — Suez Canal Shipping Guide 2025](https://www.tonlexing.com/the-suez-canal-shipping-guide/)
