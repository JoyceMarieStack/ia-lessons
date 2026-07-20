# terminology-audit

A Claude Code skill that audits technical/engineering docs for inconsistent
terminology and produces two deliverables:

1. **Termbase** — a structured glossary of preferred terms (definition,
   part of speech, usage context, forbidden variants), formatted close to
   what TMS/CAT localization tools expect.
2. **Audit report** — a written summary of what's inconsistent, why it
   matters, and what to do about it, including which conflict matters most
   and which source uses terms most precisely.

No bundled scripts or tooling — every deliverable is written directly by
the agent, so the skill runs the same regardless of which agent or
environment is running it.

See [`skills/terminology-audit/SKILL.md`](skills/terminology-audit/SKILL.md)
for the full workflow the skill follows, and
[`../../examples`](../../examples) in this repo for a worked example
(NASA solar-system docs + an Argo CD docs run) with real output.

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
    └── terminology-audit/
        └── SKILL.md
```
