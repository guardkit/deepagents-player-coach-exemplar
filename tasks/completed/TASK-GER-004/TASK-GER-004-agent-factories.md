---
id: TASK-GER-004
title: "Agent factories: player.py and coach.py (generic wiring)"
status: completed
completed: 2026-03-16
priority: high
complexity: 5
type: implementation
task_type: implementation
feature_id: FEAT-DEB
parent_review: TASK-REV-8464
wave: 2
implementation_mode: task-work
dependencies: [TASK-GER-002, TASK-GER-003]
tags: [deepagents, create-deep-agent, agent-factory, langchain, genericity]
completed_location: tasks/completed/TASK-GER-004/
---

# Task: Agent factories — `player.py` and `coach.py` (generic wiring)

## Description

Create factory functions that return configured DeepAgent instances using the
generic tools and prompts. Player gets custom tools and `FilesystemBackend` for
real file writes. Coach gets NO custom tools and uses default `StateBackend`
(ephemeral). Both wire `AGENTS.md` via `memory=` parameter.

This task replaces TASK-DEB-004. The factory PATTERN is identical — only the
tool and prompt imports change to their generic equivalents.

Player/Coach naming preserved per Adversarial Cooperation paper terminology.

## Review Finding Reference

TASK-REV-8464 Finding 5 (LOW): Factory and entrypoint patterns are already generic.
Only tool/prompt imports need updating.

## Files to Create

- `agents/player.py`
- `agents/coach.py`

## Files NOT to Touch

`agents/__init__.py`, prompts, tools, any other files

## Critical Design (from original review findings — still valid)

1. **Coach uses default StateBackend** — do NOT pass `backend=FilesystemBackend`.
   Built-in filesystem middleware still exists but operates on ephemeral state only.

2. **Player uses FilesystemBackend** — passes `backend=FilesystemBackend(root_dir=".")`
   so `write_output` tool reaches real filesystem.

3. **Both pass `memory=["./AGENTS.md"]`** — activates MemoryMiddleware which injects
   AGENTS.md boundaries into the system prompt at runtime.

## Acceptance Criteria

### agents/player.py
- [x] Imports `create_deep_agent` from `deepagents`
- [x] Imports `FilesystemBackend` from `deepagents.backends`
- [x] Imports `search_data`, `write_output` from `tools`
- [x] Imports `PLAYER_SYSTEM_PROMPT` from `prompts.player_prompts`
- [x] Defines `create_player(model, domain_prompt: str)` factory function
- [x] Returns `create_deep_agent(model=model, tools=[search_data, write_output], system_prompt=..., memory=["./AGENTS.md"], backend=FilesystemBackend(root_dir="."))`
- [x] System prompt combines `PLAYER_SYSTEM_PROMPT` + `domain_prompt` (concatenated)
- [x] No agent instantiated at module level

### agents/coach.py
- [x] Imports `create_deep_agent` from `deepagents`
- [x] Imports `COACH_SYSTEM_PROMPT` from `prompts.coach_prompts`
- [x] Defines `create_coach(model, domain_prompt: str)` factory function
- [x] Returns `create_deep_agent(model=model, tools=[], system_prompt=..., memory=["./AGENTS.md"])` — NO custom tools
- [x] Coach tools list is explicitly empty (`tools=[]`)
- [x] Does NOT specify `backend=` — uses default StateBackend (ephemeral)
- [x] Does NOT import or use `FilesystemBackend`
- [x] Passes `memory=["./AGENTS.md"]`
- [x] No agent instantiated at module level

### Both
- [x] Import check: `from agents.player import create_player; from agents.coach import create_coach`
- [x] Both accept `model` and `domain_prompt` parameters (not `subject_prompt`)
- [x] No references to rag_retrieval, jsonl_writer, subject_prompt, curriculum

## Player Constraints

- Do not instantiate agents at module level
- Do not give Coach any tools
- Do not give Coach a `FilesystemBackend`
- Do not import `agent.py` (circular dependency risk)
- Both factories must pass `memory=["./AGENTS.md"]`

## Coach Validation Commands

```bash
uv run python -c "
from agents.player import create_player
from agents.coach import create_coach
import inspect
player_sig = inspect.signature(create_player)
coach_sig = inspect.signature(create_coach)
assert 'model' in player_sig.parameters, 'create_player must accept model param'
assert 'domain_prompt' in player_sig.parameters, 'create_player must accept domain_prompt param'
assert 'model' in coach_sig.parameters, 'create_coach must accept model param'
assert 'domain_prompt' in coach_sig.parameters, 'create_coach must accept domain_prompt param'
print('Agent factory signatures OK')
"
uv run python -c "
import ast, pathlib
coach_src = pathlib.Path('agents/coach.py').read_text()
tree = ast.parse(coach_src)
for node in ast.walk(tree):
    if isinstance(node, ast.Assign):
        if isinstance(node.value, ast.Call):
            func = node.value.func
            name = getattr(func, 'id', getattr(func, 'attr', ''))
            assert name != 'create_deep_agent', 'Coach must not instantiate agent at module level'
assert 'FilesystemBackend' not in coach_src, 'Coach must NOT use FilesystemBackend'
assert 'AGENTS.md' in coach_src, 'Coach factory must pass memory=[\"./AGENTS.md\"]'
player_src = pathlib.Path('agents/player.py').read_text()
assert 'AGENTS.md' in player_src, 'Player factory must pass memory=[\"./AGENTS.md\"]'
assert 'FilesystemBackend' in player_src, 'Player factory must use FilesystemBackend'
# Generic tool check
assert 'search_data' in player_src, 'Player must import search_data'
assert 'write_output' in player_src, 'Player must import write_output'
assert 'rag_retrieval' not in player_src, 'Player must NOT reference rag_retrieval'
assert 'jsonl_writer' not in player_src, 'Player must NOT reference jsonl_writer'
print('Backend, memory, and tool wiring OK')
"
```
