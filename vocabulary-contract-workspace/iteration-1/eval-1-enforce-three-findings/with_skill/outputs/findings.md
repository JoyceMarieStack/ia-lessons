# Terminology Findings: test-fixtures/enforce/spec.md

Checked against `test-fixtures/termbase.csv` (8 terms; 7 approved and enforced,
1 candidate skipped). Column mapping was one-to-one with the expected headers
(`term`, `variants`, `code_identifier`, `file_form`, `cli_flag`, `env_var`,
`definition`, `status`) — no remapping was needed.

These findings are advisory; no edits have been made to the spec.

## Findings by term

### extend mode (termbase row 2) — 2 occurrences of banned variant "extension mode"

1. **test-fixtures/enforce/spec.md:5** — variant `extension mode`, canonical: **extend mode**

   > When a project defines its own schema, the loader runs in extension mode and

   Suggested rewrite:

   > When a project defines its own schema, the loader runs in extend mode and

2. **test-fixtures/enforce/spec.md:14** — variant `extension mode`, canonical: **extend mode**

   > - FR-003: Switching to extension mode MUST NOT change the merge policy.

   Suggested rewrite:

   > - FR-003: Switching to extend mode MUST NOT change the merge policy.

### project-local schema (termbase row 3) — 1 occurrence of banned variant "local schema override"

1. **test-fixtures/enforce/spec.md:12** — variant `local schema override`, canonical: **project-local schema**

   > - FR-002: If a local schema override is present, it is applied after the base

   Suggested rewrite:

   > - FR-002: If a project-local schema is present, it is applied after the base

## Correct usage observed

The spec already uses the approved forms `schema registry` (line 6),
`config.yaml` (line 10, correctly in backticks), `validation pass` (line 11),
and `merge policy` (line 14) — no drift for those terms.

## Non-enforced terms

- **draft proposal** (termbase row 9, status `candidate`) was skipped — only
  `approved` terms are enforced. Note that line 18 ("This began as a proposal
  draft...") uses its listed variant `proposal draft`; if this term is later
  approved, that line would become a finding. Not counted as a violation now.

## Summary

3 findings across 1 file, checked against 7 approved terms: **extend mode** (2),
**project-local schema** (1). Skipped as non-approved: draft proposal.
