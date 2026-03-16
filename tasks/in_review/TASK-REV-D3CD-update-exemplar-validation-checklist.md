---
id: TASK-REV-D3CD
title: "Update exemplar validation checklist for generic architecture"
status: review_complete
created: 2026-03-16T00:00:00Z
updated: 2026-03-16T00:00:00Z
priority: high
complexity: 5
type: documentation
task_type: review
tags: [deepagents, review, validation, genericity, template]
decision_required: true
related_review: TASK-REV-8464
related_tasks: [TASK-GER-001, TASK-GER-002, TASK-GER-003, TASK-GER-004, TASK-GER-005, TASK-GER-006, TASK-GER-007]
review_results:
  mode: architectural
  depth: standard
  findings_count: 14
  recommendations_count: 1
  decision: implement
  report_path: .claude/reviews/TASK-REV-D3CD-review-report.md
  implementation_task: TASK-IMP-D3CD
---

# Task: Update exemplar validation checklist for generic architecture

## Description

The original validation checklist
(`docs/research/project_template/TASK-REV-deepagents-exemplar-validation.md`)
was written for the domain-specific study-tutor-factory exemplar. TASK-REV-8464
found the exemplar was only 3/10 for template genericity and recommended a full
revision. The TASK-GER-001 through TASK-GER-007 implementation tasks define the
generic replacement architecture.

This review task updates the validation checklist so it validates the **generic**
exemplar — not the original tutor-specific one. If the checklist is not updated,
running `/template-create` will either validate against stale criteria or miss
new generic patterns entirely.

## Scope

Update every section of `TASK-REV-deepagents-exemplar-validation.md` to reflect:

### Section-by-Section Changes Required

**Section 1 (Environment and Dependencies):**
- Replace `chromadb` with `tavily-python` (per TASK-GER-001 scaffold)
- Update import check: `from tools.search_data import search_data` not `rag_retrieval`
- Update `.env.example` vars: add `TAVILY_API_KEY`, remove ChromaDB references

**Section 2 (Agent entrypoint):**
- References to `domains/{domain}/DOMAIN.md` instead of `subjects/`
- `--domain` CLI arg instead of `--subject`
- Default domain is `example-domain` not `gcse-english`

**Section 4 (Subject configuration) → rename to "Domain configuration":**
- Path: `domains/example-domain/DOMAIN.md` not `subjects/gcse-english/SUBJECT.md`
- Remove AQA, exam board, AO1-AO6 framework references
- Replace with generic domain config: evaluation criteria, domain description, quality standards
- Per TASK-GER-005: placeholder content users replace for their domain

**Section 5 (Agent definitions):**
- Tools list: `search_data` and `write_output` (not `rag_retrieval` and `jsonl_writer`)
- Per TASK-GER-004: factory functions import from generic tools/prompts modules

**Section 6 (Tools):**
- Replace `rag_retrieval.py` checklist with `search_data.py` (Tavily web search)
- Replace `jsonl_writer.py` checklist with `write_output.py` (validated file writer)
- Remove ChromaDB lazy init check, layer routing, `train.jsonl`/`rag_index/` references
- Per TASK-GER-002: new tool contracts and validation patterns

**Section 7 (Prompts):**
- Remove 75/25 reasoning/direct split, ShareGPT JSONL format, layer field
- Remove AO1-AO6, Socratic quality metrics from Coach schema
- Replace with generic: `criteria_met`, `quality_assessment` (per TASK-GER-003)
- Coach schema: `decision`, `score`, `issues`, `criteria_met`, `quality_assessment`

**Section 8 (AGENTS.md):**
- Update ALWAYS/NEVER/ASK examples to generic domain language
- Remove GCSE, grade level, AO references

**Section 9 (LangSmith):**
- Update project name from `"study-tutor-factory"` to generic default

**Section 10 (Smoke test):**
- Update imports to generic module names (per TASK-GER-006 smoke test)
- Update CLI args: `--domain example-domain` not `--subject gcse-english`
- Update expected outcomes: generic output file not `train.jsonl`

**Target Structure (top of doc):**
- Replace `subjects/` tree with `domains/` tree
- Replace tool filenames
- Per TASK-GER-001: updated directory layout

**Context paragraph:**
- Remove study-tutor-factory references
- Frame as generic Player-Coach orchestration exemplar
- Reference TASK-REV-8464 decision and TASK-GER revision tasks

**After This Review Passes section:**
- Template name may change from `deepagents-agentic-loop` — verify or make generic
- Remove `study-tutor-factory` project reference

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

This is a documentation-only review task. No Python or config files should be modified.

The updated checklist should be usable as a gate AFTER all TASK-GER tasks complete
and BEFORE running `/template-create`.
