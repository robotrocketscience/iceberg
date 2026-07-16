"""Block 4 composite exit-burn power audit.

Computes exit-burn time across (exit_power, exit_isp) grid, finds minimum
exit power that fits 6-month residence dwell at each Isp, computes cathode-
on time per mission for the composite at multiple power classes, and
adjudicates H1-H8 hypotheses.

Block 4 composite nominal:
- exit dv = 7.4 km/s
- spacecraft mass at exit = 380 t (200 collected + 180 dry-effective)
- exit Isp = 7000 s, exit power = 500 kWe, anode efficiency = 0.65
- residence dwell budget = 6 months
"""

from __future__ import annotations

import csv
import json
from math import exp
from pathlib import Path

G0 = 9.80665
SEC_PER_MONTH = 30.4375 * 86400.0       # average month length
SEC_PER_YEAR = 365.25 * 86400.0
HOUR = 3600.0

OUT = Path(__file__).parent / "results"
OUT.mkdir(parents=True, exist_ok=True)

# Block 4 composite nominal parameters
M_AT_EXIT_T = 380.0                      # 200 collected + 180 dry-effective
DV_EXIT_KMS = 7.4
DV_INBOUND_KMS_NET = 23.2                # 24.7 - 1.5 aerocapture saving
ISP_INBOUND_S = 5000.0
M_AFTER_EXIT_AT_ISP7000_T = 344.86       # from Block 9 baseline

ETA_CANONICAL = 0.65                     # matrix optimistic
ETA_REALISTIC = 0.30                     # R-cathode-life sensitivity

RESIDENCE_DWELL_MONTHS = 6.0
RESIDENCE_DWELL_SEC = RESIDENCE_DWELL_MONTHS * SEC_PER_MONTH

# Advanced-Electric-Propulsion-System design life
AEPS_DESIGN_LIFE_HOUR = 50000.0


def burn_time_seconds(
    power_we: float,
    isp_s: float,
    dv_kms: float,
    m_start_t: float,
    eta: float = ETA_CANONICAL,
) -> dict:
    """Continuous-thrust burn time at fixed power.

    thrust = 2 * jet_power / v_exhaust = 2 * eta * P / (Isp * g0)
    mass_flow = thrust / (Isp * g0)
    propellant = m_start * (1 - 1/mass_ratio)
    burn_time = propellant / mass_flow
    """
    v_e = isp_s * G0
    thrust_n = 2.0 * eta * power_we / v_e
    mr = exp(dv_kms * 1000.0 / v_e)
    m_propellant_kg = m_start_t * 1000.0 * (1.0 - 1.0 / mr)
    mass_flow_kgs = thrust_n / v_e
    if mass_flow_kgs <= 0.0:
        return {"burn_time_s": float("inf"), "thrust_n": 0.0,
                "m_propellant_kg": m_propellant_kg, "mr": mr}
    t_s = m_propellant_kg / mass_flow_kgs
    return {
        "burn_time_s":      t_s,
        "thrust_n":         thrust_n,
        "m_propellant_kg":  m_propellant_kg,
        "mr":               mr,
        "mass_flow_kgs":    mass_flow_kgs,
    }


def min_power_for_dwell(
    isp_s: float, dv_kms: float, m_start_t: float,
    dwell_s: float, eta: float = ETA_CANONICAL,
) -> float:
    """Minimum power (W) such that burn_time <= dwell_s.

    Since burn_time = propellant * v_e / thrust = propellant * v_e^2 / (2 * eta * P),
    we get P_min = propellant * v_e^2 / (2 * eta * dwell_s).
    """
    v_e = isp_s * G0
    mr = exp(dv_kms * 1000.0 / v_e)
    m_propellant_kg = m_start_t * 1000.0 * (1.0 - 1.0 / mr)
    return m_propellant_kg * v_e * v_e / (2.0 * eta * dwell_s)


# -----------------------------------------------------------------------------
# Grid sweep: (exit_power, exit_isp) -> burn time
# -----------------------------------------------------------------------------

POWER_GRID_KWE = [500, 1000, 2000, 5000, 10000]      # kilowatt-electric
ISP_GRID_S = [3000, 5000, 7000, 9000]

grid_rows = []
for power_kwe in POWER_GRID_KWE:
    for isp_s in ISP_GRID_S:
        for eta_label, eta in [("canonical", ETA_CANONICAL),
                               ("realistic", ETA_REALISTIC)]:
            r = burn_time_seconds(power_kwe * 1000.0, isp_s,
                                  DV_EXIT_KMS, M_AT_EXIT_T, eta)
            grid_rows.append({
                "power_kwe":       power_kwe,
                "isp_s":           isp_s,
                "eta":             eta_label,
                "thrust_n":        f"{r['thrust_n']:.2f}",
                "mr":              f"{r['mr']:.4f}",
                "m_propellant_t":  f"{r['m_propellant_kg']/1000:.2f}",
                "burn_time_year":  f"{r['burn_time_s']/SEC_PER_YEAR:.3f}",
                "burn_time_month": f"{r['burn_time_s']/SEC_PER_MONTH:.2f}",
                "fits_6mo_dwell":  "yes" if r['burn_time_s'] <= RESIDENCE_DWELL_SEC else "no",
            })

with open(OUT / "burn_time_grid.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(grid_rows[0].keys()))
    w.writeheader()
    w.writerows(grid_rows)


# -----------------------------------------------------------------------------
# Closure envelope: minimum power for 6-month dwell at each Isp
# -----------------------------------------------------------------------------

closure_rows = []
for isp_s in ISP_GRID_S:
    for dwell_months in [6, 12, 24, 36]:
        for eta_label, eta in [("canonical", ETA_CANONICAL),
                               ("realistic", ETA_REALISTIC)]:
            dwell_s = dwell_months * SEC_PER_MONTH
            p_min_w = min_power_for_dwell(isp_s, DV_EXIT_KMS, M_AT_EXIT_T,
                                          dwell_s, eta)
            closure_rows.append({
                "isp_s":         isp_s,
                "dwell_months":  dwell_months,
                "eta":           eta_label,
                "min_power_kwe": f"{p_min_w/1000:.1f}",
                "min_power_mwe": f"{p_min_w/1e6:.3f}",
            })

with open(OUT / "closure_envelope.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(closure_rows[0].keys()))
    w.writeheader()
    w.writerows(closure_rows)


# -----------------------------------------------------------------------------
# Per-mission cathode-on time (exit + inbound) at canonical Block 4 nominal
# -----------------------------------------------------------------------------

cathode_rows = []
for power_kwe in POWER_GRID_KWE:
    for isp_exit in [5000, 7000, 9000]:
        for eta_label, eta in [("canonical", ETA_CANONICAL)]:
            t_exit = burn_time_seconds(power_kwe * 1000.0, isp_exit,
                                       DV_EXIT_KMS, M_AT_EXIT_T, eta)
            # Compute m_after_exit at this isp_exit
            v_e_exit = isp_exit * G0
            mr_exit = exp(DV_EXIT_KMS * 1000.0 / v_e_exit)
            m_after_exit_t = M_AT_EXIT_T / mr_exit
            # Inbound burn at this power, Isp_inbound 5000, dv 23.2
            t_inbound = burn_time_seconds(power_kwe * 1000.0,
                                          ISP_INBOUND_S,
                                          DV_INBOUND_KMS_NET,
                                          m_after_exit_t, eta)
            t_total_s = t_exit["burn_time_s"] + t_inbound["burn_time_s"]
            t_total_hr = t_total_s / HOUR
            cathode_rows.append({
                "power_kwe":          power_kwe,
                "isp_exit_s":         isp_exit,
                "eta":                eta_label,
                "t_exit_year":        f"{t_exit['burn_time_s']/SEC_PER_YEAR:.3f}",
                "t_inbound_year":     f"{t_inbound['burn_time_s']/SEC_PER_YEAR:.3f}",
                "t_total_hour":       f"{t_total_hr:.0f}",
                "fraction_aeps_5mn":  f"{5*t_total_hr/AEPS_DESIGN_LIFE_HOUR:.3f}",
                "fraction_aeps_10mn": f"{10*t_total_hr/AEPS_DESIGN_LIFE_HOUR:.3f}",
            })

with open(OUT / "cathode_budget.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(cathode_rows[0].keys()))
    w.writeheader()
    w.writerows(cathode_rows)


# -----------------------------------------------------------------------------
# Hypothesis adjudication
# -----------------------------------------------------------------------------

# H1: exit burn at Block 4 nominal (500 kWe, Isp 7000, eta 0.65, dv 7.4, 380 t)
nominal = burn_time_seconds(500_000.0, 7000.0, DV_EXIT_KMS,
                            M_AT_EXIT_T, ETA_CANONICAL)
t_nominal_month = nominal["burn_time_s"] / SEC_PER_MONTH
H1_status = ("held" if 5.0 <= t_nominal_month <= 7.0
             else "marginal" if 3.0 <= t_nominal_month <= 12.0
             else ("falsified_high" if t_nominal_month > 12.0 else "falsified_low"))

# H2: power required for 6-month exit burn at Isp 7000
p_min_h2_mwe = min_power_for_dwell(7000.0, DV_EXIT_KMS, M_AT_EXIT_T,
                                   RESIDENCE_DWELL_SEC, ETA_CANONICAL) / 1e6
H2_status = ("held" if 1.0 <= p_min_h2_mwe <= 3.0
             else "marginal" if 0.5 <= p_min_h2_mwe <= 15.0
             else ("falsified_high" if p_min_h2_mwe > 15.0
                   else "falsified_low"))

# H3: burn time at 500 kWe / Isp 7000 in years range
t_nominal_year = nominal["burn_time_s"] / SEC_PER_YEAR
H3_status = ("held" if 5.0 <= t_nominal_year <= 15.0
             else "marginal" if 1.0 <= t_nominal_year <= 20.0
             else ("falsified_high" if t_nominal_year > 20.0
                   else "falsified_low"))

# H4: min power for 6-month at Isp 5000
p_min_h4_mwe = min_power_for_dwell(5000.0, DV_EXIT_KMS, M_AT_EXIT_T,
                                   RESIDENCE_DWELL_SEC, ETA_CANONICAL) / 1e6
H4_status = ("held" if 1.0 <= p_min_h4_mwe <= 3.0
             else "marginal" if 0.5 <= p_min_h4_mwe <= 10.0
             else ("falsified_high" if p_min_h4_mwe > 10.0
                   else "falsified_low"))

# H5: composite doesn't close at 500 kWe / Isp 7000 in 6 months
H5_status = "held" if (H1_status == "falsified_high"
                       and H2_status in ("marginal", "falsified_high")) else "falsified"

# H6: mission duration with 9-year exit > 20 years vs L0-05 ceiling
cruise_round_trip_year = 12.0           # ~Hohmann Earth-Saturn round trip
inbound_burn_year = 1.5                  # Block 4 inbound burn at Isp 5000 / 500 kWe
total_mission_year = (t_nominal_year + inbound_burn_year + cruise_round_trip_year)
H6_status = "held" if total_mission_year > 20.0 else "falsified"

# H7: at Isp 5000 exit, composite delivered fraction < 12% AND burn time > 5 years
# Recompute delivered fraction at Isp 5000 (no exit-Isp uplift)
mr_exit_5000 = exp(DV_EXIT_KMS * 1000.0 / (5000.0 * G0))
mr_in_5000 = exp(DV_INBOUND_KMS_NET * 1000.0 / (5000.0 * G0))
# Composite no-Jupiter: 200 collected, 180 dry-effective, 4.13 t shield (Block 8)
m_shield = 4.13
m_dry_total = 180 + m_shield
m_at_exit = 200 + m_dry_total
m_post_exit = m_at_exit / mr_exit_5000
m_at_earth = m_post_exit / mr_in_5000
m_delivered = max(0.0, m_at_earth - m_dry_total)
df_isp5000_pct = m_delivered / 200 * 100
# Burn time at 500 kWe / Isp 5000
t_exit_5000_year = burn_time_seconds(500_000.0, 5000.0, DV_EXIT_KMS,
                                     M_AT_EXIT_T, ETA_CANONICAL)["burn_time_s"] / SEC_PER_YEAR
H7_status = ("held" if df_isp5000_pct < 12.0 and t_exit_5000_year > 5.0
             else "marginal" if df_isp5000_pct < 14.0 or t_exit_5000_year > 3.0
             else "falsified")

# H8: min power to close 6-month exit at Isp in [5000, 7000] range
p_min_5000 = min_power_for_dwell(5000.0, DV_EXIT_KMS, M_AT_EXIT_T,
                                 RESIDENCE_DWELL_SEC, ETA_CANONICAL) / 1e6
p_min_7000 = min_power_for_dwell(7000.0, DV_EXIT_KMS, M_AT_EXIT_T,
                                 RESIDENCE_DWELL_SEC, ETA_CANONICAL) / 1e6
H8_status = ("held" if 3.0 <= max(p_min_5000, p_min_7000) <= 15.0
             else "marginal" if 1.0 <= max(p_min_5000, p_min_7000) <= 20.0
             else "falsified_low" if max(p_min_5000, p_min_7000) < 1.0
             else "falsified_high")

summary = {
    "model_parameters": {
        "m_at_exit_t": M_AT_EXIT_T,
        "dv_exit_kms": DV_EXIT_KMS,
        "eta_canonical": ETA_CANONICAL,
        "eta_realistic": ETA_REALISTIC,
        "residence_dwell_months": RESIDENCE_DWELL_MONTHS,
        "aeps_design_life_hour": AEPS_DESIGN_LIFE_HOUR,
    },
    "block4_nominal_burn": {
        "power_kwe": 500,
        "isp_s": 7000,
        "eta": ETA_CANONICAL,
        "thrust_n": nominal["thrust_n"],
        "m_propellant_t": nominal["m_propellant_kg"] / 1000,
        "burn_time_years": t_nominal_year,
        "burn_time_months": t_nominal_month,
        "block4_assumed_months": 6.0,
        "actual_vs_assumed_factor": t_nominal_month / 6.0,
    },
    "min_power_for_6mo_dwell_canonical": {
        "isp_3000_mwe":
            min_power_for_dwell(3000.0, DV_EXIT_KMS, M_AT_EXIT_T,
                                RESIDENCE_DWELL_SEC, ETA_CANONICAL) / 1e6,
        "isp_5000_mwe": p_min_5000,
        "isp_7000_mwe": p_min_7000,
        "isp_9000_mwe":
            min_power_for_dwell(9000.0, DV_EXIT_KMS, M_AT_EXIT_T,
                                RESIDENCE_DWELL_SEC, ETA_CANONICAL) / 1e6,
    },
    "isp5000_revert_path": {
        "delivered_fraction_pct": df_isp5000_pct,
        "exit_burn_year_at_500kWe": t_exit_5000_year,
    },
    "hypothesis_adjudication": {
        "H1_burn_5to7_months_block4_nominal": {
            "status": H1_status,
            "observed_months": t_nominal_month,
            "predicted": "[5, 7] months",
        },
        "H2_power_for_6mo_at_isp7000_1to3MWe": {
            "status": H2_status,
            "observed_mwe": p_min_h2_mwe,
            "predicted": "[1, 3] MWe",
        },
        "H3_burn_5to15_years_at_500kWe_isp7000": {
            "status": H3_status,
            "observed_years": t_nominal_year,
        },
        "H4_min_power_isp5000_1to3MWe": {
            "status": H4_status,
            "observed_mwe": p_min_h4_mwe,
        },
        "H5_block4_composite_doesnt_close": {
            "status": H5_status,
        },
        "H6_mission_duration_exceeds_L0-05": {
            "status": H6_status,
            "total_mission_years": total_mission_year,
        },
        "H7_isp5000_revert_doesnt_save": {
            "status": H7_status,
            "df_isp5000_pct": df_isp5000_pct,
            "burn_year_isp5000_500kWe": t_exit_5000_year,
        },
        "H8_resolution_requires_3to15MWe": {
            "status": H8_status,
            "p_min_5000_mwe": p_min_5000,
            "p_min_7000_mwe": p_min_7000,
        },
    },
}

with open(OUT / "summary.json", "w") as f:
    json.dump(summary, f, indent=2, default=str)


# -----------------------------------------------------------------------------
# Console summary
# -----------------------------------------------------------------------------

print("=" * 72)
print("R-exit-burn-power-audit -- results")
print("=" * 72)
print()
print(f"Block 4 nominal exit burn (500 kWe, Isp 7000, eta 0.65, dv 7.4, 380 t):")
print(f"  Thrust:         {nominal['thrust_n']:.2f} N")
print(f"  Propellant:     {nominal['m_propellant_kg']/1000:.2f} t")
print(f"  Mass ratio:     {nominal['mr']:.4f}")
print(f"  Burn time:      {t_nominal_year:.2f} years "
      f"({t_nominal_month:.1f} months)")
print(f"  Block 4 assumed: 6 months. Actual/assumed: "
      f"{t_nominal_month/6.0:.1f}x")
print()
print("Minimum exit power for 6-month dwell (canonical eta):")
print(f"  Isp 3000 s:   {min_power_for_dwell(3000.0, DV_EXIT_KMS, M_AT_EXIT_T, RESIDENCE_DWELL_SEC, ETA_CANONICAL)/1e6:>7.3f} MWe")
print(f"  Isp 5000 s:   {p_min_5000:>7.3f} MWe")
print(f"  Isp 7000 s:   {p_min_7000:>7.3f} MWe")
print(f"  Isp 9000 s:   {min_power_for_dwell(9000.0, DV_EXIT_KMS, M_AT_EXIT_T, RESIDENCE_DWELL_SEC, ETA_CANONICAL)/1e6:>7.3f} MWe")
print()
print("Isp 5000 'revert' path (no exit-Isp uplift):")
print(f"  Composite delivered fraction:  {df_isp5000_pct:.2f}%")
print(f"  Exit burn time at 500 kWe:     {t_exit_5000_year:.2f} years")
print()
print(f"Mission duration with 9-year exit:")
print(f"  Cruise round-trip (Hohmann):   {cruise_round_trip_year:.1f} yr")
print(f"  + Inbound burn:                 {inbound_burn_year:.1f} yr")
print(f"  + Exit burn at 500 kWe Isp 7000: {t_nominal_year:.2f} yr")
print(f"  Total:                          {total_mission_year:.1f} yr (L0-05 ceiling 15 yr)")
print()
print("Hypothesis adjudication:")
for hname, hdata in summary["hypothesis_adjudication"].items():
    print(f"  {hname}: {hdata['status']}")
