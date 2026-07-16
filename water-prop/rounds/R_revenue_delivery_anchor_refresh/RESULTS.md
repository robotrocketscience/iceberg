# R-revenue-delivery-anchor-refresh — RESULTS

**Worker:** hyperion (re-spawn 2). **Date:** 2026-05-26. Deterministic; `python3 run.py` reproduces `results/sweep_summary.json` and `results/anchor_reconciliation.csv`.

---

## Headline

**The financial verdict does NOT flip anywhere in the corrected 17–28% delivery band, nor at the conservative 0 t reading. H6 (load-bearing) holds.** The delivery correction sharpens per-mission tonnage and revenue but is not the binding constraint on program-class; reactor-program availability (L0-24) and the 200 t chunk-mass cap (L1-007) bind first. The pitch §4 table's "50 t delivered" is the optimistic-corner artifact (only honest at 25%, the top of the band); the **revenue rounds' operative anchors already sit inside the band** (clearing 42 t; demand-curve central E_500 50 t), while the demand-curve's *VariantB at 80 t* is a genuine above-cap optimism — but it belongs to a retired (500 kWe) power class, so it does not carry the live verdict.

This confirms M-3's underlying worry was directionally real for one architecture (VariantB 80 t violates the cap) but the conclusion M-3 feared — a financial-verdict flip — does not occur. **It is a pitch-honesty fix, not a thesis change.**

---

## Anchor reconciliation (results/anchor_reconciliation.csv)

| Round | Anchor | delivered_t used | In corrected band 34–56 t? | Capture needed @ ~20% pin | Cap (200 t) status |
|---|---|---|---|---|---|
| R-LEO-water-demand-curve | E_500kWe_200t | 50 t | **yes** (25% corner) | 250 t | **violates** at ≤20% |
| R-LEO-water-demand-curve | E_200kWe_100t | 30 t | no (below) | 150 t | ok |
| R-LEO-water-demand-curve | VariantB_500kWe | 80 t | **no (far above)** | 400 t | **violates** at every band fraction |
| R-clearing-price-tail-integration | 1-launch arch (run.py:117) | 42.04 t | **yes** (~21%) | 210 t | borderline (ok at ≥21%) |
| R-pricing-anchor-revisit | n/a — purely $/kg | — | n/a | — | n/a |

The two **live, operative** anchors (clearing 42 t; demand central E_500 50 t) are in-band. The two out-of-band anchors are E_200 (30 t, below) and VariantB (80 t, far above — a hard cap violation: 80 t delivered at 17–28% needs 286–470 t captured). VariantB is a retired 500 kWe architecture.

---

## Band sweep (results/sweep_summary.json)

P(any architecture NPV+) is the demand-curve **conditional-on-engineering-and-reactor-success** metric (clearing-round "Frame B"). Clearing break-even $/t = mission_cost($0.3433B) / delivered_t.

| delivered_t | implied fraction @ 200 t cap | P(any NPV+) sov-bond 3% | P(any NPV+) venture 8.7% | clearing break-even $/t | P(price ≥ BE) |
|---|---|---|---|---|---|
| 0 (conservative) | 0% | **0.0%** | 0.0% | ∞ (no revenue) | 0.0% |
| 34 (band floor, 17%) | 17% | 38.6% | 13.2% | $10.10M/t | 33.5% |
| 42 (clearing anchor, 21%) | 21% | 44.0% | 16.3% | $8.18M/t | 38.7% |
| 50 (pitch headline, 25%) | 25% | 48.8% | 19.5% | $6.87M/t | 43.1% |
| 56 (band ceiling, 28%) | 28% | 52.2% | 21.5% | $6.13M/t | 46.1% |
| **baseline** (per-arch {50,30,80}) | mixed | **51.1%** | 29.1% | — | — |

**Framework-pinned operative points:** constraints-OFF ≈ 40 t → P(any) sov ≈ 42–43%; constraints-ON = 0 t → P(any) = 0%. At neither pin does the conditional sovereign-bond P(any) reach 50%.

---

## Chunk-cap interaction (the binding arithmetic)

To deliver the swept tonnage at the honest fraction, required captured tonnes = delivered / fraction:

| delivered_t | @17% | @20% | @25% | @28% |
|---|---|---|---|---|
| 50 t | 294 t ❌ | 250 t ❌ | 200 t ✅ | 179 t ✅ |
| 56 t | 329 t ❌ | 280 t ❌ | 224 t ❌ | 200 t ✅ |

❌ = exceeds 200 t cap (L1-007). **50 t delivered requires ≥25% fraction; 56 t requires 28%.** At the framework's pinned ~20% fraction the cap-respecting delivered ceiling is **40 t**. This is exactly why the pitch's "50 t at 54%" is doubly wrong: the fraction is too high (honest 17–28%, not 54%) AND 50 t at the honest fraction violates the cap.

---

## Verdict-flip detection (H6 load-bearing)

- P(any NPV+) at sovereign-bond over the corrected band: **38.6% → 52.2%**. The 50% line is crossed **only at the 56 t band ceiling** (the 28% optimistic corner), and **only in the conditional-success frame**.
- The **unconditional program-class number** = conditional Frame B × the reactor+engineering conjunction (clearing-round Frame A, < 1% / iapetus 0.0055–0.77%). **Delivered tonnage does not appear in that conjunction.** So the unconditional, full-chain program-class verdict (RULED OUT, P ≪ 1%) is invariant to the delivery anchor.
- The standing program-class reading (iapetus + worktree-110450 + clearing-round H5/H6): full-chain ruled out; conditional-success "viable in principle" only at low discount; marginal IRR sub-sovereign-bond (1.45% at the 200 t cap; sovereign-bond hurdle needs 209 t/ship — 5× the cap). **None of these crossovers move with delivered-per-mission inside 34–56 t**, because the 200 t cap and the reactor conjunction bind first.

**PROGRAM-CLASS VERDICT FLIPS across the band: NO.**

---

## Hypothesis scoring

| # | Verdict | Basis |
|---|---|---|
| H1 | **SPLIT / held-for-live-anchors** | The two operative anchors (clearing 42 t, demand central E_500 50 t) are in-band. But the demand round also carries VariantB at 80 t (hard cap violation) and E_200 at 30 t (below band). Strict reading "≥2 of 3 rounds cleanly in-band" → only clearing is unambiguous; held only if the demand round is scored on its E_500 operative anchor. Matches the pre-registered directional expectation that H1 would be split. |
| H2 | **HELD** | ΔP(any NPV+) at sovereign-bond across 34–56 t vs baseline (51.1%): min 38.6% (at 34 t) → max 52.2% (at 56 t); max swing 12.5 pp < 15 pp. (The 0 t conservative point is outside the 34–56 band the hypothesis names; it trivially exceeds 15 pp — flagged, not counted against H2.) |
| H3 | **HELD** | Clearing break-even $/t across 34–56 t spans **$6.13–10.10M/t**, inside the pre-registered [\$6M, \$13M]. Scales inversely with delivered tonnes as predicted. |
| H4 | **HELD (structural)** | R-pricing-anchor-revisit `run.py` + `inverse_risk_check.py` take only `price_per_kg`; zero delivered-tonnage references (grep-confirmed). H7 cannot move under a delivery-anchor correction. |
| H5 | **FALSIFIED-narrow / held-in-effect** | The pitch §4 table is NOT the *only* artifact misstating delivered tonnage — the demand round's VariantB (80 t) is also above-cap optimistic. But VariantB is a retired 500 kWe architecture, so the only *live* misstatement is the pitch table. Practical conclusion (revenue-round verdicts robust) holds. |
| **H6** | **HELD (load-bearing)** | Program-class verdict invariant across {0, 34, 42, 50, 56} t. Conditional sovereign-bond P(any) crosses 50% only at the 56 t optimistic corner and only in the conditional frame; the unconditional full-chain verdict does not touch delivered tonnage. Conservative 0 t reading is trivially NPV-negative. |

**4 clean HELD (H2/H3/H4/H6), 1 split (H1), 1 falsified-narrow (H5).** The two non-clean grades are both about *which artifacts carry an optimistic anchor* (M-3's bookkeeping question), not about *whether the verdict flips* (H6 — the load-bearing reading), which holds unambiguously.

---

## Cross-references

- Feeds R-pitch-arithmetic-audit deferred claims **C20 / C26 / C28** (revenue figures) and the `PROPOSED-PITCH-DIFF.md` cascade via `corrected_era_table.md`.
- Sharpens `SATURN-PUNCH-LIST-20260521.md` **M-3**: M-3's feared verdict-flip does not occur; the live issue is the pitch §4 table's optimistic-corner tonnage, addressed by the drop-in.
- Consumes R-framework-matrix-parity (`READING.md` delivery-ratio pin) and R-pitch-arithmetic-audit (`f9f7fc2`, 17–28% band).
- Does not contradict iapetus R-T1-sensitivity / R-staged-options program-class framing (verified: verdict invariant).
