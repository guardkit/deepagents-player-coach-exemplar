# Feature: DeepAgents Exemplar Build

## Problem

Before running `/template-create` to produce a reusable `deepagents-agentic-loop`
template, a working exemplar repo must exist. Templates are created FROM proven
working code, not authored by hand. This feature builds that exemplar using
patterns from `deep_research` and `content-builder-agent` examples, demonstrating
a generic two-agent Player-Coach orchestration pattern.

## Solution

Build a 7-task exemplar combining:
- **deep_research** patterns: prompts.py separation, LangGraph deployment, LangSmith tracing
- **content-builder-agent** patterns: AGENTS.md boundaries, config-driven domain design
- **New**: Player-Coach peer agent architecture with structured JSON evaluation

## Architecture

```
agent.py (entrypoint, config loading, wiring)
  ├── agents/player.py   → create_deep_agent(tools=[...], backend=FilesystemBackend, memory=["./AGENTS.md"])
  ├── agents/coach.py    → create_deep_agent(tools=[], memory=["./AGENTS.md"])  # StateBackend default
  ├── tools/             → @tool decorated functions (search_data, write_output)
  ├── prompts/           → System prompt string constants
  ├── AGENTS.md          → Runtime boundaries via MemoryMiddleware
  ├── coach-config.yaml  → Model selection (local/API)
  └── domains/           → Custom config per domain (not SkillsMiddleware)
```

## Tasks

| ID | Title | Complexity | Wave | Depends On |
|----|-------|-----------|------|------------|
| TASK-GER-001 | Scaffold fixes | 3 | 1 | — |
| TASK-GER-002 | Tools (search_data, write_output) | 5 | 1 | 001 |
| TASK-GER-003 | Prompts (generic) | 7 | 1 | 001 |
| TASK-GER-005 | Config (AGENTS.md, coach-config, domain) | 5 | 1 | 001 |
| TASK-GER-004 | Agent factories | 5 | 2 | 002, 003 |
| TASK-GER-006 | Entrypoint (generic wiring) | 7 | 2 | 004, 005 |
| TASK-GER-007 | FEAT spec update | 5 | 2 | 002, 003, 005 |

## Getting Started

```bash
# Wave 1: scaffold first, then parallel
/task-work TASK-GER-001

# After 001 completes — parallel via Conductor
/task-work TASK-GER-002
/task-work TASK-GER-003
/task-work TASK-GER-005

# Wave 2: sequential
/task-work TASK-GER-004
/task-work TASK-GER-006
/task-work TASK-GER-007

# Verify
# Run smoke test from TASK-GER-006
# Then /task-review for validation gate
```
