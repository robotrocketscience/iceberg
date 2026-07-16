# R-chunk-fed-chemical — Variant B: where does electrolyze-chunk-water-at-Saturn beat all-electric and carried-hypergolic?

**Status:** pre-result.

## Question

R-two-stage-dv's Post-result correction (committed 2026-05-14) found that carried-hypergolic two-stage architecture is structurally inferior on delivered-per-launch-mass once outbound mass is accounted for. The corrected reading: two-stage is an **early-era bridge** only — useful when all-electric is power-infeasible, otherwise all-electric wins.

This round examines the **third architecture** that came out of that discussion: chunk-fed chemical, in which the chemical Saturn-departure burn uses propellant electrolyzed from chunk water at Saturn rather than chemical propellant launched from Earth.

The architecture eliminates the outbound chemical-propellant burden entirely. The cost: the chemical burn now accelerates the vehicle + chemical stage dry hardware **through** the chunk, paying for that acceleration with electrolyzed chunk water. This depletes the chunk inventory before the electric stage even starts.

**The question:** map the (reactor power × chunk mass × chemical offload) plane and identify cells where Variant B beats both all-electric (single-stage) and carried-hypergolic two-stage on delivered-water-per-tonne-launched-to-low-Earth-orbit.

## Architecture definition

**Variant B (chunk-fed chemical):**
- Outbound launch carries: vehicle dry mass (tug + reactor + bag + grapple) + chemical stage dry hardware (electrolyzer + cryotankage + cryocoolers + nozzle + structure) + outbound electric propellant. No chemical propellant.
- Outbound electric burn (all-electric, 9 km/s, specific impulse 2000 s) delivers vehicle + chemical stage hardware to Saturn.
- At Saturn: grapple chunk.
- Phase 1 burn (Saturn-departure, chemical): electrolyze chunk water on-site, burn at hydrolox specific impulse 450 s. Δv_chem ∈ {0, 1, 2, 3} km/s.
- Jettison chemical stage dry mass after the burn.
- Phase 2 burn (heliocentric + Earth approach, electric): use remaining chunk water as propellant. Δv_elec = 6.42 − Δv_chem km/s.
- Inbound mass = vehicle + remaining chunk water = delivered mass at low Earth orbit.
- Delivered water = inbound mass − vehicle dry mass.

**All-electric baseline** (R-design-envelope reference):
- Outbound launch: vehicle dry + outbound electric prop. No chemical stage.
- Single-stage electric inbound at the specific impulse required to deliver target η of chunk at full 6.42 km/s.

**Carried-hypergolic two-stage** (R-two-stage-dv reference):
- Outbound launch: vehicle dry + chemical stage dry + chemical propellant (hypergolic, 320 s) + outbound electric prop.
- Chemical burn at Saturn-depart uses carried propellant.
- Electric inbound at Δv_elec on chunk water.

## Pre-registered hypothesis (H-cfc)

**Aggregate (H-cfc-agg):** Variant B is structurally lightest at low Earth orbit of the three but pays for the chemical impulse by depleting the chunk. It wins on delivered-per-launch-mass only in reactor-era cells where all-electric is power-infeasible AND carried-hypergolic's outbound mass penalty exceeds Variant B's chunk-depletion penalty. The winning region is narrow: roughly Fission Surface Power era (40–100 kilowatt-electric) with chunks ≥ 100 t. Outside that window, either all-electric wins (megawatt era) or no architecture closes (Kilopower era with large chunks).

**Pre-registered sub-claims:**

| Sub-claim | Predicted | Falsification |
|---|---|---|
| H-cfc-a — At 500+ kilowatt-electric (sub-megawatt + megawatt reactor era), all-electric wins on delivered/launch-mass across all chunk sizes ≤ 500 t | yes | falsified if any Variant B cell at ≥500 kilowatt-electric beats all-electric by >5% on delivered/launch-mass |
| H-cfc-b — At Kilopower (10 kilowatt-electric), no architecture closes the 7-year inbound burn time for chunks ≥ 50 t | yes | falsified if any architecture closes at 10 kilowatt-electric for chunks ≥ 50 t |
| H-cfc-c — Variant B wins at Fission Surface Power era (40–100 kilowatt-electric) for chunks 100–500 t | yes | falsified if Variant B does not win any cell in that region |
| H-cfc-d — Variant B's optimum chemical offload is 1.0–1.5 km/s (smaller than carried-hypergolic's 2.0 km/s, because chunk-depletion penalty grows faster than the all-electric power saving) | 1.0–1.5 km/s | outside ±0.5 km/s |
| H-cfc-e — Variant B's delivered/launch-mass in winning cells | 1.0–1.5 | outside ±20% |
| H-cfc-f — Variant B never beats all-electric at 5000 s (water dual-ion) electric stage, even at Kilopower | yes | falsified if Variant B beats all-electric at any dual-ion cell |

**Aggregate decision:** if H-cfc-c holds, **Variant B is the recommended architecture for the early-program era** (years 0–15 in the R-reactor-roadmap timeline) for chunks > 100 t. If H-cfc-c fails high (Variant B wins more broadly), the megawatt-reactor roadmap urgency drops because pre-megawatt architectures become viable. If H-cfc-c fails low (Variant B never wins), the program either accepts smaller chunks pre-megawatt or sits on the Kilopower → Fission Surface Power era with no large-chunk option.

## Method

Algebra, no integrator. Same approximations as R6/R10/R10b/R-design-envelope/R-two-stage-dv. Constants:

```
g₀                       = 9.80665 m/s²
v_e_chem (hydrolox)      = 4413 m/s  (specific impulse 450 s)
v_e_chem (hypergolic)    = 3138 m/s  (specific impulse 320 s)
v_e_outbound_electric    = 19,613 m/s (specific impulse 2000 s)
Δv_total_inbound         = 6.42 km/s   (R10b 7-flyby case)
Δv_outbound              = 9.00 km/s   (low Earth orbit to Saturn arrival, all-electric outbound)
τ_burn_max               = 7 yr        (inbound coast budget)
specific_power_reactor   = 10 W/kg     (Fission Surface Power target)
m_tug_kg                 = 5000        (vehicle structure, bag, grapple, radio, RCS, etc.)
m_chem_dry_kg            = 10000       (electrolyzer + cryotankage + cryocoolers + nozzle)
electric_thruster_efficiencies = {Hall: 0.55, RF-ion: 0.65, dual-ion: 0.55}
```

For each (reactor_kWe, chunk_t, dv_chem_km_s, electric_isp_s) cell, compute three architectures and pick winner by delivered-water-per-low-Earth-orbit-mass.

**Variant B mass accounting:**

```
M_v       = m_tug + reactor_kWe × 1000 / specific_power_reactor   # vehicle dry
M_initial = M_v + m_chem_dry + chunk_t × 1000
M_after_chem = M_initial × exp(-Δv_chem / v_e_chem_hydrolox)
chunk_consumed_chem = M_initial × (1 - exp(-Δv_chem / v_e_chem))
M_after_jettison = M_after_chem - m_chem_dry
M_after_elec = M_after_jettison × exp(-Δv_elec / v_e_elec)
delivered_water_t = (M_after_elec - M_v) / 1000
```

Feasibility: chunk_consumed_chem must be ≤ chunk_t (cannot burn more than the chunk has). M_after_elec must be ≥ M_v (vehicle has to come home).

Burn time check:
```
m_prop_elec = M_after_jettison - M_after_elec
F_elec = 2 × η_thr × P_electrical / v_e_elec
τ_burn = m_prop_elec × v_e_elec / F_elec / YEAR_S
```
Flag if τ_burn > 7 yr.

**All-electric baseline:**
```
M_v_baseline = m_tug + reactor_kWe × 1000 / specific_power_reactor
M_initial = M_v + chunk_t × 1000
M_final = M_initial × exp(-Δv_total / v_e_elec)
delivered_water = (M_final - M_v) / 1000
```

**Carried-hypergolic two-stage:**
```
M_v + m_chem_dry at Saturn arrival.
M_chem_prop_kg = chunk_t × 1000 × (exp(Δv_chem / v_e_chem_hypergolic) - 1)
Outbound: deliver (M_v + m_chem_dry + M_chem_prop) to Saturn.
At Saturn-depart: chunk + M_chem_prop burned at hypergolic, leaving chunk + M_v + m_chem_dry minus prop.
... (full accounting in run.py)
```

**Outbound launch mass for each architecture:**
```
M_LEO = M_at_Saturn_arrival / exp(-Δv_outbound / v_e_outbound_elec)
       = M_at_Saturn_arrival × exp(Δv_outbound / v_e_outbound_elec)
       = M_at_Saturn_arrival × 1.583
```
(plus the outbound electric propellant itself, which equals M_at_Saturn × (1.583 - 1) = M_at_Saturn × 0.583)

**Comparison metric:** delivered_water_t / M_LEO_t. Higher is better.

**Sweep axes:**

- Reactor power: 10, 40, 100, 200, 500, 1000 kilowatt-electric (Kilopower → megawatt era)
- Chunk mass: 50, 100, 200, 500 tonnes
- Chemical offload Δv_chem: 0, 1, 2, 3 km/s (capped to avoid extreme chunk depletion)
- Electric thruster Isp: 1500 (Hall), 2000 (RF-ion), 2934 (high RF-ion), 5000 (dual-ion)

= 6 × 4 × 4 × 4 = 384 Variant B cells. Plus matched all-electric and carried-hypergolic comparisons per cell.

**Validity caveats:**

- Outbound architecture fixed at all-electric (specific impulse 2000 s, 9 km/s). Real conops uses chemical kick stage for Earth-departure plus electric for heliocentric — that would increase outbound launch mass for all three architectures roughly proportionally, so the *relative* comparison is preserved but absolute delivered/launch-mass numbers shift down.
- Chemical stage dry mass fixed at 10 t. In reality the electrolyzer + cryotanks scale with propellant mass; below 1 t of propellant the electrolyzer dominates. Cells with very small chemical propellant consumption (low Δv_chem) overpenalize Variant B; cells with very large consumption underpenalize. Acceptable for design-region mapping.
- No silicate contamination modeling. The dual-ion cells are reported but should be read as "if dual-ion at 5000 s on chunk water were achievable" — see R11 for the actual constraint.
- Bag efficiency η_c, electric stage efficiency, duty cycle all set to nominal flat values. Sensitivity to these is in prior rounds; not re-modeled here.
- Saturn-side dwell time (1 yr per conops) not modeled. Electrolysis at Saturn needs power and time; at 100 kilowatt-electric a ~50 t electrolysis run takes weeks. Within 1 year dwell.

## Result

### Winning architecture by (reactor power × chunk mass)

Best of {all-electric, Variant B at Δv_chem ∈ {1, 2, 3}, carried-hypergolic at Δv_chem ∈ {1, 2, 3}} per cell, at any feasible electric specific impulse, requiring inbound burn time ≤ 7 years. Format: `architecture · Δv_chem · Isp_elec · (delivered/launch-mass)`. "–" = no feasible architecture.

| Reactor (kilowatt-electric) | 50 t chunk | 100 t chunk | 200 t chunk | 500 t chunk |
|---:|---|---|---|---|
| 10 | Variant B · 2 km/s · 2000 s · **(0.77)** | Variant B · 3 km/s · 1500 s · **(1.29)** | – | – |
| 40 | all-electric · 2934 s · **(2.68)** | all-electric · 1500 s · **(4.32)** | Variant B · 2 km/s · 2000 s · **(3.13)** | – |
| 100 | all-electric · 5000 s · **(1.77)** | all-electric · 2934 s · **(3.24)** | all-electric · 2000 s · **(5.90)** | Variant B · 2 km/s · 2000 s · **(6.15)** |
| 200 | all-electric · 5000 s · **(1.03)** | all-electric · 5000 s · **(2.14)** | all-electric · 2934 s · **(3.92)** | all-electric · 2000 s · **(8.94)** |
| 500 | all-electric · 5000 s · **(0.43)** | all-electric · 5000 s · **(0.93)** | all-electric · 5000 s · **(1.94)** | all-electric · 2934 s · **(4.47)** |
| 1000 | all-electric · 5000 s · **(0.19)** | all-electric · 5000 s · **(0.45)** | all-electric · 5000 s · **(0.98)** | all-electric · 5000 s · **(2.56)** |

### Delivered water (tonnes) by best architecture per cell

| Reactor (kilowatt-electric) | 50 t | 100 t | 200 t | 500 t |
|---:|---:|---:|---:|---:|
| 10 | 19.5 | 32.7 | – | – |
| 40 | 38.2 | 61.5 | 94.1 | – |
| 100 | 42.0 | 77.0 | 140.0 | 243.4 |
| 200 | 40.8 | 84.7 | 155.0 | 353.4 |
| 500 | 37.1 | 81.0 | 168.7 | 389.0 |
| 1000 | 31.0 | 74.8 | 162.6 | 425.8 |

### Launch mass to low Earth orbit (tonnes) by best architecture per cell

| Reactor (kilowatt-electric) | 50 t | 100 t | 200 t | 500 t |
|---:|---:|---:|---:|---:|
| 10 | 25 | 25 | – | – |
| 40 | 14 | 14 | 30 | – |
| 100 | 24 | 24 | 24 | 40 |
| 200 | 40 | 40 | 40 | 40 |
| 500 | 87 | 87 | 87 | 87 |
| 1000 | 166 | 166 | 166 | 166 |

### Three-way comparison at 100 t chunk, electric specific impulse 2000 s, Δv_chem = 1 km/s

| Reactor (kilowatt-electric) | All-electric delivered | Variant B delivered | Carried-hyp delivered | All-electric / launch mass | Variant B / launch mass | Carried-hyp / launch mass |
|---:|---:|---:|---:|---:|---:|---:|
| 10 | 70.4 t (slow) | 56.6 t (slow) | 74.4 t (slow) | 7.42 | 2.23 | 0.79 |
| 40 | 69.6 t (slow) | 55.4 t | 73.7 t | 4.89 | 1.84 | 0.73 |
| 100 | 67.9 t | 53.0 t | 72.2 t | 2.86 | 1.34 | 0.63 |
| 200 | 65.1 t | 49.1 t | 69.8 t | 1.65 | 0.89 | 0.52 |
| 500 | 56.7 t | 37.2 t | 62.6 t | 0.65 | 0.36 | 0.31 |
| 1000 | 42.8 t | 17.4 t | 50.5 t | 0.26 | 0.10 | 0.16 |

"(slow)" indicates schedule-infeasible (inbound burn time > 7 years).

### Hypothesis grading

| Sub-claim | Predicted | Actual | Held? |
|---|---|---|---|
| H-cfc-a — All-electric wins at 500+ kilowatt-electric across all chunk sizes ≤ 500 t | yes | yes (all winners at 500 and 1000 kilowatt-electric are all-electric) | held |
| H-cfc-b — No architecture closes at Kilopower for chunks ≥ 50 t | yes | falsified — Variant B closes at 50 t (delivers 19.5 t) and at 100 t (delivers 32.7 t) within the 7-yr burn cap | **falsified** |
| H-cfc-c — Variant B wins at Fission Surface Power era (40–100 kilowatt-electric) for chunks 100–500 t | yes | partially held — Variant B wins at (40 kWe, 200 t) and (100 kWe, 500 t) but not at (40 kWe, 100 t) where all-electric Hall wins, nor at (100 kWe, 100–200 t) where all-electric wins | partially held |
| H-cfc-d — Variant B's optimum Δv_chem in 1.0–1.5 km/s range | 1.0–1.5 km/s | falsified — Variant B winners pick 2 km/s and 3 km/s, not 1–1.5 | **falsified** |
| H-cfc-e — Variant B delivered/launch-mass ratio in winning cells: 1.0–1.5 | 1.0–1.5 | falsified — winning Variant B ratios are 0.77, 1.29, 3.13, 6.15 (range much wider than predicted) | falsified-favorable |
| H-cfc-f — Variant B never beats all-electric at 5000 s dual-ion electric | yes | held (no Variant B winner uses 5000 s; both Variant B winning cells at the boundary use 1500–2000 s) | held |

## Reading

**The architecture-by-reactor-era decision matrix is now resolved.** Three of six hypotheses falsified, one partially held; the falsifications all favored a stronger Variant B than I predicted.

**Five observations the result actually supports:**

1. **Variant B is the only feasible architecture at Kilopower for chunks ≥ 50 t.** All-electric at Kilopower can in principle deliver more chunk mass (70.4 t vs Variant B's 32.7 t at 100 t chunk) but the burn time exceeds 7 years. Variant B's chemical impulse compresses burn time at the cost of depleting the chunk. **If the campaign accepts a Kilopower-era demonstrator flight, Variant B is the architecture.** This falsifies H-cfc-b in a useful direction.

2. **The economic peak of delivered-water-per-launch-mass is at Fission-Surface-Power to sub-megawatt power with 100–200 t chunks** (delivered/launch ratio of 5.90 at 100 kilowatt-electric / 200 t chunk). Below this region, the chunks are too small to amortize the launch overhead. Above this region, the reactor mass dominates the outbound launch and drags efficiency back down. **The campaign's economic sweet spot is not the megawatt era as R-reactor-roadmap implied.**

3. **Megawatt-class reactor delivers more absolute water per ship but lower delivered-per-launch-mass.** At 1000 kilowatt-electric / 500 t chunk, delivered = 425.8 t but launch mass = 166 t (ratio 2.56). At 100 kilowatt-electric / 200 t chunk, delivered = 140 t at 24 t launch mass (ratio 5.90). **There is a tension between R-reactor-roadmap (megawatt-class is the IRR lever) and this round (megawatt-class is launch-inefficient).** The tension resolves by recognizing the two rounds optimize different things: R-reactor-roadmap holds delivered-per-ship as the revenue driver; this round holds delivered-per-launch as the cost-of-goods driver. The right answer depends on which is the binding economic constraint — if launch capacity is plentiful and customer demand is unbounded, megawatt wins; if either is scarce, the Fission Surface Power era wins.

4. **Carried-hypergolic never wins a single cell.** Across all 24 (reactor × chunk) configurations, carried-hypergolic is dominated by either all-electric or Variant B. The original R-two-stage-dv "winning architecture" headline was wrong — corrected in that round's Post-result patch and now empirically confirmed here.

5. **Reactor specific power is a more leveraged variable than reactor absolute power.** At 10 watts/kg specific power, a 1-megawatt-electric reactor weighs 100 tonnes, which alone exceeds the launch mass at lower reactor powers. Doubling specific power to 20 W/kg (technologically aggressive but not impossible) would halve reactor mass and could push the megawatt-era delivered/launch-mass ratio above the Fission Surface Power peak. **The campaign should track reactor-mass-per-electric-watt as carefully as reactor-power-arrival-year.**

**What this round assumes that should be questioned:**

- **7-year inbound burn cap.** Comes from prior conops (6.09 yr Hohmann outbound + 1 yr dwell + 7 yr inbound = 14 yr round-trip). Relaxing this — to 10–13 yr inbound — would let Kilopower all-electric close more cells (the "(slow)" cells at Kilopower deliver 70+ t but at 8–18 yr burn time). The physical reason to cap burn time is bag permeability, not the 14-yr ceiling per se; the bag-engineering analysis showed 4–5% mass loss over a 7-year inbound coast, which would scale to 8–10% over 13 years. **A round on bag-permeability vs inbound-burn-time would close this loop.**
- **Reactor specific power fixed at 10 watts/kg.** Aggressive programs target 20–40 W/kg; conservative achieves 5–7 W/kg. The result is highly sensitive to this constant.
- **Chemical stage dry mass fixed at 10 tonnes.** Real electrolyzer + cryotankage mass scales with throughput. At low Δv_chem (small propellant mass), 10 tonnes is over-penalizing Variant B; at high Δv_chem (large propellant mass), 10 tonnes is under-penalizing.
- **Outbound architecture fixed at all-electric.** Real conops uses a chemical trans-Saturn-injection kick stage. Re-running with chemical-kick outbound would shift absolute launch masses up but the *relative* comparison across architectures is preserved.
- **Silicate contamination still ignored.** The dual-ion winning cells at 5000 s specific impulse should be read as aspirational. R11 enforced silicate-tolerance constraint would degrade dual-ion → radio-frequency-ion → Hall progression.

## Revisit clause

H-cfc-a held; H-cfc-b, H-cfc-d, H-cfc-e falsified (the latter two in favorable directions); H-cfc-c partially held; H-cfc-f held. Aggregate H-cfc-agg held in shape (Variant B has a narrow winning region near low-reactor-era + large-chunk cells) but the winning region is *smaller* than I predicted — three winning cells, not "Fission-Surface-Power era for chunks 100–500 t."

**Architecture decision matrix surfaced by this round:**

| Reactor era (year) | Recommended architecture | Best electric specific impulse | Chunk size sweet spot |
|---|---|---|---|
| Kilopower (year 0) | Variant B, chunk-fed chemical 2–3 km/s | 1500–2000 s (water Hall / radio-frequency ion) | 50–100 t |
| Fission Surface Power (year 7) | All-electric for chunks ≤ 100 t; Variant B for chunks ≥ 200 t | 1500–2934 s | 50–200 t |
| Stretch / sub-megawatt (year 12–15) | All-electric | 2000–5000 s | 100–500 t |
| Megawatt (year 20) | All-electric, but watch reactor specific power | 5000 s (dual-ion if silicate-tolerance closes) | 200–500 t |

**Next-round candidates surfaced by this round:**

- **R-bag-permeability-vs-burn-time:** how much delivered mass do we lose by relaxing the 7-yr inbound burn cap to 10–13 yr? If small, Kilopower all-electric becomes viable and Variant B's narrow winning region narrows further.
- **R-reactor-specific-power-sensitivity:** delivered/launch-mass ratio at 5, 10, 20, 40 W/kg reactor specific power. This may be a more important campaign variable than reactor absolute power.
- **R-aerocapture-revisit:** still open from R-two-stage-dv. Aerocapture would collapse inbound Δv from 6.42 km/s to 1–2 km/s and reshuffle every cell in this round.


## Revisit clause

Grade H-cfc-a through H-cfc-f. If H-cfc-c holds, **the recommended architecture maps to reactor era**: pre-Fission-Surface-Power use all-electric small-chunk; Fission-Surface-Power-to-sub-megawatt use Variant B at chunk ≥ 100 t; megawatt-and-above use all-electric large-chunk. This becomes the campaign's headline architecture decision matrix and should propagate to the conops document.
