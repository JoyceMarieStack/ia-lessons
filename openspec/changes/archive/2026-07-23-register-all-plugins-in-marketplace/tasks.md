## 1. Verify each plugin's own packaging

- [x] 1.1 Confirm `plugins/terminology-audit/.claude-plugin/plugin.json` is valid JSON, `name` matches the folder name, and `description` accurately reflects the skills in `plugins/terminology-audit/skills/`
- [x] 1.2 Confirm `plugins/vocabulary-contract/.claude-plugin/plugin.json` is valid JSON, `name` matches the folder name, and `description` accurately reflects the skills in `plugins/vocabulary-contract/skills/`
- [x] 1.3 Re-confirm `plugins/markdown-ia/.claude-plugin/plugin.json` still matches its current skills (baseline check, since it's already registered)

## 2. Register missing plugins in the marketplace

- [x] 2.1 Add a `terminology-audit` entry to `.claude-plugin/marketplace.json`'s `plugins` array with `name`, `source: "./plugins/terminology-audit"`, and `description` sourced from its `plugin.json` — already present (commit c07c98e, prior to this change's implementation)
- [x] 2.2 Add a `vocabulary-contract` entry to `.claude-plugin/marketplace.json`'s `plugins` array with `name`, `source: "./plugins/vocabulary-contract"`, and `description` sourced from its `plugin.json` — already present (commit b540805, prior to this change's implementation)
- [x] 2.3 Validate `.claude-plugin/marketplace.json` is still well-formed JSON after edits

## 3. Document the verification check

- [x] 3.1 Add a short section (README at repo root, or a comment near `marketplace.json`) documenting a one-line check — e.g. comparing `plugins/*/.claude-plugin/plugin.json` names against `marketplace.json`'s `plugins[].name` — that a contributor can run after adding a new plugin
- [x] 3.2 Run that check against the current repo state and confirm it reports zero missing entries
