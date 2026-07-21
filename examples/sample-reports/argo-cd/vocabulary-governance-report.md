# Vocabulary Governance Report — Argo CD Docs

## Summary

Scanned 456 Markdown files. Vocabulary is largely consistent for a corpus
this size — most acronyms (API, CLI, TLS, RBAC, etc.) are used as
expected — but two real product-naming variants surfaced: "ArgoCD" vs.
"Argo CD" and "Application Set(s)" vs. "ApplicationSet(s)". Taxonomy is
the bigger gap: there is no frontmatter-based tagging or categorization
anywhere in the corpus (0 files use `tags`, `categories`, `labels`,
`domain`, or `topic`) — all classification is implicit, carried entirely
by folder structure and the `mkdocs.yml` nav. One candidate ("Side
Apply") was ruled out as a regex artifact — it matched inside both
"client-side apply" and "server-side apply," two genuinely distinct and
correctly-used Kubernetes concepts, not a real variant pair.

## Vocabulary Governance

### Canonical terms

| Term | Classification | Status | Notes |
|---|---|---|---|
| Argo CD | ● unambiguous | approved | Dominant form (3,744 prose occurrences) and the project's official branding; canonical |
| ArgoCD | △ ambiguous | needs stakeholder input | 258 occurrences in prose (e.g. `bug_triage.md`, `security_considerations.md`, `try_argo_cd_locally.md`) use the closed-compound form where the rest of the corpus uses "Argo CD" |
| ApplicationSet | ● unambiguous | approved | Dominant form (626 singular + 94 plural) and matches the actual Kubernetes CRD `kind: ApplicationSet` |
| Application Set / Application Sets | △ ambiguous | needs stakeholder input | 16 occurrences (`operator-manual/webhook.md`, `operator-manual/metrics.md`, `operator-manual/cluster-bootstrapping.md`) space the term where it should match the CRD's closed-compound name |
| client-side apply / server-side apply | ○ correct-in-context | approved | Two distinct Kubernetes apply strategies, both used correctly — not a variant pair despite matching a shared "Side Apply" regex candidate |
| CMP (Config Management Plugin) | ● unambiguous | approved | Acronym (83 uses) expanded on first use in guide-style docs (28 spelled-out uses); consistent with the corpus's general first-use-expansion pattern |
| GitOps | ● unambiguous | approved | 50 Title Case vs. 17 lowercase (`gitops`) — lowercase instances are consistently inside code, URLs, or repo/package names, not prose drift |

### Synonyms

| Canonical | Observed variants |
|---|---|
| Argo CD | ArgoCD |
| ApplicationSet | Application Set, Application Sets, Applicationset, Applicationsets |

### Preferred spellings

| Preferred | Rejected forms |
|---|---|
| Argo CD | ArgoCD |
| ApplicationSet | Application Set, Applicationset |
| ApplicationSets | Application Sets, Applicationsets |

### Naming conventions

- Product and component names use Title Case with the space preserved where the official name has one ("Argo CD") and closed where the CRD/binary name has none ("ApplicationSet").
- Acronyms (CMP, RBAC, OIDC, SSO) are expanded on first use in conceptual/how-to guides; CLI reference and upgrade-guide pages use them unexpanded, consistent with those types being generated/terse by design (see `content-model-report.md`).
- Kubernetes-native terms (client-side apply, server-side apply, ConfigMap, Secret) follow upstream Kubernetes casing and hyphenation rather than an Argo-specific convention.

### Deprecation rules

| Deprecated | Replacement | Notes |
|---|---|---|
| ArgoCD | Argo CD | Closed-compound form should be phased out of prose; leave untouched inside code blocks, CLI binary name (`argocd`), and URLs where it's technically correct |
| Application Set(s) | ApplicationSet(s) | Space-separated form should be phased out in favor of the CRD-matching closed-compound form |

## Taxonomy Design

### Classification facets

| Facet | In use? | Notes |
|---|---|---|
| `tags` | No | 0 occurrences anywhere in the corpus |
| `categories` | No | 0 occurrences anywhere in the corpus |
| `labels` | No | 0 occurrences anywhere in the corpus |
| `domain` | No | 0 occurrences anywhere in the corpus |
| `topic` | No | 0 occurrences anywhere in the corpus |
| Folder structure (implicit) | Yes | The only classification signal in the corpus — `user-guide/`, `operator-manual/`, `developer-guide/`, `proposals/` |
| `mkdocs.yml` nav grouping | Yes | Adds a curated layer on top of folders (e.g. nests `snyk/` under Operator Manual → Security) — see `corpus-discovery-report.md` |

### Allowed values

No frontmatter facet fields exist to normalize — there is no drift to resolve because there is no taxonomy metadata in use. If a facet were introduced, the natural starting values are the four content types identified in `content-model-report.md`: `cli-reference`, `upgrade-guide`, `design-proposal`, `conceptual-guide`.

### Hierarchies

- Implicit only, via folders and nav nesting, e.g.:
  - `operator-manual` → `user-management` → per-provider pages (auth0, okta, github-actions, ...)
  - `operator-manual` → `applicationset` → generator-specific pages
- No explicit parent/child facet values exist since no facet fields are populated.

### Metadata schema

| Facet | Frontmatter field | Cardinality | Required? |
|---|---|---|---|
| Content type | *(none currently — recommend `type`)* | single-value | Would be optional to introduce; not currently required anywhere |
| Topic/domain | *(none currently — recommend `domain`)* | multi-value | Would be optional; folder structure already carries most of this signal |

### Facet governance

- No facet values currently exist, so there's nothing actively drifting — but that also means there's no owner or review process to point to.
- If `type`/`domain` frontmatter fields are introduced (see Classification facets), ownership should sit with whoever already maintains `mkdocs.yml`, since that's the closest existing taxonomy authority.
- New facet values should be reviewed against the four content types and existing folder/nav structure before being added, to avoid the tag sprawl a corpus this size (1,007 contributors to `docs/`) could easily produce once tagging starts.

## Cross-cutting observations

- The "ArgoCD" vs. "Argo CD" drift concentrates in older/security-related conceptual pages (`bug_triage.md`, `security_considerations.md`) rather than the CLI reference or upgrade-guide types, consistent with those two types being hand-written prose vs. generated/templated content.
- The complete absence of taxonomy metadata mirrors the content-model finding that only `proposals/` has any frontmatter at all — this corpus relies on structure (folders, nav, headings) rather than metadata fields for both content typing and classification.
- The "ApplicationSet" drift and content-model discovery's finding that `applicationset/` is its own subfolder under `operator-manual/` suggest the same underlying pattern: the feature is well-established structurally but its name hasn't been fully normalized across older pages.
