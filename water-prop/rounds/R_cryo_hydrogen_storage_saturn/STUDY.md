# R-cryo-hydrogen-storage-saturn — storage is reactor-dominated, not environment-dominated; three worker hypotheses falsified

**Status:** run + STUDY complete 2026-07-22. **H-G1 held; H-G2 split (power clause falsified, conclusion held); H-G3 and H-G4-as-registered falsified.** A rigorous outcome that corrects both Round F's under-specification and the worker's own pre-registration. Result JSON `results/cryo_h2.json`; figure `results/cryo_h2.png`.
**Predecessor under test:** `R-electrolysis-departure-stage` (`49f4bb1`) — the H₂/O₂ departure lever rests on storing 77 t LH₂ at 20 K over the Saturn dwell, treated there as a "first-order risk." This round models it.

## Hypothesis (pre-registered; see SCOPE.md)

Three heat sources compete: MLI radiation (predicted small at Saturn's 90 K), ortho-para self-heating (predicted >100 kW showstopper if uncatalyzed), reactor proximity (predicted a shadow shield brings it to ≤10 W). Expected: storage tractable, contingent on para-catalysis + reactor separation.

## Test

Deterministic. LH₂ tank geometry (77 t / 70.8 kg m⁻³ para → 12.8 m sphere, 511 m²); MLI radiation over warm-boundary × emittance grids; ortho-para self-heat (uncatalyzed full conversion vs catalyzed); reactor radiation over an effective-view-factor grid (geometry × shield attenuation) at 700 K radiators; strut conduction; total boiloff over the dwell; zero-boiloff cryocooler input (Carnot × 20 % real fraction, 20 K → 90 K); and the geometric view factor vs boom length for a 150 kWe reactor.

## Result

| Sub-claim | Pre-registered | Measured | Verdict |
|---|---|---|---|
| H-G1 MLI radiation | < 5 %/2yr at 90 K | **0.35 %/2yr** (near-Earth 20.8 %; **60× better**) | ✅ HELD |
| H-G2 ortho-para power | > 100 kW uncatalyzed | **1.3 kW** self-heat | ❌ power clause FALSIFIED (~80× off) |
| H-G2 conclusion | catalysis mandatory | full conversion = **118 %** boiloff → mandatory | ✅ conclusion HELD (via boiloff fraction) |
| H-G3 reactor, shielded | ≤ 10 W at VF 10⁻³ | **6962 W at VF 10⁻³** (640 %/yr) | ❌ FALSIFIED (~700× off) |
| H-G4 total, req. met | 10–40 W, cryo < 2 kW | 1-layer shield: **6969 W / 122 kW cryo** | ❌ as-registered FALSIFIED |
| H-G4 recovery | — | VF 10⁻⁶: 14 W / 2.5 %/2yr / **0.24 kW** cryo | ✅ recovers only with a JWST-class-or-better shield |

**Reactor-heat vs effective view factor (700 K radiators, 511 m² tank):** unshielded (VF 0.1) 696 kW; point-away (10⁻²) 70 kW; 1-layer shadow (10⁻³) 7.0 kW; JWST-class (10⁻⁵) 70 W; extreme (10⁻⁶) 7 W. Required for ≤ 10 W: **VF_eff ≈ 1.4×10⁻⁶.** Geometric VF alone at a 100 m boom is ~3.5×10⁻⁴ (2.4 kW) — so a multilayer shadow shield (attenuation ~10⁻²–10⁻³ on top of the geometry) is required to reach VF_eff ~10⁻⁶.

## Reading

**Cryo-H₂ storage at Saturn is reactor-dominated, not environment-dominated — the opposite of the framing I pre-registered — and it is tractable only with the LH₂ tank sitting deep in the reactor's radiation/thermal shadow (long boom + multilayer shadow shield) plus ortho-para catalysis. With those, boiloff is a few percent over 2 years and a sub-1.5 kW cryocooler zeros it. Round F's H₂/O₂ departure lever survives, but its cryo-H₂ cost is heavier and more specific than "first-order risk."**

1. **The cold Saturn environment is a genuine but minor advantage (H-G1 ✅).** MLI radiation from the ~90 K environment boils off only 0.35 % of the H₂ over 2 years — 60× less than a 250 K near-Earth boundary (T⁴ scaling). If the environment were the only source, storage would be trivial. It is not.

2. **The reactor is the dominant source, and it is hard to mitigate (H-G3, H-G4 falsified).** A 150–440 kWe reactor's ~700 K radiators, seen by a 511 m² tank, deliver kilowatts even through a single-layer shadow shield (7 kW at VF 10⁻³ → 640 %/yr — the tank would boil dry). I pre-registered that a shadow shield brings this to ≤ 10 W; that was wrong by ~700×, because I under-weighted the σ·A·T⁴ magnitude (5.67×10⁻⁸ × 511 × 700⁴ = 7 MW of one-sided blackbody flux, of which even 10⁻³ is 7 kW). Reaching benign (≤ 10 W) needs **VF_eff ~1.4×10⁻⁶** — a ~100 m boom (geometric VF ~3.5×10⁻⁴) *plus* a multilayer (JWST-class, ~5–10 layer) thermal shadow shield (~10⁻²–10⁻³ attenuation). This is a real, specific architecture requirement, not the modest separation Round F implied.

3. **The mitigation is architecturally natural, though.** A nuclear-electric vehicle already carries a **reactor radiation shadow shield** (gamma/neutron) to protect its electronics, avionics, and the bag; the whole payload — including the LH₂ tank — sits in that shadow at boom distance. Co-locating the cryo-tank there, behind a few added thermal-shadow layers, is how such vehicles are already laid out. So the requirement is "put the tank in the reactor's shadow with adequate thermal shielding," which is compatible with the vehicle architecture but is a hard placement/shielding constraint that must be designed in, not a free lunch.

4. **Ortho-para catalysis is mandatory but standard (H-G2 conclusion ✅).** My pre-registered power figure (>100 kW) was wrong — the self-heat is only ~1.3 kW — but the conclusion is unchanged and actually cleaner: full ortho→para conversion of 77 t releases 118 % of the latent-heat-equivalent, so an uncatalyzed inventory self-boils-off completely over the dwell regardless of the (modest) power. Catalytic para-conversion at liquefaction (industry standard for stored LH₂) reduces storage self-heating to ~0. A hard requirement on the electrolysis/liquefaction plant, not a showstopper.

5. **With the requirements met, the cryocooler adder is negligible.** At VF_eff 10⁻⁶ (extreme shield / deep shadow), total heat leak is ~14 W → 2.5 %/2yr boiloff, or a **0.24 kW** zero-boiloff cryocooler — negligible against the 150–440 kWe electrolysis. At VF_eff 10⁻⁵ (JWST-class), ~76 W → 14 %/2yr, or a **1.34 kW** cryocooler — still small. Only at a mere 1-layer shield (VF 10⁻³) does the cryocooler balloon to 122 kW, which would erode Round F's power savings — so the multilayer shadow shield is what keeps the lever intact.

## Revisit

**This round falsified three of my five pre-registered hypotheses (H-G2 power clause, H-G3, H-G4-as-registered), which is the scientific method working exactly as intended and the honest headline of this round.** I made specific quantitative predictions, tested them, and was wrong in two directions: I over-estimated ortho-para self-heating power by ~80× (used a garbled figure — the correct 1.3 kW is what the arithmetic gives) and under-estimated reactor radiative coupling by ~700× (I intuited a shadow shield as "≤10 W" without computing σ·A·T⁴, which is 7 MW one-sided — even parts-per-thousand of it is kilowatts). The *net* physical conclusion (storage tractable with catalysis + reactor thermal separation) survives, but the *dominant* mechanism flipped from the environment (my framing) to the reactor (reality), and the required reactor-tank isolation is far stronger than I stated. Consistent with methodology lesson 1 (pessimistic prediction default) failing in the *optimistic* direction on the reactor term — a reminder to compute σ·A·T⁴ rather than intuit radiative leaks. Per lesson 7, I should have computed the reactor term under the pessimistic anchor (hot radiator, large tank) first; I did not, and the pre-registration paid for it.

Honest limitations: (a) the shield-attenuation values (10⁻²–10⁻³ multilayer) are literature order-of-magnitude, not a designed shield stackup; (b) the reactor radiator temperature (700 K) is a Brayton-class assumption — a lower-temperature Stirling radiator (~500 K) cuts the flux ~2.4× (still kilowatts at VF 10⁻³); (c) strut conduction is a placeholder 5 W; (d) the O₂ tank (near its 90 K boiling point at Saturn) is noted but not modeled — a minor cooling problem; (e) tank micrometeoroid/ring-particle protection over the dwell is not modeled and is a separate risk for a 12.8 m tank in the ring environment.

**Deferred (retest spec):** a designed reactor-tank shadow-shield stackup + boom-length trade against the vehicle's existing radiation shield (does the gamma/neutron shield double as the thermal shield?); the Stirling-vs-Brayton radiator-temperature choice's effect on the shield requirement; a micrometeoroid/ring-particle tank-protection model over the dwell; the O₂ tank thermal balance at Saturn ambient.

## Cross-learning

- **Forward to axis 05:** the Round F H₂/O₂ departure lever survives, but its cryo-H₂ cost is now specified and heavier — it requires the LH₂ tank to sit in the reactor's radiation+thermal shadow (long boom + multilayer shadow shield, VF_eff ≲ 10⁻⁵–10⁻⁶) plus ortho-para catalysis at liquefaction. With those met, boiloff is ~2–14 %/2yr and a < 1.5 kW cryocooler zeros it (negligible vs electrolysis); without adequate shielding the cryocooler balloons to ~100 kW and erodes the lever. Integration records this as a **sharpened requirement on the departure-stage architecture**, not a kill.
- **Backward to R-electrolysis-departure-stage:** its "first-order cryo-H₂ risk" is now the "reactor-tank thermal-shadow requirement" — the dominant cryo issue is not boiloff to space (benign at Saturn) but boiloff *from the onboard reactor*. This is the honest correction to that round.
- **Methodology (reinforces lesson 7, and a candidate refinement):** radiative-leak intuitions are unreliable at the σ·A·T⁴ scale — a 511 m² surface at 700 K radiates 7 MW one-sided, so any view factor above ~10⁻⁶ is watts-to-kilowatts. Compute the blackbody magnitude before intuiting "a shield handles it." The pre-registration would have caught this had I computed the pessimistic (hot-radiator, large-tank) anchor first. Candidate protocol note: for any radiative-coupling hypothesis, pre-register the σ·A·T⁴ one-sided magnitude and the required view factor, not a guessed wattage.
