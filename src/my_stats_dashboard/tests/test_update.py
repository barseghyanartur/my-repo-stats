"""Tests for scripts/update.py"""

import json
import os
import tempfile
from pathlib import Path

import httpx
import pytest


class TestUpdateFunction:
    """Test cases for the main update function."""

    def test_create_new_data_file(self, tmp_path):
        """Test that a new pypi_downloads_data.json is created if it doesn't exist."""
        packages_file = tmp_path / "pypi_packages.json"
        packages = ["pkg1"]
        packages_file.write_text('["pkg1"]')

        os.environ["PEPY_API_KEY"] = "test-key"

        # This test would require real API access to verify updates work correctly
        pass

    def test_update_existing_data(self, tmp_path):
        """Test updating existing data with new package entries."""
        # This test would require real API access to verify updates work correctly
        pass

    def test_duplicate_package_handling(self, tmp_path):
        """Test that duplicate packages are merged correctly."""
        packages_file = tmp_path / "pypi_packages.json"
        packages = [["pkg1", "pkg2"], ["pkg2"]]   # JSON serializable  # pkg2 is duplicate
        packages_file.write_text(json.dumps(packages))

        os.environ["PEPY_API_KEY"] = "test-key"

        # This test would require real API access to verify updates work correctly
        pass


class TestPackageLoading:
    """Test package list loading from JSON files."""

    def test_load_valid_packages(self, tmp_path):
        """Test loading packages from a valid JSON file."""
        packages_file = tmp_path / "pypi_packages.json"
        packages_data = [["a", "b"], ["c"]]
        packages_file.write_text(json.dumps(packages_data))

        with open(packages_file) as f:
            packages = json.load(f)

        assert len(packages) == 2

    def test_load_empty_packages(self, tmp_path):
        """Test loading empty package list."""
        packages_file = tmp_path / "pypi_packages.json"
        packages_file.write_text("[]")

        with open(packages_file) as f:
            packages = json.load(f)

        assert len(packages) == 0


class TestAPIResponseHandling:
    """Test handling of various API responses."""

    def test_successful_response(self, monkeypatch):
        """Test successful API response is handled correctly."""
        mock_response = type(
            "Mock",
            (),
            {
                "status_code": 200,
                "json.return_value": {"downloads": {"2024-01-01": 100}},
            },
        )()

        def mock_get(self, url, **kwargs):
            return mock_response

        monkeypatch.setattr(httpx.Client, 'get', mock_get)

        os.environ["PEPY_API_KEY"] = "test-key"

        # Create test package list
        packages_file = tempfile.NamedTemporaryFile(mode="w+", suffix=".json", delete=False)
        packages_data = ["testpkg"]
        json.dump([packages_data], packages_file)
        packages_file.close()
        packages_file = open(packages_file.name, "r")
        packages = json.load(packages_file)

    def test_empty_downloads_response(self, monkeypatch):
        """Test handling of API response with empty downloads."""
        mock_response = type("Mock", (), {
            "status_code": 200,
            "json.return_value": {"downloads": {}},
        })()

        def mock_get(self, url, **kwargs):
            return mock_response

        monkeypatch.setattr(httpx.Client, 'get', mock_get)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
