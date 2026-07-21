# markdown-ia

A Claude Code plugin for information-architecture analysis of Markdown
documentation corpora (a git repo or folder of `.md`/`.mdx` files).

1. **[markdown-docs-corpus-discovery](skills/markdown-docs-corpus-discovery/SKILL.md)**
   — first-pass reconnaissance. Answers what exists, how it's organized,
   what's missing, and how mature the corpus is: file/directory counts,
   nav-config vs. folder-structure comparison, git provenance signals,
   and a sampled read of representative files. Scoped to Markdown only
   and stays at the level of directories and freshness signals — it does
   not classify documents into types or infer a schema.

This is the first skill in a planned IA analysis suite. Later skills
(content modeling, vocabulary governance) will build on its output once
they land in this plugin.

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
    └── markdown-docs-corpus-discovery/
        └── SKILL.md
```
