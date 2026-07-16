# R-framework-matrix-parity — RESULTS

**Worker:** titan-4 · **Date:** 2026-05-22 · **Branch:** `iceberg-titan-4`

All four matrix-carried constraints are encoded in `mission_graph`, each gated by
a param defaulting to non-binding, so **constraints-OFF reproduces the
pre-encoding baseline exactly** and the diff is a clean before/after on one
codebase. 143 framework tests pass (121 prior + 22 new constraint tests).

---

## Headline

| Sweep | 30 t / strict 15 yr | 30 t / waiver 25 yr |
|---|---|---|
| Canonical 750-cell, constraints **OFF** | **16 cells** | 16 |
| Canonical 750-cell, constraints **ON** | **0 cells** | **0** |

**The framework's 200-tonne-chunk closure cell collapses completely under joint
encoding of the four matrix constraints.** It collapses on TWO independent
killers, each sufficient on its own:

1. **Powerplant dry-mass floor (constraints 2+3).** The cells that closed in the
   baseline were small vehicles (50/63/100 t) carrying a 200 t chunk. A 50 t
   vehicle at 80 % propellant has 10 t of dry mass; a 30 kWe powerplant needs
   **22.8 t** (2 t bus + 12.5 t reactor @ 2.4 W/kg + 8 t MARVL radiator +
   0.3 t thrusters). The vehicle cannot carry its own reactor — rejected at
   Phase 1. The vehicles big enough to carry the plant (≥150 t) deliver < 30 t
   even in the baseline.
2. **Reactor lifetime (constraint 1).** Cells that *do* clear the mass floor
   (e.g. 100 t vehicle at sp = 10 W/kg) are killed by cumulative reactor ON-time
   of **14–16 yr at 30 kWe** — well over any plausible lifetime ceiling. The
   reactor cannot run long enough to move a 200 t chunk at the flyable power
   envelope.

This is H6's "collapse" branch: the matrix returns to **zero surviving cells at
conservative anchors** in the framework's full-round-trip accounting.

---

## Constraint-by-constraint diff (canonical grid)

| Constraint | Mechanism | Effect on the 200 t cell |
|---|---|---|
| 1 — reactor lifetime | cumulative electric-burn ON-time vs L·8760 h | Kills cells that clear the mass floor (14–16 yr burn > L). At sp = 2.4 the mass floor removes the deliverers first, so lifetime is non-marginal there (0 close even at L = ∞ on the sp = 2.4 grid). |
| 2 — reactor + MARVL radiator mass | dry-mass floor = reactor (P/sp) + radiator (5 t + 0.1 t/kWe) + thrusters | Dominant killer at sp = 2.4: removes every small-vehicle deliverer. The framework previously charged **zero** for the powerplant. |
| 3 — conservative bus floor | + 2000 kg bus in the floor | Marginal on top of constraint 2 (2 t of a 22.8 t floor). |
| 4 — vis-viva capture burn | √(v_inf² + v_esc²) − v_circ instead of 0.4·v_inf+0.3 | Raises arrival burns 2.5–3 km/s; not the binding killer for the 200 t cell (it dies upstream at Phase 1), but it correctly prices the arrival leg and reproduces titan-3's 7.3-direct / 4.2-post-LGA anchors. |

### H1 — reactor-lifetime sensitivity (canonical grid, sp = 2.4)
`L ∈ {5, 10, 15, ∞}` → **0 closing in every case.** H1's predicted "survives at
L = 15, collapses at L = 5" is **falsified in framing**: lifetime is not the
marginal axis on the sp = 2.4 grid because the mass floor (constraint 2) has
already removed every cell that would deliver ≥ 30 t. Lifetime *is* binding on
the sp = 10 grid (it is the killer for the 100 t-vehicle cell that clears the
mass floor — 14.37 yr > 10 yr).

### H2 — specific-power sensitivity (canonical grid, L = 10)
`sp ∈ {2.4, 5, 10}` → **0 closing in every case.** Even at the optimistic
Kilopower-extrapolation 10 W/kg, the 200 t cell does not survive: lighter
reactor mass lets the 100 t vehicle clear the floor, but it then fails reactor
lifetime. H2's "200 t cell survives, band narrows" is **falsified** — the cell
collapses outright at all three specific powers.

---

## titan-3 reproducibility (H4) — does NOT reproduce; scope mismatch (not a bug)

titan-3 R-chunk-size-pareto's 4 strict cells (50–60 t chunk / 30 kWe / lunar-GA
arrival, delivering 35.6–45.4 t) **do not reproduce in the framework**, even with
constraints OFF and titan-3's Isp 2000 anchor:

| Chunk | titan-3 delivered | framework delivered (OFF, Isp 2000, 63 t veh) | ratio |
|---|---|---|---|
| 50 t | 35.6 t | **19.4 t** | 0.54 |
| 60 t | 43.4 t | **24.6 t** | 0.57 |
| 80 t | (n/a) | 34.9 t (closes 30 t) | — |

**Root cause is mission scope, not a physics bug.** titan-3 modeled the
**inbound leg only**: it assumed the vehicle is already in Saturn orbit with a
captured chunk, used the chunk as the *sole* propellant, and charged **no
Earth-launched propellant and no powerplant mass on the launch stack**
(`m_initial = m_dry + chunk`, with m_dry ≈ 20 t). The framework models the **full
round-trip from Earth launch**: it launches an 80 %-propellant vehicle, spends
most of that propellant getting to Saturn (Phase 1 spiral + Phase 2 capture),
captures the chunk, and only then runs the inbound leg. The framework therefore
delivers ~half of titan-3's number for the same chunk because titan-3 never paid
for delivering the vehicle and its propellant to Saturn.

The two artifacts answer different questions:
- **titan-3:** *given a chunk already at Saturn, can the inbound leg deliver ≥ 30 t?*
- **framework:** *can a vehicle launched from Earth go to Saturn, capture a chunk,
  and return ≥ 30 t — carrying its own powerplant the whole way?*

The framework is the **stricter, more complete** model. It reproduces titan-3's
*qualitative* conclusion (small chunks at the flyable power envelope are
marginal-to-infeasible) and the *direction* of the cliff, but not the cell-level
delivered tonnage, because titan-3's accounting omitted the outbound cost.

---

## enceladus-r5 reproducibility (H5) — reproduces within tolerance (methodological check)

500 kWe is RETIRED per the project-owner directive; this is a methodology check
only. At enceladus-r5's anchor (200 t chunk / 500 kWe / sp 10 / Isp 2934 /
Cassini 600 kg bus):

| | framework (constraints OFF) | enceladus-r5 claimed |
|---|---|---|
| Best delivered | **106 t** | 91.5 t |
| Round-trip | 11.2 yr | 12.7 yr |

Agreement is **+15.9 % on delivered mass — within H5's ±20 % band.** The
framework runs slightly *generous* because it omits enceladus-r5's realistic
radiation-shield + power-control-unit + cable penalties (which took
enceladus-r5's 9 cells down to 6). Constraints-OFF the framework closes 8 cells
at the enceladus-r5 anchors vs enceladus-r5's stated 9 — consistent.

Constraints-ON, the 500 kWe cell collapses: its powerplant is **~110 t** (50 t
reactor + 55 t MARVL radiator + 5 t thrusters) and cannot fit a 200 t vehicle's
40 t dry envelope. Cells stay retired.

**Note the opposite-direction biases:** titan-3 (inbound-only) was *generous*, so
the framework delivers *less* than titan-3; enceladus-r5 (shielding-penalized)
was *pessimistic*, so the framework delivers *more* than enceladus-r5. Both
reconcile once the differing simplifications are accounted for. The framework
brackets cleanly between them.

---

## Where the bug lives

No framework physics bug was found. The encoding surfaced **one genuine
framework correctness fix** (constraint 4: the Phase 6 capture-burn formula was
unphysically cheap — 0.7 km/s at v_inf = 1, ignoring the LEO escape-velocity
floor; now vis-viva-correct) and **three missing terms** the framework simply did
not model (reactor mass, radiator mass, reactor lifetime). After encoding, the
remaining framework-vs-matrix divergence is **entirely attributable to mission
scope**: titan-3 and enceladus-r5 each modeled a partial mission (inbound-only /
shielding-omitted-or-penalized), while the framework models the full round-trip
with the powerplant carried throughout. The divergence is documented, not
unexplained.
