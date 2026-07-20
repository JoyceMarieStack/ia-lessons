# terminology-audit

A Claude Code plugin with two skills that audit terminology and produce a
termbase + a written audit report:

1. **[terminology-audit](skills/terminology-audit/SKILL.md)** — for human-
   facing technical/engineering docs (READMEs, API references, guides).
   Produces a **termbase** (structured glossary of preferred terms —
   definition, part of speech, usage context, forbidden variants —
   formatted close to what TMS/CAT localization tools expect) and an
   **audit report** (what's inconsistent, why it matters, which conflict
   matters most, which source is most precise).
2. **[sdd-terminology-audit](skills/sdd-terminology-audit/SKILL.md)** — for
   spec-driven-development (SDD) spec files that get handed to an AI
   coding agent as a prompt. Same two deliverables, but weighted toward
   structural spec elements (Given/When/Then, MUST/SHALL, interface
   names) and held to a stricter bar: the termbase must have zero
   unresolved rows before it's agent-ready.

No bundled scripts or tooling in either skill — every deliverable is
written directly by the agent, so both run the same regardless of which
agent or environment is running them.

See each skill's `SKILL.md` for its full workflow, and
[`../../examples`](../../examples) in this repo for worked examples
(NASA solar-system docs + an Argo CD docs run for `terminology-audit`;
a spec-kit-generated feature spec for `sdd-terminology-audit`).

## Install

```
/plugin marketplace add JoyceMarieStack/ia-lessons
/plugin install terminology-audit
```

## What's inside

```
terminology-audit/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    ├── terminology-audit/
    │   └── SKILL.md
    └── sdd-terminology-audit/
        └── SKILL.md
```
