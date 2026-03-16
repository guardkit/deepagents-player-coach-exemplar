---
id: TASK-GER-003
title: "Prompts: generic Player and Coach system prompts"
status: completed
completed: "2026-03-16T00:00:00Z"
completed_location: tasks/completed/TASK-GER-003/
priority: critical
complexity: 7
type: implementation
task_type: implementation
feature_id: FEAT-DEB
parent_review: TASK-REV-8464
wave: 1
implementation_mode: task-work
dependencies: [TASK-GER-001]
tags: [deepagents, prompt-engineering, system-prompt, agentic-loop, genericity]
---

# Task: Prompts — generic Player and Coach system prompts

## Description

Create module-level string constants for Player and Coach system prompts that
demonstrate the two-agent adversarial cooperation pattern WITHOUT coupling to
any specific domain. These replace the tutor-factory prompts that specified
ShareGPT format, AO1-AO6 criteria, Socratic quality metrics, and layer routing.

The Player-Coach terminology is preserved per the Block Adversarial Cooperation
paper: Player generates content, Coach evaluates and provides structured feedback.

Prompts must be domain-agnostic — domain-specific config is appended at runtime
from DOMAIN.md.

## Review Finding Reference

TASK-REV-8464 Finding 2 (CRITICAL): Original prompts saturated with tutor-factory
logic. Recommendation 2: Rewrite with generic structured evaluation pattern.

## Files to Create

- `prompts/player_prompts.py`
- `prompts/coach_prompts.py`

## Files NOT to Touch

`prompts/__init__.py`, any other files

## Relevant Decisions

- D4: Separate agents with distinct responsibilities (Adversarial Cooperation)
- D5: Coach returns structured JSON, not prose

## Acceptance Criteria

### player_prompts.py
- [x] Defines `PLAYER_SYSTEM_PROMPT` as module-level string constant
- [x] Instructs Player to call `search_data` BEFORE generating content
- [x] Specifies output must be valid JSON with a `content` field
- [x] Instructs Player to call `write_output` only AFTER Coach accepts
- [x] Instructs Player to revise using Coach critique JSON, not re-generate from scratch
- [x] Does NOT include domain-specific content (that comes from DOMAIN.md at runtime)
- [x] Does NOT reference: ShareGPT, JSONL format, think blocks, layer, behaviour, knowledge, AO, curriculum, tutor, GCSE
- [x] Contains the words "search_data" and "write_output"
- [x] `PLAYER_SYSTEM_PROMPT` > 400 chars (1,496 chars)

### coach_prompts.py
- [x] Defines `COACH_SYSTEM_PROMPT` as module-level string constant
- [x] Instructs Coach to return ONLY valid JSON — no prose, no preamble
- [x] Defines generic evaluation schema:
  ```json
  {
    "decision": "accept | reject",
    "score": 1-5,
    "issues": ["..."],
    "criteria_met": true,
    "quality_assessment": "high | adequate | needs_revision"
  }
  ```
- [x] Defines score rubric: 5=excellent, 4=good, 3=borderline (flag), 2=significant issues, 1=reject
- [x] Instructs Coach to evaluate against domain criteria provided in system prompt (from DOMAIN.md)
- [x] Instructs Coach it does NOT have write tools — only Player writes
- [x] Does NOT reference: ao_correct, socratic_quality, layer_correct, AO1-AO6, Socratic, GCSE, curriculum
- [x] Contains the words "decision" and "criteria_met"
- [x] `COACH_SYSTEM_PROMPT` > 400 chars (2,110 chars)

### Both
- [x] Import check passes
- [x] No domain-specific terminology in either prompt

## Player Constraints

Do not create agent factory functions here — prompts module is string constants
only. Do not import from `agents/` or `tools/`.

## Coach Validation Commands

```bash
uv run python -c "from prompts.player_prompts import PLAYER_SYSTEM_PROMPT; from prompts.coach_prompts import COACH_SYSTEM_PROMPT; print('Prompts import OK')"
uv run python -c "
from prompts.player_prompts import PLAYER_SYSTEM_PROMPT
from prompts.coach_prompts import COACH_SYSTEM_PROMPT
assert 'search_data' in PLAYER_SYSTEM_PROMPT, 'Player prompt must reference search_data tool'
assert 'write_output' in PLAYER_SYSTEM_PROMPT, 'Player prompt must reference write_output tool'
assert 'decision' in COACH_SYSTEM_PROMPT.lower(), 'Coach prompt must define evaluation schema'
assert 'criteria_met' in COACH_SYSTEM_PROMPT.lower(), 'Coach prompt must include criteria_met field'
assert len(PLAYER_SYSTEM_PROMPT) > 400, 'Player prompt too short'
assert len(COACH_SYSTEM_PROMPT) > 400, 'Coach prompt too short'
# Domain-specific terms must NOT appear
banned = ['socratic', 'ao_correct', 'layer_correct', 'gcse', 'curriculum', 'ShareGPT', 'train.jsonl']
for term in banned:
    assert term.lower() not in PLAYER_SYSTEM_PROMPT.lower(), f'Player prompt must not contain domain term: {term}'
    assert term.lower() not in COACH_SYSTEM_PROMPT.lower(), f'Coach prompt must not contain domain term: {term}'
print('Prompt content validation OK — generic confirmed')
"
```
