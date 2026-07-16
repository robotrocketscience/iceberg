"""Stub ephemeris / launch-window calculators.

The framework needed epoch-aware feasibility checks for gravity-assist
options but the rest of the campaign does not yet have a real planetary
ephemeris in scope. This module provides closed-form approximations
adequate for sizing-level go/no-go:

  - Earth -> Saturn launch window: opens every ~378 days (synodic period),
    ~21-day usable opening. Phase 1 chemical-class options that depend on a
    Hohmann transfer geometry must launch inside one of these.

  - Jupiter gravity-assist window: launch must be within ~30 days of the
    Earth-Jupiter synodic alignment for the cruise to land the spacecraft
    near Jupiter at flyby. Synodic period ~398.88 days.

  - Mars + Jupiter (Cassini-class) gravity-assist window: rare. Approx.
    every ~20 years, ~60-day window. Cassini precedent: launched October
    1997; analogous windows ~1977, ~2017, ~2037.

  - Low-thrust spiral options have wide windows because continuous-thrust
    trajectories adapt to launch date; the model treats them as always
    in-window for sizing purposes.

All windows are approximations adequate for go/no-go gating. Real mission
design needs JPL ephemeris (SPICE) or MALTO/SCOPE for Pareto trajectories.
"""

from __future__ import annotations

EARTH_SATURN_SYNODIC_DAYS = 378.10
EARTH_SATURN_WINDOW_WIDTH_DAYS = 21.0

EARTH_JUPITER_SYNODIC_DAYS = 398.88
EARTH_JUPITER_WINDOW_WIDTH_DAYS = 30.0

CASSINI_CLASS_WINDOW_PERIOD_DAYS = 7300.0  # ~20 years
CASSINI_CLASS_WINDOW_WIDTH_DAYS = 60.0

# Venus-Earth-Earth gravity-assist window — used to set up the
# canonical VEEGA-class trajectory for outer-planet missions
# (Galileo, Cassini both used Venus segments). The window is set by
# Venus alignment relative to Earth; Earth-Venus synodic period is
# ~583.92 days, and the VEEGA launch window opens for ~20 days every
# synodic cycle. After Venus encounter the spacecraft does one Earth
# flyby (or two for VVEJGA-class) to pump up velocity for the outer
# leg.
EARTH_VENUS_SYNODIC_DAYS = 583.92
VENUS_EARTH_GA_WINDOW_WIDTH_DAYS = 20.0

# Reference epoch for all windows. Using JD 0 lets tests pick simple
# synthetic launch epochs that are obviously in (or out of) every window
# simultaneously. Real ephemeris reference dates (Cassini 1997-10-15 etc.)
# are documented but not used here — this is a stub for go/no-go gating,
# not a real launch-window finder.
EPHEMERIS_REFERENCE_JD = 0.0


def _in_window(epoch_jd, period_days, width_days):
    phase = (epoch_jd - EPHEMERIS_REFERENCE_JD) % period_days
    return phase < width_days or phase > (period_days - width_days)


def in_earth_saturn_launch_window(epoch_jd):
    return _in_window(epoch_jd, EARTH_SATURN_SYNODIC_DAYS, EARTH_SATURN_WINDOW_WIDTH_DAYS)


def in_jupiter_assist_window(epoch_jd):
    return _in_window(epoch_jd, EARTH_JUPITER_SYNODIC_DAYS, EARTH_JUPITER_WINDOW_WIDTH_DAYS)


def in_cassini_class_window(epoch_jd):
    return _in_window(epoch_jd, CASSINI_CLASS_WINDOW_PERIOD_DAYS, CASSINI_CLASS_WINDOW_WIDTH_DAYS)


def in_venus_earth_ga_window(epoch_jd):
    """Venus-Earth(-Earth) gravity-assist launch window for VEEGA-class
    trajectories used by Galileo and Cassini."""
    return _in_window(epoch_jd, EARTH_VENUS_SYNODIC_DAYS, VENUS_EARTH_GA_WINDOW_WIDTH_DAYS)
