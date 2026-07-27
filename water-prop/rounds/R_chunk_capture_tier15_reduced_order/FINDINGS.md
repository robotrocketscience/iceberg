# R-chunk-capture-tier15-reduced-order — FINDINGS

**Worker:** rhea-5, 2026-06-12. Pre-registration: STUDY.md (written before first run).
Artifacts: `run.py` (mechanics-derived event chain, n = 50,000, seed 20260612),
`results/tier15_results.json`. Harpoon only; ram-scoop event physics explicitly NOT
claimed (multi-contact — remains with the MuJoCo/Drake round).

## Headline

A mechanics-derived event model in plain numpy puts harpoon single-pass capture at
**0.549 prior-predictive mean** (bootstrap [0.545, 0.553]) vs Tier 1's closed-form
median 0.365 — and shows the number is **dominated by two engineering choices, not by
physics constants**: projectile speed (total-order sensitivity 0.592) and reel speed (0.143)
against one material unknown, porous-ice strength (0.529). At the swept design point
(projectile ≥ 8 m/s, reel ≥ 5 cm/s) capture probability is **0.907**, implied
multiplier 1.067 — *above* the 0.85 desk anchor. At the prior mean (0.646 multiplier)
the closed-loop 30 t floor stays shut (best delivered 28.5 t); at the design point it
reopens fully (10 cells, 48.5 t best). **The capture bet is therefore not a fixed
probability to be estimated — it is a design trade with one measurable material unknown.**

## Verdicts vs pre-registered predictions

| Hypothesis | Verdict | Predicted | Measured |
|---|---|---|---|
| T15-H1: derived result ≥ 0.05 from Tier-1's 0.365 | **HELD** (direction as predicted) | above, 0.55–0.80 | 0.549 — at the bottom edge of the band |
| T15-H2: spin total-order < 0.05 | **FALSIFIED** | spin mechanically inert | spin = 0.172; wrap-bind is 12.4 % of failures |
| T15-H3: tear-out is modal failure (> 50 %) | **FALSIFIED** | Philae-informed retention worry | **shallow penetration is 72 %**; tear-out only 15 % |
| T15-H4: 30 t floor reopens at derived multiplier | **PARTIALLY HELD** | reopens | prior-mean 0.646 sits just under the ~0.66 cliff (30 t: 0 cells; best 28.5 t — the 25 t L0-04 floor *marginally* closes); design-point 1.067 reopens 30 t fully (10 cells, 48.5 t) |
| T15-H5: "gentle" corner (slow approach, soft tether, slow reel) gains ≥ 0.10 | **FALSIFIED, sign inverted** | +0.10 | −0.066 — slow reeling LOSES the wrap race |

## Prediction-error analysis

1. **I dismissed spin using the wrong invariant.** Spin kinetic energy is indeed
   negligible (≤ 0.03 J), but the binding constraint is kinematic: the tether wrap
   window (π/ω ≈ 5–10 min at the prior's fast tail) races the reel-in time (3–30 min).
   Energy arguments miss timing failures. Tier 1's spin coefficients were "right" to
   keep spin alive — for a reason its linear forms could not represent.
2. **I worried about the wrong tail of the ice-strength axis.** The Philae anchor
   anchored me on retention (weak ice, barb pulls out). The model says the dominant
   failure is at the *strong*-ice tail: penetration depth ∝ v²/σ_crush, and a 5 kg
   projectile at the low end of the speed band simply does not bury a 15 cm barb in
   sintered ice. Same axis, opposite tail, different fix (more impact energy, not a
   bigger barb).
3. **"Gentle capture" intuition inverted.** Soft tether and slow approach do reduce
   snatch loads — but tear-out was never the modal failure, and slow reeling directly
   feeds the actual second-order failure (wrap-bind). Design guidance flips to: shoot
   hard, reel fast, approach slow. Capture probability at that corner: 0.961.
4. **Where the model must not be trusted:** the projectile-speed lever (the #1
   sensitivity) is exactly where the missing physics bites — high-speed impact into
   porous cryogenic ice risks fracture, crater ejecta, and chunk break-up, none of
   which a rigid-body energy-bearing penetration law represents. "Shoot harder" is
   model-form-conditional. This makes **bench-scale penetration testing into porous
   ice analogs the single highest-value next evidence in the campaign** — it is the
   one measurement that simultaneously pins the modal failure mode (72 % of failure
   mass) and the top design lever.

## What this means for the tier ladder and the MuJoCo question

- The Tier-1 closed-form number (0.365) should not be quoted as the harpoon anchor
  going forward; it embeds spin penalties the mechanics do not support and misses the
  penetration mode entirely. Recommended interim anchor: **0.55 (prior mean) with the
  0.65–1.07 design-conditional band**, explicitly flagged as Tier-1.5 model-form-limited.
- The MuJoCo/Drake round remains justified but should be **re-scoped**: its unique
  value is (a) ram-scoop multi-contact containment (untouched here) and (b) a
  cross-check of the harpoon wrap-race and snatch-load chains. The harpoon
  penetration/retention question is NOT answerable by either engine — it needs
  material data. Recommend the orchestrator split the SCOPE accordingly before
  spending the 36–72 hour budget.
- Campaign chain as of this round: fidelity round showed closure hinges on capture
  multiplier ≥ ~0.66 in the f ≈ 0.2 window; this round shows the multiplier is
  0.646–1.067 depending on two design choices and one measurable material constant.
  **The commercial-class verdict now reduces to a bench test.**

## Limitations (declared)

Prior-predictive mean vs Tier-1 median is not a like-for-like statistic (Bernoulli
outcomes vs smooth stage products); both feed the framework as a scalar multiplier, so
the comparison is operative, not statistical. Glance criterion and penetration law are
desk anchors (STUDY model-form risks). Spacecraft mass fixed at 80 t. Long-residence
containment (months-scale) out of scope both here and in Tier 1.

---

## CORRECTION NOTE — 2026-06-12, same worker (rhea-5), appended

The closure-coupling numbers in this round (30 t floor shut at multiplier 0.646 /
reopened at 1.067; 28.5 t / 48.5 t best delivered) were computed through the kick-stage
manifest bug retracted in R_closing_path_self_consistency and are VOID — under corrected
physics nothing closes commercial-class at any capture multiplier. The capture-physics
findings of this round (0.549 prior-mean capture probability, penetration-dominant
failure structure, wrap-race spin channel, design levers, bench-test recommendation) are
framework-independent and STAND. The bench test now supports the demonstrator thesis
rather than a commercial-class closure.
