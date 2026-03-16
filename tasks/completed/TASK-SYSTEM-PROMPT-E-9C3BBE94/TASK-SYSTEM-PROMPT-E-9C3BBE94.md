# TASK-SYSTEM-PROMPT-E-9C3BBE94: Enhance system-prompt-engineer agent for langchain-deepagents template

**Task ID**: TASK-SYSTEM-PROMPT-E-9C3BBE94
**Priority**: MEDIUM
**Status**: COMPLETED
**Created**: 2026-03-16T11:19:45.678767
**Completed**: 2026-03-16
**Completed Location**: tasks/completed/TASK-SYSTEM-PROMPT-E-9C3BBE94/

## Description

Enhance the system-prompt-engineer agent with template-specific content:
- Add related template references
- Include code examples from templates
- Document best practices
- Add anti-patterns to avoid (if applicable)

**Agent File**: /Users/richardwoollcott/.agentecflow/templates/langchain-deepagents/agents/system-prompt-engineer.md
**Template Directory**: /Users/richardwoollcott/.agentecflow/templates/langchain-deepagents

## Command

```bash
/agent-enhance langchain-deepagents/system-prompt-engineer
```

## Acceptance Criteria

- [x] Agent file enhanced with template-specific sections
- [x] Relevant templates identified and documented
- [x] Code examples from templates included
- [x] Best practices documented
- [x] Anti-patterns documented (if applicable)

## Completion Summary

Enhanced from 30-line stub to ~290-line comprehensive agent definition. Added:
- YAML discovery metadata (stack, phase, capabilities, keywords)
- Expanded Purpose with specific responsibilities
- Why This Agent Exists with 3 concrete failure modes
- Quick Start with 4 invocation scenarios and example prompts
- Boundaries (7 ALWAYS, 7 NEVER, 4 ASK rules)
- 7 specific Capabilities
- 4 Related Templates with exact file paths
- 3 Code Examples (Player prompt, Coach prompt, factory concatenation pattern)
- 3 Common Patterns (JSON enforcement, domain placeholder, memory injection)
- 5 Best Practices
- 4 Anti-Patterns with correct/wrong examples
- 5 Integration Points with sibling agents

## Metadata

```json
{
    "type": "agent_enhancement",
    "agent_file": "/Users/richardwoollcott/.agentecflow/templates/langchain-deepagents/agents/system-prompt-engineer.md",
    "template_dir": "/Users/richardwoollcott/.agentecflow/templates/langchain-deepagents",
    "template_name": "langchain-deepagents",
    "agent_name": "system-prompt-engineer"
}
```
