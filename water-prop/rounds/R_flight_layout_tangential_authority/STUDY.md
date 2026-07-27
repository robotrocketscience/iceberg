# R-flight-layout-tangential-authority — the residual clears for nominal ops, but the bare 12-thruster count is single-fault intolerant

**Status:** run + STUDY complete 2026-07-22. **4/5 HELD** (H-A4 falsified — the pre-flagged genuine unknown). Result JSON `results/layout_findings.json`; figure `results/layout_authority.png`.
**Predecessor:** `R-berth-dump-axis-geometry` (`107bf5b`) closed the berth momentum-management thread on an **idealized cardinal ring**. This round makes the **one named residual** concrete (SATURN-SHIP-SPEC §7, matrix latest+25 deliverable f): does the real corner-mounted RCS keep plume-safe tangential couple authority about both in-plane axes?

## Hypothesis (pre-registered; see SCOPE.md)

The claim under test is that plume-safe tangential authority about both in-plane axes is "a generic property of any 3-axis-couple RCS." This round argued it is generic only for a **±z-distributed** layout, tested a realistic box-corner 12-thruster layout, and pre-flagged single-fault robustness (H-A4) as the genuine unknown because a minimal corner layout has only one tangential thruster per (direction, deck).

## Test

Deterministic pure-numpy. Realistic box-corner layout (bus half-dims 1.5×1.5×2.0 m; 8 corner-tangential + 2 prograde +z + 2 retro −z; F=5 N, Isp 70 s — all anchors identical to the berth rounds). 6×12 wrench map; exhaustive subset search for pure (|net force| ≤ 0.1 N, torque aligned to axis within 5 %) plume-safe (summed bag-plume torque < 2.5 N·m via the berth-dump `bag_plume` model, reused verbatim) couples about each axis and sense; single-fault sweep over all thrusters (distributed-12 and a redundant-16-tangential variant); aft-clustered pessimistic variant.

## Result

| Sub-claim | Predicted | Measured | Held? |
|---|---|---|---|
| H-A1 pure 3-axis couples | net force ≤ 0.1 N about x,y,z | x,y,z all pure (net force 0.00 N) | ✅ |
| H-A2 plume-safe in-plane couples ±x,±y | all four < 2.5 N·m bag-plume | all four exist, **20.0 N·m** each, bag-plume ≪ 2.5 | ✅ |
| H-A3 authority / dump / propellant | ≥ 10 N·m, ≤ 1800 s, ~42 kg | **20 N·m, 250 s, 42 kg** | ✅ |
| H-A4 single-fault robustness | both in-plane axes survive any 1 failure | **FALSIFIED — distributed-12 loses one couple sense on any tangential-thruster failure** (redundant-16 survives) | ❌ |
| H-A5 genericity ⇒ ±z distribution | aft-clustered has no plume-safe in-plane couple | aft-clustered: **0 plume-safe in-plane couples** | ✅ |

## Reading

**The berth-thread close survives on the real flight layout for nominal operations, and the vague "generic property" is now a concrete, quantified layout constraint — but the as-specced 12-thruster count is not single-fault tolerant for berth dump.**

1. **Residual clears (nominal).** Moving from the idealized cardinal ring to a realistic box-corner layout, pure plume-safe couples about **both** in-plane axes (±x, ±y) still exist at **20 N·m** each (arm 2·a_z = 4 m), dumping the ~5000 N·m·s berth injection in **250 s** for **42 kg** of water — identical to R-berth-momentum-management's despin-scaled figure. So the berth-dump leg-A verdict holds on the flight vehicle, not just the idealized ring.

2. **Corner penalty is real but negligible.** A box-corner "tangential" thruster sits offset in the transverse direction, so its plume tilts ~14° toward the bag (min plume-bag angle ~76°, vs the ring's exact 90°). This lands it technically inside the plume "core" cone, but the model's cos⁴ falloff makes the actual bag-plume torque ~0.03 N·m — ~74× under the 2.5 N·m re-perturbation threshold. The corner geometry costs almost nothing here; the ring's exact-90° purity was not load-bearing.

3. **H-A5 converts "generic" into a design rule.** An aft-clustered RCS (all 12 thrusters on one deck, |Δz| ≈ 0) yields **zero** plume-safe in-plane couples: with no z-separation an in-plane couple requires ±z (axial) thrusters separated in x/y, and the +z members fire their plume straight into the bag at high +z. **So the layout-drawing constraint is precise: the 12 RCS thrusters must be ±z-distributed (top and bottom deck), not clustered aft near the propulsion.** This is exactly the kind of latent placement assumption the residual asked us to confirm — it is not automatic.

4. **H-A4 is the real new finding (falsified [S], as flagged).** A minimal 8-tangential layout has exactly one plume-safe couple pair per in-plane sense (±x, ±y), so losing **any one** tangential thruster removes one couple sense — the distributed-12 layout is **single-fault intolerant** for berth dump. The redundant-16-tangential layout (two thrusters per direction·deck) survives every single failure. **Spec consequence:** if berth dump must be single-fault tolerant (a berth is a contact operation with a flexible multi-tonne bag — a stuck-closed RCS valve mid-dump should not strand the vehicle in an un-dumpable attitude), the RCS needs tangential redundancy beyond the bare 12, OR a qualified degraded mode. Two degraded modes exist and are cheap: (i) a **3-thruster asymmetric couple** whose small residual net force is absorbed by the 4×10 kg reaction wheels (the residual force-impulse over a 250 s dump is well inside wheel capacity — the wheels are only saturated by the *5000 N·m·s* injection, not by a small trim); (ii) a brief **plume-core dump with the aerogel intake retracted** (the berth-plume round already established grams-scale icing and 3.6-order pressure margin). Either removes the single-fault gap without new thrusters.

## Revisit

H-A1/A2/A3/A5 held as predicted; H-A4 fell exactly where the SCOPE flagged the risk ("the hypothesis most at risk — a corner layout has fewer redundant tangential thrusters per in-plane axis"). Consistent with methodology lesson 1 (pre-register pessimistically and let the [S] fall): the honest prior named the failure mode before the run. The one modeling choice that mattered was the plume-safe criterion — an initial hard "≥90° backflow" gate wrongly rejected the corner couples; correcting it to the berth-dump *torque* threshold (which is the actual re-perturbation criterion) is what surfaced that the corner penalty is negligible. That correction was made before grading and is documented in the run (the cos⁴ falloff, not the raw angle, is load-bearing). No inertia tensor was needed — couple authority is a wrench-map property, independent of mass properties (spec §1's deferred inertia tensor does not gate this result).

**Deferred (retest spec):** once the layout drawing exists (spec §1/§2), re-run this search on the *as-drawn* thruster positions and directions to confirm the ±z-distribution and per-sense redundancy; and quantify degraded-mode (i)'s reaction-wheel trim-impulse against the 4×10 kg cluster capacity for the worst single-fault couple. Both are drawing-dependent and named, not run here.

## Cross-learning

- **Forward to SATURN-SHIP-SPEC §7 + REQUIREMENTS §7.5 (demonstrator objective #4):** the momentum-management thread's leg-A verdict is confirmed for the flight layout under a **two-part constraint** — (a) RCS ±z-distributed, not aft-clustered (H-A5); (b) single-fault tolerance requires tangential redundancy or a qualified degraded mode (H-A4). This is a spec sizing input, not a closure-moving result — it does not touch any matrix axis verdict; it hardens the vehicle spec.
- **Methodology note:** a "generic property" claim in a spec is worth a concrete-layout round precisely because genericity claims hide placement assumptions (±z distribution) and fault-tolerance assumptions (per-sense redundancy) that only surface when you instantiate a real layout and fail a thruster. The idealized-model close (berth-dump) was correct but incomplete on exactly the two dimensions the word "generic" papered over.
- **Backward to R-berth-dump-axis-geometry:** its close is upheld (nominal plume-safe authority exists on the real layout); this round adds the redundancy/placement riders the idealized ring could not surface.
