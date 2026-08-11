# claude-skills

Personal Claude Code skill library — specialized workflows for Python development, debugging, code review, LLM engineering, and more.

## Install

First, add the marketplace (one-time setup):

```
/plugin marketplace add pytholic/claude-skills
```

Then install all skills at once:

```
/plugin install all@pytholic-skills
```

Or install a single skill:

```
/plugin install python-dev@pytholic-skills
```

Replace `python-dev` with any skill name from the table below.

### Update
```
# 1. Refresh the marketplace to pick up new versions (one-time per update)
/plugin marketplace update pytholic-skills

# 2. Reinstall to pull the latest version of the skill
/plugin install hac-init@pytholic-skills
```

## Available skills

| Skill | Description |
|---|---|
| `python-code-review` | Structured review for quality, correctness, SOLID/DRY/YAGNI, type safety, and security |
| `codebase-research` | Navigate and map codebases — find symbols, trace dependencies, answer architecture questions |
| `explain-code` | Step-by-step walkthroughs with analogies and diagrams, depth matched to the question |
| `llm-dev` | LLM architectures, RAG, fine-tuning, agentic workflows, evals, and production deployment |
| `playwright-cli` | Browser automation and Playwright test workflows |
| `python-dev` | Planning-first Python development with Python 3.13+, ruff, pyright, pytest, pyproject.toml |
| `systematic-debugging` | Four-phase debugging: reproduce → isolate → root cause → fix |
| `task-handover` | Structured HANDOVER.md for cold-start session resumption |
| `write-tests` | Focused pytest coverage for critical paths, edge cases, and error handling |
| `excalidraw-diagram` | Generate Excalidraw diagrams from text descriptions |
| `hac-init` | Initialize a Human-Agent Context (HAC) directory with templates and bootstrapping process |
| `python-project-scaffold` | Scaffold a new Python project with production-ready tooling and structure |
| `help` | User-facing cheat sheet of all personal skills — invoke with `/help` |
| `goal-workflow` | Implement a spec fully, verify each requirement with parallel agents, and produce a report |
| `interview-me` | One-question-at-a-time intent extraction for underspecified asks, until ~95% confidence |
| `pr-description` | Generate a minimal, clear PR description from the branch diff and the repo's PR template |
| `task-scope-and-spec` | Scope a loose engineering task into a tight, testable spec list. |
| `planning-and-task-decomposition` | Decompose a scoped goal into an ordered, verifiable implementation plan with checkpoints |
| `guided-implementation` | Guide you through writing the code yourself, one piece per turn — human-driven counterpart to `goal-workflow` |

## Shared rules

Some rules are inlined into several skills so each stays self-contained. **`shared/`
holds the canonical copy.** When you change one there, propagate to every listed location
in the same commit.

### Minimality ladder

Canonical text: [`shared/minimality-ladder.md`](shared/minimality-ladder.md). Adapted from
[ponytail](https://github.com/DietrichGebert/ponytail) (MIT).

Edit that file, then run the sync script to propagate:

```bash
python3 scripts/sync_shared_rules.py --check   # report drift, exit 1 if any
python3 scripts/sync_shared_rules.py --fix     # rewrite copies from shared/
```

Copies are delimited by `<!-- BEGIN shared: minimality-ladder -->` /
`<!-- END shared: minimality-ladder -->`. Only the text between the markers is replaced —
the framing around each copy differs per skill on purpose and is left alone.

Skills carry inlined copies rather than importing, so each stays self-contained when
installed from the marketplace — a consumer gets the rule without needing this repo or a
global CLAUDE.md. CLAUDE.md imports instead, because it lives in a different repo.

| Location | How it's carried |
|---|---|
| `~/.claude/CLAUDE.md` — §2 | `@` import — **not a copy, cannot drift** |
| `python-dev/SKILL.md` — Phase 2a | inlined copy |
| `python-code-review/SKILL.md` — 2c | inlined copy |
| `guided-implementation/SKILL.md` — turn contract | inlined copy |

### Enforcing sync

A pre-commit hook blocks a commit while copies have drifted. It isn't version-controlled,
so set it up once per clone:

```bash
cat > .git/hooks/pre-commit <<'EOF'
#!/bin/sh
python3 "$(git rev-parse --show-toplevel)/scripts/sync_shared_rules.py" --check || {
    echo "shared rules drifted — run: python3 scripts/sync_shared_rules.py --fix"
    exit 1
}
EOF
chmod +x .git/hooks/pre-commit
```

Adding a second shared rule needs no code change — create `shared/<name>.md` with matching
BEGIN/END markers and the script picks it up.

## Repo layout

```
<skill-name>/SKILL.md   one directory per skill
shared/                 canonical text for rules inlined into several skills
scripts/                authoring-time tooling (not shipped behaviour)
```

## Usage

Once installed, invoke a skill in Claude Code:

```
/python-dev
/systematic-debugging
/code-review
```

Each skill's `SKILL.md` contains the full workflow and instructions Claude follows.
