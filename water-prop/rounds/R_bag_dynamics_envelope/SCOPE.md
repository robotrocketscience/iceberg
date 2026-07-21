# R-bag-dynamics-envelope — a lumped-parameter box around the campaign's single largest unmodeled physics

**Status:** SCOPE pre-registered 2026-07-21, before `run.py`. Bounds from `scope_bounds.py`, committed alongside.
**Worker:** worktree-115637 session. R185 named it: *"bag dynamics of a non-rigid 40 t load during berthing is the single largest unknown and has no precedent anywhere."* R189 found the berth_bag stage drives both the retention floor and the catastrophic mothership tail. This round puts a **lumped-parameter envelope** around the physics. It explicitly **does not resolve coupled stability** — that requires a 6-DOF sim, named as the follow-on with the Basilisk module identified. Honesty posture: every stiffness/damping number is an order-of-magnitude desk anchor; the **envelope shape and the design-corner narrowness are the claim**, not any point value.

## Model (two timescales)

**Contact:** capture arrests the closing rate v_c through a soft-capture stiffness k_c and the participating mass; peak force F = v_c·√(k_c·m), arrest impulse J = m·v_c, contact time τ = π√(m/k_c). **Slosh:** a fraction f_s ≈ 0.5 of the 40 t sloshes as a first-mode spring-mass-damper at period T_s set by the bag's elastic restoring stiffness — in microgravity there is **no gravity restoring**, only membrane tension, so T_s is long and design-dependent (swept 10–300 s). Hub disturbance torque = m_s·x_s·ω_s²·r_off; settling ≈ 4/(ζ·ω_s). The load (40 t) versus the mothership (4 t relay bus … 20 t monolithic) is a **mass ratio ≥ 2 — the slosh mass exceeds a relay bus and equals a monolithic**. Bag dynamics is not a perturbation on the host; it is the dominant body.

## Pre-registered hypotheses (bounds scripted)

**H1 [S] (contact is not the problem).** Peak capture force is **0.1–6.3 kN** across berthing rates 0.01–0.1 m/s × stiffness 10³–10⁵ N/m; soft capture (v_c ≤ 0.05 m/s, k_c ≤ 10⁴ N/m) holds it **≤ 1 kN**, within a purpose-built berthing arm; arrest impulse 0.4–4 kN·s. The contact mechanics are tractable and not the risk driver. Falsified if any soft-capture corner exceeds 10 kN.

**H2 [S] (slosh overlaps the control bandwidth).** First-mode slosh frequency is **0.003–0.1 Hz** (T_s 10–300 s); it **overlaps a large spacecraft's ACS bandwidth (0.01–0.1 Hz) for T_s ≲ 100 s** — most of the plausible range — a control-structure-interaction risk. Only a very floppy bag (T_s ≳ 150 s) drops below. Falsified if no overlap anywhere in the band.

**H3 [S] (mass-ratio dominance defeats wheel control).** Mass ratio **2:1 (monolithic) to 10:1 (relay bus)**; slosh disturbance torque spans **1.8–1579 N·m** — it **exceeds reaction-wheel authority (~5 N·m) for T_s ≲ 180 s and exceeds thruster authority (~50 N·m) for stiff bags (T_s ~10 s, ~1.6 kN·m)**. Attitude cannot be held on wheels during berth; thruster control is forced (with its plume/contamination near the bag). Falsified if mass ratio < 1 or torque ≤ RW authority across the band.

**H4 [W] (a narrow viable corner that prescribes unprecedented bag design — and the sim gate).** A comfortable design point **exists but is narrow**: only **~9 % of the T_s × ζ grid** is both reaction-wheel-controllable and settles inside a 30-min berth window (**~35 %** if thrusters are allowed). That corner **prescribes** a specific, unprecedented 40 t space-bag: moderate membrane compliance (T_s ≈ 100–180 s) *and* ζ ≥ 0.1 damping (active or baffled). Outside it, at least one of {CSI overlap, thruster-exceeding torque, over-window settling} bites. The desk model **locates** the corner but **cannot verify coupled stability inside it** — that is the **Basilisk 6-DOF follow-on** (`linearSpringMassDamper` slosh particles coupled to the ACS in `water-prop/sims/`). This is the one campaign question that cannot be desk-closed, and it **explains R185's low berth_bag stage probability (0.88–0.95) and R189's berth-driven mothership threat from first principles**. Falsified if the viable corner spans > 50 % of the grid, or if coupled stability is resolvable without a sim.

## Sweep (run.py)

Contact-force surface (v_c × k_c); slosh-frequency vs ACS-band overlay (T_s); disturbance-torque vs T_s with RW/thruster authority lines; viable-corner heatmap over T_s × ζ (settle-in-window ∩ controllable). Grids span the pre-script's.

## Deliverables

`scope_bounds.py`, `run.py` (+ `results/bag_dynamics.png`), `results/findings.json`, `STUDY.md` with Revisit; orchestrator notes: bag dynamics enters the risk register as **the one desk-irreducible unknown** — envelope bounded (contact tractable; the problem is the coupled attitude dynamics of a host-dominating sloshing mass), a **narrow prescribed design corner**, and a **named Basilisk 6-DOF sim as the only way to close it**; the LEO handoff-rehearsal gate (R185/R189) gains bag-slosh characterization as an explicit objective; this round grounds R185's berth_bag probability and R189's mothership threat in physics rather than desk anchor.
