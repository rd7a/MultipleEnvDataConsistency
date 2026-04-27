
BASE_URL = "http://api.open-notify.org/iss-now.json"


# ── Positive Tests (all use session-scoped fixture — 1 HTTP call total) ───────


def test_status_code_200(iss_response):
    assert iss_response.status_code == 200    


def test_message_is_success(iss_response):
    assert iss_response.json()["message"] == "success"


def test_iss_position_key_present(iss_response):
    assert "iss_position" in iss_response.json()


def test_latitude_key_present(iss_response):
    assert "latitude" in iss_response.json()["iss_position"]


def test_longitude_key_present(iss_response):
    assert "longitude" in iss_response.json()["iss_position"]


def test_latitude_not_empty(iss_response):
    assert iss_response.json()["iss_position"]["latitude"] != ""


def test_longitude_not_empty(iss_response):
    assert iss_response.json()["iss_position"]["longitude"] != ""

"""
def test_latitude_is_valid_float(iss_response):
    lat = float(iss_response.json()["iss_position"]["latitude"])
    assert -90.0 <= lat <= 90.0


def test_longitude_is_valid_float(iss_response):
    lon = float(iss_response.json()["iss_position"]["longitude"])
    assert -180.0 <= lon <= 180.0


def test_timestamp_present(iss_response):
    assert "timestamp" in iss_response.json()


def test_timestamp_is_positive_int(iss_response):
    ts = iss_response.json()["timestamp"]
    assert isinstance(ts, int) and ts > 0


def test_response_is_json(iss_response):
    assert "application/json" in iss_response.headers["Content-Type"]


def test_response_time_under_5_seconds(iss_response):
    assert iss_response.elapsed.total_seconds() < 5


# ── Negative Tests (these inherently need separate calls) ─────────────────────

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


def test_latitude_not_out_of_range(iss_response):
    lat = float(iss_response.json()["iss_position"]["latitude"])
    assert lat != 999 and lat != -999


def test_longitude_not_out_of_range(iss_response):
    lon = float(iss_response.json()["iss_position"]["longitude"])
    assert lon != 999 and lon != -999


def test_no_unexpected_keys_in_response(iss_response):
    assert set(iss_response.json().keys()) == {"message", "timestamp", "iss_position"}


def test_no_unexpected_keys_in_iss_position(iss_response):
    assert set(iss_response.json()["iss_position"].keys()) == {"latitude", "longitude"}
"""