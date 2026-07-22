# Terminology Check: test-fixtures/enforce-edge/spec.md

- **Termbase:** `test-fixtures/termbase.csv` — 8 rows, 7 approved terms enforced.
  All columns mapped exactly (`term`, `variants`, `code_identifier`, `file_form`,
  `cli_flag`, `env_var`, `definition`, `status`); no unmapped columns.
- **Files checked:** `test-fixtures/enforce-edge/spec.md`
- **Mode:** enforce (advisory — no edits applied to the spec)

## Findings

### extend mode (termbase row 2)

**1. Surface mismatch — `extend-mode` used in running prose**

- **File / line:** `test-fixtures/enforce-edge/spec.md`, line 5
- **Quoted line:**
  > When extend-mode is active, the loader keeps base keys that the project-local
- **Found:** `extend-mode` (the kebab-case file/flag surface form) in prose, outside backticks
- **Canonical term:** `extend mode`
- **Suggested rewrite:**
  > When extend mode is active, the loader keeps base keys that the project-local schema does not override.

  The sentence refers to the mode as a concept, not to a literal flag or file
  name, so the prose form "extend mode" is the right fix. (If the author truly
  meant the CLI flag, the alternative fix would be backticks: `--extend-mode`.)

## Correct usages worth noting (not violations)

- Line 11: `extendMode` inside the js code fence — matches the term's declared
  code identifier; canonical surface form in code context, correctly not flagged.
- Line 16: `--extend-mode` in inline backticks — matches the declared CLI flag;
  code context, correctly not flagged.
- Lines 5–6: "project-local schema" (spanning the line break) uses the
  canonical prose form for termbase row 3.

## Summary

Checked 1 file against 7 approved terms: **1 violation found** (1 surface
mismatch for "extend mode"; 0 banned-variant hits). Skipped as non-approved:
"draft proposal" (status `candidate` — context only, not enforced).
