# R-berth-momentum-management — the momentum-management architecture trade at berth

**Status:** SCOPE pre-registered 2026-07-21 (latest+25), before `run.py` was written or executed.
**Worker:** worktree-115637 session. Project-owner-directed follow-on to the `bag_dynamics_6dof` sim; scope reframed after the project owner flagged (a) that water-fed RCS momentum management is prior art and (b) that gravity-gradient torque could desaturate the wheels using the boulder's inertia.
**Predecessors:** `bag_dynamics_6dof` sim (`7a716f3`) — berth capture injects ~5000 N.m.s the 4 small RWs cannot buffer; thruster firing at the bag interface is a plume hazard. `R_chunk_despin_budget` (`2f781d7`/STUDY) — water cold-gas RCS dumps up to 15,000 N.m.s for <125 kg. `vehicle/SATURN-SHIP-SPEC.md` — 4×10 kg reaction wheels, 12× water cold-gas RCS + 50 kg reserve.

## Non-redundancy statement (why this is not just a deeper dive on water RCS)

`R_chunk_despin_budget` already settled that water thrusters can dump captured angular momentum cheaply (its 1-rpm stress tail dumps 15,000 N.m.s for <125 kg cold-gas / <15 kg on the MET). **This round does NOT re-price thruster propellant.** It tests what the sim + the project owner's gravity-gradient insight opened and nothing prior touched:

1. The berth *capture transient* injects ~5000 N.m.s that the current 4-RW cluster (~100–150 N.m.s) **cannot buffer inside the berth window** — wheels saturate and tumble (sim).
2. Firing thrusters at the flexible-bag interface at every one of N berths is a **plume hazard on the critical path** (sim caveat) — so "just use the cheap thrusters" carries a non-propellant cost.
3. The boulder's enormous inertia asymmetry (ΔI ≈ m·r_off² ≈ 1×10⁶ kg·m²) makes **gravity-gradient torque a usable desaturation actuator** (~0.046 N·m at ring distance) — **unstudied anywhere in the campaign** (the only prior "gravity gradient" mentions are aerobraking perturbations).

## Question

At the mothership berth, the captured-bag momentum injection must be managed within the berth window without saturating attitude control. Three architectural legs are available; which is preferred, and under what conditions?

- **Leg A — thruster dump:** cheap propellant (despin-confirmed), but plume at the bag interface, once per berth.
- **Leg B — gravity-gradient desaturation:** propellant- and plume-free, but needs a buffer to *hold* one berth injection while GG bleeds it off over the coast, and a berth-cadence floor set by the GG clear-time.
- **Leg C — capture-geometry control:** shrink r_off·v_c so the injected L stays inside RW capacity — no dump, no plume, no extra hardware; needs a controllably slow, close capture.

## Boundary

- **IN:** GG torque and secular desaturation rate at B-ring distance with the boulder-dominated inertia; buffer-hardware mass (RW/CMG) to hold one berth injection; berth-cadence floor GG can keep up with; capture-geometry RW-only corner; thruster-dump baseline (propellant scaled from despin, plus the plume/critical-path count). Deterministic desk analysis; the sim's own capture-rate diagnostic is the empirical RW-only threshold anchor.
- **OUT:** re-deriving thruster-dump propellant from scratch (despin owns it); the 6-DOF coupled attitude sim itself (already run — `bag_dynamics_6dof`); chunk-spin de-spin (that is `R_chunk_despin_budget`'s axis; this is the *capture-transient* injection, a different L); full CMG gimbal control law; plume-impingement CFD on the bag (named follow-on if a leg is chosen).

## Pre-registered hypotheses (numeric, falsifiable, written before the run)

**H1 [S] — GG torque with the boulder is a usable desaturation actuator; one berth injection clears in days.** τ_gg,max = (3μ/2R³)·ΔI with ΔI = m_bag·r_off² ≈ 1e6 kg·m². **SCOPE:** τ_gg ∈ [0.02, 0.08] N·m; secular shed ∈ [200, 900] N·m·s/orbit (η_gg ∈ [0.15, 0.5], ring orbit ≈ 9.9 h); one 5000 N·m·s berth clears in **[2.5, 10] days**. **Falsified** if τ_gg < 0.005 N·m (GG negligible) or clear-time > 30 days (impractically slow vs residence).

**H2 [S] — Buffering one berth injection to enable leg B costs CMG-class hardware (~300–600 kg) ≫ thruster-dump propellant (~42 kg): GG-desat buys plume-avoidance, not mass.** The 4×10 kg RW cluster (~100–150 N·m·s) is 33–50× short of one 5000 N·m·s injection; holding it needs a CMG (ISS M2000: 4760 N·m·s @ 272 kg → 0.057 kg/N·m·s). **SCOPE:** buffer hardware ∈ [285, 600] kg; thruster-dump propellant ∈ [3, 45] kg (cold-gas to MET, despin-scaled). GG-desat's cost is **dry mass + a cadence floor, not propellant**. **Falsified** if buffer hardware < thruster propellant (GG-desat strictly dominates on mass) or the 4-RW cluster (≤200 N·m·s) already absorbs one berth injection.

**H3 [S] — Capture-geometry control (leg C) can eliminate the dump entirely.** RW-only (no-dump) requires v_c·r_off ≤ H_rw/m_s ∈ [0.005, 0.0075] m²/s. **SCOPE:** achievable at r_off ≤ 2 m with v_c a few mm/s (r_off=1 m → v_c ≤ 5–7.5 mm/s; r_off=2 m → ≤ 2.5–3.75 mm/s); consistent with the sim diagnostic (L=100 held at 4.5°, L=500 tumbled → threshold ≈ cluster capacity). **Falsified** if the required v_c at every realistic r_off ≥ 1 m falls below 1 mm/s (geometry control alone cannot reach the RW-only corner).

**H4 [W] — Synthesis: leg B's only advantage is plume-avoidance; it costs dry mass + a cadence floor; leg C dominates if achievable.** **SCOPE:** rank C < B < A on plume/mass **if** leg-C capture control is operationally reachable; else the live decision is leg A (plume hazard, ~42 kg) vs leg B (no plume, +300–600 kg CMG + berth-cadence floor ≥ clear-time). **Falsified** if thruster propellant > 1% of wet mass (leg A self-defeating on its own terms) or GG clear-time < 1 day (cadence never binding → leg B is a free win, no trade).

If H1–H3 hold and H4 resolves as written, the honest reading is a **design finding, not a wonder:** GG-desat is real and the boulder makes it unusually strong, but it is *not free* (CMG mass + a days-scale berth-cadence floor); the cleanest architecture is leg C (capture-geometry control) where reachable, with leg A (cheap thrusters, accept plume management) as the robust fallback and leg B reserved for the case where plume at the bag is a hard showstopper.

## Method

Closed-form, deterministic. All in `run.py`:

- **GG:** τ_gg = (3μ_S/2R³)·ΔI, ΔI = m_bag·r_off²; T_orb = 2π√(R³/μ_S); shed/orbit = η_gg·τ_gg·T_orb; clear-time = L/(shed/orbit). Sweep r_off ∈ {1,2,5,10} m, η_gg ∈ {0.15,0.3,0.5}.
- **Buffer mass:** RW cluster vs CMG (0.057 kg/N·m·s from ISS M2000); deficit ratio L/H_rw; CMG mass to hold L (×1 and ×2 redundancy).
- **Thruster baseline:** propellant = 125 kg·(L/15000) cold-gas, 15 kg·(L/15000) MET (despin-scaled); plume-firing count = N berths.
- **Geometry corner:** v_c·r_off ≤ H_rw/m_s; map v_c(r_off) at cluster bounds; cross-check vs sim diagnostic (L=100 held, L=500 tumbled).
- **Injection band:** L ∈ {5000 (sim 20 t half), 10000 (full 40 t bag)}.
- **Synthesis table:** per leg — propellant, plume, extra dry mass, cadence floor — with the falsification checks.

**Anchors (all reproduced, not re-derived):** μ_S=3.793e16, R_RING=1.07e8 (R179); bag 40 t, f_s=0.5, r_off 5 m, v_c 0.05 m/s (sim); 4×10 kg RW + water cold-gas RCS (vehicle spec); despin 125 kg/15000 N·m·s (R_chunk_despin_budget). ISS CMG 4760 N·m·s @ 272 kg (Honeywell M2000, ISS heritage — cited in STUDY).
