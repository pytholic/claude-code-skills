# claude-skills

Personal Claude Code skill library — specialized workflows for Python development, debugging, code review, LLM engineering, and more.

## Install a single skill

```
/plugin install skill-name@pytholic/claude-skills
```

Replace `skill-name` with any skill listed below.

## Install all skills

Clone the repo directly into your `~/.claude/skills/` directory:

```bash
git clone https://github.com/pytholic/claude-skills.git ~/.claude/skills
```

Or, if `~/.claude` is already a git repo, add it as a submodule:

```bash
git submodule add https://github.com/pytholic/claude-skills.git ~/.claude/skills
```

## Available skills

| Skill | Description |
|---|---|
| `code-review` | Structured review for quality, correctness, SOLID/DRY/YAGNI, type safety, and security |
| `codebase-research` | Navigate and map codebases — find symbols, trace dependencies, answer architecture questions |
| `explain-code` | Step-by-step walkthroughs with analogies and diagrams, depth matched to the question |
| `llm-dev` | LLM architectures, RAG, fine-tuning, agentic workflows, evals, and production deployment |
| `playwright-cli` | Browser automation and Playwright test workflows |
| `python-dev` | Planning-first Python development with Python 3.13+, ruff, pyright, pytest, pyproject.toml |
| `systematic-debugging` | Four-phase debugging: reproduce → isolate → root cause → fix |
| `task-handover` | Structured HANDOVER.md for cold-start session resumption |
| `write-tests` | Focused pytest coverage for critical paths, edge cases, and error handling |

## Usage

Once installed, invoke a skill in Claude Code:

```
/python-dev
/systematic-debugging
/code-review
```

Each skill's `SKILL.md` contains the full workflow and instructions Claude follows.
