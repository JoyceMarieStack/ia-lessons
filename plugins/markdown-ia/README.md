# markdown-ia

A Claude Code plugin for information-architecture analysis of Markdown
documentation corpora (a git repo or folder of `.md`/`.mdx` files).

Three skills, meant to run in sequence:

1. **[markdown-docs-corpus-discovery](skills/markdown-docs-corpus-discovery/SKILL.md)**
   — first-pass reconnaissance. Answers what exists, how it's organized,
   what's missing, and how mature the corpus is: file/directory counts,
   nav-config vs. folder-structure comparison, git provenance signals,
   and a sampled read of representative files. Scoped to Markdown only
   and stays at the level of directories and freshness signals — it does
   not classify documents into types or infer a schema.

2. **[markdown-content-model-discovery](skills/markdown-content-model-discovery/SKILL.md)**
   — infers the implicit content model (document types, common sections,
   metadata fields) without a predefined schema. Produces recommended
   content types, a per-type schema of required/optional metadata, and
   validation rules, with missing-metadata findings calibrated by
   document type (governance artifacts like standards/policies/ADRs
   held to a real bar; reference content like CLI docs or how-tos not
   penalized for lacking it).

3. **[markdown-vocabulary-governance](skills/markdown-vocabulary-governance/SKILL.md)**
   — analyzes terminology, tagging, and taxonomy consistency, producing
   two independent artifacts: Vocabulary Governance (canonical terms
   with a four-way ambiguity classification, synonyms, preferred
   spellings, naming conventions, deprecation rules) and Taxonomy
   Design (classification facets, allowed values, hierarchies, metadata
   schema, facet governance).

Each skill runs with general-purpose tools (`find`, `grep`, direct file
reading) rather than a bundled script, and can also be run standalone if
you only need one piece of the analysis.

See [examples/sample-reports](../../examples/sample-reports/argo-cd) for
sample output from all three skills run against a real corpus.

## Install

```
/plugin marketplace add JoyceMarieStack/ia-lessons
/plugin install markdown-ia
```

## What's inside

```
markdown-ia/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    ├── markdown-docs-corpus-discovery/
    │   └── SKILL.md
    ├── markdown-content-model-discovery/
    │   └── SKILL.md
    └── markdown-vocabulary-governance/
        └── SKILL.md
```
