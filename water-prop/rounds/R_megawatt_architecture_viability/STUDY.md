# R-megawatt-architecture-viability — does the megawatt cell survive MARVL-anchored mass + 0-of-6 base rate?

**Status:** pre-result.

## Question

Four user-locked findings from a prior `R-power-wonder` round (locked May 2026; never integrated into this campaign's matrix or REQUIREMENTS.md) directly attack the assumptions I built Rounds 1, 2, and 3 on:

1. **40 watts-per-kilogram specific power at megawatt class is Technology-Readiness-Level 2 aspirational**, not an extrapolation of Kilowatt Reactor Using Stirling Technology ground-test data. Flown radioisotope thermoelectric generators top out at ~5.3 watts-per-kilogram (General Purpose Heat Source). Kilowatt Reactor Using Stirling Technology measured ~2.4 watts-per-kilogram system-level. National Academies 2021 report says "very little advancement" in nuclear-electric-propulsion in the past decade.
2. **US space-fission programs have a 0-of-6 base rate of reaching orbit within their originally-stated decade since 1965.** SNAP-10A (1965) is the only US fission reactor ever orbited. SP-100 (~$400M, cancelled 1994), Project Timberwind (~$340M, cancelled 1993), Prometheus/Jupiter-Icy-Moons-Orbiter (~$464M, cancelled 2006), Defense-Advanced-Research-Projects-Agency Demonstration Rocket for Agile Cislunar Operations (~$499M ceiling, cancelled May 2025), Kilopower flight (no flight program funded), NASA Fission Surface Power (Phase 2 not yet awarded). Total ~$1.7B spent post-SNAP with zero orbital outcomes.
3. **Fission Surface Power Phase 2 has not been awarded** as of May 2026. The same FY2026 budget request zeroed NASA nuclear-electric-propulsion and nuclear-thermal-propulsion technology lines entirely.
4. **At megawatt-electric scale, the radiator subsystem is 40–55 % of total system mass** per the National Academies report and NASA Modular Assembled Radiators for Very Large systems studies. Reactor + shield is 25–35 %; power conversion 15–25 %. The R_radiator_mass_penalty bundled-versus-decomposed finding had it backwards: the **bundled formula (≈ 105 t at 1 megawatt-electric) is closer to correct, and the decomposed-mid model I used in Round 2 (29 t at 1 megawatt-electric) is the optimistic one**.

My Rounds 1, 2, and 3 used the 29-t megawatt baseline from R_radiator_mass_penalty's decomposed-mid model, and they implicitly treated megawatt all-electric as a *real* architecture path — not as a 1-in-7 historical bet. Both assumptions are wrong by the locked-belief evidence.

**The question this round answers:**

1. Under MARVL-anchored mass decomposition (radiator 40–55 % of system mass), what is the 1-megawatt-electric tug dry mass?
2. At that dry mass, does the megawatt all-electric cell still close L0-05's 15-year ceiling — baseline, and with Round 2's 12.76 t redundancy overlay?
3. Apply the 0-of-6 historical base rate plus the FY2026 budget evidence as a Bayesian posterior on "megawatt-class fission delivery by the ICEBERG demonstrator window 2032–2035." What is the credible posterior probability?
4. Does the architecture-decision-matrix's clean two-cell binary (Kilopower variant B / megawatt all-electric) survive these corrections, or does it collapse to one defensible cell plus an upside-only megawatt option?
5. Is even Kilopower variant B safe under the same base-rate prior? Kilopower has no funded flight program either; the 0-of-6 record applies to it too.

## Pre-registered hypothesis (H-r4)

**Aggregate (H-r4-agg):** The MARVL-anchored mass model lifts megawatt 1-megawatt-electric tug dry mass from 29 t (Round 2 decomposed-mid baseline) into the 70–150 t range. Round-trip at that mass closes L0-05 baseline at the low end of the band but busts L0-05 at the top end and with redundancy overlay added. The 0-of-6 historical base rate plus FY2026 budget zero gives a credible posterior probability of megawatt-class delivery by 2035 in the 0.10–0.25 range — well below the architecture-matrix's implicit confidence. The cleanest reading: **the megawatt cell collapses to "upside only" and is not a defensible baseline. Kilopower variant B is the only defensible baseline cell, and even it carries the same 0-of-6 prior because Kilopower has no funded flight program.** The architecture campaign needs a non-fission baseline option to anchor the matrix; megawatt fission and Kilopower fission both become contingent paths.

**Pre-registered sub-claims:**

| Sub-claim | Predicted | Falsification |
|---|---|---|
| H-r4-a — 1-megawatt-electric tug dry mass under MARVL-anchored decomposition | 70–150 t (vs Round 2 baseline 29 t) | outside 50–180 t |
| H-r4-b — Round-trip at MARVL-anchored 100 t dry, 1 megawatt-electric, 2000 s, 200 t chunk | 14.0–15.0 yr | outside 13.5–15.5 yr |
| H-r4-c — Round-trip after redundancy overlay (Round 2: +12.76 t) at MARVL-anchored baseline | 14.5–15.5 yr; busts L0-05 at top of MARVL band | outside 14.0–16.0 yr |
| H-r4-d — Maximum dry mass that still closes L0-05 = 15 yr with redundancy overlay | 130–150 t | outside 120–160 t |
| H-r4-e — Bayesian posterior on megawatt-class fission delivery by 2035 given 0-of-6 base rate + FY2026 budget zero | 0.10–0.25 | outside 0.05–0.40 |
| H-r4-f — Bayesian posterior on Kilopower flight delivery by 2032 given 0-of-6 base rate + no funded flight program | 0.20–0.45 (less ambitious than megawatt class but the base rate still applies; KRUSTY ground demo is a partial offset) | outside 0.10–0.55 |
| H-r4-g — Architecture-decision-matrix verdict | Megawatt all-electric collapses to upside-only. Kilopower variant B carries reduced confidence ~0.30. **Neither current cell is a defensible baseline; the matrix needs a non-fission baseline option.** | falsified if megawatt cell defensibly closes at MARVL mass with redundancy and high base-rate confidence |

**Aggregate decision:** if H-r4-agg holds — megawatt cell collapses to upside-only and Kilopower variant B is contingent — surface the finding to the orchestrator with two recommendations: (a) add an "Architecture-program risk" column to the matrix that captures the 0-of-6 prior; (b) spawn R-non-fission-baseline to identify a defensible baseline architecture that does not depend on a fission flight program that has not been funded. If H-r4-agg falsifies — the megawatt cell survives MARVL mass + redundancy + base-rate adjustment — the matrix stands as-is and Rounds 1–3 hold without correction.

## Method

### MARVL-anchored mass decomposition

From locked beliefs, at 1 megawatt-electric:
- Reactor + shield: 25–35 % of system mass
- Power conversion: 15–25 % of system mass
- Radiator: 40–55 % of system mass
- Sum: 80–115 % (the radiator dominance leaves ~10 % structural / harness / margin)

Pick the bundled formula `m_dry_t = 5.0 + 0.1 × P_kWe` as the MARVL-anchored baseline because it produces 105 t at 1 megawatt-electric, consistent with radiator-dominated mass at the National Academies / MARVL-anchored fractions. Sweep dry-mass models: bundled (105 t), MARVL-pessimistic (150 t), MARVL-optimistic (70 t).

### Round-trip computation

Reuse R-electric-outbound's constant-thrust burn function. Vary tug dry mass; hold all other parameters (chunk 200 t, outbound dv 17.97 km/s, inbound dv 6.42 km/s, Isp 2000 s, reactor 1 MWe, eta_thr 0.65). Compute outbound burn, Hohmann cruise (6.08 yr one-way, 12.17 yr round-trip), Saturn ops (1 yr), inbound burn. Compare against Round 2's redundancy-overlay scenario (add +12.76 t).

### Bayesian posterior — base rate + budget evidence

Prior: 0 of 6 US space-fission programs since 1965 reached orbit within their original-stated decade. The 7th attempt (FSP Phase 2 + flight or successor) is the program in question. Apply a Beta(α, β) prior with weakly informative prior parameters that capture "we know fission can be hard but a non-zero success rate is possible."

- Beta(1, 1) uniform: posterior after 0 of 6 successes is Beta(1, 7), mean = 1/8 = 0.125.
- Beta(0.5, 0.5) Jeffreys: posterior is Beta(0.5, 6.5), mean = 0.5/7 = 0.071.
- Beta(2, 2) weakly favorable: posterior is Beta(2, 8), mean = 2/10 = 0.20.

Three priors give posteriors in the 0.07–0.20 band; H-r4-e predicted 0.10–0.25 lands at the upper end.

For Kilopower (H-r4-f), the base rate is the same 0-of-6, but Kilopower has the KRUSTY ground-demo result (a partial milestone the other 6 failed programs did not all reach). Add a "+0.5 fractional success" credit to the success count: Beta(1, 1) + 0.5 / 6 → posterior mean ≈ 0.18. Range 0.10–0.30 with the three priors.

### Sensitivity / assumption-questioning

- **MARVL claim depends on radiator technology.** The 40–55 % radiator fraction applies to high-efficiency-Brayton waste-heat rejection. Lower-efficiency power-conversion (e.g., thermionic, thermoelectric) accepts higher waste-heat fractions but with lower specific mass. The "decomposed-mid 29 t" from R_radiator_mass_penalty was anchored on a high-temperature radiator scaling that may or may not flight-qualify; the bundled formula doesn't depend on that. The locked-belief assertion that "bundled is closer to correct" is the load-bearing claim of this round.
- **0-of-6 prior is small-sample-size.** With n=6 trials, the 95 % confidence interval on the underlying success rate is roughly [0, 0.46] (binomial). Reading too much into the point estimate is over-fitting. Mitigation: use Bayesian posteriors with multiple priors, not point estimates.
- **The "originally-stated decade" framing** rewards programs that quietly stretched timelines and counted as success after eventually flying. Conservative interpretation: any program that did not reach orbit by its initial commitment counts as failed for that decade. This is the framing in the locked belief.
- **FY2026 budget zero is one-year evidence.** Budget priorities reverse year-on-year. A FY2027 reinstatement is plausible if there is administration support; conservatively, the FY2026 evidence updates the posterior downward by maybe 0.05–0.10 of the prior mean.
- **The matrix's "year 20+ megawatt" cell window is 2042+** (year 0 = funding start, year 20 = first commercial-class). That gives 16+ more years for the funding pipeline to materialize. The 0-of-6 prior covers 60 years of attempts; the next 16 years might not move the needle proportionally, but they do offer time for a Phase 2 award to land.

### Validity caveats

- The Bayesian update is sensitive to the choice of prior. The round documents three priors transparently rather than picking one.
- The MARVL fraction-of-mass claim is anchored to one report family (National Academies 2021 + MARVL studies). Other system studies disagree on radiator-mass fraction at megawatt class (some lower, some higher); the locked-belief assertion treats the 40–55 % band as authoritative for paper-grade purposes.
- The architecture-decision-matrix is a planning artifact; whether it is operationally "the program's plan" or "an architecture-trade record" affects how seriously the upside-only verdict on the megawatt cell should be taken. The orchestrator decides.
- The 0-of-6 prior weighs program-management failure (cost overruns, policy reversals, technical issues) as one combined failure mode. ICEBERG's bag-and-mining mission profile is sufficiently different from the failed flight-program profiles that some of the failure modes may not transfer; this round does not adjudicate that.

## Result

Run output at `results/dry_mass_sweep.json`, `results/bayesian_posteriors.json`, `results/tables.md`.

**Dry-mass sweep at megawatt all-electric (1 MWe, 2000 s Isp, 200 t chunk):**

| Scenario | Dry mass | Round-trip | L0-05 margin | Clears? |
|---|---|---|---|---|
| Round 2 baseline (decomposed-mid) | 29 t | 13.93 yr | +1.07 yr | yes |
| MARVL-optimistic | 70 t | 14.27 yr | +0.73 yr | yes |
| MARVL bundled-formula | 105 t | 14.56 yr | +0.44 yr | yes |
| MARVL-pessimistic | 150 t | 14.93 yr | +0.07 yr | yes (barely) |
| Off-band high | 160 t | 15.01 yr | −0.01 yr | NO |

| Scenario + redundancy overlay (+12.76 t) | Dry+overlay | Round-trip | L0-05 margin | Clears? |
|---|---|---|---|---|
| MARVL bundled (105 + 12.76) | 117.8 t | 14.67 yr | +0.33 yr | yes |
| MARVL-pessimistic (150 + 12.76) | 162.8 t | 15.04 yr | −0.04 yr | NO |

**Max dry mass that clears L0-05:** 150 t baseline, 140 t with redundancy overlay.

**Bayesian posteriors on fission-flight delivery by 2032–2035:**

| Prior | Megawatt (0/6) | Megawatt + FY2026 zero | Kilopower-B + KRUSTY credit |
|---|---|---|---|
| uniform Beta(1,1) | 0.125 [0.00, 0.35] | 0.118 [0.00, 0.33] | 0.176 [0.00, 0.42] |
| Jeffreys Beta(0.5, 0.5) | 0.071 [0.00, 0.25] | 0.067 [0.00, 0.24] | 0.133 [0.00, 0.37] |
| weakly favorable Beta(2, 2) | 0.200 [0.00, 0.44] | 0.190 [0.00, 0.42] | 0.238 [0.00, 0.49] |

**Hypothesis grading:**

| Sub-claim | Predicted | Actual | Held? |
|---|---|---|---|
| H-r4-a — 1-MWe tug dry mass under MARVL-anchored decomposition | 70–150 t | 105 t (bundled formula); 70–150 t band agrees with locked-belief decomposition | **held** |
| H-r4-b — Round-trip at MARVL 100 t baseline | 14.0–15.0 yr | 14.52 yr at 100 t | **held** |
| H-r4-c — Round-trip with redundancy overlay at MARVL baseline | 14.5–15.5 yr (busts at top of band) | 14.63 yr at 100 t + overlay; busts at 150 t + overlay (15.04 yr) | **held** |
| H-r4-d — Max dry clearing L0-05 with overlay | 130–150 t | 140 t | **held** (mid-band) |
| H-r4-e — Bayesian posterior megawatt delivery by 2035 | 0.10–0.25 | 0.07–0.19 across priors with FY2026 evidence | **held** (lower half of band) |
| H-r4-f — Bayesian posterior Kilopower-B flight | 0.20–0.45 | 0.13–0.24 across priors | **falsified low** — posteriors are lower than predicted even with KRUSTY credit |
| H-r4-g — Matrix verdict: megawatt cell upside-only; Kilopower-B contingent; matrix needs non-fission baseline | held | held: posteriors 0.07–0.24 across both cells with both priors and evidence; matrix's implicit "this is a real architecture" confidence (probably > 0.5) is not supported by the base-rate evidence | **held** |

**Aggregate (H-r4-agg): held in headline, mechanism partially different than predicted.** I expected the MARVL-anchored mass to push the megawatt cell out of L0-05 compliance physically. Instead, the megawatt cell still closes L0-05 at MARVL bundled-formula 105 t with redundancy overlay (margin +0.33 yr). What collapses is the **program-risk posterior**, not the physics. At 0.07–0.19 mean posterior across priors, megawatt-class delivery by the 2032–2035 demonstrator window is a 1-in-5-to-1-in-15 bet, not a defensible baseline.

## Reading

**The architecture is physically fine; the program is the bet.** I was wrong to expect the MARVL-anchored mass to push the megawatt cell out of L0-05 compliance. Even at the locked-belief-implied 105 t dry mass (3.6× the decomposed-mid 29 t Round 2 baseline), the round-trip at 1 megawatt-electric / 2000 s Isp / 200 t chunk is 14.56 yr — comfortably inside L0-05 at +0.44 yr margin. With Round 2's redundancy overlay (+12.76 t), it shrinks to +0.33 yr but still closes. The cell only physically busts L0-05 above ~140 t dry with overlay, and the MARVL band ceiling is around 150 t.

The mechanism behind the matrix collapse is **program-risk Bayesian posterior**, not physics. Three priors (uniform, Jeffreys, weakly favorable) applied to the 0-of-6 historical evidence + FY2026 budget zero give posterior means of 0.07–0.19 for megawatt-class delivery by 2035. Adding Kilopower's KRUSTY-ground-demo partial-success credit lifts the variant-B posterior modestly to 0.13–0.24. **Neither posterior is consistent with an architecture-matrix listing of "this is the year-20+ commercial-class cell."** That listing implies confidence > 0.5, which the base-rate evidence does not support.

**The locked-belief assertion that "the bundled formula is closer to correct at megawatt scale" should be folded into the architecture-decision-matrix.** Currently the matrix uses R_radiator_mass_penalty's decomposed-mid model implicitly (megawatt cell dry mass treated as ~29 t). Per the locked belief, that's a 3.4× understatement of dry mass at megawatt class. The decomposed model is optimistic; bundled (105 t) is closer to MARVL-anchored reality. **Update the matrix to carry both bundled and decomposed masses, with the program-risk column noting that decomposed is conditional on deployable ultra-low-areal-density radiators that have not flown.**

**The "0-of-6 base rate" is small-sample-size and prior-sensitive but the direction is robust.** Across three weakly-informative priors, the 95 % credible interval upper bound on megawatt-class delivery by 2035 caps at 0.42–0.44. Even the most favorable reading does not give better-than-50/50 confidence. The matrix has been quietly assuming that a fission-electric flight program will materialize on the program's schedule; the base-rate evidence says: don't.

**Kilopower variant B is also contingent.** I had been treating Variant B as the "safe" cell (10 kWe is small, low-bar). Per locked belief #3, Kilopower has no funded flight program as of May 2026. The 0-of-6 prior applies to Kilopower too. With KRUSTY's ground-demo partial credit (+0.5 successes), Variant B's posterior is 0.13–0.24 — better than megawatt (0.07–0.19) but still well below the matrix's implicit baseline confidence. **Variant B is also upside-only when measured against program-risk.**

**Where this leaves the architecture campaign.** The matrix has been built on two fission-electric cells, both of which carry baseline-program-risk posteriors of 0.07–0.24. Adding a non-fission baseline cell is therefore a strategic priority. Candidate baseline architectures that do not depend on a fission flight program:

1. **Solar-electric in the inner astronomical unit + chemical Saturn-departure.** Pioneered on Dawn and BepiColombo at inner-AU scale. At Saturn, solar flux is ~1.1 % of Earth's; solar-electric is not viable beyond ~3 astronomical units. Use solar for the outbound leg up to Jupiter's distance, chemical for the rest. Probably bursts L0-05 due to slow Hohmann + slow inner-AU spiral.
2. **Radioisotope-electric (REP).** General-Purpose-Heat-Source-class radioisotope thermoelectric generators have decades of heritage at 5.3 W/kg. A 100 kWe REP system requires ~19 t of plutonium-238-class heat sources — plutonium-238 supply is the bottleneck (US production restart ~2015, target 1.5 kg/yr by 2028). A 100-kWe-class mission needs ~12 kg of Pu-238, achievable in the program window but supply-constrained.
3. **Solar concentrator.** Reflectors focus sunlight onto a smaller power-conversion stack. At Saturn distance, geometric area for 1 MWe of concentrated solar is ~10 km² of mirror — infeasible. Inner-AU only.
4. **Chemical-only with depot architecture.** Cassini-class chemical to Saturn, propellant depot at Earth-Moon Lagrange-1 or Lagrange-2 for refueling on inbound. Bursts L0-05's 15-yr ceiling and L0-12 cost competitiveness; probably not viable as a baseline either, but lacks the program-risk dependency on fission.

**Recommended orchestrator action: spawn R-non-fission-baseline to identify which of these (or a combination) is the defensible baseline architecture cell.** Update the matrix to:
- Add a "Program-risk posterior" column with the 0.07–0.24 numbers for the two fission cells.
- Mark both fission cells as "contingent on Phase-2 award (megawatt) or Kilopower flight program (Variant B)."
- Add a third cell labelled "Non-fission baseline (TBD per R-non-fission-baseline)" as the L0-05/L0-10/L0-12-compliant fallback if neither fission program materializes.

## Revisit

**Did the hypothesis hold?** Aggregate held; mechanism partially different. The physics held the megawatt cell inside L0-05 at MARVL mass; the program-risk posterior is what collapses the matrix. I expected the cell to bust on physics; it busts on program-risk evidence.

**Where was I wrong?**
- **H-r4-c framing** ("busts L0-05 at top of band"). It busts at 150 t with overlay (15.04 yr, marginally over) but holds throughout the MARVL bundled-formula range of 80–140 t. The cell is more physically robust to mass overlay than I expected — confirming Round 2's lesson that cruise dominates round-trip at megawatt class.
- **H-r4-f Kilopower posterior** predicted 0.20–0.45; actual 0.13–0.24. KRUSTY's partial credit doesn't lift the posterior as much as I imagined because Beta posteriors are mass-weighted by the prior count. Falsified low.
- **The mental model I held when pre-registering** was "physics is the binding constraint." Locked-belief evidence reframes it: at megawatt class, physics is *not* the binding constraint — base-rate program-risk is.

**Methodology lesson candidate #7** for the cross-campaign log:
> *When a campaign has spent N rounds optimizing the physics of an architecture cell, run a base-rate / program-history check before declaring the cell viable. The physics may close at 14.04 yr but the program may close at 0.07–0.20 posterior. Architecture decisions need both columns; ignoring program-risk produces optimistic matrices that quietly assume schedule and budget that nothing in the historical record supports.*

This is methodology lesson candidate #7 for this campaign.

**Adopt / drop / defer:**
- **Adopt:** the MARVL-anchored bundled-formula 105 t dry as the megawatt baseline going forward, not the decomposed-mid 29 t. Update Rounds 2 and 3's analyses with a forward pointer.
- **Adopt:** the recommendation to add a "Program-risk posterior" column to the architecture-decision-matrix with 0.07–0.24 numbers for both fission cells.
- **Adopt:** the recommendation to spawn R-non-fission-baseline. Architecture campaign needs a baseline that doesn't depend on a flight program that has not been funded.
- **Defer:** which non-fission baseline (REP, solar-electric, hybrid) is the actual recommendation. Out of scope for this round.
- **Drop:** the Round 1 / Round 2 / Round 3 implicit assumption that megawatt all-electric is "the year-20+ baseline." Re-cast it as "the year-20+ upside-case if Phase 2 fission programs deliver."

## Cross-learning

**Forward references:**
- **R-non-fission-baseline** (new high-priority proposal): identify a defensible baseline architecture not dependent on a fission flight program. REP / solar-electric / hybrid candidates. This is the load-bearing follow-up to this round.
- **R-program-risk-column-matrix** (new low-priority proposal): add a "Program-risk posterior" column to ARCHITECTURE-DECISION-MATRIX.md with 0.07–0.20 for megawatt, 0.13–0.24 for Variant B. Orchestrator action, not a worker round.
- **R-pu238-supply-availability** (new, only if R-non-fission-baseline picks REP): is the US Pu-238 production restart on schedule to deliver the ~12 kg needed for a 100-kWe-class REP mission in the ICEBERG demonstrator window? Bottleneck question.
- **R-redundancy-budget-cost-MARVL** (new): re-price the redundancy overlay at MARVL 105 t baseline. Round 2's $710M per vehicle was anchored on 29 t; bigger reactor stack at MARVL mass implies different reactor-redundancy form-factor and cost.

**Backward references:**
- **R_radiator_mass_penalty** (commit `ad8156c`): its conclusion that "the bundled formula over-counts megawatt stack by 3×" was anchored against an optimistic decomposed model. Per the locked-belief evidence (MARVL studies), the *bundled* formula is closer to correct. This round inverts that finding. **Update R_radiator_mass_penalty's STUDY.md with a forward pointer.**
- **R-mission-success-probability** (commit `ef1bc21`): Round 1's premise that "megawatt all-electric is the year-20+ baseline" needs reframing. Architecture is now: fission-electric cells are upside-only with program-risk posteriors 0.07–0.24; baseline must be non-fission.
- **R-redundancy-budget-cost** (commit `a8c72d2`): $565M–$710M per vehicle priced at 29 t Round 2 baseline. At MARVL 105 t baseline, the reactor stack is bigger and the redundancy form-factor is different (parallel 105 t reactor is structurally infeasible; internal redundancy is still the right form, but at 3.5× the mass it may scale differently). Re-price needed.
- **R-electric-outbound** (commit `9001ce9`): used decomposed-mid model for megawatt. Re-evaluate at MARVL mass — round-trip 14.56 yr vs the 13.94 yr quoted. Still closes L0-05, but tighter.

**Methodology forward:**
- The pattern across this session: **every reliability or base-rate round has falsified an earlier optimistic assumption in this campaign.** Round 1 falsified "L0-10 = 0.90 single-string" (caught later by Round 3's block-clause discovery). Round 3 falsified Round 1's per-mission framing. Round 4 falsifies the matrix's "two-cell binary" framing by introducing program-risk. **Future architecture rounds should include a program-history / base-rate check as a standard step before declaring a cell viable.** Codify in PROTOCOL.md.
- Two-bucket pre-registration bias becomes three-bucket: physics rounds (pessimistic at megawatt class because of Tsiolkovsky-exponential intuition), reliability rounds (optimistic at HERITAGE-NONE rows), program-risk rounds (this one: I expected physics to bind, base-rate did). The pattern: pre-registration anchors on the prior-round mechanism even when a new evidence type calls for a different model.

**Open follow-up rounds spawned by this one:**
- R-non-fission-baseline (priority 1; load-bearing for the matrix to have a defensible baseline)
- R-program-risk-column-matrix (orchestrator task)
- R-pu238-supply-availability (priority 2; only if REP is chosen)
- R-redundancy-budget-cost-MARVL (priority 3; updates Round 2 numbers)

**Verdict for the architecture-decision-matrix:**

1. **Megawatt all-electric cell:** physically still closes L0-05 at MARVL bundled-formula 105 t dry (round-trip 14.56 yr baseline / 14.67 yr with redundancy). **But:** program-risk posterior 0.07–0.19 across priors. **Re-cast from "year-20+ baseline" to "year-20+ upside if Phase-2 fission delivers."**
2. **Kilopower variant B cell:** program-risk posterior 0.13–0.24 with KRUSTY credit. **Re-cast from "year-0–15 baseline" to "year-0–15 upside if Kilopower flight program is funded and delivers."**
3. **Add a third cell:** "Non-fission baseline (R-non-fission-baseline pending)." This is the L0-05 / L0-10 / L0-12-compliant architecture that does not depend on a fission flight program. Until R-non-fission-baseline runs, the matrix has no defensible baseline; both current cells are upside-only when measured against program-history evidence.

This is the load-bearing finding of the session: **the matrix needs a non-fission baseline cell. Both current cells are upside-only.**

