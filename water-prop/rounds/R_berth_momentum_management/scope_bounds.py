#!/usr/bin/env python3
"""Pre-script: R-berth-momentum-management bounds.

CONTEXT / non-redundancy note (read first):
  `R_chunk_despin_budget` already priced water cold-gas RCS dumping captured
  angular momentum -- its stress tail dumps up to 15,000 N.m.s for <125 kg
  (or <15 kg on the 800 s MET). The vehicle spec already carries 12x water
  cold-gas RCS + 50 kg reserve + 4x10 kg reaction wheels
  (vehicle/SATURN-SHIP-SPEC.md:48,60,62). So "use ISRU water thrusters for
  momentum management, and is the propellant affordable" is SETTLED (yes,
  cheaply). This round does NOT re-price that.

  What is NEW (from the bag_dynamics_6dof sim + project-owner's insight):
    (1) the berth CAPTURE TRANSIENT injects ~5000 N.m.s that the 4 small RWs
        cannot buffer inside the berth window (sim: wheels saturate, tumble);
    (2) firing thrusters at the flexible-bag interface at every berth is a
        PLUME hazard on the critical path (sim caveat);
    (3) the boulder's enormous inertia asymmetry makes GRAVITY-GRADIENT torque
        a usable desaturation actuator at Saturn ring distance -- UNSTUDIED
        anywhere in the campaign (the only "gravity gradient" hits are
        aerobraking perturbations).

  The round tests the momentum-management ARCHITECTURE trade at berth across
  three legs:
    A. thruster dump   -- cheap propellant (despin-confirmed), PLUME at bag
    B. GG desaturation -- propellant- and plume-free, but needs a buffer to
                          hold one berth injection + a berth-cadence floor
    C. geometry control-- shrink r_off*v_c so L <= RW capacity: no dump at all

Physics:
  Injected berth momentum:      L = m_s * v_c * r_off            (sim anchor)
  GG torque (boulder-dominated): tau_gg = (3 mu / 2 R^3) * dI,   dI ~ m_bag r_off^2
  Ring orbit:                    T_orb = 2 pi sqrt(R^3 / mu)
  GG secular shed per orbit:     dL_orbit ~ eta_gg * tau_gg * T_orb
  RW-only (no-dump) corner:      v_c * r_off <= H_rw / m_s
  Buffer hardware mass (CMG):    m_cmg = (L / H_cmg_unit) * m_cmg_unit
  Thruster-dump propellant:      scale despin's 125 kg / 15000 N.m.s linearly

Grids here SPAN the run grids: r_off in {1,2,5,10} m, v_c in {0.005,0.01,0.05} m/s,
eta_gg in {0.15,0.3,0.5}, host/buffer in {4xRW ~150, ISS-CMG 4760} N.m.s.
"""
import math

# --- Saturn / ring anchors (R179, reproduced) ---
MU_S = 3.793e16          # m^3/s^2
R_RING = 1.07e8          # m (B-ring co-orbital)
G0 = 9.80665

# --- bag / berth anchors (bag_dynamics_6dof sim; R191) ---
BAG_T = 40_000.0         # kg full bag load
F_SLOSH = 0.5
M_SLOSH = BAG_T * F_SLOSH        # 20 t momentum-carrying half
R_OFF = 5.0              # m capture arm
V_CAP = 0.05             # m/s soft-capture closing rate
L_BERTH = M_SLOSH * V_CAP * R_OFF          # 5000 N.m.s (sim central)
L_BERTH_FULLBAG = BAG_T * V_CAP * R_OFF    # 10000 N.m.s (full-bag upper bound)

# --- attitude actuators ---
# current spec: 4 x 10 kg reaction wheels, pyramidal. 10 kg wheel ~ 50 N.m.s;
# usable cluster about worst axis ~ 100-150 N.m.s.
H_RW_CLUSTER = (100.0, 150.0)
# CMG buffer option (ISS Honeywell M2000): 4760 N.m.s at ~272 kg each.
H_CMG_UNIT = 4760.0
M_CMG_UNIT = 272.0
CMG_KG_PER_NMS = M_CMG_UNIT / H_CMG_UNIT   # 0.0571 kg per N.m.s

# --- water RCS (despin anchors) ---
ISP_COLDGAS = 70.0
ISP_MET = 800.0
DESPIN_KG_AT_15000 = 125.0   # despin H2: cold-gas bound at 15000 N.m.s
DESPIN_MET_KG_AT_15000 = 15.0

# --- GG efficiency band ---
ETA_GG = (0.15, 0.30, 0.50)

T_ORB = 2 * math.pi * math.sqrt(R_RING ** 3 / MU_S)
DI_BOULDER = BAG_T * R_OFF ** 2              # ~1.0e6 kg.m^2 asymmetry lever
TAU_GG = (3 * MU_S / (2 * R_RING ** 3)) * DI_BOULDER

print("=" * 72)
print("Anchors")
print("=" * 72)
print(f"  injected berth L (sim, 20 t half)   = {L_BERTH:.0f} N.m.s")
print(f"  injected berth L (full 40 t bag)    = {L_BERTH_FULLBAG:.0f} N.m.s")
print(f"  ring orbit period                   = {T_ORB:.0f} s ({T_ORB/3600:.1f} h)")
print(f"  boulder inertia asymmetry dI        = {DI_BOULDER:.2e} kg.m^2")

print()
print("=" * 72)
print("H1 [S] -- GG torque with the boulder is a USABLE desaturation actuator;")
print("          one berth injection clears in days, propellant- and plume-free")
print("=" * 72)
print(f"  tau_gg,max = (3 mu / 2 R^3) dI      = {TAU_GG:.3f} N.m")
for eta in ETA_GG:
    shed = eta * TAU_GG * T_ORB
    orbits = L_BERTH / shed
    print(f"  eta_gg={eta:.2f}: shed/orbit={shed:6.0f} N.m.s -> "
          f"clear 5000 in {orbits:4.1f} orbits = {orbits*T_ORB/86400:4.1f} days")
print(f"  SCOPE: tau_gg in [0.02,0.08] N.m; shed in [200,900] N.m.s/orbit;")
print(f"         clear-time in [2.5,10] days. Falsified if tau_gg < 0.005 N.m")
print(f"         (GG negligible) OR clear-time > 30 days (impractically slow).")

print()
print("=" * 72)
print("H2 [S] -- buffering one berth injection to ENABLE leg B costs CMG-class")
print("          hardware (~300-600 kg) >> thruster-dump propellant (~42 kg):")
print("          GG-desat buys plume-avoidance, NOT mass")
print("=" * 72)
for Lname, L in (("sim 20t", L_BERTH), ("full bag", L_BERTH_FULLBAG)):
    for hlo, hhi in (H_RW_CLUSTER,):
        deficit_lo, deficit_hi = L / hhi, L / hlo
    m_cmg_1 = L * CMG_KG_PER_NMS
    print(f"  {Lname:8} L={L:5.0f}: RW deficit x{deficit_lo:.0f}-{deficit_hi:.0f} "
          f"(cluster {hlo:.0f}-{hhi:.0f} N.m.s); CMG buffer ~{m_cmg_1:.0f} kg "
          f"(x2 redun ~{2*m_cmg_1:.0f} kg)")
p_dump_cg = DESPIN_KG_AT_15000 * L_BERTH / 15000.0
p_dump_met = DESPIN_MET_KG_AT_15000 * L_BERTH / 15000.0
print(f"  thruster dump 5000 N.m.s: {p_dump_cg:.0f} kg cold-gas / "
      f"{p_dump_met:.0f} kg MET (despin-scaled)")
print(f"  SCOPE: buffer hardware [285,600] kg; thruster propellant [3,45] kg.")
print(f"  -> GG-desat's cost is DRY MASS + a cadence floor, not propellant.")
print(f"     Falsified if buffer hardware < thruster propellant, or the 4-RW")
print(f"     cluster (<=200 N.m.s) already absorbs one berth injection.")

print()
print("=" * 72)
print("H3 [S] -- capture-geometry control (leg C) can eliminate the dump")
print("          entirely: v_c*r_off <= H_rw/m_s keeps L within RW capacity")
print("=" * 72)
for hlo, hhi in (H_RW_CLUSTER,):
    corner_lo, corner_hi = hlo / M_SLOSH, hhi / M_SLOSH
print(f"  RW-only corner: v_c*r_off <= H_rw/m_s = "
      f"{corner_lo:.4f}-{corner_hi:.4f} m^2/s")
for r_off in (1.0, 2.0, 5.0):
    vc_lo = corner_lo / r_off
    vc_hi = corner_hi / r_off
    tag = "  (< 1 mm/s: below controllable)" if vc_hi < 1e-3 else ""
    print(f"    r_off={r_off:4.1f} m -> v_c <= {vc_lo*1000:.2f}-{vc_hi*1000:.2f} "
          f"mm/s{tag}")
print(f"  sim cross-check: L=100 N.m.s held (4.5 deg), L=500 tumbled -> RW-only")
print(f"  threshold ~ cluster capacity, consistent.")
print(f"  SCOPE: RW-only corner v_c*r_off in [0.005,0.0075]; achievable at")
print(f"  r_off<=2 m with v_c a few mm/s. Falsified if required v_c at r_off>=1 m")
print(f"  is < 1 mm/s everywhere (geometry control alone cannot reach RW-only).")

print()
print("=" * 72)
print("H4 [W] -- synthesis: leg B's ONLY advantage is plume-avoidance; it costs")
print("          dry mass + a berth-cadence floor. Leg C dominates if achievable.")
print("=" * 72)
print(f"  leg A thruster: propellant ~{p_dump_cg:.0f} kg/berth (immaterial vs 100 t)")
print(f"                  cost = N plume firings at the flexible-bag interface")
print(f"  leg B GG-desat: 0 propellant, 0 plume; +~{L_BERTH*CMG_KG_PER_NMS:.0f}-"
      f"{2*L_BERTH*CMG_KG_PER_NMS:.0f} kg CMG; berth cadence floor ~ clear-time")
print(f"  leg C geometry: 0 propellant, 0 plume, 0 extra hardware; needs capture")
print(f"                  control to v_c*r_off <= {corner_hi:.4f} m^2/s")
print(f"  SCOPE: rank C < B < A on plume/mass IF leg-C capture control is")
print(f"  operationally reachable; else A vs B is plume-hazard vs +300-600 kg.")
print(f"  Falsified if thruster propellant > 1% wet mass (leg A self-defeating)")
print(f"  or GG clear-time < 1 day (cadence never binding -> leg B free win).")
