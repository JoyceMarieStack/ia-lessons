# ia-lessons

A Claude Code plugin marketplace repo. Currently distributes one plugin:

## Plugins

- **[terminology-audit](plugins/terminology-audit/)** — audits technical/
  engineering docs for inconsistent terminology and produces a termbase
  and a written audit report. No bundled scripts — pure judgment work,
  so it runs the same in any agent/environment.

## Install

```
/plugin marketplace add JoyceMarieStack/ia-lessons
/plugin install terminology-audit
```

## Examples

[`examples/`](examples/) has a worked walkthrough of the skill — sample
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
  sample-dataset/           # source docs used in the walkthrough
  sample-reports/           # generated termbase/report output
```
