# ia-lessons

A Claude Code plugin marketplace for information-architecture work on
documentation corpora.

You can't organize, label or navigate content you haven't actually looked at.

* Corpus Discovery -  how much content, what shape is it in, is it maintained or abandoned.
* Content Model Discovery - A content model is what IA people mean when they talk about 'organisation systems' made concrete: what types of docs exist, what structure each type follows, what metadata each carries.
* Vocabularly Governance - This is two IA concerns at once: labeling (are we calling the same thing by the same name — ApplicationSet vs Application Set) and organization via facets/taxonomy (is there a controlled way to classify content — tags, categories — or is folder placement the only signal)

These three things answer: what exists, what shape it has and what words and categories are already in use to describe it.

## Plugins in this marketplace

* **[markdown-ia](plugins/markdown-ia/)** — corpus discovery, content-model
  inference, and vocabulary/taxonomy governance for Markdown documentation
  corpora. Three skills, meant to run in sequence.
* **[terminology-audit](plugins/terminology-audit/)** — audits technical/
  engineering docs (or SDD spec files) for inconsistent terminology and
  produces a termbase and a written audit report. Two skills: one for
  human-facing docs, one retargeted at spec-driven-development specs with
  a stricter agent-ready bar.

See each plugin's README for its full skill list and worked examples.

## Install

```
/plugin marketplace add JoyceMarieStack/ia-lessons
/plugin install markdown-ia@ia-lessons
/plugin install terminology-audit@ia-lessons
``` 


