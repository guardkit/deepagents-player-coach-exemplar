# Review Report: TASK-REV-8464

## Executive Summary

The current FEAT-deepagents-exemplar-build spec and its 6 implementation tasks are **heavily coupled to the study-tutor-factory domain**. If `/template-create` extracts a template from this exemplar as-is, the resulting `deepagents-agentic-loop` template will force every new project to strip out GCSE marking frameworks, fine-tuning dataset formats, ChromaDB curriculum retrieval, and Socratic quality metrics before they can begin.

**Recommendation: REVISE tasks 2, 3, and 5 to be domain-generic. Apply minor fixes to task 1 (already implemented). Tasks 4 and 6 need only naming/reference updates that follow automatically.**

The architecture — two-agent orchestration, factory functions, config-driven domains, structured evaluation loops — is sound and should be preserved. Only the domain-specific *content* needs replacing with generic equivalents.

---

## Review Details

- **Mode**: Architectural Review
- **Depth**: Standard
- **Task**: TASK-REV-8464 — "Review exemplar genericity: specific tutor-factory vs generic DeepAgents template"
- **Complexity**: 7/10

---

## Architecture Assessment: 68/100

| Criterion | Score | Notes |
|-----------|:-----:|-------|
| SOLID — Single Responsibility | 8/10 | Each file/module has clear purpose |
| SOLID — Open/Closed | 4/10 | Domain logic hardcoded, not extensible |
| SOLID — Liskov Substitution | 7/10 | Factory pattern allows substitution |
| SOLID — Interface Segregation | 7/10 | Clean tool interfaces |
| SOLID — Dependency Inversion | 4/10 | Tools depend on ChromaDB concretions |
| DRY | 8/10 | No duplication across tasks |
| YAGNI | 5/10 | Over-specified for template purposes |
| **Template Genericity** | **3/10** | **Critical: 4 of 6 tasks contain domain-specific content** |

---

## Findings

### Finding 1: CRITICAL — Tools are 100% domain-specific
**Tasks affected**: TASK-DEB-002
**Evidence**: `rag_retrieval` is tied to ChromaDB curriculum chunks. `jsonl_writer` implements `behaviour`/`knowledge` layer routing for fine-tuning datasets. Neither tool pattern is reusable — a template user building a code review agent or data pipeline has no use for them.
**Impact**: Template consumers must delete and rewrite both tools from scratch.

### Finding 2: CRITICAL — Prompts saturated with tutor-factory logic
**Tasks affected**: TASK-DEB-003
**Evidence**: Player prompt specifies ShareGPT JSONL format, 75% `<think>` block requirement, layer field routing. Coach prompt defines `ao_correct`, `socratic_quality`, `layer_correct` schema fields, AO1-AO6 evaluation criteria. Every acceptance criterion references domain concepts.
**Impact**: Template consumers must rewrite both prompts entirely. No reusable structure remains.

### Finding 3: HIGH — AGENTS.md boundaries reference domain tools and concepts
**Tasks affected**: TASK-DEB-005
**Evidence**: Player ALWAYS rules reference `rag_retrieval`, `layer` field, `think` blocks. Coach rules reference `layer routing`. `subjects/gcse-english/SUBJECT.md` contains AQA exam board, specification numbers, AO1-AO6 framework.
**Impact**: AGENTS.md must be rewritten. SUBJECT.md must be replaced with generic domain config.

### Finding 4: LOW — Scaffold has minor domain artifacts
**Tasks affected**: TASK-DEB-001 (implemented)
**Evidence**: `chromadb>=0.5` dependency, `subjects/gcse-english/` directory, `LANGSMITH_PROJECT=study-tutor-factory`, `train.jsonl`/`rag_index/` in .gitignore.
**Impact**: Surgical fixes only — no rebuild needed.

### Finding 5: LOW — Factory and entrypoint patterns are generic
**Tasks affected**: TASK-DEB-004, TASK-DEB-006
**Evidence**: Factory pattern (`create_deep_agent()` with `memory=`, `backend=`, `tools=`) and entrypoint pattern (config loading, model init, CLI args) are exactly the SDK idiom. Domain leak is only through tool imports and naming, which follows from tasks 2-3.
**Impact**: If tools and prompts become generic, these tasks need only reference updates.

### Finding 6: OBSERVATION — Coach rejection schema design is sound but domain-coupled
**Tasks affected**: TASK-DEB-003, TASK-DEB-005
**Evidence**: The pattern of structured JSON evaluation (`decision`, `score`, `issues`) is a valuable generic template pattern. But `ao_correct`, `socratic_quality`, `layer_correct` are study-tutor-factory fields.
**Impact**: Replace domain fields with generic quality assessment fields; preserve the structured evaluation pattern.

### Finding 7: OBSERVATION — coach-config.yaml is already mostly generic
**Tasks affected**: TASK-DEB-005
**Evidence**: The local/API provider switching pattern (`coach.provider`, `coach.local.model`, `coach.api.model`) is a useful generic pattern for any two-agent system where agents may use different model providers.
**Impact**: Rename from "coach" to "reviewer" or keep as-is with generic role documentation. Low effort.

### Finding 8: OBSERVATION — The `domains/` pattern is correct but needs renaming
**Tasks affected**: TASK-DEB-005, TASK-DEB-006
**Evidence**: The `subjects/` directory follows the content-builder-agent `skills/` pattern — per-domain config directories loaded at runtime. This IS a good generic pattern.
**Impact**: Rename `subjects/` → `domains/`, `SUBJECT.md` → `DOMAIN.md`, provide generic example content.

---

## Recommendations

### Recommendation 1: Rewrite TASK-DEB-002 with generic tools
**Priority**: Critical
**Effort**: Medium (tool patterns stay the same, only domain logic changes)

Replace:
- `rag_retrieval(query, subject)` → `search_data(query: str, source: str) -> str`
  - Web search via configurable provider (Tavily/DuckDuckGo)
  - Demonstrates: `@tool` decorator, docstring routing, lazy client init, graceful error handling
  - Returns search results as string, never raises
- `jsonl_writer(example, layer)` → `write_output(content: str, output_path: str) -> str`
  - Validates content is valid JSON, writes to specified path
  - Demonstrates: input validation, file I/O, directory creation, error strings
  - No layer routing — just generic validated file writing

**Update dependencies**: Replace `chromadb>=0.5` with search provider dependency (or make optional).

### Recommendation 2: Rewrite TASK-DEB-003 with generic prompts
**Priority**: Critical
**Effort**: Medium-High (prompts need careful redesign)

**Player prompt** should instruct:
- Call `search_data` before generating content
- Generate structured output (JSON format, but not ShareGPT-specific)
- Only call `write_output` after Reviewer approval
- Revise using Reviewer critique, don't regenerate from scratch

**Coach/Reviewer prompt** should instruct:
- Return ONLY valid JSON (no prose)
- Generic evaluation schema:
  ```json
  {"decision": "accept|reject", "score": 1-5, "issues": [...],
   "criteria_met": true, "quality_assessment": "high|adequate|needs_revision"}
  ```
- Score rubric: 5=excellent, 4=good, 3=borderline, 2=significant issues, 1=reject
- NO domain-specific criteria (no AOs, no Socratic quality, no layers)

### Recommendation 3: Rewrite TASK-DEB-005 with generic config
**Priority**: High
**Effort**: Low-Medium

- **AGENTS.md**: Generic two-agent boundaries. Generator ALWAYS retrieves context, NEVER writes without approval. Reviewer ALWAYS returns structured JSON, NEVER writes to output, ASK when borderline.
- **coach-config.yaml** → **reviewer-config.yaml**: Same local/API structure, generic naming.
- **subjects/gcse-english/SUBJECT.md** → **domains/example-domain/DOMAIN.md**: Generic sections (Domain Description, Generation Guidelines, Evaluation Criteria). No AOs, no exam boards.

### Recommendation 4: Apply minor fixes to TASK-DEB-001 (implemented)
**Priority**: Medium
**Effort**: Low (<30 min)

1. Remove `chromadb>=0.5` from `pyproject.toml` (add search provider dep if needed)
2. Rename `subjects/gcse-english/` → `domains/example-domain/`
3. Update `.gitignore` output paths (remove `train.jsonl`, `rag_index/`)
4. Update `.env.example` project name
5. Update `README.md` description
6. Update `pyproject.toml` name/description

### Recommendation 5: Update TASK-DEB-004 and TASK-DEB-006 references
**Priority**: Low (follows automatically from Recs 1-3)
**Effort**: Low

- TASK-DEB-004: Update tool imports (`search_data`, `write_output`), rename factories if desired (`create_generator`/`create_reviewer` vs `create_player`/`create_coach`)
- TASK-DEB-006: Update `--subject` → `--domain`, default `gcse-english` → `example-domain`, rename config file references

---

## Decision Matrix

| Option | Template Genericity | Effort | Risk | Recommendation |
|--------|:---:|:---:|:---:|:---:|
| **A: Accept as-is** — Let template-create abstract | 3/10 | None | High — template inherits domain logic | Not recommended |
| **R: Revise tasks 2, 3, 5** — Rewrite domain-specific tasks | 9/10 | Medium (2-3 days) | Low — patterns preserved, only content changes | **Recommended** |
| **I: Revise + apply fixes to task 1** | 10/10 | Medium (2-3 days + 30 min) | Low | Best option |
| **C: Cancel** | N/A | N/A | N/A | Not warranted |

---

## Impact on Already-Implemented Work

### TASK-DEB-001 (in_review)
- **Rebuild needed?** No
- **Changes**: Surgical — dependency swap, directory rename, text updates
- **Estimated effort**: 30 minutes
- **Risk**: None — structural scaffold is correct

### FEAT Spec
- Decision log D5 (rejection schema), D6 (tools), D9 (subjects) need updates
- Architecture section 3.1 component table needs updating
- API contracts section 4 needs rewriting for generic tools
- Tasks section 5 needs rewriting for tasks 2, 3, 5

---

## Appendix: Proposed Generic File Tree

```
deepagents-exemplar/
├── pyproject.toml                    # No chromadb dep
├── .env.example                      # Generic project name
├── .gitignore
├── README.md                         # "DeepAgents Exemplar — Two-Agent Orchestration"
├── AGENTS.md                         # Generic generator/reviewer boundaries
├── reviewer-config.yaml              # Local/API model selection
├── langgraph.json
├── agent.py                          # --domain flag, generic wiring
├── agents/
│   ├── __init__.py
│   ├── generator.py                  # create_generator() factory
│   └── reviewer.py                   # create_reviewer() factory
├── tools/
│   ├── __init__.py
│   ├── search_data.py                # Web search, @tool pattern
│   └── write_output.py              # Validated file writer, @tool pattern
├── prompts/
│   ├── __init__.py
│   ├── generator_prompts.py          # Generic generation instructions
│   └── reviewer_prompts.py           # Generic structured evaluation
└── domains/
    └── example-domain/
        └── DOMAIN.md                 # Generic: description, guidelines, criteria
```

---

*Review completed: 2026-03-16 | Reviewer: architectural-reviewer | Mode: architectural | Depth: standard*
