# Spec: Schema Extension Behavior

## Overview

When a project defines its own schema, the loader runs in extension mode and
combines it with the base schema fetched from the schema registry.

## Requirements

- FR-001: The loader MUST read `config.yaml` from the project root before any
  validation pass begins.
- FR-002: If a local schema override is present, it is applied after the base
  schema loads.
- FR-003: Switching to extension mode MUST NOT change the merge policy.

## Notes

This began as a proposal draft and still needs acceptance criteria.
