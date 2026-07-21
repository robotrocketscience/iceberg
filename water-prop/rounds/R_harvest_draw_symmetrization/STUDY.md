# R-harvest-draw-symmetrization — STUDY

**Round:** R-harvest-draw-symmetrization. SCOPE pre-registered 2026-07-20 before `run.py` existed.
**Worker:** worktree-115637 session. Third round of the spin/attitude arc; attacks R-com-offset-thrust-alignment's one-sided-draw default.

## Hypotheses, tests, results

Computations in `run.py` (closed form, deterministic); numbers in `results/findings.json`; figure `results/walk_strategies.png`.

### H1 — polar port with δ = 0.3 m tolerance — **FALSIFIED**

| metric | predicted | measured | held? |
| --- | --- | --- | --- |
| worst draw-walk at δ = 0.3 m | < 0.25 m | **0.882 m** (25 t chunk) | **FALSIFIED** |

**Reading.** The registered claim assumed the walk amplification uses the *stack* propellant fraction (~0.41). It uses the *cargo* fraction: a 25 t chunk spends 75 percent of itself hauling the 20 t ship home, and walk = f·δ/(1−f) amplifies the port offset by f/(1−f) ≈ 2.9. The tolerance is therefore not the registered absolute 0.3 m; it is chunk-size-dependent: holding the walk under 0.2 m needs the port centered within **6.8 cm at 25 t, 12 cm at 40 t, 20 cm at 80 t, 24 cm at 200 t**. Centimeter-class port alignment is still a bench problem rather than a physics veto — but this is the arc's one genuine inversion: **small chunks, easy everywhere else in the campaign, are the hard case for draw geometry.**

### H2 — no-roll sun ablation exceeds the kill regime at s ≥ 0.6 — **FALSIFIED**

Measured walks at a 60/40 sun split (porous, ≥ 40 t): 0.27–0.33 m — under the registered 0.5 m. At s = 1.0 (fully one-sided, round 169's case) the walks are 1.35–1.65 m as before.

**Reading.** The sun-channel severity is governed by (2s−1), and s is a thermal-design unknown this campaign cannot pin from the desk: a mild bias lands in the manageable-but-not-cheap band (above 0.2 m, below 0.5 m), a strong bias lands in the kill regime. The registered hypothesis overstated the mild case. The architectural consequence is unchanged by which side of 0.5 m the unknown falls on — see H3.

### H3 — 1 rev/day roll symmetrizes the sun channel — **HELD**

Worst residual transverse walk across the full grid (10–100 kWe, s up to 1.0): **0.023 m**, against the 0.05 m bound. The roll retires the sun-split unknown entirely — successive half-revolutions cancel the transverse moment, and the uncancelled residue is one revolution's worth of ablated mass.

### H4 — the roll is gyroscopically free — **FALSIFIED**

| metric | predicted | measured | held? |
| --- | --- | --- | --- |
| worst slew-precession propellant | < 1 kg | **24.6 kg** (200 t, 10 kWe) | **FALSIFIED** |

**Reading.** Precessing the rolling stack's angular momentum through even a generous 3°/day tracking slew is cheap per unit time, but the 10 kWe / 200 t corner burns for ~15 years, and the integral lands at 24.6 kg. The bound-setting error was the burn duration, again taken from the central case rather than the worst corner — the same lesson as R-chunk-despin-budget, imperfectly applied. Absolute reading: 24.6 kg is 0.1 percent of the delivery floor and is an over-bound (the axial center-of-mass motion needs far less than continuous 3°/day tracking).

## Revisit (mandatory)

One held, three falsified — and this round's falsifications are the findings. H1's miss exposed the f/(1−f) amplification and converted a lazy "0.3 m tolerance" into a real, chunk-size-dependent alignment requirement. H2's miss demoted the sun channel from "certain kill" to "unknown severity" — which strengthens, not weakens, the case for the roll, because H3 shows the roll deletes the unknown for the price of H4's ~25 kg bound. On bound-setting: two of three misses came from evaluating a *derived* quantity (draw fraction, burn time) at the central case even while sweeping the primitive grid corners. The standing convention gets a sharper phrasing: **propagate the worst corner through every derived quantity, not just the swept primitives.**

## Cross-learning

- **Supersedes half of R-com-offset-thrust-alignment's proposed requirement.** The compliant design is now: **polar harvest port centered to 0.07–0.24 m (chunk-size-dependent), stack roll ≥ 1 revolution/day about the thrust axis, 3° thrust-vector trim, and a ~25 kg attitude-propellant allowance.** The ±1.7 m / 12° tracking requirement stands only as the no-roll fallback. Round 169's cosine-tax and RCS-fought-is-dead findings are untouched.
- **Positive for the barbecue-roll heritage line:** Apollo passive thermal control is the flown precedent for exactly this maneuver class; the stack roll also evens bag-wall thermal loading, which the bag-engineering doc treats as a separate open item — one maneuver, two problems.
- **New bench item for the bag design:** port-centering under cinch (does the cinch geometry pull the port off-axis?) joins the three existing bag bench questions.
- **Follow-on candidates:** coupled roll + wobble dynamics of the flexible bag under thrust (Basilisk material); thermal-front model to pin s empirically.
- Orchestrator handoff: requirement rewrite and design-axes amendment are orchestrator-owned; this round supplies the numbers.
