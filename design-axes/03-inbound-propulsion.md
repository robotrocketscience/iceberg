---
axis: "Inbound propulsion choice"
status: closed
confidence: high
last_revised: 2026-05-22
related:
  - "[[inbound-dv-accounting]]"
  - "[[outbound-launch-architecture]]"
---

# Inbound propulsion choice

## Current

All-electric end-to-end. Chemical-trim at Earth capture is falsified as a Variant-B saver (chemical exhaust velocity 4.41 km/s is 4.45x lower than electric 19.62 km/s; smaller chemical burn eats more propellant than the larger electric burn it replaces).

**2026-05-22 latest+18 — bet #2 audit + demonstrator-mission concept ammend electric-thruster choice with an architecture-trap finding:** the matrix's closure cells run at Isp 2000 s (RF-ion class), which closes the matrix on Isp but is **contamination-SENSITIVE on Saturn-ring water** (hyperion R-water-electrothermal-flight-scale-audit `cd8d753`). Microwave-Electrothermal-Thruster (the contamination-tolerant thruster a Kilopower-class small vehicle would naturally fly) at realistic continuous flight 500-700 s gives 0-0.5 percent matrix closure (the 800-s ground/pulse A1 anchor is above the campaign's own R0 continuous ceiling and yields only 4 percent). The two requirements pull against each other; continuous-months flight-readiness on Saturn-ring water at matrix-closing Isp is a conjunction 0.48 mid (0.25-0.73 range), un-flown. Flight gap 144-1461× cumulative operating time versus closest flown precedent. **Demonstrator implication (R-demonstrator-mission-concept `61afe0c`):** the demonstrator must fly the commercial water RF-ion (2000 s) + bag sublimation-distillation filtration stack on dirty chunk water, NOT the power-appropriate MET (~543 s) a small low-power vehicle would naturally fly. MET would prove water-electrothermal in deep space but would not retire the contamination-sensitive RF-ion-continuous bet the commercial matrix actually rests on. Status remains closed on the chemical-vs-electric question; the electric-thruster sub-choice (RF-ion vs MET) is now load-bearing on the demonstrator's bet-#2 retirement.

## Open question

Closed.

## Last touched by

- rhea R-chemical-trim-vs-all-electric-earth-arrival — `47b69bc`
- hyperion R-water-electrothermal-flight-scale-audit — `cd8d753` (bet #2 architecture trap: RF-ion 2000 s closes Isp but is contamination-sensitive; MET 500-700 s tolerates Saturn-water silicates but does not close on Isp)
- hyperion R-demonstrator-mission-concept — `61afe0c` (demonstrator must fly commercial RF-ion + bag filtration, not power-appropriate MET)

## HISTORY

### 2026-05-15 — Initial scaffold from `ARCHITECTURE-DECISION-MATRIX.md` current-decision-state table

Status: closed. Confidence: high.

Current state and open question captured from the matrix's top section as of commit `9704700`. Full audit trail of how this axis arrived at its current state is in the matrix HISTORY section (`water-prop/docs/ARCHITECTURE-DECISION-MATRIX.md`).

---

<!-- Append-only HISTORY entries go below this line. Each entry: ### YYYY-MM-DD — round-name or commit-hash — one-line summary -->

### 2026-05-22 latest+18 — hyperion R-water-electrothermal-flight-scale-audit (`cd8d753`) + R-demonstrator-mission-concept (`61afe0c`) — electric-thruster sub-choice (RF-ion vs MET) becomes load-bearing on bet #2 retirement

Audit finds bet #2 (continuous water-electrothermal at flight scale on Saturn-water purity) fails as an architecture trap, not a physics wall. Contamination-tolerant MET at realistic continuous flight 500-700 s gives 0-0.5 percent matrix closure (the 800-s ground/pulse A1 anchor is above the campaign's own R0 continuous ceiling and yields only 4 percent). Isp-sufficient RF-ion at 2000 s closes the matrix on Isp but is contamination-SENSITIVE; continuous-months flight-readiness on Saturn-ring water is a conjunction (bag silicate-rejection holds) × (cathode/grid life ≥ burn) × (no anomaly) = 0.48 mid (0.25-0.73 range), un-flown. Flight gap 144-1461× cumulative operating time versus closest flown precedent (Momentus Vigoride-5 water-MET 2023 orbit-raising; AQUARIUS 91-s water resistojet in deep space).

R-demonstrator-mission-concept synthesises: demonstrator must fly commercial water RF-ion (2000 s) + bag sublimation-distillation filtration stack on dirty chunk water, NOT power-appropriate MET (~543 s) a small low-power vehicle would naturally fly. MET would prove water-electrothermal in deep space but would not retire the contamination-sensitive RF-ion-continuous bet the commercial matrix actually rests on. This is the most-consequential design decision the demonstrator faces; the SCOPE pre-audit assumed MET and was corrected by the bet-#2 audit landing.

Status remains closed on chemical-vs-electric. Sub-choice (RF-ion vs MET) is load-bearing on the demonstrator's bet-#2 retirement path. Locked beliefs `650938e3` (A1 800-s anchor) and `5535179f` (bet #2 framing) surfaced for project-owner update.
