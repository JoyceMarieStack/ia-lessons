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
├── .claude-plugin/marketplace.json   # marketplace manifest (three plugins)
├── LICENSE
├── plugins/
│   ├── markdown-ia/                  # IA analysis for Markdown corpora
│   │   └── skills/
│   │       ├── markdown-docs-corpus-discovery/
│   │       ├── markdown-content-model-discovery/
│   │       └── markdown-vocabulary-governance/
│   ├── terminology-audit/            # terminology auditing → termbase
│   │   ├── skills/
│   │   │   ├── terminology-audit/          # for human-facing docs
│   │   │   └── sdd-terminology-audit/      # for SDD spec files
│   │   └── evals/                    # eval prompts + assertions for both skills
│   └── vocabulary-contract/          # termbase.csv → naming contract
│       ├── skills/vocabulary-contract/
│       │   └── test-fixtures/        # known-answer fixtures
│       └── evals/                    # eval prompts, grader, trigger-eval set
└── examples/                         # shared sample datasets and worked reports
```

Each plugin's own README has the detail; this file is the map.

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

**Two independent skills for two different inputs — they don't chain, and
each produces its own `termbase.csv` with a different column set.** Pick the
one that matches what you're auditing:

- **terminology-audit** — for human-facing docs (READMEs, API references,
  guides, wikis). Produces a termbase (with a `status` column: `approved` /
  `needs stakeholder input` / `provisional`) and a written audit report.
- **sdd-terminology-audit** — for spec-driven-development spec files
  (spec-kit, OpenSpec, Given/When/Then, MUST/SHALL requirements). Produces
  lint-style ambiguity alerts (`AMB-SYN` / `AMB-POLY` / `AMB-SCENT`) pointing
  at the exact sentence to clarify, a resolved-only termbase (no `status`
  column — unresolved concepts are omitted, not flagged), and a
  machine-readable `ambiguity-alerts.csv` for CI or pre-commit hooks.

### vocabulary-contract

Consumes a `termbase.csv` — from either terminology-audit skill above, or
hand-maintained — and turns it into an enforceable naming contract for
spec-driven workflows (proposal → spec → tasks → implementation). It depends
only on the CSV, not on whatever produced it. Three modes: **render** (an
AGENTS.md/CLAUDE.md vocabulary fragment plus a spec-preamble block),
**enforce** (advisory findings against a draft spec/proposal/tasks file, with
suggested rewrites), and **round-trip** (after an implementation, propose new
recurring terms for the next termbase revision — never writes the termbase
itself).

## Examples

`examples/` is not just illustrative — it's the fixture data the plugins'
evals run against:

- `examples/sample-dataset/` — NASA planet pages (public domain): a small,
  fully readable corpus with a real terminology conflict baked in (Pluto's
  2006 reclassification, which should NOT be flagged as inconsistency — it's
  a legitimate definitional change), a near-synonym pair (moon vs
  satellite), and an accepted stylistic variant (Mars vs the Red Planet).
  Used by `terminology-audit`'s evals.
- `examples/sample-sdd-dataset/` — a job-scheduler spec with three planted
  ambiguities (task/job synonym conflict, an underspecified TTL reference, an
  overloaded "schedule" field). Used by `sdd-terminology-audit`'s evals.
- `examples/sample-reports/` — worked outputs from real runs: termbases and
  audit reports for the planets, job-scheduler, and timezone-utility corpora,
  ambiguity alerts for the job-scheduler spec, and corpus-discovery /
  content-model / vocabulary-governance reports for Argo CD's docs. These
  double as golden references for the evals above and as show-don't-tell
  examples for anyone deciding whether to install a skill. (The
  timezone-utility report predates the current report format and is kept for
  history — see `plugins/terminology-audit/README.md`.)

See `examples/README.md` for why these datasets make good test corpora and a
concept-by-concept walkthrough of controlled vocabulary management.

## Tests

Each skill that produces structured, checkable output (a CSV, a specific
report format) has an `evals/evals.json` — eval prompts plus assertions, in
the format the `skill-creator` skill's eval loop consumes — under its
plugin's `evals/` directory. Run them the same way vocabulary-contract's were
validated: spawn an agent per eval prompt pointed at the skill, grade the
assertions against its output. `vocabulary-contract/evals/grade.py` is a
worked example of a programmatic grader. Eval run outputs, the
description-optimization log/report, and packaged `.skill` files are
regenerated, not committed — see `.gitignore`.

## How the pieces fit

1. **Discover** what exists and how it's organized (`markdown-ia`).
2. **Audit** the words in use and settle on canonical terms — pick
   `terminology-audit` for docs or `sdd-terminology-audit` for specs
   (`termbase.csv` either way).
3. **Enforce** those decisions in every new spec, and **round-trip** newly
   coined terms back into the termbase (`vocabulary-contract`).

## License

[MIT](LICENSE).
