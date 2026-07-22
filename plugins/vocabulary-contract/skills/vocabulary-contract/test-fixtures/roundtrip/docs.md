# Implementation notes

Schema pinning is resolved before the validation pass starts. When a project
pins a version, the loader skips registry lookups for that base schema.

A rollback window was discussed for failed pins but rejected for this release.
