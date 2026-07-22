# Terminology Enforcement Report

- **Checked document:** `test-fixtures/clean/spec.md`
- **Termbase:** `test-fixtures/termbase.csv` (8 rows; 7 approved terms enforced)
- **Date:** 2026-07-22

## Termbase load

Column mapping was clean — all headers matched the expected schema directly
(`term`, `variants`, `code_identifier`, `file_form`, `cli_flag`, `env_var`,
`definition`, `status`); no unmapped columns.

Terms enforced (status `approved`): **extend mode**, **project-local schema**,
**config.yaml**, **schema registry**, **merge policy**, **validation pass**,
**spec preamble**.

Skipped as non-approved: **draft proposal** (status `candidate` — context only,
not part of the contract).

## Findings

**Checked 1 file against 7 approved terms: no violations found.**

No banned variants (prose or code-shaped forms) and no surface mismatches
(code/file/flag/env forms used in running prose) were detected. Notably, the
spec uses the canonical forms correctly throughout:

| Line | Canonical usage observed |
|------|--------------------------|
| 5 | "schema registry", "extend mode" |
| 6 | "project-local schema", "merge policy" |
| 11 | `config.yaml` (correctly in backticks as the file form) |
| 12 | "validation pass" |

## Summary

- Total findings: **0**
- Files scanned: 1
- Approved terms enforced: 7
- Terms skipped as non-approved: 1 (`draft proposal`, candidate)

This report is advisory. No files were modified and the termbase was not
changed.
