# Argo CD Docs — Terminology Audit

## Summary

Scanned 453 Markdown files under `docs/` (56.5K lines), excluding `docs/snyk/`, which is a
vendored third-party scan report and not authored documentation. Given the corpus size, this
pass prioritized the 8 concept families with the most observable variation (via targeted
frequency counts across the whole tree) rather than reading all 453 files line by line; a full
manual pass would likely surface additional low-frequency variants.

Overall severity: **mostly cosmetic, with one naming collision worth a quick fix.** Argo CD's
docs are generally disciplined about defining CRD/API names once and reusing them — the main
gaps are an inconsistent-casing file (`Appset-Any-Namespace.md`) that could confuse a skimming
reader, an unexpanded `SSO` acronym on several top-level pages, and a handful of informal
synonyms (`target cluster`, `git repo`) that don't match the API's actual field/component names.

## Inconsistencies found

| Concept | Variants observed | Recommended preferred term | Locations | Notes |
|---|---|---|---|---|
| ApplicationSet CRD/controller | `ApplicationSet` (68), `AppSet` (9), `Appset` (3) | `ApplicationSet`; `AppSet` as accepted shorthand | operator-manual/applicationset/*.md, feature-maturity.md, server-commands/argocd-applicationset-controller.md | `Appset-Any-Namespace.md`'s filename and inline prose use a third casing that matches neither the CRD name nor the shorthand — this is the one true naming collision, see callout below. |
| AppProject CRD | `AppProject` (32), `Application Project` (1) | `AppProject` | operator-manual/declarative-setup.md; user-guide/source-integrity.md:6 | Single stray instance; low risk but easy fix. |
| Destination cluster | `destination cluster` (13), `target cluster` (11) | `destination cluster` (matches `spec.destination` API field) | operator-manual/secret-management.md, deep_links.md, applicationset/Use-Cases.md, declarative-setup.md | Roughly 50/50 split — worth standardizing since `destination` is the literal spec field name. |
| Sync status OutOfSync | `OutOfSync` (17, code/status literal), `out-of-sync` (9, attributive), `out of sync` (7, predicate) | `OutOfSync` for code/API references; `out of sync`/`out-of-sync` prose forms are both grammatically correct depending on position in the sentence | getting_started.md, index.md, faq.md, cluster-bootstrapping.md | Not a real conflict — English correctly hyphenates attributive adjectives ("out-of-sync status") and not predicate ones ("is out of sync"). Flagged only for awareness; no action needed unless a single doc mixes both forms in the same sentence type. |
| Config Management Plugin | `Config Management Plugin (CMP)` (14), `CMP` (9) | `Config Management Plugin (CMP)` on first use, `CMP` after | config-management-plugins.md, high_availability.md | This is the model to copy elsewhere — each page defines the acronym before using it. |
| Single Sign-On | `SSO` unexpanded (21), `Single Sign-On` (4) | `Single Sign-On (SSO)` — expand on first use per page | index.md, security_considerations.md, getting_started.md, custom-styles.md, declarative-setup.md vs. operator-manual/security.md, user-management/okta.md, identity-center.md | Several high-traffic top-level pages (index.md, getting_started.md) use `SSO` with no expansion anywhere on the page — a first-time reader has to infer the meaning. |
| Resource hook | `resource hook` (1), `Resource Hook` (1, heading case) | `resource hook` in prose, `Resource Hook` only in headings/titles | user-guide/annotations-and-labels.md, applicationset/Progressive-Syncs.md | Trivial, sentence-case-in-prose vs title-case-in-headings is standard and fine as-is. |
| Git repository vs. repo-server | `Git repository` (42), `git repo` (19), `repo-server` (210, component name) | `Git repository` in prose describing the source of truth; `repo-server` reserved strictly for the `argocd-repo-server` component | security.md, cluster-bootstrapping.md, high_availability.md | `repo-server` is **not** a synonym for "Git repository" — it's the name of the running service that clones/caches repos. Docs already keep these distinct in practice; flagged only so it isn't accidentally conflated in future edits. `git repo` (informal) vs. `Git repository` (formal) is a minor register inconsistency, not a meaning conflict. |
| Rollback vs. revert | `rollback` (16), `revert` (12) | `rollback` for Argo CD's Application history/rollback feature; `revert` for Git/PR/config reverts | index.md, architecture.md, auto_sync.md vs. submit-your-pr.md, running-locally.md | These are genuinely different concepts that happen to sound similar — correctly kept distinct in current usage, no change needed. |

## Items needing stakeholder input

| Concept | Competing options | Why it's not a clear call |
|---|---|---|
| SSO expansion policy | Expand `SSO` on every page vs. only in `operator-manual/security.md` and link to it | Practitioners overwhelmingly search "SSO," so forcing full expansion everywhere may hurt scannability; but top-level pages (index.md, getting_started.md) are often a new user's first exposure. Needs a docs-team call on whether to add a glossary link instead of re-expanding inline each time. |
| target cluster vs. destination cluster | Standardize on `destination cluster` (API-aligned) vs. keep `target cluster` as more approachable prose | Both are understandable to readers; the split is roughly even (13 vs 11), so this is a style preference more than an error — flagging for a style-guide decision rather than forcing one now. |

## Recommendations

1. **Fix the `Appset-Any-Namespace.md` casing first** — rename references (and ideally the file)
   to align with either `ApplicationSet` or the accepted `AppSet` shorthand. This is the one spot
   where a reader could genuinely misread the term as naming something else.
2. **Add an SSO glossary entry or first-use expansion** on `index.md` and `getting_started.md` —
   cheap fix, high visibility since these are entry-point pages.
3. **Fix the single `Application Project` instance** in `user-guide/source-integrity.md:6` to
   `AppProject`.
4. **Add a short "Terminology" section to the contributor/style guide** (`docs/developer-guide/`)
   capturing: `ApplicationSet`/`AppSet`, `AppProject`, `destination cluster`, and the
   expand-then-abbreviate pattern used well in `config-management-plugins.md`. This gives new
   contributors and AI-assisted edits a reference to check against, since docs are contributed by
   many people over time and drift is expected without one.
5. **No action needed** on `OutOfSync`/`out of sync`/`out-of-sync` or `rollback`/`revert` — both
   are correctly distinct usages, included here only so they aren't mistakenly "fixed" by a
   future cleanup pass.
