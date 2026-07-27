# R-chunk-capture-contact-fidelity — STUDY (pre-registration, Tier-1.5 re-scoped execution)

**Worker:** worktree-172651 (project-owner-directed "run the open rounds"), 2026-07-24
latest+28. **SCOPE:** `SCOPE.md` (Saturn, latest+25, `855c126`) — never executed by its
dispatched worker (hyperion-3 never spawned).

## Re-scope declaration (read first)

The SCOPE as written is a MuJoCo-primary / Drake-cross-check contact Monte Carlo,
estimated 36–72 hours of dedicated model-building and runs. Executing that hastily
in-session would produce fidelity theater, not fidelity. Two integrated post-SCOPE
recommendations govern this execution instead:

- **rhea-5 (Tier-1.5 round, integrated latest+28):** re-scope the contact-fidelity
  round to **ram-scoop containment + harpoon cross-check** — the harpoon capture chain
  is already mechanics-derived at Tier 1.5 (0.549 [0.545, 0.553]) and its remaining
  load-bearing unknown is a *bench measurement* (porous-ice penetration), which no
  contact sim can supply.
- **rhea-3 (Δv coupling):** the Tier-1 ram-scoop capture lead was an artifact of
  scoring capture in isolation; any ram-scoop number must be carried through the
  +7.4 km/s residence-out bookkeeping.

**This execution therefore delivers: (1) a mechanics-derived Tier-1.5 ram-scoop
containment event chain (the piece never modeled beyond hand-set closed-form stage
probabilities), (2) the harpoon cross-check by reusing rhea-5's Tier-1.5 model
unchanged, (3) the cross-architecture delivered-mass coupling via rhea-3's validated
η_dv accounting.** The MuJoCo/Drake Tier 2/3 contact layer REMAINS OPEN as a named
follow-on; nothing here claims contact fidelity, and the SCOPE's H1/H2 (run-count /
engine A/B) transfer to that follow-on untouched.

## Deviations (pre-registered)

- **D-1 (tier):** numpy mechanics event chain (Tier 1.5), not MuJoCo/Drake contact
  (Tier 2/3). Honest-tier labeling per Deviation-8 precedent.
- **D-2:** SCOPE H1 (binomial run count) answered analytically at this tier (n is
  cheap); SCOPE H2 (engine A/B) deferred to the MuJoCo follow-on.
- **D-3:** harpoon side is rhea-5's model reused verbatim (cross-check, not rebuild).
- **D-4 (declared exclusion):** cinch-actuator / latch *mechanism reliability* is not
  derivable from mechanics at any desk tier — per Round J, containment is precisely a
  "GNC / mechanism-reliability problem." What this model derives is the physics
  envelope (geometry, timing race, energy); the mechanism-reliability residual is the
  demonstrator/bench deliverable.
- **D-5:** SCOPE H6 (≥ 25 t delivered at commercial coupling) is re-read as MOOT after
  R-l0-relaxation-envelope (latest+28: commercial closure is the empty set at every
  relaxation). Capture posteriors are reported for the demonstrator track instead.

## Model (ram-scoop Tier-1.5 containment chain)

Per-chunk event chain on the Tier-1 shared priors (comparability), plus mechanics axes
in the style of rhea-5's harpoon model. Fixed design parameters (declared): aperture
radius 15 m; bag depth 30 m; drawstring radial closure speed sampled (see axes).
Grounded inputs: Round J's derived containment ceiling (Zylon whole-bag 24.6 m/s at
1 t → 10.2 m/s at 200 t, exact m^(−1/6) scaling; pessimistic contact-patch corner
~2.4→0.99 m/s) sampled as a single ceiling-coefficient axis; Round J's fragmentation
threshold √(3σ_ice/2ρ); ellipsoid chunk geometry per rhea-5.

Chain (first-failure): **aperture-miss** (pose error + spin drift vs aperture margin)
→ **oversize-jam** (silhouette vs aperture) → **bounce-out race** (inelastic rebound
transit time vs drawstring closure; escape only if the chunk fits through the
still-open aperture at return) → **containment tear** (operating velocity vs Round-J
mass-scaled ceiling) → captured. **Fragmentation** (v > √(3σ/2ρ)) is tracked as
`captured_rubble` — contained water, degraded coherent-chunk handling, per Round J's
reading — and counts as capture success for water accounting, reported separately.

Operating velocity v_op = max(approach velocity, GNC null residual) — the residual
axis (1 mm/s – 1 m/s, log) encodes Round J's caveat (b) that the *achievable* null,
not the dynamics floor, sets the operating point.

Two runs: **(A) shared-prior run** (Tier-1 axes, v_op capped in the 0.3–3 cm/s band,
GNC residual axis pinned low) for the H-K1 comparison against Tier-1's 0.405;
**(B) operating-velocity sweep** (residual axis live) to map the containment cliff.

## Hypotheses

| # | Hypothesis | Gate | Prediction |
|---|---|---|---|
| H-K1 | Mechanics-derived ram-scoop capture differs from Tier-1 closed-form 0.405 by ≥ 0.05 on shared priors (SCOPE-H3 analog) | \|p − 0.405\| < 0.05 falsifies | **Tier-1.5 HIGHER, 0.80–0.95** — hand-set stage penalties (0.92/0.95/0.90/0.92/0.93) have no mechanical basis at cm/s: entry geometry, race timing, and energy margins are all easy there (same direction as harpoon 0.365 → 0.549) |
| H-K2 | Harpoon's delivered-mass lead survives Tier-1.5 posteriors through rhea-3's η_dv coupling (SCOPE-H4) | lead < 2× or credible intervals overlap falsifies | **HOLDS at ~3×** — 5.31× η_dv penalty × (0.549 / p_rs); even p_rs = 1.0 leaves harpoon ≥ 2.9× |
| H-K3 | Chunk spin is structurally irrelevant to ram-scoop capture (SCOPE-H5 analog) | spin total-order sensitivity ≥ 0.10 falsifies | Holds — accretion has no wrap-race; spin enters only via entry drift (mm-scale) and rubble threshold |
| H-K4 | The containment cliff is operational (GNC-residual band), not structural: capture collapses by ≥ 0.2 between v_op = 1 cm/s and 1 m/s, dominated by bounce-out + pessimistic-ceiling tear | collapse < 0.2, or dominated by other modes, falsifies | Holds — mechanizes R-A14's velocity-conditional 0.78 → 0.55 and Round J's "operational effect" attribution |
| H-K5 | SCOPE-H1 (±0.02 binomial half-width at n ≈ 1200) is satisfiable at the operating point | half-width at n=1200 > 0.02 falsifies | Holds (Bernoulli outcome; 1.96·√(p(1−p)/1200) ≤ 0.028 worst-case, ≤ 0.02 for p outside [0.27, 0.73]) — report exactly |

## Model-form risks (declared)

The bounce-out race treats the chunk as a point mass on a normal-incidence rebound
with a single restitution draw; a real bag interaction is multi-contact with tumbling
and fabric billow (that is the MuJoCo follow-on's job). The drawstring is modeled as a
constant-rate radial closure with no snag. Both simplifications *flatter* the
ram-scoop; since the load-bearing verdict (H-K2) is that ram-scoop loses anyway, the
flattery is verdict-safe (adverse-direction bias would only widen harpoon's lead).
