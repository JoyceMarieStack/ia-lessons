# plugin-marketplace-registration

## Purpose

TBD - defines the requirements for keeping every plugin under `plugins/`
registered in the root `.claude-plugin/marketplace.json`, consistent with
each plugin's own metadata, and verifiable via a documented check.

## Requirements

### Requirement: Every plugin directory has a marketplace entry
Every directory under `plugins/` that contains a valid `.claude-plugin/plugin.json`
SHALL have a corresponding entry in the root `.claude-plugin/marketplace.json`
`plugins` array, identified by matching `name`.

#### Scenario: Plugin exists but is unregistered
- **WHEN** a directory `plugins/<name>/.claude-plugin/plugin.json` exists
- **THEN** `.claude-plugin/marketplace.json` contains an entry in `plugins`
  with `"name": "<name>"`

#### Scenario: New plugin added later
- **WHEN** a new plugin directory is added under `plugins/` with its own
  `plugin.json`
- **THEN** it is not considered fully packaged until a matching entry is
  added to `.claude-plugin/marketplace.json`

### Requirement: Marketplace entry fields are consistent with the plugin's own metadata
Each marketplace entry's `source` SHALL point at the plugin's directory
(`./plugins/<name>`), and its `description` SHALL describe the same
capabilities as the plugin's own `plugin.json` `description` (not
necessarily verbatim, but not contradicting or omitting a skill the plugin
ships).

#### Scenario: Marketplace description omits a shipped skill
- **WHEN** a plugin's `plugin.json` description references a skill that the
  plugin's `skills/` directory contains
- **THEN** the marketplace entry's `description` does not contradict or
  silently drop that skill

### Requirement: Marketplace registration is verifiable
There SHALL be a documented, repeatable way to check that every
`plugins/*/.claude-plugin/plugin.json` has a matching `marketplace.json`
entry, so future plugin additions don't silently go unregistered.

#### Scenario: Contributor adds a plugin and wants to verify registration
- **WHEN** a contributor finishes adding a new plugin directory
- **THEN** they can run a documented check (command or documented manual
  steps) that reports any `plugins/*/` directory missing a
  `marketplace.json` entry
