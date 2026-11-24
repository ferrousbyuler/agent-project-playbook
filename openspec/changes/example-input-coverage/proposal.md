# Proposal

> Example change, included so a new project can see the folder shape.
> Replace or delete this folder when you start real work.

## Why

A job that starts expensive work and then fails on the first missing
input wastes time and can look "started" without producing valid output.
Coverage should be checked before that work begins.

## What Changes

- WHEN a job starts, THE SYSTEM SHALL verify that every work item in the
  configured range has a valid, parseable input that uses only known
  names, and otherwise stop before the first worker with a clear error
  naming the gap.

## Capabilities

### New Capabilities
- `input-coverage`: Fail closed when required inputs are missing,
  unreadable, or refer to unknown names.

### Modified Capabilities

## Impact

A small preflight module hooked in the job supervisor (before the
expensive step) and in the worker-launcher so a newly staged script still
fails closed. Tests cover a missing-input case and a good case, and do
not require a live backend.
