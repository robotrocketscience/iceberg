# R-berth-plume-impingement — is RCS plume at the bag interface a showstopper?

**Status:** SCOPE pre-registered 2026-07-21 (latest+25), before `run.py` was written or executed.
**Worker:** worktree-115637 session. Project-owner-directed: the pivot of the momentum-management trade — "does thruster plume at the flexible-bag interface actually damage or re-perturb the bag?"
**Predecessors:** `R-berth-momentum-management` (`b3b579c`) — leg A (thruster dump) is propellant-cheap but its whole cost is "N plume firings at the bag"; the A-vs-B-vs-C ranking hinges on whether that plume is benign. `bag_dynamics_6dof` sim (`7a716f3`) — settling the slosh/attitude at berth takes 2–10 min; a plume that re-excites it defeats the dump. `vehicle/SATURN-SHIP-SPEC.md` — 12× water cold-gas RCS at envelope corners; bag = Vectran laminate + 50 kg aerogel intake, grappled on a boom.

## Why this round decides the trade

`R-berth-momentum-management` ranked the three legs **C < B < A** but flagged that the ranking *inverts* on one unanswered question: if firing the onboard water thrusters to dump the berth momentum (leg A) is harmless to the bag, then leg A is the robust default and the ~300–600 kg CMG (leg B) / precision-capture (leg C) are optional. If the plume damages the Vectran/aerogel or re-excites the just-settled slosh, leg A is disqualified and legs C/B become **mandatory** — the momentum-management cost becomes real. This round answers that pivot.

## Question

Does the water cold-gas RCS plume, fired for a ~5000 N·m·s / ~100 s momentum dump at the berth, (1) mechanically damage the Vectran laminate or aerogel intake, (2) re-perturb the just-settled bag attitude/slosh, or (3) ice-clog the aerogel soft-capture intake over N berths?

## Boundary

- **IN:** far-field plume momentum-flux pressure at the bag standoff (2–10 m); pressure vs Vectran/aerogel structural limits; plume torque on the bag vs the dump torque (re-perturbation); cumulative water-ice deposition on the aerogel intake over N berths; the geometry distinction between the bag sitting in the plume **core** vs **backflow** (θ > 90°), and whether a 12-corner-thruster layout can keep the bag in backflow for the required dump axes.
- **OUT:** full DSMC/CFD plume simulation (this is a parametrized engineering plume model — see bug-catch); the momentum injection itself (`bag_dynamics_6dof` owns it); thruster propellant (`R_chunk_despin_budget` owns it); MET (main-drive) plume (the dump uses cold-gas RCS, not the MET); detailed Vectran laminate FEM.

## Pre-registered hypotheses (numeric, falsifiable, written before the run)

**H1 [S] — Plume pressure is 3–4 orders below structural limits: no fabric/aerogel damage.** Worst-case core pressure (F=10 N, r=2 m, κ=6) vs the conservative aerogel compressive/Vectran membrane limit (~10 kPa). **SCOPE:** worst core pressure < 100 Pa (0.01× the 10 kPa limit); measured margin ~4000× (3.6 orders). **Falsified** if core pressure at minimum standoff ≥ 100 Pa.

**H2 [S] — With the bag in backflow, plume torque ≪ dump torque: it does not re-excite the settled slosh/attitude.** τ_plume = P·A_bag·r_off vs the re-perturbation threshold (5% of the 50 N·m dump = 2.5 N·m). **SCOPE:** at the operating point (backflow, r ≥ 3 m, β = 1e-2) τ_plume < 2.5 N·m (measured ~0.22 N·m). **Falsified** if backflow τ ≥ 2.5 N·m at the operating point, **or if backflow geometry is unachievable** so the bag sits in the plume core (core case gives ~11 N·m ≈ 22% of dump → re-excites; that is the *design constraint*, and its unavoidability would falsify leg A's viability).

**H3 [S] — Cumulative water-ice on the aerogel intake over N berths is grams: no clog.** Deposition = 2·mdot·t_dump·β_m·f_intake·stick·N onto the 50 kg intake. **SCOPE:** cumulative ice < 1% of intake mass (500 g) across the grid; central ~4 g (0.009%), stress corner ~290 g (0.58%). **Falsified** if deposition ≥ 500 g, **or** if the intake sits in the plume core (deposition ×κ/β ≈ 100–1000× → clog).

**H4 [W] — Synthesis: with a backflow-keeping thruster placement (feasible with 12 corner thrusters for most dump axes), plume is NOT a showstopper → leg A robust, CMG/GG optional.** **SCOPE:** plume benign at the operating point AND no worst-case dump axis forces > 50% core illumination of the bag → leg A survives with a thruster-*placement* constraint; the CMG (leg B) and precision-capture (leg C) become optional risk reduction. **Falsified** if some required dump axis unavoidably puts the bag in the plume core (then leg C/B mandatory and the momentum-management cost is real).

**Honest expected reading:** H1 and H3 hold robustly (pressure and deposition are physically tiny). H2/H4 are the live ones and are **geometry-conditioned**: plume is benign *provided* the momentum-dump thrusters are placed/pointed so the bag is in backflow, which a 12-corner-thruster layout can do for most (not necessarily all) dump axes. So the likely verdict is not "plume is fine, use leg A freely" but **"leg A is viable under a thruster-placement/dump-axis constraint; the residual worst-case-axis risk is what legs C/B exist to retire"** — which keeps the trade honest rather than collapsing it.

## Method

Closed-form, deterministic, parametrized plume model. All in `run.py`:

- **Plume pressure:** P_iso(r) = F/(2π r²); core P = κ·P_iso (κ ∈ {2,4,6}); backflow P = β·P_iso (β ∈ {2e-3,1e-2,3e-2}). F ∈ {3,5,10} N (from τ_dump 50 N·m / arm 5–15 m), r ∈ {2,3,5,10} m.
- **Mechanical:** compare worst core P to P_damage = 10 kPa (aerogel-limited, conservative).
- **Re-perturbation:** τ_plume = P·A_bag·r_off (A_bag = 50 m², r_off = 5 m) vs 2.5 N·m; core-case uses the illuminated spot A = π(r·tan25°)².
- **Icing:** m_ice = 2·(F/v_e)·t_dump·β_m·f_intake·stick·N; v_e = 687 m/s, β_m ∈ {1e-4,1e-3,1e-2}, f_intake ∈ {0.05,0.1,0.2}, stick = 1, N ∈ {10,30,50}, intake 50 kg.
- **Synthesis:** per-leg decision table conditioned on backflow-achievable vs core-forced.

**Anchors (reproduced, not re-derived):** cold-gas Isp 70 s (spec / despin); τ_dump 50 N·m, t_dump 100 s, injection 5000 N·m·s (sim); 12 corner thrusters, aerogel intake 50 kg (`SATURN-SHIP-SPEC.md`). Structural and plume-shape parameters are conservative engineering bands, flagged as such in the bug-catch.
