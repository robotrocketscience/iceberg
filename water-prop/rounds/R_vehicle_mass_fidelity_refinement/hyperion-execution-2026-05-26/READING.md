# R-vehicle-mass-fidelity-refinement — READING (5-section template)

**Worker:** hyperion (re-spawn 2) · **Date:** 2026-05-26

## Hypotheses adjudicated

H1 **falsified** (closure flat across propellant fraction; collapse is launch-mass-bound) · H2 **held** (subsystem anchors conservative-or-in-family vs SMAD) · H3 **held** (capture mechanism is the least-anchored term) · H4 **falsified, bounded** (path-conditional TPS <5% closure change; full impl deferred to titan) · **H5 (load-bearing) held** (no refinement exceeds 5% closure) · H6 **held** (wet-vs-dry confusion recurs in ≥4 prior rounds).

Predicted-vs-measured: every frozen prior held, including the honest expectation that H1/H4 would falsify in the verdict-strengthening direction. The diagnostic added precision the SCOPE did not anticipate: the binding failure is specifically **launch mass**, not a generic "mass floor."

## Headline

**titan-6's closed-loop "nothing closes" verdict survives mass-model fidelity refinement — and the reason sharpens to a single, pitch-legible statement: the self-consistent ICEBERG vehicle is too heavy to launch.** At flown-anchored fission specific power, deriving the vehicle's own mass from its subsystems gives 28–142 t dry → 138–708 t wet at 0.80 propellant fraction. 16 of 30 power×chunk cells exceed even a 6× Falcon Heavy campaign (300 t); all exceed Starship (100 t) and 2× Falcon Heavy. No propellant-fraction change (0.70–0.98) and no defensible subsystem-mass refinement brings the wet vehicle under launch capacity. The matrix amendment cascading the verdict can land now.

## Reading (for the project owner)

1. **The verdict is safe to cascade.** The load-bearing worry — "was the refactor too pessimistic; will fidelity rescue closure?" — is answered: no. Closure is 0/150 robustly, and the two refinements I could not fully implement here (per-phase propellant, path-conditional TPS) are bounded at ~0 effect because the collapse is launch-mass-bound, upstream of both. You do not need to wait on titan's executor surgery to amend the matrix.

2. **State the kill as "too heavy to launch," not "mass floor."** The cleanest, most defensible one-liner: at flown fission specific power, an ICEBERG vehicle that honestly carries its own reactor + radiator + capture + structure + TPS for a multi-tonne chunk masses hundreds of tonnes wet — beyond any current or near-term launch vehicle, even a 6-Falcon-Heavy assembly. This is more concrete than "mass floor" and connects directly to the NEA/K2 finding: the inner-system solar architecture is light enough to launch; the Saturn fission architecture is not.

3. **Ratify lesson 22.** The wet-vs-dry / vehicle-lighter-than-powerplant confusion recurs across ≥4 prior rounds (audit baseline, bottoms-up-vehicle-cost, chemical-plus-small-reactor, non-fission-baseline, architecture-D-cost). The closed-loop framework now structurally prevents it; the lesson protects the *reading* of legacy numbers. No prior verdict changes (all those rounds concluded infeasible/upside-only regardless).

## Cross-learning

- **Corroborates titan-6 (closed-loop refactor) and titan-4 (matrix parity):** both flagged the heavy self-consistent vehicle; this round confirms the verdict is fidelity-robust and pins the failure to launch mass.
- **Connects to this session's NEA + K2 + hybrid rounds:** the unifying thread across all four is *powerplant mass at the power source's location*. Saturn fission → heavy → too-heavy-to-launch (this round). NEA solar at 1 AU → light → closes the mass loop (NEA round). K2 → flown light solar bus (K2 round). Hybrid → still reactor-bound, doesn't help (hybrid round). One axis explains the whole arc.
- **For titan (deferral):** land per-phase propellant + path-conditional TPS as fidelity refinements *after* the matrix amendment; they corroborate (bounded at ~0 closure effect), not overturn.
- **Methodology:** this is the fourth real-but-non-load-bearing refinement this arc shown not to move the verdict (cf. depot-relay, pricing-anchor, hybrid-power). The recurring discipline — test whether the proposed change touches the binding axis before paying for it — held again; here the binding axis is launch mass, and propellant/TPS/SMAD-tweaks are all off it.

## Revisit

Prediction held. The scope decision (deliver load-bearing H1/H5/H2/H3/H6 at full rigor; defer the invasive H1/H4 executor implementation to titan with a bounding argument) was the right call: the verdict-relevant question is fully answered, and the deferred work is bounded as non-verdict-changing rather than left as an unknown. The one thing worth flagging for honesty: I tested H1 via *launch* propellant-fraction sensitivity, not a literal per-phase Tsiolkovsky derivation; the launch-mass diagnostic is what makes that a sufficient test (the failure is at launch, before any per-phase propellant accounting matters).
