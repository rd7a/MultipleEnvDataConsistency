import allure
from http_client import get_with_retry
import logging


logger = logging.getLogger(__name__)

@allure.feature("iss")
class TestIssLocation:

    def test_status_code_200(self, iss_config):
        iss_config_response = get_with_retry(iss_config['base_url'])
        logger.info(f"iss base url {iss_config['base_url']}")
        assert iss_config_response.status_code == 200

    def test_latitude_key_present(self, iss_config):
        iss_config_response = get_with_retry(iss_config['base_url'])
        assert "latitude" in iss_config_response.json()["iss_position"]


    def test_longitude_key_present(self, iss_config):
        iss_config_response = get_with_retry(iss_config['base_url'])
        assert "longitude" in iss_config_response.json()["iss_position"]


    def test_latitude_not_empty(self, iss_config):
        iss_config_response = get_with_retry(iss_config['base_url'])
        assert iss_config_response.json()["iss_position"]["latitude"] != ""


    def test_longitude_not_empty(self, iss_config):
        iss_config_response = get_with_retry(iss_config['base_url'])
        assert iss_config_response.json()["iss_position"]["longitude"] != ""