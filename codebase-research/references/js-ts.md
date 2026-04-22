# JavaScript / TypeScript — Codebase Research Patterns

Load this file when the project is JS or TS based. Use these patterns in Phase 2 instead of the generic ones in SKILL.md.

All commands use `git grep`. Substitute `rg` or `grep -rn` if not in a git repo.

---

## Symbol Definitions

```bash
git grep -n 'class SYMBOL\b'                                         # Class
git grep -n -E '(function SYMBOL\b|const SYMBOL\s*=.*=>)'           # Function (all styles)
git grep -n -E '^(type|interface) SYMBOL\b'                         # Type alias or interface
git grep -n -E '^export (const|function|class|type|interface) SYMBOL\b'  # Named export
```

---

## Import Patterns & Aliases

```bash
# Who imports from a specific module path
git grep -n -E "from ['\"].*MODULE['\"]"

# CommonJS require
git grep -n -E "require\(['\"].*MODULE['\"]\)"

# Who imports a specific named symbol
git grep -n -E "import.*\bSYMBOL\b.*from"
```

**Aliasing — always check:**
```bash
# Named alias:    import { Foo as Bar } from '...'
git grep -n "import.*SYMBOL as"

# Namespace alias: import * as Bar from '...'
git grep -n "import \* as"
```
If an alias is found, run a secondary Usage Search (2B in SKILL.md) for the alias name.

---

## Common Structural Patterns

```bash
git grep -n -E '^(interface|export interface) '                      # Interfaces
git grep -n -E '^(type|export type) \w+\s*='                        # Type aliases
git grep -n -E '^(enum|export enum|const enum) '                    # Enums
git grep -n -E '(export.*function \w+.*React|const \w+.*:\s*FC|const \w+.*ReactNode)'  # React components
git grep -n -E '(router|app)\.(get|post|put|patch|delete)\('        # Express / Fastify routes
git grep -n -E 'class \w+Error extends '                            # Custom error classes
git grep -n -E '@(Injectable|Controller|Module|Entity|Column|Get|Post|Put|Delete)'  # TS decorators (NestJS etc.)
```

---

## Module Orientation

```bash
# Public API entry points (barrel files)
git ls-files | grep -E '(^|/)index\.(ts|js)$'

# All exports from a module
git grep -n '^export ' -- 'module_path/*'

# Barrel re-exports (architectural seams — good for understanding boundaries)
git grep -n -E '^export \* from|^export \{'

# Largest files (most logic)
git ls-files | grep -E '\.(ts|js|tsx|jsx)$' \
  | xargs wc -l 2>/dev/null | sort -rn | head -10
```

---

## Architecture Signals

```bash
# Entrypoints
git grep -l -E '(ReactDOM\.render|createRoot|app\.listen|server\.listen)'

# package.json main/exports/scripts
cat package.json | python3 -c "import sys,json; d=json.load(sys.stdin); [print(k,':',d[k]) for k in ('main','exports','scripts') if k in d]" 2>/dev/null

# Path aliases (tsconfig)
grep -A20 '"paths"' tsconfig.json 2>/dev/null

# Wiring / DI / container files
git ls-files | grep -iE 'dependencies\.|container\.|config\.|settings\.|providers\.|module\.'
```
