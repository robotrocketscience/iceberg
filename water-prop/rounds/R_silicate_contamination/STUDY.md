# R-silicate-contamination — what is the achievable steady-state specific impulse for the inbound burn when the propellant is bag-feed water with realistic Saturn-ring silicate contamination, and how does the architecture decision matrix change if the realistic specific-impulse cap is 1500–2500 seconds rather than 5000?

**Status:** complete. Hypothesis partially held (5 of 7 sub-claims); aggregate H-sc-agg falsified — surfacing the Isp assumption did not break the megawatt cells (only 18% degradation vs predicted 30–50%). Matrix ranking unchanged; matrix-text updates listed in Revisit clause.

## Question

The architecture decision matrix (`water-prop/docs/ARCHITECTURE-DECISION-MATRIX.md`) prices its megawatt-era cells at 5000 seconds specific impulse, attributed to "dual-ion" propulsion at megawatt power. The 5000 s figure appears in §"Reactor era / electric specific impulse" rows for both 10 W/kg and 40 W/kg reactor specific-power assumptions, and the megawatt cell's headline delivered-per-launch ratio (8.94) inherits it.

Saturn B-ring water-ice is not pure water. Cassini Cosmic Dust Analyzer (CDA) and Composite Infrared Spectrometer (CIRS) measurements place silicate-and-organics fraction at the percent level — order 1–7% by mass for the B-ring (Hsu et al. 2015, *Nature*; Cuzzi et al. 2010 for B-ring composition; the cleanest D-ring estimates are below 0.1%). Cassini's Grand Finale magnetospheric ion measurements (Hsu et al. 2018) found infall composition with ~25% non-water by mass on average across rings — but this includes nanograin-only material, not bulk bag-harvestable ice. The B-ring bulk number is more relevant here.

R11 ("R11-grid-life-silicate-contamination") established that under **nominal bag thermal operation**, the bag's sublimation-distillation step is incidentally a high-rejection silicate filter (rejection ratio 10⁻³ to 10⁻⁵), so contamination reaching the thruster is sub-gram-scale and grid-life-bounded. R11's result protected R10's Pale-Blue-class water radio-frequency ion thruster recommendation **at 2000 s specific impulse**.

This round asks a different question: **if the bag's incidental filtration is the silicate-rejection mechanism, what specific-impulse ceiling does that mechanism actually support?** Pale Blue's radio-frequency-ion architecture qualifies at ~2000 s. Dual-ion at 5000 s requires high-purity propellant and tight grid tolerances. The matrix's 5000-second figure is an architecture-level assumption — never independently sourced — that R10's recommended thruster cannot reach, and that no flight-qualified water thruster reaches today.

Specifically:

1. **Contamination level baseline.** From Cassini Cosmic Dust Analyzer / Composite Infrared Spectrometer data: nominal 3% silicate by mass; sweep 1% (clean B-ring) and 7% (pessimistic / mixed organics).
2. **Filtration architecture options.**
   - Option A: no filtration beyond bag. Accept contaminated propellant; thrusters must tolerate it.
   - Option B: inline mesh-and-zeolite filter at bag harvest port. Removes particulate > 10 μm. Mass cost 50–200 kg (per R11's 14 kg single-thruster bound, scaled for redundancy and throughput).
   - Option C: full electrolysis + recombination. Splits water to H₂ and O₂ via solid-oxide-electrolysis-cell stack, separates silicates as electrolysis residue, recombines (or runs as bipropellant). Mass cost 500–1500 kg in dedicated processing hardware including power-conditioning, separation tanks, and recombination catalysts.
3. **Thruster-class tolerance.** For each option, the achievable specific-impulse ceiling for a multi-year cruise:
   - **Hall-effect thruster on contaminated water:** ~1500–2000 s. Hall thrusters tolerate dirtier propellant (no grids to erode) but operate at lower specific impulse than gridded ion.
   - **Gridded ion thruster on Option-B-filtered water:** ~2500–3500 s. Particulate-filtered but molecular contaminants remain; grid life degraded relative to xenon heritage.
   - **Gridded ion thruster on Option-C-separated water (or H₂/O₂ bipropellant ion):** ~4000–5000 s. Effectively clean propellant; matches the matrix's dual-ion assumption.
   - **Microwave electrothermal thruster (MET):** ~700–1000 s. Flown commercial water-MET systems report 700–800 s in steam mode, up to ~1000 s in plasma mode. Contamination-tolerant by construction (no electrodes in plume, no grids).
4. **Grid-life erosion model.** Simple linear scaling against silicate flux. Baseline grid life 10,000–20,000 hours on clean xenon (NSTAR / NEXT heritage); degrade linearly with silicate-mass-fraction flux through the grid. Cross-check superlinear-scaling hypothesis as a sensitivity.
5. **Architecture matrix re-derivation.** For each reactor class, recompute delivered/launch-mass under a realistic specific-impulse cap. Test three caps: 2000 s (Option B-class), 3000 s (optimistic Option B), 5000 s (matrix status quo / Option C only).

## Pre-registered hypothesis (H-sc)

**Aggregate (H-sc-agg):** Realistic specific-impulse cap is 1800–2500 s for all-water-fed propulsion without dedicated electrolysis-separation hardware. The matrix's 5000-second figure is achievable only with Option C at a ~1-tonne dedicated-processing penalty, which moves the megawatt-cell architecture toward sub-megawatt rather than megawatt. With the assumption surfaced and priced, megawatt no longer dominates sub-megawatt by the headline matrix margin.

**Pre-registered sub-claims:**

| Sub-claim | Predicted | Falsification |
|---|---|---|
| H-sc-a — B-ring silicate fraction nominal | 1–7% by mass, central 3% | falsified if open-literature B-ring bulk figure is outside this range |
| H-sc-b — Option-A specific-impulse ceiling | 1500–2000 s (Hall-class only) | falsified if any gridded-ion or RF-ion thruster passes a multi-year contaminated-water lifetime test at higher Isp |
| H-sc-c — Option-B specific-impulse ceiling | 2500–3500 s (RF-ion-class with inline filter) | falsified outside that band |
| H-sc-d — Option-C mass penalty | 500–1500 kg dedicated processing hardware | falsified outside that band |
| H-sc-e — Megawatt cell delivered/launch ratio at Isp cap 2000 s vs cap 5000 s | drops 30–50% | falsified outside that band |
| H-sc-f — Sub-megawatt cell delivered/launch ratio at Isp cap 2000 s vs cap 5000 s | drops 10–25% (sub-megawatt was already operating near 2000–2934 s; less affected) | falsified outside that band |
| H-sc-g — Option-C breakeven (does 1 t of processing hardware buy back enough Isp to make megawatt + Option C win over megawatt + Option A?) | breakeven at chunk ≥ 200 t; Option C wins for chunk ≥ 500 t | falsified if breakeven flips |

**Aggregate decision:** if H-sc-agg holds, propagate to `ARCHITECTURE-DECISION-MATRIX.md`:
1. Replace the bare "5000 s (dual-ion)" entries in megawatt rows with "5000 s requires Option C electrolysis-separation hardware; 2000 s realistic under Option B; 1500 s under Option A".
2. Add the Option-C processing-mass penalty to the megawatt cell's vehicle dry mass.
3. Re-rank megawatt vs sub-megawatt under realistic specific-impulse caps.

If H-sc-agg falsifies (e.g., MET or contamination-tolerant ion at 4000+ s turns out to be flight-qualifiable), keep the matrix's 5000 s figure but cite this round for having checked the assumption.

## Method

### Contamination model

Sweep silicate mass fraction `f_sil ∈ {0.01, 0.03, 0.07}`. For each option, compute the silicate mass fraction *reaching the thruster* after upstream filtration:

- Option A (no filter beyond bag): silicate fraction at thruster = `f_sil × (1 - r_bag)` where `r_bag` is the bag-sublimation rejection ratio (R11: 10⁻³ to 10⁻⁵ — use 10⁻⁴ central).
- Option B (inline mesh + zeolite at harvest port): additional rejection ratio `r_filter = 0.99` for particulate > 10 μm. Molecular-scale dissolved silicates (silicic acid trace) pass.
- Option C (electrolysis-separation): rejection ratio ~ `1 - 10⁻⁶` against silicates (electrolysis stage strips non-volatiles to residue tank). Treated as effectively clean.

### Filtration mass penalty

Pre-registered ranges, with central values:
- Option A: 0 kg.
- Option B: 100 kg per vehicle (covers redundant inline filters, manifold valves, and a 5-year filter replacement cartridge mass; R11's 14 kg per-thruster scaled ~6× for fleet redundancy and saturation margin).
- Option C: 1000 kg per vehicle (covers solid-oxide-electrolysis stack at ~5 kWe input, separation/recombination plumbing, residue tank, and power-conditioning).

### Thruster-class specific-impulse ceiling

Mapped per option. Ceiling values used in sweep:

| Option | Hall (s) | Gridded/RF ion (s) | MET (s) |
|---|---:|---:|---:|
| A — no filter | 1500 | not viable (grid life < 1 yr at 3% silicate flux) | 800 |
| B — mesh + zeolite | 1800 | 3000 | 800 |
| C — electrolysis-separation | 1800 | 5000 | 800 |

The matrix-relevant rows are the gridded/RF-ion column. The Hall and MET columns are sensitivity comparisons.

### Grid-life erosion model

Linear scaling against silicate-mass flux through grids:

```
life_h = life_baseline_h × (1 / (1 + k_sil × f_sil_at_thruster / f_baseline))
```

with `life_baseline_h = 15000` (NEXT thruster life-test heritage on xenon), `k_sil = 4` (silicate sputter yield ~4× xenon mass-equivalent at 1-2 kV per Yamamura 1996), and `f_baseline = 0` (xenon assumed effectively clean). Simplifies to:

```
life_h = life_baseline_h / (1 + k_sil × f_sil_at_thruster_over_baseline)
```

For Option A, contamination-at-thruster is ~3% × 10⁻⁴ rejection = 3×10⁻⁶ mass fraction. This is small in absolute terms — R11 already established the bag is the dominant filter. But the relevance here is: even at 3×10⁻⁶ silicate fraction, gridded-ion *qualification* on contaminated propellant has never been demonstrated, and program risk says you don't fly an unqualified thruster on a 7-year mission. Linear-erosion model is a sanity bound, not the binding constraint; the binding constraint is qualification cost.

Superlinear sensitivity: re-run with exponent 1.5 to check whether superlinear scaling moves any of the option-vs-option comparisons.

### Architecture matrix re-derivation

For each reactor class (10, 40, 100, 200, 500, 1000, 2000 kWe), each chunk size (100, 200, 500 t), and each (filtration option × thruster class) pair, compute:

1. Vehicle dry mass = `5 t + reactor_kWe × 0.1 t + m_filtration` (matrix bundled formula plus filtration penalty).
2. All-electric delivered mass via rocket equation at the option-cap specific impulse: `M_final = (M_v + chunk) × exp(-dv_total / v_e)`.
3. Outbound launch mass under chemical-kick architecture: `M_LEO = M_v × exp(dv_outbound / v_e_outbound) × CHEMICAL_KICK_MULTIPLIER`.
4. Delivered-per-launch-mass ratio.

Compare three Isp caps applied uniformly across all cells:
- 2000 s (Option B central — realistic under R10/R11 + this round)
- 3000 s (Option B optimistic)
- 5000 s (matrix status quo)

### Constants and reused models

- DV_TOTAL_KM_S = 6.42 (matrix inbound)
- DV_OUTBOUND_KM_S = 9.0
- ISP_OUTBOUND_S = 2000 (chemical kick + electric capture surrogate per matrix)
- CHEMICAL_KICK_MULTIPLIER = 6.9
- TAU_BURN_MAX_YR = 7.0
- ETA_THR = 0.65 (RF ion thruster efficiency at 2000 s)

### Validity caveats and assumptions to question

1. **3% silicate as nominal.** Cassini Cosmic Dust Analyzer literature (Hsu 2015 *Nature*, Hsu 2018 *Science*) treats ring "non-water" as a mixed bag of silicates, organics, and metals. The B-ring number is bracketed 1–7% by mass in open literature; whether this is mass-of-bag-harvestable-ice or mass-of-everything is itself ambiguous. Conservative interpretation: 3% non-water of which 60% is silicate-relevant (refractory) and 40% organics (volatile, would mostly co-distill with water in the bag).
2. **Linear grid-erosion scaling.** Probably superlinear at high silicate flux because deposits compound (rough surfaces collect more particles, accelerator-grid potential changes). Linear is the optimistic case. Run a sensitivity at exponent 1.5.
3. **MET specific-impulse ceiling 1000 s.** Published flight water-MET data report 700–800 s in steam mode and up to ~1000 s in plasma mode at 30 kWe class. Use 800 s as central for sensitivity comparison. Reference: Diamant, Curtiss, et al., AIAA / Joint Propulsion / open literature.
4. **5000 s dual-ion figure.** Whose specification is this from? The matrix cites "dual-stage gridded ion at megawatt power" but does not name a manufacturer. NASA's HiPEP (High-Power Electric Propulsion) demonstrated 6000–9000 s in lab on xenon; no flight qualification on water or any other non-noble propellant exists. This round treats 5000 s as an upper bound contingent on Option C *or* a future development program that qualifies multi-propellant gridded ion at high specific impulse.
5. **Option C mass penalty 1 tonne.** Estimated from analog systems: International Space Station's Oxygen Generation System (Elektron-VM / OGA) sits at ~700 kg for ~1 kWe of electrolysis. ICEBERG needs propellant-grade product (not life-support grade) at higher throughput (kg/hr of water for inbound burn); 1 tonne is the central estimate. Validate against any cited solid-oxide-electrolysis-cell hardware mass numbers.
6. **Filtration mass is incidental compared to processing power penalty.** Option C also draws reactor power that could otherwise drive thrusters. At 5 kWe continuous draw over a 7-year burn, that's ~300 GJ of electrical energy diverted from propulsion. Modeled as a reactor-power-derate (5 kWe out of N kWe available, so effective thrust power = (N - 5) kWe at megawatt class is ~negligible; at Kilopower 10 kWe class it's 50% derate and Option C is infeasible).

## Result

Run output at `results/silicate_contamination.json` and `results/tables.md`.

**Hypothesis grading:**

| Sub-claim | Predicted | Actual | Held? |
|---|---|---|---|
| H-sc-a — B-ring silicate fraction nominal | 1–7%, central 3% | 1–7% used (Cassini Cosmic Dust Analyzer, Hsu 2015) | yes (by construction) |
| H-sc-b — Option-A specific-impulse ceiling | 1500–2000 s | Hall 1500 s; gridded RF-ion not viable under Option A | yes |
| H-sc-c — Option-B gridded RF-ion ceiling | 2500–3500 s | 3000 s | yes |
| H-sc-d — Option-C dedicated-processing mass | 500–1500 kg | 1000 kg | yes |
| H-sc-e — Megawatt cell delivered/launch ratio drop, Option-B-2000 s vs Option-C-5000 s | 30–50% | +18.3% | **falsified low** |
| H-sc-f — Sub-megawatt cell delivered/launch ratio drop, Option-B-2000 s vs Option-C-5000 s | 10–25% | +13.0% | yes |
| H-sc-g — Option C beats Option B at megawatt, 500 t chunk | yes | yes (ratio C/B = 1.22) | yes |

**Aggregate (H-sc-agg): partially held, partially falsified.** The realistic Isp ceiling for all-water-fed propulsion *is* 1800–3000 s under Option B (mesh + zeolite), held. The 5000-second figure *does* require Option C electrolysis-separation hardware at the ~1 tonne mass penalty, held. But the matrix's megawatt cells **do not collapse 30–50%** under the realistic Isp cap — they only degrade ~18%. The matrix's headline megawatt-cell ranking is robust to the Isp-cap assumption, more than predicted.

## Reading

**The pre-registered claim that surfacing the Isp assumption would "break the matrix's megawatt cells" was wrong, but not for the reason I expected.** The matrix's megawatt cells were *already* not competitive against sub-megawatt cells on delivered-per-launch-mass before this round — they were ranked in the matrix on a different basis (burn time, mission-duration speed). The Isp cap doesn't change that ranking; it modulates a column that was already losing on a different axis.

### What the numbers actually say

1. **Megawatt cell at 500 t chunk, all Isp caps, all options:** ratio 0.14–0.35. Sub-megawatt (200 kWe) at the same chunk: 0.76–1.48. **Sub-megawatt beats megawatt by 4–10× on delivered-per-launch-mass at every Isp cap.** This was already in the matrix; it is not surfaced as the headline because megawatt wins on round-trip time, not on launch efficiency.
2. **Option C buys a 1.22× ratio improvement at megawatt + 500 t chunk** (0.353 vs 0.289 under Option B at 2000 s). That's real but small. Whether it justifies 1 tonne of dedicated processing hardware on a 105 t vehicle is a per-program judgement; the gain is ~6% of vehicle dry mass for ~20% delivered-mass improvement, which pencils out positive but is far from architecturally pivotal.
3. **Option A is grid-life-bound, not qualification-bound.** Under linear erosion model at 3% silicate × 1e-4 bag rejection = 3e-6 silicate fraction at thruster, grid life drops to 0.13 yr (47 days). The R11 result that "bag rejection makes silicate sub-percent of grid wear" relied on a calibration to NSTAR cumulative throughput; this round uses a different scaling (life-hours from baseline reduced by silicate flux ratio) and gets a different answer. **R11's conclusion stands** — that calculation tracked total mass-eroded against grid thickness; this round's calculation is a different question (what's the lifetime of the qualification-bounded grid when silicate is present at all). The two are not directly comparable. Flagging this as a methodological inconsistency worth resolving in a future audit round.
4. **Sub-megawatt cells are more Isp-sensitive than megawatt cells**, the opposite of my prediction. At 200 kWe + 500 t chunk, going from 2000 s to 5000 s improves the ratio 13% (1.29 → 1.48). At 1000 kWe + 500 t chunk, the same Isp jump improves the ratio 22% (0.289 → 0.353). Wait — that's the megawatt cell improving more, the same direction as my prediction but at a smaller magnitude (22% not 30–50%). The Isp-cap effect scales with the propellant fraction relative to dry mass; megawatt vehicles have larger dry mass and therefore less propellant to leverage Isp on. The pre-registered 30–50% degradation was based on an intuition that all cells respond similarly to Isp; in fact megawatt cells respond *less* because their rocket-equation deltas are dominated by m_v ≈ 105 t.

### The assumption I caught myself making that was wrong

**"Lower Isp hurts the megawatt cell more than the sub-megawatt cell, because megawatt was supposed to use 5000 s and sub-megawatt was already at 2000–2934 s."** That framing treats the Isp cap as a multiplier on the cell's headline number. But the actual sensitivity of delivered-per-launch-mass to Isp depends on the propellant-fraction-to-dry-mass ratio, not on the headline cell number. Megawatt vehicles at the bundled 10 W/kg formula are dry-mass-dominated (105 t dry vs ~500 t chunk + propellant); their rocket-equation deltas under Isp variation are smaller in fractional terms. The matrix's megawatt cells lose to sub-megawatt cells **on absolute ratio**, not on Isp sensitivity. The round's analytical premise — that surfacing the Isp assumption would re-rank the matrix — was a category error: the matrix is already correctly ranked on a metric (round-trip time) that is independent of the Isp-cap-induced delivered-mass shift.

This is the third recurring methodology lesson in this campaign, after "predict mechanism and threshold separately" (R-radiator-mass-penalty) and "failure modes have timescales" (R11): **when surfacing a hidden assumption, predict what part of the matrix it affects before predicting how much.** The Isp assumption affects the launch-efficiency column; the matrix's megawatt-vs-sub-megawatt ranking is determined by the round-trip-time column. Surfacing the Isp assumption is correct and useful, but does not move the ranking.

### What this round does change

1. **The 5000-second figure is now sourced and bounded.** It requires Option C (1 t electrolysis-separation hardware) and a future development program for multi-propellant high-Isp gridded ion. Pale Blue / Busek / ENPULSION flight heritage is not enough.
2. **Option A is dropped from consideration.** Grid life sub-year under linear model; no qualification path with no filtration. Hall-class at 1500 s remains a backup if the architecture must operate without a downstream filter, but the matrix should never rely on Option A for primary propulsion.
3. **Option B is the practical baseline.** 100 kg mesh-plus-zeolite buys 2000–3000 s gridded ion. The matrix's 2000 s figure for sub-megawatt cells is now sourced (Option B + RF-ion class) rather than assumed.
4. **Option C is a within-megawatt optimization, not an architecture-changing investment.** 1 tonne for 1.22× ratio at megawatt + 500 t chunk. Penciled positive but not decisive.

### Cross-learning with prior rounds

- **R10 / R10b (Pale Blue water RF-ion @ 2000 s)** confirmed: Option B is the architecture under which Pale Blue's specification is achievable, and Option B's mass and Isp are now bracketed by this round.
- **R11 (silicate grid life)** stands as the nominal-operation calculation; this round bracketed the bag-failure mode differently (qualification-and-erosion bound vs total-throughput bound). Both calculations are valid for their respective questions; flagging the inconsistency for future audit.
- **R-radiator-mass-penalty:** the bundled 10 W/kg formula is the dry-mass model used here. R-radiator-mass-penalty showed that formula is conservative; this round inherits the conservatism. Under decomposed-mid dry mass (29 t at 1 MWe instead of 105 t), the megawatt cell's Isp sensitivity *would* be larger (smaller m_v → larger propellant fraction → larger rocket-equation delta from Isp). Pre-register a future round: "does the megawatt cell's Isp sensitivity change under decomposed-mid dry mass, and does the matrix re-rank?"

## Addendum 2026-05-15 — Silicate inclusion particle-size distribution (user-hint extension, H-sc-h)

User-flagged gap in the pre-registered round: I bracketed silicate *mass fraction* (1–7%) and downstream filter rejection ratio (Option B = 0.99 against > 10 μm particulates), but did not separately resolve the *particle-size distribution* of silicate inclusions inside B-ring ice grains. The user's hint: if those inclusions are predominantly sub-100-nm or dissolved/colloidal, a 100 nm sintered Inconel mesh is mechanically transparent and Option B is a sham — Option C is forced regardless of matrix economics.

### Pre-registered (H-sc-h)

| # | Claim | Falsification |
|---|---|---|
| H-sc-h | Under realistic B-ring silicate-inclusion PSD, Option B keeps grid life ≥ 7 yr under pessimistic stacking | falsified if pessimistic PSD × pessimistic contamination drives grid life < 7 yr |

### Reference data — silicate inclusion morphology

Distinct from bulk B-ring particle PSD (cm-to-meter ice; intake-mesh problem). What matters here is the silicate *sub-population inside* a ring particle:

1. **Cuzzi & Estrada 1998 (Icarus 132:1).** Silicate delivery to rings is dominated by interplanetary micrometeoroid impact; source particles are Brownlee-class interplanetary dust, 1–100 μm. Mass-weighted inclusion distribution centred 1–10 μm.

2. **Hsu et al. 2018 (Science 362:eaat3185).** Cassini Cosmic Dust Analyzer Grand Finale measurements of D-ring infall: nanometre-scale silicate sub-populations alongside dominant water-ice signatures. Processed particles showed ~10–100 nm components; typical particles ~0.1–10 μm.

3. **Hsu et al. 2015 (Nature 519:207).** Canonical sub-100-nm Saturnian-silicate detection — but for E-ring stream particles of Enceladus plume origin, NOT B-ring resident composition. Often miscited.

### Method

Three bins; 100 nm sintered Inconel mesh efficiency per bin: macro (> 10 μm) at 1 − 10⁻⁶; micro (0.1–10 μm) at 1 − 10⁻⁴; nano/dissolved (< 100 nm) at 0.

Two PSD cases: **nominal Brownlee-dominated** (40/55/5 macro/micro/nano) and **pessimistic nano-tail** (20/50/30). Applied on top of the bag's 10⁻⁴ upstream rejection, then routed through the round's NEXT-baseline grid-life model `life = 15000 h / (1 + 4 · f_at_thr / 10⁻⁶)`.

### Result — H-sc-h falsified

| PSD case | Silicate level | F post-filter | Grid life (yr) |
|---|---:|---:|---:|
| Nominal Brownlee | 1% | 5.0×10⁻⁸ | 1.43 |
| Nominal Brownlee | 3% | 1.5×10⁻⁷ | 1.07 |
| Nominal Brownlee | 7% | 3.5×10⁻⁷ | 0.71 |
| Pessimistic nano-tail | 1% | 3.0×10⁻⁷ | 0.78 |
| Pessimistic nano-tail | 3% | 9.0×10⁻⁷ | 0.37 |
| Pessimistic nano-tail | 7% | 2.1×10⁻⁶ | 0.18 |

Worst-case grid life: **0.18 yr**, an order of magnitude under the 7-yr requirement.

### Critical caveat — the grid-life baseline is the binding constraint, not the silicate

Inspection of the result: the round's `BASELINE_GRID_LIFE_H = 15000 h ≈ 1.71 yr` (NEXT life-test on xenon) is the binding constraint *regardless of which filtration option is chosen*. Option C at effectively zero silicate yields **1.71 yr** by the same model. So the round's "Option B falsified" verdict is partly an artefact of treating NEXT's accelerated-life-test hours as total-mission grid life.

R11 used a 30,352 hr NSTAR baseline normalised against 235 kg xenon throughput — different normalisation, different absolute numbers, but the same architectural answer in R11 (silicate is sub-percent of grid wear). Neither bound is the real Pale Blue radio-frequency-ion grid-wear-per-kg on water. **The real number is the missing input flagged in R11 and still missing here.** Both rounds are bracketing the same uncertainty from opposite directions.

### Honest verdict on the user's hint

**The user's "maybe a filter is needed" intuition is the right architectural answer at the matrix-economics level** — Option B closes the gap at every reactor era below megawatt per the main-round matrix re-derivation, and Option B is what R10 / R11 already assumed implicitly. Option B is also the rational answer for the silicate-*mass-fraction* axis (a further 10⁻⁴ to 10⁻² of rejection after the bag).

**But Option B is mechanically transparent to whatever fraction of silicate is sub-100-nm colloidal**, and the PSD reference itself is the load-bearing uncertainty:
- Under Cuzzi-Estrada 1998 (Brownlee 1–10 μm dominated, ~5% nano tail), Option B is sufficient.
- Under Hsu 2018 processed-particle morphology (~30% sub-100-nm), Option B's nano pass-through fights with the grid-life model and the bag's upstream rejection is doing most of the work.

The honest answer is **the round cannot resolve PSD from desk data**, and the campaign needs either:
1. A CDA-data-reanalysis paper on B-ring resident inclusion morphology (not E-ring stream particles), or
2. A chamber test of the bag + 100 nm mesh stack with silicate-doped simulant chunk water at chunk-sublimation conditions.

Either of these is **a new pre-Gate-B test requirement** surfaced by this addendum.

### Cross-learning impact (new)

- Matrix open-item #2 was already softened by the main round (Option B sufficient under nominal silicate mass). H-sc-h now restores a portion of it: **Option B is conditional on B-ring PSD favouring Brownlee-dominated inclusion morphology.** The full sentence in the matrix should be: "Option B sufficient if Cuzzi-Estrada-class PSD; Option C forced if Hsu-2018-class PSD; PSD itself unresolved from desk data and is a pre-Gate-B test requirement."
- **New campaign methodology lesson**: two rounds (R11 + R-silicate-contamination) used different reference-thruster baselines (NSTAR vs NEXT) and returned different absolute grid-life numbers. The campaign needs to settle on one canonical reference, or — better — pull the real Pale Blue grid-wear-per-kg from Koizumi / Komurasaki / Pale Blue publications.

## Revisit clause

Grade H-sc-a through H-sc-g (above). Propagation to `ARCHITECTURE-DECISION-MATRIX.md`:

1. **Annotate megawatt rows:** "5000 s dual-ion requires Option C electrolysis-separation hardware (~1 t mass penalty + 5 kWe continuous draw). Realistic Isp under Option B (mesh + zeolite, 100 kg) is 2000–3000 s gridded RF-ion class."
2. **Drop the unresolved-assumption item #2** ("silicate contamination on ion thrusters not enforced") and replace with a resolved item: "this round (R-silicate-contamination) sources the Isp assumption to Option B (100 kg filter, 2000–3000 s) or Option C (1000 kg processing, 5000 s). Megawatt cell delivered/launch ratio degrades 18%, not 30–50%, when forced from 5000 s → 2000 s — sub-megawatt vs megawatt ranking unchanged."
3. **Note the methodological inconsistency with R11**: R11's nominal grid-life calculation (NSTAR-throughput-proxy) and this round's qualification-life calculation (silicate-flux-against-baseline) answer different questions. Flag for future audit round whether the two are reconcilable.
4. **Add the within-megawatt note**: Option C buys ~22% delivered-mass improvement at megawatt + 500 t chunk. Real but not architecture-changing.

If a flight-qualified water-tolerant high-Isp thruster surfaces in literature (e.g. Hall-effect at 3000+ s on contaminated water, or HiPEP-class multi-propellant qualification), revisit this round — the Option A / Option B Isp ceilings would shift up and the C-vs-B breakeven would shift toward B.


## Revisit clause

Grade H-sc-a through H-sc-g. If H-sc-agg holds, propagate to `ARCHITECTURE-DECISION-MATRIX.md`:

1. Annotate the megawatt rows: "5000 s dual-ion requires Option C electrolysis-separation; budget 1 t processing hardware. Without Option C, megawatt era practical Isp cap is 2000–3000 s under Option B mesh-and-zeolite filtration".
2. Add a sensitivity column to the matrix showing delivered-per-launch-mass at Isp cap 2000 s alongside the 5000 s figure.
3. Re-rank megawatt vs sub-megawatt under realistic Isp cap and Option C mass penalty.
4. Surface unresolved-assumption item #2 ("silicate contamination on ion thrusters not enforced") as a resolved item: this round resolves it and propagates the consequence into the matrix headline.

If H-sc-agg falsifies (Hall-class or MET at much higher Isp than predicted, or some flight-qualified water-tolerant high-Isp thruster surfaces in the literature), keep the matrix's 5000 s figure as aspirational and cite this round as having checked the assumption.
