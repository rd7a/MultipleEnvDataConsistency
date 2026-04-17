# Testing Standards

## Parametrization
- Always parametrize from JSON files in `test_data/` — never inline test data inside test functions or parametrize decorators.
- City lists, country lists, and any dataset with more than one entry must live in `test_data/`.

## Schema Validation
- Every endpoint test must include a schema validation step.
- Schema validators live in `src/validators/` — never inline field checks directly in test assertions.

## Response Time
- Response time thresholds must come from the environment fixture (`countries_config` / `weather_config`).
- Never hardcode a seconds value inside test code (e.g., `assert elapsed < 2.0` is forbidden).

## Fixtures
- Use session-scoped fixtures for any HTTP call shared across multiple tests.
- Fixtures that load config or make network calls must be session-scoped to avoid redundant I/O.

## Test Naming
- Test function names must describe the behaviour being validated, not the implementation.
  - Good: `test_europe_region_count`
  - Bad: `test_get_request_1`

## Markers
- All country tests must be in `tests/test_countries.py`.
- All weather tests must be in `tests/test_weather.py`.
- Test files must not import from other test files.

## Allure
- Every test class or module must carry an `@allure.feature(...)` decorator matching its environment name.
