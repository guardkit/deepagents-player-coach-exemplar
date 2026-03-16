# Implementation Guide: DeepAgents Exemplar Build

**Feature ID:** FEAT-DEB
**Parent Spec:** [FEAT-deepagents-exemplar-build.md](../../../docs/research/project_template/FEAT-deepagents-exemplar-build.md)
**Tasks:** 7 (TASK-GER-001 through TASK-GER-007)
**Waves:** 2

> **Revision Note:** Original TASK-DEB tasks have been superseded by TASK-GER tasks
> following the TASK-REV-8464 genericity review. See FEAT spec Section 5 for full mapping.

---

## Execution Strategy

### Wave 1: Foundation (4 tasks, parallelisable)

These tasks have no dependencies on each other — only on the repo scaffold (TASK-GER-001).
Run TASK-GER-001 first, then execute 002, 003, 005 in parallel.

| Task | Title | Complexity | Method | Workspace |
|------|-------|-----------|--------|-----------|
| TASK-GER-001 | Scaffold fixes: remove domain artifacts | 3 | task-work | deepagents-exemplar-wave1-1 |
| TASK-GER-002 | Tools (`search_data`, `write_output`) | 5 | task-work | deepagents-exemplar-wave1-2 |
| TASK-GER-003 | Prompts (generic Player, Coach) | 7 | task-work | deepagents-exemplar-wave1-3 |
| TASK-GER-005 | Config (AGENTS.md, coach-config, domain) | 5 | task-work | deepagents-exemplar-wave1-4 |

**Dependency chain within Wave 1:**
```
TASK-GER-001 (scaffold fixes)
  ├── TASK-GER-002 (tools)      ← needs uv sync
  ├── TASK-GER-003 (prompts)    ← needs uv sync
  └── TASK-GER-005 (config)     ← needs uv sync
```

**Recommended execution:**
1. Run TASK-GER-001 first (scaffold fixes)
2. After 001 completes, run 002 + 003 + 005 in parallel via Conductor

### Wave 2: Integration (3 tasks, sequential dependency)

| Task | Title | Complexity | Method | Workspace |
|------|-------|-----------|--------|-----------|
| TASK-GER-004 | Agent factories (player.py, coach.py) | 5 | task-work | deepagents-exemplar-wave2-1 |
| TASK-GER-006 | Main entrypoint (agent.py) | 7 | task-work | deepagents-exemplar-wave2-2 |
| TASK-GER-007 | FEAT spec update | 5 | task-work | — |

**Dependency chain within Wave 2:**
```
TASK-GER-004 (agent factories) ← needs tools (002) + prompts (003)
  └── TASK-GER-006 (entrypoint) ← needs factories (004) + config (005)
TASK-GER-007 (docs update)     ← needs 002, 003, 005 completed
```

---

## File Conflict Analysis

No file conflicts between parallel tasks:

| Task | Files Created/Modified |
|------|----------------------|
| TASK-GER-001 | pyproject.toml, .env.example, .gitignore, langgraph.json, README.md, __init__.py files |
| TASK-GER-002 | tools/search_data.py, tools/write_output.py |
| TASK-GER-003 | prompts/player_prompts.py, prompts/coach_prompts.py |
| TASK-GER-005 | AGENTS.md, coach-config.yaml, domains/example-domain/DOMAIN.md |
| TASK-GER-004 | agents/player.py, agents/coach.py |
| TASK-GER-006 | agent.py |
| TASK-GER-007 | FEAT spec, IMPLEMENTATION-GUIDE.md, README.md (docs only) |

Zero overlap — safe for full parallel execution within each wave.

---

## Critical Review Findings (incorporated)

These findings from the architectural review and TASK-REV-8464 genericity review
are already incorporated into the task acceptance criteria:

1. **Coach uses StateBackend (default)** — do not give Coach a FilesystemBackend.
   Built-in middleware filesystem tools operate on ephemeral state only.

2. **AGENTS.md wired via `memory=`** — both factories must pass
   `memory=["./AGENTS.md"]` to `create_deep_agent()`. Without this, boundaries
   are not injected into the system prompt.

3. **Player/Coach are peer agents** — they are NOT subagents. Do not use
   `subagents=[]` or `load_subagents()`. Orchestration is imperative in agent.py.

4. **domains/ is custom config** — not a DeepAgents skill. Do not pass to
   `skills=[]` parameter.

5. **Dependency versions pinned** — `deepagents>=0.4.11`, `langchain>=1.2.11`,
   `langchain-core>=1.2.18`.

6. **Generic tool names** — `search_data` and `write_output` (not `rag_retrieval`
   or `jsonl_writer`). Tools are domain-agnostic.

7. **Generic Coach schema** — `criteria_met` and `quality_assessment` (not
   `ao_correct`, `socratic_quality`, `layer_correct`). Domain-specific criteria
   loaded from `DOMAIN.md` at runtime.

---

## Post-Implementation

After all GER tasks complete, run the full smoke test from TASK-GER-006, then
pass to `/task-review` for TASK-REV validation before running `/template-create`.
