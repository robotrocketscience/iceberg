# R-closing-path-self-consistency — STUDY (pre-registration)

**Worker:** rhea-5 (`iceberg-rhea-5`), 2026-06-12. Adversarial self-test of THIS WORKER'S
OWN R-vehicle-mass-fidelity-refinement headline (H5 falsification / f ≈ 0.2 closure
revival), per the campaign's self-questioning convention (methodology lesson 11).
**Disclosure:** the code read of `phase1_leo_to_saturn.py` PRECEDED this registration and
motivates H1 — the hypotheses below are informed by static inspection; the experiments
(ledger walk, corrected re-sweep) had not been run when this file was written.

## The suspected inconsistency (from static read)

The kick-stage model (corrected once already for the "free delta-velocity" bug) checks
that kick wet mass fits within `dry_envelope = state.mass_kg − propellant − payload`
and then **subtracts kick propellant + kick dry from `state.mass_kg`**
(`phase1_leo_to_saturn.py:316-372`). Under open-loop v0 this was defensible: `mass_kg`
was a swept launch-manifest boundary condition with unallocated headroom. Under
closed-loop v1, `mass_kg` at low-Earth orbit is the DERIVED vehicle wet mass — the
"dry envelope" IS the vehicle's allocated subsystem hardware (reactor, radiators,
capture bag, thermal protection). Worked example at the fidelity round's closing cell
(30 kWe, 200 t chunk, f = 0.20): derived dry 110 t, wet 137.5 t; Helios kick propellant
from the rocket equation on 137.5 t at 4 km/s / 330 s ≈ 97.5 t; check passes
(102.5 ≤ 110); executor leaves **35 t of vehicle** to fly to Saturn — less than a third
of its own derived dry mass. The vehicle burns its own reactor as kick propellant.

## Hypotheses and predictions (registered before running)

**H1 (load-bearing).** An instrumented ledger walk of the closing path at the closing
cell violates the mass invariant: post-Phase-1 `mass_kg` < derived dry mass.
**Prediction: HELD — post-kick mass ≈ 0.3 × derived dry (≈ 35 t vs 110 t).**

**H2 (load-bearing).** Re-running the closure sweep with a self-consistent kick model —
kick stage must push ITSELF plus the vehicle (implicit stack equation), and the stack
must fit the most permissive launch manifest (multi-Falcon-6, 300 t) — collapses the
f-window closure. **Prediction: HELD.** Hand calculation: Helios stack for a 137.5 t
vehicle solves to ≈ 490 t (kick propellant ≈ 348 t), Star-class to ≈ 341 t — both over
the 300 t cap, a fortiori with realistic kick tankage scaling (fixed 5 t dry for 348 t
of propellant is already absurdly generous). Quantitative: 30 t floor → 0 cells; total
`arrived_at_depot` at best-f drops to the non-kick families only (prediction: ≤ 10 cells,
low-thrust-spiral survivors, possibly 0).

**H3.** Surviving corrected arrivals (if any) deliver < 30 t at the 0.85 capture anchor
(the kick-ballistic family WAS the entire 30 t closure set). **Prediction: HELD.**

**H4 (scope of damage).** Titan-6's f = 0.80 "0 closures" verdict is unaffected by this
bug — at f = 0.80 the kick paths already died on the (mis-specified but conservative-
at-high-f) envelope check. **Prediction: HELD — corrected f = 0.80 sweep still 0.**

**H5 (meta).** My fidelity round's OTHER verdicts survive: the f-window *mechanism*
(manifest headroom vs propellant need) remains real for non-kick families, and the
capture-multiplier coupling curve (Tier 1.5 round) retains its shape — only the absolute
closure counts collapse. **Prediction: HELD for the conditioning-curve shape; the
"H5 falsified" headline REVERSES to "H5 held under corrected kick physics."**

## Method

1. **Ledger walk (H1):** walk the exact closing path at the closing cell, print
   per-node VehicleState (mass, propellant, payload, time), check mass-invariant
   violations node by node against the derived dry mass.
2. **Corrected kick model (H2/H3/H4):** round-local patched `Mission` (no framework
   edits): kick options replaced with self-consistent stack equation
   `kick_prop = (m_vehicle_wet + kick_dry + kick_prop)(1 − e^{−Δv/(g·Isp)})`, gated on
   `vehicle_wet + kick_wet ≤ 300 t`. Re-run closure sweep f ∈ {0.15, 0.18, 0.20, 0.22,
   0.25, 0.30, 0.80} × capture multiplier ∈ {1.0, 0.43}.
3. **FINDINGS** with verdicts, prediction-error analysis, and — if H2 holds — a
   correction notice block for the fidelity round's FINDINGS (append-only; no rewriting
   of the prior round's file body) plus RUNNING_DOC and handoff corrections.

Declared risk to H2: the framework may contain a manifest mechanism I have not found
that legitimately reserves headroom for kick hardware (in which case H1 falsifies and
the fidelity headline stands). The ledger walk settles it either way.
