import logging
import allure
from http_client import get_with_retry
from validators.countries_validator import validate_country_schema, validate_population

logger = logging.getLogger(__name__)


@allure.feature("countries")
class TestCountries:

    def test_europe_region_count(self, countries_config):
        """GET /region/europe must return more than 40 countries within threshold."""
        url = f"{countries_config['base_url']}/region/europe"
        logger.info("GET %s", url)
        response = get_with_retry(url)
        assert response.elapsed.total_seconds() < countries_config["max_response_time"]
        assert len(response.json()) > 40

    def test_germany_schema(self, countries_config):
        """GET /name/germany must include all required schema fields."""
        url = f"{countries_config['base_url']}/name/germany"
        logger.info("GET %s", url)
        response = get_with_retry(url)
        assert response.elapsed.total_seconds() < countries_config["max_response_time"]
        country = response.json()[0]
        missing = validate_country_schema(country)
        assert not missing, f"Missing fields: {missing}"

    def test_all_countries_population(self, countries_config):
        """Every country returned by /all must have a population greater than zero."""
        url = f"{countries_config['base_url']}/all"
        logger.info("GET %s?fields=name,population", url)
        response = get_with_retry(url, params={"fields": "name,population"})
        assert response.elapsed.total_seconds() < countries_config["max_response_time"]
        invalid = [c for c in response.json() if not validate_population(c)]
        assert not invalid, f"Countries with missing/invalid population field: {[c['name'] for c in invalid]}"

    def test_cross_reference(self, countries_config):
        """A country found via /name must also appear in the /region/europe results."""
        name_url = f"{countries_config['base_url']}/name/germany"
        logger.info("GET %s", name_url)
        name_resp = get_with_retry(name_url)
        germany_name = name_resp.json()[0]["name"]["common"]

        region_url = f"{countries_config['base_url']}/region/europe"
        logger.info("GET %s", region_url)
        region_resp = get_with_retry(region_url)
        region_names = [c["name"]["common"] for c in region_resp.json()]

        assert germany_name in region_names, (
            f"{germany_name} not found in /region/europe results"
        )
