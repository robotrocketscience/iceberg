# Tier 0.5 — Saturn B-ring chunk spin-rate prior

**Round:** R-chunk-capture-monte-carlo
**Date:** 2026-05-26
**Status:** complete. Blocks Tier 1; prior table below replaces the SCOPE placeholder.

## What we want to know

A defensible prior on the rotation rate (revolutions per minute, abbreviated rpm) of Saturn B-ring particles in the meter-to-decameter (~1 m to ~100 m) size class, for use in the ICEBERG capture-architecture Monte Carlo. The SCOPE placeholder was log-uniform over [0.01, 1.0] rpm anchored against asteroid-belt spin distributions; this is the wrong-population prior because B-ring chunks sit in a dense collisional and tidal environment that asteroids do not.

## What the literature reports

### 1. Cassini Composite Infrared Spectrometer thermal data — direct observational constraint

Spilker et al. 2006 [1] and Morishima et al. 2010, 2012 [2, 3] inverted Cassini CIRS thermal phase curves to constrain ring-particle rotation. Key reported numbers:

- Thermal inertia of B-ring particles: 13 J/m^2/K/s^(1/2) (similar for A: 16, C: 20, Cassini Division: 11) [3].
- The CIRS data require a **bimodal rotation distribution**: a population of small fast rotators (random spin axes, spin period roughly under 1 hour) and a population of large slow rotators with spin axes preferentially normal to the ring plane and **spin period greater than 3.6 hours, i.e. under 0.28 rpm** [1, 2].
- Morishima 2010 reports the fast-rotator fraction by cross-section as a free fit parameter varying with radius across A / B / C; B-ring fits favor slow-rotator dominance among the larger particles. The fast-rotator population is associated with cm-scale regolith grains, NOT with the meter-and-larger bodies ICEBERG targets [2].
- No direct rotation measurement exists for any specific named B-ring chunk in the 1-100 m class; the result is statistical, inferred via radiative-transfer model fits to integrated thermal phase behavior.

### 2. N-body and Boltzmann theory — collisional spin damping

Ohtsuki and Toyama 2005 [4] and Ohtsuki 2006 [5, 6] derived the equilibrium spin distribution from N-body simulation:

- For an extended size distribution, **spin period scales roughly linearly with particle size**: angular velocity proportional to inverse particle radius in the practical regime, with **the largest particles having spin period comparable to the local orbital period** [4].
- The pure equipartition prediction (angular velocity proportional to r^-2.5) is **violated**: smaller particles are colder rotationally and translationally than equipartition predicts because of inelastic collisional dissipation [Salo 1995, summarized in Schmidt et al. 2009, ref 7].
- The B-ring local Keplerian orbital period at r about 110,000 km is **about 11.0 hours = 0.00152 rpm**. "Spin period comparable to orbital period" therefore anchors the **decameter end at about 0.001-0.005 rpm**.
- Collisional spin-damping timescale at B-ring optical depth (tau about 1-2) is of order one collision time, i.e. about one orbital period (about 10 hours) [7]. Spin and translational velocity dispersion are tightly coupled and re-equilibrate fast; the prior should be interpreted as a steady-state, not a primordial, distribution.

### 3. Propeller moonlets

Tiscareno et al. 2006, 2010 [8, 9] inferred 40-120 m to 1-2 km moonlets at propeller centers. Propeller hosts are characterized by orbital libration, not by direct spin measurement. **No published rotation-state measurement exists for any propeller host.** They bracket the upper bound of ICEBERG's target only by size, not by direct spin data.

### 4. Saturn's small ring-moons — upper-bound bracket

Pan (~14 km), Daphnis (~7.6 km), Atlas (~30 km) are all **tidally locked / synchronous with Saturn** at their orbital periods of about 13.8-14.4 hours [10, 11]. Equivalent spin rate about 0.0012 rpm. These are 2-4 orders of magnitude larger than ICEBERG targets, but they confirm that for bodies large enough for Saturn tides to dominate, the system drives spin toward synchronous rotation rather than spinning bodies up. For decameter chunks, tidal locking timescales are far too long for the ring's age, so this is a limiting case, not the operating point.

### 5. Asteroid spin distributions — wrong-population reference only

Pravec and Harris 2008 [12], Polishook et al. 2013 [13]: main-belt 3-15 km bodies spin at 1-9.5 cycles per day (about 0.0007-0.0066 rpm), with slow-rotator excess from YORP. The YORP timescale is ~45 million years per cycle per day. Ring collisions reset spin every ~1 orbit (~10 hours), so the asteroid distribution is broader than what a collisional ring can sustain. **Asteroid priors should not be transplanted onto ring chunks.**

## Synthesis — defensible prior

**Recommended prior, B-ring chunk spin rate, size-conditioned:**

| Size class | Median angular velocity (rpm) | 90% credible interval (rpm) | Distribution shape |
|---|---|---|---|
| 1-10 m | 0.01 | 0.002 - 0.05 | log-normal, sigma_log = 0.4 |
| 10-100 m | 0.002 | 0.0005 - 0.01 | log-normal, sigma_log = 0.4 |
| Combined (size-marginal, ICEBERG default) | 0.005 | 0.0005 - 0.05 | log-normal |

Anchors:

- Decameter end (10-100 m) anchored at "spin period comparable to orbital period" per Ohtsuki 2005 → spin period about 5-50 hours → 0.0003-0.003 rpm [4]; consistent with tidally locked ring-moon bracket at 0.0012 rpm [10, 11].
- Meter end anchored to the CIRS slow-rotator constraint spin period at least 3.6 hours, i.e. angular velocity at most 0.28 rpm, with Ohtsuki's linear-inverse-radius practical scaling extrapolated from the decameter anchor → median about 0.01 rpm at 1 m [1, 4].
- Log-normal shape (rather than the placeholder log-uniform) because collisional equilibrium produces a peaked, not flat, distribution; sigma about 0.4 reflects the model-fit residuals in Morishima 2010 and the absence of direct per-chunk measurement.

**This lowers the central prior by 1-2 orders of magnitude versus the asteroid-anchored placeholder.**

## Confidence assessment

- **High confidence:** ring chunks in the 1-100 m class spin slower than asteroid populations and are bounded above by spin period at least 3.6 hours (angular velocity at most 0.28 rpm). Directly supported by CIRS thermal modeling [1, 2, 3].
- **Medium confidence:** spin period scales roughly linearly with size, with decameter chunks near orbital-period synchronous. Supported by Ohtsuki 2005 simulations [4], indirectly corroborated by tidally locked ring-moons [10, 11].
- **Low confidence:** the exact width (sigma) and shape of the distribution within each size bin. **No direct rotation-state observation has been published for any individual B-ring particle in the 1-100 m class.** All numbers are inferred via radiative-transfer modeling, theoretical equilibrium, or extrapolation from larger or smaller bodies.
- **Explicit disclosure:** the prior is a theoretical and inferred bound, not a measurement. The Monte Carlo should treat the upper tail (angular velocity over 0.1 rpm) as plausible but disfavored, not excluded.

## Implications for ICEBERG architecture selection

A median spin rate 10-100x lower than the placeholder prior **substantially relaxes despin requirements** for any capture concept:

- A 10 m chunk at 0.002 rpm has an equatorial surface tangential speed of about 1 mm/s — comparable to or below approach-velocity errors. **Harpoon-style capture concepts that previously had to budget for de-tumble propellant become more attractive.**
- The size-conditioned shape (smaller chunks spin faster) means ram-scoop and bulk-collection of meter-class chunks faces non-trivial spin (about 0.01 rpm median, tens of centimeters/s edge speed at the 10 m scale), while single-chunk decameter capture is almost a non-issue spin-wise. **This tilts the architecture trade toward fewer, larger captures.**
- The Monte Carlo should still carry the upper tail (angular velocity about 0.1 rpm at 1 m) as a sensitivity case, since CIRS data do not exclude a small population of recently-disturbed fast rotators.

**Headline for the comparison memo:** the everting-sleeve's compliance advantage over harpoon — its main advantage in the cooperative-satellite-capture application — matters less for ring chunks because the spin distribution is intrinsically narrow and slow. The harpoon's spin-matching cost, which the wondering pass flagged as a structural concern, is also smaller than initial framing suggested.

## References

1. Spilker, L. J., et al. (2006). *Cassini thermal observations of Saturn's main rings: Implications for particle rotation and vertical mixing*. Planetary and Space Science, 54, 1167-1176. https://www.sciencedirect.com/science/article/abs/pii/S0032063306001310
2. Morishima, R., Spilker, L., and Ohtsuki, K. (2010). *A multilayer model for thermal infrared emission of Saturn's rings II*. Icarus, 210, 330-345. https://ui.adsabs.harvard.edu/abs/2010Icar..210..330M/abstract
3. Morishima, R., Spilker, L., and Salo, H. (2012). *A multilayer model for thermal infrared emission of Saturn's rings III*. https://arxiv.org/pdf/1209.3797
4. Ohtsuki, K. (2005). *Rotation Rates of Particles in Saturn's Rings*. Astrophysical Journal Letters, 626, L61-L64. https://ui.adsabs.harvard.edu/abs/2005ApJ...626L..61O/abstract
5. Ohtsuki, K. (2006a). *Rotation rate and velocity dispersion of planetary ring particles with size distribution: I*. Icarus. https://www.sciencedirect.com/science/article/abs/pii/S0019103506001175
6. Ohtsuki, K. (2006b). *Rotation rate and velocity dispersion of planetary ring particles with size distribution: II*. Icarus. https://www.sciencedirect.com/science/article/abs/pii/S0019103506001199
7. Schmidt, J., Ohtsuki, K., Rappaport, N., Salo, H., Spahn, F. (2009). *Dynamics of Saturn's Dense Rings*. In: Saturn from Cassini-Huygens. Springer. http://cc.oulu.fi/~hsalo/Schmidt_etal_Chap14.pdf
8. Tiscareno, M. S., et al. (2006). *100-metre-diameter moonlets in Saturn's A ring from observations of "propeller" structures*. Nature, 440, 648.
9. Tiscareno, M. S., et al. (2010). *Physical Characteristics and Non-Keplerian Orbital Motion of "Propeller" Moons*. Astrophysical Journal Letters, 718, L92.
10. Buratti, B. J., et al. (2019). *Close Cassini flybys of Saturn's ring moons Pan, Daphnis, Atlas, Pandora, and Epimetheus*. Science. https://www.science.org/doi/10.1126/science.aat2349
11. Charnoz, S., Crida, A., et al. *Accretion of ornamental equatorial ridges on Pan, Atlas and Daphnis*. https://www.sciencedirect.com/science/article/abs/pii/S0019103520305820
12. Pravec, P., et al. (2008). *Spin rate distribution of small asteroids*. Icarus, 197, 497.
13. Polishook, D., et al. (2013). *Size matters: The rotation rates of small near-Earth asteroids*. Icarus.
