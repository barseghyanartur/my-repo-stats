import json
import os
import time
import datetime
import httpx
from dotenv import load_dotenv
from pathlib import Path
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_chain,
    wait_fixed,
)

RETRY_STATUS_CODES = {429, 403, 500, 502, 503, 504}
OWNER = os.environ.get("GITHUB_USERNAME", "barseghyanartur")
SLEEP_BETWEEN_REPOS = 2  # seconds


class RetryableHTTPError(Exception):
    """Raised for HTTP status codes that warrant a retry."""


def _fetch_stars(client: httpx.Client, repo: str, token: str) -> int | None:
    """Fetch total stars for a single repo."""

    headers = {"Authorization": f"token {token}"} if token else {}

    @retry(
        retry=retry_if_exception_type((RetryableHTTPError, httpx.TransportError)),
        wait=wait_chain(wait_fixed(2), wait_fixed(3), wait_fixed(5)),
        stop=stop_after_attempt(4),
        reraise=True,
    )
    def _do_request() -> httpx.Response:
        resp = client.get(
            f"https://api.github.com/repos/{OWNER}/{repo}",
            headers=headers,
        )
        if resp.status_code in RETRY_STATUS_CODES:
            print(f"  Retryable error {resp.status_code} for {repo}, will retry...")
            raise RetryableHTTPError(f"HTTP {resp.status_code}")
        return resp

    resp = _do_request()

    if resp.status_code == 404:
        print(f"  Repo not found: {OWNER}/{repo}")
        return None
    if resp.status_code == 401:
        print(f"  Unauthorized: check GITHUB_TOKEN")
        return None
    if resp.status_code != 200:
        print(f"  Error {resp.status_code} for {repo}: {resp.text}")
        return None

    return resp.json().get("stargazers_count", 0)


def main():
    current_dir = Path(__file__).resolve().parent.parent
    parent_dir = current_dir.parent

    dotenv_path = parent_dir / ".env"
    load_dotenv(dotenv_path=dotenv_path)

    TOKEN = os.environ.get("GITHUB_TOKEN")
    DATA_FILE = parent_dir / "github_stars_data.json"
    PACKAGES_FILE = parent_dir / "github_repos.json"

    with open(PACKAGES_FILE) as f:
        packages = json.load(f)

    if DATA_FILE.exists():
        with open(DATA_FILE) as f:
            data = json.load(f)
    else:
        data = {"last_updated": None, "repos": {}}
    data.setdefault("repos", {})
    data.setdefault("last_updated", None)

    today = datetime.datetime.utcnow().date().isoformat()

    with httpx.Client(timeout=30, follow_redirects=True) as client:
        for i, repo in enumerate(packages):
            if i > 0:
                print(f"  Waiting {SLEEP_BETWEEN_REPOS}s before next repo...")
                time.sleep(SLEEP_BETWEEN_REPOS)

            print(f"Fetching {OWNER}/{repo}...")
            stars = _fetch_stars(client, repo, TOKEN)
            if stars is not None:
                if repo not in data["repos"]:
                    data["repos"][repo] = {}
                data["repos"][repo][today] = stars

    data["last_updated"] = datetime.datetime.utcnow().isoformat()

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2, sort_keys=True)

    print("Done. Stars updated.")


if __name__ == "__main__":
    main()