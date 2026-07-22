---
name: sdd-terminology-audit
description: Audit implementation-facing specifications and requirements for terminology ambiguity that could cause developers or coding agents to interpret the same concept differently. Use for SDD specs, requirement files, Given/When/Then scenarios, MUST/SHALL statements, schemas, interfaces, commands, states, events, errors, and field names. Produce an evidence-backed Markdown report and CSV termbase. Do not use for general prose editing, completeness review, readiness assessment, or broad logical-consistency review.
---

# SDD Terminology Audit

Audit only vocabulary ambiguity in implementation-facing specifications.

The goal is practical:

> A developer reading the report must know exactly which sentence to clarify and why.

Produce:

- `terminology-audit-report.md`
- `termbase.csv`

Do not execute code. Inspect only files explicitly included in the audit scope.

## 1. Scope boundary

A terminology finding exists only when wording can materially change an implementation-facing concept such as a name, field, filter, file set, state, command, event, error, API, or stored value.

Do not report:

- style preferences;
- harmless shorthand;
- capitalization, hyphenation, or grammatical variation by itself;
- missing execution order;
- missing optional-versus-required behavior;
- missing inputs or outputs;
- incomplete acceptance criteria;
- unstated implementation details;
- logical contradictions that use consistent vocabulary;
- general writing quality issues.

Omit out-of-scope observations entirely.

## 2. Inventory the audit scope

List:

- every specification file audited;
- every additional authority source inspected.

Authority sources may include implementation identifiers, schemas, interface contracts, published APIs, repository conventions, or documented stakeholder decisions.

Do not claim authority from a source that was not inspected.

## 3. Extract exact evidence

Copy the smallest useful exact fragments from the specification and authority sources.

Use this evidence table:

| Exact text | Structural position | Source location | Candidate concept |
| --- | --- | --- | --- |

Prioritize wording in:

- Given/When/Then steps;
- MUST, SHALL, and MUST NOT statements;
- preconditions, postconditions, and invariants;
- fields, parameters, schemas, and interfaces;
- states, transitions, commands, workflows, events, errors, and status codes.

Do not normalize, paraphrase, or infer missing behavior while collecting evidence.

## 4. Mandatory finding gate

Apply this gate before adding any `△` or `✕` finding.

A finding is allowed only when every answer below is **yes**:

1. Can you quote the exact sentence or fragment the developer must clarify?
2. Can you show two meanings or competing terms supported by the audited evidence?
3. Would those alternatives produce a materially different implementation-facing result?
4. Does nearby context fail to resolve the difference?
5. Is the issue genuinely vocabulary ambiguity rather than missing behavior or detail?

If any answer is **no**, omit the finding.

For every proposed finding, write this internal check before classification:

- **Sentence to clarify:** exact wording.
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
- a developer would not know which exact sentence to edit.

## 5. Authority and unresolved decisions

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
- list the exact choice under `Items Needing Stakeholder Input`.

A mismatch proves that clarification may be needed. It does not prove which wording is correct.

## 6. Classification

Use:

| Symbol | Meaning |
| --- | --- |
| `●` | Supported and unambiguous in the audited scope |
| `○` | Understandable variation that does not create a material implementation ambiguity |
| `△` | One wording has two evidence-supported meanings that could change implementation |
| `✕` | Audited sources use incompatible terms for the same implementation concept |

Use `behavioral` for normative or executable specification text and `contextual` for supporting prose.

Do not add severity, risk, readiness, safety, approval, or blocking labels.

`○` rows are supporting context only. Never include them in `Terminology Findings`.

## 7. Build `termbase.csv`

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

Do not include unresolved concepts, recommendations, proposed behavior, or terms chosen only because they sound clearer.

## 8. Write `terminology-audit-report.md`

Use exactly these sections.

### 1. Summary

State only:

- files audited;
- authority sources inspected;
- number of `✕` findings;
- number of `△` findings;
- number of unresolved terminology decisions.

Do not make readiness, safety, completeness, approval, severity, or workflow claims.

### 2. Evidence Table

Include the evidence table.

### 3. Terminology Findings

Include only findings that passed the Mandatory finding gate.

Use:

| Sentence to clarify | Concept | Variants or meanings | Judgment | Supported wording |
| --- | --- | --- | --- | --- |

For unresolved findings, write `Unresolved` in `Supported wording`.

Do not include `●` or `○` rows here.

### 4. Why Each Finding Matters

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

Do not invent hypothetical implementations that are not grounded in the audited evidence.

### 5. Settled Classification Table

Print the symbol and spec-position legends first.

Use:

| Concept | Wording found | Judgment | Spec position | Wording to use |
| --- | --- | --- | --- | --- |

Include `●` and `○` rows only when they help explain a reported `△` or `✕` finding. Do not fill this table with unrelated approved terminology.

For unresolved concepts, write `Unresolved` in `Wording to use`.

### 6. Items Needing Stakeholder Input

List only unresolved terminology choices.

For each, state:

- the exact sentence to clarify;
- the competing terms or meanings;
- why audited authority does not settle the choice;
- the exact decision required.

Write `None` when no terminology decision is unresolved.

### 7. Scope Limitation

State that the audit covers vocabulary ambiguity only and does not evaluate logical consistency, requirement completeness, technical feasibility, or implementation correctness.

Do not include recommendations, next steps, action items, readiness claims, or workflow advice anywhere in the report.

## 9. Final quality check

Before delivery, remove any finding that fails even one check:

- The exact sentence to clarify is visible.
- Two alternatives are supported by evidence.
- The alternatives cause a concrete implementation-facing difference.
- Nearby context does not settle the meaning.
- The issue is terminology, not missing behavior.
- Authority is visible for every selected term.
- Inconsistent authority results in `Unresolved`, not an invented winner.
- A developer can immediately answer: “Which sentence do I edit, and why?”

If no finding passes, report zero findings. A short report with zero findings is better than weak findings.

## Deliver

Return:

- `terminology-audit-report.md`
- `termbase.csv`
