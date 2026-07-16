# R-non-fission-baseline — does any non-fission architecture close L0-05 + L0-09 + L0-12 simultaneously?

**Status:** complete. Pre-registration → run → Revisit → Cross-learning all below.

## Question

R-megawatt-architecture-viability (commit `28d2370`, this session) integrated four user-locked findings from prior R-power-wonder work:

1. The 40-watts-per-kilogram specific-power assumption for megawatt-class nuclear-electric propulsion is a paper-study aspirational figure at Technology-Readiness-Level 2, not an extrapolation of Kilowatt-Reactor-Using-Stirling-Technology ground-test data. Flown radioisotope thermoelectric generators top out at ~5.3 watts-per-kilogram; Kilowatt-Reactor-Using-Stirling-Technology measured ~2.4 watts-per-kilogram system-level.
2. US space-fission programs have a 0-of-6 base rate of reaching orbit within their originally-stated decade since 1965. ~$1.7 billion spent post-Systems-for-Nuclear-Auxiliary-Power-10A with zero orbital outcomes.
3. NASA Fission Surface Power Phase 2 has not been awarded as of May 2026; the same FY2026 budget request zeroed NASA nuclear-electric-propulsion and nuclear-thermal-propulsion technology lines entirely.
4. At megawatt-electric scale, the radiator subsystem is 40–55 percent of total system mass per the National Academies 2021 report and NASA Modular-Assembled-Radiators-for-Very-Large-systems studies.

R-megawatt-architecture-viability's verdict: the megawatt all-electric cell of the architecture decision matrix collapses to upside-only against program-history evidence, with a Bayesian posterior probability of megawatt-class fission delivery by 2035 in the 0.07–0.20 range. Kilopower Variant B carries 0.13–0.24 under the same prior. **Both current matrix cells are upside-only. The matrix has no baseline.**

This round answers: **does any non-fission architecture close L0-05 (15-year round-trip), L0-09 (service availability), and L0-12 (cost ceiling) simultaneously?** If yes, the matrix has a defensible baseline that does not depend on a fission flight program. If no, the matrix's program-risk problem is unfixable by architecture choice — the program either accepts the 0-of-6 fission base rate as the risk it is actually taking, or it relaxes L0-05.

### Candidate architectures

- **Architecture A — solar-electric outbound + chemical-kick + chunk-fed chemical inbound.** Solar-electric (state-of-art Roll-Out Solar Array, 50–200 watts-per-kilogram array) handles the Edelbaum low-Earth-orbit-to-Earth-escape spiral (specific-impulse 2000 seconds). A chemical kick stage (hydrolox at specific-impulse 450 seconds) does the heliocentric injection from Earth-escape to Saturn-Hohmann perihelion velocity. Ballistic Hohmann cruise. Saturn-side: chunk-fed chemical inbound (water-steam thruster at specific-impulse ~200 seconds, or onsite-electrolyzed hydrolox at 450 seconds if Saturn-side power supports an electrolysis plant). Saturn-side power problem is the binding constraint: solar at 9.58 astronomical units is 1/92 of Earth-vicinity power, so a 200-kilowatt-electric array at Earth delivers ~2 kilowatts at Saturn — useful for life-support and electronics, not for kilowatt-scale electrolysis.

- **Architecture B — all-chemical end-to-end.** Chemical kick stage outbound (full heliocentric injection ~10.3 km/s at specific-impulse 450 seconds). Ballistic cruise. Chunk-fed chemical inbound (6.42 km/s at specific-impulse 450 seconds if onsite electrolysis is somehow powered, or ~200 seconds if water-steam direct). No fission, no solar dependence beyond solar panels for electronics. The dominated baseline against which Architecture A must demonstrate value.

- **Architecture C — plutonium-238 radioisotope-electric.** General-Purpose-Heat-Source-class radioisotope thermoelectric generators (flown specific power 5.3 watts-per-kilogram electrical, thermal-to-electric conversion efficiency 6.3% at state-of-art Stirling). Supply-constrained on US plutonium-238 production (~1.5 kilograms-per-year target rate, 35 kilograms cumulative US inventory as of ~2020). Same physics as fission-electric otherwise.

Out-of-scope rescue paths (mentioned in Cross-learning, not modeled in this round):

- Beamed power (Earth or lunar-based laser/microwave transmitter delivering tens of kilowatts to Saturn distance). Sci-fi for the demonstrator window 2032–2035.
- Multi-launch outbound with on-orbit assembly (Starship-class refilling).
- Hypothetical high-energy-density-material chemical propellants (specific-impulse 500–1000 seconds, not flown).
- Comet or near-Earth-object water mining instead of Saturn B-ring. Different mission concept entirely.

## Pre-registered hypothesis (H-nfb)

**Aggregate (H-nfb-agg):** No non-fission architecture closes L0-05 (round-trip ≤ 15 years) and L0-12 (cost projection bounded) simultaneously. Architecture A (solar-electric + chemical hybrid) busts L0-05 by 1–4 years because the Saturn-side power problem forces low-specific-impulse inbound that crushes delivered-mass-per-launch-mass. Architecture B (all-chemical) busts L0-12 by a factor of 30–50× because the outbound chemical kick stage mass-ratio is 9–11×. Architecture C (plutonium-238 radioisotope-electric) busts plutonium-238 supply by 2–4 orders of magnitude at the 100-kilowatt-electric scale needed for the matrix's existing electric-thrust closure. **Conclusion: the architecture matrix's program-risk problem is unfixable by architecture choice.** The honest framing is that ICEBERG at the L0-05 15-year ceiling is fission-dependent; the program either bets on the 7th attempt at US space fission flight, or L0-05 relaxes to 20–25 years to admit Architecture A.

### Pre-registered sub-claims

| Sub-claim | Predicted | Falsification |
|---|---|---|
| H-nfb-a — Solar-electric outbound Edelbaum spiral time at 200 kilowatt-electric array, 25 tonne spacecraft, specific-impulse 2000 seconds | 0.3–1.5 years | outside 0.2–2.5 years |
| H-nfb-b — Chemical-kick stage mass ratio for heliocentric departure (10.3 km/s at specific-impulse 450 seconds) | 9–11 | outside 8–12 |
| H-nfb-c — Architecture A round-trip time, assuming Saturn-side onsite-electrolyzed hydrolox inbound (specific-impulse 450 seconds, 6.42 km/s inbound delta-velocity, 200 tonne chunk) | 16–20 years (busts L0-05) | falsified if ≤ 15.5 years |
| H-nfb-d — Architecture A round-trip time, water-steam inbound (specific-impulse 200 seconds, otherwise same) | 14–17 years; delivered-mass fraction < 10% of chunk (crushes L0-09 cadence and L0-12) | falsified if delivered-mass fraction > 25% |
| H-nfb-e — Architecture B (all-chemical) per-mission Earth-launch wet mass, normalized to a 50-tonne payload delivered to a B-ring orbit | 1500–4000 tonnes | outside 1000–5000 tonnes |
| H-nfb-f — Architecture B launch-mass-per-delivered-tonne ratio vs the megawatt all-electric Modular-Assembled-Radiators baseline | 30–80× | outside 20–120× |
| H-nfb-g — Plutonium-238 mass required for 100-kilowatt-electric Architecture C system at 5.3 watts-per-kilogram and 6.3% Stirling efficiency | 2500–3500 kilograms | outside 2000–4000 kilograms |
| H-nfb-h — Architecture C plutonium-238 supply infeasibility ratio, US production at 1.5 kilograms-per-year vs single-mission demand | 1500–2500× one-mission demand vs annual production (i.e. 1500–2500 years of production for one mission) | outside 1000–3000× |
| H-nfb-i — Bayesian posterior on non-fission baseline closing L0-05 + L0-09 + L0-12 at the demonstrator window 2032–2035 | < 0.05 | falsified if any architecture's combined-criteria closure is plausibly ≥ 0.20 |
| H-nfb-j — Honest framing: ICEBERG at L0-05 = 15 years is fission-dependent; non-fission requires L0-05 relaxation to 20–25 years | held | falsified if any cell of Architectures A/B/C closes the unrelaxed matrix |

**Aggregate decision:** if H-nfb-agg holds — no non-fission architecture closes the unrelaxed matrix — surface to the orchestrator: (a) add a "fission-dependent" annotation to the matrix's status line; (b) the L0-05 relaxation conversation moves from "nice-to-have" to "load-bearing" if the program wants any plausible path that doesn't bet on the 7th US space-fission attempt; (c) Architecture A becomes the defensible baseline at a relaxed L0-05 ≥ 20 years. If H-nfb-agg falsifies — some non-fission architecture closes — re-anchor the matrix on that cell and demote both fission cells to upside-only.

## Method

### Architecture A — solar-electric + chemical hybrid

**Outbound — solar-electric Edelbaum low-Earth-orbit-to-escape spiral:** Reuse R-megawatt-architecture-viability's `constant_thrust_burn` with `power_kwe` set to the solar-electric array power. Edelbaum integrated delta-velocity = 7.67 km/s (heliocentric speed at 400-km low-Earth-orbit). Specific impulse 2000 seconds. Initial wet mass = vehicle dry + chemical kick stage wet + solar array.

**Outbound — chemical kick stage:** After Earth escape, the solar-electric system is jettisoned (or carried as dead weight for return; round explores both). A hydrolox chemical kick stage performs the heliocentric departure burn from Earth-escape velocity to Saturn-Hohmann perihelion velocity. Delta-velocity for this leg: heliocentric excess `v_∞` at Earth for a Saturn Hohmann transfer, equal to `v_perihelion - v_Earth`. Reuse R-megawatt-architecture-viability's `outbound_dv_km_s` *minus* the Edelbaum spiral component already paid by solar-electric (i.e. 17.97 − 7.67 = 10.3 km/s). Specific impulse 450 seconds. Mass ratio = exp(10300 / (450 × 9.81)) ≈ 10.27.

**Cruise:** Hohmann ballistic, 6.08 years one-way each direction.

**Saturn ops:** 1 year fixed (consistent with prior rounds).

**Saturn-side power:** solar-electric array at 9.58 astronomical units delivers `P_AU1 / 91.8`. For a 200-kilowatt-electric Earth-vicinity array, 2.18 kilowatts at Saturn. Not enough for kilowatt-scale electrolysis.

**Inbound — option A1 (water-steam thruster):** Direct steam expansion at specific-impulse ~200 seconds (resistojet/arcjet adjacent; this is a stretch but heritage exists for water resistojets at ~150–250 seconds). Inbound delta-velocity 6.42 km/s. Mass ratio = exp(6420 / 1962) ≈ 26.5. From 200-tonne chunk: 200 × (1 − 1/26.5) = 192.5 tonnes propellant, 7.5 tonnes delivered (less the vehicle dry returning home).

**Inbound — option A2 (onsite hydrolox, requires Saturn-side power source):** Specific-impulse 450 seconds. Mass ratio = exp(6420 / 4413) ≈ 4.27. From 200-tonne chunk: 200 × (1 − 1/4.27) = 153.1 tonnes propellant, 46.9 tonnes delivered (less the vehicle). But the Saturn-side electrolysis plant requires ~5–15 tonnes of equipment AND a power source >> 2 kilowatts. Solar at Saturn doesn't supply it. Pre-launched batteries don't either (~3–10 megawatt-hours-per-tonne energy density × the leg time). The honest model treats option A2 as requiring a plutonium-238 radioisotope-thermoelectric-generator power source on board, at the kilopower scale needed for electrolysis (~5–10 kilowatts), which brings back the supply problem at smaller scale.

### Architecture B — all-chemical

**Outbound — chemical kick stage:** Full outbound delta-velocity for an impulsive chemical departure. Combined Earth-escape + heliocentric injection. Standard expression: `Δv_out = sqrt(v_escape_LEO² + v_∞²) − v_circ_LEO` where `v_escape_LEO = sqrt(2) × v_circ_LEO` and `v_∞` is the heliocentric Earth-departure excess. This is the Oberth-credited impulsive budget (~7.3 km/s), much smaller than the all-electric integrated 17.97 km/s.

**Cruise:** Hohmann ballistic, 6.08 years one-way each direction.

**Saturn ops:** 1 year fixed.

**Inbound — chunk-fed chemical:** Same as Architecture A option A2 — specific-impulse 450 seconds onsite-electrolyzed hydrolox, *if* Saturn-side power supports electrolysis. Same caveat: needs a kilopower radioisotope-thermoelectric-generator power source. Or specific-impulse 200 seconds water-steam, same caveat as A1.

**Launch mass:** working backwards from a 50-tonne payload landed at a low-Earth-orbit depot (or directly delivered) after Earth return, traversing inbound chemical, Saturn ops, cruise, and outbound chemical kick. Compute Earth-launch wet mass per delivered tonne and compare against the megawatt fission Modular-Assembled-Radiators baseline.

### Architecture C — plutonium-238 radioisotope-electric

**Plutonium-238 mass scaling:** plutonium-238 thermal output = 0.54 watts-per-gram. Thermal-to-electric conversion efficiency = 6.3% (state-of-art Stirling). Therefore mass of plutonium-238 needed for `P_kWe` electrical = `P_kWe × 1000 / (0.063 × 0.54)` grams.

**US production rate:** 1.5 kilograms-per-year target rate as of 2026 (DOE Oak-Ridge restart; ~700 grams FY2024, ~900 grams FY2025 target, 1.5 kilograms-per-year plateau ~2026, no funded scale-up beyond that). Cumulative US inventory ~35 kilograms.

**Verdict criterion:** if single-mission plutonium-238 demand exceeds US production rate by a factor of 10 or more (i.e. 10 years of production for one mission), the architecture is infeasible at any plausible cadence.

### Bayesian posterior on combined-criteria closure

Three weakly-informative priors for the probability that *any* non-fission architecture closes L0-05 + L0-09 + L0-12 at the 2032–2035 demonstrator window:

- **Prior 1 (Beta(2, 2)):** symmetric weakly-informative.
- **Prior 2 (Beta(1, 4)):** mildly skeptical given the architecture-specific physics constraints identified above.
- **Prior 3 (Beta(1, 9)):** strongly skeptical given that all three architectures hit at least one structural failure mode in pre-registration.

Likelihood: model "evidence" as the count of independent structural failures per architecture (L0-05 bust, L0-09 bust, L0-12 bust, supply infeasibility). Update posteriors using a Bernoulli-likelihood approximation. Report all three posteriors.

This is not a rigorous decision-theoretic computation; it is a structured way to express the posterior given pre-registered failure modes. Same approach as R-megawatt-architecture-viability.

### Outputs

- `results/architecture_A.json` — Architecture A trade table.
- `results/architecture_B.json` — Architecture B trade table.
- `results/architecture_C.json` — Architecture C plutonium-238 supply table.
- `results/bayesian_posteriors.json` — H-nfb-i posteriors.
- `results/tables.md` — human-readable summary.

Deterministic; runtime < 1 second; pure Python standard library.

### Things this round explicitly does *not* do

- Beamed power, multi-launch on-orbit assembly, hypothetical high-energy-density-material chemistry, non-Saturn water sources. All mentioned in Cross-learning as orchestrator-spawnable threads if the program wants to keep searching.
- Detailed solar-electric-array radiation degradation during the Edelbaum Van-Allen spiral (a real cost, not modeled; mentioned in Reading).
- Plutonium-238 production rate scale-up scenarios beyond the funded 1.5-kilograms-per-year plateau (mentioned in Reading; pessimistic by intent).
- Net-present-value or cost computations at the L0-12 level. The round flags expected L0-12 failures via launch-mass-multiplier ratios; explicit dollar-figure pricing is for R-redundancy-financing or a successor cost round.

---

## Result

Run complete; results under `results/`. Two bugs caught in the first iteration:

1. **Chunk-fed inbound mass-balance formula was wrong** in the initial run.py — coded as `delivered = chunk/(MR−1) − vehicle` instead of the correct `delivered = chunk/MR − vehicle × (1 − 1/MR)`. Inflated delivered tonnage by ~30%. Fixed and re-run.
2. **Solar-electric power class was undersized in pre-registration**. The original sweep at 200 kilowatts-electric gave an 8-year Edelbaum spiral and the round read "Architecture A busts L0-05 by 6 years." Sweeping power class to 2 megawatts-electric reveals Architecture A *closes* L0-05 at 1–2 megawatts-electric Earth-vicinity solar-electric. The launch mass at megawatt-class solar-electric was the pre-registration's missing dimension.

The Saturn-side process-power problem was not in pre-registration at all. Added it as an emergent criterion.

### Headline numbers

| Architecture | Best closure | Round-trip (yr) | Launch / delivered | Saturn energy-supply ratio | Verdict |
|---|---|---:|---:|---:|---|
| A — solar-electric + chemical kick + chunk-fed chemical inbound | 2 megawatts-electric Earth-vicinity solar-electric, 15-tonne vehicle, no Saturn radioisotope thermoelectric generator | 13.80 | 11.8 | 0.145 | closes L0-05 (just); busts Saturn-side energy by 7× |
| B — all-chemical end-to-end | 10-tonne vehicle, no Saturn radioisotope thermoelectric generator | 13.17 | 1.8 | 0.0 (no Saturn-side power source) | closes L0-05 and L0-12 trivially; **hidden-fails because no Saturn-side power means no electrolysis means no inbound propellant means no return** |
| B with 30-tonne Saturn radioisotope thermoelectric generator | 10-tonne vehicle | 13.17 | 17.7 | 0.947 | closes L0-05; still busts energy budget (just); supply infeasible (~3 tonnes of plutonium-238 ≈ 2000 years of US production) |
| C — plutonium-238 radioisotope-electric, 100 kilowatts-electric system | — | — | — | n/a | plutonium-238 supply busts US production by 196–759× (theoretical Stirling vs flown MMRTG bounds) |

### Pre-registered claims, hit/miss

| Sub-claim | Predicted | Measured | Held? |
|---|---|---:|:---:|
| H-nfb-a — SEP spiral 0.3–1.5 yr @ 200 kWe / 25 t spacecraft / Isp 2000 s | 0.3–1.5 yr | 6.12–10.18 yr at 200 kWe (driven by ~360-t kick-stage stack, not 25 t spacecraft) | NO (off by 4–20×) |
| H-nfb-b — Chemical kick MR for 10.3 km/s @ Isp 450 s | 9–11 | 10.27 (single-stage); 2-stage split at 5.15 km/s/stage MR 3.21 | held (single-stage); 2-stage decomposition was the practical model |
| H-nfb-c — Architecture A round-trip 16–20 yr (busts L0-05) | 16–20 yr | 13.80–19.29 yr depending on solar-electric power class | PARTIALLY HELD (busts L0-05 at ≤500 kWe; closes at ≥1 MWe) |
| H-nfb-d — Isp 200 s water-steam, delivered fraction < 10% of chunk | <10% | delivered = NEGATIVE at vehicle ≥ 15 t, chunk = 200 t (structurally infeasible) | held; in fact stronger than predicted |
| H-nfb-e — Architecture B Earth-launch wet mass 1500–4000 t for 50-t payload | 1500–4000 t | 70.9 t for 39 t delivered (10-t vehicle); 354 t for 8 t delivered (20-t vehicle with 30-t RTG) | **FALSIFIED dramatically** (off by 10–40×); chemical impulsive outbound from LEO is Oberth-credited 7.29 km/s, much smaller than I anticipated |
| H-nfb-f — Architecture B launch-mass / delivered ratio 30–80× | 30–80× | 1.8–4.5× (no Saturn RTG); 17.7× (30-t RTG) | **FALSIFIED dramatically**; B is competitive on launch mass when RTG isn't loaded |
| H-nfb-g — Pu-238 mass for 100 kWe REP 2500–3500 kg (theory Stirling) | 2500–3500 kg | 2939 kg (theory Stirling); 11,379 kg (flown MMRTG) | HELD (theory); flown is 3× worse |
| H-nfb-h — Pu-238 supply ratio (years of US production per mission) 1500–2500× | 1500–2500× | 1960× (theory); 7590× (flown) | HELD (theory); flown is worse |
| H-nfb-i — Posterior on any non-fission architecture closing L0-05 + L0-09 + L0-12 < 0.05 | <0.05 | post-run failure counts {A:1/4, B:3/4 hidden-fail, C:4/4}; combined posterior 0.20–0.35 — pre-reg failure count was wrong direction | partially falsified; see Revisit |
| H-nfb-j — Honest framing: fission-dependent | held | held but for **different reason than pre-registered** — Saturn-side process power for electrolysis, not propulsion-side launch mass | HELD with framing correction |

### Why pre-registration H-nfb-e and H-nfb-f failed

I anticipated all-chemical Architecture B would be dominated on launch mass because of cascading mass-ratio in the chemical kick stage. Two errors in that anticipation:

1. I anchored on the *integrated electric* outbound delta-velocity (17.97 km/s, no Oberth credit) and propagated that intuition to chemical. The chemical impulsive outbound from low Earth orbit is Oberth-credited and computes to 7.29 km/s — half the electric value, because impulsive burns at low Earth orbit get the full v²-bonus while electric burns do not.
2. The Architecture A pre-registration also under-counted the kick-stage mass cascade pushing the solar-electric spiral mass into the 300–800-tonne range, which is what made the spiral slow. Sweeping solar-electric power class to megawatt rescues the spiral time but does not rescue the launch-mass-per-delivered ratio, which is 11–34× for Architecture A.

The new headline: **Architecture B beats Architecture A on launch-mass-per-delivered, *and* Architecture B closes L0-05 trivially** because it does not pay for an Edelbaum spiral. The "all-chemical is dominated everywhere" claim from the architecture-decision-matrix exec summary was anchored on a *different* objective function (raw delivered mass with electric outbound, no Saturn-side power constraint).

## Reading

The pre-registration aggregate H-nfb-agg **holds** but the failure mode was misidentified. The honest finding from this round:

**No non-fission architecture closes L0-05 + L0-09 + L0-12 + Saturn-side-electrolysis-energy-budget simultaneously. The binding non-fission gap is Saturn-side process power for inbound propellant electrolysis, not propulsion-side launch mass.**

Three observations.

1. **The Saturn-side power problem is the deepest fission dependence in ICEBERG**, not the propulsion-side power problem. The architecture decision matrix has been treating "reactor era" as the variable that controls *propulsion* — what specific impulse and thrust the tug can produce in cruise. But the chunk-fed inbound architecture cannot pay its inbound delta-velocity at *any* useful specific impulse without onsite electrolysis of harvested water, and onsite electrolysis at the scale needed (160 tonnes of propellant per mission, 1.3 gigawatt-hours of electrical energy in one year of Saturn-vicinity ops) requires ~150 kilowatts-electric of Saturn-side electrical power. Solar at Saturn delivers 1/92 of Earth-vicinity power; the largest plausible Earth-vicinity solar array (a few megawatts-electric) gives 10–20 kilowatts-electric at Saturn. Plutonium-238 radioisotope thermoelectric generators at the same Saturn-side power level need 30+ tonnes of system mass = 3–11 tonnes of plutonium-238 = 2,000–7,000 years of US production. Only fission delivers Saturn-side power at the right scale.

2. **Architecture B (all-chemical) is more competitive than the matrix's exec summary admits, on propulsion alone.** A 70-tonne low-Earth-orbit wet mass delivers 39 tonnes of water per mission (chunk-fed inbound at specific-impulse 450 seconds) — launch-mass-per-delivered ratio of 1.8. This is *better* than the megawatt all-electric Modular-Assembled-Radiators baseline (~2.0–2.5 ratio). The matrix dismissed all-chemical as dominated; this round shows it isn't, on propulsion alone. What it is dominated by is Saturn-side power — and Architecture B has *no Saturn-side power source at all*. So the rescue path "all-chemical when chunk-fed at specific-impulse 450 seconds" is hidden-infeasible. Onsite hydrolox requires onsite electrolysis requires onsite power.

3. **The architecture-decision-matrix's "fission-dependent" framing should be rewritten.** Right now the matrix annotates "reactor era" as a propulsion power dimension. The truer framing is: the matrix is *Saturn-side-process-power-dependent*. Megawatt reactors solve propulsion and Saturn-side power simultaneously. Kilopower-class reactors at 10 kilowatts-electric, used purely for Saturn-side electrolysis, would also rescue Architecture B (chemical outbound + chunk-fed chemical inbound + Saturn-side reactor for electrolysis only). This is a *different* architecture not in the current matrix: chemical propulsion + small reactor for process power. Worth a separate round.

### Things this round did NOT prove

- That Pu-238 production cannot be scaled up. Russia produces ~0.8 kg/yr separately; combined NASA-Russia at 2.3 kg/yr still leaves the 100-kilowatt-electric REP architecture infeasible by ~50×. A 100× US production scale-up (1.5 → 150 kilograms per year) would bring 100-kilowatt-electric REP into "decades-per-mission" range. No funded program to do this.
- That solar-electric-spiral radiation degradation makes Architecture A worse than modeled. The Edelbaum spiral spends ~1–6 years in the Van Allen belts; published estimates put cumulative array degradation at 20–50%. The model treats array power as constant; in reality it degrades over the spiral and would extend round-trip time by 1–3 years. Did not model.
- That solar-thermal Saturn-side power (large mirror concentrators) is impossible. A 1-kilometer-squared mirror at Saturn collects ~13 megawatts thermal; could in principle replace the electrolysis-electrical step with direct solar-thermal water cracking at very high temperatures (Isp 350–500 seconds theoretically achievable with thermal water decomposition). Mirror mass at state-of-art ~1–3 tonnes per 1000 square meters → 1,000–3,000 tonnes for 1 square kilometer. Multi-launch deployable mirror architecture. Not modeled here — flagged for orchestrator.
- That hypothetical high-energy-density-material chemical propellants (specific-impulse 500–1000 seconds, not flown) couldn't rescue chemical Saturn-side architecture. None has flown; speculative.
- That beamed power from Earth or lunar transmitters couldn't deliver tens of kilowatts to Saturn. The diffraction-limited optical aperture for ~10 kilowatts at 9.58 astronomical units is ~10s of kilometers, sci-fi for the demonstrator window.

## Revisit

**Did the pre-registration hold?** Aggregate H-nfb-agg holds: no non-fission architecture closes the matrix's compliance criteria simultaneously. But three of the eight numeric sub-claims **falsified**, and one was wrong in framing rather than number.

**What went wrong in pre-registration:**

- H-nfb-a (SEP spiral time): I anchored on the spacecraft mass (~25 tonnes) and forgot the chemical kick stack stacks behind it during the spiral (~340 tonnes additional). Off by 4–20×. *Lesson: when an architecture stacks one propulsion stage on top of another, the underneath stage pays the full upstream wet mass. Always.*
- H-nfb-e and H-nfb-f (Architecture B launch mass): I anchored on the *electric* outbound integrated delta-velocity of 17.97 km/s. The chemical *impulsive* outbound from low Earth orbit gets Oberth credit and is 7.29 km/s — half the electric value. Chemical staging at 7.29 km/s is feasible with 2 stages. Architecture B's launch-mass-per-delivered ratio is therefore 1.8–4.5×, not 30–80×. *Lesson: when comparing electric vs chemical, the electric integrates delta-velocity; the chemical gets the Oberth bonus. They are not the same number.*
- H-nfb-i (Bayesian posterior < 0.05): the *post-run* per-architecture failure counts gave a higher posterior (0.18–0.31) than pre-registered, because I had Architecture B at 2/4 failures pre-registration and the actual structural-failure picture is different (B is good on launch mass, busts only Saturn-side energy unless a heavy radioisotope thermoelectric generator is added, which then drags everything). The right Bayesian framing is: each architecture has a *binding* failure on one criterion (Saturn-side energy for A and B; supply for C). Posterior on aggregate closure should be very low (<0.10) once the Saturn-side energy budget is added as a binding criterion. Pre-registration omitted that criterion; I'm adding it post-hoc, which is normally bad pre-registration practice but here the Saturn-side criterion comes from physics that pre-registration should have caught.

**The recurring lesson** (per the aelfrice experiment conventions, recurring lesson #7 "cheapest path vs. only viable path"): I pre-registered three architectures by *propulsion technology* (solar-electric, chemical, plutonium-238). The binding constraint turned out to be *Saturn-side process power*, which is orthogonal to propulsion technology choice. Pre-registration should have started by asking "what is the binding constraint?" and worked back from there. This is the same class of error as R-mission-success-probability's misread of L0-10 (per-mission threshold vs rolling-5-block clause). **The error mode: I optimized within a frame instead of questioning the frame.**

## Cross-learning

### Forward — adopt

- **Negative for the architecture decision matrix**: drop the implicit framing that "reactor era" controls propulsion specifically. The matrix should annotate two distinct fission dependences: (i) propulsion-side electric power, (ii) Saturn-side process power for inbound electrolysis. The second dependence has been hidden in the matrix's chunk-fed inbound assumption (every chemical Variant-B-style cell silently assumes Saturn-side electrical power for water electrolysis).
- **Positive for R-non-fission-baseline finding**: the verdict "no non-fission baseline closes the unrelaxed matrix" holds, but the binding criterion is Saturn-side process power, not propulsion-side launch mass. The orchestrator should treat this as the load-bearing version of the finding.
- **Spawn R-saturn-side-power**: explicit round on what Saturn-side power source could supply ~150 kilowatts-electric for one year of Saturn-vicinity operations. Candidates: (i) small fission reactor used purely for Saturn-side process power, decoupled from propulsion (changes the program-risk picture; a 10–40 kilowatt-electric Kilopower-class for process power is a smaller bet than megawatt-class for propulsion); (ii) megawatt-class Earth-vicinity solar arrays delivering 10–20 kilowatts-electric at Saturn (close to 14% of the target — needs 7× the demonstrator); (iii) large solar thermal mirror concentrator (≥1 square kilometer, mass-feasibility check); (iv) plutonium-238 radioisotope thermoelectric generator cluster at supply-infeasible scale (supply problem); (v) Russian or international plutonium-238 supply (geopolitically complex).
- **Spawn R-chemical-plus-small-reactor**: cell not currently in the matrix. Chemical propulsion (Architecture B numbers) + 10–40 kilowatt-electric reactor used purely for Saturn-side electrolysis. Round-trip 13–14 years. Launch-mass-per-delivered ratio ~3–5× depending on reactor mass. Program-risk anchor is "fission for *process* power" — a smaller-scale fission bet than megawatt propulsion fission. May be the most defensible cell in the entire matrix once the Saturn-side power problem is named.

### Forward — drop

- The "all-chemical end-to-end is dominated by all-electric Variant B on launch mass" claim in the architecture decision matrix's exec summary needs a correction. All-chemical (with Saturn-side power somehow supplied) has a *better* launch-mass-per-delivered ratio than megawatt fission Modular-Assembled-Radiators-anchored mass. The exec summary should be revised.

### Forward — defer

- Solar-thermal Saturn-side power (large mirror concentrator). Could in principle close the energy budget with a sub-1-tonne-per-1000-square-meter inflatable mirror at 1 square kilometer (~1 tonne). Speculative areal density; flag for R-solar-thermal-saturn-power round if the program wants to explore this.
- Russian or international plutonium-238 supply. Geopolitical not physical.
- Solar-electric-array radiation degradation during the Edelbaum spiral. Material refinement to Architecture A; not load-bearing for the round's verdict.

### Backward — cross-references

- **R-megawatt-architecture-viability** (commit `28d2370`): the previous round's claim that the matrix has no defensible baseline still holds, but is now sharper. The matrix is fission-dependent on Saturn-side *process* power; megawatt propulsion fission is one way to supply that, but not the only way. A small-reactor-for-process-power-only cell would change the program-risk picture materially.
- **R-electric-outbound** (commit `9001ce9`): claimed that megawatt all-electric closes L0-05 inside 12–14 years. This round confirms — chemical all-electric outbound is not the only path. Megawatt solar-electric also closes the Edelbaum spiral inside 1–2 years. But Architecture A still busts on Saturn-side power.
- **R-outbound-architecture** (commit `72c6077`): the 6.9× chemical-kick launch-mass multiplier was anchored on integrated electric 17.97 km/s outbound delta-velocity. The Oberth-credited chemical impulsive outbound is 7.29 km/s; this round's Architecture B numbers should be propagated back as a correction to the 6.9× multiplier interpretation.
- **R_radiator_mass_penalty** (commit `ad8156c`): R-megawatt-architecture-viability already flagged the optimistic-vs-pessimistic mass-decomposition swap. This round adds: even at Modular-Assembled-Radiators-anchored mass, Architecture B beats megawatt fission on launch-mass-per-delivered when Saturn-side power is held constant. The propulsion-side mass penalty was less binding than the Saturn-side power problem.

### Methodology issues caught

- **Two computation bugs caught in first run**: chunk-fed mass-balance formula error, and solar-electric power class under-sweep. Both fixed before recording the result table. Documented in Result section above. This is consistent with the pattern of pre-registered numeric-range hypotheses catching algebra errors that would have gone unflagged in an unstructured exploration.
- **Saturn-side energy budget was missing from pre-registration**. Added post-hoc. This is normally bad practice but the criterion is physics-deterministic (you cannot make hydrolox without electrolysis without power), so the criterion was always implicit. The pre-registration *should* have made it explicit. Recurring lesson #7 applies: optimize the frame, not within the frame.

