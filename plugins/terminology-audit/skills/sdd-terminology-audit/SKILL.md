---
name: sdd-terminology-audit
description: Audit spec-driven development specifications and requirements for vocabulary ambiguity that could lead developers or coding agents to interpret the same concept differently. Produce an evidence-backed terminology audit report and a CSV termbase of supported canonical terms. Use for SDD specs, requirement files, Given/When/Then scenarios, MUST/SHALL statements, schemas, interfaces, and other documents intended to guide implementation. Do not use for general prose editing or broad logical-consistency review.
---

# SDD Terminology Audit

Audit terminology in specifications used to guide implementation. Identify places where different wording could cause the same concept to be interpreted, named, filtered, stored, or implemented differently.

Produce two files:

- `terminology-audit-report.md`: evidence and explanations for terminology findings.
- `termbase.csv`: supported canonical vocabulary for resolved concepts.

Do not execute code. Read only the specification files and any implementation or domain sources explicitly included in the audit scope.

## Scope boundary

This is a terminology audit, not a complete specification review.

Only report a terminology finding when wording creates a vocabulary problem, such as:

- two labels appear to name the same concept;
- one label appears to name different concepts;
- a term has two plausible meanings in the audited material;
- an abbreviation and expanded form could create separate identifiers;
- a field, state, command, event, or error is named inconsistently;
- a generic phrase weakens or broadens a more precise implementation term.

Do not classify these as terminology findings:

- missing execution order;
- missing optional-versus-required behaviour;
- missing inputs or outputs;
- incomplete acceptance criteria;
- unstated implementation details;
- logical contradictions expressed with consistent vocabulary;
- general writing quality or style preferences.

Omit out-of-scope observations. Do not add a separate specification-review section.

## Workflow

### Step 1 — Inventory the audit scope

List every specification file included in the audit.

Also list any additional sources explicitly inspected to establish terminology authority, such as:

- implementation identifiers;
- database schemas;
- interface contracts;
- published APIs;
- repository conventions;
- documented stakeholder decisions.

Do not claim authority from a source that was not inspected.

### Step 2 — Extract exact evidence

Read the specification directly. Extract candidate terminology from structural positions that can influence implementation:

- Given/When/Then subjects and objects;
- preconditions, postconditions, and invariants;
- MUST, SHALL, and MUST NOT statements;
- interface, field, parameter, and schema names;
- state and transition names;
- commands, workflows, events, errors, and status codes.

Also record contextual wording when it appears to name the same concept differently.

Build an evidence table before classifying anything:

| Exact text | Structural position | Source location | Candidate concept |
| --- | --- | --- | --- |

Rules:

- Copy the smallest useful exact fragment.
- Do not normalise or paraphrase it.
- Record repeated occurrences when they appear in different structural positions.
- Give a source location precise enough for a reader to find the wording.
- Do not infer behaviour that is absent from the source.

### Step 3 — Group wording by concept

For each concept, group all observed variants, including:

- abbreviations and expanded forms;
- singular and plural forms;
- hyphenation and capitalisation variants;
- generic and specific labels;
- near-synonyms with no shared surface wording.

Before calling something ambiguous, write down at least two plausible interpretations supported by the audited evidence.

If two plausible interpretations cannot be shown, do not classify the wording as `△` or `✕`.

#### Finding threshold

Only include a terminology finding when all of these are true:

1. You can quote the exact sentence or fragment the developer must clarify.
2. You can show at least two plausible interpretations of that wording, or two incompatible terms for the same implementation concept.
3. You can describe one concrete implementation difference those interpretations could cause.
4. The difference is material to naming, filtering, storage, states, APIs, commands, events, errors, or another implementation-facing concept.
5. The finding is not merely a style preference, harmless shorthand, grammatical variation, or wording that is already made clear by nearby context.

Do not report a finding when:

- adding or removing a word does not change any plausible implementation outcome;
- the surrounding sentence already resolves the meaning;
- the only difference is capitalization, hyphenation, singular/plural grammar, or expanded versus abbreviated form and no separate identifier family is likely;
- the interpretation requires inventing facts not present in the audited evidence;
- the issue is really missing behaviour, execution order, optionality, completeness, or implementation detail.

When authority sources also use the competing variants inconsistently, do not choose a winner. Report the undefined relationship between the terms and mark the decision unresolved.

Apply this success test to every proposed finding:

> Would a developer reading the report know exactly which sentence to clarify and why?

If the answer is no, omit the finding.

### Step 4 — Apply authority carefully

Use this authority order only when the relevant source is inside the declared audit scope:

1. Existing implementation identifiers, schemas, or public contracts.
2. Explicit definitions in the audited specification.
3. Documented product or domain vocabulary.
4. Consistent usage across the audited specification.

Never choose a preferred term for a `✕` conflict unless the report shows the authoritative evidence supporting that choice.

If the evidence proves a mismatch but does not prove which term should win:

- do not invent a preferred term;
- mark the concept as requiring stakeholder input;
- state the exact terminology decision that remains unresolved;
- omit that concept from the resolved termbase.

A mismatch proves that a decision may be needed. It does not prove which wording is correct.

### Step 5 — Classify each wording occurrence

Use these symbols:

| Symbol | Meaning |
| --- | --- |
| `●` | Preferred and unambiguous in the audited scope |
| `○` | Understandable in context, but not the supported canonical wording |
| `△` | The wording has at least two plausible interpretations |
| `✕` | The audited sources use incompatible terminology for the same implementation concept |

Tag each occurrence by spec position:

| Spec position | Meaning |
| --- | --- |
| `behavioral` | Appears in normative or executable specification text |
| `contextual` | Appears in explanatory or background text |

Do not add high, medium, low, blocking, critical, readiness, or safety ratings.

Build one settled classification table and use it as the single source for both deliverables.

### Step 6 — Build `termbase.csv`

Include only concepts for which the preferred terminology is supported by evidence.

Use these columns:

| Column | Meaning |
| --- | --- |
| `term_id` | Stable lowercase slug |
| `preferred_term` | Supported canonical label |
| `part_of_speech` | noun, verb, adjective, or proper noun |
| `definition` | One or two plain-language sentences |
| `usage_context` | Where and how the term is used |
| `forbidden_variants` | Semicolon-separated non-preferred variants |
| `source_locations` | Sources supporting the term decision |

Quote CSV fields containing commas.

Do not include:

- unresolved concepts;
- invented requirements;
- implementation proposals;
- audit commentary;
- status labels inside `preferred_term`;
- terms chosen only because they sound clearer.

An empty `forbidden_variants` field is valid.

### Step 7 — Write `terminology-audit-report.md`

Use only these sections.

#### 1. Summary

State:

- files and authority sources audited;
- number of `✕` conflicts;
- number of `△` ambiguities;
- number of unresolved terminology decisions.

Do not state or imply that the specification is:

- agent-ready or not agent-ready;
- safe or unsafe for code generation;
- complete or incomplete;
- approved or rejected;
- ready for `AGENTS.md` or any other workflow.

Do not rank findings as highest risk, high severity, medium severity, blocking, or critical.

#### 2. Evidence Table

Include the evidence table from Step 2.

#### 3. Terminology Findings

Include only `△` and `✕` findings that pass the Finding threshold. Do not list harmless `○` variations as findings. A `○` may appear only in the Settled Classification Table as supporting context.

Omit rows where every occurrence is `●` or `○`.

Use this table:

| Concept | Variants observed | Supported wording | Spec position | Locations |
| --- | --- | --- | --- | --- |

For unresolved concepts, write `Unresolved` in `Supported wording`.

Do not use headings such as `Recommendations`, `Next steps`, `Evidence-based next steps`, or `Action items`.

#### 4. Settled Classification Table

Immediately print both legends, then use these exact columns:

| Concept | Wording found in spec | Judgment | Spec position | Wording to use |
| --- | --- | --- | --- | --- |

For unresolved concepts, write `Unresolved` in `Wording to use`.

Do not use internal labels such as `Variant/card`, `Symbol`, `Severity`, or `Preferred term` as column headings.

#### 5. Why the Flagged Wording Matters

For every `△` or `✕`, include one compact teaching block:

| Field | Required content |
| --- | --- |
| `What the spec says` | The smallest exact flagged fragment |
| `Possible interpretation A` | One plausible meaning supported by the evidence |
| `Possible interpretation B` | A different plausible meaning supported by the evidence |
| `What could differ in implementation` | One concrete naming, filtering, storage, state, API, or behavioural difference |
| `Evidence` | The exact contrasting wording or authoritative source |
| `Terminology decision` | The supported wording, or the exact stakeholder choice if unresolved |

Keep each block brief and plain-language. Teach the reader why the wording matters without making predictions about overall code-generation success.

For `○` findings, a teaching block is optional. Include one only when the difference is not obvious.

#### 6. Items Needing Stakeholder Input

List only unresolved terminology choices.

For each item state:

- the competing wording;
- why authority could not be established;
- the exact naming or meaning decision required.

Write `None` when every preferred term is supported by audited evidence.

Do not include corrections, recommendations, workflow advice, or implementation suggestions in this section.

#### 7. Scope Limitation

State that the audit covers vocabulary ambiguity only and does not evaluate logical consistency, requirement completeness, technical feasibility, or implementation correctness.

## Report quality checks

Before delivery, verify all of the following:

- Every reported finding identifies the exact sentence or fragment a developer must clarify.
- Every reported finding explains why clarification is needed in plain language.
- Every `△` shows two plausible interpretations supported by audited evidence.
- Every `✕` shows incompatible terminology for one implementation concept and a concrete implementation difference.
- Harmless shorthand, grammatical variants, and nearby-context-resolved wording are omitted.
- If authority sources use competing variants inconsistently, the report does not invent a winner.
- The success test passes for every finding: a developer can identify exactly which sentence to clarify and why.
- Every selected preferred term has visible authoritative evidence.
- Every unresolved conflict appears under `Items Needing Stakeholder Input`.
- No unresolved concept appears in `termbase.csv`.
- The report and termbase use the same preferred wording.
- The report contains no readiness, safety, approval, severity-ranking, recommendation, or next-step claims.
- The report contains no out-of-scope specification findings.
- A reader can trace every finding from exact wording to classification and authority.

## Deliver

Save and return:

- `termbase.csv`
- `terminology-audit-report.md`

Deliver both even when terminology decisions remain unresolved.
