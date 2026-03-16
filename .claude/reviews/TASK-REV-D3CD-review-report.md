# Review Report: TASK-REV-D3CD

## Executive Summary

The current validation checklist (`docs/research/project_template/TASK-REV-deepagents-exemplar-validation.md`) is **100% domain-specific** to the original study-tutor-factory exemplar. Every section contains references that no longer match the generic architecture defined by TASK-GER-001 through TASK-GER-007. Running `/template-create` against this checklist would either validate against stale criteria or miss the new generic patterns entirely.

**42 specific changes** required across all 10 sections plus header/footer. 18 are critical (block `/template-create`), 14 are high priority (produce misleading validation), 10 are medium (cosmetic/naming).

**Recommendation: Full rewrite** — the density of changes (every section, every subsection) means editing in place is less efficient than rewriting the document section by section against the completed TASK-GER specifications.

---

## Review Details

- **Mode**: Architectural Review (documentation)
- **Depth**: Standard
- **Task**: TASK-REV-D3CD
- **Related**: TASK-REV-8464 (original genericity finding), TASK-GER-001–007 (implementation)
- **Reviewer**: Architectural review (manual cross-reference analysis)

---

## Findings

### F1 (CRITICAL): Header and Context — study-tutor-factory framing

**Current**: Title says "Before running /template-create for study-tutor-factory". Context paragraph describes assembling from two LangChain examples into a "study-tutor-factory Player-Coach data generation pattern."

**Required**: Reframe as generic Player-Coach orchestration exemplar. Reference TASK-REV-8464 decision to revise from tutor-specific to generic. Remove "study-tutor-factory" entirely.

**Evidence**: TASK-GER-001 renamed project to `deepagents-exemplar`.

---

### F2 (CRITICAL): Target Structure — subjects/ tree and tool filenames

**Current**:
```
subjects/
  └── gcse-english/
      └── SUBJECT.md
tools/
  ├── rag_retrieval.py
  └── jsonl_writer.py
```

**Required** (per TASK-GER-001, GER-002):
```
domains/
  └── example-domain/
      └── DOMAIN.md
tools/
  ├── search_data.py
  └── write_output.py
```

---

### F3 (CRITICAL): Section 1 — Dependencies

| Item | Current | Required (per TASK-GER-001) |
|------|---------|---------------------------|
| ChromaDB dependency | `chromadb` present | Remove — replaced by `tavily-python` |
| ChromaDB import check | `import chromadb` | Replace with `from tools.search_data import search_data` |
| .env.example vars | No TAVILY_API_KEY | Add `TAVILY_API_KEY` |
| Project name | `study-tutor-factory` | `deepagents-exemplar` |

---

### F4 (CRITICAL): Section 2 — Agent entrypoint

| Item | Current | Required (per TASK-GER-006) |
|------|---------|---------------------------|
| Config reference | `subjects/` | `domains/{domain}/DOMAIN.md` |
| CLI arg | `--subject` | `--domain` |
| Default value | `gcse-english` | `example-domain` |
| Smoke test | `--subject gcse-english` | `--domain example-domain` |

---

### F5 (CRITICAL): Section 4 — Subject configuration → Domain configuration

**Current**: Validates `subjects/gcse-english/SUBJECT.md` with `exam_board`, `specifications`, `ao_framework` (AO1-AO6).

**Required** (per TASK-GER-005):
- Rename section to "Domain configuration"
- Path: `domains/example-domain/DOMAIN.md`
- Validate: `Domain Description`, `Generation Guidelines`, `Evaluation Criteria`, `Output Format` sections
- Verify placeholder content users replace for their domain
- Remove all AQA, exam board, AO1-AO6, specification references

---

### F6 (CRITICAL): Section 5 — Agent definitions

**Current**: Player tools list: `rag_retrieval` and `jsonl_writer`. Factory signature: `create_player(model, tools, subject_config)`.

**Required** (per TASK-GER-004):
- Player tools: `search_data` and `write_output`
- Factory signature: `create_player(model, domain_prompt: str)`
- Coach factory: `create_coach(model, domain_prompt: str)` — no tools, no FilesystemBackend
- Both pass `memory=["./AGENTS.md"]`

---

### F7 (CRITICAL): Section 6 — Tools

**Current**: Validates `rag_retrieval.py` (ChromaDB client, collection handling, subject param) and `jsonl_writer.py` (layer routing to train.jsonl/rag_index/).

**Required** (per TASK-GER-002):
- **search_data.py**: `(query: str, source: str) -> str`, Tavily lazy init, graceful fallback when TAVILY_API_KEY not set, returns concatenated results or error strings
- **write_output.py**: `(content: str, output_path: str) -> str`, JSON validation, path traversal guard (`output/` prefix), parent dir creation, JSONL append pattern

---

### F8 (CRITICAL): Section 7 — Prompts

**Current**: Validates ShareGPT JSONL format, 75/25 reasoning/direct split, layer field, AO1-AO6 references, Socratic quality metrics. Coach schema includes `ao_correct`, `socratic_quality`, `layer_correct`.

**Required** (per TASK-GER-003):
- Player: instructs to call `search_data` before generating, output valid JSON with `content` field, call `write_output` only after Coach accepts
- Coach schema: `decision`, `score`, `issues`, `criteria_met`, `quality_assessment`
- Remove all domain-specific evaluation criteria

---

### F9 (HIGH): Section 8 — AGENTS.md

**Current**: ALWAYS/NEVER/ASK examples reference "grade level", "75% of examples", "think blocks", "layer field routing".

**Required** (per TASK-GER-005):
- Player ALWAYS: call search_data before generating, produce valid JSON, include source references
- Player NEVER: write output without Coach approval, generate more than one item per turn, skip search
- Coach ALWAYS: return structured JSON, evaluate against domain criteria from DOMAIN.md
- Coach NEVER: write to output files, modify content directly, return prose instead of JSON

---

### F10 (HIGH): Section 9 — LangSmith

**Current**: `LANGSMITH_PROJECT` set to `"study-tutor-factory"`.

**Required**: Generic default — `"deepagents-exemplar"` per TASK-GER-001.

---

### F11 (HIGH): Section 10 — Smoke test

**Current**: `--subject gcse-english`, imports `rag_retrieval`/`jsonl_writer`, expects `train.jsonl` output.

**Required** (per TASK-GER-006):
- `--domain example-domain`
- Imports: `search_data`, `write_output`, `create_player`, `create_coach`
- Expected outcome: generic output file under `output/`, not `train.jsonl`
- Smoke test matches TASK-GER-006 coach validation commands

---

### F12 (MEDIUM): PASS/FAIL criteria

**Current**: References anti-patterns using old tool names. "Coach and Player use identical system prompts" still valid.

**Required**: Update tool/prompt references to generic equivalents. Add: "No domain-specific terms in prompts or tool docstrings".

---

### F13 (MEDIUM): "After this review passes" section

**Current**: References `study-tutor-factory`, `deepagents-agentic-loop` template name.

**Required**: Remove study-tutor-factory. Make template name generic or note it may vary. Reference TASK-REV-8464 decision.

---

### F14 (MEDIUM): Footer and attribution

**Current**: `*TASK-REV prepared March 2026 | study-tutor-factory pre-work*`

**Required**: Update to reference generic exemplar and TASK-REV-8464 decision.

---

## Recommendations

### R1: Full section-by-section rewrite (Recommended)

Rewrite the validation checklist document using the completed TASK-GER specifications as the source of truth. This is more efficient than 42 individual edits because every section is affected.

**Subtasks**:
1. Rewrite header/context (reference TASK-REV-8464 decision)
2. Rewrite target structure (domains/, search_data, write_output)
3. Rewrite Section 1 (tavily, TAVILY_API_KEY, deepagents-exemplar)
4. Rewrite Section 2 (--domain, DOMAIN.md references)
5. Rename and rewrite Section 4 (Domain configuration)
6. Rewrite Section 5 (agent factories with generic tools/params)
7. Rewrite Section 6 (search_data and write_output contracts)
8. Rewrite Section 7 (generic prompts and coach schema)
9. Rewrite Section 8 (generic AGENTS.md boundaries)
10. Rewrite Section 9 (deepagents-exemplar project name)
11. Rewrite Section 10 (generic smoke test)
12. Update PASS/FAIL criteria and footer
13. Run acceptance criteria validation commands from TASK-REV-D3CD

**Estimated complexity**: 5/10 (documentation only, all source material exists in completed TASK-GER specs)

### R2: Dependency note

TASK-GER-004 (agent factories) is in review and TASK-GER-006 (entrypoint) is still in backlog. The checklist update can proceed using the task specifications as the source of truth, but the final smoke test (Section 10) should be verified after GER-006 completes.

---

## Decision Matrix

| Option | Effort | Risk | Accuracy | Recommendation |
|--------|--------|------|----------|----------------|
| Full rewrite (R1) | Medium (1 task, 13 subtasks) | Low | High — uses TASK-GER specs directly | **Recommended** |
| Incremental edits | Medium-High (42 edits) | Medium — easy to miss items | Medium | Not recommended |
| Defer until GER-006/007 complete | Low | High — blocks /template-create gate | N/A | Not recommended |

---

## Appendix

### Domain-specific terms to remove (acceptance criteria)

```
study-tutor-factory, gcse-english, SUBJECT.md, subjects/, AQA, AO1-AO6,
Socratic, rag_retrieval, jsonl_writer, ChromaDB, chromadb, train.jsonl,
rag_index/, layer (in routing context), socratic_quality, ao_correct,
layer_correct
```

### Generic terms to add

```
search_data, write_output, domains/, DOMAIN.md, example-domain, criteria_met,
quality_assessment, TAVILY_API_KEY, deepagents-exemplar, TASK-REV-8464
```

### Source material for rewrite

| Section | Source TASK-GER |
|---------|----------------|
| Structure, deps, env | TASK-GER-001 (completed) |
| Tools | TASK-GER-002 (completed) |
| Prompts | TASK-GER-003 (completed) |
| Agent factories | TASK-GER-004 (in review — spec is final) |
| Config (AGENTS.md, coach-config, DOMAIN.md) | TASK-GER-005 (completed) |
| Entrypoint, smoke test | TASK-GER-006 (backlog — spec is final) |

---

*Report generated for TASK-REV-D3CD | March 2026*
