# One-shot plan template

Copy this file (or start a dated one) before a focused slice of work.
Fill the tables. Do not start implementation until the keep/defer split
and the validation column are written.

Nothing in the slice should replace a running job's supervisor, worker,
or in-memory process. Prefer: tests first; read-only inspection of a
live system; deploy at a job handoff or after the job exits.

## Keep now (implementation order)

| Order | Change | Touches a live job? | Validation |
|-------|--------|---------------------|------------|
| 1 | `<openspec change name>` | No / only at next start | Unit tests: `<cases>`. Command: `<cmd>`. Evidence: exit code, hashes, sizes. |
| 2 | | | |

## Defer

| Change | Why defer | When / how to validate later |
|--------|-----------|------------------------------|
| | | |

## Post-slice

After the slice, fill `docs/postmortems/TEMPLATE.md` (or a dated file)
and store evidence under `docs/validation/`. Record what shipped vs
deferred, every material command and its output, whether any live job
file was written, validations that could not be run, and new checks that
should become standing tests.
