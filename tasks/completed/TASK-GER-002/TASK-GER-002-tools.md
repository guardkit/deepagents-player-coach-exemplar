---
id: TASK-GER-002
title: "Tools: search_data and write_output (generic replacements)"
status: completed
completed: "2026-03-16T00:00:00Z"
priority: critical
complexity: 5
type: implementation
task_type: implementation
feature_id: FEAT-DEB
parent_review: TASK-REV-8464
wave: 1
implementation_mode: task-work
dependencies: [TASK-GER-001]
tags: [deepagents, langchain-tools, tavily, tool-decorator, genericity]
---

# Task: Tools — `search_data` and `write_output` (generic replacements)

## Description

Create two `@tool`-decorated functions that demonstrate DeepAgents/LangChain tool
conventions WITHOUT coupling to any specific domain. These replace the domain-specific
`rag_retrieval` (ChromaDB curriculum) and `jsonl_writer` (fine-tuning layer routing)
from the original spec.

Tools return strings (never raise exceptions) per D7. Docstrings are load-bearing
for tool routing per D6.

## Review Finding Reference

TASK-REV-8464 Finding 1 (CRITICAL): Original tools are 100% domain-specific.
Recommendation 1: Replace with generic search_data and write_output.

## Files to Create

- `tools/search_data.py`
- `tools/write_output.py`

## Files NOT to Touch

`tools/__init__.py`, any other files

## API Contracts

### search_data
- Signature: `(query: str, source: str) -> str`
- `query`: The search query string
- `source`: Context hint for the search (e.g., domain name from config)
- Uses Tavily search client (lazy init, not at import time)
- Falls back gracefully when `TAVILY_API_KEY` not set — returns informative error string
- Returns concatenated search result strings on success
- Returns `"no results found for: {query}"` when results empty
- Returns `"error: {reason}"` on failure — never raises

### write_output
- Signature: `(content: str, output_path: str) -> str`
- `content`: Must be valid JSON string — returns error string if not
- `output_path`: Relative path under `output/` directory (e.g., `output/results.jsonl`)
- Validates `content` is valid JSON — returns error string if not
- Validates `output_path` starts with `output/` — returns error string if not (path traversal guard)
- Creates parent directories if needed
- Appends content as a line to the output file (JSONL pattern)
- Returns `"written to {output_path}"` on success
- Never raises exceptions

## Relevant Decisions

- D6: `@tool` decorated functions with docstrings
- D7: Tools return strings, never raise exceptions

## Acceptance Criteria

- [x] `search_data.py` imports `@tool` from `langchain_core.tools`
- [x] `search_data` signature: `(query: str, source: str) -> str`
- [x] Docstring explains: searches for relevant information using the given query and source context
- [x] Tavily client initialised inside function body (lazy), not at module level
- [x] Returns concatenated result strings on success
- [x] Returns `"no results found for: {query}"` when empty — no exception
- [x] Returns `"error: {reason}"` on failure (including missing API key) — no exception
- [x] `write_output.py` imports `@tool` from `langchain_core.tools`
- [x] `write_output` signature: `(content: str, output_path: str) -> str`
- [x] Docstring explains: validates JSON content and appends to the specified output file
- [x] Validates `content` is valid JSON — returns error string if not
- [x] Validates `output_path` starts with `output/` — returns error string if not
- [x] Creates parent directories if needed
- [x] Appends content line to file
- [x] Returns `"written to {output_path}"` on success
- [x] Never raises exceptions under any circumstance
- [x] Import check: `uv run python -c "from tools.search_data import search_data; from tools.write_output import write_output; print('OK')"`
- [x] No references to ChromaDB, curriculum, rag, jsonl_writer, layer, behaviour, knowledge

## Player Constraints

Do not modify `agents/` or `prompts/` files.

## Coach Validation Commands

```bash
uv run python -c "from tools.search_data import search_data; from tools.write_output import write_output; print('Tools import OK')"
uv run python -c "
from tools.write_output import write_output
import json, os, tempfile, shutil
orig = os.getcwd()
tmp = tempfile.mkdtemp()
os.chdir(tmp)
os.makedirs('output', exist_ok=True)
result = write_output.invoke({'content': json.dumps({'key': 'value'}), 'output_path': 'output/test.jsonl'})
assert 'output/test.jsonl' in result, f'Expected output path in result, got: {result}'
result2 = write_output.invoke({'content': 'not-json', 'output_path': 'output/test.jsonl'})
assert 'error' in result2.lower(), f'Expected error for invalid JSON, got: {result2}'
result3 = write_output.invoke({'content': json.dumps({}), 'output_path': '/etc/passwd'})
assert 'error' in result3.lower(), f'Expected error for path traversal, got: {result3}'
os.chdir(orig)
shutil.rmtree(tmp)
print('write_output validation OK')
"
uv run python -c "
from tools.search_data import search_data
result = search_data.invoke({'query': 'test', 'source': 'example'})
assert isinstance(result, str), 'Must return string'
# Without TAVILY_API_KEY set, should return error gracefully
print(f'search_data returned: {result[:80]}...')
print('search_data graceful handling OK')
"
```
