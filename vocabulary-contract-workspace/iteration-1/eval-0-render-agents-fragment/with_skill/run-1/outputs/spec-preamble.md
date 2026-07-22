<!-- vocabulary contract: test-fixtures/termbase.csv, 7 approved terms, rendered 2026-07-22 -->
> **Vocabulary.** This document uses the following canonical terms:
> **extend mode** (not extension mode, inherit mode; code: `extendMode`) — the mode in which a project-local schema extends the base schema instead of replacing it.
> **project-local schema** (not local schema, local schema override, project schema; code: `projectLocalSchema`) — a schema defined inside a project directory that applies only to that project.
> **config.yaml** (not config.yml, configuration file) — the single configuration file read at startup from the project root.
> **schema registry** (not registry service, schema store; code: `SchemaRegistry`) — the service that stores and serves versioned base schemas.
> **merge policy** (not merge strategy, combine policy; code: `mergePolicy`) — the rule set that decides how project-local values combine with base values.
> **validation pass** — a single end-to-end run of schema validation over a project.
> **spec preamble** — the vocabulary block pasted at the top of a spec or proposal document.
