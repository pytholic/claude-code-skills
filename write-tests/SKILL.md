---
name: write-tests
description: Write focused pytest tests covering critical paths, edge cases, and error handling. Avoids redundant tests that bloat codebase. Use for creating minimal but comprehensive test coverage of complex logic, public APIs, and failure scenarios.
arguments:
  - name: target
    description: File path to test (e.g., "src/module.py") or code string to write tests for
    required: true
  - name: focus
    description: Test focus - "critical" (default, core logic only), "full" (include edge cases), or "integration"
    required: false
---

# Pytest Test Writing - Focused & Valuable

Write minimal, high-value tests. Avoid testing trivial code, framework behavior, or implementation details.

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

- Python 3.12+ type hints (`str | None`)
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