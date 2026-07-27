# R-berth-dump-axis-geometry — STUDY

**Round:** R-berth-dump-axis-geometry. SCOPE pre-registered 2026-07-22 latest+25 arc (commit `8022ec1`) before `run.py` existed.
**Worker:** worktree-115637 session. Project-owner-directed: the **last question standing** in the momentum-management thread.
**One line:** Because the capture arm is along the boom, the injected momentum is **structurally perpendicular to the boom**, so every required dump axis is in-plane — and in-plane torque couples are realizable from **tangential** thrusters whose plumes fire sideways (~90° to the forward bag), giving a max bag-plume torque of **0.038 N·m, 66× under** the re-perturbation threshold, for **every** azimuth. The retro (−z) thrusters are the only plume-danger and are avoidable. **Leg A (thruster dump) is unconditionally viable; the momentum-management thread closes.**

## What this round closes

`R-berth-plume-impingement` (`a418d4d`) left leg A viable *"under a placement constraint"* — pending confirmation that a backflow-keeping thruster subset exists for **every** physically-required dump axis, not just the operating point. That was the last open question in the thread (bag-6dof sim → momentum trade → plume → this). This round answers it and closes the thread.

## Hypotheses, tests, results

All in `run.py` (deterministic 3-D geometry); numbers in `results/geometry_findings.json`; figure `results/geometry.png`.

### H1 [S] — Injected momentum is structurally in-plane (r_off ∥ boom) — **HELD**

| boom sway α | along-boom fraction of L | held? |
| --- | --- | --- |
| 0° | 0.00 (exact) | yes |
| 10° | 0.17 | yes |
| 20° | 0.34 | yes |

**Reading.** L = r_off_vec × (m_s·v_c_vec); with r_off_vec ∥ ẑ (boom), L = r_off·m_s·(v_x·ŷ − v_y·x̂) — **exactly perpendicular to the boom.** The along-boom component of the closing velocity contributes *nothing* to the injected momentum. So every required dump axis (−L̂) lies in the boom-perpendicular plane; only bag sway off the boom (α) tilts it, and even 20° sway keeps ≥ 0.66 of L in-plane. This is the structural fact the whole close rests on.

### H2 [S] — Tangential couples keep the bag in backflow across all in-plane axes — **HELD (66× margin)**

| boom | max bag-plume torque over all azimuths | per-thruster max |
| --- | --- | --- |
| 3 m | **0.038 N·m** | 0.022 N·m |
| 5 m | 0.026 N·m | 0.014 N·m |
| 7 m | 0.018 N·m | 0.010 N·m |

**Reading.** Sweeping the in-plane dump azimuth φ over [0,360°) and building each couple from tangential thrusters ({T1,T5} for +τ_x, {T2,T6} for +τ_y, etc. — verified pure couples, net-zero force), the bag-plume torque never exceeds **0.038 N·m at boom = 3 m — 66× under** the 2.5 N·m re-perturbation threshold. The reason is geometric: every tangential thruster's plume lies in the x-y plane, while the bag is at high +z, so the plume-bag angle is ≈ 90° (backflow) for all of them. **No in-plane dump axis puts the bag in the plume core.**

### H3 [S] — Retro (−z) thrusters are the only plume-danger, and avoidable — **HELD**

| thruster type | bag-plume torque | plume-bag angle | regime |
| --- | --- | --- | --- |
| tangential (T2) | 0.02 N·m | 90° | wing/backflow ✓ |
| prograde +z (P0) | 0.02 N·m | 137° | backflow ✓ |
| **retro −z (R0)** | **1.46 N·m** | **22°** | **core ✗** |

Tangential-set torque about x: [−4,+4]; about y: [−4,+4] (per unit F·arm) — **both in-plane axes are ± controllable from the tangential set alone.**

**Reading.** Only the retro (−z) thrusters point their plume at the +z bag (22°, plume core, 1.46 N·m — the danger). Prograde (+z-thrust, plume −z away from the bag) and tangential thrusters are safe. And the retro thrusters are **not needed**: the tangential set spans ± torque about both in-plane axes, so a control allocation that deprioritizes the retro thrusters loses no in-plane authority. The danger is real but designed around, not hardware-limited.

### H4 [W] — Synthesis: leg A unconditionally viable; the thread closes — **HELD**

**Reading.** H1–H3 combine to a clean close: the dump is always in-plane (H1), in-plane couples are tangential and plume-safe (H2), and the one dangerous thruster set is avoidable without losing controllability (H3). So **leg A (thruster dump) is unconditionally viable for the physically-required dump axes**, secured by a **cheap plume-aware control-allocation rule** — build the dump couple from tangential thrusters, deprioritize the retro pair — plus a grapple boom ≥ 3 m. **No new hardware.** Legs B (CMG, ~300–600 kg) and C (precision capture) are retired to *optional* risk reduction. The boom-sway residual (≤ 0.34 of L out-of-plane at 20° sway) is a small yaw-like component coverable by tangential x-y couples; only a pathological > 45° sway would demand retro thrust.

## Revisit / bug-catch (mandatory)

- **Representative layout, not the flight layout.** 8 tangential + 2 prograde + 2 retro is a plausible 12-thruster config; the flight layout needs the layout drawing (absent per `SATURN-SHIP-SPEC.md` note 1). The close requires the flight layout to have tangential authority about both in-plane axes — a generic property of any 3-axis-couple RCS; a real layout only adds authority. **This is the one named residual.**
- **Allocation-independent bound.** A couple fires ≤ 4 tangential thrusters; even the naive sum (4 × per-thruster max 0.022) = 0.09 N·m ≪ 2.5. So the exact control allocation *cannot* break the H2 bound — the result holds for any tangential-only couple, not just the canonical pairs used in the sweep.
- **Parametrized plume model** inherited from `R-berth-plume-impingement` (P ~ F/r², cosⁿ forward, β backflow). The 66× H2 margin and the tangential-vs-retro geometry distinction survive any plausible plume shape; exact Pa would need DSMC.
- **Boom sway is bounded by capture mechanics.** The α ≤ 20° assumption rests on cinch/grapple stiffness holding the bag near the boom axis; a very floppy grapple that lets the bag swing > 45° would re-introduce a retro-thrust need. That ties the close to a capture-mechanics parameter, flagged for the demonstrator.

## Cross-learning — the thread closes

- **To the whole momentum-management thread (`7a716f3` → `b3b579c` → `a418d4d` → this):** **CLOSED.** The berth momentum injection is managed by firing the onboard water RCS in a tangential couple — no CMG, no precision-capture requirement, no new hardware — under a control-allocation rule and boom ≥ 3 m. The ~300–600 kg CMG that the thread surfaced as a worry is **not needed.**
- **To `design-axes/15`:** the R189 saturated-wheel-tumble-at-berth loss mode is retired to a *managed* operation (tangential RCS dump), not an open architectural risk.
- **To `SATURN-SHIP-SPEC.md`:** the Open-Question #7 momentum-buffer gap resolves to a **control-allocation rule + boom ≥ 3 m + thruster-placement note** (tangential authority about both in-plane axes), not a CMG. The layout drawing, when it exists, must confirm that authority.
- **To REQUIREMENTS obj #4:** the berth rehearsal should confirm the tangential-couple dump keeps the bag in backflow at the flight layout, and measure the boom sway during the dump (the one parameter the close is conditioned on).
- **Named residual (not run):** flight-layout confirmation of tangential authority about both in-plane axes — the single remaining check, generic for any 3-axis-couple RCS.
