---
id: TASK-IMP-D3CD
title: "Rewrite exemplar validation checklist for generic architecture"
status: in_review
created: 2026-03-16T00:00:00Z
updated: 2026-03-16T00:00:00Z
priority: high
complexity: 5
type: documentation
task_type: implementation
parent_review: TASK-REV-D3CD
feature_id: FEAT-DEB
tags: [deepagents, validation, genericity, template, documentation]
related_tasks: [TASK-GER-001, TASK-GER-002, TASK-GER-003, TASK-GER-004, TASK-GER-005, TASK-GER-006]
implementation_mode: task-work
dependencies: []
---

# Task: Rewrite exemplar validation checklist for generic architecture

## Description

Full section-by-section rewrite of
`docs/research/project_template/TASK-REV-deepagents-exemplar-validation.md`
to validate the **generic** exemplar architecture defined by TASK-GER-001
through TASK-GER-007, replacing all study-tutor-factory domain-specific content.

This is the single implementation task from TASK-REV-D3CD review findings.
Review report: `.claude/reviews/TASK-REV-D3CD-review-report.md`

## File to Modify

- `docs/research/project_template/TASK-REV-deepagents-exemplar-validation.md`

## No Other Files Should Be Modified

This is a documentation-only task. No Python, YAML, or config files should change.

## Section-by-Section Rewrite Spec

Use the completed TASK-GER specifications as the authoritative source for each section.

### Header & Context (Source: TASK-GER-001)
- Title: "Before running /template-create for deepagents-exemplar"
- Remove all "study-tutor-factory" references
- Frame as generic Player-Coach orchestration exemplar
- Reference TASK-REV-8464 decision and TASK-GER revision tasks
- Keep prerequisite for `/template-create` framing

### Target Structure (Source: TASK-GER-001, GER-002)
Replace directory tree:
```
domains/
  └── example-domain/
      └── DOMAIN.md
tools/
  ├── search_data.py
  └── write_output.py
```
Remove `subjects/`, `rag_retrieval.py`, `jsonl_writer.py`.

### Section 1: Environment and Dependencies (Source: TASK-GER-001)
- Remove `chromadb` check — replace with `tavily-python`
- Import check: `from tools.search_data import search_data` (not `import chromadb`)
- `.env.example` vars: add `TAVILY_API_KEY`, `LANGSMITH_PROJECT=deepagents-exemplar`
- Remove `LANGSMITH_PROJECT=study-tutor-factory`

### Section 2: Agent entrypoint (Source: TASK-GER-006)
- References to `domains/{domain}/DOMAIN.md` instead of `subjects/`
- `--domain` CLI arg instead of `--subject`
- Default domain is `example-domain` not `gcse-english`
- Smoke test: `--domain example-domain`

### Section 3: Coach configuration — no changes needed
- coach-config.yaml structure is already generic (per TASK-GER-005)

### Section 4: Rename to "Domain configuration" (Source: TASK-GER-005)
- Path: `domains/example-domain/DOMAIN.md`
- Validate sections: `Domain Description`, `Generation Guidelines`, `Evaluation Criteria`, `Output Format`
- Verify placeholder content indicating "replace with your domain"
- Remove AQA, exam board, AO1-AO6, specifications references

### Section 5: Agent definitions (Source: TASK-GER-004)
- Player tools: `search_data` and `write_output` (not `rag_retrieval`/`jsonl_writer`)
- Factory signatures: `create_player(model, domain_prompt: str)`, `create_coach(model, domain_prompt: str)`
- Player uses `FilesystemBackend(root_dir=".")`
- Coach has NO custom tools, does NOT use FilesystemBackend
- Both pass `memory=["./AGENTS.md"]`
- Anti-patterns: same as before but updated tool names

### Section 6: Tools (Source: TASK-GER-002)
Replace entire section with:
- **search_data.py**: `@tool`, `(query: str, source: str) -> str`, Tavily lazy init, graceful TAVILY_API_KEY fallback, returns strings never raises
- **write_output.py**: `@tool`, `(content: str, output_path: str) -> str`, JSON validation, path traversal guard (`output/` prefix), parent dir creation, JSONL append
- Remove all ChromaDB, layer routing, train.jsonl, rag_index references

### Section 7: Prompts (Source: TASK-GER-003)
- Player prompt: instructs search_data before generating, output valid JSON with `content` field, write_output only after Coach accepts
- Coach prompt schema:
  ```json
  {
    "decision": "accept | reject",
    "score": 1-5,
    "issues": ["..."],
    "criteria_met": true | false,
    "quality_assessment": "high | adequate | needs_revision"
  }
  ```
- Remove: ShareGPT, 75/25 split, layer field, AO1-AO6, Socratic quality

### Section 8: AGENTS.md (Source: TASK-GER-005)
- Player ALWAYS: call search_data before generating, produce valid JSON, include source references
- Player NEVER: write output without Coach approval, generate more than one item per turn, skip search
- Coach ALWAYS: return structured JSON evaluation, evaluate against domain criteria from DOMAIN.md
- Coach NEVER: write to output files, modify content directly, return prose instead of JSON
- Coach ASK: when score is 3 (borderline) — escalate for human review

### Section 9: LangSmith (Source: TASK-GER-001)
- Project name: `"deepagents-exemplar"` (not `"study-tutor-factory"`)

### Section 10: Smoke test (Source: TASK-GER-006)
- CLI: `--domain example-domain` (not `--subject gcse-english`)
- Imports: `create_player`, `create_coach`, `search_data`, `write_output`, `PLAYER_SYSTEM_PROMPT`, `COACH_SYSTEM_PROMPT`
- Expected outcome: output under `output/` directory, not `train.jsonl`
- Match TASK-GER-006 coach validation commands

### PASS/FAIL criteria
- Update tool/prompt references to generic equivalents
- Add: "No domain-specific terms in prompts or tool docstrings"

### "After this review passes" section
- Remove `study-tutor-factory` project reference
- Make template name generic or note it may vary
- Update `cd` command to generic

### Footer
- Update attribution to reference generic exemplar and TASK-REV-8464

## Acceptance Criteria

- [ ] No references to: `study-tutor-factory`, `gcse-english`, `SUBJECT.md`, `subjects/`, `AQA`, `AO1-AO6`, `Socratic`, `rag_retrieval`, `jsonl_writer`, `ChromaDB`, `chromadb`, `train.jsonl`, `rag_index/`, `layer` (in routing context)
- [ ] All tool references use `search_data` and `write_output`
- [ ] All path references use `domains/` not `subjects/`
- [ ] Coach evaluation schema uses `criteria_met`/`quality_assessment`
- [ ] Smoke test section matches TASK-GER-006 validation commands
- [ ] Context paragraph references TASK-REV-8464 and generic architecture decision
- [ ] `.env.example` checks include `TAVILY_API_KEY`
- [ ] Section 4 renamed from "Subject configuration" to "Domain configuration"
- [ ] PASS/FAIL criteria updated for generic architecture
- [ ] Document remains a usable pre-`/template-create` gate

## Validation Commands

```bash
# Verify no domain-specific terms remain
! grep -qi "study-tutor-factory\|gcse-english\|SUBJECT\.md\|subjects/\|rag_retrieval\|jsonl_writer\|chromadb\|train\.jsonl\|rag_index\|socratic_quality\|ao_correct\|layer_correct" docs/research/project_template/TASK-REV-deepagents-exemplar-validation.md && echo "Generic OK" || echo "FAIL: domain-specific terms found"

# Verify generic terms present
grep -q "search_data" docs/research/project_template/TASK-REV-deepagents-exemplar-validation.md && echo "search_data OK"
grep -q "write_output" docs/research/project_template/TASK-REV-deepagents-exemplar-validation.md && echo "write_output OK"
grep -q "domains/" docs/research/project_template/TASK-REV-deepagents-exemplar-validation.md && echo "domains/ OK"
grep -q "criteria_met" docs/research/project_template/TASK-REV-deepagents-exemplar-validation.md && echo "Generic schema OK"
grep -q "TASK-REV-8464" docs/research/project_template/TASK-REV-deepagents-exemplar-validation.md && echo "Review reference OK"
grep -q "TAVILY_API_KEY" docs/research/project_template/TASK-REV-deepagents-exemplar-validation.md && echo "Tavily env var OK"
```

## Implementation Notes

- This is documentation-only. No Python or config files should be modified.
- Use completed TASK-GER task files as authoritative source material.
- The updated checklist should be usable as a gate AFTER all TASK-GER tasks complete and BEFORE running `/template-create`.
- TASK-GER-004 is in review and TASK-GER-006 is in backlog — their specs are final, so the rewrite can proceed now.
