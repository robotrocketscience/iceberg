### Per-mode heat flux, bag survival, and chunk ablation

| Quantity | A (aerocapture, 90 km, 1 pass) | B (aerobraking, 180 km, multi-pass) | C (intermediate, 130 km) |
|---|---:|---:|---:|
| Periapsis altitude (km) | 90 | 180 | 130 |
| Atmospheric density (kg/m³) | 1.0e-04 | 5.0e-10 | — |
| Entry velocity (km/s) | 12.62 | 12.55 | — |
| Peak heat flux (kW/m²) | **4,434** | **9.72** | **138.98** |
| Number of passes | 1 | 4543782 | 22719 |
| Total campaign time (days) | < 0.1 | 22718910 | 113595 |
| Total campaign time (months) | < 0.01 | 757297.0 | 3786.5 |
| Chunk ablation total (kg) | **532** | **15899607.55** | **1136664.67** |
| Chunk ablation as % of 100 t chunk | 0.532% | 15899.60755% | — |
| Bag radiative equilibrium temperature, MLI emissivity 0.3 (K) | **4,018** | **869** | **1691** |
| Bag survives? (polyimide T_max 700 K) | **NO** | **NO** | **NO** |

### Time penalty as fraction of 14-year round trip

- Aerobraking adds 757297.0 months = **444292.75%** of mission time.
- Within mission uncertainty budget; not a load-bearing constraint.

### Altitude trade-off: heat flux vs per-pass delta-v

**Ballistic coefficient = 4,000 kg/m² (100 t vehicle, 25 m² area).** This is the binding constraint.

| Altitude (km) | ρ (kg/m³) | Heat flux (kW/m²) | dv per pass (m/s) | Passes to dissipate 6 km/s | T_eq @ ε=0.8 (K) | Bag survives? |
|---:|---:|---:|---:|---:|---:|:--:|
| 90 | 1.0e-04 | 4433.87 | 284.810 | 22 | 3144 | no |
| 100 | 1.0e-05 | 1399.01 | 28.486 | 211 | 2357 | no |
| 110 | 1.0e-06 | 441.43 | 2.408 | 2,492 | 1766 | no |
| 130 | 1.0e-07 | 138.98 | 0.241 | 24,910 | 1323 | no |
| 150 | 1.0e-08 | 43.76 | 0.059 | 101,656 | 991 | no |
| 180 | 5.0e-10 | 9.72 | 0.003 | 2,032,041 | 680 | yes |
| 200 | 1.5e-10 | 5.30 | 0.001 | 6,771,111 | 585 | yes |

No altitude exists where bag survives AND pass count is tractable for this vehicle's ballistic coefficient.


### Bag laminate material tolerances (reference)

| Material | Continuous T_max (K) | Notes |
|---|---:|---|
| Aluminised Mylar | 520 | Outer-MLI layer; melts at ~250 °C |
| Vectran fabric | 600 | High-tenacity liquid-crystal polymer |
| Polyimide film (Kapton) | 700 | Continuous; ~800 K short-term |

Multi-layer-insulation laminate is typically Mylar/Kapton/Vectran stack; outer layer dictates failure threshold. **For aerobraking, the bag is well inside Mylar's tolerance; for aerocapture, every layer fails immediately.**