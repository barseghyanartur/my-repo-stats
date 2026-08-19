.PHONY: help init install update update-stars update-pypi serve test clean sync run

help:       ## Show this help message
	@echo "PyPI Downloads Dashboard"
	@echo ""
	@echo "Available targets:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "      %s\n", $$1}' $(MAKEFILE_LIST)

init:       ## Copy .env.example to .env (if not present)
	@test -f .env || (cp .env.example .env && echo "Created .env — fill in your API keys") || true

install:   ## Install dependencies from pyproject.toml
	uv pip install .

sync:      ## Sync dependencies from pyproject.toml to .venv
	uv sync

update-pypi:    ## Fetch latest download data from pepy.tech API (updates pypi_downloads_data.json)
	uv run my-stats

update-stars: ## Fetch latest stars from GitHub API (updates github_stars_data.json)
	uv run python -c "from my_stats_dashboard.stars import main; main()"

update: update-stars update-pypi

serve:     ## Serve the dashboard locally (http://localhost:8000)
	@echo "🚀 Starting local server at http://localhost:8000"
	@echo "   (Ctrl+C to stop)"
	uv run python -m http.server 8000

test:      ## Run all tests with pytest
	uv run pytest . -v --cov=my_stats_dashboard

clean:     ## Remove generated data and venv
	rm -f pypi_downloads_data.json github_stars_data.json
	rm -rf .venv
	@echo "🧹 Cleaned generated files"

run:       ## Run the main application
	uv run python -m my_stats_dashboard
