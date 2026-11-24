# Post-mortem: <title>

All times are in the owner's local timezone (name the zone).

## 1. What happened

### Timeline

| Time | Event |
|------|-------|
| | |

### Root cause

What actually failed, in a few sentences. Name the signal that was
trusted without being verified (an exit code, a cache file, a type, a
summary).

### Impact

What was wrong, what had to be redone, and who or what was affected.

### Detection gap

What should have failed loudly and did not. Why discovery was late.

### Fixes

- Already in place:
- Added in this slice:
- Still open:

## 2. Slice record

- What shipped vs deferred, and why
- Every material command and its output (exit codes, hashes, durations, sizes)
- Whether any live job file was written
- Validations that could not be run (resource still in use, approval pending)
- New checks that should become standing tests

## 3. Addendum (optional)

Later incidents related to this one get a numbered addendum: timeline,
root cause, and what changed. Do not rewrite the original history.
