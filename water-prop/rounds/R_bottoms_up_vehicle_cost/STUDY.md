# R-bottoms-up-vehicle-cost — what is a defensible first-unit cost for Variant B and Architecture E ships, and what does that do to R8's NPV-positive probabilities?

**Status:** pre-registration. Authored 2026-05-15 by enceladus-r5 (round 13).

## Question

Round 7 (R-fleet-ramp-NPV, commit `253345a`) and round 8 (R-LEO-water-demand-curve, commit `ed3dd58`) both used placeholder first-unit costs:

- Variant B: $500M / ship
- Architecture E_500: $300M / ship
- Architecture E_200: $300M / ship

These were flagged in `R_architecture_E_no_saturn_side_electrolysis/STUDY.md` as "best-guess from prior matrix work and have not been independently verified." The round-8 STATE.md follow-up thread #18 (`R-bottoms-up-vehicle-cost`) flagged the placeholders as **load-bearing** for the round-8 strict-dominance finding (Variant B > Arch E on P(NPV+)), because Variant B's "won" status assumes the $500M placeholder is approximately correct.

**Primary question:** what is a defensible bottoms-up first-unit cost for each architecture's ship, anchored against flight-heritage cost-per-kilogram, programmatic cost-estimating-relationships, and recent nuclear-electric / high-power-propulsion cost data?

**Secondary question:** how do round-8's P(NPV+) curves shift when round-7's placeholder is replaced with the bottoms-up median (and 5th / 95th percentile of cost uncertainty)?

**Tertiary question:** does Variant B retain its strict-dominance status over Architecture E on NPV-probability under bottoms-up cost, or does Architecture E's relatively-smaller upward revision flip the ordering?

## What this round is and is NOT

**Is:** a subsystem-level Monte Carlo over flight-unit cost using heritage $/kg ranges, CER-anchored subsystem mixes, and DRACO / PPE / FSP-Phase-2 anchors for the nuclear-electric components. Propagates the resulting cost distribution into round-8's two-factor clearing-price model.

**Is NOT:** a full TRANSCOST or NASA Air Force Cost Model run — those require subsystem mass breakdowns and complexity factors I do not have to better than ±50% precision. The Monte Carlo here folds that precision band into the uncertainty rather than pretending to one.

## Component-level arithmetic (pre-registration protocol fix for recurring lesson #7)

Two prior rounds (R3, R4) and again R9 / R10 / R11 / R12 each saw recurring-lesson-7 strikes when arithmetic was skipped at pre-registration. This round computes one reference cell per architecture before freezing falsification bands.

### Heritage anchors (sources documented in `MARKET_ANCHORS.md`)

| Anchor | Total cost (then-year) | Dry mass | $/kg dry (2026$) |
|---|---:|---:|---:|
| Cassini-Huygens (1997 launch) | $3.26B | 2,150 kg | $2.4M/kg |
| Curiosity / MSL (2011) | $2.5B | 900 kg (rover) | $3.1M/kg |
| Europa Clipper (2024) | $5.2B | 3,240 kg | $1.6M/kg |
| Voyager 1/2 (1977) | $865M (1977$) → ~$4B (2026$) | 825 kg | $4.9M/kg |
| Lunar Gateway PPE (60-kW SEP tug) | ~$1.2B total | ~5,000 kg | $0.24M/kg |
| DARPA DRACO (cancelled 2025) | $499M ceiling for flight demo | ~10,000 kg target | $0.05M/kg ceiling |

Range: $0.05M–$4.9M / kg dry. Median anchor near **$2M/kg** for flagship-class flight units; PPE/DRACO suggest commercial-class power-and-propulsion subsystems can be ~10× cheaper per kilogram than flagship-class instruments-and-cameras.

### Reference cell A: Variant B, first-unit cost stack

Variant B per the matrix: ~5.3 t dry, Kilopower-class 10-kWe reactor, chemical Saturn-departure kick stage, bag harvest, no Saturn-side electrolysis (small reactor only feeds housekeeping + electrolyzed-O2 attitude).

| Subsystem | Mass est. | $/kg (heritage anchor) | Subtotal |
|---|---:|---:|---:|
| Reactor (Kilopower 10-kWe + Stirling conv.) | 1.5 t | $200k/kg (extrap from FSP Phase-1 + KRUSTY ground) | $300M |
| Chemical kick stage (engines + tankage) | 0.8 t | $80k/kg (heritage liquid stage) | $64M |
| Bag + harvest mechanism | 0.6 t | $100k/kg (composite + deployable) | $60M |
| Solar panels (Saturn-distance, housekeeping) | 0.1 t | $300k/kg (deep-space grade) | $30M |
| Power management & distribution | 0.3 t | $200k/kg (high-voltage, custom) | $60M |
| Avionics / GNC / comms (DSN-class, Saturn) | 0.4 t | $400k/kg (Cassini-comparable) | $160M |
| Structure + propellant tankage | 1.2 t | $50k/kg (cryogenic structure) | $60M |
| Thermal control | 0.3 t | $150k/kg | $45M |
| Hardware subtotal | 5.2 t | — | **$779M** |
| Integration & test (20% of hardware) | — | — | $156M |
| Program-level overhead (25% on subtotal+I&T) | — | — | $234M |
| **First-unit total** | | | **$1.17B** |

Mid-range first-unit estimate Variant B = **$1.17B**, ~2.3× the $500M placeholder. Sensitivity: ±50% reasonable from CER imprecision plus reactor-line uncertainty.

### Reference cell B: Architecture E_500, first-unit cost stack

Arch E_500 per the matrix: 500 kWe reactor, Brayton conversion, MARVL-class radiator (~3 t at 10 W/kg), ~20-thruster ion array, 200-t chunk capacity. R12 confirmed dry mass ~6 t at 10 W/kg specific power.

| Subsystem | Mass est. | $/kg | Subtotal |
|---|---:|---:|---:|
| Reactor core (500 kWe fission + Brayton conv.) | 1.5 t | $1M/kg (anchored: 50× Kilopower → ~$1.5B per FSP Phase-2 cost class) | $1,500M |
| Power management & distribution (500 kWe class) | 0.4 t | $400k/kg (custom HV, no heritage above 60 kW PPE) | $160M |
| Radiator stack (deployable, MARVL-class) | 2.4 t | $150k/kg (deployable composite) | $360M |
| Thruster array (20× AEPS-class 25 kW, $30M each) | 0.4 t | — (priced as units, not per-kg) | $600M |
| Bag + harvest | 0.6 t | $100k/kg | $60M |
| Avionics / GNC / comms | 0.4 t | $400k/kg | $160M |
| Structure + propellant tankage | 0.8 t | $50k/kg | $40M |
| Thermal control | 0.3 t | $150k/kg | $45M |
| Hardware subtotal | 6.8 t | — | **$2,925M** |
| Integration & test (20%) | — | — | $585M |
| Program-level overhead (25%) | — | — | $878M |
| **First-unit total** | | | **$4.39B** |

Mid-range first-unit estimate Arch E_500 = **$4.39B**, ~15× the $300M placeholder.

Sanity check against PPE: 60 kW SEP tug ~$1.2B. Linear-in-power scaling to 500 kWe (8.3×) → ~$10B; but PPE includes substantial NRE that the ICEBERG ship inherits from FSP / DRACO development as program-level sunk cost, so the per-unit cost is properly lower. $4.4B sits between linear-PPE-extrapolation and DRACO's ceiling. Order-of-magnitude OK.

### Reference cell C: Architecture E_200, first-unit cost stack

Arch E_200 per the matrix: 200 kWe reactor, smaller ship, 30-t chunk. Roughly half the dry mass and half the reactor cost of E_500 at the same $/kW for reactor and same $/unit for thrusters (8 units instead of 20).

| Subsystem | Mass est. | $/kg | Subtotal |
|---|---:|---:|---:|
| Reactor core (200 kWe + Brayton) | 0.8 t | $1M/kg | $800M |
| Power management & distribution | 0.2 t | $400k/kg | $80M |
| Radiator stack | 1.0 t | $150k/kg | $150M |
| Thruster array (8× AEPS at $30M) | 0.16 t | — | $240M |
| Bag + harvest | 0.3 t | $100k/kg | $30M |
| Avionics / GNC / comms | 0.4 t | $400k/kg | $160M |
| Structure + tankage | 0.5 t | $50k/kg | $25M |
| Thermal control | 0.2 t | $150k/kg | $30M |
| Hardware subtotal | 3.6 t | — | **$1,515M** |
| Integration & test (20%) | — | — | $303M |
| Program-level overhead (25%) | — | — | $455M |
| **First-unit total** | | | **$2.27B** |

Mid-range first-unit estimate Arch E_200 = **$2.27B**, ~7.6× the $300M placeholder.

### Recurring-unit cost (Wright's-Law learning, LR 15%) at unit 33

Round 7 found ~33 PV-discounted deliveries in horizon. Wright's-Law factor at unit 33 with LR 15%:
- 33^log2(0.85) = 33^(-0.2345) ≈ 0.467.

Recurring unit cost ≈ first-unit cost × 0.467:
- Variant B: $1.17B × 0.467 ≈ **$547M** (essentially matches R7/R8's $500M placeholder — placeholder appears to have been a *recurring-with-learning* estimate, not first-unit)
- Arch E_500: $4.39B × 0.467 ≈ **$2.05B**
- Arch E_200: $2.27B × 0.467 ≈ **$1.06B**

This is the load-bearing observation: **the R7/R8 placeholders were approximately right *as recurring-with-learning estimates* for Variant B, but the same number for Architecture E was off by ~7×** because Arch E's reactor + radiator + thruster-array stack does not scale down as cheaply as the placeholder assumed.

## Pre-registered hypotheses

| Hypothesis | Predicted | Falsification |
|---|---|---|
| H-bvc-a — Median bottoms-up *first-unit* cost, Variant B | $0.9B–$1.6B (range allows ±35% on $1.17B reference cell) | outside band |
| H-bvc-b — Median bottoms-up *first-unit* cost, Arch E_500 | $3.5B–$5.5B (±25% on $4.39B reference) | outside band |
| H-bvc-c — Median bottoms-up *first-unit* cost, Arch E_200 | $1.8B–$2.8B (±23% on $2.27B reference) | outside band |
| H-bvc-d — Cost ratio E_500 / Variant B at median | 3.0×–5.0× (Arch E has reactor + radiator + thruster-array cost block that Variant B does not) | outside band |
| H-bvc-e — Reactor + power-conversion + thruster array dominate Arch E_500 cost | combined > 55% of first-unit total | combined ≤ 55% |
| H-bvc-f — Cost uncertainty (5th–95th percentile) at architecture level | spread ≥ 3.5× | spread < 3.5× |
| H-bvc-g — Recurring-unit cost (post-NRE, LR 15%, unit 33), Variant B | $400M–$700M (placeholder's neighborhood) | outside band |
| H-bvc-h — Recurring-unit cost, Arch E_500 | $1.5B–$2.5B (5–8× R7/R8 placeholder of $300M with implicit learning) | outside band |
| H-bvc-i — At median bottoms-up *first-unit* cost (no learning), R8 P(NPV+) for Variant B at sov 3% | drops from 51.1% to < 20% | drops to ≥ 20% |
| H-bvc-j — At median bottoms-up *first-unit* cost (no learning), R8 P(NPV+) for Arch E_500 at sov 3% | drops from 42.8% to < 5% | drops to ≥ 5% |
| H-bvc-k — At recurring-unit cost (LR 15%, unit 33), Variant B P(NPV+) at sov 3% LR15 | recovers to > 35% (placeholder was 51.1% — recurring is close to placeholder so curve should be near-original) | < 35% or > 60% |
| H-bvc-l — Recurring-unit cost ordering: Variant B retains strict-dominance over Arch E on P(NPV+) at every WACC × LR combo | yes — both grow but E_500 grows more | falsified if any (WACC, LR) cell has Arch E P(NPV+) ≥ Variant B P(NPV+) |
| H-bvc-m — At corporate 8.7% WACC + bottoms-up *first-unit* cost, no architecture clears P(NPV+) ≥ 20% under any LR ∈ {0%, 10%, 15%, 20%} | yes (corporate WACC was already near-marginal at placeholder) | any LR cell has P(NPV+) ≥ 20% |
| H-bvc-n — Cost / mass elasticity (Arch E_500 vs Arch E_200): cost scales sub-linearly with mass | (E_500 cost / E_200 cost) < (E_500 mass / E_200 mass) i.e. < ~1.9× | ≥ 1.9× |

## Method

### Step 1 — subsystem-level Monte Carlo over first-unit cost

For each architecture (Variant B, Arch E_500, Arch E_200), draw 10,000 samples over the subsystem cost stack. Each subsystem cost is log-normal:
- median: from the reference cell tables above
- 5th / 95th percentile: ±50% (general engineering CER uncertainty) for non-novel subsystems
- 5th / 95th percentile: factor 3 (±200%) for reactor core, thruster array, radiator (no flight heritage above PPE / KRUSTY)

Subsystem draws independent (no covariance). Sum subsystem draws to get hardware subtotal, then apply I&T factor (log-normal 0.20 ± 0.05) and program overhead (log-normal 0.25 ± 0.07) on top.

### Step 2 — Wright's-Law recurring cost

Apply learning curve to first-unit costs. Sweep LR ∈ {0%, 10%, 15%, 20%}. Compute recurring unit cost at unit 33 (round 7 PV-discounted-delivery count).

### Step 3 — propagate to round-8 NPV-positive probabilities

For each architecture × (WACC ∈ {3%, 8.7%}) × (LR ∈ {0%, 10%, 15%, 20%}) × (cost regime ∈ {first-unit, recurring-with-learning}):

- Re-run round-8's two-factor clearing-price Monte Carlo (Starship $/kg × in-space markup), with the cost distribution replacing the placeholder constant.
- Per-sample: cost draw from step 1, clearing-price draw from R8 distribution, revenue/mission = clearing × delivered_mass, fleet-ramp NPV per round 7 formula but with the sampled cost.
- Per architecture × regime: report P(NPV ≥ 0).

### Step 4 — score hypotheses

Mark each H-bvc-* as held / falsified against measured.

## Caveats

- **CER uncertainty.** Subsystem-level cost-estimating-relationships are calibrated against historical flight programs; nuclear-electric components above the FSP Phase-1 power class have no calibrated CER. The $1M/kg used for the 500-kWe reactor and the $30M per thruster come from extrapolation, not from a built unit. The 5th–95th band (factor 3) is wide on purpose to absorb this.
- **No covariance modeling.** Real subsystem cost overruns covary positively (a program that runs over budget on the reactor also runs over budget on integration). Ignoring covariance understates the upper tail.
- **NRE not separately modeled.** First-unit includes NRE bundled into program overhead. Splitting first-unit into recurring + NRE would change the WACC-discounted NPV (NRE concentrated at year 0); doing so is a follow-up.
- **No cost growth over schedule.** Mature aerospace programs systematically overrun by 30–80% (GAO data on Major Defense Acquisition Programs). Not modeled here; folded into the wide reactor / thruster band.
- **Inflation.** All numbers in 2026 dollars; no escalation modeled. ICEBERG is a 23-year build, so this matters but is a tractable correction left for follow-up.

## Decision matrix consequence

If H-bvc-i and H-bvc-j hold, the round-8 P(NPV+) headline ("Variant B 51.1% at sov 3% LR 15%") shifts down. If H-bvc-l holds (strict-dominance survives), the round-8 architectural ordering is preserved. If H-bvc-l falsifies, **the matrix architecture ordering must be re-evaluated**; specifically, if a cheap-cost favorable scenario lets Arch E catch up because its credibility advantage (R6: 4.78% vs 0.78%) outweighs its NPV-probability disadvantage, the joint-expected-value flip from R8 (Arch E_500 2.05% vs Variant B 0.40%) would need re-checking under bottoms-up cost.
