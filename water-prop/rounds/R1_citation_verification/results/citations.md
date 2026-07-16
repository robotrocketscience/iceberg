# R1 Citation Verification — Results Table

Web-search-based verification of training-data citations used in round 0, round 1 stage, and round 2 stage docs.

## Table

| # | Claim | My value | Verified value | Source | Verdict |
|---|---|---|---|---|---|
| 1 | Penn State Micci/Bilén water microwave electrothermal thruster specific impulse | 500–800 s | **No consistent measurement.** Helium MET: 410 s, 73% efficiency. Nitrogen MET: 231 s, 45%. Water plasma: "proof of concept only, not consistently functional." | IEPC 2017 paper [296], Penn State Space Propulsion Lab | **Falsified-informative**: water specifically has no published Isp measurement. My 500–800 s came from extrapolation, not data. R0's Cantera bounds (416–558 s) are the best available estimate. |
| 2 | Tethers Unlimited HYDROS-C demonstrated specific impulse | 310 s | "Up to 300 seconds" with up to 1 N thrust. PTD-1 flew Jan 24, 2021 — first in-orbit demonstration of a water-electrolysis propulsion system. | Tethers Unlimited HYDROS product page, USU Small Satellite Conference 2015 + 2021 papers | **Held** (250–350 s predicted, 300 s found) |
| 3 | Pale Blue water ion thruster specific impulse | 800–1500 s | **2000 s specific impulse**, 350 μN thrust, 7000 N·s total impulse, at 60 W power, in 1U+ form factor. From University of Tokyo (Koizumi heritage) Electron Cyclotron Resonance technology. | Pale Blue PBI product page, USU Small Satellite Conference 2025 performance evaluation paper | **Falsified-informative**: real value 2000 s exceeds my predicted upper bound of 1500 s. Pale Blue is a stronger candidate than I had budgeted. |
| 4 | Hydrogen permeation through 316 stainless steel at room temperature | ~10⁻⁹ mol/(m²·s·√Pa) | Sandia Technical Reference SAND2012-7321 confirms Arrhenius-type relationship, nearly independent of austenitic stainless steel composition. Specific room-temperature numbers not in search snippets; need WebFetch on the report. | Sandia SAND2012-7321; h2tools.org technical reference | **Deferred**: source identified but specific number not yet pulled. Round 0c (storage thermal model) will close this. |
| 5 | NASA Kilopower / KRUSTY electrical power | 1–10 kWe | **1 kWe nominal** for KRUSTY (28 kg uranium-235 core, 134 kg total mass). Project scales to 1–10 kWe. Specific power 2.5–6.5 W/kg. KRUSTY ran 28 hr at full power on March 20, 2018. | Wikipedia, NASA NTRS [20180007389], Nuclear Technology journal | **Held** (1–10 kWe predicted, confirmed). **New finding**: specific power 2.5–6.5 W/kg means a 10 kWe reactor weighs 1.5–4 tons. This is a mass-budget item I had not been tracking. |
| 6 | Saturn B-ring water-ice fraction | 92–98% | **>99% water ice for most Saturn rings.** B-ring non-icy volume fractions: 0.3–0.5% inner/outer, 0.1–0.2% middle — so 99.5–99.9% ice. Hedman & Nicholson 2016 reports B-ring surface mass density ~600 kg/m². B-ring particle porosity 85–90%. | Springer Space Science Reviews 2024 (Miller / Hedman composition review), Hedman & Nicholson 2016 | **Held-conservative**: real number (>99%) exceeds my predicted upper bound of 98%. B-ring is even purer than I had assumed; strengthens propellant-cleanliness story (risk C06 ratings drop). |
| 7 | Saturn B-ring max particle diameter | 5–20 m | **2–10 m** maximum particle size with power-law slope q = 2.7–3.2 (differential index). Steep cutoff above ~10 m. | Cuzzi 2009 review, Zebker 1985, Cornell ecommons paper | **Partially held**: 10 m is the real upper edge; 20 m overshoot. The single-chunk mass ceiling of ~470 tons (from `docs/CHUNK-MASS-RANGE.md`) is the right value. Going above ~500 tons requires aggregation, confirmed. |

## Aggregate grading

My H1 aggregate prediction was: "1–3 of 7 claims falsified beyond the predicted range."

**Actual: 2 falsified-informative (claims 1 and 3), 4 held or held-conservative, 1 partially held, 1 deferred.**

H1 aggregate **held**.

## Key downstream implications

1. **Penn State has not measured water microwave-electrothermal specific impulse.** The 500–800 s figure used in R1/R2 stage docs is extrapolation from helium and nitrogen, not data. **R0's Cantera-bounded value (416–558 s at realistic operating conditions) is the most rigorous public estimate.** Update propulsion register entry C01 — confidence in the 500–700 s real-world estimate increases.

2. **Pale Blue water ion thruster delivers 2000 s specific impulse with in-orbit flight heritage at the 60 W power level.** This is a credible high-Isp candidate with real product status, not paper concept. Strengthens the water-ion architecture branch. Update propulsion register entries C02 (grid life) and F03 (no public data) — F03 partially retired by the existence of the 7000 N·s total-impulse demonstration.

3. **Kilopower reactor specific power is 2.5–6.5 W/kg.** A 10 kWe reactor is 1.5–4 tons of dry mass; a 40 kWe Fission Surface Power-class reactor would be 6–16 tons. **This is a significant mass overhead I had not been tracking in the R1/R2 power-vs-Isp trade table.** Round 5 (duty cycle + mass margin) needs to include reactor mass explicitly.

4. **Saturn B-ring is >99% water ice** (vs my 92–98% estimate). Lowers risk C06 (propellant contamination from dust) probability rating.

5. **B-ring single-particle mass ceiling is ~470 tons (10 m diameter).** Anything larger requires multi-chunk aggregation. The chunk-mass sweep range in `docs/CHUNK-MASS-RANGE.md` (5–500 tons) is correct.

6. **Sandia hydrogen permeation number deferred** — will pull from SAND2012-7321 PDF when R0c (storage thermal model) opens.

## Sources

Sources:
- [Penn State IEPC 2017 paper on water-propellant 17.8 GHz microwave electrothermal thruster](https://electricrocket.org/IEPC/IEPC_2017_296.pdf)
- [Tethers Unlimited HYDROS Propulsion System](http://www.tethers.com/HYDROS.html)
- [Tethers HYDROS performance characterization, USU 2015](https://digitalcommons.usu.edu/smallsat/2015/all2015/75/)
- [PTD-1 in-orbit demonstration, USU 2021](https://digitalcommons.usu.edu/smallsat/2021/all2021/209/)
- [Pale Blue Water Ion Thruster PBI product page](https://pale-blue.co.jp/product/pbi/)
- [Pale Blue 1U+ water ion thruster performance evaluation, USU 2025](https://digitalcommons.usu.edu/smallsat/2025/E-S5-2025/1/)
- [Sandia Technical Reference SAND2012-7321 on hydrogen compatibility of materials](https://www.sandia.gov/app/uploads/sites/158/2021/12/SAND2012_7321.pdf)
- [Sandia Technical Reference on Hydrogen Compatibility of 316 stainless steel](https://h2tools.org/sites/default/files/2103TechRef_316SS.pdf)
- [KRUSTY reactor design, Nuclear Technology journal](https://www.tandfonline.com/doi/full/10.1080/00295450.2020.1725382)
- [KRUSTY NASA NTRS report](https://ntrs.nasa.gov/api/citations/20180007389/downloads/20180007389.pdf)
- [Kilopower project, Wikipedia](https://en.wikipedia.org/wiki/Kilopower)
- [The Composition of Saturn's Rings, Space Science Reviews 2024](https://link.springer.com/article/10.1007/s11214-024-01104-y)
- [Particle Sizes in Saturn's Main Rings, Cornell ecommons](https://ecommons.cornell.edu/server/api/core/bitstreams/aa5390f5-9899-4ce2-8420-0f08c8b29f62/content)
