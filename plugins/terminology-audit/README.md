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
   coding agent as a prompt. Weighted toward structural spec elements
   (Given/When/Then, MUST/SHALL, interface names) and held to a strict
   evidence gate: a finding exists only when one quoted sentence has two
   evidence-supported readings that would change the implementation.
   Findings are classified with three IA-grounded rules — `AMB-SYN`
   (synonym conflict: different words, one concept), `AMB-POLY`
   (homograph collision: one word, two concepts), and `AMB-SCENT`
   (an abbreviation in normative text with two supported referents) —
   and tagged with a facet (object, field, state, command, …) so
   clusters show where a spec needs a definitions pass. Produces three
   deliverables: the audit report, led by a lint-style **Ambiguity
   Alerts** block (location, quoted fragment, and the exact decision
   needed); the termbase; and a machine-readable `ambiguity-alerts.csv`
   that a pre-commit hook, CI step, or agent harness can surface to the
   spec writer.

No bundled scripts or tooling in either skill — every deliverable is
written directly by the agent, so both run the same regardless of which
agent or environment is running them.

See each skill's `SKILL.md` for its full workflow, and
[`../../examples`](../../examples) in this repo for worked examples
(NASA solar-system docs + an Argo CD docs run for `terminology-audit`;
the job-scheduler spec in `examples/sample-sdd-dataset/` with outputs in
`examples/sample-reports/job-scheduler/` for `sdd-terminology-audit` —
the earlier timezone-utility outputs predate the current report format
and are kept for history).

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
