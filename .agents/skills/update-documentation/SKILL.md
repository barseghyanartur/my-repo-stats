---
name: update-documentation
description: Documentation policy and agent-based synchronization to keep docs aligned with code
---

## Operation Mode

- **Pure agent-based synchronization** — no scripts are used
- **Docs are updated to match code** — code is never changed to match docs
- Agent reads code, scans docs, identifies misalignments, auto-fixes safely, reports changes

---

## Ground Truth and Authority Hierarchy

1. **Code** — ground truth for API, CLI, defaults, exceptions, configuration behavior
2. **AGENTS.md** + **SKILL.md** — policy; must match reality
3. **README.rst** — end-user documentation; must match code and policy
4. **Exclusions** — auto-generated/vendored docs are not modified

---

## Agent-Based Sync Process (Step-by-Step)

### Step 1: Extract Ground Truth from Code
Scan for:
- Public API (functions, classes, constants exported in `__init__.py` or `pyproject.toml` scripts)
- CLI commands/options (Makefile targets, `pyproject.toml` `[project.scripts]`)
- Exceptions raised (custom exception classes, retry logic)
- Defaults/limits (constants at module top: `RETRY_STATUS_CODES`, `SLEEP_BETWEEN_PACKAGES`, `OWNER`, etc.)
- Environment variables (`.env` usage in code)
- Config file formats (`pypi_packages.json`, `github_repos.json` structure)

### Step 2: Scan Documentation Files
Read:
- `README.rst` (user-facing)
- `AGENTS.md` (agent-facing policy)
- All `.agents/skills/**/SKILL.md` (procedural skills)
- `pyproject.toml` (metadata)
- `Makefile` (targets and help text)

### Step 3: Identify Misalignments
Check for:
- Missing items in docs that exist in code
- Outdated references (old paths, renamed functions, changed signatures)
- Broken file paths in docs
- Stale defaults/limits in examples or tables
- Wrong examples (API calls that no longer work)
- Inconsistent terminology

### Step 4: Auto-Fix Documentation Safely
Edit docs to match code:
- Update tables, lists, examples
- Fix cross-references and file paths
- Correct stale defaults/limits
- Preserve intent while correcting facts
- **Never invent behavior** — only document what code actually does
- Minimize diffs (no unnecessary reformatting)

### Step 5: Report Changes
Output:
- Files changed
- What changed (specific sections/lines)
- What could not be fixed automatically (requires human decision)
- Why (missing info, ambiguous intent, etc.)

---

## Documentation Files Overview and Targeting Rules

| File | Audience | Responsible For | When to Update |
|------|----------|-----------------|----------------|
| `README.rst` | End users | Quick start, features, config, deployment, Makefile commands | User-facing behavior changes, new CLI targets, config format changes |
| `AGENTS.md` | Agents | Architecture invariants, hard constraints, known behaviors, mandatory workflow, config authority | Architecture changes, new invariants, workflow changes, config authority changes |
| `.agents/skills/dev-setup/SKILL.md` | Agents | Environment setup, tool invocation rules, recovery steps | Runtime prefix changes, new dependencies, new recovery procedures |
| `.agents/skills/dev-workflow/SKILL.md` | Agents | Definition of Done, mandatory sequence, retry logic | Test/lint commands change, new steps added, retry limits change |
| `.agents/skills/coding-standards/SKILL.md` | Agents | Style, typing, naming, error-handling, logging | New conventions adopted, prohibited patterns added |
| `.agents/skills/pr-review/SKILL.md` | Agents | PR review checklist, reporting expectations | New review criteria, architecture invariants added |
| `.agents/skills/update-documentation/SKILL.md` | Agents | Documentation policy, sync process, targeting rules | New doc files added, authority hierarchy changes |

---

## Feature-Specific Documentation Checklist

### Adding an Exception
- [ ] Document in `coding-standards` (error-handling philosophy)
- [ ] Add to PR review checklist if it affects API contracts
- [ ] Update any example showing error handling

### Adding CLI Commands/Options
- [ ] Add to `README.rst` Makefile Commands table
- [ ] Update `Makefile` help text (target `help`)
- [ ] Document in `dev-setup` if new tool invocation pattern

### Adding/Changing Public API
- [ ] Update type hints and docstrings in code
- [ ] Update `README.rst` if user-facing
- [ ] Update `AGENTS.md` if agent-facing (new script, changed behavior)

### Changing Defaults/Limits
- [ ] Update constant in code (single source of truth)
- [ ] Update `README.rst` examples showing the default
- [ ] Update `AGENTS.md` if it's a known intentional behavior
- [ ] Update `coding-standards` if it's a project-wide convention

---

## Code Example Rules (Documentation-as-Tests)

- If Markdown examples are intended to be runnable, enforce:
  - Use actual command names from Makefile/pyproject.toml
  - Use actual file paths from repository layout
  - Use actual environment variable names
- Preserve repository-specific conventions (RST format for README)
- No pseudo-code where runnable examples are expected

---

## Validation Checklist (Before Reporting Completion)

- [ ] README.rst examples match actual API/CLI
- [ ] AGENTS.md matches architecture and workflows
- [ ] SKILL.md descriptions remain accurate
- [ ] Cross-references and file paths are valid
- [ ] No generated docs were modified
- [ ] Any documentation tests required by the repository are respected

---

## What NOT To Do

- ❌ Do not modify source code to match docs
- ❌ Do not weaken policy encoded in SKILL.md or AGENTS.md
- ❌ Do not silently delete content; preserve intent while correcting facts
- ❌ Do not reformat docs unnecessarily; minimize diffs

---

## Exclude from this Skill

- Any dependency changes
- Any source code modifications
- Any "fix by changing code to match docs" behavior