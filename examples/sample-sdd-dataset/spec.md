# Feature Specification: Timezone Meeting Utility

Source: this is the abbreviated spec.md excerpt as published in course material
covering the real greenfield demo repo mnriem/spec-kit-dotnet-cli-demo
(https://github.com/mnriem/spec-kit-dotnet-cli-demo), generated via GitHub's
official spec-kit tool (https://github.com/github/spec-kit, MIT license). This
demo is also linked directly from spec-kit's own official documentation as a
Community Walkthrough (https://github.github.io/spec-kit/community/walkthroughs.html).

NOTE: this excerpt is abbreviated, not the complete generated file. For the
full, unabridged spec.md, plan.md, and tasks.md, clone the real repo:
  git clone https://github.com/mnriem/spec-kit-dotnet-cli-demo.git
and look under specs/001-timezone-utility/

**Feature Branch**: `001-timezone-utility`
**Status**: Draft

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Get Current Time for Location (Priority: P1)

As a user working with international colleagues, I want to quickly check
the current date and time in any location using whatever identifier I have
available (timezone, city name, country, or US zip code).

**Acceptance Scenarios**:

1. **Given** I request time for timezone "America/New_York",
   **Then** I see the current date and time with timezone abbreviation
2. **Given** I request time for US zip code "94102",
   **Then** I see the current date and time for San Francisco's timezone
3. **Given** I request time for an invalid location,
   **Then** I see a helpful error message suggesting how to format my input

### Edge Cases

- City name matches multiple locations → display all matches, prompt user
- Country has multiple timezones → list all applicable timezones
- DST transitions → use current DST rules automatically

## Requirements *(mandatory)*

- **FR-001**: System MUST accept IANA timezone identifiers
- **FR-002**: System MUST accept city names and resolve to timezones
- **FR-003**: System MUST accept US zip codes (5-digit)
- **FR-005**: System MUST handle ambiguous queries by presenting options

## Success Criteria *(mandatory)*

- Users can look up current time for any location in under 3 seconds
- 95% of common city names resolve correctly without additional user input
- All error messages provide actionable guidance
