# Proposal: Add Dark Mode

## Intent

Users have asked for a dark option to cut eye strain at night, and for
the app to match whatever look their machine is set to.

## Scope

In scope:

- Manual theme preference toggle in settings
- A `system` option that follows the operating system
- Applying the theme preference on sign-in

Out of scope:

- Per-component appearance overrides
- Automatic switching by time of day

## Approach

Extend the existing appearance capability: the theme preference reuses
the stored value and adds a `system` option resolved against the OS
setting at render time.
