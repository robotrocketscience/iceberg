# R-saturn-system-water-depot-demand — READING (5-section template)

**Worker:** hyperion (re-spawn 2) · **Date:** 2026-05-26

## Hypotheses adjudicated

H1 **held (strong)** · H2 **held but moot** (demand is structurally zero, not probability-gated) · H3 **falsified** (Δv-inverted: ~15.4 km/s to use the depot vs ~0 savings) · H4 **held-as-reframe but weaker than the SCOPE expected** (the relay re-imports the loaded-inbound kill) · H5 **held** (very-low-probability, not before 2050) · **H6 (load-bearing) held — in a stronger form than pre-registered.**

Predicted-vs-measured: my STUDY.md prior expected H1 and H6 to hold and the interesting question to be H3-vs-H4 weight. That was right, with one sharpening I did not fully anticipate: **H3 is not merely thin, it is Δv-inverted** (a negative-sum market, not a small one), and **H4 does not cleanly escape the binding kill** — so the campaign's "depot waiver re-opens the matrix at single-kWe" intuition is half-true (it frees the *filler*) but incomplete (the *relay* re-imports the wall).

## Headline

**There is no commercial market for water at Saturn at a 2026 baseline, and the one architecture-internal reading that could substitute for a market (a two-vehicle relay) does not cleanly escape the constraint that closed the one-vehicle architecture.** Matrix decision #15 **option (b) (depot waiver) is not commercially actionable.** The three live Saturn-destination missions (Dragonfly, two Enceladus flagships) are self-provisioned science missions; no commercial Saturn entrant exists; the logistics market is Δv-inverted; human presence is off-horizon. **Decision #15 collapses toward option (c)** (hold L0-04 strict, accept campaign termination at flyable power), softened only by decision #16's parametric L0-04-floor sweep — not by a depot waiver.

## Reading (for the project owner)

1. **Option (b) is not a live commercial option.** A Saturn depot is technologically conceivable but economically empty: there is no customer, there is no forecastable customer before 2050, and the logistics "customer" (a passing mission refueling) is killed by the ~15.4 km/s cost of capturing into and re-departing the Saturn system to reach the depot. Building a depot for water nobody can profitably collect is a stranded asset. **Do not carry option (b) as a market-demand path.**

2. **The depot's only coherent rationale is internal (H4), and it is not free.** The reason a depot looked attractive — it removes the Earth-return leg and its reactor-lifetime/mass-floor kills — applies *only to the vehicle that stays at Saturn (the filler)*. To actually get water to Earth you still need a relay to fly the loaded inbound leg, which is the leg that killed the one-vehicle architecture. So the two-vehicle split **relocates the binding kill onto the relay, it does not remove it.** Decision #15(b), if pursued, is therefore mislabeled: it is not a depot-demand decision, it is a **two-vehicle-architecture decision**, and that architecture has not been shown to beat the one-vehicle architecture on the binding axis.

3. **My recommendation:** treat decision #15 as **(c) with #16 as the only live softener.** Demote the H4 two-vehicle relay from "worth a dedicated round" (the SCOPE's framing) to **"conditional candidate, gated on first identifying a relay-propulsion concept that escapes the loaded-inbound kill."** Two such concepts are worth a one-paragraph feasibility look before committing a full round: (a) a **depot-water-fed high-thrust relay** (trade reactor-lifetime cumulative burn for short high-power sprints fed by the depot itself), and (b) **Earth aerocapture on the relay** (deletes the Earth-side capture burn; campaign finding is that aerocapture is necessary-but-not-sufficient because Saturn departure + cruise braking remain). If neither survives a back-of-envelope, option (b) is fully closed and decision #15 is unambiguously (c).

## Cross-learning

- **Negative for matrix decision #15 option (b):** depot waiver is not commercially actionable. Recommend the matrix record #15 → (c) as the substantive reading, with the depot-waiver branch annotated "demand-side empty (R-saturn-system-water-depot-demand); only internal-relay rationale survives, and it re-imports the binding kill."
- **Conditional candidate, not a clean hand-off, for R-iceberg-two-vehicle-relay-architecture:** the SCOPE expected this round to recommend standing up the two-vehicle round. I recommend a **gate** instead: stand it up only after a relay-propulsion-escape concept passes a back-of-envelope. SCOPE outline below.
- **Reinforces the three-bets / iapetus framing:** with option (b) demand-empty and option (c) the live reading, the campaign's standing verdict (technology-demonstrator class; commercial-class hard-conditioned on a reactor program per L0-24) is unchanged. This round removes the last "maybe a depot rescues it" escape hatch on the demand side.
- **Methodology note:** the depot-waiver intuition is a clean example of *moving a constraint instead of removing it.* Removing the return leg helps the filler and feels like progress, but conservation of the delivery problem means the loaded inbound Δv has to be paid by *some* vehicle. Worth a PROTOCOL-lesson candidate: *when an architecture change "removes" a binding leg, check which vehicle now flies that leg before crediting the relief.* (Compounds the campaign's existing scope-mismatch lesson from titan-4.)

## Revisit

The frozen prediction held. The one place I was usefully wrong: I pre-registered H4 as "the only reading under which option (b) is genuinely actionable" — implying it probably was actionable as an architecture question. The back-of-envelope showed it is *not even that* without a new relay-propulsion concept. So the round's net result is more negative than my own prior: option (b) has no demand-side path AND no clean architecture-side path. Decision #15 is (c) unless a relay-propulsion escape is found.

---

## SCOPE outline (conditional) — R-iceberg-two-vehicle-relay-architecture

**Gate:** stand up only if a relay-propulsion concept that escapes the loaded-inbound kill passes a back-of-envelope first. Two candidates to screen:
1. **Depot-water-fed high-thrust relay** — relay refuels at the depot and flies the inbound on a short high-power profile, trading cumulative reactor burn-time (the killer) for peak power. Question: does the relay's inbound burn-time fall below the reactor-lifetime wall while staying inside a flyable power/mass envelope?
2. **Earth-aerocapture relay** — relay does Earth aerocapture to delete the Earth-side capture burn. Question: does deleting *only* the Earth capture burn (Saturn departure + cruise braking remain) bring the relay's loaded-inbound under the wall?

**If either passes:** full round encodes the two-vehicle architecture in `mission_graph` (filler tree + relay tree), reports total cost-per-delivered-kg vs the one-vehicle baseline, and checks whether the depot-decoupling buys anything net. **If neither passes:** option (b) is fully closed; no round needed; decision #15 is unambiguously (c).
