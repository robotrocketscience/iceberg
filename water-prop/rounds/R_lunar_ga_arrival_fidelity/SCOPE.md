# R-lunar-ga-arrival-fidelity — does R12's inbound lunar-GA braking survive the v∞-conservation invariant?

**Status:** SCOPE pre-registered 2026-07-22, before `run.py` was written or executed. `scope_bounds.py` (committed with this SCOPE) computes only the R12-reproduction baseline and the analytic v∞-globe bound; the honest vectorial per-flyby optimizer and the flyby-count sweep live in `run.py` and were not run before pre-registration.
**Worker:** worktree-115637 session. Project-owner-directed: "run r&d rounds, question your assumptions and test your hypotheses."
**Predecessor under test:** `R12_lunar_GA_both_legs` (`water-prop/rounds/R12_lunar_GA_both_legs`), whose inbound N-flyby lunar tour sheds 5.83 km/s of a 10.30 km/s Earth arrival in 10 flybys and feeds the **axis-10 strict L0-05 closure** (titan-3 `R-chunk-size-pareto` `1997a51`: 4 strict-15yr cells "under … R12 lunar-gravity-assist Earth-arrival").
**Load-bearing claim challenged:** the 4 strict-closing cells on `design-axes/10-round-trip-ceiling` depend on R12's inbound tour residual (~4.47 km/s after 10 flybys). If R12 over-credits the lunar tour, those cells vanish.

## The specific assumption under test

R12's `single_flyby_braking` (`src/waterprop/trajectory/lunar_flyby.py:77-135`) does two things this round argues are wrong:

1. **It violates v∞-conservation.** At each flyby it recomputes the Moon-relative speed `v_inf_moon = v_sc_earth(v∞) + v_M` from the *reduced* Earth-frame v∞ (line 116, `v_sc_earth_at_lunar_distance` treats the craft as freshly arriving from infinity). But a patched-conic flyby is elastic in the Moon frame: it **rotates** the v∞-vector and **conserves its magnitude** U_m (the "v∞-globe" invariant, Tisserand mechanics). R12 lets U_m shrink as v∞ shrinks, which keeps δ_max and per-flyby braking growing without bound.
2. **It assumes perfect alignment.** It subtracts the full Moon-frame velocity-change magnitude `2·U_m·sin(δ/2)` directly from the Earth-frame v∞ (line 122-133), i.e. it assumes that whole vector is anti-parallel to the spacecraft's Earth-frame velocity. For small δ the Δv is ≈ perpendicular to v∞_moon (hence nearly perpendicular to v_sc), so only a small component actually reduces Earth-frame speed. Inclination is hard-set to 0.

The honest model rotates the v∞_moon **vector** (magnitude conserved) by at most δ_max and minimizes the resulting Earth-frame speed over approach geometry and rotation.

## The hard bound this implies

With U_m conserved, the reachable Earth-frame speeds over all rotations of v∞_moon are `[|U_m − v_M|, U_m + v_M]`. The minimum Earth-frame speed a lunar tour can reach is therefore `|U_m − v_M|`, minimized over arrival geometry at U_m = v_sc − v_M, giving **min Earth-frame speed = v_sc − 2·v_M** and hence a **maximum total v∞ shed ≈ v_sc − 2v_M mapped back through the energy relation ≈ 2.07 km/s from a 10.30 km/s arrival — independent of flyby count and (in 3-D) of inclination.** Reaching it requires rotating v∞_moon a cumulative ~180° at ≤ δ_max ≈ 3.4°/flyby, i.e. ~50+ flybys, each needing a phasing return (~1 lunar synodic month).

## Boundary

- **IN:** honest vectorial single-flyby optimizer (rotate v∞_moon by ≤ δ_max, minimize Earth-frame speed over approach geometry + rotation direction, 2-D coplanar and full 3-D with relative inclination φ); the analytic v∞-globe bound; flyby-count to reach the bound; instrumentation of R12's model to exhibit the U_m-conservation violation; propagation of the honest residual v∞ and honest phasing time through R12's **own** delivery `cell()` model (apples-to-apples) to test axis-10 strict closure; cross-validation of δ_max against `~/projects/trajectory-bot` (`scripts/flyby_leverage.delta_max` / `inclination_flyby`).
- **OUT:** full CR3BP numerical integration of the tour (a Tier-2 fidelity check named as a deferred follow-on with retest spec — patched-conic-vs-CR3BP per-flyby Δv agreement); the **outbound** boost tour (R12 owns it; only the inbound braking tour feeds axis-10 strict closure); resonance/DSM-augmented tours (a lunar-GA + deep-space-maneuver variant — flagged, out of scope, does not change the U_m invariant); re-deriving the 10.30 km/s arrival anchor (verified this round as the clean Saturn→Earth Hohmann arrival excess: v_perihelion 40.08 − v_Earth 29.78 = 10.30 km/s).

## Pre-registered hypotheses (numeric, falsifiable, written before run.py)

**H-B1 [S] — honest first-flyby braking ≪ R12.** At the 10.30 km/s arrival, the honest optimizer's max single-flyby Earth-frame braking is **≤ 0.20 km/s**, at least 2× below R12's 0.458 km/s, because braking ≈ δ_max·v_M·sin(geom) with δ_max ≈ 0.04 rad. **Falsified** if honest first-flyby braking > 0.25 km/s (R12 not badly optimistic at high v∞) or < 0.01 km/s (honest model under-credits).

**H-B2 [S] — hard v∞-globe bound: max total shed ≈ 2 km/s regardless of N.** The honest tour sheds **≤ 2.3 km/s total** from the 10.30 km/s arrival at *any* flyby count (predicted 2.0–2.1). **Falsified** if the honest tour sheds > 2.5 km/s (invariant wrong) — this is the decisive test versus R12's 5.83 km/s.

**H-B3 [S] — flyby-count blowup.** To shed the bound's ~2 km/s the honest model needs **≥ 40 flybys** (predicted ~50–78), versus R12's implied ~4 flybys for the same 2 km/s. **Falsified** if the honest model reaches within 0.1 km/s of the bound in ≤ 25 flybys.

**H-B4 [W] — inclination is second-order for the total (asymptotic) shed.** In full 3-D the flyby can rotate v∞_moon in any direction, so anti-alignment with v_M is reachable regardless of φ; the max total shed at realistic φ ∈ {5,10,20}° is **within 5 %** of the coplanar bound. Inclination raises the *per-flyby count*, not the ceiling. **Falsified** if φ=20° reduces the max total shed by > 15 % (inclination, not the U_m violation, is the dominant R12 error).

**H-B5 [S] — axis-10 strict L0-05 closure does NOT survive.** Feeding the honest residual v∞ (~8.2 km/s, vs R12's 4.47) and honest phasing (≥ 3 yr for ≥ 40 flybys, vs R12's 0.7 yr) into R12's own `cell()` delivery model, the strict-15yr closure titan-3 credited to R12 collapses: **0 cells close the strict 15 yr ceiling at ≥ 30 % delivery.** **Falsified** if ≥ 1 cell still closes strict-15yr at ≥ 30 % delivery under the honest tour.

**H-B6 [S] — root cause is U_m-conservation violation.** Instrumenting R12's model over its 10-flyby tour, the Moon-relative speed U_m it implicitly uses **falls monotonically** (from ~11.4 to a much lower value) instead of staying constant, and that decay is what inflates its late-flyby per-Δv. **Falsified** if R12's implied U_m stays within ±5 % of its first-flyby value across the tour (then the optimism is alignment-only, not conservation).

**Honest expected reading (pre-registered):** H-B1/2/3/5/6 hold; R12's inbound lunar tour is falsified as an efficient braking mechanism — a lunar tour sheds at most ~2 km/s of a 10.30 km/s Earth arrival over ~50+ flybys/years of phasing, not 5.83 km/s in 10 flybys — and the **axis-10 strict L0-05 closure that depended on it is removed** (moving those cells to waiver-only, or to a genuinely different inbound mechanism: aerocapture, which was the conops baseline R12 was trying to replace, or a Jupiter GA). H-B4 holds (inclination second-order). This is a scope/physics falsification with a clean root cause (lesson 19), not a bug in R12's downstream delivery model — that model is reused unchanged.

## Method

Deterministic, pure-numpy (no JAX needed). `run.py`:

1. **Honest single-flyby optimizer** `honest_flyby(v_inf_E_in, phi_deg)`: build v_sc (Earth frame) at lunar distance; sweep approach geometry (angle of v_sc relative to v_M, and out-of-plane by φ); form v∞_moon = v_sc − v_M (vector, magnitude U_m); δ_max = 2·arcsin(1/(1 + r_p·U_m²/μ_moon)); over rotations of v∞_moon by ≤ δ_max about the optimal axis, minimize |v_M + v∞_moon_out| → v∞_E_out. Return max braking and the U_m used.
2. **Honest N-flyby tour** `honest_tour(v_inf0, N, phi)`: conserve U_m across flybys (rotate the *same* v∞_moon vector incrementally by ≤ δ_max/flyby toward anti-v_M); track cumulative rotation, v∞_E, and stop at the |U_m − v_M| floor. Sweep N up to 120; sweep φ ∈ {0,5,10,20}°.
3. **Analytic bound** `vinf_globe_bound(v_inf0)`: v_sc − 2v_M → v∞_floor; max shed.
4. **R12 instrumentation:** re-run R12's `n_flyby_tour(10.30, N, "braking")` and record the implied U_m = v_sc(v∞_in)+v_M at each flyby to exhibit the decay (H-B6).
5. **δ_max cross-check:** compare this round's δ_max(U_m) against trajectory-bot's closed form (import if reachable; else assert against the identical analytic 2·arcsin(1/(1+r_p V²/μ)) — same formula, recorded).
6. **Axis-10 closure:** import/replicate R12's `cell()` and feed (honest residual v∞, honest phasing) across R12's power×specific-power×flyby grid; count strict-15yr closures at ≥30 % delivery. Compare to R12's strict/waiver counts.

**Anchors:** μ_Moon=4902.800066, R_Moon=1737.4, v_M=1.0220 km/s, r_lunar_orbit=384400 km, μ_Earth=398600.4418 (all matching `lunar_flyby.py`); peri altitude 100 km (R12 default); arrival v∞=10.30 km/s (R12 `V_INF_INBOUND_KM_S`, verified Hohmann arrival excess). Delivery model constants inherited verbatim from R12 `cell()` (chunk 14 t, dry 5 t, Isp 2000 s, η 0.65, duty 0.5).
