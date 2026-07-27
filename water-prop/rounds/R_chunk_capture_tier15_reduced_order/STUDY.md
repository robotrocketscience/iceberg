# R-chunk-capture-tier15-reduced-order — STUDY (pre-registration)

**Worker:** rhea-5 (`iceberg-rhea-5`), 2026-06-12, at project-owner direction ("can't we
construct a simpler but still useful model in Python?").
**Position in the tier ladder:** Tier 1.5 — between R-chunk-capture-monte-carlo's Tier 1
closed-form (hand-calibrated linear stage products) and the SCOPE'd MuJoCo/Drake Tier 2/3
contact fidelity (R_chunk_capture_contact_fidelity, not yet run). Harpoon architecture
ONLY: ram-scoop event physics is repeated multi-contact inside a closing bag and does not
reduce to impulsive closed forms — that half genuinely needs the contact engine and is NOT
claimed here.
**Pre-registered:** before the model produced any number.

## What this round replaces

Tier 1's harpoon stage probabilities are smooth linear heuristics in the axes (e.g.,
`p_catch = 0.90 − 0.45·(spin/0.05)`), calibrated to the audit's ~46 % decomposition.
Correlation between failure modes exists only through shared inputs to assumed forms.
This round derives the event chain from impulse-momentum mechanics per sample:

1. **Hit / miss** — aim error (Rayleigh from sensor noise) + target-surface drift during
   projectile flight vs the chunk's projected silhouette (ellipsoid from mass, density,
   aspect ratio).
2. **Glance-off** — incidence angle at the sampled impact point vs a friction-plus-barb
   bite criterion.
3. **Penetration** — energy-bearing penetration depth m_p·v_n²/2 ÷ (σ_crush·A_tip) vs
   required barb depth (σ_crush = 3 × σ_shear).
4. **Anchor retention vs snatch load** — tether-taut peak load F = v_rel·√(k·μ_reduced)
   (+ reel tension) vs anchor capacity σ_shear·A_anchor·(depth/depth_req); TEAR-OUT if
   exceeded, SNAP if F exceeds tether strength.
5. **Wrap race** — tether wrap-around window (π/ω) vs reel-in time at reel speed; the
   ONLY mechanism by which spin can matter under the Tier 0.5 slow-spin prior.

Failure probabilities fall out of sampled loads vs strengths — derived, not assumed.
Spin, approach velocity, and sensor noise each enter multiple stages through shared
physical state, which is exactly the correlation structure the contact-fidelity SCOPE's
H3 worries about.

## Axes (priors) — Tier 1 axes inherited where meaningful, material axes added

| Axis | Prior | Source |
|---|---|---|
| chunk_mass_t | log-uniform 10–200 | Tier 1 |
| spin_rate_rpm | log-uniform 0.0005–0.05 | Tier 0.5 Cassini prior |
| approach_vel_cms | uniform 0.3–3.0 | Tier 1 |
| sensor_noise_m | uniform 0.05–0.50 | Tier 1 |
| surface_friction | uniform 0.05–0.40 | Tier 1 |
| chunk_density_kg_m3 | uniform 300–900 | ring-particle porosity literature |
| aspect_ratio | uniform 1.0–2.5 | replaces Tier 1 "contact_geom" |
| ice_shear_strength_kpa | log-uniform 10–200 | NEW, load-bearing material axis (porous cryo-ice; weak-snow to sintered) |
| tether_stiffness_n_m | log-uniform 1e3–1e5 | replaces "catcher_compliance" |
| tether_strength_kn | uniform 5–50 | spec band |
| projectile_speed_ms | uniform 2–10 | design variable, swept |
| reel_speed_cms | uniform 1–10 | design variable, swept |

Fixed design parameters (documented, not swept): projectile mass 5 kg, tip area 2e-3 m²,
deployed barb anchor area 0.02 m², required barb depth 0.15 m, standoff 20 m, spacecraft
mass at capture 80 t (post-fidelity-round mid-anchor). Model-form risks declared: the
glance criterion and penetration law are themselves desk anchors; this round's claim is
the correlation/load-chain structure, not absolute calibration.

## Hypotheses and predictions (registered before first run)

**T15-H1 (load-bearing).** The mechanics-derived event-level capture probability median
differs from Tier 1's 0.365 by ≥ 0.05 in either direction. **Point prediction: lands
ABOVE, median 0.55–0.80**, because (a) under the slow-spin prior the spin penalties that
dominate Tier 1's catch/contain forms are mechanically negligible (≤ 0.03 J spin energy),
and (b) meter-scale aim error against multi-meter silhouettes makes hit/glance benign.
**Declared risk:** if weak-ice anchor retention dominates (low σ_shear tail × snatch
loads), the median lands BELOW 0.365 and the campaign story worsens, not improves.

**T15-H2.** Spin-rate total-order sensitivity index < 0.05 (vs Tier 1, which built 0.40–0.45
spin coefficients into catch/contain). Dominant axes predicted: ice_shear_strength,
tether_stiffness, approach_vel — the snatch-load chain. **Falsified if spin ≥ 0.05**,
which would mean the wrap-race mechanism (the one physical spin channel) carries real
probability mass under the slow-spin prior.

**T15-H3.** Tear-out (anchor retention failure) is the modal failure, > 50 % of all
failures (Philae-informed prior). Falsified if any other mode (miss, glance, shallow
penetration, snap, wrap) exceeds it.

**T15-H4 (campaign coupling).** Feeding the derived median into the closed-loop closure
sweep at f = 0.20 as capture_efficiency_multiplier = median/0.85: per the fidelity
round's conditioning curve, the 30 t floor reopens iff multiplier ≥ ~0.66 (median
≥ ~0.56). **Prediction: it reopens** (follows from T15-H1's point prediction). If T15-H1
lands below 0.365 instead, the 10 t floor closes too and the demonstrator envelope
shrinks — either outcome is matrix-relevant.

**T15-H5 (design leverage).** Within the swept design variables, slower approach velocity
and softer tether (lower stiffness) dominate capture probability improvement — i.e.,
the architecture has cheap operational levers; capture probability at the favorable
design corner (approach ≤ 1 cm/s, k ≤ 3e3 N/m, reel ≤ 3 cm/s) exceeds the overall
median by ≥ 0.10. Falsified if the design corner gains < 0.10 (would mean material
uncertainty swamps design choices, strengthening the case for bench tests over design
iteration).

## Method

Vectorized numpy Monte Carlo, n = 50,000, seed 20260612. Failure-mode accounting per
sample. Sensitivity via the Jansen total-order estimator (validated in
R_vehicle_mass_fidelity_refinement). Design-corner conditional re-run for T15-H5.
Closure coupling re-run for T15-H4 (10 t / 20 t / 30 t floors at f ∈ {0.18, 0.20, 0.22}).
Expected runtime: seconds. FINDINGS.md with verdicts + prediction-error analysis +
explicit statement of what still requires MuJoCo/Drake (ram-scoop containment,
multi-contact tumbling) and what requires bench data regardless (σ_shear of ring ice).
