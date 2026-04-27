import json
import logging
from pathlib import Path

import allure
import pytest
from http_client import get_with_retry

logger = logging.getLogger(__name__)

from validators.weather_validator import (
    validate_temperature_range,
    validate_hourly_count,
    validate_timezone,
    validate_elevation
)

# ---------------------------------------------------------------------------
# Load city list from test_data/cities.json at collection time
# ---------------------------------------------------------------------------
_cities_path = Path(__file__).parent.parent / "test_data" / "cities.json"
with open(_cities_path) as _f:
    _cities = json.load(_f)

logger.info(f"Current cities test data {_cities} ")
for c in _cities:
    logger.info(f"City {c['name']}")


@allure.feature("weather")
@pytest.mark.parametrize("city", _cities, ids=[c["name"] for c in _cities])
def test_forecast(city: dict, weather_config: dict) -> None:
    """Forecast endpoint must respond within threshold and return valid data for each city."""
    params = {
        "latitude": city["latitude"],
        "longitude": city["longitude"],
        "hourly": "temperature_2m",
    }
    url = f"{weather_config['base_url']}/forecast"
    logger.info("GET %s params=%s", url, params)
    response = get_with_retry(url, params=params)

    # Response time gate — threshold comes from YAML, never hardcoded
    assert response.elapsed.total_seconds() < weather_config["max_response_time"], (
        f"{city['name']}: response took {response.elapsed.total_seconds():.2f}s "
        f"(max {weather_config['max_response_time']}s)"
    )

    data = response.json()

    # Timezone field must be present
    assert validate_timezone(data), f"{city['name']}: timezone field missing or empty"

    #Check whether Elevation is present
    assert validate_elevation(data), f"{city['name']}: elevation field is missing or empty"

    # Hourly temperature entries must exist
    assert validate_hourly_count(data), f"{city['name']}: no hourly temperature entries"

    # All returned temperatures must be within the valid range
    out_of_range = validate_temperature_range(data["hourly"]["temperature_2m"])
    assert not out_of_range, f"{city['name']}: temperatures out of range: {out_of_range}"