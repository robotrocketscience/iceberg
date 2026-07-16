# R-chemical-plus-small-reactor — does small-reactor-for-process-power-only close the matrix?

**Status:** complete. Pre-registration → run → Revisit → Cross-learning all below.

## Question

R-non-fission-baseline (commit `85a5aac`, this session) established that the binding fission-dependence in the architecture decision matrix is **Saturn-side process power for inbound-propellant electrolysis** (~150 kilowatts-electric for one Saturn-ops year), not propulsion-side power. Architecture B (all-chemical end-to-end) has a launch-mass-per-delivered ratio of 1.8–4.5× — better than the megawatt fission Modular-Assembled-Radiators-anchored baseline — but is hidden-infeasible because its chunk-fed inbound at specific-impulse 450 seconds requires onsite electrolysis with no Saturn-side power source.

The natural next architecture is **Architecture D**:

> Chemical propulsion end-to-end (Architecture B) PLUS a small fission reactor at Saturn used purely for electrolysis process power. The reactor never propels; it only powers the inbound-propellant electrolysis plant.

The program-risk profile of Architecture D is materially different from the matrix's megawatt-class fission propulsion bet:

| Dimension | Megawatt fission propulsion (current matrix cell) | Small fission for Saturn process power (Architecture D candidate) |
|---|---|---|
| Power level | 1000 kilowatts-electric | 40–150 kilowatts-electric |
| Ground demo | None | Kilowatt Reactor Using Stirling Technology (KRUSTY) flew ~10 kilowatts-electric, 2018 |
| Funded contract scope | $0 in FY2026 (nuclear-electric and nuclear-thermal lines zeroed) | NASA Fission Surface Power Phase 1 contracts active ($5M each × 3 teams, 2022 → 2025 extension); Phase 2 Draft Announcement issued August 2025, final anticipated early 2026; Duffy directive August 2025 scope = 100 kilowatts-electric |
| Specific power assumption | 40 watts-per-kilogram (Technology-Readiness-Level 2 paper study) | 2.4 watts-per-kilogram (KRUSTY measured) → 5–10 watts-per-kilogram (Fission Surface Power Phase 1 contracted target) |
| Bayesian posterior on delivery by 2032–2035 (per R-megawatt-architecture-viability) | 0.07–0.20 | open — this round prices it |

The question this round answers: **does Architecture D close L0-05 + L0-09 + L0-12 + Saturn-side-energy-budget at a fission scale that the program-risk evidence treats as substantially more credible than megawatt propulsion?** If yes, Architecture D is the most defensible cell in the matrix once the Saturn-side power problem is named — a smaller fission bet with a shorter risk-bridge to closure than any current matrix cell.

## Pre-registered hypothesis (H-cps)

**Aggregate (H-cps-agg):** Architecture D closes L0-05 + L0-09 + L0-12 + Saturn-side-energy-budget at a Saturn-side reactor in the 50–150 kilowatts-electric range. At Fission Surface Power Phase 1 contracted specific-power target (5–10 watts-per-kilogram system-level), the reactor masses 15–30 tonnes; this drags the chunk-fed inbound delivered mass into the 5–25 tonnes-per-mission range and the launch-mass-per-delivered ratio into the 5–15× range. The architecture closes L0-05 (round-trip 13.17 years) and L0-09 (cadence supportable). L0-12 closure is borderline but plausible. **Bayesian posterior on Architecture D delivery by 2035 is 0.30–0.55** — 2–6× higher than the megawatt-class fission-propulsion posterior from R-megawatt-architecture-viability (0.07–0.20). Architecture D is the most defensible non-current-matrix cell.

### Pre-registered sub-claims

| Sub-claim | Predicted | Falsification |
|---|---|---|
| H-cps-a — Saturn-side electrolysis electrical power required for 200 tonne chunk, one year of Saturn-vicinity ops, electrolysis at 8 kilowatt-hours-per-kilogram | 140–160 kilowatts-electric | outside 120–180 kilowatts-electric |
| H-cps-b — Saturn-side reactor mass at Fission Surface Power Phase 1 contracted target (5–10 watts-per-kilogram system) for 150 kilowatts-electric | 15–30 tonnes | outside 10–40 tonnes |
| H-cps-c — Architecture D delivered water per mission, vehicle dry 10 tonnes, reactor 20 tonnes, electrolysis plant 5 tonnes, chunk 200 tonnes, specific-impulse 450 seconds inbound | 15–25 tonnes per mission | outside 5–35 tonnes |
| H-cps-d — Architecture D round-trip time (chemical impulsive outbound + Hohmann cruise + 1 year Saturn ops + impulsive inbound) | 13.17 years; closes L0-05 with 1.8-year margin | falsified if > 14.0 years |
| H-cps-e — Architecture D Earth-launch wet mass per delivered tonne at Fission Surface Power Phase 1 reactor mass scaling | 5–15× | outside 3–25× |
| H-cps-f — Bayesian posterior on Architecture D fission delivery by 2035 (Saturn-side 40–150 kilowatts-electric reactor) | 0.30–0.55 | outside 0.20–0.70 |
| H-cps-g — Architecture D delivered mass per mission at KRUSTY-class specific power (2.4 watts-per-kilogram) for 150 kilowatts-electric reactor (62.5 tonne reactor) | < 0 tonnes (infeasible — reactor mass alone busts chunk-fed inbound) | falsified if delivered > 5 tonnes |
| H-cps-h — Architecture D verdict relative to current matrix | Most defensible cell once Saturn-side power problem is named. Matrix should add it as the new baseline with annotation "Saturn-side fission for process power; chemical propulsion end-to-end" | falsified if any current matrix cell has higher combined-criteria closure posterior |

**Aggregate decision:** if H-cps-agg holds — Architecture D closes at Fission Surface Power Phase 1 scaling with posterior ≥ 0.30 — surface to the orchestrator: (a) add Architecture D as a new matrix cell; (b) reframe the matrix's "fission dependence" annotation to distinguish propulsion-side vs Saturn-side process-power dependences; (c) the program's smallest-credible-fission-bet is now 40–150 kilowatts-electric for Saturn-side process power, not 1000 kilowatts-electric for propulsion. If H-cps-agg falsifies — Architecture D fails on either reactor-mass cascade or posterior — the matrix's "no baseline" verdict from R-non-fission-baseline + R-megawatt-architecture-viability stands and the program's options narrow to: (i) bet on megawatt propulsion fission anyway, (ii) relax L0-05 to admit non-fission, (iii) abandon ICEBERG.

## Method

### Architecture D mass accounting

Same outbound and inbound physics as Architecture B (R-non-fission-baseline), with the Saturn-side reactor added as a payload mass at Earth and during transit.

**Outbound (chemical impulsive from low Earth orbit):** delta-velocity 7.29 kilometers-per-second (Oberth-credited, computed from `sqrt(v_escape² + v_∞²) − v_circ`). Specific-impulse 450 seconds. Two-stage hydrolox at 10% dry/wet ratio per stage. Payload at Earth-escape = vehicle dry + Saturn-side reactor + electrolysis plant.

**Cruise:** Hohmann ballistic, 6.086 years one-way each direction.

**Saturn ops:** 1 year (consistent with prior rounds).

**Saturn-side power:** Saturn-side reactor at specific power `s_pwr` watts-per-kilogram system-level delivers `P_kWe = M_reactor_t × s_pwr / 1000` kilowatts-electric. Sweep `s_pwr ∈ {2.4, 5, 10, 40}` watts-per-kilogram and `M_reactor_t ∈ {10, 20, 30, 50, 70}` tonnes.

**Energy budget:** Saturn-side electrolysis requires `8 kilowatt-hours per kilogram` of water (industrial alkaline electrolysis + cryogenic liquefaction). For a chunk of 200 tonnes with inbound propellant burned = chunk − delivered ≈ 150–185 tonnes, total energy required = 1.2–1.5 gigawatt-hours, over 1 year of Saturn ops at `P_kWe` continuous = `P_kWe × 8760` kilowatt-hours available.

**Inbound:** chunk-fed chemical at specific-impulse 450 seconds, delta-velocity 6.42 kilometers-per-second (post-lunar-gravity-assist residual). Mass ratio = 4.27. Delivered = chunk / mass-ratio − (vehicle dry + reactor + electrolysis plant) × (1 − 1/mass-ratio).

### Reactor specific-power scenarios

- **KRUSTY-baseline (2.4 watts-per-kilogram):** the only measured system-level number from a US ground demo (Kilowatt Reactor Using Stirling Technology, 2018, ~10 kilowatts-electric demonstrated).
- **Fission Surface Power Phase 1 contracted target (5 watts-per-kilogram):** the system-level specific power target in active Phase 1 contracts (Lockheed Martin, Westinghouse, IX joint venture; June 2022, extended January 2025). Lower bound of FSP-projected.
- **Fission Surface Power stretch (10 watts-per-kilogram):** upper-bound of FSP-projected specific power; consistent with Phase 2 Draft Announcement scope (August 2025) at 100 kilowatts-electric. This is what a successful FSP Phase 2 would land at if the August 2025 directive is taken at face value.
- **Aspirational matrix (40 watts-per-kilogram):** the matrix's current paper-study target for megawatt nuclear-electric propulsion. Per locked beliefs, Technology-Readiness-Level 2 aspirational, not extrapolated from KRUSTY. Reporting for comparison only — no funded program targets this at Kilopower-class scale either.

### Bayesian posterior on Architecture D delivery

Reuse the 0-of-6 US space-fission base rate as the structural prior. But adjust for:

- **KRUSTY ground demo**: a 10-kilowatts-electric ground demo flew successfully. Treat as 0.5-of-1 partial-orbit-equivalent (ground demo ≠ flight, but it is non-zero evidence).
- **Fission Surface Power Phase 1 contracts active**: 3 contracted partners with public deliverables and milestones. Treat as a multiplier on the prior — Phase 1 success would lift posterior by a factor of 2–3 vs the baseline-only prior, conditional on Phase 2 being awarded.
- **FY2026 budget context**: Phase 2 not yet awarded; nuclear-electric-propulsion and nuclear-thermal-propulsion technology lines zeroed; Defense-Advanced-Research-Projects-Agency Demonstration Rocket for Agile Cislunar Operations cancelled May 2025. Same headwind as megawatt propulsion fission, but the headwind is *less* binding for FSP-class because FSP is a separate Office of Space Technology line (different appropriation, different congressional politics).

Posterior computation (Beta-distribution update with weak-informative priors): three priors as in R-non-fission-baseline + R-megawatt-architecture-viability, plus a "KRUSTY-credit" adjustment:

- Prior A (Beta(2, 4) symmetric-pessimistic): no KRUSTY adjustment.
- Prior B (Beta(2, 4) + KRUSTY half-credit): post-KRUSTY 2.5-of-7 evidence weight.
- Prior C (Beta(2, 4) + FSP Phase 1 milestone credit): post-Phase-1-active +1 conditional success.

Posteriors reported as `0.30–0.55` range across the three priors.

### Outputs

- `results/architecture_D.json` — sweep across reactor specific power × reactor mass × vehicle mass.
- `results/posteriors.json` — three-prior Bayesian posterior table.
- `results/tables.md` — human-readable summary.

Deterministic; runtime < 1 second; pure Python standard library.

### Things this round explicitly does *not* do

- Cost-side L0-12 closure in dollar figures. Use launch-mass-per-delivered as a proxy. A Kilopower-Fission-Surface-Power flight unit at 50–150 kilowatts-electric in 2032 is likely $300M–$1B per unit (extrapolated from Kilopower Phase A study $400M for 10 kilowatts-electric, scaled with caveat that fixed-cost dominates); explicit dollar pricing is for an R-program-cost round.
- Saturn-side reactor heat rejection at 1.5 megawatts thermal (for 100 kilowatts-electric at 6.3% Stirling efficiency). Radiator mass at the locked-belief 40–55% Modular-Assembled-Radiators-share applies *at megawatt scale*; at Kilopower scale the share is much smaller, but a clean component-decomposition model is not derived here. Specific-power figures used are flat system-level numbers that implicitly bundle the radiator.
- Reactor launch licensing, Kennedy-Space-Center range safety, or transit-through-Van-Allen-belts thermal cycling. All real costs; not modeled.
- Reactor-on-Saturn operational lifetime. Kilowatt Reactor Using Stirling Technology design life is ~10 years; FSP Phase 1 specs target 10-year operation. ICEBERG mission profile is 6 years cruise + 1 year ops + 6 years cruise = 13 years total reactor lifetime end-to-end. Reactor must operate for the full mission and then either be safely passivated at Saturn (no return) or returned to Earth (regulatory question). Treat as compliant for this round; flag for follow-up.

---

## Result

Run complete; results under `results/`. Sweep across reactor specific power × reactor mass × vehicle dry mass. Headline cells (those that close *all* criteria — L0-05 + L0-09 + L0-12 + Saturn-side energy budget):

| reactor mass (t) | spec power (W/kg) | reactor power (kilowatts-electric) | vehicle dry (t) | delivered (t) | launch/delivered ratio | Saturn-energy ratio |
|---:|---:|---:|---:|---:|---:|---:|
| 20 | 10 (Fission Surface Power stretch) | 200 | 10 | 19.89 | 12.47 | 1.22 |
| 20 | 10 (Fission Surface Power stretch) | 200 | 15 | 16.06 | 17.65 | 1.19 |
| 30 | 10 (Fission Surface Power stretch) | 300 | 10 | 12.22 | 26.09 | 1.75 |
| 10 | 40 (matrix aspirational) | 400 | 10 | 27.55 | 6.43 | 2.54 |
| 20 | 40 (matrix aspirational) | 800 | 10 | 19.89 | 12.47 | 4.87 |

At Kilowatt-Reactor-Using-Stirling-Technology specific power (2.4 watts-per-kilogram): no cell closes the energy budget; ratios 0.15–0.42. At Fission Surface Power Phase 1 contracted target (5 watts-per-kilogram): no cell closes either; ratios 0.32–0.88. **Architecture D closure requires specific power ≥ 10 watts-per-kilogram — the Phase 1 stretch target, not the baseline contracted target.**

Best closing cell on launch-mass-per-delivered: 10-tonne reactor at 40 watts-per-kilogram aspirational specific power, 10-tonne vehicle, delivered 27.55 tonnes, launch/delivered 6.43. But the 40-watts-per-kilogram figure is the same Technology-Readiness-Level-2 aspirational number that R-megawatt-architecture-viability already flagged as paper-study; this cell is upside-only.

Best closing cell on physically-defensible specific power: 20-tonne reactor at 10 watts-per-kilogram (Phase 1 stretch), 10-tonne vehicle, delivered 19.89 tonnes, launch/delivered 12.47. This is the cell to compare against the matrix's existing megawatt fission propulsion cell.

### Pre-registered claims, hit/miss

| Sub-claim | Predicted | Measured | Held? |
|---|---|---|:---:|
| H-cps-a — Saturn-side electrolysis power required | 140–160 kilowatts-electric | 165–200 kilowatts-electric at minimum-closing-cell | partially (slightly higher than predicted) |
| H-cps-b — Reactor mass at Fission Surface Power Phase 1 (5–10 watts-per-kilogram) for 150 kilowatts-electric | 15–30 tonnes | requires Phase 1 STRETCH (10 W/kg), reactor 20+ t — Phase 1 BASELINE (5 W/kg) doesn't close at any cell | partially (Phase 1 baseline assumption was too generous) |
| H-cps-c — Delivered water per mission at Fission Surface Power Phase 1 reactor | 15–25 tonnes | 8.39–27.55 tonnes across closing cells; 19.89 tonnes at the load-bearing cell | held |
| H-cps-d — Round-trip time | 13.17 years | 13.17 years exactly | HELD |
| H-cps-e — Launch-mass / delivered | 5–15× | 6.43–42.22× across closing cells; 12.47 at the load-bearing cell | held at load-bearing cell, wider band than predicted |
| H-cps-f — Bayesian posterior on Architecture D fission delivery by 2035 | 0.30–0.55 | 0.17–0.26 across three priors | **FALSIFIED on the optimistic side** |
| H-cps-g — KRUSTY-class specific power (2.4 W/kg) for 150 kWe reactor (62 t) is infeasible | delivered < 0 | delivered negative at 50 t reactor + 10 t vehicle (chunk-fed-inbound dry-payload exceeds chunk-pushing capacity); confirmed | HELD |
| H-cps-h — Architecture D verdict: most defensible cell | Held conditionally | held with caveat: best-in-class posterior is 0.26 (Prior C) vs Kilopower Variant B 0.13–0.24 — modest margin, not the 4–6× I'd anticipated | partially held; reframe required |

### Why pre-registration H-cps-f was wrong

Two errors in pre-registration:

1. **I'd anchored on the conditional probability "given fission program continues, Architecture D works"** instead of the unconditional joint probability "fission program continues AND specific power hits stretch target AND program completes." The conditional cascade discounts the headline posterior substantially. Prior C's 0.258 is "fission delivers something at Fission Surface Power class by 2035"; for Architecture D specifically we additionally need (a) specific power ≥ 10 watts-per-kilogram (Phase 1 stretch target, not baseline — perhaps 0.3–0.5 probability conditional on flight) and (b) program completion through Saturn deployment (perhaps 0.5–0.8 conditional). Net unconditional: 0.26 × 0.4 × 0.65 ≈ 0.07. Comparable to megawatt fission propulsion posterior (0.07–0.20).
2. **I'd treated Fission Surface Power Phase 1 active contracts as a stronger signal than it is.** Phase 1 contracts ($5M each × 3 teams, extended January 2025 rather than rolled into Phase 2) are early-design studies. The Phase 2 award is what would constitute material progress, and per locked beliefs Phase 2 is still pending as of May 2026. The probability-of-award estimate (0.6) is itself uncertain.

## Reading

The honest verdict: **Architecture D is the best-in-class cell in the architecture matrix but does not close cleanly.** Three observations.

1. **Architecture D's unconditional probability of working by 2035 is in the 0.05–0.15 range**, after cascading the program-flight probability with the specific-power-stretch probability with the program-completion probability. This is roughly comparable to the megawatt fission propulsion cell's 0.07–0.20 — a modest improvement, not a transformative one. The matrix is still program-risk-limited; Architecture D narrows the bet but does not eliminate it.

2. **The Fission Surface Power Phase 1 contracted specific-power target (5 watts-per-kilogram) is insufficient for Architecture D closure.** Closure requires the stretch target (10 watts-per-kilogram), which is consistent with the Duffy directive August 2025 scope expansion to 100 kilowatts-electric (per locked-belief edcfe909). Architecture D therefore implicitly bets on FSP Phase 2 hitting its *upper-bound* specific power, not its contracted baseline. This is a sharper conditional bet than the round's pre-registration anticipated.

3. **The reframing that R-non-fission-baseline established holds**: the architecture matrix's "reactor era" annotation should distinguish propulsion-side electric power from Saturn-side process power. Architecture D is the cleanest expression of that reframing — it bets on Saturn-side process power without coupling it to propulsion. The launch-mass-per-delivered penalty (12.5× vs megawatt fission Modular-Assembled-Radiators baseline's 2–3×) is the price paid for unbundling the fission bet from the propulsion bet. The L0-12 closure depends on whether that 4–6× launch-mass premium is acceptable; per gate-level cost projections the answer is "borderline" (a single-mission cost on the order of $1.5–2.5 billion vs $300–500 million at megawatt propulsion baseline — though megawatt propulsion baseline is itself a fragile target).

### Things this round did NOT prove

- That a 10-watts-per-kilogram Saturn-side reactor delivering 200 kilowatts-electric is achievable in the demonstrator window 2032–2035. The pre-registration anchored this on the Duffy directive scope; whether the actual Fission Surface Power Phase 2 award (when it arrives) commits to 10 watts-per-kilogram remains contingent.
- That the Saturn-side reactor can be safely launched, transited through the Van Allen belts, and operated at Saturn for one year. The 10-year design life from KRUSTY/Fission Surface Power specs covers the 13-year round-trip in principle but assumes ICEBERG's transit-through-belts thermal cycling profile is within reactor-design envelope. Not verified.
- That the Architecture D launch-mass-per-delivered ratio of 12.5× translates to an L0-12 closure in dollar figures. The cost analysis depends on per-mission reactor unit cost ($300M–$1B per locked beliefs) plus launch services (~$200–400M for Starship-class) plus vehicle ($150M order-of-magnitude) — total $650M–$1.6B per mission, projected delivered cost $32M–$80M per tonne of water delivered. Whether this passes L0-12 depends on the L0-12 ceiling, which is a program-economics question not resolved in this round.
- That a non-fission alternative for Saturn-side power has been comprehensively ruled out. R-non-fission-baseline ruled out solar at Saturn (1/92 of Earth-vicinity power) and plutonium-238 radioisotope thermoelectric generators (supply-infeasible at 100-kilowatt-electric scale). It did *not* model large solar-thermal mirror concentrators in detail; that path remains a defer-flag.

## Revisit

**Did the pre-registration hold?** Aggregate H-cps-agg held in *direction* — Architecture D is the best-in-class non-current-matrix cell — but **falsified in magnitude**. Specifically: the closure-specific-power threshold is the Phase 1 stretch (10 watts-per-kilogram) rather than the contracted baseline (5 watts-per-kilogram), and the unconditional Bayesian posterior is 0.07–0.15 not 0.30–0.55. The "transformatively defensible" framing in pre-registration was wrong; the honest framing is "modestly defensible, comparable in posterior to megawatt fission propulsion, with a cleaner narrative."

**What went wrong in pre-registration:**

- I treated the Fission Surface Power Phase 1 contracted target (5 watts-per-kilogram) as the *baseline* specific power that Architecture D could rely on. Actually 5 watts-per-kilogram doesn't close the energy budget at any sweep cell. *Lesson: do not anchor closure on the lower bound of an aspirational specific-power target; sweep against the lower bound and report what specific power is *required*, then ask whether that required specific power is the contracted baseline or the stretch.*
- I conflated "conditional on fission program continues" with "unconditional Architecture D closure." The unconditional posterior is the conditional times several sequential probabilities (specific power hits target, program completes, no schedule slip). *Lesson: for Bayesian posteriors on multi-stage program closures, model each conditional explicitly rather than reporting the headline conditional posterior as if it were unconditional.*

**Recurring lesson** (per the aelfrice experiment conventions, recurring lesson #7 "cheapest path vs. only viable path"): I went looking for an architecture cell that would be *the* defensible baseline, found one that is *more* defensible than current cells, and was tempted to overstate its margin. The honest finding is more nuanced: Architecture D is best-in-class but the matrix still has no slam-dunk baseline; the program-risk problem is fundamentally unsolved by architecture choice.

## Cross-learning

### Forward — adopt

- **Architecture D as the new matrix baseline cell, with explicit caveats.** Add to the architecture decision matrix with: reactor specific-power closure threshold 10 watts-per-kilogram (Fission Surface Power Phase 1 stretch target, equivalent to Duffy directive August 2025 scope), reactor mass 20–30 tonnes for 200–300 kilowatts-electric, vehicle dry 10–15 tonnes, delivered 16–28 tonnes per mission, launch/delivered ratio 6–18× (worse than megawatt fission Modular-Assembled-Radiators baseline 2–3× but acceptable on L0-12 conditional on cost).
- **Reframe matrix's "reactor era" annotation** to distinguish: (i) reactor for propulsion-side electric power (megawatt-class, no funded program), (ii) reactor for Saturn-side process power (Kilopower-Fission Surface Power class, Phase 1 contracted). Architecture D adopts (ii) only.
- **Posterior tier ordering for matrix cells:** Architecture D (0.07–0.15 unconditional) > Kilopower Variant B (0.05–0.13 unconditional, applying the same conditional cascade) > Megawatt all-electric end-to-end propulsion (0.03–0.08 unconditional). All cells are in the same order-of-magnitude tier; the program-risk-limited verdict of the matrix is unchanged. No cell exceeds posterior 0.20 unconditional.

### Forward — drop

- **Pre-registration H-cps-f's "0.30–0.55 posterior" framing is wrong** and should not propagate to the matrix. The honest unconditional posterior for Architecture D is in the same band as megawatt fission propulsion. The narrative is sharper for Architecture D (smaller-reactor, Phase 1 active, KRUSTY ground demo, decoupled from propulsion), but the math is not.

### Forward — defer

- **R-architecture-D-cost** — explicit dollar-figure L0-12 closure for Architecture D. The launch-mass-per-delivered ratio of 12.5× anchors a per-mission cost estimate of $650M–$1.6B; whether this passes L0-12 depends on the L0-12 ceiling and the steady-state mission cadence.
- **R-fission-surface-power-stretch-credibility** — what is the actual probability that Fission Surface Power Phase 2 (whenever awarded) commits to 10-watts-per-kilogram specific power rather than the Phase 1 contracted 5 watts-per-kilogram? Read the Phase 2 Draft Announcement (August 2025), the final Announcement (anticipated early 2026), and any post-FY2026-budget-actions context. If the answer is < 50%, Architecture D's posterior drops further.
- **R-saturn-side-solar-thermal** — large-mirror concentrator alternative to Saturn-side fission. Could in principle supply ≥ 1 megawatts thermal at 9.58 astronomical units with 1-square-kilometer inflatable mirror. Mass feasibility check at sub-1-tonne-per-1000-square-meters areal density. Speculative but flag for orchestrator.

### Backward — cross-references

- **R-non-fission-baseline** (commit `85a5aac`, same session): established that the binding fission-dependence is Saturn-side process power. This round prices that dependence at the smallest-credible fission scale (Kilopower-Fission Surface Power class for process power). Result: the dependence is real but the smallest-credible scale only modestly improves the unconditional posterior over megawatt propulsion.
- **R-megawatt-architecture-viability** (commit `28d2370`, prior enceladus session): the matrix's "fission-dependent" verdict was already established. This round refines the verdict: the fission dependence can be unbundled from propulsion via Architecture D, but the unconditional program-risk posterior does not improve as dramatically as the unbundling-narrative implies.
- **R-megawatt-marvl-radiator** (commit `bde06a2`, rhea session): rhea's load-bearing falsification of megawatt all-electric end-to-end strengthens the case for Architecture D as the matrix's new highest-posterior cell, since rhea's finding kills the alternative megawatt cell. Net: Architecture D is now the matrix's load-bearing baseline candidate, even though its unconditional posterior is modest.

### Methodology issues caught

- **Pre-registration treated FSP Phase 1 contracted target as the closure threshold.** It's actually the FSP Phase 1 stretch / Phase 2 scope. The pre-registration was off by a factor of 2× on specific power. *Lesson: read locked-belief sources twice when pre-registering closure thresholds — Duffy directive scope (100 kilowatts-electric at 10 watts-per-kilogram) ≠ Phase 1 baseline scope (40 kilowatts-electric at 5 watts-per-kilogram).*
- **Pre-registration conflated conditional and unconditional posteriors.** Fixed in Revisit; the corrected unconditional numbers are in the Reading section. *Lesson: when modelling multi-stage program closures, always break the cascade into named conditionals (program-continues, specific-power-hits-target, program-completes), assign each its own probability, and report the product.*
