# R-corridor-financial-model — STUDY (pre-registration)

**Worker:** worktree-172651, 2026-07-26 latest+29d (owner: "do them all").
Discharges decision #16's last dependency: an operative financial model priced
over the surviving corridor surface (electrolysis-fed nuclear-thermal;
corrected launch requirements ×8.75–×11.4; multi-chunk N ≤ 3; delivered
31.7–87.8 t at 18.7–21.1 yr). Tier-1 deterministic; all cost priors declared.

## Hypotheses

| # | Hypothesis | Gate | Prediction |
|---|---|---|---|
| H-F1 | Corridor breakeven price ≥ 3× the top defensible bulk band ($5,025/kg) at SOVEREIGN discount (3%) even under the cheapest launch prior ($100/kg Starship-mature) | breakeven < $15k/kg falsifies | Holds — cost stack and 19–21-yr revenue delay dominate |
| H-F2 | No captive segment has depth ≥ one corridor delivery (≥ 30 t at ≥ $20k/kg): the demand doc's anchored base case is 40–60 t/yr TOTAL at bulk prices, DoD reserve has no funding authority | a funded ≥30 t captive segment falsifies | Holds |
| H-F3 | The 13%/yr clearing-price decay defeats fleet learning: mission k+1 revenue falls faster than any ≤ 50%-learning-curve cost decline over a ~20-yr cycle | crossover found falsifies | Holds |
| H-F4 | Sovereign-grant framing (L0-13) remains the only compliant capital structure for the corridor | any hurdle-clearing IRR falsifies | Holds — H-M6 already killed delivery-class hurdles |

## Model + declared priors

Breakeven price = Σ(cost_i × (1+r)^(t_delivery − t_i)) / delivered_kg (costs
compounded to the revenue date; single mission, marginal basis; program/NRE
reported separately). Priors: launch $/kg-to-LEO ∈ {3,000 (Falcon-Heavy class),
500 (Starship early), 100 (Starship mature)}; raw lift 875 t (32-t cell) /
1,140 t (88-t cell); vehicle+stage+ISRU marginal unit ∈ {$0.5B, $1.0B}; first
unit ∈ {$1.5B, $3.0B} (NRE excluded from marginal breakeven, reported as
program overhang with the $1.11B staged-tranche ceiling); ops $40M/yr over the
mission; r ∈ {8.7% corporate, 3% sovereign, 0%}; t_delivery 21.1 yr (32-t
cell) / 18.7 yr (88-t cell) from mission start (spend at t = 0–2 approximated
at t = 1). Price comparators: defensible era bands $5,025 / $2,225 / $505 per
kg; captive $10k–$25k/kg; anchored demand depth 40–60 t/yr (2040 base case).
Decay: 13%/yr from mission start applied to the realized price at delivery
(sensitivity: 0%/yr).
