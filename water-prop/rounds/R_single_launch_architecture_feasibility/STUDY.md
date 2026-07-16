# R-single-launch-architecture-feasibility — STUDY.md

**Author:** rhea (worker session, iceberg-rhea-2 branch)
**Date:** 2026-05-15 (latest+8, fourth round this sitting)
**Status:** pre-registration. Tests the launch-count tradeoff surfaced as highest-leverage finding by R-clearing-price-tail-integration-decision-frame (round 11): 1-launch architecture doubles Frame B closure probability (38% vs 17%) but requires harder reactor target.

## Why this round

R-clearing-price-tail-integration-decision-frame found:
- Frame B probability of positive program net-present-value at zero discount, conditional on technical closure, integrated over demand-curve clearing-price distribution: 17% at 3 launches per mission, 38% at 1 launch per mission.
- Launch count is the single highest-leverage architectural cost lever.

**The unanswered question:** does the technology stack that fits a single-Starship-launch architecture actually close at the same conjunction posterior as the round-9 H2a minimum-point? If single-launch architecture requires higher specific power (which my back-of-envelope below shows), then the conjunction multiplier drops — and Frame A's full-chain probability of positive net-present-value may DROP at single-launch even though Frame B's conditional probability rises. The tradeoff is decision-frame-dependent.

## Back-of-envelope: mass-to-low-Earth-orbit budget

From R-specific-power-cliff `best_at_25yr` table at chunk=200 tonnes, specific impulse 2934 seconds, reactor 500 kilowatts-electric:

| specific power (watts per kilogram) | tug dry mass (tonnes) | outbound propellant (tonnes) | total mass to low-Earth-orbit (tonnes) |
|---:|---:|---:|---:|
| 5  | 115.3 | 206.9 | 322.2 |
| 6  |  97.0 | 174.1 | 271.1 |
| 7  |  84.0 | 150.6 | 234.6 |
| 8  |  74.2 | 133.0 | 207.2 |
| 9  |  66.5 | 119.3 | 185.8 |
| 10 |  60.4 | 108.4 | 168.8 |

Scaling: tug mass × specific power ≈ 593 tonnes-watts per kilogram (slowly increasing, near-constant). Outbound mass ratio is constant at 2.794 (Tsiolkovsky for outbound 29.57 kilometres per second at specific impulse 2934 seconds). Therefore:

**m_LEO ≈ (593 / specific_power) × 2.794 ≈ 1656 / specific_power tonnes** (at specific impulse 2934 seconds, chunk 200 tonnes, reactor 500 kilowatts-electric).

**Note:** chunk mass does not appear in mass-to-Earth-orbit because the chunk is rendezvous'd at Saturn rings (not launched from Earth). Inbound propellant (158 tonnes at H2a baseline) is sourced from chunk-water electrolysis at Saturn (also not launched). Only the tug (reactor + radiator + structure) and outbound propellant are Earth-launched.

### Single-Starship launch budget

Starship payload to low-Earth-orbit: 150 tonnes (mid of current ~100 and target ~150). Single-launch threshold:

**single-Starship feasibility: m_LEO ≤ 150 tonnes**

Solving: specific power ≥ 1656 / 150 = **11.04 watts per kilogram** at specific impulse 2934 seconds.

This is above the round-9 H2a minimum-point (8 watts per kilogram) and above the R-specific-power-cliff data's upper edge (10 watts per kilogram). The conjunction posterior on a reactor program delivering 11 watts per kilogram is harder than 8 watts per kilogram by the conditional-prior ladder (P(≥10) = 0.10 → P(≥11) ≈ 0.07).

### Specific-impulse lift as alternative lever

At fixed specific power 8 watts per kilogram (round-9 H2a), m_tug = 74.15 tonnes. Mass-to-Earth-orbit scales with mass ratio = exp(29570 / (specific impulse × 9.81)):

| specific impulse (seconds) | mass ratio | m_LEO at sp=8 (tonnes) | single-launch fit? |
|---:|---:|---:|---|
| 2934 (current MET cathode anchor) | 2.79 | 207 | no |
| 3500 | 2.37 | 175 | no |
| 4000 | 2.13 | 158 | borderline |
| 4500 | 1.95 | 145 | yes |
| 5000 | 1.83 | 136 | yes |

Specific impulse lift requires either advanced microwave-electrothermal-thruster cathode life beyond water-plasma anchor (titan R-cathode-life-water-plasma surfaced erosion concerns above 3000 s) or a different thruster (Hall-effect at ~3000 s, gridded ion at 4000–5000 s with non-water propellant, or VASIMR-class). All are technology-program contingent.

### Joint specific-power × specific-impulse trade

A single-launch fit exists at lower specific power if specific impulse rises. Pre-registered joint trade space:

| specific impulse | minimum specific power for single-launch |
|---:|---:|
| 2934 (water-plasma microwave electrothermal thruster) | 11.0 |
| 3500 | 9.3 |
| 4000 | 8.1 |
| 4500 | 7.3 |
| 5000 | 6.6 |

The 8 watts per kilogram × 2934 second baseline (round-9 H2a) fits 1.4 Starships per mission; the 10 watts per kilogram × 3500 second point fits 0.95 Starships per mission (single-launch achievable).

## Pre-registered hypotheses

### H1 — single-Starship feasibility threshold

| | predicted | falsification |
|---|---|---|
| H1 | Single-Starship architecture (≤150 tonnes to low-Earth-orbit) requires either specific power ≥ 11 watts per kilogram at conservative specific impulse 2934 seconds, OR specific impulse ≥ 4500 seconds at conservative specific power 8 watts per kilogram, OR joint reduction. Joint relation: m_LEO = 593 × (specific impulse mass ratio) / specific power. | falsified if single-launch fits at specific power ≤ 9 W/kg AND specific impulse ≤ 3000 s (would indicate I miscalculated tug-scaling) |

### H2 — two-Starship architecture closes at conservative anchors

Round-9 H2a baseline at specific power 8 watts per kilogram, specific impulse 2934 seconds gives m_LEO = 207 tonnes. Two Starships at 150 tonnes each give 300 tonnes budget. Closes comfortably.

| | predicted | falsification |
|---|---|---|
| H2 | Two-Starship architecture (≤300 tonnes to low-Earth-orbit) accommodates round-9 H2a baseline at conservative anchors with 31% mass margin | falsified if H2a baseline exceeds 300 tonnes (would indicate I'm missing a mass component) |

### H3 — conjunction posterior at single-launch minimum-point

At specific power 11 watts per kilogram, lifetime 10 years, no aerocapture, uniform prior:
- P(US fission orbit by 2035, uniform) = 0.089
- P(delivers ≥ 11 W/kg | flies) ≈ 0.07 (linearly interpolated between round-9 priors: 0.10 at 10 W/kg, 0.03 at 20 W/kg)
- P(delivers ≥ 10 yr lifetime | flies) = 0.30
- Joint reactor posterior = 0.089 × 0.07 × 0.30 = **0.187%** (vs round-9 H2a's 0.667% at 8 W/kg)

| | predicted | falsification |
|---|---|---|
| H3 | Conjunction posterior at single-launch min-point (11 W/kg, 10 yr, no aerocapture, uniform prior) is in [0.10%, 0.30%]; central 0.19%. 3× lower than round-9 H2a's 0.67%. | falsified if outside range |

### H4 — Frame B at single-launch minimum-point

Per-mission cost at 1 launch, ship reuse 15, ship CapEx $0.65 billion: ($0.65 / 15) + (1 × $0.30) = $0.343 billion.

Delivered mass at specific power 11 watts per kilogram: extrapolating cliff trend (sp=10 → 49.95 tonnes; sp=9 → 46.43; sp=8 → 42.04 — ~3.5 tonnes per watts-per-kilogram), at sp=11 → ~53 tonnes.

Break-even clearing price = $0.343 billion / 53 tonnes = **$6.47 million per tonne**.

P(clearing price ≥ $6.47 million per tonne) under log-normal demand-curve fit (mu_log10 = 3.72, sigma_log10 = 0.66):
- log10($6470 per kg) = 3.81
- z = (3.81 - 3.72) / 0.66 = 0.14
- P(Z ≥ 0.14) ≈ **0.44 (44%)**

| | predicted | falsification |
|---|---|---|
| H4 | Frame B (conditional + price-tail-integrated) at single-launch min-point is in [40%, 50%]; central 44% | falsified if outside, or if Frame B at single-launch is below Frame B at 3-launch (17%) |

### H5 — full-chain Frame A tradeoff

Full-chain P(positive net-present-value) at single-launch min-point:
- 1-launch: conjunction posterior × Frame B = 0.187% × 44% = **0.082%**
- 3-launch (round-9 H2a baseline): conjunction × Frame B = 0.667% × 17% = **0.114%**

**Frame A is LOWER at single-launch** despite higher Frame B. The conjunction multiplier dominates the launch-count gain.

| | predicted | falsification |
|---|---|---|
| H5 | Full-chain P(positive net-present-value) at single-launch min-point (0.08%) is LOWER than at 3-launch round-9 H2a baseline (0.11%) by ~30%. Tradeoff is decision-frame-dependent. | falsified if Frame A at single-launch exceeds Frame A at 3-launch (which would mean Frame B doubling beats conjunction-multiplier tightening) |

### H6 — decision rule for project owner

The launch-count decision is not architecture-independent; it depends on which decision frame the funding stakeholder uses:

- **Under Frame A** (full-chain return-seeking expected value): pursue 3-launch architecture (higher conjunction posterior).
- **Under Frame B** (conditional on reactor + engineering, sovereign-bond underwriter): pursue 1-launch architecture (higher Frame B; the sovereign-grant funds the reactor program separately, so conjunction multiplier is borne by the grant).
- **Under Frame C** (conditional + point estimate): both architectures are ruled out at point-estimate BEST_CELL clearing price.

The decision rule maps directly to funding stakeholder identity.

| | predicted | falsification |
|---|---|---|
| H6 | Launch-count optimum decision is decision-frame-dependent: 3-launch wins under Frame A, 1-launch wins under Frame B. Project-owner pitch posture should be Frame-aware. | falsified if one architecture dominates under both frames |

---

## Method (run.py)

1. Verify back-of-envelope scaling against R-specific-power-cliff `best_at_25yr` data (compute m_tug × specific_power across the 5–10 watts-per-kilogram range).
2. Compute m_LEO(specific power, specific impulse) joint trade surface.
3. Identify single-launch minimum-point (≤150 tonnes), two-launch minimum-point (≤300 tonnes), three-launch minimum-point (≤450 tonnes).
4. Apply round-9 conjunction-posterior priors to compute reactor posterior at each minimum-point.
5. Apply round-11 log-normal demand-curve fit to compute Frame B probability at each minimum-point.
6. Tabulate Frame A and Frame B per launch-count.
7. Grade H1-H6.

Output: `results/launch_count_tradeoff.json`, `results/launch_count_tradeoff_table.csv`, `results/findings.md`.

---

## Validity caveats

1. **Linear extrapolation of conditional prior P(delivers ≥ specific power | flies) beyond 10 watts per kilogram.** Anchored at 0.10 (10 W/kg) and 0.03 (20 W/kg) from round-9 priors. The interpolated 0.07 at 11 W/kg is a guess; could be 0.05 or 0.10. Sensitivity: factor-of-2 swing on 11 W/kg conditional moves H3 posterior by 2× (range 0.10% to 0.37%) which is inside the predicted H3 band.

2. **Extrapolation of m_LEO scaling beyond 10 W/kg.** The constant m_tug × specific_power ≈ 593 trend is slowly increasing (576 at 5 W/kg → 604 at 10 W/kg). Extrapolation to 11 W/kg may overstate the m_tug saving slightly; this only tightens H1, doesn't falsify it.

3. **Starship payload 150 tonnes is a target, not a measurement.** Current Starship has demonstrated lower (Q1 FY2026 successful flights at ~100-tonne payload). If the demonstrator window slips beyond Starship Block 2 maturity, 100 tonnes may be the binding constraint, lifting the single-launch specific-power requirement to 1656/100 = 16.6 watts per kilogram. **This makes single-launch architecture more conjunction-fragile.**

4. **Chunk mass not in m_LEO is load-bearing.** This rests on chunk-rendezvous-at-Saturn-rings (axis 19 held). If the architecture were to ship chunk material from Earth (e.g. rendezvous fails, backup chunk launched), single-launch becomes structurally infeasible at any specific power.

5. **Specific impulse 4500 seconds requires non-water propellant** (water-plasma microwave electrothermal thruster cathode-life concerns above ~3000 seconds per titan-2). Switching propellant means losing chunk-water-as-inbound-propellant lever — which is the architectural cost lever per project-owner direction (axis 19 ram-scoop retirement reasoning). **Specific-impulse-lift path may be structurally incompatible with chunk-water-as-propellant.** Worth flagging but not pre-registering.

6. **Frame B at single-launch (44%) is anchored on log-normal fit to demand curve.** Round-11 fit validated at p25/p75 within 3%; extrapolation to lower break-even price ($6.47 million per tonne, near demand-curve p50 of $5.28 million per tonne) is well-supported by the fit.

7. **Single-launch architecture cost savings carries through to lower NRE** in principle (simpler integration, fewer interfaces). Not modeled here — would tighten Frame B further but not change H5 verdict.
