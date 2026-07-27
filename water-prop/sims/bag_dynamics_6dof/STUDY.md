# Bag-dynamics 6-DOF coupled slosh + ACS sim — STUDY

**Sim:** `water-prop/sims/bag_dynamics_6dof/` (worktree-115637, 2026-07-21 latest+25). Basilisk 2.10.2, run on archon (`ssh jso@archon`, `~/venvs/iceberg-basilisk-sims`).
**One line:** R191's named 6-DOF follow-on. It **confirms** R191's mean-zero-slosh viable corner (for the favorable monolithic host) **and overturns its framing of the gate**: the berth *capture transient* injects net angular momentum that reaction wheels cannot remove, so **no (T_s, ζ, host) cell is RW-viable for a realistic berth — momentum-dumping thrusters are mandatory, not merely "forced for stiff bags."**

## What R191 predicted (the thing this sim exists to test)

R191 `R_bag_dynamics_envelope` (lumped desk model) H4: *a comfortable design point exists but is narrow — ~9 % of the T_s × ζ grid is reaction-wheel-controllable and settles inside a 30-min berth window (~35 % if thrusters allowed). The desk model **locates** the corner but **cannot verify coupled stability inside it** — that is the Basilisk 6-DOF `linearSpringMassDamper` follow-on.* The desk model's control test was **disturbance torque vs RW torque authority** (~5 N·m).

## Setup

Basilisk `spacecraft` hub (mothership host + rigid half of the 40 t bag) + a `linearSpringMassDamper` slosh particle (the other 20 t, f_s = 0.5) at r_off = 5 m, coupled to 3 orthogonal reaction wheels (u_max 5 N·m, 100 N·m·s each) under MRP-feedback inertial-hold ACS. Slosh mapping: ω = 2π/T_s, k = m_s ω², c = 2 ζ m_s ω. Grid: T_s ∈ {60,100,140,180} s × ζ ∈ {0.02,0.05,0.10,0.20} × host ∈ {monolithic 20 t, relay 4 t}, **two seed modes**:
- **`capture_impulse`** — slosh seeded with ρ̇ = v_c = 0.05 m/s (a realistic soft-capture berth). Injects **net** angular momentum L = m_s·v_c·r_off = **5000 N·m·s**.
- **`displacement`** — slosh seeded with ρ = 0.10 m, ρ̇ = 0 (mean-zero oscillation; **net L = 0** — R191's implicit picture).
2-hour integration, 0.5 s step. Deterministic. `results/bag_6dof_findings.json`, figure `results/bag_6dof.png`.

## Result

| Seed mode | host | RW-viable cells | RW saturates | peak attitude | reading |
|---|---|---|---|---|---|
| **capture_impulse** | monolithic | **0 / 16** | 16 / 16 | 180° (tumble) | injected 5000 N·m·s ≫ 300 N·m·s RW store; conserved |
| **capture_impulse** | relay | **0 / 16** | 16 / 16 | 180° (tumble) | same; residual body L ~1370 N·m·s at 2 h |
| **displacement** | monolithic | **16 / 16** | 0 / 16 | ≤ 1.0° | mean-zero slosh: RWs handle it, settles 2–10 min, peak 7 N·m·s |
| **displacement** | relay | 0 / 16 | 0 / 16 | ≤ 1.1° | mean-zero but light host: attitude damps too slowly for the 30-min window |

**Cross-check (validity):** a diagnostic sweep of the capture rate showed the threshold is exactly the momentum balance — at v_c = 0.001 m/s (L = 100 N·m·s ≈ RW capacity) the vehicle holds to 4.5°; at v_c ≥ 0.005 (L ≥ 500) it saturates and tumbles. The control loop is correct (mean-zero 10 cm slosh settles cleanly on the monolithic host); the tumble is physics, not a broken controller.

## Reading

**The desk model asked the wrong question, and this sim shows why.** R191 compared slosh *disturbance torque* to RW *torque authority* and found a narrow-but-real controllable corner. The 6-DOF coupled dynamics reveal that the binding constraint is **angular-momentum conservation**, not torque:

1. **A reaction wheel stores angular momentum; it cannot remove it.** A berth capture that is even slightly off-center imparts net angular momentum L ≈ m_s·v_c·r_off. For the campaign's numbers (20 t slosh, 5 cm/s soft capture, 5 m arm) that is **5000 N·m·s — ~17× the 300 N·m·s the three wheels can store.** The wheels saturate and the residual momentum is left in the vehicle body, which tumbles. **Damping the slosh dissipates energy but not momentum**, so no ζ and no T_s rescues it. **0 of 32 capture-berth cells are RW-viable.**
2. **R191's corner is real only in the zero-net-momentum idealization.** With a mean-zero slosh (displacement seed, L = 0), the monolithic host is RW-viable across the whole grid (settles 2–10 min, peak 7 N·m·s) — R191's H4 corner is **confirmed for the favorable host**. But the light relay host (slosh:host mass ratio 5:1) loses even that: the mean-zero slosh drives ~1° attitude that damps too slowly to settle within 30 min over most of the grid.
3. **Thrusters are mandatory — for momentum management, not just plume-torque.** A 50 N·m thruster couple dumps the injected 5000 N·m·s in **100 s**, well inside the berth window. This is R191's "thrusters forced" conclusion, but reached for a stronger and more general reason: it holds for *any* off-center berth, not only stiff (short-T_s) bags. The plume-contamination-near-the-bag concern R191 raised is therefore **not optional** — thruster firing at the berth interface is on the critical path.

**Net contribution vs R191:** the sim does what a coupled 6-DOF model is for — it exposes a conservation-law gate the lumped torque-vs-authority model structurally could not. R191's "desk-irreducible unknown" is now resolved: the coupled attitude dynamics are stable for a well-behaved mean-zero slosh on a heavy host, but the **berth transient itself** is the design driver, and it is a **momentum-management** problem requiring thrusters, RCS momentum budgeting, and (ideally) a capture geometry that minimizes r_off.

## Caveats / honesty posture

- Every number is R191's order-of-magnitude desk anchor (m_s, r_off, v_c, RW authority). The **structural finding** (RWs store not remove; the capture injects ≫-capacity momentum) is anchor-robust; the exact per-cell settle times are not the claim.
- The injected momentum assumes an **off-center** capture (r_off = 5 m). A perfectly centered capture (r_off → 0) injects no net L and reverts to R191's mean-zero corner — but a centered catch of a flexible 40 t bag is not a realistic design assumption; some offset is unavoidable.
- Slosh is modeled as a single first-mode LSMD particle (R191's f_s = 0.5). Higher modes and the full membrane FEM are out of scope; the momentum argument is mode-count-independent (total injected L is a rigid-body property of the capture).
- Reaction-wheel momentum read from `Js·Ω` per wheel; saturation at the 100 N·m·s wheel spec.

## Cross-learning

- **To R191 (`R_bag_dynamics_envelope`):** H1 (contact tractable) and H3 (mass-ratio dominance) stand; **H4 is sharpened** — the viable corner exists only for mean-zero slosh on a heavy host, and the berth *capture* (not the steady slosh) is the binding case, gated by momentum not torque. Corrections live forward; R191's frozen STUDY is not retro-edited.
- **To REQUIREMENTS §7.5 demonstrator objective #4 (LEO handoff/berth rehearsal):** the objective should measure **injected angular momentum and RCS momentum-dump performance at the berth**, not only T_s/ζ — the sim shows momentum management is the design driver.
- **To design-axes 15 (reliability) / 20 (reactor lifetime):** the mothership berth is confirmed as a momentum-management-critical operation; the R189 mothership single-point-of-failure threat is grounded in this (a saturated-wheel tumble at berth is a plausible loss mode).
- **Named follow-on (not run):** a capture-geometry optimization (minimize r_off, pre-berth momentum budgeting, RCS sizing for the 5000 N·m·s dump) — **R-berth-momentum-management** — is the next step if the demonstrator concept advances.
