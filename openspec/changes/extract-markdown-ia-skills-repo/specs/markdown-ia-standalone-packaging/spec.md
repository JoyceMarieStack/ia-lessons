## ADDED Requirements

### Requirement: markdown-ia-skills is self-contained
The `markdown-ia-skills` repo SHALL contain everything needed to install
and run its three skills without reference to `ia-lessons` — its own
`.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` at repo
root, `skills/`, `evals/`, `README.md`, and `LICENSE`, with no relative
paths or links pointing back into `ia-lessons`. `examples/sample-dataset/`
(the NASA planets fixture) is explicitly excluded — it belongs to
`terminology-audit`, not markdown-ia.

#### Scenario: Plugin installed from markdown-ia-skills alone
- **WHEN** a user runs `/plugin marketplace add` pointed at
  `markdown-ia-skills` and then `/plugin install`
- **THEN** all three skills (`markdown-docs-corpus-discovery`,
  `markdown-content-model-discovery`, `markdown-vocabulary-governance`)
  are available with no missing files or broken references to `ia-lessons`

#### Scenario: Marketplace entry matches the plugin
- **WHEN** `markdown-ia-skills/.claude-plugin/marketplace.json` is read
- **THEN** it contains exactly one entry, whose `name` matches
  `.claude-plugin/plugin.json`'s `name` and whose `source` resolves to the
  repo root

#### Scenario: README no longer links into ia-lessons
- **WHEN** `markdown-ia-skills/README.md` references its own worked
  examples (e.g. the Argo CD sample reports)
- **THEN** the link points inside `markdown-ia-skills` (e.g.
  `examples/sample-reports/argo-cd/`), not `../../examples/...` back into
  `ia-lessons`

### Requirement: ia-lessons has no residual markdown-ia references
After extraction, `ia-lessons` SHALL NOT reference `markdown-ia` as an
installable plugin, a marketplace entry, or a live file path.

#### Scenario: Marketplace no longer offers markdown-ia
- **WHEN** a user reads `.claude-plugin/marketplace.json` in `ia-lessons`
- **THEN** it lists only `terminology-audit` and `vocabulary-contract`

#### Scenario: Root README doesn't link to removed files
- **WHEN** a user reads `ia-lessons`'s root `README.md`
- **THEN** it does not link to `plugins/markdown-ia/` or
  `examples/sample-reports/argo-cd/` (both removed), and any mention of
  markdown-ia states it moved to its own repo rather than describing it
  as installable from `ia-lessons`

### Requirement: markdown-ia's evals fixture matches its new repo
The eval self-scan fixture and assertions SHALL describe
`markdown-ia-skills` itself, not assumptions inherited from scanning
`ia-lessons`'s multi-plugin structure.

#### Scenario: Self-scan assertions don't assume multi-plugin structure
- **WHEN** `markdown-ia-skills/evals/evals.json`'s assertions are read
- **THEN** they don't require findings that only made sense in
  `ia-lessons` (e.g. "plugin vs skill" terminology tension across three
  plugins) unless verified to still hold true when the skill is actually
  run against `markdown-ia-skills`
