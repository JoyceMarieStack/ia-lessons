## 1. Scaffold the new repo

- [x] 1.1 Create `/Users/joycestack/Documents/workspace/markdown-ia-skills/` and `git init` it
- [x] 1.2 Copy `plugins/markdown-ia/.claude-plugin/plugin.json` to the new repo's root `.claude-plugin/plugin.json` (content unchanged — name, version, description, author)
- [x] 1.3 Create a new root `.claude-plugin/marketplace.json` scoped to this one plugin (single entry, `source: "."`, description matching `plugin.json`), so the repo is directly addable via `/plugin marketplace add`
- [x] 1.4 Copy `plugins/markdown-ia/skills/` to the new repo's root `skills/` (all three SKILL.md files, unchanged)
- [x] 1.5 Copy `plugins/markdown-ia/evals/` to the new repo's root `evals/`
- [x] 1.6 Copy `plugins/markdown-ia/README.md` to the new repo's root `README.md`
- [x] 1.7 Copy `examples/sample-reports/argo-cd/` to the new repo's `examples/sample-reports/argo-cd/` — do NOT copy `examples/sample-dataset/` (NASA planets); confirmed that's terminology-audit's fixture, unrelated to markdown-ia, and stays in `ia-lessons` only
- [x] 1.8 Copy `LICENSE` (MIT) from `ia-lessons` to the new repo's root, unchanged
- [x] 1.9 Create a `.gitignore` in the new repo carrying over the relevant `ia-lessons` entries (`evals/runs/`, `*.skill`, `.DS_Store`) scoped to the new repo's own paths

## 2. Fix up cross-references inside the new repo

- [x] 2.1 Update `markdown-ia-skills/README.md`'s link to the Argo CD sample reports from `../../examples/sample-reports/argo-cd` (relative to `ia-lessons`) to `examples/sample-reports/argo-cd` (relative to the new repo root)
- [x] 2.2 Update `markdown-ia-skills/README.md`'s Install section and "What's inside" tree to reflect the new root-level layout (no `plugins/markdown-ia/` nesting)
- [x] 2.3 Grep the new repo for any other `ia-lessons`-relative path or reference and fix or remove it — only hit was `evals/evals.json`'s self-scan fixture note/prompt (expected; handled in group 3)

## 3. Rework the evals self-scan fixture for the new repo

- [x] 3.1 Read `markdown-ia-skills/evals/evals.json`'s current fixture note and the three eval prompts/assertions (all built around scanning `ia-lessons`'s multi-plugin structure)
- [x] 3.2 Actually run (or reason through) each of the three skills against the new repo's own content to see what's really there now (single plugin, three skills, no "plugin vs skill" tension from sibling plugins) — verified via direct grep/count: 7 total .md files (3 SKILL.md, 3 argo-cd reports, 1 README), no .py/.csv, skill:plugin term ratio ~29:6 with "plugin" confined to install/packaging context, and a real trap found (argo-cd report content discusses Argo CD's own ApplicationSet/Application Set drift, which could be mistaken for this repo's own drift)
- [x] 3.3 Rewrite the fixture note and any assertions that assumed `ia-lessons`'s multi-plugin shape (e.g. the "plugin vs skill" terminology-tension assertion in the vocabulary-governance eval) so they describe what's actually true when scanning `markdown-ia-skills` alone
- [x] 3.4 Leave assertions that still hold unchanged (near-zero tagging/facet frontmatter outside SKILL.md's name/description is still true; SKILL.md as a distinct content type at the 3+ file threshold is still true) — verified, not assumed

## 4. Commit the new repo

- [x] 4.1 `git add` everything in the new repo and make a single fresh initial commit (no history import, per design)
- [x] 4.2 Verify the new repo's `plugin.json` and `marketplace.json` are both valid JSON, the marketplace entry's `name` matches `plugin.json`'s `name`, and `skills/*/SKILL.md` frontmatter names match their directory names

## 5. Remove markdown-ia from ia-lessons

- [x] 5.1 Remove `.claude-plugin/marketplace.json`'s `markdown-ia` entry
- [x] 5.2 Validate `.claude-plugin/marketplace.json` is still well-formed JSON with `terminology-audit` and `vocabulary-contract` remaining
- [x] 5.3 Delete `plugins/markdown-ia/` from `ia-lessons`
- [x] 5.4 Delete `examples/sample-reports/argo-cd/` from `ia-lessons`
- [x] 5.5 Confirm `examples/sample-dataset/` and `examples/sample-reports/planets/` (terminology-audit's fixtures) are untouched

## 6. Update ia-lessons's root README

- [x] 6.1 Remove the `markdown-ia/` block from the "Repo layout" tree
- [x] 6.2 Remove the `### markdown-ia` subsection under "## Plugins", replacing it with a short note that it moved to its own repo (`markdown-ia-skills`), per the design's decision to leave a pointer even without a live URL yet
- [x] 6.3 Update the "## Tests" section's markdown-ia paragraph (references `plugins/markdown-ia/evals/evals.json`) to remove or reframe it as no longer part of this repo
- [x] 6.4 Update "## Examples" section to remove the Argo CD report bullet (or note it moved) and confirm the NASA planets and job-scheduler/SDD bullets are unaffected
- [x] 6.5 Update "## How the pieces fit" step 1 ("Discover... (`markdown-ia`)") to reflect that markdown-ia is now a separate, standalone tool rather than step 1 of this repo's in-repo pipeline
- [x] 6.6 Run the "Adding a plugin" verification check (`comm -23 <(ls plugins | sort) <(jq -r '.plugins[].name' .claude-plugin/marketplace.json | sort)`) and confirm it reports zero missing entries with markdown-ia gone from both sides

## 7. Final verification

- [x] 7.1 Grep all of `ia-lessons` for the string `markdown-ia` and confirm every remaining hit is an intentional "moved to its own repo" pointer, not a stale link or leftover file reference — only hits are in README.md, all intentional
- [x] 7.2 Confirm `plugins/markdown-ia/` and `examples/sample-reports/argo-cd/` no longer exist in `ia-lessons`
- [x] 7.3 Confirm the new `markdown-ia-skills` repo has a clean `git status` after the initial commit
