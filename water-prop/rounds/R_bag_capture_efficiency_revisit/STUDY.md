# R-bag-capture-efficiency-revisit — propagating η_c < 1.0 through the architecture decision matrix

**Status:** pre-result.
**Worker:** hyperion (parallel session, orthogonal to titan's R-inbound-delta-v-continuous-thrust).

## Question

Every round in the water-prop campaign has implicitly held the bag capture efficiency η_c at 1.0. The end-of-day handoff document (HANDOFF-2026-05-15-EOD.md) lists "R-bag-capture-efficiency-revisit" as candidate next round #4 specifically because of this:

> "Bag efficiency held at 1.0 in all rounds; realistic 0.68–0.90 per bag-engineering doc. Multiplies delivered mass uniformly; doesn't change matrix shape but does change absolute economics."

The end-of-day handoff's prediction — "doesn't change matrix shape" — is the prediction this round tests. It is exactly the kind of unchecked assumption the user asked to be questioned. Three structural reasons the prediction may be wrong:

1. **The decomposition is mixed.** `ICEBERG-bag-engineering.md §6` decomposes η_c into three serial terms: `η_bag × η_feed × η_thruster`. The first two represent **mass lost before propulsive use** (bag escape, frost stranded in cold wall). The third represents **specific-impulse degradation during the burn** (thruster efficiency). The bag-engineering document folds all three into an effective-Isp degradation in its sensitivity table. That is a first-order approximation. Mass-loss-before-burn and effective-Isp degradation have different non-linear interactions with the inbound rocket equation, especially for cells where m_tug is comparable to chunk mass.
2. **The thruster-efficiency range is microwave-electrothermal-thruster specific.** The bag-engineering document quotes η_thruster of 0.75–0.92 from the microwave electrothermal thruster open literature. The architecture decision matrix's **megawatt all-electric end-to-end** winner uses radio-frequency ion thrusters at Isp 5000 seconds. Radio-frequency ion thrusters typically run 0.65–0.75 total efficiency (NASA Evolutionary Xenon Thruster / NEXT data, scaled to water propellant). Composite η_c for the megawatt era may be **lower** than the bag-engineering document's 0.68 floor, which was derived from microwave-electrothermal-thruster numbers.
3. **The bag-engineering document only checks one cell.** Its sensitivity table uses Δv 4.2 km/s, Isp 700 s — the Kilopower microwave-electrothermal-thruster operating point. The matrix's two surviving winners are **Kilopower Variant B** (chunk-fed chemical departure, electric inbound at Isp 2000 s) and **megawatt all-electric** (electric end-to-end at Isp 5000 s). Neither matches the bag-engineering document's test cell. The doc's "doesn't threaten the thesis" conclusion may not extend.

**The question this round answers:**

For each cell in the architecture decision matrix at the current end-of-day state — separating the two physical loss mechanisms (mass-loss-before-burn `η_bag × η_feed`, versus Isp-degradation-during-burn `η_thruster`) — what is the delivered customer mass, the round-trip time, and the depot-fill mission ramp count, across the realistic range of η_c per era?

Specifically:

- Does the architecture-decision-matrix **winner set** (Kilopower Variant B + megawatt all-electric) survive η_c ∈ [0.55, 0.90]?
- Is there any matrix cell that **flips** between L0-05-compliant and L0-05-non-compliant as η_c drops?
- Does the megawatt era's radio-frequency-ion-thruster efficiency drag composite η_c below the bag-engineering document's stated 0.68 floor?

## Pre-registered hypothesis (H-bcer)

Pre-registration discipline (campaign convention §9): widen the falsification band on whichever side I am tempted to call as "obvious." The end-of-day handoff document said "doesn't change matrix shape" — that is the optimistic call. So I widen on the **pessimistic** side: I bias toward predicting that at least one matrix cell flips.

**Aggregate (H-bcer-agg):** At realistic per-era composite η_c (megawatt era 0.55–0.70; Kilopower era 0.68–0.85), **the matrix shape changes in at least one of the following three ways**:

- (a) at least one matrix cell that closes L0-05 at η_c=1.0 fails to close at the realistic η_c for its era, OR
- (b) the depot-fill mission ramp for the sub-megawatt sweet spot (100 kilowatt-electric / 200 tonne chunk) doubles or worse (from 1 mission to ≥ 2), OR
- (c) the megawatt-era composite η_c drops below 0.60 (below the bag-engineering document's stated 0.68 floor).

**Pre-registered sub-claims (numeric):**

| Sub-claim | Predicted band | Falsification |
|---|---|---|
| H-bcer-a — Megawatt-era composite η_c using radio-frequency ion thruster efficiency 0.70 mid, η_bag 0.97, η_feed 0.95 | 0.60–0.70 | outside this band |
| H-bcer-b — Megawatt all-electric (1000 kilowatt-electric, 500 tonne chunk) delivered customer mass at composite η_c 0.65, relative to η_c 1.0 baseline | reduced 35–55% | outside this band |
| H-bcer-c — Megawatt all-electric round-trip time at composite η_c 0.65, relative to η_c 1.0 baseline | within ±1.0 year of baseline (could go either way because smaller chunk reduces inbound burn time but lower thruster Isp increases it) | outside ±1.0 yr |
| H-bcer-d — Kilopower Variant B (10 kilowatt-electric, 100 tonne chunk) critical η_c floor where delivered customer mass = 0 | 0.20–0.40 | outside band, or above 0.55 |
| H-bcer-e — Depot-fill mission ramp at 100 kilowatt-electric / 200 tonne sweet spot, at composite η_c 0.78 (Kilopower-era mid) | increases from 1 to 2–4 missions | outside this band |
| H-bcer-f — At least one matrix cell that closes L0-05 at η_c=1.0 fails at its realistic per-era η_c | true | false (no cell flips) |
| H-bcer-g — Treating η_c as effective-Isp degradation (bag-engineering document convention) versus as chunk-mass reduction gives different delivered-mass predictions for cells where m_tug > 10% of chunk mass | divergence > 5% relative | divergence < 5% |

**Aggregate decision rule:** if H-bcer-agg holds (any of a, b, c), the architecture decision matrix needs a per-era η_c-realistic delivered-mass column, and the depot-fill ramp table needs a second-row "η_c-realistic" version. If H-bcer-agg falsifies (matrix shape stable across the realistic range), the end-of-day handoff's "doesn't change matrix shape" conclusion is confirmed and η_c can stay as a uniform footnote.

## Method

### Two-mechanism decomposition

The bag-engineering document folds three terms into one effective η_c, then uses effective-Isp degradation in its sensitivity table:

```
m_0 / m_f = exp(Δv / (η_c × v_e))
```

This round splits the three terms into two physical mechanisms:

1. **η_pre = η_bag × η_feed** — mass-loss-before-burn. The chunk that arrives at Saturn departure is the *intended* chunk multiplied by η_pre. Water lost to bag escape or stranded as un-re-sublimable cold-wall frost reduces both the deliverable mass and the propellant available for inbound. Modeled as pre-burn chunk mass reduction.
2. **η_thr = η_thruster** — specific-impulse degradation during inbound burn. Water that reaches the thruster but is not propulsively utilized exits at low velocity, contributing mass flow but little thrust. Modeled as effective exhaust velocity reduced by factor η_thr.

Net: the rocket equation for inbound becomes

```
m_initial = m_tug + η_pre × m_chunk_intended
v_e_effective = η_thr × Isp_nominal × g0
m_final = m_initial / exp(Δv_inbound / v_e_effective)
delivered_mass = m_final - m_tug
```

Note the asymmetry: if `m_tug` is large relative to `η_pre × m_chunk_intended`, the final delivered mass can go negative — the architecture stops closing.

### Per-era thruster choices and η_c ranges

From the architecture decision matrix:

| Era | Reactor (kilowatt-electric) | Thruster | Isp (s) | η_thr range | η_pre range | Composite η_c range |
|---|---:|---|---:|---|---|---|
| Kilopower-microwave-electrothermal-thruster | 10 | Microwave electrothermal | 700 | 0.75–0.92 | 0.90–0.94 | 0.68–0.87 |
| Kilopower Variant B (matrix winner) | 10 | Radio-frequency ion (inbound) | 2000 | 0.65–0.75 | 0.90–0.94 | 0.59–0.71 |
| Fission Surface Power / 40 kilowatt-electric | 40 | Radio-frequency ion | 2000 | 0.65–0.75 | 0.90–0.94 | 0.59–0.71 |
| Sub-megawatt | 200 | Radio-frequency ion | 2934 | 0.65–0.75 | 0.90–0.94 | 0.59–0.71 |
| Megawatt all-electric (matrix winner) | 1000 | Dual-ion (radio-frequency ion + microwave-electrothermal hybrid) | 5000 | 0.65–0.75 | 0.90–0.94 | 0.59–0.71 |

The microwave-electrothermal-thruster row matches the bag-engineering document's table; every other row is sub-document. Radio-frequency-ion thrusters have higher specific impulse but lower total efficiency than microwave-electrothermal at the operating points relevant to this campaign. NASA Evolutionary Xenon Thruster running on xenon delivers ~0.70 total efficiency at 4000 s; water-propellant radio-frequency ion is projected lower because water dissociates and scavenges electrons. Estimating water-propellant radio-frequency ion efficiency at 0.65–0.75 is generous on the high end.

### Sweep axes

- Composite η_c: [0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.00]
- Decomposition: at each composite η_c, evaluate both pure-η_pre (all loss is mass-before-burn) and pure-η_thr (all loss is Isp degradation) as bounds; report mid (η_pre = η_thr = sqrt(η_c)) as the midpoint case
- Matrix cells: Kilopower Variant B (10 kilowatt-electric / 100 tonne chunk, Δv 6.42 km/s electric inbound at Isp 2000 s); megawatt all-electric (1000 kilowatt-electric / 500 tonne chunk, Δv 6.42 km/s electric inbound at Isp 5000 s); sub-megawatt sweet spot (100 kilowatt-electric / 200 tonne chunk, Isp 2934 s). All inbound delta-v held at 6.42 km/s per matrix; titan is testing whether that's the correct number — this round is orthogonal and accepts 6.42 km/s as input.
- Tug mass: decomposed-mid model from R-radiator-mass-penalty (campaign-consensus number).

### Outputs

For each (cell, η_c, decomposition mode):
- Delivered customer mass (tonnes)
- Inbound burn time (years)
- Round-trip time (years)
- Closes L0-05 (yes/no)

Plus three derived tables:
- Critical η_c floor per cell (where delivered = 0)
- Depot-fill mission ramp at per-era realistic η_c versus η_c = 1.0 (for 100 kilowatt-electric / 200 tonne sweet spot)
- Composite η_c per era using realistic thruster efficiencies (re-derive the bag-engineering document's table for radio-frequency ion and dual-ion)

### Validity caveats

- Outbound burn unaffected by η_c (vehicle is empty going out; chunk not yet captured).
- Saturn ops time unaffected by η_c (1 year fixed budget).
- Hohmann cruise unaffected (ballistic).
- Mass model held at decomposed-mid; bundled-10-W/kg sensitivity not run (R-radiator-mass-penalty established the two models agree within one reactor class).
- η_c held constant across the inbound burn; in reality η_thr could degrade as the chunk is consumed and propellant feed dynamics change. This is a tractable extension but out of scope for the present round.
- Variant B chemical Saturn-departure is **not** modeled here; only the electric inbound leg. Variant B's chemical kick stage burns to depletion and is jettisoned, so η_c does not directly degrade the chemical leg. The electric inbound at 3 km/s (post-chemical-offload residual) is what η_c reduces. Round-trip totals for Variant B will be computed against the electric leg only.

## Findings

**Status:** post-result.

### Headline (four findings, in order of strategic weight)

1. **Per-era thruster choice drags megawatt composite η_c below the bag-engineering document's stated floor.** When the bag-engineering document's microwave-electrothermal-thruster efficiency range (0.75–0.92) is replaced with the radio-frequency-ion-thruster efficiency range that actually applies to the matrix's megawatt-all-electric winner (0.65–0.75, scaled from xenon-propellant NASA Evolutionary Xenon Thruster data with a margin for water-propellant chemistry), composite η_c falls to 0.599–0.691 (mid 0.645). The bag-engineering document's "0.80 design point with 0.30 margin to cliff" claim is **microwave-electrothermal-thruster-specific** and **does not extend to the matrix's radio-frequency-ion-based megawatt-era winner**. The honest design number for megawatt era is composite η_c ≈ 0.65, not 0.80. Margin to the η_c < 0.5 cliff drops from 0.30 to 0.15. (Sub-claim H-bcer-a held.)

2. **The bag-engineering document's effective-Isp-only convention understates delivered-mass reduction by a factor of 3–5×.** Treating η_c as pure effective-specific-impulse degradation (the document's convention, where `m_0/m_f = exp(Δv / (η_c·v_e))`) predicts ~7% delivered-mass reduction at composite η_c = 0.65. Treating η_c as pure pre-burn mass loss predicts ~35% reduction. The two physical loss mechanisms (η_bag·η_feed is mass-loss-before-burn; η_thr is specific-impulse-degradation-during-burn) have non-equivalent rocket-equation interactions because mass loss before burn shrinks the inbound rocket equation's initial mass while specific-impulse loss only degrades the exhaust velocity. A balanced (mid) decomposition predicts ~22% reduction for the megawatt cell. The document's table is an apples-to-oranges comparison: it folds three serial efficiencies into one effective-Isp number without checking that the physical loss mechanisms map to that approximation. (Sub-claim H-bcer-g falsified high — divergence is 22–30% across all cells, larger than the predicted 5% threshold, and present even in cells where tug mass is small.)

3. **The architecture-decision-matrix's promised round-trip times for stretch and megawatt all-electric cannot be reproduced from Hohmann cruise plus constant-thrust electric burn at decomposed-mid mass.** Hohmann transfer Earth-to-Saturn alone is 6.09 years each way (computed first-principles from `π·sqrt(a_h³/GM_sun)` with `a_h = (1 + 9.5826) AU / 2`). Round-trip ballistic-coast time is 12.18 years. Adding 1 year Saturn-operations budget leaves only **1.82 years** for outbound burn + inbound burn combined under L0-05's 15-year ceiling. At the matrix's stated megawatt configuration (1000 kilowatt-electric, 500-tonne chunk, specific impulse 5000 seconds, decomposed-mid tug mass 32 tonnes), inbound burn alone is 3.83 years — by itself enough to burst the budget. Round-trip is 17.52 years at η_c = 1.0. The matrix's promised 12–17-year round trip for megawatt era requires assumptions beyond Hohmann + constant-thrust-electric — most likely **40 watts-per-kilogram specific power** (which the matrix row explicitly notes for the 12-year line) or **non-Hohmann low-thrust trajectory** (which has not been quantitatively closed in any campaign round). Until one or both of those is closed, the matrix's megawatt-all-electric winner is **L0-05-non-compliant at the conservative-but-honest baseline** (10 watts-per-kilogram, Hohmann cruise). Stretch (100 kilowatt-electric) and sub-megawatt (200 kilowatt-electric) are also non-compliant at the same baseline. (Sub-claim H-bcer-f held by accident — the L0-05 flip is happening at η_c = 1.0 already, not because of η_c < 1.0. The η_c effect on closure status is secondary; the primary driver is the matrix's hidden specific-power and trajectory assumptions.)

4. **A bug in R-electric-outbound's outbound-burn-time formula understates outbound burn by factor 1/mass-ratio (~2.5× at megawatt era).** R-electric-outbound `run.py:148` computes `m_prop = m_initial × (1 - 1/mass_ratio)` with `m_initial` documented as the wet-mass-at-start-of-burn. The function is called for outbound at `run.py:223` with `m_tug_t` (the dry mass at end of outbound burn, not the wet mass at start). For a burn with mass ratio 2.50, this returns `m_prop = m_tug × 0.60` instead of the correct `m_prop = m_tug × (mass_ratio − 1) = m_tug × 1.50`. Outbound propellant and burn time are understated by `1/mass_ratio ≈ 0.40` at the megawatt operating point. Correcting the bug pushes 1000-kilowatt-electric / decomposed-mid outbound burn from R-electric-outbound's reported **0.17 years** to **~0.42 years** and 500-kilowatt-electric outbound burn similarly upward. Round-trip totals at 500 kilowatt-electric were reported at 14.49 years (claimed L0-05-compliant); the corrected outbound budget pushes that to ~14.7–15.0 years, **brushing or breaching L0-05**. The reported "smallest reactor closing inside 15 years (decomposed-mid) = 500 kilowatt-electric" claim is therefore **on or just past the L0-05 boundary**, not comfortably inside it. The inbound-burn call at `run.py:236` passes `m_tug + chunk` which IS the wet mass at start of inbound — so inbound burns are correctly computed. Bug is **contained to outbound** but propagates into every round-trip total in R-electric-outbound's tables.

### Hypothesis grading (numeric)

| Sub-claim | Predicted | Actual | Held? |
|---|---|---|---|
| H-bcer-a — megawatt-era composite η_c mid | [0.60, 0.70] | 0.645 | **yes** |
| H-bcer-b — megawatt delivered-mass reduction at composite η_c = 0.65 | 35–55% | 22.3% (mid decomp) / 7.4% (pure-thr) / 35.4% (pure-pre) | **no** — falsified low under mid decomp; pure-pre is inside band, pure-thr is far below |
| H-bcer-c — megawatt round-trip change at composite η_c = 0.65 | ±1.0 year | -1.34 years (round-trip *shortens* with lower η_c because less mass to push) | **no** — falsified low; direction predicted correctly (either-way disclaimer in pre-reg saved the call from being more wrong) |
| H-bcer-d — Kilopower Variant B critical η_c floor | [0.20, 0.40] | ≤ 0.55 (sweep bottoms out — true floor not bracketed) | **no** — sweep range too narrow on the low side; true floor is below 0.55 |
| H-bcer-e — Stretch depot-fill ramp at η_c = 0.80 | 2–4 missions | 3 missions | **yes** |
| H-bcer-f — at least one matrix winner flips L0-05 status | true | true (stretch + megawatt both flip) — but flip is driven by baseline-modeling discrepancy with R-electric-outbound, not by η_c | **yes (by accident)** |
| H-bcer-g — pure_pre vs pure_thr divergence > 5% relative where tug mass > 10% of chunk | > 5% in qualified cells | 22–30% across all cells, including cells with small tug mass | **no** — falsified high; divergence is broader and larger than predicted |

**Aggregate (H-bcer-agg) held.** The matrix shape does change — but the strategically-weightiest reason is not what I pre-registered. I pre-registered: matrix cells flip L0-05 status because of η_c. Actual: matrix cells were already L0-05-non-compliant at η_c = 1.0 under a faithful Hohmann + decomposed-mid model; R-electric-outbound's closure claim depends on a propellant-formula bug at outbound. The η_c effect on delivery is real (and the doc's "doesn't threaten the thesis" was right *on its own terms*) but the deeper finding is that the matrix's closure claim is upstream-overstated.

### Methodology lessons (for the cross-campaign convention log)

1. **Composite efficiencies decomposed into different physical loss mechanisms (mass-loss versus exhaust-velocity-degradation) do not commute under the rocket equation.** Folding η_bag, η_feed, and η_thr into a single effective-Isp degradation is a first-order approximation; for cells where the two mechanisms have meaningful weight, the approximation diverges by 20-30% from a balanced treatment. Future η_c-style sensitivity analyses should propagate the two mechanisms separately and report bounds.
2. **A documented assumption that has "been held silently across all prior rounds" is exactly where to look for upstream errors.** The handoff document predicted "η_c < 1.0 doesn't change matrix shape." The actual matrix-shape change comes not from η_c itself but from finding that the matrix's L0-05 closure claim depended on a transcription bug at R-electric-outbound that was downstream of the silent η_c = 1.0 assumption. The "this won't change much" intuition can be a flag that nobody has actually checked it.
3. **Lesson #3 from end-of-day handoff (pre-registration bias is pessimistic) confirmed again, with a twist.** Three of seven sub-claims falsified low (less reduction / less change than predicted). The aggregate held but for the wrong reason. When pre-registering, ask both "where could this be 2× worse?" AND "what *other* failure modes does the model expose that I haven't pre-registered for?"

### Recommendations to orchestrator

1. **Fix the R-electric-outbound outbound-burn bug** (`run.py:148` and call site at `run.py:223`). Re-run R-electric-outbound. Update the architecture decision matrix's L0-05 closure column based on corrected outbound burn times. The matrix may collapse further (some currently-claimed-compliant cells may now be non-compliant).
2. **Audit whether 40-watts-per-kilogram specific power is the load-bearing assumption** for megawatt all-electric L0-05 closure. The matrix row notes it as a stretch parameter. If the only way megawatt closes is at 40-watts-per-kilogram, the megawatt-all-electric architecture inherits the specific-power gating risk explicitly.
3. **Decide between two conventions for η_c sensitivity going forward**: (a) report all three modes (pure-pre, pure-thr, mid) for every cell, or (b) commit to mid as the campaign-standard convention and footnote the bounds. Suggest (a) for the next two rounds and (b) for the final architecture handoff.
4. **Update REQUIREMENTS.md L0-05 narrative** to say the 15-year ceiling is being tested against the Hohmann + decomposed-mid baseline (which currently fails) rather than against the matrix's stated round-trip times (which depend on un-closed specific-power and trajectory assumptions).
5. **Coordinate with titan:** titan is testing inbound-Δv-continuous-thrust; this round's findings about the bug at outbound are orthogonal and additive. The two rounds together suggest the matrix has both an outbound-burn-time error and an inbound-Δv error. The corrected matrix may have NO L0-05-compliant cell — which is a much larger finding than either round alone.

