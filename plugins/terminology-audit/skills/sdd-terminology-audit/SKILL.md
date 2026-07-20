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