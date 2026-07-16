# R-pricing-anchor-revisit — READING (5-section template)

**Worker:** titan-5 · **Date:** 2026-05-22

## Hypotheses adjudicated

H1 **held** · H2 **held** · H3 **held** (via recurring comparables, not the collectible
analogue) · H4 **held-plausible** at the lower edge (precise rate base deferred) ·
H5 **split** (held early / falsified sustained) · H6 **falsified** · H7 **held**.

Predicted-vs-measured: every frozen prediction in STUDY.md held. The project-owner challenge
("$1,400/kg is too low") is **correct in direction** — $1,400/kg is the Falcon-Heavy
launch-displacement floor and sits below the blended realised price in the two near-term
eras ($3.6–5.0k/kg at 100 t/yr; $1.6–2.2k/kg at 1,000 t/yr) and far below mission-essential
WTP (ISS-CRS $26–125k/kg; Orbit Fab GEO $200k/kg).

## Headline

**The $1,400/kg pitch anchor understates defensible willingness-to-pay by 2–150× across
segments — but correcting it does NOT change the program-class verdict.** The binding
constraint is reactor-program availability (L0-24), not revenue per kilogram. The financial
rounds already assume $10,000/kg and still land technology-demonstrator / sub-sovereign-bond,
so a higher price cannot rescue the architecture, and the *defensible* blended price
($3.6–5k near-term) is actually **below** what those rounds already use.

## Reading (for the project owner)

Three decisions follow, none of them architectural:

1. **The pitch headline is wrong in the conservative direction.** Restate it as a band, not a
   single number: **Earth-launch displacement ($1,400–3,000/kg) as the FLOOR**, lunar-ISRU
   displacement (~$1,000/kg at scale) as the **bulk competing-supply ceiling**, and
   **mission-essential WTP ($5–25k+/kg for crewed / GEO / DoD) as the operative blend-weighted
   band** in the near-term eras. The current single-number $1,400/kg is the floor masquerading
   as the plan.

2. **Pricing is not the gate.** H7 holds: even generous pricing leaves the program at
   technology-demonstrator until a flight-qualified reactor is on contract (L0-24). Do not let
   a pricing-up-revision be read as a thesis rescue. The pitch rewrite — which the SCOPE says
   is blocked on this round's H7 — is now **unblocked: H7 held**, so the rewrite proceeds with
   the floor/ceiling/operative-band framing AND the unchanged program-class verdict.

3. **The campaign's price assumptions are internally generous, not pessimistic.** Load-bearing
   rounds at $10k/kg and the R_LEO_water_demand_curve median at $1,500/kg bracket the
   defensible band; if anything the matrix should treat $10k/kg as an upper-operative anchor
   and re-check that no verdict is *propped up* by it (the inverse risk to the one the
   project-owner challenge raised).

## Cross-learning

This is the asymmetric case **PROTOCOL lesson 7 (pessimistic anchor first) does not cover.**
For pricing, the "pessimistic" anchor (flat $1,400/kg launch displacement) is *too*
pessimistic, because it ignores supplier market power in captive, no-substitute segments
(DoD, crewed-station resupply) where realised price sits near WTP, not near competing supply.
Lesson 7 protects against optimism on engineering axes; on a pricing axis under natural
monopoly it can manufacture false pessimism. **The discipline that saved the verdict here was
not the pessimistic anchor — it was checking which axis is binding.** Pricing was the wrong
axis to worry about; the reactor program is the right one. Candidate PROTOCOL lesson: *before
correcting an anchor, confirm the axis it sits on is load-bearing for the verdict.*

## Inverse-risk check (done — `inverse_risk_check.py`)

The mirror of the project-owner challenge: is any positive-leaning verdict propped up by the
generous $10k anchor? Re-running R_reactor_roadmap's marginal-IRR machinery across the price
band shows **marginal IRR sub-sovereign-bond (< 4%) at every price from $1,400 to $10,000/kg**
(1.45% at $10k, flooring to 0% below ~$10k as branches go NPV-negative). H7 is confirmed
**bidirectionally**: pricing cannot rescue the program (H6) and is not secretly carrying it.
The economic axis is robustly non-binding regardless of where in the defensible band the price
actually lands.

## Next-round candidates

- **Pitch rewrite** (now unblocked on H7): floor/ceiling/operative-band pricing + unchanged
  technology-demonstrator program-class. Orchestrator-owned (shared doc); proceed at
  integration.
- **Contract-structure design** (if a future operator wants to *maximise* realised price):
  long-term sovereign offtake vs spot vs regulated-utility — which structure captures the
  captive-segment market power H5 identifies without inviting a margin-capping regulator.
