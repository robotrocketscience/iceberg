### Inbound delta-velocity per architecture variant (high-elliptical 1 Mkm Saturn departure, with Lunar Gravity Assist credit)

| Variant | Description | Saturn spiral | Helio retro | Earth helio | LEO spiral | LGA | Saturn-egress kick | **Electric DV total** | Ratio to matrix 6.42 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A_as_stated | as-stated (no recovery) | 6.159 | 5.44 | 10.30 | 7.669 | -2.0 | 0.00 (impulsive) | **27.57** | 4.29× |
| B_saturn_egress_kick | + chemical Saturn egress | n/a (kick) | 5.44 | 10.30 | 7.669 | -2.0 | 2.09 (impulsive) | **21.41** | 3.33× |
| C_earth_aerocapture | + Earth aerocapture | 6.159 | 5.44 | 10.30 | n/a (aero) | -2.0 | 0.00 (impulsive) | **19.90** | 3.10× |
| D_both | + both recoveries | n/a (kick) | 5.44 | 10.30 | n/a (aero) | -2.0 | 2.09 (impulsive) | **13.74** | 2.14× |

### Variant B closure under each corrected delta-velocity, MARVL-anchored mass, chunk 200 t, specific impulse 2000 s

#### A_as_stated (as-stated (no recovery), electric inbound DV = 27.57 km/s)

| Reactor (kWe) | Tug (t) | Egress prop (t, chem) | Inbound prop (t, elec) | Delivered (t) | Fraction | t_inbound (yr) | Round-trip (yr) | Strict 15? | Soft 16? | Expected (uniform, t) |
|---:|---:|---:|---:|---:|---:|---:|---:|:--:|:--:|---:|
| 500 | 65.0 | 0.0 | 200.0 | 0.0 | 0.000 | 3.75 | 16.92 | no | no | 0.0000 |
| ? | INFEASIBLE: electric inbound burn requires more propellant than chunk has |
| ? | INFEASIBLE: electric inbound burn requires more propellant than chunk has |

#### B_saturn_egress_kick (+ chemical Saturn egress, electric inbound DV = 21.41 km/s)

| Reactor (kWe) | Tug (t) | Egress prop (t, chem) | Inbound prop (t, elec) | Delivered (t) | Fraction | t_inbound (yr) | Round-trip (yr) | Strict 15? | Soft 16? | Expected (uniform, t) |
|---:|---:|---:|---:|---:|---:|---:|---:|:--:|:--:|---:|
| ? | INFEASIBLE: electric inbound burn requires more propellant than chunk has |
| ? | INFEASIBLE: electric inbound burn requires more propellant than chunk has |
| ? | INFEASIBLE: electric inbound burn requires more propellant than chunk has |

#### C_earth_aerocapture (+ Earth aerocapture, electric inbound DV = 19.90 km/s)

| Reactor (kWe) | Tug (t) | Egress prop (t, chem) | Inbound prop (t, elec) | Delivered (t) | Fraction | t_inbound (yr) | Round-trip (yr) | Strict 15? | Soft 16? | Expected (uniform, t) |
|---:|---:|---:|---:|---:|---:|---:|---:|:--:|:--:|---:|
| 500 | 63.4 | 0.0 | 167.9 | 32.1 | 0.161 | 3.15 | 16.32 | no | no | 0.0418 |
| 750 | 89.2 | 0.0 | 184.3 | 15.7 | 0.078 | 2.30 | 15.48 | no | **yes** | 0.0204 |
| ? | INFEASIBLE: electric inbound burn requires more propellant than chunk has |

#### D_both (+ both recoveries, electric inbound DV = 13.74 km/s)

| Reactor (kWe) | Tug (t) | Egress prop (t, chem) | Inbound prop (t, elec) | Delivered (t) | Fraction | t_inbound (yr) | Round-trip (yr) | Strict 15? | Soft 16? | Expected (uniform, t) |
|---:|---:|---:|---:|---:|---:|---:|---:|:--:|:--:|---:|
| 500 | 59.0 | 100.0 | 80.1 | 20.0 | 0.100 | 1.50 | 14.67 | **yes** | **yes** | 0.0259 |
| 750 | 84.4 | 109.4 | 88.1 | 2.5 | 0.012 | 1.10 | 14.27 | **yes** | **yes** | 0.0032 |
| ? | INFEASIBLE: electric inbound burn requires more propellant than chunk has |

### Departure-orbit sensitivity, variant A, 500 kWe

| Departure orbit | Saturn spiral DV (km/s) | Total electric inbound DV (km/s) | Round-trip (yr) | Delivered (t) | Closes soft 16? |
|---|---:|---:|---:|---:|:--:|
| B_ring | 16.76 | 38.17 | INFEASIBLE | INFEASIBLE | no |
| high_elliptical_1Mkm | 6.16 | 27.57 | 16.92 | 0.0 | no |
| Iapetus_distance | 3.26 | 24.67 | 16.72 | 10.7 | no |

### Hypothesis grading

| Sub-claim | Predicted | Measured | Held? |
|---|---|---|---|
| H-vbic-a_variant_A_inbound_dv | 24.0-30.0 km/s | 27.57 km/s | yes |
| H-vbic-b_variant_B_inbound_dv | 20.0-24.0 km/s | 21.41 km/s | yes |
| H-vbic-c_variant_C_inbound_dv | 18.0-22.0 km/s | 19.90 km/s | yes |
| H-vbic-d_variant_D_inbound_dv | 12.0-16.0 km/s | 13.74 km/s | yes |
| H-vbic-e_variant_A_500kWe_does_not_close | round-trip 16-18 yr (over soft ceiling), delivered 0-25 t, cell does NOT close | round-trip 16.92215308710872 yr, delivered 0.014750671062614629 t, closes soft False | yes |
| H-vbic-f_variant_D_500kWe_closes | closes inside soft margin with delivered 80-110 t, round-trip ~14.5 yr | round-trip 14.673558516400288 yr, delivered 19.956844610897747 t, closes soft True | **no** |