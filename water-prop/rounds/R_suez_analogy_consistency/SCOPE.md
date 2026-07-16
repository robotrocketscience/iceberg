# R-Suez-analogy-consistency-check — SCOPE

**Author:** rhea (worker session, iceberg-rhea-2 branch).
**Date:** 2026-05-16 (latest+8, eighth round this sitting; queued from R-mean-EV-decomposition priority-1 thread #2).

## Goal

Reconcile (or flag the inconsistency in) the locked anchor-investor framing — belief `76fd04cdba8b2c3b` — which describes ICEBERG's upside as a "Suez-Canal-class business in cislunar water." R15 demonstrated that **the EV-upside case (mean Δ-NPV in favor of upfront fleet) depends entirely on uncapped upper-tail clearing capture** (top-decile clearings $36k+/kg drive the entire -$10.6 B gap). Cap at clearing p79 ($18.6k/kg) flips mean Δ-NPV sign. The historical Suez Canal Authority tariff regime — the analogy's reference point — is sovereign-regulated, not free-market. If the analogy is taken seriously, the implied operating environment IS a cap-regulated regime, which contradicts the EV-upside claim.

This round asks empirically: **does the Suez-Canal toll regime, applied to ICEBERG, imply a clearing-price cap above or below R15's sign-flip threshold of p79 ($18.6 k/kg)?** If above, the locked belief is internally consistent (EV-upside survives Suez-style regulation). If below, the belief contains a contradiction (the analogy implies a regime under which EV-upside vanishes; the pitch is selling free-market upside while invoking sovereign-regulated-infrastructure language).

## What this round does

1. **Empirical: Suez Canal Authority tariff regime.** How is the per-transit toll set? Is it cost-plus, market-cleared, regulated against the Cape of Good Hope alternative, or some hybrid? Historical margins (toll revenue vs operating cost). Recent (2020-2025) rate hikes and the regulatory framework behind them.
2. **Cross-check: Panama Canal Authority.** Independent sovereign canal-toll regime; comparable structural question.
3. **Cross-check: US LNG-export tariff regulation (DOE / FERC).** A more direct economic analog (commodity export from sovereign jurisdiction with market-implied clearing price + regulated-margin oversight). What is the regulated-margin or windfall-tax structure?
4. **Compute the implied clearing-price-cap percentile** that Suez-style regulation would impose on ICEBERG. Anchor: Suez transit-cost vs Cape-route alternative differential as the "marginal-alternative" anchor for cislunar water vs Earth-launch-equivalent.
5. **Reconcile with R15.** Three possible outcomes:
   - **(A) Suez-implied cap > p79:** EV-upside survives under Suez-style regulation. Locked belief consistent. R15's matrix-amendment three-regime framing should foreground regime (1) "unregulated or weakly-capped clearing."
   - **(B) Suez-implied cap in [p70, p79]:** EV-flat-or-modestly-negative under Suez-style regulation. Locked belief is borderline; the "Suez-class business" framing supports the SCALE claim but not the EV-upside claim. R15 matrix-amendment three-regime framing should foreground regime (2) "mild cap, EV break-even."
   - **(C) Suez-implied cap < p70:** EV-positive for staged commitment under Suez-style regulation. Locked belief contains a direct contradiction — the analogy implies the regulatory regime where the EV-upside case fails. R15 matrix-amendment three-regime framing should foreground regime (3) "public-utility cap, staged wins on EV."
6. **Belief-revision recommendation.** Three sub-recommendations contingent on the reconciliation:
   - If (A): annotate locked belief; keep framing.
   - If (B): annotate locked belief; clarify "Suez-Canal-class" is scale-only, not pricing-regime.
   - If (C): flag locked belief as containing a contradiction; propose new framing language.

## What this round does NOT do

- Does NOT propose specific cislunar regulatory language. Treaty / policy work is out of scope; only the *implication* of the historical analogy for the matrix economic comparison is in scope.
- Does NOT introduce new economic variables (no new MC, no new physics). R15's cap-sweep numbers are the load-bearing comparator; this round translates Suez-empirical-margins into a cap-percentile and compares.
- Does NOT speculate about future cislunar resource clearing prices. The clearing-price distribution is inherited from R-LEO-water-demand-curve (Starship × markup lognormal); only the cap point in that distribution is the question.
- Does NOT make a normative recommendation about whether ICEBERG SHOULD operate as a Suez-style regulated entity. This round is a consistency check on the existing pitch's stated framing.
- Does NOT touch shared docs. Output is one round dir + commit + handoff.

## Why now

R15 promoted "R-Suez-canal-analogy-consistency-check" to priority-1. The locked anchor-investor belief (~quote-block prepared for the anchor investor) was inserted into the planning record by the project owner and is currently load-bearing for the pitch's capital-framing narrative. R15 demonstrated the belief's EV-upside-and-Suez-analogy bundle is potentially internally inconsistent. Before the orchestrator integrates R14 + R15 matrix-axis-17 amendments, the orchestrator (and project owner) need a structured answer to: *can the belief stay as written, or does it require annotation/revision?*

This is also a Bayesian-prior check on whether the cap-regulated regime (R15's headline) is the policy-default for ICEBERG. The Suez analogy is the pitch's OWN reference framework. If the pitch invokes a sovereign-regulated infrastructure analogy as its scale anchor, the cap-regulated regime is what the pitch is implicitly assuming whether or not it says so explicitly.

## Methodology lessons inherited

- **#7-v5** convex-hull check on distribution-aware BOE (this round is not distribution-integrated; lesson does not apply directly).
- **#11** grade SCOPE against primary input data (applied below; primary input is web research on Suez/Panama/LNG, plus R15 results).
- **#17 (R15, new)** sign-mixed distribution decomposition (not applicable here; this round is qualitative-empirical with quantitative anchoring).
- **#16 (R14)** scale-invariant ratio metrics caveat (applicable: margin-ratio vs absolute-margin distinction — be careful about reporting "Suez margin = X%" vs "Suez margin per transit = $Y").

## Primary input grading

| Input | Source | Status | Notes |
|---|---|---|---|
| R15 cap-sweep results | `R_mean_EV_decomposition/results/mean_ev_decomposition_summary.json` | exists | provides the sign-flip percentile p79 ($18.6k/kg) |
| R15 vigintile decomposition | same | exists | provides sign-inflection at p60-p65 ($8.5k/kg) |
| Demand-curve clearing distribution | inherited from R-LEO-water-demand-curve | exists | clearing $/kg p05/p50/p95 = 429 / 5,240 / 62,707 |
| Locked anchor-investor belief text | belief `76fd04cdba8b2c3b` | locked | will quote verbatim in §"The claim under test" |
| Suez Canal Authority tariff history | external; web research | needed | NEXT STEP |
| Panama Canal Authority tariff history | external; web research | needed | cross-check |
| US LNG-export DOE/FERC regulation | external; web research | needed | cross-check |
| Cape of Good Hope shipping cost (alternative-route anchor) | external; web research | needed | for Suez-margin calibration |
| Cislunar marginal cost (Starship $/kg) | inherited from clearing-price MC | already in distribution | used as ICEBERG's "marginal-alternative" anchor |

## Pre-registered hypotheses

Outcome question: where does Suez-style regulation imply the ICEBERG clearing-price cap sits relative to R15's sign-flip threshold of p79 ($18.6 k/kg)?

| ID | Predicted | Falsification |
|---|---|---|
| **H1** Suez Canal Authority tariff is sovereign-regulated, not free-market. Empirical evidence: published tariff schedule, periodic adjustments by SCA decree, public consultation requirements. | Empirical evidence shows free-market clearing with no sovereign tariff oversight. |
| **H2** The Suez "margin" — toll revenue per transit divided by the cost differential between Suez and Cape of Good Hope routes — is bounded historically at **20-50% of the cost differential** (the alternative-route savings the shipper realizes; sovereign captures a *fraction* of the savings, not all). | Margin > 50% (rapacious) or < 10% (cost-plus only). |
| **H3** The Panama Canal Authority operates a similar regulated-tariff regime; published toll schedules; tariff oversight by Panamanian government. | Panama operates a free-market clearing or otherwise diverges structurally from Suez. |
| **H4** US LNG-export prices are NOT capped by FERC/DOE in the spot market; the regulated component is the export-authorization licensing, not the clearing price. The LNG-export precedent says: **commodity export prices float at market clearing; the sovereign regulates licensing and capacity, not price.** | US LNG-export prices are price-capped by FERC. |
| **H5 (load-bearing reconciliation)** Applying Suez-margin-fraction (H2: 20-50% of marginal-alternative savings) to ICEBERG: the implied clearing-price cap sits at the **p50-p70 of the R15 distribution ($5k - $12k per kg)**, which is BELOW R15's sign-flip threshold of p79. *Outcome (C): the analogy implies a regime under which staged commitment wins on EV.* | Cap above p79 (outcome A) or cap in [p70, p79] (outcome B). |

## Cross-checks

| ID | Check | Tolerance |
|---|---|---|
| XC-1 | Suez tariff regime is regulated, not market-cleared (per H1 finding) | qualitative |
| XC-2 | Panama tariff regime is structurally similar to Suez (per H3 finding) | qualitative |
| XC-3 | R15 sign-flip threshold ($18.6k/kg at p79) replicates in this round's reference table | exact identity from R15 JSON |
| XC-4 | Demand-curve p70 clearing ≈ $11.6k/kg per R15 JSON | exact identity |
| XC-5 | At least 3 independent web sources confirm Suez SCA-regulated tariff structure | citation count ≥ 3 |

## Method

1. Web research, Suez Canal Authority tariff history (last 50 years; particular focus on post-2015 rate adjustments).
2. Web research, Panama Canal Authority structural comparator.
3. Web research, US LNG-export DOE/FERC regulatory structure.
4. Compute Suez margin-fraction = toll revenue per transit / (Cape route cost - Suez route cost). Anchor on 2022-2024 reported toll revenues and route cost differentials.
5. Apply margin-fraction to ICEBERG's analogous quantities: marginal cost = Starship $/kg launch (the "Cape route" of cislunar water — bring it up from Earth); savings = clearing $/kg - marginal cost. Implied cap = marginal cost + margin-fraction × savings.
6. Compare implied cap to R15's sign-flip threshold (p79 = $18.6k/kg). Report (A) / (B) / (C) outcome.
7. Belief-revision recommendation per outcome.
8. Commit; write handoff; refresh STATE.md.

## Estimated runtime

15-25 minutes including web research. No new computation, mostly synthesis.

## Files produced

- `SCOPE.md` (this file)
- `STUDY.md` — research findings + reconciliation table + belief-revision recommendation.
- `results/suez_analogy_summary.json` — quantitative anchor table.
- One commit on iceberg-rhea-2 with `exp:` prefix.
- One handoff under `~/.claude/handoffs/iceberg-rhea-20260516-suez-analogy-consistency.md`.

No shared-doc edits.
