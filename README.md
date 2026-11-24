# Agent project playbook

A public GitHub **template** for running and maintaining any project with
spec-driven, check-enforced agent operations.

It packages a paste-ready operating prompt plus a starter layout:
`AGENTS.md`, OpenSpec (EARS requirements and an example change), ADRs,
one-shot and post-mortem templates, validation evidence, an optional
Graphify note, and a small drift-check script.

This is a playbook, not an application. Use it as the skeleton for a new
repo, then replace the examples with your project's real specs, decisions,
and checks.

## Use it as a GitHub template

1. Open this repository on GitHub and choose **Use this template** →
   **Create a new repository**.
2. Clone your new repository.
3. Fill in `AGENTS.md` with your real commands and hard rules.
4. Replace the example OpenSpec spec and the example change with your
   first real behavior change. Add ADRs for decisions you have already
   made.
5. Paste `PROMPT.md` into an agent's brief, or point the agent at this
   repository and `AGENTS.md`.
6. Optionally adopt Graphify later; see `docs/graphify.md`. It is a code
   map, not a requirement.

You can also clone this repository directly and delete the example change
once you start real work.

## What's in here

| Path | Purpose |
|------|---------|
| `PROMPT.md` | Operating brief to paste into an agent or project |
| `AGENTS.md` | Short starter instruction file (commands, hard rules, pointers) |
| `openspec/specs/` | Current behavior. One example capability is included |
| `openspec/changes/example-input-coverage/` | Example in-flight change (proposal, design, tasks, delta spec) |
| `docs/adr/` | ADR template and one example decision |
| `docs/one-shot-plan.md` | Keep/defer plan template with a validation column |
| `docs/postmortems/TEMPLATE.md` | Incident / slice post-mortem template |
| `docs/validation/` | Evidence JSON schema and a worked example |
| `docs/graphify.md` | Optional knowledge-graph code map (not adopted by default) |
| `scripts/check-drift.py` | Inventory and optional live-vs-repo hash comparison |
| `.github/workflows/checks.yml` | Runs the drift check and a simple secret-pattern scan |

## Principles in one screen

- Keep `AGENTS.md` short. Put behavior in OpenSpec, reasons in ADRs, and
  work items in your issue tracker.
- Write requirements as `WHEN <condition>, THE SYSTEM SHALL <behavior>`.
- Enforce anything that must not slip with a check, not a louder prompt.
- Fail loud: an output guard is the definition of done, not a zero exit code.
- Preflight at job start; quarantine stale caches and bad outputs; never
  delete evidence; never overwrite good outputs.
- Record evidence (commands, hashes, sizes, exit codes) and write a
  post-mortem when a slice ends.

The full rules are in `PROMPT.md`.

## License

MIT. See `LICENSE`.
