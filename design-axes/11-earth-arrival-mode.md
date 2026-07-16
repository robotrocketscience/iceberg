---
axis: "Earth-arrival mode"
status: falsified
confidence: high
last_revised: 2026-05-18
related:
  - "[[surviving-cell]]"
  - "[[round-trip-ceiling]]"
---

# Earth-arrival mode

## Current

**Atmospheric-capture is structurally closed at conservative anchors.** Aerocapture is necessary for any surviving cell (hyperion R-no-atmospheric-capture-baseline `1ce7c89`, kill-shot, 0/288 without aerocapture). Single-pass aerocapture closed (hyperion R-aerocapture-fast-cruise-envelope at engineering level; phoebe R-chunk-as-heat-shield-revisit `9b3d29e` at ICEBERG ballistic coefficients 4600-6600 kg/m²). **Hybrid aerocapture + multi-pass aerobraking closed** (phoebe R-hybrid-aerocapture-aerobraking `1623cca`, 2026-05-16 merge `b5c5d61`: 0 of 1920 cells under conservative anchors (US Standard 1976 atmosphere, ice tensile 1.0 MPa, boundary-layer-blocking 0.4, body-absorbed 0.5); three independent failure modes — pass-1 chunk shatter, aerobraking unphysical timescale, sublimation consumes chunk). Megawatt-scale aerocapture engineering closes per rhea R-megawatt-aerocapture-engineering-closure but rests on a megawatt all-electric stack that fails on other axes. **Drag-skirt is the only remaining within-chunk-rendezvous recovery candidate** (phoebe-named) but is downstream of axis-19 retire-decision.

## Open question

Atmospheric-capture closed. Within-chunk-rendezvous, only R-deployable-drag-skirt (phoebe-named) remains as an architectural-recovery candidate, and it is downstream of axis-19 retire-decision. Outside chunk-rendezvous, Earth-arrival mode is a per-pivot question in R-mission-architecture-pivot-survey (catcher-at-Saturn return-tug never crosses high-energy atmosphere; processor-at-Saturn returns lower-mass products with different ballistic profile; alternative-source vehicles may have different mass ratios).

## Last touched by

- hyperion R-no-atmospheric-capture-baseline — `1ce7c89` (kill-shot)
- hyperion R-hybrid-aerocapture-aerobraking SCOPE — `6ef36eb` (now run)
- hyperion R-aerocapture-fast-cruise-envelope — `203d351`
- rhea R-megawatt-aerocapture-engineering-closure — `38bd198`
- phoebe R-chunk-as-heat-shield-revisit — `9b3d29e` (single-pass closed)
- phoebe R-hybrid-aerocapture-aerobraking — `1623cca` (hybrid closed; merge `b5c5d61`)

## HISTORY

### 2026-05-15 — Initial scaffold from `ARCHITECTURE-DECISION-MATRIX.md` current-decision-state table

Status: open. Confidence: medium.

Current state and open question captured from the matrix's top section as of commit `9704700`. Full audit trail of how this axis arrived at its current state is in the matrix HISTORY section (`water-prop/docs/ARCHITECTURE-DECISION-MATRIX.md`).

---

<!-- Append-only HISTORY entries go below this line. Each entry: ### YYYY-MM-DD — round-name or commit-hash — one-line summary -->

### 2026-05-15 — R-no-atmospheric-capture-baseline (commit `1ce7c89`) — kill-shot: zero surviving cells without aerocapture across 288-cell sweep

Aerocapture confirmed necessary for any surviving cell at conservative anchors. Status bumped open / medium → open / high. Sole open architectural-recovery candidate is hybrid aerocapture-aerobraking (SCOPE `6ef36eb`, not yet run).

### 2026-05-18 latest+8 — phoebe R-hybrid-aerocapture-aerobraking (commit `1623cca`, merge `b5c5d61`) — atmospheric-capture structurally closed

0 of 1920 cells in the architecturally-relevant envelope close under conservative anchors (US Standard 1976 atmosphere, ice tensile 1.0 MPa, boundary-layer-blocking 0.4, body-absorbed 0.5). Three independent failure modes mutually exclusive across the periapsis axis: pass-1 chunk shatter at any altitude where pass-1 Δv ≥ 4.18 km/s (chunk stress > 1 MPa tensile); aerobraking unphysical timescale at any altitude where chunk T_eq < ice melt point (need ≥ 180 km, where pass count ≥ 3 million and time ≥ 700 yr); sublimation consumes chunk at any altitude where time is tractable (≤ 130 km, 259-1486 t chunk loss vs 100 t tolerance for a 200-t chunk). The 'deep, tractable, low-loss' interior solution does not exist. Three SCOPE input-assumption errors documented (β-by-chunk-size non-monotonic; pass-1 Δv set by parabolic-velocity not engineering judgment; single-scale-height exponential atmosphere wrong above 110 km). Status flipped open / high → falsified / high. Drag-skirt is the residual recovery candidate but downstream of axis-19 retire-decision.

### 2026-05-18 latest+11 — phoebe R-hybrid-chemical-power-augmentation (`a969aa6`) — aerocapture-credit lever foreclosed even at hybrid-chemical architecture

Phoebe's R-hybrid-chemical-power-augmentation sweep stripped aerocapture_credit = 0 km/s (the audit-conditional anchor inheriting from falsified R-hybrid-aerocapture-aerobraking) as one of three audit-conditional axes. The 54 raw joint-demonstrator-passing cells under charitable flags collapse to 0 after the strip. Atmospheric-capture closure remains structurally closed without an architectural pivot; axis status unchanged at falsified/high.

Plus methodology improvement: lesson 12 candidate surfaced (conditional-axis stripping discipline) — when a SCOPE inherits axes from upstream-falsified architectures, report results with and without those axes side-by-side. PROTOCOL.md amendment candidate pending project-owner ratification.
