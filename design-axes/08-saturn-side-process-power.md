---
axis: "Saturn-side process power"
status: open
confidence: medium
last_revised: 2026-05-15
related:
  - "[[surviving-cell]]"
  - "[[reactor-power-floor]]"
---

# Saturn-side process power

## Current

Required ~150 kilowatt-electric for inbound electrolysis if Variant B / Architecture D. Architecture E (pure all-electric end-to-end) drops this dependency entirely.

## Open question

If Architecture E is adopted: zero Saturn-side process power required. **Architecture D as a path is closed:** rhea R-architecture-D-cost (`a4d163d`) shows both D-fission and D-solar-thermal are structurally money-losing at zero discount rate — even before applying any cost-of-capital hurdle, the program loses money. Solar-thermal's credibility advantage over fission (2.0 vs 0.78 percent posterior) is moot if neither cell pays for itself at zero cost-of-capital.

## Last touched by

- rhea R-architecture-D-cost — `a4d163d` (closes Architecture D economically)
- enceladus-r5 R-fission-surface-power-stretch-credibility — `7cb39c2`
- enceladus-r5 R-saturn-side-solar-thermal — `0fcab42`
- enceladus-r5 R-architecture-E — `448505e`

## HISTORY

### 2026-05-15 — Initial scaffold from `ARCHITECTURE-DECISION-MATRIX.md` current-decision-state table

Status: open. Confidence: medium.

Current state and open question captured from the matrix's top section as of commit `9704700`. Full audit trail of how this axis arrived at its current state is in the matrix HISTORY section (`water-prop/docs/ARCHITECTURE-DECISION-MATRIX.md`).

---

<!-- Append-only HISTORY entries go below this line. Each entry: ### YYYY-MM-DD — round-name or commit-hash — one-line summary -->

### 2026-05-15 — R-architecture-D-cost (commit `a4d163d`) — Architecture D economically closed: both variants money-losing at zero discount rate
