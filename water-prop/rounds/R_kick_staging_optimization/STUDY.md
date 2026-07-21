# R-kick-staging-optimization — STUDY

**Round:** R-kick-staging-optimization. SCOPE pre-registered 2026-07-21, scripted bounds ([S]/[W] labeled per R175 convention).
**Worker:** worktree-115637 session. R174's 81-percent line item.

## Results

| # | Claim | Measured | Verdict |
| --- | --- | --- | --- |
| H1 [S] | 2-stage saves 47–55%; 3rd stage adds 15–20% | 2-stage saves **13–34%** (13% at struct 0.06, 34% at 0.12) | **FALSIFIED** |
| H2 [S] | hybrid optimum: kick 3.9–4.3 km/s, lit water 44–48.2 t | kick 4.1 km/s, 46.9 t (cap-bound) | HELD |
| H3 [W] | best corner ≤ 300 t, ratio 2.6–3.4× | **357 t, 3.57×** (3-stage, struct 0.06, kick 4.1 km/s) | **FALSIFIED** (marginally above) |
| H4 [W] | outbound share < 81% but ≥ 55% | 74–76% | HELD |

**Reading.** The hybrid kick/lit-thruster split is the real lever — it alone saves 41 percent of outbound mass by moving 3.2 km/s of injection onto sunlight the mission already harvests. Staging adds a further 6–19 percent, far less than the pre-script promised, because **the pre-script's staging model was buggy**: it never accumulated upper-stage wet mass into lower-stage payloads, so it sized every stage against bare hardware and overstated 2-stage savings as 52 percent. H1's falsification is a bug-catch of the bounds script itself.

**End-to-end consequence: the non-fission round-trip floor improves from R174's 4.8× to 3.57×** the reactor baseline's launch economics. The R173→R176 arc settles at: fission is worth ~3.6× on launch economics; every cheaper escape tested (bootstrap, staging) has been priced or killed.

## Revisit (mandatory)

Bug-catch three of the arc, and the first *inside a bounds pre-script* — the convention that was created to stop hand-arithmetic errors produced a script with a modeling error instead. Amended rule: **the pre-script's physics gets the same review as run.py — specifically, any iterative or staged structure must be checked against a hand-verifiable one-step case before its outputs become bounds.** (The single-stage row matched the closed form, which is what localized the bug to the staging loop.) H3's marginal miss (3.57 vs 3.4) is downstream of H1's inflated staging promise, not an independent error. Thin spots: stage structural fractions treated as free parameters (no engine mass floor); the lit-thrust leg is energy-limited but not thrust- or trajectory-scheduled; chunk fixed at the 80 t corner.

## Cross-learning

- **Adopt:** hybrid injection (kick ~4 km/s + array-lit thruster ~3.2 km/s) as the non-fission variant's outbound baseline; 2-stage kick at realistic structural fractions worth its 19 percent; third stage marginal.
- **Corrects R174:** its flat 1.12 kick factor sat between the 1-stage and 2-stage realities; the 4.8× headline becomes **3.57×** at the optimized outbound.
- **For the orchestrator:** matrix note — the R173–R176 arc concludes: bet #3 is an economic bet at ≈ 3.6×; components adopted along the way (fuel-cell/turbine bank, regenerative electrolysis, solar-bank inbound, hybrid injection) all survive as reactor-mission resilience assets too.
- **Follow-ons:** trajectory-scheduled lit-thrust model (the energy-limited assumption is the loosest plank); engine-mass floors on stage fractions; encode the full non-fission variant into mission_graph for canonical-sweep confirmation.
