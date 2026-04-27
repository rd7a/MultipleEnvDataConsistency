import pytest
import yaml
from pathlib import Path
from http_client import get_with_retry
import logging

logger = logging.getLogger(__name__)
# ---------------------------------------------------------------------------
# CLI flag: --env countries | --env weather | (omit to run both)
# ---------------------------------------------------------------------------
def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default=None,
        choices=["countries", "weather", "iss"],
        help="Run tests for a specific environment: countries or weather",
    )


# ---------------------------------------------------------------------------
# Skip tests that don't belong to the selected environment.
# Matching is done by test node ID (file name contains 'countries' or 'weather').
# ---------------------------------------------------------------------------
def pytest_collection_modifyitems(config, items):
    env = config.getoption("--env")
    
    if env is None:
        return  # no filter — run everything
    skip = pytest.mark.skip(reason=f"--env={env} selected; skipping this environment")
    for item in items:
        if env == "countries" and ("weather" in item.nodeid or "iss" in item.nodeid):
            item.add_marker(skip)
        elif env == "weather" and ("countries" in item.nodeid or "iss" in item.nodeid):
            item.add_marker(skip)
        elif env == "iss" and ("weather" in item.nodeid or "countries" in item.nodeid):
            item.add_marker(skip)


# ---------------------------------------------------------------------------
# Helper: load a single environment block from environments.yaml
# ---------------------------------------------------------------------------
def _load_env(name: str) -> dict:
    config_path = Path(__file__).parent / "config" / "environments.yaml"
    
    with open(config_path) as f:
        return yaml.safe_load(f)[name]


# ---------------------------------------------------------------------------
# Session-scoped fixtures — YAML is read once per pytest session per env
# ---------------------------------------------------------------------------
@pytest.fixture(scope="session")
def countries_config() -> dict:
    """Provides base_url and thresholds for the countries environment."""
    return _load_env("countries")


@pytest.fixture(scope="session")
def weather_config() -> dict:
    """Provides base_url and thresholds for the weather environment."""
    return _load_env("weather")


# ---------------------------------------------------------------------------
# ISS fixture kept here so tests/test_iss_location_fixture.py can still use it
# ---------------------------------------------------------------------------
@pytest.fixture(scope="session")
def iss_response():
    """Single HTTP call to the ISS Now API, shared across the session.
    Retries up to 3 times on transient failures before raising."""
    return get_with_retry("http://api.open-notify.org/iss-now.json")


# ---------------------------------------------------------------------------
# ISS fixture kept here so tests/test_iss_location_fixture.py can still use it
# ---------------------------------------------------------------------------
@pytest.fixture(scope="session")
def iss_config() -> dict:
    """Single HTTP call to the ISS Now API, shared across the session.
    Retries up to 3 times on transient failures before raising."""
    return _load_env("iss")
