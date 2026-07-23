## Context

`.claude-plugin/marketplace.json` is the single source of truth for which
plugins in this repo are installable via `/plugin install`. It currently
lists one of three plugins. The other two (`terminology-audit`,
`vocabulary-contract`) are fully built — valid `plugin.json`, README,
skills — but silently absent from the marketplace. This was only caught by
manual inspection while working on the `markdown-ia` README; there's no
existing check that would have caught it sooner.

## Goals / Non-Goals

**Goals:**
- Every plugin under `plugins/` is registered in `marketplace.json` and
  therefore installable.
- Marketplace entry descriptions stay honest about what each plugin ships.
- A future contributor adding a fourth plugin has a documented way to check
  they haven't forgotten this step.

**Non-Goals:**
- No changes to plugin behavior, skills, or `plugin.json` version numbers.
- No CI/automation build-out — a documented manual/scriptable check is
  sufficient for a repo this size (3 plugins); a full pre-commit hook or CI
  job is more machinery than three entries warrants.
- No redesign of the marketplace.json schema itself.

## Decisions

**Source each new entry's description from the plugin's own `plugin.json`,
not re-authored from scratch.** `plugin.json` descriptions were already
written carefully (see `markdown-ia`'s, which lists all three of its
skills). Re-deriving marketplace descriptions independently risks the same
drift this change is fixing — two descriptions of the same plugin that say
different things. Copying (with light trimming if too long for a listing)
keeps one source of truth.

**Verification is a documented shell one-liner, not a script file.** Considered
adding a `scripts/check-marketplace.sh` or a CI step. Rejected for now: three
plugins is small enough that a documented `jq`/`grep` comparison a
contributor can run ad hoc is proportionate; a maintained script or CI job
is overhead for a check this cheap to redo by hand. If the plugin count
grows significantly, this should be revisited.

## Risks / Trade-offs

- **Risk**: Documented-but-manual verification gets skipped, and this drifts
  again. → **Mitigation**: The check is a single command documented in this
  change's tasks; low friction to actually run before adding a plugin.
- **Risk**: Trimming a plugin's `plugin.json` description for the
  marketplace listing introduces a new, third wording. → **Mitigation**:
  Prefer using the `plugin.json` description verbatim; only trim if it's
  clearly too long for a listing context, and keep the trim minimal.
