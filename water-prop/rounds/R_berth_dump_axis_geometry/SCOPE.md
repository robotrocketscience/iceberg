# R-berth-dump-axis-geometry — does a plume-safe dump couple exist for every required axis?

**Status:** SCOPE pre-registered 2026-07-22 (latest+25 arc), before `run.py` was written or executed.
**Worker:** worktree-115637 session. Project-owner-directed: the **last question standing** in the momentum-management thread — `R-berth-plume-impingement` left leg A viable *"under a placement constraint"* pending confirmation that a backflow-keeping thruster subset exists for every physically-required momentum-dump axis.
**Predecessors:** `R-berth-plume-impingement` (`a418d4d`) — plume benign in backflow, re-excites in core; the open residual is the worst-case dump axis. `R-berth-momentum-management` (`b3b579c`) — the 3-leg trade. `bag_dynamics_6dof` sim (`7a716f3`) — the 5000 N·m·s injection. `SATURN-SHIP-SPEC.md` — 12 water cold-gas RCS at envelope corners; bag on a grapple boom.

## The structural insight this round tests

The capture arm `r_off` is **along the grapple boom** (+z). The injected momentum is L = r_off_vec × (m_s·v_c_vec); with r_off_vec ∥ ẑ this is L = r_off·m_s·(v_x·ŷ − v_y·x̂) — **always in the boom-perpendicular (x-y) plane**, because the along-boom component of the closing velocity contributes nothing to L. So *every* required dump axis (−L̂) lies in-plane. In-plane torque couples can be built from **tangential** thrusts (in x-y) at z-offset, whose plumes point sideways — away from the forward bag at high +z. The only plume-dangerous thrusters are the **retro** (−z) ones, whose plume points at the +z bag; the claim is that they are *avoidable* for in-plane dumps. This round verifies that against a concrete 12-thruster layout and boom-sway.

## Question

Given the fixed 12-corner RCS layout and the fixed forward grapple position, does a plume-safe (bag-in-backflow) thruster couple exist for every physically-required momentum-dump axis — closing the leg-A verdict — or is there a required axis that forces a plume-core hit on the bag (which legs C/B would then have to retire)?

## Boundary

- **IN:** the direction of the injected momentum from capture geometry (in-plane, with boom-sway sensitivity); a concrete 12-thruster layout (8 tangential + 2 prograde + 2 retro); per-axis plume-torque on the bag from the couple that produces it; controllability of ±torque about both in-plane axes from the tangential set alone; the plume-aware control-allocation rule that keeps the bag in backflow.
- **OUT:** DSMC plume (parametrized model, per the plume round); the injection magnitude (`bag_dynamics_6dof` owns it); reaction-wheel/CMG sizing (`R-berth-momentum-management`); the exact flight thruster layout (uses a plausible representative layout — a real layout only improves on it if it has more tangential authority).

## Pre-registered hypotheses (numeric, falsifiable, written before the run)

**H1 [S] — The injected momentum is structurally in-plane; every required dump axis lies in the boom-perpendicular plane.** L ⊥ boom exactly for r_off ∥ boom. **SCOPE:** |L·boom|/|L| = 0 at zero sway; < 0.35 for boom sway α ≤ 20°. **Falsified** if realistic capture geometry puts > 0.5 of L along the boom.

**H2 [S] — In-plane couples from tangential thrusters keep the bag in backflow: max bag-plume torque ≪ 2.5 N·m at boom ≥ 3 m.** Tangential plumes lie in x-y; the bag is at high +z → plume-bag angle ≈ 90° (backflow). **SCOPE:** max tangential bag-plume torque < 2.5 N·m across all in-plane dump axes at boom ≥ 3 m (measured ~0.02 N·m). **Falsified** if any tangential couple exceeds 2.5 N·m.

**H3 [S] — The retro (−z) thrusters are the only plume-dangerous ones, and they are avoidable.** Retro plume points at the +z bag (core, ~22°, ~1.5 N·m); prograde and tangential plumes do not. The tangential set spans ± torque about both in-plane axes (x and y), so excluding the retro thrusters retains full in-plane controllability. **SCOPE:** tangential-set torque_x and torque_y both span ± ; excluding retro loses no in-plane axis. **Falsified** if an in-plane axis is uncontrollable without the retro thrusters.

**H4 [W] — Synthesis: leg A is unconditionally viable for the required dump axes; the momentum thread closes.** Because the dump is always in-plane and in-plane couples are tangential/plume-safe, a plume-aware control-allocation rule ("build the dump couple from tangential thrusters, deprioritize retro, keep boom ≥ 3 m") makes leg A safe for every required axis with **no new hardware** — legs B/C are fully optional. **SCOPE:** leg A plume-safe for all in-plane axes at boom ≥ 3 m AND the boom-sway along-boom residual (≤ 0.35 of L at α ≤ 20°) stays plume-manageable (the small out-of-plane component needs only a small tangential-dominated correction). **Falsified** if a realistic geometry (sway, layout) forces a plume-core hit on some required axis.

**Honest expected reading:** H1–H3 hold on clean geometry; H4 is [W] because it rests on (a) the representative layout having tangential authority about both in-plane axes — a real flight layout must be checked but generically does — and (b) boom-sway keeping the dump axis near-in-plane. The likely verdict is **the momentum thread closes: leg A is the baseline, secured by a control-allocation rule + boom ≥ 3 m, with legs B/C retired to optional** — a genuine close, not a punt.

## Method

Closed-form 3-D geometry, deterministic. All in `run.py`:

- **Layout:** envelope half-size a = 4 m, half-height h = 4 m; 12 thrusters = 8 tangential (top/bottom faces, ±x/±y) + 2 prograde (+z, plume away from bag) + 2 retro (−z, plume at bag). Bag at (0,0,z_bag), z_bag = h + boom + r_bag, boom ∈ {3,5,7} m, r_bag = 3 m.
- **Plume-on-bag:** for each firing thruster, plume dir = −thrust dir; θ = angle to (bag − pos); P(θ,r) = P_iso·κ·cosⁿθ forward, P_iso·β backflow (κ=4, n=4, β=1e-2); torque = P·A_eff·r_off, A_eff = min(bag area, plume-spot area).
- **Axis sweep:** in-plane dump azimuth φ ∈ [0,360°); build the tangential couple producing torque about (cosφ, sinφ, 0); sum bag-plume torque over firing thrusters; take max over φ.
- **Controllability:** torque_x, torque_y ranges of the tangential set (± span check).
- **Boom-sway:** along-boom fraction sin(α) for α ∈ {0,10,20}°; check dump axis stays near-in-plane.
- **Retro contrast:** compute the retro-thruster bag-plume torque to show it is the (avoidable) danger.

**Anchors:** τ_dump 50 N·m, re-perturb threshold 2.5 N·m, injection in-plane (sim + `R-berth-plume-impingement`); 12 corner thrusters (`SATURN-SHIP-SPEC.md`); F = 5 N, cold-gas Isp 70 s. Representative layout flagged as such in the bug-catch.
