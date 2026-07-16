# R-pricing-anchor-revisit — RESULTS

**Worker:** titan-5 · **Date:** 2026-05-22 · **Branch:** `iceberg-titan-5`

Synthesis round. Comparables from titan-5 web research (sources in `run.py`); segment
bands from `ICEBERG-demand.md` §5; financial-round anchors from the pre-existing `AUDIT.md`.

---

## Comparables (real public, ≈2026 $/kg)

| Comparable | $/kg | Heritage | Source |
|---|---|---|---|
| ISS resupply, effective (Cygnus) | 125,000 | AVAILABLE | NASA OIG IG-18-021 |
| ISS resupply, effective (Dragon) | 78,000 | AVAILABLE | NASA OIG IG-18-021 |
| NASA ISS-upmass planning assumption | 26,000 | AVAILABLE | NASA OIG IG-18-021 |
| Orbit Fab GEO hydrazine (published price) | 200,000 | ADJACENT | Orbit Fab 2022 ($20M/100 kg) |
| Intuitive Machines CLPS lunar-surface (value÷payload) | 775,000 | AVAILABLE | NASA CLPS 2021 |
| Lunar-ISRU propellant (projected) | 90,000 | NONE | NASA NTRS ISRU breakeven |
| **Falcon Heavy $/kg-to-LEO (= the pitch anchor)** | **1,500** | AVAILABLE | CSIS / SpaceX list |
| Falcon 9 $/kg-to-LEO | 3,000 | AVAILABLE | CSIS / OWID |
| Starship aspirational | 100 | NONE | SpaceX statements |
| Luna-16 sample auction (novelty ceiling) | 4.3 B | ADJACENT | Sotheby's 2018 (collectible) |

The closest **recurring, real, government-paid "deliver mass to a space destination"**
comparable is ISS commercial resupply at **$26–125k/kg**. The closest **published
propellant-to-an-asset** price is Orbit Fab at **$200k/kg**. Both sit far above every
non-Mars segment ceiling in the demand doc.

## Blended realised price per era (volume-weighted, demand §5 bands)

| Era | full (incl. spec) | conservative (no spec) | external-only | reproduces demand-doc |
|---|---|---|---|---|
| 100 t/yr (Kilopower) | **$5,025/kg** | $3,639/kg | $9,050/kg | yes ($3–5k) |
| 1,000 t/yr (FSP) | $2,225/kg | $1,639/kg | $4,062/kg | yes ($1.5–3k) |
| 10,000 t/yr (MW + Mars) | $505/kg | $1,226/kg | $458/kg | yes ($0.3–0.8k, Mars-weighted) |

The pitch anchor **$1,400/kg sits below the blended realised price in the two near-term
eras** and equals the Falcon-Heavy launch-displacement floor by construction.

---

## Hypotheses adjudicated

| # | Verdict | Evidence |
|---|---|---|
| H1 | **HELD** | Min non-Mars segment ceiling $1,500/kg (tier-3 lunar) ≥ $1,400. Every other segment ceiling is $2k–$25k. Decisively held above the floor; thinnest where lunar-ISRU competing supply caps it. |
| H2 | **HELD** | Tier-1 blended $5,025/kg (full) / $3,639/kg (conservative, no speculative) — both ≥ 2× pitch ($2,800). |
| H3 | **HELD via recurring comparables** | First-100 t ≥ $10k/kg supported by ISS-CRS ($26–125k) and Orbit Fab GEO ($200k) — *recurring* market prices, not the collectible analogue. The Luna-sample $4.3 B/kg (HERITAGE-ADJACENT) is a rarity premium that does NOT transfer to bulk water; the defensible first-delivery premium is mission-essential WTP, not collectible value. |
| H4 | **HELD-PLAUSIBLE (lower edge)** | Tier-2 blended $1,639–2,225/kg brackets the $2,500 low end of the predicted regulated-utility band; the precise rate-base figure needs R_financing_capital_stack's capital number (deferred). Within the demand envelope; not falsified (not <$1,500 nor >$8,000). |
| H5 | **SPLIT — held early, falsified sustained** | DoD one-shot $10–25k/kg and Orbit Fab $200k/kg support ≥ $20k/kg for *low-volume early* captive demand. But demand §5 shows DoD eroding to $3–5k/kg at the 10,000 t/yr tier, so ≥ $20k/kg for ≥ 100 t/yr *through year 30+* is not sustainable. Captive segments do sustain ≥ $10k/kg early (H5 falsification band not tripped). |
| H6 | **FALSIFIED** | Per AUDIT.md the load-bearing financial rounds already use **$10,000/kg** — above the defensible blended ($3.6–5k early, $1.6–2.2k mid). Correcting the *pitch* anchor toward the defensible band moves the financial rounds' assumption *downward*, not up; **no verdict flips positive on price**. The "matrix-empty / sub-sovereign-bond" verdicts are robust because they already assume generous pricing. |
| H7 (load-bearing) | **HELD** | Even at $10,000/kg the program-class verdict is technology-demonstrator (iapetus L0-24; 2.7% absolute posterior ceiling on flight-reactor availability). Pricing correction is real but **not architecturally rescuing** — the binding constraint is reactor-program availability, not revenue per kilogram. |

## Inverse-risk check (mirror of the project-owner challenge)

`inverse_risk_check.py` imports R_reactor_roadmap's own IRR machinery and recomputes its
marginal internal-rate-of-return (integrated over the R_power_base_rate reactor-arrival
distribution) across the price band, to test whether any positive-leaning verdict is *propped
up* by the generous $10k anchor:

| Price anchor | Marginal IRR | vs sovereign-bond hurdle (~4%) |
|---|---|---|
| pitch floor ($1,400) | 0.00% | below |
| conops base ($2,000) | 0.00% | below |
| tier-1 conservative ($3,639) | 0.00% | below |
| tier-2 external ($4,062) | 0.00% | below |
| tier-1 full ($5,025) | 0.00% | below |
| campaign anchor ($10,000) | 1.45% | below |

(The $10k figure reproduces R_reactor_roadmap's own published 1.45% headline; below ~$10k the
megawatt-arrival branches go net-present-value-negative even at a 0% discount, so the IRR
floors to 0.) **The marginal-IRR verdict is sub-sovereign-bond across the ENTIRE range
$1,400–10,000/kg.** No verdict is propped up by the generous anchor; if anything the economic
case is *more* fragile below $10k. This confirms H7 from both directions: pricing cannot
rescue the program (H6) and is not secretly carrying it (this check). The economic axis is
robustly not the binding constraint.

## R_LEO_water_demand_curve distribution defensibility

Distribution: median ~$1,500/kg, 5th $200, 95th $15,000 (Starship cost × in-space markup).
**Verdict: defensible-but-conservative.** The median sits at the competing-supply floor
(Falcon-Heavy / lunar-ISRU), and the 95th percentile ($15k) reaches DoD/ISS-CRS WTP. It is
a sound *launch-cost-driven bulk* prior, but it **under-weights captive-segment market power**
(ISS-CRS $78k, Orbit Fab $200k are above its 95th percentile). The campaign's most
price-aware round is therefore conservative, not optimistic — consistent with the
demand doc's own confidence-stratified reading.
