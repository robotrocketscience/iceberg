"""Physical constants and unit conversions used across waterprop."""

# Standard gravity (m/s^2). Used to convert v_e <-> Isp.
G0 = 9.80665

# Unit conversions
TORR_TO_PA = 133.322
BAR_TO_PA = 1e5
ATM_TO_PA = 101325.0

# Astrodynamics (SI, km-based)
GM_SUN = 1.32712440018e11      # km^3/s^2
GM_EARTH = 3.986004418e5        # km^3/s^2
GM_SATURN = 3.7931187e7         # km^3/s^2
AU = 1.495978707e8              # km

R_EARTH = 6378.137              # km
R_SATURN = 60268.0              # km
A_EARTH = 1.0 * AU              # km
A_SATURN = 9.5826 * AU          # km
