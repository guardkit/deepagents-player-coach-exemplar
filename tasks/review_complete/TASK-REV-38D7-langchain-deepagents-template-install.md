---
id: TASK-REV-38D7
title: "Review: add langchain-deepagents to GuardKit built-in templates"
status: review_complete
created: 2026-03-16T00:00:00Z
updated: 2026-03-16T00:00:00Z
priority: high
complexity: 6
type: review
task_type: review
decision_required: true
feature_id: FEAT-DEB
tags: [guardkit, template, installer, langchain-deepagents, documentation]
dependencies: []
---

# Task: Review — add langchain-deepagents to GuardKit built-in templates

## Description

The `langchain-deepagents` template has been generated via `/template-create` and
exists at `~/.agentecflow/templates/langchain-deepagents/`. It needs to be
promoted from a user-local template to a **built-in GuardKit template** so that
any user can run `guardkit init langchain-deepagents` without manual setup.

This review task analyses what changes are needed to the GuardKit installer,
template registry, documentation, and CI to make this happen — then produces
implementation tasks for the actual work.

## Template Summary (from /template-create output)

- **Location**: `~/.agentecflow/templates/langchain-deepagents/`
- **Generated files**: `manifest.json`, `settings.json`, 14 template files
- **Specialist agents (7)**:
  - adversarial-cooperation-architect
  - deepagents-factory-specialist
  - domain-driven-config-specialist
  - langgraph-entrypoint-specialist
  - system-prompt-engineer
  - langchain-tool-specialist
  - pytest-factory-test-specialist
- **Rules**: `.claude/rules/` with code-style, testing, patterns, and per-agent guidance
- **Enhancement tasks**: 7 created in backlog (from `/template-create`)

## Known Issue

Minor display error in `/template-create` output: looked for `CLAUDE.md` at repo
root instead of `.claude/CLAUDE.md`. All files were written correctly — this is a
cosmetic bug in the template-create command, not in the template itself.

## Review Scope

### 1. Installer / Registry Integration
- Where does GuardKit register built-in templates? (installer manifest, directory listing, or registry file?)
- What changes are needed to `guardkit init` to recognise `langchain-deepagents`?
- Does the template need to be copied from `~/.agentecflow/templates/` to the GuardKit installer directory?
- Are there naming conventions for built-in templates? (e.g., must match `installer/core/templates/{name}/`)

### 2. Template Completeness
- Does `manifest.json` have all required fields for a built-in template?
- Does `settings.json` correctly configure the `project.template` field?
- Are all 14 template files present and non-empty?
- Do the 7 specialist agents have correct discovery metadata (stack, phase, capabilities, keywords)?
- Is the rules structure complete (code-style, testing, patterns)?

### 3. Documentation Updates
- CLAUDE.md: Does the template selection guidance need updating? (currently lists react-typescript, fastapi-python, nextjs-fullstack, react-fastapi-monorepo)
- README or installation docs: Do they reference available templates?
- Template migration guide: Does it need a langchain-deepagents entry?

### 4. CLAUDE.md Display Bug
- Investigate the `CLAUDE.md` root vs `.claude/CLAUDE.md` lookup issue
- Determine if this is a template-create bug or a template-level issue
- Create fix task if needed

### 5. CI / Validation
- Are there template validation tests that need updating?
- Does the installer have a template listing test?
- Do agent metadata tests cover the new specialist agents?

## Acceptance Criteria

- [ ] Review report documents the exact files/locations that need modification in GuardKit installer
- [ ] Review report confirms template completeness (all 14 files, 7 agents, manifest, settings)
- [ ] Review report identifies documentation that references the template list
- [ ] Review report assesses the CLAUDE.md display bug severity and fix path
- [ ] Review produces implementation tasks for each area of change
- [ ] Each implementation task is scoped to complexity <= 5

## Review Decision Options

At the checkpoint, the reviewer should choose:
- **[A]ccept** — Template is complete, create implementation tasks for installer integration
- **[I]mplement** — Create implementation tasks directly from review findings
- **[R]evise** — Template needs fixes before it can be promoted to built-in
- **[C]ancel** — Template should remain user-local, not promoted

## Suggested Workflow

```bash
# 1. Run this review
/task-review TASK-REV-38D7

# 2. Review findings and decide at checkpoint

# 3. If [I]mplement — work the generated tasks:
/task-work TASK-IMP-XXXX   # Installer integration
/task-work TASK-IMP-YYYY   # Documentation updates
/task-work TASK-IMP-ZZZZ   # CLAUDE.md bug fix (if needed)
```

## Implementation Notes

- The template was generated from the deepagents-tutor-exemplar after all TASK-GER
  tasks completed and the validation checklist (TASK-IMP-D3CD) passed.
- The exemplar is fully generic (no domain-specific content) per TASK-REV-8464.
- The 7 enhancement tasks from `/template-create` are separate from this review —
  they enhance agent quality, not installer integration.
