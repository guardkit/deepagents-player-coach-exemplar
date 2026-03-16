---
id: TASK-REV-8464
title: "Review exemplar genericity: specific tutor-factory vs generic DeepAgents template"
status: review_complete
created: 2026-03-16T00:00:00Z
updated: 2026-03-16T00:00:00Z
review_results:
  mode: architectural
  depth: standard
  score: 68
  findings_count: 8
  recommendations_count: 5
  decision: revise
  report_path: .claude/reviews/TASK-REV-8464-review-report.md
priority: critical
complexity: 7
task_type: review
review_mode: architectural
review_depth: standard
tags: [architecture-review, decision-point, deepagents, template-design, genericity]
decision_required: true
feature_id: FEAT-DEB
related_tasks: [TASK-DEB-001, TASK-DEB-002, TASK-DEB-003, TASK-DEB-004, TASK-DEB-005, TASK-DEB-006]
---

# Review: Exemplar Genericity — Specific Tutor-Factory vs Generic DeepAgents Template

## Problem Statement

The FEAT-deepagents-exemplar-build spec and its 6 implementation tasks
(TASK-DEB-001 through TASK-DEB-006) were designed to build a working exemplar
from which `/template-create` will extract a reusable `deepagents-agentic-loop`
project template.

**Concern**: The current spec bakes in domain-specific functionality for the
study-tutor-factory Player-Coach fine-tuning dataset generation use case:

- `rag_retrieval` tool tied to ChromaDB curriculum chunks
- `jsonl_writer` tool with `behaviour`/`knowledge` layer routing
- Coach rejection schema with `ao_correct`, `socratic_quality`, `layer_correct`
- `subjects/gcse-english/SUBJECT.md` with AO1-AO6 framework
- AGENTS.md boundaries referencing GCSE-specific validation
- Prompts specifying ShareGPT JSONL format and `<think>` blocks

If `/template-create` extracts a template from this exemplar, the template will
inherit these domain-specific patterns. Users creating new projects from the
template would need to strip out tutor-factory concerns before adding their own.

**The template should be generic** — demonstrating DeepAgents patterns (tools,
prompts, agent factories, config-driven design, AGENTS.md boundaries) without
coupling to any specific domain.

## Review Scope

1. **Audit all 6 tasks** in `tasks/backlog/deepagents-exemplar-build/` for
   domain-specific leakage that would corrupt the template
2. **Cross-reference with FEAT spec** at
   `docs/research/project_template/FEAT-deepagents-exemplar-build.md`
3. **Assess what has been implemented** — TASK-DEB-001 (scaffold) is complete
4. **Determine the right abstraction level** — what should the exemplar tools,
   prompts, config, and agent roles demonstrate without being tutor-specific?
5. **Propose revised task definitions** if the current ones need to change

## Key Questions

1. Should the exemplar tools be generic placeholders (e.g. `search_tool`,
   `write_output`) or domain-neutral but functional (e.g. web search + file writer)?
2. Should the Coach rejection schema be a generic structured evaluation, or
   should it have no domain-specific fields at all?
3. Should `subjects/` be replaced with a generic `config/` or `domains/` directory?
4. Should AGENTS.md boundaries be generic (any two-agent review pattern) or
   specific to generation-validation loops?
5. What from deep_research and content-builder-agent patterns should be
   preserved vs abstracted?
6. Does TASK-DEB-001 (already implemented) need changes, or is the scaffold
   generic enough?

## Input Documents

- **FEAT spec**: `docs/research/project_template/FEAT-deepagents-exemplar-build.md`
- **Implementation tasks**: `tasks/backlog/deepagents-exemplar-build/`
- **DeepAgents SDK source**: `/Users/richardwoollcott/Projects/appmilla_github/deepagents`
- **DeepAgents examples**: `deep_research/`, `content-builder-agent/` in the SDK repo

## Decision Options (expected at checkpoint)

- **[A]ccept** — Current specificity is acceptable; template-create can abstract
- **[R]evise** — Rewrite tasks 2-6 to be domain-generic
- **[I]mplement** — Create new revised tasks replacing the specific ones
- **[C]ancel** — Abandon this review

## Success Criteria

- Clear recommendation on generic vs specific exemplar architecture
- If revising: concrete list of what changes in each task
- Assessment of TASK-DEB-001 impact (already implemented)
- Revised acceptance criteria for affected tasks
