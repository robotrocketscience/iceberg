#!/usr/bin/env python3
"""Pre-script: R-departure-anchor-reconciliation bounds.

The desk arc (R173-R178) priced Saturn departure at 1.5 km/s inside a
4.2 km/s inbound budget — a conops-era line R8 flagged as under-itemized
in May. The campaign's own anchors say otherwise:
  - R_dv_anchor_audit: 7.7 km/s impulsive Oberth from B-ring parking;
  - mission_graph phase4 (state of record): CHEMICAL_TEI_DV_KM_S = 7.7,
    CHUNK_FED_DV_KM_S = 9.0 at 800 s — the reactor baseline PAID these;
  - R_HE_graze_feasibility: grazing capture dead (5-10 km/s relative);
    co-orbital B-ring capture binding -> the chunk-laden ship starts its
    departure deep in the well;
  - R_bring_fine_structure_rendezvous: residence-class 7.4 in / 7.4 out
    (owner-retired, axis 19).

This pre-script (1) regresses those anchors from vis-viva, (2) prices the
Titan-assisted departure (apo-raise to Titan-crossing, then a Cassini-
reverse pump-up tour supplies the 6.21 km/s hyperbolic excess for ~free
plus time), (3) reprices the R178 chain's best corner at the honest
anchors under every non-fission departure option, and (4) re-derives the
Saturn-side power class that chunk-fed departure demands — bet #3 from
pure departure physics.
"""
import math

G0 = 9.80665
MU_S = 3.793e16          # m^3/s^2
R_RING = 1.07e8          # mid-B-ring, m (audit)
R_PERI = 6.0e7           # cloud-top Oberth periapsis, m (audit)
R_TITAN = 1.2217e9       # Titan orbit radius, m
VINF_DEP = 6210.0        # m/s, Hohmann-return hyperbolic excess (audit)
VE_MET = 800.0 * G0
VE_GAS = 480.0 * G0
ETA_THR = 0.6
YEAR = 3.156e7


def vis(r, a):
    return math.sqrt(MU_S * (2.0 / r - 1.0 / a))


def a_of(rp, ra):
    return (rp + ra) / 2.0


# --- (1) anchor regressions ---
v_circ_ring = vis(R_RING, R_RING)
# audit parking orbit: peri 60e3 km, apo at ring
a_park = a_of(R_PERI, R_RING)
v_p_park = vis(R_PERI, a_park)
v_p_hyp = math.sqrt(VINF_DEP ** 2 + 2 * MU_S / R_PERI)
dv_oberth = v_p_hyp - v_p_park
# and the cost of getting from co-orbital circular INTO that parking orbit:
v_a_park = vis(R_RING, a_park)
dv_drop = v_circ_ring - v_a_park
dv_two_burn = dv_drop + dv_oberth
# single-burn direct escape from co-orbital circular (v1 pre-script missed
# this; the Oberth detour does not pay from a deep circular orbit)
dv_single = math.sqrt(VINF_DEP ** 2 + 2 * MU_S / R_RING) - v_circ_ring
# bi-elliptic via Titan radius
dv_be1 = vis(R_RING, a_of(R_RING, R_TITAN)) - v_circ_ring
dv_be2 = vis(R_TITAN, a_of(R_PERI, R_TITAN)) - vis(R_TITAN, a_of(R_RING, R_TITAN))
dv_be3 = math.sqrt(VINF_DEP ** 2 + 2 * MU_S / R_PERI) - vis(R_PERI, a_of(R_PERI, R_TITAN))
dv_bielliptic = dv_be1 + abs(dv_be2) + dv_be3
dv_direct_total = min(dv_single, dv_two_burn, dv_bielliptic)
print("== anchor regressions ==")
print(f"v_circ at B-ring: {v_circ_ring/1e3:.2f} km/s")
print(f"audit Oberth burn (from parking): {dv_oberth/1e3:.2f} km/s (audit text: 7.7)")
print(f"from co-orbital: single-burn {dv_single/1e3:.2f} | two-burn Oberth "
      f"{dv_two_burn/1e3:.2f} | bi-elliptic-via-Titan {dv_bielliptic/1e3:.2f} "
      f"-> min {dv_direct_total/1e3:.2f} km/s")
# residence-class regression (R_bring_fine_structure: ~7.4 one way at 100k km)
r100 = 1.0e8
v_p_park100 = vis(R_PERI, a_of(R_PERI, r100))
dv_res = (vis(r100, r100) - vis(r100, a_of(R_PERI, r100))) \
    + (math.sqrt(VINF_DEP ** 2 + 2 * MU_S / R_PERI) - v_p_park100)
print(f"residence-class one-way regression at 100k km: {dv_res/1e3:.2f} km/s "
      f"(round text: ~7.4)")

# --- (2) Titan-assisted departure from co-orbital B-ring ---
# option A: direct apo-raise ring -> Titan-crossing, tour pumps v_inf
dv_raise_direct = vis(R_RING, a_of(R_RING, R_TITAN)) - v_circ_ring
# option B: Oberth-staged raise: drop peri first, raise apo from depth
dv_b1 = v_circ_ring - vis(R_RING, a_park)                    # drop at ring
dv_b2 = vis(R_PERI, a_of(R_PERI, R_TITAN)) - v_p_park        # raise at depth
dv_raise_oberth = dv_b1 + dv_b2
best_raise = min(dv_raise_direct, dv_raise_oberth)
TRIMS = 300.0            # tour phasing/trim allowance (Cassini-class, m/s)
dv_titan_total = best_raise + TRIMS
print("\n== Titan-assisted departure ==")
print(f"apo-raise direct: {dv_raise_direct/1e3:.2f} km/s | via Oberth depth: "
      f"{dv_raise_oberth/1e3:.2f} km/s -> best {best_raise/1e3:.2f}")
print(f"Titan-assisted total (raise + {TRIMS:.0f} m/s trims, v_inf pumped free, "
      f"+1-2 yr tour): {dv_titan_total/1e3:.2f} km/s")
print(f"saving vs direct impulsive: "
      f"{(dv_direct_total-dv_titan_total)/1e3:.2f} km/s "
      f"({(1-dv_titan_total/dv_direct_total)*100:.0f}%)")

# capture-side symmetry: circularizing at the ring from a Titan-crossing
# ellipse (peri at ring) is the same 6.70 km/s in reverse; Titan flybys
# cannot remove it (co-orbital circular state at 1.8 R_S is Tisserand-
# unreachable from an outer-moon flyby sequence).
dv_capture_circ = vis(R_RING, a_of(R_RING, R_TITAN)) - v_circ_ring
rt = dv_capture_circ + dv_titan_total
print(f"capture-side circularization (flyby-irreducible): "
      f"{dv_capture_circ/1e3:.2f} km/s")
print(f"honest in-system round trip with maximal Titan assist: "
      f"{rt/1e3:.2f} km/s (retired axis-19 residence-class: 14.7)")

# --- (3) repricing the desk arc's best corner at honest anchors ---
# R178 best corner post-regen: launch 503 t, delivered 76.7, ratio 5.24 on
# the 1.5 km/s ledger. Departure payload at that corner (ship 20 + chunk 80
# + residual bank ~5 t incl tanks):
PAYLOAD_DEP = 105_000.0
KICK_MULT = 5.84         # 2-stage eps 0.08 launch multiplier (R176/R178)
BASELINE = 50.0 / 40.0
print("\n== honest repricing of the non-fission departure ==")
for name, dv in (("direct impulsive", dv_direct_total),
                 ("Titan-assisted", dv_titan_total)):
    # staged 2-stage gas burn at Saturn, eps 0.08
    m = PAYLOAD_DEP
    for _ in range(2):
        r = math.exp(dv / 2 / VE_GAS)
        w = m * (r - 1) / (1 - 0.08 * r)
        m += w
    gas_at_saturn = m - PAYLOAD_DEP
    extra_launch = gas_at_saturn * 1.2 * KICK_MULT / 1000.0
    launch = 503.0 + extra_launch - 0.0
    ratio = (launch / 76.7) / BASELINE
    print(f"{name} ({dv/1e3:.2f} km/s, staged gas): {gas_at_saturn/1e3:.0f} t "
          f"of gas AT Saturn -> +{extra_launch:.0f} t launch -> ratio "
          f"{ratio:.1f}x (was 3.28x translated)")
# chunk-fed MET at non-fission power (2.2 kWe at Saturn)
for name, dv in (("direct spiral 9.0", 9000.0),
                 ("Titan-assisted MET", dv_titan_total)):
    m_f = 100_000.0
    prop = m_f * (math.exp(dv / VE_MET) - 1)
    e_jet = 0.5 * VE_MET ** 2 * prop
    for p_kwe in (2.2, 110.0, 200.0):
        t_yr = e_jet / ETA_THR / (p_kwe * 1e3) / YEAR
        print(f"chunk-fed {name}: prop {prop/1e3:.0f} t, burn at "
              f"{p_kwe:g} kWe = {t_yr:.1f} yr")

# --- (4) reactor requirement from departure physics ---
print("\n== bet #3 re-derived ==")
for name, dv in (("direct 9.0 km/s", 9000.0),
                 ("Titan-assisted", dv_titan_total)):
    m_f = 100_000.0
    prop = m_f * (math.exp(dv / VE_MET) - 1)
    e_jet = 0.5 * VE_MET ** 2 * prop
    p_req = e_jet / ETA_THR / (2 * YEAR) / 1e3
    print(f"{name}: P for 2-yr chunk-fed burn on 100 t final mass: "
          f"{p_req:.0f} kWe")
