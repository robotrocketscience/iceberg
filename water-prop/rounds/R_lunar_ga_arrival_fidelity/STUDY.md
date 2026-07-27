# R-lunar-ga-arrival-fidelity — R12's inbound lunar-GA braking violates v∞-conservation

**Status:** run + STUDY complete 2026-07-22. 6/6 pre-registered hypotheses HELD. Result JSON `results/lunar_ga_fidelity.json`; figure `results/lunar_ga_fidelity.png`.
**Predecessor under test:** `R12_lunar_GA_both_legs`. **Load-bearing target:** matrix finding **A15** ("lunar gravity-assist tour 5.83 km/s plausible-provisional"), axis-04 anchor **"4.2 km/s after R12 10-flyby lunar-GA tour"**, titan-3 R-chunk-size-pareto closure-cell condition **(c)** ("R12 lunar-gravity-assist Earth-arrival").

## Hypothesis (pre-registered before run.py; see SCOPE.md)

A lunar gravity assist is elastic in the Moon frame — it **rotates** the Moon-relative velocity vector at **fixed magnitude U_m** (the "v∞-globe" invariant). R12's `single_flyby_braking` instead recomputes `U_m = v_sc(v∞) + v_M` from the *reduced* Earth-frame v∞ at every flyby, letting U_m shrink so δ_max and per-flyby braking grow without bound. With U_m conserved, the minimum reachable Earth-frame speed is `|U_m − v_M|`, so the **maximum total v∞ a lunar tour can shed from a 10.30 km/s Earth arrival is ≈ v_sc − 2·v_M ≈ 2.07 km/s — at any flyby count, in 3-D independent of inclination.** R12 claims 5.83 km/s in 10 flybys; that is physically impossible if the invariant holds.

## Test

Pure-numpy, deterministic (`run.py`). Honest vectorial single-flyby optimizer (rotate the v∞_moon **vector**, magnitude conserved, by ≤ δ_max toward −v_M, minimize outgoing Earth-frame speed over approach geometry, 2-D and 3-D with relative inclination φ); analytic v∞-globe bound; honest N-flyby tour; instrumentation of R12's own model to exhibit its implied-U_m decay; δ_max cross-checked against the trajectory-bot closed form; the honest residual + honest phasing fed through R12's **own** delivery `cell()` (reused verbatim) to test the axis-10 strict closure. Arrival v∞ = 10.30 km/s (R12's value; verified as the clean Saturn→Earth Hohmann arrival excess, 40.08 − 29.78).

## Result

| Sub-claim | Predicted | Measured | Held? |
|---|---|---|---|
| H-B1 honest first-flyby braking | ≤ 0.20 km/s (≥2× below R12 0.458) | **0.050 km/s** (R12 is **9.1×** high) | ✅ |
| H-B2 max total shed (v∞-globe bound) | ≤ 2.3 km/s at any N (pred 2.07) | **2.069 km/s** = analytic bound; vs R12 claim 5.83 | ✅ |
| H-B3 flyby count to bound | ≥ 40 (pred ~53) | **51 flybys** (~4.1 yr phasing) | ✅ |
| H-B4 inclination second-order for ceiling | within 5% of φ=0 | **0.0000** frac change over φ∈{5,10,20}° | ✅ |
| H-B5 axis-10 strict closure survives? | 0 strict cells at ≥30% delivery | **0 cells** (vs 8 in R12-input reproduction); best honest RT **17.3 yr** | ✅ |
| H-B6 root cause = U_m-conservation violation | R12 implied U_m falls >5% | R12 U_m **11.42 → 3.10 (−73%)** across its tour | ✅ |

δ_max cross-check: this round's 3.3749° == closed-form 2·arcsin(1/(1+r_p·U²/μ)) 3.3749° (the identical form used by trajectory-bot `flyby_leverage.delta_max` / `inclination_flyby`).

## Reading

**R12's inbound lunar tour is falsified as an efficient braking mechanism, with a clean, textbook root cause.** A lunar flyby conserves the Moon-relative speed U_m and only rotates its direction; R12 lets U_m decay 73% across its tour (11.42 → 3.10 km/s), and that decay — not real physics — is what makes its late flybys appear to shed ~1 km/s each. Under conservation, the entire tour is bounded: from a 10.30 km/s Earth arrival the deepest reachable Earth-frame v∞ is 8.23 km/s (v_sc − 2·v_M), a **total shed of 2.07 km/s regardless of flyby count**, and reaching even that requires rotating the v∞-vector a cumulative 180° at ≤ 3.37°/flyby → **51 flybys ≈ 4.1 years of Earth-orbit phasing**. R12 credited 5.83 km/s in 10 flybys — **2.8× too much shed in 5× too few flybys.** Inclination is exactly second-order (the 3-D flyby can always rotate toward −v_M given enough flybys), confirming the error is the U_m violation, not the hard-set-to-zero inclination penalty R12's own Revisit worried about.

**What this does and does not reach (scope, per methodology lesson 19).**

- **Falsifies** matrix finding A15 ("lunar-GA tour 5.83 km/s plausible-provisional") → **capped at ~2.07 km/s.**
- **Falsifies** the axis-04 Earth-arrival anchor "**4.2 km/s after R12 10-flyby lunar-GA tour**." The honest post-lunar-GA capture burn is ~**6.0 km/s** (from residual 8.23 km/s), bought only at ~4 yr of phasing — barely better than the **7.3 km/s direct** capture and not worth the phasing. Direct-propulsive 7.3 km/s becomes the operative Earth-arrival anchor; lunar-GA is not a meaningful lever on it.
- **Retires** the titan-3 latest+13 closure-cell **condition (c)** (the 4 strict + 30 waiver cells at 40-80 t chunk / 30 kWe were explicitly conditioned on "R12 lunar-GA Earth-arrival … residual 4.47 km/s"; the honest residual is 8.23 km/s and the tour adds ~4 yr, pushing best round-trip to 17.3 yr, past the strict 15 yr ceiling → **0 strict cells** under the honest tour).
- **Does NOT collapse the current dominant closing path.** The latest+21 assumption-audit best-architecture sweep already found lunar-GA "not in the dominant closing path"; the dominant pattern is "single-launch + autonomous-assembly + low-thrust spiral + chunk-fed-spiral departure + **direct propulsive or hybrid aerocapture return**." This round leaves direct-propulsive capture untouched. So the round **removes an optimistic escape hatch** (a cheap lunar inbound-braking lever that could be re-invoked) rather than felling the state-of-record.
- **Does NOT touch** R12's delivery `cell()` model (reused verbatim; it reproduces 8 strict cells on R12's own residual input — the change is entirely in the tour physics feeding it), nor the 10.30 km/s arrival anchor (verified), nor the **outbound** boost tour (same U_m-violation applies but outbound is not load-bearing for any closure).

## Revisit

Prediction held cleanly and the magnitude matched the analytic bound to 3 decimals (2.069 measured vs 2.069 predicted) — the v∞-globe invariant is not a modeling choice, it is conservation of energy in the Moon frame, so there was little room for the number to land elsewhere once the invariant was identified. The one genuinely uncertain pre-registration was H-B5's downstream consequence (would the closure survive on delivery even with the higher residual?); it failed on the **time** axis (phasing), not the delivery axis (residual 8.23 km/s still delivers 51% per-cell), which is the honest and slightly non-obvious mechanism — the lunar tour's cost is its 4-year phasing tail, not primarily its weak braking. Consistent with methodology lesson 1 (the *prediction* was pessimistic on R12 and held) and lesson 7 (computed the bound under the conserved-U_m anchor first).

**Deferred (retest spec):** a **CR3BP numerical spot-check** — propagate one representative high-v∞ lunar encounter through trajectory-bot's Earth-Moon CR3BP (`scripts/cr3bp_sim.py`) and confirm the patched-conic per-flyby Δv is within ±20% of the three-body value. Patched-conic could in principle understate braking near the Moon's Hill sphere; the v∞-globe bound, however, is frame-independent conservation and would survive a CR3BP check (CR3BP conserves the Jacobi constant, the rotating-frame analogue). Named, not run this round. Also out of scope: lunar-GA **+ deep-space-maneuver** tours, which can change U_m between flybys via a heliocentric DSM — but a DSM is propulsive Δv, so crediting it is double-counting against the propulsive budget the tour was meant to save.

## Cross-learning

- **New methodology-lesson candidate (number to be assigned by orchestrator): a sequential-operation model must conserve the operation's invariant.** R12 modeled N flybys by re-initializing each flyby from the *current scalar state* (Earth-frame v∞) instead of carrying the *conserved vector invariant* (U_m). Re-deriving the per-step gain from the reduced scalar broke conservation and produced an unbounded-looking sequence. When modeling a repeated physical operation, identify the conserved quantity of the single operation and carry it across the sequence; do not recompute the operation's leverage from the post-operation reduced state. This is the sequential-operation companion to lesson 18 (pre-register the conditioning structure) and lesson 6 (shared-physics input conventions need assertions) — `single_flyby_braking` had no assertion that U_m is conserved call-to-call, and no reader cross-checked it across three rounds (R9, R9b, R12).
- **Backward to R12:** R12's aggregate "14 yr / 70% via 10-flyby lunar tour" is falsified; its outbound TSI-savings table shares the same U_m-violation and is over-credited by the same mechanism (not load-bearing, so not re-run). R12's delivery `cell()` model is sound and reused here.
- **Forward to axis 04 / axis 02 / axis 10 / matrix A15:** integration this pass folds the falsification (see integration commit). Net campaign effect: the inbound leg has **no cheap velocity-reduction lever** — aerocapture is closed (axis 11, 0/1920), lunar-GA sheds ≤2 km/s at a 4-yr phasing cost (this round), so direct-propulsive capture (~7.3 km/s) is the operative inbound mechanism, and the honest inbound Δv budget is correspondingly heavier. This *reinforces* the three-engineering-bets reading (locked finding 5): none of the bets is inbound-braking, and this round confirms there is no fourth free lunch there.
- **Cross-application check (trajectory-bot):** trajectory-bot's flyby primitives (`flyby_leverage.delta_max`, `inclination_flyby`) use the identical turn-angle law and would have surfaced this immediately — the v∞-globe / Tisserand invariant is the organizing principle of that whole toolkit. The ICEBERG `lunar_flyby.py` module predates the trajectory-bot cross-application and reinvented the flyby without the invariant. Recommend future flyby work import trajectory-bot rather than the local module.
