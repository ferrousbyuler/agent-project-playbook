# Spec Delta

## ADDED Requirements

### Requirement: Input coverage before a job starts
WHEN a job is about to start, THE SYSTEM SHALL verify that every work
item in the configured range has a valid input file with only known
names. WHEN any item is missing an input, the input does not parse, or a
name is not in the project's registry, THE SYSTEM SHALL stop before the
expensive step and before the first worker, with a clear error naming
the item.

#### Scenario: Missing input
- **WHEN** item 1 has a valid input and item 2 is in the range but has no input
- **THEN** preflight fails, the reason names item 2, and the expensive step is not started

#### Scenario: Complete coverage with known names
- **WHEN** every work item in the range has a parseable input whose names are all in the registry
- **THEN** preflight passes and the job may start
