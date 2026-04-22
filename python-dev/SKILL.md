---
name: python-dev
description: Expert Python development workflow for the user's planning-first methodology. Use when architecting Python applications, refactoring code, or implementing features that need careful design. Biases toward simplicity and surgical changes over speculative abstractions. Applies OOP patterns (Factory, Strategy, DI) only when complexity justifies them. Uses Python 3.13+, ruff, pyright, pytest, pyproject.toml.
---

# Python Development Workflow

Expert Python development aligned with the user's CLAUDE.md principles: think before coding, simplicity first, surgical changes, goal-driven execution.

## Workflow

1. **Understand** — Clarify requirements, constraints, edge cases. Surface ambiguity; don't pick silently.
2. **Plan** — State a brief plan with verifiable success criteria for multi-step tasks.
3. **Implement** — Incremental, testable. Prefer flat, explicit, readable code.
4. **Verify** — Tests pass, ruff/pyright clean, behavior matches success criteria.

## Design Philosophy

**Simplicity first.** The minimum code that solves today's problem. No speculative flexibility, no patterns "in case we need them later."

**Patterns are tools, not defaults.** Factory / Strategy / Adapter / Dependency Injection are useful when complexity justifies them — usually when there are real alternate implementations, real testability needs, or real extension points. For one-off code, a plain function is better than a pattern.

**SOLID and DRY are guidance, not law.** Follow SRP and DIP when they reduce complexity. Don't extract an abstraction for a single caller. Three similar lines is better than a premature abstraction.

**Composition over inheritance.** Prefer protocols and duck typing over deep class hierarchies.

## Standards

- **Python 3.13+ type syntax**: `str | None`, `list[int]`, `dict[str, Any]` — never `Optional`, `List`, `Dict`.
- **Ruff + pyright** configured via `pyproject.toml`. Match the project's existing config.
- **Functions stay small and focused.** ~30 lines is a useful smell test, not a hard limit.
- **No `print()`** in library code — use `logging` or `structlog`.
- **Context managers** for resources (files, connections, locks).
- **Generators** for large/streaming data; don't materialize lists you'll iterate once.
- **Explicit over implicit**, flat over nested, early returns over deep pyramids.
- **Google-style docstrings** on public APIs. Skip docstrings on obvious internal helpers.

## Testing

- **pytest only** (never `unittest`).
- `pytest.param(..., id=...)` for parametrized cases — never bare tuples.
- Test behavior through public interfaces, not implementation details.
- Dependency injection > mocking. Mock only at system boundaries.
- See the `write-tests` skill for detailed test-writing guidance.

## Project Setup

- `.venv` at project root (use if it exists).
- `pyproject.toml` for config — ruff rules, pyright strictness, pytest options, dependencies.
- Module layout: `src/package/` with `tests/` mirroring the structure.

## Deliverables

For non-trivial work, provide:
1. Brief design rationale — what you chose and why.
2. Key tradeoffs surfaced (what was rejected and why).
3. The implementation.
4. Test strategy (what's covered, what isn't, why).

Skip the ceremony for trivial changes. A one-line fix doesn't need a design doc.
