# ia-lessons

A Claude Code plugin marketplace repo. Currently distributes two plugins:

## Plugins

- **[terminology-audit](plugins/terminology-audit/)** — two skills, no
  bundled scripts (pure judgment work, so it runs the same in any agent/
  environment):
  - `terminology-audit` — audits human-facing technical/engineering docs
    for inconsistent terminology and produces a termbase and a written
    audit report.
  - `sdd-terminology-audit` — the same audit, retargeted at
    spec-driven-development (SDD) spec files handed to an AI coding
    agent as a prompt, with a stricter completion bar (zero unresolved
    termbase rows) before the spec is considered agent-ready.
- **[markdown-ia](plugins/markdown-ia/)** — information-architecture
  analysis for Markdown documentation corpora:
  - `markdown-docs-corpus-discovery` — first-pass reconnaissance of a
    Markdown corpus (file/directory counts, nav-config vs. folder
    structure, git provenance, freshness/maturity signals) before
    deeper IA work begins.

## Install

```
/plugin marketplace add JoyceMarieStack/ia-lessons
/plugin install terminology-audit
/plugin install markdown-ia
```

## Examples

[`examples/`](examples/) has a worked walkthrough of both skills — sample
source docs, real generated output, and notes tying the results back to
information-architecture concepts (controlled vocabulary, synonymy vs.
polysemy, etc.) and to spec-driven-development workflows.

## Repo layout

```
.claude-plugin/
  marketplace.json          # lists the plugins this repo distributes
plugins/
  terminology-audit/        # the plugin itself
examples/
  README.md                 # walkthrough notes
  sample-dataset/           # source docs used in the terminology-audit walkthrough
  sample-reports/           # generated termbase/report output
  sample-sdd-dataset/       # sample spec files used in the sdd-terminology-audit walkthrough
```
