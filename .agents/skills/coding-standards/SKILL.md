---
name: coding-standards
description: Style rules, typing rules, naming conventions, logging conventions, and error-handling philosophy
---

## Style Rules

### Formatting
- Follow PEP 8 (enforced by default Python tooling)
- Line length: 100 characters (project convention, not strict)
- Use 4 spaces for indentation (no tabs)
- Trailing commas in multi-line collections

### Imports
- Standard library imports first, then third-party, then local
- Use absolute imports for local modules: `from my_stats_dashboard import update`
- Avoid wildcard imports (`from module import *`)

### Type Hints
- **Required** on all public functions and methods
- Use modern syntax: `list[str]`, `dict[str, int]`, `int | None` (Python 3.10+)
- Use `from __future__ import annotations` if needed for forward references
- Annotate return types explicitly

### Naming Conventions
| Entity | Convention |
|--------|------------|
| Modules | `snake_case` |
| Classes | `PascalCase` |
| Functions/Methods | `snake_case` |
| Constants | `UPPER_SNAKE_CASE` |
| Type variables | `PascalCase` (e.g., `T`, `KT`, `VT`) |
| Private (module/class) | `_leading_underscore` |

### Docstrings
- Google-style docstrings for public functions/classes
- One-line summary for simple functions
- Args, Returns, Raises sections for complex functions

---

## Error-Handling Philosophy

- **Fail fast** on programming errors (assertions, type errors)
- **Retry with backoff** on transient external failures (network, API rate limits)
- Use custom exception types for retryable vs permanent errors (see `RetryableHTTPError` in update.py/stars.py)
- Never silently swallow exceptions — log or re-raise
- Use `tenacity` for structured retry logic with explicit stop/wait conditions

---

## Logging Conventions

- Use `print()` for CLI output (this project is CLI-oriented)
- Prefix with descriptive context: `print(f"Fetching {pkg}...")`
- Use `print(f"  Retryable error {code} for {pkg}, will retry...")` for retry logs
- Avoid `logging` module unless structured logging is needed

---

## Project-Specific Conventions

### API Clients
- Use `httpx.Client` with explicit timeout (default 30s)
- Use context manager: `with httpx.Client(timeout=30) as client:`
- Set `follow_redirects=True` for GitHub API

### Data Persistence
- JSON files use `indent=2, sort_keys=True` for consistent git diffs
- Date keys: ISO 8601 (`YYYY-MM-DD`) strings
- Aggregate version-level counts to daily totals (see `update.py:55-57`)

### Configuration
- Load `.env` via `python-dotenv` at script entry point
- Never hardcode API keys or tokens

---

## Prohibited Patterns

- Bare `except:` — always specify exception type
- Mutable default arguments (`def foo(items=[])`)
- Global mutable state (except module-level constants)
- `time.sleep()` in production paths (only in CLI scripts for rate limiting)
- Hardcoded URLs — use constants at module top

---

## Exclude from this skill
- Commands to run tools (see `dev-setup`, `dev-workflow`)
- Procedural workflows (see `dev-workflow`)