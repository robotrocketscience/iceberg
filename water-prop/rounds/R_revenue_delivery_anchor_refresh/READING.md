# R-revenue-delivery-anchor-refresh — READING (5-section template)

**Worker:** hyperion (re-spawn 2) · **Date:** 2026-05-26

## Hypotheses adjudicated

H1 **split** (held for the two live operative anchors; the demand round's retired VariantB 80 t anchor is out-of-band and cap-violating) · H2 **held** (max P(any NPV+) swing 12.5 pp < 15 pp across 34–56 t) · H3 **held** (clearing break-even $6.13–10.10 M/t, inside [6, 13]) · H4 **held** (pricing round is purely $/kg; structural) · H5 **falsified-narrow / held-in-effect** (the pitch §4 table is not the *only* artifact misstating delivered tonnage, but the other offender is a retired architecture) · **H6 (load-bearing) held** (program-class verdict invariant across the band and at the 0 t conservative reading).

Predicted-vs-measured: my frozen STUDY.md directional note predicted H1 would be split (it was) and H6 would hold robustly despite H1 failing (it did). The financial verdict cannot move toward viability on a delivery-anchor change because lowering delivered tonnage only lowers revenue, and the binding constraints (200 t cap, reactor conjunction) sit upstream of per-mission tonnage.

## Headline

**The delivery correction is a pitch-honesty fix, not a financial-thesis change.** Punch-list M-3 feared that correcting the 54% delivery claim down to the honest 17–28% would shift the financial verdict. It does not: the program-class verdict (sub-sovereign-bond / technology-demonstrator at conservative anchors) is invariant across the entire corrected band, and is trivially confirmed at the matrix-faithful conservative 0 t reading (zero revenue). The pitch §4 "50 t delivered" was the 25%-corner optimistic value; the framework pins the constraints-off delivered mass at ~40 t (and 0 t conservative). The revenue *rounds'* operative anchors (clearing 42 t, demand central 50 t) already sit in-band, so M-3's "the revenue model assumes the wrong number" worry is mostly unfounded — the one exception (demand-curve VariantB at 80 t) is a retired 500 kWe architecture and a hard cap violation, so it carries no live verdict.

## Reading (for the project owner)

Three things follow, none of them architectural:

1. **The pitch §4 table is the live artifact to fix, and the fix is small.** State entry-tier delivered as a band (0 t conservative; 34–56 t constraints-off; ~40 t at the framework pin), not the point "50 t." Per-ship gross becomes ~$270–450M (centered ~$320M), not a point $400M, and $0 under the conservative reading. The mid-program "200 t" and steady-state "500–1000 t" rows conflate *captured* with *delivered*; at L1-007 = 200 t captured, delivered cannot exceed 56 t in any era. `corrected_era_table.md` is the drop-in. It does not touch the program-class verdict.

2. **The binding arithmetic is the cap, not the fraction.** Even at the optimistic 25–28% fraction, delivering 50–56 t consumes the entire 200 t capture budget; at the honest ~20% pin, 50 t is impossible (needs 250 t captured). The delivered-per-mission ceiling is **56 t while L1-007 holds**, regardless of reactor era. Any pitch revenue line above ~$450M/ship at the current $/kg implies a cap violation.

3. **Do not read the conditional sovereign-bond P(any) ≈ 50% as viability.** That number (38.6–52.2% across the band) is conditional on engineering AND reactor success. The unconditional program-class number multiplies it by the < 1% reactor+engineering conjunction (iapetus 0.0055–0.77%), which delivered tonnage does not touch. The full-chain verdict stays RULED OUT.

## Cross-learning

- **Positive for R-pitch-arithmetic-audit (`f9f7fc2`):** supplies the corrected revenue figures (C20 / C26 / C28) and the `corrected_era_table.md` drop-in that its `PROPOSED-PITCH-DIFF.md` deferred. The audit's directional FAIL on C13 (54% → 17–28%) is now quantified into the era table.
- **Negative for R-LEO-water-demand-curve (`enceladus-r5`):** its VariantB_500kWe architecture carries `delivered_t = 80 t`, which is unachievable under L1-007 (needs 286–470 t captured at the honest fraction) — independent of its already-retired 500 kWe power class. Not a verdict-changer (VariantB is retired), but the harness's delivered_t set {30, 50, 80} should be re-anchored to the cap-respecting band if the round is ever revived.
- **Consistent with R-pricing-anchor-revisit (titan-5) + iapetus R-T1-sensitivity:** the verdict is invariant; the binding axis remains reactor-program availability (L0-24), not revenue per mission. This round adds a third independent confirmation (after pricing-anchor and the parity round) that the economic axis is non-binding.
- **Methodology-lesson candidate (hyperion, awaiting project-owner ratification):** *a flagged-wrong headline number and a load-bearing input are different objects; correcting the former does not require — and should not be assumed to cause — a verdict change.* M-3 reasoned "if the 54% delivery claim is wrong, the financial verdict shifts." But the delivery fraction feeds revenue, which was never the binding constraint; the cap and the reactor conjunction bind upstream. This compounds R-pricing-anchor-revisit's lesson ("before correcting an anchor, confirm the axis it sits on is load-bearing") with its mirror: *when a punch-list item predicts a verdict shift from a number correction, test whether the number is on the binding axis before assuming the shift.* The honest output here is a band-sweep that shows the verdict is flat across the entire corrected range.

## Revisit

The frozen prediction (H6 holds; H1 splits) was accurate. The one thing I underestimated in STUDY.md: I expected the demand round to be the worse offender on H1, but its *central* anchor (E_500 at 50 t) is actually in-band — it is only the retired VariantB row that fails. So the live revenue model is in better shape than M-3 (or I) feared; the optimism is concentrated in (a) the pitch table and (b) a retired architecture, both of which are harmless to the standing verdict. The exact-fraction re-touch the SCOPE flagged as blocked on R-framework-matrix-parity is now moot for the verdict: the parity pin (~20% / 0 t) lands inside the swept band and the verdict is flat across it.
