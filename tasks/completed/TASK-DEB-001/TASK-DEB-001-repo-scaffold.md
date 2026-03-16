---
id: TASK-DEB-001
title: Repository scaffold and dependencies
status: completed
completed: 2026-03-16T00:00:00Z
priority: high
complexity: 3
type: configuration
task_type: implementation
feature_id: FEAT-DEB
parent_review: FEAT-deepagents-exemplar-build
wave: 1
implementation_mode: task-work
dependencies: []
tags: [python, uv, project-setup, deepagents, langchain]
---

# Task: Repository scaffold and dependencies

## Description

Create the greenfield repository structure with all directories, `pyproject.toml`,
environment template, gitignore, and LangGraph deployment config. After this task,
`uv sync` must work and all core imports must resolve.

## Files to Create

- `pyproject.toml` — with `[project]` section, `name = "deepagents-tutor-exemplar"`, Python >=3.11
- `.env.example` — documents all required env vars
- `.gitignore` — excludes secrets, caches, output files
- `langgraph.json` — `{"dependencies": ["."], "graphs": {"data_factory": "./agent.py:agent"}, "env": ".env"}`
- `README.md` — brief setup instructions only
- `agents/__init__.py` — empty
- `tools/__init__.py` — empty
- `prompts/__init__.py` — empty
- `subjects/gcse-english/` — empty dir with `.gitkeep`

## Files NOT to Touch

None (greenfield)

## Dependencies (pinned versions from review)

```toml
[project]
name = "deepagents-tutor-exemplar"
requires-python = ">=3.11"
dependencies = [
    "deepagents>=0.4.11",
    "langchain>=1.2.11",
    "langchain-core>=1.2.18",
    "langgraph>=0.2",
    "langchain-community>=0.3",
    "chromadb>=0.5",
    "langsmith>=0.2",
    "python-dotenv>=1.0",
    "pyyaml>=6.0",
]
```

## Relevant Decisions

- D8: uv for dependency management

## Acceptance Criteria

- [x] `pyproject.toml` exists with `[project]` section, `name = "deepagents-tutor-exemplar"`
- [x] Dependencies listed: `deepagents>=0.4.11`, `langchain>=1.2.11`,
  `langchain-core>=1.2.18`, `langgraph>=0.2`, `langchain-community>=0.3`,
  `chromadb>=0.5`, `langsmith>=0.2`, `python-dotenv>=1.0`, `pyyaml>=6.0`
- [x] `uv sync` completes without errors
- [x] `uv run python -c "from deepagents import create_deep_agent; print('OK')"` passes
- [x] `uv run python -c "import chromadb; print('OK')"` passes
- [x] `uv run python -c "import langsmith; print('OK')"` passes
- [x] `.env.example` documents: `LANGSMITH_API_KEY`, `LANGSMITH_TRACING=true`,
  `LANGSMITH_PROJECT=study-tutor-factory`, `LOCAL_MODEL_ENDPOINT`,
  `ANTHROPIC_API_KEY` (marked optional)
- [x] `.gitignore` excludes: `.env`, `__pycache__`, `.venv`, `train.jsonl`,
  `rag_index/`, `*.pyc`
- [x] `langgraph.json` contains `"graphs": {"data_factory": "./agent.py:agent"}`
- [x] No secrets present in any tracked file

## Player Constraints

Do not create `agent.py` yet — that is TASK-DEB-006.

## Coach Validation Commands

```bash
uv sync
uv run python -c "from deepagents import create_deep_agent; import chromadb; import langsmith; print('All imports OK')"
python -c "import tomllib; tomllib.load(open('pyproject.toml','rb'))" 2>/dev/null || python -c "import tomli; tomli.load(open('pyproject.toml','rb'))"
grep -q "LANGSMITH_API_KEY" .env.example && echo "env template OK"
grep -q ".env" .gitignore && echo "gitignore OK"
```
