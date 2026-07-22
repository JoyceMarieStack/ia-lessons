# Corpus Discovery Report — Argo CD Docs

## Summary

The corpus is 456 Markdown files under `docs/`, and Markdown is effectively
the whole corpus — `find` turns up no other document formats in scope (a
handful of PNG assets aside). This reads as a mature, actively maintained
docs-as-code set: it's driven by an `mkdocs.yml` nav that structures nearly
everything, and `docs/` has 1,007 distinct contributors in git history, with
the most recent commit from 2026-07-16. Structure is consistent within the
two largest folders (`user-guide`, `operator-manual`) and looser toward the
edges (`proposals`, top-level loose files).

Note: three stray files were found in the corpus that are not real
documentation — `docs/corpus-discovery-report.md`,
`docs/developer-guide/corpus-discovery-report.md`, and a
`terminology-audit-output/` directory at the repo root, all untracked in
git. These look like output artifacts from a previous IA-skill run that
wrote into the source repo instead of an outputs directory. They're
excluded from all counts below and are worth deleting from that repo.

## Content distribution

| Folder | Markdown files |
|---|---|
| `user-guide/` | 218 |
| `operator-manual/` | 157 |
| `proposals/` | 35 |
| `developer-guide/` | 31 (excludes the stray report file) |
| `snyk/` | 1 |
| Top-level loose files (`index.md`, `getting_started.md`, `faq.md`, etc.) | 9 |

Total: 456 files (after excluding the 2 stray report files noted above).

## Repository structure

Hierarchical and nav-driven: `mkdocs.yml` at the repo root defines an
explicit `nav:` tree that maps folders like `operator-manual/` and
`user-guide/` into sectioned menus (e.g. Operator Manual → High
Availability, User Management, Security as sub-groups). This is the real
reading order — folder layout on disk and nav grouping mostly agree, but
the nav adds a layer of curated grouping (e.g. `snyk/index.md` is nested
under Operator Manual → Security in the nav despite living in its own
top-level folder). `developer-guide/` and `proposals/` are looser: the
former reads as a flat FAQ/how-to collection, the latter is numbered or
date-prefixed design docs (`001-proposal-template.md`,
`2022-07-13-appset-progressive-rollout-strategy.md`) without a nav entry
per file.

## Observations

| Observation | Example file(s) | What it suggests |
|---|---|---|
| Frontmatter is rare — only 40 of 456 files open with a `---` block | most `user-guide/*.md` | Structure is carried by the nav config, not per-file metadata |
| File length varies widely within one folder | `developer-guide/ci.md` (~70 lines) vs. `operator-manual/*.md` (many 200+ lines) | No uniform length convention even within a folder |
| GitHub-flavored admonitions (`> [!TIP]`, `> [!WARNING]`, `> [!NOTE]`) are common in top-level and user-guide docs | `getting_started.md` | A real, repeated structural pattern worth checking for consistency |
| Some files are pure redirects/stubs | `user-guide/sync_waves.md` variant: `"> This page has moved. See [New Page]"` | A handful of pages are placeholders, not content |
| `proposals/` files are numbered or date-prefixed rather than title-named | `001-proposal-template.md`, `004-scalability-benchmarking.md` | This folder follows a design-doc convention distinct from the rest of the corpus |

## Gaps

- No per-file metadata (owner, status, last-reviewed) anywhere sampled — currency is tracked at the git/repo level instead.
- `developer-guide/` mixes CI troubleshooting, contribution process, and local dev setup in one flat folder with no sub-grouping, unlike the nested `operator-manual/`.
- A few stub/redirect pages exist inside otherwise substantive folders (see Observations) — worth a pass to confirm none are stale.

## Out of scope

The corpus also has non-Markdown assets (PNGs like `ci-pipeline-failed.png`, CSS/JS under `assets/`) that support the docs but aren't analyzed here; these are a small fraction of the tree.

## Recommendations for deeper analysis

**`markdown-content-model-discovery`** would be valuable next — file length varies substantially within folders, frontmatter presence is inconsistent (40/456), and heading structure looks looser in `developer-guide/` and `proposals/` than in the nav-driven folders, all of which point to real variety worth turning into an explicit schema.

**`markdown-vocabulary-governance`** is also worth running — a project this size with 1,007 contributors across `docs/` is a strong candidate for terminology drift (e.g. how consistently "ApplicationSet controller," "sync wave," and similar Argo CD-specific terms are used across `user-guide/` and `operator-manual/`).
