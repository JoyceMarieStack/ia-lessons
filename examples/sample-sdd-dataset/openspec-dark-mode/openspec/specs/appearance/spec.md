# Appearance Specification

## Purpose

Define how the application stores and applies a user's appearance
setting.

## Requirements

### Requirement: Appearance Setting

The system SHALL store a per-user appearance setting with the values
`light` and `dark`.

#### Scenario: Choosing dark

- GIVEN a signed-in user
- WHEN the user selects `dark`
- THEN the appearance setting is saved as `dark`

### Requirement: Setting Persistence

The system SHALL apply the saved appearance setting on every new
session.

#### Scenario: Returning user

- GIVEN a user whose appearance setting is `dark`
- WHEN the user starts a new session
- THEN the interface renders with the dark palette
