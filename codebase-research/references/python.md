# Python — Codebase Research Patterns

Load this file when the project is Python-based. Use these patterns in Phase 2 instead of the generic ones in SKILL.md.

All commands use `git grep`. Substitute `rg` or `grep -rn` if not in a git repo.

---

## Symbol Definitions

```bash
git grep -n '^class SYMBOL\b'                    # Class definition
git grep -n -E '^\s*def SYMBOL\b'                # Function or method
git grep -n '^SYMBOL\s*[=:]'                     # Constant or type alias
git grep -n '@dataclass' -A 1 | grep 'SYMBOL'    # Dataclass
```

---

## Import Patterns & Aliases

```bash
# Who imports a specific module
git grep -n -E '(from path\.to\.module import|import path\.to\.module)'

# Who imports a specific symbol
git grep -n -E 'from .* import.*\bSYMBOL\b'

# All imports in a file
head -50 path/to/file.py | grep -E '^import |^from '
```

**Aliasing — always check:**
```bash
# Look for: from module import Foo as Bar
git grep -n 'import SYMBOL as'
```
If an alias is found, run a secondary Usage Search (2B in SKILL.md) for the alias name.

---

## Common Structural Patterns

```bash
git grep -n '^class \w\+(.*BaseModel'                        # Pydantic models
git grep -n '^class \w\+(.*ABC\b'                            # Abstract base classes
git grep -n '^class \w\+(.*Protocol\b'                       # Protocols / structural typing
git grep -n '@dataclass' -l                                  # All dataclasses (file list)
git grep -n -E '^class \w+\(.*Error\b|.*Exception\b'        # Custom exceptions
git grep -n '@\(router\|app\)\.\(get\|post\|put\|patch\|delete\)'  # FastAPI / Flask routes
git grep -n 'Depends('                                       # FastAPI dependency injections
git grep -n -E '(os\.environ|os\.getenv|settings\.)'        # Env / config usage
```

---

## Module Orientation

```bash
# Public API surfaces
git ls-files | grep '__init__\.py$'

# All class and function signatures in a module (no bodies)
git grep -n -E '^(class |def |    def )' -- 'module_path/*'

# Largest files (most central logic)
git ls-files -- '*.py' | xargs wc -l 2>/dev/null | sort -rn | head -10
```

---

## Architecture Signals

```bash
# All packages (directories with __init__.py)
git ls-files | grep '__init__\.py$' | sed 's|/__init__\.py||' | sort

# Main execution entrypoints
git grep -l 'if __name__.*__main__'

# Declared CLI entrypoints
grep -A5 '\[project\.scripts\]\|\[console_scripts\]' pyproject.toml setup.cfg 2>/dev/null

# Wiring / DI files
git ls-files | grep -iE 'dependencies\.py$|container\.py$|providers\.py$|config\.py$|settings\.py$'
```
