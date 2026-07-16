# R-per-mission-economics-sensitivity-revisit — STUDY.md

**Author:** rhea (worker session, iceberg-rhea-2 branch)
**Date:** 2026-05-15 (latest+8, immediately following R-reactor-specific-power-program-targets)
**Status:** pre-registration. Self-questioning round against rhea's just-shipped R-reactor-specific-power-program-targets H7 finding.

## Why this round (the assumption I'm questioning)

R-reactor-specific-power-program-targets (commit `b7ddf0a`, just shipped) found max program net-present-value at zero discount of negative $132.5 billion across all twelve rows (every minimum-point × three-prior combination). Two assumptions in that finding deserve testing:

**Assumption 1 — per-mission cost.** I used $2 billion ship capital expenditure + $3 billion launch = $5 billion per mission. My own prior round R-architecture-D-cost used $0.55–0.70 billion ship + $0.2–0.7 billion launch = $0.75–1.40 billion central per-mission cost. **I over-counted per-mission cost by 3–6 times against my own anchor.** This is a cross-round cost-anchor inconsistency — methodology lesson candidate #12.

**Assumption 2 — decision frame.** H7 multiplied conditional delivered mass by the full conjunction posterior (reactor delivers × engineering closes × engineering closes) to compute "programmatic-risk-adjusted expected delivered mass." This is the right decision frame for return-seeking capital, which P-weights expected returns. But it's the **wrong** decision frame for sovereign-grant pitch — a sovereign grant exists to underwrite the reactor program; it does not multiply expected delivered mass by P(reactor program succeeds). The matrix's pitch/capital framing axis (axis 17) currently does not distinguish these two decision frames.

This round answers: (a) does H7's structural finding survive a 3–5 times cost-anchor correction? (b) what is the conditional-on-success per-mission cashflow at corrected anchors? (c) does the matrix have a decision frame under which any minimum-point closes?

This is a sensitivity round, not a new physics round. Inputs: R-reactor-specific-power-program-targets synthesis table; R-architecture-D-cost economics anchors; R-LEO-water-demand-curve clearing-price assumption (BEST_CELL ≈ $2.5 million per tonne via Saturn integration `e7d43dd`).

---

## Pre-registered hypotheses

### H1 — corrected per-mission cost lifts net-present-value but does not flip sign

Anchors corrected from R-architecture-D-cost:
- ship capital expenditure: $0.65 billion (central; the D-fission anchor)
- launch cost per mission: $0.30 billion (Starship central, three launches per mission)
- nonrecurring engineering: $1.0 billion (mid of R-architecture-D-cost's $0.5 billion and ICEBERG's flagship-class-by-mass guess)
- ship reuse: 15 missions per ship (Variant B implicit anchor; ship CapEx amortizes)
- effective per-mission cost = $0.65 / 15 + $0.30 = **$0.343 billion per mission**

Conditional delivered mass at H2a minimum-point (8 watts per kilogram specific power, 10-year lifetime, no aerocapture) = 42.0 tonnes per mission per R-specific-power-cliff `best_at_25yr`.

Conditional per-mission revenue at BEST_CELL ($2.5 million per tonne) = $0.105 billion.

**Conditional per-mission cashflow = $0.105 - $0.343 = -$0.238 billion.** Negative, but order-of-magnitude smaller than H7's implied -$5 billion per mission.

Conditional program net-present-value at zero discount = (-$0.238 × 25 missions) - $1.0 billion nonrecurring engineering = **-$6.95 billion**.

**H1 prediction:** corrected conditional net-present-value is in [-$15 billion, -$3 billion]. Compare to H7's -$132 billion → **2 orders of magnitude correction.** Direction correct (still negative), magnitude off by ~20 times.

| | predicted | falsification |
|---|---|---|
| H1 | corrected conditional program net-present-value(0) at H2a is in [-$15 billion, -$3 billion] | falsified if outside, or if sign flips positive at central anchors |

### H2 — break-even clearing-price threshold

At ship-amortized per-mission cost $0.343 billion, per-mission revenue must exceed cost to flip cashflow positive. At conditional delivered mass 42 tonnes per mission, required clearing price = $0.343 billion / 42 tonnes = **$8.2 million per tonne**, or 3.3 times BEST_CELL. Pre-registered range $5–15 million per tonne accommodating launches-per-mission uncertainty.

**Sensitivity:** at higher launches per mission (5 instead of 3), per-mission launch cost $1.5 billion, effective cost $1.54 billion, break-even clearing price = $36.7 million per tonne, or 15 times BEST_CELL.

| | predicted | falsification |
|---|---|---|
| H2 | break-even clearing price for conditional per-mission cashflow at H2a minimum-point is in [$5, $40] million per tonne depending on launches-per-mission anchor | falsified if any anchor configuration gives break-even below $3 million per tonne (1.2 times BEST_CELL — too easy) or above $100 million per tonne (40 times BEST_CELL — too hard) |

### H3 — H7 magnitude correction

H7 from R-reactor-specific-power-program-targets reported program net-present-value(0) = -$132.5 billion across all rows. Re-deriving at corrected anchors (H1 anchors above) for H2a uniform-prior row:

- conjunction posterior 0.167%
- conjunction-weighted expected delivered mass = 0.167% × 42 tonnes = 0.070 tonnes per mission
- conjunction-weighted per-mission revenue = 0.070 × $2.5 million = $0.000175 billion = $175,000
- conjunction-weighted per-mission cashflow = $0.000175 - $0.343 = -$0.343 billion per mission
- conjunction-weighted program net-present-value(0) = (-$0.343 × 25) - $1.0 nonrecurring engineering = **-$9.58 billion**

H7's headline magnitude (-$132.5 billion) was inflated by 14 times at H2a uniform-prior row due to cost over-counting. The structural reading (net-present-value negative) survives; the magnitude does not.

| | predicted | falsification |
|---|---|---|
| H3 | corrected conjunction-weighted program net-present-value(0) at H2a uniform-prior row is in [-$15 billion, -$5 billion] — direction matches H7 (negative), magnitude off by 8–15 times | falsified if magnitude correction is less than 3 times (H7 was right) or more than 30 times (suspect double-counting somewhere) |

### H4 — decision-frame distinction

The conjunction-weighted framing is correct for **return-seeking capital**. Under return-seeking capital, the project is structurally not closeable at conservative anchors (corroborated by R-power-bayesian-update, R-architecture-D-cost, R-reactor-specific-power-program-targets — three rounds, same direction).

The conjunction-weighted framing is **wrong** for **sovereign-grant pitch**. Sovereign-grant decision criteria are not P-weighted expected return; they are technology-readiness-lift, scientific value, strategic value, conditional on programmatic milestones. The relevant calculation is conditional-on-success per-mission cashflow and conditional-on-success program net-present-value, which the corrected H1 finding gives.

Reframe: H2a minimum-point under sovereign-grant decision frame has conditional program net-present-value -$7 billion at zero discount — comparable to NASA Flagship-class missions (Europa Clipper $5 billion, Mars Sample Return $11 billion, Cassini $3.9 billion). **The decision is whether the demonstrator-class value (megawatt-class fission flight heritage + Saturn-system in-situ + water-ice harvest precursor) justifies a $7 billion programmatic cost.** That is a NASA-or-equivalent-agency policy question, not a finance question.

| | predicted | falsification |
|---|---|---|
| H4 | ICEBERG H2a minimum-point at conservative anchors falls within NASA Flagship-class cost band ($3–11 billion); decision frame is sovereign-grant policy, not commercial net-present-value | falsified if corrected conditional program net-present-value exceeds $20 billion (well beyond Flagship class) or is below $1 billion (below Discovery class) |

### H5 — matrix amendment recommendation

R-reactor-specific-power-program-targets H6 said "technology-demonstrator-only" at conservative anchors. This round refines: the matrix should distinguish two decision frames, each with its own viability reading on axis 17 (pitch / capital framing):

- **Track A (return-seeking capital):** conjunction-weighted expected net-present-value. **Ruled out** at conservative anchors per R-reactor-specific-power-program-targets H6.
- **Track B (sovereign-grant policy):** conditional-on-success program cost vs Flagship-class threshold. **Viable in principle** at H2a minimum-point (corrected conditional net-present-value -$7 billion sits inside Flagship cost band). Conditional on (a) reactor program succeeding inside ICEBERG window, (b) hybrid-aerocapture-aerobraking or non-aerocapture engineering closure, (c) sovereign-grant policy buy-in on demonstrator value.

The two tracks are not contradictory; they answer different decision-maker questions. Matrix axis 17 currently mixes them under one "pitch / capital framing" label.

| | predicted | falsification |
|---|---|---|
| H5 | matrix axis 17 amendment should split pitch framing into two tracks (return-seeking-ruled-out + sovereign-grant-viable-in-principle); this is a refinement of R-reactor-specific-power-program-targets H6, not a contradiction | falsified if the two-track framing produces internally inconsistent verdicts on any single matrix cell |

### H6 — methodology-lesson candidate #12

Cross-validate cost anchors against recent rounds before back-of-envelope pre-registration. The round-9 cost over-counting (5 times against my own R-architecture-D-cost anchor) was caught only by self-review after the round shipped. Lesson candidate: **before BOE on cost numbers, grep recent rounds for the same parameters.**

| | predicted | falsification |
|---|---|---|
| H6 | methodology-lesson #12 holds — cross-round cost-anchor inconsistency is the largest single source of magnitude error in round-9 H7 | falsified if a different source (e.g. miscoded clearing price, wrong delivered-mass anchor) is bigger |

---

## Method (run.py)

1. Load R-reactor-specific-power-program-targets `synthesis.json`. Use its minimum-point + conjunction-posterior data.
2. Re-derive economics under R-architecture-D-cost anchors (ship $0.65 billion, launch $0.30 billion central, nonrecurring engineering $1 billion, ship reuse 15 missions).
3. Sweep launches-per-mission {3, 5, 8} × ship reuse {5, 15, 25} × clearing price {$2.5, $10, $25, $100 million per tonne} × N missions {10, 25, 50}.
4. Compute three net-present-value frames per cell: (a) conjunction-weighted, (b) conditional-success, (c) conditional-success with no nonrecurring engineering (i.e. nonrecurring engineering externalized to reactor program).
5. Find break-even clearing price per cell at conditional-success frame.
6. Identify which sweep points produce positive net-present-value at conditional-success frame.
7. Grade H1–H6.
8. Write synthesis table + findings.

Output: `results/sensitivity.json`, `results/sensitivity_table.csv`, `results/findings.md`.

---

## Validity caveats

1. **Ship reuse 15 missions is a guess.** Variant B implicit anchor. ICEBERG architecture may permit fewer (chunk-rendezvous wear-and-tear, micrometeoroid exposure during 20-yr round-trip × 15 ship-lifetime = 300 years cumulative exposure). Sensitivity sweep covers {5, 15, 25}.
2. **Launches per mission is architecture-dependent.** 200-tonne chunk outbound + reactor + tug + propellant: at Starship 100 tonnes to low-Earth orbit, likely 3–5 launches per mission. titan-2 R-launch-cost-sensitivity assumed 3.
3. **Nonrecurring engineering at $1 billion is a guess.** R-architecture-D-cost used $0.5 billion (matched R-reactor-roadmap). Flagship-class historical: Cassini $3.9 billion total (mostly recurring), Europa Clipper $5 billion. ICEBERG's nonrecurring is unanchored. Sensitivity sweep covers {$0.5, $1.0, $3.0 billion}.
4. **Clearing price is the most uncertain economic input.** R-LEO-water-demand-curve produced a Monte Carlo distribution; BEST_CELL is the favorable tail. CONOPS_BASE is a more conservative anchor. This round sweeps {$2.5, $10, $25, $100} million per tonne to span the full range.
5. **Conditional-success framing externalizes reactor program cost.** Under sovereign-grant pitch, the reactor program (Fission Surface Power Phase 2 at ~$1–3 billion or scoped successor) is funded separately. ICEBERG nonrecurring engineering is then ICEBERG-specific only. This is the H4 framing.
