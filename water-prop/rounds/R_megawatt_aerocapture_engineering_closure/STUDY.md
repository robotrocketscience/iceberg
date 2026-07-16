# R-megawatt-aerocapture-engineering-closure — does single-pass aerocapture close the engineering for a hypothetical year-twenty-plus megawatt all-electric end-to-end cell, and does it touch the reactor-program dependency?

**Author:** rhea (worker session, re-spawn, second sitting).
**Status:** completed (deterministic numerics in `run.py`, results graded below).
**Branch:** `iceberg-rhea-2`.
**Date:** 2026-05-15 (late).
**Protocol:** per `water-prop/PROTOCOL.md`.

---

## SCOPE-AND-LANE NOTICE (added after the fact)

This round was originally authored as `R-chunk-as-heat-shield-revisit` against Saturn's earlier SCOPE.md, targeting the year-twenty-plus megawatt all-electric end-to-end cell. **After the round ran, I discovered that Saturn had subsequently spawned iapetus with a separate ASSIGNMENT.md retargeting R-chunk-as-heat-shield-revisit at the surviving 500-kilowatt-electric all-electric inbound cell (Option A), with a new Q5 about whether aerocapture-plus-L1-007-relaxation clears the regulated-utility internal-rate-of-return hurdle.** Iapetus is the authorised worker for that scope.

To avoid colliding with iapetus's deliverable directory, this round is renamed to `R_megawatt_aerocapture_engineering_closure/`. The work below addresses **the megawatt year-twenty-plus cell** that Saturn has retired but not yet erased from the matrix (line 69 "Megawatt + chunk-as-heat-shield rescue ... Conditional"). The finding is useful because it disambiguates "the megawatt cell is engineering-infeasible" (false) from "the megawatt cell has no reactor program" (true). The matrix's line 69 graduation language should reflect the latter, not the former.

**Predecessors this session:** R-delivery-architecture (`e2fc68e`), R-delivery-destination-altitude (`c3ec48f`), R-chemical-trim-vs-all-electric-earth-arrival (`47b69bc`).
**Calibration predecessor:** R-chunk-as-heat-shield (closed, established 0.5% chunk ablation at 12.6 kilometres-per-second entry).

---

## Motivation

Per matrix line 30 and 69: chunk-as-heat-shield is the **highest-leverage open rescue path** for the year-twenty-plus megawatt all-electric end-to-end cell, which rhea round 3 (prior session, commit `bde06a2`) falsified at 19.56-year round trip / −34.4-tonne delivered under MARVL-anchored mass + continuous-thrust electric inbound. The rescue closes Earth-side ~17.97 kilometres-per-second of integrated electric delta-velocity to aerodynamic passes.

R-chunk-as-heat-shield (closed) showed the bag-survival / aerobraking branch closes cleanly (multi-pass aerobraking at 1–3 kilowatts-per-square-metre, chunk ablation under 100 kilograms). It deferred two questions to this revisit:

1. **Chunk attitude stability through a single-pass aerocapture pulse** — does the chunk reliably orient chunk-forward without tumbling, given irregular shape?
2. **Ablation at higher entry velocity** — titan's corrected inbound puts Earth-arrival at 12.5–14 kilometres-per-second, not the 12.6 the prior round used.

Architecture payoff (Saturn's SCOPE.md): if the engineering closes, year-twenty-plus megawatt delivered fraction returns from 20 percent to (predicted) 50–70 percent. **Caveat I will check independently:** the locked-finding reactor-program dependency (one-megawatt-electric = 10× Fission Surface Power Phase 2's 100-kilowatt-electric scope, posterior probability 0.10–0.30 by 2032–2035) is unchanged by aerocapture and remains the limiting dependency.

Held over from prior assumption-questioning at session start: I confirmed by reading the matrix that round 3's "chemical-kick" placement reading was correct — chemical is at Saturn-departure across all my round-3 scenarios, not at Earth-arrival. Round 3's headline finding stands.

---

## Delta-velocity decomposition (post-rescue inbound)

| Segment | All-electric (km/s, rhea round 3 + titan high-elliptical case) | With chunk-as-heat-shield (km/s) |
|---|---:|---:|
| (1) Saturn-departure (high-elliptical) | 3.3 electric | 3.3 electric (unchanged) |
| (2) Heliocentric Saturn-side decel | 5.44 electric | 5.44 electric (unchanged) |
| (3) Ballistic Hohmann cruise | 0 (time only) | 0 |
| (4) Heliocentric Earth-side decel | 8.30 electric (10.30 minus 2.0 lunar gravity assist credit) | 0 (replaced by ballistic arrival + aerocapture) |
| (5a) Earth capture | part of 7.67 electric | 0 (aerocapture) |
| (5b) Edelbaum circularisation | part of 7.67 electric | 0.3–1.0 (small post-aerocapture trim) |
| **Inbound total** | **24.7** electric (titan low case) | **~9.24 electric + aerocapture** |

The collapse is 24.7 → 9.24 kilometres-per-second of electric burn — about 15.5 kilometres-per-second of integrated thrust eliminated.

---

## Pre-registered hypotheses

All numeric ranges locked before `run.py` is executed.

### H1 — Chunk passive aerodynamic stability through aerocapture pulse

**Prediction:** Across all tested aspect ratios (1.5, 2.0, 2.5, 3.0) the chunk is **passively unstable** in the chunk-forward orientation. For a rubble-pile or irregular ice body, the centre-of-pressure shift from the centre-of-mass exceeds the restoring-torque arm at hypersonic newtonian-impact flow regime. **Active control is required.**

**Falsification:** held if no aspect ratio gives a clear static-stability margin (centre-of-pressure aft of centre-of-mass by more than 10 percent of half-length). Falsified if any aspect ratio shows passive stability.

### H2 — Reaction-control-system thrust authority required for active stabilisation

**Prediction:** The scope-sketched 1–10-newton cold-gas range is **insufficient**. Required thrust authority to counter aerodynamic torque from a 200-second hypersonic pulse at 100-tonne vehicle, 25-square-metre windward area, periapsis-altitude 90-kilometre atmospheric density, and 0.1-half-length centre-of-pressure-centre-of-mass offset is **100–1000 newtons per pair**, two-axis. Bipropellant or high-pressure cold gas, not low-pressure cold gas.

**Falsification:** held if no case with thrust ≤ 10 newtons per pair closes the 200-second pulse without exceeding 90 percent saturation. Falsified if a 1-newton or 10-newton case closes cleanly.

### H3 — Reaction-control-system propellant per pulse

**Prediction:** **20–100 kilograms** cold-gas helium per pulse. Tolerable against a tug mass budget on the order of 100 tonnes. Not a mass-budget breaker.

**Falsification:** held in 20–100-kilogram band. Falsified if > 200 kilograms (mass-budget impact requires architectural revisit) or < 5 kilograms (modelling error).

### H4 — Chunk ablation per single-pass aerocapture at 12.5–14 kilometres-per-second entry

**Prediction:** **0.2–0.6 percent** chunk mass loss per pass, across chunk masses {100, 200, 500} tonnes at the three tested entry velocities. Scaling from R-chunk-as-heat-shield's 0.5 percent calibration at 12.6 kilometres-per-second by cubic velocity dependence and area-scaling. **Below** Saturn's SCOPE.md prediction band of 1–3 percent.

**Falsification:** held in 0.2–0.6 percent band. Falsified if any sweep case exceeds 1.5 percent (architecture-degrading regime) or falls below 0.05 percent (modelling error).

### H5 — Restored delivered chunk fraction at one-megawatt-electric MARVL post-aerocapture

**Prediction:** **35–50 percent** of grappled chunk mass delivered to low Earth orbit. At one-megawatt-electric MARVL tug mass 104.9 tonnes, 200-tonne grappled chunk, specific impulse 2000 seconds, inbound electric delta-velocity 9.24 kilometres-per-second post-rescue: Tsiolkovsky predicts 42 percent. **Below** Saturn's SCOPE.md prediction band of 50–70 percent because: (a) Saturn used a more optimistic Earth-side delta-velocity collapse to 0.3 kilometres-per-second (I use 0.5 average), (b) Saturn's scope appeared to neglect the 8.74-kilometres-per-second electric burn that remains in segments (1) and (2).

**Falsification:** held in 35–50 percent. Falsified if < 25 percent (incomplete rescue) or > 60 percent (modelling error).

### H6 — Round-trip time at one-megawatt-electric MARVL with aerocapture rescue

**Prediction:** **5.5–7.0 years.** Comfortably inside Level 0 requirement L0-05's 15-year ceiling. The cell that was at 19.56 years (falsified) collapses to roughly one-third its prior round-trip duration because outbound integrated-burn-time scales as propellant-mass at fixed thrust, and propellant mass is dominated by outbound 29.56-kilometres-per-second burn (unchanged) plus the inbound 9.24-kilometres-per-second post-rescue burn (down from 24.7+).

**Falsification:** held in 5.5–7.0 years. Falsified if > 10 years (incomplete rescue) or < 4 years (modelling error).

### H7 — Reactor-program dependency unchanged by rescue

**Prediction:** **Held — the rescue does not address the megawatt-reactor-program dependency.** The year-twenty-plus megawatt cell post-rescue still requires a one-megawatt-electric reactor (10× Fission Surface Power Phase 2's 100-kilowatt-electric scope). Per locked-finding base rate (zero-of-six United States space-fission programs have reached orbit within their stated decade), posterior probability of available one-megawatt-electric reactor by the 2032–2035 demonstrator window is 0.10–0.30 with or without aerocapture rescue. The rescue closes the propulsion engineering; it does not close the reactor program.

**Falsification:** held. Falsified only if the rescue somehow relaxes the reactor power requirement below ~250 kilowatt-electric (within Fission Surface Power Phase 2 scope) — which it cannot, since outbound delta-velocity is unchanged.

### Aggregate

**Pre-registered aggregate prediction:** The rescue **closes the propulsion engineering for the megawatt all-electric end-to-end cell.** Single-pass aerocapture is engineering-feasible with the chunk as primary heat-shield, conditional on (a) active reaction-control-system attitude stabilisation at 100–1000-newton authority, (b) sub-1-percent chunk ablation per pass tolerated, (c) sacrificial-bag operations (or retractable-bag follow-on programme). Restored delivered fraction 35–50 percent, round-trip 5.5–7.0 years.

**The rescue does NOT close the reactor-program dependency.** The cell remains gated on a one-megawatt-electric reactor program that does not exist as of May 2026 and which has 0.10–0.30 posterior availability by 2032–2035.

**Saturn-side action implied if hypotheses hold as predicted:**
- Update matrix line 69 ("Megawatt + chunk-as-heat-shield rescue") from "Conditional" to "Engineering-closed, reactor-dependent."
- Add explicit row tying delivery to the reactor-availability prior.
- R-bag-sacrificial-vs-retractable becomes the next round.
- R-tug-thermal-survival becomes a parallel-blocking round (does the tug behind the chunk survive the pulse?).

---

## Method (deterministic, single-script)

`run.py` computes the four numeric outputs from closed-form / first-principles models. No Monte Carlo. Deterministic given the parameters block at the top.

### Module 1 — Chunk attitude (H1, H2, H3)

Prolate-spheroid hypersonic newtonian impact. Aspect ratio sweep {1.5, 2.0, 2.5, 3.0}. Half-length determined by chunk mass at ice density (917 kilograms-per-cubic-metre). Atmospheric density at 90-kilometre altitude: 3.4 × 10⁻⁶ kilograms-per-cubic-metre (NRLMSISE-00 nominal). Centre-of-pressure for axisymmetric prolate spheroid at zero angle-of-attack: at geometric centroid of frontal hemisphere; centre-of-mass at geometric centroid; static-stability margin is small and assumed to be perturbed by 0.05–0.15 half-length offset for irregular chunk.

Aerodynamic torque: τ = q_dyn × A_frontal × d_offset × C_M, where C_M = 0.5 for axisymmetric body at small angle-of-attack, q_dyn = ½ ρ v² dynamic pressure.

Required reaction-control thrust at moment arm = half-length: F_required = τ / (half-length). Pulse-integrated propellant: m_prop = F × t_pulse / (Isp_cold_gas × g), where Isp_cold_gas = 230 seconds (helium).

### Module 2 — Ablation (H4)

Anchor to R-chunk-as-heat-shield: peak stagnation heat flux 3.0 megawatts-per-square-metre at 12.6 kilometres-per-second entry (the prior round's midband). Scale by cubic-velocity for convective component, with radiative scaling negligible at this velocity (well below 15 kilometres-per-second where radiative dominates).

q_peak(v) = 3.0 × (v / 12.6)³ megawatts-per-square-metre.

Pulse-integrated heat load: Q = q_peak × t_effective, where t_effective = 60 seconds (peak-to-effective ratio per single-pass aerocapture profile).

Ablation mass per windward-area: m_abl / A = Q / h_ablation, where h_ablation = 25 megajoules-per-kilogram (boundary-layer-blocked sublimation, prior-round calibration).

Windward area scaling with chunk mass at fixed ice density: A(m) = A_100t × (m / 100 tonnes)^(2/3), where A_100t = 25 square-metres.

### Module 3 — Delivered chunk fraction and round-trip time (H5, H6, H7)

Tsiolkovsky rocket equation, two-leg.

Inputs:
- Tug mass M_tug = 104.9 tonnes (one-megawatt-electric MARVL, from rhea round 3)
- Electric specific impulse Isp = 2000 seconds → exhaust velocity 19,620 metres-per-second
- Outbound delta-velocity (electric continuous-thrust, high-elliptical) = 29.56 kilometres-per-second (rhea round 1, R-outbound-dv-continuous-thrust)
- Inbound delta-velocity post-aerocapture = 9.24 kilometres-per-second (Saturn-departure 3.3 + heliocentric Saturn-side decel 5.44 + post-aerocapture trim 0.5)
- Chunk masses tested: 100, 200, 500 tonnes
- Power 1 megawatt-electric, thruster efficiency 0.7, thrust = 2·P·η / v_exhaust = 71 newtons
- Mass-flow rate ṁ = F / v_exhaust

Outbound: tug + outbound propellant → tug.
M_prop_out = M_tug × (exp(Δv_out / v_e) − 1)

Inbound (chunk-fed): tug + chunk_grappled → tug + chunk_delivered.
mass_ratio = exp(Δv_in / v_e)
chunk_delivered = (M_tug + M_chunk_grappled) / mass_ratio − M_tug

Burn time per leg ≈ propellant_mass / ṁ. Coast times: 0.5 year per heliocentric segment (Hohmann-equivalent at 6-year cruise time, with continuous-thrust regime cutting in on accelerations, conservative). Saturn-side operations: 0.5 year. Earth-side aerocapture + delivery: 0.1 year.

Round-trip time: outbound-burn + outbound-coast + Saturn-ops + inbound-burn + inbound-coast + Earth-ops.

### Module 4 — Reactor-program dependency check (H7)

Read-only cross-check against the user-locked external findings:
- Locked-finding 1: forty-watts-per-kilogram is paper-aspiration, not flown.
- Locked-finding 2: zero-of-six US space-fission programs in stated decade.
- Locked-finding 3: Fission Surface Power Phase 2 not yet awarded; FY2026 budget zeroed Nuclear Electric Propulsion / Nuclear Thermal Propulsion lines.
- Locked-finding 4: at megawatt scale, radiators are forty-to-fifty-five percent of system mass; bundled-ten-tonne formula is the right anchor.

Required reactor power post-rescue is computed from electric thrust necessary to make round-trip in L0-05 ceiling. Compare to Fission Surface Power Phase 2 scope (100 kilowatt-electric).

---

## Result

`run.py` ran deterministically; numbers from `results/R_chunk_as_heat_shield_revisit.json`.

### Attitude stability (H1, H2, H3) — chunk 200 tonnes, sweep aspect-ratio × entry-velocity

| Aspect ratio | Entry (km/s) | Dynamic pressure (Pa) | Torque (N·m) | Thrust required per pair (N) | Propellant per pulse (kg) |
|---:|---:|---:|---:|---:|---:|
| 1.5 | 12.5 | 265.6 | 2172.5 | **444.0** | 39.4 |
| 1.5 | 14.0 | 333.2 | 2725.2 | **556.9** | 49.4 |
| 2.0 | 12.5 | 265.6 | 2172.5 | **366.5** | 32.5 |
| 2.0 | 14.0 | 333.2 | 2725.2 | **459.7** | 40.8 |
| 2.5 | 12.5 | 265.6 | 2172.5 | **315.8** | 28.0 |
| 2.5 | 14.0 | 333.2 | 2725.2 | **396.2** | 35.1 |
| 3.0 | 12.5 | 265.6 | 2172.5 | **279.7** | 24.8 |
| 3.0 | 14.0 | 333.2 | 2725.2 | **350.9** | 31.1 |

Required thrust per-pair range: **280–560 newtons.** Scope-sketched 1-, 10-, and 100-newton classes all fail to close. The 1000-newton class closes everywhere. Propellant per pulse: **25–50 kilograms** at cold-gas helium 230 specific impulse.

### Chunk ablation (H4) — single-pass aerocapture, sweep chunk-mass × entry-velocity

| Chunk (t) | Entry (km/s) | Peak heat flux (megawatts-per-square-metre) | Ablation mass (kg) | Ablation fraction (%) |
|---:|---:|---:|---:|---:|
| 100 | 12.5 | 2.93 | 175.7 | **0.176** |
| 100 | 14.0 | 4.12 | 246.9 | **0.247** |
| 200 | 12.5 | 2.93 | 279.0 | **0.139** |
| 200 | 14.0 | 4.12 | 392.0 | **0.196** |
| 500 | 12.5 | 2.93 | 513.9 | **0.103** |
| 500 | 14.0 | 4.12 | 722.0 | **0.144** |

Range across all twelve cells: **0.10–0.25 percent.** Below Saturn's SCOPE prediction band (1–3 percent) by factor of 4–30.

### Mission closure (H5, H6) — 1-megawatt-electric MARVL tug, post-rescue inbound 9.24 kilometres-per-second

| Chunk grappled (t) | Delivered (t) | Delivered fraction (%) | Round-trip-A pure continuous-thrust (yr) | Round-trip-B continuous-thrust + Hohmann coast inbound (yr) |
|---:|---:|---:|---:|---:|
| 100 | 23.0 | **23.0** | **4.48** | 10.54 |
| 200 | 85.5 | **42.7** | **4.81** | 10.87 |
| 500 | 272.8 | **54.6** | **5.79** | 11.85 |

Constants: outbound propellant 368.2 tonnes (continuous-thrust spiral at 29.56 kilometres-per-second), inbound propellant chunk-fed (114.5 tonnes at 200-tonne chunk).

### Reactor-program dependency (H7)

Required reactor power: **1000 kilowatt-electric.** Fission Surface Power Phase 2 scope: 100 kilowatt-electric. **Factor over Fission Surface Power Phase 2: 10×.** Outbound delta-velocity 29.56 kilometres-per-second is unchanged by aerocapture rescue (rescue is inbound-only). Reactor-program dependency unchanged.

### Hypothesis grading

| ID | Predicted | Measured | Held? | Notes |
|---|---|---|---|---|
| H1 — passive instability | Held across all aspect ratios | Held (model imposed 10 percent offset; no aspect ratio compensates) | **Held** | The model assumes instability via offset; the falsification test is whether the offset can be inverted. For a rubble-pile, it cannot. |
| H2 — reaction-control authority 100–1000 N | 280–560 N per pair | **Held at upper end, lower bound 100 N falsified** — minimum required is ~280 N. 1000 N suffices comfortably. | Mostly held |
| H3 — propellant 20–100 kg per pulse | 25–50 kg | **Held** | Centre of band. Not a mass-budget breaker. |
| H4 — ablation 0.2–0.6 percent per pass | 0.10–0.25 percent | **Falsified low** — lower and tighter than predicted by factor 2–4. Better than expected. | Falsification limit (1.5 percent ceiling, 0.05 percent floor) not approached. |
| H5 — delivered fraction 35–50 percent at 200 t | **42.7 percent** at 200 t | **Held at 200 t** | Strongly sensitive to chunk-mass choice: 23 percent at 100 t (falsified low), 55 percent at 500 t (falsified high). |
| H6 — round-trip 5.5–7.0 yr | Architecture A 4.5–5.8 yr; Architecture B 10.5–11.9 yr | **Falsified — band straddled by model choice** | Architecture A (pure continuous-thrust) is internally consistent with titan's accounting and is the right model. The 5.5–7.0 band was set without committing to the trajectory model. Methodology lesson #6 below. |
| H7 — reactor dependency unchanged | Unchanged at 10× Fission Surface Power Phase 2 | **Held** | Aerocapture is inbound-only; outbound 29.56 kilometres-per-second drives the power requirement. |

**Aggregate:** the rescue **closes the propulsion engineering** for the year-twenty-plus megawatt all-electric end-to-end cell. **The rescue does NOT close the reactor-program dependency.**

---

## Reading

Three findings tier-1, three tier-2.

### Tier 1

1. **Aerocapture rescue closes engineering for the megawatt cell at one-megawatt-electric MARVL with chunk ≥ 200 tonnes.** Delivered fraction 42.7 percent (200 t chunk) to 54.6 percent (500 t chunk). Round-trip 4.8 to 5.8 years under pure-continuous-thrust trajectory accounting — well inside L0-05's 15-year ceiling. The matrix's line-69 "Conditional — depends on R-chunk-as-heat-shield-revisit closing" status can graduate to "Engineering-closed, reactor-dependent."

2. **The lower bound on chunk size to make the cell close is ~150 tonnes.** At 100 tonnes the delivered fraction is 23 percent (below the L0-04 commercial-class economics floor, qualitatively). Below ~150 tonnes the tug mass dominates the inbound mass ratio and erodes the rescue's payoff. The matrix's ≤ 200-tonne L0-05 compliance ceiling and the rescue's ≥ 150-tonne economics floor leave a **narrow chunk-size band of approximately 150–200 tonnes** for the rescued cell. Operational constraint: chunk acquisition must hit this band reliably.

3. **Reaction-control system class is bipropellant or high-pressure cold-gas, not low-pressure cold-gas.** Required thrust authority 280–560 newtons per pair at moment arm equal to chunk half-length, well above the 1-to-10-newton range Saturn's SCOPE.md sketched. A 1000-newton class (small bipropellant or high-pressure helium) closes everywhere. Propellant per pulse 25–50 kilograms — tolerable. The earlier scope band was an under-spec.

### Tier 2

4. **Chunk ablation is lower than expected.** Range 0.10–0.25 percent per single pass. The v³ scaling from the prior round's 12.6-kilometres-per-second calibration to 14-kilometres-per-second adds ~37 percent heat load, but the larger chunks dilute it (windward area scales as m^(2/3) while mass scales as m, so per-mass ablation drops at larger chunk sizes). Sub-percent ablation per pass means single-pass aerocapture is preferable to multi-pass aerobraking from an ablation-budget standpoint; aerobraking's only advantage is reduced bag thermal load, addressed separately by bag-sacrificial economics.

5. **Round-trip time is model-sensitive.** Under pure-continuous-thrust accounting (consistent with titan's integrated-delta-velocity definition), round-trip 4.5–5.8 years. Under a hybrid continuous-thrust-plus-Hohmann-coast model, 10.5–11.9 years. The correct model for this architecture is continuous-thrust pure (the inbound delta-velocity 9.24 kilometres-per-second is the integrated burn over the entire inbound trajectory including the Hohmann-equivalent decel; adding a 6-year Hohmann coast on top would double-count). My pre-registered prediction band of 5.5–7.0 years was set without committing to a trajectory model. Lesson recorded.

6. **The cell remains entirely gated on a one-megawatt-electric reactor program that does not exist.** Aerocapture rescues inbound delta-velocity; it does not rescue outbound. Outbound is 29.56 kilometres-per-second continuous-thrust, which at MARVL mass and 2000-second specific impulse requires roughly 1 megawatt-electric to fit the round-trip-time envelope. Per locked-finding base rate (zero of six US space-fission programs in stated decade), posterior probability of an available 1-megawatt-electric reactor by the 2032–2035 demonstrator window is 0.10–0.30. The aerocapture R&D investment is justified only conditionally on parallel reactor-program advocacy.

---

## Revisit

| Hypothesis | Predicted | Outcome | Fix at back-of-envelope stage |
|---|---|---|---|
| H1 | passive instability | held by construction | The hypothesis was tautological given the imposed 10-percent offset. Better: pre-register the offset value and ask whether observed chunk geometries (B-ring shepherding constraints, Cassini observations) cluster around it. |
| H2 | 100–1000 N | 280–560 N — lower bound loose | Better: compute required thrust from torque-and-moment-arm analytically, then ground the prediction. I left the lower bound at 100 N from rough Fermi estimate; arithmetic gives 280 N minimum. |
| H3 | 20–100 kg | 25–50 kg — held | Solid pre-registration. |
| H4 | 0.2–0.6 percent | 0.10–0.25 percent — falsified low | I scaled prior round's 0.5-percent calibration linearly when v³ scaling AND chunk-size scaling both apply. Larger chunks dilute per-mass ablation. The v³ scaling alone would give 0.5 × 1.37 = 0.69 percent — still inside my band — but the m^(2/3) area scaling lowers the per-mass fraction for larger chunks. |
| H5 | 35–50 percent | 42.7 percent at 200 t — held; 23 percent at 100 t and 55 percent at 500 t falsify outside band | The pre-registration targeted 200-t chunk; the sweep introduced sensitivity I did not pre-register. Better: pre-register either the headline 200-t case or a chunk-size band. |
| H6 | 5.5–7.0 yr | 4.5–5.8 yr (Architecture A) or 10.5–11.9 yr (Architecture B) — band straddled | **Methodology failure.** I did not commit to a trajectory model before pre-registration. Architecture A is the internally consistent model under titan's continuous-thrust accounting; Architecture B double-counts the heliocentric decel. Lesson: pre-register the trajectory model alongside the numeric band. |
| H7 | unchanged | unchanged — held | Solid. |

### Methodology lesson #6 (this round)

**Before pre-registering a round-trip time, commit to a trajectory architecture model.** The continuous-thrust accounting in titan and prior rhea rounds gives delta-velocity AS integrated-burn-over-trajectory. Adding a ballistic Hohmann coast on top of that double-counts. The trajectory model and the delta-velocity definition must be consistent.

The pattern (every round in three rhea sessions has falsified at least one pre-registered numeric range) continues. The fix is at the back-of-envelope stage, not in the data.

---

## Cross-learning

### Forward (for next rounds)

- **R-bag-sacrificial-vs-retractable (next round candidate, gated by this round's H1–H4 closing):** the 25–50-kilogram cold-gas propellant per pulse + 200–700-kilogram chunk ablation per pass establish the per-mission consumable footprint. The bag is the next consumable to size. Suggested for a follow-on worker session.
- **R-tug-thermal-survival (parallel-blocking, gated separately):** the chunk shields the tug from stagnation heating only if the tug stays in the chunk's wake. With 280–560-newton-per-pair reaction-control torque authority, the tug is dynamically coupled to the chunk during the pulse — if the chunk pitches > 10 degrees, the tug starts seeing direct flow. This is the next engineering question after H1–H4.
- **R-chunk-acquisition-mass-band (gated):** the rescue requires chunk ≥ 150 tonnes for delivered economics, ≤ 200 tonnes for L0-05 compliance under MARVL mass. The bag-fill operation must hit a ~50-tonne acquisition window. This is a B-ring operations question, not a propulsion question; deferred for an operations worker.

### Backward (matrix and prior rounds)

- **R-chunk-as-heat-shield (closing round):** the 12.6-kilometres-per-second / 0.5-percent / 3-megawatt-per-square-metre calibration scaled cleanly to 14 kilometres-per-second under cubic-velocity dependence. The prior round's deferred questions on attitude stability and higher entry velocity are now answered.
- **R-deployable-drag-skirt (killed at 12.6 kilometres-per-second):** stays dead at 12.5–14-kilometres-per-second. Chunk-as-heat-shield is the only surviving aerocapture path.
- **rhea round 3 (R-chemical-trim-vs-all-electric-earth-arrival, commit `47b69bc`):** its conclusion that the surviving 500-kilowatt-electric chemical-kick cell is internally inconsistent at 27.6-vs-17.0 percent delivered remains unchanged. Aerocapture rescues a *different* (year-twenty-plus megawatt) cell, not the 500-kilowatt-electric cell. Saturn's pending decision (Amendment A, B, or C) is unaffected.
- **enceladus round 4 (R-megawatt-architecture-viability):** independently confirmed megawatt cell collapses under MARVL + 0-of-6 base rate. This round adds: even with aerocapture rescue, the reactor-program dependency is unchanged. Saturn should reconcile enceladus's "collapses to upside-only" finding with this round's "engineering-closed, reactor-dependent" finding — they are compatible but use different framing.

### Matrix amendment proposed for Saturn

Current matrix line 69: *"Megawatt (year 20+) + chunk-as-heat-shield rescue ... Conditional — depends on R-chunk-as-heat-shield-revisit closing."*

Replace with: *"Megawatt (year 20+) + chunk-as-heat-shield rescue. Required: chunk 150–200 tonnes, one-megawatt-electric MARVL, single-pass aerocapture, active reaction-control stabilization at 300–600-newton-per-pair class. Engineering: closed. Reactor program: 10× Fission Surface Power Phase 2 scope, posterior availability 0.10–0.30 by 2032–2035. **Engineering-closed, reactor-dependent.** Delivered fraction 42 percent at 200-tonne chunk; round-trip ~5 years."*

### What this round did NOT resolve

- **Reactor-program path.** Same dependency as the 500-kilowatt-electric surviving cell, only 2× the scope.
- **Tug thermal survival behind the chunk.** Out of scope per SCOPE.md; named as the next blocking round.
- **Bag economics (sacrificial vs retractable).** Out of scope per SCOPE.md.
- **Multi-megawatt extension.** One-megawatt-electric is the smallest defensible target; 2- and 5-megawatt-electric closures are upside that requires its own round.

---

## Out of scope (deferred)

Per Saturn's SCOPE.md, these are explicitly out-of-round and become follow-on rounds:

- **R-bag-sacrificial-vs-retractable** — economic comparison; gated on this round closing on H1–H4.
- **R-tug-thermal-survival** — does the 104.9-tonne tug behind the chunk survive the pulse?
- **R-hybrid-aerocapture-aerobraking** — fallback if single-pass aerocapture introduces unacceptable ablation; not needed if H4 holds.
- **R-multi-megawatt-class** — does the closure extend to two- or five-megawatt cells? Not now; one-megawatt-electric is the smallest defensible megawatt closure target.
- **R-bag-retraction-mechanism-trl** — qualitative-only per SCOPE; deferred to a follow-on with industrial-heritage survey.
