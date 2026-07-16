---
axis: "Pitch / capital framing"
status: open
confidence: high
last_revised: 2026-05-22
related:
  - "[[program-class]]"
  - "[[surviving-cell]]"
---

# Pitch / capital framing

## Current

Sovereign + strategic-corporate + infrastructure-fund. Venture-class framing retired (was already flagged in the eleven-round pass; now flagged as structural, not just current-conservative-reading, per titan-2 R-HE-graze-feasibility).

**2026-05-22 latest+20 — pitch rewrite UNBLOCKED on H7; concrete diff awaits ratification.** Two pitch-side audits land jointly. **R-pricing-anchor-revisit (titan-5 `1023a45`)** finds the $1,400/kg pitch anchor understates defensible willingness-to-pay by 2-150×, but correcting it does NOT change the program-class verdict (H6 falsified; binding constraint is reactor-program availability L0-24, not revenue/kg). Recommended §4/§9 restatement as a band: Earth-launch displacement ($1,400-3,000/kg) FLOOR; lunar in-situ-resource-utilisation (~$1,000/kg at scale) competing-supply ceiling; mission-essential willingness-to-pay ($5-25k+/kg crewed / geostationary / Department-of-Defense) operative blended band. **R-pitch-arithmetic-audit (hyperion `f9f7fc2`)** finds the §2 ΔV budget is the load-bearing arithmetic fail (Saturn departure listed 1.5 km/s versus defensible 5.5-7.7 km/s; impulsive accounting on low-thrust electric legs; 54-percent delivered-fraction claim where honest figure is 17-28 percent). Five-edit `PROPOSED-PITCH-DIFF.md` shipped at `water-prop/rounds/R_pitch_arithmetic_audit/` (D-1 Saturn departure load-bearing; D-2/D-3/D-4 cascade; D-5 §6 reconciliation independent). **Do NOT auto-apply the diff** — project-owner ratifies. **§4 revenue numbers held** until M-3 revenue re-run against corrected 17-28-percent anchor (now unblocked by R-framework-matrix-parity). Program-class verdict UNCHANGED by either round; both corroborate that the binding constraint is upstream (reactor + bets #1+#2), not the pitch itself.

## Open question

Full pitch rewrite still queued. Reader-notes-only at top of `ICEBERG-pitch.md` flag the falsifications; prose body unchanged.

## Last touched by

- titan-2 R-HE-graze-feasibility — `b2e7a35`
- worktree-110450 R-reactor-roadmap — `e9ab1ba`
- titan-5 R-pricing-anchor-revisit — `1023a45` (latest+20; H7 held — pitch rewrite unblocked; pricing-band recommendation; H6 falsified)
- hyperion R-pitch-arithmetic-audit — `f9f7fc2` (latest+20; §2 ΔV is load-bearing fail; 54% delivered → honest 17-28%; PROPOSED-PITCH-DIFF.md shipped)

## HISTORY

### 2026-05-15 — Initial scaffold from `ARCHITECTURE-DECISION-MATRIX.md` current-decision-state table

Status: open. Confidence: high.

Current state and open question captured from the matrix's top section as of commit `9704700`. Full audit trail of how this axis arrived at its current state is in the matrix HISTORY section (`water-prop/docs/ARCHITECTURE-DECISION-MATRIX.md`).

---

<!-- Append-only HISTORY entries go below this line. Each entry: ### YYYY-MM-DD — round-name or commit-hash — one-line summary -->

### 2026-05-22 latest+20 — titan-5 R-pricing-anchor-revisit (`1023a45`) + hyperion R-pitch-arithmetic-audit (`f9f7fc2`) — pitch rewrite UNBLOCKED on both load-bearing blocks

**R-pricing-anchor-revisit** is the long-carried "pitch rewrite block (H7)" round. H7 HELD: the pitch rewrite is unblocked. The project-owner challenge ("$1,400/kg is too low") is correct in direction — $1,400/kg is the Falcon Heavy launch-displacement floor and sits below the blended realised price in the two near-term eras ($3.6-5.0k/kg at 100 tonnes/yr; $1.6-2.2k/kg at 1,000 tonnes/yr) and far below mission-essential willingness-to-pay (International-Space-Station-Commercial-Resupply $26-125k/kg; Orbit Fab geostationary-Earth-orbit $200k/kg). H6 (the "price correction flips program-class verdict" hypothesis) falsified — load-bearing financial rounds already assume $10k/kg ABOVE the defensible blended band, so correcting the pitch anchor moves the campaign's assumption the wrong way. Binding constraint remains reactor-program availability (L0-24), not revenue per kilogram. Recommended §4/§9 pitch restatement: floor/ceiling/operative-band framing — Earth-launch displacement ($1,400-3,000/kg) FLOOR; lunar in-situ-resource-utilisation (~$1,000/kg at scale) competing-supply ceiling; mission-essential willingness-to-pay ($5-25k+/kg) operative blended band. Inverse-risk follow-on flagged: re-run R-reactor-roadmap + R-delivery-irr-curve + R-variant-B-recovery-paths at the defensible $3.6-5k near-term band to confirm no verdict is propped up by the generous $10k anchor.

**R-pitch-arithmetic-audit** audits the pitch's quantitative claims after the punch-list pre-edits (punch-list S-3). 35 claims audited; 21 survive; 4 hard fails (all one root cause); 1 framing fail; 5 downstream/already-flagged; 1 blocked. The §2 ΔV budget is the load-bearing fail: Saturn departure listed at 1.5 km/s — physically impossible from circular B-ring (v_circ 18 km/s; escape alone 7.5 km/s; campaign vis-viva anchors 5.5-7.7 km/s). Low-thrust electric legs priced impulsively. Output: 54-percent delivered-fraction claim where the honest figure is 17-28 percent. This is the SAME error class punch-list P-1 (75 percent) flagged; the 75 → 54 edit halved the symptom but kept the disease. PROPOSED-PITCH-DIFF.md shipped at `water-prop/rounds/R_pitch_arithmetic_audit/` with five edits (D-1 Saturn departure 1.5 → 5.5-7.7 km/s, D-2/D-3/D-4 cascade, D-5 §6 revenue-stream reconciliation). Do NOT auto-apply — project-owner ratifies. Hold §4 revenue numbers until M-3 revenue re-run against corrected 17-28-percent anchor (M-3 now unblocked by R-framework-matrix-parity).

Status held at open / high. Resolution gated on project-owner ratification of `PROPOSED-PITCH-DIFF.md` D-1 through D-5 plus pricing-band restatement.
