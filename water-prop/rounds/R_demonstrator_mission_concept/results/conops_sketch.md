# Demonstrator concept-of-operations sketch

Scaled-down per REQUIREMENTS §7.5 (demonstrator-class: any non-zero delivered mass; L0-04/05/06/07/08/09 do not apply). Populated with this session's three bet-audit numbers, superseding the placeholder values in the 2026-05-21 SCOPE (which predated the audits).

## Vehicle and mission

| Element | Demonstrator value | Note vs SCOPE |
|---|---|---|
| Vehicle dry mass | 4–6 t | per SCOPE |
| Launch to low-Earth orbit | 15–30 t (one Falcon Heavy partial-reuse) | per SCOPE |
| Target chunk at Saturn | 5–10 t | per SCOPE (proves capture at small scale) |
| Delivered to low-Earth orbit | 1–3 t (any non-zero, §7.5) | per SCOPE |
| Round-trip | 12–15 yr (L0-05 relaxed but worth honoring) | per SCOPE |
| Power | RTG ~1–3 kW, or solar-inner + RTG-Saturn hybrid | bet #3 deferred — non-nuclear |
| **Propulsion (test article)** | **commercial water RF-ion (2000 s) + bag sublimation-distillation filtration stack** | **CORRECTED from SCOPE's "water-MET ≥700 s"** — see thruster-mismatch constraint below |
| Chunk capture (test article) | single-pass trawl, full telemetry, mm/s closing | per SCOPE |

## The thruster-mismatch constraint (new; corrects the SCOPE)

A small low-power demonstrator (RTG ~1–3 kW, 5–10 t chunk) would, on power-optimal grounds (R6: optimal Isp ≈ 543 s at Kilopower-class power), *naturally* fly a water-MET at ~500–650 s. The SCOPE assumed exactly this ("water-MET ≥700 s … this IS bet 2's experiment").

**But the commercial architecture does not close on MET.** R-water-electrothermal-flight-scale-audit (bet #2) showed MET at realistic continuous flight (500–700 s) gives 0–0.5% matrix closure; the closure cells run **2000 s RF-ion**, which is contamination-*sensitive* and depends on the bag's silicate rejection holding for months. **Therefore, to retire commercial bet #2, the demonstrator must fly the commercial RF-ion + bag-filtration stack on dirty chunk water — not the power-appropriate MET.** A demonstrator that flies MET (simpler for its own propulsion needs) would prove water-electrothermal works in deep space but would *not* retire the contamination-sensitive RF-ion-continuous bet the commercial matrix actually rests on.

This is the single most important CONOPS design decision the demonstrator faces, and it is the kind of architecture-branch the SCOPE could not see before the bet-2 audit existed.

## Bet → experiment mapping

| Bet | Demonstrator experiment | Retires |
|---|---|---|
| #1 chunk capture | (a) Earth-orbit catch-and-contain proxy with deployable target mass (pre-cruise) → (b) Saturn small-chunk capture with full telemetry | (a) deployment + catch + containment at mm/s; (b) rendezvous + short-duration survive |
| #2 water-electrothermal | continuous-months RF-ion run on bag-filtered chunk water; Isp telemetry; resonant-cavity/grid erosion inspection at Earth return | the duration + contamination flight gap (144–1461× over flown precedent) |
| #3 reactor | NOT on demonstrator — fly non-nuclear; reactor retired separately / by NASA FSP | (deferred) |

## Why fly non-nuclear (bet #3 deferred)

R-kilopower-scale-up-credibility: the reactor bet has ≤1.5% delivery probability by 2035 and is not ICEBERG-controllable. Bundling it into the demonstrator would re-couple the program to the external FSP-2 award — exactly the dominant external kill-gate the re-gating removes. A non-nuclear demonstrator (RTG / solar-hybrid) retires bets #1 and #2 — the two ICEBERG *can* control — without waiting on the reactor.
