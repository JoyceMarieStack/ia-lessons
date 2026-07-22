# SDD Terminology Audit Report — add-dark-mode change folder

## 1. Ambiguity Alerts

```
✕ "theme preference" vs "appearance setting" — two words for one thing (AMB-SYN)
  proposal.md › Scope › In scope — "Manual theme preference toggle in settings"
  The base spec stores an "appearance setting"; the proposal's Approach says the change "reuses the stored value" but coins "theme preference" for it, and the delta spec and tasks inherit the new name.
  Decide: adopt "appearance setting" throughout the change, or make the rename explicit in the delta so the base spec's term is updated rather than shadowed.

✕ "Preference Persistence" vs "Setting Persistence" — two words for one thing (AMB-SYN)
  specs/appearance/spec.md › MODIFIED Requirements — "### Requirement: Preference Persistence"
  OpenSpec matches MODIFIED requirements to the base spec by exact header text; the base header is "Setting Persistence", so at archive time this block is added as a new requirement and the old one survives unchanged.
  Decide: retitle the MODIFIED header to exactly "Setting Persistence" (rewording a requirement's title is a separate, explicit step).

✕ "DisplayModeStore" vs "theme preference" — two words for one thing (AMB-SYN)
  design.md › Decision: DisplayModeStore over per-page state — "owns the current selection"
  The store evidently holds the same value the spec calls the theme preference / appearance setting, but no sentence states that mapping — an agent can build DisplayModeStore and separate preference handling half each.
  Decide: add one bridge sentence (e.g. "DisplayModeStore holds the appearance setting, including `system`") — a bridge, not a rename.

? "the preference bridge" — a name nothing establishes (AMB-GHOST)
  tasks.md › Task 2.2 — "Wire the toggle through the preference bridge"
  No audited artifact or base spec defines a "preference bridge"; nearest names found: "theme preference" (proposal, delta), DisplayModeStore and the profile-service mirroring (design).
  Decide: which established thing is this — DisplayModeStore, the profile-service mirror, or something new that must first be introduced in the design?
```

The findings enter one per artifact, but the first two share a root: the
proposal's coinage of "theme preference" is what led the delta to retitle
the persistence requirement. Fixing the coinage in `proposal.md` resolves
both (facets: field 2 · object 2).

## 2. Summary

- Files audited — base spec: `openspec/specs/appearance/spec.md`; change artifacts: `proposal.md`, `design.md`, `specs/appearance/spec.md` (delta), `tasks.md` (all under `openspec/changes/add-dark-mode/`)
- Authority sources inspected: the base spec above; no implementation identifiers were in scope
- `✕` findings (`AMB-SYN`, two words for one thing): 3
- `△` findings (`AMB-POLY` / `AMB-SCENT`, one word or shorthand with two meanings): 0
- `?` findings (`AMB-GHOST`, a name nothing establishes): 1
- Unresolved terminology decisions: 2

## 3. Evidence Table

| Exact text | Anchor | Source location | Candidate concept |
| --- | --- | --- | --- |
| "store a per-user appearance setting with the values `light` and `dark`" | Requirement: Appearance Setting | openspec/specs/appearance/spec.md | Stored light/dark choice |
| "Manual theme preference toggle in settings" | Scope › In scope | proposal.md | Stored light/dark choice |
| "the theme preference reuses the stored value" | Approach | proposal.md | Stored light/dark choice |
| "a `system` value for the theme preference" | ADDED › Requirement: System Option | specs/appearance/spec.md (delta) | Stored light/dark choice |
| "### Requirement: Setting Persistence" | Requirements | openspec/specs/appearance/spec.md | Persistence requirement title |
| "### Requirement: Preference Persistence" | MODIFIED Requirements | specs/appearance/spec.md (delta) | Persistence requirement title |
| "A single `DisplayModeStore` owns the current selection" | Decision: DisplayModeStore over per-page state | design.md | Holder of the stored choice |
| "The `ThemeToggle` component implements the manual theme preference toggle from the proposal" | Decision: CSS custom properties over per-component styles | design.md | Toggle control (bridged) |
| "Wire the toggle through the preference bridge" | Task 2.2 | tasks.md | Unknown referent |

## 4. Terminology Findings

| Sentence to clarify | Concept | Rule | Facet | Variants or meanings | Judgment | Supported wording |
| --- | --- | --- | --- | --- | --- | --- |
| "Manual theme preference toggle in settings" (proposal.md, Scope) | Stored light/dark choice | AMB-SYN | field | "appearance setting" (base spec) vs. "theme preference" (proposal, delta, tasks) | `✕` | appearance setting |
| "### Requirement: Preference Persistence" (delta, MODIFIED) | Persistence requirement title | AMB-SYN | artifact | "Setting Persistence" (base header) vs. "Preference Persistence" (delta header) | `✕` | Setting Persistence |
| "A single `DisplayModeStore` owns the current selection" (design.md) | Holder of the stored choice | AMB-SYN | object | `DisplayModeStore` (design, tasks) vs. "theme preference" storage (proposal, delta) — mapping unstated | `✕` | Unresolved |
| "Wire the toggle through the preference bridge" (tasks.md, Task 2.2) | Unknown referent | AMB-GHOST | object | No referent in any audited artifact; nearest names: DisplayModeStore, profile-service mirror, theme preference | `?` | Unresolved |

## 5. Why Each Finding Matters

| Field | Content |
| --- | --- |
| `Sentence to clarify` | "Manual theme preference toggle in settings" (and every downstream use of "theme preference") |
| `Interpretation A` | "theme preference" is the base spec's "appearance setting" under a new name — supported by Approach: "reuses the stored value" |
| `Interpretation B` | "theme preference" is a new, separate stored value alongside the appearance setting |
| `What could differ` | Whether generated code reads/writes the existing setting or introduces a second field, store key, and API name for the same choice |
| `Why context does not settle it` | The proposal never names "appearance setting"; only the Approach's indirect "reuses the stored value" hints the concepts are one, and the delta and tasks repeat "theme preference" without ever bridging back |
| `Evidence` | Base spec "Requirement: Appearance Setting" vs. proposal Scope/Approach, delta "System Option", tasks 2.3 |
| `Terminology decision` | "appearance setting" — the base spec outranks the change folder in the authority order, and no delta explicitly renames the term |

| Field | Content |
| --- | --- |
| `Sentence to clarify` | "### Requirement: Preference Persistence" |
| `Interpretation A` | The same requirement the base spec titles "Setting Persistence", reworded |
| `Interpretation B` | A new requirement, distinct from "Setting Persistence" |
| `What could differ` | The archive merge: OpenSpec matches MODIFIED blocks by exact header text, so under Interpretation A the intended replacement never happens — the merged spec carries both the old "Setting Persistence" and a near-duplicate "Preference Persistence" |
| `Why context does not settle it` | The delta's body clearly rewrites the base requirement (same scenario, extended for `system`), but the tool does not read bodies — only headers |
| `Evidence` | Base spec "### Requirement: Setting Persistence" vs. delta "### Requirement: Preference Persistence" |
| `Terminology decision` | "Setting Persistence" — a MODIFIED header must match the base header exactly |

| Field | Content |
| --- | --- |
| `Sentence to clarify` | "A single `DisplayModeStore` owns the current selection" |
| `Interpretation A` | `DisplayModeStore` holds the appearance setting / theme preference — the spec concept under an implementation name |
| `Interpretation B` | `DisplayModeStore` is a separate display-state object, with preference storage handled elsewhere (e.g. the profile-service mirror) |
| `What could differ` | Whether an agent implements one holder of the value or two — a store and separate preference persistence, each half-built |
| `Why context does not settle it` | "the current selection" never names the spec term; contrast with `ThemeToggle`, whose decision states its bridge explicitly ("implements the manual theme preference toggle from the proposal") and is therefore not a finding |
| `Evidence` | design.md Decision + File Changes vs. proposal Scope and delta "System Option" |
| `Terminology decision` | Unresolved — the fix is a stated bridge in the design, not a choice between the names |

| Field | Content |
| --- | --- |
| `Sentence to clarify` | "Wire the toggle through the preference bridge" |
| `Interpretation A` | — (no established referent; nearest names found: `DisplayModeStore`, the profile-service mirroring, "theme preference") |
| `Interpretation B` | — |
| `What could differ` | Everything about task 2.2: an agent must invent what a "preference bridge" is before it can wire anything through it |
| `Why context does not settle it` | The group heading ("Settings UI") and adjacent tasks name `ThemeToggle` and the theme preference, but nothing called a bridge; no design decision or file-change entry introduces one |
| `Evidence` | tasks.md Task 2.2 against all audited artifacts and the base spec |
| `Terminology decision` | Unresolved — name the established thing meant, or introduce "preference bridge" in the design first |

## 6. Settled Classification Table

Symbols: `●` supported and unambiguous · `○` benign variation · `△` one word or shorthand with two meanings (`AMB-POLY`/`AMB-SCENT`) · `✕` two words for one thing (`AMB-SYN`) · `?` a name nothing establishes (`AMB-GHOST`). Spec position: `behavioral` = normative or executable text · `contextual` = supporting prose.

| Concept | Wording found | Judgment | Spec position | Wording to use |
| --- | --- | --- | --- | --- |
| Stored light/dark choice | "appearance setting" (base spec); "theme preference" (proposal, delta, tasks) | `✕` | behavioral | appearance setting |
| Persistence requirement title | "Setting Persistence" (base); "Preference Persistence" (delta MODIFIED) | `✕` | behavioral | Setting Persistence |
| Holder of the stored choice | "DisplayModeStore" (design, tasks) vs. unnamed spec-side storage | `✕` | behavioral | Unresolved |
| Task 2.2 referent | "the preference bridge" (tasks.md only) | `?` | behavioral | Unresolved |
| Toggle control | "ThemeToggle" (design, tasks), bridged to "manual theme preference toggle" (proposal) | `●` | behavioral | ThemeToggle |
| Dark option, informally | "a dark option", "match whatever look their machine is set to" (proposal Intent) | `○` | contextual | — |

The `●` row shows what a correct cross-register rename looks like — the
design states the bridge, so `ThemeToggle` is not drift. The `○` row is
proposal Intent prose, which is allowed its informal register.

## 7. Items Needing Stakeholder Input

1. **Sentence:** "A single `DisplayModeStore` owns the current selection" (design.md, Decision: DisplayModeStore over per-page state)
   **Competing meanings:** the store holds the appearance setting itself vs. a separate display-state object beside it.
   **Why unresolved:** no audited sentence maps the design name to the spec concept, and the design also mentions mirroring "it" to the profile service without naming what "it" is.
   **Decision needed:** add one bridge sentence to the design stating what `DisplayModeStore` holds, in the spec's vocabulary.

2. **Sentence:** "Wire the toggle through the preference bridge" (tasks.md, Task 2.2)
   **Competing meanings:** none — no audited source establishes a referent.
   **Why unresolved:** a ghost name cannot be resolved by picking among candidates; the author must say what was meant.
   **Decision needed:** replace "the preference bridge" with the established name intended (`DisplayModeStore`? the profile-service mirror?) or introduce and define it in `design.md` before tasks reference it.

## 8. Scope Limitation

This audit covers vocabulary ambiguity only, within the
`add-dark-mode` change folder and its base spec
`openspec/specs/appearance/spec.md`. It does not evaluate logical
consistency, requirement completeness, technical feasibility, or
implementation correctness.
