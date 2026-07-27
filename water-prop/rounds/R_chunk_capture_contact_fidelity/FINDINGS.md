# R-chunk-capture-contact-fidelity — FINDINGS (Tier-1.5 re-scoped execution)

**Worker:** worktree-172651, 2026-07-24 latest+28. Pre-registration: `STUDY.md`
(re-scope + deviations D-1..D-5 declared before the run). Artifacts: `run.py`,
`results/tier15_ramscoop_results.json`. Deterministic (seed 20260724, n = 50,000).
Harpoon cross-check reuses rhea-5's Tier-1.5 model verbatim (reproduces 0.549).
**Tier label: mechanics-derived Tier 1.5 — NOT contact fidelity. The MuJoCo/Drake
Tier 2/3 layer remains open (see Residuals).**

## Headline

**The ram-scoop containment physics envelope is LOSSLESS below ~1 m/s operating
velocity — P(water captured) = 1.000 on the shared Tier-1 priors — and the
architecture still loses: harpoon's delivered-mass lead is 2.92× even when ram-scoop
is credited with perfect capture.** The containment cliff onsets between 1 and 3 m/s
(at 3 m/s: capture 0.573, failing by pessimistic-fabric tear 0.332 + bounce-out
0.095), which is 2–3 orders of magnitude above the mm/s ring-dynamics floor. The
practical meaning: **every failure probability the Tier-1 closed-form assigned to
ram-scoop stages at residence velocities (joint 0.405) was mechanism-reliability
guesswork, not physics — mirroring, and strengthening, Round J's harpoon-side
reframe.** Capture architecture (axis 19) stays falsified in ram-scoop's direction
for delivered-mass reasons that no capture-probability improvement can fix.

## Verdicts

| # | Hypothesis | Verdict | Measured |
|---|---|---|---|
| H-K1 | Tier-1.5 differs from Tier-1's 0.405 by ≥ 0.05 | **HELD** (direction right, band under-shot) | 1.000 vs 0.405 (Δ = +0.595; predicted 0.80–0.95 — see prediction-error note) |
| H-K2 | Harpoon delivered-mass lead survives (≥ 2×) | **HELD** | 2.92× at the 200-t anchor, crediting ram-scoop p = 1.0 (harpoon 0.549 × η 20.85 % vs 1.000 × η 3.92 %) |
| H-K3 | Spin structurally irrelevant to ram-scoop | **HELD** (non-vacuous, at cliff) | spin total-order ≈ 0.000; cliff variance is ceiling-coefficient-dominated (0.862), then restitution (0.184), drawstring speed (0.180), mass (0.153) |
| H-K4 | Containment collapses ≥ 0.2 between 1 cm/s and 1 m/s | **FALSIFIED** | collapse = 0.000 in the registered band; the cliff sits between 1 and 3 m/s |
| H-K5 | ±0.02 binomial half-width at n ≈ 1200 (SCOPE-H1) | **HELD at the operating point, FAILS at the cliff** | p = 1.0 → half-width 0; at the cliff (p = 0.573) half-width at 1200 is 0.028 → n ≈ 2,400 needed where measurement actually matters |

## Prediction-error notes (the part that matters)

1. **H-K1 under-shot (predicted 0.80–0.95, measured 1.000):** I expected residual
   physics losses below the cliff; there are none. A 15-m aperture vs meter-scale pose
   error cannot miss; a 30-m-deep bag with inelastic rebound (return leg at e·v) gives
   the drawstring minutes to close a race it needs only ~150 s to win; and the Round-J
   ceiling (verified in-model to reproduce the 0.99 m/s pessimistic 200-t corner
   exactly) is untouchable at cm/s. Everything binding is excluded-by-declaration
   mechanism reliability (D-4).
2. **H-K4 falsified informatively:** I placed the cliff in the GNC-residual band
   (0.01–1 m/s) following R-A14's velocity-conditional collapse (0.78 → 0.55 at
   low-m/s). The mechanics put it at 1–3 m/s. Implication: **A14's low-m/s containment
   degradation cannot be envelope physics — it is entirely mechanism-reliability**,
   which sharpens Round J's "GNC/mechanism wall" attribution by another decade of
   velocity margin.

## Matrix / axis-19 amendment specification

- Axis 19 status **unchanged (falsified, ram-scoop direction)** — delivered-mass
  accounting, not capture probability, is dispositive (H-K2 re-confirms rhea-3 with
  ram-scoop maximally credited).
- The **Tier-1 closed-form's ram-scoop 0.405 should not be quoted further**: below
  the cliff the derivable physics gives 1.000; the difference was hand-set
  reliability, which is exactly the demonstrator/bench unknown.
- SCOPE-H1's n = 1200 Tier-3 run count is insufficient at the only regime worth
  measuring (the cliff): plan n ≈ 2,400 per architecture in the MuJoCo follow-on.

## Residuals (open, honestly labeled)

1. **MuJoCo Tier 2/3 contact layer** (SCOPE as written): multi-contact tumbling,
   fabric billow, drawstring snag, multi-chunk stream — the mechanism-reliability
   content this tier excludes by construction. Now scoped tighter by this round: the
   only measurement-worthy regime is the 1–3 m/s cliff and the mechanism itself.
2. **Bench measurements** stay the pre-Gate-B critical path: porous-ice penetration
   (harpoon, per rhea-5) and cinch-mechanism reliability (ram-scoop, per this round).
3. Model-form risks as declared in STUDY (single-contact rebound, no-snag drawstring)
   — both flatter ram-scoop; verdict-safe since ram-scoop loses anyway.
