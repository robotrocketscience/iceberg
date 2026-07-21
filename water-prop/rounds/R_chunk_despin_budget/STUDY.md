# R-chunk-despin-budget — STUDY

**Round:** R-chunk-despin-budget. SCOPE pre-registered 2026-07-20 (commit `2f781d7`) before `run.py` existed.
**Worker:** worktree-115637 session. Project-owner-directed: "de-spin adds a fuel loss and reduces delivered water — quantify it."

## Hypotheses, tests, results

All computations in `run.py` (seed 0); headline numbers in `results/despin_findings.json`; figures in `results/`.

### H1 — de-spin propellant negligible at the Tier 0.5 prior

**Claim:** p95 de-spin propellant < 1 kg for 10–200 t chunks, cold-gas RCS (Isp 70 s, arm 3 m, η 0.7, tumbling ×1.5).

**Result:**

| metric | predicted | measured | held? |
| --- | --- | --- | --- |
| worst-case p95 propellant | < 1 kg | **1.64 kg** (200 t porous, 500 kg/m³) | **FALSIFIED** |
| same case, p50 | — | 0.36 kg | — |
| solid-density cases, p95 | < 1 kg | ≤ 1.1 kg | mixed |

**Reading.** The registered bound missed by 1.64× — exactly the (900/500)^(2/3) ≈ 1.5 inertia inflation of the porous case that the SCOPE's own parameter grid contained but the bound-setting back-of-envelope ignored. The qualitative claim survives untouched: 1.64 kg against a 25,000 kg delivery floor is 0.0066 percent.

### H2 — stress tail bounded

**Claim:** at a deterministic 1 rpm (two orders above the decameter prior median), 200 t porous chunk: < 125 kg cold-gas, < 15 kg on the 800 s thruster.

**Result:**

| metric | predicted | measured | held? |
| --- | --- | --- | --- |
| cold-gas propellant at 1 rpm | < 125 kg | **182 kg** | **FALSIFIED** |
| MET-800 propellant at 1 rpm | < 15 kg | **15.9 kg** | **FALSIFIED** (marginally) |

**Reading.** Same porous-inertia miss. Absolute reading: 182 kg is 0.73 percent of the floor, at a spin rate the Cassini Composite Infrared Spectrometer evidence and Ohtsuki collisional equilibrium both say ring chunks of this size do not sustain (collisions re-equilibrate spin every ~10 hours). If the mission ever meets a 1 rpm decameter chunk, the correct response is chunk selection (move to the next one), not propellant budgeting.

### H3 — passive fabric damping under one hour

**Claim:** cinch pressure ≥ 10 Pa, μ = 0.1: residual chunk spin self-damps inside the bag in < 1 hour everywhere up to 1 rpm.

**Result:**

| metric | predicted | measured | held? |
| --- | --- | --- | --- |
| worst damping time in envelope | < 3,600 s | **5,323 s** (1 Pa cinch, 200 t, 1 rpm) | **FALSIFIED** |
| at 10 Pa cinch, same case | — | 532 s | (registered condition holds) |

**Reading.** The falsifier tripped on the 1 Pa corner of the sweep, which the hypothesis text excluded ("≥ 10 Pa") but the falsifier-as-written scanned. Protocol reading: falsified as registered; held on the stated operating condition. Lesson recorded: write the falsifier over exactly the domain the claim names. Physically the result is strong: at any plausible cinch tension the bag de-spins its own cargo passively in minutes — active chunk-relative de-spin machinery is unnecessary.

### H4 — stack spin-up absorbable — **HELD**

Worst median-prior stack rate after capture: **0.0086 deg/s** (bound 0.1); 1 rpm stress tail peaks at 3.9 deg/s (bound 5). Angular-momentum transfer from the chunk to the stack is an ordinary attitude-control event, not a mission event.

### H5 — closure impact nil — **HELD** (after bug catch)

Charging every cell of the audit sweep (48 cells, `20260522T175555Z`) with the p95 de-spin propellant: **0 of 5 closing cells flip** at the 25 t floor.

**Bug catch (protocol §bug-catch):** the first run read a nonexistent `delivered_mass_kg` field, scored every cell zero, and reported H5 as vacuously held over "0 of 0" cells. Caught because the denominator was impossible (the audit round closes 5 cells). Fixed to `leaf_state.payload_kg`; the corrected denominator matches the audit round's own count. One-line lesson: a hypothesis that "holds" with a zero denominator has not been tested.

## Revisit (mandatory)

Three of five registered bounds fell, all in the same direction and for the same reason: I set numeric bounds from a solid-ice back-of-envelope and then registered a parameter grid whose conservative corner (porous 500 kg/m³) inflates moment of inertia by ~1.5×. The predictions were wrong; the architecture conclusion is unchanged. **Methodology lesson: register bounds against the worst corner of your own declared grid, not the central case.**

The larger revisit is about the question itself. The project owner's concern — "de-spin costs fuel and reduces delivered water" — is quantitatively refuted at ring-chunk spin rates: grams to single kilograms at the evidence-based prior, tenths of a percent of the floor even at implausible tails, zero closure impact. But the exercise surfaced where spin-adjacent mass cost actually lives, and it is not de-spin:

1. **Capture success under spin** — already the campaign's single most load-bearing axis (A14; the capture Monte Carlo carries spin-rate sensitivity explicitly). De-spin propellant is not the mechanism by which spin threatens this mission; failed capture is.
2. **Thrust-phase attitude control of an offset, shifting center of mass.** The inbound burn pushes a stack whose cargo is an irregular chunk in a fabric bag — center of mass off the thrust line by decimeters, and *walking* as the sublimation harvest draws the cargo down asymmetrically over years. A first-look bound in this round's margin: fighting a 0.5 m offset with corner RCS over the full inbound burn is a **hundred-tonne-class** propellant absurdity, while steering thrust through the center of mass reduces it to a cosine tax in the tens-of-kilograms class. That gap — four orders of magnitude hinging on thrust-vector-control authority — is unpriced anywhere in the campaign.

## Cross-learning

- **Adopt:** de-spin drops from the open-questions list as a fuel item; carries forward only inside A14 (capture mechanics).
- **Negative for** the pitch's silence on gimbal authority: SATURN-SHIP-SPEC.md carries no thrust-vector-control requirement through a shifting cargo center of mass.
- **Follow-on (SCOPE'd next): R-com-offset-thrust-alignment** — pre-register the RCS-fought vs steer-through-center-of-mass comparison, the gimbal-authority requirement as a function of offset envelope, and the sublimation center-of-mass-walk model. This is the round the owner's instinct was actually pointing at.
- Orchestrator handoff: design-axes and matrix amendments are orchestrator-owned; this round's outputs are the two figures, the findings JSON, and this STUDY.
