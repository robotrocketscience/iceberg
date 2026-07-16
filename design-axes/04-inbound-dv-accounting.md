---
axis: "Inbound delta-velocity accounting"
status: closed
confidence: high
last_revised: 2026-05-22
related:
  - "[[inbound-propulsion]]"
  - "[[surviving-cell]]"
  - "[[architecture-source-comparator]]"
---

# Inbound delta-velocity accounting

## Current

First-principles continuous-thrust. The matrix's prior impulsive 6.42 km/s number is wrong by 2.1-4.3x once electric thrusters' continuous-thrust nature is properly modeled. **2026-05-19 latest+13 (titan-3 R-delta-velocity-anchor-audit `42120cf`):** two additional anchors corrected via vis-viva re-derivation. Saturn-departure was 5.5 kilometres-per-second informal-sketch; correct value from Hohmann v∞ + Oberth-optimised periapsis ellipse is **7.7 kilometres-per-second** (40 percent understatement). Earth-arrival chemical capture was 3.5 kilometres-per-second informal-sketch; correct value is **7.3 kilometres-per-second direct or 4.2 kilometres-per-second after R12 10-flyby lunar-gravity-assist tour** (~2× understatement under either reading). Methodology lesson 20 candidate (vis-viva-default anchoring when no primary-text source).

**2026-05-21 latest+15 (saturn-worker gap-filler on belief `8be3ec81`, commit `030cb5e`):** the **lunar-surface-to-low-Earth-orbit anchor with aerobraking is ~4.6 kilometres-per-second** (1.87 ascent + 5.93 low-lunar-orbit-to-low-Earth-orbit minus 3.2 aerobraking savings per Wikipedia delta-v-budget table) — not the 6-kilometres-per-second "forever tax" framing carried by `ICEBERG-pitch.md`. The lunar-versus-ICEBERG case loses on per-tonne Δv when aerobraking is admitted; it should be argued on **source concentration** instead — Saturn B-ring 99.7-99.8 percent water (locked belief `c646b3c6`) versus lunar polar 5.6 ± 2.9 percent best-case (LCROSS Cabeus) / ~1 percent average; ore-grade ratio 18× best-case / ~100× average. The 4.6-kilometres-per-second figure is the no-conservative upper bound for the lunar accounting; the pitch can quote 6 kilometres-per-second only if it explicitly restricts to no-aerobraking. Pitch-text correction is `SATURN-PUNCH-LIST-20260521.md` item P-2 (deferred per project-owner direction 2026-05-21).

**2026-05-22 latest+20 (hyperion R-pitch-arithmetic-audit `f9f7fc2`):** the pitch §2 ΔV budget post-punch-list-edits is still wrong, but in a different way than P-1 (75 percent → 54 percent — the symptom was halved but the disease preserved). **The load-bearing post-edit fail is Saturn departure at 1.5 km/s**, which is physically impossible from a circular B-ring orbit (v_circ 18 km/s; escape alone 7.5 km/s; this axis's vis-viva anchors are 5.5-7.7 km/s). The 1.5 km/s figure is the result of impulsively accounting a low-thrust electric leg that should be continuous-thrust per this axis's first-principles framing. Output of the error: a 54-percent delivered-fraction claim where the honest figure is 17-28 percent. Five-edit `PROPOSED-PITCH-DIFF.md` shipped at `water-prop/rounds/R_pitch_arithmetic_audit/`; D-1 fixes the Saturn-departure number, D-2/D-3/D-4 cascade the delivery fraction + round-trip + lunar comparison with a new continuous-thrust footnote that makes the impulsive-vs-continuous frame explicit. Methodology-lesson candidate from the round: *correcting a flagged number without re-deriving its inputs preserves the error class.*

## Open question

Closed.

## Last touched by

- hyperion R-variant-B-impulsive-vs-continuous — `e6467ab`
- titan R-inbound-dv-continuous-thrust — `58581fb`
- titan-3 R-delta-velocity-anchor-audit — `42120cf`
- Saturn worker assumption-audit gap-filler — `030cb5e`

## HISTORY

### 2026-05-15 — Initial scaffold from `ARCHITECTURE-DECISION-MATRIX.md` current-decision-state table

Status: closed. Confidence: high.

Current state and open question captured from the matrix's top section as of commit `9704700`. Full audit trail of how this axis arrived at its current state is in the matrix HISTORY section (`water-prop/docs/ARCHITECTURE-DECISION-MATRIX.md`).

---

<!-- Append-only HISTORY entries go below this line. Each entry: ### YYYY-MM-DD — round-name or commit-hash — one-line summary -->

### 2026-05-19 latest+13 — titan-3 R-delta-velocity-anchor-audit (`42120cf`) — two additional anchors corrected via vis-viva

Triggered by user direction "question your assumptions" mid-session after R-chemical-electric-leapfrog. Two unverified delta-velocity anchors had propagated across multiple prior rounds. Vis-viva re-derivation: Saturn-departure 5.5 → 7.7 kilometres-per-second (Hohmann v∞ at Saturn 6.21 kilometres-per-second; elliptical parking with B-ring apoapsis 107,000 kilometres from Saturn centre and Oberth-optimised periapsis 60,000 kilometres just above clouds; periapsis burn 36.1 − 28.4 = 7.7 kilometres-per-second). Earth-arrival chemical capture 3.5 → 7.3 kilometres-per-second direct from Hohmann v∞ 10.3 kilometres-per-second to low Earth orbit, OR 4.2 kilometres-per-second after R12 10-flyby lunar-gravity-assist tour. Combined effect on commercial 200-tonne chunk: chemical propellant burden rises ~38 tonnes (Saturn departure) + 0-32 tonnes (Earth capture, scenario-dependent). At commercial scale, retracts the prior-round 13-cells leapfrog headline. Methodology lesson 20 candidate (vis-viva-default anchoring when no primary-text source). Status held at closed; the audit reinforces the closed reading at corrected anchors.

### 2026-05-21 latest+15 — Saturn worker assumption-audit gap-filler (`030cb5e`) — lunar-LEO ~4.6 km/s with aerobraking added; source-concentration framing replaces "6 km/s forever tax"

Wonder + reason gap-filler dispatch on belief `8be3ec81e5902bf4`. The pitch had carried "lunar surface to low-Earth orbit is ~6 km/s of Δv out of a gravity well, every tonne, forever" as a lunar-versus-ICEBERG comparator. Correct value with aerobraking is ~4.6 kilometres-per-second (1.87 ascent + 5.93 low-lunar-orbit-to-low-Earth-orbit minus 3.2 aerobraking savings per Wikipedia delta-v-budget table). The lunar case loses on per-tonne Δv when aerobraking is admitted; the right framing is **source concentration** — Saturn B-ring 99.7-99.8% water (Cassini microwave radiometry, locked belief `c646b3c6`) versus lunar polar 5.6 ± 2.9% best-case / ~1% average; ore-grade ratio 18× to 100× advantage for Saturn-ring. Pitch-text correction is punch-list item P-2; deferred per project-owner direction 2026-05-21. Status held at closed; the new anchor is additive (the corrected Saturn-side anchors from latest+13 remain authoritative for Saturn-side Δv accounting).
