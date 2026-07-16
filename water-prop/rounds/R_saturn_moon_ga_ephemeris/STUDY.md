# R-saturn-moon-ga-ephemeris — STUDY

**Worker:** phoebe (re-spawn, branch `iceberg-phoebe`)
**Started:** 2026-05-26
**Status:** pre-registered, in progress
**Predecessor:** SCOPE.md (Saturn worker, 2026-05-21); work order `~/.claude/handoffs/iceberg-saturn-to-phoebe-20260526.md`

---

## Question

The `mission_graph` framework carries three constant-scalar Saturn-moon gravity-assist
capture options at Phase 2 (`water-prop/sims/mission_graph/missions/phase2_saturn_capture.py`):

| Option | v_inf reduction anchor | min arrival v_inf | tour months | residual trim |
|---|---|---|---|---|
| `titan_gravity_assist_capture` | 4.0 km/s | 4.0 km/s | 8 | small |
| `rhea_gravity_assist_capture` | 1.5 km/s | 4.0 km/s | 12 | 0.7 km/s |
| `cassini_class_multi_moon_tour` | 5.5 km/s | 3.0 km/s | 24 | 0.2 km/s |

None of these is derived from orbital mechanics. Do they over- or under-state the
v_inf reduction actually available from a moon-flyby tour, across the 2032-2050
demonstrator window?

---

## Method

**Patched-conic gravity-assist, upper-bound posture.** A single flyby conserves the
spacecraft's velocity *relative to the moon* (`v_inf,m`) and rotates it by a turn angle
δ bounded by the moon's gravity:

```
sin(δ/2) = 1 / (1 + r_p · v_inf,m² / μ_moon)          # r_p = flyby periapsis radius
```

The change it imparts to the spacecraft's *Saturn-relative* velocity is
`Δv = 2 · v_inf,m · sin(δ/2)`. This Δv is maximised over v_inf,m at
`v_inf,m* = √(μ_moon/r_p)`, giving a **hard per-flyby ceiling**:

```
Δv_max,single = √(μ_moon / r_p)                        # moon escape speed at r_p / √2 · √2
```

Two consequences drive the whole round:

1. **The per-flyby ceiling is a property of the moon, not the trajectory.** It is
   epoch-independent. Titan's ceiling (~1.6 km/s) dwarfs every other moon's
   (Rhea ~0.42, Dione ~0.33, Tethys ~0.26, Enceladus ~0.14, Mimas ~0.09 km/s).

2. **A multi-flyby tour can in principle pump arrival v_inf all the way to capture**
   (because v_inf,m is conserved and can be re-oriented each pass). So the binding
   constraint is *not* "is the reduction physically possible" — for Titan it almost
   always is — but **how many flybys it takes and how long that tour is**, plus
   whether the smaller moons contribute anything worth the multi-moon complexity.

**What I compute (all as optimistic UPPER bounds — best-case tangential, coplanar,
optimal-geometry every pass):**

- v_inf,m at each moon as a function of arrival v_inf,S (vis-viva at the moon's orbit
  radius, best-case prograde-tangential geometry → minimum v_inf,m → maximum leverage).
- Realistic per-flyby Δv at that v_inf,m (not the theoretical ceiling, the actual value
  at the geometry-determined v_inf,m).
- A sequential pump-down: apply per-flyby Δv repeatedly to reduce v_inf,S, count flybys
  to reach the anchor's claimed reduction, convert flyby count → tour time via a
  resonant-re-encounter spacing assumption, compare to the anchor's tour-months.
- Titan-led multi-moon tour: Titan carries the reduction; inner moons add marginal trims
  bounded by their (much smaller) per-flyby Δv.

**Falsification logic.** Because I compute optimistic upper bounds:
- If the *upper bound* cannot reach an anchor's reduction within the anchor's tour time
  → the anchor is **falsified** (over-stated; not even best-case geometry reaches it).
- If the upper bound exceeds the anchor → the anchor is "physically possible but requires
  near-perfect, never-flown execution"; realistic-geometry derates then apply.

**Ephemeris role.** JPL Horizons pull (Titan, Rhea, Dione, Tethys, Enceladus, Mimas)
across 2032-2050 to (a) verify orbital radii/velocities, (b) confirm leverage is
epoch-invariant (stable near-circular equatorial orbits), (c) sample inter-moon phasing
to assess whether a multi-moon *sequence* is geometrically constructible per epoch.

**Simplifying assumptions (documented limits):** patched-conic (no n-body), coplanar
(moon inclinations < 0.4° → negligible), best-case tangential encounter geometry
(yields upper bounds — real tours derate), resonant re-encounter modelled as a fixed
multiple of moon orbital period (not a phase-search). Out of scope per SCOPE.md:
real-time replanning, Titan-atmosphere altitude optimisation, multi-vehicle sequencing.

---

## Pre-registered hypotheses

Handoff hypotheses (orchestrator-authored), restated precisely:

- **H1.** Titan-only GA achieves > 5 km/s v_inf,S reduction at best-of-window arrival.
- **H2.** Rhea-only GA achieves > 2 km/s v_inf,S reduction at best-of-window arrival.
- **H3.** Cassini-class multi-moon tour exceeds the 5.5 km/s anchor across most arrival epochs.
- **H4.** ≥ 1 arrival epoch exists where multi-moon-tour Δv exceeds the matrix anchor by
  > 50 % (> 8.25 km/s).
- **H5 (load-bearing, orchestrator).** Across 2032-2050, the matrix anchors are within
  30 % of the median ephemeris-derived Δv for each option.
- **H6.** Worst-case arrival epoch produces a multi-moon-tour Δv below the matrix's
  titan-only anchor (4.0 km/s).

phoebe physics-bound additions (pre-registered this round):

- **H7 (load-bearing, phoebe).** The *leverage* (achievable v_inf,S reduction per unit
  tour time) is epoch-INDEPENDENT to within 1 % across 2032-2050, because Saturnian major
  moons have stable near-circular equatorial orbits. The only epoch dependence is in tour
  *phasing/sequencing feasibility*, not in the per-flyby Δv. → If H7 holds, H5's "median
  ephemeris-derived Δv" collapses to a single value per option and the right matrix
  amendment is a constant correction, not an epoch-dependent lookup table.
- **H8 (phoebe).** The small moons (Rhea, Dione, Tethys, Enceladus, Mimas) contribute
  < 1.0 km/s combined to a multi-moon tour under realistic flyby counts; the
  `cassini_class_multi_moon_tour` is operationally a **Titan tour** with marginal trims,
  and the 5.5 vs 4.0 km/s gap between the multi-moon and Titan-only anchors over-states
  the small-moon contribution.
- **H9 (phoebe).** At least one anchor is wrong by a factor relevant to the matrix: either
  a tour-time understatement (anchor's months too few for the flyby count its Δv implies),
  or the Rhea 1.5 km/s anchor is unreachable in 12 months given Rhea's per-flyby ceiling.

**Coordination trip-wire (per work order):** if any anchor is wrong by > 2× in either
direction, surface immediately to orchestrator — do NOT bundle into round completion.

---

## Deliverables (per SCOPE.md + work order)

1. STUDY.md (this file) with H1-H9 pre-registered. ✅
2. JPL Horizons ephemeris pull → `results/horizons_moon_states.json`.
3. GA leverage + pump-down model → `ga_leverage.py`.
4. `results/ephemeris_dv_table.json` — per-option per-epoch Δv / flyby-count / tour-time.
5. FINDINGS.md — verdict H1-H9 + matrix amendment spec (keep / replace / bracket).

## Physical constants (to verify against Horizons; IAU/JPL standard values)

| Body | GM (km³/s²) | mean radius (km) | semi-major axis (km) | V_orb (km/s) | period (d) |
|---|---|---|---|---|---|
| Saturn (system) | 3.7931206e7 | — | — | — | — |
| Titan | 8978.14 | 2574.7 | 1,221,870 | 5.57 | 15.945 |
| Rhea | 153.94 | 763.8 | 527,108 | 8.48 | 4.518 |
| Dione | 73.116 | 561.4 | 377,396 | 10.03 | 2.737 |
| Tethys | 41.21 | 531.1 | 294,619 | 11.35 | 1.888 |
| Enceladus | 7.211 | 252.1 | 237,948 | 12.63 | 1.370 |
| Mimas | 2.503 | 198.2 | 185,539 | 14.30 | 0.942 |

Min flyby altitude assumed: Titan 1000 km (atmosphere ~600 km; Cassini min ~880 km);
all others 100 km.
