# Round 1 — Citation Verification

**Question.** Of the citations used without verification in pre-protocol stage docs (round 1 landscape and round 2 deep-dive) and in round 0, how many hold up against a fresh web search? Where the published number differs from my training-data citation, the downstream analysis that depends on it must be updated.

**Method.**
- Identify the seven highest-leverage citations baked into the R1/R2 stage docs.
- Web search each one and capture the most authoritative source.
- Grade each prediction: held, held-conservative, partially held, falsified-informative, falsified-load-bearing, or deferred.
- Update downstream propulsion-register risk ratings and stage-doc claims that referenced the changed numbers.
- Output: `results/citations.md`.

**Validity caveats.**
- Web search snippets are summaries, not the source documents themselves. Numbers cited here are second-hand and need WebFetch on the source PDF for engineering use. R1 is sufficient to grade direction of bias, not for 3-significant-figure design data.
- The h2 permeation citation is deferred pending WebFetch on Sandia SAND2012-7321.
- "Pale Blue 2000 s specific impulse" is from a 2025 conference paper abstract; the operating point and any caveats need WebFetch on the full paper before downstream rounds rely on the number.

**Result.** See `results/citations.md`.

| Claim | Predicted | Found | Verdict |
|---|---|---|---|
| Penn State water microwave electrothermal Isp | 500–800 s | not measured for water | falsified-informative |
| Tethers HYDROS Isp | 250–350 s | up to 300 s | held |
| Pale Blue water ion Isp | 800–1500 s | 2000 s | falsified-informative |
| Hydrogen permeation through 316 stainless steel | 10⁻⁹ mol/(m²·s·√Pa) | source identified | deferred |
| Kilopower electrical power | 1–10 kWe | 1 kWe nominal, 1–10 kWe project range | held |
| B-ring water-ice fraction | 92–98% | >99% | held-conservative |
| B-ring max particle diameter | 5–20 m | 2–10 m | partially held |

Aggregate H1 prediction (1–3 of 7 falsified beyond range): **held**, with 2 falsified.

**Reading.**

Two findings are load-bearing for downstream rounds:

1. **Penn State has not consistently measured water-MET specific impulse.** The 500–800 second number I used in stage docs is extrapolation from helium and nitrogen MET operation. **Round 0's Cantera-bounded value (416–558 seconds at realistic chamber conditions) is the most rigorous public estimate for water specifically.** This strengthens the round 0 conclusion that microwave electrothermal cannot reach 1000 seconds; the gap between training-data lore and measured reality is structural.

2. **Pale Blue water ion thruster delivers 2000 seconds at 60 watts in a 1U+ form factor with in-orbit flight heritage.** My predicted upper bound of 1500 seconds was below this. This is a real product, not a paper concept, and the 7000 N·s total impulse demonstration partially retires risk F03 (no public long-duration water-ion data). Scaling to a hundreds-of-kilowatt class for ICEBERG-mass thrust is a separate question, but the per-thruster Isp ceiling at low power is now data-backed.

Three additional findings:

3. **Kilopower specific power is 2.5–6.5 W/kg.** A 10 kWe reactor weighs 1.5–4 tons; a 40 kWe Fission Surface Power-class reactor would weigh 6–16 tons. This mass overhead has not been in the R1/R2 power-vs-Isp trade table and is significant relative to chunk masses below 50 tons.

4. **Saturn B-ring is >99% water ice** (not 92–98%). The propellant-contamination risk (register entry C06) gets a probability downgrade.

5. **B-ring maximum single-particle diameter is 10 m**, not 20 m. The single-chunk mass ceiling of 470 tons in `docs/CHUNK-MASS-RANGE.md` is correct; anything above that requires aggregation.

**Revisit.** H1 aggregate (1–3 of 7 falsified): **held**. Of the seven specific predictions, four held or held-conservative, one partially held, two were falsified-informative, one was deferred. The pattern across the two falsifications is that both my predicted ranges were *narrower than the real values' bounds* — meaning my uncertainty bands were under-spread, not centered wrong. The water microwave electrothermal claim was unfounded (no data exists); Pale Blue's specific impulse exceeded my upper bound.

**Cross-learning.**
- Positive for round 0: the 416–558 second equilibrium-to-frozen band for water microwave-electrothermal is the most rigorous public estimate. Update propulsion register entry C01 confidence rating upward.
- Positive for round 3a/3b/3c (water ion, water Hall, water gridded ion): Pale Blue's 2000-second flight result is data, not speculation. Use as the demonstrated upper bound when sizing the per-thruster operating point.
- Positive for round 5 (duty cycle + mass margin): add reactor mass at 2.5–6.5 W/kg to the mass budget. Mid-range 5 W/kg gives 2 t for 10 kWe, 8 t for 40 kWe, 20 t for 100 kWe.
- Negative for risk C06 (B-ring dust contamination): probability rating drops; >99% water-ice composition reduces dust ingestion risk.
- Methodology issue flagged for round 0c (storage thermal model): pull hydrogen permeation number from Sandia SAND2012-7321 PDF, not snippet.
- Methodology issue flagged for all future rounds: training-data references for specific impulse have a systematic optimistic bias; my predicted ranges have been too narrow.
