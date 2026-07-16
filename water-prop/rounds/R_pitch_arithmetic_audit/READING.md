# READING — R-pitch-arithmetic-audit

**Worker:** hyperion · **Date:** 2026-05-22 · **Load-bearing hypothesis:** H6.

## The load-bearing reading

**The pitch's arithmetic is not riddled with errors — it has one, repeated four times, and it is the most load-bearing number in the document.** The §2 ΔV budget understates Saturn-side ΔV (departure listed at 1.5 km/s against a defensible 5.5–7.7) and prices the low-thrust electric legs impulsively. The downstream effect is a delivered-fraction claim of ~54% where the honest figure is 17–28%. Everything in §4 and §5 that is "sized in terms of delivered chunk mass" inherits this ~2–3× optimism.

This is the **same error class** the campaign has now hit repeatedly: impulsive accounting flatters low-thrust electric architectures (methodology lessons 2 and 7). The punch-list caught it as the 75% delivery ratio (P-1); the pitch was edited 75→54%, which *halved the symptom but kept the disease*. An outside propulsion engineer who computes `v_circ` at the B-ring (18 km/s, derivable in 30 seconds from the pitch's own numbers) sees a 1.5 km/s departure and stops reading. **That is the deal-killer the SCOPE was worried about.**

## On H6 (the pre-registered load-bearing reading)

H6 **holds, but the pitch already moved most of the way there.** The dual-revenue science stream (P-5) is already labeled speculative, excluded from the revenue table, and explicitly not load-bearing in §4/§7. The only residual is §6 over-billing it as a co-equal revenue stream. There is no precedent for a science-allocation prebuy; the precedented analogue is a hardware-contribution consortium (Cassini-Huygens, BepiColombo). Recommended edit (D-5) is small and low-risk because no revenue number depends on it.

So the *pre-registered* load-bearing concern (P-5 business model) turns out **not** to be the pitch's biggest arithmetic exposure. **The biggest exposure is the §2 ΔV budget (D-1…D-4).** This is the round's most important reframing: the load-bearing fix is propulsion arithmetic, not the revenue model.

## Project-owner-facing summary

**How many claims fail:** 4 hard arithmetic/physics fails (all one root cause), 1 framing fail, 5 downstream/already-flagged, 21 survive, 1 blocked. The pitch is in better shape than the punch-list implied — most P-1…P-5 literals are already gone — but the surviving error is the central one.

**Which are pitch-killers (fix before any sophisticated external reader sees it):**
1. **Saturn departure 1.5 km/s → 5.5–7.7 km/s (D-1).** Physically impossible as written; trivially caught.
2. **Delivery efficiency 54% → 17–28% (D-2).** Cascades from #1 + continuous-thrust accounting; drives the revenue model.

**Which are derisked / already-handled:** P-2 (lunar 4.6 km/s) fixed; P-4 (97%) absent; P-5 mostly hedged.

**Recommended pitch-rewrite sequence:**
1. **Apply D-1 first** (Saturn departure). Everything else in the ΔV story cascades from it.
2. Apply D-2/D-3/D-4 (delivery fraction, round-trip total, lunar comparison) as the cascade, with the new `[^contthrust]` footnote making the impulsive-vs-continuous frame explicit.
3. Apply D-5 (§6 revenue-stream reconciliation) — independent, low-risk.
4. **Hold the revenue-table numbers** (C20, C26, C28) until a revenue-round re-run against the corrected 17–28% delivery anchor (punch-list M-3, downstream of R-framework-matrix-parity). Do not patch §4 dollar figures piecemeal; they move together with the delivery fraction.
5. **Defer the exact delivered fraction** to R-framework-matrix-parity. Use the 17–28% band as the interim honest figure; it is bounded by titan-2 Block-4 (21.8%) and Option A (17%) on the low side and impulsive-with-corrected-departure (~22–30%) on the high side.

**The honest one-liner for the pitch:** "Delivered fraction is ~20%, not ~54%; the math still closes on Kilopower at 50 t delivered, but the revenue ramp is ~2× slower than the current §4 table — and that is before the reactor-availability and capital-class constraints the rest of the campaign has surfaced."

## Methodology note (candidate, for orchestrator → PROTOCOL ratification)

**Candidate lesson:** *Correcting a flagged number without re-deriving its inputs preserves the error class.* The 75%→54% edit fixed the symptom (a too-high output) by editing the output, not by fixing the impulsive-frame + low-departure-anchor inputs that produced it — so the corrected 54% is still wrong by the same mechanism. When a pre-registered audit flags a derived quantity, the fix must re-derive from inputs, not back-solve a more conservative-looking output. (Surfaced here; orchestrator's call whether it rises to a numbered lesson or a footnote on lesson 2/7.)
