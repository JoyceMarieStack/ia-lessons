---
name: sdd-terminology-audit
description: Audit spec-driven development (SDD) specification files — specs used as prompts for AI coding agents — for vocabulary ambiguity that could cause an agent to silently misinterpret intent during code generation. Produces (1) a machine-ready termbase with zero unresolved terms, meant for AGENTS.md or agent context as a ubiquitous-language constraint, and (2) an audit report distinguishing spec-critical conflicts from cosmetic ones. Plain markdown/CSV output, no code execution, so results are portable to whatever tool consumes the spec (Claude Code, Cursor, GitHub Spec-Kit, Kiro, etc.). Use when the user asks to audit terminology in specs, requirement specifications, SDD specs, Given/When/Then scenarios, or files meant to be handed to an AI coding agent — not human docs (use the separate terminology-audit skill for that). Trigger on "audit my specs," "check terminology before I generate code," or cues like Given/When/Then, MUST/SHALL, interface contracts.
---

# SDD Terminology Audit

Audits spec-driven development (SDD) specification files for vocabulary
ambiguity, with one goal that's different from ordinary documentation
review: **the spec is the prompt.** A human reading a slightly
inconsistent doc can usually infer intent from context. An AI coding
agent generating code from a spec cannot ask for clarification — it
silently picks an interpretation and generates code around it. That
silent resolution is a form of hallucination risk specific to SDD, and
it's what this skill exists to catch before it happens.

This skill is the SDD-specific sibling of `terminology-audit` (for human
documentation). Use that skill instead if auditing docs, READMEs, or
other human-facing material — the rubric below is deliberately different
and would misjudge severity if applied to prose written for people.

**This skill produces plain markdown/CSV output only — no scripts, no
code execution.** Specs written for SDD are meant to be consumed by
whatever AI coding agent or tool a team uses, not just Claude Code, so
the audit itself stays tool-agnostic: two files, produced entirely by
reading and reasoning, portable to any workflow.

## How this differs from documentation audits

| | Documentation audit | This skill (SDD) |
|---|---|---|
| Definitional weight | Headings, bold, first-use | Structural spec elements: interface/field names, Given/When/Then subjects, preconditions/postconditions, schema keys |
| Authority hierarchy | Defer to most authoritative *existing* doc | The spec itself is the top of the hierarchy; defer only to existing code identifiers if code already exists |
| Severity | Reader confusion / operational risk to a human | Whether the ambiguous term sits in a part of the spec that compiles into behavior, vs. background/rationale prose |
| "Done" bar for the termbase | Some rows can stay `needs stakeholder input` | **Zero** unresolved rows — an unresolved row handed to an agent is worse than no termbase at all |
| Deliverables | Termbase, diagram, report | Termbase, report (no diagram) |

## Workflow

### Step 1 — Inventory the spec material

List every spec file in scope. SDD specs are typically Markdown files
under a `specs/` directory, organized per feature or user story. Note
whether any implementation code already exists for this feature — if it
does, existing identifiers in code outrank the spec's own wording (see
Step 3).

### Step 2 — Read and extract terms by structural position, not typography

Read each spec directly. Unlike documentation, do not weight bold text or
headings as primary signals — SDD specs are often written in fairly flat
Markdown. Instead, extract terms based on where they sit structurally:

**High-weight positions (behavioral — this text becomes code):**
- Given/When/Then step subjects and objects
- Precondition / postcondition / invariant statements
- Interface, field, and parameter names
- MUST / SHALL / MUST NOT normative statements
- State machine states and transition names
- Error/exception names and status codes

**Low-weight positions (contextual — this text does not become code):**
- Rationale, background, "why this feature exists" prose
- Non-normative examples and illustrative commentary
- Open questions / notes-to-self sections

Tag every candidate term with which bucket it came from. This tag carries
through to severity classification in Step 3 — don't discard it.

As with documentation audits, watch for near-miss synonym pairs sharing
no surface characters (e.g., "cancel" vs. "void" vs. "revoke" all
referring to one lifecycle action) — these are easy to miss by pattern
matching and are exactly the kind of drift that produces inconsistent
method/field naming in generated code.

### Step 2a — Build an evidence table before analysing concepts

Before grouping terms into concepts, build an evidence table that preserves
the exact wording found in the specification. Use this table as the
provenance trail for every later conclusion.

| Exact text | Structural position | Source location | Candidate concept |
|---|---|---|---|

Apply these rules:

- Copy the wording exactly as it appears in the specification.
- Do not paraphrase or silently normalise the wording at this stage.
- Do not infer missing behaviour or invent a proposed requirement.
- Record repeated occurrences separately when they appear in different
  structural positions or sources.
- Give each source location enough precision for a reader to find the text
  directly, such as file, heading, requirement ID, scenario ID, or line range.
- Ensure every term, variant, definition, and finding in the final outputs is
  traceable to one or more rows in this evidence table.

Keep this table as working analysis. Include its relevant evidence in the
audit report so a reader can reconstruct why each conclusion was reached.

### Step 3 — Concept-oriented analysis, spec-first authority

For each distinct concept, work out:

1. **All the terms used for it**, per source, from Step 2 (include
   differing capitalization, pluralization, expanded vs. abbreviated
   forms, and differing part-of-speech usage).
2. **Authority order.** If implementation code already exists for this
   feature, existing identifiers in that code outrank the spec's
   wording — the spec should conform to what's already built, not the
   reverse. If no code exists yet, the spec is the ground truth; there's
   no more-authoritative source to defer to, so resolve conflicts by
   which term better matches the domain's actual terminology (check for
   existing product/business vocabulary if available) rather than by
   deferring to "the most authoritative doc."
3. **The preferred term**, using these default heuristics:
   - An existing code identifier or externally-published API/field name
     always wins if the feature is already implemented.
   - Otherwise, prefer the term that best matches established domain/
     business vocabulary over an invented or overly technical synonym.
   - Prefer full/expanded forms as canonical, with abbreviations noted
     as accepted shorthand after first use.
   - When usage is a genuine toss-up, don't force a decision — mark it
     `needs stakeholder input` (this must be resolved before Step 4
     completes — see below).
4. **A classification for every term+source pair** ("card"), using the
   same four-way scheme as the documentation skill:

   | Symbol | Meaning |
   |--------|---------|
   | `●` unambiguous | Clearly scoped, matches the concept, is the preferred term |
   | `○` correct-in-context | Technically correct but narrower than the concept |
   | `△` ambiguous | Reader/agent has to guess which meaning applies |
   | `✕` conflict | Same word, incompatible meaning across sources |

5. **A severity tag for every card**, carried over from Step 2:
   `behavioral` (sits in a high-weight structural position) or
   `contextual` (sits in prose/background). This is what separates
   blocking issues from cosmetic ones in this skill — treat it as
   mandatory, not optional metadata.

**Build one settled classification table before generating any
deliverable.** Don't let the termbase and report re-derive judgments
independently — decide the preferred term, status, symbol, and severity
for every concept once, then generate both outputs from that single
table. Cross-check before delivery: pick two or three concepts and
confirm the preferred term, forbidden variants, and severity agree
identically across the termbase and the report. If they don't agree, the
analysis wasn't actually settled — resolve it, don't paper over the
mismatch by picking whichever answer sounds most confident.

Out of everything classified `✕` with `behavioral` severity, identify
the one that would cause the worst generation error if an agent picked
the wrong meaning — lead the report's summary with this.






### Keep terminology decisions separate from specification findings

Do not mix controlled-vocabulary decisions with specification-quality
findings.

A terminology decision answers:

> What should this concept be called?

A specification finding answers:

> Is the behaviour involving this concept sufficiently and consistently
> specified?

Missing requirements, implied behaviour, conflicting acceptance criteria,
and underspecified inputs or outputs belong in the audit report. They are not
terms and must not become termbase rows unless the specification contains an
actual vocabulary concept that needs a canonical label.

Do not turn a proposed fix into a preferred term. For example, if the spec is
unclear whether a response returns an IANA identifier, an abbreviation, or
both, report that uncertainty as a specification finding. Do not create a
preferred term such as `return both an IANA timezone identifier field and a
timezone abbreviation field`.

### Step 4 — Build the termbase, with a stricter completion bar

Produce a CSV at `termbase.csv` (write it directly) with these columns:

| Column | Meaning |
|---|---|
| `term_id` | short stable slug, e.g. `access-token` |
| `preferred_term` | the canonical label |
| `part_of_speech` | noun / verb / adjective / proper noun |
| `definition` | 1–2 sentence definition in plain language |
| `usage_context` | where/how it's used |
| `forbidden_variants` | semicolon-separated list of terms NOT to use |
| `status` | `approved` / `provisional` (never `needs stakeholder input` — see below) |
| `severity` | `behavioral` or `contextual`, from Step 3 |
| `source_locations` | file(s)/section(s) where this concept appears |

Quote any field containing a comma so the CSV stays well-formed.

#### Preferred term rules

The `preferred_term` field must contain only the canonical label for a
concept. It must be a term a writer or coding agent can actually use.

It must never contain:

- `PROVISIONAL —` or other status labels
- recommendations or proposed fixes
- inferred behaviour
- implementation suggestions
- explanations or audit commentary

Use `status` to mark a concept as `provisional`. Put the reason in the
`definition` only when it helps define the concept; otherwise put the
uncertainty in the audit report.

Examples:

- Valid: `timezone abbreviation`
- Valid: `IANA timezone identifier`
- Invalid: `PROVISIONAL — return both an IANA timezone identifier field and a timezone abbreviation field`

A provisional term is still a usable canonical label. If no usable label can
be chosen without inventing behaviour or making a stakeholder decision, mark
the item as `needs stakeholder input` in the working classification and treat
it as blocking. Do not disguise the unresolved decision as a provisional term.

**Before delivering, check: does any concept from Step 3 still carry
`needs stakeholder input`?** If so, this termbase is not ready to hand
to a coding agent. Say so explicitly — list the unresolved terms and
what decision is needed — rather than delivering a termbase with open
questions baked silently into it. A human must resolve these before the
spec (and this termbase) goes to code generation. This is the one hard
rule that's stricter than the documentation skill: there, an unresolved
row is fine, since a human reader can hold ambiguity in mind. An agent
generating code cannot.

Once every row is `approved` or `provisional`, note in the deliverable
that this termbase is ready to be included in `AGENTS.md` or equivalent
agent-context configuration as a ubiquitous-language constraint.

### Step 5 — Write the audit report

Produce `terminology-audit-report.md` with these sections:

1. **Summary** — lead with whether the spec set is agent-ready, i.e.
   whether any `behavioral` `✕` conflicts or unresolved stakeholder
   items remain. State this before file counts or general scope.
2. **Inconsistencies found** — a table: Concept | Variants observed |
   Recommended preferred term | Severity | Locations | Notes. Group by
   concept. Sort or flag so `behavioral` rows are easy to find first.
3. **Items needing stakeholder input** — treat this as a blocking
   checklist, not optional reading, since Step 4 means these must be
   resolved before generation.
4. **Recommendations** — concrete next steps; where the termbase is
   fully resolved, explicitly recommend adding it to `AGENTS.md` or
   equivalent, so the audit closes the loop into the SDD workflow rather
   than sitting as a standalone report.

Keep it skimmable — tables over prose. This is a working document for an
engineering team about to run code generation, not a formal deliverable.

For every inconsistency or specification finding, include an evidence block or
table with:

| Exact spec text | Location | Interpretation | Why it matters |
|---|---|---|---|

Quote only the smallest exact fragment needed. The report must make the path
from source wording to conclusion visible without requiring the reader to
reverse-engineer the termbase.


### Settled Classification Table

Include the settled classification table in the audit report using these exact consumer-friendly columns:

| Concept | Wording found in spec | Judgment | Spec position | Wording to use |
| --- | --- | --- | --- | --- |

Use the columns as follows:

- `Concept`: the underlying domain concept being discussed.
- `Wording found in spec`: the exact variant found in the specification.
- `Judgment`: one of the classification symbols from the legend below.
- `Spec position`: `behavioral` or `contextual`.
- `Wording to use`: the approved preferred term.

Do not use internal analysis labels such as `Variant/card`, `Symbol`, `Severity`, or `Preferred term` as report column headings.

Immediately before the table, always print this legend:

| Symbol | Meaning                                                    |
| ------ | ---------------------------------------------------------- |
| `●`    | Preferred and unambiguous                                  |
| `○`    | Correct in context, but not the preferred term             |
| `△`    | Ambiguous; an agent may need to guess the intended meaning |
| `✕`    | Conflicting meaning; must be resolved                      |

Also explain the severity values:

| Severity     | Meaning                                                                                   |
| ------------ | ----------------------------------------------------------------------------------------- |
| `behavioral` | Appears in normative or executable specification text and may affect generated behavior   |
| `contextual` | Appears in explanatory or background text and is less likely to affect generated behavior |

Do not output a classification table containing symbols unless both legends are present in the same report.



## How to read the generated artefacts

The generated artefacts must be understandable together, not as isolated
files.

Read them in this order:

1. Start with `terminology-audit-report.md` to understand the issues and see
   the exact supporting evidence.
2. Use each finding's source location to inspect the cited wording in the
   specification.
3. Open `termbase.csv` to see the settled canonical term that should be used
   after the issue is understood or resolved.

For each termbase row:

1. Read `source_locations`.
2. Find those locations in the specification.
3. Compare the exact wording recorded in the report's evidence table.
4. Read `definition` and `forbidden_variants`.
5. Confirm that the preferred term is a reusable label, not a recommendation
   or an invented requirement.

The relationship between the files is:

```text
specification wording
        ↓
evidence table in the audit report
        ↓
concept grouping and classification
        ↓
canonical vocabulary in termbase.csv
```

If a reader cannot determine why a preferred term or finding exists by
following this chain, revise the audit before delivery.

### Step 6 — Deliver

Save `termbase.csv` and `terminology-audit-report.md`. If any termbase
rows are unresolved, deliver both anyway but say clearly, before
anything else, that the spec set is not yet ready for code generation
and why.

## Scope limitation, state this explicitly when relevant

This skill catches **vocabulary** ambiguity only. It cannot detect specs
that are internally *logically* inconsistent while using perfectly
consistent terminology (e.g., a precondition that contradicts a
postcondition elsewhere, both worded consistently) — that's a semantic
review problem, not a terminology problem, and is out of scope here.
