---
name: write-tests
description: Write focused pytest tests covering critical paths, edge cases, and error handling. Avoids redundant tests that bloat codebase. Invoke this skill any time the user asks for tests to be written — including brief or casual phrasing like "write tests", "add tests for this", or "write important tests" — rather than writing tests inline directly. Also invoke it as a step within a larger multi-part request (e.g. implement-then-test-then-review workflows), even without an explicit /write-tests call.
arguments:
  - name: target
    description: File path to test (e.g., "src/module.py") or code string to write tests for. If omitted, infer it from context — the file(s) just implemented or most recently changed in this session.
    required: false
  - name: focus
    description: Test focus - "critical" (default, core logic only), "full" (include edge cases), or "integration"
    required: false
---

# Pytest Test Writing - Focused & Valuable

Write minimal, high-value tests. Avoid testing trivial code, framework behavior, or implementation details.

## Step 0: Resolve the target

If `target` wasn't given: use the file(s) just implemented or edited earlier in this session (check recent diffs / tool calls). If more than one file changed and it's not obvious which one needs coverage, ask which file(s) to target — don't guess silently across an ambiguous multi-file change.

## What to Test (Priority Order)

1. **Critical business logic** - Core algorithms, calculations, transformations
2. **Public API contracts** - Input/output behavior, state changes
3. **Error handling** - Exception cases, validation, recovery
4. **Edge cases** - Boundaries, empty/None, type coercion
5. **Integration points** - External dependencies, I/O operations

## What NOT to Test

- Trivial getters/setters, property access
- Framework/library code (trust pytest, FastAPI, Django, etc.)
- Implementation details (private methods, internal state)
- Configuration/constants without logic
- Auto-generated code (dataclasses, ORMs without custom logic)

## Test Structure

**Naming:** `test_<what>_<condition>_<expected>`

**ALWAYS use pytest.param() for parametrize - never bare tuples:**
```python
# CORRECT - Use pytest.param() with id
@pytest.mark.parametrize(
    ("input_val", "expected"),
    [
        pytest.param(5, 25, id="positive"),
        pytest.param(0, 0, id="zero"),
        pytest.param(-3, 9, id="negative"),
        pytest.param(None, None, id="none_input", marks=pytest.mark.xfail),
    ],
)
def test_square_returns_correct_value(input_val: int | None, expected: int | None):
    assert square(input_val) == expected


# INCORRECT - Bare tuples (less readable in test output)
@pytest.mark.parametrize(
    ("input_val", "expected"),
    [(5, 25), (0, 0), (-3, 9)],  # Don't do this
)


# Complex parametrization with pytest.param()
@pytest.mark.parametrize(
    ("user_data", "expected_status", "expected_error"),
    [
        pytest.param(
            {"name": "Alice", "email": "alice@example.com"},
            "success",
            None,
            id="valid_user",
        ),
        pytest.param(
            {"name": "", "email": "test@example.com"},
            "error",
            "Name cannot be empty",
            id="empty_name",
        ),
        pytest.param(
            {"name": "Bob", "email": "invalid"},
            "error",
            "Invalid email format",
            id="invalid_email",
        ),
    ],
)
def test_user_validation(
    user_data: dict[str, str],
    expected_status: str,
    expected_error: str | None,
):
    result = validate_user(user_data)
    assert result.status == expected_status
    assert result.error == expected_error


def test_divide_by_zero_raises_value_error():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)


@pytest.fixture
def user() -> User:
    return User(name="Test", email="test@example.com")
```

## Standards

- Python 3.13+ type hints (`str | None`) — or the project's `requires-python` floor if lower
- AAA pattern (Arrange-Act-Assert)
- ALWAYS use `pytest.param()` with descriptive `id` parameter
- Parametrize similar cases (avoid copy-paste tests)
- Fixtures for shared setup (function scope default)
- Dependency injection over mocking when possible
- One logical assertion group per test
- Never import any function or variable from conftest file. Always use fixture for shared setup.
- Use built-in fixtures where they fit: `tmp_path` for filesystem, `monkeypatch` for env/attr patching, `caplog` for log assertions, `capsys` for stdout/stderr.
- **ALWAYS use `pytest-mock` (`mocker` fixture) for mocking — never `unittest.mock` directly.**

```python
# CORRECT - pytest-mock
def test_something(mocker):
    mock_fn = mocker.patch("module.ClassName.method", return_value="value")
    mocker.patch.object(instance, "method", return_value="value")

# INCORRECT - unittest.mock
from unittest.mock import patch, MagicMock  # Don't do this
with patch("module.fn") as mock_fn:  # Don't do this
    ...
```

- **Extract repeated literal values (int/float/str) into named constants or variables — don't repeat the same magic value across tests.**

If the same literal value appears 2+ times across test cases (e.g. a threshold, a magic ID, an expected count), assign it to a module-level constant (`SCREAMING_SNAKE_CASE`) or a local variable with a name that says what it represents. This avoids silent drift when one occurrence gets updated and others don't, and makes the value's meaning explicit instead of a bare number.

```python
# BAD — same magic number repeated, meaning unclear
def test_apply_discount_below_threshold():
    assert apply_discount(49.99) == 49.99

def test_apply_discount_at_threshold():
    assert apply_discount(50.0) == 45.0

def test_apply_discount_above_threshold():
    assert apply_discount(75.0) == 67.5

# GOOD — named constant, reused, self-documenting
DISCOUNT_THRESHOLD = 50.0
DISCOUNT_RATE = 0.9

def test_apply_discount_below_threshold():
    assert apply_discount(DISCOUNT_THRESHOLD - 0.01) == DISCOUNT_THRESHOLD - 0.01

def test_apply_discount_at_threshold():
    assert apply_discount(DISCOUNT_THRESHOLD) == DISCOUNT_THRESHOLD * DISCOUNT_RATE
```

This applies within `pytest.param()` cases too — if several `pytest.param()` entries share a literal (e.g. the same expected error code), pull it into a constant referenced by each `id`/value instead of retyping it.

- **Extract repeated mock objects into fixtures — don't rebuild the same configured mock in every test.**

If the same mock object (same patch target + same attribute/return_value setup) appears in 3+ tests, define it once as a fixture in `conftest.py`. Tests that need different behavior override locally.

```python
# BAD — identical mock setup copy-pasted across tests
def test_fetch_user(mocker):
    mock_db = mocker.MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = User(id=1, name="Alice")
    mocker.patch("myapp.service.db", mock_db)
    ...

def test_update_user(mocker):
    mock_db = mocker.MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = User(id=1, name="Alice")
    mocker.patch("myapp.service.db", mock_db)
    ...

# GOOD — shared fixture in conftest.py
@pytest.fixture
def mock_db(mocker: MockerFixture) -> MagicMock:
    mock = mocker.MagicMock()
    mock.query.return_value.filter.return_value.first.return_value = User(id=1, name="Alice")
    mocker.patch("myapp.service.db", mock)
    return mock

def test_fetch_user(mock_db):
    ...

def test_update_user(mock_db):
    ...

# Override locally only when a test needs different behavior
def test_fetch_missing_user(mock_db):
    mock_db.query.return_value.filter.return_value.first.return_value = None
    ...
```

## Coverage Strategy

Coverage is a smell test, not a target. Chase *valuable* coverage, not a number:
- Critical business logic and error paths: aim for full coverage.
- Trivial code (dataclasses, constants, simple property access): skip. Use `# pragma: no cover` sparingly for unreachable branches.
- If the project sets a `--cov-fail-under` threshold in `pyproject.toml`, match it. Don't invent one.

```bash
pytest --cov=src --cov-report=term-missing
```

## Organization
```
tests/
├── conftest.py          # Shared fixtures only
├── test_module.py       # Mirror src/ structure
└── unit/integration/    # Optional grouping
```

## Deliverables

1. Focused test file with essential coverage
2. Parametrized tests using pytest.param() with clear ids
3. Error path coverage for public APIs
4. Fixtures in conftest.py only if reused 3+ times
5. Type hints throughout