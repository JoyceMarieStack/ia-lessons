---
name: sdd-terminology-audit
description: Audit implementation-facing specifications and requirements for terminology ambiguity that could cause developers or coding agents to interpret the same concept differently, and notify spec writers with lint-style ambiguity alerts that point at the exact sentence to fix. Use for SDD specs (spec-kit, OpenSpec, or similar), requirement files, Given/When/Then scenarios, MUST/SHALL statements, schemas, interfaces, commands, states, events, errors, and field names — especially as a pre-flight check before a spec is handed to a coding agent for planning or generation. Also use for whole OpenSpec change folders (proposal.md, design.md, delta specs with ADDED/MODIFIED/REMOVED requirements, tasks.md), where it additionally checks terminology drift across the artifact chain. Produce an evidence-backed Markdown report led by an Ambiguity Alerts block, a CSV termbase, and a machine-readable ambiguity-alerts.csv. Do not use for general prose editing, completeness review, readiness assessment, or broad logical-consistency review.
---

# SDD Terminology Audit

Audit only vocabulary ambiguity in implementation-facing specifications.

The goal is practical:

> A developer reading the report must know exactly which sentence to clarify and why — without reading the whole report first.

That second clause is why this skill produces alerts, not just analysis. A
spec writer is "notified" only if the finding reaches them in a form they
can act on in seconds: a location they can jump to, a quoted fragment, and
the exact decision needed. Everything else in the report exists to back
those alerts with evidence.

Produce:

- `terminology-audit-report.md` — led by an Ambiguity Alerts block
- `termbase.csv` — resolved vocabulary, ready to feed into agent context
- `ambiguity-alerts.csv` — machine-readable alerts for hooks, CI, or an agent harness

Do not execute code. Inspect only files explicitly included in the audit scope.

## 1. The ambiguity model

This skill applies controlled-vocabulary analysis from information
architecture. The foundational distinction: **a concept and the word used
for it are not the same thing.** Every finding is one of three ways that
mapping breaks in a spec.

| Rule | Plain name | IA name | Symbol | What broke |
| --- | --- | --- | --- | --- |
| `AMB-SYN` | Two words for one thing | Synonym conflict (synonymy) | `✕` | The audited sources use competing terms for the same implementation concept, so a generated codebase can grow two names — or two entities — for one thing. |
| `AMB-POLY` | One word, two meanings | Homograph collision (polysemy) | `△` | A single wording has two evidence-supported meanings, so the agent must guess which one a given sentence intends. |
| `AMB-SCENT` | Shorthand with two possible referents | Scent failure | `△` | A subtype of polysemy: an abbreviation or unexpanded term of art appears in normative text, and the audited scope supports two different expansions or referents. The reader arriving at that sentence has no trail to follow. |

The codes exist for machines — grep, CI annotations,
`ambiguity-alerts.csv`. The plain names exist for developers. Never
print a bare code in the report: pair every code with its plain name, as
in `AMB-POLY (one word, two meanings)`, so a reader who has never seen
this skill can act on a finding without consulting a legend.

Why the distinction matters: the two main failures need opposite fixes.
A synonym conflict is fixed by **picking one preferred term** and demoting
the variants. A homograph collision cannot be fixed by picking a winner —
it is fixed by **renaming or qualifying one of the meanings** so the word
stops doing double duty. Conflating them sends the spec writer down the
wrong repair.

Two traps that look like findings but are not:

- **False synonyms.** Two near-synonymous words that the spec uses for
  genuinely different concepts (e.g., *cancel* a queued run vs. *kill* a
  running process) are correct domain modeling, not drift. Merging them
  would introduce the very ambiguity this audit exists to remove.
- **Intentional register variation.** A user-facing label and an internal
  identifier for the same object are sometimes correctly different. Flag a
  register pair only when the spec crosses the registers in a way that
  could change an implementation-facing name or value.

### Facets

Tag every finding with the kind of thing the ambiguous concept is:

`object` · `field` · `state` · `command` · `event` · `error` · `actor` · `value` · `artifact`

This is lightweight faceted classification, and it earns its place as a
diagnostic: when findings cluster in one facet (three of four findings are
state names), the cluster — not the individual findings — is the real
signal about where the spec needs a definitions pass.

### Multi-artifact scopes (OpenSpec change folders)

When the audit scope is an OpenSpec change folder
(`openspec/changes/<id>/` — `proposal.md`, `design.md`, delta specs,
`tasks.md`) or any chain of upstream/downstream artifacts for one
change, read `references/openspec-change-audit.md` before extracting
evidence. It adds the chain model (anchor each alert at the earliest
artifact where the term enters), a replacement authority order,
per-artifact priorities and traps, and a fourth rule that only exists in
multi-artifact audits: `AMB-GHOST` (a name nothing establishes, symbol
`?`) — for a task or design sentence that uses a name no upstream
artifact or inspected source defines, so every implementation of that
line is a guess.

## 2. Scope boundary

A terminology finding exists only when wording can materially change an
implementation-facing concept such as a name, field, filter, file set,
state, command, event, error, API, or stored value.

Do not report:

- style preferences;
- harmless shorthand (an abbreviated form after a qualified first use);
- capitalization, hyphenation, or grammatical variation by itself;
- missing execution order;
- missing optional-versus-required behavior;
- missing inputs or outputs;
- incomplete acceptance criteria;
- unstated implementation details;
- logical contradictions that use consistent vocabulary;
- general writing quality issues.

Omit out-of-scope observations entirely. The alerts block only works as a
notification channel if every line in it is real — one padded alert
teaches the spec writer to skim past all of them.

## 3. Inventory the audit scope

List:

- every specification file audited;
- every additional authority source inspected.

Authority sources may include implementation identifiers, schemas,
interface contracts, published APIs, repository conventions, or documented
stakeholder decisions.

Do not claim authority from a source that was not inspected.

## 4. Extract exact evidence

Copy the smallest useful exact fragments from the specification and
authority sources.

Use this evidence table:

| Exact text | Anchor | Source location | Candidate concept |
| --- | --- | --- | --- |

**Anchor** is the nearest addressable structural position: a requirement
ID (`FR-003`), scenario ID (`AS1`), or heading. Record it during
extraction — alerts reuse it verbatim, and an alert without a jumpable
anchor is not a notification, it is homework.

Prioritize wording in:

- Given/When/Then steps;
- MUST, SHALL, and MUST NOT statements;
- preconditions, postconditions, and invariants;
- fields, parameters, schemas, and interfaces;
- states, transitions, commands, workflows, events, errors, and status codes.

Do not normalize, paraphrase, or infer missing behavior while collecting
evidence.

## 5. Mandatory finding gate

Apply this gate before adding any `△` or `✕` finding. (`?` findings, which
have zero referents rather than two, use the adapted gate in
`references/openspec-change-audit.md`.)

A finding is allowed only when every answer below is **yes**:

1. Can you quote the exact sentence or fragment the developer must clarify?
2. Can you show two meanings or competing terms supported by the audited evidence?
3. Would those alternatives produce a materially different implementation-facing result?
4. Does nearby context fail to resolve the difference?
5. Is the issue genuinely vocabulary ambiguity rather than missing behavior or detail?

If any answer is **no**, omit the finding.

For every proposed finding, write this internal check before classification:

- **Sentence to clarify:** exact wording.
- **Rule:** `AMB-SYN`, `AMB-POLY`, or `AMB-SCENT`.
- **Facet:** one facet from the list above.
- **Interpretation A:** evidence-supported meaning.
- **Interpretation B:** evidence-supported different meaning.
- **Implementation difference:** exact name, filter, file set, field, state, API, command, event, error, or stored value that could differ.
- **Nearby-context check:** why surrounding text does not already settle the meaning.

Do not include this internal check in the final report unless the finding passes.

### Automatic rejection rules

Reject the finding when:

- one interpretation depends on invented facts;
- the difference would not change implementation;
- the surrounding sentence names the precise concept already;
- authority sources use the supposedly non-preferred term for the same concept;
- the issue is only that one phrase is more precise or elegant;
- the pair is a false synonym — the spec consistently uses the two words for two different concepts;
- the variation is intentional register difference that never crosses into an implementation-facing name or value;
- a developer would not know which exact sentence to edit.

## 6. Authority and unresolved decisions

Use authority only from inspected sources, in this order:

1. Existing implementation identifiers, schemas, and public contracts.
2. Explicit definitions in the audited specification.
3. Documented product or domain vocabulary.
4. Consistent usage across the audited specification.

Choose supported wording only when the evidence clearly establishes it.

If authority sources use competing variants inconsistently:

- do not choose a winner;
- describe the relationship between the terms as undefined;
- mark the terminology decision unresolved;
- omit the concept from `termbase.csv`;
- carry it as an unresolved alert and list the exact choice under `Items Needing Stakeholder Input`.

A mismatch proves that clarification may be needed. It does not prove
which wording is correct.

## 7. Classification

Use:

| Symbol | Rule | Meaning |
| --- | --- | --- |
| `●` | — | Supported and unambiguous in the audited scope |
| `○` | — | Understandable variation that does not create a material implementation ambiguity |
| `△` | `AMB-POLY` / `AMB-SCENT` | One wording has two evidence-supported meanings that could change implementation |
| `✕` | `AMB-SYN` | Audited sources use incompatible terms for the same implementation concept |
| `?` | `AMB-GHOST` | A name is used as if established, but no audited artifact or inspected source defines a referent (multi-artifact audits only — see `references/openspec-change-audit.md`) |

Use `behavioral` for normative or executable specification text and
`contextual` for supporting prose.

Do not add severity, risk, readiness, safety, approval, or blocking labels.

`○` rows are supporting context only. Never include them in `Terminology
Findings` or in alerts.

## 8. Build `termbase.csv`

Include only resolved concepts with evidence-supported wording.

Use these columns:

| Column | Meaning |
| --- | --- |
| `term_id` | Stable lowercase slug |
| `preferred_term` | Evidence-supported canonical label |
| `part_of_speech` | noun, verb, adjective, or proper noun |
| `definition` | One or two plain-language sentences |
| `usage_context` | Where and how the term is used |
| `forbidden_variants` | Semicolon-separated non-preferred variants |
| `source_locations` | Evidence supporting the decision |

Do not include unresolved concepts, recommendations, proposed behavior, or
terms chosen only because they sound clearer. Unresolved concepts live in
`ambiguity-alerts.csv` instead — the termbase is the resolved vocabulary a
team can drop into an agent's context as a naming constraint, and one
guessed row poisons that use.

## 9. Build `ambiguity-alerts.csv`

One row per passed finding — this is the artifact a pre-commit hook, CI
step, or agent harness reads to notify the spec writer without parsing
prose.

Use these columns:

| Column | Meaning |
| --- | --- |
| `alert_id` | Stable lowercase slug |
| `rule` | `AMB-SYN`, `AMB-POLY`, `AMB-SCENT`, or `AMB-GHOST` (multi-artifact audits only) |
| `facet` | One facet from section 1 |
| `file` | Spec file the sentence lives in |
| `anchor` | Requirement ID, scenario ID, or heading nearest the sentence |
| `quoted_text` | Exact fragment to clarify |
| `meaning_a` | First evidence-supported meaning or variant |
| `meaning_b` | Second evidence-supported meaning or variant |
| `supported_wording` | Evidence-supported wording, or `unresolved` |
| `decision_needed` | The exact question the spec writer must answer, phrased so editing the spec answers it |

If no finding passed the gate, write the header row only.

Quote any field containing a comma (standard CSV double-quoting).

## 10. Write `terminology-audit-report.md`

Use exactly these sections.

### 1. Ambiguity Alerts

The notification block. One alert per passed finding, most consequential
first, in this format:

```
✕ "task" vs "job" — two words for one thing (AMB-SYN)
  spec.md › AS1 — "submits a task, Then the task appears in the job queue"
  AS1 and Edge Cases say "task"; all seven FRs say "job" — both name the schedulable unit.
  Decide: confirm "job" and replace "task" in AS1 and Edge Cases, or define "task" as a distinct concept.
```

The first line is the triage line: symbol, the disputed wording in
quotes (for `AMB-SYN`, the competing pair), then the plain rule name
with the code in parentheses. Lead with the wording, not the code — the
first thing a developer scans for is *which word* is the problem. Follow
with the location (file `›` anchor) and quoted fragment, one sentence
stating the two meanings or competing terms, and a `Decide:` line with
the exact question to answer. Four short lines maximum per alert — the
block must be triageable without reading the rest of the report.

Do not put a facet on the alert lines. A bare facet in parentheses reads
as if it named the ambiguous word; facets belong in the findings table,
`ambiguity-alerts.csv`, and the closing rollup.

Close the block with a rollup written in plain words that names its
facets in parentheses — e.g., `Both findings are names for files and
documents (facet: artifact).` — and, only when one facet dominates, one
sentence naming the cluster.

If nothing passed the gate, write `No ambiguity alerts.` and nothing else
in this section.

### 2. Summary

State only:

- files audited;
- authority sources inspected;
- number of `✕` findings (`AMB-SYN`, two words for one thing);
- number of `△` findings (`AMB-POLY` / `AMB-SCENT`, one word or shorthand with two meanings);
- number of unresolved terminology decisions.

Do not make readiness, safety, completeness, approval, severity, or
workflow claims.

### 3. Evidence Table

Include the evidence table.

### 4. Terminology Findings

Include only findings that passed the Mandatory finding gate.

Use:

| Sentence to clarify | Concept | Rule | Facet | Variants or meanings | Judgment | Supported wording |
| --- | --- | --- | --- | --- | --- | --- |

For unresolved findings, write `Unresolved` in `Supported wording`.

Do not include `●` or `○` rows here.

### 5. Why Each Finding Matters

For every finding, use one compact block:

| Field | Content |
| --- | --- |
| `Sentence to clarify` | Exact sentence or fragment |
| `Interpretation A` | Evidence-supported meaning |
| `Interpretation B` | Different evidence-supported meaning |
| `What could differ` | Concrete implementation-facing difference |
| `Why context does not settle it` | Brief explanation |
| `Evidence` | Exact contrasting wording or authority source |
| `Terminology decision` | Supported wording or exact unresolved choice |

Do not invent hypothetical implementations that are not grounded in the
audited evidence.

### 6. Settled Classification Table

Print the symbol and spec-position legends first.

Use:

| Concept | Wording found | Judgment | Spec position | Wording to use |
| --- | --- | --- | --- | --- |

Include `●` and `○` rows only when they help explain a reported `△` or
`✕` finding. Do not fill this table with unrelated approved terminology.

For unresolved concepts, write `Unresolved` in `Wording to use`.

### 7. Items Needing Stakeholder Input

List only unresolved terminology choices.

For each, state:

- the exact sentence to clarify;
- the competing terms or meanings;
- why audited authority does not settle the choice;
- the exact decision required.

Write `None` when no terminology decision is unresolved.

### 8. Scope Limitation

State that the audit covers vocabulary ambiguity only and does not
evaluate logical consistency, requirement completeness, technical
feasibility, or implementation correctness.

Do not include recommendations, next steps, action items, readiness
claims, or workflow advice anywhere in the report.

## 11. Final quality check

Before delivery, remove any finding that fails even one check:

- The exact sentence to clarify is visible.
- Two alternatives are supported by evidence.
- The alternatives cause a concrete implementation-facing difference.
- Nearby context does not settle the meaning.
- The issue is terminology, not missing behavior.
- The rule code matches the failure (competing terms → `AMB-SYN`; one wording, two meanings → `AMB-POLY`/`AMB-SCENT`).
- Authority is visible for every selected term.
- Inconsistent authority results in `unresolved`, not an invented winner.
- A developer can immediately answer: "Which sentence do I edit, and why?"

Then check the deliverables agree:

- Every passed finding appears exactly once in the Ambiguity Alerts block and exactly once in `ambiguity-alerts.csv`, and the counts match the Summary.
- Every alert's first line leads with the disputed wording itself, not a code or a facet.
- Every rule code printed in the report is paired with its plain name; no bare codes anywhere.
- Every alert's anchor exists in the audited file.
- Every `Decide:` clause is a question a stakeholder can answer by editing the spec.

If no finding passes, report zero findings. A short report with zero
findings is better than weak findings — and an empty alerts block a
writer can trust is worth more than a full one they learn to ignore.

## Deliver

Return:

- `terminology-audit-report.md`
- `termbase.csv`
- `ambiguity-alerts.csv`
