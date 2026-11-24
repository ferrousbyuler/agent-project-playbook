# Project name

Replace this file with your project's short instruction set. Keep it to
about one screen. Put behavior in `openspec/specs/`, decisions in
`docs/adr/`, and work items in your issue tracker.

## Commands

- Tests: `<your test command>`
- Specs: `openspec list --specs` and `openspec validate --all --no-interactive`
- Drift check: `python3 scripts/check-drift.py`
- Secret scan: `python3 scripts/check-secrets.py` (and `gitleaks detect` if you use it)

## Hard rules (also enforced, or to be enforced, by checks)

- Never print keys. Never open, `cat`, or commit `.env`. Keys come from the environment only.
- Never `git clean`.
- Never overwrite an output that already passes the definition-of-done guard; skip it.
- Quarantine bad or partial artifacts (move them, with sidecars, into a dated folder). Never delete them.
- A unit of work is done only when the output guard passes, not when a worker exits 0.
- Do not interrupt a running production job unless the owner authorizes that specific interruption.
- Project-specific overrides stay scoped to that project. Edit individual config entries; do not replace a whole file unless explicitly asked.

## Where things live

- Behavior specs: `openspec/specs/`
- In-flight changes: `openspec/changes/` (archive when done)
- Decisions: `docs/adr/`
- Work items: GitHub Issues (or the project's issue tracker)
- Operating brief: `PROMPT.md`
