---
id: TASK-DEB-003
title: "Prompts: Player and Coach system prompts"
status: superseded
superseded_by: TASK-GER-003
superseded_reason: "TASK-REV-8464 genericity review — domain-specific prompts replaced with generic equivalents"
priority: high
complexity: 7
type: implementation
task_type: implementation
feature_id: FEAT-DEB
parent_review: FEAT-deepagents-exemplar-build
wave: 1
implementation_mode: task-work
dependencies: [TASK-DEB-001]
tags: [deepagents, prompt-engineering, system-prompt, agentic-loop, gcse]
---

# Task: Prompts — Player and Coach system prompts

## Description

Create module-level string constants for Player and Coach system prompts.
These are the core instructions that drive agent behaviour. Prompts must be
subject-agnostic (subject config appended at runtime from SUBJECT.md).

## Files to Create

- `prompts/player_prompts.py`
- `prompts/coach_prompts.py`

## Files NOT to Touch

`prompts/__init__.py`, any other files

## Relevant Decisions

- D4: Separate agents with distinct responsibilities
- D5: Coach returns structured JSON, not prose

## Acceptance Criteria

### player_prompts.py
- [ ] Defines `PLAYER_SYSTEM_PROMPT` as module-level string constant
- [ ] Instructs Player to call `rag_retrieval` BEFORE generating an example
- [ ] Specifies ShareGPT JSONL format (messages array with role/content)
- [ ] Specifies 75% of examples must include `<think>...</think>` block in assistant content
- [ ] Specifies `layer` field must be set: `"behaviour"` for tutoring style, `"knowledge"` for factual
- [ ] Instructs Player to call `jsonl_writer` only AFTER Coach accepts
- [ ] Instructs Player to revise using Coach critique JSON, not re-generate from scratch
- [ ] Does NOT include subject-specific content (comes from SUBJECT.md at runtime)
- [ ] Contains the words "rag_retrieval" and "jsonl_writer"

### coach_prompts.py
- [ ] Defines `COACH_SYSTEM_PROMPT` as module-level string constant
- [ ] Instructs Coach to return ONLY valid JSON — no prose, no preamble
- [ ] Defines exact rejection schema:
  `{"decision": "accept|reject", "score": 1-5, "issues": [...], "ao_correct": bool, "socratic_quality": "guides|gives_answer|mixed", "layer_correct": bool}`
- [ ] Defines score rubric: 5=excellent, 4=good, 3=borderline (flag), 2=significant, 1=wrong
- [ ] Defines AO1-AO6 criteria Coach must evaluate against
- [ ] Defines Socratic quality meanings
- [ ] Instructs Coach it does NOT have write tools — only Player writes
- [ ] Contains the words "decision" and "socratic"

### Both
- [ ] Import check passes
- [ ] `PLAYER_SYSTEM_PROMPT` > 500 chars
- [ ] `COACH_SYSTEM_PROMPT` > 500 chars

## Player Constraints

Do not create agent factory functions here — prompts module is string constants
only. Do not import from `agents/` or `tools/`.

## Coach Validation Commands

```bash
uv run python -c "from prompts.player_prompts import PLAYER_SYSTEM_PROMPT; from prompts.coach_prompts import COACH_SYSTEM_PROMPT; print('Prompts import OK')"
uv run python -c "
from prompts.player_prompts import PLAYER_SYSTEM_PROMPT
from prompts.coach_prompts import COACH_SYSTEM_PROMPT
assert 'rag_retrieval' in PLAYER_SYSTEM_PROMPT, 'Player prompt must reference rag_retrieval tool'
assert 'jsonl_writer' in PLAYER_SYSTEM_PROMPT, 'Player prompt must reference jsonl_writer tool'
assert 'think' in PLAYER_SYSTEM_PROMPT.lower(), 'Player prompt must specify think block requirement'
assert 'layer' in PLAYER_SYSTEM_PROMPT.lower(), 'Player prompt must specify layer field'
assert 'decision' in COACH_SYSTEM_PROMPT.lower(), 'Coach prompt must define rejection schema'
assert 'socratic' in COACH_SYSTEM_PROMPT.lower(), 'Coach prompt must define socratic quality'
assert 'ao' in COACH_SYSTEM_PROMPT.lower(), 'Coach prompt must reference AOs'
assert len(PLAYER_SYSTEM_PROMPT) > 500, 'Player prompt too short'
assert len(COACH_SYSTEM_PROMPT) > 500, 'Coach prompt too short'
print('Prompt content validation OK')
"
```
