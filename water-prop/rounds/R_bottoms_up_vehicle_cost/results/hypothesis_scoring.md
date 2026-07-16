# R-bottoms-up-vehicle-cost — hypothesis scoring

| ID | Predicted | Measured | Verdict |
|---|---|---|---|
| H-bvc-a | Variant B median first-unit $900M–$1600M | $4143M | **FALSIFIED** |
| H-bvc-b | Arch E_500 median first-unit $3500M–$5500M | $4589M | **HELD** |
| H-bvc-c | Arch E_200 median first-unit $1800M–$2800M | $2361M | **HELD** |
| H-bvc-d | Cost ratio E_500/VariantB 3.0×–5.0× | 1.11× | **FALSIFIED** |
| H-bvc-e | Reactor+PMAD+thruster share > 55% of Arch E_500 first-unit | 50.9% (first-unit basis) | **FALSIFIED** |
| H-bvc-f | Cost spread (95/5 percentile) ≥ 3.5× for at least one architecture | VariantB 2.86×, E_500 2.79× (max 2.86×) | **FALSIFIED** |
| H-bvc-g | Variant B recurring unit (LR15 unit-33) $400M–$700M | $1825M | **FALSIFIED** |
| H-bvc-h | Arch E_500 recurring unit (LR15 unit-33) $1500M–$2500M | $2022M | **HELD** |
| H-bvc-i | P(NPV+) Variant B sov 3% bottoms-up no-learning < 20% (R8 placeholder LR15 was 50.0%) | 3.8% | **HELD** |
| H-bvc-j | P(NPV+) Arch E_500 sov 3% bottoms-up no-learning < 5% | 1.1% | **HELD** |
| H-bvc-k | P(NPV+) Variant B sov 3% LR15 bottoms-up in (35%, 60%) | 8.6% (R8 placeholder was 50.0%) | **FALSIFIED** |
| H-bvc-l | Variant B strict-dominance over Arch E variants on P(NPV+) across all WACC×LR | 0 violation(s): [] | **HELD** |
| H-bvc-m | At corporate 8.7%, no architecture ≥ 20% P(NPV+) under any LR | max P(NPV+) across all arch/LR = 3.62% | **HELD** |
| H-bvc-n | E_500/E_200 cost ratio < mass ratio (1.89) | cost ratio = 1.94 | **FALSIFIED** |
