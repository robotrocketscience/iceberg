# R-hybrid-aerocapture-aerobraking — does pass-1-deep-aerocapture-with-bag-sacrificed plus pass-2-onward-shallow-aerobraking close where single-pass aerocapture and pure aerobraking each fail?

**Worker:** phoebe (resumed session, 2026-05-15 latest+).
**Status:** pre-result. Hypotheses pre-registered with central back-of-envelope estimates computed BEFORE range bands, per methodology lesson 1 (pessimistic-default holds), methodology lesson 7 (compute under most pessimistic credible anchor first), and methodology lesson 9 (anchor on PRIMARY-text aggregate verdict — phoebe's own lesson from the prior round).

---

## Why this round, and why phoebe

Hyperion authored the SCOPE for this round 2026-05-15 after the matrix surviving cell collapsed to empty (R-aerocapture-fast-cruise-envelope falsified the Round-F STRICT cell at the engineering level; R-no-atmospheric-capture-baseline showed zero of 288 cells close without atmospheric capture). The hybrid candidate — sacrifice bag in a deep pass-1, then aerobrake bag-less over multiple shallow passes — is the only architecturally-credible aerocapture-adjacent rescue remaining. Phoebe was the natural worker: phoebe's prior round (R-chunk-as-heat-shield-revisit, commit `9b3d29e`) imported hyperion's aerocapture physics functions verbatim, identified a latent solver-direction bug in `required_periapsis_altitude_km`, and was the original author of the recommendation to promote R-hybrid-aerocapture-aerobraking to next critical-path round. The project owner directed that recommendation (commit `0c29de8` 2026-05-15 latest+6).

This round inherits phoebe's prior methodology stack and adds a fourth load-bearing methodology choice: an US Standard 1976 atmosphere table replaces hyperion's single-scale-height exponential, because the hybrid architecture spans both deep (40-90 km, scale height ~6-7 km) and shallow (130-200 km, scale height ~10-30 km) regimes that a single H = 7.5 km exponential cannot represent. The choice is documented as a methodology improvement; both regimes use the same lookup table.

---

## Three load-bearing methodology choices the SCOPE got partly wrong

The hyperion-authored SCOPE makes three input-assumption errors that the round must correct before it can answer the SCOPE's own question. Naming them explicitly here per methodology lesson 9.

### Choice 1: the ballistic coefficient does NOT decrease with smaller chunk when tug mass is held fixed.

SCOPE lines 87-89 argue: "smaller chunk → smaller β → less drag needed → shallower periapsis". The mass-invariance of internal stress at equal periapsis is correctly identified (line 87). The β-rescue argument that follows is geometrically broken.

Computing directly: β = m_total / (Cd × A_chunk), with A_chunk = π × r² and r ∝ m_chunk^(1/3). Holding tug = 63.8 t (Round F 500-kilowatt-electric MARVL-anchored) and Cd = 1.0:

| Chunk mass (t) | r (m) | A (m²) | β with tug (kg/m²) |
|---:|---:|---:|---:|
| 50 | 2.35 | 17.4 | 6,546 |
| 100 | 2.96 | 27.6 | 5,936 |
| 200 | 3.73 | 43.8 | 6,022 |
| 350 | 4.50 | 63.6 | 6,505 |

β is **minimised** at chunk mass 100 t (≈ 5,936 kg/m²), worsens at both 50 t (smaller frontal area can't accommodate the fixed tug behind it) and 350 t (extra mass outpaces extra area). The SCOPE's "β = 4,400 at 50 t chunk" assumed no tug; that input assumption does not match the architecturally-relevant cell. Smaller-chunk-as-β-rescue is foreclosed.

A real β-reduction would require decoupling windward area from chunk size — a deployable drag skirt (R-deployable-drag-skirt, named as a separate follow-on in R-chunk-as-heat-shield's revisit clause). The hybrid round cannot inherit a benefit that requires a different round.

### Choice 2: pass-1 Δv to "insert into elliptical orbit" is the SAME as Δv to fully capture, both ≥ 4.18 km/s at periapsis 75 km.

SCOPE pre-registers pass-1 Δv target = 5.0 km/s (line 68) as a "65 percent of total" engineering judgment, with the implication that this is much easier than full capture. It is not. To insert into ANY captured orbit (apoapsis < ∞), specific orbital energy must drop from positive to negative — equivalently, v at periapsis must drop below local escape velocity. At periapsis altitude 75 km (r_p = 6,453.137 km), v_escape = √(2µ/r_p) = 11.115 km/s. With entry v = 15.289 km/s (Round F, aphelion 11 AU, no lunar-gravity-assist), the **minimum pass-1 Δv to insert is 15.289 − 11.115 = 4.175 km/s**. That is 83 percent of the SCOPE's 5.0 km/s target. The "hybrid relaxes pass-1" intuition is geometrically false: the deep-periapsis requirement is set by the parabolic-velocity threshold, not by the aerobraking residual.

This matters because the SCOPE then estimates pass-1 peak g at 25 g (line 72, "shorter pulse"). At 4.175 km/s rather than 5.0 km/s the difference is only ~17 percent — the structural failure does not relax. Hyperion's R-aerocapture-fast-cruise-envelope already measured 47.9 g and chunk tensile margin 0.62× for full capture at the same vehicle; the hybrid pass-1 sits in the same regime.

### Choice 3: single-scale-height exponential atmosphere is wrong above 110 km.

R-chunk-as-heat-shield and R-aerocapture-fast-cruise-envelope both use a single 7.5-km exponential scale height anchored at 5.6e-7 kg/m³ at 100 km. This matches US Standard 1976 within a factor of ~2 between 90-110 km but **underestimates density by ~40× at 180 km** (because real-atmosphere scale height grows from ~6 km at 90 km to ~22 km at 180 km, where the upper thermosphere is dominated by light species at near-isothermal high temperature). For pure-aerocapture rounds this discrepancy was inert — those rounds operated entirely below 110 km. For a hybrid round whose aerobraking campaign sits at 130-200 km, the choice dominates the verdict.

This round adopts a piecewise log-linear interpolation over the US Standard 1976 tabulated values (NASA SP-3084 / NRLMSISE-00 quiet-sun proxy) for ALL altitude calculations. The same lookup table services both regimes, removing internal inconsistency. Validity caveats below document the methodology choice; sensitivity check against hyperion's exponential is included for cross-comparison.

### Surfaced for PROTOCOL update queue

The atmosphere-model discrepancy across rounds (R-chunk-as-heat-shield tabulated values that match US Standard at some altitudes and miss it by 30× at others; hyperion's single-exponential that's quietly accurate at 100 km and wrong at 180 km; phoebe's prior round inheriting hyperion's choice) is a recurring-bug pattern across the aerocapture-adjacent rounds. Worth a candidate PROTOCOL methodology lesson 10 if this round's verdict is heavily atmosphere-dependent. Annotated in the Revisit clause.

---

## Question this round answers

For a vehicle entering Earth atmosphere at v_entry in the range 13.5-15.5 km/s (slow cruise + lunar-gravity-assist through fast cruise no-lunar-gravity-assist), chunk mass 50-350 t, tug mass 40-115 t (200/500/1000 kilowatt-electric reactor class):

1. **Pass-1 envelope.** What periapsis altitude h₁ is required to bleed at least the pass-1 minimum Δv (≥ 4.18 km/s, set by parabolic-velocity threshold)? At that altitude, does the chunk survive structurally (internal stress < 1.0 MPa tensile)? Does the bag fail thermally — sacrificed by design — or does the chunk surface ablate beyond economically tolerable bounds? Does the pulse duration exceed the orientation-stability gap left by R-chunk-as-heat-shield-revisit?

2. **Aerobraking envelope.** Given pass-1 insertion into an elliptical orbit, what aerobraking periapsis h₂ produces a tractable pass count (≤ 100,000 passes, corresponding roughly to time ≤ 5 yr at average orbital period ~1.5-2 hr) while keeping the chunk surface T_eq low enough to limit sublimation losses? Across the campaign, what total chunk mass is sublimed?

3. **Combined closure.** Does any (chunk, reactor, aphelion, lunar-gravity-assist, h₁, h₂) cell simultaneously (a) survive pass-1 structurally, (b) achieve pass-1 Δv ≥ 4.18 km/s, (c) limit chunk total sublimation to < 100 t (50 percent of chunk mass), (d) complete the aerobraking campaign in < 5 yr, AND (e) close L0-05 strict 15-yr round-trip ceiling when cruise + pass-1 + aerobraking time is added?

4. **Bag economic line.** What sacrificial-bag mass per mission is required to survive a pulse 1 of 4-5 km/s Δv at peak heat flux 10-20 MW/m²? Compare to R-chunk-as-heat-shield's 1-3 t / $5-20M anchor.

---

## Pre-registered hypothesis (H-hyb)

### Recurring-lesson-#N anchor — central estimates COMPUTED BEFORE range

Per the now-thrice-confirmed methodology intervention (R-chunk-as-heat-shield-revisit and earlier titan-2 lessons), central numerical anchors derived first via conversational back-of-envelope, before range bands written. The ranges below wrap each anchor.

**Pass-1 anchors at chunk 200 t / tug 64 t / β = 6,022 kg/m² / v_entry 15.29 km/s (no-lunar-gravity-assist, aphelion 11 AU — Round F closing cell):**

| Quantity | Anchor | Source |
|---|---:|---|
| Pass-1 minimum Δv to insert | 4.175 km/s | parabolic-threshold derivation, periapsis 75 km |
| Pass-1 Δv at periapsis 75 km, US Standard 1976 atmosphere | 53 m/s | King-Hele drag impulse: ρ × v × √(2π(R+h)H) / β |
| Pass-1 depth required for 4.18 km/s | ≤ 40 km | exhaustive sweep: only altitudes ≤ 40 km produce ≥ 4 km/s; deeper exits chunk-failure regime |
| Peak heat flux at 40 km | 20.4 MW/m² | Sutton-Graves: 1.74e-4 × √(4e-3/3.73) × (15.29e3)³ |
| Bag radiative-equilibrium temperature at 40 km | 4,600 K | (q/(0.8σ))^0.25 — every laminate fails, expected |
| Peak g at 40 km, β=6,022 | ~40 g | pulse duration / Δv = ~35 s, 2.5× peak-to-avg |
| Chunk internal stress at 40 km | ~1.3 MPa | r × ρ_ice × g_peak × g_earth |
| Chunk tensile margin at 40 km | 0.75× | ≤ 1.0 — chunk shatters |

**Aerobraking anchors at residual Δv ≈ 3.0 km/s (post-pass-1 from insertion to LEO), vehicle v ≈ 11 km/s at periapsis, β = 6,022, no bag:**

| Periapsis h₂ | ρ (kg/m³) | Δv per pass (mm/s) | Passes to dump 3 km/s | Years at 2-hr period | Chunk T_eq (K) | Total sublimation (t)* |
|---:|---:|---:|---:|---:|---:|---:|
| 110 km | 9.71e-8 | 85.5 | 35,100 | 8.0 | 953 | ~445 |
| 130 km | 8.48e-9 | 9.9 | 303,000 | 69 | 702 | ~1,505 |
| 150 km | 2.08e-9 | 2.9 | 1,040,000 | 238 | 589 | ~3,039 |
| 180 km | 5.20e-10 | 0.9 | 3,320,000 | 757 | 496 | ~6,079 |
| 200 km | 2.54e-10 | 0.5 | 6,010,000 | 1,371 | 453 | ~8,697 |

\*Total-sublimation column upper bound: heat-of-sublimation 2.83 MJ/kg, area = chunk frontal area, peak-pulse triangular integration. Real partition between body absorption and atmospheric/shock-layer dissipation may halve these numbers, but qualitative verdict (chunk consumed many times over) is robust.

### Anchored aggregate intuition

The hybrid architecture is **strongly falsified across the entire architecturally-relevant envelope** at flown-anchor atmosphere model. Three independent failure modes, any one of which closes the round:

- **Pass-1 fails structurally** at any altitude where pass-1 Δv ≥ 4.18 km/s (need ≤ 40 km, where chunk stress > tensile).
- **Aerobraking is unphysical timescale** at any altitude where chunk T_eq < ice melting point (need ≥ 180 km, where pass count ≥ 3 million and time ≥ 700 yr).
- **Chunk consumed by sublimation** at any altitude where time is tractable (need ≤ 130 km, where total sublimation ≥ 1,500 t — chunk gone ~8× over at 200 t initial).

These constraints are mutually exclusive across the periapsis axis. No interior solution exists.

### Sub-claim ranges (anchored to central estimates)

| Sub-claim | Central anchor | Predicted range (sub-claim H-hyb-N) | Falsification threshold |
|---|---|---|---|
| H-hyb-a — Pass-1 structural failure at chunk 200 t, β=6,022 | tensile margin 0.75× at depth needed for 4.18 km/s | 0.5-1.0× margin | margin ≥ 1.0× (closure of pass-1 structural) = falsified-pessimistic |
| H-hyb-b — Pass-1 structural failure at chunk 100 t (β-optimum) | tensile margin 0.85× | 0.6-1.2× margin | margin ≥ 1.2× = falsified-pessimistic |
| H-hyb-c — Pass-1 Δv achievability at periapsis 75 km, chunk 200 t, no-lunar-gravity-assist | 53 m/s achieved; 4,180 m/s required; ratio 0.013 | 0.01-0.03 | ratio ≥ 0.10 (within reach of single-altitude solution) = falsified-pessimistic |
| H-hyb-d — Aerobraking pass count at 130 km, β=6,022, 3 km/s residual | 303,000 passes | 100k-1M | < 100k = falsified-pessimistic; > 1M = falsified-conservative |
| H-hyb-e — Aerobraking total chunk sublimation at 130 km | 1,505 t | 500-3,000 t | < 500 t (chunk closes) = falsified-pessimistic |
| H-hyb-f — Aerobraking chunk T_eq exceeds ice melting at 130 km | T_eq 702 K (above 273 K melt) | 500-900 K | T_eq < 273 K = falsified-pessimistic (would imply chunk doesn't sublime) |
| H-hyb-g — Aerobraking time at 180 km (bag-survivable equivalent altitude under US Standard 1976) | 757 yr | 200-1500 yr | < 50 yr (closure within L0-05 stretch) = falsified-pessimistic |
| H-hyb-h — Lunar-gravity-assist rescue: at v_e = 13.84 km/s (lunar-gravity-assist + slow cruise + 100 t), pass-1 minimum Δv | 2.73 km/s | 2.5-3.0 km/s | unchanged (Δv reduces but periapsis depth still ≤ 50 km, structural still fails) |
| H-hyb-i — Architecture closure: any cell in (chunk, reactor, aphelion, lunar-gravity-assist, h₁, h₂) sweep simultaneously meets all five closure conditions (a)-(e) | 0 cells of ~480-cell sweep | 0-2 cells | ≥ 3 cells = aggregate falsified, hybrid has surviving region |
| H-hyb-j — Bag sacrificial mass at 10-20 MW/m² peak | 5-15 t (5× R-chunk-as-heat-shield's 1-3 t anchor, because peak flux is 2-4× higher) | 3-30 t | < 3 t = falsified-pessimistic (bag is cheaper than expected); > 30 t = falsified-conservative |

### Aggregate (H-hyb-agg)

**Prediction:** the hybrid architecture does NOT close at any cell in the architecturally-relevant envelope. The matrix's "single-pass-engineering-falsified, hybrid-engineering-pending" framing (introduced by phoebe's prior round) should be retired in favor of "atmospheric-capture-engineering-falsified, requires-deployable-drag-skirt-or-mission-architecture-pivot." The only path the hybrid architecture is consistent with is one that lowers β by deploying a drag skirt, which is a separate engineering programme (R-deployable-drag-skirt named as a follow-on by R-chunk-as-heat-shield).

If H-hyb-agg holds, the matrix collapses further. Surviving cells become: (a) Variant A under acknowledged-collapse path 2 of the bake-off (no atmospheric capture, ZERO closure), (b) Architecture-E with ≥ 25-year L0-05 waiver per enceladus-r5 round 6, (c) hybrid-conditional ONLY IF a deployable drag skirt closes engineering. The aerocapture-adjacent surviving-cell list collapses to (c)-only conditional.

If H-hyb-agg is falsified — particularly H-hyb-i ≥ 3 cells — the matrix's surviving-cell list grows back. That would also retire the methodology lesson 1 pessimistic-default pattern at the 13th aerocapture-adjacent round, suggesting domain anchor has finally over-corrected.

### Recurring-lesson watchpoints

1. **Methodology lesson 1 (pessimistic-default holds) on its 13th aerocapture-adjacent test.** Continues to be the most-reliable pre-registration heuristic in this campaign. If H-hyb-agg lands more-pessimistic-than-predicted, the lesson is reinforced; if less-pessimistic, the lesson is finally retired.
2. **Methodology lesson 7 (compute under most pessimistic credible anchor first).** This round adopts US Standard 1976 atmosphere precisely because it's more pessimistic at aerobraking altitudes (~40× denser than hyperion's exponential at 180 km — but ALSO ~30× less dense than R-chunk-as-heat-shield's tabulated 1e-4 at 90 km, so the choice goes both ways depending on regime). The aerobraking-shallow regime is the binding leg, so US Standard's denser-at-130-200-km values are the conservative choice.
3. **Methodology lesson 9 (anchor SCOPE on aggregate verdict, not cherry-picked sub-finding).** Phoebe's own lesson from the prior round. This SCOPE was authored by hyperion BEFORE running R-aerocapture-fast-cruise-envelope; consequently the SCOPE's β-rescue and pass-1-Δv-target arguments are based on input assumptions that the subsequent hyperion round itself contradicts. Three input-assumption errors documented in "Three load-bearing methodology choices the SCOPE got partly wrong" above.
4. **Atmosphere-model PROTOCOL lesson candidate.** If this round's verdict turns out to be sensitive to atmosphere-model choice (US Standard 1976 vs hyperion's exponential vs R-chunk-as-heat-shield's hand-tabulated), it's a campaign-wide methodology issue, not a round-specific one. Annotated for cross-round propagation in Revisit.

---

## Method

Detailed implementation in `run.py`.

### Atmosphere model

Piecewise log-linear interpolation over US Standard 1976 / NRLMSISE-00 quiet-sun tabulated densities, at 5-10 km intervals from 40 km to 250 km. Tabulated values (kg/m³):

```
40 km: 4.00e-3
50 km: 1.03e-3
60 km: 3.10e-4
70 km: 8.28e-5
80 km: 1.85e-5
90 km: 3.42e-6
100 km: 5.60e-7
110 km: 9.71e-8
120 km: 2.22e-8
130 km: 8.48e-9
150 km: 2.08e-9
180 km: 5.20e-10
200 km: 2.54e-10
250 km: 6.07e-11
```

Local scale height computed adjacent-altitude pair-wise. Tracked as a function for use in drag-pass-Δv formula.

### Drag-pass Δv per pass (King-Hele)

For a high-eccentricity orbit grazing periapsis r_p at velocity v_p:

```
Δv_pass = ρ(h_p) × v_p × √(2π(R_E + h_p) × H_local) × Cd × A / m_total
        = ρ(h_p) × v_p × √(2π(R_E + h_p) × H_local) / β
```

where H_local is the local scale height at h_p. This formulation is asymptotically exact for r_p / H >> 1 (Mars/Venus/Earth aerobraking heritage validates within ~30 percent).

### Pass-1 envelope

Sweep:
- Chunk mass {50, 100, 200, 350} t
- Tug mass {40, 64, 115} t (corresponding to {200, 500, 1000} kilowatt-electric reactor class per rhea round MARVL anchoring)
- Cruise aphelion {9.58, 11.0} AU (slow Hohmann, faster cruise)
- Lunar-gravity-assist credit {0, 2} km/s
- Pass-1 periapsis {40, 50, 60, 70, 75, 80, 85, 90} km

For each cell:
1. Compute v_entry at atmospheric interface (125 km) via v_∞ + lunar-gravity-assist credit.
2. Compute Δv achievable at that periapsis under King-Hele.
3. Compute Sutton-Graves peak heat flux at periapsis density.
4. Compute peak g (decel) and chunk internal stress (radius × density × g_peak).
5. Test: pass-1 captures? structural? bag thermally survives? (Bag presumed sacrificial; flag if ablation < 30 percent, indicating recoverable design.)
6. Compute residual Δv to dump in aerobraking = (entry velocity at pass-1 periapsis) − (LEO circular velocity at periapsis).

### Aerobraking campaign

For each cell that survived pass-1 (structural + capture):
1. Iterate over aerobraking periapsis {110, 130, 150, 180, 200} km.
2. Compute Δv per pass at v_p = average periapsis velocity (~11 km/s decaying to ~7.7 km/s; use mean).
3. Pass count = residual Δv / Δv per pass.
4. Total time = pass count × average orbital period (~1.5-2 hr; assume 2 hr conservative).
5. Chunk T_eq per pass (peak): (q_peak / (ε × σ))^(1/4) for ε = 0.8.
6. Chunk sublimation per pass: 0.5 × q_peak × area × pulse_duration / heat_of_sublimation; total = passes × per-pass mass × boundary-layer-blocking factor (0.6) × absorbed fraction (0.5).
7. Test: time < 5 yr AND sublimation < 100 t AND T_eq < ice surface failure (~500 K above which sublimation rate dominates).

### Closure test

A cell closes IFF all five conditions:
- (a) Pass-1 captures: pass-1 Δv ≥ Δv_insert = v_entry − v_escape(h₁).
- (b) Pass-1 structural: chunk tensile margin > 1.0.
- (c) Aerobraking finite: time < 5 yr (allowing 10 yr cruise budget within L0-05 strict 15 yr).
- (d) Chunk sublimation tractable: total sublimation < 100 t (50 percent of 200 t chunk; 50 percent of 100 t chunk = 50 t; floors at chunk_mass / 2).
- (e) L0-05 closure: total round-trip < 15 yr accounting for cruise + pass-1 + aerobraking.

### Sensitivity check

For comparison with prior rounds, sweep all cells at hyperion's exponential atmosphere model (ρ₀ = 5.6e-7 kg/m³ at 100 km, H = 7.5 km) and compare verdicts.

### Cross-check against hyperion's R-aerocapture-fast-cruise-envelope

Re-run the Round-F STRICT cell (chunk 200 t, tug 63.8 t, aphelion 11 AU, no-lunar-gravity-assist, pass-1 only, with my US Standard 1976 atmosphere) and compare measured peak g and stress to hyperion's 47.9 g / 1.6 MPa. Agreement within ±30 percent validates the methodology choice; greater discrepancy means atmosphere-model choice is binding and round verdict carries an explicit caveat.

### Validity caveats

1. **King-Hele drag-pass formula is exact for r_p / H >> 1; pulses below ~50 km altitude where the atmosphere becomes structurally thick (boundary layers, finite turning rate) are extrapolations.** Periapsis altitudes 40-45 km are extrapolated; verdict at those altitudes is conservative (real drag may differ).
2. **Sutton-Graves stagnation-point heat flux.** Average heat flux across the windward face is 0.3-0.5× q_peak. The round's chunk-sublimation calculation uses q_peak × area as upper bound; real partition halves the answer.
3. **Boundary-layer-blocking factor (BLBF) for water ice ablation.** Treated as 0.4 (PICA-X-class lower end; water-ice properties less-characterized). Real value 0.3-0.7. Sublimation estimates carry ±50 percent.
4. **Body-absorbed fraction of incident heat.** Treated as 0.5 — half of incident is absorbed by surface, half re-radiated by shock layer. Real value 0.3-0.6. Combined with BLBF, total sublimation uncertainty ±2-3×.
5. **Chunk thermal inertia and between-pass radiation.** Between-pass cooling assumed perfect (chunk surface re-equilibrates to deep space by next pass). If not, surface temperature ramps; sublimation rates rise super-linearly. This round's estimate is therefore a LOWER bound on chunk loss.
6. **Pass-1 attitude control.** R-chunk-as-heat-shield-revisit's binding open question (orientation stability through pulse) is still unscoped. This round assumes it closes; if it does not, the entire round is conditional on that prior gap.
7. **Lunar-gravity-assist epoch dependence.** Lunar-gravity-assist credit 2 km/s is favorable-geometry value; 60-85 percent of arrival epochs per R2 round; 15-40 percent of epochs would give 0 credit.
8. **Outbound chemical-kick economics.** Even if hybrid closed engineering, outbound burn requires 145-174 t hydrolox per mission (hyperion's R-outbound-chemical-kick-economics, retracted from 715 t). Orthogonal but related sleeper falsifier.
9. **Backward planetary-protection.** Multi-month aerobraking of Saturn-system material near LEO is a COSPAR Category III/IV issue. Not addressed.
10. **L0-05 ceiling assumed fixed at 15 yr.** Stretch 20 yr or 25 yr ceilings would be required for hybrid closure even at the best-case (110 km) aerobraking; this round flags but does not assume relaxation.

---

## Out-of-scope (deferred to follow-on rounds)

- **R-deployable-drag-skirt:** the only architecturally-credible β-reduction lever. Mass penalty for inflatable 100-500 m² windward area; whether the mass deficit closes Variant C economically. **If hybrid is falsified at every cell, this becomes the next critical-path round.**
- **Pass-1 attitude control through pulse.** Still unscoped from R-chunk-as-heat-shield-revisit.
- **Tug aerodynamic wake survival.** Tug behind chunk is shadowed for stagnation but wake-exposed for convective heating. Not modeled.
- **Bag thermal-protection-system detailed design.** This round estimates bag sacrificial mass; full design is a separate programme.
- **Mission-architecture pivots** (lunar-orbit catcher, cislunar processing). Out of scope for atmospheric-arrival branch.

---

## Revisit clause

Grade H-hyb-a through H-hyb-j against measured outputs. Aggregate H-hyb-agg: aggregate held iff 7-of-10 sub-claims held AND no surviving cells (H-hyb-i ≤ 2). If H-hyb-i ≥ 3, aggregate falsified regardless of sub-claim count.

**Three propagations to ARCHITECTURE-DECISION-MATRIX.md:**

1. If H-hyb-agg holds: retire the "hybrid-engineering-pending" framing introduced by phoebe's prior round; replace with "atmospheric-capture-falsified-without-drag-skirt." The aerocapture-conditional rows become drag-skirt-conditional.
2. If H-hyb-agg falsified-pessimistic: refine matrix to "hybrid-conditional-on-specific-cell" with the surviving cell's parameters explicit.
3. Atmosphere-model methodology caveat — flag for PROTOCOL update queue regardless of verdict, because three rounds have used three different atmosphere models and verdicts are sensitive to this choice.

**Next-round candidates:**

- **R-deployable-drag-skirt** (highest priority if hybrid falsified): does inflatable ballute close engineering with mass penalty ≤ 10 t? Establishes whether atmospheric capture has any surviving cell at all.
- **R-mission-architecture-pivot-survey:** lunar-orbit catcher, cislunar processing, Earth-rendezvous via lower-energy trajectories. Out of the atmospheric-capture branch entirely.
- **R-program-class-reframe-2:** if both hybrid and drag-skirt fail engineering, the program's foundational delta-velocity-minimization premise needs re-derivation. Phoebe flagged this candidate previously; orchestrator deferred.

**Recurring-lesson 4th datapoint candidate:** if H-hyb-agg holds and pre-registration was correctly pessimistic, the campaign has now seen 4 aerocapture-adjacent rounds (R-chunk-as-heat-shield, R-aerocapture-fast-cruise-envelope, R-chunk-as-heat-shield-revisit, R-hybrid) all return more-pessimistic-than-pre-registered, with cumulative falsification of progressively-narrower architectural hopes. The methodology lesson 1 base rate at end of this round will be 4/4 in the aerocapture domain.
