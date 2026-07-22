## Vocabulary

The terms below are a binding naming contract (source: test-fixtures/termbase.csv,
7 approved terms). Use the canonical form in prose; use the listed surface
forms in code, file names, flags, and environment variables. Do not coin
synonyms for these concepts.

### extend mode

Always write "extend mode" when referring to the mode in which a project-local
schema extends the base schema instead of replacing it. Never write "extension
mode" or "inherit mode".
In code, use the identifier `extendMode`; in file names, `extend-mode`; as a
CLI flag, `--extend-mode`; as an environment variable, `EXTEND_MODE`. Do not
use these surface forms in running prose — prose always says "extend mode".
<!-- source: termbase.csv row 2 -->

### project-local schema

Always write "project-local schema" when referring to a schema defined inside
a project directory that applies only to that project. Never write "local
schema", "local schema override", or "project schema".
In code, use the identifier `projectLocalSchema`. Do not use this surface form
in running prose — prose always says "project-local schema".
<!-- source: termbase.csv row 3 -->

### config.yaml

Always write "config.yaml" when referring to the single configuration file
read at startup from the project root. Never write "config.yml" or
"configuration file".
In file names, use `config.yaml`. Do not use this surface form in running
prose — prose always says "config.yaml".
<!-- source: termbase.csv row 4 -->

### schema registry

Always write "schema registry" when referring to the service that stores and
serves versioned base schemas. Never write "registry service" or "schema
store".
In code, use the identifier `SchemaRegistry`. Do not use this surface form in
running prose — prose always says "schema registry".
<!-- source: termbase.csv row 5 -->

### merge policy

Always write "merge policy" when referring to the rule set that decides how
project-local values combine with base values. Never write "merge strategy" or
"combine policy".
In code, use the identifier `mergePolicy`; as a CLI flag, `--merge-policy`; as
an environment variable, `MERGE_POLICY`. Do not use these surface forms in
running prose — prose always says "merge policy".
<!-- source: termbase.csv row 6 -->

### validation pass

Always write "validation pass" when referring to a single end-to-end run of
schema validation over a project.
<!-- source: termbase.csv row 7 -->

### spec preamble

Always write "spec preamble" when referring to the vocabulary block pasted at
the top of a spec or proposal document.
<!-- source: termbase.csv row 8 -->

**Pending terms** (not yet binding): draft proposal (candidate).
