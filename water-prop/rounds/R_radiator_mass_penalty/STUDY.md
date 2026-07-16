# R-radiator-mass-penalty — what is the correct tug dry mass at each reactor class once radiator mass scales properly with reactor power, and how does this shift the architecture decision matrix's megawatt cells?

**Status:** pre-result.

## Question

The architecture decision matrix's operational rule (`ARCHITECTURE-DECISION-MATRIX.md` §"How to size the reactor", step 5) computes vehicle dry mass as `5 t tug + reactor_kWe × 0.1 t` — i.e. 5 tonnes of non-reactor fixed equipment plus a reactor stack scaling at 10 watts-per-kilogram total electrical specific power. The matrix's unresolved-assumption item #7 already notes that this formula does not separate radiator mass from reactor mass: at megawatt class, the radiator alone is on the order of 10–15 tonnes, but the 10 W/kg figure is "total electrical" and is therefore claimed to already embed it.

Two questions need disentangling:

1. **Is the 10 W/kg "total electrical specific power" figure realistic at megawatt class once radiator mass is explicitly counted?** The NASA Fission Surface Power 40-kilowatt-electric concept sits at ~6–10 W/kg total system. A 1-megawatt-electric system at 10 W/kg requires that reactor + power-conversion + radiator + tankage all fit inside 100 tonnes — and that includes ~3 MW of waste heat rejection. Is that achievable, or is the right number closer to 5 W/kg, pushing megawatt vehicles to 200 tonnes dry?
2. **If we decompose the dry mass explicitly into `m_fixed + m_reactor + m_PC + m_radiator + m_tank` rather than rolling everything into a single specific-power figure, does the megawatt cell still win, or does sub-megawatt (200 kWe) become the optimum?**

The decomposition matters because each subsystem scales differently:

- `m_reactor` scales with thermal power (megawatts thermal) and has its own specific power (~30–50 W_th/kg for compact space reactors)
- `m_PC` (power conversion) scales with electrical output and conversion-cycle choice (Brayton ~5 kg/kWe, Stirling ~10 kg/kWe)
- `m_radiator` scales with waste heat (megawatts thermal × (1 - η_conversion)) and radiator areal density × heat-flux-capacity (typical: 5–10 kg/m², 5–20 kW/m² rejection at 600–800 K hot-side)
- `m_tank` scales with propellant mass; for an all-electric burn at high specific impulse the propellant fraction is small but the tank for water at low Saturn temperature is not free

Reference points from NASA/DOE studies cited in the matrix and in R-reactor-specific-power:

- Fission Surface Power 40 kWe: total system mass target ~7 t (5.7 W/kg total)
- Megawatt-class concepts (JIMO, Project Prometheus): 5–10 W/kg with 30+ tonnes of radiator alone at 1 MWe
- NASA Glenn Brayton Power Conversion: ~5 kg/kWe at megawatt scale
- Heat-pipe / pumped-loop radiators at 700 K hot-side: 5 kg/m², 10 kW/m² heat flux → 0.5 kg/kW_th rejected

## Pre-registered hypothesis (H-rmp)

**Aggregate (H-rmp-agg):** Megawatt cells degrade 20–40% on delivered-mass-per-launch-mass once the radiator is properly counted as a separate scaling line item rather than implicitly bundled into a 10 W/kg total figure. The optimum reactor power shifts from "as high as possible" toward sub-megawatt (200–500 kilowatt-electric). The Kilopower cells are unchanged (the 5-tonne fixed equipment was a good fit there). The matrix's "megawatt era is the asymptote" framing remains qualitatively correct but the gap to sub-megawatt narrows substantially.

**Pre-registered sub-claims:**

| Sub-claim | Predicted | Falsification |
|---|---|---|
| H-rmp-a — Megawatt tug dry mass with explicit radiator scaling at η_conv = 0.30 | 50–120 t (vs matrix's implicit 105 t at 10 W/kg) | outside ±25% |
| H-rmp-b — Megawatt cell delivered-fraction degradation under explicit radiator model vs current 10 W/kg lumped model | 15–40% | outside that band |
| H-rmp-c — Optimum reactor power for near-term technology readiness shifts from 1000 kWe | toward 200–500 kWe | falsified if megawatt still wins by ≥20% margin |
| H-rmp-d — Kilopower cell unchanged | within ±5% | outside ±5% |
| H-rmp-e — Launch-mass-multiplier shift across matrix | megawatt cell launch mass increases ≥30%; sub-megawatt cell unchanged ±5% | outside those bands |

**Aggregate decision:** if H-rmp-agg holds, propagate to `ARCHITECTURE-DECISION-MATRIX.md` to (1) replace the single-line "10 W/kg total electrical" simplification with an explicit decomposition table, (2) flag megawatt-cell delivered/launch ratios as degraded relative to prior matrix, (3) re-rank sub-megawatt vs megawatt on delivered-per-launch-mass.

## Method

### Decomposed dry-mass model

Per the round prompt:

```
m_tug(P) = m_fixed + m_reactor(P) + m_PC(P) + m_radiator(P) + m_tank(m_prop)
```

Sub-models:

```
m_reactor(P_el)    = P_el_kWe / α_reactor_W_per_kg            # α ≈ 50 W/kg (electrical-equivalent)
m_PC(P_el)         = P_el_kWe / α_PC_W_per_kg                  # α ≈ 200 W/kg → 5 kg/kWe
m_radiator(P_el)   = P_th_waste_kW / α_radiator_kW_per_kg
   where P_th_waste_kW = P_el_kWe × (1 - η_conv) / η_conv
   and α_radiator_kW_per_kg ≈ 2 kW_th/kg (= 10 kW/m² × 5 kg/m² → 0.5 kg/kW_th rejected for high-T radiators)
   conservative case: 1 kW_th/kg (= 5 kW/m² × 5 kg/m² → 1 kg/kW_th)
m_tank(m_prop)     = m_prop × f_tank                           # f_tank ≈ 0.05 (5% tank fraction for water at 200 K)
m_fixed            = 3 t (avionics, structure, attitude control, comms, electric thrusters themselves)
```

At 10 W/kg total electrical specific power, the bundled formula gives `m_reactor + m_PC + m_radiator = P_el / 10 kg/kWe`. We compare:

- **Bundled** (matrix's current formula): `m_tug = 5 t + P_el_kWe × 0.1 t`
- **Decomposed mid case**: η_conv = 0.30, α_reactor = 50 W/kg, α_PC = 200 W/kg, α_radiator = 2 kW_th/kg → at 1 MWe gives 20 + 5 + 1.17 = 26.2 t reactor stack + 3 t fixed + tank
- **Decomposed conservative case**: η_conv = 0.25, α_reactor = 30 W/kg, α_PC = 100 W/kg, α_radiator = 1 kW_th/kg → at 1 MWe gives 33 + 10 + 3 = 46 t reactor stack + 3 t fixed + tank
- **Decomposed stretch case**: η_conv = 0.40, α_reactor = 80 W/kg, α_PC = 200 W/kg, α_radiator = 4 kW_th/kg → 12.5 + 5 + 0.375 = 18 t reactor stack + 3 t fixed + tank

### Architecture sweep

For each (reactor_kWe, chunk_t, dry-mass-model) combination, compute:

1. All-electric delivered mass via rocket equation: `M_final = (M_v + chunk) × exp(-dv_total / v_e)`; delivered = M_final - M_v
2. Outbound launch mass under chemical-kick architecture (the matrix's headline outbound case): `M_LEO = M_v × exp(dv_outbound / v_e_outbound)` with dv_outbound = 9 km/s, Isp_outbound = 2000 s, then multiplied by 6.9 to reach LEO via R-outbound-architecture's hydrolox-kick factor.

Use the same constants as `R_reactor_specific_power/run.py` (G0, 6.42 km/s inbound, 2000 s outbound, etc.) so this round is directly comparable.

### Sweep axes

- Reactor power: 10, 40, 100, 200, 500, 1000, 2000 kWe (same as R-reactor-specific-power)
- Chunk size: 100, 200, 500 t
- Mass model: bundled-10-W/kg / decomposed-mid / decomposed-conservative / decomposed-stretch
- Electric specific impulse: 2000 s (representative; matrix optimum across most cells)

### Output

- Per-cell delivered mass, launch mass, delivered/launch ratio
- Per-mass-model: tug dry mass at each reactor class
- Pairwise comparison: degradation factor from bundled-10-W/kg to decomposed-mid at 1 MWe
- Headline question: does the megawatt cell still beat sub-megawatt under decomposed-mid?

### Validity caveats

- The decomposed model treats radiator areal density as constant; real radiators degrade in areal density at very high reject rates (panel-deployment mass, fluid-loop mass). The model probably *under*-counts radiator at megawatt scale.
- Power-conversion specific mass at megawatt scale has minimal flight heritage; the 200 W/kg figure is from NASA Glenn Brayton studies and Project Prometheus, not flight hardware.
- Reactor-only specific power at 30–80 W/kg is the contested range. Modern HALEU / FSP-derivative concepts cluster around 50 W/kg; cold-war SP-100 was ~25 W/kg; Soviet Topaz-II was ~10 W/kg. The "α_reactor = 50 W/kg" assumption is mainline but not conservative.
- Conversion efficiency η_conv = 0.30 is mid-Brayton; Stirling at 0.25; advanced Brayton or thermophotovoltaic at 0.40. Higher η_conv reduces radiator mass quadratically (waste heat drops AND radiator can run hotter), so this is the highest-leverage parameter.
- Tank fraction f_tank = 5% is a guess at low temperatures (200 K, water-stable); structural and insulation mass at 200 K is well-bounded but not modeled in detail.
- This round does not re-derive the matrix's chunk-mass-vs-reactor-power optimum (R-reactor-specific-power did that under bundled assumptions). The optimum may shift under decomposed assumptions; checking the qualitative shift is part of this round; re-running the full sweep is not.

## Result

Run output at `results/radiator_penalty.json` and `results/tables.md`.

**Hypothesis grading:**

| Sub-claim | Predicted | Actual | Held? |
|---|---|---|---|
| H-rmp-a — 1 MWe tug dry mass, decomposed-mid, no tank | 50–120 t | 29.2 t | falsified low |
| H-rmp-b — Megawatt cell delivered/launch-mass degradation, decomposed-mid vs bundled, 500 t chunk | degrade 15–40% | improves 230% (factor 2.77×) | falsified, opposite direction |
| H-rmp-c — Optimum reactor power at 500 t chunk, 7-yr cap, decomposed-mid | shift from 1000 kWe to 200–500 kWe | 200 kilowatt-electric in both bundled and decomposed | held qualitatively (optimum unchanged at 200 kWe) |
| H-rmp-d — Kilopower cell within ±5% on delivered/launch | unchanged | improves 60% under decomposed-mid | falsified |
| H-rmp-e — Megawatt launch mass +30%, sub-megawatt unchanged ±5% | +30% / ±5% | −68% at 1 MWe, −30 to −50% at sub-megawatt | falsified, opposite direction across the board |

**Aggregate (H-rmp-agg): falsified in inverted direction.** The matrix's "5 tonnes fixed + reactor power times 0.1 tonnes per kilowatt-electric" operational formula does NOT under-count radiator mass. It over-counts total stack mass. Under physically defensible component-level assumptions (reactor specific power 50 W/kg, power-conversion specific power 200 W/kg, radiator specific heat-rejection 2 kW-thermal per kg, conversion efficiency 0.30), a 1 megawatt-electric stack masses 29 tonnes including 1.2 tonnes of radiator. The bundled formula gives 100 tonnes for the same stack. The matrix has been carrying a hidden ~3× margin on megawatt-class tug mass for the entire campaign.

## Reading

**Pre-registered intuition was wrong, and the matrix's framing should change but not in the direction predicted.**

What I expected: explicit radiator scaling would expose a hidden penalty at megawatt class that the bundled lumped figure obscured. What actually happened: the bundled figure is the conservative case, not the optimistic one. Radiator at 1 megawatt-electric, even under conservative areal-density assumptions (5 kilograms per square metre at 5 kilowatts per square metre rejection, hot-side 700 K), is ~3 tonnes. Small against reactor and power-conversion mass at the same power level.

**Why the prediction failed:** I conflated two distinct figures-of-merit. The 10 W/kg cited in the matrix is total electrical specific power for *fielded historical systems* (Project Prometheus design exercise, Kilopower Reactor Using Stirling TechnologY / KRUSTY). That number embeds historical low conversion efficiency, mass-conservative reactor shielding, and flight-qualified-with-margin hardware overhead. The decomposed model uses component-level *physical* specific powers (modern Brayton conversion, high-temperature radiator panels, compact reactor cores) — all of which sit 2–4× above their flight-qualified equivalents. The decomposed-mid case is therefore an "aspirational physics" figure, not a "what would actually fly" figure.

**Implications for the architecture decision matrix:**

1. **Keep the bundled 10 W/kg formula as the matrix's operational rule.** It embeds the realistic gap between physics and flight hardware. Replacing it with the decomposed mid-case would be over-claiming.
2. **Treat the decomposed-mid model as the upside bound.** If a megawatt-class technology-development program closes its specific-mass goals, megawatt cells improve substantially — launch mass drops 60–70%.
3. **Drop the "megawatt requires on-orbit assembly" framing.** Under decomposed-mid, 1 megawatt-electric is a 29-tonne tug, deliverable on a single heavy-lift launch. The on-orbit-assembly claim was a bundled-formula artefact.
4. **Optimum reactor power at 7-year burn cap and 500-tonne chunk is 200 kilowatt-electric in both models.** Robust result. The matrix's framing that sub-megawatt is the practical optimum is unchanged.
5. **Kilopower cells also benefit.** Even the small-reactor cells have ~2 tonnes of hidden margin in the bundled formula (10 kilowatt-electric: 6 tonnes bundled versus 3.5 tonnes decomposed). If released, kilopower delivered/launch ratios improve 60%.

**Methodology lesson, candidate for CONVENTIONS log:**

> When a lumped simplification has lasted across multiple rounds without challenge, the lumped figure is more likely to be conservative-with-margin than optimistic-with-cheating, because the engineer who introduced it had to pick a number nobody would push back on. The instinct to "decompose and find a hidden penalty" is wrong roughly half the time — sometimes you decompose and find a hidden margin.

This sits alongside "predict mechanism and threshold separately" and "model both legs of the round trip explicitly" as the third recurring lesson in this campaign.

## Revisit clause

Grade H-rmp-a through H-rmp-e. If H-rmp-agg holds, propagate to `ARCHITECTURE-DECISION-MATRIX.md`:

1. Replace the single-line "5 t tug + reactor_kWe × 0.1 t" operational rule with an explicit decomposition (m_fixed, m_reactor, m_PC, m_radiator, m_tank) or at minimum cite the decomposed-mid case as a sanity-check column.
2. Add a column to the matrix's reactor-era table showing decomposed-mid tug dry mass alongside bundled-10-W/kg.
3. Re-rank the megawatt vs sub-megawatt cells on delivered/launch-mass under decomposed-mid.
4. If H-rmp-c holds (optimum shifts to sub-megawatt), revise the matrix's headline "Megawatt era is the asymptote" framing to "Sub-megawatt to low-megawatt is the practical optimum once radiator mass is explicitly counted."

If H-rmp-c falsifies (megawatt still wins by ≥20%), keep the matrix's framing but cite this round as having checked the radiator-mass-penalty assumption explicitly.
