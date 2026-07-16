# R-saturn-system-water-depot-demand — STUDY (pre-registration; locked before inventory)

**Worker:** hyperion (re-spawn 2). **Date:** 2026-05-26. **Status:** pre-registration frozen; inventory pending.
**Round type:** desk-study demand-side adjudication. No mission_graph encoding. Public-source-only; every claim cited with a link, or flagged "no source".

**Question:** Is there any commercial market for water at a Saturn-system depot? This is the load-bearing demand-side input on whether matrix decision #15 **option (b)** (waive L0-04 strict deliver-to-Earth-orbit; admit a Saturn-system water depot as a product class) is a *substantive* option at all, or whether #15 collapses to **option (c)** (hold L0-04 strict, accept campaign termination at flyable power).

Why it matters: a drop-and-go Saturn-system depot removes the Earth-return leg, which removes the two framework killers that closed the matrix at flyable power (the 14–16-yr cumulative-burn reactor-lifetime kill and the 50-tonne small-vehicle mass-floor kill, per titan-4 `0eb11a7`). So if demand exists, the matrix re-opens at single-kilowatt power. If demand is an empty set, the depot is technologically achievable but economically empty.

---

## Pre-registered hypotheses (authored by Saturn/orchestrator in SCOPE; graded here)

| # | Hypothesis (abbreviated) | Predicted reading if it holds |
|---|---|---|
| H1 | Saturn-system demand is **structurally absent** under 2026 baseline — no commercial mission with a real customer operating or planned to launch before 2050. | Option (b) achievable but customerless; demand-side empty; #15 → (c). |
| H2 | Demand exists **only conditional** on future agency/commercial Saturn-system program commitments, each at ≤10% base rate through 2045 (locked finding 2 generalised). | Real option at venture-portfolio probability; ICEBERG cannot underwrite delivery before customer commitment. |
| H3 | Demand exists at **"fuel for Earth-return / outer-system missions crossing the Saturn system"** scale (logistics market: sell reaction mass / sample-return propellant to passing missions). | Demand-curve depth (missions/decade × $/kg-saved) is load-bearing; likely 0–2 missions/decade at most. |
| H4 | Demand exists at **"ICEBERG is its own customer"** scale — depot is a load-balancing element of a two-vehicle relay (Saturn filler with no Earth-return + fast Earth–Saturn–Earth shipper). | Not a market-demand question; an architecture-restructure question. Reduces to whether two-vehicle total cost/delivered-kg beats one-vehicle. |
| H5 | A Saturn-system **human-presence** program (Titan colony, ring tourism) generates industrial-scale demand before 2050. | Opens the whole matrix, but at a very-low-probability conditioning event. |
| **H6 (load-bearing)** | At **any defensible 2026-baseline prior, Saturn-system demand is too thin to underwrite a commercial-class L0-04 waiver** — BUT the H4 ICEBERG-internal-relay reframe is worth a dedicated mission_graph round. Option (b) under H1/H2/H3 priors is not commercially actionable; under H4 it is an architecture-restructure decision, not a depot-demand decision. | If H4 is the path, decision #15(b) is mislabeled: it is not a depot-demand decision but a two-vehicle-architecture decision. |

### My honest prior (recorded before inventory)

I expect **H1 to substantially hold** (no commercial customer at Saturn before 2050) and **H6 to hold as written**. The interesting output is not whether a commercial market exists — I am near-certain it does not at a 2026 baseline — but **the relative weight of H3 (logistics) vs H4 (internal relay)** as the two non-empty readings. My pre-inventory lean: H3 is real but vanishingly thin (≤1 mission/decade plausibly able to use a Saturn depot, and even those ship their own propellant today); H4 is the only reading under which option (b) is genuinely actionable, and it is an architecture question the campaign has not yet costed. So I expect the round's load-bearing recommendation to be: **decision #15(b) is not a demand decision; route it to a two-vehicle-relay architecture round or close it to (c).**

Where I could be wrong: (1) if a credible commercial outer-system logistics entrant has emerged since my knowledge cutoff (Jan 2026), H3 could be less thin than I expect — I will search explicitly for this and cite. (2) The H4 back-of-envelope could show the two-vehicle architecture is obviously worse (relay vehicle inherits the same reactor-lifetime/mass-floor kills on its own return leg), in which case even H4 does not rescue option (b) and #15 collapses cleanly to (c). I will compute the relay leg's burn-time/mass-floor exposure explicitly rather than assuming it inherits the depot's relief.

---

## Source-set (frozen before inventory)

1. **Agency announced/studied outer-system missions through 2050.** NASA Planetary Science Decadal Survey 2023 (*Origins, Worlds, and Life*); ESA Voyage 2050 themes; JAXA outer-system roadmap. Tabulate every Saturn-system mission with a launch or decision date. Score: commitment level (announced / studied / proposed / aspirational); est. water/propellant demand; P(materialises) using historical agency follow-through base rates + locked finding 2.
2. **Commercial Saturn-system entrants.** Explicit search for any commercial actor with a stated Saturn-system architecture. Score: capitalisation, technical credibility, customer base, regulatory status. (Prior: empty set.)
3. **Logistics-customer demand model (H3).** Forward pipeline of Jupiter-gravity-assist outer-system missions 2026–2076; estimate which could use a Saturn-system propellant stop; price the Δv reduction / sample-return mass savings in $/kg-saved using the corrected vis-viva anchors (titan-3 R-delta-velocity-anchor-audit, latest+13).
4. **ICEBERG-internal-relay analysis (H4).** Back-of-envelope two-vehicle decomposition; does two-vehicle total cost/delivered-kg beat one-vehicle at any sensible setting, AND does the relay leg escape the reactor-lifetime/mass-floor kills? Viability check only — not a mission_graph encoding.

### Out of scope (per SCOPE)
- Supply-side closure of a one-way single-kWe Saturn vehicle (decision #16 parametric floor sweep + a one-way re-encoding round).
- Pricing of water at Saturn as a clearing price (this round produces demand-curve *quantity* points, not a clearing price).
- Detailed two-vehicle architecture design (H4 is back-of-envelope; a dedicated round would design it).

---

## Deliverables (commit order)

1. `STUDY.md` — this file (frozen). [exp commit 1]
2. `results/demand_side_inventory.md` — scored inventory across the four source axes. [exp commit 2]
3. `results/H1_through_H5_verdicts.md` — per-hypothesis verdict. [exp commit 2]
4. `READING.md` — H6 load-bearing reading; decision #15(b) actionability recommendation; if H4, a SCOPE outline for R-iceberg-two-vehicle-relay-architecture. [exp commit 3]
5. Handoff update to orchestrator.

## Method note on citations

Knowledge cutoff is January 2026. For any time-sensitive claim (mission status, award dates, commercial entrants) I will web-search to confirm current state and cite a link. Stable facts (Decadal 2023 priorities, orbital mechanics) I state from baseline knowledge and cite the primary document. Where no public source exists for a claim, I say so explicitly per the citation rule.
