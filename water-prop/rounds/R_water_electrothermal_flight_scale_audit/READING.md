# READING — R-water-electrothermal-flight-scale-audit (bet #2)

## Load-bearing reading

**Bet #2 fails as an architecture trap, not a physics wall.** Water electrothermal propulsion is flight-proven — but only in pulses, on distilled water, at low Isp (Vigoride-5 raised orbit with a water MET in 2023; AQUARIUS ran a 91 s water resistojet in deep space). ICEBERG needs continuous-months operation on Saturn-ring water at matrix-closing Isp, and the two requirements pull against each other:

- **Contamination-tolerant (MET):** ~500–700 s continuous-flight Isp → **0–0.5% matrix closure**. Tolerates Saturn-water silicates but cannot reach matrix-closing Isp. (The 800 s A1 anchor is a ground/clean/pulse figure above the campaign's own R0 continuous ceiling and yields only 4%.)
- **Isp-sufficient (RF-ion, 2000 s):** closes the matrix on Isp, but is contamination-SENSITIVE. Its continuous-months flight-readiness on Saturn water is a conjunction of (bag silicate rejection holds) × (cathode/grid life ≥ burn) × (no anomaly) = **0.48 (mid), 0.25–0.73** — un-flown.
- **Flight gap:** 144–1461× in cumulative operating time vs the closest flown precedent.

## Recommended amendments

**mission_graph framework:** carry continuous-flight water-MET Isp at R0's **500–650 s** (not the 800 s ground/pulse anchor). The closure cells' 2000 s assumes RF-ion; price its continuous-months-on-Saturn-water flight-readiness (~0.48 conjunction) rather than treating 2000 s as free.

**Matrix propulsion cell:** carry as **demonstrator-conditional on a continuous-months water-thruster run on chunk-purity water in deep space.** Note the architecture trap explicitly (MET tolerant-but-low-Isp; RF-ion high-Isp-but-contamination-sensitive).

**Locked beliefs `650938e3` (A1) + `5535179f` (bet #2 framing):** the 800 s anchor is ground/clean/pulse and is not what the closure cells run; the live bet is RF-ion-continuous-on-Saturn-water reliability. Surface for project-owner update (locked — do not silently rewrite).

## Highest-leverage next action

A **continuous-months water-RF-ion (or MET) run on chunk-purity water in deep space** — the single experiment that retires both the duration gap (144–1461×) and the bag-rejection-holds-for-months factor (largest driver of the 0.48 conjunction). This is bet #2's retirement; pair with the Earth-orbit catch-and-contain demonstrator (bet #1) for tranche-1. The reactor (bet #3) stays off the critical path per matrix decision #14.
