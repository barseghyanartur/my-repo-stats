---
name: pr-review
description: Deterministic pull-request review behavior with numbered checklist
---

## PR Review Checklist

Review every PR against this checklist. Report findings explicitly.

### 1. Architecture & Invariants
- [ ] Does the change respect **single static HTML** invariant? (No build step introduced)
- [ ] Are `pypi_downloads_data.json` / `github_stars_data.json` **never modified directly** in the PR? (Only regenerated via scripts)
- [ ] Is `.env` **not committed**? (Secrets in GitHub Actions only)
- [ ] Does the change preserve **zero build step**? (index.html remains standalone)
- [ ] Are all Python invocations using `uv run`? (No bare `python`/`pytest`)

### 2. Code Quality
- [ ] Type hints on all new public functions/methods?
- [ ] Custom exceptions used for retryable vs permanent errors?
- [ ] `httpx.Client` with timeout and context manager?
- [ ] No bare `except:` clauses?
- [ ] No mutable default arguments?
- [ ] ISO 8601 date format (`YYYY-MM-DD`) for JSON keys?

### 3. Testing
- [ ] Step 0 test decision made? (New tests for behavior changes, regression test for bugs)
- [ ] Unit test for specific component changed?
- [ ] Integration test for system-level behavior?
- [ ] Happy-path test confirming no regression?
- [ ] All tests pass (`make test`)?

### 4. Configuration & Data
- [ ] `pypi_packages.json` / `github_repos.json` remain flat JSON arrays?
- [ ] No nested structures introduced?
- [ ] `PEPY_API_KEY` / `GITHUB_USERNAME` only via env/secrets?
- [ ] `GITHUB_USERNAME` configured via env var (not hardcoded)?

### 5. Documentation
- [ ] README.rst updated if user-facing behavior changed?
- [ ] AGENTS.md updated if architecture/workflow changed?
- [ ] SKILL.md files updated if procedures changed?
- [ ] Code examples in docs match actual API?

### 6. CI/CD
- [ ] GitHub Actions workflow (`.github/workflows/update.yml`) still runs daily at 18:00 UTC?
- [ ] Workflow triggers on `pypi_packages.json` / `github_repos.json` changes?
- [ ] No hardcoded secrets in workflow?

### 7. Security
- [ ] No API keys, tokens, or secrets in code or commit history?
- [ ] `.env` in `.gitignore`?
- [ ] Dependencies pinned in `uv.lock`?

---

## Reporting Expectations

For each checklist item:
- **Pass**: ✅
- **Fail**: ❌ with file:line and description
- **N/A**: ➖ with justification

Summarize:
- **Blocking issues** (must fix before merge)
- **Non-blocking suggestions** (nice to have)
- **Questions** (clarification needed)

---

## Exclude from this skill
- Implementation guidance (see `coding-standards`)
- Development workflow details (see `dev-workflow`)
- Environment setup (see `dev-setup`)