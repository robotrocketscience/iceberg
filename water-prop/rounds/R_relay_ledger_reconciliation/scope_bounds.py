#!/usr/bin/env python3
"""Pre-script: R-relay-ledger-reconciliation bounds.

Two debts fall due together:

1. R178 flagged the chunk-water ledger for reconciliation (R173/R174
   never debited lit-leg EP propellant from delivered mass).
2. R186 revoked R179's "v_inf pumped free" departure — and the relay arc
   (R182-R185) had priced the mothership's Saturn departure on exactly
   that lever: the staging ellipse IS the Hohmann raise orbit, so R182
   carried the mothership at 4 t bus, no reactor, no departure
   propellant, "departs by the pump-up tour". That line is now 0.0 km/s
   of a real 1.7 (impulsive-equivalent) or 3.3 (spiral) km/s.

This pre-script prices the omitted mothership departure honestly under
both propulsion options, propagates it through the relay arc's ladder
(R184 fleet steady 0.365 -> R185 ops-honest 0.453 -> departure-honest),
recomputes the knife-edge d*, unifies the harvest ledger, and quantifies
the R173/R174 lit-leg footnote for the record.

Unified chunk-water ledger convention (registered):
  delivered = mass at Earth handoff; every gram of propellant debits
  harvest; every tank/stage/reactor launched debits launch mass; every
  hour of Saturn-side work debits residence.

Anchors inherited: staging ellipse peri 1.07e8 / apo Titan-crossing
(R182); exit ceiling from its contour = exit_vinf(3.34 km/s) (R186);
S4-from-ellipse impulsive repair (R186); MET 800 s eta 0.6; kick 5.84;
chunk 40 t x N=4; MONO_LPD 1.02 (unaffected: the monolithic already
paid the honest 9.0 chunk-fed spiral); R185 retention 0.908, ops lpd
0.453; waiver decay 10.4-yr delay (R183); reactor life L=10 fpy (R184);
kappa 100 paper / 417 flown; in-situ gas 480 s 2-stage eps 0.08 with
electrolysis at 20.2 MJ/kg (R171 bank convention) on the shuttle's
30 kWe between sorties.
"""
import math

import numpy as np

G0 = 9.80665
MU_S = 3.7931206e16
R_RING = 1.07e8
A_TITAN = 1.22187e9
MU_T = 8.97814e12
R_T_BODY = 2.5747e6
ALT = 1.0e6
VINF_DEP = 6210.0
VE_MET = 800.0 * G0
VE_GAS = 480.0 * G0
ETA_THR = 0.6
YEAR = 3.156e7
KICK = 5.84
CHUNK, N_CH = 40_000.0, 4
M_BUS = 4_000.0
MONO_LPD = 1.02
OPS_LPD = 0.453
DELAY = 10.4
L_FPY = 10.0
T_TRANSIT_YR = 8.0
E_ELEC = 20.2e6
P_SHUTTLE = 30.0
TRIMS_TOUR, TRIMS_ONE = 300.0, 50.0
EPS = 0.08


def vis(r, a):
    return math.sqrt(MU_S * (2.0 / r - 1.0 / a))


def turn(vinf_t, rp):
    return 2.0 * math.asin(1.0 / (1.0 + rp * vinf_t ** 2 / MU_T))


def exit_vinf(vinf_t, r_enc, rp):
    v_t = vis(r_enc, A_TITAN)
    vesc = math.sqrt(2.0 * MU_S / r_enc)
    ca = (vesc ** 2 - v_t ** 2 - vinf_t ** 2) / (2.0 * v_t * vinf_t)
    if ca > 1.0:
        return 0.0
    a_out = max(math.acos(max(ca, -1.0)) - turn(vinf_t, rp), 0.0)
    v2 = v_t ** 2 + vinf_t ** 2 + 2.0 * v_t * vinf_t * math.cos(a_out)
    return math.sqrt(max(v2 - vesc ** 2, 0.0))


# --- the omitted line, priced (H1) ---
a_ell = (R_RING + A_TITAN) / 2.0
v_peri_ell = vis(R_RING, a_ell)
rp = R_T_BODY + ALT
# impulsive: S4-from-ellipse — peri burn onto the R186 S4 hyperbola
best_imp = None
for i in range(400):
    v0 = VINF_DEP * i / 399.0
    v_peri = math.sqrt(v0 ** 2 + 2.0 * MU_S / R_RING)
    v_sc = math.sqrt(v0 ** 2 + 2.0 * MU_S / A_TITAN)
    v_th = R_RING * v_peri / A_TITAN
    v_r = math.sqrt(max(v_sc ** 2 - v_th ** 2, 0.0))
    vinf_t = math.hypot(v_th - vis(A_TITAN, A_TITAN), v_r)
    kick = 2.0 * vinf_t * math.sin(turn(vinf_t, rp) / 2.0)
    v1 = math.sqrt(max((v_sc + kick) ** 2 - 2.0 * MU_S / A_TITAN, 0.0))
    tot = (v_peri - v_peri_ell) + max(0.0, VINF_DEP - v1) + TRIMS_ONE
    if best_imp is None or tot < best_imp[0]:
        best_imp = (tot, v0)
dv_imp = best_imp[0]
# spiral: ride the pump from the ellipse contour, buy the residual linearly
vinf_ell = vis(A_TITAN, A_TITAN) - vis(A_TITAN, a_ell)
v_exit = exit_vinf(vinf_ell, A_TITAN, rp)
dv_spiral = (VINF_DEP - v_exit) + TRIMS_TOUR
print("== H1: the mothership departure line R182 carried at 0.0 ==")
print(f"staging-ellipse peri speed {v_peri_ell/1e3:.2f} km/s; contour "
      f"v_inf,T {vinf_ell/1e3:.2f} -> exit ceiling {v_exit/1e3:.2f}")
print(f"impulsive (S4-from-ellipse + {TRIMS_ONE:.0f} trims): "
      f"{dv_imp/1e3:.2f} km/s (peri burn at v0 {best_imp[1]/1e3:.2f})")
print(f"spiral (pump free + linear residual + {TRIMS_TOUR:.0f} trims): "
      f"{dv_spiral/1e3:.2f} km/s")

# --- honest options through the ladder (H2) ---
print("\n== H2: relay ladder repriced ==")
stack_dry = M_BUS + N_CH * CHUNK
options = {}
# option A: in-situ gas, 2-stage 480 s; tanks/stages launched dry
m = stack_dry
for _ in range(2):
    r = math.exp(dv_imp / 2.0 / VE_GAS)
    w = m * (r - 1.0) / (1.0 - EPS * r)
    m += w
gas = m - stack_dry
hw_gas = EPS * gas / (1.0 - EPS)          # stage dry mass, launched
t_elec_yr = gas * E_ELEC / (P_SHUTTLE * 1e3) / YEAR
options["gas"] = {"harvest_t": gas / 1000.0,
                  "launch_t": hw_gas * KICK / 1000.0,
                  "residence_yr": t_elec_yr}
# option B: mothership reactor + MET spiral spread over the transit
for kappa, tag in ((100.0, "paper"), (417.0, "flown")):
    m_react = 0.0
    for _ in range(6):
        m_f = stack_dry + m_react
        prop = m_f * (math.exp(dv_spiral / VE_MET) - 1.0)
        p_m = 0.5 * VE_MET ** 2 * prop / ETA_THR \
            / (T_TRANSIT_YR * YEAR) / 1e3
        m_react = kappa * p_m
    fpy_frac = min(p_m * T_TRANSIT_YR / (p_m * L_FPY), 1.0)
    options[f"met_{tag}"] = {"harvest_t": prop / 1000.0,
                             "launch_t": m_react * KICK / 1000.0 * fpy_frac,
                             "residence_yr": 0.52,
                             "p_kwe": p_m}
for name, o in options.items():
    dlpd = o["launch_t"] / (N_CH * CHUNK / 1000.0)
    lpd = OPS_LPD + dlpd
    adv = MONO_LPD / lpd
    d_star = math.exp(math.log(adv) / DELAY) - 1.0
    o.update({"dlpd": dlpd, "lpd": lpd, "d_star_pct": d_star * 100.0})
    print(f"  {name}: harvest +{o['harvest_t']:.0f} t, launch "
          f"+{o['launch_t']:.1f} t, residence +{o['residence_yr']:.2f} yr "
          f"-> lpd {lpd:.3f}, adv {adv:.2f}x, d* {d_star*100:.1f}%")
best_opt = min(options.values(), key=lambda o: o["lpd"])
print(f"  cheapest honest option: lpd {best_opt['lpd']:.3f}, "
      f"d* {best_opt['d_star_pct']:.1f}% vs hurdles 8/10%")

# --- harvest ledger unified (H3) ---
print("\n== H3: harvest per delivered tonne, unified ==")
VE = VE_MET
R_WELL = math.exp(6700.0 / VE) - 1.0
m_sh = 2500.0 + 100.0 * 30.0            # R182 winning shuttle, paper 30 kWe
sortie_w = (m_sh + CHUNK) * R_WELL + m_sh * R_WELL
harv_relay_shipped = (sortie_w + CHUNK) / CHUNK
harv_relay_honest = (sortie_w + CHUNK
                     + best_opt["harvest_t"] * 1000.0 / N_CH) / CHUNK
mono_dry = 4000.0 + 100.0 * 30.0
mono_prop = (mono_dry + CHUNK) * (math.exp(9000.0 / VE) - 1.0)
harv_mono = (mono_prop + CHUNK) / CHUNK
print(f"  monolithic {harv_mono:.2f}x | relay as shipped "
      f"{harv_relay_shipped:.2f}x | relay honest {harv_relay_honest:.2f}x")
print(f"  R182-H4's capture-exposure relief: "
      f"{(1-harv_relay_shipped/harv_mono)*100:.0f}% shipped -> "
      f"{(1-harv_relay_honest/harv_mono)*100:.0f}% honest")

# --- the R173/R174 lit-leg footnote (H4) ---
print("\n== H4: lit-leg footnote (falsified arc, for the record) ==")
SATURN_R = 9.54
A_ELL = (1 + SATURN_R) / 2
ECC = (SATURN_R - 1) / (SATURN_R + 1)
T_FULL = A_ELL ** 1.5 * YEAR
_E = np.linspace(0, math.pi, 4000)
_M = _E - ECC * np.sin(_E)
T_GRID = _M / (2 * math.pi) * T_FULL
R_GRID = A_ELL * (1 - ECC * np.cos(_E))
mask = R_GRID <= 4.0
e_lit = float(np.trapezoid(300e3 / R_GRID[mask] ** 2, T_GRID[mask]))
prop_lit = e_lit * ETA_THR / (0.5 * VE_MET ** 2)
chunk80 = 80_000.0
dv_lit = VE_MET * math.log((20_000.0 + chunk80 + prop_lit)
                           / (20_000.0 + chunk80))
print(f"  canonical 300 kW lit leg (r <= 4 AU, {T_GRID[mask][-1]/YEAR:.2f} "
      f"yr): energy {e_lit/1e12:.2f} TJ -> propellant {prop_lit/1e3:.0f} t "
      f"= {dv_lit/1e3:.2f} km/s of the desk arc's 4.2 budget")
print(f"  never debited from delivered: up to {prop_lit/chunk80*100:.0f}% "
      f"of the 80 t chunk at full utilization (footnote only; the arc's "
      f"headline is already falsified by R179)")
