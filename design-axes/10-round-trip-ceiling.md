---
axis: "Round-trip ceiling (L0-05)"
status: open
confidence: high
last_revised: 2026-05-19
related:
  - "[[program-class]]"
  - "[[surviving-cell]]"
  - "[[cruise-trajectory]]"
  - "[[chunk-mass-cap]]"
---

# Round-trip ceiling (L0-05)

## Current

15 years strict. Variant C and Architecture E both miss strict L0-05; Architecture E was retired anyway under flown-anchored specific power (enceladus-r5 `62f7079`). **2026-05-19 latest+13 (titan-3 R-chunk-size-pareto `1997a51`):** at 40-80 tonne chunks + 30 kilowatt-electric Kilopower-extrapolation + R12 lunar-gravity-assist Earth-arrival, 4 cells close L0-05 strict (50-60 tonne chunks; round-trip 14-15 years; delivered 30-37 tonnes per mission). 30 cells close L0-05 waiver across 50-150 tonne chunks / 20-30 kilowatt-electric / round-trip 14-22 years / delivered 30-60 tonnes per mission. Strict closure exists physically but only at the smallest closing chunk band — commercial value reduces to 30-37 tonnes per mission, near the L0-09 floor.

## Open question

Project-owner decision (amended 2026-05-19 latest+13): hold L0-05 strict at 15 years and accept the narrow 50-60 tonne / 30-37 tonne-delivered closure cell, OR admit waiver to ≥ 25 years and unlock the broader 50-150 tonne / 30-60 tonne-delivered band. Architecture E's prior 50 tonnes-at-25-years framing is moot per Architecture E falsification and the 500 kilowatt-electric retirement; the live decision is between strict vs waiver under the titan-3 closure cell.

## Last touched by

- enceladus-r5 R-architecture-E — `448505e` [Architecture E falsified]
- hyperion R-cruise-time-optimization — `db249ba`
- titan-3 R-chunk-size-pareto — `1997a51`

## HISTORY

### 2026-05-15 — Initial scaffold from `ARCHITECTURE-DECISION-MATRIX.md` current-decision-state table

Status: open. Confidence: high.

Current state and open question captured from the matrix's top section as of commit `9704700`. Full audit trail of how this axis arrived at its current state is in the matrix HISTORY section (`water-prop/docs/ARCHITECTURE-DECISION-MATRIX.md`).

---

<!-- Append-only HISTORY entries go below this line. Each entry: ### YYYY-MM-DD — round-name or commit-hash — one-line summary -->

### 2026-05-19 latest+13 — titan-3 R-chunk-size-pareto (`1997a51`) — strict L0-05 closes at narrow 50-60 tonne chunk band; waiver closes broader 50-150 tonne band

Under the 500 kilowatt-electric retirement + corrected vis-viva delta-velocity anchors + R12 lunar-gravity-assist Earth-arrival, the strict 15-year ceiling closes at 4 cells (50-60 tonne chunks / P=30 kilowatt-electric / both Kilopower-measured 2.4 watts-per-kilogram and R12-optimistic 10 watts-per-kilogram). Delivered 30-37 tonnes per mission, just above L0-09 floor. Waiver to 25 years adds 30 cells across 50-150 tonne chunks / 20-30 kilowatt-electric / delivered 30-60 tonnes. Strict-vs-waiver decision is now meaningful (both have non-empty closures); the gain from waiver is broader chunk-mass band and higher per-mission delivered mass at the cost of an additional 7-10 years of mission duration. Status held at open / high pending project-owner decision.
