# R-pricing-anchor-revisit — STUDY (pre-registered)

**Worker:** titan (re-spawn 5, branch `iceberg-titan-5` off `origin/main`)
**Date frozen:** 2026-05-22
**SCOPE:** `water-prop/rounds/R_pricing_anchor_revisit/SCOPE.md` (Saturn, latest+9)
**Round type:** synthesis / industrial-organisation. ~60% literature, ~30% modelling, ~10% code.
**Project-owner trigger:** "$1,400/kg does not accurately reflect what can be charged."

---

## Question

For each (operational era × customer segment), what is the **defensible realised price
per kilogram** ICEBERG can charge, and does correcting the pitch's flat $1,400/kg anchor
change the program-class verdict?

---

## What the pre-existing AUDIT already settled (frozen, before any new modelling)

`AUDIT.md` (orchestrator, task 8 of latest+9) walked every load-bearing financial round.
**Headline: no financial round uses $1,400/kg.** Most anchor at **$2,000–10,000/kg flat**;
the load-bearing ones (R_reactor_roadmap, R_delivery_irr_curve, R_variant_B_recovery_paths,
R_architecture_D_L1007_relaxation) use **$10,000/kg**; the price-aware ones
(R_LEO_water_demand_curve, R_heterogeneous_cadence) sweep $1,000–25,000/kg. The single
round near the pitch headline (R_financing_capital_stack, ~$1,000/kg) is not architecture-
load-bearing.

**This reframes the round.** The disagreement is **pitch-vs-campaign**, not within-campaign:
the pitch headline ($1,400/kg, = Falcon-Heavy published $/kg-to-LEO per footnote 540) is
*below* what the financial rounds already assume. The pitch's own §3.4 already reframes the
operative ceiling to **lunar-ISRU displacement ~$1,000/kg midpoint** with Earth-launch as
upper bound. So the real deliverable (AUDIT implication #5) is **not** "is $1,400 right" but:
**is the campaign's revenue assumption (≈$10k/kg in load-bearing rounds; the
R_LEO_water_demand_curve median-$1,500/kg Monte-Carlo distribution) defensible against real
public comparables?**

## Comparables gathered (titan-5 web research; full table + sources in run.py / RESULTS)

| Comparable | $/kg (≈2026) | Heritage |
|---|---|---|
| ISS commercial resupply, effective (NASA OIG IG-18-021) | ~$78,000–125,000/kg | AVAILABLE (1 hop) |
| NASA ISS-upmass planning assumption (same report) | ~$26,000/kg | AVAILABLE |
| Orbit Fab GEO hydrazine, published price ($20M / 100 kg) | ~$200,000/kg | ADJACENT (list price, pre-transaction) |
| Lunar-surface delivery, Intuitive Machines CLPS (value ÷ ~payload) | ~$775,000/kg | AVAILABLE (arithmetic) |
| Lunar-ISRU propellant, projected (NASA NTRS ISRU breakeven) | ~$78,000–100,000/kg | NONE (model) |
| Falcon Heavy published $/kg-to-LEO (= the pitch anchor) | ~$1,400–1,800/kg | AVAILABLE |
| Falcon 9 published $/kg-to-LEO | ~$2,800–3,500/kg | AVAILABLE |
| Starship aspirational | ~$10–200/kg | NONE |
| Luna-16 sample auction (novelty ceiling) | ~$4.3B/kg | ADJACENT (collectible, non-analogous) |
| Lunar helium-3 value claim | ~$20M/kg | NONE |

The recurring, government-paid, real comparable closest to "deliver mass to a destination in
space" is **ISS-CRS at ~$78–125k/kg**. The closest published *propellant-to-an-asset* price
is **Orbit Fab ~$200k/kg**. Both sit far above every segment ceiling in `ICEBERG-demand.md`
§3 (which tops out at DoD $10–25k/kg one-shot, crewed $5–10k/kg).

---

## Pre-registered hypotheses (SCOPE H1–H7; predictions revised per AUDIT + comparables)

| # | Hypothesis | Frozen prediction | Falsification band |
|---|---|---|---|
| H1 | $1,400/kg is below the realised WTP ceiling for every non-Mars segment through year 30+. | **HELD, decisively** — ISS-CRS ($78k), Orbit Fab GEO ($200k), DoD ($10–25k), crewed ($5–10k) all >> $1,400. | any non-Mars segment ceiling < $1,400/kg in any era. |
| H2 | Anchor-era (100 t/yr) blended price ≥ 2× pitch headline (≥ $2,800/kg). | **HELD** — demand §3 tier-1 blended $3,000–5,000/kg; conservative (no Mars/DoD) $4,000/kg. | blended anchor-era < $2,000/kg under conservative weightings. |
| H3 | A novelty / sovereign-flag premium ≥ $10,000/kg is defensible for the first ≤ 100 t. | **HELD-via-recurring-comparables** — first-100 t ≥ $10k/kg supported by ISS-CRS/Orbit Fab/DoD WTP. The *collectible* analogue (lunar samples $4.3B/kg) is HERITAGE-ADJACENT and does NOT transfer to bulk water; the defensible premium is mission-essential WTP, not collectible rarity. | no defensible analogue supports > $10,000/kg even for the first 10 t. |
| H4 | Regulated-utility rate-of-return pricing sustains $2,500–5,000/kg in the 1,000 t/yr era. | **HELD-PLAUSIBLE, lower edge** — demand §3 tier-2 blended $1,500–3,000/kg brackets the low end; the precise rate-base figure needs R_financing_capital_stack's capital number (deferred). | regulated rate-base gives < $1,500/kg or > $8,000/kg. |
| H5 | Monopoly-rent ≥ $20,000/kg sustainable for ≥ 100 t/yr captive volume through year 30+. | **SPLIT: held early, falsified sustained** — DoD one-shot $10–25k/kg and Orbit Fab $200k/kg support ≥ $20k/kg for *low-volume early* captive; demand §3 shows DoD eroding to $3–5k/kg at the 10,000 t/yr tier, so ≥ $20k/kg for ≥ 100 t/yr through year 30 is not sustainable. | no captive segment sustains ≥ $10,000/kg through year 30+. |
| H6 | Replacing $1,400/kg with the tier-aware band flips ≥ 1 load-bearing financial-cell verdict positive. | **FALSIFIED (predicted)** — the rounds already assume $10k/kg (above the demand-doc defensible blended of $3–5k early / $1.5–3k mid). Correcting toward the defensible band moves verdicts the *wrong* way; none flips positive on price. | a load-bearing verdict flips positive under revised pricing up to $5,000/kg blended. |
| H7 (load-bearing) | Pricing-anchor correction does NOT flip program-class; L0-24 reactor-program availability is binding. | **HELD (predicted)** — even at $10k/kg the verdict is technology-demonstrator (iapetus L0-24, 2.7% absolute ceiling). Price is real but not architecturally rescuing. | H6 + revised pricing puts a regulated-utility cell above the L0-24-conditioned 2.7% posterior threshold. |

**Frozen prior:** the AUDIT makes the outcome largely legible before modelling — the project-
owner challenge is *correct in direction* ($1,400 understates WTP) but *not load-bearing* on
the architecture verdict, because (a) the financial rounds already assume far more than
$1,400, and (b) the binding constraint is the reactor program, not price. The honest finding
is the asymmetry PROTOCOL lesson 7 does not cover: pricing is the rare axis where the
pessimistic anchor (flat launch-displacement) is *too* pessimistic, yet correcting it changes
nothing because a different axis dominates.

---

## Method

1. Encode the comparables table (with heritage tags + sources) and the demand §3 segment
   bands in `run.py`.
2. Per era (100 / 1,000 / 10,000 t/yr): WTP ceiling, competing-supply floor, defensible
   realised band per segment; volume-weight to a blended price; compare to the $1,400 pitch
   anchor, the $10k campaign anchor, and the lunar-ISRU $1,000/kg planning ceiling.
3. Test whether the R_LEO_water_demand_curve clearing-price distribution (median ~$1,500/kg,
   5th $200, 95th $15,000) is defensible against the comparables.
4. Adjudicate H1–H7; reading-level H7 verdict for the project owner; pitch-headline
   restatement recommendation.

## Out of scope (per SCOPE)

Cost-to-produce (that is the cost side; this is revenue). Re-deriving orbital-mechanics /
propulsion numbers. Resolving L0-24 or the program-class decision (this round informs it).
