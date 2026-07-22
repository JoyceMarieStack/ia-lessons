# Spec: Registry Lookup Caching

## Overview

The loader caches responses from the schema registry. In extend mode, the
project-local schema is merged according to the merge policy after the cache
is consulted.

## Requirements

- FR-001: Cache entries MUST be keyed by `config.yaml` checksum.
- FR-002: A validation pass MUST NOT use expired cache entries.
