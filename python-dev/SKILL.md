---
name: python-dev
description: Expert Python development workflow following SOLID principles, OOP design patterns, and modern best practices. Use when architecting Python applications, refactoring code, implementing complex features, or making design decisions requiring careful planning. Applies Factory Method, Strategy, Dependency Injection patterns. Creates modular architecture with pytest testing. For new project setup, see the python-project-scaffold skill instead.
---

# Python Development Workflow

Expert Python development following a planning-first methodology.

---

## Core Principle

**PLAN BEFORE YOU CODE. DESIGN BEFORE YOU IMPLEMENT.**

Never start writing code without understanding the requirements and selecting an architecture. A 10-minute design session prevents hours of refactoring.

---

## Triage Gate

Before starting, classify the work:

- **Small change** (bug fix, single function, config tweak): Skip to Implementation Standards. No formal design needed.
- **Medium feature** (new module, new endpoint, new service): Follow Phase 1 + 2 lightly, then implement.
- **Large feature / new subsystem** (multi-module, cross-cutting, architectural impact): Full workflow below.

When in doubt, default to the full workflow.

---

## Phase 1: Understand

Before any design work, answer these questions:

1. **What problem are we solving?** State the goal in one sentence.
2. **What are the inputs and outputs?** Data flowing in and out of the system.
3. **What are the constraints?** Performance, compatibility, external dependencies, existing patterns in the codebase.
4. **What are the edge cases?** Empty inputs, concurrent access, failure modes, missing data.
5. **What does "done" look like?** Acceptance criteria — how do we know this works?

Make routine calls yourself and state the assumption. Ask only when two readings of the requirement would lead to materially different designs.

---

## Phase 2: Design

### 2a. Architecture Decision

**The ladder comes first.** Rungs 1–6 mean there is no architecture decision to make — don't build it, reuse it, or use what exists. Everything in this phase applies only once the ladder has reached rung 7.

<!-- BEGIN shared: minimality-ladder -->
Before writing code, stop at the first rung that holds:

1. Does this need to exist? → no: don't build it
2. Already in this codebase? → reuse, don't rewrite
3. Stdlib does it? → use it
4. Native platform feature? → use it
5. Installed dependency? → use it
6. One line? → one line
7. Only then: the minimum that works

Walk the ladder *after* understanding the problem, not instead of it — read the code the
change touches and trace the real flow before picking a rung. Lazy about the solution,
never about reading.

**Never traded away, at any rung:** trust-boundary validation, data-loss handling,
security, accessibility. Code ends up small because it's necessary, not golfed.
<!-- END shared: minimality-ladder -->

Then select the right level of abstraction:

- **Simple function** — No state, no side effects, pure transformation → standalone function
- **Stateful component** — Manages internal state, lifecycle → class
- **Pluggable behavior** — Multiple strategies, swappable implementations → Protocol + Strategy
- **External boundary** — Database, API, file system → Interface + concrete adapter
- **Orchestration** — Coordinates multiple components → Facade or Service class

### 2b. Pattern Selection

Apply when complexity justifies — never introduce a pattern for a problem that doesn't exist:

| Problem | Pattern | When to use |
|---------|---------|-------------|
| Object creation varies by context | Factory Method | 3+ creation paths, or creation logic is complex |
| Algorithm varies by context | Strategy (via Protocol) | 2+ interchangeable behaviors |
| External system boundary | Adapter | Wrapping third-party APIs or infrastructure |
| Complex subsystem access | Facade | Simplifying a multi-step internal workflow |
| Cross-cutting concerns | Dependency Injection | Testing, swappable implementations |

**Composition over inheritance.** If you reach for a base class, ask whether a Protocol + composition achieves the same with less coupling.

### 2c. Module Layout

For a package that has earned one — not a default, and not a target to grow into. A single module is the right answer until it isn't:

```
package/
├── __init__.py          # Public API — re-exports only
├── core/
│   ├── interfaces.py    # Protocols and abstract contracts
│   ├── models.py        # Domain models (dataclasses / Pydantic)
│   └── exceptions.py    # Domain-specific exceptions
├── services/            # Business logic and orchestration
├── infrastructure/      # External adapters (DB, API clients, file I/O)
├── facade/              # High-level entry points (optional)
└── config.py            # Configuration loading
```

Dependencies flow inward: infrastructure → services → core. Core never imports from infrastructure.

---

## Phase 3: Implement

### Implementation Standards

- **Functions under 30 lines.** If longer, decompose.
- **Type hints everywhere** using Python 3.13+ syntax (`str | None`, not `Optional[str]`) — or the project's `requires-python` floor if lower.
- **PEP compliance** — follow project ruff and pyright config in `pyproject.toml`.
- **Explicit over implicit, flat over nested.**
- **Generators** for memory efficiency on large data.
- **Context managers** for any resource with a lifecycle (files, connections, cursors).
- **No `print()` statements** — use structured logging.
- **Google-style docstrings** on all public APIs.
- **Protocols over ABCs** where you don't need shared implementation.

### Error Handling

- Define domain-specific exceptions in `core/exceptions.py`.
- Catch specific exceptions, never bare `except Exception`.
- Validate at system boundaries (user input, external API responses, file reads).
- Use early returns to reduce nesting.

### Dependency Management

- Pin dependencies with version bounds (`>=2.0.0,<3.0.0`).
- Separate runtime, dev, and docs dependency groups.
- Use `uv` for environment management.

---

## Phase 4: Check

The acceptance check is the tooling: `ruff check` and `pyright` pass clean on the changed
files, and new behavior has tests that pass. Run them. Don't add a separate self-review
pass on top — for a deliberate quality review, invoke the `python-code-review` skill as its
own step.

The structural constraints (typed public interfaces, functions under 30 lines, no circular
imports, dependencies flowing inward, specific exception handling) are things to get right
while implementing in Phase 3, not a checklist to re-walk afterwards.

### Testing

Apply the project's testing skill if one exists. Otherwise:

- pytest (never unittest)
- `pytest.param()` with descriptive `id` for parametrized tests
- AAA pattern (Arrange-Act-Assert)
- Test edge cases and error paths
- Mock only at boundaries; prefer dependency injection
- Profile before optimizing

---

## Deliverables Format

Always provide:

1. **Design rationale** — Why this approach, what alternatives were considered
2. **Architecture decisions** — Patterns chosen and tradeoffs made
3. **Implementation** — Clean, modular code with clear separation of concerns
4. **Future considerations** — Extension points and known limitations

---

## Process Violations — Red Flags

Stop and correct if you catch yourself doing any of the following:

- Writing code before understanding requirements
- Introducing a design pattern without a concrete problem it solves
- Creating an inheritance hierarchy when composition would work
- Skipping type hints on public interfaces
- Catching broad exceptions to silence errors
- Adding speculative abstractions ("we might need this later")
- Writing a 100-line function instead of decomposing
