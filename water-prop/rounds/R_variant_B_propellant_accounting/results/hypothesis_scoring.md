# R-variant-B-propellant-accounting — hypothesis scoring

| ID | Predicted | Measured | Verdict |
|---|---|---|---|
| H-vbpa-a | Saturn-egress dv 1.5–2.5 km/s | 2.00 km/s (input) | **HELD** |
| H-vbpa-b | Earth-LEO capture dv with LGA 3.0–4.0 km/s | 3.50 km/s (input) | **HELD** |
| H-vbpa-c | Variant B matrix params (200-t chunk, with LGA) delivered ≤ 15 t | 4.0 t | **HELD** |
| H-vbpa-d | Without lunar GA, Variant B at 200-t chunk delivered ≤ 0 t | -22.2 t | **HELD** |
| H-vbpa-e | Required chunk for 80-t delivered with LGA ≥ 450 t (≥2.25× L0-05) | 528.7 t | **HELD** |
| H-vbpa-f | Variant B requires Saturn-side electrolysis OR outbound-carried chem OR matrix params wrong | At 200-t chunk with LGA, water consumed = 196.0 t <= chunk 200 t | **FALSIFIED** |
| H-vbpa-g | Matrix has not added Saturn-side-electrolysis cascade factor to Variant B's posterior | matrix prose carries 10-t electrolyzer line but R6 cascade was for Arch E only; Variant B posterior unrecomputed | **HELD** |
| H-vbpa-h | Outbound-carried scenario: LEO launch multiplier ≥ 12× per delivered tonne | 50.3× at 300-t chunk, 80-t delivered | **HELD** |
| H-vbpa-i | Electrolysis energy available > required | available 5.92 TJ vs required 3.92 TJ; ratio 1.51 | **HELD** |
| H-vbpa-j | 200-t chunk is the binding constraint (not energy, not power, not time) | water consumed 196.0 t > chunk 200 t AND energy available 1.5× required | **FALSIFIED** |
