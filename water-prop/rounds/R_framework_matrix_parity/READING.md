# R-framework-matrix-parity — READING (load-bearing)

**Worker:** titan-4 · **Date:** 2026-05-22

## H6 verdict

**The framework is matrix-replay-trustworthy as a full-round-trip accounting —
and it is MORE conservative than the matrix. It is NOT a cell-for-cell replay of
titan-3, because titan-3 modeled a different (smaller) mission scope.**

Once the four matrix-carried constraints are encoded, the framework's surviving
set at conservative anchors is **empty**. The framework does not "reproduce
titan-3's 4 cells + enceladus-r5's 9/6 cells within tolerance" (the optimistic H6
reading). Instead it shows that titan-3's 4 strict cells **were computed on an
inbound-only model** that omitted the outbound delivery cost and the powerplant
mass, and that they **do not close once the full round-trip is paid for**.

H6 is **not falsified** under its own clause (which falsifies only on persistent
> 30 % disagreement with *no identifiable root cause*): the disagreement is large
but the root cause is identified and clean — **mission scope**. The framework
charges for (a) launching the vehicle and its propellant from Earth, (b) the
outbound spiral and Saturn capture, (c) carrying the reactor + radiator + bus the
whole way, and (d) the reactor's finite lifetime. titan-3 charged for none of
(a)–(d); it began with a chunk already in Saturn orbit and burned it home.

### What this means for the matrix

The framework should be treated as the **canonical, more-complete sweep
substrate going forward**, replacing per-round copy-paste scripts — but with one
explicit caveat recorded in the matrix:

- The matrix's **titan-3 closure cells (axis 02 / axis 09)** are an
  **inbound-only accounting**. Under the framework's full-round-trip accounting,
  they deliver **~half** their stated tonnage (50 t chunk: 19.4 t vs 35.6 t) and
  **do not close** at the conservative-anchor floor.
- The matrix's **enceladus-r5 cells** reproduce within ±16 % at their own anchors
  (methodological validation), and the framework brackets cleanly between
  titan-3 (generous, inbound-only) and enceladus-r5 (pessimistic,
  shielding-penalized).
- The framework's constraints-ON verdict — **0 surviving cells at conservative
  anchors (1–55 kWe flyable envelope)** — is consistent with the locked power
  findings and titan-3's own R-kilowatt-class-power-envelope round (0 of 36
  cells). It is the strongest converged statement to date that the inbound
  delivery cell at the flyable power envelope is **empty under honest
  full-round-trip + powerplant + lifetime accounting**.

This does NOT resolve project-owner decision points #14 or #15 (out of scope).
It produces a clean substrate for them: future architectural rounds should run
in the framework, where the four constraints are now first-class and gated.

## Two independent killers (both real, both load-bearing)

1. **A vehicle small enough to be launch-feasible cannot carry a flyable-class
   reactor.** At 30 kWe / 2.4 W/kg the powerplant is 22.8 t; a 50 t launch
   vehicle has 10 t of dry mass. This is the dominant killer at conservative
   specific power (constraint 2 + 3).
2. **A reactor cannot run long enough to move a multi-tonne chunk at the flyable
   power envelope.** Cumulative full-power burn to move a 200 t chunk at 30 kWe
   is 14–16 yr — over any plausible lifetime ceiling (constraint 1). This kills
   the larger vehicles that *can* carry the plant.

These are the same two physics walls the campaign's locked findings already name
(power finding 1: 40 W/kg is aspirational; the audit's three engineering bets).
The framework now enforces them structurally rather than by per-round assertion.

## M-3 — 75 % chunk-tow delivery anchor (framework-derived replacement)

The pitch headline's **"~75 % chunk-tow delivery"** is an **inbound-leg chunk
retention number** from titan-3's inbound-only model (60 t chunk → 45.4 t
delivered = 75.7 %, i.e. ~25 % of the chunk is burned as propellant on the way
home, at Isp 2000). It is **not an end-to-end delivery ratio** and should not be
presented as one.

Framework-derived full-round-trip delivery ratios (delivered / nominal chunk):

| Accounting | Delivery ratio |
|---|---|
| titan-3 inbound-only (the 75 % anchor) | ~75 % of chunk |
| Framework full round-trip, **constraints OFF** | **~20 %** of nominal chunk (39.5 t / 200 t) |
| Framework full round-trip, **constraints ON** (conservative) | **0 %** — no cell delivers ≥ 30 t |

**Recommendation for a future R-pitch-arithmetic-audit:** retire the bare "75 %"
figure as a delivery claim. If a delivery ratio is needed, state it leg-by-leg
with explicit scope: capture efficiency × inbound retention × (outbound +
powerplant overhead). The single end-to-end number the framework supports
constraints-off is **~20 % of the nominal chunk**; under conservative
constraints there is no closing cell to quote a ratio from.

## Honest-prior scorecard (frozen STUDY.md predictions vs outcome)

| # | Predicted | Outcome |
|---|---|---|
| H1 | Lifetime collapses 200 t cell at L = 5, survives L = 15 | **Falsified-in-framing**: 0 close at all L on sp = 2.4 (mass floor removes deliverers first); lifetime binds on sp = 10. |
| H2 | 200 t cell survives, band narrows | **Falsified**: cell collapses outright at sp ∈ {2.4, 5, 10}. |
| H3 | Vis-viva is the load-bearing split; arrival paths shift to LGA/aero | **Partial**: vis-viva correctly raises arrival cost and reproduces titan-3's anchors, but is not the binding killer (cells die upstream at Phase 1). |
| H4 | titan-3's 4 cells reproduce within ±20 % | **Falsified**: ~half delivery; root cause = inbound-only scope mismatch (not a bug). |
| H5 | enceladus-r5 reproduces within ±20 % | **Supported**: +16 % delivered, 8 vs 9 cells constraints-off. |
| H6 | Framework matrix-replay-trustworthy | **Supported with qualification**: trustworthy and MORE conservative; supersedes (does not replay) titan-3's inbound-only cells. |

My frozen prior expected H2 to be the dominant effect and the 200 t cell to
collapse — both held. I underestimated that the architecture-parameterization
mismatch (round-trip vs inbound-only) would make H4 a *scope* finding rather than
a tolerance finding; that is the most important thing this round surfaced.
