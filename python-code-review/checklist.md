# Code Review Checklist

Reference only — the review dimensions live in `SKILL.md` Step 2. This file lists the
items that are easy to miss and are *not* already spelled out there. Do not run this as
a second pass over the diff; consult it when a change touches one of these areas.

## Easy to miss

- [ ] Exhaustiveness in `if`/`elif`/`match` — is the fall-through branch actually correct,
      or just the leftover case?
- [ ] Broad exception handling that hides failures (`except Exception: pass`, bare
      `except:`, swallowed errors with only a log line)
- [ ] Resources closed on the error path, not just the happy path (files, connections,
      cursors, async context managers)
- [ ] Mutable default arguments, and mutable class attributes shared across instances
- [ ] `async` code: unawaited coroutines, blocking calls inside an event loop, shared
      state across tasks
- [ ] Boundary values in the diff's own tests: empty collection, `None`, zero, negative,
      single-element

## Project conventions

- [ ] `requires-python` floor in `pyproject.toml` respected (3.13+ syntax by default)
- [ ] Naming prefixes follow the project convention (`make_*` pure factory,
      `create_*` side-effecting, `build_*` builder)
- [ ] New test helpers live in `conftest.py` as fixtures, not imported across test modules
