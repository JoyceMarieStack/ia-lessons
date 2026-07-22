# Termbase candidate proposal — round-trip scan of `test-fixtures/roundtrip/`

Scanned 3 implementation files against `test-fixtures/termbase.csv`
(8 terms, 7 approved) using the vocabulary-contract candidate scanner
(default min-count 3; a min-count 2 sweep was also run to catch borderline
phrases in this small corpus):

- `/home/user/ia-lessons/test-fixtures/roundtrip/cli.md`
- `/home/user/ia-lessons/test-fixtures/roundtrip/docs.md`
- `/home/user/ia-lessons/test-fixtures/roundtrip/pinning.py`

**Nothing was written to the termbase.** Everything below is a proposal for
human review. If your process stages adoption, add accepted entries with
status `candidate` first and promote them to `approved` in a later revision.

---

## Proposed candidates

### 1. schema pinning — strong candidate

- **Occurrences:** 6 (prose and code)
- **Surfaces seen:**
  - prose: `schema pinning`
  - code identifier (config key): `schemaPinning`
  - function name: `resolve_schema_pinning`
  - CLI flag: `--schema-pin`
  - file form: `pinning.py`
- **Example locations:**
  - `/home/user/ia-lessons/test-fixtures/roundtrip/docs.md:3` — "Schema pinning is resolved before the validation pass starts. When a project"
  - `/home/user/ia-lessons/test-fixtures/roundtrip/pinning.py:3` — "Schema pinning locks a project to a specific base schema version so registry"
  - `/home/user/ia-lessons/test-fixtures/roundtrip/pinning.py:10` — `pin = config.get("schemaPinning")`
- **Suggested definition (inferred from usage):** Locking a project to a
  specific base schema version so that schema registry updates cannot change
  validation results between runs. Resolved before the validation pass starts;
  when a version is pinned, the loader skips registry lookups for that base
  schema.
- **Suggested termbase row:**

  | column | value |
  |---|---|
  | term | `schema pinning` |
  | code_identifier | `schemaPinning` |
  | cli_flag | `--schema-pin` |
  | definition | as above |
  | status | `candidate` |

- **Note:** the related noun phrase **"pinned version"** (2 occurrences:
  `cli.md:3`, `pinning.py:9`) is the value produced by schema pinning. It is
  probably covered by this entry's definition rather than needing its own row,
  but is listed here so a reviewer can decide.

### 2. base schema — low-confidence candidate (possible pre-existing gap)

- **Occurrences:** 2 in the scanned files (`docs.md:4` — "pins a version, the
  loader skips registry lookups for that base schema."; `pinning.py:3`), below
  the default threshold.
- **Why flagged anyway:** the existing termbase already *uses* "base schema"
  in the definitions of `extend mode` and `schema registry`, yet has no row
  for it. The implementation now also uses it in prose and docstrings. This is
  not new drift introduced by this change, but if the concept matters enough
  to define other terms with, the next revision may want to name it
  explicitly.
- **Suggested definition (inferred):** The versioned schema served by the
  schema registry that project-local schemas extend or pin.

---

## Discarded shortlist entries (with reasons)

- `resolve schema pinning` (2) — fragment produced by splitting the function
  name `resolve_schema_pinning`; not an independent concept, covered by the
  schema pinning entry.

## Other observations (single occurrences, not proposed)

- **rollback window** (`docs.md:6`) — "A rollback window was discussed for
  failed pins but rejected for this release." Explicitly a rejected concept;
  not proposed, noted only so the vocabulary owner knows the phrase exists in
  the docs.
- **audit trail** (`cli.md:3-4`) — single mention referencing the operations
  guide; generic operations vocabulary at this frequency, not proposed.
- **Near-synonym check:** no shortlisted phrase looks like a near-synonym of
  an existing approved term (e.g. nothing competing with `merge policy`,
  `schema registry`, etc.), so no drift call-outs.

---

## Summary

1 strong candidate (**schema pinning**) and 1 low-confidence candidate
(**base schema**) proposed from 3 files. The termbase was not modified.
