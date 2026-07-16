# R-non-fission-baseline — results tables

## Shared physics

- Hohmann cruise (one-way): 6.086 yr
- Edelbaum spiral integrated dv (low Earth orbit → escape): 7.669 km/s
- Heliocentric v_inf (Earth → Saturn Hohmann): 10.298 km/s
- Chemical impulsive outbound from LEO (Oberth-credited): 7.287 km/s
- Inbound delta-velocity (post-Lunar-Gravity-Assist residual): 6.42 km/s

## Architecture A — solar-electric + chemical kick + chunk-fed chemical inbound

| SEP (kWe) | vehicle dry (t) | Saturn RTG (t) | inbound Isp (s) | SEP burn (yr) | m_LEO wet (t) | delivered water (t) | round-trip (yr) | closes L0-05 | launch/delivered | Saturn energy ratio | closes energy |
|---:|---:|---:|---:|---:|---:|---:|---:|:---:|---:|---:|:---:|
| 200 | 15 | 0.0 | 450 | 6.12 | 403.0 | 35.22 | 19.29 | no | 11.4 | 0.0145 | no |
| 200 | 25 | 0.0 | 450 | 10.18 | 670.7 | 27.55 | 23.35 | no | 24.3 | 0.0138 | no |
| 200 | 15 | 5.0 | 450 | 8.15 | 536.8 | 31.38 | 21.32 | no | 17.1 | 0.186 | no |
| 200 | 25 | 5.0 | 450 | 12.21 | 804.5 | 23.72 | 25.38 | no | 33.9 | 0.178 | no |
| 500 | 15 | 0.0 | 450 | 2.46 | 405.2 | 35.22 | 15.63 | no | 11.5 | 0.0362 | no |
| 500 | 25 | 0.0 | 450 | 4.09 | 672.9 | 27.55 | 17.26 | no | 24.4 | 0.0346 | no |
| 500 | 15 | 5.0 | 450 | 3.27 | 539.0 | 31.38 | 16.44 | no | 17.2 | 0.208 | no |
| 500 | 25 | 5.0 | 450 | 4.90 | 806.7 | 23.72 | 18.07 | no | 34.0 | 0.199 | no |
| 1000 | 15 | 0.0 | 450 | 1.24 | 408.9 | 35.22 | 14.41 | yes | 11.6 | 0.0724 | no |
| 1000 | 25 | 0.0 | 450 | 2.05 | 676.6 | 27.55 | 15.23 | no | 24.6 | 0.0692 | no |
| 1000 | 15 | 5.0 | 450 | 1.65 | 542.7 | 31.38 | 14.82 | yes | 17.3 | 0.243 | no |
| 1000 | 25 | 5.0 | 450 | 2.46 | 810.4 | 23.72 | 15.63 | no | 34.2 | 0.232 | no |
| 2000 | 15 | 0.0 | 450 | 0.63 | 416.3 | 35.22 | 13.80 | yes | 11.8 | 0.145 | no |
| 2000 | 25 | 0.0 | 450 | 1.04 | 684.0 | 27.55 | 14.21 | yes | 24.8 | 0.138 | no |
| 2000 | 15 | 5.0 | 450 | 0.83 | 550.1 | 31.38 | 14.01 | yes | 17.5 | 0.314 | no |
| 2000 | 25 | 5.0 | 450 | 1.24 | 817.8 | 23.72 | 14.41 | yes | 34.5 | 0.3 | no |
| — | ? | ? | ? | — | infeasible | -6.85 | — | — | — | — | — |

## Architecture B — all-chemical end-to-end

| vehicle dry (t) | Saturn RTG (t) | inbound Isp (s) | m_LEO wet (t) | delivered water (t) | round-trip (yr) | launch/delivered | Saturn energy ratio | closes energy |
|---:|---:|---:|---:|---:|---:|---:|---:|:---:|
| ? | ? | ? | infeasible | -2.04 | — | — | — | — |
| ? | ? | ? | infeasible | -6.85 | — | — | — | — |
| ? | ? | ? | infeasible | -30.90 | — | — | — | — |
| ? | ? | ? | infeasible | -6.85 | — | — | — | — |
| ? | ? | ? | infeasible | -11.66 | — | — | — | — |
| ? | ? | ? | infeasible | -35.71 | — | — | — | — |
| ? | ? | ? | infeasible | -11.66 | — | — | — | — |
| ? | ? | ? | infeasible | -16.47 | — | — | — | — |
| ? | ? | ? | infeasible | -40.52 | — | — | — | — |
| 10 | 0.0 | 450 | 70.9 | 39.05 | 13.17 | 1.8 | 0 | no |
| 10 | 5.0 | 450 | 106.3 | 35.22 | 13.17 | 3.0 | 0.176 | no |
| 10 | 30.0 | 450 | 283.4 | 16.06 | 13.17 | 17.7 | 0.947 | no |
| 15 | 0.0 | 450 | 106.3 | 35.22 | 13.17 | 3.0 | 0 | no |
| 15 | 5.0 | 450 | 141.7 | 31.38 | 13.17 | 4.5 | 0.172 | no |
| 15 | 30.0 | 450 | 318.9 | 12.22 | 13.17 | 26.1 | 0.928 | no |
| 20 | 0.0 | 450 | 141.7 | 31.38 | 13.17 | 4.5 | 0 | no |
| 20 | 5.0 | 450 | 177.1 | 27.55 | 13.17 | 6.4 | 0.168 | no |
| 20 | 30.0 | 450 | 354.3 | 8.39 | 13.17 | 42.2 | 0.909 | no |

## Architecture C — plutonium-238 radioisotope-electric supply table

- US production rate: 1.5 kg/yr
- US inventory ~2020: 35.0 kg
- Pu-238 electrical specific power (theoretical Stirling 6.3%): 34.02 W/kg
- Pu-238 electrical specific power (flown MMRTG): 8.79 W/kg

| power (kWe) | Pu-238 mass theory (kg) | Pu-238 mass flown (kg) | years US production theory | years US production flown | × US inventory theory | feasible single-mission |
|---:|---:|---:|---:|---:|---:|:---:|
| 1 | 29.4 | 113.8 | 19.6 | 75.9 | 0.84 | yes |
| 10 | 293.9 | 1137.9 | 196.0 | 758.6 | 8.40 | no |
| 40 | 1175.8 | 4551.7 | 783.9 | 3034.5 | 33.59 | no |
| 100 | 2939.4 | 11379.3 | 1959.6 | 7586.2 | 83.98 | no |
| 1000 | 29394.5 | 113793.1 | 19596.3 | 75862.1 | 839.84 | no |

## Bayesian posteriors — probability that *some* non-fission architecture closes L0-05 + L0-09 + L0-12 + supply

(pre-registration failure counts: A=3/4, B=2/4, C=4/4)

| prior | α_post | β_post | posterior mean |
|---|---:|---:|---:|
| Beta(2,2) symmetric | 5.0 | 11.0 | 0.312 |
| Beta(1,4) mild skeptic | 4.0 | 13.0 | 0.235 |
| Beta(1,9) strong skeptic | 4.0 | 18.0 | 0.182 |
