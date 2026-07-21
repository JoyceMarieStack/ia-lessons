# Content Model Report — Argo CD Docs

## Summary

Four content types emerge from the corpus: two large auto-generated CLI
reference groups, one folder of frontmatter-driven design proposals, and a
broad conceptual/how-to bucket covering the rest. The CLI reference and
proposal types are internally very consistent (heading and frontmatter
patterns repeat 80–100% of the time); the conceptual/how-to bucket is the
least consistent, as expected for a group this size and origin.

## Content types

| Type | File count | Sample files | Common sections |
|---|---|---|---|
| CLI command reference | 179 | `user-guide/commands/argocd_app_sync.md`, `operator-manual/server-commands/argocd-dex.md` | Synopsis, Options, Options inherited from parent commands, Examples, See Also |
| Upgrade guides | 32 | `operator-manual/upgrading/2.8-2.9.md`, `operator-manual/upgrading/1.0-1.1.md` | Breaking changes, upgraded dependency notes (e.g. "Upgraded Helm version"), added healthchecks |
| Design proposals | 35 | `proposals/001-proposal-template.md`, `proposals/004-scalability-benchmarking.md` | Summary, Motivation, Goals, Non-Goals, Proposal, Risks and Mitigations, Security Considerations |
| Conceptual / how-to guides | 210 | `user-guide/application-set.md`, `operator-manual/rbac.md`, `developer-guide/ci.md` | Overview, Prerequisites, Configuration, Examples — present inconsistently, no fixed set |

CLI reference is a fallback-folder grouping confirmed by heading pattern
(`user-guide/commands/` — 170 files — and `operator-manual/server-commands/`
— 9 files — both follow the same auto-generated `--help`-derived structure).
Upgrade guides is likewise folder-based (`operator-manual/upgrading/`),
named by version pair rather than topic. The conceptual/how-to bucket is
everything not captured by the other three — it spans `user-guide/`
top-level, most of `operator-manual/` (including `applicationset/`,
`notifications/`, `user-management/`), all of `developer-guide/`, and the
repo-root loose files.

## Recommended schema per type

| Field | Required/Optional | Observed in (%) | Notes |
|---|---|---|---|
| **Design proposals** `title` | Required | 91% (32/35) | De facto required |
| **Design proposals** `authors` | Required | 91% (32/35) | De facto required |
| **Design proposals** `creation-date` | Required | 91% (32/35) | De facto required |
| **Design proposals** `reviewers`/`approvers`/`sponsors` | Recommended | 83% (29/35) | Present in most but not all |
| **Design proposals** `last-updated` | Recommended | 69% (24/35) | Meaningful minority |
| **Design proposals** `status` | Not currently used | 0% (0/35) | See Missing metadata below |
| **CLI reference** frontmatter | N/A | 0% | Auto-generated from CLI `--help`; structure lives in headings, not frontmatter |
| **Upgrade guides** frontmatter | N/A | 0% | Structure lives in headings, not frontmatter |
| **Conceptual/how-to** frontmatter | N/A | ~0% | No consistent frontmatter observed in sample |

## Missing metadata

| Type | Bucket (governance/reference) | Field | Present in (%) | Verdict |
|---|---|---|---|---|
| Design proposals | Governance | `status` | 0% (0/35) | Gap — proposals track motivation and risk in detail but have no field marking draft/accepted/implemented/superseded |
| Design proposals | Governance | `last-updated` | 69% (24/35) | Gap (partial) — worth pushing toward required given the type already treats currency as important |
| CLI command reference | Reference | owner/status/review-date | 0% | N/A — currency is tied to the CLI itself; git history covers it |
| Upgrade guides | Reference | owner/status/review-date | 0% | N/A — tied to release cadence, not independently governed |
| Conceptual/how-to guides | Reference | owner/status/review-date | 0% | N/A — tied to the feature/process it documents |

## Validation rules

- Every `proposals/*.md` file should have `title`, `authors`, and `creation-date` in frontmatter.
- Every `proposals/*.md` file should declare a `status` field (currently absent corpus-wide) with a value such as {draft, implementable, implemented, deferred, rejected, withdrawn, replaced}.
- Every file under `user-guide/commands/` and `operator-manual/server-commands/` should include an `## Options` heading — its near-universal presence (170/179) suggests deviation indicates an incomplete auto-generation pass.
- Every file under `operator-manual/upgrading/` should be named `<from>-<to>.md` matching the version-pair pattern already in universal use.

## Unclassified content

A handful of files didn't cleanly fit any type above — mainly short stub or redirect pages (e.g. a moved-page notice found during corpus discovery) and `operator-manual/templates/` (1 file), too thin to profile as its own group. These are folded into the conceptual/how-to bucket rather than given a dedicated type.
