---
id: TASK-DEB-004
title: "Agent factories: player.py and coach.py"
status: backlog
priority: high
complexity: 5
type: implementation
task_type: implementation
feature_id: FEAT-DEB
parent_review: FEAT-deepagents-exemplar-build
wave: 2
implementation_mode: task-work
dependencies: [TASK-DEB-002, TASK-DEB-003]
tags: [deepagents, create-deep-agent, agent-factory, langchain]
---

# Task: Agent factories — `player.py` and `coach.py`

## Description

Create factory functions that return configured DeepAgent instances. Player gets
custom tools and `FilesystemBackend` for real file writes. Coach gets NO custom
tools and uses default `StateBackend` (ephemeral) so built-in middleware can't
write real files. Both wire `AGENTS.md` via `memory=` parameter.

## Files to Create

- `agents/player.py`
- `agents/coach.py`

## Files NOT to Touch

`agents/__init__.py`, prompts, tools, any other files

## Critical Design (from review findings)

1. **Coach uses default StateBackend** — do NOT pass `backend=FilesystemBackend`.
   Built-in filesystem middleware (ls, write_file, etc.) still exists but operates
   on ephemeral state only. This enforces D4: Coach cannot write real files.

2. **Player uses FilesystemBackend** — passes `backend=FilesystemBackend(root_dir=".")`
   so `jsonl_writer` tool output reaches real filesystem.

3. **Both pass `memory=["./AGENTS.md"]`** — this activates MemoryMiddleware which
   injects AGENTS.md content (ALWAYS/NEVER/ASK boundaries) into the system prompt
   at runtime. Without this, AGENTS.md is inert documentation.

## Relevant Decisions

- D4: Separate agents, Coach has no write capability
- D6: @tool decorated functions with docstrings

## Acceptance Criteria

### agents/player.py
- [ ] Imports `create_deep_agent` from `deepagents`
- [ ] Imports `FilesystemBackend` from `deepagents.backends`
- [ ] Imports `rag_retrieval`, `jsonl_writer` from `tools`
- [ ] Imports `PLAYER_SYSTEM_PROMPT` from `prompts.player_prompts`
- [ ] Defines `create_player(model, subject_prompt: str)` factory function
- [ ] Returns `create_deep_agent(model=model, tools=[rag_retrieval, jsonl_writer], system_prompt=..., memory=["./AGENTS.md"], backend=FilesystemBackend(root_dir="."))`
- [ ] Uses `FilesystemBackend` for real file output
- [ ] Passes `memory=["./AGENTS.md"]` for runtime boundary injection
- [ ] System prompt combines `PLAYER_SYSTEM_PROMPT` + `subject_prompt` (concatenated)
- [ ] No agent instantiated at module level

### agents/coach.py
- [ ] Imports `create_deep_agent` from `deepagents`
- [ ] Imports `COACH_SYSTEM_PROMPT` from `prompts.coach_prompts`
- [ ] Defines `create_coach(model, subject_prompt: str)` factory function
- [ ] Returns `create_deep_agent(model=model, tools=[], system_prompt=..., memory=["./AGENTS.md"])` — NO custom tools
- [ ] Coach tools list is explicitly empty (`tools=[]`)
- [ ] Does NOT specify `backend=` — uses default StateBackend (ephemeral)
- [ ] Does NOT import or use `FilesystemBackend`
- [ ] Passes `memory=["./AGENTS.md"]` for runtime boundary injection
- [ ] No agent instantiated at module level

### Both
- [ ] Import check: `from agents.player import create_player; from agents.coach import create_coach`
- [ ] Both accept `model` and `subject_prompt` parameters

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
assert 'model' in coach_sig.parameters, 'create_coach must accept model param'
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
print('No module-level agent instantiation OK')
print('Backend and memory wiring OK')
"
```
