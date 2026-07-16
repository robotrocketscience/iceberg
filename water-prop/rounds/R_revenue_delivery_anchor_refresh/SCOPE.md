# R-revenue-delivery-anchor-refresh — re-run the revenue rounds against the corrected delivered-per-mission anchor

**Status:** scope, pre-study. Authored by hyperion (worker), 2026-05-22, from R-pitch-arithmetic-audit (`f9f7fc2`) findings + punch-list item **M-3**. Sharpens M-3 with the corrected delivery anchor and the chunk-cap interaction R-pitch-arithmetic-audit surfaced.

---

## Why this round

R-pitch-arithmetic-audit (`f9f7fc2`) found the pitch's §2 delivered-fraction claim (**54%**) fails: the honest figure under continuous-thrust accounting + a defensible Saturn-departure anchor (5.5–7.7 km/s, not the pitch's 1.5) is **17–28%** (bounded by titan-2 Block-4 21.8% / Option A 17% low, impulsive-corrected ~22–30% high). Punch-list M-3 anticipated this: "the 75 percent delivery claim is what the revenue model assumes; if it's wrong … the financial verdict shifts. Re-run R-LEO-water-demand-curve, R-pricing-anchor-revisit, and R-clearing-price-tail-integration-decision-frame against a corrected delivery anchor."

**Two facts make this more than a mechanical re-run, and reframe M-3:**

1. **The corrected anchor moved further than M-3 assumed.** M-3 was written when the Tsiolkovsky-at-stated-inputs correction looked like ~45% (75 → ~45). Continuous-thrust accounting + the corrected Saturn departure pushes it to **17–28%**. The financial sensitivity must be re-tested at the *real* band, not the punch-list's interim figure.

2. **The binding interaction is delivery-fraction × chunk-mass-cap, not delivery-fraction alone.** The revenue rounds take **delivered tonnes per mission** as a direct architecture input (`delivered_t`), not a fraction. To hit the pitch's headline 50 t delivered at a 22% fraction you must capture 227 t raw — which **violates the 200 t chunk-mass cap (L1-007)**. At the 200 t cap, honest delivered-per-mission is **~34–56 t (centered ~44 t)**. The clearing-price round already uses **42 t delivered** (`R_clearing_price_tail_integration/run.py:115`). So the revenue rounds may already sit at the corrected anchor, and **the pitch §4 table (50 t at 54%) is the optimistic outlier — not the revenue model.** This round tests whether that is true.

**Round type:** parameter-refresh + sensitivity sweep over three existing revenue rounds, with one new joint constraint (delivered-tonnes capped by chunk-mass-cap × corrected delivery fraction). Primarily Python re-runs of existing `run.py` harnesses with a swapped delivered-tonnes input + a sweep over the 17–28% band.

**Dependency note:** the *exact* delivery fraction is BLOCKED on R-framework-matrix-parity (per R-pitch-arithmetic-audit C13/C15). This round can run NOW on the honest 17–28% band as a sweep (no single point needed); it should be re-touched once the framework pins the point value. The band-sweep verdict (does the financial conclusion flip anywhere in 17–28%?) is the load-bearing output and does not require the framework.

---

## The corrected anchor (inputs this round swaps in)

| Quantity | Old (pitch / prior rounds) | Corrected (this round) | Source |
|---|---|---|---|
| Delivery fraction (delivered ÷ captured) | 54% (pitch §2) / 75% (retired P-1) | **17–28% band** (sweep) | R-pitch-arithmetic-audit `f9f7fc2` |
| Chunk-mass cap (captured) | 200 t (L1-007) | 200 t (unchanged) | REQUIREMENTS L1-007 |
| Delivered tonnes per mission at cap | 50 t (pitch headline) | **34–56 t** (= 200 t × 17–28%) | derived |
| Delivered tonnes the revenue rounds currently use | 42 t (clearing-price); per-arch `delivered_t` elsewhere | re-state against corrected band | round harnesses |

---

## Pre-registered hypotheses (worker's honest predictions)

| # | Hypothesis | Predicted range | Falsification band |
|---|---|---|---|
| H1 | At the 200 t chunk-mass cap, the corrected delivered-per-mission band (34–56 t) **overlaps the delivered tonnes the revenue rounds already use** (≈42 t). The revenue rounds are therefore less sensitive to the delivery correction than M-3 feared. | revenue-round `delivered_t` ∈ corrected band for ≥2 of 3 rounds | H1 falsified if ≥2 of 3 rounds use a `delivered_t` outside 34–56 t (i.e., they assumed the optimistic 54%/75% headline). |
| H2 | Re-running R-LEO-water-demand-curve at the corrected band shifts P(any architecture NPV-positive) by **< 15 percentage points** vs its current verdict, because the round already prices realistic delivered tonnage. | ΔP(NPV+) < 15 pp | H2 falsified if ΔP(NPV+) ≥ 15 pp anywhere in the 17–28% sweep. |
| H3 | R-clearing-price-tail-integration's break-even $/tonne ($8.17M at 42 t, 1 launch/15-reuse) **scales inversely with delivered tonnes** and stays within its already-reported tail band across 34–56 t. | break-even $/t ∈ [$6M, $13M] across band | H3 falsified if break-even $/t exits that band at any swept delivered tonnage. |
| H4 | R-pricing-anchor-revisit's H7 verdict (does pricing flip the program-class?) is **invariant** to the delivery correction — the binding constraint is willingness-to-pay vs competing-supply, not delivered tonnage. | H7 verdict unchanged | H4 falsified if the corrected delivered anchor changes R-pricing-anchor-revisit's H7 reading. |
| H5 | The pitch §4 era table (50 t at 54%, FSP 200 t, MW 500–1000 t) is the **only** artifact that materially misstates revenue from the delivery error; the revenue *rounds* do not. Correcting the pitch table down ~20% (50 → ~42 t entry) reconciles it with the rounds. | pitch table is the outlier; rounds robust | H5 falsified if any revenue round's headline verdict moves materially under the correction. |
| H6 (load-bearing) | The financial verdict (program-class: sub-sovereign-bond at conservative anchors, per iapetus + worktree-110450) **does NOT flip anywhere in the 17–28% delivery band.** The delivery correction sharpens per-mission tonnage but is not the binding constraint on program-class — reactor-program availability (L0-24) and the chunk-mass cap bind first. The corrected anchor makes the pitch §4 table honest without changing the campaign's standing financial conclusion. | program-class verdict invariant across band | H6 falsified if the program-class verdict (e.g., crosses the sovereign-bond IRR hurdle) flips at any delivered tonnage in the corrected band. |

---

## Method (worker drafts the actual implementation)

1. **Anchor reconciliation.** For each of the three revenue rounds, extract the `delivered_t` (or equivalent per-mission delivered-tonnage) actually used. Tabulate against the corrected band (34–56 t at the 200 t cap). Output: `anchor_reconciliation.csv`.
2. **Band sweep.** Re-run each round's `run.py` with `delivered_t` swept across {34, 42, 50, 56} t (the corrected band plus the pitch headline 50 t as the optimistic reference point). Capture each round's headline verdict metric (P(NPV+), break-even $/t, H7 reading) at each point. Output: per-round sweep JSON.
3. **Chunk-cap interaction check.** Confirm the delivered-tonnage ↔ captured-tonnage ↔ chunk-cap arithmetic: for each delivered point, back out required captured tonnage at the swept fraction; flag any point that requires >200 t captured (cap violation). This is the constraint that caps delivered-per-mission.
4. **Verdict-flip detection.** For each round, determine whether the headline verdict flips anywhere in the corrected band. The load-bearing output (H6) is the program-class verdict across the band.
5. **Pitch-table reconciliation.** Produce the corrected §4 era-table delivered-tonnage column (entry/FSP/MW rows) and the revenue figures that follow, as a drop-in for the pitch rewrite (feeds R-pitch-arithmetic-audit's deferred C20/C26/C28 + PROPOSED-PITCH-DIFF cascade). Output: `corrected_era_table.md`.
6. **Reading.** `READING.md` with H6 verdict + whether the delivery correction is financially load-bearing or merely a pitch-honesty fix.

---

## Out of scope

- Pinning the exact delivery fraction (BLOCKED on R-framework-matrix-parity). This round sweeps the 17–28% band; it does not need the point value.
- Re-deriving the delivery fraction itself — that is R-pitch-arithmetic-audit's finding + R-framework-matrix-parity's job. This round consumes the corrected band as input.
- Re-opening the chunk-mass cap (L1-007 = 200 t). Taken as given; the cap is the constraint that bounds delivered-per-mission.
- Applying the pitch diff. `corrected_era_table.md` is a drop-in; orchestrator applies after project-owner ratification (same gate as R-pitch-arithmetic-audit).
- Reactor-program-availability / L0-24 (orthogonal; iapetus territory).

---

## Inputs to acquire (reading order)

1. R-pitch-arithmetic-audit deliverables (`water-prop/rounds/R_pitch_arithmetic_audit/`) — corrected anchor + claims C13/C20/C26/C28.
2. `water-prop/rounds/R_LEO_water_demand_curve/run.py` — `ARCHITECTURES[].delivered_t`, clearing-price + NPV logic, H-8-i verdict.
3. `water-prop/rounds/R_clearing_price_tail_integration/run.py` + `STUDY.md` — 42 t delivered, break-even $/t.
4. `water-prop/rounds/R_pricing_anchor_revisit/` (markdown only; no run.py) — H7 reading + AUDIT.md per-round $/kg anchors.
5. REQUIREMENTS L1-007 (chunk-mass cap 200 t) + L0-04 (delivered-mass floor 25 t provisional, locked belief `c95626970c29aeef`).
6. iapetus R-T1-sensitivity + worktree-110450 R-delivery-irr-curve — program-class hurdle crossovers (sovereign-bond 209 t/ship, etc.) for H6.

---

## Deliverables (in commit order)

1. `STUDY.md` — pre-registered H1–H6 frozen before the re-runs.
2. `anchor_reconciliation.csv` — `delivered_t` used by each round vs corrected band.
3. Per-round sweep JSON (`results/`) — headline verdict metric at {34, 42, 50, 56} t.
4. `corrected_era_table.md` — drop-in corrected §4 delivered-tonnage column for the pitch rewrite.
5. `RESULTS.md` — verdict-flip table; H1–H6 scoring; cross-ref to R-pitch-arithmetic-audit C20/C26/C28.
6. `READING.md` — H6 load-bearing reading: is the delivery correction financially load-bearing or a pitch-honesty fix?
7. Handoff doc to orchestrator.

---

## Suggested worker

Any moon comfortable with NPV / clearing-price sweeps and the existing revenue `run.py` harnesses. **Best fit: rhea** (authored R-heterogeneous-cadence + NPV machinery) or **iapetus** (staged-options + program-class framing). Hyperion (this SCOPE's author) is also a fit but has a deep stack of unintegrated commits on `worktree-121226`; prefer a fresh worker so this doesn't pile onto the same branch.

**Workflow flag:** band-sweep can run immediately (no framework dependency). Re-touch the exact-fraction point once R-framework-matrix-parity lands; the band verdict (H6) should not need it.

---

## Cross-references

- R-pitch-arithmetic-audit (`f9f7fc2`) — source of the corrected 17–28% anchor + the deferred C20/C26/C28 revenue claims.
- `SATURN-PUNCH-LIST-20260521.md` M-3 (this round sharpens it).
- R-framework-matrix-parity (open SCOPE) — upstream for the exact delivery point value.
- iapetus R-T1-sensitivity / R-staged-options-with-technology-gates — program-class verdict this round must not silently contradict.
- REQUIREMENTS L1-007 (chunk-mass cap), L0-04 (delivered-mass floor, locked belief `c95626970c29aeef`).
