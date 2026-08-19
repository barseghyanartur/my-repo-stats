---
name: dev-workflow
description: Full Definition of Done and mandatory lint → test sequence with retry logic
---

## Step 0 — Test Decision (REQUIRED, runs before any code change)

Every task starts with a test decision.

> **Step 0 — Test decision**: Before writing any code, decide:
>
> - Does this task change or add public API, behavior, or edge cases?
> - If yes, write or update tests first (or alongside the implementation).
> - If no, justify explicitly why no new tests are needed.
>
> **Bug fix sub-rule:** Write a regression test that reproduces the bug before implementing the fix. Run it — it must fail. Then fix the bug and confirm the test passes.
>
> **Test types:** When writing tests, cover all three:
>
> 1. Unit test — targets the specific function or class being changed
> 2. Integration test — verifies system-level behaviour end-to-end
> 3. Happy-path test — confirms the existing working flow has not regressed
>
> Never declare a task complete without having made this decision consciously.

---

## Mandatory Sequence (NON-SKIPPABLE)

This sequence is **mandatory for every task without exception**. No task is "too small" or "too obvious" to skip it.

### Runtime Rule
**ALWAYS use `uv run`.** Never call `python`, `python3`, `pytest`, `pip`, or any project tool directly — they will resolve to the wrong Python or missing dependencies. Every tool invocation must use `uv run` (or a `make` target that wraps it).

### Sequence

| Step | Action | Command |
|------|--------|---------|
| 0 | Test decision (see above) | — |
| 1 | Lint | No dedicated linter configured. Run type checking if available, else proceed. |
| 2 | Fix lint errors | Repeat Step 1 until clean |
| 3 | Test | `make test`  <br>`# = uv run pytest . -v --cov=my_stats_dashboard` |
| 4 | Fix test failures | Repeat Step 3 until all pass |
| 5 | Re-lint | Re-run Step 1 to catch regressions |
| 6 | Documentation gate | If public API, CLI flags, or defaults changed → run `update-documentation` skill |
| 7 | Pre-commit gate | No `.pre-commit-config.yaml` exists. Re-run all lint commands individually (as in Step 1) as final gate |

### Retry Logic
- Maximum **3 lint → test iterations** (Steps 1–5).
- After 3 iterations with unresolved issues: **stop and report**.

### Explicit Stop Conditions
- All tests pass
- Lint clean (or no linter configured)
- Documentation updated if API changed
- Pre-commit gate passes

---

## Definition of Done

A task is **done** only when:
- [ ] Step 0 test decision made and documented
- [ ] All tests pass (`make test`)
- [ ] Lint clean (Step 1)
- [ ] Documentation updated if public API/CLI/defaults changed (Step 6)
- [ ] Pre-commit gate passes (Step 7)

---

## Forbidden Actions

- Never skip tests to complete a task
- Never bypass linting to complete a task
- Never modify test assertions to make tests pass
- Never change code to match documentation (update docs instead)
- Never call tools without the required runtime prefix (`uv run`)
- Never skip Step 0 — always make a conscious test decision before coding
- Never declare done without running the pre-commit gate (final step)

---

## Exclude from this skill
- Environment setup (see `dev-setup`)
- Coding standards (see `coding-standards`)
- PR review checklist (see `pr-review`)