# TASK-REV: DeepAgents Exemplar Repo Validation
## Before running /template-create for deepagents-exemplar

**Task Type:** review
**Complexity:** medium
**Domain tags:** `deepagents, langchain, template, python, agentic-loop`
**Prerequisite for:** `/template-create` → `deepagents-agentic-loop` GuardKit template
**Date:** March 2026

---

## Context

Before running `/template-create` on the DeepAgents exemplar repo,
this review verifies the exemplar is structurally sound, runs correctly, and
represents genuine best-practice patterns — not noise that would corrupt the
template.

The GuardKit template philosophy is explicit: templates are created FROM proven
working code. If the exemplar has broken imports, missing dependencies, or
anti-patterns, `/template-create` will encode those flaws permanently.

The exemplar implements a generic two-agent Player-Coach orchestration pattern
based on the Block Adversarial Cooperation paper. Following the TASK-REV-8464
architectural decision, all domain-specific content (original project name,
curriculum references, assessment frameworks) has been removed. The exemplar is now a
domain-agnostic template that users configure via `domains/{domain}/DOMAIN.md`.

The exemplar is assembled from two LangChain official examples:
- `langchain-ai/deepagents/examples/deep_research` — structural backbone,
  multi-agent coordination, LangSmith integration
- `langchain-ai/deepagents/examples/content-builder-agent` — config-driven
  pattern (`AGENTS.md`, `subagents.yaml`, `skills/` directory)

These are merged into a single exemplar repo demonstrating the generic
Player-Coach data generation pattern, revised by TASK-GER-001 through
TASK-GER-007.

---

## Target Exemplar Structure

The reviewer should verify this exact structure exists and is correct:

```
deepagents-exemplar/
├── pyproject.toml                  # uv-managed, pins deepagents + dependencies
├── .env.example                    # documents required env vars, no secrets
├── AGENTS.md                       # agent roles, behaviour boundaries
├── coach-config.yaml               # configurable coach: local or API
├── langgraph.json                  # LangGraph deployment config
├── README.md                       # setup + usage instructions
│
├── domains/                        # domain-agnostic config (one dir per domain)
│   └── example-domain/
│       └── DOMAIN.md               # domain description, generation guidelines, evaluation criteria
│
├── agents/
│   ├── __init__.py
│   ├── player.py                   # data generation agent
│   └── coach.py                    # validation agent
│
├── tools/
│   ├── __init__.py
│   ├── search_data.py              # Tavily search tool
│   └── write_output.py             # JSON validation + output writer
│
├── prompts/
│   ├── __init__.py
│   ├── player_prompts.py           # Player system prompt + generation instructions
│   └── coach_prompts.py            # Coach rubric + rejection schema
│
└── agent.py                        # main entrypoint — wires everything together
```

---

## Review Checklist

Work through each section in order. Mark each item PASS or FAIL with notes.

---

### Section 1: Environment and Dependencies

- [ ] `pyproject.toml` exists and is valid TOML
- [ ] `deepagents` is listed as a dependency with a pinned or minimum version
- [ ] `langchain`, `langgraph`, `langchain-community` are present
- [ ] `tavily-python` (or `tavily-py`) is present (for search_data tool)
- [ ] `langsmith` is present (for tracing)
- [ ] `python-dotenv` or equivalent is present
- [ ] `uv sync` completes without errors from a clean environment
- [ ] `uv run python -c "from deepagents import create_deep_agent; print('OK')"` passes
- [ ] `uv run python -c "from tools.search_data import search_data; print('OK')"` passes
- [ ] `.env.example` documents: `LANGSMITH_API_KEY`, `LANGSMITH_TRACING`,
  `LANGSMITH_PROJECT`, `LOCAL_MODEL_ENDPOINT`, `ANTHROPIC_API_KEY` (optional),
  `TAVILY_API_KEY`
- [ ] `LANGSMITH_PROJECT` is set to `deepagents-exemplar` in `.env.example`
- [ ] No API keys or secrets present in any tracked file

---

### Section 2: Agent entrypoint (`agent.py`)

- [ ] File imports `create_player` from `agents.player`
- [ ] File imports `create_coach` from `agents.coach`
- [ ] File imports `init_chat_model` from `langchain.chat_models`
- [ ] Model is loaded from config, not hardcoded — reads `coach-config.yaml`
  and selects local endpoint or API based on `provider` field
- [ ] When `provider: local` — initialises model using `LOCAL_MODEL_ENDPOINT` env var
- [ ] When `provider: api` — initialises model using `init_chat_model()` with model
  string from `coach.api.model` config field
- [ ] Reads domain config from `domains/{domain}/DOMAIN.md`
- [ ] Supports `--domain` CLI argument (defaults to `example-domain`)
- [ ] Creates Player and Coach agents using factory functions
- [ ] Defines module-level `agent` variable (required for `langgraph.json`)
- [ ] `uv run python agent.py --help` runs without error (or equivalent smoke test)
- [ ] No model strings hardcoded (no `gpt-4o`, `claude-opus`, `gemini`, `openai:`)

**Anti-patterns to reject:**
- [ ] Model hardcoded as `"openai:gpt-4o"` or any specific provider string
- [ ] API keys read directly from hardcoded strings
- [ ] Both agents sharing the same system prompt

---

### Section 3: Coach configuration (`coach-config.yaml`)

- [ ] File parses as valid YAML
- [ ] Contains `provider` field: value is `local` or `anthropic`
- [ ] Contains `local` section with `model` and `endpoint` fields
- [ ] Contains `api` section with `model` field
- [ ] `agent.py` reads this file and selects the correct provider at startup
- [ ] Switching `provider: local` → `provider: anthropic` changes model without
  code changes (config only)

**Expected structure:**
```yaml
coach:
  provider: local
  local:
    model: nemotron-3-super-120b-a12b
    endpoint: http://localhost:8000/v1
  api:
    model: claude-opus-4-6
```

---

### Section 4: Domain configuration (`domains/example-domain/DOMAIN.md`)

- [ ] File exists and is valid Markdown
- [ ] Contains `Domain Description` section — brief description of the example domain
- [ ] Contains `Generation Guidelines` section — what Player should generate
- [ ] Contains `Evaluation Criteria` section — what Coach should evaluate against
- [ ] Contains `Output Format` section — expected structure of generated content
- [ ] Content is clearly a GENERIC EXAMPLE that users replace with their own domain
- [ ] Includes inline comments/notes indicating "replace this with your domain"
- [ ] A second domain directory (`domains/another-domain/`) does NOT need to
  exist — verify the pattern is documented but not required

---

### Section 5: Agent definitions (`agents/player.py`, `agents/coach.py`)

**player.py:**
- [ ] Imports `create_deep_agent` from `deepagents`
- [ ] Imports `FilesystemBackend` from `deepagents.backends`
- [ ] Imports `search_data` and `write_output` from `tools`
- [ ] Imports `PLAYER_SYSTEM_PROMPT` from `prompts.player_prompts`
- [ ] Defines `create_player(model, domain_prompt: str)` factory function
- [ ] Returns `create_deep_agent(model=model, tools=[search_data, write_output],
  system_prompt=..., memory=["./AGENTS.md"], backend=FilesystemBackend(root_dir="."))`
- [ ] System prompt combines `PLAYER_SYSTEM_PROMPT` + `domain_prompt` (concatenated)
- [ ] Uses `FilesystemBackend(root_dir=".")` for real file writes
- [ ] Function is callable without side effects (no top-level agent instantiation)

**coach.py:**
- [ ] Imports `create_deep_agent` from `deepagents`
- [ ] Imports `COACH_SYSTEM_PROMPT` from `prompts.coach_prompts`
- [ ] Defines `create_coach(model, domain_prompt: str)` factory function
- [ ] Returns `create_deep_agent(model=model, tools=[], system_prompt=...,
  memory=["./AGENTS.md"])` — NO custom tools
- [ ] Coach tools list is explicitly empty (`tools=[]`)
- [ ] Does NOT specify `backend=` — uses default StateBackend (ephemeral)
- [ ] Does NOT import or use `FilesystemBackend`
- [ ] Passes `memory=["./AGENTS.md"]`
- [ ] Function is callable without side effects

**Anti-patterns to reject:**
- [ ] Agent instantiated at module level (breaks testability)
- [ ] System prompts written as inline multi-line strings in agent files
- [ ] Coach given write access to output files
- [ ] Coach given any custom tools

---

### Section 6: Tools (`tools/`)

**search_data.py:**
- [ ] Decorated with `@tool` from `langchain_core.tools`
- [ ] Signature: `(query: str, source: str) -> str`
- [ ] Returns concatenated search result strings on success
- [ ] Tavily client is initialised lazily (not at import time)
- [ ] Falls back gracefully when `TAVILY_API_KEY` not set — returns informative
  error string, does not raise
- [ ] Returns `"no results found for: {query}"` when results empty
- [ ] Returns `"error: {reason}"` on failure — never raises
- [ ] Tool docstring is clear — DeepAgents uses docstrings for tool selection

**write_output.py:**
- [ ] Decorated with `@tool` from `langchain_core.tools`
- [ ] Signature: `(content: str, output_path: str) -> str`
- [ ] Validates `content` is valid JSON — returns error string if not
- [ ] Validates `output_path` starts with `output/` — returns error string if not
  (path traversal guard)
- [ ] Creates parent directories if needed
- [ ] Appends content as a line to the output file (JSONL pattern)
- [ ] Returns `"written to {output_path}"` on success
- [ ] Does NOT raise exceptions — returns error as string (agents handle errors
  via return value, not exceptions)

---

### Section 7: Prompts (`prompts/`)

**player_prompts.py:**
- [ ] Defines `PLAYER_SYSTEM_PROMPT` as a module-level string constant
- [ ] Prompt instructs the Player to call `search_data` BEFORE generating content
- [ ] Prompt specifies output must be valid JSON with a `content` field
- [ ] Prompt instructs the Player to call `write_output` only AFTER Coach accepts
- [ ] Prompt instructs the Player to revise using Coach critique JSON, not
  re-generate from scratch
- [ ] Does NOT include domain-specific content (that comes from DOMAIN.md at runtime)
- [ ] `PLAYER_SYSTEM_PROMPT` > 400 chars

**coach_prompts.py:**
- [ ] Defines `COACH_SYSTEM_PROMPT` as a module-level string constant
- [ ] Prompt instructs Coach to return ONLY valid JSON — no prose, no preamble
- [ ] Prompt defines the generic evaluation schema:
  ```json
  {
    "decision": "accept | reject",
    "score": 1-5,
    "issues": ["list of specific problems"],
    "criteria_met": true | false,
    "quality_assessment": "high | adequate | needs_revision"
  }
  ```
- [ ] Prompt defines score rubric: 5=excellent, 4=good, 3=borderline (flag),
  2=significant issues, 1=reject
- [ ] Prompt instructs Coach to evaluate against domain criteria provided in
  system prompt (from DOMAIN.md)
- [ ] Prompt instructs Coach it does NOT have write tools — only Player writes
- [ ] `COACH_SYSTEM_PROMPT` > 400 chars

---

### Section 8: AGENTS.md

- [ ] File exists and describes the two agent roles clearly
- [ ] Defines Player's responsibilities and boundaries
- [ ] Defines Coach's responsibilities and boundaries
- [ ] Includes ALWAYS/NEVER/ASK sections per GuardKit boundary pattern:

  ```
  ## Player Agent
  ALWAYS: call search_data before generating content, produce valid JSON output,
         include source references
  NEVER: write output without Coach approval, generate more than one item per
         turn, skip search step
  ASK: (none currently defined)

  ## Coach Agent
  ALWAYS: return structured JSON evaluation, evaluate against domain criteria
         from DOMAIN.md, check content quality
  NEVER: write to output files, modify content directly, return prose instead
         of JSON
  ASK: when score is 3 (borderline) — escalate for human review
  ```

- [ ] AGENTS.md is referenced in agent factories via `memory=["./AGENTS.md"]`
- [ ] No domain-specific terms in AGENTS.md

---

### Section 9: LangSmith integration

- [ ] `LANGSMITH_TRACING=true` is documented in `.env.example`
- [ ] `LANGSMITH_PROJECT` is set to `"deepagents-exemplar"` in `.env.example`
- [ ] No explicit LangSmith callback setup needed — DeepAgents traces
  automatically when env vars are set
- [ ] Verify: `uv run python -c "import langsmith; print(langsmith.__version__)"` passes

---

### Section 10: Smoke test

Run the full agent loop with a minimal test input before declaring the
exemplar ready:

```bash
# Requires: LANGSMITH_API_KEY set, LangSmith tracing active
# Requires: either local vLLM endpoint OR ANTHROPIC_API_KEY for coach
# Tavily does not need to be populated — search_data returns graceful fallback

uv run python agent.py \
  --domain example-domain \
  --mode smoke \
  --max-examples 2 \
  --max-coach-turns 2
```

Expected outcome:
- [ ] Player generates 2 draft examples without error
- [ ] Coach validates each and returns structured JSON decision
- [ ] At least 1 accepted example is written to `output/` directory
- [ ] LangSmith trace appears at smith.langchain.com
- [ ] No unhandled exceptions in the trace

If no `--mode smoke` flag exists yet, a minimal `python -c` import test is
the minimum acceptable:

```bash
uv run python -c "
from agents.player import create_player
from agents.coach import create_coach
from tools.search_data import search_data
from tools.write_output import write_output
from prompts.player_prompts import PLAYER_SYSTEM_PROMPT
from prompts.coach_prompts import COACH_SYSTEM_PROMPT
print('All imports OK')
"
```

- [ ] All imports resolve without error

---

## Review Decision

### PASS criteria (all must be true)
- All Section 1 dependency checks pass
- Sections 2-8 have zero FAIL on anti-pattern items
- Section 10 smoke test passes (at minimum: all imports OK)
- No API keys in tracked files
- No domain-specific terms in prompts or tool docstrings

### CONDITIONAL PASS criteria
If any non-critical items fail (e.g. AGENTS.md missing ALWAYS/NEVER sections,
coach prompt is prose not structured JSON), document the gaps and fix before
running `/template-create`. These gaps will be encoded into the template if
not fixed.

### FAIL criteria (any one blocks /template-create)
- `uv sync` fails
- Any import in Section 10 fails
- Coach and Player use identical system prompts
- Model is hardcoded (not configurable via `coach-config.yaml`)
- Any API key present in tracked files
- Domain-specific terms remain in prompts, tools, or agent docstrings

---

## What to do with failures

For each FAIL: fix it in the exemplar repo first. Do not run
`/template-create` on a broken exemplar. The template is only as good as
what you feed it.

Common fixes:
- Missing `@tool` decorator -> add it, ensure docstring is clear
- Agent instantiated at module level -> wrap in `create_*()` function
- Inline system prompt -> move to `prompts/` module
- Hardcoded model -> read from `coach-config.yaml`
- Exception raised in tool -> return error string instead
- Domain-specific terms -> replace with generic equivalents

---

## After this review passes

```bash
# From the exemplar repo root
cd deepagents-exemplar

# Run template-create (GuardKit command in Claude Code)
/template-create

# This produces a local GuardKit template at:
# ~/.guardkit/templates/local/deepagents-agentic-loop/

# Verify the template was created
guardkit template list --local

# Initialise a new project from it
cd ../my-project
guardkit init deepagents-agentic-loop
```

---

*TASK-REV prepared March 2026 | Generic Player-Coach exemplar pre-work | Revised per TASK-REV-8464 architectural decision*
