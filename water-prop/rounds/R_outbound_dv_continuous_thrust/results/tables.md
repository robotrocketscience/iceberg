### Hohmann baseline and spiral endpoints

- Earth heliocentric orbital speed: 29.785 km/s
- Saturn heliocentric orbital speed: 9.622 km/s
- Hohmann perihelion velocity at Earth's distance: 40.082 km/s
- Hohmann aphelion velocity at Saturn's distance: 4.183 km/s
- Velocity-at-infinity at Earth: 10.298 km/s
- Velocity-at-infinity at Saturn: 5.439 km/s
- Low-Earth-orbit Edelbaum spiral integrated Δv: 7.669 km/s
- Hohmann cruise (each way): 6.086 years

### Outbound continuous-thrust integrated Δv — no lunar gravity assist

Composition: LEO spiral (segment 5') + Earth-side heliocentric (4') + Saturn-side heliocentric (2') + Saturn-side capture spiral (1').

| Saturn arrival orbit | 5' LEO spiral | 4' Earth-helio | 2' Saturn-helio | 1' Saturn spiral | **Total Δv (km/s)** | Δ vs R-electric-outbound 17.97 km/s |
|---|---:|---:|---:|---:|---:|---:|
| b_ring_1.35e5_km | 7.67 | 10.30 | 5.44 | 16.76 | **40.17** | +22.20 |
| high_elliptical_1e6_km | 7.67 | 10.30 | 5.44 | 6.16 | **29.56** | +11.59 |
| iapetus_3.561e6_km | 7.67 | 10.30 | 5.44 | 3.26 | **26.67** | +8.70 |

### Outbound continuous-thrust integrated Δv — with 2 km/s lunar gravity assist credit

Lunar gravity assist credit subtracted from the Earth-side combined (5' + 4'). Same methodology as titan's inbound treatment.

| Saturn arrival orbit | Earth combined (post-LGA) | 2' Saturn-helio | 1' Saturn spiral | **Total Δv (km/s)** |
|---|---:|---:|---:|---:|
| b_ring_1.35e5_km | 15.97 | 5.44 | 16.76 | **38.17** |
| high_elliptical_1e6_km | 15.97 | 5.44 | 6.16 | **27.56** |
| iapetus_3.561e6_km | 15.97 | 5.44 | 3.26 | **24.67** |

### Round-trip composition — 1 MWe / decomposed-mid (m_tug = 31.5 t) / Isp 2000 s / chunk 200 t

Outbound: corrected continuous-thrust integrated Δv (this round); corrected dry-at-end burn formula (R-electric-outbound-rerun).
Inbound: titan's continuous-thrust integrated Δv; chunk-fed wet-at-start burn formula.

| Outbound arrival | Inbound regime | t_out (yr) | t_in (yr) | Round-trip (yr) | Delivered (t) | Closes 15 yr? |
|---|---|---:|---:|---:|---:|:--:|
| b_ring_1.35e5_km | titan_inbound_high_elliptical_24.7_km_s | 1.99 | 1.55 | 16.72 | 34.2 | no |
| b_ring_1.35e5_km | titan_inbound_b_ring_40.2_km_s | 1.99 | 1.89 | 17.06 | -1.7 | no |
| high_elliptical_1e6_km | titan_inbound_high_elliptical_24.7_km_s | 1.04 | 1.55 | 15.76 | 34.2 | no |
| high_elliptical_1e6_km | titan_inbound_b_ring_40.2_km_s | 1.04 | 1.89 | 16.10 | -1.7 | no |
| iapetus_3.561e6_km | titan_inbound_high_elliptical_24.7_km_s | 0.86 | 1.55 | 15.58 | 34.2 | no |
| iapetus_3.561e6_km | titan_inbound_b_ring_40.2_km_s | 0.86 | 1.89 | 15.92 | -1.7 | no |

### Best-case composite — high-elliptical both ends + LGA credit on both legs

- Outbound Δv (high-elliptical arrival, LGA credit): 27.56 km/s
- Inbound Δv (titan high-elliptical departure, LGA credit): 24.7 km/s
- t_outbound burn: 0.91 yr
- t_inbound burn: 1.55 yr
- Round-trip: **15.64 yr** (**MISSES** the 15-year L0-05 ceiling)
- Delivered: 34.2 t out of 200 t chunk (17.1% delivered fraction)

### Cross-check against R-electric-outbound-rerun

- Using R-electric-outbound's outbound Δv (17.97 km/s) with titan-inbound 24.7 km/s and corrected formulas: round-trip = 15.17 yr (matches R-electric-outbound-rerun's 15.17 yr headline within rounding).
- Using corrected outbound Δv to high-elliptical, no LGA (29.56 km/s) with the same inbound: round-trip = 15.76 yr.
- Δ round-trip from outbound DV correction alone: 0.60 yr.

### Hypothesis grading

| Sub-claim | Predicted | Actual | Held? |
|---|---|---|---|
| H-od-a — Outbound Δv high-elliptical, no LGA | [27.0, 32.0] km/s | 29.56 km/s | yes |
| H-od-b — Outbound Δv B-ring, no LGA | [37.0, 42.0] km/s | 40.17 km/s | yes |
| H-od-c — Corrected outbound ≥ 1.5× R-electric-outbound's 17.97 km/s | >= 1.5x R-electric-outbound outbound DV | 1.65× | yes |
| H-od-d — Round-trip at 1 MWe / decomposed-mid / outbound-high-ellip / titan-inbound-24.7 > 18 yr | > 18.0 yr | 15.76 yr | **no** |
| H-od-e — Best-case high-elliptical both ends + LGA both legs round-trip > 15 yr | best case round-trip > 15 yr (architecture falsified at L0-05) | 15.64 yr | yes |
