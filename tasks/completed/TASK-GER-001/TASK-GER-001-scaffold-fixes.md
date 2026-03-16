---
id: TASK-GER-001
title: "Scaffold fixes: remove domain artifacts from TASK-DEB-001 output"
status: completed
completed: "2026-03-16T00:00:00Z"
priority: high
complexity: 2
type: configuration
task_type: implementation
feature_id: FEAT-DEB
parent_review: TASK-REV-8464
wave: 1
implementation_mode: task-work
dependencies: []
tags: [deepagents, scaffold, genericity, cleanup]
---

# Task: Scaffold fixes — remove domain artifacts from TASK-DEB-001 output

## Description

TASK-DEB-001 (repo scaffold) is already implemented and in review. This task
applies surgical fixes to remove study-tutor-factory domain artifacts identified
in the TASK-REV-8464 architectural review. The scaffold structure is sound —
only content changes needed.

## Review Finding Reference

TASK-REV-8464 Finding 4 (LOW): Scaffold has minor domain artifacts including
`chromadb>=0.5` dependency, `subjects/gcse-english/` directory, domain-specific
.gitignore entries, and cosmetic text references.

## Changes Required

### pyproject.toml
- Change `name` to `"deepagents-exemplar"`
- Change `description` to `"DeepAgents exemplar demonstrating two-agent Player-Coach orchestration"`
- Remove `chromadb>=0.5` from dependencies
- Add `tavily-py>=0.5` to dependencies (for generic search_data tool)

### .env.example
- Change `LANGSMITH_PROJECT=study-tutor-factory` to `LANGSMITH_PROJECT=deepagents-exemplar`
- Add `TAVILY_API_KEY=your-tavily-api-key` (required for search_data tool)

### .gitignore
- Remove `train.jsonl` entry
- Remove `rag_index/` entry
- Add `output/` entry (generic output directory for write_output tool)

### Directory rename
- Rename `subjects/gcse-english/` to `domains/example-domain/`
- Move `.gitkeep` to new location

### langgraph.json
- Change `"data_factory"` to `"agent"` in graphs key

### README.md
- Rewrite to describe generic two-agent Player-Coach orchestration exemplar
- Remove "study tutor" and "educational content" references
- Keep setup instructions (uv sync, .env, usage)

## Files to Modify

- `pyproject.toml`
- `.env.example`
- `.gitignore`
- `langgraph.json`
- `README.md`

## Files to Create/Move

- `domains/example-domain/.gitkeep` (moved from `subjects/gcse-english/.gitkeep`)

## Files to Delete

- `subjects/gcse-english/.gitkeep`
- `subjects/gcse-english/` (empty dir)
- `subjects/` (empty dir)

## Acceptance Criteria

- [x] `pyproject.toml` name is `"deepagents-exemplar"`
- [x] `chromadb` not in dependencies
- [x] `tavily-py>=0.5` in dependencies
- [x] `uv sync` completes without errors
- [x] `.env.example` has `LANGSMITH_PROJECT=deepagents-exemplar`
- [x] `.env.example` has `TAVILY_API_KEY` entry
- [x] `.gitignore` does NOT contain `train.jsonl` or `rag_index/`
- [x] `.gitignore` contains `output/`
- [x] `domains/example-domain/.gitkeep` exists
- [x] `subjects/` directory does NOT exist
- [x] `langgraph.json` contains `"agent"` not `"data_factory"`
- [x] README.md does not contain "study tutor" or "educational content"
- [x] No secrets present in any tracked file

## Coach Validation Commands

```bash
uv sync
grep -q '"deepagents-exemplar"' pyproject.toml && echo "Name OK"
! grep -q "chromadb" pyproject.toml && echo "ChromaDB removed OK"
grep -q "tavily" pyproject.toml && echo "Tavily added OK"
grep -q "TAVILY_API_KEY" .env.example && echo "Tavily env OK"
grep -q "LANGSMITH_PROJECT=deepagents-exemplar" .env.example && echo "Project name OK"
! grep -q "train.jsonl" .gitignore && echo "train.jsonl removed OK"
grep -q "output/" .gitignore && echo "output/ added OK"
test -d domains/example-domain && echo "domains dir OK"
! test -d subjects && echo "subjects removed OK"
grep -q '"agent"' langgraph.json && echo "Graph name OK"
! grep -qi "study tutor" README.md && echo "README generic OK"
```
