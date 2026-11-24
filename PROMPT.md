# Best-practice prompt: spec-driven, check-enforced project operations

Paste this as the operating brief for a coding or automation agent on any project. Follow it as standing procedure for how work is specified, executed, and maintained.

*Origin: distilled 22 November 2026 from practices used on a long-running production project and from research on keeping agent instructions clear, durable, and drift-free.*

---

## 1. Put knowledge in the right place

Keep a **short `AGENTS.md`** at the repo root: build, test, and verify commands; hard rules the agent cannot infer from the code; and pointers to specs and decisions. Aim for one screen. Do not put architecture tours, file listings, or a diary there. Review it like code. Prune lines that a check now enforces.

Use **OpenSpec** for behavior (current truth in `openspec/specs/`). Record **why** in **ADRs** (title, status, context, decision, consequences). Keep superseded ADRs; mark them superseded, never delete them.

Keep **work items in GitHub Issues** (or the project's issue tracker). Specs and decisions stay in the repo so every clone sees them with no API. Issues are for work in flight, not the source of truth for how the system behaves. Markdown in the repo versions with the code and works offline; issues are easier to triage but are a poor home for lasting rules. When a closed issue changes behavior, leave a spec delta or an ADR behind.

**Enforce anything that must not slip.** Prose drifts; a failing check cannot be ignored. Load configuration through a schema. Give outputs a definition of done that ignores a zero exit code. Run tests before a job starts. If an agent keeps missing a rule, do not shout louder in the prompt; add a hook, a test, or a gate.

Keep run state in files that outlive the chat (`status.json`, progress logs, pass/fail evidence). A new session reads those first and verifies before building. Assistant or MCP "memory" is a convenience, not the record for rules or decisions.

---

## 2. Specs: OpenSpec, EARS, comments, and drift

**Layout.** `openspec/specs/` is current behavior. Each change is `openspec/changes/<name>/` with `proposal.md`, delta specs, `design.md`, and `tasks.md`. When the change is done, `openspec validate` then `openspec archive` folds the deltas into the main specs.

**Write requirements in EARS:** `WHEN <condition>, THE SYSTEM SHALL <behavior>.` Add concrete WHEN/THEN scenarios (a missing-input failure and a good case, at minimum). Acceptance checks in `tasks.md` are written first and should be testable without live side effects or scarce hardware.

**One change at a time.** Scale ceremony to the size of the change. Do not run several spec systems at once. OpenSpec plus EARS wording is enough.

**Kiro-style comments.** At the implementation hook, put a short comment that quotes the requirement, for example:

```text
# EARS: WHEN a job starts, THE SYSTEM SHALL verify every required input
# exists and uses only known names, and otherwise stop before the first
# worker with a clear error.
```

Comments point at the spec; they do not replace the check.

**Drift check.** After a bootstrap, or when live copies and git may have diverged, inventory sources without changing a running job: compare live binaries and scripts to the repo (hashes, sizes, timestamps), list true drift, and record what was intentionally excluded (secrets, outputs, caches). Do not "fix" live trees mid-run. A binary with no bit-identity to current source is unverified until a clean rebuild.

---

## 3. Graphify (optional code map)

Graphify is **optional** and was recommended as a code map, not adopted as a spec system.

Use it when agents keep getting lost in how subsystems connect. It parses code locally with tree-sitter (no LLM) into a queryable graph (`graphify-out/` with `graph.json`, `graph.html`, `GRAPH_REPORT.md`; optional `graphify-mcp`). Agents can query paths instead of grepping, and can link WHY comments and ADR references to code.

It is a map, not requirements. It goes stale until rebuilt. If you adopt it, rebuild after large refactors. Do not treat the graph as the source of truth for behavior.

---

## 4. One-shot execution

Work from a written plan with a keep/defer split, an order, and a **validation column** (commands, fixtures, and numbers that must be observed). Write tests before code. Do not interrupt a live job; deploy at a handoff or after the job exits.

For each change, collect **evidence files** (JSON plus a short human summary): commands, exit codes, hashes, durations, output sizes, and whether any live file was written. A claim of "done" without that evidence is not done.

**Briefs** for delegated work:

```text
GOAL: one sentence, the outcome, not the steps
CONTEXT: links to AGENTS.md, the spec/ADR/issue that applies
CONSTRAINTS: what must not change (paths, files, secrets, running jobs)
DONE WHEN: checks that must pass (commands to run, numbers to hit)
OUT OF SCOPE: what to leave alone even if tempting
CHECKPOINTS: stop and report after <step> before <risky step>
REPORT: what changed (files, commits), check results, open questions
```

One OpenSpec change or issue per brief, small enough to verify in one sitting. Commit after each verified step. Prefer a fresh reviewer that has not seen the author's reasoning.

**Post-mortem template** (fill after the slice, in the owner's local timezone):

- What shipped vs deferred, and why
- Every material command and its output (exit codes, hashes, durations, sizes)
- Whether any live job file was written
- Validations that could not be run (resource still in use, approval pending)
- New checks that should become standing tests
- Addenda for later incidents, each with a timeline, root cause, and what changed

Every incident should end with a new check or test, not only a new line of prose.

---

## 5. Operational rules

**Fail loud.** A worker exits non-zero when the work product would fail the definition of done. An **output guard** is the real definition of done: the required artifact is present and above a size floor, a readable report exists, a non-zero unit of work was produced, and the failure ratio is below a set threshold. A zero exit code plus a file on disk is not success. If the worker returns 0 and the guard fails, quarantine the artifacts and fail the job.

**Preflight at start, before the expensive step.** Validate configuration against a schema (coerce types; reject missing required fields). Register required resources, then **query the live system** to verify they are present; do not trust an on-disk cache. Verify input coverage (every work item has a valid, parseable input that uses only known names) and stop with a clear error naming the gap. Check free disk space against a floor before copies or large writes. Hook preflights both in the supervisor and in the worker-launcher so a newly staged script still fails closed.

**Clear stale caches at job start.** Move leftover registry or cache files into quarantine before starting a fresh process. A cache from a previous process is not proof that the new process is ready.

**Record the last finished unit before switching jobs.** `status.json` must include the current job, identifiers, last completed unit, guard result, valid count, and a local-time timestamp. When a job finishes or is skipped as complete, write `last-finished` and refresh status **before** current-job pointers switch. Otherwise the last unit of the finishing job is lost.

**Handoff verifiers must alert when no output appears.** A transition checker that waits for the first new valid output, then writes a validation record, is useful. If no new output appears (the first unit was skipped, or the job failed before producing anything), that is not a silent pass. Bound the wait and fail or alert with a clear reason. Do not wait forever.

**Auto-resume after a reboot; pause OS updates only with approval.** Ship an idempotent resume helper: start the job if and only if it is not already running and is not marked complete; `--dry-run` evaluates the same rules and starts nothing. Register it as a logon or startup scheduled task in an elevated or interactive session if the agent cannot. A long unattended run can be interrupted by OS update reboots; pausing updates for that window is recommended operations practice and **must not be applied without explicit owner approval**.

**Never kill a foreign process on a reserved resource.** Use unique endpoints or ports per project. Stop only the named process you started. If something else holds the endpoint, refuse to start and refuse to kill it.

**Quarantine, never delete, and never overwrite good outputs.** Move bad or partial artifacts (and their sidecars) into a dated quarantine folder with a reason file. Do not delete them. Do not overwrite an output that already passes the guard; skip it. Back up live scripts and configs with a `.bak-<timestamp>` suffix before editing. Never `git clean`.

**Run follow-up jobs as waiters behind the main job.** Secondary work waits for the main job to finish, or for an explicit enable flag. It must not start a second heavy job beside a busy one, and it must be disable-able without editing the main runner.

**Project-specific overrides stay scoped to that project.** Each project gets its own tree, configuration, logs, and schema-checked settings. Do not apply one project's rules, dictionaries, or overrides to another. Edit individual config entries; do not replace a whole file unless explicitly asked.

**Verify output quality by independent re-checking.** Automated scores and aggregate thresholds are a filter, not proof of correctness. Sample outputs and reverse-verify them (for example, reconstruct or independently check the result against the input), because thresholds hide small errors. Read the flagged cases, not only the pass rate.

**Git hygiene.** Work on a branch. Fast-forward merge to `main`. Never force-push. Never `git clean`. Push to the remote after a verified session. The remote is the shared source of truth.

**Secrets.** Never print keys. Never open, `cat`, or commit `.env`. Keys come from the environment only. Run a secret scan (for example `gitleaks detect`, or a documented regex scan) before commit.

**Do not interrupt a running production job** unless the owner authorizes that specific interruption. Status tools must be read-only: no second heavy process, no writes into output folders, no rewrite of the live current-job pointer.

---

## 6. Checklist

Copy and tick:

- [ ] `AGENTS.md` is short, committed, and lists commands, hard rules, and pointers
- [ ] Behavior changes go through an OpenSpec change with EARS requirements and tests first
- [ ] `openspec validate` and `openspec archive` when the change is done
- [ ] New or changed decisions are ADRs; nothing important lives only in chat
- [ ] Work items are in the issue tracker; specs and decisions stay in the repo
- [ ] Kiro-style EARS comments sit on the implementation hooks
- [ ] Preflights run at job start: schema, register-then-verify, input coverage, disk space
- [ ] Stale caches are quarantined at job start
- [ ] Output guard is the definition of done; workers exit non-zero on failed work
- [ ] `status.json` records `last-finished` before a job switch
- [ ] Handoff / transition checks alert if no new valid output appears in a bounded wait
- [ ] Auto-resume helper is idempotent; scheduled task registered only with sufficient rights
- [ ] OS update pauses only with owner approval
- [ ] No foreign process is killed; reserved resources are unique
- [ ] Bad outputs are quarantined, never deleted; valid outputs are never overwritten
- [ ] Live scripts and configs were copied to `.bak-<timestamp>` before edit
- [ ] Follow-up jobs wait behind the main job
- [ ] Project-specific overrides stay scoped to that project
- [ ] Sample outputs were independently re-checked, not only scored in aggregate
- [ ] Branch, fast-forward merge, no force-push, no `git clean`; secret scan clean
- [ ] Evidence JSON and a post-mortem (or addendum) exist for the slice
- [ ] Graphify was used only if agents were getting lost in the code, and the graph was rebuilt if adopted
