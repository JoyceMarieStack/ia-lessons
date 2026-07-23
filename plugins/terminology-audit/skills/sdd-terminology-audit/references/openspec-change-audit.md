# Auditing an OpenSpec change folder

Read this when the audit scope is an OpenSpec change folder
(`openspec/changes/<change-id>/`) or any set of artifacts from one:
`proposal.md`, `design.md`, delta specs (`specs/<domain>/spec.md`), and
`tasks.md`. Everything in the core SKILL.md still applies — the evidence
gate, the rejection rules, the deliverables. This file adds what changes
when the scope is a chain of artifacts rather than one spec.

## Contents

1. The chain model — why artifact order matters
2. Cross-artifact authority order
3. Per-artifact profiles (proposal, delta specs, design, tasks)
4. The fourth rule: `AMB-GHOST`
5. Alert conventions for change folders

## 1. The chain model

OpenSpec artifacts form a dependency chain:

```
proposal ──► delta specs ──► design ──► tasks ──► implementation
             (normative)     (how)      (what the agent executes)
```

Terminology flows down this chain. The proposal *coins* terms, the delta
specs *normalize* them into SHALL statements, the design *maps* them to
implementation names, and the tasks *reference* them for an agent to act
on. This has two consequences for the audit:

- **Ambiguity is inherited.** A term that means two things in
  `proposal.md` will re-ambiguate every downstream artifact even after a
  downstream patch. So when the same ambiguity is visible in several
  artifacts, anchor the alert at the **earliest artifact where the term
  enters**, and mention the downstream echoes in the meanings sentence.
  Fixing the coinage fixes the chain; fixing `tasks.md` alone fixes one
  symptom.
- **Cross-artifact drift is the dominant failure.** Within one artifact,
  authors are usually consistent. The high-yield comparison is *between*
  artifacts: does `tasks.md` call things what the delta spec calls them?
  Does the design rename a spec concept without saying so? Audit the
  chain pairwise (proposal↔deltas, deltas↔design, design+deltas↔tasks),
  not each file in isolation.

## 2. Cross-artifact authority order

For a change folder, replace the core skill's authority list with:

1. Existing implementation identifiers, schemas, and public contracts.
2. Base specs in `openspec/specs/` — the already-archived truth the
   change is written against.
3. The change's own delta specs (normative SHALL text).
4. Explicit definitions in `proposal.md`.
5. Consistent usage across the change folder.

`design.md` is authoritative only for implementation-register names
(class, file, component names) — and only once it states the bridge to
the spec term (see the design profile below). `tasks.md` is never an
authority; it is where drift is detected, not where it is settled.

## 3. Per-artifact profiles

### `proposal.md` — where terms are born

Sections: `## Intent`, `## Scope` (In scope / Out of scope), `## Approach`.

Prioritize:

- **Names in the Scope bullets.** These are the highest-value sentences
  in the whole folder: an ambiguous term in a scope bullet makes the
  in/out boundary itself unenforceable. If "In scope: profile settings"
  and "Out of scope: account management" and the audited evidence
  supports profile = account, no downstream artifact can know which side
  a given field falls on.
- **New coinages vs. established vocabulary.** Check every concept name
  in Scope and Approach against the base specs in `openspec/specs/` and
  existing identifiers. A proposal that says "user account" for what the
  base specs call "profile" is `AMB-SYN` at the moment of coinage — the
  cheapest possible time to fix it.

Trap — do not flag: informal register in `## Intent`. Intent is
contextual prose (motivation, user pain); loose synonyms there are fine
*as long as* Scope and Approach use the established names. Classify
Intent-only variation `○`.

### Delta specs (`specs/<domain>/spec.md`) — the normative contract

Sections: `## ADDED Requirements`, `## MODIFIED Requirements`,
`## REMOVED Requirements`; requirements as `### Requirement: <name>`
with `#### Scenario:` blocks. Everything the core skill says about
normative text applies at full strength here. Two delta-specific checks:

- **Header-match integrity (mechanical, highest priority).** OpenSpec
  matches `MODIFIED` and `REMOVED` requirements to the base spec **by
  exact requirement header text** and replaces the whole block at
  archive time. A header that rewords the base spec's header —
  `### Requirement: Session Expiry` for the base's
  `### Requirement: Session Expiration` — reads as the same requirement
  to a human and as a *different* requirement to the tool: the archive
  merge adds a near-duplicate instead of replacing, and the old
  requirement survives. This is `AMB-SYN` with a mechanical failure
  attached; always inspect the base spec headers in `openspec/specs/`
  when a delta has MODIFIED/REMOVED sections, and quote both headers as
  the evidence pair.
- **Delta vocabulary vs. base vocabulary.** An `ADDED` requirement using
  a variant of a term the base spec in the same domain already
  established (`AMB-SYN`), or reusing a base term for a new concept
  (`AMB-POLY`), will be merged into that spec verbatim at archive time —
  the delta is not a scratchpad, it is a patch to the permanent record.

Also compare delta specs to each other: two domains' deltas in the same
change using different terms for one concept is exactly the drift an
agent implementing both will turn into two identifiers.

### `design.md` — where implementation names are chosen

Sections: `## Technical Approach`, `## Architecture Decisions`
(`### Decision:` blocks), `## Data Flow`, `## File Changes`.

Prioritize:

- **Unbridged renames.** A design will rightly introduce
  implementation-register names (`ThemeContext`, `SessionStore`) for
  spec-register concepts ("theme preference", "login state"). That is
  not a finding — *unless* the evidence supports that a design name and
  a spec name denote the same concept and no sentence states the
  mapping. Then it is `AMB-SYN` across registers: an agent executing
  tasks can create both a `SessionStore` and a `LoginState`, each
  half-implemented. The fix to propose is a bridge, not a merge: one
  sentence in the design ("`SessionStore` implements the login-state
  requirement") dissolves the finding.
- **`## File Changes` names.** These become literal paths and
  identifiers; treat them with the same weight as schema fields in the
  core skill.
- **Definite-article references.** "The cache", "the store", "the
  config" in Decision or Data Flow text when the design defines more
  than one candidate is `AMB-POLY` — quote the sentence with the bare
  definite reference.
- **Coined abbreviations.** An abbreviation minted in the design and
  reused in `tasks.md` is where `AMB-SCENT` findings in change folders
  usually originate.

Trap — do not flag: technical synonyms inside decision *rationale*
("we chose X because a client-side store is simpler than global state").
Rationale is contextual prose; only names that will become identifiers,
files, or task nouns carry implementation weight.

### `tasks.md` — where an agent greps for names

Structure: `## <group>` headings with `- [ ] N.M <task>` checklist items.

A task line is an instruction an agent executes by *finding the named
thing*. So the unit of audit is each load-bearing noun in each task, and
the question is: **does this name resolve to exactly one thing
established upstream** (delta specs, design, proposal) **or in the
existing codebase?** Three failure shapes:

- Resolves to an upstream name *via a new variant* — the task says
  "night mode toggle" where the proposal said "dark mode" and the design
  said `ThemeToggle` — a third name for the concept: `AMB-SYN`, anchored
  at the earliest artifact that let the variant in.
- Resolves to *more than one* upstream referent — "update the config
  file" in a change that touches both `config.yaml` and a tool rule
  file: `AMB-POLY`.
- Resolves to *nothing* upstream: `AMB-GHOST` — see section 4.

Trap — do not flag: task shorthand that is an unambiguous truncation of
an established name in its group context ("1.2 Add CSS custom
properties" under `## Theme Infrastructure` does not need spec
vocabulary), and pure verb phrasing ("wire up", "clean up") — verbs are
execution style, not vocabulary.

## 4. The fourth rule: `AMB-GHOST`

| Rule | Plain name | Symbol | What broke |
| --- | --- | --- | --- |
| `AMB-GHOST` | A name nothing establishes | `?` | A task or design sentence uses a name as if it were already defined, but no audited artifact, base spec, or inspected identifier establishes a referent for it. Every implementation of that line is a guess. |

`AMB-GHOST` exists because the core gate requires *two* evidence-
supported meanings — and a ghost name has zero. It applies **only in
multi-artifact audits** (change folders), where "upstream" is well
defined. Adapt the gate for it:

1. Quote the exact task or design sentence using the name.
2. Show that you searched every upstream artifact in scope, the base
   specs, and any inspected authority sources, and found no referent —
   list the nearest near-miss names you did find (or `none`).
3. Confirm the name is load-bearing: implementing the line requires
   knowing what it denotes.
4. Confirm nearby context (the task's group heading, adjacent tasks)
   does not resolve it.

In `ambiguity-alerts.csv`, a ghost row puts the near-miss candidates in
`meaning_a` (or `none found`), `—` in `meaning_b`, and `unresolved` in
`supported_wording`. The `Decide:` question is always some form of:
"which established name is this, or should it be introduced upstream
first?" — because the fix is either a rename in `tasks.md` or a new
definition in the proposal/design/delta, never both.

Do not stretch `AMB-GHOST` into completeness review: it fires on a
*name* with no referent, not on missing steps, missing requirements, or
work the tasks forgot. If the sentence would still be unclear after the
name was defined, the problem is not terminology — omit it.

## 5. Alert conventions for change folders

- **Anchors:** use the requirement header for delta specs
  (`Requirement: Session Expiration`), the decision header for design
  (`Decision: Context over Redux`), the section for proposals
  (`Scope › In scope`), and the task number for tasks (`Task 2.1`).
- **Anchor at the source, echo the rest.** When one ambiguity surfaces
  in several artifacts, one alert, anchored at the earliest artifact
  where the term enters; name the downstream artifacts in the meanings
  sentence. Do not emit one alert per artifact for the same finding —
  the writer fixes the coinage once.
- **Facet rollup by artifact too.** In change-folder audits, close the
  rollup with one plain sentence on *where in the chain* findings
  concentrate (e.g., "all three enter at proposal.md — the delta specs
  and tasks inherit them"), since that tells the writer which single
  file most needs the fix.
- The Summary's file list groups files by artifact type so a reader can
  see at a glance which parts of the chain were in scope, and gains one
  extra count line: number of `?` findings (`AMB-GHOST`, a name nothing
  establishes).
