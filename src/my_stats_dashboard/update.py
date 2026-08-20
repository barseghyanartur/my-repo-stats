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

RETRY_STATUS_CODES = {429, 500, 502, 503, 504}
SLEEP_BETWEEN_PACKAGES = 5  # seconds


class RetryableHTTPError(Exception):
    """Raised for HTTP status codes that warrant a retry."""


def _fetch_package(client: httpx.Client, pkg: str, api_key: str) -> dict:
    """Fetch download data for a single package, raising RetryableHTTPError on
    transient failures so tenacity can retry, and returning None-sentinel on
    permanent client errors (4xx other than 429)."""

    @retry(
        retry=retry_if_exception_type((RetryableHTTPError, httpx.TransportError)),
        wait=wait_chain(wait_fixed(10), wait_fixed(15), wait_fixed(20)),
        stop=stop_after_attempt(4),  # 1 initial attempt + 3 retries
        reraise=True,
    )
    def _do_request() -> httpx.Response:
        resp = client.get(
            f"https://api.pepy.tech/api/v2/projects/{pkg}",
            headers={"X-API-Key": api_key},
        )
        if resp.status_code in RETRY_STATUS_CODES:
            print(f"  Retryable error {resp.status_code} for {pkg}, will retry...")
            raise RetryableHTTPError(f"HTTP {resp.status_code}")
        return resp

    resp = _do_request()

    if resp.status_code != 200:
        print(f"  Permanent error {resp.status_code} for {pkg}: {resp.text}")
        return {}

    api_data = resp.json()
    downloads = api_data.get("downloads", {})

    pkg_history = {}
    for date_str, ver_dict in downloads.items():
        total = sum(int(count) for count in ver_dict.values())
        pkg_history[date_str] = total

    return pkg_history


def main():
    # Get the path to the directory containing this script
    current_dir = Path(__file__).resolve().parent.parent

    # Go up one level to the parent directory
    parent_dir = current_dir.parent

    # Define the path to the .env file
    dotenv_path = parent_dir / '.env'

    # Load environment variables from .env file
    load_dotenv(dotenv_path=dotenv_path)

    API_KEY = os.environ.get("PEPY_API_KEY")
    DATA_FILE = parent_dir / "pypi_downloads_data.json"
    PACKAGES_FILE = parent_dir / "pypi_packages.json"

    # Load packages
    with open(PACKAGES_FILE) as f:
        packages = json.load(f)

    # Load existing data (or create new)
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            data = json.load(f)
    else:
        data = {"last_updated": None, "packages": {}}
    data.setdefault("packages", {})
    data.setdefault("last_updated", None)

    with httpx.Client(timeout=30) as client:
        for i, pkg in enumerate(packages):
            if i > 0:
                print(f"  Waiting {SLEEP_BETWEEN_PACKAGES}s before next package...")
                time.sleep(SLEEP_BETWEEN_PACKAGES)

            print(f"Fetching {pkg}...")
            pkg_history = _fetch_package(client, pkg, API_KEY)

            if pkg_history:
                # Merge (new data overwrites old, older history is preserved)
                if pkg not in data["packages"]:
                    data["packages"][pkg] = {}
                data["packages"][pkg].update(pkg_history)

    # Update timestamp
    data["last_updated"] = datetime.datetime.utcnow().isoformat()

    # Save
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2, sort_keys=True)

    print("Done. Data updated.")


if __name__ == "__main__":
    main()
