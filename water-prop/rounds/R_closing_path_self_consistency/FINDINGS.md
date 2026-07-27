# R-closing-path-self-consistency — FINDINGS

**Worker:** rhea-5, 2026-06-12. Adversarial self-test of this worker's own
R-vehicle-mass-fidelity-refinement headline. Pre-registration: STUDY.md (disclosed:
code-read preceded registration). Artifacts: `run.py` (ledger walk + corrected-kick
sweep), `results/self_consistency.json`; framework fix + regression tests shipped in the
same branch (`phase1_leo_to_saturn.py`, `tests/test_kick_stage_manifest.py`).

## Headline: the fidelity round's closure revival was a framework bug. REVERSED.

The f ≈ 0.2 closure window — the basis for "H5 falsified" in
R-vehicle-mass-fidelity-refinement — was manufactured by v0-era kick-stage manifest
semantics surviving into the closed-loop v1 framework. The kick model carved its wet
mass out of the vehicle's "dry envelope" and subtracted it from the vehicle's state.
Under open-loop v0 that envelope was unallocated manifest headroom; under closed-loop
v1 it is the vehicle's derived hardware. The ledger walk of the closing path shows the
consequence directly: **after the Helios kick, 9.2 t of vehicle remained — against
93.2 t of derived reactor + radiator + capture-bag hardware — and that ghost ship then
"captured" 170 t of chunk and delivered 45.3 t.** With self-consistent kick physics
(the stage pushes itself plus the vehicle; stack gated at even the most permissive
300 t manifest), **closure is 0 of 150 cells at every propellant fraction (0.15–0.80)
and every capture multiplier (1.0, 0.43). Titan-6's collapse verdict is restored,
stronger than before: it now holds across the entire f axis.**

## Verdicts

| Hypothesis | Verdict | Predicted | Measured |
|---|---|---|---|
| H1: closing path violates the mass invariant | **HELD, worse than predicted** | post-kick ≈ 35 t vs derived dry | post-kick **9.2 t** vs 93.2 t derived dry; 7 of 10 path nodes below derived dry |
| H2: corrected kick collapses the f-window closure | **HELD at the zero end** | ≤ 10 surviving arrivals, possibly 0 | **0 arrivals everywhere** — every one of the fidelity round's 45–50 "arrivals" was kick-routed |
| H3: survivors deliver < 30 t | **HELD (vacuously)** | held | no survivors exist |
| H4: titan-6's f = 0.80 verdict unaffected | **HELD** | corrected f = 0.80 still 0 | confirmed (0/0/0/0) |
| H5: fidelity round's other findings survive; its headline reverses | **HELD** | reversal | "H5 falsified" → **"H5 held under corrected physics"**; the f-window *mechanism* and Tier-1.5 capture-physics findings stand; the specific closure couplings quoted in both rounds are void |

## Prediction-error analysis

1. **H1's magnitude error (9.2 t vs predicted 35 t):** my hand calculation skipped the
   12 % autonomous-assembly mass penalty (applied before the kick) and used a stale
   per-cell derivation. Direction right, magnitude 4× off — consistent with the
   campaign's lesson that hand-checks bound but do not replace ledger instrumentation.
2. **H2 landing at exactly 0:** I hedged at "≤ 10 spiral survivors." In fact the
   low-thrust spiral family never arrives at ANY f: at low f it lacks propellant
   (needs f ≈ 0.36 equivalent), at high f it exceeds manifests, and in between the
   burn-time-vs-coast-window gate kills it. The kick bug was not merely inflating
   closure — it was the *sole* source of every arrival in the fidelity round.
3. **The bug's fingerprint was visible one round earlier and I missed it.** The
   fidelity round's own ledger printed `best=45.3 t delivered` from cells whose wet
   vehicles could not plausibly carry a kick — I treated the closing-path option list
   as a finding rather than auditing its mass ledger then. Round-design lesson: any
   round that produces a NEW closure surface must ship a single-path mass-ledger walk
   as a standard artifact (candidate PROTOCOL lesson 25).

## Framework changes shipped (orchestrator review requested)

- `phase1_leo_to_saturn.py`: second kick-model correction — self-consistent stack
  equation, stack gated at `MAX_KICK_MANIFEST_KG = 300 t` (most permissive; documented
  approximation — exact per-manifest gating needs the walker state to carry the Phase-0
  manifest choice, titan follow-on). Executor no longer touches vehicle mass.
- `tests/test_kick_stage_manifest.py`: 3 new regression tests, including the
  closing-cell counterexample.
- `tests/test_phase1_demo.py`: 3 kick tests rewritten — they pinned the old
  dry-envelope-carving semantics.
- Enumeration count pins updated with history lines (4005 → 9669 total; 798 → 2066
  feasible): the corrected kick legitimately opens kick access to LIGHT open-loop
  vehicles (a 50 t vehicle CAN ride a 190 t stack) while pruning heavy ones.
- **Side effect the orchestrator must re-derive:** the v0 open-loop baseline closure
  surface changed (now 30 of 750 cells close the 30 t floor; 64 at 10 t). Titan-6's
  "0/150 closed vs 16/150 open" comparison ratio needs recomputation against the
  corrected baseline. Closed-loop at f = 0.80 remains 0 everywhere.

## Matrix amendment specification (supersedes the fidelity round's §"What this means")

1. The state-of-record statement reverts to: **closed-loop closure is 0 of 150 cells at
   L0-04 = 25 t at every propellant fraction and every capture anchor.** The pause on
   titan-6's amendment cascade can lift; the cascade lands as titan-6 wrote it.
2. The fidelity round's surviving contributions: per-phase propellant fraction remains
   the right refinement (titan-7 proper); the f-window mechanism is real but no family
   currently exploits it legitimately; lessons 23/24 candidates stand.
3. The Tier-1.5 capture round's physics (0.549 capture, penetration-dominant failures,
   design levers, bench-test recommendation) is framework-independent and stands; its
   closure-coupling table (28.5 t / 48.5 t) is void.
4. The capture bench test remains the highest-value evidence for the DEMONSTRATOR
   thesis, but it no longer carries a commercial-class closure on its back — under
   corrected physics nothing closes commercial-class regardless of capture efficiency.
