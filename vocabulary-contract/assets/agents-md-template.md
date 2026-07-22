# Template: rendered vocabulary fragment

Two sections: the full AGENTS.md / CLAUDE.md fragment, then the compact spec
preamble. Replace the bracketed slots; follow the prose style of the worked
example exactly. Rules that matter:

- Imperative prose, one block per term. No tables — agents follow prose better.
- Include a transform surface (code / file / CLI / env) **only if the termbase
  row declares it**. Never invent transforms.
- Fold the definition into the "Always write..." sentence when present; if
  there is no definition, anchor the sentence on the term alone.
- Every entry ends with an HTML comment citing the source row.

## Section 1: AGENTS.md / CLAUDE.md fragment

```markdown
## Vocabulary

The terms below are a binding naming contract (source: [termbase path],
[N] approved terms). Use the canonical form in prose; use the listed surface
forms in code, file names, flags, and environment variables. Do not coin
synonyms for these concepts.

### [term]

Always write "[term]" when referring to [definition, rephrased as a clause].
Never write [quoted banned variants, comma-separated, e.g. "extension mode" or
"inherit mode"].
In code, use the identifier `[code_identifier]`; in file names, `[file_form]`;
as a CLI flag, `[cli_flag]`; as an environment variable, `[env_var]`. Do not
use these surface forms in running prose — prose always says "[term]".
<!-- source: [termbase filename] row [row], term_id: [term_id] -->

### [term with no variants or transforms]

Always write "[term]" when referring to [definition clause].
<!-- source: [termbase filename] row [row], term_id: [term_id] -->

[Optional, only if non-approved rows exist:]
**Pending terms** (not yet binding): [term] ([status]), [term] ([status]).
```

Worked example entry:

```markdown
### extend mode

Always write "extend mode" when referring to the mode in which a project-local
schema extends the base schema instead of replacing it. Never write "extension
mode" or "inherit mode".
In code, use the identifier `extendMode`; in file names, `extend-mode`; as a
CLI flag, `--extend-mode`; as an environment variable, `EXTEND_MODE`. Do not
use these surface forms in running prose — prose always says "extend mode".
<!-- source: termbase.csv row 2, term_id: extend-mode -->
```

Notes:

- Drop each surface clause that has no value in the row; if a row declares no
  surfaces at all, drop the whole "In code, ..." sentence.
- If a row has no banned variants, drop the "Never write ..." sentence.
- Keep entries in termbase row order so diffs against re-renders stay readable.

## Section 2: compact spec preamble

One line per approved term, for pasting at the top of a spec or proposal:

```markdown
<!-- vocabulary contract: [termbase path], [N] approved terms, rendered [date] -->
> **Vocabulary.** This document uses the following canonical terms:
> **[term]** (not [variant]; code: `[code_identifier]`) — [definition].
> **[term]** — [definition].
```

Same omission rules apply: no invented surfaces, no invented definitions.
