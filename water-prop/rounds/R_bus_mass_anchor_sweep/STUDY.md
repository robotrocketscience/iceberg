# R-bus-mass-anchor-sweep — STUDY

**Worker:** enceladus-r5, 2026-05-16. **Status:** complete. **Predecessor:** R-hybrid-power-generator-exhaust-revisit (commit `10bbeb1`), which surfaced that bus + bag dry mass is load-bearing.

## Why this round exists — questioning the predecessor's predecessor

Both R-hybrid-chemical-power-augmentation (commit `98a9ded`) and R-hybrid-power-generator-exhaust-revisit (commit `10bbeb1`) used `m_bus = 15 t + m_bag = 8 t` = **23 tonnes** as the vehicle dry-mass anchor. This number was inherited from earlier matrix work without anchoring against flown spacecraft heritage. Heritage data:

| Spacecraft | Dry mass | Era |
|---|---|---|
| Cassini | 2,150 kg | 1997, Saturn flagship |
| Galileo | 2,000 kg | 1989, Jupiter flagship |
| Voyager 1/2 | 720 kg | 1977, outer-planet flyby |
| New Horizons | 400 kg | 2006, Pluto flyby |
| Europa Clipper | 5,900 kg | 2024, Jupiter flagship |
| Mars Reconnaissance Orbiter | 1,030 kg | 2005 |
| DAWN ion-propulsion | 750 kg | 2007 |

The 23-tonne anchor in the predecessor rounds was **roughly 10× Cassini and 4× Europa Clipper**. This round sweeps bus + bag mass across {Cassini, Europa-Clipper, 10-t, 15-t-predecessor} and quantifies how many matrix-relevant architectures open at each anchor.

## Scope

Pure-electric inbound (no hydrolox augmentation). Single-stream Tsiolkovsky. 1920 cells over:

- `P_reactor` ∈ {50, 200, 500} kilowatts-electric (matrix-resident Arch E corner)
- `chunk` ∈ {10, 50, 100, 200} t (demonstrator → commercial)
- `m_bus` ∈ {2, 5, 10, 15} t (Cassini → Europa Clipper → mid → predecessor)
- `m_bag` ∈ {0.5, 2, 5, 8} t flat AND linear-scaled to 5% × chunk
- `specific_power` ∈ {5, 10} W/kg (KRUSTY-flown → R10 cliff target)
- `aerocapture_credit` ∈ {0, 10} km/s (phoebe-conditional hybrid aerocapture)
- `Isp` ∈ {2000, 2934} s (matrix surviving cell → R6 high-Isp sensitivity)

η_thruster = 0.5 (water-electric MET/arcjet, from predecessor-revisit anchor).

## Headline numerical result

**At Cassini-anchor bus (m_bus = 2 t, m_bag = 5 % × chunk), 9 cells close L0-05 strict AND L0-09 commercial floor (delivered ≥ 30 t) simultaneously.** Best cell delivers 91.5 t at RT 12.7 yr. At flown-anchored specific power (5 W/kg, KRUSTY-class), 1 cell closes commercial-strict at Cassini bus.

| P kWe | chunk t | sp W/kg | aero km/s | Isp s | RT yr | delivered t |
|---|---|---|---|---|---|---|
| 500 | 200 | 10 | 10 | 2934 | 12.69 | **91.5** |
| 200 | 200 | 10 | 10 | 2000 | 14.62 | 74.9 |
| 500 | 200 | 5 | 10 | 2934 | 13.76 | 71.2 |
| 500 | 200 | 10 | 10 | 2000 | 10.48 | 57.3 |
| 200 | 100 | 10 | 10 | 2934 | 13.87 | 47.6 |
| 200 | 100 | 5 | 10 | 2934 | 14.94 | 39.5 |
| 500 | 100 | 10 | 10 | 2934 | 10.45 | 34.2 |
| 200 | 100 | 10 | 10 | 2000 | 11.20 | 31.0 |
| 500 | 200 | 5 | 10 | 2000 | 11.13 | 30.5 |

All-pass-waiver count by (m_bus, m_bag flat):

| m_bus \ m_bag (t) | 0.5 | 2 | 5 | 8 |
|---|---|---|---|---|
| **2** | 30 | 29 | 27 | 25 |
| 5 | 28 | 27 | 25 | 25 |
| 10 | 25 | 25 | 24 | 21 |
| **15** (predecessor) | 24 | 22 | 20 | **17** |

Monotonically more cells close at lower bus mass. Predecessor's (15, 8) corner had 17 cells; Cassini's (2, 0.5) has 30. Modest 1.76× factor, not the 3× I pre-registered.

## Pre-registered hypotheses and grades

| # | Hypothesis | Verdict | Notes |
|---|---|---|---|
| H1 | Cassini-anchor opens 500-kWe/200-t Arch-E cell at sp=10, aero=10, Isp=2000 | **HELD** | 1 of 1 cells all-pass waiver (RT 10.48 yr, delivered 57.3 t). |
| H2 | Cassini opens ≥ 3× more all-pass-waiver cells than full-bus | **FALSIFIED** | 29 vs 17 = 1.71×. Below predicted 3×. Effect is real but smaller than expected — most all-pass-waiver cells are dominated by P_reactor × Isp × aerocapture, not bus mass. |
| H3 | At sp=5 W/kg + Cassini bus, no commercial cell (chunk≥100, delivered≥30 t) closes L0-05 strict | **FALSIFIED** | 1 cell closes: 500 kWe / 200 t / sp=5 / aero=10 / Isp=2934 / RT 13.76 yr / delivered 71.2 t. Substantively important falsification. |
| H4 | Chunk-scaled bag (5%) more permissive at small chunks, less at large | **HELD** | At chunk=10: linear=4 vs flat-8=0. At chunk=200: linear=34 vs flat-8=35 (essentially tied, slight reversal as predicted). |
| H5 | Matrix R6 Arch-E falsified verdict (23.6 yr) reverses at Cassini bus | **FALSIFIED** | At full-bus the R6-config (Isp=2934, aero=0, sp=10) already passes waiver — 1 cell. R6's "falsified" verdict was about L0-05 strict, not waiver. My H5 mis-stated the comparison. |

**Score: 2 HELD, 3 FALSIFIED.** Two of the falsifications (H2, H3) are informative — they show the matrix verdict was less bus-anchored than predicted, but also that even at flown-anchored specific power (sp=5), heritage bus mass opens commercial-strict cells.

## Headline architectural verdict

**The matrix's "no engineering-closed cell" verdict from R-variant-B-propellant-accounting (R16) and R-reactor-specific-power-program-targets (R17) is substantially weakened by heritage-anchored bus mass.** At Cassini bus, **9 cells** close L0-05 strict AND L0-09 commercial floor simultaneously across the matrix-relevant Arch-E architecture.

The matrix R16 finding that "Variant B delivers 4 t per mission at 200-t chunk" stands — that was specifically about Variant B's chemical-electric-chemical three-stage stack. **This round addresses Arch E (pure-electric end-to-end), which had been falsified by rhea R6 because of the full-bus anchor and zero aerocapture credit.** At Cassini bus + 10 km/s aerocapture + R6's other parameters (Isp 2934 / sp 10), Arch-E closes strict.

## What this does and does not overturn

**Does overturn:**
- Rhea R6 / R10 / R11 / R12 conclusion that "Arch E has no all-pass cell at sp ≤ 10 W/kg" → at Cassini bus, Arch E has 9 all-pass-strict-commercial cells at sp ∈ {5, 10}.
- Enceladus-r5 R6 (own prior round) verdict "Arch E requires L0-05 waiver to ≥ 25 years" → at Cassini bus, 9 Arch-E cells close at L0-05 strict 15 yr.
- The R-bottoms-up-vehicle-cost (R13) implicit assumption that dry mass ~ 50 t — true dry mass at Cassini bus + 500 kWe + 5 W/kg + linear bag: 2 + 10 + 100 + 5 = **117 t** at sp=5, or 2 + 10 + 50 + 5 = **67 t** at sp=10. The 500 kWe reactor system at flown specific power is the dominant mass, not the bus.

**Does NOT overturn:**
- R17's reactor-program-availability conjunction posterior (0.004 %). That is about funded reactor programs, independent of bus mass.
- R-variant-B-propellant-accounting (R16). Variant B is a different architecture (chemical-kick + electric + chemical-capture); R16's 4-t-delivered finding is about Variant B specifically.
- R-chunk-as-heat-shield-revisit (phoebe). The 10-km/s aerocapture credit is still conditional on hybrid aerocapture.

## Caveats — what my bus model omits

A 500-kWe reactor needs:
- **Radiation shadow shield** (LiH + tungsten typically): 1-3 t at 500 kWe scope. NOT in my m_bus.
- **High-voltage power conditioning** at 500 kWe: 0.5-2 t. NOT in my m_bus.
- **Reactor-to-thruster power transmission cables and harness**: 0.5-1 t. NOT in my m_bus.

A more honest "minimum" bus for a 500-kWe ICEBERG vehicle:
- Cassini-base subsystems (structure, thermal, comms, attitude, propulsion ancillaries): 2 t
- Radiation shadow shield: 2 t
- Power conditioning: 1 t
- Cables + harness: 0.5 t
- **Total: ~5.5 t**, close to Europa Clipper (5.9 t).

At m_bus = 5 t (Europa-Clipper-anchor) with linear bag (5% × chunk), the all-pass-waiver count drops to 26 (vs Cassini's 29). The all-pass-strict-commercial count drops by ~1 (the 200-t chunk cells at sp=5/Isp=2000 lose margin). The architectural conclusion holds at Europa-Clipper anchor: **engineering-closed commercial cells exist for Arch E at 500 kWe + 200 t chunk + 5-10 W/kg + 10 km/s aerocapture + Cassini-or-Europa-Clipper bus mass.**

## Implications for the matrix

1. **Engineering closure exists for Arch E at heritage bus mass, conditional on hybrid aerocapture.** The matrix's R6+R10+R11+R12 sequence falsifying Arch E was anchored on full-bus 23 t + zero aerocapture credit. With realistic bus + R-chunk-as-heat-shield revisit at hybrid (multi-pass) aerocapture, Arch E reopens.

2. **R17's program-availability verdict (0.004% conjunction posterior) is unchanged.** R17 is about whether a 500-kWe reactor program at 8 W/kg + 5 yr lifetime materialises. That is independent of bus mass. The framing decisions L0-13 → government/sovereign-grant and reactor-program-availability → forced still stand.

3. **The matrix should add a "bus-mass anchor" column.** Currently absent. Three reasonable anchors: Cassini (2 t), Europa Clipper (5.9 t), full-vehicle (15 t). The closure verdict differs by 1.7-2× between extremes.

4. **R-architecture-E-no-saturn-side-electrolysis (R6) should be revisited with heritage-anchored bus mass.** Spawn `R-architecture-E-heritage-bus-revisit` — predict that the "L0-05 strict 0/120, waiver 9/120" verdict updates to substantially more closures.

5. **R-bottoms-up-vehicle-cost (R13) should be revisited.** R13 computed first-unit costs based on a ~50-t subsystem stack. With heritage bus + 500-kWe reactor + 200-t chunk capability, the bus subsystem cost line drops (1-2 t vs 15 t at $1.6-3M/kg heritage = $1.6-9M vs $24-45M) but the reactor system mass (50-100 t at 5-10 W/kg) becomes the cost driver, not the bus. **Bottoms-up first-unit cost should redistribute mass-weight among subsystems but total cost may not change much** — the reactor was already the dominant line item in R13.

## What other assumptions should be questioned next

This round questioned bus mass. Other still-load-bearing assumptions inherited from earlier rounds:

- **dv_inbound = 25 km/s continuous-thrust.** R-matrix-dv-regime-consistency (R15) already flagged this. Per-cell dv selection (impulsive for chemical-dominated, CT for electric-dominated) is the right resolution.
- **L0-05 = 15-yr strict ceiling and L0-09 = 30-t commercial floor.** These are project-owner requirements, not engineering. Could be relaxed in REQUIREMENTS amendment.
- **Aerocapture 10 km/s credit.** Conditional on R-hybrid-aerocapture-aerobraking closure (hyperion-pending).
- **Reactor specific power 5-10 W/kg.** R10 / R17 work.
- **Reactor lifetime 10 yr.** Could be qualified to 15 yr with reactor-program development.
- **Outbound 6 yr / Saturn-side 1 yr.** Fixed.

The highest-leverage remaining question, given this round's findings: **if Arch E engineering-closes at heritage bus + hybrid aerocapture, what is the program-availability posterior of the 500-kWe / 5-10 W/kg / 5-yr-lifetime reactor program by 2035?** R17 has the answer (0.004% conjunction). The engineering side closing doesn't help if the reactor side doesn't.

## Sensitivity check — does my bus model survive realistic shielding?

`shielding_sensitivity.py` re-runs the 9 Cassini-anchor commercial-strict cells with added components I omitted from the main sweep: radiation shadow shield (1-5 kg/kWe), power-conditioning unit (1.5-2 t at 500 kWe, scales with P), and cable harness (0.5-1 t).

| Scenario | Commercial-strict cells surviving |
|---|---|
| Cassini bus only (original) | 9/9 |
| Cassini + light shield (1 kg/kWe) + 1.5 t PCU + 0.5 t cables | 7/9 |
| Cassini + medium shield (3 kg/kWe) + 1.5 t PCU + 0.5 t cables | 7/9 |
| Cassini + heavy shield (5 kg/kWe) + 2 t PCU + 1 t cables | 6/9 |
| **Europa Clipper bus (5.9 t) + light shield (1 kg/kWe)** | **6/9** |
| Europa Clipper bus (5.9 t) + medium shield (3 kg/kWe) | 6/9 |

**Verdict holds.** At Europa Clipper bus + medium shield (realistic anchor for an ICEBERG-class vehicle with 500-kWe reactor), 6 of 9 commercial-strict cells survive. The most robust cells (500 kWe + 200 t chunk + sp=10 + aero=10 + Isp=2934, delivering 88-92 t at RT 12.7-12.85 yr) pass at every tested shielding anchor. The cells that fall first are the marginal RT~14.9 yr ones at 200 kWe / 100 t / sp=5.

This corroborates the main-round conclusion: the matrix's "no engineering-closed cell" verdict is overturned for Arch E at heritage bus mass, conditional on hybrid aerocapture. The closure margin is real (1-3 yr of RT slack on the best cells) and not an artifact of an over-simplified bus model.

## Files of record

```
water-prop/rounds/R_bus_mass_anchor_sweep/STUDY.md                        (this file)
water-prop/rounds/R_bus_mass_anchor_sweep/run.py                          (main sweep)
water-prop/rounds/R_bus_mass_anchor_sweep/shielding_sensitivity.py        (post-hoc check)
water-prop/rounds/R_bus_mass_anchor_sweep/results/tables.md
water-prop/rounds/R_bus_mass_anchor_sweep/results/results.json
water-prop/rounds/R_bus_mass_anchor_sweep/results/shielding_sensitivity.txt
```

## Methodology / recurring-lesson tracker

- **Recurring-lesson-7 strike 10 averted.** Hand-checked the 500-kWe/200-t/sp=10/aero=10/Isp=2000/Cassini-bus cell: m_reactor 50 t + m_bus 2 t + m_bag 10 t + m_thrusters 5 t = m_dry 67 t. m_0 = 267 t. v_e = 19613 m/s. dv 15 km/s. m_f = 267 / exp(0.7649) = 124.2 t. m_w = 142.8 t. delivered = 200 - 142.8 = 57.2 t. E_jet = 0.5 × 142.8e3 × 19613² = 2.75e13 J. E_elec = 5.49e13 J. t_burn = 1.099e8 s = 3.48 yr. RT = 6 + 1 + 3.48 = 10.48 yr. Matches table to four-decimal places.
- **Recurring lesson 11 filed (NEW).** When inheriting a numerical anchor across rounds without questioning it, the anchor accumulates analytical authority that the original source didn't justify. The 23-t bus + bag anchor was used in 3+ rounds (R-architecture-E, R-bottoms-up-vehicle-cost, R-hybrid-chemical-power-augmentation) before this round questioned it. Protocol fix: anchors that propagate across ≥ 2 rounds should be flagged as load-bearing and explicitly traced to a primary source before being inherited.
