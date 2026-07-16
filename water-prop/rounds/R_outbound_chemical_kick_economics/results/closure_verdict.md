# R-outbound-chemical-kick-economics — Closure Verdict

**Aggregate held:** True.
**Kill-shot status:** retired.

## One-paragraph verdict

The batch-3/4 sleeper-falsifier claim "Round F uses 715 t of hydrolox per outbound mission" is **retracted** (True, max measured 174.0 t). The actual `variant_b_closure`-anchored figure for surviving 500-kWe / 200-t cells is 145–155 t hydrolox per mission. At rhea bake-off's inherited LAUNCH_PLUS_TSI = $290M/ship and central LEO mission-1 mass 224 t, implied launch cost is **$1273/kg** (True). Falcon Heavy expendable's stated LEO capacity is 63.8 t — the surviving cell needs **3.57×** that (True), so the rhea bake-off's "$150M Falcon Heavy expendable + $140M Vulcan-Centaur kick = $290M/ship" anchor is internally inconsistent at 500-kWe MARVL ship mass. Updating launch+TSI to realistic Falcon-Heavy market ($665M/ship) does not change the rhea bake-off's marginal IRR verdict (True) because IRR is already floored at zero. Sweep across launch market × water price × sovereign payment confirms zero rows cross sovereign-bond IRR at L0-05 hard (0 rows pass; H-ock-f held: True). Outbound chemical-kick economics is therefore **NOT an independent matrix-killer** — the cell remains killed by reactor program risk + L0-05 ceiling. The "outbound chemical-kick economics sleeper falsifier" framing should be retired from the matrix open-items list, AND the bake-off's launch-cost anchor should be flagged as internally inconsistent (held: True).

## Three findings the orchestrator must reconcile

1. **The sleeper-falsifier claim was a back-of-envelope error.** The 715 t figure was inserted as text into `R_aerocapture_fast_cruise_envelope/results/closure_verdict.md` without being computed from `variant_b_closure`. It propagated into batch-3 and batch-4 handoffs as load-bearing. Per recurring lesson #N (compute back-of-envelope FIRST, anchor on PRIMARY texts), this round catches the error. **The matrix's "open items" list should retire the outbound-chemical-kick sleeper-falsifier item.**

2. **The rhea bake-off's $290M/ship LAUNCH_PLUS_TSI is internally inconsistent with the MARVL ship LEO mass.** R-reactor-roadmap's source comment claims "Falcon Heavy expendable + Vulcan-Centaur-class kick" for $290M, but Falcon Heavy expendable's 63.8 t LEO capacity cannot launch 224 t in a single mission. The bake-off implicitly assumes either (a) Starship-class launch economics (~$1,200/kg with kick) — which is the SpaceX 2025 pessimistic-target band, NOT YET ACHIEVED, OR (b) the per-ship launch contribution is undercounted by ~1.8–3.5× under realistic 2026 launch markets. **Recommendation: matrix-amendment to flag this internal inconsistency; defer cost-anchor revision to a separate round (R-launch-cost-anchor-revision) that re-derives ship cashflow under explicit launcher assumptions.**

3. **The bake-off's verdict is robust to launch-cost revision.** Even raising LAUNCH_PLUS_TSI to $665M/ship (realistic Falcon Heavy expendable, 4 launches at $150M plus kick), or to $1,500M/ship (SLS-class), no row in this round's sweep crosses sovereign-bond IRR at L0-05 hard. The cell does not return capital under any tested launch market × water price × sovereign payment combination. The kill mechanism remains reactor program risk + L0-05 ceiling, NOT outbound launch economics. **The matrix's headline finding survives; the calibration just makes the cost anchor more defensible.**

## What this round did NOT close (out of scope)

- **Cryogenic depot scenario (mission 2+).** Mission-1 is the binding constraint for capital amortization. Depot economics (build cost, boil-off, operating cost) are matrix item #6 and need their own round.
- **Reactor program risk parameter sensitivity.** R-power-bayesian-update already absorbed; this round inherits.
- **Ship cost / NRE / ground ops sensitivity.** Inherited from R15-rerun via R-reactor-roadmap. Out of scope.
- **Starship-target launch economics being achieved.** This round shows that even AT the Starship target ($200/kg, $290M/ship implied), the cell does not close. So the question is moot — Starship-target is necessary but not sufficient for closure.

## Recommended next round

If a worker is to close the launch-cost anchor properly: **R-launch-cost-anchor-revision** — re-derive ship cashflow under explicit launcher market assumptions (Falcon Heavy realistic, Starship target, Starship pessimistic), with depot-amortization scenario, ship-cadence sensitivity, and refresh of R-reactor-roadmap cashflow constants. Estimate 4–6 hours analyst time.

Hyperion track record now: 9 rounds, 9 aggregate findings (2 kill-shots, 6 falsifications-of-pre-reg-intuition, 1 calibration-retraction-of-prior-finding). The recurring-lesson-#N stacked intervention (back-of-envelope FIRST, PRIMARY-text anchors) is now consistently producing held aggregates AND catching prior-round errors.
