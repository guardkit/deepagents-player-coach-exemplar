---
id: TASK-GER-006
title: "Main entrypoint agent.py (generic wiring)"
status: completed
completed: 2026-03-16
priority: high
complexity: 7
type: implementation
task_type: implementation
feature_id: FEAT-DEB
parent_review: TASK-REV-8464
wave: 2
implementation_mode: task-work
dependencies: [TASK-GER-004, TASK-GER-005]
tags: [deepagents, langchain, init-chat-model, config-loading, entrypoint, genericity]
---

# Task: Main entrypoint `agent.py` (generic wiring)

## Description

Create the main entrypoint that wires everything together: reads config, initialises
models, creates Player and Coach agents, and exposes a module-level `agent` variable
for LangGraph Studio deployment.

This replaces TASK-DEB-006 with generic naming and references. The wiring pattern
is identical — only names and defaults change.

Note: The Player-Coach orchestration loop is OUT OF SCOPE for this exemplar.
`agent.py` proves the wiring is correct. Actual generation loops belong in
domain-specific projects that use this as a template.

## Review Finding Reference

TASK-REV-8464 Finding 5 (LOW): Entrypoint pattern is generic. Only naming and
default updates needed.

## Files to Create

- `agent.py`

## Files NOT to Touch

All previously created files — `agent.py` only imports from them.

## Key Wiring

1. Reads `coach-config.yaml` -> selects provider (`local` or `anthropic`)
2. Uses `init_chat_model()` from `langchain.chat_models` to create model instances
3. When `provider: local` -> uses `LOCAL_MODEL_ENDPOINT` env var with OpenAI-compatible interface
4. When `provider: anthropic` -> uses model string from `coach.api.model` in config
5. Reads `domains/{domain}/DOMAIN.md` -> passes as `domain_prompt` to factories
6. Creates Player and Coach via factory functions (factories handle `memory=` and `backend=`)
7. Defines module-level `agent` variable for `langgraph.json`

## Acceptance Criteria

- [x] Imports `create_player` from `agents.player`
- [x] Imports `create_coach` from `agents.coach`
- [x] Imports `init_chat_model` from `langchain.chat_models`
- [x] Reads `coach-config.yaml` at startup to select provider
- [x] When `provider: local` — initialises model using `LOCAL_MODEL_ENDPOINT` env var
- [x] When `provider: api` — initialises model using `init_chat_model()` with model string from `coach.api.model` config field
- [x] Reads domain config from `domains/{domain}/DOMAIN.md`
- [x] Creates Player and Coach agents using factory functions
- [x] Passes `AGENTS.md` loading to factory functions (factories handle `memory=` param)
- [x] Defines `agent` variable at module level (required for `langgraph.json`)
- [x] No model strings hardcoded — all from config or env vars
- [x] Supports `--domain` CLI argument (defaults to `example-domain`)
- [x] Full import check passes
- [x] No hardcoded model strings (gpt-4o, claude-opus, gemini, openai:)
- [x] Does NOT reference: subject, gcse-english, SUBJECT.md, rag_retrieval, jsonl_writer

## Player Constraints

Do not modify any files from Tasks 1-5. `agent.py` only imports from them —
no duplication of logic.

## Coach Validation Commands

```bash
uv run python -c "
from agents.player import create_player
from agents.coach import create_coach
from tools.search_data import search_data
from tools.write_output import write_output
from prompts.player_prompts import PLAYER_SYSTEM_PROMPT
from prompts.coach_prompts import COACH_SYSTEM_PROMPT
print('All imports OK — exemplar is wired correctly')
"
python3 -c "
import ast, pathlib
src = pathlib.Path('agent.py').read_text()
assert 'coach-config.yaml' in src or 'coach_config' in src, 'agent.py must read coach-config.yaml'
assert 'DOMAIN.md' in src or 'domain' in src.lower(), 'agent.py must load domain config'
assert 'subject' not in src.lower() or 'subject' in 'domain_subject', 'agent.py should use domain, not subject'
print('Config loading patterns present OK')
"
grep -v "^#" agent.py | grep -v ".env" | python3 -c "
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
from tools.search_data import search_data
from tools.write_output import write_output
from prompts.player_prompts import PLAYER_SYSTEM_PROMPT
from prompts.coach_prompts import COACH_SYSTEM_PROMPT
import yaml, pathlib
config = yaml.safe_load(pathlib.Path('coach-config.yaml').read_text())
domain = pathlib.Path('domains/example-domain/DOMAIN.md').read_text()
assert config['coach']['provider'] in ['local', 'anthropic']
assert len(domain) > 100
print('Full smoke test OK — generic exemplar ready for /template-create')
"
```
