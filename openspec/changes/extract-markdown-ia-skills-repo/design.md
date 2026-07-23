## Context

`ia-lessons` currently hosts three independent plugins under `plugins/`:
`markdown-ia`, `terminology-audit`, `vocabulary-contract`. Of the three,
only `markdown-ia` has zero dependency on the other two — it doesn't
consume a `termbase.csv`, doesn't feed `vocabulary-contract`, and its
own evals fixture is "scan this repo," not a shared `examples/` dataset.
`terminology-audit` and `vocabulary-contract` form a real pipeline
(termbase → naming contract) and share `examples/sample-dataset/` and
`examples/sample-sdd-dataset/` as fixtures — those two stay together.

The user has decided: **move** (not copy) markdown-ia out of `ia-lessons`,
**fresh start** (no git history carried over), **prepare locally only**
(no `gh repo create` / push — that's a manual follow-up). `examples/sample-reports/argo-cd/`
moves with it (markdown-ia's own worked output); `examples/sample-dataset/`
stays in `ia-lessons` (confirmed as terminology-audit's fixture, unrelated
to markdown-ia).

## Goals / Non-Goals

**Goals:**
- `markdown-ia-skills` is a new, self-contained local git repo, structured
  so it can itself be added as a Claude Code plugin marketplace source —
  both `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`
  at repo root (not nested under `plugins/`), the latter scoped to just
  this one plugin — once pushed to GitHub.
- `ia-lessons` no longer references or ships markdown-ia in any form —
  no dangling links, no stale marketplace entry, no broken README
  cross-references.
- The evals self-scan fixture is re-verified (not just copied blindly)
  against the new repo's actual shape, since the old assertions were
  written assuming a multi-plugin `ia-lessons`-sized corpus.

**Non-Goals:**
- Creating the GitHub repo or pushing — explicitly a manual follow-up per
  the user's answer.
- Preserving git history/blame for the extracted files — explicitly a
  fresh start per the user's answer.
- Changing the three skills' behavior, SKILL.md content, or scope in any
  way — this is a relocation, not a rewrite.
- Re-adding markdown-ia to `ia-lessons`'s marketplace.json pointing at
  the new (not-yet-existing) GitHub URL — out of scope until the repo is
  actually pushed; can be a small follow-up change later if wanted.

## Decisions

**New repo is single-plugin-at-root, not `plugins/markdown-ia/` nested,
and carries its own `marketplace.json`.** `ia-lessons`'s `plugins/<name>/`
nesting exists because it hosts *three* plugins from one marketplace.json.
A standalone repo with only one plugin doesn't need that indirection —
`.claude-plugin/plugin.json` at repo root matches the common
single-plugin-repo pattern. A `plugin.json` alone isn't installable,
though — `.claude-plugin/marketplace.json` is what a user actually adds
as a source (`/plugin marketplace add`), so the new repo needs its own,
scoped to just this one plugin (mirroring `ia-lessons`'s marketplace.json
shape, but with a single entry pointing at `.`). Alternative considered:
keep the `plugins/markdown-ia/` nesting for consistency with `ia-lessons`
— rejected as unnecessary indirection for a repo with nothing else in it.

**Local path for the new repo: a sibling directory next to `ia-lessons`**
(`/Users/joycestack/Documents/workspace/markdown-ia-skills`), matching how
this workspace already organizes independent projects side by side, not
nested inside `ia-lessons` (which would contradict "extract into a new
repo").

**Evals self-scan fixture is rewritten against the new repo, not ported
verbatim.** The old assertions specifically check for things unique to
`ia-lessons`'s shape: "plugin vs skill" terminology tension (only present
because `ia-lessons` documents multiple plugins), near-zero tagging
frontmatter across *three* plugins worth of files, SKILL.md as "a distinct
content type" (meaningful only when SKILL.md files are a minority pattern
among other doc types). The new repo is smaller and single-plugin, so
those specific claims may not hold. Tasks will re-run each skill against
the new repo and adjust eval assertions to match what's actually true
there, rather than copy old assertions that could now be false claims
about the fixture.

**`.gitignore` and `LICENSE` are copied, not referenced.** The new repo
needs to stand alone; copying `ia-lessons`'s relevant `.gitignore` entries
(the `evals/runs/`, `*.skill` exclusions) and the MIT `LICENSE` verbatim
keeps it self-sufficient without a dependency back on `ia-lessons`.

## Risks / Trade-offs

- **Risk**: Losing git blame/history for these files makes it harder to
  answer "when did this skill's guidance change" later. → **Mitigation**:
  Explicitly the user's informed choice (fresh start); `ia-lessons`'s own
  history still has the full history up to the point of extraction, so it
  isn't gone, just not carried into the new repo.
- **Risk**: Root README and other cross-references in `ia-lessons` get
  updated inconsistently (one section mentions markdown-ia, another
  forgets). → **Mitigation**: tasks.md enumerates every known
  cross-reference found via grep before editing, not just the obvious
  ones.
- **Risk**: The rewritten eval assertions in the new repo turn out to be
  weaker than the originals (easier to pass, less useful signal).
  → **Mitigation**: Read the actual skill output against the new repo
  before finalizing assertions, don't just relax them to make the fixture
  fit — same discipline the original evals.json note already calls for
  ("judge substance qualitatively, don't force exact-content assertions").
- **Risk**: A contributor or user still has `ia-lessons`'s marketplace
  cached and tries `/plugin install markdown-ia` after this change ships,
  and it fails with no explanation. → **Mitigation**: Root README's
  removal of the markdown-ia section should note where it moved to (even
  without a live URL yet), so anyone reading gets a pointer instead of a
  silent gap.

## Migration Plan

1. Create the new repo locally with the moved content and a fresh initial
   commit (tasks.md).
2. Verify the new repo's skills/evals/README are self-consistent and its
   evals pass against the new fixture shape.
3. Remove `plugins/markdown-ia/` and `examples/sample-reports/argo-cd/`
   from `ia-lessons`, update `marketplace.json` and root `README.md`.
4. Commit the `ia-lessons` side of the change.
5. Rollback, if needed before either commit lands: nothing destructive
   happens until step 3's removal is committed — the new repo can be
   deleted and `ia-lessons` is untouched up to that point.

## Open Questions

- Should `ia-lessons`'s root README leave a pointer to the new repo's name
  (`markdown-ia-skills`) even without a live URL, for anyone who lands on
  the old README before it's updated in their local checkout? (Current
  plan: yes, mention the repo name as "moved to its own repo" even without
  a clickable link, since the URL doesn't exist until the user pushes it.)
