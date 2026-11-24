# Tasks

## 0. Acceptance checks (write first)

- [ ] A0. WHEN a job has work item 2 but no valid input for item 2, THE SYSTEM SHALL fail preflight with a clear error naming item 2 and SHALL NOT start the expensive step or write output artifacts.
- [ ] A1. WHEN every work item in the range has a parseable input whose names are all known, THE SYSTEM SHALL pass preflight.
- [ ] A2. Unit tests SHALL cover both the missing-input case and the good case, and SHALL NOT require a live backend.

## 1. Implement

- [ ] 1.1 Add the coverage preflight module.
- [ ] 1.2 Hook the supervisor (before the expensive step) and the worker-launcher.
- [ ] 1.3 Write a preflight JSON report and a clear log line.

## 2. Validate

- [ ] 2.1 Run the unit tests and keep the evidence JSON.
