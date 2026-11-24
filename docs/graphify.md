# Graphify (optional)

Graphify is **not required** by this playbook. It was recommended as an
optional code map for when agents keep getting lost in how parts of a
codebase connect. It is **not** a spec system and is **not** a substitute
for OpenSpec or ADRs.

## What it is

Graphify turns a codebase into a local, queryable knowledge graph.
According to the project's own docs (as summarized in November 2026
research):

- Code is parsed **locally** with tree-sitter. No LLM is used for the parse.
- Output typically lives under `graphify-out/`, including `graph.json`,
  `graph.html`, and `GRAPH_REPORT.md`.
- An optional `graphify-mcp` server can expose the graph to an agent.
- Agents can query paths instead of grepping, and can link WHY comments
  and ADR references to code.

## When to use it

Adopt it when agents repeatedly misread how subsystems connect. Skip it
if the repo is small or the specs and `AGENTS.md` already keep agents
oriented.

## Limits

- It is a **map**, not requirements. Behavior still lives in
  `openspec/specs/`.
- The graph **goes stale until rebuilt**. If you adopt it, rebuild after
  large refactors.
- Do not treat the graph as the source of truth for how the system
  should behave.

## Setup

Follow the current documentation of the Graphify project rather than
copied install steps, which go out of date:

- Repository: [https://github.com/Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify)
- Architecture: [https://docs.graphify.com/concepts/architecture](https://docs.graphify.com/concepts/architecture)

Add `graphify-out/` to `.gitignore` unless you have a reason to commit a
generated graph. This playbook does not invent CLI flags, MCP tool
names, or install commands beyond what those docs provide.
