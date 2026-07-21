# Vocabulary Governance Report — argo-cd/docs

## 1. Summary

Scanned 456 Markdown files under `argo-cd/docs` (`user-guide` 218, `operator-manual` 157, `proposals` 35, `developer-guide` 32, `snyk` 1). Terminology looks generally disciplined for a project of this size — most acronyms (API, RBAC, OIDC, CMP) are used consistently — but roughly a dozen term clusters show real casing/spacing drift or old-vs-new naming (`ApplicationSet` vs `Application Set`, `Server-Side Apply` vs `ServerSideApply`, `manifest hydrator` vs `source hydrator`). Taxonomy is the bigger first-pass finding: there is effectively **no classification/tagging system** in this corpus — no `tags`, `categories`, `domain`, or `topic` frontmatter anywhere, and only the 32 files under `proposals/` carry any frontmatter at all (an RFC-style authorship schema, not a content taxonomy). Organization is entirely implicit, via folder structure.

## 2. Vocabulary Governance

### Canonical terms

| Term | Classification | Status | Notes |
|---|---|---|---|
| ApplicationSet | ● | approved | 626 occurrences vs. 16 for spaced "Application Set"; product/CRD name, not a general noun phrase |
| Server-Side Apply | ○ | approved | Prose term for the Kubernetes feature; `ServerSideApply=true` / `ServerSideDiff=true` are literal sync-option string values, not prose variants — both forms are correct in their own context |
| Config Management Plugin (CMP) | ● | approved | 119 CMP vs. ~34 spelled-out forms; expanded on first use in guides, used as acronym elsewhere — consistent per section |
| Source Hydrator | ● | approved | Current feature name; supersedes early "Manifest Hydrator" |
| Manifest Hydrator | △ | needs stakeholder input | Only in the original 2024 proposal doc (4 occurrences) — read as historical, but proposal isn't marked deprecated |
| Single Sign-On (SSO) | ○ | approved | SSO (76) dominates as the working acronym; spelled-out form appears mainly in headings/menu-item quotes from third-party UIs (Microsoft, AWS) — those are literal UI labels, not inconsistency |
| repository / repo | ○ | approved | "repository" (845) is the formal/reference term, "repo" (1469) the informal/CLI-flag term (`repo-server`, `--repo`) — split tracks real vs. component naming, not drift |
| Progressive Syncs | ● | approved | Current shipped feature name (9 occurrences) |
| Progressive Rollout | △ | needs stakeholder input | 2 occurrences, both in a 2022 proposal title/body for what became "Progressive Syncs" — proposal not updated to reflect final name |
| Continuous Delivery | ● | approved | Used consistently to expand "CD" in intro/concept material; no competing "Continuous Deployment" usage found |
| High Availability (HA) | ○ | approved | HA (357) is the working acronym across operator docs; spelled-out form only in intro material — consistent first-use pattern |

### Preferred spellings

| Preferred | Rejected forms |
|---|---|
| ApplicationSet | Application Set, Application Sets (when referring to the CRD/controller by name — plain-English "application sets" as a general noun phrase is fine) |
| Server-Side Apply | ServerSide Apply, Server Side Apply (in prose; `ServerSideApply` stays as-is inside code/flag values) |
| Server-Side Diff | SideDiff, Side Diff (in prose; `ServerSideDiff` stays as-is inside code/flag values) |
| Source Hydrator | Manifest Hydrator (legacy) |
| Single Sign-On | Single sign-on (mid-sentence lowercase is fine; avoid where it's not a proper-noun UI label) |

### Naming conventions (observed)

- Component/CRD names (ApplicationSet, AppProject) are written as single CamelCase or PascalCase tokens matching the Kubernetes `kind`, never spaced, when referring to the resource type itself.
- Acronyms tied to a Kubernetes-native concept (RBAC, OIDC, CMP, SSO) are expanded once near the top of the page they're introduced on, then used as the acronym for the rest of that page.
- ConfigMap/Secret/flag names are always presented in backticked `code font`, which naturally keeps them separate from prose terminology drift.

### Deprecation rules

| Deprecated | Replacement | Notes |
|---|---|---|
| Manifest Hydrator | Source Hydrator | Confirm with the docs/proposals owner whether `proposals/manifest-hydrator.md` should get a "superseded by" note pointing at `user-guide/source-hydrator.md` |
| Progressive Rollout (as a feature name) | Progressive Syncs | Same treatment — the 2022 proposal predates the shipped feature's final name |

## 3. Taxonomy Design

### Classification facets

| Facet | In use? | Notes |
|---|---|---|
| tags | No | Zero `tags:` frontmatter fields found anywhere in the corpus |
| categories | No | Zero `categories:` frontmatter fields found |
| domain / topic | No | Not used |
| Folder (implicit) | Yes | The only classification signal: `user-guide`, `operator-manual`, `developer-guide`, `proposals`, `snyk` |
| Proposal metadata (title/authors/sponsors/reviewers/approvers/dates) | Yes, but scoped | Present only in `proposals/*.md` (32 of 456 files); this is workflow/authorship metadata, not a content-classification taxonomy |

Recommendation: given zero existing tag adoption, don't retrofit a `tags` field onto the whole corpus — it would be 456 files of guesswork with no current governance owner. If a facet is introduced, start with a single low-cardinality `audience` or `doc-type` field (e.g. `reference`, `how-to`, `concept`, `proposal`) mapped from the folder a file already lives in, rather than inventing free-text tags.

### Allowed values

Not applicable — no facet has any recorded values to reconcile; there is no drift to resolve because there is no taxonomy to have drifted.

### Hierarchies

- Implicit only, via folders:
  - `operator-manual/` → `applicationset/`, `server-commands/`, `templates/`, `upgrading/`, `user-management/`, `notifications/`
  - `user-guide/` → `commands/`
- No frontmatter hierarchy (e.g. `domain: x > y`) exists to compare against these folders.

### Metadata schema

| Facet | Frontmatter field | Cardinality | Required? |
|---|---|---|---|
| Proposal title | `title` | single | Required (in `proposals/`) |
| Proposal authorship | `authors` | multi | Required (in `proposals/`) |
| Proposal review | `sponsors`, `reviewers`, `approvers` | multi | Present but often placeholder `TBD` — effectively optional in practice |
| Proposal dates | `creation-date`, `last-updated` | single | Required at creation; `last-updated` frequently stale relative to file mtime |
| Content classification (any facet) | — none exists — | — | — |

### Facet governance

- No facet governance is needed today because no facet exists — the immediate action is a decision, not a process: does this corpus want a lightweight `doc-type`/`audience` field at all, or is folder placement sufficient?
- If a field is added, its owner should be whoever already reviews `proposals/*.md` frontmatter (the reviewers/approvers list shows an existing informal review habit for that one directory) — extend that habit rather than inventing a new review path.
- New tag values, if introduced, should be listed in a single canonical location (e.g. a `CONTRIBUTING.md` section) before use, so the corpus doesn't repeat the current all-folder-no-tags pattern with a half-populated tags field instead.

## 4. Cross-cutting observations

- The one clear vocabulary/taxonomy overlap is `proposals/`: it's the only directory with any metadata schema at all, and it's also where the two "needs stakeholder input" terminology items (Manifest Hydrator, Progressive Rollout) live — stale proposal docs are a source of both naming drift and the corpus's only metadata inconsistency (missing `status: implemented/superseded` field).
- Because there is no explicit taxonomy, the folder structure (`user-guide` vs `operator-manual` vs `developer-guide`) is doing double duty as both navigation and classification — any future tagging work should treat "does this file live in the right folder" as the taxonomy question, not "what tags should it have."
- Terminology drift is concentrated in newer/evolving features (Source Hydrator, Server-Side Apply, Progressive Syncs) rather than stable core concepts (Application, Project, Sync) — expect the same pattern to recur as new features ship faster than their proposal docs get retired.
