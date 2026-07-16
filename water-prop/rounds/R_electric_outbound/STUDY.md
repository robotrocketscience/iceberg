# R-electric-outbound — at what reactor era does all-electric end-to-end fit inside the 15-year L0-05 ceiling?

**Status:** pre-result.

## Question

R-outbound-architecture (commit 72c6077) imposed a constant 6.9× launch-mass multiplier on every cell of the architecture decision matrix by assuming a hydrolox chemical kick stage for the Earth-departure burn. That round implicitly dismissed all-electric outbound on timeline grounds — too slow — but never quantified the timeline against the 15-year round-trip ceiling fixed by L0-05.

R-radiator-mass-penalty (commit ad8156c) then showed that the matrix's bundled "10 watts-per-kilogram total electrical specific power" formula carries a hidden ~3× margin at megawatt class. A 1 megawatt-electric stack under physically-defensible component-level scaling masses ~29 tonnes dry, not the ~100 tonnes the bundled formula implied. Megawatt all-electric vehicles are therefore substantially smaller than the matrix has been costing them.

These two findings interact. If a megawatt all-electric vehicle is ~29 tonnes dry rather than ~100 tonnes, its outbound spiral-out time at fixed thrust-to-mass scales correspondingly. The question this round answers:

**For each reactor power class in the architecture decision matrix, what is the all-electric round-trip time, and at what reactor era does an all-electric end-to-end mission close inside the 15-year L0-05 ceiling?**

If a reactor era exists where all-electric end-to-end closes inside 15 years, the 6.9× chemical-kick tax (and the depot-architecture prerequisite that comes with it) can be eliminated for that era.

## Pre-registered hypothesis (H-eo)

**Aggregate (H-eo-agg):** A 1 megawatt-electric all-electric end-to-end mission closes the round trip in 12–14 years total, eliminating the 6.9× chemical-kick launch-mass tax for the megawatt era. Sub-megawatt (200–500 kilowatt-electric) is borderline at 14–16 years, fitting inside L0-05 only at the favourable end of the band. Kilopower (10–40 kilowatt-electric) bursts the budget — the outbound burn alone exceeds 5 years at the available thrust-to-mass.

**Pre-registered sub-claims:**

| Sub-claim | Predicted | Falsification |
|---|---|---|
| H-eo-a — Outbound delta-velocity from low Earth orbit to trans-Saturn trajectory, derived from circular-orbit speed plus Hohmann excess | 8.5–9.5 km/s | outside this band |
| H-eo-b — Outbound spiral time at 1 megawatt-electric, decomposed-mid tug dry mass, specific impulse 2000 s | 1.5–3.0 years | outside this band |
| H-eo-c — Outbound spiral time at 200 kilowatt-electric, decomposed-mid | 5–9 years | outside this band |
| H-eo-d — Outbound spiral time at 40 kilowatt-electric, decomposed-mid | exceeds 15 years (infeasible) | held if > 15 yr; falsified if < 15 yr |
| H-eo-e — Total round-trip at 1 megawatt-electric, decomposed-mid (all-electric end-to-end) | 12–14 years | outside band |
| H-eo-f — Smallest reactor that closes all-electric end-to-end inside 15 years | between 200 and 1000 kilowatt-electric | falsified if < 200 kWe or no class closes |
| H-eo-g — Bundled-formula dry-mass tug (matrix's current rule) closes all-electric end-to-end at the same reactor era as decomposed-mid, within ±1 reactor class | held | falsified if the close-era differs by ≥2 classes |

**Aggregate decision:** if H-eo-agg holds — i.e. some reactor era closes all-electric end-to-end inside L0-05's 15-year ceiling — propagate to `ARCHITECTURE-DECISION-MATRIX.md` to add an "all-electric outbound" option for that era, dropping the 6.9× chemical-kick multiplier and the depot-prerequisite annotation for cells at or above the close-era reactor class. If H-eo-agg falsifies, the chemical-kick outbound assumption (and the 6.9× tax) is confirmed structural across the matrix.

## Method

### Delta-velocity budgets

**Outbound** (low Earth orbit → trans-Saturn Hohmann injection):

Derive from first principles rather than assuming. Low Earth orbit circular speed at 400 km altitude is v_circ = sqrt(GM_Earth / r_LEO) ≈ 7.67 km/s. Earth-escape from low Earth orbit is sqrt(2)×v_circ - v_circ ≈ 3.22 km/s impulsive. Departure hyperbolic excess (C3) to reach Saturn via Hohmann is computed from the Hohmann transfer at 1 astronomical unit perihelion / 9.58 astronomical unit aphelion. The total impulsive outbound is the "Oberth-effective" combined Earth-escape + Hohmann ejection: Δv_out = sqrt(v_escape² + v_∞²) - v_circ.

For all-electric outbound this *impulsive* delta-velocity is not what the vehicle actually flies — the Edelbaum spiral pays a larger total integrated delta-velocity than the impulsive budget because each velocity addition is tangential to a slowly-expanding circular orbit. Edelbaum's closed-form for circular-to-escape spiral gives integrated Δv = v_circ_LEO (the spiral asymptotes at the circular orbit speed at the starting altitude). After escape the spacecraft is on a hyperbolic trajectory and the post-escape Hohmann excess is added closed-form.

So:
- Δv_spiral_LEO_to_escape = v_circ_LEO ≈ 7.67 km/s (Edelbaum)
- Δv_post_escape_to_Saturn_Hohmann = v_∞_Earth at Hohmann (computed from orbital mechanics)
- Δv_outbound_total_electric ≈ 7.67 + v_∞_Earth ≈ 7.67 + 8.79 ≈ but the post-escape leg is hyperbolic and far from Earth so the linear-addition approximation overstates it; the proper closed-form is Δv_outbound = Δv_spiral + v_∞ where v_∞ is the heliocentric excess after Earth escape.

The exact decomposition: Edelbaum spiral from low Earth orbit to Earth-escape costs an integrated Δv equal to v_circ_LEO. Once escaped (at zero geocentric energy, i.e. v_∞_geocentric = 0), the spacecraft is at Earth's heliocentric orbit speed (~29.78 km/s). To reach Hohmann perihelion velocity (~40.07 km/s, computed below), it needs Δv_helio = v_Hohmann_peri - v_Earth ≈ 10.3 km/s. Continuous low-thrust does NOT get the Oberth bonus, so this 10.3 km/s is paid in full.

Total outbound electric Δv ≈ 7.67 + 10.3 = ~17.9 km/s.

This is much higher than the prompt's stated ~9 km/s. The prompt's 9 km/s figure is the impulsive Oberth-discounted budget; all-electric pays the full non-Oberth budget. **This is the assumption I am explicitly questioning per the prompt's "constant-thrust approximation" item.**

**Cruise:** Hohmann ballistic transfer time = π × sqrt(a_h³ / GM_sun), where a_h = (1 + 9.5826) / 2 AU. Computed in `run.py`. (Continuous low-thrust trajectories can shorten cruise modestly by phasing the burn through perihelion / aphelion, but for first pass we treat the spacecraft as coasting after Hohmann injection; thrust ends at Hohmann perihelion velocity, vehicle is ballistic to Saturn.)

**Saturn-side operations:** 1 year fixed budget (capture, bag deployment, harvest, departure). Consistent with R-outbound-architecture and the architecture matrix.

**Inbound:** 6.42 km/s electric (chunk-fed) per R8 / R10_inbound_propulsion_revisit. Post-lunar-gravity-assist residual. Treated as one continuous burn at electric specific impulse 2000 s. Cruise back: same Hohmann time.

### Spiral / burn-time model

For each (reactor power, dry-mass model) pair:

1. Compute tug dry mass at that reactor class under both bundled-10-W/kg and decomposed-mid models (lifted from R-radiator-mass-penalty).
2. Outbound vehicle initial mass at low Earth orbit = m_tug + outbound_propellant. Propellant from rocket equation at Δv_outbound_electric and v_e = Isp × g₀ (no payload on the outbound leg — the vehicle is empty, picking up its chunk at Saturn).
3. Available thrust: F = 2·η·P_electric / v_e where η = 0.65 (RF ion at 2000 s, consistent with prior rounds).
4. Outbound burn time (Edelbaum + heliocentric leg) at constant thrust: t_out = m_prop_out × v_e / F. Note: this is the standard constant-thrust integration; mass decreases over the burn, so this is an approximation in the same family used by prior rounds (R-reactor-specific-power, R-outbound-architecture). At low mass-ratios it is accurate within 5%.
5. Cruise out: Hohmann transfer time, ballistic.
6. Saturn ops: 1 year.
7. Inbound burn time at constant thrust: same formula but with initial mass = m_tug + chunk; chunk = 200 t (matrix mid-cell baseline).
8. Cruise back: same Hohmann time.
9. Round-trip total = outbound burn + cruise out + Saturn ops + inbound burn + cruise back.

### Sweep axes

- Reactor power: 10, 40, 100, 200, 500, 1000 kilowatt-electric
- Dry-mass model: bundled-10-W/kg, decomposed-mid (both)
- Outbound electric Isp: 2000 s (matched to inbound; per the prompt, the Isp-matching question is checked separately as a sensitivity)
- Chunk mass: 200 t fixed (architecture-matrix mid cell; sensitivity to 100 / 500 t in tables)

### Sensitivity / assumption-questioning

- **2000 s electric Isp on outbound.** Sweep also at 3000 s and 4000 s (dual-ion / high-Isp Hall) to see whether higher Isp shortens or lengthens outbound. Higher Isp means lower thrust at fixed power, so longer burn; lower propellant means smaller initial mass and faster acceleration. The tradeoff is non-monotone.
- **Edelbaum approximation accuracy.** For the LEO-to-escape phase, Edelbaum's integrated Δv = v_circ_LEO is the well-known closed-form (Edelbaum 1961, "Propulsion requirements for controllable satellites"). It assumes planar, low-thrust, slowly-changing-orbit spiral. For hyperbolic-escape, the standard correction is to treat the LEO-to-escape phase via Edelbaum and the post-escape heliocentric phase via "tangential continuous burn" against the Sun's gravity — i.e. add v_∞_Earth as the heliocentric Δv. See Sauer (1973), "Optimization of multiple-target electric propulsion trajectories."
- **6.9× chemical-kick multiplier from R-outbound-architecture.** Re-derive from rocket equation at Δv_kick = 7.3 km/s, Isp = 450 s, kick stage dry/wet = 0.1, electric capture Δv = 2 km/s at Isp = 2000 s — confirm the multiplier holds.
- **Solar-electric versus nuclear-electric.** Solar power scales 1/r² with heliocentric distance; at Saturn's distance the solar flux is ~1.1% of Earth's. Solar-electric is plausible for the inner-AU phase of outbound, nuclear takes over thereafter. Not modeled — flagged as a sentence in Reading.

### Validity caveats

- The Edelbaum-plus-heliocentric integrated-Δv model overstates outbound burn time relative to optimal-control trajectories (which can use perihelion / aphelion phasing and gravity-assist sequences to shave the integral). It is correct to within 10–20% for "vanilla" continuous-thrust electric outbound, which is the relevant comparison for L0-05 closure.
- The constant-thrust approximation treats thrust as constant over the burn while mass falls. At outbound mass-ratios under 2 (typical here) the error is ~5%.
- Reactor cycle life under multi-year continuous burn is not modeled. Kilopower-class designs target 10–15 years of cycle life. A 5-year continuous outbound burn plus 5-year inbound burn is 10 years on-time, which is borderline. Flagged for follow-up.
- Solar-electric augmentation for the inner-AU phase of outbound not modeled. If feasible (R-solar-electric-augment-outbound, not in scope here), it would reduce nuclear-electric burn time for the first ~year of outbound.
- The "chunk = 200 t fixed" baseline is a matrix mid-cell. Sensitivity to chunk size shown in tables. The inbound burn time scales sublinearly with chunk: bigger chunk means larger initial mass but the same Δv, so propellant scales linearly and burn time scales linearly with chunk. Outbound burn is chunk-independent.

## Result

Run output at `results/electric_outbound.json` and `results/tables.md`.

**Hypothesis grading:**

| Sub-claim | Predicted | Actual | Held? |
|---|---|---|---|
| H-eo-a — Outbound Δv (first-principles continuous-burn) | 8.5–9.5 km/s | **17.97 km/s** | falsified (≈2× higher) |
| H-eo-b — Outbound burn at 1 megawatt-electric (decomposed-mid) | 1.5–3.0 yr | **0.17 yr** | falsified low (≈10× faster) |
| H-eo-c — Outbound burn at 200 kilowatt-electric (decomposed-mid) | 5–9 yr | **0.24 yr** | falsified low (≈25× faster) |
| H-eo-d — Outbound burn at 40 kilowatt-electric exceeds 15 yr | > 15 yr | **0.59 yr** | falsified (outbound is not the bottleneck) |
| H-eo-e — Round-trip at 1 megawatt-electric (decomposed-mid) | 12–14 yr | **13.94 yr** | held (top of band) |
| H-eo-f — Smallest reactor closing all-electric end-to-end inside 15 yr | between 200 and 1000 kWe | **500 kWe** (decomposed-mid) | held |
| H-eo-g — Bundled and decomposed-mid close within 1 reactor class | within 1 class | bundled 1000 kWe / decomposed-mid 500 kWe → 1-class gap | held (at the edge) |

**Aggregate (H-eo-agg): held in headline, mechanism falsified.** All-electric end-to-end closes inside L0-05's 15-year ceiling at 500 kilowatt-electric (decomposed-mid) or 1000 kilowatt-electric (bundled-10-W/kg). The headline prediction — "megawatt class closes around 12–14 years" — held at 13.94 years. But the *reasoning* behind that prediction was structurally wrong: I expected outbound burn to be the rate-limiting step, with megawatt class being the first era where outbound spiral time becomes tractable. Outbound burn turns out to be almost negligible across the entire sweep. The 15-year ceiling is consumed almost entirely by ballistic Hohmann cruise (12.17 yr round-trip) plus inbound burn time (which is the actual rate-limiting step at low reactor power).

## Reading

**The mechanism was inverted.** I had cast this round as "does megawatt-class give enough thrust to spiral out of low Earth orbit fast enough to fit inside 15 years?" The answer is: outbound burn time is trivial at *every* reactor class above ~100 kilowatt-electric. The actual rate-limiting step is the *inbound* burn — vehicle plus chunk burning 6.42 km/s at electric specific impulse 2000 s — which is what the matrix has been computing for two campaigns under the seven-year-burn-cap convention.

Specifically:

- Outbound burn at 1 megawatt-electric, decomposed-mid tug: **0.17 years** (≈2 months).
- Inbound burn at the same power with a 200-tonne chunk: **0.60 years**.
- Hohmann cruise each way: **6.09 years**.
- Sum: 0.17 + 6.09 + 1.00 + 0.60 + 6.09 = **13.94 years**, of which 87% is ballistic cruise.

At sub-megawatt power, inbound burn balloons fast (5.4 yr at 100 kWe, 13.4 yr at 40 kWe, 53 yr at 10 kWe with a 200 t chunk) while outbound burn stays under a year. The matrix's seven-year burn cap, originally pitched as a "burn-life ceiling," is in this view a proxy for L0-05: the cap exists because if the inbound burn exceeds 7 years, round-trip exceeds 14 years, and L0-05 is at risk.

**Two assumptions I made that turned out to be wrong:**

1. **The prompt's "outbound Δv ~9 km/s" figure was wrong for all-electric.** That 9 km/s is the *impulsive* (Oberth-discounted) budget — a single chemical burn at perigee gets a velocity bonus by burning deep in Earth's gravity well. All-electric continuous-thrust does not get the Oberth bonus. The Edelbaum spiral from low Earth orbit to Earth-escape integrates to v_circ_LEO ≈ 7.67 km/s (Edelbaum 1961), and after escape the spacecraft must add the full heliocentric excess v_∞_Earth ≈ 10.3 km/s to reach Hohmann perihelion velocity, paid in full. Total integrated outbound Δv is **17.97 km/s, roughly twice the impulsive figure.** I accepted the prompt's stated 9 km/s in my hypothesis (H-eo-a) and was promptly falsified. The flag-and-question-the-assumption instruction in the prompt was load-bearing: this is the single biggest first-principles correction in the round.

2. **I assumed outbound spiral time would dominate at sub-megawatt.** It does not. Even at 40 kilowatt-electric, outbound burn is 0.59 years. The vehicle is small (a few tonnes dry), the propellant fraction is modest (mass ratio ≈ 2.5 at 17.97 km/s, Isp 2000 s), and the burn finishes in months. The big inbound-mass + chunk + 6.42 km/s burn is what eats years of timeline. **My intuition was anchored on chemical-rocket scaling, where the spiral phase is the dominant cost** because Hall-thruster spacecraft burn most of their propellant getting out of Earth's gravity well. For ICEBERG, the outbound vehicle is empty (chunk is picked up at Saturn); the inbound vehicle is full. That asymmetry is the dominant cost driver, and I missed it.

**The 6.9× chemical-kick multiplier from R-outbound-architecture re-derived as 10.92× / m_v_clean.** Both numbers are consistent: R-outbound's 6.9× compares chemical-kick LEO mass to all-electric-outbound LEO mass (the latter already including outbound propellant; mass ratio 1.583 at impulsive Δv 9 km/s, Isp 2000 s); my 10.92× compares chemical-kick LEO mass to the clean vehicle dry mass. 10.92 / 1.583 = 6.9, exactly. Both representations are correct relative to their baseline. The matrix should pick one and state it explicitly to avoid future confusion.

**Implications for the architecture decision matrix:**

1. **At 500 kilowatt-electric (decomposed-mid) or 1000 kilowatt-electric (bundled-10-W/kg), all-electric end-to-end closes inside L0-05's 15-year ceiling.** The 6.9× chemical-kick launch-mass tax can be dropped for these cells. The depot-architecture prerequisite annotation can be dropped for these cells. The mission-1 financing problem (R-outbound-architecture's "build the depot from scratch" sub-problem) does not apply to these cells.

2. **At ≤200 kilowatt-electric, all-electric end-to-end exceeds 15 years.** The chemical-kick architecture (or some equivalent outbound-mass-amplifier) remains structural for these cells.

3. **The matrix should add an "outbound-architecture column" to each cell.** Currently the matrix reads as if chemical-kick is the only option. From this round, all-electric end-to-end is an option for ≥500 kilowatt-electric (decomposed-mid) or ≥1000 kilowatt-electric (bundled). Architecture choice per cell:

   | Reactor era | Best outbound | Why |
   |---|---|---|
   | ≤ 100 kilowatt-electric | chemical-kick | inbound burn > 5 yr alone; all-electric round-trip > 18 yr |
   | 200 kilowatt-electric | chemical-kick (borderline) | 16.1 yr all-electric, just over L0-05 |
   | 500 kilowatt-electric | **all-electric** (decomposed-mid) or chemical-kick (bundled) | decomposed-mid: 14.5 yr; bundled: 15.2 yr |
   | ≥ 1000 kilowatt-electric | **all-electric** | 13.9 yr decomposed-mid; 14.6 yr bundled |

4. **The Edelbaum + heliocentric Δv = ~18 km/s figure should replace the "9 km/s outbound" assumption in any future round that touches the outbound architecture.** Every prior round that quoted "all-electric outbound mass ratio 1.583" was using the impulsive-equivalent figure, which understates true all-electric outbound propellant by roughly 2× in Δv (mass ratio jumps from 1.583 to ~2.50 at Isp 2000 s).

5. **Specific-impulse sensitivity is favorable.** At 1 megawatt-electric, sweeping outbound Isp from 2000 s to 4000 s adds only 0.9 yr to round-trip (13.94 → 14.88). Both close inside 15 yr. Higher Isp drops propellant mass (better delivered fraction) at modest timeline cost. Dual-ion / high-Isp Hall-effect thrusters are not penalized by the timeline ceiling in the megawatt era.

**What this round still papers over:**

- **Solar-electric augmentation for the inner-AU phase of outbound** not modeled. Sun is ~1.1% as bright at Saturn as at Earth, so solar-electric on the way out is plausible for the first AU. This would reduce nuclear-electric reactor on-time and is worth a sentence: at 1 AU, a 100-kilowatt solar array masses ~500 kg (200 W/kg) versus a 100-kilowatt-electric nuclear stack at ~2.5 tonnes (decomposed-mid). Solar dominates inside ~3 AU; nuclear dominates beyond. Composite outbound-power systems are a real concept (Project Prometheus, Mars Cargo Transport) but adding them here would be over-scoping.
- **Reactor cycle life under 14-year mission** not modeled. Kilopower-class targets 10-15 yr cycle life. Megawatt-class reactor cycle-life data is sparse but space-qualified designs typically target ~10-year cycle life. A 14-yr round-trip with continuous reactor operation throughout cruise is borderline. Real concept-of-operations probably idles the reactor during ballistic cruise (drops power-conversion thermal cycle count); this is consistent with prior matrix assumptions but should be flagged for R-reactor-cycle-life.
- **Trajectory optimization** (gravity assists, low-thrust shaping, perihelion / aphelion phasing) not modeled. Real low-thrust missions can shave 10-20% off the "vanilla" continuous-thrust budget through optimal-control trajectory shaping. Applied here, the megawatt close-margin would improve from 1 year to ~3 years; the 500-kilowatt-electric close-margin from 0.5 year to ~2 years.
- **Reactor startup time and shielding mass for crew-free vehicle** assumed instant. Real nuclear-electric stack has multi-day startup and a small shielding penalty against the spacecraft electronics; both are small versus the round-trip budget but should be itemized in a downstream round.

**Methodology lesson, candidate for CONVENTIONS log:**

> When pre-registering a hypothesis about which phase of a mission is rate-limiting, check the actual time-budget allocation under the *current* model assumptions before committing to the prediction. I was anchored on the conventional-rocket intuition that outbound spiral dominates; ICEBERG's asymmetric mass profile (empty outbound, full inbound) inverts that. A 10-minute time-budget allocation table before writing the hypothesis would have flagged this. (Compare R-radiator-mass-penalty: "decompose and find a hidden penalty" was wrong half the time; here, "outbound is the bottleneck" was wrong from a similar source — anchoring on the wrong mass profile.)

This sits alongside the R-radiator-mass-penalty "lumped figures may be conservative-with-margin" lesson as a related family of unanchoring mistakes.

## Revisit clause

Grade H-eo-a through H-eo-g. If H-eo-agg holds (some reactor era closes all-electric end-to-end inside 15 years):

1. Propagate to `ARCHITECTURE-DECISION-MATRIX.md`: add an "all-electric outbound" architecture option for cells at or above the close-era reactor class, with the 6.9× chemical-kick multiplier dropped and the depot-architecture prerequisite annotation removed for those cells.
2. Update the matrix's "Important caveat on launch-mass numbers" paragraph to qualify the 6.9× multiplier as conditional on chemical-kick outbound — for the close-era cells, all-electric outbound is an option at the cost of a longer (but still L0-05-compliant) round-trip.
3. Flag for R-NPV revisit: the project internal-rate-of-return may improve materially for the all-electric end-to-end era because the mission-1 capital cost drops by ~6.9× (no chemical kick stage), and the depot-architecture build cost is no longer a prerequisite for that era's operations.

If H-eo-agg falsifies (no reactor class closes inside 15 years):

1. Confirm the chemical-kick outbound assumption as structural for the matrix.
2. Document the closing reactor-era threshold (which would need to be above 1 megawatt-electric) for a future-era propagation.
