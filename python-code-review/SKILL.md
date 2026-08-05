---
name: python-code-review
description: Reviews Python code changes for quality, correctness, and adherence to project conventions before commits or PRs. Checks for SOLID violations, DRY/YAGNI issues, missing tests, type safety, security concerns, and style compliance. Invoke this skill any time the user asks for a review — including brief or casual phrasing like "quick review", "check this over", or "does this look OK" — rather than reviewing inline directly; the forked subagent context is worth paying for even on "quick" asks, since a casual tone doesn't mean lower stakes. Also invoke it as a step within a larger multi-part request (e.g. implement-then-test-then-review workflows), even without an explicit /python-code-review call. Python-specific — covers ruff, pyright, pytest, and modern Python 3.13+ idioms by default (falls back to the project's pyproject.toml `requires-python` floor if it pins something lower). For deep silent-failure hunting or type-invariant design, use code-review's targeted agents instead.
context: fork
agent: general-purpose
allowed-tools: Read, Grep, Glob, Bash
---

# Python Code Review

Thorough code review of recent Python changes. Focuses on what matters: correctness, design, and maintainability.

## Step 1: Gather Context

1. Run `git diff` to see unstaged changes (or `git diff --cached` for staged, or `git diff main...HEAD` for full branch diff)
2. Read the project's `CLAUDE.md` and `pyproject.toml` for conventions (ruff rules, pyright config, test config, and the `requires-python` version floor)
3. Read each changed file in full to understand surrounding context
4. Run the tooling on the changed files and capture the real output — don't eyeball what a tool can decide:
   - `ruff check <changed files>` and `ruff format --check <changed files>` for lint and formatting
   - `pyright <changed files>` (or the project's configured type checker) for type errors
   Fold the concrete findings into the report. If a tool isn't installed or configured, note that and fall back to manual inspection.

## Step 2: Review (in priority order)

### 2a. Correctness

- Logic errors, off-by-one, wrong comparisons, missing return paths
- Race conditions, resource leaks, unhandled exceptions at boundaries
- Null/None handling — does the code handle missing data at system boundaries?
- API contract violations — does the public interface match its protocol/ABC?

### 2b. Security (OWASP-aware)

- Injection risks (SQL, command, template)
- Secrets or credentials in code or config
- Input validation at system boundaries (user input, external APIs)
- Overly permissive access or missing auth checks

### 2c. Design Principles

**SOLID:**
- **S** — Does each class/module have one reason to change?
- **O** — Can behavior be extended without modifying existing code?
- **L** — Do subtypes honor the contracts of their base types?
- **I** — Are interfaces focused, or do they force unused dependencies?
- **D** — Do high-level modules depend on abstractions, not concretions?

**DRY** — Flag duplicated logic (3+ occurrences). Do NOT flag intentional similarity in tests.

**YAGNI** — Flag speculative abstractions, unused parameters, configurability nobody asked for.

**KISS** — Flag unnecessary complexity. If 50 lines can replace 200, say so.

### 2d. Python Quality

- Type hints on all public interfaces (Python 3.13+ syntax by default: `str | None`, not
  `Optional[str]` — unless `pyproject.toml`'s `requires-python` pins an older floor, in
  which case follow that floor instead)
- Functions under 30 lines; if longer, suggest decomposition
- Composition over inheritance
- Context managers for resources, generators for memory efficiency
- No `print()` statements (use logging)
- Google-style docstrings on public APIs
- Protocol pattern over ABCs where appropriate

### 2e. Style & Linting

- Report the real `ruff` and `pyright` findings from Step 1 — don't re-derive lint, formatting, or type errors by eye.
- Beyond the tools: naming consistency with the surrounding codebase, and any dead code the linter isn't configured to catch.

### 2f. Test Quality

- New behavior has corresponding tests
- Tests follow Red-Green-TDD: does the test actually fail without the implementation?
- AAA pattern (Arrange-Act-Assert)
- Uses `pytest.param()` with `id` for parametrized tests (never bare tuples)
- Tests cover: happy path, edge cases, error paths
- No testing of framework behavior or trivial getters
- Mocks only at boundaries; prefer dependency injection

### 2g. Comments & Docstrings (changed lines only)

- Flag comments in the diff that are stale (describe code that has since changed), redundant (restate what the code obviously does), or misleading.
- Where a comment is worth keeping but verbose or awkward, suggest a tighter, natural, plain-language rewrite.
- Check docstrings on added/changed modules, classes, and functions: they should state purpose (plus args/returns where non-obvious) in plain language. Simplify overcomplicated, padded, or lengthy docstrings to a concise Google-style form — a one-line summary is enough when the signature is self-explanatory.
- Don't request new comments or docstrings on code that already reads clearly.

### 2h. Simplification (brief)

- Spot changed code that's more complex than it needs to be: redundant branches, needless intermediate variables, reimplemented stdlib, over-nesting.
- Offer the simpler form in one line. Keep it light — the one or two highest-value simplifications, not a full rewrite.

## Step 3: Report

Output a structured review using this format:

```
## Review Summary

**Scope**: [files reviewed, lines changed]
**Verdict**: APPROVE | REQUEST_CHANGES | COMMENT

## Critical (must fix)
- [file:line] Issue description → Suggested fix

## Warnings (should fix)
- [file:line] Issue description → Suggested fix

## Suggestions (consider)
- [file:line] Improvement idea

## What's Good
- Brief note on well-done aspects (keep to 1-3 points)
```

## Rules

- Apply every rule below to **each** changed file, not a representative sample.
- Review ONLY changed code. Do not critique pre-existing code unless the change makes it worse.
- Report anything that could cause incorrect behavior, a test failure, a security issue, or a
  misleading result. Omit only pure style and naming nits that ruff already catches or that are
  preference-level. Sort what remains into the Critical / Warnings / Suggestions tiers — the
  tiers do the filtering, not you.
- Be specific: reference exact file and line, show the problematic code, show the fix.
- Do not nitpick formatting that ruff would auto-fix.
- Do not suggest adding comments/docstrings to code you didn't write.
- If no issues found, say so. Don't invent problems.
- This skill owns general quality, comment clarity, light simplification, and test
  coverage. For deep silent-failure hunting or type-invariant design, use `code-review`'s
  targeted agents (silent-failure-hunter / type-design-analyzer) instead of duplicating
  that depth here.
- For the checklist, see [checklist.md](checklist.md).
