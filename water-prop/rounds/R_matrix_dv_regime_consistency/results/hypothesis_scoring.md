# R-matrix-dv-regime-consistency — hypothesis scoring

| ID | Predicted | Measured | Verdict |
|---|---|---|---|
| H-mdvc-a | Arch E_500 RT at impulsive 14.5–16.0 yr | 15.55 yr | **HELD** |
| H-mdvc-b | Arch E RT_impulsive ≤ 18.6 yr (≥ 5 yr shorter than CT 23.6) | 15.55 yr vs CT 22.58 yr | **HELD** |
| H-mdvc-c | Arch E cumulative burn at impulsive ≤ 4 yr | 2.87 yr | **HELD** |
| H-mdvc-d | Arch E delivered at impulsive > 60 t | 149.0 t | **HELD** |
| H-mdvc-e | Variant B RT at CT 24.7 km/s in [15.5, 16.5] yr | 16.10 yr | **HELD** |
| H-mdvc-f | Variant B delivered at CT 24.7 km/s ≤ 25 t | 17.4 t | **HELD** |
| H-mdvc-g | Variant B / Arch E cumulative burn ratio at CT ≤ 0.45 | 0.346 | **HELD** |
| H-mdvc-h | At CT, both architectures L0-05-non-compliant | VB_RT=16.10, E_RT=22.58 | **HELD** |
| H-mdvc-i | At impulsive, only Variant B closes L0-05 | VB_compliant=True, E_compliant=False | **HELD** |
| H-mdvc-j | Arch E RT swing between impulsive and CT ≥ 5 yr | 7.04 yr swing | **HELD** |
| H-mdvc-k | No (arch, regime) cell satisfies L0-05 AND L0-09 ≥ 50 t at 500 kWe / 200-t | any_full_compliant=True | **FALSIFIED** |
| H-mdvc-l | Required chemical inbound prop > 200-t chunk at impulsive 6.42 km/s | 837.3 t | **HELD** |
