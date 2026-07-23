## Why

`markdown-ia`'s three skills (corpus discovery, content-model discovery,
vocabulary governance) are a self-contained, standalone-installable unit
with no dependency on the other two plugins in this repo (`terminology-audit`,
`vocabulary-contract`). Giving it its own repo lets it be installed,
versioned, and iterated on independently, and keeps `ia-lessons` focused on
the terminology-audit → vocabulary-contract pipeline that the other two
plugins form together.

## What Changes

- **BREAKING**: Remove `plugins/markdown-ia/` (plugin.json, skills/,
  evals/, README.md) from `ia-lessons` entirely — installing `markdown-ia`
  from `ia-lessons`'s marketplace will no longer work after this change.
- **BREAKING**: Remove the `markdown-ia` entry from
  `.claude-plugin/marketplace.json`.
- Create a new standalone local git repo, `markdown-ia-skills`, containing:
  the three skills, the plugin's `plugin.json` (promoted to repo root, not
  nested under `plugins/markdown-ia/`), its evals, its README, a copied
  `LICENSE` (MIT, matching `ia-lessons`), and `examples/sample-reports/argo-cd/`
  (moved from `ia-lessons`, since those three reports are markdown-ia's own
  worked output and referenced by its README).
- Rework markdown-ia's evals self-scan fixture: today it scans `ia-lessons`
  itself (multi-plugin structure, "plugin vs skill" terminology tension).
  Once extracted, the new repo is the self-scan target instead — smaller
  and single-plugin — so the eval prompts/assertions built on the old
  repo's shape need to be re-verified against the new one's.
- No commit history is carried over — the new repo starts with a fresh
  initial commit of the current file contents.
- Update `ia-lessons`'s root `README.md` (repo layout, Plugins section,
  Examples section, "How the pieces fit") to remove markdown-ia coverage
  and, where useful, point to the new repo.
- This change prepares the new repo locally only; creating it on GitHub and
  pushing is a separate, manual step for the user.

## Capabilities

### New Capabilities
- `markdown-ia-standalone-packaging`: the extracted `markdown-ia-skills`
  repo is self-contained and independently installable as a Claude Code
  plugin, with no residual dependency on `ia-lessons`.

### Modified Capabilities
(none — no existing `openspec/specs/` capability governs plugin layout or
repo structure; `plugin-marketplace-registration` from the prior change
covers marketplace *entries* matching plugin directories, which this
change satisfies by removing both together, not by changing that
requirement's behavior)

## Impact

- Removed: `plugins/markdown-ia/` (entire directory) and
  `examples/sample-reports/argo-cd/` from `ia-lessons`.
- Modified: `.claude-plugin/marketplace.json`, root `README.md`.
- New: a sibling local git repo `markdown-ia-skills` (path to be decided
  in design), self-contained and independently installable once pushed.
- No impact on `terminology-audit` or `vocabulary-contract` — verified
  `examples/sample-dataset/` (their shared fixture) is unrelated to
  markdown-ia and stays in `ia-lessons` untouched.
- No impact on code/runtime behavior of the three skills themselves — this
  is a relocation, not a rewrite.
