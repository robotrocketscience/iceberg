#!/usr/bin/env python3
"""Pre-script: R-kick-staging-optimization bounds (R174 best corner as base)."""
import math

G0 = 9.80665
VE_MET = 800.0 * G0
VE_K = 480.0 * G0
HW = 20_000.0 + 58.8e3 * 1.2 + 2_500.0     # R174 best corner: ship+bank+array
DV_TSI = 7300.0
HARVEST_300KW_GJ = 684.0 * 300 / 83        # outbound lit window, 300 kW

def kick_prop(dv, n, eps):
    """N equal stages, structural fraction eps of each stage's wet mass."""
    m = HW
    total = 0.0
    for _ in range(n):
        r = math.exp(dv / n / VE_K)
        # stage wet w solves: (m + w) / (m + eps*w) = r
        w = m * (r - 1) / (1 - eps * r)
        if w <= 0:
            return float("inf")
        total += w
        m = m  # stage dropped
    return total

for n in (1, 2, 3):
    for eps in (0.06, 0.08, 0.12):
        print(f"N={n} eps={eps}: kick wet {kick_prop(DV_TSI, n, eps)/1000:.0f} t")

# hybrid: lit MET supplies dv_met, kick supplies the rest
e_jet = HARVEST_300KW_GJ * 1e9 * 0.6
prop_met_max = e_jet / (0.5 * VE_MET ** 2)
print(f"lit MET water available: {prop_met_max/1000:.1f} t")
best = None
for dv_k in range(3500, 7301, 100):
    dv_m = DV_TSI - dv_k
    m_after_kick = HW
    prop_met = m_after_kick * (math.exp(dv_m / VE_MET) - 1)
    if prop_met > prop_met_max:
        continue
    # kick pushes hardware + the MET water it must carry
    m = HW + prop_met
    r = math.exp(dv_k / VE_K)
    w = m * (r - 1) / (1 - 0.08 * r)
    launch = HW + prop_met + w
    if best is None or launch < best[3]:
        best = (dv_k, dv_m, prop_met, launch, w)
dv_k, dv_m, pm, launch, w = best
print(f"hybrid optimum: kick {dv_k} + MET {dv_m} m/s; MET water {pm/1000:.1f} t, "
      f"kick wet {w/1000:.0f} t, outbound launch {launch/1000:.0f} t")
single = HW + kick_prop(DV_TSI, 1, 0.08)
print(f"vs single-stage all-kick: {single/1000:.0f} t -> hybrid saves "
      f"{(1 - launch/single)*100:.0f}%")
ratio = ((launch + 0) / 1000 / 80.0) / 1.25   # end-to-end approx: outbound dominates
print(f"approx end-to-end ratio at 80 t chunk: {ratio:.1f}x (R174 was 4.8x)")
