# Corpus Discovery Report: Argo CD Docs

Corpus root: `argo-cd/docs`

## 1. Summary

The corpus holds **455 Markdown files**, about **68% of the 668 total files** under `docs/` — the remainder is mostly screenshots and generated scan reports, so Markdown is the right scope but not the whole story. First impression: this reads as an actively maintained set — commits run through 2026-07-16, roughly 950+ distinct contributors have touched `docs/` over its history, and it's wired into a real `mkdocs.yml` nav — though structural conventions vary a lot between areas (hand-written guides vs. auto-generated CLI reference vs. structured proposals).

## 2. Content distribution

| Top-level location | Markdown files |
|---|---|
| `user-guide/` (incl. `commands/`, 170 files) | 218 |
| `operator-manual/` (incl. `applicationset/`, `upgrading/`, `notifications/`, etc.) | 157 |
| `proposals/` | 35 |
| `developer-guide/` | 32 |
| Root-level files (`index.md`, `faq.md`, `core_concepts.md`, etc.) | 12 |
| `snyk/` | 1 |
| **Total** | **455** |

## 3. Repository structure

The layout is hierarchical and audience-first: `user-guide/` and `operator-manual/` each split into topic subfolders (`commands/`, `applicationset/`, `upgrading/`, `notifications/services/`, `user-management/`), while `developer-guide/` and `proposals/` stay flatter — a sensible split for a project this size (user vs. operator vs. developer, topic-first below that).

A root-level `mkdocs.yml` governs the actual reading order and is worth consulting before judging structure from folders alone — `snyk/` has only one Markdown file but a real nav entry, since most of its content is generated HTML scan reports it links out to rather than more Markdown.

## 4. Observations

| Observation | Example file(s) | What it suggests |
|---|---|---|
| Frontmatter confined to one folder | `proposals/002-ui-extensions.md` (title/authors/creation-date) vs. `operator-manual/rbac.md` (none) | Only 32 of 455 files (7%) open with a real YAML frontmatter block, all in `proposals/`; everything else relies on headings and nav placement alone |
| Wide file-length spread | `user-guide/commands/argocd_app.md` (99 lines) vs. `operator-manual/rbac.md` (460 lines) vs. `operator-manual/applicationset/Generators-Cluster.md` (315 lines) | Hand-authored topic pages and generated reference pages coexist at very different scales within the same corpus |
| Heading density varies sharply by area | `proposals/002-ui-extensions.md` (23 heading lines) vs. `user-guide/commands/argocd_app_sync.md` (6 heading lines) | Some content is deeply sectioned prose, other content is short and formulaic — not one shared document shape |
| Mechanical naming convention in one subtree | `operator-manual/upgrading/3.5-3.6.md` (32 files, one per version pair) | Good candidate for pattern-based tooling rather than manual review |
| Long history predates most current content | first `docs/` commit 2018-03-08, latest 2026-07-16 | Roughly 8 years of accretion — expect real variance in style/length even within one folder |

## 5. Gaps

- No frontmatter or metadata convention outside `proposals/` — no owner, status, or last-reviewed signal on the bulk of the corpus
- `snyk/` is a single thin file pointing to generated reports; unclear if it's meant to expand or stay a redirect page
- Root-level files (`faq.md`, `core_concepts.md`, `getting_started.md`, etc.) sit outside any of the three main audience folders — worth confirming the nav treats them intentionally rather than as orphans

## 6. Out of scope

Roughly 213 non-Markdown files live under `docs/` — screenshots, generated HTML scan reports, YAML samples, and a handful of image/JSON/JS/CSS files. These aren't inventoried here.

## 7. Recommendations for deeper analysis

- **`markdown-content-model-discovery`** would be the natural next step — the variety visible here (frontmatter present in only one subfolder, a roughly 4x length spread between sampled files, and heading counts ranging from 6 to 23 across files) is exactly the kind of structural inconsistency a frequency-based field/section analysis can turn into a grounded schema.
- **`markdown-vocabulary-governance`** is lower priority right now — nothing sampled here pointed to competing terminology, but it'd be worth a look if a glossary/style-guide effort is planned, since the corpus spans user-, operator-, and developer-facing content that may name the same concepts differently.
