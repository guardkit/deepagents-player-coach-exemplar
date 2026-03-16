---
id: TASK-GER-007
title: "Update FEAT spec for generic exemplar"
status: completed
completed: 2026-03-16T00:00:00Z
completed_location: tasks/completed/TASK-GER-007/
priority: high
complexity: 5
type: documentation
task_type: implementation
feature_id: FEAT-DEB
parent_review: TASK-REV-8464
wave: 2
implementation_mode: task-work
dependencies: [TASK-GER-002, TASK-GER-003, TASK-GER-005]
tags: [deepagents, documentation, feat-spec, genericity]
---

# Task: Update FEAT spec for generic exemplar

## Description

Update `docs/research/project_template/FEAT-deepagents-exemplar-build.md` to
reflect the generic exemplar architecture. The FEAT spec is the authoritative
design document — it must accurately describe what is being built.

This task also updates the IMPLEMENTATION-GUIDE.md and README.md in the
`tasks/backlog/deepagents-exemplar-build/` directory, and archives the original
domain-specific task files.

## Review Finding Reference

TASK-REV-8464: All recommendations. The FEAT spec must be updated to match the
revised generic architecture.

## Files to Modify

- `docs/research/project_template/FEAT-deepagents-exemplar-build.md`
- `tasks/backlog/deepagents-exemplar-build/IMPLEMENTATION-GUIDE.md`
- `tasks/backlog/deepagents-exemplar-build/README.md`

## Changes Required

### FEAT Spec Updates

1. **Section 1 (Problem Statement)**: Remove "study-tutor-factory Player-Coach
   data generation" reference. Replace with generic: "two-agent Player-Coach
   orchestration pattern from the Adversarial Cooperation paper"

2. **Decision Log**: Update:
   - D5: Generic structured JSON evaluation schema (not tutor-specific fields)
   - D6: Generic tool examples (search_data, write_output)
   - D9: `domains/` directory (not `subjects/`)
   - Warnings: Update tool names, remove ChromaDB constraint, update directory refs

3. **Section 3 (Architecture)**:
   - Component table: Replace rag_retrieval/jsonl_writer with search_data/write_output
   - Replace subjects/ with domains/
   - Data flow: Generic search→generate→evaluate→write flow
   - Remove output routing section (no layer concept)

4. **Section 4 (API Contracts)**:
   - Coach schema: Replace `ao_correct`/`socratic_quality`/`layer_correct` with
     `criteria_met`/`quality_assessment`
   - Tool contracts: search_data and write_output signatures

5. **Section 5 (Tasks)**: Reference TASK-GER-001 through TASK-GER-007 as the
   active implementation tasks. Note original TASK-DEB-002/003/005 superseded.

6. **Section 6 (Test Strategy)**: Update smoke test to use generic imports

7. **Section 8 (File Tree)**: Update to generic structure

8. **Section 11 (Revision Log)**: Add entry for TASK-REV-8464 genericity review

### IMPLEMENTATION-GUIDE.md Updates

- Update task references from DEB to GER
- Update file conflict analysis with generic filenames
- Update critical review findings for generic tools/prompts

### README.md Updates

- Update feature description for generic exemplar
- Update task table with GER task IDs

## Acceptance Criteria

- [ ] FEAT spec Section 1 does not reference "study-tutor-factory"
- [ ] FEAT spec D5 describes generic evaluation schema
- [ ] FEAT spec component table lists search_data, write_output (not rag_retrieval, jsonl_writer)
- [ ] FEAT spec API contracts use generic schema fields
- [ ] FEAT spec file tree shows `domains/` not `subjects/`
- [ ] FEAT spec revision log includes TASK-REV-8464 entry
- [ ] FEAT spec smoke test uses generic imports
- [ ] IMPLEMENTATION-GUIDE references TASK-GER tasks
- [ ] README references generic exemplar
- [ ] No references to: GCSE, AQA, AO1-AO6, Socratic, curriculum, train.jsonl, rag_index, ChromaDB (in active/current sections — historical revision log may reference)

## Player Constraints

Documentation changes only. Do not modify any Python or config files.

## Coach Validation Commands

```bash
# FEAT spec generic checks
! grep -qi "study-tutor-factory" docs/research/project_template/FEAT-deepagents-exemplar-build.md && echo "No study-tutor-factory refs OK" || echo "WARN: study-tutor-factory still referenced"
grep -q "search_data" docs/research/project_template/FEAT-deepagents-exemplar-build.md && echo "search_data present OK"
grep -q "write_output" docs/research/project_template/FEAT-deepagents-exemplar-build.md && echo "write_output present OK"
grep -q "domains/" docs/research/project_template/FEAT-deepagents-exemplar-build.md && echo "domains/ present OK"
grep -q "criteria_met" docs/research/project_template/FEAT-deepagents-exemplar-build.md && echo "Generic schema OK"
grep -q "TASK-REV-8464" docs/research/project_template/FEAT-deepagents-exemplar-build.md && echo "Revision log updated OK"
grep -q "TASK-GER" tasks/backlog/deepagents-exemplar-build/IMPLEMENTATION-GUIDE.md && echo "IMPL-GUIDE updated OK"
```
