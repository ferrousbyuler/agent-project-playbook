# ADR 0001: Quarantine artifacts, never delete them

- Status: Accepted
- Date: 2026-11-22
- Deciders: Project owner, recorded by the agent that adopted this playbook

## Context

Failed, partial, or invalid outputs are still evidence. Deleting them
hides the failure mode and risks accidental data loss. `git clean` is
similarly too broad for a live tree.

## Decision

Bad or partial outputs (the artifact, its report, sidecars, stale
caches, and interrupted work) are moved into a dated `quarantine/`
directory with a reason file. Nothing in that flow is deleted. Copies
already published elsewhere are moved to a matching quarantine folder,
not erased.

## Consequences

Disk use grows, and quarantine paths must stay out of publish globs and
out of git. Resume or skip logic must not treat quarantined files as
complete. Live scripts and configs are backed up with a `.bak-<timestamp>`
suffix before they are edited.
