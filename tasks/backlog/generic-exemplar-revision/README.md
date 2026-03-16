# Feature: Generic Exemplar Revision

## Problem

The original FEAT-deepagents-exemplar-build spec baked in study-tutor-factory
domain logic (ChromaDB retrieval, JSONL fine-tuning format, GCSE AO marking
framework, Socratic quality metrics) into what should be a domain-neutral template
exemplar. The TASK-REV-8464 architectural review scored template genericity at
3/10 and recommended revising tasks 2, 3, and 5.

If `/template-create` extracted a template from the domain-specific exemplar,
every new project would need to strip out tutor-factory concerns before starting.

## Solution

Revise the exemplar to demonstrate DeepAgents patterns generically:
- **Generic tools**: `search_data` (Tavily web search) and `write_output` (validated file writer)
- **Generic prompts**: Player-Coach adversarial cooperation without domain-specific evaluation criteria
- **Generic config**: `domains/example-domain/DOMAIN.md` with placeholder content users replace
- **Generic evaluation schema**: `criteria_met` / `quality_assessment` instead of AO/Socratic fields

Architecture preserved: Player-Coach peer agents, factory functions, config-driven
domains, structured JSON evaluation, `FilesystemBackend` vs `StateBackend` distinction.

## Tasks

| ID | Title | Complexity | Wave | Depends On |
|----|-------|-----------|------|------------|
| TASK-GER-001 | Scaffold fixes | 2 | 1 | -- |
| TASK-GER-002 | Generic tools | 5 | 1 | 001 |
| TASK-GER-003 | Generic prompts | 7 | 1 | 001 |
| TASK-GER-005 | Generic config | 5 | 1 | 001 |
| TASK-GER-004 | Agent factories | 5 | 2 | 002, 003 |
| TASK-GER-006 | Entrypoint | 7 | 2 | 004, 005 |
| TASK-GER-007 | FEAT spec update | 5 | 2 | 002, 003, 005 |

## Getting Started

```bash
# Wave 1: scaffold first, then parallel
/task-work TASK-GER-001

# After 001 completes — parallel via Conductor
/task-work TASK-GER-002
/task-work TASK-GER-003
/task-work TASK-GER-005

# Wave 2: sequential (004 first, then 006+007 parallel)
/task-work TASK-GER-004
/task-work TASK-GER-006
/task-work TASK-GER-007

# Verify
# Run smoke test from TASK-GER-006
# Then /task-review for validation gate
# Then /template-create to extract template
```
