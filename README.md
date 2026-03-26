# .claude

Personal Claude Code configuration — behavioral guidelines, custom skills, and agent definitions.

## Structure

| Path | Purpose |
|---|---|
| `CLAUDE.md` | Global behavioral guidelines (think-first, simplicity, surgical changes, goal-driven execution) |
| `settings.json` | Permissions, enabled plugins, and effort level |
| `skills/` | Reusable skill definitions for specialized workflows |
| `agents/` | Custom agent configurations for delegated tasks |

## Skills

- **code-review** — Structured code review with checklist
- **explain-code** — Visual diagrams and analogies for code explanation
- **llm-dev** — LLM architecture, fine-tuning, RAG, and agentic workflows
- **python-dev** — SOLID/OOP-driven Python development workflow
- **systematic-debugging** — Four-phase debugging with root cause analysis
- **write-tests** — Focused pytest coverage for critical paths and edge cases

## Agents

- **code-reviewer** — Automated code quality review
- **issue-analyzer-fixer** — Bug diagnosis and remediation
- **test-runner** — Test execution and failure reporting
