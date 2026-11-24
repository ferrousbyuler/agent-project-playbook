# Design

## Context

The worker today discovers a missing input only after the job has already
started. A preflight that uses the same inventory the runner will use can
fail closed first.

## Decisions

- Inventory work items the same way the runner does, so the check and the
  job cannot disagree about the range.
- Known names come from the project's registry or schema, not from ad-hoc
  lists in the checker.
- Fail closed on a missing file, unparseable input, empty required
  fields, or any name not in the registry.
- Run the preflight in the supervisor *before* the expensive step, and
  also at the start of the worker-launcher.
- Write a preflight report (JSON) next to the job logs and a log line
  with the reason.

## Risks / Trade-offs

- A job with a deliberate incomplete range will now refuse to start.
  That is the intended fail-closed behavior. Narrow the configured range
  or supply the missing inputs.
