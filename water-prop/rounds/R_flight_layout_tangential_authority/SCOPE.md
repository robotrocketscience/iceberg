# R-flight-layout-tangential-authority — does a real corner-mounted RCS keep plume-safe in-plane couple authority?

**Status:** SCOPE pre-registered 2026-07-22, before `run.py`. `scope_bounds.py` reproduces only the idealized-ring baseline (berth-dump) and states the corner-layout predictions.
**Worker:** worktree-115637 session. Project-owner-directed follow-on.
**Predecessor:** `R-berth-dump-axis-geometry` (`107bf5b`, 4/4 HELD) closed the berth momentum-management thread with leg A (tangential water-RCS dump) using an **idealized symmetric ring** (thrusters at cardinal points (±A,0,±H) / (0,±A,±H), purely ±x/±y thrust directions). The spec (`water-prop/vehicle/SATURN-SHIP-SPEC.md` §7) and matrix latest+25 deliverable (f) carry the **one named residual**: "the flight thruster layout has tangential authority about both in-plane axes — a generic property of any 3-axis-couple RCS; the layout drawing must confirm it." The real vehicle has "12 × water-vapor cold-gas thrusters **at corners of the spacecraft envelope**" — not a cardinal ring.

## The assumption under test

That plume-safe tangential couple authority about **both** in-plane axes is "a generic property of any 3-axis-couple RCS." This round argues it is **generic only for a ±z-distributed layout**, and can fail for a plausible real placement (RCS clustered on the aft deck near the propulsion, no top/bottom separation) — so it is a real layout-drawing constraint, not automatic.

## Boundary

- **IN:** a realistic box-corner 12-thruster layout (8 corner-tangential + 2 prograde +z + 2 retro −z; bus half-dims 1.5×1.5×2.0 m; F=5 N/thruster, Isp 70 s cold-gas — all matching the berth rounds); the 6×12 wrench map; explicit construction + verification of pure couples (net force ≈ 0, pure torque) about x, y, z from non-negative thruster firings; plume-safety of the in-plane (x,y) couples via the berth-dump `bag_plume` model reused verbatim; torque authority + dump time + propellant for the ~5000 N·m·s berth injection; single-thruster-failure robustness; a pessimistic **aft-clustered** variant (all thrusters at −z) to bound the genericity claim.
- **OUT:** the mass-properties / inertia tensor (spec §1 defers it; the couple authority is inertia-independent — it is a wrench-map property); the berth momentum magnitude derivation (R-berth-momentum-management owns the 5000 N·m·s); slosh dynamics (bag_dynamics_6dof owns it); the plume threshold model itself (reused from the closed berth-dump round, not re-litigated).

## Pre-registered hypotheses (numeric, falsifiable, before run.py)

**H-A1 [S] — distributed corner layout gives pure 3-axis couples.** The box-corner layout yields a pure couple (net force ≤ 2 % of one thruster's force, i.e. ≤ 0.1 N) about each of x, y, z. **Falsified** if any axis lacks a constructible pure couple.

**H-A2 [S] — plume-safe in-plane couples about BOTH axes.** The x-couple and y-couple built from corner-tangential thrusters keep the bag in backflow: max bag-plume torque < 2.5 N·m (the berth-dump re-perturbation threshold) for both. **Falsified** if either in-plane axis's plume-safe couple exceeds 2.5 N·m (would re-open leg A on the real layout).

**H-A3 [W] — torque authority and dump time are benign.** Max in-plane pure-couple torque ≥ 10 N·m (F=5 N, arm ≥ 2 m, ≥2 thrusters); dump time for 5000 N·m·s ≤ 1800 s; propellant ≈ 42 kg (consistent with R-berth-momentum-management's despin-scaled 125 kg / 15000 N·m·s). **Falsified** if dump time > 3600 s or torque < 5 N·m.

**H-A4 [S] — single-thruster-failure robustness.** With any one thruster failed, a plume-safe in-plane couple about **both** x and y still exists (possibly at reduced torque). **Falsified** if any single-thruster failure removes plume-safe couple authority about an in-plane axis. *(Honest flag: this is the hypothesis most at risk — a corner layout has fewer redundant tangential thrusters per axis than the idealized ring.)*

**H-A5 [S] — the genericity is conditional on ±z distribution (design constraint).** An aft-clustered layout (all 12 thrusters within one deck, |Δz| ≈ 0) does **NOT** provide plume-safe in-plane couples — an in-plane couple then requires ±z-firing (axial) thrusters, whose +z members fire into the bag. **Falsified** if the aft-clustered layout yields a plume-safe in-plane couple about either axis.

**Honest expected reading:** H-A1/A2/A3 hold (the residual clears — the real corner layout retains plume-safe in-plane authority, confirming the berth-thread close on the flight vehicle). H-A5 holds and converts the vague "generic property" into a **concrete layout-drawing constraint: the 12 RCS thrusters must be ±z-distributed (top and bottom deck), not aft-clustered.** H-A4 is the genuine unknown — if it fails, the finding is that the flight layout needs ≥ N tangential thrusters per in-plane axis for single-fault tolerance, a sizing requirement for the spec.

## Method

Deterministic pure-numpy 3-D geometry + linear algebra. Wrench map W (6×12) columns = [thrust_dir; r×thrust_dir] per thruster. Construct candidate couples as non-negative thruster subsets; verify |Σ F| ≤ 0.1 N and torque is along the target axis. Plume torque via berth-dump `bag_plume` (bag at z_bag = az + boom + R_bag, boom = 3 m). Failure sweep: drop each thruster, re-construct. Aft-clustered variant: same 12 thrusters relocated to z ∈ [−az, −az+0.3] m. Anchors identical to the berth rounds (F=5 N, Isp 70 s, L_berth 5000 N·m·s, TAU_TH 2.5 N·m, plume KAPPA/BETA/NEXP/THETA_C).
