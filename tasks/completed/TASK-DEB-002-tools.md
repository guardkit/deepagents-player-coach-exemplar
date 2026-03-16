---
id: TASK-DEB-002
title: "Tools: rag_retrieval and jsonl_writer"
status: superseded
superseded_by: TASK-GER-002
superseded_reason: "TASK-REV-8464 genericity review — domain-specific tools replaced with generic equivalents"
priority: high
complexity: 5
type: implementation
task_type: implementation
feature_id: FEAT-DEB
parent_review: FEAT-deepagents-exemplar-build
wave: 1
implementation_mode: task-work
dependencies: [TASK-DEB-001]
tags: [deepagents, langchain-tools, chromadb, jsonl, tool-decorator]
---

# Task: Tools — `rag_retrieval` and `jsonl_writer`

## Description

Create two `@tool`-decorated functions following DeepAgents/LangChain conventions.
Tools return strings (never raise exceptions) per D7. Docstrings are load-bearing
for tool routing per D6.

## Files to Create

- `tools/rag_retrieval.py`
- `tools/jsonl_writer.py`

## Files NOT to Touch

`tools/__init__.py`, any other files

## API Contracts

### rag_retrieval
- Signature: `(query: str, subject: str) -> str`
- ChromaDB client initialised inside function body (lazy, not at import time)
- Returns concatenated chunk strings on success
- Returns `"no results found for subject: {subject}"` when collection empty
- Returns `"error: {reason}"` on failure — never raises

### jsonl_writer
- Signature: `(example: str, layer: str) -> str`
- Validates `example` is valid JSON — returns error string if not
- Validates `layer` is `"behaviour"` or `"knowledge"` — returns error string if not
- Routes `behaviour` → appends to `train.jsonl`
- Routes `knowledge` → appends to `rag_index/knowledge.jsonl` (creates dir if needed)
- Returns `"written to train.jsonl"` or `"written to rag_index/"` on success
- Never raises exceptions

## Relevant Decisions

- D6: `@tool` decorated functions with docstrings
- D7: Tools return strings, never raise exceptions

## Acceptance Criteria

- [ ] `rag_retrieval.py` imports `@tool` from `langchain_core.tools`
- [ ] `rag_retrieval` signature: `(query: str, subject: str) -> str`
- [ ] Docstring explains: retrieves relevant curriculum chunks from ChromaDB
- [ ] ChromaDB client initialised inside function body (lazy), not at module level
- [ ] Returns concatenated chunk strings on success
- [ ] Returns `"no results found for subject: {subject}"` when empty — no exception
- [ ] Returns `"error: {reason}"` on failure — no exception
- [ ] `jsonl_writer.py` imports `@tool` from `langchain_core.tools`
- [ ] `jsonl_writer` signature: `(example: str, layer: str) -> str`
- [ ] Docstring explains: validates and writes accepted training example
- [ ] Validates `example` is valid JSON — returns error string if not
- [ ] Validates `layer` is `"behaviour"` or `"knowledge"` — returns error string if not
- [ ] Routes correctly based on layer
- [ ] Returns success strings on write
- [ ] Never raises exceptions under any circumstance
- [ ] Import check: `uv run python -c "from tools.rag_retrieval import rag_retrieval; from tools.jsonl_writer import jsonl_writer; print('OK')"`

## Player Constraints

Do not modify `agents/` or `prompts/` files.

## Coach Validation Commands

```bash
uv run python -c "from tools.rag_retrieval import rag_retrieval; from tools.jsonl_writer import jsonl_writer; print('Tools import OK')"
uv run python -c "
from tools.jsonl_writer import jsonl_writer
import json, os, tempfile, shutil
tmp = tempfile.mkdtemp()
os.chdir(tmp)
result = jsonl_writer.invoke({'example': json.dumps({'messages': []}), 'layer': 'behaviour'})
assert 'train.jsonl' in result, f'Expected train.jsonl routing, got: {result}'
result2 = jsonl_writer.invoke({'example': 'not-json', 'layer': 'behaviour'})
assert 'error' in result2.lower(), f'Expected error for invalid JSON, got: {result2}'
result3 = jsonl_writer.invoke({'example': json.dumps({}), 'layer': 'invalid'})
assert 'error' in result3.lower(), f'Expected error for invalid layer, got: {result3}'
shutil.rmtree(tmp)
print('jsonl_writer validation OK')
"
uv run python -c "
from tools.rag_retrieval import rag_retrieval
result = rag_retrieval.invoke({'query': 'test', 'subject': 'nonexistent-subject'})
assert isinstance(result, str), 'Must return string'
assert 'error' in result.lower() or 'no results' in result.lower(), f'Expected graceful empty result, got: {result}'
print('rag_retrieval graceful empty OK')
"
```
