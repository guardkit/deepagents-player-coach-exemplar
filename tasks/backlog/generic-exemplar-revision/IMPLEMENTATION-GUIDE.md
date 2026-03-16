# Implementation Guide: Generic Exemplar Revision

**Feature ID:** FEAT-DEB (revised)
**Parent Review:** TASK-REV-8464
**Tasks:** 7
**Waves:** 2

---

## Context

This revision replaces the domain-specific study-tutor-factory exemplar with a
generic two-agent Player-Coach orchestration exemplar. The architectural review
(TASK-REV-8464, score 68/100) found that 4 of 6 original tasks contained
domain-specific content that would corrupt the template extracted by `/template-create`.

**What changed:** Tools, prompts, config content, and naming.
**What stayed:** Architecture, factory pattern, SDK wiring, wave structure.

---

## Execution Strategy

### Wave 1: Foundation (4 tasks, parallelisable after GER-001)

Run TASK-GER-001 first (scaffold fixes), then execute 002, 003, 005 in parallel.

| Task | Title | Complexity | Method | Workspace |
|------|-------|-----------|--------|-----------|
| TASK-GER-001 | Scaffold fixes (deps, dirs, text) | 2 | task-work | generic-exemplar-wave1-1 |
| TASK-GER-002 | Tools (search_data, write_output) | 5 | task-work | generic-exemplar-wave1-2 |
| TASK-GER-003 | Prompts (Player, Coach — generic) | 7 | task-work | generic-exemplar-wave1-3 |
| TASK-GER-005 | Config (AGENTS.md, coach-config, domain) | 5 | task-work | generic-exemplar-wave1-4 |

**Dependency chain within Wave 1:**
```
TASK-GER-001 (scaffold fixes)
  ├── TASK-GER-002 (tools)      <- needs tavily dep from uv sync
  ├── TASK-GER-003 (prompts)    <- needs uv sync
  └── TASK-GER-005 (config)     <- needs domains/ directory
```

**Recommended execution:**
1. Run TASK-GER-001 first (scaffold fixes)
2. After 001 completes, run 002 + 003 + 005 in parallel via Conductor

### Wave 2: Integration (3 tasks, dependency chain)

| Task | Title | Complexity | Method | Workspace |
|------|-------|-----------|--------|-----------|
| TASK-GER-004 | Agent factories (player.py, coach.py) | 5 | task-work | generic-exemplar-wave2-1 |
| TASK-GER-006 | Main entrypoint (agent.py) | 7 | task-work | generic-exemplar-wave2-2 |
| TASK-GER-007 | FEAT spec + doc updates | 5 | task-work | generic-exemplar-wave2-3 |

**Dependency chain within Wave 2:**
```
TASK-GER-004 (agent factories) <- needs tools (002) + prompts (003)
  └── TASK-GER-006 (entrypoint) <- needs factories (004) + config (005)
TASK-GER-007 (docs)            <- needs tools (002) + prompts (003) + config (005)
```

**Recommended execution:**
1. Run TASK-GER-004 after Wave 1 completes
2. Run TASK-GER-006 + TASK-GER-007 in parallel after 004 completes
   (007 only needs Wave 1 outputs, but running with 006 is simpler)

---

## File Conflict Analysis

No file conflicts between parallel tasks:

| Task | Files Created/Modified |
|------|----------------------|
| 001 | pyproject.toml, .env.example, .gitignore, langgraph.json, README.md, domains/ |
| 002 | tools/search_data.py, tools/write_output.py |
| 003 | prompts/player_prompts.py, prompts/coach_prompts.py |
| 005 | AGENTS.md, coach-config.yaml, domains/example-domain/DOMAIN.md |
| 004 | agents/player.py, agents/coach.py |
| 006 | agent.py |
| 007 | docs/research/...FEAT..., tasks/.../IMPLEMENTATION-GUIDE.md, tasks/.../README.md |

Zero overlap — safe for full parallel execution within each wave.

---

## Relationship to Original Tasks

| Original Task | Status | Revised Task | Action |
|--------------|--------|-------------|--------|
| TASK-DEB-001 | in_review | TASK-GER-001 | Apply surgical fixes to existing scaffold |
| TASK-DEB-002 | backlog | TASK-GER-002 | **Superseded** — rewrite with generic tools |
| TASK-DEB-003 | backlog | TASK-GER-003 | **Superseded** — rewrite with generic prompts |
| TASK-DEB-004 | backlog | TASK-GER-004 | Updated references only |
| TASK-DEB-005 | backlog | TASK-GER-005 | **Superseded** — rewrite with generic config |
| TASK-DEB-006 | backlog | TASK-GER-006 | Updated naming/defaults only |
| (new) | — | TASK-GER-007 | FEAT spec + doc updates |

Original TASK-DEB-002, 003, 005 should be moved to `tasks/completed/` with a note
that they were superseded by TASK-GER-002, 003, 005 per TASK-REV-8464.

---

## Critical Review Findings (incorporated)

These findings from the original architectural review remain valid:

1. **Coach uses StateBackend (default)** — do not give Coach a FilesystemBackend.

2. **AGENTS.md wired via `memory=`** — both factories must pass
   `memory=["./AGENTS.md"]` to `create_deep_agent()`.

3. **Player/Coach are peer agents** — NOT subagents. Orchestration is imperative
   in agent.py.

4. **domains/ is custom config** — not a DeepAgents skill. Do not pass to `skills=[]`.

5. **Dependency versions pinned** — `deepagents>=0.4.11`, `langchain>=1.2.11`,
   `langchain-core>=1.2.18`.

**New finding from TASK-REV-8464:**

6. **Generic tools required** — search_data (Tavily) and write_output replace
   domain-specific rag_retrieval and jsonl_writer.

7. **Generic evaluation schema** — `criteria_met` and `quality_assessment` replace
   `ao_correct`, `socratic_quality`, `layer_correct`.

---

## Post-Implementation

After all 7 tasks complete:
1. Run the full smoke test from TASK-GER-006
2. Verify no domain-specific terms leak through: `grep -ri "gcse\|socratic\|ao_correct\|curriculum\|train.jsonl" --include="*.py" --include="*.md" --include="*.yaml" .`
3. Pass to `/task-review` for validation before running `/template-create`
