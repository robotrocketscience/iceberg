"""Corridor-era showcase figures (rounds 192-215).

Generates the four static charts and two animations that accompany the
2026-07 refresh of the README and the website write-up:

  plots/18_departure_anchor.png    - spiral departure delta-v vs thrust acceleration
  plots/19_corridor_map.png        - the sole surviving corridor, priced in launches
  plots/20_breakeven_race.png      - breakeven vs decaying price bands over the mission
  plots/21_capture_reliability.png - joint capture reliability vs chunk count
  plots/departure_spiral.gif       - animated low-thrust spiral out of Saturn's well
  plots/price_race.gif             - animated market decay vs corridor breakeven

Inputs are the committed result JSONs of the rounds that produced the numbers:
R_departure_anchor_resolution, R_per_phase_propellant_fidelity,
R_corridor_financial_model, R_multi_chunk_per_mission (execution 2).

Run from the repo root:  python water-prop/scripts/plot_corridor_figures.py
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
ROUNDS = ROOT / "water-prop" / "rounds"
OUT = ROOT / "plots"

candidates = ["Helvetica Neue", "Arial", "DejaVu Sans"]
available = {f.name for f in fm.fontManager.ttflist}
SANS = next((c for c in candidates if c in available), "sans-serif")

INK_DARK = "#0a0e1a"
INK_PANEL = "#11182a"
INK_GRID = "#1f2a44"
INK_TEXT = "#e6edf5"
INK_MUTED = "#8a96b0"
ACCENT_GOLD = "#e8b54e"
ACCENT_BLUE = "#5fa8ff"
ACCENT_TEAL = "#3ed4c0"
ACCENT_RED = "#ff7676"
ACCENT_GREEN = "#7adc7a"

DASH_BG = "#ffffff"
DASH_FG = "#1a1f2e"
DASH_MUTED = "#5a6378"
DASH_GRID = "#e6e8ed"
DASH_BLUE = "#3b6ee5"
DASH_TEAL = "#0fb9a3"
DASH_RED = "#dc4a4a"
DASH_AMBER = "#d49612"
DASH_GREEN = "#2c9c4f"


def style_space():
    plt.rcParams.update({
        "font.family": SANS, "font.size": 13,
        "figure.facecolor": INK_DARK, "axes.facecolor": INK_DARK,
        "savefig.facecolor": INK_DARK, "axes.edgecolor": INK_GRID,
        "axes.labelcolor": INK_TEXT, "axes.titlecolor": INK_TEXT,
        "xtick.color": INK_MUTED, "ytick.color": INK_MUTED,
        "grid.color": INK_GRID, "legend.facecolor": INK_PANEL,
        "legend.edgecolor": INK_GRID, "legend.labelcolor": INK_TEXT,
        "text.color": INK_TEXT,
    })


def style_dashboard():
    plt.rcParams.update({
        "font.family": SANS, "font.size": 13,
        "figure.facecolor": DASH_BG, "axes.facecolor": DASH_BG,
        "savefig.facecolor": DASH_BG, "axes.edgecolor": DASH_GRID,
        "axes.labelcolor": DASH_FG, "axes.titlecolor": DASH_FG,
        "xtick.color": DASH_MUTED, "ytick.color": DASH_MUTED,
        "grid.color": DASH_GRID, "legend.facecolor": DASH_BG,
        "legend.edgecolor": DASH_GRID, "legend.labelcolor": DASH_FG,
        "text.color": DASH_FG,
    })


# ---------------------------------------------------------------- #
# 18 - departure anchor: dv vs thrust acceleration
# ---------------------------------------------------------------- #

def fig_departure_anchor():
    d = json.load(open(ROUNDS / "R_departure_anchor_resolution" / "results" / "dv_vs_accel.json"))
    pairs = sorted((float(k), v["dv_km_s"]) for k, v in d["dv_vs_accel"].items())
    accels = [p[0] for p in pairs]
    dvs = [p[1] for p in pairs]
    style_space()
    fig, ax = plt.subplots(figsize=(9, 5.6))
    ax.semilogx(accels, dvs, "-o", color=ACCENT_TEAL, lw=2.2, ms=7, zorder=5,
                label="spiral departure, integrated (RK4)")
    ax.axhline(d["impulsive_oberth_km_s"], color=ACCENT_GOLD, lw=1.8, ls="--",
               label=f"impulsive burn from the same orbit: {d['impulsive_oberth_km_s']} km/s")
    ax.axhline(9.0, color=ACCENT_RED, lw=1.5, ls=":",
               label="the 9.0 km/s anchor the electric family was priced at")
    lo, hi = d["campaign_electric_accel_band_m_s2"]
    ax.axvspan(lo, hi, color=ACCENT_BLUE, alpha=0.14, zorder=1)
    ax.annotate("what flyable electric\nthrust actually gives\n(22.5-24.2 km/s)",
                xy=(math.sqrt(lo * hi), 19.6), ha="center", va="center",
                fontsize=11.5, color=ACCENT_BLUE)
    ax.annotate("~1 m/s$^2$ needed to\napproach the old anchor",
                xy=(0.1, 14.31), xytext=(0.012, 11.6), fontsize=11, color=INK_MUTED,
                arrowprops=dict(arrowstyle="->", color=INK_MUTED, lw=1))
    ax.set_xlabel("thrust acceleration (m/s$^2$), log scale")
    ax.set_ylabel("delta-v to leave Saturn from the B ring (km/s)")
    ax.set_title("Why the electric return died: low thrust cannot buy the Oberth discount")
    ax.grid(True, alpha=0.5)
    ax.legend(loc="lower left", fontsize=11)
    ax.set_ylim(8, 26)
    fig.tight_layout()
    fig.savefig(OUT / "18_departure_anchor.png", dpi=110)
    plt.close(fig)


# ---------------------------------------------------------------- #
# 19 - corridor map
# ---------------------------------------------------------------- #

def fig_corridor_map():
    d = json.load(open(ROUNDS / "R_per_phase_propellant_fidelity" / "results" / "min_multiplier_vs_f.json"))
    mc = json.load(open(ROUNDS / "R_multi_chunk_per_mission" / "worktree172651-execution-2026-07-26" /
                        "results" / "multi_chunk_results.json"))["H-M5_corridor_with_overheads"]
    cells = [
        ("500 t harvest\n150 kWe reactor\n2 chunks", d["corridor_150kwe_500t"]["min_mult_at_opt"],
         mc["500t_150kwe"]["with_overhead"]["delivered_t"], mc["500t_150kwe"]["with_overhead"]["round_trip_yr_incl_ops"]),
        ("1,000 t harvest\n200 kWe reactor\n3 chunks", d["corridor_200kwe_1000t"]["min_mult_at_opt"],
         mc["1000t_200kwe"]["with_overhead"]["delivered_t"], mc["1000t_200kwe"]["with_overhead"]["round_trip_yr_incl_ops"]),
    ]
    style_dashboard()
    fig, ax = plt.subplots(figsize=(9, 5.6))
    x = [c[1] * 100 for c in cells]          # tonnes to low Earth orbit (multiplier x 100 t)
    y = [c[2] for c in cells]
    ax.scatter(x, y, s=[260, 420], color=DASH_TEAL, zorder=5, edgecolor=DASH_FG, linewidth=1.2)
    for (label, mult, dt, yr), xi, yi in zip(cells, x, y):
        ax.annotate(f"{label}\n{dt} t delivered, {yr} yr",
                    xy=(xi, yi), xytext=(xi + 30, yi - 16), fontsize=10.5, color=DASH_FG)
        ax.annotate(f"x{mult:.2f} = {xi:,.0f} t of lift", xy=(xi, yi), xytext=(xi - 40, yi + 7),
                    fontsize=10.5, color=DASH_MUTED, ha="right")
    ax.axhspan(0, 30, color=DASH_RED, alpha=0.06)
    ax.text(1480, 15, "below the 30 t class the corridor\nwas asked to clear", fontsize=10.5,
            color=DASH_RED, ha="right")
    ax.axhline(209, color=DASH_RED, lw=1.4, ls="--")
    ax.text(1480, 214, "cheapest sovereign-hurdle delivery class (209 t): unreachable anywhere", fontsize=10.5,
            color=DASH_RED, ha="right")
    ax.text(660, 130, "electric-thruster family:\ncloses nowhere at any launch scale\n(dead at the honest 22.5 km/s departure)",
            fontsize=11, color=DASH_MUTED, style="italic")
    ax.set_xlim(500, 1500)
    ax.set_ylim(0, 240)
    ax.set_xlabel("launch mass required in low Earth orbit (tonnes) - 6-11 fully-refilled-Starship-class flights")
    ax.set_ylabel("water delivered to Earth orbit (tonnes)")
    ax.set_title("The one corridor that still closes: electrolysis-fed nuclear-thermal return")
    ax.grid(True, alpha=0.6)
    fig.tight_layout()
    fig.savefig(OUT / "19_corridor_map.png", dpi=110)
    plt.close(fig)


# ---------------------------------------------------------------- #
# 20/gif - breakeven vs decaying prices
# ---------------------------------------------------------------- #

BANDS = [(5025, "bulk price if demand reaches 100 t/yr"),
         (2225, "bulk mid band"),
         (505, "bulk low band")]
CAPTIVE = (10000, 25000)
DECAY = 0.87          # 13 percent per year clearing-price decline
BREAKEVEN_CHEAP = 15513   # 88 t cell, $100/kg launch, undiscounted
BREAKEVEN_SOV = 26176     # same cell at the 3 percent sovereign discount
DELIVERY = (18.7, 21.1)


def _price_axes(ax):
    t = np.linspace(0, 22, 200)
    for p0, label in BANDS:
        ax.plot(t, p0 * DECAY ** t, color=DASH_BLUE, lw=1.6, alpha=0.85)
        ax.annotate(label, xy=(0.15, p0 * 1.12), fontsize=9.5, color=DASH_BLUE)
    ax.fill_between(t, CAPTIVE[0] * DECAY ** t, CAPTIVE[1] * DECAY ** t,
                    color=DASH_AMBER, alpha=0.18)
    ax.annotate("captive buyers (\\$10-25k/kg)", xy=(0.15, 11200), fontsize=9.5, color=DASH_AMBER)
    ax.axhline(BREAKEVEN_CHEAP, color=DASH_RED, lw=2.0)
    ax.annotate("cheapest conceivable breakeven: \\$15,513/kg\n(mature Starship launch, \\$0.5B ship, money costs nothing)",
                xy=(8.6, BREAKEVEN_CHEAP * 1.10), fontsize=10, color=DASH_RED)
    ax.axhline(BREAKEVEN_SOV, color=DASH_RED, lw=1.4, ls="--")
    ax.annotate("same mission at a 3% sovereign discount: \\$26,176/kg",
                xy=(0.15, BREAKEVEN_SOV * 1.14), fontsize=10, color=DASH_RED)
    ax.axvspan(*DELIVERY, color=DASH_GREEN, alpha=0.15)
    ax.annotate("water\narrives", xy=(sum(DELIVERY) / 2, 33), ha="center", fontsize=10, color=DASH_GREEN)
    ax.set_yscale("log")
    ax.set_ylim(20, 60000)
    ax.set_xlim(0, 22)
    ax.set_xlabel("years after the program starts")
    ax.set_ylabel("dollars per kilogram of water in low Earth orbit (log scale)")
    ax.grid(True, which="both", alpha=0.4)


def fig_breakeven_race():
    style_dashboard()
    fig, ax = plt.subplots(figsize=(9, 5.8))
    _price_axes(ax)
    ax.set_title("The market runs away: every price band decays below breakeven before delivery")
    fig.tight_layout()
    fig.savefig(OUT / "20_breakeven_race.png", dpi=110)
    plt.close(fig)


def gif_price_race():
    style_dashboard()
    fig, ax = plt.subplots(figsize=(7.2, 4.8), dpi=72)
    t_full = np.linspace(0, 22, 200)
    frames = 110

    def draw(i):
        ax.clear()
        tmax = 22 * (i + 1) / frames
        mask = t_full <= tmax
        for p0, _ in BANDS:
            ax.plot(t_full[mask], p0 * DECAY ** t_full[mask], color=DASH_BLUE, lw=1.6)
        ax.fill_between(t_full[mask], CAPTIVE[0] * DECAY ** t_full[mask],
                        CAPTIVE[1] * DECAY ** t_full[mask], color=DASH_AMBER, alpha=0.2)
        ax.axhline(BREAKEVEN_CHEAP, color=DASH_RED, lw=2.0)
        ax.annotate("cheapest breakeven \\$15,513/kg", xy=(0.3, BREAKEVEN_CHEAP * 1.18),
                    fontsize=10, color=DASH_RED)
        if tmax >= DELIVERY[0]:
            ax.axvspan(DELIVERY[0], min(tmax, DELIVERY[1]), color=DASH_GREEN, alpha=0.2)
            gap = BREAKEVEN_CHEAP / (BANDS[0][0] * DECAY ** DELIVERY[0])
            ax.annotate(f"delivery: best price is\n{gap:,.0f}x below breakeven",
                        xy=(DELIVERY[0] - 0.4, 45), fontsize=11, color=DASH_GREEN, ha="right")
        ax.annotate(f"year {tmax:4.1f}", xy=(0.985, 0.96), xycoords="axes fraction",
                    ha="right", va="top", fontsize=13, color=DASH_FG)
        ax.set_yscale("log")
        ax.set_ylim(20, 60000)
        ax.set_xlim(0, 22)
        ax.set_xlabel("years after program start")
        ax.set_ylabel("$ per kg of water in orbit")
        ax.set_title("Delivered-water prices decay 13%/yr; the mission takes 19-21 years", fontsize=11.5)
        ax.grid(True, which="both", alpha=0.4)

    anim = FuncAnimation(fig, draw, frames=frames)
    anim.save(OUT / "price_race.gif", writer=PillowWriter(fps=18))
    plt.close(fig)


# ---------------------------------------------------------------- #
# 21 - capture reliability
# ---------------------------------------------------------------- #

def fig_capture_reliability():
    d = json.load(open(ROUNDS / "R_multi_chunk_per_mission" / "worktree172651-execution-2026-07-26" /
                       "results" / "multi_chunk_results.json"))["H-M2_reliability"]
    ns = [1, 2, 3, 5]
    style_dashboard()
    fig, ax = plt.subplots(figsize=(8.4, 5.2))
    ax.plot(ns, [d[f"p0.961_N{n}"] for n in ns], "-o", color=DASH_TEAL, lw=2.2, ms=8,
            label="optimized harpoon operating point (96.1% per capture)")
    ax.plot(ns, [d[f"p0.549_N{n}"] for n in ns], "-o", color=DASH_RED, lw=2.2, ms=8,
            label="un-optimized prior mean (54.9% per capture)")
    ax.axhline(0.80, color=DASH_AMBER, lw=1.6, ls="--", label="mission reliability floor (0.80)")
    ax.set_xticks(ns)
    ax.set_xlabel("chunks captured per mission")
    ax.set_ylabel("probability every capture succeeds")
    ax.set_title("Multi-chunk physics is cheap; capture reliability is the corridor's real gate")
    ax.set_ylim(0, 1.0)
    ax.grid(True, alpha=0.6)
    ax.legend(loc="lower left", fontsize=10.5)
    fig.tight_layout()
    fig.savefig(OUT / "21_capture_reliability.png", dpi=110)
    plt.close(fig)


# ---------------------------------------------------------------- #
# gif - departure spiral
# ---------------------------------------------------------------- #

def gif_departure_spiral():
    GM = 3.7931e7            # km^3/s^2
    r0 = 1.0e5               # km
    a_thrust = 1e-5          # km/s^2  (= 1e-2 m/s^2, 100x the flyable electric band)

    def accel(state):
        x, y, vx, vy = state
        r = math.hypot(x, y)
        v = math.hypot(vx, vy) or 1.0
        ag = -GM / r**3
        return np.array([vx, vy, ag * x + a_thrust * vx / v, ag * y + a_thrust * vy / v])

    period = 2 * math.pi * math.sqrt(r0**3 / GM)
    dt = period / 400
    s = np.array([r0, 0.0, 0.0, math.sqrt(GM / r0)])
    xs, ys, ts = [s[0]], [s[1]], [0.0]
    t = 0.0
    while True:
        k1 = accel(s); k2 = accel(s + 0.5 * dt * k1)
        k3 = accel(s + 0.5 * dt * k2); k4 = accel(s + dt * k3)
        s = s + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        t += dt
        xs.append(s[0]); ys.append(s[1]); ts.append(t)
        E = 0.5 * (s[2]**2 + s[3]**2) - GM / math.hypot(s[0], s[1])
        if E >= 0 or t > 0.2 * 365.25 * 86400:
            break
    xs, ys, ts = np.array(xs), np.array(ys), np.array(ts)
    dv_total = a_thrust * ts[-1]

    style_space()
    fig, ax = plt.subplots(figsize=(6.4, 6.4), dpi=72)
    frames = 130
    idx = np.unique(np.linspace(1, len(xs) - 1, frames).astype(int))
    lim = max(abs(xs).max(), abs(ys).max()) * 1.06

    def draw(i):
        ax.clear()
        j = idx[min(i, len(idx) - 1)]
        ax.plot(xs[:j], ys[:j], color=ACCENT_TEAL, lw=1.0, alpha=0.9)
        ax.plot(xs[j], ys[j], "o", color=ACCENT_TEAL, ms=6)
        ring = plt.Circle((0, 0), r0, fill=False, color=INK_GRID, ls="--", lw=0.9)
        ax.add_patch(ring)
        ax.plot(0, 0, "o", color=ACCENT_GOLD, ms=16)
        dv = a_thrust * ts[j]
        ax.text(0.03, 0.97, f"delta-v spent: {dv:5.1f} km/s\nday {ts[j]/86400:5.0f}",
                transform=ax.transAxes, va="top", fontsize=12, color=INK_TEXT)
        ax.text(0.03, 0.06,
                "an impulsive burn from the same orbit: 8.6 km/s\n"
                f"the spiral, even at 100x flyable electric thrust: {dv_total:.1f} km/s\n"
                "at flyable electric thrust: 22.5-24.2 km/s",
                transform=ax.transAxes, fontsize=9.5, color=INK_MUTED)
        ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim)
        ax.set_aspect("equal"); ax.axis("off")
        ax.set_title("Leaving Saturn's gravity well on low thrust", color=INK_TEXT, fontsize=13)

    anim = FuncAnimation(fig, draw, frames=frames)
    anim.save(OUT / "departure_spiral.gif", writer=PillowWriter(fps=16))
    plt.close(fig)


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    fig_departure_anchor(); print("18_departure_anchor.png")
    fig_corridor_map(); print("19_corridor_map.png")
    fig_breakeven_race(); print("20_breakeven_race.png")
    fig_capture_reliability(); print("21_capture_reliability.png")
    gif_price_race(); print("price_race.gif")
    gif_departure_spiral(); print("departure_spiral.gif")
