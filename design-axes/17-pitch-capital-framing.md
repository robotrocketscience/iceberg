---
axis: "Pitch / capital framing"
status: open
confidence: high
last_revised: 2026-07-21 (latest+25)
related:
  - "[[program-class]]"
  - "[[surviving-cell]]"
  - "[[10-round-trip-ceiling]]"
---

# Pitch / capital framing

## Current

Sovereign + strategic-corporate + infrastructure-fund. Venture-class framing retired (was already flagged in the eleven-round pass; now flagged as structural, not just current-conservative-reading, per titan-2 R-HE-graze-feasibility).

**2026-05-22 latest+20 — pitch rewrite UNBLOCKED on H7; concrete diff awaits ratification.** Two pitch-side audits land jointly. **R-pricing-anchor-revisit (titan-5 `1023a45`)** finds the $1,400/kg pitch anchor understates defensible willingness-to-pay by 2-150×, but correcting it does NOT change the program-class verdict (H6 falsified; binding constraint is reactor-program availability L0-24, not revenue/kg). Recommended §4/§9 restatement as a band: Earth-launch displacement ($1,400-3,000/kg) FLOOR; lunar in-situ-resource-utilisation (~$1,000/kg at scale) competing-supply ceiling; mission-essential willingness-to-pay ($5-25k+/kg crewed / geostationary / Department-of-Defense) operative blended band. **R-pitch-arithmetic-audit (hyperion `f9f7fc2`)** finds the §2 ΔV budget is the load-bearing arithmetic fail (Saturn departure listed 1.5 km/s versus defensible 5.5-7.7 km/s; impulsive accounting on low-thrust electric legs; 54-percent delivered-fraction claim where honest figure is 17-28 percent). Five-edit `PROPOSED-PITCH-DIFF.md` shipped at `water-prop/rounds/R_pitch_arithmetic_audit/` (D-1 Saturn departure load-bearing; D-2/D-3/D-4 cascade; D-5 §6 reconciliation independent). **Do NOT auto-apply the diff** — project-owner ratifies. **§4 revenue numbers held** until M-3 revenue re-run against corrected 17-28-percent anchor (now unblocked by R-framework-matrix-parity). Program-class verdict UNCHANGED by either round; both corroborate that the binding constraint is upstream (reactor + bets #1+#2), not the pitch itself.

**2026-07-21 latest+25 — A MARKET/ECONOMICS BET SURFACES BENEATH THE THREE ENGINEERING BETS (R188 `R_clearing_price_time_path`).** R183 (`R_waiver_value_consolidation`) swept water-price decay as a free parameter and flagged that it had *no campaign anchor*; R188 supplied it from external data (the launch-cost experience curve, [PNAS Nexus](https://academic.oup.com/pnasnexus/article/5/7/pgag217/8732400)). The load-bearing structure: ICEBERG sells water at a destination, and at any **Earth-accessible** destination (LEO/cislunar) the clearing price is capped by the cheapest substitute — Earth-launched propellant (~$3,000-4,000/kg in LEO, 2025) — whose cost is on a steep experience curve ($3,868 → ~$273/kg 2025-2040). That gives a delivered-water price decline of **9-18 %/yr (central ~13 %)**, which is **3-6× the 3 %/yr decay R183 showed already sinks the waiver NPV**, and — the decisive fact — **the decline rate alone exceeds both campaign hurdles (8 % utility, 10 % growth)**. Over the mission's own 13-23-yr decision-to-delivery timeline the substitute price falls 3-63×, so revenue is discounted faster by the market than by capital (23.5-yr revenue discount factor < 1 %). The one regime immune to this is a **deep-space** destination where Earth launch pays the full rocket-equation penalty (substitute 10-90× LEO), but that market needs outer-system demand absent in the window and itself gated on cheap launch. **The dilemma is structural: ICEBERG's water is either sold cheap (LEO, into a substitute racing away) or dear (deep space, to customers who do not exist)** — an economics/market bet that sits *beneath* the three engineering bets, not beside them. This does not falsify the engineering (the locked matrix verdict brackets economics by construction), and it does not overturn the prior pitch verdict (binding constraint is still upstream) — but it means **the pitch cannot rest the revenue case on a stable delivered-water price; the launch experience curve is a headwind the mission cannot outrun at any Earth-accessible destination.** A full-cashflow round with a demand model and sovereign/strategic-buyer scenarios (the one path to a sustained premium) is named as the follow-on. See [[10-round-trip-ceiling]] — schedule is now doubly penalized (R183 ~10 %/yr of NPV on the capital side; R188 ~13 %/yr on the revenue/price side).

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

### 2026-07-21 latest+25 — worktree-115637 R-clearing-price-time-path (public `93a9888`) — R183's open price-decay parameter anchored to the launch experience curve; a market bet surfaces under the three engineering bets

R183 (`R_waiver_value_consolidation`) had left the water-price-decay path as an un-anchored swept scenario, noting a clearing-price-vs-launch-cost round would anchor it. R188 is that round, and the first externally-anchored round of the campaign. It anchors the decline rate to the launch-cost experience curve (external sources cited in SCOPE): delivered-water clearing price in LEO is capped by Earth-launched propellant, whose cost falls from ~$3,868/kg (2025) toward ~$273/kg (2040 median), a 9-18 %/yr decline (central 12.8 %). This is 3-6× R183's 3 %/yr kill threshold, and it exceeds both campaign hurdles outright — so over the mission's 13-23-yr timeline the market discounts revenue faster than capital does (23.5-yr revenue discount factor 0.47-0.76 %). The deep-space substitute (10-90× LEO at Δv 10-20 km/s) is the only immune regime, but has no market in the window. The economics/market bet is surfaced as a fourth bet-adjacent gate beneath the three engineering bets, with the cheap-vs-dear dilemma as its structure. Program-class verdict unchanged (binding constraint upstream); the pitch implication is that the revenue case cannot assume a stable delivered-water price. Status held at open / high; full-cashflow follow-on with a demand model named. All four hypotheses HELD.
