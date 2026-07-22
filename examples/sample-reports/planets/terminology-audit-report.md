# Terminology Audit Report — Solar System Sample Docs

## Summary

Scanned 3 documents (`dwarf-planets.md`, `mars.md`, `solar-system-overview.md`, all sourced from NASA Science). This is a small corpus, so treat this as a first pass — additional low-frequency variants may surface as more docs are added. Found 8 concepts worth tracking, of which 5 use terminology consistently or in correctly narrower/context-specific ways, and 3 have real inconsistency: one genuine conflict (same word, two meanings) and two "needs stakeholder input" toss-ups. Overall severity: **mostly cosmetic**, with one exception — the "moon" vs "Moon" vs "satellite" overload is worth fixing because it's disambiguated only by capitalization, which is fragile for search, TMS/localization extraction, and skimming readers.

## Inconsistencies found

| Concept | Variants observed | Recommended preferred term | Locations | Notes |
|---|---|---|---|---|
| Natural satellite of a planet | "moon"/"moons" (generic), "Moon" (proper noun, Earth's), "satellite" (Charon comparison) | `moon` (generic); reserve capitalized `Moon` strictly for Earth's | solar-system-overview.md (Facts, Moons, #9); mars.md (Humans to Mars); dwarf-planets.md (Star of Dwarf Planets, Why No Longer a Planet) | **True conflict** — capitalization is the only disambiguator between "any moon" and "Earth's Moon," and "satellite" is a third word for the same underlying concept. |
| Uncrewed exploration vehicle | "rover," "orbiter," "spacecraft," "mission" | `rover` / `orbiter` for the vehicle type; `spacecraft` as umbrella; reserve `mission` for the program, not the hardware | mars.md (Active Missions); dwarf-planets.md (Star of Dwarf Planets); solar-system-overview.md (#9) | Rover vs. orbiter is a correct, meaningful distinction (surface vehicle vs. non-landing vehicle) — don't flatten that. The looser problem is "mission" occasionally standing in for the craft itself (e.g. "Dawn mission... visited by a spacecraft"). |
| Milky Way arm containing our solar system | "Orion Arm," "Orion Spur" | Pick one as canonical (see below) | solar-system-overview.md (Facts, #4) | Source itself presents these as interchangeable ("Orion Arm, or Orion Spur"). Not wrong, just undecided. |
| The solar system's star | "host star" (generic), "the Sun" (proper noun) | Both are fine — flagged for awareness, not for correction | dwarf-planets.md (Overview) | Correct-in-context: "host star" is used in the abstract 3-point IAU planet definition; "the Sun" is used when talking about our specific system. Not a real problem, just worth noting the pattern is intentional. |

## Items needing stakeholder input

| Concept | Competing options | Why it's not a clear call |
|---|---|---|
| Natural satellite of a planet | `moon` vs `satellite`, plus the `Moon`/`moon` capitalization rule | Astronomy content sometimes wants "satellite" as the more technical/precise term (as used for Charon's relative-size comparison), but "satellite" is heavily overloaded with artificial satellites in general usage. Need a style-guide ruling on when (if ever) "satellite" is preferred over "moon." |
| Milky Way arm name | `Orion Arm` vs `Orion Spur` | Both are legitimate, NASA-published names for the same feature (the source text uses them interchangeably in the same sentence). Picking one as canonical is a style choice, not a factual correction — needs an editorial decision, not an audit judgment call. |
| "Mission" as vehicle vs. program | `mission` vs `spacecraft`/`rover`/`orbiter` | Depends on whether docs want to keep the informal, narrative register NASA's public-facing pages use (where blending program-name and hardware is common and reads naturally) or move toward stricter engineering precision. This is a register/audience call, not a pure terminology fix. |

## Recommendations

1. **Fix the moon/Moon/satellite overload first** — it's the one item with real ambiguity risk (capitalization-only disambiguation breaks in search, TMS extraction, and text-to-speech). Add an explicit style-guide rule: lowercase `moon`/`moons` for the generic class, capitalized `Moon` reserved for Earth's, and drop standalone `satellite` unless directly comparing relative sizes.
2. **Add a short "Naming & Terms" section to the style guide** covering the two toss-up items (Orion Arm/Spur, mission vs. vehicle-type words) so future docs don't have to re-decide this per-document.
3. **Use `dwarf-planets.md` as the internal style exemplar** — it's the most consistent source (correct acronym expansion pattern, uniform dwarf-planet definition throughout) and is a good template for onboarding new doc authors.
4. **Re-run this audit as more docs are added** — this corpus is only 3 files; NASA's broader solar-system content (other planets, asteroid/comet pages) will likely introduce more "vehicle terminology" and "moon vs. satellite" instances worth tracking against the termbase above.
