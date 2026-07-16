# R-variant-B-burn-consistency — hypothesis scoring

| ID | Predicted | Measured | Verdict |
|---|---|---|---|
| H-vbrc-a | Variant B inbound burn at impulsive 6.42 km/s: 1.0–1.5 yr | 1.33 yr | **HELD** |
| H-vbrc-b | Variant B delivered at impulsive 6.42 km/s: 120–135 t | 128.8 t | **HELD** |
| H-vbrc-c | Variant B m_prop at CT 24.7 km/s ≥ 180 t | 182.6 t | **HELD** |
| H-vbrc-d | Variant B delivered at CT 40.2 km/s < 0 t | -22.2 t | **HELD** |
| H-vbrc-e | Matrix's 7.5-yr inbound burn does NOT reproduce (within ±20%) in any regime | burns at dv {6.42, 24.7, 32, 40.2} = ['1.33', '3.42', '3.85', '4.17'] | **HELD** |
| H-vbrc-f | Matrix's 80-t delivered does NOT reproduce (within ±15%) in any regime | delivered at dv {6.42, 24.7, 32, 40.2} = ['128.8', '17.4', '-5.1', '-22.2'] | **HELD** |
| H-vbrc-g | Variant B round-trip at impulsive 6.42 km/s: 13.5–15.0 yr | 14.01 yr | **HELD** |
| H-vbrc-h | Variant B cumulative burn at impulsive: 1.0–1.5 yr | 1.33 yr | **HELD** |
| H-vbrc-i | Variant B / Arch E cumulative burn ratio ≤ 0.20 | 0.135 | **HELD** |
| H-vbrc-j | Variant B reactor-life margin vs 10-yr Kilopower target ≥ 8 yr | 8.67 yr margin | **HELD** |
| H-vbrc-k | Arch E_500 cumulative burn 8.5–14.2 yr (R12 stated 11.37 yr ± 25%) | 9.91 yr | **HELD** |
| H-vbrc-l | No self-consistent Variant B cell at any of CT inbound dv ∈ {24.7, 32, 40.2} | feasibilities = [True, False, False] | **FALSIFIED** |
| H-vbrc-m | Impulsive cell feasible AND all continuous-thrust cells infeasible | imp_feasible=True, CT feasibilities=[True, False, False] | **FALSIFIED** |
| H-vbrc-n | Required chunk for VB at CT 24.7 km/s + delivered ≥ 30 t is ≥ 250 t | required chunk = 244.5 t | **FALSIFIED** |
