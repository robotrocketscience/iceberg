---
axis: "Saturn-orbit-insertion delta-velocity"
status: closed
confidence: high
last_revised: 2026-05-15
related:
  - "[[12-saturn-side-capture-mode]]"
  - "[[13-outbound-launch-architecture]]"
---

# Saturn-orbit-insertion delta-velocity

## Current

**0.8 km/s** including margin. Saturn-orbit-insertion at v∞ = 5.44 km/s with sub-D-ring periapsis (63,000 km) costs ~0.71 km/s for a single burn into an ellipse with apoapsis 3 r_titan; a 2-Titan-tour over ~30–50 days pumps periapsis to B-ring outer (~92,000 km) at zero additional propulsive. Down from 1.55 km/s direct chemical baseline; down from 1.24 km/s prior matrix placeholder. Sub-D-ring saves only 76–99 m/s vs Cassini-depth periapsis — Cassini already extracted nearly all the available Oberth benefit.

**Argument-of-periapsis must lock at trans-Saturn-injection** to place ring-plane crossings in the F-G gap. Post-arrival argument-trim costs ≥100 m/s per 10 degrees rotation (845 m/s for 90°), so arrival geometry cannot be fixed post-hoc. This is a constraint on heliocentric trajectory design, not a Saturn-side cost.

## Open question

Closed at conservative anchor. Cost flows back to the trans-Saturn-injection burn as a constraint on heliocentric trajectory design (argument-of-periapsis lock).

## Last touched by

- titan-2 R-saturn-soi-periapsis-depth — `1b1b889`

## HISTORY

### 2026-05-15 — titan-2 R-saturn-soi-periapsis-depth (`1b1b889`) — initial scaffold

Axis created during the post-kill-shot three-handoff integration pass (matrix commit `ceafb9d`). Saturn-orbit-insertion delta-velocity was a free placeholder on the matrix prior to this round; titan-2's R-saturn-soi-periapsis-depth set the value at 0.8 km/s and surfaced the trans-Saturn-injection argument-of-periapsis lock as a constraint on heliocentric design.

Round also surfaced an orthogonal finding (B-ring rendezvous crossings 99 percent per-pass impact probability under zone-averaged optical-depth ~ 2) which lives on axis 12 (Saturn-side capture mode), not here — that risk is on the rendezvous, not the insertion.

---

<!-- Append-only HISTORY entries go below this line. Each entry: ### YYYY-MM-DD — round-name or commit-hash — one-line summary -->
