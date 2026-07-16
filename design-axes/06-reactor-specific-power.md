---
axis: "Reactor specific power assumption"
status: closed
confidence: high
last_revised: 2026-05-19
related:
  - "[[radiator-mass-model]]"
  - "[[reactor-power-floor]]"
  - "[[chunk-mass-cap]]"
---

# Reactor specific power assumption

## Current

Conservative: 10 watts-per-kilogram. The 40 W/kg target referenced in earlier matrix versions is Technology-Readiness-Level-2 paper aspiration; flown radioisotope thermoelectric generators top out at ~5.3 W/kg; KRUSTY measured ~2.4 W/kg system-level.

## Open question

Closed at the conservative anchor.

## Last touched by

- rhea R-megawatt-marvl-radiator — `bde06a2`
- R-power-wonder finding 1 (user-locked external evidence)
- titan-3 R-chunk-size-pareto — `1997a51`

## HISTORY

### 2026-05-15 — Initial scaffold from `ARCHITECTURE-DECISION-MATRIX.md` current-decision-state table

Status: closed. Confidence: high.

Current state and open question captured from the matrix's top section as of commit `9704700`. Full audit trail of how this axis arrived at its current state is in the matrix HISTORY section (`water-prop/docs/ARCHITECTURE-DECISION-MATRIX.md`).

---

<!-- Append-only HISTORY entries go below this line. Each entry: ### YYYY-MM-DD — round-name or commit-hash — one-line summary -->

### 2026-05-19 latest+13 — titan-3 R-chunk-size-pareto (`1997a51`) — Kilopower-measured 2.4 W/kg closes at P=30 kilowatt-electric with 40-80 tonne chunks

Test of both Kilopower-measured (2.4 watts-per-kilogram) and R12-optimistic (10 watts-per-kilogram) at chunk 10-200 tonnes × reactor 10-30 kilowatt-electric, corrected vis-viva delta-velocity anchors, R12 lunar-gravity-assist Earth-arrival. Both specific-power anchors close the same strict band (50-60 tonnes at P=30 kilowatt-electric) and similar waiver bands. The closure is NOT sensitive to the specific-power anchor at P=30 kilowatt-electric (reactor mass at 2.4 watts-per-kilogram is 12.5 tonnes at P=30 kilowatt-electric, vs 3.0 tonnes at 10 watts-per-kilogram; the 9.5-tonne penalty fits inside the 40-80 tonne chunk budget margin). What IS sensitive is reactor power class — closure requires P=30 kilowatt-electric; P=10-20 kilowatt-electric does not close strict L0-05. Specific-power as anchor of record stays closed; the load-bearing axis is now reactor power floor (axis 05).
