---
name: dev-setup
description: Environment setup, dependency installation, and recovery steps for common environment failures
---

## Tool Invocation Rules (MANDATORY)

Always prefix tool invocations with `uv run`.

Canonical test command (from Makefile):
```bash
make test          # = uv run pytest . -v --cov=my_stats_dashboard
```

All observed Makefile targets use `uv run`:
- `make install`   → `uv pip install .`
- `make sync`      → `uv sync`
- `make update`    → `uv run my-stats`
- `make update_stars` → `uv run python -c "from my_stats_dashboard.stars import main; main()"`
- `make serve`     → `uv run python -m http.server 8000`
- `make test`      → `uv run pytest . -v --cov=my_stats_dashboard`
- `make run`       → `uv run python -m my_stats_dashboard`

**Forbidden bare invocations** (use `uv run` instead):
- `python` / `python3`
- `pytest`
- `pip`
- `httpx` (as CLI, if any)
- `tenacity` (as CLI, if any)

These are forbidden because bare calls use the wrong Python version or missing dependencies — `uv run` resolves both automatically.

---

## Environment Setup

### Prerequisites
- Python ≥ 3.10 (managed by uv)
- uv package manager (https://docs.astral.sh/uv/)

### Installation

```bash
# Clone and enter repo
git clone <repo-url>
cd my-repo-stats

# Sync dependencies (creates .venv, installs from pyproject.toml + uv.lock)
make sync
# or directly:
uv sync

# Verify installation
make test
```

### Environment Variables

Create `.env` file in repo root (gitignored):
```bash
PEPY_API_KEY=pepy_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
GITHUB_USERNAME=your_github_username
```

- `PEPY_API_KEY`: Required for `make update` (fetching download data). Get from https://pepy.tech (Pro plan).
- `GITHUB_TOKEN`: Required for `make update_stars` (fetching stars). Classic PAT with `public_repo` scope.
- `GITHUB_USERNAME`: Required for `make update_stars` (fetching stars). Your GitHub username.

---

## Common Recovery Steps

| Problem | Solution |
|---------|----------|
| `uv run` fails with "command not found" | Install uv: `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| Dependencies out of sync | Run `make sync` or `uv sync` |
| Lock file corrupted | Delete `uv.lock` and run `uv sync` |
| Virtualenv issues | Run `make clean` then `make sync` |
| Tests fail due to missing API keys | Tests requiring live API are skipped by design; add keys to `.env` for local integration testing |

---

## Exclude from this skill
- Coding rules (see `coding-standards`)
- Lint/test loops (see `dev-workflow`)
- PR review logic (see `pr-review`)