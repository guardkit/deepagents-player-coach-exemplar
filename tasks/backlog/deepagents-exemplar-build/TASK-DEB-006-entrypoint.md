---
id: TASK-DEB-006
title: "Main entrypoint agent.py"
status: backlog
priority: high
complexity: 7
type: implementation
task_type: implementation
feature_id: FEAT-DEB
parent_review: FEAT-deepagents-exemplar-build
wave: 2
implementation_mode: task-work
dependencies: [TASK-DEB-004, TASK-DEB-005]
tags: [deepagents, langchain, init-chat-model, config-loading, entrypoint]
---

# Task: Main entrypoint `agent.py`

## Description

Create the main entrypoint that wires everything together: reads config, initialises
models, creates Player and Coach agents, and exposes a module-level `agent` variable
for LangGraph Studio deployment.

Note: The Player-Coach orchestration loop is OUT OF SCOPE for this exemplar (see
Section 9 of FEAT spec). `agent.py` proves the wiring is correct. The actual
generation loop belongs in `study-tutor-factory`.

## Files to Create

- `agent.py`

## Files NOT to Touch

All previously created files — `agent.py` only imports from them.

## Key Wiring

1. Reads `coach-config.yaml` → selects provider (`local` or `anthropic`)
2. Uses `init_chat_model()` from `langchain.chat_models` to create model instances
3. When `provider: local` → uses `LOCAL_MODEL_ENDPOINT` env var with OpenAI-compatible interface
4. When `provider: anthropic` → uses model string from `coach.api.model` in config
5. Reads `subjects/{subject}/SUBJECT.md` → passes as `subject_prompt` to factories
6. Creates Player and Coach via factory functions (factories handle `memory=` and `backend=`)
7. Defines module-level `agent` variable for `langgraph.json`

## Relevant Decisions

- D1: deep_research as structural backbone
- D3: coach-config.yaml for model selection
- D4: Separate agent instances

## Acceptance Criteria

- [ ] Imports `create_player` from `agents.player`
- [ ] Imports `create_coach` from `agents.coach`
- [ ] Imports `init_chat_model` from `langchain.chat_models`
- [ ] Reads `coach-config.yaml` at startup to select provider
- [ ] When `provider: local` — initialises model using `LOCAL_MODEL_ENDPOINT` env var
- [ ] When `provider: anthropic` — initialises model using `init_chat_model()` with model string from `coach.api.model` config field
- [ ] Reads subject config from `subjects/{subject}/SUBJECT.md`
- [ ] Creates Player and Coach agents using factory functions
- [ ] Passes `AGENTS.md` loading to factory functions (factories handle `memory=` param)
- [ ] Defines `agent` variable at module level (required for `langgraph.json`)
- [ ] No model strings hardcoded — all from config or env vars
- [ ] Supports `--subject` CLI argument (defaults to `gcse-english`)
- [ ] Full import check passes
- [ ] No hardcoded model strings (gpt-4o, claude-opus, gemini, openai:)

## Player Constraints

Do not modify any files from Tasks 1-5. `agent.py` only imports from them —
no duplication of logic.

## Coach Validation Commands

```bash
uv run python -c "
from agents.player import create_player
from agents.coach import create_coach
from tools.rag_retrieval import rag_retrieval
from tools.jsonl_writer import jsonl_writer
from prompts.player_prompts import PLAYER_SYSTEM_PROMPT
from prompts.coach_prompts import COACH_SYSTEM_PROMPT
print('All imports OK — exemplar is wired correctly')
"
python -c "
import ast, pathlib
src = pathlib.Path('agent.py').read_text()
assert 'coach-config.yaml' in src or 'coach_config' in src, 'agent.py must read coach-config.yaml'
assert 'SUBJECT.md' in src or 'subject' in src.lower(), 'agent.py must load subject config'
print('Config loading patterns present OK')
"
grep -v "^#" agent.py | grep -v ".env" | python -c "
import sys
content = sys.stdin.read()
bad = ['gpt-4o', 'claude-opus', 'gemini', 'openai:']
for b in bad:
    assert b not in content, f'Hardcoded model string found: {b}'
print('No hardcoded model strings OK')
"
```

## Smoke Test (run after this task completes)

```bash
uv run python -c "
from agents.player import create_player
from agents.coach import create_coach
from tools.rag_retrieval import rag_retrieval
from tools.jsonl_writer import jsonl_writer
from prompts.player_prompts import PLAYER_SYSTEM_PROMPT
from prompts.coach_prompts import COACH_SYSTEM_PROMPT
import yaml, pathlib
config = yaml.safe_load(pathlib.Path('coach-config.yaml').read_text())
subject = pathlib.Path('subjects/gcse-english/SUBJECT.md').read_text()
assert config['coach']['provider'] in ['local', 'anthropic']
assert len(subject) > 100
print('Full smoke test OK — ready for /template-create review')
"
```
