# SDD Terminology Audit Report — Timezone Meeting Utility

**Scope:** `examples/sample-sdd-dataset/spec.md` (feature spec, `001-timezone-utility`) and `examples/sample-sdd-dataset/spec-template.md` (the generic spec-kit template it was generated from — reviewed for structural-convention consistency only, not as a source of domain terminology).

**Caveat carried through this whole report:** `spec.md` states in its own header that it is "the abbreviated spec.md excerpt," not the complete file — some of the gaps flagged below (missing `FR-004`, no `SC-XXX` numbering) may simply be artifacts of that abbreviation rather than real defects in the source spec. Confirm against the full file in `mnriem/spec-kit-dotnet-cli-demo` before treating the "needs stakeholder input" items as blocking in a real project.

## Summary

**Not yet agent-ready.** Three concepts are marked `provisional` in `termbase.csv` and need a human decision before this spec should be handed to a coding agent for generation. None of the conflicts found are simple wording drift (no `✕` outright contradiction) — the risk here is *underspecification wearing the disguise of consistent vocabulary*: a word is used correctly everywhere it appears, but the spec never pins down enough about it for an agent to build the right thing without guessing.

The highest-risk item: **`timezone-output-representation`.** AS1 says the response includes a "timezone abbreviation" (e.g., "EST"), while FR-001 defines "timezone" elsewhere in the spec as the IANA identifier format (e.g., "America/New_York") used for *input*. The spec never states whether the *output* also includes the IANA identifier, only the abbreviation, or both. An agent generating a response schema has to invent an answer — and whichever one it picks, a later consumer of the API who expected the other will get a silent mismatch, not an error.

- Files scanned: 2 (1 filled spec, 1 template used only for convention cross-checks)
- Concepts extracted: 7 (all `behavioral` severity — this is a short, requirements-dense spec with almost no background prose)
- Blocking items: 3 (`timezone-output-representation`, `location-query-scope-country`, `error-message-requirement-gap`)
- Resolved without stakeholder input: 4

## Inconsistencies found

| Concept | Variants observed | Recommended preferred term | Severity | Locations | Notes |
|---|---|---|---|---|---|
| Timezone, as output | "timezone abbreviation" (AS1) vs. "timezone" used elsewhere for the IANA input identifier (FR-001) | *(blocking — see below)* | behavioral | AS1; FR-001 | Not a contradiction in wording — both uses are locally correct. The risk is that "timezone" quietly covers two different data shapes (display abbreviation vs. machine identifier) with nothing in the spec saying whether the output needs one, the other, or both. |
| Location query scope | "country" named as an accepted identifier (User Story, Edge Cases) with no matching FR | *(blocking — see below)* | behavioral | User Story 1; Edge Cases | `FR-004` is missing from the requirements list (jumps `FR-003` → `FR-005`), and "country" is the only identifier type named in the User Story that has no FR backing it. Likely where the missing requirement belongs — see caveat above. |
| Error-message behavior | Required by AS3 ("helpful error message...") and Success Criteria bullet 3 ("All error messages provide actionable guidance"), with no FR | *(blocking — see below)* | behavioral | AS3; Success Criteria | Same missing-`FR-004` root cause as the row above; flagged separately because it's a distinct concept (error handling vs. location scope), not because it needs a separate decision. |
| Result value returned to the user | "current time" (Title; Success Criteria bullet 1) vs. "current date and time" (User Story; AS1; AS2) | **current date and time** | behavioral | Title; User Story 1; AS1; AS2; Success Criteria | Resolved without stakeholder input — the three Acceptance Scenarios (the actual testable behavior) all specify date *and* time; the Title and one Success Criteria line under-describe it. If an agent names a generated function/endpoint off the Title alone (e.g. `GetCurrentTime`), it may build a time-only response that technically satisfies the narrower phrasing but fails AS1/AS2. |
| Location input, generically | "location" (AS3, Edge Cases) vs. "identifier" (User Story 1, once) | **location** | behavioral | User Story 1; AS3; Edge Cases | True synonym pair, same concept, no real confusion risk — flagged for consistency in generated field/parameter naming, not because a reader would misinterpret either term. |
| US postal code input | "US zip code (5-digit)" (FR-003, first use) vs. "zip code" (AS2, shorthand) | **US zip code** | behavioral | FR-003; AS2 | Fine as-is; shorthand comes after the qualified first use. Flagged only because a future spec revision introducing non-US postal codes would make bare "zip code" ambiguous — worth keeping the qualified form as the field name in code. |
| Timezone, as input | "IANA timezone identifiers" (FR-001) vs. bare "timezone" (AS1 example, Edge Cases) | **IANA timezone identifier** | behavioral | FR-001; AS1; Edge Cases | Unambiguous in context; included because it's the identifier the output-representation conflict above needs to stay distinct from. |

## Items needing stakeholder input

These block `termbase.csv` from being fully `approved`/ready. `provisional` rows above carry the audit's best-effort default so downstream work isn't fully stalled, but each needs an explicit decision before code generation:

1. **Does the lookup response return the IANA timezone identifier, the timezone abbreviation, or both?**
   AS1 only requires the abbreviation. `termbase.csv` provisionally recommends returning both as separate fields (satisfies AS1 and avoids losing the identifier), but this is a guess, not something the spec states.

2. **Is country-based lookup actually in scope?**
   Named in the User Story and an Edge Case, but has no Functional Requirement. Either restore the missing `FR-004` for country support, or remove "country" from the User Story/Edge Cases if it was descoped. (See the abbreviated-excerpt caveat — check the full source spec first; this may already be resolved there.)

3. **Is there a Functional Requirement for error-message behavior?**
   AS3 and a Success Criteria bullet both require "helpful"/"actionable" error messages, but no FR mandates this. Likely the same missing-`FR-004` gap as item 2 — confirm whether one FR should cover both, or two separate ones are needed.

## Recommendations

1. **Resolve the two items above tied to the missing `FR-004`** before this spec goes to code generation — start by checking the unabridged spec in the source repo, since the gap may just be an artifact of this being a teaching excerpt.
2. **Pin down the output schema for timezone data** (item 1) explicitly in the spec — e.g., add a line to AS1 or FR-001 stating the response includes both `timezone_id` (IANA) and `timezone_abbreviation`, or whichever the team decides.
3. **Align the Title and Success Criteria wording** with "current date and time" (the AS-established term) so a generated function/endpoint name doesn't silently drop the date component.
4. **Adopt the `spec-template.md` `SC-XXX` numbering convention** for Success Criteria bullets in `spec.md` — the template defines it (paralleling `FR-XXX`), but the filled spec's Success Criteria bullets have no IDs, which makes them harder to reference from tasks/tests later. Minor, non-blocking.
5. **Once items 1–3 above are resolved,** re-run this audit (or simply flip the three `provisional` rows to `approved`) and add `termbase.csv` to `AGENTS.md` or equivalent agent-context configuration as a ubiquitous-language constraint before generation.
