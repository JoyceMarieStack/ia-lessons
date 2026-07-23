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
├── LICENSE
├── plugins/
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

## Adding a plugin

Every `plugins/<name>/` directory needs a matching entry in
`.claude-plugin/marketplace.json` — that's what makes it installable via
`/plugin install`. It's easy to build out a plugin's `skills/`, `evals/`,
and `plugin.json` and forget the marketplace entry, so after adding one,
verify nothing's missing:

```bash
comm -23 \
  <(ls plugins | sort) \
  <(jq -r '.plugins[].name' .claude-plugin/marketplace.json | sort)
```

Empty output means every plugin directory has a marketplace entry. Any
name it prints is a plugin that exists on disk but isn't registered yet.

## Plugins

**markdown-ia** (information-architecture analysis for Markdown
documentation corpora — corpus discovery, content-model discovery,
vocabulary governance) moved to its own repo, `markdown-ia-skills`, since
it has no dependency on the terminology-audit → vocabulary-contract
pipeline the other two plugins here form together. Install it from that
repo directly rather than from `ia-lessons`.

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
  and ambiguity alerts for the job-scheduler spec. These double as golden
  references for the evals above and as show-don't-tell examples for anyone
  deciding whether to install a skill. (The timezone-utility report predates
  the current report format and is kept for history — see
  `plugins/terminology-audit/README.md`. The Argo CD corpus-discovery /
  content-model / vocabulary-governance reports moved to `markdown-ia-skills`
  along with the skills that produced them.)

See `examples/README.md` for why these datasets make good test corpora and a
concept-by-concept walkthrough of controlled vocabulary management.

## Tests

Every plugin has an `evals/evals.json` — eval prompts plus assertions, in the
format the `skill-creator` skill's eval loop consumes — under its `evals/`
directory. Run them the same way vocabulary-contract's were validated: spawn
an agent per eval prompt pointed at the skill, check the assertions against
its output.

The assertion style differs by how checkable each skill's output is:

- **vocabulary-contract** and **terminology-audit** produce structured or
  format-constrained output (a CSV with a fixed column set, a specific report
  section list, known planted findings in the fixtures), so their assertions
  can be exact and mechanically graded — `vocabulary-contract/evals/grade.py`
  is a worked example of a programmatic grader. Even here, exact-match
  assertions on *which* findings a judgment-based skill catches
  (`sdd-terminology-audit`) turned out to overfit one run's output — a real
  spec can have more genuine ambiguities than any one pass will surface, so
  those assertions check for internal consistency and the one
  always-must-catch finding, not an exact checklist.

`markdown-ia`'s evals (structure-only assertions over first-pass analysis,
self-scanning its own repo as fixture) now live in `markdown-ia-skills`,
not here.

Eval run outputs, the description-optimization log/report, and packaged
`.skill` files are regenerated, not committed — see `.gitignore`.

## How the pieces fit

`markdown-ia` (now in its own repo) is a standalone reconnaissance tool —
useful before or independent of the pipeline below, not a required first
step in it:

1. **Audit** the words in use and settle on canonical terms — pick
   `terminology-audit` for docs or `sdd-terminology-audit` for specs
   (`termbase.csv` either way).
2. **Enforce** those decisions in every new spec, and **round-trip** newly
   coined terms back into the termbase (`vocabulary-contract`).

## License

[MIT](LICENSE).
