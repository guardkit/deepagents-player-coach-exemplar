# Feature Specification: DeepAgents Exemplar Repo

**Date:** March 2026
**Author:** Rich
**Status:** Revised after architectural review (2026-03-16) — Ready for Implementation
**Research Method:** Claude Desktop → `/task-review`
**Target Repo:** `appmilla/deepagents-tutor-exemplar` (new repo)
**Target Branch:** `main`
**Feature ID:** FEAT-XXX *(assigned by `/feature-plan`)*

---

## 1. Problem Statement

Before running GuardKit's `/template-create` to produce a reusable
`deepagents-agentic-loop` template, a working exemplar repo must exist.
GuardKit's template philosophy is explicit: templates are created FROM proven
working code, not authored by hand. This feature builds that exemplar by
combining patterns from two official LangChain DeepAgents examples
(`deep_research` and `content-builder-agent`) into a single repo that
demonstrates a generic two-agent Player-Coach orchestration pattern
inspired by the Adversarial Cooperation paper.

The exemplar must run end-to-end, pass the TASK-REV validation checklist,
and represent genuine best practices — not noise that would corrupt the
template permanently.

---

## 2. Decision Log

| # | Decision | Rationale | Alternatives Rejected | ADR Status |
|---|----------|-----------|----------------------|------------|
| D1 | Use `deep_research` as structural backbone | Has multi-agent coordination, `prompts.py` separation, LangSmith integration, and LangGraph deployment config already working | Authoring from scratch (slower, no proven baseline) | Accepted |
| D2 | Borrow config-driven pattern from `content-builder-agent` | `AGENTS.md` + `subagents.yaml` + `skills/` externalisation maps directly to subject-agnostic design — adding a subject is a config change not a code change | Hardcoding subject logic in Python (breaks generality) | Accepted |
| D3 | `coach-config.yaml` for configurable Coach model | Enables local (Nemotron 3 Super) for overnight volume runs and Claude Opus API for spot-check validation with zero code changes | Env var switching (less explicit), hardcoded model (breaks the pattern) | Accepted |
| D4 | Player and Coach as separate `create_deep_agent()` instances | Each gets different system prompt, tools, and responsibilities. Coach has NO custom tools (`tools=[]`) and uses default `StateBackend` so built-in filesystem middleware operates on ephemeral state only — Coach cannot write real files. Player uses `FilesystemBackend` for real output writes | Single agent doing both roles (conflates generation and validation) | Accepted |
| D5 | Coach returns structured JSON evaluation schema, not prose | Makes evaluation reasons parseable for metrics. Schema: `{decision, score, issues, criteria_met, quality_assessment}` — domain-specific criteria are loaded from `DOMAIN.md` at runtime | Free-text critique (not machine-parseable, can't gate on confidence) | Accepted |
| D6 | `@tool` decorated functions (`search_data`, `write_output`) with docstrings for tool selection | DeepAgents uses docstrings for tool routing — clear docstrings are load-bearing, not documentation. Tool names are generic: `search_data` retrieves domain-relevant context, `write_output` writes accepted results | Class-based tools (unnecessary complexity for this use case) | Accepted |
| D7 | Tools return strings, never raise exceptions | Agents handle errors via return value. Exceptions crash the agent loop | Raising exceptions (breaks DeepAgents tool calling loop) | Accepted |
| D8 | `uv` for dependency management | Consistent with GB10 Python toolchain, fast, lockfile reproducibility | pip + requirements.txt (less reproducible), poetry (heavier) | Accepted |
| D9 | `domains/` directory inspired by `skills/` layout from content-builder | Domain = config directory with `DOMAIN.md` containing generation guidelines and evaluation criteria. Adding a new domain requires only a new directory. NOTE: this is custom config read by `agent.py`, NOT a DeepAgents skill — do not pass to `skills=[]` parameter or use `SkillsMiddleware` | Hardcoded domain logic (breaks generality, forces code changes per domain) | Accepted |

**Warnings & Constraints:**
- DeepAgents traces automatically when `LANGSMITH_TRACING=true` — no explicit callback setup needed
- This exemplar does NOT use the `subagents` or `load_subagents()` pattern — Player and Coach are independent `create_deep_agent()` instances orchestrated imperatively by `agent.py`
- Coach must NOT receive `write_output` tool — only Player writes output
- `AGENTS.md` must be loaded at runtime via `memory=["./AGENTS.md"]` parameter in `create_deep_agent()` — without this, MemoryMiddleware won't inject the boundaries into the system prompt and the file is just inert documentation
- Player and Coach are **peer agents** orchestrated by `agent.py` in a loop — they are NOT subagents of each other. Do not use `subagents=[]` or `load_subagents()` for this pattern

---

## 3. Architecture

### 3.1 Component Design

| Component | File Path | Purpose | Source |
|-----------|-----------|---------|--------|
| Entrypoint | `agent.py` | Wires everything, reads config, runs loop | deep_research pattern |
| Player agent | `agents/player.py` | `create_player()` factory function | new |
| Coach agent | `agents/coach.py` | `create_coach()` factory function | new |
| Search tool | `tools/search_data.py` | Retrieves domain-relevant context data | new |
| Write tool | `tools/write_output.py` | Writes accepted output to configured destination | new |
| Player prompts | `prompts/player_prompts.py` | `PLAYER_SYSTEM_PROMPT` constant | deep_research pattern |
| Coach prompts | `prompts/coach_prompts.py` | `COACH_SYSTEM_PROMPT` + evaluation schema | deep_research pattern |
| Agent roles | `AGENTS.md` | ALWAYS/NEVER/ASK boundaries per agent | content-builder pattern |
| Coach config | `coach-config.yaml` | local vs API model selection | new |
| Domain config | `domains/example-domain/DOMAIN.md` | Generation guidelines + evaluation criteria | inspired by content-builder skills/ layout (custom config, not SkillsMiddleware) |
| LangGraph config | `langgraph.json` | Deployment configuration | deep_research pattern |
| Dependencies | `pyproject.toml` | uv-managed package list | new |
| Env template | `.env.example` | Documents required env vars | new |

### 3.2 Data Flow

```
1. agent.py reads coach-config.yaml → selects local or API coach model
2. agent.py reads domains/{domain}/DOMAIN.md → loads generation guidelines and evaluation criteria
3. Player agent receives task: "generate N outputs for [domain topic]"
4. Player calls search_data(query, domain) → gets relevant domain context
5. Player generates draft output (with metadata)
6. Player passes draft to Coach agent
7. Coach evaluates against domain-specific criteria from DOMAIN.md
8. Coach returns structured JSON: {decision, score, issues, criteria_met, quality_assessment}
9a. If accepted: Player calls write_output(data) → writes to configured destination
9b. If rejected (turns < max): Player revises using Coach critique → back to step 6
9c. If max turns reached: output discarded, reason logged
10. LangSmith traces entire loop automatically
```

---

## 4. API Contracts

### Coach Evaluation Schema

Every Coach response must be valid JSON matching this schema:

```json
{
  "decision": "accept | reject",
  "score": 1,
  "issues": ["specific problem descriptions"],
  "criteria_met": true,
  "quality_assessment": "high | acceptable | needs_revision | inadequate"
}
```

Score rubric: 5=excellent, 4=good minor issues, 3=borderline (escalate),
2=significant problems, 1=fundamentally wrong.

The `criteria_met` field indicates whether the output satisfies domain-specific
criteria defined in `DOMAIN.md`. The `quality_assessment` field provides a
qualitative rating of the overall output quality.

### search_data Tool Contract

- Input: `query: str`, `domain: str` (e.g. "example-domain")
- Output: relevant context strings, or `"no results found"` if no data available
- Never raises exceptions — returns empty gracefully

### write_output Tool Contract

- Input: `data: str` (valid JSON string)
- Output: `"written to output/{domain}/output.jsonl"` | `"error: [reason]"`
- Never raises exceptions — always returns string

---

## 5. Implementation Tasks

> **Note:** The original TASK-DEB-002, TASK-DEB-003, and TASK-DEB-005 tasks have been
> superseded by TASK-GER-001 through TASK-GER-007 following the TASK-REV-8464 genericity
> review. The GER tasks implement the same architecture with generic tool names,
> domain-agnostic prompts, and configurable domain directories.

### Task Mapping (DEB → GER)

| Original | Replacement | Title |
|----------|------------|-------|
| TASK-DEB-001 | TASK-GER-001 | Scaffold fixes: remove domain artifacts |
| TASK-DEB-002 | TASK-GER-002 | Tools: `search_data` and `write_output` (generic) |
| TASK-DEB-003 | TASK-GER-003 | Prompts: generic Player and Coach system prompts |
| TASK-DEB-004 | *(Wave 2)* | Agent factories (unchanged architecture) |
| TASK-DEB-005 | TASK-GER-005 | Config: AGENTS.md, coach-config, domain configuration |
| TASK-DEB-006 | TASK-GER-006 | Main entrypoint `agent.py` (generic wiring) |
| *(new)* | TASK-GER-007 | Update FEAT spec for generic exemplar (this document) |

### Wave 1: Foundation (TASK-GER-001 → 002, 003, 005 in parallel)

- **TASK-GER-001** — Scaffold fixes: remove domain-specific artifacts from repo scaffold
- **TASK-GER-002** — Tools: `search_data` (domain context retrieval) and `write_output` (writes accepted output)
- **TASK-GER-003** — Prompts: generic Player and Coach system prompts (domain-agnostic, criteria loaded from `DOMAIN.md`)
- **TASK-GER-005** — Config: AGENTS.md boundaries, coach-config.yaml, `domains/example-domain/DOMAIN.md`

### Wave 2: Integration (sequential)

- **TASK-GER-006** — Main entrypoint `agent.py`: generic wiring with `--domain` CLI argument
- **TASK-GER-007** — Update FEAT spec and implementation guides to reflect generic architecture

### Key Changes from Original DEB Tasks

| Aspect | Original (DEB) | Generic (GER) |
|--------|----------------|---------------|
| Tools | `rag_retrieval`, `jsonl_writer` | `search_data`, `write_output` |
| Config dir | `subjects/gcse-english/SUBJECT.md` | `domains/example-domain/DOMAIN.md` |
| Coach schema | `ao_correct`, `socratic_quality`, `layer_correct` | `criteria_met`, `quality_assessment` |
| Output routing | `train.jsonl`, `rag_index/` (layer-based) | `output/{domain}/output.jsonl` |
| CLI argument | `--subject gcse-english` | `--domain example-domain` |
| Prompts | Tutor-specific (AO rubric, Socratic quality) | Domain-agnostic (criteria from DOMAIN.md) |

---

## 6. Test Strategy

### Smoke test (run after TASK-GER-006 completes)

```bash
# Minimum viable smoke test — no real model needed
uv run python -c "
from agents.player import create_player
from agents.coach import create_coach
from tools.search_data import search_data
from tools.write_output import write_output
from prompts.player_prompts import PLAYER_SYSTEM_PROMPT
from prompts.coach_prompts import COACH_SYSTEM_PROMPT
import yaml, pathlib
config = yaml.safe_load(pathlib.Path('coach-config.yaml').read_text())
domain = pathlib.Path('domains/example-domain/DOMAIN.md').read_text()
assert config['coach']['provider'] in ['local', 'anthropic']
assert len(domain) > 100
print('Full smoke test OK — ready for /template-create review')
"
```

### TASK-REV gate

After all GER tasks complete, pass `TASK-REV-deepagents-exemplar-validation.md`
to `/task-review` or work through it manually. The exemplar must pass all
PASS criteria before running `/template-create`.

---

## 7. Dependencies and Setup

### Python dependencies (in `pyproject.toml`)
```
deepagents>=0.4.11
langchain>=1.2.11
langchain-core>=1.2.18
langgraph>=0.2
langchain-community>=0.3
langsmith>=0.2
python-dotenv>=1.0
pyyaml>=6.0
```

### System dependencies
None — all Python, no Docker required for the exemplar itself.

### Environment variables (from `.env`)
```
LANGSMITH_API_KEY=<from smith.langchain.com>
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=deepagents-exemplar
LOCAL_MODEL_ENDPOINT=http://localhost:8000/v1
ANTHROPIC_API_KEY=<optional — only needed when coach.provider=anthropic>
```

---

## 8. File Tree (Target State)

```
deepagents-tutor-exemplar/
├── pyproject.toml
├── .env.example
├── .gitignore
├── README.md
├── AGENTS.md
├── coach-config.yaml
├── langgraph.json
├── agent.py
├── agents/
│   ├── __init__.py
│   ├── player.py
│   └── coach.py
├── tools/
│   ├── __init__.py
│   ├── search_data.py
│   └── write_output.py
├── prompts/
│   ├── __init__.py
│   ├── player_prompts.py
│   └── coach_prompts.py
└── domains/
    └── example-domain/
        └── DOMAIN.md
```

---

## 9. Out of Scope

- Real data source population (exemplar uses placeholder search implementation)
- Full end-to-end run with real models (exemplar proves structure; real runs
  are downstream project concern)
- LangGraph Studio UI setup
- Multi-domain implementation (only `example-domain` config needed for exemplar)
- Domain-specific processing pipelines (separate from the exemplar pattern)
- Error recovery / retry logic beyond max-turns (v1 scope)

---

## 10. Open Questions (Resolved)

| Question | Resolution |
|---|---|
| Should Player and Coach share a model instance? | No — each gets its own `init_chat_model()` call. Allows different models per role in future. |
| Does Coach need any tools at all? | No custom tools — `tools=[]`. Coach also uses default `StateBackend` (not `FilesystemBackend`) so built-in middleware filesystem tools operate on ephemeral state only. Write access to real files belongs to Player only (via `FilesystemBackend`). |
| How does domain config reach the agents at runtime? | `agent.py` reads `DOMAIN.md`, passes as `domain_prompt` to factory functions, which append to base system prompt. |
| Should exemplar include a full production loop? | No — wiring only. The loop logic belongs in downstream projects. Exemplar proves patterns are correct. |
| What Python version? | 3.11+ (compatible with all dependencies) |

---

---

## 11. Revision Log

| Date | Reviewer | Finding | Change |
|------|----------|---------|--------|
| 2026-03-16 | /task-review architectural | Coach gets built-in write tools via FilesystemMiddleware | D4 updated: Coach uses default StateBackend (ephemeral); Player uses FilesystemBackend. Task 4 acceptance criteria updated with backend and memory= requirements |
| 2026-03-16 | /task-review architectural | AGENTS.md not wired via memory= parameter | Added `memory=["./AGENTS.md"]` to both factory functions in Task 4. Added warning to Constraints section. Task 6 updated to delegate memory wiring to factories |
| 2026-03-16 | /task-review architectural | `load_subagents()` warning misleading | Replaced with clarification that Player/Coach are peer agents, not subagents |
| 2026-03-16 | /task-review architectural | subjects/ vs skills/ confusion | D9 clarified: custom config, not SkillsMiddleware. Component table updated |
| 2026-03-16 | /task-review architectural | Loose dependency versions | Pinned to deepagents>=0.4.11, langchain>=1.2.11, langchain-core>=1.2.18. Task 1 criteria updated |
| 2026-03-16 | TASK-REV-8464 genericity review | Exemplar was tutor-domain-specific; must be generic | Full revision: tools renamed (`search_data`, `write_output`), `subjects/` → `domains/`, Coach schema genericised (`criteria_met`, `quality_assessment`), prompts made domain-agnostic, output routing simplified, ChromaDB dependency removed, all domain-specific references (GCSE, AQA, AO1-AO6, Socratic, curriculum) removed from active sections. TASK-DEB-002/003/005 superseded by TASK-GER-001 through TASK-GER-007 |

---

*FEAT prepared March 2026 | Revised 2026-03-16 (TASK-REV-8464 genericity review) | Consumed by `/task-review` → GuardKit AutoBuild*
