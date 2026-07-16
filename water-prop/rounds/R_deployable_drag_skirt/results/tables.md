### Bare ICEBERG reference

- Bare vehicle: 55 t over 12.5 m² -> beta = **4400 kg/m²**
- Bare-chunk peak heat flux at 90 km (R_nose ≈ 2.0 m): **3.84 MW/m²** (matches R-chunk-as-heat-shield mode A within rounding).

### Required deployed area, skirt mass, and resulting beta

Skirt sized so that (vehicle_bare + skirt_mass) / skirt_area = beta_target.

| Target beta (kg/m²) | Areal density (kg/m²) | Skirt area (m²) | Skirt diameter (m) | Skirt mass (t) | Vehicle total mass (t) | Actual beta (kg/m²) | Fits in 5 t tug? | Fits in 10 t growth? |
|---:|---:|---:|---:|---:|---:|---:|:--:|:--:|
| 500 (aerocapture_aggressive_500) | 5 | 111 | 11.9 | 0.56 | 55.56 | 500 | YES | YES |
| 500 (aerocapture_aggressive_500) | 10 | 112 | 12.0 | 1.12 | 56.12 | 500 | YES | YES |
| 500 (aerocapture_aggressive_500) | 15 | 113 | 12.0 | 1.70 | 56.70 | 500 | YES | YES |
| 200 (aerocapture_nominal_200) | 5 | 282 | 19.0 | 1.41 | 56.41 | 200 | YES | YES |
| 200 (aerocapture_nominal_200) | 10 | 289 | 19.2 | 2.89 | 57.89 | 200 | YES | YES |
| 200 (aerocapture_nominal_200) | 15 | 297 | 19.5 | 4.46 | 59.46 | 200 | YES | YES |
| 100 (aerocapture_loftid_class_100) | 5 | 579 | 27.2 | 2.89 | 57.89 | 100 | YES | YES |
| 100 (aerocapture_loftid_class_100) | 10 | 611 | 27.9 | 6.11 | 61.11 | 100 | NO | YES |
| 100 (aerocapture_loftid_class_100) | 15 | 647 | 28.7 | 9.71 | 64.71 | 100 | NO | YES |
| 100 (aerobraking_mars_class_100) | 5 | 579 | 27.2 | 2.89 | 57.89 | 100 | YES | YES |
| 100 (aerobraking_mars_class_100) | 10 | 611 | 27.9 | 6.11 | 61.11 | 100 | NO | YES |
| 100 (aerobraking_mars_class_100) | 15 | 647 | 28.7 | 9.71 | 64.71 | 100 | NO | YES |

### Peak heat flux on the deployed skirt (90 km, v_inf = 6 km/s)

Skirt is much blunter than the bare chunk (R_nose set by the deployed envelope, not the chunk geometry). Heat flux scales as 1/sqrt(R_nose), so bigger skirt -> lower flux.

| Target beta | Areal density | Skirt diameter (m) | Skirt R_nose (m) | Peak heat flux (kW/m²) | T_eq @ eps=0.8 (K) | Within LOFTID (350 kW/m²)? | Within HIAD-2 (500 kW/m²)? |
|---:|---:|---:|---:|---:|---:|:--:|:--:|
| 500 | 5 | 11.9 | 5.9 | 2227 | 2647 | NO | NO |
| 500 | 10 | 12.0 | 6.0 | 2221 | 2645 | NO | NO |
| 500 | 15 | 12.0 | 6.0 | 2215 | 2644 | NO | NO |
| 200 | 5 | 19.0 | 9.5 | 1764 | 2497 | NO | NO |
| 200 | 10 | 19.2 | 9.6 | 1753 | 2493 | NO | NO |
| 200 | 15 | 19.5 | 9.7 | 1741 | 2489 | NO | NO |
| 100 | 5 | 27.2 | 13.6 | 1474 | 2387 | NO | NO |
| 100 | 10 | 27.9 | 13.9 | 1454 | 2379 | NO | NO |
| 100 | 15 | 28.7 | 14.4 | 1433 | 2371 | NO | NO |
| 100 | 5 | 27.2 | 13.6 | 1474 | 2387 | NO | NO |
| 100 | 10 | 27.9 | 13.9 | 1454 | 2379 | NO | NO |
| 100 | 15 | 28.7 | 14.4 | 1433 | 2371 | NO | NO |

### Heritage anchors

| Mission | Year | Diameter (m) | Vehicle mass | beta (kg/m²) | Peak heat flux |
|---|---:|---:|---:|---:|---:|
| LOFTID (Low-Earth Orbit Flight Test of an Inflatable Decelerator) | 2022 | 6 | 1.2 t | ~42 | ~350 kW/m² measured |
| HIAD-2 (Hypersonic Inflatable Aerodynamic Decelerator) | ground test | 6 | n/a | n/a | ~500 kW/m² design |
| IRDT (Inflatable Reentry and Descent Technology) | 2000-2005 | 2.3 | ~110 kg | ~90 | ~200 kW/m² |
| Mars Global Surveyor (aerobraking, rigid solar panels as drag area) | 1996-1999 | n/a | 1,030 kg | ~100 | ~3 kW/m² |
