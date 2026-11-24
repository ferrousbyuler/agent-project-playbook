# output-guard Specification

## Purpose

Define the loud-fail checks that decide whether a unit of work counts as
complete, and how invalid output is quarantined instead of deleted or
published.

## Requirements

### Requirement: Validity criteria
WHEN checking a unit of work in an output directory, THE SYSTEM SHALL
treat the output as invalid if any of the following hold: the required
artifact is missing; the artifact is at or below a documented size floor;
the matching report is missing or unreadable; the report records zero
units of work; every unit failed; or the failure ratio meets or exceeds a
documented threshold. WHEN none of those hold, THE SYSTEM SHALL return
success.

#### Scenario: Tiny stub
- **WHEN** the required artifact exists but is at or below the size floor
- **THEN** the guard fails with a reason that names the size problem

#### Scenario: High fail rate
- **WHEN** a report lists a failure ratio at or above the threshold
- **THEN** the guard fails even if the artifact is larger than the size floor

#### Scenario: Clean output
- **WHEN** a substantial artifact has a readable report with a non-zero
  unit count and a failure ratio below the threshold
- **THEN** the guard returns success

### Requirement: Worker exit code is not sufficient
WHEN the worker exits 0 but the validity guard fails, THE SYSTEM SHALL
treat the unit as failed, move the artifact, report, and sidecars into
quarantine without deleting them, and return a non-zero status from the
job runner.

#### Scenario: Failed work with rc=0
- **WHEN** the worker writes a report plus a short artifact and exits 0,
  and the guard fails
- **THEN** the files are quarantined, the unit is not marked complete,
  and the job stops with a non-zero status
