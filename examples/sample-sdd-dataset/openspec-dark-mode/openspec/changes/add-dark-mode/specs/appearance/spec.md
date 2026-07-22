# Delta for Appearance

## ADDED Requirements

### Requirement: System Option

The system SHALL support a `system` value for the theme preference that
follows the operating system's color scheme.

#### Scenario: Following the OS

- GIVEN a user whose theme preference is `system`
- WHEN the operating system switches to dark
- THEN the interface renders with the dark palette

## MODIFIED Requirements

### Requirement: Preference Persistence

The system SHALL apply the saved theme preference on every new session,
resolving `system` against the current OS setting.

#### Scenario: Returning user

- GIVEN a user whose theme preference is `system`
- WHEN the user starts a new session on an OS set to dark
- THEN the interface renders with the dark palette
