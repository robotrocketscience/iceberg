#!/usr/bin/env python3
"""Pre-script: R-bag-silicate-rejection-derivation bounds.

Vapor conditions vs bag temperature, the free-molecular entrainment cutoff
d_max(T), and the throughput area A_ice -- the brackets behind the SCOPE
pre-registration. Does NOT run the full T x PSD carryover grid or the grid-life
loop (run.py). Deterministic.

Question: is the bag silicate rejection factor an intrinsic ~1e-4 (as R11 and
R_silicate_contamination ASSUMED), or a temperature-and-PSD-gated derived quantity?
"""
import math

M_H2O = 0.018015           # kg/mol
R_UNIV = 8.314             # J/mol/K
R_SPEC = R_UNIV / M_H2O    # J/kg/K water vapor
RHO_GRAIN = 3000.0         # kg/m^3 silicate
L_TRANSPORT = 1.0          # m bag vapor transport length
MDOT = 5.0e-4              # kg/s thruster demand (0.5 g/s, matrix RF-ion upper)


def p_sat_ice(T):
    """Marti & Mauersberger 1993 ice sublimation vapor pressure [Pa]."""
    return 10 ** (-2663.5 / T + 12.537)


def vapor(T):
    P = p_sat_ice(T)
    rho_g = P * M_H2O / (R_UNIV * T)                 # kg/m^3
    cbar = math.sqrt(8 * R_UNIV * T / (math.pi * M_H2O))
    J = P / math.sqrt(2 * math.pi * R_SPEC * T)      # kg/m^2/s Hertz-Knudsen
    d_max = rho_g * L_TRANSPORT / RHO_GRAIN          # m, St=1 free-molecular
    A_ice = MDOT / J                                  # m^2 to feed thruster
    return P, rho_g, cbar, J, d_max, A_ice


def main():
    print("=" * 72)
    print("Vapor conditions + entrainment cutoff vs bag temperature")
    print("=" * 72)
    print(f"    {'T(K)':>5} {'P_sat(Pa)':>11} {'rho_g(kg/m3)':>13} {'J(kg/m2/s)':>11} "
          f"{'d_max':>10} {'A_ice(m2)':>10}")
    for T in (200, 220, 250, 273):
        P, rho_g, cbar, J, d_max, A_ice = vapor(T)
        dnm = d_max * 1e9
        dstr = f"{dnm:.2f}nm" if dnm < 1000 else f"{dnm/1000:.2f}um"
        print(f"    {T:>5} {P:>11.3g} {rho_g:>13.3e} {J:>11.3e} {dstr:>10} {A_ice:>10.3g}")

    print()
    print("=" * 72)
    print("What the cutoff implies for carryover (power-law PSD q=3.5)")
    print("=" * 72)
    q = 3.5
    r_min = 5e-9
    for r_max, tag in ((1e-6, "r_max=1um"), (1e-4, "r_max=100um")):
        print(f"    {tag}: massfrac of silicate below the cutoff radius d_max/2 --")
        for T in (200, 250, 273):
            _, _, _, _, d_max, _ = vapor(T)
            r_cut = min(d_max / 2, r_max)
            num = r_cut ** (4 - q) - r_min ** (4 - q)
            den = r_max ** (4 - q) - r_min ** (4 - q)
            f = max(0.0, num / den)
            print(f"        T={T}K  d_max/2={d_max/2*1e9:8.3g} nm  f_pass_gas={f:.3e}")
    print()
    print("    SCOPE bands: d_max ~0.5nm@200K, 150-250nm@250K, 1-2um@273K;")
    print("    A_ice <=3 m2 @200K; f_pass_gas ~0 (cold) to 1e-2..3e-1 (warm);")
    print("    R11 assumed 1e-4 => a cold-bag + small-sub-micron-mass corner, not intrinsic.")


if __name__ == "__main__":
    main()
