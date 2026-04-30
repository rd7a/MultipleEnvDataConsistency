import pytest
import requests
import logging
from http_client import get_with_retry
from conftest import iss_config

BASE_URL = "http://api.open-notify.org/iss-now.json"
logger = logging.getLogger(__name__)

def get_iss():
    return requests.get(BASE_URL)


# ── Positive Tests ────────────────────────────────────────────────────────────

def test_status_code_200():
    assert get_iss().status_code == 200

def test_message_is_success():
    assert get_iss().json()["message"] == "success"


def test_iss_position_key_present():
    assert "iss_position" in get_iss().json()


def test_latitude_key_present():
    assert "latitude" in get_iss().json()["iss_position"]


def test_longitude_key_present():
    r = get_iss()
    logger.info("Response: ")
    logger.info("%s", r.text)
    logger.info("%s" , str(r.status_code))
    logger.info("%s", r.headers.get("content-type"))
    
    assert "longitude" in get_iss().json()["iss_position"]


def test_latitude_not_empty():
    assert get_iss().json()["iss_position"]["latitude"] != ""


def test_longitude_not_empty():
    assert get_iss().json()["iss_position"]["longitude"] != ""


def test_latitude_is_valid_float():
    lat = float(get_iss().json()["iss_position"]["latitude"])
    assert -90.0 <= lat <= 90.0


def test_longitude_is_valid_float():
    lon = float(get_iss().json()["iss_position"]["longitude"])
    assert -180.0 <= lon <= 180.0


def test_timestamp_present():
    assert "timestamp" in get_iss().json()


def test_timestamp_is_positive_int():
    ts = get_iss().json()["timestamp"]
    assert isinstance(ts, int) and ts > 0


def test_response_is_json():
    response = get_iss()
    assert "application/json" in response.headers["Content-Type"]


@pytest.mark.xfail(reason="intentional failure — elapsed.total_time exceeds abnormally")
def test_response_time_under_5_seconds():
    response = get_iss()
    assert response.elapsed.total_seconds() < 5


# ── Negative Tests ────────────────────────────────────────────────────────────
"""
def test_post_method_not_allowed():
    response = requests.post(BASE_URL)
    assert response.status_code in (404, 405)


def test_invalid_endpoint_returns_404():
    response = requests.get("http://api.open-notify.org/iss-invalid.json")
    assert response.status_code == 404


def test_extra_query_params_ignored():
    response = requests.get(BASE_URL, params={"foo": "bar"})
    assert response.status_code == 200
    assert response.json()["message"] == "success"


def test_latitude_not_out_of_range():
    lat = float(get_iss().json()["iss_position"]["latitude"])
    assert lat != 999 and lat != -999


def test_longitude_not_out_of_range():
    lon = float(get_iss().json()["iss_position"]["longitude"])
    assert lon != 999 and lon != -999


def test_no_unexpected_keys_in_response():
    keys = set(get_iss().json().keys())
    assert keys == {"message", "timestamp", "iss_position"}


def test_no_unexpected_keys_in_iss_position():
    keys = set(get_iss().json()["iss_position"].keys())
    assert keys == {"latitude", "longitude"}
"""
