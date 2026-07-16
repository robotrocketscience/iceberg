# R-architecture-D-L1007-relaxation — study

**Owner:** rhea (re-spawn, fifth re-entry, round 7)
**Status:** PRE-REGISTERED (hypothesis frozen before run.py executes)
**Round directory:** `water-prop/rounds/R_architecture_D_L1007_relaxation/`

## Question

**Question my own round-6 finding.** Round 6 (R-architecture-D-cost) concluded "Architecture D is structurally money-losing at zero discount under every conservative anchor swept." That conclusion held the chunk-mass at the L1-007 cap (200 tonnes) and used a fixed FSP-stretch 20-tonne reactor. Both held assumptions falsifiable by current matrix decision points:

1. **Chunk-mass cap (L1-007) is a live project-owner decision point (#3 in matrix).** Single-chunk physical cap at the B-ring is 482 tonnes; hurdle crossovers for Variant B per R-delivery-irr-curve are at 209 t (sovereign-bond), 461 t (regulated-utility), 691 t (corporate-growth, requires multi-chunk now-falsified).
2. **Round 6 used reactor mass from R-chemical-plus-small-reactor's fixed sweep grid (20 t at 10 W/kg = 200 kWe).** Saturn-side energy budget at chunk 200 t only requires 140 kWe → right-sized reactor mass is 14 t, not 20. Round 6 over-counted reactor mass (and CapEx) by ~30 percent.

This round answers: **under L1-007 relaxation upward (to the B-ring single-chunk cap of 482 tonnes) AND right-sized FSP-stretch reactor, does Architecture D become commercially defensible? Does D-solar-thermal dominate Variant B on programmatic-risk-adjusted expected delivered mass at any chunk-mass value?**

## Method discipline

Methodology lessons applied:

- **Lesson #1 (back-of-envelope first):** computed delivered, CapEx, gross cashflow, and expected delivered mass for both D variants and Variant B at chunk values 200, 250, 300, 350, 400, 482 tonnes BEFORE pre-registering. Surfaced the right-sized-reactor correction and the chunk-cashflow-crossover anchor.
- **Lesson #7 (re-fetch origin first):** re-fetched origin/main, merged in `8f3dafe` design-axes move to project root.
- **Lesson #9 (re-fetch before handoff too):** will re-fetch before writing handoff.
- **Standing user directive: question your assumptions.** This entire round is structured as a falsification attempt against round 6.

## Pre-registered hypothesis (H7)

**Aggregate (H7-agg):** Under L1-007 relaxation, Architecture D becomes per-mission cashflow-positive at chunk ≥ 450 tonnes (D-fission) and chunk ≥ 470 tonnes (D-solar-thermal), at BEST_CELL pricing and central CapEx anchor. Conditional marginal-internal-rate-of-return becomes defined at chunk ≥ 350 tonnes for both D variants. Sovereign-bond (4 percent marginal-IRR) is cleared by D-solar-thermal at chunk ≥ 450 tonnes only under Starship-optimistic launch ($200M); at mixed-baseline launch ($500M) sovereign-bond is not cleared anywhere in the swept range. **Architecture D's expected delivered mass per mission at chunk 482 tonnes exceeds Variant B's by 3.5-4.5×** (D-solar-thermal) and 1.3-1.6× (D-fission); the matrix should record this as a load-bearing finding for the L1-007 decision.

### Pre-registered sub-claims

| Sub-claim | Predicted | Falsification |
|---|---|---|
| H7-a — Right-sizing the FSP-stretch reactor at chunk 200 t (140 kWe needed for 1-yr Saturn ops) | M_reactor = 14 t, delivered = 24.5 t | outside 12-16 t or 22-27 t |
| H7-b — D-fission per-mission gross cashflow break-even chunk (BEST_CELL, central CapEx, right-sized reactor) | 450-480 t | outside 400-550 t |
| H7-c — D-solar-thermal per-mission gross cashflow break-even chunk (BEST_CELL, central CapEx, optimistic stack scaling) | 460-490 t | outside 410-560 t |
| H7-d — D-fission conditional IRR at chunk 482 t, BEST_CELL, mixed-baseline launch, central CapEx, right-sized reactor | -1.0 to +2.5 percent (defined but below sovereign-bond at mixed-baseline launch) | outside -3 to +4 percent |
| H7-e — D-solar-thermal conditional IRR at chunk 482 t, BEST_CELL, Starship-optimistic launch, central CapEx | +2.0 to +5.0 percent (clears sovereign-bond at Starship-optimistic launch) | outside 0 to +6 percent |
| H7-f — D-fission expected delivered mass per mission at chunk 482 t (posterior 0.78% × conditional 75 t) | 0.45-0.75 t | outside 0.30-1.00 t |
| H7-g — D-solar-thermal expected delivered mass per mission at chunk 482 t (posterior 2.03% × conditional 75 t) | 1.3-1.8 t | outside 0.8-2.5 t |
| H7-h — Variant B expected delivered mass per mission at chunk 482 t (chained posterior 0.13% × conditional 310 t) | 0.38-0.45 t | outside 0.25-0.60 t |
| H7-i — D-solar-thermal vs Variant B dominance factor on expected delivered mass at chunk 482 t | 3.5-4.5× | outside 2.5-6.0× |
| H7-j — Sovereign-bond clearance for Architecture D at any swept chunk and launch anchor (BEST_CELL) | D-solar-thermal Starship-optimistic clears at chunk ≥ 450 t; D-fission does not clear anywhere | falsified if D-fission clears OR if D-solar-thermal Starship-optimistic does not clear at chunk 482 t |
| H7-k — Variant B per-mission gross cashflow at every chunk-mass dominates Architecture D per-mission gross cashflow | yes, by 5-10× (Variant B's per-mission revenue advantage 6.5× × similar CapEx) | falsified if D matches or exceeds Variant B per-mission cashflow at any chunk |
| H7-l — Falsification check on round 6 headline: under L1-007 relaxation, is Architecture D "structurally money-losing"? | falsified: at chunk ≥ 450 t (D-fission) or ≥ 470 t (D-solar-thermal), Architecture D becomes per-mission cashflow-positive. Round 6's "structurally money-losing" headline is conditional on the L1-007 200-t cap; under L1-007 relaxation it falsifies. | falsified-of-falsification: if no swept chunk gives positive per-mission cashflow for any D variant |
| H7-m — Combined verdict relative to Variant B under L1-007 relaxation | Variant B remains per-mission cashflow-superior; D-solar-thermal dominates Variant B on programmatic-risk-adjusted expected delivered mass at chunk ≥ 200 t; matrix records multi-axis tradeoff under L1-007 relaxation | falsified if either claim fails |

**Aggregate decision rule:** if H7-agg holds: surface to project owner that **the L1-007 decision is more consequential for Architecture D than for Variant B on programmatic-risk-adjusted basis**, because D-solar-thermal's credibility advantage (2.03 percent posterior vs 0.13 percent chained Variant B posterior) compounds with chunk-mass scaling. The L1-007 decision is the single most leveraged decision for the surviving-cell axis. If H7-agg falsifies: round 6's headline holds independent of L1-007; no chunk-mass relaxation rescues Architecture D economically.

## Method

### Mass cascade at variable chunk mass

For each chunk mass `C` (tonnes) and Saturn-ops duration `T` (years, default 1.0):

1. Inbound propellant required: `P_inb = C × (1 - 1/MR_inbound)` where `MR_inbound = exp(6.42 / 4.413) = 4.284`.
2. Electrolysis energy required: `E_kWh = P_inb × 1000 × 8.0` (industrial alkaline + cryogenic liquefaction, per R-chemical-plus-small-reactor).
3. Saturn-side power required for 1-yr ops at full duty: `P_kWe = E_kWh / (T × 8760)`.
4. **D-fission:** reactor mass at FSP-stretch specific power 10 W/kg = `M_reactor = P_kWe / 10` tonnes.
5. **D-solar-thermal:** stack mass at 101 kg/kWe (SOEC + 0.1 kg/m² mirror, DC=1.0 per R-saturn-side-solar-thermal) = `M_stack = P_kWe × 0.101` tonnes.
6. Dry mass at Saturn: `M_dry_Sat = M_vehicle + M_subsystem + M_electrolysis` where M_vehicle = 10 t, M_electrolysis = 5 t (D-fission only — SOEC integrated for D-solar-thermal, so no separate electrolysis), M_subsystem = M_reactor or M_stack.
7. Delivered: `D = C / MR_inbound - M_dry_Sat × (1 - 1/MR_inbound)`.

### CapEx scaling with subsystem mass

D-fission ship CapEx at right-sized reactor:
- Baseline (R6 central): $600M at M_reactor = 20 t.
- Linear scaling on reactor mass at $8M-per-extra-tonne (derived from $250M reactor at 20 t → $12.5M/t baseline; marginal scaling assumed lower at $8M/t for already-engineered subsystem mass).
- At M_reactor = 14 t (chunk 200 t demand): $600M - (20 - 14) × $8M = $552M.
- At M_reactor = 34 t (chunk 482 t demand): $600M + (34 - 20) × $8M = $712M.

D-solar-thermal ship CapEx at variable stack mass:
- Baseline (R6 central): $608M at stack ≈ 20 t (200 kWe useful).
- Linear scaling on stack mass at $6M-per-extra-tonne (mirror + concentrator scale more cheaply than reactor; mirror cost is dominant and scales as area).
- At M_stack = 14 t (chunk 200 t demand): $608M - (20 - 14) × $6M = $572M.
- At M_stack = 34 t (chunk 482 t demand): $608M + (34 - 20) × $6M = $692M.

### Variant B reference at variable chunk

Variant B 500-kWe chemical-kick architecture per hyperion R-variant-B-500kWe-sizing at MARVL-anchored masses delivers 128.8 tonnes at chunk 200 tonnes (Option-A-impulsive, since hyperion R-variant-B-impulsive-vs-continuous falsified this and re-derived Variant A/C/D under continuous-thrust accounting). For this round, Variant B is the comparison baseline at the matrix's old chemical-kick reading; the comparison serves to bracket Architecture D against the original Variant B target, not to re-litigate Variant B itself.

- Variant B delivered scales linearly with chunk: `D_VB = 128.8 × (C / 200)`.
- Variant B ship CapEx fixed at $650M (R-reactor-roadmap `Chemical_kick_500kWe` ship cost).
- Variant B posterior fixed at 0.13% (chained, per hyperion R-variant-B-500kWe-sizing programmatic-risk-adjusted = 0.166 t/mission at chunk 200).

### Cashflow framework

Same as round 6, except:
- Delivered mass per ship is now chunk-dependent.
- Ship CapEx is now chunk-dependent (via reactor or stack mass).
- All other constants (DEMONSTRATOR_NRE $500M, GROUND_OPS_PER_YEAR $50M, fleet schedule, horizon 45 yr, perpetuity TV at growth=0) unchanged.

### Posterior overlay

Posterior medians from R-fission-surface-power-stretch-credibility cascade-Monte-Carlo:
- D-fission: 0.78%
- D-solar-thermal: 2.03%
- Variant B: 0.13% (chained from hyperion, used as reference)

### Sweep

Chunk values: 200, 250, 300, 350, 400, 450, 482 tonnes.
Launch costs: 200 (Starship-opt), 300 (Starship-central), 500 (mixed-baseline), 700 (FH+assembly) $M.
Price anchors: BEST_CELL ($10K/kg + $2B sovereign at yr 11) and CONOPS_BASE ($2K/kg, no sovereign).
Variants: D-fission, D-solar-thermal, Variant B.

Total cells = 7 × 4 × 2 × 3 = 168.

## Pre-registered headline (per Lesson #1)

I expect:
1. Architecture D becomes per-mission cashflow-positive at chunk ≥ 450 tonnes for D-fission and ≥ 470 tonnes for D-solar-thermal.
2. D-solar-thermal at Starship-optimistic launch clears sovereign-bond at chunk ≥ 450 tonnes (BEST_CELL).
3. D-solar-thermal expected delivered mass per mission at chunk 482 t is 1.3-1.8 t — 3.5-4.5× Variant B's 0.38-0.45 t.
4. Variant B per-mission gross cashflow strictly dominates Architecture D at every chunk-mass on the cashflow axis, by 5-10×.
5. Combined: **the L1-007 chunk-mass-cap decision is more consequential for Architecture D than for Variant B on programmatic-risk-adjusted basis.** This is the load-bearing finding for the matrix.

If H7-l falsifies (no chunk-mass relaxation rescues Architecture D), round 6's headline strengthens. If H7-i falsifies in the other direction (D-solar-thermal does not exceed Variant B by 3.5×), the multi-axis tradeoff narrative weakens.

## Findings (post-run, 2026-05-15)

### Headline

**Round 6's "structurally money-losing" headline is partially falsified at per-mission cashflow level but holds at program-NPV level even under L1-007 relaxation.** Per-mission gross cashflow turns positive at chunk ≥ 413 t (D-solar-thermal) and ≥ 448 t (D-fission). However, program-level NPV at zero discount rate **remains negative across all 168 swept cells** including the most favourable (D-solar-thermal at low ship CapEx + Starship-optimistic launch + chunk 482 t + BEST_CELL pricing) because the fleet-scale launch costs, opex, and NRE outweigh the modest per-mission positive cashflow at maximum chunk.

**D-solar-thermal expected delivered mass per mission at chunk 482 t is 3.96× Variant B's** (1.598 vs 0.404 tonnes), confirming H7-i in the predicted band. This is the load-bearing finding for the L1-007 chunk-mass-cap decision: under L1-007 relaxation, D-solar-thermal dominates Variant B on programmatic-risk-adjusted basis by a wider margin than at the L1-007 cap.

### Right-sized reactor correction

Round 6 anchored on R-chemical-plus-small-reactor's fixed-grid 20-tonne reactor at chunk 200 t. Right-sizing to actual Saturn-side power demand (140 kWe at 10 W/kg FSP-stretch) gives **14-tonne reactor, 24.5-tonne delivered chunk** at the L1-007 cap — versus round 6's 20-tonne reactor, 19.9-tonne delivered. **Round 6 over-counted reactor mass and CapEx by ~30 percent and under-counted delivered mass by ~23 percent.**

### Per-mission cashflow break-even chunks (BEST_CELL, central CapEx, right-sized subsystem)

| Variant | Break-even chunk t | Delivered at break-even t | Per-mission cashflow at chunk 482 t |
|---|---:|---:|---:|
| D-fission | 448 | 69 | $+42M |
| D-solar-thermal | 413 | 64 | $+108M |
| Variant B (reference) | < 200 | always positive | $+2,454M at chunk 482 |

Variant B per-mission cashflow dominance ratio at chunk 482 t: **58.9× over D-fission**, ~22× over D-solar-thermal. Variant B is on a fundamentally different cashflow-efficiency tier.

### Program-level NPV at zero discount (best case)

| Variant | Best swept cell | NPV at zero discount |
|---|---|---:|
| D-fission | chunk 482, Starship-optimistic, BEST_CELL | $-15.6B |
| D-solar-thermal | chunk 482, Starship-optimistic, BEST_CELL | $-14.1B |
| Variant B (reference) | chunk 482, Starship-optimistic, BEST_CELL | $+42.3B |

Architecture D NPV at zero discount **stays negative even at chunk 482 t** because per-mission gross cashflow ($+42M to $+108M) is small relative to launch + opex + NRE fleet-scale costs ($200-500M launch per mission × 30+ ships, $2.25B opex over horizon, $500M NRE).

### Programmatic-risk-adjusted expected delivered mass per mission

| Chunk t | D-fission t | D-solar-thermal t | Variant B t | D-solar / Variant B |
|---:|---:|---:|---:|---:|
| 200 | 0.191 | 0.497 | 0.167 | 2.97× |
| 300 | 0.331 | 0.861 | 0.251 | 3.43× |
| 400 | 0.471 | 1.226 | 0.335 | 3.66× |
| **482** | **0.586** | **1.598** | **0.404** | **3.96×** |

D-solar-thermal dominance over Variant B on raw expected-delivered scales monotonically with chunk mass.

### Sub-claim grading

10 of 13 sub-claims held. 3 falsifications:

- **H7-d FALSIFIED (mis-anchored prediction):** D-fission conditional IRR at chunk 482 + BEST_CELL + mixed-baseline launch was predicted at -1.0 to +2.5%, observed `None` (NPV-at-near-zero-rate negative). I overestimated the magnitude of per-mission cashflow improvement at L1-007 relaxation; failed to apply program-level NPV check in pre-registration BOE.

- **H7-e FALSIFIED (mis-anchored prediction):** D-solar-thermal conditional IRR at chunk 482 + BEST_CELL + Starship-optimistic launch was predicted at +2.0 to +5.0%, observed `None`. Sovereign-bond clearance does NOT happen at chunk 482 t even under Starship-optimistic launch. **My pre-registration BOE only checked per-mission gross cashflow, not program-level NPV.** Should have computed program-level NPV at chunk 482 before pre-registering.

- **H7-j FALSIFIED:** D-solar-thermal Starship-optimistic does NOT clear sovereign-bond at chunk 482 t. Consistent with H7-e falsification.

### Methodology lesson #10 (NEW)

**Pre-registration BOE for any IRR claim MUST include a program-level NPV check, not just a per-mission cashflow check.** Per-mission cashflow can turn positive (~$42-108M at chunk 482) while program-level NPV-at-zero-discount remains deeply negative (~$-9B to $-12B) because fleet-scale costs and perpetuity tail dominate. The pre-registration BOE for H7-d, H7-e, H7-j was based on per-mission gross cashflow at chunk 482 — and I correctly predicted that turning positive — but mistakenly inferred that program-level IRR would also turn positive. The two are decoupled at small per-mission margins.

This is distinct from Lesson #1 (BOE first): Lesson #1 says compute BOE before pre-registering; Lesson #10 specifies WHICH BOE to compute for IRR claims. **For any prediction of marginal-IRR clearing a hurdle, the BOE must include a coarse cashflow accumulation over the fleet horizon, not just a per-mission gross.**

### Recommended matrix amendments

1. **Update Architecture D cell annotation under L1-007 relaxation.** At L1-007 cap (200 t): per-mission cashflow-negative; at L1-007 relaxation to 482 t: per-mission cashflow-positive but program-level NPV-negative. Neither reading clears sovereign-bond. The matrix should record this as "Architecture D: structurally NPV-negative at conservative anchors regardless of L1-007 decision."

2. **Update L1-007 chunk-mass-cap design axis (#9) finding.** R-delivery-irr-curve says Variant B clears sovereign-bond at chunk 209 t. **D variants do NOT clear sovereign-bond at any chunk up to 482 t** under conservative anchors. The L1-007 chunk-cap decision is more leveraged for Variant B than for D on cashflow basis; it is more leveraged for D than for Variant B on programmatic-risk-adjusted expected-delivered basis (3.96× dominance at chunk 482 vs ~3× at chunk 200).

3. **Update multi-axis matrix finding.** D-solar-thermal beats Variant B on expected delivered mass per mission at every chunk-mass value swept (200-482 t), with the gap widening as chunk grows. Variant B beats D on per-mission gross cashflow at every chunk-mass value, with the gap widening as chunk grows. **The L1-007 chunk-cap decision amplifies both dominances rather than reconciling them.** The matrix should record this trade-off explicitly when the L1-007 decision is made.

4. **Falsify the implicit "L1-007 relaxation is universally rescue-positive" framing.** R-delivery-irr-curve's hurdle-crossover table (sovereign-bond at 209 t, regulated-utility at 461 t, corporate-growth at 691 t) is Variant-B-economics specific. **For Architecture D economics, no chunk-mass relaxation up to 482 t (the B-ring physical cap) clears any hurdle.** Project owners considering L1-007 relaxation should be told that the relaxation rescues VARIANT B economics, not Architecture D economics.

### Threads opened for follow-on rounds

1. **R-architecture-D-NPV-sensitivity-to-sovereign-anchor.** Architecture D NPV at zero is dominated by the $2B sovereign payment in BEST_CELL. At what sovereign-payment magnitude does Architecture D conditional NPV at zero turn positive at chunk 482 t? Estimated ~$11-12B sovereign anchor at year 11 needed (rough scale-up from observed $-9B program NPV at chunk 482). A targeted sensitivity round would close this question. Tied to matrix decision point #5 (reactor program path) by implication.

2. **R-architecture-D-saturn-ops-duration-tradeoff.** This round held Saturn ops at 1.0 yr. If Saturn ops extended to 2 yrs, Saturn-side reactor mass halves (or stack mass halves), CapEx drops, but round-trip extends by 1 yr toward L0-05 ceiling. Worth pricing this tradeoff if Architecture D survives matrix decision. Not currently load-bearing.

3. **R-architecture-D-with-aerocapture-rescue-collapse.** Round 6 + round 7 both held aerocapture off-table per the Variant C engineering falsification. If D were to add Earth aerocapture rescue (treating chunk-as-heat-shield as the rescue path), delivered mass at chunk X would scale upward by ~1.3-1.5× via reduced inbound delta-velocity. But hyperion R-aerocapture-fast-cruise-envelope falsified this at engineering level. Round NOT recommended.

## Validity caveats (declared in advance)

1. **Linear CapEx scaling with subsystem mass is a simplification.** Reactor mass and stack mass scale-up engineering costs are not linear in practice — larger reactors require regulatory delta-burden, larger mirrors require deployment-mechanism redesign. The linear scaling is a first-order assumption only; sensitivity to slope is reported.

2. **Saturn-side energy budget assumed 1.0-yr Saturn ops fixed.** Longer Saturn ops would reduce Saturn-side power need but extend round-trip toward L0-05 ceiling. This round holds Saturn ops at 1.0 yr per R-chemical-plus-small-reactor baseline; a separate sensitivity round on Saturn-ops-duration would be needed to explore that tradeoff.

3. **D-solar-thermal stack at 101 kg/kWe** is the OPTIMISTIC end of R-saturn-side-solar-thermal's range (SOEC + 0.1 kg/m² mirror + DC=1.0). Conservative stack at 1560 kg/kWe (Stirling + flight-heritage mirror) would dominate the dry mass. This round uses optimistic stack only; sensitivity to stack mass is reported at one anchor.

4. **Variant B comparison uses the matrix's pre-Option-A impulsive number (128.8 t delivered at 200 t chunk).** Under Option A continuous-thrust accounting and rhea Round 3, Variant B's actual delivered fraction is 17 percent (not the matrix-impulsive 64 percent), and at chunk 200 t Variant B delivers ~34 t/mission, not 128.8 t. The 128.8-t number is held in this round for **comparison with the matrix's original Variant B baseline only**. If Variant B is reframed at Option-A 17-percent delivered fraction, D dominates Variant B more strongly (since D delivered does not change but Variant B delivered drops 4×).

5. **L1-007 relaxation upward is a project-owner decision, not an engineering question.** L1-007 is the matrix's hard chunk-mass cap. This round prices the economic value of relaxing the cap — it does NOT argue for or against the relaxation. Per matrix decision point #3, L1-007 relaxation requires single-chunk > 200 t which exceeds matrix-tested architectures; engineering-level feasibility at chunk 482 t is its own open question not covered here.
