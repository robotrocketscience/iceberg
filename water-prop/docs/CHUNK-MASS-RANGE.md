# Chunk Mass Range — Bounding the Trade Study Sweep Variable

**Question:** What chunk-mass range should the trade study sweep over? The previous ICEBERG analysis used 50–200 tons (from reactor-power scaling). The actual upper bound is set by Saturnian ring particle physics; the lower bound by economic viability.

**Status:** Pre-protocol finding, sourced from training-data references. Citations verified in round 1.

---

## Why Saturn's B-ring specifically

Saturn has seven named rings (D, C, B, A, F, G, E). Their water-ice fractions, particle size distributions, and densities differ enough that the answer to "which ring should we mine?" has one credible answer.

| Ring | Water-ice fraction | Particle size distribution | Optical depth | Verdict |
|---|---|---|---|---|
| D-ring | Mostly micron-scale dust | Sub-meter | Very low (~10⁻⁵) | Useless for bulk collection |
| C-ring | ~80–90% ice, dust-contaminated | Most particles <2 m | ~0.05–0.15 | Too sparse, contamination problem |
| **B-ring** | **~92–98% water ice** | **1 cm to ~10 m, power-law** | **~1.0–2.5 (highest)** | **Densest, ice-richest, biggest chunks. The right target.** |
| A-ring | ~95% water ice | Most particles <5 m | ~0.5–0.7 | Viable fallback; fewer big chunks |
| F-ring | ~98% water ice | Small particles, narrow ring | High but narrow | Dynamically chaotic (shepherd moons), small particles |
| G-ring | Mostly dust | Faint | Very low | Negligible mass |
| E-ring | Micron-scale ice from Enceladus geysers | Sub-meter | Diffuse | Useless for bulk |

The B-ring wins on all three criteria that matter for a trawl architecture:
1. **Mass density per unit swept volume** — highest of any ring, by a factor of several over A-ring and orders of magnitude over the others.
2. **Particle size distribution favors usable masses** — the only ring with a meaningful mass fraction in the 1–10 m range. Other rings either have only micron-to-centimeter dust (D, E, G), small particles (F), or much lower density (C).
3. **Water-ice purity** — 92–98% in B-ring vs. 80–90% in C-ring. Purity matters for propellant contamination risk (register entry C06 in the propulsion risk doc).

**Open citation in round 1:**
- Cuzzi et al. "An Evolving View of Saturn's Dynamic Rings," *Science* 327, 1470 (2010)
- Tiscareno et al. multiple papers on particle-size distributions from Cassini stellar occultations
- Hedman & Nicholson on B-ring composition

---

## Chunk mass as a function of diameter

For a spherical water-ice particle at density 900 kg/m³ (corresponds to bulk ring particles, which are mostly water ice with some porosity):

```
mass = (4/3) × π × r³ × ρ
```

| Diameter (m) | Volume (m³) | Mass (tons) | Comment |
|---|---|---|---|
| 1 | 0.52 | 0.47 | Lower end of "big" particles |
| 2 | 4.2 | 3.8 | Typical large B-ring particle |
| 3 | 14.1 | 12.7 | |
| 4 | 33.5 | 30.2 | |
| 5 | 65.4 | 58.9 | Bottom of original 50-ton estimate |
| 6 | 113 | 102 | |
| 7 | 180 | 162 | |
| 8 | 268 | 241 | Top of original 200-ton estimate |
| 9 | 382 | 343 | |
| 10 | 524 | 471 | Upper edge of observed distribution |
| 12 | 905 | 814 | Beyond observed distribution — would require either an exceptionally rare oversized particle or aggregation |

**Original 50–200 ton range corresponds to ~5–8 m diameter chunks** — comfortably in the middle of the B-ring particle distribution, neither rare nor edge-case.

**The upper bound from particle physics is ~470 tons (10 m chunk).** Anything larger requires either an exceptionally rare oversized particle (which contradicts the power-law size distribution) or **aggregation of multiple chunks into one bag** — operationally harder but not physically impossible.

---

## What chunk mass should the trade study sweep over?

Recommend sweeping **5 to 500 tons** in the synthesis round, with sensitivity to:

- **Small chunks (5–50 tons)** — thruster, electrolyzer, and tankage mass overhead dominate the total dry mass. High specific impulse wins more aggressively because every kilogram of propellant saved matters relative to a small chunk. Question: is there a minimum-economic chunk size below which the program does not close?
- **Medium chunks (50–200 tons)** — the original ICEBERG analysis range. Tsiolkovsky losses scale with chunk mass; thruster mass becomes a smaller fraction.
- **Large chunks (200–500 tons)** — Tsiolkovsky losses become the dominant loss term. Specific impulse buys more delivered mass in absolute terms. Power becomes the binding constraint via the reactor class.
- **Aggregated chunks (>500 tons)** — beyond single-particle physics. Treat as a separate architecture branch (multiple-grapple, multi-chunk bag).

**The "optimal" propulsion technology may differ across this range.** A high-thrust mid-specific-impulse choice (microwave electrothermal) might win for small chunks where power is limited; a high-specific-impulse choice (ion or Hall) might win for large chunks where the propellant savings outweigh the thruster mass. This is what the synthesis round (R-synthesis) characterizes.

---

## Implications

- **Update the trade-study objective**: maximize delivered mass to low Earth orbit as a function of (chunk mass, propulsion technology, available power, mission timeline). Not a single number — a Pareto surface.
- **Update round R2 (trajectory)**: sweep chunk mass over 5 to 500 tons. Mission velocity changes do not scale linearly with chunk mass; the lunar gravity assist tour delivers the same velocity change regardless of cargo mass, so smaller chunks see proportionally more relief.
- **Update round R-synthesis (architecture ranking)**: deliver a chunk-mass-vs-propulsion-tech Pareto surface, not a scalar ranking.

---

## Open questions for round 1 (citation verification)

1. Confirm B-ring water-ice fraction at 92–98% (Cassini, Hedman or Nicholson — exact reference).
2. Confirm particle size distribution power-law slope (Cuzzi 2010 or Tiscareno).
3. Confirm maximum observed B-ring particle size — is "10 m" the observation, or an extrapolation?
4. Estimate density of representative B-ring particle (is 900 kg/m³ right, or do they have meaningful porosity?).
5. Check whether multi-chunk aggregation is operationally credible at all, or whether a single-bag architecture is one-chunk-only by construction.
