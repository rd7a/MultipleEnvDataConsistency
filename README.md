# Multiple Environment Data Consistency

A pytest-based API test framework that validates two independent APIs against the same test logic. Environment configuration (base URLs, thresholds) lives entirely in YAML — no hardcoded values in test code.

---

## Targets

| Environment | Base URL | Auth |
|---|---|---|
| `countries` | https://restcountries.com/v3.1 | None |
| `weather` | https://api.open-meteo.com/v1 | None |

---

## Setup Instructions

### Prerequisites
- Python 3.10 or higher
- Java 8+ (required by Allure CLI)

### 1. Clone the repository
```bash
git clone <repo-url>
cd MultipleEnvDataConsistency
```

### 2. Create and activate a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate        # macOS/Linux
.venv\Scripts\activate           # Windows
```

### 3. Install project dependencies
```bash
pip install -e ".[dev]"
```

### 4. Install Allure CLI (for HTML report generation)

**macOS (via Homebrew):**
```bash
brew install allure
```

**macOS/Linux (manual):**
```bash
curl -L https://github.com/allure-framework/allure2/releases/download/2.30.0/allure-2.30.0.tgz -o allure.tgz
tar -xzf allure.tgz
sudo mv allure-2.30.0 /usr/local/allure
echo 'export PATH=$PATH:/usr/local/allure/bin' >> ~/.zshrc
source ~/.zshrc
```

---

## How to Run Tests Locally

### Run all tests (both environments)
```bash
pytest -v
```

### Run countries tests only
```bash
pytest --env countries -v
```

### Run weather tests only
```bash
pytest --env weather -v
```

### Run a single test by name
```bash
pytest tests/test_countries.py::TestCountries::test_germany_schema -v
```

### Run tests with live log output (request URLs visible)
Logging is enabled by default (`log_cli = true` in `pyproject.toml`). No extra flags needed.

### Generate and open the Allure report
```bash
# After running tests, generate the report:
allure generate reports/allure-results -o reports/allure-report --clean

# Open in browser:
allure open reports/allure-report

# Restart the Allure server if needed:
pkill -f allure
allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allure-report
```

### HTML report
A self-contained HTML report is auto-generated at `reports/report.html` after every test run.

---

## How to Interpret Test Results

### Terminal output
```
tests/test_countries.py::TestCountries::test_europe_region_count
-------------------------------- live log call ---------------------------------
INFO  GET https://restcountries.com/v3.1/region/europe
PASSED
```
- Each test logs the exact request URL at INFO level before making the call.
- `PASSED` / `FAILED` / `SKIPPED` shown per test.
- `SKIPPED` means the test belongs to a different environment than the one selected via `--env`.

### Allure report sections
The Allure report is split by `@allure.feature`:
- **countries** — all tests in `tests/test_countries.py`
- **weather** — all tests in `tests/test_weather.py` (parametrized per city)

### What each test validates

**Countries (`--env countries`)**

| Test | Endpoint | Validates |
|---|---|---|
| `test_europe_region_count` | `GET /region/europe` | Result count > 40, response time within threshold |
| `test_germany_schema` | `GET /name/germany` | All required fields present: `name`, `capital`, `population`, `currencies`, `languages` |
| `test_all_countries_population` | `GET /all?fields=name,population` | Every country has a non-negative integer population |
| `test_cross_reference` | `/name/germany` + `/region/europe` | A country found by name also appears in regional results |

**Weather (`--env weather`)**

| Test | Endpoint | Validates |
|---|---|---|
| `test_forecast[<city>]` | `GET /forecast?latitude=...&longitude=...` | Temperature range (-80 to 60°C), hourly entry count > 0, timezone field present, response time within threshold |

Cities tested: London, Tokyo, New York, Sydney, Cairo (defined in `test_data/cities.json`).

### CI pipeline
The GitHub Actions workflow (`.github/workflows/ci.yml`) runs on every push. If any test fails, the pipeline fails. Reports are uploaded as downloadable artifacts under the **Actions** tab.

---

## Assumptions and Design Decisions

### 1. YAML-driven configuration — no hardcoded values
All base URLs and thresholds (`max_response_time`, `min_results_count`) live in `config/environments.yaml`. Tests receive these values via session-scoped fixtures (`countries_config`, `weather_config`). Adding a new environment requires only a new YAML block — zero code changes.

### 2. Collection-time skipping via `pytest_collection_modifyitems`
When `--env countries` is passed, weather tests are skipped at **collection time** — before fixtures are set up. This avoids unnecessary HTTP calls. Skipping inside a fixture would still initialize the session and make the first request.

### 3. Population 0 is valid data
Some uninhabited territories (e.g. Bouvet Island, Heard Island) are returned by the REST Countries API with `population: 0`. The validator uses `>= 0` rather than `> 0` to reflect this real-world data correctly.

### 4. Validators are pure functions in `src/validators/`
All schema and field validation logic is in `src/validators/`, not inlined in tests. Validators return data (missing fields, out-of-range values) rather than raising exceptions, so test assertions carry the full context of what failed.

### 5. Session-scoped fixtures for shared API calls
The `iss_response`, `countries_config`, and `weather_config` fixtures are session-scoped — the YAML file is read once and HTTP calls are made once per session, not once per test.

### 6. Test data from JSON, never inline
City coordinates live in `test_data/cities.json`. Adding a new city to the parametrized weather test requires only editing the JSON file.

### 7. Logging over print statements
Request URLs are logged using Python's `logging` module (`logger.info`), not `print`. This integrates with pytest's `--log-cli-level`, Allure, and the HTML report automatically.
