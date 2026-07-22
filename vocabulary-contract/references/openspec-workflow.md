# Where each mode fits in a spec-driven workflow

Spec-driven development (OpenSpec-style) moves through four artifacts, each
derived from the last:

```
proposal ──> spec ──> tasks ──> implementation
   ▲                                  │
   └────── termbase revision <────────┘
```

Terminology drift compounds at every arrow: a variant that slips into the
proposal gets copied into the spec, turned into identifiers in the tasks, and
frozen into public API names in the implementation. The vocabulary contract
inserts a check at each hand-off.

## Proposal stage → Render

Before (or while) drafting a proposal, render the termbase:

- Paste the **spec preamble block** at the top of the proposal so authors and
  reviewing agents see the binding vocabulary without leaving the document.
- Merge the **AGENTS.md / CLAUDE.md fragment** into the repo's agent context so
  any agent drafting or editing project documents inherits the contract
  automatically.

Re-render whenever the termbase changes; the fragments cite termbase rows, so
stale copies are easy to detect.

## Spec and tasks stages → Enforce

Run enforce mode on each draft before it is accepted as the input to the next
stage — proposal before it becomes a spec, spec before tasks are cut, tasks
before implementation starts. Early enforcement is cheap: renaming a phrase in
a spec is a one-line edit; renaming it after implementation is a refactor plus
a migration note.

Enforcement is advisory. The author sees findings with suggested rewrites and
decides; a "violation" is sometimes the first sighting of a genuinely better
term — which belongs in the next termbase revision, not suppressed.

## Implementation stage → Round-trip

Implementation always coins vocabulary the spec didn't anticipate: helper
concepts, internal mechanisms, operational states. After implementation (or on
a PR diff), run round-trip mode to:

- surface recurring new domain terms as **candidates** for the next termbase
  revision, with counts and locations;
- catch near-synonyms of existing terms early, before they fork into drift.

Candidates go to a human for approval — typically entering the termbase with
status `candidate`, promoted to `approved` once the owners sign off. The next
render then closes the loop: the new vocabulary becomes binding for the next
proposal.

## Cadence summary

| Stage | Mode | Trigger |
|-------|------|---------|
| Repo setup / termbase change | Render | termbase.csv added or edited |
| Proposal draft | Enforce | before review |
| Spec draft | Enforce | before tasks are cut |
| Tasks draft | Enforce | before implementation |
| Implementation / PR | Round-trip | before merge or during review |
| Termbase revision | (human) | approve/reject candidates, then re-render |
