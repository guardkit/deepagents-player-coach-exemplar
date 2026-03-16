---
id: TASK-GER-005
title: "AGENTS.md, coach-config, and domain configuration (generic)"
status: completed
completed: 2026-03-16
priority: high
complexity: 5
type: implementation
task_type: implementation
feature_id: FEAT-DEB
parent_review: TASK-REV-8464
wave: 1
implementation_mode: task-work
dependencies: [TASK-GER-001]
tags: [deepagents, agents-md, config-driven, domain-agnostic, genericity]
---

# Task: AGENTS.md, coach-config, and domain configuration (generic)

## Description

Create the agent boundary documentation (`AGENTS.md`), configurable Coach model
selection (`coach-config.yaml`), and the example domain configuration
(`domains/example-domain/DOMAIN.md`).

This replaces TASK-DEB-005, removing all GCSE/tutor-specific content while
preserving the configuration patterns.

AGENTS.md is loaded at runtime via `memory=["./AGENTS.md"]` in the agent factory
functions — MemoryMiddleware injects boundaries into the system prompt.

`domains/example-domain/DOMAIN.md` is custom config read by `agent.py` — NOT a
DeepAgents skill.

## Review Finding Reference

TASK-REV-8464 Finding 3 (HIGH): AGENTS.md boundaries reference domain tools and
concepts. Recommendation 3: Rewrite with generic two-agent boundaries.
TASK-REV-8464 Finding 7 (OBSERVATION): coach-config.yaml already mostly generic.
TASK-REV-8464 Finding 8 (OBSERVATION): domains/ pattern correct, needs renaming.

## Files to Create

- `AGENTS.md`
- `coach-config.yaml`
- `domains/example-domain/DOMAIN.md`

## Files NOT to Touch

Any Python files

## Acceptance Criteria

### AGENTS.md
- [x] Contains `## Player Agent` section
- [x] Contains `## Coach Agent` section
- [x] Each section has `ALWAYS:`, `NEVER:`, `ASK:` subsections
- [x] Player ALWAYS: call search_data before generating content, produce valid JSON output, include source references
- [x] Player NEVER: write output without Coach approval, generate more than one item per turn, skip search step
- [x] Coach ALWAYS: return structured JSON evaluation, evaluate against domain criteria from DOMAIN.md, check content quality
- [x] Coach NEVER: write to output files, modify content directly, return prose instead of JSON
- [x] Coach ASK: when score is 3 (borderline) — escalate for human review
- [x] Does NOT reference: rag_retrieval, jsonl_writer, layer, behaviour, knowledge, AO, GCSE, curriculum, Socratic, think blocks

### coach-config.yaml
- [x] Parses as valid YAML
- [x] Contains `coach.provider` field (value: `local`)
- [x] Contains `coach.local.model` and `coach.local.endpoint` fields
- [x] Contains `coach.api.model` field
- [x] Default `provider` is `local`

### domains/example-domain/DOMAIN.md
- [x] Contains `## Domain Description` section — brief description of the example domain
- [x] Contains `## Generation Guidelines` section — what Player should generate
- [x] Contains `## Evaluation Criteria` section — what Coach should evaluate against
- [x] Contains `## Output Format` section — expected structure of generated content
- [x] Content is clearly a GENERIC EXAMPLE that users replace with their own domain
- [x] Includes inline comments/notes indicating "replace this with your domain"
- [x] Does NOT contain: AO1-AO6, exam_board, AQA, specifications, GCSE, Socratic, curriculum
- [x] Does NOT contain any Python code

## Player Constraints

Do not modify any Python files in this task. Configuration and documentation only.

## Coach Validation Commands

```bash
uv run python -c "import yaml; yaml.safe_load(open('coach-config.yaml')); print('coach-config.yaml valid YAML')"
grep -q "ALWAYS" AGENTS.md && grep -q "NEVER" AGENTS.md && grep -q "ASK" AGENTS.md && echo "AGENTS.md boundaries OK"
grep -q "Generation Guidelines" domains/example-domain/DOMAIN.md && echo "DOMAIN.md structure OK"
grep -q "Evaluation Criteria" domains/example-domain/DOMAIN.md && echo "DOMAIN.md criteria OK"
grep -q "provider" coach-config.yaml && echo "coach-config.yaml structure OK"
uv run python -c "import yaml; c = yaml.safe_load(open('coach-config.yaml')); assert 'coach' in c; assert 'provider' in c['coach']; assert 'local' in c['coach']; assert 'api' in c['coach']; print('coach-config structure valid')"
grep -c "ALWAYS\|NEVER\|ASK" AGENTS.md | xargs -I{} python3 -c "assert int('{}') >= 6, 'Expected at least 6 boundary markers in AGENTS.md'"
echo "AGENTS.md boundary count OK"
# Domain-specific terms must NOT appear
! grep -qi "gcse\|AO1\|socratic\|curriculum\|rag_retrieval\|jsonl_writer\|layer_correct" AGENTS.md && echo "AGENTS.md generic OK"
! grep -qi "gcse\|AO1\|AQA\|socratic\|curriculum" domains/example-domain/DOMAIN.md && echo "DOMAIN.md generic OK"
```
