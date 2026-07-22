# ia-lessons

A Claude Code plugin marketplace repo for information-architecture skills:
auditing what a documentation corpus actually contains, standardizing the
vocabulary it uses, and then enforcing that vocabulary downstream in
spec-driven development.

The underlying premise: you can't organize, label, or navigate content you
haven't actually looked at.

## Repo layout

```
ia-lessons/
├── .claude-plugin/marketplace.json   # marketplace manifest (two plugins)
├── plugins/
│   ├── markdown-ia/                  # IA analysis for Markdown corpora
│   │   └── skills/
│   │       ├── markdown-docs-corpus-discovery/
│   │       ├── markdown-content-model-discovery/
│   │       └── markdown-vocabulary-governance/
│   └── terminology-audit/            # terminology auditing → termbase
│       └── skills/
│           ├── terminology-audit/
│           └── sdd-terminology-audit/
├── vocabulary-contract/              # standalone skill: termbase → naming contract
├── test-fixtures/                    # known-answer fixtures for vocabulary-contract
├── examples/                         # sample datasets and worked reports
└── vocabulary-contract-workspace/    # eval results + packaged .skill artifact
```

## Plugins

### markdown-ia

Information-architecture analysis for Markdown documentation corpora. Three
skills, answering three questions:

- **Corpus discovery** — how much content exists, what shape it is in, and
  whether it is maintained or abandoned.
- **Content model discovery** — a content model is what IA people mean by
  "organization systems" made concrete: what types of docs exist, what
  structure each type follows, what metadata each carries.
- **Vocabulary governance** — two IA concerns at once: labeling (are we
  calling the same thing by the same name — ApplicationSet vs Application
  Set?) and organization via facets/taxonomy (is there a controlled way to
  classify content — tags, categories — or is folder placement the only
  signal?).

Together these answer: what exists, what shape it has, and what words and
categories are already in use to describe it.

### terminology-audit

Audits technical/engineering docs — or spec-driven-development (SDD) spec
files — for inconsistent terminology, producing a **termbase** (a CSV of
preferred terms, banned variants, definitions, and statuses), a written audit
report, and, for SDD specs (`sdd-terminology-audit`), lint-style ambiguity
alerts pointing spec writers at the exact sentence to clarify.

## Standalone skill: vocabulary-contract

Consumes the `termbase.csv` a terminology audit produces (but depends only on
the CSV) and turns it into an enforceable naming contract for spec-driven
workflows (proposal → spec → tasks → implementation). Three modes:

- **Render** — generate an AGENTS.md / CLAUDE.md vocabulary fragment in
  imperative prose (canonical term, banned variants, per-surface forms: code
  identifier, file name, CLI flag, env var) plus a compact spec-preamble
  block.
- **Enforce** — check a draft spec/proposal/tasks file against approved terms;
  advisory findings with file, line, quoted sentence, and suggested rewrite.
  A clean pass is reported explicitly, never silently.
- **Round-trip** — after an implementation, surface recurring domain terms not
  yet in the termbase as candidates (counts + locations) for the next
  revision. The termbase itself is never modified.

Deterministic matching lives in `vocabulary-contract/scripts/check_terms.py`
(word-boundary aware, prose and code-form variants, code-fence/backtick
context); interpretation and reporting are left to the model. `test-fixtures/`
holds the known-answer fixtures the skill was validated against, and
`vocabulary-contract-workspace/` contains the eval results and the packaged
`vocabulary-contract.skill` file.

## Examples

- `examples/sample-dataset/` — NASA planet pages (public domain): a small,
  fully readable corpus with a real terminology conflict baked in (Pluto's
  2006 reclassification), a near-synonym pair (moon vs satellite), and an
  accepted stylistic variant (Mars vs the Red Planet).
- `examples/sample-sdd-dataset/` — a job-scheduler spec for SDD-flavored runs.
- `examples/sample-reports/` — worked outputs from real runs: termbases and
  audit reports for the planets, job-scheduler, and timezone-utility corpora,
  ambiguity alerts for the job-scheduler spec, and corpus-discovery /
  content-model / vocabulary-governance reports for Argo CD's docs.

See `examples/README.md` for why these datasets make good test corpora and a
concept-by-concept walkthrough of controlled vocabulary management.

## How the pieces fit

1. **Discover** what exists and how it's organized (`markdown-ia`).
2. **Audit** the words in use and settle on canonical terms
   (`terminology-audit` → `termbase.csv`).
3. **Enforce** those decisions in every new spec, and **round-trip** newly
   coined terms back into the termbase (`vocabulary-contract`).
