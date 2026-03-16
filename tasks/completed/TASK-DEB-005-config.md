---
id: TASK-DEB-005
title: "AGENTS.md and subject configuration"
status: superseded
superseded_by: TASK-GER-005
superseded_reason: "TASK-REV-8464 genericity review — domain-specific config replaced with generic equivalents"
priority: high
complexity: 5
type: implementation
task_type: implementation
feature_id: FEAT-DEB
parent_review: FEAT-deepagents-exemplar-build
wave: 1
implementation_mode: task-work
dependencies: [TASK-DEB-001]
tags: [deepagents, agents-md, config-driven, subject-agnostic, gcse]
---

# Task: AGENTS.md and subject configuration

## Description

Create the agent boundary documentation (`AGENTS.md`), configurable coach model
selection (`coach-config.yaml`), and the first subject configuration
(`subjects/gcse-english/SUBJECT.md`).

IMPORTANT: `AGENTS.md` is loaded at runtime via `memory=["./AGENTS.md"]` in the
agent factory functions. This is a DeepAgents SDK feature — MemoryMiddleware
injects the file content into the system prompt. The ALWAYS/NEVER/ASK boundaries
are enforced at the prompt level, not just documentation.

`subjects/gcse-english/SUBJECT.md` is custom config read by `agent.py` — it is
NOT a DeepAgents skill and should NOT be passed to `skills=[]`.

## Files to Create

- `AGENTS.md`
- `coach-config.yaml`
- `subjects/gcse-english/SUBJECT.md`

## Files NOT to Touch

Any Python files

## Relevant Decisions

- D2: Config-driven pattern from content-builder-agent
- D3: coach-config.yaml for configurable Coach model
- D9: subjects/ directory (custom config, not SkillsMiddleware)

## Acceptance Criteria

### AGENTS.md
- [ ] Contains `## Player Agent` section
- [ ] Contains `## Coach Agent` section
- [ ] Each section has `ALWAYS:`, `NEVER:`, `ASK:` subsections
- [ ] Player ALWAYS: call rag_retrieval before generating, set layer field, use think blocks for 75% of examples
- [ ] Player NEVER: write output without Coach approval, generate more than one example per turn
- [ ] Coach ALWAYS: return structured JSON, check layer routing
- [ ] Coach NEVER: write to output files, modify example directly
- [ ] Coach ASK: when score is 3 (borderline) — escalate for human review

### coach-config.yaml
- [ ] Parses as valid YAML
- [ ] Contains `coach.provider` field (value: `local`)
- [ ] Contains `coach.local.model` and `coach.local.endpoint` fields
- [ ] Contains `coach.api.model` field
- [ ] Default `provider` is `local` (not `anthropic`)

### subjects/gcse-english/SUBJECT.md
- [ ] Contains `exam_board: AQA` field
- [ ] Contains `specifications` list: `[8700, 8702]`
- [ ] Contains `## Assessment Objectives` section defining AO1-AO6
- [ ] Contains `## Synthesis Prompts` section with Player generation instructions
- [ ] Contains `## Coach Rubric Additions` section with subject-specific validation
- [ ] Does NOT contain any Python code

## Player Constraints

Do not modify any Python files in this task. Configuration and documentation only.

## Coach Validation Commands

```bash
uv run python -c "import yaml; yaml.safe_load(open('coach-config.yaml')); print('coach-config.yaml valid YAML')"
grep -q "ALWAYS" AGENTS.md && grep -q "NEVER" AGENTS.md && grep -q "ASK" AGENTS.md && echo "AGENTS.md boundaries OK"
grep -q "AO1" subjects/gcse-english/SUBJECT.md && echo "SUBJECT.md AO framework OK"
grep -q "provider" coach-config.yaml && echo "coach-config.yaml structure OK"
uv run python -c "import yaml; c = yaml.safe_load(open('coach-config.yaml')); assert 'coach' in c; assert 'provider' in c['coach']; assert 'local' in c['coach']; assert 'api' in c['coach']; print('coach-config structure valid')"
grep -c "ALWAYS\|NEVER\|ASK" AGENTS.md | xargs -I{} python -c "assert int('{}') >= 6, 'Expected at least 6 boundary markers in AGENTS.md'"
echo "AGENTS.md boundary count OK"
```
