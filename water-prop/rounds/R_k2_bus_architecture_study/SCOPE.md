# R-k2-bus-architecture-study — K2 Space buses as ICEBERG vehicle inspiration

**Status:** scope, pre-study. Authored by Saturn (worker), 2026-05-21 latest.

**Context.** K2 Space (US satellite-bus startup, $250M Series C at $3B valuation December 2025) is selling a design philosophy ICEBERG should pay attention to: mass-abundant, power-rich, launcher-bay-filling, mass-produced spacecraft buses optimized for the Falcon Heavy / Starship / New Glenn era.

K2's specs (public, May 2026):
- **Mega-class** (live, first launch February 2026 on the "Gravitas" Space Force mission): 1,000 kg payload capacity, 20 kilowatts of power, 27-meter solar array tip-to-tip. ~$60M contract value.
- **Giga-class** (next platform, announced, not yet built): 100 kilowatts of power, sized for Starship and New Glenn payload bays.

Direct comparison to ICEBERG vehicle requirements (50-200 tonnes, 10 kilowatts to 1 megawatt of power, 7+ year deep-space mission): K2 buses are **one to two orders of magnitude too small** as a literal chassis. And K2's entire power model is solar — at Saturn, solar flux is ~1 percent of Earth's value, so a K2-scale array delivers ~200 watts at Saturn, not the kilowatts needed.

But the *architectural pattern* is the right one for ICEBERG demonstrator-era vehicles.

This round answers: **can the ICEBERG vehicle be a stack of N K2 Giga buses (or scaled-up successors) via on-orbit assembly, and what does that imply for the framework's vehicle_mass_kg and power_kwe sweep axes?**

## Five sub-questions

1. **Stack arithmetic.** 10 × Giga = 1 megawatt power, ~300-tonne stack wet mass. Falls inside the ICEBERG vehicle-mass grid (50-200 tonnes nominal, 200+ tonnes for multi-launch). Does the supply-chain / manufacturing realism cost get cheaper or more expensive than a clean-sheet ICEBERG bus?
2. **Specific power.** K2 Mega is ~20 watts per kilogram (1 tonne / 20 kilowatts). Giga is projected at ~30 watts per kilogram (best case). Compare to flown radioisotope hardware (~5 watts per kilogram) and to the locked-belief 40 watts per kilogram megawatt-class aspirational target.
3. **Solar-at-Saturn problem.** K2 only does solar power. Hybrid architecture (K2 buses with grafted nuclear power module at Saturn-arrival point) would solve this but K2 has not announced reactor integration. Is this a contractual/business gap or a fundamental design constraint?
4. **Deep-space hardening.** Mega is marketed as "deep space rated" but has no operational deep-space heritage. ICEBERG cruise is 7+ years. What heritage path connects current LEO/MEO/GEO buses to a Saturn-rated vehicle?
5. **Procurement vs build.** Cost and schedule comparison: ICEBERG procuring N K2 Giga units vs ICEBERG building a clean-sheet bus. Decision criterion for the demonstrator gate.

## Inputs to acquire

- K2 Space published specs (public sources only).
- Comparable supplier landscape: Maxar (1300-class bus), Lockheed Martin LM-2100, Northrop Grumman GEOStar, Boeing 702, OneWeb Joint Venture (Airbus).

## Deliverables

1. A vehicle-architecture table comparing ICEBERG clean-sheet vs K2 Giga stack vs hybrid across mass, power, cost (rough order of magnitude), schedule, supply-chain risk, deep-space heritage.
2. A specific recommendation on whether to add a `vehicle_bus_architecture` parameter to the mission_graph framework.
3. A short "what would a K2-style ICEBERG demonstrator look like?" sketch — a concept of operations slide for pitch use.

## Out of scope

- Building any code in the mission_graph framework. This is a research / business-strategy SCOPE.

## Predecessor work

- The May 2026 audit of mission_graph framework gaps that surfaced this as a missing architectural axis.

## Priority

Low — engineering work, but the procurement-vs-build question is a downstream consequence of the demonstrator-gate go/no-go, not a precondition for it. Useful before pitch conversations.
