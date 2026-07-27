# R-hohmann-vinf-reconciliation — STUDY

**Round:** R-hohmann-vinf-reconciliation (worktree-115637, 2026-07-21 latest+25)
**One line:** The campaign's 6.21 km/s Saturn-departure v∞ is a **faster-transfer** value (perihelion ≈0.65 AU), ~14 % above the minimum-energy Hohmann **5.44 km/s** — but the correction is **immaterial** downstream (≤5 kWe of a 155-175 kWe reactor floor; Titan-lever revocation intact). Discharges the design-axes/04 corrections-live-forward item.

## Hypotheses (pre-registered in SCOPE.md; bounds in scope_bounds.py)

**Test.** `run.py` computes the two-body heliocentric Hohmann v∞, solves the transfer perihelion that yields 6.21, propagates both v∞ through the single-burn B-ring departure Δv and R179's reactor-power model (reproduced verbatim), and checks R186's Titan bound-chain cap. Deterministic.

## Result

| ID | Predicted (SCOPE band) | Measured | Held? |
|---|---|---|---|
| **H1 [S]** two-body minimum | 5.44 km/s, robust; band [5.3,5.6] | **5.44** (5.443 / 5.443 / 5.439 at a_S = 9.537 / 9.5388 / 9.582 AU) | **HELD** |
| **H2 [S]** what 6.21 is | faster transfer, perihelion q ∈ [0.55,0.75] AU | **q = 0.646 AU** (inside Venus's orbit); 6.21 is conservative by ~12–14 %, not tangent | **HELD** |
| **H3 [S]** Δv barely moves | change [0.10,0.25] km/s; reproduces R179's 8.51 | 8.513 (6.21) → 8.349 (5.44); **change 0.164 km/s (1.9 %)**; d(Δv)/d(v∞)=0.23 | **HELD** |
| **H4 [S]** reactor + Titan unmoved | floor ∈[150,175] kWe, |Δ|<10, Titan cap <5.44 | **159→154 kWe** (Δ 5 kWe); R179 headline 175 (9.0 spiral); Titan cap 3.2 < 5.44 | **HELD** |

**Score: 4 HELD, 0 FALSIFIED.** Figure: `results/vinf_reconciliation.png`. Data: `results/findings.json`.

### Cross-checks
- Single-burn escape at v∞=6.21 reproduces R179's departure Δv **8.51 km/s** exactly (verifies the Saturn-centric anchors: μ_S 3.793e16, R_ring 1.07e8, v_circ 18.83 km/s).
- Reactor power at the 9.0 km/s chunk-fed spiral reproduces R179's **175 kWe** headline.
- v∞ robust across three published Saturn semi-major-axis values (9.537–9.582 AU) → the 5.44 result does not depend on the distance convention.

## Reading

**The flag was correct, and its consequence is null.** The campaign's 6.21 km/s is not the minimum-energy Hohmann v∞ (that is 5.44); it corresponds to a **faster Saturn→Earth transfer** whose perihelion dips to ~0.65 AU — a legitimate trajectory (a returning ship *could* fly a faster transfer), but labeling it "Hohmann" was imprecise, and it is **conservative** (it over-states the departure requirement by 14 %). A returning ship minimizing departure energy would use 5.44.

The reason nothing downstream moves is **Oberth quadrature**. The departure burn leaves a deep well: v_circ at the B-ring is 18.83 km/s, escape is 26.63 km/s, and the hyperbolic excess adds *in quadrature* — `Δv = sqrt(v∞² + v_esc²) − v_circ`. So d(Δv)/d(v∞) ≈ 0.23: a 0.77 km/s v∞ error propagates to only 0.16 km/s (1.9 %) of departure Δv, and — through the exponential Tsiolkovsky/burn-time chain — ~5 kWe (3 %) of reactor power, entirely inside the existing 155-175 kWe band. R186's Titan bound-chain cap (~3.2 km/s) sits far below even the corrected 5.44, so the Titan pump-up lever stays revoked either way. **The 155-175 kWe reactor floor and the Titan-lever revocation are both robust to the v∞ correction.**

Net: the correction lives forward as a footnote (design-axes/04), not a verdict change. If anything, the campaign was slightly *pessimistic* on departure — the honest minimum-energy return is marginally easier than assumed, but not enough to matter.

## Revisit (mandatory)

- **All four held**, three of them as tight derivations (H1/H3/H4 are closed-form; the "prediction" is a consistency check that the campaign's anchors reproduce and that the sensitivity is as small as the quadrature argument implies). H2 is the one genuinely diagnostic result — I did not know a priori that 6.21 would map to a ~0.65 AU perihelion; it does, cleanly identifying 6.21 as a faster-transfer value rather than an arithmetic error.
- **Framing precision:** the gap is 0.77 km/s = 12.4 % of the campaign value (6.21) or 14.2 % relative to the minimum (5.44). Both are stated; neither changes the "immaterial downstream" conclusion.
- **Scope honesty:** H4 uses the impulsive single-burn chain, which is the *upper bound* on the v∞-sensitivity. R179's 175 kWe headline uses the 9.0 km/s chunk-fed *spiral* Δv, whose v∞-dependence is even weaker (low-thrust escape cost is dominated by climbing the well, ~v_circ; v∞ is residual). So the true reactor-floor sensitivity is ≤ the 5 kWe reported. I did **not** re-derive the spiral model — that was explicitly out of scope; the impulsive bound is sufficient to settle the "does it matter" question.

## Bug-catch

- No code errors; all Saturn-centric anchors reproduce R179 to the digit (departure Δv 8.51, reactor 175 at 9.0 spiral).
- **Not fixed (out of scope, flagged):** the mission_graph `CHUNK_FED_DV_KM_S = 9.0` spiral anchor is carried as a state-of-record constant; this round bounds its v∞-sensitivity but does not re-derive it. A low-thrust spiral-escape derivation with explicit v∞-dependence is a possible follow-on (**R-lowthrust-spiral-departure-vinf**) if the reactor floor ever needs sub-kWe precision — it does not today.
- No NaN/precision issues (deterministic closed forms).

## Cross-learning

- **Backward to R179 / R186:** their departure-Δv and reactor-floor headlines are **robust** to the v∞ correction; the frozen STUDYs are not retro-edited (corrections live forward). R186's Titan-lever revocation is re-confirmed at the corrected v∞.
- **Forward to design-axes/04:** the corrections-live-forward footnote is discharged — the 6.21-vs-5.44 gap is characterized (faster-transfer value, conservative by 14 %) and shown immaterial; the axis note can be updated from "flagged, not yet reconciled" to "reconciled: 6.21 is a conservative faster-transfer value; correction ≤5 kWe, Titan revocation intact."
- **Methodology note:** Oberth quadrature is why departure-leg v∞ errors are cheap and capture/aerocapture v∞ errors are not — worth carrying as a general anchor-sensitivity heuristic (v∞ errors on burns out of deep wells are suppressed by the well depth).
