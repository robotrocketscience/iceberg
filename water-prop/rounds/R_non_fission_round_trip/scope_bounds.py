#!/usr/bin/env python3
"""Pre-script: derive SCOPE bounds for R-non-fission-round-trip.

Chains the full mission for the non-fission variant (solar-bank + lit legs)
and the reactor baseline, at the canonical 40 t chunk. Prints the numbers the
SCOPE registers. Simplifications are stated in the SCOPE.
"""
import math

G0 = 9.80665
VE_MET = 800.0 * G0
VE_CHEM = 450.0 * G0
SHIP_DRY = 20_000.0
CHUNK = 40_000.0
TANK = 0.20
ZBO_KG_PER_T = 1.5 * 50 / 9

# dark-side dv ledger (m/s), chronological
DV_CAPTURE = 1000.0        # Saturn arrival multi-pass (dark)
DV_RING_OPS = 500.0        # rendezvous + stationkeeping (dark)
DV_DEPART = 1500.0         # departure (dark, chunk aboard)
HOTEL_GAS = 2_600.0        # kg, per R171/172 mid-duty
LIT_INBOUND = 1575.0       # m/s, per R173 at 83 kW; scales ~linearly with array
DV_BUDGET_IN = 4200.0

def chain_bank():
    """Solve bank size so the chain closes; iterate on total bank mass."""
    bank = 40_000.0
    for _ in range(60):
        # walk backward from arrival: what gas is left when each burn happens
        # forward walk: outbound carries full bank; capture burns first
        m_cap = SHIP_DRY + bank * (1 + TANK)
        g_cap = m_cap * (1 - math.exp(-DV_CAPTURE / VE_CHEM))
        rem = bank - g_cap
        m_ops = SHIP_DRY + rem * (1 + TANK)
        g_ops = m_ops * (1 - math.exp(-DV_RING_OPS / VE_CHEM))
        rem -= g_ops + HOTEL_GAS
        m_dep = SHIP_DRY + CHUNK + rem * (1 + TANK)
        g_dep = m_dep * (1 - math.exp(-DV_DEPART / VE_CHEM))
        rem -= g_dep
        # residual gas gives mid-cruise dv; need residual dv = budget - depart - lit
        need_resid = DV_BUDGET_IN - DV_DEPART - LIT_INBOUND   # 1125 m/s
        m_mid = SHIP_DRY + CHUNK + max(rem, 0) * (1 + TANK)
        g_resid = m_mid * (1 - math.exp(-need_resid / VE_CHEM))
        shortfall = g_resid - max(rem, 0)
        bank += shortfall * 0.8
        if abs(shortfall) < 10:
            break
    return bank, g_cap, g_ops, g_dep, g_resid

bank, g_cap, g_ops, g_dep, g_resid = chain_bank()
penalty = bank * (1 + TANK) + bank / 1000 * ZBO_KG_PER_T
print(f"full-chain bank: {bank/1000:.1f} t  (capture {g_cap/1000:.1f}, ops {g_ops/1000:.1f}, "
      f"hotel {HOTEL_GAS/1000:.1f}, depart {g_dep/1000:.1f}, resid {g_resid/1000:.1f})")
print(f"bank-side penalty (tanks+ZBO): {penalty/1000:.1f} t")

# outbound mode (a): chemical TSI kick, 7.3 km/s, 450 s, staged (kick jettisoned)
stack_tsi = SHIP_DRY + bank * (1 + TANK) + 1_500  # + array ~1.25 t at 150 kW
kick_prop = stack_tsi * (math.exp(7300.0 / VE_CHEM) - 1)
print(f"mode (a) chemical kick: stack through TSI {stack_tsi/1000:.1f} t -> "
      f"kick propellant {kick_prop/1000:.0f} t (plus stage dry)")

# mode (b): lit solar-electric spiral on launched water at 800 s, thrust only
# while flux supports it (approximate lit-spiral dv 7.7 km/s Earth escape +
# heliocentric to ~3 AU ~ 8 km/s of the Edelbaum 20; then ballistic to Saturn
# is NOT free — treat as kick of 4.2 km/s residual at 3 AU by gas)
DV_LIT_SPIRAL = 7700.0 + 8000.0
m1 = stack_tsi
prop_spiral = m1 * (math.exp(DV_LIT_SPIRAL / VE_MET) - 1)
g_escape = (m1 + 0) * (1 - math.exp(-4200.0 / VE_CHEM))
print(f"mode (b) lit spiral: water propellant {prop_spiral/1000:.0f} t + "
      f"3-AU gas kick {g_escape/1000:.1f} t (adds to bank)")

# reactor baseline launch-per-delivered (audit-consistent): ~50 t / 40 t
for mode, extra in (("a", kick_prop * 1.12), ("b", prop_spiral)):
    launch = (stack_tsi + extra) / 1000
    ratio = (launch / 40.0) / (50.0 / 40.0)
    print(f"mode ({mode}) launch ~{launch:.0f} t; ratio vs baseline: {ratio:.2f}x")
