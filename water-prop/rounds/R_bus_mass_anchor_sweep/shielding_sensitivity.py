"""Quick sanity check: add radiation shadow shield + PCU + cables to bus mass and re-check
the 9 commercial-strict Cassini-anchor cells from R-bus-mass-anchor-sweep.

Shield mass anchors (NASA SP-100 / Kilopower / NEXTM heritage):
- Shadow shield: ~1 kg/kWe for unmanned electronics dose budget (low end)
- Shadow shield: ~5 kg/kWe for crewed-or-conservative budget (high end)
- PCU at 500 kWe: 0.5-2 t (use 1.5 t at 500 kWe, scale linearly with P)
- Cables/harness: 0.5 t fixed
"""

import math

G0 = 9.80665
ETA_THRUSTER = 0.5
SEC_PER_YEAR = 365.25 * 86400.0

# the 9 Cassini-anchor commercial-strict cells (P_kWe, chunk_t, sp_W/kg, aero_km/s, isp_s, delivered_t, RT_yr)
cells = [
    (500, 200, 10, 10, 2934, 91.53, 12.69),
    (200, 200, 10, 10, 2000, 74.91, 14.62),
    (500, 200,  5, 10, 2934, 71.21, 13.76),
    (500, 200, 10, 10, 2000, 57.27, 10.48),
    (200, 100, 10, 10, 2934, 47.59, 13.87),
    (200, 100,  5, 10, 2934, 39.47, 14.94),
    (500, 100, 10, 10, 2934, 34.18, 10.45),
    (200, 100, 10, 10, 2000, 31.04, 11.20),
    (500, 200,  5, 10, 2000, 30.54, 11.13),
]

def rerun(P, chunk, sp, aero, isp, shield_kg_per_kWe, m_bus, m_pcu_at_500, cables_t):
    v_e = isp * G0
    dv = 25000 - aero * 1000
    m_reactor = P / sp
    m_bag = max(0.5, 0.05 * chunk)
    m_thrust = 0.01 * P
    m_shield = shield_kg_per_kWe * P / 1000.0  # convert kg→t
    m_pcu = m_pcu_at_500 * (P / 500.0)
    m_dry = m_bus + m_bag + m_reactor + m_thrust + m_shield + m_pcu + cables_t
    m_0 = m_dry + chunk
    ratio = math.exp(dv / v_e)
    m_f = m_0 / ratio
    m_w = m_0 - m_f
    if m_w > chunk:
        return None, None, None, m_dry, False
    delivered = chunk - m_w
    e_jet = 0.5 * m_w * 1000 * v_e * v_e
    e_elec = e_jet / ETA_THRUSTER
    t_burn = e_elec / (P * 1000)
    rt = 6 + 1 + t_burn / SEC_PER_YEAR
    strict = rt <= 15
    commercial = delivered >= 30
    return delivered, rt, t_burn / SEC_PER_YEAR, m_dry, strict and commercial

scenarios = [
    ("Cassini bus only (original)", 0, 2, 0, 0),
    ("Cassini + light shield (1 kg/kWe) + 1.5t PCU + 0.5t cables", 1, 2, 1.5, 0.5),
    ("Cassini + medium shield (3 kg/kWe) + 1.5t PCU + 0.5t cables", 3, 2, 1.5, 0.5),
    ("Cassini + heavy shield (5 kg/kWe) + 2t PCU + 1t cables", 5, 2, 2.0, 1.0),
    ("Europa Clipper bus (5.9 t) + light shield (1 kg/kWe)", 1, 5.9, 1.0, 0.5),
    ("Europa Clipper bus (5.9 t) + medium shield (3 kg/kWe)", 3, 5.9, 1.5, 0.5),
]

for label, shield_kg, m_bus, m_pcu, cables in scenarios:
    print(f"\n=== {label} ===")
    print(f"{'P kWe':>6} {'chunk':>6} {'sp':>5} {'aero':>5} {'Isp':>5} {'m_dry':>7} {'delivered':>10} {'RT yr':>7} {'pass?':>6}")
    survivors = 0
    for (P, chunk, sp, aero, isp, _, _) in cells:
        delivered, rt, tb, m_dry, p = rerun(P, chunk, sp, aero, isp, shield_kg, m_bus, m_pcu, cables)
        if delivered is None:
            print(f"{P:>6} {chunk:>6} {sp:>5} {aero:>5} {isp:>5} {m_dry:>7.1f} {'INFEAS':>10} {'-':>7} {'-':>6}")
        else:
            mark = "PASS" if p else "FAIL"
            if p: survivors += 1
            print(f"{P:>6} {chunk:>6} {sp:>5} {aero:>5} {isp:>5} {m_dry:>7.1f} {delivered:>10.2f} {rt:>7.2f} {mark:>6}")
    print(f"  → {survivors}/9 cells still commercial-strict")
