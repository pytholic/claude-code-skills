# Code Review Checklist

Use this checklist for systematic reviews. Not every item applies to every change — use judgment.

## Correctness
- [ ] Logic handles all branches (if/else/match exhaustiveness)
- [ ] Edge cases: empty collections, None, zero, negative, boundary values
- [ ] Error handling at system boundaries (external APIs, user input, file I/O)
- [ ] Resources properly closed (files, connections, cursors)
- [ ] Async/concurrent code: no race conditions, proper awaiting

## Security
- [ ] No hardcoded secrets, tokens, or credentials
- [ ] Input sanitized before use in queries, commands, templates
- [ ] Auth checks present where required
- [ ] No overly broad exception handling hiding failures (`except Exception: pass`)

## Design
- [ ] Single Responsibility — each unit does one thing
- [ ] Open/Closed — new behavior via extension, not modification
- [ ] Liskov — subtypes honor base contracts
- [ ] Interface Segregation — no forced unused dependencies
- [ ] Dependency Inversion — depend on abstractions
- [ ] No premature abstraction (YAGNI) — code solves today's problem
- [ ] No duplicated logic across 3+ locations (DRY)
- [ ] Simplest solution that works (KISS)

## Python Quality
- [ ] Type hints on all public signatures (3.13+ syntax by default; fall back to the `requires-python` floor)
- [ ] Functions under 30 lines
- [ ] No `print()` — use structured logging
- [ ] Google-style docstrings on public APIs
- [ ] Context managers for resource management
- [ ] Protocol pattern over ABCs where appropriate

## Tests
- [ ] New/changed behavior has corresponding tests
- [ ] Tests would fail without the implementation (Red-Green)
- [ ] AAA pattern: Arrange-Act-Assert
- [ ] `pytest.param()` with `id` for parametrized tests
- [ ] Edge cases and error paths covered
- [ ] No testing of framework internals or trivial code
- [ ] Mocks only at boundaries

## Tooling
- [ ] `ruff check` and `ruff format --check` run on changed files; real findings reported
- [ ] `pyright` (or project type checker) run on changed files; type errors reported

## Comments & Docstrings
- [ ] Comments in the diff are accurate (not stale or misleading)
- [ ] No redundant comments restating the code
- [ ] Verbose/awkward comments tightened to concise, natural phrasing
- [ ] Docstrings on added modules/classes/functions are clear and intelligible
- [ ] Overcomplicated or lengthy docstrings simplified to concise Google-style

## Style
- [ ] Follows project ruff config (line length, import order, rules)
- [ ] Consistent naming with existing codebase
- [ ] No dead code introduced (unused imports, variables, functions)
