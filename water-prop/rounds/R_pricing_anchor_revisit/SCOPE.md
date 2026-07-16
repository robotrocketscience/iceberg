# R-pricing-anchor-revisit — does $1,400/kg Earth-launch-displacement under-anchor what ICEBERG can charge per kilogram?

**Status:** scope, pre-study. Authored by Saturn (orchestrator), 2026-05-15 latest+9. Triggered by project-owner challenge: "$1,400/kg does not accurately reflect what can be charged."

**Worker assignment:** open to any moon (Mimas, Dione, Tethys, Iapetus on resume, or a fresh moon name). Touches industrial-organisation, willingness-to-pay analysis, public-comparable pricing, and propagation back into the matrix's economic-cell verdicts.

---

## Context

The current pitch headline (`ICEBERG-pitch.md:142`, `:232`) anchors steady-state per-kilogram revenue at **$1,400–2,800/kg** — Falcon-Heavy / Falcon-9 launch-cost displacement. The reasoning: ICEBERG can price near Earth-launch displacement because the customer's only alternative is launching the same water from Earth at that price.

The demand-side analysis (`ICEBERG-demand.md` §3 "Tiered ramp", lines 198–235) already disagrees with the pitch headline. The tiered table shows blended **$3,000–5,000/kg** in the 100 t/yr supply tier (anchor era), with mission-essential segments at $5–10k/kg (crewed stations), $3–7.5k/kg (GEO servicing), and **$10–25k/kg one-shot for the DoD strategic reserve in the ramp era**. ISS commercial resupply effective per-kg is **~$25,000–50,000/kg** (NASA Office of Inspector General IG-18-021). The single-buyer ceiling at GEO is **~$30,000/kg effective** (Earth-launched hypergolics + tug). Lunar in-situ-resource-utilisation at scale lands at $1,500–3,000/kg planning-band per Sanders 2019.

The disagreement: the pitch headline uses **bulk-supply displacement** as the anchor; the demand doc uses **mission-essential willingness-to-pay** as the anchor. The two are 2–10× apart, and the financial rounds need to anchor on one or the other consistently. As of 2026-05-15 latest+9 it is not consistent across the campaign:

- Tier-aware: `R-LEO-water-demand-curve` (enceladus-r5, `ed3dd58`), `R-clearing-price-tail-integration-decision-frame` (rhea-2, `c8dbfa9`).
- Suspected flat-displacement-anchored: `R-reactor-roadmap` (worktree-110450, `e9ab1ba`), `R-delivery-irr-curve`, `R-bottoms-up-vehicle-cost` (enceladus-r5), `R-per-mission-economics-sensitivity-revisit` (rhea-2, `e6fd6a2`), other internal-rate-of-return rounds. **Audit-in-progress (task 8 of latest+9 integration pass)** — preliminary read; this round should not assume the audit is complete.

If a meaningful share of the campaign's financial-cell verdicts (internal-rate-of-return, net-present-value, hurdle-crossover) were derived from flat $1,400/kg, they are systematically pessimistic by a factor that grows with the share of mission-essential / captive volume in the supply tier. The matrix's "matrix-empty under every anchor" verdict (axis 02) and the iapetus-chain "program-class technology-demonstrator" verdict (REQUIREMENTS L0-24, latest+9) may be partially load-bearing on this anchor choice. Resolving the anchor is therefore a structural-reopener candidate, not a cosmetic update.

The project-owner challenge is specifically the supply-side framing: "what can ICEBERG charge" is a pricing-strategy question (operator decision under a natural-monopoly cost structure), not solely a buyer-willingness-to-pay question (demand-side ceiling). The two converge under perfect competition; under natural monopoly with single-supplier-no-substitute segments, supplier pricing can sit anywhere between marginal cost (floor) and willingness-to-pay (ceiling), and the realised price depends on contract structure, regulatory framing, and the operator's market-power capture.

---

## What this round answers

For each (operational era × customer segment), what is the **defensible realised price per kilogram** that ICEBERG can charge, conditioned on:

1. **Willingness-to-pay ceiling** — what each segment would pay rather than go without (mission-essential pricing).
2. **Competing-supply floor** — what each segment can pay because alternatives exist (Earth-launch, lunar in-situ-resource-utilisation, customer in-orbit electrolysis).
3. **Contract structure** — long-term offtake at sovereign-flag pricing, spot pricing, regulated-utility rate-of-return pricing, monopoly-rent extraction.
4. **First-mover / novelty premium** — symbolic value of the first delivery (sovereign-flag, scientific-firsts, public-relations) priced separately from bulk volume.
5. **Captive segments** — segments with no alternative supplier (DoD strategic reserve, scientific buyers with unique-Saturn-ring isotopic requirements).

The deliverable is a defensible price band per (era × segment), with sourcing on each anchor point, and a re-run of the matrix's load-bearing financial cells under the revised pricing.

---

## Pre-registered hypotheses (numeric ranges + falsification bands)

| # | Hypothesis | Predicted range | Falsification band |
|---|---|---|---|
| H1 | The current $1,400/kg pitch-headline anchor is below the realised willingness-to-pay ceiling for **every** segment listed in `ICEBERG-demand.md` §3 except Mars-architecture water at steady state. Crewed-station, GEO-servicing, and DoD-strategic-reserve all support per-kilogram pricing above $1,400/kg through year 30+. | each non-Mars segment supports ≥ $1,400/kg through year 30+ | H1 falsified if any non-Mars segment ceiling is < $1,400/kg in any era |
| H2 | The realised blended price in the 100 t/yr anchor era is ≥ 2× the pitch headline. The mission-essential weighting (DoD strategic reserve at $10–25k/kg one-shot, crewed stations at $5–10k/kg) pulls the blended average above $2,800/kg. | blended anchor-era price ≥ $2,800/kg | H2 falsified if blended anchor-era price < $2,000/kg under conservative weightings |
| H3 | A novelty / sovereign-flag premium is defensible for the first ≤ 100 tonnes delivered, priced **separately** from bulk volume. The premium is sized by analogy to (a) the first Apollo lunar sample resale prices (per-gram), (b) Cassini-mission per-kilogram science-return economics, (c) inaugural sovereign-flag space-asset pricing (SNAP-10A, first GEO comsat). Predicted band: $50,000–500,000/kg for the first 1–10 tonnes; $10,000–50,000/kg for the next 10–100 tonnes. | first-100-t novelty premium ≥ $10,000/kg | H3 falsified if no defensible novelty-premium analogue supports > $10,000/kg even for the first ten tonnes |
| H4 | Under regulated-utility-class rate-of-return pricing (operator earns a regulated return on rate base, akin to a power utility or canal authority), the operator can sustain $2,500–5,000/kg in the 1,000 t/yr era without exceeding what a regulator would approve as "just and reasonable" given the program's capital base. This is independent of willingness-to-pay; it is set by regulated cost-plus-margin. | regulated-utility realised price $2,500–5,000/kg in the 1,000 t/yr era | H4 falsified if the regulated rate-base calculation gives < $1,500/kg or > $8,000/kg in that era |
| H5 | Under monopoly-rent extraction in segments with no alternative supplier (DoD strategic reserve plus any contracted single-source science buyer), the operator can sustain ≥ $20,000/kg for ≥ 100 t/yr of contracted volume through year 30+, **provided** the operator does not face a regulator or a sovereign offtake contract that caps margin. This is the upside case the pitch headline omits entirely. | monopoly-rent realisable in captive segments ≥ $20,000/kg | H5 falsified if no captive segment can sustain ≥ $10,000/kg through year 30+ |
| H6 | Replacing the flat $1,400/kg anchor with a tier-aware era-segment band in the load-bearing financial rounds (internal-rate-of-return, hurdle-crossover, program net-present-value) shifts the matrix's economic verdict materially. Specifically: at least one financial-cell verdict currently classified "matrix empty" or "below sovereign-bond hurdle" flips to "above sovereign-bond hurdle" or "regulated-utility class accessible" under the revised pricing. The aerobraking-engineering-closure and reactor-program-availability bottlenecks (latest+9 L0-24) remain binding, but the economic axis becomes a less load-bearing constraint than the engineering axes. | at least one financial-cell verdict flips under revised pricing | H6 falsified if every load-bearing financial verdict is robust to anchor change up to $5,000/kg blended |
| H7 | (Reading-level — load-bearing for project owner.) The corrected pricing anchor does NOT change the iapetus L0-24 / matrix-empty verdict because the engineering-closure × reactor-program-availability axes are the binding constraints, not the economic axis. Pricing-anchor correction is real but not architecturally rescuing. Under H6 + iapetus chain: even if every financial cell flips positive under revised pricing, the program-class decision stays at technology-demonstrator-only until L0-24 is satisfied. | H7 held: pricing correction does not flip program-class | H7 falsified if H6 + revised pricing puts a regulated-utility cell above the L0-24-conditioned-on-Fission-Surface-Power-Phase-2 posterior threshold (currently 2.7% absolute ceiling per iapetus) |

H7 is the load-bearing reading. H1–H5 build the evidence; H6 propagates it through the matrix; H7 says whether the propagation changes the project-owner decision.

---

## Method sketch (worker drafts the actual code in `run.py`)

This is a synthesis / market-research round, not a physics round. Expected ~60% literature work, ~30% spreadsheet modelling, ~10% code.

1. **Build the comparables table.** For each anchor below, a single defensible per-kilogram dollar figure with explicit citation, year, and adjustment-to-2026-dollars factor:
   - ISS commercial resupply effective per-kg (NASA Office of Inspector General IG-18-021; verify the citation).
   - GEO comsat servicing analogues (Northrop Grumman SpaceLogistics Mission Extension Vehicle 1 + 2 actual contracts; Orbit Fab fuel-depot pricing announcements).
   - Falcon Heavy, Falcon 9, Starship published per-kilogram-to-LEO.
   - Lunar in-situ-resource-utilisation projected costs (Sanders et al. 2019; ispace, Astrobotic, Intuitive Machines public pricing on water-equivalents).
   - DoD on-orbit servicing pricing (publicly disclosed Space Development Agency, US Space Force, AFRL contracts where pricing is public).
   - Cassini-mission per-kilogram returned-data economics (only a science-analogue, not direct).
   - Apollo lunar-sample per-gram public-sale and private-sale prices (novelty-premium analogue).
   - Helium-3 lunar-mining pricing claims (Moon-Express, similar).
   - First-of-kind / sovereign-flag premiums in adjacent industries (commercial space-station debut, first private deep-sea mining sample, first commercial fusion electricity).

2. **For each segment in `ICEBERG-demand.md` §3, derive three numbers per era (100 t/yr, 1,000 t/yr, 10,000 t/yr):**
   - **Willingness-to-pay ceiling** = highest price the segment will pay rather than go without.
   - **Competing-supply floor** = price at which a viable alternative supplier exists for that segment.
   - **Defensible realised band** = bracket of plausible operator-realised prices given contract structure and market power.

3. **Aggregate into a blended realised price per era**, weighted by segment volume from `ICEBERG-demand.md` §3. Compare to the pitch headline $1,400/kg. Compute the magnitude of the disagreement.

4. **Re-run the load-bearing financial rounds with revised pricing.** Critical-path subset:
   - `R-reactor-roadmap` marginal internal-rate-of-return (worktree-110450, `e9ab1ba`).
   - `R-delivery-irr-curve` hurdle crossovers (worktree-110450, `6068140`).
   - `R-per-mission-economics-sensitivity-revisit` (rhea-2, `e6fd6a2`).
   - `R-bottoms-up-vehicle-cost` net-present-value-probability headline (enceladus-r5, `0098239`).
   - Any other round flagged by the audit (task 8 of latest+9 pass) as flat-anchored.

5. **Stress-test the revised pricing.** Sensitivity sweeps: contract-structure-mix shift (more / less long-term offtake vs spot), regulator-imposed margin caps, mission-essential segment volume share, novelty-premium decay rate. Identify which sensitivities can flip H6 or H7.

6. **Reading-level conclusion.** Either:
   - **H6 held, H7 held:** pricing-anchor correction is real, financial rounds are revised, but program-class decision (technology-demonstrator) is unaffected. Update the pitch and the matrix; queue no architectural reopener.
   - **H6 held, H7 falsified:** pricing correction is enough to put a regulated-utility cell above the L0-24-conditioned posterior. Architectural reopener: project-owner decision on whether to admit pricing-driven program-class promotion despite the reactor-program-availability constraint.
   - **H6 falsified:** revised pricing does not move financial verdicts materially. Pitch headline is wrong-but-not-load-bearing; cosmetic fix.

---

## Reading template (5-section round template, worker fills in after run)

- **Hypotheses adjudicated.** Verdict per H1..H7 (held / falsified / held-with-margin / falsified-at-magnitude). Predicted vs measured numeric range for each.
- **Headline.** One-line summary: does the corrected pricing anchor change the program-class verdict?
- **Reading.** Reading-level decision the project-owner needs.
- **Cross-learning.** What this round teaches about anchor-choice in long-cycle economic models. Relationship to PROTOCOL methodology lesson 7 (pessimistic anchor first) — pricing is the rare axis where the pessimistic anchor (flat $1,400/kg launch displacement) may be **too pessimistic** because it ignores market power in captive segments. This is the asymmetric case lesson 7 doesn't cover.
- **Next-round candidates.** If H6 held, follow-on on the contract-structure design (which contracts maximise realised price). If H7 falsified, follow-on on whether the L0-24-conditioned posterior re-opens under pricing-corrected NPV.

---

## Worker assignment notes

- **Round priority:** **high.** Project-owner-triggered. Lands upstream of any pitch rewrite (which is currently blocked by the iapetus/titan-2 framing tension AND now by this pricing-anchor question). Pitch rewrite should wait for this round's H7 verdict.
- **Worker fit:** any moon. Light on physics, heavy on industrial-organisation, public-comparable research, and financial-cell propagation. The PROTOCOL.md HERITAGE survey applies to pricing-comparable sourcing — each comparable should be HERITAGE-AVAILABLE (real public contract or disclosed sample sale), HERITAGE-ADJACENT (proxy market with disclosed pricing), or HERITAGE-NONE (speculative analogue; flag explicitly).
- **Inputs the worker needs:**
  - `ICEBERG-pitch.md` §4 + §9 (the pitch-headline anchor and the era table).
  - `ICEBERG-demand.md` §3 (the tier-aware ramp table).
  - `water-prop/rounds/R_LEO_water_demand_curve/STUDY.md` (anchor on tier-aware-vs-flat distinction).
  - `water-prop/rounds/R_clearing_price_tail_integration_decision_frame/STUDY.md` (existing decision-frame work).
  - `REQUIREMENTS.md` L0-12 (cost-competitiveness clause; reads on "lowest competing supply") and L0-13 (NPV at infrastructure-class cost of capital with the latest+9 capital-structure parenthetical).
  - The latest+9 financial-round audit (task 8 of integration pass) — once complete, the audit identifies which rounds are flat-anchored.
  - PROTOCOL.md methodology lessons 7 (pessimistic anchor first — note the asymmetric case this round may surface), 8 (per-mission vs program NPV — apply both checks).
- **Out-of-scope for this round:** any anchor on what ICEBERG **costs to produce** (that is the cost side; this round is the revenue side). Bottoms-up-vehicle-cost lives in its own round. Out-of-scope to re-derive any orbital-mechanics or propulsion-physics number; treat physics inputs as fixed at the current matrix state.
- **Out-of-scope provenance check:** if the audit (task 8) has not run when this worker picks up, treat the financial-round-anchor-status as unknown and report flat-vs-tier-aware for each round before propagating revised pricing. Do not assume the audit's preliminary read.
- **Authorial note from Saturn:** this SCOPE is anchored on the project-owner's challenge that $1,400/kg is too low. The pre-registered hypotheses are deliberately phrased to allow the round to falsify the challenge (H1, H6 falsification bands) — pessimistic-prediction default per PROTOCOL lesson 1. If the round comes back with "$1,400/kg was approximately right after all," that is a defensible outcome and should be reported as such.
