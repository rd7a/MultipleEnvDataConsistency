# Skill: Test Generator

## Trigger
Use this skill when given: an endpoint URL, HTTP method, and a list of response fields.

## Output
A complete pytest test file with:
- Session-scoped fixture for the HTTP call
- `@allure.feature(...)` decorator matching the environment
- Positive tests: status code, schema validation via `src/validators/`, response time from config
- Negative tests: wrong method, invalid path, extra query params
- Parametrized tests if multiple inputs are provided (data from `test_data/*.json`)
- Type hints on all functions

## Template

```python
import allure
import pytest
import requests
from validators.<name>_validator import validate_<name>_schema


@allure.feature("<environment>")
class Test<Name>:

    def test_status_code(self, <env>_config):
        response = requests.get(f"{<env>_config['base_url']}/<path>")
        assert response.status_code == 200

    def test_response_time(self, <env>_config):
        response = requests.get(f"{<env>_config['base_url']}/<path>")
        assert response.elapsed.total_seconds() < <env>_config["max_response_time"]

    def test_schema(self, <env>_config):
        response = requests.get(f"{<env>_config['base_url']}/<path>")
        item = response.json()[0]
        missing = validate_<name>_schema(item)
        assert not missing, f"Missing fields: {missing}"

    def test_invalid_method(self, <env>_config):
        response = requests.post(f"{<env>_config['base_url']}/<path>")
        assert response.status_code in (404, 405)
```

## Rules
- Thresholds always from fixture — never hardcoded
- Validators always from `src/validators/` — never inline
- Test data always from `test_data/*.json` — never inline
