#!/usr/bin/env python3
"""Pre-script: R-burst-duty-cycle bounds.

Owner direction: "i dont really care about continuous power, the win is
figuring out what duty cycle enables burst power from the generator."

The bank (H2/O2 + fuel cell / turbine) is an energy-shifting device; its
duty-cycle envelope is set by three closed forms:

  (1) sustainability: average burst draw <= P_recharge * eta_rt,
      eta_rt = eta_chg * eta_fc = 0.66 * 0.55 = 0.363
      -> cadence tau = P_b * t_b / (P_re * eta_rt);
  (2) plant-vs-inventory mass: per kWe of burst, fuel-cell plant is
      ~10 kg (100 W/kg) while cycled gas costs ~0.59 kg per kWe-h
      (incl. tankage) -> crossover t* = 17 h;
  (3) battery comparator: ~5 kg per kWe-h at 80 % depth-of-discharge
      -> battery/bank crossover at ~2.3 h.

Post-R179 context: recharge at Saturn is spare-watt class (0.8-2.2 kWe
fission-free) or reactor margin (10-30 kWe). At the demonstrator (1 AU)
the full array recharges. All numbers below feed the SCOPE bands.
"""
LHV = 13.3e6
ETA_FC = 0.55
ETA_CHG = 0.66
ETA_RT = ETA_FC * ETA_CHG
FC_KG_PER_KWE = 10.0          # 100 W/kg plant
TANK = 0.20
BATT_KG_PER_KWEH = 3.6e6 / (250 * 3600.0) / 0.80   # 250 Wh/kg, 80% DoD
GAS_KG_PER_KWEH = 3.6e6 / ETA_FC / LHV * (1 + TANK)
DAY = 86400.0

print(f"eta_rt = {ETA_RT:.3f}")
print(f"gas per kWe-h (incl tank): {GAS_KG_PER_KWEH:.3f} kg | battery: "
      f"{BATT_KG_PER_KWEH:.2f} kg/kWe-h")

print("\n== (1) sustainable cadence tau [days] for burst P_b x t_b ==")
for p_re in (0.8, 2.2, 10.0, 30.0, 100.0):
    row = {}
    for pb, td in ((50, 1), (100, 1), (100, 3), (15, 7)):
        tau = pb * td * DAY / (p_re * ETA_RT) / DAY
        row[f"{pb}kWe x {td}d"] = round(tau, 1)
    print(f"P_re {p_re:5.1f} kWe: {row}")
print("avg-power law: P_b * duty_fraction <= 0.363 * P_re")

print("\n== (2) plant-vs-inventory crossover ==")
t_star = FC_KG_PER_KWE / GAS_KG_PER_KWEH
print(f"t* = {t_star:.1f} h  (shorter bursts: plant-mass-limited; longer: inventory)")

print("\n== (3) battery/bank crossover ==")
# per kWe of burst power, duration t: battery 5t kg vs FC 10 + 0.59t kg
t_x = FC_KG_PER_KWE / (BATT_KG_PER_KWEH - GAS_KG_PER_KWEH)
print(f"crossover: {t_x:.2f} h  (sub-{t_x:.1f}-h bursts -> battery; longer -> bank)")

print("\n== R172 burst-class adjudication at Saturn ==")
for pb, td in ((50, 1), (100, 3)):
    for p_re in (0.8, 2.2):
        tau = pb * td * DAY / (p_re * ETA_RT) / DAY
        print(f"{pb} kWe x {td} d at {p_re} kWe recharge: every {tau:.0f} d")
p_weekly = 50 * 1 / 7 / ETA_RT
print(f"recharge needed for WEEKLY 50 kWe-d bursts: {p_weekly:.1f} kWe "
      f"(reactor-margin class; coheres with R179)")

print("\n== demonstrator gate (1 AU, 100 kW array) ==")
duty_100 = 0.363 * 100.0 / 100.0
print(f"100 kWe MET firing sustainable {duty_100*24:.1f} h/day "
      f"(bet #2 flight-scale continuous demo fits fission-free)")

print("\n== one-shot reserve per 10 t launched bank ==")
e = 10_000.0 * LHV * ETA_FC
print(f"{e/1e9:.0f} GJe = 100 kWe for {e/100e3/DAY:.1f} days, one-shot")
