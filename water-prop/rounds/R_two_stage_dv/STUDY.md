# R-two-stage-dv — does a chemical Saturn-departure stage relax the inbound-electric requirement?

**Status:** pre-result.

## Question

R-design-envelope assumed a single-stage architecture: one electric thruster does the entire 6.42 km/s inbound residual (post-lunar-flyby) propulsive delta-v. That assumption forced the η = 0.9 cell into water dual-ion territory (≥6000 s specific impulse, technology readiness level 1–2) and pushed the η = 0.8 cell into 200–400 kilowatt-electric power.

A two-stage architecture — high-thrust chemical impulsive burn at Saturn departure, followed by low-thrust electric cruise — splits the delta-v budget. Chemical absorbs some delta-v at low specific impulse but with the impulsive-burn advantage that no time is needed. Electric absorbs the rest at high specific impulse over years.

The question: at what split does the inbound electric requirement collapse into water-Hall or water-radio-frequency-ion territory (technology readiness level 5–7, sub-megawatt-electric power)? And does the cost of carrying chemical propellant from Earth out to Saturn dominate the savings?

## Pre-registered hypothesis (H-2s)

**Aggregate (H-2s-agg):** A modest chemical offload (1.5–3 km/s) at hypergolic specific impulse (~320 s) pulls the η = 0.7–0.8 cell out of water radio-frequency ion territory and into water-Hall territory, and pulls η = 0.9 from water dual-ion into water radio-frequency ion. The chemical propellant mass becomes prohibitive above ~3 km/s of offload (chemical propellant mass exceeds chunk mass for hypergolic; the outbound launch penalty becomes the binding constraint). The optimum chemical share is therefore in the 1.5–3 km/s band, and the two-stage architecture earns its keep primarily at η ≥ 0.8 — for η ≤ 0.7 the all-electric architecture is already adequate.

**Pre-registered sub-claims:**

| Sub-claim | Predicted | Falsification |
|---|---|---|
| H-2s-a — Required electric specific impulse at η=0.7, chemical offload = 2 km/s, hypergolic chem | 1100–1500 s (water-Hall band) | outside ±15% |
| H-2s-b — Required electric specific impulse at η=0.9, chemical offload = 4 km/s, hypergolic chem | 2200–2800 s (water radio-frequency ion band) | outside ±15% |
| H-2s-c — Chemical-propellant-mass to chunk-mass ratio at chemical offload = 4 km/s, hypergolic | ≥ 1.5 (chemical prop exceeds chunk by ≥50%) | outside ±20% |
| H-2s-d — Optimum chemical offload for minimum required electric specific impulse subject to chem-prop ≤ chunk-mass | 1.5–3 km/s | outside that band |
| H-2s-e — All-electric remains adequate for η ≤ 0.7 (water-Hall covers it) | yes | falsified if all-electric required electric specific impulse for η=0.7 exceeds 2000 s (it was 1835 s in R-design-envelope) |
| H-2s-f — Switching chemical from hypergolic to cryogenic methalox (specific impulse 360 → 320 s gain to 360 s) reduces chemical propellant mass by ~10–15% at fixed offload | yes | outside ±30% |

**Aggregate decision:** if H-2s-d holds, **the recommended architecture for η ≥ 0.8 cells is two-stage: 2 km/s hypergolic + 4.42 km/s electric.** This is a meaningful update to the campaign's prior conops (which had electric doing the entire inbound residual). It also reopens the question of whether to carry hypergolic propellant from Earth or to electrolyze ring water in situ (a much bigger engineering ask, deferred).

## Method

Pure algebra, same as R-design-envelope. No trajectory integration.

For each cell (η, chunk, delta-v_chem, specific-impulse_chem):

```
delta_v_elec      = 6.42 km/s − delta_v_chem
v_e_chem          = Isp_chem × g₀
v_e_elec_required = −delta_v_elec / ln(η)
Isp_elec_required = v_e_elec_required / g₀

# Chemical propellant carried at Saturn-departure (dry stage mass neglected)
# Starting wet mass at Saturn-depart = chunk + M_chem_prop
# After chemical burn, drop chemical stage; remaining mass = chunk
# Rocket equation: chunk = (chunk + M_chem_prop) × exp(−delta_v_chem / v_e_chem)
# Solving:
M_chem_prop = chunk × (exp(delta_v_chem / v_e_chem) − 1)

# Electric propellant from chunk
m_prop_elec_kg = chunk × (1 − η)

# Electric stage delivers η fraction of chunk after chemical stage
delivered_chunk = chunk × η

# Required electric thrust at tau_burn = 5 yr (same convention as R-design-envelope)
F_elec = m_prop_elec_kg × v_e_elec_required / tau_burn

# Required electric jet power and electrical power (auto-select thruster class by Isp band)
P_jet = F_elec × v_e_elec_required / 2
P_electrical = P_jet / eta_thruster_class
```

**Sweep axes:**

- Delivered fraction η ∈ {0.5, 0.6, 0.7, 0.8, 0.9}
- Grappled chunk M ∈ {50, 100, 200, 350, 500} tonnes (drop the small-chunk corner where dry-mass-neglect dominates)
- Chemical offload delta-v_chem ∈ {0, 1, 2, 3, 4, 5} km/s
- Chemical specific impulse Isp_chem ∈ {320, 360, 450} s — hypergolic (monomethyl hydrazine / nitrogen tetroxide), cryogenic methalox, cryogenic hydrolox

= 5 × 5 × 6 × 3 = 450 cells.

**Validity caveats:**

- Dry mass neglected for both chemical and electric stages. Chemical-stage dry-to-wet ratio is typically 0.10–0.15; this is an additional 10–15% propellant burden not captured.
- Cryogenic methalox over a 13-year cruise is currently technology readiness level 4–5; long-duration cryogenic storage is its own unsolved problem (boil-off rates, zero-boil-off active-cooling mass). Hypergolic storable over 13 years is technology readiness level 9 (flight heritage on Cassini, New Horizons, etc.). The "specific impulse 320 vs 360 vs 450" sweep is best read as "which propellant chemistry, conditional on having solved the storage problem."
- Outbound launch penalty for carrying chemical propellant to Saturn is not modeled here. Order of magnitude: at outbound specific impulse 2000 s electric and 9 km/s outbound delta-v, delivering 1 tonne of chemical propellant to Saturn requires ~1.6 tonnes at Earth low-orbit departure. Flagged in the result interpretation.
- Constant chemical specific impulse (no thrust-tail-off, no chamber-pressure droop). Real impulsive burns have ~5% specific-impulse penalty from non-ideal expansion.
- Single-burn chemical (one big impulsive maneuver at Saturn-departure periapsis). A multi-burn architecture (e.g., periapsis raise then plane change) might split chemical further but is out of scope here.
- All other R-design-envelope caveats still apply: duty cycle implicit, no aerocapture, no silicate contamination, lunar tour delta-v as point estimate.

## Result

### Required electric specific impulse (s) by (delivered fraction × chemical delta-v offload)

Total inbound delta-v = 6.42 km/s. Chemical specific impulse is irrelevant for this table — it only affects how much propellant is carried.

| η | Δv_chem = 0 | 1 km/s | 2 km/s | 3 km/s | 4 km/s | 5 km/s |
|---:|---:|---:|---:|---:|---:|---:|
| 0.5 |  944 |  797 |  650 |  503 |  356 |  209 |
| 0.6 | 1282 | 1082 |  882 |  683 |  483 |  283 |
| 0.7 | 1835 | 1550 | 1264 |  978 |  692 |  406 |
| 0.8 | 2934 | 2477 | 2020 | 1563 | 1106 |  649 |
| 0.9 | 6214 | 5246 | 4278 | 3310 | 2342 | 1374 |

### Hypergolic chemical-propellant mass (tonnes) by (chunk × chemical delta-v offload), Isp_chem = 320 s

Ratio in parentheses is chemical-propellant-mass / chunk-mass.

|  chunk | Δv_chem = 0 | 1 km/s | 2 km/s | 3 km/s | 4 km/s | 5 km/s |
|---:|---:|---:|---:|---:|---:|---:|
|  50 t | 0 |  19 (0.38×) |  45 (0.89×) |  80 (1.60×) | 129 (2.58×) |  196 (3.92×) |
| 100 t | 0 |  38 (0.38×) |  89 (0.89×) | 160 (1.60×) | 258 (2.58×) |  392 (3.92×) |
| 200 t | 0 |  75 (0.38×) | 178 (0.89×) | 320 (1.60×) | 515 (2.58×) |  784 (3.92×) |
| 350 t | 0 | 131 (0.38×) | 312 (0.89×) | 560 (1.60×) | 902 (2.58×) | 1372 (3.92×) |
| 500 t | 0 | 188 (0.38×) | 446 (0.89×) | 801 (1.60×) | 1289 (2.58×) | 1960 (3.92×) |

The chem-to-chunk ratio crosses 1.0 between Δv_chem = 2 and 3 km/s for hypergolic. Above that, the chemical propellant outweighs the chunk being returned.

### Optimum chemical delta-v offload per delivered-fraction target, chunk = 100 t, constraint chem ≤ chunk

| η | chemistry | optimum Δv_chem | electric Isp required | thruster class | chem/chunk | electric power |
|---:|---|---:|---:|---|---:|---:|
| 0.5 | hypergolic | 2 km/s |  650 s | microwave-electrothermal | 0.89 |  21 kWe |
| 0.5 | methalox | 2 km/s |  650 s | microwave-electrothermal | 0.76 |  21 kWe |
| 0.5 | hydrolox | 3 km/s |  503 s | microwave-electrothermal | 0.97 |  13 kWe |
| 0.6 | hypergolic | 2 km/s |  882 s | microwave-electrothermal | 0.89 |  32 kWe |
| 0.6 | hydrolox | 3 km/s |  683 s | microwave-electrothermal | 0.97 |  19 kWe |
| 0.7 | hypergolic | 2 km/s | 1264 s | water-Hall | 0.89 |  27 kWe |
| 0.7 | hydrolox | 3 km/s |  978 s | microwave-electrothermal | 0.97 |  29 kWe |
| 0.8 | hypergolic | 2 km/s | 2020 s | water-radio-frequency-ion | 0.89 |  38 kWe |
| 0.8 | hydrolox | 3 km/s | 1563 s | water-Hall | 0.97 |  27 kWe |
| 0.9 | hypergolic | 2 km/s | 4278 s | water-dual-ion | 0.89 | 101 kWe |
| 0.9 | hydrolox | 3 km/s | 3310 s | water-dual-ion | 0.97 |  61 kWe |

### Hypothesis grading

| Sub-claim | Predicted | Actual | Held? |
|---|---|---|---|
| H-2s-a — Electric Isp @ η=0.7, Δv_chem=2 km/s, hypergolic | 1100–1500 s | 1264 s | held |
| H-2s-b — Electric Isp @ η=0.9, Δv_chem=4 km/s, hypergolic | 2200–2800 s | 2342 s | held |
| H-2s-c — Chem/chunk ratio @ Δv_chem=4 km/s, hypergolic | ≥ 1.5 | 2.58× | held |
| H-2s-d — Optimum Δv_chem subject to chem ≤ chunk | 1.5–3 km/s | 2 km/s (hypergolic, methalox); 3 km/s (hydrolox) | held |
| H-2s-e — All-electric adequate at η ≤ 0.7 (water Hall) | yes | partially — η=0.7 needs water radio-frequency ion all-electric (1835 s), not Hall. With Δv_chem = 1 km/s it drops into Hall. | partially falsified (technology-band off by one tier; spirit holds) |
| H-2s-f — Methalox cuts chem propellant by 10–15% vs hypergolic at fixed offload | yes | 14.6% reduction @ Δv_chem=2 km/s | held |

## Reading

**The headline finding:** a 2 km/s hypergolic chemical offload (technology readiness level 9, flight-heritage on Cassini and New Horizons) collapses the inbound-electric power requirement by 3–5× across the (η = 0.5–0.8, chunk = 100 t) region. At η = 0.8 specifically, required electric power drops from 161 kilowatt-electric (all-electric, R-design-envelope) to 38 kilowatt-electric. That is the difference between needing a Fission Surface Power stretch reactor and needing Kilopower-class fission.

**Five observations the result actually supports:**

1. **The two-stage architecture earns its keep at η = 0.7–0.8.** Below η = 0.7 the all-electric architecture is already in the water-radio-frequency-ion / water-Hall band — adding a chemical stage is over-engineering. Above η = 0.8, even with chemical offload the electric stage stays in water-dual-ion territory (technology readiness 1–2). **The sweet spot is η = 0.8 with 2 km/s hypergolic offload.**

2. **Two km/s is the structural ceiling for chemical offload.** At hypergolic specific impulse, chemical propellant mass equals chunk mass at 2.2 km/s. Above that, you are carrying more hypergolic than chunk you bring home — the architecture inverts and the outbound launch penalty dominates. Cryogenic hydrolox stretches the ceiling to ~3 km/s but introduces 13-year cryogenic storage as an unsolved subsystem (technology readiness 4–5 at this duration).

3. **The η = 0.9 cell is not rescuable by chemistry.** Even at 4 km/s hypergolic offload (chem/chunk = 2.58×), the electric stage still needs 2342 s — water radio-frequency ion class. The structural problem is that a 90% delivered fraction at any reasonable inbound delta-v demands specific impulse north of 2300 s, and the only way to drop that further is to drop delta-v itself (aerocapture or more aggressive lunar tour). **The campaign should drop η = 0.9 as a design target unless aerocapture becomes available.**

4. **The outbound launch penalty is not free.** A 100-tonne-chunk mission with 2 km/s hypergolic offload requires 89 tonnes of hypergolic at Saturn-departure. Carrying that to Saturn on electric outbound (2000 s, 9 km/s) requires roughly 140 tonnes at Earth low-orbit *just for the chemical stage*. Plus the outbound electric propellant, plus the tug + reactor + chemical-stage dry mass. Per-mission Earth-launch mass roughly doubles vs all-electric. At Starship-floor launch cost (~$1k/kg to low Earth orbit) that is ~$140 million of launch cost per mission attributable to the chemical stage. Whether the avoided reactor mass and shorter cycle pay for that is a discounted-cash-flow question, not a propulsion question — and is the natural next round.

5. **The hypothesis I got wrong was H-2s-e.** I predicted all-electric at η = 0.7 would land in the water-Hall band; it actually lands in the water-radio-frequency-ion band (1835 s). The technology-readiness gap between water-Hall (5–7) and water-radio-frequency-ion (6–7 for Pale-Blue-class) is small, so the practical impact is minor, but the error is exactly the kind of "off-by-one technology tier" that the memory note on `Cost if uncorrected` warns about. Recorded in the revisit log.

**What this round still assumes, by way of continuing the meta-critique:**

- **Outbound launch penalty quantified but not optimized.** I computed it for the reading but did not let it drive sizing. A full economic round should price launch + propellant + reactor jointly.
- **Aerocapture still off the table.** If aerocapture works, 2–5 km/s of inbound delta-v becomes free and this entire two-stage exercise is partly redundant. The combined "chemical Saturn-departure + aerocapture at Earth" architecture would collapse the inbound electric delta-v to 1–2 km/s, where every η cell lands in microwave-electrothermal territory. That is potentially a much bigger lever than two-stage alone.
- **Silicate contamination still ignored.** The η = 0.8 winner cell uses water radio-frequency ion at 2020 s. If silicate contamination forces a switch to silicate-tolerant water-microwave-electrothermal, η = 0.8 becomes unachievable regardless of chemical offload.
- **Saturn-departure chemical stage is dry-mass-free in this model.** Real hypergolic stages run dry-to-wet ~0.10–0.15. The actual electric requirement after the chemical burn would degrade by ~10% across the board.
- **The chemical burn is single-impulse.** Multi-burn strategies (periapsis kick + plane change) might split the chemical efficiency loss differently.

## Post-result correction (2026-05-14)

**The Reading above is misleading without the outbound-mass correction below.**

This round modeled only the inbound-electric power and specific-impulse requirements. It did **not** model the cost of carrying chemical propellant from Earth to Saturn. When that cost is added, the "two-stage earns its keep at η = 0.7–0.8" headline does not survive on a delivered-water-per-launch-mass basis.

End-to-end mass accounting at a 100 t chunk reference:

| Architecture | At low Earth orbit | Delivered water | Delivered / launch mass |
|---|---:|---:|---:|
| All-electric, water radio-frequency ion at 2934 s (R-design-envelope baseline, η = 0.8 target) | ~38 t | ~75 t | **1.98** |
| Carried-hypergolic two-stage (this round's headline architecture) | ~185 t | ~80 t | **0.43** |
| Variant B — chunk-fed chemical (electrolyze chunk water at Saturn for the chemical burn) | ~35 t | ~42 t | **1.20** |

The carried-hypergolic architecture has the **worst** delivered-per-launched-mass ratio of the three: 4.5× more expensive per delivered tonne than all-electric. The reactor-class savings on the inbound do not pay for the outbound launch penalty.

**Corrected conclusion:** the carried-hypergolic two-stage architecture earns its keep **only in reactor-era cells where all-electric is power-infeasible** — i.e., early-program cells (Kilopower / Fission Surface Power era) where the megawatt-class reactor is not yet flying and all-electric cannot supply the ~160 kilowatt-electric the single-stage water radio-frequency ion approach needs. In steady-state cadence (megawatt-class reactor available), all-electric wins on every metric that matters. **Two-stage is an early-era bridge architecture, not a long-term design target.**

The chunk-fed Variant B is the structurally cheaper version of two-stage on launch mass (lightest at low Earth orbit of the three) but pays for the chemical impulse by depleting the chunk. It is the topic of the follow-on round R-chunk-fed-chemical.

## Revisit clause

H-2s-a through H-2s-d held; H-2s-e partially falsified (recorded as a "technology-band-off-by-one" calibration error); H-2s-f held. Aggregate H-2s-agg held *only in the narrow inbound-power-and-specific-impulse sense*; **falsified on delivered-per-launch-mass** once outbound mass is accounted for. Lesson: forward-design rounds in this campaign have a habit of modeling one leg in isolation; outbound mass must be included in any architecture trade going forward.

**Next-round candidates surfaced by this round:**
- **R-chunk-fed-chemical (Variant B):** map the (reactor-era × delivered-fraction) plane explicitly. Identify cells where chunk-fed chemical beats both all-electric and carried-hypergolic. **Triggered.**
- **R-aerocapture-revisit:** verify whether aerocapture at Earth is actually ruled out, or just assumed away. Potential 2–5 km/s of free delta-v on the inbound.
- **R-silicate-tolerance:** enforce the silicate contamination constraint and see whether the η = 0.8 winner survives.


## Revisit clause

Grade H-2s-a through H-2s-f against numeric outputs. If H-2s-d holds (optimum chemical offload in 1.5–3 km/s band), the next round candidate is a full economic comparison — outbound launch cost + chemical procurement + reduced reactor mass — to settle whether the two-stage architecture beats all-electric on net-present-value per launch.
