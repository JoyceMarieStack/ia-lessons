## Why

This repo hosts three Claude Code plugins (`markdown-ia`, `terminology-audit`,
`vocabulary-contract`), each with its own valid `plugin.json` and README, but
`.claude-plugin/marketplace.json` — the file that actually makes a plugin
installable via `/plugin install` — only registers `markdown-ia`. The other
two plugins are fully built but effectively invisible to anyone using this
repo as a marketplace. There's also no repeatable check that catches this
kind of drift when a new plugin is added later.

## What Changes

- Add marketplace entries for `terminology-audit` and `vocabulary-contract` to
  `.claude-plugin/marketplace.json`, matching the existing `markdown-ia` entry's
  shape (`name`, `source`, `description`).
- Source each new entry's `description` from that plugin's own `plugin.json`
  description (kept in sync, not re-authored independently).
- Verify all three plugins' `plugin.json` files are internally consistent
  (valid JSON, name matches folder name, description accurately reflects the
  skills the plugin ships) before registering them.
- Add a lightweight verification step (documented, not necessarily scripted)
  for confirming every `plugins/*/` directory has a corresponding
  `marketplace.json` entry, so this doesn't silently drift again.

## Capabilities

### New Capabilities
- `plugin-marketplace-registration`: every plugin under `plugins/` is
  discoverable and installable through `.claude-plugin/marketplace.json`, and
  that stays true as plugins are added.

### Modified Capabilities
(none — no existing specs in this repo)

## Impact

- Affected file: `.claude-plugin/marketplace.json` (two new entries added).
- Affected files (read-only verification, edits only if inconsistencies are found):
  `plugins/terminology-audit/.claude-plugin/plugin.json`,
  `plugins/vocabulary-contract/.claude-plugin/plugin.json`,
  `plugins/markdown-ia/.claude-plugin/plugin.json`.
- No code or skill behavior changes — this is a packaging/discoverability fix.
- No breaking changes.
