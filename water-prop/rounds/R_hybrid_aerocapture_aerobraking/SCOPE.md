# R-hybrid-aerocapture-aerobraking — does pass-1-deep-aerocapture-with-bag-sacrificed + pass-2-onward-shallow-aerobraking close where pure aerocapture and pure aerobraking each fail?

**Status:** scope, pre-study. Authored by hyperion (worker session, post hyperion-3 batch-4 kill-shot rounds), 2026-05-15.

**Context.** The matrix's surviving cell is currently empty. R-aerocapture-fast-cruise-envelope (commit pending push) showed Round F's STRICT-closing Variant C cell is FALSIFIED at the engineering level — chunk shatters at 47.9 g, bag radiative-equilibrium temperature 4,127 K. R-no-atmospheric-capture-baseline (commit pending push) showed that with Earth aerocapture entirely removed, ZERO of 288 swept cells close any version of L0-05. The matrix as currently shaped has no surviving cell.

R-chunk-as-heat-shield closed eight rounds ago and explicitly named a hybrid architecture as its "most-likely-to-work" follow-on candidate, but that candidate was never run. With the matrix now empty, this candidate is the highest-priority architectural-recovery round.

---

## What R-chunk-as-heat-shield actually said about the hybrid (PRIMARY-text quotes)

Per recurring-lesson-#N updated reading: anchor on PRIMARY-text Reading sections, not on downstream SCOPE summaries. Re-reading R-chunk-as-heat-shield's STUDY.md directly, not via Saturn's `R_chunk_as_heat_shield_revisit/SCOPE.md`:

Lines 156–158 ("Three observations the result actually supports"), observation 3:

> "Aerocapture-then-aerobraking is a possible hybrid architecture. Single-pass aerocapture inserts the vehicle into a high elliptical orbit (apogee ~300,000 km). Subsequent aerobraking passes at 130–180 km could circularize over many months — once the bag has been sacrificed during the deep aerocapture pass, residual aerobraking heating of the chunk-and-tug only is tractable. This is the most likely architecture if aerocapture is in scope."

Lines 178–180 (next-round candidates):

> "**R-hybrid-aerocapture-aerobraking:** model the single-pass-then-multi-pass trajectory with bag sacrificed in the first pass. Estimate time, delta-v, total chunk loss."

Lines 100–107 (per-altitude per-pass behaviour, the data this round must extend):

| Periapsis altitude | Atm density | Peak heat flux | Δv per pass | Passes to dissipate 6 km/s | T_eq @ ε=0.8 | Bag survives |
|---:|---:|---:|---:|---:|---:|:---:|
| 90 km | 1e-4 kg/m³ | 4,434 kW/m² | 285 m/s | 22 | 3,144 K | no |
| 100 km | 1e-5 kg/m³ | 1,399 kW/m² | 28 m/s | 211 | 2,357 K | no |
| 110 km | 1e-6 kg/m³ | 441 kW/m² | 2.4 m/s | 2,492 | 1,766 K | no |
| 130 km | 1e-7 kg/m³ | 139 kW/m² | 0.24 m/s | 24,910 | 1,323 K | no |
| 150 km | 1e-8 kg/m³ | 44 kW/m² | 0.06 m/s | 101,656 | 991 K | no |
| 180 km | 5e-10 kg/m³ | 9.7 kW/m² | 0.003 m/s | 2,032,041 | 680 K | yes |
| 200 km | 1.5e-10 kg/m³ | 5.3 kW/m² | 0.001 m/s | 6,771,111 | 585 K | yes |

The hybrid splits this table into two regimes:
- **Pass 1 deep:** 60–90 km. Dumps a large fraction of total Δv in one pulse. Bag dies (sacrificed). Chunk + tug must survive the pulse thermally and structurally.
- **Passes 2..N shallow:** 130–180 km. Bag is gone; chunk + tug only. Each pass dumps small Δv but bag thermal limit no longer applies. Chunk-only T_eq at 130 km is 1,323 K — well above ice melt 273 K. Chunk-as-radiator only works if pulse duration is short enough that internal conduction does not raise bulk chunk temperature.

---

## Question this round answers

For a Round-F-equivalent vehicle (200 t chunk + 64 t tug, entry at 15.3 km/s, ballistic coefficient ~5,940 kg/m², from heliocentric Hohmann return aphelion 9.58 astronomical units OR aphelion 11 astronomical units faster cruise):

1. **What pass-1 periapsis altitude minimizes total mission delivered-mass-loss?** Trade-space: deeper periapsis dumps more Δv per pass (fewer aerobraking passes), but ablates more chunk and risks chunk structural failure (peak g exceeded ice tensile strength at 40 km in R-aerocapture-fast-cruise-envelope). Shallower pass-1 dumps less, requires more aerobraking passes, longer mission time.

2. **How many aerobraking passes are required at survivable altitudes (130 km+) to circularize from pass-1's elliptical insertion?** R-chunk-as-heat-shield's table shows 24,910 passes at 130 km dumps 6 km/s. Hybrid needs maybe 1–3 km/s post-pass-1, so 4,000–12,000 passes. Each pass is one orbital period; period scales with semi-major axis. Total time penalty is the integral.

3. **Does the chunk geometric stability question (R-chunk-as-heat-shield-revisit's binding open question) close any easier in the hybrid case than in pure single-pass?** Pass-1 pulse is shorter (less Δv to bleed), so the orientation-control problem is briefer. Pass 2..N at shallow altitude has nearly-zero hypersonic torque so orientation is passive.

4. **What's the chunk bulk temperature evolution across the multi-month aerobraking campaign?** Each pass adds heat, between-pass time radiates it. Chunk has 200 t of water at melting point 273 K; total thermal capacity is enormous, but if the surface layer melts and re-freezes irregularly, structural integrity may degrade.

5. **Does the bag-sacrificed-per-mission economic line close versus mission revenue?** R-chunk-as-heat-shield estimated bag at 1–3 t / $5–20 million per unit. Per-mission consumable would add to matrix as a first-class line.

6. **Combined: is hybrid the architectural escape that closes Variant C / Variant D for the matrix?** With pass 1 dumping 5 km/s and pass 2..N circularizing the rest, the propulsive inbound Δv for the electric stage drops from 17.97 km/s (titan) to ~0.5–1.0 km/s (LEO trim post-aerobraking). This is the architecture-saving recovery, IF it closes engineering-side.

---

## Pre-registered prediction sketch (full hypothesis-grading deferred to STUDY.md)

**Anchored back-of-envelope (PRIMARY-text computed FIRST, per recurring-lesson-#N stacked intervention):**

| Quantity | Anchor | Source |
|---|---:|---|
| Earth velocity-at-infinity, Round F closing case (no LGA) | 10.55 km/s | Round F output |
| Earth periapsis hyperbolic velocity | 15.29 km/s | sqrt(v_∞² + v_escape²) |
| Total Δv to bleed (entry → LEO circular) | 7.62 km/s | 15.29 − 7.67 |
| Pass-1 deep aerocapture target Δv | 5.0 km/s | engineer-judgment 65 percent of total in pass 1 |
| Pass-1 periapsis altitude estimate | 75 km | between 90 km (4.4 MW/m², bag dies) and 60 km (chunk shatters per R-aerocapture-fast-cruise-envelope) |
| Pass-1 q_peak (Sutton-Graves at 75 km, R_n 3.74 m, v 15.3 km/s) | 3.7 MW/m² (370 W/cm²) | derivation |
| Pass-1 chunk ablation | 1.8 percent | total heat load 8 GJ / heat-of-vaporization 2.26 MJ/kg |
| Pass-1 peak g (rough) | 25 g | shorter pulse than full-capture so lower peak |
| Pass-1 chunk tensile margin | 0.8× | likely STILL FAILS structurally even at hybrid pass 1 |
| Post-pass-1 elliptical orbit period | ~weeks | apoapsis 50,000–300,000 km |
| Aerobraking Δv to dump after pass 1 | 2.6 km/s | 7.6 − 5.0 |
| Aerobraking passes at 150 km (Δv 0.06 m/s/pass) | 43,000 passes | 2600 / 0.06 |
| Aerobraking time at average period 12 hr | 60 years | unphysical |
| Aerobraking passes at 130 km (Δv 0.24 m/s/pass) | 11,000 passes | 2600 / 0.24 |
| Aerobraking time at 130 km | 15 years | still unphysical |

**Predicted aggregate (sketch, full hypothesis in STUDY.md):**

The hybrid architecture is **likely also infeasible** for ICEBERG at the tested ballistic coefficient, but the failure mode is different:
- Pass 1 likely still fails structurally (chunk shatters at 25 g, internal stress > ice tensile strength).
- Even if pass 1 survives, aerobraking time penalty at survivable altitudes is years to decades — same root cause R-chunk-as-heat-shield identified ("ballistic coefficient is too high; Mars heritage does not transfer").

**The hybrid is most likely to close conditional on chunk size reduction.** A 50 t chunk gives β ≈ 4,400 kg/m² (similar to R-chunk-as-heat-shield's nominal). At that ballistic coefficient, pass-1 g-load is lower (chunk surface stress mass^(−1/3) on g, mass^(+1/3) on chunk radius, net mass^0 — wait, internal stress = chunk_radius × ρ × g_peak; chunk_radius scales as mass^(1/3), g scales inversely with mass via β; net stress scales as mass^(1/3) × mass^(−1/3) = mass^0. **Internal stress is INDEPENDENT of chunk mass at equal entry velocity and equal periapsis altitude.** Smaller chunk does NOT help structural failure at equal periapsis.

But smaller chunk DOES help via lower required-periapsis-depth (smaller β → less drag needed → shallower periapsis). At β = 4,400 instead of 5,940, periapsis can be 5–10 km shallower for same Δv, dropping q_peak and g_peak materially.

**Prediction:** R-hybrid-aerocapture-aerobraking closes engineering-side ONLY at chunk ≤ 100 t AND with multi-month (6–18 month) aerobraking campaign. Sacrificial-bag mass ~1–2 t per mission. Total chunk loss across full mission 3–5 percent. This is the R-megawatt-chunk-100t architectural escape combined with hybrid; neither closes alone.

If this prediction holds, the matrix's surviving cell becomes:
- Variant C with chunk 50–100 t, hybrid aerocapture-then-aerobraking, sacrificial bag, multi-month aerobraking campaign.
- Delivered ~50 t per mission (after ablation losses, before sacrificial bag).
- Round-trip ~17–19 yr (cruise + aerobraking time).
- Per-mission consumable bag cost $5–20 million.
- Mission cadence increases (more missions per delivered tonne).

Conditional on the chunk size reduction round (R-megawatt-chunk-100t) closing, this combined architecture is the matrix's recovery path.

---

## Method sketch

Detailed methodology in STUDY.md when round runs.

1. **Pass-1 deep aerocapture parameterization.** Sweep periapsis altitude {65, 70, 75, 80, 85} km × chunk size {50, 100, 200, 350} t. Compute q_peak, total heat load, ablation, peak g, internal stress, achieved Δv. Identify (chunk size × periapsis) cells where chunk survives structurally AND achieves > 3 km/s Δv in pass 1.

2. **Aerobraking campaign for surviving cases.** For each surviving (chunk, pass-1-Δv) configuration: iterate aerobraking passes from elliptical insertion to LEO. Per-pass: solve perturbed two-body for orbital decay; reduce semi-major axis; check chunk thermal cycling (per-pass heating + between-pass radiation); count passes; compute total time. Halt when periapsis can be raised enough that drag effectively zero (post-circularization).

3. **Bag thermal design.** Pass-1 q_peak determines bag layer-by-layer ablation rate (bag designed to ablate, not just thermally fail). Estimate bag mass per single-mission consumable. Compare to R-chunk-as-heat-shield's 1–3 t / $5–20 million estimate.

4. **Chunk thermal cycling across campaign.** Chunk surface layer heats during pass, radiates between passes. If between-pass cooling is incomplete, surface temperature rises monotonically. Compute steady-state surface temperature; if > 273 K continuously, chunk surface is liquid water (sublimation losses much higher).

5. **Architecture closure re-derivation.** With Earth-side Δv collapsed to 0.5–1.0 km/s post-circularization, recompute Round F closure machinery. Sweep reactor power 500/1000 kWe × chunk 50/100/200 t × cruise time aphelion 9.58/10.5/11 AU. Identify any (chunk, reactor, cruise) cell that closes L0-05 strict 15-year ceiling.

6. **Sweep axes:**
   - Pass-1 periapsis altitude: 65, 70, 75, 80, 85 km
   - Chunk mass: 50, 100, 200, 350 t
   - Pass-1 Δv target: 3, 4, 5, 6 km/s
   - Reactor power: 500, 1000 kWe
   - Transfer aphelion: 9.58, 10.5, 11 AU
   - Lunar gravity assist credit: with, without
   - Aerobraking altitude: 130, 150 km

7. **Deterministic run.py per project convention.** No randomness.

---

## Validity caveats (non-exhaustive)

1. **Exponential atmosphere with single scale height** is approximate above 100 km; periapsis estimates ±5 km error (per R-aerocapture-fast-cruise-envelope's caveat 6).
2. **Sutton-Graves stagnation-point only.** Real heat flux distribution has off-axis attenuation; conservative upper bound.
3. **Bag ablation modeling.** Bag is designed to ablate progressively; this round must distinguish "thermal failure of laminate" (T_eq exceeds glass transition) from "designed ablation of laminate" (sacrificial layer, controlled mass loss). R-chunk-as-heat-shield treated bag as non-ablating; this is more conservative than actual sacrificial-bag design.
4. **Chunk thermal cycling.** Per-pass heat load divided among (1) ablation of surface, (2) conduction into chunk bulk, (3) re-radiation between passes. Real partition depends on water-ice thermal conductivity, surface emissivity, and pass cadence. Estimate band: 30–70 percent into bulk per pass.
5. **Tug aerodynamic geometry.** Tug behind chunk is shadowed for stagnation streamline but exposed in wake to convective heating. Not modeled in detail.
6. **Aerobraking trajectory perturbations.** Real aerobraking has eccentric-orbit perturbations from drag asymmetry, lunar-solar gravity gradient, and atmospheric density variability (±30 percent at 130–180 km). Adds 10–30 percent margin to pass-count estimates.
7. **Pass-1 attitude control.** R-chunk-as-heat-shield-revisit's binding open question (orientation stability through pulse) still applies to pass 1. This round can either assume orientation-control closes or treat as a separate dependency.
8. **Round F outbound chemical-kick economics still unaddressed.** Even if hybrid closes engineering-side, outbound kick requires 715 t hydrolox per mission; this round does not address that orthogonal sleeper falsifier.
9. **No COSPAR planetary-protection assessment.** Multi-month aerobraking with chunk-as-payload near LEO has backward-contamination risk from Saturn-system material. Regulatory item not addressed.
10. **L0-05 ceiling assumed unchanged.** If hybrid time penalty is 6–18 months, round-trip becomes 13.5–18 yr at faster cruise; some configurations would push past strict 15 yr ceiling.

---

## Cross-references (read before authoring STUDY.md)

- `water-prop/rounds/R_chunk_as_heat_shield/STUDY.md` — primary text. Required reading. **Do NOT read via Saturn's `R_chunk_as_heat_shield_revisit/SCOPE.md` summary, which misrepresents the prior round's findings (per R-aerocapture-fast-cruise-envelope's recurring-lesson-#N updated reading).**
- `water-prop/rounds/R_aerocapture_fast_cruise_envelope/results/closure_verdict.md` — the engineering-envelope failure for full-Δv single-pass. Establishes the chunk-shatters-at-47.9-g and the q_peak / ablation calibration this round must extend.
- `water-prop/rounds/R_no_atmospheric_capture_baseline/results/closure_verdict.md` — the matrix-empty verdict that motivates this round as the architectural recovery candidate.
- `water-prop/rounds/R_cruise_time_optimization/results/R_cruise_time_optimization.json` — Round F transfer table, source of v_perihelion and cruise-time anchors.
- `water-prop/rounds/R_inbound_dv_continuous_thrust/STUDY.md` — titan's segment decomposition, source of the 17.97 km/s Earth-side Δv that this round attempts to collapse.
- `water-prop/rounds/R_megawatt_marvl_radiator/STUDY.md` — rhea's MARVL mass model, source of tug dry mass at each reactor power class.
- `ICEBERG-bag-engineering.md` — bag mechanical and capture-efficiency reference.

---

## Out-of-scope (deferred to follow-on rounds)

- **Detailed bag thermal-protection-system design.** This round estimates bag mass and cost as parameter; full design is a separate engineering programme.
- **Tug thermal survival behind chunk.** Wake heating analysis. R-tug-thermal-survival named as separate follow-on.
- **Orientation control through pass-1 pulse.** R-chunk-as-heat-shield-revisit's binding open question. This round assumes orientation closes; the assumption can be relaxed in a follow-on R-chunk-orientation-stability round.
- **Outbound chemical-kick economics.** Orthogonal but related sleeper falsifier flagged in batch-3 / batch-4 handoffs.
- **Mission-architecture pivots** (lunar-orbit catcher, cislunar processing depot). Out of scope for "Earth-arrival via atmosphere" branch.
- **R-megawatt-chunk-100t — separate but related round.** This SCOPE flags chunk-size-reduction as the conditional that may make hybrid close. R-megawatt-chunk-100t should be its own round; if it closes, the combined hybrid + small-chunk architecture is the matrix recovery.

---

## Recommended next worker

This round is sizable: pass-1 sweep with structural and thermal closure, multi-pass aerobraking trajectory iteration, chunk thermal cycling, bag ablation modeling, architecture re-derivation. Estimate 6–10 hours of analyst time including STUDY.md draft, run.py, results, grading, and Reading.

Recommend spawning a new worker session under a Saturn-moon name not yet used: **Iapetus**, **Tethys**, **Mimas**, **Phoebe**, or **Dione**. Worker reads this SCOPE.md, drafts STUDY.md against the project's pre-registration template (with central anchors computed FIRST per recurring-lesson-#N stacked intervention; PRIMARY-text-only sourcing), writes run.py, runs it, grades hypotheses, and hands off to Saturn (orchestrator) for matrix integration.

Worker brief should include:

1. **The recurring-lesson-#N stacked intervention is mandatory.** Compute back-of-envelope FIRST. Anchor on PRIMARY-text Reading and Revisit sections of source rounds, not on SCOPE summaries. Re-read R-chunk-as-heat-shield's STUDY.md directly.
2. **The matrix is currently EMPTY.** This round is one of the architectural-recovery candidates. Other candidates (R-megawatt-chunk-100t, R-sacrificial-bag-mass-and-cost, mission-architecture pivots) are independent. Worker should not over-claim — closing this round does not close the matrix; it just adds a candidate cell back.
3. **The orientation-stability question (R-chunk-as-heat-shield-revisit's binding open) is still unscoped.** If this round predicts hybrid closure conditional on orientation-control closing, that conditional must be explicit in the Reading.

If the worker name should track topic rather than moon convention: **hybrid-aerobrake** or **chunk-pass-one**. Protocol is name-agnostic.

---

## What this round should produce

- `STUDY.md` — full pre-registration, method, validity caveats, test plan, revisit clause.
- `run.py` — deterministic sweep machinery for pass-1 envelope and aerobraking campaign.
- `results/R_hybrid_aerocapture_aerobraking.json` — per-tuple closure data.
- `results/tables.md` — human-readable summary.
- `results/closure_verdict.md` — single-paragraph architecture verdict (hybrid closes or hybrid does not close, what conditions, what follows).
- Handoff to orchestrator at `~/.claude/handoffs/iceberg-WORKER-YYYYMMDD-HHMM.md`.
