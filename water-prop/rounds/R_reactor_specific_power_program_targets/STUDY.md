# R-reactor-specific-power-program-targets — STUDY

**Author.** iapetus
**Date.** 2026-05-15 (latest+9)
**Anchor SCOPE.** `SCOPE.md` (commit prior to this round). Synthesis round; no new propulsion physics.
**Pre-registered hypotheses.** H1-H6 (see `SCOPE.md` §"Pre-registered hypotheses").

---

## Inputs

Five prior rounds' closure tables and Bayesian posterior set, all loaded verbatim:

| Round | Path | What it gives |
|---|---|---|
| R-specific-power-cliff | `R_specific_power_cliff/results/specific_power_cliff.json` | close-Nyr counts at each specific-power level (X=0 baseline) |
| R-aerocapture-cliff-shift | `R_aerocapture_cliff_shift/results/aerocapture_cliff_shift.json` | close-Nyr counts on (specific-power × aerocapture-credit) grid |
| R-reactor-lifetime-vs-burn-time | `R_reactor_lifetime_vs_burn_time/results/reactor_lifetime_regrade.json` | close-25yr counts on (specific-power × aerocapture-credit × lifetime-ceiling) grid |
| R-arch-E-specific-power-flown-anchored | `R_arch_E_specific_power_flown_anchored/results/arch_E_specific_power_sweep.json` | flown-anchored baseline (KRUSTY 2.4 W/kg) |
| R-power-bayesian-update | `R_power_bayesian_update/results/R_power_bayesian_update_summary.json` | three-prior posterior on US-fission orbit by 2035: 2.92% (skeptical) / 4.93% (Jeffreys) / 8.92% (uniform); scope conditional p(500 kWe given Fission-Surface-Power orbit) = 0.6 |

No new physics. Three subjective conditional-probability priors introduced (documented in §"Subjective priors below"):
- p(specific-power ≥ S | orbit, scope-500 kWe) — anchored on Fission-Surface-Power-Phase-1 design-spec range and the Kilowatt-Reactor-Using-Stirling-Technology flown anchor.
- p(lifetime ≥ L | orbit, scope-500 kWe) — anchored on Kilopower design target 10-15 yr.
- p(aerocapture-credit X ≥ X_min | hybrid-aerocapture-aerobraking round closes) — closure level matters, treated as decreasing in X.

---

## Hypotheses adjudicated

### H1 — L0-05 strict min-point: predicted (specific-power ≥ 8, lifetime ≥ 5 yr)

**Verdict: FALSIFIED, but on the strict-feasibility side.**

The L0-05 strict requirement (≤20-yr round-trip) has **zero closing cells anywhere in the tested specific-power range up to 10 W/kg**. From `specific_power_cliff.json`:

| specific power (W/kg) | close_20yr count (of 60 cells) |
|---:|---:|
| 2.4 | 0 |
| 5.0 | 0 |
| 6.0 | 0 |
| 7.0 | 0 |
| 8.0 | 0 |
| 9.0 | 0 |
| 10.0 | 0 |

→ The hypothesis is **misspecified**: there is no min-point at L0-05 strict within tested specific-power range. The result tightens R-arch-E-specific-power-flown-anchored: not just "doesn't close at KRUSTY 2.4 W/kg" but "doesn't close at any specific power tested up to 10 W/kg" when the round-trip ceiling is the strict 20-yr value.

**Consequence.** Any matrix-cell-restoration argument under L0-05 strict requires either specific-power > 10 W/kg (which crosses into pure paper-study territory per the National Academies 2021 report — flown anchor is 5.3 W/kg General-Purpose-Heat-Source Radioisotope-Thermoelectric-Generator, KRUSTY 2.4 W/kg system-level), OR a waiver to ≥25-yr round-trip ceiling. Project owner already has the waiver path documented; this round confirms the strict path is closed.

### H2 — L0-05 waiver + aerocap-10 km/s min-point: predicted (specific-power ≥ 5, lifetime ≥ 10 yr)

**Verdict: PARTIALLY-FALSIFIED.**

Measured at aerocap-credit X=10 km/s:

| specific power (W/kg) | lifetime L=10 yr | lifetime L=15 yr |
|---:|---:|---:|
| 5.0 | 0 | 3 |
| 6.0 | 1 | 8 |
| 7.0 | 6 | 13 |
| 8.0 | 15 | 20 |

→ At specific-power=5 W/kg, lifetime=10 yr is **not enough** (0 cells). The minimum at X=10 is either (specific-power=5, lifetime=15) → 3 cells OR (specific-power=6, lifetime=10) → 1 cell. The predicted point is one axis-click short on either dimension.

**Consequence.** The 5 W/kg specific-power band is recoverable only with longer lifetime (15 yr) than predicted. The Fission-Surface-Power-Phase-1 design-spec target is 10-15 yr cumulative full-power burn; the upper end of that range is the load-bearing one.

### H3 — p(US fission orbit in 2032-2035, specific-power ≥ 8 AND lifetime ≥ 5) ≤ 3 percent

**Verdict: CONFIRMED.**

Upper-bound calculation under the most-optimistic (uniform) prior:
- p(500 kWe orbit by 2035 | uniform) = 0.13%
- p(specific-power ≥ 8 | orbit, 500 kWe) = 8% (anchored on FSP-1 stretch + 3× KRUSTY heritage)
- p(lifetime ≥ 5 | orbit, 500 kWe) = 80% (Brayton-flight-rated minimum)
- joint = 0.13% × 0.08 × 0.80 ≈ **0.0083%**

Three orders of magnitude below the 3% upper bound. Even under aggressively-optimistic specific-power conditional priors (e.g. 50% rather than 8%), the joint stays under 1%. The Bayesian-update round already absorbs the dominant negative shock (p_500kWe small because both fission orbit AND scope conditional are required).

### H4 — p(US fission orbit in 2032-2035, specific-power ≥ 5 AND lifetime ≥ 10) ≤ 1 percent

**Verdict: CONFIRMED.**

Upper-bound under uniform prior:
- 0.13% × 0.40 × 0.40 ≈ **0.021%**

Well below the 1% upper bound. Even with maximally-generous specific-power conditional (1.0 — i.e. "if any orbit happens, sp ≥ 5 W/kg is essentially certain"), joint = 0.13% × 0.40 = 0.052%, still below 1%.

### H5 — full-conjunction posterior ≤ 1% (optimistic) / ≤ 0.1% (conservative)

**Verdict: CONFIRMED on both legs.**

Full conjunction = p(reactor delivers specific-power ≥ S AND lifetime ≥ L AND scope ≥ 500 kWe AND in window) × p(hybrid-aerocapture-aerobraking closes at X ≥ X_min) × p(bring-rendezvous-survivability closes).

Best corner (specific-power=5 W/kg, aerocapture-X=10 km/s, lifetime=∞) under uniform prior + rendezvous-survivability-high 30% prior + hybrid-aerocapture 50% prior:
- p_full_conjunction = **0.0055%**

Best corner under skeptical prior + rendezvous-survivability-low 20% prior:
- p_full_conjunction ≈ **0.0006%**

Both well below the predicted upper bounds. The Bayesian floor is dominant — the reactor-program priors alone (p_500kWe_orbit_by_2035 ~0.01-0.13%) already put the conjunction below 0.1%, before engineering closures are even applied.

### H6 — reading-level: technology-demonstrator-only is the honest reading

**Verdict: CONFIRMED.**

Cross-tabulation of every (corner × prior × rendezvous-prior) combination — 26 corners × 3 priors × 2 rendezvous priors = 156 cells. **Zero** clear the venture-class 10% threshold, and zero clear the corporate-growth-class 30% threshold.

| capital class | min p_full_conjunction | cells qualifying / 156 |
|---|---:|---:|
| technology-demonstrator (any positive) | 0 | 156 |
| venture (≥10%) | 0.10 | **0** |
| corporate-growth (≥30%) | 0.30 | 0 |
| regulated-utility (≥50%) | 0.50 | 0 |
| sovereign-bond (≥80%) | 0.80 | 0 |

Every (corner × prior × rendezvous) combination lands in the technology-demonstrator class. There is no candidate reactor-program profile and engineering-closure conjunction that supports anything more than research-grade financing posture under the conservative-anchor matrix state as of latest+7.

---

## Headline

Under conservative anchors (Fission-Surface-Power Phase-2 not awarded as of May 2026, US-fission base rate 0-of-6 since Strontium-Nuclear-Auxiliary-Power-10A 1965, and engineering rounds R-hybrid-aerocapture-aerobraking and R-bring-rendezvous-survivability not yet closed), the **maximum full-conjunction posterior** for any restored matrix cell is **0.0055% under the most-optimistic prior bracket**. **L0-05 strict (≤20-yr round-trip) is unreachable at any tested specific power up to 10 W/kg**; the matrix is restorable only with a ≥25-yr round-trip waiver AND a reactor-program profile no current US program funds AND both engineering rounds closing positively. Three orders of magnitude below the venture-class 10% threshold; zero of 156 cross-cuts clear it.

---

## Reading

**Matrix decision point #1 (program-class decision at conservative anchors): technology-demonstrator-only.**

This is the project-owner-level recommendation. The project-owner walk-through latest+8 deferred two Level-0 framing decisions (L0-13 capital structure, reactor-program-availability Level-0) to this round's results. This round's reading:

1. **L0-13 capital-structure decision is forced to government-grant / sovereign-research-grant framing.** No private-capital class clears even venture-risk threshold under any prior bracket. The L0-13 amendment that the walk-through deferred is therefore required, with the structure being a research grant or sovereign technology-demonstrator program rather than equity venture or sovereign-bond infrastructure financing.
2. **Reactor-program-availability Level-0 must be added as a binding constraint.** A reactor program delivering specific-power ≥ 5 W/kg AND lifetime ≥ 10 yr AND scope ≥ 500 kWe in the 2032-2035 window has posterior probability ≤ 0.13% under uniform prior, dropping to 0.0001% under skeptical prior. Until a Fission-Surface-Power Phase-2 contract is awarded with scope and lifetime in this band, the reactor closure is the binding viability gate.

**The honest pitch posture remains technology-demonstrator.** Restoring regulated-utility or sovereign-bond framing requires (a) a Fission-Surface-Power-Phase-2 contract announcement with specific-power and lifetime in the 5+ W/kg / 10+ yr band, AND (b) R-hybrid-aerocapture-aerobraking returning a positive closure result with X ≥ 10 km/s credit, AND (c) R-bring-rendezvous-survivability returning a positive closure result. None of these have happened. Until at least one of them does, the joint conjunction stays in technology-demonstrator class.

**A narrow lobby-target band exists.** If a future US fission program announcement targets specific-power ≥ 5 W/kg AND lifetime ≥ 10 yr AND scope ≥ 500 kWe AND has an orbital flight plan within the 2032-2035 window, the conjunction posterior could move from 0.0055% to perhaps 1-3% (still venture-marginal but not sovereign-bond). That is the reactor-program target profile the project owner could rationally advocate for; absent it, no candidate cell exists.

---

## Cross-learning

- **R-power-bayesian-update (hyperion).** This round's outputs are downstream of hyperion's three-prior posterior, and the Bayesian floor is the dominant negative factor in every conjunction. Confirms hyperion's bracket of 2.9-8.9% on US-fission-orbit-by-2035 propagates directly to the matrix-cell-restoration question — multiplying by the reasonable specific-power and lifetime conditionals brings it down by 2-3 more orders of magnitude.
- **R-power-wonder findings 1-4 (user-locked May 2026).** Finding 1 (40 W/kg is Technology-Readiness-Level 2 paper figure) corroborates: even the most-aggressive specific-power band tested here (10 W/kg) is 4× below the matrix's optimistic 40-W/kg assumption. Finding 4 (radiators are 40-55% of system mass at megawatt-electric scale per Modular-Assembled-Radiators-for-Very-Large MARVL studies) explains why scaling specific-power up is hard: deployable ultra-low-areal-density radiators do not exist.
- **R-arch-E-specific-power-flown-anchored.** Tightened: not just "Architecture E doesn't close at KRUSTY-anchored 2.4 W/kg" but "Architecture E doesn't close at L0-05 strict at any specific power up to 10 W/kg".
- **R-aerocapture-cliff-shift.** Aerocapture credit is the highest-leverage engineering recovery axis. At X=20 km/s, sp=5 W/kg, L=10 yr → 12 cells. At X=25, → 32 cells. **But** R-aerocapture-cliff-shift's own outbound-binding finding caps the rescue: at KRUSTY-anchored 2.4 W/kg, even closing aerocapture perfectly does not rescue the cell (the outbound burn becomes the binding constraint).
- **R-hybrid-aerocapture-aerobraking and R-bring-rendezvous-survivability (open).** Reading even with both closing at 100%: best corner posterior = 0.13% × 0.40 × 0.40 × 1.0 × 1.0 = **0.021%**. Still venture-infeasible. Closing both does not by itself restore non-research-grade financing.

---

## Next-round candidates

1. **(L0-13 amendment + reactor-program-availability Level-0 ratification.)** This is project-owner work in the matrix and Level-0 requirements docs, not a worker round. With this round's result, the walk-through latest+8 deferred decisions can be ratified: L0-13 → government-grant / sovereign-research-grant; new Level-0 added for reactor-program-availability binding constraint.
2. **R-non-US-reactor-program-priors (out-of-scope here, called out in SCOPE).** If the project owner wants to expand the reactor-program-priors beyond US-anchored, China-National-Space-Agency, Roscosmos, and emerging European reactor programs would each need their own base-rate analysis. Caveat: regulatory and capital-class implications differ — a non-US reactor program might restore reactor-orbit posterior but the US-sovereign-financing class would simultaneously close.
3. **Pitch rewrite anchored on technology-demonstrator class.** Per H6 verdict, the honest pitch posture is research-grade. ICEBERG-pitch.md currently positions across multiple capital classes — the load-bearing pitch reframe is to lead with technology-demonstrator and surface other classes only conditional on the reactor-program announcement.
4. **Optional — R-engineering-closures-conditional-on-tech-demo-funding.** If the program is reframed as technology-demonstrator, the cost of failure on R-hybrid-aerocapture-aerobraking and R-bring-rendezvous-survivability is research dollars, not commercial-capital write-down. Different go/no-go logic; worth a follow-on synthesis.

---

## Methodology notes (lessons applied)

- **Lesson 7 (pessimistic-anchor-first).** Applied conservative reactor-program priors (R-power-bayesian-update three-prior bracket; subjective specific-power and lifetime conditionals anchored on flown heritage, not paper-study targets).
- **Lesson 8 (program-level NPV check).** This round reports joint-posterior probability per capital class, not per-mission unit economics. Per H6, the right question at the program-level decision point is "what financing-class threshold does the joint posterior clear?", not "is a single cell profitable?".
- **Lesson 9 (anchor SCOPE on prior aggregate verdict).** SCOPE anchored on the four enceladus-r5 STUDY.md primary-text result tables verbatim. Re-uses closure_verdict counts directly; no re-running of propulsion physics. Subjective priors documented inline in `run.py`.

---

## Files

- `SCOPE.md` — pre-registration (saturn, latest+7)
- `run.py` — synthesis composition + Bayesian conjunction
- `results/reactor_program_targets.json` — full output with min-corner table, synthesis_table, capital-class roll-up, hypotheses verdicts
